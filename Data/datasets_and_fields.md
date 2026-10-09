# WorldQuant BRAIN Data Notes

This file records datasets and fields shared in the conversation.

## Data Hierarchy

WorldQuant BRAIN data is organized as:

```text
Dataset Category -> Dataset -> Data Field -> Alpha Expression
```

Examples:

- Dataset Category: Price/Volume
- Dataset: PV1
- Data Fields: `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`, `adv20`

## Dataset Categories Mentioned

Before consultant level, BRAIN shows fewer categories. Consultant-level access can include more regions and more datasets.

Categories or dataset families mentioned:

- Price Volume Data
- Company Fundamental Data for Equity
- Analyst Estimate Data
- Volatility Data
- Relationship Data
- Fundamental Scores
- News/Sentiment/RavenPack style data

## Recommended Dataset Priority

Highest priority:

1. Company Fundamental Data for Equity
2. Price Volume Data
3. Analyst Estimate Data for Equity
4. Volatility Data
5. Relationship Data
6. News and Sentiment data, later

## Company Fundamental Data for Equity

This was the main dataset discussed. It contains fields related to profitability, valuation, cash flow, growth, balance sheet strength, and efficiency.

Fields shared or discussed:

```text
operating_income
return_equity
return_assets
ebitda
ebit
income
enterprise_value
bookvalue_ps
cashflow_op
cashflow
cash
sales_growth
assets
debt
current_ratio
revenue
sales
inventory_turnover
cap
dividend
```

Field search notes:

- `operating_income` appeared as a Matrix field with high alpha count.
- Other search results included vector fields like `fnd6_oidbps`, `fnd6_ops`, and `fnd6_oiadps`.
- Prefer Matrix fields as a beginner.
- Vector fields may be metadata-like or less flexible for ordinary time-series alpha construction.

## Fields And Economic Meaning

`operating_income`

- Measures profit from core business operations.
- Raw field was weak in simulations.
- Better used as a ratio: `operating_income / assets`, `operating_income / enterprise_value`, or `operating_income / sales`.

`cashflow_op`

- Operating cash flow.
- Useful for cash generation and cash flow yield.
- `cashflow_op / enterprise_value` showed positive but weak Sharpe in the recorded simulation.

`enterprise_value`

- Valuation denominator.
- Useful in ratios such as `enterprise_value / ebitda`, `cashflow_op / enterprise_value`, or `operating_income / enterprise_value`.

`return_equity`

- Profitability/quality measure.
- Can complement value or cash flow signals.

`return_assets`

- Asset efficiency and profitability.

`debt`

- Balance sheet risk.
- Often used as `debt / assets`.

`current_ratio`

- Liquidity/financial health signal.

`sales_growth`

- Growth signal.
- More promising than raw size fields when used carefully.

`volume`, `adv20`

- Price Volume fields.
- `volume / adv20` captures unusual volume.
- Can increase turnover if weighted too heavily.

`returns`

- Daily returns.
- `-returns` is short-term mean reversion.
- Noisy and can increase turnover.

`top2000`

- Universe field, not a predictive signal.
- Do not use raw as an alpha.
- Do not use raw as the first argument of `trade_when()`.

## Field Selection Checklist

For every new field, record:

```text
Field name:
Dataset:
Type: Matrix / Vector / Group / Universe / Other
Coverage:
Date coverage:
Alpha count:
Description:
Economic intuition:
Useful denominators:
Possible transforms:
First tests:
Results:
```

## Search Keywords To Use

```text
income
profit
gross_profit
gross_margin
ebitda
ebit
roe
roa
cashflow
operating_cash_flow
free_cash_flow
cash
asset
debt
liability
current_ratio
revenue
sales
sales_growth
book
enterprise_value
market_cap
inventory
dividend
estimate
revision
eps
```


## EUR Field Families Found In The 2026-10 Bulk Sweeps

These families were exercised across 4,223 EUR simulations (`simulations/067`-`069`,
raw data in `simulations/sweeps/`). Region EUR, Delay 1, Truncation 0.08, Pasteurization ON,
NaN Handling ON. The "best" columns are the best (Sharpe, Fitness) any single-field
transform of that family reached; the two artifact families are called out explicitly.

