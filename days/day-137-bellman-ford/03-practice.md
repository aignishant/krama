---
day: 137
track: practice
title: "Practice — Bellman-Ford, and what negative edges break"
status: written
---

# Day 137 · Practice

**DSA topic:** Bellman-Ford, and what negative edges break
**System design topic:** Time-series and metrics stores

---

## Code these, in this order

One rule for the whole set: **before writing a line, check the weights and say which algorithm applies.** All
equal → BFS. Only 0 and 1 → deque BFS. Non-negative → Dijkstra. It is a DAG → one topological pass, whatever
the weights. Negative and cyclic → Bellman-Ford. Reaching for Bellman-Ford on a non-negative graph is a
seven-hundred-fold slowdown for nothing.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Cheapest Flights Within K Stops | LeetCode 787 (Medium) | `k+1` rounds — the round count *is* the edge limit. |
| 2 | Network Delay Time | LeetCode 743 (Medium) | Solve with both, and compare the operation counts. |
| 3 | Currency arbitrage | Not on LeetCode — build it | The `−log(rate)` transformation and cycle detection. |
| 4 | Find the City With the Smallest Number of Neighbors | LeetCode 1334 (Medium) | Floyd-Warshall, and why `V ≤ 100` permits it. |
| 5 | Minimum Cost to Make at Least One Valid Path | LeetCode 1368 (Hard) | 0-1 BFS — the algorithm the decision table picks. |

### On problem 1, write the copy explicitly

The version that reads and writes the same array in a round chains two flights together and allows more stops
than intended. Write both versions, run them on the LeetCode example with `k = 1`, and record the two answers.
Then write one sentence saying what a "round" means in the correctness proof.

### On problem 2, count the operations

Instrument both solutions to count edge relaxations. Run on the largest input. Two numbers, and the ratio
should be roughly what the complexity predicts. Then say which you would write in the interview and why.

### On problem 3, build it yourself

Take five currencies and a rate matrix. Convert each rate to `−log(rate)`, run Bellman-Ford with the extra
round, and report whether arbitrage exists. Then plant an arbitrage cycle deliberately and check you find it —
and extract the actual sequence of trades with the parent-walk trick.

Then add a 0.3% fee to every trade and see whether the arbitrage survives. It usually does not, and that is
the point.

### Then the Dijkstra failure

Build the three-vertex graph — `S→A` cost 1, `S→B` cost 2, `B→A` cost −5 — and run your Dijkstra from
[day 136](../day-136-dijkstra/README.md) on it. Record the distance it gives for `A` and the true answer.
Then write out the sentence of the correctness proof that this input breaks.

### Then the sentinel experiment

Run Bellman-Ford with `INF = float("inf")` and again with `INF = 10**18`, on a graph with an unreachable
vertex that has a negative outgoing edge — and with the `distance[u] != INF` guard removed in both cases.
Record all four outputs. One of them is quietly catastrophic.

---

### The why-not-Dijkstra drill

1. State Dijkstra's correctness clause and point at the part negative edges delete.
2. Give a three-vertex counter-example with the numbers.
3. Say what Dijkstra returns and what the truth is.
4. Name the transformation that accidentally creates negative weights.

### The algorithm drill

1. Write Bellman-Ford from memory in eight lines.
2. Say why an edge list is the right representation here.
3. Explain why `V − 1` rounds are enough, using the induction.
4. Say why edge order does not affect correctness.
5. Say what the early exit is and why it is valid.

### The negative-cycle drill

1. Say what a negative cycle means for the answer.
2. Write the detection in six lines.
3. Say why one extra round is sufficient.
4. Distinguish "the graph has a negative cycle" from "this vertex is −∞".
5. Describe the parent-walk trick for extracting the cycle and say why the `n` steps are needed.

### The SPFA drill

1. Write it from memory.
2. Say what the optimisation actually is, in one sentence.
3. Give its worst case and say what you must not claim.
4. Say how it detects a negative cycle without an extra round.

### The decision-table drill

Say the algorithm and its cost for each, from memory:

1. Every edge costs the same.
2. Weights are only 0 and 1.
3. Weights are non-negative.
4. Weights can be negative.
5. The graph is a DAG with arbitrary weights.
6. All pairs, `V = 200`.
7. All pairs, `V = 10,000`, sparse, with negatives.

### The costs drill

1. Compute Bellman-Ford against Dijkstra at `V = 10,000, E = 50,000`.
2. Give the practical round count with early exit and recompute.
3. Give Floyd-Warshall's cost at `V = 100`, `500` and `1,000`.
4. Say what Floyd-Warshall buys that justifies it at small `V`.
5. Name Johnson's algorithm, its cost, and when it wins.

### The break-it drill

Trigger each and record the exact output or error:

1. Bellman-Ford on a positive-weight graph with `V = 10,000` — time it.
2. The `INF` guard removed with an integer sentinel.
3. `range(n)` instead of `range(n-1)`, then the cycle check.
4. An "undirected" graph with one negative edge.
5. Float weights with an exact `<` comparison, on a graph with no negative cycle.
6. Reporting "no solution" for a graph with a negative cycle in one corner.

