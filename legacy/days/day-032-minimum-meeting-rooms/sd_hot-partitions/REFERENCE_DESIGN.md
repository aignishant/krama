# Reference design — Hot partitions

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and requirement

Four partitions hold equal numbers of link records. Each has an assumed capacity of 1,000
reads/s for equal-cost point reads. These numbers exist solely for the example. Background
traffic totals 800 reads/s, evenly spread. One viral link receives 2,400 reads/s and hashes to
partition P0. The requirement is to explain the overload and select a bounded mitigation.

## Load calculation

| Partition | Background | Viral key | Total | Assumed capacity |
| --- | --- | --- | --- | --- |
| P0 | 200 reads/s | 2400 reads/s | 2600 reads/s | 1000 reads/s |
| P1 | 200 reads/s | 0 | 200 reads/s | 1000 reads/s |
| P2 | 200 reads/s | 0 | 200 reads/s | 1000 reads/s |
| P3 | 200 reads/s | 0 | 200 reads/s | 1000 reads/s |

Total utilization appears to be 3200/4000=80%, but P0 demand is 260% of its capacity. With
unbounded admission and the constant-rate model, its backlog grows at 1600 requests/s.
After five seconds that is 8,000 queued requests; real systems typically reject or time out
some work before that. Balanced record counts say nothing about this request skew.

## Decision and alternative

Cache the hot immutable redirect payload across serving workers or a cache tier with sufficient
capacity. At an assumed 90% hit rate on the viral key, source demand is 200+2400*0.10=440
reads/s on P0. Verify that hit rate and cache capacity; the arithmetic is not an observation.
Coalesce simultaneous misses and cap total fallback requests to the origin. Cap admission or
return a retryable response when the origin budget is exhausted rather than forming an unbounded
queue. Payload validity and expiry still apply to cached copies.

An alternative is read replication with an explicit freshness contract, appropriate if more
keys become hot or cache reuse is poor. Merely increasing hash partition count need not split
one key's traffic. For a hot click counter, deliberate write sharding can distribute increments,
but reading the total must sum shards and deduplicate retries. It is not the chosen redirect-read
mitigation because salting a point lookup without routing knowledge forces fan-out.

## Failure walkthrough

The popular cache entry expires on many workers at once. All miss and rush P0, temporarily
recreating the 2600 reads/s demand. Coalescing reduces duplicate in-flight loads per key, while
origin concurrency/admission limits bound the residual fleet-wide burst. Per-process coalescing
alone does not coordinate all workers. Add jitter to cache lifetimes only where it does not
extend the link's actual validity deadline. Monitor fallback rate and shed excess demand.

## Self-review and next verification

The calculation explains why spare cluster capacity does not protect one partition. Next,
measure request distribution by key and partition, load-test the viral key, then force cache
eviction/failure and inspect source queues and tail latency. The example does not claim a
provider quota, measured hit rate, or completed load test. Write hot spots require a separate
consistency and aggregation decision.


## Sources and comparison

[Designing partition keys effectively](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) explains why request distribution matters alongside data distribution. No vendor capacity limit is assumed here.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
