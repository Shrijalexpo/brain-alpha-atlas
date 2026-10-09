# Tools and Reproducible Workflows

Small, dependency-free scripts in this repository that make large-scale research tractable — and
the rules for handling platform credentials safely.

Everything documented here runs on a plain Python 3 install. No third-party packages, no
network access, no accounts.

## `Tools/brain_sweep_parser.py`

Paste a BRAIN multi-simulation results page into a text file and this script turns it into
machine-readable results and a readable report. It is the tool that keeps a 5,000-block sweep
from becoming a spreadsheet problem.

### What it handles

| Input shape | Behaviour |
|---|---|
| One pasted results page | One set of outputs |
| **Several pages concatenated in one file** | Splits on every `N Results` header; each page keeps its own settings and its own `Fx` legend |
| Blocks headed `### Result N` | Standard layout |
| Blocks headed `### Decay: N · Truncation: X` | Result numbers are synthesised (flagged `number_synthesised`); decay and truncation are stored per row |
| Pages reporting `Train Fitness` instead of `Train Sharpe` | Parsed into a separate `train_fitness` column |

### Why the `Fx` legend matters

The platform abbreviates failed-check sets as `F1`, `F2`, … **and the mapping is per results page.**
`F14` in one dump can mean a different set of checks than `F14` in another. The parser resolves
each code through its own page's legend and stores the resolved names in `failed_checks`. Compare
resolved names across files, never raw codes. `[Observed]`

### Usage

```bash
python3 Tools/brain_sweep_parser.py --selftest

python3 Tools/brain_sweep_parser.py SWEEP.txt --outdir simulations/sweeps

# A bundle already stored in the same directory: prefix the combined files so they
# cannot overwrite the earlier bundle's all_results.csv / SUMMARY.md
python3 Tools/brain_sweep_parser.py SWEEP.txt --outdir simulations/sweeps --prefix 20261009_
```

Outputs per page: `<slug>.csv` (one row per result block), `<slug>.json` (data plus settings,
legend and section offsets) and `<slug>.md` (a generated report with headline counts, failed-check
frequency, top-N tables and per-family bests). With more than one page it also writes
`all_results.csv` and `SUMMARY.md`.

CSV columns:

```text
result_no  universe  neutralization  decay  truncation  family  primary_field
sharpe  train_sharpe  train_fitness  fitness  turnover  returns  drawdown
margin_bps  long_count  short_count  status  failed_check_codes  failed_checks  expression
```

**`sharpe` and `train_sharpe` are different columns.** In the recorded USA sweep they disagreed in
2,448 of 2,500 rows, with the training column systematically higher. Never treat them as
interchangeable, and never build a summary from the wrong one. `[Observed]`

The `--selftest` flag runs built-in checks covering single-page files, concatenated multi-page
files, decay-style block headers, per-page legend isolation and output generation. Run it after
any modification.

### Statuses it emits

`PASS`, `FAIL`, or `PENDING` for blocks that were still computing when the page was captured.
`PENDING` is **not** a pass and not a clean result — it is an absence of measurement. `[Observed]`

## `Tools/validate_spc_isin.py`

A dependency-free validator for ISIN/MIC identifiers and JSON sample outputs, with a `--selftest`
mode. It exists because competition-style tasks that require instrument identifiers need a fast
sanity check before submission.

```bash
python3 Tools/validate_spc_isin.py --selftest
python3 Tools/validate_spc_isin.py --isin US0378331005
```

It performs checksum validation and format checks locally. It does not connect to any service, and
it does not validate whether an identifier is *correct* for your task — only whether it is
well-formed.

## `Tools/check_docs.py`

A hygiene checker for this documentation layer. Editing many Markdown tables by hand introduces
exactly the defects that are invisible on screen but obvious to a reader: a link to a file that
was never published, a table row with one cell too few, an unbalanced code span.

```bash
python3 Tools/check_docs.py --selftest          # built-in fixtures
python3 Tools/check_docs.py                     # docs/ and README.md
python3 Tools/check_docs.py docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS
```

