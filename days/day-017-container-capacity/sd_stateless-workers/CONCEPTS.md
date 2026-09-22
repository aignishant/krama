---
day: 17
part: "2.1"
title: "Make workers replaceable by locating authoritative state"
ids: [SD-17]
level: working
prerequisites: ["Days 10 and 16 retries; Day 15 domain ownership"]
failure: true
---

# Make workers replaceable by locating authoritative state

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Any healthy worker can serve the next request when authoritative session and link state live outside individual workers.

## The story

You log in, create a short link, and refresh after a deployment. The next worker knows
neither your session nor the link because the first worker kept both only in memory.

## The idea in plain language

Stateless workers may hold temporary request data, pools, and rebuildable caches. The
requirement is that correctness of a later request does not depend on reaching that same
process. Name the authoritative location for every fact and what happens when that location
is unavailable. Moving a dictionary to a shared service changes its failure boundary; it
does not remove state or automatically make it durable.

Build on [Day 15 domain ownership](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md)
and [Day 10 replay records](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md).
Opaque session tokens can identify records in shared storage. Link records and replay results
must survive worker replacement. Request-local parsing buffers can disappear after a crash.

## Why Krama needs it

This develops SD-17 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[The Twelve-Factor App — VI. Processes](https://12factor.net/processes) explains stateless,
share-nothing application processes with persistent data in backing services. The storage
choices and failure policy below are authored design decisions. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

First inventory state, then trace a replacement.

| Fact | Authority in this example | Safe local copy? |
| --- | --- | --- |
| Session identity, expiry, revocation | Shared session table | Omit initially to avoid stale revocation |
| Destination and link expiry | Shared links table | Omit initially to avoid stale redirects |
| Create-operation replay | Shared transactional replay table | Never the only copy |
| Parsed request and scratch calculation | Current request frame | Yes; loss ends that attempt |

A load balancer routes request 1 to A. A validates the shared session and commits a link
and replay result. A restarts. Request 2 reaches B with the same session token; B checks the
same shared session and reads the same link. The worker identity is irrelevant to those reads.
If the create response was lost, B uses the same owner/key to recover the committed result.

Correctness depends on shared storage's durability and atomicity guarantees, not merely its
network address. In this deliberately simple model, one durable database stores all three
tables. That removes worker affinity but adds remote storage latency and a common dependency.
There is no claim of database failover or outage tolerance without a separate design.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.
For SD, it is a local model of a failure, not a running service or a production measurement.

```python
worker_a = {"sessions": {"token": "owner-1"}, "links": {"c1": "destination"}}
worker_b = {"sessions": {}, "links": {}}
try:
    assert worker_b["sessions"].get("token") == "owner-1", "restart routing lost session state"
except AssertionError as error:
    print(f"AssertionError: {error}")
shared = {"sessions": dict(worker_a["sessions"]), "links": dict(worker_a["links"])}
worker_a.clear()
print("replacement reads:", shared["sessions"]["token"], shared["links"]["c1"])
assert shared["sessions"]["token"] == "owner-1"
assert shared["links"]["c1"] == "destination"
```

**Line by line:** The first dictionaries represent isolated worker memory and reproduce a missing-session
failure. The shared dictionary models storage outside the worker. Clearing A represents only
a worker restart, not a storage crash; the assertions verify logical ownership, not persistence.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
AssertionError: restart routing lost session state
replacement reads: owner-1 destination
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Bound each worker's database pool: adding workers also adds possible connections, as
[Day 11](../../day-011-group-anagrams/sd_connection-budgets/CONCEPTS.md) showed. Monitor storage
timeouts and pool waits as well as worker health. Session caches require a stated revocation
delay; link caches require expiry/deletion rules. Sticky routing can reduce cache misses but
cannot recover authoritative memory after a crash. Signed self-contained session tokens are
an alternative with different revocation and key-management tradeoffs.

## Check yourself

### Readiness before practice

1. Which state can disappear without corrupting a later request?
2. What lets B answer an uncertain create retry after A restarts?
3. Why does shared storage still need a durability policy?
4. What user behavior changes if session storage is unavailable?

Compare the [complete reference answer](REFERENCE_DESIGN.md) before guided practice or after your own attempt.

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
