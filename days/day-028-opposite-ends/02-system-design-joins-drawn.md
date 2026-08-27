---
day: 28
track: system-design
title: "Joins, drawn"
phase: "Databases from zero"
status: written
---

# Day 028 · System Design — Joins, drawn

**After today you can:** You can draw inner, left, right and full joins and predict the row count of each.

**The interviewer asks it as:** *What is the difference between an inner join and a left join?*

---

## 1. What this is, and why they ask it

A **join** combines rows from two tables by matching them on a shared value. On
[day 026](../day-026-strings-revision/README.md) you put `author_id` on the posts table so a post could
point at its author; a join is how you follow that pointer and get the author's name back alongside
the post.

There are four kinds, and the only thing that separates them is **what happens to rows that find no
match**:

- **Inner** — drop them. Only matched pairs survive.
- **Left** — keep everything from the left table, filling the right side with `NULL` where there was
  no match.
- **Right** — the mirror image.
- **Full** — keep unmatched rows from both sides.

That is the whole concept, and it takes ten seconds to say. The reason it gets a whole day is the
second half of the question: **how many rows come out?** Almost everyone can define an inner join and
almost nobody can predict, without thinking, that joining three rows to two rows on the same key gives
six. Row multiplication is where real queries go wrong — a report that double-counts revenue is
usually a join fan-out, not a bug in the arithmetic.

Interviewers ask it constantly because it is fast, unfakeable, and the follow-ups have real depth:
*why did my `COUNT` go up?*, *why did `LEFT JOIN ... WHERE right.col = 'x'` silently become an inner
join?*, and *what does the database actually do to execute this?*

---

## 2. The story

Sarita's brother got married in December and the reception was at a hall on the bypass, and the thing
she remembers most clearly is the two lists.

Her father had been keeping one for four months — everybody invited, about six hundred names, typed
into his phone a few at a time as he thought of people. Her cousin Anwar stood at the gate on the
night with his own phone and typed in everyone who actually walked in.

The week after, sitting on the floor with both phones, they went through it.

The first thing they wanted was straightforward: who was invited **and** came. Six hundred on one
side, five hundred and ten on the other, and the names that appeared on both lists came to four
hundred and sixty. Those were the people they had to thank.

Then Sarita's mother wanted something different. She wanted the whole invitation list, all six
hundred, with a mark against the ones who had not turned up — because she wanted to know who to
telephone. That is a different question and it gives a different-sized answer: six hundred rows, with
a hundred and forty of them blank on the right-hand side.

Anwar wanted the opposite. He had fifty names on his list that were not on his uncle's at all —
neighbours, somebody's driver, a whole family nobody could identify — and he wanted those, because he
thought it was funny.

And Sarita's father, who is thorough, wanted one list with everybody on it from either side, marked
one way or the other. Six hundred and fifty.

The part that caused an actual argument was smaller and stranger. One man — a supplier of her
father's — had been invited twice, because her father had entered him once under his name and once
under his firm's name. And he had come twice, in a manner of speaking: he signed in at the gate, went
out to move his car, and Anwar typed him in again.

So when they matched the two lists, that one man produced four lines. Two invitations against two
arrivals. Sarita said that could not be right and her father showed her, and it was right — the
matching does what it says, and if a name is on one side twice and the other side twice, it comes out
four times.

---

## 3. The idea in plain English

The invitation list is the **left table**. The arrivals list is the **right table**. The four questions
Sarita's family asked are the four joins. And the man who appeared four times is **row
multiplication**, which is the thing you must be able to predict.

### The four joins, on one example

Two small tables:

```
  customers                    orders
  +----+------+                +----+-------------+--------+
  | id | name |                | id | customer_id | amount |
  +----+------+                +----+-------------+--------+
  | 1  | Asha |                | 10 | 1           | 500    |
  | 2  | Ravi |                | 11 | 1           | 300    |
  | 3  | Nita |                | 12 | 2           | 900    |
  | 4  | Sam  |                | 13 | NULL        | 150    |
  +----+------+                +----+-------------+--------+
```

