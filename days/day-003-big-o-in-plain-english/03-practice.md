---
day: 3
track: practice
title: "Practice — Big-O in plain English"
status: written
---

# Day 003 · Practice

**DSA topic:** Big-O in plain English
**System design topic:** IP addresses, ports, and DNS

**Theme:** Strings and text

---

## Code these, in this order

Four problems, easiest first. Each one has an obvious quadratic solution and a better one,
which is the point.

The habit gains a third step today. For each problem:

1. **Read the constraint first.** Find the largest `n` the problem allows, multiply it out,
   and compare against 10⁸. Decide what shape you are allowed to write **before** you think
   about the solution.
2. Write the obvious solution, whatever it is, and state its Big-O out loud.
3. If the shape does not fit the constraint, improve it, and say what resource you spent to
   do it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Contains Duplicate | LeetCode 217 (Easy) | The exact trap from §7. The nested-loop version is `O(n²)`, the set version is `O(n)`, and the code looks almost identical. |
| 2 | Two Sum | LeetCode 1 (Easy) | Trading space for time. `O(n²)` with two loops, `O(n)` with a dictionary and `O(n)` extra space. Say the trade out loud. |
| 3 | Majority Element | LeetCode 169 (Easy) | Three different shapes for one problem — counting each element is `O(n²)`, sorting is `O(n log n)`, and Boyer-Moore is `O(n)` with `O(1)` space. |
| 4 | Maximum Subarray | LeetCode 53 (Medium) | The brute force is `O(n³)` if you are not careful, `O(n²)` if you are, and `O(n)` with Kadane. Notice how easy the cubic version is to write by accident. |

### On problem 1, do this properly

- Write the nested-loop version first. Run it on 20,000 distinct numbers and time it.
- Write the `set` version. Time it on the same input.
- Look at the ratio. It should be in the thousands, and the two functions differ by one
  word.
- Now state both complexities out loud, and say which line in the first version is the
  hidden loop.

### The measurement drill

Take any one solution you wrote today and run it at n = 250, 500, 1,000 and 2,000, counting
steps rather than timing. Look at the ratio between each size and the next. Name the shape
from the ratio alone, without looking at the code. If your ratio and your Big-O disagree,
your Big-O is wrong.

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Use your own name in your own script for exercise 1; if your script is Latin, borrow `"अंजलि"` for the second half so you see the gap.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Store your name in English and in a non-Latin script. For each, print the byte count and the character count, clearly labelled. In C++, count the characters yourself. | Do you know which count each language gives you by default, and can you get the other one? |
| 2 | Print the first character, the last character, and the middle third of the English name using indexing and slicing. Then try the same three on the non-Latin name and say out loud, for each language, which of the three came out right and why. | Do you understand that Go and C++ slice bytes and Python slices code points? |
| 3 | Print one formatted receipt line: the name right-aligned in twelve spaces, then a price with exactly two decimals, then the number of characters, using f-strings, `fmt.Sprintf`, and `std::format`. Then try to build the same line by adding the pieces together with `+`, and record what each language does with the number. | Can you format in all three, and do you know which language rejects `text + number`, which rejects it at compile time, and which silently does pointer arithmetic? |

**Exercise 1, what you should notice.** Python `len` gives characters and `len(s.encode())` gives bytes. Go `len` gives bytes and `utf8.RuneCountInString` gives characters. C++ `.size()` gives bytes and the character count needs a loop over the bytes counting those below 128 or at least 192.

**Exercise 2, what you should notice.** Python gets all three right on the Hindi name. Go and C++ get the first character right only if you slice exactly three bytes, get the last character wrong unless you count backwards by three, and the middle third is garbage unless the byte count divides neatly. The fix in Go is `[]rune(s)`. There is no built-in fix in C++.

**Exercise 3, what you should notice.** All three formatting tools take a spec after a colon or a percent: `{:>12}` and `{:.2f}` in Python and C++, `%12s` and `%.2f` in Go. For the `+` version: Python raises `TypeError` at run time, Go refuses to compile, and C++ compiles `"text" + 9` and prints a piece of the wrong text. Say the phrase "pointer arithmetic" out loud even though day 12 is when it is explained.

## Compare

- **Python** — Immutable str, f-strings, and slicing. Counts characters, refuses to change a string in place, and refuses to add a number to text, but only when that line runs.
- **Go** — Strings are bytes, runes are characters, fmt.Sprintf. Counts bytes, has a name for a character and a loop that walks them, and refuses text plus number before the program exists.
- **C++** — std::string, string literals, and std::format. Counts bytes, has no name for a character, lets you change a string in place, and accepts text plus number as arithmetic on a pointer.

## Say these out loud

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *What is the time complexity of your solution?*
   Use problem 2 above. Do not open with the letter O — open with the count, reduce it, then
   check every line inside the loop, then give the space separately, then put a number on it
   against the constraint.

2. *How does the browser find the server for google.com?*
   Walk the four caches and the three hops in order, and get to the TTL without being asked
   for it.

3. *You change your server's IP address. How long until every user reaches the new one?*
   One sentence on the answer, one on why nobody can hurry it, and one on what you would do
   the day before a planned migration.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. Why does the length of a string not always equal the number of characters?
2. Which of the three languages let you change a string in place, and what does that make possible and dangerous?
3. What does searching for something that is not there return in each language, and which of the three comparisons `== -1`, `> 0`, and `!= npos` is correct where?

## Before you move on

- [ ] I read the constraint before choosing a solution shape, on all four problems.
- [ ] I can name three things that look like one step and are really loops.
- [ ] I can say what happens to `O(n)`, `O(n log n)` and `O(n²)` when the input doubles,
      from memory.
- [ ] I can walk the DNS chain out loud, in order, and say what is cached at each hop.
- [ ] I can say the difference between an IP address and a port in one sentence.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
