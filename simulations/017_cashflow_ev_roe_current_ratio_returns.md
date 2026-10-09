# Simulation 017 - Cash Flow Yield + ROE + Current Ratio + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value)
    + rank(return_equity)
    + rank(current_ratio)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.19
Fitness: 0.66
```

Conclusion:

- Slight Sharpe improvement versus Simulation 015, but Fitness fell.
- `current_ratio` did not help enough in this factor family.
- Do not suggest this exact alpha again.