| Family prefix | What it is | Blocks | Best Sharpe | Best Fitness | Verdict |
|---|---|---:|---:|---:|---|
| `anl69_*` | Slow analyst best-estimate levels (`sales_best_eeps_cur_yr`, `net_new_best_eeps_nxt_yr`, `nav_best_eeps_nxt_yr`, `roe_best_eeps_*`, `ltg_dif_*`, `expected_report_*`) | 96 | 1.97 | 1.58 | **Best cluster in EUR.** Use levels with `ts_scale(...,63)` / `ts_quantile(...,63)`, not `rank`. |
| `anl4_*` | Analyst detail/advanced estimates (`sadaf_netprofit_median`, `af_div_low`, `fs_detail_estimate_advanced_*`, `tbve_ft`, flags like `cff_flag`) | 48 | 1.81 | 1.28 | **Second-best analyst cluster**; same slow-level + `ts_quantile(...,63)` pattern works. |
| `anl10_*` | Analyst consensus/revision family (`*_consensus`, `*_pred_surps_*`, `*_smart_ests_*`, `*smun`, `*fy1/fy2`, `netinnovate/salinnovate` scores) | 802 | 1.67 | 1.09 | Saturates at Sharpe 1.2-1.4 with Fitness <= 1.02. Only `anl10_ebtfy2_consensus` (`normalize(ts_zscore(...,63))`) and `anl10_salfy1_consensus_559` were usable. Most numerous family, most crowded. |
| `anl15_*` | Broker/aggregate estimate fields (`bps_ind_cal_fy3_gro`, `ebt_s_cal_fy2_*`, `gr_18_m_1m_chg`, `dps_s_18_m_mean`) | 334 | 0.92 | 0.75 | Weak everywhere; no block above Sharpe 0.92. |
| `anl39_*` | Analyst-derived valuation (`spvba`, `atanbvps`) | 3 | 0.92 | 0.29 | Too few observations; not established. |
| `anl11_*` | ESG scores/ranks (`cit3regsubsecrnk`, `esgposcorreg_industryperc`, `e1reg_industryrnk`, `2_region`) | 30 | 0.56 | 0.19 | Weak; ESG ranks are effectively static in this grid. |
| `anl9_*` | Recommendation codes (`recommendationbrokeroptioncode`) | 1 | −0.60 | −0.27 | Not usable as a raw rank. |
| `pv37_*` | Price/volume snapshots, intraday volumes (`snapshot1_volume*`, `volume_*`, `vwap_*`, `snapshot1_price*`, `pricesnap1600_*`, `cap_*`) | 530 | 2.51 (legit) | 1.16 | **Highest raw Sharpe in EUR** but structurally fragile: `LOW_SUB_UNIVERSE_SHARPE` at decay 5, `HIGH_TURNOVER` (100%+) at decay 0. Double-smoothing (`ts_decay_linear` then `ts_quantile`) is the only way to bring turnover to ~10%. |
| `pv37_low_14` | Anomalous pv37 field | 1 | 11.18 | 4.60 | **Artifact - discard.** Train Sharpe 0.00, turnover 100.00%, DD 0.00%, 12-long/218-short book. |
| `adjfactor` | Corporate-action price adjustment factor | 1 | 1.94 | 1.60 | **Artifact - not a cross-sectional signal.** Returns 31.20% on a 295/25 book; fails CONCENTRATED_WEIGHT + IS_LADDER_SHARPE. |
| `session_1600to1600_total_traded_volume` | Full-session traded volume aggregate | 1 | 2.41 | 1.16 | Most interesting non-`pv37` price/volume finding; best legitimate decay-5 Fitness. Needs sub-universe repair. |
| `pv20_*` | Derived price/volume and factor-style indicators (`*_indicator_*_feature*`, `*_best_eeps_*`, `returns*_t_*`, `netprofit/roe/bps/ebt/gps/sal/nav/net/pre_indicator_*`) | 688 | 1.52 | 1.09 | Mixed. Best member `pv20_eps_indicator_3_feature12_394` (Sharpe 1.32 / Fitness 1.09 / returns 12.99%) fails CONCENTRATED_WEIGHT. Long `feature<n>` numerics are noisy; treat as unexplored, not as a family. |
| `pv87_*` | NLP/news/estimate aggregates (`v2_expavg*_group_*`, `webv2_*`, `daily_ann_matrix_*`, `scores_certaintymuncertainty`, `target_price_consensus_mean`) | 198 | 1.29 | 0.78 | Weak but real; best is `pv87_ebitda_estimate_2_yr_annual_growth` under `group_zscore(ts_rank(...,252), sector)`. |
| `pv47_spret` | Spurious-return / stats-only return fields | 2 | −1.80 | −0.38 | **Do not use.** Strongly negative with damaged drawdown. |
| `fnd28_*` | Fundamental value/quantile fields (`value_*`, `newq_value_*`, `ndda1_value_*`, `wcishtq_value_*`) | 162 | 1.60 | 0.96 | Best found: `group_zscore(ts_rank(ts_backfill(fnd28_value_08698q, 21), 252), sector)` - Sharpe 1.60 / Fitness 0.93 / 3.32% turnover / 25.31 bps. Best low-turnover fundamental pocket. |
| `fnd17_*` | TTM and derived fundamental ratios (`ttmepsincx`, `qtotse`, `vol3mavg`, `8_ttmgrosmgn`, `ngmtpmtt`, `aptmgnpct`, `beta_up`) | 51 | 2.06 | 1.00 | `fnd17_vol3mavg` (volatility average) is the standout; `ttmepsincx` also reached Fitness 1.00. |
| `fnd23_*` | Interim/fundamental matrices (`intfvm_*`, `cf_m_ecns`, `annfv1a_*`, `blsm_derq`) | 82 | 1.25 | 0.61 | Marginal. |
| `fnd6_*` | Legacy fundamental fields (`newq_req`, `gpsa`, `cptnewq_ceqq`, `oidbps`-style) | 36 | 1.00 | 0.58 | Weak in EUR. |
| `est_*` | Estimate/consensus aggregates (`12m_dps_median`, `q_ner_median`, `12m_ner_*`, `12m_prr_*`, `12m_cps_std_28d`, `12m_sal_low_*`) | 107 | 1.54 | 0.92 | Best: `group_scale(ts_quantile(ts_backfill(est_12m_dps_median, 21), 63), sector)` - Sharpe 1.54 / Fitness 0.92. |
| `adv*` | Liquidity averages (`adv20_extra_usd`, `adv60`, `adv60_usd`, `adv20_usd_capped_100m`) | 19 | 1.58 | 0.90 | `group_rank(ts_quantile(ts_backfill(adv20_extra_usd, 21), 252), industry)` is the useful form. |
| `snt21*` | Sentiment fields (`*_conf_low`, `*_neg_max`, `*_neut_median`, `*dts_gen`) | 117 | 1.09 | 0.31 | Weak in EUR, consistent with the earlier USA sentiment lesson. |
| `sector_*`, `group_*`, `ebg_*` | Grouping/metadata fields (`*_currency_code*`, `government_bond_yield`, `*_marketcap_percent`, `bookvalue_currency_code`) | 47+ | 1.05 | 0.89 | Mostly `LOW_TURNOVER` (sub-1% turnover) - these are static metadata, not signals. `ebg_sector_government_bond_yield` never exceeds Sharpe 1.05. |
| `principal_component_*` | PCA/grouping scores (`grouping_method1_*clusters_top*`, `score_*_all`) | 29 | 0.25 | 0.08 | Dead in this grid. |
| `*_marketcap_percent` | Market-cap percentile bins (`group_fy2/fy3_*`, `sector_12mo/18mo_*`) | ~20 | 0.38 | 0.16 | Neutralization sinks, as expected for size proxies. |

