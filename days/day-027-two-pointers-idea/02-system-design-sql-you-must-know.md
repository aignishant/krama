---
day: 27
track: system-design
title: "SQL you must know for interviews"
phase: "Databases from zero"
status: written
---

# Day 027 · System Design — SQL you must know for interviews

**After today you can:** You can write SELECT, WHERE, GROUP BY, HAVING and ORDER BY without looking anything up.

**The interviewer asks it as:** *Write a query for the top five customers by total spend.*

---

## 1. What this is, and why they ask it

**SQL** — Structured Query Language — is how you ask a relational database for data. Its defining
property is that it is **declarative**: you describe the result you want, and the database works out
how to produce it. You never write a loop, never say which index to use, never decide the order of
operations. You state conditions and it finds a way.

That is unusual and it takes getting used to. In Python you say *how*: iterate, accumulate, sort. In
SQL you say *what*: these rows, grouped this way, filtered by that, in this order. The database's
**query planner** then chooses the actual steps — and it usually chooses better than you would,
because it knows how many rows are in each table and which indexes exist.

You need six clauses. `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, plus `LIMIT`.
That is genuinely most of the SQL asked in interviews, and *"write me a query for the top five
customers by total spend"* uses five of them in eight lines.

Interviewers ask because SQL is unfakeable and fast to assess. A candidate either produces the query
in two minutes or does not. It is also the most common way people reveal that they have only ever used
an ORM — they know `User.objects.filter(...)` and cannot say what it generates, which matters the
first time a query is slow.

---

## 2. The story

Nagaraj cooks for a small hotel near the bus stand — sixty or seventy meals at lunch, a bit less in the
evening — and three mornings a week he is at the wholesale market by five.

The first year he did it himself. He walked every row of the shed, looked at everything, remembered
what he had seen, compared prices in his head, and came out two hours later fairly sure he had missed
something. Usually he had.

Now he goes to Selvaraj, who sits at a desk near the gate and has run that shed for thirty years, and
he asks. He has got very good at asking, and it is always the same shape.

*Tomatoes. Only the ones that came in from Kolar. Only lots over fifty kilos. Cheapest first.*

Twenty seconds, and Selvaraj tells him which four suppliers and what they want per kilo. Nagaraj never
tells him how to find it. He never says which row to walk down, or which end to start from. He says
what he wants and what counts, and Selvaraj — who knows which rows were restocked at four this
morning, and which supplier's man is standing right there — works out the route.

Sometimes he asks a different shape of question, and this one took him longer to learn.

*How many suppliers have each vegetable today? Only tell me the ones with more than three.*

That is not a question about individual sacks at all. It is a question about groups of them, and the
"more than three" is about the groups rather than about any one sack, so it has to come after the
counting rather than before it. It took Nagaraj a while to see that those two kinds of condition are
genuinely different, and he got wrong answers for a month before he did.

What he says about the whole arrangement is that Selvaraj is not cleverer than him. He simply knows
the shed, and Nagaraj does not, and the fastest way through a place you do not know is to say clearly
what you want and let somebody who does know decide the route.

---

## 3. The idea in plain English

Nagaraj's question is a `SELECT`. Selvaraj working out the route is the **query planner**. And the two
kinds of condition — "only lots over fifty kilos" versus "only the vegetables with more than three
suppliers" — are `WHERE` and `HAVING`, which is the distinction this lesson exists to fix.

### The six clauses

```sql
SELECT   customer_id, SUM(amount) AS total     -- what to show
FROM     orders                                -- where to get it
WHERE    status = 'completed'                  -- which ROWS count
GROUP BY customer_id                           -- collapse rows into groups
HAVING   SUM(amount) > 10000                   -- which GROUPS count
ORDER BY total DESC                            -- what order
LIMIT    5;                                    -- how many
```

That is the whole shape, and almost every interview query is a subset of it.

### The order they actually run in

This is the single most useful thing on this page, because it explains three things that otherwise
look like arbitrary rules.

```
  written:   SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT
  executed:  FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
             1       2        3           4         5         6           7
