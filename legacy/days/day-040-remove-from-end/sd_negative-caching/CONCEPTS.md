---
day: 40
part: "2.1"
title: "Negative caching"
ids: [SD-40]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Negative caching

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Cache authoritative absence as a distinct short-lived result, with keys and invalidation that preserve who may observe it.

## The story

A nonexistent short code is requested thousands of times. The database keeps confirming absence, but caching every failed lookup as absence would turn a temporary outage into false 404s.

## The idea in plain language

Recall [cache-aside and source ownership](../../day-036-reverse-a-linked-list/sd_cache-aside/CONCEPTS.md).
A cache miss means the cache has no answer. A negative cache hit means an authoritative lookup
previously found no matching object. A third state is lookup failure: absence is unknown.
Recognize negative caching when repeated missing-key queries are expensive and some delay
before a newly created object appears is acceptable.

## Why Krama needs it

This develops SD-40; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[RFC 2308](https://www.rfc-editor.org/rfc/rfc2308) is a concrete protocol example of negative caching in DNS. This lesson designs an application cache; its result tags, keys, and TTL values are original choices, not DNS rules.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Use a tagged cache result: FOUND(value) or NOT_FOUND, plus expiry. No entry is MISS;
exceptions remain errors and do not become NOT_FOUND. If absence depends on caller identity,
tenant, or visibility scope, those dimensions belong in the key or the result is not shared.

| Time | Event | Correct interpretation |
| --- | --- | --- |
| 0 s | authoritative lookup says no code K | store NOT_FOUND until 2 s |
| 0.5 s | K is created and committed | invalidate K's negative result |
| 0.6 s | request K | load new object if invalidation succeeded |
| 2 s | old negative reaches expiry | next reader must recheck source |

The creation/delete race resembles [late positive fills](../../day-037-middle-node/sd_invalidation-race/CONCEPTS.md):
an old absence read may publish after creation invalidates the key. A finite loader deadline
D and negative TTL T give the same conditional D+T visibility lag from commit, assuming
authoritative reads and no expiry extension. Version barriers or a direct read are alternatives
when read-after-create must be stronger.

Suppose the same missing key receives 2,000 requests/s, negative TTL is 2 seconds, and one
coordinator coalesces its misses. Roughly one source lookup per two seconds replaces thousands
of identical lookups in steady state. A stream of unique invalid keys gains little and can
consume memory; bound admission and the negative-entry budget. Rate limiting and authentication
remain independent controls.

Do not cache transient timeout, connection failure, or server error as definitive absence.
Avoid truthiness-based lookup because a legitimate value can be empty or zero. An internal
negative TTL is separate from downstream HTTP cache headers; a short internal TTL cannot
revoke a longer negative response already cached elsewhere.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
MISS = object()
NOT_FOUND = object()
cache = {'empty': '', 'missing': NOT_FOUND}
print('wrong falsey miss:', not cache['empty'])
assert cache.get('empty', MISS) == ''
assert cache.get('missing', MISS) is NOT_FOUND
assert cache.get('unknown', MISS) is MISS
try:
    raise TimeoutError('origin unavailable')
except TimeoutError:
    wrong = NOT_FOUND
    repaired = 'retryable error'
print('wrong timeout cached as absent:', wrong is NOT_FOUND)
print('repaired outcome:', repaired)
assert 'unknown' not in cache
cache.pop('missing')  # create-commit invalidation in this simple schedule
print('after creation invalidation:', cache.get('missing', MISS) is MISS)
```

**Line by line:** Two distinct sentinels separate no cached answer from cached absence; the empty string remains a valid positive value. The caught timeout demonstrates the incorrect classification without installing it in the repaired cache. Creation removes the negative marker so the next read consults the source.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong falsey miss: True
wrong timeout cached as absent: True
repaired outcome: retryable error
after creation invalidation: True
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Treat negative entries as potentially sensitive existence information. Share only responses
with identical authorization semantics, and authenticate before serving protected results.
Measure negative hits, authoritative misses, unique-key cardinality, false-negative reports,
and invalidation delay. Optional depth: design admission limits for random-code scans and
document the read-after-create exception without caching transient infrastructure failures.

## Check yourself

### Readiness before practice

1. Which three outcomes must a lookup distinguish?
2. How could one tenant's NOT_FOUND hide another tenant's valid object?
3. Why can creation invalidation still be followed by a stale negative fill?

Read [the complete reference answer](REFERENCE_DESIGN.md) for a guided example or
compare it after your own attempt. [DESIGN.md](DESIGN.md) belongs to you.

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
