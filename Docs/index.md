# WorldQuant BRAIN Alpha Research — Consultant Curriculum & Knowledge Base

A structured, evidence-linked curriculum for **WorldQuant BRAIN** quantitative researchers and consultants. Start at Module 01 if you are opening the simulator for the first time, or jump directly to intermediate and advanced modules on consultant submission gates, Power Pool, Genius pyramids, Osmosis allocations, the BRAIN API, and empirical lessons from **71 recorded experiments** and **13,319 multi-simulation sweep blocks**.

## Dual-Track Consultant Portal: Choose Your Path

Whether you are opening the WorldQuant BRAIN simulator for the first time or you are an active consultant looking for the latest multi-simulation sweep analytics and candidate shortlists, start with your track below:

| Consultant Track | Recommended Entry Points | What You Will Find |
|---|---|---|
| **New Consultant Track (Onboarding & Foundations)** | 1. [01 — Getting Started](01-getting-started/index.md)<br>2. [02 — Financial & Quant Foundations](02-financial-and-quantitative-foundations/index.md)<br>3. [03 — BRAIN Simulator Settings](03-worldquant-brain-fundamentals/index.md)<br>4. [04 — Data Explorer & Datasets](04-data-explorer-and-datasets/index.md)<br>5. [05 — Fast Expression Language](05-fast-expression-language/index.md)<br>6. [06 — Building Your First Alpha](06-alpha-research-and-construction/index.md)<br>7. [07 & 08 — Evaluation & Submission Checks](07-simulation-and-evaluation/index.md) | Step-by-step progressive curriculum explaining long/short weights, neutralization, decay, truncation, matrix vs vector fields, operator syntax, and how to diagnose and repair your first Alpha to pass consultant submission checks. |
| **Expert Consultant Track (Live Simulation Analytics, Lessons & Advanced Topics)** | 1. [**18 — Live Simulation Results & Sweep Hub**](18-simulation-results-and-sweep-analytics/index.md)<br>2. [**USA 3,550-Block Factor Screening (`070`)**](18-simulation-results-and-sweep-analytics/usa-3550-sweep-analysis.md)<br>3. [**Complete 71-Experiment & Sweep Ledger**](18-simulation-results-and-sweep-analytics/master-experiment-ledger.md)<br>4. [**17 — Case Studies & 26 Empirical Lessons**](17-case-studies-and-lessons-learned/index.md)<br>5. [09–11 — Power Pool, Genius Pyramids & Osmosis](09-power-pool-and-thematic-competitions/index.md)<br>6. [12–13 — Double/Risk Neutralization & Multi-Region Alphas](12-advanced-alpha-research/index.md)<br>7. [14–16 — BRAIN API Automation & Alpha Harness](14-brain-api-and-automation/index.md) | Continuously updated empirical database covering **71 experiments** and **13,319 multi-simulation sweep blocks** (`USA, EUR, KOR, AMR, GLB`), submitted Alpha architectures (`026, 027, 053`), Group A/B/C candidate repair queues, and reusable lessons `L-001`–`L-026`. |

## Repository Navigation

| Knowledge Base Pillar | Location | Purpose |
|---|---|---|
| **Curriculum & Reference (`Docs/`)** | [`index.md`](index.md) | 17-module progressive curriculum from beginner foundations to consultant-level engineering |
| **Tools & Automation (`Tools/`)** | [`../Tools/README.md`](../Tools/README.md) | Sweep parsers, index reconcilers, Markdown/ISIN validators, and ACE API utilities |
| **External Literature (`Books/`)** | [`../Books/README.md`](../Books/README.md) | Academic papers (Kakushadze 101 Alphas), Qlib Alpha158, and official BRAIN documentation archive |
| **Empirical Evidence (`Analysis and Simulation Reports/`)** | [`../Analysis and Simulation Reports/index.md`](../Analysis%20and%20Simulation%20Reports/index.md) | All 71 experiment records, regional results (`USA, EUR, KOR, AMR, GLB`), and parsed sweep CSVs |