```

Three consequences fall straight out of that:

**`WHERE` cannot see an alias defined in `SELECT`**, because `SELECT` has not run yet. So
`WHERE total > 100` fails when `total` was defined as `SUM(amount) AS total`.

**`ORDER BY` *can* see it**, because `ORDER BY` runs after `SELECT`. That is why `ORDER BY total DESC`
works in the query above and `WHERE total > 100` would not.

**`WHERE` cannot use an aggregate** like `SUM(...)`, because the grouping has not happened yet. That is
what `HAVING` is for.

### `WHERE` versus `HAVING`, which is the whole point

Nagaraj's two conditions:

- *"only lots over fifty kilos"* — a condition about **one row**. It applies before anything is
  grouped, so: `WHERE`.
- *"only vegetables with more than three suppliers"* — a condition about **a group**. It cannot be
  decided until the counting has happened, so: `HAVING`.

```sql
SELECT   vegetable, COUNT(*) AS supplier_count
FROM     lots
WHERE    quantity_kg > 50          -- discard individual small lots FIRST
GROUP BY vegetable
HAVING   COUNT(*) > 3;             -- then discard groups that are too small
```

**The rule to say out loud: `WHERE` filters rows, `HAVING` filters groups.** And a corollary that is
worth marks: **put every condition you can into `WHERE`**, because `WHERE` runs first and reduces how
much there is to group. Filtering in `HAVING` what could have been filtered in `WHERE` is correct and
slower.

### Aggregates

Five functions do most of the work: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

```sql
SELECT COUNT(*)              FROM orders;   -- number of rows
SELECT COUNT(discount_code)  FROM orders;   -- rows where discount_code IS NOT NULL
SELECT COUNT(DISTINCT user_id) FROM orders; -- how many different users
SELECT AVG(amount)           FROM orders;   -- NULLs are skipped, not treated as 0
```

Two behaviours that get asked directly:

**`COUNT(*)` counts rows; `COUNT(column)` counts non-null values in that column.** If 300 of 1,000
orders have no discount code, `COUNT(*)` is 1,000 and `COUNT(discount_code)` is 700.

**Aggregates ignore `NULL`.** `AVG` of `[10, 20, NULL]` is 15, not 10 — the null is skipped, not
counted as zero. That is usually what you want and it is occasionally a bug: if a null *means* zero in
your data, `AVG` will be wrong, and `COALESCE(amount, 0)` is the fix.

### Grouping, precisely

`GROUP BY` collapses many rows into one row per distinct value. After it runs, **every column in
`SELECT` must either be in the `GROUP BY` or be inside an aggregate** — because for anything else there
would be many values and only one row to put them in.

```sql
-- error: name is neither grouped nor aggregated
SELECT customer_id, name, SUM(amount) FROM orders GROUP BY customer_id;

-- fine
SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id;
```

Postgres raises `column "name" must appear in the GROUP BY clause or be used in an aggregate
function`. MySQL historically allowed it and returned an arbitrary value, which is worse than an
error and is a real source of wrong reports.

### `NULL` in conditions

From [day 026](../day-026-strings-revision/README.md): `NULL` is *unknown*, so comparing with it gives
unknown, not true.

```sql
WHERE discount_code = NULL       -- matches NOTHING, ever
WHERE discount_code IS NULL      -- correct
WHERE discount_code <> 'SALE'    -- excludes NULLs too! unknown is not true
```

That third line is the one that catches people. If you want the nulls as well you must say so:
`WHERE discount_code <> 'SALE' OR discount_code IS NULL`.

### `ORDER BY` and `LIMIT`

```sql
ORDER BY total DESC, customer_id ASC     -- second column breaks ties
LIMIT 5 OFFSET 10                        -- rows 11-15
```

Two things worth saying: **without `ORDER BY`, row order is undefined**, so `LIMIT 5` on its own gives
you five arbitrary rows and may give different ones each run. And **add a tie-breaker** — without one,
two customers with the same total may swap places between runs, which makes paginated results
duplicate and skip.

---

## 4. The picture

The two orders — written and executed — with what each stage does:

```
   WRITTEN                      EXECUTED               what it holds afterwards
   ------------------------     ------------------     -------------------------------
   SELECT   cust, SUM(amt)  5   1  FROM orders         every row in the table
   FROM     orders          2   2  WHERE status=...    only the rows that pass
   WHERE    status = '...'  3   3  GROUP BY cust       one bucket per customer
   GROUP BY cust            4   4  HAVING SUM(..)>...  only the buckets that pass
   HAVING   SUM(amt) > ...  5   5  SELECT cust, SUM    one row per bucket, chosen columns
   ORDER BY total DESC      6   6  ORDER BY total      the same rows, sorted
   LIMIT    5               7   7  LIMIT 5             the first five
