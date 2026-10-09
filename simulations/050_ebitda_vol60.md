# Simulation 050 - EBITDA + Low 60-Day Volatility

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(ebitda)
        + rank(-historical_volatility_60)
    ),
    industry
)
```

Known result:

```text
Sharpe: 0.05
Fitness: 0.01
```

Conclusion:

- Very poor. Drop this branch.

