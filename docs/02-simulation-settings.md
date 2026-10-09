# Simulation Settings

Settings are set before the run and are part of the result. This page covers each one, what it
does, and what the recorded experiments show about its effect.

## The settings panel

| Setting | What it controls | Notes |
|---|---|---|
| **Instrument Type** | What you trade | Equity for the work in this repository |
| **Region** | The market | USA, EUR, ASI, CHN, KOR, AMR, GLB/ALL … `[Platform]` |
| **Universe** | Instruments inside the region | TOP3000, TOP1000, TOP600, TOPCS1600 … `[Platform]` |
| **Language** | Expression language | Fast Expression in all recorded work |
| **Delay** | Days between data and trading | Delay 1 is standard here `[Notes]` |
| **Decay** | Pre-trade smoothing of the alpha | The main turnover lever |
| **Truncation** | Maximum weight per instrument | Cap on concentration |
| **Neutralization** | Group-centring of final scores | Market, Sector, Industry, Subindustry, Country, None |
| **Pasteurization** | Limits single-day influence | On in all recorded work |
| **NaN Handling** | How missing values are treated | On in the sweeps, Off in the early records |
| **Lookback / Max Trade / Max Position** | Additional platform controls | Off in the documented examples `[Platform]` |
| **Test Period** | Splits in-sample into train and test | See below — required before submission |

## Decay

Decay smooths the alpha across recent days before trading, so the portfolio does not chase
one-day noise. Raising decay lowers turnover, which raises Fitness when turnover is the problem.

What the recorded evidence shows: `[Observed]`

- A EUR sweep run at decay 0 and another at decay 5 covered overlapping fields. Turnover moved
  a lot between them; the rank ordering of Sharpe barely did. The best decay-0 result was
  1.82 Sharpe / 1.41 Fitness on an analyst field, and the analogous decay-5 work was
  1.97 / 1.58 — comparable, not transformed.
- Decay does **not** fix weight concentration. In the USA implied-volatility family, decay 4, 6
  and 8 all failed `CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE` identically. Changing
  decay changed the numbers, not the failure set.

Working rule: `[Notes]`

```text
Turnover too high, signal otherwise good  -> try higher decay (4 -> 6 -> 8), or smooth the
                                            fastest component with ts_mean / ts_decay_linear / hump
Signal weak at low turnover              -> decay is not your problem; change the idea
Concentration or sub-universe failing    -> change the book construction, not decay
```

## Truncation

Truncation caps the largest weight any single instrument can take. It is a blunt instrument
against concentration: it limits damage from one outsized position without changing the
underlying ranking. All recorded sweeps use 0.08. `[Observed]`

Truncation interacts with neutralization: if you neutralise inside very small groups, a few
instruments can end up with large residual weights, and truncation is what stops that from
becoming a concentrated book. `[Hypothesis]`

## Neutralization

Neutralization splits the cross-section into groups and subtracts the group mean, so the alpha
expresses relative performance inside each group rather than a directional market bet.
`[Platform]`

Two ways to do the same thing: `[Platform]`

```text
-zscore(ebit / capex)                 with Neutralization = Industry, Decay 0, Truncation 0
group_neutralize(-zscore(ebit / capex), industry)   with Neutralization = None, Decay 0, Truncation 0
```

If you neutralise explicitly inside the expression, set the settings neutralization to `None`
and set decay and truncation to 0, then apply any smoothing inside the expression. Doing both
at once applies the operation twice. `[Platform]`

Recommended neutralization by dataset category, from the captured platform guidance: `[Platform]`

| Dataset category | Suggested neutralization | Reason given |
|---|---|---|
| Fundamental | Industry | Fundamentals affect prices differently by industry |
| Analyst estimates | Industry | Estimates relate to future fundamentals; compare peers |
| Model datasets | Market, Sector, Industry or Subindustry — experiment | Varies by model subcategory |
| News | Subindustry | Impact differs by company and subindustry |
| Option data | Market or Sector | Option effects are broader than one industry |
| Price/volume | Market or Sector | Generic PV ideas travel across instruments; narrow groups can hurt |
| Social media | Subindustry or Industry | Context-dependent impact |
| Short interest | Industry | |
| Insider | Industry or Subindustry | |
| Sentiment | Industry or Subindustry | |
| Earnings | Industry | |
| Macro | Sector, Market or Industry | Macro effects are broad; subindustry adds little |

Evidence from this repository adds a caveat: analyst and model fields neutralised at
*subindustry* in a TOP600 universe produced some of the strongest blocks recorded (AMR
`mdl39` value-momentum at ~1.6 Sharpe / ~1.4 Fitness with ~7% turnover), while the same
families neutralised at market or industry were weaker. `[Observed]` That is one universe and
one family — treat it as a lead to test, not a rule.

Also worth knowing: `group_*` operators used purely as wrappers over volume or grouping fields
added turnover and `CONCENTRATED_WEIGHT` without adding Sharpe in the EUR sweeps.
`[Observed]` Treat grouping operators as a turnover and weight-concentration tool, not a
Sharpe tool.

## Pasteurization and NaN Handling

Pasteurization restricts how much a single day's data can influence the book, which protects
against stale prices and single-day artifacts. Leaving it on is the safe default and is what
every sweep here uses. `[Platform]`

NaN Handling decides whether missing values are tolerated or substituted. All recorded work
uses On. `[Observed]` Low coverage is better addressed at the field level with `ts_backfill`,
`kth_element` or `group_backfill` than by relying on the setting. `[Platform]`

## Universe

Universe size changes both the difficulty and the result. The recorded evidence is consistent
and blunt: `[Observed]`

- In the USA page of the 2026-10 sweeps, all 12 blocks above Sharpe 1.25 came from TOP3000;
  the smaller universes (TOP200, TOP500, TOP1000, TOP2000, TOPSP500) produced none on the same
  field list.
- In the EUR sweeps, universes below TOP2500 collapsed relative to TOP2500.
- TOPCS1600 behaved like its own surface: in one sweep the best decay-5 result was 0.82 Sharpe
  while the decay-0 work reached 1.82 / 1.41.

Sub-universe Sharpe is a check precisely because small universes are harder — expect the check
to fail more often as you go down in universe size. `[Platform]`

## Test Period

The Test Period feature splits the in-sample window into a training segment and a test segment
so you can see whether the alpha works outside the data you developed on. Choosing it does not
change the simulation; it changes how statistics and the PnL chart are displayed. The test
segment can be 0–5 years at the end of IS, and stats default to the training period until the
test period is shown. An alpha can only be submitted after the test period has been revealed.
`[Platform]`

Use it as a cheap overfitting check: a large gap between the train and test curves is your
warning, and it costs no extra simulation. `[Notes]`

## Delay

Delay 1 means you trade on data known at least one day earlier. Delay 0 uses same-day data and
is a different research surface with its own behaviour — among other things it is far more
sensitive to turnover. `[Platform]` The expert-level "D0" material is a separate topic in the
platform documentation; nothing here should be read as a D0 result. `[Notes]`

## Defaults used in this repository

```text
Instrument Type: Equity
Region: USA
Universe: TOP3000
Language: Fast Expression
Delay: 1
Neutralization: Subindustry (or Market for price/volume ideas)
Decay: 4
Truncation: 0.08
Pasteurization: On
Unit Handling: Verify
NaN Handling: Off
```

These are a starting point, not an optimum. Change one setting at a time, and only when you can
say why the change should help — see [Research workflow](06-research-workflow.md).

Next: [Fast Expression](03-fast-expression.md).
