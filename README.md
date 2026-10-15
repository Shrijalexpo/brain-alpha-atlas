# BRAIN Alpha Atlas

A structured, evidence-linked knowledge base and research repository for **WorldQuant BRAIN Alpha research**: a 17-module progressive consultant curriculum, dependency-free Python parsing and validation utilities, an external quantitative literature library, and the complete empirical record of **71 Alpha experiments** and **13,319 multi-simulation sweep blocks**.

**Start the Curriculum → [`Docs/index.md`](Docs/index.md)**

## Four-Pillar Repository Architecture

```text
brain-alpha-atlas/
├── Docs/                              17-module beginner-to-advanced consultant curriculum + reference hub
├── Tools/                             Python sweep parsers, index reconcilers, doc/ISIN validators & ACE API
├── Books/                             Academic papers, formula libraries (Alpha101/158) & official captures
└── Analysis and Simulation Reports/   71 experiment records, regional results, sweep CSVs & raw source dumps
```

| Directory | Entry Point | What Lives Here |
|---|---|---|
| **[`Docs/`](Docs/index.md)** | [`Docs/index.md`](Docs/index.md) | Progressive learning path from [01 — Getting Started](Docs/01-getting-started/index.md) through [08 — Submission & Eligibility](Docs/08-submission-and-eligibility/index.md), [09 — Power Pool](Docs/09-power-pool-and-thematic-competitions/index.md), [10 — Pyramids & Genius](Docs/10-pyramids-and-genius-program/index.md), [11 — Osmosis](Docs/11-osmosis-and-compensation/index.md), [14 — BRAIN API](Docs/14-brain-api-and-automation/index.md), [15 — Alpha Harness](Docs/15-alpha-harness/index.md), and [17 — Case Studies](Docs/17-case-studies-and-lessons-learned/index.md) |
| **[`Tools/`](Tools/README.md)** | [`Tools/README.md`](Tools/README.md) | [`brain_sweep_parser.py`](Tools/simulation-processing/brain_sweep_parser.py), [`verify_index.py`](Tools/documentation-validation/verify_index.py), [`check_docs.py`](Tools/documentation-validation/check_docs.py), [`validate_spc_isin.py`](Tools/alpha-analysis/validate_spc_isin.py), and the local ACE API library (`Tools/api-and-automation/ace-api/`) |
| **[`Books/`](Books/README.md)** | [`Books/README.md`](Books/README.md) | Kakushadze (2016) *101 Formulaic Alphas*, Qlib `Alpha158`, WorldQuant India fee methodology guide, All Region Competition 2026 rules, and the 78-article official BRAIN Learn archive (excluded from public push via `.gitignore`) |
| **[`Analysis and Simulation Reports/`](Analysis%20and%20Simulation%20Reports/README.md)** | [`Analysis and Simulation Reports/index.md`](Analysis%20and%20Simulation%20Reports/index.md) | Regional simulation records (`USA`, `EUR`, `KOR`, `AMR`, `GLB`, `multi-region`), parsed sweep CSV/JSON/MD reports (`sweeps-and-experiments/`), cumulative ledgers (`alpha-research/`), 71-row catalog (`aggregate-analytics/master_experiments_catalog.csv`), and raw exports (`source-data/`) |

## Curriculum Modules (`Docs/`)

