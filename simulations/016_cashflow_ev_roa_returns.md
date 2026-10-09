# Simulation 016 - Cash Flow Yield + ROA + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: worse than Simulation 015.
```

Conclusion:

- `return_assets` was worse than `return_equity` in this branch.
- Do not repeat this exact substitution unless testing a genuinely new transformation.

