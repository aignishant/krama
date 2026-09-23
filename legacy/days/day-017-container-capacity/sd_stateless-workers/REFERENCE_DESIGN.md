# Reference design — A request survives worker replacement

Author-written answer to [the assignment](README.md#assignment). Read before guided practice
or compare after your own attempt. [DESIGN.md](DESIGN.md) remains your evidence file.
This is a hypothetical design; no database or service restart was executed.

## Assumptions and requirement

An authenticated owner creates and reads short links through either worker A or B. Workers
can restart between requests. Public redirects do not require an owner session. Administrative
reads and creates do. Link expiry remains authoritative on the server, as in Day 16.

Choose opaque session tokens, represented in storage by a token digest. A shared durable
relational database holds session identity, expiry and revocation, links, and owner-scoped
create replay records. This exercise assumes committed transactions survive a worker crash;
database disaster recovery is a separate requirement. No local cache is needed initially.

The invariant is that replacing a worker cannot lose an acknowledged link or change the
meaning of a valid session. A request already in flight may fail and require a safe retry.

## State placement and request trace

| State | Owner and location | Lifetime and recovery |
| --- | --- | --- |
| Session token | Client; token digest and identity in shared session table | Check expiry/revocation on every authenticated request |
| Link destination, owner, expiry | Links module; shared links table | Durable until lifecycle policy removes it |
| Create request/result | Shared replay table | Same 24-hour replay window as Day 16 |
| Parsing buffers, response assembly | Worker handling this request | Discard and retry after failure |
| Database connections | Bounded pool per worker | Recreate after restart; never an authority for domain state |

The 24-hour replay retention is a previously chosen product policy, not a database guarantee.
Never log the raw session token. The diagram shows logical state access, not deployment sizing.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Worker A
    participant D as Shared database
    participant B as Worker B
    C->>A: Create link with session token and idempotency key
    A->>D: Validate session; atomically commit link and replay record
    D-->>A: Committed result
    A-->>C: Created link
    Note over A: Worker restarts
    C->>B: Read link with same session token
    B->>D: Validate session and read owner-authorized link
    D-->>B: Session and link state
    B-->>C: Same link
```

**Line by line:** A and B consult the same authority. The create response follows commit.
The restart removes A's request state and connections; it does not remove database rows.
B checks both authentication and authorization rather than trusting a client-supplied owner ID.

## Failure walkthrough

Suppose A commits but loses the connection before sending success. The client cannot infer
that creation failed. It retries the same payload and owner-scoped key at B. B authenticates,
resolves the shared replay record, and returns the original result. If A died before commit,
there is no completed transaction to replay and B may execute the create. Concurrent duplicate
keys must serialize through the uniqueness decision described in Day 16.

If session storage is unavailable, authenticated operations fail with a temporary service
error rather than treating the request as authenticated or silently inventing an anonymous
identity. If link storage is unavailable, redirects fail temporarily because this baseline has
no trusted cache. Distinguish storage failure from a confirmed missing or expired record.

Before replacing a healthy worker, stop routing new requests to it and allow bounded draining;
unexpected termination still relies on the retry contract. Worker replacement and database
availability are separate claims.

## Decision and alternative

Choose shared durable records and no worker affinity. It makes restart reasoning simple and
keeps revocation and expiry checks current at the cost of storage access on each request.
Sticky sessions with local authoritative memory cannot meet restart recovery. Signed session
tokens can reduce shared session reads, but immediate revocation then needs a separate policy
or lookup; they do not replace durable link or replay storage.

## Self-review

The artifact locates both session and link state, traces a request at another worker, and
handles uncertain creates. It does not claim that a dictionary demonstration proves durability.
An implementation should test replacement after commit and before commit, expired/revoked
sessions on B, replay conflicts, and unavailable storage. Measure storage latency and aggregate
pool limits as workers increase. These service tests remain proposed; only the local model in
[CONCEPTS.md](CONCEPTS.md) was executed.

Source: [The Twelve-Factor App — Processes](https://12factor.net/processes), checked 2026-09-22,
supports external authoritative state. Transaction/replay choices are this design's assumptions.
