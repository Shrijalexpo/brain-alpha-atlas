# 04 — Data Explorer and Datasets

## 1. Learning Objectives

By completing this module, you will be able to:

- Navigate the WorldQuant BRAIN data hierarchy (`Dataset Category -> Dataset -> Data Field`).
- Distinguish **Matrix**, **Vector**, and **Group** data fields and apply the required conversion operators (`vec_*`, `group_*`).
- Run Fast Expression diagnostic probes to inspect an unfamiliar field's coverage, non-zero rate, update frequency, and distribution before building an Alpha.
- Apply the 5-step field selection priority protocol rather than sorting blindly by lowest Alpha count.

## 2. Prerequisites

- [03 — WorldQuant BRAIN Fundamentals & Simulation Settings](../03-worldquant-brain-fundamentals/index.md)

## 3. Core Concepts

### Data Hierarchy on BRAIN

WorldQuant BRAIN organizes data into three levels (`[Platform]`):

```text
Dataset Category (e.g., Price Volume, Fundamental, Analyst, Option, Sentiment, Model, Risk)
  └── Dataset (identified by long name and short ID, e.g., pv1, fnd6, anl69, option6, model77)
        └── Data Field (individual time series per instrument, e.g., close, ebitda, anl69_sales_best_eeps_cur_yr)
```

### The Three Data Field Types

| Field Type | Structure | Examples | How to Use in Fast Expression |
|---|---|---|---|
| **Matrix** | Exactly one scalar value per instrument per date ($D \times I$) | `close`, `returns`, `cap`, `ebitda`, `sales_growth` | Ready for direct use with arithmetic, cross-sectional (`rank`), and time-series (`ts_*`) operators (`[Platform]`) |
| **Vector** | Zero, one, or multiple event values per instrument on a single date | News releases, broker-level analyst revisions, short-interest quotes (`shrt3_bar`) | **Must** be reduced to a Matrix first using a `vec_*` operator (`vec_avg`, `vec_sum`, `vec_count`, `vec_stddev`, `vec_ir`, `vec_max`, `vec_min`, `vec_percentage`) (`[Platform]`) |
| **Group** | Categorical bucket identifier per instrument per date | `market`, `sector`, `industry`, `subindustry`, `country`, `exchange`, or `bucket(rank(cap), ...)` | Passed as the second argument to `group_*` operators (`group_rank(x, group)`, `group_neutralize(x, group)`, `group_backfill(x, group, d)`) (`[Platform]`) |

> **Important Exception:** Universe indicator fields (such as `top2000`) are neither predictive Matrix signals nor boolean events. Passing `top2000` as the first argument to `trade_when(top2000, alpha, -1)` raises a validation error because `trade_when` requires a boolean condition such as `volume > adv20` (`[Observed]`).

## 4. Step-by-Step Explanations

### Step 1: The 5-Step Field Selection Protocol

Do **not** pick fields solely because their `Alphas` count in Data Explorer is near zero (`[Notes]`). A zero count often signals a broken, low-coverage, or non-predictive identifier field (such as currency codes or report dates). Follow this priority order (`[Platform]`, `[Notes]`):

1. **Economic Intuition:** State in one sentence why this field should predict future cross-sectional stock returns and what sign (`+` or `-`) it should carry.
2. **Instrument Coverage (`>= 70%`, ideally `>= 85%`):** Check the `Coverage` column in Data Explorer. Low-coverage fields leave most of the universe at `NaN` and trigger `CONCENTRATED_WEIGHT` or `LOW_SUB_UNIVERSE_SHARPE`.
3. **Data Type (`Matrix` first, then `Vector` with `vec_*`):** Confirm whether the field is Matrix or Vector before applying `ts_*` operators.
4. **Historical Date Coverage (`>= 8–10 years`):** Short-history datasets fail multi-year in-sample stability checks (`IS_LADDER_SHARPE`).
5. **Value Score & Alpha Count (Secondary tie-breaker):** Prefer datasets with high platform Value Scores and moderate Alpha counts once criteria 1–4 are satisfied (`[Platform]`).

### Step 2: Diagnostic Probes for Unfamiliar Fields

Before writing a complex Alpha around a new field `x`, you can inspect its behavior directly in the simulator (`[Platform]`):

| Diagnostic Question | Fast Expression Probe | What to Look For in Results |
|---|---|---|
| **Is coverage adequate across time?** | `is_nan(x) ? 0 : 1` (or inspect Long/Short instrument counts on `rank(x)`) | Total active instruments (`long_count + short_count`) should be close to the universe size (e.g., `> 2,400` in `TOP3000`) |
| **How often does the field update?** | `ts_step(1) - ts_arg_max(x != delay(x, 1) ? ts_step(1) : 0, 252)` (or check turnover of `ts_delta(x, 1)`) | Daily fields have high 1-day delta turnover; quarterly/slow fields change only every ~21–63 days |
| **Needs backfilling?** | `ts_backfill(x, 21)` or `ts_backfill(x, 63)` | Essential for quarterly fundamentals and periodic analyst estimates so stocks do not drop out between reporting dates (`[Platform]`) |

## 5. Working Examples

### Example 1: Converting a Vector Field to a Matrix Signal

```text
/* Reduce intra-day or multi-analyst vector values to a daily mean before time-series ranking */
daily_signal = vec_avg(scl12_alltype_buzzvec);
rank(-ts_std_dev(ts_backfill(daily_signal, 21), 10))
```

### Example 2: Backfilling a Slow Analyst Field (`anl69`)

```text
/* Backfill up to 21 trading days of missing observations, then scale over a 63-day quarter */
ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)
```
*(Produced Sharpe `1.97`, Fitness `1.58`, Turnover `5.78%` in EUR `TOP2500` Simulation [`067`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/067_eur_top2500_country_analyst_sweep.html), `[Observed]`.)*

## 6. Common Mistakes and Troubleshooting

- **Applying `ts_delta` directly to event/vector estimate fields:** Simulations [`042`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/042_estimate_eps_delta_error.html) (`eps_estimate_value`) and [`043`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/043_estimate_sales_delta_error.html) (`sales_estimate_value`) failed validation with event-input errors (`[Observed]`). Always check whether an estimate field is Vector/Event type and convert with `vec_avg()` or `ts_backfill()` first.
- **Using technical metadata fields as signals:** Fields like `adjfactor`, `*_currency_code`, or `expected_report_*` variance fields produced degenerate sub-1% turnover or step-function artifacts in EUR sweeps (`068`, `069`) (`[Observed]`).

## 7. Practical Exercises

1. Read the companion [Dataset Catalog & Field Notes](dataset-catalog-and-field-notes.md) to review every dataset family tested in this repository (`pv1`, `pv37`, `fnd6`, `anl4`, `anl10`, `anl69`, `option6`, `model77`, `sentiment1`).
2. Compare the failure modes of `anl10_*` vs `anl69_*` in [`SUMMARY.md`](../../Analysis%20and%20Simulation%20Reports/sweeps-and-experiments/SUMMARY.html).

## 8. Related Topics and Next Steps

- **Companion Catalog:** [Dataset Catalog and Empirical Field Notes](dataset-catalog-and-field-notes.md)
- **Next Module:** [05 — Fast Expression Language](../05-fast-expression-language/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Understanding Data in BRAIN: Key Concepts and Tips*, *How to Use the Data Explorer*, *Vector Data Fields*, *Group Data Fields*, *Option6 Implied Volatility*, *Model77*, and *Sentiment1* (`[Platform]`, captured 2026-07-26 and 2026-10-09); repository experiments `001`–`071` (`[Observed]`).
- **Verification Date:** 2026-10-15.
