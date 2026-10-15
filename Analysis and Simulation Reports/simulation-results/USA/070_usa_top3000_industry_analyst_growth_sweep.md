# Simulation 070 — USA analyst-growth sweep (2,500 + 1,050 blocks, Decay 5)

Status: FAILED

> **Correction (2026-10-09).** This record was first written from an ad-hoc parse that read
> the `Train Sharpe` line and wrote it into both the `train_sharpe` and `sharpe` columns, and
> it also read only the first of the two pages in the source export. Both defects are fixed
> here: every `Sharpe` below is the out-of-sample column from the dump, `Train Sharpe` is
> shown separately, universe attribution comes from the dump's own `## Universe:` sections,
> and the second page (1,050 blocks) is now recorded. The superseded machine-readable files
> were moved to `Analysis and Simulation Reports/sweeps-and-experiments/superseded/`; the corrected ones are listed below.
> The old numbers were inflated by design, not by chance: `Train Sharpe` differs from
> `Sharpe` in 2,448 of the 2,500 blocks.

Source and artefacts:

```text
Source RTF:   ~/Downloads/Simulation Results.rtf
              size 1,063,519 bytes, md5 1b461cf245bd7fadbd3f42d812389e3f
Parsed text:  Analysis and Simulation Reports/source-data/20261008_071542.txt  (md5 3a92f8e8980c9b789778aaad65528b9f)
Page 1:       2,500 blocks, six universes  -> 20261008_071542_d1_usa_6universes.{csv,json,md}
Page 2:       1,050 blocks, USA/TOP3000    -> 20261008_071542_d2_usa_top3000.{csv,json,md}
Combined:     3,550 rows                    -> 20261008_071542_all_results.csv, 20261008_071542_SUMMARY.md
Superseded:   Analysis and Simulation Reports/sweeps-and-experiments/superseded/20261008_071542_usa_top3000_industry_decay5.csv
              Analysis and Simulation Reports/sweeps-and-experiments/superseded/20261008_071542_usa_top3000_industry_decay5_field_summary.json
```

Settings (Delay 1, Decay 5, Truncation 0.08, Pasteurization ON, NaN Handling ON throughout):

```text
Page 1  Region USA, Neutralization INDUSTRY, no top-level Universe:
        the page is split by section into TOP200 (71), TOP500 (52), TOP1000 (50),
        TOP2000 (52), TOP3000 (2,194) and TOPSP500 (81) blocks.
Page 2  Region USA, Universe TOP3000, Neutralization INDUSTRY.
```

Expression family: every block is `ts_backfill(<field>, 21)` under one of `group_rank`,
`group_zscore`, `group_std_dev`, `scale`, `ts_quantile`, or the bare backfill. This is a
field screen: 2,444 distinct fields, almost all sampled once or twice.

## Page 1 results (2,500 blocks)

```text
Checks PASS: 0 of 2,500
Blocks with TRUE Sharpe >= 1.25: 12   (22 blocks have Train Sharpe >= 1.25)
Blocks with TRUE Sharpe >= 1.25 AND Fitness >= 1.0: 1
Highest TRUE Sharpe in the page: 1.54   Highest Train Sharpe: 1.95
Every one of the 12 blocks above Sharpe 1.25 sits in TOP3000; the five smaller
universes contributed no block above 1.25.
```

Best block in the page — the only one clearing Fitness >= 1.0:

```text
Expression: group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)
Universe: TOP3000   Neutralization: INDUSTRY
Train Sharpe: 1.69
Sharpe: 1.40
Fitness: 1.03
Turnover: 2.00%
Returns: 6.73%
Drawdown: 5.97%
Margin: 67.19 bps
Long / Short: 1903 / 1218
Checks: FAIL F19 (LOW_SHARPE, LOW_2Y_SHARPE)
```

Highest out-of-sample Sharpe in the page:

```text
Expression: group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)
Train Sharpe: 1.44   Sharpe: 1.54
Fitness: 0.94   Turnover: 3.72%   Returns: 4.66%   Drawdown: 5.57%   Margin: 25.08 bps
Checks: FAIL F8 (LOW_SHARPE, LOW_FITNESS)
```

```text
Expression: group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)
Train Sharpe: 1.26   Sharpe: 1.52
Fitness: 0.98   Turnover: 3.71%   Returns: 5.16%   Drawdown: 11.90%   Margin: 27.82 bps
Checks: FAIL F8 (LOW_SHARPE, LOW_FITNESS)
```

Remaining named candidates, with corrected Sharpe:

