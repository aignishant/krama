---
day: 30
track: system-design
title: "Indexes: how a database finds a row fast"
phase: "Databases from zero"
status: written
---

# Day 030 · System Design — Indexes: how a database finds a row fast

**After today you can:** You can explain why an index makes reads fast and writes slower.

**The interviewer asks it as:** *This query is slow. How do you find out why, and what do you do about it?*

---

## 1. What this is, and why they ask it

An **index** is a second structure, stored alongside a table, that maps values of one or more columns
to the rows holding them — kept in sorted order so it can be searched without reading everything.

Without one, finding the rows where `customer_id = 4217` means reading every row and discarding the
ones that do not match. That is a **sequential scan**, and it is `O(n)`. With a B-tree index it is
three or four page reads regardless of table size — the difference between 112 milliseconds and 0.02
on a million rows.

The reason this gets a whole day is the second half, which people miss: **an index is a copy, and every
write has to update it.** A table with eight indexes does nine writes per insert. So indexing is not
free and "index everything" is a real mistake, with a real cost you can quantify.

Interviewers ask *"this query is slow, what do you do?"* in almost every backend interview, and it has
a right shape of answer: **measure first with `EXPLAIN`, then look at the specific thing it tells you.**
Candidates who immediately say "add an index" without asking what the query is get marked down, because
about half the time the problem is something else — an unindexed foreign key, an ORM issuing sixty-one
queries, a function wrapped round the indexed column, or deep `OFFSET` pagination.

---

## 2. The story

The spare parts shop where Nadeem works is one room, and along three walls there are wooden cabinets of
small drawers — six hundred and something drawers, four inches square, holding everything a two-wheeler
mechanic asks for at eight in the morning.

Every drawer has a number painted on the front, and nothing else. Not what is in it. Just a number.

The list is what makes the shop work. It is a long list, ordered by part number, and against each part
number it says a drawer. A man comes in with a part number off the old part, Nadeem runs his eye down
the list — it is in order, so he lands on the right place in about four seconds — and goes straight to
drawer 218.

The alternative is what happened on the day the list went missing, before Nadeem's time, and the owner
still tells the story. They opened drawers. All morning.

There is a second list, and it took the owner two years to agree to it. That one is ordered by the name
of the part — clutch cable, brake shoe, chain sprocket — because half the customers do not have a part
number, they have a broken thing in their hand and a word for it. Without that list, a man who says
"clutch cable" is back to opening drawers, because the first list is in part-number order and a name
tells you nothing about where you are in it.

And here is the thing the owner was right about, which is why he resisted.

Every time a new kind of part comes in, Nadeem has to write it into **both** lists, in the right place
in each, and it has to be the right place or the list is worse than useless. A delivery of forty new
part numbers on a Tuesday is forty entries in one list and forty in the other, and it takes him most of
the afternoon. Two lists means twice the afternoon.

There was talk of a third list, by manufacturer. Nadeem was against it. He says he already spends more
time keeping the lists right than he does finding parts, and finding parts is the job.

---

## 3. The idea in plain English

Nadeem's part-number list is an **index on the part number column**. The name list is a **second index
on a different column**. Opening every drawer is a **sequential scan**. And the Tuesday afternoon is the
**write cost**, which is the half people forget.

### What an index actually is

A **B-tree** — a shallow, wide, always-balanced tree stored on disk, where each node is one disk page.
Each entry holds a value and a pointer to the row that has it.

The critical property is the **fanout**: because a page is 8 KB and an entry is small, one node holds
hundreds of entries. Postgres manages around 500 per page for a typical integer key. So:

```
depth 1 :         500 entries
depth 2 :     250,000
depth 3 : 125,000,000
depth 4 :  62,500,000,000
```

**Three levels covers ten million rows. Four covers sixty billion.** That is why an index lookup is
"three or four page reads" rather than a number that grows with your data — the tree gets *wider*
before it gets deeper, and depth grows like `log₅₀₀(n)`.

Trees properly arrive on [day 098](../day-098-what-a-tree-is/README.md). What you need today is: **it
is sorted, it is shallow, and a lookup is a handful of reads.**

