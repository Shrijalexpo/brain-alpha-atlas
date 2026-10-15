# Changelog

Chronological record of major structural, analytical, and documentation milestones in **BRAIN Alpha Atlas**.

## 2026-10-15 — Complete Four-Folder Repository Audit and Curriculum Reorganization

- **Four-Directory Canonical Architecture:** Reorganized the entire repository into four primary top-level content directories:
  - [`Docs/`](../index.md) — 17-module progressive WorldQuant BRAIN consultant curriculum (`01-getting-started/` through `17-case-studies-and-lessons-learned/`) plus `reference/`.
  - [`Tools/`](../../Tools/README.md) — Categorized Python utilities under `simulation-processing/`, `documentation-validation/`, `alpha-analysis/`, and `api-and-automation/ace-api/`.
  - [`Books/`](../../Books/README.md) — Structured library under `books/`, `research-papers/`, `technical-guides/`, `official-documentation/`, and `bibliographies/` with full bibliographic metadata and SHA-256 provenance checksums.
  - [`Analysis and Simulation Reports/`](../../Analysis%20and%20Simulation%20Reports/README.md) — Centralized empirical evidence hub organizing all 71 experiment records by region (`USA`, `EUR`, `KOR`, `AMR`, `GLB`, `multi-region`), parsed sweep datasets (`sweeps-and-experiments/`), research ledgers (`alpha-research/`), raw exports (`source-data/`), and a machine-readable 71-row catalog (`aggregate-analytics/master_experiments_catalog.csv`).
- **Consolidated Legacy Top-Level Folders:** Merged and retired scattered top-level directories (`Data/`, `Operators/`, `Research/`, `Troubleshooting/`, `tutorials/`, `simulations/`, `_private_review/`, `.remember/`, `.freebuff/`, `site-preview313/`, `.venv-docs313/`) with a full recoverable backup and deletion log.
- **Restored & Repaired Broken Tutorial Links:** Resolved all 78 broken links previously in `docs/platform_tutorial_index.md` and reunited the 78 official platform documentation articles with their 142 figures under `Books/official-documentation/brain-platform-docs/`.
- **Standardized Research Record Metadata:** Enriched all 71 simulation records (`001`–`071`) with standardized metadata tables while maintaining 100% consistency with `verify_index.py`.

## 2026-10-09 — Multi-Region Sweep Bundle (`071`), USA Sweep Correction (`070`), and Verification Tooling

- Recorded Simulation `071` (`5,546` blocks across 6 pages covering `KOR`, `AMR`, `EUR`, `ALL`, and `USA`).
- Corrected Simulation `070` (`3,550` USA blocks across 2 pages), separating `Train Sharpe` from out-of-sample `Sharpe` and archiving superseded files under `superseded/`.
- Added `Tools/documentation-validation/check_docs.py` and `Tools/documentation-validation/verify_index.py` plus GitHub Actions workflows (`.github/workflows/docs-ci.yml` and `pages.yml`).

## 2026-10-06 — Consultant Program, Osmosis, SPC 2026, and EUR Sweeps (`067`–`069`)

- Captured consultant-level submission rules (IS Ladder, prod-correlation `<= 0.7`, ATOM single-dataset criteria, Power Pool, Genius pyramids, Osmosis allocation rules, and SPC 2026 prompt competition).
- Parsed 4,223 EUR multi-simulation sweep blocks (`067`–`069`) using `brain_sweep_parser.py` and added `validate_spc_isin.py`.

## 2026-07-24 to 2026-10-05 — Initial USA Alpha Research Ledger (`001`–`066`)

- Conducted 66 controlled hand-built simulations in `USA / TOP3000 / Delay 1`, producing 3 passing/submitted Alphas (`026`, `027`, `053`), 4 high-Sharpe self-correlation rejections (`029`, `031`, `033`, `046`), and 2 event-field validation error records (`042`, `043`).
