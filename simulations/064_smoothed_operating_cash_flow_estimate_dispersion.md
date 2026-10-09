# Simulation 064 - Smoothed Operating Cash Flow Estimate Dispersion

Status: FAILED

Expression:

```text
zscore(
    rank(ts_mean(ts_delta(op_cash_flow_stddev, 20), 20))
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
Decay: 8
Truncation: 0.08
Neutralization: Subindustry
Pasteurization: On
Unit Handling: Verify
NaN Handling: Off
Test Period:
```

Known result:

```text
Alpha ID: QP9RKk95
Sharpe: 0.85
Fitness: 0.48
Returns:
Turnover: 11.81%
Drawdown:
Margin:
Sub-universe Sharpe: 0.55
Self-correlation:
Checks: 5 PASS, 2 FAIL
Error:
```

Conclusion:

- Failed because Sharpe and Fitness were both below threshold.
- Turnover, weight distribution, sub-universe Sharpe, and competition challenge checks passed.
- The 20-day delta averaged over 20 days slowed the signal too much and removed useful predictive edge from Simulation 063.

Lesson:

- The `op_cash_flow_stddev` branch seems sensitive to over-smoothing.
- Do not repeat this exact smoothed expression.
- Future fixes should keep a faster dispersion impulse or add a stronger orthogonal anchor, rather than simply increasing smoothing.

Next action:

- Try a controlled variant that keeps the 10-day dispersion change from Simulation 063 but replaces the high-turnover volume leg with a slower fundamental/value anchor.
