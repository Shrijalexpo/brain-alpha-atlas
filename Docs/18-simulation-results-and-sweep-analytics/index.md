# Module 18 — Live Simulation Results & Multi-Region Sweep Hub

This hub is the central analytical dashboard for **expert WorldQuant BRAIN consultants** and active researchers. It consolidates every recorded simulation (`001–071`), all **13,319 multi-simulation sweep blocks** across five regional exports (`USA, EUR, KOR, AMR, GLB`), factor-screening distributions, candidate repair queues, and the live update pipeline.

## Quick Navigation for Expert Consultants

| Analytical View | Target Page | Contents & Scope |
|---|---|---|
| **USA 3,550-Block Factor Screening** | [USA 3,550-Block Sweep Analysis](usa-3550-sweep-analysis.md) | Complete metric distributions, operator ranking (`group_rank` vs `group_zscore`), field family scorecard across 2,444 fields, `F1–F21` check breakdowns, and Group A/B/C candidate shortlists |
| **Complete 71-Experiment Ledger** | [Full 71-Experiment & Sweep Ledger](master-experiment-ledger.md) | Every individual Alpha simulation (`001–066`) and bulk sweep (`067–071`) with exact Fast Expressions, settings, Sharpe, Fitness, Turnover, Drawdown, Margin, and verdicts |
| **Empirical Case Studies & 26 Lessons** | [Module 17 — Case Studies & Lessons](../17-case-studies-and-lessons-learned/index.md) | Post-mortems on the `024 -> 026` breakthrough, the self-correlation wall, sentiment noise traps, `anl69` slow-analyst signals, and lessons `L-001` through `L-026` |
| **Raw Machine-Readable Exports** | [`Analysis and Simulation Reports/`](../../Analysis%20and%20Simulation%20Reports/) | Normalized CSV/JSON tables, source dumps, and regional simulation files |

## 1. Submitted & Top-Performing Alpha Leaderboard

Across 71 structured experiments and 13,319 sweep blocks, three USA Alphas passed all submission checks (`SUBMITTED`), while several high-Sharpe candidates across `USA`, `EUR`, and `KOR` stand one targeted repair away from eligibility:

| ID | Region / Univ | Neutralization / Decay | Sharpe | Fitness | Turnover | Returns | Drawdown | Margin | Status & Bottleneck | Core Expression Structure |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **`026`** | `USA / TOP3000` | `SUBINDUSTRY / 4` | **`1.86`** | **`1.30`** | `24.16%` | `9.96%` | `6.66%` | `8.25 bps` | **`SUBMITTED (PASS)`** | `0.5*ts_rank(ebitda/ev,252) + 0.3*ts_rank(sales_growth,252) + 0.2*rank(ts_mean(-returns,5))` |
| **`027`** | `USA / TOP3000` | `SUBINDUSTRY / 4` | **`1.93`** | **`1.47`** | `23.51%` | `11.15%` | `6.82%` | `9.48 bps` | **`SUBMITTED (PASS)`** | `0.45*rank(cashflow_op/ev) + 0.35*ts_rank(ts_delta(operating_income/assets,60),252) + 0.20*rank(ts_mean(-returns,5))` |
| **`053`** | `USA / TOP3000` | `SUBINDUSTRY / 0` | **`1.28`** | **`1.06`** | `39.18%` | `13.23%` | `9.11%` | `6.75 bps` | **`SUBMITTED (PASS)`** | `rank(ebitda/ev) + rank(-returns)` |
| **`071-U1`** | `USA / TOP3000` | `SUBINDUSTRY / 4` | **`2.61`** | **`1.88`** | `26.82%` | `12.50%` | `5.84%` | `9.32 bps` | `FAIL (HIGH_TURNOVER / 2Y)` | `call_breakeven_90 - put_breakeven_90` (Implied volatility dispersion) |
| **`071-K1`** | `KOR / TOP600` | `MARKET / 4` | **`1.89`** | **`1.80`** | `4.12%` | `14.20%` | `8.90%` | `68.90 bps` | `FAIL (SUB_UNIVERSE)` | `ts_decay_linear(anl69_..., 10)` (Slow analyst consensus revision) |
| **`070-A1`** | `USA / TOP3000` | `INDUSTRY / 5` | **`1.54`** | `0.94` | `3.72%` | `4.66%` | `5.57%` | `25.08 bps` | `FAIL (F8: LOW_FITNESS)` | `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)` |
| **`070-A2`** | `USA / TOP3000` | `INDUSTRY / 5` | **`1.52`** | `0.98` | `3.71%` | `5.16%` | `11.90%` | `27.82 bps` | `FAIL (F8: LOW_FITNESS)` | `group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)` |
| **`070-A3`** | `USA / TOP3000` | `INDUSTRY / 5` | **`1.40`** | **`1.03`** | `2.00%` | `6.73%` | `5.97%` | `67.19 bps` | `FAIL (F19: LOW_2Y_SHARPE)` | `group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)` |
| **`068-E1`** | `EUR / TOP2500` | `COUNTRY / 5` | **`1.46`** | `0.81` | `4.85%` | `4.92%` | `7.10%` | `20.28 bps` | `FAIL (LOW_FITNESS)` | `group_rank(ts_backfill(anl15_..., 21), sector)` |

