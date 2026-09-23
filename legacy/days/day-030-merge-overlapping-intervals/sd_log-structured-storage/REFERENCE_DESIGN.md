# Reference design — Log structured storage

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and requirement

Assume an update-heavy keyed workload requiring durable acknowledged writes, point reads,
and occasional ordered scans. Each write has a monotonically ordered sequence number in one
engine's history. The example assumes WAL durability before acknowledgment; exact sync and
failure-domain semantics must be configured in the actual engine. No throughput is claimed.

## Buffer, files, and compaction

```text
put(k,v,seq) -> durable WAL -> active memtable -> acknowledge
                                |
                         freeze when full
                                v
                       immutable sorted file F

read(k) -> active/frozen tables + candidate files -> newest visible entry
compaction(F1,F2,...) -> merged replacement files -> safe metadata publication
                                                 -> retire obsolete inputs
```

The write path sketches an ownership/durability sequence, not a library API call order.
Frozen buffers can coexist with the active one during flush. A WAL cannot be retired merely
because a flush began; persisted state and recovery metadata must cover its records first.

Trace k@1=A in F1, k@2=B in F2, and k@3=deleted in memory. A latest-state read returns absence.
After the deletion flushes, compaction must preserve that absence while any older A/B version
remains visible to supported readers. Snapshot rules can require keeping older versions.
Publishing replacement files before safely discarding inputs avoids losing the durable state
if compaction is interrupted. Exact protocols belong to the storage engine.

## Read cost, write cost, and alternative

Assume 10 MiB of logical updates, 10 MiB WAL output, 10 MiB flush output, and 30 MiB compaction
output. Count storage bytes written excluding compression, replication, metadata, and filesystem
overhead: amplification=(10+10+30)/10=5. It is an illustrative accounting example. A point miss
may consider several files; filters can avoid some reads, while a hit must still respect versions.
Range reads merge relevant runs. Compaction reduces overlap at the cost of rewriting data.

Choose log-structured storage only if batched writes and measured maintenance capacity fit the
workload. An ordered page tree is the alternative: fewer candidate versions may simplify reads,
but random updates dirty pages and splits cause maintenance. Compare p95/p99 latency, bytes
written, disk occupancy, and recovery under the same workload and durability policy.

## Failure walkthrough

Ingest outpaces compaction. Immutable files and pending compaction bytes grow, reads examine
more candidates, and disk headroom falls. Continuing admission without bounds risks running
out of space. Apply backpressure or write throttling, reserve compaction headroom, and restore
maintenance capacity. Never delete live files manually to make room. A crash before an
acknowledged update is covered by a durable flush requires WAL replay; disabling the required
sync changes the durability promise and must not be hidden behind the same success response.

## Self-review

The answer includes memory, immutable storage, maintenance, and both cost directions. The
unknown is whether the proposed engine can sustain ingest while recovering backlog. Next,
benchmark steady state and a write burst, verify post-restart values, and inspect tombstone
and snapshot retention. None of these engine experiments has been run for this reference.


## Sources and comparison

[RocksDB getting started](https://rocksdb.org/docs/getting-started.html) and [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction) describe log-structured storage components and compaction.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
