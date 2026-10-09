# Simulation 018 - Cash Flow Yield + ROE + ROA + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(return_assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: worse than the prior best branch.
```

Conclusion:

- Stacking similar profitability factors hurt performance.
- Avoid adding both `return_equity` and `return_assets` to this branch without a new reason.

