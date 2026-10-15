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

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `064` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst / Cashflow Estimate Dispersion |
| **Region / Delay / Universe** | `USA` · Delay `1` · `TOP3000` |
| **Neutralization / Decay / Truncation** | `Subindustry` · Decay `8` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.85` · Fitness: `0.48` · Turnover: `11.81%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.55` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `5 PASS, 2 FAIL` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/064_smoothed_operating_cash_flow_estimate_dispersion.md` |

