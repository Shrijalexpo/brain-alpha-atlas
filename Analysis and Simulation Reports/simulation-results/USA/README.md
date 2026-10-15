# USA Simulation Results (`001`–`066`, `070`, and `071 d5`)

This directory contains all 66 hand-built USA Alpha experiments (`001`–`066`) and the USA multi-universe analyst-growth sweep (`070`), plus links to the USA implied-volatility decay sweep (`071 d5`).

## Outcome Summary for USA

- **Cleared User-Level Checks (3):**
  - [`026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md`](026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md) — Sharpe `1.61`, Fitness `1.02`, Turnover `25.25%` (`PASSED_SUBMITTABLE`)
  - [`027_submitted_cashflow_quality_improvement_reversal.md`](027_submitted_cashflow_quality_improvement_reversal.md) — Sharpe `1.39`, Turnover `21.31%` (`PASSED_SUBMITTED`)
  - [`053_submitted_ebitda_ev_mean_reversion.md`](053_submitted_ebitda_ev_mean_reversion.md) — Sharpe `1.46`, Fitness `1.05` (`PASSED_SUBMITTED`)
- **Failed on Self-Correlation After Passing Metrics (4):**
  - [`029_operating_income_roa_reversal_selfcorr.md`](029_operating_income_roa_reversal_selfcorr.md) (`Sharpe 1.76, Fitness 1.21, self-corr 0.8817`)
  - [`031_cashflow_roa_reversal_selfcorr.md`](031_cashflow_roa_reversal_selfcorr.md) (`Sharpe 1.71, Fitness 1.13, self-corr 0.933`)
  - [`033_operating_income_ebitda_ev_delta_reversal_selfcorr.md`](033_operating_income_ebitda_ev_delta_reversal_selfcorr.md)
  - [`046_dividend_volume_returns_selfcorr.md`](046_dividend_volume_returns_selfcorr.md) (`Sharpe 1.86, Fitness 1.07, self-corr 0.935`)
- **Syntax / Event-Type Validation Errors (2):**
  - [`042_estimate_eps_delta_error.md`](042_estimate_eps_delta_error.md) and [`043_estimate_sales_delta_error.md`](043_estimate_sales_delta_error.md)
- **Bulk Sweeps (2):**
  - [`070_usa_top3000_industry_analyst_growth_sweep.md`](070_usa_top3000_industry_analyst_growth_sweep.md) — 3,550 blocks across 2 pages (`TOP200`, `TOP500`, `TOP1000`, `TOP2000`, `TOP3000`, `TOPSP500`); parsed data in [`../../sweeps-and-experiments/20261008_071542_SUMMARY.md`](../../sweeps-and-experiments/20261008_071542_SUMMARY.md).
  - [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md) (Dump `d5`) — 174 blocks on `USA / TOP3000` testing `option6` implied volatility across Decay `0..16`; parsed report in [`../../sweeps-and-experiments/20261009_115500_d5_usa_top3000.md`](../../sweeps-and-experiments/20261009_115500_d5_usa_top3000.md).
