# Simulation Status Index

This file is the quick duplicate-check ledger. Before suggesting or fixing an alpha, check this file and avoid giving any exact formula already marked `FAILED`, `ERROR`, `FAILED_SELF_CORRELATION`, `PASSED_SUBMITTABLE`, or `PASSED_SUBMITTED`.

Status meanings:

- `FAILED`: not submittable, not submitted, or observed worse than the best branch.
- `PASSED_SUBMITTABLE`: met the known submission thresholds in the shared screenshot.
- `PASSED_SUBMITTED`: user reported the alpha was submitted.
- `FAILED_SELF_CORRELATION`: performance may be good, but the platform rejected it for similarity.
- `ERROR`: the expression failed syntax, type, unit, or field validation.
- `NO_REPEAT`: do not suggest the exact expression again unless the user explicitly asks to revisit it.

## Rules From This Ledger

- Never suggest the exact submitted alpha again as a "new" alpha.
- Never suggest an exact failed alpha again.
- If using a failed alpha family, change the actual mechanism, not just formatting.
- If a past formula was close, build a single targeted variant and explain which component changed.
- Preserve the submitted alpha as a baseline; clone or compare against it, but do not overwrite it.

## Status Table

| ID | Status | Short name | Key result | Main lesson |
|---:|---|---|---|---|
| 001 | FAILED | Positive-days momentum | Sharpe 0.99, Fitness 1.13 | Fitness can pass while Sharpe fails. |
| 002 | FAILED | Operating income/cap + returns | Sharpe 1.14, Fitness 0.84 | Close but weak; needs stronger transformation. |
| 003 | FAILED | Operating income/cap + ts_rank returns | Sharpe 1.29, Fitness 0.60 | Sharpe passed, turnover/Fitness failed. |
| 004 | FAILED | Operating income/cap + ts_mean returns | Sharpe 1.05, Fitness 0.98 | Smoothing lowered Sharpe. |
| 005 | FAILED | ts_mean operating income/cap + returns | Sharpe 1.01, Fitness 0.89 | Smoothing slow fundamentals did not help. |
| 006 | FAILED | Operating income/cap + volatility-adjusted returns | Sharpe 0.99, Fitness 0.86 | Vol adjustment did not help this branch. |
| 007 | FAILED | Dividend + volume + returns | Sharpe 1.78, Fitness 0.67 | Strong Sharpe can still fail due high turnover/Fitness. |
| 008 | FAILED | Raw operating income ts_rank | Sharpe below 0.5 | Raw operating income was weak. |
| 009 | FAILED | Raw operating income ts_mean | Weak | Time-series mean on quarterly field weak. |
| 010 | FAILED | Raw operating income ts_delta | Weak | Raw fundamental changes not enough here. |
| 011 | FAILED | ROE + cashflow/assets - EV/EBITDA | Sharpe 0.46, Fitness 0.22 | Generic quality/value too weak. |
| 012 | FAILED | Large quality/value composite | Sharpe -0.28 | Too many linear factors diluted signal. |
| 013 | FAILED | Nonlinear ROE/cashflow product | Sharpe -1.01 | Multiplicative interaction distorted signal. |
| 014 | FAILED | Cashflow/EV only | Sharpe 0.41 | Positive but weak standalone value signal. |
| 015 | FAILED | Cashflow/EV + ROE + reversal | Sharpe 1.18, Fitness 0.71 | Good ancestor, not enough. |
| 016 | FAILED | Cashflow/EV + ROA + reversal | Worse than 015 | ROA worse than ROE here. |
| 017 | FAILED | Cashflow/EV + ROE + current_ratio + reversal | Sharpe 1.19, Fitness 0.66 | Current ratio lowered Fitness. |
| 018 | FAILED | Cashflow/EV + ROE + ROA + reversal | Worse than prior best | Stacking profitability hurt. |
| 019 | FAILED | Cashflow/EV + operating_income/assets + reversal | Plateaued/worse | Operating-income branch stayed weak. |
| 020 | FAILED | Cashflow/EV + sales_growth + reversal | Sharpe 1.21, Fitness 0.58 | Growth helped but Fitness failed. |
| 021 | FAILED | Cashflow/EV + sales_growth + current_ratio + reversal | Worse than 020 | Current ratio hurt again. |
| 022 | FAILED | EBITDA/EV + sales_growth + reversal | Sharpe 1.21, SubU 1.26 | EBITDA/EV improved robustness. |
| 023 | FAILED | EBITDA/EV + ROE + sales_growth | Sharpe 0.28 | ROE badly hurt this branch. |
| 024 | FAILED | ts_rank EBITDA/EV + sales_growth + reversal | Sharpe 1.36, Fitness 0.68 | TS rank made value signal stronger. |
| 025 | FAILED | ts_rank EBITDA/EV + ts_rank sales_growth + reversal | Sharpe 1.78, Fitness 0.97 | Very close; reversal needed smoothing. |
| 026 | PASSED_SUBMITTABLE | ts_rank EBITDA/EV + ts_rank sales_growth + ts_mean reversal | Sharpe 1.61, Fitness 1.02 | First submitted/submittable alpha. |
| 027 | PASSED_SUBMITTED | cashflow/assets + operating_income/assets delta + reversal | Sharpe 1.39, submitted | Quality/improvement plus reversal worked. |
| 028 | FAILED | current_ratio + sales_growth delta + 10d reversal | Sharpe 0.87, Fitness 0.47 | Liquidity/growth branch weak. |
| 029 | FAILED_SELF_CORRELATION | operating_income/assets + return_assets delta + reversal | Sharpe 1.76, Fitness 1.21, selfcorr 0.8817 | Great metrics but too similar. |
| 030 | FAILED | operating_income/assets + return_assets delta + 20d reversal | Sharpe 1.19 | Longer reversal weakened signal. |
| 031 | FAILED_SELF_CORRELATION | cashflow/assets + return_assets delta + reversal | Sharpe 1.71, Fitness 1.13, selfcorr 0.933 | Similar quality/reversal backbone. |
| 032 | FAILED | operating_income/assets + current_ratio delta + reversal | Sharpe 1.50, Fitness 0.96 | Close but failed Fitness. |
| 033 | FAILED_SELF_CORRELATION | operating_income/assets + EBITDA/EV delta + reversal | Failed correlation | Still too close to submitted family. |
| 034 | FAILED | current_ratio + sales_growth + 10d reversal | Sharpe 0.66 | Liquidity family weak. |
| 035 | FAILED | debt/assets + sales_growth + reversal | Sharpe 0.91 | Leverage family weak. |
| 036 | FAILED | scl12 sentiment + buzz | Sharpe 1.38, Fitness 0.44, Turnover 87.5% | Sentiment too reactive. |
| 037 | FAILED | snt value + buzz | Sharpe 1.31, Fitness 0.52 | Sentiment still noisy. |
| 038 | FAILED | fast d1 sentiment | Sharpe 1.11, Turnover 87% | Avoid fast_d1 sentiment for now. |
| 039 | FAILED | sentiment + operating income | Sharpe 1.59, Fitness 0.68 | Good Sharpe but failed Fitness. |
| 040 | FAILED | snt value + EBITDA/EV | Sharpe 1.11, Fitness 0.60 | Weak sentiment/value mix. |
| 041 | FAILED | sentiment + sales growth | Sharpe 1.04, Fitness 0.36 | Weak. |
| 042 | ERROR | eps_estimate_value ts_delta | Event input error | Do not ts_delta event/vector field directly. |
| 043 | ERROR | sales_estimate_value ts_delta | Event input error | Do not ts_delta event/vector field directly. |
| 044 | FAILED | dividend + return reversal | Sharpe 1.50, Fitness 0.83 | Good Sharpe, Fitness failed. |
| 045 | FAILED | dividend + close-vwap + reversal | Sharpe 0.60, Fitness 0.18 | Weak. |
| 046 | FAILED_SELF_CORRELATION | dividend + volume/adv20 + reversal | Sharpe 1.86, Fitness 1.07, selfcorr 0.935 | Strong but too correlated. |
| 047 | FAILED | dividend + intraday range + reversal | Sharpe 0.62, Fitness 0.19 | Weak. |
| 048 | FAILED | dividend + low vol20 + reversal | Sharpe 0.42, Fitness 0.22 | Weak. |
| 049 | FAILED | operating_income + reversal | Sharpe 0.95, Fitness 0.66 | Raw operating income weak. |
| 050 | FAILED | EBITDA + low vol60 | Sharpe 0.05, Fitness 0.01 | Dead branch. |
| 051 | FAILED | volume surprise x low vol20 | Sharpe 0.93, Fitness 0.50 | Product did not preserve volume edge. |
| 052 | FAILED | volume surprise + low vol20 | Sharpe 0.54, Fitness 0.29 | Low vol diluted signal. |
| 053 | PASSED_SUBMITTED | EBITDA/EV + 5d mean reversion | Sharpe 1.46, Fitness 1.05 | Simple value plus reversal submitted. |
| 054 | FAILED | cashflow/assets + operating improvement | Sharpe 1.29, Fitness 0.78 | Close but no reversal hurt. |
| 055 | FAILED | cashflow delta x low vol120 | Completely failed | Multiplication with vol weak. |
| 056 | FAILED | long cashflow rank + operating delta | Sharpe 1.35, Fitness 0.89 | Longer lookback close but failed. |
| 057 | FAILED | EBITDA/EV + ts_rank(-returns,10) | Sharpe 1.11, Fitness 0.58 | Worse than 5d mean reversal. |
| 058 | FAILED | EBITDA/EV + volume/adv20 | Sharpe 0.67, Fitness 0.29 | Volume did not complement value. |
| 059 | FAILED | EBITDA/EV + return delta | Sharpe 1.06, Fitness 0.55 | Delta worse than mean reversal. |
| 060 | FAILED | EBITDA/EV + low vol120 | Sharpe 0.06, Fitness 0.02 | Dead branch. |
| 061 | FAILED | ts_rank EBITDA/EV + 5d reversal | Sharpe 1.51, Fitness 0.98 | Very close but not passed. |
| 062 | FAILED | EBITDA/EV + close/high behavior | Sharpe -0.04, Fitness -0.01 | Dead branch. |
| 063 | FAILED | op_cash_flow_stddev HT alpha | Sharpe 1.52, Fitness 0.84 | Strong Sharpe, Fitness failed. |
| 064 | FAILED | smoothed op_cash_flow_stddev | Sharpe 0.85, Fitness 0.48, Turnover 11.81% | Over-smoothing killed signal strength. |
| 065 | FAILED | op_cash_flow_stddev + sales growth | Sharpe 1.48, Fitness 0.91, Turnover 21.78%, SubU 1.49 | Close; only Fitness failed. |
| 066 | FAILED | op_cash_flow_stddev level + reversal | Sharpe 1.16, Fitness 0.78, Turnover 13.12% | Level-rank branch weaker than delta branch. |
| 067 | FAILED | EUR TOP2500/COUNTRY analyst sweep (314 blocks, decay 5) | Best `anl69` Sharpe 1.97 / Fitness 1.58; 2 of 314 cleared Sharpe 1.25 + Fitness 1.0; 0 PASS | First EUR evidence: analyst single-field transforms top out at Sharpe 1.2-1.4; `LOW_2Y_SHARPE` fails 95.5%. |
| 068 | FAILED | EUR multi-universe sweep (2,100 blocks, decay 5) | Best legit Sharpe 2.51 / Fitness 1.16; 7 of 2,100 cleared both user thresholds; 0 PASS; 2 blocks degenerate | `pv37` snapshot volume is the strongest raw EUR signal but fails `LOW_SUB_UNIVERSE_SHARPE`; universes below TOP2500 collapse; `IS_LADDER_SHARPE` already active. |
| 069 | FAILED | EUR multi-universe sweep (1,809 blocks, decay 0) | Best `anl69` Sharpe 1.82 / Fitness 1.41 at 15.2% turnover; 8 of 1,809 cleared both; 0 PASS | Decay moves turnover, not Sharpe; `anl69` low-turnover cluster is the workspace's best risk-adjusted pocket; `HIGH_TURNOVER` 9.3%. |
| 070 | FAILED | USA analyst-growth sweep, 6 universes (3,550 blocks over 2 pages, decay 5) — **numbers corrected 2026-10-09** | Page 1: best out-of-sample Sharpe 1.54, 12 blocks >= 1.25, 1 clears Fitness >= 1.0 (annual_financing_cashflow_amount, true Sharpe 1.40 / Fitness 1.03). Page 2 (1,050 blocks, USA/TOP3000, previously unrecorded): best true Sharpe 1.23. 0 PASS, 6 PENDING | Field screen over 2,444 fields. The first parse read `Train Sharpe` into the Sharpe column and dropped page 2 — see `simulations/sweeps/superseded/README.md`. The real out-of-sample ceiling is lower than first recorded, and the five smaller universes contributed nothing above 1.25. |
| 071 | FAILED | Six-page multi-region bundle: KOR / AMR / EUR / GLB / USA (5,546 blocks; decay 5, USA 0-16) | 0 PASS, 42 PENDING, 35 blocks at Sharpe >= 1.25 with Fitness >= 1.0 (12 of them unevaluated). Best: KOR `oth176_lmt_close_eq_score` 2.36 / 1.67; USA IV-dispersion 2.61 / 1.88; AMR `mdl39` leaders unevaluated; GLB best Fitness 0.57 | First KOR-scope and GLB-scope evidence. Failures have moved from signal strength to book geometry (`CONCENTRATED_WEIGHT`), robustness and the consultant ladder (`IS_LADDER_SHARPE` in 96 of 174 USA blocks, `CLUSTER_TEST` in 27 EUR blocks). Only 19 of 5,524 expressions repeat earlier sweeps. |

