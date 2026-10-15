# Simulation 046 - Dividend + Volume Surprise + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + rank(volume / adv20)
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 1.86
Fitness: 1.07
Self-correlation: 0.935
```

Conclusion:

- Strong performance, but failed self-correlation.
- Volume/ADV20 was powerful but crowded with existing signals.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `046` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.86` · Fitness: `1.07` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED_SELF_CORRELATION` · Checks: `FAILED one or more checks` · Self-correlation: `0.935` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/046_dividend_volume_returns_selfcorr.md` |

