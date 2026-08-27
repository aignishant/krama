---
day: 24
track: practice
title: "Practice — Substrings versus subsequences: the distinction they test"
status: written
---

# Day 024 · Practice

**DSA topic:** Substrings versus subsequences: the distinction they test
**System design topic:** API revision and interview questions

---

## Code these, in this order

Four problems chosen so that two are substring problems and two are subsequence problems, and the
words in the titles are the only clue. **Before writing a line of any of them, say out loud which
kind it is and which technique follows.**

Before each one, ask:

1. Contiguous or not? Which word in the statement told me?
2. How many candidates are there — quadratic or exponential?
3. Sliding window, greedy walk, or a table?
4. What does the empty input return?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Is Subsequence | LeetCode 392 (Easy) | The greedy walk, and whether you can say *why* taking the earliest match is never worse. |
| 2 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | A window, and the `last[ch] >= start` guard. `"dvdf"` and `"abba"` are the inputs that expose it. |
| 3 | Longest Common Subsequence | LeetCode 1143 (Medium) | The 2-D table, and why greedy fails here when it worked in problem 1. |
| 4 | Maximum Length of Repeated Subarray | LeetCode 718 (Medium) | The *substring* version of problem 3. One line of the recurrence differs, and the answer is in a different cell. Do these two back to back. |

### Do problems 3 and 4 together, deliberately

They look almost identical and they are not. Solve 3, then solve 4, then put the two recurrences side
by side and answer:

1. Which line differs, and why does contiguity force that?
2. Where is the answer in each — the bottom-right cell, or the maximum anywhere?
3. If someone handed you the problem statement with the word removed, what would you ask?

This pair is the single most valuable half-hour on this page.

### On problem 1, argue before you code

Say out loud why greedy is correct: *if some solution matches this character later in B, replacing it
with the earlier occurrence leaves at least as much of B for everything that follows.* Then write it.
Then test the two empty cases and predict both:

```python
is_subsequence("", "abc")     # ?
is_subsequence("abc", "")     # ?
```

Then delete the `i < len(a)` guard and run `is_subsequence("ab", "abc")`. Read the traceback and say
why Python's short-circuiting `and` was doing real work.

### On problem 2, break the window

Run this version and predict the output on all four inputs first:

```python
def length_of_longest_substring(s):
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last:                     # the guard is missing
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best

for x in ("abcabcbb", "pwwkew", "abba", "dvdf"):
    print(x, length_of_longest_substring(x))
```

Two of those four are wrong. Say which, trace the exact step where `start` moved backwards, and then
state the fix two ways — the `>= start` guard, and `start = max(start, last[ch] + 1)`.

### The counting drill

Without running anything:

1. How many substrings does a string of length 7 have? Length 20?
2. How many subsequences?
3. At what length does the subsequence count pass a million? A billion?
4. `"aaa"` — how many substrings, and how many **distinct** substrings? Why do those differ?
5. Listing every substring of a 1,000-character string — how much memory, roughly, and why is it
   cubic rather than quadratic?

Question 4 is a real interview follow-up. Question 5 is the reason you work with indices.

### The classification drill

For each phrase, say **substring** or **subsequence** in under three seconds, then name the technique:

1. "longest substring with at most two distinct characters"
2. "longest increasing subsequence"
3. "does string A appear inside string B"
4. "minimum window containing all characters of T"
5. "delete some characters from A to make it equal B"
6. "count subarrays whose sum equals k"
7. "longest palindromic substring"
8. "longest palindromic subsequence"
9. "maximum sum of any k consecutive elements"
10. "can you interleave A and B to make C"

Numbers 7 and 8 are the same words apart from one, and they need completely different code. Say what
each needs.

### The enumeration drill

Run this and watch the second column stop being reasonable:

```python
def all_substrings(s):
    return [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]

def all_subsequences(s):
    out = [""]
    for ch in s:
        out += [prev + ch for prev in out]
    return out

for n in (3, 5, 10, 15, 20):
    t = "abcdefghijklmnopqrst"[:n]
    print(n, len(all_substrings(t)), len(all_subsequences(t)))
```

