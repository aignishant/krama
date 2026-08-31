---
day: 115
track: practice
title: "Practice — Python's heapq, and the min-heap-only problem"
status: written
---

# Day 115 · Practice

**DSA topic:** Python's heapq, and the min-heap-only problem
**System design topic:** Consistency models

---

## Code these, in this order

One rule for the whole set: **every tuple you push has three elements** — priority, counter, payload —
even when you think you do not need the counter. The bug it prevents only appears on a tie, which means it
passes your tests and fails in production.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Kth Largest Element in an Array | LeetCode 215 (Medium) | The max-heap workaround, and heap-versus-sort with numbers. |
| 2 | Top K Frequent Elements | LeetCode 347 (Medium) | Tuples, the tie-breaker, and `nlargest` with a `key`. |
| 3 | Task Scheduler | LeetCode 621 (Medium) | A max-heap of counts, and re-pushing after a cooldown. |
| 4 | Network Delay Time | LeetCode 743 (Medium) | Dijkstra with lazy deletion, written the Python way. |

### On problem 1, do it four ways

`sorted()[-k]`, `heapq.nlargest`, a size-k heap with `heapreplace`, and quickselect. Time all four at
k = 10 and k = 500,000 on a million elements. Record eight numbers.

### On problem 2, break it on purpose

Push `(count, item_dict)` with two items of equal count and record the exact `TypeError`. Then fix it with
a counter, and then rewrite the whole thing with `nlargest(..., key=...)` and say which you prefer.

### On problem 3, use the right shortcut

Write the inner loop with `heappop` followed by `heappush`, then with `heapreplace`. Say how many passes
over the heap each does.

### On problem 4, do not write an indexed heap

Write it with lazy deletion — push a better distance, and skip an entry whose node is already settled. Say
how many entries the heap can hold in terms of V and E.

---

### The min-only drill

1. Give both ways to get a max-heap.
2. Say exactly where negation stops working, with three examples.
3. Write the inverted-`__lt__` class from memory.
4. Say which methods `heapq` actually calls, and what that means for a custom class.
5. Name the private max functions and say why you would not use them.

### The tuple drill

1. Say how tuples compare, and where the comparison stops.
2. Construct the `TypeError` and quote it exactly.
3. Say why the bug is invisible in testing.
4. State the two requirements of a tie-breaker and give something that fails each.
5. Say what the counter gives you for free.

### The API drill

Write from memory what each of these does and its complexity:

`heapify` · `heappush` · `heappop` · `h[0]` · `heappushpop` · `heapreplace` · `nsmallest` · `nlargest` ·
`merge`

Then say which one has no function at all and how you do it instead.

### The list drill

1. Say what `heapq` operates on, and what that means.
2. Name four things you can do to that object that break it silently.
3. Write the one-line invariant check.
4. Run `append` on a heapified list and show that a later pop is wrong.

### The lazy-deletion drill

1. Say why a heap cannot update a priority.
2. Describe the textbook fix and say why nobody writes it in Python.
3. Write lazy deletion with a live-sequence dict.
4. State the memory cost in terms of pushes versus live items.
5. Say what the equivalent line looks like inside a Dijkstra loop.

### The top-k drill

1. Give three approaches and their complexities.
2. Say what to use when k = 1.
3. Say roughly where the crossover to sorting is.
4. Compute the comparison counts at n = 1,000,000 for k = 10 and k = 500,000.
5. Say what `key=` buys you beyond convenience.

### The break-it drill

Trigger each and record the exact output or error:

1. `heapq.heappush(h, x, reverse=True)`.
2. Two equal-priority tuples whose payloads are dicts.
3. `time.time()` as a tie-breaker, pushed twice in a tight loop.
4. `h.append(0)` on a heapified list, then `heappop`.
5. Building a 200,000-item heap by pushing, timed against `heapify`.
6. `-"banana"`.
7. `float('nan')` pushed into a heap of floats, then several pops.
8. `nlargest(500_000, million_items)` timed against `sorted()`.

