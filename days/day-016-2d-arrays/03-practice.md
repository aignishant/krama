---
day: 16
track: practice
title: "Practice — 2D arrays and matrix traversal"
status: written
---

# Day 016 · Practice

**DSA topic:** 2D arrays and matrix traversal
**System design topic:** REST, properly

---

## Code these, in this order

Four problems that all reduce to *visit each cell once, in the right order*. None of them needs a
clever idea. All of them punish sloppy handling of the two numbers, which is exactly the skill being
built.

Before each one, say out loud:

1. What do `r` and `c` mean, and what are their ranges?
2. Is the matrix square, or `m × n`? Which sizes do I need, and where do I compute them?
3. What happens on `[]` and on `[[]]`?
4. Am I reading, or writing? If writing, am I allowed a new matrix?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Richest Customer Wealth | LeetCode 1672 (Easy) | The bare row walk, and whether you reach for `sum(row)` instead of indexing by hand. Two minutes. |
| 2 | Transpose Matrix | LeetCode 867 (Easy) | That the output is `n × m` when the input is `m × n`. Write it with explicit loops first, then with `zip(*matrix)`, and be able to explain the second. |
| 3 | Diagonal Traverse | LeetCode 498 (Medium) | `r + c` is constant on an anti-diagonal. The zigzag is a separate, easier concern — solve them in that order or you will tangle them. |
| 4 | Matrix Diagonal Sum | LeetCode 1572 (Easy) | Both diagonals at once, and the odd-size trap: on an odd `n × n` the centre cell is on both diagonals and must not be counted twice. |

### On problem 1, then break it deliberately

Solve it, then change the input to a non-square matrix such as `[[1, 2, 3], [4, 5, 6]]` and confirm
your code still works. Then write the version with `len(matrix)` used for both sizes and run it. Read
the traceback. That is the error you will see under pressure, and recognising it in one second is
worth having.

### On problem 3, do it in two passes of your own

- **First**, just group. Return the list of anti-diagonals, top to bottom, and check them by eye
  against the picture in §4 of the lesson. On `[[1,2,3],[4,5,6],[7,8,9]]` you want
  `[[1], [2,4], [3,5,7], [6,8], [9]]`.
- **Then** add the zigzag, and confirm you get `[1, 2, 4, 7, 5, 3, 6, 8, 9]`.

Only after both pass, try the `O(1)`-extra-space version that walks each diagonal directly with a
moving row and column. Work out the range of `r` for diagonal `s` before writing any code — it is
`max(0, s - cols + 1)` to `min(s, rows - 1)` — and check that against `s = 0` and against the last
diagonal by hand.

### The aliasing drill

Predict the output of each, then run them.

```python
grid = [[0] * 3] * 4
grid[1][2] = 7
print(grid)
```

```python
grid = [[0] * 3 for _ in range(4)]
grid[1][2] = 7
print(grid)
```

```python
row = [0] * 3
grid = [row, row, row]
grid[0][0] = 5
print(grid)
```

Then say, in one sentence, what `*` actually copies. If you cannot, re-read the aliasing trap in §7
before going on — this bug will find you again in the dynamic programming phase, where the table is
always a grid you built with one of these two lines.

### The notation drill

Take `[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]` and answer these without running anything:

1. What is `matrix[3][1]`?
2. What is `len(matrix)`, and what is `len(matrix[0])`?
3. Which cells have `r + c == 3`?
4. Which cells have `r - c == 1`?
5. How many anti-diagonals are there, and what is the longest one?
6. What does `matrix[-1][-1]` give you, and why does it not raise?

Check all six by running the code afterwards. Question 6 is the one that causes silent bugs.

### The REST drill

Design the API for a **library** — books, members, loans — with no help. Write out at least eight
lines in the form `METHOD /path → status`. Cover: listing books, filtering to only the available
ones, borrowing a book, returning it, seeing one member's current loans, and what happens when
somebody tries to borrow a book that is already out.

Then check your own design against these five questions:

1. Is there a verb anywhere in a path? If yes, can it be replaced by a method, or is it a genuine
   action that deserves a sub-resource?
2. Are your collections plural, and consistent?
3. Did filtering go in the query string rather than into a new path?
4. Which of your calls are idempotent? Is the borrow call safe to retry after a timeout?
5. What status code does a borrow return when the book is already lent out — and why is it `409` and
   not `400`?

### The critique drill

Say what is wrong with each of these, in one sentence, out loud:

```
POST /api/getUserById            {"id": 42}
GET  /users/42/delete
POST /orders                     → 200 OK, {"error": "out of stock"}
GET  /orders?page=200000&per_page=50
PUT  /users/42                   {"email": "new@example.com"}     # the user has 12 fields
GET  /getAllOrdersForUserSortedByDateDescending?u=42
```

Each one breaks a different rule from the lesson. Name the rule, not just the symptom.

### The constraints drill

Name all six REST constraints from memory, in under sixty seconds, and after each one say in a
single sentence what you would lose without it. Then say which one almost nobody implements, and
name one API that partly does.

Mark each as **said it / knew it but could not say it / did not know it**. Only the first counts.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Print the matrix diagonally.*
   Fix your notation first, then ask whether it is square. State the identity — `r + c` is constant
   along an anti-diagonal — before you write a line of code, because that is the whole answer. Then
   the grouping loop, then the zigzag as a separate step, then `O(m × n)` time and `O(m × n)` extra
   space with the `O(1)` alternative named.

2. *What makes an API RESTful?*
   Style not technology. Uniform interface first, statelessness second, then cacheable, layered,
   client-server, code-on-demand. Finish with the honest line about HATEOAS and Richardson level 2.
   Ninety seconds, then stop.

3. *Why is walking a matrix by row faster than walking the same matrix by column, when both are
   O(m × n)?*
   Give the memory-layout reason, then the latency ladder from
   [day 010](../day-010-traversal-patterns/README.md), then the one-line conclusion: complexity
   counts operations, hardware counts cache misses, and the two can differ by a factor of several
   without either being wrong.

---

## Before you move on

- [ ] I say what `r` and `c` mean before writing any matrix loop.
- [ ] I compute `rows` and `cols` into named variables, and I never use `len(matrix)` for both.
- [ ] I test matrix code on a non-square input, always.
- [ ] I never write `[[0] * cols] * rows`, and I can say exactly what goes wrong when I do.
- [ ] I know `r + c` is constant on an anti-diagonal and `r - c` on the main-direction diagonal.
- [ ] I can name the six REST constraints and say which one is not implemented in practice.
- [ ] I can look at any endpoint and say whether the path is a noun and the method is right.
- [ ] I can redraw the collection-versus-item diagram from memory, in whatever tool I like.
