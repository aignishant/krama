---
day: 10
track: lang-practice
title: "Practice — Files and standard I/O"
status: written
---

# Day 010 · Practice

**Theme:** Files and standard I/O

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before you write each read loop, say out loud: "this holds one line" or "this holds the whole file".

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Write a program that creates `shopping.txt` with five lines, one item per line, then reads it back and prints each line with its number. Then append a sixth item and print only the last line, without reading the earlier five into a list. | Can you write, read, and append in each language, and does the file get closed on every path? |
| 2 | Write `wc` in miniature: read standard input to the end and print the number of lines, words, and characters. Run it three ways: typing lines by hand and ending with Ctrl+D or Ctrl+Z, with `< shopping.txt`, and with the output of another program piped in. Then point it at the largest file on your machine and watch memory stay flat. | Do you know the standard-input loop in each language, and have you seen with your own eyes that it does not care what is upstream? |
| 3 | Write a program that copies `in.txt` to `out.txt` while turning every line to upper case, and reports how many lines it copied. Make it fail cleanly with a clear message when `in.txt` is missing, in each language's style: exception, error value, stream check. Then, in each language, deliberately break the closing: drop the `with`, drop the `defer` or the `Flush`, or write with `std::endl` in a loop over a million lines and time it. | Can you stream from one file to another, handle the missing file the native way, and have you felt each language's closing and buffering trap? |

**Exercise 1, what you should notice.** Python `with` and `"a"` mode, Go `os.OpenFile` with `os.O_APPEND|os.O_WRONLY` or simply `os.Create` again for the rewrite plus `defer f.Close()`, C++ `std::ios::app` and no close at all. To print only the last line, keep one variable that each loop iteration overwrites.

**Exercise 2, what you should notice.** `for line in sys.stdin`, `bufio.NewScanner(os.Stdin)`, `while (std::getline(std::cin, line))`. Characters are a byte count in Go and C++ and a code-point count in Python, which is day 3 again; say so in your output.

**Exercise 3, what you should notice.** Missing file: Python's `FileNotFoundError`, Go's `open in.txt: no such file or directory` from `os.Open`, C++'s `if (!in)` which you must remember to write. The broken closings: Python without `with` may leave `out.txt` short if the program dies; Go without `Flush` leaves it empty; C++ with `std::endl` finishes but noticeably slower than `'\n'`.

## Compare

- **Python** — open, with, read/write, pathlib, and sys.stdin. `with` closes on every path, iterating the file object streams one line with its newline attached, and a missing file raises.
- **Go** — os.Open, bufio.Scanner, io.Reader and io.Writer. `defer f.Close()` closes at function exit, the scanner streams one line without its newline and needs `Err()` checked, and a missing file is an error you cannot take the file without.
- **C++** — std::ifstream, std::ofstream, std::cin, std::cout, and buffering. The destructor closes with no line of code, `getline` streams one line without its newline, and a missing file is a silent flag you must test with `if (!in)`.

## Say these out loud

Three questions from today. Answer each in two minutes, standing up, no notes.

1. How do you read a file that is bigger than memory?
2. In each language, what guarantees the file gets closed, and what happens to unwritten data if the program crashes first?
3. What does each language do when the file you try to open does not exist, and which of the three lets you not notice?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
