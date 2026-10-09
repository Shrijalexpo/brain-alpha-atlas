# Simulation 020 - Cash Flow Yield + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.21
Fitness: 0.58
```

Conclusion:

- Closest cashflow/value branch before switching to EBITDA/EV.
- `sales_growth` helped more than the extra profitability factors.
- Failed Fitness; do not repeat exact expression.