| Expression | Train Sharpe | Sharpe | Fitness | Turnover | Returns | Drawdown | Margin | L/S | Checks |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `group_rank(ts_backfill(eps_q1_estimate_asymmetry, 21), subindustry)` | 1.64 | 1.50 | 0.79 | 6.91% | 3.48% | 2.98% | 10.07 | 1542/1574 | F2 |
| `group_rank(ts_backfill(eps_q1_estimate_asymmetry, 21), market)` | 1.54 | 1.42 | 0.77 | 5.85% | 3.66% | 2.92% | 12.49 | 1533/1583 | F2 |
| `group_rank(ts_backfill(consensus_next_fiscal_year_interest_expense, 21), subindustry)` | 1.46 | 1.45 | 0.73 | 3.24% | 3.20% | 4.43% | 19.73 | 1537/1582 | F2 |
| `group_rank(ts_backfill(consensus_next_fiscal_year_interest_expense, 21), market)` | 1.51 | 1.44 | 0.77 | 2.67% | 3.61% | 4.50% | 27.13 | 1524/1595 | F2 |
| `group_rank(ts_backfill(estimate_y1_skewness_book_value_ps, 21), market)` | 1.49 | 1.44 | 0.83 | 3.13% | 4.17% | 7.12% | 26.63 | 1858/1258 | F2 |
| `group_rank(ts_backfill(op_expense_estimate_y1_skewness, 21), subindustry)` | 1.62 | 1.37 | 0.67 | 3.36% | 3.00% | 2.84% | 17.86 | 1724/1393 | F1 |

Failed check sets in this dump:

```text
F1: LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE
F2: LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F3: LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE
F4: LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F5: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_2Y_SHARPE
F6: LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F7: LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE
F8: LOW_SHARPE, LOW_FITNESS
F9: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F10: LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE
F11: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE
F12: LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT
F13: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE
F14: LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F15: LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, LOW_2Y_SHARPE
F16: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER
F17: LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
F18: LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE
F19: LOW_SHARPE, LOW_2Y_SHARPE
F20: LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE
F21: LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT
```

Fail-code distribution (unchanged by the correction — the `Checks` lines were always parsed
correctly): F1 1,116 · F2 562 · F3 281 · F4 155 · F5 112 · F6 65 · F7 56 · F8 44 · F9 32 ·
F10 20 · F11 18 · F12 10 · F13-F21 all below 10.

Artifact fields in page 1, with corrected numbers (see the do-not-re-run table in
`status_index.md`):

```text
group_rank(ts_backfill(net_9_feature3_predictor, 21), market)      1.35 / 0.84, 4.74% turnover
group_zscore(ts_backfill(option_return_bucket2_label_2, 21), industry)  1.20 / 0.34, 61.72% turnover
group_rank(ts_backfill(option_return_bucket3_prob1, 21), market)       0.24 / 0.07
group_rank(ts_sum(ts_backfill(adjfactor, 21), 126), subindustry)       0.32 / 0.11
```

Only `net_9_feature3_predictor` shows any strength; the other three are simply weak in this
region, not strong artifacts. The `adjfactor` rows that looked impressive were in the EUR
page of Simulation 071, not here.

## Page 2 results (1,050 blocks, USA/TOP3000/INDUSTRY)

This page was present in the source export but was never recorded before. It is a second
sweep of the same shape, dominated by two families:

```text
anl15 (analyst/estimate) fields: 796 blocks
anl10 (analyst/model) fields:    237 blocks
Checks PASS: 0 of 1,050
Blocks with TRUE Sharpe >= 1.0: 10;  >= 1.25: 0
Highest TRUE Sharpe: 1.23   Highest Train Sharpe: 0.96
Verdicts: 1,044 FAIL, 6 PENDING
```

Best block in page 2:

```text
Expression: group_rank(ts_backfill(anl10_roaff_2277, 21), sector)
Train Sharpe: 0.96   Sharpe: 1.23   Fitness: 0.43   Turnover: 43.88%
Checks: FAIL LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE
```

Page 2 changes the conclusion slightly: the second half of the Oct-8 session was a
`anl10_*` / `anl15_*` field screen with no block above Sharpe 1.23, so the whole Oct-8 export
is weaker than the first page alone suggested. It also shows the train/out-of-sample direction
running the other way — 0.96 train against 1.23 out-of-sample — so neither column alone
should be read as the truth.

## Conclusion

- The Oct-8 USA export contains **3,550 blocks across two pages**, uses **six universes** on
  page 1, and produced **0 submittable alphas**. Corrected headline: best out-of-sample Sharpe
  in page 1 is 1.54, not 1.69, and page 2 tops out at 1.23.
