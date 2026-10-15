# Simulation 007 - Dividend, Volume Surprise, Return Reversion

Status: FAILED

Expression:

```text
zscore(
    rank(dividend)
    + 0.3 * rank(volume / adv20)
    + 0.2 * rank(-returns)
)
```

Metrics:

```text
Sharpe: 1.78
Fitness: 0.67
Turnover: 57.5%
Decay: 4
```

Conclusion:

- Strong Sharpe.
- Fitness failed because Turnover was too high.
- Next fix should target Turnover, not signal strength.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `007` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.78` · Fitness: `0.67` · Turnover: `57.5%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/007_dividend_volume_returns.md` |

