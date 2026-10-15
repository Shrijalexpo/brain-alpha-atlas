# Simulation 063 - High-Turnover Operating Cash Flow Estimate Stddev

Status: FAILED

Expression:

```text
zscore(
    rank(ts_delta(op_cash_flow_stddev, 10))
    + 0.4 * rank(volume / adv20)
    - 0.2 * rank(returns)
)
```

Known result:

```text
Sharpe: 1.52
Fitness: 0.84
```

Conclusion:

- Strong Sharpe but failed Fitness.
- Needs smoothing or persistence, but exact expression should not be repeated.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `063` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst / Cashflow Estimate Dispersion |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.52` · Fitness: `0.84` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/063_op_cash_flow_stddev_high_turnover.md` |

