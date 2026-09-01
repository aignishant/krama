---
day: 128
track: practice
title: "Practice — Depth-first search on a graph"
status: written
---

# Day 128 · Practice

**DSA topic:** Depth-first search on a graph
**System design topic:** Distributed systems revision and interview questions

---

## Code these, in this order

One rule for the whole set: **read the constraints line before writing the first character, and if `n` can
exceed a few thousand, write the iterative version.** Not "write it recursively and convert later". The
conversion is where the bugs are, and the constraint tells you which one you need before you start.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Islands | LeetCode 200 (Medium) | DFS on a grid, plus the outer loop over every cell. |
| 2 | Course Schedule | LeetCode 207 (Medium) | Three colours, and the outer loop over every vertex. |
| 3 | Clone Graph | LeetCode 133 (Medium) | The `seen` map doing double duty as the old-to-new mapping. |
| 4 | All Paths From Source to Target | LeetCode 797 (Medium) | Marking on entry and **unmarking on exit** — the difference. |
| 5 | Pacific Atlantic Water Flow | LeetCode 417 (Medium) | Two DFS runs from the edges inward, not one from each cell. |

### On problem 1, write it three ways

Recursive, iterative with a stack, and BFS. Then run all three on a 1,000 × 1,000 grid of all land. Record
which ones survive and what the failures look like. One of them produces a `RecursionError`; try raising the
limit and record what you get instead.

### On problem 2, deliberately write the two-state version

Implement cycle detection with a single `seen` set and run it on the diamond `0→1→3`, `0→2→3`. Record the
answer. Then fix it with three colours and run it again. Write one sentence saying what "seen" failed to
distinguish.

### On problem 4, watch the unmark

Solve it, then delete the line that removes the vertex from the current path on the way out. Record how many
paths each version finds on a small graph with two routes to the same vertex. Say in one sentence why a
traversal must not unmark and a path enumeration must.

### Then the conversion drill

Take your recursive solution to problem 2 and convert it to iterative **with finish order**, using the
two-push marker technique. Verify both give the same answer on ten random graphs. This is the hardest twenty
lines in the phase and it is worth doing once, properly, now.

---

### The shape drill

1. Write recursive DFS from memory in thirty seconds.
2. Write iterative DFS and say which single character differs from BFS.
3. Write the finish-order iterative version with the marker flag.
4. Write the components version and point at the line that makes it different.
5. Say where the mark goes in each version, and why there.

### The BFS-or-DFS drill

1. State the one-line rule.
2. Say what DFS has that BFS does not, and name three problems that need it.
3. Say what BFS has that DFS does not, and name two problems that need it.
4. Give both memory profiles on a star graph and on a path graph.
5. Say which is faster, and why that is a trick question.

### The colours drill

1. Name the three colours and what each means.
2. Say which one is the cycle test and why.
3. Walk the diamond example out loud and say where a two-state check goes wrong.
4. Give the equivalent formulation with two sets, and the line people forget.
5. Say why undirected cycle detection needs a completely different check.

### The recursion-limit drill

1. Give Python's default limit and the usable depth.
2. Name three ordinary graph shapes that exceed it.
3. Say what `setrecursionlimit(200_000)` produces and why that is worse.
4. Give the depth of a DFS on a 1,000 × 1,000 open grid.
5. Say what in the constraints tells you to write the iterative version.

### The costs drill

1. Derive `O(V + E)` for DFS.
2. Say why it is identical to BFS.
3. Give the space cost of each and the graph shape that makes each one worst.
4. Give the extra cost of the finish-marker version.

### The break-it drill

Trigger each and record the exact output or error:

1. The mark placed after the loop instead of on entry, on a graph with a cycle.
2. Two-state cycle detection on a diamond.
3. Undirected cycle detection with no parent check, on a single edge.
4. Directed cycle detection starting only from vertex 0, on a graph whose cycle is elsewhere.
5. Recursive DFS on a 5,000-vertex chain.
6. `sys.setrecursionlimit(500_000)` followed by the same call.
7. Path enumeration with no unmark on the way out.

---

### The one-problem drill

1. State the single problem underneath the whole phase, in one sentence.
2. Say why it is different from failure in a single program.
3. Name the eight responses and the day each came from.
4. State the ninth — the stance, not a mechanism.
5. Give the recognition question for the phase, in one line.

### The consistency drill

1. Name the five levels of the spectrum and what each guarantees.
2. Give the cost of each.
3. Give a real system for each.
4. Say why choosing per operation beats choosing per system, with an example.
5. State what CAP actually forces and when.

