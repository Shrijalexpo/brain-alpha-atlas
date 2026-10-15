# 08 — Submission Checks and Consultant Eligibility

## 1. Learning Objectives

By completing this module, you will be able to:

- Diagnose every platform submission check (`LOW_SHARPE`, `LOW_FITNESS`, `HIGH_TURNOVER`, `LOW_TURNOVER`, `LOW_2Y_SHARPE`, `LOW_SUB_UNIVERSE_SHARPE`, `LOW_ROBUST_UNIVERSE_SHARPE`, `CONCENTRATED_WEIGHT`, `IS_LADDER_SHARPE`, `SELF_CORRELATION`, `PROD_CORRELATION`).
- Apply the exact **Sub-Universe Sharpe formula** and **Consultant IS Ladder algorithm** (including the `< 30%` turnover `0.85x` relaxation).
- Leverage **ATOM (Single Dataset Alpha)** relaxed submission thresholds when full 10-year IS Ladder thresholds are too restrictive.
- Reduce self-correlation and platform-wide production correlation (`<= 0.7` or `+10%` higher Sharpe rule) using legitimate structural diversification.

## 2. Prerequisites

- [07 — Simulation and Evaluation](../07-simulation-and-evaluation/index.md)

## 3. Core Concepts: User-Level vs. Consultant-Level Submission Gates

Passing the basic user-level metrics (`Sharpe > 1.25`, `Fitness > 1.0`, `Turnover 1%–70%`) is necessary but **not sufficient** at the Research Consultant level (`[Platform]`).

| Submission Gate | User-Level Requirement | Consultant-Level Requirement (`[Platform]`) |
|---|---|---|
| **In-Sample Sharpe Consistency** | Full-period `Sharpe > 1.25` (D1) or `> 2.00` (D0), plus `LOW_2Y_SHARPE` | **Regular Alpha:** Must clear the **IS Ladder Test** across `N = 2..10` year windows.<br>**ATOM (Single-Dataset):** Must clear last **2-Year Avg IS Sharpe** (`>= 1.59–2.08` D1; `>= 2.69–3.50` D0).<br>**Power Pool:** `Sharpe >= 1.00` (`<= 8` ops, `<= 3` fields). |
| **Correlation Ceiling** | **Self-Correlation `< 0.70`** against your own submitted Alphas (or `>= +10%` higher Sharpe than your correlated Alpha) | **Prod-Correlation `<= 0.70`** against **all Alphas in the entire BRAIN platform pool** (or `>= +10%` higher Sharpe than every correlated platform Alpha; Power Pool exempt) |
| **Universe Robustness** | **Sub-Universe Sharpe** test (`>= 0.75 * sqrt(N_sub / N_univ) * Sharpe`) | Sub-Universe Sharpe + **Robust-Universe Sharpe** (`IND` `>= 1.0`) + **Sub-Geography Sharpe** (`GLB`: `AMER >= 1, APAC >= 1, EMEA >= 1`) |
| **Weight Concentration** | Max single-stock weight `< 10%` and sufficient active instruments per day | Same, plus investability-constrained checks in scopes like `EUR TOPCS1600` (`Max Trade = ON`) |

### The Consultant IS Ladder Test (Regular Alphas)

The IS Ladder test verifies that an Alpha maintains high risk-adjusted performance consistently across recent sub-windows rather than relying on a single historical spike (`[Platform]`):

```text
If full IS Sharpe < FAIL_THRESHOLD: return FAIL
Else for N_YEARS in 2..10:
    If Sharpe[last N_YEARS] < FAIL_THRESHOLD[N_YEARS]: return FAIL
    Else if Sharpe[last N_YEARS] > PASS_THRESHOLD[N_YEARS]: return PASS
    Else: continue to next N_YEARS window
```

- **Low-Turnover Relief (`< 30%` Turnover):** If the Alpha's turnover is **below 30%**, every `PASS_THRESHOLD` is multiplied by **`0.85`** (a 15% reduction), while `FAIL_THRESHOLD` remains unchanged (`[Platform]`).

