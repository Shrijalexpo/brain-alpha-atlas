# Simulation 007 - Dividend, Volume Surprise, Return Reversion

Status: FAILED

Expression:

```text
zscore(
    rank(dividend)
    + 0.3 * rank(volume / adv20)
    + 0.2 * rank(-returns)
)
```

Metrics:

```text
Sharpe: 1.78
Fitness: 0.67
Turnover: 57.5%
Decay: 4
```

Conclusion:

- Strong Sharpe.
- Fitness failed because Turnover was too high.
- Next fix should target Turnover, not signal strength.
