---
day: 114
track: practice
title: "Practice — Push, pop, and heapify"
status: written
---

# Day 114 · Practice

**DSA topic:** Push, pop, and heapify
**System design topic:** The CAP theorem, honestly

---

## Code these, in this order

One rule for the whole set: **after every operation, assert the heap property.** One line —
`all(data[(i-1)//2] <= data[i] for i in range(1, len(data)))` — and it catches every structural bug in
this lesson, all of which are otherwise silent.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Build your own `MinHeap` | — | `sift_up`, `sift_down`, `push`, `pop`, and the invariant check. |
| 2 | Sort an Array | LeetCode 912 (Medium) | Heapsort in place, and why it loses to quicksort anyway. |
| 3 | Kth Largest Element in an Array | LeetCode 215 (Medium) | `heapify` + k pops against a full sort, argued with numbers. |
| 4 | Find K Pairs with Smallest Sums | LeetCode 373 (Medium) | `heapreplace` on a fixed-size heap, rather than push-then-pop. |

### On problem 1, instrument it

Count swaps. Build a heap of 100,000 random values two ways — bottom-up `heapify` and `n` pushes — and
record swaps per node for both, at n = 1,000, 10,000 and 100,000.

### On problem 2, then compare against `sorted()`

Time your heapsort against Python's built-in on a million integers. Record the ratio and say what explains
it, in one sentence about memory access.

### On problem 3, do it three ways

Full sort; `heapify` plus k pops; a fixed-size heap of k. Time all three at k = 10 and k = 500,000 on a
million elements. Say which wins where and why.

### On problem 4, use `heapreplace`

Write it once with `heappush` followed by `heappop`, and once with `heapreplace`. Say what the difference
is in passes over the heap.

---

### The two-primitives drill

1. Write `sift_up` and `sift_down` from memory.
2. Say how many comparisons per level each one does, and why they differ.
3. Say which one insert uses and which one extract uses, and why not the reverse.
4. Say where each one stops.

### The completeness drill

1. Say why insert appends rather than inserting anywhere else.
2. Say why extract moves the **last** element to the root.
3. Draw what happens if you delete index 0 directly.
4. Draw what happens if you promote the smaller child instead.

### The smaller-child drill

1. Write the sift-down comparison correctly.
2. Change it to swap with the left child unconditionally and run a hundred random operations.
3. Say what the invariant check reports, and whether anything raised.
4. Say what a user of the heap would observe.

### The `O(n)` drill

1. State the two ways to build a heap and their complexities.
2. Say where `heapify` starts and in which direction, and justify both.
3. Give the depth-by-depth work table for a 15-node heap.
4. Write the sum and say what `Σ k/2^k` converges to.
5. Explain the asymmetry — why sift-**up** top-down is genuinely `O(n log n)`.
6. Report your measured swaps per node for both methods at three sizes.

### The heapsort drill

1. Write heapsort in place.
2. Say why it builds a **max**-heap for an ascending sort.
3. State its three properties and say which common sort shares all three.
4. Say why nobody uses it, in one sentence about cache.
5. Name where it *is* used, and why.

### The shortcuts drill

1. Say what `heappushpop` and `heapreplace` each do.
2. Say which one a fixed-size top-k heap wants, and why.
3. Say what `heappushpop` does when the new value is already the smallest.
4. Count the passes over the heap for each against the naive pair.

### The mutation drill

1. Say what to do when a value in the heap decreases, and when it increases.
2. State the complexity, and the caveat.
3. Describe an indexed heap and what it costs.
4. Describe lazy deletion and say which language forces you into it.

### The break-it drill

Trigger each and record the output or error:

1. `heapify` running forwards instead of backwards.
2. `heapify` starting from the last element rather than the last parent — count the wasted calls.
3. Sifting down without the `left < n` bounds check.
4. `data.pop(0)` used to extract the minimum.
5. Popping the only element without the `if data:` guard.
6. Building a million-item heap by pushing, timed against `heapify`.
7. Mutating `h[3]` directly and then popping.

---

### The statement drill

