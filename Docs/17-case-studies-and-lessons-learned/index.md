# 17 — Empirical Case Studies and Lessons Learned (71 Experiments & 13,319 Sweep Blocks)

## 1. Learning Objectives

By completing this module, you will be able to:

- Trace the exact empirical progression that produced the repository's 3 passing/submitted Alphas (`026`, `027`, `053`) out of 66 hand-built USA iterations.
- Recognize the four recurring failure archetypes (**Raw Accounting Levels**, **Factor-Stacking Dilution**, **The Self-Correlation Wall**, and **Over-Smoothing Signal Destruction**).
- Apply the quantitative findings from **13,319 multi-simulation sweep blocks** across `EUR`, `USA`, `KOR`, `AMR`, and `GLB/ALL` (`067`–`071`).

## 2. Prerequisites

- [07 — Simulation and Evaluation](../07-simulation-and-evaluation/index.md)
- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)

## 3. Core Concepts: The Empirical Record at a Glance

Every lesson in this chapter is grounded in committed simulation records inside [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/) (`[Observed]`):

| Metric / Category | Recorded Count | Key Empirical Takeaway (`[Observed]`) |
|---|---:|---|
| **Total Canonical Experiment Records** | `71` | `001`–`066` hand-built USA iterations + `067`–`071` multi-simulation sweeps |
| **Hand-Built Alphas Clearing User Checks** | `3` (`026, 027, 053`) | All 3 combined a slow fundamental value/quality ratio with a smoothed 5-day reversal (`ts_mean(-returns, 5)`) |
| **High-Metric Alphas Rejected for Self-Correlation** | `4` (`029, 031, 033, 046`) | Reached Sharpe `1.71–1.86` and Fitness `1.07–1.21`, but failed at `0.88–0.94` correlation |
| **Validation / Type Errors Recorded** | `2` (`042, 043`) | Direct `ts_delta` on event/vector estimate fields (`eps_estimate_value`, `sales_estimate_value`) |
| **Total Bulk Sweep Blocks Simulated** | `13,319` | Across 11 multi-simulation pages in 5 regions (`EUR, USA, KOR, AMR, ALL`) |
| **Submittable Alphas Produced Directly by Sweeps** | `0` | Single-field transform grids map the promising field clusters (`anl69`, `pv37`, `option6`), but never pass all checks without targeted engineering |

## 4. Step-by-Step Case Studies

### Case Study 1: From Failed Value Composites to Submitted Alpha `026` (`Simulations 001–026`)

1. **Dead End A — Raw Operating Income (`008`–`010`):** Applying `ts_rank`, `ts_mean`, and `ts_delta` to raw `operating_income` all yielded `Sharpe < 0.50` because raw dollar levels act as uncompensated size bets and update only quarterly (`[Observed]`).
2. **Dead End B — Multi-Factor Linear & Multiplicative Stacking (`011`–`013`):** Combining multiple static ranks (`ROE + cashflow/assets - EV/EBITDA`) gave `Sharpe 0.46` (`011`), a larger linear stack dropped to `Sharpe -0.28` (`012`), and a nonlinear product collapsed to `Sharpe -1.01` (`013`) (`[Observed]`).
3. **Breakthrough 1 — Switching Denominator & Factor (`014`–`022`):** Isolating `cashflow_op / enterprise_value` showed positive standalone signal (`Sharpe 0.41` in `014`). Pairing with `sales_growth` and `-returns` beat `ROE`/`ROA`/`current_ratio` variants (`Sharpe 1.21` in `020`). Replacing `cashflow_op / enterprise_value` with `ebitda / enterprise_value` (`022`) raised Sub-universe Sharpe to `1.26` (`[Observed]`).
4. **Breakthrough 2 — Time-Series Ranking Over 126 Days (`024`–`025`):** Wrapping `ebitda / enterprise_value` in `ts_rank(..., 126)` (`024`) lifted Sharpe to `1.36`. Wrapping `sales_growth` in `ts_rank(..., 126)` (`025`) lifted Sharpe to `1.78` and Fitness to `0.97` (`[Observed]`).
5. **Breakthrough 3 — Smoothing the Reversal Leg (`026`):** Replacing raw `rank(-returns)` with `rank(ts_mean(-returns, 5))` inside cap-decile neutralization cut Turnover to `25.25%`, lifting Fitness to **`1.02`** at **Sharpe `1.61`** (`PASSED_SUBMITTABLE`) (`[Observed]`).

### Case Study 2: The Self-Correlation Trap (`Simulations 027, 029, 031, 033, 046`)

