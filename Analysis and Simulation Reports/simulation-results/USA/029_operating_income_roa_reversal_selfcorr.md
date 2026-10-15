# Simulation 029 - Operating Income Quality + ROA Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(return_assets, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.76
Fitness: 1.21
Turnover: 18.73%
Sub-universe Sharpe: 1.37
Self-correlation: 0.8817
Self-correlation cutoff: 0.70
```

Conclusion:

- Performance passed, but self-correlation failed.
- The backbone was too similar to existing submitted alphas.
- Avoid this exact structure.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `029` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.76` · Fitness: `1.21` · Turnover: `18.73%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.37` |
| **Check Verdict & Failure Reasons** | Status `FAILED_SELF_CORRELATION` · Checks: `FAILED one or more checks` · Self-correlation: `0.8817` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/029_operating_income_roa_reversal_selfcorr.md` |

