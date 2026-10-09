# Simulation 022 - EBITDA Yield + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ebitda / enterprise_value)
    + rank(sales_growth)
    + rank(-returns),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 1.21
Sub-universe Sharpe: 1.26
```

Conclusion:

- Sharpe did not improve versus cashflow/EV, but Sub-universe Sharpe improved.
- EBITDA/EV looked like a better robustness base than cashflow/EV.
- Failed overall; do not suggest exact expression again.

