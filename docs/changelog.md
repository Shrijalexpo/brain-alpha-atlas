# Change Log

## 2026-10-09 — Licence, local-only files, and first publication

### Added

| File | Purpose |
|---|---|
| [`LICENSE`](../LICENSE) | MIT, covering `Tools/*.py`, the workflows, `mkdocs.yml` and `requirements-docs.txt` |
| [`LICENSE-DOCS`](../LICENSE-DOCS) | CC BY 4.0, covering the documentation and research prose |
| [`NOTICE`](../NOTICE) | What neither licence covers: raw pasted platform result pages, platform material, cited third-party work |

### Kept local, not published

Four files were reviewed before the first push and deliberately excluded, because they restate
material the platform's own program terms govern and this wiki's [evidence
policy](15-sources-and-policy.md) does not redistribute:

```text
CLAUDE.md                                             agent working preferences
instructions.md                                       personal research rules
 tutorials/consultant_program_osmosis_allocation_guide.md   program mechanics
tutorials/spc_2026_prompt_competition.md              competition rules
```

`.gitignore` keeps them on the authoring machine, and three published files were annotated so a
reader is not sent looking for them: `Commands.md`, `Research/iteration_workflow.md` and
`tutorials/worldquant_brain_documentation_index.md`. Their durable, general rules already live in
[Lessons](11-lessons.md) and [Tools and API](13-tools-and-api.md).

### Changed

- **`README.md`** and **[Sources and policy](15-sources-and-policy.md)** now state the licence split
  explicitly instead of the previous "shared for study".
- **[Contributing](contributing.md)** points durable rules at Lessons rather than at a local-only
  file, and warns against linking to unpublished material from a published page.

## 2026-10-09 — CI gate, index reconciliation, and publication preparation

### Added

| File | Purpose |
|---|---|
| `Tools/verify_index.py` | Reconciles [the experiment index](10-experiment-index.md) against the 71 records and the sweep CSVs. Reports row-without-record, record-not-indexed, duplicate ids, invalid or misfiled statuses, metric mismatches,  expression drift, sweep block/region/tally contradictions, and a contradictory `Totals:` line. Exits non-zero on any error; `--selftest` covers two clean fixtures, nine deliberate failures, and the missing-record, unindexed-record, invalid-status, malformed-expression, pending-claimed-as-passed and annotation cases |
| `Tools/check_docs.py --text-scan` | Applies the content rules (excluded references, absolute machine paths, credential shapes) to *any* file type, so the **built** site can be scanned before it is published. A long hex string in a bundled asset warns rather than fails |
| `requirements-docs.txt` | The documentation build dependency, pinned exactly (`mkdocs==1.6.1`). MkDocs' built-in theme means there is no theme package to keep in step |
| `.github/workflows/docs-ci.yml` | On every pull request and push to `main`: tool self-tests, Markdown hygiene, index reconciliation, strict documentation build, built-site scan. Read-only permissions, no credentials, no network beyond installing the pinned dependency |
| `.github/workflows/pages.yml` | Publishing, **manual only** (`workflow_dispatch`) |

### Changed

- **The index is now a verified derived artefact, not a maintained copy.** One authority per
  fact: records and CSVs are canonical, the index is checked against them. The current index
  reconciles exactly — 71 records, 66 experiment rows, 5 sweep rows, 0 errors, 0 warnings.
- **`Tools/check_docs.py`** now shares its table parser with the reconciliation tool, so both
  read a Markdown row the same way.
- **`mkdocs.yml`** takes its base path from the `MKDOCS_SITE_URL` environment variable, with the
  repository's own Pages URL as the fallback, so a fork does not need a code change. Link
  validation is relaxed for the two rules that fire on deliberate links to repository files
  outside `docs/` — those links are still enforced, against the real filesystem, by
  `check_docs.py`. Anchor validation was raised to warn, so a stale anchor fails the strict build.
- **`.gitignore`** covers `site/` and `.venv-docs/`.
- **`docs/13-tools-and-api.md`** documents the reconciliation rules, the CI checks, and the
  publishing procedure; **`docs/contributing.md`** adds the reconciliation step and the CI
  checklist.

### Verified

- Every tool self-test passes: sweep parser, SPC validator, docs checker, index reconciler.
- `mkdocs build --strict` succeeds with no warnings (18 pages), and both the default and an
  overridden `site_url` reach the generated sitemap.
- The built site scans clean for excluded material, machine paths and credential shapes.
- Both workflows pass `actionlint` 1.7.12 with no findings.

### Not done

