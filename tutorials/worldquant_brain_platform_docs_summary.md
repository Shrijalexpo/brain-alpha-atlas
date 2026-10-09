# WorldQuant BRAIN Platform Documentation Summary

Source: BRAIN Learn > Documentation, captured through Computer Use on 2026-07-26.

Raw captures:

```text
tutorials/worldquant_brain_documentation_raw/
```

## Fast Expression

Fast Expression is WorldQuant BRAIN's proprietary expression language for writing and testing financial models. It is intended to be close to pseudocode so researchers can focus on idea logic rather than implementation details.

Fast Expression elements:

- Data fields: named data such as `open`, `close`, `returns`, `cap`, etc.
- Operators: mathematical and transformation tools.
- Numerical values.

Syntax notes:

- Use `/* ... */` for block comments.
- Use `;` to separate statements.
- The last statement is the actual alpha expression used by the simulator to calculate positions.
- Fast Expression does not use classes, objects, pointers, or ordinary programming-language functions.

## Simulation Workflow

The core process:

```text
Alpha idea
-> Fast Expression implementation
-> simulation settings
-> backtest / IS summary
-> result diagnosis
-> controlled improvement
-> submission tests
```

Good alpha research has both creative and scientific parts:

- come up with an intuitive idea,
- implement it using available data/operators,
- optimize parameters and neutralization settings.

## Test Period

The Test Period feature splits the in-sample period into Train and Test segments.

Purpose:

- reduce overfitting,
- validate whether an alpha works outside the period used for development,
- compare Train vs Test stats.

Important notes:

- Choosing a Test Period does not change the underlying simulation.
- It changes statistics and visualization by showing Train and Test separately.
- Test Period can be 0-5 years from the final part of IS.
- Stats default to training period until the test period is shown.
- Test period is shown in orange, train period in blue.
- An Alpha/SuperAlpha can only be submitted after the Test Period is revealed with `Show test period`.

## Simulation Settings

Core settings:

- Region
- Universe
- Language
- Delay
- Decay
- Truncation
- Neutralization
- Pasteurization
- Lookback
- Max Trade
- Max Position

Common documented examples used:

```text
Region: USA
Universe: TOP3000 or TOP200
Language: Fast Expression
Decay: 0
Delay: 1
Truncation: 0.08
Neutralization: Market, Sector, or Industry
Pasteurization: On
Lookback: OFF
Max Trade: OFF
Max Position: OFF
```

Working rule:

- Start with simple settings.
- Change one setting at a time.
- Pick neutralization based on dataset category and economic intuition.

## Result Interpretation

From the intermediate results documentation:

- A good PnL graph should rise steadily, with few severe drops.
- High fluctuations and major drawdowns are warning signs.
- In-sample simulation uses historical data over a 5-year timeframe.
- IS summary includes Sharpe, Turnover, Fitness, Returns, Drawdown, and Margin.

Passing thresholds captured:

```text
Sharpe: above 1.25
Turnover: between 1% and 70%
Fitness: above 1.0
```

Common result problems:

- Low Sharpe: increase alpha return or reduce volatility.
- Weight concentration: use range-normalized functions such as `rank`, set truncation, and consider `ts_backfill`.
- Sub-universe Sharpe below cutoff: try larger instrument universes such as TOP3000.
- Syntax errors: check spelling of data fields/operators and expression logic.
- Unit warnings: often appear when combining fields with different units, such as `close + cap`; warnings may be informational if the alpha intentionally handles units.

## Alpha Improvement Reading List From Docs

The docs recommend must-read posts on:

- getting higher Sharpe,
- increasing returns,
- reducing correlation,
- reducing Turnover using `trade_when`,
- smoothing PnL,
- gaining neutralization intuition,
- avoiding overfitting.

These are saved as topics to investigate later in:

```text
Research/alpha_improvement_from_docs.md
```

