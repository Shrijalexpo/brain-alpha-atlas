# Failed Checks

The check list is the real gate. Two alphas with the same Sharpe can have completely different
fates depending on which checks they clear. This page covers every check that appears in the
recorded simulations, what it means, what to inspect, and when to stop.

## How to read the check names

The platform reports a set of failed checks per simulation. In this repository's raw sweep data
the sets are abbreviated to codes (`F1`, `F2`, …), and **the code-to-check mapping is per file** —
the same code means different things in different dumps. Always resolve codes through their own
file's legend, never across files. `[Observed]`

## The checks

### `LOW_SHARPE`

**Means:** the risk-adjusted return is below the platform's bar for this region and universe.
`[Platform]`

**Inspect:** the Sharpe number, but also the region — the bar is not uniform. Recorded AMR/TOP600
blocks with Sharpe 1.4–1.6 still failed this check. `[Observed]`

**Likely causes and fixes:** the signal is weak (change the idea or field); the direction is
wrong (question the construction before inverting); the alpha is diluted by too many terms.

**When to stop:** if several controlled changes to the *idea* (not the settings) leave Sharpe
near or below the bar, the field family is the problem — move on. `[Notes]`

### `LOW_FITNESS`

**Means:** the composite quality metric is below 1.0. Since Fitness divides by turnover and
multiplies by the square root of returns, this check encodes "the signal is not worth what it
costs to trade." `[Notes]`

**Inspect:** returns and turnover together, plus margin.

**Likely causes and fixes:**

| Sub-pattern | Fix |
|---|---|
| Turnover high | Smooth the fastest component (higher Decay, `ts_mean`, `ts_decay_linear`, `hump`) |
| Turnover already low, returns small | Strengthen the signal selectively; smoothing further will not help |
| Margin low | The edge per trade is thin; reconsider the horizon |

This is the most common failure in the recorded data — it appears in five of the six pages of the
latest 5,546-block bundle. `[Observed]`

### `LOW_2Y_SHARPE`

**Means:** the alpha does not perform well in the most recent two-year window, even if the full
period is strong. `[Platform]`

**Inspect:** the recent portion of the PnL curve. Is the performance concentrated in older data?

**Likely causes and fixes:** regime dependence, or a relationship that has decayed. There is no
setting that fixes this. Candidate approaches: re-examine whether the signal is still
economically current, test a shorter or differently-anchored window, or accept that the idea is
time-bound.

**When to stop:** this is the least fixable check in the recorded record. It was the *only*
failure for the best block in a 5,546-block bundle (Sharpe 2.36 / Fitness 1.67, single failed
check), and it dominates whole regions — in KOR/TOP600 it failed 761 of 789 blocks (96.5%).
`[Observed]` Treat persistent `LOW_2Y_SHARPE` as evidence about the idea, not about the
expression.

### `LOW_SUB_UNIVERSE_SHARPE`

**Means:** the alpha does not survive when measured on a smaller universe. It is a robustness
proxy: if the edge lives only in the long tail of illiquid names, the smaller universe loses it.
`[Platform]`

**Inspect:** whether the biggest contributions come from small or thinly traded names.

**Likely causes and fixes:** concentration in the tail; over-reliance on names that would not be
tradeable at size. Fixes worth testing: a broader final ranking, `winsorize` or `truncate`,
different neutralisation groups, or simply testing the idea on the smaller universe directly.

**When to stop:** if the signal only exists in the tail, that is not a robustness problem you can
patch — it is a different, more fragile alpha. This check and `CONCENTRATED_WEIGHT` failed
together across decay 4, 6 and 8 in the USA implied-volatility family, which is strong evidence
the cause is construction, not smoothing. `[Observed]`

### `CONCENTRATED_WEIGHT`

**Means:** too much of the book sits in too few instruments. `[Platform]`

**Inspect:** the long/short counts and the weight distribution. A book of 1,900 long against
1,200 short is fine; 12 long against 218 short is a red flag. `[Observed]`

**Likely causes and fixes:** few instruments receiving extreme scores; an unnormalised signal; a
grouping scheme that leaves few names per group; a signal that is zero for most of the universe.

Fixes in priority order: `[Platform]` `[Notes]`

1. Rank or winsorise the final signal to remove extremes.
2. Use a wider universe so groups have enough members.
3. Check the grouping: very small groups concentrate weight.
4. Apply truncation (all recorded work uses 0.08).
5. Improve coverage if NaNs are shrinking the tradeable set.

