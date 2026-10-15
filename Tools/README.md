# Research Tools and Automation Utilities

Dependency-free Python utilities for parsing multi-simulation sweeps, reconciling experiment indexes, validating Markdown hygiene and ISIN/MIC schemas, and automating WorldQuant BRAIN research workflows via the ACE API.

## Directory Structure

```text
Tools/
├── README.md                                  This catalog, usage reference, and dependency guide
├── simulation-processing/                     Parsers and report generators for BRAIN simulation exports
│   └── brain_sweep_parser.py                  Multi-simulation ("N Results") page parser -> CSV/JSON/MD
├── documentation-validation/                  Repository integrity, link, hygiene, and index validators
│   ├── check_docs.py                          Markdown link, table, backtick, fence, and privacy scanner
│   └── verify_index.py                        Reconciles experiment index against simulation records & CSVs
├── alpha-analysis/                            Competition schema and financial identifier validators
│   ├── validate_spc_isin.py                   ISO 6166 ISIN (Luhn mod-10), MIC, and SPC JSON validator
│   └── spc_sample_output_example.json         Reference sample output schema for SPC 2026 validation
└── api-and-automation/                        BRAIN API session management and batch simulation library
    └── ace-api/
        ├── README.md                          Original ACE library overview
        ├── SETUP_JUPYTER_ANACONDA.md          Environment setup for the local `brain-ace` Conda kernel
        ├── ace_lib.py                         Core BRAIN API authentication, simulation, and polling client
        ├── helpful_functions.py               DataFrame formatting, PnL concatenation, and result helpers
        ├── how_to_use.ipynb                   End-to-end Jupyter tutorial notebook for ACE workflows
        └── requirements.txt                   Python package dependencies for the ACE notebook environment
```

## Tool Inventory and Status

| Utility | Path | Purpose | Dependencies | Inputs & Outputs | Status |
|---|---|---|---|---|---|
| **Sweep Parser** | [`simulation-processing/brain_sweep_parser.py`](simulation-processing/brain_sweep_parser.py) | Parses pasted BRAIN multi-simulation pages (`N Results`), resolves per-page `Fx` failed-check legends, splits concatenated multi-page exports, and distinguishes `Sharpe` from `Train Sharpe` | Python 3.9+ standard library only | **In:** Raw pasted text file (`source-data/*.txt`)<br>**Out:** `<slug>.csv`, `<slug>.json`, `<slug>.md`, plus combined `all_results.csv` & `SUMMARY.md` | Active (`--selftest` passing) |
| **Documentation Hygiene Checker** | [`documentation-validation/check_docs.py`](documentation-validation/check_docs.py) | Checks Markdown files for broken relative links, mismatched table column counts, odd inline backticks, unclosed fences, excluded private references, absolute `/Users/` paths, and credential patterns; also scans built HTML (`--text-scan`) | Python 3.9+ standard library only | **In:** Markdown directories/files or built `site/` directory<br>**Out:** Line-addressed findings + exit code (`0` clean, `1` errors) | Active (`--selftest` passing) |
| **Experiment Index Reconciler** | [`documentation-validation/verify_index.py`](documentation-validation/verify_index.py) | Verifies that every experiment record (`001`–`071`) and sweep CSV in `Analysis and Simulation Reports/` reconciles line-by-line with `Analysis and Simulation Reports/index.md` | Python 3.9+ standard library (imports `split_row` from `check_docs.py`) | **In:** `Analysis and Simulation Reports/index.md`, `simulation-results/**/*.md`, `sweeps-and-experiments/*.csv`<br>**Out:** Reconciliation report + exit code (`0` consistent, `1` error) | Active (`--selftest` passing) |
| **SPC & ISIN Validator** | [`alpha-analysis/validate_spc_isin.py`](alpha-analysis/validate_spc_isin.py) | Validates ISO 6166 ISIN check digits, ISO 10383 MIC codes, and Systematic Prediction Challenge (SPC) JSON output files | Python 3.9+ standard library (optional `python-stdnum` cross-check if installed) | **In:** JSON sample output file or `--isin <CODE>`<br>**Out:** Per-record validation report + exit code | Active (`--selftest` passing) |
| **Alpha Creation Engine (ACE API)** | [`api-and-automation/ace-api/ace_lib.py`](api-and-automation/ace-api/ace_lib.py) | Automates authentication (including Persona biometric URL handling), single/multi-simulation submission, rate-limit backoff, and dataset/field retrieval against `https://api.worldquantbrain.com` | `pandas`, `requests`, `tqdm`, `matplotlib`, `seaborn`, `plotly`, `networkx`, `notebook` (see [`api-and-automation/ace-api/requirements.txt`](api-and-automation/ace-api/requirements.txt)) | **In:** Credentials from `~/.brain_credentials` or `~/secrets/platform-brain.json` (never stored in repo), Alpha config dicts<br>**Out:** Simulation stats, PnL DataFrames, yearly stats | Active (local only; excluded from public git push via `.gitignore`) |

## Quick Usage Reference

### 1. Run All Tool Self-Tests

```bash
python3 Tools/simulation-processing/brain_sweep_parser.py --selftest
python3 Tools/documentation-validation/check_docs.py --selftest
python3 Tools/documentation-validation/verify_index.py --selftest
python3 Tools/alpha-analysis/validate_spc_isin.py --selftest
```

### 2. Validate Repository Documentation and Experiment Index

```bash
# Check Markdown links, table formatting, and hygiene across Docs/ and root files
python3 Tools/documentation-validation/check_docs.py Docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS

# Reconcile Analysis and Simulation Reports/index.md against all 71 records and sweep CSVs
python3 Tools/documentation-validation/verify_index.py

# Build the MkDocs site and scan rendered HTML for accidental path or secret leaks
.venv-docs/bin/mkdocs build --strict
python3 Tools/documentation-validation/check_docs.py --text-scan site
```

### 3. Parse a Multi-Simulation Sweep Export

```bash
python3 Tools/simulation-processing/brain_sweep_parser.py \
  "Analysis and Simulation Reports/source-data/20261009_115500.txt" \
  --outdir "Analysis and Simulation Reports/sweeps-and-experiments" \
  --prefix 20261009_115500_
```

### 4. Validate SPC 2026 JSON Output or Individual ISINs

```bash
python3 Tools/alpha-analysis/validate_spc_isin.py Tools/alpha-analysis/spc_sample_output_example.json
python3 Tools/alpha-analysis/validate_spc_isin.py --isin US0378331005
```

## Credential and Security Policy

- **Never commit credentials, API tokens, session cookies, or account identifiers.**
- Store BRAIN API credentials outside the repository (for example, `~/.brain_credentials` or `~/secrets/platform-brain.json` with `chmod 600` permissions).
- Clear Jupyter notebook outputs (`jupyter nbconvert --clear-output --inplace`) before sharing any notebook.
