# Simulation 040 - SNT Value + EBITDA/EV

Status: FAILED

Expression:

```text
rank(ts_rank(snt_value, 252))
+ rank(ts_rank(ebitda / enterprise_value, 126))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.11
Fitness: 0.60
```

Conclusion:

- Weak alpha after mixing sentiment with value.
- Do not prioritize this sentiment/value combination.