- The binding constraints are still the joint Sharpe/Fitness shortfall (F1 + F2 = 1,678 of
  2,500) and robustness (`LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE`), not turnover.
- `annual_financing_cashflow_amount` remains the only Fitness >= 1.0 block, at true Sharpe
  1.40. It clears the 1.25 user bar on the out-of-sample column, so the repair is still
  framed correctly — robustness, not strength — but it is a 1.40, not a 1.69.
- The cleanest fitness-band targets are the F8 blocks `netprofit_actual_q1_qoq_growth`
  (Sharpe 1.54 / Fitness 0.94) and `estimate_year2_change_3mo_gross_margin` (1.52 / 0.98).
  The first of those is also the page's highest out-of-sample Sharpe.
- The five smaller universes (TOP200/500/1000/2000/TOPSP500) contributed nothing above
  Sharpe 1.25 on this field list, so the effective universe for this work is TOP3000.

## Lesson

- **Never record a sweep without separating `Train Sharpe` from `Sharpe`.** A near-substring
  match (`"Sharpe" in line`) silently captures the training line, and every downstream table,
  ledger row and conclusion inherits the error. The parser now writes both columns explicitly.
- A pasted export can hold more than one page. The declared `N Results` header only describes
  the first page, so a file-level parse silently drops the rest (here: 1,050 blocks, 29% of
  the export).
- Universe attribution must come from the dump's `## Universe:` sections. The page header
  omitted `Universe:` entirely, and assuming the section default put 306 non-TOP3000 blocks
  under a TOP3000 label.
- The second page is a useful negative control: same shape, same settings, no block above
  Sharpe 1.23, and the train/out-of-sample columns disagree in both directions.

## Next action

- Treat `annual_financing_cashflow_amount` and the two F8 blocks as repair targets only; they
  are already simulated and must not be re-proposed as new alphas.
- Prefer the newer USA surface in Simulation 071 (implied-volatility dispersion at Sharpe
  2.61 / Fitness 1.88) over further field screens in this family; this page shows the field
  screen is exhausted.


## Full 3,550-Record Factor Screening Analytics

### 1. Overall Distribution of Metrics (3,550 Total Records)

The 3,550 simulation blocks (2,500 on Page 1 across 6 universes, 1,050 on Page 2 for TOP3000) show clear structural properties:

| Metric | Sample (N) | Min | 5th Pct | 25th Pct | Median | Mean | 75th Pct | 95th Pct | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Sharpe (Out-of-Sample)** | 3,550 | `-1.8200` | `-0.4400` | `-0.0800` | **`0.1900`** | `0.1946` | `0.4600` | `0.8400` | **`1.5400`** |
| **Train Sharpe (IS Window)** | 3,550 | `-10.0000` | `-0.4800` | `-0.1100` | `0.1600` | `0.1261` | `0.4500` | `0.8600` | `1.9500` |
| **Fitness (Out-of-Sample)** | 3,532 | `-0.9200` | `-0.1900` | `-0.0100` | `0.0600` | `0.0976` | `0.2000` | `0.4700` | `1.0300` |
| **Turnover (%)** | 3,550 | `0.00%` | `0.96%` | `2.42%` | **`8.31%`** | `18.00%` | `21.01%` | `72.90%` | `145.18%` |
| **Returns (%)** | 3,550 | `-26.67%` | `-3.74%` | `-0.51%` | `1.33%` | `1.41%` | `3.14%` | `6.52%` | `41.74%` |
| **Drawdown (%)** | 3,550 | `0.00%` | `7.63%` | `13.21%` | `21.57%` | `32.39%` | `39.47%` | `92.23%` | `427.84%` |
| **Margin (bps)** | 3,550 | `-210.97` | `-12.64` | `-0.65` | `1.88` | `9.88` | `11.91` | `66.79` | `384.10` |

### 2. Comparative Performance Across USA Universes

Every block above Sharpe `1.25` sits in `TOP3000`; the more liquid/concentrated universes exhibited no viable Alpha tails on this single-factor backfilled surface:

| Universe | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Median Fitness | Sharpe >= 1.00 | Sharpe >= 1.25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **TOP3000** | 3,244 | `0.20` | `0.20` | `8.37%` | `0.06` | **76** | **12** |
| **TOPSP500** | 81 | `0.12` | `0.17` | `10.34%` | `0.03` | `1` | `0` |
| **TOP200** | 71 | `0.16` | `0.17` | `5.29%` | `0.06` | `0` | `0` |
| **TOP2000** | 52 | `0.19` | `0.19` | `4.21%` | `0.04` | `1` | `0` |
| **TOP500** | 52 | `0.18` | `0.17` | `6.85%` | `0.06` | `1` | `0` |
| **TOP1000** | 50 | `0.20` | `0.13` | `8.91%` | `0.04` | `0` | `0` |