```

**What to notice:** `SELECT` is fifth, not first. That single fact explains why `WHERE` cannot use an
alias, why `ORDER BY` can, and why aggregate conditions need `HAVING`.

The same query on real rows:

```
  orders                                     after WHERE status='completed'
  +----+------+--------+-----------+         +----+------+--------+
  | id | cust | amount | status    |         | id | cust | amount |
  +----+------+--------+-----------+         +----+------+--------+
  | 1  | 7    | 1200   | completed |         | 1  | 7    | 1200   |
  | 2  | 7    |  800   | completed |   --->  | 2  | 7    |  800   |
  | 3  | 9    | 5000   | cancelled |         | 4  | 9    |  300   |
  | 4  | 9    |  300   | completed |         | 5  | 4    | 9000   |
  | 5  | 4    | 9000   | completed |         +----+------+--------+
  +----+------+--------+-----------+
                                             after GROUP BY cust
                                             +------+------------+
                                             | cust | SUM(amount)|
                                             +------+------------+
                                             | 7    | 2000       |
                                             | 9    |  300       |
                                             | 4    | 9000       |
                                             +------+------------+

                                             after HAVING SUM(amount) > 1000
                                             +------+------+       after ORDER BY total DESC
                                             | 7    | 2000 |       +------+------+
                                             | 4    | 9000 |  -->  | 4    | 9000 |
                                             +------+------+       | 7    | 2000 |
                                                                   +------+------+
```

**What to notice:** the cancelled ₹5,000 order disappears at the `WHERE` stage, so customer 9's total
is 300 and not 5,300. Filtering **before** grouping changes the answer, not just the speed — which is
why deciding whether a condition belongs in `WHERE` or `HAVING` is a correctness question, not a
style one.

---

## 5. How it actually works

### Building the interview question, one clause at a time

> *"Write a query for the top five customers by total spend."*

**Start with the raw rows.**

```sql
SELECT customer_id, amount FROM orders;
```

**Collapse to one row per customer.**

```sql
SELECT   customer_id, SUM(amount) AS total_spend
FROM     orders
GROUP BY customer_id;
```

**Ask the clarifying question out loud** — this is the part interviewers are actually watching for:
*"Should cancelled and refunded orders count? And do you want the customer's name, or is the id
enough?"* Say completed only, and the name.

**Filter the rows before grouping.**

```sql
SELECT   customer_id, SUM(amount) AS total_spend
FROM     orders
WHERE    status = 'completed'
GROUP BY customer_id;
```

**Get the name, which needs the other table.**

```sql
SELECT   c.id, c.name, SUM(o.amount) AS total_spend
FROM     orders   o
JOIN     customers c ON c.id = o.customer_id
WHERE    o.status = 'completed'
GROUP BY c.id, c.name
ORDER BY total_spend DESC
LIMIT    5;
```

Joins are [day 028](../day-028-opposite-ends/README.md) in full; for today, `JOIN ... ON` means *match
each order to its customer by id*.

Note `GROUP BY c.id, c.name` — every non-aggregated column in `SELECT` must be grouped. Grouping by
`c.id` alone is enough in Postgres when `c.id` is the primary key, because the name is then
functionally determined, but writing both is portable and clearer.

**Two details worth mentioning unprompted:**

*"I'd add a tie-breaker to the `ORDER BY` — `total_spend DESC, c.id` — so the result is stable when two
customers have identical totals."*

*"And this excludes customers with no completed orders entirely. If you want them shown with a total
of zero, that's a `LEFT JOIN` from customers to orders with `COALESCE(SUM(o.amount), 0)`."*

### Reading a query plan

`EXPLAIN ANALYZE` in front of any query shows what the planner chose and what it actually cost:

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

**`Seq Scan` plus `Rows Removed by Filter: 999997`** means it read a million rows to return three. Add
the index and it becomes:

```
Index Scan using orders_customer_id_idx on orders  (cost=0.42..8.45 rows=3 width=64)
                                                   (actual time=0.018..0.024 rows=3 loops=1)
