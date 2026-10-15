# Simulation 061 - TS-Ranked EBITDA/EV + 5-Day Mean Reversion

Status: FAILED

Expression:

```text
rank(ts_rank(ebitda / enterprise_value, 126))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.51
Fitness: 0.98
```

Conclusion:

- Very close, but missed Fitness by about 0.02.
- This is a strong family, but exact expression should not be repeated.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `061` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.51` · Fitness: `0.98` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/061_ts_rank_ebitda_ev_mean_reversion_close.md` |

