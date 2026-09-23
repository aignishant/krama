---
day: 4
part: "2.1"
title: "Separate stored data from the capacity needed to operate it"
ids: [SD-04]
level: working
prerequisites: ["Traffic estimates", "Units and ratios"]
failure: true
---

# Separate stored data from the capacity needed to operate it

Core: follow the capacity calculation and failure check before writing your memo. All sizes,
retention periods, overhead factors, and utilization targets below are teaching assumptions.
Compression, archival tiers, and detailed engine layouts are optional depth.

## One-line answer

Calculate retained logical bytes first, then account separately for indexes, copies, and working headroom.

## The story

You estimate shelf space for a year's parcel records. Counting just the pages misses index
cards and the duplicate archive at another site. Filling every shelf also leaves nowhere to
sort incoming boxes. The records' size and the room's required capacity are different quantities.

## The idea in plain language

**Retention** is how long records remain stored. **Logical raw storage** is the sum of modeled
record bytes before extra storage layers. A **replication factor** counts total live copies,
including the original. **Headroom** is spare provisioned capacity for operations and growth.
Use [Day 3's unit reasoning](../../day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md), but
do not substitute read requests for newly retained records.

Recognize this framework when asked how much data accumulates or whether a storage plan fits.
State what “bytes per record” includes: payload only, serialized fields, or measured on-disk
rows. An undefined record size makes even perfect multiplication misleading.

## Why Krama needs it

Storage-engine choices later change index, log, and compaction costs. Today a transparent
model lets you revise one assumption without losing track of what has already been counted.

## The mechanism

### Worked trace

Assume 20,000 new parcel records per day, 800 bytes per record, and retention for 180 days.
Assume steady arrivals, no initial backlog, no early deletion, and no compression. This is
an original arithmetic model, not a claim about any database's physical layout.

| Layer | Calculation | Decimal bytes or GB |
| --- | --- | --- |
| Retained count | 20,000/day × 180 days | 3,600,000 records |
| Raw logical data B | 3,600,000 × 800 bytes | 2,880,000,000 bytes = 2.88 GB |
| Index estimate I | Assumed 25% of B | 0.72 GB |
| One copy, data plus indexes | B + I | 3.60 GB |
| Three total live copies | (B + I) × 3 | 10.80 GB |
| Provisioning at 75% maximum use | 10.80 / 0.75 | 14.40 GB total |

GB means 10^9 bytes here; GiB means 2^30 bytes. Convert at the end and name the unit. At the
180-day retention horizon, count reaches steady state only if expiry actually removes data
as fast as it ages out. With no expiry, storage keeps growing. Real reclamation may lag logical deletion.

The equation is `capacity = (raw + indexes) × total_live_copies / target_utilization` for this
specific model. It assumes indexes exist on each replica. Backups, write-ahead logs, temporary
compaction space, metadata, and historical versions are outside this equation until separately
estimated. Headroom is not proof that every omitted category fits.

Why the model works: each multiplication introduces an explicitly named dimension or copy
count. No term is charged twice. Divide by utilization because “occupied bytes / capacity =
utilization.” Merely adding 25% to occupied bytes yields 80% utilization, not 75%.

### Sensitivity and limits

Doubling record size doubles B and the index estimate **under the percentage assumption**.
It need not double a real index whose keys are unchanged. Decreasing retention halves stored
count only after old data is reclaimed. A mean record size can miss unusually large records;
sample the distribution and the encoding, not just character counts.

## When it breaks

```python
raw_bytes = 20_000 * 180 * 800
index_bytes = raw_bytes * 0.25
copies = 3
wrong = raw_bytes * copies + index_bytes
occupied = (raw_bytes + index_bytes) * copies
print(f"indexes once={wrong / 10**9:.2f} GB, on every copy={occupied / 10**9:.2f} GB")
try:
    assert wrong == occupied, "replicated indexes were omitted"
except AssertionError as error:
    print(f"AssertionError: {error}")
capacity = occupied / 0.75
assert abs(occupied / capacity - 0.75) < 1e-12
print(f"capacity at 75% use={capacity / 10**9:.2f} GB")
```

**Line by line:** raw bytes and indexes are separate terms. The wrong expression replicates
only the data, even though this model stores indexes on every copy. Parentheses repair that
accounting error. Dividing by 0.75 sets the intended occupancy, and the final assertion checks
the ratio instead of trusting a label. Floating-point tolerance is sufficient for this toy model.

Author verification on Python 3.12.10, 2026-09-22:

```text
indexes once=9.36 GB, on every copy=10.80 GB
AssertionError: replicated indexes were omitted
capacity at 75% use=14.40 GB
```

## In production

Replace assumed bytes with measured serialized and on-disk sizes on representative records.
Budget restore space, log retention, and temporary rewrite space explicitly before provisioning.
Replication supports serving through failures, while independently retained backups support
recovery from some mistakes; replicas may repeat an accidental deletion. Neither is established
by a capacity number alone. Compare shorter retention or archival storage with keeping every
record immediately queryable, stating the product and recovery consequences.

## Check yourself

### Readiness before practice

Why do ten reads of one link create no ten-record storage increment? Does replication factor
three mean three copies or four? Why must index replication be stated? Does a 75%-full target
mean adding 25% to occupied bytes? Which omitted category is most uncertain in your model?

Open [the assignment](README.md#assignment) and calculate its separate link-storage workload
in [DESIGN.md](DESIGN.md). Name your year length, byte units, retention, and record-size boundary.
Show raw, index, and replication terms separately. Add an alternative and a failure walkthrough
such as delayed cleanup filling the disk. Explain what you would measure before buying capacity;
the exercise requires a memo, not a deployed database.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-004-storage-estimates)

## Complete worked design

Open [REFERENCE_DESIGN.md](REFERENCE_DESIGN.md) for a finished response to the actual daily
assignment, including assumptions, reasoning, an alternative, and a failure walkthrough.
Read it first for guidance or compare after an independent attempt. The assistant writes the
reference; you fill [DESIGN.md](DESIGN.md) for your own practice. Reference reading is available
without completing that practice and does not mark the track complete.