**When to stop:** if the alpha only clears concentration by discarding most of its signal, the
underlying idea is probably too narrow to be a portfolio alpha.

### `HIGH_TURNOVER` / `LOW_TURNOVER`

**Means:** turnover is outside the acceptable band (roughly 1%–70%). `[Platform]`

**Inspect:** which component of the expression changes fastest. Fast price/volume and `*_fast_d1`
sentiment fields are the usual culprits.

**Likely causes and fixes:** for high turnover, decay and smoothing (`ts_mean`,
`ts_decay_linear`, `hump`, `trade_when`). For low turnover, the alpha barely trades — its signal
is too static to react to anything, and very low turnover is rarely a good sign in a
cross-sectional alpha.

A recorded example of the high-turnover failure: a sentiment-plus-buzz composite reached Sharpe
1.38 but 87.5% turnover and Fitness 0.44. `[Observed]`

### `IS_LADDER_SHARPE`

**Means:** a consistency test across successive in-sample windows: the alpha must clear a
per-window Sharpe bar at several horizons, not just on the full period. `[Notes]`

**Inspect:** whether performance is spread across the windows or concentrated in one.

**Why it matters here:** this is a consultant-stage check and it is active in ordinary
simulations — it fired in 96 of 174 blocks (55%) of the USA page of the 2026-10 bundle, and it
appears in the EUR and GLB pages too. `[Observed]` In practice, a strong headline Sharpe is now
routinely stopped by consistency and book-quality checks rather than by the headline metric.

**When to stop:** an alpha that cannot hold a bar across successive windows is a regime alpha.
More expression engineering will not change that.

### `CLUSTER_TEST`

**Means:** a check on how the alpha clusters with related ideas — a form of diversity
requirement. `[Notes]`

**Observed:** 27 blocks in the EUR page of the 2026-10 bundle. `[Observed]`

### Region-specific Sharpe checks

**Mean:** the global/ALL scope is assessed per sub-region, not only in aggregate. `[Observed]`

Checks observed in the ALL/LARGE pages: `LOW_GLB_APAC_SHARPE`, `LOW_ASI_JPN_SHARPE`,
`LOW_GLB_AMER_SHARPE`, `LOW_GLB_EMEA_SHARPE`, plus `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` and
`LOW_ROBUST_UNIVERSE_RETURNS`. `[Observed]`

**Practical consequence:** a region-agnostic alpha must work in Asia/Japan as well as the
Americas — good performance in one region is not evidence for an ALL-scope alpha. See
[Regions and universes](12-regions-and-universes.md) and [Advanced topics](14-advanced.md).

### Self-correlation

**Means:** the alpha is too similar to alphas that already exist. Metrics can be excellent and
the alpha still be rejected. `[Platform]`

**Inspect:** which existing family it resembles — in the recorded cases, a
quality/improvement-plus-reversal backbone.

**Fixes:** change the economic backbone, not the window. Cosmetic edits do not move
correlation. Four recorded experiments failed on exactly this after clearing the metrics,
including one at Sharpe 1.76 / Fitness 1.21 with a self-correlation of 0.88. `[Observed]`

**When to stop:** if the only way to reduce correlation is to weaken the alpha, the honest move is
to find a different signal — which is also why the platform pairs self-correlation with a
production-pool correlation gate. `[Notes]`

## Error conditions (not check failures)

| Error | Cause | Fix |
|---|---|---|
| `Event input error` | Vector/event field used directly in a matrix operator | Reduce with `vec_avg` / `vec_sum` first |
| Universe field rejected as a boolean | Universe objects are not events | Use a data-derived condition |
| Division by zero | Unguarded denominator | `divide(x, add(y, 0.0001))` |
| Unit warning | Combining fields with different units | Use ratios or normalise first; do not ignore silently |

Both `ERROR` records in this repository are the same mistake: `ts_delta` applied directly to an
event/vector estimate field. `[Observed]`

## A diagnosis order that works

```text
1. Is the expression valid?          -> syntax, types, units, coverage
2. Is Sharpe credible?               -> out-of-sample, steady PnL shape
3. Is Fitness failing on cost or on weakness?  -> turnover vs returns
4. Is the book concentrated?         -> weight distribution and counts
5. Is it robust?                     -> sub-universe, recent window, ladder
6. Is it original?                   -> self-correlation, then production pool
```

Work down the list. Fixing a lower item while an upper one is broken wastes simulations.

Next: [Improving alphas](09-improving-alphas.md).
