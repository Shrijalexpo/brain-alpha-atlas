# Simulation 044 - Dividend + Return Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + 0.5 * rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 1.50
Fitness: 0.83
Sub-universe Sharpe: 1.22
Later retest: Sharpe 1.47, Fitness 0.82, Turnover 59.5%
```

Conclusion:

- Strong Sharpe, but Fitness failed.
- Settings alone were not enough to fix it.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `044` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.50` · Fitness: `0.83` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.22` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/044_dividend_returns_industry.md` |

