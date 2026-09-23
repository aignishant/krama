---
day: 34
part: "2.1"
title: "Storage decision memo"
ids: [SD-34]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Storage decision memo

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Choose storage by the operations and failure invariants it must support, then state what would change the decision.

## The story

A team selects a key-value store for fast redirects, then discovers owner listings and safe create retries need access paths and atomicity it never designed.

## The idea in plain language

Recall [query modeling](../../day-031-insert-an-interval/sd_access-pattern-modeling/CONCEPTS.md), [hot partitions](../../day-032-minimum-meeting-rooms/sd_hot-partitions/CONCEPTS.md), and
[expiration](../../day-033-kth-smallest/sd_ttl-and-deletion/CONCEPTS.md). A storage decision compares a relational model—tables,
constraints, indexes, and transactions—with a key-value model centered on keyed access.
Neither name alone specifies consistency, durability, scalability, or failure behavior.
Compare concrete capabilities under explicit assumptions, not “SQL versus NoSQL” slogans.

## Why Krama needs it

This develops SD-34. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) and [partition-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) support the access-path tradeoffs. The recommendation is conditional on the stated workload.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Use three patterns: redirect by code; create a code exactly once per owner/request token;
list an owner's newest links. Require two failure properties: a timed-out committed create
must not create a second link on retry, and an expired link must never be served merely because
cleanup lags. A relational baseline can use unique code, unique(owner_id,request_id), an
owner/time/id index, and transactional create handling. A key-value alternative needs conditional
creation plus explicit secondary views and an atomic strategy for retry identity.

| Criterion | Relational baseline | Key-value alternative |
| --- | --- | --- |
| redirect | unique code index | keyed get |
| create retry | transaction + unique request key | conditional/transactional idempotency mapping |
| owner listing | composite ordered index | queryable secondary view or maintained index items |
| expiry | read predicate | same application predicate or verified native semantics |

For a hypothetical modest workload that fits one primary, choose the relational baseline
because it meets all three patterns with one transaction domain. This does not prove it will
meet an unspecified throughput target. Key-value storage becomes more attractive when keyed
traffic and measured scaling needs justify its view-maintenance complexity. Both still need
backups, failure recovery, hot-key mitigation, and deadline-aware reads.

Correctness comes from the enforcement point: a preflight existence check followed by an
unconditional insert is racy in either family. A unique/conditional write must resolve the
race, and retries must recover the original result. State the tolerated loss and freshness
requirements before discussing replica reads or asynchronous projections.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
requests = ['req-1', 'req-1']
naive = ['code-' + str(i) for i, request in enumerate(requests)]
by_request = {}
results = []
for request in requests:
    if request not in by_request:
        by_request[request] = 'code-' + str(len(by_request))
    results.append(by_request[request])
print('blind retry creates:', naive)
print('idempotent model:', results)
assert len(set(naive)) == 2 and len(set(results)) == 1
```

**Line by line:** The duplicate request token must map to the same result. The dictionary models the desired atomic behavior only; a real concurrent service must enforce uniqueness and result recovery in storage rather than copying this check-then-set sequence.

Observed author output on Python 3.12.10, 2026-09-23:

```text
blind retry creates: ['code-0', 'code-1']
idempotent model: ['code-0', 'code-0']
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Write the decision memo so a future engineer can reverse it when the assumptions change.
Measure throughput, skew, query latency, index size, and recovery behavior before migration.
A reviewer should ask which failure requirement is enforced by which operation, and which
new maintenance job is needed by the alternative. Optional depth: prototype both owner-list
access paths with representative skew and compare operational work as well as query speed.

## Check yourself

### Readiness before practice

1. Which three operations must the decision cover?
2. Where is retry uniqueness enforced?
3. What evidence would justify changing storage?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
