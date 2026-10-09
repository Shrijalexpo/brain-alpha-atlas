# Simulation 062 - EBITDA/EV + Close/High Behavior

Status: FAILED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(ts_mean(close / high - 1, 5))
```

Known result:

```text
Sharpe: -0.04
Fitness: -0.01
```

Conclusion:

- Dead branch. Close/high behavior did not work here.

