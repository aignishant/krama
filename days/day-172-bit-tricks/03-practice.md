---
day: 172
track: practice
title: "Practice — Bit tricks, logging and tracing"
status: written
---

# Day 172 · Practice

**DSA topic:** The bit tricks every interview uses
**System design topic:** Logging and distributed tracing

---

## Code these, in this order

One rule for the whole set: **before you write an expression, say the sentence it stands for.** "Clears the
lowest set bit." "Marks every place they differ." **If you cannot say the sentence, you have memorised a
shape rather than learnt a move**, and it will not survive a problem you have not seen.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Hamming Distance | LeetCode 461 (Easy) | That you know XOR means "different". One line. |
| 2 | Counting Bits | LeetCode 338 (Easy) | The one-line recurrence, and why the smaller answer is already there. |
| 3 | Reverse Bits | LeetCode 190 (Easy) | Fixed width, and why Python has to be told what the width is. |
| 4 | Subsets | LeetCode 78 (Medium) | A subset is a number. The iterative bitmask answer, not backtracking. |
| 5 | Single Number | LeetCode 136 (Easy) | Pairs cancel. Warm-up for tomorrow. |
| 6 | Maximum Product of Word Lengths | LeetCode 318 (Medium) | A word as a 26-bit mask, and "no shared letters" as `a & b == 0`. |

### On problem 1, resist the loop

Write it in one line. **Then say out loud why counting the set bits of `a ^ b` is the same as counting the
places where they disagree.** If that sentence does not come easily, the one-liner is memorised, not known.

### On problem 2, find both recurrences

Get it with `bits[i] = bits[i & (i - 1)] + 1`, then again with `bits[i] = bits[i >> 1] + (i & 1)`. **Say what
each one claims about the number**, in a sentence each. Then say why both are valid dynamic programmes — the
argument is the same three words for both.

### On problem 3, break it first

Write the version that loops `while number:` instead of thirty-two times. **Run it on `1` and record what it
gives.** Say why that answer is not wrong so much as an answer to a different question. Then fix it.

### On problem 4, write it twice

Once with backtracking, once with `for mask in range(1 << n)`. **Time both on a twenty-element list.** Then
say which one you would write in an interview and why — and note that the answer is not always the fast one.

### On problem 6, invent the mask

Nobody tells you to use a mask here. **Work out for yourself that a lowercase word is twenty-six yes-or-no
answers**, so it fits in an integer, and that "these two words share no letter" becomes `a & b == 0`. **Say
what that turns an `O(n × m)` character comparison into.**

### Then the two-core-moves drill

Take `176`. Compute `n & (n - 1)` and `n & -n` by hand, writing both bit patterns out. **Say which one removes
and which one keeps.** Then explain each in terms of borrowing or flipping — not by what it produces.

### Then the guard drill

Delete the `number > 0` from the power-of-two test and run it on `0`. **Record the answer.** Say what `0 & -1`
is and why that is the whole bug. Then write the all-ones test and check it agrees with itself on `0`.

### Then the hang drill

Run `count_set_bits(-8)` with the guard removed. **Stop it after two seconds.** Then compute `-8 & -9` and
`-16 & -17` by hand and say why the loop can never reach zero. Say why a hang is worse than a crash.

### Then the submask drill

Enumerate every submask of `1011` by hand, biggest first. **Then write the loop and check you got the same
eight.** Move the test to the top of the loop and record what you lose. Then work out what `(0 - 1) & mask`
is, and why that makes the obvious fix an endless circle.

### Then the logging drill

Take one log line you have written or seen — any one — and rewrite it as structured fields. **Name the four
fields that must be on every line.** Then go through the same line and say what in it must never be logged,
and what you would put there instead.

### Then the trace drill

Take the six-service request from the lesson and say, out loud, **where the trace id is created, how it
reaches the fifth service, and where it is written down.** Then name three places the chain breaks in real
systems.

---

### The core-moves drill

1. Give both expressions and say which removes and which keeps.
2. Explain `n & (n - 1)` in terms of borrowing, without saying what it produces.
3. Explain `n & -n` in terms of two's complement.
4. Say what each one is used for, one use each.

### The masks drill

1. Give the three masks and what each looks like in eight bits.
2. Say what `1 << k - 1` actually is and what you meant.
3. Say what `(1 << width) - 1` does to a negative Python number.
4. Give `x & (size - 1)` and the condition under which it is a remainder.

### The tests drill

1. Give the power-of-two test with its guard and say why the guard exists.
2. Give the all-ones test and say why the carry makes it work.
3. Give the odd test.
4. Say which numbers make all three disagree, and why that is a good check.

