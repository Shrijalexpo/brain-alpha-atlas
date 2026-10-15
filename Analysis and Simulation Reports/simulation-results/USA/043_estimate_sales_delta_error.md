# Simulation 043 - Sales Estimate Delta Error

Status: ERROR

Expression:

```text
rank(ts_delta(sales_estimate_value, 20))
```

Known error:

```text
Operator ts_delta does not support event inputs
```

Conclusion:

- `sales_estimate_value` behaved like event/vector data.
- Use only valid matrix fields or convert vector/event fields with appropriate `vec_*` operators first.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `043` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst Estimates (event/vector) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `unknown` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `ERROR` · Checks: `ERROR` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/043_estimate_sales_delta_error.md` |

