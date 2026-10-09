#!/usr/bin/env python3
"""Validate SPC 2026 sample prompt output before submission.

Why this exists
---------------
The SPC 2026 documentation ("What should I avoid?") tells consultants to verify
every ISIN with a script before pasting the JSON sample output into the
submission form, and shows a ``stdnum``-based snippet. Submitting a
non-existent or structurally incorrect ISIN, or output that is not valid JSON
in the exact required shape, costs that prompt its PnL for the day.

This script is a dependency-free version of that check. It validates:

1. ISIN structure: ``^[A-Z]{2}[A-Z0-9]{9}[0-9]$`` plus the Luhn check digit
   (letters mapped A=10 .. Z=35, then Luhn over the full string).
2. MIC structure: 4 characters, first alphabetic, remainder alphanumeric.
3. JSON output shape: a top-level list of objects, each with exactly the seven
   required keys, correct types, ``-1 <= confidence_score <= 1``,
   ``investment_horizon`` a positive integer, and ``return_prediction`` a
   positive number.

It also reports portfolio-level warnings (duplicate ISINs, all-flat book,
coverage against the ~500 stock guideline, long/short split).

Scope limits (intentional)
--------------------------
* MIC codes are checked for structure only. ISO 10383 registry membership is
  not bundled, so ``ZZZZ`` passes structure. Cross-check unknown exchanges by
  hand.
* ISIN country prefixes are checked for shape only, not against ISO 3166.
* ``stdnum`` is used as an optional cross-check when it happens to be
  installed; its absence never changes the verdict.

Usage
-----
    python3 Tools/validate_spc_isin.py Tools/spc_sample_output_example.json
    python3 Tools/validate_spc_isin.py --isin US0378331005 --isin US5949181046
    python3 Tools/validate_spc_isin.py --selftest

Exit codes: 0 = all valid, 1 = problems found, 2 = usage/IO error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

ISIN_RE = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
MIC_RE = re.compile(r"^[A-Z][A-Z0-9]{3}$")
UNKNOWN_MIC_PLACEHOLDER = "ZZZZ"

REQUIRED_FIELDS: tuple[str, ...] = (
    "company_name",
    "ticker",
    "isin",
    "mic",
    "confidence_score",
    "investment_horizon",
    "return_prediction",
)

DOCUMENTED_STOCK_COVERAGE_TARGET = 500
DOCUMENTED_STOCKS_PER_PROMPT = 50
MAX_PROMPT_CHARS = 10_000

try:  # optional cross-check only
    from stdnum import isin as _std_isin
    from stdnum.exceptions import ValidationError as _StdnumError

    _HAVE_STDNUM = True
except ImportError:  # pragma: no cover - depends on environment
    _std_isin = None
    _StdnumError = Exception
    _HAVE_STDNUM = False


def _luhn_ok(digits: str) -> bool:
    """Luhn check over a decimal digit string (rightmost digit not doubled)."""
    total = 0
    for index, char in enumerate(reversed(digits)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0


def validate_isin(isin: Any) -> tuple[bool, str]:
    """Return (ok, reason) for an ISIN string."""
    if not isinstance(isin, str):
        return False, f"not a string ({type(isin).__name__})"
    candidate = isin.strip()
    if not candidate:
        return False, "empty"
    if candidate != isin:
        return False, "leading/trailing whitespace"
    if candidate != candidate.upper():
        return False, "not uppercase (ISINs must be uppercase)"
    if len(candidate) != 12:
        return False, f"length {len(candidate)}, expected 12"
    if not ISIN_RE.match(candidate):
        return False, "layout must be 2 letters, 9 alphanumeric, 1 digit"

    expanded = "".join(str(int(char, 36)) for char in candidate)
    if not _luhn_ok(expanded):
        return False, "Luhn check digit failed"

    if _HAVE_STDNUM:
        assert _std_isin is not None
        try:
            _std_isin.validate(candidate)
        except _StdnumError as exc:  # pragma: no cover - optional dependency
            return False, f"stdnum rejected: {type(exc).__name__}"

    return True, "valid_format_and_check_digit"


def validate_mic(mic: Any) -> tuple[bool, str]:
    """Return (ok, reason) for a MIC string. Structure only, no registry check."""
    if not isinstance(mic, str):
        return False, f"not a string ({type(mic).__name__})"
    if not mic:
        return False, "empty"
    if mic != mic.upper():
        return False, "not uppercase (MICs must be uppercase)"
    if not MIC_RE.match(mic):
        return False, "must be 4 characters: a letter followed by 3 alphanumerics"
    if mic == UNKNOWN_MIC_PLACEHOLDER:
        return False, f"{UNKNOWN_MIC_PLACEHOLDER} is a placeholder, not a real MIC"
    return True, "valid_structure"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_horizon(value: Any) -> tuple[bool, str]:
    if isinstance(value, bool) or not isinstance(value, int):
        return False, "investment_horizon must be an integer"
    if value <= 0:
        return False, "investment_horizon must be positive"
    if value > 1500:
        return False, f"investment_horizon {value} looks implausible (trading days)"
    return True, "ok"


def validate_return_prediction(value: Any) -> tuple[bool, str]:
    if not _is_number(value):
        return False, "return_prediction must be a number"
    if value <= 0:
        return False, "return_prediction must be positive; direction comes from confidence_score"
    if value > 5:
        return False, f"return_prediction {value} looks implausible for a per-horizon return"
    return True, "ok"


def validate_confidence(value: Any) -> tuple[bool, str]:
    if not _is_number(value):
        return False, "confidence_score must be a number"
    if not -1.0 <= float(value) <= 1.0:
        return False, "confidence_score must be between -1 and 1"
    return True, "ok"


def validate_payload(payload: Any) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate the whole sample output. Returns (errors, warnings, stats)."""
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, Any] = {
        "rows": 0,
        "long": 0,
        "short": 0,
        "flat": 0,
        "unique_isins": 0,
        "valid_scores": 0,
    }

    if not isinstance(payload, list):
        return [f"top level must be a JSON list, got {type(payload).__name__}"], warnings, stats
    if not payload:
        return ["top level list is empty"], warnings, stats

    stats["rows"] = len(payload)
    seen_isins: dict[str, int] = {}

    for row_index, row in enumerate(payload):
        where = f"row {row_index}"
        if not isinstance(row, dict):
            errors.append(f"{where}: must be an object, got {type(row).__name__}")
            continue

        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            errors.append(f"{where}: missing required field(s): {', '.join(missing)}")
        extra = [field for field in row if field not in REQUIRED_FIELDS]
        if extra:
            warnings.append(f"{where}: unexpected extra field(s): {', '.join(extra)}")

        isin = row.get("isin")
        ok, reason = validate_isin(isin)
        if not ok:
            errors.append(f"{where}: isin {isin!r} invalid - {reason}")
        else:
            stats["unique_isins"] += 0 if isin in seen_isins else 1
            if isin in seen_isins:
                warnings.append(
                    f"{where}: duplicate isin {isin} (also on row {seen_isins[isin]})"
                )
            else:
                seen_isins[isin] = row_index

        ok, reason = validate_mic(row.get("mic"))
        if not ok:
            errors.append(f"{where}: mic {row.get('mic')!r} invalid - {reason}")

        score = row.get("confidence_score")
        ok, reason = validate_confidence(score)
        if not ok:
            errors.append(f"{where}: confidence_score {score!r} invalid - {reason}")
        else:
            score = float(score)
            stats["valid_scores"] += 1
            if score > 0:
                stats["long"] += 1
            elif score < 0:
                stats["short"] += 1
            else:
                stats["flat"] += 1

        ok, reason = validate_horizon(row.get("investment_horizon"))
        if not ok:
            errors.append(f"{where}: investment_horizon {row.get('investment_horizon')!r} invalid - {reason}")

        ok, reason = validate_return_prediction(row.get("return_prediction"))
        if not ok:
            errors.append(f"{where}: return_prediction {row.get('return_prediction')!r} invalid - {reason}")

        for text_field in ("company_name", "ticker"):
            value = row.get(text_field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{where}: {text_field} must be a non-empty string")

    if stats["valid_scores"] and stats["long"] + stats["short"] == 0:
        warnings.append(
            "every confidence_score is 0 - the book is flat and generates no PnL"
        )
    if stats["valid_scores"] and stats["short"] == 0 and stats["long"] > 0:
        warnings.append("no short positions; consider whether the thesis is one-sided by design")
    if stats["rows"] and stats["rows"] != DOCUMENTED_STOCKS_PER_PROMPT and abs(
        stats["rows"] - DOCUMENTED_STOCKS_PER_PROMPT
    ) > 20:
        warnings.append(
            f"{stats['rows']} rows vs the ~{DOCUMENTED_STOCKS_PER_PROMPT} equities per prompt "
            "recommended for efficient token usage"
        )
    if stats["unique_isins"]:
        warnings.append(
            f"this prompt covers {stats['unique_isins']} unique ISINs; the across-prompts "
            f"coverage target is {DOCUMENTED_STOCK_COVERAGE_TARGET} different stocks"
        )

    return errors, warnings, stats


def _selftest() -> int:
    """Run built-in cases. Returns 0 on success, 1 on unexpected results."""
    known_valid = [
        "US0378331005",
        "US5949181045",
        "US67066G1040",
        "US88160R1014",
        "US4581401001",
    ]
    known_invalid = [
        ("US5949181046", "bad check digit"),
        ("US594918104", "too short"),
        ("us5949181045", "lowercase"),
        ("US594918104!", "punctuation"),
        ("ZZ0000000000", "bad check digit on placeholder prefix"),
    ]

    failures: list[str] = []
    for isin in known_valid:
        ok, reason = validate_isin(isin)
        if not ok:
            failures.append(f"expected valid, got invalid: {isin} ({reason})")
    for isin, label in known_invalid:
        ok, reason = validate_isin(isin)
        if ok:
            failures.append(f"expected invalid ({label}), got valid: {isin}")

    for mic, should_pass in [("XNAS", True), ("XETR", True), ("xnas", False), ("ZZZZ", False), ("XN", False)]:
        ok, _ = validate_mic(mic)
        if ok != should_pass:
            failures.append(f"mic {mic!r}: expected ok={should_pass}, got ok={ok}")

    for score, should_pass in [(0.82, True), (-0.58, True), (0.0, True), (1.0, True), (-1.0, True), (1.01, False), (-2, False)]:
        ok, _ = validate_confidence(score)
        if ok != should_pass:
            failures.append(f"confidence {score}: expected ok={should_pass}, got ok={ok}")

    for horizon, should_pass in [(22, True), (1, True), (0, False), (-5, False), (22.5, False), ("22", False)]:
        ok, _ = validate_horizon(horizon)
        if ok != should_pass:
            failures.append(f"horizon {horizon!r}: expected ok={should_pass}, got ok={ok}")

    for prediction, should_pass in [(0.045, True), (0.001, True), (0.0, False), (-0.02, False), ("0.04", False)]:
        ok, _ = validate_return_prediction(prediction)
        if ok != should_pass:
            failures.append(f"return_prediction {prediction!r}: expected ok={should_pass}, got ok={ok}")

    good_payload = [
        {"company_name": "Apple Inc.", "ticker": "AAPL", "isin": "US0378331005", "mic": "XNAS",
         "confidence_score": 0.82, "investment_horizon": 22, "return_prediction": 0.045},
    ]
    errors, _, _ = validate_payload(good_payload)
    if errors:
        failures.append(f"well-formed single-row payload reported errors: {errors}")

    bad_payload = [
        {"company_name": "Apple Inc.", "ticker": "AAPL", "isin": "US0378331006", "mic": "xnax",
         "confidence_score": 1.4, "investment_horizon": 0, "return_prediction": -0.01},
    ]
    errors, _, _ = validate_payload(bad_payload)
    if len(errors) != 5:
        failures.append(f"malformed payload should raise 5 errors, got {len(errors)}: {errors}")

    if not isinstance(validate_payload({"not": "a list"})[0], list):
        failures.append("non-list payload should report an error")

    if failures:
        print("SELFTEST FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("SELFTEST PASSED")
    print(f"  ISIN cases: {len(known_valid)} valid, {len(known_invalid)} invalid")
    print(f"  stdnum cross-check active: {_HAVE_STDNUM}")
    return 0


def _report(errors: list[str], warnings: list[str], stats: dict[str, Any], label: str) -> int:
    print(f"Checked: {label}")
    if stats:
        print(
            "  rows={rows} unique_isins={unique_isins} valid_scores={valid_scores} "
            "long={long} short={short} flat={flat}".format(**stats)
        )
    for warning in warnings:
        print(f"  WARN  {warning}")
    for error in errors:
        print(f"  ERROR {error}")
    if errors:
        print(f"RESULT: INVALID ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"RESULT: VALID ({len(warnings)} warning(s))")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SPC 2026 sample prompt output.")
    parser.add_argument("path", nargs="?", help="path to a JSON file holding the sample output")
    parser.add_argument("--isin", action="append", default=[], help="validate a single ISIN (repeatable)")
    parser.add_argument("--json-text", help="validate a JSON string given inline")
    parser.add_argument("--selftest", action="store_true", help="run built-in test cases and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()

    if args.isin:
        if args.path or args.json_text:
            print("error: pass --isin or a JSON source, not both", file=sys.stderr)
            return 2
        errors: list[str] = []
        warnings: list[str] = []
        for isin in args.isin:
            ok, reason = validate_isin(isin)
            print(f"{'OK   ' if ok else 'BAD  '} {isin:<14} {reason}")
            if not ok:
                errors.append(isin)
        print(f"RESULT: {'INVALID' if errors else 'VALID'} ({len(args.isin) - len(errors)}/{len(args.isin)} valid)")
        return 1 if errors else 0

    if args.json_text:
        try:
            payload = json.loads(args.json_text)
        except json.JSONDecodeError as exc:
            print(f"ERROR: not valid JSON - {exc}", file=sys.stderr)
            return 1
        label = "inline JSON"
    elif args.path:
        try:
            with open(args.path, encoding="utf-8") as handle:
                payload = json.load(handle)
        except OSError as exc:
            print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print(f"ERROR: {args.path} is not valid JSON - {exc}", file=sys.stderr)
            return 1
        label = args.path
    else:
        parser.print_help()
        return 2

    errors, warnings, stats = validate_payload(payload)
    return _report(errors, warnings, stats, label)


if __name__ == "__main__":
    sys.exit(main())
