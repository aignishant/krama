---
day: 164
track: practice
title: "Practice — Greedy: when taking the best option now is safe"
status: written
---

# Day 164 · Practice

**DSA topic:** Greedy: when taking the best option now is safe
**System design topic:** Design a payment system

---

## Code these, in this order

One rule for the whole set: **before writing anything, spend thirty seconds trying to break greedy.** Write
down what you tried and whether you found a counter-example. **Only then choose the algorithm.** Three of these
six are greedy and three are not, and the diagnosis is the exercise.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Assign Cookies | LeetCode 455 (Easy) | The simplest correct greedy, and its exchange argument. |
| 2 | Non-overlapping Intervals | LeetCode 435 (Medium) | Sort by end time, and why not by start. |
| 3 | Maximum Subarray | LeetCode 53 (Medium) | Greedy and DP are the same algorithm here. |
| 4 | Partition Labels | LeetCode 763 (Medium) | A greedy whose rule is not a sort. |
| 5 | Coin Change | LeetCode 322 (Medium) | Greedy fails — construct the counter-example first. |
| 6 | Best Time to Buy and Sell Stock IV | LeetCode 188 (Hard) | Greedy fails as soon as the limit binds. |

### On all six, write the diagnosis first

For each, record: **the greedy rule you would try, whether you found a counter-example in thirty seconds, and
what you chose as a result.** Then solve it. **Then check whether your diagnosis was right.**

### On problem 2, run all three sort keys

Implement sorting by end time, by start time and by duration. Run all three on the same input and record the
three answers. **Find an input where by-duration is right and one where it is wrong**, and say why that makes
it the more dangerous rule.

### On problem 3, notice they coincide

Write the greedy version — running sum, reset when negative — and the DP version — `dp[i]` = the best subarray
ending at `i`. **Say in one sentence why they are the same algorithm**, and which one you would explain in an
interview.

### On problem 4, find the rule

The greedy here is not "sort by something". Work out what the rule is before coding. **Then state the exchange
argument in one sentence**: why is extending the current partition to the last occurrence always safe?

### On problem 5, break it before solving it

Do not write any code until you have a written counter-example with specific coins and a specific amount.
**Then say what property of the coin set makes greedy work when it does**, and name a real currency where it
holds.

### On problem 6, find where greedy stops working

Write the greedy for unlimited transactions — sum the positive differences. Run it with `k = 1`, `k = 2` and
unlimited on `[3,3,5,0,0,3,1,4]` and record all three. **Say what greedy is ignoring.**

### Then the counter-example drill

For each, spend thirty seconds and record what you find:

1. Activity selection, sorted by end time.
2. Activity selection, sorted by start time.
3. Fractional knapsack by value per kilo.
4. 0/1 knapsack by value per kilo.
5. Huffman: merge the two least frequent.
6. Huffman: merge the two most frequent.
7. Shortest job first, to minimise total waiting.
8. Longest job first, to minimise total waiting.

**Four break and four hold.** For each of the four that hold, write the exchange argument in one sentence.

### Then the verification drill

Take problem 2 and write a brute-force version for `n ≤ 12`. Check your greedy against it on two thousand
random inputs. **Time how long the brute force took to write** — it should be about five minutes — and say what
it would have cost you to be wrong instead.

---

### The definition drill

1. Define greedy in one sentence.
2. Name the two properties it needs.
3. Say which one it shares with DP and which one it adds.
4. Give the exact phrasing of the greedy choice property, and say why "an" rather than "the" matters.

### The counter-example drill

1. Say where in an input to look for a counter-example.
2. Give all three from the lesson, with their numbers.
3. Say how long each one is.
4. State the asymmetry between finding one and not finding one.
5. Say what you do when you cannot find one and cannot argue.

### The exchange-argument drill

1. State it generally, in two sentences.
2. Give it for activity selection.
3. Give it for shortest job first.
4. Say what "greedy stays ahead" is, and how it differs.

### The four-that-work drill

For each of activity selection, fractional knapsack, Huffman and MST:

1. What is sorted, or what is the rule?
2. What is the one-sentence reason it is safe?
3. What is the complexity, and what dominates it?

### The near-misses drill

