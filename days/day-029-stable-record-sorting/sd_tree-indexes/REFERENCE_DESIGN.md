# Reference design — Tree indexes

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and requirement

We need equality lookup by redirect code and ordered traversal for an indexed key range.
Use an illustrative B+tree-style ordered index. Leaf capacity is three entries only to make
the split visible; actual capacity depends on engine page layout and key width. Keys below
are numeric stand-ins for comparable codes. Payloads live in a separate table. Assume a
cached root and a cold leaf for the read example, not for every request.

## Lookup and page split

```text
Before: root [40]
          left [10,20,30]       right [40,50]
Lookup 30: root says <40 -> left leaf -> table payload

Insert 25 into full left leaf:
  distribute [10,20,25,30] -> [10,20] and [25,30]
  publish separator 25 and the new child reference

After: root [25,40]
          [10,20]      [25,30]      [40,50]
Lookup 30: 25<=30<40 -> middle leaf -> table payload
```

The split preserves sorted key coverage without duplicating or dropping a key. A split of
a full parent can propagate upward; a new root can increase height. Real engines need
concurrency and recovery protocols beyond these snapshots. Separator publication must not
leave keys unreachable to supported readers.

## Amplification and decision

For a toy 4 KiB page and a 64-byte useful entry, one cold leaf read transfers 4096/64=64
times the useful bytes. A cold table payload page adds another read. A cached leaf may avoid
physical disk I/O altogether; page visits and physical reads are different metrics. Inserting
25 changes an old leaf, creates a new leaf, and modifies the parent in this model. WAL and
ancestor splits add work. These are affected pages, not a promise of exactly three physical
writes, since buffering and logging alter when bytes reach storage.

Choose the ordered index for point queries plus range access. A hash-style access path is a
credible alternative for equality-only workloads, but does not supply this key ordering.
An LSM-based engine can offer ordered access with different write/read maintenance costs;
compare it under a representative update workload rather than assuming one engine wins.

## Failure walkthrough

A reader uses the old root while keys 25 and 30 have already moved out of the old leaf.
A naive implementation can report 30 absent. The required invariant is reachability through
every supported structural transition. Rely on the chosen engine's logged split and recovery
mechanism; do not implement it by separately persisting these toy arrays. After a crash,
recovery must restore a valid published structure and preserve the engine's acknowledged-write
contract. This is a hypothetical failure schedule, not a tested PostgreSQL corruption case.

## Self-review and next verification

Lookup, split, read amplification, and write amplification are covered. Unknowns are actual
page occupancy, key size, cache behavior, and update distribution. Next, inspect engine-specific
split documentation and measure index/table page activity for equality, range, and insert
workloads. Check returned rows independently of timing; the Python lesson verifies only the
simplified routing example.


## Sources and comparison

[PostgreSQL B-Tree Indexes](https://www.postgresql.org/docs/18/btree.html) supplies the ordered-index context. The page diagrams here are simplified teaching models, not PostgreSQL on-disk layouts.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
