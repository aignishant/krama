---
day: 156
track: practice
title: "Practice — Grid DP: unique paths"
status: written
---

# Day 156 · Practice

**DSA topic:** Grid DP: unique paths
**System design topic:** Design WhatsApp

---

## Code these, in this order

One rule for the whole set: **write the base cases before the recurrence, and say what they mean.** The
recurrence barely changes across these six problems. The base cases change every time, and that is where every
bug is.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Unique Paths | LeetCode 62 (Medium) | The cleanest state in DP, and the one-row collapse. |
| 2 | Unique Paths II | LeetCode 63 (Medium) | Obstacles, and the first row that is no longer all ones. |
| 3 | Minimum Path Sum | LeetCode 64 (Medium) | Same state, `min`, and running-sum base cases. |
| 4 | Triangle | LeetCode 120 (Medium) | A grid that is not rectangular, and filling upwards. |
| 5 | Minimum Falling Path Sum | LeetCode 931 (Medium) | Where the one-row trick breaks, and why. |
| 6 | Maximal Square | LeetCode 221 (Medium) | An "ending at" state, so the answer is not the last cell. |

### On problem 1, do it three ways

Write the full table, the one-row version and the closed form. Confirm all three agree on ten random sizes.
**Then say, in one sentence each, what the one-row version costs you and what the formula costs you.**

### On problem 1, point at the two values

In the one-row version, print `row` mid-pass and mark which entries are the previous row and which are the
current one. **Say which side of the cursor is which**, and why that makes `row[c] += row[c-1]` correct.

### On problem 2, keep the initialise-to-1 trick

Use `[[1] * cols for _ in range(rows)]` with obstacles. Run on a 3×4 grid with one obstacle in the top row and
record the answer. Then run the no-obstacle version on the same shape. **Say why the two numbers are the same
and what that tells you.**

### On problem 3, keep the counting base cases

Leave the first row and column as zeros. Run on `[[1,3,1],[1,5,1],[4,2,1]]` and record the answer against the
correct 7. **Say what the algorithm believed about the edges.**

### On problem 3, use 0 for a blocked cell

Add an obstacle and mark it `0` instead of infinity. Say what the `min` does with it. **Then say why the
counting version uses `0` and the cost version cannot.**

### On problem 5, apply the one-row trick anyway

Update the row in place. Run on `[[2,1,3],[6,5,4],[7,8,9]]` and record the answer against the correct one.
**Say exactly which read was of the wrong generation**, and what the precondition for the trick actually is.

### On problem 6, return the last cell

Run `maximal_square` returning `dp[-1][-1]` instead of the maximum. Find an input where it differs. **Say which
other problem this week had the same property, and what the two states have in common.**

### Then the counting-overflow drill

Compute `unique_paths_formula` for a 40×40 grid and count the digits. Say what a Java `long` would have done.
**Then say which of the two approaches — table or formula — handles a required modulus more easily, and why.**

---

### The state drill

1. State it in one sentence.
2. Say why no redefinition is needed here, unlike the last four days.
3. Say why adding, not maxing, is correct for the counting version.
4. Give the base cases and what each means in words.

### The collapse drill

1. Say which two cells the recurrence reads.
2. Say what `row[c]` is before it is overwritten, and what `row[c-1]` is.
3. Give the space numbers at 1,000² and 10,000².
4. State the precondition for the trick in one sentence.
5. Name the variant that violates it and say what it needs instead.

### The base-case drill

For each, give the first row and first column and say why:

1. Counting paths, no obstacles.
2. Counting paths with obstacles.
3. Minimum path sum.
4. Minimum path sum with blocked cells.

### The formula drill

1. Derive it: how many moves, how many are down.
2. Give the expression and check it on a 2×2 grid.
3. Give the time and space.
4. Say what breaks it, and why inclusion-exclusion does not save you.
5. Say what happens if the problem demands a modulus.

### The family drill

Name the change for each:

1. Minimum path sum.
2. Obstacles.
3. Diagonal moves allowed.
4. Minimum falling path.
5. Maximal square.
6. Two walkers at once.

### The break-it drill

Trigger each and record the exact output or error:

1. Initialise-to-1 with an obstacle.
2. Zero base cases in minimum path sum.
3. A blocked cell marked `0` in the cost version.
4. The one-row trick on minimum falling path.
5. Returning `dp[-1][-1]` from maximal square.
6. `math.comb(m+n, m)` instead of `(m+n-2, m-1)`.
7. An empty grid.

