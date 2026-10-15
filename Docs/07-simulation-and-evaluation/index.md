# 07 — Simulation and Evaluation

## 1. Learning Objectives

By completing this module, you will be able to:

- Interpret all six core WorldQuant BRAIN simulation metrics (**Sharpe**, **Fitness**, **Turnover**, **Returns**, **Drawdown**, **Margin**) as an interconnected system.
- Use the exact **Fitness formula** to determine whether a low Fitness score is caused by excessive Turnover or insufficient Returns.
- Distinguish **Out-of-Sample / Full IS Sharpe (`Sharpe`)** from **`Train Sharpe`** and **Investability-Constrained Sharpe**.
- Apply the prioritized repair catalog to fix weak Sharpe, high Turnover, or high Drawdown without destroying the underlying signal.

## 2. Prerequisites

- [06 — Alpha Research and Construction](../06-alpha-research-and-construction/index.md)

## 3. Core Concepts: The Simulation Metrics System

No single number determines whether an Alpha is good. You must read the metrics together (`[Platform]`, `[Notes]`):

| Metric | Definition & Formula | Target / Working Bar | What It Reveals |
|---|---|---|---|
| **Sharpe** | Annualized risk-adjusted return: $\frac{\text{Mean Daily Return}}{\text{Std Dev of Daily Return}} \times \sqrt{252}$ | User D1: `> 1.25`<br>User D0: `> 2.00`<br>Power Pool: `>= 1.00`<br>ATOM D1 2Y: `>= 1.59–2.08`<br>Consultant Regular: IS Ladder (`1.59–3.96`) (`[Platform]`) | Signal consistency and statistical significance before transaction costs |
| **Returns** | Annualized return as a percentage of booksize (`PnL / Booksize`) | Higher is better (CHN D1 requires `>= 6.3%`, D0 `>= 8.9%`) (`[Platform]`) | Raw economic magnitude; feeds the numerator of Fitness |
| **Turnover** | Percentage of booksize traded each day (`Daily $ Traded / Booksize`) | `1.0% < Turnover < 70.0%` (`< 30%` for IS Ladder `0.85x` relief & `HKG/KOR`; `< 40%` for `IND`) (`[Platform]`) | Trading frequency and transaction-cost drag; feeds the denominator of Fitness |
| **Fitness** | $$\text{Fitness} = \frac{\text{Sharpe} \times \sqrt{\vert\text{Returns}\vert}}{\max(\text{Turnover},\, 0.125)}$$ | User D1: `> 1.00`<br>User D0: `> 1.30` (`[Platform]`, `[Notes]`) | Composite efficiency score balancing Sharpe and Returns against Turnover |
| **Drawdown** | Maximum peak-to-trough percentage loss over the simulation window | Prefer `Returns / Drawdown > 1.0` (`[Notes]`) | Tail-risk and regime vulnerability |
| **Margin** | Profit per unit of dollar volume traded, in basis points (`bps` or `‱`, $10^{-4}$) | Higher is better (`>= 10 bps` in `TWN`, `> 5‱` in `EUR TOPCS1600`) (`[Platform]`) | Capacity to survive real-world bid-ask spread and slippage |

### Three Consequences of the Fitness Equation

From $\text{Fitness} = \text{Sharpe} \times \sqrt{|\text{Returns}|} / \max(\text{Turnover}, 0.125)$:

1. **The Turnover Penalty (`Turnover > 12.5%`):** Above `12.5%` daily turnover, doubling turnover cuts Fitness in half. In Simulation [`007`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/007_dividend_volume_returns.md), a strong `Sharpe = 1.78` failed with `Fitness = 0.67` because `Turnover = 57.51%` (`[Observed]`).
2. **The `12.5%` Turnover Floor (`max(Turnover, 0.125)`):** Once turnover is already below `12.5%`, reducing turnover further does **not** shrink the denominator of Fitness! If Fitness is still below `1.0` when turnover is `<= 12.5%`, the only way to raise Fitness is to increase `Sharpe` or `Returns`.
3. **The Low-Returns Trap:** In Simulation [`066`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/066_op_cash_flow_stddev_level_reversal.md), `Sharpe = 1.16` at `Turnover = 13.12%` yielded `Fitness = 0.78` because `Returns` were too small (`[Observed]`).

