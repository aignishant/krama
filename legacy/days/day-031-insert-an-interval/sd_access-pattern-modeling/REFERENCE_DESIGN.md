# Reference design — Access-pattern modeling

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and access contracts

Clicks are immutable events with globally unique event_id, link_id, owner_id_at_event,
occurred_at in UTC, and ingested_at. A retry carries the same event ID. Owner identity is
captured at event time; a later transfer does not rewrite historical attribution. Two queries
are required: the latest 20 events for an authorized link owner, and counts per owner over
a chosen UTC-day range. Twenty is an illustrative UI size, not measured demand.

Recent events reflect committed source data. Daily totals may lag by a target of 60 seconds;
this target must be measured. They are eventually exact for accepted unique events after
projection catches up. Client event time is validated against a stated ingestion policy before
acceptance; the service must decide how far back late events may update retained daily buckets.

## Data and query artifact

| Representation | Identity / ordered key | Purpose |
| --- | --- | --- |
| Click source | unique event_id | deduplication and rebuilding |
| Recent-link access path | (link_id, occurred_at DESC, event_id DESC) | ordered detail page |
| Owner daily totals | (owner_id_at_event, UTC_day) -> count | sum one row per selected day |
| Projection receipts | unique event_id | prevent repeated increments during replay |

Recent query: authorize link, filter link_id, order by (occurred_at,event_id) descending,
limit 20. Subsequent pages use both last-seen fields as a cursor, avoiding tied-time ambiguity.
This is ordered traversal, not a cross-request snapshot guarantee. Owner query: authorize owner,
read the requested daily buckets, and sum counts. A missing bucket is zero only if its projection
state is known; expose a freshness watermark so zero is not confused with unprocessed history.

```text
accepted unique event -> durable source -> projector
                                           |
                 atomic receipt insert + owner/day count increment
                                           |
                            advance durable processing position
```

An atomic conditional receipt insertion and increment can share a transaction. A failed
duplicate receipt means no increment. A crash after commit but before position advancement
replays the event and safely finds the receipt. Advancing position before committing the
effect would lose an event. Receipts must cover the permitted replay window, or a rebuild
must produce fresh counts from deduplicated source events instead.

## Decision and alternative

Start with a relational events table, the ordered link index, and transactional daily projection
if asynchronous freshness is acceptable. A synchronous source insert plus count update is simpler
for exact committed totals at moderate volume but couples ingestion to the aggregate's write
contention. An asynchronous design adds lag and recovery work while separating those paths.
These are choices derived from queries, not claims that one database family is required.

## Failure walkthrough

e1 for owner A/link L is committed; projection increments A to 1. The worker crashes before
acknowledging delivery. On replay, a blind increment yields 2. With the atomic receipt-plus-count
transaction, e1 already has a receipt and count remains 1. Add e2 for A/link M and total becomes
2. A delayed e3 updates its event-day bucket, not silently today's bucket. If the projector
stalls beyond 60 seconds, show stale freshness and alert; do not call the old total current.

## Self-review

Both access patterns have keys, order, ownership, and freshness semantics. Remaining questions
are retention, late-event window, event-ID trust, hot-owner contention, and rebuild cost. Next,
test duplicate delivery, crash between commit and acknowledgment, tied timestamps, transfer of
ownership, and delayed projection. This memo and the small dedupe model are not database tests.


## Sources and comparison

[PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) supports the access-path discussion. The event and aggregate contracts here are design assumptions.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
