---
day: 31
track: system-design
title: "B-trees and why indexes are shaped that way"
phase: "Databases from zero"
status: written
---

# Day 031 · System Design — B-trees and why indexes are shaped that way

**After today you can:** You can draw a B-tree and explain why the database does not use a binary tree on disk.

**The interviewer asks it as:** *Why is a database index a B-tree and not a binary search tree?*

---

## 1. What this is, and why they ask it

Yesterday you learned what an index buys you. Today is *why it has the shape it has*, and the answer is
one fact about hardware:

> **Reading from disk costs the same whether you read 1 byte or 8,000 bytes.**

A disk read has an enormous fixed cost — the operating system fetches a whole page, typically 8 KB,
whatever you asked for. So the number that matters is not "how many comparisons" but **how many page
reads**. Everything about a B-tree's shape follows from minimising that one number.

A binary search tree makes one decision per node, so it needs `log₂(n)` nodes — 24 levels for ten
million rows, and if each node is on a different page, 24 disk reads. A **B-tree** packs hundreds of
keys into each node, so one page read makes a several-hundred-way decision. Three or four page reads
cover ten million rows. **Same number of comparisons, eight times fewer trips to the disk**, and the
trips are what cost.

Interviewers ask this because it is the clearest example in the whole subject of a data structure
shaped by hardware rather than by theory. A candidate who says "B-trees are balanced" has half the
answer; one who says "because a disk read is a fixed cost, so you want the fattest node that fits in
one page" has all of it. It also opens the door to the LSM-tree comparison, which is the natural
follow-up and the reason Cassandra and RocksDB behave differently from Postgres.

---

## 2. The story

Habib's godown is one big room with a loft above it, reached by a wooden ladder in the corner, and the
loft is where everything that is not moving this week goes.

The ladder is the whole problem. It takes him about two minutes to go up it properly — he is
sixty-one, and the third rung has been going for a while — and about two minutes to come down. Once he
is up there, walking around and looking at things costs him nothing. He can read the labels on forty
boxes in twenty seconds.

So the arithmetic of his day is entirely about trips, not about looking.

When he started, things went up in the order they arrived, and when a customer wanted something he
went up, looked, came down, went up again. Six trips was a normal morning — twenty-four minutes on a
ladder to find one box of clutch plates.

What he does now is that there is a board nailed to the wall at the top of the ladder, and on it is
written what is in each of the eight bays — the ranges, roughly. Bay one, part numbers up to 4000. Bay
two, 4000 to 9000. And so on. He climbs once, stands at the top, reads the board, and walks to the
right bay.

At the front of each bay there is a smaller board doing the same thing for the twelve shelves in it.

So it is: one climb, read the big board, walk to the bay, read the small board, take the box. **One
climb.** Not six, not twenty-four.

His nephew suggested something during the renovation that Habib turned down flat. The nephew wanted a
neat system where at the top of the ladder there was a sign saying "under 5000, go left; over 5000, go
right", and then another sign at each place saying the same thing again, halving each time. It is
tidier, and it needs fewer words on each board.

Habib's objection was simple and correct. Every one of those signs is a place you have to *walk to*,
and walking to a place is what costs. Reading eight ranges off one board costs the same as reading two.
So put as much on each board as you can possibly fit, and make the number of places you have to walk
to as small as possible.

---

## 3. The idea in plain English

The ladder climb is a **disk page read**. Reading the board once you are up there is **comparisons in
memory**, which are effectively free. And Habib's objection to his nephew is the entire argument for
B-trees over binary trees.

### The hardware fact everything rests on

From [day 009](../day-009-what-an-array-is/README.md) and
[day 010](../day-010-traversal-patterns/README.md):

```
one CPU comparison        ≈ 1 nanosecond
one main-memory access    ≈ 100 nanoseconds
one SSD page read         ≈ 100,000 nanoseconds  (0.1 ms)
one spinning-disk seek    ≈ 10,000,000 nanoseconds (10 ms)
```

