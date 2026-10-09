# BRAIN Alpha Atlas

An open knowledge base for **WorldQuant BRAIN alpha research**: how the platform works, how to
design and simulate alphas, how to read the numbers, why submissions get rejected — and what
71 recorded experiments actually taught us.

Built for new BRAIN users who want a path from "I can open the simulator" to "I know how to
research an idea", and for experienced researchers who want a specific answer fast.

**Start here → [`docs/index.md`](docs/index.md)**

## What is in here

| | |
|---|---|
| **[Foundations](docs/01-foundations.md)** | Alpha, universe, neutralisation, Fitness — the vocabulary, defined before it is used |
| **[Simulation settings](docs/02-simulation-settings.md)** | Every setting, and what the recorded evidence says it does |
| **[Fast Expression](docs/03-fast-expression.md)** | Syntax rules, normalisation patterns, and an error catalogue |
| **[Operators](docs/04-operators.md)** | Operators by family, with practical rules and failure modes |
| **[Data and fields](docs/05-data-and-fields.md)** | Field inspection protocol and family-by-family recorded outcomes |
| **[Research workflow](docs/06-research-workflow.md)** | The disciplined loop: hypothesis → baseline → one change → record |
| **[Evaluating results](docs/07-evaluating-results.md)** | Reading Sharpe, Fitness, Turnover and the PnL shape together |
| **[Failed checks](docs/08-failed-checks.md)** | Every check that appears in the record: meaning, causes, fixes, when to stop |
| **[Improving alphas](docs/09-improving-alphas.md)** | The repair catalogue, in priority order |
| **[Experiment index](docs/10-experiment-index.md)** | All 71 experiments with settings, metrics and the lesson recorded |
| **[Lessons](docs/11-lessons.md)** | Durable findings, every one traceable to evidence |
| **[Regions and universes](docs/12-regions-and-universes.md)** | Per-region evidence and what transfers between scopes |
| **[Tools](docs/13-tools-and-api.md)** | The sweep parser, the validators, the docs checker, the index reconciler, and safe credential practice |
| **[Advanced topics](docs/14-advanced.md)** | Neutralisation mechanics, correlation, multi-region, sweeps |
| **[Sources and policy](docs/15-sources-and-policy.md)** | Evidence tags, citation rules, what is withheld and why |
| **[Contributing](docs/contributing.md)** | How to add an experiment without publishing anything private |

## The beginner path

If you are new, read in this order — roughly two hours:

```text
docs/01-foundations.md          what you are building
docs/02-simulation-settings.md  the knobs
docs/03-fast-expression.md      how to write it
docs/06-research-workflow.md    how to iterate
docs/07-evaluating-results.md   how to read the outcome
docs/08-failed-checks.md        why it gets rejected
```

Then read [`docs/10-experiment-index.md`](docs/10-experiment-index.md) before your second week —
the fastest way to avoid re-running someone else's dead end.

## Why this knowledge base exists

Alpha research is easy to do badly and hard to do systematically. The failure modes are specific
and repeatable: testing settings instead of ideas, stacking similar factors, smoothing a signal
until it disappears, quoting a training number as a result, or spending a hundred simulations
rediscovering a family that was already exhausted.

This repository is an attempt to make those mistakes visible *before* they are made. Its value is
less in the answers than in the record: every experiment is stored with its settings, its metrics,
the checks it failed, and the lesson learned — including the ones that failed, which are the
majority.

## The research record in numbers

| | |
|---|---|
| Recorded experiments | 71 |
| Cleared the platform checks | 3 |
| Submitted | 2 |
| Rejected for self-correlation after passing the metrics | 4 |
| Bulk sweep blocks simulated | 13,319 |
| Projects produced by those sweep blocks | 0 |

The last two rows are the single most useful fact in this repository. Sweeps map a surface; they
do not produce submittable alphas. The two submissions came from small, deliberate iterations.

## Evidence and source policy

Nothing here is asserted from memory. Claims are tagged by source:

| Tag | Meaning |
|---|---|
| `[Platform]` | Official BRAIN documentation or platform behaviour, with a capture date |
| `[Notes]` | This repository's own research notes |
| `[Observed]` | Measured in a simulation whose record is committed here |
| `[Hypothesis]` | A plausible interpretation, not verified |
| `[External]` | Published paper or third-party source |

Material that should not be published — personal agreements, third-party documentation captures,
copyrighted papers, consultant-scoped material, credentials and account data — is excluded and
documented without reproducing its contents. See
[Sources and evidence policy](docs/15-sources-and-policy.md).

## Limitations, stated plainly

- **Historical backtest results do not guarantee future performance.** Every number here describes
  a period under specific settings.
- **Platform rules, thresholds and competition requirements change.** Where a threshold is quoted,
  it is a working reference with a date; the live platform is authoritative.
- **Results are scope-specific.** A result in one region, universe or delay is not evidence for
  another until it is tested there.
- **The record is uneven.** USA and EUR are well covered; other regions are thin or absent.
- **Nothing here is investment advice**, and no statement in this repository implies any level of
  compensation or success.

## Contributing

Add experiments, sweeps, corrections or lessons by following
[`docs/contributing.md`](docs/contributing.md). The short version: record the settings, quote the
out-of-sample numbers, name the failed checks, state the lesson, and never commit credentials,
account identifiers, absolute local paths or uncleared notebook outputs.

## Repository layout

```text
docs/            Curated knowledge base (start at docs/index.md)
simulations/     One record per experiment, plus parsed sweep data
Research/        Workflow notes, neutralisation guidance, accumulated lessons
Data/            Dataset and field research notes
Operators/       Curated operator reference and Fast Expression cheat sheet
Troubleshooting/ Errors, warnings and fixes
Tools/           Dependency-free validation and parsing scripts
tutorials/       Platform tutorial notes
```

## Licence and use

The repository is licensed in two parts: the tooling under **MIT** ([`LICENSE`](LICENSE)) and the
documentation and research prose under **CC BY 4.0** ([`LICENSE-DOCS`](LICENSE-DOCS)), which allows
reuse with attribution. [`NOTICE`](NOTICE) records what neither grant covers: raw pasted platform
result pages, platform documentation and terminology, and any cited third-party work, all of which
remain the property of their owners. BRAIN Alpha Atlas is independent and is not affiliated with or
endorsed by WorldQuant.

Licensing aside, treat the content as evidence rather than instruction: the recorded metrics are
one user's backtests under stated settings. Verify anything important against the live platform
before relying on it.
