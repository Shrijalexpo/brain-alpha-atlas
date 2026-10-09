# Simulation 060 - EBITDA/EV + Low Historical Volatility

Status: FAILED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(-historical_volatility_120)
```

Known result:

```text
Sharpe: 0.06
Fitness: 0.02
```

Conclusion:

- Dead branch. Low volatility did not complement EBITDA/EV.

