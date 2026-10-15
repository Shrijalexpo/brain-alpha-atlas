# 11 — Osmosis Allocation and Consultant Compensation

## 1. Learning Objectives

By completing this module, you will be able to:

- Configure **Osmosis** point allocations across your submitted Alpha pool (`>= 3` scopes, exactly `100,000` points across `>= 10` Alphas per scope).
- Understand the Sunday `23:59 EST` lock schedule, the **Daily Osmosis Rank** (quality multiplier `1.0` to `2.0`), and quarterly **Combined Osmosis Performance**.
- Apply portfolio-construction rules (turnover bucketing, dataset/neutralization diversification, and the `60%` investability-constrained Sharpe drop cutoff) when assigning Osmosis weights.
- Explain how **Quantity Factor** and **Quality Factor** interact in the consultant base-fee methodology.

## 2. Prerequisites

- [10 — Pyramids and the BRAIN Genius Program](../10-pyramids-and-genius-program/index.md)

## 3. Core Concepts

### What is Osmosis?

**Osmosis** is a consultant's personal meta-portfolio (combo) of submitted Alphas (`[Platform]`). Instead of relying solely on an equal-weighted average of your submissions, Osmosis lets you allocate custom weights (**Osmosis Points**) to your best, most diversified Alphas within each **scope (`Region x Delay`)** (`[Platform]`).

The platform computes the daily out-of-sample PnL of your Osmosis combo and uses it in three ways (`[Platform]`):

1. **Daily Base-Payment Quality Multiplier (`1.0` to `2.0`):** Driven by your **Daily Osmosis Rank** on the consultant leaderboard.
2. **Combined Osmosis Performance (Genius Dashboard):** One of the four quarterly combined performance metrics used for Genius tier qualification and quarterly payment evaluation.
3. **Leaderboard Visibility:** Reported daily as your **Daily Osmosis Rank**.

### Hard Allocation Requirements

To have a valid Osmosis allocation (`[Platform]`):

| Requirement | Exact Rule (`[Platform]`) |
|---|---|
| **Minimum Active Scopes** | Allocate points to **at least 3 distinct scopes** (`Region x Delay`, e.g., `USA D1`, `EUR D1`, `GLB D1`) permitted by your Genius level |
| **Minimum Alphas per Scope** | Allocate positive points to **at least 10 submitted Alphas** within each active scope |
| **Total Points per Scope** | Points within **each** active scope must sum to **exactly `100,000` points** |
| **Eligible Alphas** | All Alpha types (`Regular`, `ATOM`, `Power Pool`) and all historical submission dates are eligible |
| **Weekly Lock Schedule** | Allocations lock every **Sunday at `23:59 EST`** and take effect for daily combo calculations roughly one week later |
| **Daily Osmosis Rank Lag** | Today's Daily Osmosis Rank reflects the locked allocation from **two Sundays ago** |
| **Quarterly Genius Requirement** | Combined Osmosis Performance requires valid allocations across **at least 6 weeks within the previous 3 months** (updates every 4–6 weeks) |

### Consultant Compensation Structure Overview

Consultant merit-based payments consist of two main pillars (`[Platform]`):

1. **Periodic Base Payments:** Driven by a **Quantity Factor** (daily submission utilization up to the daily quota of 4 Alphas + 1 SuperAlpha) and a **Quality Factor** (enhanced by Dynamic Pyramid Multipliers, Theme Multipliers, region/universe/correlation multipliers, and the Osmosis quality multiplier between `1.0` and `2.0`) (`[Platform]`).
2. **Quarterly Genius & Performance Payments:** Driven by Genius tier (`Gold`, `Expert`, `Master`, `Grand Master`) and Combined Alpha / Osmosis Out-of-Sample Performance (`[Platform]`).

