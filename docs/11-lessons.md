# Lessons From The Recorded Research

Durable lessons extracted from the experiments in this repository. Each one is traceable to
recorded evidence, marked with `[Observed]`, or is an explicit interpretation marked
`[Hypothesis]`.

## On signal strength

- **Raw fundamental levels are size signals.** Time-series transforms of raw `operating_income`
  (`ts_rank`, `ts_mean`, `ts_delta`) all produced Sharpe below 0.5 in the early records. Ratios —
  per asset, per unit of sales, per unit of enterprise value — are the minimum viable form.
  `[Observed]`
- **Stacking similar factors dilutes rather than compounds.** A large linear quality/value
  composite returned −0.28, and a multiplicative interaction of the same components returned
  −1.01. `[Observed]`
- **The transform can matter more than the field.** On slow analyst level fields,
  `ts_scale(x, 63)` / `ts_quantile(x, 63)` beat plain `rank(ts_backfill(x, 21))` consistently.
  `[Observed]`
- **A crowded family is not automatically a dead family; an uncrowded field is not automatically
  an opportunity.** The crowded `anl10_*` analyst family saturates around Sharpe 1.2–1.4, but the
  best blocks in the recorded sweeps came from well-known families, not obscure fields.
  `[Observed]`

## On settings

- **Decay moves turnover, not Sharpe.** Across a decay-0 sweep and a decay-5 sweep with
  overlapping fields, the rank ordering of Sharpe was broadly stable while turnover changed
  substantially. `[Observed]`
- **Decay does not fix concentration.** The USA implied-volatility family failed
  `CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE` identically at decay 4, 6 and 8. `[Observed]`
- **Universe size changes the game more than most settings.** On one USA field list, all 12
  blocks above Sharpe 1.25 came from TOP3000; the five smaller universes produced none.
  `[Observed]`
- **Universe behaviour is region-specific.** EUR TOPCS1600 behaved as its own surface: best
  decay-5 result 0.82 Sharpe, while the decay-0 work reached 1.82 / 1.41. `[Observed]`
- **Neutralisation level matters and interacts with dataset type.** Model and analyst families in
  a TOP600 universe performed best at subindustry in the recorded AMR work, against general
  guidance that suggests broader groups for price/volume and option data. `[Observed]` `[Platform]`

## On the submission gates

- **The binding constraint has moved from strength to structure.** Five regions now produce
  blocks above Sharpe 2.2 in the recorded data, and the failures are
  `CONCENTRATED_WEIGHT`, `LOW_SUB_UNIVERSE_SHARPE`, `LOW_2Y_SHARPE` and the consistency checks —
  not the headline Sharpe. `[Observed]`
- **`LOW_2Y_SHARPE` is the least addressable failure.** It was the single failed check on the
  strongest block in a 5,546-block bundle (Sharpe 2.36 / Fitness 1.67), and it fails 96.5% of
  KOR/TOP600 blocks. `[Observed]`
- **Weight concentration and sub-universe failure travel together** and indicate construction
  problems, not tuning problems. `[Observed]`
- **Region-specific bars differ.** AMR/TOP600 blocks at Sharpe 1.4–1.6 still failed
  `LOW_SHARPE`. `[Observed]`
- **Self-correlation kills good alphas without warning.** Four recorded experiments cleared the
  metrics and were rejected for similarity (self-correlation 0.88–0.94), all sharing a
  quality/improvement-plus-reversal backbone. `[Observed]`

## On method

- **Field screens do not produce submittable alphas.** 4,223 EUR blocks, 3,550 USA blocks and
  5,546 multi-region blocks produced zero passes between them. The three experiments that cleared
  the checks were small, deliberate iterations. `[Observed]`
- **Record the settings with the result.** A number without its region, universe, delay, decay and
  neutralisation is not reproducible and therefore not evidence. `[Notes]`
- **Separate train from out-of-sample, always.** In the USA sweep the two columns disagreed in
  2,448 of 2,500 blocks, with the training column systematically higher, by up to 0.29 on a
  headline block. `[Observed]`
- **Watch for alias fields.** Two `anl69` fields returned byte-identical metrics in one sweep;
  they are one signal, not two confirmations. Fields can also differ wildly in meaning across
  regions despite a shared prefix. `[Observed]`
- **`PENDING` is not `PASS`.** 42 of 5,546 blocks in the latest bundle were still computing when
  the page was captured, including the top four in one region. An unevaluated block is not a
  near-pass. `[Observed]`
- **One pasted result page can contain several experiments.** The declared count describes only
  the first page; a file-level read silently drops the rest. `[Observed]`

## On building an alpha that passes

The only family in this repository that cleared the checks and was submitted has a recognisable
shape: `[Observed]`

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
/* Sharpe 1.61  Fitness 1.02  Turnover 25.25%  Sub-universe 1.53 */

rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))
/* Sharpe 1.46  Fitness 1.05 — submitted */
```

Three things are worth extracting from it:

1. **A slow value anchor** (`ebitda / enterprise_value`), time-series ranked so it is compared
   against its own history.
2. **A growth confirmation** (`sales_growth`), also time-series ranked — a different data
   category, so it adds information rather than repeating the value signal.
3. **A smoothed reversal term** (`ts_mean(-returns, 5)`), which supplies the short-horizon timing
   and was the specific change that lifted Fitness above the bar.

The same repository also shows the failure mode of this shape: adding a further quality/improvement
term to the same backbone produced self-correlation failures, and longer reversal windows weakened
the result. `[Observed]` The winning configuration is narrow — which is why it is recorded as a
protected baseline rather than a template to re-propose.

## Open questions (not settled by the evidence here)

These are recorded as open, so nobody mistakes them for conclusions: `[Hypothesis]`

- Whether the implied-volatility family's concentration failure is fixable by finer buckets, or
  whether the mechanism is intrinsically low-breadth in a TOP3000 universe.
- Whether the AMR `mdl39` value-momentum blocks (≈1.6 Sharpe / 1.4 Fitness at ~7% turnover) are
  genuinely clean — the leaders were still `PENDING` when the page was captured.
- Whether `LOW_2Y_SHARPE` failures are a regime artifact of the recorded period or a genuine
  decay in these signal families.
- Whether the KOR `oth176_lmt_close_eq_score` block is a real signal or a single-field
  coincidence; it is one observation with no independent confirmation.

Next: [Regions and universes](12-regions-and-universes.md) ·
[Sources and evidence policy](15-sources-and-policy.md).
