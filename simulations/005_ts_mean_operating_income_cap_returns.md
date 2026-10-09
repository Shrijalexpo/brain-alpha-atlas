# Simulation 005 - Smoothed Operating Income / Cap Plus Return Reversion

Status: FAILED

Expression:

```text
zscore(
    rank(ts_mean(operating_income / cap, 4))
    +
    0.4 * rank(-returns)
)
```

Metrics:

```text
Sharpe: 1.01
Fitness: 0.89
```

Conclusion:

- Smoothing the slow-moving fundamental component did not help enough.