Six of the seven give no error at all. Name them.

---

### The shape drill

1. Say how messaging differs from a social feed, in three points.
2. Give the messages-per-second and the bandwidth, and the comparison with Instagram.
3. Say what the system is actually bounded by.

### The connection drill

1. Say why polling is wrong, with the numbers.
2. Say what the registry holds and why it is a hash.
3. Say why it needs a TTL.
4. Give the memory per connection and the fleet total.
5. Say what statefulness costs at deploy time and what clients must do.

### The ticks drill

1. Name the three events and what each actually means.
2. Say which two people conflate and why they are different.
3. Say why persist comes before ack, and what goes wrong otherwise.
4. Say why the sender never retries after a bad ack.

### The offline drill

1. Describe the queue structure and why that structure.
2. Say when a message is removed, and what the alternative loses.
3. Say what delivery guarantee this gives and how the client copes.
4. Say what the expiry is for and what the sender is told.
5. Say how an app that is not running at all gets woken.

### The ordering drill

1. Say what ordering is required and what is not.
2. Give the example that shows why within-conversation matters.
3. Say what a sequence gap lets the client do.
4. Say what global ordering would cost and buy.

### The encryption drill

1. Name the four capabilities it removes.
2. For each, say where the capability goes instead.
3. Say what spam filtering can still use.
4. Say why multi-device is hard.
5. Do the group encryption arithmetic and give the fix.

### The groups drill

1. Say what the cap is and what it removes.
2. Compare with Twitter's follower problem in one sentence.
3. Say what happens to keys when someone leaves, and when someone joins.
4. Say what you would do if the product wanted million-member channels.

### The storage drill

1. Compute store-forever and store-until-delivered.
2. Say what the ratio is and what it costs the user.
3. Say where the actual storage is, and what makes forwarding free.

### The presence drill

1. Compute the naive event rate and fan-out.
2. Compare it with the message traffic.
3. Give the mitigation and the resulting number.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many unique paths are there through the grid?*
   The state, why addition is correct, the base cases, the one-row collapse with what each value is, and the
   closed form with its limitation.

2. *Now some cells are blocked, and each cell has a cost.*
   What changes in the recurrence, what changes in the base cases, why a blocked cell is `0` in one version
   and `inf` in the other, and why the formula dies.

3. *Design WhatsApp.*
   Why it is a different shape, WebSockets and the registry, the three ticks with persist-before-ack, the
   offline queue with removal-after-ack, and the four things encryption removes.

---

## Before you move on

- [ ] I can state the grid DP state in one sentence.
- [ ] I know why addition counts each path exactly once.
- [ ] I can give the base cases for all four variants.
- [ ] I know the initialise-to-1 trick and exactly when it breaks.
- [ ] I can write the one-row version and point at both values.
- [ ] I can state the precondition for the collapse.
- [ ] I know which variant violates it and what it needs.
- [ ] I know a blocked cell is `0` when counting and `inf` when costing.
- [ ] I can derive the closed form and check it on a 2×2 grid.
- [ ] I know why one obstacle destroys the formula.
- [ ] I know which approach handles a modulus more easily.
- [ ] I know maximal square's answer is the table maximum.
- [ ] I can reconstruct a path and know it needs the full table.
- [ ] I can give the space numbers at 1,000² and 10,000².
- [ ] I know the counts overflow a 64-bit integer by 40×40.
- [ ] I can say how messaging differs from a feed, in three points.
- [ ] I know the bandwidth comparison and what really bounds the system.
- [ ] I can explain why polling is wrong, with numbers.
- [ ] I know what the registry holds and why it needs a TTL.
- [ ] I can give per-connection memory and the fleet total.
- [ ] I know the three tick events and why delivered ≠ read.
- [ ] I know persist comes before ack, and what breaks otherwise.
- [ ] I can describe the offline queue and when messages are removed.
- [ ] I know this gives at-least-once and how the client copes.
- [ ] I know ordering is per conversation, and why.
- [ ] I can name the four capabilities encryption removes.
- [ ] I know spam filtering falls back to metadata.
- [ ] I can do the group encryption arithmetic and name the fix.
- [ ] I know the group cap deletes the fan-out problem.
- [ ] I can give both storage numbers and the ratio.
- [ ] I know presence is bigger than messaging without its mitigation.
- [ ] I answered all three questions above out loud.
