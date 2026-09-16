---
day: 3
track: lang-practice
title: "Practice — Strings and text"
status: written
---

# Day 003 · Practice

**Theme:** Strings and text

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. Why does the length of a string not always equal the number of characters?
2. Which of the three languages let you change a string in place, and what does that make possible and dangerous?
3. What does searching for something that is not there return in each language, and which of the three comparisons `== -1`, `> 0`, and `!= npos` is correct where?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
