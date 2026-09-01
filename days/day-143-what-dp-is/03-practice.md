---
day: 143
track: practice
title: "Practice — What dynamic programming actually is"
status: written
---

# Day 143 · Practice

**DSA topic:** What dynamic programming actually is
**System design topic:** Bloom filters and probabilistic structures

---

## Code these, in this order

One rule for the whole set, and it is the habit this entire phase depends on: **write the recurrence in words
as a comment, then the base cases, then plain recursion, then add memory.** In that order, every time. Writing
a table before you have the recurrence is how DP becomes impossible, and it is the single most common way
people get stuck.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Fibonacci Number | LeetCode 509 (Easy) | The four versions: naive, memo, table, two variables. |
| 2 | Climbing Stairs | LeetCode 70 (Easy) | The same recurrence, different base cases. Get them right. |
| 3 | Min Cost Climbing Stairs | LeetCode 746 (Easy) | `min` instead of `+`, and where the answer lives. |
| 4 | Unique Paths | LeetCode 62 (Medium) | Two dimensions, and the base row and column. |
| 5 | Unique Paths II | LeetCode 63 (Medium) | Obstacles — the base cases stop being trivial. |
| 6 | House Robber | LeetCode 198 (Medium) | The first genuine choice at each step. |

### On problem 1, write all four and measure

Naive, memoised, tabulated, and two-variable. Then:

1. Count the calls the naive version makes for `n` = 10, 20, 30, 35.
2. Time `naive(32)` against `optimised(32)` and record the ratio.
3. Print the number of *distinct* subproblems next to the call count.

Two columns, and the gap between them is what memory removes.

### On problem 2, get the base cases wrong on purpose

Set `ways(2) = 1` instead of 2. Run it for `n = 12`. Record the answer and how far off it is. Then say why
there was no error.

### On problem 5, do the base row by hand

Write down the first row of the table for a grid with an obstacle in the middle of it. Then write the loop
that produces it. The naive `dp[0][j] = 1` is wrong the moment there is an obstacle, and that is the whole
problem.

### On problem 6, name the state before coding

Write `dp[i] = ` as a full English sentence before anything else. Then check it against a three-house example
by hand. If your sentence does not let you compute `dp[3]` from `dp[2]` and `dp[1]` alone, the state is wrong.

### Then the conversion drill

For each of problems 3, 4 and 6:

1. Write the top-down memoised version.
2. Convert it to bottom-up, working out the fill order explicitly.
3. Reduce the space, and say what you gave up by doing so.

Three versions each, and the third one should make you say out loud what the window is.

---

### The definition drill

1. Define DP in one sentence.
2. Name the two conditions and say what each means.
3. Say what distinguishes DP from divide-and-conquer, with an example of each.
4. Say what a "state" is, and give the test for whether yours is complete.
5. Give the cost formula for any DP.

### The order-of-work drill

1. Say the four steps, in order, from problem statement to memoised code.
2. Say what goes wrong if you start with the table.
3. Say why you would write top-down before bottom-up in an interview.
4. Give the two reasons to convert to bottom-up.

### The stairs drill

1. Derive the recurrence out loud, from "my last move was".
2. Give the base cases and say why `ways(2) = 2`.
3. Give the naive call count for `n` = 10, 20, 30, 35, and the growth factor per step.
4. Write all four versions from memory.
5. Say what window the space optimisation keeps, and why.

### The state drill

1. Say what `dp[i]` means for stairs, for unique paths, and for house robber.
2. Give the test for whether a state is complete.
3. Give an example where a one-dimensional state is not enough, and say what the second dimension is.
4. Say what happens — exactly — when the cache key omits part of the state.

### The costs drill

1. Give the naive and memoised costs for stairs, with the reason for each.
2. Apply the states-times-work formula to a 1D, a 2D, a 2D-with-inner-loop, and a bitmask DP.
3. Compare top-down and bottom-up on time and on space.
4. Give Python's recursion limit and the `n` at which top-down stops being viable.

### The break-it drill

Trigger each and record the exact output or error:

1. No base case at all.
2. A base case off by one.
3. `@lru_cache` on a function taking a list.
4. A manual cache keyed on only some of the arguments.
5. A mutable default argument as the cache, called twice from the top.
6. Memoised recursion at `n = 100,000`.
7. `@lru_cache` on a method with `self`, across two test cases.

Five of the seven give no error. Name them.

---

### The mechanism drill

1. Describe a Bloom filter's `add` and `check` in two sentences each.
2. State the guarantee precisely, in the right order.
3. Say why there can be no false negatives.
4. Say what a false positive actually is, in terms of bits.
5. Say why it cannot delete, and what breaks if you try.

