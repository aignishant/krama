---
day: 32
part: "2.1"
title: "Hot partitions"
ids: [SD-32]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Hot partitions

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Evenly distributed keys can leave one partition overloaded when request rates are highly skewed.

## The story

Four storage nodes each hold the same number of links. A viral link overwhelms one node while the other three are almost idle.

## The idea in plain language

Recall [traffic estimates](../../day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md) and [access patterns](../../day-031-insert-an-interval/sd_access-pattern-modeling/CONCEPTS.md). A partition
owns a subset of keys. Hashing can distribute distinct keys evenly, but every request for
one key still reaches its owner under a simple hash partition scheme. A hot key gets a large
share of requests; a hot partition receives more total work than it can handle. Storage
balance measures bytes or records, whereas traffic balance measures operations and their cost.

## Why Krama needs it

This develops SD-32. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Designing partition keys effectively](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) explains why request distribution matters alongside data distribution. No vendor capacity limit is assumed here.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Assume four partitions, each able to sustain 1,000 reads/s for the modeled workload. This
is an illustrative assumption, not a vendor quota or measured capacity. Background traffic
is 800 reads/s total, evenly split at 200 each. A single key adds 2,400 reads/s to partition 0.

| Partition | Background reads/s | Hot-key reads/s | Total reads/s |
| --- | --- | --- | --- |
| 0 | 200 | 2400 | 2600 |
| 1–3, each | 200 | 0 | 200 |

Cluster demand is 3,200 against nominal total 4,000, yet partition 0 exceeds its capacity by
1,600 reads/s. In a simple queue model, backlog grows by that much each second until requests
are rejected, time out, or the load changes. Adding partitions without changing how the hot
key is served can leave all 2,400 reads on one owner.

For immutable redirect payload reads, replicated caches can absorb repeated access. An assumed
90% hot-key hit rate leaves 240 source reads/s plus 200 background=440 on the owner. This is
conditional arithmetic, not a measured hit rate. Hot writes require a different response:
sharded counters can spread independent increments but need read aggregation and replay-safe
updates. Randomly salting a lookup key makes reads fan out unless the routing is explicit.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
loads = [2600, 200, 200, 200]
capacity = 1000
print('aggregate fits:', sum(loads) <= 4*capacity)
print('every partition fits:', all(x <= capacity for x in loads))
assert sum(loads) == 3200 and max(loads) > capacity
remaining = 200 + 2400*(1 - 0.9)
print('assumed cache relief, reads/s:', round(remaining))
assert round(remaining) == 440
```

**Line by line:** Summing capacity hides the overloaded partition; checking each load exposes it. The hit-rate calculation isolates only the hot-key traffic, leaving background reads unchanged.

Observed author output on Python 3.12.10, 2026-09-23:

```text
aggregate fits: True
every partition fits: False
assumed cache relief, reads/s: 440
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Measure per-key and per-partition rates, tail latency, and throttling, including bursts.
Cache misses can synchronize after expiry or eviction, creating a stampede; request coalescing
and bounded origin concurrency matter alongside average hit rate. A reviewer should ask how
the proposed mitigation behaves for hot writes and during cache failure. Optional depth:
evaluate replication freshness and the fan-out cost of deliberate write sharding.

## Check yourself

### Readiness before practice

1. Why does spare cluster capacity not fix partition 0?
2. What assumption makes 440 reads/s plausible?
3. Why is salting read keys different from sharding counters?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
