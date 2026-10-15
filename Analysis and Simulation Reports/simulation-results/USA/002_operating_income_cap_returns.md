# Simulation 002 - Operating Income / Cap Plus Return Reversion

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-returns)
)
```

Metrics:

```text
Sharpe: 1.14
Fitness: 0.84
Turnover: 22.78%
Sub-universe Sharpe: 0.73
```

Conclusion:

- Close but not passing.
- Both Sharpe and Fitness needed improvement.
- The daily return component was noisy.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `002` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.14` · Fitness: `0.84` · Turnover: `22.78%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.73` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/002_operating_income_cap_returns.md` |

