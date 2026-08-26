---
day: 2
track: practice
title: "Practice — Counting steps: your first cost model"
status: written
---

# Day 002 · Practice

**DSA topic:** Counting steps: your first cost model
**System design topic:** Client and server, explained properly

---

## Code these, in this order

Four problems, easiest first, and each one is a different counting shape. Every one is on
LeetCode and free.

Today the habit gains a step. For each problem:

1. **Before you write anything**, say how many times the loop body will run for an input of
   size n. Commit to a formula, not a feeling.
2. Solve it.
3. Add a `steps` counter to the loop body, run it on a small input, and compare the number
   with your prediction.

Getting the prediction wrong is useful. Getting it wrong and not noticing is the thing this
step exists to prevent.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Final Value of Variable After Performing Operations | LeetCode 2011 (Easy) | The simplest possible count. One loop, no nesting, body runs exactly n times. Say "n" out loud before you start. |
| 2 | Number of Steps to Reduce a Number to Zero | LeetCode 1342 (Easy) | The halving loop. For n = 14 the answer is 6, not 14. Count the steps for 1,000 and see that it is 10-ish, not 1,000. |
| 3 | Plus One | LeetCode 66 (Easy) | The count depends on the input, not just its size. `[1,2,3]` costs one step; `[9,9,9]` costs three. Best case and worst case in one small function. |
| 4 | Number of Good Pairs | LeetCode 1512 (Easy) | The staircase. Write the nested version first and check the count against n × (n − 1) / 2 before you improve it. |

### On problem 4, do this properly

- Write the nested version, with the inner loop starting at `i + 1`.
- Run it on a list of four items and check that the body ran **6** times, not 10 and not 16.
- Then change the inner loop to start at `i` instead of `i + 1`, run it again, and watch the
  count become 10 and the answer become wrong. That is trap one from §7 of the lesson,
  happening to you rather than being described to you.
- Change it back.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *How many times does the inner loop execute if the array has n elements?*
   Use problem 4 above as the code. Do not stop at "n squared" — give the exact count, then
   check it at n = 4 the way §8 of the lesson does.

2. *What is the difference between a client and a server? Where does your code live?*
   Draw the boundary as you talk, and get to the untrusted-client consequence without being
   asked for it.

3. *A user changes the price in the browser before checking out. What happens, and why?*
   One sentence on what the client is allowed to send, and one on what the server must work
   out for itself.

---

## Before you move on

- [ ] I predicted the count before coding, on all four problems.
- [ ] I checked at least two predictions with a `steps` counter and they matched.
- [ ] I can say why the staircase is n × (n − 1) / 2 by pairing the ends, without looking
      it up.
- [ ] I can name what lives on the client side and what lives on the server side, out loud,
      from memory.