Asha has two orders. Ravi has one. Nita and Sam have none. Order 13 belongs to nobody.

| Join | Rows out | What comes back |
|---|---:|---|
| `INNER JOIN` | **3** | Asha×2, Ravi×1. Nita, Sam and order 13 all vanish. |
| `LEFT JOIN` | **5** | those 3, plus Nita and Sam with `NULL` order columns. |
| `RIGHT JOIN` | **4** | those 3, plus order 13 with `NULL` customer columns. |
| `FULL OUTER JOIN` | **6** | those 3, plus Nita, Sam, **and** order 13. |

Those four numbers — 3, 5, 4, 6 — are worth being able to produce from that table in your head, because
that is precisely what "predict the row count" means.

### The syntax

```sql
SELECT c.name, o.amount
FROM   customers c
JOIN   orders o ON o.customer_id = c.id;          -- INNER is the default

SELECT c.name, o.amount
FROM   customers c
LEFT JOIN orders o ON o.customer_id = c.id;       -- LEFT OUTER JOIN, "OUTER" is optional
```

`JOIN` on its own means `INNER JOIN`. `LEFT JOIN` means `LEFT OUTER JOIN`. The word `OUTER` is noise
and nobody writes it.

**`ON` is not `WHERE`.** `ON` says how the rows are matched; `WHERE` filters the result afterwards.
For an inner join the distinction rarely matters. For an outer join it changes the answer completely,
and that is §7.

### Row multiplication — the part that matters

**A join is not a lookup. It is a matching, and matching can multiply.**

For each row on the left, the output contains **one row per match on the right**. So:

| Relationship | Left rows | Matches each | Rows out |
|---|---|---|---|
| one-to-one | 100 | 1 | 100 |
| one-to-many | 100 customers | avg 5 orders | 500 |
| many-to-many | 3 rows with key `1` | 2 rows with key `1` | **6** |

That last line is Sarita's supplier. Three on one side and two on the other, on the same key, gives
`3 × 2 = 6`. Not 3, not 2, not 5.

**The consequence that bites in real work:** joining an orders table to an order-items table and then
summing `orders.total` double-counts, because each order's total now appears once per item.

```sql
-- WRONG: an order with 4 items contributes its total 4 times
SELECT SUM(o.total)
FROM   orders o
JOIN   order_items i ON i.order_id = o.id;
```

The fixes are to aggregate before joining, or to use `SUM(DISTINCT ...)` carefully, or to not join at
all when you only need one side. **When a total looks too big after adding a join, this is why.**

### `LEFT JOIN` and counting

The most common real use of a left join is *"everyone, with their count, including the zeroes"*:

```sql
SELECT   c.id, c.name, COUNT(o.id) AS order_count
FROM     customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;
```

**`COUNT(o.id)`, not `COUNT(*)`.** A customer with no orders still produces one output row, with all
the order columns `NULL`. `COUNT(*)` counts that row and reports 1. `COUNT(o.id)` counts non-null
values and correctly reports 0.

On the example above: Asha 2, Ravi 1, Nita 0, Sam 0 — with `COUNT(o.id)`. With `COUNT(*)` you get
Asha 2, Ravi 1, Nita **1**, Sam **1**, which is wrong and looks entirely plausible.

### Anti-joins: "the ones with none"

*"Which customers have never ordered?"* Three ways:

```sql
-- 1. LEFT JOIN ... IS NULL
SELECT c.* FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;

-- 2. NOT EXISTS   <- usually the best
SELECT c.* FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 3. NOT IN       <- dangerous
SELECT c.* FROM customers c
WHERE c.id NOT IN (SELECT customer_id FROM orders);
```

