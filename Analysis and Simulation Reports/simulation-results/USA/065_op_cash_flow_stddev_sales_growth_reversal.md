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

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `065` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst / Cashflow Estimate Dispersion |
| **Region / Delay / Universe** | `USA` · Delay `1` · `TOP3000` |
| **Neutralization / Decay / Truncation** | `Subindustry` · Decay `6` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.48` · Fitness: `0.91` · Turnover: `21.78%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `1.49` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `6 PASS, 1 FAIL, 1 PENDING` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/065_op_cash_flow_stddev_sales_growth_reversal.md` |