| Level | Module | Focus |
|---|---|---|
| **Beginner** | [01 — Getting Started](Docs/01-getting-started/index.md) | Platform overview, 10-step onboarding, Challenge vs Consultant tracks |
| **Beginner** | [02 — Financial & Quant Foundations](Docs/02-financial-and-quantitative-foundations/index.md) | Long/short weights, group neutrality, factor families, why raw levels fail |
| **Beginner** | [03 — WorldQuant BRAIN Fundamentals](Docs/03-worldquant-brain-fundamentals/index.md) | Simulation settings (`Delay`, `Decay`, `Truncation`, `Neutralization`, `Test Period`), Visualization Tool |
| **Beginner** | [04 — Data Explorer & Datasets](Docs/04-data-explorer-and-datasets/index.md) | Matrix vs Vector vs Group fields, coverage probes, [Dataset & Field Catalog](Docs/04-data-explorer-and-datasets/dataset-catalog-and-field-notes.md) |
| **Beginner** | [05 — Fast Expression Language](Docs/05-fast-expression-language/index.md) | Syntax rules, normalization idioms, [Categorized Operator Reference](Docs/05-fast-expression-language/operator-reference.md) |
| **Beginner** | [06 — Alpha Research & Construction](Docs/06-alpha-research-and-construction/index.md) | Hypothesis-first loop, 1-minute explainability rule, single-mechanism iteration |
| **Intermediate** | [07 — Simulation & Evaluation](Docs/07-simulation-and-evaluation/index.md) | `Sharpe`, `Fitness` formula, `Turnover`, `Returns`, `Drawdown`, `Margin`, `Train Sharpe` vs `Sharpe` |
| **Intermediate** | [08 — Submission & Eligibility](Docs/08-submission-and-eligibility/index.md) | User vs Consultant checks, IS Ladder (`<30%` turnover `0.85x` relief), Prod-Correlation (`<= 0.7`), ATOM rules |
| **Intermediate** | [09 — Power Pool & Competitions](Docs/09-power-pool-and-thematic-competitions/index.md) | Power Pool rules (`<= 8` ops, `<= 3` fields, `< 0.5` corr), quotas, All Region & SPC 2026 competitions |
| **Intermediate** | [10 — Pyramids & Genius Program](Docs/10-pyramids-and-genius-program/index.md) | Gold/Expert/Master/Grand Master tiers, 3-Alpha Pyramids, Dynamic & Theme Multipliers, tie-breakers |
| **Intermediate** | [11 — Osmosis & Compensation](Docs/11-osmosis-and-compensation/index.md) | Osmosis `>= 3` scopes x `100,000` points across `>= 10` Alphas, Sunday lock, turnover bucketing |
| **Advanced** | [12 — Advanced Alpha Research](Docs/12-advanced-alpha-research/index.md) | Double neutralization, risk neutralization (`SLOW/FAST/CROWDING/STATISTICAL/RAM`), D0, SuperAlphas, Python Alphas |
| **Advanced** | [13 — Region-Agnostic & Cluster Alphas](Docs/13-region-agnostic-and-cluster-alphas/index.md) | Regional specifications (`USA, EUR, GLB, ASI, CHN, IND, JPN, HKG/KOR/TWN, AMR`), `RA Parent` & Cluster notes |
| **Advanced** | [14 — BRAIN API & Automation](Docs/14-brain-api-and-automation/index.md) | `/authentication`, Persona biometrics, `/simulations` polling, rate limits, SHA-256 hash caching, ACE API |
| **Advanced** | [15 — Alpha Harness](Docs/15-alpha-harness/index.md) | Local parsing, index reconciliation, doc hygiene, and reproducible research architecture |
| **Advanced** | [16 — Quant Research Methodology](Docs/16-quantitative-research-methodology/index.md) | Consultant Dos & Don'ts, paper translation workflow, parameter discipline, duplicate avoidance |
| **Advanced** | [17 — Case Studies & Lessons Learned](Docs/17-case-studies-and-lessons-learned/index.md) | Post-mortems of 71 experiments & 13,319 sweep blocks across 5 regions |

## Empirical Research Record in Numbers

| Metric | Value |
|---|---:|
| Canonical experiment records (`001`–`071`) | `71` |
| Hand-built USA Alphas clearing user checks (`026, 027, 053`) | `3` |
| Hand-built USA Alphas submitted (`027, 053`) | `2` |
| High-Sharpe Alphas rejected for self-correlation (`029, 031, 033, 046`) | `4` |
| Multi-simulation sweep blocks parsed across 5 regions (`067`–`071`) | `13,319` |
| Submittable Alphas produced directly by unedited sweep blocks | `0` |

## Verification & Local Build Commands

```bash
# Run all tool self-tests
python3 Tools/simulation-processing/brain_sweep_parser.py --selftest
python3 Tools/alpha-analysis/validate_spc_isin.py --selftest
python3 Tools/documentation-validation/check_docs.py --selftest
python3 Tools/documentation-validation/verify_index.py --selftest

# Validate Markdown links/hygiene and reconcile the 71-experiment index
python3 Tools/documentation-validation/check_docs.py Docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS
python3 Tools/documentation-validation/verify_index.py

# Build the MkDocs site in strict mode and scan rendered HTML
.venv-docs/bin/mkdocs build --strict
python3 Tools/documentation-validation/check_docs.py --text-scan site
```

## Licensing and Notice

Code (`Tools/**/*.py`, `.github/workflows/`, `mkdocs.yml`) is licensed under **MIT** ([`LICENSE`](LICENSE)). Original documentation and research prose (`Docs/`, `README.md`, `Analysis and Simulation Reports/`) are licensed under **CC BY 4.0** ([`LICENSE-DOCS`](LICENSE-DOCS)). [`NOTICE`](NOTICE) specifies what neither grant covers (raw platform exports, WorldQuant BRAIN platform terminology, and cited third-party works). This repository is an independent research knowledge base and is not affiliated with or endorsed by WorldQuant.