**Prefer `NOT EXISTS`.** It can stop at the first match rather than building all of them, and — the
important part — **`NOT IN` returns no rows at all if the subquery contains a single `NULL`**. In the
example above, order 13 has `customer_id` `NULL`, so version 3 returns an empty result and version 2
returns Nita and Sam. That is a silent, complete wrong answer, and it is one of the nastiest gotchas
in SQL.

### Self-joins

A table can be joined to itself, which is how you compare rows within one table — an employee to their
manager, a comment to its parent:

```sql
SELECT e.name AS employee, m.name AS manager
FROM   employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

`LEFT`, so the chief executive — who has no manager — still appears. The aliases `e` and `m` are what
make it work; without them the database cannot tell which copy you mean.

### `CROSS JOIN`

Every row with every row, with no condition: `m × n` rows. Rarely what you want, occasionally exactly
what you want — generating every date-and-product combination for a report so that missing days show
as zero. And **an accidental cross join is what you get when you forget the `ON` clause**, which on two
tables of a million rows is a trillion rows and a very unhappy afternoon.

---

## 4. The picture

The four joins, drawn as what survives:

```
   customers (left)          orders (right)
   +--------+                +--------+
   |  1 2   |                |   1 2  |
   |  3 4   |                |    13  |     1 and 2 match; 3, 4 and 13 do not
   +--------+                +--------+

   INNER                LEFT                 RIGHT                FULL
   +--------+           +--------+           +--------+           +--------+
   |  ####  |           |########|           |  ######|           |########|
   |        |           |########|           |      ##|           |########|
   +--------+           +--------+           +--------+           +--------+
   matched only         all of left          all of right         everything
   3 rows               5 rows               4 rows               6 rows
                        (3 + Nita + Sam)     (3 + order 13)       (3 + 2 + 1)
```

**What to notice:** the row counts are not 3, 4, 4, 5. `LEFT` is 5 because Asha's *two* orders already
made two rows before the unmatched customers were added. **Row counts come from matches, not from
table sizes**, and that is the thing to internalise.

Row multiplication, drawn:

```
   left rows with key 1        right rows with key 1        output
   +-----+                     +-----+                      +-----------+
   | x   |                     | p   |                      | x p       |
   | y   |        JOIN         | q   |         --->         | x q       |
   | z   |       on key        +-----+                      | y p       |
   +-----+                                                  | y q       |
                                                            | z p       |
      3            ×              2              =          | z q       |
                                                            +-----------+
                                                                 6
```

**What to notice:** every left row is paired with every matching right row. This is why an order with
four items makes the order's total appear four times, and why a `SUM` over that join is wrong.

The `ON`-versus-`WHERE` trap, which is the highest-value picture on this page:

```
  LEFT JOIN orders o ON o.customer_id = c.id
  WHERE o.status = 'completed'
                |
                v
  1. the LEFT JOIN produces:   Asha|500  Asha|300  Ravi|900  Nita|NULL  Sam|NULL
  2. then WHERE runs on that:  NULL = 'completed' is UNKNOWN, so Nita and Sam are DROPPED
                |
                v
  the LEFT JOIN has silently become an INNER JOIN


  LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'completed'
                |
                v
  the condition is part of the MATCHING, so Nita and Sam still appear with NULLs
