---
day: 11
track: practice
title: "Practice — Insert, delete, and the cost of the middle"
status: written
---

# Day 011 · Practice

**DSA topic:** Insert, delete, and the cost of the middle
**System design topic:** The operating system's job

---

## Code these, in this order

Four problems that are all deletion in disguise. Every one of them has a natural solution that
calls `remove` or `pop(i)` inside a loop and is quadratic, and a one-pass solution that is
linear.

For each problem:

1. Say how many elements move for a single deletion at position `i`.
2. Say what happens if you do that `k` times.
3. Ask the two questions that change the answer: **does order matter**, and **may I modify the
   input?**
4. Then write the one-pass version.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove Element | LeetCode 27 (Easy) | Order does **not** matter here, which the statement says explicitly. So both the write-pointer solution and the swap-with-last solution are valid — write both and compare. |
| 2 | Remove Duplicates from Sorted Array | LeetCode 26 (Easy) | Order **does** matter, so swap-with-last is out. Pure write pointer, and the return value is a length rather than a list. |
| 3 | Remove Duplicates from Sorted Array II | LeetCode 80 (Medium) | The same pattern with a count. The whole difficulty is deciding what the write pointer compares against — and the answer is `items[write - 2]`, not the previous element. |
| 4 | Merge Sorted Array | LeetCode 88 (Easy) | The direction trap from §7. Merging forwards overwrites data you still need; merging **from the end backwards** does not. This is the same rule as shifting right. |

### On problem 1, do this properly

- Write the version that calls `items.remove(val)` in a `while` loop. Time it on 50,000
  elements where every element is the target.
- Write the write-pointer version. Time it.
- Write the swap-with-last version. Time it.
- Then answer: which two produce the same array, and which one is only valid because the
  problem says order does not matter?

### The cost drill

Answer these six from memory, with the arithmetic, in under ninety seconds:

- Delete position 3 from an array of 20. How many elements move?
- Delete the last element of an array of 20. How many move?
- Insert at position 0 of an array of 20. How many move?
- Delete 5,000 elements one at a time from a list of 20,000. Roughly how many operations?
- Do the same with a write pointer. How many?
- When is deletion `O(1)`, and what is the condition?

### The direction drill

Type this and predict the output before running it:

```python
row = ["A", "B", "C", "D", "E"]
row.append(None)
for j in range(1, len(row) - 1):
    row[j + 1] = row[j]
row[1] = "X"
print(row)
```

Then explain in one sentence why `C`, `D` and `E` disappeared, and rewrite the loop so it
works. Then state the general rule about which end to start from.

### The one to try in a terminal

```
strace -c python3 -c "open('/etc/hostname').read()"
```

(On macOS, `dtruss`; on Windows, run it in WSL.) Look at the list of system calls your
three-word program actually made. Count them. Then run it with the file read one byte at a
time and count again.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *What is the cost of deleting an element from the middle of an array?*
   Give the exact count first, then the range from front to back, then why the hole cannot
   stay, then the `O(1)` version and its condition.

2. *What does the operating system do when your program asks to read a file?*
   Walk the path: syscall, mode switch, permission check, page cache hit or miss, blocking,
   interrupt, copy, return. Then give the buffering consequence.

3. *Why is buffered I/O faster than unbuffered?*
   Do the multiplication out loud for a 1 MB file at one byte and at 4 KB, and say what the
   ratio between a system call and a function call is.

---

## Before you move on

- [ ] I can say `n − i − 1` and `n − i` and explain which is which.
- [ ] I ask "does order matter?" before writing any deletion code.
- [ ] I never call `remove` or `pop(i)` inside a loop over the same list.
- [ ] I know which direction to shift when inserting, and why the other direction corrupts
      data.
- [ ] I can name the four jobs of the operating system and say what a system call costs.
