---
day: 32
track: practice
title: "Practice — Variable-size sliding window"
status: written
---

# Day 032 · Practice

**DSA topic:** Variable-size sliding window
**System design topic:** Query plans and the slow query

---

## Code these, in this order

Four problems, two of each shape. **Before writing a line of any of them, say out loud whether it is
shape A or shape B**, and therefore where the recording goes. Getting that wrong is the failure mode of
this whole family, and it produces code that runs.

Before each one, ask:

1. Minimise or maximise? Therefore shrink-while-valid or shrink-while-invalid?
2. Is the condition monotonic as the window grows? (Any negative numbers?)
3. What does the window carry, and can it be updated in `O(1)` per move?
4. What is returned when no valid window exists?

| # | Problem | Source | Shape, and what it is really testing |
|---|---|---|---|
| 1 | Minimum Size Subarray Sum | LeetCode 209 (Medium) | Shape A. Record **inside** the shrink loop. And whether you ask about negative values. |
| 2 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | Shape B. Shrink **before** adding, record **after**. |
| 3 | Longest Repeating Character Replacement | LeetCode 424 (Medium) | Shape B with a subtle validity test, and an optimisation whose correctness argument is the real question. |
| 4 | Minimum Window Substring | LeetCode 76 (Hard) | Shape A with a count map and a `missing` counter. The hardest window problem asked routinely. |

### On problem 1, get the recording place wrong on purpose

Write it correctly, then move the recording line to after the `while` loop:

```python
for right, x in enumerate(nums):
    total += x
    while total >= target:
        total -= nums[left]
        left += 1
    best = min(best, right - left + 1)      # moved OUT of the loop
```

Run it on `[2,3,1,2,4,3]` with target 7. It returns 1 instead of 2. Say exactly why — what is true about
the window at the moment the `while` loop exits?

Then say the rule in one sentence: minimise records where, maximise records where?

### On problem 1, break it with negatives

```python
print(min_subarray_len(3, [-3, 5]))
```

It returns `0`, meaning "no such subarray", and the answer is `1` — the single element `5`.

Trace it: what is the total after `right = 0`? After `right = 1`? Why does the shrink loop never run,
and why is that the *correct* behaviour for the code and the wrong answer for the problem?

Then say what makes a sliding window legal, in one sentence, and name the technique you would use
instead.

### On problem 2, do it both ways

Write the `while`-shrink version and the jump-with-a-last-seen-map version. Confirm both give
`[3, 1, 3, 0, 2, 3, 2]` for
`["abcabcbb", "bbbbb", "pwwkew", "", "au", "dvdf", "abba"]`.

Then delete the `last[ch] >= left` guard from the jump version and run it on `"abba"`. You should get 3
instead of 2.

Then answer:

1. Where exactly did `left` move backwards, and why?
2. Why can the `while` version never have this bug?
3. Why does `left` moving backwards break the `O(n)` argument as well as the answer?

### On problem 3, write the honest version first

Write it recomputing `max(count.values())` inside the shrink condition. Confirm it gives `[4, 4, 4, 0]`
for `[("ABAB",2), ("AABABBA",1), ("AAAA",0), ("",1)]`. State its cost — and say why `O(26)` per step is
still `O(n)` overall.

Only then write the version that carries `max_freq` and never decreases it. Then answer the question
that matters:

1. Why is it correct never to decrease `max_freq` when the window shrinks?
2. What could go wrong if the problem asked for the *smallest* window instead?

### On problem 4, build it in three stages

1. First, a version that checks validity by comparing two `Counter`s. Get it correct.
2. Then replace the comparison with the `missing` counter and confirm the answers are unchanged.
3. Then explain what a **negative** value in `need` represents, and why the trim loop uses `< 0`.

Test on `[("ADOBECODEBANC","ABC"), ("a","a"), ("a","aa"), ("ab","b")]` — expect
`['BANC', 'a', '', 'b']`.

### The shape drill

For each problem, say **shape A** or **shape B**, and where the recording goes, in under five seconds:

1. Shortest subarray with sum at least k.
2. Longest subarray with sum at most k.
3. Longest substring with at most 2 distinct characters.
4. Smallest window containing all letters of t.
5. Longest subarray where max minus min is at most k.
6. Number of subarrays with at most k distinct values.
7. Shortest substring containing at least k of some character.

Number 6 is the one that becomes tomorrow's material — say why counting is different from finding a
best.

### The monotonicity drill

For each, say whether a sliding window is legal, and why:

1. Sum ≥ target, all values positive.
2. Sum ≥ target, values may be negative.
3. Product ≤ target, all values ≥ 1.
4. Product ≤ target, values may be 0 or between 0 and 1.
5. At most k distinct characters.
6. The window contains all letters of `t`.
7. Maximum minus minimum ≤ k.

Numbers 2 and 4 fail. For number 7, the window *is* legal but needs two extra structures — name them.

