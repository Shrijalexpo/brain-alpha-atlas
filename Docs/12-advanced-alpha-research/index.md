# 12 — Advanced Alpha Research: Risk Neutralization, D0, SuperAlphas & Python Alphas

## 1. Learning Objectives

By completing this module, you will be able to:

- Apply **Double Neutralization** (`group_cartesian_product(country, industry)`) and **Factor / Risk Neutralization** (`SLOW`, `FAST`, `SLOW_AND_FAST`, `CROWDING`, `STATISTICAL`, `RAM`, `vector_neut`, `regression_neut`).
- Build **Delay-0 (`D0`)** and **High-Turnover** Alphas for liquid universes.
- Construct **SuperAlphas** (unlocked at `>= 100` submissions) using `Selection` expressions, `Combo` expressions, and `generate_stats()`.
- Write and simulate **Python Alphas** using the `@alpha` decorator, `BrainCache`, and corporate-action split adjustments (`pv1_split`).

## 2. Prerequisites

- [05 — Fast Expression Language](../05-fast-expression-language/index.md)
- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)

## 3. Core Concepts

### 1. Double Neutralization and Factor Risk Neutralization

In multi-country regions (`EUR`, `GLB`, `ASI`, `AMR`) or crowded factor spaces, single-dimension neutralization (`Industry` alone) leaves unhedged country or style-factor exposure (`[Platform]`):

| Neutralization Technique | How to Implement | When to Use (`[Platform]`) |
|---|---|---|
| **Double Neutralization (`Country x Industry`)** | `grp = group_cartesian_product(country, industry); group_neutralize(alpha, grp)` (or `densify(country) + densify(industry)*100`) | Essential in `EUR TOP2500` and `GLB TOPDIV3000` so stocks are compared against same-country, same-industry peers |
| **Slow / Fast Risk Factors (`SLOW`, `FAST`, `SLOW_AND_FAST`)** | Select in Simulation Settings -> Neutralization | Purges systematic Barra-style slow fundamental risk factors, fast price/momentum factors, or both (`[Platform]`) |
| **Statistical Risk (`STATISTICAL`)** | Select `Statistical` in Neutralization settings | Purges principal-component (PCA) statistical risk factors extracted from the return covariance matrix (`[Platform]`) |
| **Crowding Risk (`CROWDING`)** | Select `Crowding` in Neutralization settings | Orthogonalizes against platform-wide crowded positioning to lower production correlation (`[Platform]`) |
| **RAM Risk (`RAM`)** | Select `RAM` in Neutralization settings | Short-term risk-adjusted market neutralization (`[Platform]`) |
| **Expression Orthogonalization (`vector_neut`, `regression_neut`)** | `vector_neut(alpha, log(cap))` or `regression_neut(alpha, historical_volatility_120)` | Removes linear exposure to a specific continuous variable inside Fast Expression (`[Platform]`) |

> **Global (`GLB`) Risk-Neutralization Caveat:** Selecting `SLOW`, `FAST`, or `SLOW_AND_FAST` in settings resets the group neutralization baseline to `Market` (`[Platform]`). In `GLB`, always apply `group_neutralize(alpha, country)` inside the expression when using Risk Neutralization settings (`[Platform]`).

### 2. Delay-0 (`D0`) and High-Turnover Alphas

- **Delay-0 (`D0`) Alphas:** Use data available prior to the same day's close (`[Platform]`). Because `D0` captures immediate intraday/same-day reaction, submission thresholds are higher:
  - User bar: `Sharpe > 2.0`, `Fitness > 1.3` (`[Platform]`).
  - ATOM D0 2-Year Sharpe bar: `FAIL 2.69 / PASS 3.50` (`[Platform]`).
  - `CHN` D0 bar: `Sharpe >= 2.60`, `Returns >= 8.9%`, `Fitness >= 1.30` (`[Platform]`).
- **Fast D1 Datasets (`*_fast_d1`):** Datasets updated with lower latency before D1 cutoffs (`[Platform]`). In our USA sentiment tests (`038`), raw `fast_d1` sentiment had `87%` turnover and weak Fitness; pair fast datasets with turnover control (`[Observed]`).

### 3. SuperAlphas (Meta-Portfolios of Submitted Alphas)

Unlocked once a consultant has submitted **at least 100 Alphas overall** (`[Platform]`). A SuperAlpha combines `>= 10` active submitted Alphas (`type = SUPER`) using two expressions (`[Platform]`):

