---
day: 9
part: "1.1"
title: "Make each route's effect and cache policy explicit"
ids: [SD-09]
level: working
prerequisites: ["Request journey", "Functional scope"]
failure: true
---

# Make each route's effect and cache policy explicit

Core: create and redirect semantics, response fields, and explicit caching. Conditional requests
and detailed cache directives are optional depth. Keep one design deliverable within 30 minutes.

## One-line answer

Choose a method for the operation's intended effect, then specify its response and caching policy separately.

## The story

A shop shares a short link to a product. Previewing that link should open a destination, not create
another saved link. Later, changing the destination should not leave customers following an old
redirect cached indefinitely by their browser.

## The idea in plain language

The [request journey](../../day-008-first-repeated-value/sd_request-journey/CONCEPTS.md) gets a
message to a service; the API contract defines what that message means. A safe operation does
not request a state change. An idempotent operation has the same intended effect when repeated.
The properties are different, and neither promises identical responses or zero logging.

Recognize a method-design problem when a route mixes retrieval with creation, or when retry and
cache behavior are left to accident. Name the resource and the effect before choosing a verb.
Response status, headers, and body together describe the result. A cache policy is a separate
freshness decision; a method or redirect status alone does not express all product requirements.

## Why Krama needs it

[Idempotency semantics](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md) handles
the uncertain result of retrying a create. Today's contract must first distinguish that write
from an ordinary redirect lookup.

## The source behind it

[HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-9) (`RFC 9110`, 2022) defines
method properties and status semantics. [HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html#section-5.2)
(`RFC 9111`, 2022) defines cache directives. Checked 2026-09-22. The product policy below is our
design choice, not a claim that HTTP mandates this short-link API.

## The mechanism

### Worked trace

Assume editable short links whose latest stored destination must be used on each redirect.

| Step | Request or response | Meaning in this design |
| --- | --- | --- |
| Create | POST /links with destination URL | Ask the service to allocate and save one code |
| Acknowledge | 201, Location: /links/q7, body with short URL | Identify the new resource |
| Open | GET /q7 | Read the saved destination |
| Redirect | 302, Location: destination, Cache-Control: no-store | Let the browser navigate without storing this response |
| Open unknown code | 404, Cache-Control: no-store | Do not retain a miss that may later change |

The source of truth is the stored code-to-destination mapping. Creation must commit before
success is acknowledged. Redirect performs a lookup and returns a Location header; fetching the
destination is a separate browser request outside this service's latency boundary.

The method contract allows intermediaries and clients to distinguish reads from writes. Putting
creation behind GET makes a preview or automated fetch able to change application state. Returning
302 does not by itself establish the desired freshness policy; this design explicitly forbids
storage. `no-cache` instead permits storage with validation before reuse. A stable-link product
could choose a bounded cache lifetime to reduce reads, accepting staleness during that interval.

## When it breaks

This local model exposes the mismatch between mutable destinations and unconditional cached
redirects. It is a synthetic policy check, not an observed browser exchange.

```python
stored = {"q7": "https://example.org/old"}
cached = dict(stored)
stored["q7"] = "https://example.org/new"
print("cached destination:", cached["q7"])
print("authoritative destination:", stored["q7"])
try:
    assert cached["q7"] == stored["q7"], "cached redirect violates immediate freshness"
except AssertionError as error:
    print(f"AssertionError: {error}")
response = {"Location": stored["q7"], "Cache-Control": "no-store"}
assert response["Location"] == "https://example.org/new"
print("chosen policy:", response["Cache-Control"])
```

**Line by line:** the copied dictionary represents a previously saved redirect. Updating the
authoritative mapping leaves that copy stale. The assertion tests the stated freshness promise.
The repaired response expresses the chosen policy; this does not retroactively purge previously
cached responses, and it does not test a real HTTP cache implementation.

Author verification on Python 3.12.10, 2026-09-22:

```text
cached destination: https://example.org/old
authoritative destination: https://example.org/new
AssertionError: cached redirect violates immediate freshness
chosen policy: no-store
```

## In production

Validate destination schemes, authorize creation, and handle unknown or disabled codes explicitly.
Untrusted destinations can support abuse; the API needs a policy and operational ownership.
Redirect caching saves origin work but delays visible changes; disabling it increases lookup load.
A reviewer should ask which headers survive the proxy and whether old cache policies require a
migration strategy. Keep destination-page latency separate from redirect-service latency.

## Check yourself

### Readiness before practice

1. Why must a preview of the short URL not create a new mapping?
2. Which response field tells the browser where to go?
3. How do no-store and no-cache differ for this design?
4. What changes if links become immutable and cacheable for an hour?

Run the model and explain the freshness tradeoff aloud. Read [the complete reference](REFERENCE_DESIGN.md)
for guidance or compare after your own [DESIGN.md](DESIGN.md) attempt. Reading does not mark completion.

[Navigation](README.md) · [Recall](../../../docs/SD_RECALL.md#day-009-http-methods)
