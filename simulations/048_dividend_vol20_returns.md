# Simulation 048 - Dividend + Low Volatility + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + rank(-historical_volatility_20)
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 0.42
Fitness: 0.22
```

Conclusion:

- Bad result. Low volatility did not complement the dividend branch.

