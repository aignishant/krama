---
day: 29
part: "2.1"
title: "Tree indexes"
ids: [SD-29]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Tree indexes

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

An ordered page index trades a short lookup path for page maintenance and extra writes on updates.

## The story

A redirect lookup needs one record, but storage reads an entire page. Adding one key to a full page then changes more than that one page.

## The idea in plain language

Recall [index selection](../../day-023-target-range/sd_index-selection/CONCEPTS.md). A page is a block transferred or cached as a
unit. An ordered tree index uses separator keys in internal pages to choose child ranges;
leaf pages hold ordered entries. High fan-out—many children per internal page—keeps the
number of levels small. A page split divides a full page and publishes a new separator.
Read amplification is extra data read relative to useful data; write amplification is extra
physical work relative to the logical update. Always specify bytes or operations as the unit.

## Why Krama needs it

This develops SD-29. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[PostgreSQL B-Tree Indexes](https://www.postgresql.org/docs/18/btree.html) supplies the ordered-index context. The page diagrams here are simplified teaching models, not PostgreSQL on-disk layouts.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Use a deliberately tiny tree with leaf capacity three entries and root separator 40:

```text
root [40]
  <40: [10,20,30]        >=40: [40,50]
insert 25 -> split left into [10,20] and [25,30]
root [25,40]
  <25: [10,20]    [25,40): [25,30]    >=40: [40,50]
```

Lookup 30 follows the middle child after the split. The separator invariant ensures every
key remains reachable through the appropriate range. A stale root containing only 40 could
route 30 to a left page that no longer contains it. Real engines coordinate concurrent reads,
logging, and recovery around structural changes; this diagram is not a crash-safe algorithm.

If the root is cached and the leaf is not, this toy lookup reads one leaf page; an uncached
root adds another. A non-covering index may need a separate table page for the payload.
With an illustrative 4 KiB page and 64 useful bytes, one page read transfers 4096/64=64
times the useful bytes. That is a defined example ratio, not a measured database metric.
Splitting touches the old leaf, new leaf, and parent, with additional logging and possible
ancestor splits. Lookup depth is O(log_f N) page levels for fan-out f, not a constant disk-I/O
guarantee. Range scans benefit from leaf ordering; random updates can dirty many pages.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
leaves = [[10, 20], [25, 30], [40, 50]]
def lookup(key, separators):
    child = sum(key >= boundary for boundary in separators)
    return key in leaves[child]
print('stale routing finds 30:', lookup(30, [40]))
print('published separator finds 30:', lookup(30, [25, 40]))
assert not lookup(30, [40]) and lookup(30, [25, 40])
print('illustrative page/useful-byte ratio:', 4096 // 64)
```

**Line by line:** The same leaf contents are searched with stale and updated separators. The child index counts crossed boundaries. This deliberately simplified routing failure explains why split publication matters; it does not model engine concurrency or recovery.

Observed author output on Python 3.12.10, 2026-09-23:

```text
stale routing finds 30: False
published separator finds 30: True
illustrative page/useful-byte ratio: 64
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Use an established storage engine rather than implementing the split protocol from this
diagram. Measure page-cache hit rates, payload fetches, write volume, and tail latency under
the actual key distribution. Wide keys reduce fan-out. A reviewer should ask which queries
need ordered traversal and whether covering more columns is worth a larger index. Optional
depth: inspect engine-specific page split and recovery documentation.

## Check yourself

### Readiness before practice

1. Which separator must be added after the split?
2. Why can one logical insert change several pages?
3. Does a cached-root lookup imply one physical disk read?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
