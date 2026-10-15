# Simulation 052 - Volume Surprise + Low Volatility

Status: FAILED

Expression:

```text
rank(volume / adv20) + rank(-historical_volatility_20)
```

Known result:

```text
Sharpe: 0.54
Fitness: 0.29
```

Conclusion:

- Weak. Adding low volatility diluted the volume signal.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `052` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.54` · Fitness: `0.29` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/052_volume_volatility_sum.md` |

