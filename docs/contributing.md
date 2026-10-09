# Contributing

How to add an experiment, a lesson or a correction to this knowledge base — and how to do it
without publishing anything private or overstating a result.

## The two layers

This repository has a raw research layer and a curated documentation layer. They have different
jobs, and contributions should respect the split.

| Layer | Where | Rule |
|---|---|---|
| Raw research | `simulations/`, `Research/`, `Data/`, `Operators/`, `Troubleshooting/` | Preserve what was measured. Correct it explicitly; never silently rewrite a result |
| Curated wiki | `docs/` | Synthesise. Summarise in original language, cite the source, link to it |

If you learn something new, the wiki should reflect it. If you measured something new, the
evidence belongs in the research layer and the wiki links to it.

## Adding an experiment

1. **Create the record** in `simulations/`, using the template in
   [`simulations/simulation_template.md`](../simulations/simulation_template.md). Number it as the
   next in sequence.

2. **Fill in the settings, not just the metrics.** Region, universe, delay, decay, truncation,
   neutralisation, pasteurisation, NaN handling, test period. A result without its settings cannot
   be reproduced or compared.

3. **Quote the out-of-sample numbers.** If the platform reports both a training and an
   out-of-sample Sharpe, record both and label them. Never quote the training column as the
   result — in one recorded sweep the columns disagreed in 2,448 of 2,500 rows.

4. **Record which checks failed**, with the resolved check names (not the abbreviated `Fx`
   codes). The code-to-check mapping is per results page.

5. **Write the lesson.** One or two sentences: what this result tells the next researcher. "It
   didn't work" is not a lesson; "the signal survives peer-neutralisation but not the 2-year
   window" is.

6. **Update the ledger** in [`simulations/status_index.md`](../simulations/status_index.md) so the
   expression can never be re-proposed as new.

7. **Update the wiki** if the result changes a general lesson: add the row to the
   [experiment index](10-experiment-index.md) and, if a durable principle changed, to
   [Lessons](11-lessons.md). The index is assembled from the records, so copy the expression and
   metrics from the record you just wrote — never from memory — then run the two checks that
   prove it: `python3 Tools/check_docs.py` and `python3 Tools/verify_index.py` (see
   [Tools](13-tools-and-api.md)). The reconciliation step is not optional: it is what keeps the
   index from quietly disagreeing with the records it summarises.

### Statuses

Use exactly these, and do not upgrade a status you did not observe:

| Status | Use when |
|---|---|
| `PASSED_SUBMITTED` | Submission is documented |
| `PASSED_SUBMITTABLE` | The checks were cleared; no submission observed |
| `FAILED` | A required check failed, or the evidence rejects the candidate |
| `FAILED_SELF_CORRELATION` | Metrics acceptable, rejected for similarity |
| `ERROR` | The expression failed validation |
| `PENDING` | The platform had not finished evaluating it |

`PENDING` is not a near-pass. It is an absence of measurement.

## Adding a bulk sweep

```bash
# Keep the raw pasted page. This is the step that is usually skipped and cannot be recovered.
python3 Tools/brain_sweep_parser.py --selftest
python3 Tools/brain_sweep_parser.py SWEEP.txt --outdir simulations/sweeps --prefix <stem>_
```

- Store the raw text under `simulations/sweeps/sources/`.
- Use `--prefix` so the combined `all_results.csv` / `SUMMARY.md` cannot overwrite an earlier
  bundle's.
- Check the declared-vs-parsed block count before trusting the output; a mismatch means the page
  was truncated or the format changed.
- Summarise in the wiki by headline counts and best results, and link to the data — do not paste
  thousands of rows into Markdown.

## Documenting a failure

Failures are the most valuable entries in this repository, provided they are specific.

Good: *"Sharpe 2.61 / Fitness 1.88 fails `CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE`
identically at decay 4, 6 and 8, so the constraint is book construction, not smoothing."*

Weak: *"Disappointing."*

Also record **abandonment**: which family is exhausted and why. That is what stops the next
researcher repeating it.

## Citing sources

Tag non-obvious claims in the wiki:

```text
[Platform]   official platform documentation or behaviour (note the capture date)
[Notes]      this repository's own notes
[Observed]   measured in a recorded simulation (link the record)
[Hypothesis] an interpretation that is not verified
[External]   published paper or third-party source
```

Use relative links to material actually included in this repository. For official documentation,
give the topic name and the capture date; keep the platform as the authoritative reference. If two
sources conflict, record the conflict and compare dates and authority rather than silently choosing
one.

## Protecting private data

Before committing anything, check for and remove:

- Credentials, tokens, cookies, authorisation headers, session identifiers.
- Account identifiers, usernames, email addresses — including those that sneak in via copied UI
  text or log output.
- Absolute local paths (`/Users/...`, `C:\Users\...`) and machine-specific configuration.
- Notebook outputs: clear them. Outputs can embed tokens, plotly bundles, account artefacts and
  megabytes of noise.
- Captured platform pages: these carry the capturing account's header and are third-party text.
- Contracts, agreements, competition terms and program-specific instructions.

`.gitignore` excludes the known-sensitive paths, but ignoring is not erasing: if something private
was ever committed, remove it from history and rotate the credential rather than assuming the
ignore rule is enough.

## Writing style

- Plain, specific, professional English. Explain a term before relying on it.
- Prefer a short page with an actionable lesson over a long page repeating raw data.
- Do not duplicate an explanation — link to the canonical page instead.
- Keep warnings visible.
- Never claim a result is guaranteed, and never imply compensation.

## Before you finish

```text
[ ] Record created and numbered; settings captured
[ ] Out-of-sample numbers labelled correctly
[ ] Failed checks recorded by resolved name
[ ] Ledger row added
[ ] Wiki lesson/ index updated if the lesson is general
[ ] No credentials, identifiers, absolute paths or notebook outputs added
[ ] Parser self-test still passes, if you touched tooling
[ ] python3 Tools/check_docs.py exits zero
[ ] python3 Tools/verify_index.py exits zero
[ ] If a sweep moved a PASS/PENDING tally, the index row was updated to match
```

## What CI runs on the change

Every pull request runs the same checks that are available to you locally: the tool self-tests,
Markdown hygiene, index reconciliation, a strict documentation build, and a scan of the built
site for excluded material (see [Tools](13-tools-and-api.md)). Finding a fixable failure locally
is faster than reading it in the Actions log.

## Repository layout conventions

| Content | Goes to |
|---|---|
| Simulation result | `simulations/` |
| Suggested but unrun idea | `AlphaQueue/` |
| Data field or dataset note | `Data/` |
| Tutorial or platform note | `tutorials/` |
| Error or warning | `Troubleshooting/` |
| Durable research rule (the public home for it) | [`11-lessons.md`](11-lessons.md) |
| Operator capture or reference | `Operators/` |
| Reusable script | `Tools/` |
| Curated explanation | `docs/` |

Personal working files — `instructions.md`, `CLAUDE.md`, and the consultant-program notes they
reference — are deliberately **not** part of this repository; `.gitignore` keeps them local. Do not
link to them from a page that is published, because a reader on GitHub will not find them. Their
durable, general rules belong in [Lessons](11-lessons.md) instead.
