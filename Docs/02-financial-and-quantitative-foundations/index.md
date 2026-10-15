# 02 — Financial and Quantitative Foundations

## 1. Learning Objectives

By completing this module, you will be able to:

- Calculate and interpret daily portfolio weights, long/short dollar neutrality, and daily PnL from a raw Alpha vector.
- Explain why group neutralization (Market, Sector, Industry, Subindustry, Country) isolates stock-specific alpha from market/sector beta.
- Distinguish the primary equity signal families (Mean Reversion, Momentum, Value, Quality, Growth, Analyst Revisions, Volatility, Liquidity) and their natural time horizons.
- Explain why raw accounting levels (`operating_income`, `ebitda`, `cashflow_op`) must be scaled by size or valuation denominators (`enterprise_value`, `assets`, `cap`).

## 2. Prerequisites

- [01 — Getting Started with WorldQuant BRAIN](../01-getting-started/index.md)

## 3. Core Concepts

### Long/Short Portfolio Mechanics

In a market-neutral equity book, positive weights (`w_i > 0`) represent **long positions** (buying stocks expected to outperform peers) and negative weights (`w_i < 0`) represent **short positions** (borrowing and selling stocks expected to underperform peers) (`[Platform]`).

| Position Type | Sign of Weight `w_i` | Stock Rises `+1%` | Stock Falls `-1%` | Economic Bet |
|---|---|---|---|---|
| **Long (`+$100`)** | `+` | `+$1` | `-$1` | Instrument outperforms its neutralization group |
| **Short (`-$100`)** | `-` | `-$1` | `+$1` | Instrument underperforms its neutralization group |

If every stock in an industry rises `+2%` on a macro rally, a long/short portfolio neutralized within that industry profits from the **spread** between the stocks held long (say `+3.5%`) and the stocks held short (say `+1.0%`), rather than from the direction of the market (`[Platform]`).

### Mathematical Pipeline from Expression to Weights

On each simulation day $t$, for instruments $i = 1, \dots, N$ in the universe (`[Platform]`):

1. **Raw Evaluation:** Compute raw signal $x_{i,t}$ from the Fast Expression using data available at $t - \text{Delay}$.
2. **Group Neutralization:** Within each peer group $g$ (for example, each GICS Subindustry), subtract the group mean:
   $$\tilde{x}_{i,t} = x_{i,t} - \frac{1}{|g|} \sum_{j \in g} x_{j,t}$$
3. **Decay (Linear Time Smoothing):** Blend today's neutralized vector with the previous $d - 1$ days using linear weights $d, d-1, \dots, 1$:
   $$z_{i,t} = \frac{\sum_{k=0}^{d-1} (d - k)\,\tilde{x}_{i,t-k}}{\sum_{k=0}^{d-1} (d - k)}$$
4. **Truncation & Unit-Book Scaling:** Cap any single stock's weight magnitude at the `Truncation` threshold (e.g., `0.08` = 8% of book) and normalize so that:
   $$\sum_{i=1}^{N} |w_{i,t}| = 1.0, \qquad \sum_{i \in g} w_{i,t} = 0$$

### Core Quantitative Equity Factor Families

| Factor Family | Economic Intuition | Typical Horizon | Representative BRAIN Fields | Empirical Behavior in This Repository |
|---|---|---|---|---|
| **Short-Term Reversal** | Liquidity provision and temporary overreaction reverse over 1–5 days | 1–10 days | `-returns`, `close - vwap`, intraday range | Strong Sharpe booster when smoothed (`ts_mean(-returns, 5)`), high turnover if raw (`[Observed]`) |
| **Valuation (Value)** | High cash flow or operating earnings relative to enterprise value indicates cheapness | 63–252 days | `ebitda / enterprise_value`, `cashflow_op / enterprise_value`, `bookvalue_ps / close` | `ebitda / enterprise_value` showed stronger sub-universe robustness than `cashflow_op / enterprise_value` (`[Observed]`) |
| **Quality / Profitability** | Firms generating high cash flow or operating income per unit of assets compound value | 63–252 days | `cashflow_op / assets`, `operating_income / assets`, `return_equity`, `return_assets` | Works best as `ts_rank(..., 126)` or `ts_delta(..., 63)` rather than static levels (`[Observed]`) |
| **Growth** | Expanding revenue/sales prevents value traps | 63–252 days | `sales_growth`, `revenue_growth`, `eps_growth` | `ts_rank(sales_growth, 126)` paired effectively with `ebitda / enterprise_value` (`[Observed]`) |
| **Analyst Expectations** | Consensus earnings/sales revisions and dispersion reflect fundamental information flow | 21–126 days | `anl69_*`, `anl4_*`, `anl10_*`, `op_cash_flow_stddev` | Slow analyst levels (`anl69_*`) with `ts_scale(..., 63)` produced the best EUR & KOR risk-adjusted clusters (`[Observed]`) |
| **Implied Volatility (Options)** | Call-put implied volatility spread or IV vs historical volatility captures informed options flow | 10–120 days | `implied_volatility_call_120`, `implied_volatility_put_120`, `historical_volatility_120` | High raw Sharpe (`2.61` in USA `071 d5`), but requires careful bucket/group control to avoid `CONCENTRATED_WEIGHT` (`[Observed]`) |
| **News & Sentiment** | Unusual media buzz or sentiment spikes predict short-term attention or reversion | 1–20 days | `scl12_buzz`, `snt_value`, `snt21_*` | High turnover (`87%+`) and weak Fitness when used unsmoothed (`036`–`041`) (`[Observed]`) |

