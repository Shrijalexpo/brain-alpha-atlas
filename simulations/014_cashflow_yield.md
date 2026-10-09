# Simulation 014 - Cash Flow Yield

Status: FAILED

Expression:

```text
group_neutralize(
    rank(cashflow_op / enterprise_value),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Metrics:

```text
Sharpe: 0.41
```

Conclusion:

- Positive but weak.
- Best current base direction from the latest tests.
- Add one complementary factor at a time.
