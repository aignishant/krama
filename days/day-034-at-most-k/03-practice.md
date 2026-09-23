---
day: 34
track: practice
title: "Practice — At-most-K, and the exactly-K trick"
status: written
---

# Day 034 · Practice

**DSA topic:** At-most-K, and the exactly-K trick
**System design topic:** Isolation levels and the anomalies they allow

---

## Code these, in this order

Four problems. **Before writing a line of each, say two sentences out loud:** is this a counting
question or a longest question, and is it at-most as asked or exactly-needing-the-subtraction? Those
two sentences are today's entire skill.

Before each one, ask:

1. "How many" or "longest"? Therefore `total +=` or `max`?
2. At-most directly, or exactly via `at_most(k) - at_most(k - 1)`?
3. What is the guard — negative `k`, `goal = 0`, `k <= 1`?
4. Does the condition use `len(count)`? Then the `del` at zero, as always.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Subarray Product Less Than K | LeetCode 713 (Medium) | The counting line `total += right - left + 1`, no subtraction needed — and the `k <= 1` guard. |
| 2 | Binary Subarrays With Sum | LeetCode 930 (Medium) | The subtraction, the collapsed map, and whether `goal = 0` crashes you. |
| 3 | Count Number of Nice Subarrays | LeetCode 1248 (Medium) | Seeing "exactly k odd numbers" as the same problem after one observation. |
| 4 | Subarrays with K Different Integers | LeetCode 992 (Hard) | The full trick with a real map — a hard problem that is two tested calls and a minus sign. |

### On problem 1, earn the counting line

Before coding, answer: after the shrink, why is every subarray ending at `right` and starting at or
after `left` valid? Say the one-sentence reason — shortening from the front can only remove things.

Then write it, and test `[10, 5, 2, 6]` with `k = 100` — expect 8. List the eight subarrays out loud
from the walk, not from the code.

### On problem 1, remove the guard on purpose

Delete the `k <= 1` guard and run `[2, 3]` with `k = 1`, then `[1, 1, 1]` with `k = 1`. The first
returns −1 — a count of minus one subarrays, silently. The second raises
`IndexError: list index out of range`. Say why the shrink loop cannot ever be satisfied, and why one
input crashes while the other lies.

### On problem 2, chase the zero

Write it with the subtraction and the `goal < 0` guard. Confirm `([1,0,1,0,1], 2)` gives 4 and
`([0,0,0,0,0], 0)` gives 15.

Then explain: when `goal = 0`, what does `at_most(-1)` get asked, and what does your guard return?
Now count the fifteen subarrays of `[0,0,0,0,0]` by hand — 5 + 4 + 3 + 2 + 1 — and say why that is
the sum of window lengths.

### On problem 3, find the collapse

Say before coding: what would the map hold, and why does it collapse to one integer? Then write it
with just an `odds` counter. Confirm `([1,1,2,1,1], 3)` gives 2 and `([2,4,6], 1)` gives 0.

### On problem 4, respect the hard label

Write `at_most` as its own function and test it alone first: `[1,2,1,2,3]` with `k = 2` must give 12,
with `k = 1` must give 5. Only then write the two-line `exactly` and confirm 7.

Then answer the question that makes this a hard problem: why can a single shrink-while-invalid window
not count exactly-k directly? Two directions of wrongness, one repair tool — say it in your own words.

### The counting-versus-longest drill

For each phrasing, say `total +=` or `max`, in under five seconds:

1. Longest subarray with at most k distinct values.
2. Number of subarrays with at most k distinct values.
3. Count the subarrays whose product is under k.
4. Shortest subarray with sum at least k.
5. How many subarrays contain exactly k odd numbers?
6. Longest run of 1s after flipping at most k zeros.

### The anomaly-matching drill

For each scene, name the anomaly and the weakest standard level that stops it:

1. A report reads a balance that a transaction later rolls back.
2. A transaction reads a price twice and gets 100, then 120.
3. A count of matching rows grows between two identical searches in one transaction.
4. Two processes read stock = 1, both decide to sell, both write stock = 0.
5. Two doctors both go off call after each checking that two were on call.

Numbers 4 and 5 are the write-side ones — say why no read level in the table fixes number 5, and
which two tools do.

### The level-choosing drill

For each transaction, pick a level (or a lock) and name the anomaly you are accepting:

1. Transfer money between two accounts, arithmetic in SQL.
2. A monthly report that reads forty tables over twenty minutes.
3. Book a seat if it is still free.
4. Increment a view counter ten thousand times a second.
5. Claim a username if nobody has it.

Number 5 has a better answer than any isolation level — name the constraint.

### The error-text drill

Two real Postgres errors. For each: which level produces it, what happened, and what must the
application do?

```
ERROR:  could not serialize access due to concurrent update
```

```
ERROR:  could not serialize access due to read/write dependencies among transactions
HINT:  The transaction might succeed if retried.
```

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Count the subarrays with exactly k distinct integers.*
   Counting, so the sum-of-window-lengths line, and why it is exact. Then the subtraction, why the
   nesting makes it legal, the negative-k guard, and the two-passes-still-O(n) cost.

2. *What isolation level would you use, and what anomaly are you accepting?*
   Refuse the global question — choose per transaction. Default plus SQL arithmetic, repeatable read
   for reports, serialisable in a retry loop for check-then-act. Name what each choice accepts.

3. *Two transactions each checked the rule and the rule still broke. What happened?*
   Write skew, told as the on-call doctors. Why repeatable read misses it — different rows written,
   no conflict — and the two fixes: `FOR UPDATE` on what you checked, or serialisable with retries.

---

## Before you move on

- [ ] I say "counting or longest" before every window problem, and place `total +=` or `max`
      accordingly.
- [ ] I can prove the counting line: after the shrink, `right - left + 1` subarrays end here, no more
      and no fewer.
- [ ] I guard the inner call — negative k, `goal - 1`, `k <= 1` — and I know the crash and the silent
      −1 that appear without it.
- [ ] I can recite the three read anomalies with a two-transaction story each.
- [ ] I can say the levels table from memory, plus the two Postgres deviations from it.
- [ ] I can tell write skew as a story and name both fixes.
- [ ] I answered all three questions above out loud.