## EUR Sweep Escalation Candidates (from 067 / 068 / 069)

These exact expressions are **already simulated** and are recorded here so they are never
re-proposed as new alphas. They are listed only as repair targets, because each is the
closest block in its sweep to clearing a check set. All are `FAILED`.

| Source | Expression | Sharpe | Fitness | Turnover | Failed checks | Why it is interesting |
|---|---|---:|---:|---:|---|---|
| 067 #1 | `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` | 1.97 | 1.58 | 5.78% | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Best Fitness in the analyst sweep; single-dataset ATOM shape; < 30% turnover for the IS-Ladder x0.85 relaxation. |
| 068 #614 | `scale(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 126))` | 2.51 | 1.09 | 47.29% | LOW_SUB_UNIVERSE_SHARPE | Closest block in the decay-5 sweep to passing; only one check failing. |
| 068 #615 | `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))` | 2.41 | 1.16 | 37.80% | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Highest Fitness among legitimate decay-5 blocks; non-`pv37` session-volume field. |
| 068 #620 | `rank(ts_scale(ts_backfill(anl10_salfy1_consensus_559, 21), 63))` | 1.67 | 1.09 | 6.69% | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Best low-turnover decay-5 option (6.69%), 15.91 bps margin. |
| 069 #1540 | `ts_quantile(ts_backfill(anl69_net_new_best_eeps_nxt_yr, 21), 63)` | 1.82 | 1.41 | 15.20% | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Best legitimate Sharpe+Fitness pair in the whole workspace; TOPCS1600 consultant scope; ATOM shape. |
| 069 #925 | `ts_quantile(ts_backfill(anl4_sadaf_netprofit_median, 21), 63)` | 1.81 | 1.28 | 10.99% | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Confirms the slow-analyst + `ts_quantile(..., 63)` pattern on a second family. |
| 069 #926 | `group_scale(ts_quantile(ts_backfill(anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_mean, 21), 63), sector)` | 1.66 | 0.84 | 21.34% | LOW_FITNESS, LOW_2Y_SHARPE | 2Y Sharpe passes only if the field is confirmed distinct; watch alias/dedup. |
| 069 #10 | `scale(ts_backfill(pv20_eps_indicator_3_feature12_394, 21))` | 1.32 | 1.09 | 19.12% | LOW_SHARPE, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE | Highest returns of the decay-0 sweep (12.99%); repair weight concentration, not Sharpe. |
| 069 #931 | `ts_zscore(ts_decay_linear(ts_backfill(anl4_af_div_low, 21), 21), 126)` | 1.53 | 1.01 | 7.70% | LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | 7.70% turnover, 14.26 bps margin. |
| 069 #5 | `ts_quantile(ts_decay_linear(ts_backfill(pv37_volume_153000, 21), 126), 252)` | 1.55 | 1.02 | 10.14% | LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE | Shows `pv37_volume_*` can be tamed to 10% turnover when double-smoothed. |

