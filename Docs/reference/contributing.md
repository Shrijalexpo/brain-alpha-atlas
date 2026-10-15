# Contributing to the Knowledge Base

How to add new simulation records, multi-simulation sweeps, curriculum updates, utilities, or external references while maintaining repository hygiene.

## 1. Where Every File Belongs (The Four-Folder Architecture)

This repository enforces a strict four-directory content layout at the root:

| Directory | What Belongs Here |
|---|---|
| [`Docs/`](../index.md) | Progressive consultant curriculum (`01`–`17`) and quick reference guides (`reference/`) |
| [`Tools/`](../../Tools/README.md) | Python parsers, validators, index reconcilers, and API automation scripts |
| [`Books/`](../../Books/README.md) | External textbooks, academic papers, code-level factor collections, and official platform documentation captures |
| [`Analysis and Simulation Reports/`](../../Analysis%20and%20Simulation%20Reports/README.md) | All experiment records (`001`–`071+`), regional breakdowns, parsed sweep CSV/JSON/MD files, aggregate catalogs, and raw sweep exports |

Do **not** create extra top-level folders at the repository root.

## 2. Adding a New Single-Alpha Simulation (`072+`)

1. Copy [`simulation-template.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/simulation-template.md) to `Analysis and Simulation Reports/simulation-results/<REGION>/<NNN>_<slug>.md`.
2. Fill in the exact `Status:`, `Expression:`, `Settings:`, `Known result:`, `Conclusion:`, and `Standardized Research Record Metadata` table. Never invent uncaptured metrics; leave unknown fields blank or `unknown`.
3. Add the corresponding row to [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/index.md), [`status-and-duplicate-ledger.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/status-and-duplicate-ledger.md), and [`master_experiments_catalog.csv`](../../Analysis%20and%20Simulation%20Reports/aggregate-analytics/master_experiments_catalog.csv).
4. Reconcile the index:
   ```bash
   python3 Tools/documentation-validation/verify_index.py
   ```

## 3. Adding a Multi-Simulation Sweep Export

1. Save the raw pasted text to `Analysis and Simulation Reports/source-data/<YYYYMMDD_HHMMSS>.txt`.
2. Parse it with `brain_sweep_parser.py`:
   ```bash
   python3 Tools/simulation-processing/brain_sweep_parser.py \
     "Analysis and Simulation Reports/source-data/<YYYYMMDD_HHMMSS>.txt" \
     --outdir "Analysis and Simulation Reports/sweeps-and-experiments" \
     --prefix <YYYYMMDD_HHMMSS>_
   ```
3. Create the canonical sweep record in `Analysis and Simulation Reports/simulation-results/<REGION>/<NNN>_<slug>.md`, update `Analysis and Simulation Reports/index.md`, and run `verify_index.py`.

## 4. Pre-Commit Validation Checklist

Every change must pass all five checks before committing:

```bash
# 1. Run tool self-tests
python3 Tools/simulation-processing/brain_sweep_parser.py --selftest
python3 Tools/alpha-analysis/validate_spc_isin.py --selftest
python3 Tools/documentation-validation/check_docs.py --selftest
python3 Tools/documentation-validation/verify_index.py --selftest

# 2. Check Markdown links, table formatting, backticks, fences, and privacy rules
python3 Tools/documentation-validation/check_docs.py Docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS

# 3. Reconcile experiment index against all canonical records and sweep CSVs
python3 Tools/documentation-validation/verify_index.py

# 4. Build the MkDocs site in strict mode
.venv-docs/bin/mkdocs build --strict

# 5. Scan rendered HTML for accidental machine paths or secret patterns
python3 Tools/documentation-validation/check_docs.py --text-scan site
```

Never commit credentials, API tokens, session cookies, personal agreements, uncleared notebook outputs, or machine-specific absolute paths (such as `/Users/...`).
