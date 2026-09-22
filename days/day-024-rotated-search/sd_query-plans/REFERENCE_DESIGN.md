# Query-plan reference — scan, filter, order, and limit

This is a completed interpretation of a proposed query using the
[Day 22 schema](../../day-022-lower-bound/sd_schema-constraints/REFERENCE_DESIGN.md) and
[Day 23 index](../../day-023-target-range/sd_index-selection/REFERENCE_DESIGN.md).
No database was run. The shapes below are conceptual possibilities, not captured EXPLAIN
output. [DESIGN.md](DESIGN.md) is your own artifact and evidence file.

## Assumptions and query

Owner 7 is an illustrative existing owner ID. The client requests the newest 20 links,
ordered by creation timestamp and then ID descending. Twenty is a chosen page size in rows;
it is not an estimate of scanned rows. Owner cardinalities, table size, cache state, latency,
and planner statistics are unknown.

```sql
EXPLAIN
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = 7
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## Read the row flow

One possible shape without a useful ordered access path is:

```text
Limit: emit at most 20 rows
  Sort: created_at DESC, id DESC
    Sequential scan of links, with filter owner_id = 7
```

Read from the leaf upward. The scan visits table rows, applies the owner predicate, and
emits matching rows. The sort considers those matches and supplies the requested order.
Limit consumes at most 20 sorted results. PostgreSQL may use a bounded sort strategy; that
does not imply it avoids examining the qualifying input. If five illustrative stored rows
include three owner-7 rows, the scan can visit five, filter to three, and limit emit three.
Those are hand-trace counts, not estimates from a real plan.

With links_owner_newest_idx, another possible shape is:

```text
Limit: emit at most 20 rows
  Ordered index scan using links_owner_newest_idx
    Index condition: owner_id = 7
```

The owner condition narrows the key range and the suffix supplies order, potentially removing
Sort. Heap visibility and payload retrieval still matter. Extra predicates could appear as
filters and make more entries necessary. A small table may legitimately use scan plus sort.

## Interpret the fields without inventing measurements

| Field | Meaning in this review |
| --- | --- |
| cost=startup..total | Planner cost units; neither milliseconds nor a service deadline |
| rows | Estimated output rows for a node; not all visited input rows |
| width | Estimated output row width in bytes |
| actual time/rows/loops | Execution observations from ANALYZE; per-loop time/row figures need loop context |
| Buffers | Database buffer/page activity, not full client latency |

Parent costs include child costs. Summing costs down a path therefore double-counts.
[PostgreSQL Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) supplies
these distinctions; [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html)
explains the candidate Sort elimination. These sources support interpretation, not a claim
that either conceptual plan will be chosen for an unmeasured data set.

## Decision and alternative

Start by inspecting plain EXPLAIN for the real schema and representative owner IDs. If
measurement is appropriate in a controlled database, this read-only query can be run as:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = 7
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

ANALYZE here executes SELECT; it adds load and returns instrumentation rather than the query's
normal result set. Do not treat ANALYZE as a dry run of arbitrary writes. The alternative is
to reason from estimates only, with lower operational impact but no claim of actual speed.
Separate SQL timings from connection wait, serialization, transport, and user-visible latency.

## Failure walkthrough

Suppose the planner expects few matching rows but this owner actually owns a large fraction
of the table. A path chosen from that estimate can do far more work than expected, especially
with additional filtering or sorting. The client experiences delay. Compare estimate and
actual cardinality at the first divergent node, inspect statistics and data skew, then assess
updated statistics or a revised access path. Forcing an index because its name exists can
make things worse. This is a hypothetical incident and proposed investigation, not an observed
slow query or proof that stale statistics caused one.

## Self-review

The artifact explains scan, filter, sort, limit, both access-path choices, and estimated
versus observed evidence. It intentionally contains no fabricated plan costs or timings.
Next verification is a captured plan with database version, representative data distribution,
query parameters, row results checked separately, and actual execution observations if run.
The concepts lesson's Python model only verifies the row-ordering example.