### Do Not Re-run (degenerate or artifact fields)

| Source | Expression | Reported | Why it must be discarded |
|---|---|---|---|
| 068 #1 | `ts_product(ts_backfill(pv37_low_14, 21), 63)` | Sharpe 11.18, Fitness 4.60, turnover 100.00%, DD 0.00%, 12 L / 218 S | Degenerate book: train Sharpe 0.00, pinned 100% turnover, zero drawdown. |
| 068 #5 | `normalize(ts_zscore(ts_backfill(adjfactor, 21), 126))` | Sharpe 1.94, Fitness 1.60, returns 31.20%, 295 L / 25 S | `adjfactor` is a price-adjustment factor, not a cross-sectional signal; fails CONCENTRATED_WEIGHT and IS_LADDER_SHARPE. |
| 070 | `net_9_feature3_predictor`, `option_return_bucket2_label_2`, `option_return_bucket3_prob1`, `adjfactor` | USA page 1: `net_9_feature3_predictor` 1.35 / 0.84; `option_return_bucket2_label_2` 1.20 / 0.34; `option_return_bucket3_prob1` 0.24 / 0.07; `adjfactor` 0.32 / 0.11 | Same artifact families as EUR: `net_9` is a synthetic/model feature, `option_return_bucket*` are bucket/probability series, `adjfactor` is a price-adjustment factor. Only `net_9_feature3_predictor` shows any strength here; the other three are simply weak in this region. Discard all four as alpha inputs. |
| 071 d3 | `ts_zscore(ts_backfill(adjfactor, 21), 252)` and `normalize(ts_backfill(adjfactor, 21))` | EUR TOP2500/INDUSTRY: Sharpe 1.80 / Fitness 1.24 (59.31% turnover) and Sharpe 1.66 / Fitness 1.08; second and third best EUR blocks in the bundle | `adjfactor` is a price-adjustment factor, not a cross-sectional signal; it also triggers CONCENTRATED_WEIGHT and, for the normalize form, IS_LADDER_SHARPE. Do not use in any region. |

