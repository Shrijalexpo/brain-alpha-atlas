# Fast Expression Cheat Sheet

This file stores operator notes from the WorldQuant BRAIN tutorial conversation.

For the curated official operator list captured from BRAIN Learn, see:

```text
Operators/worldquant_brain_operator_reference.md
```

## Basic Data Fields

Common Price Volume fields:

```text
open
high
low
close
volume
vwap
returns
adv20
```

Fundamental fields discussed:

```text
operating_income
return_equity
return_assets
cashflow_op
enterprise_value
ebitda
assets
debt
current_ratio
sales_growth
dividend
cap
```

## `-x`

Reverses the direction of a signal.

Example:

```text
-returns
```

Meaning:

- Recent winners receive lower values.
- Recent losers receive higher values.
- This is a mean reversion idea.

## `rank(x)`

Cross-sectional rank across stocks on the same date.

Mental model:

```text
Among all stocks today, where does this stock stand?
```

Example with 4 stocks:

```text
Position 1 -> 0.00
Position 2 -> 0.33
Position 3 -> 0.67
Position 4 -> 1.00
```

Formula:

```text
Rank = (Position - 1) / (Total Stocks - 1)
```

Why it is useful:

- Reduces the effect of extreme values.
- Makes signals more comparable across stocks.
- Often improves robustness.

## `zscore(x)`

Normalizes a signal by subtracting mean and dividing by standard deviation.

Use when combining ranked or raw components and you want the final signal standardized.

## `ts_mean(x, n)`

Rolling time-series average over `n` days.

Use for:

- smoothing noisy signals,
- reducing Turnover,
- making daily return signals less jumpy.

Example:

```text
rank(-ts_mean(returns, 5))
```

## `ts_rank(x, n)`

Ranks the current value against the stock's own past `n` observations.

Use for:

- time-series momentum/reversion,
- checking whether a stock's value is high or low relative to itself.

Example:

```text
rank(-ts_rank(returns, 20))
```

## `ts_delta(x, n)`

Change in a field over `n` periods.

Useful for detecting improvement or deterioration.

Caution:

- Fundamental fields update quarterly, so short windows may not add much information.

## `ts_std_dev(x, n)`

Rolling standard deviation over `n` periods.

Use for volatility adjustment:

```text
rank(-returns / ts_std_dev(returns, 20))
```

## `trade_when(event, alpha, exit)`

Trades alpha only when `event` is true.

The first argument must be boolean.

Good:

```text
trade_when(volume > adv20, rank(-returns), -1)
```

Bad:

```text
trade_when(top2000, rank(-returns), -1)
```

Reason:

- `top2000` is a Universe field, not a boolean event.

Official documentation note:

- `trade_when(x, y, z)` changes alpha values only when condition `x` is met, keeps previous values otherwise, and can close positions by assigning NaN under an exit condition.

## `group_neutralize(x, group)`

Neutralizes the signal inside a group.

Used examples:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Purpose:

- Reduce exposure to group effects.
- Compare stocks within comparable buckets.

## `bucket(rank(cap), range="0.1,1,0.1")`

Creates market-cap buckets from ranked `cap`.

Used to compare stocks within size groups.

## Common Patterns

Mean reversion:

```text
rank(-returns)
```

Smoothed mean reversion:

```text
rank(-ts_mean(returns, 5))
```

Volume surprise:

```text
rank(volume / adv20)
```

Cash flow yield:

```text
rank(cashflow_op / enterprise_value)
```

Quality:

```text
rank(return_equity)
rank(return_assets)
rank(cashflow_op / assets)
```

Leverage penalty:

```text
-rank(debt / assets)
```

## Official Docs Additions

Fast Expression rules:

- Use `/* ... */` for block comments.
- Use `;` to separate statements.
- The last statement is the alpha expression used by BRAIN.
- Fast Expression does not use classes, objects, pointers, or ordinary programming-language functions.

Turnover reducers:

```text
hump(x, hump=0.01)
ts_decay_linear(x, d)
ts_mean(x, d)
trade_when(event, alpha, exit)
```

Coverage helpers:

```text
ts_backfill(x, lookback=d, k=1)
kth_element(x, d, k)
group_backfill(x, group, d)
ts_count_nans(x, d)
```

Outlier/scale helpers:

```text
rank(x)
zscore(x)
normalize(x)
winsorize(x, std=4)
quantile(x)
scale(x)
```
