# Simulation 057 - EBITDA/EV + TS-Ranked Returns

Status: FAILED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(ts_rank(-returns, 10))
```

Known result:

```text
Sharpe: 1.11
Fitness: 0.58
```

Conclusion:

- Worse than the submitted 5-day mean-reversion version.
- `ts_mean(-returns,5)` was better than `ts_rank(-returns,10)`.

