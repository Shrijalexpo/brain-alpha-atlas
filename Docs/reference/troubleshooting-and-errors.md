# Troubleshooting and Error Catalog

Diagnostic reference for resolving WorldQuant BRAIN expression validation errors, runtime warnings, and submission-check rejections (`[Platform]`, `[Observed]`).

## 1. Expression Validation & Type Errors

| Error / Warning Message | Recorded Example | Cause | Solution |
|---|---|---|---|
| **First argument of `trade_when` must be a boolean event** | `trade_when(top2000, alpha, -1)` | `top2000` is a Universe field, not a boolean expression | Replace first argument with a comparison such as `volume > adv20` (`[Observed]`) |
| **Event / Vector input not allowed for matrix time-series operator** | `rank(ts_delta(eps_estimate_value, 20))` ([`042`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/042_estimate_eps_delta_error.md), [`043`](../../Analysis%20and%20Simulation%20Reports/simulation-results/USA/043_estimate_sales_delta_error.md)) | Field is Vector/Event type rather than a regular daily Matrix | Reduce with `vec_avg(field)` first, or choose a Matrix consensus field (`anl69_*`, `anl4_*`) wrapped in `ts_backfill(x, 21)` (`[Observed]`) |
| **Unit mismatch warning (`Unit Handling: Verify`)** | `ebitda + sales_growth` or `operating_income / cap + -returns` | Adding expressions with incompatible financial units (USD vs % growth vs daily return) | Normalize each component via dimensionless ratios and wrap in `rank()` or `zscore()` before adding (`[Platform]`) |
| **Division by zero / `NaN` explosion** | `operating_income / dividend` (many stocks pay `0` dividend) | Denominator equals `0` or `NaN` for a large share of the universe | Use `enterprise_value`, `assets`, or `cap` as denominators, or guard with `divide(x, add(y, 0.0001))` (`[Platform]`) |
| **Degenerate `ts_product` overflow/underflow** | `ts_product(ts_backfill(pv37_low_14, 21), 63)` ([`068`](../../Analysis%20and%20Simulation%20Reports/simulation-results/EUR/068_eur_multi_universe_decay5_sweep.md)) | Multiplying 63 daily non-unit values overflows or collapses to zero | Never apply `ts_product` over long windows to raw price/volume levels (`[Observed]`) |

## 2. Simulation Metric & Check Failures

| Failed Check | Primary Symptom | First Diagnostic Check | Best Verified Fix |
|---|---|---|---|
| `LOW_SHARPE` | Sharpe below regional cutoff | Is Turnover also low (`< 20%`)? | Change the economic ratio or switch from `rank(x)` to `ts_rank(x, 126)` / `ts_scale(x, 63)` (`[Observed]`) |
| `LOW_FITNESS` | Fitness `< 1.0` (D1) or `< 1.3` (D0) | Check whether `Turnover > 30%` or `Returns` are too small | If Turnover is high: smooth fast leg (`ts_mean(-returns, 5)`), use `hump`, or raise `Decay`. If Turnover `< 15%`: strengthen signal rather than smoothing (`[Observed]`) |
| `HIGH_TURNOVER` | Turnover `> 70%` (or `> 30%` in HKG/KOR, `> 40%` in IND) | Which term changes daily? | Smooth the daily price/volume/sentiment term or increase settings `Decay` (`0 -> 5`) (`[Observed]`) |
| `LOW_TURNOVER` | Turnover `< 1.0%` | Using a static identifier or un-updated annual field | Replace metadata/identifier field with an active economic variable (`[Observed]`) |
| `LOW_2Y_SHARPE` | Recent 2-year window Sharpe fails despite strong 10-year Sharpe | Inspect recent 2-year PnL slope | Use adaptive 63-day scaling (`ts_scale(x, 63)`, `ts_quantile(x, 63)`) or risk neutralization (`[Observed]`) |
| `LOW_SUB_UNIVERSE_SHARPE` | Fails on `TOP1000` / `TOP800` | Check if signal tilts toward small/illiquid stocks | Remove `-rank(cap)` size biases; apply `group_neutralize(..., bucket(rank(cap), range="0.1,1,0.1"))` (`[Platform]`, `[Observed]`) |
| `CONCENTRATED_WEIGHT` | Single stock `>= 10%` weight or too few stocks active | Check active `long_count + short_count` and outliers | Add `ts_backfill(x, 63)`, wrap in `rank()` or `winsorize(x, std=4)`, and lower `Truncation` to `0.01–0.02` (`[Platform]`, `[Observed]`) |
| `SELF_CORRELATION` / `PROD_CORRELATION` | Correlation `>= 0.70` without `+10%` Sharpe margin | Reusing a crowded factor backbone in `USA / D1` | Move to less-crowded regions (`EUR, GLB, KOR, AMR`), use single-dataset ATOMs (`anl69`), or apply risk neutralization (`[Platform]`, `[Observed]`) |