### What an index gives you, beyond equality

Because it is **sorted**, one index serves five different query shapes:

| Query | Uses the index? |
|---|---|
| `WHERE id = 42` | yes — walk down to the value |
| `WHERE age > 30` | yes — find 30, then walk right along the leaves |
| `WHERE age BETWEEN 20 AND 30` | yes — a range scan |
| `ORDER BY created_at` | yes — the index is already in that order, so **no sort needed** |
| `WHERE name LIKE 'Ram%'` | yes — a prefix is a range |
| `WHERE name LIKE '%kumar'` | **no** — a suffix is not a range |

That fourth row is worth pausing on. `ORDER BY` on an indexed column costs nothing, because the index
*is* the order. That is often a bigger win than the lookup, since sorting a million rows means either
`O(n log n)` in memory or a spill to disk.

### The rule that catches everyone: don't wrap the column

```sql
WHERE YEAR(created_at) = 2026        -- index NOT used: sequential scan
WHERE created_at >= '2026-01-01'
  AND created_at <  '2027-01-01'     -- index used
```

The index stores `created_at`, not `YEAR(created_at)`. Once you apply a function, the database has to
compute it for every row to find out which match — so it reads every row. Same for
`WHERE LOWER(email) = 'x'` and `WHERE price * 1.18 > 100`.

**The fix is always the same: rearrange so the bare column is on one side.** Or, when you genuinely
need the function, build an index *on the expression*:

```sql
CREATE INDEX ON users (LOWER(email));
```

This one line accounts for a large share of real-world slow queries, and spotting it in a query someone
shows you is a strong interview signal.

### Composite indexes and the left-prefix rule

An index can cover several columns, and then **order matters enormously**:

```sql
CREATE INDEX ON orders (customer_id, created_at);
```

That index is sorted by `customer_id` first, and by `created_at` within each customer. So it serves:

```
WHERE customer_id = 5                              yes
WHERE customer_id = 5 AND created_at > '2026-01-01' yes — this is what it is FOR
WHERE customer_id = 5 ORDER BY created_at          yes — and no sort step
WHERE created_at > '2026-01-01'                    NO  — created_at is not the first column
```

**An index on `(A, B)` can be used for `A`, and for `A` with `B`, but not for `B` alone.** That is the
**left-prefix rule**, and it is the most-asked detail in this topic.

It is Nadeem's list exactly. A list ordered by part number, then by name within each number, lets you
find a part number instantly and a name within it — and is no help at all if all you have is a name.

An index on `(A, B)` also makes a separate index on `A` redundant, which is a useful thing to notice
when someone shows you six indexes on one table.

### The covering index

If the index contains **every column the query needs**, the database can answer from the index alone
and never read the table row at all. Postgres calls this an *index-only scan*.

```sql
CREATE INDEX ON orders (customer_id, status, amount);

SELECT status, amount FROM orders WHERE customer_id = 5;   -- served entirely from the index
```

On a wide table this is often a 5–10× win, because the index is far smaller than the rows. **And it is
the real argument against `SELECT *`** — from [day 027](../day-027-two-pointers-idea/README.md), asking
for columns you do not need makes a covering index impossible.

### Selectivity: when an index is worse than useless

An index on a column with two distinct values — `is_active`, where 95% of rows are `true` — will not be
used for `WHERE is_active = true`, and the planner is right to refuse.

Reading 950,000 rows through an index means 950,000 **random** reads scattered across the table.
Reading the whole table sequentially is 200 MB in one continuous sweep. From
[day 010](../day-010-traversal-patterns/README.md), sequential reads are far faster per byte than
random ones, so beyond roughly 5–10% of the table, **the scan wins**.

**High selectivity — many distinct values — is what makes an index worth having.** Email addresses and
user ids: excellent. Booleans and status columns with three values: usually not, on their own.

The exception is a **partial index**, which is often the right answer for exactly that case:

```sql
CREATE INDEX ON orders (created_at) WHERE status = 'pending';
```

