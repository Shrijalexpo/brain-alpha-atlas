# Simulation 027 - Submitted Cashflow Quality + Operating Improvement + Reversal

Status: PASSED_SUBMITTED

Expression:

```text
group_neutralize(
    rank(ts_rank(cashflow_op / assets, 126))
    + rank(ts_delta(operating_income / assets, 63))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.39
Fitness: 0.73 in IS summary
Turnover: 21.31%
Returns: 5.85%
Submission: Successfully submitted according to shared result
```

Conclusion:

- This became a submitted alpha.
- It uses a quality/improvement backbone plus the recurring 5-day mean-reversion component.
- Do not suggest this exact expression again.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `027` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.39` · Fitness: `0.73 in IS summary` · Turnover: `21.31%` · Returns: `5.85%` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `PASSED_SUBMITTED` · Checks: `PASSED user-level checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/027_submitted_cashflow_quality_improvement_reversal.md` |

