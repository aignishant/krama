---
day: 147
track: practice
title: "Practice — Finding the state: the hardest part of DP"
status: written
---

# Day 147 · Practice

**DSA topic:** Finding the state: the hardest part of DP
**System design topic:** Design a pastebin

---

## Code these, in this order

One rule for the whole set: **before writing anything, apply the test out loud.** "Given only the state, can I
decide what happens next without knowing anything else about how I got here?" Then write the state as a full
sentence, then count the state space, then code. Three steps, about ninety seconds, and they save the twenty
minutes that a wrong state costs.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | 0/1 Knapsack | classic — write it yourself | A resource dimension, and why one index fails. |
| 2 | Best Time to Buy and Sell Stock IV | LeetCode 188 (Hard) | A mode *and* a count, and where the count is consumed. |
| 3 | Best Time to Buy and Sell with Cooldown | LeetCode 309 (Medium) | A mode with three values instead of two. |
| 4 | Edit Distance | LeetCode 72 (Medium) | Two positions, and prefix-length versus index conventions. |
| 5 | Cheapest Flights Within K Stops | LeetCode 787 (Medium) | A count dimension on a graph. |
| 6 | Partition Equal Subset Sum | LeetCode 416 (Medium) | A resource dimension, and the pseudo-polynomial point. |

### On problem 1, write the broken version first

Implement it with `dp[i]` only and run it on three items totalling more than the capacity. Record what it
returns and compare with the sum of all values. Then apply the test and say, in one sentence, what was missing.

### On problem 2, break the transaction counting

Decrement `transactions_left` on both the buy and the sell. Run with `k = 2` on `[7,1,5,3,6,4]` and record the
answer. Then fix it and record the correct one. Write one sentence on why the wrong answer is plausible.

Then add the observation that `k > n/2` is the same as unlimited, and cap it. Run with `k = 1,000,000` and
confirm it is instant rather than a memory error.

### On problem 4, decide the convention before coding

Write down whether `dp[i][j]` means "the first `i` characters" or "up to index `i`". Then write the base cases
from that sentence. Then write the table dimensions. Doing it in that order removes every off-by-one in this
problem.

### On problem 6, compute the state space first

For `nums` summing to `S`, the state is `(index, remaining_target)` and the space is `n × S/2`. Compute it for
`n = 200` with values up to 100, and again for values up to 10⁹. Say which one is viable and what that tells
you about the complexity class.

### Then the state-space audit

For each of the six problems, write down: the state as a sentence, the number of states as a formula, the work
per state, and the total. Six rows. **Any total above about ten million means the state is wrong or the
problem is not DP**, and this table is how you find that out in ten seconds.

### Then the redefinition drill

Take maximum subarray and write both states: "the best using elements 0..i" and "the best ending exactly at
i". For the first, try to write the recurrence and record where you get stuck. Then write the second and note
that the dimension count did not change.

---

### The test drill

1. State the test in one sentence.
2. Apply it to climbing stairs, knapsack, stock-with-one-transaction and edit distance.
3. For each failure, name the missing dimension.
4. Say what an incomplete state does, and why nothing reports it.

### The five-dimensions drill

Name each kind, give a problem, and say what the tell is:

1. A resource being consumed.
2. A count of something limited.
3. A mode you are in.
4. A position in a second sequence.
5. A set already used.

Then say which is the most expensive and at what `n` it stops being viable.

### The incomplete-versus-awkward drill

1. Define both, in one sentence each.
2. Give an example of each.
3. Say what the fix is for each.
4. Say what it costs to treat an awkward state as an incomplete one.

### The counting drill

1. Give the state-space formula for five different shapes.
2. Compute each at realistic sizes and say which are viable.
3. Say what the practical ceiling is in Python.
4. Explain what pseudo-polynomial means, using knapsack.
5. Say why that does not contradict knapsack being NP-hard.

### The break-it drill

Trigger each and record the exact output or error:

1. Knapsack with `dp[i]` only.
2. A hand-rolled cache keyed on fewer arguments than the function takes.
3. `@lru_cache` on a function taking a list.
4. A dimension that is derivable from the others.
5. A bitmask state at `n = 40`.
6. Transaction counting on both the buy and the sell.
7. `left == 0` as the base case when `left` means "used" rather than "remaining".

Five of the seven give no error at all. Name them.

---

### The requirements drill

1. Give the in-scope and out-of-scope lists.
2. Give the four non-functional requirements and say which one differs from a shortener.
3. Describe the read distribution in one sentence.

