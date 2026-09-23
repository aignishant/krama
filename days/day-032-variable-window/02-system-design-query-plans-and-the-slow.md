---
day: 32
track: system-design
title: "Query plans and the slow query"
phase: "Databases from zero"
status: written
---

# Day 032 · System Design — Query plans and the slow query

**After today you can:** You can read an EXPLAIN output and say which part of the query is the problem.

**The interviewer asks it as:** *Here is an EXPLAIN plan. What is wrong with this query?*

---

## 1. What this is, and why they ask it

SQL is declarative — from [day 027](../day-027-two-pointers-idea/README.md), you say *what* you want
and the database decides *how*. The thing that decides is the **query planner**, and the decision it
produces is the **query plan**: a tree of physical operations, chosen from many possible ones, that
together answer your query.

The planner chooses by **estimating**. It keeps statistics about each table — how many rows, how many
distinct values in each column, the most common values — and uses them to guess how many rows each step
will produce. Then it costs the alternatives and picks the cheapest.

Which means the plan can be wrong in exactly one way: **the estimates can be wrong.** A planner that
believes a filter matches one row will happily choose a strategy that is catastrophic when it actually
matches half a million. And the way you find out is `EXPLAIN ANALYZE`, which shows the estimate and the
reality side by side.

Interviewers ask this because it is the most practical database skill there is. Every backend engineer
meets a slow query in their first month. The bad answer is "add an index", offered before looking. The
good answer is a **procedure**: run `EXPLAIN ANALYZE`, read the plan from the inside out, find where the
row counts explode or the estimate diverges from reality, and fix *that*. Roughly half the time it is
not a missing index at all.

---

## 2. The story

Ramanathan does the errands on Saturday morning because his wife works, and he has got it down to a
system.

He works out the order before he leaves. Bank first, because he thinks that takes ten minutes; then
the electricity office, twenty; then the vegetable market on the way back, fifteen; then the tailor,
five. Forty-five minutes plus the riding, back by ten, and he plans the route around that order so he
is never doubling back.

The plan is a good plan. It is the right order given what he believes.

The Saturday it went wrong, he got to the bank at half past eight and there were about seventy people
outside it, because it was the first Saturday of the month and everybody's pension had come in. He was
in that queue for an hour and forty minutes. By the time he got out, the electricity office had shut
for lunch, so he had to go back in the afternoon, and by then the tailor had closed as well.

The thing he says about it, and he is right, is that the plan was not the mistake. Ten minutes for the
bank was the mistake. Everything downstream — the order, the route, the timing — followed correctly
from a number that happened to be wrong by a factor of ten.

His son asked him afterwards how he could have known, and Ramanathan said the honest thing: he
couldn't have, not from where he was standing. But he could have found out. The bank has a board
outside with the pension dates on it and he has walked past it four hundred times.

Now he does two things. Before he leaves, he checks the two or three things that change — is it pension
week, is there a strike, is it the end of the quarter at the electricity office. And afterwards, if it
took longer than he thought, he makes himself say where the time actually went, out loud, rather than
just saying it was a bad morning. He says the second one has taught him more, because his guesses about
the tailor were wrong for six years and he never once noticed.

---

## 3. The idea in plain English

Ramanathan's order of errands is the **query plan**. His ten-minutes-for-the-bank is a **row estimate**.
Checking the pension board before leaving is **`ANALYZE`**, which refreshes the statistics. And making
himself say where the time actually went is **`EXPLAIN ANALYZE`**.

### What the planner is actually doing

For a query like `SELECT ... FROM a JOIN b ... WHERE ...`, the planner must choose:

- **How to read each table** — sequential scan, index scan, index-only scan, bitmap scan.
- **Which join algorithm** — nested loop, hash join, merge join, from
  [day 028](../day-028-opposite-ends/README.md).
- **In what order to join** — with three tables there are twelve possible orderings, and the choice can
  change the cost by orders of magnitude.
- **Where to filter and where to sort.**

It enumerates the plausible combinations, assigns each a **cost** — an abstract number, not
milliseconds — and picks the smallest. The cost model weighs sequential page reads, random page reads,
CPU per row and CPU per operator.

**Everything depends on knowing how many rows each step produces.** That comes from the statistics.

### The statistics

Postgres stores, per column: the number of distinct values, the fraction that are null, a list of the
most common values with their frequencies, and a histogram of the rest. They are refreshed by
`ANALYZE`, which autovacuum runs automatically — but not instantly, and not after a bulk load unless
you ask.

