# Advanced Topics

Material that assumes you are already comfortable with the basics: the mechanics of
neutralisation, correlation gates, multi-region and region-agnostic work, and systematic sweeps.

## Neutralisation mechanics

Neutralisation splits the cross-section into groups and subtracts the group mean from each value,
so the alpha expresses relative performance inside each group rather than a directional bet on
the group itself. The vector is then normalised and scaled to book size. `[Platform]`

```text
alpha = alpha - mean(alpha)      within each group
```

Three practical consequences:

- **Group size matters.** Every group needs enough instruments for the mean to be meaningful. In
  a 600-name universe, subindustry neutralisation leaves very few names per group; in a
  3,000-name universe the same grouping is comfortable. `[Hypothesis]`
- **Neutralisation affects the book, not just the signal.** Grouping choices change which
  instruments end up with the largest residual weights, which is why grouping and
  `CONCENTRATED_WEIGHT` failures are related. `[Observed]`
- **Do not neutralise twice.** If you use `group_neutralize` inside the expression, set the
  settings neutralisation to `None`, and set decay and truncation to 0, applying any smoothing
  inside the expression instead. `[Platform]`

## Decay and smoothing in detail

Decay is smoothing applied to the alpha before trading. When you raise decay you are making an
explicit statement that the signal's information persists for several days. When it does not,
raising decay removes signal and noise together.

The recorded evidence for that failure mode: a smoothed cash-flow-dispersion variant fell from
Sharpe 1.52 to 0.85 while turnover dropped to 11.8% — the smoothing removed more signal than
noise. `[Observed]`

Where to apply smoothing, in order of preference: `[Notes]`

1. The fastest-changing component only (typically a reversal or volume term).
2. The final composite, if several components are fast.
3. Settings decay, as an additional layer — not as a substitute for fixing the expression.

## Correlation: self and production

Similarity, not performance, is the constraint that is hardest to reason about, because it is
invisible in your own results. Two distinct gates exist: `[Platform]` `[Notes]`

| Gate | What it compares against | What it implies for research |
|---|---|---|
| Self-correlation | Alphas that already exist on the platform | A good alpha can be rejected for being unoriginal |
| Production-pool correlation (consultant-level) | The wider pool of production alphas | Passing self-correlation is not sufficient |

This has a direct design consequence: **diversification has to be built in from the idea stage,
not patched afterwards.** Changing a window length or reordering terms does not move correlation.
Four recorded experiments cleared the metrics and failed on self-correlation with values of 0.88
to 0.94, all sharing a quality/improvement-plus-reversal backbone. `[Observed]`

Practical diversification axes, distinct from "changing the expression": `[Platform]`

```text
Data category   (fundamentals, analyst estimates, sentiment, options, news, price/volume)
Time horizon    (overnight, days, weeks, months)
Mechanism       (value, revision, reversal, dispersion, volatility relationships)
Region          (the same idea is a different alpha in a different market)
```

## Multi-region and region-agnostic alphas

Region-agnostic ("RA"/global) alpha types and the parent-child relationship between global alphas
and their regional children are described in the platform's own documentation; the mechanics are
outside the scope of what this repository can verify, and program-specific requirements change
between seasons. What the recorded evidence supports is narrower but concrete: `[Observed]`

- **Global scope is judged per sub-region.** The GLB pages show checks for Asia/Japan, the
  Americas and EMEA separately, plus robust-universe variants.
- **Excellent regional performance is not evidence for global performance.** The recorded GLB
  blocks were the weakest in a 5,546-block bundle: best Sharpe 1.42, best Fitness 0.57.
- **The same field list behaves differently by region**, so a ported expression is a new
  experiment, not a reuse.

Any statement about current RA or competition requirements should be verified against the live
platform documentation, with its date noted. See
[Sources and evidence policy](15-sources-and-policy.md) for how this repository treats
time-sensitive program rules.

## Consultant-level gates (described, not reproduced)

Beyond the user-level thresholds, consultant submissions face additional gates: a
window-by-window consistency requirement across the in-sample period, a production-correlation
ceiling, and different criteria for single-dataset alphas. The recorded evidence shows these
checks firing in ordinary simulations — `IS_LADDER_SHARPE` in 96 of 174 USA blocks and
`CLUSTER_TEST` in 27 EUR blocks. `[Observed]`

**The specific thresholds for these gates are deliberately not reproduced in this wiki.** They
are consultant-program material that changes over time and is subject to program terms. The
platform's own documentation and your consultant program materials are the authoritative source.

What is safe and useful to carry over from the evidence: `[Observed]`

- The consistency ladder is a practical filter that ordinary simulations already expose, so you
  can see it before you reach submission.
- Passing the headline metrics is not the end of the process; the gates that stop strong alphas
  are consistency and correlation.
- A single-dataset alpha is a different shape from a composite, so "add another factor" is not
  automatically an improvement.

## Systematic sweeps: when they help and when they waste simulations

A sweep is many simulations in one batch. Sweeps are good at mapping a surface and bad at
producing a submittable alpha.

| Sweeps are good for | Sweeps are bad for |
|---|---|
| Checking whether a family has any signal at all | Polishing a single idea |
| Comparing neutralisations for one field | Finding the best expression, because nothing is tuned |
| Building a coverage map before committing effort | Producing alphas — 13,319 recorded sweep blocks produced 0 passes |

The counter-evidence is worth internalising: 4,223 EUR blocks, 3,550 USA blocks and 5,546
multi-region blocks produced zero passes, while the three experiments that cleared the checks were
small, deliberate iterations. `[Observed]`

Rules that make a sweep worth its budget: `[Notes]`

- Decide **in advance** what result would change your mind about a family.
- Vary one dimension at a time (field, or transform, or neutralisation — not all three).
- Read the failed-check distribution across the whole page before believing any single block.
- Keep the raw pasted text, so the sweep can be re-parsed later.
- Treat `PENDING` blocks as unmeasured.

## Where the ceiling actually is

The recorded picture, stated plainly: the raw-Sharpe ceiling in every explored region now sits
above 1.9, and the failures have moved to weight concentration, robustness, and the consistency
and correlation gates. Adding more signal is not the bottleneck. `[Observed]`

That is the single most useful strategic conclusion in this repository, and it is why
[Improving alphas](09-improving-alphas.md) puts construction fixes ahead of tuning.

Next: [Sources and evidence policy](15-sources-and-policy.md).
