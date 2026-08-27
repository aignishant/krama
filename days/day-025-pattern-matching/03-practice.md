---
day: 25
track: practice
title: "Practice — Pattern matching, the simple way"
status: written
---

# Day 025 · Practice

**DSA topic:** Pattern matching, the simple way
**System design topic:** What a database gives you that a file does not

---

## Code these, in this order

Four problems where a short pattern is checked against a long one. The code is never more than a
dozen lines; the marks are in the boundaries and in what you can say about the cost.

Before each one, ask:

1. What are `n` and `m`, and what is the last valid starting position?
2. Does the bound test come before the character comparison in my `while`?
3. What does the empty pattern do?
4. What input would make this hit its worst case?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find the Index of the First Occurrence in a String | LeetCode 28 (Easy) | `range(n - m + 1)`, resetting `k`, and whether you can state both costs with an example input for each. |
| 2 | Repeated Substring Pattern | LeetCode 459 (Easy) | Whether you spot the `(s + s)[1:-1].find(s) != -1` trick — and can explain *why* it works, which is the actual question. |
| 3 | Longest Common Prefix | LeetCode 14 (Easy) | Comparing many strings position by position, and stopping at the first disagreement. The empty-list case. |
| 4 | Implement strStr with KMP | LeetCode 28 again | Only after the naive version passes. Build the failure table by hand on `"aabaaac"` before writing any code. |

### On problem 1, measure it rather than guessing

Add a counter to your solution and run it on these two inputs:

```python
count_comparisons("a" * 1000 + "b", "a" * 10 + "b")
count_comparisons("the quick brown fox jumps over the lazy dog" * 10, "lazy dog")
```

You should get roughly `(990, 10901)` and `(35, 43)`. Then answer:

1. What is `n × m` for the first one, and how close did you get to it?
2. Why is the second one barely more than `n`?
3. Which of those two inputs would you show an interviewer, and why both?

### On problem 1, break it three ways

Run each and say what happens and why:

```python
# A — bound test after the comparison
while haystack[start + k] == needle[k] and k < m:
    k += 1
```

```python
# B — k declared outside the outer loop
k = 0
for start in range(n - m + 1):
    while k < m and haystack[start + k] == needle[k]:
        k += 1
```

```python
# C — wrong outer bound, with a slice comparison
for start in range(n):
    if haystack[start:start + m] == needle:
        return start
```

A raises. B gives confident wrong answers. C silently misses a match at the very end — construct the
input that proves it.

### On problem 2, explain before you accept

`(s + s)[1:-1].find(s) != -1` decides whether `s` is a whole number of repeats of some shorter
string. Do not use it until you can say why it works, in two sentences, out loud.

Hint to work from: if `s` is `k` copies of a block, then `s + s` is `2k` copies, and `s` must appear
starting somewhere in the middle. The `[1:-1]` exists to stop it matching at position 0.

Then write the honest version — try every divisor length of `n`, check whether repeating that prefix
rebuilds `s` — and say which you would present first in an interview and why.

### The timing drill

```python
import time
haystack = "a" * 200_000 + "b"
needle = "a" * 1_000 + "b"

start = time.perf_counter(); str_str(haystack, needle); naive = time.perf_counter() - start
start = time.perf_counter(); haystack.find(needle);     lib   = time.perf_counter() - start
print(naive, lib, naive / lib)
```

Expect roughly 14 seconds against 0.0006 seconds. Then answer:

1. How much of that gap is a better algorithm and how much is C versus Python? Argue it.
2. What would KMP do on this input, in comparisons?
3. What is the right sentence to say in an interview about `find`?

### The KMP table drill

Before coding anything, build the failure table for `"aabaaac"` by hand. For each prefix, the value
is the length of the longest proper prefix of that prefix which is also a suffix of it.

```
prefix:   a   aa  aab aaba aabaa aabaaa aabaaac
value:    ?   ?   ?   ?    ?     ?      ?
```

