---
day: 129
track: practice
title: "Practice — Connected components"
status: written
---

# Day 129 · Practice

**DSA topic:** Connected components
**System design topic:** Message queues: why async changes everything

---

## Code these, in this order

One rule for the whole set: **write the outer loop first, before the traversal.** Type
`for v in range(n): if v not in seen:` and only then fill in the flood. Doing it the other way round is how
the outer loop gets forgotten, and forgetting it is the single most common failure on this family of
problems.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Provinces | LeetCode 547 (Medium) | The outer loop, on a matrix input. |
| 2 | Number of Islands | LeetCode 200 (Medium) | The grid version, iteratively, marking on push. |
| 3 | Max Area of Island | LeetCode 695 (Medium) | Component *sizes*, not just a count. |
| 4 | Number of Connected Components in an Undirected Graph | LeetCode 323 (Medium) | Build from `range(n)` — the isolated vertex. |
| 5 | Accounts Merge | LeetCode 721 (Medium) | Components after a modelling step, with labels not counts. |

### On problem 4, break it on purpose

Solve it once building the adjacency structure from the edge list alone, and once from `range(n)`. Run both
on `n = 6` with edges `[(0,1), (2,3)]`. Record both answers. Say in one sentence what the first one lost.

### On problem 2, run all three failure modes

On a 1,000 × 1,000 grid of all land:

1. Recursive flood — record the error.
2. Recursive flood after `sys.setrecursionlimit(2_000_000)` — record what you get instead.
3. Iterative flood marking on **pop** — record the peak stack length and what happens.
4. Iterative flood marking on **push** — record the peak stack length.

Four results. Two of them are crashes and the difference between them is the point.

### On problem 3, keep labels not counts

Return the sizes of every island, sorted, not just the maximum. Then answer "are cells (3,4) and (7,1) on the
same island?" in one comparison. This is the version real problems want.

### Then the Union-Find comparison

Take problem 4 and re-solve it with edges arriving one at a time, printing the component count after each
edge. Do it twice: once by re-running your traversal after every edge, once with Union-Find. Time both at
`n = 20,000` and `m = 20,000`. Two numbers, and the ratio is the argument.

---

### The algorithm drill

1. Write `count_components` from memory, and point at the two lines that are the whole lesson.
2. Say what happens if `seen` is created inside the loop, and what number you get.
3. Write the labelling version and say what the one dictionary is doing.
4. Say how you get "same group?" and "largest group" from labels.
5. Write the grid version and point at where the outer loop is.

### The cost drill

1. Explain why the outer loop does not multiply the cost.
2. Derive `O(V + E)` including the cheap checks.
3. Give the cost for `V = 10^6`, `E = 3×10^6`, 40,000 components.
4. Give `V` and `E` for an `r × c` grid.
5. Say what marking by overwriting the grid saves, in bytes, on a 1,000 × 1,000 grid.

### The Union-Find drill

1. State the rule for choosing between traversal and Union-Find.
2. Give the cost of each for `m` edges arriving one at a time.
3. Compute both at `m = 100,000`, `V = 100,000`.
4. Say what Union-Find cannot do that a traversal can.

### The directed drill

1. Say why "components" is ambiguous on a directed graph.
2. Define weakly connected and how you would compute it.
3. Define strongly connected and say why it needs a different algorithm.
4. Say what you would ask the interviewer.

### The break-it drill

Trigger each and record the exact output or error:

1. Flooding from vertex 0 only, on a four-component graph.
2. `seen` reset inside the outer loop.
3. Adjacency built from edges only, with an isolated vertex.
4. Grid flood marking on pop, on a million-cell all-land grid.
5. Recursive grid flood on the same grid.
6. `count_components` called on a directed adjacency list.

---

### The what-goes-async drill

1. State the rule for what belongs in a queue, in one line.
2. Sort these: send welcome email, validate password, resize image, charge card, index for search, compute
   the search results.
3. For each one you moved async, say what the user sees instead.
4. Give one case where "charge the card" legitimately goes async, and what makes it legitimate.

### The numbers drill

1. Compute the synchronous and asynchronous latency for the five-step signup.
2. Compute availability for five services at 99.9% in series, and for the async version.
3. Compute machines needed for a 5× peak, synchronous and asynchronous.
4. Compute drain time for a 300,000-message backlog at 2,000/s capacity and 1,000/s arrivals.
5. Recompute it at 1,100/s capacity and say what that shows.
6. Size consumers with Little's Law for 1,000 msg/s at 200 ms each.
7. Compute the SQS bill for 100M messages a day, with and without batching.

