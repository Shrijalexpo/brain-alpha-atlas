# Simulation 028 - Growth Acceleration + Liquidity + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(current_ratio, 126))
    + rank(ts_delta(sales_growth, 63))
    + rank(ts_mean(-returns, 10)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.87
Fitness: 0.47
Turnover: 16.47%
Sub-universe Sharpe: 0.60
```

Conclusion:

- Different factor family, but too weak.
- Liquidity plus growth acceleration was not strong enough.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `028` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.87` · Fitness: `0.47` · Turnover: `16.47%` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `0.60` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/028_growth_liquidity_reversal.md` |

