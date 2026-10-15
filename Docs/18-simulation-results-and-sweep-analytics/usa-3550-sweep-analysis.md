# Deep-Dive: 3,550-Block USA Factor Screening & Candidate Shortlist (`Simulation 070`)

This page presents the complete quantitative factor screening of the **3,550-block USA simulation sweep** ([Experiment `070`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/070_usa_top3000_industry_analyst_growth_sweep.md), dataset `20261008_071542_*`), evaluating **2,444 distinct fields** across six USA universes under `Delay = 1`, `Decay = 5`, `Neutralization = INDUSTRY`, `Truncation = 0.08`, `Pasteurization = ON`, and `NaN Handling = ON`.

## 1. Executive Summary & Data-Quality Reconciliation

- **Reconciled Block Count:** `3,550` total simulation blocks across two export pages:
  - **Page 1 (`20261008_071542_d1_usa_6universes`):** `2,500` blocks partitioned across `TOP3000` (`2,194`), `TOPSP500` (`81`), `TOP200` (`71`), `TOP2000` (`52`), `TOP500` (`52`), and `TOP1000` (`50`).
  - **Page 2 (`20261008_071542_d2_usa_top3000`):** `1,050` blocks in `USA / TOP3000`.
- **Platform Verdicts:** `3,544` `FAIL` (`99.83%`), `6` `PENDING` (`0.17%`), `0` `PASS` (`0.00%`).
- **Train vs Out-of-Sample Sharpe Audit:** `Train Sharpe` diverged from out-of-sample `Sharpe` in **3,469 of 3,550 blocks (97.7%)**. While `Train Sharpe` reached `1.95`, the true out-of-sample maximum was **`1.54`**. All tables below report verified out-of-sample metrics alongside `Train Sharpe`.

## 2. Full-Sweep Metric Distributions (N = 3,550)

| Metric | Sample (N) | Min | 5th Pct | 25th Pct | Median | Mean | 75th Pct | 95th Pct | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Sharpe (Out-of-Sample)** | `3,550` | `-1.8200` | `-0.4400` | `-0.0800` | **`0.1900`** | `0.1946` | `0.4600` | `0.8400` | **`1.5400`** |
| **Train Sharpe (IS Window)** | `3,550` | `-10.0000` | `-0.4800` | `-0.1100` | `0.1600` | `0.1261` | `0.4500` | `0.8600` | `1.9500` |
| **Fitness (Out-of-Sample)** | `3,532` | `-0.9200` | `-0.1900` | `-0.0100` | **`0.0600`** | `0.0976` | `0.2000` | `0.4700` | **`1.0300`** |
| **Turnover (%)** | `3,550` | `0.00%` | `0.96%` | `2.42%` | **`8.31%`** | `18.00%` | `21.01%` | `72.90%` | `145.18%` |
| **Returns (%)** | `3,550` | `-26.67%` | `-3.74%` | `-0.51%` | **`1.33%`** | `1.41%` | `3.14%` | `6.52%` | `41.74%` |
| **Drawdown (%)** | `3,550` | `0.00%` | `7.63%` | `13.21%` | **`21.57%`** | `32.39%` | `39.47%` | `92.23%` | `427.84%` |
| **Margin (bps)** | `3,550` | `-210.97` | `-12.64` | `-0.65` | **`1.88`** | `9.88` | `11.91` | `66.79` | `384.10` |

## 3. Performance Across USA Universes

| Universe | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Median Fitness | Sharpe >= 1.00 | Sharpe >= 1.25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **TOP3000** | `3,244` | `0.20` | `0.20` | `8.37%` | `0.06` | **76** | **12** |
| **TOPSP500** | `81` | `0.12` | `0.17` | `10.34%` | `0.03` | `1` | `0` |
| **TOP200** | `71` | `0.16` | `0.17` | `5.29%` | `0.06` | `0` | `0` |
| **TOP2000** | `52` | `0.19` | `0.19` | `4.21%` | `0.04` | `1` | `0` |
| **TOP500** | `52` | `0.18` | `0.17` | `6.85%` | `0.06` | `1` | `0` |
| **TOP1000** | `50` | `0.20` | `0.13` | `8.91%` | `0.04` | `0` | `0` |