### `Sharpe` vs. `Train Sharpe` vs. `Investability-Constrained Sharpe`

- **`Sharpe` vs. `Train Sharpe`:** When a Test Period is active or in multi-simulation result dumps, BRAIN reports both `Sharpe` and `Train Sharpe`. In the 2,500-block USA sweep (`070` page 1), `Train Sharpe` differed from true `Sharpe` in **2,448 of 2,500 blocks**, systematically inflating results (`[Observed]`). Always evaluate and index the true `Sharpe` column.
- **Investability-Constrained Metrics:** Evaluates the Alpha after capping daily trades and positions by real-world stock liquidity (`Max Trade = ON`). For Osmosis portfolio selection, drop any Alpha whose Sharpe drops by `>= 60%` under investability constraints (`[Platform]`).

## 4. Step-by-Step Diagnostic and Repair Matrix

Before changing an expression, classify the failure into one of four diagnostic quadrants (`[Notes]`, `[Observed]`):

| Diagnostic Quadrant | Observed Metrics | Root Cause | Ordered Repair Actions |
|---|---|---|---|
| **Quadrant 1: Weak Signal** | `Sharpe < 1.10`, `Turnover < 25%` | The economic idea or raw field lacks predictive power | 1. Replace raw level with size/valuation ratio (`ebitda/enterprise_value`).<br>2. Change transform from `rank(x)` to `ts_rank(x, 126)` or `ts_scale(x, 63)`.<br>3. Discard field family if 2–3 controlled variants stay `< 1.0`. **Do not** raise Decay. |
| **Quadrant 2: Good Signal, Excessive Trading Cost** | `Sharpe >= 1.30`, `Fitness < 1.00`, `Turnover > 35%` | Fast leg (returns or volume) flips positions too rapidly | 1. Smooth only the fastest component (`rank(-returns)` -> `rank(ts_mean(-returns, 5))`).<br>2. Wrap signal in `ts_decay_linear(x, 10)` or `hump(x, hump=0.01)`.<br>3. Reduce weight on the fast leg (`0.3 * rank(...)`) or raise settings `Decay` (`4 -> 6 -> 8`). |
| **Quadrant 3: Low Turnover, Weak Returns** | `Sharpe ~ 1.15–1.30`, `Fitness < 1.00`, `Turnover < 15%` | Signal is slow and stable, but per-stock return spread is too small | 1. Add one complementary medium-horizon factor (e.g., `ts_rank(sales_growth, 126)`).<br>2. Test `quantile(x, driver="gaussian")` or `zscore()` instead of flat `rank()`.<br>3. **Do not** add more smoothing (`064` over-smoothing trap). |
| **Quadrant 4: Strongly Negative Sharpe** | `Sharpe < -0.50` | Economic direction is inverted or nonlinear product is distorted | 1. Verify whether economic logic supports reversing the sign (`-x`).<br>2. If caused by multiplying noisy terms (`013`), replace product with ranked sum. |


### Empirical Check Failure Incidence in Broad Sweeps (3,550 USA Blocks)

In Experiment [`070`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/070_usa_top3000_industry_analyst_growth_sweep.md) (single-field backfilled screen across USA universes), 3,544 of 3,550 blocks (99.8%) failed platform validation (`[Observed]`):

