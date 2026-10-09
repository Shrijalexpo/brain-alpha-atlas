#!/usr/bin/env python3
"""Wiki hygiene checker for the public documentation layer.

Checks every Markdown file it is given for the defects that are cheap to introduce and
expensive to notice in a knowledge base:

  link         relative Markdown links that do not resolve on disk
  table        table rows whose cell count differs from the header row
  backtick     a line with an odd number of inline-code backticks
  fence        an unterminated or unopened ``` code fence
  private-ref  a link or path pointing at material excluded from public release
  home-path    an absolute machine path (``/Users/<name>/``, ``C:\\Users\\<name>\\``)
  secret       an obvious credential shape (long hex token, bearer/API-key assignment)

``--text-scan`` applies only the content rules (private-ref, home-path, secret) to every file
under a directory, whatever its extension. That is how the *built* MkDocs site is checked
before it is published: rendered HTML is not Markdown, but the same leaks matter. A long hex
string in a bundled theme asset is common and harmless, so it is reported as a warning there
and does not fail the run; the other content rules remain fatal.

It is meant for build output (``site/``), not for scanning this repository wholesale: the
self-test fixtures below deliberately contain the very patterns the tool looks for, so
`--text-scan Tools` reports them by design.

Dependency-free, no network access. Run ``--selftest`` after any edit.

Usage:
    python3 Tools/check_docs.py --selftest
    python3 Tools/check_docs.py                       # docs/ and README.md
    python3 Tools/check_docs.py docs README.md mkdocs.yml
    python3 Tools/check_docs.py --text-scan site      # built site, any file type
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

# --------------------------------------------------------------------------------------
# Patterns
# --------------------------------------------------------------------------------------

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Material kept out of the public build. A reference to it would be a broken promise at best
# and a leak at worst, so documented paths must not mention it.
PRIVATE_REFS = [
    "tutorials/consultant_information",
    "tutorials/worldquant_brain_documentation_raw",
    "Operators/worldquant_brain_operators_raw_capture.txt",
    "competition_contract.txt",
    "Consulting Agreement",
    "ACE_API__Gold_",
    "formula_collections",
]

SECRET_RES = [
    (re.compile(r"\b(?:api[_-]?key|apikey|access[_-]?token|auth[_-]?token|session[_-]?token|token|password|passwd|secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"), "credential assignment"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9_\-\.]{20,}"), "bearer token"),
    (re.compile(r"\b[0-9a-fA-F]{40,}\b"), "long hex token"),
]

# The relative example in the contributing guide is written ``/Users/...`` on purpose:
# that is the pattern contributors are told to look for, not a machine path.
HOME_PATH_RE = re.compile(
    r"(?:/Users/|/home/|[A-Za-z]:\\\\?Users\\\\?)"
    r"(?![.]{2,})([A-Za-z0-9._-]{2,})"
)

FENCE_RE = re.compile(r"^\s*(```+|~~~+)")

BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svgz", ".ico", ".woff", ".woff2",
                   ".ttf", ".otf", ".eot", ".zip", ".gz", ".pdf", ".mp4", ".webm", ".map"}


def split_row(line: str) -> list[str]:
    """Split a Markdown table row into trimmed cells, ignoring pipes inside code spans.

    Shared with ``Tools/verify_index.py`` so both tools read a table row the same way.
    """
    out, in_code = [], False
    for ch in line:
        if ch == "`":
            in_code = not in_code
            out.append(ch)
            continue
        out.append("\x00" if (ch == "|" and not in_code) else ch)
    parts = "".join(out).split("\x00")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [cell.strip() for cell in parts]


def table_cells(line: str) -> int:
    """Number of cells in a Markdown table row."""
    return len(split_row(line))


# A long hex string is a real signal in prose and background noise in a bundled asset, so it
# carries a different severity in the two modes.
WARN_ONLY_RULE = "long hex token"


def content_findings(text: str, rel_path: str) -> list[tuple[str, str]]:
    """Apply the content rules that hold for any file type. Returns (level, message) pairs."""
    out: list[tuple[str, str]] = []
    for i, line in enumerate(text.splitlines(), 1):
        for needle in PRIVATE_REFS:
            if needle in line:
                out.append(("ERROR", f"{rel_path}:{i}: references excluded material -> {needle}"))
        for match in HOME_PATH_RE.finditer(line):
            out.append(("ERROR", f"{rel_path}:{i}: absolute machine path -> ...{match.group(1)}"))
        for pattern, label in SECRET_RES:
            if pattern.search(line):
                level = "WARN" if label == WARN_ONLY_RULE else "ERROR"
                out.append((level, f"{rel_path}:{i}: possible {label}"))
    return out


def check_text(text: str, rel_path: str, root: str) -> list[str]:
    """Return findings as ``rel_path:line: RULE message`` strings."""
    findings: list[str] = []
    lines = text.splitlines()
    in_fence = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        fence = FENCE_RE.match(line)
        if fence:
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # --- links -----------------------------------------------------------------
        for target in LINK_RE.findall(line):
            if re.match(r"^(?:https?://|mailto:|#)", target):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(rel_path), clean))
            if not os.path.exists(os.path.join(root, resolved)):
                findings.append(f"{rel_path}:{i}: link does not resolve -> {target}")

        if stripped.startswith("|"):
            width = table_cells(line)
            if not hasattr(check_text, "_tbl"):
                check_text._tbl = {}
            # (file, column index) -> expected width is tracked by the table's first row
            key = rel_path
            prev = check_text._tbl.get(key)
            if prev is None:
                check_text._tbl[key] = width
            elif width != prev:
                findings.append(
                    f"{rel_path}:{i}: table row has {width} cells, header has {prev}"
                )
        else:
            if hasattr(check_text, "_tbl"):
                check_text._tbl.pop(rel_path, None)

        # --- inline code balance ---------------------------------------------------
        if line.count("`") % 2:
            findings.append(f"{rel_path}:{i}: odd number of backticks on this line")

    for _level, message in content_findings(text, rel_path):
        findings.append(message)

    if in_fence:
        findings.append(f"{rel_path}: unclosed code fence at end of file")
    if hasattr(check_text, "_tbl"):
        check_text._tbl.pop(rel_path, None)
    return findings


def text_scan(targets: list[str], root: str) -> int:
    """Content rules over every file in the given directories, whatever the file type."""
    files: list[str] = []
    for target in targets:
        if os.path.isdir(target):
            for base, _dirs, names in os.walk(target):
                for name in names:
                    files.append(os.path.join(base, name))
        elif os.path.isfile(target):
            files.append(target)
        else:
            print(f"skip (not found): {target}", file=sys.stderr)

    errors = warnings = 0
    for path in sorted(files):
        if os.path.splitext(path)[1].lower() in BINARY_SUFFIXES:
            continue
        try:
            if os.path.getsize(path) > 8 * 1024 * 1024:
                continue
            with open(path, encoding="utf-8", errors="ignore") as handle:
                text = handle.read()
        except OSError as exc:
            print(f"skip (unreadable): {path}: {exc}", file=sys.stderr)
            continue
        for level, message in content_findings(text, os.path.relpath(path, root)):
            if level == "WARN":
                warnings += 1
                print(f"WARN  {message}")
            else:
                errors += 1
                print(f"ERROR {message}")
    print(f"scanned {len(files)} file(s): {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def collect_targets(targets: list[str]) -> list[str]:
    files: list[str] = []
    for target in targets:
        if os.path.isdir(target):
            for base, _dirs, names in os.walk(target):
                for name in names:
                    if name.endswith(".md"):
                        files.append(os.path.join(base, name))
        elif os.path.isfile(target):
            files.append(target)
        else:
            print(f"skip (not found): {target}", file=sys.stderr)
    return sorted(files)


def run(targets: list[str], root: str) -> int:
    files = collect_targets([os.path.join(root, t) if not os.path.isabs(t) else t for t in targets])
    findings: list[str] = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        rel = os.path.relpath(path, root)
        findings.extend(check_text(text, rel, root))
    for item in findings:
        print(item)
    print(f"checked {len(files)} file(s): {len(findings)} finding(s)")
    return 1 if findings else 0


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

GOOD = """# Title

