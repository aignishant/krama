---
day: 36
part: "2.1"
title: "Cache aside"
ids: [SD-36]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Cache aside

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Cache-aside serves reusable copies while the database remains the source of truth on a miss.

## The story

The database returns a valid redirect, but storing it in the cache fails. Turning that optional fill failure into a failed redirect reduces availability for no correctness benefit.

## The idea in plain language

Recall [stateless workers](../../day-017-container-capacity/sd_stateless-workers/CONCEPTS.md) and [expiration](../../day-033-kth-smallest/sd_ttl-and-deletion/CONCEPTS.md). A cache stores
copies to reduce repeated source reads. Cache-aside means application code checks the cache,
loads from the database on a miss, and attempts to populate the cache. A miss is not proof of
absence. A database failure is not proof of absence either. Keep successful absence, timeout,
and failed fill as distinct states.

## Why Krama needs it

This develops SD-36. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) explains loading on a miss and the consistency tradeoff. Failure responses and numeric budgets here are proposed application choices.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For a redirect code, store destination, version, and expires_at in a cached payload. A hit
must satisfy the validity rule; expired content is treated as unusable even if the cache key
still exists. The database owns durable link state.

| Path | Action | User result under this example policy |
| --- | --- | --- |
| valid hit | check deadline; return payload | redirect without source read |
| miss, DB valid | load, attempt cache fill | redirect |
| miss, DB absent/expired | return absence | no redirect |
| miss, DB failure | bounded failure response | retryable error, not not-found |
| DB valid, fill failure | record fill error | redirect from fetched value |

On a write, update the database before invalidating the cache. This ordering avoids one
simple stale refill but does not solve every race: a reader may fetch v1, a writer commit v2
and invalidate, then the reader fill v1. TTL limits lifetime from fill, not necessarily from
the database update. Strong freshness needs version-aware coordination or source validation.

If hit rate is h, read demand is R requests/s, and misses load once, expected source reads
are approximately R*(1-h). Synchronized misses, retries, and cache outages break that simple
model. The cache adds memory, network hops, invalidation work, and a new failure mode; it
should be introduced for a measured repeated-read benefit, not as a substitute for truth.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
def read_model(cache_hit, db_ok=True, found=True, fill_ok=True):
    if cache_hit:
        return 'redirect', 'cache'
    if not db_ok:
        return 'retryable error', 'database failure'
    if not found:
        return 'absent', 'database'
    return 'redirect', 'filled' if fill_ok else 'fill failed'
for args in [(True,), (False,), (False, False), (False, True, True, False)]:
    print(read_model(*args))
assert read_model(False, False)[0] != 'absent'
assert read_model(False, True, True, False)[0] == 'redirect'
```

**Line by line:** The model assumes cache_hit already means a valid hit. Database failure is handled before absence. The fill flag changes telemetry but not a successfully fetched redirect, isolating the failure coupling to avoid.

Observed author output on Python 3.12.10, 2026-09-23:

```text
('redirect', 'cache')
('redirect', 'filled')
('retryable error', 'database failure')
('redirect', 'fill failed')
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Bound cache and source timeouts inside the request deadline. Coalesce concurrent misses for
the same key and cap fallback source concurrency so cache failure does not overwhelm storage.
Negative caching needs its own short-lived contract and must never cache transient failures as
absence. A reviewer should ask whether stale destinations are acceptable after edit or revoke.
Optional depth: design a version-aware fill strategy and test the late-reader race explicitly.

## Check yourself

### Readiness before practice

1. Why can a fill failure still return a redirect?
2. Why is DB timeout different from absent?
3. Which race survives update-then-invalidate?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
