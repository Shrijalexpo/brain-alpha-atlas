---
title: Analysis and Simulation Reports — Experiment Index
---

# Analysis and Simulation Reports — Experiment Index

Centralized single source of truth and curated index for all **71 WorldQuant BRAIN Alpha experiments**, **13,319 multi-simulation sweep blocks**, regional performance analyses, and research ledgers in this repository. Each row below was taken directly from the canonical simulation records and sweep CSVs and verified line by line by `Tools/documentation-validation/verify_index.py`.

## Directory & Subfolder Navigation

| Subfolder / Resource | Entry Point | Contents & Scope |
|---|---|---|
| **Live Simulation & Sweep Analytics Hub** | [Module 18 — Live Simulation Hub](../Docs/18-simulation-results-and-sweep-analytics/index.md) | Executive leaderboard, cross-region findings, [USA 3,550-Block Sweep Analysis](../Docs/18-simulation-results-and-sweep-analytics/usa-3550-sweep-analysis.md), and [Full 71-Experiment Clickable Ledger](../Docs/18-simulation-results-and-sweep-analytics/master-experiment-ledger.md) |
| **`simulation-results/`** | [`simulation-results/`](simulation-results/) | Canonical experiment records (`001`–`071`) organized by region: [`USA/`](simulation-results/USA/), [`EUR/`](simulation-results/EUR/), [`KOR/`](simulation-results/KOR/), [`AMR/`](simulation-results/AMR/), [`GLB/`](simulation-results/GLB/), and [`multi-region/`](simulation-results/multi-region/) |
| **`alpha-research/`** | [`alpha-research/`](alpha-research/) | [Status & Duplicate Ledger](alpha-research/status-and-duplicate-ledger.md), [Past Simulations Narrative](alpha-research/past-simulations-ledger.md), [Lessons from Simulations](alpha-research/lessons-from-simulations.md), [Field Research Notebook](alpha-research/field-research-notebook.md), and [Simulation Template](alpha-research/simulation-template.md) |
| **`sweeps-and-experiments/`** | [`sweeps-and-experiments/`](sweeps-and-experiments/) | Parsed CSV, JSON, and Markdown reports for all bulk sweeps ([EUR 3-Sweep Summary](sweeps-and-experiments/SUMMARY.md), [USA 3,550-Block Summary](sweeps-and-experiments/20261008_071542_SUMMARY.md), [Multi-Region 5,546-Block Summary](sweeps-and-experiments/20261009_115500_SUMMARY.md)) |
| **`aggregate-analytics/`** | [`aggregate-analytics/`](aggregate-analytics/) | Cross-experiment quantitative summary and machine-readable [`master_experiments_catalog.csv`](aggregate-analytics/master_experiments_catalog.csv) |
| **`source-data/`** | [`source-data/`](source-data/) | Raw pasted multi-simulation platform exports (`20261008_071542.txt`, `20261009_115500.txt`) with MD5/SHA-256 provenance checksums |

**Reading the statuses:** `PASSED_SUBMITTED` / `PASSED_SUBMITTABLE` mean the platform checks
were cleared in the recorded session; `FAILED` means a required check failed;
`FAILED_SELF_CORRELATION` means the metrics were acceptable but the alpha was too similar to
an existing one; `ERROR` means the expression did not pass validation. See
[Sources and evidence policy](../Docs/reference/sources-and-policy.md) for how these statuses are assigned.

**Totals:** 71 recorded experiments — 3 cleared checks, 4 failed on self-correlation, 2 raised errors, 57 failed on performance or robustness, 5 bulk sweeps.

## Experiments that cleared the checks

Treat these as protected baselines: clone and compare against them, do not re-propose them as
new ideas.