## 4. Step-by-Step Explanation: Why Raw Accounting Levels Fail

A recurring beginner error is applying time-series operators directly to raw dollar accounting fields such as `operating_income` or `ebitda`:

1. **The Size Confounder:** A `$500B` mega-cap company naturally has much larger dollar `operating_income` than a `$2B` mid-cap company. Cross-sectionally, `operating_income` is mostly a proxy for market capitalization (`cap`).
2. **Stale Quarterly Step-Functions:** Fundamental fields update once per quarter (roughly every 63 trading days). Taking a short window like `ts_mean(operating_income, 4)` or `ts_delta(operating_income, 4)` yields zero on ~95% of trading days (`[Observed]`).
3. **Empirical Verification:** In Simulations [`008`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/008_raw_operating_income_ts_rank.md), [`009`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/009_raw_operating_income_ts_mean.md), and [`010`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/010_raw_operating_income_ts_delta.md), raw `operating_income` transforms all produced `Sharpe < 0.50` (`[Observed]`).
4. **The Solution — Scale by Enterprise Value or Assets:** Dividing by `enterprise_value`, `assets`, or `cap` converts a dollar level into a dimensionless yield or profitability ratio (`ebitda / enterprise_value`, `cashflow_op / assets`), and using a semi-annual or annual lookback (`63`, `126`, or `252` days) captures genuine multi-quarter fundamental improvement (`[Observed]`).

## 5. Working Examples

### Example 1: Dimensionless Enterprise Value Yield

```text
/* Compare operating cash flow generation per unit of total firm value across peers */
rank(ebitda / enterprise_value)
```

### Example 2: Multi-Quarter Fundamental Momentum + Short-Term Reversal

```text
/* Combine 6-month fundamental trajectory with 5-day price mean reversion */
rank(ts_rank(cashflow_op / assets, 126))
+ rank(ts_delta(operating_income / assets, 63))
+ rank(ts_mean(-returns, 5))
```
*(Basis of submitted Alpha [`027`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/027_submitted_cashflow_quality_improvement_reversal.md), `[Observed]`.)*

## 6. Common Mistakes and Troubleshooting

| Mistake | Why It Fails | Fix |
|---|---|---|
| Stacking 4–6 correlated quality/value ranks (`ROE + ROA + CF/Assets - EV/EBITDA`) | Dilutes the strongest signal and increases collinearity (Sim `011` Sharpe `0.46`, Sim `012` Sharpe `-0.28`) (`[Observed]`) | Isolate 1 base factor and add at most 1–2 orthogonal mechanisms (`[Notes]`) |
| Multiplying noisy fundamental ratios (`(ROE * CF) / (Assets * EV)`) | Nonlinear products amplify extreme outliers and flip signs when denominators are negative (Sim `013` Sharpe `-1.01`) (`[Observed]`) | Rank or z-score individual ratios before combining (`[Notes]`) |
| Applying short lookbacks (`d = 4` or `5`) to quarterly fundamental fields | Misses quarterly reporting intervals, leaving most days zero or unchanged | Use `d = 63` (1 quarter), `126` (half year), or `252` (1 year) on fundamental series (`[Notes]`) |

## 7. Practical Exercises

1. Write down the economic hypothesis for why `ebitda / enterprise_value` behaves differently from `operating_income / cap` for highly leveraged companies.
2. Compare the results of Simulations [`011`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/011_quality_value_composite.md)–[`025`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/025_ts_rank_ebitda_ev_ts_rank_sales_growth_returns.md) in the [USA Simulation Results](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/README.md) to trace how each single-variable change affected Sharpe and Fitness.

## 8. Related Topics and Next Steps

- **Next Module:** [03 — WorldQuant BRAIN Fundamentals](../03-worldquant-brain-fundamentals/index.md)
- **Bibliography:** [Books & Quantitative Alpha References](../../Books/README.md)

## 9. Sources and Verification

- **Sources:** BRAIN Learn *Introduction to Alphas* and *How BRAIN Works* (`[Platform]`), plus recorded experiments `001`–`027` (`[Observed]`).
- **Verification Date:** 2026-10-15.
