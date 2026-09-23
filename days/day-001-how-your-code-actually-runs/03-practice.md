---
day: 1
track: practice
title: "Practice — How your code actually runs, and where the time goes"
status: written
---

# Day 001 · Practice

**DSA topic:** How your code actually runs, and where the time goes
**System design topic:** What happens when you type google.com and press Enter

---

## Code these, in this order

Four problems, easiest first. Every one of them is on LeetCode, and every one is free.

For each problem, do the same three things. This is the habit the whole course is built on.

1. Solve it.
2. **Before you submit**, point at the hot line and say how many times it runs.
3. Add a counter to the hot line, print it for a small input, and check whether you were
   right.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Concatenation of Array | LeetCode 1929 (Easy) | Can you write a single loop at all, and do you know how many times its body runs? |
| 2 | Running Sum of 1d Array | LeetCode 1480 (Easy) | One loop that carries a value forward. It is the shape of every prefix problem you will meet on day 037. |
| 3 | Richest Customer Wealth | LeetCode 1672 (Easy) | Your first genuinely nested loop. The hot line sits inside both loops. Say the count out loud before you run it. |
| 4 | Contains Duplicate | LeetCode 217 (Easy) | The exact function from today's lesson. Write the nested version **deliberately**, submit it, and watch what happens on the big test case. |

### On problem 4, do this properly

It is the whole day in one exercise, so do not skip the second half.

- Write `has_duplicate` with two nested loops, exactly as in §5 of the lesson.
- Submit it, and note what LeetCode says.
- Then run it on your own machine, on a list of 5,000 numbers with no duplicates in it, and
  time it.
- Then double the list to 10,000 numbers and time it again.
- The second number should be roughly **four times** the first, not twice. When you see
  that with your own eyes rather than being told it, it stays with you.

Use a list with no duplicates, because that is the input that forces the loops to run all
the way to the end. A list with a duplicate near the front returns almost immediately and
tells you nothing.

You are not expected to know the fast solution yet. That is
[day 062](../day-062-sets/README.md).

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson. Say them to a wall if there is nobody around. Speaking is a different skill from
knowing, and the interview tests the speaking one.

1. *Walk me through this function line by line. Which line runs the most times?*
   Use problem 3 above as the function.

2. *What happens when you type google.com into your browser and hit Enter?*
   Six beats, roughly fifteen seconds each. Name the shape of your answer before you start.

3. *Is `x in my_list` a single step? Say exactly what the computer does when it runs that
   line, and what that means for a loop with it inside.*

---

## Before you move on

- [ ] I can write today's DSA code from memory, with nothing to refer to.
- [ ] I can name the six beats of the journey in order, out loud, without looking at the
      lesson.
- [ ] I answered all three questions above out loud.
- [ ] I timed problem 4 at two input sizes and saw the four-times jump myself.