1. **Selection Expression (`Selection Limit >= 10`):** Evaluated across your pool of eligible submitted Alphas (plus University/Country/Global pools at Expert/Master/Grand Master). Orders Alphas by selection weight and picks the top $N$ (`Selection Handling`: `Positive`, `Non-Zero`, or `Non-NaN`) (`[Platform]`).
2. **Combo Expression:** Takes the selected Alphas tensor of shape $(A \times D \times I)$ and outputs daily Alpha weights of shape $(D \times A)$ (`[Platform]`).
   - Setting Combo Expression to `1` creates an equal-weighted benchmark (plotted as the gray line on SuperAlpha PnL charts; your custom combo is the blue line and should beat the gray line) (`[Platform]`).
   - **`generate_stats(alpha)` Operator:** Computes daily historical IS performance series of shape $(S \times D \times A)$ for each component Alpha, exposing fields: `pnl`, `returns`, `drawdown`, `sharpe`, `hold_pnl`, `trade_pnl`, `long_count`, `short_count`, `long_value`, `short_value`, `trade_shares`, `trade_value` (`[Platform]`).
   - **Both descriptions required:** Submitting a SuperAlpha requires completing both the Selection Description and Combo Description in `Properties` (`[Platform]`).

### 4. BRAIN Python Alphas (`@alpha`)

Python Alphas allow arbitrary NumPy/SciPy/Pandas logic inside a self-contained single-file module decorated with `@alpha` (`[Platform]`):

| Python Alpha Rule | Specification (`[Platform]`) |
|---|---|
| **Self-Contained Module** | Must be a single file; cannot `import` local helper files |
| **Input Declaration** | `@alpha(data=["close", "volume"], store=[])` — list only Matrix data fields in `data` (never list `"universe"`) |
| **Return Type** | Must return a 1D `np.ndarray` of dtype `np.float32` matching the day's instrument cross-section |
| **Integer Field Sentinels** | Integer fields represent missing values as `np.iinfo(np.int32).min` (`-2147483648`); cast to `float32` and replace with `np.nan` |
| **Corporate Action Split Adjustment** | In `store`-based stateful Python Alphas, adjust stored historical prices across stock splits using `pv1_split` (`stored_price /= data["pv1_split"]`) (`[Platform]`) |

## 4. Step-by-Step Explanations: Translating Fast Expression to Python Alpha

```python
from brain.alphas import alpha
import numpy as np
import numpy.typing as npt

@alpha(
    data=["ebitda", "enterprise_value", "returns"],
    store=["hist_val", "hist_ret"],
)
def value_reversion_alpha(data, store) -> npt.NDArray[np.float32]:
    ev = np.where(data["enterprise_value"] > 0, data["enterprise_value"], np.nan)
    val_ratio = data["ebitda"].astype(np.float32) / ev.astype(np.float32)
    ret = data["returns"].astype(np.float32)
    # Cross-sectional rank helper
    valid = ~np.isnan(val_ratio) & ~np.isnan(ret)
    out = np.full_like(val_ratio, np.nan, dtype=np.float32)
    if np.sum(valid) > 10:
        v_rank = np.argsort(np.argsort(val_ratio[valid])).astype(np.float32) / (np.sum(valid) - 1)
        r_rank = np.argsort(np.argsort(-ret[valid])).astype(np.float32) / (np.sum(valid) - 1)
        out[valid] = v_rank + 0.5 * r_rank
    return out
```

## 5. Working Examples: Double Neutralization in `EUR` / `GLB`

```text
/* Neutralize an analyst signal jointly by Country x Industry in EUR TOP2500 or GLB TOPDIV3000 */
raw_sig = ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63);
ctry_ind = group_cartesian_product(country, industry);
group_neutralize(raw_sig, ctry_ind)
```

## 6. Common Mistakes and Troubleshooting

- **Using `BrainCache` for interactive data exploration in BrainLabs:** `BrainCache` is reserved strictly for `simulate()` calls; use `brain.get_data_frame("field")` when inspecting data shapes and dtypes (`[Platform]`).
- **Forgetting to recreate `BrainCache` after changing Region, Delay, or Date Range:** Cached data is bound to the initial scope (`[Platform]`).

## 7. Practical Exercises

1. Write a Fast Expression that uses `vector_neut(x, y)` to orthogonalize `rank(ebitda / enterprise_value)` against `rank(historical_volatility_120)`.
2. Compare the 5-step LLM translation prompt structure in `Books/official-documentation/brain-platform-docs/how-translate-fast-expression-alpha-python-alpha.md`.

## 8. Related Topics and Next Steps

- **Next Module:** [13 — Region-Agnostic and Cluster Alphas](../13-region-agnostic-and-cluster-alphas/index.md)
- **BRAIN API:** [14 — BRAIN API and Automation](../14-brain-api-and-automation/index.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Double Neutralization*, *Risk Neutralized Alphas* (`Slow/Fast/Crowding/Statistical/RAM`), *D0*, *SuperAlpha Overview / Selection / Combo / Results / Operators*, and *Brain Python Alphas* (`[Platform]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