| Lookback Window (`N_YEARS`) | `FAIL_THRESHOLD` | Standard `PASS_THRESHOLD` | Low-Turnover (`< 30%`) `PASS_THRESHOLD (x 0.85)` |
|---|---:|---:|---:|
| **2 years** | `2.38` | `3.96` | `3.37` |
| **3 years** | `2.38` | `3.96` | `3.37` |
| **4 years** | `2.38` | `3.96` | `3.37` |
| **5 years** | `2.38` | `3.96` | `3.37` |
| **6 years** | `2.22` | `3.64` | `3.09` |
| **7 years** | `2.06` | `3.33` | `2.83` |
| **8 years** | `1.90` | `3.17` | `2.69` |
| **9 years** | `1.74` | `2.85` | `2.42` |
| **10 years** | `1.59` | `2.69` | `2.29` |

*(Note: Verify live per-window cutoffs in the Submission tab of the simulator, as captured table headers rendered the 10-year row first, `[Platform]`.)*

### ATOM (Single Dataset Alpha) Relaxed Criteria

An Alpha is classified as a **Single Dataset Alpha (ATOM)** if all data fields come from **one single dataset**, excluding the 6 permitted grouping fields (`country`, `exchange`, `market`, `sector`, `industry`, `subindustry`) (`[Platform]`). Note that `inst_pnl()` and `convert()` count as using `pv1` (`[Platform]`).

Instead of the full 2–10 year IS Ladder, an ATOM only needs its **Last 2-Year Average IS Sharpe** to clear (`[Platform]`):

| Delay | ATOM 2Y `FAIL_THRESHOLD` | ATOM 2Y `PASS_THRESHOLD` | Additional Requirement |
|---|---:|---:|---|
| **Delay-1 (`D1`)** | `1.59` | `2.08` | Prod-Correlation `< 0.70` |
| **Delay-0 (`D0`)** | `2.69` | `3.50` | Prod-Correlation `< 0.70` |

### The Sub-Universe Test Formula

BRAIN verifies that an Alpha built on a broad universe (such as `USA TOP3000`, $N_{\text{alpha}} = 3000$) also works on the next more liquid sub-universe (`USA TOP1000`, $N_{\text{sub}} = 1000$) (`[Platform]`):

$$\text{Sub-Universe Sharpe} \ge 0.75 \times \sqrt{\frac{N_{\text{sub}}}{N_{\text{alpha}}}} \times \text{Alpha Sharpe}$$

- **Example:** For `USA TOP3000` tested on `TOP1000` with $\text{Alpha Sharpe} = 2.73$:
  $$\text{Cutoff} = 0.75 \times \sqrt{\frac{1000}{3000}} \times 2.73 = 0.433 \times 2.73 = 1.18$$
- **How BRAIN computes Sub-Universe Sharpe:** It pasteurizes out-of-sub-universe stocks to `NaN`, applies market neutralization to the remaining sub-universe stocks, rescales to booksize, and calculates PnL (`[Platform]`).

## 4. Step-by-Step Catalog of Failed Checks and Fixes

