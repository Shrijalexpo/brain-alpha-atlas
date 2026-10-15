# 09 — Power Pool and Thematic Competitions

## 1. Learning Objectives

By completing this module, you will be able to:

- Design Alphas that satisfy all **Power Pool** eligibility criteria (`Sharpe >= 1.0`, `<= 8` total operators, `<= 3` data fields, `< 0.5` Power Pool correlation, and mandatory `>= 100`-character Idea/Rationale description).
- Classify hybrid Power Pool submissions (`[Power Pool + ATOM]`, `[Power Pool + Regular]`, `[Power Pool + ATOM + Regular]`) to maximize daily and monthly submission quotas.
- Compete in **Power Pool Thematic Competitions**, **All Region Competitions**, and the monthly **Systematic Prediction Challenge (SPC 2026)** LLM prompt competition.

## 2. Prerequisites

- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)

## 3. Core Concepts

### 1. Power Pool Alphas

Power Pool Alphas are concise, interpretable, low-complexity signals designed to resist overfitting and combine cleanly into institutional portfolios (`[Platform]`).

| Power Pool Criterion | Exact Rule (`[Platform]`) |
|---|---|
| **Minimum Sharpe** | `Sharpe >= 1.00` |
| **Operator Count Limit** | `<= 8` total operators (including repeated operators; **`ts_backfill` and `group_backfill` are NOT counted**) |
| **Data Field Limit** | `<= 3` unique data fields (**excluding** the 6 support grouping fields: `country, industry, subindustry, currency, market, sector, exchange`) |
| **Power Pool Correlation** | `< 0.50` against existing Power Pool Alphas (or `>= +10%` higher Sharpe than the most correlated Power Pool Alpha) |
| **Prod-Correlation Exemption** | Pure Power Pool Alphas are **exempt** from the regular 0.70 platform-wide prod-correlation test |
| **Robustness Checks** | Turnover test `PASS`, Sub-universe test `PASS`, Robust-universe test (where applicable) `PASS` |
| **Mandatory Description** | Must include at least **100 characters** in the `Properties` description box using the **Idea + Rationale** template before submission |

### Hybrid Classifications & Submission Quotas (After 3 Months)

Once a consultant passes 3 months from their first Power Pool submission, submission quotas depend on whether the Alpha is a **Pure Power Pool Alpha** or a **Hybrid** (`[Platform]`):

| Classification | Criteria Passed | Counts Against 1/Day & 10/Month Pure Power Pool Quota? | Counts Against Standard 4/Day Consultant Quota? |
|---|---|---|---|
| **Pure Power Pool** | Power Pool rules + matches active **Power Pool Theme** (does not pass ATOM or Regular IS Ladder) | **Yes** (`<= 1/day`, `<= 10/month` in a single allowed scope) | Yes |
| **`[Power Pool + ATOM]`** | Power Pool rules + Single Dataset + Last 2Y IS Sharpe (`>= 1.59` D1) | **No** (exempt from Pure Power Pool limits) | Yes (up to 4/day) |
| **`[Power Pool + Regular]`** | Power Pool rules + full IS Ladder + Prod-Correlation `<= 0.7` | **No** (exempt from Pure Power Pool limits) | Yes (up to 4/day) |
| **`[Power Pool + ATOM + Regular]`** | Passes all three sets of criteria simultaneously | **No** (exempt from Pure Power Pool limits) | Yes (up to 4/day) |

- **Allowed Scopes for Pure Power Pool (after 3 months):** `USA D0/D1`, `EUR D0/D1`, `ASI D1`, `GLB D1`, and `OTHER (JPN, CHN, HKG, TWN, KOR, AMR, IND) D0/D1` (`[Platform]`).

### 2. Power Pool Thematic Competitions & All Region Competitions

- **Power Pool Thematic Competitions:** Periodic 2–4 week competitions targeting a specific scope or dataset theme (for example, `GLB / D1 / TOPDIV3000 Liquid Power Pool`). Requires at least **5 tagged Power Pool Alphas** on the thematic leaderboard to qualify for placement awards (`[Platform]`).
- **All Region Competition (Seasonal):** 5-week global competition for consultants requiring at least **10 qualifying Alphas** of type `RA Parent` with `Delay 1`, scored on an equal-weighted combined portfolio of In-Sample and Out-of-Sample Sharpe (`[Platform]`).

### 3. Systematic Prediction Challenge (SPC 2026 — Prompt Competition)

SPC is a separate **monthly LLM prompt competition** where the submission is an investment-thesis **prompt** (up to 10,000 characters) executed daily by a chosen LLM (`Claude`, `GPT`, `Gemini`) with web search enabled (`[Platform]`):