From those numbers the planner estimates **selectivity**: what fraction of rows a condition keeps.

```
WHERE status = 'pending'
  status has 4 distinct values, 'pending' is 3% by the most-common-values list
  -> estimate 3% of 1,000,000 = 30,000 rows
```

**Stale statistics are the single most common cause of a bad plan**, and the fix is one command.

### Reading a plan

Two rules make plans readable, and without them they are impenetrable.

**Read from the inside out — the most indented lines run first.** The output is a tree printed with the
root at the top, so execution goes bottom-up.

**Every line has the same shape:**

```
Node Type  (cost=START..TOTAL rows=EST width=BYTES)
           (actual time=START..TOTAL rows=ACTUAL loops=N)
```

- **`cost=0.42..8.45`** — the planner's abstract estimate. The first number is the cost to produce the
  *first* row, the second to produce *all* of them. The first number matters for `LIMIT` queries.
- **`rows=`** in the cost line is the **estimate**; `rows=` in the actual line is the **truth**.
- **`loops=N`** — this node ran N times. **The `actual time` is per loop, so multiply.** This is the
  single most misread field in the whole output.

`EXPLAIN` shows only the estimates. **`EXPLAIN ANALYZE` actually runs the query** and adds the actual
line — which means it also executes any `UPDATE` or `DELETE`, so wrap those in a transaction you roll
back.

### The four things to look for, in order

**1. Estimate versus actual.** If `rows=1` estimated and `rows=480000` actual, everything downstream
was chosen for the wrong problem. This is the first thing to check and the most valuable. Fix:
`ANALYZE`, or increase the statistics target on that column.

**2. A `Seq Scan` on a large table with a filter.** Look for `Rows Removed by Filter`. Reading a
million rows to return three is a missing index.

**3. `loops=` greater than one on a large node.** A nested loop running its inner side sixty-one times
is often an ORM N+1 problem or a bad join order.

**4. Anything that says `Disk`.** `Sort Method: external merge Disk: 52000kB` means the operation
exceeded `work_mem` and spilled. Either raise `work_mem` for that session or give it an index that
provides the order.

### The scan nodes, and what each means

| Node | What it is doing | When it is right |
|---|---|---|
| `Seq Scan` | read every page of the table | small tables, or when returning most rows |
| `Index Scan` | walk the index, then fetch each row | few matching rows |
| `Index Only Scan` | answered from the index alone | the index covers every column needed — the best case |
| `Bitmap Heap Scan` | collect row locations, sort them, read pages in order | many matches — turns random reads into sequential ones |

**`Bitmap Heap Scan` is not a problem.** People see it and assume something is wrong; it is the planner
being clever in the middle ground where an index scan would do too many random reads and a sequential
scan would read too much.

### The six causes of a slow query

The list from [day 030](../day-030-fast-and-slow/README.md), now with what each looks like in a plan:

| Cause | In the plan | Fix |
|---|---|---|
| missing index | `Seq Scan` + high `Rows Removed by Filter` | add the index |
| function on the column | `Seq Scan` despite an index existing | rewrite as a range, or index the expression |
| stale statistics | estimated rows wildly different from actual | `ANALYZE` |
| N+1 from an ORM | each plan looks fine; there are just 61 of them | eager loading — not visible in `EXPLAIN` |
| deep `OFFSET` | `Limit` with a huge `rows` beneath it | keyset pagination |
| spilling to disk | `Sort Method: external merge Disk:` | raise `work_mem`, or index the sort column |

**Two of those six do not appear in the plan at all.** The N+1 is invisible because each individual
query is fine, and you find it in the application log or in `pg_stat_statements`. That is worth saying
in an interview, because it is the one people never mention.

---

## 4. The picture

A plan, annotated:

```
   Sort  (cost=1250.30..1252.80 rows=1000 width=68)
         (actual time=45.2..45.6 rows=987 loops=1)                 <- runs LAST
     Sort Key: o.created_at DESC
     Sort Method: quicksort  Memory: 128kB                         <- in memory: good
     ->  Hash Join  (cost=25.10..1200.45 rows=1000 width=68)
                    (actual time=0.8..42.1 rows=987 loops=1)
           Hash Cond: (o.customer_id = c.id)
           ->  Seq Scan on orders o  (cost=0.00..1100.00 rows=50000 width=40)
                                     (actual time=0.01..20.4 rows=50000 loops=1)
                 Filter: (status = 'completed')
                 Rows Removed by Filter: 950000                    <- READ THIS
           ->  Hash  (cost=20.00..20.00 rows=400 width=32)
                     (actual time=0.7..0.7 rows=400 loops=1)
                 ->  Seq Scan on customers c (rows=400)            <- runs FIRST

   read bottom-up:  scan customers -> build hash -> scan orders -> join -> sort
```

