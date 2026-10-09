# Simulation 001 - Positive Days Momentum

Status: FAILED

Expression:

```text
positive_days = ts_sum(returns > 0 ? 1 : 0, 250);

trade_when(
    volume > adv20,
    positive_days,
    -1
)
```

Metrics:

```text
Sharpe: 0.99
Fitness: 1.13
Turnover: 3.04%
Sub-universe Sharpe: 0.47
```

Conclusion:

- Fitness and Turnover were acceptable.
- Sharpe was below the likely threshold.
- Avoid repeating this exact form unless testing ranked or normalized variants.
