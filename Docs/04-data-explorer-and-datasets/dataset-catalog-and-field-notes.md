# Dataset Catalog and Empirical Field Notes

Detailed reference of WorldQuant BRAIN dataset categories, individual fields, and observed performance across the 71 experiments and 13,319 sweep blocks recorded in this repository.

## 1. Dataset Families Tested in This Repository

| Dataset Family / ID | Category | Primary Field Types | Empirical Performance Summary (`[Observed]`) | Recommended Usage & Neutralization |
|---|---|---|---|---|
| **Price & Volume (`pv1`)** | Price / Volume | Matrix (`open, high, low, close, vwap, volume, returns, adv20, cap`) | Essential for short-term reversal legs (`ts_mean(-returns, 5)`) and liquidity scaling (`volume / adv20`) | Pair with fundamental or analyst anchors; `Market` or `Subindustry` neutralization |
| **Intraday / Session Volume (`pv37`, session fields)** | Price / Volume | Matrix (`pv37_snapshot1_volume*`, `session_1600to1600_total_traded_volume`) | Highest raw EUR Sharpe (`2.51` in `068`), but fails `LOW_SUB_UNIVERSE_SHARPE` at Decay 5 and `HIGH_TURNOVER` (`100%+`) at Decay 0 | Requires aggressive turnover smoothing (`ts_decay_linear`, `ts_quantile(..., 126–252)`) |
| **Company Fundamentals (`fnd6`)** | Fundamental | Matrix (`ebitda, operating_income, cashflow_op, assets, enterprise_value, debt, current_ratio, sales_growth, return_equity, return_assets, dividend`) | Backbone of all 3 submitted/submittable USA Alphas (`026, 027, 053`) when expressed as size-scaled ratios (`ebitda/enterprise_value`, `cashflow_op/assets`) with `ts_rank(..., 126)` | Always normalize by `enterprise_value`, `assets`, or `cap`; `Subindustry` or `Industry` neutralization |
| **Slow Analyst Estimates (`anl69`, `anl4`)** | Analyst | Matrix (`anl69_sales_best_eeps_cur_yr`, `anl69_net_new_best_eeps_nxt_yr`, `anl69_ebitda_best_eeps_cur_yr`, `anl4_sadaf_netprofit_median`, `anl4_af_div_low`) | Strongest low-turnover single-dataset (ATOM) cluster across `EUR` (`Sharpe 1.97, Fitness 1.58, Turnover 5.78%` in `067`) and `KOR` (`Sharpe 2.36, Fitness 1.67` in `071 d1`) | Wrap in `ts_backfill(x, 21)` followed by `ts_scale(..., 63)` or `ts_quantile(..., 63)`; `COUNTRY` or `INDUSTRY` neutralization |
| **Crowded Consensus Analyst (`anl10`)** | Analyst | Matrix (`anl10_salfy1_consensus_559`, etc.) | Saturates around `Sharpe 1.20–1.40`, `Fitness <= 1.02` in EUR sweeps; struggles on `LOW_2Y_SHARPE` | Deprioritize in favor of `anl69` and `anl4` |
| **Option Implied Volatility (`option6`)** | Option / Volatility | Matrix (`implied_volatility_call_120`, `implied_volatility_put_120`, `implied_volatility_mean_*`, `historical_volatility_*`) | Reached `Sharpe 2.61, Fitness 1.88` in USA `071 d5`, but failed `CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE` when unbucketed | Use call-put spreads (`iv_call - iv_put`) neutralized within `historical_volatility` buckets (`[Platform]`) |
| **Sentiment (`sentiment1`, `scl12`, `snt21`)** | Sentiment / News | Matrix & Vector (`scl12_buzz`, `snt_value`, `snt_social_volume`) | High raw Sharpe (`1.31–1.59` in `036–039`) but extreme turnover (`87%+`) and low Fitness (`0.36–0.68`) | Avoid raw `*_fast_d1` sentiment; use rolling stability (`-ts_std_dev(scl12_buzz, 10)`) (`[Platform]`, `[Observed]`) |
| **Quantitative Models (`model77`, `model25`)** | Model | Matrix | Pre-computed factor and valuation scores (`[Platform]`) | Useful starting dataset in `HKG` (`model25`) and multi-factor overlays (`[Platform]`) |

