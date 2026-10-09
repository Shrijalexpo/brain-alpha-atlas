# EUR Multi-Simulation Sweeps (2026-10-04 → 2026-10-06)

Raw pasted BRAIN "N Results" pages for three EUR sweeps, parsed into machine-readable
files. These are bulk sweeps, not hand-crafted alphas: each dump is one page of the
BRAIN multi-simulation results table, transcribed verbatim by the user.

## Files

| File | Blocks | Region / Universe / Neutralization | Decay | Source dump |
|---|---:|---|---:|---|
| `20261004_171500.*` | 314 | EUR / TOP2500 / COUNTRY | 5 | `Pasted text(20261004-171500).txt` |
| `20261005_123752.*` | 2,100 | EUR / TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 / MARKET, INDUSTRY, COUNTRY | 5 | `Pasted text(20261005-123752).txt` |
| `20261006_100742.*` | 1,809 | EUR / TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 / INDUSTRY, MARKET, COUNTRY | 0 | `Pasted text(20261006-100742).txt` |
| `all_results.csv` | 4,223 | all of the above, one row per result block | — | combined |
| `SUMMARY.md` | — | cross-dump comparison + expressions repeated across dumps | — | combined |

Per dump there are three artifacts with the same stem:

- `<stem>.csv` — one row per result block, ready for spreadsheet analysis.
- `<stem>.json` — the same data plus settings, the file-specific `Fx` legend, and section offsets.
- `<stem>.md` — generated report: headline counts, failed-check frequency, top-30 tables,
  best-per-section, and per-field-family bests.

All four columns of every block (expression, train Sharpe, Sharpe, turnover, fitness,
returns, drawdown, margin, long/short counts, failed checks) are preserved.

## How to regenerate

```bash
cd "~/Documents/Quant DB"
python3 Tools/brain_sweep_parser.py --selftest
python3 Tools/brain_sweep_parser.py \
  "~/Downloads/Pasted text(20261004-171500).txt" \
  "~/Downloads/Pasted text(20261005-123752).txt" \
  "~/Downloads/Pasted text(20261006-100742).txt" \
  --outdir simulations/sweeps
```

## Later bundles in this directory

The three EUR dumps above are the original EUR bundle. Two more dumps have since been parsed
into the same directory, plus the raw page text of both:

| Stem | Blocks | Region / Universe / Neutralization | Source dump |
|---|---:|---|---|
| `20261008_071542_d1_usa_6universes.*` | 2,500 | USA / TOP3000, TOPSP500, TOP200, TOP2000, TOP500, TOP1000 / INDUSTRY | `~/Downloads/Simulation Results.rtf` (md5 `1b461cf245bd7fadbd3f42d812389e3f`) |
| `20261008_071542_d2_usa_top3000.*` | 1,050 | USA / TOP3000 / INDUSTRY | same export, second page |
| `20261008_071542_all_results.csv`, `20261008_071542_SUMMARY.md` | 3,550 | combined | — |
| `20261009_115500_d1_kor_top600.*` | 789 | KOR / TOP600 / INDUSTRY, MARKET, SUBINDUSTRY | `~/Downloads/Simulation .rtf` (md5 `862d3bacb18569ae2aea90cc6717c493`) |
| `20261009_115500_d2_amr_top600.*` | 3,250 | AMR / TOP600 / SUBINDUSTRY, INDUSTRY, MARKET | same export, page 2 |
| `20261009_115500_d3_eur_5universes.*` | 1,141 | EUR / TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 / COUNTRY, INDUSTRY | page 3 |
| `20261009_115500_d4_all_large.*` | 113 | ALL / LARGE / INDUSTRY | page 4 |
| `20261009_115500_d5_usa_top3000.*` | 174 | USA / TOP3000 / SUBINDUSTRY, INDUSTRY, MARKET, SECTOR, NONE; decay varies per block | page 5 |
| `20261009_115500_d6_all_large.*` | 79 | ALL / LARGE / INDUSTRY | page 6 |
| `20261009_115500_all_results.csv`, `20261009_115500_SUMMARY.md` | 5,546 | combined | — |

`20261008_071542` supersedes `20261008_071542_usa_top3000_industry_decay5.csv` and its
`_field_summary.json`, which held the dump's `Train Sharpe` in the `sharpe` column and missed
the second page. Those two files are in `superseded/` with an explanation.

### `sources/` — the parsed page text

Each dump's pasted text is archived as `sources/<stem>.txt` so a sweep can be re-parsed years
later; the earlier EUR dumps only ever existed as transient `Pasted text(...).txt` files in
`~/Downloads` and cannot be re-parsed from this repository.

### Parser capabilities added 2026-10-09

`Tools/brain_sweep_parser.py` now handles what these two exports needed:

1. **Several pages concatenated in one file.** The declared `N Results` header only describes
   the first page, so the parser splits on every such header and gives each page its own
   settings, its own `Fx` legend and its own slug (`<stem>_d<N>_<region>_<universe>`).
