# Simulation 001 - Positive Days Momentum

Status: FAILED

Expression:

```text
positive_days = ts_sum(returns > 0 ? 1 : 0, 250);

trade_when(
    volume > adv20,
    positive_days,
    -1
)
```

Metrics:

```text
Sharpe: 0.99
Fitness: 1.13
Turnover: 3.04%
Sub-universe Sharpe: 0.47
```

Conclusion:

- Fitness and Turnover were acceptable.
- Sharpe was below the likely threshold.
- Avoid repeating this exact form unless testing ranked or normalized variants.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `001` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.99` · Fitness: `1.13` · Turnover: `3.04%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.47` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/001_positive_days_momentum.md` |

