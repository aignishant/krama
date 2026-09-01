---
day: 136
track: practice
title: "Practice — Dijkstra's algorithm"
status: written
---

# Day 136 · Practice

**DSA topic:** Dijkstra's algorithm
**System design topic:** Elasticsearch in a design

---

## Code these, in this order

One rule for the whole set: **write `heapq.heappush(heap, (cost, vertex))` and say "cost first" out loud.**
The reversed tuple orders the heap by vertex id, produces a confidently wrong answer, and never raises. It is
the fastest possible way to lose twenty minutes.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Network Delay Time | LeetCode 743 (Medium) | Plain Dijkstra, then `max` of the distances, then the unreachable check. |
| 2 | Path with Minimum Effort | LeetCode 1631 (Medium) | `max` instead of `+` — the generalised combining rule. |
| 3 | Cheapest Flights Within K Stops | LeetCode 787 (Medium) | The state variant, and why plain Dijkstra is wrong. |
| 4 | Swim in Rising Water | LeetCode 778 (Hard) | Same as 2, on an implicit grid. |
| 5 | Path with Maximum Probability | LeetCode 1514 (Medium) | Multiplication and a max-heap — the third combining rule. |
| 6 | Minimum Cost to Make at Least One Valid Path | LeetCode 1368 (Hard) | Weights are only 0 and 1 — use 0-1 BFS and compare. |

### On problem 3, prove plain Dijkstra fails first

Solve it with ordinary Dijkstra ignoring the stop limit, then apply the limit afterwards. Find an input where
it gives the wrong answer, and write one sentence saying why — the phrase "settled once" should appear. Then
expand the state and solve it properly. Then solve it a third time with Bellman-Ford limited to `k+1` rounds,
and say which you would write in an interview.

### On problems 2, 4 and 5, name the combining rule

For each, write down the accumulate operation and the comparison. Then state, in one sentence, the property
all three share that makes Dijkstra's proof still hold.

### On problem 6, compare against 0-1 BFS

Solve it with Dijkstra and with a deque-based 0-1 BFS. Time both on the largest input and record the ratio.
Say why the deque version has no `log` factor.

### Then the negative-weight experiment

Build this graph by hand and run your Dijkstra on it:

```
0 -> 1  cost 1
0 -> 2  cost 2
2 -> 1  cost -5
```

Record what it returns for the distance to vertex 1, and what the true answer is. Then write the one sentence
of the correctness proof that this input breaks.

### Then the stale-entry measurement

Instrument your solution to count (a) heap pushes, (b) heap pops, and (c) pops skipped as stale. Run it on a
graph with many improving paths — a dense random graph works. Three numbers. Then delete the stale check and
count how many extra neighbour scans happen.

---

### The substitution drill

1. State what Dijkstra is, in terms of BFS, in one sentence.
2. Say what the priority queue changes and what stays the same.
3. Write the eleven-line core from memory.
4. Point at the relaxation line and the lazy-deletion line and say what each does.
5. Say why the tuple is `(cost, vertex)` and not the other way round.

### The proof drill

1. State the invariant in one sentence.
2. Give the three-sentence proof.
3. Point at the exact sentence that needs non-negative weights.
4. Give a three-vertex counter-example with a negative edge.
5. Say what "extending a path never improves it" generalises to.

### The variants drill

1. Write the early-exit version and say why it returns on pop, not on discovery.
2. Write the parent-map version and say where the assignment goes.
3. Write the state-space version for a stop limit.
4. Give the state-space size for `V` vertices and `k` stops, and say when you would worry.
5. Give the `max`-instead-of-`+` version and the problem family it solves.

### The costs drill

1. Derive `O(E log E)` and explain why it is written `O((V + E) log V)`.
2. Give the array version's cost and the graph density where it wins.
3. Compute heap versus array at `V = 1,000, E = 500,000` and at `V = 100,000, E = 300,000`.
4. Compare against BFS on the same sparse graph and give the ratio.
5. Compute the memory of the heap at `V = 10^6, E = 5×10^6`.
6. Give the whole comparison table: BFS, 0-1 BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, A*.

### The break-it drill

Trigger each and record the exact output or error:

1. A negative edge, on the three-vertex graph above.
2. Returning when the target is discovered rather than popped.
3. The stale check removed — measure, do not just observe.
4. `(vertex, cost)` instead of `(cost, vertex)`.
5. Pushing an object with no tie-breaker at equal cost.
6. Dijkstra on a graph where every weight is 1 — measure against BFS.
7. Negating weights to turn a maximisation into a minimisation.

---

### The role drill

1. State what Elasticsearch is in the architecture, in one sentence.
2. State Sudha's two rules in system terms.
3. Say what "must be rebuildable" rules out.
4. Draw the write path and the read path from memory.
5. Say what the read path buys you by returning ids rather than content.

