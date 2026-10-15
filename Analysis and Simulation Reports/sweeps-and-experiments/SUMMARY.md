# Cross-dump summary

| Dump | Blocks | Region | Decay | Universes | S&P ≥1.25 | Fitness ≥1.0 | PASS | Top Sharpe |
|---|---:|---|---:|---|---:|---:|---:|---:|
| `20261004_171500` | 314 | EUR | 5 | TOP2500 | 2 | 2 | 0 | 1.97 |
| `20261005_123752` | 2100 | EUR | 5 | TOP1200, TOP2500, TOP400, TOP800, TOPCS1600 | 7 | 7 | 0 | 11.18 |
| `20261006_100742` | 1809 | EUR | 0 | TOP1200, TOP2500, TOP400, TOP800, TOPCS1600 | 8 | 8 | 0 | 2.14 |

## Expressions repeated across dumps

9 expressions appear in more than one dump.

| Expression | Occurrences |
|---|---|
| `rank(ts_backfill(anl10_ebtfy2_pred_surps_v2, 21))` | 20261004_171500#42, 20261005_123752#63 |
| `scale(ts_backfill(anl10_cpxfy1_smart_ests_v1, 21))` | 20261004_171500#116, 20261006_100742#53 |
| `scale(ts_backfill(anl10_ndtfy2_smart_ests_v0, 21))` | 20261004_171500#269, 20261006_100742#845 |
| `rank(ts_backfill(pv37_cap_12, 21))` | 20261005_123752#310, 20261006_100742#200 |
| `normalize(ts_backfill(pv37_snapshot1_volume121500, 21))` | 20261005_123752#357, 20261006_100742#1274 |
| `group_count(ts_backfill(pv37_snapshot1_volume135500, 21), subindustry)` | 20261005_123752#564, 20261006_100742#881 |
| `winsorize(ts_backfill(pv20_sal_indicator_3_feature9_1254, 21))` | 20261005_123752#719, 20261006_100742#79 |
| `winsorize(ts_backfill(pv20_nav_best_eeps_cur_yr_1033, 21))` | 20261005_123752#770, 20261006_100742#1020 |
| `rank(ts_backfill(pv37_snapshot1_volume122500, 21))` | 20261005_123752#1045, 20261006_100742#240 |
