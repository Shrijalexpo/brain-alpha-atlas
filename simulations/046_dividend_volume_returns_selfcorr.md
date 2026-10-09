# Simulation 046 - Dividend + Volume Surprise + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + rank(volume / adv20)
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 1.86
Fitness: 1.07
Self-correlation: 0.935
```

Conclusion:

- Strong performance, but failed self-correlation.
- Volume/ADV20 was powerful but crowded with existing signals.

