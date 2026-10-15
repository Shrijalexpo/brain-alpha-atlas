# Simulation 069 - EUR Multi-Universe Sweep, Decay 0 (1,809 Results)

Status: FAILED

Type: bulk sweep record (1,809 result blocks across 15 universe/neutralization sections).
Machine-readable data: `Analysis and Simulation Reports/sweeps-and-experiments/20261006_100742.csv` / `.json` / `.md`.
Full generated report with all 1,809 expression rows: `Analysis and Simulation Reports/sweeps-and-experiments/20261006_100742.md`.

## Sweep

Same single-field-transform grid as 067 and 068, re-run on the whole EUR universe ladder,
but with **Decay 0** instead of Decay 5 — the only setting that differs from simulation 068.
This makes the pair (068, 069) a direct decay experiment on the same expression family.

Representative expressions:

```text
ts_rank(ts_backfill(pv37_snapshot1_volume125000, 21), 63)
ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)
```

## Settings

```text
Instrument Type: Equity (not shown in paste)
Region: EUR
Universe: TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 (sectioned)
Language: Fast Expression
Delay: 1
Decay: 0
Truncation: 0.08
Neutralization: INDUSTRY, MARKET, COUNTRY (sectioned)
Pasteurization: ON
Unit Handling: not shown in paste
NaN Handling: ON
Test Period: not shown in paste
```

## Known result

```text
Blocks: 1,809
Checks PASS: 0
Sharpe >= 1.25: 41
Fitness >= 1.0: 8
Sharpe >= 1.25 AND Fitness >= 1.0: 8
Sharpe >= 2.0: 4
Turnover > 70%: 168
Turnover < 1%: 106
Best Sharpe: 2.14   Best Fitness: 1.51
IS_LADDER_SHARPE failures: 1
```

Failed-check frequency (resolved through this dump's own legend — note `F14`, `F15`,
`F16`, `F20`, `F22`, `F24`, `F25` here mean something completely different from the same
codes in the 2026-10-04 dump):

```text
LOW_FITNESS               1801 / 1809   99.6%
LOW_SHARPE                1792 / 1809   99.1%
LOW_2Y_SHARPE             1669 / 1809   92.3%
LOW_SUB_UNIVERSE_SHARPE    888 / 1809   49.1%
CONCENTRATED_WEIGHT        508 / 1809   28.1%
LOW_TURNOVER               216 / 1809   11.9%
HIGH_TURNOVER              168 / 1809    9.3%
IS_LADDER_SHARPE             1 / 1809    0.1%
```

Top 12 by Sharpe:

| # | Section | Sharpe | Train | Fitness | Turnover | Returns | Margin | L/S | Expression | Failed |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | TOP2500/INDUSTRY | 2.14 | 2.44 | 0.51 | 108.03% | 6.13% | 1.13 | 1389/1427 | `ts_rank(ts_backfill(pv37_snapshot1_volume125000, 21), 63)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 518 | TOP2500/MARKET | 2.06 | 2.35 | 0.73 | 54.17% | 6.77% | 2.50 | 859/864 | `rank(ts_scale(ts_backfill(fnd17_vol3mavg, 21), 5))` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 920 | TOP2500/COUNTRY | 2.03 | 2.36 | 0.53 | 107.00% | 7.22% | 1.35 | 1387/1428 | `group_neutralize(ts_quantile(ts_backfill(pv37_snapshot1_volume122500, 21), 252), market)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 921 | TOP2500/COUNTRY | 2.01 | 2.48 | 0.45 | 101.47% | 5.09% | 1.00 | 1341/1395 | `ts_rank(ts_scale(ts_backfill(pv37_volume_11, 21), 21), 126)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 922 | TOP2500/COUNTRY | 1.98 | 2.27 | 0.47 | 102.65% | 5.81% | 1.13 | 1398/1417 | `ts_rank(ts_quantile(ts_backfill(pv37_snapshot1_volume132500, 21), 252), 126)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 923 | TOP2500/COUNTRY | 1.95 | 2.35 | 0.49 | 109.59% | 6.88% | 1.26 | 1389/1425 | `group_scale(ts_quantile(ts_backfill(pv37_snapshot1_volume110000, 21), 252), sector)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 924 | TOP2500/COUNTRY | 1.85 | 2.36 | 0.39 | 119.08% | 5.34% | 0.90 | 1382/1428 | `ts_quantile(ts_backfill(pv37_snapshot1_volume115000, 21), 21)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 1540 | TOPCS1600/COUNTRY | 1.82 | 2.10 | 1.41 | 15.20% | 9.15% | 12.04 | 613/592 | `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 925 | TOP2500/COUNTRY | 1.81 | 2.08 | 1.28 | 10.99% | 6.30% | 11.45 | 1010/1171 | `ts_quantile(ts_backfill(anl4_sadaf_netprofit_median, 21), 63)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 2 | TOP2500/INDUSTRY | 1.69 | 2.12 | 0.45 | 113.67% | 8.07% | 1.42 | 910/1895 | `ts_zscore(ts_backfill(pv37_snapshot1_volume110000, 21), 252)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 926 | TOP2500/COUNTRY | 1.66 | 1.70 | 0.84 | 21.34% | 5.43% | 5.09 | 642/682 | `group_scale(ts_quantile(ts_backfill(anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_mean, 21), 63), sector)` | LOW_FITNESS; LOW_2Y_SHARPE |
| 3 | TOP2500/INDUSTRY | 1.63 | 1.85 | 0.40 | 104.17% | 6.36% | 1.22 | 1082/1727 | `ts_av_diff(ts_scale(ts_backfill(pv37_snapshot1_volume132500, 21), 252), 126)` | LOW_FITNESS; HIGH_TURNOVER; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |

All 8 blocks with Sharpe ≥ 1.25 and Fitness ≥ 1.0:

| # | Section | Sharpe | Fitness | Turnover | Returns | Margin | Expression | Failed |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 927 | TOP2500/COUNTRY | 1.63 | 1.51 | 9.70% | 10.69% | 22.04 | `group_scale(ts_quantile(ts_backfill(anl69_nav_best_eeps_nxt_yr, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 928 | TOP2500/COUNTRY | 1.63 | 1.51 | 9.70% | 10.69% | 22.04 | `group_scale(ts_quantile(ts_backfill(anl69_ndebt_best_eeps_nxt_yr, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 1540 | TOPCS1600/COUNTRY | 1.82 | 1.41 | 15.20% | 9.15% | 12.04 | `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 925 | TOP2500/COUNTRY | 1.81 | 1.28 | 10.99% | 6.30% | 11.45 | `ts_quantile(ts_backfill(anl4_sadaf_netprofit_median, 21), 63)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 10 | TOP2500/INDUSTRY | 1.32 | 1.09 | 19.12% | 12.99% | 13.59 | `scale(ts_backfill(pv20_eps_indicator_3_feature12_394, 21))` | LOW_SHARPE; CONCENTRATED_WEIGHT; LOW_2Y_SHARPE |
| 5 | TOP2500/INDUSTRY | 1.55 | 1.02 | 10.14% | 5.43% | 10.71 | `ts_quantile(ts_decay_linear(ts_backfill(pv37_volume_153000, 21), 126), 252)` | LOW_SHARPE; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 931 | TOP2500/COUNTRY | 1.53 | 1.01 | 7.70% | 5.49% | 14.26 | `ts_zscore(ts_decay_linear(ts_backfill(anl4_af_div_low, 21), 21), 126)` | LOW_SHARPE; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 933 | TOP2500/COUNTRY | 1.45 | 1.00 | 5.98% | 5.95% | 19.87 | `scale(ts_zscore(ts_backfill(fnd17_ttmepsincx, 21), 252))` | LOW_SHARPE; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |

Best per universe / neutralization section (best Sharpe in each):

