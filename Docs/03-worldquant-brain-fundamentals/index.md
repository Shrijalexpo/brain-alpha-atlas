# 03 — WorldQuant BRAIN Fundamentals & Simulation Settings

## 1. Learning Objectives

By completing this module, you will be able to:

- Configure every parameter in the WorldQuant BRAIN **Simulation Settings** panel intentionally rather than by trial-and-error.
- Predict how changing **Delay**, **Decay**, **Truncation**, **Neutralization**, **Pasteurization**, and **NaN Handling** affects Turnover, Sharpe, Fitness, and Weight Concentration.
- Use the **Test Period** and **Visualization Tool** to guard against in-sample overfitting and sector/country concentration bias.

## 2. Prerequisites

- [01 — Getting Started with WorldQuant BRAIN](../01-getting-started/index.md)
- [02 — Financial and Quantitative Foundations](../02-financial-and-quantitative-foundations/index.md)

## 3. Core Concepts: The Simulation Settings Panel

Every simulation result is a joint product of the **Alpha expression** and the **Simulation Settings** (`[Platform]`). Recording an expression without its settings makes the result irreproducible.

| Setting | Options / Range | What It Controls | Empirical & Platform Guidance |
|---|---|---|---|
| **Instrument Type** | `EQUITY` | Asset class simulated | All recorded research in this repository uses `EQUITY` (`[Notes]`) |
| **Region** | `USA, EUR, ASI, CHN, KOR, AMR, GLB, IND, JPN, HKG, TWN` | Geographic market scope | Determines trading calendar, currency/cost structure, and regional submission thresholds (`[Platform]`) |
| **Universe** | `TOP3000, TOP2000, TOP1000, TOP500, TOPSP500, TOP2500, TOPCS1600, TOPDIV3000, MINVOL10M, ...` | Liquidity/capitalization basket of stocks | Larger universes provide broader cross-sections; smaller universes have higher liquidity and lower transaction cost drag (`[Platform]`) |
| **Language** | `Fast Expression`, `Python` | Execution engine | Fast Expression is standard; Python Alphas use `@alpha` in BrainLabs/UI (`[Platform]`) |
| **Delay** | `1` or `0` | Lag in trading days between data observation and execution | `Delay = 1` uses yesterday's close/data (standard bar: Sharpe `> 1.25`, Fitness `> 1.0`). `Delay = 0` trades same-day prior to close (higher bar: Sharpe `> 2.0`, Fitness `> 1.3`) (`[Platform]`) |
| **Decay** | Integer `0` to `512` (typical `0–16`) | Linear weighted moving average over the past $d$ days of raw Alpha vectors | Primary settings lever for reducing **Turnover**. In EUR sweeps `068` (Decay 5) vs `069` (Decay 0), Decay shifted turnover up to `3.3x` while moving Sharpe by `<= 0.13` (`[Observed]`) |
| **Truncation** | Decimal `0.00` to `1.00` (typical `0.01–0.08`) | Maximum absolute portfolio weight (`|w_i|`) allowed in any single stock | `0.08` (8%) is the tutorial default; `0.01–0.02` (1%–2%) prevents single-stock outliers from dominating PnL or failing the Weight test (`[Platform]`) |
| **Neutralization** | `None, Market, Sector, Industry, Subindustry, Country`, plus Risk modes (`Slow, Fast, Slow_and_Fast, Crowding, Statistical, RAM`) | Demeans Alpha scores within each group so net weight per group is zero | Match neutralization to dataset family (see Step-by-Step guide below) (`[Platform]`) |
| **Pasteurization** | `On`, `Off` | Sets values for instruments outside the active universe to `NaN` before operators run | Keep **`On`** so out-of-universe stocks do not distort cross-sectional ranks or group means (`[Platform]`) |
| **Unit Handling** | `Verify` | Warns when adding or comparing fields with incompatible units (e.g., Dollars + Shares) | Always `Verify`; normalize fields via ratios or `rank()` before combining (`[Platform]`) |
| **NaN Handling** | `On`, `Off` | Replaces `NaN` values with `0` (neutral weight after centering) instead of propagating `NaN` | Keep `Off` when using explicit `ts_backfill(x, d)` / `group_backfill`; turn `On` when sparse fields otherwise drop too many instruments (`[Platform]`) |
| **Max Trade** | `On`, `Off` | Constrains daily position changes based on instrument liquidity (`adv20`) | **Mandatory `On`** in `HKG / KOR / TWN` and used for investability-constrained checks (`[Platform]`) |
| **Test Period** | `0Y0M` to `P2Y0M+` (e.g. `P1Y0M`, `P1Y6M`) | Holds out the end of the In-Sample window as a blind Test split during development | Prevents parameter overfitting; **must be revealed (`0Y0M`) before final submission** (`[Platform]`) |

## 4. Step-by-Step Explanations

### Step 1: Choosing Neutralization by Dataset Category

Neutralization is not a random toggle; it defines the benchmark peer group against which each stock is compared (`[Platform]`, `[Notes]`):

| Dataset Category | Recommended First-Try Neutralization | Why |
|---|---|---|
| **Price / Volume (`pv1`, `pv37`)** | `Market` or `Sector` (or `Subindustry` for short-horizon reversal) | Broad market beta drives daily price moves; peer industry neutralization isolates stock-specific reversal |
| **Company Fundamentals (`fnd6`)** | `Industry` or `Subindustry` | Accounting structures (margins, leverage, asset intensity) vary structurally across industries |
| **Analyst Estimates (`anl4`, `anl10`, `anl69`)** | `Industry` or `Country` (in multi-country regions like `EUR` / `GLB`) | Analyst coverage and accounting standards cluster by country and industry |
| **Multi-Country Regions (`EUR`, `GLB`, `AMR`, `ASI`)** | `Country` or **Double Neutralization** (`country` x `industry`) | Removes country-level macro/currency drift before comparing industry peers (`[Platform]`) |

