---
day: 116
track: practice
title: "Practice — Top K problems"
status: written
---

# Day 116 · Practice

**DSA topic:** Top K problems
**System design topic:** Eventual consistency in practice

---

## Code these, in this order

One rule for the whole set: **name all three approaches before writing any of them, then choose out loud
with `n` and `k`.** The question is explicitly about the trade-off, so producing one solution without the
comparison is answering half of it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Kth Largest Element in a Stream | LeetCode 703 (Easy) | The one case where the heap is forced, and why. |
| 2 | Top K Frequent Elements | LeetCode 347 (Medium) | Counting first, and the `O(n)` bucket answer. |
| 3 | K Closest Points to Origin | LeetCode 973 (Medium) | A computed key, and not taking the square root. |
| 4 | Kth Largest Element in an Array | LeetCode 215 (Medium) | Quickselect with a random pivot, written iteratively. |

### On problem 1, say why the heap is forced

Before coding, say in one sentence why sorting and quickselect are both unavailable here.

### On problem 2, write both versions

The `nlargest` version and the bucket version. Say which is `O(n)` and exactly what makes it possible.
Then say what the heap is actually sized over, and why that matters.

### On problem 3, count the square roots

Write it with `math.sqrt` and without. Time both at a million points and record the difference. Say in one
sentence why removing it is safe.

### On problem 4, break it deliberately

Write quickselect with a fixed last-element pivot, run it on `list(range(100_000))`, and record what
happens. Then add the random pivot and run it again.

---

### The three-approaches drill

1. Name all three and give time, space, ordering and streaming support for each.
2. Say which question each of `n`, `k` and "in memory or a stream" answers.
3. Say roughly where the crossover between heap and sort is.
4. Say what to use when k = 1.

### The min-heap drill

1. State the counter-intuitive rule and justify it in one sentence.
2. State the mirror rule for the k smallest.
3. Write the size-k heap loop from memory.
4. Say what `heap[0]` is doing in the comparison and why it is `O(1)`.
5. Say why `heapreplace` rather than pop-then-push.

### The rejection drill

1. Give the expected number of insertions for a size-k heap on random data.
2. Compute it for n = 1,000,000 and k = 10.
3. Say what that means for the real cost versus the stated bound.
4. Give the input that produces the worst case, and say why it is not exotic.

### The quickselect drill

1. Write it iteratively from memory, with a random pivot.
2. Write the sum that shows it is `O(n)`.
3. Say why quicksort is `O(n log n)` and this is not, in one sentence.
4. Give the worst-case input and say why it is common.
5. Name two fixes beyond a random pivot, and say which one real libraries use.
6. Say what it does to the caller's array.

### The variants drill

1. For top-k frequent, say what the heap is sized over.
2. Give the `O(n)` alternative and the property that makes it possible.
3. For k-closest, say what you would omit and why it is safe.
4. For a stream, say why the heap is the only option.
5. For many queries on unchanging data, say what you would do instead.

### The ordering drill

1. Say which approaches return results in order and which do not.
2. Say what it costs to fix.
3. Say why this matters for a test.

### The break-it drill

Trigger each and record the exact output, error or timing:

1. A max-heap of everything instead of a size-k min-heap, on a stream.
2. `heappop` + `heappush` instead of `heapreplace`, timed at n = 1,000,000.
3. Quickselect with a fixed pivot on sorted input.
4. Quickselect on the caller's array, then printing the original.
5. `nlargest(500_000, million_items)` timed against `sorted()`.
6. Top-k-frequent with the heap over all items rather than the counts.
7. `k = 0`, `k = n`, `k > n`, and an empty input, on all three approaches.

---

### The right-question drill

1. State the question you ask instead of "is eventual consistency acceptable?"
2. Give five data points and say how bad two seconds of staleness is for each.
3. State the display-versus-decision rule.
4. Apply it to a stock count on a product page and at checkout.

### The four-patterns drill

1. Name all four patterns.
2. For each, say what it costs on the server.
3. Say which one converts a server problem into a client one, and how.
4. Say what must be built first for that one, and why.
5. Give two things you would never apply it to.

### The pending-state drill

1. Describe the bank statement's three numbers and what each answers.
2. Give four software equivalents of a pending state.
3. State the principle about uncertainty in one sentence.
4. Say what showing it costs, and when it is worth it.

### The bounded-optimism drill

1. Describe the cheque example precisely, with both amounts.
2. State the general rule.
3. Name the real-world system that does this and the term for its threshold.
4. Give two software examples.

### The convergence drill

1. Name all three mechanisms.
2. For each, say what triggers it and how fast it is.
3. Say which keys each one converges, and which it never touches.
4. Explain Merkle trees in one sentence and give the exchange count for a million keys.
5. Answer "how long is eventually?" with a distribution rather than a number.

### The never-eventual drill

1. State the test you apply.
2. Give six things you would never make eventually consistent.
3. For each, say what the failure actually is — and note that it is not staleness.
4. Say what you would do instead for one of them.

### The compensation drill

1. Describe the airline arithmetic with numbers.
2. State the general rule for when to compensate.
3. Give two cases where compensation is not acceptable.
4. Name the hidden engineering cost of a compensating action.

### The counter drill

1. Write the naive counter and say what is wrong with it.
2. Name three correct approaches and their limits.
3. Say which one is a CRDT and why it converges without coordination.
4. Compute the throughput of each at 1,000,000 increments a second.

### The failure drill

For each, say what happens and what you would add:

1. A user likes a post and the count does not move.
2. A user's optimistic action fails and the UI silently keeps the old value.
3. A key is written once and never read, on a replica that missed the write.
4. Two users buy the last item at the same moment.
5. An idempotency store is itself eventually consistent.
6. A dashboard shows a number with no indication of when it was computed.

Two of the six are not fixed by better replication. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the k largest elements. Which approach, and why?*
   The three questions that decide it, all three approaches named with their properties, the min-heap rule
   with its justification, the rejection argument with numbers, quickselect with both caveats, and the
   streaming case where it is not a trade-off.

2. *The like count is wrong for two seconds. Is that acceptable?*
   The question split by who is looking, the display-versus-decision rule, optimistic UI as the cheapest
   fix with its failure path, the pending state as the honest fallback, what "eventually" actually is, and
   where you draw the line.

3. *Why a min-heap for the k largest?*
   The heap holds candidates, the only question you ask is about the worst of them, and the mirror rule.

---

## Before you move on

- [ ] I name all three approaches before writing any of them.
- [ ] I can state the min-heap rule and justify it in one sentence.
- [ ] I know the mirror rule for the k smallest.
- [ ] I can give the expected insertion count for a size-k heap.
- [ ] I know the worst-case input for the heap approach.
- [ ] I can write quickselect iteratively with a random pivot.
- [ ] I can write the sum that shows quickselect is `O(n)`.
- [ ] I know the worst-case input and why it is common.
- [ ] I remember that quickselect mutates the caller's array.
- [ ] I know where the crossover to sorting is.
- [ ] I know the `O(n)` bucket answer for top-k-frequent and why it works.
- [ ] I do not take the square root in k-closest-points.
- [ ] I always check `k = 0`, `k = n` and empty input.
- [ ] I ask what a user sees rather than whether eventual is acceptable.
- [ ] I can state the display-versus-decision rule.
- [ ] I can name all four patterns and their server cost.
- [ ] I would build the revert path before the optimistic update.
- [ ] I can name all three convergence mechanisms and what each one reaches.
- [ ] I can answer "how long is eventually?" with a distribution.
- [ ] I can state the test for what must never be eventual.
- [ ] I answered all three questions above out loud.
