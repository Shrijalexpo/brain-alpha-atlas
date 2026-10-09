# Simulation 034 - Current Ratio + Sales Growth + Reversal

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
Sharpe: 0.66
```

Conclusion:

- Liquidity family was weak.
- Do not prioritize `current_ratio` as the main signal in this setup.

