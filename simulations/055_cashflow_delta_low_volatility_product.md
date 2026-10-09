# Simulation 055 - Cashflow Improvement x Low Volatility

Status: FAILED

Expression:

```text
rank(ts_delta(cashflow_op / assets, 63))
* rank(-historical_volatility_120)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: completely failed.
```

Conclusion:

- Multiplication with low volatility was not useful here.

