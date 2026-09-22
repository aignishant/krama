---
day: 5
part: "2.1"
title: "Budget the request path without adding unrelated percentiles"
ids: [SD-05]
level: working
prerequisites: ["Quality requirements", "Percentiles and measurement boundaries"]
failure: true
---

# Budget the request path without adding unrelated percentiles

Core: trace one request, distinguish allocations from measurements, and study the percentile
counterexample. Then write one memo within the 30-minute session. Parallel calls and timeout
propagation are optional bridges to later days, not extra implementation assignments.

## One-line answer

Allocate time across the actual request path, then measure its end-to-end distribution to verify the target.

## The story

You allow an hour to collect a parcel: travel, wait at the counter, collect it, and return.
The journey needs room for variation. Knowing the counter's usual wait and the road's usual
delay does not tell you whether the worst waits and worst traffic affect the same journeys.

## The idea in plain language

Recall [Day 2's measurement boundaries and percentiles](../../day-002-find-the-first-maximum/sd_quality-requirements/CONCEPTS.md).
A **latency budget** allocates an end-to-end time target among parts of a request path. It is
a planning constraint, not a measured percentile. A **critical path** is the dependency path
that determines when the response can finish. Sequential work adds; overlapping work requires
following dependencies rather than summing all recorded activity.

Use this framework when a user-visible latency target exists but each service owner sees only
one part of the journey. Name eligible requests and whether the endpoint is first byte, final
byte, or rendered UI before assigning numbers. Keep failures and timeouts visible in a
separate indicator if the latency population includes only successful requests.

## Why Krama needs it

An allocation gives later timeout, caching, and storage decisions a purpose. Without a shared
boundary, every component can report a good local metric while the complete interaction misses its goal.

## The source behind it

[Service Level Objectives](https://sre.google/sre-book/service-level-objectives/), rechecked
2026-09-22 (`spec:sre-slos`), explains service indicators and why latency distributions matter.
The allocation and paired-request counterexample below are original hypothetical examples;
they are not measured service performance or a statistical guarantee from that source.

## The mechanism

### Worked trace

Assume a parcel-status page has a 160 ms end-to-end p95 target, from starting the client action
to displaying the result. Start with a simplified serial path:

```text
client prepare -> network outbound -> app -> storage -> app -> network return -> client display
|------------------------------ observed end-to-end time -------------------------------|
```

| Component | Assumed allocation | Boundary |
| --- | --- | --- |
| Client | 15 ms | Preparation plus rendering, excluding waiting |
| Network | 35 ms | Outbound plus return transit |
| App | 40 ms | Queueing and app work, excluding storage wait |
| Storage | 50 ms | Storage request through response |
| Unallocated margin | 20 ms | Remaining slack for variation and omitted small costs |
| Total | 160 ms | Whole modeled interaction |

For one request, observed durations of 12, 30, 32, and 46 ms total 120 ms, leaving 40 ms under
the target. That one observation does not establish p95. Nor must each request spend the
full allocation. The budget makes tradeoffs explicit: reducing a component's time gives room
elsewhere, while increasing one allocation consumes margin or another allocation.

Avoid double counting: an inclusive app span that already contains the storage call cannot
be added to the same storage duration again. A trace's parent duration includes its child
wait. Use nonoverlapping durations when adding a serial request's components.

Why percentiles differ: p95 identifies a rank within a distribution, not a particular request
that is simultaneously p95 at every stage. The slowest app calls and slowest storage calls
may belong to different requests. Even when 95% of requests pass each of two component limits,
the sets that pass can differ. Both limits therefore need not hold for 95% of complete requests.

To verify the end-to-end target, retain paired timings from the same requests or directly
measure end-to-end durations. Compute the percentile on those totals, using a declared method
and a representative workload. Instrumenting more detail costs collection, storage, and
analysis effort; begin with the boundary needed for the user promise.

## When it breaks

Twenty synthetic requests pass through two serial stages. Each stage is slow on one request,
and those two requests differ. The nearest-rank p95 is the 19th sorted observation.

```python
from math import ceil

def p95(values):
    ordered = sorted(values)
    return ordered[ceil(0.95 * len(ordered)) - 1]

app_ms = [10] * 19 + [100]
storage_ms = [10] * 18 + [100, 10]
totals_ms = [app + storage for app, storage in zip(app_ms, storage_ms)]
component_sum = p95(app_ms) + p95(storage_ms)
end_to_end = p95(totals_ms)
print(f"sum of component p95={component_sum} ms")
print(f"p95 of request totals={end_to_end} ms")
try:
    assert component_sum == end_to_end, "component percentiles are not additive"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert end_to_end == 110
print("paired-request calculation: PASS")
```

**Line by line:** the helper implements the stated percentile convention for nonempty fixtures.
The app's slow call is last; storage's is second-last. `zip` pairs measurements by request
position. Eighteen totals are 20 ms and two are 110 ms. The deliberately false equality exposes
the mistake; the repaired calculation takes p95 after summing each paired request. Real traces
need request identifiers, not merely matching positions in independently collected logs.

Author verification on Python 3.12.10, 2026-09-22:

```text
sum of component p95=20 ms
p95 of request totals=110 ms
AssertionError: component percentiles are not additive
paired-request calculation: PASS
```

This repairs the calculation, not the service. A real latency problem still needs an intervention
and a new measurement. The synthetic sample proves a counterexample, not a population estimate.

## In production

Trace queueing as well as execution. A fast database cannot rescue a request that spent its
budget waiting for an app worker. Compare reducing expensive work, caching with a freshness
tradeoff, or changing the dependency path before adding servers blindly.

Optional parallel example: two independent calls starting together and both required contribute
roughly the slower call's duration, plus launch/join overhead. Staggered starts or dependencies
change that path. Retries add attempts and waits. Passing the remaining deadline downstream
can prevent wasted work after the caller has stopped waiting, but assigning every stage its
own full end-to-end timeout can exceed the original budget.

## Check yourself

### Readiness before practice

1. Why can two component p95 values fail to predict end-to-end p95?
2. Which app and storage spans would you accidentally double count?
3. How does waiting for two parallel dependencies change the path?
4. Is reserved margin an observed latency, and does a passing sample prove the target?

Use [the assignment](README.md#assignment)'s separate **200 ms** target in [DESIGN.md](DESIGN.md).
State the boundary, population, allocations, and any margin; label every number as an assumption.
Trace a request exceeding one allocation, describe its user impact, and compare a remedy with
an alternative. Explain what end-to-end observations would validate your design. No server is required.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-005-latency-budgets)
