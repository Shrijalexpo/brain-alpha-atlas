# Simulation 054 - Cashflow Quality + Operating Improvement Without Reversal

Status: FAILED

Expression:

```text
rank(ts_rank(cashflow_op / assets, 126))
+ rank(ts_delta(operating_income / assets, 63))
```

Known result:

```text
Sharpe: 1.29
Fitness: 0.78
```

Conclusion:

- Close but failed Fitness.
- Removing the reversal component reduced submission quality.

