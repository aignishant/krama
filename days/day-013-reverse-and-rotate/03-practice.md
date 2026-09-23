---
day: 13
track: practice
title: "Practice — Reversing, rotating, and swapping in place"
status: written
---

# Day 013 · Practice

**DSA topic:** Reversing, rotating, and swapping in place
**System design topic:** Containers and why everyone uses Docker

---

## Code these, in this order

Four problems built from the same two moves: swap two positions, and walk two markers towards
each other. Three of them are the reversal trick in different clothes.

Before you write anything, for each one:

1. Say whether the function must **mutate** its input or **return** a new one. If it mutates,
   remember that `items = ...` will not work.
2. Say what happens when the input is empty, and when it has one element.
3. If there is a `k`, say what happens when `k` is `0`, when `k == n`, and when `k > n`.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse String | LeetCode 344 (Easy) | The two-pointer loop, and the bound. `while left < right`, `n // 2` swaps. Write it once and never get it wrong again. |
| 2 | Rotate String | LeetCode 796 (Easy) | Whether you understand what a rotation *is*. There is a one-line answer using `s + s`, and finding it is the point. |
| 3 | Rotate Array | LeetCode 189 (Medium) | Today's question, exactly as an interviewer asks it. Do it three ways — extra array, one-at-a-time, three reversals — and time all three. |
| 4 | Reverse Words in a String | LeetCode 151 (Medium) | The three-reversal idea again: reverse everything, then reverse each word. Also a lesson in messy input — leading, trailing and repeated spaces. |

### On problem 3, do it properly

- Write the slice version first. Submit it. It passes.
- Then re-read the constraint: *"Could you do it in-place with O(1) extra space?"* Write that
  one too.
- Then answer, out loud: **why do three reversals produce a rotation?** If you cannot say it in
  two sentences without looking, you have memorised the code and not the idea.
- Then run both on a list of a million elements and time them. Notice that the version you were
  asked for is the slower of the two, and be able to say why that is still the right answer.

### On problem 4, notice the shape

`"  the sky   is blue  "` must come out as `"blue is sky the"`. Solve it twice:

- **The easy way:** `" ".join(reversed(s.split()))`. Correct, `O(n)`, and `O(n)` space.
- **The interview way:** strip and squash the spaces in place, reverse the whole thing, then
  reverse each word. This is the same three-reversal skeleton as problem 3, and the reason
  interviewers like it is that the second reversal is over a variable-length group.

### The swap drill

Answer these in your head, then check:

1. `a, b = b, a` — why does this work without a temporary variable, and what would you write in
   Java?
2. Reversing a 9-element list: how many swaps, and which position never moves?
3. Reversing a 10-element list: how many swaps?
4. `items[i], items[j] = items[j], items[i]` when `i == j` — what happens?

### The rotation drill

For `[1, 2, 3, 4, 5, 6, 7, 8]`, say the answer out loud before working it out:

1. Rotate right by 3.
2. Rotate left by 3.
3. Rotate right by 8.
4. Rotate right by 11.
5. Rotate right by −3. (What does Python's `%` do here, and what would Java do?)

Then, for each of those, say what `k % n` becomes.

### The in-place drill

Predict the output before running it:

```python
def rotate(items, k):
    k %= len(items)
    items = items[-k:] + items[:-k]

data = [1, 2, 3, 4, 5]
rotate(data, 2)
print(data)
```

Then fix it with a one-character change, and say in one sentence what the difference is between
`items = ...` and `items[:] = ...`.

### The one to try in a terminal

If Docker is installed, run these four and read the output rather than skipping past it:

```
docker run --rm -it alpine sh -c "ps aux"
docker run --rm alpine uname -r
uname -r
docker run --rm --memory=32m python:3.12-slim python -c "x = ' ' * 100_000_000"
```

Then answer: how many processes did the first one see, and why? Why do the second and third
print the same thing? And what killed the fourth — and which of namespaces or cgroups was
responsible for each of those three answers?

If Docker is not installed, answer them from the lesson instead. They are the whole of §3.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Rotate the array to the right by k, in O(1) extra space.*
   Say the constraint back, reject the two naive versions with numbers, give the three
   reversals, and then **explain why they work** without being asked.

2. *What problem does Docker actually solve?*
   Give both problems — packaging and density. Define a container as a process, name namespaces
   and cgroups, and land the two numbers: 100 ms against 45 s, and a few MB against a gigabyte.

3. *What is the difference between a container and a virtual machine?*
   Answer with one structural fact — the shared kernel — and then derive start time, memory,
   density and the Windows-on-Linux question from it. Finish on the trade-off: the shared kernel
   is also the weakness.

---

## Before you move on

- [ ] I can write the two-pointer reversal from memory, with the right bound, first time.
- [ ] I say `k %= n` before anything else, and I know why the empty check comes before it.
- [ ] I can explain the three-reversal trick in two sentences, out loud, with no notes.
- [ ] I know that `items = ...` inside a function changes nothing for the caller.
- [ ] I can name namespaces and cgroups and say which one limits *seeing* and which limits
      *using*.
- [ ] I can draw the VM stack against the container stack — in any tool I like — and point at
      the one box that is missing.
