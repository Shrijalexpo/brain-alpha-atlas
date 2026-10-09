# Simulation 023 - EBITDA Yield + ROE + Sales Growth

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ebitda / enterprise_value)
    + rank(return_equity)
    + rank(sales_growth),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.28
```

Conclusion:

- Replacing `-returns` with `return_equity` badly hurt performance.
- In this branch, `return_equity` should not replace the reversal component.

