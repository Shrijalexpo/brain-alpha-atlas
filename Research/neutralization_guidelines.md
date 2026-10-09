# Neutralization Guidelines

Source: BRAIN Learn > Documentation > Advanced Topics > Neutralization, captured through Computer Use on 2026-07-26.

## Basic Concept

Neutralization splits raw alpha values into groups and subtracts the group mean from each value.

Groups may be:

- entire market,
- sector,
- industry,
- subindustry,
- country,
- exchange,
- custom buckets.

Purpose:

- focus on relative returns inside a group,
- reduce market or group risk exposure,
- create a portfolio that is roughly half long and half short.

Example:

```text
Alpha = -ts_delta(close, 5)
Neutralization = Market
```

Conceptually:

```text
Alpha = Alpha - mean(Alpha)
```

Then the vector is normalized and scaled to book size.

## Settings Neutralization Vs `group_neutralize`

`Neutralization` in Simulation Settings neutralizes the alpha as the last step.

`group_neutralize(x, group)` uses the same operation, but can be applied manually inside the expression.

They can be interchangeable when used as the final operation.

Example equivalence:

```text
-zscore(ebit / capex)
```

with `Neutralization = Industry`, `Decay = 0`, `Truncation = 0`

is conceptually similar to:

```text
group_neutralize(-zscore(ebit / capex), industry)
```

with `Neutralization = None`, `Decay = 0`, `Truncation = 0`.

If using `group_neutralize(x, group)` as the last operator:

- set Simulation Settings Neutralization to `None`,
- set Decay to `0`,
- set Truncation to `0`,
- insert decay/truncation operators directly inside the expression if needed.

## Practical Tips

- Always pick a neutralization setting.
- Leave neutralization as `None` only when neutralization is manually incorporated in the expression.
- Try larger groups for more liquid universes with fewer stocks, because each group needs enough stocks.
- Try smaller groups for illiquid universes.
- Use `country` and `exchange` neutralization for EUR and ASI regions when appropriate.

## Recommended Neutralization By Dataset Type

Fundamental datasets:

- Recommended: Industry.
- Reason: fundamentals affect prices differently by industry.

Analyst datasets:

- Recommended: Industry.
- Reason: analyst estimates relate to future fundamentals and should be peer-compared.

Model datasets:

- Recommended: experiment with Market, Sector, Industry, and Subindustry.
- Reason: model datasets vary by subcategory.

News datasets:

- Recommended: Subindustry.
- Reason: news impact differs by company/subindustry.

Option datasets:

- Recommended: Market or Sector.
- Reason: option effects may be similar across broader industries.

Price Volume datasets:

- Recommended: Market or Sector.
- Reason: generic PV ideas often work across instruments; Industry/Subindustry neutralization may reduce performance.

Social media datasets:

- Recommended: Subindustry or Industry.
- Reason: impact differs by company and context.

Institution datasets:

- Recommended: Sector or Industry.
- Reason: depends on provider/type/implication.

Short interest datasets:

- Recommended: Industry.

Insider datasets:

- Recommended: Industry or Subindustry.

Sentiment datasets:

- Recommended: Industry or Subindustry.

Earnings datasets:

- Recommended: Industry.

Macro datasets:

- Recommended: Sector, Market, or Industry.
- Reason: macro effects are broad; subindustry may not add much.

