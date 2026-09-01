---
day: 126
track: practice
title: "Practice — Representing a graph: adjacency matrix versus adjacency list"
status: written
---

# Day 126 · Practice

**DSA topic:** Representing a graph: adjacency matrix versus adjacency list
**System design topic:** Circuit breakers and bulkheads

---

## Code these, in this order

One rule for the whole set: **write `V` and `E` at the top of the file before anything else, with the actual
numbers from the constraints.** Then write one line saying which representation you chose and why. If the
constraints say `n <= 200`, that line is allowed to say "matrix, because 40,000 cells is nothing".

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find Center of Star Graph | LeetCode 1791 (Easy) | Reading the edge list without building anything at all. |
| 2 | Number of Provinces | LeetCode 547 (Medium) | You are handed a matrix. Traverse it without converting. |
| 3 | Find if Path Exists in Graph | LeetCode 1971 (Medium) | Converting an edge list, at a size where a matrix would fail. |
| 4 | Course Schedule | LeetCode 207 (Medium) | Directed build, and the direction stated as a sentence first. |
| 5 | Network Delay Time | LeetCode 743 (Medium) | Weighted list of `(neighbour, weight)`, stored the way the heap wants it. |

### On problem 2, resist the conversion

The input is an `n × n` matrix and `n <= 200`. Solve it directly on the matrix. Then say out loud what your
traversal costs — it is `O(n²)`, and that is correct here, not a mistake. Then say at what `n` you would have
converted.

### On problem 3, compute the matrix size first

`n` goes up to 200,000. Before writing anything, compute `n²` and say the number out loud. Then write the
adjacency list. This is the habit that stops the memory-limit failure.

### Run the size comparison yourself

Take the complete program from the lesson and run it at three densities of your own choosing. Record the
crossover point — the `E` at which the matrix becomes smaller than the list in Python — for `V = 500` and for
`V = 2,000`. Two numbers. Then say why the theoretical crossover and the measured one differ.

### Then deliberately write the aliasing bug

```python
matrix = [[0] * 4] * 4
matrix[0][1] = 1
print(matrix)
print(matrix[0] is matrix[1])
```

Run it. Record the output. Then write it correctly and run it again. Do this once, properly, so that the hour
you would otherwise lose to it later is spent now instead.

---

### The three-operations drill

1. Give the cost of the edge test in both representations.
2. Give the cost of listing neighbours in both.
3. Give the space cost of both.
4. Say which of the three questions a traversal actually asks, and what follows from that.
5. Give the cost of a whole BFS in both, with the arithmetic.

### The choosing drill

1. State the default choice in one sentence, with the reason.
2. Name the three cases where a matrix is right.
3. Say what density means and roughly where the crossover is.
4. Say what you do when you need `O(1)` edge tests on a sparse graph.
5. Say when you would keep the edge list and not convert at all, with two algorithms.

### The building drill

Write each from memory:

1. `build_matrix`, undirected.
2. `build_list`, undirected.
3. Both, directed.
4. The weighted matrix, including what "no edge" is and why.
5. The weighted list, and say which order you store the pair in and why.

### The numbers drill

1. Compute matrix cells and list entries for `V = 1,000`, `E = 3,000`.
2. Compute both in bytes for `V = 10,000`, `E = 50,000`.
3. Compute the bit-packed matrix size for the same graph and say what it buys.
4. Compute BFS steps for both on that graph and give the ratio.
5. Compute where the theoretical crossover is for `V = 1,000`.
6. Say why the measured crossover in Python comes much earlier.

### The break-it drill

Trigger each and record the exact output or error:

1. `[[0] * n] * n` followed by one cell assignment.
2. A matrix at `V = 100,000`.
3. A weighted matrix using `0` for "no edge", with a genuine zero-weight edge.
4. A directed graph built with both assignments.
5. An adjacency list built from a `defaultdict` on a graph with an isolated vertex.
6. A traversal claiming `O(V + E)` that contains a nested `range(n)`.

---

### The exhaustion drill

1. Compute time-to-exhaust for 200 workers, 1,000 requests/s, 10% touching a 30-second dependency.
2. Say in one sentence why the healthy 90% of traffic fails too.
3. Recompute with a 20-permit bulkhead and give both remaining capacities.
4. Say what this failure looks like on a dashboard, and why the cause is hard to find.

