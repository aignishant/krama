---
day: 26
part: "2.1"
title: "Isolation anomalies"
ids: [SD-26]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Isolation anomalies

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

An atomic transaction can still make a decision from stale concurrent reads; enforce the invariant at the shared write boundary.

## The story

Two tabs both see one remaining quota unit. Each creates a link successfully, and the owner ends with two new links even though each tab saw a valid balance.

## The idea in plain language

Use [transactions](../../day-025-integer-square-root/sd_transactions/CONCEPTS.md).
An interleaving lists operations from different transactions in the order they occur. Each
transaction can be atomic while their combined decisions violate a rule. Isolation determines
which concurrent effects statements can observe. A lost update overwrites another change;
write skew can violate a shared rule through different written rows. Identify the actual
pattern instead of calling every race a dirty read.

## Why Krama needs it

This develops SD-26 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

Read the [complete reference answer](REFERENCE_DESIGN.md) within the concept/critique
window; keep your own practice in [DESIGN.md](DESIGN.md).

## The source behind it

[13.2. Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html) documents Read Committed update rechecks and serializable retry requirements; these guarantees are database-specific.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Suppose used=4 and limit=5. The unsafe application separately reads used and later writes
the computed value used+1, with a link insert in each transaction:

| Step | Transaction A | Transaction B | Consequence |
| --- | --- | --- | --- |
| 1 | read 4 | | A believes one unit remains |
| 2 | | read 4 | B believes one unit remains |
| 3 | insert link A; write literal 5; commit | | one allocation committed |
| 4 | | insert link B; write literal 5; commit | two links added, counter says one |

The counter never exceeds 5, so a local range CHECK misses the broken relationship. Wrapping
these stale decisions in transactions does not make the check fresh. This is a proposed
schedule for an application that overwrites with a precomputed literal, not every database's
behavior at every isolation level.

For this single-owner invariant, issue UPDATE owners SET used=used+1 WHERE id=:owner
AND used<quota_limit, then require one affected row before inserting a link in the same
transaction. PostgreSQL Read Committed can wait for a competing row update and re-evaluate
the condition on the updated row. The first reservation consumes the last unit; the second
then matches zero rows and creates no link. See the version-specific source below.

Alternatives: SELECT ... FOR UPDATE serializes the decision under a row lock; serializable
isolation can reject transactions whose combined effects cannot be serialized. Retrying a
serialization failure means starting the whole transaction again, including reads. A quota
rejection is a business result, not a transient error to retry in a tight loop. Under high
contention a single owner row becomes a coordination bottleneck; a distributed counter would
require a new correctness argument, not just a throughput claim.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
used, limit = 4, 5
read_a = read_b = used
links_added = 0
for stale_read in (read_a, read_b):
    if stale_read < limit:
        used = stale_read + 1
        links_added += 1
print("stale writes: used", used, "links added", links_added)
assert links_added > used - 4

used, links_added = 4, 0
for request in ("A", "B"):
    # One indivisible decision in this sequential model.
    if used < limit:
        used += 1
        links_added += 1
print("guarded reservations: used", used, "links added", links_added)
assert used == 5 and links_added == 1
```

**Line by line:** Both saved reads hold 4 even after the first write, reproducing the stale-literal lost update. The second loop models the intended serial decision, not a lock-free Python implementation or a database test. Its assertions check both the counter and allocation count, exposing the invariant the first loop lost.

Observed author output on Python 3.12.10, 2026-09-23:

```text
stale writes: used 5 links added 2
guarded reservations: used 5 links added 1
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

Review all paths that consume or release quota, not just one endpoint. Instrument affected-row
counts, lock waits, deadlocks, and transaction retries. Retry only failures classified as
transient, with a bounded attempt/deadline policy; recheck authorization and business conditions
on each new transaction. Optional depth: a quota computed from multiple rows can require a
different lock scope or serializable transaction, even if each individual row update is safe.

## Check yourself

### Readiness before practice

1. Why does used<=limit remain true in the broken trace?
2. What prevents a zero-row reservation from creating a link?
3. Which reads must be repeated after a serialization failure?
4. How does a quota rejection differ from a transient concurrency failure?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
