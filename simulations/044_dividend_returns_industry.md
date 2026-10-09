# Simulation 044 - Dividend + Return Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(dividend)
        + 0.5 * rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 1.50
Fitness: 0.83
Sub-universe Sharpe: 1.22
Later retest: Sharpe 1.47, Fitness 0.82, Turnover 59.5%
```

Conclusion:

- Strong Sharpe, but Fitness failed.
- Settings alone were not enough to fix it.