| ID | Experiment | Sharpe | Fitness | Turnover | Expression | Lesson recorded |
|---:|---|---:|---:|---:|---|---|
| 026 | Submitted Alpha: TS-Ranked Value + TS-Ranked Growth + Smooth | 1.61 | 1.02 | 25.25% | `group_neutralize( rank(ts_rank(ebitda / enterprise_value, 126)) + rank(ts_rank(sales_growth, 126)) + rank(ts_m…` | This is the first recorded submittable alpha.; Smoothing the reversal component with `ts_mean(-returns, 5)` pushed Fitness above 1.; Do not suggest this exact alpha again. Treat it as a pr… |
| 027 | Submitted Cashflow Quality + Operating Improvement + Reversa | 1.39 | 0.73 in IS summary | 21.31% | `group_neutralize( rank(ts_rank(cashflow_op / assets, 126)) + rank(ts_delta(operating_income / assets, 63)) + r…` | This became a submitted alpha.; It uses a quality/improvement backbone plus the recurring 5-day mean-reversion component.; Do not suggest this exact expression again. |
| 053 | Submitted EBITDA/EV + 5-Day Mean Reversion | 1.46 | 1.05 | — | `rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))…` | Simple value plus short-term mean reversion worked.; Do not suggest this exact expression again. |

## Failed on self-correlation (metrics were acceptable)

These are the most instructive failures in the repository: the signal worked, but it was too
close to an alpha that already existed. Note the pattern — four of them share a
quality/improvement-plus-reversal backbone.

| ID | Experiment | Sharpe | Fitness | Turnover | Expression | Lesson recorded |
|---:|---|---:|---:|---:|---|---|
| 029 | Operating Income Quality + ROA Trend + Reversal | 1.76 | 1.21 | 18.73% | `group_neutralize( rank(ts_rank(operating_income / assets, 126)) + rank(ts_delta(return_assets, 126)) + rank(ts…` | Performance passed, but self-correlation failed.; The backbone was too similar to existing submitted alphas.; Avoid this exact structure. |
| 031 | Cashflow Quality + ROA Trend + Reversal | 1.71 | 1.13 | — | `group_neutralize( rank(ts_rank(cashflow_op / assets, 126)) + rank(ts_delta(return_assets, 126)) + rank(ts_mean…` | Strong metrics, but failed self-correlation.; `cashflow_op/assets`, `return_assets`, and `ts_mean(-returns,5)` are now crowded in the user's submitted set. |
| 033 | Operating Income Quality + EBITDA/EV Trend + Reversal | — | — | — | `group_neutralize( rank(ts_rank(operating_income / assets, 126)) + rank(ts_delta(ebitda / enterprise_value, 126…` | Changing ROA trend to value trend did not solve correlation.; Avoid this same quality plus value plus 5-day reversal backbone. |
| 046 | Dividend + Volume Surprise + Reversal | 1.86 | 1.07 | — | `group_neutralize( zscore( rank(dividend) + rank(volume / adv20) + rank(-returns) ), industry )…` | Strong performance, but failed self-correlation.; Volume/ADV20 was powerful but crowded with existing signals. |

## Errors (expression did not validate)

| ID | Experiment | Sharpe | Fitness | Turnover | Expression | Lesson recorded |
|---:|---|---:|---:|---:|---|---|
| 042 | EPS Estimate Delta Error | — | — | — | `rank(ts_delta(eps_estimate_value, 20))…` | `eps_estimate_value` behaved like event/vector data, not a normal matrix time series.; Do not use `ts_delta()` directly on this field without proper conversion. |
| 043 | Sales Estimate Delta Error | — | — | — | `rank(ts_delta(sales_estimate_value, 20))…` | `sales_estimate_value` behaved like event/vector data.; Use only valid matrix fields or convert vector/event fields with appropriate `vec_*` operators first. |

## Bulk sweeps

Large parameter scans. These are field screens, not single hand-built alphas; the full
per-block data lives in `Analysis and Simulation Reports/sweeps-and-experiments/`.

