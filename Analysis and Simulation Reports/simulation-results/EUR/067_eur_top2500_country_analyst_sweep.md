# Simulation 067 - EUR TOP2500 / COUNTRY Analyst Sweep (314 Results)

Status: FAILED

Type: bulk sweep record (314 result blocks on one BRAIN multi-simulation page).
Machine-readable data: `Analysis and Simulation Reports/sweeps-and-experiments/20261004_171500.csv` / `.json` / `.md`.
Full generated report with all 314 expression rows: `Analysis and Simulation Reports/sweeps-and-experiments/20261004_171500.md`.

## Sweep

Single page of EUR analyst-field transforms. Every expression has the same skeleton:
one analyst or grouping field wrapped in `ts_backfill(field, 21)`, then exactly one
outer transform drawn from `rank`, `zscore`, `normalize`, `scale`, `quantile`,
`winsorize`, `group_rank`, `group_zscore`, `group_scale`, `group_sum`, `group_count`,
`group_std_dev`, `group_neutralize`, `ts_rank`, `ts_zscore`, `ts_scale`, `ts_quantile`,
`ts_delta`, `ts_av_diff`, `ts_ir`, `ts_returns`, `ts_sum`, `ts_product`, `ts_kurtosis`,
`ts_arg_min`, `ts_arg_max`, `ts_max_diff`, `ts_std_dev`, `last_diff_value`, `ts_decay_linear`.

Representative top expression:

```text
ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)
```

## Settings

```text
Instrument Type: Equity (not shown in paste)
Region: EUR
Universe: TOP2500
Language: Fast Expression
Delay: 1
Decay: 5
Truncation: 0.08
Neutralization: COUNTRY
Pasteurization: ON
Unit Handling: not shown in paste
NaN Handling: ON
Test Period: not shown in paste
```

## Known result

```text
Blocks: 314
Checks PASS: 0
Sharpe >= 1.25: 4
Fitness >= 1.0: 2
Sharpe >= 1.25 AND Fitness >= 1.0: 2
Sharpe >= 2.0: 0
Turnover > 70%: 16
Turnover < 1%: 37
Best Sharpe: 1.97   Best Fitness: 1.58   Best Margin: 88.58 bps
```

