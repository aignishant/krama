---
day: 30
part: "2.1"
title: "Log structured storage"
ids: [SD-30]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Log structured storage

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Log-structured storage batches writes into immutable sorted files and pays later to reconcile those files.

## The story

Writes are fast while memory buffers fill, but after a long burst the service pauses because background file merging cannot keep up.

## The idea in plain language

Compare [tree pages](../../day-029-stable-record-sorting/sd_tree-indexes/CONCEPTS.md). A memtable is an in-memory ordered buffer. A write-ahead
log (WAL) records changes for recovery under the chosen durability policy. Flushing writes an
immutable sorted file. Compaction merges files, preserving relevant versions and eventually
reclaiming obsolete data. Immutable files avoid in-place updates, but multiple files may hold
different versions of the same key. A read must resolve the newest visible version.

## Why Krama needs it

This develops SD-30. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[RocksDB getting started](https://rocksdb.org/docs/getting-started.html) and [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction) describe log-structured storage components and compaction.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Consider versions k@1=A, k@2=B, then k@3=deleted. After separate flushes, F1 contains A,
F2 contains B, and F3 contains a tombstone, a marker suppressing older values. A read must
return absence, not A or B. A memtable entry could be newer than all files. Metadata, indexes,
and filters help decide which files might contain the key; they do not change version rules.

```text
write -> durability log -> mutable memtable -> immutable flush file
read  -> memtable + candidate files -> newest visible value/tombstone
files -> compaction -> replacement files -> retire obsolete files safely
```

For a toy budget, ingest 10 MiB of logical data, append 10 MiB to the WAL, flush 10 MiB,
and later write 30 MiB of compaction output. Storage bytes written=50 MiB and write
amplification=50/10=5 under this explicit accounting convention. Compression, metadata,
replication, and filesystem effects are excluded. Lower write amplification may mean more
overlapping files and higher read work; more aggressive compaction can reverse that tradeoff.

Correctness requires recoverable acknowledged writes and a visibility rule across versions.
Do not remove a tombstone while an older value can still be consulted, including snapshots
or replicas where relevant. Compaction is neither a universal constant cost nor free garbage
collection: it competes for I/O, CPU, and temporary disk space. Sustained ingest above that
maintenance capacity creates backlog and can force write throttling.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
files = [(1, 'A'), (2, 'B'), (3, None)]  # None is a deletion marker in this model.
wrong = next(value for version, value in files if value is not None)
newest = max(files, key=lambda entry: entry[0])[1]
print('oldest nonempty read:', wrong)
print('latest visible read:', newest)
assert wrong == 'A' and newest is None
print('modeled write amplification:', (10 + 10 + 30) / 10)
```

**Line by line:** Skipping deletion markers and accepting the first value resurrects A. Selecting the highest sequence instead respects the delete. The arithmetic names a chosen accounting boundary; it does not measure RocksDB.

Observed author output on Python 3.12.10, 2026-09-23:

```text
oldest nonempty read: A
latest visible read: None
modeled write amplification: 5.0
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Start with engine defaults and workload measurements rather than choosing a compaction
policy from slogans about cheap writes. Monitor pending compaction bytes, stalls, disk headroom,
and read tails. WAL sync settings determine what an acknowledged write survives. A reviewer
should ask what happens when recovery replays writes and compaction has not completed.
Optional depth: compare leveled and tiered compaction for the same read/write mix.

## Check yourself

### Readiness before practice

1. Why can immutable files contain contradictory values?
2. When would dropping a tombstone resurrect data?
3. What work is included in the ratio 5?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
