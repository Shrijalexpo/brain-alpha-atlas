# Sources and Evidence Policy

How claims in this knowledge base are tagged, how sources are attributed, and what material is kept local (`[Notes]`).

## 1. Evidence Tags

Every non-obvious factual claim, threshold, or empirical finding carries an inline provenance tag:

| Tag | Meaning | Authority Level |
|---|---|---|
| `[Platform]` | Official WorldQuant BRAIN documentation, Help Center article, or observed simulator behavior with a capture date | Authoritative for its capture date; always verify live platform rules before submitting |
| `[Observed]` | Measured directly in a simulation or multi-simulation sweep committed in [`Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/) | Empirical backtest evidence under the stated settings and historical window |
| `[Notes]` | Repository research workflow rules, mathematical derivations, or synthesis decisions | Internal engineering standard |
| `[Hypothesis]` | Plausible quantitative interpretation not yet isolated by a controlled experiment | Treat as a testable lead, never as an established fact |
| `[External]` | Published academic paper, textbook, or open-source factor library cataloged in [`Books/README.md`](../../Books/README.md) | External literature citation |

## 2. Research Integrity Rules

1. **No Fabricated Numbers or Rules:** Never invent operator names, field semantics, submission thresholds, API endpoints, or simulation metrics. Where a value was not captured in a screenshot or export, record it as `unknown` or `—`.
2. **Scope Specificity:** Backtest outcomes apply only to the `Region`, `Universe`, `Delay`, `Neutralization`, `Decay`, and historical window in which they were simulated. Never average metrics across incompatible scopes.
3. **Training vs. Out-of-Sample Separation:** Never report `Train Sharpe` as `Sharpe`.
4. **No Investment or Compensation Claims:** All recorded metrics are historical simulation outputs for educational and research tracking; nothing in this repository constitutes investment advice or a guarantee of consultant payouts.

## 3. Repository Privacy and Licensing Boundaries

- **Code (`Tools/**/*.py`, `.github/workflows/*.yml`, `mkdocs.yml`):** Licensed under **MIT** ([`LICENSE`](../../LICENSE)).
- **Curated Documentation & Analysis (`Docs/`, `README.md`, `Analysis and Simulation Reports/`):** Licensed under **CC BY 4.0** ([`LICENSE-DOCS`](../../LICENSE-DOCS)).
- **Third-Party Works & Official Captures (`Books/`, `Tools/api-and-automation/ace-api/`):** Retained locally for research reference and excluded from public redistribution via `.gitignore` (see [`NOTICE`](../../NOTICE)).