If 1% of orders are pending, this index is 1% of the size, and it is highly selective for the query
that matters.

### The cost: every write updates every index

This is Nadeem's Tuesday.

- **`INSERT`** — one row written, plus one entry inserted into every index on the table.
- **`UPDATE`** — the row, plus every index on a column you changed. In Postgres, an update writes a new
  row version, so it often touches **all** the indexes.
- **`DELETE`** — the row, plus an entry removed from every index.

So a table with eight indexes does roughly nine writes per insert. In practice that is three to five
times slower than an unindexed table, plus the storage.

**"Index everything" is the mistake this fact prevents.**

---

## 4. The picture

A B-tree, and why the depth barely grows:

```
                    +---------------------------+
        root        |  200 | 400 | 600 |  800   |          1 page read
                    +---------------------------+
                     /      |      |       \
          +--------+   +--------+  +--------+  +--------+
 internal |210|250 |   |410|450|   |610|650|   |810|850 |   1 page read
          +--------+   +--------+  +--------+  +--------+
            /    \
     +----------+  +----------+
leaf |211|...|249|  |251|...|  ... sorted, and linked left-to-right   1 page read
     +----------+  +----------+
        |    |
        v    v
      the actual rows in the table

   fanout ~500 per page:
     depth 3 covers 125,000,000 rows
     depth 4 covers  62,500,000,000 rows
```

**What to notice:** the leaves are linked to each other in order. That is what makes `>`, `BETWEEN` and
`ORDER BY` work — find the start, then walk sideways. An index is not just a lookup table; it is a
**sorted** lookup table, and half its value is the sortedness.

Scan versus index, on a million rows:

```
   SEQUENTIAL SCAN                       INDEX SCAN
   read every page, discard non-matches  walk down, then read the rows

   [][][][][][][][][][][][][][][] ...      root
   [][][][][][][][][][][][][][][] ...       |
   [][][][][][][][][][][][][][][] ...     internal
   ... 25,000 pages, 200 MB                 |
                                          leaf  --> 3 matching row pointers
   112 ms                                 0.02 ms
   999,997 rows read and thrown away      3 rows read
```

The left-prefix rule, drawn as the sort order:

```
   index on (customer_id, created_at) — sorted by the first, then the second

   customer_id | created_at
   ------------+------------
        5      | 2026-01-04     <-- all of customer 5 is together,
        5      | 2026-02-11         and in date order within that
        5      | 2026-03-02
        7      | 2026-01-09
        7      | 2026-05-20
        9      | 2026-01-01
        9      | 2026-04-15

   WHERE customer_id = 5                    -> jump straight to the block. YES
   WHERE customer_id = 5 AND created_at > X -> jump, then walk. YES
   WHERE customer_id = 5 ORDER BY created_at-> already ordered. YES, no sort
   WHERE created_at > '2026-04-01'          -> the dates are scattered
                                               through the whole index. NO
```

**What to notice:** the dates are only sorted *within* a customer. Globally they are all over the place,
which is why the index cannot help a query that filters on the date alone.

---

## 5. How it actually works

### Finding out why a query is slow

Always start here. `EXPLAIN` shows the plan; `EXPLAIN ANALYZE` runs it and shows what actually
happened.

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 4217;
```

```
Seq Scan on orders  (cost=0.00..18334.00 rows=1 width=64)
                    (actual time=0.021..112.4 rows=3 loops=1)
  Filter: (customer_id = 4217)
  Rows Removed by Filter: 999997
```

Four things to read, in order:

1. **`Seq Scan` on a large table with a filter** — the headline problem. It read a million rows to
   return three.
2. **`Rows Removed by Filter: 999997`** — confirms it, and quantifies how much work was wasted.
3. **Estimated `rows=1` versus actual `rows=3`** — close enough. A large gap here means stale
   statistics, and `ANALYZE orders;` may fix the plan without any schema change.
4. **`actual time`** — where the time really went, as opposed to where the cost model guessed.

Add the index:

```sql
CREATE INDEX CONCURRENTLY ON orders (customer_id);
```

```
Index Scan using orders_customer_id_idx on orders
  (cost=0.42..8.45 rows=3 width=64) (actual time=0.018..0.024 rows=3 loops=1)
  Index Cond: (customer_id = 4217)
