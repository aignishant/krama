---
day: 139
track: practice
title: "Practice — Minimum spanning trees: Kruskal and Prim"
status: written
---

# Day 139 · Practice

**DSA topic:** Minimum spanning trees: Kruskal and Prim
**System design topic:** ETL, batch pipelines, and where data goes to be counted

---

## Code these, in this order

One rule for the whole set: **store edges as `(weight, a, b)` so a bare `sort()` is correct**, and **check
`len(chosen) == n - 1` before returning a total.** The first removes a place to make a mistake; the second is
the line almost everybody forgets, and without it a disconnected graph returns a plausible number.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Min Cost to Connect All Points | LeetCode 1584 (Medium) | An implicit complete graph — dense Prim's, and never building the edge list. |
| 2 | Connecting Cities With Minimum Cost | LeetCode 1135 (Medium) | Plain Kruskal's, plus the disconnected check. |
| 3 | Optimize Water Distribution in a Village | LeetCode 1168 (Hard) | The virtual-vertex trick. |
| 4 | Find Critical and Pseudo-Critical Edges | LeetCode 1489 (Hard) | Kruskal's run repeatedly, with an edge forced in or excluded. |
| 5 | Min Cost to Connect All Points, again | — | Solve with Kruskal's too, and compare the memory. |

### On problem 1, do the arithmetic before coding

`n` points means `n(n−1)/2` edges. Compute that for `n = 1,000`. Then write the `O(n²)` dense Prim's that never
materialises the edge list, and separately write the Kruskal's version that does. Record the peak memory of
each. One of them is `O(n)` and the other is `O(n²)`.

### On problem 3, write the reframing down first

Before any code, write two sentences: what the extra vertex is, and what a well becomes. Then say why the
graph is now guaranteed connected and what that means for the `-1` check. Then solve it.

### On problem 4, be careful with "forced in"

Forcing an edge into the tree means taking it *before* sorting the rest and starting the total from its
weight. Excluding one means skipping it entirely, not deprioritising it. Write both helpers, and test each on
a graph where you know the answer by hand.

### Then the Prim's-versus-Dijkstra experiment

Take your Dijkstra from [day 136](../day-136-dijkstra/README.md) and change exactly one line — the value
pushed into the heap — to turn it into Prim's. Then build a graph where the two give different trees:

```
A --1-- B --5-- C
A ---------4--------- C
```

Run both from A. Record the edge sets. Write one sentence saying which objective each one minimised.

### Then the disconnected check

Run Kruskal's on four vertices and two edges, with and without the `len(chosen) == n - 1` check. Record both
returns. Say which one a caller would notice.

### Then the tie experiment

Build a graph where three edges share the same weight and there are several minimum spanning trees. Run
Kruskal's and Prim's and compare the edge sets and the totals. Write down which one is safe to assert in a
test.

---

### The definitions drill

1. Define a spanning tree and say how many edges it has.
2. Say why a minimum spanning tree never contains a cycle.
3. Say what happens on a disconnected graph and what you return.
4. Say when the minimum spanning tree is unique.

### The two-algorithms drill

1. Write Kruskal's from memory in eight lines.
2. Write Prim's with a heap from memory.
3. Point at the one line that differs from Dijkstra and say what each version minimises.
4. Write the dense `O(V²)` Prim's and say what `best[v]` holds.
5. Give the rule for choosing between them, with the density arithmetic.

### The proof drill

1. State the cut property.
2. Give the swap argument in three sentences.
3. Say how Prim's is an application of it.
4. Say how Kruskal's is an application of it.
5. State the cycle property and say what it justifies.

### The not-shortest-path drill

1. Give the triangle counter-example and both answers.
2. State the two objectives in one sentence each.
3. Say what happens if you write Prim's with Dijkstra's key.
4. Say why that bug agrees with the correct version surprisingly often.

### The costs drill

1. Give Kruskal's cost and say what dominates.
2. Give heap-Prim's and dense-Prim's costs.
3. Compute all three at `V = 100,000, E = 300,000` and at `V = 5,000` complete.
4. Say what Kruskal's memory constraint is and when it binds.
5. Say what happens to Kruskal's cost if the edges are pre-sorted.

### The break-it drill

Trigger each and record the exact output or error:

1. Prim's with the accumulated key, on a chain-versus-single-edge graph.
2. No `len(chosen) == n - 1` check, on a disconnected graph.
3. Prim's without the `in_tree` stale-entry skip.
4. Kruskal's on a directed edge list.
5. A test asserting a specific edge set on a graph with tied weights.
6. Building the full edge list for 100,000 points on a plane.

---

### The path drill

1. Trace a number from a production write to a dashboard, naming every stage.
2. Say what a pipeline's dependency structure is, in graph terms.
3. Say what the number of levels and the widest level tell you.
4. Say what ELT is and give the two reasons it replaced ETL.

