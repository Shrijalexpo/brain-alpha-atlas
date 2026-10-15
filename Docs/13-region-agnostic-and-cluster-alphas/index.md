# 13 — Region-Agnostic, Multi-Region, and Cluster Alphas

## 1. Learning Objectives

By completing this module, you will be able to:

- Navigate every consultant equity region (`USA, EUR, GLB/ALL, ASI, CHN, IND, JPN, HKG/KOR/TWN, AMR, MEA`) and its specific universes and submission rules.
- Build **Global (`GLB`)** and **Region-Agnostic (`RA Parent`)** Alphas that pass sub-geography Sharpe cutoffs (`AMER >= 1, APAC >= 1, EMEA >= 1`).
- Adapt signals across regional microstructure differences (such as the `HKG/KOR/TWN` circuit-breaker sign-flip asymmetry and `Max Trade = ON` rule).
- Identify what is documented vs. still uncaptured regarding **Cluster Alphas**.

## 2. Prerequisites

- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)
- [12 — Advanced Alpha Research](../12-advanced-alpha-research/index.md)

## 3. Core Concepts: Master Regional Specifications Table

Every region on WorldQuant BRAIN has distinct universe sizes, liquidity characteristics, and extra submission checks (`[Platform]`, `[Observed]`):

| Region | Genius Tier Required | Key Universes (`[Platform]`) | Region-Specific Submission Rules & Microstructure Notes (`[Platform]`, `[Observed]`) |
|---|---|---|---|
| **USA** | Bronze / Gold | `TOP3000, TOP2000, TOP1000, TOP500, TOPSP500 (~650), ILLIQUID_MINVOL1M` | Most crowded scope on BRAIN. `TOPSP500` has higher industry diversification than `TOP500` and tolerates higher turnover. |
| **EUR** | Gold | `TOP2500 (~2,500), TOPCS1600 (~1,600), TOP1200, TOP800, TOP400` | Less crowded than USA. **Double neutralization (`country x industry`)** strongly recommended. `TOPCS1600` requires upper-40% cap bucket performance (`60–100`), investability-constrained `Sharpe > 0.8`, `Margin > 5‱`, and surviving a `rank()` wrapper test (`[Platform]`). In sweeps (`068, 069`), universes below `TOP1200` (`TOP800, TOP400`) collapsed (`Sharpe <= 0.87`) (`[Observed]`). |
| **GLB / ALL** | Gold | `TOPDIV3000 (~2,200), TOP3000, MINVOL10M, MINVOL1M, LARGE (~9,000)` | **Delay-1 only** due to global time-zone differences. Must pass **Sub-Geography Sharpe >= 1.0 in all 3 regions: `AMER >= 1.0`, `APAC >= 1.0`, `EMEA >= 1.0`**. `TOPDIV3000` is ~50% USA, ~25% EUR, ~25% ASI + AMR (`[Platform]`). |
| **ASI** | Gold | `TOP500, MINVOL10M, MINVOL1M` | Shorter market trading hours and distinct market microstructure; `MINVOL10M` & `TOP500` offer higher liquidity and lower trading costs (`[Platform]`). |
| **CHN** | Gold | `TOP2000, TOP3000` | Stricter headline thresholds: **D1 requires `Sharpe >= 1.625, Returns >= 6.3%, Fitness >= 1.0`**; **D0 requires `Sharpe >= 2.60, Returns >= 8.9%, Fitness >= 1.3`** (`[Platform]`). |
| **IND** | Gold | `TOP500` (top 500 by liquidity) | Requires **Robust Universe Sharpe `>= 1.0`** and **Maximum Turnover `< 40%`** (`[Platform]`). |
| **AMR** | Master | `TOP600` (~600–650 stocks across Americas) | Heavy sector concentration in Basic Materials, Energy, Financials, and Industrials (Canada weight). High volatility & transaction costs: maximize `Margin`. Neutralize by `country` first. In Sweep `071 d2`, `LOW_SHARPE` still fired at `Sharpe 1.4–1.6` (`[Platform]`, `[Observed]`). |
| **JPN** | Master | `TOP1200, TOP1600` | Large single-country cross-section (`1,200–1,600` stocks); expect lower baseline Sharpe than emerging markets (`[Platform]`). |
| **HKG / KOR / TWN** | Grand Master | `TOP800, TOP600` | 1. **`Max Trade = ON` is mandatory**.<br>2. **Sign-Flip Asymmetry:** In `KOR` and `TWN` (and `CHN`), `(-1) * Alpha` is **NOT** the exact opposite PnL because of daily price-limit circuit breakers.<br>3. **Turnover & Margin targets:** `HKG` & `KOR` keep `Turnover < 30%`; `TWN` aim for `Margin >= 10 bps` (`[Platform]`). |
| **Illiquid Universes** | Gold | `ILLIQUID_MINVOL1M` | Higher return potential per trade but severe transaction-cost sensitivity; keep turnover low and verify investability-constrained metrics (`[Platform]`). |

## 4. Step-by-Step Explanations

### Step 1: Building Global (`GLB`) and Region-Agnostic (`RA Parent`) Alphas

