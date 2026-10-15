# Simulation 031 - Cashflow Quality + ROA Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(cashflow_op / assets, 126))
    + rank(ts_delta(return_assets, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.71
Fitness: 1.13
Self-correlation: 0.933
```

Conclusion:

- Strong metrics, but failed self-correlation.
- `cashflow_op/assets`, `return_assets`, and `ts_mean(-returns,5)` are now crowded in the user's submitted set.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `031` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.71` · Fitness: `1.13` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED_SELF_CORRELATION` · Checks: `FAILED one or more checks` · Self-correlation: `0.933` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/031_cashflow_roa_reversal_selfcorr.md` |

