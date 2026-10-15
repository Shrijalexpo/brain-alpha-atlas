# 10 — Pyramids and the BRAIN Genius Program

## 1. Learning Objectives

By completing this module, you will be able to:

- Explain the four consultant tiers of the **BRAIN Genius Program** (`Gold`, `Expert`, `Master`, `Grand Master`), their quarterly slot allocations (`70% / 20% / 8% / 2%`), and the data/region/SuperAlpha privileges unlocked at each tier.
- Formulate **Pyramids** (`Region x Delay x Dataset Category`, minimum 3 submitted Alphas per pyramid) to satisfy Genius eligibility and increase diversification.
- Calculate **Dynamic Pyramid Multipliers** and stacked **Theme Multipliers** (`sum of multipliers - count of themes + 1`).
- Optimize the six **Genius Tie-Breaker** metrics (`Avg distinct Operators/Alpha`, `Avg distinct Fields/Alpha`, `Total distinct Operators`, `Total distinct Fields`, `Maximum Simulation Streak`, `Community Leader`).

## 2. Prerequisites

- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)
- [09 — Power Pool and Thematic Competitions](../09-power-pool-and-thematic-competitions/index.md)

## 3. Core Concepts

### The Four BRAIN Genius Tiers

New Research Consultants begin at **Gold** level (`[Platform]`). Levels are evaluated quarterly (taking effect in the first week of each calendar quarter), with fixed percentage slot allocations among active quarterly-payment-eligible consultants (`[Platform]`):

| Feature / Access | Gold (Default) | Expert | Master | Grand Master |
|---|---|---|---|---|
| **Quarterly Slot Share** | `70%` | `20%` | `8%` | `2%` |
| **Research Regions** | `USA, ASI, EUR, GLB, IND, CHN` | + Additional Pyramids across regions | + `AMR, JPN` | + `HKG, KOR, TWN` |
| **Data Field Access** | `50%` of available fields | `61%` | `78%` | `100%` |
| **Operator Access** | `45%` of all operators | `63%` | `78%` | `100%` |
| **SuperAlpha Component Pool** (requires `>= 100` Alpha submissions) | Own submitted Alphas only | + Consultants from your **University** | + Consultants from your **Country** | + **All Consultants** globally |
| **Biometrics Re-Auth Interval** | Every `4 hours` | Every `6 hours` | Every `12 hours` | Every `24 hours` |

> **Downgrade Caveat:** If you move to a lower level in a subsequent quarter, you lose direct simulation access to higher-tier datasets, regions, and operators (preventing re-simulation of those Alphas), though previously submitted Alphas remain usable inside new SuperAlphas (`[Platform]`).

### The Three Quarterly Eligibility Criteria

To qualify for Expert, Master, or Grand Master in a calendar quarter, a consultant must clear three threshold gates (`[Platform]`):

1. **Minimum Signal Count:** Total Alphas + SuperAlphas submitted during the quarter.
2. **Minimum Formulated Pyramids:** Number of distinct **Pyramids** (`Region x Delay x Dataset Category`) containing **at least 3 submitted Alphas** (`[Platform]`).
   - *Example:* Submitting 3 Alphas in `USA - D1 - Analyst` completes 1 Pyramid. A multi-dataset Alpha using both `Fundamental` and `Analyst` fields in `EUR - D1` contributes toward both the `EUR-D1-Fundamental` and `EUR-D1-Analyst` pyramids (`[Platform]`).
3. **Minimum Combined Alpha Performance (Out-of-Sample Sharpe):** Evaluated as the **maximum** of four portfolio combinations on the Genius dashboard at quarter-end (refreshed every 4–6 weeks) (`[Platform]`):
   - Combined OS performance of **all consultant Alphas** submitted by you.
   - Combined OS performance of **all consultant Alphas selected by WorldQuant**.
   - Combined OS performance of **all Power Pool Alphas** submitted by you.
   - **Combined Osmosis Performance** (requires valid Osmosis allocations for at least 6 weeks in the prior 3 months; see [11 — Osmosis and Compensation](../11-osmosis-and-compensation/index.md)).

### The Six Genius Tie-Breaker Criteria

Eligibility thresholds are pass/fail gates. When more consultants pass the eligibility thresholds for a tier than the available slot share (`20%` Expert, `8%` Master, `2%` Grand Master), candidates are ranked by the **sum of ranks** across six tie-breaker metrics (`[Platform]`):