| ID | Sweep | Blocks | Region(s) | Best recorded result |
|---:|---|---:|---|---|
| 067 | EUR TOP2500/COUNTRY analyst sweep, decay 5 | 314 | EUR TOP2500 | `anl69_sales_best_eeps_cur_yr` Sharpe 1.97 / Fitness 1.58; 0 passed all checks |
| 068 | EUR multi-universe sweep, decay 5 | 2,100 | EUR (5 universes) | Sharpe 2.51 / Fitness 1.16 on `pv37` volume; 0 passed; 2 degenerate blocks |
| 069 | EUR multi-universe sweep, decay 0 | 1,809 | EUR (5 universes) | Sharpe 1.82 / Fitness 1.41 on `anl69`; 0 passed |
| 070 | USA analyst-growth sweep, decay 5, 6 universes | 3,550 (2 pages) | USA (6 universes) | Page 1: Sharpe 1.54 / Fitness 0.98; 1 block cleared Fitness 1.0. Page 2: Sharpe 1.23 |
| 071 | Multi-region bundle (KOR/AMR/EUR/GLB/USA), 6 pages | 5,546 | KOR, AMR, EUR, ALL, USA | KOR Sharpe 2.36 / Fitness 1.67; USA IV Sharpe 2.61 / Fitness 1.88; 0 passed, 42 PENDING |

## Failed experiments (chronological)

The useful part of this table is the lesson column: each entry records why the attempt stopped,
so the same ground is not re-covered. The first ~26 experiments are a single narrative —
searching for a value/quality backbone in USA — and are best read in sequence; the
later ones branch into sentiment, dividend, EBITDA/EV and cash-flow-dispersion families.