An SSD page read is about **100,000 times** the cost of a comparison. And crucially, the disk delivers
a whole **page** — 8 KB in Postgres, 16 KB in MySQL's InnoDB — whether you wanted one byte or all of
it.

So a structure stored on disk should be designed to answer the question **"how few pages must I
touch?"** and should treat everything inside a page as free.

### Why a binary tree is the wrong shape here

A binary search tree stores one key per node and makes one decision at each. For `n` items, the depth
is `log₂(n)`:

```
n = 10,000,000  ->  log2(10,000,000) ≈ 24 levels
```

Each node is small — a key and two pointers, maybe 24 bytes — so it sits somewhere unpredictable in
memory or on disk. Walking down the tree touches 24 different nodes, and in the worst case that is
**24 separate page reads**:

```
24 page reads × 0.1 ms = 2.4 ms
```

And 8,000 bytes arrive with each read of which you use 24. You are paying for a full page and using
0.3% of it.

That is the nephew's tidy scheme: many signs, each carrying one bit of information, each requiring a
walk.

### What a B-tree does instead

A **B-tree** node is exactly one page, and it is filled with as many keys as will fit. With an 8 KB
page and roughly 16 bytes per entry:

```
8,192 bytes / 16 bytes ≈ 500 entries per node
```

That is the **fanout** — the number of children a node can have. One page read now makes a 500-way
decision instead of a 2-way one, so the depth is `log₅₀₀(n)`:

```
log500(10,000,000) ≈ 2.7   ->  3 levels
```

| Rows | Binary tree depth | B-tree depth (fanout 500) |
|---:|---:|---:|
| 1,000 | 10 | 2 |
| 250,000 | 18 | 2 |
| 10,000,000 | 24 | 3 |
| 62,500,000,000 | 36 | 4 |

**Three page reads instead of twenty-four.** Same total number of comparisons — about 24 either way,
since `log₂(500) ≈ 9` and `3 × 9 = 27` — but 24 of them happen *inside pages you have already paid
for*.

That is the whole answer: **the comparisons are free and the page reads are not, so you want the
fattest node that fits in one page.**

### The three properties of a B-tree

1. **Every leaf is at the same depth.** The tree is perfectly balanced by construction, so every lookup
   costs the same. There is no bad case.
2. **Nodes are kept at least half full.** A node that drops below half merges with a sibling. This is
   what stops the tree degenerating into something tall and sparse after many deletions.
3. **Keys within a node are sorted, and so are the children.** That is what makes range queries work.

### B+ trees, which is what databases actually use

Almost every real database uses a **B+ tree**, a variant with two differences that both matter:

**All the actual data pointers live in the leaves.** Internal nodes hold only keys, used for
navigation. That makes internal nodes smaller, so the fanout is higher, so the tree is shallower.

**The leaves are linked to each other in order.** Once you have found the start of a range, you walk
sideways along the leaves without going back up the tree.

That second property is why range queries are cheap:

```sql
SELECT * FROM orders WHERE created_at BETWEEN '2026-01-01' AND '2026-03-31';
```

Three page reads down to the first matching leaf, then a **sequential** walk along linked leaves. From
[day 010](../day-010-traversal-patterns/README.md), sequential reads are far cheaper than random ones,
so a range scan over a million rows is genuinely fast — and it is the reason `ORDER BY` on an indexed
column needs no sort step, which is often a bigger win than the lookup itself.

Everyone says "B-tree" and means B+ tree. **Saying "it's actually a B+ tree, with the data in the
leaves and the leaves linked" is a cheap, strong signal.**

### What it costs to write

Inserting a key means finding the right leaf — three page reads — and writing into it. If the leaf is
full, it **splits**: half the keys move to a new page, and a key is pushed up to the parent. If the
parent is full too, that splits as well, and in the rare worst case the split propagates to the root
and the tree gains a level.