1. State CAP correctly, in one sentence.
2. Say what it does **not** say.
3. Say why "pick two of three" is wrong.
4. Name the only genuine CA system.

### The vocabulary drill

1. Define CAP's C precisely, and say what it is not.
2. Define CAP's A precisely, and say what it is not.
3. Compute the ordinary uptime of a CP system with four ten-minute partitions a year affecting a third of
   clients.
4. Say why that number matters for how you talk about CP.

### The per-operation drill

1. Say the sentence about systems versus operations.
2. Mark each of these AP or CP with a reason: catalogue browsing, cart, stock check, payment,
   confirmation email, recommendations, session data, leader election.
3. Name the third option that is neither, and give three concrete forms of it.

### The systems drill

1. Name four CP systems and four AP systems.
2. For each of Cassandra, MongoDB, DynamoDB and Spanner, give its PACELC classification.
3. Say what Kubernetes does when etcd loses quorum, and whether that is a bug.
4. Say why DNS is the everyday AP system.

### The PACELC drill

1. State PACELC in one sentence.
2. Say which branch applies more often, and why that makes it more useful.
3. Give latency figures for a local read, a leader read, a same-region quorum and a cross-region quorum.
4. Say how DynamoDB prices the trade, and what that tells you.

### The reconciliation drill

1. Name four conflict-resolution strategies.
2. For each, say what it costs.
3. Say what last-write-wins does when clocks are skewed.
4. Compute the writes to reconcile after a two-hour partition at 1,000 writes/s per side.
5. Describe Amazon's shopping-cart choice and say why it is deliberate.

### The quorum drill

1. Fill in the nodes-to-tolerated-failures table for 3 through 7.
2. Say why even numbers buy nothing.
3. Say what a 4-node cluster does when split 2|2.
4. State the `R + W > N` condition and say what it guarantees.

### The failure drill

For each, say what happens and what you would choose:

1. A 20-second GC pause on one node.
2. An asymmetric partition where A can reach B but not the reverse.
3. A cross-region link fails during a sale.
4. A CP config store loses quorum.
5. Two sides of an AP system both accept a write to the same key.
6. A system claims exactly-once and strong consistency across regions with low latency.

The last one is a claim you should be suspicious of. Say why.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Insert into the heap. Now remove the minimum.*
   What both operations share, insert appending with the completeness reason, extract moving the last
   element with the hole argument, swap-with-the-smaller-child said explicitly, and both complexities.

2. *Explain CAP. Which one does your design give up?*
   The correct narrow statement, "pick two of three" corrected with P not being optional, both words
   defined against what they are not, the per-operation answer with a concrete table, degradation as the
   third option, and PACELC as the more useful frame.

3. *Why is building a heap `O(n)`?*
   Half the nodes are leaves, the depth-by-depth table, the series converging to 2, and the asymmetry that
   makes the top-down version genuinely `O(n log n)`.

---

## Before you move on

- [ ] I can write both sift operations from memory.
- [ ] I know how many comparisons each does per level, and why.
- [ ] I can say why insert appends and why extract moves the last element.
- [ ] I always swap with the smaller child, and know what happens if I do not.
- [ ] I know where `heapify` starts, which direction it runs, and why both.
- [ ] I can give the depth-by-depth work table and the series that converges to 2.
- [ ] I can explain the asymmetry between sift-up and sift-down builds.
- [ ] I measured swaps per node for both build methods.
- [ ] I can write heapsort and say why nobody uses it, and where it is used.
- [ ] I know what `heapreplace` saves and when to reach for it.
- [ ] I know what to do when a heap value changes, and why finding it is the hard part.
- [ ] I can state CAP in one sentence and say what it does not say.
- [ ] I can say why "pick two of three" is wrong.
- [ ] I can define CAP's C and A against what they are not.
- [ ] I can compute a CP system's ordinary uptime and explain why that matters.
- [ ] I can classify eight operations as AP or CP with reasons.
- [ ] I can name the third option and three concrete forms of it.
- [ ] I can state PACELC and say which branch applies more often.
- [ ] I can name four reconciliation strategies and what each costs.
- [ ] I answered all three questions above out loud.
