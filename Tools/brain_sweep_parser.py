#!/usr/bin/env python3
"""Parse pasted WorldQuant BRAIN multi-simulation result dumps ("N Results" pages).

The BRAIN research UI lets you copy a whole page of simulation results. The
pasted text has this shape:

    N Results

    Simulation Settings
    Region: EUR
    Universe: TOP2500          (only in some dumps)
    Delay: 1
    Decay: 5
    Truncation: 0.08
    Pasteurization: ON
    NaN Handling: ON

    Failed Check Sets
    F1: LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE
    ...

    ## Universe: TOP2500        (only in multi-universe dumps)
    ### Neutralization: MARKET  (only in multi-universe dumps)

    #### Result 1
    - Expression: `ts_rank(ts_backfill(some_field, 21), 63)`
    - Train Sharpe: 2.43
    - Sharpe: 2.16
    - Turnover: 45.10%
    - Fitness: 0.96
    - Returns: 8.90%
    - Drawdown: 6.36%
    - Margin: 3.95 bps
    - Long Count: 1388
    - Short Count: 1431
    - Checks: FAIL F11

Critical caveat handled here: the `Fx` -> check-name legend is PER FILE. The
same F-number means different checks in different dumps, so the legend is
always re-read from the dump being parsed and F-codes are resolved immediately.

Supported dump shapes
---------------------
* One pasted page per file (the usual case) -> one set of outputs.
* Several pages concatenated into one file, each starting with its own
  `N Results` header. Every embedded page keeps its own `Simulation Settings`
  and its own `Fx` legend; outputs are written per page and the combined files
  cover all of them.
* Pages whose blocks are labelled `### Decay: <n> · Truncation: <x>` instead of
  `### Result <n>`. Those blocks carry no result number in the source, so a
  sequential `result_no` is synthesised (flagged `number_synthesised`), the
  per-block decay/truncation is kept in dedicated columns, and such pages report
  `Train Fitness` rather than `Train Sharpe`.

Usage
-----
    python3 Tools/brain_sweep_parser.py DUMP.txt [DUMP2.txt ...] --outdir simulations/sweeps

Writes, per embedded dump: `<slug>.csv`, `<slug>.json`, `<slug>.md`, and (when
more than one dump is given) `all_results.csv` plus `SUMMARY.md`. Pass
`--prefix NAME_` when a bundle is already stored in the same directory, so the
combined files do not overwrite it.

Run `python3 Tools/brain_sweep_parser.py --selftest` to check the parser.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Tuple

RESULT_RE = re.compile(r"^(#{2,4})\s+Result\s+(\d+)\s*$")
# Decay-style block header: `### Decay: 6 · Truncation: 0.08`. The separator
# between the two settings has varied, so match it loosely.
DECAY_HEADER_RE = re.compile(r"^#{2,4}\s+Decay:\s*(\d+)\b.*?Truncation:\s*([0-9.]+)\s*$")
# `N Results` header that opens each page of a possibly-concatenated paste.
DUMP_HEADER_RE = re.compile(r"^\s*([\d,]+)\s+Results?\s*$")
SETTING_RE = re.compile(r"^(Region|Universe|Delay|Decay|Truncation|Neutralization|"
                        r"Pasteurization|NaN Handling|Unit Handling|Language|"
                        r"Instrument Type|Test Period):\s*(.*)$")
LEGEND_RE = re.compile(r"^F(\d+):\s*(.+)$")
UNIVERSE_RE = re.compile(r"^#{2,4}\s+Universe:\s*(.*)$")
NEUT_RE = re.compile(r"^#{2,4}\s+Neutralization:\s*(.*)$")
FIELD_RE = re.compile(r"^-\s+([A-Za-z][A-Za-z0-9 ]*?):\s*(.*)$")
BACKFILL_RE = re.compile(r"ts_backfill\(\s*([A-Za-z0-9_]+)")
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# Operators/keywords that are never data fields (kept deliberately broad).
OPERATORS = {
    "ts_backfill", "ts_rank", "ts_zscore", "ts_scale", "ts_decay_linear", "ts_mean",
    "ts_sum", "ts_std_dev", "ts_delta", "ts_delay", "ts_av_diff", "ts_arg_max",
    "ts_arg_min", "ts_max_diff", "ts_min_diff", "ts_product", "ts_returns", "ts_ir",
    "ts_quantile", "ts_kurtosis", "ts_skewness", "ts_max", "ts_min", "ts_count_nans",
    "ts_regression", "ts_corr", "ts_covariance", "ts_median", "ts_step", "ts_weighted_delay",
    "ts_decay_exp_window", "ts_entropy", "ts_theilsen", "ts_triple_corr", "ts_min_max_cps",
    "ts_min_max_diff", "ts_rank_gmean_amean_diff", "ts_scaled_rank", "ts_moment",
    "rank", "zscore", "normalize", "scale", "winsorize", "quantile", "truncate",
    "group_rank", "group_zscore", "group_scale", "group_neutralize", "group_mean",
    "group_sum", "group_count", "group_std_dev", "group_max", "group_min", "group_median",
    "bucket", "vec_avg", "vec_sum", "vec_max", "vec_min", "vec_choose", "vec_ir",
    "vec_kurtosis", "vec_skewness", "vec_stddev", "vec_count", "vec_percentage",
    "vec_powersum", "vec_range", "vec_skew", "vec_norm", "vec_quantile", "vec_median",
    "vec_rank", "last_diff_value", "days_from_last_change", "hump", "kth_element",
    "trade_when", "if_else", "and", "or", "not", "log", "ln", "sqrt", "abs", "sign",
    "power", "exp", "sigmoid", "tanh", "arc_tan", "arc_sin", "arc_cos", "add", "subtract",
    "multiply", "divide", "densify", "pasteurize", "reverse", "signed_power",
    "one_side", "nan_out", "nan_mask", "to_nan", "clamp", "keep", "left_tail", "right_tail",
    "tail", "filter", "regression_neut", "scale_down", "vector_neut", "matrix",
    "industry", "subindustry", "sector", "market", "country", "exchange", "densities",
}

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def slugify(name: str) -> str:
    base = os.path.basename(name)
    base = re.sub(r"^Pasted text\((.*)\)\.txt$", r"\1", base)
    base = re.sub(r"\.[A-Za-z0-9]+$", "", base)
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")
    return base or "sweep"


def to_num(text: str) -> Optional[float]:
    if text is None:
        return None
    cleaned = text.strip().replace("%", "").replace(",", "")
    m = NUM_RE.search(cleaned)
    return float(m.group(0)) if m else None


def primary_field(expression: str) -> str:
    """Best-effort identification of the data field a formula is built on."""
    m = BACKFILL_RE.search(expression)
    if m:
        return m.group(1)
    for tok in TOKEN_RE.findall(expression):
        if tok.lower() not in OPERATORS and not tok.isdigit():
            return tok
    return ""


def family_of(field: str) -> str:
    if not field:
        return "unknown"
    if field.startswith("anl10_"):
        return "anl10 (analyst)"
    for pref, name in (
        ("anl69_", "anl69 (analyst)"), ("anl4_", "anl4 (analyst)"), ("anl9_", "anl9 (analyst)"),
        ("anl15_", "anl15 (analyst)"), ("anl39_", "anl39 (analyst)"), ("anl11_", "anl11 (ESG)"),
        ("pv37_", "pv37 (price/volume)"), ("pv20_", "pv20 (price/volume)"),
        ("pv87_", "pv87 (nlp/estimates)"), ("snt21", "snt21 (sentiment)"),
        ("fnd28_", "fnd28 (fundamental)"), ("fnd17_", "fnd17 (fundamental)"),
        ("fnd23_", "fnd23 (fundamental)"), ("fnd6", "fnd6 (fundamental)"),
        ("est_", "est_ (estimate)"), ("sector_", "sector_ (grouping)"),
        ("group_", "group_ (grouping)"), ("tbv_", "tbv_ (analyst)"), ("ebg_", "ebg_ (group)"),
        ("adv", "adv (liquidity)"), ("principal_component", "principal_component"),
    ):
        if field.startswith(pref):
            return name
    return "other"


def split_checks(raw: str, legend: Dict[str, List[str]]) -> Tuple[str, List[str], List[str]]:
    """Return (status, F-codes, resolved check names) for a `Checks:` line."""
    raw = (raw or "").strip()
    if raw.upper().startswith("PASS"):
        return "PASS", [], []
    codes = re.findall(r"F(\d+)", raw)
    codes = ["F" + c for c in codes]
    names: List[str] = []
    for code in codes:
        for name in legend.get(code, []):
            if name not in names:
                names.append(name)
    return ("FAIL" if codes else raw or "UNKNOWN"), codes, names


def segment_bounds(lines: List[str]) -> List[Tuple[int, int]]:
    """Line ranges of every `N Results` page in a possibly-concatenated paste."""
    starts = [i for i, l in enumerate(lines) if DUMP_HEADER_RE.match(l)]
    if not starts:
        return [(0, len(lines))]
    ends = starts[1:] + [len(lines)]
    return list(zip(starts, ends))


def parse_dumps(path: str) -> List[Dict[str, Any]]:
    """Parse every page embedded in a pasted dump file (one page per dump)."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    return [_parse_segment(lines[s:e], os.path.abspath(path), k + 1)
            for k, (s, e) in enumerate(segment_bounds(lines))]


