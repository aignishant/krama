# Reference design: Week 4 design review

Compare only after your cold attempt. This is an example revision, not your assessment evidence.

The scenario below is hypothetical. No PostgreSQL deployment or load test was run.
Your personal work belongs in [DESIGN.md](DESIGN.md); start with [CONCEPTS.md](CONCEPTS.md).

## Chosen weak decision and assumptions

This example reviews Day 27's edit contract. The initial memo proposed a version column but
checked it in application code before issuing an unconditional update. That leaves a gap
between check and write. The user-visible requirement is that a stale form cannot silently
overwrite a newer saved destination.

Assume one authoritative PostgreSQL links table, owner-scoped edits, stable link identity,
and low conflict frequency. The low-conflict assumption is not measured. The learner can
instead select another Days 22–27 decision; this is one complete sample revision.

## Before: the decision fails under this schedule

| Step | A | B | Stored state |
| --- | --- | --- | --- |
| 1 | read and approve version 8 | | old / 8 |
| 2 | | read and approve version 8 | old / 8 |
| 3 | save alpha | | alpha / 9 |
| 4 | | save beta unconditionally | beta / 10 |

B's check was true when performed but stale when acted on. An index on id makes each lookup
fast without closing this gap. Two individually atomic transactions can still implement this
bad protocol if the comparison is outside the guarded write.

## After: revised memo and artifact

Move the version predicate into the UPDATE itself. Include id and authenticated owner, set
the new destination, and increment version in that statement. Return the new version only
when one row changes. Use the [Day 27 statement](../../day-027-median-of-two-arrays/sd_optimistic-concurrency/REFERENCE_DESIGN.md#atomic-artifact)
as the complete artifact. The request path is:

client GET with ETag -> client prepares edit -> PUT with If-Match -> owner-scoped conditional
UPDATE -> one row: success/new ETag; zero rows: missing resource or failed precondition.

Replaying the same schedule now gives A success at version 9 and B no mutation. B fetches the
current representation and resolves intent before resubmitting. There is no lock while the
user thinks, and no blind refresh-and-overwrite loop.

## Defended alternative

A server could lock the row while checking and writing, which is reasonable for short atomic
server work. It cannot reasonably hold that lock for the entire human edit interval. Merely
locking at save time without comparing the old version would still allow stale intent to
overwrite a current value. Retain optimistic comparison; switch to a richer merge workflow
if measured conflict frequency and domain rules justify it. One version field and occasional
extra reads are the chosen storage and latency costs.

## Failure walkthrough

Before the update, a process failure changes nothing. After the guarded update but before
commit, rollback leaves the old state. After commit but before response, the new version is
durable but the client is uncertain. Replaying the old precondition cannot apply another
edit; fetch current state or resolve a stored operation record. A 412 conflict is not a signal
to retry the identical stale replacement with a freshly fetched token.

## Self-review and next evidence

Requirements: the stale-write prohibition is explicit. Data/API: the table owns truth and
the HTTP token maps to the stored version. Scale: one indexed conditional write per save,
with contention and conflict rates still to measure. Failure: precommit rollback and lost
acknowledgment have different outcomes. This is a sample self-review, not a learner score.

The next meaningful check uses two database clients that read version 8 before either writes;
assert one guarded save succeeds and one does not, and inspect the final destination. Add a
test for unauthorized identity and a separate test for a lost success response. Preserve the
original memo beside the revision in personal evidence. No such database test was run here.

Sources: [UPDATE](https://www.postgresql.org/docs/18/sql-update.html) and
[HTTP Semantics, RFC 9110 §13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1),
checked 2026-09-23. The scenario and evaluation are original review examples.
