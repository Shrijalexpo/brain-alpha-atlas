# Data and Fields

Choosing the field is the highest-leverage decision in alpha research, and the one most often
made by scrolling rather than reasoning. This page covers how to inspect a field, how to decide
which fields are worth testing, and what the recorded work shows about the families that have
been explored.

## The field is a hypothesis

Before simulating, be able to answer these five questions. If you cannot, the simulation is
guessing. `[Notes]`

```text
Why might this quantity predict returns?
Should a high value be long or short?
Does the raw value need a denominator (per share, per asset, per unit of sales)?
How fast does it update? (quarterly accounting vs daily market data)
Which peer group should it be compared within?
```

The second and third questions catch most weak fields early. Raw accounting levels are largely
company-size signals, so an alpha built on `operating_income` alone is mostly a size bet — and
that is exactly what the recorded early experiments found: Sharpe below 0.5 from several
time-series transforms of raw `operating_income`. `[Observed]`

## Inspecting a field before you use it

| Check | Why it matters |
|---|---|
| **Description** | What the field is supposed to measure; also exposes whether it is an estimate, an actual, or a derived score |
| **Data type (Matrix vs Vector)** | Vector/event fields need `vec_*` reduction before matrix operators |
| **Coverage** | Below ~70% coverage you will get NaNs and a thin book; prefer 90%+ |
| **Date coverage** | A field with a short history cannot be judged on a five-year backtest |
| **Unit** | Combining fields with different units produces warnings and meaningless sums |
| **Update frequency** | Daily price data and quarterly accounting data react to different transformations |

`[Platform]` `[Notes]`

The Data Explorer is the place to do this. `[Platform]` A systematic diagnostic workflow —
including expressions that measure coverage and behaviour of an unfamiliar field — is recorded
in [`Data/data_explorer_and_field_research.md`](../Data/data_explorer_and_field_research.md).
`[Notes]`

## Do not select by alpha count alone

The "Alphas" count on a field tells you how often it has been used, not whether it predicts.
Both extremes carry information: `[Notes]`

| Count | Possible meanings |
|---|---|
| Low | Underexplored — or new, hard to use, low coverage, or weak |
| High | Crowded — or genuinely useful and economically meaningful |

The right order of priority is: **economic intuition → coverage → data type → date coverage →
alpha count as a secondary hint.** `[Notes]`

There is an important consequence for anyone tempted to hunt for the least-used field: low
usage is not evidence of opportunity. In the recorded EUR work, the crowded `anl10_*` analyst
family saturated around Sharpe 1.2–1.4, but the *un*crowded fields did not do better — the
highest blocks came from specific well-covered fields within recognised families, not from
obscure ones. `[Observed]`

## Field families that appear in this repository's research

The table below summarises what the recorded sweeps found, by field prefix. Coverage: EUR sweeps
(067–069, 4,223 blocks) and the USA/AMR/KOR/EUR bundle (070–071, 9,096 blocks).
`[Observed]`

