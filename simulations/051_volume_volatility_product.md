# Simulation 051 - Volume Surprise x Low Volatility

Status: FAILED

Expression:

```text
rank(volume / adv20) * rank(-historical_volatility_20)
```

Known result:

```text
Sharpe: 0.93
Fitness: 0.50
```

Conclusion:

- Medium but not close enough.
- Multiplying volume by low volatility did not preserve the strong standalone volume signal.

