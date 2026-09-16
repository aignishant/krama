---
day: 6
track: lang-practice
title: "Practice — Growable sequences"
status: written
---

# Day 006 · Practice

**Theme:** Growable sequences

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. For each, say out loud before running: "this line copies" or "this line shares".

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Start with an empty sequence and add the numbers 1 to 30 one at a time. Print a line every time the hidden block changes size. In Python use `sys.getsizeof`, in Go `cap`, in C++ `capacity()`. Then do it again after asking for room for 30 up front where the language lets you, and count the copies. | Can you see amortised growth happen, and do you know which languages let you pre-size? |
| 2 | Make a sequence of five names. Make a second name for it with plain `=`, and a third with whatever the language's real copy is. Add a name through the second, change the first element through the third, then print all three. Predict the output before you run. | Do you know what `=` does in each language, and what a real copy looks like? |
| 3 | Given the sequence `[10, 20, 30, 40, 50]`, remove every value greater than 25 while walking the sequence, the naive way, and print the result. Then do it the right way. In Go, additionally take a sub-slice of the first two, append to it, and print the original. In C++, additionally read index 7 with `[]` and then with `at()`. | Do you know the three classic bugs: mutating while iterating, the shared sub-slice, and the unchecked index? |

**Exercise 1, what you should notice.** All three double for small sizes. Python: 1, 5, 9, 17, 25. Go and C++: 1, 2, 4, 8, 16, 32. Go's `make([]int, 0, 30)` and C++'s `reserve(30)` give zero copies; Python has no equivalent, and that is a fact about Python worth saying out loud.

**Exercise 2, what you should notice.** Python and Go: the second name shares, so the addition shows through the first name; the real copy, `list(a)` or `a[:]` and `slices.Clone(a)`, does not. C++: `=` already is the real copy, so nothing shows through. If your prediction was wrong in any language, that is the day's lesson and it is worth ten minutes.

**Exercise 3, what you should notice.** The naive removal skips an element in Python and C++ and in Go the `append`-based delete inside a `range` loop behaves worse. The right way in all three is to build a new sequence of the ones to keep. The Go sub-slice overwrites the original's third element. The C++ `[]` prints garbage or nothing; `at()` stops with `std::out_of_range`.

## Compare

- **Python** — list: append, insert, pop, slicing, and the cost of each. Capacity hidden, `=` shares, slicing copies, every index checked, and no way to pre-size.
- **Go** — slice: length, capacity, append, and the backing array. Capacity visible, `=` and slicing both share the backing array, `append` may or may not move, every index checked with a panic.
- **C++** — std::vector: push_back, size, capacity, and reallocation. Capacity visible and reservable, `=` copies everything, `[]` checks nothing, and a reference dies when the block moves.

## Say these out loud

Three questions from today. Answer each in two minutes, standing up, no notes.

1. What happens under the hood when you append to a full sequence?
2. In each language, what does `b = a` do to a sequence, and how do you make a real copy?
3. What does reading one past the end do in each language, and which answer is the most dangerous?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
