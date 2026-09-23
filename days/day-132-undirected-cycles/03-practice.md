---
day: 132
track: practice
title: "Practice — Cycle detection in an undirected graph"
status: written
---

# Day 132 · Practice

**DSA topic:** Cycle detection in an undirected graph
**System design topic:** Stream processing basics

---

## Code these, in this order

One rule for the whole set: **your first test is two vertices and one edge, and it must return "no cycle".**
Write that assertion before you write the function. It is the only test that catches the missing parent check,
and every other test you would think of passes without it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Graph Valid Tree | LeetCode 261 (Medium) | Connected *and* acyclic, and the `E = V−1` shortcut. |
| 2 | Redundant Connection | LeetCode 684 (Medium) | Union-Find, and returning *which* edge closed the cycle. |
| 3 | Number of Connected Components | LeetCode 323 (Medium) | The same Union-Find, counting instead of detecting. |
| 4 | Find Critical and Pseudo-Critical Edges | LeetCode 1489 (Hard) | Cycles inside a minimum-spanning-tree build. |
| 5 | Detect Cycles in 2D Grid | LeetCode 1559 (Medium) | The parent check on an implicit grid graph. |

### On problem 1, use the shortcut first

Before writing any traversal, check `len(edges) == n - 1`. Say out loud what each of the three cases
(`>`, `<`, `=`) tells you. Then write the single traversal that finishes the job, and explain in one sentence
why checking connectivity alone is now sufficient.

### On problem 5, notice what "parent" means on a grid

The grid version has the same trap in a different costume: the cell you came from is always a neighbour. Write
down what you pass down instead of a vertex id, and why `(r, c)` coordinates work directly.

### Then the two-vertex experiment

Write the naive version — `if neighbour in seen: return True`, no parent — and run it on:

1. Two vertices, one edge.
2. A path of five vertices.
3. A triangle.

Record all three answers. Two of them are wrong. Then add the parent check and rerun.

### Then the parallel-edge experiment

Build a graph with two separate edges between vertices 0 and 1. Run:

1. The DFS parent-by-vertex version.
2. The DFS parent-by-edge-id version.
3. The Union-Find version.

Record all three answers. One of them is wrong, and it is the one you would have written by default.

### Then the online comparison

Take 20,000 vertices and 20,000 edges arriving one at a time, and print whether a cycle exists after each
edge. Do it once by re-running the traversal and once with Union-Find. Time both. The ratio is the argument.

---

### The condition drill

1. State the cycle condition for an undirected graph in one line.
2. Say why "already seen" alone is wrong, and on what input it fails.
3. Say what you pass down and what the root's value is.
4. Say why the directed version cannot use this, and what it uses instead.
5. Say when excluding by vertex is not enough.

### The two-algorithms drill

1. Write the DFS version from memory.
2. Write the BFS version from memory and say where the parent lives.
3. Say when you would choose BFS.
4. Say what a self-loop does to each, and how you would handle it.

### The Union-Find drill

1. Write `find` with path compression from memory.
2. Say in one sentence why an edge between two same-group vertices means a cycle.
3. Give the cost per operation and what alpha means.
4. Say when Union-Find is not just an alternative but the only option, with the arithmetic.
5. Say what Union-Find catches that the DFS parent check misses.

### The counting-shortcut drill

1. State the three arithmetic cases and what each decides.
2. Say why `E = V−1` alone decides nothing without connectivity.
3. Give the one-comparison answer for a promised-connected graph.
4. Say why, once `E = V−1`, checking only connectivity is enough for "is this a tree".

### The costs drill

1. Give time and space for DFS, BFS and Union-Find.
2. Say why early exit matters and what the worst case is.
3. Compare memory constants for the three at `V = 10^6`.
4. Compute traversal-per-edge versus Union-Find for `m = 100,000`.

### The break-it drill

Trigger each and record the exact output or error:

1. The naive check on two vertices and one edge.
2. Parent-by-vertex on a graph with parallel edges.
3. Starting from vertex 0 only, with the cycle among vertices 7–9.
4. The three-colour directed algorithm on an undirected graph.
5. The parent check on a directed graph with a real cycle.
6. Recursive DFS on a 100,000-vertex path.

---

### The out-of-order drill

1. Say in one sentence why stream processing is hard.
2. Define event time and processing time, and give an example where they differ by minutes.
3. Say why processing time makes numbers non-reproducible.
4. Say when processing time is the right choice.

### The windows drill

1. Define tumbling, sliding and session windows in one line each.
2. Say how many windows an event belongs to in each.
3. Compute the state multiplier for a 5-minute window sliding every 10 seconds.
4. Give the cheaper alternative to a sliding window and what it costs.
5. Say what decides a session's gap parameter.

