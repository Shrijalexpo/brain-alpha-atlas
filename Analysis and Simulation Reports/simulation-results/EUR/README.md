# EUR Simulation Results (`067`–`069` and `071 d3`)

This directory holds the canonical records for the European equity (`EUR`) multi-simulation sweeps across `TOP2500`, `TOPCS1600`, `TOP1200`, `TOP800`, and `TOP400`.

## Canonical EUR Records

| ID | Record | Universe(s) | Neutralization | Decay | Blocks | Best Legitimate Signal |
|---:|---|---|---|---|---:|---|
| `067` | [`067_eur_top2500_country_analyst_sweep.md`](067_eur_top2500_country_analyst_sweep.md) | `TOP2500` | `COUNTRY` | `5` | 314 | `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` — Sharpe `1.97`, Fitness `1.58`, Turnover `5.78%` |
| `068` | [`068_eur_multi_universe_decay5_sweep.md`](068_eur_multi_universe_decay5_sweep.md) | `TOP2500, TOPCS1600, TOP1200, TOP800, TOP400` | `MARKET, INDUSTRY, COUNTRY` | `5` | 2,100 | `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))` — Sharpe `2.51`, Fitness `1.16` |
| `069` | [`069_eur_multi_universe_decay0_sweep.md`](069_eur_multi_universe_decay0_sweep.md) | `TOP2500, TOPCS1600, TOP1200, TOP800, TOP400` | `INDUSTRY, MARKET, COUNTRY` | `0` | 1,809 | `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` (`TOPCS1600`) — Sharpe `1.82`, Fitness `1.41`, Turnover `15.20%` |
| `071 (d3)` | [`../multi-region/071_multi_region_bundle_20261009.md`](../multi-region/071_multi_region_bundle_20261009.md) | 5 EUR universes | `COUNTRY, INDUSTRY` | `5` | 1,141 | Sharpe `2.63`, Fitness `1.19` (7 blocks >= 1.25 Sharpe & >= 1.0 Fitness; 15 `PENDING`) |

## Underlying Sweep Reports and CSVs

- [`../../sweeps-and-experiments/SUMMARY.md`](../../sweeps-and-experiments/SUMMARY.md) — Cross-dump comparison of `067`, `068`, and `069` (4,223 blocks)
- [`../../sweeps-and-experiments/20261004_171500.md`](../../sweeps-and-experiments/20261004_171500.md) (`067`)
- [`../../sweeps-and-experiments/20261005_123752.md`](../../sweeps-and-experiments/20261005_123752.md) (`068`)
- [`../../sweeps-and-experiments/20261006_100742.md`](../../sweeps-and-experiments/20261006_100742.md) (`069`)
- [`../../sweeps-and-experiments/20261009_115500_d3_eur_5universes.md`](../../sweeps-and-experiments/20261009_115500_d3_eur_5universes.md) (`071 d3`)