```

**What to notice:** the two queries differ by moving one condition from `WHERE` to `ON`, and they
return different numbers of rows. This is the single most common outer-join bug, and interviewers ask
about it directly.

---

## 5. How it actually works

### The three join algorithms

The planner picks one; you should be able to name all three and say when each wins.

**Nested loop join.** For each row on the left, scan the right table for matches. `O(n × m)` unless
there is an index on the right side's join column, in which case each lookup is a B-tree probe and it
becomes `O(n log m)`. **Best when the left side is small and the right side is indexed** — which is why
an unindexed foreign key turns this from fast into catastrophic.

**Hash join.** Build a hash table from the smaller table's join column, then scan the larger table
probing it. `O(n + m)`. **The workhorse for large unindexed joins**, and it needs the smaller side to
fit in memory — if it does not, it spills to disk in batches and gets much slower.

**Merge join.** Sort both sides by the join key, then walk them together with two pointers — literally
today's DSA lesson, applied to two sequences instead of one. `O(n log n + m log m)` if sorting is
needed, or `O(n + m)` if both sides already arrive sorted, which they do when you join on indexed
columns. **Best for large, already-sorted inputs.**

That merge join is worth pausing on: **the database is running the two-pointer walk from
[the DSA side of today](01-dsa-opposite-ends-pair-sums.md)**, with one index into each sorted stream,
advancing whichever is behind. It is the same idea in a different costume.

### Reading it in a plan

```sql
EXPLAIN ANALYZE
SELECT c.name, o.amount
FROM customers c JOIN orders o ON o.customer_id = c.id;
```

```
Hash Join  (cost=1.09..21.03 rows=500 width=68) (actual time=0.03..2.4 rows=500 loops=1)
  Hash Cond: (o.customer_id = c.id)
  ->  Seq Scan on orders o  (cost=0.00..16.00 rows=600 width=12)
  ->  Hash  (cost=1.04..1.04 rows=4 width=64)
        ->  Seq Scan on customers c  (cost=0.00..1.04 rows=4 width=64)
```

Read it inside out: scan `customers`, build a hash of it, then scan `orders` probing that hash. The
thing to check is **estimated versus actual rows** — `rows=500` estimated against `rows=500` actual is
healthy; a large gap means stale statistics and probably a bad plan choice.

### Indexes and joins

**Index the join columns.** From [day 026](../day-026-strings-revision/README.md), primary keys are
indexed automatically and foreign keys are not, so `orders.customer_id` needs an index you create
yourself. Without it, a nested loop join scans the whole orders table once per customer.

```
1,000 customers × 1,000,000 orders, nested loop, no index:
    1,000 × 1,000,000 = 1,000,000,000 row comparisons

with an index on orders(customer_id):
    1,000 × ~4 page reads = 4,000 reads
