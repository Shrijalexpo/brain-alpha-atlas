# Simulation 056 - Long Lookback Cashflow Quality + Operating Improvement

Status: FAILED

Expression:

```text
rank(ts_rank(cashflow_op / assets, 252))
+ rank(ts_delta(operating_income / assets, 126))
```

Known result:

```text
Sharpe: 1.35
Fitness: 0.89
```

Conclusion:

- Close, but still failed Fitness.
- Longer lookbacks helped but did not make the alpha submittable.

