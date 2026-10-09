# Simulation 049 - Operating Income + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    zscore(
        rank(operating_income)
        + rank(-returns)
    ),
    industry
)
```

Known result:

```text
Sharpe: 0.95
Fitness: 0.66
```

Conclusion:

- Best of that small fundamental batch, but still weak.
- Raw operating income remained unreliable.

