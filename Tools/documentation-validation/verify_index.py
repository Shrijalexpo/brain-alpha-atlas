#!/usr/bin/env python3
"""Reconcile the experiment index with its canonical sources.

Authority hierarchy
-------------------
Every fact in this repository has exactly one authoritative home:

1. ``simulations/NNN_*.md`` -- the experiment records. Status, expression, metrics and
   lessons live here.
2. ``simulations/sweeps/*.csv`` -- the per-block sweep data. Block counts, per-block
   metrics, and PASS/PENDING tallies live here.
3. ``docs/10-experiment-index.md`` -- a *derived display* of 1 and 2. It is never the
   authority; this tool exists to prove it has not drifted.

The index is verified rather than generated, because its lesson column is deliberately
condensed prose. Every row must resolve to a canonical record, every metric cell must agree
with that record, every status must match the record's own status, and every sweep number
must be reproducible from the CSV files.

Normalisation rules (the only ones permitted)
---------------------------------------------
* Whitespace is collapsed to single spaces. A display expression may be a truncation of the
  canonical expression and must then be an exact whitespace-insensitive prefix of it.
* Numeric comparison is string equality after removing thousands separators, a trailing
  percent sign, a leading plus sign, and normalising the Unicode minus sign (U+2212).
* A display value that is not a bare number is *annotated*: every number it contains must
  appear verbatim in the canonical field. ``0.73 in IS summary`` passes against a record
  field of the same text; a bare display of ``0.73`` would not.
* ``—`` means "not shown in the index". If the record does hold the value, that is reported
  as a warning (lost detail), never as an error (wrong fact).

Nothing here touches the network or the live BRAIN API.

Usage
-----
    python3 Tools/documentation-validation/verify_index.py --selftest
    python3 Tools/documentation-validation/verify_index.py                 # repository rooted at this script's parent
    python3 Tools/documentation-validation/verify_index.py --root DIR

Exit codes: 0 = consistent, 1 = at least one error, 2 = usage/IO problem.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_docs import split_row  # noqa: E402  shared, backtick-aware table parser

INDEX_REL = os.path.join("Analysis and Simulation Reports", "index.md")
RECORD_DIR = os.path.join("Analysis and Simulation Reports", "simulation-results")
SWEEP_DIR = os.path.join("Analysis and Simulation Reports", "sweeps-and-experiments")

EXPERIMENT_SECTIONS = (
    "Experiments that cleared the checks",
    "Failed on self-correlation (metrics were acceptable)",
    "Errors (expression did not validate)",
    "Failed experiments (chronological)",
)
SWEEP_SECTION = "Bulk sweeps"

# Index section -> statuses its records are allowed to carry.
SECTION_STATUSES = {
    "Experiments that cleared the checks": {"PASSED_SUBMITTABLE", "PASSED_SUBMITTED"},
    "Failed on self-correlation (metrics were acceptable)": {"FAILED_SELF_CORRELATION"},
    "Errors (expression did not validate)": {"ERROR"},
    "Failed experiments (chronological)": {"FAILED", "NO_REPEAT"},
    "Bulk sweeps": {"FAILED"},
}

KNOWN_STATUSES = {
    "PASSED_SUBMITTABLE",
    "PASSED_SUBMITTED",
    "FAILED_SELF_CORRELATION",
    "FAILED",
    "ERROR",
    "NO_REPEAT",
    "PENDING",
    "QUEUED",
}

# Statuses meaning "the platform cleared the checks". Used to ensure an unevaluated block is
# never presented as a pass.
CLEARED_STATUSES = {"PASSED_SUBMITTABLE", "PASSED_SUBMITTED"}

# Index metric columns -> canonical record field name.
METRIC_COLUMNS = (("Sharpe", 2), ("Fitness", 3), ("Turnover", 4))

# Region vocabulary we are willing to verify against sweep dump names / universe values.
REGION_TOKENS = {
    "USA", "EUR", "ASI", "CHN", "KOR", "AMR", "GLB", "ALL", "JPN", "HKG", "TWN",
    "IND", "GBR", "DEU", "MENA", "BRA",
}
UNIVERSE_RE = re.compile(r"^(?:TOP[A-Z0-9]*|TOPSP\d+|LARGE|MINVOL[A-Z0-9]+|ILLIQUID[A-Z0-9]*|TOPCS\d+)$")

RECORD_FILE_RE = re.compile(r"^(\d{3})_.*\.md$")
EXPRESSION_FENCE_RE = re.compile(r"Expression:\s*\n+```text\n(.*?)\n```", re.S)
FIELD_RE = re.compile(r"^([A-Z][A-Za-z /-]*?):\s*(.*)$")
CSV_REF_RE = re.compile(r"`?((?:simulations/sweeps|Analysis and Simulation Reports/sweeps-and-experiments|sweeps-and-experiments)/[A-Za-z0-9_.\-]+\.csv)`?")
BARE_CSV_RE = re.compile(r"(?<![\w/])(\d{8}_\d{6}[A-Za-z0-9_\-]*\.csv)")


class Finding:
    """One inconsistency, addressed to a specific experiment id."""

    __slots__ = ("level", "code", "where", "message")

    def __init__(self, level: str, code: str, where: str, message: str) -> None:
        self.level, self.code, self.where, self.message = level, code, where, message

    def __str__(self) -> str:
        return f"{self.level:<5} {self.code:<24} {self.where:<6} {self.message}"


# --------------------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------------------

def norm_number(text: str) -> str:
    """Canonical numeric string, or '' when the text is not a bare number."""
    value = (text or "").strip().replace("\u2212", "-")
    if value.startswith("+"):
        value = value[1:]
    value = value.replace(",", "")
    if value.endswith("%"):
        value = value[:-1].strip()
    return value if re.match(r"^-?\d+(?:\.\d+)?$", value) else ""


def norm_text(text: str) -> str:
    """Collapse whitespace runs to single spaces."""
    return re.sub(r"\s+", " ", text or "").strip()


def numbers_in(text: str) -> list[str]:
    """Every number in the text, with thousands separators removed (``2,100`` -> ``2100``)."""
    cleaned = (text or "").replace("\u2212", "-")
    return [m.replace(",", "") for m in re.findall(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?", cleaned)]


def round2(value: str) -> str:
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return ""


# --------------------------------------------------------------------------------------
# Loading the canonical sources
# --------------------------------------------------------------------------------------

def load_records(root: str) -> dict[str, dict]:
    """id -> {path, text, fields, status, expression, title, mentions_pending}."""
    records: dict[str, dict] = {}
    directory = os.path.join(root, RECORD_DIR)
    if not os.path.isdir(directory):
        return records
    discovered_paths: list[tuple[str, str]] = []
    for base, _dirs, names in os.walk(directory):
        for name in sorted(names):
            if RECORD_FILE_RE.match(name):
                discovered_paths.append((name, os.path.join(base, name)))
    for name, path in sorted(discovered_paths, key=lambda x: x[0]):
        match = RECORD_FILE_RE.match(name)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        fields: dict[str, str] = {}
        for line in text.splitlines():
            found = FIELD_RE.match(line)
            if found:
                fields.setdefault(found.group(1).strip(), found.group(2).strip())
        status_raw = fields.get("Status", "")
        status = status_raw.split("|")[0].split("(")[0].strip()
        expression = EXPRESSION_FENCE_RE.search(text)
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = re.sub(r"^Simulation\s+\d+\s*[-—:]\s*", "", line[2:].strip())
                break
        records[match.group(1)] = {
            "path": os.path.relpath(path, root),
            "text": text,
            "fields": fields,
            "status": status,
            "status_raw": status_raw,
            "expression": expression.group(1) if expression else None,
            "title": title,
            "mentions_pending": bool(re.search(r"\bPENDING\b", text)),
        }
    return records


def sweep_csv_paths(record: dict, root: str) -> list[str]:
    """CSV files a sweep record names, as repo-relative paths, in first-mention order.

    Records name their artefacts either with a full ``simulations/sweeps/...`` path or with
    a bare filename inside a fence, so both forms are accepted. References to
    ``superseded/`` files are historical mentions and are ignored. When a record names only
    a combined ``<stem>_all_results.csv``, the per-dump ``<stem>_d*.csv`` siblings are added,
    because the index's block-count and page claims are checked against them.
    """
    text = record["text"]
    found = list(CSV_REF_RE.findall(text))
    found += [os.path.join(SWEEP_DIR, name) for name in BARE_CSV_RE.findall(text)]

    out: list[str] = []
    for path in found:
        if path.startswith("sweeps-and-experiments/"):
            path = os.path.join("Analysis and Simulation Reports", path)
        elif path.startswith("simulations/sweeps/") and not os.path.exists(os.path.join(root, path)):
            alt = os.path.join(SWEEP_DIR, os.path.basename(path))
            if os.path.exists(os.path.join(root, alt)):
                path = alt
        if "superseded" in path or path in out:
            continue
        out.append(path)

    directory = os.path.join(root, SWEEP_DIR)
    for path in list(out):
        if not path.endswith("all_results.csv"):
            continue
        stem = os.path.basename(path)[: -len("all_results.csv")]
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.startswith(stem) and re.match(rf"^{re.escape(stem)}d\d+.*\.csv$", name):
                sibling = os.path.join(SWEEP_DIR, name)
                if sibling not in out:
                    out.append(sibling)
    return out


def read_csv(root: str, rel_path: str) -> list[dict]:
    with open(os.path.join(root, rel_path), newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# --------------------------------------------------------------------------------------
# Parsing the index
# --------------------------------------------------------------------------------------

def parse_index(text: str) -> tuple[dict[str, list[dict]], list[Finding]]:
    """Return {section: [row]} plus structural findings."""
    rows: dict[str, list[dict]] = {name: [] for name in SECTION_STATUSES}
    findings: list[Finding] = []
    section = None

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section not in SECTION_STATUSES or not line.startswith("|"):
            continue
        if set(line) <= set("|-: ") or re.match(r"^\|\s*(?:ID|#)", line):
            continue
        cells = split_row(line)
        if not cells or not re.match(r"^\d{3}$", cells[0]):
            continue
        expected = 5 if section == SWEEP_SECTION else 7
        if len(cells) != expected:
            findings.append(Finding("ERROR", "row-shape", cells[0],
                                    f"expected {expected} cells, found {len(cells)} (line {lineno})"))
            continue
        rows[section].append({"id": cells[0], "cells": cells, "line": lineno})
    return rows, findings


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

def check_metric(findings: list[Finding], where: str, column: str,
                 index_value: str, canonical: str) -> None:
    display = (index_value or "").strip()
    if display in ("", "—"):
        if norm_number(canonical):
            findings.append(Finding("WARN", "metric-omitted", where,
                                    f"{column}: index shows '{display or 'nothing'}' but the record has {canonical}"))
        return
    display_num, canonical_num = norm_number(display), norm_number(canonical)
    if display_num:
        if not canonical_num:
            findings.append(Finding("ERROR", "metric-value", where,
                                    f"{column}: index shows {display}, record field is '{canonical or 'absent'}'"))
        elif display_num != canonical_num:
            findings.append(Finding("ERROR", "metric-value", where,
                                    f"{column}: index {display} vs record {canonical}"))
        return
    numbers = numbers_in(display)
    if not numbers:
        findings.append(Finding("ERROR", "metric-shape", where,
                                f"{column}: cannot interpret display '{display}'"))
        return
    for number in numbers:
        if number not in canonical:
            findings.append(Finding("ERROR", "metric-value", where,
                                    f"{column}: annotated display '{display}' is not supported by "
                                    f"record field '{canonical or 'absent'}'"))
            return


def check_expression(findings: list[Finding], where: str, index_cell: str, record: dict) -> None:
    canonical_raw = record["expression"]
    spans = re.findall(r"`([^`]*)`", index_cell)
    if not spans:
        if canonical_raw:
            findings.append(Finding("ERROR", "expression-missing", where,
                                    "record has an expression but the index row shows none"))
        return
    display_raw = max(spans, key=len)
    truncated = display_raw.rstrip().endswith("…")
    display = norm_text(display_raw.rstrip().rstrip("…").rstrip())
    if canonical_raw is None:
        findings.append(Finding("ERROR", "expression-missing", where,
                                "index quotes an expression but the record has none"))
        return
    canonical = norm_text(canonical_raw)
    if display and not canonical.startswith(display):
        findings.append(Finding("ERROR", "expression-prefix", where,
                                f"index expression is not a prefix of the record expression "
                                f"(index: '{display[:55]}…', record: '{canonical[:55]}…')"))
    if canonical.count("(") != canonical.count(")") or canonical.count("[") != canonical.count("]"):
        findings.append(Finding("ERROR", "expression-malformed", where,
                                "record expression has unbalanced brackets"))


def check_title(findings: list[Finding], where: str, index_title: str, record: dict) -> None:
    """The index title is a shortened display of the record title: its words must appear in
    order. A final word may be truncated mid-word ('Sales G' for 'Sales Growth'), because the
    display cut happens at a character budget, not at a word boundary."""
    haystack = re.findall(r"[A-Za-z0-9]+", (record["title"] or "").lower())
    if not haystack:
        return
    words = re.findall(r"[A-Za-z0-9]+", index_title.lower())
    position = 0
    for index, word in enumerate(words):
        last = index == len(words) - 1
        matched = False
        while position < len(haystack):
            candidate = haystack[position]
            position += 1
            if candidate == word \
                    or (len(word) >= 4 and (candidate.startswith(word) or word.startswith(candidate))) \
                    or (last and candidate.startswith(word)):
                matched = True
                break
        if not matched:
            findings.append(Finding("WARN", "title-drift", where,
                                    f"index title '{index_title}' does not track record title '{record['title']}'"))
            return


def check_experiments(records: dict, rows: list[dict], section: str,
                      seen: dict[str, str], findings: list[Finding]) -> None:
    for row in rows:
        rid, cells = row["id"], row["cells"]
        if rid in seen:
            findings.append(Finding("ERROR", "duplicate-id", rid,
                                    f"indexed twice: first under '{seen[rid]}', again under '{section}' (line {row['line']})"))
            continue
        seen[rid] = section

        record = records.get(rid)
        if record is None:
            findings.append(Finding("ERROR", "row-without-record", rid,
                                    f"no record file simulations/{rid}_*.md"))
            continue

        if record["status"] not in KNOWN_STATUSES:
            findings.append(Finding("ERROR", "invalid-status", rid,
                                    f"record Status='{record['status_raw']}' is not a known status"))
        elif record["status"] not in SECTION_STATUSES[section]:
            findings.append(Finding("ERROR", "status-section", rid,
                                    f"listed under '{section}' but record Status='{record['status']}'"))
        if record["mentions_pending"] and record["status"] in CLEARED_STATUSES:
            findings.append(Finding("ERROR", "pending-claimed-passed", rid,
                                    "record mentions PENDING blocks but is listed as cleared"))

        for field_name, column in METRIC_COLUMNS:
            check_metric(findings, rid, field_name, cells[column], record["fields"].get(field_name, ""))

        check_expression(findings, rid, cells[5], record)
        check_title(findings, rid, cells[1], record)


def stated_decay_sets(record_text: str) -> dict[str, set[int]]:
    """Dump label -> the decay values the record states for that dump.

    Handles both forms used in the sweep records: a single value ('d1 ... Decay 5') and an
    enumerated set ('d5 ... Decay varies per block: 0,3,4,5,6,7,8,10,12,16').
    """
    stated: dict[str, set[int]] = {}
    for line in record_text.splitlines():
        label = re.search(r"\b(d\d+)\b", line)
        if not label or not re.search(r"decay", line, re.I):
            continue
        after = line[label.end():]
        enumerated = re.search(r"decay[^:]*:\s*([0-9][0-9,\s]*)", after, re.I)
        if enumerated:
            stated[label.group(1)] = {int(n) for n in re.findall(r"\d+", enumerated.group(1))}
            continue
        single = re.search(r"decay\s*[:=]?\s*(\d+)\b", after, re.I)
        if single:
            stated[label.group(1)] = {int(single.group(1))}
    return stated


def check_sweeps(root: str, records: dict, rows: list[dict], seen: dict[str, str],
                 findings: list[Finding], stats: dict) -> None:
    for row in rows:
        rid, cells = row["id"], row["cells"]
        if rid in seen:
            findings.append(Finding("ERROR", "duplicate-id", rid, f"indexed twice (first under '{seen[rid]}')"))
            continue
        seen[rid] = SWEEP_SECTION

        record = records.get(rid)
        if record is None:
            findings.append(Finding("ERROR", "row-without-record", rid,
                                    f"no sweep record simulations/{rid}_*.md"))
            continue

        blocks_cell, region_cell, best_cell = cells[2], cells[3], cells[4]

        paths = sweep_csv_paths(record, root)
        if not paths:
            findings.append(Finding("ERROR", "sweep-source-missing", rid,
                                    "record names no simulations/sweeps/*.csv file"))
            continue
        missing = [p for p in paths if not os.path.exists(os.path.join(root, p))]
        if missing:
            findings.append(Finding("ERROR", "sweep-source-missing", rid,
                                    f"referenced CSV not on disk: {', '.join(missing)}"))
            continue

        tables = {path: read_csv(root, path) for path in paths}
        combined = [p for p in paths if p.endswith("all_results.csv")]
        per_dump = [p for p in paths if p not in combined]

        dump_rows = sum(len(tables[p]) for p in per_dump)
        total_rows = len(tables[combined[0]]) if combined else dump_rows
        # Per-dump files and the combined file hold the same blocks, so every tally below is
        # taken from one of them, never from both.
        primary = combined if combined else per_dump
        all_rows = [r for path in primary for r in tables[path]]

        # --- block counts --------------------------------------------------------
        numbers = [int(n) for n in numbers_in(blocks_cell)]
        expected_total = total_rows if combined else dump_rows
        if not numbers:
            findings.append(Finding("ERROR", "sweep-blocks", rid, f"no block count in '{blocks_cell}'"))
        else:
            if numbers[0] != expected_total:
                findings.append(Finding("ERROR", "sweep-blocks", rid,
                                        f"index says {numbers[0]} blocks, canonical CSVs hold {expected_total}"))
            if combined and per_dump and dump_rows != total_rows:
                findings.append(Finding("ERROR", "sweep-blocks", rid,
                                        f"per-dump CSVs total {dump_rows} but "
                                        f"{os.path.basename(combined[0])} holds {total_rows}"))
            page_claim = re.search(r"(\d+)\s*pages?", blocks_cell, re.I)
            if page_claim and int(page_claim.group(1)) != len(per_dump):
                findings.append(Finding("ERROR", "sweep-blocks", rid,
                                        f"index claims {page_claim.group(1)} pages, "
                                        f"found {len(per_dump)} per-dump CSV file(s)"))

        # --- regions and universes ----------------------------------------------
        # The index's Region(s) cell must be supported by the record's own settings lines,
        # by the CSV universe column, or by the per-dump file names.
        universes = {(r.get("universe") or "").strip().lower() for r in all_rows}
        dump_names = " ".join(os.path.basename(p).lower() for p in per_dump)
        setting_lines = " ".join(
            line.lower() for line in record["text"].splitlines()
            if re.search(r"\b(region|universe|neutralization)\b", line, re.I)
        )
        for token in re.findall(r"[A-Za-z0-9]+", region_cell):
            upper = token.upper()
            if upper in REGION_TOKENS:
                evidence = (upper.lower() in dump_names
                            or any(upper.lower() in u for u in universes)
                            or re.search(rf"\b{re.escape(upper.lower())}\b", setting_lines))
                if not evidence:
                    findings.append(Finding("ERROR", "sweep-region", rid,
                                            f"region '{token}' is not supported by the record settings, "
                                            f"CSV universe column, or dump file names"))
            elif UNIVERSE_RE.match(upper) and upper.lower() not in dump_names \
                    and not any(upper.lower() == u for u in universes) \
                    and not re.search(rf"\b{re.escape(upper.lower())}\b", setting_lines):
                findings.append(Finding("ERROR", "sweep-region", rid,
                                        f"universe '{token}' absent from the record settings and the CSV universe column"))

        # --- settings: per-block decay, where the CSVs and the record both carry it ---
        stated = stated_decay_sets(record["text"])
        for path in per_dump:
            table = tables[path]
            if not table or "decay" not in table[0]:
                continue
            values = {int(r["decay"]) for r in table if (r.get("decay") or "").strip()}
            if not values:
                continue
            label = re.search(r"_(d\d+)_", os.path.basename(path))
            expected = stated.get(label.group(1)) if label else None
            if expected is None:
                findings.append(Finding("WARN", "sweep-settings-unchecked", rid,
                                        f"{os.path.basename(path)} carries per-block decay but the record "
                                        f"states no decay for that dump"))
                continue
            stats["decay_dumps_compared"] = stats.get("decay_dumps_compared", 0) + 1
            if values != expected:
                findings.append(Finding("ERROR", "sweep-decay", rid,
                                        f"{os.path.basename(path)} carries decay {sorted(values)}, "
                                        f"the record states {sorted(expected)}"))

        # --- PASS / PENDING tallies ---------------------------------------------
        statuses = [(r.get("status") or "").strip().upper() for r in all_rows]
        passes = sum(1 for s in statuses if s == "PASS")
        pendings = sum(1 for s in statuses if s == "PENDING")

        claimed = re.search(r"(\d+)\s*(?:PASS\b|pass(?:ed|es)?\b)", best_cell)
        if claimed and int(claimed.group(1)) != passes:
            findings.append(Finding("ERROR", "sweep-passes", rid,
                                    f"index claims {claimed.group(1)} passing block(s), CSVs record {passes}"))
        claimed = re.search(r"(\d+)\s*PENDING", best_cell)
        if claimed and int(claimed.group(1)) != pendings:
            findings.append(Finding("ERROR", "sweep-pending", rid,
                                    f"index claims {claimed.group(1)} PENDING block(s), CSVs record {pendings}"))
        if pendings and re.search(r"\bPASS\b", best_cell):
            findings.append(Finding("ERROR", "pending-claimed-passed", rid,
                                    f"row reports a PASS while {pendings} block(s) are still unevaluated"))

        # --- quoted Sharpe / Fitness must be supported by the data ----------------
        pools = {
            "Sharpe": [r.get("sharpe", "") for r in all_rows],
            "Fitness": [r.get("fitness", "") for r in all_rows],
        }
        # A "N block(s) cleared <Metric> <X>" phrase quotes a *threshold*, and is verified by
        # counting the blocks that meet it, not by looking for the value in the data.
        cell = best_cell
        for count, metric, threshold in re.findall(
                r"(\d+)\s*blocks?\s+(?:cleared|above|at or above)\s+(Sharpe|Fitness)\s+(-?\d+(?:\.\d+)?)",
                cell, re.I):
            metric = metric.capitalize()
            actual = sum(1 for value in pools[metric]
                         if value and float(value) >= float(threshold))
            if int(count) != actual:
                findings.append(Finding("ERROR", "sweep-threshold", rid,
                                        f"index claims {count} block(s) at or above {metric} {threshold}, "
                                        f"the CSVs hold {actual}"))
            cell = re.sub(rf"{count}\s*blocks?\s+(?:cleared|above|at or above)\s+{metric}\s+{re.escape(threshold)}",
                          "", cell, flags=re.I)

        for label, values in pools.items():
            pool = {round2(v) for v in values} - {""}
            for quoted in re.findall(rf"{label}\s*(-?\d+(?:\.\d+)?)", cell):
                if round2(quoted) not in pool:
                    findings.append(Finding("ERROR", "sweep-quote-unsupported", rid,
                                            f"{label} {quoted} quoted in the index does not occur in the sweep data"))


def check_totals(index_text: str, counts: dict, findings: list[Finding]) -> None:
    """Verify the '**Totals:**' summary line against the section counts."""
    match = re.search(r"\*\*Totals:\*\*\s*(.+)", index_text)
    if not match:
        findings.append(Finding("WARN", "totals-unchecked", "index", "no '**Totals:**' line found to verify"))
        return
    line = match.group(1)
    patterns = [
        (r"(\d+)\s*recorded experiments", "records", counts["records"]),
        (r"(\d+)\s*cleared checks", "cleared", counts["cleared"]),
        (r"(\d+)\s*failed on self-correlation", "self-correlation", counts["self_correlation"]),
        (r"(\d+)\s*raised errors", "errors", counts["error_section"]),
        (r"(\d+)\s*failed on performance", "failed", counts["failed_section"]),
        (r"(\d+)\s*bulk sweeps", "sweeps", counts["sweeps"]),
    ]
    for pattern, label, actual in patterns:
        found = re.search(pattern, line)
        if not found:
            findings.append(Finding("WARN", "totals-unchecked", "index",
                                    f"totals line has no '{label}' figure; it was not verified"))
        elif int(found.group(1)) != actual:
            findings.append(Finding("ERROR", "totals", "index",
                                    f"totals line says {found.group(1)} {label}, sections hold {actual}"))


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def verify(root: str) -> tuple[list[Finding], dict]:
    index_path = os.path.join(root, INDEX_REL)
    if not os.path.isfile(index_path):
        raise FileNotFoundError(INDEX_REL)
    with open(index_path, encoding="utf-8") as handle:
        index_text = handle.read()

    records = load_records(root)
    rows, findings = parse_index(index_text)
    seen: dict[str, str] = {}

    settings_stats: dict = {}
    for section in EXPERIMENT_SECTIONS:
        check_experiments(records, rows[section], section, seen, findings)
    check_sweeps(root, records, rows[SWEEP_SECTION], seen, findings, settings_stats)

    for rid in sorted(set(records) - set(seen)):
        findings.append(Finding("ERROR", "record-not-indexed", rid,
                                f"{records[rid]['path']} exists but has no index row"))

    counts = {
        "records": len(records),
        "indexed": len(seen),
        "cleared": len(rows[EXPERIMENT_SECTIONS[0]]),
        "self_correlation": len(rows[EXPERIMENT_SECTIONS[1]]),
        "error_section": len(rows[EXPERIMENT_SECTIONS[2]]),
        "failed_section": len(rows[EXPERIMENT_SECTIONS[3]]),
        "sweeps": len(rows[SWEEP_SECTION]),
    }
    counts["experiment_rows"] = sum(counts[k] for k in ("cleared", "self_correlation", "error_section", "failed_section"))
    check_totals(index_text, counts, findings)

    stats = dict(counts)
    stats.update(settings_stats)
    stats["errors"] = sum(1 for f in findings if f.level == "ERROR")
    stats["warnings"] = sum(1 for f in findings if f.level == "WARN")
    return findings, stats


def report(findings: list[Finding], stats: dict, quiet: bool) -> int:
    for finding in sorted(findings, key=lambda f: (f.where, f.code, f.message)):
        if quiet and finding.level == "WARN":
            continue
        print(str(finding))
    summary = ("records={records} indexed={indexed} experiment-rows={experiment_rows} "
               "sweep-rows={sweeps} decay-dumps-compared={decay_dumps_compared} "
               "errors={errors} warnings={warnings}")
    stats.setdefault("decay_dumps_compared", 0)
    print(summary.format(**stats))
    if stats["errors"]:
        print("RESULT: INCONSISTENT")
        return 1
    print("RESULT: CONSISTENT")
    return 0


# --------------------------------------------------------------------------------------
# Self-test fixtures
# --------------------------------------------------------------------------------------

RECORD_ALPHA = """# Simulation 001 - Alpha One