After submitting `026` and `027` (`cashflow_op/assets + ts_delta(operating_income/assets, 63) + ts_mean(-returns, 5)`), several variants achieved even higher Sharpe and Fitness:

- [`029`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/029_operating_income_roa_reversal_selfcorr.html): `Sharpe 1.76, Fitness 1.21, Turnover 18.73%` -> **Rejected (`Self-Correlation = 0.8817`)**
- [`031`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/031_cashflow_roa_reversal_selfcorr.html): `Sharpe 1.71, Fitness 1.13` -> **Rejected (`Self-Correlation = 0.933`)**
- [`046`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/046_dividend_volume_returns_selfcorr.html): `Sharpe 1.86, Fitness 1.07` -> **Rejected (`Self-Correlation = 0.935`)**

**Lesson:** Once a 3-factor backbone (`fundamental quality + ts_mean(-returns, 5)`) is in your submitted pool, swapping `cashflow_op/assets` for `operating_income/assets` or `return_assets` leaves 4-year PnL correlation above `0.88` (`[Observed]`). Removing the reversal leg entirely (`054`, `056`) dropped Fitness below `1.0` (`0.78` and `0.89`). True correlation reduction requires moving to a genuinely orthogonal dataset (`anl69`, `option6`) or a new region (`EUR`, `KOR`, `GLB`).

### Case Study 3: Sentiment Noise and Cash-Flow Dispersion Over-Smoothing (`Simulations 036–041, 063–066`)

- **Sentiment (`036`–`041`):** `scl12_buzz` and `snt_value` produced `Sharpe 1.31–1.59`, but daily turnover hit **`87.5%`**, crushing Fitness to `0.36–0.68` (`[Observed]`).
- **Cash-Flow Estimate Dispersion (`063`–`066`):** A high-turnover `op_cash_flow_stddev` alpha achieved `Sharpe 1.52, Fitness 0.84` (`063`). Attempting to fix turnover by applying a 20-day mean to a 20-day delta at `Decay = 8` (`064`) reduced turnover to `11.81%` but destroyed the signal (`Sharpe 0.85, Fitness 0.48`) (`[Observed]`). Pairing the faster dispersion leg with `sales_growth` and 5-day reversal (`065`) recovered `Sharpe 1.48, Fitness 0.91, Turnover 21.78%` (`[Observed]`).

### Case Study 4: Multi-Region Sweep Evidence (`Simulations 067–071`, 13,319 Blocks)

Across 11 multi-simulation pages in [`sweeps-and-experiments/README.md`](../../Analysis%20and%20Simulation%20Reports/sweeps-and-experiments/) (`[Observed]`):

1. **`LOW_2Y_SHARPE` is the #1 Binding Constraint in Europe:** In EUR sweeps `067` (314 blocks), `068` (2,100 blocks), and `069` (1,809 blocks), `LOW_2Y_SHARPE` failed in **95.5%**, **92.9%**, and **98.0%** of all blocks (`[Observed]`).
2. **`anl69_*` Slow Analyst Fields under `ts_scale(..., 63)` / `ts_quantile(..., 63)` Form the Best Cross-Regional Cluster:**
   - `EUR TOP2500` (`067`): `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` -> `Sharpe 1.97, Fitness 1.58, Turnover 5.78%`.
   - `EUR TOPCS1600` (`069`): `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` -> `Sharpe 1.82, Fitness 1.41, Turnover 15.20%`.
   - `KOR TOP600` (`071 d1`): `ts_scale(ts_backfill(anl69_ebitda_best_eeps_cur_yr, 21), 63)` -> `Sharpe 2.36, Fitness 1.67, Turnover 6.60%`.
3. **Decay Moves Turnover, Not Sharpe Ordering:** Comparing `068` (`Decay 5`) and `069` (`Decay 0`) on identical EUR expressions showed that `Decay 5` cut turnover by up to `3.3x` while changing Sharpe by at most `0.13` (`[Observed]`).


### Case Study 5: The 3,550-Block USA Sweep & Operator Dominance (`Simulation 070`)

Experiment [`070`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/070_usa_top3000_industry_analyst_growth_sweep.html) screened 2,444 distinct fields across USA universes using `ts_backfill(field, 21)` under multiple outer transforms (`[Observed]`):

