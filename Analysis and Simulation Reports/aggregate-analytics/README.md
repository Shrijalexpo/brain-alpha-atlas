# Aggregate Analytics and Master Experiment Catalog

Cross-experiment quantitative synthesis across all **71 recorded experiments** (`66` hand-built USA alphas + `5` bulk multi-simulation sweeps totaling **13,319 simulated blocks**).

## Machine-Readable Catalog

- [`master_experiments_catalog.csv`](master_experiments_catalog.csv) — Standardized 71-row CSV table containing `id`, `title`, `status`, `type`, `region`, `universe`, `delay`, `decay`, `neutralization`, `truncation`, `sharpe`, `fitness`, `turnover`, `returns`, `drawdown`, `margin`, `sub_universe_sharpe`, `self_correlation`, `primary_dataset_or_fields`, `simulation_date`, `expression`, and `canonical_path`.

## Aggregate Breakdown of the Research Record

### 1. Hand-Built Alpha Iterations (`001`–`066`, Region: `USA`)

| Status Category | Count | Share of 66 | Representative Records | Key Takeaway |
|---|---:|---:|---|---|
| `PASSED_SUBMITTED` | 2 | 3.0% | `027`, `053` | Value/quality + smoothed 5-day reversal cleared user-level checks and were submitted |
| `PASSED_SUBMITTABLE` | 1 | 1.5% | `026` | `ts_rank(ebitda/ev, 126) + ts_rank(sales_growth, 126) + ts_mean(-returns, 5)` |
| `FAILED_SELF_CORRELATION` | 4 | 6.1% | `029`, `031`, `033`, `046` | High Sharpe (`1.71–1.86`) and Fitness (`1.07–1.21`), rejected for `0.88–0.94` self-correlation |
| `ERROR` | 2 | 3.0% | `042`, `043` | Applying matrix `ts_delta` directly to event/vector estimate fields (`eps_estimate_value`, `sales_estimate_value`) |
| `FAILED` (Performance / Robustness) | 57 | 86.4% | `001`–`025`, `028`, `030`, `032`, `034`–`041`, `044`–`045`, `047`–`052`, `054`–`066` | Raw fundamental levels, unsmoothed daily reversals, high-turnover sentiment (`87%` turnover), or over-smoothed cashflow dispersion |

### 2. Bulk Multi-Simulation Sweeps (`067`–`071`, 13,319 Total Blocks)

| Sweep ID | Date | Region(s) & Scope | Pages | Total Blocks | Sharpe >= 1.25 & Fitness >= 1.0 | Checks PASS | PENDING | Binding Failure Modes |
|---:|---|---|---:|---:|---:|---:|---:|---|
| `067` | 2026-10-04 | `EUR / TOP2500 / COUNTRY` (Decay 5) | 1 | 314 | 2 | 0 | 0 | `LOW_2Y_SHARPE` (95.5%), `LOW_SUB_UNIVERSE_SHARPE` (48.7%) |
| `068` | 2026-10-05 | `EUR` 5 universes (Decay 5) | 1 | 2,100 | 7 | 0 | 0 | `LOW_2Y_SHARPE` (92.9%), `LOW_FITNESS` (92.0%), `IS_LADDER_SHARPE` (2) |
| `069` | 2026-10-06 | `EUR` 5 universes (Decay 0) | 1 | 1,809 | 8 | 0 | 0 | `LOW_2Y_SHARPE` (98.0%), `HIGH_TURNOVER` (9.3%) |
| `070` | 2026-10-08 | `USA` 6 universes + `TOP3000` (Decay 5) | 2 | 3,550 | 1 | 0 | 0 | `LOW_SHARPE`, `LOW_FITNESS`, `LOW_2Y_SHARPE`; `Train Sharpe` exceeded `Sharpe` in 2,448/2,500 page-1 rows |
| `071` | 2026-10-09 | `KOR`, `AMR`, `EUR`, `ALL`, `USA` | 6 | 5,546 | 35 (12 `PENDING`) | 0 | 42 | `LOW_FITNESS`, `LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE`, `CONCENTRATED_WEIGHT` |
| **Total** | | **5 Regions (`USA, EUR, KOR, AMR, ALL`)** | **11** | **13,319** | **53** | **0** | **42** | **Single-field transform sweeps map the surface but never auto-produce submittable alphas** |
