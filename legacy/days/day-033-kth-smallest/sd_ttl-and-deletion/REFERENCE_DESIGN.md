# Reference design — TTL and deletion

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and contract

A link has active, expires_at, and a version. expires_at is a UTC instant interpreted by a
defined service clock; the contract treats now>=expires_at as expired. Logical expiration
must not wait for physical cleanup. Cached payloads include the same deadline. Storage may
retain expired rows for asynchronous cleanup, and replicated deletion uses ordered tombstones.

## State and retention artifact

| Time in illustrative seconds | State | Allowed redirect? |
| --- | --- | --- |
| 99 | stored; expires_at=100 | yes if active |
| 100 | logically expired, row remains | no |
| 120 | cleanup delayed, cache entry may remain | no |
| 150 | cleanup processes row/deletion | no |

Enforce active AND (expires_at is absent OR now<expires_at) on every serving path. Set a
cache lifetime no later than the remaining logical lifetime, and still validate expires_at
on a hit. A cleanup outage can grow storage and maintenance work; it must not expose the
expired destination. An administrative retention view may include expired metadata if its
authorization and labeling allow it. This serving rule is not a guarantee of physical erasure.

For deletion propagation, choose an illustrative maximum offline participation window of
24 hours and a required repair completion bound of 6 hours after return. Retain tombstones
for at least 48 hours in this proposed policy: 24+6=30 hours plus 18 hours of operational
margin. These numbers are assumptions requiring validation, not universal settings. If a
replica misses the participation or repair bounds, fence it and rebootstrap from current
state; do not merge its old data back after deletion history has been retired. Failed repair
extends retention or fences stale participants. Snapshots and backups need separate restore
rules preserving deletion knowledge.

## Decision and alternative

Use read-time expiration with asynchronous reclamation, and retain deletion metadata according
to supported stale-state windows. It tolerates delayed cleanup while maintaining serving
correctness. Synchronous deletion at expiry is an alternative for earlier reclamation but
requires reliable scheduling and still leaves cache/replica/backup semantics unresolved.
Explicit deny-state checks against an authoritative store can support stricter revocation at
the cost of read availability and latency.

## Failure walkthrough

R2 goes offline with live version 7. R1 accepts tombstone version 8. A naive process drops
the tombstone early; R2 returns with version 7 and old content resurfaces. Under this policy,
version 8 is retained through the permitted repair window. A too-late R2 is fenced and rebuilt,
so it cannot reintroduce v7. An independently expired v7 should also fail the read predicate;
the tombstone rule matters for deletion of values with no reached expiry deadline too.

## Self-review

Logical visibility, physical cleanup, and stale-state prevention have separate enforcement.
Remaining uncertainty includes clock skew, maximum outage, actual repair duration, and backup
retention. Test reads exactly at expiry, cache hits after expiry, delayed cleanup, and a replica
returning beyond the retention window. Only the lesson's abstract state model has been run;
the 48-hour policy has not been validated against a deployed replication system.


## Sources and comparison

[Working with expired items and TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ttl-expired-items.html) distinguishes pending cleanup from filtering expired records. The replica/tombstone schedule here is a generic model.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