| Prefix | What it generally is | Recorded outcome |
|---|---|---|
| `anl10_*` | Analyst consensus, revisions, "smart estimate" model scores | Large and crowded; single-field transforms saturate near Sharpe 1.2–1.4. USA page: 318 blocks, best 1.21 Sharpe / 0.96 Fitness |
| `anl15_*` | Broker/aggregate estimate fields | Largest family in the USA page (1,226 blocks) and weak: best 1.23 Sharpe / 0.97 Fitness |
| `anl69_*` | Slow analyst estimate/report fields | The best EUR risk-adjusted pocket: `ts_quantile`/`ts_scale` forms reached 1.82 Sharpe / 1.41 Fitness at 15% turnover. In USA the same prefix behaved differently — see the warning below |
| `anl4_*` | Analyst guidance and advanced estimate families | High variance; some high-Sharpe/low-Fitness blocks. Not a ready cluster |
| `anl11_*` | ESG / coverage / industry rank | Weak in both EUR and USA — ESG ranks are effectively static |
| `est_*` | Estimate aggregates and counts | Mid-range; the low-turnover corner costs Sharpe |
| `pv20_*` | Derived price/volume and factor-style indicators | Weak in the USA grid (best 1.22 Sharpe / 0.77 Fitness); one `pv20` block was the best EUR decay-5 result |
| `pv37_*` | Snapshot volume fields | Highest raw EUR Sharpe (2.3–2.5) but structurally high turnover — hostage to `HIGH_TURNOVER` and `LOW_SUB_UNIVERSE_SHARPE` |
| `snt21*`, `scl12*` | Sentiment scores and buzz | Sharpe can clear 1.2 but Fitness and turnover fail; `*_fast_d1` variants are consistently too fast |
| `fnd28_*`, `fnd23_*`, `fnd17_*` | Fundamental value/ratio matrices | Weak in single-field USA form; the good EUR `fnd17` block did not port to USA |
| `mdl39_*` | Model value-momentum ranks | AMR: several blocks near 1.6 Sharpe / 1.4 Fitness at ~7% turnover, but the leaders were still `PENDING` — unverified |
| `oth176_lmt_close_eq_score` | Unclassified ("other" dataset) score field | The strongest single block in the 5,546-block bundle: 2.36 Sharpe / 1.67 Fitness, failing only the 2-year check. One observation |
| `implied_volatility_*`, `historical_volatility_*` | Option-implied and realised volatility | Basis of the strongest USA surface recorded: 2.21–2.61 Sharpe / 1.07–1.88 Fitness, blocked by `CONCENTRATED_WEIGHT` |

## Fields to avoid

These are recorded as unusable inputs, with the reason. `[Observed]`

| Field / pattern | Reason |
|---|---|
| `adjfactor` | A price-adjustment factor, not a cross-sectional signal. It appeared as the 2nd- and 3rd-best EUR block in one sweep purely because it is an accounting device, and it trips `CONCENTRATED_WEIGHT` |
| `pv37_low_14` | Produced a degenerate book: 100% turnover, zero drawdown, 12 long vs 218 short |
| `pv47_spret` and `pv47_for_statssimple_only_spret` | Spurious-return fields; blocks reached Sharpe −1.8 to −2.1 with damaged drawdown |
| `net_9_feature3_predictor` | Synthetic model feature; instrumented appearance, not a market quantity |
| `option_return_bucket*` | Bucket/probability series rather than a cross-sectional quantity |
| `*_currency_code`, `expected_report_*` variance fields | Produced artifacts or sub-1% turnover |
| Universe fields (`top2000`, …) | These select instruments; they are not predictive signals |

## The cross-region trap

Field prefixes are not portable semantics. The recorded evidence is unambiguous on this point:
the `anl69_*` fields that formed the best EUR pocket (slow estimate levels) behaved completely
differently in the USA page, where the same prefix surfaced as report-time and best-estimate
variants and topped out at Sharpe 1.09. `[Observed]`

The practical rule: **before reusing a field name in a new region, confirm that the field is the
same kind of quantity.** Check its description and update frequency, not just its name.

The same caution applies to whole results. A block that works in EUR TOP2500 is not evidence
about USA TOP3000, and a result in one universe is not evidence about another — in the USA page,
every block above Sharpe 1.25 came from TOP3000 and none from the five smaller universes on the
same field list. `[Observed]`

## Working with groups and buckets

Field values become comparable only within a sensible peer group. Two mechanisms: `[Platform]`

- **Settings neutralization** — applied to the finished alpha (see [Simulation settings](02-simulation-settings.md)).
- **`bucket` + `group_*` inside the expression** — e.g. `bucket(rank(cap), range="0.1,1,0.1")` to compare within size deciles.

Size bucketing is the most common explicit grouping in the recorded work, and it is usually
motivated by a real economic asymmetry: a valuation ratio means different things for a
mega-cap and a micro-cap. `[Notes]`

What bucketing does not do is control the final book — the strongest USA block used cap-decile
neutralisation and still failed `CONCENTRATED_WEIGHT`. `[Observed]`

Next: [Research workflow](06-research-workflow.md).