Then say, in one sentence, how that table is used: when a mismatch happens after matching `j`
characters, what does the algorithm do instead of restarting?

If you can do the table and say that sentence, you can answer the follow-up in an interview without
writing KMP at all — which is the point.

### The naming drill

For each situation, name the algorithm and say why in one sentence:

1. One needle, one haystack, ordinary English text.
2. One needle, one haystack, both highly repetitive (DNA).
3. A thousand different needles, one haystack, all the same length.
4. A thousand needles of different lengths, one haystack, streaming.
5. A very long needle in a very long haystack, large alphabet.

Numbers 3 and 4 have different answers, and the difference is worth knowing.

### The database drill

Answer each in one or two sentences, out loud:

1. Name the four things a database gives you that a file does not.
2. Two processes read a JSON file, each add a record, each write it back. What happens, and what is it
   called?
3. Why does a crash halfway through writing a file lose *everything*, not just the last change?
4. What is a write-ahead log, and what two other features does it also enable?
5. Ten million records at 200 bytes — how long to find one by scanning, and how long with an index?
6. Give three constraints a database enforces that a file cannot.
7. Name three situations where a file is genuinely the better choice.
8. What is SQLite, and why is it the answer nobody gives?
9. What does an index cost you?

Number 8 is the one that makes you sound like you have built things.

### The arithmetic drill

From memory, in under two minutes:

- 10M records at 200 bytes — total size, seconds to read from SSD, seconds to parse as JSON.
- The same lookup through a B-tree with a fanout of 500 — how many levels, how many page reads?
- 2 GB of JSON parsed into objects — how much RAM, roughly, and why the multiplier?
- 100 writes a second with a 50 ms read-modify-write cycle — how many lost updates per second, and per
  eight-hour day?
- Random 8 KB writes versus sequential writes on SSD — the two throughput figures, and why the WAL
  exploits the gap.

### The "why not a file" drill

For each, say **file** or **database**, and give the deciding reason in one sentence:

1. Application configuration read at start-up.
2. A user's uploaded profile photograph.
3. Which users are currently logged in.
4. A list of 400 customers, edited by two people.
5. Server access logs.
6. Product catalogue for a shop with 50,000 items and a search box.
7. Local state for a command-line tool.
8. A record of every money transfer.

At least three of those are files. If you said "database" to all eight, re-read §7 of the lesson.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement strStr: find the first occurrence of a needle in a haystack.*
   Contract questions first. Then the two loops, saying the `n - m + 1` bound and the short-circuit
   ordering as you write them. Then both costs with an input for each. Then `find` exists, and then
   KMP in one sentence.

2. *Why not just store the data in a JSON file?*
   Four things, concurrency first because it is the one people underestimate. Give the lost-update
   sequence, the truncation problem, the 24-seconds-versus-0.4-milliseconds number, and one integrity
   example. Then give the other side unprompted — configuration, static assets, append-only logs, and
   SQLite.

3. *Can you do better than O(n·m)?*
   KMP, and the reason: the naive version discards what it just learned, but it knows which prefix of
   the needle matched, so a precomputed table lets it slide forward without moving the haystack index
   backwards. `O(n + m)` time, `O(m)` space. Then say you would describe it rather than improvise it.

---

## Before you move on

- [ ] I write `range(n - m + 1)` and can derive it on a small example.
- [ ] I put the bound test first in the `while` and can say why.
- [ ] I reset the inner index at every starting position, and know that is what KMP avoids.
- [ ] I can give both costs with a concrete input for each, not just the worst case.
- [ ] I can name KMP, Rabin-Karp and Boyer-Moore, with one sentence each.
- [ ] I do not attempt KMP from memory unless I have practised the table.
- [ ] I can name the four things a database gives me, leading with concurrency.
- [ ] I can describe a lost update as a sequence of four steps with no error message.
- [ ] I can name three cases where a file is right, and I remember SQLite exists.
