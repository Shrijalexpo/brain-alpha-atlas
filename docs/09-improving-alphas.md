# Improving Alphas

A repair catalogue, ordered by how often each problem shows up in the recorded work.

The first question is always the same: **which single check is failing?** Different failures need
opposite actions, and applying the wrong fix wastes simulations. See
[Failed checks](08-failed-checks.md) for the diagnosis and this page for the treatment.

## Priority order

```text
1. Fix the idea before the expression    (weak signal)
2. Fix the cost before the signal        (high turnover)
3. Fix the book before the decay         (concentration)
4. Fix the robustness question honestly  (universe, recent window)
5. Fix originality, not cosmetics        (self-correlation)
```

## 1. Weak signal: Sharpe below the bar

| Move | Detail |
|---|---|
| Change the economic idea | The most effective and least popular fix |
| Add a denominator | Raw levels are size signals; ratios are signals about the business |
| Change the normalisation | Cross-sectional rank vs the instrument's own history are different hypotheses |
| Change the field within the family | Prefer confirmed slow-level fields over short estimate changes |
| Check the direction | Question whether high should be long |

Do **not**: raise decay, add `` operators, or stack more factors. The recorded failure pattern is
unmistakable — a weak base signal produced Sharpe 0.46 with 3.98% turnover, and repeated attempts
to rescue weak branches by stacking similar quality/value factors made results worse, including a
large composite at −0.28 and a multiplicative interaction at −1.01. `[Observed]`

A stronger pattern, also recorded: changing the *transform* on the same field moved results more
than changing settings. Slow analyst level fields responded to `ts_scale(x, 63)` and
`ts_quantile(x, 63)` where plain `rank(ts_backfill(x, 21))` did not. `[Observed]`

## 2. High turnover / low Fitness from trading cost

This is the most common failure in the recorded data. Attack the fastest component first.

| Technique | Where it goes | Notes |
|---|---|---|
| Higher Decay | settings | Cheapest first move; raises turnover cost explicitly |
| `ts_mean(x, d)` | on the fastest term | Smooths the noisiest input |
| `ts_decay_linear(x, d)` | on the signal or a component | Shape-controlled smoothing |
| `hump(x, hump=0.01)` | on the signal | Limits the size and number of changes |
| `trade_when(condition, alpha, exit)` | around the alpha | Trades only when a condition holds |

Evidence for the approach: smoothing a reversal component with `ts_mean(-returns, 5)` is what
moved an alpha's Fitness from just under the bar to 1.02 and made it submittable. `[Observed]`

Evidence for the limit of the approach: over-smoothing killed a signal outright — a smoothed
cash-flow-dispersion variant dropped from Sharpe 1.52 to 0.85 while turnover fell to 11.8%,
meaning the smoothing removed the signal rather than its noise. `[Observed]` Smooth the fastest
component, not the whole alpha, and re-check Sharpe after each step.

## 3. Concentration and sub-universe failures

These two usually travel together, and they are **not** fixed by decay. Both failed identically
at decay 4, 6 and 8 in the USA implied-volatility family. `[Observed]`

| Move | Detail |
|---|---|
| Rank or winsorise the final signal | Removes the extreme values that create outsized weights |
| Widen the universe | More names per group means fewer extreme residuals |
| Re-examine the grouping | Very small groups concentrate the book; larger groups dilute it |
| Truncation | Caps any single weight (0.08 in all recorded work) |
| Improve coverage | NaNs shrink the tradeable set and distort weights |
| Change the neutralisation level | Subindustry vs industry vs size bucket changes who is compared with whom |

A concrete diagnosis from the record: the best-performers in the bundle had long/short counts near
balance (1,903 vs 1,218 on a 3,000-name universe), while the degenerate blocks were wildly
asymmetric (12 vs 218). `[Observed]` Check the counts early — they are the cheapest concentration
signal available.

## 4. Robustness: sub-universe, recent-window and ladder checks

| Failure | Honest interpretation | Reasonable next step |
|---|---|---|
| `LOW_SUB_UNIVERSE_SHARPE` | The edge may live in names you cannot trade at size | Test on the smaller universe directly; check tail dependence |
| `LOW_2Y_SHARPE` | The relationship may have decayed, or be regime-dependent | Question currency of the idea; do not chase it with settings |
| `IS_LADDER_SHARPE` | Performance concentrated in some windows | Accept it as regime-dependent, or find a more stable construction |

Do not treat robustness failures as tuning problems. In the recorded data, the block that cleared
everything except `LOW_2Y_SHARPE` was already at Sharpe 2.36 and Fitness 1.67 — there was no
"more signal" left to add, and the gap was structural. `[Observed]`

## 5. Self-correlation: originality, not cosmetics

`FAILED_SELF_CORRELATION` means the metrics were acceptable and the alpha was rejected for
similarity. Four recorded experiments failed this way, with self-correlations of 0.88 to 0.94,
all sharing a quality/improvement-plus-reversal backbone. `[Observed]`

What works: changing the economic backbone — a different data category, a different horizon, a
different mechanism. What does not work: changing a window length, reordering terms, or renaming
anything. Tiny variants of an existing alpha stay correlated, and the platform also checks the
production pool, so "different from my own alphas" is not sufficient. `[Notes]`

## Overfitting: the failure that looks like success

The signature is a good training period and a poor test period, or a delicate expression that
only works with specific coefficients.

Countermeasures: `[Platform]` `[Notes]`

- Use the Test Period to see train and test separately before believing a result.
- Prefer simple expressions: fewer terms, fewer tuned constants.
- Be suspicious of coefficients that must be small to avoid hurting the result.
- Do not tune a threshold until the metric clears the bar; that is fitting the check, not the
  market.
- Compare against the train-versus-out-of-sample gap, not just the headline number.

A recorded, quantified warning: across the USA sweep the training and out-of-sample Sharpe
columns disagreed in 2,448 of 2,500 blocks, with the training column systematically higher — by
up to 0.29 on a headline block. `[Observed]` A workflow that reads only one column is measuring
something other than what the platform will evaluate.

## What "improvement" should look like

Each iteration should leave you able to say:

```text
What changed:      one mechanism, named
What was expected: the direction of the effect, and on which metric
What happened:     the recorded numbers
Why:               the best explanation, marked as hypothesis if it is one
Next:              the single next change
```

If an iteration cannot answer those, it was a random draw rather than an experiment — and the
[experiment index](10-experiment-index.md) is the record that stops the same draw being made twice.

Next: [Experiment index](10-experiment-index.md) · [Lessons](11-lessons.md).
