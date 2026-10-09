# Simulation 025 - Time-Series Ranked EBITDA Yield + Time-Series Ranked Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.78
Fitness: 0.97
Sub-universe Sharpe: 1.78
```

Conclusion:

- Very strong, but still not submittable because Fitness was just below 1.
- Time-series ranking `sales_growth` was a major improvement.
- Exact expression should not be repeated; use only as the direct parent of the submitted alpha.