Link to [a sibling](other.md) and [the web](https://example.com/x).

| A | B |
|---|---|
| `x | y` | 2 |
| plain | 3 |

Keep paths machine-relative: `~/Downloads/page.txt`.
"""

BAD = """# Title

[broken link](missing.md)

| A | B |
|---|---|
| one | 2 | 3 |

A stray `backtick here.

See tutorials/consultant_information/README.md for more.

Saved at /Users/somebody/Documents/file.md yesterday.

token = "abcdefghijklmnopqrstuvwx"

```text
unclosed
"""


def selftest() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        other = os.path.join(tmp, "other.md")
        with open(other, "w", encoding="utf-8") as fh:
            fh.write("# sibling\n")

        good = check_text(GOOD, "good.md", tmp)
        if good:
            failures.append(f"clean fixture produced findings: {good}")

        bad = check_text(BAD, "bad.md", tmp)
        rules = "\n".join(bad)
        for expected in [
            "link does not resolve",
            "table row has 3 cells, header has 2",
            "odd number of backticks",
            "references excluded material",
            "absolute machine path",
            "possible credential assignment",
            "unclosed code fence",
        ]:
            if expected not in rules:
                failures.append(f"missing expected finding: {expected}")

        # Built-site text scan: any file type, content rules only, hex tokens are warnings.
        def quiet_scan(directory: str) -> int:
            with contextlib.redirect_stdout(io.StringIO()):
                return text_scan([directory], tmp)

        good_site = os.path.join(tmp, "site_good")
        os.makedirs(good_site)
        with open(os.path.join(good_site, "index.html"), "w", encoding="utf-8") as fh:
            fh.write("<html><body><a href='https://example.com'>ok</a></body></html>\n")
        if quiet_scan(good_site) != 0:
            failures.append("clean built-site fixture should scan clean")

        bad_site = os.path.join(tmp, "site_bad")
        os.makedirs(bad_site)
        with open(os.path.join(bad_site, "index.html"), "w", encoding="utf-8") as fh:
            fh.write("<p>from /Users/somebody/Quant DB</p>\n<p>see tutorials/consultant_information/</p>\n")
        if quiet_scan(bad_site) != 1:
            failures.append("dirty built-site fixture should fail the scan")

        hex_only = os.path.join(tmp, "site_hex")
        os.makedirs(hex_only)
        with open(os.path.join(hex_only, "bundle.js"), "w", encoding="utf-8") as fh:
            fh.write("var h='deadbeefdeadbeefdeadbeefdeadbeefdeadbeef';\n")
        if quiet_scan(hex_only) != 0:
            failures.append("a hex string in a bundled asset should warn, not fail")

    if failures:
        print("SELFTEST FAILED")
        for item in failures:
            print("  -", item)
        return 1
    print("selftest passed: clean fixture is silent, every rule fires on the bad fixture, "
          "built-site scan separates errors from warnings")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Markdown hygiene checker for the wiki.")
    parser.add_argument("targets", nargs="*", default=["docs", "README.md"],
                        help="files or directories to check (default: docs README.md)")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        help="repository root used to resolve relative links")
    parser.add_argument("--text-scan", action="store_true",
                        help="apply only the content rules to every file under the targets (use on the built site)")
    parser.add_argument("--selftest", action="store_true", help="run built-in checks and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if args.text_scan:
        targets = [os.path.join(root, t) if not os.path.isabs(t) else t for t in args.targets]
        return text_scan(targets, root)
    return run(args.targets, root)


if __name__ == "__main__":
    raise SystemExit(main())