## 4. Operator Family Comparative Performance

| Outer Operator | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Median Fitness | Sharpe >= 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| **`group_rank`** | `715` | **`0.51`** | **`0.49`** | `3.26%` | **`0.24`** | **63** (79.7%) |
| **`ts_sum`** | `56` | `0.34` | `0.33` | `2.50%` | `0.15` | `2` |
| **`rank`** | `166` | `0.29` | `0.24` | `5.10%` | `0.10` | `1` |
| **`scale`** | `158` | `0.27` | `0.21` | `4.97%` | `0.09` | `4` |
| **`ts_decay_linear`** | `46` | `0.25` | `0.20` | `4.03%` | `0.10` | `0` |
| **`ts_av_diff`** | `42` | `0.24` | `0.16` | `13.62%` | `0.07` | `0` |
| **`normalize`** | `150` | `0.20` | `0.19` | `8.32%` | `0.07` | `2` |
| **`group_neutralize`**| `187` | `0.20` | `0.19` | `6.33%` | `0.07` | `1` |
| **`ts_arg_min`** | `56` | `0.19` | `0.17` | `8.56%` | `0.05` | `0` |
| **`quantile`** | `146` | `0.18` | `0.18` | `6.94%` | `0.05` | `0` |
| **`ts_std_dev`** | `54` | `0.18` | `0.15` | `5.20%` | `0.05` | `1` |
| **`winsorize`** | `141` | `0.14` | `0.17` | `8.51%` | `0.04` | `0` |
| **`ts_arg_max`** | `53` | `0.14` | `0.12` | `8.34%` | `0.03` | `0` |
| **`last_diff_value`** | `42` | `0.13` | `0.09` | `9.21%` | `0.02` | `0` |
| **`group_zscore`** | `179` | `0.12` | `0.15` | `6.86%` | `0.03` | `3` |
| **`zscore`** | `170` | `0.12` | `0.12` | `6.61%` | `0.04` | `0` |
| **`group_scale`** | `141` | `0.12` | `0.14` | `6.99%` | `0.03` | `0` |
| **`ts_quantile`** | `47` | `0.11` | `0.09` | `18.83%` | `0.02` | `1` |
| **`ts_mean`** | `46` | `0.11` | `0.11` | `2.34%` | `0.03` | `0` |
| **`group_count`** | `144` | `0.11` | `-0.00` | `60.47%` | `0.02` | `0` |
| **`ts_scale`** | `56` | `0.08` | `0.06` | `17.22%` | `0.01` | `0` |
| **`ts_zscore`** | `57` | `0.08` | `0.04` | `19.46%` | `0.01` | `0` |
| **`ts_delay`** | `46` | `0.06` | `0.03` | `5.54%` | `0.01` | `0` |
| **`group_std_dev`** | `174` | `0.05` | `0.08` | `70.28%` | `0.01` | `1` |
| **`ts_delta`** | `49` | `0.05` | `0.09` | `13.20%` | `0.01` | `0` |
| **`ts_returns`** | `42` | `0.05` | `0.02` | `23.34%` | `0.01` | `0` |
| **`ts_kurtosis`** | `51` | `0.01` | `-0.00` | `14.26%` | `0.00` | `0` |
| **`ts_ir`** | `44` | `0.01` | `-0.03` | `15.76%` | `0.00` | `0` |
| **`group_sum`** | `132` | `-0.02` | `-0.00` | `67.74%` | `0.00` | `0` |
| **`ts_product`** | `59` | `-0.02` | `0.02` | `35.79%` | `0.00` | `0` |
| **`ts_rank`** | `45` | `-0.09` | `-0.06` | `17.78%` | `-0.01` | `0` |
| **`ts_max_diff`** | `56` | `-0.10` | `-0.08` | `13.71%` | `-0.03` | `0` |