## USA TOP3000 Escalation Candidate (from 070)

The single closest block to clearing all checks in the USA / D1 / TOP3000 / INDUSTRY sweep.
It is **already simulated** and is recorded here so it is never re-proposed as a new alpha;
it is a repair target only.

| Source | Expression | Sharpe | Fitness | Turnover | Failed checks | Why it is interesting |
|---|---|---:|---:|---:|---|---|
| 070 # (annual_financing_cashflow_amount) | `group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)` | 1.40 | 1.03 | 2.00% | LOW_SHARPE, LOW_2Y_SHARPE (fail set F19) | The only block in the page-1 USA sweep with Fitness >= 1.0 (1.03). True out-of-sample Sharpe is 1.40 (train 1.69), which still clears the 1.25 user threshold, so the only gap is the 2-year window. Low 2.00% turnover leaves room to increase signal strength carefully. |

### USA TOP3000 repair-target blocks (already simulated, failed)

Listed only as repair targets, not as new alphas. The Sharpe column is the out-of-sample
`Sharpe` from the dump (the corrected column); Train Sharpe was higher for every row.
Sorted by out-of-sample Sharpe.

| Source | Expression | Sharpe | Fitness | Turnover | Failed checks | Notes |
|---|---|---:|---:|---:|---|---|
| 070 | `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)` | 1.54 | 0.94 | 3.72% | LOW_SHARPE, LOW_FITNESS (F8) | Highest out-of-sample Sharpe in page 1 and the cleanest fitness-band target: only fails LOW_SHARPE + LOW_FITNESS. |
| 070 | `group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)` | 1.52 | 0.98 | 3.71% | LOW_SHARPE, LOW_FITNESS (F8) | Only fails LOW_SHARPE + LOW_FITNESS; Fitness 0.98 is very close to 1.0. |
| 070 | `group_rank(ts_backfill(eps_q1_estimate_asymmetry, 21), subindustry)` | 1.50 | 0.79 | 6.91% | LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE (F2) | Highest Sharpe among low-turnover legitimate blocks; fails on both Fitness and robustness. |
| 070 | `group_rank(ts_backfill(consensus_next_fiscal_year_interest_expense, 21), subindustry)` | 1.45 | 0.73 | 3.24% | LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE (F2) | Low turnover, clean book; robustness + Fitness gap. |
| 070 | `group_rank(ts_backfill(estimate_y1_skewness_book_value_ps, 21), market)` | 1.44 | 0.83 | 3.13% | LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE (F2) | Good returns (4.17%) at low turnover; robustness is the gap. |
| 070 | `group_rank(ts_backfill(op_expense_estimate_y1_skewness, 21), subindustry)` | 1.37 | 0.67 | 3.36% | LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE (F1) | Lower Fitness; only fails LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE — no sub-universe failure. |

