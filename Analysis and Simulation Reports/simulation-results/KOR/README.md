# KOR Simulation Results (`071 d1` — 789 Blocks)

Summary of Korea (`KOR / TOP600 / Delay 1 / Decay 5`) simulation results captured in Page `d1` of [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md).

## Key Metrics and Artifacts

- **Canonical Bundle Record:** [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md)
- **Full Generated Report:** [`../../sweeps-and-experiments/20261009_115500_d1_kor_top600.md`](../../sweeps-and-experiments/20261009_115500_d1_kor_top600.md)
- **Machine-Readable Data:** [`../../sweeps-and-experiments/20261009_115500_d1_kor_top600.csv`](../../sweeps-and-experiments/20261009_115500_d1_kor_top600.csv) · [`../../sweeps-and-experiments/20261009_115500_d1_kor_top600.json`](../../sweeps-and-experiments/20261009_115500_d1_kor_top600.json)
- **Settings:** Region `KOR`, Universe `TOP600`, Delay `1`, Decay `5`, Truncation `0.08`, Neutralization `INDUSTRY, MARKET, SUBINDUSTRY` (sectioned).
- **Headline Findings:**
  - **789 blocks** evaluated; **0 PASS**, **0 PENDING**, **2 blocks** cleared both Sharpe >= 1.25 and Fitness >= 1.0.
  - Top expression: `ts_scale(ts_backfill(anl69_ebitda_best_eeps_cur_yr, 21), 63)` with Sharpe `2.36`, Fitness `1.67`, Turnover `6.60%` (failed `LOW_2Y_SHARPE` and `LOW_SUB_UNIVERSE_SHARPE`).
  - Confirming the EUR finding, slow analyst consensus levels (`anl69_*`) under `ts_scale(..., 63)` transfer across regions at low turnover (`< 10%`).
