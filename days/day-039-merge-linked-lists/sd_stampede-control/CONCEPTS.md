---
day: 39
part: "2.1"
title: "Stampede control"
ids: [SD-39]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Stampede control

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Coalesce same-key loads, spread different-key expiration, and serve bounded stale data only when the product permits it.

## The story

A popular redirect expires. Hundreds of waiting requests all ask the database for the same value before the first lookup has finished.

## The idea in plain language

Recall [TTL versus eviction](../../day-038-cycle-entry/sd_ttl-and-eviction/CONCEPTS.md).
A cache stampede is overlapping origin work triggered by misses or refreshes. Single-flight
means callers for one key share one in-progress load. TTL jitter disperses expiration across
keys. Stale-while-revalidate serves an old answer during a bounded window while refresh runs.
These act on different causes and can be combined.

## Why Krama needs it

This develops SD-39; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Go singleflight documentation](https://pkg.go.dev/golang.org/x/sync/singleflight) describes duplicate-call suppression. [RFC 5861](https://www.rfc-editor.org/rfc/rfc5861) defines bounded HTTP stale-while-revalidate semantics.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Assume a popular key receives 1,000 requests/s and an origin load takes 0.1 s. During one
load, approximately 100 requests arrive. Without coalescing, that is roughly 100 overlapping
loads; it is an assumed rate-times-duration estimate, not a benchmark.

| Technique | What it controls | What it does not guarantee |
| --- | --- | --- |
| Single-flight per key | overlapping loads in the coordinator's scope | freshness, global uniqueness across processes |
| TTL jitter per fill | correlated expiry across many keys | one hot key's burst |
| Stale-while-revalidate | caller wait time during allowed staleness | permission to serve indefinitely stale data |

For one process, retain a map key -> pending result. The first miss installs it atomically
and becomes loader. Later callers attach to that result. On success, publish, notify waiters,
and remove the pending entry; on failure, notify error and clear it too. Use bounded waiting
and an origin concurrency budget. A cancelled waiter must not accidentally cancel work still
needed by other waiters. Scope the key to every request attribute that affects the answer.

For a stale window, store both fresh_until and stale_until. Before fresh_until, serve normally.
Between the boundaries, serve stale if allowed and trigger one refresh. At stale_until or
later, wait within a deadline or fail; never reset that boundary merely because a refresh
failed. Hard deletion/authorization decisions need a stricter route. The HTTP extension
defines this behavior for HTTP caches; using two deadlines in an application cache is an
explicit analogous policy, not automatic protocol compliance.

With P independent worker processes, local single-flight can still create P concurrent
origin loads for a key. A shared lease may reduce that number but adds failure and ownership
rules; a paused former owner must not overwrite a newer result after its lease expires.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
arrivals = ['popular'] * 6
naive_loads = len(arrivals)
pending = set()
leaders = waiters = 0
for key in arrivals:  # all arrivals precede completion in this model
    if key in pending:
        waiters += 1
    else:
        pending.add(key)
        leaders += 1
print('naive, shared, waiters:', naive_loads, leaders, waiters)
assert (leaders, waiters) == (1, 5)
pending.remove('popular')  # required on failure as well as success
assert not pending
fresh_until, stale_until = 10, 13
def mode(now):
    if now < fresh_until:
        return 'fresh'
    if now < stale_until:
        return 'stale and refresh'
    return 'wait or fail'
print('at 11:', mode(11))
print('at 13:', mode(13))
assert mode(13) == 'wait or fail'
```

**Line by line:** Six overlapping arrivals create six naive loads but one leader and five followers with a pending-key registry. Removing the pending key models completion cleanup. The two explicit deadlines prevent a refresh failure from authorizing unbounded stale service.

Observed author output on Python 3.12.10, 2026-09-23:

```text
naive, shared, waiters: 6 1 5
at 11: stale and refresh
at 13: wait or fail
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Optional depth: model a loader crash, coordinator restart, waiter cancellation, and a lease
expiring mid-load. Recheck the cache after acquiring a distributed lease; someone may already
have filled it. Protect origin capacity during cache outages, when every key appears missing.
Measure coalesced waiters, load duration, refresh errors, served age, and origin concurrency.

## Check yourself

### Readiness before practice

1. Why does random TTL not prevent six misses for the same expired key?
2. How many loads might eight processes create with only local single-flight?
3. What should happen after stale_until when the origin remains unavailable?

Read [the complete reference answer](REFERENCE_DESIGN.md) for a guided example or
compare it after your own attempt. [DESIGN.md](DESIGN.md) belongs to you.

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
