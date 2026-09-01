---
day: 157
track: practice
title: "Practice — DP on decisions: buy and sell stock"
status: written
---

# Day 157 · Practice

**DSA topic:** DP on decisions: buy and sell stock
**System design topic:** Design a chat system with presence

---

## Code these, in this order

One rule for the whole set: **before writing anything, say the state out loud including the mode.** "Day, and
whether I am holding" — then say which variant changes it. Five of these six are the same machine with one
edit, and treating them as six separate problems is how people fall off the ladder.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Best Time to Buy and Sell Stock | LeetCode 121 (Easy) | Greedy: min-so-far and best difference. |
| 2 | Best Time to Buy and Sell Stock II | LeetCode 122 (Medium) | The two-state machine, and why greedy also works. |
| 3 | Best Time to Buy and Sell Stock with Cooldown | LeetCode 309 (Medium) | A third state, and saving yesterday's values. |
| 4 | Best Time to Buy and Sell Stock with Transaction Fee | LeetCode 714 (Medium) | One constant, no new state. |
| 5 | Best Time to Buy and Sell Stock III | LeetCode 123 (Hard) | `k = 2`, and where the transaction is consumed. |
| 6 | Best Time to Buy and Sell Stock IV | LeetCode 188 (Hard) | General `k`, and the `k ≥ n/2` shortcut. |

### On problem 2, write both solutions and compare

Write the two-variable state machine and the one-line greedy sum of positive differences. Confirm they agree on
twenty random price series. **Then say why the greedy one works**, using the word "telescope".

### On problem 2, try the greedy on a limited version

Run your greedy on `[3,3,5,0,0,3,1,4]` and record the answer. Then run problems 5 and 6 with `k = 2` and
`k = 1` on the same input and record those. **Three different numbers. Say what greedy is ignoring.**

### On problem 3, read the fresh value on purpose

Write the cooldown version without saving yesterday's `free` and `holding`. Run it on `[1, 2, 3, 0, 2]` and
record the answer against the correct one. **Say precisely what the bug allows you to do**, in terms of days.

### On problem 4, charge the fee twice

Subtract it on both the buy and the sell. Run on `[1, 3, 7, 5, 10, 3]` with a fee of 3 and record the answer.
**Say why the wrong answer reads like "the fee is high" rather than like a bug.**

### On problem 5, count the transaction on both halves

Write `buy[t]` from `sell[t-1]` and `sell[t]` from `buy[t-1]`. Run with `k = 2` on `[3,3,5,0,0,3,1,4]` and
record the answer. **Say which correct question you have accidentally answered.**

### On problem 6, remove the shortcut

Delete the `k >= n // 2` check and call it with `k = 1_000_000_000`. Record the exact error. **Then say why
`n/2` is the right threshold**, in one sentence about how many days a transaction needs.

### On problem 6, measure the space

Write the full `n × k × 2` table version and the two-array version. Measure both at `n = 100_000`, `k = 100`.
Record both figures and the ratio.

### Then the ladder drill

Starting from the two-state machine, write each of the other four variants without looking at your earlier
code. Time yourself. **The target is about two minutes each**, because each is one edit.

---

### The state drill

1. State it as a sentence, including the word "mode".
2. Say why "best profit in the first `n` days" is incomplete.
3. Say what goes wrong, and whether anything reports it.
4. Say why you track money rather than profit.

### The transitions drill

1. Give both transitions with their meanings in words.
2. Give both base cases.
3. Say why the answer is the not-holding state.
4. Say what the answer becomes in the cooldown version, and why.

### The greedy drill

1. Name the two variants greedy solves.
2. Give the one-transaction algorithm in two lines.
3. Give the unlimited algorithm in one line and justify it.
4. Say precisely why a transaction limit breaks it.
5. Give the three numbers on `[3,3,5,0,0,3,1,4]`.

### The k-transactions drill

1. Say what dimension is added.
2. Say where the transaction is consumed and why it must be stated.
3. Say what counting on both halves does, and what the answer looks like.
4. Give the shortcut and say why `n/2`.
5. Give the exact error without it.
6. Give the time and space, and the full-table comparison.

### The cooldown drill

1. Name the three states and what each means.
2. Give all three transitions.
3. Say why `holding` reads `free` and not `cooling`.
4. Say why yesterday's values must be saved.
5. Say why the answer is a max of two states.
6. Say why adding a state costs nothing and adding a dimension costs a lot.

### The break-it drill