Status: FAILED

Expression:

```text
rank(close / vwap)
```

Metrics:

```text
Sharpe: 0.50
Fitness: 0.40
Turnover: 3.04%
```
"""

RECORD_BETA = """# Simulation 002 - Beta Two

Status: PASSED_SUBMITTED

Expression:

```text
rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.61
Fitness: 1.02
Turnover: 25.25%
```
"""

RECORD_SWEEP = """# Simulation 067 - Sweep

Status: FAILED

Region: EUR   Universe: TOP2500

Machine-readable data: `Analysis and Simulation Reports/sweeps-and-experiments/s1_d1_eur_top2500.csv` (per dump),
`Analysis and Simulation Reports/sweeps-and-experiments/s1_all_results.csv` (combined).

Settings per dump:

```text
d1  Region EUR   Universe TOP2500   Decay 5
```

```text
Blocks: 3
```
"""

SWEEP_CSV = (
    "dump,result_no,universe,sharpe,fitness,turnover,status\n"
    "s1_d1_eur_top2500,1,TOP2500,1.97,1.58,0.0578,FAIL\n"
    "s1_d1_eur_top2500,2,TOP2500,1.37,1.02,0.1270,FAIL\n"
    "s1_d1_eur_top2500,3,TOP2500,0.42,0.16,0.7439,PENDING\n"
)

SWEEP_CSV_PER_DUMP = (
    "result_no,universe,decay,sharpe,fitness,turnover,status\n"
    "1,TOP2500,5,1.97,1.58,0.0578,FAIL\n"
    "2,TOP2500,5,1.37,1.02,0.1270,FAIL\n"
    "3,TOP2500,5,0.42,0.16,0.7439,PENDING\n"
)


def fixture_index(alpha_sharpe: str = "0.50", blocks: str = "3", passes: str = "0",
                  pending: str = "1", region: str = "EUR TOP2500",
                  expression: str = "`rank(close / vwap)`", duplicate: bool = False,
                  totals: str = "3 recorded experiments — 1 cleared checks, 0 failed on "
                                 "self-correlation, 0 raised errors, 1 failed on performance or "
                                 "robustness, 1 bulk sweeps",
                  threshold: str = "") -> str:
    header = "| ID | Experiment | Sharpe | Fitness | Turnover | Expression | Lesson |\n|---:|---|---:|---:|---:|---|---|\n"
    second = "| 002 | Beta Two | 1.61 | 1.02 | 25.25% | `rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))` | submitted |\n"
    first = (f"| 001 | Alpha One | {alpha_sharpe} | 0.40 | 3.04% | {expression} | weak |\n"
             if not duplicate else f"| 001 | Alpha One | {alpha_sharpe} | 0.40 | 3.04% | {expression} | weak |\n")
    if duplicate:
        second = second.replace("| 002 | Beta Two |", "| 001 | Beta Two |")
    return (
        "# Experiment Index\n\n"
        f"**Totals:** {totals}.\n\n"
        "## Experiments that cleared the checks\n\n" + header + second + "\n"
        "## Failed on self-correlation (metrics were acceptable)\n\n" + header + "\n"
        "## Errors (expression did not validate)\n\n" + header + "\n"
        "## Failed experiments (chronological)\n\n" + header + first + "\n"
        "## Bulk sweeps\n\n"
        "| ID | Sweep | Blocks | Region(s) | Best recorded result |\n|---:|---|---:|---|---|\n"
        f"| 067 | EUR sweep | {blocks} | {region} | `anl69` Sharpe 1.97 / Fitness 1.58; "
        f"{passes} passed; {pending} PENDING{'; ' + threshold if threshold else ''} |\n"
    )


def selftest() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, RECORD_DIR), exist_ok=True)
        os.makedirs(os.path.join(tmp, SWEEP_DIR), exist_ok=True)
        os.makedirs(os.path.join(tmp, os.path.dirname(INDEX_REL)), exist_ok=True)

        def write(rel: str, text: str) -> None:
            with open(os.path.join(tmp, rel), "w", encoding="utf-8") as handle:
                handle.write(text)

        write(os.path.join(RECORD_DIR, "001_alpha_one.md"), RECORD_ALPHA)
        write(os.path.join(RECORD_DIR, "002_beta_two.md"), RECORD_BETA)
        write(os.path.join(RECORD_DIR, "067_sweep.md"), RECORD_SWEEP)
        write(os.path.join(SWEEP_DIR, "s1_all_results.csv"), SWEEP_CSV)
        write(os.path.join(SWEEP_DIR, "s1_d1_eur_top2500.csv"), SWEEP_CSV_PER_DUMP)

        cases = [
            ("consistent fixture", {}, []),
            ("metric mismatch", {"alpha_sharpe": "0.51"}, ["metric-value"]),
            ("expression not a prefix", {"expression": "`rank(vwap / close)`"}, ["expression-prefix"]),
            ("sweep block count", {"blocks": "99"}, ["sweep-blocks"]),
            ("sweep pass claim", {"passes": "2"}, ["sweep-passes"]),
            ("sweep pending claim", {"pending": "0"}, ["sweep-pending"]),
            ("sweep region", {"region": "JPN TOP2500"}, ["sweep-region"]),
            ("duplicate id", {"duplicate": True}, ["duplicate-id"]),
            ("totals line", {"totals": "9 recorded experiments — 1 cleared checks, 0 failed on "
                                        "self-correlation, 0 raised errors, 1 failed on performance or "
                                        "robustness, 1 bulk sweeps"}, ["totals"]),
            ("threshold claim supported", {"threshold": "1 block cleared Fitness 1.58"}, []),
            ("threshold claim wrong", {"threshold": "2 blocks cleared Fitness 1.58"}, ["sweep-threshold"]),
        ]
        for label, kwargs, expected in cases:
            write(INDEX_REL, fixture_index(**kwargs))
            findings, _ = verify(tmp)
            codes = {f.code for f in findings if f.level == "ERROR"}
            if not expected:
                if findings:
                    failures.append(f"{label}: expected a clean run, got {[str(f) for f in findings]}")
            else:
                for code in expected:
                    if code not in codes:
                        failures.append(f"{label}: expected {code}, got {sorted(codes)}")

        # A record with no index row, and an index row with no record.
        write(INDEX_REL,
              fixture_index().replace("| 001 | Alpha One |", "| 003 | Ghost |"))
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        for code in ("row-without-record", "record-not-indexed"):
            if code not in codes:
                failures.append(f"missing/unindexed record: expected {code}, got {sorted(codes)}")

        # Invalid status, then a passed-status record parked in the failed section.
        write(os.path.join(RECORD_DIR, "003_gamma.md"),
              RECORD_ALPHA.replace("Simulation 001 - Alpha One", "Simulation 003 - Gamma")
              .replace("Status: FAILED", "Status: BANANA"))
        write(INDEX_REL,
              fixture_index().replace(
                  "| 001 | Alpha One | 0.50 |",
                  "| 003 | Gamma | 0.50 |").replace(
                  "| 003 | Gamma | 0.50 |", "| 001 | Alpha One | 0.50 |\n| 003 | Gamma | 0.50 |"))
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        if "invalid-status" not in codes:
            failures.append(f"invalid status: expected invalid-status, got {sorted(codes)}")

        # Malformed record expression (unbalanced brackets).
        write(os.path.join(RECORD_DIR, "003_gamma.md"),
              RECORD_ALPHA.replace("Simulation 001 - Alpha One", "Simulation 003 - Gamma")
              .replace("rank(close / vwap)", "rank(close / vwap"))
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        if "expression-malformed" not in codes:
            failures.append(f"malformed expression: expected expression-malformed, got {sorted(codes)}")
        os.remove(os.path.join(tmp, RECORD_DIR, "003_gamma.md"))

        # Annotated display values: supported annotation passes, unsupported fails.
        write(os.path.join(RECORD_DIR, "001_alpha_one.md"),
              RECORD_ALPHA.replace("Sharpe: 0.50", "Sharpe: 0.73 in IS summary"))
        write(INDEX_REL,
              fixture_index(alpha_sharpe="0.73 in IS summary"))
        findings, _ = verify(tmp)
        if [f for f in findings if f.level == "ERROR"]:
            failures.append(f"supported annotation should pass, got {[str(f) for f in findings]}")
        write(INDEX_REL,
              fixture_index(alpha_sharpe="0.99 in IS summary"))
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        if "metric-value" not in codes:
            failures.append(f"unsupported annotation: expected metric-value, got {sorted(codes)}")

        # Per-block decay in the CSV must agree with the decay the record states.
        write(os.path.join(RECORD_DIR, "067_sweep.md"), RECORD_SWEEP.replace("Decay 5", "Decay 7"))
        write(INDEX_REL, fixture_index())
        findings, stats = verify(tmp)
        codes = {f.code for f in findings if f.level == "ERROR"}
        if "sweep-decay" not in codes:
            failures.append(f"decay mismatch: expected sweep-decay, got {sorted(codes)}")
        if stats.get("decay_dumps_compared") != 1:
            failures.append(f"decay comparison should have run once, ran {stats.get('decay_dumps_compared')}")
        write(os.path.join(RECORD_DIR, "067_sweep.md"), RECORD_SWEEP)

        # A record that mentions unevaluated blocks must not be filed as cleared.
        write(os.path.join(RECORD_DIR, "002_beta_two.md"),
              RECORD_BETA.replace("Status: PASSED_SUBMITTED",
                                  "Status: PASSED_SUBMITTED\n\n42 blocks are still PENDING."))
        write(INDEX_REL, fixture_index())
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        if "pending-claimed-passed" not in codes:
            failures.append(f"pending record filed as cleared: expected pending-claimed-passed, got {sorted(codes)}")

        # A sweep row that reports a PASS while blocks are still unevaluated.
        write(os.path.join(RECORD_DIR, "002_beta_two.md"), RECORD_BETA)
        write(INDEX_REL,
              fixture_index().replace("1 PENDING |", "1 PENDING; 0 PASS |"))
        codes = {f.code for f in verify(tmp)[0] if f.level == "ERROR"}
        if "pending-claimed-passed" not in codes:
            failures.append(f"PASS beside PENDING: expected pending-claimed-passed, got {sorted(codes)}")

        # An em dash over a value the record does hold is a warning, not an error.
        write(os.path.join(RECORD_DIR, "001_alpha_one.md"), RECORD_ALPHA)
        write(INDEX_REL, fixture_index(alpha_sharpe="—"))
        findings, _ = verify(tmp)
        if [f for f in findings if f.level == "ERROR"]:
            failures.append(f"em dash should not be an error, got {[str(f) for f in findings]}")
        if not [f for f in findings if f.code == "metric-omitted"]:
            failures.append("em dash over a recorded value should warn (metric-omitted)")

    if failures:
        print("SELFTEST FAILED")
        for failure in failures:
            print("  -", failure)
        return 1
    print("SELFTEST PASSED (11 table fixtures: 2 clean, 9 expected failures; plus missing record, "
          "unindexed record, invalid status, malformed expression, decay mismatch, "
          "pending-claimed-passed and annotation cases)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reconcile the experiment index with its records.")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        help="repository root (default: this script's parent directory)")
    parser.add_argument("--selftest", action="store_true", help="run built-in fixtures and exit")
    parser.add_argument("--quiet", action="store_true", help="suppress warnings")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    try:
        findings, stats = verify(os.path.abspath(args.root))
    except FileNotFoundError as exc:
        print(f"error: cannot read {exc}", file=sys.stderr)
        return 2
    return report(findings, stats, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
