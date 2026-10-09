# Simulation 071 — Six-page multi-region sweep bundle (5,546 blocks)

Status: FAILED (0 blocks passed all checks; 42 blocks are still `PENDING`)

This is not one alpha. It is one RTF export containing **six concatenated BRAIN
multi-simulation pages** covering five regions. Each page has its own settings and its own
`Fx` failed-check legend, so the pages are recorded and read separately.

Source and provenance:

```text
Source RTF:   ~/Downloads/Simulation .rtf
              size 1,674,831 bytes, md5 862d3bacb18569ae2aea90cc6717c493
Parsed text:  simulations/sweeps/sources/20261009_115500.txt
              md5 485d8962d27370eda1bbbdde118bd322
Artifacts:    simulations/sweeps/20261009_115500_d1..d6_*.{csv,json,md}
              simulations/sweeps/20261009_115500_all_results.csv   (5,546 rows)
              simulations/sweeps/20261009_115500_SUMMARY.md
```

Parsed counts (declared header vs parsed blocks — all pages reconcile exactly):

| Page | Region / Universe | Neutralizations | Blocks | Declared | Sharpe ≥1.25 & Fitness ≥1.0 | PASS | PENDING | Top Sharpe |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| d1 | KOR / TOP600 | INDUSTRY, MARKET, SUBINDUSTRY | 789 | 789 | 2 | 0 | 0 | 2.36 |
| d2 | AMR / TOP600 | SUBINDUSTRY, INDUSTRY, MARKET | 3,250 | 3,250 | 19 | 0 | 25 | 1.69 |
| d3 | EUR / TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 | COUNTRY, INDUSTRY | 1,141 | 1,141 | 7 | 0 | 15 | 2.63 |
| d4 | ALL / LARGE | INDUSTRY | 113 | 113 | 0 | 0 | 0 | 1.42 |
| d5 | USA / TOP3000 | SUBINDUSTRY, INDUSTRY, MARKET, SECTOR, NONE | 174 | 174 | 7 | 0 | 2 | 2.61 |
| d6 | ALL / LARGE | INDUSTRY | 79 | 79 | 0 | 0 | 0 | 0.72 |

Totals: **5,546 blocks, 0 PASS, 42 PENDING, 35 blocks at or above Sharpe 1.25 with
Fitness 1.0 — of which 12 have no verdict yet.** A `PENDING` block is unevaluated, not
clean; never quote one as a near-pass.

Settings per page (Delay 1, Truncation 0.08, Pasteurization ON, NaN Handling ON throughout):

```text
d1  Region KOR  Universe TOP600   Decay 5   (neutralization varies by section)
d2  Region AMR  Universe TOP600   Decay 5   (neutralization varies by section)
d3  Region EUR  (Universe varies by section)  Decay 5
d4  Region ALL  Universe LARGE    Decay 5  Neutralization INDUSTRY
d5  Region USA  Universe TOP3000  Decay varies per block: 0,3,4,5,6,7,8,10,12,16
d6  Region ALL  Universe LARGE    Decay 5  Neutralization INDUSTRY
```

Page d5 is the first page in this workspace whose blocks are pasted in the
`### Decay: N · Truncation: X` form instead of `### Result N`, and it reports
`Train Fitness` in place of `Train Sharpe`. Those blocks carry no number in the source, so
`result_no` in the CSV is a synthesised sequence and per-block decay/truncation live in
their own columns.

## Best blocks (all already simulated — repair targets only)

### KOR / TOP600 — the single strongest block in the bundle

```text
Expression: normalize(ts_backfill(oth176_lmt_close_eq_score, 21))
Universe: TOP600   Neutralization: INDUSTRY   Decay 5
Train Sharpe: 2.79
Sharpe: 2.36
Fitness: 1.67
Turnover: 32.62%
Returns: 16.28%
Drawdown: 13.39%
Margin: 9.98 bps
Long / Short: 264 / 252
Checks: FAIL LOW_2Y_SHARPE   (that is the ONLY failed check)
```

This is the highest Sharpe-and-Fitness pair anywhere in the bundle, and the only block in it
that fails a single check. `LOW_2Y_SHARPE` is the whole gap: 761 of 789 KOR blocks (96.5%)
fail it, so the 2-year window — not strength, not turnover — is the binding constraint.

