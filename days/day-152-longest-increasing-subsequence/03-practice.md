---
day: 152
track: practice
title: "Practice — Longest increasing subsequence"
status: written
---

# Day 152 · Practice

**DSA topic:** Longest increasing subsequence
**System design topic:** Design a notification system at scale

---

## Code these, in this order

One rule for the whole set: **write the state as a full sentence containing the words "ending exactly at"
before you write any code.** The natural state fails on every problem here, and the sentence is what stops you
writing it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Increasing Subsequence | LeetCode 300 (Medium) | The state redefinition, and `max(dp)` not `dp[-1]`. |
| 2 | Russian Doll Envelopes | LeetCode 354 (Hard) | Sorting to remove a dimension, and the tie-break minus sign. |
| 3 | Number of Longest Increasing Subsequences | LeetCode 673 (Medium) | Counting alongside, and the replace-versus-add branches. |
| 4 | Longest Increasing Path in a Matrix | LeetCode 329 (Hard) | The same idea on a graph — memoised DFS, not a table. |
| 5 | Maximum Length of Pair Chain | LeetCode 646 (Medium) | Where greedy beats LIS, and why. |
| 6 | Longest Arithmetic Subsequence | LeetCode 1027 (Medium) | LIS with a second dimension in the state. |

### On problem 1, write the wrong state first and see it fail

Implement `dp[i] = best in the first i elements` by comparing only with the immediately previous element. Run
it on `[2, 5, 3, 7]` and record the answer. Then run it on `[3, 4, 1, 2, 5]` and record that.

**One of those is right and one is wrong.** Say which, and say why the first test passing is the dangerous
part.

### On problem 1, return `dp[-1]` deliberately

Run the correct `O(n²)` version on `[1, 2, 3, 0]` and print the whole `dp` array. Record `dp[-1]` and
`max(dp)`. **Say in one sentence why they differ**, using the words from your state definition.

### On problem 1, prove `tails` is not the answer

Run the `O(n log n)` version on `[1, 6, 7, 2]` and print `tails` at the end. Check by hand whether those values
appear in that order in the input. **Then write the parent-pointer version** and confirm it returns something
that does.

### On problem 1, flip one character

Change `bisect_left` to `bisect_right`. Run both on `[1, 3, 3, 5]` and record both answers. Say which problem
each one solves, and where in a problem statement you would look to decide.

### On problem 2, get the tie-break wrong on purpose

Sort by `(width, height)` ascending and run LIS on the heights. Test on three envelopes all of width 1 with
heights 1, 2 and 3. Record the answer, and the correct answer. **Then add the minus sign and explain it in one
sentence.**

### On problem 3, break the counting branches

Swap the `>` and `==` branches — add on a strictly better length, replace on an equal one. Run on
`[1, 3, 5, 4, 7]` and record the answer against the correct one. **Say why the wrong number is plausible.**

### On problem 5, find where greedy wins

Solve it with LIS first, then with a greedy sort-by-end-time. Compare running times at `n = 1000`. **Say in one
sentence why greedy is valid here and not for problem 1.**

### Then the timing drill

Time the `O(n²)` and `O(n log n)` versions at `n = 1,000`, `n = 5,000` and `n = 20,000` on random input.
Record the ratio at each size and say roughly where the crossover in practice sits.

---

### The state drill

1. State the wrong state and say exactly where the recurrence gets stuck.
2. State the right state, with the words "ending exactly at".
3. Say what the state space cost of the fix was. (Nothing — say that, and why it matters.)
4. Say why the answer is `max(dp)`, and give the input where it differs.

### The tails drill

1. Say what `tails[k]` holds, in one sentence.
2. Give the argument for why smallest is best, using 7 and 9.
3. Say why `tails` is sorted and why that matters.
4. Trace it by hand on `[10, 9, 2, 5, 3, 7, 101, 18]`.
5. Say what `tails` is *not*, and give the input that proves it.

### The reconstruction drill

1. Say why you cannot read the answer off `tails`.
2. Describe the two extra arrays and what each holds.
3. Give the parent rule in one sentence.
4. Say what the walk-back starts from.
5. Say why the quadratic version is easier here, and when you would prefer it.

### The variants drill

1. `bisect_left` versus `bisect_right` — which problem each solves.
2. Longest decreasing, two ways.
3. Longest bitonic, and why the `-1`.
4. Russian dolls, including the tie-break.
5. Counting the longest ones, and the two branches.

### The complexity drill

1. Give both complexities, time and space.
2. Compute comparisons for `n = 1,000`, `10,000` and `100,000` in the quadratic version.
3. Say what the ratio is at `n = 100,000`.
4. Say what LeetCode 300's constraint is and why it is set there.

