# GLB / ALL Simulation Results (`071 d4 & d6` — 192 Blocks)

Summary of Global / All-Region (`ALL / LARGE / Delay 1 / Decay 5`) simulation results captured in Pages `d4` and `d6` of [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md).

## Key Metrics and Artifacts

- **Canonical Bundle Record:** [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md)
- **Full Generated Reports:**
  - Dump `d4` (113 blocks): [`../../sweeps-and-experiments/20261009_115500_d4_all_large.md`](../../sweeps-and-experiments/20261009_115500_d4_all_large.md) · [`CSV`](../../sweeps-and-experiments/20261009_115500_d4_all_large.csv)
  - Dump `d6` (79 blocks): [`../../sweeps-and-experiments/20261009_115500_d6_all_large.md`](../../sweeps-and-experiments/20261009_115500_d6_all_large.md) · [`CSV`](../../sweeps-and-experiments/20261009_115500_d6_all_large.csv)
- **Settings:** Region `ALL`, Universe `LARGE`, Delay `1`, Decay `5`, Truncation `0.08`, Neutralization `INDUSTRY`.
- **Headline Findings:**
  - **192 total blocks** (`113` in `d4`, `79` in `d6`); **0 PASS**, **0 PENDING**.
  - Top Sharpe in `d4` reached `1.42` (Fitness `0.72`); top Sharpe in `d6` reached `0.72`.
  - Global/ALL scopes require double neutralization (`country` + `industry`) and must clear sub-geography Sharpe cutoffs (`AMER >= 1`, `APAC >= 1`, `EMEA >= 1` for `GLB`).