Trigger each and record the exact output or error:

1. Counting the transaction on both halves.
2. `k = 10^9` without the shortcut.
3. Reading fresh values in the cooldown version.
4. The fee charged on both halves.
5. Greedy on a limited-transaction input.
6. An empty price list.
7. Returning `max` of both states in the plain version.

Five of the seven give no error at all. Name them.

---

### The contrast drill

1. Give the five ways this differs from a WhatsApp-style design.
2. Say which parts of the transport are unchanged.
3. Say what keeping history costs, with numbers, and what it buys.

### The storage drill

1. Give the partition key and the clustering key, and say why each.
2. Say what "the last fifty" costs.
3. Explain why the time bucket exists, with the partition-size arithmetic.
4. Say what scrollback costs as a result.
5. Say why the message id should be a Snowflake.

### The fan-out drill

1. Describe the naive path and count its operations.
2. Describe the pub/sub path and count its operations.
3. Say what each connection server subscribes to, and the mistake to avoid.
4. Say what happens for offline members, and what you deliberately do not build.
5. Say what a bus partition means and what clients must do.

### The presence drill

1. Do the naive arithmetic from concurrent users to pushes per second.
2. Compare it with the message traffic.
3. Give both mitigations and the resulting number.
4. Say why presence must be an expiring key.
5. Name three cases that never send a disconnect.
6. Say what the TTL is a dial between.
7. Say why approximate presence is correct rather than a limitation.

### The typing drill

1. Give the mechanism and the TTL.
2. Explain the `SET NX` throttle in one sentence.
3. Say why typing is never persisted.

### The unread drill

1. Give the field and say what it replaces.
2. Compute the write amplification of the alternative.
3. Say how the count is produced.
4. Say why it is computed lazily, with the arithmetic.

### The search drill

1. Say why indexing is asynchronous and what the alternative costs.
2. Say why it shards by time.
3. Give the wrong way to handle permissions.
4. Say exactly what it leaks, and why counts are the problem.
5. Give the right way.
6. Name two things that must invalidate or update the index.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Buy and sell stock to maximise profit.*
   The state including the mode, why the naive state is incomplete, both transitions, the base cases, the
   answer, and which variants greedy solves.

2. *Now at most `k` transactions, and then with a cooldown.*
   The added dimension, where the transaction is consumed and what happens if you get it wrong, the `k ≥ n/2`
   shortcut, the three cooldown states, and why saving yesterday's values matters.

3. *Design Slack, and tell me how presence works.*
   The three inversions from WhatsApp, the bucketed partition key, pub/sub fan-out, the naive presence
   arithmetic and both mitigations, and expiring keys with no offline event.

---

## Before you move on

- [ ] I can state the stock DP state including the word "mode".
- [ ] I know why "best profit so far" is an incomplete state.
- [ ] I track money, not profit, and know why.
- [ ] I can write both transitions with their meanings.
- [ ] I know the answer is the not-holding state, and why.
- [ ] I know greedy solves one-transaction and unlimited, and only those.
- [ ] I can justify the unlimited greedy with the telescoping argument.
- [ ] I can give the three numbers that show greedy ignoring `k`.
- [ ] I know where the transaction is consumed and say it out loud.
- [ ] I know what counting on both halves does to the answer.
- [ ] I know the `k ≥ n/2` shortcut is required, not an optimisation.
- [ ] I can say why `n/2` is the threshold.
- [ ] I can name the three cooldown states and all three transitions.
- [ ] I know why yesterday's values must be saved.
- [ ] I know the cooldown answer is a max over two states.
- [ ] I know a fee adds no state at all.
- [ ] I know adding a state is free and adding a dimension is not.
- [ ] I can give the space comparison at `n = 100,000`, `k = 100`.
- [ ] I can list the ways a channel chat differs from WhatsApp.
- [ ] I can give the partition key and justify the time bucket.
- [ ] I know the partition-size arithmetic that forces bucketing.
- [ ] I can describe pub/sub fan-out and count both paths.
- [ ] I know servers subscribe per channel, not per client.
- [ ] I know unread is one field, and the write amplification it avoids.
- [ ] I can do the naive presence arithmetic and the comparison.
- [ ] I can give both presence mitigations and the resulting number.
- [ ] I know presence must be an expiring key with no offline event.
- [ ] I can name three cases that never send a disconnect.
- [ ] I know why permission filters go in the query, and what a post-filter leaks.
- [ ] I answered all three questions above out loud.