## 5. Field Family Performance Scorecard (2,444 Distinct Fields)

| Field Family | Category | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Sharpe >= 1.00 |
|---|---|---:|---:|---:|---:|---:|
| **`anl11`** | ESG & Reputation | `11` | **`0.61`** | `0.42` | `2.65%` | `0` |
| **`fnd6`** | Fundamental Valuation | `1` | `0.53` | `0.53` | `1.05%` | `0` |
| **`snt21`** | News Sentiment | `12` | `0.52` | `0.36` | `22.64%` | `0` |
| **`pv20`** | Price-Volume Indicators | `45` | `0.48` | `0.40` | `6.15%` | `4` |
| **`est_`** | Analyst Consensus Estimates | `57` | `0.47` | **`0.45`** | `2.67%` | **7** |
| **`fnd23`** | Balance Sheet / Income | `41` | `0.40` | `0.36` | `1.49%` | `0` |
| **`other`** | Company Filings / Earnings Growth | `502` | `0.34` | `0.32` | `5.67%` | **32** |
| **`fnd28`** | Corporate Ratios / Performance | `57` | `0.34` | `0.29` | `1.01%` | `1` |
| **`fnd17`** | Per-share Financials | `11` | `0.34` | `0.33` | `1.22%` | `0` |
| **`anl69`** | Broker Recommendations | `48` | `0.29` | `0.22` | `7.29%` | `1` |
| **`adv`** | Liquidity / Dollar Volume | `10` | `0.23` | `0.18` | `10.61%` | `0` |
| **`anl10`** | Model Predictions / Revisions | `555` | `0.20` | `0.21` | `10.89%` | **25** |
| **`anl15`** | Global Industry Estimates | `2,022` | `0.14` | `0.15` | `9.37%` | **7** |
| **`anl4`** | Company Guidance Detail | `173` | `0.03` | `0.10` | `3.13%` | `2` |
| **`sector_`** | Categorical Sector Dummies | `5` | `0.00` | `-0.22` | `5.37%` | `0` |

## 6. Platform Check Failure Breakdown

| Failed Check Code | Check Combination | Blocks | Share (%) |
|---|---|---:|---:|
| **F1** | `LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE` | `1,573` | `44.3%` |
| **F2** | `LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | `810` | `22.8%` |
| **F3** | `LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE` | `404` | `11.4%` |
| **F4** | `LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | `233` | `6.6%` |
| **F5** | `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_2Y_SHARPE` | `154` | `4.3%` |
| **F6** | `LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | `102` | `2.9%` |
| **F7** | `LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE` | `78` | `2.2%` |
| **F8** | `LOW_SHARPE, LOW_FITNESS` | `63` | `1.8%` |
| **F9** | `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | `38` | `1.1%` |
| **F10**| `LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE` | `23` | `0.6%` |
| **F11–F21** | Tail combinations (`IS_LADDER_SHARPE`, extreme concentration/turnover) | `66` | `1.9%` |

## 7. Ranked Candidate Shortlist (Groups A, B, and C)

### Group A — Strongest Candidates for Targeted Validation

