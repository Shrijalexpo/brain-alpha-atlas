# WorldQuant BRAIN Command System

Use these short commands in chat to make the alpha workflow faster and consistent. Every command must use the saved knowledge base before answering.

Core rule:

- Before generating or fixing an alpha, check the saved knowledge base: `simulations/status_index.md`, `Research/lessons_from_simulations.md`, and the queue in `AlphaQueue/suggested_not_confirmed.md` (created on demand).
- After each simulation screenshot/result, save the alpha, settings, metrics, status, and lesson before suggesting the next iteration.
- Never suggest an exact alpha that is already marked `FAILED`, `ERROR`, `FAILED_SELF_CORRELATION`, `PASSED_SUBMITTABLE`, or `PASSED_SUBMITTED`.
- Give at most 3 alpha candidates at once.

> **Local-only working files.** `instructions.md` and `CLAUDE.md` hold personal working
> preferences and are deliberately kept out of this public repository (see `.gitignore`). The
> durable, general rules they produce are republished in [`docs/`](docs/index.md), chiefly
> [Lessons](docs/11-lessons.md) and [Research workflow](docs/06-research-workflow.md).

## Main Commands

### `#new`

Generate fresh alpha candidates.

Behavior:

- Generate 1 to 3 new alpha expressions.
- Use previous learnings and avoid repeated failed/submitted structures.
- Prefer meaningful economic logic over random formulas.
- Avoid expression-level `group_neutralize()` unless specifically needed.
- Include recommended settings only if they differ from the current default.

Optional variants:

```text
#new volatility
#new analyst estimates
#new low correlation
#new high turnover
#new no fundamentals
```

### `#fix`

Debug or improve the alpha shown by the user.

Behavior:

- Read the alpha and screenshot metrics/errors.
- Identify the main bottleneck first: Sharpe, Fitness, Turnover, Returns, Drawdown, Sub-universe Sharpe, self-correlation, or syntax/type/unit error.
- Save the current simulation result before giving fixes.
- Suggest 1 to 3 targeted fixes only.
- Change one meaningful mechanism at a time when possible.

### `#save`

Save a simulation, dataset field list, tutorial note, reference, or error without generating a new alpha.

Behavior:

- If it is a simulation, create the next numbered file in `simulations/`.
- Update `simulations/status_index.md`.
- Update `Research/lessons_from_simulations.md` if there is a useful lesson.
- If it is a field list, save it under `Data/`.
- If it is an error, save it under `Troubleshooting/`.
- If it is a paper/book/reference, save it under `Books/References/`.

Useful forms:

```text
#save simulation
#save fields
#save error
#save tutorial
#save reference
```

### `#learn`

Summarize what has been learned from recent simulations.

Behavior:

- Read the latest simulation files and status index.
- Identify which factor families are working, weak, crowded, or error-prone.
- Update `Research/lessons_from_simulations.md` if new lessons are present.
- Do not generate alpha code unless asked.

Useful forms:

```text
#learn
#learn last 5
#learn sentiment
#learn submitted
```

### `#status`

Show the current alpha research state.

Behavior:

- Summarize submitted alphas, failed branches, close candidates, and no-repeat patterns.
- Mention the latest default settings.
- Do not generate new alpha code unless combined with `#new`.

### `#settings`

Recommend simulation settings for the current alpha or alpha family.

Behavior:

- Start from current default settings unless the screenshot says otherwise.
- Explain only the settings that matter.
- Avoid over-tuning settings when the signal itself is weak.

### `#fields`

Save or evaluate available data fields.

Behavior:

- Extract field names from user screenshots/text.
- Save them under `Data/`.
- Classify fields by theme: value, quality, growth, sentiment, analyst, volatility, price/volume, event/vector risk.
- Recommend which fields are worth testing and which to avoid.

### `#error`

Debug a BRAIN error message.

Behavior:

- Identify whether it is syntax, field availability, unit mismatch, vector/event input, NaN, operator type, or submission error.
- Save recurring errors under `Troubleshooting/`.
- Give a corrected expression or clear next step.

### `#submitted`

Mark an alpha as submitted/passed.

Behavior:

- Save the alpha as `PASSED_SUBMITTED` or `PASSED_SUBMITTABLE`.
- Update `simulations/status_index.md`.
- Add it to the no-repeat list.
- Extract lessons from why it worked.

### `#correlation`

Fix or analyze self-correlation failure.

Behavior:

- Save the failed alpha as `FAILED_SELF_CORRELATION`.
- Do not make tiny cosmetic changes.
- Identify repeated backbone factors.
- Suggest 1 to 3 genuinely different replacements or a new factor family.

### `#queue`

Save alpha ideas that were suggested but not yet simulated.

Behavior:

- Add ideas to `AlphaQueue/suggested_not_confirmed.md`.
- Do not mark as failed or passed until results are shared.

### `#avoid`

Record a new user preference or pattern to avoid.

Behavior:

- Update the local `instructions.md` if the rule is personal, or [`docs/11-lessons.md`](docs/11-lessons.md) if it is general.
- If related to alpha generation, also update `Research/lessons_from_simulations.md`.

Examples:

```text
#avoid group_neutralize
#avoid sentiment fast_d1
#avoid more than 3 alphas
```

## Default Current Workflow

1. User sends `#new`, `#fix`, or a simulation screenshot.
2. Check prior simulations and instructions.
3. Save any new result first.
4. Extract the lesson.
5. Generate at most 3 next candidates.
6. Mark anything suggested but not yet tested in `AlphaQueue/`.

## Default Current Settings

Unless the user says otherwise:

```text
Instrument Type: Equity
Region: USA
Universe: TOP3000
Language: Fast Expression
Delay: 1
Neutralization: Subindustry
Decay: 4
Truncation: 0.08
Pasteurization: On
Unit Handling: Verify
NaN Handling: Off
```

