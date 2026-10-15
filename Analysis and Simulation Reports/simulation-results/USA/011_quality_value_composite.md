# Simulation 011 - Quality Value Composite

Status: FAILED

Expression:

```text
group_neutralize(
    rank(return_equity)
    + rank(cashflow_op / assets)
    - rank(enterprise_value / ebitda),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: 0.46
Fitness: 0.22
Turnover: 3.98%
Sub-universe Sharpe: 0.39
```

Conclusion:

- Structural checks were acceptable.
- Signal was too weak.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `011` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.46` · Fitness: `0.22` · Turnover: `3.98%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.39` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/011_quality_value_composite.md` |

