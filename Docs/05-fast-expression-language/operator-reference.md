# WorldQuant BRAIN Categorized Operator Reference

Complete reference of Fast Expression operators organized by functional family, combining official platform signatures (`[Platform]`, captured 2026-07-26 / 2026-10-09) with empirical behavior from recorded simulations (`[Observed]`).

> **Genius Tier Note:** Base operators are available to all users and Gold consultants. Additional specialized operators unlock at Expert (63%), Master (78%), and Grand Master (100%) Genius levels (`[Platform]`). Note that `ts_backfill` and `group_backfill` are **excluded** from operator-count limits in Power Pool (`<= 8` operators) and Genius tie-breaker calculations (`[Platform]`).

## 1. Arithmetic & Mathematical Operators

| Operator Signature | Description | Practical Research Notes |
|---|---|---|
| `add(x, y, filter=false)` or `x + y` | Element-wise addition | Setting `filter=true` replaces `NaN` inputs with `0` before summing (`[Platform]`) |
| `subtract(x, y, filter=false)` or `x - y` | Element-wise subtraction | `filter=true` prevents one `NaN` leg from wiping out the composite |
| `multiply(x, y, filter=false)` or `x * y` | Element-wise multiplication | `filter=true` replaces `NaN` with `1`; avoid multiplying unranked noisy factors (`013` Sharpe `-1.01`, `[Observed]`) |
| `divide(x, y)` or `x / y` | Element-wise division | Guard zero denominators via `divide(x, add(y, 0.0001))` |
| `abs(x)` | Absolute value $\vert x \vert$ | Useful for magnitude filters (`abs(returns)`) |
| `inverse(x)` | Reciprocal $1 / x$ | Converts P/E or EV/EBITDA into earnings yield |
| `log(x)` | Natural logarithm $\ln(x)$ | Compresses right-skewed positive variables (`cap`, `volume`, `assets`) |
| `sqrt(x)` | Square root $\sqrt{x}$ | Undefined for negative values; pair with `signed_power(x, 0.5)` when signed |
| `power(x, y)` | Raises $x^y$ | Use small exponents (`0.5`–`2.0`) to avoid outlier explosion |
| `signed_power(x, y)` | $\text{sign}(x) \cdot \vert x \vert^y$ | Preserves Long/Short direction while compressing or stretching tails (`[Platform]`) |
| `sign(x)` | Returns `+1`, `-1`, or `0` | Strips magnitude information; rarely optimal alone |
| `reverse(x)` or `-x` | Negates $x$ (`-1 * x`) | Flips Long and Short bets (note: in `KOR`/`TWN`, `-x` does not strictly mirror PnL due to circuit breakers, `[Platform]`) |
| `max(x, y, ...)` / `min(x, y, ...)` | Element-wise maximum or minimum | Useful for floor/cap bounds |
| `densify(x)` | Remaps sparse categorical group IDs into contiguous integers `0..K-1` | Essential when constructing custom composite groups such as `densify(country) + densify(industry) * 100` (`[Platform]`) |

## 2. Cross-Sectional Operators (Across Instruments on Each Date)

| Operator Signature | Description | Practical Research Notes |
|---|---|---|
| `rank(x, rate=2)` | Cross-sectional rank mapped uniformly to `[0.0, 1.0]` | Default `rate=2` uses fast approximate sorting; `rate=0` performs exact sorting (`[Platform]`). Primary outlier guard |
| `zscore(x)` | Cross-sectional standardization $(x - \mu_t)/\sigma_t$ | Preserves relative tail distance; pair with `winsorize` if input has extreme outliers |
| `normalize(x, useStd=false, limit=0.0)` | Subtracts cross-sectional mean; divides by std if `useStd=true`; clips to `[-limit, +limit]` if `limit > 0` | Combines centering, standardization, and winsorization in one call (`[Platform]`) |
| `scale(x, scale=1, longscale=1, shortscale=1)` | Scales vector so $\sum \vert x_i \vert = \text{scale}$ (and separate long/short targets if specified) | Sizing operator; does not alter relative cross-sectional order |
| `quantile(x, driver="gaussian", sigma=1.0)` | Ranks $x$ and maps onto a target distribution (`gaussian`, `uniform`, `cauchy`) | Useful when combining multiple ranked legs that need Gaussian tail behavior (`[Platform]`) |
| `winsorize(x, std=4)` | Clips values outside $[\mu_t - \text{std}\cdot\sigma_t,\, \mu_t + \text{std}\cdot\sigma_t]$ | Direct cure for `CONCENTRATED_WEIGHT` when preserving cardinal values (`[Platform]`) |
| `truncate(x, maxPercent=0.01)` | Caps maximum weight share in any single stock | Expression-level equivalent of the `Truncation` setting (`[Platform]`) |
| `bucket(x, range="0,1,0.1")` or `buckets="..."` | Discretizes a continuous matrix `x` (usually `rank(y)`) into a **Group** field | Example: `bucket(rank(cap), range="0.1,1,0.1")` creates 10 size decile groups (`026`, `[Observed]`) |