Failed-check frequency (resolved through this dump's own legend):

```text
LOW_SHARPE             313 / 314   99.7%
LOW_FITNESS            312 / 314   99.4%
LOW_2Y_SHARPE          300 / 314   95.5%
LOW_SUB_UNIVERSE_SHARPE 148 / 314  47.1%
CONCENTRATED_WEIGHT     96 / 314   30.6%
LOW_TURNOVER            37 / 314   11.8%
HIGH_TURNOVER           16 / 314    5.1%
```

Top 10 by Sharpe (all failed at least one check):

| # | Sharpe | Train | Fitness | Turnover | Returns | Margin | Expression | Failed |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 1.97 | 2.09 | 1.58 | 5.78% | 8.03% | 27.78 | `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 2 | 1.37 | 1.55 | 1.02 | 12.70% | 7.02% | 11.06 | `normalize(ts_zscore(ts_backfill(anl10_ebtfy2_consensus, 21), 63))` | LOW_SHARPE; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 3 | 1.36 | 1.67 | 0.42 | 74.39% | 7.18% | 1.93 | `quantile(ts_zscore(ts_backfill(anl10_prefy2_smart_ests_v1_456, 21), 5))` | LOW_SHARPE; LOW_FITNESS; HIGH_TURNOVER; CONCENTRATED_WEIGHT; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 4 | 1.26 | 1.37 | 0.90 | 7.46% | 6.38% | 17.10 | `ts_zscore(ts_backfill(anl10_netfy1_smart_ests_v2_621, 21), 126)` | LOW_SHARPE; LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 5 | 1.23 | 1.37 | 0.37 | 68.86% | 6.38% | 1.85 | `zscore(ts_zscore(ts_backfill(anl10_prefy1_smart_ests_v0_462, 21), 5))` | LOW_SHARPE; LOW_FITNESS; CONCENTRATED_WEIGHT; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 6 | 1.18 | 1.29 | 0.63 | 15.83% | 4.50% | 5.68 | `ts_rank(ts_backfill(anl10_prefy1_consensus_451, 21), 21)` | LOW_SHARPE; LOW_FITNESS; LOW_2Y_SHARPE |
| 7 | 1.16 | 1.19 | 0.62 | 5.31% | 3.53% | 13.30 | `quantile(ts_backfill(anl10_ebify1_pred_surps_v0_12, 21))` | LOW_SHARPE; LOW_FITNESS; LOW_2Y_SHARPE |
| 8 | 1.12 | 1.18 | 0.43 | 16.09% | 2.36% | 2.93 | `ts_rank(ts_sum(ts_backfill(anl10_ebtfy1_pred_surps_v1, 21), 5), 21)` | LOW_SHARPE; LOW_FITNESS; LOW_2Y_SHARPE |
| 9 | 1.10 | 1.30 | 0.53 | 8.28% | 2.88% | 6.95 | `scale(ts_zscore(ts_backfill(anl10_netfy2_pred_surps_v1_635, 21), 252))` | LOW_SHARPE; LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 10 | 1.09 | 1.07 | 0.73 | 2.31% | 5.58% | 48.30 | `ts_scale(ts_backfill(anl10_nerfy1_consensus, 21), 252)` | LOW_SHARPE; LOW_FITNESS; LOW_2Y_SHARPE |

Field families in this sweep:

| Family | Blocks | Best Sharpe | Best Fitness |
|---|---:|---:|---:|
| `anl10` analyst | 263 | 1.37 | 1.02 |
| `anl69` analyst | 24 | 1.97 | 1.58 |
| `sector_` grouping | 9 | 0.42 | 0.16 |
| `ebg_` group | 6 | 0.86 | 0.49 |
| `group_` grouping | 5 | 0.38 | 0.14 |
| `anl4` analyst | 4 | 0.37 | 0.09 |
| `tbv_` analyst | 2 | 0.51 | 0.14 |
| `anl9` analyst | 1 | −0.60 | −0.27 |

## Conclusion

- **Only 2 of 314 blocks cleared both user-level thresholds** (Sharpe ≥ 1.25 and
  Fitness ≥ 1.0) and **neither cleared all checks**; both failed
  `LOW_SUB_UNIVERSE_SHARPE` and `LOW_2Y_SHARPE`. This is the first EUR evidence in the
  workspace and it says the EUR/COUNTRY analyst surface is much harder than the
  USA/TOP3000 fundamental surface the ledger was built on.
- The largest family (`anl10` consensus / `pred_surps` / `smart_ests` revisions,
  263 blocks) tops out at Sharpe 1.37 with Fitness 1.02. Only one block in that family
  is even usable, and it fails sub-universe and 2-year Sharpe.
- `anl69` fields are the exception: 24 blocks, best Sharpe 1.97 / Fitness 1.58 / turnover
  5.78% / margin 27.78 bps. Tiny sample, but it is the only family here that produced a
  submittable-looking metric pair.
- **The bottleneck is not the headline Sharpe.** `LOW_SHARPE` and `LOW_FITNESS` dominate
  because most single-field transforms are simply weak, but among the *strong* blocks the
  recurring killers are `LOW_2Y_SHARPE` (95.5% of blocks) and `LOW_SUB_UNIVERSE_SHARPE`
  (47.1%). Any repair work must target the recent-period and sub-universe profile, not the
  headline number.
- **Short second arguments collapse Fitness through turnover.** `..., 5)` inside
  `ts_zscore`/`quantile` (results 3 and 5) produced 68–75% turnover and Fitness 0.37–0.42
  while keeping Sharpe ~1.2–1.4. The long windows (`21`, `63`, `126`, `252`) are the only
  ones that produced workable Fitness.
- **Grouping operators on these fields add turnover or concentration without adding
  Sharpe.** `group_count`/`group_sum`/`group_std_dev` over `market`/`sector`/`industry`
  (results 30, 45, 51, 52, 54, 58, 109) land at Sharpe 0.2–0.7 with 56–87% turnover, or
  trigger `CONCENTRATED_WEIGHT`/`LOW_TURNOVER`. 96 of 314 blocks failed
  `CONCENTRATED_WEIGHT`.
- **Sign flips are not symmetric.** Negative-Sharpe blocks at the bottom of the sweep
  (e.g. `ts_std_dev(ts_backfill(anl69_ltg_dif_expected_report_dt, 21), 63)` at −1.37)
  do not become +1.37 when negated, and some `zscore`/`group_zscore` variants inverted
  sign relative to their `rank` equivalents. Residualised/relative transforms are
  producing different exposures, not a mirrored signal.
- 37 blocks fell below 1% turnover (`LOW_TURNOVER`) — a large share of the sweep is
  variance fields (`government_bond_yield`, `*_currency_code`, `expected_report_*`) that
  are essentially static, which is a field-selection error rather than a tuning issue.

## Lesson

- In EUR/TOP2500 under COUNTRY neutralization, **analyst consensus level fields are weak**
  as standalone ranks; the strongest uses are `anl69` best-EPS-style fields with
  time-series scaling (not ranking), and `anl10_*_consensus` with `ts_zscore(..., 63)`.
- **`ts_backfill(field, 21)` + one transform is not enough to clear the 2-year Sharpe
  test.** The task is not "find a stronger transform" but "find a signal whose recent
  2-year profile is at least as good as its full-history profile".
- Never carry an `F`-code between dumps: this dump's `F15` is
  `LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE`, this dump's `F16` adds `LOW_SHARPE`, and the
  2026-10-06 dump's `F15`/`F16` mean entirely different things.

## Next action

- Treat `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` (Result 1) as the
  sweep's one escalation candidate: single-dataset `anl69` → ATOM-shaped, 5.78% turnover
  → inside the IS-Ladder ×0.85 PASS relaxation band (turnover < 30%). Repair target is
  sub-universe / 2-year Sharpe, not Sharpe or Fitness.
- Do not re-run the generic `anl10` single-field transform grid; it is saturated at
  Sharpe ≈ 1.2–1.4 with Fitness ≤ 1.0.
- Before any further EUR analyst work, run field diagnostics on the `anl69_*` family and
  check coverage/history length — a 24-block sample with one strong result is suggestive,
  not established.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `067` |
| **Record Type** | `Bulk Multi-Simulation Sweep` |
| **Source Dataset / Fields** | Multi-field sweep (analyst, price-volume, fundamental, option/IV) |
| **Region / Delay / Universe** | `EUR` · Delay `1` · `TOP2500` |
| **Neutralization / Decay / Truncation** | `COUNTRY` · Decay `5` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-10-04` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `see sweep summary` · Fitness: `see sweep summary` · Turnover: `see sweep summary` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `0` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `ATOM-eligible candidate surface (single-dataset transforms)` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/EUR/067_eur_top2500_country_analyst_sweep.md` |