| Rank Component | Direction | Strategic Implication (`[Platform]`) |
|---|---|---|
| **1. Avg Distinct Operators / Alpha** | **Lower is better** | Favors concise expressions (`2–4` operators per Alpha); `ts_backfill` and `group_backfill` are **excluded** |
| **2. Avg Distinct Fields / Alpha** | **Lower is better** | Favors single-field or 2-field ATOM / Power Pool expressions |
| **3. Total Distinct Operators Used** | **Higher is better** | Rewards exploring the broader operator catalog across different Alphas |
| **4. Total Distinct Fields Used** | **Higher is better** | Rewards exploring diverse datasets/fields across different Alphas |
| **5. Maximum Simulation Streak** | **Higher is better** | Best consecutive daily simulation streak ending in or continuing through the quarter |
| **6. Community Leader** | **Higher is better** | Forum likes on posts/comments (`>= 100` chars) + successful consultant referrals |

### Dynamic Pyramid Multipliers and Theme Multiplier Stacking

- **Dynamic Pyramid Multiplier:** Displayed on the Datasets page and simulation results; scales the Quality Factor of daily base fees inversely with platform-wide utilization of that `Region x Delay x Category` pyramid (less crowded pyramids earn higher multipliers, updated daily) (`[Platform]`).
- **Parallel Theme Multiplier Stacking Formula:** When an Alpha simultaneously satisfies $k$ active platform Themes with multipliers $M_1, M_2, \dots, M_k$, the combined Quality Factor multiplier is (`[Platform]`):
  $$M_{\text{final}} = \left(\sum_{j=1}^{k} M_j\right) - k + 1$$
  - *Example:* Satisfying a Region Theme ($M_1 = 3$) and a Dataset Theme ($M_2 = 5$) simultaneously yields $M_{\text{final}} = (3 + 5) - 2 + 1 = 7\times$ on your Quality Factor (`[Platform]`).

## 4. Step-by-Step Strategy for Pyramid & Tie-Breaker Optimization

1. **Build in 3-Alpha Pyramid Blocks:** Whenever you discover a working mechanism in a less-crowded scope (such as `EUR - D1 - Analyst` on `anl69` or `anl4`), submit at least **3 distinct Alphas** in that `Region x Delay x Category` so the Pyramid officially registers toward Genius eligibility (`[Platform]`).
2. **Keep Individual Alphas Concise, Diversify Across Alphas:** Notice the tension between Tie-Breakers 1–2 (*low* average operators/fields per Alpha) and Tie-Breakers 3–4 (*high* total distinct operators/fields across your pool). The mathematical optimum is to write **many simple 1-to-2 field Alphas (ATOM / Power Pool style)**, each using a *different* field and operator pair!
3. **Submit Early in the Quarter:** Because Combined Alpha Performance refreshes every 4–6 weeks, Alphas submitted in the final month of a calendar quarter may not be reflected in that quarter's Combined Alpha Performance calculation (though they still count toward signal count, pyramids, and next quarter's performance) (`[Platform]`).

## 5. Working Examples

### Example: Designing a 3-Alpha Pyramid in `EUR - D1 - Analyst`

Using the empirical findings from [`EUR Simulation Results`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/README.md), a consultant targeting the `EUR - D1 - Analyst` pyramid tests distinct slow-analyst fields with distinct operators so that:
- `Avg Fields/Alpha = 1.0` (optimal for Tie-Breaker 2),
- `Avg Operators/Alpha = 1.0` (excluding `ts_backfill`, optimal for Tie-Breaker 1),
- `Total Distinct Fields` and `Total Distinct Operators` increase with each submission (optimal for Tie-Breakers 3 & 4).

## 6. Common Mistakes and Troubleshooting

- **Submitting 1–2 Alphas in five different categories instead of 3 in one:** `2` Alphas in five categories gives `0` completed Pyramids (`10` Alphas total), whereas `3` Alphas in three categories gives `3` completed Pyramids (`9` Alphas total) (`[Platform]`).
- **Padding an Alpha with extra fields/operators:** Hurts both Tie-Breaker 1 & 2 (`Avg Operators/Alpha` and `Avg Fields/Alpha`) and disqualifies the Alpha from Power Pool (`<= 8` operators, `<= 3` fields).

## 7. Practical Exercises

1. Compute the stacked multiplier for an Alpha that satisfies three concurrent themes with multipliers `2x`, `3x`, and `4x`: $(2 + 3 + 4) - 3 + 1 = 7\times$.
2. Audit our existing submissions (`026`, `027`, `053`) in [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/index.md) and identify which `Region x Delay x Category` pyramids they populate (`USA - D1 - Fundamental` and `USA - D1 - Price Volume`).

## 8. Related Topics and Next Steps

- **Next Module:** [11 — Osmosis and Compensation](../11-osmosis-and-compensation/index.md)
- **Regional Unlocks:** [13 — Region-Agnostic and Cluster Alphas](../13-region-agnostic-and-cluster-alphas/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Brain Genius* (`brain-genius`), *Overview of Themes* (`overview-themes`), *Multiplier Rules* (`multiplier-rules`), and *Theme Calendar* (`consgrp5`) (`[Platform]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