### The state-machine drill

1. Name the three states and every transition between them.
2. Say what half-open is for, and what happens without it.
3. Say what closes a half-open breaker and what re-opens it.
4. Write the `call` method from memory.
5. Say why `time.monotonic()` and not `time.time()`.

### The thresholds drill

1. Say why the threshold is a rate and not a count, with the 10,000 QPS arithmetic.
2. Say why the window must be recent, and what breaks in both directions if it is not.
3. Say what the minimum call volume is for and what happens without it.
4. Say what `slowCallDurationThreshold` catches that a failure count does not.
5. Give the cost of a 30-second cooldown, stated as a user-visible number.

### The bulkhead drill

1. Define a bulkhead in one sentence and say where the name comes from.
2. Size one with Little's Law for 100 requests/s at a 200 ms p99.
3. Say why you do not size it for the failure case.
4. Compare thread-pool and semaphore isolation: what each costs and what each cannot do.
5. Say why `blocking=False` is the whole point.

### The fallback drill

1. List the five fallback options in order.
2. Give a real example of each.
3. State the rule about what you may and may not fall back on.
4. Give two fallbacks that are worse than an error, and say why.

### The ordering drill

1. Give the four things in the request path, in order.
2. Say why retries go inside the breaker, giving both consequences.
3. Say what goes wrong if retries are outside it.
4. Say which of the four you would add first to a service that has none.

### The failure drill

For each, say what happens and what you would build:

1. A dependency slows to 30 seconds and 10% of traffic uses it.
2. A breaker configured with an absolute threshold of 20 failures, on a 10,000 QPS service.
3. A breaker that has no half-open state.
4. A bulkhead that queues instead of rejecting.
5. A semaphore bulkhead with no timeout on the call.
6. A fallback that returns a default price.
7. Fifty instances, each with its own breaker, and traffic heavily skewed to five of them.

Two of the seven are configuration mistakes and five are design mistakes. Sort them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How will you store this graph? Why not the other way?*
   `V²` against `V + 2E` with a number, the three operations, the observation that traversals only ask one of
   them, and the three cases where a matrix is right.

2. *A million users, two hundred friends each. How much memory?*
   Both representations computed out loud, the edges-are-the-memory observation, and compressed sparse row as
   the next step with what it costs you.

3. *One downstream service is slow. How do you protect the rest?*
   The two-second exhaustion arithmetic first, then the bulkhead with Little's Law sizing, then the breaker
   with its three states, then the fallback decision — and the order in the request path.

---

## Before you move on

- [ ] I can state the space cost of both representations.
- [ ] I can give the cost of all three operations in both.
- [ ] I know which question a traversal actually asks.
- [ ] I can give BFS cost in both and explain where `V²` comes from.
- [ ] I compute `V²` in my head before writing a matrix.
- [ ] I can name the three cases where a matrix is right.
- [ ] I know to use sets when I need fast edge tests on a sparse graph.
- [ ] I know when to keep the edge list and not convert.
- [ ] I have written the `[[0] * n] * n` bug and seen its output.
- [ ] I know why "no edge" is `INF` and not `0` in a weighted matrix.
- [ ] I can do the byte arithmetic for a ten-thousand-vertex graph.
- [ ] I know what bit-packing buys and when to reach for it.
- [ ] I can explain why the measured crossover differs from the theoretical one.
- [ ] I can compute time-to-exhaust for a slow dependency.
- [ ] I can say why the healthy traffic fails too.
- [ ] I can draw all three breaker states and every transition.
- [ ] I know what half-open is for.
- [ ] I know why the threshold is a rate over a recent window.
- [ ] I know what a minimum call volume prevents.
- [ ] I know why slow calls must count as failures.
- [ ] I can size a bulkhead with Little's Law.
- [ ] I know why a bulkhead must reject and not queue.
- [ ] I can compare thread-pool and semaphore isolation.
- [ ] I can list the five fallbacks and the rule about what not to fall back on.
- [ ] I know the order: bulkhead, breaker, retries, call.
- [ ] I know why retries live inside the breaker.
- [ ] I answered all three questions above out loud.