So a write is a handful of page reads plus one or a few page writes, and occasionally more. That is
the concrete cost behind yesterday's "every index makes writes slower".

The other cost is **fragmentation**. Splits leave pages half full, and random insertion order — random
UUID primary keys, from [day 026](../day-026-strings-revision/README.md) — spreads writes across the
whole tree, so pages fill unevenly and the index grows larger than the data it indexes. Sequential
keys append to the rightmost leaf, which stays in cache and fills completely. **That is the real reason
`BIGSERIAL` beats random UUIDs**, and it is a much better answer than "UUIDs are bigger".

### The alternative: LSM trees

The natural follow-up is *"is a B-tree always right?"*, and the answer is no.

A **log-structured merge tree** — used by Cassandra, RocksDB, LevelDB and ScyllaDB — takes the opposite
trade. Writes go into an in-memory sorted structure and are appended to a log; when it fills, it is
flushed to disk as one sorted immutable file. Background compaction merges those files.

```
                B-tree                          LSM tree
  writes   random page updates,           sequential appends only
           read-modify-write               (much faster writes)
  reads    3-4 page reads, predictable    may check several files
                                           (bloom filters help; still slower)
  space    fragmentation from splits      write amplification from compaction
  best for read-heavy, ranges, OLTP       write-heavy, time series, logs
```

**B-trees favour reads; LSM trees favour writes.** Postgres, MySQL, Oracle and SQLite use B-trees.
Cassandra, RocksDB and ScyllaDB use LSM trees. MongoDB's WiredTiger can do either. Naming that
contrast is what turns a textbook answer into a design answer.

---

## 4. The picture

The two shapes, side by side, for the same ten million rows:

```
   BINARY SEARCH TREE                    B+ TREE (fanout ~500)
   one key per node, 24 levels           ~500 keys per node, 3 levels

        (o)          <- page read             +---------------------------+
        / \                                   | 200 | 400 | ... | 99800 |  <- 1 page read
     (o)   (o)       <- page read             +---------------------------+
     / \   / \                                  /        |          \
   (o) (o)(o) (o)    <- page read       +---------+  +---------+  +---------+
    ...                                 |210|...|  |410|...|  |610|...|      <- 1 page read
    ... 24 levels ...                   +---------+  +---------+  +---------+
                                             |
                                        +--------------+--------------+
                                   leaf |211|212|...|249| -> |251|...|  <- 1 page read
                                        +--------------+--------------+
                                          leaves LINKED in order

   24 page reads × 0.1 ms = 2.4 ms       3 page reads × 0.1 ms = 0.3 ms
   uses 24 bytes of each 8 KB page       uses all 8 KB of each page
```

**What to notice:** the comparison count is nearly the same — about 24 either way — but the binary tree
pays a disk read for each one, and the B-tree pays for three. **The unit of cost is the page, not the
comparison.**

Why the fanout is what it is:

```
   one page = 8,192 bytes
   one entry = key (8 bytes) + child pointer (~6) + overhead (~2)  ≈ 16 bytes

   8,192 / 16 ≈ 500 entries per node

   depth 1:            500
   depth 2:        250,000        (500 x 500)
   depth 3:    125,000,000        (500 x 500 x 500)
   depth 4: 62,500,000,000

   A 1,000-fold increase in rows costs ONE extra page read.
```

The range query, which is what the linked leaves are for:

```
   WHERE created_at BETWEEN 'A' AND 'B'

        root      ------------------ 1 page read, navigate down
         |
      internal    ------------------ 1 page read
         |
        leaf  --> leaf --> leaf --> leaf ...
         ^                            ^
       find A                    stop at B

   3 random reads to find the start, then SEQUENTIAL reads along the leaves.
   No going back up the tree. This is why ORDER BY on an indexed column
   needs no sort step at all.
```

---

## 5. How it actually works

### A lookup, step by step

`SELECT * FROM orders WHERE id = 4217` on a ten-million-row table:

