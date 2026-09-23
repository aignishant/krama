---
day: 127
track: practice
title: "Practice — Breadth-first search on a graph"
status: written
---

# Day 127 · Practice

**DSA topic:** Breadth-first search on a graph
**System design topic:** Distributed locks

---

## Code these, in this order

One rule for the whole set: **write `seen.add(neighbour)` on the line above `queue.append(neighbour)`, always,
in that order.** Then say the sentence "each vertex enters the queue at most once" out loud. If your code does
not make that sentence true, it is wrong, whatever answer it produces.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find if Path Exists in Graph | LeetCode 1971 (Medium) | Plain reachability. Ten lines, and `deque` not a list. |
| 2 | Shortest Path in Binary Matrix | LeetCode 1091 (Medium) | BFS on an implicit grid, with eight directions instead of four. |
| 3 | Word Ladder | LeetCode 127 (Hard) | The neighbour function, and why building edges is the trap. |
| 4 | Rotting Oranges | LeetCode 994 (Medium) | Level-by-level, and the check for what never gets reached. |
| 5 | Open the Lock | LeetCode 752 (Medium) | An implicit graph of states, plus a set of forbidden vertices. |

### On problem 1, write both versions and time them

Solve it once with `deque.popleft()` and once with `list.pop(0)`. Run both on 100,000 vertices. Record the two
times. This is the cheapest possible way to make `deque` automatic.

### On problem 3, count the two models

Version A: compare every word against every other to build edges. Version B: generate the `L × 25` candidate
strings and check a set. On the LeetCode input, count the operations each version performs before the search
starts. Two numbers.

Then implement bidirectional BFS and record the number of words each version explores.

### On problem 4, notice what "impossible" means

The problem asks for `-1` when some orange can never rot. Say out loud which BFS concept that is, and where in
your code the check goes. It is not inside the loop.

### Then the marking experiment

Take your problem 1 solution and move `seen.add()` from the push to the pop. Run it on a dense graph —
2,000 vertices, 500,000 edges. Record:

1. Whether the answer is still correct.
2. The maximum queue length in each version.
3. The runtime of each version.

Three pairs of numbers. This is the single most useful measurement in the whole graph phase.

---

### The shape drill

1. Write plain BFS from memory in under two minutes.
2. Write the distances version, using one dictionary and not two.
3. Write the path version and the parent walk.
4. Write the level-by-level version with two lists and no queue.
5. Write the components version, and point at the line that makes it different.

### The guarantee drill

1. State the shortest-path guarantee in one sentence.
2. Give the one-sentence reason it holds.
3. Give the full induction argument out loud.
4. State the assumption it depends on, and give a graph where it fails.
5. Say what you use instead when that assumption fails, and what you use when the weights are only 0 and 1.

### The push-versus-pop drill

1. Say what changes if you mark on pop.
2. Say what stays correct and what breaks.
3. Give the queue size in each version, in terms of `V` and `E`.
4. Say which sentence stops being true.

### The costs drill

1. Derive `O(V + E)` from the loops, out loud.
2. Say why it is a sum and not a product.
3. Give the maximum queue size for a star graph and for a path graph, both with a million vertices.
4. Give BFS's cost on an adjacency matrix and say where the `V²` comes from.
5. Give `V` and `E` for a 1,000 × 1,000 grid.

### The break-it drill

Trigger each and record the exact output or error:

1. `list.pop(0)` on 200,000 vertices.
2. No `seen` set, on a three-vertex cycle.
3. `seen.add()` moved to the pop, on a graph with 500,000 edges.
4. `distances[goal]` on an unreachable goal.
5. A single BFS used to count all vertices on a disconnected graph.
6. BFS on a weighted graph where a one-edge path costs 10 and a two-edge path costs 2.

---

### The build-it-up drill

State each version and the failure that forces the next one:

1. `GET` then `SET`.
2. `SET NX` with no expiry.
3. `SET NX` then `EXPIRE`.
4. `SET NX PX` with a constant value.
5. `SET NX PX` with a unique token, released by `GET` then `DEL`.
6. The correct version.

Six steps. Say the failure at each one before giving the fix.

### The paused-holder drill

1. Give the timeline with times on it.
2. Say why client A is not at fault.
3. Say why no timeout setting avoids both failure directions.
4. Say why a check inside client A does not help.
5. Say where the enforcement has to live, and why there.

### The fencing drill