### The sync drill

1. Name the three mechanisms and reject one with a specific reason.
2. Describe the outbox version, including what is in the transaction.
3. Say what CDC catches that the outbox does not.
4. Say why indexing is idempotent for free.
5. Say why a reconciliation job is not optional, with two causes of drift.

### The mapping drill

1. State the `text` versus `keyword` distinction and what each is for.
2. Say what happens if you get it wrong and what fixing it costs.
3. Say what dynamic mapping does and why it is dangerous on user input.
4. Say which mapping changes are possible in place and which are not.

### The query drill

1. State the difference between `must` and `filter`.
2. Say why filters are cheaper, in two ways.
3. Say what belongs in each, with three examples.
4. Say what deep pagination costs and what to use instead.

### The alias drill

1. Say what an alias is and why the application must use one.
2. Give the five steps of a zero-downtime reindex.
3. Name the step people forget and what it costs.
4. Estimate the reindex time for 50M documents on 3 nodes.

### The sizing drill

1. Compute index size on disk for 50M documents at 2 KB, with a replica.
2. Derive the shard count from that.
3. Give the heap rule and the reason for the 31 GB ceiling.
4. Say why the other half of RAM matters more than the heap.
5. Give query and indexing throughput per node, bulk and single-document.

### The staleness drill

1. Decompose end-to-end staleness into its four components.
2. Give the typical total and what it becomes under load.
3. Say what you alert on and why not the configured interval.
4. Say what `?refresh=true` per write does and why it is the worst fix.
5. Give the three product answers to "I cannot find what I just created".

### The failure drill

For each, say what happens and what you would build:

1. The application writes to the database and then to Elasticsearch, and crashes in between.
2. A brand field mapped as `text`, and the product team asks for brand facets.
3. A user searches and sees a product deleted an hour ago.
4. Dynamic mapping on seller-supplied attributes, after a year.
5. A cluster goes red during a search.
6. `from: 100000` in a user-facing paginator.
7. The application queries `products_v1` directly and the mapping must change.

Two of the seven need a reindex to fix. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the shortest path in a weighted graph.*
   Dijkstra as BFS with a priority queue, the settled invariant, the three-sentence proof, the sentence that
   needs non-negative weights, lazy deletion, and returning on the pop.

2. *There is a limit of at most k stops. What changes?*
   Nothing about the algorithm and everything about the vertex — the state becomes `(city, stops)`, why plain
   Dijkstra settles too early, the state-space size computed out loud, and Bellman-Ford as the neater
   alternative here.

3. *Where does Elasticsearch sit, and how does it stay up to date?*
   Derived copy, never the source of truth, rebuildable. Outbox in one transaction, consumer, bulk index.
   Search returns ids and the app hydrates. Staleness as a number. Reconciliation as a requirement.

---

## Before you move on

- [ ] I can state Dijkstra in terms of BFS in one sentence.
- [ ] I write `(cost, vertex)` and say "cost first".
- [ ] I can write the eleven-line core from memory.
- [ ] I can state the settled invariant and give the three-sentence proof.
- [ ] I can point at the sentence that requires non-negative weights.
- [ ] I have a three-vertex negative-weight counter-example ready.
- [ ] I know why lazy deletion exists and what the check costs to omit.
- [ ] I return on the pop, not on the discovery, and can say why.
- [ ] I put the parent assignment inside the relaxation.
- [ ] I can write the state-space variant and compute the state-space size.
- [ ] I know the `max`-instead-of-`+` family and the property that makes it valid.
- [ ] I can derive the complexity and explain the two ways of writing it.
- [ ] I know where the array version beats the heap version.
- [ ] I know Dijkstra is ~13× BFS and would say "BFS" when weights are equal.
- [ ] I can give the six-algorithm comparison table.
- [ ] I know Elasticsearch is a derived copy and must be rebuildable.
- [ ] I can draw both paths from memory.
- [ ] I know why search returns ids and not content.
- [ ] I can reject dual write with a specific reason.
- [ ] I know what CDC catches that the outbox does not.
- [ ] I know why a reconciliation job is required.
- [ ] I can state `text` versus `keyword` and what getting it wrong costs.
- [ ] I know why dynamic mapping is dangerous on user input.
- [ ] I know the `must` versus `filter` distinction and what belongs where.
- [ ] I query an alias, never a concrete index.
- [ ] I can give the five reindex steps and name the forgotten one.
- [ ] I can size shards from data volume and give the heap and cache rules.
- [ ] I can decompose staleness and say what I alert on.
- [ ] I know what forcing a refresh per write does.
- [ ] I answered all three questions above out loud.
