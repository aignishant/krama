---
day: 148
track: practice
title: "Practice — The 0/1 knapsack"
status: written
---

# Day 148 · Practice

**DSA topic:** The 0/1 knapsack
**System design topic:** Design a rate limiter, at system scale

---

## Code these, in this order

One rule for the whole set: **before writing the loops, say the state as a sentence and say which direction
the inner loop runs, and why.** Knapsack is the one topic where the same six lines, with the range reversed,
solve a completely different problem and never tell you which one you wrote.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | 0/1 Knapsack | classic — write it yourself | Two dimensions, take-or-skip, and the greedy counter-example. |
| 2 | Partition Equal Subset Sum | LeetCode 416 (Medium) | Subset sum in disguise, and spotting the odd-total shortcut. |
| 3 | Target Sum | LeetCode 494 (Medium) | An algebraic rewrite into subset-sum counting. |
| 4 | Last Stone Weight II | LeetCode 1049 (Medium) | The same rewrite again, hidden much better. |
| 5 | Ones and Zeroes | LeetCode 474 (Medium) | Two resource dimensions at once — a three-dimensional table. |
| 6 | Coin Change | LeetCode 322 (Medium) | Unbounded, so tomorrow's loop direction. Do it to feel the difference. |

### On problem 1, build the greedy counter-examples yourself

Write `greedy_by_value` and `greedy_by_ratio` before you write the DP. Run both on `capacity = 10` with items
`(10, 60), (5, 50), (5, 50)`, then on `capacity = 10` with `(6, 60), (5, 40), (5, 40)`. Record the four numbers.

Then say, in one sentence, why the ratio version is provably correct for the fractional version of the problem
and collapses here. **That sentence is the answer to "why not greedy", and it is worth more than the DP.**

### On problem 1, reverse the inner loop and see nothing happen

Take the working one-row solution and change `range(capacity, weight - 1, -1)` to
`range(weight, capacity + 1)`. Run it on `capacity = 10` with `(5, 50)` alone. Record the answer, and say
which problem you have now solved.

**No error, no warning, a plausible number.** Write one sentence on how you would catch this in an interview
without running anything.

### On problems 3 and 4, do the algebra before the code

For Target Sum, write out the two-line derivation from `P - N = target` and `P + N = total` to
`P = (target + total) / 2`. Then state the two conditions under which the answer is immediately zero.

For Last Stone Weight II, say in one sentence what the smashing actually is, and why it becomes
"split into two groups with the closest possible sums".

**Both problems are the same trick and neither looks like knapsack.** Do them back to back.

### On problem 5, count the state space first

Write the state as a sentence, count the states, and multiply by the work per state. Do it for `m = 100`,
`n = 100`, and 600 strings. Say whether it is viable and what the loop directions have to be.

### On problem 6, feel the difference

Solve it with the forward loop. Then try the backward loop and record what changes. **The two answers are both
correct programs for different problems**, and having produced both deliberately is the point.

### Then the bitset drill

Implement subset-sum with `reachable |= reachable << number` on a Python integer. Run it against your table
version on ten random inputs and confirm they agree. Then time both at `n = 200` with values up to 1,000, and
record the ratio.

---

### The greedy drill

1. Give the by-value counter-example with exact numbers, and both answers.
2. Give the by-ratio counter-example with exact numbers, and both answers.
3. Say which greedy *is* correct, and for which version of the problem.
4. Say in one sentence what indivisibility breaks.

### The state drill

1. State the knapsack state as a full sentence.
2. Say why one index is not enough, and what the broken version returns.
3. Write the recurrence, both branches, and name the guard on the take branch.
4. Give the base cases and say what each one means in words.

### The direction drill

1. Say what `range(capacity, weight - 1, -1)` guarantees, in one sentence about which values have been
   updated.
2. Say what the forward loop allows, and name the problem it solves.
3. Say why neither produces an error.
4. Say how you would state this out loud while writing it, so an interviewer sees you know.

### The reconstruction drill

1. Say what you need to keep in order to recover which items were chosen.
2. Say why the one-row version cannot do it.
3. Give the walk-back rule in one sentence.
4. Say what it costs in space, and when it is worth paying.

### The complexity drill

1. Give time and space for the table version and the one-row version.
2. Explain what pseudo-polynomial means, using `W` and the number of bits in `W`.
3. Compute the table size for `n = 100, W = 1,000` and for `n = 100, W = 10⁹`.
4. Say why this does not contradict knapsack being NP-hard.

### The break-it drill

Trigger each and record the exact output or error:

