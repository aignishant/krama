---
day: 31
part: "2.1"
title: "Access-pattern modeling"
ids: [SD-31]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Access-pattern modeling

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Define the query, order, freshness, and ownership before choosing storage keys or derived aggregates.

## The story

A clicks table answers one link’s recent activity quickly, but an owner’s dashboard must scan every event because its access pattern was never modeled.

## The idea in plain language

Recall [domain modeling](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md) and [index selection](../../day-023-target-range/sd_index-selection/CONCEPTS.md). An access
pattern describes a concrete read or write: equality filters, time range, ordering, output
size, and freshness. A derived aggregate stores a summary maintained from source events.
The two assigned queries need different shapes: detailed events for one link and a count
across an owner's links. One well-chosen key does not automatically serve both.

## Why Krama needs it

This develops SD-31. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) supports the access-path discussion. The event and aggregate contracts here are design assumptions.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Assume events carry event_id, link_id, owner_id_at_event, occurred_at, and an immutable
payload. The ownership snapshot means later link transfers do not rewrite historical counts.

| Query | Filter and order | Proposed representation |
| --- | --- | --- |
| recent clicks | link equality; time/id descending; limit 20 | events index (link_id,time DESC,event_id DESC) |
| owner totals | owner equality; UTC day range | daily count keyed by (owner_id,day) |

Twenty rows is a chosen UI page size. Use (time,id) as a cursor to break equal timestamps.
The aggregate can lag the durable event stream by a stated target, here an illustrative
60 seconds; it cannot silently claim real-time exactness. A synchronous transaction can
insert a unique event and update a count once. An asynchronous projector must atomically
record deduplication state with the increment or be replay-safe by another explicit method.

Example: e1 belongs to owner A/link L, e2 to A/M, and a retry of e1 arrives. Recent L events
contain e1 once; A's count is 2, not 3. The source event identity supplies the invariant.
Read savings cost extra writes, storage, and a reconciliation path. With an ordered index,
fetching a small link page can avoid scanning all events; owner summaries read one row per
selected day rather than one per click. Backfills, late events, and dedupe retention complicate
the summary and must be included in its contract.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
events = [('e1', 'A'), ('e2', 'A'), ('e1', 'A')]
naive = len(events)
seen = set()
count = 0
for event_id, owner in events:
    if event_id not in seen:
        seen.add(event_id)
        count += 1
print('blind increments:', naive, 'deduplicated:', count)
assert naive == 3 and count == 2
```

**Line by line:** The replayed event increments the naive counter twice. The set models an atomic deduplication-and-increment decision only in a single-threaded interpreter; separate database writes would not inherit atomicity from this example.

Observed author output on Python 3.12.10, 2026-09-23:

```text
blind increments: 3 deduplicated: 2
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Begin with a simple queryable source model, then materialize only summaries justified by
query volume. Persist event identity and define late-arrival behavior before promising exact
totals. A reviewer should ask how to rebuild a corrupt aggregate and whether retained source
history covers the reporting window. Optional depth: compare transactionally maintained daily
counts with an asynchronous projection under the same freshness requirement.

## Check yourself

### Readiness before practice

1. Which fields make recent-event ordering deterministic?
2. Does a link transfer change historical owner totals here?
3. What must be atomic to deduplicate increments safely?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
