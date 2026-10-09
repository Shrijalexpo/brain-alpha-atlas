# Simulation 053 - Submitted EBITDA/EV + 5-Day Mean Reversion

Status: PASSED_SUBMITTED

Expression:

```text
rank(ebitda / enterprise_value)
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.46
Fitness: 1.05
Submission: Passed and submitted
```

Conclusion:

- Simple value plus short-term mean reversion worked.
- Do not suggest this exact expression again.

