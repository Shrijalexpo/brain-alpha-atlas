# Alpha Improvement Notes From BRAIN Docs

Source: BRAIN Learn > Documentation, captured through Computer Use on 2026-07-26.

## Research Cycle

BRAIN describes alpha research as a cycle:

1. Come up with an intuitive alpha idea.
2. Implement it using available datasets and operators.
3. Optimize parameters and neutralization settings to submit the alpha in its best form.

Key principle:

- There are no fixed right or wrong answers in alpha research.
- The repeatable skill is controlled experimentation.

## Common Improvement Targets

The BRAIN docs point researchers toward learning how to:

- get higher Sharpe,
- increase returns,
- reduce alpha correlation,
- reduce turnover,
- smooth PnL fluctuations,
- gain intuition for neutralization,
- avoid overfitting.

## Practical Diagnosis Table

| Problem | Likely issue | First actions |
|---|---|---|
| Low Sharpe | Low return or high volatility | Improve idea, normalize signal, reduce noise, check direction. |
| High Turnover | Signal changes too quickly | Use `hump`, `ts_decay_linear`, `ts_mean`, `trade_when`, or higher Decay. |
| Weight concentration | Too few/extreme positions | Use `rank`, `winsorize`, `truncation`, `ts_backfill`, broader universe. |
| Weak Sub-universe Sharpe | Not robust on smaller universe | Try TOP3000, reduce concentration, improve coverage. |
| Low coverage | Many NaNs | Use `ts_backfill`, `kth_element`, `group_backfill`, or choose better field. |
| Unit warning | Mixing unlike units | Prefer ratios, normalize before combining, ignore only when logically justified. |
| Overfit-looking result | Good train, bad test | Use Test Period, simplify expression, reduce parameter tweaking. |

## Submission-Oriented Thresholds Captured

From documentation capture:

```text
Sharpe > 1.25
Fitness > 1.0
Turnover between 1% and 70%
```

Use these as a working reference, but always trust the live BRAIN checks shown on the simulation page.

## Alpha Example Ideas Captured

Bronze/Silver example themes in docs:

1. Valuation based on cash flow

Idea:

- Lower EV/CF suggests a company is cheaper relative to cash generation.
- Higher multiple suggests it is more expensive.

Implementation clue:

- Use `ts_zscore` to standardize change in the ratio.
- Use `group_rank` to control Turnover.
- Try different cash flow types.

2. Overpriced stocks

Idea:

- If analyst price target estimates and free cash flow estimates move highly in sync, the market may have priced in cash flow expectations already.

Implementation clue:

- Use `est_ptp` for price estimate and `est_fcf` for free cash flow estimate.
- Use `ts_corr` to measure dynamics between them.
- Try shorter windows if one year reacts too slowly.

3. Volatility arbitrage

Idea:

- Higher volatility often appears during bearish markets, lower volatility during bullish markets.
- Lower Parkinson's volatility plus higher implied volatility may suggest stronger bullish sentiment.

Implementation clue:

- Go long when implied volatility significantly exceeds historical volatility, short the opposite.
- Use `ts_backfill` to avoid missing data on certain days.

## Working Rules Added To Future Alpha Generation

- Prefer one clear idea over a large factor soup.
- Convert the idea into a measurable relationship.
- Use the right neutralization for the dataset category.
- Handle missing data before trusting metrics.
- Use Test Period to reduce overfitting.
- Record every simulation result before modifying again.

