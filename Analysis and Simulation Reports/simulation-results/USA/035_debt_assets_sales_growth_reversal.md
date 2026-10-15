# Simulation 035 - Debt/Assets + Sales Growth + Reversal

Status: FAILED

Expression:

```text
group_neutralize(
    rank(ts_rank(debt / assets, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Sharpe: 0.91
```

Conclusion:

- Leverage plus growth was still weak.
- Liquidity/leverage family was not promising on USA TOP3000 D1 in these tests.

## Standardized Research Record Metadata

| Metadata Field | Recorded Value |
|---|---|
| **Experiment / Record ID** | `035` |
| **Record Type** | `Single Alpha Simulation` |
| **Source Dataset / Fields** | Company Fundamentals (fnd6) + Price/Volume (pv1) |
| **Region / Delay / Universe** | `USA (workspace default)` · Delay `1` · `TOP3000 (workspace default)` |
| **Neutralization / Decay / Truncation** | `Subindustry / Market (workspace default)` · Decay `4 (workspace default)` · Truncation `0.08` |
| **Simulation / Capture Date** | `2026-07 to 2026-10` |
| **Recorded Metrics (OOS / IS)** | Sharpe: `0.91` · Fitness: `unknown` · Turnover: `unknown` · Returns: `unknown` · Drawdown: `unknown` · Margin: `unknown` · Sub-universe Sharpe: `unknown` |
| **Check Verdict & Failure Reasons** | Status `FAILED` · Checks: `FAILED one or more checks` · Self-correlation: `unknown` |
| **Power Pool / Cluster / ATOM Match** | `Multi-dataset or standard user-level test; not verified against Power Pool or Cluster theme` |
| **Canonical File Path** | `Analysis and Simulation Reports/simulation-results/USA/035_debt_assets_sales_growth_reversal.md` |

