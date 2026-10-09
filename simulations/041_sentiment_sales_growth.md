# Simulation 041 - Sentiment + Sales Growth

Status: FAILED

Expression:

```text
rank(ts_rank(scl12_sentiment, 252))
+ rank(ts_delta(sales_growth, 63))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.04
Fitness: 0.36
```

Conclusion:

- Weak and noisy.
- Sentiment dataset was paused after this branch.