1. Explain a fencing token in three sentences.
2. Write the SQL `WHERE` clause that enforces it.
3. Say what zero rows updated means.
4. Say what you do when the resource cannot check tokens — three options.
5. Say what ZooKeeper gives you for free here.

### The watchdog drill

1. Say why a longer lease is the wrong fix for a long job.
2. Give the refresh interval as a fraction of the lease, and why that fraction.
3. Say what the extension must be conditional on.
4. Say what the worker must do when the extension fails.
5. Say what the watchdog cannot protect against.

### The choose-your-store drill

1. Define an efficiency lock and a correctness lock, with an example each.
2. Give Redis's throughput and its failure mode.
3. Give ZooKeeper's throughput and the three properties ephemeral sequential nodes buy.
4. Say why watching the node below you beats polling, with the arithmetic.
5. Say what Redlock fixes and what it does not.

### The numbers drill

1. Compute maximum throughput under a lock with 50 ms of work.
2. Say why adding machines does not help, and what does.
3. Compute wasted Redis calls for 50 waiters polling every 100 ms.
4. Compute how many jobs a day exceed a 30-second lease at a p999 of 45 s and 100,000 jobs.
5. Estimate the frequency of a GC pause longer than the lease across 50 instances.

### The do-not-lock drill

1. Name four alternatives to a distributed lock.
2. For the daily cron job, give the full non-lock design including takeover.
3. Say what the unique-constraint version gives you that the lock does not.
4. Say what it does not give you, and how you add it back.

### The failure drill

For each, say what happens and what you would build:

1. A holder crashes with no lease set.
2. A holder's lease expires during a 25-second GC pause.
3. A client releases with `GET` then `DEL` after its lease expired.
4. A job takes 45 seconds under a 30-second lease with no watchdog.
5. A watchdog whose extension fails, and a worker that does not check.
6. Redis becomes unavailable while ten workers hold locks.
7. One global lock protecting ten thousand independent jobs.

Two of the seven are throughput problems and five are correctness problems. Sort them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Traverse this graph breadth-first, and find the shortest path.*
   Queue plus seen set, mark on push with the reason, one dictionary doing three jobs, the parent walk, the
   `O(V + E)` derivation, and the unweighted assumption named before anyone asks.

2. *Find the shortest word transformation sequence.*
   Vertices and edges as a sentence, the implicit-graph move with the `L × 25` arithmetic, why building edges
   is `n²`, the two edge cases, and bidirectional BFS as the improvement.

3. *Implement a distributed lock. What if the holder crashes?*
   The six versions in order, each fixing the last, then the paused holder as the failure with no fix, then
   fencing at the resource — and "would a unique constraint do instead?" offered first.

---

## Before you move on

- [ ] I can write BFS from memory in under two minutes.
- [ ] I mark on push and can say why in one sentence.
- [ ] I know what marking on pop does to the queue size.
- [ ] I use `deque` and know what `list.pop(0)` costs.
- [ ] I can state the shortest-path guarantee and give the reason.
- [ ] I can give the induction argument out loud.
- [ ] I know the assumption it depends on and what to use when it fails.
- [ ] I know what to use when weights are only 0 and 1.
- [ ] I can derive `O(V + E)` from the loops.
- [ ] I know the queue's peak is the widest level, not `V`.
- [ ] I can write the distances version with one dictionary.
- [ ] I can reconstruct a path from parent pointers.
- [ ] I write the outer loop whenever the question says "all".
- [ ] I know why an unreachable lookup raises `KeyError`.
- [ ] I recognise an implicit graph and compute neighbours instead of storing them.
- [ ] I can explain bidirectional BFS and what it buys.
- [ ] I can give the six lock versions and the failure at each.
- [ ] I know why the expiry must be in the same command as the set.
- [ ] I know why the lock value is a unique token.
- [ ] I know why release must be a script.
- [ ] I can give the paused-holder timeline with times.
- [ ] I know why no timeout setting fixes it.
- [ ] I can explain fencing and write the `WHERE` clause.
- [ ] I know what to do when the resource cannot check tokens.
- [ ] I can size a lease and a watchdog refresh.
- [ ] I know what the worker does when the extension fails.
- [ ] I can distinguish efficiency and correctness locks and pick a store for each.
- [ ] I can compute throughput under a lock and say what actually fixes it.
- [ ] I look for a unique constraint before reaching for a lock.
- [ ] I answered all three questions above out loud.
