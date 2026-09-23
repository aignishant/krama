---
day: 13
part: "2.1"
title: "Continue a listing from a stable ordered boundary"
ids: [SD-13]
level: working
prerequisites: ["Ordered tuples", "HTTP query parameters"]
failure: true
---

# Continue a listing from a stable ordered boundary

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

A cursor records the last returned ordering key, so the next page can request rows strictly beyond that boundary.

## The story

You open the second page of your saved links and see the last link from page one again. Someone created a newer link between requests, shifting every numbered position.

## The idea in plain language

Pagination splits a listing into bounded pages. Offset pagination counts how many rows to
skip; cursor pagination names where to continue in a declared order. A timestamp alone is not
unique, so use the pair (created_at, link_id). Compare timestamps first and IDs on ties.
Descending order means the next page uses keys strictly less than the last returned pair.
A cursor is continuation state, not an authorization token and not automatically a snapshot.
Recognize this design when a changing list needs sequential navigation without position shifts.

## Why Krama needs it

The [Week 2 design review](../../day-014-week-2-review/sd_week-2-design-review/CONCEPTS.md) revises a decision by tracing a concurrent change.

## The source behind it

[PostgreSQL 18 — LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html) explains deterministic ordering and the cost of skipped rows. The cursor policy below is an authored design choice. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Suppose newest-first keys are `(12, 9), (12, 8), (11, 7), (10, 6)`, where the first
component is an illustrative creation-time unit and IDs uniquely break ties. Page size is 2.
Page one returns IDs 9 and 8; its boundary is (12, 8). Insert (13, 10). Offset 2 now begins
with ID 8 again. A strict key comparison still returns 7 and 6.

Both pages use the same filters, owner scope, and ordering. If an unchanged row was already
returned, its key cannot be below the boundary, so it cannot repeat. This proof assumes keys
are immutable. A new older/backdated row may appear later, a deleted row may vanish, and a
newer row is omitted until refresh. That is a live traversal contract, not a frozen export.

Fetch page_size+1 rows: return the first page_size and use the extra only to decide whether
another page exists. Build the next cursor from the last returned row, never the lookahead.
With a matching owner/key index, a typical seek plan can approach O(log N + page_size) work;
verify the real plan. Without an appropriate index, filtering and sorting can dominate.
Offset work grows with rows skipped even though the response remains small.

## When it breaks

```python
rows = [(12, 9), (12, 8), (11, 7), (10, 6)]
first = rows[:2]
boundary = first[-1]
rows.insert(0, (13, 10))
offset_page = rows[2:4]
cursor_page = [row for row in rows if row < boundary][:2]
print("offset:", offset_page, "cursor:", cursor_page)
try:
    assert not set(first) & set(offset_page), "offset repeated a row after insertion"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert cursor_page == [(11, 7), (10, 6)]
```

**Line by line:** The tuples model a declared total order. Inserting a newer row shifts offsets but leaves the saved key unchanged. Strict comparison selects the continuation independently of its position. This is an executed in-memory ordering model, not a database benchmark.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
offset: [(12, 8), (11, 7)] cursor: [(11, 7), (10, 6)]
AssertionError: offset repeated a row after insertion
```

## In production

Validate cursor version, sort direction, filter identity, and owner scope. An opaque encoding alone prevents neither tampering nor data access; authenticate requests and scope every query. Choose a signed token or server-held cursor state when integrity matters. Bound page size and cursor lifetime. Snapshot exports need a separate consistency design and may retain expensive database state.

## Check yourself

### Readiness before practice

1. Why does the tie-breaker belong in both ordering and cursor?
2. Which comparator continues descending order?
3. Why does a new link not necessarily appear during this traversal?
4. Which row supplies the next cursor when using lookahead?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
