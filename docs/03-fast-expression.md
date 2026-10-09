# Fast Expression

Fast Expression is BRAIN's expression language: close enough to pseudocode that you can focus
on the idea rather than the syntax. `[Platform]` This page covers the rules, the patterns worth
reusing, and the mistakes that make expressions fail.

An expression is built from three things: `[Platform]`

- **Data fields** — named series such as `close`, `returns`, `cap`, `operating_income`.
- **Operators** — transformations such as `rank`, `ts_mean`, `group_neutralize`.
- **Numbers** — constants, including window lengths like `126` or `252`.

## Syntax rules that matter

| Rule | Detail |
|---|---|
| Statements are separated by `;` | `a = rank(x); a + 1` |
| The **last** statement is the alpha | Everything before it is definition |
| No trailing semicolon needed on the last statement | It is tolerated, but not required |
| Block comments use `/* … */` | Not `#` or `//` |
| Comparisons return booleans | `volume > adv20` is usable as a condition |
| No classes, objects, pointers or user functions | It is not a general-purpose language |
| Parentheses matter | `a + b / c` is `a + (b / c)` |

An expression with two definitions and a final statement — the most readable form for anything
non-trivial:

```text
iv_difference = implied_volatility_call_120 - implied_volatility_put_120;
hvol_group = bucket(rank(historical_volatility_120), range="0.1,1,0.1");
group_neutralize(iv_difference, hvol_group)
```

The first two statements only define intermediate values. BRAIN simulates the third — the last
one. `[Platform]`

## The shape of most working expressions

```text
normalise(raw economic quantity)  ->  make it comparable across instruments
```

Three normalisation families, in rough order of use: `[Notes]`

| Family | Operators | When to use |
|---|---|---|
| Cross-sectional | `rank`, `zscore`, `quantile`, `normalize`, `winsorize`, `scale` | Making today's scores comparable between instruments |
| Time-series | `ts_rank`, `ts_zscore`, `ts_scale`, `ts_quantile`, `ts_av_diff` | Comparing an instrument to its own history |
| Group-relative | `group_rank`, `group_zscore`, `group_scale`, `group_neutralize` | Comparing within peers (industry, size bucket) |

The choice is not cosmetic. In the EUR sweeps, slow analyst level fields responded to
time-series scaling rather than plain ranking — `ts_scale(x, 63)` and `ts_quantile(x, 63)`
consistently outperformed `rank(ts_backfill(x, 21))` on the same fields. `[Observed]`

## Building a first expression

Start from a ratio of two economically related quantities, then make it comparable.

```text
/* Raw level: mostly a size signal, weak on its own */
operating_income

/* Ratio: profitability per unit of assets */
operating_income / assets

/* Comparable across instruments and robust to outliers */
group_rank(operating_income / assets, industry)
```

Why the progression matters: raw fundamental levels are dominated by company size — the
recorded early experiments produced Sharpe below 0.5 from raw `operating_income` under
`ts_rank`, `ts_mean` and `ts_delta`. `[Observed]` Ratios remove size; ranking removes outliers.

## Combining components

When you combine terms, standardise them first so one component's scale does not dominate.

```text
zscore(rank(component_a) + 0.5 * rank(component_b) + 0.5 * rank(component_c))
```

Two cautions from the recorded work: `[Observed]`

- **Stacking similar factors dilutes.** A large quality/value composite in the early records
  produced negative Sharpe. Adding a fifth similar rank is rarely better than improving the
  first one.
- **Keep coefficients meaningful.** If a term needs a weight of 0.05 to avoid hurting the
  result, that is evidence it does not belong.

## Conditions and events

```text
trade_when(condition, alpha, exit_condition)
```

`trade_when` updates the alpha only when the condition holds, otherwise it keeps the previous
value; the third argument can close positions. `[Platform]`

The first argument must be a **boolean event**. This is a real and common error: using a
universe field such as `top2000` as the first argument fails, because a universe object is not
an event. `[Observed]` Use a price/volume or fundamental condition instead:

```text
/* Good: a boolean derived from data */
trade_when(volume > adv20, rank(-returns), -1)

/* Bad: top2000 is a universe field, not an event */
trade_when(top2000, rank(-returns), -1)
```

A conditional gate can also be an alpha in its own right — in the USA sweep, a gated expression
reached 2.17 Sharpe / 1.10 Fitness at 30% turnover (recorded as `PENDING`, so unverified):
`[Observed]`

```text
rank(ts_rank(operating_income / cap, 250)) > 0.5 ? 1 : rank(-ts_delta(close, 2))
```

## Vector and event fields

Some datasets return a **vector** per instrument — several values per day, often events.
Matrix operators (`rank`, `ts_mean`) do not accept them directly. Convert to a matrix first
with a `vec_*` operator: `[Platform]`

```text
/* Wrong: vector field into a matrix operator */
ts_delta(eps_estimate_value, 5)

/* Right: reduce the vector to a matrix first */
ts_delta(vec_avg(eps_estimate_value), 5)
```

Two recorded `ERROR` results came from exactly this mistake (direct `ts_delta` on
`eps_estimate_value` and `sales_estimate_value`). `[Observed]` The same rule applies to any
event-like field: reduce it to one number per instrument per day before using time-series
operators.

## Division and units

Division by zero errors, so guard denominators with a small epsilon when the denominator could
be zero or negative: `[Platform]`

```text
divide(x, add(y, 0.0001))
```

Unit warnings usually appear when fields with different units are added — `close + cap` is
meaningless as a quantity. Prefer ratios over sums for combining fundamentals, and treat unit
warnings as a signal that the expression's economics need a second look rather than as noise to
ignore. `[Platform]`

## Coverage and NaNs

Low coverage shows up as NaNs, which can silently shrink the tradeable book. Fix coverage at
the field level: `[Platform]`

| Operator | Use |
|---|---|
| `ts_backfill(x, lookback=d, k=1)` | Fill from the most recent valid value |
| `kth_element(x, d, k)` | Take the k-th value over a window |
| `group_backfill(x, group, d, std=4)` | Fill within a peer group |
| `ts_count_nans(x, d)` | Measure how bad the coverage actually is |

`ts_backfill(field, 21)` is the default first step in almost every sweep in this repository.
It establishes coverage; it is not itself a strategy — the transform applied on top is what
decides the result. `[Observed]`

## Common mistakes and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| `Event input error` | Vector/event field used directly in a matrix operator | Wrap in `vec_avg` / `vec_sum` first |
| Universe field rejected as a condition | Universe objects are not events | Use a data-derived boolean |
| Division by zero | Unguarded denominator | `divide(x, add(y, 0.0001))` |
| Unit warning | Adding fields with different units | Use a ratio, or normalise both first |
| Expression runs but is all NaN | Field has poor coverage | `ts_backfill` / `group_backfill`, or pick another field |
| Signal reversed | Sign convention wrong for the economic idea | Check whether high values should be long or short before flipping |

The last row is the trap worth naming: **do not reverse a signal just to improve a number.** If
the economics say high values should outperform and the alpha only works inverted, that is a
reason to question the construction, not to ship the inverse. `[Notes]`

Next: [Operators](04-operators.md).