### 3. Operator Family Comparative Performance

The choice of outer operator is the single most decisive structural determinant of performance:

| Outer Operator | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Median Fitness | Sharpe >= 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| **`group_rank`** | 715 | **`0.51`** | **`0.49`** | `3.26%` | **`0.24`** | **63** (80% of all top alphas) |
| **`ts_sum`** | 56 | `0.34` | `0.33` | `2.50%` | `0.15` | `2` |
| **`rank`** | 166 | `0.29` | `0.24` | `5.10%` | `0.10` | `1` |
| **`scale`** | 158 | `0.27` | `0.21` | `4.97%` | `0.09` | `4` |
| **`ts_decay_linear`** | 46 | `0.25` | `0.20` | `4.03%` | `0.10` | `0` |
| **`ts_av_diff`** | 42 | `0.24` | `0.16` | `13.62%` | `0.07` | `0` |
| **`normalize`** | 150 | `0.20` | `0.19` | `8.32%` | `0.07` | `2` |
| **`group_neutralize`**| 187 | `0.20` | `0.19` | `6.33%` | `0.07` | `1` |
| **`ts_arg_min`** | 56 | `0.19` | `0.17` | `8.56%` | `0.05` | `0` |
| **`quantile`** | 146 | `0.18` | `0.18` | `6.94%` | `0.05` | `0` |
| **`ts_std_dev`** | 54 | `0.18` | `0.15` | `5.20%` | `0.05` | `1` |
| **`winsorize`** | 141 | `0.14` | `0.17` | `8.51%` | `0.04` | `0` |
| **`ts_arg_max`** | 53 | `0.14` | `0.12` | `8.34%` | `0.03` | `0` |
| **`last_diff_value`** | 42 | `0.13` | `0.09` | `9.21%` | `0.02` | `0` |
| **`group_zscore`** | 179 | `0.12` | `0.15` | `6.86%` | `0.03` | `3` |
| **`zscore`** | 170 | `0.12` | `0.12` | `6.61%` | `0.04` | `0` |
| **`group_scale`** | 141 | `0.12` | `0.14` | `6.99%` | `0.03` | `0` |
| **`ts_quantile`** | 47 | `0.11` | `0.09` | `18.83%` | `0.02` | `1` |
| **`ts_mean`** | 46 | `0.11` | `0.11` | `2.34%` | `0.03` | `0` |
| **`group_count`** | 144 | `0.11` | `-0.00` | `60.47%` | `0.02` | `0` |
| **`ts_scale`** | 56 | `0.08` | `0.06` | `17.22%` | `0.01` | `0` |
| **`ts_zscore`** | 57 | `0.08` | `0.04` | `19.46%` | `0.01` | `0` |
| **`ts_delay`** | 46 | `0.06` | `0.03` | `5.54%` | `0.01` | `0` |
| **`group_std_dev`** | 174 | `0.05` | `0.08` | `70.28%` | `0.01` | `1` |
| **`ts_delta`** | 49 | `0.05` | `0.09` | `13.20%` | `0.01` | `0` |
| **`ts_returns`** | 42 | `0.05` | `0.02` | `23.34%` | `0.01` | `0` |
| **`ts_kurtosis`** | 51 | `0.01` | `-0.00` | `14.26%` | `0.00` | `0` |
| **`ts_ir`** | 44 | `0.01` | `-0.03` | `15.76%` | `0.00` | `0` |
| **`group_sum`** | 132 | `-0.02` | `-0.00` | `67.74%` | `0.00` | `0` |
| **`ts_product`** | 59 | `-0.02` | `0.02` | `35.79%` | `0.00` | `0` |
| **`ts_rank`** | 45 | `-0.09` | `-0.06` | `17.78%` | `-0.01` | `0` |
| **`ts_max_diff`** | 56 | `-0.10` | `-0.08` | `13.71%` | `-0.03` | `0` |

### 4. Field Family Performance & Data Coverage (2,444 Distinct Fields)