## Progressive Learning Roadmap (Beginner → Advanced)

### Part I — Beginner Foundations (Modules 01–06)

| Module | Topic | Key Skills & Concepts |
|---|---|---|
| **01** | [Getting Started with WorldQuant BRAIN](01-getting-started/index.md) | Platform overview, the 10-step onboarding workflow, WorldQuant Challenge vs Consultant track, and running your first simulation |
| **02** | [Financial and Quantitative Foundations](02-financial-and-quantitative-foundations/index.md) | Long/short equity portfolios, market/industry neutrality, mean reversion vs momentum, fundamental ratios vs raw levels, and trading costs |
| **03** | [WorldQuant BRAIN Fundamentals](03-worldquant-brain-fundamentals/index.md) | Simulation Settings panel (`Region`, `Universe`, `Delay`, `Decay`, `Truncation`, `Neutralization`, `Pasteurization`, `NaN Handling`, `Test Period`), PnL horizon, and Visualization Tool |
| **04** | [Data Explorer and Datasets](04-data-explorer-and-datasets/index.md) | Dataset hierarchy, Matrix vs Vector vs Group fields, coverage diagnostics, field selection priority, and [Dataset & Field Catalog](04-data-explorer-and-datasets/dataset-catalog-and-field-notes.md) |
| **05** | [Fast Expression Language](05-fast-expression-language/index.md) | Syntax rules, statements, comments, type conversions, and the complete [Categorized Operator Reference](05-fast-expression-language/operator-reference.md) |
| **06** | [Alpha Research and Construction](06-alpha-research-and-construction/index.md) | Hypothesis-first workflow, cross-sectional vs time-series normalization, neutralizing by dataset type, and single-change iteration |

### Part II — Intermediate Evaluation, Submission & Competitions (Modules 07–11)

| Module | Topic | Key Skills & Concepts |
|---|---|---|
| **07** | [Simulation and Evaluation](07-simulation-and-evaluation/index.md) | Interpreting `Sharpe`, `Fitness`, `Turnover`, `Returns`, `Drawdown`, `Margin`, `Train Sharpe` vs `Sharpe`, investability-constrained metrics, and bottleneck repair |
| **08** | [Submission and Eligibility](08-submission-and-eligibility/index.md) | User-level vs consultant-level checks, IS Ladder test (window thresholds & `<30%` turnover `0.85x` relief), Self-Correlation vs Prod-Correlation (`<= 0.7`), Sub-Universe Sharpe formula, and ATOM (Single Dataset Alpha) rules |
| **09** | [Power Pool and Thematic Competitions](09-power-pool-and-thematic-competitions/index.md) | Power Pool eligibility (`Sharpe >= 1.0`, `<= 8` operators, `<= 3` fields, `< 0.5` correlation, `>= 100`-char description), quotas, All Region Competition, and SPC 2026 Prompt Competition |
| **10** | [Pyramids and Genius Program](10-pyramids-and-genius-program/index.md) | Gold, Expert, Master, and Grand Master tiers, slot allocations, Pyramid definition (`Region x Delay x Category`, `>= 3` Alphas), Dynamic Pyramid Multipliers, Theme Multiplier stacking, and tie-breakers |
| **11** | [Osmosis and Compensation](11-osmosis-and-compensation/index.md) | Osmosis personal Alpha combo, `>= 3` scopes x `100,000` points across `>= 10` Alphas, Sunday lock schedule, Daily Osmosis Rank, Combined Osmosis Performance, and base/quarterly fee structure |

### Part III — Advanced Research, Automation & Case Studies (Modules 12–17)

