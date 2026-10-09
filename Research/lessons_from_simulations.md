# Lessons From Recorded WorldQuant BRAIN Simulations

Last updated: 2026-10-06

This file captures what the previous simulations taught, so future alpha suggestions do not repeat the same failed paths.

## Main Outcome

The first recorded submittable alpha was:

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

## What Failed

- Raw `operating_income` variants failed because slow quarterly fields did not become useful just by applying `ts_mean`, `ts_rank`, or `ts_delta`.
- `operating_income / cap` plus short-term reversal got close but did not reach both Sharpe and Fitness targets.
- Dividend plus volume plus reversal produced strong Sharpe but failed Fitness due high turnover.
- Generic quality/value composites such as ROE plus cashflow/assets minus EV/EBITDA were too weak.
- Large linear factor stacks performed worse than smaller, cleaner combinations.
- The nonlinear product `(return_equity * cashflow_op) / (assets * enterprise_value)` produced strongly negative Sharpe.
- `current_ratio` hurt the tested cashflow/value-growth branches.
- Replacing `-returns` with `return_equity` in the EBITDA/EV and sales-growth branch collapsed Sharpe.

## What Worked

- Adding short-term reversal to value/fundamental factors improved performance.
- `sales_growth` was more useful than adding more profitability ratios in the cashflow/value branch.
- Switching from `cashflow_op / enterprise_value` to `ebitda / enterprise_value` improved robustness, especially Sub-universe Sharpe.
- Applying `ts_rank(..., 126)` to `ebitda / enterprise_value` was a major improvement.
- Applying `ts_rank(..., 126)` to `sales_growth` further improved Sharpe.
- Smoothing reversal with `ts_mean(-returns, 5)` improved Fitness enough to pass.

## Future Alpha Generation Rules

- Check `simulations/status_index.md` before suggesting alpha code.
- Do not repeat exact failed or submitted expressions.
- Suggest only 1 to 3 alphas at a time.
- Prefer one controlled change per iteration.
- If a branch plateaus after 3 to 5 nearby tests, move to a different factor family instead of stacking more fields.
- For future variants of the submitted branch, watch self-correlation risk carefully.
- Avoid exact expressions recorded as `FAILED_SELF_CORRELATION`; good Sharpe/Fitness is not enough if the backbone is too similar.
- For now, avoid expression-level `group_neutralize()` unless the user explicitly asks, because the user is relying on BRAIN Settings neutralization.
- Keep suggestions to at most 3 alphas at a time.

## Promising Next Directions

Use these directions instead of replaying the submitted alpha:

- Change the lookback window, for example `63`, `189`, or `252`, but only one window at a time.
- Replace the reversal component with a different smoothed price-volume signal.
- Try analyst revisions, volatility, accruals, or earnings-quality datasets.
- Explore group-relative transforms inside industry/subindustry rather than only size buckets.
- Test alternative value measures only if they are time-series transformed, not as plain static ranks.

## Later Lessons Added

- `rank(ebitda/enterprise_value) + rank(ts_mean(-returns,5))` submitted successfully, but nearby variants with `ts_rank(-returns,10)`, `volume/adv20`, `ts_delta(-returns,5)`, low volatility, or close/high behavior failed.
- `ts_rank(ebitda/enterprise_value,126) + ts_mean(-returns,5)` was very close, with Sharpe 1.51 and Fitness 0.98.
- `volume/adv20` can be strong but self-correlation is a major risk.
- `current_ratio`, `debt/assets`, and low-volatility combinations were weak in the tested universe/settings.
- Pure and mixed sentiment alphas produced encouraging Sharpe but poor Fitness or excessive Turnover; sentiment is not a priority right now.
- Event/vector estimate fields caused operator errors when used directly with `ts_delta`; verify field type before applying time-series operators.
- The `op_cash_flow_stddev` branch had Sharpe 1.52 with a fast 10-day delta plus volume/reversal, but the slower 20-day delta averaged over 20 days fell to Sharpe 0.85 and Fitness 0.48. For this branch, avoid simply adding more smoothing; keep a faster dispersion impulse or pair it with a stronger slow anchor.
- Replacing the high-turnover volume leg with `ts_rank(sales_growth,126)` produced a close result: Sharpe 1.48, Fitness 0.91, Turnover 21.78%, SubU 1.49. The backup `ts_rank(op_cash_flow_stddev,63)` level version was weaker at Sharpe 1.16 and Fitness 0.78, so continue with the 10-day delta branch.

## EUR Bulk Sweeps (2026-10-04 to 2026-10-06) - 4,223 Simulated Expressions

Three pasted EUR multi-simulation pages were parsed and recorded as
`simulations/067_...`, `068_...`, `069_...` with machine-readable data and generated
reports in `simulations/sweeps/`. This is the first EUR evidence in the workspace.
Settings throughout: Region EUR, Delay 1, Truncation 0.08, Pasteurization ON,
NaN Handling ON; decay 5 for 067/068 and decay 0 for 069.

