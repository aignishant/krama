---
day: 6
part: "2.1"
title: "Start with one service and an explicit source of truth"
ids: [SD-06]
level: working
prerequisites: ["Scope", "Traffic estimates", "Storage estimates", "Latency budgets"]
failure: true
---

# Start with one service and an explicit source of truth

Core: draw the path, identify durable state, and nominate a measurable bottleneck. Deployment,
replication, and caching implementation are optional later topics, not extra tasks today.

## One-line answer

A useful baseline follows each operation through the smallest architecture that can honor its promises.

## The story

A shop records orders in one notebook. Adding another clerk will not help if both clerks wait
for the same notebook, and saying an order is saved before writing it risks losing that order.

## The idea in plain language

A component diagram names responsibilities; a request trace explains their order. The source
of truth is the authoritative stored fact from which the service answers. A bottleneck is a
resource that limits useful throughput for a particular workload. “The database is slow” is
a hypothesis until timings and utilization support it.

Recognize the need for a baseline when a design has many boxes but cannot explain one create
or read. Reuse [traffic units](../../day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md)
and [latency boundaries](../../day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md).
One service process plus a database can be drawn as separate logical responsibilities even
when both run on one host. That host is one shared failure domain.

## Why Krama needs it

The [request journey](../../day-008-first-repeated-value/sd_request-journey/CONCEPTS.md) will
expand the browser-to-service arrow. Today's baseline makes clear which state is authoritative
before networking detail is added.

## The source behind it

[Handling Overload](https://sre.google/sre-book/handling-overload/)
(`spec:sre-overload`, rechecked 2026-09-22) supports measuring resource pressure and bounding
overload. The topology and arithmetic below are original hypothetical models.

## The mechanism

### Worked trace

```text
Browser -> service -> database       create: validate, insert, commit, acknowledge
Browser -> service -> database       redirect: look up code, return destination
Browser ----------------> destination after receiving the redirect
```

For a create, the database stores `code -> destination`. A uniqueness constraint prevents two
destinations from owning one code; a collision requires another candidate or a clear rejection.
The service acknowledges creation only after the database reports its configured durable commit.
For a redirect, it looks up the code and returns the destination. The browser retrieves the
destination itself. A missing code and an unavailable database are different outcomes.

Keep these invariants: acknowledged mappings have been committed; a code has at most one
authoritative destination; a database error does not become a false “not found.” They make
correctness inspectable at each arrow. They do not promise survival of a destroyed disk;
that needs a separate recovery design and tested backups.

Suppose a simplified database worker handles one operation at a time at 4 ms per operation.
Its ideal ceiling is `1000 / 4 = 250 operations/s`. At 200 requests/s with one database call
per request, estimated demand is 80% of that worker. Two calls per request demand 400
operations/s, above the ceiling. Worker counts, lock contention, disk behavior, and cache
effects make real databases more complicated; this arithmetic identifies an experiment,
not a measured production capacity. More app workers do not change this assumed database ceiling.

## When it breaks

```python
requests_per_second = 200
calls_per_request = 2
service_ms = 4
capacity = 1000 / service_ms
demand = requests_per_second * calls_per_request
print(f"database demand={demand} ops/s; modeled capacity={capacity:.0f} ops/s")
try:
    assert demand <= capacity, "database demand exceeds the modeled worker"
except AssertionError as error:
    print(f"AssertionError: {error}")
revised_demand = requests_per_second * 1
assert revised_demand < capacity
print(f"one-call design demand={revised_demand} ops/s; measure before accepting")
```

**Line by line:** the variables label rate, operations per request, and milliseconds per
operation. Multiplication converts request rate to database demand. The assertion rejects the
overloaded model. Reducing to one operation fits the arithmetic, but requires a valid application
change and measurements before accepting the design. It is not evidence of a faster service.

Author verification on Python 3.12.10, 2026-09-22:

```text
database demand=400 ops/s; modeled capacity=250 ops/s
AssertionError: database demand exceeds the modeled worker
one-call design demand=200 ops/s; measure before accepting
```

## In production

Measure queue wait, database call duration, CPU, disk activity, connections, and end-to-end
latency under a stated read/write mix. Begin with one suspected limit and compare it with
alternatives; high app CPU and low database utilization would challenge a database hypothesis.
Bound waiting work so overload does not become unlimited memory growth. Moving the database
to another host separates resources but adds network latency and another failure boundary.
Caching can reduce reads but introduces freshness and invalidation decisions.

A single host is easy to operate but cannot serve during its own outage. A backup helps
recovery, not live availability. Ask what happens when a commit succeeds and the response is
lost: blindly retrying creation may create another mapping. Exactly one effect is not established
by merely drawing one database; later idempotency work must address that ambiguity.

## Check yourself

### Readiness before practice

1. At what event is create allowed to report success?
2. Which arrows belong to the shortener and which to the destination site?
3. What measurement could disprove your first bottleneck hypothesis?
4. What happens if the service crashes before commit versus after commit but before replying?

Run the model and explain its limits. Then use [the assignment](README.md#assignment) to draw
your baseline in [DESIGN.md](DESIGN.md). Read the [complete reference](REFERENCE_DESIGN.md)
before a guided attempt or compare afterwards. Reading alone does not complete practice.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-006-single-node-baseline)
