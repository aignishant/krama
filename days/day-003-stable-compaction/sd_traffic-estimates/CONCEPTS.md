---
day: 3
part: "2.1"
title: "Convert a workload into rates with explicit assumptions"
ids: [SD-03]
level: working
prerequisites: ["Quality requirements", "Units and ratios"]
failure: true
---

# Convert a workload into rates with explicit assumptions

Core: derive average and peak rates, then write your own estimate. Concurrency and backend
fan-out are optional extensions, not additional mandatory design deliverables.

## One-line answer

Estimate request volume first, divide by a time interval, then model peak demand separately.

## The story

A shop sells 240 lunches in an eight-hour day. Planning for 30 lunches every hour may look
reasonable, until 120 customers arrive during one lunch hour. The daily total is right; the
assumption that demand arrives evenly is wrong.

## The idea in plain language

**QPS** means queries or requests per second at a named boundary. Users are not requests,
and daily requests are not requests per second. Write units at every step. Distinguish an
assumed active-user population, actions per active user, and requests per action.
Refer to [assumptions and scope](../../day-001-count-target-values/sd_functional-scope/CONCEPTS.md)
when deciding what counts. This model fits early sizing discussions where traffic measurements
are unavailable; later replace its inputs with observations.

## Why Krama needs it

Later decisions about servers and caches need a workload, but a rough rate does not establish
machine capacity. Keeping assumptions separate prevents an estimate from turning into a fake benchmark.

## The source behind it

[Handling Overload — The Pitfalls of Queries per Second](https://sre.google/sre-book/handling-overload/),
checked 2026-09-22 (`spec:sre-overload`), explains why requests with different resource costs
cannot be treated as interchangeable capacity units. The arithmetic below is an original model.

## The mechanism

### Worked trace

Assume a parcel tracker has 240,000 daily active users, each making 6 status reads per day,
with one API request per read. There are 86,400 seconds in the modeled 24-hour day.

| Stage | Calculation with units | Result |
| --- | --- | --- |
| Daily reads | 240,000 users/day × 6 reads/user | 1,440,000 reads/day |
| Average rate | 1,440,000 reads/day ÷ 86,400 seconds/day | About 16.67 reads/second |
| Busy-hour assumption | 25% of daily reads in 3,600 seconds | 100 reads/second |
| Peak multiplier for that interval | 100 ÷ 16.67 | About 6× |

The units cancel to the requested rate. The peak factor comes from a stated concentration
scenario, not from the word “industry.” A busy-hour average can still hide second-long bursts.
Specify the interval and test an alternative: at 50% in one hour, the estimate becomes 200 QPS.
Do not multiply another unexplained peak factor on top of an already peaked rate.

The retained model is small: population × actions × requests/action, interval, concentration,
and assumptions. It is sufficient for an order-of-magnitude arrival estimate. It deliberately
does not infer CPU time, payload sizes, writes, retries, or cache misses without more inputs.

Optional boundary extension:

```text
user action -> API request -> cache lookup -> miss -> database operations
                API QPS                        a different rate
```

If measured miss fraction is m and each miss causes f database operations, a simplified model
is database QPS ≈ API QPS×m×f. Retry amplification and background jobs require separate terms.
Optional concurrency estimate: average in-flight work ≈ arrival rate×average time in system
under a stable workload. This is not a thread count and must not substitute p99 for the mean.

## When it breaks

```python
daily_requests = 240_000 * 6
wrong_qps = daily_requests / 24
average_qps = daily_requests / 86_400
busy_hour_qps = daily_requests * 0.25 / 3_600
print(f"wrong label: {wrong_qps:.0f} QPS")
try:
    assert abs(wrong_qps * 86_400 - daily_requests) < 1, "hourly rate was labelled per second"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert abs(average_qps * 86_400 - daily_requests) < 1
print(f"average={average_qps:.2f} QPS, busy hour={busy_hour_qps:.2f} QPS")
```

**Line by line:** daily volume is calculated before dividing. Dividing by 24 produces requests
per hour, so multiplying that mislabeled rate by seconds/day cannot recover the original volume.
The repaired rate passes the reverse-units check. The busy-hour calculation models concentration
explicitly and does not claim an observed production peak.

Author verification on Python 3.12.10, 2026-09-22:

```text
wrong label: 60000 QPS
AssertionError: hourly rate was labelled per second
average=16.67 QPS, busy hour=100.00 QPS
```

## In production

Rounding a planning estimate is sensible; rounding intermediate values too early obscures
ratios. Report a range driven by plausible scenarios, then measure arrivals, request mix,
CPU, I/O, and latency before deciding server count. A popular link can concentrate reads on
one key even if global QPS is modest. Trace that hotspot rather than assuming uniform load.
Compare added capacity with reducing expensive work; each addresses a different bottleneck.

## Check yourself

### Readiness before practice

Why do total registered users and daily active users differ? What units remain after dividing
daily requests by 24? Which evidence could justify your peak factor? Why doesn't “100 QPS” alone
tell you how many servers are needed?

Use [the assignment](README.md#assignment)'s separate one-million-user workload in
[DESIGN.md](DESIGN.md). Show units, average QPS, a justified peak scenario, and one sensitivity
case. Walk through a burst exceeding the assumed peak and explain the user impact and next
measurement. These are hypothetical calculations; label them as such.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-003-traffic-estimates)
