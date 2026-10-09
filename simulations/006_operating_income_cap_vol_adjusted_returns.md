# Simulation 006 - Operating Income / Cap Plus Volatility-Adjusted Returns

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-returns / ts_std_dev(returns, 20))
)
```

Metrics:

```text
Sharpe: 0.99
Fitness: 0.86
```

Conclusion:

- Volatility adjustment did not improve this alpha family.
