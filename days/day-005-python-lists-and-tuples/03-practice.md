---
day: 5
track: practice
title: "Practice — Python for DSA I: lists, tuples, and slicing"
status: written
---

# Day 005 · Practice

**DSA topic:** Python for DSA I: lists, tuples, and slicing
**System design topic:** HTTP: the request and the response

---

## Code these, in this order

Four problems that all reward knowing where a list is cheap and where it is not. Each one
has an obvious solution that touches the front of a list, and a better one that does not.

For each problem:

1. Solve it however comes naturally.
2. Then go back and put a finger on every list operation you used. Say its cost out loud.
3. If any `O(n)` operation is sitting inside a loop, rewrite it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove Element | LeetCode 27 (Easy) | The tempting solution is `remove()` or `pop(i)` in a loop, which is `O(n²)`. The write-pointer version is `O(n)` and touches nothing but the end. |
| 2 | Move Zeroes | LeetCode 283 (Easy) | Same trap, sharper. `pop(i)` then `append(0)` is quadratic; two indices walking forward is linear. This is the shape of [day 015](../day-015-the-write-pointer/README.md). |
| 3 | Implement Queue using Stacks | LeetCode 232 (Easy) | Forces you to think about which end of a list is cheap. `pop()` is free, `pop(0)` is not, and the whole problem exists because of that asymmetry. |
| 4 | Rotate Array | LeetCode 189 (Medium) | The one-line slice solution works and allocates a full copy. The reversal trick does it in `O(1)` extra space. Write both and say what each costs in memory. |

### On problem 1, do this properly

- Write the version that calls `items.remove(val)` inside a `while` loop.
- Time it on a list of 50,000 elements where every element is the target.
- Now write the write-pointer version, and time that.
- The ratio should be in the hundreds. Say which line was the hidden `O(n)`.

### The measurement drill

Run the complete program from §5 of the lesson at `N = 50_000`, then again at `N = 100_000`.

For each row, look at what the time did when the input doubled:

- Rows that roughly **doubled** are `O(n)`.
- Rows that roughly **quadrupled** are `O(n²)`.

Name the shape of every row from the ratio alone, before checking it against the lesson.
Then answer one question out loud: **which single method name is the difference between the
two groups?**

### The one to try in a terminal

```
curl -v https://httpbin.org/get
```

Read the lines starting with `>` — that is your actual request. Read the lines starting with
`<` — that is the actual response. Find the request line, four headers, the blank line and
the status code. Then run it again with `-X POST -H "Content-Type: application/json" -d
'{"a":1}'` and see what changed.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *What is the complexity of inserting at the front of a Python list?*
   Give the answer, then the reason from the memory layout, then why `append` is different,
   then what "amortised" means, then what you would use instead if you needed a queue.

2. *Describe an HTTP request. What is in the headers, and what is in the body?*
   Name the four parts in order. Get to safe and idempotent without being asked.

3. *A payment POST times out and the client does not know whether it succeeded. What do you
   do?*
   One sentence on why `POST` is the hard case, one on idempotency keys, one on what the
   server stores.

---

## Before you move on

- [ ] I can give the cost of `append`, `pop()`, `insert(0, x)`, `pop(0)`, `items[i]` and
      `items[a:b]` from memory.
- [ ] I can say what "amortised O(1)" means in one sentence, with the reason.
- [ ] I know why `[[0] * 3] * 3` is a bug and what to write instead.
- [ ] I can write out a full HTTP request by hand — request line, four headers, blank line,
      body — and label every part.
- [ ] I can say the difference between 401 and 403, and between PUT and PATCH.