1. **Read the root page.** It holds ~500 separated key ranges. Binary-search *within the page*, in
   memory, to find which child covers 4217. One page read, about 9 comparisons.
2. **Read that internal page.** Same again. One page read.
3. **Read the leaf page.** It holds ~500 keys with pointers to rows. Binary-search it, find 4217, get
   the row location. One page read.
4. **Read the table page** holding the row itself. One page read.

**Four page reads total.** And in practice the root and often the whole first internal level are
already in the buffer pool, because they are read constantly — so the real cost is frequently one or
two physical reads.

That caching point is worth making: **the top of the tree is hot by definition**, because every single
lookup goes through it.

### An insert, and the split

1. Navigate to the correct leaf — three page reads.
2. If the leaf has room, insert the key in sorted position and write the page. Done.
3. If it is full, **split**: create a new page, move half the keys into it, and insert a separator key
   into the parent.
4. If the parent is now full, split it too. If that reaches the root, the root splits and **the tree
   grows by one level** — the only way a B-tree gets taller, and it happens from the top, which is what
   keeps every leaf at the same depth.

Splits are why the "at least half full" rule exists: after a split both halves are half full, so there
is room for future inserts without immediately splitting again.

### Why insertion order matters so much

```
sequential keys (BIGSERIAL):
    every insert goes to the RIGHTMOST leaf
    that page stays in cache and fills completely
    -> few splits, dense pages, small index

random keys (UUIDv4):
    every insert goes to a DIFFERENT leaf
    each one must be read from disk, modified, written back
    -> the working set is the whole index, pages half full, index much larger
```

This is the concrete mechanism behind yesterday's advice, and behind
[day 026](../day-026-strings-revision/README.md)'s preference for `BIGSERIAL` or UUIDv7 over random
UUIDv4. **UUIDv7 and ULID put a timestamp in the high bits precisely to restore this locality.**

### Bloating, and what to do about it

Deletions leave pages under-full, and Postgres's MVCC — from
[day 025](../day-025-pattern-matching/README.md) — leaves dead row versions behind. Over time an index
can become several times larger than it needs to be, which means more pages to read, which means
slower.

The fixes: `VACUUM` reclaims space for reuse; `REINDEX CONCURRENTLY` rebuilds an index compactly
without blocking writes. **Index bloat is one of the classic causes of "it got slower and nothing
changed."**

### Page size, and why 8 KB

Not arbitrary. It balances three things: the operating system reads in 4 KB pages, so 8 KB is two of
them; larger pages give higher fanout and shallower trees but waste more when you only want one row;
and the whole page must be written back for any change, so bigger pages mean more write amplification.
Postgres uses 8 KB, InnoDB 16 KB, and both are configurable and almost never changed.

### What else is a B-tree

Worth knowing, because it shows the idea is general: **filesystems** use them — NTFS, ext4's HTree,
XFS, APFS — for exactly the same reason, since a directory lookup is also a disk-bound search. The
constraint produces the same shape wherever it appears.

---

## 6. The numbers

### Depth, and the read cost

```
fanout 500:
   depth 2 :        250,000 rows
   depth 3 :    125,000,000 rows
   depth 4 : 62,500,000,000 rows

binary tree, same 10,000,000 rows: log2(10,000,000) ≈ 24 levels

page reads : 3 vs 24
at 0.1 ms per SSD read : 0.3 ms vs 2.4 ms        -> 8x
at 10 ms per HDD seek  :  30 ms vs 240 ms        -> 8x, and both are terrible
```

The ratio is the same on either device; the absolute numbers are what made this design mandatory in
the disk era and still worthwhile on SSDs.

### Comparisons versus page reads

```
B-tree   : 3 pages × log2(500) ≈ 3 × 9  = 27 comparisons, 3 page reads
binary   : 24 nodes            = 24 comparisons, up to 24 page reads

comparisons: 27 vs 24 — the B-tree does slightly MORE
page reads : 3 vs 24 — the B-tree does 8x FEWER
```

