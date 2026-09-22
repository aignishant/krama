# Reference design — Idempotency semantics

Author-written response to the same-create/two-retries assignment. [DESIGN.md](DESIGN.md) remains
your practice file. This is a proposed single-database design, not an implemented crash test.

## Assumptions and requirement

Continue [Day 9's create API](../../day-009-frequency-ranking/sd_http-methods/REFERENCE_DESIGN.md).
The authenticated client generates an unpredictable request token before submitting a logical
create and persists it across retries. Our API accepts it as an application-defined
`Idempotency-Key` header. Scope is `(owner_id, operation, token)`; operation is `create-link`.
Require the key for this route. Different legitimate creates get different tokens.

Assume a maximum supported retry window of 24 hours, chosen for this exercise rather than measured
from client behavior. Retain completed records for at least that window from commit. Clients must
not blindly retry old operations after the window; reconcile by saved resource ID where possible.

## Data and transaction artifact

The authoritative database stores a unique scoped key, normalized effect-changing fields
(`destination_url`, explicit expiry after applying defaults), resulting resource ID, response
status/body/Location, and commit time. Compare normalized values exactly; a digest alone needs
an explicit collision policy. Request IDs and tracing timestamps are not effect-changing fields.

Within one short transaction, claim the unique key, insert the link, store the completed response,
and commit. A losing concurrent attempt waits only within its deadline, then reads the committed
record or returns a declared in-progress error. Our choice is 409 with a distinct `in_progress`
error code and retry guidance; a changed payload uses 409 `key_conflict` and must not be retried
unchanged. These codes are explicit application choices. Rollback removes uncommitted work.

## Original attempt and two retries

| Attempt | Key and payload | Server outcome | Client observation |
| --- | --- | --- | --- |
| Original | owner-7/create-link/k1, destination A | Commit link q7 and saved 201 result together | Response lost; timeout |
| Retry 1 | Same scope, key, destination A | Find matching completed record, return saved 201 and q7 | Response lost again in this hypothetical trace |
| Retry 2 | Same scope, key, destination A | Replay the same result without another insert | Client receives q7 |

There is one committed mapping. The status/body/Location are replayed; transport-level Date and
per-attempt trace IDs need not be identical. A later request using k1 with destination B returns
`key_conflict` and creates nothing. A new intended create for B uses a new key. Repeat authorization
before disclosing any stored result. Use the create route's no-store response policy.

## Decision and alternative

Choose durable keyed POST because the server allocates resource IDs while the client owns retry
identity. The additional table and retention cleanup are the cost. A client-chosen resource ID
with a suitable PUT contract could simplify identity, but it moves naming and replacement semantics
into the API. I would choose it if clients should own stable resource names and overwrite behavior
can be defined safely. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
provides the method concept; it does not provide our storage protocol.

## Failure walkthrough

Crash before commit: neither link nor replay result persists; the retry may execute the operation.
Crash after commit but before response: both persist; the retry replays. A crash between separately
committed link and record writes would violate the design, which is why both share a transaction.
If a claim is locked, bounded waiting avoids an indefinitely stalled caller. Database transaction
recovery, not an in-memory flag, determines whether that claim survived.

At expiry, removing the key removes the duplicate barrier for future attempts. Remote side effects
are excluded from this atomicity claim. Adding them requires a downstream identity/reconciliation
design and explicit treatment of uncertain outcomes.

## Self-review

The client key, replay eligibility, conflict behavior, original attempt, and two retries are explicit.
The invariant is at most one committed local create per retained scoped key. Next validation should
race matching requests, race different payloads, kill the process around commit, and test expiry.
Measure real client retry ages before adopting 24 hours. The sequential concept demo checks only
branch behavior; it is not evidence that this transaction design has been implemented.

[Concepts](CONCEPTS.md) · [Acceptance](README.md#acceptance-check) · [Personal practice](DESIGN.md)
