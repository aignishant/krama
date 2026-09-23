---
day: 3
track: practice
title: "Practice — Big-O in plain English"
status: written
---

# Day 003 · Practice

**DSA topic:** Big-O in plain English
**System design topic:** IP addresses, ports, and DNS

---

## Code these, in this order

Four problems, easiest first. Each one has an obvious quadratic solution and a better one,
which is the point.

The habit gains a third step today. For each problem:

1. **Read the constraint first.** Find the largest `n` the problem allows, multiply it out,
   and compare against 10⁸. Decide what shape you are allowed to write **before** you think
   about the solution.
2. Write the obvious solution, whatever it is, and state its Big-O out loud.
3. If the shape does not fit the constraint, improve it, and say what resource you spent to
   do it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Contains Duplicate | LeetCode 217 (Easy) | The exact trap from §7. The nested-loop version is `O(n²)`, the set version is `O(n)`, and the code looks almost identical. |
| 2 | Two Sum | LeetCode 1 (Easy) | Trading space for time. `O(n²)` with two loops, `O(n)` with a dictionary and `O(n)` extra space. Say the trade out loud. |
| 3 | Majority Element | LeetCode 169 (Easy) | Three different shapes for one problem — counting each element is `O(n²)`, sorting is `O(n log n)`, and Boyer-Moore is `O(n)` with `O(1)` space. |
| 4 | Maximum Subarray | LeetCode 53 (Medium) | The brute force is `O(n³)` if you are not careful, `O(n²)` if you are, and `O(n)` with Kadane. Notice how easy the cubic version is to write by accident. |

### On problem 1, do this properly

- Write the nested-loop version first. Run it on 20,000 distinct numbers and time it.
- Write the `set` version. Time it on the same input.
- Look at the ratio. It should be in the thousands, and the two functions differ by one
  word.
- Now state both complexities out loud, and say which line in the first version is the
  hidden loop.

### The measurement drill

Take any one solution you wrote today and run it at n = 250, 500, 1,000 and 2,000, counting
steps rather than timing. Look at the ratio between each size and the next. Name the shape
from the ratio alone, without looking at the code. If your ratio and your Big-O disagree,
your Big-O is wrong.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *What is the time complexity of your solution?*
   Use problem 2 above. Do not open with the letter O — open with the count, reduce it, then
   check every line inside the loop, then give the space separately, then put a number on it
   against the constraint.

2. *How does the browser find the server for google.com?*
   Walk the four caches and the three hops in order, and get to the TTL without being asked
   for it.

3. *You change your server's IP address. How long until every user reaches the new one?*
   One sentence on the answer, one on why nobody can hurry it, and one on what you would do
   the day before a planned migration.

---

## Before you move on

- [ ] I read the constraint before choosing a solution shape, on all four problems.
- [ ] I can name three things that look like one step and are really loops.
- [ ] I can say what happens to `O(n)`, `O(n log n)` and `O(n²)` when the input doubles,
      from memory.
- [ ] I can walk the DNS chain out loud, in order, and say what is cached at each hop.
- [ ] I can say the difference between an IP address and a port in one sentence.
