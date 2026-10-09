# Alpha Research Workflow

This file stores the practical workflow learned from the conversation.

Also use:

```text
Research/alpha_improvement_from_docs.md
Research/neutralization_guidelines.md
Data/data_explorer_and_field_research.md
Operators/worldquant_brain_operator_reference.md
```

## Core Principle

Do not hunt for a magic field. Build testable economic ideas.

Good alpha research process:

```text
Business idea
-> relevant fields
-> clean ratio or transform
-> first simulation
-> diagnose bottleneck
-> one controlled change
-> record result
```

## Field Selection Workflow

When choosing fields in Company Fundamental Data for Equity:

1. Search by theme, not only by alpha count.
2. Prefer Matrix fields.
3. Check coverage and date coverage.
4. Read the field description.
5. Write the economic intuition before testing.
6. Test a simple ratio before building a composite.

Do not choose the field with the least submitted alphas by default.

Low alpha count can mean:

- new or underexplored,
- difficult to use,
- low coverage,
- weak predictive value.

High alpha count can mean:

- crowded,
- but also genuinely useful.

## Theme-Based Search Plan

Profitability:

```text
return_equity
return_assets
gross_margin
gross_profit
ebitda
net_income
operating_income
```

Valuation:

```text
enterprise_value
market_cap
book_value
bookvalue_ps
price_to_book
ev
```

Cash flow:

```text
cashflow_op
operating_cash_flow
free_cash_flow
cash
```

Growth:

```text
sales_growth
revenue_growth
eps_growth
asset_growth
```

Balance sheet:

```text
assets
debt
liabilities
current_ratio
leverage
```

Analyst expectations:

```text
analyst
estimate
revision
eps_estimate
target_price
recommendation
```

## Controlled Experiment Rules

- Change one thing at a time.
- If a base factor has negative Sharpe, do not build a complex composite from it.
- If a base factor has weak positive Sharpe, add one complementary factor.
- If a composite gets worse, return to the best simple component.
- Record every simulation in `simulations/`.

## Diagnosis Rules

Low Sharpe:

- Improve signal idea.
- Try a better field or ratio.
- Consider group/industry neutralization.

Low Fitness with high Turnover:

- Increase Decay.
- Smooth return or volume terms.
- Lower coefficients on fast terms.

Low Fitness with low Turnover:

- Returns are probably too weak.
- A stronger or more selective signal is needed.

Negative Sharpe:

- Reverse only if the economic intuition supports it.
- Otherwise discard or isolate components.

## Current Research State

The operating income family was weak:

```text
operating_income
operating_income / cap
operating_income / enterprise_value
```

The large quality/value composite was weak.

The nonlinear profitability/cashflow product was worse.

The current best base signal from the latest recorded tests is:

```text
cashflow_op / enterprise_value
```

Next research direction:

- Pair cash flow yield with exactly one complementary factor.
- First suggested factor: `return_equity`.
- If that fails, try growth or balance sheet strength rather than stacking more quality factors.
