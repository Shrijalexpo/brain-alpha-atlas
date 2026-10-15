# 06 — Alpha Research and Construction

## 1. Learning Objectives

By completing this module, you will be able to:

- Execute the 6-step disciplined Alpha research loop (`Hypothesis -> Field Inspection -> Baseline -> Bottleneck Diagnosis -> Single Controlled Change -> Record`).
- Construct clean single-dataset (**ATOM**) and multi-factor composite Alphas without diluting signal strength.
- Apply the **One-Minute Explainability Rule** and avoid overfitting traps before running simulations.

## 2. Prerequisites

- [04 — Data Explorer and Datasets](../04-data-explorer-and-datasets/index.md)
- [05 — Fast Expression Language](../05-fast-expression-language/index.md)

## 3. Core Concepts: The Disciplined Research Loop

Quantitative alpha research fails when treated as random formula generation (`[Notes]`). In this repository, **13,319 automated single-field sweep blocks produced 0 submittable Alphas**, whereas **small, deliberate hypothesis-driven iterations produced all 3 passing/submitted Alphas** (`026`, `027`, `053`) (`[Observed]`).

```text
1. Economic Hypothesis   Write one sentence explaining who is on the other side of the trade and why.
2. Field Selection       Pick 1 primary field (Matrix, coverage >= 70%, long history) + size/value denominator.
3. Baseline Simulation   Run the simplest normalized expression (e.g. rank(a / b) or ts_rank(a / b, 126)).
4. Bottleneck Diagnosis  Identify the single binding failure: Sharpe, Fitness, Turnover, Sub-universe, or Weight.
5. One Controlled Change Modify ONE mechanism (transform, window, complement, or smoothing) to address that bottleneck.
6. Record in Ledger      Log expression, settings, metrics, failed checks, and lesson before testing the next idea.
```

### The One-Minute Explainability Rule

WorldQuant BRAIN's consultant guidelines state a simple test (`[Platform]`):

> **Can you explain the economic rationale of your Alpha and the role of every operator in under one minute?**

If an expression contains an arbitrary lookback like `37` days, four nested `if_else` branches, or an unmotivated product of unrelated fields, remove the complexity (`[Platform]`). Restrict lookback windows to economically meaningful horizons (`[Platform]`):

| Window (Trading Days) | Calendar Equivalent | Economic Meaning |
|---:|---|---|
| `5` | 1 trading week | Short-term weekly price/liquidity mean reversion |
| `20` or `21` | 1 trading month | Monthly revision, volume participation, or monthly backfill |
| `60` or `63` | 1 fiscal quarter | Quarterly earnings/sales reporting cycle and quarterly estimate scaling |
| `120` or `126` | Half year (2 quarters) | Semi-annual fundamental trajectory |
| `250` or `252` | 1 trading year (4 quarters) | Annual fundamental rank or 52-week price/volume anchor |

## 4. Step-by-Step Explanations: Building From Baseline to Composite

### Step 1: Isolate and Test the Base Signal Alone

Before combining three factors, simulate the primary factor by itself (`[Notes]`):

- **Bad start:** Jumping straight to `rank(a) + rank(b) + rank(c) + rank(d) - rank(e)` (Simulation [`012`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/012_large_multifactor_quality_value.md), Sharpe `-0.28`, `[Observed]`).
- **Good start:** Testing `rank(cashflow_op / enterprise_value)` alone in Simulation [`014`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/014_cashflow_yield.md) (`Sharpe 0.41`, positive baseline, `[Observed]`), then comparing `ebitda / enterprise_value` (`[Observed]`).

### Step 2: Upgrade the Normalization Before Adding Factors

Often a fundamental ratio looks weak in static cross-sectional `rank(x)` because industries or companies have persistent structural valuation differences. Switching from static `rank(ebitda / enterprise_value)` to **time-series rank** `rank(ts_rank(ebitda / enterprise_value, 126))` (asking whether the firm is cheap *relative to its own 6-month history*) jumped Sharpe from `1.21` (`022`) to `1.36` (`024`) (`[Observed]`).

### Step 3: Add At Most One Orthogonal Complement at a Time

When combining signals, pair **different economic mechanisms** or **different horizons**, never three versions of the same accounting ratio (`[Observed]`):

- **Redundant stacking (fails):** `ROE + ROA + operating_income/assets` (all measure current profitability; Simulations `016`–`019` degraded performance, `[Observed]`).
- **Orthogonal pairing (works):**
  1. **Value level/trajectory:** `rank(ts_rank(ebitda / enterprise_value, 126))` (6-month horizon)
  2. **Fundamental growth:** `rank(ts_rank(sales_growth, 126))` (6-month horizon, prevents value traps)
  3. **Smoothed price entry timing:** `rank(ts_mean(-returns, 5))` (1-week mean reversion)

## 5. Working Examples

### Example 1: Single-Dataset Analyst Alpha (ATOM Candidate in `EUR` / `KOR`)

```text
/* Single dataset (anl69): backfill quarterly gaps over 21 days and scale over 1 quarter (63 days) */
ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)
```
- **Why this structure is strong:** Uses only 1 dataset (`anl69`) and 2 operators (`ts_backfill` is free), qualifying for both **ATOM** relaxed submission tests and **Power Pool** simplicity rules (`[Platform]`, `[Observed]`).

### Example 2: Three-Leg Value + Growth + Smoothed Reversal Composite (`USA`)

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```
- **Recorded Result (Simulation [`026`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md)):** Sharpe `1.61`, Fitness `1.02`, Turnover `25.25%`, Sub-universe Sharpe `1.53` (`[Observed]`). *(Protected baseline — do not re-submit verbatim.)*

## 6. Common Mistakes and Troubleshooting

- **Injecting random noise to lower correlation:** Strictly prohibited by WorldQuant BRAIN compliance rules and grounds for account termination (`[Platform]`). Lower correlation legitimately by exploring less-crowded regions (`EUR`, `GLB`, `KOR`, `AMR`), single-dataset ATOM structures, or underutilized dataset categories.
- **Re-testing already-exhausted expressions:** Always check [`status-and-duplicate-ledger.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/status-and-duplicate-ledger.md) before running a simulation (`[Notes]`).

## 7. Practical Exercises

1. Pick one dataset family in `EUR` (`anl69` or `anl4`) and draft a 1-sentence hypothesis and a 1-line baseline expression using only standard lookbacks (`21`, `63`, `126`, or `252`).
2. Check your candidate against [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/index.md) to verify it has not already been simulated.

## 8. Related Topics and Next Steps

- **Next Module:** [07 — Simulation and Evaluation](../07-simulation-and-evaluation/index.md)
- **Methodology Rules:** [16 — Quantitative Research Methodology](../16-quantitative-research-methodology/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Simulate Your First Alpha*, *Alpha Examples for Beginners/Bronze/Silver*, and *Consultant Dos and Don'ts* (`[Platform]`, captured 2026-07-26 and 2026-10-06/09); empirical records `001`–`071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