### Field-level rules for EUR

- **Slow analyst level fields should be scaled, not ranked.** `ts_scale(x, 63)`,
  `ts_quantile(x, 63)` and `group_scale(ts_quantile(x, 252), sector)` beat
  `rank(ts_backfill(x, 21))` consistently on the `anl69` / `anl4` families.
- **`ts_backfill(field, 21)` alone is not a strategy.** It establishes coverage; the
  transform and the window decide the result.
- **Never use `adjfactor`, `pv37_low_14`, `pv47_*_spret`, or `*_currency_code` /
  `expected_report_*` variance fields as alpha inputs.** They produce artifacts or
  sub-1% turnover.
- **Watch for alias fields** (`anl69_nav_best_eeps_nxt_yr` and
  `anl69_ndebt_best_eeps_nxt_yr` returned identical metrics). Confirm a candidate field is
  genuinely distinct before treating two results as independent.  - **`anl10_*` is the crowded family in EUR.** Prefer `anl69_*`, `anl4_*`, `fnd28_*` and the
  `pv37` low-turnover corner for new work.

## USA Field Families Found In The 2026-10 USA Sweeps (Simulation 070)

> **Correction (2026-10-09).** The numbers in this section were first computed from a parse
> that had read the dump's `Train Sharpe` line into the `Sharpe` column, so every "Sharpe"
> below was the training value. The table is regenerated from the corrected parse: `Sharpe`
> is now the out-of-sample column, which is lower for almost every family. Grouping is by the
> first `ts_backfill(<field>, 21)` argument and is reproducible with
> `python3 Tools/brain_sweep_parser.py simulations/sweeps/sources/20261008_071542.txt`.

