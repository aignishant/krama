---
day: 4
track: practice
title: "Practice — The growth curves you will meet again and again"
status: written
---

# Day 004 · Practice

**DSA topic:** The growth curves you will meet again and again
**System design topic:** TCP and UDP

---

## Code these, in this order

Four problems chosen because their **constraints** point at four different shapes. Today the
constraint is the exercise; the code is almost incidental.

For each problem, before writing anything:

1. Find the largest `n` allowed. Say it out loud.
2. Divide 10⁸ by it and name the shape you can afford.
3. Say which technique that shape implies — sorting, a hash map, subsets, a formula.
4. Only then solve it. Afterwards, check that what you wrote matches what you predicted.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Running Sum of 1d Array | LeetCode 1480 (Easy) | `n ≤ 1000`, so almost anything passes. Notice that the constraint gives you no pressure at all, and that this is rare. |
| 2 | Subsets | LeetCode 78 (Medium) | `n ≤ 10`. That number is the answer: 2¹⁰ is 1,024, so generating every subset is intended. Read the constraint before the statement. |
| 3 | Two Sum II — Input Array Is Sorted | LeetCode 167 (Medium) | `n ≤ 30,000` and the array is sorted. Quadratic is 9 × 10⁸ and dies; the sortedness is the hint that two pointers are the target. |
| 4 | Kth Largest Element in an Array | LeetCode 215 (Medium) | `n ≤ 10⁵`. Sorting is `O(n log n)` and comfortably fits, so it is a valid answer — but a heap gives `O(n log k)`. Say what each one costs. |

### On problem 2, do this properly

- Before reading the problem statement, read only the constraint. Write down what shape it
  permits.
- Now read the statement. If your prediction and the problem agree, that is the skill this
  day exists to build.
- Solve it, then compute how long your solution would take at n = 30. Say the number out
  loud. It should frighten you.

### The ceiling drill

Answer these six from memory, in under a minute, without the lesson open:

- The largest `n` an `O(n²)` solution survives.
- The largest `n` an `O(2ⁿ)` solution survives.
- The largest `n` an `O(n!)` solution survives.
- How many operations `O(n log n)` does at n = 100,000.
- How many halvings it takes to get from a billion to one.
- What `n ≤ 20` in a problem statement is telling you.

Then check them against §6 of the lesson. Any you got wrong, redo tomorrow.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *n is 100,000. Will an O(n²) solution pass?*
   Do not say "no". Say the multiplication, the division, the number of seconds, and then
   what shape you would aim for instead.

2. *TCP or UDP for a live video call, and why?*
   Get to head-of-line blocking, and to the fact that the retransmission arrives three
   frames late. Then say what you would put over TCP anyway.

3. *Why does HTTP/3 run over UDP when the web needs reliable delivery?*
   One sentence on what TCP's ordering does to parallel streams, one on what QUIC rebuilds,
   and one on the handshake saving.

---

## Before you move on

- [ ] I read the constraint before choosing an approach, on all four problems.
- [ ] I can recite the eight shapes in order, best to worst, from memory.
- [ ] I can give the ceiling for `O(n²)`, `O(2ⁿ)` and `O(n!)` without looking them up.
- [ ] I can name the four things TCP does that UDP does not.
- [ ] I can explain head-of-line blocking to someone who has never heard the phrase.
