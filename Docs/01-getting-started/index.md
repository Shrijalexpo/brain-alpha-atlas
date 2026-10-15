# 01 — Getting Started with WorldQuant BRAIN

## 1. Learning Objectives

By completing this module, you will be able to:

- Explain how the WorldQuant BRAIN simulation platform converts an Alpha expression into daily long/short equity portfolio weights.
- Follow the official 10-step beginner onboarding sequence from first login to first submitted Alpha.
- Distinguish between the user-level **WorldQuant Challenge** track and the **BRAIN Research Consultant** track.
- Run and interpret your first baseline simulation (`-returns` and `rank(-returns)`).

## 2. Prerequisites

- None. This is the entry point for new WorldQuant BRAIN users and newly onboarded consultants.

## 3. Core Concepts

### What is WorldQuant BRAIN?

WorldQuant BRAIN is a web-based quantitative research and backtesting simulator (`[Platform]`). Researchers write mathematical models—called **Alphas**—using historical market and fundamental datasets (`close`, `volume`, `returns`, `operating_income`, analyst estimates) and predefined transformation functions (**operators**).

For each trading day in the historical simulation period, BRAIN:

1. Evaluates your Alpha expression for every stock in the selected **Universe** (for example, `USA / TOP3000`).
2. Applies post-processing settings (**Neutralization**, **Decay**, **Pasteurization**, **Truncation**).
3. Normalizes the resulting vector so that the sum of absolute portfolio weights equals `1.0` (`sum(|w_i|) = 1.0`), allocating capital across long (`w_i > 0`) and short (`w_i < 0`) positions scaled to a `$20,000,000` reference booksize (`[Platform]`).
4. Computes daily Profit and Loss (**PnL**) and multi-year summary statistics (**Sharpe**, **Fitness**, **Turnover**, **Returns**, **Drawdown**, **Margin**).

### The Alpha Lifecycle

```text
Research Hypothesis (Economic Intuition)
  -> Select Dataset & Fields in Data Explorer
  -> Write Fast Expression Formula
  -> Configure Simulation Settings (Region, Universe, Delay, Neutralization, Decay, Truncation)
  -> Run Historical Backtest (In-Sample Period)
  -> Diagnose Metrics & Submission Checks
  -> Refine Controlled Mechanism or Discard
  -> Submit Passing Alpha to Out-of-Sample (OS) Production Pool
```

### User Track vs. Research Consultant Track

| Dimension | Challenge User Track (Bronze / Silver / Gold) | Research Consultant Track (Gold / Expert / Master / Grand Master) |
|---|---|---|
| **Primary Goal** | Learn Fast Expression, accumulate challenge points, qualify for consultant invitation | Build diversified production Alphas, SuperAlphas, Power Pool Alphas, and Pyramids |
| **Available Regions** | Primarily `USA` (plus limited starter scopes) | Unlocks `USA, EUR, ASI, GLB, IND, CHN` at Gold; `+ AMR, JPN` at Master; `+ HKG, KOR, TWN` at Grand Master (`[Platform]`) |
| **Headline Submission Gate** | `Sharpe > 1.25` (D1) / `> 2.0` (D0), `Fitness > 1.0` (D1) / `> 1.3` (D0), `Turnover 1%–70%` | Must also clear the **IS Ladder Test** (or **ATOM** 2Y Sharpe bar) and platform-wide **Prod-Correlation `<= 0.7`** (`[Platform]`) |
| **Throughput Tools** | Single simulation | **Multi-Simulation** (up to 8 concurrent batches of 10 Alphas), **Visualization Tool**, **BRAIN API / ACE Library**, **SuperAlphas** (after 100 submissions) (`[Platform]`) |

## 4. Step-by-Step Explanations: The 10-Step Starter Workflow

WorldQuant BRAIN recommends a structured 10-step onboarding progression (`[Platform]`):

