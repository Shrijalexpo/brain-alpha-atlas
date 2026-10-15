# CLAUDE.md

Guidance for AI coding and quantitative research assistants working in the `brain-alpha-atlas` repository.

## Repository Architecture (Four Canonical Content Directories)

```text
brain-alpha-atlas/
├── Docs/                              17-module progressive WorldQuant BRAIN consultant curriculum + reference/
├── Tools/                             Python sweep parsers, index reconcilers, doc/ISIN validators & ACE API
├── Books/                             Academic papers, formula libraries (Alpha101/158) & official captures
└── Analysis and Simulation Reports/   71 experiment records, regional results, sweep CSVs & raw exports
```

Do **not** create additional top-level content directories.

## Key Entry Points

- **Curriculum Home:** `Docs/index.md`
- **Command & Workflow Playbook:** `Docs/reference/command-and-workflow-playbook.md` (`#new`, `#fix`, `#save`, `#learn`, `#status`, `#settings`, `#fields`, `#error`, `#submitted`, `#correlation`, `#avoid`)
- **Master Experiment & Sweep Index:** `Analysis and Simulation Reports/index.md`
- **Quick Duplicate-Avoidance Ledger:** `Analysis and Simulation Reports/alpha-research/status-and-duplicate-ledger.md`
- **Machine-Readable 71-Experiment Catalog:** `Analysis and Simulation Reports/aggregate-analytics/master_experiments_catalog.csv`
- **Tools Guide:** `Tools/README.md`
- **Literature & Official Captures Catalog:** `Books/README.md`

## Validation & Build Commands

Run all checks from the repository root before completing any documentation or experiment update:

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
