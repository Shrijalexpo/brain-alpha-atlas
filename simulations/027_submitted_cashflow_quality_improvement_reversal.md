# Simulation 027 - Submitted Cashflow Quality + Operating Improvement + Reversal

Status: PASSED_SUBMITTED

Expression:

```text
group_neutralize(
    rank(ts_rank(cashflow_op / assets, 126))
    + rank(ts_delta(operating_income / assets, 63))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.39
Fitness: 0.73 in IS summary
Turnover: 21.31%
Returns: 5.85%
Submission: Successfully submitted according to shared result
```

Conclusion:

- This became a submitted alpha.
- It uses a quality/improvement backbone plus the recurring 5-day mean-reversion component.
- Do not suggest this exact expression again.

