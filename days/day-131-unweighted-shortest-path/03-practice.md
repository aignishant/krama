---
day: 131
track: practice
title: "Practice — Shortest path in an unweighted graph"
status: written
---

# Day 131 · Practice

**DSA topic:** Shortest path in an unweighted graph
**System design topic:** Publish-subscribe versus point-to-point

---

## Code these, in this order

One rule for the whole set: **before writing anything, answer out loud "does every move cost exactly the
same?"** If yes, BFS and say so. If no, name what you would use instead. Two of the problems below are
deliberately chosen to make you check.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Shortest Path in Binary Matrix | LeetCode 1091 (Medium) | BFS on a grid with eight directions, and the blocked-start case. |
| 2 | Word Ladder | LeetCode 127 (Hard) | The implicit neighbour function, then bidirectional. |
| 3 | Open the Lock | LeetCode 752 (Medium) | An implicit state graph, plus a set of forbidden vertices. |
| 4 | Minimum Genetic Mutation | LeetCode 433 (Medium) | The same shape as 2, small enough to write in ten minutes. |
| 5 | Number of Ways to Arrive at Destination | LeetCode 1976 (Medium) | Counting shortest paths — **and it is weighted.** Check first. |

### On problem 5, notice the trap before you write

Read the constraints. The roads have times on them. Say out loud what that does to BFS's guarantee, and what
you need instead. Then write the counting logic — the `elif` idea is the same, only the search underneath
changes.

### On problem 2, write three versions and count

1. Build the graph explicitly by comparing every pair of words.
2. BFS with generated neighbours.
3. Bidirectional BFS with generated neighbours.

For each, count how many words are examined and how long it takes on the largest LeetCode case. Three pairs of
numbers. The ratio between (1) and (2) is the modelling win; between (2) and (3) is the search win.

### On problem 3, add path reconstruction

The problem asks only for the number of turns. Return the actual sequence of combinations as well, using a
parent map. Then check whether your answer is the only shortest sequence, by counting them.

### Then the weighted counter-example

Build this graph by hand:

```
A --1-- B --1-- C
A ----10-------- C
```

Run your BFS shortest-path function on it, ignoring the weights. Record the path it returns and its true cost.
Write one sentence explaining exactly which step of the correctness proof fails.

---

### The guarantee drill

1. State the guarantee in one sentence.
2. Give the three-sentence proof.
3. Name the exact step that fails when edges are weighted.
4. Say what "a shortest path" versus "the shortest path" means and why it matters for tests.
5. Say when you may stop early, and why that is safe.

### The variants drill

1. Write the distance version from memory.
2. Write the path version and the rebuild.
3. Write the counting version and point at the `elif`.
4. Say what changes to list *all* shortest paths, and what its complexity is bounded by.
5. Give a graph shape where the number of shortest paths is exponential.

### The bidirectional drill

1. Give the cost of one-directional and bidirectional search in terms of `b` and `d`.
2. Compute both for `b = 200`, `d = 6`.
3. Say why you always expand the smaller frontier.
4. Say where the meeting check goes and why not later.
5. Say what changes on a directed graph.
6. Name two situations where bidirectional is useless.

### The boundary drill

1. Give the one-line test for whether BFS applies.
2. Name the three situations that look unweighted and are not.
3. Describe 0-1 BFS and say why it stays linear.
4. Give the costs of BFS, 0-1 BFS, Dijkstra, Bellman-Ford and Floyd-Warshall.
5. Compute BFS versus Dijkstra on `V = 100,000`, `E = 500,000` and give the ratio.

### The break-it drill

Trigger each and record the exact output or error:

1. BFS on the weighted counter-example above.
2. Marking on pop, on a graph with 12 million edges.
3. `shortest_distance(graph, x, x)` without the equality check.
4. `graph[current]` on a plain dict with an isolated vertex.
5. Bidirectional search on a directed graph without reversed edges.
6. A test asserting one specific shortest path, with the adjacency order changed.
7. Counting shortest paths with the `elif` removed, on a diamond.

---

### The two-shapes drill

1. Define point-to-point and pub-sub in one line each.
2. Say what adding a consumer does in each case.
3. Give the smell of the wrong choice, in one sentence.
4. Say which shape cares about completion and which about the announcement.
5. Give the parcel and the shout for a real system you know.

### The fan-out drill

1. Draw the fan-out shape from memory.
2. Say what the topic gives you and what the per-consumer queue gives you.
3. Say what happens to the warehouse consumer when the email consumer hits a poison message.
4. Name the AWS services and the Kafka equivalent.
5. Say what changes when a fourth team wants the data.