## KOR / TOP600 escalation candidates (from 071)

Both are **already simulated**; recorded so they are never re-proposed as new alphas.

| Source | Expression | Sharpe | Fitness | Turnover | Failed checks | Why it is interesting |
|---|---|---:|---:|---:|---|---|
| 071 d1 #1 | `normalize(ts_backfill(oth176_lmt_close_eq_score, 21))` | 2.36 | 1.67 | 32.62% | LOW_2Y_SHARPE | Best Sharpe+Fitness pair in the whole 071 bundle and the only block in it that fails a single check. First KOR-scope candidate: single field, ATOM-shaped, INDUSTRY, Decay 5. |
| 071 d1 #2 | `zscore(ts_backfill(analyst_revisions_revenue_score, 21))` | 1.26 | 1.03 | 5.38% | LOW_SHARPE, CONCENTRATED_WEIGHT | 5.38% turnover; the repair is weight concentration, not strength. |

## USA implied-volatility escalation candidates (from 071)

**Already simulated.** The strongest USA surface in the workspace so far, and a different
mechanism from the exhausted USA fundamental/value branch. Every variant fails the same two
checks at decay 4, 6 and 8, so the repair is book construction, not smoothing.

| Source | Expression | Sharpe | Fitness | Turnover | Failed checks | Why it is interesting |
|---|---|---:|---:|---:|---|---|
| 071 d5 #1 | `iv_signal = zscore(implied_volatility_call_120 - implied_volatility_put_120) + rank(implied_volatility_call_120 / historical_volatility_120); cap_group = bucket(rank(cap), range="0.1,1,0.1"); group_neutralize(iv_signal, cap_group)` | 2.61 | 1.88 | 35.73% | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE | Best USA block recorded so far (Simulation 070's best was 1.54 / 0.98). IV dispersion vs realized vol, neutralized inside cap deciles. Decay 6, SUBINDUSTRY. |
| 071 d5 #2 | `iv_difference = implied_volatility_call_120 - implied_volatility_put_120; hv_group = bucket(rank(ts_rank(operating_income / cap, 250)), range="0.1,1,0.1"); group_neutralize(iv_difference, hv_group)` | 2.34 | 1.47 | 48.23% | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE | Same mechanism with an op-income/cap conditioning bucket; identical failures at decay 4. |
| 071 d5 #3 | `iv_difference = implied_volatility_call_120 - implied_volatility_put_120; hv_group = bucket(rank(ts_sum(vec_avg(nws12_afterhsz_sl), 60)), range="0.1,1,0.1"); group_neutralize(iv_difference, hv_group)` | 2.29 | 1.47 | 47.32% | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE | News-sentiment-conditioned bucket; shows the result is not bucket-specific. |
| 071 d5 #4 | `hv_group = bucket(rank(historical_volatility_120), range="0.1,1,0.1"); group_neutralize(rank(implied_volatility_call_120 - implied_volatility_put_120), hv_group)` | 2.21 | 1.07 | 32.91% | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE | Decay 8; decay alone does not clear the concentration failure. |

