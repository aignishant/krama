---
day: 113
track: practice
title: "Practice — The heap: a tree stored in an array"
status: written
---

# Day 113 · Practice

**DSA topic:** The heap: a tree stored in an array
**System design topic:** Why distributed systems are hard

---

## Code these, in this order

One rule for the whole set: **write the index arithmetic on the screen before anything else**, and say
which convention you are using. Every structural bug in a heap is an off-by-one in those three formulas.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Kth Largest Element in a Stream | LeetCode 703 (Easy) | The `O(1)` peek, and why a heap of size k is the right shape. |
| 2 | Last Stone Weight | LeetCode 1046 (Easy) | Repeated extract-max, and Python's min-only gotcha. |
| 3 | Kth Largest Element in an Array | LeetCode 215 (Medium) | Heap against sort against quickselect, argued with numbers. |
| 4 | Top K Frequent Elements | LeetCode 347 (Medium) | A heap over tuples, and where the tie-breaker matters. |

### Before problem 1, build your own heap

Write `MinHeap` from scratch: `peek`, `push`, `pop`, `_sift_up`, `_sift_down`. Then check `is_valid()`
after a thousand random pushes and pops. Do not use `heapq` until this passes.

### On problem 2, hit the min-only wall on purpose

Try to solve it with `heapq` directly and notice that it gives you the smallest. Then fix it by negating,
and say what you would do instead if the values were objects rather than numbers.

### On problem 3, do it three ways and time them

Sort, heap of size k, and quickselect. Run all three at n = 1,000,000 and k = 10, then at k = 500,000.
Record six numbers and say which approach wins where.

### On problem 4, print the heap

After building it, print the underlying list and confirm it is **not** sorted. Say in one sentence why
that is correct.

---

### The definition drill

1. State both rules of a heap.
2. Say which one people forget and what it buys.
3. Say what the value rule does **not** guarantee, with an example.
4. Say why a heap cannot search, in one sentence.

### The arithmetic drill

1. Write the three 0-based formulas from memory.
2. Write the three 1-based formulas.
3. For a heap of 15 elements, give the children and parent of indices 0, 3, 6 and 7.
4. Say what happens if you mix the conventions, and whether anything raises.

### The completeness drill

1. Say what "complete" means precisely.
2. Compute the array slots needed for a complete tree of 1,000 nodes.
3. Do the same for a degenerate tree of 40 nodes.
4. Say why the shape rule is half the definition rather than a detail.

### The operations drill

1. Give the complexity of peek, push, pop, build, find and delete.
2. Say why push appends rather than inserting in the middle.
3. Say why pop moves the **last** element to the root.
4. Say what happens if you sift down against the larger child instead of the smaller.

### The not-sorted drill

1. Build a heap from `[5, 3, 8, 1, 9, 2, 7]` and print the array.
2. Say why it is not sorted and why that is correct.
3. Produce sorted order and state its cost.
4. Say what `heapq.nsmallest(3, ...)` does internally, roughly.

### The comparison drill

1. Fill in the table against sorted array, unsorted array and balanced BST.
2. Say what a heap wins outright, and what it loses badly.
3. Compute memory for a million integers as a heap and as a pointer BST.
4. Say when you would choose a sorted array instead.

### The heapq drill

1. Write the five `heapq` functions you would actually use.
2. Say what happens when you ask for a max-heap.
3. Say what happens if you `append` to a heapified list instead of using `heappush`.
4. Say why there is no heap object in Python, and what that means for correctness.

### The break-it drill

Trigger each and record the exact output or error:

1. `parent = i // 2` with 0-based indexing.
2. Sifting down against the left child unconditionally.
3. Popping by removing index 0 from the list directly.
4. Mutating an element of a heapified list, then popping.
5. `heapq.heappush` on a list you sorted yourself, then popping.
6. Searching a heap for a value, timed at n = 1,000,000.

---

### The three-assumptions drill

1. Name the three things that stop being true with two machines.
2. For each, give the single-machine version and the distributed version.
3. Say which one matters most and why.
4. Give the latency figures for local, same-datacentre, same-continent and cross-world calls.

