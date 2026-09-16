---
day: 2
track: practice
title: "Practice — Counting steps: your first cost model"
status: written
---

# Day 002 · Practice

**DSA topic:** Counting steps: your first cost model
**System design topic:** Client and server, explained properly

**Theme:** Variables, types, and numbers

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

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before you run each one, say out loud what you expect it to print. Then run it. The gap between the two is today's lesson.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Declare a whole number holding your age, a decimal holding your height in metres, and a piece of text holding your name. Print all three on one line, then print the type of each. | Can you declare each kind of value in each language, and do you know which languages make you name the type? |
| 2 | Predict, then print, `2 000 000 000 + 2 000 000 000` three ways: in whatever the language's default whole number is, in an explicit 32-bit type, and in an explicit 64-bit type. In Python, explain out loud why the second and third do not exist. | Do you know how wide each language's default integer is, and can you say what each one does past the top? |
| 3 | Add `0.1` ten times in a running total and compare it with `1.0`. Print the total with enough digits to see the problem, and print whether it is equal. Then do the same sum counting in whole tenths as integers, and show that this version is exact. | Do you understand why floats fail equality checks, and can you fix it the way money code fixes it? |

**Exercise 1, what you should notice.** Python: `type(age)`. Go: `%T` in `fmt.Printf`. C++: there is no built-in way to print a type's name nicely, so print `sizeof` instead and say the type out loud. That absence is itself a lesson about C++.

**Exercise 2, what you should notice.** Python: `4000000000`, always. Go: `4000000000` for `int` and `int64`, `-294967296` for `int32`, and the compiler stops you if you write the overflowing sum as a constant. C++: `int` and `int32_t` give `-294967296` on your machine, with a warning if the compiler can see the constants, and no warning at all if the values are in variables. Say the phrase "undefined behaviour" and say what it does not mean.

**Exercise 3, what you should notice.** In all three, the float total is `0.9999999999999999` and the comparison is false. In all three, ten integer tenths is exactly ten, and the comparison is true. In C++ you need `std::setprecision(17)` to see the digits; in Go and Python they print by default.

## Compare

- **Python** — Dynamic names, int without limits, float with them. The only one where the same name can hold an int and then a string, and the only one where you never think about integer width.
- **Go** — Static types, int64, and := versus var. Width is chosen on the name, overflow is a defined wrap, and the compiler catches the constant case but not the variable case.
- **C++** — Fixed-width ints, overflow, and auto. Width is chosen on the name and signed overflow is a promise the language refuses to make, so the check goes before the arithmetic, not after.

## Say these out loud

### DSA and system design
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



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. What is the difference between a statically and a dynamically typed language?
2. Add two runtime values of 2,000,000,000 in a signed 32-bit integer. Why does Go wrap, while signed overflow in C++ has undefined behaviour and no guaranteed result? Why does Go reject an overflowing constant expression instead?
3. Why is `0.1 + 0.2` not `0.3`, in all three languages, and what do you do about it when the numbers are money?

## Before you move on

- [ ] I predicted the count before coding, on all four problems.
- [ ] I checked at least two predictions with a `steps` counter and they matched.
- [ ] I can say why the staircase is n × (n − 1) / 2 by pairing the ends, without looking
      it up.
- [ ] I can name what lives on the client side and what lives on the server side, out loud,
      from memory.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