**That table is the answer to the interview question.** The B-tree is not saving comparisons. It is
moving them inside pages you have already paid to fetch.

### Page utilisation

```
binary tree node : 24 bytes used of an 8,192-byte page  = 0.3%
B-tree node      : ~8,000 bytes used of 8,192           = 98%
```

### Index size

```
10,000,000 rows, bigint key:
   entry ≈ 16 bytes
   leaves : 10,000,000 × 16      = 160 MB
   internal levels add ~1/500th   ≈   0.3 MB
   with ~70% average fill          ≈ 230 MB

table itself, 200 bytes/row      = 2 GB
so the index is ~11% of the table
```

### Sequential versus random insertion

```
1,000,000 inserts:

sequential keys : nearly all hit the rightmost leaf, which is cached
                  ≈ 1,000,000 / 500 = 2,000 page writes
random keys     : each hits a different leaf; the working set is the whole index
                  ≈ up to 1,000,000 page read-modify-writes

difference: up to 500x in page I/O, and the index ends up ~30-40% larger
            from half-full pages
```

**That is why sequential ids matter**, stated in a way that survives a follow-up.

### The range scan

```
WHERE created_at BETWEEN A AND B, matching 100,000 rows:

   navigate to the first leaf : 3 random page reads
   walk the linked leaves     : 100,000 × 16 B ≈ 1.6 MB, sequential
   at 500 MB/s               ≈ 3 ms

versus 100,000 independent lookups : 100,000 × 3 page reads = 300,000 random reads ≈ 30 s
```

**Four orders of magnitude**, and it comes entirely from the leaves being linked.

---

## 7. The trade-offs

### B-tree against a hash index

A hash index is `O(1)` for equality and cannot do anything else — no ranges, no `BETWEEN`, no prefix
`LIKE`, no `ORDER BY`. A B-tree is `O(log n)`, but `log₅₀₀` of anything realistic is 3 or 4, so the
"slower" one is slower by nothing measurable and does five extra things.

**That is why Postgres's default is a B-tree and hash indexes are rarely used.** The constant-factor
win does not exist in practice and the lost functionality is real.

### B-tree against an LSM tree

The real trade, and the one worth arguing:

- **B-tree**: predictable reads at 3–4 page reads; in-place updates, so writes are random I/O; space
  lost to fragmentation. Right for read-heavy transactional workloads with range queries.
- **LSM tree**: writes are pure sequential appends, which is dramatically faster; reads may have to
  check several sorted files, mitigated by bloom filters but still slower and less predictable;
  background compaction consumes I/O and causes latency spikes.

**Choose an LSM tree when writes dominate** — time-series, event logs, metrics, sensor data. **Choose a
B-tree when reads and ranges dominate**, which is most transactional applications.

### Higher fanout, or smaller pages

A larger page means higher fanout and a shallower tree — but every modification rewrites the whole
page, so write amplification goes up, and a lookup that wants one 200-byte row fetches 16 KB. 8 KB is
the settled compromise and almost nobody changes it.

### Sequential or random keys

Sequential keys give dense pages, few splits and a cached hot spot. They also create a **write hot
spot**: in a distributed system every insert goes to the same shard, which is exactly what you do not
want. **That is why Cassandra and DynamoDB push you towards randomly-distributed partition keys**, and
why the answer differs between a single Postgres instance and a distributed store. UUIDv7 is the
compromise: roughly ordered for locality, random enough in the low bits to avoid perfect contention.

### The sentence that separates candidates

> **I would not use a binary search tree for anything stored on disk.** The comparison count is
> essentially the same either way — about 24 for ten million rows — but a binary tree pays a page read
> for every one of those comparisons, while a B-tree pays for three and does the other 24 inside pages
> it has already fetched. The unit of cost is the page, not the comparison. In memory, where there is
> no page to fetch, a balanced binary tree is perfectly reasonable and is what an in-memory sorted map
> usually is — the shape follows from where the data lives.

---

