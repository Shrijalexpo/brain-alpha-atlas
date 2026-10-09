# Simulation 033 - Operating Income Quality + EBITDA/EV Trend + Reversal

Status: FAILED_SELF_CORRELATION

Expression:

```text
group_neutralize(
    rank(ts_rank(operating_income / assets, 126))
    + rank(ts_delta(ebitda / enterprise_value, 126))
    + rank(ts_mean(-returns, 5)),
    bucket(rank(cap), range="0.1,1,0.1")
)
```

Known result:

```text
Exact metrics not captured in text.
Observed result: failed self-correlation.
```

Conclusion:

- Changing ROA trend to value trend did not solve correlation.
- Avoid this same quality plus value plus 5-day reversal backbone.