### The watermark drill

1. Define a watermark precisely.
2. Give the usual formula for computing one.
3. Say where the allowance number comes from.
4. Say why the watermark only advances when events arrive, and the incident that causes.
5. Say why the job's watermark is the minimum across partitions.

### The lateness drill

1. Name the three policies for a late event.
2. Say which is right for a dashboard, for an hourly total, and for billing.
3. Distinguish the watermark from allowed lateness — two different numbers, two different jobs.
4. Say what a side output is for and why dropping silently is worse.
5. Say what late firing forces on every downstream consumer.

### The numbers drill

1. Compute state for 10M keys, one-minute tumbling windows.
2. Recompute with ten minutes of allowed lateness.
3. Recompute for a 5-minute sliding window every 10 seconds.
4. Given a delay distribution (p50 1.2 s, p99 45 s, p99.9 4 min), choose a watermark and state what it drops.
5. Break down end-to-end latency and name the dominant term.
6. Compute discarded events per day at 1M/min and a 0.1% late rate.
7. Size the state for a 30-minute stream-to-stream join at 1M impressions a minute.

### The correctness drill

1. Say how you find out whether the streaming numbers are right.
2. Describe the batch recount and what you publish from it.
3. Name the architecture that pairs them and the criticism of it.
4. Give the modern alternative and what it requires.
5. Say exactly where Flink's exactly-once guarantee stops.

### The trade-offs drill

1. State the latency-versus-completeness trade in one sentence.
2. Say what allowed lateness costs, in more than just memory.
3. Say why many teams choose to be slightly wrong, and when that is right.
4. Give three cases where a batch job beats a streaming job.
5. Say what makes a mis-tuned watermark worse than a failed batch job.

### The failure drill

For each, say what happens and what you would build:

1. A region goes quiet at 2 a.m. and the dashboard stops updating.
2. An event arrives an hour after its window closed.
3. A viral video makes one partition 40% of all traffic.
4. Allowed lateness is set to one hour on a one-minute window over 10M keys.
5. A sink that appends rather than upserts, with late firing enabled.
6. Someone asks for "real-time and exactly right".
7. The streaming total and the batch total differ by 0.014%.

Two of the seven are working as designed. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Does this undirected graph contain a cycle?*
   The condition with the parent check, why "seen" alone fails on two vertices and one edge, the outer loop,
   the parallel-edge question asked rather than assumed, and the `E > V−1` shortcut offered first.

2. *Given `n` nodes and these edges, is this a valid tree?*
   The arithmetic first, then why one traversal is now enough, then the Union-Find alternative and the case
   where it is the only option.

3. *How do you count events per minute when events arrive late?*
   Event time not processing time and why; the watermark as a chosen number from a measured distribution; the
   three lateness policies with the one you would pick; the side output; and the state cost of allowed
   lateness.

---

## Before you move on

- [ ] My first test is two vertices and one edge.
- [ ] I can state the undirected cycle condition in one line.
- [ ] I know why "already seen" alone is wrong and on what input.
- [ ] I can write both the DFS and BFS versions from memory.
- [ ] I know why the directed version needs a different mechanism.
- [ ] I ask about parallel edges and self-loops rather than assuming.
- [ ] I know excluding by edge id fixes the parallel-edge case.
- [ ] I always loop over every vertex with a shared `seen`.
- [ ] I can write Union-Find with path compression from memory.
- [ ] I can say in one sentence why it detects cycles.
- [ ] I know when Union-Find is the only option, with numbers.
- [ ] I know what Union-Find catches that the parent check misses.
- [ ] I can state the three arithmetic cases and what each decides.
- [ ] I know why `E = V−1` alone decides nothing.
- [ ] I know why connectivity alone finishes the tree question.
- [ ] I can compare the memory constants of all three approaches.
- [ ] I can say why stream processing is hard, in one sentence.
- [ ] I can define event time and processing time and say which to use.
- [ ] I can define a watermark precisely and give the formula.
- [ ] I know where the allowance number comes from.
- [ ] I know why an idle partition freezes the output.
- [ ] I can name the three lateness policies and pick one per use case.
- [ ] I know the watermark and allowed lateness are different numbers.
- [ ] I always send late events to a side output.
- [ ] I know what late firing forces on the sink.
- [ ] I can compute state for tumbling, sliding and lateness-extended windows.
- [ ] I know the watermark lag dominates end-to-end latency.
- [ ] I can describe the batch recount and what it buys.
- [ ] I know exactly where exactly-once stops.
- [ ] I answered all three questions above out loud.
