# Data Explorer And Field Research

Source: BRAIN Learn > Documentation > Understanding Data, captured through Computer Use on 2026-07-26.

## Data Fundamentals

A data field is a named collection of data with constant type and business meaning.

Examples:

- `open` and `close` are both numeric price fields, but have different business meanings.
- `returns`, `cap`, and `close` are Matrix fields.

A dataset is a collection of data fields. A dataset can be identified by:

- long explanatory name,
- short dataset ID, mainly relevant for advanced scripting.

## Matrix Fields

Matrix fields have one value per date and instrument.

Examples:

```text
close
returns
cap
```

These can be used directly in simulations.

## Vector Fields

Vector fields can have more than one value per date and instrument.

Examples:

- News events: different instruments may have different numbers of news items per day.
- Sentiment scores: one stock may have several event scores on the same day.

Rule:

- Convert vector fields to matrix fields with `vec_*` operators before using ordinary matrix operators.
- The final alpha must be a matrix of alpha values because BRAIN takes one position per instrument per date.

Useful vector conversions:

```text
vec_avg(x)
vec_sum(x)
vec_count(x)
vec_max(x)
vec_min(x)
vec_stddev(x)
vec_ir(x)
vec_range(x)
vec_skewness(x)
vec_kurtosis(x)
vec_percentage(x, percentage=0.5)
vec_choose(x, nth=k)
```

## Data Explorer Workflow

Data Explorer helps identify fields for an alpha idea.

Before searching:

- set region,
- set delay,
- set universe.

Reason:

- Some fields exist only for certain regions/delays/universes.

Search modes:

- Search based on an idea, e.g. market sentiment.
- Filter fields by coverage, type, Alpha count, user count, dataset, and other criteria.
- Search datasets by category or dataset name.

Rule of thumb:

- Use the `3S` search rule: short, simple, straightforward.
- Use domain terminology when known.
- If the exact term is unknown, describe the idea plainly.
- For well-known concepts, search both full name and abbreviation.

Examples:

```text
earnings per share
eps
implied volatility
IV
trade by people inside company
```

## Field Diagnostic Expressions

Use these expressions to understand a field before building alphas from it.

Coverage estimate:

```text
datafield
```

Approximate coverage:

```text
(Long Count + Short Count in IS Summary) / Universe Size
```

Non-zero coverage:

```text
datafield != 0 ? 1 : 0
```

Unique update frequency:

```text
ts_std_dev(datafield, N) != 0 ? 1 : 0
```

Interpretation:

- For quarterly fields, using `N = 66` may show coverage near actual coverage.
- `N = 22` may show lower counts for quarterly data.
- `N = 5` may show even lower counts for slow-updating fields.

Bounds:

```text
abs(datafield) > X
```

Median over about 5 years:

```text
ts_median(datafield, 1000) > X
```

Distribution:

```text
X < scale_down(datafield) && scale_down(datafield) < Y
```

Note:

- `scale_down` acts like a MinMaxScaler and preserves the original distribution shape.

Example sanity check:

```text
close <= 0
```

Expected result:

- Long and Short Counts should be 0, because closing price should be positive.

## Dataset Value Score

Dataset Value Score is available for consultants.

Meaning:

- It indicates dataset underutilization.
- Consultants are advised to research datasets with higher value score.

Important:

- Do not confuse Dataset Value Score with a value factor.

## Data Coverage

Coverage means the fraction of instruments in the universe for which a field has a defined value.

Low coverage can be handled with:

```text
ts_backfill
kth_element
group_backfill
```

Also use visualization features to inspect field coverage.

