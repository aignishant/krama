---
day: 4
track: lang-practice
title: "Practice — Conditions and loops"
status: written
---

# Day 004 · Practice

**Theme:** Conditions and loops

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. Write a loop that stops early. Now write it without `break`.
2. What does `switch` do after the matching case in each of the three languages, and what do you write in C++ to make the intention clear?
3. Which of the three languages accepts `if (x = 3)`, what does it do, and how did the other two stop you?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
