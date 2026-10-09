# Simulation 003 - Operating Income / Cap Plus Time-Series Return Rank

Status: FAILED

Expression:

```text
zscore(
    rank(operating_income / cap)
    +
    0.4 * rank(-ts_rank(returns, 20))
)
```

Metrics:

```text
Sharpe: 1.29
Fitness: 0.60
Turnover: 63.33%
Sub-universe Sharpe: 0.77
```

Conclusion:

- Sharpe passed.
- Fitness failed because Turnover was very high.
- Do not repeat without changing Decay or smoothing/reducing the return component.
