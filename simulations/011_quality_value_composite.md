# Simulation 011 - Quality Value Composite

Status: FAILED

Expression:

```text
group_neutralize(
    rank(return_equity)
    + rank(cashflow_op / assets)
    - rank(enterprise_value / ebitda),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: 0.46
Fitness: 0.22
Turnover: 3.98%
Sub-universe Sharpe: 0.39
```

Conclusion:

- Structural checks were acceptable.
- Signal was too weak.
