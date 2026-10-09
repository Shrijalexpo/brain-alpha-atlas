# Simulation 045 - Dividend + Close/VWAP + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + rank((close - vwap) / vwap)
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 0.60
Fitness: 0.18
```

Conclusion:

- Weak. Drop this branch.

