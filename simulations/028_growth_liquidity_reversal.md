# Simulation 028 - Growth Acceleration + Liquidity + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(current_ratio, 126))
    + rank(ts_delta(sales_growth, 63))
    + rank(ts_mean(-returns, 10)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.87
Fitness: 0.47
Turnover: 16.47%
Sub-universe Sharpe: 0.60
```

Conclusion:

- Different factor family, but too weak.
- Liquidity plus growth acceleration was not strong enough.