```

112 ms to 0.024 ms. **Recognising `Seq Scan` on a large table as the thing to fix** is most of what
"can you read a query plan?" is asking.

### The patterns that come up

**Top N per group** — "the three most recent orders for each customer" — is the one that needs a window
function, and it is worth knowing the shape even if you cannot write it from memory:

```sql
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM   orders o
) t
WHERE rn <= 3;
```

`PARTITION BY` is "restart the numbering for each customer". Window functions are the single biggest
gap in most candidates' SQL, and naming `ROW_NUMBER`, `RANK` and `PARTITION BY` is a strong signal.

**Counting things that may be zero** needs a `LEFT JOIN`:

```sql
SELECT   c.id, c.name, COUNT(o.id) AS order_count
FROM     customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;
```

`COUNT(o.id)` and not `COUNT(*)` — with a `LEFT JOIN`, a customer with no orders still produces one
row with nulls, so `COUNT(*)` would say 1 and `COUNT(o.id)` correctly says 0. That is a genuinely
common bug and a good thing to mention.

**Existence** is usually better as `EXISTS` than as a join, because it can stop at the first match:

```sql
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.amount > 10000);
```

### Dialects

The core is standard and portable. The differences that bite: `LIMIT 5` in Postgres, MySQL and SQLite;
`TOP 5` in SQL Server; `FETCH FIRST 5 ROWS ONLY` in the standard and Oracle. String concatenation is
`||` in Postgres and `CONCAT()` in MySQL. Postgres is strict about `GROUP BY`; MySQL historically was
not. Write standard SQL and mention that you would check the dialect.

---

## 6. The numbers

### The index, again

1,000,000 orders, about 200 bytes each:

```
table size = 1,000,000 × 200 B = 200 MB

WHERE customer_id = 4217:
  sequential scan : read 200 MB, discard 999,997 rows  ≈ 112 ms
  index scan      : ~3 B-tree page reads + 3 row reads ≈ 0.02 ms
                                                         about 5,000x
```

And it gets worse linearly: at 10 million orders the scan is 1.1 seconds and the index scan is
still about 0.02 ms, because a B-tree gains a level roughly every 500× growth.

### `SELECT *` versus naming columns

An orders row is 200 bytes, of which `id`, `customer_id` and `amount` are 24.

```
SELECT *             : 1,000,000 × 200 B = 200 MB read and sent
SELECT id, cust, amt : the same rows, but a covering index can serve it
                       from ~24 MB of index without touching the table at all