*(Note: Specific commercial terms are governed by each consultant's individual agreement; historical backtest metrics never guarantee any level of compensation, `[Platform]`, `[Notes]`.)*

## 4. Step-by-Step Explanations: Managing Osmosis Allocations

### Step 1: Three Ways to Allocate Osmosis Points in the UI

On the **Alphas -> Submitted** tab (`[Platform]`):

1. **Inline Table Editing:** Hover over the `Osmosis Points` cell in the Submitted Alphas table, click the edit icon, and type the point value.
   - A **green checkmark** means the cell edit saved to the database; it does **not** verify that your scope totals `100,000` or has `>= 10` Alphas (`[Platform]`).
   - A **red warning icon** indicates a save error (hover for tooltip details).
2. **Alpha Properties Panel:** Open an individual Alpha and set its Osmosis points in the bottom Properties section.
3. **The `Osmosis Scale` Button:** Located next to the `Filter` button on the Submitted tab (`[Platform]`):
   - Enabled **only** when a scope has `>= 10` Alphas with non-zero points whose sum is not yet `100,000`.
   - Clicking **`Scale All to 100,000`** proportionally rescales your assigned points in every eligible scope so each scope sums to exactly `100,000` in one click (`[Platform]`).

### Step 2: Portfolio Construction Rules for High Osmosis Performance

Official BRAIN Osmosis guidance recommends four quantitative selection filters when weighting your Alphas (`[Platform]`):

1. **Drop Fragile Investability Alphas (`>= 60%` Drop Rule):** Compare each Alpha's standard Sharpe against its **Investability-Constrained Sharpe**. If Sharpe drops by **`60%` or more** under investability constraints, exclude it from Osmosis (`0` points) (`[Platform]`).
2. **Bucket by Turnover Bands:** Spread your 100,000 points within each scope across three turnover buckets so transaction costs do not correlate during volatility spikes (`[Platform]`):
   - **Low Turnover:** `< 10%`
   - **Medium Turnover:** `10% – 20%`
   - **Higher Turnover:** `> 20%`
3. **Diversify Datasets, Operators, and Neutralizations:** Do not assign 100,000 points to 10 slight variations of `ebitda / enterprise_value`. Mix Fundamental (`fnd6`), Analyst (`anl69`, `anl4`), Option (`option6`), and Price-Volume (`pv1`) Alphas across `Industry`, `Subindustry`, `Country`, and Risk neutralizations (`[Platform]`).
4. **Weight by Out-of-Sample Stability:** Favor Alphas with steady post-submission OS PnL and low pairwise correlation.

## 5. Working Examples: Strategic Gap Analysis for This Workspace

Let us compare our current repository state against the Osmosis requirements (`[Observed]`, `[Notes]`):

| Scope (`Region x Delay`) | Submitted Alphas Required | Currently Submitted in Ledger | Action Needed to Unlock Osmosis |
|---|---:|---:|---|
| `USA / D1` | `>= 10` | `2` submitted (`027, 053`) + `1` submittable (`026`) | Need `7–8` additional uncorrelated `USA / D1` submissions |
| `EUR / D1` | `>= 10` | `0` (`5,364` sweep blocks mapped) | Convert top `EUR` `anl69` / `pv37` sweep candidates into `10` passing ATOM / Power Pool submissions |
| `GLB / D1` (or `KOR / D1`, `AMR / D1`) | `>= 10` | `0` (`789` KOR, `3,250` AMR, `192` ALL blocks mapped) | Build `10` submissions in a third scope (`GLB / D1` or `KOR / D1`) to satisfy the **3-scope minimum** |

## 6. Common Mistakes and Troubleshooting

- **Assuming the green checkmark means a valid 100,000-point scope:** The green checkmark only confirms the single row update succeeded. Always click `Osmosis Scale` or verify that each of your `>= 3` scopes has `>= 10` Alphas totaling `100,000` points before Sunday `23:59 EST` (`[Platform]`).
- **Concentrating 100% of research in `USA / D1`:** A consultant with 50 Alphas in `USA / D1` and 0 in other scopes **cannot activate Osmosis** because Osmosis strictly requires at least **3 distinct scopes** (`[Platform]`).

## 7. Practical Exercises

1. Suppose you select 12 Alphas in `EUR / D1`: 4 low-turnover Alphas (`< 10%`) given `12,000` points each, 4 medium-turnover Alphas (`10%–20%`) given `8,000` points each, and 4 higher-turnover Alphas (`> 20%`) given `5,000` points each. Verify that the total equals $4(12,000) + 4(8,000) + 4(5,000) = 100,000$ points across $12 \ge 10$ Alphas.

## 8. Related Topics and Next Steps

- **Next Module:** [12 — Advanced Alpha Research](../12-advanced-alpha-research/index.md)
- **Multi-Region Expansion:** [13 — Region-Agnostic and Cluster Alphas](../13-region-agnostic-and-cluster-alphas/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Osmosis Allocation Guide for Consultants* (`osmosis-allocation-guide-consultants`), *Starting Guide for Research Consultants*, and *India WorldQuant BRAIN Base Fee Guide* (`[Platform]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
