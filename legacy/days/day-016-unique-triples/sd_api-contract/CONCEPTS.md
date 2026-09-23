---
day: 16
part: "2.1"
title: "Make link creation observable at the boundary"
ids: [SD-16]
level: working
prerequisites: ["Day 15 domain model", "HTTP methods and idempotency"]
failure: true
---

# Make link creation observable at the boundary

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Define accepted input, committed success, and distinguishable errors before implementing a create-link endpoint.

## The story

A client submits an expiry without a timezone and receives a generic failure. It cannot tell whether to fix the request or retry a link that may already have been created.

## The idea in plain language

An API contract describes what a caller can send and rely on receiving. Validation is part
of it: accepted types, required fields, limits, and time interpretation. A success response
should identify the created resource; an error should have a stable machine-readable reason.
Use the [domain model](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md) to identify
the link and derive ownership from authentication. HTTP method semantics alone do not prevent
duplicate creates after a lost response; review [Day 10](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md).
Recognize an incomplete contract when two reasonable clients would interpret the same field differently.

## Why Krama needs it

Later service-boundary and API sessions rely on a concrete operation whose validation, effects, and retries can be reasoned about independently.

## The source behind it

[HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), RFC 9110, sections 9 and 15, defines method and status semantics. The payload fields, validation limits, and retry policy here are authored choices. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Trace one request through four boundaries: decode JSON, validate authenticated input,
commit a new link, return its resource identity. Invalid input must produce no link. A successful
response follows commit; a transport failure after commit can leave the caller uncertain.
Separate those cases in the contract instead of presenting every failure as safe to retry.

For a hypothetical request received at 12:00 UTC, an expiry of 12:30 UTC is future; an expiry
of exactly 12:00 is invalid. State the clock used and compare normalized instants. At redirect
time use the complementary rule: now >= expires_at means expired. These boundaries agree and
avoid a link being simultaneously accepted as live and expired at equality.

Parsing and validation take work proportional to bounded input size; persistence latency and
availability dominate the real service. More detailed error types help callers repair input,
but every public type becomes part of a compatibility promise. The [reference answer](REFERENCE_DESIGN.md)
provides the complete wire examples, input limits, and retry decision for this assignment.

## When it breaks

```python
from datetime import datetime, timezone
now = datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc)
expiry = now
wrong = expiry >= now
correct = expiry > now
print("accept equality:", wrong, "strictly future:", correct)
try:
    assert wrong == correct, "expiry at creation time is already expired"
except AssertionError as error:
    print(f"AssertionError: {error}")
try:
    datetime(2026, 9, 22, 12, 30) > now
except TypeError as error:
    print(f"TypeError: {error}")
```

**Line by line:** The fixed aware timestamp makes the example reproducible. Equality exposes the acceptance-boundary bug. The second comparison shows the real error when a timezone-free datetime is compared with an aware one. These are local validation demonstrations, not HTTP server responses.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
accept equality: True strictly future: False
AssertionError: expiry at creation time is already expired
TypeError: can't compare offset-naive and offset-aware datetimes
```

## In production

Perform authoritative validation at the service boundary even if clients validate first. Do not fetch the destination merely to create a link; any future preview feature needs its own network access policy. Bound body size and choose deterministic error precedence. Make idempotency-key lifetime and concurrency handling explicit if retries are supported. Log request IDs and error codes without assuming payloads are safe to log.

## Check yourself

### Readiness before practice

1. Which clock decides whether expiry is future?
2. What should happen at exact expiry equality?
3. How does the caller distinguish a rejected request from an unknown commit outcome?
4. Why should owner_id come from authentication?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
