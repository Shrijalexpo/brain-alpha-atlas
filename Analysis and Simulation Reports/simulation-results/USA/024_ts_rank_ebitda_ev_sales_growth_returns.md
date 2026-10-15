# Simulation 024 - Time-Series Ranked EBITDA Yield + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.36
Fitness: 0.68
Sub-universe Sharpe: 1.39
```

Conclusion:

- First branch to pass the Sharpe threshold.
- Fitness still failed, so the signal needed smoother/more robust components.
- Time-series rank on `ebitda / enterprise_value` was a major improvement.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `024` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.36` · Fitness: `0.68` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.39` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/024_ts_rank_ebitda_ev_sales_growth_returns.md` |

