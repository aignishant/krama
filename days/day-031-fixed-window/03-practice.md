---
day: 31
track: practice
title: "Practice — Fixed-size sliding window"
status: written
---

# Day 031 · Practice

**DSA topic:** Fixed-size sliding window
**System design topic:** B-trees and why indexes are shaped that way

---

## Code these, in this order

Four problems with the same window and four different things carried inside it. **For each one, say
what you are maintaining and whether it can be updated in `O(1)` per slide** — that single question
decides whether the problem is easy or hard.

Before each one, ask:

1. What quantity does the window carry — a sum, a count, a set, a maximum?
2. Does that quantity have an inverse, so it can be adjusted rather than recomputed?
3. Which index enters and which leaves? State the resulting range out loud.
4. What is the answer when `k` is larger than the input?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Maximum Average Subarray I | LeetCode 643 (Easy) | The core slide, and dividing once at the end rather than inside the loop. |
| 2 | Contains Duplicate II | LeetCode 219 (Easy) | The window is `k + 1` wide, so the element leaving is at `i - k - 1`. Off by one from every other problem here, on purpose. |
| 3 | Find All Anagrams in a String | LeetCode 438 (Medium) | Window plus a `Counter`, and the `del` at zero without which every comparison fails after the first zero. |
| 4 | Sliding Window Maximum | LeetCode 239 (Hard) | The monotonic deque. Easy problem, one sentence away, and a completely different technique — because `max` has no inverse. |

### On problem 1, check the index rule out loud

Before writing the loop, complete these three lines:

```
k = 3, window currently covers indices 0,1,2
  index 3 enters -> index ___ leaves -> window is now [___ .. ___]
  index 4 enters -> index ___ leaves -> window is now [___ .. ___]
```

Then write the loop and confirm that after `total += nums[i] - nums[i - k]` the window is
`nums[i-k+1 .. i]`, which has exactly `k` elements.

### On problem 1, break it three ways

Run each and say what happens:

```python
# A
total += nums[i] - nums[i - k + 1]
```

```python
# B
best = 0                              # instead of the first window's sum
print(max_sum([-1, -2, -3], 2))
```

```python
# C
for i in range(1, len(nums)):         # instead of range(k, ...)
```

A gives a plausible wrong answer. B returns 0, which is not the sum of any window. C uses a negative
index, which in Python reads from the **end** of the array rather than raising. Say which of the three
you would be least likely to notice, and why.

### On problem 2, work out the width yourself

The problem says "there exist two distinct indices `i` and `j` such that `nums[i] == nums[j]` and
`abs(i - j) <= k`". Before coding, answer:

1. How many elements does the window need to hold?
2. Therefore, which index leaves when `i` enters?
3. Why is it different from problems 1 and 3?

Then run it on `[1,0,1,1]` with `k = 1` — the answer is `True` — and on `[1,2,3,1,2,3]` with `k = 2`,
where it is `False`.

Then swap `discard` for `remove` and run it on `[1,1,1]`. Read the error and say why `discard` is the
right choice here.

### On problem 3, find the silent failure

Write it, then delete the two lines that remove a zero count:

```python
window[left] -= 1
# if window[left] == 0:
#     del window[left]
```

Run it on `find_anagrams("cbaebabacd", "abc")`. You should get `[0]` instead of `[0, 6]`.

Then explain, in one sentence, why `Counter({'a': 1, 'b': 0})` is not equal to `Counter({'a': 1})`, and
why that makes every comparison after the first zero fail.

### On problem 4, do the two easy things first

1. Write the naive version: `max(nums[i:i+k])` at each position. State its cost.
2. Write the heap version and state its cost. Say what extra bookkeeping it needs.
3. Only then write the deque version.

Then answer, out loud:

1. Why can a sum be maintained incrementally and a maximum cannot?
2. In the deque, why do you store **indices** rather than values?
3. Why do you pop from the back everything smaller than the entering value?
4. Why is it `O(n)` and not `O(n·k)`, given there is a `while` inside a `for`?

Number 4 is the argument you will be asked for. It is about counting pushes.

### The maintainability drill

For each quantity, say whether a fixed window can maintain it in `O(1)` per slide, and why:

1. Sum.
2. Average.
3. Product. (Careful — there is a subtlety.)
4. Maximum.
5. Number of distinct values.
6. Whether all values are distinct.
7. Median.
8. The count of a particular character.

