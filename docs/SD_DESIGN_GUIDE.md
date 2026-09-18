# A repeatable system design method

Use this guide throughout the 30-minute track. A daily task asks for one piece of a design,
not a complete architecture every day.

1. **Define the operation.** State who uses it, what it returns and what is outside scope.
2. **State quality targets.** Latency needs a percentile and measurement boundary. Availability
   needs a definition of a successful request. Freshness and durability are separate requirements.
3. **Estimate with units.** Daily events divided by 86400 gives average events/second. Peak load
   needs an explicit assumption. Storage is records × bytes/record × retention, then separately
   account for indexes, replicas and temporary data. These are planning estimates until measured.
4. **Choose the source of truth.** For every important fact, name where the durable authoritative
   value lives. Caches, queues and search indexes may contain derived copies with different freshness.
5. **Design APIs and data together.** Start from access patterns and invariants. An API promising
   atomic behavior needs a storage or coordination boundary that can enforce it.
6. **Draw the simple path.** Label reads, writes, asynchronous edges and ownership. Trace one
   request end to end before adding specialized components.
7. **Find the limiting resource.** CPU, memory, connections, bandwidth and storage have different
   remedies. Replicating workers cannot fix one overloaded database record.
8. **Trace failures.** Consider a crash before an effect, after an effect but before acknowledgment,
   and during recovery. Ask what the user observes, which invariant survives and what gets retried.
9. **Compare alternatives.** Explain what is worse about your chosen design. State the measured
   threshold or changed requirement that would make a different option preferable.

## Concepts that are easy to mix up

| Concepts | Distinction to defend |
| --- | --- |
| Throughput and latency | More simultaneous work can increase throughput while worsening waiting time. |
| Replication and partitioning | Replication makes copies; partitioning divides responsibility. Many systems use both. |
| Durability and availability | An unavailable system may preserve data; a responsive system may lose recent data. |
| Cache TTL and eviction | TTL controls freshness/expiry; eviction makes room under memory pressure. |
| Delivery and effect | Duplicate delivery can still produce one business effect if deduplication is durable and atomic with that effect. |
| Consensus and transactions | Agreement on an ordered log is not the same abstraction as an application transaction spanning resources. |
| Authentication and authorization | Knowing the caller does not imply that caller may access this particular object. |
| Backup and recovery | A backup's existence does not demonstrate a working restore within the recovery objective. |

## Case-study rhythm

The six sessions of a case study accumulate: requirements, API/data, capacity, architecture,
one deep dive and failure review. Reuse prior sessions' artifacts. The seventh session revises
the weakest decision. You are building a portfolio of defensible reasoning, not a collection
of diagrams filled with every available technology.

## Failure exercise

Take one write. Draw three states: not applied, applied but response lost, and acknowledged.
Introduce a retry at each state. Explain how the service detects a duplicate, whether the
duplicate record survives restart, and whether recording the key is atomic with the actual
business effect. If the side effect crosses another service boundary, describe the uncertainty
and reconciliation path explicitly instead of labeling it exactly once.

## Reference navigation

The [source ledger](SOURCES.md) links verified source records. Use HTTP Semantics for request
contracts, the database concurrency chapter for transaction behavior, the consensus paper for
agreement mechanisms, and reliability-book chapters for operations. They support particular
decisions; none supplies a universal architecture for every case study.