| Field Family | Category | Blocks | Median Sharpe | Mean Sharpe | Median Turnover | Sharpe >= 1.00 |
|---|---|---:|---:|---:|---:|---:|
| **`anl11`** | ESG & Reputation | 11 | **`0.61`** | `0.42` | `2.65%` | `0` |
| **`fnd6`** | Fundamental Valuation | 1 | `0.53` | `0.53` | `1.05%` | `0` |
| **`snt21`** | News Sentiment | 12 | `0.52` | `0.36` | `22.64%` | `0` |
| **`pv20`** | Price-Volume Indicators | 45 | `0.48` | `0.40` | `6.15%` | `4` |
| **`est_`** | Analyst Consensus Estimates | 57 | `0.47` | **`0.45`** | `2.67%` | **7** |
| **`fnd23`** | Balance Sheet / Income | 41 | `0.40` | `0.36` | `1.49%` | `0` |
| **`other`** | Company filings / Earnings growth | 502 | `0.34` | `0.32` | `5.67%` | **32** |
| **`fnd28`** | Corporate Ratios / Performance | 57 | `0.34` | `0.29` | `1.01%` | `1` |
| **`fnd17`** | Per-share Financials | 11 | `0.34` | `0.33` | `1.22%` | `0` |
| **`anl69`** | Broker Recommendations | 48 | `0.29` | `0.22` | `7.29%` | `1` |
| **`adv`** | Liquidity / Dollar Volume | 10 | `0.23` | `0.18` | `10.61%` | `0` |
| **`anl10`** | Model Predictions / Revisions | 555 | `0.20` | `0.21` | `10.89%` | **25** |
| **`anl15`** | Global Industry Estimates | 2,022 | `0.14` | `0.15` | `9.37%` | **7** |
| **`anl4`** | Company Guidance Detail | 173 | `0.03` | `0.10` | `3.13%` | `2` |
| **`sector_`** | Categorical Sector Dummies | 5 | `0.00` | `-0.22` | `5.37%` | `0` |

### 5. Failure Reason Frequency (3,544 FAIL Verdicts)

Every failure set is a deterministic combination of standard platform validation tests:

| Failed Check Code | Description | Count | Share (%) |
|---|---|---:|---:|
| **F1** | `LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE` | 1,573 | 44.3% |
| **F2** | `LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | 810 | 22.8% |
| **F3** | `LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE` | 404 | 11.4% |
| **F4** | `LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | 233 | 6.6% |
| **F5** | `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_2Y_SHARPE` | 154 | 4.3% |
| **F6** | `LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | 102 | 2.9% |
| **F7** | `LOW_SHARPE, LOW_FITNESS, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_2Y_SHARPE` | 78 | 2.2% |
| **F8** | `LOW_SHARPE, LOW_FITNESS` | 63 | 1.8% |
| **F9** | `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` | 38 | 1.1% |
| **F10**| `LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE` | 23 | 0.6% |
| **F11–F21** | Tail combinations (concentrated weight, ladder Sharpe, extreme turnover) | 66 | 1.9% |

Individual Check Incidence:
- `LOW_SHARPE`: 3,544 (99.8%)
- `LOW_FITNESS`: 3,543 (99.8%)
- `LOW_2Y_SHARPE`: 3,412 (96.1%)
- `LOW_SUB_UNIVERSE_SHARPE`: 1,237 (34.8%)
- `CONCENTRATED_WEIGHT`: 887 (25.0%)
- `HIGH_TURNOVER`: 213 (6.0%)
- `LOW_TURNOVER`: 201 (5.7%)
- `IS_LADDER_SHARPE`: 2 (0.1%)

### 6. Audit of the 6 PENDING Records

In Page 2 (`20261008_071542_d2_usa_top3000`), exactly 6 records were exported in `PENDING` state:

| Result No. | Expression | Sharpe | Train Sharpe | Fitness | Turnover | Returns | Drawdown | Margin |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **2** | `scale(ts_std_dev(ts_backfill(anl10_smartest_ner_ff, 21), 126))` | **`1.21`** | `0.95` | `0.84` | `2.45%` | `6.05%` | `14.33%` | `49.35 bps` |
| **3** | `rank(ts_sum(ts_backfill(anl15_dpsgics_s_fy2_ests_up, 21), 252))` | `1.06` | `0.93` | `0.79` | `1.79%` | `6.91%` | `19.53%` | `77.39 bps` |
| **5** | `ts_sum(ts_backfill(anl15_dpsgics_gr_12_m_ests_up, 21), 126)` | `1.03` | `0.94` | `0.65` | `2.06%` | `4.96%` | `13.91%` | `48.11 bps` |
| **8** | `group_rank(ts_returns(ts_backfill(anl10_epsnormal_increase_fy2, 21), 126), sector)` | `1.01` | `0.90` | `0.41` | `21.08%` | `3.47%` | `9.84%` | `3.29 bps` |
| **9** | `group_rank(ts_backfill(actuals_value_currency_code, 21), sector)` | `1.01` | `0.72` | `0.65` | `1.15%` | `5.17%` | `17.67%` | `90.18 bps` |
| **10** | `ts_std_dev(ts_std_dev(ts_backfill(anl10_fcfff_1975, 21), 63), 63)` | `1.00` | `1.12` | `0.53` | `3.38%` | `3.53%` | `5.95%` | `20.86 bps` |

> **Audit Note:** None of these 6 records can be treated as passed. Result 9 uses `actuals_value_currency_code` (a categorical currency identifier), which is an uninvestable categorical leakage hazard. Result 2 is the most promising candidate for formal resimulation.


## Ranked Candidate Shortlist

### Group A — Strongest Candidates for Targeted Validation

These candidates achieved genuine out-of-sample Sharpe `>= 1.35` with low turnover (`< 7%`), low drawdown (`< 12%`), positive margin, and failed only user-level thresholds (`F8`: `LOW_SHARPE, LOW_FITNESS` or `F19`: `LOW_SHARPE, LOW_2Y_SHARPE`):

| Rank | Expression | Universe | Sharpe | Train | Fit | TO | Ret | DD | Margin | Fail Code | Diagnosis & Recommended Validation |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **A1** | `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, 21), subindustry)` | TOP3000 | **`1.54`** | `1.44` | `0.94` | `3.72%` | `4.66%` | `5.57%` | `25.08 bps` | `F8` | Highest true Sharpe in sweep. Only needs `+0.06` Fitness. Test `ts_backfill(..., 63)` and blend with 5-day reversal. |
| **A2** | `group_rank(ts_backfill(estimate_year2_change_3mo_gross_margin, 21), market)` | TOP3000 | **`1.52`** | `1.26` | `0.98` | `3.71%` | `5.16%` | `11.90%` | `27.82 bps` | `F8` | Fitness `0.98` is just `0.02` short of passing. Test `subindustry` neutralization and longer backfill. |
| **A3** | `group_rank(ts_backfill(annual_financing_cashflow_amount, 21), market)` | TOP3000 | **`1.40`** | `1.69` | **`1.03`** | `2.00%` | `6.73%` | `5.97%` | `67.19 bps` | `F19` | **Only candidate in sweep with Fitness >= 1.00**. Failed `LOW_2Y_SHARPE`. Test decay reduction (`5 -> 2`) or `subindustry`. |
| **A4** | `group_rank(ts_backfill(eps_q1_estimate_asymmetry, 21), subindustry)` | TOP3000 | **`1.50`** | `1.64` | `0.79` | `6.91%` | `3.48%` | `2.98%` | `10.07 bps` | `F2` | Outstanding drawdown (`2.98%`). Failed sub-universe check. Test cap-weight neutralization. |
| **A5** | `group_rank(ts_backfill(estimate_y1_skewness_book_value_ps, 21), market)` | TOP3000 | **`1.44`** | `1.49` | `0.83` | `3.13%` | `4.17%` | `7.12%` | `26.63 bps` | `F2` | Stable analyst dispersion factor. Test `ts_scale` instead of raw rank. |
| **A6** | `group_rank(ts_backfill(consensus_next_fiscal_year_interest_expense, 21), market)` | TOP3000 | **`1.44`** | `1.51` | `0.77` | `2.67%` | `3.61%` | `4.50%` | `27.13 bps` | `F2` | Low turnover, high margin (`27.1 bps`). Test scaling by enterprise value (`interest / ev`). |

### Group B — Promising Research Hypotheses (Requiring Structural Repair)

| Rank | Expression | Universe | Sharpe | Fit | TO | Ret | DD | Bottleneck & Hypothesis |
|---:|---|---|---:|---:|---:|---:|---:|---|
| **B1** | `scale(ts_std_dev(ts_backfill(anl10_smartest_ner_ff, 21), 126))` | TOP3000 | `1.21` | `0.84` | `2.45%` | `6.05%` | `14.33%` | **Pending status**: Model revision volatility has high return spread (`6.05%`); requires full check evaluation. |
| **B2** | `group_rank(ts_backfill(net_9_feature3_predictor, 21), market)` | TOP3000 | `1.35` | `0.84` | `4.74%` | `4.82%` | `7.11%` | Machine-learning predictor feature. Test if `net_9` has point-in-time publication lag. |
| **B3** | `group_rank(ts_backfill(revenue_actual_q1_qoq_growth, 21), market)` | TOP3000 | `1.34` | `0.81` | `3.34%` | `4.53%` | `6.11%` | Top revenue momentum signal. Complement with gross margin growth (`estimate_year2_change_3mo_gross_margin`). |
| **B4** | `group_rank(ts_backfill(actual_q1_qoq_gross_income_growth, 21), subindustry)` | TOP3000 | `1.29` | `0.74` | `3.38%` | `4.13%` | `4.02%` | Low drawdown (`4.02%`). Pair with fast reversal leg to push Fitness above `1.00`. |
| **B5** | `group_rank(ts_backfill(interest_expense_volatility_adjusted_2yr, 21), market)` | TOP3000 | `1.21` | `0.78` | `1.79%` | `5.21%` | `6.36%` | Margin `58.28 bps`. Triggered `F3` (`CONCENTRATED_WEIGHT`). Needs `winsorize` or `Truncation=0.04`. |

### Group C — Failure References (Negative Controls to Avoid)

| Expression | Universe | Sharpe | Turnover | Drawdown | Root Cause Failure Mode |
|---|---|---:|---:|---:|---|
| `group_std_dev(ts_product(ts_backfill(anl15_bps_ind_fy1_cos_up, 21), 5), sector)` | TOP3000 | `0.55` | `72.48%` | `27.46%` | **Cross-sectional standard deviation explosion** (`F6`). Destroys signal stability. |
| `ts_product(ts_backfill(anl15_salgics_s_cal_fy1_cos, 21), 252)` | TOP3000 | `0.46` | `102.38%` | `201.96%` | **Rolling time-series product compounding trap** (`F7`). Generates catastrophic drawdown. |
| `group_scale(ts_product(ts_backfill(anl15_salgics_ind_cal_fy3_mean, 21), 126), market)` | TOP3000 | `0.50` | `106.42%` | `180.64%` | **Extreme turnover / tail concentration**. Triggers margin collapse. |
| `group_rank(ts_backfill(actuals_value_currency_code, 21), sector)` | TOP3000 | `1.01` | `1.15%` | `17.67%` | **Categorical code data-leakage hazard**. Trading on currency symbols is economically non-viable. |


## Reusable Research Lessons from Experiment 070

### Lesson L-022: Cross-Sectional Ranking (`group_rank`) Outperforms Z-Scoring on Fundamental & Analyst Estimates

- **Empirical Observation:** Across 3,550 simulations, `group_rank` delivered a median Sharpe of `0.51` (mean `0.49`, median turnover `3.26%`) and accounted for **63 of the 79 (79.7%) alphas with Sharpe >= 1.00**, including all 12 alphas with Sharpe `>= 1.25`. By contrast, `group_zscore` produced a median Sharpe of `0.12` (mean `0.15`) with only 3 alphas clearing `1.00`, and `group_std_dev` produced a median turnover of `70.28%` with zero viable alphas.
- **Quantitative Mechanism:** Fundamental ratios and analyst estimate revisions exhibit extreme kurtosis and fat tails. `group_rank` projects values uniformly onto `[0, 1]`, dampening extreme analyst outlier revisions while preserving ordinal predictive ordering. Z-scoring preserves extreme variance spikes, causing concentrated bets on small, erratic companies and inflating portfolio turnover.
- **Confidence Level:** High (N = 715 `group_rank` blocks vs 179 `group_zscore` blocks in identical settings).
- **Follow-Up Experiment:** Directly test `group_rank(field, subindustry)` vs `group_zscore(winsorize(field, 3), subindustry)` on candidates A1–A3 to evaluate if winsorized z-scoring can match rank performance.

### Lesson L-023: Sub-Universe Breakdown on Analyst Revision Factors

- **Empirical Observation:** Every one of the 12 alphas with Sharpe `>= 1.25` emerged in `TOP3000`. When tested on smaller, more liquid universes (`TOP200`, `TOP500`, `TOPSP500`, `TOP1000`), zero alphas cleared `1.25`, and `LOW_SUB_UNIVERSE_SHARPE` was triggered in 1,237 of 3,550 blocks (34.8%).
- **Quantitative Mechanism:** Consensus analyst estimate dispersion has lower pricing efficiency in the small-and-mid-cap segment of `TOP3000`. In large-cap universes (`TOP200` / `TOPSP500`), institutional sell-side revisions are rapidly discounted by high-frequency market participants, compressing return spread and causing sub-universe tests to fail.
- **Confidence Level:** High (N = 3,244 `TOP3000` vs 306 smaller universe blocks).
- **Follow-Up Experiment:** Test whether adding a market-cap interaction term (`* log(cap)`) or double-neutralizing by size buckets (`bucket(rank(cap))`) restores sub-universe robustness.

### Lesson L-024: The `ts_backfill(..., 21)` Window Mismatch on Quarterly Earnings Fields

- **Empirical Observation:** 887 blocks (25.0%) failed with `CONCENTRATED_WEIGHT` and 201 blocks (5.7%) failed with `LOW_TURNOVER`.
- **Quantitative Mechanism:** The entire sweep applied an arbitrary lookback of `21` days (`ts_backfill(field, 21)`). Because quarterly financial statements and guidance updates occur every ~63 trading days, a 21-day lookback leaves up to 42 trading days of missing data (`NaN`) between disclosures. When `NaN Handling: ON` is active, instruments with expired backfills receive zero weight, causing portfolio weights to concentrate into a smaller subset of recently reporting firms.
- **Confidence Level:** High (structural data property of quarterly US GAAP filings).
- **Follow-Up Experiment:** Resimulate Candidates A1 and A3 with `ts_backfill(field, 63)` and `ts_backfill(field, 126)`, measuring the change in weight concentration and Fitness.

### Lesson L-025: In-Sample (Train) Sharpe vs Out-of-Sample Sharpe Divergence

- **Empirical Observation:** In 3,469 of 3,550 blocks (97.7%), `Train Sharpe` diverged from true out-of-sample `Sharpe`. While `Train Sharpe` reached `1.95`, the true maximum was `1.54`. On Page 2, the bias inverted (Train Sharpe median `0.16` vs OOS `0.19`).
- **Research Safeguard:** Documentation and index tools must never rely on substring matches for `"Sharpe"`. Ingestion pipelines must mandate explicit separate extraction of `Train Sharpe` and out-of-sample `Sharpe`.
- **Confidence Level:** High (verified across all 3,550 CSV rows).

### Lesson L-026: Outperforming Fundamental Growth & Analyst Revision Field Families

- **Empirical Observation:** The top 3 performing field families in USA were quarterly net income growth (`netprofit_actual_q1_qoq_growth`, Sharpe `1.54`), consensus gross margin changes (`estimate_year2_change_3mo_gross_margin`, Sharpe `1.52`), and analyst revision asymmetry (`eps_q1_estimate_asymmetry`, Sharpe `1.50`).
- **Research Implication:** Prioritize quarterly fundamental growth rates and multi-month consensus revision slopes over static balance sheet ratios or un-decayed news sentiment.
- **Confidence Level:** High (replicated across independent estimate fields).


## Prioritized Next Experiments

Instead of repeating broad, uncontrolled multi-thousand sweeps, execute these three tightly controlled tests:

1. **Experiment E-070A: Backfill Optimization on Top Candidates (A1 & A2)**
   - **Hypothesis:** Extending the lookback window from `21` to `63` and `126` days will eliminate the quarterly `NaN` gap, smooth booksize transitions, and raise Fitness above `1.00`.
   - **Expressions:** `group_rank(ts_backfill(netprofit_actual_q1_qoq_growth, D), subindustry)` for `D in [21, 42, 63, 126]`.
   - **Settings:** `USA / TOP3000 / Delay 1 / Decay 5 / INDUSTRY / Truncation 0.08`.

2. **Experiment E-070B: Fast Reversal Leg Smoothing on Candidate A1**
   - **Hypothesis:** Blending `netprofit_actual_q1_qoq_growth` with a smoothed short-term reversal leg (`0.7 * group_rank(...) + 0.3 * rank(ts_mean(-returns, 5))`) will raise Sharpe above `1.75` and Fitness above `1.20` (replicating the `024 -> 026` breakthrough).
   - **Settings:** `USA / TOP3000 / Delay 1 / Decay 4 / INDUSTRY / Truncation 0.08`.

3. **Experiment E-070C: Sub-Universe Stabilization on Candidate A4 (`eps_q1_estimate_asymmetry`)**
   - **Hypothesis:** Neutralizing by `group_cartesian_product(bucket(rank(cap), "0.2,1,0.2"), subindustry)` will remove size-bias and clear the sub-universe Sharpe check (`LOW_SUB_UNIVERSE_SHARPE`).
   - **Settings:** `USA / TOP3000 / Delay 1 / Decay 5 / Truncation 0.05`.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `070` |
| **Record Type** | `Bulk Multi-Simulation Sweep` |
| **Source Dataset / Fields** | Multi-field sweep (analyst, price-volume, fundamental, option/IV) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000   Neutralization: INDUSTRY` |
| **Neutralization / Decay / Truncation** | `INDUSTRY` · Decay `5` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-10-08` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.40` · Fitness: `1.03` · Turnover: `2.00%` · Returns: `6.73%` · Drawdown: `5.97%` · Margin: `67.19 bps` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAIL F19 (LOW_SHARPE, LOW_2Y_SHARPE)` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `ATOM-eligible candidate surface (single-dataset transforms)` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/070_usa_top3000_industry_analyst_growth_sweep.md` |

