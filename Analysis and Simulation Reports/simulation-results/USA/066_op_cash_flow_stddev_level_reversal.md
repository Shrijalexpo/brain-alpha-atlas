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

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `066` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Analyst / Cashflow Estimate Dispersion |
| **Region / Delay / Universe** | `USA` · Delay `1` · `TOP3000` |
| **Neutralization / Decay / Truncation** | `Subindustry` · Decay `6` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `1.16` · Fitness: `0.78` · Turnover: `13.12%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.92` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `5 PASS, 2 FAIL, 1 PENDING` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/066_op_cash_flow_stddev_level_reversal.md` |

