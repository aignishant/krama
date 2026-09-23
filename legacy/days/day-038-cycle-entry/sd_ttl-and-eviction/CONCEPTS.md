---
day: 38
part: "2.1"
title: "TTL and eviction"
ids: [SD-38]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# TTL and eviction

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Expiration decides whether an entry may be served; eviction decides which entry to remove when memory is scarce.

## The story

The cache has plenty of free space, yet every popular key becomes unusable at the same instant. More memory cannot make expired answers fresh.

## The idea in plain language

Recall [cache freshness and fill races](../../day-037-middle-node/sd_invalidation-race/CONCEPTS.md).
A TTL is a lifetime, normally measured from a defined insertion or refresh point. An eviction
policy chooses victims under a capacity limit. LRU prefers evicting entries not used recently;
LFU favors entries used more often. Neither popularity rule establishes correctness or freshness.

## Why Krama needs it

This develops SD-38; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Redis key eviction](https://redis.io/docs/latest/develop/reference/eviction/) and [EXPIRE](https://redis.io/docs/latest/commands/expire/) distinguish memory policies and expiration semantics.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Assume a two-entry toy cache and a five-second TTL measured from each fill:

| Time | Event | Consequence |
| --- | --- | --- |
| 0 s | fill A and B | both eligible until 5 s |
| 1 s | read A | A becomes most recently used; expiry stays 5 s |
| 2 s | insert C | evict B for space although B was fresh |
| 5 s | request A | A has expired although it was popular |

Check `now < expires_at` to serve an entry; at equality it is expired. Logical expiration
can be enforced during reads even if physical memory reclamation happens later. Memory
eviction can remove a still-fresh key earlier. Cache TTL is also separate from the record's
own domain expiry: an expired link is invalid even if its cache entry is young.

For a hypothetical 20,000-key warmup at time zero with fixed TTL 60 seconds, all keys become
eligible for reload together. If the origin admits 500 reads/second and those keys are all
requested immediately, even one load per key takes at least 40 seconds of origin capacity.
This is a demand/capacity bound, not an observed latency. Duplicate same-key loads can be worse.

Choose a maximum TTL from the freshness requirement, then choose eviction independently from
memory and access locality. To keep a maximum 60-second TTL while spreading expiration,
draw each fill TTL from 45..60 seconds. Do not use 60 plus positive jitter if 60 is a hard
maximum. Jitter spreads different keys; it cannot suppress simultaneous reloads for one hot
key. [The next lesson](../../day-039-merge-linked-lists/sd_stampede-control/CONCEPTS.md)
teaches that separate mechanism. Hit/miss handling should remain correct under arbitrary
eviction, including an entirely empty cache.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
from collections import OrderedDict

cache = OrderedDict(A=('a', 5), B=('b', 5))
cache.move_to_end('A')  # a hit changes recency, not expiry
cache['C'] = ('c', 7)
victim, _ = cache.popitem(last=False)
print('evicted while fresh:', victim)
assert victim == 'B'
now = 5
wrong = 'A' in cache
fresh = 'A' in cache and now < cache['A'][1]
print('presence versus freshness:', wrong, fresh)
assert wrong and not fresh
expirations = [45 + i % 16 for i in range(32)]
print('spread range:', min(expirations), max(expirations))
assert max(expirations) <= 60
```

**Line by line:** OrderedDict represents a two-entry LRU example. Access moves A to the recent end, insertion evicts B, and the clock then makes A logically expired. The final deterministic offsets illustrate the allowed jitter range; they do not test a random production distribution.

Observed author output on Python 3.12.10, 2026-09-23:

```text
evicted while fresh: B
presence versus freshness: True False
spread range: 45 60
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Redis separates configured memory pressure policy from per-key expiration; eviction can
be approximate and some policies consider only expiring keys. Verify the selected engine's
behavior rather than treating this toy LRU as its implementation. Budget for keys, values,
allocator overhead, and replication buffers, then measure actual memory usage. Monitor
expired misses separately from capacity evictions to diagnose the right cause.

## Check yourself

### Readiness before practice

1. Can a fresh key be evicted? Can a popular key expire?
2. Why does adding memory not solve simultaneous expiration?
3. Which jitter interval preserves a hard 60-second maximum?

Read [the complete reference answer](REFERENCE_DESIGN.md) for a guided example or
compare it after your own attempt. [DESIGN.md](DESIGN.md) belongs to you.

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
