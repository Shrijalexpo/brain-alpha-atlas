# Simulation 063 - High-Turnover Operating Cash Flow Estimate Stddev

Status: FAILED

Expression:

```text
zscore(
    rank(ts_delta(op_cash_flow_stddev, 10))
    + 0.4 * rank(volume / adv20)
    - 0.2 * rank(returns)
)
```

Known result:

```text
Sharpe: 1.52
Fitness: 0.84
```

Conclusion:

- Strong Sharpe but failed Fitness.
- Needs smoothing or persistence, but exact expression should not be repeated.