### The sizing drill

1. Do the full estimate from 1M pastes a day at 10 KB.
2. Compare writes and storage against the URL shortener, both directions.
3. Say the sentence that follows from the comparison.

### The storage drill

1. Give the numbers for content-in-database versus content-in-object-storage.
2. Say which of those numbers matters most during an incident, and why.
3. Explain the inline threshold and what it buys, with the latency figures.
4. Give the size distribution and the fraction the threshold covers.
5. Say what the `CHECK` constraint is for.

### The immutability drill

1. Say what property makes a paste perfectly cacheable.
2. Give the exact header and what each part does.
3. Say what that header costs you.
4. Say how you would resolve that conflict.

### The expiry drill

1. Say why a `DELETE ... WHERE expires_at < now()` job fails at scale.
2. Give the three mechanisms and say which one is the correctness mechanism.
3. Explain partition-by-expiry-day and what `DROP TABLE` buys.
4. Say how per-paste expiry maps onto per-prefix lifecycle rules.

### The viral drill

1. Compute requests per second for 100,000 reads in 20 minutes.
2. Give the three absorbing layers and what each handles.
3. Say which layer would actually struggle, and why.
4. Compute the egress for a 1 MB paste read 100,000 times, origin and CDN.
5. Say what you would monitor, and what a falling CDN hit rate usually means.

### The abuse drill

1. Name the five defences.
2. Say what content scanning looks for and what a good service does beyond blocking.
3. Say why `is_removed` rather than delete.
4. Say why a size limit is a product decision with a large blast radius.
5. State the conflict between caching and takedown, and your resolution.

### The failure drill

For each, say what happens and what you would build:

1. A 1 KB paste stored in object storage and read once.
2. 3.6 TB of paste content in the database, during a restore.
3. A `DELETE` expiry job on a 500-million-row table.
4. A 1 MB paste read 100,000 times from origin.
5. A paste removed after a CDN has cached it for a year.
6. A user pastes an AWS key into an "unlisted" paste.
7. The object write succeeds and the row insert fails.

Two of the seven are cost problems rather than correctness problems. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What does `dp[i]` represent in your solution?*
   The sentence, the test, what an incomplete state does and why it is silent, the five kinds of dimension,
   and the incomplete-versus-awkward distinction.

2. *Now there is a limit of at most k transactions.*
   Why `(day, holding)` is no longer enough, the third dimension, where the count is consumed and why that
   must be stated, the state-space arithmetic, and the `k > n/2` cap.

3. *Design pastebin. What happens when a paste goes viral?*
   The sizing ending in "fewer writes, six times the storage", the split with the inline threshold,
   immutability as the enabling property, the three caching layers with numbers, and the takedown conflict.

---

## Before you move on

- [ ] I apply the test before writing any DP.
- [ ] I write the state as a full sentence.
- [ ] I count the state space before coding.
- [ ] I know an incomplete state fails silently and why.
- [ ] I can name the five kinds of dimension with a problem for each.
- [ ] I know which dimension is expensive and at what `n`.
- [ ] I can distinguish incomplete from awkward, and know the fix for each.
- [ ] I know redefining is often better than extending.
- [ ] I know adding a dimension multiplies the state space.
- [ ] I know the practical ceiling is ~10⁷ states in Python.
- [ ] I can explain pseudo-polynomial using knapsack.
- [ ] I know why the cache key must be the complete state.
- [ ] I have seen the broken knapsack return the sum of everything.
- [ ] I know where a transaction count is consumed, and that it must be one place.
- [ ] I know `k > n/2` is the same as unlimited.
- [ ] I can size a pastebin and compare it with a shortener both ways.
- [ ] I can give the database-versus-object-storage numbers.
- [ ] I know which of those numbers matters during an incident.
- [ ] I can justify the inline threshold with latency figures.
- [ ] I know immutability is what makes the caching work.
- [ ] I can give the cache header and what it costs.
- [ ] I know why a `DELETE` expiry job fails, and the three mechanisms that replace it.
- [ ] I know the read-time check is the correctness mechanism.
- [ ] I can compute the viral case and name the layer that would struggle.
- [ ] I can compute egress for a large hot paste both ways.
- [ ] I can name five abuse defences.
- [ ] I can state the caching-versus-takedown conflict and resolve it.
- [ ] I know "unlisted" is not private and would say so in the product.
- [ ] I answered all three questions above out loud.
