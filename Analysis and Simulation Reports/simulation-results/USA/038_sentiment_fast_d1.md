# Simulation 038 - Fast D1 Sentiment

Status: FAILED

Expression:

```text
rank(ts_delta(scl12_sentiment_fast_d1, 10))
+ rank(ts_rank(scl12_buzz_fast_d1, 63))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.11
Turnover: 87%
```

Conclusion:

- Fast D1 sentiment fields produced very high turnover.
- Avoid `*_fast_d1` sentiment fields for now.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `038` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Sentiment (scl12 / snt) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.11` · Fitness: `unknown` · Turnover: `87%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/038_sentiment_fast_d1.md` |

