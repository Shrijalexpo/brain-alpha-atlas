# Technical Guides and Formula Collections

Code-level factor definitions and operator pattern libraries for translating quantitative signals into WorldQuant BRAIN Fast Expression and Python Alphas.

## Stored Collections

| File | Title | Source / Author | Year | Classification | SHA-256 Checksum |
|---|---|---|---:|---|---|
| [`alpha_101.txt`](alpha_101.txt) | `Alpha101` Polars Factor Implementation | WorldQuant / Kakushadze (2016) community port | 2016 | Community-produced | `172d867fee2be8e7...` |
| [`alpha_158.txt`](alpha_158.txt) | `Alpha158` Qlib Factor Library | Microsoft Research Qlib | 2020 | Academic / Community | `05b29aa65572d3d7...` |

## Usage Rules for WorldQuant BRAIN

1. **Translate Syntax Carefully:**
   - `cs_rank(x)` in `alpha_101.txt` maps to `rank(x)` in Fast Expression.
   - `ts_corr(x, y, d)` maps to `ts_corr(x, y, d)`.
   - `ts_std(x, d)` maps to `ts_std_dev(x, d)`.
2. **Avoid Crowding:** Classic `Alpha101` price-volume formulas in `USA / TOP3000 / D1` have high production correlation. Combine structural ideas (such as candlestick body-to-range ratios from `Alpha158` or volume-price divergence from `Alpha101`) with fundamental, analyst, or volatility fields.
3. **Check Duplicate Ledger First:** Before simulating any translated expression, verify [`../../Analysis and Simulation Reports/index.md`](../../Analysis%20and%20Simulation%20Reports/).
