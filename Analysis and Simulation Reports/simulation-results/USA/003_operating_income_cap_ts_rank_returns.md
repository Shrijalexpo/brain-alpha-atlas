# Simulation 003 - Operating Income / Cap Plus Time-Series Return Rank

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-ts_rank(returns, 20))
)
```

Metrics:

```text
Sharpe: 1.29
Fitness: 0.60
Turnover: 63.33%
Sub-universe Sharpe: 0.77
```

Conclusion:

- Sharpe passed.
- Fitness failed because Turnover was very high.
- Do not repeat without changing Decay or smoothing/reducing the return component.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `003` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.29` · Fitness: `0.60` · Turnover: `63.33%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.77` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/003_operating_income_cap_ts_rank_returns.md` |

