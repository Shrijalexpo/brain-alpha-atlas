# Simulation 014 - Cash Flow Yield

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: 0.41
```

Conclusion:

- Positive but weak.
- Best current base direction from the latest tests.
- Add one complementary factor at a time.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `014` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.41` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/014_cashflow_yield.md` |