## 3. Time-Series Operators (Across $d$ Past Trading Days per Instrument)

| Operator Signature | Description | Practical Research Notes |
|---|---|---|
| `ts_rank(x, d, constant=0)` | Rank of today's $x_{i,t}$ within its own past $d$ days (`[0, 1]`) | Transforming `ebitda/enterprise_value` and `sales_growth` with `ts_rank(..., 126)` drove the breakthrough in Simulations `024`–`026` (`[Observed]`) |
| `ts_zscore(x, d)` | Rolling time-series z-score over $d$ days | Strong on volume and analyst series over `d = 63, 126, 252` (`068`, `[Observed]`) |
| `ts_scale(x, d, constant=0)` | Min-max rescales $x_{i,t}$ within its $d$-day range: $(x_t - \min_d)/(\max_d - \min_d)$ | Top-performing operator on slow analyst fields (`anl69_*`) at `d = 63` in EUR (`067`) and KOR (`071 d1`) (`[Observed]`) |
| `ts_quantile(x, d, driver="gaussian")` | Maps `ts_rank(x, d)` onto a target distribution | Second-best operator on `anl69_*` and `anl4_*` at `d = 63` (`069`, `[Observed]`) |
| `ts_mean(x, d)` | Simple moving average over $d$ days | `ts_mean(-returns, 5)` is the canonical turnover reducer for fast reversal legs (`026, 027, 053`, `[Observed]`) |
| `ts_decay_linear(x, d, dense=false)` | Linearly weighted moving average over $d$ days (weights $d, d-1, \dots, 1$) | Smooths turnover while keeping higher weight on recent days (`[Platform]`) |
| `ts_delta(x, d)` | Difference $x_{i,t} - x_{i,t-d}$ | Use `d = 63` or `126` on fundamental ratios (`ts_delta(operating_income / assets, 63)` in `027`, `[Observed]`) |
| `ts_av_diff(x, d)` | Difference from rolling mean: $x_{i,t} - \text{ts\_mean}(x, d)$ | Cleaner than `ts_delta` when the baseline endpoint $t-d$ is noisy (`[Platform]`) |
| `ts_returns(x, d, mode=1)` | Relative change $(x_t - x_{t-d}) / x_{t-d}$ | Avoid on series that cross zero or go negative |
| `ts_std_dev(x, d)` | Rolling standard deviation over $d$ days | Used for return volatility or sentiment stability (`-ts_std_dev(scl12_buzz, 10)`, `[Platform]`) |
| `ts_ir(x, d)` | Rolling Information Ratio: $\text{ts\_mean}(x, d) / \text{ts\_std\_dev}(x, d)$ | Rewards steady trends over volatile spikes (`[Platform]`) |
| `ts_sum(x, d)` / `ts_product(x, d)` | Rolling sum or product over $d$ days | Warning: `ts_product` can overflow/underflow to degenerate constants on price fields (`068`, `[Observed]`) |
| `ts_min(x, d)` / `ts_max(x, d)` / `ts_max_diff(x, d)` | Rolling extrema over $d$ days | Useful for 52-week high/low anchoring (`d = 252`) |
| `ts_arg_max(x, d)` / `ts_arg_min(x, d)` | Days elapsed since the $d$-day high or low (`0` = today) | Captures recency of breakouts or capitulation |
| `ts_corr(x, y, d)` / `ts_covariance(x, y, d)` | Rolling correlation or covariance between $x$ and $y$ over $d$ days | Core building block of price-volume divergence alphas (`ts_corr(rank(close), rank(volume), 10)`) |
| `ts_regression(y, x, d, lag=0, rettype=0)` | Rolling OLS of $y$ on $x$ over $d$ days (`rettype`: `0`=residual, `1`=intercept, `2`=slope, `3`=fitted, `4`=SSE, `5`=SST, `6`=$R^2$) | `rettype=0` extracts the orthogonal residual of $y$ purged of $x$ (`[Platform]`) |
| `ts_backfill(x, lookback=d, k=1)` | Carries forward the $k$-th most recent non-`NaN` value within `lookback` days | **Mandatory** for quarterly/periodic fields (`ts_backfill(x, 21)` or `63`); exempt from Power Pool operator count (`[Platform]`) |
| `kth_element(x, d, k=1)` | Returns the $k$-th non-`NaN` value in the past $d$ days | Generalized lookback backfill (`[Platform]`) |
| `last_diff_value(x, d)` | Most recent previous value within $d$ days that differs from today's $x_{i,t}$ | Allows computing change across step-function updates (`x - last_diff_value(x, 126)`) (`[Platform]`) |
| `delay(x, d)` | Value of $x$ exactly $d$ trading days ago | `x - delay(x, d)` equals `ts_delta(x, d)` |
| `hump(x, hump=0.01)` | Limits daily change in $x_{i,t}$ unless change exceeds threshold proportional to cross-sectional book | Directly suppresses small noise trades to cut Turnover (`[Platform]`) |