### The quorum drill

1. State the two quorum inequalities and what each buys.
2. Give three `(N, W, R)` settings and what each is for.
3. Say what happens to writes when a majority is unreachable, and why that is deliberate.
4. Summarise Raft in five lines.

### The transactions drill

1. Give 2PC's guarantee and its failure mode.
2. Give a saga's guarantee and its two losses.
3. Say why compensation is not rollback, with a concrete example.
4. State the ordering rule for saga steps.
5. Describe the outbox pattern and what it makes atomic.

### The numbers drill

Quote each from memory, then check:

1. Memory read, SSD read, same-datacentre hop, cross-region hop, cross-planet hop.
2. Clock skew, local and remote.
3. Raft election timeout; Kubernetes liveness default; ALB default.
4. Retry attempts, budget percentage, breaker threshold and cooldown, amplification for three layers.
5. Redis, etcd, Postgres hot-row and Kafka per-partition throughput.

Then compute live:

6. Pool exhaustion for 200 workers and a 30-second dependency at 100 req/s.
7. Bulkhead size for 100 req/s at a 200 ms p99.
8. Throughput under a global lock with 50 ms of work.
9. The full ten-million-payments idempotency calculation, all six lines.

### The trade-offs drill

State each as the sentence you would say out loud:

1. Consistency against availability.
2. Synchronous against asynchronous.
3. Strong coordination against none.
4. Fast detection against correct detection.
5. Doing it twice against not at all.
6. The meta-trade-off about adding components.

### The interruption drill

For each, give a two-minute answer:

1. "Your write succeeded on two of three replicas. What do you tell the user?"
2. "The debit succeeded and the credit timed out. What now?"
3. "Two machines both think they hold the lock. How, and what breaks?"
4. "The downstream bank is down for two hours. What does the user see?"
5. "The consumer crashed after processing and before acknowledging."
6. "How do you know the money is right at the end of the day?"
7. "What would you build first?"

Record yourself on three of them. Listen for whether you gave a number.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Traverse this graph depth-first. What if it is disconnected?*
   Mark on entry, the outer loop with `seen` shared, iterative when `n` is large with the segfault reason, and
   `O(V + E)` identical to BFS with the difference stated as "what you know while running".

2. *Does this directed graph contain a cycle?*
   Three colours with grey as the current path, the diamond as the case two states get wrong, the outer loop
   over all vertices because a cycle can hide in an unreachable region, and topological sort as the free
   follow-up.

3. *Your write succeeded on two of three replicas. What do you tell the user?*
   `R + W > N` and what `W = 2, N = 3` actually promises, then the honest part: the third replica will
   converge, a read at `R = 2` will see it, and what you say to the user depends on whether this operation is
   the balance or the profile picture.

---

## Before you move on

- [ ] I can write recursive DFS in thirty seconds.
- [ ] I can write iterative DFS and name the one character that differs from BFS.
- [ ] I can write the finish-order version with the marker flag.
- [ ] I mark on entry and know what happens if I mark after the loop.
- [ ] I can state the BFS-or-DFS rule in one line.
- [ ] I know what DFS has that BFS does not, and three problems that need it.
- [ ] I can name the three colours and say which one is the cycle test.
- [ ] I can walk the diamond example and say what two states get wrong.
- [ ] I know why undirected cycle detection is a different algorithm.
- [ ] I always loop over every vertex on a directed graph.
- [ ] I know Python's usable recursion depth and three shapes that exceed it.
- [ ] I know what raising the limit produces, and why it is worse.
- [ ] I know DFS and BFS have identical complexity.
- [ ] I know which graph shape makes each one's memory worst.
- [ ] I know path enumeration must unmark and traversal must not.
- [ ] I can state the one problem underneath this whole phase.
- [ ] I can name the eight responses and the day each came from.
- [ ] I can state the ninth — the stance.
- [ ] I can give the consistency spectrum with costs and real systems.
- [ ] I can state both quorum inequalities and what each buys.
- [ ] I can summarise Raft in five lines.
- [ ] I can give 2PC and saga guarantees and their failure modes.
- [ ] I can quote the latency ladder from memory.
- [ ] I can quote the clock, detection, retry and throughput numbers.
- [ ] I can compute pool exhaustion, bulkhead size and lock throughput live.
- [ ] I can do the ten-million-payments calculation in six lines.
- [ ] I can state all six trade-offs as sentences.
- [ ] I have answered all seven interruptions out loud.
- [ ] I answered all three questions above out loud.
