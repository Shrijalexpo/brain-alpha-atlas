# Superseded sweep artefacts

Files here are kept for provenance only. **Do not use them for analysis.** Each was replaced
after a defect was found in how it was generated.

## `20261008_071542_usa_top3000_industry_decay5.csv` + `..._field_summary.json`

Removed from the parent directory on 2026-10-09.

| Defect | Detail |
|---|---|
| Wrong Sharpe column | The `sharpe` column held the dump's **`Train Sharpe`** value for all 2,500 rows. The real out-of-sample `Sharpe` differs in 2,448 of them (e.g. `annual_financing_cashflow_amount` is 1.40, not 1.69). Every conclusion drawn from this file inherited the inflation. |
| Wrong universe label | The page is split into six universes (TOP200, TOP500, TOP1000, TOP2000, TOP3000, TOPSP500); the filename and the record claimed TOP3000 only. 306 rows were mislabelled. |
| Missing page | The source export contained a second page of 1,050 USA/TOP3000 blocks that was never parsed. |

Replaced by, in the parent directory:

```text
20261008_071542_d1_usa_6universes.{csv,json,md}    page 1, 2,500 blocks, true Sharpe, per-universe rows
20261008_071542_d2_usa_top3000.{csv,json,md}       page 2, 1,050 blocks (previously unrecorded)
20261008_071542_all_results.csv                    3,550 rows
20261008_071542_SUMMARY.md                         cross-page comparison
```

Regenerate from the archived source text:

```bash
cd "~/Documents/Quant DB"
python3 Tools/brain_sweep_parser.py \
  simulations/sweeps/sources/20261008_071542.txt \
  --outdir simulations/sweeps --prefix 20261008_071542_
```
