---
day: 33
part: "2.1"
title: "TTL and deletion"
ids: [SD-33]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# TTL and deletion

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Logical expiration, physical reclamation, and deletion propagation are separate contracts.

## The story

An expired link still exists in storage the next morning. Returning it because the cleanup worker has not run violates the promised expiration time.

## The idea in plain language

Recall [log-structured versions](../../day-030-merge-overlapping-intervals/sd_log-structured-storage/CONCEPTS.md). Logical expiration means the read path
treats a value as absent after its deadline. Physical cleanup later removes bytes. A tombstone
records a deletion so older values cannot reappear when files or replicas are reconciled.
TTL is a lifetime rule; it is not automatically a guarantee that every copy is erased at
the deadline. Distinguish serving eligibility from retention in primary storage, caches,
replicas, logs, and backups.

## Why Krama needs it

This develops SD-33. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Working with expired items and TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ttl-expired-items.html) distinguishes pending cleanup from filtering expired records. The replica/tombstone schedule here is a generic model.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Use an illustrative timeline in seconds: expires_at=100, read at 101, cleanup at 150.
The correct read at 101 is absent even though the row still occupies disk. The read predicate
is active and (no expiration or now<expires_at). Equality at 100 is already expired under
this contract. A cache must check the same deadline, not only whether its key exists.

For replicated deletion, assume replica R1 receives delete version 8 while offline R2 retains
value version 7. If R1 erases the tombstone before R2 is reconciled, an unsound merge policy
can restore version 7. Retain deletion knowledge until every allowed source of stale state
is reconciled or fenced out. A duration alone is insufficient without a maximum offline
window, repair guarantees, and a rebootstrap rule for replicas outside that window.

Longer retention consumes storage and can increase read/compaction work; shorter retention
requires stronger anti-resurrection controls. Delayed cleanup should expose storage usage and
maintenance backlog, not expired content to users. Wall-clock skew matters to expiry decisions:
define an authoritative clock policy and test boundary behavior. Physical deletion from every
backup is a separate retention workflow, not established by an application filter.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
row = {'target': 'old', 'expires_at': 100, 'active': True}
now = 101
wrong = row['target']  # Row existence alone is insufficient.
visible = row['target'] if row['active'] and now < row['expires_at'] else None
print('cleanup-dependent read:', wrong)
print('deadline-aware read:', visible)
assert visible is None
versions = [(7, 'old'), (8, None)]
assert max(versions)[1] is None
without_tombstone = [item for item in versions if item[1] is not None]
print('unsafe early purge reveals:', max(without_tombstone)[1])
assert max(without_tombstone)[1] == 'old'
```

**Line by line:** The read predicate enforces logical expiry before any deletion job. The version list then models a separate deletion-propagation hazard: removing the newest marker makes an older value appear newest among remaining candidates.

Observed author output on Python 3.12.10, 2026-09-23:

```text
cleanup-dependent read: old
deadline-aware read: None
unsafe early purge reveals: old
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Document whether expired items can appear in administrative views and exports, and restrict
those paths separately. Measure cleanup lag and disk headroom without treating either as the
user-visible expiry guarantee. A reviewer should ask how an old backup or long-offline replica
is restored without reviving deleted data. Optional depth: design clock-skew handling and
retention checks for each copy rather than applying one vague TTL to the whole system.

## Check yourself

### Readiness before practice

1. What should a read return before cleanup but after expiry?
2. What protects against an old replica reviving a value?
3. Why does cache existence not prove validity?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