Number 3 has an inverse in principle — division — and one input breaks it. Say which. Number 7 needs a
structure you have not met yet; name what it would have to support.

### The measurement drill

Run this and read the ratio column.

```python
import time, random
random.seed(3)

def window(nums, k):
    total = sum(nums[:k]); best = total
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        best = max(best, total)
    return best

def brute(nums, k):
    best = None
    for i in range(len(nums) - k + 1):
        s = sum(nums[i:i + k])
        if best is None or s > best: best = s
    return best

for n, k in ((10_000, 100), (50_000, 500), (100_000, 1000)):
    arr = [random.randint(-100, 100) for _ in range(n)]
    s = time.perf_counter(); window(arr, k); t1 = time.perf_counter() - s
    s = time.perf_counter(); brute(arr, k);  t2 = time.perf_counter() - s
    print(f"n={n:>7} k={k:>5}  {t1:.5f}s  {t2:.4f}s  ratio {t2/t1:>6.0f}x")
```

Then answer:

1. Why does the ratio grow as `k` grows, rather than staying constant?
2. The brute version uses `sum()` on a slice, which runs as compiled C. Does that make the measured
   ratio bigger or smaller than the true gap between the two ideas?
3. Give the operation counts at `n = 100,000`, `k = 1,000` for both.

### The B-tree drill

Answer each in one or two sentences, out loud:

1. Why is the unit of cost on disk a page rather than a comparison? Give both timings.
2. Fanout 500 — rows covered at depth 2, 3 and 4.
3. Compare page reads **and** comparison counts for a B-tree against a binary tree on ten million
   rows. Which one is the point?
4. What are the two differences in a B+ tree, and what does each buy?
5. Why do range queries and `ORDER BY` cost almost nothing on an indexed column?
6. What happens on an insert when the leaf is full? How does the tree ever get taller?
7. Why do sequential primary keys produce a smaller, faster index than random UUIDs?
8. When would you choose an LSM tree instead, and what do you give up?

Number 3 is the one that separates a memorised answer from an understood one.

### The derivation drill

Do not recall these — derive them, out loud, in under a minute:

1. Page 8 KB, entry 16 bytes → fanout.
2. Fanout → depth for 10 million rows.
3. Depth × 0.1 ms → lookup time.
4. Binary tree depth for the same rows → its lookup time.
5. The ratio.

Then do the same for a 16 KB page and say what changes and what does not.

### The comparison drill

Fill in this table from memory:

| | B-tree | Hash index | LSM tree |
|---|---|---|---|
| equality lookup | | | |
| range query | | | |
| `ORDER BY` for free | | | |
| write cost | | | |
| used by | | | |

Then say, in one sentence each, why Postgres defaults to a B-tree rather than a hash index, and why
Cassandra does not use a B-tree at all.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the maximum sum of any subarray of size k.*
   Brute force and its cost. Then the overlap insight in one sentence. Then the slide, saying the index
   rule and checking the resulting range aloud. Then `O(n)` with the counting. Then flag the two
   boundary cases — `k` too large, and `best` starting from the first window.

2. *Why is a database index a B-tree and not a binary search tree?*
   Lead with the hardware fact and both timings. Derive the fanout and the depth. Then the point that
   makes it: the comparison counts are the same and the page reads differ by eight times. Then B+
   refinements, then LSM as the alternative.

3. *Now find the maximum in each window instead of the sum.*
   Say why the arithmetic stops working — addition has an inverse and `max` does not. Then the deque of
   indices, both pop rules with their reasons, and the `O(n)` argument by counting pushes.

---

## Before you move on

- [ ] I say "consecutive windows overlap in `k−1` elements" before writing any window code.
- [ ] I state the resulting range `[i−k+1 .. i]` out loud to check the index rule.
- [ ] I start `best` from the first window, never from 0.
- [ ] I guard `k` larger than the array and say what I return.
- [ ] I know which quantities have an inverse and which do not, and why that decides the technique.
- [ ] I delete zero counts from a `Counter`, and use `discard` rather than `remove` on a set.
- [ ] I can give the deque's two pop rules with a one-line reason for each.
- [ ] I can argue the deque is `O(n)` by counting pushes rather than loop nesting.
- [ ] I can derive fanout → depth → page reads without recalling any of the numbers.
- [ ] I can say why the B-tree does *more* comparisons than a binary tree and is still eight times
      faster.
- [ ] I can redraw the sliding-window diagram and the B-tree fanout diagram from memory, in whatever
      tool I like.
