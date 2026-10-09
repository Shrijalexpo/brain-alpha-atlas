# Foundations: How BRAIN Research Works

This page defines the vocabulary the rest of the wiki depends on. If you only read one page
before your first simulation, read this one.

## What an alpha is

An **alpha** is a rule that assigns a weight to every instrument each day, based on a
prediction of the next period's return: [Platform]

```text
positive weight  -> expected to outperform  (long)
negative weight  -> expected to underperform (short)
```

You never write the weights directly. You write an expression that produces a score per
instrument, and BRAIN converts those scores into portfolio weights through a fixed pipeline:
neutralisation, scaling to book size, and the position limits in your settings.

The practical consequence: **an alpha is a ranking device, not a prediction of return
magnitude.** Most of the time you care about which instruments get high scores relative to each
other, not the size of the number. That is why `rank`, `zscore`, `quantile` and `winsorize`
appear everywhere — they control the shape of the ranking without changing its order.
[Platform]

## The three things you control

| Layer | What you decide | Where it lives |
|---|---|---|
| **Idea** | Which economic relationship should predict returns | your head — the only part that cannot be automated |
| **Expression** | How that relationship is expressed with data fields and operators | Fast Expression |
| **Settings** | Region, universe, delay, decay, truncation, neutralisation, pasteurisation, NaN handling | Simulation Settings panel |

A common failure mode is treating the third layer as the search space: running hundreds of
setting combinations against a weak idea. Settings change how a signal is expressed and how
much it costs to trade; they rarely create signal that was not there. The recorded evidence in
this repository supports that: a EUR sweep that varied decay moved turnover substantially but
left Sharpe broadly unchanged `[Observed]`.

## The research loop

BRAIN describes research as a cycle: form an intuitive idea, implement it with available data
and operators, then optimise parameters and neutralisation to submit the alpha in its best
form. There are no fixed right answers — the repeatable skill is controlled experimentation.
`[Platform]`

Expanded into the concrete loop used throughout this repository: `[Notes]`

```text
1. Hypothesis      Write the economic reason in one sentence, before touching the simulator.
2. Field           Pick a field that can express it; check coverage and type.
3. Baseline        Write the simplest expression that tests the idea. Simulate it.
4. Diagnose        Read the stats AND the failed checks. Name the single binding constraint.
5. One change      Change exactly one mechanism. Simulate again.
6. Record          Save the result, the settings, and the lesson. Update the ledger.
7. Compare         Judge the variant against the baseline under identical settings.
8. Decide          Improve, abandon, or escalate to robustness and correlation work.
```

Step 3 is where most beginners lose time. The baseline should be small — a ratio, a rank, a
single time-series transform — because a small baseline tells you *which part* of a large idea
is carrying the signal. If a five-term composite works, you do not know why; if it fails, you
do not know which term to fix.

## Vocabulary you will meet immediately

| Term | Meaning |
|---|---|
| **Region** | The market you trade in, e.g. USA, EUR, ASI, CHN, KOR, AMR `[Platform]` |
| **Universe** | The set of instruments inside a region, e.g. TOP3000, TOP600, TOPCS1600 `[Platform]` |
| **Delay** | How many days after the data date you can trade. Delay 1 is the common consultant setting `[Platform]` |
| **Neutralization** | How the final scores are centred within groups before sizing `[Platform]` |
| **Decay** | Smoothing applied to the alpha before trading — the primary turnover control `[Platform]` |
| **Truncation** | A cap on the maximum weight any single instrument can take `[Platform]` |
| **Pasteurization** | Whether the platform restricts how much a single day's data can influence the book `[Platform]` |
| **In-sample (IS)** | The historical period the simulator measures on, roughly five years `[Platform]` |
| **Fast Expression** | The expression language you write alphas in `[Platform]` |
| **Sub-universe** | A smaller universe checked alongside yours, to test whether the alpha survives fewer names `[Platform]` |
| **Turnover** | Share of the book traded per day `[Platform]` |
| **Fitness** | A composite reward that penalises turnover: roughly `Sharpe × sqrt(|Returns|) / max(Turnover, 0.125)` `[Notes]` |
| **Self-correlation** | Similarity between your alpha and alphas that already exist — the main reason good alphas get rejected `[Platform]` |

## What "submittable" means

Passing the checks is a sequence, not a single score. An alpha can have a 2.6 Sharpe and still
be rejected — the record in this repository contains several examples `[Observed]`. The layers
are roughly:

```text
1. Expression validates        (syntax, types, units, field availability)
2. IS metrics clear thresholds (Sharpe, Fitness, turnover band)
3. Robustness checks clear     (sub-universe, recent-window, ladder checks)
4. Book quality checks clear   (weight concentration, turnover extremes)
5. Correlation gates clear     (self-correlation, then the production pool)
```

Layer 4 and 5 are where strong signals die. See [Failed checks](08-failed-checks.md) for what
each check means and how to respond, and [Advanced topics](14-advanced.md) for the
correlation gates.

## Why disciplined records matter

A research log is not bookkeeping. In a search space this large, the only way to know whether
an idea is new is to have written down what was already tried. This repository's
[experiment index](10-experiment-index.md) exists precisely so that an idea can be checked
before it costs simulations — and so that a failure teaches something beyond "it didn't work".

Two habits make the difference: `[Notes]`

- Record the **settings** with the result. A Sharpe without its region, universe, delay, decay
  and neutralisation is not a result, it is a number.
- Record **which check failed**, not just that the alpha failed. "Sharpe 1.5, Fitness 0.8,
  `LOW_FITNESS`" implies a different next step from "Sharpe 2.6, `CONCENTRATED_WEIGHT`".

Next: [Simulation settings](02-simulation-settings.md).
