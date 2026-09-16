---
day: 1
track: lang-practice
title: "Practice — Toolchain and the first program"
status: written
---

# Day 001 · Practice

**Theme:** Toolchain and the first program

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. What actually happens between saving the file and seeing the output?
2. Why did `Hello, world` print before the error in Python but not in Go or C++?
3. What is a warning, which of the three languages has them, and what do you do about them?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
