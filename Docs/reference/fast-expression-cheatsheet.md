# Fast Expression Cheat Sheet

Concise one-page reference for writing WorldQuant BRAIN Fast Expressions. For full operator tables, see [Categorized Operator Reference](../05-fast-expression-language/operator-reference.md).

## 1. Core Syntax Rules

```text
/* 1. Block comments use C-style slash-star */
/* 2. Separate intermediate assignments with semicolons (;) */
/* 3. The LAST statement is the Alpha simulated by BRAIN */

val_leg = rank(ts_rank(ebitda / enterprise_value, 126));
growth_leg = rank(ts_rank(sales_growth, 126));
rev_leg = rank(ts_mean(-returns, 5));
cap_bucket = bucket(rank(cap), range="0.1,1,0.1");

group_neutralize(val_leg + growth_leg + rev_leg, cap_bucket)
```

## 2. Most Frequently Used Operators by Task

| Task | Idiom |
|---|---|
| **Cross-sectional rank (`0..1`)** | `rank(x)` |
| **Cross-sectional z-score** | `zscore(x)` |
| **Winsorize extreme tails** | `winsorize(x, std=4)` |
| **Backfill quarterly / periodic gaps** | `ts_backfill(x, 21)` or `ts_backfill(x, 63)` |
| **Position within own history (`0..1`)** | `ts_rank(x, 126)` or `ts_scale(x, 63)` |
| **Gaussian time-series quantile** | `ts_quantile(x, 63)` |
| **Smooth fast daily noise** | `ts_mean(x, 5)` or `ts_decay_linear(x, 10)` or `hump(x, hump=0.01)` |
| **Multi-quarter change** | `ts_delta(x, 63)` or `ts_av_diff(x, 63)` |
| **Convert Vector field to Matrix** | `vec_avg(x)`, `vec_sum(x)`, `vec_stddev(x)`, `vec_ir(x)` |
| **Peer-group rank or neutralization** | `group_rank(x, industry)` or `group_neutralize(x, subindustry)` |
| **Double neutralization (`Country x Industry`)** | `group_neutralize(x, group_cartesian_product(country, industry))` |
| **Conditional trading on boolean event** | `trade_when(volume > adv20, alpha, -1)` |
| **Safe division guard** | `divide(x, add(y, 0.0001))` |

## 3. Standard Lookback Windows

- `5` = 1 trading week
- `21` = 1 trading month
- `63` = 1 fiscal quarter
- `126` = 6 months (2 quarters)
- `252` = 1 trading year (4 quarters)
