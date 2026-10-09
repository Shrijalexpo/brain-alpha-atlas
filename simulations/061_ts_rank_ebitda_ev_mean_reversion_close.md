# Simulation 061 - TS-Ranked EBITDA/EV + 5-Day Mean Reversion

Status: FAILED

Expression:

```text
rank(ts_rank(ebitda / enterprise_value, 126))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.51
Fitness: 0.98
```

Conclusion:

- Very close, but missed Fitness by about 0.02.
- This is a strong family, but exact expression should not be repeated.