> **Critical Rule — Do Not Double-Neutralize Unintentionally:** If you apply `group_neutralize(x, subindustry)` as the outer wrapper of your Fast Expression AND set `Neutralization = Subindustry` in the settings panel, you are neutralizing twice. If you use expression-level `group_neutralize` deliberately (for example, to neutralize against custom `cap` or `volatility` buckets), either set panel `Neutralization = None` (with `Decay = 0`, `Truncation = 0`, handling smoothing inside the expression) or recognize that the panel setting will re-center by the panel group as the final step (`[Platform]`).

### Step 2: Using Decay Without Destroying Signal Horizon

When an Alpha has strong `Sharpe` (`> 1.4`) but fails `Fitness` because `Turnover` is high (`> 40%`):

1. Understand the **PnL Realization Horizon**: fast signals (1–5 day price reversal, intraday snapshot volume) realize their predictive edge within a few days (`[Platform]`).
2. Applying excessive `Decay` (e.g., `Decay = 20`) to a 3-day signal forces the portfolio to hold stale positions long after the edge has decayed.
3. **Empirical proof:** In Simulation [`063`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/063_op_cash_flow_stddev_high_turnover.html) (`Sharpe 1.52, Fitness 0.84`), heavy smoothing in Simulation [`064`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/064_smoothed_operating_cash_flow_estimate_dispersion.html) (`Decay = 8` plus 20-day averaging) cut Turnover to `11.81%` but collapsed Sharpe to `0.85` (`[Observed]`).
4. **Best practice:** Smooth only the fastest leg inside the expression (e.g., `ts_mean(-returns, 5)`) and step `Decay` gradually (`4 -> 6 -> 8`).

### Step 3: Using the Visualization Tool (Consultant Feature)

Available on consultant simulation result pages (`[Platform]`):

- **Coverage by Sector / Country:** Confirms that your Alpha assigns weights across the full universe rather than only one sector or country.
- **Sharpe by Capitalization Buckets (`0–20`, `20–40`, `40–60`, `60–80`, `80–100`):** In universes like `EUR TOPCS1600`, a substantial portion of performance must come from the upper 40% capitalization buckets (`60–80` and `80–100`) to pass sub-universe and investability checks (`[Platform]`).

## 5. Working Examples

### Standard Workspace Baseline Configuration (`USA`)

```text
Instrument Type: Equity
Region:          USA
Universe:        TOP3000
Language:        Fast Expression
Delay:           1
Decay:           4
Truncation:      0.08
Neutralization:  Subindustry
Pasteurization:  On
Unit Handling:   Verify
NaN Handling:    Off
```

### Multi-Country Consultant Baseline Configuration (`EUR`)

```text
Instrument Type: Equity
Region:          EUR
Universe:        TOP2500 (or TOPCS1600)
Language:        Fast Expression
Delay:           1
Decay:           5
Truncation:      0.08
Neutralization:  COUNTRY (or INDUSTRY with expression-level country conditioning)
Pasteurization:  On
Unit Handling:   Verify
NaN Handling:    On
```

## 6. Common Mistakes and Troubleshooting

- **Expecting Decay to fix `CONCENTRATED_WEIGHT` or `LOW_SUB_UNIVERSE_SHARPE`:** In Simulation [`071`](../../Analysis%20and%20Simulation%20Reports/simulation-results/multi-region/071_multi_region_bundle_20261009.html) (Dump `d5`), testing `Decay = 0, 3, 4, 5, 6, 7, 8, 10, 12, 16` on the exact same USA implied-volatility expressions left the `CONCENTRATED_WEIGHT` and `LOW_SUB_UNIVERSE_SHARPE` failure set completely unchanged (`[Observed]`). Fix weight concentration with `rank()`, `winsorize()`, `ts_backfill()`, or lower `Truncation` (`0.01–0.02`).
- **Forgetting to reset Test Period before submission:** BRAIN blocks submission while a non-zero Test Period is active; reveal the full in-sample period once your expression is finalized (`[Platform]`).

## 7. Practical Exercises

1. Inspect [`068_eur_multi_universe_decay5_sweep.md`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/068_eur_multi_universe_decay5_sweep.html) (`Decay 5`) and [`069_eur_multi_universe_decay0_sweep.md`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/069_eur_multi_universe_decay0_sweep.html) (`Decay 0`). Compare how `HIGH_TURNOVER` failure rates changed between Decay 0 and Decay 5.
2. Check how performance changes across `TOP2500`, `TOPCS1600`, `TOP1200`, `TOP800`, and `TOP400` in [`SUMMARY.md`](../../Analysis%20and%20Simulation%20Reports/sweeps-and-experiments/SUMMARY.html).

## 8. Related Topics and Next Steps

- **Next Module:** [04 — Data Explorer and Datasets](../04-data-explorer-and-datasets/index.md)
- **Advanced Neutralization:** [12 — Advanced Alpha Research](../12-advanced-alpha-research/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *How to Choose the Simulation Settings*, *Understanding PnL Realization Horizon*, *Test Period*, and *Visualization Tool* (`[Platform]`, captured 2026-07-26 and 2026-10-06/09); empirical sweep records `068`, `069`, `071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
