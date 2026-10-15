# Simulation 068 - EUR Multi-Universe Sweep, Decay 5 (2,100 Results)

Status: FAILED

Type: bulk sweep record (2,100 result blocks across 15 universe/neutralization sections).
Machine-readable data: `Analysis and Simulation Reports/sweeps-and-experiments/20261005_123752.csv` / `.json` / `.md`.
Full generated report with all 2,100 expression rows: `Analysis and Simulation Reports/sweeps-and-experiments/20261005_123752.md`.

## Sweep

Same single-field-transform pattern as simulation 067 but spread over the whole EUR
universe ladder and all three neutralizations, and extended to price/volume, fundamental,
estimate, NLP and sentiment families.

Representative top expression (degenerate, see Conclusion):

```text
ts_product(ts_backfill(pv37_low_14, 21), 63)
```

Best legitimate expression:

```text
rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))
```

## Settings

```text
Instrument Type: Equity (not shown in paste)
Region: EUR
Universe: TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 (sectioned)
Language: Fast Expression
Delay: 1
Decay: 5
Truncation: 0.08
Neutralization: MARKET, INDUSTRY, COUNTRY (sectioned)
Pasteurization: ON
Unit Handling: not shown in paste
NaN Handling: ON
Test Period: not shown in paste
```

## Known result

```text
Blocks: 2,100
Checks PASS: 0
Sharpe >= 1.25: 22
Fitness >= 1.0: 7
Sharpe >= 1.25 AND Fitness >= 1.0: 7
Best Sharpe: 11.18 (degenerate)   Best legitimate Sharpe: 2.51
Best Fitness: 4.60 (degenerate)   Best legitimate Fitness: 1.60
IS_LADDER_SHARPE failures: 2     LOW_ROBUST_UNIVERSE_SHARPE failures: 6
```

