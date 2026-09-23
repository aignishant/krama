---
day: 25
part: "2.1"
title: "Transactions"
ids: [SD-25]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Transactions

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Put all database changes that must succeed together inside one transaction, then distinguish commit from receipt of the response.

## The story

A link appears in a dashboard, but a crash prevented the owner quota from being charged. The next request now sees spare capacity that should no longer exist.

## The idea in plain language

Start with [schema constraints](../../day-022-lower-bound/sd_schema-constraints/CONCEPTS.md).
An invariant is a rule that must remain true for valid committed state. Here each created link
must consume one quota unit. A transaction groups statements into one commit or one rollback.
Atomicity means partial effects are not committed. Isolation addresses concurrent operations;
it is a separate question, developed on Day 26. A database transaction cannot automatically
undo an email or an external HTTP request.

## Why Krama needs it

This develops SD-25 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

Read the [complete reference answer](REFERENCE_DESIGN.md) within the concept/critique
window; keep your own practice in [DESIGN.md](DESIGN.md).

## The source behind it

[3.4. Transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html) supports commit/rollback semantics. The SQLite block is explicitly a local rollback demonstration.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Assume one relational database contains owners and links, and used counts live links.
Initially owner 7 has used=2, limit=3, and two links. A successful creation moves both counters
of reality together: (used=2, links=2) -> (used=3, links=3).

| Stage | Transaction's tentative state | Committed outcome on failure |
| --- | --- | --- |
| Begin | (2,2) | (2,2) |
| Reserve quota | (3,2) | rollback -> (2,2) |
| Insert link | (3,3) | rollback -> (2,2) |
| Commit | both changes committed | (3,3), even if reply is lost |

Reserve quota with one conditional update, checking used < quota_limit in the statement that
increments used. Continue only if one owner row was updated. Insert the link using that same
connection and transaction. Commit only after both statements succeed. An insertion error,
including a unique-code conflict, must roll back the reservation as well.

The proof has a clear boundary: before commit the new operation has no committed partial state;
after commit both changes exist. Every writer, including deletion paths, must preserve the same
accounting rule. A CHECK constraint can bound the counter but cannot by itself establish a
cross-table count equality. The [reference](REFERENCE_DESIGN.md) supplies the full request trace.

The tradeoff is holding transactional resources while statements execute. Keep the transaction
short and avoid external waits inside it. A response timeout after COMMIT creates uncertainty
for the client; it is not evidence of rollback. Resolve repeated requests using an operation
key recorded atomically with the mutation, building on Day 10 idempotency.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE quota (used INTEGER)")
db.execute("INSERT INTO quota VALUES (2)")
db.execute("CREATE TABLE links (code TEXT UNIQUE)")
db.commit()
try:
    db.execute("BEGIN")
    db.execute("UPDATE quota SET used = used + 1")
    raise RuntimeError("crash between statements")
except RuntimeError as exc:
    db.rollback()
    print(type(exc).__name__ + ": " + str(exc))
state = (db.execute("SELECT used FROM quota").fetchone()[0],
         db.execute("SELECT COUNT(*) FROM links").fetchone()[0])
print("after rollback:", state)
assert state == (2, 0)
db.close()
```

**Line by line:** This isolated SQLite transaction checks rollback only; its empty links table deliberately avoids claiming cross-table quota equality. The injected exception occurs after the update but before insertion. rollback removes the tentative update. Reads and the assertion verify the two observed values; no PostgreSQL concurrency claim follows from this test.

Observed author output on Python 3.12.10, 2026-09-23:

```text
RuntimeError: crash between statements
after rollback: (2, 0)
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

For a pooled connection, verify that all statements use the same checked-out connection and
that errors do not return it to the pool with a transaction still open. A reviewer should ask
where the commit acknowledgment can be lost. Track rollback and contention rates separately
from business rejections. Optional depth: durable deduplication and an outbox for external
effects; adding a network call inside the transaction does not make that effect transactional.

## Check yourself

### Readiness before practice

1. What survives a failure before the insert? What survives after commit but before reply?
2. Why does a counter CHECK alone not prove link-count equality?
3. Which operation must be conditional to avoid allocating an exhausted quota?
4. Why does a timeout not justify blindly repeating a create?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
