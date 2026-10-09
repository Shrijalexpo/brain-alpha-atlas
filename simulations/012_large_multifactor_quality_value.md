# Simulation 012 - Large Multi-Factor Quality/Value Composite

Status: FAILED

Expression:

```text
group_neutralize(
      rank(return_equity)
    + rank(return_assets)
    + rank(cashflow_op / assets)
    + rank(current_ratio)
    + rank(sales_growth)
    - rank(debt / assets)
    - rank(enterprise_value / ebitda),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: -0.28
```

Conclusion:

- Large linear stacking made performance worse.
