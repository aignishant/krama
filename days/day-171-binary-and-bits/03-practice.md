---
day: 171
track: practice
title: "Practice — Binary, bits, and monitoring"
status: written
---

# Day 171 · Practice

**DSA topic:** Binary, bits, and why they matter
**System design topic:** Monitoring, metrics, and alerting

---

## Code these, in this order

One rule for the whole set: **write out the bit pattern before you write the expression.** Eight characters of
bit manipulation is three ideas stacked on top of each other, and reading it back afterwards will not tell you
whether it is right. **Say the pattern, then write the code that produces it.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of 1 Bits | LeetCode 191 (Easy) | The naive loop, then `n & (n-1)`. |
| 2 | Power of Two | LeetCode 231 (Easy) | The one-liner, and the guard everyone omits. |
| 3 | Counting Bits | LeetCode 338 (Easy) | Bits meeting DP — the recurrence is one line. |
| 4 | Reverse Bits | LeetCode 190 (Easy) | Fixed width, and why Python needs to be told it. |
| 5 | Sum of Two Integers | LeetCode 371 (Medium) | Addition from AND, XOR and shift — and Python's traps. |
| 6 | Bitwise AND of Numbers Range | LeetCode 201 (Medium) | The common prefix, and why the answer is a shift. |

### On problem 1, count the iterations

Instrument both versions. Run them on `1024`, `255` and `1 << 31` and **record the iteration counts in a small
table.** Say which input makes them equal and why.

### On problem 2, remove the guard

Delete `number > 0` and run on `0` and `-8`. **Record both answers.** Say what `0 & -1` is and why that is the
whole bug.

### On problem 3, find the one-line recurrence

`bits[i]` can be built from a smaller answer. **Find two different ways** — one using `i >> 1`, one using
`i & (i - 1)` — and say what each one is really saying about the number.

### On problem 4, discover why Python is awkward

Write the obvious loop. **Run it and see what happens with leading zeros.** Then say what "32-bit" means here
and write the version that respects it. **Record what `bin(x)[2:]` gives you for a small number** and why that
is the problem.

### On problem 5, meet the arbitrary-width trap

Implement addition with XOR for the sum and AND-shifted for the carry. **Run it on two positives** — it works.
**Then run it on a negative** and say what happens. Then fix it with a mask, and **say out loud what the mask
is standing in for.**

### On problem 6, do it by hand first

Take `[5, 7]` and write out `101`, `110`, `111`. **Say what survives the AND and why.** Then say what that has
to do with the common prefix, and only then write the shifting solution.

### Then the conversion drill

Convert `37`, `100` and `255` to binary by hand, saying "upwards" out loud each time. **Then convert them back
using double-and-add.** Check against `bin()`. Then deliberately read one set of remainders downwards and
record the wrong number you get.

### Then the precedence drill

Write `mask = 1 << n - 1` for `n = 4` and record its value against `(1 << n) - 1`. **Say which one you meant.**
Then find every unbracketed shift in code you have written today.

### Then the negative-shift drill

Run `while n: n >>= 1` on `-5`. **Do not let it run long.** Say what `-1 >> 5` is, why the loop never ends, and
why hanging is worse than crashing.

---

### The place-value drill

1. Give the binary places up to 64.
2. Convert 13 both ways and state the direction rule.
3. Say what `n` bits gives you, in values and in range.
4. Give `2^10`, `2^20`, `2^30` and their rough decimal names.
5. Say why the machine uses two and not ten.

### The operators drill

1. Give all six with a one-sentence meaning each.
2. Say what XOR is the same as.
3. Say what shifting left does and why, from place value.
4. Say why right shift rounds down, and what the rounding is.
5. Give `1 << k` in words.

### The edits drill

1. Give all four one-liners from memory.
2. Say what they have in common.
3. Say which operator forces on, which forces off, which flips.
4. Say what `~(1 << p)` is in Python and why it still works.

### The tricks drill

1. Say what `n & (n - 1)` does and why, in terms of borrowing.
2. Give the two things that fall out of it.
3. Give the iteration counts for `1024` and `255`, both methods.
4. Say what `n & -n` gives.
5. Say why hash tables use power-of-two sizes, with the cycle counts.
6. Say what that costs, and what Java does about it.

### The negatives drill

1. Give the two's complement rule.
2. Work `-5` in eight bits and check it sums to zero.
3. Say why this scheme was chosen over a sign bit.
4. Give the range in eight bits and say why it is asymmetric.
5. Say what `~x` is in Python and what to do about it.
6. Say what `-1 >> 5` is and what loop that breaks.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Reading the remainders downwards.
2. `1 << n - 1` when you meant a mask.
3. `int('1101')` without the base.
4. `bin(-5)[2:]`.
5. `is_power_of_two(0)` without the guard.
6. `while n: n >>= 1` on a negative.
7. `1 << 2.0` after a `/` division.