## Pending blocks (already simulated, no verdict — re-run for a result, do not re-propose)

These were still computing when the page was copied, so they are **unevaluated**, not clean.

| Source | Expression | Sharpe | Fitness | Turnover | Notes |
|---|---|---:|---:|---:|---|
| 071 d5 #5 | `rank(ts_rank(operating_income / cap, 250)) > 0.5 ? 1 : rank(-ts_delta(close, 2))` | 2.17 | 1.10 | 30.08% | Decay 4, SUBINDUSTRY. A conditional gate on the op-income/cap branch; needs a verdict before any conclusion. |
| 071 d5 #9 | `zscore(rank(-returns) + 0.25 * rank(ts_rank(fnd6_cptnewqv1300_epsfxq, 126)) + 0.25 * rank(ebitda / enterprise_value))` | 1.73 | 1.02 | 33.13% | Decay 16, SUBINDUSTRY. Includes the exhausted `ebitda / enterprise_value` component. |
| 071 d2 #1 | `group_zscore(ts_backfill(mdl39_12_val_mo_industry_rank, 21), subindustry)` | 1.69 | 1.39 | 7.62% | AMR TOP600; the top four AMR `mdl39_12_val_mo_*` blocks all lack verdicts. |
| 071 d2 #2 | `quantile(ts_backfill(mdl39_12_val_mo_sector_rank, 21))` | 1.63 | 1.49 | 7.57% | AMR TOP600; best Fitness among the pending AMR leaders. |

**Cross-region grouping/operator notes (not USA-specific):**

- `group_count` / `group_sum` / `group_std_dev` / `group_neutralize` wrappers over volume
  or grouping fields added turnover and `CONCENTRATED_WEIGHT` without adding Sharpe in EUR
  (067 #30/#45/#51, 068 #41/#102/#120, 069 #518/#920); Sharpe ranged 0.2-0.7 at 48-90%
  turnover. Treat grouping operators as a turnover/weight source, not a Sharpe source.
- `pv47_spret` (and `pv47_for_statssimple_only_spret`) are spurious-return fields: the
  EUR blocks `quantile(ts_backfill(anl69_pe_all_delay_1_expected_report_dt, 21))`, `winsorize(ts_rank(ts_backfill(pv47_for_statssimple_only_spret, 21), 21))`, and `group_zscore(ts_backfill(pv47_spret, 21), sector)` reached Sharpe -1.8 to -2.1 with damaged drawdown. Do not use `pv47_spret` as an alpha input.