def parse_dump(path: str) -> Dict[str, Any]:
    """Backwards-compatible single-page view: the first page in the file."""
    return parse_dumps(path)[0]


def _parse_segment(lines: List[str], source: str, dump_index: int) -> Dict[str, Any]:
    declared = None
    settings: Dict[str, str] = OrderedDict()
    legend: Dict[str, List[str]] = OrderedDict()
    results: List[Dict[str, Any]] = []
    cur: Optional[Dict[str, Any]] = None
    universe: Optional[str] = None
    neutralization: Optional[str] = None
    section_marks: List[Tuple[int, Optional[str], Optional[str]]] = []
    auto_no = 0

    def flush() -> None:
        nonlocal cur
        if cur is not None:
            # Single-universe dumps declare Universe/Neutralization under
            # "Simulation Settings" instead of section headers.
            cur["universe"] = cur.get("universe") or universe or settings.get("Universe")
            cur["neutralization"] = (cur.get("neutralization") or neutralization
                                     or settings.get("Neutralization"))
            results.append(cur)
            cur = None

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        if declared is None:
            m = DUMP_HEADER_RE.match(stripped)
            if m:
                declared = int(m.group(1).replace(",", ""))
                continue

        m = UNIVERSE_RE.match(stripped)
        if m:
            flush()
            universe = m.group(1).strip()
            neutralization = None
            section_marks.append((lineno, universe, neutralization))
            continue
        m = NEUT_RE.match(stripped)
        if m:
            flush()
            neutralization = m.group(1).strip()
            section_marks.append((lineno, universe, neutralization))
            continue

        m = RESULT_RE.match(stripped)
        if m:
            flush()
            auto_no = int(m.group(2))
            cur = {
                "result_no": auto_no,
                "line": lineno,
                "universe": universe,
                "neutralization": neutralization,
            }
            continue

        # Decay-style pages have no `Result N` header; the block header instead
        # records the settings that were varied for that run.
        m = DECAY_HEADER_RE.match(stripped)
        if m:
            flush()
            auto_no += 1
            cur = {
                "result_no": auto_no,
                "number_synthesised": True,
                "line": lineno,
                "universe": universe,
                "neutralization": neutralization,
                "decay": int(m.group(1)),
                "truncation": to_num(m.group(2)),
            }
            continue

        if cur is None:
            m = SETTING_RE.match(stripped)
            if m:
                settings.setdefault(m.group(1), m.group(2).strip())
                continue
            m = LEGEND_RE.match(stripped)
            if m:
                legend["F" + m.group(1)] = [c.strip() for c in m.group(2).split(",") if c.strip()]
                continue
            continue

        m = FIELD_RE.match(stripped)
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()

        if key == "Expression":
            expr = val.strip()
            if expr.startswith("`") and expr.endswith("`"):
                expr = expr[1:-1]
            cur["expression"] = expr
            cur["primary_field"] = primary_field(expr)
            cur["family"] = family_of(cur["primary_field"])
        elif key == "Checks":
            status, codes, names = split_checks(val, legend)
            cur["status"] = status
            cur["failed_check_codes"] = codes
            cur["failed_checks"] = names
        elif key.startswith("Train Sharpe"):
            cur["train_sharpe"] = to_num(val)
        elif key.startswith("Train Fitness"):
            cur["train_fitness"] = to_num(val)
        else:
            mapping = {
                "Sharpe": "sharpe", "Turnover": "turnover", "Fitness": "fitness",
                "Returns": "returns", "Drawdown": "drawdown", "Margin": "margin_bps",
                "Long Count": "long_count", "Short Count": "short_count",
            }
            if key in mapping:
                cur[mapping[key]] = to_num(val)
            cur.setdefault("extra", {})[key] = val

    flush()

    for r in results:
        r.setdefault("expression", "")
        r.setdefault("primary_field", "")
        r.setdefault("family", "unknown")
        r.setdefault("status", "UNKNOWN")
        r.setdefault("failed_checks", [])
        r.setdefault("failed_check_codes", [])

    return {
        "source": source,
        "dump_index": dump_index,
        "declared_count": declared,
        "settings": dict(settings),
        "legend": legend,
        "universe_labels": sorted({r["universe"] for r in results if r.get("universe")}),
        "neutralization_labels": sorted({r["neutralization"] for r in results
                                         if r.get("neutralization")}),
        "sections": [
            {"line": ln, "universe": u, "neutralization": n} for ln, u, n in section_marks
        ],
        "results": results,
    }


