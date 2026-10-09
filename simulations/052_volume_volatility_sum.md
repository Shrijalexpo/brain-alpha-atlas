# Simulation 052 - Volume Surprise + Low Volatility

Status: FAILED

Expression:

```text
rank(volume / adv20) + rank(-historical_volatility_20)
```

Known result:

```text
Sharpe: 0.54
Fitness: 0.29
```

Conclusion:

- Weak. Adding low volatility diluted the volume signal.

