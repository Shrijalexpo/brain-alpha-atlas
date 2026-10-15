# Command and Workflow Playbook

Standardized shorthand commands and iteration rules for interactive Alpha research sessions in this repository (`[Notes]`).

## 1. Core Operational Rules

1. **Check the Ledger First:** Before generating or fixing an Alpha, inspect [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/index.md) and [`status-and-duplicate-ledger.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/status-and-duplicate-ledger.md).
2. **Save Before Iterating:** Whenever a new simulation result or export arrives, save its record in `Analysis and Simulation Reports/simulation-results/<REGION>/` and reconcile `Analysis and Simulation Reports/index.md` via `python3 Tools/documentation-validation/verify_index.py` before proposing the next iteration.
3. **Never Repeat Exhausted Expressions:** Never propose an exact expression already marked `FAILED`, `ERROR`, `FAILED_SELF_CORRELATION`, `PASSED_SUBMITTABLE`, or `PASSED_SUBMITTED`.
4. **At Most 1 to 3 Candidates at a Time:** Propose 1–3 focused, hypothesis-backed expressions per iteration, changing one mechanism at a time.

## 2. Shorthand Command Reference

| Command Tag | Purpose & Required Action |
|---|---|
| `#new` (or `#new <theme>`) | Propose 1–3 fresh Alpha candidates with explicit economic intuition, avoiding all previously tested structures in `Analysis and Simulation Reports/index.md`. |
| `#fix` | Diagnose the primary bottleneck (`Sharpe`, `Fitness`, `Turnover`, `Sub-universe Sharpe`, `Weight concentration`, `LOW_2Y_SHARPE`, `Self/Prod-Correlation`, or syntax error) of the shared result, record the simulation, and propose 1–3 single-mechanism repairs. |
| `#save` | Record a new simulation result, sweep export, field note, or reference into its canonical folder (`Analysis and Simulation Reports/`, `Docs/`, or `Books/`) and run `verify_index.py` / `check_docs.py` without generating new Alpha candidates. |
| `#learn` | Synthesize empirical patterns from recent simulation records and update [`lessons-from-simulations.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/lessons-from-simulations.md) and [17 — Case Studies and Lessons Learned](../17-case-studies-and-lessons-learned/index.md). |
| `#status` | Summarize current submitted baselines, near-miss repair candidates, regional sweep coverage, and active research priorities. |
| `#settings` | Recommend simulation settings (`Region`, `Universe`, `Delay`, `Neutralization`, `Decay`, `Truncation`, `Max Trade`) tailored to the specific dataset and market scope. |
| `#fields` | Classify newly shared data fields by theme, type (`Matrix` vs `Vector` vs `Group`), coverage, and crowding, and log them in [Dataset Catalog and Field Notes](../04-data-explorer-and-datasets/dataset-catalog-and-field-notes.md). |
| `#error` | Diagnose a BRAIN validation or runtime error, log recurring patterns in [Troubleshooting and Error Catalog](troubleshooting-and-errors.md), and provide a corrected Fast Expression. |
| `#submitted` | Mark a verified simulation record as `PASSED_SUBMITTED` or `PASSED_SUBMITTABLE`, update `Analysis and Simulation Reports/index.md`, and add its exact expression to the protected baseline list. |
| `#correlation` | Record a correlation rejection as `FAILED_SELF_CORRELATION`, identify the shared factor backbone, and propose 1–3 structurally orthogonal replacements. |
| `#avoid` | Add a newly identified dead-end field or operator pattern to the avoidance list in [Dataset Catalog and Field Notes](../04-data-explorer-and-datasets/dataset-catalog-and-field-notes.md) and [16 — Quantitative Research Methodology](../16-quantitative-research-methodology/index.md). |
