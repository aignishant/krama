---
day: 130
track: practice
title: "Practice — Grids are graphs: islands and flood fill"
status: written
---

# Day 130 · Practice

**DSA topic:** Grids are graphs: islands and flood fill
**System design topic:** Kafka, explained

---

## Code these, in this order

One rule for the whole set: **write the neighbour function with its bounds check first, as a separate
function, before you write anything else.** Every problem below uses it unchanged. Doing it once properly is
the difference between five clean solutions and five chances to forget one of the four comparisons.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Flood Fill | LeetCode 733 (Easy) | The neighbour function, and the case where the new colour equals the old. |
| 2 | Number of Islands | LeetCode 200 (Medium) | The double loop as the outer loop, iteratively. |
| 3 | Max Area of Island | LeetCode 695 (Medium) | Component sizes, and returning 0 on an empty grid. |
| 4 | Rotting Oranges | LeetCode 994 (Medium) | Multi-source BFS, level counting, and the `-1` case. |
| 5 | Surrounded Regions | LeetCode 130 (Medium) | Flooding from the border — the inverted question. |
| 6 | Making A Large Island | LeetCode 827 (Hard) | Labelling plus the *distinct* neighbouring ids. |

### On problem 1, find the infinite loop

Run it with the new colour equal to the starting colour. Record what happens. Then say in one sentence why the
`seen` mechanism failed, and write the one-line guard.

### On problem 2, run the four failure modes

On a 1,000 × 1,000 grid of all land:

1. Recursive flood.
2. Recursive after `sys.setrecursionlimit(2_000_000)`.
3. Iterative, marking on pop — record peak stack length.
4. Iterative, marking on push — record peak stack length.

Then run BFS instead of DFS on the same grid and record the peak *queue* length. Compare it with (4). That
number is the argument for BFS on grids.

### On problem 4, build the impossible case

Construct a grid with a fresh orange that no rotten one can reach. Verify your solution returns `-1` and not
a number. Then delete the `fresh` counter and record what it returns instead.

### On problem 6, break the distinct check

Solve it, then replace the set of neighbouring island ids with a list. Find a grid where the two versions
disagree — a U shape works — and record both answers.

### Then the wrap-around experiment

Take your island counter, remove the bounds check entirely, and run it on:

```
1001
0000
0000
1001
```

Record the answer. Then say which of the four comparisons was responsible, and why the failure is silent in
one direction and an `IndexError` in the other.

---

### The model drill

1. Say what a vertex is and what an edge is, for a grid.
2. Say what "implicit graph" means and why grids are the classic case.
3. Write the four-way offsets and the eight-way offsets from memory.
4. Give a grid where four-way and eight-way give different island counts.
5. Say what one line of translation turns a graph algorithm into a grid algorithm.

### The bounds drill

1. Write the check from memory. Count the comparisons.
2. Say what `grid[-1][3]` returns and why that is worse than an error.
3. Say which direction raises `IndexError` and which does not.
4. Say what shape the grid effectively becomes without the check.

### The traversal-choice drill

1. Give both frontier sizes on a 1,000 × 1,000 open grid, BFS and DFS.
2. Say why that is the opposite of the general graph case.
3. Say when BFS is mandatory rather than preferable.
4. Say what recursion costs and what raising the limit costs.
5. Give the grid size below which recursion is safe.

### The costs drill

1. Give `V` and `E` for an `r × c` grid and simplify `O(V + E)`.
2. Compute total operations for a 1,000 × 1,000 grid.
3. Compare the memory of a `visited` list-of-lists against a `bytearray`.
4. Give the cost of multi-source BFS with `k` sources and say why `k` does not appear.
5. Compute the naive alternative for 500 gates on a million cells.

### The multi-source drill

1. Say what the one-line change is.
2. Say why each cell still gets the distance to its *nearest* source, with no comparison.
3. Give three problem statements that are this shape and the words that give it away.
4. Say how you count levels rather than steps, and where that loop goes.

### The break-it drill

Trigger each and record the exact output or error:

1. No bounds check, on the four-corner grid.
2. Marking on pop, on a million-cell all-land grid.
3. Recursion on the same grid, before and after raising the limit.
4. `[[False] * cols] * rows` as the visited grid.
5. Flood fill where the new colour equals the old.
6. Rotting oranges with the `fresh` counter removed.
7. One BFS per gate, with 500 gates on a 1,000 × 1,000 grid.

---

### The log-not-a-queue drill

1. State the one difference between Kafka and a queue, and three things that follow from it.
2. Define topic, partition, offset, consumer group — one line each.
3. Say what happens to a message when a consumer reads it.
4. Say what it costs the cluster to add a fifth consumer group.

### The ordering drill

