# Reference design — HTTP methods

This is an author-written answer to the create/redirect assignment. Keep personal work in
[DESIGN.md](DESIGN.md). Read after [the concepts](CONCEPTS.md), either before guided practice or
after an independent attempt. All behavior below is proposed; no service was deployed.

## Assumptions and requirement

Authenticated owners create editable short links. Visitors can open a public short URL without
authentication. Each successful create stores one mapping; redirects use the latest committed
mapping. Destination content is outside scope. The database is authoritative. HTTPS is assumed.

## Route contract

| Route | Request fields | Success | Failure and caching policy |
| --- | --- | --- | --- |
| POST /links | Auth context; JSON `destination_url`, optional `expires_at` | 201; Location `/links/q7`; body contains `code`, `short_url`, `destination_url`, `expires_at` | 400 malformed body/invalid URL or expiry; 401 missing credentials; 403 forbidden caller; 503 temporary inability to serve. All responses use `Cache-Control: no-store`. |
| GET /q7 | Path code; no request body | 302; Location is the stored destination; empty response body is sufficient | 404 unknown, disabled, or expired code under this chosen concealment policy; 503 unavailable lookup. All responses use `Cache-Control: no-store`. |
| HEAD /q7 | Same path as GET | Same status and redirect headers as GET, no response content | Same lookup and cache policy |

The route supports HTTP(S) destinations with a host and rejects invalid types, disallowed schemes,
and past expiry times. Code collisions are retried internally under a uniqueness constraint before
returning success. Error bodies contain a stable error identifier and request ID, not stack traces.
Create status and redirect semantics follow [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html);
the exact validation rules and concealment policy are application choices.

## Request artifact

```text
Owner -> POST /links -> validate + authorize -> commit mapping q7 -> 201
Visitor -> GET /q7 -> read mapping q7 -> 302 + Location + no-store
Visitor -> destination host -> destination response (outside our service)
```

The 201 response's Location identifies the created resource. The 302 response's Location identifies
the navigation target. They have different roles even though both use the same header name.

## Decision and alternative

Choose POST for server-assigned creation and GET for retrieval. A temporary redirect with explicit
no-store matches editable links and avoids retained misses. The tradeoff is an origin lookup on
every visit. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html) supplies the cache directive
semantics; freshness requirements determine our policy.

For immutable mappings, a permanent redirect with an explicit bounded freshness lifetime could
reduce service traffic. I would adopt that only with a product agreement about delayed revocation
and measured read pressure. A permanent cached response is a poor default for immediate edits.

## Failure walkthrough

The database commits q7, but the create response is lost. The owner sees a timeout although the
mapping exists. Blindly repeating this POST may create another code. Method choice alone does not
solve that uncertainty; [Day 10's reference](../../day-010-pair-sum-indices/sd_idempotency-semantics/REFERENCE_DESIGN.md)
adds a durable retry identity. Do not report a timed-out creation as definitely unapplied.

If the redirect lookup fails, return the declared temporary error rather than invent a destination.
If an earlier deployment allowed caching, adding no-store today does not evict an already stored
redirect. A migration may need a new URL or waiting for old entries to expire.

## Self-review

The methods, request fields, response codes, headers, source of truth, and cache implications are
specified. Creation retries, abuse handling, and exact URL parsing limits still need implementation
work. Next I would test a committed-but-lost create, an expired code, and a destination edit through
the actual proxy/browser path. The dictionary check in the concept lesson establishes only the
staleness counterexample. It does not establish protocol conformance or production capacity.

[Assignment and acceptance](README.md#assignment) · [Personal practice](DESIGN.md)