| Rule | Catches |
|---|---|
| `link` | relative Markdown links that do not resolve on disk |
| `table` | a row whose cell count differs from its table's header |
| `backtick` | an odd number of inline-code backticks on a line |
| `fence` | an unterminated or never-opened code fence |
| `private-ref` | a reference to material excluded from the public build |
| `home-path` | an absolute machine path such as `/Users/<name>/…` |
| `secret` | an obvious credential shape (token assignment, long hex string) |

It exits non-zero when it finds anything, so it works as a pre-commit check. It is deliberately
narrow — it is a spelling checker for formatting, not a substitute for reading the page. `[Notes]`

## `Tools/verify_index.py`

[The experiment index](10-experiment-index.md) is the page readers trust most and the one most
likely to drift, because it repeats numbers that actually live in 71 record files and five sweep
bundles. This tool reconciles the two, and it is the reason the index can be trusted as a
summary. `[Notes]`

The repository keeps one authoritative home per fact:

| Fact | Authority |
|---|---|
| Status, expression, metrics, lessons for one experiment | the record, `simulations/NNN_*.md` |
| Block counts, per-block metrics, PASS/PENDING tallies | the sweep CSV files, `simulations/sweeps/*.csv` |
| Everything in the index | **derived**; verified against the two rows above, never the other way round |

The index is verified rather than generated because its lesson column is deliberately condensed
prose — generating it would have to throw that away.

```bash
python3 Tools/verify_index.py --selftest   # built-in fixtures
python3 Tools/verify_index.py              # exit 0 when the index matches the records
```

| Rule | Caught |
|---|---|
| `row-without-record` / `record-not-indexed` | an index row with no record, or a record no row mentions |
| `duplicate-id` | the same experiment indexed twice |
| `invalid-status` / `status-section` | a status outside the vocabulary, or a record filed in the wrong section |
| `pending-claimed-passed` | unevaluated (`PENDING`) blocks presented as a pass |
| `metric-value` / `metric-shape` | a metric cell that disagrees with the record, or cannot be interpreted |
| `metric-omitted` (warning) | the index shows `—` where the record does hold a value |
| `expression-prefix` / `expression-malformed` | a quoted expression that is not a truncation of the record's, or unbalanced brackets |
| `sweep-blocks` / `sweep-source-missing` | a block or page count that disagrees with the CSVs, or a missing CSV |
| `sweep-region` | a region or universe the record settings, CSVs and dump names do not support |
| `sweep-decay` | per-block `decay` in a CSV disagreeing with the decay the record states for that dump |
| `sweep-passes` / `sweep-pending` / `sweep-threshold` | a PASS, PENDING or “N blocks cleared” claim the data contradicts |
| `sweep-quote-unsupported` | a Sharpe or Fitness number quoted in the index that appears nowhere in the sweep |
| `totals` | the headline “Totals:” line disagreeing with the sections |

Settings are compared only where both sides carry the value: a CSV whose `decay` column is
empty for a dump is not compared against the record's prose, and the run prints how many such
comparisons it actually made (`decay-dumps-compared=`), so an unverified surface is never
mistaken for a verified one. Other settings — neutralisation, truncation, pasteurisation — are
recorded in the records but not repeated in the index, so they are out of this tool's scope.
`[Notes]`

Normalisation is deliberately narrow, and it is the only place a value is allowed to differ in
appearance: whitespace is collapsed; a truncated display expression must be an exact
whitespace-insensitive prefix of the record's; numbers compare after removing thousands
separators, a trailing `%`, a leading `+` and the Unicode minus sign; an annotated cell such as
`0.73 in IS summary` is valid only if the record holds the same text. Nothing here rewrites a
canonical value to make a check pass. `[Notes]`

What it does **not** check: the wording of the lesson column, the settings and failed-check
outcomes of individual experiments (the index carries no such columns — see the records), and
anything outside this repository. It never contacts the platform.

## Continuous integration

Two workflows, both offline. Neither needs a credential, a dataset, or a simulation.

| Workflow | Trigger | Checks |
|---|---|---|
| `.github/workflows/docs-ci.yml` | every pull request, and pushes to `main` | tool self-tests, Markdown hygiene, index reconciliation, strict MkDocs build, built-site scan |
| `.github/workflows/pages.yml` | **manual only** (`workflow_dispatch`) | repeats those checks, then publishes `site/` to GitHub Pages |

