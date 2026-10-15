# Simulation 025 - Time-Series Ranked EBITDA Yield + Time-Series Ranked Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.78
Fitness: 0.97
Sub-universe Sharpe: 1.78
```

Conclusion:

- Very strong, but still not submittable because Fitness was just below 1.
- Time-series ranking `sales_growth` was a major improvement.
- Exact expression should not be repeated; use only as the direct parent of the submitted alpha.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `025` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.78` · Fitness: `0.97` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.78` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/025_ts_rank_ebitda_ev_ts_rank_sales_growth_returns.md` |

