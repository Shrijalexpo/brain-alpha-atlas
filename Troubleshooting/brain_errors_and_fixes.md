# WorldQuant BRAIN Errors And Fixes

This file stores troubleshooting lessons from the conversation. Update it whenever a new BRAIN error screenshot or Help Center file is shared.

## Universe Field Used As Boolean Event

Problem expression:

```text
trade_when(
    top2000,
    zscore(
        rank(dividend)
        + 0.3 * rank(volume / adv20)
        + 0.2 * rank(-returns)
    ),
    -1
)
```

Issue:

- `top2000` is a Universe-type field.
- The first argument of `trade_when()` must be a boolean event.
- A raw Universe field is not a predictive signal and should not be used directly as an alpha.

Preferred fix:

```text
zscore(
    rank(dividend)
    + 0.3 * rank(volume / adv20)
    + 0.2 * rank(-returns)
)
```

If an actual event filter is needed, use price/volume/fundamental conditions:

```text
trade_when(
    volume > adv20,
    rank(-returns),
    -1
)
```

Possible but uncertain variants:

```text
top2000 == 1
top2000 > 0
```

Only try these if BRAIN allows comparison on that Universe field. If it still fails, treat `top2000` as a pure Universe object that cannot be used in `trade_when()`.

## Weak Fundamental Field Warning

Symptom:

- Raw fundamental fields produce Sharpe below about `0.5`.

Examples:

```text
rank(ts_rank(operating_income, 12))
rank(ts_mean(operating_income, 4))
rank(ts_delta(operating_income, 4))
```

Likely cause:

- Accounting fields update quarterly.
- Raw levels are mostly company-size signals.
- Time-series operators on slow-moving fields may not add much useful daily information.

Fix:

- Use ratios.
- Compare against peers.
- Add one complementary factor at a time.

Examples:

```text
operating_income / assets
operating_income / enterprise_value
cashflow_op / enterprise_value
debt / assets
enterprise_value / ebitda
```

## High Sharpe But Low Fitness

Example:

```text
Sharpe: 1.78
Fitness: 0.67
Turnover: 57.5%
```

Diagnosis:

- Signal may be good.
- Turnover is likely damaging Fitness.

Fix order:

1. Increase Decay gradually.
2. Smooth fast return or volume components.
3. Reduce coefficients on high-turnover components.
4. Keep the alpha structure mostly unchanged until Turnover is controlled.

## Good Turnover But Low Sharpe

Example:

```text
Sharpe: 0.46
Fitness: 0.22
Turnover: 3.98%
```

Diagnosis:

- Settings are not the main issue.
- Signal itself is weak.

Fix:

- Change the field or economic idea.
- Do not only increase Decay.
- Avoid adding many similar quality/value ranks blindly.

## Negative Sharpe

Examples:

```text
Sharpe: -0.28
Sharpe: -1.01
```

Diagnosis:

- Direction may be wrong, or the transformation is distorting the signal.

Fix:

- Consider reversing the signal only if the economic logic supports it.
- Otherwise discard that factor construction.
- Isolate simpler components to find which part has predictive value.

