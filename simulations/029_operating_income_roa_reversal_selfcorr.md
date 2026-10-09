# Simulation 029 - Operating Income Quality + ROA Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(return_assets, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.76
Fitness: 1.21
Turnover: 18.73%
Sub-universe Sharpe: 1.37
Self-correlation: 0.8817
Self-correlation cutoff: 0.70
```

Conclusion:

- Performance passed, but self-correlation failed.
- The backbone was too similar to existing submitted alphas.
- Avoid this exact structure.

