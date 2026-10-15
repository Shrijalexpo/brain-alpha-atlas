# Past WorldQuant BRAIN Simulations

This file records alpha simulations shared through screenshots or discussed in the referenced conversation. The goal is to avoid repeating alphas that were already tested and to preserve what each result taught us.

Metrics are transcribed from the conversation when available. Some screenshots were not machine-readable in this environment, so details are based on the prior assistant's extracted notes.

## Simulation 001 - Positive Days Momentum

Expression:

```text
positive_days = ts_sum(returns > 0 ? 1 : 0, 250);

trade_when(
    volume > adv20,
    positive_days,
    -1
)
```

Known result:

```text
Fitness: 1.13
Turnover: 3.04%
Sub-universe Sharpe: 0.47
Sharpe: 0.99
```

Conclusion:

- Fitness and Turnover were acceptable.
- Sharpe was below the likely threshold of 1.25.
- Suggested fixes included ranking the signal, using percentage positive days, reversing the signal, and volatility normalization.

## Simulation 002 - Operating Income / Cap Plus Return Reversion

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-returns)
)
```

Known result:

```text
Sharpe: 1.14
Fitness: 0.84
Turnover: 22.78%
Sub-universe Sharpe: 0.73
```

Conclusion:

- Close but not passing.
- Sharpe and Fitness both needed improvement.
- Raw `operating_income / cap` plus daily return reversion was too noisy.

## Simulation 003 - Operating Income / Cap Plus Time-Series Return Rank

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-ts_rank(returns, 20))
)
```

Known result:

```text
Sharpe: 1.29
Fitness: 0.60
Turnover: 63.33%
Sub-universe Sharpe: 0.77
```

Conclusion:

- Sharpe passed, but Fitness failed.
- Turnover was very high.
- Main fix direction: increase Decay and reduce/smooth the return component.

## Simulation 004 - Operating Income / Cap Plus Smoothed Returns

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-ts_mean(returns, 5))
)
```

Known result:

```text
Sharpe: 1.05
Fitness: 0.98
```

Conclusion:

- Worse Sharpe than Simulation 003.
- Fitness nearly improved but still failed.

## Simulation 005 - Smoothed Operating Income / Cap Plus Return Reversion

Expression:

```text
zscore(
    rank(ts_mean(operating_income / cap, 4))
    +
    0.4 * rank(-returns)
)
```

Known result:

```text
Sharpe: 1.01
Fitness: 0.89
```

Conclusion:

- Not enough improvement.
- Smoothing slow-moving fundamentals did not solve the issue.

## Simulation 006 - Operating Income / Cap Plus Volatility-Adjusted Returns

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-returns / ts_std_dev(returns, 20))
)
```

Known result:

```text
Sharpe: 0.99
Fitness: 0.86
```

Conclusion:

- Volatility adjustment did not improve this family.

## Simulation 007 - Dividend, Volume Surprise, Return Reversion

Expression:

```text
zscore(
    rank(dividend)
    + 0.3 * rank(volume / adv20)
    + 0.2 * rank(-returns)
)
```

Known result:

```text
Sharpe: 1.78
Fitness: 0.67
Turnover: 57.5%
Decay: 4
```

Conclusion:

- Strong Sharpe.
- Fitness failed because Turnover was too high.
- Suggested fixes: Decay 8 to 10, smooth returns, reduce return or volume component.

## Simulation 008 - Raw Operating Income Time-Series Rank

Expression:

```text
rank(ts_rank(operating_income, 12))
```

Known result:

```text
Sharpe: below about 0.5
```

Conclusion:

- Raw operating income alone was weak.
- Time-series transforms on quarterly fundamentals were not useful enough.

## Simulation 009 - Raw Operating Income Time-Series Mean

Expression:

```text
rank(ts_mean(operating_income, 4))
```

Known result:

```text
Sharpe: below about 0.5
```

Conclusion:

- Raw operating income alone was weak.

## Simulation 010 - Raw Operating Income Time-Series Delta

Expression:

```text
rank(ts_delta(operating_income, 4))
```

Known result:

```text
Sharpe: below about 0.5
```

Conclusion:

- Raw operating income changes did not produce a strong signal in tested settings.

## Simulation 011 - Quality Value Composite

Expression:

```text
group_neutralize(
    rank(return_equity)
    + rank(cashflow_op / assets)
    - rank(enterprise_value / ebitda),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.46
Fitness: 0.22
Turnover: 3.98%
Sub-universe Sharpe: 0.39
```

Conclusion:

- Structural checks were acceptable.
- Signal was too weak.
- Low Turnover means settings were not the main problem.

