# Simulation 059 - EBITDA/EV + Return Delta

Status: FAILED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(ts_delta(-returns, 5))
```

Known result:

```text
Sharpe: 1.06
Fitness: 0.55
```

Conclusion:

- Return delta was worse than 5-day mean reversion.