2. **Decay-style pages** whose blocks are headed `### Decay: <n> · Truncation: <x>` instead of
   `### Result <n>`. Those have no result number in the source, so `result_no` is synthesised
   (flagged `number_synthesised`) and `decay`/`truncation` are stored per row. Such pages also
   report `Train Fitness` in place of `Train Sharpe`, which is parsed into `train_fitness`.
3. **`--prefix NAME_`** for the combined `all_results.csv` / `SUMMARY.md`, so a new bundle
   cannot overwrite one already stored in the same directory.

The per-dump CSV columns are now `result_no, universe, neutralization, decay, truncation,
family, primary_field, sharpe, train_sharpe, train_fitness, fitness, turnover, returns,
drawdown, margin_bps, long_count, short_count, status, failed_check_codes, failed_checks,
expression` — note that `sharpe` and `train_sharpe` are separate columns and must not be
conflated.

```bash
cd "~/Documents/Quant DB"
python3 Tools/brain_sweep_parser.py --selftest
python3 Tools/brain_sweep_parser.py simulations/sweeps/sources/20261008_071542.txt \
  --outdir simulations/sweeps --prefix 20261008_071542_
python3 Tools/brain_sweep_parser.py simulations/sweeps/sources/20261009_115500.txt \
  --outdir simulations/sweeps --prefix 20261009_115500_
```

## Caveats that must be honoured when reading these files

1. **The `Fx` failed-check legend is per dump.** `F14` means `LOW_FITNESS, HIGH_TURNOVER,
   LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE` in the 2026-10-06 dump but
   `LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE,
   LOW_2Y_SHARPE` in the 2026-10-04 dump. The parser resolves each code through its own
   dump's legend and stores the resolved names in `failed_checks`; use those, never the
   raw codes, when comparing across dumps.
2. **Nothing here passed all checks.** 0 of 4,223 blocks are `PASS`. Every alpha in these
   dumps failed at least one platform check, so none is submittable as-is.
3. **Two blocks are degenerate artifacts, not signal**: `pv37_low_14` (Sharpe 11.18,
   turnover exactly 100.00%, drawdown 0.00%, 12 long / 218 short) and `adjfactor`
   (Sharpe 1.94, returns 31.20%, 295 long / 25 short, fails `CONCENTRATED_WEIGHT` and
   `IS_LADDER_SHARPE`). Both need field diagnostics before any interpretation.
4. **Train Sharpe vs Sharpe columns differ**, sometimes by a lot, and several fields show
   a large out-of-sample drop. Treat the second column as the headline number.
5. Numbers are transcribed from a pasted page; treat the metrics as indicative and confirm
   anything important with a fresh single simulation.

## Headline findings

- **`LOW_2Y_SHARPE` is the universal binding constraint**: it appears in 95.5%, 98.3% and
  92.3% of failed blocks in the three dumps. The last-2-year window is what kills this
  work, not the headline Sharpe.
- 27 blocks reach Sharpe ≥ 1.25 **and** Fitness ≥ 1.0 across the three dumps (2 + 7 + 8
  counting the two degenerate ones); none clears sub-universe or 2-year Sharpe.
- The **`anl69_*` analyst family** (96 blocks) is the only family where every
  Sharpe ≥ 1.25 result also cleared Fitness 1.0 (4 of 4). Its best is
  `ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)` at Sharpe 1.97 / Fitness 1.58
  / turnover 5.78%.
- **`pv37_*` volume** fields produce the highest raw Sharpe (2.51 / 2.41 / 2.33 at decay 5)
  but are hostage to `HIGH_TURNOVER` and `LOW_SUB_UNIVERSE_SHARPE`; at decay 0 with short
  windows they exceed 100% turnover.
- **EUR TOPCS1600 is much harder than TOP2500** in these sweeps: best decay-5 result is
  Sharpe 0.82, and the best decay-0 result is Sharpe 1.82 / Fitness 1.41.
- The consultant tests are already firing in this EUR session: `IS_LADDER_SHARPE` appears in
  3 blocks and `LOW_ROBUST_UNIVERSE_SHARPE` in 6. See
  `tutorials/consultant_information/submission_tests_and_alpha_types.md`.

## Where these are recorded

- `simulations/067_eur_top2500_country_analyst_sweep.md` — the 314-block dump
- `simulations/068_eur_multi_universe_decay5_sweep.md` — the 2,100-block dump
- `simulations/069_eur_multi_universe_decay0_sweep.md` — the 1,809-block dump
- `simulations/070_usa_top3000_industry_analyst_growth_sweep.md` — the 2026-10-08 USA export,
  2,500 + 1,050 blocks, numbers corrected 2026-10-09
- `simulations/071_multi_region_bundle_20261009.md` — the six-page KOR/AMR/EUR/GLB/USA bundle
- `simulations/status_index.md` — status rows plus the escalation-candidate table
- `Research/lessons_from_simulations.md` — the durable lessons
- `Data/datasets_and_fields.md` — field-family notes