## 8. In the interview

### How it gets asked

- *"Why is a database index a B-tree and not a binary search tree?"* — the direct version. The answer is
  about page reads, not about balance.
- *"How many disk reads to find a row in a ten-million-row table?"* — three or four, and you should be
  able to derive it from the fanout.
- *"Why do range queries work on an index but hash lookups don't?"* — the linked leaves.
- *"Why are sequential ids better than random UUIDs for a primary key?"* — page locality and splits.
- *"When would you not use a B-tree?"* — LSM trees, and write-heavy workloads.

### What to say out loud, in the first ninety seconds

1. **Lead with the hardware fact.** *"Because the unit of cost on disk is the page, not the comparison.
   A read fetches 8 KB whether you wanted one byte or all of it, and it costs about 0.1 ms — roughly a
   hundred thousand times a comparison."*
2. **Say what follows from it.** *"So you want to make each page read decide as much as possible. A
   binary node uses 24 bytes of an 8 KB page and makes a two-way decision. A B-tree node fills the page
   with about 500 keys and makes a 500-way decision."*
3. **Give the depths.** *"For ten million rows that's log base 500, so three levels, against log base 2,
   which is 24. Three page reads instead of twenty-four."*
4. **Make the comparison point explicitly.** *"The comparison count is about the same — 27 against 24 —
   so this isn't saving comparisons. It's moving them inside pages I've already paid to fetch."*
5. **Add the B+ detail.** *"And it's really a B+ tree: all the row pointers are in the leaves, so
   internal nodes are smaller and the fanout is higher, and the leaves are linked in order."*
6. **Say what the linking buys.** *"That's why ranges and `ORDER BY` are cheap — find the start, then
   walk sideways sequentially instead of doing independent lookups."*
7. **Name the alternative.** *"If the workload were write-heavy I'd consider an LSM tree instead —
   Cassandra and RocksDB — which turns random writes into sequential appends at the cost of slower,
   less predictable reads."*

### The follow-ups

**"How many disk reads to find one row in a ten-million-row table?"**
Three or four, and I can derive rather than recall it. A page is 8 KB and an index entry is roughly 16
bytes — a key plus a pointer plus overhead — so about 500 entries fit in a page, which is the fanout.
That gives 500 at depth one, 250,000 at depth two, and 125 million at depth three, so ten million rows
needs three levels. Three page reads walks me down to the leaf, and one more fetches the actual table
row, so four. In practice fewer are physical reads, because the root and usually the whole second level
are permanently in the buffer pool — every lookup goes through them, so they are hot by definition. And
if the index covers every column the query needs, the fourth read disappears entirely, because it can
be answered from the leaf without touching the table.

**"Why not just use a balanced binary tree?"**
Because the cost model is wrong for disk. A red-black or AVL tree does `log₂(n)` comparisons, which for
ten million rows is 24 — and that is fine in memory. On disk, each of those 24 nodes is likely on a
different page, so it is 24 page reads at 0.1 ms each, about 2.4 milliseconds, and each read delivers 8
KB of which the node uses about 24 bytes. A B-tree does roughly the same number of comparisons — three
levels times nine comparisons within each page is 27 — but only three page reads, because 24 of those
comparisons happen inside pages already in memory. So the B-tree is not a cleverer search; it is the
same search reorganised so that the expensive operation happens as rarely as possible. In memory, where
there is no page to fetch, a balanced binary tree is entirely reasonable, and that is what an in-memory
sorted map usually is.

**"Why can an index do range queries when a hash index can't?"**
Because a B-tree is sorted and a hash is not. A hash function deliberately scatters similar keys to
unrelated buckets — that is what makes it uniform — so there is no sense in which the entries "next to"
a key are the next values. A B-tree keeps keys in order within each node and orders the children the
same way, and in a B+ tree the leaves are additionally linked left to right. So a range query navigates
down to the first matching leaf in three reads and then walks sideways along linked leaves, reading
sequentially. That is also why `ORDER BY` on an indexed column costs nothing extra — the index already
*is* that order, so the sort step disappears, which for a large result is often a bigger win than the
lookup. It is also why prefix `LIKE 'Ram%'` works and suffix `LIKE '%kumar'` does not: a prefix is a
contiguous range in sorted order and a suffix is not.