1. **`group_rank` is the Outlier Guard:** `group_rank` delivered a median Sharpe of `0.51` (mean `0.49`, median turnover `3.26%`) and accounted for **63 of the 79 (79.7%) alphas with Sharpe >= 1.00**, including all 12 alphas with Sharpe `>= 1.25`. `group_zscore` produced a median Sharpe of only `0.12`, and `group_std_dev` suffered turnover collapse (`70.28%`).
2. **Sub-Universe Degradation on Analyst Signals:** All 12 alphas with Sharpe `>= 1.25` occurred in `TOP3000`. In smaller universes (`TOP200`, `TOP500`, `TOPSP500`), zero alphas cleared `1.25`, and `LOW_SUB_UNIVERSE_SHARPE` was triggered in 34.8% of blocks (`1,237` of `3,550`). Institutional pricing efficiency in large caps compresses analyst revision return spreads.
3. **The Quarterly `ts_backfill(..., 21)` Gap:** 887 blocks (25.0%) failed `CONCENTRATED_WEIGHT` because a 21-day lookback expires between 63-day quarterly filing intervals, leaving stocks unweighted. Lookbacks on quarterly data should be `>= 63` days.
4. **Train vs OOS Divergence:** In 97.7% of blocks (`3,469` of `3,550`), `Train Sharpe` diverged from out-of-sample `Sharpe`. Always verify and index out-of-sample metrics.
5. **Top Candidates for Repair:**
   - `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)`: Sharpe `1.54`, Fitness `0.94`, Turnover `3.72%`, Drawdown `5.57%` (`F8: LOW_SHARPE, LOW_FITNESS`).
   - `group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)`: Sharpe `1.52`, Fitness `0.98`, Turnover `3.71%`, Drawdown `11.90%` (`F8`).
   - `group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)`: Sharpe `1.40`, Fitness `1.03`, Turnover `2.00%`, Drawdown `5.97%` (`F19: LOW_SHARPE, LOW_2Y_SHARPE`).

## 5. Working Examples: Summary Comparison of Top Recorded Alphas

| Sim ID | Scope | Expression | Sharpe | Fitness | Turnover | Verdict (`[Observed]`) |
|---:|---|---|---:|---:|---:|---|
| [`026`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.html) | `USA / TOP3000 / D1` | `group_neutralize(rank(ts_rank(ebitda/ev, 126)) + rank(ts_rank(sales_growth, 126)) + rank(ts_mean(-returns, 5)), bucket(rank(cap), range="0.1,1,0.1"))` | `1.61` | `1.02` | `25.25%` | `PASSED_SUBMITTABLE` (User checks) |
| [`053`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/053_submitted_ebitda_ev_mean_reversion.html) | `USA / TOP3000 / D1` | `rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))` | `1.46` | `1.05` | — | `PASSED_SUBMITTED` (User checks) |
| [`067`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/067_eur_top2500_country_analyst_sweep.html) | `EUR / TOP2500 / D1` | `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` | `1.97` | `1.58` | `5.78%` | Failed `LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE` |
| [`071 d1`](../../Analysis%20and%20Simulation%20Reports/simulation-results/multi-region/071_multi_region_bundle_20261009.html) | `KOR / TOP600 / D1` | `ts_scale(ts_backfill(anl69_ebitda_best_eeps_cur_yr, 21), 63)` | `2.36` | `1.67` | `6.60%` | Failed `LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE` |

## 6. Common Mistakes and Troubleshooting

- **Assuming user-level `PASSED_SUBMITTED` Alphas automatically clear consultant gates:** None of `026`, `027`, or `053` was evaluated against the consultant IS Ladder (`2.38` 2Y fail bar) or platform-wide prod-correlation (`<= 0.70`). Always re-verify under consultant checks (`[Notes]`).

## 7. Practical Exercises

1. Browse [`aggregate-analytics/README.md`](../../Analysis%20and%20Simulation%20Reports/aggregate-analytics/) and [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/).
2. Formulate a hypothesis to repair the `LOW_SUB_UNIVERSE_SHARPE` failure on `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` in `EUR TOP2500` using only `anl69` and support grouping fields (`country`, `industry`, `subindustry`) so it remains an **ATOM**.

## 8. Related Topics and Next Steps

- **Reference Hub:** [Reference Overview](../reference/index.md)
- **Full Evidence Catalog:** [Analysis and Simulation Reports](../../Analysis%20and%20Simulation%20Reports/)

## 9. Sources and Verification

- **Sources:** Canonical simulation records `001`–`071` and parsed sweep CSVs in [`Analysis and Simulation Reports/`](../../Analysis%20and%20Simulation%20Reports/) (`[Observed]`).
- **Verification Date:** 2026-10-15.
