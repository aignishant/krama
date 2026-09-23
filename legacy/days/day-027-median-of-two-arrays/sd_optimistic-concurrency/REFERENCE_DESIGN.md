# Reference design: Optimistic concurrency

Read before guided practice or compare after your independent attempt.

The scenario below is hypothetical. No PostgreSQL deployment or load test was run.
Your personal work belongs in [DESIGN.md](DESIGN.md); start with [CONCEPTS.md](CONCEPTS.md).

## Assumptions and contract

Each link has id, owner_id, destination_url, and a positive BIGINT version. All edits to the
protected representation increment version. Identifiers are not reused in this example;
otherwise include a generation identifier in the token. Authenticated clients may edit only
their own links. Conflicts are expected to be uncommon; this is an assumption to measure.

Select an HTTP precondition contract: GET returns the representation and a strong ETag such
as "link-42-v8". PUT sends the desired replacement and If-Match with that exact ETag. A missing
required token is rejected according to the API's documented precondition-required policy.
The service validates and decodes the token rather than trusting an arbitrary version supplied
for another resource. A successful update returns the new ETag.

## Atomic artifact

```sql
UPDATE links
SET destination_url = :destination_url, version = version + 1
WHERE id = :link_id
  AND owner_id = :authenticated_owner
  AND version = :expected_version
RETURNING id, destination_url, version;
```

**Line by line:** SET changes content and token together. The identity and owner predicates
enforce resource scope. The version predicate tests the state the editor actually read.
RETURNING supplies the saved representation only when a row changed. Colon names denote
driver-bound parameters; this is a statement template, not a measured query plan.

| Event | Stored destination/version | Visible result |
| --- | --- | --- |
| A and B read | old / 8 | both retain ETag for 8 |
| A saves alpha with expected 8 | alpha / 9 | success, ETag for 9 |
| B saves beta with expected 8 | alpha / 9 | zero rows; stale precondition |
| B fetches fresh state | alpha / 9 | show conflict and current content |
| B deliberately resolves and saves against 9 | chosen value / 10 | success only if 9 is still current |

After zero rows, an owner-scoped existence check may distinguish a missing resource (404)
from an existing resource with a stale condition (412). If concurrent deletion occurs during
diagnosis, either documented outcome is acceptable for that changed state; neither authorizes
the failed write. A resource owned by someone else is treated as absent to avoid disclosure.

## Decision and alternative

Use optimistic concurrency so that no database lock spans the human editing interval. A
pessimistic row lock is useful for a short server-side critical section but unsuitable for
an unbounded open browser form. Last-write-wins is simpler and would be appropriate only if
overwriting intervening edits were an accepted product requirement. It is rejected here.

## Client retry decision and failure walkthrough

B must not fetch version 9 and automatically attach it to the unchanged stale form: that
would knowingly overwrite A. Instead show the conflict, fetch current data, and ask the user
to reconcile, or apply a proven domain-specific merge. Submit the resulting intent with the
fresh token, and handle another conflict if someone else edits again.

If A's success response is lost, repeating If-Match version 8 will fail after the first commit.
A should read current state and compare with its intent; if attribution matters, an operation
identifier and stored result can establish whether this particular request committed. Version
checking prevents stale writes but is not a general idempotency ledger.

## Self-review

The design includes the version field, one atomic comparison/write, a failed comparison result,
client action, authorization, and an alternative. Verify every writer changes version, test
two edits from the same token with real database sessions, and test response loss separately.
Track conflict rates before choosing merge automation. No concurrency tests or service latency
measurements have been claimed for this reference.

Sources: [UPDATE](https://www.postgresql.org/docs/18/sql-update.html) and
[HTTP Semantics, RFC 9110 §13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1),
checked 2026-09-23. The latter supports the chosen If-Match/412 contract.
