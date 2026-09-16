---
day: 2
track: lang-practice
title: "Practice — Variables, types, and numbers"
status: written
---

# Day 002 · Practice

**Theme:** Variables, types, and numbers

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. What is the difference between a statically and a dynamically typed language?
2. What does `2 000 000 000 + 2 000 000 000` print in a 32-bit signed integer, and what is the difference between Go's answer and C++'s answer even though they print the same number?
3. Why is `0.1 + 0.2` not `0.3`, in all three languages, and what do you do about it when the numbers are money?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
