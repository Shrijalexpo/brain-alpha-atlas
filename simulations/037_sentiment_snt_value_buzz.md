# Simulation 037 - SNT Value + SNT Buzz

Status: FAILED

Expression:

```text
rank(ts_rank(snt_value, 126))
+ rank(ts_rank(snt_buzz, 63))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.31
Fitness: 0.52
```

Conclusion:

- Better than fast sentiment, but still failed Fitness.
- Sentiment remained too noisy.