1. **What is an `RA Parent` Alpha?** In global/multi-region competitions (such as the All Region Competition 2026), qualifying Alphas must be of type `RA Parent` with `Delay 1` (`[Platform]`). A region-agnostic expression uses universal economic ratios (such as `ebitda / enterprise_value` or `anl69` consensus revisions) rather than region-specific dataset quirks so the same mathematical logic transfers across markets.
2. **Balancing `AMER`, `APAC`, and `EMEA` in `GLB`:** Because `GLB` requires sub-geography Sharpe `>= 1.0` in all three continental zones simultaneously (`[Platform]`):
   - Always use **price-relative or size-relative ratios** (never raw local-currency values, since JPY, KRW, USD, and EUR scales differ by orders of magnitude).
   - Apply **Double Neutralization** (`group_cartesian_product(country, industry)`) so a country with high inflation or currency drift does not dominate the portfolio (`[Platform]`).
   - Inspect the **PnL by Geography** chart on the simulation results page to spot which zone (`AMER`, `APAC`, or `EMEA`) is dragging down sub-geography Sharpe (`[Platform]`).

### Step 2: Cross-Regional Transfer Protocol

Our multi-region sweep (`071`) demonstrated that **slow analyst consensus levels (`anl69_*`, `anl4_*`) wrapped in `ts_scale(ts_backfill(x, 21), 63)`** achieved top risk-adjusted performance in both **EUR (`TOP2500`, Sharpe `1.97`, Fitness `1.58`)** and **KOR (`TOP600`, Sharpe `2.36`, Fitness `1.67`)** (`[Observed]`). When transferring an Alpha from one region to another:

1. Verify field coverage (`>= 70%`) in the target region's Data Explorer.
2. Adjust neutralization (`Subindustry` in `USA TOP3000` -> `COUNTRY` or `country x industry` in `EUR TOP2500` / `GLB TOPDIV3000` -> `INDUSTRY` in `KOR TOP600`).
3. Respect regional settings (`Max Trade = ON` and `Turnover < 30%` in `KOR/HKG/TWN`).

### Step 3: Cluster Alphas — Current Knowledge & Research Gap Placeholder

> **Documented vs. Uncaptured Material (`[Notes]`):**
> - **What is supported in this repository:** Grouping and clustering stocks via `bucket(rank(x), range="...")`, `group_cartesian_product(g1, g2)`, and alternative industry classifications (`pv29` Derived and `pv30` Alternate industry datasets in `GLB`, `[Platform]`) are documented and tested (e.g., cap-decile clustering in Simulation `026`).
> - **Explicit Research Gap / Placeholder:** If a specific WorldQuant BRAIN thematic competition or future platform module defines a dedicated **"Cluster Alpha"** submission type or Cluster Theme rulebook beyond standard group/bucket operators and Pyramid themes, those specific rules have not yet been captured in the offline documentation archive. When official Cluster Alpha guidelines are shared, add the source capture to `Books/official-documentation/` and document the verified rules here.

## 5. Working Examples: Transferring an Analyst Alpha Across `EUR`, `KOR`, and `GLB`

```text
/* Universal slow-analyst revision expression adaptable across EUR, KOR, and GLB TOPDIV3000 */
sig = ts_scale(ts_backfill(anl69_ebitda_best_eeps_cur_yr, 21), 63);
ctry_ind = group_cartesian_product(country, industry);
group_neutralize(sig, ctry_ind)
```

## 6. Common Mistakes and Troubleshooting

- **Negating a negative-Sharpe Alpha in `KOR`, `TWN`, or `CHN` and expecting `+Sharpe`:** Due to circuit breakers and trade execution mechanics in these Asian markets, `-1 * Alpha` does not simply invert the PnL curve (`[Platform]`). Always re-simulate and inspect the actual PnL.
- **Using raw unscaled fields across multiple currencies in `EUR`, `ASI`, or `GLB`:** A figure of `1,000` in Japanese Yen or Korean Won is tiny compared to `1,000` in Euros or Pounds. Always normalize within each instrument's own time series (`ts_rank`, `ts_scale`, `ts_zscore`) or within `country` groups (`group_rank(x, country)`) (`[Platform]`).

## 7. Practical Exercises

1. Compare the failure distribution across `KOR` (`d1`), `AMR` (`d2`), `EUR` (`d3`), `ALL` (`d4, d6`), and `USA` (`d5`) in [`071_multi_region_bundle_20261009.md`](../../Analysis%20and%20Simulation%20Reports/simulation-results/multi-region/071_multi_region_bundle_20261009.md).
2. Design a 3-scope Osmosis roadmap using `USA D1`, `EUR D1`, and `GLB D1` (`TOPDIV3000`).

## 8. Related Topics and Next Steps

- **Next Module:** [14 — BRAIN API and Automation](../14-brain-api-and-automation/index.md)
- **Regional Simulation Records:** [Simulation Results by Region](../../Analysis%20and%20Simulation%20Reports/simulation-results/README.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Regions and Universes* series (`global-region`, `getting-started-glb-topdiv3000-universe`, `getting-started-eur-top2500-universe`, `getting-started-eur-topcs1600-universe`, `china-region-consultants`, `getting-started-india-alphas`, `getting-started-jpn-alphas`, `getting-started-hkgkortwn`, `getting-started-amr-alphas`, `getting-started-mea-region`, `getting-started-illiquid-universes`) (`[Platform]`, captured 2026-10-06/09); empirical sweep `071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
