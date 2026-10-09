# Simulation 036 - SCL12 Sentiment + Buzz

Status: FAILED

Expression:

```text
rank(ts_rank(scl12_sentiment, 126))
+ rank(ts_delta(scl12_buzz, 21))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.38
Fitness: 0.44
Turnover: 87.5%
```

Conclusion:

- Sentiment had predictive power but turnover was too high.
- Pure sentiment/buzz signals were too reactive.