### The third-outcome drill

1. List the four things a timeout may mean.
2. Say why they are indistinguishable.
3. State the consequence in one sentence, using the word "repeat".
4. Say what mechanism follows from that consequence.

### The delivery drill

1. Define at-most-once, at-least-once and exactly-once.
2. Say which is impossible and why, naming the result.
3. State what is achievable instead, precisely.
4. Say what a system advertising exactly-once is actually doing.
5. Compute the double-charge exposure at 1M requests/day and 0.1% ambiguous timeouts.

### The clock drill

1. Give typical clock drift and NTP accuracy figures.
2. Say what NTP does that makes time non-monotonic.
3. Construct the case where last-write-wins discards the newer write.
4. Name three logical-clock mechanisms and what each one buys.
5. Say what Spanner does instead, and what it costs.

### The fallacies drill

1. Name at least five of the eight fallacies.
2. For each, give a design decision it invalidates.
3. Pick a system you have designed in this course and say which fallacy it assumes.

### The defences drill

For each, say what it protects and what it costs:

timeouts · exponential backoff · jitter · idempotency keys · circuit breakers · bulkheads ·
propagated deadlines

Then compute the wasted work when a caller's timeout is shorter than the callee's retry budget.

### The impossibility drill

1. State the Two Generals problem in two sentences.
2. State FLP informally.
3. Say what real systems do instead of solving them.
4. Say what fencing, quorums and epochs are all defending against.

### The judgement drill

1. Name the four reasons that justify distributing.
2. Say what one machine is better at.
3. Say what you would tell an interviewer who proposes microservices for a small product.
4. Say what the hardest practical problem is, and what it requires to be designed in advance.

### The failure drill

For each, say what happens and what you would add:

1. A payment call times out and the client retries.
2. A thousand clients retry a recovering service simultaneously.
3. Two replicas record writes with timestamps 20 ms apart and clocks skewed by 60 ms.
4. A service's timeout is longer than its caller's.
5. A slow dependency does not time out at all.
6. An incident spans eight services with no correlation id.

Two of the six are not fixed by retrying. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is a heap? Where is the parent of index i?*
   Both rules with the shape rule flagged as the one people forget, the arithmetic with the convention
   named, what completeness buys, the narrow promise stated as `O(1)` peek and `O(n)` for everything else,
   and the memory comparison against a pointer tree.

2. *What changes when you go from one server to two?*
   The three broken assumptions, the third outcome as the whole subject, the consequence about repeating
   safely, exactly-once killed before it is offered, the clock consequence with last-write-wins, and why
   anyone accepts the cost.

3. *Your call times out. What do you do?*
   A timeout is not a failure, the four possibilities, is-it-idempotent as the deciding question, backoff
   with jitter, and idempotency keys as what makes at-least-once safe.

---

## Before you move on

- [ ] I wrote a heap from scratch and it passes `is_valid()` after a thousand operations.
- [ ] I can state both rules and say which one people forget.
- [ ] I can write the index arithmetic in both conventions.
- [ ] I can say what completeness buys, with the array-slot numbers.
- [ ] I know why push appends and why pop moves the last element up.
- [ ] I can say what a heap cannot do, in one sentence.
- [ ] I know the heap array is not sorted, and why that is correct.
- [ ] I can compare a heap against a BST on memory as well as complexity.
- [ ] I know `heapq` is min-only and what to do about it.
- [ ] I know what breaks if I mutate a heapified list directly.
- [ ] I can name the three things that stop being true with two machines.
- [ ] I can list the four meanings of a timeout.
- [ ] I can say why exactly-once delivery is impossible and what is achievable.
- [ ] I can construct the case where last-write-wins loses data.
- [ ] I can name five fallacies and a decision each one invalidates.
- [ ] I can name seven defences and what each protects.
- [ ] I can state Two Generals and FLP and what systems do instead.
- [ ] I can name the four reasons to distribute, and say when not to.
- [ ] I answered all three questions above out loud.