**What to notice:** `Rows Removed by Filter: 950000`. The orders scan read a million rows and threw away
95% of them. That is the line that tells you where the 20 milliseconds went, and it is the argument for
an index on `status` — or better, a partial index on the pending rows only.

Estimate against actual, and why a bad estimate poisons everything downstream:

```
   BAD ESTIMATE                              WHAT ACTUALLY HAPPENED
   ------------                              ----------------------
   Nested Loop  (rows=1)                     Nested Loop (actual rows=480000)
     ->  Index Scan on a  (rows=1)             ->  Index Scan on a (actual rows=480000)
     ->  Index Scan on b  (rows=1 loops=1)     ->  Index Scan on b (loops=480000)  <-- !!
                                                                     ^^^^^^^^^^^^
   "one row from a, so one lookup in b —      480,000 index lookups instead of one.
    a nested loop is obviously cheapest"      A hash join would have been right.

   The plan was correct given the estimate. The estimate was wrong.
```

**What to notice:** this is Ramanathan's bank queue exactly. The plan followed correctly from a number
that was wrong by a factor of half a million, and the fix is not to change the plan — it is to fix the
number, with `ANALYZE`.

The `loops` trap:

```
   ->  Index Scan on orders  (actual time=0.02..0.05 rows=3 loops=61)

   "0.05 ms — that's fine"        WRONG
   actual time is PER LOOP.
   real total = 0.05 x 61 = 3.05 ms, and 61 round trips.

   loops=61 on a table you expected to touch once
   almost always means an N+1 or a nested loop over too many rows.
```

---

## 5. How it actually works

### The procedure, in order

**1. Find the right query first.** Do not optimise the one somebody complained about; optimise the one
consuming the most time.

```sql
SELECT query, calls, total_exec_time, mean_exec_time
FROM   pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

`total_exec_time`, not `mean_exec_time`. **A 20 ms query called a million times a day costs far more
than a 2-second report run nightly**, and the 20 ms one is usually the real problem. Sorting by the mean
is how people spend a week optimising something that runs once.

**2. `EXPLAIN ANALYZE` it**, with `BUFFERS` for the I/O picture:

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

`Buffers: shared hit=12 read=8340` — "hit" came from the cache, "read" came from disk. A high `read`
count is where the time is.

**3. Read bottom-up and find the biggest `actual rows` and the biggest `actual time`.**

**4. Check estimate against actual at every level.** The first place they diverge badly is usually the
root cause; everything above it inherited the mistake.

**5. Apply the specific fix**, then re-run and compare.

### Fixing each cause

**Stale statistics.**

```sql
ANALYZE orders;
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;   -- default is 100
```

Raising the statistics target makes the histogram finer, which helps on columns with skewed
distributions. Postgres also supports **extended statistics** for correlated columns — if `city` and
`pincode` are related, the planner otherwise multiplies their selectivities as if independent and
underestimates badly:

```sql
CREATE STATISTICS orders_city_pin (dependencies) ON city, pincode FROM orders;
```

**A function on the column.**

```sql
-- before: Seq Scan, even though created_at is indexed
WHERE DATE(created_at) = '2026-03-01'
-- after: Index Scan
WHERE created_at >= '2026-03-01' AND created_at < '2026-03-02'
```

Or index the expression: `CREATE INDEX ON orders (DATE(created_at));`

**Deep pagination.**

```sql
-- before: Limit over a node with rows=1000020
LIMIT 20 OFFSET 1000000
-- after
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20
```

The row-comparison syntax `(a, b) < (x, y)` handles the tie-break correctly in one condition, which is
neater than the `OR` version people usually write.

**Spilling to disk.**

```sql
SET work_mem = '64MB';         -- for this session only
```

Or add an index that provides the order, so the sort disappears entirely rather than being made faster.

**The N+1.** Not visible in any plan. You find it by counting queries per request in the application
log, and you fix it in the ORM with eager loading — `select_related`/`prefetch_related` in Django,
`includes` in Rails, `joinedload` in SQLAlchemy.

### Making the planner do something else

Postgres deliberately has no query hints. What you can do:

- **`ANALYZE`** — fix the estimates, which fixes the plan properly.
- **Rewrite the query** — `EXISTS` instead of `IN`, a lateral join, a CTE.
- **`SET enable_seqscan = off`** — a diagnostic sledgehammer, useful to *ask* "what would you do
  otherwise, and what did you think it would cost?" Never leave it on in production.
- **Materialise a CTE deliberately** — in Postgres 12+, `WITH x AS MATERIALIZED (...)` forces the old
  behaviour of computing it once.

**The absence of hints is a design position**: the Postgres view is that a hint freezes a decision that
should adapt as the data changes. Oracle and SQL Server disagree and provide them. Knowing that this is
a deliberate disagreement rather than a missing feature is a good signal.

### `EXPLAIN` versus `EXPLAIN ANALYZE`

`EXPLAIN` plans without running: instant, safe, estimates only. `EXPLAIN ANALYZE` **executes the
query** — so it takes as long as the query does, and on an `UPDATE` or `DELETE` it really updates or
deletes. Wrap it:

```sql
BEGIN;
EXPLAIN ANALYZE DELETE FROM orders WHERE id = 5;
ROLLBACK;
```

---

## 6. The numbers

### What a bad estimate costs

10,000 customers, 1,000,000 orders. The planner estimates a filter yields 1 row; it actually yields
480,000.

```
plan chosen: nested loop
   estimated : 1 outer row  x 1 index lookup  = 1 lookup       ≈ 0.02 ms
   actual    : 480,000 outer rows x 1 lookup  = 480,000 lookups
               480,000 × 0.02 ms                                ≈ 9.6 seconds

