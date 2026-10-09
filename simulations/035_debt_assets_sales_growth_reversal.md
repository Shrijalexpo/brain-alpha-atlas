# Simulation 035 - Debt/Assets + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(debt / assets, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.91
```

Conclusion:

- Leverage plus growth was still weak.
- Liquidity/leverage family was not promising on USA TOP3000 D1 in these tests.

