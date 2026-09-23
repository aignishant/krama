---
day: 27
part: "2.1"
title: "Optimistic concurrency"
ids: [SD-27]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Optimistic concurrency

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Apply an edit only if the stored version still matches the version the editor read, and let the client resolve conflicts deliberately.

## The story

Two people open the same destination URL. One corrects it and saves; the other later saves an old form and silently restores stale content.

## The idea in plain language

Start with [isolation anomalies](../../day-026-minimum-shipping-capacity/sd_isolation-anomalies/CONCEPTS.md).
Optimistic concurrency assumes conflicts are uncommon enough to detect at save time rather
than hold a lock while a human edits. A version is a changing token identifying the state that
was read. Compare-and-swap means the comparison and replacement happen together at one storage
boundary. Comparing in application code and updating later recreates the original race.

## Why Krama needs it

This develops SD-27 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

Read the [complete reference answer](REFERENCE_DESIGN.md) within the concept/critique
window; keep your own practice in [DESIGN.md](DESIGN.md).

## The source behind it

[UPDATE](https://www.postgresql.org/docs/18/sql-update.html) documents conditional updates and RETURNING; [HTTP Semantics, RFC 9110 §13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1) defines If-Match.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

A link starts with version=8 and destination="old". Both clients read version 8. Client A
requests destination="alpha" only if version remains 8. A single conditional update writes
the destination and increments version to 9. Client B's update, also requiring 8, now affects
zero rows; it must not report a successful save.

| Client event | Stored version | Outcome |
| --- | --- | --- |
| A reads, B reads | 8 | both retain expected=8 |
| A conditional save | 9 | one row changed |
| B conditional save | 9 | zero rows changed; conflict |
| B fetches current content | 9 | compare or ask user to merge |
| B deliberately resubmits against 9 | 10 if still current | recheck, do not bypass condition |

Use a WHERE clause combining identity, owner authorization, and expected version. Increment
version in that same UPDATE and return the new version. A successful row count provides a
certificate that the comparison and write happened together. A zero row count can mean stale
version, absent link, or ownership mismatch; define a non-leaking API policy for distinguishing
those cases. Do not expose another owner's record through a diagnostic follow-up read.

For an HTTP API, a strong ETag can represent the version and If-Match can carry the condition.
A failed precondition is 412 when using that contract. An explicit version field API may use
a documented 409 conflict response instead. Do not conflate these two contracts. The complete
[reference](REFERENCE_DESIGN.md) selects one and explains the client behavior.

Cost: one conditional indexed update for the row, plus a fresh read after conflict. The version
column adds storage and write work. Low contention avoids long-held edit locks; high contention
causes repeated conflicts. Blindly rereading a new token and resending the old full payload
defeats the purpose: it authorizes overwriting intervening work without reconciliation.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
record = {"destination": "old", "version": 8}

def conditional_edit(expected, destination):
    # A sequential model of a single storage operation, not a thread-safe function.
    if record["version"] != expected:
        return False
    record.update(destination=destination, version=expected + 1)
    return True

assert conditional_edit(8, "alpha")
second = conditional_edit(8, "beta")
print("stale edit accepted:", second, "record:", record)
assert not second and record["destination"] == "alpha"
record["destination"] = "beta"  # Remove the guard to expose the lost edit.
print("unguarded overwrite:", record["destination"])
assert record["destination"] != "alpha"
```

**Line by line:** The first guarded edit advances the token. The second retains the stale expected token and is rejected. Removing the guard in the final assignment exposes the lost edit. This deterministic model illustrates a protocol; a real implementation needs the database to make the guarded update atomic.

Observed author output on Python 3.12.10, 2026-09-23:

```text
stale edit accepted: False record: {'destination': 'alpha', 'version': 9}
unguarded overwrite: beta
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

Every mutation of protected content must change the token, including admin jobs. Do not reset
versions after a delete/recreate if old clients could mistake the new resource for the old one;
use a generation identity where required. A lost response remains an uncertain outcome even
with versioning: fetch current state or use a durable operation identifier. Optional depth:
merge independent fields when the domain can prove that doing so preserves intent.

## Check yourself

### Readiness before practice

1. Why must comparison and write be in one database statement?
2. When does zero affected rows mean something other than a stale edit?
3. Why is reread-and-blind-overwrite an unsafe conflict policy?
4. What should a client do if the successful edit's response is lost?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
