---
day: 8
part: "2.1"
title: "Separate finding a host, securing a connection, and making a request"
ids: [SD-08]
level: working
prerequisites: ["Single-node baseline", "Latency boundaries"]
failure: true
---

# Separate finding a host, securing a connection, and making a request

Core: trace a cold HTTPS navigation over TCP through the redirect and destination request.
Connection reuse is the main comparison; HTTP/3 and TLS resumption are optional later depth.

## One-line answer

A browser must reach the right endpoint, establish the required secure channel, and exchange HTTP messages before following a redirect.

## The story

To collect a parcel, you find the counter's address, travel there, check that it is the right
counter, then ask for your parcel. A sign sending you to another branch begins another journey;
it does not mean the parcel has already arrived in your hands.

## The idea in plain language

DNS resolves a host name to records used to find an endpoint; it does not resolve the URL's
path into a database row. TCP establishes a reliable ordered byte-stream connection. TLS
authenticates the server and protects communication. HTTP carries the application request
and response. Each layer answers a different question and can fail before the next begins.

Recognize this model when the app reports fast requests but the browser is slow, or when a
browser failure never appears in application logs. State your protocol assumptions: this lesson
uses a fresh TCP connection and TLS 1.3 without early data. It is not every browser's exact trace.

## Why Krama needs it

[HTTP methods](../../day-009-frequency-ranking/sd_http-methods/README.md) describes what the
request means, and later connection/deadline lessons budget the resources and time it consumes.
The [single-node baseline](../../day-006-best-single-trade/sd_single-node-baseline/CONCEPTS.md)
still owns the mapping; this lesson expands its browser arrow.

## The source behind it

Checked 2026-09-22: [RFC 1034 — DOMAIN NAMES - CONCEPTS AND FACILITIES](https://www.rfc-editor.org/rfc/rfc1034.html)
for name resolution; [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html)
for connection establishment; [RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
for the secure handshake; and [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
for the redirect response. The timings below are an original synthetic model, not protocol guarantees.

## The mechanism

### Worked trace

Assume `https://short.example/a7` maps to `https://destination.example/page`. No usable DNS
cache or existing connection is available to either host. Ignore proxies and additional page assets.

```text
Browser -> resolver: address records for short.example
Resolver -> Browser: usable address (resolve/cache upstream as needed)
Browser <-> shortener: TCP SYN, SYN-ACK, ACK
Browser <-> shortener: TLS handshake, certificate verification, traffic keys
Browser -> shortener: GET /a7 with the shortener authority
Shortener -> database -> shortener: lookup a7
Shortener -> Browser: 302, Location: https://destination.example/page
Browser -> destination: resolve/connect/secure as needed, then GET /page
Destination -> Browser: page response
```

Name lookup concerns `short.example`; `/a7` is sent in the application request. On an ordinary
full TLS handshake, the client verifies the server certificate and handshake before proceeding
with normal application data. A redirect is an instruction to the browser, not the shortener
fetching and returning the destination page. If the destination is a different origin, it may
need its own resolution and connection. A successful redirect and a successful destination load
are separate outcomes.

For one deliberately serial model, assume DNS 20 ms, TCP setup 40 ms, TLS setup 40 ms, request/
response network transit 40 ms, and shortener processing 10 ms. The modeled redirect arrival
is 150 ms. Processing includes the database wait; adding it again would double count.
Do not sum these as percentiles or infer real performance from them. On a usable warm connection,
the first three setup costs can disappear from this particular request, giving 50 ms under
the same remaining assumptions. Caches, concurrent connection attempts, and packet loss can
change both paths. The destination journey is additional work outside the redirect boundary.

Why the trace is useful: every event has a prerequisite. Failed name resolution prevents
connecting to the selected host; failed server authentication prevents an authenticated HTTP
exchange; a database miss is only possible after the shortener received a valid request.
Putting these failures in order identifies the owner who can observe and fix each one.

## When it breaks

```python
cold_ms = {"dns": 20, "tcp": 40, "tls": 40, "http_transit": 40, "app": 10}
app_only = cold_ms["app"]
redirect_arrival = sum(cold_ms.values())
print(f"app-only={app_only} ms; modeled redirect arrival={redirect_arrival} ms")
try:
    assert app_only == redirect_arrival, "the browser boundary includes setup and transit"
except AssertionError as error:
    print(f"AssertionError: {error}")
warm_ms = cold_ms["http_transit"] + cold_ms["app"]
assert redirect_arrival == 150 and warm_ms == 50
print(f"modeled warm request={warm_ms} ms; destination load excluded")
```

**Line by line:** named entries define nonoverlapping synthetic stages. The sum belongs to
one modeled cold request, while app-only timing uses a narrower boundary. The failed equality
exposes that mismatch. The warm calculation omits setup only under the stated reuse assumption.
This is a calculation test, not an observed DNS, TLS, or browser trace.

Author verification on Python 3.12.10, 2026-09-22:

```text
app-only=10 ms; modeled redirect arrival=150 ms
AssertionError: the browser boundary includes setup and transit
modeled warm request=50 ms; destination load excluded
```

## In production

Measure client timings alongside server spans and label cold versus reused connections.
Browser-visible DNS/TLS failures may occur before an HTTP status exists. Do not turn a
certificate verification failure into a reason to disable verification; repair the endpoint's
identity or certificate configuration. A missing code can produce an application response,
whereas a timeout may leave the browser without one.

Connection reuse reduces repeated setup but retains resources and can fail on stale connections.
Adding redirects adds dependencies and possible loops. Optional protocol boundary: HTTP/3 uses
QUIC rather than the TCP sequence shown here; TLS resumption and early data also change details.
Neither is required to explain today's explicitly scoped journey.

## Check yourself

### Readiness before practice

1. Which host and path are used before and after the redirect?
2. Why can a TLS failure be absent from the app's HTTP logs?
3. Which stages can reuse skip, and under what assumptions?
4. Where does a redirect latency target end compared with a page-load target?

Run the calculation, then draw your own journey in [DESIGN.md](DESIGN.md), following
[the assignment](README.md#assignment). Use the [complete reference](REFERENCE_DESIGN.md)
before a guided attempt or afterwards for comparison. Explain a failure at a named stage.
Reading and practice share the existing 30-minute budget.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-008-request-journey)
