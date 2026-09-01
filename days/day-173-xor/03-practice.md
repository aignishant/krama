---
day: 173
track: practice
title: "Practice — XOR, SLOs and error budgets"
status: written
---

# Day 173 · Practice

**DSA topic:** XOR problems
**System design topic:** SLAs, SLOs, and error budgets

---

## Code these, in this order

One rule for the whole set: **before you write the loop, say what cancels.** "Pairs cancel." "Everything
present appears twice." **If nothing cancels, XOR is the wrong tool and you should stop looking for a clever
line.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Single Number | LeetCode 136 (Easy) | Pairs cancel, and that the constraint named the technique. |
| 2 | Missing Number | LeetCode 268 (Easy) | Supplying the partners yourself, and why XOR beats the sum. |
| 3 | Single Number III | LeetCode 260 (Medium) | The split bit. This is the one that separates people. |
| 4 | Single Number II | LeetCode 137 (Medium) | Counting modulo three, and Python's sign problem. |
| 5 | Set Mismatch | LeetCode 645 (Easy) | One doubled, one missing — the split trick again, in disguise. |
| 6 | Maximum XOR of Two Numbers in an Array | LeetCode 421 (Medium) | Greedy from the top bit, with a set lookup instead of a second loop. |

### On problem 1, distrust it first

Trace `[4, 1, 2, 1, 2]` by hand and **write down every intermediate value.** Notice that 5, 7 and 6 mean
nothing. **Then say the rearrangement argument out loud** — that is what turns the trick into a proof.

### On problem 2, do it three ways

XOR, the sum formula, and a set. **Say the space cost of each.** Then say what happens to the sum formula at
`n = 100,000` in a language with 32-bit integers, and why XOR is immune.

### On problem 3, find the split bit by hand

Take `[1, 2, 1, 3, 2, 5]`. **XOR everything and write out the bit pattern.** Then say what a set bit in that
number means. Pick it, split the list into two piles on it by hand, **and check that both copies of every
duplicate landed in the same pile.** Only then write the code.

### On problem 3 again, break the precondition

Run your solution on `[1, 1, 2, 2]` — a list with no loners at all. **Record what comes back.** Say why, in
terms of what `both` and `split` become.

### On problem 4, meet Python's sign

Write the column-counting version without the final correction. **Run it on `[2, 2, -3, 2]` and record the
number.** Say why it is 4,294,967,293 and not −3, and what one line fixes it. Then say why that line does not
exist in the Java version.

### On problem 6, do the small case by hand

Take `[3, 10, 5, 25, 2, 8]`. **Work out the answer by trying all fifteen pairs.** Then work it out again the
greedy way, top bit first, and check you reached the same 28. **Say why greedy is safe here** — the reason is
one sentence about place value.

### Then the three-facts drill

Say all three facts. **Then use them to explain, in one sentence each, why the one-loner solution works and
why `both ^ first` gives you the second answer without another pass.**

### Then the repeat-count drill

Run plain XOR on `[2,2,3]`, `[2,2,2,3]`, `[2,2,2,2,3]` and `[1,1,1,3]`. **Record all four answers.** Say which
are right, which are wrong, and what rule decides it. Then say why this is a dangerous bug rather than an
obvious one.

### Then the range drill

Write out the XOR of `0..n` for `n` from 0 to 11. **Find the period yourself.** State the four cases. Then
compute `xor_range(3, 9)` two ways and check they agree. Finally run `xor_to(-1)` and say why it returns
something rather than complaining.

### Then the nines drill

From 43,200 minutes, compute the monthly downtime for 99%, 99.9%, 99.99% and 99.999% **without looking at the
table.** Then say what changes about the design at the last one, and why.

### Then the budget drill

Take 100 million requests a day. **Compute the monthly budget in failed requests at 99.9 percent.** Then
compute what a 20-minute outage costs, as a fraction of it. Then say what your policy does at that point.

### Then the dependency drill

Six dependencies, each 99.9 percent, all required. **Compute your ceiling and convert it to minutes.** Then
compute two independent replicas at 99 percent each. **Say which multiplication applies to which arrangement**,
and what the word "independent" is hiding.

---

### The facts drill

1. Give the three facts of XOR.
2. Say which one makes the list order irrelevant.
3. Say why starting the accumulator at zero is correct.
4. Say what XOR is asking, per column.

### The family drill

1. One loner: the code and the proof, in two sentences.
2. One missing: what you XOR against, and the seeding detail.
3. Two loners: why the plain XOR is not enough, and what the split bit means.
4. Three times each: what replaces cancelling, and the general rule.
5. Say what all four have in common.

### The split-bit drill

1. Say what a set bit in `a ^ b` tells you.
2. Give the expression that isolates one, and why that one.
3. Say why duplicates cannot be separated by the split.
4. Say why the loners must be separated by it.
5. Give the second answer without a third pass, and why that works.