Second KOR block at both thresholds: `zscore(ts_backfill(analyst_revisions_revenue_score, 21))`
— Sharpe 1.26 / Fitness 1.03 / Turnover 5.38% / INDUSTRY, fails LOW_SHARPE + CONCENTRATED_WEIGHT.

### USA / TOP3000 — implied-volatility dispersion, group_neutralized on buckets

```text
Expression: iv_signal = zscore(implied_volatility_call_120 - implied_volatility_put_120) + rank(implied_volatility_call_120 / historical_volatility_120); cap_group = bucket(rank(cap), range="0.1,1,0.1"); group_neutralize(iv_signal, cap_group)
Universe: TOP3000   Neutralization: SUBINDUSTRY   Decay 6   Truncation 0.08
Train Fitness: 1.76
Sharpe: 2.61
Fitness: 1.88
Turnover: 35.73%
Returns: 18.61%
Drawdown: 7.62%
Margin: 10.42 bps
Long / Short: 1427 / 1201
Checks: FAIL CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE
```

This is the best USA block in the workspace so far, well clear of the previous best
(Simulation 070: Sharpe 1.54 / Fitness 0.98). The family is coherent — three more variants
land at 2.34 / 2.29 / 2.21 Sharpe with Fitness 1.47 / 1.47 / 1.07 — and it is a genuinely
different mechanism from the equity-fundamental work:

```text
[2] Decay 4, SUBINDUSTRY — Sharpe 2.34 / Fitness 1.47 / Turnover 48.23%
    iv_difference = implied_volatility_call_120 - implied_volatility_put_120; hv_group = bucket(rank(ts_rank(operating_income / cap, 250)), range="0.1,1,0.1"); group_neutralize(iv_difference, hv_group)

[3] Decay 4, SUBINDUSTRY — Sharpe 2.29 / Fitness 1.47 / Turnover 47.32%
    iv_difference = implied_volatility_call_120 - implied_volatility_put_120; hv_group = bucket(rank(ts_sum(vec_avg(nws12_afterhsz_sl), 60)), range="0.1,1,0.1"); group_neutralize(iv_difference, hv_group)

[4] Decay 8, SUBINDUSTRY — Sharpe 2.21 / Fitness 1.07 / Turnover 32.91%
    hv_group = bucket(rank(historical_volatility_120), range="0.1,1,0.1"); group_neutralize(rank(implied_volatility_call_120 - implied_volatility_put_120), hv_group)
```

The mechanism is option-implied vs realized volatility: the call-minus-put 120-day IV
difference, plus an IV-to-realized-vol ratio, neutralized inside cap or volatility deciles so
the book is not a single risk bucket. Every variant fails the same two checks:
`CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE`. Decay does not fix either — decay 4, 6
and 8 all fail the same pair — so the repair is book construction (more buckets, tighter
truncation, or a size-neutral cap grouping), not smoothing.

Two further USA blocks clear both thresholds with no verdict yet:

```text
Decay 4  — Sharpe 2.17 / Fitness 1.10 / Turnover 30.08% / SUBINDUSTRY / PENDING
rank(ts_rank(operating_income / cap, 250)) > 0.5 ? 1 : rank(-ts_delta(close, 2))

Decay 16 — Sharpe 1.73 / Fitness 1.02 / Turnover 33.13% / SUBINDUSTRY / PENDING
zscore(rank(-returns) + 0.25 * rank(ts_rank(fnd6_cptnewqv1300_epsfxq, 126)) + 0.25 * rank(...))
```

### AMR / TOP600 — model value-momentum (`mdl39_*`), leaders not yet evaluated

10 of the 19 AMR blocks at both thresholds are `PENDING`, including the top four, so the AMR
leaderboard is **not readable yet**. The evaluated leader is:

```text
Expression: scale(ts_av_diff(ts_backfill(industry_relative_valuation_rank_3, 21), 126))
Universe: TOP600   Neutralization: SUBINDUSTRY   Decay 5
Sharpe: 1.54   Fitness: 1.40   Turnover: 10.96%
Checks: FAIL LOW_SHARPE
```

The pending family is worth one deliberate re-run: `mdl39_12_val_mo_industry_rank` and
`mdl39_12_val_mo_sector_rank` (model 39 industry/sector value-momentum rank) appear as
`group_zscore`, `quantile`, `scale`, `winsorize`, `group_scale` variants, all around
Sharpe 1.60–1.69 / Fitness 1.39–1.49 at ~7% turnover. Note `LOW_SHARPE` fires on AMR blocks
with Sharpe 1.4–1.6, so the AMR/TOP600 Sharpe bar is above the workspace's 1.25 assumption —
do not import the USA threshold into this region.

