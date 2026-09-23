# Reference design: Isolation anomalies

Read before guided practice or compare after your independent attempt.

The scenario below is hypothetical. No PostgreSQL deployment or load test was run.
Your personal work belongs in [DESIGN.md](DESIGN.md); start with [CONCEPTS.md](CONCEPTS.md).

## Assumptions and requirement

One owner has quota_limit=5, used=4, and four existing links. Requests A and B each want one
new link. Both use the same relational database. All successful creations must preserve
used=owned-link-count<=quota_limit. The chosen implementation uses PostgreSQL Read Committed;
behavior under another engine or isolation level must be checked separately.

## Unsafe interleaving

| Step | A | B | Committed state |
| --- | --- | --- | --- |
| 1 | BEGIN; read used=4 | | used=4, links=4 |
| 2 | | BEGIN; read used=4 | unchanged |
| 3 | insert A; SET used=5; COMMIT | | used=5, links=5 |
| 4 | | insert B; SET used=5; COMMIT | used=5, links=6 |

The stale literal 5 in B's update overwrites the same value. Every individual row can pass a
range check, while two new links spend the one remaining unit. If instead the code blindly
increments twice, the counter reaches 6; a CHECK may reject that write, but the application
must still roll back the associated insert. The chosen remedy makes the admission decision
explicit rather than relying on an accidental constraint error.

## Revised artifact and retry behavior

Both requests begin a transaction and execute:

```sql
UPDATE owners
SET used = used + 1
WHERE id = :owner_id AND used < quota_limit
RETURNING used;
```

**Line by line:** The update reserves one unit using the current stored value. The predicate
is part of that write, not a preceding application read. The returned row is required before
inserting a link. Parameters represent bound values in application code.

A updates 4 to 5 and inserts its link. B attempting the same row waits while A holds its
write lock. If A commits, B rechecks the predicate against used=5, obtains zero rows, rolls
back its transaction, and returns the documented quota-exhausted business response. If A
rolls back, B can reserve the restored unit. A duplicate-code insert failure rolls back the
reservation too. The design serializes only this owner's reservation boundary.

| Result | Response policy |
| --- | --- |
| Zero rows because quota is full | reject; no automatic transient retry |
| Serialization failure or deadlock | roll back, retry the whole transaction with fresh reads |
| Connection loss around commit | uncertain; resolve using the durable operation key from Day 25 |
| Repeated contention | stop after the request deadline/attempt budget; return a retryable service outcome |

For this reference, use at most three transaction attempts and the remaining request deadline,
whichever ends first. Three is an illustrative policy choice, not an experimentally optimal
number. Delays should avoid synchronized retries; detailed backoff policy is a later topic.

## Decision and alternative

Choose the conditional increment for a rule contained in one owner row. SELECT ... FOR UPDATE
followed by a fresh check is a credible alternative: it makes the lock scope explicit and can
support more complex logic, but holds the lock across more application steps. Serializable
transactions are another option for invariants involving multiple rows, with whole-transaction
retry obligations. Changing isolation does not eliminate the need to specify client outcomes.

## Failure walkthrough

A reserves the final unit, then its insert fails. A rolls back. B, which was waiting, can now
reserve that unit and finish. If application code swallows A's error and commits only the
reservation, the quota leaks; therefore the error path must end the entire transaction.
No email or remote side effect is performed before the database outcome is known.

## Self-review

The schedule identifies a stale-write anomaly and tests the full accounting invariant. The
remedy specifies admission, rollback, waits, and retry classification. A hot owner's row can
limit throughput; observe lock waits and retry counts before redesigning that boundary.
A meaningful next verification uses two actual database connections and controlled barriers
to reproduce commit and rollback cases. The Python model is not that database experiment.

Source: [13.2. Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html),
checked 2026-09-23. In particular, the update-condition recheck is a PostgreSQL guarantee.
