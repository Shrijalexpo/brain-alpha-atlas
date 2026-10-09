# Simulation 065 - Operating Cash Flow Estimate Dispersion + Sales Growth + Reversal

Status: FAILED

Expression:

```text
zscore(
    rank(ts_delta(op_cash_flow_stddev, 10))
    + 0.4 * rank(ts_rank(sales_growth, 126))
    + 0.2 * rank(ts_mean(-returns, 5))
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
Alpha ID: MPLv3QPz
Sharpe: 1.48
Fitness: 0.91
Returns:
Turnover: 21.78%
Drawdown:
Margin:
Sub-universe Sharpe: 1.49
Self-correlation:
Checks: 6 PASS, 1 FAIL, 1 PENDING
Error:
```

Conclusion:

- Failed only on Fitness.
- Sharpe, turnover, weight distribution, sub-universe Sharpe, and challenge checks passed.
- This is a strong repair versus Simulation 064 and confirms the faster `op_cash_flow_stddev` impulse is useful.

Lesson:

- Replacing the `volume / adv20` leg with `ts_rank(sales_growth, 126)` improved robustness while keeping turnover reasonable.
- The next fix should aim to lift Fitness slightly, either by reducing turnover or raising returns, without over-smoothing the 10-day dispersion component.

Next action:

- Try a small coefficient/window adjustment before abandoning this branch.
