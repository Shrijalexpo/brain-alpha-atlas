# Sources and Evidence Policy

How to know where a claim in this wiki came from, how to cite, and what was deliberately left out
of the public documentation.

## Source categories

Every non-obvious claim is tagged inline. The tags are:

| Tag | Meaning | Trust |
|---|---|---|
| `[Platform]` | Official WorldQuant BRAIN documentation or observed platform behaviour, captured on a stated date | Authoritative for its date; verify current rules live |
| `[Notes]` | This repository's own research notes and workflow decisions | Opinionated but consistent; not authority |
| `[Observed]` | Measured in a simulation whose record is in [`simulations/`](../simulations/) | Evidence about a period, under stated settings only |
| `[Hypothesis]` | A plausible interpretation that has **not** been verified | Treat as a lead, never as a fact |
| `[External]` | Published paper or third-party source | Citable, but not a platform rule |

If a statement has no tag, it is either a definition from the platform documentation or a
straightforward consequence of one.

## Rules this wiki follows

1. **No invented operator definitions, field semantics, platform rules or performance claims.**
   Operator and metric descriptions trace to the platform reference; field behaviour traces to
   recorded experiments.
2. **No fabricated success.** Neither the repository nor this wiki makes claims about submission
   outcomes beyond what was actually observed, and none about compensation.
3. **Results carry their settings.** A number is quoted with its region, universe and parameters,
   or it is marked as incomplete.
4. **Observed, hypothesised and recommended are kept separate.** A next step is labelled as a
   recommendation, not as a known fix.
5. **Comparability is respected.** Results from different regions, universes, delays or
   parameter configurations are not averaged or presented as directly comparable.
6. **Time-sensitive rules carry dates.** Competition and program specifics are treated as
   historical captures, never as statements about the present.

## Where the evidence lives

| Evidence | Location |
|---|---|
| Individual experiment records | [`simulations/`](../simulations/) — one file per experiment |
| Duplicate-avoidance ledger and repair targets | [`simulations/status_index.md`](../simulations/status_index.md) |
| Bulk sweep data and per-page reports | [`simulations/sweeps/`](../simulations/sweeps/) |
| Raw pasted sweep text (re-parseable) | [`simulations/sweeps/sources/`](../simulations/sweeps/sources/) |
| Superseded / corrected artefacts | [`simulations/sweeps/superseded/`](../simulations/sweeps/superseded/) |
| Accumulated lessons | [`Research/lessons_from_simulations.md`](../Research/lessons_from_simulations.md) |
| Field-family notes | [`Data/datasets_and_fields.md`](../Data/datasets_and_fields.md) |
| Error catalogue | [`Troubleshooting/brain_errors_and_fixes.md`](../Troubleshooting/brain_errors_and_fixes.md) |

## How to cite

Within the wiki, link to the page. For an experiment, link to its record and quote its settings:

```text
Sharpe 2.36 / Fitness 1.67, USA-equivalent KOR TOP600, INDUSTRY, decay 5, truncation 0.08.
Failed LOW_2Y_SHARPE only.
Source: simulations/071_multi_region_bundle_20261009.md
```

For a platform rule, cite the captured documentation topic, not a summarising page:

```text
Source: BRAIN Learn > Documentation > (topic), captured <date>.
```

Links are relative and point only at material included in this repository. No link points at a
source document that was withheld from the public build.

## Handling disagreements between sources

Where two sources conflict, the conflict is recorded rather than silently resolved. Compare by
authority and date: platform documentation outranks research notes, a newer capture outranks an
older one, and a measured result outranks an expectation. Two conflicts worth knowing about
already exist in this repository: `[Notes]`

- **Neutralisation guidance vs measured results.** Captured platform guidance suggests broad
  groups for price/volume and option datasets; the recorded AMR work found narrow (subindustry)
  grouping best for model and analyst families in a 600-name universe. Both are recorded; the
  measured result is one universe and one family.
- **Decay's importance.** Captured guidance lists decay as a primary improvement lever; the
  recorded sweeps show it moving turnover substantially while leaving Sharpe broadly unchanged.
  Not a contradiction — decay is a turnover lever, and turnover matters through Fitness.

## What was deliberately excluded from the public build

This repository was reviewed before publication, file by file. The categories below were withheld
from the public documentation layer. Their contents are **not** summarised here beyond the reason,
and they are excluded from version control:

| Category | Why it is excluded |
|---|---|
| Personal consulting agreements and contracts | Confidential, personally identifying, and not ours to publish |
| Competition terms and legal documents | Third-party legal text; governed by their own terms |
| Consultant-program instructions and program-specific thresholds | Consultant-scoped material, subject to program terms; changes over time |
| Verbatim captures of official platform documentation | Third-party copyrighted text; the wiki summarises in original language and points to the platform instead |
| Captured operator lists in raw form | Same reason as above, plus they contained the capturing account's UI header |
| Third-party papers, books and formula collections | Copyright status is not ours to determine; cite and link instead |
| Platform automation library and notebooks | Contain a credential-handling flow and account artefacts; unsafe to redistribute, and the platform terms govern automation |
| Editor and agent state directories, caches, compiled files | Machine-specific noise, and in some cases session logs |
| Local absolute paths and account identifiers | Machine-specific and personally identifying; anonymised wherever they appeared in publications |
| Personal working files (`instructions.md`, `CLAUDE.md`) | Working preferences rather than research; the durable general rules they produce are republished in [Lessons](11-lessons.md). Kept local by `.gitignore` |

A full per-file review, including the reasoning per item and the remaining decisions that only the
repository owner can make, is kept in a private audit note that is **not** part of the public
documentation.

## Licensing

The public repository is licensed in two parts: **MIT** for the tooling
([`LICENSE`](../LICENSE)) and **CC BY 4.0** for the documentation and research prose
([`LICENSE-DOCS`](../LICENSE-DOCS)), with [`NOTICE`](../NOTICE) stating what neither grant covers —
raw pasted platform result pages, platform material and cited third-party work. That split is
deliberate: the scripts are meant to be lifted and reused, while the prose deserves attribution.
`[Notes]`

## Known gaps and unresolved questions

Stated plainly, so nobody mistakes absence for agreement:

- **Region coverage is thin outside USA and EUR.** CHN, JPN, ASI, IND and HKG/TWN appear in the
  platform documentation but have no meaningful recorded experiments here.
- **Per-region threshold values are not reproduced.** The evidence shows thresholds differ by
  region; the authoritative numbers are the live checks on your own simulation.
- **The consultant-level gates are described structurally, not numerically**, for the reasons in
  the table above.
- **Some recorded blocks remain unverified** because they were still computing when captured
  (42 of 5,546 in the most recent bundle). They are marked `PENDING` throughout.
- **One corrected-incident is preserved deliberately**: an earlier sweep summary contained a
  training-column-to-Sharpe mix-up that inflated a headline number. It is documented in
  [`simulations/sweeps/superseded/README.md`](../simulations/sweeps/superseded/README.md) because
  the failure mode is instructive, and every affected conclusion has been corrected.
- **Nothing here is investment advice**, and historical backtest results do not guarantee future
  performance.

Back to the [index](index.md).