| ID | Experiment | Sharpe | Fitness | Turnover | Expression | Lesson recorded |
|---:|---|---:|---:|---:|---|---|
| 001 | Positive Days Momentum | 0.99 | 1.13 | 3.04% | `positive_days = ts_sum(returns > 0 ? 1 : 0, 250); trade_when( volume > adv20, positive_days, -1 )…` | Fitness and Turnover were acceptable.; Sharpe was below the likely threshold.; Avoid repeating this exact form unless testing ranked or normalized variants. |
| 002 | Operating Income / Cap Plus Return Reversion | 1.14 | 0.84 | 22.78% | `zscore( rank(operating_income / cap) + 0.4 * rank(-returns) )…` | Close but not passing.; Both Sharpe and Fitness needed improvement.; The daily return component was noisy. |
| 003 | Operating Income / Cap Plus Time-Series Return Rank | 1.29 | 0.60 | 63.33% | `zscore( rank(operating_income / cap) + 0.4 * rank(-ts_rank(returns, 20)) )…` | Sharpe passed.; Fitness failed because Turnover was very high.; Do not repeat without changing Decay or smoothing/reducing the return component. |
| 004 | Operating Income / Cap Plus Smoothed Returns | 1.05 | 0.98 | — | `zscore( rank(operating_income / cap) + 0.4 * rank(-ts_mean(returns, 5)) )…` | Worse Sharpe than the `ts_rank(returns, 20)` variant.; Fitness was close but still below target. |
| 005 | Smoothed Operating Income / Cap Plus Return Reversion | 1.01 | 0.89 | — | `zscore( rank(ts_mean(operating_income / cap, 4)) + 0.4 * rank(-returns) )…` | Smoothing the slow-moving fundamental component did not help enough. |
| 006 | Operating Income / Cap Plus Volatility-Adjusted Returns | 0.99 | 0.86 | — | `zscore( rank(operating_income / cap) + 0.4 * rank(-returns / ts_std_dev(returns, 20)) )…` | Volatility adjustment did not improve this alpha family. |
| 007 | Dividend, Volume Surprise, Return Reversion | 1.78 | 0.67 | 57.5% | `zscore( rank(dividend) + 0.3 * rank(volume / adv20) + 0.2 * rank(-returns) )…` | Strong Sharpe.; Fitness failed because Turnover was too high.; Next fix should target Turnover, not signal strength. |
| 008 | Raw Operating Income Time-Series Rank | below about 0.5 | — | — | `rank(ts_rank(operating_income, 12))…` | Raw operating income alone was weak. |
| 009 | Raw Operating Income Time-Series Mean | below about 0.5 | — | — | `rank(ts_mean(operating_income, 4))…` | Raw operating income alone was weak. |
| 010 | Raw Operating Income Time-Series Delta | below about 0.5 | — | — | `rank(ts_delta(operating_income, 4))…` | Raw operating income changes were weak in the tested settings. |
| 011 | Quality Value Composite | 0.46 | 0.22 | 3.98% | `group_neutralize( rank(return_equity) + rank(cashflow_op / assets) - rank(enterprise_value / ebitda), bucket(r…` | Structural checks were acceptable.; Signal was too weak. |
| 012 | Large Multi-Factor Quality/Value Composite | -0.28 | — | — | `group_neutralize( rank(return_equity) + rank(return_assets) + rank(cashflow_op / assets) + rank(current_ratio)…` | Large linear stacking made performance worse. |
| 013 | Nonlinear Profitability Cash Flow Product | -1.01 | — | — | `group_neutralize( rank((return_equity * cashflow_op) / (assets * enterprise_value)) - rank(debt / assets), buc…` | Nonlinear multiplication made performance much worse. |
| 014 | Cash Flow Yield | 0.41 | — | — | `group_neutralize( rank(cashflow_op / enterprise_value), bucket(rank(cap), range="0.1,1,0.1") )…` | Positive but weak.; Best current base direction from the latest tests.; Add one complementary factor at a time. |
| 015 | Cash Flow Yield + ROE + Reversal | 1.18 | 0.71 | 30.35% | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(return_equity) + rank(-returns), bucket(rank(cap…` | Close, but not submittable.; Adding `-returns` materially improved the cashflow/value branch.; Keep as a useful ancestor, but do not suggest this exact alpha again. |
| 016 | Cash Flow Yield + ROA + Reversal | — | — | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(return_assets) + rank(-returns), bucket(rank(cap…` | `return_assets` was worse than `return_equity` in this branch.; Do not repeat this exact substitution unless testing a genuinely new transformation. |
| 017 | Cash Flow Yield + ROE + Current Ratio + Reversal | 1.19 | 0.66 | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(return_equity) + rank(current_ratio) + rank(-ret…` | Slight Sharpe improvement versus Simulation 015, but Fitness fell.; `current_ratio` did not help enough in this factor family.; Do not suggest this exact alpha again. |
| 018 | Cash Flow Yield + ROE + ROA + Reversal | — | — | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(return_equity) + rank(return_assets) + rank(-ret…` | Stacking similar profitability factors hurt performance.; Avoid adding both `return_equity` and `return_assets` to this branch without a new reason. |
| 019 | Cash Flow Yield + Operating Income / Assets + Reversal | — | — | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(operating_income / assets) + rank(-returns), buc…` | Replacing ROE/ROA with `operating_income / assets` did not solve the problem.; This reinforced the lesson that the operating-income family was weak in the tested setup. |
| 020 | Cash Flow Yield + Sales Growth + Reversal | 1.21 | 0.58 | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(sales_growth) + rank(-returns), bucket(rank(cap)…` | Closest cashflow/value branch before switching to EBITDA/EV.; `sales_growth` helped more than the extra profitability factors.; Failed Fitness; do not repeat exact expression. |
| 021 | Cash Flow Yield + Sales Growth + Current Ratio + Reversal | — | — | — | `group_neutralize( rank(cashflow_op / enterprise_value) + rank(sales_growth) + rank(current_ratio) + rank(-retu…` | `current_ratio` hurt the best cashflow/value-growth branch.; Do not suggest this exact alpha again. |
| 022 | EBITDA Yield + Sales Growth + Reversal | 1.21 | — | — | `group_neutralize( rank(ebitda / enterprise_value) + rank(sales_growth) + rank(-returns), bucket(rank(cap), ran…` | Sharpe did not improve versus cashflow/EV, but Sub-universe Sharpe improved.; EBITDA/EV looked like a better robustness base than cashflow/EV.; Failed overall; do not suggest exact express… |
| 023 | EBITDA Yield + ROE + Sales Growth | 0.28 | — | — | `group_neutralize( rank(ebitda / enterprise_value) + rank(return_equity) + rank(sales_growth), bucket(rank(cap)…` | Replacing `-returns` with `return_equity` badly hurt performance.; In this branch, `return_equity` should not replace the reversal component. |
| 024 | Time-Series Ranked EBITDA Yield + Sales Growth + Reversal | 1.36 | 0.68 | — | `group_neutralize( rank(ts_rank(ebitda / enterprise_value, 126)) + rank(sales_growth) + rank(-returns), bucket(…` | First branch to pass the Sharpe threshold.; Fitness still failed, so the signal needed smoother/more robust components.; Time-series rank on `ebitda / enterprise_value` was a major improve… |
| 025 | Time-Series Ranked EBITDA Yield + Time-Series Ranked Sales G | 1.78 | 0.97 | — | `group_neutralize( rank(ts_rank(ebitda / enterprise_value, 126)) + rank(ts_rank(sales_growth, 126)) + rank(-ret…` | Very strong, but still not submittable because Fitness was just below 1.; Time-series ranking `sales_growth` was a major improvement.; Exact expressionshould not be repeated; use only as… |
| 028 | Growth Acceleration + Liquidity + Reversal | 0.87 | 0.47 | 16.47% | `group_neutralize( rank(ts_rank(current_ratio, 126)) + rank(ts_delta(sales_growth, 63)) + rank(ts_mean(-returns…` | Different factor family, but too weak.; Liquidity plus growth acceleration was not strong enough. |
| 030 | Operating Income Quality + ROA Trend + 20-Day Reversal | 1.19 | — | — | `group_neutralize( rank(ts_rank(operating_income / assets, 126)) + rank(ts_delta(return_assets, 126)) + rank(ts…` | Longer mean-reversion window reduced signal strength.; Failed to preserve the strong performance of Simulation 029. |
| 032 | Operating Income Quality + Current Ratio Trend + Reversal | 1.50 | 0.96 | — | `group_neutralize( rank(ts_rank(operating_income / assets, 126)) + rank(ts_delta(current_ratio, 126)) + rank(ts…` | Almost passed, but Fitness missed.; More distinct than ROA variants, but still not enough. |
| 034 | Current Ratio + Sales Growth + Reversal | 0.66 | — | — | `group_neutralize( rank(ts_rank(current_ratio, 126)) + rank(ts_delta(sales_growth, 63)) + rank(ts_mean(-returns…` | Liquidity family was weak.; Do not prioritize `current_ratio` as the main signal in this setup. |
| 035 | Debt/Assets + Sales Growth + Reversal | 0.91 | — | — | `group_neutralize( rank(ts_rank(debt / assets, 126)) + rank(ts_rank(sales_growth, 126)) + rank(ts_mean(-returns…` | Leverage plus growth was still weak.; Liquidity/leverage family was not promising on USA TOP3000 D1 in these tests. |
| 036 | SCL12 Sentiment + Buzz | 1.38 | 0.44 | 87.5% | `rank(ts_rank(scl12_sentiment, 126)) + rank(ts_delta(scl12_buzz, 21)) + rank(ts_mean(-returns, 5))…` | Sentiment had predictive power but turnover was too high.; Pure sentiment/buzz signals were too reactive. |
| 037 | SNT Value + SNT Buzz | 1.31 | 0.52 | — | `rank(ts_rank(snt_value, 126)) + rank(ts_rank(snt_buzz, 63)) + rank(ts_mean(-returns, 5))…` | Better than fast sentiment, but still failed Fitness.; Sentiment remained too noisy. |
| 038 | Fast D1 Sentiment | 1.11 | — | 87% | `rank(ts_delta(scl12_sentiment_fast_d1, 10)) + rank(ts_rank(scl12_buzz_fast_d1, 63)) + rank(ts_mean(-returns, 5…` | Fast D1 sentiment fields produced very high turnover.; Avoid `*_fast_d1` sentiment fields for now. |
| 039 | Sentiment + Operating Income Quality | 1.59 | 0.68 | — | `rank(ts_rank(scl12_sentiment, 252)) + rank(ts_rank(operating_income / assets, 126)) + rank(ts_mean(-returns, 5…` | Good Sharpe but failed Fitness.; Mixing sentiment with slower fundamentals still did not pass. |
| 040 | SNT Value + EBITDA/EV | 1.11 | 0.60 | — | `rank(ts_rank(snt_value, 252)) + rank(ts_rank(ebitda / enterprise_value, 126)) + rank(ts_mean(-returns, 5))…` | Weak alpha after mixing sentiment with value.; Do not prioritize this sentiment/value combination. |
| 041 | Sentiment + Sales Growth | 1.04 | 0.36 | — | `rank(ts_rank(scl12_sentiment, 252)) + rank(ts_delta(sales_growth, 63)) + rank(ts_mean(-returns, 5))…` | Weak and noisy.; Sentiment dataset was paused after this branch. |
| 044 | Dividend + Return Reversal | 1.50 | 0.83 | — | `group_neutralize( zscore( rank(dividend) + 0.5 * rank(-returns) ), industry )…` | Strong Sharpe, but Fitness failed.; Settings alone were not enough to fix it. |
| 045 | Dividend + Close/VWAP + Reversal | 0.60 | 0.18 | — | `group_neutralize( zscore( rank(dividend) + rank((close - vwap) / vwap) + rank(-returns) ), industry )…` | Weak. Drop this branch. |
| 047 | Dividend + Intraday Close Range + Reversal | 0.62 | 0.19 | — | `group_neutralize( zscore( rank(dividend) + rank((close - low) / (high - low)) + rank(-returns) ), industry )…` | Weak. Drop this branch. |
| 048 | Dividend + Low Volatility + Reversal | 0.42 | 0.22 | — | `group_neutralize( zscore( rank(dividend) + rank(-historical_volatility_20) + rank(-returns) ), industry )…` | Bad result. Low volatility did not complement the dividend branch. |
| 049 | Operating Income + Reversal | 0.95 | 0.66 | — | `group_neutralize( zscore( rank(operating_income) + rank(-returns) ), industry )…` | Best of that small fundamental batch, but still weak.; Raw operating income remained unreliable. |
| 050 | EBITDA + Low 60-Day Volatility | 0.05 | 0.01 | — | `group_neutralize( zscore( rank(ebitda) + rank(-historical_volatility_60) ), industry )…` | Very poor. Drop this branch. |
| 051 | Volume Surprise x Low Volatility | 0.93 | 0.50 | — | `rank(volume / adv20) * rank(-historical_volatility_20)…` | Medium but not close enough.; Multiplying volume by low volatility did not preserve the strong standalone volume signal. |
| 052 | Volume Surprise + Low Volatility | 0.54 | 0.29 | — | `rank(volume / adv20) + rank(-historical_volatility_20)…` | Weak. Adding low volatility diluted the volume signal. |
| 054 | Cashflow Quality + Operating Improvement Without Reversal | 1.29 | 0.78 | — | `rank(ts_rank(cashflow_op / assets, 126)) + rank(ts_delta(operating_income / assets, 63))…` | Close but failed Fitness.; Removing the reversal component reduced submission quality. |
| 055 | Cashflow Improvement x Low Volatility | — | — | — | `rank(ts_delta(cashflow_op / assets, 63)) * rank(-historical_volatility_120)…` | Multiplication with low volatility was not useful here. |
| 056 | Long Lookback Cashflow Quality + Operating Improvement | 1.35 | 0.89 | — | `rank(ts_rank(cashflow_op / assets, 252)) + rank(ts_delta(operating_income / assets, 126))…` | Close, but still failed Fitness.; Longer lookbacks helped but did not make the alpha submittable. |
| 057 | EBITDA/EV + TS-Ranked Returns | 1.11 | 0.58 | — | `rank(ebitda / enterprise_value) + rank(ts_rank(-returns, 10))…` | Worse than the submitted 5-day mean-reversion version.; `ts_mean(-returns,5)` was better than `ts_rank(-returns,10)`. |
| 058 | EBITDA/EV + Volume Surprise | 0.67 | 0.29 | — | `rank(ebitda / enterprise_value) + rank(volume / adv20)…` | Volume did not complement EBITDA/EV in this test. |
| 059 | EBITDA/EV + Return Delta | 1.06 | 0.55 | — | `rank(ebitda / enterprise_value) + rank(ts_delta(-returns, 5))…` | Return delta was worse than 5-day mean reversion. |
| 060 | EBITDA/EV + Low Historical Volatility | 0.06 | 0.02 | — | `rank(ebitda / enterprise_value) + rank(-historical_volatility_120)…` | Dead branch. Low volatility did not complement EBITDA/EV. |
| 061 | TS-Ranked EBITDA/EV + 5-Day Mean Reversion | 1.51 | 0.98 | — | `rank(ts_rank(ebitda / enterprise_value, 126)) + rank(ts_mean(-returns, 5))…` | Very close, but missed Fitness by about 0.02.; This is a strong family, but exact expression should not be repeated. |
| 062 | EBITDA/EV + Close/High Behavior | -0.04 | -0.01 | — | `rank(ebitda / enterprise_value) + rank(ts_mean(close / high - 1, 5))…` | Dead branch. Close/high behavior did not work here. |
| 063 | High-Turnover Operating Cash Flow Estimate Stddev | 1.52 | 0.84 | — | `zscore( rank(ts_delta(op_cash_flow_stddev, 10)) + 0.4 * rank(volume / adv20) - 0.2 * rank(returns) )…` | Strong Sharpe but failed Fitness.; Needs smoothing or persistence, but exact expression should not be repeated. |
| 064 | Smoothed Operating Cash Flow Estimate Dispersion | 0.85 | 0.48 | 11.81% | `zscore( rank(ts_mean(ts_delta(op_cash_flow_stddev, 20), 20)) + 0.3 * rank(ts_mean(-returns, 5)) )…` | Failed because Sharpe and Fitness were both below threshold.; Turnover, weight distribution, sub-universe Sharpe, and competition challenge checks passed.; The 20-day delta averaged over 2… |
| 065 | Operating Cash Flow Estimate Dispersion + Sales Growth + Rev | 1.48 | 0.91 | 21.78% | `zscore( rank(ts_delta(op_cash_flow_stddev, 10)) + 0.4 * rank(ts_rank(sales_growth, 126)) + 0.2 * rank(ts_mean(…` | Failed only on Fitness.; Sharpe, turnover, weight distribution, sub-universe Sharpe, and challenge checks passed.; This is a strong repair versus Simulation 064 and confirms the faster `op…` |
| 066 | Operating Cash Flow Estimate Dispersion Level + Reversal | 1.16 | 0.78 | 13.12% | `zscore( rank(ts_rank(op_cash_flow_stddev, 63)) + 0.3 * rank(ts_mean(-returns, 5)) )…` | Failed on Sharpe and Fitness.; Turnover was acceptable, but the level/rank version was weaker than the 10-day delta version. |


## What the index shows at a glance

- **Three of 71 experiments cleared the checks**, and two of those were submitted. The
  submitted family is `ts_rank(ebitda / enterprise_value, 126)` + `ts_rank(sales_growth, 126)`
  + a smoothed reversal, optionally inside a size bucket.
  See [experiment 026](simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md).
- **Four experiments were killed by self-correlation, not by performance** — the strongest
  evidence that in this workspace the binding constraint on a working signal is similarity to
  what already exists, not raw Sharpe.
- **The `ERROR` entries are both the same mistake**: applying `ts_delta` directly to an
  event/vector estimate field.
- **Bulk sweeps dominate the recent record**: 5,546 blocks in the latest bundle produced 0
  passes. Large scans are useful for mapping a surface, but they have not produced a passing
  alpha here; the two submissions came from small, deliberate iterations.
- **Train-vs-out-of-sample gap is material.** In the USA sweep the two columns disagreed in
  2,448 of 2,500 blocks. Quote the out-of-sample column.