---

### The ladder drill

1. Name all five rungs in order.
2. For each, say what it costs and what it prevents.
3. Say which rung is the strongest that is still available during a partition.
4. Say what going down the ladder buys.

### The definitions drill

1. Define linearizable precisely, including the real-time part.
2. Define eventual precisely, including three things it does **not** promise.
3. Define causal in one sentence, and give a related and an unrelated pair.
4. Say what sequential adds and what it lacks.

### The session-guarantees drill

1. Name all four.
2. For each, give the user's own words for the complaint.
3. For each, give the fix and its cost.
4. Say which one is mostly a sharding problem and why.

### The choose-a-model drill

For each, name the model and justify in one sentence:

seat booking · a chat thread · a like count · a user's own profile edit · leader election ·
a recommendation list · stock at checkout · an analytics dashboard · a search index

Then say the sentence about systems versus operations.

### The anomaly drill

For each user complaint, name the missing guarantee:

1. "I posted it and it's not there."
2. "It was there, and now it's gone."
3. "The reply is above the message."
4. "Two of us booked the same seat."
5. "I changed my name and then my photo, and the name reverted."
6. "The count says 41 and my friend sees 42."

Say which one of the six you would not fix, and why.

### The conflict drill

1. Name four conflict-resolution strategies.
2. For each, say what it costs.
3. Say what last-write-wins does under clock skew.
4. Explain CRDTs in two sentences and say what they cannot express.
5. Say why "we'll use eventual consistency" is not yet a design.

### The numbers drill

1. Give read latency for each rung.
2. Give DynamoDB's price ratio for strong versus eventual reads.
3. Give typical replication lag in four situations.
4. Explain why the read following a write is the worst possible sample.
5. Give the cost of the read-your-writes fix, as a share of reads.

### The scepticism drill

1. Name the practice for verifying a consistency claim.
2. Say what it does, mechanically.
3. Say what it has found.
4. Say what you would ask for before believing a vendor's claim.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Python only has a min-heap. How do you get the maximum?*
   Negation with its limits, inverted `__lt__` as the general answer, the private functions named and
   rejected, then the tie-breaker problem raised unprompted with its two requirements, and what you must
   never do to the list.

2. *What consistency does this feature need? Justify it.*
   The ladder rather than a binary, linearizable and eventual both defined precisely, causal named as the
   strongest AP model, the four session guarantees, per-operation choices with concrete features, and the
   conflict-resolution requirement.

3. *A user posts a comment and cannot see it. Which guarantee is missing?*
   Read-your-writes, why it happens essentially always rather than rarely, three fixes with their costs,
   and the monotonic-reads sibling.

---

## Before you move on

- [ ] I can give both max-heap workarounds and say where each applies.
- [ ] I know `heapq` only calls `<`, and what that means for a custom class.
- [ ] I push three-element tuples by habit.
- [ ] I can quote the `TypeError` and say why it is invisible in testing.
- [ ] I can state the tie-breaker's two requirements and something that fails each.
- [ ] I know the whole `heapq` API and which function does not exist.
- [ ] I know four ways to break a heap silently.
- [ ] I can write lazy deletion and say its memory cost.
- [ ] I can write Dijkstra the Python way without an indexed heap.
- [ ] I know where the top-k crossover to sorting is.
- [ ] I always use `heapify` when I already have the items.
- [ ] I can name all five rungs of the consistency ladder in order.
- [ ] I can define linearizable and eventual precisely, including what eventual omits.
- [ ] I can say why causal is the strongest model that is still AP.
- [ ] I can name the four session guarantees and the complaint each one answers.
- [ ] I choose a model per operation and can justify nine features.
- [ ] I can name four conflict-resolution strategies and their costs.
- [ ] I know what CRDTs cannot express, and why.
- [ ] I know what Jepsen is and what it has found.
- [ ] I answered all three questions above out loud.
