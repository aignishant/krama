---
day: 11
part: "1.1"
title: "Budget each connection pool at its own boundary"
ids: [SD-11]
level: working
prerequisites: ["Traffic estimates", "Single-node limits"]
failure: true
---

# Budget each connection pool at its own boundary

Core: concurrent demand, fleet multiplication, independent pools, and bounded waiting.
Multiplexing and autoscaling policy are optional depth. The assignment is a calculation, not a load test.

## One-line answer

Multiply per-worker demand across the fleet, then cap each separate pool against the resource it actually consumes.

## The story

A shop opens more checkout workers to reduce a queue, but every worker opens its own set of
database connections. The database runs out of room even though each worker's pool looks modest.
Adding front-end capacity moved the queue to a shared bottleneck.

## The idea in plain language

Concurrency counts work in flight; throughput counts completed work per time unit. A connection
is a communication resource, not a request. Depending on protocol and workload, a request may
use no connection, one connection, several connections, or share a multiplexed connection.
State the relationship before multiplying.

A pool is a bounded collection of reusable resources with a checkout policy. At least four
boundaries matter: client-facing sockets, outbound HTTP pools, database pools, and cache pools.
One limit does not automatically bound the others. Recall [traffic estimates](../../day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md)
and [single-node limits](../../day-006-best-single-trade/sd_single-node-baseline/CONCEPTS.md).
Recognize the issue when scaling replicas unexpectedly exhausts a shared dependency.

## Why Krama needs it

[Timeout propagation](../../day-012-range-sums/sd_timeout-propagation/CONCEPTS.md) must include pool
wait in the remaining deadline. A queue that waits forever can consume the full request lifetime
before any useful database work starts.

## The source behind it

[20.3. Connections and Authentication](https://www.postgresql.org/docs/16/runtime-config-connection.html)
(`spec:postgresql-16-connections`, checked 2026-09-22) documents a server connection ceiling and
reserved slots. Actual configuration must be inspected; the numerical ceilings here are assumptions.

## The mechanism

### Worked trace

The assignment gives 200 concurrent requests per worker and 20 workers: 4,000 in-flight requests.
If every request simultaneously holds one database connection, unconstrained DB demand is 4,000.
That is a demand scenario, not a justified pool size and not a requests-per-second estimate.

Assume instead a database ceiling of 500 connections with 100 reserved for operations, other
services, and margin. The application has a 400-connection budget. Twenty pools of 20 each
respect that ceiling. With no overflow, a worker handling 200 all-DB requests can lend 20 connections;
up to 180 requests must wait or be rejected. A per-worker queue cap of 40 makes at least 140
immediate rejections necessary in this simultaneous worst-case arrival, assuming no completions.
These are illustrative arithmetic bounds, not predictions of steady traffic.

| Boundary | What to count | Separate constraint |
| --- | --- | --- |
| Incoming traffic | Active and idle sockets, request streams | Listener/proxy limits and file descriptors |
| Outbound HTTP | Per-origin pools across processes | Remote limit and multiplexing policy |
| Database | Pool maximum plus permitted overflow | Shared server budget across all callers |
| Cache | Clients, pools, and supported request sharing | Cache server and library limits |

The invariant is that total permitted application connections never exceeds the app allocation,
including rollout overlap. Adding workers can break it without changing any individual pool.
Use maximum simultaneously running workers, not only desired steady-state replicas. Other limits,
including CPU and memory, may bind before connection count does.

## When it breaks

```python
workers, pool, overflow = 20, 20, 0
server_limit, reserve = 500, 100
budget = server_limit - reserve
print("request concurrency:", workers * 200)
print("planned DB cap:", workers * (pool + overflow), "budget:", budget)
rollout_workers = 25
try:
    assert rollout_workers * pool <= budget, "rollout exceeds the application DB budget"
except AssertionError as error:
    print(f"AssertionError: {error}")
revised_pool = budget // rollout_workers
print("pool for rollout ceiling:", revised_pool)
assert rollout_workers * revised_pool <= budget
```

**Line by line:** the first multiplication computes request concurrency, not connection usage.
The second enforces a chosen database allocation. The assertion models five extra workers during
rollout. Integer division finds a per-worker upper bound of 16 at the 25-worker ceiling. It
establishes a configured cap, not adequate throughput or acceptable latency.

Author verification on Python 3.12.10, 2026-09-22:

```text
request concurrency: 4000
planned DB cap: 400 budget: 400
AssertionError: rollout exceeds the application DB budget
pool for rollout ceiling: 16
```

## In production

Count pools per process if each process owns one. Include overflow, background jobs, migrations,
and old/new replicas running together. Reuse connections and release them on success, error, and
cancellation; leaked checkouts defeat the intended pool capacity. Do not hold a DB connection
while waiting on unrelated network work if the transaction does not require it.

Measure active/idle connections, checkout wait, timeouts, query duration, and queue depth.
A reviewer should ask whether scaling can stay inside the dependency allocation and whether
requests expire while waiting. Bounded admission trades some rejected requests for predictable
resource use; unlimited queues trade immediate rejection for rising latency and memory.

## Check yourself

### Readiness before practice

1. What assumption turns 4,000 concurrent requests into 4,000 DB connections?
2. Why can HTTP, DB, and cache pool limits differ?
3. What happens to the fleet cap when five rollout workers appear?
4. Which metric distinguishes slow queries from time spent waiting for a connection?

Run the arithmetic model and explain the resource boundary aloud. Use [the reference](REFERENCE_DESIGN.md)
for a complete answer, then write or compare your own [DESIGN.md](DESIGN.md).

[Navigation](README.md) · [Recall](../../../docs/SD_RECALL.md#day-011-connection-budgets)