| Check Name | Empirical Frequency in Sweeps (`[Observed]`) | Exact Cause | Targeted Repair Strategy |
|---|---|---|---|
| `LOW_2Y_SHARPE` | **92%–98%** of EUR sweep blocks (`067`–`069`) | Recent 2-year PnL is flat or decaying even when 10-year Sharpe is high | Use medium-horizon adaptive normalization (`ts_scale(x, 63)`, `ts_quantile(x, 63)`) or risk neutralization (`SLOW`, `FAST`, `STATISTICAL`) (`[Observed]`, `[Platform]`) |
| `LOW_SUB_UNIVERSE_SHARPE` | **46%–49%** of EUR sweep blocks; top `pv37` volume signals | Profit is concentrated in small/illiquid tail stocks rather than liquid large-caps | 1. Remove size tilts like `rank(-assets)` or `1 - rank(cap)`.<br>2. Decay liquid and illiquid stocks differently (`ts_decay_linear(sig, 5) * rank(volume*close) + ts_decay_linear(sig, 15) * (1 - rank(volume*close))`).<br>3. Neutralize within `bucket(rank(cap), range="0.1,1,0.1")` (`[Platform]`, `[Observed]`). |
| `CONCENTRATED_WEIGHT` | Dominant failure in USA `option6` IV sweeps (`071 d5`) | Too few instruments receive non-zero weight, or single stocks exceed the weight cap | 1. Backfill sparse fields (`ts_backfill(x, 63)` or `group_backfill`).<br>2. Wrap in `rank(x)` or `winsorize(x, std=4)`.<br>3. Lower settings `Truncation` from `0.08` to `0.01–0.02` (`[Platform]`, `[Observed]`). |
| `HIGH_TURNOVER` / `LOW_TURNOVER` | `9.3%` in EUR Decay 0 (`069`) | Daily trading outside `1%–70%` (or regional `< 30%` / `< 40%` cap) | Adjust `Decay`, `ts_mean`, `ts_decay_linear`, or `hump` (`[Platform]`). |
| `IS_LADDER_SHARPE` | Fired on top EUR blocks (`068`, `071`) | Multi-window Sharpe falls below ladder cutoffs | Target `< 30%` turnover for the `0.85x` PASS relaxation, or convert the expression into a single-dataset **ATOM** (`[Platform]`, `[Observed]`). |
| `SELF_CORRELATION` / `PROD_CORRELATION` | Rejected 4 strong USA Alphas (`029, 031, 033, 046` at `0.88–0.94`) | 4-year PnL correlation `>= 0.70` without a `+10%` Sharpe advantage | Switch region (`EUR, GLB, KOR, AMR`), switch dataset category (`anl69, option6, model77`), or apply risk-factor neutralization (`[Platform]`, `[Observed]`). |

## 5. Working Examples: Fixing Sub-Universe Failure via Cap-Bucket Neutralization

In Simulation [`026`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/026_submitted_ts_rank_ebitda_ev_sales_growth_ts_mean_reversal.md), wrapping the 3-factor composite inside decile market-cap buckets ensured that mega-cap (`TOP1000`) stocks were ranked and neutralized against mega-cap peers rather than against small-cap stocks (`[Observed]`):

```text
group_neutralize(
    rank(ts_rank(ebitda / enterprise_value, 126))
    + rank(ts_rank(sales_growth, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```
Result: `Sub-universe Sharpe = 1.53` against `Alpha Sharpe = 1.61` (well above the `0.75 * sqrt(1000/3000) * 1.61 = 0.70` cutoff) (`[Observed]`).

## 6. Common Mistakes and Troubleshooting

- **Making cosmetic window tweaks to fix Self-Correlation:** Changing `ts_delta(return_assets, 126)` to `ts_delta(ebitda / enterprise_value, 126)` in Simulation [`033`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/033_operating_income_ebitda_ev_delta_reversal_selfcorr.md) still failed self-correlation because the `operating_income/assets + ts_mean(-returns, 5)` backbone was unchanged (`[Observed]`). You must change the underlying dataset or mechanism.

## 7. Practical Exercises

1. Check Simulations [`029`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/029_operating_income_roa_reversal_selfcorr.md), [`031`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/031_cashflow_roa_reversal_selfcorr.md), [`033`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/033_operating_income_ebitda_ev_delta_reversal_selfcorr.md), and [`046`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/046_dividend_volume_returns_selfcorr.md) and identify the shared expression terms that caused `0.88–0.94` correlation.
2. Calculate the `+10%` Sharpe threshold required to submit an Alpha whose correlation is `0.78` against an existing Alpha with `Sharpe = 1.61` (`1.61 * 1.10 = 1.771`).

## 8. Related Topics and Next Steps

- **Next Module:** [09 — Power Pool and Thematic Competitions](../09-power-pool-and-thematic-competitions/index.md)
- **Regional Rules:** [13 — Region-Agnostic and Cluster Alphas](../13-region-agnostic-and-cluster-alphas/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Clear These Tests Before Submitting an Alpha*, *Consultant Submission Tests*, *Single Dataset Alphas*, and *Finding Consultant Alphas* (`[Platform]`, captured 2026-07-26 and 2026-10-06/09); empirical records `026`–`071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
