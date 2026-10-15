# Simulation 042 - EPS Estimate Delta Error

Status: ERROR

Expression:

```text
rank(ts_delta(eps_estimate_value, 20))
```

Known error:

```text
Operator ts_delta does not support event inputs
```

Conclusion:

- `eps_estimate_value` behaved like event/vector data, not a normal matrix time series.
- Do not use `ts_delta()` directly on this field without proper conversion.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `042` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst Estimates (event/vector) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `unknown` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `ERROR` · Checks: `ERROR` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/042_estimate_eps_delta_error.md` |