1. Say when coin change greedy works and why the intuition is misleading.
2. Give the two wrong sort keys for interval scheduling.
3. Say which of them often gives the right answer, and why that is worse.
4. Say what one word in a problem statement turns greedy into DP.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Greedy used where a counter-example exists.
2. DP used where greedy is provably correct.
3. Sorting by start time instead of end time.
4. Sorting by duration.
5. The ratio rule applied to 0/1 knapsack.
6. No sort at all.
7. Mutating the caller's list with `.sort()`.

---

### The scope drill

1. Give your in and out lists.
2. Say what you establish about card handling in the first minute, and why.
3. Give the scale and say what it implies about the technology choice.

### The ledger drill

1. Describe double-entry in two sentences.
2. Give the three properties that follow from it.
3. Say why the balance is derived and what a snapshot is.
4. Say why the ledger is append-only, and how a mistake is corrected.
5. Give the two rules about representing money, with the reason for each.
6. Say why the currency exponent is not always two, with examples.

### The idempotency drill

1. State the problem in one sentence.
2. Say where the key comes from and what the near-miss mistake is.
3. Say what the key maps to.
4. Describe the concurrent-retry race and the fix.
5. Say what the retention should be and why.

### The timeout drill

1. Say what state a timed-out payment goes into, and what it must not go into.
2. Say why that single line is the most common bug.
3. Name the three resolving mechanisms.
4. Say which one is authoritative and why.
5. Say what must be verified on the webhook, and what happens without it.
6. Say what happens if the webhook arrives before your own response.

### The lifecycle drill

1. Name the four operations.
2. Say what happens in the gap between two of them.
3. Give the void-versus-refund asymmetry, with the annual figure.
4. Say what expires and what that forces.

### The reconciliation drill

1. Say what double-entry cannot catch.
2. Describe the daily job.
3. Give the four categories and the response to each.
4. Say which one is alarming.
5. Say what a zero-discrepancy run means.
6. Give the metric you would actually track.

### The honesty drill

1. Say what consistency you can offer, precisely.
2. Say what "exactly-once delivery" actually means when someone claims it.
3. Compare infrastructure cost with fees, and say what follows.
4. Say what you would never build, and what you would build anyway.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can you solve this greedily?*
   The two properties, the thirty-second counter-example search with a real example, the asymmetry, and what
   you do when you cannot find one.

2. *Why does sorting by end time work?*
   The intuition, the exchange argument as a swap, why start time and duration both fail, and the one word
   that turns it into DP.

3. *Design a payment system.*
   Card handling and scale, double-entry with its three properties, the timeout going to `unknown` with the
   three resolving mechanisms, and daily reconciliation with its four categories.

---

## Before you move on

- [ ] I can define greedy and name both properties it needs.
- [ ] I know which property it shares with DP and which it adds.
- [ ] I know why "an optimal solution" rather than "the" matters.
- [ ] I spend thirty seconds trying to break greedy, every time.
- [ ] I know where in an input to look for a counter-example.
- [ ] I can give all three counter-examples with their numbers.
- [ ] I know a counter-example proves failure and none proves nothing.
- [ ] I know what to do when I can neither break it nor argue it.
- [ ] I can state the exchange argument generally.
- [ ] I can give it for activity selection and for shortest job first.
- [ ] I know the four provably-correct greedies and their sort keys.
- [ ] I know why fractional knapsack works and 0/1 does not.
- [ ] I know coin change greedy works only for canonical systems.
- [ ] I know both wrong sort keys for interval scheduling.
- [ ] I know which wrong key is more dangerous, and why.
- [ ] I know "maximum number" versus "maximum value" changes everything.
- [ ] I know greedy is `O(n log n)` dominated by the sort.
- [ ] I have the brute-force verification habit.
- [ ] I would say I do not handle card numbers, in the first minute.
- [ ] I can describe double-entry and its three properties.
- [ ] I know the balance is derived and the snapshot is a cache.
- [ ] I know the ledger is append-only and how corrections work.
- [ ] I store money as integers, and know the exponent is not always two.
- [ ] I know a timeout goes to `unknown`, never `failed`.
- [ ] I know where the idempotency key comes from and the near-miss mistake.
- [ ] I know the insert must be the lock, not a check-then-write.
- [ ] I can name the three mechanisms that resolve an unknown.
- [ ] I know the provider is the source of truth after a timeout.
- [ ] I know why webhooks need signature verification and dedup.
- [ ] I can give the void-versus-refund asymmetry in money.
- [ ] I know reconciliation always finds something, and what it means if it does not.
- [ ] I answered all three questions above out loud.
