# WorldQuant BRAIN Alpha Research — Knowledge Base

A practical, evidence-linked guide to researching alphas on the WorldQuant BRAIN platform:
how the platform works, how to write valid expressions, how simulation settings change results,
how to read the checks that decide whether an alpha is submittable, and what a long record of
real experiments actually taught us.

## Who this is for

- **New BRAIN users** who can open the simulator but do not yet know how to move from a data
  field to a defensible alpha.
- **Experienced researchers** who want a specific answer fast: which check is failing, which
  operator fixes turnover, which field families have already been exhausted.

You do not need prior quant finance experience. Every technical term is introduced before it is
used, and concrete examples are taken from the experiments recorded in this repository.

## What you will learn

1. How the BRAIN research loop works, from hypothesis to submission.
2. How to pick a data field and write a testable economic hypothesis around it.
3. How to write correct Fast Expression, and the mistakes that make an expression fail.
4. What each simulation setting does, and which ones actually move the numbers.
5. How to read Sharpe, Fitness, Turnover, Returns, Drawdown and Margin together.
6. What every failed submission check means and what to do about it.
7. How to improve a weak alpha without overfitting it.
8. Which research directions have already been explored here — and which look exhausted.

## Learning path for a new consultant

Read these in order. Each page stands alone, but this sequence builds up without gaps.

| Step | Page | Why this order |
|---:|---|---|
| 1 | [Foundations](01-foundations.md) | Vocabulary and the shape of the research loop |
| 2 | [Simulation settings](02-simulation-settings.md) | The knobs you set before you can run anything |
| 3 | [Fast Expression](03-fast-expression.md) | How to write an expression that validates |
| 4 | [Operators](04-operators.md) | The transformations you will actually use |
| 5 | [Data and fields](05-data-and-fields.md) | Choosing the input — the highest-leverage decision |
| 6 | [Research workflow](06-research-workflow.md) | The disciplined loop, step by step |
| 7 | [Evaluating results](07-evaluating-results.md) | Reading the numbers correctly |
| 8 | [Failed checks](08-failed-checks.md) | Why submissions get rejected, and what to change |
| 9 | [Improving alphas](09-improving-alphas.md) | The repair strategies, in priority order |
| 10 | [Experiment index](10-experiment-index.md) | What has already been tried here |

## Navigate by question

| If you are asking… | Go to |
|---|---|
| What does `ts_backfill` actually do? | [Operators](04-operators.md) |
| Why is my Turnover 80%? | [Improving alphas](09-improving-alphas.md) · [Failed checks](08-failed-checks.md) |
| What is a good Fitness? | [Evaluating results](07-evaluating-results.md) |
| Why did `LOW_2Y_SHARPE` fail when Sharpe is 2.4? | [Failed checks](08-failed-checks.md) |
| Which neutralization for analyst data? | [Simulation settings](02-simulation-settings.md) · [Regions and universes](12-regions-and-universes.md) |
| Why did my `ts_delta` on an estimate field error out? | [Fast Expression](03-fast-expression.md) · [Failed checks](08-failed-checks.md) |
| Has anyone already tried this idea? | [Experiment index](10-experiment-index.md) · [Lessons](11-lessons.md) |
| How do I run a 2,500-block sweep and parse it? | [Tools and API](13-tools-and-api.md) |
| What is the difference between ALL and a single region? | [Regions and universes](12-regions-and-universes.md) · [Advanced topics](14-advanced.md) |

## Evidence policy

Numbers in this knowledge base come from recorded experiments, not from memory. Every
non-obvious claim is tagged with where it came from:

| Tag | Meaning |
|---|---|
| `[Platform]` | Official BRAIN documentation or platform behaviour |
| `[Notes]` | A research note recorded in this repository |
| `[Observed]` | Measured in a simulation recorded in [`simulations/`](../simulations/) |
| `[Hypothesis]` | An interpretation that is plausible but **not** verified |
| `[External]` | Published paper or third-party source |

Two rules follow from this, and they matter more than any single page:

- **A backtest is evidence about a period, not a guarantee.** A Sharpe of 2.6 in a recorded
  simulation says the signal worked on that data under those settings. It says nothing about
  the future.
- **Platform thresholds and rules change.** Where a number is quoted as a threshold, it is
  marked as a working reference captured on a date, and the live platform always wins.

Full provenance, citation rules and the list of source material deliberately *not* reproduced
here: [Sources and evidence policy](15-sources-and-policy.md).

## The repository around this wiki

This documentation is a curated layer over a working research repository. The wiki explains and
synthesises; the raw material stays where it is and is linked from here.

| Folder | What it holds |
|---|---|
| [`simulations/`](../simulations/) | One record per experiment, plus the sweep data |
| [`Research/`](../Research/) | Workflow notes, neutralization guidance, accumulated lessons |
| [`Data/`](../Data/) | Dataset and field notes |
| [`Operators/`](../Operators/) | Curated operator reference and cheat sheet |
| [`Troubleshooting/`](../Troubleshooting/) | Error messages and their fixes |
| [`Tools/`](../Tools/) | Validation and parsing scripts (dependency-free) |

## Limitations

- Nothing here guarantees a submission, a payout, or any level of compensation. The platform
  decides; this wiki only helps you experiment better.
- Thresholds described as "passing" are working references. The authoritative source is the
  check list shown with your own simulation.
- Results are region-, universe- and parameter-specific. A result in one region is not
  evidence for another until it is tested there.
- The research record in this repository is mostly USA and EUR. Conclusions about other regions
  are marked as thin evidence where they exist at all.

## Contributing

Add experiments with the [contribution guide](contributing.md): record the settings, quote the
out-of-sample numbers, state the lesson, and never publish credentials or private data.
