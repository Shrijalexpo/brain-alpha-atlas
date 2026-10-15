# Simulation 040 - SNT Value + EBITDA/EV

Status: FAILED

Expression:

```text
rank(ts_rank(snt_value, 252))
+ rank(ts_rank(ebitda / enterprise_value, 126))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.11
Fitness: 0.60
```

Conclusion:

- Weak alpha after mixing sentiment with value.
- Do not prioritize this sentiment/value combination.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `040` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Sentiment (scl12 / snt) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.11` · Fitness: `0.60` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/040_sentiment_snt_value_ebitda.md` |

