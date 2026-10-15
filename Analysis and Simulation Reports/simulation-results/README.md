# Simulation Results by Region

All 71 canonical experiment records (`001`–`071`) and regional sweep breakdowns organized by market scope.

## Regional Coverage Summary

| Region Directory | Hand-Built Alpha Records | Bulk Sweep Records | Total Sweep Blocks | Best Recorded Sharpe / Fitness | Primary Bottleneck Observed |
|---|---:|---:|---:|---|---|
| [`USA/`](USA/) | 66 (`001`–`066`) | 1 (`070` + `071 d5`) | 3,724 (3,550 in `070` + 174 in `071 d5`) | Hand-built: `1.86 / 1.07` (`046`, failed self-corr); Submitted: `1.61 / 1.02` (`026`); Sweep (`071 d5` IV): `2.61 / 1.88` | Self-correlation (`029, 031, 033, 046`), `CONCENTRATED_WEIGHT`, and `LOW_SUB_UNIVERSE_SHARPE` |
| [`EUR/`](EUR/) | 0 | 3 (`067`–`069` + `071 d3`) | 5,364 (4,223 in `067`–`069` + 1,141 in `071 d3`) | `2.63 / 1.19` (`071 d3`); `anl69` slow analyst: `1.97 / 1.58` at 5.78% turnover (`067`) | `LOW_2Y_SHARPE` (92–98% of blocks) and `LOW_SUB_UNIVERSE_SHARPE` (46–49%) |
| [`KOR/`](KOR/) | 0 | 1 (`071 d1`) | 789 | `2.36 / 1.67` on `anl69_ebitda_best_eeps_cur_yr` (Turnover 6.6%) | `LOW_2Y_SHARPE` and `LOW_SUB_UNIVERSE_SHARPE` |
| [`AMR/`](AMR/) | 0 | 1 (`071 d2`) | 3,250 | `1.69 / 1.38` on `anl4` / `fnd6` (19 blocks cleared Sharpe >= 1.25 & Fitness >= 1.0) | Higher regional Sharpe bar (`LOW_SHARPE` fires up to ~1.60) and 25 `PENDING` blocks |
| [`GLB/`](GLB/) | 0 | 1 (`071 d4 & d6`) | 192 (113 + 79 in `ALL / LARGE`) | `1.42 / 0.72` (`071 d4`) | `LOW_FITNESS` and `LOW_SUB_UNIVERSE_SHARPE` |
| [`multi-region/`](multi-region/) | 0 | 1 (`071`) | 5,546 across 6 pages | `2.63` (EUR), `2.61` (USA IV), `2.36` (KOR) | 0 PASS across 5,546 blocks (42 `PENDING`) |
