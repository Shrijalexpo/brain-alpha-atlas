# Simulation 026 - Submitted Alpha: TS-Ranked Value + TS-Ranked Growth + Smoothed Reversal

Status: PASSED_SUBMITTABLE

Expression:

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.61
Fitness: 1.02
Turnover: 25.25%
Sub-universe Sharpe: 1.53
Competition Challenge: Passed
Self-correlation: pending at screenshot time
```

Conclusion:

- This is the first recorded submittable alpha.
- Smoothing the reversal component with `ts_mean(-returns, 5)` pushed Fitness above 1.
- Do not suggest this exact alpha again. Treat it as a protected submitted baseline.