### Outcome, in one line

**0 of 4,223 expressions passed all platform checks.** 17 blocks (0.4%) cleared the
user-level Sharpe >= 1.25 and Fitness >= 1.0 pair, and two of those 17 are construction
artifacts.

### What failed, and why

- **`LOW_2Y_SHARPE` is the binding constraint**, not headline Sharpe: it appears in 95.5%
  (067), 98.3% (068) and 92.3% (069) of failed blocks. `LOW_SUB_UNIVERSE_SHARPE` adds
  46-49%. The last-2-year window and the sub-universe profile are what kill this work.
- **A single `ts_backfill(field, 21)` plus one transform is not a viable EUR strategy.**
  263 of 314 blocks in 067 are `anl10` single-field transforms and the whole family peaks
  at Sharpe 1.37 / Fitness 1.02.
- **Grouping operators add turnover and concentration without adding Sharpe.** `group_count`,
  `group_sum`, `group_std_dev` and `group_neutralize` over `market`/`sector`/`industry`
  land at Sharpe 0.2-0.7 with 48-90% turnover, and `CONCENTRATED_WEIGHT` fires in 22-31%
  of blocks across all three sweeps.
- **Degenerate books look spectacular and must be discarded first.** `ts_product(ts_backfill(pv37_low_14, 21), 63)`
  reports Sharpe 11.18 with train Sharpe 0.00, turnover pinned at exactly 100.00%, zero
  drawdown and a 12-long/218-short book. `normalize(ts_zscore(ts_backfill(adjfactor, 21), 126))`
  reports Sharpe 1.94 / Fitness 1.60 / returns 31.20% on a 295/25 book - `adjfactor` is a
  price-adjustment factor, not a signal. **Always check train Sharpe, turnover and
  long/short counts before sorting a sweep by Sharpe.**
- **Universes below TOP2500 collapse**: every TOP400/TOP800/TOP1200 section in both
  multi-universe sweeps has best Sharpe <= 0.87.
- **Sign flips are not symmetric** in EUR either: negating a negative-Sharpe block does not
  reproduce the positive counterpart, and `rank` versus `zscore`/`group_zscore` equivalents
  of the same field differ in sign in places.

### What worked

- **`anl69_*` slow analyst fields are the best cluster found so far.** 96 blocks across the
  sweeps; it is the only family where *every* Sharpe >= 1.25 block also cleared Fitness 1.0
  (4 of 4). Best pairs:
  - `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` - Sharpe 1.97 / Fitness 1.58 / turnover 5.78% / margin 27.78 bps
  - `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` - Sharpe 1.82 / Fitness 1.41 / turnover 15.20% (TOPCS1600)
  - `group_scale(ts_quantile(ts_backfill(anl69_nav_best_eeps_nxt_yr, 21), 252), sector)` - Sharpe 1.63 / Fitness 1.51 / turnover 9.70%
- **The pattern is "slow analyst level + `ts_quantile` / `ts_scale` at 63-252", not "rank a field".**
  `ts_quantile(ts_backfill(anl4_sadaf_netprofit_median, 21), 63)` reproduces it on a second
  analyst family (Sharpe 1.81 / Fitness 1.28 / 10.99% turnover).
- **`pv37` snapshot/session volume fields produce the highest raw EUR Sharpe** -
  `scale(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 126))` at Sharpe 2.51 /
  Fitness 1.09, and `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))`
  at Sharpe 2.41 / Fitness 1.16 - both with the signal holding out-of-sample
  (train Sharpe 2.7). Their defect is always the same: `LOW_SUB_UNIVERSE_SHARPE` at decay 5,
  `HIGH_TURNOVER` at decay 0.
- **`pv37_volume_*` can be tamed**: `ts_quantile(ts_decay_linear(ts_backfill(pv37_volume_153000, 21), 126), 252)`
  reaches Sharpe 1.55 / Fitness 1.02 at 10.14% turnover. Double smoothing, no short windows.
- **`fnd17_vol3mavg`** is the best non-`pv37` price/volume field seen (Sharpe 2.06 /
  Fitness 0.73 / 54.17% turnover) - a volatility average rather than a volume level.
- **`adv20_extra_usd`** is worth a second look: `group_rank(ts_quantile(ts_backfill(adv20_extra_usd, 21), 252), industry)`
  gives Sharpe 1.58 / Fitness 0.90 at 15.78% turnover.

### Decay lesson (directly comparable, 068 vs 069)

- The same grid run at decay 5 and decay 0 shows **Sharpe changing by <= 0.13 while turnover
  changes by up to 3.3x** (e.g. 11.74% -> 37.41%). **Decay is a turnover dial for this alpha
  family, not a strength dial.** Choose decay from the target turnover band, then repair
  sub-universe and 2-year Sharpe at that decay.