```

`CONCURRENTLY` matters in production: a plain `CREATE INDEX` takes a lock that blocks writes to the
table for the whole build, which on a large table is minutes of downtime. `CONCURRENTLY` is slower and
does not block. **Mentioning it unprompted is a strong operational signal.**

### The scan types you will see

| Node | Means |
|---|---|
| `Seq Scan` | read the whole table. Fine on small tables, the thing to fix on large ones. |
| `Index Scan` | walk the index, then fetch each matching row. |
| `Index Only Scan` | answered entirely from the index — a covering index. The best case. |
| `Bitmap Heap Scan` | many matches: collect their locations first, sort them, then read the table in page order. Postgres chooses this between "a few rows" and "most rows". |
| `Nested Loop` / `Hash Join` / `Merge Join` | the join algorithms from [day 028](../day-028-opposite-ends/README.md). |

**`Bitmap Heap Scan` is worth understanding**, because people see it and assume something is wrong. It
is the planner being clever: rather than making 50,000 random row reads in index order, it gathers the
page numbers, sorts them, and reads the table in physical order — turning random I/O into something
closer to sequential.

### The six causes of a slow query

Have this list. It is the answer to the interview question.

1. **A missing index** — `Seq Scan` with a high "Rows Removed". Add one.
2. **A function wrapped round the column** — `WHERE YEAR(x) = 2026`. Rewrite as a range, or index the
   expression.
3. **An unindexed foreign key** — from [day 026](../day-026-strings-revision/README.md), primary keys
   are indexed automatically and foreign keys are not. This shows up as a slow join or a slow delete.
4. **N+1 queries from an ORM** — the plan looks fine because each individual query *is* fine; there are
   just sixty-one of them. You find this in the application log, not in `EXPLAIN`.
5. **Deep `OFFSET` pagination** — `OFFSET 1000000` generates and discards a million rows. Use a keyset
   cursor.
6. **A sort or hash aggregate spilling to disk** — `Sort Method: external merge Disk: 52000kB` in the
   plan. Either raise `work_mem` or add an index that provides the order.

### Index types beyond B-tree

Know that they exist and roughly what each is for:

- **B-tree** — the default. Equality, ranges, ordering, prefixes. Covers 95% of needs.
- **Hash** — equality only, no ranges. Rarely worth it in Postgres, since B-tree is nearly as fast for
  equality and does far more.
- **GIN** — for columns containing many values: full-text search, `JSONB`, arrays. `WHERE tags @> '{sql}'`.
- **GiST** — geometric and range types. "Points within 5 km of here."
- **BRIN** — tiny indexes for huge tables where the data is physically ordered, such as append-only
  time-series. Stores a summary per block rather than an entry per row.

### Writing indexes for a real workload

The practical procedure:

1. **Find the slow queries.** `pg_stat_statements` ranks them by total time — which surfaces the query
   that takes 20 ms and runs a million times a day, and that is usually the real problem rather than
   the 2-second report that runs nightly.
2. **`EXPLAIN ANALYZE` each one.**
3. **Index the columns in `WHERE`, `JOIN` and `ORDER BY`**, most selective first in a composite.
4. **Check for redundancy.** An index on `(A, B)` makes one on `(A)` unnecessary.
5. **Find unused indexes** — `pg_stat_user_indexes` shows scan counts; an index with zero scans is
   pure write cost, and dropping it is free speed.

---

## 6. The numbers

### Scan against index lookup

1,000,000 orders at about 200 bytes:

```
table size                       = 200 MB = ~25,000 pages of 8 KB
sequential scan @ 500 MB/s       ≈ 400 ms of I/O, ~112 ms when cached
index scan: 3 B-tree pages + 3 row pages = 6 page reads ≈ 0.02 ms
```

**About 5,000×.** And it gets better with size: at 10 million rows the scan is ten times slower and the
index scan is unchanged, because the tree gained no depth.

### Depth against table size

```
fanout ~500 per 8 KB page:

       1,000 rows -> 2 levels
     250,000 rows -> 2 levels
  10,000,000 rows -> 3 levels
 100,000,000 rows -> 4 levels