### The systems drill

1. For each of SQS, SNS, RabbitMQ fanout, Kafka, Redis pub-sub, Redis Streams: which shape, and does it retry?
2. Explain RabbitMQ's four exchange types in one line each.
3. State Kafka's both-shapes sentence precisely.
4. Say what Kafka does not give you that SQS does.

### The Redis drill

1. Say exactly what `PUBLISH` delivers to and what it does not.
2. Name three cases where that is the right behaviour.
3. Say why the failure is worse than an error.
4. Give the durable alternative and one fallback for detecting loss.

### The events-versus-commands drill

1. Define each in one sentence.
2. Give the naming tell.
3. Say which shape each belongs to.
4. Say what goes wrong when you broadcast a command.
5. State the design advice that follows, and why.

### The numbers drill

1. Compute delivery volume for 10,000 events/s at 2 KB, point-to-point and fanned out to five.
2. Compare stored copies for SNS→SQS and Kafka with five consumers.
3. Compute the monthly SQS bill at 864M messages, with and without batching.
4. List what changes when adding a subscriber, in each shape.
5. Give throughput limits for SQS standard, SQS FIFO, SNS and Redis pub-sub.

### The trade-offs drill

1. Say what pub-sub costs you in visibility, and the mitigation.
2. Say what point-to-point costs you in flexibility.
3. Say what fan-out multiplies.
4. Give the three places to filter and the rule for choosing.
5. Say what neither shape helps with.
6. Name three cases where you would not use pub-sub.

### The failure drill

For each, say what happens and what you would build:

1. The producer writes to five queues and dies after the third.
2. A subscriber restarts during a Redis `PUBLISH`.
3. A command is published to a topic with five subscribers.
4. A poison message in a shared queue serving three teams.
5. A topic with eleven subscribers, three of them abandoned.
6. Five SQS queues at 864M messages a month with no batching.
7. An event consumer that is not idempotent, after a crash before acknowledgement.

Two of the seven fail silently. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the shortest path from A to B. Why does BFS work here?*
   The guarantee, then the three-sentence proof, then the parent map and rebuild, then the unweighted
   assumption named before being asked — with the counter-example ready.

2. *The graph has ten million vertices. Make it faster.*
   Bidirectional search, the `b^d` versus `2·b^(d/2)` arithmetic with real numbers, expanding the smaller
   frontier, the meeting check placement, and the reversed-edges caveat for directed graphs.

3. *One event, five consumers. Queue or topic?*
   Fan-out, and the reason stated as coupling rather than delivery — then the per-consumer queue for retries
   and DLQs, the AWS and Kafka shapes, and the storage multiplication named as the cost.

---

## Before you move on

- [ ] I can state the shortest-path guarantee precisely.
- [ ] I can give the three-sentence proof.
- [ ] I know which step of the proof weights break.
- [ ] I can write the distance, path and counting versions from memory.
- [ ] I know why the counting version needs an `elif` and what it checks.
- [ ] I know listing all paths can be exponential and counting them is linear.
- [ ] I say "a shortest path" and know why tests must not assert one.
- [ ] I handle `start == goal` explicitly.
- [ ] I can implement bidirectional BFS.
- [ ] I can do the `b^d` versus `2·b^(d/2)` arithmetic.
- [ ] I know to always expand the smaller frontier.
- [ ] I know the backward search needs reversed edges on a directed graph.
- [ ] I can name two cases where bidirectional is useless.
- [ ] I can give the one-line test for whether BFS applies.
- [ ] I can name the three unweighted-looking-but-not cases.
- [ ] I know what 0-1 BFS is and why it stays linear.
- [ ] I can compare BFS and Dijkstra with numbers.
- [ ] I can define point-to-point and pub-sub and say what adding a consumer does to each.
- [ ] I can name the smell of the wrong choice.
- [ ] I can draw the fan-out shape and say what each half buys.
- [ ] I know the AWS and Kafka versions of fan-out.
- [ ] I can state Kafka's both-shapes sentence precisely.
- [ ] I know Kafka has no per-message retry and what that forces.
- [ ] I know exactly what Redis pub-sub delivers to, and why loss is silent.
- [ ] I can distinguish an event from a command and give the naming tell.
- [ ] I know what goes wrong when a command is broadcast.
- [ ] I can compute the fan-out storage and bill, with and without batching.
- [ ] I can name three cases where pub-sub is the wrong choice.
- [ ] I answered all three questions above out loud.