### The counting drill

1. Give Kernighan and the iteration count for `1024`, `255` and `1 << 31`.
2. Say when it ties with the naive loop.
3. Say what it does on a negative number in Python, and why.
4. Give both counting-bits recurrences and the reason each is valid.

### The subsets drill

1. Say what a subset is, as a number.
2. Give the two-loop enumeration and the test for "is item i in".
3. Give the cost, and the value of `n` at which it stops being possible.
4. Give the sparse-mask walk and what it saves.
5. Give the submask loop, its shape, and `3^n` against `4^n`.

### The pillars drill

1. Say what a log line is and what a span is.
2. Say what a trace is, in one sentence.
3. Give the sequence: which pillar detects, which localises, which diagnoses.
4. Say which pillar the trace id must never appear in, and why.

### The propagation drill

1. Name the header and the standard.
2. Name the in-process context mechanism in two languages.
3. Give three places propagation breaks.
4. Say what the symptom of a broken chain looks like.

### The numbers drill

1. Compute the daily log volume from 100M requests, 8 services, 3 lines, 300 bytes.
2. Compare it with the daily metrics volume and give the ratio.
3. Price it at fifty cents per gigabyte ingested.
4. Compute unsampled trace volume, then at 1% plus errors.
5. Give the retention-tier saving and what it costs you.

### The hygiene drill

1. Name six things that must never appear in a log line.
2. Say what you log instead, for three of them.
3. Say where redaction belongs and why there.
4. Say why logs are written to standard output rather than sent over the network.
5. Say what a full disk does to a process, and the two settings that prevent it.

### The break-it drill

For each, say what happens and whether anything reports it:

1. `1 << 4 - 1` when you meant a mask of four ones.
2. `is_power_of_two(0)` without the guard.
3. `while n: n &= n - 1` on `-8`.
4. Reversing bits with `while number:` instead of a fixed width.
5. The XOR swap when both positions are the same.
6. `bin(5)[2] & 1`.
7. Head sampling at 1%, when a customer rings with a specific slow request.
8. A background worker picking up a job, with nobody carrying the context across.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Count the number of ones in the binary representation.*
   The naive loop and its iteration count, `n & (n-1)` explained by borrowing, the case where they tie, the
   Python hang on negatives, and `bit_count()` as the production answer.

2. *Generate every subset of this list, and tell me when that stops being possible.*
   A subset is a number, the two-loop enumeration, `n × 2^n` with the figure at `n = 20` and `n = 25`, the
   sparse walk, and the submask loop with `3^n` against `4^n`.

3. *A request took four seconds. How do you find out which service was slow?*
   The trace id minted at the front door, `traceparent` propagation, spans and parent links, reading the
   waterfall for waiting rather than working, then logs filtered by the same id — and the sampling policy that
   means you still have the trace.

---

## Before you move on

- [ ] I can give both core moves and say which removes and which keeps.
- [ ] I can explain `n & (n - 1)` by borrowing, not by its output.
- [ ] I can explain `n & -n` by two's complement.
- [ ] I can write all three masks and I bracket every shift.
- [ ] I know what `1 << k - 1` really is.
- [ ] I can give the power-of-two test and say why the guard is not decoration.
- [ ] I can give the all-ones test and explain the carry.
- [ ] I know Kernighan's iteration counts for `1024`, `255` and `1 << 31`.
- [ ] I know it hangs on a negative in Python, and why a hang is worse than a crash.
- [ ] I can give both counting-bits recurrences and justify each.
- [ ] I know Hamming distance is the set-bit count of the XOR, and why.
- [ ] I can enumerate every subset with two loops and no recursion.
- [ ] I know `n × 2^n` and the value of `n` where bitmasks stop working.
- [ ] I can walk only the set bits of a sparse mask.
- [ ] I can write the submask loop, in the right shape, and say why that shape.
- [ ] I know `3^n` against `4^n` and what it is worth at `n = 16`.
- [ ] I can say what a log line, a span and a trace each are.
- [ ] I know the sequence: metrics detect, traces localise, logs diagnose.
- [ ] I can name the header and the standard that carry the trace id.
- [ ] I can name three places propagation breaks, and the symptom.
- [ ] I can compute 720 GB a day from first principles.
- [ ] I know logs are about eighty times the metrics volume.
- [ ] I can price a logging bill and name the four levers to cut it.
- [ ] I know the trace id must never be a metric label, and why.
- [ ] I can name six things that must never be logged, and what to log instead.
- [ ] I know why services write to standard output rather than over the network.
- [ ] I can describe today's request path out loud, from the front door to the last service.
- [ ] I answered all three questions above out loud.
