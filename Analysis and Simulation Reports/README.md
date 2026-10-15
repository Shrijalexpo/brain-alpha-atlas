# Analysis and Simulation Reports

Centralized single source of truth for all WorldQuant BRAIN Alpha experiments, simulation exports, multi-simulation sweeps, performance analyses, and research ledgers in this repository.

## Directory Structure

```text
Analysis and Simulation Reports/
├── README.md                                  Overview, provenance rules, and navigation
├── index.md                                   Master Experiment & Sweep Index (71 records, verified by verify_index.py)
├── simulation-results/                        Individual experiment records organized by region
│   ├── README.md                              Regional index and summary statistics
│   ├── USA/                                   Simulations 001–066 (hand-built) + 070 (3,550-block sweep)
│   ├── EUR/                                   Simulations 067–069 (4,223 sweep blocks across 5 universes)
│   ├── KOR/                                   KOR TOP600 sweep analysis (789 blocks from Bundle 071 d1)
│   ├── AMR/                                   AMR TOP600 sweep analysis (3,250 blocks from Bundle 071 d2)
│   ├── GLB/                                   ALL/GLB LARGE sweep analysis (192 blocks from Bundle 071 d4 & d6)
│   └── multi-region/                          Simulation 071 (5,546-block 6-page multi-region bundle)
├── alpha-research/                            Cumulative research ledgers, duplicate checks, and templates
│   ├── README.md                              Guide to research ledgers and workflow rules
│   ├── status-and-duplicate-ledger.md         Quick status & duplicate-avoidance table (001–071)
│   ├── past-simulations-ledger.md             Detailed chronological narrative of past simulations
│   ├── lessons-from-simulations.md            Durable empirical findings from completed simulations
│   ├── field-research-notebook.md             Field-by-field diagnostic notes
│   └── simulation-template.md                 Standard template for recording new simulations
├── sweeps-and-experiments/                    Parsed CSV, JSON, and Markdown reports for all bulk sweeps
│   ├── README.md                              Sweep dataset schema, Fx legend rules, and file map
│   ├── SUMMARY.md                             EUR 3-dump cross-sweep comparison (4,223 blocks)
│   ├── 20261004_171500.{csv,json,md}          Sim 067: EUR TOP2500 / COUNTRY (314 blocks)
│   ├── 20261005_123752.{csv,json,md}          Sim 068: EUR 5-universe Decay 5 (2,100 blocks)
│   ├── 20261006_100742.{csv,json,md}          Sim 069: EUR 5-universe Decay 0 (1,809 blocks)
│   ├── 20261008_071542_*.{csv,json,md}        Sim 070: USA 6-universe + TOP3000 (3,550 blocks)
│   ├── 20261009_115500_*.{csv,json,md}        Sim 071: KOR, AMR, EUR, ALL, USA (5,546 blocks)
│   ├── all_results.csv                        Combined EUR sweep blocks (4,223 rows)
│   └── superseded/                            Historical record of corrected/superseded sweep parses
├── aggregate-analytics/                       Cross-experiment quantitative summaries and master CSV catalog
│   ├── README.md                              Aggregate statistics across 71 records and 13,319 sweep blocks
│   └── master_experiments_catalog.csv         Machine-readable catalog of all 71 experiment records
└── source-data/                               Raw pasted platform multi-simulation exports for reproducibility
    ├── README.md                              Provenance, MD5/SHA256 checksums, and regeneration commands
    ├── 20261008_071542.txt                    Raw 2-page USA multi-simulation export (3,550 blocks)
    └── 20261009_115500.txt                    Raw 6-page multi-region export (5,546 blocks)
```

## Research Integrity and Provenance Rules

1. **Single Authoritative Record:** Every experiment has one canonical Markdown record in [`simulation-results/`](simulation-results/README.md) and one row in [`index.md`](index.md) and [`aggregate-analytics/master_experiments_catalog.csv`](aggregate-analytics/master_experiments_catalog.csv).
2. **Automated Reconciliation:** Run `python3 Tools/documentation-validation/verify_index.py` after any update to confirm that [`index.md`](index.md) matches every record and sweep CSV.
3. **Out-of-Sample vs Training Metrics:** Always record the out-of-sample `Sharpe` column separately from `Train Sharpe`. Never substitute training metrics for out-of-sample evaluation.
4. **Per-Page Legend Isolation:** Failed-check codes (`F1`, `F2`, ...) are local to each pasted results page. Always use the resolved check names (`LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE`, `IS_LADDER_SHARPE`, etc.) stored in [`sweeps-and-experiments/`](sweeps-and-experiments/README.md).
5. **No Fabricated Values:** Missing or uncaptured settings/metrics are explicitly recorded as `unknown` or `—`.
