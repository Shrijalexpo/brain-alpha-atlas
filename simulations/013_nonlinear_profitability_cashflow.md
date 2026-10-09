# Simulation 013 - Nonlinear Profitability Cash Flow Product

Status: FAILED

Expression:

```text
group_neutralize(
    rank((return_equity * cashflow_op) / (assets * enterprise_value))
    - rank(debt / assets),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: -1.01
```

Conclusion:

- Nonlinear multiplication made performance much worse.
