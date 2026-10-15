# AMR Simulation Results (`071 d2` — 3,250 Blocks)

Summary of Americas (`AMR / TOP600 / Delay 1 / Decay 5`) simulation results captured in Page `d2` of [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md).

## Key Metrics and Artifacts

- **Canonical Bundle Record:** [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md)
- **Full Generated Report:** [`../../sweeps-and-experiments/20261009_115500_d2_amr_top600.md`](../../sweeps-and-experiments/20261009_115500_d2_amr_top600.md)
- **Machine-Readable Data:** [`../../sweeps-and-experiments/20261009_115500_d2_amr_top600.csv`](../../sweeps-and-experiments/20261009_115500_d2_amr_top600.csv) · [`../../sweeps-and-experiments/20261009_115500_d2_amr_top600.json`](../../sweeps-and-experiments/20261009_115500_d2_amr_top600.json)
- **Settings:** Region `AMR`, Universe `TOP600`, Delay `1`, Decay `5`, Truncation `0.08`, Neutralization `SUBINDUSTRY, INDUSTRY, MARKET` (sectioned).
- **Headline Findings:**
  - **3,250 blocks** evaluated; **0 PASS**, **25 PENDING**, **19 blocks** cleared Sharpe >= 1.25 and Fitness >= 1.0 (top Sharpe `1.69`, Fitness `1.38`).
  - Blocks with Sharpe `1.40–1.60` in `AMR / TOP600` still triggered `LOW_SHARPE`, proving that the effective regional Sharpe threshold in `AMR` is materially higher than the generic `1.25` user-level orientation figure.