| SPC Parameter | Requirement (`[Platform]`) |
|---|---|
| **Active & Daily Limits** | Up to **50 active prompts** total, and at most **50 prompt submissions per day** (including zero-weight prompts) |
| **Portfolio Breadth Target** | Roughly **50 equities per prompt** and **500 distinct stocks** across all active prompts |
| **Update Frequencies** | `Daily`, `Weekly`, `Monthly`, or `Quarterly`; weight `0.0` to `1.0` |
| **Required JSON Output Schema** | JSON array of objects, each containing: `company_name` (string), `ticker` (string), `isin` (valid 12-char ISO 6166 with Luhn mod-10 check digit), `mic` (valid 4-char ISO 10383 Market Identifier Code, e.g. `XNAS`, `XNYS`), `confidence_score` (`-1.0` to `1.0`, sign sets Long/Short direction), `investment_horizon` (positive integer trading days), `return_prediction` (positive float magnitude) |

## 4. Step-by-Step Explanations

### Step 1: Writing a Valid Power Pool Description (`>= 100` Characters)

Before clicking Submit on any Power Pool candidate, open **Properties** at the bottom of the Simulation Results page and fill in the structured template (`[Platform]`):

```text
Idea: In normal market conditions, stocks with rapidly rising analyst consensus sales estimates
relative to their own 1-quarter range outperform industry peers over the subsequent month.
Rationale for data used: anl69_sales_best_eeps_cur_yr captures current-year consensus sales
estimates from the anl69 analyst dataset.
Rationale for operators used:
- ts_backfill(x, 21): Carries forward the most recent estimate for up to 21 trading days.
- ts_scale(x, 63): Normalizes the current estimate within its 63-day (1-quarter) min-max range.
```

### Step 2: Validating SPC Sample JSON Locally Before Submission

Never submit an SPC prompt without validating its sample JSON output against ISO 6166 ISIN check-digit rules using [`validate_spc_isin.py`](../../Tools/alpha-analysis/validate_spc_isin.py):

```bash
python3 Tools/alpha-analysis/validate_spc_isin.py Tools/alpha-analysis/spc_sample_output_example.json
```

## 5. Working Examples: Counting Operators and Fields for Power Pool

Consider the top EUR/KOR slow-analyst expression from Simulations [`067`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/067_eur_top2500_country_analyst_sweep.html) and [`071`](../../Analysis%20and%20Simulation%20Reports/simulation-results/multi-region/071_multi_region_bundle_20261009.html):

```text
ts_scale(ts_backfill(anl69_sales_best_eeps_cur_yr, 21), 63)
```

- **Unique Data Fields:** `1` (`anl69_sales_best_eeps_cur_yr`) — well below the `<= 3` limit.
- **Counted Operators:** `1` (`ts_scale`; `ts_backfill` is exempt) — well below the `<= 8` limit.
- **Dataset Count:** `1` (`anl69`) — simultaneously qualifies for **`[Power Pool + ATOM]`**!

## 6. Common Mistakes and Troubleshooting

- **Exceeding 8 operators via repeated helper calls:** Power Pool counts **repeat occurrences** of operators toward the `<= 8` cap (except `ts_backfill` and `group_backfill`) (`[Platform]`). If you call `rank()` four times and `ts_rank()` three times and `+` twice, that is `9` operators and disqualifies the Alpha from Power Pool.
- **Negative `return_prediction` in SPC JSON:** In SPC, `return_prediction` must always be **positive**; a short recommendation is indicated solely by a negative `confidence_score` (`-1.0` to `0.0`) (`[Platform]`).

## 7. Practical Exercises

1. Count the non-exempt operators and non-grouping data fields in Submitted Alpha [`053`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/053_submitted_ebitda_ev_mean_reversion.html) (`rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))`) and verify that it uses `3` fields (`ebitda, enterprise_value, returns`) and `6` operators (`/, -, ts_mean, rank, rank, +`) — eligible for Power Pool structure!
2. Run `python3 Tools/alpha-analysis/validate_spc_isin.py --selftest` from the terminal.

## 8. Related Topics and Next Steps

- **Next Module:** [10 — Pyramids and Genius Program](../10-pyramids-and-genius-program/index.md)
- **SPC Validator Tool:** [`Tools/alpha-analysis/validate_spc_isin.py`](../../Tools/alpha-analysis/validate_spc_isin.py)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Power Pool Alphas* (`getting-started-power-pool-alphas`), *Single Dataset Alphas*, and Help Center *Systematic Prediction Challenge — SPC 2026* (`[Platform]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