```

**A thousand-fold increase in data costs you one extra page read.** That is the single most persuasive
fact about B-trees.

### The write cost

```
table with 0 indexes : 1 write per insert
table with 1 index   : 2 writes
table with 8 indexes : 9 writes

measured effect: roughly 3-5x slower inserts with 8 indexes than with none
```

At 1,000 inserts a second:

```
0 indexes : 1,000 writes/s
8 indexes : 9,000 writes/s of index maintenance
```

### Storage

```
1,000,000 rows, index on a bigint column:
  ~16 bytes per entry (key + pointer + overhead)
  1,000,000 × 16 B ≈ 16 MB, plus tree overhead ≈ 25 MB

table itself : 200 MB
one index    :  25 MB   (12%)
eight indexes: 200 MB   (100% — the indexes now cost as much as the data)
```

### Selectivity: where the scan wins

```
1,000,000 rows, matching:
        10 rows (0.001%) : index scan, 10 random reads       — obviously index
    10,000 rows   (1%)   : index or bitmap scan              — index
   100,000 rows  (10%)   : bitmap heap scan                  — borderline
   500,000 rows  (50%)   : sequential scan                   — obviously scan
```

The crossover is roughly **5–10%** of the table, and the reason is that index scans produce random
reads while a sequential scan is one continuous sweep. From
[day 010](../day-010-traversal-patterns/README.md), the ratio between random and sequential access is
what drives the whole decision.

### The covering index

```
orders row : 200 bytes
index on (customer_id, status, amount) : ~32 bytes per entry

query needing only those three columns, 10,000 matching rows:
   index scan + row fetch : 10,000 random row reads ≈ 2,000,000 bytes touched
   index only scan        : ~320,000 bytes, sequential within the index
                            about 6x less I/O, and no random access