### The break-it drill

Trigger each and record the exact output or error:

1. Returning `dp[-1]`.
2. The incomplete state, on `[3, 4, 1, 2, 5]`.
3. `bisect_right` when you wanted strict.
4. Returning `tails` as the subsequence.
5. `max(dp)` on an empty input.
6. Envelopes sorted `(width, height)` ascending.
7. The quadratic version at `n = 100,000`.

Five of the seven give no error at all. Name them.

---

### The pipeline drill

1. Name the five stages and what each does.
2. Say why ingest is asynchronous and what it costs you.
3. Say why `202` rather than `200`.
4. Say why there is one queue per channel, and name the pattern.

### The gates drill

1. Name the four gates in order.
2. Say why that order and not another.
3. Write the quiet-hours condition and say why the range check is wrong.
4. Say why the timezone must be the user's.
5. Say which gate is the most valuable and when it usually gets built.

### The dedup drill

1. Say where duplicates come from, precisely.
2. Say where the idempotency key must come from, and the mistake if it does not.
3. Give the exact Redis command and say why `GET`-then-`SET` is wrong.
4. Say what gap remains, and which way you would fall on it.
5. Say what the provider can do for you, and name the header.
6. Do the sizing at 1 billion/day and say why a Bloom filter is wrong here.

### The retry drill

1. Classify seven provider responses into retry and no-retry.
2. Say what a `410` requires beyond not retrying.
3. Say what a `403` on email requires, and why deliverability makes it urgent.
4. Say what jitter prevents.
5. Say what the circuit breaker is for and what a slow provider does without one.
6. Say what a TTL prevents, and what its counter tells you.

### The fan-out drill

1. Give the two stages and say why they are separate messages.
2. Do the arithmetic for 10M followers, both ways.
3. Say what engagement filtering does to cost and to open rate.
4. Say what a holdout group is for.
5. Say what you would do if fairness of ordering mattered.

### The cost drill

1. Give the channel split by volume and by cost at 1 billion/day.
2. Say which channel dominates cost and by how much.
3. Say what one Twilio number can send per day.
4. Say why that is a procurement problem rather than a scaling one.
5. Compute what batching saves, in volume and in open rate terms.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the longest strictly increasing subsequence.*
   Why the natural state fails, the redefined state, the recurrence, `max(dp)` with the counter-example, and
   the complexity.

2. *Can you do better than `O(n²)`? What does that array hold?*
   `tails[k]`'s meaning, the smallest-is-best argument, why it is sorted, the four-line loop, and the fact
   that its contents are not the answer.

3. *Design a notification system.*
   The five stages, the four gates in order, dedup with an event-derived key, retry classification with the
   `410` action, and the SMS cost line.

---

## Before you move on

- [ ] I can state the wrong LIS state and say where it gets stuck.
- [ ] I can state the right one, with "ending exactly at".
- [ ] I know redefining cost nothing in state space.
- [ ] I return `max(dp)` and can give the input where `dp[-1]` differs.
- [ ] I can write the `O(n²)` version from the sentence.
- [ ] I can say what `tails[k]` holds, exactly.
- [ ] I can give the smallest-is-best argument with 7 and 9.
- [ ] I know why `tails` is sorted and why that licenses binary search.
- [ ] I can trace `tails` by hand on the standard input.
- [ ] I know `tails` is not a subsequence, and the input that proves it.
- [ ] I can reconstruct with parent pointers.
- [ ] I know `bisect_left` is strict and `bisect_right` is not.
- [ ] I can do Russian dolls including the tie-break minus sign.
- [ ] I can count the longest ones with the right two branches.
- [ ] I know both complexities and the ratio at `n = 100,000`.
- [ ] I know `max([])` raises and the `tails` version does not.
- [ ] I can name the five notification stages.
- [ ] I know why ingest is asynchronous and what it costs.
- [ ] I can name the four gates in order and justify the order.
- [ ] I can write the quiet-hours condition correctly.
- [ ] I know where the idempotency key must come from.
- [ ] I know `SET NX EX` and why `GET`-then-`SET` is a race.
- [ ] I know which way I fall on the check-then-send gap.
- [ ] I can classify provider responses into retry and no-retry.
- [ ] I know a `410` means delete the token.
- [ ] I know why email bounces threaten deliverability.
- [ ] I know what a TTL prevents and what its counter signals.
- [ ] I can do the fan-out arithmetic both ways.
- [ ] I know engagement filtering beats parallelism, and why.
- [ ] I know SMS is ~1% of volume and ~88% of cost.
- [ ] I answered all three questions above out loud.