Simulation 070 page 1: Region USA, Neutralization INDUSTRY, Delay 1, Decay 5, Truncation
0.08, Pasteurization ON, NaN Handling ON — 2,500 blocks over **six universes** (TOP3000 2,194,
TOPSP500 81, TOP200 71, TOP2000 52, TOP500 52, TOP1000 50), 2,444 distinct fields, 0 passed
all checks. All 12 blocks above out-of-sample Sharpe 1.25 sit in TOP3000. Page 2 (1,050
blocks, USA/TOP3000, `anl15_*` 796 + `anl10_*` 237) is a negative control: best out-of-sample
Sharpe 1.23, 0 blocks above 1.25, 6 still PENDING.

| Family prefix | What it is | Blocks | Best out-of-sample Sharpe | Best Fitness | Verdict |
|---|---|---:|---:|---:|---|
| `anl15_*` | Broker/aggregate estimate fields (`dpsgics_*`, `bpsgics_*`, `ebtgics_*`, `salgics_*`, `*_cal_fy*`, `*_18_m_*`) | 1,226 | 1.23 | 0.97 | **Largest family and still weak.** Best block `anl15_dpsgics_ind_cal_fy3_mean` (group_rank, subindustry) reaches 1.23 / 0.97 at 5.56% turnover, i.e. just below both bars. Most of the family is a short-estimate-change tail; do not start new work here unless the field is a confirmed slow-estimate level. |
| `other` (no listed prefix: estimate-growth, skewness, cashflow, volatility-adjusted, `netprofit_actual_*`, `interest_expense_*`) | Single-name estimate/return-growth/skewness signals | 490 | 1.54 | 1.03 | **The only surface in the whole USA session that produced a Fitness ≥ 1.0 block.** `annual_financing_cashflow_amount` (1.40 / 1.03 at 2.00% turnover) and the two F8 leaders `netprofit_actual_q1_qoq_growth` (1.54 / 0.94) and `estimate_year2_change_3mo_gross_margin` (1.52 / 0.98) all live here. Low turnover, robustness-starved. |
| `anl10_*` | Analyst consensus / revision / smartest estimates (`*_consensus`, `*pred_surps*`, `*_smart_ests_*`, `netinnovate`/`salinnovate` scores) | 318 | 1.21 | 0.96 | **Most crowded family; saturates just under the bar.** Best `anl10_analyst_innovation_sal_normal_increase_fy2` 1.21 / 0.96 at 14.8% turnover. 318 distinct forms and none above 1.25 — treat as exhausted for single-field transforms. |
| `anl4_*` | Analyst guidance / advanced estimate families (`fs_guidances_advanced_qf_nd_*`, `fs_detail_estimates_basic_*`) | 173 | 1.14 | 0.87 | High variance: `anl4_fs_guidances_advanced_qf_nd_capex_minguidance` reaches 1.14 / 0.87 at 46.89% turnover. Earlier variants looked strong on the training column only. Not ready. |
| `est_*` | Estimate aggregates (`est_q_bps_lowerednum_4wks`, `est_q_tbv_low`, `est_q_ebi_raisednum_1mth`) | 57 | 1.17 | 0.75 | Mid-range; `est_q_tbv_low` is the low-turnover corner (0.70% turnover) but low turnover costs it Sharpe. |
| `fnd28_*` | Fundamental value/quantile fields (`value_*`, `annualprof_value_*`) | 57 | 1.00 | 0.58 | Weak in this grid; the comfortable EUR `fnd28` results did not transfer to USA ranks. |
| `anl69_*` | Slow analyst estimate/report fields (`eps_best_crncy_iso`, `eps_expected_report_time`, `dps_new_best_eeps_cur_yr`) | 48 | 1.09 | 0.88 | **Not the EUR `anl69` cluster.** The USA forms tested are report-time and best-estimate variants that top out at 1.09. Confirm a field is a slow estimate level before reusing the name across regions. |
| `pv20_*` | Derived price/volume and factor-style indicators (`pre_indicator_*_feature*`) | 45 | 1.22 | 0.77 | `pv20_pre_indicator_6_feature6` 1.22 / 0.77 at 3.43% turnover is the best of the family; the EUR `pv20_eps_indicator_3_feature12_394` did not surface. Unexplored, not established. |
| `fnd23_*` | Interim fundamental matrices (`blsm_cipq`, `annfv1a_*`, `net_income`, `roe`) | 41 | 0.91 | 0.90 | Best Fitness-to-Sharpe shape in the fundamental group but both numbers are below the bars. |
| `snt21` | Sentiment confidence/neutral/negative fields | 12 | 0.98 | 0.36 | Confirms the earlier USA sentiment lesson: Sharpe near 1.0 with Fitness 0.36 and 22.9% turnover. Discard as a primary source. |
| `fnd17_*` | TTM fundamental ratios (`sphsca`, `pr2tanbk`, `vol3mavg`) | 11 | 0.97 | 0.54 | Weak here; the good EUR `fnd17_vol3mavg` behaviour did not port. |
| `anl11_*` | ESG / coverage / industry-rank fields | 11 | 0.95 | 0.60 | Weak, same as EUR: ESG ranks are effectively static. |
| `adv` (liquidity) | ADV-style liquidity fields (`adv20_usd_capped_100m`) | 5 | 0.64 | 0.34 | Weak. |
| `sector_*` (grouping) | Sector grouping fields (`sector_grouping_level5_*`) | 5 | 0.67 | 0.48 | Grouping fields as signals; weak, as expected. |

