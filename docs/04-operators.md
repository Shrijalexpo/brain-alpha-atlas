# Operators

The operators worth knowing, grouped by what they are for. Definitions and signatures follow the
platform's operator reference; the practical notes and failure modes come from the experiments
recorded in this repository. `[Platform]` `[Observed]`

See also [Fast Expression](03-fast-expression.md) for how these are combined into a valid
expression.

## How to choose an operator

Work backwards from the problem, not forwards from the operator list.

| Problem | Operators to reach for |
|---|---|
| Scores are on wildly different scales | `rank`, `zscore`, `quantile`, `normalize` |
| Extremes are dominating | `winsorize`, `truncate`, `rank`, `quantile` |
| Turnover is too high | `hump`, `ts_decay_linear`, `ts_mean`, `trade_when`, higher Decay |
| Field has gaps | `ts_backfill`, `kth_element`, `group_backfill` |
| Signal should be peer-relative | `group_rank`, `group_zscore`, `group_scale`, `group_neutralize` |
| Idea is about change over time | `ts_delta`, `ts_av_diff`, `ts_zscore`, `ts_rank` |
| Vector/event field needs to be a series | `vec_avg`, `vec_sum`, `vec_choose`, `vec_ir` |
| Two series should be compared | `ts_corr`, `ts_covariance`, `ts_regression` |

## Cross-sectional operators

They act across instruments on one day: "how does this stock compare with all others today?"

| Operator | Meaning | Notes |
|---|---|---|
| `rank(x, rate=2)` | Rank across instruments, 0 → 1 | The workhorse normaliser; reduces outlier influence |
| `zscore(x)` | Cross-sectional standard score | Standardises for combining components |
| `normalize(x, useStd=false, limit=0.0)` | Subtracts the cross-sectional mean; optionally divides by std and clamps | Market-centring plus outlier control |
| `quantile(x, driver=gaussian, sigma=1.0)` | Maps ranks onto a target distribution | Reshapes without changing order |
| `winsorize(x, std=4)` | Clamps to N standard deviations | Typical values 2–5 |
| `scale(x, scale=1, longscale=1, shortscale=1)` | Rescales so the sum of absolute weights hits a target | Sizing, not signal |

`rank` is the operator you will use most. Because it is monotone, it never changes which
instrument is "best" — it only removes the influence of how much better it was. That is why
ranking almost always improves robustness while leaving the ordering intact. `[Platform]`

## Time-series operators

They act on one instrument's own history: "is today's value high or low for *this* stock?"

| Operator | Meaning | Typical use |
|---|---|---|
| `ts_mean(x, d)` | Rolling mean | Smoothing; the simplest turnover reducer |
| `ts_rank(x, d, constant=0)` | Rank of today within the last `d` days | Time-series normalisation |
| `ts_zscore(x, d)` | Standardised distance from the recent mean | "Surprise" measures |
| `ts_scale(x, d, constant=0)` | Rescales the window to 0–1 | Slow fields that need their own range |
| `ts_quantile(x, d, driver="gaussian")` | `ts_rank` through an inverse CDF | Distribution reshaping |
| `ts_delta(x, d)` | `x - ts_delay(x, d)` | Change, momentum, improvement |
| `ts_av_diff(x, d)` | `x - ts_mean(x, d)`, NaNs ignored | Deviation from the recent average |
| `ts_std_dev(x, d)` | Rolling standard deviation | Volatility, normalisation |
| `ts_decay_linear(x, d, dense=false)` | Linear decay weighting | Turnover reduction with shape control |
| `hump(x, hump=0.01)` | Limits the size and number of changes | Turnover control / noise filter |
| `ts_delay(x, d)` | Value `d` days ago | Lags |
| `ts_sum(x, d)` | Rolling sum | Counts and totals |
| `ts_corr(x, y, d)` | Rolling Pearson correlation | Relationship strength between two series |
| `ts_covariance(y, x, d)` | Rolling covariance | Co-movement |
| `ts_regression(y, x, d, lag=0, rettype=0)` | Rolling regression output | Beta / residual / slope ideas |
| `ts_arg_max(x, d)` / `ts_arg_min(x, d)` | Days since the window's max / min | Position-in-range |
| `ts_count_nans(x, d)` | Count of NaNs in the window | Coverage diagnostics |
| `last_diff_value(x, d)` | Most recent different value | Slow-changing data |
| `days_from_last_change(x)` | Days since the value last changed | Detecting stale data |
| `ts_step(1)` | Day counter | Time index |

The window length is part of the idea, not a free parameter to tune until the number looks
good. `ts_mean(x, 5)` and `ts_mean(x, 63)` are different hypotheses about how fast the signal
decays, not two settings of the same hypothesis. `[Notes]`

A concrete illustration from the recorded work: smoothing a reversal component with
`ts_mean(-returns, 5)` was what pushed an alpha's Fitness above 1.0 and made it submittable,
while a longer-window variant of the same idea weakened it. `[Observed]`

## Group operators

