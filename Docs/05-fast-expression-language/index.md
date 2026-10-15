# 05 — Fast Expression Language

## 1. Learning Objectives

By completing this module, you will be able to:

- Write syntactically valid multi-statement **Fast Expression** code using intermediate variable assignments, semicolons, and block comments.
- Apply operator precedence, keyword parameters, and conditional expressions (`condition ? x : y`, `trade_when`).
- Select the right normalization family (cross-sectional, time-series, or group-relative) for any economic hypothesis.
- Diagnose and fix syntax, unit, and data-type validation errors immediately.

## 2. Prerequisites

- [04 — Data Explorer and Datasets](../04-data-explorer-and-datasets/index.md)

## 3. Core Concepts: Fast Expression Syntax Rules

Fast Expression is WorldQuant BRAIN's domain-specific vectorized expression language (`[Platform]`). It is designed to read like mathematical pseudocode evaluated across all instruments and dates simultaneously.

| Syntax Element | Rule | Valid Example | Invalid Example (Error) |
|---|---|---|---|
| **Statement Separator** | Separate intermediate variable assignments with `;`. The **final statement** is the Alpha output simulated by BRAIN (`[Platform]`). | `val = ebitda / enterprise_value; rank(val)` | `val = ebitda / enterprise_value rank(val)` (Missing `;`) |
| **Comments** | Use C-style block comments `/* ... */` (`[Platform]`). | `/* 6-month value rank */ rank(ebitda / enterprise_value)` | `# comment` or `// comment` (Syntax error) |
| **Conditional / Ternary** | `condition ? expr_if_true : expr_if_false` or `if_else(cond, a, b)` (`[Platform]`). | `returns > 0 ? 1 : 0` | `if returns > 0 then 1 else 0` |
| **Keyword Arguments** | Optional operator parameters can be passed by name after positional arguments (`[Platform]`). | `bucket(rank(cap), range="0.1,1,0.1")` | `bucket(rank(cap), 0.1, 1, 0.1)` |
| **Division Guards** | Guard denominators that can hit `0` using `add(denom, 0.0001)` or `max(denom, 0.0001)`. | `divide(operating_income, add(enterprise_value, 0.0001))` | Dividing by a field that frequently equals `0` |
| **No General-Purpose Constructs** | No `for`/`while` loops, `def` functions, classes, or external imports (`[Platform]`). | Vectorized operators (`ts_sum`, `rank`, `group_rank`) | Python-style `def` or list comprehensions (use Python Alphas instead) |

## 4. Step-by-Step Explanations: The Three Normalization Idioms

Raw financial series have incompatible scales, units, and outlier distributions. Almost every working Fast Expression uses one or more of three normalization idioms (`[Notes]`):

### Idiom 1: Cross-Sectional Normalization (`rank`, `zscore`, `quantile`, `normalize`)

Compares every stock against all other stocks in the universe **on the same day**:

```text
/* Maps the lowest value today to 0.0 and the highest value today to 1.0 */
rank(ebitda / enterprise_value)
```

- Use `rank(x)` as your default workhorse: it is invariant to monotone outliers and eliminates unit mismatches (`[Platform]`, `[Observed]`).

### Idiom 2: Time-Series Normalization (`ts_rank`, `ts_zscore`, `ts_scale`, `ts_quantile`, `ts_delta`)

Compares each stock today against **its own historical window** of $d$ trading days (`[Platform]`):

```text
/* Measures where today's sales growth sits within the stock's own 6-month (126-day) range */
ts_rank(sales_growth, 126)
```

- **Key empirical finding:** On slow analyst estimate fields (`anl69_*`, `anl4_*`), `ts_scale(ts_backfill(x, 21), 63)` and `ts_quantile(ts_backfill(x, 21), 63)` consistently outperformed plain cross-sectional `rank(ts_backfill(x, 21))` across EUR and KOR sweeps (`067`, `069`, `071`) (`[Observed]`).

### Idiom 3: Group-Relative Normalization (`group_rank`, `group_zscore`, `group_scale`, `group_neutralize`)

Compares each stock against peers **within the same group** (`industry`, `subindustry`, `country`, or a custom `bucket()`) on the same day (`[Platform]`):

```text
/* Rank 60-day earnings-yield momentum within each industry */
group_rank(ts_rank(est_eps / close, 60), industry)
```

## 5. Working Examples

### Example 1: Multi-Statement Option Implied Volatility Spread

```text
/* 1. Compute call-put implied volatility spread */
iv_difference = implied_volatility_call_120 - implied_volatility_put_120;

/* 2. Group stocks into deciles by 120-day historical volatility */
hvol_group = bucket(rank(historical_volatility_120), range="0.1,1,0.1");

/* 3. Neutralize IV spread within historical volatility deciles */
group_neutralize(iv_difference, hvol_group)
```
*(Official BRAIN Learn *Option6 Implied Volatility* example, `[Platform]`.)*

### Example 2: Event-Conditioned Trading with `trade_when`

```text
/* Only update positions on days when volume exceeds 20-day average daily volume;
   never exit based on the third argument (-1 < 0) */
positive_days = ts_sum(returns > 0 ? 1 : 0, 250);
trade_when(volume > adv20, rank(-positive_days), -1)
```

## 6. Common Mistakes and Troubleshooting

| Error / Symptom | Root Cause | Exact Fix |
|---|---|---|
| `Attempted to use inaccessible or unknown operator` | Typo in operator name (e.g., `ts_std` instead of `ts_std_dev`, `cs_rank` instead of `rank`) or operator locked behind higher Genius tier | Check exact signatures in [Operator Reference](operator-reference.md) (`[Platform]`) |
| `First argument of trade_when must be an event` | Passing a Universe field (`top2000`) or continuous float instead of a boolean comparison | Use a comparison expression such as `volume > adv20` or `abs(returns) > 0.02` (`[Observed]`) |
| `Event input not allowed for ts_delta` | Passing a Vector/Event field (`eps_estimate_value`) directly to a Matrix time-series operator (`042`, `043`) | Convert with `vec_avg(field)` or use a Matrix field (`[Observed]`) |
| Unit warning on `+` or `-` | Adding raw dollar fields to ratios or percentages (`ebitda + sales_growth`) | Wrap each leg in `rank()` or `zscore()` before adding (`rank(a) + rank(b)`) (`[Platform]`) |
| Unbalanced parentheses or trailing operator | Missing closing `)` in nested `group_neutralize(rank(ts_rank(...)))` | Format multi-term expressions across multiple intermediate `var = ...;` lines |

## 7. Practical Exercises

1. Rewrite `zscore(rank(ebitda / enterprise_value) + rank(ts_rank(sales_growth, 126)) + rank(ts_mean(-returns, 5)))` as a clean 4-line multi-statement Fast Expression using intermediate variables `val_leg`, `growth_leg`, and `rev_leg`.
2. Review the complete [Operator Reference](operator-reference.md) and identify three operators that reduce Turnover (`hump`, `ts_decay_linear`, `trade_when`).

## 8. Related Topics and Next Steps

- **Companion Reference:** [Complete WorldQuant BRAIN Operator Reference](operator-reference.md)
- **Quick Cheat Sheet:** [Fast Expression Cheat Sheet](../reference/fast-expression-cheatsheet.md)
- **Next Module:** [06 — Alpha Research and Construction](../06-alpha-research-and-construction/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Introduction to BRAIN Expression Language* and *Operators* (`[Platform]`, captured 2026-07-26 and 2026-10-09); troubleshooting records `001`–`071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