### EUR — highest raw Sharpe, worst turnover, and a known artifact again

```text
Expression: ts_zscore(ts_backfill(pv20_netdebt_best_eeps_nxt_yr_434, 21), 5)
Universe: TOP2500   Neutralization: COUNTRY   Decay 5
Sharpe: 2.63   Fitness: 1.24   Turnover: 69.46%   Returns: 15.54%   Drawdown: 9.15%
Checks: FAIL LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE
```

`adjfactor` reappears as the second-best EUR block — Sharpe 1.80 / Fitness 1.24 at 59.31%
turnover, and `normalize(ts_backfill(adjfactor, 21))` at 1.66 / 1.08 triggering
`IS_LADDER_SHARPE` as well as `CONCENTRATED_WEIGHT`. It is a price-adjustment factor, not a
signal; see the do-not-re-run table in `status_index.md`. EUR's own consultant checks are
active in this page: `CLUSTER_TEST` 27 blocks, `LOW_ROBUST_UNIVERSE_SHARPE` 35 blocks.

### ALL / LARGE (GLB) — 192 blocks, no thresholds cleared

The two GLB pages are a field screen that has not produced anything usable: best Sharpe 1.42
(`winsorize(ts_scale(ts_backfill(anl69_pe_all_delay_1_best_eeps_nxt_yr, 21), 5))`,
Fitness 0.57) and best Fitness 0.57 across 192 blocks. They do add new check vocabulary that
will appear on any future GLB work: `LOW_GLB_APAC_SHARPE` (44), `LOW_ASI_JPN_SHARPE` (30),
`LOW_GLB_AMER_SHARPE` (27), `LOW_GLB_EMEA_SHARPE` (27), plus
`LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` (15) and `LOW_ROBUST_UNIVERSE_RETURNS` (18) — i.e. the
global scope is judged on Asia/Japan separately, not only on the headline Sharpe.

## Consultant-level tests are now the visible ceiling

`IS_LADDER_SHARPE` fires in **96 of 174 USA blocks (55%)** and `CLUSTER_TEST` in 27 EUR
blocks. The blocks with the best headline metrics are exactly the ones being stopped by
these consultant-stage checks or by weight concentration:

| Page | Block | Sharpe | Fitness | Checks |
|---|---|---:|---:|---|
| d5 | IV dispersion on cap buckets | 2.61 | 1.88 | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE |
| d5 | IV difference on op-income/cap buckets | 2.34 | 1.47 | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE |
| d3 | EUR `pv20_netdebt` z-score | 2.63 | 1.24 | LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE |
| d1 | KOR `oth176_lmt_close_eq_score` | 2.36 | 1.67 | LOW_2Y_SHARPE |
| d3 | EUR `adjfactor` z-score | 1.80 | 1.24 | CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE |

Read together with the earlier sweeps: the raw-Sharpe ceiling in every region now sits above
1.9, and the failures have moved from "not enough signal" to book geometry
(`CONCENTRATED_WEIGHT`), robustness (`LOW_SUB_UNIVERSE_SHARPE`, `LOW_2Y_SHARPE`) and the
consultant ladder. Adding more signal is not the bottleneck.

## Duplicate check against earlier sweeps

5,524 of the 5,546 blocks are distinct expressions, and only **19** were already simulated in
the earlier EUR/USA sweep files — so this bundle is almost entirely new ground. The repeats
are EUR analyst-transforms already logged in 067–069 plus a handful of Oct-8 USA blocks; they
are already covered by the existing do-not-re-run and repair-target tables.

Within the bundle itself, 18 expressions repeat across pages (for example
`rank(ts_backfill(dividend, 21))` appears in the AMR page and the EUR page, and
`ts_decay_linear(pcr_oi_1080, 120)` three times in the USA page at different decay settings).
Those are re-tests of one expression under different settings, not independent evidence; see
`20261009_115500_SUMMARY.md` for the full list.

## Failed-check frequency per page

