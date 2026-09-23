---
day: 150
track: practice
title: "Practice — Unbounded knapsack and coin change"
status: written
---

# Day 150 · Practice

**DSA topic:** Unbounded knapsack and coin change
**System design topic:** Design a distributed unique ID generator

---

## Code these, in this order

One rule for the whole set: **say the loop direction and its reason out loud before writing the inner loop, and
say which loop is on the outside and why.** Two decisions, four words each, and they are the only thing
separating these six problems from each other.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Coin Change | LeetCode 322 (Medium) | Forwards, `min`, and the infinity sentinel. |
| 2 | Coin Change II | LeetCode 518 (Medium) | Counting combinations — coins on the outside. |
| 3 | Combination Sum IV | LeetCode 377 (Medium) | Counting permutations — amount on the outside. |
| 4 | Perfect Squares | LeetCode 279 (Medium) | Coin change where you generate the coins. |
| 5 | Minimum Cost For Tickets | LeetCode 983 (Medium) | Unbounded, with an unusual "coin" — a duration. |
| 6 | Integer Break | LeetCode 343 (Medium) | Unbounded knapsack maximising a product. |

### On problem 1, write greedy first and break it

Implement biggest-coin-first. Run it and the DP on `coins = [1, 5, 7]`, `amount = 10`, and record both
answers. Then run both on `[1, 2, 5]` with `amount = 11` and record those.

**Say in one sentence why the second pair agrees**, and what that tells you about why nobody notices greedy is
wrong.

### On problem 1, reverse the loop and get "impossible"

Change `range(coin, amount + 1)` to `range(amount, coin - 1, -1)`. Run on `coins = [3]`, `amount = 9`. Record
what comes back.

Then run the same broken version on `[1, 2, 5]` with `amount = 8` and record that. **Say why the second test
passes**, and what that means for how you choose test inputs.

### On problem 1, try all three wrong sentinels

Initialise `dp` to `0`, then to `-1`, then to `float('inf')`. Run each on `[1, 5, 7]` with `amount = 10` and
record all three answers. **Two of them are plausible numbers rather than errors.** Say which, and why that is
worse than crashing.

### On problems 2 and 3, run the same input through both

Give both `coins = [1, 2]` and `amount = 3`. Record both answers. Then list the actual arrangements each one
counted, by hand. **Then swap the loop nesting in problem 2 and confirm you get problem 3's answer.**

Write one sentence explaining why coins-outside cannot produce `2+1`.

### On problem 4, notice you already solved it

Before coding: say what the coins are. Then say what the amount is. **Then call your problem 1 function.**

### On problem 5, find the coin

The costs are 1-day, 7-day and 30-day passes. Say what plays the role of a coin and what plays the role of the
amount. **Note that the state runs over days, not over money**, and say why that changes which direction the
loop runs.

### Then the BFS drill

Solve problem 1 with BFS instead — amounts as nodes, coins as unit edges. Verify agreement on twenty random
inputs. Then time both on `coins = [1, 5000]`, `amount = 10000` and record the ratio. **Say why the gap is that
large.**

---

### The greedy drill

1. Give the counter-example with exact coins and both answers.
2. Say why greedy works for Indian denominations.
3. Say what a "canonical" coin system is, in one sentence.
4. Say what greedy costs and what DP costs, and what the difference buys.

### The direction drill

1. Say what the backwards loop guarantees about the cell being read.
2. Say what the forwards loop allows, and which problem that is.
3. Give the one-coin example that separates them.
4. Say what the error message is, and what you do instead.
5. Say what kind of test input would hide the bug.

### The sentinel drill

1. Say what `dp[0]` is for minimum coins, and why.
2. Say what the rest starts at, and why.
3. Say what `0` produces instead, and what `-1` produces.
4. Give the exact error from `int(float('inf'))`.
5. Say where the conversion to `-1` belongs.

### The loop-order drill

1. Say what coins-outside counts and what amount-outside counts.
2. Give both answers for `[1, 2]` and amount 3, and list the arrangements.
3. Explain in one sentence why coins-outside cannot form `2+1`.
4. Say which LeetCode problem wants which, and why one name misleads.
5. Say how you decide when the problem statement is ambiguous.

### The family drill

Fill in the table from memory: cell type, operator, base case.

1. Subset sum.
2. Count the ways.
3. Minimum coins.
4. Maximum value, unbounded.

Then say what stays the same across all four.

### The break-it drill

Trigger each and record the exact output or error:

1. The backwards loop on `[3]` with amount 9.
2. `dp` initialised to `0`.
3. `dp` initialised to `-1`.
4. Missing `ways[0] = 1`.
5. Swapped loop nesting in the counting version.
6. `int(float('inf'))`.
7. `[float('inf')] * (10**9 + 1)`.

Five of the seven give no error at all. Name them.

---

### The layout drill

1. Give all four fields and their widths, in order.
2. Say what each width buys, with the arithmetic.
3. Say why the timestamp is first — the real reason, about integers.
4. Say what the custom epoch is worth, in years.
5. Say what the sign bit is for.

### The UUID drill

1. Give the size difference and multiply it out at 1 billion rows.
2. Explain the B-tree argument in three sentences.
3. Give the insert throughput ratio.
4. Say why the degradation is dangerous, not just bad.
5. Say what UUIDv7 fixes and what it still costs.
6. Name two cases where UUIDv4 is the right answer.

### The clock drill

1. Say exactly what breaks when the clock steps backwards.
2. Say why it is close to unrecoverable.
3. Give the three defences and which one is prevention.
4. Say what slewing is and how long a 1-second correction takes.
5. Say where the threshold between wait and refuse sits, and that it is policy.
6. Say what the monotonic clock gives you and what it does not.

### The machine-id drill

1. Say why a config file is not acceptable, and what the failure looks like.
2. Name the three real mechanisms.
3. Say what ZooKeeper costs you at boot.
4. Give the exact case where IP derivation collides.
5. Say why Kubernetes ordinals are structurally better.
6. Say what detection you would add regardless.

### The sequence drill

1. Say how many IDs per millisecond and per second per machine.
2. Compare that with a real workload, with numbers.
3. Say what happens on exhaustion, and name the two wrong answers.
4. Say why the branch must be correct even though it never runs.

### The privacy drill

1. Say exactly what a sortable ID leaks.
2. Give the measurement anyone can perform.
3. Give two ways to expose a public identifier instead.
4. Say which you prefer and why.
5. Say whether UUIDv7 solves this.

### The when-not-to drill

1. Say at what scale an auto-increment is the right answer.
2. Say what a ticket server is and its one weakness.
3. Say when only UUIDs work.
4. Say why you might choose UUIDv7 over Snowflake at moderate scale.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the fewest coins that make the amount.*
   The greedy counter-example, the state as a sentence, the recurrence as "what was the last coin", the
   infinity sentinel, the forwards loop with its reason, and the amount-size caveat.

2. *Now count how many combinations make the amount. Does the loop order matter?*
   Both answers for `[1,2]` and 3, why coins-outside fixes the order, which problem wants which, and the
   modulus warning.

3. *Generate unique IDs across a hundred servers. No central counter.*
   The four fields and their widths, why the timestamp is first, the UUID index argument, the clock-backwards
   handling, and where the machine id comes from.

---

## Before you move on

- [ ] I can give the greedy counter-example with exact numbers.
- [ ] I know why greedy works for Indian denominations.
- [ ] I can state the minimum-coins state as a full sentence.
- [ ] I can give the recurrence as "what was the last coin".
- [ ] I know `dp[0] = 0` and the rest is infinity, and why.
- [ ] I know what `0` and `-1` sentinels produce instead.
- [ ] I know `int(float('inf'))` raises, and where to check.
- [ ] I run the inner loop forwards and can say why.
- [ ] I know the backwards loop reports "impossible" on `[3]` to 9.
- [ ] I know which test inputs would hide that bug.
- [ ] I know `ways[0] = 1` and why it is the seed.
- [ ] I know coins-outside counts combinations.
- [ ] I know amount-outside counts permutations.
- [ ] I can list both sets of arrangements for `[1,2]` to 3.
- [ ] I know Combination Sum IV wants permutations despite its name.
- [ ] I can fill in the four-row family table from memory.
- [ ] I can give time and space, and the amount-size caveat.
- [ ] I know minimum coins is also a BFS, and when that wins.
- [ ] I can reconstruct the coins used, and know it is cheap here.
- [ ] I can lay out the 64 bits and justify every width.
- [ ] I know why the timestamp is in the high bits.
- [ ] I know what the custom epoch is worth.
- [ ] I can give the UUID size difference at 1 billion rows.
- [ ] I can explain the B-tree argument without notes.
- [ ] I know the insert throughput ratio and why it degrades invisibly.
- [ ] I know what UUIDv7 fixes and what it costs.
- [ ] I can say exactly what a backwards clock does.
- [ ] I know the three clock defences and which is prevention.
- [ ] I know the three machine-id mechanisms and why not a config file.
- [ ] I know what a sortable ID leaks and how to fix it.
- [ ] I answered all three questions above out loud.
