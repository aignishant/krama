---
day: 38
track: practice
title: "Practice — Subarray sum equals K: prefix plus hash map"
status: written
---

# Day 038 · Practice

**DSA topic:** Subarray sum equals K: prefix plus hash map
**System design topic:** Document databases

---

## Code these, in this order

Four problems, one machine: carry a running quantity, ask a map about the past. **Before each, say
two things out loud:** what the running quantity is (sum, recast sum, remainder), and what the map
stores (count, or first index).

Before each one, ask:

1. Can values be negative — and did the problem just retire the window for me?
2. "How many" (count map) or "longest" (first-index map, never overwritten)?
3. What is the sentinel — `{0: 1}` or `{0: -1}` — and what does it mean?
4. Ask first, record after — which input checks that order?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Subarray Sum Equals K | LeetCode 560 (Medium) | The machine itself: `seen[0] = 1`, ask-then-record, and why the window is illegal. |
| 2 | Subarray Sums Divisible by K | LeetCode 974 (Medium) | The remainder costume — same remainder at both ends — and Python's friendly `%`. |
| 3 | Contiguous Array | LeetCode 525 (Medium) | The longest variant: recast 0 → −1, first-index map, sentinel `{0: -1}`, never overwrite. |
| 4 | Maximum Size Subarray Sum Equals k | LeetCode 325 (Medium) | Problem 1's quantity with problem 3's map — proof you know which contract is which. |

### On problem 1, remove the sentinel on purpose

Delete `seen[0] = 1` and run `[1, 2, 3]` with `k = 3`. You get 1 instead of 2. Name the subarray
that went missing and say why every left-edge subarray needs the opening balance.

Then swap the two loop lines and run `[-1, -1, 1]` with `k = 0` — you get 4 instead of 1. Say what
got counted.

### On problem 2, check the language edge

Print `(-7) % 5` and say why Python needs no fix-up. Then say the one sentence you would add in a
Java or C++ interview about `(r % k + k) % k`.

### On problem 3, overwrite on purpose

Store `first[running] = i` unconditionally and run `[0, 0, 1, 0, 0, 0, 1, 1]`. You get 4 instead
of 6. Say which direction the stored index drifted and why "longest" wants the earliest occurrence
frozen.

### On problem 4, say the hybrid before coding

One sentence: "running sum like 560, first-index map like 525, sentinel `{0: -1}`." If you can say
it, the code is four edits from problem 3.

### The contract drill

For each phrasing, say the quantity, the map contract, and the sentinel — five seconds each:

1. Count subarrays summing to k.
2. Longest subarray summing to k.
3. Count subarrays with sum divisible by k.
4. Longest subarray with equal 0s and 1s.
5. Does any subarray sum to k?

### The routing echo

Say which day's tool serves each, and why, in one sentence:

1. Longest subarray with sum ≤ k, all positive.
2. Longest subarray with sum = k, negatives allowed.
3. Count subarrays with at most k odd numbers.
4. Count subarrays with sum = k, negatives allowed.

### The embed-or-reference drill

For each relationship in a marketplace, say embed or reference, and the deciding question:

1. An order's line items.
2. The seller's display name shown on a product card.
3. A product's reviews.
4. The buyer's default address, as it was when the order shipped.
5. A device's event log, 100 events a day.

Number 4 is the snapshot — say why this copy is *meant* to stay old.

### The ceiling drill

From memory, in under two minutes:

- Comments at 2 KB embedded: the size at 100, at 1,000, and where the hard error lands.
- An events array at 1 KB × 100/day — months until 16 MB.
- A rename fanning out to 102,000 embedded copies at 5,000 writes/s — the background job's
  duration, and the two failure modes to name (mixed names mid-job; a write racing the job).

### The breakage drill

Answer each in one or two sentences, out loud:

1. Why does "top commenters this month" hurt in a document model?
2. What stops a comment pointing at a deleted post — and in Postgres, what would have?
3. When do MongoDB's multi-document transactions signal the domain wanted tables?
4. Why does "just use JSONB" answer many MongoDB proposals?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Count the subarrays whose sum equals k.*
   Ask about negatives first. The flip — earlier prefix equals running minus k — then the sentinel,
   the ask-then-record order with the k = 0 input, and O(n)/O(n) with the space named as the price
   of negatives.

2. *Model a blog in MongoDB. What happens when a user changes their name?*
   Three collections, embed-versus-reference with reasons, then the rename: truth in users, fan-out
   job for the display-name copies, the staleness window said out loud, and when the name was never
   embeddable at all.

3. *Why does the sliding window fail on this problem, when it worked all last week?*
   Monotonicity, both directions broken by negatives, the discarded start it cannot justify — and
   the honest counterpart: when the window is still the better tool, and what today's O(n) space
   buys instead.

---

## Before you move on

- [ ] I can write the 560 machine from memory: sentinel, ask, record — in that order.
- [ ] I know which map contract serves "how many" and which serves "longest", and the two
      sentinels.
- [ ] I can name the input that punishes each of the three classic bugs — missing sentinel, swapped
      order, overwritten first index.
- [ ] I ask "can values be negative?" before choosing between window and map.
- [ ] I can model the blog with reasons per relationship, and answer the rename without pausing.
- [ ] I can run the 16 MB and fan-out arithmetic for any array or copy in a model.
- [ ] I answered all three questions above out loud.
