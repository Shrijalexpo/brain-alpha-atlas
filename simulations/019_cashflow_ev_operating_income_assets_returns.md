# Simulation 019 - Cash Flow Yield + Operating Income / Assets + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(operating_income / assets)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: plateaued or worse than the prior best branch.
```

Conclusion:

- Replacing ROE/ROA with `operating_income / assets` did not solve the problem.
- This reinforced the lesson that the operating-income family was weak in the tested setup.

