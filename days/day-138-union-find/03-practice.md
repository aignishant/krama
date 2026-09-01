---
day: 138
track: practice
title: "Practice — Union-Find: the disjoint set union"
status: written
---

# Day 138 · Practice

**DSA topic:** Union-Find: the disjoint set union
**System design topic:** Data warehouses: OLAP versus OLTP

---

## Code these, in this order

One rule for the whole set: **write both optimisations before you write anything that uses the structure.**
Path halving in `find`, the size swap in `union`. They are two lines each and either one alone gives you
`O(log n)` — which on the adversarial input is the difference between passing and timing out.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Provinces | LeetCode 547 (Medium) | The `groups` counter, decremented only on a real merge. |
| 2 | Redundant Connection | LeetCode 684 (Medium) | The boolean return naming the offending edge. |
| 3 | Accounts Merge | LeetCode 721 (Medium) | Keying on the shared property to avoid `n²` comparisons. |
| 4 | Number of Islands II | LeetCode 305 (Hard) | The dynamic shape — count as land is added. |
| 5 | Satisfiability of Equality Equations | LeetCode 990 (Medium) | Equality as grouping; process `==` before `!=`. |
| 6 | Most Stones Removed with Same Row or Column | LeetCode 947 (Medium) | Grouping by row and column indices, not by stone. |

### On problem 1, solve it both ways and time it

Once with a traversal and once with Union-Find. Same complexity, so record both times and both line counts.
Then modify the problem: report the count after each edge is added, and time both again. The second ratio is
the argument for the structure.

### On problem 4, watch the boolean

Write the version that decrements once per land neighbour instead of once per successful `union`. Construct an
input where a new cell touches two cells already in the same island, and record both answers. Then construct
one where a new cell merges three separate islands at once and check your count drops by three.

### On problem 5, notice the ordering

Process all `==` equations first, then check every `!=` against the finished groups. Try it in the other order
and find an input that gives the wrong answer. One sentence on why order matters here and not in the other
problems.

### On problem 6, the modelling is the whole thing

Do not union stones. Union **row indices with column indices** — treating a row and a column as elements of
the same structure. Write down the two sentences before coding, and say why the answer is
`stones − number of groups`.

### Then the adversarial input

Build a `DisjointSet` with **no union by size** and run `union(i, i-1)` for `i` in `range(1, 100000)`, then
`find(99999)`. Time it. Add union by size and time it again. Two numbers.

Then remove path compression instead, keeping union by size, and time a million `find` calls. Three
configurations, three numbers, and you will never write only one optimisation again.

### Then the recursion experiment

Write `find` recursively, build a hundred-thousand-element chain without union by size, and call it. Record the
error. Then add union by size and try again.

---

### The structure drill

1. Say what the two arrays hold and what `parent[i] == i` means.
2. Write `find` with path halving from memory, iteratively.
3. Write `union` with union by size from memory.
4. Say what the boolean return means, in three different problem contexts.
5. Say why `size` must be read through `find`.

### The optimisations drill

1. Say what path compression does, in one sentence.
2. Say what union by size does, in one sentence.
3. Give the cost with neither, with each alone, and with both.
4. Say what `α(n)` is and the practical statement about its value.
5. Give the adversarial input that breaks a structure with no union by size.

### The recognition drill

1. Name the four problem shapes Union-Find solves.
2. State the rule for traversal versus Union-Find.
3. Give the arithmetic behind that rule at `m = V = 10^5`.
4. Say what it cannot do — four things.
5. Give the reverse-processing trick and when it applies.

### The costs drill

1. Give time and space, and compare memory against a traversal's structures.
2. Compute traversal-per-edge against Union-Find for 100,000 edges.
3. Say what dominates Kruskal's cost and why the Union-Find part is free.
4. Say what a single addition can do to the group count, and why the loop matters.

### The break-it drill

Trigger each and record the exact output or error:

1. No union by size, with `union(i, i-1)` in a loop.
2. Recursive `find` on a chain of 100,000 built without union by size.
3. Reading `size[x]` for a non-root.
4. Comparing `a == b` instead of `find(a) == find(b)`.
5. Decrementing the count per neighbour instead of per successful union.
6. Union-Find on a directed graph where you wanted strongly connected components.

---

### The two-workloads drill

1. Give the seven-row comparison table from memory.
2. Say what makes them incompatible, and why it is not a tuning problem.
3. Give an example query of each kind on the same table.
4. Say what data freshness each one needs.

### The columnar drill