1. **Complete the "Introduction to Alphas" course** in the BRAIN Learn portal to learn the simulator interface.
2. **Read the Discover BRAIN Starter Pack** articles (*Read this First — Starter Pack*, *Introduction to Alphas*, *Introduction to BRAIN Expression Language*).
3. **Simulate three simple expressions** using the price field `close` and the cross-sectional operator `rank`.
4. **Master Simulation Settings**, starting with **Delay** (`1` vs `0`) and **Neutralization** (`Market`, `Industry`, `Subindustry`).
5. **Inspect built-in Examples** via the *Example* button at the bottom-left of the Simulate page, and practice improving them using the provided hints.
6. **Study Simulation Results and Submission Tests** so you know how `Sharpe`, `Fitness`, `Turnover`, and `Sub-universe Sharpe` interact.
7. **Reproduce the guided tutorials** (*Run Your First Alpha* and *Alpha Examples for Beginners*).
8. **Check the Events calendar** for live onboarding webinars and regional advisory calls.
9. **Review the BRAIN Tips & Beginner FAQ posts** in the Community forum.
10. **Construct original Price-Volume (`pv1`) and Fundamental (`fnd6`) Alphas** using a disciplined research log.

### Consultant Onboarding Checklist (First 30 Days)

When transitioning to a Research Consultant role (`[Platform]`):

- **Conditional Access:** Alphas begin accruing credit immediately upon conditional activation, while payout disbursement requires completion of the background check and Workday banking setup (`[Platform]`).
- **30-Day Welcome Milestones:** Submit at least 10 Alphas and complete the onboarding survey within 30 days of receiving the welcome email (`[Platform]`).
- **Quarterly Recertification:** Recertify your BRAIN account every three months and keep employment and residence details current (`[Platform]`).

## 5. Working Examples

### Example 1: Naive Price Reversion (`-returns`)

- **Hypothesis:** Stocks that rose strongly yesterday may experience short-term profit-taking today, while yesterday's losers may rebound (1-day mean reversion).
- **Expression:**
  ```text
  -returns
  ```
- **Limitation:** Raw returns contain extreme outliers (such as a `+40%` earnings gap). Unranked `-returns` concentrates portfolio weight in a handful of volatile stocks.

### Example 2: Cross-Sectionally Ranked Reversion (`rank(-returns)`)

- **Hypothesis:** Ranking stocks uniformly from `0.0` (highest yesterday return, shorted) to `1.0` (lowest yesterday return, bought) preserves the mean-reversion ordering while eliminating outlier weight concentration.
- **Expression:**
  ```text
  rank(-returns)
  ```
- **Settings:** `Region = USA`, `Universe = TOP3000`, `Delay = 1`, `Decay = 4`, `Neutralization = Subindustry`, `Truncation = 0.08`, `Pasteurization = On`, `NaN Handling = Off`.

### Example 3: Smoothed 5-Day Reversal (`rank(ts_mean(-returns, 5))`)

- **Why it matters:** Single-day `-returns` flips sign every day, creating excessive daily trading (**Turnover > 70%**) that destroys **Fitness**. Averaging over 5 trading days (`ts_mean(-returns, 5)`) was the exact mechanism that turned failing value-growth composites into submittable Alphas in [`026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.html) (`[Observed]`).

## 6. Common Mistakes and Troubleshooting

- **Treating training-period metrics as final results:** Never quote `Train Sharpe` as your Alpha's Sharpe; in recorded USA sweeps they differed in `2,448` of `2,500` blocks (`[Observed]`).
- **Changing five settings at once:** Modify one variable (field, operator, window, or neutralization) per simulation so you can attribute what caused the change (`[Notes]`).
- **Sharing Alpha code or credentials:** Consultant operating rules strictly prohibit sharing exact Alpha code outside official teams or sharing account credentials (`[Platform]`).

## 7. Practical Exercises

1. Open the BRAIN simulator, set `USA / TOP3000 / Delay 1 / Subindustry / Decay 4 / Truncation 0.08`, and compare `-returns`, `rank(-returns)`, and `rank(ts_mean(-returns, 5))`.
2. Record how **Turnover** and **Fitness** change across the three runs.
3. Inspect [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/) to see how early experiments (`001`–`027`) evolved from simple momentum/reversion into multi-factor submissions.

## 8. Related Topics and Next Steps

- **Next Module:** [02 — Financial and Quantitative Foundations](../02-financial-and-quantitative-foundations/index.md)
- **Settings Reference:** [03 — WorldQuant BRAIN Fundamentals](../03-worldquant-brain-fundamentals/index.md)
- **Full Experiment Ledger:** [Master Experiment Index](../../Analysis%20and%20Simulation%20Reports/)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Discover BRAIN* series (*Read this First — Starter Pack*, *10 Steps to Start on BRAIN*, *Introduction to Alphas*) and *Starting Guide for Research Consultants* (`[Platform]`, captured 2026-07-26 and 2026-10-06/09).
- **Verification Date:** 2026-10-15.