Artifact fields in this session, with corrected values:

```text
group_rank(ts_backfill(net_9_feature3_predictor, 21), market)           1.35 / 0.84, 4.74% turnover
group_zscore(ts_backfill(option_return_bucket2_label_2, 21), industry)  1.20 / 0.34, 61.72% turnover
group_rank(ts_backfill(option_return_bucket3_prob1, 21), market)        0.24 / 0.07
group_rank(ts_sum(ts_backfill(adjfactor, 21), 126), subindustry)        0.32 / 0.11
```

Only `net_9_feature3_predictor` shows any strength; the other three are simply weak in this
region. The strong `adjfactor` rows were in the EUR page of Simulation 071, not here.

Field-level rules for this USA session:

- **The best surface is estimate-growth / skewness / cashflow, all in the `other` bucket**, not
  in any `anl*` family: `annual_financing_cashflow_amount` (1.40 / 1.03), `netprofit_actual_q1_qoq_growth`
  (1.54 / 0.94) and `estimate_year2_change_3mo_gross_margin` (1.52 / 0.98), all at 2–4% turnover.
  The repair target is robustness (`LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE`), not strength.
- **The crowded families are weak where it matters.** `anl10_*` (318 blocks) and `anl15_*`
  (1,226 blocks) top out at Sharpe 1.21 and 1.23 respectively — high counts, both under the
  bar, both with Fitness just under 1.0.
