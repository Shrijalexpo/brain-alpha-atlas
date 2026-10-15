# 16 — Quantitative Research Methodology & Operating Standards

## 1. Learning Objectives

By completing this module, you will be able to:

- Adhere to all **WorldQuant BRAIN Consultant Dos and Don'ts** regarding compliance, account security, and research integrity.
- Translate academic finance papers and formula collections into testable Fast Expression hypotheses without overfitting.
- Execute the repository's **Duplicate Avoidance Protocol** and **Single-Mechanism Iteration Workflow** before proposing or running any new Alpha.

## 2. Prerequisites

- [06 — Alpha Research and Construction](../06-alpha-research-and-construction/index.md)
- [08 — Submission Checks and Consultant Eligibility](../08-submission-and-eligibility/index.md)

## 3. Core Concepts

### 1. Official Consultant Operating Guidelines (Compliance Dos & Don'ts)

Violation of platform operating rules can result in immediate account suspension or termination (`[Platform]`).

| Category | Mandatory Dos (`[Platform]`) | Strict Don'ts (`[Platform]`) |
|---|---|---|
| **Account & Identity** | Keep personal, employment, and country-of-residence details accurate; **recertify your BRAIN account every 3 months**. | Never share login credentials, digital certificates, or User Codes; never maintain duplicate accounts (deactivate any accidental duplicate at `https://platform.worldquantbrain.com/deactivate`). |
| **Confidentiality** | Discuss general research concepts only in official BRAIN Community forums, advisory calls, or registered teams. | **Never share your exact Alpha code, Alpha details, or payout information** with any unauthorized person or on public forums/social media. |
| **Platform Load & API** | Follow BRAIN API rate limits (`X-Ratelimit-*` and `Retry-After`) and read Help Center FAQs before opening support tickets. | Never engage in screen scraping, database scraping, spidering, or deploying scripts that overload platform servers. |
| **Research Integrity** | Ensure every Alpha has a clear **economic foundation** explainable in under 1 minute; use automation only to eliminate redundant mechanical work. | **Never inject random noise into an Alpha to lower production correlation**; never use automation to blindly generate random Alpha ideas. |

### 2. Quantitative Overfitting Guards

Backtest overfitting is the primary reason Alphas with high In-Sample Sharpe fail in Out-of-Sample production (`[Platform]`, `[Notes]`):

1. **Parameter Discipline:** Restrict lookback windows to standard calendar horizons: **`5, 20 (or 21), 60 (or 63), 120 (or 126), 252` trading days** (`[Platform]`). Never tune a window from `20` to `17` or `37` just to squeeze out `+0.05` IS Sharpe.
2. **Structural Simplicity:** Avoid combining Signals from unrelated datasets without a clear economic link, and avoid deep `if_else` branching trees or Narrow signal presetting (`[Platform]`).
3. **Multi-Universe Stability Check:** While tuning an idea, test it across multiple sub-universes (`TOP500`, `TOP1000`, `TOP2000`, `TOP3000` in USA; `TOP2500`, `TOPCS1600`, `TOP1200`, `TOP800` in EUR) (`[Platform]`). If an Alpha works in `TOP3000` but collapses in `TOP2000` and `TOP1000`, it is overfit to illiquid small-caps.
4. **The `rank()` Robustness Test:** Wrap your final expression in `rank(alpha)` and verify that Sharpe remains positive and comparable (`[Platform]`). If ranking destroys the Sharpe ratio, your PnL is driven by extreme cardinal outliers in a few stocks.

## 4. Step-by-Step Explanations

### Step 1: Workflow for Building Alphas from Academic Research Papers

WorldQuant BRAIN recommends a 4-stage process for turning academic papers, blogs, or SSRN/arXiv preprints into production Alphas (`[Platform]`):

