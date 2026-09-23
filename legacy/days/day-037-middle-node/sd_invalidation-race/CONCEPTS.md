---
day: 37
part: "2.1"
title: "Invalidation race"
ids: [SD-37]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Invalidation race

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Deleting after a write does not prevent an older in-flight read from filling the cache again; enforce a freshness bound or an atomic version barrier.

## The story

A writer commits a new destination and deletes the cached old link. A reader that started earlier finishes later and puts the old destination back.

## The idea in plain language

Recall [cache-aside](../../day-036-reverse-a-linked-list/sd_cache-aside/CONCEPTS.md):
the database owns truth; the application fills a cache after a miss. An interleaving is the
order in which separate requests' individual steps occur. Each request can be correct in
isolation while their combined order is wrong. Recognize this risk whenever loading and
publishing are separated by time and writers can change the same key.

## Why Krama needs it

This develops SD-37; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Azure Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) describes cache/source consistency limits. The interleaving and proposed policies are original design analysis.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

The database initially contains version 4. The cache is empty.

| Time order | Reader R | Writer W | Cache |
| --- | --- | --- | --- |
| 1 | misses; reads version 4 | | absent |
| 2 | pauses before fill | commits version 5 | absent |
| 3 | still paused | deletes cache key | absent |
| 4 | publishes version 4 | | version 4 |
| 5 | another reader hits old value | | version 4 |

Changing write/delete ordering alone does not remove all races. For a bounded-staleness
policy, suppose authoritative reads plus publication finish within D=0.2 seconds and entries
expire T=5 seconds after fill, with no hit-based extension. A pre-commit snapshot can be
published as late as D after commit and live another T: the conditional bound is D+T=5.2 s,
not merely T. Discard late loader results. A replica with unbounded lag destroys this bound;
so does refreshing TTL on every hit. Direct responses need the same deadline/freshness policy.

Alternatively maintain a minimum accepted version per key. The writer advances that barrier
to 5, and a loader may publish only if its version is at least the barrier, with check and
publish performed atomically. A barrier must outlive stale loaders and survive relevant cache
eviction/restart cases; otherwise absence again permits version 4. This alone does not make
the database commit and cache update atomic. Define write acknowledgment, recovery, and read
behavior while propagation is incomplete before claiming read-after-write guarantees.

TTL is simpler but allows stale answers; version coordination costs metadata and operations.
For strict decisions such as revocation, an authoritative read can be the appropriate route.
The numeric policy here is an assumption for a display destination, not a measured service.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
db = (4, 'old')
cache = {}
snapshot = db
db = (5, 'new')
cache.pop('link', None)
cache['link'] = snapshot
print('after delete and late fill:', cache['link'])
assert cache['link'] != db
# One sequential atomic-step model, not a distributed implementation.
minimum_version = 5
cache.clear()
if snapshot[0] >= minimum_version:
    cache['link'] = snapshot
print('late fill rejected:', 'link' not in cache)
assert 'link' not in cache
delay, ttl = 0.2, 5.0
print('conditional bound seconds:', delay + ttl)
```

**Line by line:** A saved tuple models the old read. Committing a new tuple and deleting cannot retract that saved value. The second schedule checks a retained version barrier before publishing; the final arithmetic includes loader delay in the staleness budget.

Observed author output on Python 3.12.10, 2026-09-23:

```text
after delete and late fill: (4, 'old')
late fill rejected: True
conditional bound seconds: 5.2
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Measure stale-version hits, loader duration, invalidation lag, and dropped late fills.
Retry invalidation reliably, but do not describe eventual retries as atomic commit. Optional
depth: design restart recovery for version metadata, delayed messages, and a cache outage.
Never place a critical authorization decision behind an assumed display-only freshness bound.

## Check yourself

### Readiness before practice

1. Why can a delete that runs after commit still leave stale data?
2. Why is the bound D+T instead of T when expiry starts at fill?
3. What breaks if eviction removes the minimum-version barrier?

Read [the complete reference answer](REFERENCE_DESIGN.md) for a guided example or
compare it after your own attempt. [DESIGN.md](DESIGN.md) belongs to you.

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