- **Universe matters more than field here.** Every block above Sharpe 1.25 in page 1 is
  TOP3000; TOP200/500/1000/2000/TOPSP500 produced none on this field list.
- **Discard `net_9_*`, `option_return_bucket*` and `adjfactor` as alpha inputs** in every
  region. `adjfactor` in particular re-appeared as the second-best EUR block in Simulation
  071 purely because it is an accounting device.
- **Never record a sweep without separating `Train Sharpe` from `Sharpe`.** The two disagree
  in 2,448 of these 2,500 blocks, and the training column is systematically higher.

## Field Families In The 2026-10 Multi-Region Bundle (Simulation 071)

Five regions in one export. Only the two surfaces with something usable are listed; the full
per-page data is in `simulations/sweeps/20261009_115500_d1..d6_*`.

### KOR / TOP600 — `oth176_lmt_close_eq_score`

- `normalize(ts_backfill(oth176_lmt_close_eq_score, 21))` — Sharpe 2.36 / Fitness 1.67 /
  Turnover 32.62% / Returns 16.28% / Drawdown 13.39% / Margin 9.98 bps / 264L-252S, **fails only
  `LOW_2Y_SHARPE`**. It is the best Sharpe+Fitness pair in the bundle and the first KOR-scope
  candidate in this workspace, and it is ATOM-shaped (one field, one operator).
- `zscore(ts_backfill(analyst_revisions_revenue_score, 21))` — 1.26 / 1.03 at 5.38% turnover,
  fails `LOW_SHARPE` + `CONCENTRATED_WEIGHT`.
- `LOW_2Y_SHARPE` fails in 761 of 789 KOR blocks (96.5%): the 2-year window, not strength, is
  what stops this region.
- The KOR page is dominated by fields with no listed prefix (686 of 789 blocks), so family
  grouping is not informative here; go by field.

### USA / TOP3000 — implied volatility vs realised volatility

The strongest USA surface recorded so far, and a new mechanism rather than another
fundamental-value variation:

- `iv_signal = zscore(implied_volatility_call_120 - implied_volatility_put_120) + rank(implied_volatility_call_120 / historical_volatility_120); cap_group = bucket(rank(cap), range="0.1,1,0.1"); group_neutralize(iv_signal, cap_group)`
  — Sharpe 2.61 / Fitness 1.88 / Turnover 35.73% / Returns 18.61% / Drawdown 7.62%, Decay 6,
  SUBINDUSTRY. Fails `CONCENTRATED_WEIGHT` + `LOW_SUB_UNIVERSE_SHARPE`.
- Conditioning buckets also work with `ts_rank(operating_income / cap, 250)` (2.34 / 1.47) and
  `ts_sum(vec_avg(nws12_afterhsz_sl), 60)` (2.29 / 1.47), so the result is not bucket-specific.
- All variants fail the same two checks at decay 4, 6 and 8: **decay does not clear weight
  concentration**. The repair is book construction.
- Fields: `implied_volatility_call_120`, `implied_volatility_put_120`, `historical_volatility_120`.

### The two surfaces that produced nothing

- **EUR** (1,141 blocks, five universes): best is `ts_zscore(ts_backfill(pv20_netdebt_best_eeps_nxt_yr_434, 21), 5)`
  at 2.63 / 1.24 but 69.46% turnover, failing sub-universe and 2-year. The second and third best
  are `adjfactor` (artifact). EUR repeats the existing lesson rather than adding to it.
- **ALL / LARGE (GLB)**, 192 blocks: best Sharpe 1.42, best Fitness 0.57. It does introduce the
  global check vocabulary — `LOW_GLB_APAC_SHARPE`, `LOW_ASI_JPN_SHARPE`, `LOW_GLB_AMER_SHARPE`,
  `LOW_GLB_EMEA_SHARPE`, `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`, `LOW_ROBUST_UNIVERSE_RETURNS`
  — so the global scope is judged on Asia/Japan and on robustness separately from the headline
  Sharpe. Not worth more sweeps until something clears Fitness 1.0.