---

### The four-properties drill

1. Name the four properties of time-series data.
2. Say what optimisation each one buys.
3. Give the compression figure, before and after.
4. Explain delta-of-delta in one sentence and say why it is usually zero.
5. Explain XOR float compression in one sentence.

### The cardinality drill

1. Define a series precisely.
2. Say what memory scales with, and what it does *not* scale with.
3. Work the `20 × 4 × 8 × 200 × 12 × 1,000,000` example out loud.
4. Give three labels you must never use and say where that data belongs instead.
5. Describe how a monitoring system dies from a one-line application change.
6. Give the three-part fix, and say which part is the real one.

### The retention drill

1. Give a three-tier retention policy with numbers.
2. Compute storage for each tier on 500,000 series.
3. Compare against keeping raw for two years.
4. Say what a rollup must store besides the mean, and why.
5. Say what downsampling buys beyond storage.

### The percentiles drill

1. Say why you cannot average percentiles.
2. Describe how a histogram fixes it, and where the summing happens.
3. Say what histograms cost in cardinality.
4. Say what limits the accuracy and what fixes it.
5. Say what a summary computes instead and why it cannot be aggregated.

### The why-not-Postgres drill

1. Give the four reasons with numbers.
2. Say which one partitioning fixes and which two it does not.
3. Give ingestion rates for Postgres and for a purpose-built store.
4. Say when a Postgres table is genuinely the right answer.
5. Say what TimescaleDB is for, with the query that motivates it.

### The push-pull drill

1. Describe both models.
2. Give three advantages of pull.
3. Give two things pull cannot do.
4. Say what `up` is and why it matters.

### The numbers drill

1. Size a metrics store for 500 machines × 1,000 metrics at 15 s.
2. Convert that to points per second and gigabytes per day, compressed and not.
3. Compute Prometheus memory for 500,000 and for 10,000,000 series.
4. Compute query cost for "p99 by endpoint over 30 days", raw and rolled up.
5. Compare self-hosted cost against per-host managed pricing at 500 hosts.

### The failure drill

For each, say what happens and what you would build:

1. A `path` label containing order ids is added to an HTTP histogram.
2. A counter's process restarts mid-window.
3. Someone averages per-host p99s for a fleet dashboard.
4. A rollup that stores only the mean, and an incident from six months ago.
5. Prometheus running inside the cluster it monitors, during a cluster outage.
6. A short-lived batch job that finishes between scrapes.
7. A metrics table in Postgres at a million rows a second.

Two of the seven are working as designed and need a different tool, not a fix. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why can't you use Dijkstra here?*
   The correctness clause and the exact part negative edges delete, the three-vertex counter-example with
   numbers, then Bellman-Ford, the `V − 1` induction, and the extra round for cycles.

2. *Detect arbitrage between these currencies.*
   Currencies as vertices, `−log(rate)` as the weight and why, profitable cycle becomes negative cycle,
   detection in one extra round, extracting the trades — and the two practical caveats.

3. *Where would you store the metrics for this system?*
   The four properties and what each buys, the compression figure, the sizing arithmetic for a real fleet,
   downsampling tiers — and cardinality raised before being asked.

---

## Before you move on

- [ ] I check the weights and pick the algorithm before writing anything.
- [ ] I can state Dijkstra's failing clause exactly.
- [ ] I have a three-vertex negative counter-example ready with numbers.
- [ ] I can write Bellman-Ford in eight lines from memory.
- [ ] I know why an edge list is the right representation here.
- [ ] I can give the `V − 1` induction.
- [ ] I know edge order does not affect correctness.
- [ ] I use the early exit and can say why it is valid.
- [ ] I can write the negative-cycle check and say why one round suffices.
- [ ] I distinguish "has a negative cycle" from "this vertex is −∞".
- [ ] I know the parent-walk trick and why it needs `n` steps.
- [ ] I can write SPFA and will not claim it is asymptotically better.
- [ ] I know the `INF` guard is mandatory with an integer sentinel.
- [ ] I know `range(n)` instead of `range(n-1)` breaks cycle detection.
- [ ] I know an undirected negative edge is always a negative cycle.
- [ ] I can recite the whole decision table with costs.
- [ ] I can name Johnson's algorithm and when it wins.
- [ ] I can name the four properties of time-series data and what each buys.
- [ ] I can explain delta-of-delta and XOR compression.
- [ ] I can quote the bytes-per-point figure.
- [ ] I can define a series and say what memory scales with.
- [ ] I can work the cardinality multiplication out loud.
- [ ] I know the three labels never to use and where that data belongs.
- [ ] I can give the three-part fix for cardinality and name the real one.
- [ ] I can give a retention policy with sizing arithmetic.
- [ ] I know a rollup stores min, max, sum and count.
- [ ] I know why percentiles cannot be averaged and how histograms fix it.
- [ ] I know histograms multiply cardinality by their bucket count.
- [ ] I can give the four reasons Postgres fails, with numbers.
- [ ] I know when Postgres and when TimescaleDB are the right answers.
- [ ] I answered all three questions above out loud.