| Module | Topic | Key Skills & Concepts |
|---|---|---|
| **12** | [Advanced Alpha Research](12-advanced-alpha-research/index.md) | Double neutralization (`group_cartesian_product`), factor/risk neutralization (`SLOW`, `FAST`, `CROWDING`, `STATISTICAL`, `RAM`), `D0` & High-Turnover Alphas, SuperAlphas (Selection + Combo + `generate_stats()`), and Python Alphas (`@alpha`) |
| **13** | [Region-Agnostic and Cluster Alphas](13-region-agnostic-and-cluster-alphas/index.md) | Regional (`USA, EUR, ASI, CHN, IND, JPN, HKG/KOR/TWN, AMR`) vs Global (`GLB / ALL`) rules, `TOPDIV3000` & `TOPCS1600`, `RA Parent` Alphas, and Cluster Alpha research notes |
| **14** | [BRAIN API and Automation](14-brain-api-and-automation/index.md) | `/authentication` & Persona biometrics, `/simulations` polling, rate-limit headers (`X-Ratelimit-*`), Multi-Simulation batching (`8 x 10`), SHA-256 simulation hash caching, and ACE library workflow |
| **15** | [Alpha Harness](15-alpha-harness/index.md) | Local research harness architecture: sweep parsing (`brain_sweep_parser.py`), index reconciliation (`verify_index.py`), doc hygiene (`check_docs.py`), SPC validation (`validate_spc_isin.py`), and Conda setup |
| **16** | [Quantitative Research Methodology](16-quantitative-research-methodology/index.md) | Consultant Dos & Don'ts, academic paper translation workflow, parameter discipline (`5, 20, 60, 120, 252`), multi-universe validation, and duplicate-avoidance rules |
| **17** | [Case Studies and Lessons Learned](17-case-studies-and-lessons-learned/index.md) | Empirical post-mortems of 71 experiments and 13,319 sweep blocks: USA `ebitda/ev` + `sales_growth` progression, the self-correlation wall, sentiment/event pitfalls, and EUR/KOR `anl69` slow-analyst findings |
| **18** | [Live Simulation Results & Sweep Analytics Hub](18-simulation-results-and-sweep-analytics/index.md) | Continuously updated simulation dashboard: [USA 3,550-Block Factor Screening](18-simulation-results-and-sweep-analytics/usa-3550-sweep-analysis.md), [Full 71-Experiment Ledger](18-simulation-results-and-sweep-analytics/master-experiment-ledger.md), regional leaderboards, and Group A/B/C candidate shortlists |

### Part IV — Reference Hub (`Docs/reference/`)

- [Reference Overview](reference/index.md)
- [Fast Expression Cheat Sheet](reference/fast-expression-cheatsheet.md)
- [Troubleshooting & Error Catalog](reference/troubleshooting-and-errors.md)
- [Command & Workflow Playbook](reference/command-and-workflow-playbook.md)
- [Sources & Evidence Policy](reference/sources-and-policy.md)
- [Contributing Guide](reference/contributing.md)
- [Changelog](reference/changelog.md)

## Quick Diagnostic Routing Table

| If You Need To... | Go Directly To |
|---|---|
| Understand what an Alpha weight vector and booksize mean | [01 — Getting Started](01-getting-started/index.md) · [02 — Financial Foundations](02-financial-and-quantitative-foundations/index.md) |
| Choose between `Subindustry`, `Industry`, `Market`, or `Country` neutralization | [03 — BRAIN Fundamentals](03-worldquant-brain-fundamentals/index.md) · [12 — Advanced Alpha Research](12-advanced-alpha-research/index.md) |
| Fix an `Event input` error on `ts_delta` or handle Vector fields | [04 — Data Explorer & Datasets](04-data-explorer-and-datasets/index.md) · [05 — Fast Expression](05-fast-expression-language/index.md) |
| Raise `Fitness` when `Sharpe` is already above `1.25` | [07 — Simulation & Evaluation](07-simulation-and-evaluation/index.md) |
| Understand why `LOW_2Y_SHARPE` or `IS_LADDER_SHARPE` failed | [08 — Submission & Eligibility](08-submission-and-eligibility/index.md) |
| Check whether an Alpha expression was already tested | [Master Experiment Index](../Analysis%20and%20Simulation%20Reports/index.md) · [Status Ledger](../Analysis%20and%20Simulation%20Reports/alpha-research/status-and-duplicate-ledger.md) |
