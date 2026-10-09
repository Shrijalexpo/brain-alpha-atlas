# Simulation 070 — USA analyst-growth sweep (2,500 + 1,050 blocks, Decay 5)

Status: FAILED

> **Correction (2026-10-09).** This record was first written from an ad-hoc parse that read
> the `Train Sharpe` line and wrote it into both the `train_sharpe` and `sharpe` columns, and
> it also read only the first of the two pages in the source export. Both defects are fixed
> here: every `Sharpe` below is the out-of-sample column from the dump, `Train Sharpe` is
> shown separately, universe attribution comes from the dump's own `## Universe:` sections,
> and the second page (1,050 blocks) is now recorded. The superseded machine-readable files
> were moved to `simulations/sweeps/superseded/`; the corrected ones are listed below.
> The old numbers were inflated by design, not by chance: `Train Sharpe` differs from
> `Sharpe` in 2,448 of the 2,500 blocks.

Source and artefacts:

```text
Source RTF:   ~/Downloads/Simulation Results.rtf
              size 1,063,519 bytes, md5 1b461cf245bd7fadbd3f42d812389e3f
Parsed text:  simulations/sweeps/sources/20261008_071542.txt  (md5 3a92f8e8980c9b789778aaad65528b9f)
Page 1:       2,500 blocks, six universes  -> 20261008_071542_d1_usa_6universes.{csv,json,md}
Page 2:       1,050 blocks, USA/TOP3000    -> 20261008_071542_d2_usa_top3000.{csv,json,md}
Combined:     3,550 rows                    -> 20261008_071542_all_results.csv, 20261008_071542_SUMMARY.md
Superseded:   simulations/sweeps/superseded/20261008_071542_usa_top3000_industry_decay5.csv
              simulations/sweeps/superseded/20261008_071542_usa_top3000_industry_decay5_field_summary.json
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