| Rank | Expression | Universe | Sharpe | Train | Fit | TO | Ret | DD | Margin | Fail Code | Recommended Validation Step |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **A1** | `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)` | `TOP3000` | **`1.54`** | `1.44` | `0.94` | `3.72%` | `4.66%` | `5.57%` | `25.08 bps` | `F8` | Extend backfill to `63` days and blend with 5d reversal leg |
| **A2** | `group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)` | `TOP3000` | **`1.52`** | `1.26` | `0.98` | `3.71%` | `5.16%` | `11.90%` | `27.82 bps` | `F8` | Needs `+0.02` Fitness; test `subindustry` grouping and `63d` backfill |
| **A3** | `group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)` | `TOP3000` | **`1.40`** | `1.69` | **`1.03`** | `2.00%` | `6.73%` | `5.97%` | `67.19 bps` | `F19` | Only block with Fitness `>= 1.00`; reduce Decay `5 -> 2` to lift 2Y Sharpe |
| **A4** | `group_rank(ts_backfill(eps_q1_estimate_asymmetry, 21), subindustry)` | `TOP3000` | **`1.50`** | `1.64` | `0.79` | `6.91%` | `3.48%` | `2.98%` | `10.07 bps` | `F2` | Minimal drawdown (`2.98%`); double-neutralize by size buckets |
| **A5** | `group_rank(ts_backfill(estimate_y1_skewness_book_value_ps, 21), market)` | `TOP3000` | **`1.44`** | `1.49` | `0.83` | `3.13%` | `4.17%` | `7.12%` | `26.63 bps` | `F2` | Test `subindustry` grouping and `ts_backfill(..., 63)` |
| **A6** | `group_rank(ts_backfill(consensus_next_fiscal_year_interest_expense, 21), market)` | `TOP3000` | **`1.44`** | `1.51` | `0.77` | `2.67%` | `3.61%` | `4.50%` | `27.13 bps` | `F2` | Scale by enterprise value (`interest / ev`) to remove cap bias |

### Group B — Promising Research Hypotheses

| Rank | Expression | Universe | Sharpe | Fit | TO | Ret | DD | Bottleneck & Hypothesis |
|---:|---|---|---:|---:|---:|---:|---:|---|
| **B1** | `scale(ts_std_dev(ts_backfill(anl10_smartest_ner_ff, 21), 126))` | `TOP3000` | `1.21` | `0.84` | `2.45%` | `6.05%` | `14.33%` | **PENDING state**; high return spread (`6.05%`), needs full check evaluation |
| **B2** | `group_rank(ts_backfill(net_9_feature3_predictor, 21), market)` | `TOP3000` | `1.35` | `0.84` | `4.74%` | `4.82%` | `7.11%` | Verify point-in-time publication lag on `net_9` predictor |
| **B3** | `group_rank(ts_backfill(revenue_actual_q1_qoq_growth, 21), market)` | `TOP3000` | `1.34` | `0.81` | `3.34%` | `4.53%` | `6.11%` | Combine with gross margin revision A2 as quality-growth composite |
| **B4** | `group_rank(ts_backfill(actual_q1_qoq_gross_income_growth, 21), subindustry)` | `TOP3000` | `1.29` | `0.74` | `3.38%` | `4.13%` | `4.02%` | Low drawdown (`4.02%`); pair with 5d mean-reversion leg |
| **B5** | `group_rank(ts_backfill(interest_expense_volatility_adjusted_2yr, 21), market)` | `TOP3000` | `1.21` | `0.78` | `1.79%` | `5.21%` | `6.36%` | High margin (`58.3 bps`), failed `CONCENTRATED_WEIGHT`; tighten truncation |

### Group C — Failure References (Negative Controls)

| Expression | Universe | Sharpe | Turnover | Drawdown | Root Cause Failure Mechanism |
|---|---|---:|---:|---:|---|
| `group_std_dev(ts_product(ts_backfill(anl15_bps_ind_fy1_cos_up, 21), 5), sector)` | `TOP3000` | `0.55` | `72.48%` | `27.46%` | Cross-sectional standard deviation explosion (`F6`) |
| `ts_product(ts_backfill(anl15_salgics_s_cal_fy1_cos, 21), 252)` | `TOP3000` | `0.46` | `102.38%` | `201.96%` | Rolling time-series product compounding trap (`F7`) |
| `group_rank(ts_backfill(actuals_value_currency_code, 21), sector)` | `TOP3000` | `1.01` | `1.15%` | `17.67%` | Categorical currency ticker artifact (`PENDING`); non-investable |