### The range and prefix drill

1. Give the four cases of `xor_to(n)`.
2. Say how you would rediscover them in twenty seconds.
3. Give `xor_range(low, high)` and why the lower part cancels.
4. Give the subarray XOR formula from a prefix table.
5. Say what `prefix[i] == prefix[k]` means about the stretch between them.

### The terms drill

1. Define SLI, SLO and SLA in one sentence each.
2. Say which is looser and why the gap exists.
3. Say what the window is for, and why 28 days.
4. Say what an SLA's consequence actually is, and what it is not.
5. Name the exclusion clause that matters most, and why.

### The nines drill

1. Give downtime per month at five availability levels.
2. Say which row changes the architecture rather than the budget, and why.
3. Give the rough cost multiplier per nine.
4. Give the three reasons 100 percent is the wrong target.

### The budget drill

1. Define the error budget from an SLO.
2. Give it in minutes and in requests for a stated scale.
3. Name four things you spend it on.
4. Give the three-band policy and what happens in each.
5. Say why the policy needs a written override.
6. Say what an unspent budget means.

### The burn-rate drill

1. Give the formula.
2. Give how long the budget lasts at 1 percent and 10 percent errors.
3. Give the two standard alerts with their windows.
4. Say where 14.4 comes from.
5. Say what each alert is for, and why one alert cannot do both.

### The arithmetic drill

1. Say what happens to availability in series, and compute six at 99.9 percent.
2. Say what happens in parallel, and compute two at 99 percent.
3. Give the sentence that separates the two cases.
4. Say what "independent" is hiding, with two concrete examples.
5. Say what a twenty-hop path implies, and which design debate that feeds.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Plain XOR on a list where every value appears three times.
2. `missing_number` without seeding the accumulator with `len(numbers)`.
3. The two-loner solution on a list with no loners.
4. The modulo-three solution on a negative input, in Python.
5. `xor_to(-1)`.
6. `answer ^= "3"`.
7. An SLI measured only at the load balancer, during a DNS failure.
8. An SLA and an SLO set to the same number.
9. An error budget policy with no consequence attached.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Every number appears twice except one. Find it, in O(1) space.*
   Why the constraint names the technique, the three facts, the rearrangement proof, the meaningless
   intermediate values, and the column view.

2. *Now two numbers appear once.*
   Why `a ^ b` is not enough, what a set bit in it means, `both & -both`, why duplicates stay together and
   loners split, and `both ^ first` for the second answer.

3. *What does three nines mean in minutes per month?*
   The arithmetic from 43,200 minutes, the whole table, the budget in requests, what changes at five nines,
   and why an unspent budget is waste.

---

## Before you move on

- [ ] I can give the three facts of XOR without hesitating.
- [ ] I can prove the one-loner solution by rearrangement, in one sentence.
- [ ] I know the intermediate values are meaningless, and why that unsettles people.
- [ ] I can explain XOR as an odd-count question per column.
- [ ] I can solve missing-number and say why XOR beats the sum formula.
- [ ] I know why the accumulator starts at `len(numbers)`.
- [ ] I can say what a set bit in `a ^ b` means.
- [ ] I can isolate the split bit and say why that one is easiest.
- [ ] I can explain why duplicates stay together and loners separate.
- [ ] I can get the second answer without a third pass.
- [ ] I know what the two-loner code does when the precondition fails.
- [ ] I can count modulo three and state the general `k` rule.
- [ ] I know why Python needs a sign correction there, and Java does not.
- [ ] I can derive the four cases of the range XOR in twenty seconds.
- [ ] I can give the subarray XOR formula and what equal prefixes mean.
- [ ] I know why greedy is safe in the maximum-XOR problem.
- [ ] I know plain XOR silently succeeds when repeat counts happen to be even.
- [ ] I can define SLI, SLO and SLA in one sentence each.
- [ ] I know why the SLA must be looser than the SLO.
- [ ] I can give the downtime table from 43,200 minutes.
- [ ] I know what changes in the design at five nines, and why.
- [ ] I can compute an error budget in failed requests.
- [ ] I can price a 20-minute outage against a monthly budget.
- [ ] I can give the three-band budget policy and why it needs an override.
- [ ] I know why an unspent budget is waste.
- [ ] I can give the burn-rate formula and the two standard alerts.
- [ ] I know where 14.4 comes from.
- [ ] I know series multiplies availabilities and parallel multiplies failure rates.
- [ ] I can compute six dependencies at 99.9 percent and convert it to minutes.
- [ ] I know what "independent" is hiding, with examples.
- [ ] I can give the three reasons 100 percent is the wrong target.
- [ ] I answered all three questions above out loud.