## 2. Fundamental Field Reference (`fnd6` & Standard Equities)

| Theme | Field Names | Usage Notes (`[Observed]`, `[Notes]`) |
|---|---|---|
| **Profitability & Earnings** | `ebitda`, `ebit`, `operating_income`, `income`, `gross_profit`, `return_equity`, `return_assets` | `ebitda / enterprise_value` outperformed `operating_income / cap` and `cashflow_op / enterprise_value` on sub-universe robustness (`022`–`026`). Raw `operating_income` alone fails (`008`–`010`). |
| **Cash Flow** | `cashflow_op`, `operating_cash_flow`, `free_cash_flow`, `op_cash_flow_stddev` | `cashflow_op / assets` works well in 126-day `ts_rank` (`027`). `op_cash_flow_stddev` 10-day delta had `Sharpe 1.52` (`063`) and `1.48` (`065`). |
| **Valuation & Size** | `enterprise_value`, `cap`, `assets`, `bookvalue_ps`, `liabilities`, `debt`, `current_ratio` | Use `enterprise_value`, `assets`, and `cap` as denominators. Adding `current_ratio` repeatedly degraded Fitness (`017`, `021`, `028`, `034`). |
| **Growth & Payout** | `sales_growth`, `revenue_growth`, `eps_growth`, `dividend` | `ts_rank(sales_growth, 126)` is the strongest growth complement tested (`025`, `026`). `dividend` + volume + reversal reached `Sharpe 1.86` (`046`) but hit self-correlation. |

## 3. Fields and Patterns to Avoid (`No-Repeat` List)

Based on empirical failures in [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/index.md):

1. **Degenerate / Non-Predictive Fields:** `adjfactor`, `pv37_low_14` under `ts_product` (numerical overflow artifact in `068`), `pv47_*spret`, `*_currency_code`, `expected_report_*` variance fields.
2. **Direct Matrix Time-Series on Event Fields:** `ts_delta(eps_estimate_value, 20)` (`042`) and `ts_delta(sales_estimate_value, 20)` (`043`) without vector/backfill conversion.
3. **Unanchored Grouping Aggregations:** `group_count`, `group_sum`, or `group_std_dev` over raw volume or grouping identifiers in EUR (`067`–`069`).


### Empirical Findings from the 3,550 USA Sweep (`Simulation 070`)

Screening 2,444 distinct fields in `USA / TOP3000 / Delay 1 / Decay 5` (`[Observed]`) confirmed:
- **Analyst Estimate Changes & Asymmetry:** `estimate_year2_change_3mo_gross_margin` (Sharpe `1.52`, Fitness `0.98`, Turnover `3.71%`) and `eps_q1_estimate_asymmetry` (Sharpe `1.50`, Fitness `0.79`, Turnover `6.91%`) generated robust out-of-sample risk-adjusted returns when wrapped in `group_rank`.
- **Quarterly Earnings Growth:** `netprofit_actual_q1_qoq_growth` produced Sharpe `1.54` / Fitness `0.94` at `3.72%` turnover, representing the cleanest fundamental growth signal in the USA library.
- **Backfill Rule for Quarterly Data:** Applying `ts_backfill(field, 21)` to quarterly fields triggered `CONCENTRATED_WEIGHT` in 25.0% of blocks (`887` of `3,550`) due to 42-day coverage lapses between disclosures. Always use `ts_backfill(field, 63)` or `126` for quarterly statement items.
- **Categorical Identification Hazards:** Fields such as `actuals_value_currency_code` (Sharpe `1.01`) represent categorical currency tickers, not continuous economic quantities. These are non-investable and must be excluded from Alpha construction.
