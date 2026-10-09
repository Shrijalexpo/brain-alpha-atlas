# Simulation 024 - Time-Series Ranked EBITDA Yield + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.36
Fitness: 0.68
Sub-universe Sharpe: 1.39
```

Conclusion:

- First branch to pass the Sharpe threshold.
- Fitness still failed, so the signal needed smoother/more robust components.
- Time-series rank on `ebitda / enterprise_value` was a major improvement.

