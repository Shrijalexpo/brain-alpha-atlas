# Simulation 004 - Operating Income / Cap Plus Smoothed Returns

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-ts_mean(returns, 5))
)
```

Metrics:

```text
Sharpe: 1.05
Fitness: 0.98
```

Conclusion:

- Worse Sharpe than the `ts_rank(returns, 20)` variant.
- Fitness was close but still below target.
