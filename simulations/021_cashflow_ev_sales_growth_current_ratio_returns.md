# Simulation 021 - Cash Flow Yield + Sales Growth + Current Ratio + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(sales_growth)
    + rank(current_ratio)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: worse than Simulation 020.
```

Conclusion:

- `current_ratio` hurt the best cashflow/value-growth branch.
- Do not suggest this exact alpha again.

