---
day: 151
track: practice
title: "Practice — Coin Change II: counting"
status: written
---

# Day 151 · Practice

**DSA topic:** Coin Change II: counting
**System design topic:** Design a web crawler

---

## Code these, in this order

One rule for the whole set: **before writing the loops, decide out loud whether you are counting sets or
sequences, and name the evidence.** Then run the tiny hand-checkable case first. Two combinations, three
permutations, for `[1, 2]` to 3 — that pair is the fastest bug-catcher in dynamic programming.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Coin Change II | LeetCode 518 (Medium) | Combinations, and the coins-outside nesting. |
| 2 | Combination Sum IV | LeetCode 377 (Medium) | Permutations, and a name that points the wrong way. |
| 3 | Climbing Stairs | LeetCode 70 (Easy) | Permutations you have been writing as Fibonacci all along. |
| 4 | Decode Ways | LeetCode 91 (Medium) | Sum over last moves, with validity conditions. |
| 5 | Unique Paths | LeetCode 62 (Medium) | Counting on a grid, and the one-row collapse. |
| 6 | Number of Dice Rolls With Target Sum | LeetCode 1155 (Medium) | Permutations with a fixed count — a second dimension. |

### On problem 1, run the tiny case before anything else

`coins = [1, 2]`, `amount = 3`. It must give **2**. If it gives 3, swap the loops. Then list both sets by hand
and confirm the program is counting what you listed.

### On problem 1, write the enumerator too

Write a backtracking function that returns the actual lists, and check it against the count on five small
inputs. Then run the enumerator on `amount = 100`, `coins = 1..10` and record how long it takes and how much
memory it uses. **Say in one sentence why counting is a separate problem from listing.**

### On problems 1 and 2, swap the nesting deliberately

Take your combinations solution and swap the two loops. Confirm you get the permutations answer. Then swap
problem 2's loops and confirm you get combinations. **Write one sentence explaining why coins-outside cannot
produce `2+1`.**

### On problem 3, notice what you have written

After solving it with the counting loops, write out `ways[t] = ways[t-1] + ways[t-2]`. **Say what sequence that
is.** Then say why stairs is permutations and why that is correct rather than a mistake.

### On problem 4, get the base case right first

Write `ways[0] = 1` and say what "one way to decode nothing" means. Then handle `'0'` and `'06'` and `'100'` —
record what each returns. **Say which of those three is the one people get wrong.**

### On problem 6, count the state space

State it as a sentence with both dimensions. Count the states for 30 dice, 30 faces, target 1000. Multiply by
the work per state. Say whether it is viable, and what the modulus is for.

### Then the modulus drill

Take problem 1, remove the modulus, and compute the exact answer for `amount = 5000` with coins `1..200`.
Record the number of digits. Then say what a Java `long` would have done, and where exactly the modulus has to
go.

---

### The sets-or-sequences drill

For each, say which it counts and give the evidence in one sentence:

1. Coin Change II.
2. Combination Sum IV.
3. Climbing stairs.
4. Ways to make change at a shop counter.
5. Dice rolls summing to a target.

### The nesting drill

