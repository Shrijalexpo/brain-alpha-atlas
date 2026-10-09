# Simulation 030 - Operating Income Quality + ROA Trend + 20-Day Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(return_assets, 126))
    + rank(ts_mean(-returns, 20)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.19
```

Conclusion:

- Longer mean-reversion window reduced signal strength.
- Failed to preserve the strong performance of Simulation 029.

