---
day: 24
part: "2.1"
title: "Read a query plan as a flow of rows"
ids: [SD-24]
level: working
prerequisites: ["Days 22–23 schema and indexes"]
failure: true
---

# Read a query plan as a flow of rows

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Follow rows from scan through filtering, ordering, and limit, distinguishing planner estimates from executed evidence.

## The story

A plan says rows=20 and cost=40. Neither proves the query examines only twenty rows nor takes forty milliseconds.

## The idea in plain language

SQL states the required result; a plan proposes physical operations producing it.
EXPLAIN without ANALYZE reports an estimated plan. EXPLAIN ANALYZE executes the query and
adds observed execution statistics. A node emits rows to its parent. A filter rejects rows
already visited by its scan, while an index condition can restrict the index search. A sort
establishes output order unless the chosen access path already supplies it.

## Why Krama needs it

This develops SD-24 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[PostgreSQL 18 Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) defines estimated and actual plan fields; [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html) explains avoiding an explicit sort.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

For the owner listing from [Day 23](../../day-023-target-range/sd_index-selection/CONCEPTS.md),
a conceptual path is scan links → filter owner=7 → sort by created_at/id descending → limit 20.
This is a hand-drawn possibility, not captured EXPLAIN output. Read it bottom-up even if a
printed plan displays Limit at the top. PostgreSQL can attach the filter directly to the
scan node; it need not appear as a separate node.

With illustrative rows [(A,1),(B,9),(A,4),(A,3)], scanning visits four rows, filtering emits
three A rows, sorting produces A4,A3,A1, and limit two emits A4,A3. Limiting before sorting
the matching input would emit A4,A1 instead. LIMIT does not always avoid upstream work:
a sort may need to consider all qualifying rows before identifying the best ones.

With the owner/time index, an ordered index scan may feed Limit without a separate Sort.
For a tiny table or a low-selectivity request, scan plus sort can still be reasonable.
Plan cost is in planner units, not milliseconds; rows estimates are output counts per node.
Parent cost includes child work, so adding all node costs double-counts. In executed plans,
actual time and rows are reported per loop when a node runs repeatedly. Buffer counts
describe page activity, not direct end-to-end response time. The [reference](REFERENCE_DESIGN.md)
shows a complete interpretation and an optional read-only validation query.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
rows = [('A', 1), ('B', 9), ('A', 4), ('A', 3)]
filtered = [r for r in rows if r[0] == 'A']
ordered = sorted(filtered, key=lambda r: -r[1])
right = ordered[:2]
wrong = sorted(filtered[:2], key=lambda r: -r[1])
print('visited/emitted/returned:', len(rows), len(filtered), len(right))
print('limit before sort:', wrong, 'sort before limit:', right)
assert wrong != right
assert right == [('A', 4), ('A', 3)]
```

**Line by line:** The lists model row flow and make the misplaced limit observable. The counts are actual Python model counts; they are not database estimates, query execution timings, or benchmark results.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
visited/emitted/returned: 4 3 2
limit before sort: [('A', 4), ('A', 1)] sort before limit: [('A', 4), ('A', 3)]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Find the first large estimate error and the work amplified downstream. Skewed owners or
stale statistics can undermine a planner assumption; do not force an index solely because
an index exists. For optional measurement use representative data and SELECT in a controlled
database. ANALYZE executes its statement, so it is not a harmless preview for arbitrary
writes. Keep database execution time separate from application and network latency.

## Check yourself

### Readiness before practice

1. How can a scan visit a million rows but emit only twenty?
2. Why is planner cost not elapsed milliseconds?
3. When can an ordered index remove a Sort node?
4. Which observations require ANALYZE rather than plain EXPLAIN?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
