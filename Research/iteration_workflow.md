# Iteration Workflow

Use this workflow for every WorldQuant BRAIN alpha iteration.

## Before Suggesting An Alpha

Read or check:

```text
Commands.md
simulations/status_index.md
Research/lessons_from_simulations.md
AlphaQueue/suggested_not_confirmed.md                (created on demand)
instructions.md                                      (local only, not published)
```

`instructions.md` and `CLAUDE.md` hold personal working preferences and are excluded from the
public repository by `.gitignore`; the general rules they produce are republished under
[`docs/`](../docs/index.md).

Then:

- Avoid exact failed/submitted/error/self-correlation formulas.
- Avoid recently exhausted families unless the user asks to revisit them.
- Prefer one clear economic idea per alpha.
- Give at most 3 candidates.

## When A Screenshot Result Arrives

Save first, then suggest.

1. Identify the alpha expression.
2. Extract settings if visible.
3. Extract metrics and checks.
4. Assign status:

```text
PASSED_SUBMITTED: user says submitted
PASSED_SUBMITTABLE: passes checks but not confirmed submitted
FAILED_SELF_CORRELATION: rejected for similarity
ERROR: syntax/type/unit/field/operator issue
FAILED: performance or robustness failed
```

5. Create the next numbered file in `simulations/`.
6. Update `simulations/status_index.md`.
7. Update `Research/lessons_from_simulations.md` if it teaches a new pattern.
8. Only then suggest the next 1 to 3 candidates.

## How To Decide The Next Move

Use the bottleneck:

```text
Low Sharpe: change signal or field family.
Good Sharpe, low Fitness: improve persistence, returns, or turnover.
High Turnover: smooth signal or increase Decay.
Self-correlation fail: change the economic backbone, not just the window.
Operator error: fix field type, units, syntax, or unsupported operator.
Negative Sharpe: reverse only if economic logic supports it; otherwise drop branch.
```

## Current No-Repeat Backbones

Be careful with these because they have been submitted, failed, or caused self-correlation:

- `ts_rank(ebitda / enterprise_value, 126) + ts_rank(sales_growth, 126) + ts_mean(-returns, 5)`
- `ts_rank(cashflow_op / assets, 126) + ts_delta(operating_income / assets, 63) + ts_mean(-returns, 5)`
- `rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))`
- `operating_income / assets + return_assets + ts_mean(-returns, 5)`
- `cashflow_op / assets + return_assets + ts_mean(-returns, 5)`
- `dividend + volume / adv20 + -returns`
- pure sentiment plus buzz fields
- `*_fast_d1` sentiment fields
- direct `ts_delta()` on event/vector estimate fields like `eps_estimate_value`

