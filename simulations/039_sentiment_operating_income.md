# Simulation 039 - Sentiment + Operating Income Quality

Status: FAILED

Expression:

```text
rank(ts_rank(scl12_sentiment, 252))
+ rank(ts_rank(operating_income / assets, 126))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.59
Fitness: 0.68
```

Conclusion:

- Good Sharpe but failed Fitness.
- Mixing sentiment with slower fundamentals still did not pass.