## Simulation 012 - Large Multi-Factor Quality/Value Composite

Expression:

```text
group_neutralize(
      rank(return_equity)
    + rank(return_assets)
    + rank(cashflow_op / assets)
    + rank(current_ratio)
    + rank(sales_growth)
    - rank(debt / assets)
    - rank(enterprise_value / ebitda),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: -0.28
```

Conclusion:

- Worse than simpler quality/value composite.
- Linear stacking averaged away useful signals.

## Simulation 013 - Nonlinear Profitability Cash Flow Product

Expression:

```text
group_neutralize(
    rank((return_equity * cashflow_op) / (assets * enterprise_value))
    - rank(debt / assets),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: -1.01
```

Conclusion:

- Much worse.
- The product interaction over-penalized or distorted the signal.

## Simulation 014 - Cash Flow Yield

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.41
```

Conclusion:

- Better than the negative composite attempts.
- Positive but too weak alone.
- Current best base direction: add one complementary factor at a time.

## Simulation 015 - Cash Flow Yield + ROE + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.18
Fitness: 0.71
Turnover: 30.35%
Sub-universe Sharpe: 0.72
```

Conclusion:

- Close, but not submittable.
- `-returns` improved the branch, but exact expression should not be repeated.

## Simulation 016 - Cash Flow Yield + ROA + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

- Exact metrics not captured in text.
- Observed worse than Simulation 015.

Conclusion:

- `return_assets` was worse than `return_equity` in this branch.

## Simulation 017 - Cash Flow Yield + ROE + Current Ratio + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(current_ratio)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.19
Fitness: 0.66
```

Conclusion:

- Slightly higher Sharpe than Simulation 015, but lower Fitness.
- `current_ratio` did not help enough.

## Simulation 018 - Cash Flow Yield + ROE + ROA + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(return_assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

- Exact metrics not captured in text.
- Observed worse than the prior best branch.

Conclusion:

- Stacking similar profitability factors hurt performance.

## Simulation 019 - Cash Flow Yield + Operating Income / Assets + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(operating_income / assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

- Exact metrics not captured in text.
- Observed plateaued or worse than prior best.

Conclusion:

- Operating-income family remained weak in this setup.

## Simulation 020 - Cash Flow Yield + Sales Growth + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.21
Fitness: 0.58
```

Conclusion:

- Closest cashflow/value branch.
- Growth helped more than extra profitability factors.

## Simulation 021 - Cash Flow Yield + Sales Growth + Current Ratio + Reversal

Status: FAILED

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(sales_growth)
    + rank(current_ratio)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

- Exact metrics not captured in text.
- Observed worse than Simulation 020.

Conclusion:

- `current_ratio` hurt the value-growth branch.

## Simulation 022 - EBITDA Yield + Sales Growth + Reversal

Status: FAILED

```text
group_neutralize(
    rank(ebitda / enterprise_value)
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.21
Sub-universe Sharpe: 1.26
```

Conclusion:

- Similar Sharpe to cashflow/EV, but better Sub-universe Sharpe.
- EBITDA/EV became the better value base.

## Simulation 023 - EBITDA Yield + ROE + Sales Growth

Status: FAILED

```text
group_neutralize(
    rank(ebitda / enterprise_value)
    + rank(return_equity)
    + rank(sales_growth),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.28
```

Conclusion:

- Replacing `-returns` with `return_equity` badly hurt performance.

## Simulation 024 - Time-Series Ranked EBITDA Yield + Sales Growth + Reversal

Status: FAILED

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.36
Fitness: 0.68
Sub-universe Sharpe: 1.39
```

Conclusion:

- First branch to pass Sharpe.
- Fitness still failed.

## Simulation 025 - Time-Series Ranked EBITDA Yield + Time-Series Ranked Sales Growth + Reversal

Status: FAILED

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.78
Fitness: 0.97
Sub-universe Sharpe: 1.78
```

Conclusion:

- Very close but still failed Fitness.
- Needed smoothing in the reversal component.

## Simulation 026 - Submitted Alpha