Nothing was committed, pushed, deployed, or published, and no repository visibility or Pages
setting was changed. Publishing still requires the two manual steps in
[Tools and API](13-tools-and-api.md#publishing-the-site-a-deliberate-act).

## 2026-10-09 — Documentation layer created

### Added

A curated documentation layer under `docs/`, written by synthesising the repository's existing
research notes, experiment records and platform captures. Nothing in the research layer was
deleted or reorganised to create it.

| Page | Contents |
|---|---|
| [`index.md`](index.md) | Landing page: audience, learning path, navigate-by-question table, evidence policy |
| [`01-foundations.md`](01-foundations.md) | What an alpha is, the three controllable layers, the research loop, vocabulary |
| [`02-simulation-settings.md`](02-simulation-settings.md) | Every setting, what it does, and the recorded evidence on its effect |
| [`03-fast-expression.md`](03-fast-expression.md) | Language rules, normalisation families, conditions, vector fields, error catalogue |
| [`04-operators.md`](04-operators.md) | Operators by family with practical rules and failure modes |
| [`05-data-and-fields.md`](05-data-and-fields.md) | Field inspection protocol, selection criteria, recorded family-by-family outcomes, fields to avoid |
| [`06-research-workflow.md`](06-research-workflow.md) | The end-to-end loop, one-change discipline, recipes for inefficient research |
| [`07-evaluating-results.md`](07-evaluating-results.md) | Each metric, how they interact, reading the PnL shape, robustness before enthusiasm |
| [`08-failed-checks.md`](08-failed-checks.md) | Every observed check: meaning, evidence, causes, fixes, when to stop |
| [`09-improving-alphas.md`](09-improving-alphas.md) | The repair catalogue in priority order, plus overfitting countermeasures |
| [`10-experiment-index.md`](10-experiment-index.md) | All 71 recorded experiments, assembled from the records |
| [`11-lessons.md`](11-lessons.md) | Durable lessons with evidence tags, plus explicitly open questions |
| [`12-regions-and-universes.md`](12-regions-and-universes.md) | Per-region recorded evidence, universe effects, ALL-scope behaviour |
| [`13-tools-and-api.md`](13-tools-and-api.md) | The sweep parser and validator, safe credential practice, sweep workflow |
| [`14-advanced.md`](14-advanced.md) | Neutralisation mechanics, correlation gates, multi-region work, sweeps |
| [`15-sources-and-policy.md`](15-sources-and-policy.md) | Source tags, citation rules, conflicts, what was withheld and why |
| [`contributing.md`](contributing.md) | How to add experiments, sweeps and lessons; privacy rules |
| `changelog.md` | This file |

Also added: a repository root README aimed at a public audience, a shared `.gitignore` covering the
private and machine-specific paths, and an optional `mkdocs.yml` for local sidebar navigation.

### Root README replaced

The previous root `README.md` was an internal workflow index (command shortcuts, file list, folder
map, update rules). It has been replaced by a public landing page. Nothing was lost: the command
system is fully documented in `Commands.md`, and the folder map and update rules are carried over
into [`contributing.md`](contributing.md).

### Corrected in the research layer

- **Simulation 070 had an invalid Sharpe column.** An earlier parse wrote the results page's
  `Train Sharpe` into the `sharpe` column for all 2,500 rows. The two columns disagree in 2,448 of
  them. All affected artefacts, the experiment record, the status index, the narrative ledger and
  the field-family table were regenerated from the corrected parse. The two invalid files were then
  removed to leave one canonical product per raw page;
  [`simulations/sweeps/superseded/README.md`](../simulations/sweeps/superseded/README.md) keeps the
  explanation, because the failure mode is instructive.
- **A previously unrecorded page was recovered.** The same export contained a second page of 1,050
  USA blocks that no record had captured. It is now recorded, and it is a useful negative control:
  best Sharpe 1.23, nothing above the bar.
- **Universal attribution corrected.** That page is split into six universes; the earlier record
  labelled all 2,500 blocks TOP3000. 306 blocks were mislabelled.
- **Absolute local paths removed** from repository documents, and account-level metadata generalised.

### Tooling extended

`Tools/brain_sweep_parser.py` gained support for three input shapes it previously could not parse,
each with self-test coverage:

1. Several results pages concatenated in one file (previously only the first page was read, and the
   rest was silently dropped).
2. Blocks headed `### Decay: N · Truncation: X` instead of `### Result N` (previously dropped
   entirely).
3. Pages reporting `Train Fitness` in place of `Train Sharpe`.

Plus a `--prefix` option so a new bundle's combined files cannot overwrite an earlier bundle's, and
a `sharpe` / `train_sharpe` column split made explicit.

`Tools/check_docs.py` was added: a dependency-free hygiene checker for the documentation layer that
verifies relative links resolve, table rows keep their column count, code spans and fences are
balanced, and no excluded path, machine path or credential shape has crept into a published page.
It exits non-zero on any finding and has its own self-test.

### Fixed during validation

- **Malformed code spans in the experiment index.** In 66 table rows the truncated expression was
  closed by a backtick, followed by an ellipsis and then a second backtick. That leaves the inline
  code span unbalanced, so the lesson text after it would render as code. The ellipsis now sits
  inside the span. Six cells whose lesson text was itself abbreviated are marked with a trailing
  `…`, so a reader can tell an abbreviation from a complete sentence. The defect was found while
  validating this page, and code-span balance is now a rule in the checker.
- **Pruned two superseded sweep files** described above, leaving the raw page text under
  `sources/` as the single stored source for each dump.

### Withheld from the public build

Personal agreements and contracts, competition terms, consultant-program instructions and their
program-specific thresholds, verbatim captures of third-party documentation, third-party papers and
formula collections, a platform automation library containing a credential-handling flow, and
machine-specific state directories. The reasoning per category is in
[`15-sources-and-policy.md`](15-sources-and-policy.md); the per-file review is kept privately.

### Not done (deferred)

- No site is deployed, and no repository visibility, remote or Git history was changed.
- Nothing was committed or pushed.
- The EUR sweeps could not be re-parsed from source because their raw pasted text was not retained
  at the time; only the parsed outputs exist.
- Region coverage in the wiki reflects the research that exists: USA and EUR are well covered, other
  regions are thin or absent.

## Earlier history

Experiments 001–071, the bulk sweeps, the corrections and the lessons are recorded in
[`simulations/`](../simulations/), [`Research/lessons_from_simulations.md`](../Research/lessons_from_simulations.md)
and the [experiment index](10-experiment-index.md).