### The sizing drill

1. Give both formulas.
2. Give bits per item and `k` for 1%, 0.1% and 0.01%.
3. Compute memory for a billion items at each, and against a real set.
4. Say how many extra bits per item each factor of ten in accuracy costs.
5. Say what happens when you insert five times the design capacity, and what the symptom is.

### The placement drill

1. State the placement rule in one sentence.
2. Draw the two paths and say what each costs.
3. Say why the filter must never decide anything on its own.
4. Give a case where a false positive is cheap and one where it is wrong output.
5. Cost the false-positive path for a local disk seek and for a cross-region query at 1% and a million
   lookups a second.

### The variants drill

1. Say what a counting Bloom filter buys and costs.
2. Say what a scalable Bloom filter is for.
3. Say what a cuckoo filter does better and what it does worse.
4. Say why `k` has an optimum, and what "half the bits set" has to do with it.

### The relatives drill

1. Say what HyperLogLog answers, its memory, and its error.
2. Give the intuition — leading zeros — in two sentences.
3. Say what `PFMERGE` buys that summing counts cannot.
4. Say what HyperLogLog cannot tell you.
5. Say what Count-Min Sketch answers, its error direction, and what it is good and bad at.

### The numbers drill

1. Compute the SSTable saving for ten files with and without filters.
2. Compare bit reads for a positive and a negative lookup, and say why negatives are cheaper.
3. Compute HyperLogLog against an exact set for a billion ids.
4. Compute Count-Min against a hash map for ten million terms.
5. Say what the Count-Min error is proportional to, and what that means for rare items.

### The failure drill

For each, say what happens and what you would build:

1. A Bloom filter sized for a million, holding five million.
2. A "maybe" treated as a "yes" in a username-availability check.
3. Two servers each keeping their own copy of the same filter.
4. A false positive whose exact check is an 80 ms cross-region query.
5. Someone asks which users were counted by a HyperLogLog.
6. A Count-Min Sketch queried for an item seen 50 times in a stream of 10 million.
7. A crawler that does not normalise URLs before hashing.

Two of the seven are correctness bugs rather than performance problems. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why is this exponential, and how do you fix it?*
   The recurrence first, the branching call tree, the gap between exponentially many calls and linearly many
   distinct answers, memory as the fix, and the two conditions that make it apply.

2. *What does `dp[i]` represent in your solution?*
   The full sentence, the test for completeness, what happens silently when the state is incomplete, and an
   example where one dimension is not enough.

3. *How do you check whether a URL has been crawled, using little memory?*
   The guarantee in the right order, the sizing arithmetic with the 100 GB against 1.2 GB, the placement rule,
   what a false positive costs *in this system specifically*, and what the filter cannot do.

---

## Before you move on

- [ ] I write the recurrence in words before any code.
- [ ] I write plain recursion before adding memory.
- [ ] I can define DP in one sentence and name both conditions.
- [ ] I know what distinguishes DP from divide-and-conquer.
- [ ] I can say what `dp[i]` means as a full sentence, every time.
- [ ] I know the test for whether a state is complete.
- [ ] I know what happens when the cache key omits part of the state.
- [ ] I can give the cost formula and apply it to four shapes.
- [ ] I can produce the naive call counts and the growth factor.
- [ ] I can write all four stairs versions from memory.
- [ ] I know the two reasons to convert to bottom-up.
- [ ] I know Python's recursion limit and when top-down stops being viable.
- [ ] I have seen all five silent DP failures myself.
- [ ] I can state the Bloom filter guarantee in the right order.
- [ ] I can explain why false negatives are impossible.
- [ ] I know both sizing formulas and the 1% numbers.
- [ ] I can compute a billion items at three error rates.
- [ ] I know roughly 5 extra bits buys a factor of ten in accuracy.
- [ ] I know what overfilling does and that it is silent.
- [ ] I can state the placement rule and draw both paths.
- [ ] I know the filter must never decide on its own.
- [ ] I can cost the false-positive path, not just quote the rate.
- [ ] I know the three things a Bloom filter cannot do.
- [ ] I know why `k` has an optimum.
- [ ] I can name counting, scalable and cuckoo variants and their trades.
- [ ] I can explain HyperLogLog's intuition, memory and error.
- [ ] I know why `PFMERGE` matters and what HLL cannot tell me.
- [ ] I know Count-Min's error direction and what it is bad at.
- [ ] I know the distributed-filter problem and its three answers.
- [ ] I answered all three questions above out loud.
