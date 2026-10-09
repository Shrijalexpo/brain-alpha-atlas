# Simulation 031 - Cashflow Quality + ROA Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(cashflow_op / assets, 126))
    + rank(ts_delta(return_assets, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.71
Fitness: 1.13
Self-correlation: 0.933
```

Conclusion:

- Strong metrics, but failed self-correlation.
- `cashflow_op/assets`, `return_assets`, and `ts_mean(-returns,5)` are now crowded in the user's submitted set.

