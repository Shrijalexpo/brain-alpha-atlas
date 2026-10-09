# Simulation 066 - Operating Cash Flow Estimate Dispersion Level + Reversal

Status: FAILED

Expression:

```text
zscore(
    rank(ts_rank(op_cash_flow_stddev, 63))
    + 0.3 * rank(ts_mean(-returns, 5))
)
```

Settings:

```text
Instrument Type: Equity
Region: USA
Universe: TOP3000
Language: Fast Expression
Delay: 1
Decay: 6
Truncation: 0.08
Neutralization: Subindustry
Pasteurization: On
Unit Handling: Verify
NaN Handling: Off
Test Period:
```

Known result:

```text
Alpha ID: 58kKgvgn
Sharpe: 1.16
Fitness: 0.78
Returns:
Turnover: 13.12%
Drawdown:
Margin:
Sub-universe Sharpe: 0.92
Self-correlation:
Checks: 5 PASS, 2 FAIL, 1 PENDING
Error:
```

Conclusion:

- Failed on Sharpe and Fitness.
- Turnover was acceptable, but the level/rank version was weaker than the 10-day delta version.

Lesson:

- `op_cash_flow_stddev` appears better as a recent change/impulse signal than as a medium-term relative level.
- Do not prioritize this level-rank branch unless later evidence supports it.

Next action:

- Continue from Simulation 065 rather than this backup branch.
