# Simulation 015 - Cash Flow Yield + ROE + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.18
Fitness: 0.71
Turnover: 30.35%
Sub-universe Sharpe: 0.72
```

Conclusion:

- Close, but not submittable.
- Adding `-returns` materially improved the cashflow/value branch.
- Keep as a useful ancestor, but do not suggest this exact alpha again.

