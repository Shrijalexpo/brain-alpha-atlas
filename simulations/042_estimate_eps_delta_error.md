# Simulation 042 - EPS Estimate Delta Error

Status: ERROR

Expression:

```text
rank(ts_delta(eps_estimate_value, 20))
```

Known error:

```text
Operator ts_delta does not support event inputs
```

Conclusion:

- `eps_estimate_value` behaved like event/vector data, not a normal matrix time series.
- Do not use `ts_delta()` directly on this field without proper conversion.

