# Evaluating Results

The simulator returns a small set of numbers and a list of checks. This page explains what each
one measures, how they interact, and which ones actually decide the outcome.

## The metrics

| Metric | What it measures | How to read it |
|---|---|---|
| **Sharpe** | Return per unit of risk (volatility of the alpha's PnL) | The headline quality number. Higher is better, but it is not sufficient |
| **Fitness** | A composite that rewards returns and penalises turnover | The metric that fails most often when a signal is slow but weak |
| **Turnover** | Share of the book traded per day | The cost driver; the band that matters is roughly 1%–70% `[Platform]` |
| **Returns** | Annualised profitability | Feeds Fitness; very low returns cap Fitness regardless of Sharpe |
| **Drawdown** | Worst peak-to-trough loss over the period | A risk-shape measure. Compare against returns: returns/drawdown above 1 is healthier |
| **Margin** | Profit per unit of trading | Low margin means the alpha is working for the broker, not for you |
| **Sub-universe Sharpe** | The same alpha measured on a smaller universe | A robustness proxy; failing it means the signal depends on the long tail of names |
| **Train Sharpe** | Sharpe on the training segment only | Diagnostic — never quote it as the result |
| **Self-correlation** | Similarity to alphas that already exist | The gate that rejects good alphas for being unoriginal |

Sharpes and Fitness in this repository are out-of-sample (the `Sharpe` column) unless explicitly
labelled `Train Sharpe`. `[Notes]`

## Fitness, concretely

Fitness combines quality with the cost of achieving it:

```text
Fitness ≈ Sharpe × sqrt(|Returns|) / max(Turnover, 0.125)      [Notes]
```

Two consequences follow directly from that formula, and they explain a large share of the
failures in this repository:

- **High turnover divides Fitness down.** A Sharpe of 1.78 with 57.5% turnover produced Fitness
  0.67 in a recorded experiment — the signal was real, the trading cost was not affordable.
  `[Observed]`
- **Low returns multiply Fitness down.** A Sharpe of 1.16 at 13.12% turnover produced Fitness
  0.78. Smoothing the signal further would have lowered Sharpe without fixing the real problem,
  which was that the returns were too small. `[Observed]`

The `max(Turnover, 0.125)` term means very low turnover stops being rewarded at some point —
there is no prize for an alpha that never trades.

## Working reference thresholds

| Check | Working reference | Source |
|---|---|---|
| Sharpe | above 1.25 | `[Platform]` captured documentation |
| Fitness | above 1.0 | `[Platform]` captured documentation |
| Turnover | between 1% and 70% | `[Platform]` captured documentation |

Treat these as orientation, not law: they are thresholds captured on a date, they differ by
region in practice, and the live check list shown with your simulation is authoritative. The
recorded evidence makes the regional variation concrete — AMR/TOP600 blocks with Sharpe 1.4–1.6
still failed `LOW_SHARPE`, while some USA blocks at similar Sharpe cleared it. `[Observed]`

## Reading the PnL chart

The shape matters as much as the number. What to look for: `[Platform]`

- A curve that **rises steadily** with few severe drops is the healthy pattern.
- **One dominant jump** near the start usually means the alpha is capturing a single episode,
  not a repeatable relationship.
- **Large fluctuations** and deep drawdowns are warnings that the Sharpe is being earned in a
  few windows.
- A **flat curve with no drawdown** can be a red flag rather than a good sign: it may indicate a
  degenerate book. A recorded EUR block showed exactly that shape — 100% turnover, zero
  drawdown, 12 long against 218 short, and a train Sharpe of 0.00. `[Observed]`

## The numbers interact — read them as a set

| Pattern | Reading |
|---|---|
| Sharpe ok, Fitness ok, turnover 1–70% | Clear the metrics; check robustness next |
| High Sharpe, low Fitness, high turnover | Good signal with unaffordable trading — smooth or raise decay |
| High Sharpe, low Fitness, low turnover | Weak returns per unit of risk — strengthen the signal carefully |
| Low Sharpe, low turnover | Weak signal; settings will not rescue it |
| Sharpe ok, low margin | Profitable only because of scale — fragile |
| Sharpe ok, high returns, high drawdown | Aggressive exposure; check concentration and the sub-universe |

## Robustness before enthusiasm

Metrics alone never make an alpha submittable. The recorded record contains several blocks with
excellent headline numbers that were stopped by a robustness clip: a KOR block at Sharpe 2.36 /
Fitness 1.67 failed only `LOW_2Y_SHARPE`; a EUR block at Sharpe 2.63 / Fitness 1.24 failed
`LOW_SUB_UNIVERSE_SHARPE` and `LOW_2Y_SHARPE`. `[Observed]`

So the honest reading of a strong result is: *"this signal worked on the full period; now let me
find out whether it worked in the recent window and on fewer names."* That is a different
question from "is the number big enough", and it is the one that decides submissions.

## Train versus test

Use the Test Period feature to split in-sample into a training segment and a test segment.
Statistics default to the training period until the test period is revealed, and submission
requires it to be revealed. `[Platform]`

What to look for: `[Notes]`

- **A large gap** between train and test means the alpha was fitted to the development window.
- **A test curve better than train** is not automatically good news; it can mean the recent
  regime happened to suit the signal, which is a robustness question, not a quality signal.
- In the recorded USA sweep the two columns disagreed in both directions and systematically:
  the training column was higher in 2,448 of 2,500 blocks, while in another page a block showed
  0.96 train against 1.23 out-of-sample. `[Observed]`

## A checklist for reading any result

```text
[ ] Am I reading out-of-sample Sharpe, not Train Sharpe?
[ ] Is turnover inside 1-70%, and is it inside the range Fitness rewards?
[ ] Does the PnL curve rise steadily, or is it one episode?
[ ] Which single check is failing?
[ ] Does that failure point at signal, cost, or book geometry?
[ ] Would the suggested fix change the signal, or only its expression?
```

Next: [Failed checks](08-failed-checks.md).