---

### The pillars drill

1. Name all three, what each answers, and what each cannot.
2. Give the workflow as a sequence.
3. Give the relative cost of each at 100M requests/day.
4. Say what field ties them together.

### The signals drill

1. Name the four golden signals.
2. Say what must be split, and why.
3. Say which is the leading indicator.
4. Give RED and USE and say how they relate.

### The percentiles drill

1. Give the 950/50 example and compute the average.
2. Say what is wrong with that number in one sentence.
3. Give p50 and p99 for it.
4. Compute the tail compounding at 20 and 100 calls.
5. Give the two-machine example and say why averaging p99s fails.
6. Give the fix and name the metric type that supports it.
7. Say which metric types aggregate and which do not.

### The alerting drill

1. Give the three tests every page must pass.
2. Give four things that page and four that do not.
3. Say what `for: 5m` buys and costs.
4. Say why an alert must be a ratio.
5. Say what belongs in a runbook, including the line people forget.
6. Give the alert-to-incident ratio rule.
7. Say what direction the fix always goes in.

### The budget drill

1. Define SLI, SLO and SLA and say which is loosest.
2. Give downtime per month at four availability levels.
3. Say what the budget is for and how you spend it.
4. Say what changes in the design at five nines.
5. Say why 100% is not a target.

### The cardinality drill

1. Compute the base series count from the four labels.
2. Compute it again with `user_id`.
3. Give the storage in GB/day for the base case.
4. Name five things that must never be a label.
5. Say where those belong instead.
6. Say what else must not share a failure domain, and why.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is 13 in binary, and what does shifting left by one do?*
   Place value, both conversion rules with the direction said aloud, why shifting doubles, and the Python
   width caveat.

2. *Count the set bits. Now do it faster.*
   The naive loop with its iteration count, `n & (n-1)` with the borrowing explanation, the worst case where
   they tie, and the power-of-two test that falls out.

3. *What would you put on the dashboard, and what would page you?*
   The four golden signals, percentiles over averages with the arithmetic, symptoms over causes, the three
   tests for a page, and the cardinality rule.

---

## Before you move on

- [ ] I can convert to binary by hand and I say "upwards" out loud.
- [ ] I know what reading the remainders downwards gives, and that nothing errors.
- [ ] I can convert back with double-and-add without powers.
- [ ] I know the powers of two to 2^10, and 2^20 and 2^30 by their rough names.
- [ ] I can give all six operators with one sentence each.
- [ ] I know XOR is "exactly one", which is "different".
- [ ] I can explain why shifting left doubles, from place value.
- [ ] I know right shift rounds down and what the rounding is.
- [ ] I can write all four bit edits from memory.
- [ ] I know what they have in common.
- [ ] I can explain `n & (n - 1)` in terms of borrowing.
- [ ] I know the iteration counts for `1024` and `255`, both methods.
- [ ] I know the power-of-two test and why the guard is not decoration.
- [ ] I know why hash tables use power-of-two sizes, with the cycle counts.
- [ ] I can do two's complement by hand and check it sums to zero.
- [ ] I know why that scheme beat a sign bit.
- [ ] I know `~x == -x - 1` in Python and how to get a real pattern.
- [ ] I know `-1 >> 5` is `-1` and which loop that hangs.
- [ ] I always bracket shifts.
- [ ] I know `int(s, 2)` needs the base.
- [ ] I can name the three pillars and what each answers.
- [ ] I know the workflow is detect, localise, diagnose.
- [ ] I can name the four golden signals and which is leading.
- [ ] I can give the 950/50 example and say why the average describes nobody.
- [ ] I can compute the tail compounding at 20 and 100 calls.
- [ ] I know why percentiles cannot be averaged, and the fix.
- [ ] I know which metric types aggregate and which do not.
- [ ] I can give the three tests every page must pass.
- [ ] I can name four things that page and four that do not.
- [ ] I know what `for: 5m` buys and why alerts must be ratios.
- [ ] I know what belongs in a runbook, including the `DO NOT` line.
- [ ] I can define SLI, SLO and SLA and give the monthly budgets.
- [ ] I know what changes in the design at five nines.
- [ ] I can compute the cardinality explosion and name what is never a label.
- [ ] I know monitoring must not share a failure domain with the product.
- [ ] I answered all three questions above out loud.
