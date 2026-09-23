---
day: 149
track: practice
title: "Practice — Subset sum and partition problems"
status: written
---

# Day 149 · Practice

**DSA topic:** Subset sum and partition problems
**System design topic:** Design a distributed key-value store

---

## Code these, in this order

One rule for the whole set: **before writing a line, say out loud what `T` is and where it came from.** Every
problem here is subset sum; the only work is the algebra that produces the target. Do that algebra out loud
first, every time, and the code takes four minutes.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Partition Equal Subset Sum | LeetCode 416 (Medium) | The reduction to `T = S/2`, and the odd-total exit. |
| 2 | Partition Array Into Two Arrays to Minimize Sum Difference | LeetCode 2035 (Hard) | The same table, scanned instead of indexed. |
| 3 | Target Sum | LeetCode 494 (Medium) | Two lines of algebra, and counting instead of deciding. |
| 4 | Last Stone Weight II | LeetCode 1049 (Medium) | The best-hidden disguise in the set. |
| 5 | Partition to K Equal Sum Subsets | LeetCode 698 (Medium) | Where subset sum stops working and backtracking starts. |
| 6 | Ones and Zeroes | LeetCode 474 (Medium) | Two targets at once — the same idea in three dimensions. |

### On problem 1, write the odd check before anything else

One line, before the table. Then run it on an array of a thousand odd-ish numbers and record how long the
answer takes with and without that line. **Say in one sentence why the check is not a correctness fix.**

### On problem 1, reverse the inner loop and watch nothing happen

Change `range(target, number - 1, -1)` to `range(number, target + 1)`. Run on `[3]` with `target = 9`. Record
the answer. **Then say which problem you just solved instead**, and how you would catch this without running
it.

### On problem 3, do the algebra on the board first

Write out `P - N = target`, `P + N = total`, and derive `P = (target + total) / 2`. Then write the two
conditions that make the answer zero. Then code.

Now delete the parity check and run on `nums = [1, 2, 3]`, `target = 1`. Record what it returns. **Say why the
wrong answer is plausible rather than obviously broken.**

### On problem 4, describe the smash before you code

In one sentence, say what a smash is in terms of signs. Then say what the final stone equals in terms of two
group sums. **Then notice you have written problem 2's statement.** Solve it by calling your problem 2
function.

### On problem 5, find where the reduction breaks

Try to solve it as subset sum with `T = S / k`. Run it on `[4, 3, 2, 3, 5, 2, 1]` with `k = 4`. Say in one
sentence why finding one subset summing to `S/k` is not enough, and what has to change.

### On problem 6, state it as a sentence and count

Write the state as a full sentence with both resources named. Count the states for `m = 100`, `n = 100`, 600
strings. Say what the three loop directions must be and why.

### Then the bitset drill

Rewrite problem 1 with `reachable |= reachable << number`. Verify agreement with your table version on twenty
random inputs. Then time both at `n = 200`, values up to 1,000, and record the ratio.

---

### The reduction drill

For each, state `T` and the reason, in one sentence:

1. Equal partition.
2. Minimum difference.
3. Target sum.
4. Last stone weight II.
5. A subset summing to exactly `T`.

Then say which two of those five are the same problem.

### The direction drill