### The two-properties drill

1. State both properties that make a pipeline survivable.
2. Say what "the job takes the execution date as a parameter" prevents.
3. Give three idempotent write patterns and say when each is right.
4. Say what `INSERT` alone costs you.
5. Say why resumability requires idempotency.

### The backfill drill

1. Say why a backfill is possible at all, in terms of the two properties.
2. Compute the time for 180 days at 40 minutes, sequential and at 10 and 30 parallel.
3. Say what limits the parallelism, and it is not the orchestrator.
4. Give three operational precautions for a backfill.
5. Name three things that make a backfill impossible.

### The late-data drill

1. Give the two policies and what each costs.
2. Say how you would size the reprocessing window.
3. Say why you partition by event time and not arrival time.
4. Say what "published numbers change" means for downstream consumers.
5. Give the design that keeps some numbers frozen.

### The quality drill

1. Name the three places checks belong and give two checks for each.
2. Say why a failed check must stop rather than warn.
3. Give the join check and say what bug it catches.
4. Say why row-count bounds should be wide.
5. Name the failure that none of these checks catches.

### The incremental drill

1. Compare incremental and full refresh on correctness and on runtime.
2. Give the compromise and say what it bounds.
3. Compute the runtime difference for a 100M-row fact table.

### The numbers drill

1. Compute daily volume for 50M orders and 5B events a year, and give the ratio.
2. Break a 40-minute critical path into its stages.
3. Compute backfill time at three parallelism levels.
4. Compute the monthly compute cost of a 90-minute daily pipeline.
5. Size a reprocessing window from a lateness distribution.
6. Set a row-count alert threshold from a trailing average and justify the width.

### The failure drill

For each, say what happens and what you would build:

1. A job fails at 03:12 with a three-hour SLA buffer.
2. A job crashed halfway through an `INSERT`.
3. A job that computes "today" using `now()`, re-run tomorrow.
4. A source table stops updating but the job still succeeds.
5. A join whose right side gained a duplicate key.
6. Thirty backfill runs launched while the nightly pipeline is running.
7. A scale reading 4% light for nine days, with every job green.

Two of the seven are caught by no check you can write. Name them and say what does catch them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Connect all the cities at minimum cost.*
   Spanning tree with `V − 1` edges and no cycles, Kruskal's with Union-Find, Prim's as Dijkstra with one line
   changed, the density rule for choosing, the disconnected check, and "this is not a shortest-path tree" said
   before being asked.

2. *Why does the greedy choice work here?*
   The cut property stated precisely, then the swap argument in three sentences, then how each algorithm is an
   application of it — plus the cycle property for why skipping is safe.

3. *How does yesterday's revenue number get onto the dashboard?*
   The DAG and topological order, partitioned idempotent jobs with the execution date as a parameter,
   resumption, backfills falling out for free, late-data policy, and data quality checks that stop the run.

---

## Before you move on

- [ ] I store edges as `(weight, a, b)` and use a bare `sort()`.
- [ ] I check `len(chosen) == n - 1` before returning a total.
- [ ] I can write Kruskal's in eight lines from memory.
- [ ] I can write heap-Prim's and the dense `O(V²)` version.
- [ ] I can point at the one line that differs from Dijkstra.
- [ ] I can give the density rule with numbers.
- [ ] I can state the cut property and give the swap argument.
- [ ] I can state the cycle property and what it justifies.
- [ ] I have the triangle counter-example ready for MST-is-not-shortest-path.
- [ ] I know Kruskal's cost is dominated by the sort.
- [ ] I know Kruskal's memory constraint and when it binds.
- [ ] I know the tree is not unique with tied weights, so I assert the total.
- [ ] I know the virtual-vertex trick and the general pattern behind it.
- [ ] I know Union-Find has no direction and what the directed analogue is called.
- [ ] I can trace a number from a production write to a dashboard.
- [ ] I know a pipeline is a DAG and running it is a topological sort.
- [ ] I can state both survivability properties.
- [ ] I know why `now()` in a job is the most common pipeline bug.
- [ ] I can give three idempotent write patterns.
- [ ] I know resumability requires idempotency.
- [ ] I can explain why backfills are free, with the arithmetic.
- [ ] I know what limits backfill parallelism.
- [ ] I can give both late-data policies and what each costs.
- [ ] I know to partition by event time, not arrival time.
- [ ] I know where the three kinds of quality check belong.
- [ ] I know the before-and-after-join row count check and what it catches.
- [ ] I know a failed check must stop the run.
- [ ] I alert on the SLA, not on job failures.
- [ ] I know what none of the checks catch, and what does.
- [ ] I answered all three questions above out loud.
