# 15 — Alpha Harness & Reproducible Local Research Architecture

## 1. Learning Objectives

By completing this module, you will be able to:

- Understand how the four repository pillars (`Docs/`, `Tools/`, `Books/`, `Analysis and Simulation Reports/`) operate together as a reproducible local **Alpha Research Harness**.
- Run the complete offline parsing, index reconciliation, ISIN validation, and documentation hygiene pipeline from the command line and CI.
- Identify the boundary between the implemented local toolkit and external/future Alpha Harness extensions.

## 2. Prerequisites

- [14 — BRAIN API and Automation](../14-brain-api-and-automation/index.md)

## 3. Core Concepts: Architecture of the Local Research Harness

In this repository, the **Alpha Harness** is the end-to-end operational pipeline that connects live WorldQuant BRAIN simulations to structured, machine-verified local evidence (`[Notes]`):

```text
[1. Hypothesis & Literature]
    Books/ (Kakushadze 101, Qlib 158, Official 78-Article Archive)
    Docs/  (Progressive 17-Module Consultant Curriculum)
          │
          ▼
[2. Simulation Execution]
    BRAIN Web Simulator / Multi-Simulation (8 x 10 batches)
    Tools/api-and-automation/ace-api/ (ace_lib.py + brain-ace Conda env)
          │
          ▼
[3. Automated Ingestion & Parsing]
    Tools/simulation-processing/brain_sweep_parser.py
     Raw Pasted Export (source-data/*.txt)
      -> Per-Page Fx Legend Resolution
      -> Out-of-Sample Sharpe vs Train Sharpe Separation
      -> Structured CSV / JSON / Markdown Reports (sweeps-and-experiments/)
          │
          ▼
[4. Canonical Evidence & Automated Verification]
    Analysis and Simulation Reports/
      ├── simulation-results/{USA,EUR,KOR,AMR,GLB,multi-region}/ (Records 001–071)
      ├── aggregate-analytics/master_experiments_catalog.csv
      └── index.md  <── Reconciled by Tools/documentation-validation/verify_index.py
                    <── Audited by Tools/documentation-validation/check_docs.py
```

### Why Offline Verification Matters

Two actual defects caught and repaired by this harness demonstrate why automated verification is essential (`[Observed]`):

1. **The `Train Sharpe` Inflation Defect (Simulation `070`):** An initial ad-hoc parse of the 2,500-block USA sweep copied the `Train Sharpe` column into `sharpe` and missed the second page (`1,050` blocks). `brain_sweep_parser.py` and `verify_index.py` exposed that `Train Sharpe` differed from true out-of-sample `Sharpe` in **2,448 of 2,500 rows**, quarantined the defective CSV in `sweeps-and-experiments/superseded/`, and regenerated the verified 3,550-row dataset (`[Observed]`).
2. **Per-Page `Fx` Failed-Check Legend Collision (Simulations `067`–`071`):** BRAIN abbreviates failed-check sets as `F1`, `F2`, ..., `F14`, **re-numbering the legend independently on every results page**. Comparing raw `F14` codes across pages corrupts failure statistics; `brain_sweep_parser.py` resolves every code through its own page's legend before emitting `failed_checks` (`[Observed]`).

## 4. Step-by-Step Explanations: Operating the Harness

### Step 1: Ingesting a New Multi-Simulation Export

When you paste one or more BRAIN multi-simulation pages (`N Results`) into a raw text file:

1. Save the unmodified text export under `Analysis and Simulation Reports/source-data/<YYYYMMDD_HHMMSS>.txt` and record its MD5/SHA-256 checksum in `source-data/README.md`.
2. Run the sweep parser:
   ```bash
   python3 Tools/simulation-processing/brain_sweep_parser.py \
     "Analysis and Simulation Reports/source-data/<YYYYMMDD_HHMMSS>.txt" \
     --outdir "Analysis and Simulation Reports/sweeps-and-experiments" \
     --prefix <YYYYMMDD_HHMMSS>_
   ```
3. Create the next numbered experiment record (`072_*.md`) in the appropriate regional subfolder of `Analysis and Simulation Reports/simulation-results/` using [`simulation-template.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/simulation-template.md).
4. Add the summary row to `Analysis and Simulation Reports/index.md` and run `verify_index.py`:
   ```bash
   python3 Tools/documentation-validation/verify_index.py
   ```

### Step 2: Running the Full Pre-Commit Quality Gate

Before committing any documentation or experiment update, run the exact sequence enforced by `.github/workflows/docs-ci.yml`:

```bash
python3 Tools/simulation-processing/brain_sweep_parser.py --selftest
python3 Tools/alpha-analysis/validate_spc_isin.py --selftest
python3 Tools/documentation-validation/check_docs.py --selftest
python3 Tools/documentation-validation/verify_index.py --selftest

python3 Tools/documentation-validation/check_docs.py Docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS
python3 Tools/documentation-validation/verify_index.py
.venv-docs/bin/mkdocs build --strict
python3 Tools/documentation-validation/check_docs.py --text-scan site
```

### Step 3: Research Gap / Future Extension Note on External "Alpha Harness" Frameworks

> **Scope Note (`[Notes]`):** If "Alpha Harness" in your workflow also refers to an external CLI/orchestrator package (such as a custom local batch runner, Parquet simulation hash-cache manager, or automated BrainLabs testing harness not yet committed to this repository), place its Python modules under `Tools/` (for example, `Tools/api-and-automation/`) and document its configuration schema here. No external Alpha Harness binary was present in the repository inventory during the 2026-10-15 audit.

## 5. Working Examples: Inspecting `brain_sweep_parser.py` Output Schema

Every CSV generated by `brain_sweep_parser.py` in `Analysis and Simulation Reports/sweeps-and-experiments/` contains 21 standardized columns:

```text
result_no, universe, neutralization, decay, truncation, family, primary_field,
sharpe, train_sharpe, train_fitness, fitness, turnover, returns, drawdown,
margin_bps, long_count, short_count, status, failed_check_codes, failed_checks, expression
```

## 6. Common Mistakes and Troubleshooting

- **Editing `Analysis and Simulation Reports/index.md` without updating the canonical record file:** `verify_index.py` treats `simulation-results/**/*.md` and `sweeps-and-experiments/*.csv` as the primary authority and will fail with `metric-value`, `status-section`, or `expression-prefix` errors if `index.md` drifts (`[Notes]`).
- **Treating `PENDING` blocks in a sweep export as passes:** `verify_index.py` enforces rule `pending-claimed-passed` so an unevaluated `PENDING` simulation block can never be recorded as a passing Alpha (`[Observed]`).

## 7. Practical Exercises

1. Run `python3 Tools/documentation-validation/verify_index.py` and inspect the summary line (`records=71 indexed=71 experiment-rows=66 sweep-rows=5 decay-dumps-compared=1 errors=0 warnings=0`).
2. Run `python3 Tools/documentation-validation/check_docs.py Docs README.md` to verify zero broken links or formatting defects.

## 8. Related Topics and Next Steps

- **Next Module:** [16 — Quantitative Research Methodology](../16-quantitative-research-methodology/index.md)
- **Tools Reference:** [`Tools/README.md`](../../Tools/README.md)

## 9. Sources and Verification

- **Sources:** Repository tooling [`brain_sweep_parser.py`](../../Tools/simulation-processing/brain_sweep_parser.py), [`verify_index.py`](../../Tools/documentation-validation/verify_index.py), [`check_docs.py`](../../Tools/documentation-validation/check_docs.py), and `.github/workflows/docs-ci.yml` (`[Notes]`, `[Observed]`).
- **Verification Date:** 2026-10-15.