1. The inner loop forward when you meant 0/1.
2. `dp[i]` with one dimension only.
3. The take branch without the `weight <= capacity` guard.
4. Subset sum on an odd total.
5. Float weights in the table version.
6. `W = 10**9` as a table dimension.
7. The one-row version, then asking which items were taken.

Four of the seven give no error at all. Name them.

---

### The algorithm drill

1. Name the five algorithms and the state each keeps per key.
2. Give the boundary problem with exact timestamps and the resulting count.
3. Give the sliding-window-counter formula and work one example with numbers.
4. Say what the approximation assumes, and when it is wrong.
5. Say what token bucket's two numbers mean, separately.

### The sizing drill

1. Compute memory per key for all four algorithms at 1M keys, limit 1,000/hour.
2. Say which one you reject and by what factor.
3. Compute the limiter's latency as a percentage of a 20 ms service and a 2 ms service.
4. Say how many Redis instances 1M requests/s needs, and why sharding is trivial here.

### The distributed drill

1. Name the three approaches and the cost of each.
2. Say why limit-divided-by-`n` fails, in one sentence about load balancers.
3. Compute the over-admission bound for 10 machines, limit 100/minute, 10 s sync.
4. Say the honest one-sentence description of the limit you are actually enforcing.

### The failure drill

1. Say what fail-open costs and what fail-closed costs.
2. Give the third option and why it is the answer.
3. Say why the limiter needs a circuit breaker in front of it.
4. Say what a *slow* Redis does that a *dead* Redis does not.

### The response drill

1. Give the status code and the four headers.
2. Say which header matters most, and why.
3. Say what happens without jitter.
4. Say why the headers belong on successful responses too.

### The placement drill

1. Say where the limiter goes and give three reasons.
2. Say what the second, cruder layer is for.
3. Name the four things you limit on and the weakness of the IP one.
4. Say what per-request cost buys you over per-endpoint limits.

### The lazy-refill drill

1. Write the refill line from memory.
2. Say why `time.monotonic()` and not `time.time()`.
3. Say what a backwards clock step does and what a forwards one does.
4. Say what `EXPIRE` is for and what happens without it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Solve the knapsack problem.*
   Why greedy fails with both counter-examples and their numbers, the state as a sentence, the recurrence,
   the complexity, the one-row collapse, and the loop direction with what the reverse would mean.

2. *Why can't you just take the highest value-per-kilo item first?*
   The counter-example, the fractional-versus-0/1 distinction, and what indivisibility breaks.

3. *Design a rate limiter for an API used by a million clients.*
   The boundary problem with timestamps, why not the sliding log with the memory figures, the sliding window
   counter or token bucket with its two numbers, the distributed choice with a stated bound, and the failure
   policy.

---

## Before you move on

- [ ] I can give the by-value greedy counter-example with numbers.
- [ ] I can give the by-ratio greedy counter-example with numbers.
- [ ] I know which greedy is correct and for which problem.
- [ ] I can say what indivisibility breaks, in one sentence.
- [ ] I can state the knapsack state as a full sentence.
- [ ] I know what the one-dimensional version returns and why.
- [ ] I can write the recurrence with both branches and the guard.
- [ ] I can give the base cases and say what they mean.
- [ ] I know the one-row collapse and why it works.
- [ ] I know the inner loop runs backwards for 0/1, and can say why.
- [ ] I know the forward loop solves unbounded, and that neither errors.
- [ ] I can give time and space for both versions.
- [ ] I can explain pseudo-polynomial and why it is not a contradiction.
- [ ] I can reconstruct the chosen items and know what that costs.
- [ ] I can recognise subset sum and partition as knapsack.
- [ ] I know the odd-total shortcut.
- [ ] I can do the Target Sum algebra from memory.
- [ ] I have implemented the bitset version and timed it.
- [ ] I can name the five rate-limiting algorithms and their state.
- [ ] I can give the boundary problem with timestamps.
- [ ] I can give the sliding-window-counter formula and work an example.
- [ ] I know why the sliding log is rejected, with the memory figures.
- [ ] I know token bucket's two numbers do two different jobs.
- [ ] I know the difference between token bucket and leaky bucket.
- [ ] I can name the three distributed approaches and their costs.
- [ ] I can compute the over-admission bound.
- [ ] I know the failure policy is fail open with a local fallback.
- [ ] I know why the limiter needs its own circuit breaker.
- [ ] I know `429`, `Retry-After`, and why the retry must be jittered.
- [ ] I answered all three questions above out loud.
