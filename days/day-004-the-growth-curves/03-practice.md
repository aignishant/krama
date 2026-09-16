---
day: 4
track: practice
title: "Practice — The growth curves you will meet again and again"
status: written
---

# Day 004 · Practice

**DSA topic:** The growth curves you will meet again and again
**System design topic:** TCP and UDP

**Theme:** Conditions and loops

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

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before running each, say out loud how many lines it will print.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Print the numbers 1 to 20, but for multiples of 3 print `fizz` instead, for multiples of 5 print `buzz`, and for multiples of both print `fizzbuzz`. Use `%` for the remainder and get the order of the conditions right. | Can you write an `if`/`else if`/`else` chain in each language, and do you test the most specific condition first? |
| 2 | Given the row `[3, 8, 12, 5, 20, 7]`, find the position of the first number greater than 10. Write it twice in each language: once with a `for` and `break`, once with a `while` whose condition does all the stopping. Print the position, or `not found` if there is none, using the row `[1, 2, 3]` for the second run. | Can you express early exit both ways, and can you produce the not-found branch in a language that has no `for-else`? |
| 3 | Write a countdown from 10 to 1 that skips even numbers, then prints `go`. Then write a menu that asks the same yes-or-no question until the answer is exactly `y` or `n`, hard-coding the "answers" as a row like `["maybe", "later", "y"]` and walking it. Use `do-while` in C++ and say out loud why Go and Python do not need it. | Do you know `continue`, and do you know which loop shape fits "at least once" in each language? |

**Exercise 1, what you should notice.** The `fizzbuzz` test must come first, or 15 prints `fizz` and stops. Python `elif`, Go `else if`, C++ `else if`; the shape is the same in all three and only the brackets differ.

**Exercise 2, what you should notice.** The `for`-and-`break` version is the same length in all three. The `while` version in Go is spelled `for`. In Python you can also do the not-found branch with `for-else`; do that as a fourth version and decide out loud whether it is clearer than the flag.

**Exercise 3, what you should notice.** In C++ the menu is a natural `do-while`: ask, then check. In Go and Python you write an infinite loop with a `break` when the answer is valid, or a `while True` / `for {}`, which is the same thing. Neither is worse; it is a keyword the other two chose not to spend.

## Compare

- **Python** — if/elif/else, for-in, while, break and continue. Indentation is the block, `=` in a condition is refused, and `for-else` gives a not-found branch nobody else has.
- **Go** — if with init statements, the only loop is for, switch without fallthrough. One loop keyword in four shapes, an init statement whose variable dies with the `if`, and a `switch` that stops on its own.
- **C++** — if, for, while, do-while, range-for, switch with fallthrough. Four loop keywords including the only "at least once" loop, an `if (x = 3)` that compiles, and a `switch` that needs a `break` on every case.

## Say these out loud

### DSA and system design
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



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. Write a loop that stops early. Now write it without `break`.
2. What does `switch` do after the matching case in each of the three languages, and what do you write in C++ to make the intention clear?
3. Which of the three languages accepts `if (x = 3)`, what does it do, and how did the other two stop you?

## Before you move on

- [ ] I read the constraint before choosing an approach, on all four problems.
- [ ] I can recite the eight shapes in order, best to worst, from memory.
- [ ] I can give the ceiling for `O(n²)`, `O(2ⁿ)` and `O(n!)` without looking them up.
- [ ] I can name the four things TCP does that UDP does not.
- [ ] I can explain head-of-line blocking to someone who has never heard the phrase.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
