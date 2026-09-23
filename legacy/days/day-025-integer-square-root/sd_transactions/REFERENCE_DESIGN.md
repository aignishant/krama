# Reference design: Transactions

Read before guided practice or compare after your independent attempt.

The scenario below is hypothetical. No PostgreSQL deployment or load test was run.
Your personal work belongs in [DESIGN.md](DESIGN.md); start with [CONCEPTS.md](CONCEPTS.md).

## Assumptions and invariant

One PostgreSQL database owns owners, links, and create-operation records. For this bounded
example there are no deletions, and used equals the number of owned links. Each link consumes
one unit. Owner 7 initially owns two links, used=2, quota_limit=3. These are illustrative counts,
not traffic measurements. The authenticated owner cannot choose another owner's identifier.

The requirement is that a committed create adds exactly one link and one used unit, or adds
neither. A unique constraint protects link codes; a foreign key protects owner identity.
A local CHECK enforces 0<=used<=quota_limit. The application transaction maintains the
cross-table equality, including every future deletion path if that feature is introduced.

## Artifact: one connection, one transaction

1. Begin a transaction. Claim a client operation key under a unique (owner_id, operation_key)
   constraint, storing a request fingerprint. If a committed matching operation exists, return
   its stored result without reserving quota again. A reused key with a different payload is
   a conflict. Concurrent claims must wait for or resolve the unique-key outcome before proceeding.
2. Reserve quota with the conditional statement below. Require exactly one returned row.
   Zero rows means reject this authenticated owner's create as quota exhausted, provided the
   owner still exists; a missing owner is handled as an identity/resource failure.
3. Insert the link and attach its result to the claimed operation record in this transaction.
4. Commit, then return success. Any failure before commit rolls back all changes, including
   the operation claim. A successful operation record therefore describes committed work.

```sql
UPDATE owners
SET used = used + 1
WHERE id = :owner_id AND used < quota_limit
RETURNING used;
```

**Line by line:** UPDATE targets the authoritative owner row. SET increments the stored value,
not a previously read application value. WHERE combines identity and remaining capacity.
RETURNING supplies the reservation result; continuing after zero rows would break the contract.
The colon parameter is pseudocode for driver binding, not literal SQL to paste into psql.

| Failure point | Committed state (used, link count) | User outcome and action |
| --- | --- | --- |
| Before reservation | (2,2) | no new link; retry same key if appropriate |
| After reservation, before insert | (2,2) after rollback | no quota leak |
| Insert hits a duplicate code | (2,2) after rollback | generate another code in a fresh bounded attempt |
| After insert, before commit | (2,2) after rollback | neither partial effect survives |
| After commit, before response | (3,3) | uncertain reply; replay same key to recover stored result |

The rollback example in CONCEPTS.md executes only a SQLite rollback scenario. This PostgreSQL
schedule and key protocol are design artifacts, not observed concurrent test results.

## Decision and alternative

Choose a single database transaction because both authoritative effects fit one storage boundary.
Keep external notifications outside it. The alternative is deriving usage with COUNT over links,
removing the denormalized counter but requiring a concurrency strategy for the check-and-insert
rule and adding read work. Separate autocommitted statements are not adequate: a failure can
leave an uncharged link or a charged quota without a link.

## Failure walkthrough

The process loses its connection after the quota update. No COMMIT reached the database, so the
open transaction is rolled back when the session ends; a pooled client must explicitly roll
back on handled errors. The caller sees failure, and a retry starts from the unchanged state.
If the connection instead fails while committing, the application cannot infer whether commit
succeeded. A replay with the same durable operation key resolves that uncertainty without
allocating twice. Never infer rollback from a response timeout alone.

## Self-review

The reference supplies the atomic boundary, both statements, the failure between them, an
alternative, and acknowledgment recovery. Remaining work for a production implementation is
to test key-claim races, all error paths, pool cleanup, and quota release on deletion. Measure
lock wait duration and rejected reservations under representative contention. No latency or
throughput target is asserted without measurements.

Sources: [3.4. Transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html),
[UPDATE](https://www.postgresql.org/docs/18/sql-update.html). Checked 2026-09-23.
