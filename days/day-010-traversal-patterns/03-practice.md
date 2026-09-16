---
day: 10
track: practice
title: "Practice — Traversal: the loop patterns you will reuse forever"
status: written
---

# Day 010 · Practice

**DSA topic:** Traversal: the loop patterns you will reuse forever
**System design topic:** Latency numbers every engineer should know

**Theme:** Files and standard I/O

---

## Code these, in this order

Four problems, one per traversal pattern. The code in each is short; the loop bound is the
whole exercise.

For each problem, **before writing the loop**:

1. Say the largest index the body will touch.
2. Say the bound that follows from it, out loud, with the arithmetic.
3. Say how many iterations that gives for an array of 7.
4. Then write it, and check the empty and single-element cases without adding a special case.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Monotonic Array | LeetCode 896 (Easy) | The adjacent-pairs bound, exactly. `range(n - 1)` because the body reaches `i + 1`, and it must return `True` for a one-element array without a guard. |
| 2 | Maximum Average Subarray I | LeetCode 643 (Easy) | The fixed window. The slicing version is `O(n × k)` and passes; the running-total version is `O(n)`. Write the slow one first, then fix it, and say what changed. |
| 3 | Reverse String | LeetCode 344 (Easy) | Two pointers from the ends. `while left < right`, and the loop naturally handles both odd and even lengths without a special case. |
| 4 | Remove Element | LeetCode 27 (Easy) | The trap from §7 — deleting while iterating forwards. Write the `remove()`-in-a-loop version, watch it skip elements, then write the write-pointer version. |

### On problem 2, do this properly

- Write it with `sum(nums[i:i+k])` inside the loop. Submit it. Note the runtime.
- Work out the complexity: `n` up to 10⁵ and `k` up to `n` means how many operations?
- Rewrite with a running total: add `nums[i]`, subtract `nums[i - k]`.
- Submit again and compare the runtimes.
- Then answer out loud: **why does the running total not work for a sliding-window
  maximum?**

### The bounds drill

Answer these six from memory, with the arithmetic, in under ninety seconds:

- The body touches `items[i]`. What is the bound, and how many iterations for `n = 7`?
- The body touches `items[i + 1]`. Same two questions.
- The body touches `items[i + 2]`. Same two questions.
- A window of `k = 4` over `n = 10`. How many windows, and where does the last one start?
- Walking backwards over `n = 7` — write the `range(...)` exactly.
- Two pointers from the ends of `n = 7`. How many iterations before they meet?

### The trap drill

Type this and predict the output **before** running it:

```python
items = [1, 2, 2, 3, 2, 4]
for x in items:
    if x == 2:
        items.remove(x)
print(items)
```

Then explain, in one sentence, why one `2` survived. Then write two versions that give the
right answer — one that builds a new list, one that walks backwards — and say what each costs
in space.

### The latency drill

Say these from memory, in under a minute:

- Main memory reference, in nanoseconds.
- SSD random read, in microseconds.
- Round trip within a data centre, in milliseconds.
- Round trip across the world, in milliseconds.
- 1 Gbps, converted to megabytes per second.
- How many requests per second a million requests a day works out to.

Then use them: a request has a 40 ms user network leg, a 1 ms parse, a 5 ms database query
and a 2 ms render. What is the total, which leg dominates, and what single change would help
most?

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before you write each read loop, say out loud: "this holds one line" or "this holds the whole file".

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Write a program that creates `shopping.txt` with five lines, one item per line, then reads it back and prints each line with its number. Then append a sixth item and print only the last line, without reading the earlier five into a list. | Can you write, read, and append in each language, and does the file get closed on every path? |
| 2 | Write `wc` in miniature: read standard input to the end and print the number of lines, words, and characters. Run it three ways: typing lines by hand and ending with Ctrl+D or Ctrl+Z, with `< shopping.txt`, and with the output of another program piped in. Then try a larger text file with the same maximum line length. Explain why retained input memory depends on the longest line, not the total file size; check Go Scanner errors and its token-size limit. | Do you know the standard-input loop in each language, and have you seen with your own eyes that it does not care what is upstream? |
| 3 | Write a program that copies `in.txt` to `out.txt` while turning every line to upper case, and reports how many lines it copied. Make it fail cleanly with a clear message when `in.txt` is missing, in each language's style: exception, error value, stream check. Then, in each language, deliberately break the closing: drop the `with`, drop the `defer` or the `Flush`, or write with `std::endl` in a loop over a million lines and time it. | Can you stream from one file to another, handle the missing file the native way, and have you felt each language's closing and buffering trap? |

**Exercise 1, what you should notice.** Python `with` and `"a"` mode, Go `os.OpenFile` with `os.O_APPEND|os.O_WRONLY` plus `defer f.Close()`; do not use `os.Create` to append, because it truncates an existing file, C++ `std::ios::app` and no close at all. To print only the last line, keep one variable that each loop iteration overwrites.

**Exercise 2, what you should notice.** `for line in sys.stdin`, `bufio.NewScanner(os.Stdin)`, `while (std::getline(std::cin, line))`. Characters are a byte count in Go and C++ and a code-point count in Python, which is day 3 again; say so in your output.

**Exercise 3, what you should notice.** Missing file: Python's `FileNotFoundError`, Go's `open in.txt: no such file or directory` from `os.Open`, C++'s `if (!in)` which you must remember to write. The broken closings: Python without `with` may leave `out.txt` short if the program dies; Go without `Flush` can lose the final buffered bytes; C++ with `std::endl` finishes but noticeably slower than `'\n'`.

## Compare

- **Python** — open, with, read/write, pathlib, and sys.stdin. `with` closes on every path, iterating the file object streams one line with its newline attached, and a missing file raises.
- **Go** — os.Open, bufio.Scanner, io.Reader and io.Writer. `defer f.Close()` closes at function exit, the scanner streams one line without its newline and needs `Err()` checked, and a missing file is an error you cannot take the file without.
- **C++** — std::ifstream, std::ofstream, std::cin, std::cout, and buffering. The destructor closes with no line of code, `getline` streams one line without its newline, and a missing file is a silent flag you must test with `if (!in)`.

## Say these out loud

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Iterate over every adjacent pair in the array.*
   State the bound and its reason before writing it. Give the pair count for `n = 7`. Say what
   happens for an empty list without adding a guard.

2. *Roughly how long is a network round trip to a data centre on another continent?*
   Give the range, then the physics, then the neighbouring numbers, then the design
   consequence.

3. *Our p99 is 200 ms and our p50 is 20 ms. Is that a problem?*
   Do the fan-out multiplication out loud, then say what you would investigate, then name two
   techniques that limit the damage.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. How do you read a file that is bigger than memory?
2. In each language, what guarantees the file gets closed, and what happens to unwritten data if the program crashes first?
3. What does each language do when the file you try to open does not exist, and which of the three lets you not notice?

## Before you move on

- [ ] I derive loop bounds from the largest index the body touches, not from memory.
- [ ] I can say why `n` items have `n − 1` adjacent pairs, and why a window of `k` gives
      `n − k + 1`.
- [ ] I know the three reasons to iterate backwards.
- [ ] I never delete from a list while iterating forwards over it.
- [ ] I can quote seven latency numbers cold and use them to size a request in legs.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