1. Say what `range(target, number - 1, -1)` guarantees about what each read holds.
2. Say what the forward loop solves instead.
3. Say what the error message is. (There isn't one — say that, and say what you do about it.)
4. Give the one-number example that proves the forward loop wrong.

### The base-case drill

1. Say why `reachable[0] = True`, in words about subsets.
2. Say what the whole table does if you leave it out, and what it looks like from outside.
3. Say what the counting version's base case is and why it is `1`.

### The pseudo-polynomial drill

1. Give the running time and the space.
2. Give the input size in bits for `n = 200` numbers of 30 bits.
3. Say why `O(n × T)` is exponential in that.
4. Compute the memory for `T = 10^9` and give the exact error.
5. Say which constraint you check first in an interview, and why it is the reverse of usual.

### The break-it drill

Trigger each and record the exact output or error:

1. The forward inner loop.
2. A missing `reachable[0] = True`.
3. A negative index from an unguarded `t - number`.
4. A float in the input.
5. `[False] * (10**9 + 1)`.
6. Target Sum without the parity guard.
7. Reconstruction from the one-row version.

Five of the seven give no error at all. Name them.

---

### The partitioning drill

1. Say why `hash(key) % n` is unusable, with the percentage.
2. Describe the ring in three sentences.
3. Say what virtual nodes fix, and give both benefits.
4. Compute the data moved by both schemes for 1 billion keys, 10 machines to 11.
5. Say what the preference list must skip, and what breaks if it does not.

### The quorum drill

1. State `N`, `R` and `W` in one sentence each.
2. Give the `R + W > N` argument as counting, not protocol.
3. Give three configurations and what each is for.
4. Say why `R = 2` and not `R = 3`, with the latency numbers.
5. Say what `R + W > N` does *not* give you.
6. Say what happens to writes when two of three replicas are down, and what a sloppy quorum does about it.

### The conflict drill

1. Say why timestamps cannot order two concurrent writes.
2. Give last-write-wins and its exact failure mode.
3. Explain a vector clock comparison and its three outcomes.
4. Work the `{A:2}` versus `{A:1,B:1}` example out loud.
5. Say what `get` returns and why that is an API decision.
6. Give the cart merge, and one case where union is wrong.
7. Say what truncation costs and why it is safe.

### The repair drill

1. Name the three mechanisms and what each covers.
2. Say what hinted handoff buys and when it fails.
3. Say what read repair misses, and why that is the worst case.
4. Explain a Merkle tree comparison and quantify the saving.
5. Say what happens to a node that has been down for a week.

### The sizing drill

1. Do the storage estimate for 1 billion keys at 1 KB, `N = 3`.
2. Do the throughput estimate and say which one sets the machine count.
3. Give the three read latencies for `R = 1, 2, 3`.
4. Compute the vector clock overhead on a 1 KB value and a 50 B value.
5. Give the Merkle saving as a ratio.

### The when-not-to drill

1. Say what a single Postgres handles, with numbers.
2. Say at what point this design earns its complexity.
3. Say why etcd is not this design, and what it is for.
4. Say the honest cost of eventual consistency, in terms of the application code.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can this array be split into two halves with equal sums?*
   The reduction, the odd-total exit, the state as a sentence, the base case, the backwards loop with its
   reason, and the complexity with the target-size caveat.

2. *Subset sum is NP-complete and you solved it in `O(n × T)`. Explain.*
   Input size in bits, `n × 2^(log T)`, the practical version, which constraint you check, and what exists
   when the numbers are large.

3. *Design a key-value store like DynamoDB.*
   Consistent hashing with the 91% number, virtual nodes, `N = 3` with the distinctness check, `R + W > N`
   as counting, vector clocks with both versions kept, and the three repair mechanisms.

---

## Before you move on

- [ ] I can state the subset sum state as a full sentence.
- [ ] I know the base case is `reachable[0] = True` and why.
- [ ] I know what a missing base case looks like from outside.
- [ ] I run the inner loop backwards and can say why.
- [ ] I know the forward loop solves the unbounded problem, silently.
- [ ] I can give the one-number example that proves it.
- [ ] I can reduce equal partition and know the odd-total exit.
- [ ] I can reduce minimum difference and scan the row correctly.
- [ ] I can do the Target Sum algebra from memory.
- [ ] I know both conditions that make Target Sum zero.
- [ ] I know the counting version uses `ways[0] = 1` and `+=`.
- [ ] I recognised Last Stone Weight II as minimum difference.
- [ ] I know where the reduction stops working, at `k` subsets.
- [ ] I can give time and space for both versions.
- [ ] I can explain pseudo-polynomial with the bit count.
- [ ] I check the bound on the values before writing anything.
- [ ] I have implemented and timed the bitset version.
- [ ] I know reconstruction needs the full table.
- [ ] I can explain why modulo hashing is unusable, with the number.
- [ ] I can describe the ring and virtual nodes, and both benefits.
- [ ] I know the preference list must skip same-machine vnodes and AZs.
- [ ] I can give `R + W > N` as a counting argument.
- [ ] I know why `R = 2` and not `R = 3`, with latencies.
- [ ] I know what `R + W > N` does not guarantee.
- [ ] I can explain why timestamps cannot order concurrent writes.
- [ ] I can compare two vector clocks and get the right answer.
- [ ] I know `get` returns a list and why.
- [ ] I can name the three repair mechanisms and what each covers.
- [ ] I can quantify the Merkle tree saving.
- [ ] I can say when I would not build this at all.
- [ ] I answered all three questions above out loud.