| Universe | Neut | Blocks | Best Sharpe | Best Fitness |
|---|---|---:|---:|---:|
| TOP2500 | INDUSTRY | 517 | 2.14 | 1.09 |
| TOP2500 | MARKET | 402 | 2.06 | 0.91 |
| TOP2500 | COUNTRY | 620 | 2.03 | 1.51 |
| TOPCS1600 | COUNTRY | 46 | 1.82 | 1.41 |
| TOPCS1600 | MARKET | 35 | 1.49 | 0.97 |
| TOPCS1600 | INDUSTRY | 23 | 1.16 | 0.65 |
| TOP1200 | COUNTRY | 22 | 0.74 | 0.25 |
| TOP1200 | INDUSTRY | 19 | 0.57 | 0.31 |
| TOP1200 | MARKET | 14 | 0.18 | 0.04 |
| TOP800 | INDUSTRY | 17 | 0.71 | 0.33 |
| TOP800 | MARKET | 14 | 0.62 | 0.29 |
| TOP800 | COUNTRY | 23 | 0.43 | 0.19 |
| TOP400 | INDUSTRY | 19 | 0.61 | 0.27 |
| TOP400 | MARKET | 13 | 0.47 | 0.20 |
| TOP400 | COUNTRY | 25 | 0.41 | 0.20 |

## Conclusion

- **0 of 1,809 blocks passed all checks**, and this dump contains the best legitimate
  Fitness/Sharpe pair found anywhere in the three sweeps:
  `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` at Sharpe 1.82 /
  Fitness 1.41 / 15.2% turnover / 9.15% returns / 12.04 bps margin — failing only
  `LOW_SUB_UNIVERSE_SHARPE` and `LOW_2Y_SHARPE`. It sits in the **TOPCS1600** universe,
  which is the consultant EUR investability scope.
- **Decay 0 fixes Fitness on low-turnover fields and destroys it on volume fields.**
  Comparing with simulation 068 on the same grid: TOP2500/COUNTRY now holds 5 of the 8
  passing blocks (versus 1 of 7 at decay 5), and the two best Fitness results in the dump
  (1.51 and 1.41) come from `anl69`/`anl4` analyst fields at 9.7–15.2% turnover. Removing
  decay did not raise the analyst signal; it removed the turnover penalty.
- **The cost is a large `HIGH_TURNOVER` cluster.** 168 blocks exceed 70% turnover (9.3%,
  up from 4.0% at decay 5), including 7 of the top 12 by Sharpe, all in the 100–120%
  turnover range on `pv37_snapshot1_volume*` fields. At decay 0 those volume ranks trade
  the entire book daily, so their Sharpe (1.6–2.1) is unreachable in practice
  (`HIGH_TURNOVER` is a hard fail).
- **Decay barely moves Sharpe.** On the six expressions that appear in both decay dumps,
  Sharpe changes by ≤ 0.13 while turnover changes by up to 3.3× (`rank(ts_backfill(pv37_snapshot1_volume122500, 21))`
  went from 11.74% to 37.41% turnover, Sharpe 0.02 → 0.11). Decay is a **turnover dial for
  this alpha family, not a strength dial** — a decisive finding for the fix strategy.
- **`anl69` is confirmed, not a fluke of simulation 067.** Two independent `anl69` blocks
  (results 927 and 928) both reach Sharpe 1.63 / Fitness 1.51 / 9.7% turnover. They report
  *identical* metrics for two different field names
  (`anl69_nav_best_eeps_nxt_yr` and `anl69_ndebt_best_eeps_nxt_yr`), which indicates the two
  fields carry the same values or nearly so — treat them as one signal, not as independent
  confirmations.
- **TOPCS1600 behaves differently here than at decay 5.** At decay 5 its best Sharpe was
  0.82; at decay 0 it is 1.82 with Fitness 1.41 (TOPCS1600/COUNTRY, 46 blocks, best section
  for risk-adjusted quality). The investability-constrained EUR scope is therefore
  *decay-sensitive* in a way TOP2500 is not.
