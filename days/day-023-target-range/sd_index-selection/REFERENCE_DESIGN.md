# Index reference — one owner's newest links

This proposed answer uses the [Day 22 schema](../../day-022-lower-bound/sd_schema-constraints/REFERENCE_DESIGN.md).
No index has been deployed or benchmarked. [DESIGN.md](DESIGN.md) remains your practice file.

## Workload and query assumptions

The main request lists one authorized owner's latest 20 links. Twenty rows is an illustrative
page size selected for this example, not a measured limit. Owners have unequal link counts;
we do not assume uniform distribution. Newest means created_at descending, with id descending
to break equal timestamps. Identity and creation time are stable across traversal.

```sql
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 20;

CREATE INDEX links_owner_newest_idx
ON links (owner_id, created_at DESC, id DESC);
```

The parameter is supplied by the authorized request context. Leading owner equality narrows
the ordered key range. Within it, the suffix matches the requested order and can let a scan
stop after enough visible qualifying rows. The id tie breaker gives deterministic ordering;
it does not claim transaction commit order. The selected payload can require heap access:
destination_url and code are not in this index.

## Why column order changes usefulness

Assume five illustrative entries (owner,tick,id): (A,10,1), (B,30,2), (A,20,3), (B,40,4),
(A,20,5). Ticks represent order only. The proposed index groups A's IDs as 5,3,1 before B's
4,2. A time-first index instead orders IDs 4,2,5,3,1, interleaving owners. It can serve a
global newest feed well but may examine many other owners for an owner-specific request.
The model's small count is not a prediction of pages read on a deployed database.

[PostgreSQL multicolumn B-tree rules](https://www.postgresql.org/docs/18/indexes-multicolumn.html)
support leading equality with an ordered suffix. A time-first index is not categorically
unusable: non-leading conditions and, in PostgreSQL 18, suitable skip-scan choices may help.
The chosen path depends on statistics and cost. Matching index order can avoid a separate
sort, as described by [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html).

## Alternative and costs

An owner-only index is smaller and can narrow the matching set before sorting it. It may be
adequate if each owner has few links. A time-first index is preferable for global feeds.
Maintain the proposed composite index only if owner listings justify its storage and insert/
update overhead. Including long URL payloads might reduce some heap reads but expands the
index and still does not guarantee index-only execution; measure before choosing that variant.

## Failure walkthrough

A time-first scan seeks the newest global rows for an owner with sparse activity. Many rows
belong to other owners, so returning 20 may require much more work than the page size suggests.
The user sees slow listings even though an index exists. Correct filtering still returns the
right owner; moving LIMIT ahead of the owner filter would instead create a correctness bug.
Repair the access path around owner equality, then compare actual scanned work and latency.
An independent correctness failure occurs when equal timestamps have no tie breaker: repeated
requests can return unstable ordering. Keeping id in both query order and index fixes that
ambiguity under the stated stable-key assumption.

## Self-review and next verification

The key order is justified by one explicit query. It does not accelerate every lookup or
promise a fixed response time. Compare plans and executions for small, large, and sparse
owners, including tied timestamps, and inspect write overhead and index size. Day 24 explains
those plans. Preserve the same predicates, ORDER BY, and result semantics while comparing;
the proposed improvement remains unmeasured.