1. Draw row layout and column layout for the same table.
2. Compute bytes read for `sum(amount)` over 40M rows in each.
3. Name the four mechanisms that make columnar fast.
4. Say which one is usually the largest factor, and why.
5. Give typical compression ratios and say why they are achievable.

### The replica drill

1. Say what a read replica fixes — three things.
2. Say what it does not fix.
3. Say what new problem it introduces.
4. Give the case where a replica genuinely is enough, and where it stops being.
5. Explain the buffer-pool damage and why "run it at 3 a.m." is only partial.

### The schema drill

1. Draw a star schema and label both kinds of table.
2. Say why the warehouse denormalises when production normalises.
3. Say what a slowly changing dimension is and what it protects.
4. Say what the fact table looks like — wide or thin, big or small.

### The pipeline drill

1. Name the three ways data gets into a warehouse.
2. Say what CDC catches that a nightly dump misses.
3. Say what ELT is and why it replaced ETL.
4. Name the layers and what each contains.
5. Say what dbt's dependency graph is, in graph terms.

### The numbers drill

1. Compute bytes read for the same query in a row store and a column store.
2. Recompute with monthly partitioning.
3. Compute storage cost for the same data in Postgres and in a warehouse.
4. Compute the monthly cost of a cluster left running.
5. Compute the cost of an unpartitioned 5 TB query run hourly under per-byte pricing.
6. Give the ratio of clickstream volume to transactional volume.

### The when-not drill

1. Give the data-size threshold below which you would not build one.
2. Name the tool you would use instead at a few hundred gigabytes.
3. Say what to check before proposing any platform.
4. Give the three conditions, any one of which justifies a warehouse.

### The failure drill

For each, say what happens and what you would build:

1. A monthly report runs against the production primary at 11 a.m.
2. The same report moved to the application's read replica.
3. A nightly `WHERE updated_at >` dump, and a row is hard-deleted in production.
4. A product's category changes, and last year's sales report is re-run.
5. `SELECT *` on an unpartitioned 5 TB table, scheduled hourly.
6. Two teams both computing "revenue" from the gold layer.
7. A Snowflake cluster nobody turned off.

Two of the seven are correctness problems and five are cost or performance. Sort them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Are these two nodes in the same group? Now merge two groups.*
   Two arrays, both optimisations with what each does, the `α(n)` result stated properly, the boolean return
   and the `groups` counter, and the traversal-versus-Union-Find rule with its arithmetic.

2. *How many islands are there after each addition?*
   The dynamic shape, the provisional increment, decrementing only on a successful union, why one addition can
   merge three islands, and the cost against re-running a flood fill.

3. *The analytics query is locking the production table. What do you do?*
   The two workloads, the row-versus-column arithmetic with the 16 GB figure, the buffer-pool damage, the
   replica as a half-answer, and the warehouse with its deliberate staleness — plus "how much data?" asked
   before recommending anything.

---

## Before you move on

- [ ] I write both optimisations, always.
- [ ] I can write `find` with path halving iteratively from memory.
- [ ] I can write `union` with union by size from memory.
- [ ] I know what the boolean return means in three different problems.
- [ ] I keep a `groups` counter and decrement only on a real merge.
- [ ] I know `size` is valid only at the root.
- [ ] I can state what each optimisation does and the cost of each alone.
- [ ] I can state the `α(n)` result and its practical value.
- [ ] I know the adversarial input that breaks a missing union by size.
- [ ] I can name the four shapes Union-Find solves.
- [ ] I know the traversal-versus-Union-Find rule and its arithmetic.
- [ ] I know the four things it cannot do.
- [ ] I know the reverse-processing trick for removals.
- [ ] I know one addition can merge several groups.
- [ ] I can give the OLTP versus OLAP table from memory.
- [ ] I can draw row and column layouts and compute bytes read for both.
- [ ] I can name the four mechanisms behind columnar speed.
- [ ] I know partition pruning is often the biggest factor.
- [ ] I can explain the buffer-pool damage an analytics query does.
- [ ] I know what a read replica fixes and what it does not.
- [ ] I know what new problem a replica introduces.
- [ ] I can draw a star schema and say why it denormalises.
- [ ] I know what a slowly changing dimension protects.
- [ ] I can name the three ingestion mechanisms and what CDC catches.
- [ ] I know why ELT replaced ETL.
- [ ] I can compute warehouse storage cost against compute cost.
- [ ] I know why per-byte pricing makes partitioning a financial control.
- [ ] I know the threshold below which I would not build a warehouse.
- [ ] I can name what I would use instead at a few hundred gigabytes.
- [ ] I answered all three questions above out loud.
