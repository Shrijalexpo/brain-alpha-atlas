# WorldQuant BRAIN Operator Reference

Source: BRAIN Learn > Operators, captured through Computer Use on 2026-07-26.

Raw source:

```text
Operators/worldquant_brain_operators_raw_capture.txt
```

Note: BRAIN says more complex operators unlock at Expert, Master, and Grandmaster Genius levels. This file records the base operators visible in the captured page.

## Arithmetic Operators

| Operator | Meaning | Notes |
|---|---|---|
| `abs(x)` | Absolute value. | Removes negative sign. |
| `add(x, y, filter=false)`, `x + y` | Element-wise addition. | `filter=true` treats NaNs as 0 before summing. |
| `densify(x)` | Converts grouping fields with many buckets into fewer available buckets. | Useful for efficient group operations. |
| `divide(x, y)`, `x / y` | Division. | Division by zero errors; use `divide(x, add(y, 0.0001))` style epsilon guard. |
| `inverse(x)` | Reciprocal, `1 / x`. | Add epsilon to avoid zero division. |
| `log(x)` | Natural logarithm. | Use on positive-valued data. |
| `max(x, y, ..)` | Maximum across inputs. | At least 2 inputs. |
| `min(x, y, ..)` | Minimum across inputs. | At least 2 inputs. |
| `multiply(x, y, ..., filter=false)`, `x * y` | Element-wise multiplication. | `filter=true` treats NaNs as 0 before multiplication. |
| `power(x, y)` | `x` raised to `y`. | Can drop sign for non-integer powers. |
| `reverse(x)` | `-x`. | Direction flip. |
| `sign(x)` | `+1`, `-1`, or `0` by sign. | NaN stays NaN. |
| `signed_power(x, y)` | Power transform preserving sign of `x`. | Use instead of `power` when sign matters. |
| `sqrt(x)` | Non-negative square root. | Equivalent to `power(x, 0.5)`; use `signed_power(x, 0.5)` if sign should be retained. |
| `subtract(x, y, filter=false)`, `x - y` | Left-to-right subtraction. | `filter=true` treats NaNs as 0. |

## Logical Operators

| Operator | Meaning |
|---|---|
| `and(input1, input2)` | Returns 1 if both inputs are true, else 0. |
| `if_else(input1, input2, input3)` | If condition is true returns `input2`, else `input3`. |
| `input1 < input2` | Less-than condition. |
| `input1 <= input2` | Less-than-or-equal condition. |
| `input1 == input2` | Equality condition. |
| `input1 > input2` | Greater-than condition. |
| `input1 >= input2` | Greater-than-or-equal condition. |
| `input1 != input2` | Not-equal condition. |
| `is_nan(input)` | Returns 1 if input is NaN, else 0. |
| `not(x)` | Logical negation. |
| `or(input1, input2)` | Returns 1 if either input is true. |

## Time-Series Operators

| Operator | Meaning | Practical use |
|---|---|---|
| `days_from_last_change(x)` | Days since the value last changed. | Detect update frequency or stale data. |
| `hump(x, hump=0.01)` | Limits amount and magnitude of changes. | Turnover reduction. |
| `kth_element(x, d, k, ignore="NaN")` | K-th value over a lookback. | Backfilling and robust missing-data handling. |
| `last_diff_value(x, d)` | Most recent different value over `d` days. | Slow-changing data. |
| `ts_arg_max(x, d)` | Days since max in last `d` days. | Momentum/position in range. |
| `ts_arg_min(x, d)` | Days since min in last `d` days. | Reversion/range timing. |
| `ts_av_diff(x, d)` | `x - ts_mean(x, d)` ignoring NaNs. | Deviation from recent average. |
| `ts_backfill(x, lookback=d, k=1)` | Fill NaNs with recent valid value. | Improve low coverage. |
| `ts_corr(x, y, d)` | Pearson correlation over `d` days. | Relationship between two variables. |
| `ts_count_nans(x, d)` | Counts NaNs over `d` days. | Coverage quality. |
| `ts_covariance(y, x, d)` | Covariance over `d` days. | Co-movement. |
| `ts_decay_linear(x, d, dense=false)` | Linear decay/smoothing over `d`. | Reduce noise/turnover. |
| `ts_delay(x, d)` | Value from `d` days ago. | Lagged values. |
| `ts_delta(x, d)` | `x - ts_delay(x, d)`. | Change/momentum. |
| `ts_mean(x, d)` | Rolling mean. | Smoothing. |
| `ts_product(x, d)` | Product over `d` days. | Compounding/growth. |
| `ts_quantile(x, d, driver="gaussian")` | `ts_rank` transformed by inverse CDF. | Distribution reshaping. |
| `ts_rank(x, d, constant=0)` | Current value's rank within own history. | Time-series normalization. |
| `ts_regression(y, x, d, lag=0, rettype=0)` | Regression output over a window. | Beta/residual/slope style ideas. |
| `ts_scale(x, d, constant=0)` | Scales time series to 0-1 over window. | Normalize own history. |
| `ts_std_dev(x, d)` | Rolling standard deviation. | Volatility and normalization. |
| `ts_step(1)` | Day counter. | Time index. |
| `ts_sum(x, d)` | Rolling sum. | Counts and totals. |
| `ts_zscore(x, d)` | Distance from recent mean in standard deviations. | Standardized surprise. |