```

A **covering index** — one that contains every column the query needs — lets the database answer
without reading the table rows, which on a wide table is often 5–10× less I/O. `SELECT *` makes that
impossible, which is the real argument against it, over and above sending bytes nobody uses.

### `GROUP BY` memory

Grouping one million orders by customer, with 50,000 distinct customers:

```
hash table: 50,000 groups × ~50 B = 2.5 MB     -> fits in memory, fast
```

Grouping by `order_id` instead — a million distinct values:

```
hash table: 1,000,000 × 50 B = 50 MB           -> may exceed work_mem and spill to disk
```

Postgres's default `work_mem` is 4 MB. Exceeding it turns an in-memory hash aggregate into a sort that
spills to disk, and that is a common cause of a query that was fast in testing and slow in production.
**The number of distinct groups is what decides it**, not the number of rows.

### `OFFSET` pagination

From [day 017](../day-017-matrix-tricks/README.md), now with the reason:

```
LIMIT 20 OFFSET 0        : find 20 rows                    ≈ 1 ms
LIMIT 20 OFFSET 1000000  : find and DISCARD 1,000,000 rows ≈ 2,000 ms
```

`OFFSET` does not skip cheaply — it generates and throws away every skipped row. That is why deep
pagination gets slower and why cursor pagination — `WHERE id > :last_seen ORDER BY id LIMIT 20` —
stays at about 1 ms at any depth.

### `COUNT(*)` on a big table

```
SELECT COUNT(*) FROM orders;      -- 10,000,000 rows
Postgres: full scan ≈ 1-3 seconds     (MVCC means it must check row visibility)
```

Which is why a live "12,483,221 orders" counter on a dashboard is usually a maintained counter or an
approximation from `pg_class.reltuples`, not a real `COUNT(*)`.

---

## 7. The trade-offs

### Do the work in SQL, or in the application?

**In SQL** the database does the filtering, grouping and sorting close to the data, sends only the
result, and can use indexes. Summing a million rows in the database sends back one number; doing it in
your application sends back a million rows and 200 MB.

**In the application** the logic is testable, versioned and debuggable in a language you know well, and
it does not consume database CPU — which is the hardest resource to scale, because you usually have
one primary and many application servers.

**The rule: filter and aggregate in SQL, put business rules in the application.** Reducing a million
rows to fifty in the database is obviously right. Encoding your pricing policy in a 200-line query is
obviously wrong.

### `SELECT *` or named columns

`SELECT *` is fine in an interactive session and a liability in code: it sends columns you do not need,
it breaks the moment someone adds or reorders a column, and it prevents covering-index optimisations.
**Name your columns in anything that ships.**

### ORM or raw SQL

An ORM removes boilerplate, prevents SQL injection by default, and handles migrations. It also hides
what is being executed, which is how the N+1 query problem happens — looping over 100 users and
touching `user.orders` issues 101 queries, exactly the shape from
[day 021](../day-021-frequency-maps/README.md). **Use the ORM for straightforward access, drop to SQL
for reports and anything with a `GROUP BY`, and be able to see the generated query** — every ORM has a
way to print it, and knowing that is a strong signal.

### Normalised joins or denormalised columns

A join is the correct way to combine tables and it costs work at read time. Copying a value to avoid
the join is faster to read and can go stale. Same trade as
[day 026](../day-026-strings-revision/README.md): normalise first, denormalise when a measured
read-to-write ratio justifies it.

### The sentence that separates candidates

> **I would not compute this in application code.** Pulling a million order rows across the network to
> sum them in Python costs 200 MB of transfer, several seconds, and gigabytes of memory, to produce one
> number the database could have produced in 200 milliseconds using an index it already has. What I
> *would* keep out of SQL is business logic — a 200-line query encoding pricing rules is untestable and
> unreviewable, and it runs on the one machine I cannot easily add more of. Filter and aggregate in
> SQL; decide in the application.

---

## 8. In the interview

### How it gets asked

- *"Write a query for the top five customers by total spend."* — the canonical version, using five
  clauses.
- *"What's the difference between `WHERE` and `HAVING`?"* — the definition question, and the one most
  often fumbled.
- *"This query is slow. What would you do?"* — where `EXPLAIN`, indexes and `Seq Scan` are the answer.
- *"Find the customers who have never placed an order."* — the `LEFT JOIN ... IS NULL` or `NOT EXISTS`
  question.
- *"What does `COUNT(*)` do differently from `COUNT(column)`?"* — the small precise one.

### What to say out loud, in the first ninety seconds

1. **Ask two clarifying questions before writing.** *"Which order statuses count — do cancelled and
   refunded orders get excluded? And do you want the customer's name or just the id?"*
2. **Say the shape before the syntax.** *"So: filter to completed orders, group by customer, sum the
   amounts, sort descending, take five."*
3. **Write it in execution order in your head, not written order.** `FROM`, `WHERE`, `GROUP BY`,
   `HAVING`, `SELECT`, `ORDER BY`, `LIMIT`.
4. **Say why the filter is in `WHERE` and not `HAVING`.** *"Status is a property of an individual
   order, so it belongs in `WHERE` — that runs before the grouping, so it reduces what has to be
   grouped, and it also changes the answer rather than just the speed."*
5. **Mention the tie-breaker unprompted.** *"I'd add a second `ORDER BY` column so the result is
   stable when two customers tie."*
6. **Say what the query excludes.** *"This drops customers with no completed orders. If you want them
   at zero, that's a `LEFT JOIN` with `COALESCE`."*
7. **Offer the index.** *"For this to be fast I'd want an index on `orders(customer_id)` and probably
   on `status`."*

### The follow-ups

**"What's the difference between `WHERE` and `HAVING`?"**
`WHERE` filters individual rows and runs **before** grouping; `HAVING` filters groups and runs
**after**. So a condition on a column of one row — `status = 'completed'` — goes in `WHERE`, and a
condition on an aggregate — `SUM(amount) > 10000` — must go in `HAVING`, because the sum does not exist
until the grouping has happened. It is not only a syntax rule: filtering before grouping changes the
answer, because a cancelled order excluded in `WHERE` never contributes to any customer's total, while
the same condition applied afterwards could not remove it. And where a condition *could* go in either
— which is rare — it belongs in `WHERE`, because reducing the rows before grouping is strictly less
work.

**"This query takes eight seconds. What do you do?"**
Run `EXPLAIN ANALYZE` on it first, before changing anything, because guessing is how people add indexes
that do not get used. What I would look for, in order: a `Seq Scan` on a large table with a high "Rows
Removed by Filter", which means a missing index on the filtered column; a nested loop join over a large
outer table, which usually means a missing index on the join column; and a sort or hash aggregate that
has spilled to disk, which means the grouping exceeded `work_mem`. Then I would check the estimated
versus actual row counts — if they differ wildly, the statistics are stale and `ANALYZE` may fix the
plan by itself. Beyond that: is the query selecting columns it does not need, which prevents a covering
index; and is it doing deep `OFFSET` pagination, which discards every skipped row and should be a
keyset cursor instead.

**"Find customers who have never placed an order."**
Three ways, and they are not equivalent in performance. `LEFT JOIN orders ON ... WHERE orders.id IS
NULL` — join everything and keep the rows where the join found nothing. `NOT EXISTS (SELECT 1 FROM
orders WHERE customer_id = c.id)` — usually the best, because it can stop at the first matching row
rather than materialising all of them. And `NOT IN (SELECT customer_id FROM orders)`, which I would
avoid: if any `customer_id` in that subquery is `NULL`, `NOT IN` returns no rows at all, because
comparing with unknown gives unknown. That `NULL` trap in `NOT IN` is a genuinely nasty bug and worth
naming.

**"How would you get the three most recent orders for each customer?"**
That is top-N-per-group, and it needs a window function rather than a plain `GROUP BY`, because
`GROUP BY` collapses each customer to one row and I need three. I would use `ROW_NUMBER() OVER
(PARTITION BY customer_id ORDER BY created_at DESC)` in a subquery, then filter the outer query to
`rn <= 3`. `PARTITION BY` restarts the numbering for each customer, which is exactly the "per group"
part. The alternative with a correlated subquery — for each customer, select from orders with its own
`LIMIT 3` — is easier to read and much slower, because it runs once per customer. And I would want an
index on `(customer_id, created_at DESC)` so the window function does not have to sort.

### A model answer

> "Two clarifications first. Which statuses count as spend — should I exclude cancelled and refunded
> orders? And do you want the customer's name, or is the id enough?
>
> ...Completed only, and the name.
>
> So the shape is: take orders, keep the completed ones, group by customer, sum the amounts, join to
> get the name, sort descending, take five.
>
> ```sql
> SELECT   c.id, c.name, SUM(o.amount) AS total_spend
> FROM     orders o
> JOIN     customers c ON c.id = o.customer_id
> WHERE    o.status = 'completed'
> GROUP BY c.id, c.name
> ORDER BY total_spend DESC, c.id
> LIMIT    5;
> ```
>
> The status filter is in `WHERE` rather than `HAVING`, and that's deliberate: status is a property of
> an individual order, so it can be decided before any grouping happens. That matters twice over — it
> reduces how many rows have to be grouped, and it changes the answer, because a cancelled order
> filtered out in `WHERE` never contributes to anyone's total. `HAVING` is for conditions on the
> aggregate itself, like `SUM(o.amount) > 10000`, which cannot be evaluated until the group exists.
>
> `GROUP BY c.id, c.name` because every column in `SELECT` that isn't inside an aggregate has to be
> grouped. Postgres would accept just `c.id` since it's the primary key and the name is functionally
> determined by it, but writing both is portable.
>
> I've added `c.id` as a second `ORDER BY` column so the result is stable — without a tie-breaker, two
> customers with identical totals can come back in either order, which makes paginated results
> duplicate and skip rows between pages.
>
> One thing worth flagging: this excludes customers who have no completed orders at all, because an
> inner join drops them. If you want them shown with a total of zero, it becomes a `LEFT JOIN` from
> customers to orders with `COALESCE(SUM(o.amount), 0)`.
>
> And for this to be fast on a million orders I'd want an index on `orders(customer_id)` for the join
> and something on `status` — or better, a partial index on `orders(customer_id) WHERE status =
> 'completed'`, since that's the only status this query ever looks at. Without an index the filter is a
> sequential scan: about 200 MB and 112 milliseconds on a million rows, against about 0.02 with the
> index."

---

## 9. Recall card

- **SQL is declarative:** say what you want, the planner picks the route. Six clauses cover almost
  everything.
- **Execution order is `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`** — which is why
  `WHERE` cannot see an alias and `ORDER BY` can.
- **`WHERE` filters rows, `HAVING` filters groups.** Put every condition you can in `WHERE`.
- **`COUNT(*)` counts rows, `COUNT(col)` counts non-nulls**, and aggregates skip `NULL`. Use `IS NULL`,
  never `= NULL`.
- **Always `ORDER BY` before `LIMIT`, and add a tie-breaker.** Run `EXPLAIN ANALYZE` before optimising
  anything.