Failed-check frequency (resolved through this dump's own legend):

```text
LOW_FITNESS             2092 / 2100   99.6%
LOW_SHARPE              2083 / 2100   99.2%
LOW_2Y_SHARPE           2064 / 2100   98.3%
LOW_SUB_UNIVERSE_SHARPE  973 / 2100   46.3%
CONCENTRATED_WEIGHT      468 / 2100   22.3%
LOW_TURNOVER             120 / 2100    5.7%
HIGH_TURNOVER             83 / 2100    4.0%
LOW_ROBUST_UNIVERSE_SHARPE 6 / 2100    0.3%
IS_LADDER_SHARPE           2 / 2100    0.1%
```

Top 12 by Sharpe:

| # | Section | Sharpe | Train | Fitness | Turnover | Returns | Margin | L/S | Expression | Failed |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | TOP2500/MARKET | 11.18 | 0.00 | 4.60 | 100.00% | 16.96% | 3.39 | 12/218 | `ts_product(ts_backfill(pv37_low_14, 21), 63)` | HIGH_TURNOVER; CONCENTRATED_WEIGHT; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 614 | TOP2500/INDUSTRY | 2.51 | 2.73 | 1.09 | 47.29% | 8.93% | 3.78 | 1390/1422 | `scale(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 126))` | LOW_SUB_UNIVERSE_SHARPE |
| 615 | TOP2500/INDUSTRY | 2.41 | 2.75 | 1.16 | 37.80% | 8.74% | 4.63 | 1419/1375 | `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 616 | TOP2500/INDUSTRY | 2.33 | 2.66 | 1.02 | 45.30% | 8.73% | 3.85 | 1395/1422 | `group_zscore(ts_rank(ts_backfill(pv37_snapshot1_volume112500, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 1382 | TOP2500/COUNTRY | 2.31 | 2.60 | 1.01 | 44.61% | 8.54% | 3.83 | 1390/1428 | `group_zscore(ts_rank(ts_backfill(pv37_snapshot1_volume123500, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 617 | TOP2500/INDUSTRY | 2.25 | 2.55 | 0.97 | 46.30% | 8.56% | 3.70 | 1395/1421 | `group_zscore(ts_rank(ts_backfill(pv37_snapshot1_volume102000, 21), 252), sector)` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 1383 | TOP2500/COUNTRY | 2.25 | 2.63 | 0.77 | 56.74% | 6.71% | 2.37 | 1388/1422 | `group_zscore(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 21), sector)` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 2 | TOP2500/MARKET | 2.16 | 2.43 | 0.96 | 45.10% | 8.90% | 3.95 | 1388/1431 | `ts_rank(ts_backfill(pv37_snapshot1_volume151500, 21), 126)` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 3 | TOP2500/MARKET | 2.08 | 2.34 | 0.83 | 51.60% | 8.12% | 3.15 | 1388/1430 | `ts_rank(ts_backfill(pv37_snapshot1_volume112500, 21), 63)` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 4 | TOP2500/MARKET | 2.02 | 2.25 | 0.92 | 44.12% | 9.16% | 4.15 | 1395/1420 | `normalize(ts_quantile(ts_backfill(pv37_snapshot1_volume123500, 21), 252))` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 5 | TOP2500/MARKET | 1.94 | 2.08 | 1.60 | 45.90% | 31.20% | 13.59 | 295/25 | `normalize(ts_zscore(ts_backfill(adjfactor, 21), 126))` | CONCENTRATED_WEIGHT; LOW_SUB_UNIVERSE_SHARPE; IS_LADDER_SHARPE |
| 618 | TOP2500/INDUSTRY | 1.82 | 2.15 | 0.57 | 58.50% | 5.82% | 1.99 | 1379/1420 | `ts_zscore(ts_quantile(ts_backfill(pv37_snapshot1_volume102000, 21), 21), 252)` | LOW_FITNESS; LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |

All 7 blocks with Sharpe ≥ 1.25 and Fitness ≥ 1.0:

| # | Section | Sharpe | Fitness | Turnover | Returns | Expression | Failed |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | TOP2500/MARKET | 11.18 | 4.60 | 100.00% | 16.96% | `ts_product(ts_backfill(pv37_low_14, 21), 63)` | (degenerate) |
| 5 | TOP2500/MARKET | 1.94 | 1.60 | 45.90% | 31.20% | `normalize(ts_zscore(ts_backfill(adjfactor, 21), 126))` | (artifact field) |
| 615 | TOP2500/INDUSTRY | 2.41 | 1.16 | 37.80% | 8.74% | `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 614 | TOP2500/INDUSTRY | 2.51 | 1.09 | 47.29% | 8.93% | `scale(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 126))` | LOW_SUB_UNIVERSE_SHARPE |
| 620 | TOP2500/INDUSTRY | 1.67 | 1.09 | 6.69% | 5.32% | `rank(ts_scale(ts_backfill(anl10_salfy1_consensus_559, 21), 63))` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 616 | TOP2500/INDUSTRY | 2.33 | 1.02 | 45.30% | 8.73% | `group_zscore(ts_rank(ts_backfill(pv37_snapshot1_volume112500, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |
| 1382 | TOP2500/COUNTRY | 2.31 | 1.01 | 44.61% | 8.54% | `group_zscore(ts_rank(ts_backfill(pv37_snapshot1_volume123500, 21), 252), sector)` | LOW_SUB_UNIVERSE_SHARPE; LOW_2Y_SHARPE |

Best per universe / neutralization section (best Sharpe in each):

| Universe | Neut | Blocks | Best Sharpe | Best Fitness |
|---|---|---:|---:|---:|
| TOP2500 | MARKET | 613 | 11.18 (degenerate) | 4.60 (degenerate) |
| TOP2500 | INDUSTRY | 768 | 2.51 | 1.16 |
| TOP2500 | COUNTRY | 494 | 2.31 | 1.01 |
| TOPCS1600 | MARKET | 17 | 0.82 | 0.85 |
| TOPCS1600 | INDUSTRY | 25 | 0.78 | 0.49 |
| TOPCS1600 | COUNTRY | 13 | 0.43 | 0.11 |
| TOP800 | MARKET | 19 | 0.79 | 0.41 |
| TOP800 | INDUSTRY | 24 | 0.66 | 0.38 |
| TOP800 | COUNTRY | 13 | 0.38 | 0.08 |
| TOP1200 | COUNTRY | 15 | 0.68 | 0.29 |
| TOP1200 | INDUSTRY | 24 | 0.66 | 0.27 |
| TOP1200 | MARKET | 19 | 0.62 | 0.42 |
| TOP400 | COUNTRY | 13 | 0.87 | 0.40 |
| TOP400 | INDUSTRY | 24 | 0.47 | 0.20 |
| TOP400 | MARKET | 19 | 0.44 | 0.21 |

## Conclusion

- **0 of 2,100 blocks passed all checks.** 7 cleared the user-level Sharpe/Fitness bar, and
  two of those seven are fake (see below), leaving five genuine near-misses that all fail
  sub-universe and/or 2-year Sharpe.
- **Two blocks must be discarded as artifacts, not read as signal.**
  `ts_product(ts_backfill(pv37_low_14, 21), 63)` reports Sharpe 11.18 with train Sharpe
  0.00, turnover exactly 100.00%, drawdown 0.00% and only 12 long / 218 short names — a
  degenerate book, not an alpha. `normalize(ts_zscore(ts_backfill(adjfactor, 21), 126))`
  reports Sharpe 1.94 / Fitness 1.60 / returns 31.20% on 295 long / 25 short — `adjfactor`
  is a price-adjustment factor, and its `IS_LADDER_SHARPE` failure plus extreme
  concentration confirm it is not a tradable cross-sectional signal. Both are recorded so
  the exact expressions are never re-proposed.
- **`pv37` snapshot-volume fields are the strongest raw signal in EUR TOP2500** and they
  all carry the same defect profile: Sharpe 2.0–2.5 at 44–57% turnover, Fitness 0.77–1.16,
  failing `LOW_SUB_UNIVERSE_SHARPE` and usually `LOW_2Y_SHARPE`. The signal is real
  (train Sharpe 2.4–2.75 holds up out-of-sample to 2.0–2.5) but the book is not robust
  across sub-universes.
- **Neutralization affects which volume variant works, not whether it works.**
  `group_zscore(..., sector)` on `pv37_snapshot1_volume123500` tops TOP2500/COUNTRY (2.31)
  while the same idea under INDUSTRY peaks on `session_1600to1600_total_traded_volume`
  (2.41). Fixing the volume field and varying neutralization is a productive axis;
  varying the field with fixed neutralization is not (results 614–618 and 1382–1384 are
  one idea).
- **Smaller universes collapse.** Every TOP400/TOP800/TOP1200 section has best Sharpe
  ≤ 0.87. Under decay 5 the EUR sweep has essentially no usable signal below TOP2500 —
  except inside TOPCS1600/MARKET, whose best is Sharpe 0.82 / Fitness 0.85.
- **The consultant tests are already active in this session.** `IS_LADDER_SHARPE` (2
  blocks) and `LOW_ROBUST_UNIVERSE_SHARPE` (6 blocks) appear in this dump's legends, which
  means the EUR ladder and robust-universe checks are being evaluated, not just the
  user-level Sharpe/Fitness bar. The single best-Fitness legitimate block (result 5,
  `adjfactor`) fails `IS_LADDER_SHARPE`.
- **A very low-turnover pocket exists**: `rank(ts_scale(ts_backfill(anl10_salfy1_consensus_559, 21), 63))`
  at Sharpe 1.67 / Fitness 1.09 / 6.69% turnover / 15.91 bps margin, and
  `group_zscore(ts_rank(ts_backfill(fnd28_value_08698q, 21), 252), sector)` at Sharpe 1.60 /
  Fitness 0.93 / 3.32% turnover / 25.31 bps margin. These are inside the < 30% turnover
  band that qualifies for the ×0.85 IS-Ladder PASS relaxation.

## Lesson

- **Discard degenerate books before ranking a sweep.** Any result with turnover pinned at
  100%, drawdown 0.00%, train Sharpe 0.00, or a long/short split like 12/218 or 295/25 is a
  construction artifact. Sorting a 2,100-row sweep by Sharpe without checking long/short
  counts is how a Sharpe 11.18 phantom ends up at the top of the table.
- **`adjfactor` and other corporate-action/identifier fields are not alphas.** They produce
  spectacular-looking returns because they encode an accounting adjustment, not a
  cross-sectional signal.
- **Raw-`rank` on price/volume ratio fields is a trap in EUR.** `rank(ts_backfill(pv37_cap_12, 21))`
  (result 310) produced Sharpe 0.06 / Fitness 0.01; size and cap-style fields are
  neutralization sinks, not signals.
- **Session-volume aggregates are genuinely predictive in EUR TOP2500/INDUSTRY**
  (`session_1600to1600_total_traded_volume`, Sharpe 2.41 / Fitness 1.16), which makes it
  the most interesting non-`pv37` price/volume finding in the sweep.
- Time-series transforms (`ts_zscore`, `ts_quantile`, `ts_scale`) on volume fields beat
  cross-sectional ones (`rank`) at equal windows: the volume edge is largely a
  time-series-level effect.

## Next action

- Escalation candidate: `rank(ts_zscore(ts_backfill(session_1600to1600_total_traded_volume, 21), 252))`
  (Result 615) — highest Fitness (1.16) among legitimate blocks, 37.8% turnover, ~1420
  long/1375 short. Repair target: `LOW_SUB_UNIVERSE_SHARPE` + `LOW_2Y_SHARPE`.
- Second candidate: `scale(ts_quantile(ts_backfill(pv37_snapshot1_volume125500, 21), 126))`
  (Result 614) — Sharpe 2.51 with only `LOW_SUB_UNIVERSE_SHARPE` failing, i.e. the single
  closest block to passing in the whole dump.
- Third, and the one to prefer on risk grounds:
  `rank(ts_scale(ts_backfill(anl10_salfy1_consensus_559, 21), 63))` (Result 620) —
  Sharpe 1.67 / Fitness 1.09 / 6.69% turnover. Low turnover means transaction-cost headroom
  and the ×0.85 IS-Ladder relaxation.
- Do not re-run the `pv37_snapshot1_volume*` grid at 40–60% turnover; that surface is
  mapped. Move to reducing turnover on the same field (higher decay, longer smoothing) or
  to the sub-universe repair problem.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `068` |
| **Record Type** | `Bulk Multi-Simulation Sweep` |
| **Source Dataset / Fields** | Multi-field sweep (analyst, price-volume, fundamental, option/IV) |
| **Region / Delay / Universe** | `EUR` · Delay `1` · `TOP2500, TOPCS1600, TOP1200, TOP800, TOP400 (sectioned)` |
| **Neutralization / Decay / Truncation** | `MARKET, INDUSTRY, COUNTRY (sectioned)` · Decay `5` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-10-05` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `see sweep summary` · Fitness: `see sweep summary` · Turnover: `see sweep summary` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `0` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `ATOM-eligible candidate surface (single-dataset transforms)` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/EUR/068_eur_multi_universe_decay5_sweep.md` |

