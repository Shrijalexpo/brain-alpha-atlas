# Simulation 043 - Sales Estimate Delta Error

Status: ERROR

Expression:

```text
rank(ts_delta(sales_estimate_value, 20))
```

Known error:

```text
Operator ts_delta does not support event inputs
```

Conclusion:

- `sales_estimate_value` behaved like event/vector data.
- Use only valid matrix fields or convert vector/event fields with appropriate `vec_*` operators first.

