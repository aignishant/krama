---
day: 1
track: practice
title: "Practice — How your code actually runs, and where the time goes"
status: written
---

# Day 001 · Practice

**DSA topic:** How your code actually runs, and where the time goes
**System design topic:** What happens when you type google.com and press Enter

**Theme:** Toolchain and the first program

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

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Do them in that order, in the same `day01` folder, so you feel the difference in the run cycle with your hands.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Print your own name on one line and the city you are in on the next. Run it. | Can you get from an empty file to output in all three toolchains without looking anything up? |
| 2 | Take the working program from exercise 1 and break it three different ways, one at a time: misspell the print instruction, remove a quote, and remove the import or include line. For each break, run it and write down, in your phone, the first line of the error and whether anything printed before the error. | Can you tell a syntax error from a name error, and can you predict which languages print nothing at all? |
| 3 | For Go and C++ only, build a real executable file, then delete the source file, then run the executable. It still runs. Now try to do the same in Python and explain out loud why you cannot. | Do you understand that a compiled program is a separate file that no longer needs its source? |

**Exercise 1, what you are aiming for.** Three files, `name.py`, `name.go`, `name.cpp`, each printing two lines. Python is one command to run. Go is one command with `go run` or two with `go build`. C++ is always two.

**Exercise 2, what you should notice.** In Python, the misspelled `print` still prints the lines before it. In Go and C++, nothing prints for any of the three breaks. In Python, the missing quote prints nothing either, because it is a syntax error and those are caught before line 1 runs. Say that sentence out loud until it is yours.

**Exercise 3, what you should notice.** `go build name.go`, then `rm name.go`, then `./name` still works. Same with `g++`. With Python there is no second file to run; the source is the program.

## Compare

- **Python** — python3, a file, and the interpreter. Easiest to start, one line and one command, and the only one of the three that will happily run half a broken file.
- **Go** — go run, go build, and the Go toolchain. Five lines before it will accept anything, and the strictest of the three: an unused import is a hard stop.
- **C++** — g++, a file, and the compiler. The only one where the two steps are two visible commands, and the only one with a category between "fine" and "refused", which is why the warning flags are not optional.

## Say these out loud

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson. Say them to a wall if there is nobody around. Speaking is a different skill from
knowing, and the interview tests the speaking one.

1. *Walk me through this function line by line. Which line runs the most times?*
   Use problem 3 above as the function.

2. *What happens when you type google.com into your browser and hit Enter?*
   Six beats, roughly fifteen seconds each. Name the shape of your answer before you start.

3. *Is `x in my_list` a single step? Say exactly what the computer does when it runs that
   line, and what that means for a loop with it inside.*



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. What actually happens between saving the file and seeing the output?
2. Why did `Hello, world` print before the error in Python but not in Go or C++?
3. What is a warning, which of the three languages has them, and what do you do about them?

## Before you move on

- [ ] I can write today's DSA code from memory, with nothing to refer to.
- [ ] I can name the six beats of the journey in order, out loud, without looking at the
      lesson.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] I timed problem 4 at two input sizes and saw the four-times jump myself.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