### The cost-argument drill

Say each of these out loud, without notes:

1. Why is a `while` inside a `for` still `O(n)` here?
2. How many times can `left` move in total, and why?
3. What single property of the pointers is the whole argument resting on?
4. What breaks the argument in the buggy `"abba"` version?

### The measurement drill

```python
import time, random
random.seed(5)

def window(target, nums):
    left = 0; total = 0; best = float('inf')
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]; left += 1
    return 0 if best == float('inf') else best

def brute(target, nums):
    best = float('inf')
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= target:
                best = min(best, j - i + 1); break
    return 0 if best == float('inf') else best

for n in (2000, 5000, 10000):
    arr = [random.randint(1, 10) for _ in range(n)]
    tgt = 10 ** 6                      # unreachable, so both do full work
    s = time.perf_counter(); window(tgt, arr); t1 = time.perf_counter() - s
    s = time.perf_counter(); brute(tgt, arr);  t2 = time.perf_counter() - s
    print(f"n={n:>6}  {t1:.5f}s  {t2:.4f}s  ratio {t2/t1:>6.0f}x")
```

Then answer: why is the target chosen to be unreachable, and what does the ratio doubling tell you?

### The plan-reading drill

For each fragment, give the diagnosis and the fix in one sentence:

```
Seq Scan on orders (cost=0.00..18334.00 rows=1 width=64)
                   (actual time=0.021..112.4 rows=3 loops=1)
  Filter: (customer_id = 4217)
  Rows Removed by Filter: 999997
```

```
Nested Loop  (cost=... rows=1) (actual rows=480000 loops=1)
  ->  Index Scan on a  (rows=1) (actual rows=480000 loops=1)
  ->  Index Scan on b  (rows=1) (actual rows=1 loops=480000)
```

```
Sort  (actual time=8200..8400 rows=1000000 loops=1)
  Sort Method: external merge  Disk: 102400kB
```

```
Index Scan using orders_pkey (actual time=0.02..0.05 rows=1 loops=61)
```

```
Seq Scan on users (actual rows=480000 loops=1)
  Filter: (lower(email) = 'a@b.com'::text)
```

The second one is the most important. Say why adding an index would not help it.

### The EXPLAIN drill

Answer each in one or two sentences, out loud:

1. In `(cost=0.42..8.45 rows=3 width=64)`, what is each number?
2. What is the difference between `EXPLAIN` and `EXPLAIN ANALYZE`, and what precaution does the second
   need?
3. Which do you read first — the top line or the most indented line?
4. What does `Rows Removed by Filter` tell you?
5. What does `loops=N` do to the reported `actual time`?
6. Estimated rows 1, actual rows 480,000 — what is the cause and what is the fix?
7. Name two causes of a slow query that never appear in a plan.
8. Why sort `pg_stat_statements` by total time rather than mean time?
9. Why does Postgres have no query hints?

### The arithmetic drill

From memory, in under two minutes:

- A nested loop chosen on an estimate of 1 row where the reality is 480,000 — lookups and time, against
  the hash join it should have chosen.
- 1,000,000 rows at 200 bytes — sequential scan against index scan.
- `actual time=0.05` with `loops=61` — real database time, and real wall-clock with round trips.
- Sorting 100 MB with `work_mem` at 4 MB against 128 MB.
- A 2,000 ms query run once a day against a 20 ms query run a million times — daily cost of each.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the smallest subarray with a sum at least k.*
   Ask about negatives first, and say why. Name the shape. State the invariant and why `left` never
   goes back. Say where the recording goes and why. Finish with the `2n` argument and the no-answer
   convention.

2. *Here is an EXPLAIN plan. What is wrong with this query?*
   The procedure, in order: read inside out, compare estimated with actual **first**, then scan types,
   then `loops`, then `Disk`. Name the two causes that never appear in a plan. Then fix in order of
   cost.

3. *Why does a sliding window stop working when the array has negative numbers?*
   Monotonicity. Give the concrete failure — `[-3, 5]` with target 3 returns "no answer" when the
   answer is 1 — and name the correct technique instead.

---

## Before you move on

- [ ] I say "minimise or maximise?" before writing any variable window, and therefore where to record.
- [ ] I ask about negative values before applying a window to a sum.
- [ ] I can state the monotonicity requirement in one sentence.
- [ ] In shape B I shrink **before** adding, and record **after**.
- [ ] I can argue `O(n)` from "neither pointer ever moves backwards".
- [ ] I can name the input where a missing `last[ch] >= left` guard makes `left` go backwards.
- [ ] I say `EXPLAIN ANALYZE` before "add an index".
- [ ] I compare estimated rows with actual rows **before** looking at scan types.
- [ ] I know `actual time` is per loop and multiplies by `loops`.
- [ ] I can name two causes of slowness that never appear in a plan.
- [ ] I can redraw the two-shapes template and the bad-estimate diagram from memory, in whatever tool I
      like.