The build runs on the Python version pinned in the workflow (3.12). The tools are written for
3.9+ and standard-library only, so they also run on a stock macOS `python3`. `[Notes]`

Run the same checks locally:

```bash
python3 Tools/brain_sweep_parser.py --selftest
python3 Tools/validate_spc_isin.py --selftest
python3 Tools/check_docs.py --selftest
python3 Tools/verify_index.py --selftest
python3 Tools/check_docs.py docs README.md mkdocs.yml LICENSE NOTICE LICENSE-DOCS
python3 Tools/verify_index.py

python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
.venv-docs/bin/python -m mkdocs build --strict
python3 Tools/check_docs.py --text-scan site
```

`requirements-docs.txt` pins the only build dependency, and `mkdocs.yml` uses MkDocs' built-in
theme: a documentation build should not be able to grow a dependency tree or reach the network.
`[Notes]`

### Publishing the site (a deliberate act)

The site is not published by this configuration, and nothing deploys on a push. To publish:

```text
1. Settings -> Pages -> Build and deployment -> Source: GitHub Actions   (once)
2. Actions -> "Publish docs to GitHub Pages" -> Run workflow             (each release)
3. A fork, or a renamed repository, also sets the repository variable
   MKDOCS_SITE_URL (Settings -> Secrets and variables -> Actions -> Variables),
   for example https://<owner>.github.io/<repo>/
```

Two properties make that safe to do from a repository like this one: `site/` is git-ignored and
built only from `docs/`, so material excluded from `docs/` cannot reach the artefact; and the
workflow scans the built output with `Tools/check_docs.py --text-scan` before uploading it, so a
private path or excluded reference fails the job instead of being published. Publishing still
makes the wiki public — do it deliberately. `[Notes]`

## Platform API access

This repository also contains a research-automation library that logs into the platform and
drives simulations through the official API. **It is deliberately not documented or reproduced in
this wiki.** The reasons are practical, not secretive:

| Reason | Detail |
|---|---|
| Credentials | The library reads login credentials from a local file outside the repository and prompts interactively. Publishing the flow invites credential mishandling |
| Account data | Notebook outputs can embed session and account artefacts; they must be cleared before sharing |
| Maintenance | API details track a moving platform; stale instructions are worse than none |
| Terms | Automation limits and permitted use are governed by the platform's own terms, which change |

If you use API automation, the safe pattern is: `[Notes]`

```text
1. Keep credentials in a local file outside any repository, never in code.
2. Never paste a token, session id or cookie into a notebook cell that gets committed.
3. Clear notebook outputs before sharing or committing.
4. Re-read the platform's current automation rules before scripting anything at scale.
5. Treat a rate limit as a signal, not an obstacle.
```

## General research-tooling rules

- **Keep tooling dependency-free where practical.** A parser that needs no packages still runs in
  five years, which matters more than elegance for a research archive. `[Notes]`
- **Always provide a self-test.** Every script here has one; a parser without a self-test is a
  parser you cannot trust after an edit.
- **Preserve the source text.** Store the raw pasted page alongside the parsed output so a sweep
  can be re-parsed when the parser improves. The EUR sweeps in this repository cannot be
  re-parsed because their raw text existed only transiently — a mistake worth not repeating.
  `[Observed]`
- **Sanitise before sharing.** Absolute local paths, usernames, account identifiers and email
  addresses leak through copied log output far more often than through code.

## Reproducing a sweep workflow end to end

```text
1. Run the sweep in the platform's multi-simulation interface.
2. Copy the whole results page into a text file.
3. Save the raw text alongside the parsed output (this is the step that is usually skipped).
4. Parse it: Tools/brain_sweep_parser.py SWEEP.txt --outdir simulations/sweeps --prefix <stem>_
5. Read the generated <stem>.md first — headline counts and failed-check frequency.
6. Rank candidates from the CSV, filtering on out-of-sample Sharpe and Fitness.
7. Check the whole page's failed-check pattern before believing any single block.
8. Record the sweep in the experiment index with its block count and best result.
```

See [Experiment index](10-experiment-index.md) for what the recorded sweeps found, and
[Sources and evidence policy](15-sources-and-policy.md) for how to cite them.

Next: [Advanced topics](14-advanced.md).
