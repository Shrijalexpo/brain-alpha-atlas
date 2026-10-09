# Field Selection Guide

This guide is distilled from the conversation about choosing fields in Company Fundamental Data for Equity.

For official BRAIN Data Explorer notes and field diagnostic expressions, see:

```text
Data/data_explorer_and_field_research.md
```

## Do Not Choose Only By Lowest Alpha Count

The `Alphas` count tells how often a field has been used, not whether it is predictive.

Low count can mean:

- underexplored,
- new,
- hard to use,
- low coverage,
- weak signal.

High count can mean:

- crowded,
- but also useful and economically meaningful.

## Better Field Selection Criteria

Use this order:

1. Economic intuition.
2. Coverage above 70%, ideally 90% or more.
3. Matrix type preferred.
4. Long date coverage.
5. Alpha count as a secondary hint.

## Matrix Vs Vector

Matrix:

- One value per stock per date.
- Preferred for ordinary alpha construction.
- Works naturally with `rank`, `ts_mean`, `ts_rank`, `ts_delta`.

Vector:

- Often event-oriented or metadata-like.
- Less flexible for beginner alpha construction.

## Theme Search Beats Random Search

Search by concepts:

```text
income
profit
cash
asset
debt
equity
margin
growth
expense
revenue
sales
inventory
dividend
book
```

## Fundamental Field Transformation Ideas

Raw field:

```text
operating_income
```

Often weak because it mostly captures company size.

Better ratios:

```text
operating_income / assets
operating_income / enterprise_value
operating_income / market_cap
operating_income / sales
cashflow_op / enterprise_value
cashflow_op / assets
debt / assets
enterprise_value / ebitda
```

## Practical Research Rule

For every new field, write this before simulating:

```text
Why might this predict returns?
Should high values be long or short?
Does the raw field need a denominator?
Is it slow-moving quarterly data?
What group should it be compared within?
```