- Decay 0 makes fast volume fields unusable (7 of the top 12 by Sharpe sit at 100-120%
  turnover) while making slow analyst fields usable (5 of the 8 passing blocks in 069 are
  TOP2500/COUNTRY analyst fields, versus 1 of 7 at decay 5).

### Region lesson

- **EUR TOPCS1600 is decay-sensitive**: best Sharpe 0.82 at decay 5, but 1.82 / Fitness 1.41
  at decay 0. Treat TOPCS1600 as its own research scope, not a sub-universe of TOP2500.
- **Consultant-level checks are already firing in EUR.** `IS_LADDER_SHARPE` appears in 3
  blocks and `LOW_ROBUST_UNIVERSE_SHARPE` in 6 across the sweeps. Any "passing" EUR alpha
  must still clear `tutorials/consultant_information/submission_tests_and_alpha_types.md`.

### Ledger hygiene lesson

- **The `Fx` failed-check legend is per dump.** `F14` in the 2026-10-06 dump means
  `LOW_FITNESS, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE`; `F14` in the
  2026-10-04 dump means `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, CONCENTRATED_WEIGHT,
  LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE`. Never carry an F-code between dumps - resolve it
  through its own file's legend (`Tools/brain_sweep_parser.py` does this automatically).
- **Watch alias fields.** Two `anl69` fields (`anl69_nav_best_eeps_nxt_yr`,
  `anl69_ndebt_best_eeps_nxt_yr`) returned byte-identical metrics in 069, so they are one
  signal, not two confirmations.

### Parsing and data-integrity lessons (2026-10-09)

- **`Train Sharpe` and `Sharpe` are different columns and must never be conflated.** In the
  Oct-8 USA export they disagree in 2,448 of 2,500 blocks, and the training column is
  systematically higher (up to +0.39). A substring match on `Sharpe` silently captures the
  training line; parse both explicitly. Every number in a record, ledger row or field table
  inherits the mistake otherwise.
- **One pasted export can contain several pages.** The declared `N Results` header describes
  only the first page. The Oct-8 export held 2,500 + 1,050 blocks and the second page was
  dropped for a day; the Oct-9 export held six pages across five regions. Split on every
  `N Results` header and give each page its own settings and its own legend.
- **Universe attribution must come from the dump, not from the header or a default.** A page
  header can omit `Universe:` entirely and be split into six universes by `## Universe:`
  sections; labelling all 2,500 blocks TOP3000 mislabelled 306 of them.
- **`PENDING` is not `PASS` and is not clean.** 42 of 5,546 blocks in the Oct-9 bundle were
  still computing when the page was copied, including the top four AMR leaders. A block with a
  strong Sharpe and no verdict is unmeasured.
- **Follow the output shape.** When a page names blocks `### Decay: N - Truncation: X`, the
  `result_no` must be synthesised; such rows cannot be joined to numbered rows from another
  page.

### Rules to carry forward

- Do not re-run generic single-field transform grids on `anl10_*`; that surface is saturated
  at Sharpe ~1.2-1.4 with Fitness <= 1.02.
- Do not re-run `pv37_snapshot1_volume*` at decay 0 (structurally `HIGH_TURNOVER`) or at
  40-60% turnover under decay 5. If reused, target the low-turnover corner with double
  smoothing.
- Do not use `adjfactor`, `pv37_low_14`, `pv47_spret`-family or `*_currency_code` /
  `expected_report_*` variance fields as alpha inputs.
- Prefer the `anl69` + `ts_quantile(..., 63)` cluster for the next EUR iteration, and state
  the single mechanism changed relative to the recorded expressions.
- Do not re-run single-field grids on `anl15_*` or `anl10_*` in USA: 1,226 + 318 blocks of the
  Oct-8/09 sessions top out at Sharpe 1.23 and 1.21, both just under the bar.
- The best USA surface on record is the implied-volatility family (`implied_volatility_call_120
  - implied_volatility_put_120` plus an IV-to-realised-vol rank, `group_neutralize`d on cap or
  volatility buckets): Sharpe 2.21-2.61 with Fitness 1.07-1.88. It fails only
  `CONCENTRATED_WEIGHT` + `LOW_SUB_UNIVERSE_SHARPE` at decay 4, 6 and 8, so repair the book
  construction (finer buckets, truncation, cap-neutral grouping) rather than the decay.
- Regional Sharpe bars are not uniform: AMR/TOP600 blocks at Sharpe 1.4-1.6 still fail
  `LOW_SHARPE`, so the workspace's 1.25 assumption cannot be reused across regions.
- KOR/TOP600 `LOW_2Y_SHARPE` fails 96.5% of blocks while `HIGH_TURNOVER` is rare, so the KOR
  gap is the 2-year window; `normalize(ts_backfill(oth176_lmt_close_eq_score, 21))`
  (2.36 / 1.67) is the closest block in this workspace to a single-check failure.
