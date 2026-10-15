# Simulation 026 - Submitted Alpha: TS-Ranked Value + TS-Ranked Growth + Smoothed Reversal

Status: PASSED_SUBMITTABLE

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.61
Fitness: 1.02
Turnover: 25.25%
Sub-universe Sharpe: 1.53
Competition Challenge: Passed
Self-correlation: pending at screenshot time
```

Conclusion:

- This is the first recorded submittable alpha.
- Smoothing the reversal component with `ts_mean(-returns, 5)` pushed Fitness above 1.
- Do not suggest this exact alpha again. Treat it as a protected submitted baseline.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `026` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.61` · Fitness: `1.02` · Turnover: `25.25%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.53` |
| **Check Verdict & Failure Reasons** | Status `PASSED_SUBMITTABLE` · Checks: `PASSED user-level checks` · Self-correlation: `pending at screenshot time` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md` |

