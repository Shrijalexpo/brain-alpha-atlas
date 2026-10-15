# Simulation 033 - Operating Income Quality + EBITDA/EV Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(ebitda / enterprise_value, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: failed self-correlation.
```

Conclusion:

- Changing ROA trend to value trend did not solve correlation.
- Avoid this same quality plus value plus 5-day reversal backbone.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `033` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `unknown` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED_SELF_CORRELATION` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/033_operating_income_ebitda_ev_delta_reversal_selfcorr.md` |

