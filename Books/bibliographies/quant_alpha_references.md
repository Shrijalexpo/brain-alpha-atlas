# Annotated Bibliography for Quantitative Alpha Research

Structured guide to the academic literature, technical factor libraries, and official WorldQuant BRAIN resources cataloged in [`Books/`](../README.md).

## 1. Formulaic Price-Volume and Microstructure Alphas

- **Kakushadze, Z. (2016). *101 Formulaic Alphas*. Wilmott, 2016(84), 72–81.**
  - **Stored Copy:** [`../research-papers/1601.00991v3_101_formulaic_alphas.pdf`](../research-papers/1601.00991v3_101_formulaic_alphas.pdf)
  - **Code Companion:** [`../technical-guides/alpha_101.txt`](../technical-guides/alpha_101.txt)
  - **Key Takeaways for BRAIN:**
    - Most short-horizon price-volume alphas rely on interaction between price change (`returns`, `close - open`, `vwap - close`) and volume participation (`volume / adv20`, `ts_corr(close, volume, d)`).
    - Direct copies fail consultant production correlation (`> 0.7`), but the normalization patterns (`rank`, `ts_rank`, `ts_decay_linear`, `group_neutralize`) transfer directly to less-crowded datasets.

- **Yang, X., Liu, W., Zhou, D., Bian, J., & Liu, T.-Y. (2020). *Qlib: An AI-oriented Quantitative Investment Platform* (`Alpha158`). arXiv:2009.11189.**
  - **Stored Copy:** [`../technical-guides/alpha_158.txt`](../technical-guides/alpha_158.txt)
  - **Key Takeaways for BRAIN:**
    - Categorizes price-volume features into candlestick geometry (`(close-open)/open`, `(high-max(open,close))/open`), rolling return ratios, volatility (`ts_std_dev(close, d)/close`), and volume-return correlation (`ts_corr(close/delay(close,1), log(volume/delay(volume,1)+1), d)`).

## 2. Fundamental, Analyst, and Cross-Sectional Equity Factors

- **BRAIN Learn Official Documentation Archive (78 Articles, 11 Topics).**
  - **Stored Copy:** [`../official-documentation/brain-platform-docs/index.md`](../official-documentation/brain-platform-docs/index.md)
  - **Curated Synthesis:** [`../../Docs/index.md`](../../Docs/index.md)
  - **Key Takeaways for BRAIN:**
    - Fundamental signals (`fnd6`) require size or valuation denominators (`enterprise_value`, `assets`, `cap`) to avoid acting as uncompensated size bets.
    - Slow analyst consensus fields (`anl69_*`, `anl4_*`) respond well to long-window scaling (`ts_scale(ts_backfill(x, 21), 63)` or `ts_quantile(..., 63)`), particularly in `EUR` and `KOR`.

## 3. Consultant Program, Genius, Osmosis, and Competition Mechanics

- **WorldQuant BRAIN India Formulaic Webpage & Base Fee Methodology (2022).**
  - **Stored Copy:** [`../official-documentation/india_wqbrain_formulaic_webpage_final_2022.pdf`](../official-documentation/india_wqbrain_formulaic_webpage_final_2022.pdf)
  - **Curated Synthesis:** [`../../Docs/11-osmosis-and-compensation/index.md`](../../Docs/11-osmosis-and-compensation/index.md)
- **All Region Competition 2026 Official Guidelines (2026).**
  - **Stored Copy:** [`../official-documentation/all_region_competition_2026_rules.txt`](../official-documentation/all_region_competition_2026_rules.txt)
  - **Curated Synthesis:** [`../../Docs/09-power-pool-and-thematic-competitions/index.md`](../../Docs/09-power-pool-and-thematic-competitions/index.md) and [`../../Docs/13-region-agnostic-and-cluster-alphas/index.md`](../../Docs/13-region-agnostic-and-cluster-alphas/index.md)