def dump_slug(dump: Dict[str, Any], multi: bool = False) -> str:
    """Filename stem for one parsed page.

    Single-page files keep the historical filename-derived slug. Pages inside a
    concatenated file are disambiguated by page number, region and universe.
    """
    base = slugify(dump["source"])
    if not multi:
        return base
    region = (dump["settings"].get("Region") or "unknown").lower()
    labels = [l.lower() for l in dump.get("universe_labels") or []]
    if len(labels) == 1:
        uni = labels[0]
    elif 1 < len(labels) <= 2:
        uni = "-".join(labels)
    elif labels:
        uni = "%duniverses" % len(labels)
    else:
        uni = (dump["settings"].get("Universe") or "nouniverse").lower()
    return slugify(f"{base}_d{dump.get('dump_index', 1)}_{region}_{uni}")


def write_outputs(dump: Dict[str, Any], outdir: str, multi: bool = False) -> str:
    slug = dump_slug(dump, multi)
    os.makedirs(outdir, exist_ok=True)

    cols = ["result_no", "universe", "neutralization", "decay", "truncation",
            "family", "primary_field",
            "sharpe", "train_sharpe", "train_fitness", "fitness", "turnover",
            "returns", "drawdown",
            "margin_bps", "long_count", "short_count", "status",
            "failed_check_codes", "failed_checks", "expression"]

    csv_path = os.path.join(outdir, slug + ".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in dump["results"]:
            row = []
            for c in cols:
                v = r.get(c, "")
                if isinstance(v, list):
                    v = ",".join(v)
                row.append("" if v is None else v)
            w.writerow(row)

    json_path = os.path.join(outdir, slug + ".json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(dump, fh, indent=1)

    md_path = os.path.join(outdir, slug + ".md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_report(dump, slug))

    return slug


def _fmt(v: Any, suffix: str = "") -> str:
    if v is None or v == "":
        return "—"
    return f"{v}{suffix}"


def fmt_expr(expr: str) -> str:
    return "`" + expr.replace("|", "\\|") + "`"


def render_report(dump: Dict[str, Any], slug: str) -> str:
    rs = dump["results"]
    s = dump["settings"]
    legend = dump["legend"]

    out: List[str] = []
    out.append(f"# Parsed BRAIN sweep: `{slug}`\n")
    out.append(f"- Source: `{dump['source']}`")
    out.append(f"- Declared results in header: {dump['declared_count']}")
    out.append(f"- Result blocks parsed: {len(rs)}")
    if dump["declared_count"] != len(rs):
        out.append(f"- **Mismatch:** header declared {dump['declared_count']}, "
                   f"parsed {len(rs)}. Investigate before relying on this file.")
    if dump.get("dump_index"):
        out.append(f"- Page {dump['dump_index']} of a concatenated dump file")
    if any(r.get("number_synthesised") for r in rs):
        out.append("- **No `Result N` headers in the source:** `result_no` is synthesised "
                   "from block order, not read from the dump.")
    if any(r.get("decay") is not None for r in rs):
        out.append("- This page varies `Decay`/`Truncation` per block and reports "
                   "`Train Fitness` in place of `Train Sharpe`; both are kept per row.")
    out.append("")
    out.append("## Settings\n")
    out.append("| Key | Value |")
    out.append("|---|---|")
    for k, v in s.items():
        out.append(f"| {k} | {v} |")
    if dump["sections"]:
        out.append("")
        out.append("## Sections\n")
        out.append("| Line | Universe | Neutralization |")
        out.append("|---:|---|---|")
        for sec in dump["sections"]:
            out.append(f"| {sec['line']} | {sec['universe'] or '—'} | {sec['neutralization'] or '—'} |")

    out.append("")
    out.append("## Failed-check legend (this file only)\n")
    out.append("The `Fx` codes are file-specific; never carry them between dumps.\n")
    out.append("| Code | Checks |")
    out.append("|---|---|")
    for code, names in legend.items():
        out.append(f"| {code} | {', '.join(names)} |")

    passed = [r for r in rs if r["status"] == "PASS"]
    sharpe_fit = [r for r in rs
                  if (r.get("sharpe") or -9) >= 1.25 and (r.get("fitness") or -9) >= 1.0]
    out.append("")
    out.append("## Headline counts\n")
    out.append("| Bucket | Count |")
    out.append("|---|---:|")
    out.append(f"| Result blocks | {len(rs)} |")
    out.append(f"| Checks PASS | {len(passed)} |")
    out.append(f"| Sharpe ≥ 1.25 | {sum(1 for r in rs if (r.get('sharpe') or -9) >= 1.25)} |")
    out.append(f"| Fitness ≥ 1.0 | {sum(1 for r in rs if (r.get('fitness') or -9) >= 1.0)} |")
    out.append(f"| Sharpe ≥ 1.25 and Fitness ≥ 1.0 | {len(sharpe_fit)} |")
    out.append(f"| Sharpe ≥ 2.0 | {sum(1 for r in rs if (r.get('sharpe') or -9) >= 2.0)} |")
    out.append(f"| Turnover > 70% | {sum(1 for r in rs if (r.get('turnover') or -9) > 70)} |")
    out.append(f"| Turnover < 1% | {sum(1 for r in rs if (r.get('turnover') or 9) < 1)} |")

    out.append("")
    out.append("## Failed-check frequency (resolved names)\n")
    counter: Counter = Counter()
    for r in rs:
        for name in r["failed_checks"]:
            counter[name] += 1
    out.append(f"({len(rs)} result blocks; each block can fail several checks)\n")
    out.append("| Check failed | Blocks | Share |")
    out.append("|---|---:|---:|")
    total = max(len(rs), 1)
    for name, n in counter.most_common():
        out.append(f"| {name} | {n} | {100.0 * n / total:.1f}% |")

    def train_of(r: Dict[str, Any]) -> Any:
        """Decay-style pages report Train Fitness instead of Train Sharpe."""
        v = r.get("train_sharpe")
        return v if v is not None else r.get("train_fitness")

    def table(title: str, rows: Iterable[Dict[str, Any]], key) -> None:
        rows = sorted(rows, key=lambda r: key(r) if key(r) is not None else -9, reverse=True)
        out.append("")
        out.append(f"## {title}\n")
        if not rows:
            out.append("_none_")
            return
        out.append("| # | Universe | Neut | Sharpe | Train | Fitness | Turnover | Returns | DD | Margin bps | Family | Expression | Failed |")
        out.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
        for r in rows:
            out.append(
                "| {n} | {u} | {ne} | {sh} | {tr} | {fi} | {to} | {re} | {dd} | {mg} | {fam} | {ex} | {fa} |".format(
                    n=r.get("result_no"),
                    u=r.get("universe") or "—",
                    ne=r.get("neutralization") or "—",
                    sh=_fmt(r.get("sharpe")), tr=_fmt(train_of(r)),
                    fi=_fmt(r.get("fitness")), to=_fmt(r.get("turnover"), "%"),
                    re=_fmt(r.get("returns"), "%"), dd=_fmt(r.get("drawdown"), "%"),
                    mg=_fmt(r.get("margin_bps")), fam=r.get("family"),
                    ex=fmt_expr(r.get("expression", "")),
                    fa="; ".join(r.get("failed_checks", [])) or (r.get("status") or "")))

    table("Top 30 by Sharpe", rs[:30], lambda r: r.get("sharpe"))
    table("Top 30 by Fitness", rs[:30], lambda r: r.get("fitness"))
    table("Top 20 by margin (bps)", rs[:20], lambda r: r.get("margin_bps"))
    table("Top 20 by returns (%)", rs[:20], lambda r: r.get("returns"))
    table("Worst 10 by Sharpe", rs[-10:], lambda r: -(r.get("sharpe") or -9))

    if sharpe_fit:
        table("Sharpe ≥ 1.25 and Fitness ≥ 1.0", sharpe_fit,
              lambda r: (r.get("sharpe") or 0) + (r.get("fitness") or 0))

    # Per-section best
    sections: "OrderedDict[Tuple[str, str], List[Dict[str, Any]]]" = OrderedDict()
    for r in rs:
        sections.setdefault((r.get("universe") or "—", r.get("neutralization") or "—"), []).append(r)
    out.append("")
    out.append("## Best per universe / neutralization\n")
    out.append("| Universe | Neut | Blocks | Best Sharpe | Best Fitness | Best Sharpe expr |")
    out.append("|---|---|---:|---:|---:|---|")
    for (u, ne), group in sections.items():
        bs = max(group, key=lambda r: r.get("sharpe") or -9)
        bf = max(group, key=lambda r: r.get("fitness") or -9)
        out.append(f"| {u} | {ne} | {len(group)} | {_fmt(bs.get('sharpe'))} | "
                   f"{_fmt(bf.get('fitness'))} | {fmt_expr(bs.get('expression', ''))} |")

    decays = sorted({r["decay"] for r in rs if r.get("decay") is not None})
    if decays:
        out.append("")
        out.append("## By decay\n")
        out.append("| Decay | Truncation | Blocks | Best Sharpe | Best Fitness | Best expr (by Sharpe) | Failed |")
        out.append("|---:|---|---:|---:|---:|---|---|")
        for d in decays:
            grp = [r for r in rs if r.get("decay") == d]
            trs = ", ".join(sorted({str(r.get("truncation")) for r in grp}))
            bs = max(grp, key=lambda r: r.get("sharpe") or -9)
            bf = max(grp, key=lambda r: r.get("fitness") or -9)
            out.append(f"| {d} | {trs} | {len(grp)} | {_fmt(bs.get('sharpe'))} | "
                       f"{_fmt(bf.get('fitness'))} | {fmt_expr(bs.get('expression', ''))} | "
                       f"{'; '.join(bs.get('failed_checks', [])) or bs.get('status', '')} |")

    # Families
    fams: Counter = Counter(r["family"] for r in rs)
    fam_best: Dict[str, Dict[str, Any]] = {}
    for r in rs:
        cur = fam_best.get(r["family"])
        if cur is None or (r.get("sharpe") or -9) > (cur.get("sharpe") or -9):
            fam_best[r["family"]] = r
    out.append("")
    out.append("## Field families (by primary ts_backfill field)\n")
    out.append("| Family | Blocks | Best Sharpe | Best Fitness | Best expr |")
    out.append("|---|---:|---:|---:|---|")
    for fam, n in fams.most_common():
        b = fam_best[fam]
        out.append(f"| {fam} | {n} | {_fmt(b.get('sharpe'))} | {_fmt(b.get('fitness'))} | "
                   f"{fmt_expr(b.get('expression', ''))} |")

    empty = [r for r in rs if not r.get("expression")]
    if empty:
        out.append("")
        out.append(f"## Malformed blocks\n\n{len(empty)} block(s) had no expression: "
                   + ", ".join(f"#{r['result_no']}" for r in empty))

    out.append("")
    return "\n".join(out)


def write_combined(dumps: List[Dict[str, Any]], outdir: str, prefix: str = "") -> None:
    cols = ["dump", "result_no", "universe", "neutralization", "decay", "truncation",
            "family", "primary_field",
            "sharpe", "train_sharpe", "train_fitness", "fitness", "turnover",
            "returns", "drawdown",
            "margin_bps", "long_count", "short_count", "status",
            "failed_check_codes", "failed_checks", "expression"]
    path = os.path.join(outdir, prefix + "all_results.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for d in dumps:
            slug = dump_slug(d, multi=len(dumps) > 1)
            for r in d["results"]:
                vals = []
                for c in cols:
                    v = slug if c == "dump" else r.get(c, "")
                    if isinstance(v, list):
                        v = ",".join(v)
                    vals.append("" if v is None else v)
                w.writerow(vals)

    out: List[str] = ["# Cross-dump summary\n"]
    out.append("| Dump | Blocks | Region | Decay | Universes | S&P ≥1.25 | Fitness ≥1.0 | PASS | Top Sharpe |")
    out.append("|---|---:|---|---:|---|---:|---:|---:|---:|")
    for d in dumps:
        rs = d["results"]
        unis = sorted({r.get("universe") or d["settings"].get("Universe") or "—" for r in rs})
        n_sf = sum(1 for r in rs if (r.get("sharpe") or -9) >= 1.25 and (r.get("fitness") or -9) >= 1.0)
        n_f = sum(1 for r in rs if (r.get("fitness") or -9) >= 1.0)
        n_pass = sum(1 for r in rs if r["status"] == "PASS")
        top = max(rs, key=lambda r: r.get("sharpe") or -9)
        out.append(f"| `{dump_slug(d, multi=len(dumps) > 1)}` | {len(rs)} | "
                   f"{d['settings'].get('Region', '—')} | "
                   f"{d['settings'].get('Decay', '—')} | {', '.join(unis)} | {n_sf} | {n_f} | "
                   f"{n_pass} | {_fmt(top.get('sharpe'))} |")
    out.append("")

    seen: Dict[str, List[str]] = {}
    for d in dumps:
        for r in d["results"]:
            seen.setdefault(r.get("expression", ""), []).append(
                f"{dump_slug(d, multi=len(dumps) > 1)}#{r.get('result_no')}")
    dupes = {k: v for k, v in seen.items() if len(v) > 1 and k}
    out.append(f"## Expressions repeated across dumps\n\n{len(dupes)} expressions appear in more than one dump.\n")
    if dupes:
        out.append("| Expression | Occurrences |")
        out.append("|---|---|")
        for expr, where in list(dupes.items())[:40]:
            out.append(f"| {fmt_expr(expr)} | {', '.join(where)} |")
        out.append("")

    with open(os.path.join(outdir, prefix + "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))


SELFTEST_SAMPLE = """3 Results

Simulation Settings
Region: EUR
Universe: TOP2500
Delay: 1
Decay: 5

Failed Check Sets
F1: LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE
F2: LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE

## Universe: TOP2500

### Neutralization: MARKET

#### Result 1
- Expression: `ts_rank(ts_backfill(pv37_volume_1, 21), 63)`
- Train Sharpe: 2.43
- Sharpe: 2.16
- Turnover: 45.10%
- Fitness: 0.96
- Returns: 8.90%
- Drawdown: 6.36%
- Margin: 3.95 bps
- Long Count: 1388
- Short Count: 1431
- Checks: FAIL F1

#### Result 2
- Expression: `rank(ts_backfill(fnd28_value_09202, 21))`
- Train Sharpe: 1.21
- Sharpe: 1.49
- Turnover: 2.45%
- Fitness: 1.20
- Returns: 5.16%
- Drawdown: 11.92%
- Margin: 42.09 bps
- Long Count: 1113
- Short Count: 1041
- Checks: FAIL F2

### Neutralization: INDUSTRY

#### Result 3
- Expression: `scale(ts_backfill(pv20_eps_indicator_3_feature12_394, 21))`
- Train Sharpe: 1.33
- Sharpe: 1.32
- Turnover: 19.12%
- Fitness: 1.09
- Returns: 12.99%
- Drawdown: 16.96%
- Margin: 13.59 bps
- Long Count: 631
- Short Count: 608
- Checks: PASS
"""


MULTI_SAMPLE = """2 Results

Simulation Settings
Region: KOR
Universe: TOP600
Delay: 1
Decay: 5

Failed Check Sets
F1: LOW_SHARPE, LOW_FITNESS

## Neutralization: INDUSTRY

### Result 1
- Expression: `normalize(ts_backfill(oth176_lmt_close_eq_score, 21))`
- Train Sharpe: 2.79
- Sharpe: 2.36
- Turnover: 32.62%
- Fitness: 1.67
- Returns: 16.28%
- Drawdown: 13.39%
- Margin: 9.98 bps
- Long Count: 264
- Short Count: 1018
- Checks: FAIL F1

## Neutralization: MARKET

### Result 2
- Expression: `rank(ts_backfill(anl69_sales_best_eeps_cur_yr, 21))`
- Train Sharpe: 1.97
- Sharpe: 1.90
- Turnover: 5.78%
- Fitness: 1.58
- Returns: 8.20%
- Drawdown: 6.10%
- Margin: 20.00 bps
- Long Count: 700
- Short Count: 650
- Checks: FAIL F1

1 Results

Simulation Settings
Region: USA
Universe: TOP3000
Delay: 1
Pasteurization: ON
NaN Handling: ON

Failed Check Sets
F1: CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE
F2: LOW_FITNESS, IS_LADDER_SHARPE

## Neutralization: MARKET

### Decay: 4 · Truncation: 0.08
- Expression: `iv_signal = zscore(implied_volatility_call_120 - implied_volatility_put_120); group_neutralize(iv_signal, bucket(rank(cap), range="0.1,1,0.1"))`
- Train Fitness: 1.56
- Sharpe: 2.34
- Turnover: 48.23%
- Fitness: 1.47
- Returns: 19.05%
- Drawdown: 9.19%
- Margin: 7.90 bps
- Long Count: 1445
- Short Count: 1091
- Checks: FAIL F2
"""


def selftest() -> int:
    import tempfile
    failures: List[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "Pasted text(20261006-100742).txt")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(SELFTEST_SAMPLE)
        dump = parse_dump(src)
        rs = dump["results"]

        def check(cond: bool, msg: str) -> None:
            if not cond:
                failures.append(msg)

        check(dump["declared_count"] == 3, f"declared count {dump['declared_count']} != 3")
        check(len(rs) == 3, f"parsed {len(rs)} blocks != 3")
        check(dump["settings"].get("Region") == "EUR", "region not parsed")
        check(rs[0]["neutralization"] == "MARKET", "market section not applied")
        check(rs[2]["neutralization"] == "INDUSTRY", "industry section not applied")
        check(rs[0]["sharpe"] == 2.16, "sharpe parse")
        check(rs[0]["turnover"] == 45.10, "turnover parse")
        check(rs[0]["margin_bps"] == 3.95, "margin parse")
        check(rs[0]["failed_checks"] == ["LOW_SHARPE", "LOW_FITNESS", "LOW_2Y_SHARPE"],
              f"legend resolution: {rs[0]['failed_checks']}")
        check(rs[1]["failed_checks"] == ["LOW_SUB_UNIVERSE_SHARPE", "LOW_2Y_SHARPE"],
              f"second legend resolution: {rs[1]['failed_checks']}")
        check(rs[2]["status"] == "PASS", "PASS detection")
        check(rs[0]["primary_field"] == "pv37_volume_1", "primary field via ts_backfill")
        check(rs[1]["primary_field"] == "fnd28_value_09202", "primary field fallback")
        check(rs[2]["family"] == "pv20 (price/volume)", f"family: {rs[2]['family']}")
        # File-specific legend: F1 in this file must not equal F1 elsewhere.
        other = dict(dump["legend"])
        check(other["F1"] != other["F2"], "legend entries collapsed")
        slug = write_outputs(dump, tmp)
        for ext in (".csv", ".json", ".md"):
            p = os.path.join(tmp, slug + ext)
            check(os.path.getsize(p) > 0, f"empty output {p}")
        check(slug == "20261006_100742", f"slug: {slug}")

        # --- several pages concatenated in one file -------------------------
        multi_src = os.path.join(tmp, "Pasted text(20261009-115500).txt")
        with open(multi_src, "w", encoding="utf-8") as fh:
            fh.write(MULTI_SAMPLE)
        pages = parse_dumps(multi_src)
        check(len(pages) == 2, f"expected 2 pages, got {len(pages)}")
        p1, p2 = pages
        check(p1["declared_count"] == 2 and len(p1["results"]) == 2, "page 1 size")
        check(p2["declared_count"] == 1 and len(p2["results"]) == 1, "page 2 size")
        check(p1["settings"].get("Region") == "KOR", "page 1 settings isolated")
        check(p2["settings"].get("Region") == "USA", "page 2 settings isolated")
        check(p1["legend"]["F1"] == ["LOW_SHARPE", "LOW_FITNESS"], "page 1 legend")
        check(p2["legend"]["F1"] == ["CONCENTRATED_WEIGHT", "LOW_SUB_UNIVERSE_SHARPE"],
              "page 2 legend must not inherit page 1's")
        check(p1["results"][0]["neutralization"] == "INDUSTRY", "page 1 section")
        check(p1["results"][1]["neutralization"] == "MARKET", "page 1 section switch")
        check(p1["universe_labels"] == ["TOP600"], f"page 1 universes: {p1['universe_labels']}")
        check(p2["results"][0]["neutralization"] == "MARKET", "page 2 section")
        check(p2["results"][0]["universe"] == "TOP3000", "page 2 universe from settings")
        b = p2["results"][0]
        check(b["decay"] == 4 and b["truncation"] == 0.08, f"decay header: {b.get('decay')}")
        check(b["train_fitness"] == 1.56, f"train fitness: {b.get('train_fitness')}")
        check(b["number_synthesised"] is True, "synthesised numbering flag")
        check(b["failed_checks"] == ["LOW_FITNESS", "IS_LADDER_SHARPE"],
              f"page 2 checks: {b.get('failed_checks')}")
        check(b["expression"].startswith("iv_signal ="), "multi-statement expression kept")
        slugs = [dump_slug(d, multi=True) for d in pages]
        check(len(set(slugs)) == 2, f"page slugs must differ: {slugs}")
        check(slugs[0] == "20261009_115500_d1_kor_top600", f"page 1 slug: {slugs[0]}")
        check(slugs[1] == "20261009_115500_d2_usa_top3000", f"page 2 slug: {slugs[1]}")
        for d in pages:
            write_outputs(d, tmp, multi=True)
        check(os.path.getsize(os.path.join(tmp, slugs[0] + ".csv")) > 0, "page csv")
        check(os.path.getsize(os.path.join(tmp, slugs[1] + ".md")) > 0, "page md")
        write_combined(pages, tmp, prefix="20261009_115500_")
        check(os.path.getsize(os.path.join(tmp, "20261009_115500_all_results.csv")) > 0,
              "prefixed combined csv")
        check(not os.path.exists(os.path.join(tmp, "all_results.csv")),
              "--prefix must keep the bare combined filenames unused")

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print(" -", f)
        return 1
    print("SELFTEST PASSED (3/3 blocks, legend resolution, sections, outputs)")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dumps", nargs="*", help="pasted result dump .txt files")
    ap.add_argument("--outdir", default="simulations/sweeps", help="output directory")
    ap.add_argument("--prefix", default="", help="filename prefix for the combined "
                    "all_results.csv / SUMMARY.md, so a new bundle cannot overwrite "
                    "one already stored in the same directory")
    ap.add_argument("--selftest", action="store_true", help="run built-in checks and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.dumps:
        ap.error("provide at least one dump file (or --selftest)")

    dumps = []
    for path in args.dumps:
        if not os.path.isfile(path):
            print(f"missing file: {path}", file=sys.stderr)
            return 2
        pages = parse_dumps(path)
        multi = len(pages) > 1
        if multi:
            print(f"{os.path.basename(path)}: {len(pages)} concatenated pages")
        for dump in pages:
            if dump["declared_count"] not in (None, len(dump["results"])):
                print(f"warning: {os.path.basename(path)} page {dump['dump_index']} "
                      f"declared {dump['declared_count']} results but "
                      f"{len(dump['results'])} were parsed", file=sys.stderr)
            slug = write_outputs(dump, args.outdir, multi=multi)
            print(f"  page {dump['dump_index']} "
                  f"({dump['settings'].get('Region', '?')} / "
                  f"{', '.join(dump.get('universe_labels') or ['?'])}): "
                  f"{len(dump['results'])} blocks -> "
                  f"{os.path.join(args.outdir, slug)}.[csv,json,md]")
        dumps.extend(pages)

    if len(dumps) > 1:
        write_combined(dumps, args.outdir, args.prefix)
        print(f"combined -> {os.path.join(args.outdir, args.prefix + 'all_results.csv')}, "
              f"{os.path.join(args.outdir, args.prefix + 'SUMMARY.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