plan it would have chosen with correct estimates: hash join
   build hash on 10,000 rows + scan 1,000,000                   ≈ 0.3 seconds
```

**Thirty times slower, from one wrong number.** `ANALYZE` takes a few seconds and fixes it. This is the
most important arithmetic in the lesson.

### Missing index

```
1,000,000 rows × 200 bytes = 200 MB = ~25,000 pages

Seq Scan   : read 25,000 pages, discard 999,997 rows   ≈ 112 ms
Index Scan : 3 index pages + 3 row pages = 6 reads     ≈ 0.02 ms
                                                         ~5,000x
```

### The `loops` multiplication

```
Index Scan on orders (actual time=0.02..0.05 rows=3 loops=61)

misread : 0.05 ms
actual  : 0.05 × 61 = 3.05 ms of database time
plus    : 61 network round trips at ~0.5 ms = 30 ms of latency

one query with a join instead: ~2 ms and one round trip
                                → about 15x on wall-clock
```

### Spilling to disk

```
sort 1,000,000 rows × 100 bytes = 100 MB
work_mem = 4 MB (default)

in memory   : quicksort, ~20,000,000 comparisons     ≈ 1.2 s
external    : 25 passes writing and reading 100 MB   ≈ 8-15 s
                                                       ~10x

raise work_mem to 128 MB : back to ~1.2 s
add an index on the sort column : the sort disappears entirely ≈ 0 s
```

### Choosing which query to fix

```
Query A : 2,000 ms × 1 call/day        =     2 seconds/day
Query B :    20 ms × 1,000,000/day     = 20,000 seconds/day = 5.6 hours
```

**Query B costs ten thousand times more**, and it is the one nobody complains about because each
individual call feels fast. Sorting `pg_stat_statements` by `total_exec_time` is what surfaces it.

### `OFFSET`

```
LIMIT 20 OFFSET 0        : produce 20 rows            ≈ 1 ms
LIMIT 20 OFFSET 1,000,000: produce 1,000,020, keep 20 ≈ 2,000 ms
keyset                   : index seek + 20 rows       ≈ 1 ms at any depth
```

---

## 7. The trade-offs

### Fix the query, the index, or the schema

In increasing order of cost and permanence:

- **Rewrite the query** — free, reversible, and it is the right answer for a function on a column, an
  `OFFSET`, or a `SELECT *` defeating a covering index.
- **Add an index** — permanent write cost and 10–25% storage, from
  [day 030](../day-030-fast-and-slow/README.md). Right when the query shape is stable and common.
- **Change the schema** — denormalise, add a materialised view, partition. Expensive and hard to undo.
  Only when the first two are not enough, and with the reconciliation job from
  [day 029](../day-029-read-write-pointer/README.md).

**Always try them in that order.** Reaching for the schema first is the classic mistake.

### Raise `work_mem`, or add an index

Raising it fixes the sort spill immediately, and it is **per operation, per connection** — set it to
256 MB globally with 200 connections each running two sorts and you have promised 100 GB you do not
have. Set it per session or per role for the queries that need it. An index that provides the order
removes the sort entirely and costs write throughput instead.

### `EXPLAIN` or `EXPLAIN ANALYZE`

`EXPLAIN` is instant and safe and only shows guesses — which is exactly the thing you are trying to
verify. `EXPLAIN ANALYZE` shows the truth and runs the query, so on a query that takes four minutes it
takes four minutes, and on a write it really writes. **Use `ANALYZE` inside a rolled-back transaction**,
and use plain `EXPLAIN` first when you suspect the query may be catastrophic.

### Optimise the mean or the total

Mean time finds the query that is individually painful. Total time finds the query that is actually
costing you the machine. **Sort by total** — but keep an eye on the mean too, because a query with a
two-second mean is a user-visible problem even if it runs rarely.

### The sentence that separates candidates

> **I would not add an index before running `EXPLAIN ANALYZE`, and I would look at the estimated row
> counts before I look at the scan types.** A plan is only ever as good as the numbers it was built
> from, and the most expensive failure in this area is not a missing index — it is a planner that
> believed a step would return one row when it returned half a million, chose a nested loop on that
> basis, and did half a million index lookups. The plan was correct for the problem it thought it had.
> The fix there is `ANALYZE`, which costs seconds, and adding an index would not have helped at all.

---

## 8. In the interview

### How it gets asked

- *"Here's an EXPLAIN plan. What's wrong with this query?"* — the direct version, with a plan on the
  board.
- *"This endpoint got slow last week and nothing was deployed. What happened?"* — usually data growth
  crossing a threshold, or stale statistics after a bulk load.
- *"How do you find the slow queries in the first place?"* — `pg_stat_statements`, sorted by total time.
- *"What does `loops=61` mean?"* — the field everybody misreads.
- *"Why is the planner choosing a sequential scan when there's an index?"* — selectivity, a function on
  the column, or stale statistics.

### What to say out loud, in the first ninety seconds

1. **Say the procedure before any diagnosis.** *"I'd run `EXPLAIN ANALYZE` on it — with `BUFFERS` — and
   read the plan from the inside out, since the most indented nodes execute first."*
2. **Say what you check first, and it is not the scan type.** *"The first thing I compare is estimated
   rows against actual rows at each level. If they diverge badly, everything above that point was
   chosen for the wrong problem, and no amount of indexing fixes it — that's an `ANALYZE`."*
3. **Then the scan.** *"Then I look for a `Seq Scan` on a large table with a high `Rows Removed by
   Filter` — reading a million rows to return three is a missing index."*
4. **Then `loops`.** *"Then `loops` greater than one on a big node, remembering that `actual time` is
   per loop, so it multiplies. `loops=61` usually means an N+1 or a nested loop over too many rows."*
5. **Then disk.** *"And anything mentioning `Disk` — a sort spilling means the operation exceeded
   `work_mem`."*
6. **Name the causes that are invisible in the plan.** *"Two things won't show up at all: an ORM
   issuing sixty-one separate queries, where each plan looks perfectly healthy, and deep `OFFSET`
   pagination. I'd check the application log and `pg_stat_statements` for those."*
7. **Order the fixes.** *"Then I'd fix in order of cost: rewrite the query first, add an index second,
   change the schema last."*

### The follow-ups

**"The planner is choosing a sequential scan even though there's an index on that column. Why?"**
Three likely reasons and I would check them in order. First, selectivity: if the condition matches more
than roughly five to ten per cent of the table, a sequential scan genuinely is cheaper, because an index
scan there means hundreds of thousands of random page reads while a scan is one continuous sweep. The
planner is right and there is nothing to fix. Second, the statistics are stale — it thinks the condition
matches half the table when it matches a hundred rows — and `ANALYZE` fixes it. Third, something makes
the index unusable: a function wrapped around the column, so it must compute the value per row, or a
type mismatch in the comparison. To distinguish them I would look at the estimated row count in the
plan: if the estimate is wildly wrong it is statistics, and if the estimate is right and it still scans,
the planner has correctly decided the index is not worth it.

**"What does `loops=61` tell you?"**
That this node executed sixty-one times, and — crucially — that the `actual time` shown is **per loop**,
so the real total is sixty-one times that number. It is the most misread field in the output: a node
showing `actual time=0.02..0.05` with `loops=61` looks trivially fast and actually consumed about three
milliseconds of database time plus, if these are separate round trips, thirty milliseconds of network
latency. It normally means one of two things. Inside a nested loop join, it means the outer side
produced sixty-one rows and the inner side was probed once for each — which is fine if sixty-one is
small and a disaster if the estimate was wrong and it is really half a million. Or, if you are looking
at sixty-one *separate* plans rather than one node, it is an ORM N+1.

**"An endpoint got slow last week and nothing was deployed. What happened?"**
Most likely one of three things, and none of them is a code change. The data crossed a threshold: a
table that was small enough for a sequential scan to be fine is no longer, or a sort that fitted in
`work_mem` now spills to disk — and those changes are sudden rather than gradual, because the planner
flips strategy. Or the statistics went stale, typically after a bulk load or a large migration, so the
planner is now choosing on the basis of a distribution that no longer exists. Or index bloat: after a
lot of updates and deletes, an index can grow several times larger than it needs to be, so more pages
must be read. I would compare `EXPLAIN ANALYZE` now against what the plan used to be, run `ANALYZE`
first because it is free, and check `pg_stat_user_indexes` and table sizes for bloat.

**"How do you find which query to optimise?"**
`pg_stat_statements`, sorted by `total_exec_time` rather than by mean. The reason is that the expensive
query is usually not the one people complain about: a report taking two seconds once a night costs two
seconds a day, while a twenty-millisecond query running a million times a day costs five and a half
hours a day of database time. The second one is invisible to users and is the one actually consuming
the machine. I would look at both — total to find what is costing capacity, mean to find what is
costing user experience — and I would also check `calls`, because a query whose call count jumped is
often an N+1 that appeared with a new feature rather than a query that got slower.

### A model answer

> "I'd start by running `EXPLAIN ANALYZE`, with `BUFFERS`, and I'd read it from the inside out — the
> most indented nodes execute first, and the top line runs last.
>
> The first thing I look at is not the scan types. It's the estimated row count against the actual row
> count at each level. The planner chooses everything — join algorithm, join order, whether to use an
> index — from those estimates, so if it thought a step would return one row and it returned four
> hundred thousand, every decision above that point was made for a different problem. That's the failure
> that costs the most, and no index fixes it: it's stale statistics, and `ANALYZE` takes seconds.
>
> Concretely, that failure looks like a nested loop with `rows=1` estimated and `rows=480000` actual on
> the outer side, and then `loops=480000` on the inner index scan. The planner reasoned 'one outer row,
> so one lookup — a nested loop is obviously cheapest', and it ended up doing half a million lookups
> where a hash join would have taken about a third of a second.
>
> Then I look for a `Seq Scan` on a large table with a high `Rows Removed by Filter`. Reading a million
> rows to return three is a missing index — about 112 milliseconds against 0.02.
>
> Then `loops` greater than one anywhere significant, remembering that `actual time` is per loop and
> multiplies. And anything mentioning `Disk` — `Sort Method: external merge` means the sort exceeded
> `work_mem`, which is often ten times slower than sorting in memory.
>
> Two causes won't appear in the plan at all, and I'd check for them separately. An ORM issuing
> sixty-one queries instead of one — each plan looks perfectly healthy, and you only see it in the
> application log or in the call counts in `pg_stat_statements`. And deep `OFFSET` pagination, where
> `OFFSET 1000000` produces and discards a million rows.
>
> When I fix it, I'd go in order of cost: rewrite the query first, since that's free and reversible —
> unwrapping a function from an indexed column, replacing `OFFSET` with a keyset cursor, naming columns
> so a covering index can be used. Then add an index, which is a permanent tax on every write and 10 to
> 25 per cent of the table in storage. Then change the schema, which is the expensive and hard-to-undo
> option.
>
> And to decide *which* query to work on at all, I'd sort `pg_stat_statements` by total execution time
> rather than by mean — the twenty-millisecond query running a million times a day costs far more than
> the two-second report nobody runs."

---

## 9. Recall card

- **The plan is only as good as the estimates.** Compare **estimated rows against actual rows** first —
  a bad estimate poisons every decision above it, and the fix is `ANALYZE`.
- **Read plans inside out.** `cost` is an estimate; the `actual` line is truth; **`actual time` is per
  loop**, so `loops=61` multiplies.
- **Look for:** `Seq Scan` with high `Rows Removed by Filter`, `loops > 1` on a big node, and anything
  saying `Disk`.
- **Two causes never appear in the plan:** an ORM N+1, and deep `OFFSET`. Check the app log and
  `pg_stat_statements`.
- **Fix in order of cost:** rewrite the query, then add an index, then change the schema. And pick the
  query by **total** time, not mean.