- **Best low-turnover candidates in the workspace now sit at 6–21% turnover**:
  `scale(ts_backfill(pv20_eps_indicator_3_feature12_394, 21))` (Sharpe 1.32, Fitness 1.09,
  19.12% turnover, the highest returns in the dump at 12.99%) and
  `ts_zscore(ts_decay_linear(ts_backfill(anl4_af_div_low, 21), 21), 126)`
  (Sharpe 1.53, Fitness 1.01, 7.70% turnover, 14.26 bps margin).
- **`fnd17_vol3mavg` is the best non-`pv37` price/volume field found** (Sharpe 2.06 /
  Fitness 0.73 / 54.17% turnover), and it is interesting precisely because it is a
  *volatility* average rather than a volume level.

## Lesson

- **In EUR, decay should be tuned to hit the turnover band, not to improve the signal.**
  The signal is essentially decay-invariant; only transaction frequency moves. Pick decay
  from the target turnover, then repair sub-universe and 2-year Sharpe at that decay.
- **Decay 0 makes high-frequency volume fields unusable** (100%+ turnover) while making
  slow analyst fields usable. Field speed and decay setting must be chosen together; a
  slow field at decay 5 and a fast field at decay 0 are the two mismatched combinations.
- **The strongest low-turnover cluster in the entire 4,223-block workspace is `anl69_*`
  best-EPS-style fields with `ts_quantile(..., 63)` or `group_scale(ts_quantile(..., 252), sector)`.**
  It is the only cluster that combines Sharpe ~1.6–1.8 with Fitness > 1.0 and turnover
  < 16%.
- **Watch for alias fields.** Two `anl69` fields returning identical metrics means the
  sweep contains fewer independent tests than its row count suggests; do not treat such
  pairs as corroboration.
- Again: 0 PASS in 1,809 blocks. Since `LOW_SUB_UNIVERSE_SHARPE` or `LOW_2Y_SHARPE` appears
  in every strong block, **the sub-universe/2-year robustness problem, not signal
  discovery, is what blocks this EUR work.**

## Next action

- **Primary escalation candidate for EUR**: `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)`
  (Result 1540) — Sharpe 1.82 / Fitness 1.41 / 15.2% turnover / 613-592 book, in TOPCS1600.
  Single-dataset (`anl69`) → ATOM-shaped; 15.2% turnover → inside the ×0.85 IS-Ladder
  PASS relaxation band. Repair targets: `LOW_SUB_UNIVERSE_SHARPE`, `LOW_2Y_SHARPE`.
- Pair it with `ts_zscore(ts_decay_linear(ts_backfill(anl4_af_div_low, 21), 21), 126)`
  (Result 931, Sharpe 1.53 / Fitness 1.01 / 7.7% turnover) as a second, lower-turnover
  `anl4` variant.
- Then attack turnover on `scale(ts_backfill(pv20_eps_indicator_3_feature12_394, 21))`
  (Result 10, 12.99% returns) to fix its `CONCENTRATED_WEIGHT` failure rather than its
  Sharpe.
- Do not re-run a `pv37_snapshot1_volume*` grid at decay 0 — the whole surface is
  `HIGH_TURNOVER` by construction.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `069` |
| **Record Type** | `Bulk Multi-Simulation Sweep` |
| **Source Dataset / Fields** | Multi-field sweep (analyst, price-volume, fundamental, option/IV) |
| **Region / Delay / Universe** | `EUR` · Delay `1` · `TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 (sectioned)` |
| **Neutralization / Decay / Truncation** | `INDUSTRY, MARKET, COUNTRY (sectioned)` · Decay `0` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-10-06` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `see sweep summary` · Fitness: `see sweep summary` · Turnover: `see sweep summary` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `0` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `ATOM-eligible candidate surface (single-dataset transforms)` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/EUR/069_eur_multi_universe_decay0_sweep.md` |

