# Simulation 047 - Dividend + Intraday Close Range + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + rank((close - low) / (high - low))
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 0.62
Fitness: 0.19
```

Conclusion:

- Weak. Drop this branch.