### The four-losses drill

Name each, then give its mitigation:

1. You lose the answer.
2. You gain duplicates.
3. You lose ordering.
4. Failures become quiet.

Then say which of the four is the biggest practical cost, and why.

### The delivery drill

1. Define at-most-once, at-least-once and exactly-once in one line each.
2. Say which one every real queue actually does, and what that forces on you.
3. Explain the visibility timeout mechanism.
4. Give the timeline for a 45-second job under a 30-second timeout.
5. Give both fixes and say which you need anyway.

### The ordering drill

1. Say why ordering is per key and never global.
2. Give the two costs of partitioning by key.
3. Quote SQS FIFO's throughput cap and what it is per.
4. Give the design that avoids needing ordering at all.

### The backpressure drill

1. Say what metric you alert on, and why depth is the wrong one.
2. Name the four responses to a growing queue.
3. Say what you autoscale on and why not CPU.
4. Say why consumers at 95% utilisation are a problem, with the arithmetic.
5. Say what "put a queue in front of it" does not fix.

### The choose-one drill

1. Give the three shapes of message system and one example each.
2. State the work-versus-event distinction in one sentence.
3. Give three reasons to pick Kafka and three to pick a task queue.
4. Say when a database table with a status column is the right queue.

### The failure drill

For each, say what happens and what you would build:

1. A consumer crashes after doing the work and before acknowledging.
2. A job takes 45 seconds under a 30-second visibility timeout.
3. A malformed message that fails every time, in an ordered queue.
4. A dead-letter queue nobody has alerted on.
5. One very active user's key, in a partitioned topic.
6. Arrival rate 1,100/s against a consumer capacity of 1,000/s, for an hour.
7. A photo stuck in `PROCESSING` forever because its message went to the DLQ.

Two of the seven are design omissions rather than failures. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many connected components does this graph have?*
   The outer loop with `seen` shared outside it, why that is `O(V + E)` and not `V` traversals, building from
   `range(n)` for the isolated vertex, and the Union-Find rule offered before it is asked.

2. *Count the number of islands.*
   Cells as vertices and adjacency as edges, the double loop as the outer loop, iterative with marking on
   push, the two crash modes named, and the mutation of the caller's grid flagged.

3. *The signup email takes four seconds. Fix the latency.*
   What the user actually needs before the response, the latency and availability numbers, then the four
   losses named unprompted — with what the user sees, idempotency, ordering, and the DLQ.

---

## Before you move on

- [ ] I write the outer loop before the traversal.
- [ ] I know `seen` lives outside the loop and what number I get if it does not.
- [ ] I can explain why the outer loop does not multiply the cost.
- [ ] I can derive `O(V + E)` for the whole component count.
- [ ] I build from `range(n)` and know which vertex I would otherwise lose.
- [ ] I can write the labelling version and get sizes and "same group?" from it.
- [ ] I can write the grid version iteratively.
- [ ] I mark grid cells on push and know the stack size if I do not.
- [ ] I know what recursion does on a million-cell island, and what raising the limit does.
- [ ] I know marking by overwriting mutates the caller's input, and I say so.
- [ ] I can state the traversal-versus-Union-Find rule and back it with numbers.
- [ ] I know "components" is ambiguous on a directed graph, and I ask.
- [ ] I can state the rule for what belongs in a queue.
- [ ] I can compute the latency and availability wins with numbers.
- [ ] I can compute the machine-count win from buffering a peak.
- [ ] I can name all four things async costs me.
- [ ] I always say what the user sees while the work is pending.
- [ ] I know at-least-once is not optional and what it forces on every consumer.
- [ ] I can explain the visibility timeout and its classic bug.
- [ ] I know both fixes and which one I need regardless.
- [ ] I know ordering is per key and can quote FIFO's throughput cap.
- [ ] I can give the design that removes the need for ordering.
- [ ] I alert on message age, not queue depth.
- [ ] I autoscale on queue depth or age, not consumer CPU.
- [ ] I can compute drain time and explain the headroom argument.
- [ ] I know a queue does not create capacity.
- [ ] I can distinguish work from events and pick the right system.
- [ ] I know when a database table is a good enough queue.
- [ ] I answered all three questions above out loud.
