---
day: 23
part: "2.1"
title: "Order an index around the query"
ids: [SD-23]
level: working
prerequisites: ["Day 22 link schema; equality filters and sorting"]
failure: true
---

# Order an index around the query

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

For an owner-specific newest-first listing, lead with owner equality and follow it with the requested order and a unique tie breaker.

## The story

An index on every relevant column can still scan many irrelevant records if its leading order interleaves all owners.

## The idea in plain language

An index is a maintained access path. A multicolumn B-tree orders key tuples, comparing
earlier components first. For `WHERE owner_id = ? ORDER BY created_at DESC, id DESC`,
placing owner first groups the relevant rows, and the suffix orders that group for output.
Selectivity is the fraction of rows matching a predicate; it affects whether a path is
attractive. An index helps a workload under assumptions, not every query touching its columns.

## Why Krama needs it

This develops SD-23 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[PostgreSQL 18 multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) and [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html) support the access-path tradeoff and skip-scan qualification.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Toy records use logical time ticks, not measured timestamps:

| id | owner | created tick |
| --- | --- | --- |
| 1 | A | 10 |
| 2 | B | 30 |
| 3 | A | 20 |
| 4 | B | 40 |
| 5 | A | 20 |

For owner A, the expected newest-first IDs are 5,3,1. Keys
(owner ASC, created DESC, id DESC) place those three adjacent and ordered. Swapping the
first columns to (created DESC, owner ASC, id DESC) gives global order 4,2,5,3,1;
an owner-A query may examine unrelated B rows before finding its results. The timestamp
tie needs id DESC so two rows created together still have a deterministic order.

This explains suitability, not an absolute prohibition: PostgreSQL can use non-leading
conditions, and PostgreSQL 18 may use skip scan when its cost model favors it. Actual row
distribution and LIMIT matter. A conceptual B-tree seek plus k matching entries is often
described as O(log N+k); heap access, visibility, extra filters, and page locality still
determine database work. An owner-only index narrows rows but may still require sorting.
An index ordered by time first instead fits a global newest-links feed.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
rows = [('A', 10, 1), ('B', 30, 2), ('A', 20, 3), ('B', 40, 4), ('A', 20, 5)]
owner_first = sorted(rows, key=lambda r: (r[0], -r[1], -r[2]))
time_first = sorted(rows, key=lambda r: (-r[1], r[0], -r[2]))
print('owner-first IDs:', [r[2] for r in owner_first])
print('time-first IDs:', [r[2] for r in time_first])
wrong = [r[2] for r in time_first[:2] if r[0] == 'A']
right = [r[2] for r in owner_first if r[0] == 'A'][:2]
print('limit before owner filter:', wrong, 'owner result:', right)
assert wrong == [] and right == [5, 3]
```

**Line by line:** Sorting tuple keys illustrates the two index orders. Taking the global top two before filtering owner is a deliberately wrong query transformation, not what PostgreSQL does. Filtering the correct owner before limiting preserves semantics.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
owner-first IDs: [5, 3, 1, 4, 2]
time-first IDs: [4, 2, 5, 3, 1]
limit before owner filter: [] owner result: [5, 3]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Each extra index consumes storage and adds write work. Including a large URL payload can
increase that cost; an index-only path also depends on visibility and query coverage, not
just column presence. Optional depth: a continuation predicate on (created_at,id) can avoid
large offsets, but cursor design belongs to the earlier pagination contract. Inspect a plan
and representative owner distributions before claiming a latency improvement.

## Check yourself

### Readiness before practice

1. Why put an equality-constrained owner before the ordered suffix?
2. Why is created_at alone insufficient for deterministic ties?
3. Which workload would favor time-first ordering?
4. Why is “non-leading columns can never use an index” too strong?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.


For a complete worked answer, read [REFERENCE_DESIGN.md](REFERENCE_DESIGN.md). Your own practice belongs in [DESIGN.md](DESIGN.md).