```

### `OFFSET` pagination, again

```
LIMIT 20 OFFSET 0        ≈    1 ms
LIMIT 20 OFFSET 1,000,000 ≈ 2,000 ms   — a million rows generated and discarded
keyset: WHERE id > :last ORDER BY id LIMIT 20 ≈ 1 ms at any depth
```

---

## 7. The trade-offs

### Read speed against write speed and storage

The whole subject in one line. Each index makes some reads dramatically faster and every write on that
table slower, and costs 10–25% of the table's size.

**Index the columns your real queries filter, join and sort on. Then measure, and drop what is not
used.** `pg_stat_user_indexes` tells you which have never been scanned, and dropping those is free
speed with no downside.

### Composite or several single-column indexes

A composite `(A, B)` is much better than separate indexes on `A` and `B` for a query filtering on both,
because it goes straight to the matching block instead of combining two result sets. It is also useless
for a query on `B` alone.

**Rule: build composites for the query shapes you actually run, most selective column first**, and
remember that `(A, B)` already covers `A`.

### Selective or not

A boolean or a three-value status column is a poor index on its own — the planner will ignore it and be
right. **A partial index is usually the better tool**: index only the rows matching a condition, which
is both small and highly selective for the query that matters.

### When to add the index

Adding an index to a live table takes a lock unless you use `CONCURRENTLY`, and on a large table a
plain `CREATE INDEX` can block writes for minutes. `CONCURRENTLY` is slower and safe. **Say this — it
is the difference between someone who has added an index in production and someone who has read about
it.**

### Index, or fix the query

Often the real answer is not an index at all: a function wrapped round the column, an ORM issuing
sixty-one queries, `SELECT *` defeating a covering index, or `OFFSET 1000000`. **Check those before
adding anything**, because an index is permanent write cost and a query fix is free.

### The sentence that separates candidates

> **I would not add an index before running `EXPLAIN ANALYZE`.** Roughly half the slow queries I have
> seen were not missing an index — they had a function wrapped round the indexed column, or an ORM
> issuing sixty-one queries where one would do, or a deep `OFFSET` discarding a million rows. Those are
> free to fix and an index is not: it is 10–25% of the table in storage and a permanent tax on every
> insert, update and delete. And when I do add one on a live table, it is `CREATE INDEX CONCURRENTLY`,
> because the plain form holds a lock that blocks writes for the length of the build.

---

## 8. In the interview

### How it gets asked

- *"This query is slow. What do you do?"* — the main event. The first word of the answer should be
  "measure".
- *"How does an index actually work?"* — B-tree, fanout, three levels for ten million rows.
- *"What's the downside of adding an index?"* — write cost and storage, quantified.
- *"You have an index on `(a, b)`. Does it help `WHERE b = 5`?"* — the left-prefix rule, and the answer
  is no.
- *"Why isn't my index being used?"* — a function on the column, low selectivity, or stale statistics.

### What to say out loud, in the first ninety seconds

1. **Measure before guessing.** *"First I'd run `EXPLAIN ANALYZE` on it, because 'slow' has about six
   different causes and they need different fixes."*
2. **Say what you are looking for.** *"A `Seq Scan` on a big table with a high 'Rows Removed by Filter'
   means a missing index. A big gap between estimated and actual rows means stale statistics. A sort
   spilling to disk means the grouping exceeded `work_mem`."*
3. **Name the causes that are not missing indexes.** *"I'd also check for a function wrapped round the
   column, which stops any index being used; an unindexed foreign key; an ORM doing N+1; and deep
   `OFFSET` pagination."*
4. **Explain the index if asked.** *"It's a B-tree — sorted, and shallow because the fanout is about
   500 entries per page, so three levels covers ten million rows. A lookup is three or four page reads
   instead of scanning 200 MB."*
5. **Say what else sortedness buys.** *"It also serves ranges, `BETWEEN`, prefix `LIKE`, and `ORDER BY`
   with no sort step — which is often the bigger win."*
6. **Give the cost, unprompted.** *"The price is that every insert, update and delete has to maintain
   every index — eight indexes means nine writes per insert — plus 10 to 25% of the table in storage."*
7. **Mention `CONCURRENTLY`.** *"And on a live table I'd use `CREATE INDEX CONCURRENTLY`, because the
   plain form locks out writes for the whole build."*

### The follow-ups

**"You have an index on `(customer_id, created_at)`. Does it help `WHERE created_at > '2026-01-01'`?"**
No, and the reason is the left-prefix rule. The index is sorted by `customer_id` first and by
`created_at` only within each customer, so globally the dates are scattered all through it — there is no
contiguous block of "everything after January". The index can serve `customer_id` alone, or
`customer_id` together with `created_at`, or `customer_id` with an `ORDER BY created_at` and no sort
step, but never `created_at` on its own. For that query I would need a separate index with `created_at`
first. Worth adding: the composite already covers any query on `customer_id` alone, so a separate index
on just `customer_id` would be redundant, and I would drop it if it existed.

**"Why isn't my index being used?"**
Four common reasons and I would check them in this order. First, a function or expression wrapped
around the column — `WHERE YEAR(created_at) = 2026` or `WHERE LOWER(email) = ...` — because the index
stores the raw column, not the computed value, so the database must compute it per row. The fix is to
rewrite as a range, or create an index on the expression itself. Second, low selectivity: if the
condition matches more than roughly 5 to 10 per cent of the table, the planner deliberately prefers a
sequential scan, because an index scan there means hundreds of thousands of random reads while a scan
is one continuous sweep — and it is right to. Third, stale statistics: if the planner thinks a
condition matches one row and it actually matches half the table, it will choose badly, and `ANALYZE`
fixes it. Fourth, a type mismatch — comparing a `bigint` column to a string literal can prevent the
index being used in some databases.

**"What's the actual cost of adding an index?"**
Three costs. Storage: roughly 10 to 25 per cent of the table per index, so eight indexes on a 200 MB
table is another 200 MB. Write throughput: every insert adds an entry to every index, so eight indexes
means nine writes per insert, and in practice inserts run three to five times slower than on an
unindexed table. Updates are worse in Postgres, because an update writes a new row version and often
has to touch every index rather than only the changed columns. And there is an operational cost:
building it on a live table takes a lock that blocks writes unless you use `CONCURRENTLY`. Against all
that, the read win can be several thousand-fold, which is why the answer is to index the columns your
real queries actually use and then check `pg_stat_user_indexes` for ones that have never been scanned —
those are pure cost.

**"The query does `SELECT * FROM orders WHERE status = 'pending'` and status has three values."**
A plain index on `status` will probably be ignored, and correctly so if pending is a large share of the
table. But if pending is a small share — which it usually is, since orders move out of that state — a
**partial index** is the right tool: `CREATE INDEX ON orders (created_at) WHERE status = 'pending'`.
It only contains the pending rows, so it is perhaps one per cent of the size, it is cheap to maintain
because most inserts do not qualify, and it is highly selective for exactly the query that matters. I
would also change the `SELECT *`: naming the columns lets the index cover the query, so it can be
answered without touching the table rows at all, which on a wide table is another five to ten times
less I/O.

### A model answer

> "Before changing anything I'd run `EXPLAIN ANALYZE` on the query, because 'slow' has several
> different causes and they want different fixes.
>
> What I'm reading in the plan: is there a `Seq Scan` on a large table, and what does 'Rows Removed by
> Filter' say? If it read a million rows to return three, that's a missing index and it's the headline
> problem. I'd also compare the estimated row count with the actual — a big gap means the statistics
> are stale and `ANALYZE` might fix the plan by itself. And I'd look for a sort or hash aggregate
> spilling to disk, which means the operation exceeded `work_mem`.
>
> But I'd check three things that aren't missing indexes before adding one, because they're free to
> fix. Is there a function wrapped round the column — `WHERE YEAR(created_at) = 2026` — which stops any
> index being used, since the index stores the raw value? Is this actually one slow query, or is an ORM
> issuing sixty-one of them, which `EXPLAIN` won't show me? And is it deep `OFFSET` pagination, where
> `OFFSET 1000000` generates and throws away a million rows?
>
> If it really is a missing index: an index is a B-tree, so it's sorted and it's shallow. The fanout is
> around 500 entries per 8 KB page, which means three levels covers ten million rows and four covers
> sixty billion — so a lookup is three or four page reads whatever the table size, against reading 200
> MB. That's roughly five thousand times on a million rows.
>
> Because it's sorted, the same index also serves ranges, `BETWEEN`, prefix `LIKE`, and `ORDER BY` with
> no sort step at all — and that last one is often the bigger win, since sorting a million rows
> otherwise means a spill to disk.
>
> The cost is real and I'd state it: every insert, update and delete has to maintain every index, so
> eight indexes means nine writes per insert and inserts three to five times slower, plus 10 to 25 per
> cent of the table in storage each. So I'd index what the real queries filter, join and sort on, and
> then check `pg_stat_user_indexes` for indexes that have never been scanned — those are pure write
> cost and dropping them is free speed.
>
> And on a live table I'd use `CREATE INDEX CONCURRENTLY`. The plain form takes a lock that blocks
> writes for the entire build, which on a large table is minutes of downtime."

---

## 9. Recall card

- **An index is a sorted B-tree kept alongside the table.** Fanout ~500, so **three levels covers ten
  million rows** — a lookup is 3–4 page reads, not a 200 MB scan.
- **Sortedness buys ranges, `BETWEEN`, prefix `LIKE` and free `ORDER BY`** — often the bigger win.
- **Left-prefix rule:** an index on `(A, B)` serves `A` and `A+B`, never `B` alone.
- **Every write updates every index.** Eight indexes = nine writes per insert, and 10–25% storage each.
- **Measure first.** `EXPLAIN ANALYZE`, and check for a function on the column, an N+1, or deep
  `OFFSET` before adding anything. On a live table, `CREATE INDEX CONCURRENTLY`.