## 2. Multi-Simulation Sweep Registry (13,319 Total Blocks)

All large-scale simulation exports are normalized by `Tools/simulation-processing/brain_sweep_parser.py` into deterministic CSV, JSON, and Markdown summaries with strict separation between `Train Sharpe` (in-sample) and `Sharpe` (out-of-sample):

| Sweep ID | Exp ID | Region & Universes | Neutralization / Decay | Total Blocks | Sharpe >= 1.25 | Fitness >= 1.0 | PASS | Top OOS Sharpe | Primary Signal Family & Key Finding |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| **`20261004_171500`** | [`067`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/067_eur_top2500_country_analyst_sweep.html) | `EUR / TOP2500` | `COUNTRY / 5` | `1,723` | `1` | `0` | `0` | `1.25` | Analyst estimate backfill screen; country neutralization leaves sector drift |
| **`20261005_123752`** | [`068`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/068_eur_multi_universe_decay5_sweep.html) | `EUR / 6 Universes` | `COUNTRY / 5` | `2,000` | `10` | `0` | `0` | `1.46` | Multi-universe `anl10/anl15` screen; `Decay 5` lifts median Sharpe by `+0.025` over `Decay 0` |
| **`20261006_100742`** | [`069`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/069_eur_multi_universe_decay0_sweep.html) | `EUR / 5 Universes` | `COUNTRY / 0` | `500` | `0` | `0` | `0` | `1.22` | Controlled `Decay 0` comparison against `068`; higher turnover and lower Fitness |
| **`20261008_071542`** | [`070`](usa-3550-sweep-analysis.md) | `USA / 6 Universes` | `INDUSTRY / 5` | **`3,550`** | **`12`** | **`1`** | `0` | **`1.54`** | 2,444-field screen; `group_rank` generates 80% of all Sharpe `>= 1.0` alphas |
| **`20261009_115500`** | [`071`](../../Analysis%20and%20Simulation%20Reports/simulation-results/multi-region/071_multi_region_bundle_20261009.html) | `KOR, AMR, EUR, GLB, USA` | `Multi / 4` | **`5,546`** | **`89`** | **`42`** | `0` | **`2.61`** | 6-dump regional bundle; USA option breakeven (`2.61`) and KOR `anl69` (`1.89`) lead |

## 3. Regional Research Playbook (Cross-Region Findings)

| Region | Tested Universes | Best Performing Field Families | Preferred Neutralization | Primary Submission Gate Bottleneck |
|---|---|---|---|---|
| **USA** | `TOP3000` (primary), `TOPSP500`, `TOP2000`, `TOP1000`, `TOP500`, `TOP200` | Option implied-volatility breakeven (`pv / option`), quarterly profit/margin growth (`netprofit_actual_q1_qoq_growth`), enterprise multiples (`ebitda/ev`, `cashflow_op/ev`) | `SUBINDUSTRY` or `INDUSTRY` | **Self-Correlation (`> 0.70`)** on value+reversal blends; **`LOW_SUB_UNIVERSE_SHARPE`** on single analyst fields |
| **EUR** | `TOP2500`, `TOP1200`, `TOP800`, `TOP400`, `TOPSP600` | Analyst consensus revisions (`anl15`, `anl10`) wrapped in `group_rank(..., sector)` with `Decay = 5` | `INDUSTRY` or `SUBINDUSTRY` (avoid bare `COUNTRY`) | **`LOW_FITNESS` (`0.65–0.85`)** due to moderate annualized return spreads (`3.5%–5.0%`) |
| **KOR** | `TOP600` | Broker consensus & earnings revision slopes (`anl69`, `anl14`) smoothed with `ts_decay_linear(x, 10)` | `MARKET` or `SECTOR` | **`LOW_SUB_UNIVERSE_SHARPE`** and **`CONCENTRATED_WEIGHT`** in smaller industry buckets |
| **AMR** | `TOP600` | Fundamental cash-flow yields and multi-quarter estimate revisions | `SECTOR` or `COUNTRY` | **Data coverage gaps** across multi-currency Latin American/Canadian listings |
| **GLB** | `ALL / LARGE`, `TOPDIV3000` | Slow cross-sectional valuation and quality rankings | `COUNTRY` + `SECTOR` (`group_cartesian_product`) | **`LOW_2Y_SHARPE`** and currency/country concentration |

## 4. Continuous Simulation Update Workflow

Whenever new simulation batches are exported from WorldQuant BRAIN, update the repository and GitHub Pages wiki using the four-step pipeline:

```bash
# 1. Parse raw simulation export (.rtf or .txt) into normalized CSV/JSON/MD tables
python3 Tools/simulation-processing/brain_sweep_parser.py "path/to/Simulation Results.rtf"

# 2. Reconcile experiment records against the master index and sweep summaries
python3 Tools/documentation-validation/verify_index.py

# 3. Validate Markdown tables, links, and privacy guards across Docs/
python3 Tools/documentation-validation/check_docs.py Docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS

# 4. Build strict MkDocs site and scan output HTML
.venv-docs/bin/mkdocs build --strict
python3 Tools/documentation-validation/check_docs.py --text-scan site
```