## Cross-Sectional Operators

| Operator | Meaning | Practical use |
|---|---|---|
| `normalize(x, useStd=false, limit=0.0)` | Centers daily cross-section by subtracting market mean; optionally divides by cross-sectional std and clamps. | Market centering and outlier control. |
| `quantile(x, driver=gaussian, sigma=1.0)` | Ranks and maps values to a distribution. | Outlier reduction and distribution shaping. |
| `rank(x, rate=2)` | Cross-sectional rank from 0 to 1. | Core normalizer. |
| `scale(x, scale=1, longscale=1, shortscale=1)` | Scales so sum absolute weights equals a target. | Position sizing and long/short scaling. |
| `winsorize(x, std=4)` | Limits values to a number of std devs from mean. | Outlier control; typical std 2-5. |
| `zscore(x)` | Cross-sectional z-score. | Standardization. |

## Vector Operators

Visible on operator page:

| Operator | Meaning |
|---|---|
| `vec_avg(x)` | Mean of vector elements. |
| `vec_sum(x)` | Sum of vector elements. |

Additional vector operators from documentation:

| Operator | Meaning |
|---|---|
| `vec_choose(x, nth=k)` | Choose k-th item, indexed at 0. |
| `vec_count(x)` | Number of vector elements. |
| `vec_ir(x)` | Mean divided by standard deviation. |
| `vec_kurtosis(x)` | Kurtosis. |
| `vec_max(x)` | Maximum. |
| `vec_min(x)` | Minimum. |
| `vec_norm(x)` | Sum of absolute values. |
| `vec_percentage(x, percentage=0.5)` | Percentile. |
| `vec_powersum(x, constant=2)` | Sum of powers. |
| `vec_range(x)` | Max minus min. |
| `vec_skewness(x)` | Skewness. |
| `vec_stddev(x)` | Standard deviation. |

## Transformational Operators

| Operator | Meaning | Practical use |
|---|---|---|
| `bucket(rank(x), range="0,1,0.1", skipBoth=False, NaNGroup=False)` | Creates custom groups from ranked values. | Size buckets and custom neutralization groups. |
| `bucket(rank(x), buckets="2,5,6,7,10", skipBoth=False, NaNGroup=False)` | Creates buckets using selected cut points. | Custom grouping. |
| `trade_when(x, y, z)` | Changes alpha only when condition `x` is met, otherwise keeps previous value; can close positions using `z`. | Event alphas and turnover control. |

## Group Operators

| Operator | Meaning | Practical use |
|---|---|---|
| `group_backfill(x, group, d, std=4.0)` | Fill NaNs within group using winsorized mean over `d`. | Improve coverage for sparse fields. |
| `group_mean(x, weight, group)` | Harmonic mean within group. | Group-level comparisons. |
| `group_neutralize(x, group)` | Subtracts group mean from each value. | Remove group exposure. |
| `group_rank(x, group)` | Ranks within each group from 0 to 1. | Peer-relative ranking. |
| `group_scale(x, group)` | Normalizes values within each group. | Comparable group signals. |
| `group_zscore(x, group)` | Z-score within group. | Peer-relative standardization. |

## High-Value Usage Rules

- Use `rank`, `zscore`, `normalize`, `winsorize`, and `quantile` to control scale and outliers.
- Use `ts_mean`, `ts_decay_linear`, and `hump` when Turnover is too high.
- Use `ts_backfill`, `kth_element`, or `group_backfill` when coverage is weak.
- Use `group_rank`, `group_zscore`, or `group_neutralize` for peer-relative fundamental signals.
- Use epsilon guards in denominators: `divide(x, add(y, 0.0001))`.
- Convert vector fields to matrix values with `vec_*` operators before using normal matrix operators.

