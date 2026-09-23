# Reference design — Create an expiring link

Author-written response to the [request/response/error assignment](README.md#assignment).
Use before guided practice or after an independent attempt. [DESIGN.md](DESIGN.md) stays yours.
The examples below specify a hypothetical service; no live endpoint was invoked.

## Assumptions and validation

Authenticated owners create links with a required destination_url and required expires_at.
The endpoint is `POST /v1/links`. Owner identity comes from authentication, not request JSON.
Server time is authoritative. Chosen limits: 8 KiB request body, a destination string of at
most 2,048 characters, and an expiry strictly after validation time and no more than 30 days
after it. One KiB is 1,024 bytes; the maximum body is 8,192 bytes. Thirty days means 30×24 hours.
These limits bound processing and scope the product; they are not HTTP-mandated constants.

Require a JSON object with exactly the two named fields and reject wrong types or unknown
fields. Accept absolute http or https destinations with a hostname and no embedded credentials
or control characters; reject relative URLs and other schemes. Do not fetch the destination.
Require an RFC 3339 timestamp with an explicit offset, normalize it to UTC, and support at
most microsecond precision with no leap-second input in this contract. Documenting this subset
avoids relying on whatever forms one parser happens to accept. Recheck future expiry at commit.

## Request and successful response

Assume validation/commit happens at 2026-09-22T12:00:00Z. The example expiry is 30 minutes later.

```http
POST /v1/links HTTP/1.1
Content-Type: application/json
Authorization: Bearer <access-token>
Idempotency-Key: create-demo-001

{"destination_url":"https://example.org/guide","expires_at":"2026-09-22T12:30:00Z"}
```

**Line by line:** POST requests a new resource. JSON is the required media type. The token
identifies the owner; it is illustrative, not a credential. The required idempotency key
identifies this logical create operation. The two JSON fields satisfy the declared shape.

```http
HTTP/1.1 201 Created
Location: /v1/links/L42
Content-Type: application/json
Cache-Control: no-store

{"id":"L42","short_url":"https://s.example/c42","destination_url":"https://example.org/guide","created_at":"2026-09-22T12:00:00Z","expires_at":"2026-09-22T12:30:00Z"}
```

**Line by line:** 201 follows durable creation. Location identifies the API resource; short_url
is the separate redirect address. JSON exposes server-assigned identity and normalized timestamps.
The hypothetical L42/c42 identifiers stand in for allocated unique values. no-store prevents
response storage by conforming caches; it is not an authorization mechanism.

## Error contract

All service-generated errors return JSON with `error.code`, a readable `error.message`, an
optional `error.field`, and `request_id`. Clients branch on code, not message wording.
Errors never include credentials or claim that a transport timeout means no link was created.

| Status | Stable code | Condition | Client response |
| --- | --- | --- | --- |
| 400 | invalid_json | Malformed JSON | Repair encoding |
| 400 | invalid_request | Missing/unknown fields, wrong types, invalid key shape | Repair request |
| 401 | unauthenticated | Missing or invalid credentials | Authenticate; include WWW-Authenticate: Bearer |
| 403 | owner_disabled | Valid identity lacks create permission | Resolve account permission |
| 413 | body_too_large | More than 8,192 bytes | Reduce body |
| 415 | unsupported_media_type | Content type is not application/json | Correct media type |
| 422 | invalid_destination | Destination violates URL rules | Correct destination_url |
| 422 | invalid_expiry | Missing offset, unsupported precision, past/equal or too distant | Correct expires_at |
| 409 | idempotency_conflict | Same owner/key with different request | Restore original request or use a new operation |
| 503 | temporarily_unavailable | Required storage unavailable or bounded allocation exhausted | Retry with the same key within its retention window |

Example validation error:

```json
{"error":{"code":"invalid_expiry","field":"expires_at","message":"Expiry must be after server time and within 30 days."},"request_id":"req-demo-2"}
```

**Line by line:** code is stable, field points to the rejected input, message explains the
policy, and request_id supports correlation. This is a designed payload, not observed output.
No link or successful replay record is created for this validation rejection.

Process bounded transport/media checks, authentication, JSON shape, then structural field validation.
Normalize the request and resolve matching replays before applying current-time expiry checks
for a new operation; an old successful response is not a new create.
Within field validation report destination errors before expiry errors for deterministic behavior.
Authenticate before exposing owner-specific replay information. Transport failures outside the
service may have no JSON response, which the caller must handle as an unknown outcome.

## Retry semantics and failure walkthrough

Choose owner-scoped idempotency keys of 1–128 ASCII letters, digits, hyphens, or underscores.
Retain a completed replay record for 24 hours from commit, atomically with the created link.
That chosen window bounds storage and supported retries; it is separate from link expiry.
Compare the canonical request: destination string unchanged and expiry normalized to UTC.
A matching replay returns the original status, Location, and payload without creating a link.
A conflicting payload returns 409. Resolve matching replays before rechecking future expiry,
so a delayed retry can still recover the original result even after the link has expired.

Two concurrent requests with the same owner/key must serialize through an atomic uniqueness
decision; a loser reads the winner's completed record. If waiting exceeds its deadline, it
returns an unavailable/unknown outcome and the client keeps the same key. A crash after the
transaction commits but before sending 201 leaves one link and one replay record. The retry
recovers that result. After the retention window, the server cannot promise deduplication;
clients must not blindly replay an uncertain old create. At redirect time now >= expires_at
rejects the link regardless of whether a stored create response can still be replayed.

## Alternative and self-review

A simpler POST without idempotency support is defensible if clients accept possible duplicates
or do not retry uncertain creates. This reference pays for a replay store to provide bounded
retry safety. A client-selected resource ID with PUT is another possible contract, but changes
who allocates identity and requires its own conflict rules.

The answer includes valid input, committed success, error shapes, validation, auth ownership,
and a failure trace. Boundary checks to execute in an implementation: expiry equal to now,
just after now, exactly 30 days, above 30 days, a timezone-free string, a duplicate key race,
and replay after link expiry. Only the local time-comparison demo in [CONCEPTS.md](CONCEPTS.md)
has been run. URL parsing, database transactions, HTTP responses, and availability are designs,
not measured tests. Full service implementation is outside the 30-minute assignment.

Sources: [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) and
[Date and Time on the Internet: Timestamps, RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html),
checked 2026-09-22. Limits and retry retention are authored policy choices.