1. **Extract the Core Economic Mechanism:** Identify the paper's central anomaly (for example, *firms with rising operating cash flow relative to assets and declining accrual bloat outperform peers*). Ignore complex econometric regressions that cannot be expressed cleanly in cross-sectional panels.
2. **Map Paper Variables to BRAIN Datasets:** Search Data Explorer by theme (`cashflow_op`, `assets`, `operating_income`, `anl69_*`, `option6`) and inspect coverage (`>= 70%`) and field type (`Matrix` vs `Vector`).
3. **Simulate the Simplest Baseline First:** Implement the core ratio with standard normalization (`rank(a / b)` or `ts_rank(a / b, 126)`) and appropriate peer neutralization (`Industry` or `Subindustry`).
4. **Diversify Across Variations and Regions:** Once the core mechanism shows positive Sharpe, test legitimate structural variations (different denominators, `ts_scale` vs `ts_quantile`, or transferring to `EUR`, `GLB`, `KOR`, `AMR`) rather than over-complicating a single expression (`[Platform]`).

### Step 2: Mandatory Duplicate-Avoidance Protocol

Before suggesting or simulating any new Alpha candidate in this workspace (`[Notes]`):

1. Check [`status-and-duplicate-ledger.md`](../../Analysis%20and%20Simulation%20Reports/alpha-research/status-and-duplicate-ledger.html) and [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/).
2. **Never repeat** an exact expression marked `FAILED`, `ERROR`, `FAILED_SELF_CORRELATION`, `PASSED_SUBMITTABLE`, or `PASSED_SUBMITTED`.
3. Treat submitted Alphas (`026`, `027`, `053`) as **protected baselines**: you may study why they worked, but any new candidate in that family must change a real economic mechanism while monitoring self-correlation (`< 0.70`).
4. Generate and test **at most 1 to 3 candidate Alphas at a time**, recording the outcome of each iteration before designing the next (`[Notes]`).

## 5. Working Examples: Current Research Priorities

Based on the evidence accumulated across all 71 experiments and 13,319 sweep blocks (`[Observed]`, `[Notes]`):

1. **Priority 1 — EUR & KOR Slow Analyst Single-Dataset (ATOM / Power Pool) Alphas:** Build on the `anl69_*` and `anl4_*` families using `ts_scale(ts_backfill(x, 21), 63)` and `ts_quantile(ts_backfill(x, 21), 63)`, specifically targeting repairs for `LOW_2Y_SHARPE` and `LOW_SUB_UNIVERSE_SHARPE` (via `country x industry` double neutralization or cap-bucket conditioning).
2. **Priority 2 — Turnover-Band Repair on `pv37_*` Intraday Snapshot Volume:** Preserve the high raw EUR Sharpe (`up to 2.51` in `068`) while smoothing turnover below `30%` to qualify for the IS Ladder `0.85x` PASS relaxation.
3. **Priority 3 — `EUR TOPCS1600` & `GLB TOPDIV3000` Scope Expansion:** Develop 10+ uncorrelated Alphas in at least two non-USA scopes (`EUR D1` and `GLB D1` or `KOR D1`) to unlock the **Osmosis** 3-scope multiplier.

## 6. Common Mistakes and Troubleshooting

- **Testing 20 random formulas at once without logging:** Leads to repeated dead ends and quota exhaustion. Follow the [Command & Workflow Playbook](../reference/command-and-workflow-playbook.md) (`#new`, `#fix`, `#save`, `#learn`).

## 7. Practical Exercises

1. Review the [Command & Workflow Playbook](../reference/command-and-workflow-playbook.md) and the [Simulation Record Template](../../Analysis%20and%20Simulation%20Reports/alpha-research/simulation-template.html).
2. Take one formula from [`Books/README.md`](../../Books/README.md), explain its economic meaning in one sentence, and adapt its operator structure onto a fundamental or analyst field in `EUR`.

## 8. Related Topics and Next Steps

- **Next Module:** [17 — Case Studies and Lessons Learned](../17-case-studies-and-lessons-learned/index.md)
- **Playbook Reference:** [Command and Workflow Playbook](../reference/command-and-workflow-playbook.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *Consultant Dos and Don'ts*, *Finding Consultant Alphas*, and repository workflow guides (`[Platform]`, `[Notes]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