1. Say what coins-outside guarantees, in terms of order.
2. Say what amount-outside allows.
3. Give both answers for `[1,2]` to 3 and list the arrangements.
4. Give the debugging heuristic about answer size, with the `[1,2,5]` to 30 numbers.
5. Say what the cost difference between the two nestings is. (There isn't one — say that.)

### The base-case drill

1. Say what `ways[0] = 1` means in words.
2. Say what the table does without it, and how that reads from outside.
3. Say what the equivalent is for Decode Ways.
4. Say why minimising uses `0` here and counting uses `1`.

### The modulus drill

1. Give the digit count for 5,000 from coins 1..200.
2. Say what a Java `long` holds and when it wraps.
3. Say exactly where the modulus goes and why not at the end.
4. Say why `10^9 + 7` specifically.
5. Say what happens if you add a modulus the problem did not ask for.

### The counting-versus-listing drill

1. Give the count and the list size for 100 from coins 1..10.
2. Say what algorithm each needs.
3. Say what trick the enumerator uses to avoid emitting duplicates.
4. Say what you would do if asked to enumerate a million results.

### The break-it drill

Trigger each and record the exact output or error:

1. Swapped loop nesting on a combinations problem.
2. Missing `ways[0] = 1`.
3. The backwards inner loop.
4. A coin of zero.
5. Modulus only at the return, in a language with fixed-width integers.
6. A modulus on a problem that did not ask for one.
7. `[0] * (10**9 + 1)`.

Six of the seven give no error at all. Name them.

---

### The loop drill

1. Give the four steps of the crawl loop.
2. Say what the frontier and the seen set are, in graph terms.
3. Say what makes this harder than a normal BFS, in three points.

### The dedup drill

1. Name the three levels and what each catches.
2. Say which one saves bandwidth and which two do not.
3. List six normalisation steps.
4. Say which normalisation step people forget, and why it matters.
5. Explain SimHash in two sentences — what makes it different from a normal hash.
6. Give the seen-set sizes for strings, hashes and a Bloom filter.
7. Say what a Bloom filter false positive costs here, and whether it is acceptable.

### The politeness drill

1. Say why a single FIFO frontier fails, and why it is the normal case rather than an edge case.
2. Describe the per-host queue design and the ready heap.
3. Say what clock the heap uses and why.
4. Say what you do about `robots.txt`, including the TTL and the unreachable case.
5. Compute how long a 100,000-page site takes at one request per second.
6. Say what actually bounds overall throughput.

### The frontier drill

1. Say why there are two tiers and what each does.
2. Say what the router's real job is.
3. Say why a single priority queue cannot do both.
4. Say how you would partition the frontier across machines, and what that buys.

### The trap drill

1. Give three traps and say which are malicious. (Mostly none — say that.)
2. Name the four heuristics.
3. Say what content-based detection adds.
4. Say what these heuristics cost, and why the trade is still right.
5. Say what you would do so that a truncated site is not lost silently.

### The freshness drill

1. Say what fraction of a monthly recrawl is wasted, and on what.
2. Give the `If-Modified-Since` arithmetic, both totals.
3. Describe the change-rate estimator in one sentence.
4. Name two other signals you would use.
5. Say why there must be a floor and a ceiling.

### The sizing drill

1. Compute pages per second and machines for 1 billion pages a month.
2. Compute inbound bandwidth and monthly storage.
3. Compute the host-diversity requirement.
4. Say what DNS does if you do not cache it.
5. Say what JavaScript rendering costs and what it does to the machine count.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many combinations of coins make the amount?*
   Sets versus sequences with the `[1,2]` to 3 numbers, the state, `ways[0] = 1` and what it means, the
   nesting with its reason, and the modulus.

2. *Does the order of the loops matter?*
   Both nestings, why coins-outside fixes an order, the arrangements listed, the explosion heuristic, and
   which LeetCode problem wants which.

3. *Design a web crawler.*
   The four-step loop, three levels of dedup and which saves bandwidth, why one FIFO fails and the per-host
   queue, the two-tier frontier, and the host-diversity number.

---

## Before you move on

- [ ] I decide sets or sequences before writing any loops.
- [ ] I know `[1,2]` to 3 gives 2 combinations and 3 permutations.
- [ ] I know coins-outside counts combinations, and why.
- [ ] I know amount-outside counts permutations, and why.
- [ ] I can explain why coins-outside cannot produce `2+1`.
- [ ] I know `ways[0] = 1` and what it means in words.
- [ ] I know what a missing base case looks like from outside.
- [ ] I know swapping the loops does not change the cost.
- [ ] I know permutations explode, and can use that as a debugging signal.
- [ ] I know Combination Sum IV wants permutations despite its name.
- [ ] I know climbing stairs is permutations, and is Fibonacci.
- [ ] I can write Decode Ways with both validity conditions.
- [ ] I know where the modulus goes and why not at the end.
- [ ] I know why `10^9 + 7`.
- [ ] I know not to add a modulus the problem did not ask for.
- [ ] I know counting and listing are different algorithms with different costs.
- [ ] I can give the four steps of the crawl loop.
- [ ] I can name the three dedup levels and which saves bandwidth.
- [ ] I can list six URL normalisation steps.
- [ ] I can explain SimHash and what makes it unlike a normal hash.
- [ ] I can give the three seen-set sizes.
- [ ] I know what a Bloom filter false positive costs a crawler.
- [ ] I can explain why one FIFO frontier fails.
- [ ] I can describe the per-host queue and the ready heap.
- [ ] I know the `robots.txt` policy including the unreachable case.
- [ ] I can compute the host-diversity requirement and say what it bounds.
- [ ] I know why the frontier has two tiers.
- [ ] I can name four trap heuristics and say what they cost.
- [ ] I can give the `If-Modified-Since` arithmetic.
- [ ] I know what JavaScript rendering does to the machine count.
- [ ] I answered all three questions above out loud.
