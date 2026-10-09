# Simulation 032 - Operating Income Quality + Current Ratio Trend + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(current_ratio, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.50
Fitness: 0.96
```

Conclusion:

- Almost passed, but Fitness missed.
- More distinct than ROA variants, but still not enough.