**"When would you not use a B-tree?"**
When writes dominate. A B-tree updates pages in place, so a write is a random read-modify-write, and at
very high insert rates that becomes the bottleneck — plus every split fragments the tree. An
LSM tree inverts it: writes go to an in-memory sorted structure and are appended sequentially to a log,
then flushed as immutable sorted files that background compaction merges. Sequential appends are far
faster than random page updates, so write throughput is much higher. The price is on reads — a lookup
may have to check several files, which bloom filters mitigate but do not remove — and compaction
consumes I/O in bursts, so latency is less predictable. So: time-series, event logs and metrics go to
Cassandra or RocksDB; transactional workloads with ranges and predictable read latency stay on a
B-tree, which is Postgres, MySQL, Oracle and SQLite.

### A model answer

> "Because the unit of cost on disk is the page, not the comparison.
>
> A disk read fetches a whole page — 8 KB in Postgres — whether you wanted one byte or all of it, and it
> costs around 0.1 milliseconds on an SSD. A CPU comparison is about a nanosecond. So a page read is
> roughly a hundred thousand times more expensive than a comparison, and any structure that lives on
> disk should be designed to minimise page reads and treat everything inside a page as free.
>
> A binary search tree gets that exactly backwards. Each node holds one key and makes a two-way
> decision, so for ten million rows you need log base 2, which is about 24 levels. If each node is on a
> different page, that's 24 page reads — about 2.4 milliseconds — and each read delivered 8 KB of which
> you used 24 bytes.
>
> A B-tree makes each node exactly one page and fills it. With 8 KB pages and about 16 bytes per entry,
> that's roughly 500 keys per node, so one page read makes a 500-way decision. The depth becomes log
> base 500, which for ten million rows is three levels. Three page reads instead of 24.
>
> The point I'd want to make explicitly is that this isn't saving comparisons. Three levels times about
> nine comparisons inside each page is 27, against 24 for the binary tree — slightly more. What changed
> is that 24 of those comparisons now happen inside pages I've already paid to fetch. The structure was
> reshaped around which operation is expensive.
>
> And the fanout is why the depth barely grows: 500 at one level, 250,000 at two, 125 million at three,
> 62 billion at four. A thousand-fold increase in data costs one extra page read.
>
> In practice it's a B+ tree, with two refinements. All the row pointers live in the leaves, so internal
> nodes carry only keys and the fanout is even higher. And the leaves are linked in order, which is what
> makes ranges cheap — you navigate down once and then walk sideways sequentially, instead of doing an
> independent lookup per row. That's also why `ORDER BY` on an indexed column needs no sort step.
>
> Where I'd reconsider is a write-heavy workload. A B-tree updates pages in place, so writes are random
> I/O and splits fragment it. An LSM tree — Cassandra, RocksDB — turns writes into sequential appends
> and pays for it on reads, which may have to consult several files. So time-series and event logs go
> that way; transactional workloads with ranges stay on a B-tree."

---

## 9. Recall card

- **The unit of cost on disk is the page, not the comparison.** A page read is ~0.1 ms and fetches 8 KB
  whatever you asked for.
- **So make each node one page and fill it.** Fanout ~500, so `log₅₀₀(10M) = 3` levels against
  `log₂(10M) = 24`.
- **It does not save comparisons** — 27 against 24 — **it saves page reads**, 3 against 24.
- **B+ tree: pointers in the leaves, leaves linked in order.** That is what makes ranges and `ORDER BY`
  cheap.
- **Sequential keys fill the rightmost leaf and stay cached; random keys scatter and split.** B-trees
  favour reads; **LSM trees** favour writes.