```text
d1 KOR   LOW_FITNESS 786, LOW_SHARPE 785, LOW_2Y_SHARPE 761 (96.5%), LOW_SUB_UNIVERSE_SHARPE 375, CONCENTRATED_WEIGHT 241, HIGH_TURNOVER 30
d2 AMR   LOW_SHARPE 3223 (99.2%), LOW_FITNESS 3214, LOW_2Y_SHARPE 3147, LOW_SUB_UNIVERSE_SHARPE 1590, CONCENTRATED_WEIGHT 1295, HIGH_TURNOVER 120
d3 EUR   LOW_SHARPE 1122, LOW_FITNESS 1119, LOW_2Y_SHARPE 1066, LOW_SUB_UNIVERSE_SHARPE 494, CONCENTRATED_WEIGHT 378, LOW_TURNOVER 104, LOW_ROBUST_UNIVERSE_SHARPE 35, CLUSTER_TEST 27, IS_LADDER_SHARPE 1
d4 ALL   LOW_SHARPE 113, LOW_FITNESS 113, LOW_2Y_SHARPE 112, LOW_SUB_UNIVERSE_SHARPE 74, CONCENTRATED_WEIGHT 47, LOW_GLB_APAC_SHARPE 37
d5 USA   LOW_FITNESS 165, LOW_SHARPE 164, IS_LADDER_SHARPE 96, CONCENTRATED_WEIGHT 69, LOW_2Y_SHARPE 62, LOW_SUB_UNIVERSE_SHARPE 55, LOW_TURNOVER 9, HIGH_TURNOVER 6, CLUSTER_TEST 1
d6 ALL   LOW_SHARPE 78, LOW_FITNESS 78, LOW_2Y_SHARPE 76, CONCENTRATED_WEIGHT 35, LOW_SUB_UNIVERSE_SHARPE 31, LOW_GLB_AMER_SHARPE 7
```

`LOW_FITNESS` is the most common failure in five of the six pages. Unlike the earlier EUR
work, `HIGH_TURNOVER` is rare everywhere here (30 / 120 / 38 / 6 blocks) — these are slow
signals, and the ones that die die on fitness or robustness instead.

## Conclusion

- **0 of 5,546 blocks passed.** But the shape of the failure has changed: five different
  regions now produce blocks above Sharpe 2.2, so the constraint is no longer signal strength
  but the check structure around it.
- The **KOR `oth176_lmt_close_eq_score`** block (2.36 / 1.67, single check `LOW_2Y_SHARPE`) is
  the closest thing to a near-pass in this bundle and the first KOR-scope candidate in the
  workspace.
- The **USA implied-volatility family** is the best USA surface found so far and it is a new
  mechanism, not a variation of the exhausted `cashflow_op / enterprise_value` branch.
- **EUR adds nothing new** beyond confirming `pv20`-style signals die on sub-universe and
  2-year robustness, and that `adjfactor` is an artifact in this region too.
- **GLB / ALL-LARGE is a dead end at this stage**: 192 blocks, best Fitness 0.57.

## Lesson

- A block that fails only `LOW_2Y_SHARPE` while already at Fitness > 1.5 is a robustness
  problem, not a strength problem — the repair is window/regime handling, not more signal.
- `CONCENTRATED_WEIGHT` + `LOW_SUB_UNIVERSE_SHARPE` together, identical across decay 4/6/8,
  means the book is structurally concentrated. Change the portfolio construction (bucket
  count, truncation, cap-neutral grouping) rather than the decay.
- Treat `PENDING` as unmeasured. One quarter of the AMR blocks that clear both thresholds have
  no verdict, and the AMR leaderboard's top four are all in that group.
- Regional Sharpe bars differ: AMR/TOP600 blocks at Sharpe 1.4–1.6 still fail `LOW_SHARPE`,
  so the workspace's 1.25 assumption must not be reused across regions.
- A page pasted in `### Decay: N · Truncation: X` form has no result numbers in the source.
  The parser now synthesises them and keeps decay/truncation per row; never join such a page
  to an earlier one by `result_no`.

## Next action

- Re-run the four pending USA blocks (2.17 / 1.73 and the `pcr_oi_1080` / `fnd6_acdo` decay
  variants) to get verdicts; they are cheap and two of them already clear both user thresholds.
- Try one USA repair of the IV family that attacks `CONCENTRATED_WEIGHT` directly: finer cap
  buckets (`range="0.05,1,0.05"`), or `truncate`/`winsorize` on the final signal, with decay
  and the IV construction unchanged.
- Re-run the top four pending AMR `mdl39_12_val_mo_*` blocks before drawing any conclusion
  about that family.
- Do not spend more sweeps on ALL/LARGE until a GLB page produces Fitness > 1.0 somewhere.