Stop at 20. Then work out on your own what `n = 40` would need, and say why that is not a matter of
waiting longer.

### The API design drill

Design the API for **a ride-hailing app's trip flow**, in fifteen minutes, using the seven steps.
Cover: finding nearby drivers, requesting a ride, cancelling, tracking the driver's position, ending
the trip, paying, and rating.

Time yourself against the shape:

```
0-1    scope: three or four questions, then stop
1-3    nouns, out loud, before any path
3-7    paths and methods
7-9    one response body
9-11   errors with codes
11-13  auth, pagination, idempotency, rate limits
13-15  one trade-off
```

Then score yourself out of nine on the checklist:

- [ ] nouns, plural, consistent
- [ ] nested for list and create only
- [ ] filters in the query string
- [ ] every collection paginated, with a cap
- [ ] empty collection is `200` with `[]`
- [ ] idempotency key on ride request and on payment
- [ ] `401` versus `403` used correctly, ownership checked in the query
- [ ] versioning mentioned
- [ ] rate limits mentioned with `429` and `Retry-After`

Anything under seven means do it again tomorrow with a different feature.

### The unseen-feature drill

This is Farhat's list. Pick one at random and design it in ten minutes, with no preparation:

a group chat · a hotel booking flow · a movie ticket seat selection · a bank statement export ·
a job application tracker · a fitness app's workout log · a school attendance system ·
a parcel tracking service · a subscription billing page · a photo album with sharing

The point is not the design. It is that you never rehearsed that one.

### The choosing drill

Give the **condition**, not a preference, for each. One sentence each, out loud:

1. REST or GraphQL?
2. REST or gRPC?
3. Session or JWT?
4. `PUT` or `PATCH`?
5. `PATCH /x` or `POST /x/action`?
6. Offset or cursor pagination?
7. Fail open or fail closed when the rate-limit store is down?
8. Shard the database or not?

For number 8, the answer should contain arithmetic.

### The arithmetic drill

From memory, in under three minutes:

- 10M daily users × 8 requests — requests per second, average and peak.
- 80% cacheable at a 90% hit rate — origin load, and the latency difference.
- 300,000 writes against 80M reads — the ratio, and the one conclusion it forces.
- 1M orders a day at 2 KB — storage per year with indexes, and whether you shard.
- bcrypt at 250 ms, 125,000 logins in the peak hour — cores.
- Fixed window at 100/min — the worst-case burst and when.
- 50,000 comments unpaginated — megabytes, and seconds on a 2 Mbps connection.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many substrings does a string of length n have? How many subsequences?*
   Derive both rather than reciting. Then say what the two shapes imply about technique — quadratic
   means you may enumerate, exponential means you never can, which is why one gets a window and the
   other gets a table.

2. *Design the API for a food delivery app's order flow.*
   Four scoping questions, then the nouns out loud, then paths. Say "every collection is paginated"
   and "order creation takes an idempotency key" before anyone asks. Leave time for errors and one
   trade-off. Fifteen minutes.

3. *What is the difference between longest common substring and longest common subsequence?*
   One line of the recurrence, and where the answer lives. Then the deeper point: contiguity means a
   mismatch breaks the run, which is why one resets to zero and the other carries the maximum forward.

---

## Before you move on

- [ ] I say "contiguous?" out loud whenever the word substring or subsequence is missing.
- [ ] I can derive `n(n+1)/2` and `2ⁿ` rather than reciting them.
- [ ] I know contiguous means sliding window and gaps mean a table, and I can say why.
- [ ] I can write the window guard `last[ch] >= start` and name the input that proves it.
- [ ] I can state the one line that differs between the two "longest common" problems.
- [ ] I can run the seven-step API procedure on an unseen feature without preparation.
- [ ] I produce pagination and idempotency before anyone asks for them.
- [ ] I answer every "which one" question with a condition, not a preference.
- [ ] I can redraw the whole-phase diagram from memory, in whatever tool I like.