They act across instruments but inside peer groups — industry, sector, size bucket, country.

| Operator | Meaning | Notes |
|---|---|---|
| `group_rank(x, group)` | Rank within each group | The natural form for peer-relative fundamentals |
| `group_zscore(x, group)` | Z-score within each group | Comparable within group |
| `group_scale(x, group)` | Normalise within group | |
| `group_neutralize(x, group)` | Subtract the group mean | Explicit neutralisation inside the expression |
| `group_mean(x, weight, group)` | Group-level mean | Aggregation |
| `group_backfill(x, group, d, std=4.0)` | Fill NaNs from the group's winsorised mean | Coverage repair |

Two cautions backed by recorded evidence: `[Observed]`

- **Neutralising twice.** If you use the settings-level `Neutralization`, do not also neutralise
  inside the expression with the same grouping — set settings neutralization to `None` when you
  neutralise manually. `[Platform]`
- **Grouping is not a Sharpe source.** `group_count`, `group_sum`, `group_std_dev` and
  `group_neutralize` used as wrappers over volume or grouping fields added turnover and
  `CONCENTRATED_WEIGHT` without adding Sharpe in the EUR sweeps (Sharpe 0.2–0.7 at 48–90%
  turnover).

## Transformational operators

| Operator | Meaning | Notes |
|---|---|---|
| `bucket(rank(x), range="0,1,0.1")` | Custom groups from ranked values | Size buckets, custom neutralisation |
| `bucket(rank(x), buckets="2,5,6,7,10")` | Buckets from explicit cut points | Non-uniform buckets |
| `trade_when(x, y, z)` | Update the alpha only when `x` holds; `z` closes | Events and turnover control |
| `densify(x)` | Reduce the number of groups | Efficiency for `bucket`-heavy expressions |

The bucket-based neutralisation pattern is the mechanism behind the strongest USA result
recorded here — an implied-volatility dispersion signal neutralised inside cap deciles: `[Observed]`

```text
cap_group = bucket(rank(cap), range="0.1,1,0.1");
group_neutralize(iv_signal, cap_group)
```

Note what that did *not* fix: the same expression still failed `CONCENTRATED_WEIGHT`, so
bucketing plus explicit neutralisation is not a substitute for controlling the final book.

## Arithmetic and logical operators

| Operator | Meaning |
|---|---|
| `abs(x)`, `sign(x)` | Absolute value; sign |
| `add(x, y)`, `subtract(x, y)`, `multiply(x, y)`, `divide(x, y)` / `+ - * /` | Arithmetic; `filter=true` treats NaNs as 0 |
| `log(x)`, `sqrt(x)`, `power(x, y)` | Transforms; `sqrt` is `power(x, 0.5)` |
| `signed_power(x, y)` | Power that preserves the sign of `x` — use instead of `power` when sign matters |
| `inverse(x)` | `1 / x`; guard against zero |
| `max(x, y, …)`, `min(x, y, …)` | Element-wise extremes |
| `reverse(x)` | `-x` |
| `and`, `or`, `not`, `if_else(cond, a, b)`, `is_nan(x)` | Logic and conditions |
| `> < >= <= == != ` | Comparisons producing booleans |

## Vector operators

Vector fields carry more than one value per instrument per day. Reduce them before using matrix
operators. `[Platform]`

| Operator | Meaning |
|---|---|
| `vec_avg(x)` | Mean of the vector |
| `vec_sum(x)` | Sum |
| `vec_max(x)` / `vec_min(x)` | Extremes |
| `vec_count(x)` | Number of elements |
| `vec_stddev(x)` | Standard deviation |
| `vec_ir(x)` | Mean divided by standard deviation |
| `vec_powersum(x, constant=2)` | Sum of powers |
| `vec_range(x)` | Max − min |
| `vec_choose(x, nth=k)` | Select the k-th element |
| `vec_percentage(x, percentage=0.5)` | Percentile |
| `vec_skewness(x)` / `vec_kurtosis(x)` | Shape of the distribution |
| `vec_norm(x)` | Sum of absolute values |

Typical pattern, taken from a recorded sweep: `ts_sum(vec_avg(nws12_afterhsz_sl), 60)` —
reduce the vector to a mean, then smooth it. `[Observed]`

## Practical rules of thumb

- Normalise before combining. Unnormalised components let the largest-scale one dominate.
  `[Notes]`
- Prefer `rank` over raw values for anything cross-sectional; prefer `ts_*` normalisation when
  the idea is relative to the instrument's own history. `[Notes]`
- Guard every denominator: `divide(x, add(y, 0.0001))`. `[Platform]`
- Reduce turnover at the fastest component first, not by dropping the signal. `[Observed]`
- When a group operator is added and Sharpe does not move but turnover and concentration do,
  remove it. `[Observed]`
- Operators unlocked at higher platform levels (Expert, Master, Grandmaster) are outside the
  scope of the reference captured here. `[Platform]`

Next: [Data and fields](05-data-and-fields.md).
