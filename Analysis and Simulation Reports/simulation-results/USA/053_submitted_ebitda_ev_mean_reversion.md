# Simulation 053 - Submitted EBITDA/EV + 5-Day Mean Reversion

Status: PASSED_SUBMITTED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.46
Fitness: 1.05
Submission: Passed and submitted
```

Conclusion:

- Simple value plus short-term mean reversion worked.
- Do not suggest this exact expression again.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `053` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.46` · Fitness: `1.05` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `PASSED_SUBMITTED` · Checks: `PASSED user-level checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/053_submitted_ebitda_ev_mean_reversion.md` |

