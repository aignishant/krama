# Reference design — Add optional expiry metadata to a read response

Author-written answer to [the assignment](README.md#assignment). Compare with your own
[DESIGN.md](DESIGN.md). The payloads and rollout are hypothetical; no endpoint was invoked.

## Assumptions and compatibility promise

The existing read endpoint GET /v1/links/L42 returns id and short_url. Its documented redirect
behavior already permits links to expire. This change exposes that metadata; it does not make
previously permanent links expire. Day 16's create request still requires expires_at.

Assume supported old clients ignore unknown response fields. This assumption is a release
gate to verify against real decoders, not a consequence of the field being called optional.
Keep id and short_url required with their existing types and meanings. New clients must work
with old servers during staggered rollout or rollback.

## Before, after, and field semantics

Old response:

```json
{"id":"L42","short_url":"https://s.example/c42"}
```

**Line by line:** Both original fields are present; omission of expires_at says nothing new
about lifetime. New clients show expiry information unavailable for this representation.

New response for an expiring link:

```json
{"id":"L42","short_url":"https://s.example/c42","expires_at":"2026-09-23T00:00:00Z"}
```

**Line by line:** Existing fields retain their values. The added field carries a UTC timestamp
in the service's established timestamp format. It is metadata, not permission to bypass the
server's expiry or revocation checks.

| Field state | Meaning for a new client | Behavior of a supported old client |
| --- | --- | --- |
| Absent | Expiry information unavailable; do not infer permanent | Existing behavior |
| Explicit null | No scheduled expiry, for supported legacy permanent records | Ignore unknown field |
| Valid timestamp | Scheduled expiry; may display it to the user | Ignore unknown field |

For links created by Day 16's required-expiry API, the new server emits a timestamp. Null is
only for records whose existing domain policy permits no scheduled expiry. New readers reject
or report a malformed present field as a contract error; they do not reinterpret it as null.
Clients may show a countdown, but server time determines expiry and deletion may invalidate a
link earlier. A nullable field does not guarantee a link will remain accessible forever.

## Deployment and rollback matrix

| Client | Old server | New server |
| --- | --- | --- |
| Old tolerant client | Existing read succeeds | Read succeeds; additional field ignored |
| Old strict decoder | Existing read succeeds | Fails without migration or separate representation |
| New client | Read succeeds; expiry unavailable | Reads all three defined presence states |

First run representative released decoders against old and new fixtures. Deploy new clients
that accept absent metadata. Then canary server emission and monitor decoding errors, not only
server HTTP success. Expand only when supported client behavior is verified. Keep an emission
switch so rollback returns the old representation without deleting expiry data or changing
actual redirect behavior. Shared caches must not mix separately versioned representations.

## Concrete failure and response

A legacy decoder checks that the response has exactly two keys. The server sends three and
the client raises an unknown-field error after receiving HTTP 200. The local model in
[CONCEPTS.md](CONCEPTS.md) reproduces this failure. A server success-rate metric alone misses it.
Stop the canary and disable the new field for this representation. Upgrade that decoder before
re-enabling the change, or expose the new metadata through a versioned representation while
preserving the old response for clients that cannot upgrade.

Separately, making an old permanently valid link expire would violate semantics even if every
decoder accepted the new key. Such a policy change requires an explicit product migration and
communication; it is outside this additive metadata task.

## Decision, alternative, and self-review

Choose additive metadata on v1 only after tolerant-reader evidence. It keeps the interface
small and supports gradual rollout. A separate v2 read representation is justified for strict
uncontrolled clients, at the cost of maintaining both contracts. Do not remove or rename the
old fields in the same change.

The assignment is answered with old/new payloads, three presence meanings, old-client behavior,
and rollback. Proposed checks include malformed timestamps, absent/null differences, new client
against old server, strict-client canary failure, and unchanged expiry enforcement. Only the
local decoder example was executed. Actual client inventory and compatibility tests remain
requirements for an implementation, not claimed results.

Source: [AIP-180 — Backwards compatibility](https://google.aip.dev/180), checked 2026-09-22.
It supports checking wire and semantic compatibility separately; this service's nullable
expiry policy is an authored example.