1. Answer "how does Kafka guarantee ordering?" in two sentences, narrowing the claim first.
2. Say how a message's partition is chosen.
3. Say what ordering guarantee keying by `user_id` gives you, and what it does not.
4. Explain the ordering-versus-parallelism trade in one sentence.
5. Describe a hot partition, give an example key that causes one, and say why more brokers do not help.

### The consumer-group drill

1. Say how partitions are assigned within a group.
2. Say what happens with 12 partitions and 17 consumers.
3. Say what a rebalance is and name three things that trigger it.
4. Name the classic rebalance incident and the two settings involved.
5. Say what cooperative sticky assignment changes.

### The durability drill

1. Give the three `acks` settings and what each loses.
2. Say what `replication.factor=3, min.insync.replicas=2` guarantees.
3. Say why `min.insync.replicas=1` is the dangerous-looking-safe setting.
4. Say what the idempotent producer dedupes, and its exact scope.
5. Say where exactly-once stops, precisely.

### The offsets drill

1. Say where consumer offsets are stored.
2. Give the three commit strategies and the guarantee each produces.
3. Say what the default gives you on a crash, and why that is usually wrong.
4. Say what redelivery forces on every consumer.

### The numbers drill

1. Give per-broker throughput in MB/s and messages/s.
2. Size a cluster for 1M messages/s at 1 KB, showing the replication step.
3. Compute 7-day storage before and after compression.
4. Compute the partition count from both the throughput and the parallelism constraints.
5. Compute time-to-data-loss for a lag growing at 5,000/s with 7-day retention.
6. Give end-to-end latency, tuned for throughput and tuned for latency.
7. Compute the lag created by a 10-second rebalance at 50,000 msg/s.

### The trade-offs drill

1. State the ordering-parallelism trade as a sentence.
2. State the retention-cost trade with a number.
3. Say what Kafka gives you that a queue does not, and vice versa.
4. Say why partition count is chosen early and what breaks when you change it.
5. Name four situations where Kafka is the wrong tool.

### The failure drill

For each, say what happens and what you would build:

1. A broker dies after acknowledging with `acks=1`.
2. A consumer's lag exceeds the retention period.
3. A malformed message that fails on every attempt.
4. A key where one value is 30% of all traffic.
5. Seventeen consumers on a twelve-partition topic.
6. A consumer that takes six minutes to process a batch.
7. The database commit succeeds and the Kafka publish fails.

Two of the seven lose data silently. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Count the number of islands.*
   Cells as vertices and touching as edges, the implicit graph, the double loop as the outer loop, iterative
   with marking on push, the bounds check as four comparisons with the wrap-around consequence, and
   `O(rows × cols)`.

2. *How long until every orange rots?*
   Multi-source BFS with all sources pushed before the loop, why the nearest-source distance falls out with
   no comparison, level counting for minutes, the `-1` case, and the arithmetic against one-BFS-per-source.

3. *How does Kafka guarantee ordering?*
   Narrow the claim first — per partition only — then keys and hashing, per-entity ordering as the guarantee
   that matters, the parallelism trade, and hot partitions as the failure mode more brokers cannot fix.

---

## Before you move on

- [ ] I can say what a vertex and an edge are for a grid.
- [ ] I write the neighbour function with bounds first, as its own function.
- [ ] I can write the four-way and eight-way offsets from memory.
- [ ] I know what `grid[-1]` does and why that failure is silent.
- [ ] I know which direction raises `IndexError` and which does not.
- [ ] I write grid traversals iteratively and know the two crash modes.
- [ ] I mark on push and know the stack size if I do not.
- [ ] I know BFS's and DFS's frontier sizes on an open grid.
- [ ] I know when BFS is mandatory.
- [ ] I can simplify `O(V + E)` to `O(rows × cols)` and say why.
- [ ] I know the memory cost of a visited grid and the `bytearray` alternative.
- [ ] I can spot multi-source BFS from the words in a statement.
- [ ] I know the one-line change and why `k` does not appear in the cost.
- [ ] I know to flood from the border when the condition is about reaching the edge.
- [ ] I know Kafka is a log and can name three consequences.
- [ ] I can define topic, partition, offset and consumer group.
- [ ] I can answer the ordering question by narrowing the claim first.
- [ ] I know how a partition is chosen and what a good key looks like.
- [ ] I can describe a hot partition and say why more brokers do not help.
- [ ] I know what happens with more consumers than partitions.
- [ ] I can name three rebalance triggers and the classic incident.
- [ ] I can give the three `acks` settings and what each loses.
- [ ] I know why `min.insync.replicas=1` is dangerous.
- [ ] I know exactly where Kafka's exactly-once stops.
- [ ] I know where offsets live and what the default commit gives me on a crash.
- [ ] I can size a cluster and its storage with the replication and compression steps.
- [ ] I can compute time-to-data-loss from a lag growth rate.
- [ ] I monitor lag as a time, not a count.
- [ ] I know Kafka has no per-message retry or DLQ, and what I build instead.
- [ ] I answered all three questions above out loud.