```

### Joining more than two tables

```sql
SELECT c.name, o.id, i.product_name, i.quantity
FROM   customers  c
JOIN   orders     o ON o.customer_id = c.id
JOIN   order_items i ON i.order_id = o.id
WHERE  o.status = 'completed';
```

The joins apply left to right, each one to the accumulated result. **Every join is another chance to
multiply rows**, so a customer with 5 orders of 4 items each contributes 20 rows, not 5 and not 4.
Three or four joins is normal; when you are past six, either the schema is over-normalised for this
access pattern or the query is doing two unrelated jobs.

### Doing it without a join

Two alternatives worth knowing, because interviewers ask *"could you avoid the join?"*:

- **A subquery in `SELECT`** — `(SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS n` — runs
  once per outer row, which is the N+1 problem in SQL form. Readable, and slower.
- **Two queries plus application-side stitching** — fetch customers, collect the ids, fetch all their
  orders with `WHERE customer_id IN (...)`, and match them up in code. This is exactly what
  DataLoader does for GraphQL on [day 021](../day-021-frequency-maps/README.md), and it is genuinely
  the right answer when the two tables live in different databases or different services.

### Products

Every relational database does all four joins. **MySQL has no `FULL OUTER JOIN`** — you emulate it with
a `LEFT JOIN` unioned with a `RIGHT JOIN` — which is a small, real difference worth knowing.
**Vitess and PlanetScale** restrict cross-shard joins, and **Cassandra and DynamoDB have no joins at
all**, which is why data modelling in those stores means pre-joining at write time and duplicating
data on purpose.

---

## 6. The numbers

### Row counts, which is the whole skill

```
customers: 4 rows       orders: 4 rows (one with a NULL customer_id)
matches:   Asha 2, Ravi 1, Nita 0, Sam 0, orphan order 1

INNER : 2 + 1                     = 3
LEFT  : 2 + 1 + 1(Nita) + 1(Sam)  = 5
RIGHT : 2 + 1 + 1(orphan)         = 4
FULL  : 2 + 1 + 1 + 1 + 1         = 6
CROSS : 4 × 4                     = 16
```

At realistic sizes:

```
10,000 customers, 50,000 orders, average 5 orders each, 2,000 customers with none:

INNER : 50,000                       (every order matches exactly one customer)
LEFT  : 50,000 + 2,000 = 52,000      (the ones with none appear once each)
CROSS : 10,000 × 50,000 = 500,000,000     — half a billion rows from a missing ON clause
```

### The double-counting bug, quantified

10,000 orders, average 4 items each, average order total ₹2,000:

```
true revenue                        = 10,000 × 2,000  = ₹20,000,000

SUM(o.total) after joining to items = 40,000 rows × 2,000 = ₹80,000,000
```

**Four times the real figure**, and the query is syntactically perfect. A report showing four times
the revenue usually gets noticed; one showing 1.3× because the average is 1.3 items does not.

### Join algorithms, compared

Joining 10,000 customers to 1,000,000 orders:

```
nested loop, no index      : 10,000 × 1,000,000 = 10^10 comparisons     — minutes to hours
nested loop, indexed right : 10,000 × ~4 page reads = 40,000 reads      — ~50 ms
hash join                  : build 10,000-entry hash + scan 1,000,000   — ~300 ms
merge join, both sorted    : 1,010,000 sequential steps                 — ~200 ms
```

**The unindexed nested loop is five orders of magnitude worse than everything else**, and that single
comparison is the reason "index your foreign keys" is a rule rather than a suggestion.

### Hash join memory

```
build side: 10,000 rows × ~64 bytes = 640 KB     -> fits in work_mem (4 MB default), fast
build side: 1,000,000 rows × 64 B   = 64 MB      -> spills to disk in batches
```

Postgres will choose the smaller table as the build side automatically. When a join suddenly gets slow
after data growth, a hash join spilling to disk is a common cause — and `work_mem` is the knob.

### `COUNT(*)` versus `COUNT(col)` on a left join

```
4 customers, 3 matched order rows, 2 customers with no orders

COUNT(*)     -> Asha 2, Ravi 1, Nita 1, Sam 1     WRONG (the NULL row is still a row)
COUNT(o.id)  -> Asha 2, Ravi 1, Nita 0, Sam 0     RIGHT
```

---

## 7. The trade-offs

### `ON` or `WHERE` for an outer join

Not a preference — they mean different things, and choosing wrongly changes the result.

A condition in `ON` is part of the **matching**: rows that fail it simply do not match, and the left
row survives with `NULL`s. A condition in `WHERE` runs **after** the join, and since `NULL` fails every
comparison, it removes the unmatched rows entirely — turning your left join into an inner join
silently.

**Rule: conditions on the right-hand table of an outer join go in `ON`. Conditions on the left-hand
table go in `WHERE`.**

### Join, or aggregate first

Joining then aggregating multiplies rows before you sum them. Aggregating first — in a subquery or CTE
— keeps the join one-to-one:

```sql
-- safer: one row per order before joining anything else
SELECT c.name, SUM(o.total)
FROM   customers c
JOIN   (SELECT customer_id, total FROM orders WHERE status = 'completed') o
       ON o.customer_id = c.id
GROUP BY c.name;
```

**Aggregate before joining whenever you are summing something from the "one" side**, because that is
exactly when fan-out corrupts the total.

### Join in the database, or stitch in the application

The database join happens next to the data, uses indexes, and sends only the result. Application-side
stitching — two queries and a dictionary — costs an extra round trip and moves work off the database,
which is the hardest thing to scale because there is usually one primary and many application servers.

**Join in the database by default.** Stitch in the application when the two tables are in different
databases or owned by different services, where a join is not available at all.

### Normalised with joins, or denormalised without

A join is the price of storing each fact once. Copying the customer's name onto every order removes the
join and creates a second copy to keep in step. Same trade as
[day 026](../day-026-strings-revision/README.md), and the deciding number is the read-to-write ratio.

### `NOT IN`, `NOT EXISTS`, or `LEFT JOIN ... IS NULL`

All three express "the ones with none". `NOT EXISTS` is usually fastest, because it can stop at the
first match. `LEFT JOIN ... IS NULL` is fine and reads well. **`NOT IN` is the one to avoid**, because a
single `NULL` in the subquery makes it return nothing at all — silently.

### The sentence that separates candidates

> **I would not join and then aggregate here.** The moment I join orders to order-items, every order's
> total appears once per item, so summing it gives four times the real revenue on an average of four
> items — and the query is syntactically perfect, so nothing warns me. I would aggregate the items to
> one row per order first, then join. More generally, before I write any join I want to be able to say
> how many rows it will produce, because row counts come from the number of matches, not from the size
> of the tables.

---

## 8. In the interview

### How it gets asked

- *"What's the difference between an inner join and a left join?"* — the definition, in ten seconds,
  followed immediately by a row-count question.
- *"How many rows does this return?"* — with two small tables on the board. This is the real test.
- *"Find the customers who have never ordered."* — the anti-join question, and the `NOT IN` trap.
- *"Why did my total go up when I added a join?"* — fan-out, and it is a genuinely common real bug.
- *"How does the database actually execute a join?"* — nested loop, hash, merge, and when each wins.

### What to say out loud, in the first ninety seconds

1. **Define by what happens to unmatched rows.** *"The only difference between the join types is what
   happens to rows with no match. Inner drops them; left keeps everything from the left table with
   NULLs on the right; right is the mirror; full keeps unmatched rows from both."*
2. **Give a concrete row count immediately.** *"With four customers where two have orders and two
   don't, and one orphan order — inner gives 3, left 5, right 4, full 6."*
3. **Raise fan-out before being asked.** *"The thing worth being careful about is that a join can
   multiply rows: three rows on one side matching two on the other gives six, not five."*
4. **Name the counting trap.** *"And with a left join, use `COUNT(o.id)` rather than `COUNT(*)` —
   unmatched customers still produce a row, so `COUNT(*)` reports 1 where the answer is 0."*
5. **Name the `ON`-versus-`WHERE` trap.** *"A condition on the right-hand table of a left join has to
   go in `ON`, not `WHERE`, or the NULLs get filtered out and it becomes an inner join."*
6. **Mention indexes.** *"And the join column on the right side needs an index, or a nested loop join
   scans the whole table once per row on the left."*

### The follow-ups

**"How many rows does this return?"**
It depends entirely on the number of **matches**, not on the sizes of the tables, and that is the whole
point of the question. For an inner join it is the sum over each left row of how many right rows match
it — so if one customer has two orders and another has one, that is three rows from two customers. For
a left join, add one row for each left row with no match at all. For a right join, mirror it. For a
full join, take the inner join and add the unmatched rows from both sides. The case people get wrong is
many-to-many: three rows with key `1` on the left and two with key `1` on the right give six output
rows, because every left row pairs with every matching right row. And a missing `ON` clause gives a
cross join, which is the product of the two table sizes — on two tables of a million rows, a trillion
rows.

**"Why did my revenue total go up when I added a join to order items?"**
Fan-out. Before the join there was one row per order carrying its total. After joining to items, an
order with four items becomes four rows, each still carrying the full order total — so `SUM(o.total)`
adds it four times. On an average of four items that is four times the real revenue, and nothing about
the query is syntactically wrong, which is what makes it dangerous. Two fixes. Aggregate the items to
one row per order in a subquery or CTE first, then join, so the join stays one-to-one. Or, if I only
needed the order totals, do not join to items at all — the join was added to get a column I could have
got separately. The general habit is to be able to state the expected row count before running any
query that joins and aggregates.

**"Find the customers who have never ordered."**
`NOT EXISTS` is what I would write: `SELECT * FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders
o WHERE o.customer_id = c.id)`. It reads as the question, and it can stop at the first matching order
rather than materialising all of them. `LEFT JOIN orders ... WHERE orders.id IS NULL` is equivalent and
fine — join everything, keep the rows where the join found nothing. The one I would avoid is `NOT IN`
against a subquery, because if that subquery yields even a single `NULL`, the whole `NOT IN` evaluates
to unknown for every row and the query returns **nothing at all**. In a table where `customer_id` is
nullable, that is a silent, complete wrong answer, and it is the sort of bug that survives review.

**"How does the database actually run a join?"**
Three algorithms and the planner chooses. A **nested loop** takes each row on the left and looks up
matches on the right — fine when the left side is small and the right side's join column is indexed,
because each lookup is a B-tree probe, and disastrous without the index, since it becomes a full scan
per row. A **hash join** builds a hash table from the smaller side's join column and probes it while
scanning the larger side, which is `O(n + m)` and is the usual choice for large unindexed joins,
provided the build side fits in `work_mem` — if it does not, it spills to disk and slows down sharply.
A **merge join** sorts both sides by the join key and walks them together with one index into each,
advancing whichever is behind — which is exactly the two-pointer walk, and it is the best option when
both inputs already arrive sorted, as they do when joining on indexed columns. `EXPLAIN` tells you
which was chosen, and a large gap between estimated and actual rows usually means stale statistics
rather than a bad query.

### A model answer

> "The only thing separating the join types is what happens to rows that find no match on the other
> side.
>
> An **inner join** keeps only matched pairs. A **left join** keeps every row from the left table,
> filling the right-hand columns with NULLs where nothing matched. A **right join** is the mirror. A
> **full outer join** keeps unmatched rows from both sides.
>
> Concretely — four customers, where Asha has two orders, Ravi has one, Nita and Sam have none, plus
> one order with no customer at all. Inner gives 3 rows. Left gives 5 — the same 3 plus Nita and Sam.
> Right gives 4 — the same 3 plus the orphan order. Full gives 6.
>
> The thing I'd flag before being asked is that a join can multiply rows. It isn't a lookup — it's a
> matching, and for each left row you get one output row per match. Asha's two orders already produce
> two rows before any unmatched customers are added, which is why left is 5 and not 4. And if a key
> appears three times on one side and twice on the other, you get six rows, not five.
>
> That matters in practice because of double counting. If I join orders to order items and then sum
> the order total, each order's total appears once per item — on an average of four items that's four
> times the real revenue, from a query that's syntactically perfect. The fix is to aggregate the items
> down to one row per order first, then join.
>
> Two other things I'd watch on a left join specifically. First, use `COUNT(o.id)` rather than
> `COUNT(*)` when counting per customer — an unmatched customer still produces a row with NULLs, so
> `COUNT(*)` says 1 where the right answer is 0. Second, a condition on the right-hand table has to go
> in the `ON` clause, not `WHERE`. If it goes in `WHERE`, it runs after the join, and since NULL fails
> every comparison it removes exactly the unmatched rows — your left join has silently become an inner
> join.
>
> And for it to be fast, the join column on the right needs an index. Without one, a nested loop join
> scans the whole right table once per left row — ten thousand customers against a million orders is
> ten billion comparisons, against about forty thousand page reads with the index."

---

## 9. Recall card

- **The only difference is what happens to unmatched rows.** Inner drops them; left keeps the left
  side; right mirrors; full keeps both.
- **Row counts come from matches, not table sizes.** 3 left rows × 2 right rows on the same key = **6**.
- **`COUNT(o.id)`, not `COUNT(*)`, after a left join** — the unmatched row is still a row.
- **Right-table conditions go in `ON`, not `WHERE`** — in `WHERE` they turn a left join into an inner
  join.
- **`NOT EXISTS` over `NOT IN`** — one `NULL` in the subquery makes `NOT IN` return nothing. And index
  every join column.
