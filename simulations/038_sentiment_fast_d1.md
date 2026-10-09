# Simulation 038 - Fast D1 Sentiment

Status: FAILED

Expression:

```text
rank(ts_delta(scl12_sentiment_fast_d1, 10))
+ rank(ts_rank(scl12_buzz_fast_d1, 63))
+ rank(ts_mean(-returns, 5))
```

Known result:

```text
Sharpe: 1.11
Turnover: 87%
```

Conclusion:

- Fast D1 sentiment fields produced very high turnover.
- Avoid `*_fast_d1` sentiment fields for now.