Status: PASSED_SUBMITTABLE

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.61
Fitness: 1.02
Turnover: 25.25%
Sub-universe Sharpe: 1.53
Competition Challenge: Passed
Self-correlation: pending at screenshot time
```

Conclusion:

- First recorded submittable alpha.
- Do not suggest this exact alpha again; preserve as the submitted baseline.

## Quick Status Index

See `simulations/status_index.md` for the complete pass/fail table and duplicate-avoidance rules.

## Later Simulations

Additional simulations from the continued conversation are saved as individual files:

```text
simulations/027_submitted_cashflow_quality_improvement_reversal.md
...
simulations/063_op_cash_flow_stddev_high_turnover.md
simulations/064_smoothed_operating_cash_flow_estimate_dispersion.md
simulations/065_op_cash_flow_stddev_sales_growth_reversal.md
simulations/066_op_cash_flow_stddev_level_reversal.md
simulations/067_eur_top2500_country_analyst_sweep.md
simulations/068_eur_multi_universe_decay5_sweep.md
simulations/069_eur_multi_universe_decay0_sweep.md
```

See `simulations/status_index.md` for their pass/fail/submitted/self-correlation/error statuses.

## Simulations 067-069 - EUR Bulk Sweeps

Status: FAILED (all three)

These are not single hand-built alphas. They are three pasted BRAIN multi-simulation
result pages covering **4,223 simulated expressions** in Region EUR, Delay 1,
Truncation 0.08, Pasteurization ON, NaN Handling ON. They are recorded as three sweep
files plus machine-readable data:

```text
simulations/067_eur_top2500_country_analyst_sweep.md   314 blocks  EUR/TOP2500/COUNTRY, decay 5
simulations/068_eur_multi_universe_decay5_sweep.md     2,100 blocks EUR x 5 universes x 3 neutralizations, decay 5
simulations/069_eur_multi_universe_decay0_sweep.md     1,809 blocks EUR x 5 universes x 3 neutralizations, decay 0
simulations/sweeps/                                    CSV + JSON + generated reports for all 4,223 blocks
```

Known result:

```text
Checks PASS: 0 of 4,223
Sharpe >= 1.25 AND Fitness >= 1.0: 2 (067) + 7 (068, 2 degenerate) + 8 (069)
Highest legitimate Sharpe: 2.51   Highest legitimate Fitness: 1.60 (adjfactor artifact) / 1.51 (anl69)
Best legitimate pair: Sharpe 1.82 / Fitness 1.41 / turnover 15.20%  (069 TOPCS1600/COUNTRY)
Most common failed checks: LOW_FITNESS (99.6%), LOW_SHARPE (99.1%), LOW_2Y_SHARPE (92.3-98.3%), LOW_SUB_UNIVERSE_SHARPE (46-49%)
```

Conclusion:

- The first EUR evidence in this workspace three-times over. Nothing passed, and the
  binding constraint is `LOW_2Y_SHARPE` together with `LOW_SUB_UNIVERSE_SHARPE` rather than
  headline Sharpe.
- `anl69_*` slow analyst fields with `ts_quantile(..., 63)` / `ts_scale(..., 63)` /
  `group_scale(ts_quantile(..., 252), sector)` form the only cluster combining Sharpe
  ~1.6-1.8 with Fitness > 1.0 and turnover under 16%.
- `pv37_*` snapshot and session volume fields give the highest raw Sharpe in EUR TOP2500
  (up to 2.51) but are structurally fragile: sub-universe Sharpe at decay 5, and
  `HIGH_TURNOVER` (100%+) at decay 0.
- Decay 5 -> 0 barely changes Sharpe and changes turnover by up to 3.3x, so decay is a
  turnover dial for this alpha family, not a strength dial.
- The consultant-level checks are already active in these sessions: `IS_LADDER_SHARPE`
  appears in 3 blocks and `LOW_ROBUST_UNIVERSE_SHARPE` in 6 across 068 and 069.
- Two blocks are construction artifacts to be discarded: `pv37_low_14` (Sharpe 11.18,
  100% turnover, 12/218 book) and `adjfactor` (price-adjustment factor).

See also:

- `simulations/sweeps/README.md` for the data files, regeneration command, and caveats
- `simulations/status_index.md` for the escalation-candidate table
- `Research/lessons_from_simulations.md` for the durable lessons
- `Data/datasets_and_fields.md` for the EUR and USA field-family notes

## Simulations 070 - USA TOP3000 / INDUSTRY Analyst-Growth Sweep

Status: FAILED

This is not a single hand-built alpha. It is one pasted BRAIN multi-simulation result page
covering **2,500 simulated expressions** in Region USA, Universe TOP3000, Neutralization
INDUSTRY, Delay 1, Decay 5, Truncation 0.08, Pasteurization ON, NaN Handling ON. It is
recorded as one sweep file plus machine-readable data:

```text
simulations/070_usa_top3000_industry_analyst_growth_sweep.md   2,500 + 1,050 blocks, decay 5 (corrected 2026-10-09)
simulations/sweeps/20261008_071542_d1_usa_6universes.{csv,json,md}   page 1, 2,500 rows, true out-of-sample Sharpe column
simulations/sweeps/20261008_071542_d2_usa_top3000.{csv,json,md}      page 2, 1,050 rows (previously unrecorded)
simulations/sweeps/20261008_071542_all_results.csv                   3,550 rows, combined
simulations/sweeps/superseded/                                       the two replaced files, provenance only
```

Known result:

```text
Checks PASS: 0 of 2,500 (page 1) and 0 of 1,050 (page 2)
Blocks above true Sharpe 1.25: 12 (page 1, all TOP3000), 0 (page 2)
Sharpe >= 1.25 AND Fitness >= 1.0: 1 (annual_financing_cashflow_amount, true Sharpe 1.40)
Highest true Sharpe: 1.54 (page 1, netprofit_actual_q1_qoq_growth); page 2 tops out at 1.23
Highest legitimate Fitness: 1.03
Most common failed checks: LOW_SHARPE and LOW_FITNESS (nearly every block), LOW_2Y_SHARPE and LOW_SUB_UNIVERSE_SHARPE dominating the F2/F4 sets
Artifacts: 4 fields (net_9_feature3_predictor, option_return_bucket2_label_2, option_return_bucket3_prob1, adjfactor)
Correction: the first version of this entry reported Train Sharpe as the headline Sharpe and omitted page 2 entirely.
```

Conclusion:

- The first large USA sweep in this workspace, and it mirrors the EUR lesson in a different
  region/universe/neutralization: **nothing passes**, and the blockage is robustness plus
  Fitness rather than headline Sharpe alone.
- With 2,444 distinct fields tested almost entirely as 1-2 neutralization variants each,
  this dump is a field-screen, not a tuned family exploration. The `~anl10_*` and `~anl15_*`
  analyst/estimate families are the most numerous and the most crowded, and they did **not**
  produce a passable block.
- The best surface is **low-turnover estimate-asymmetry, estimate-growth, and cashflow
  signals** (true Sharpe 1.37-1.54, turnover 2-7%). The single block with Fitness >= 1.0 is
  `annual_financing_cashflow_amount` (true Sharpe 1.40 / Fitness 1.03 / Turnover 2.00%), and
  its only failures are LOW_SHARPE + LOW_2Y_SHARPE.
- Page 2 (`anl15_*` 796 blocks, `anl10_*` 237 blocks, USA/TOP3000/INDUSTRY) is a negative
  control: 0 blocks above true Sharpe 1.25, best 1.23, and 6 blocks still PENDING. Its
  train/out-of-sample columns also disagree in both directions, so neither column alone is
  the truth.
- The cleanest fitness-band repair targets are the F8 blocks `netprofit_actual_q1_qoq_growth`
  and `estimate_year2_change_3mo_gross_margin`; they fail only LOW_SHARPE + LOW_FITNESS.
- The same artifact families appear as in EUR (`net_9_*`, `option_return_bucket*`, `adjfactor`)
  and should be discarded in both regions.
- `anl69` in this USA dump did **not** reproduce the EUR slow-level cluster; it surfaced as
  report-time and best-estimate variants that came out weak. Do not assume the clerk prefix
  means the same economic field across regions.

See also:

- `simulations/070_usa_top3000_industry_analyst_growth_sweep.md` for the full block-by-block record
- `simulations/sweeps/20261008_071542_d1_usa_6universes.csv` and `20261008_071542_d2_usa_top3000.csv` for the machine-readable results
- `simulations/sweeps/superseded/README.md` for exactly what was wrong with the first version of this entry
- `simulations/071_multi_region_bundle_20261009.md` for the next session's six-page multi-region bundle

---

## Simulations 071 - Six-Page Multi-Region Bundle (KOR / AMR / EUR / GLB / USA)

Status: FAILED

One RTF export containing **six concatenated BRAIN result pages** and five regions. Each page
has its own settings and its own `Fx` legend, so each was parsed separately:

```text
Source:      ~/Downloads/Simulation .rtf  (1,674,831 bytes, md5 862d3bacb18569ae2aea90cc6717c493)
Parsed text: simulations/sweeps/sources/20261009_115500.txt  (md5 485d8962d27370eda1bbbdde118bd322)
d1 KOR / TOP600        789 blocks,          INDUSTRY + MARKET + SUBINDUSTRY, decay 5
d2 AMR / TOP600      3,250 blocks,          SUBINDUSTRY + INDUSTRY + MARKET, decay 5
d3 EUR / 5 universes 1,141 blocks,          COUNTRY + INDUSTRY, decay 5
d4 ALL / LARGE         113 blocks,          INDUSTRY, decay 5
d5 USA / TOP3000       174 blocks,          5 neutralizations, decay 0-16 per block
d6 ALL / LARGE          79 blocks,          INDUSTRY, decay 5
Total                5,546 blocks
```

Known result:

```text
Checks PASS: 0 of 5,546
PENDING (unevaluated): 42  (AMR 25, EUR 15, USA 2)
Blocks at Sharpe >= 1.25 with Fitness >= 1.0: 35, of which 12 have no verdict yet
Best KOR:  oth176_lmt_close_eq_score   Sharpe 2.36 / Fitness 1.67, only LOW_2Y_SHARPE fails
Best USA:  IV-dispersion on cap buckets Sharpe 2.61 / Fitness 1.88
Best AMR:  mdl39 value-momentum leaders all PENDING; best evaluated 1.54 / 1.40
Best EUR:  pv20_netdebt z-score         Sharpe 2.63 / Fitness 1.24 at 69.46% turnover
Best GLB:  Sharpe 1.42 / Fitness 0.57 across 192 blocks -> nothing usable
```

Conclusion:

- **Nothing passes in any of the five regions**, but the failure mode has changed. Five
  different regions now produce blocks above Sharpe 2.2, so signal strength is no longer the
  bottleneck: `CONCENTRATED_WEIGHT`, `LOW_SUB_UNIVERSE_SHARPE`, `LOW_2Y_SHARPE` and the
  consultant ladder are.
- The **KOR `oth176_lmt_close_eq_score`** block is the best Sharpe+Fitness pair in the bundle
  and the only block that fails a single check. It is the first KOR-scope candidate here.
- The **USA implied-volatility family** is the strongest USA surface recorded so far (2.21 to
  2.61 Sharpe, 1.07 to 1.88 Fitness) and it is a new mechanism, not another variation of the
  exhausted `cashflow_op / enterprise_value` branch. All variants fail the same two checks at
  decay 4, 6 and 8, so the repair is portfolio construction, not smoothing.
- **EUR adds nothing new**: `pv20`-style z-scores die on sub-universe and 2-year robustness,
  and `adjfactor` again placed in the EUR top three, which is an artifact, not a signal.
- **GLB / ALL-LARGE is a dead end at this stage** — 192 blocks, best Fitness 0.57 — but it
  introduces the global check vocabulary (`LOW_GLB_APAC_SHARPE`, `LOW_ASI_JPN_SHARPE`,
  `LOW_GLB_AMER_SHARPE`, `LOW_GLB_EMEA_SHARPE`, `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`).
- `IS_LADDER_SHARPE` fires in **96 of 174 USA blocks (55%)** and `CLUSTER_TEST` in 27 EUR
  blocks: the consultant-stage tests are now the visible ceiling, not just the user thresholds.

Lesson:

- Treat `PENDING` as unmeasured. A quarter of the AMR blocks that clear both user thresholds
  have no verdict, and the AMR leaderboard's top four are all in that group.
- Regional Sharpe bars differ. AMR/TOP600 blocks at Sharpe 1.4-1.6 still fail `LOW_SHARPE`, so
  the workspace's 1.25 assumption cannot be reused across regions.
- A page pasted in `### Decay: N - Truncation: X` form has no result numbers in the source.
  Never join such a page to another by `result_no`; the parser now synthesises the numbers
  and keeps decay/truncation per row.
- 5,524 of the 5,546 blocks are expressions never simulated before (19 repeats against the
  earlier EUR/USA sweep files), so this bundle is genuinely new ground rather than a re-test.

Next action:

- Re-run the four pending blocks that already clear both user thresholds (two USA, two AMR)
  to turn PENDING into verdicts; they are cheap and the AMR four are the family leaders.
- Repair the USA IV family against `CONCENTRATED_WEIGHT` specifically: finer cap buckets,
  `truncate`/`winsorize` on the final signal, decay and IV construction unchanged.
- Do not spend further sweeps on ALL/LARGE until a GLB page produces Fitness > 1.0 anywhere.

See also:

- `simulations/071_multi_region_bundle_20261009.md` for the per-page record
- `simulations/sweeps/20261009_115500_d1..d6_*.csv` for per-page machine-readable results
- `simulations/sweeps/20261009_115500_all_results.csv` and `20261009_115500_SUMMARY.md` for the cross-page view
- `simulations/status_index.md` for the KOR and USA IV escalation candidates and the pending-block table
- `simulations/status_index.md` for the USA escalation-candidate table and do-not-re-run list
- `Data/datasets_and_fields.md` for the USA field-family notes and rules
