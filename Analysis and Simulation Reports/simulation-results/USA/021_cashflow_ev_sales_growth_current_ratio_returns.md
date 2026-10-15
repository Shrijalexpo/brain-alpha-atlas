# Simulation 021 - Cash Flow Yield + Sales Growth + Current Ratio + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(sales_growth)
    + rank(current_ratio)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: worse than Simulation 020.
```

Conclusion:

- `current_ratio` hurt the best cashflow/value-growth branch.
- Do not suggest this exact alpha again.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `021` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `unknown` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/021_cashflow_ev_sales_growth_current_ratio_returns.md` |