| Individual Validation Check | Blocks Failing Check | Failure Incidence (%) | Primary Root Cause in Single-Field Alphas |
|---|---:|---:|---|
| **`LOW_SHARPE`** | 3,544 | `99.8%` | Unsmoothed raw single fields rarely meet the multi-year IS Ladder bar (`1.59–3.96`) |
| **`LOW_FITNESS`** | 3,543 | `99.8%` | Low raw returns (`Median Returns = 1.33%`) cap the Fitness numerator |
| **`LOW_2Y_SHARPE`** | 3,412 | `96.1%` | Signal decay in recent 2-year testing window without complementary factors |
| **`LOW_SUB_UNIVERSE_SHARPE`**| 1,237 | `34.8%` | Mid/small-cap analyst dispersion does not translate into liquid large caps (`TOP200/500`) |
| **`CONCENTRATED_WEIGHT`** | 887 | `25.0%` | 21-day backfill window lapses between 63-day quarterly filings, dropping stocks to NaN |
| **`HIGH_TURNOVER`** | 213 | `6.0%` | Using `group_std_dev` or noisy sentiment/volume fields flips positions daily |
| **`LOW_TURNOVER`** | 201 | `5.7%` | Extreme smoothing or stale static ratios trade `< 1.0%` booksize per day |

## 5. Working Examples: The `024 -> 025 -> 026` Repair Sequence

This recorded sequence in `USA / TOP3000 / Delay 1 / Subindustry` illustrates disciplined bottleneck repair (`[Observed]`):

| Sim ID | Expression Change | Sharpe | Fitness | Turnover | Diagnosis & Next Step |
|---:|---|---:|---:|---:|---|
| [`022`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/022_ebitda_ev_sales_growth_returns.md) | `rank(ebitda/ev) + rank(sales_growth) + rank(-returns)` | `1.21` | `< 1.0` | High | Base value + growth + raw 1d reversal; Sharpe just below `1.25` |
| [`024`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/024_ts_rank_ebitda_ev_sales_growth_returns.md) | `rank(ts_rank(ebitda/ev, 126)) + rank(sales_growth) + rank(-returns)` | `1.36` | `0.68` | High | `ts_rank(..., 126)` fixed Sharpe (`1.36`), now in **Quadrant 2** (Fitness `0.68`) |
| [`025`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/025_ts_rank_ebitda_ev_ts_rank_sales_growth_returns.md) | Also apply `ts_rank(sales_growth, 126)` | `1.78` | `0.97` | High | Sharpe jumped to `1.78`, Fitness `0.97` (just `0.03` short due to unsmoothed `-returns`) |
| [`026`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md) | Smooth reversal leg: `rank(ts_mean(-returns, 5))` + cap-bucket neutralization | **`1.61`** | **`1.02`** | **`25.25%`** | **Cleared user-level checks (`PASSED_SUBMITTABLE`)** |

## 6. Common Mistakes and Troubleshooting

- **Smoothing a slow signal instead of the fast leg:** In Simulation [`005`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/005_ts_mean_operating_income_cap_returns.md), applying `ts_mean` to the quarterly `operating_income / cap` leg while leaving `-returns` raw did nothing to fix turnover and lowered Sharpe to `1.01` (`[Observed]`). Always smooth the highest-turnover leg.

## 7. Practical Exercises

1. Compute the theoretical Fitness of an Alpha with `Sharpe = 1.50`, `Returns = 10.0%` (`0.10`), and `Turnover = 45.0%` (`0.45`), and compare it with the same Alpha after smoothing reduces `Turnover` to `22.5%` (`0.225`).
2. Inspect Simulation [`065`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/065_op_cash_flow_stddev_sales_growth_reversal.md) (`Sharpe 1.48, Fitness 0.91, Turnover 21.78%`) and diagnose why Fitness fell `0.09` short despite healthy Turnover.

## 8. Related Topics and Next Steps

- **Next Module:** [08 — Submission and Eligibility](../08-submission-and-eligibility/index.md)
- **Case Studies:** [17 — Case Studies and Lessons Learned](../17-case-studies-and-lessons-learned/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Parameters in the Simulation Results*, *Intermediate Pack [1/2 & 2/2]*, and *Investability Constrained Metrics* (`[Platform]`, captured 2026-07-26 and 2026-10-09); empirical records `001`–`071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