## 4. Group Operators (Cross-Sectional Within Each Group $g$)

| Operator Signature | Description | Practical Research Notes |
|---|---|---|
| `group_neutralize(x, group)` | Subtracts the mean of `x` within each `group` bucket | Equivalent to settings Neutralization when applied once at the outer level; use inside expressions for custom `bucket()` or `country` conditioning (`[Platform]`) |
| `group_rank(x, group)` | Ranks `x` into `[0, 1]` within each `group` | Peer-relative ranking (e.g., `group_rank(ebitda/enterprise_value, subindustry)`) (`[Platform]`) |
| `group_zscore(x, group)` | Standardizes `x` within each `group` | Peer-relative z-score |
| `group_scale(x, group)` | Min-max rescales `x` into `[0, 1]` within each `group` | Peer-relative range scaling |
| `group_mean(x, weight, group)` | Weighted mean of `x` (weighted by `weight`, e.g., `cap` or `1`) within `group` | Useful for constructing custom group momentum or industry benchmark returns (`[Platform]`) |
| `group_backfill(x, group, d, std=4.0)` | Fills `NaN` values with the winsorized group mean over the past $d$ days | Best fallback when `ts_backfill` still leaves missing coverage (`[Platform]`) |
| `group_cartesian_product(g1, g2)` | Forms the joint interaction group $g_1 \times g_2$ | Canonical operator for **Double Neutralization** (e.g., `group_cartesian_product(country, industry)` in `EUR` and `GLB`) (`[Platform]`) |

## 5. Vector Operators (Reduce Vector Fields to Matrix Fields)

| Operator Signature | Description |
|---|---|
| `vec_avg(x)` | Mean of all vector observations for instrument $i$ on date $t$ |
| `vec_sum(x)` | Sum of vector observations for instrument $i$ on date $t$ |
| `vec_count(x)` | Number of vector observations on date $t$ |
| `vec_max(x)` / `vec_min(x)` / `vec_range(x)` | Maximum, minimum, or range of same-day vector entries |
| `vec_stddev(x)` / `vec_ir(x)` | Standard deviation or information ratio ($\mu / \sigma$) of same-day vector entries |
| `vec_skewness(x)` / `vec_kurtosis(x)` | Higher-moment shape of same-day vector entries |
| `vec_percentage(x, percentage=0.5)` | Quantile (`0.5` = median) of same-day vector entries |
| `vec_choose(x, nth=0)` | Selects the $n$-th element of the vector (`nth=-1` from end) |

## 6. Logical, Conditional & Special Operators

| Operator Signature | Description | Practical Research Notes |
|---|---|---|
| `trade_when(condition, alpha, exit_condition)` | Updates portfolio weight to `alpha` when `condition > 0`; holds previous day's weight when `condition == 0`; exits to `NaN` when `exit_condition > 0` | Pass `-1` as third argument (`exit_condition`) to never force-exit; first argument **must** be a boolean/event condition (`[Platform]`) |
| `if_else(condition, x, y)` or `condition ? x : y` | Element-wise conditional selection | Avoid deep nested `if_else` trees (overfitting anti-pattern in Consultant Don'ts, `[Platform]`) |
| `is_nan(x)` | Returns `1` if `x` is `NaN`, else `0` | Combine with `if_else(is_nan(x), 0, x)` for explicit missing-value substitution |
| `vector_neut(x, y)` | Orthogonalizes cross-sectional vector `x` against vector `y` on each date | Removes exposure to a specific continuous factor `y` (such as `log(cap)` or `historical_volatility_120`) (`[Platform]`) |
| `regression_neut(y, x)` | Cross-sectional OLS residual of `y` regressed on `x` | Purges linear exposure to `x` across the universe (`[Platform]`) |

## 7. SuperAlpha Combo & Selection Operators

For operators exclusive to SuperAlpha `Selection` and `Combo` expressions (`generate_stats`, `inst_pnl`, `self_corr`, `reduce_avg`, `reduce_ir`), see [12 — Advanced Alpha Research](../12-advanced-alpha-research/index.md).
