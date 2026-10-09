# Simulation 002 - Operating Income / Cap Plus Return Reversion

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-returns)
)
```

Metrics:

```text
Sharpe: 1.14
Fitness: 0.84
Turnover: 22.78%
Sub-universe Sharpe: 0.73
```

Conclusion:

- Close but not passing.
- Both Sharpe and Fitness needed improvement.
- The daily return component was noisy.
