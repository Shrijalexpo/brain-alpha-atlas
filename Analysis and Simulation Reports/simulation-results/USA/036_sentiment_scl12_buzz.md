# Simulation 036 - SCL12 Sentiment + Buzz

Status: FAILED

Expression:

```text
rank(ts_rank(scl12_sentiment, 126))
+ rank(ts_delta(scl12_buzz, 21))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.38
Fitness: 0.44
Turnover: 87.5%
```

Conclusion:

- Sentiment had predictive power but turnover was too high.
- Pure sentiment/buzz signals were too reactive.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `036` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Sentiment (scl12 / snt) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.38` · Fitness: `0.44` · Turnover: `87.5%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/036_sentiment_scl12_buzz.md` |

