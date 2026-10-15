# Simulation 015 - Cash Flow Yield + ROE + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.18
Fitness: 0.71
Turnover: 30.35%
Sub-universe Sharpe: 0.72
```

Conclusion:

- Close, but not submittable.
- Adding `-returns` materially improved the cashflow/value branch.
- Keep as a useful ancestor, but do not suggest this exact alpha again.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `015` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.18` · Fitness: `0.71` · Turnover: `30.35%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.72` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/015_cashflow_ev_roe_returns.md` |

