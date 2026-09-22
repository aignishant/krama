---
day: 2
part: "2.1"
title: "Turn quality words into measurable promises"
ids: [SD-02]
level: foundation
prerequisites: ["Functional scope and assumptions"]
failure: true
---

# Turn quality words into measurable promises

Core: follow the measurement example, then draft your own targets. All example numbers are
assumptions or synthetic fixtures, never observed service performance. Keep one memo in the
30-minute session; deeper instrumentation design is optional.

## One-line answer

A quality target needs a population, a measurement boundary, a time window, and a threshold.

## The story

A parcel service promises “quick delivery.” A sender means delivery today; the warehouse means
dispatch today. Both can claim success until a customer asks where the parcel is. A precise
promise names the start, finish, eligible parcels, and permitted delay.

## The idea in plain language

Build on [functional scope](../../day-001-count-target-values/sd_functional-scope/CONCEPTS.md).
A functional requirement identifies behavior; a quality requirement describes how well that
behavior must work. An **SLI** is the measured indicator; an **SLO** is a target for it. A target
is not evidence that the system already achieves it.

| Quality | Concrete question | Useful measurement shape |
| --- | --- | --- |
| Availability | Can eligible requests get the defined successful outcome? | Good requests / eligible requests in a window |
| Latency | How long does the outcome take? | A percentile of durations at a named boundary |
| Durability | Can acknowledged stored data be recovered later? | Loss of acknowledged records over a defined horizon |
| Freshness | How far behind current state may a response be? | Visibility delay after an acknowledged update |

These properties are distinct. A fast stale response may pass latency and fail freshness.
A service can be temporarily unavailable without losing data. A durable record may be inaccessible
during an outage. Recognize this framework whenever requirements use words like fast or reliable.

## Why Krama needs it

Quality choices guide later caching, storage, and replication decisions. Without an observable
target you cannot explain which tradeoff an architectural choice buys.

## The source behind it

[Service Level Objectives](https://sre.google/sre-book/service-level-objectives/), checked
2026-09-22 (`spec:sre-slos`), distinguishes indicators and objectives and discusses aggregation.
The toy measurements and proposed targets below are original teaching assumptions.

## The mechanism

### Worked trace

For a parcel-status API, assume a target: at least 99% of eligible status reads complete
successfully within 150 ms, measured from gateway receipt to final response byte over seven days.
This is a combined success-and-latency indicator. Define eligible reads, expected not-found
responses, and timeout treatment before measuring. Unexplained exclusions can make a bad service
look healthy.

```text
client -- network --> gateway [start timer] --> service --> gateway [end timer] --> client
                        <--------- measured duration --------->
client-perceived duration also includes the surrounding network journey
```

Keep counts and a latency distribution, rather than only a mean. In a ten-request illustration,
nine 10 ms responses and one 910 ms response average 100 ms. Under the **nearest-rank** rule,
p95 takes the sorted value at rank ceil(0.95×10)=10, so p95 is 910 ms. This tiny sample teaches
aggregation; it cannot estimate a real seven-day tail reliably. Real percentile systems must
specify their aggregation method, and averaging machine-level percentiles is not a global percentile.

For freshness, define an update event and a visible-read event on the same timeline. For
durability, distinguish acknowledged writes from attempted writes and name the failure scope
and recovery observation. “No loss” without a population and horizon cannot be evaluated.

Why this works: two reviewers using the same event definitions can calculate the same indicator.
The model retains enough context to explain a pass or failure and which user experience it covers.

## When it breaks

```python
from math import ceil

latencies_ms = [10] * 9 + [910]
mean_ms = sum(latencies_ms) / len(latencies_ms)
p95_ms = sorted(latencies_ms)[ceil(0.95 * len(latencies_ms)) - 1]
print(f"mean={mean_ms:.0f} ms, p95={p95_ms} ms")
assert mean_ms <= 150
try:
    assert p95_ms <= 150, "the average hid a slow request"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert sum(ms <= 150 for ms in latencies_ms) == 9
print("within threshold: 9/10")
```

**Line by line:** the fixture deliberately contains one slow request. `ceil` implements the
declared percentile rule; subtracting one converts rank to a list index. The average passes
while the tail check fails. Counting threshold passes makes the missed promise visible without
changing the target to fit the observations.

Author verification on Python 3.12.10, 2026-09-22, using synthetic data:

```text
mean=100 ms, p95=910 ms
AssertionError: the average hid a slow request
within threshold: 9/10
```

The repair is a correct measurement and an honest failed target, not a claim that this script
improved service latency. A proposed operational change still needs a new measurement.

## In production

Instrumentation, retention, and fine-grained breakdowns have costs. Start with measurements
connected to user outcomes; segment by endpoint or region where an aggregate hides harm.
Stricter freshness may reduce the usefulness of caches; stronger durability may add write work.
Compare a realistic alternative target and explain the user impact before selecting technology.
Review question: could this service pass the metric while visibly failing its user promise?

## Check yourself

### Readiness before practice

Explain a request that passes latency but fails freshness. Can a system lose acknowledged
data while its API remains available? Where does your timing begin and end? What happens to
timeouts in the denominator?

Open [the assignment](README.md#assignment). Continue Day 1's shortener scope; if studying this
track independently, assume create-link and resolve-link actions and record that scope explicitly.
In [DESIGN.md](DESIGN.md), define availability, latency percentile, durability, and freshness
targets with populations, windows, and all numbers marked as assumptions. Add one failure trace,
an alternative, and the measurement that would change your decision. No deployment is needed.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-002-quality-requirements)
