---
day: 16
track: dsa
title: "2D arrays and matrix traversal"
phase: "Arrays"
status: written
---

# Day 016 · DSA — 2D arrays and matrix traversal

**After today you can:** You can walk a matrix by row, by column and by diagonal without index confusion.

**The interviewer asks it as:** *Print the matrix diagonally.*

---

## 1. What this is, and why they ask it

A **matrix** is a rectangle of values addressed by two numbers instead of one: which row, then
which column. In Python it is a list whose elements are themselves lists, and you reach a single
value with `matrix[row][column]` — row first, always. Everything else today is about walking that
rectangle in the four orders an interviewer will ask for: along the rows, down the columns, along
the diagonals that run top-left to bottom-right, and along the diagonals that run the other way.

Nothing here is conceptually hard. The reason it fills whiteboards with wrong code is that the two
numbers are easy to swap and the boundaries are easy to get off by one, and unlike a one-
dimensional array you cannot hold the whole thing in your head. The candidates who do well are the
ones who write down what `r` and `c` mean before they write a loop, and who know the two identities
in §3 by heart.

It shows up directly as *print the matrix in diagonal order* (LeetCode 498) and *rotate the image*
(LeetCode 48, which is tomorrow), and indirectly as the substrate for a great deal of the course
still to come. Grid problems in graphs — flood fill, number of islands, shortest path in a maze on
[days 125–142](../day-125-what-a-graph-is/README.md) — are matrix traversal with a queue attached.
Dynamic programming tables from [day 143](../day-143-what-dp-is/README.md) onwards are
matrices you fill in a particular order. Getting fluent with `matrix[r][c]` now pays for twelve
weeks.

---

## 2. The story

Iqbal is tiling a bathroom floor in a flat in Bhopal, and the owner has been standing in the
doorway since nine o'clock. It is not a big room. Twelve tiles from the door wall to the far wall,
nine tiles across, and Iqbal has counted it twice because the tiles came in one box and there is
no second box.

He works from the far corner backwards, because you cannot stand on what you have just laid. One
line across, then the next line, then the next. He puts little plastic crosses between them so the
gaps stay even. Halfway through the fourth line the owner asks him something and Iqbal answers
without looking up, because by now he can name any spot on that floor with two numbers: how many
lines in from the far wall, and how many tiles along from the left.

Then the owner's wife comes and looks at it and says she wants the dark tiles — there are twenty
spare, a different colour — to run corner to corner.

Iqbal stops with a tile in his hand and works it out, and this is the bit worth watching. In the
first line, the dark one is the first tile along. In the second line it is the second tile along.
Third line, third tile. Each line, it moves one further from the left, exactly as it moves one
further from the wall. So he does not have to measure anything: he just counts one more each time.

Then she says she wants a second dark line, the other way, crossing it. So he starts at the other
end. First line, ninth tile along. Second line, eighth. Third line, seventh. One further from the
wall, one *back* towards the left. And Iqbal notices something that makes it easy: on that second
line, if you add the two numbers together — how many lines in, how many tiles along — you get ten
every single time. First line and ninth tile, ten. Second and eighth, ten. He stops counting
backwards and just checks the two numbers add up to ten.

He finishes at half past four, and the crosses come out the next morning.

---

## 3. The idea in plain English

Iqbal's floor is a **matrix**: a rectangle of values where every position needs two numbers to name
it. His "how many lines in" is the **row**, and his "how many tiles along" is the **column**.

### How Python stores it

Python has no separate matrix type in the standard library. A matrix is a **list of lists**: the
outer list holds the rows, and each row is itself a list holding that row's values.

```python
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          [10, 11, 12]]
```

Four rows, three columns. `matrix[2]` is the whole third row, `[7, 8, 9]`. `matrix[2][1]` is the
value in the third row, second column: `8`.

**Row first, then column. Always.** Say it out loud once now, because half the bugs in this topic
are the two numbers the wrong way round, and there is no error message when the matrix is square.

### The two sizes, and why you need both

```python
rows = len(matrix)          # 4 — how many rows
cols = len(matrix[0])       # 3 — how long a row is
```

`len(matrix)` counts the outer list, which is the number of rows. `len(matrix[0])` looks inside the
first row and counts it, giving the number of columns. Beginners write `len(matrix)` for both,
which works perfectly on a square matrix and fails on every other one. Interviewers hand you a
`3 × 5` on purpose.

Both lines fail on an empty matrix, and `len(matrix[0])` fails on `[[]]`, so real code starts with
a guard. §7 has the exact error.

### Walking it by row

```python
for r in range(rows):
    for c in range(cols):
        print(matrix[r][c])
```

The outer loop picks a row and holds it still; the inner loop sweeps across that row. This is
**row-major order**, and it prints `1 2 3 4 5 6 ...`. It is Iqbal laying one line across before
starting the next.

Row-major is also the order the values physically sit near each other in memory, which — from
[day 009](../day-009-what-an-array-is/README.md) and
[day 010](../day-010-traversal-patterns/README.md) — is the order the machine likes. Walking a big
matrix by row is measurably faster than walking the same matrix by column, and it is a good
sentence to have ready.

### Walking it by column

Swap which loop is on the outside. Nothing else changes.

```python
for c in range(cols):
    for r in range(rows):
        print(matrix[r][c])
```

This prints `1 4 7 10 2 5 8 11 ...` — straight down the first column, then down the second. Notice
that `matrix[r][c]` is written exactly the same way in both versions. **What changed is which
number is held still, not the order you write them in.** This is the single most common source of
confusion in the topic and it is worth staring at until it is obvious.

### The two diagonal families

Here is where Iqbal earns his keep, and here are the only two facts you need.

**A diagonal going down-right** — the direction of the first dark line — moves one row down and one
column right at each step. So `r` goes up by one and `c` goes up by one, which means **`r - c`
never changes** along that diagonal.

**A diagonal going down-left** — the second dark line, the crossing one — moves one row down and one
column *left*. So `r` goes up by one and `c` goes down by one, which means **`r + c` never
changes**. That is Iqbal's "they always add up to ten".

That gives you a way to group every cell into diagonals without any clever index arithmetic at all:

- To collect the down-right diagonals, group cells by the value of `r - c`.
- To collect the down-left diagonals — usually called the **anti-diagonals** — group cells by the
  value of `r + c`.

For a matrix with `rows` rows and `cols` columns there are exactly `rows + cols - 1` diagonals in
each family. On a `4 × 3` matrix that is `4 + 3 - 1 = 6`, and their sizes go 1, 2, 3, 3, 2, 1.

`r - c` can be negative — it runs from `-(cols - 1)` up to `rows - 1` — which is why grouping into
a dictionary is easier than allocating a list and shifting everything. `r + c` runs from `0` to
`rows + cols - 2`, which is nice and simple, so most "diagonal" interview problems are stated in
terms of the anti-diagonals.

### The one habit that prevents most bugs

Before writing any loop, say what your two variables mean, in words:

> `r` is which row I am on, from 0 to `rows - 1`. `c` is which column I am on, from 0 to
> `cols - 1`. The value is `matrix[r][c]`.

Then never write `matrix[c][r]` by accident, because you know what the letters mean.

---

## 4. The picture

The `4 × 3` matrix, with both numbers marked:

```
                 c=0   c=1   c=2
               +-----+-----+-----+
         r=0   |  1  |  2  |  3  |
               +-----+-----+-----+
         r=1   |  4  |  5  |  6  |
               +-----+-----+-----+
         r=2   |  7  |  8  |  9  |
               +-----+-----+-----+
         r=3   | 10  | 11  | 12  |
               +-----+-----+-----+

   matrix[2][1] is 8   —   row 2, column 1. Row first.
```

Now the same rectangle with `r + c` written in each cell instead of the value:

```
                 c=0   c=1   c=2
               +-----+-----+-----+
         r=0   |  0  |  1  |  2  |
               +-----+-----+-----+
         r=1   |  1  |  2  |  3  |
               +-----+-----+-----+
         r=2   |  2  |  3  |  4  |
               +-----+-----+-----+
         r=3   |  3  |  4  |  5  |
               +-----+-----+-----+
```

**What to notice:** every cell holding the same number lies on one straight line running from
top-right to bottom-left. The 2s are `[3, 5, 7]`. The 3s are `[6, 8, 10]`. Six distinct values, 0
through 5, so six anti-diagonals — which is `rows + cols - 1 = 4 + 3 - 1`.

And with `r - c` in each cell:

```
                 c=0   c=1   c=2
               +-----+-----+-----+
         r=0   |  0  | -1  | -2  |
               +-----+-----+-----+
         r=1   |  1  |  0  | -1  |
               +-----+-----+-----+
         r=2   |  2  |  1  |  0  |
               +-----+-----+-----+
         r=3   |  3  |  2  |  1  |
               +-----+-----+-----+
```

**What to notice:** the zeros run top-left to bottom-right — that is the main diagonal, `[1, 5, 9]`
— and the values go negative above it. Six distinct values again, from `-2` to `3`.

Finally, the two loop orders side by side. Same `matrix[r][c]`, different nesting:

```
  by row (row-major)              by column (column-major)
  1 -> 2 -> 3                     1     2     3
              |                   |     |     |
  4 -> 5 -> 6 |                   v     v     v
              |                   4     5     6
  7 -> 8 -> 9                     |     |     |
                                  v     v     v
                                  7     8     9

  visits: 1 2 3 4 5 6 7 8 9       visits: 1 4 7 2 5 8 3 6 9
```

**What to notice:** neither loop skips or repeats a cell. Both visit all nine exactly once. Only
the order differs — and only because of which `for` is on the outside.

---

## 5. The code, built step by step

### Reading the two sizes safely

```python
def size(matrix: list[list[int]]) -> tuple[int, int]:
    if not matrix or not matrix[0]:
        return 0, 0
    return len(matrix), len(matrix[0])
```

`not matrix` catches `[]`. `not matrix[0]` catches `[[]]` — a matrix with one row that has nothing
in it. Both are inputs graders actually send, and both crash the naive `len(matrix[0])`.

### Summing every row, and every column

```python
row_sums = [sum(row) for row in matrix]
```

Each element of the outer list *is* a row, so you can loop over rows directly without touching
indices at all. Prefer this when you do not need the position.

```python
col_sums = [sum(matrix[r][c] for r in range(rows)) for c in range(cols)]
```

Columns have no such shortcut, because a column is not stored anywhere — it is one value picked out
of each row. The `c` is fixed by the outer comprehension and `r` sweeps.

### Transposing: turning rows into columns

```python
transposed = [list(t) for t in zip(*matrix)]
```

`zip(*matrix)` is worth ten seconds. The `*` unpacks the outer list, so `zip` receives each row as
a separate argument, and `zip` then takes the first item of every row, then the second of every
row, and so on. Those groups are exactly the columns. On the `4 × 3` matrix above it gives
`[[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]` — a `3 × 4`.

Write the explicit version once so you know what it is doing:

```python
transposed = [[matrix[r][c] for r in range(rows)] for c in range(cols)]
```

In an interview, write `zip(*matrix)` and then say the two-line explanation. That combination —
the idiom plus proof you know why it works — reads much better than either alone.

### Grouping cells into diagonals

This is the whole trick of the day, and it is four lines.

```python
from collections import defaultdict

groups = defaultdict(list)
for r in range(rows):
    for c in range(cols):
        groups[r + c].append(matrix[r][c])
```

`defaultdict(list)` is a dictionary that creates an empty list the first time you touch a missing
key, so you never write `if key not in groups`. You met dictionaries on
[day 006](../day-006-python-strings-dicts-sets/README.md).

After this loop, `groups[0]` is `[1]`, `groups[1]` is `[2, 4]`, `groups[2]` is `[3, 5, 7]`, and so
on. Each list is one anti-diagonal, in top-to-bottom order, because the loops visit rows in
increasing order.

Change the key to `r - c` and you get the other family instead. That is the entire difference.

### Diagonal order: the zigzag

LeetCode 498 wants the anti-diagonals emitted in order, but alternating direction — the first one
upwards, the second downwards, and so on. Since each `groups[s]` is already in top-to-bottom order,
"upwards" is just that list reversed.

```python
out = []
for s in range(rows + cols - 1):
    band = groups[s]
    out.extend(reversed(band) if s % 2 == 0 else band)
```

`s % 2 == 0` picks the even-numbered diagonals to reverse, which matches the problem's rule that
the first diagonal goes up-and-right. `rows + cols - 1` is the diagonal count from §3, so this
loop touches every group exactly once and none twice.

### Visiting the four neighbours of a cell

Grid problems from [day 125](../day-125-what-a-graph-is/README.md) onwards all need this, and the
idiom is worth learning here where it is easy.

```python
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right

def neighbours(r: int, c: int, rows: int, cols: int) -> list[tuple[int, int]]:
    out = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:      # the bounds check
            out.append((nr, nc))
    return out
```

`0 <= nr < rows` is Python's chained comparison and reads exactly as it looks: `nr` is at least 0
and less than `rows`. Doing the check *before* touching `matrix[nr][nc]` is the habit. Negative
indices do not raise in Python — `matrix[-1]` is the last row — so an unchecked negative gives you
a wrong answer silently rather than a crash, which is much worse.

### The complete solutions

```python
from collections import defaultdict


def size(matrix: list[list[int]]) -> tuple[int, int]:
    """Rows and columns, safe on [] and [[]]."""
    if not matrix or not matrix[0]:
        return 0, 0
    return len(matrix), len(matrix[0])


def by_row(matrix: list[list[int]]) -> list[int]:
    """Row-major: left to right, top to bottom."""
    rows, cols = size(matrix)
    return [matrix[r][c] for r in range(rows) for c in range(cols)]


def by_column(matrix: list[list[int]]) -> list[int]:
    """Column-major: top to bottom, left to right. Same expression, loops swapped."""
    rows, cols = size(matrix)
    return [matrix[r][c] for c in range(cols) for r in range(rows)]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Rows become columns. Returns a new matrix; does not modify the input."""
    return [list(t) for t in zip(*matrix)]


def anti_diagonals(matrix: list[list[int]]) -> list[list[int]]:
    """Every top-right-to-bottom-left diagonal, each read top to bottom.

    Cells on one such diagonal all share the same value of r + c.
    """
    rows, cols = size(matrix)
    groups: defaultdict[int, list[int]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            groups[r + c].append(matrix[r][c])
    return [groups[s] for s in range(rows + cols - 1)]


def main_diagonals(matrix: list[list[int]]) -> list[list[int]]:
    """Every top-left-to-bottom-right diagonal. Cells share the same value of r - c."""
    rows, cols = size(matrix)
    groups: defaultdict[int, list[int]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            groups[r - c].append(matrix[r][c])
    return [groups[d] for d in range(-(cols - 1), rows)]


def diagonal_order(matrix: list[list[int]]) -> list[int]:
    """LeetCode 498. Anti-diagonals, alternating direction, flattened."""
    rows, cols = size(matrix)
    if rows == 0:
        return []
    groups: defaultdict[int, list[int]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            groups[r + c].append(matrix[r][c])

    out: list[int] = []
    for s in range(rows + cols - 1):
        band = groups[s]
        out.extend(reversed(band) if s % 2 == 0 else band)   # even bands run upwards
    return out


if __name__ == "__main__":
    m = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9],
         [10, 11, 12]]

    print(size(m))                 # (4, 3)
    print(by_row(m))               # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    print(by_column(m))            # [1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 12]
    print(transpose(m))            # [[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]
    print(anti_diagonals(m))       # [[1], [2, 4], [3, 5, 7], [6, 8, 10], [9, 11], [12]]
    print(main_diagonals(m))       # [[3], [2, 6], [1, 5, 9], [4, 8, 12], [7, 11], [10]]
    print(diagonal_order(m))       # [1, 2, 4, 7, 5, 3, 6, 8, 10, 11, 9, 12]

    square = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(diagonal_order(square))  # [1, 2, 4, 7, 5, 3, 6, 8, 9]
    print(diagonal_order([]))      # []
    print(diagonal_order([[]]))    # []
```

### Building a grid from nothing

Two lines that look the same and are not. This one is right:

```python
grid = [[0] * cols for _ in range(rows)]
```

This one is a bug, and §7 shows it going wrong:

```python
grid = [[0] * cols] * rows      # do not do this
```

---

## 6. What it costs

### Any full traversal

The outer loop runs `rows` times. For each of those the inner loop runs `cols` times. So the body
runs `rows × cols` times, and each run is constant work — one lookup, one append. That is
**O(rows × cols)** time.

Get the wording right, because it earns marks. If the matrix is `n × n`, that is `n²`, and saying
`O(n²)` is fine. If it is `m × n`, then `O(n²)` is simply wrong and `O(m × n)` is right. Better
still: **it is linear in the number of cells**, because it touches each cell exactly once and there
is no way to do less than that if you have to look at everything.

Concretely, a `1000 × 1000` matrix has a million cells. At roughly ten million simple Python
operations a second, that is a fraction of a second. A `10,000 × 10,000` matrix has a hundred
million cells and takes tens of seconds — the point at which you stop and ask whether you really
need to visit them all.

### `by_row` versus `by_column`

Identical counts: `rows × cols` visits either way. But they are not equally fast in practice.
Row-major follows memory order, so a whole cache line's worth of neighbouring values arrives with
the first one. Column-major jumps `cols` positions between reads and throws that away. From the
latency ladder on [day 010](../day-010-traversal-patterns/README.md), a value already in the cache
is roughly a hundred times closer than one that has to come from main memory. Both are `O(rows ×
cols)`; the constant factor between them can be several times.

### The diagonal grouping

One pass over every cell, so `rows × cols` visits — **O(rows × cols)** time, the same as any other
traversal. The extra cost is space: every value is copied into a group, so the dictionary holds
`rows × cols` values in total, spread across `rows + cols - 1` lists. That is **O(rows × cols)
extra space**.

If an interviewer objects to the extra space, the alternative is to walk each diagonal directly
with a moving `(r, c)` and emit as you go, which is `O(1)` extra space beyond the output. It is
noticeably fiddlier to get right under pressure. Say that the grouping version is `O(rows × cols)`
extra, that a direct walk is `O(1)`, and that you would write the grouping version first and
tighten it if the memory mattered. That answer is better than either code alone.

### The neighbour check

Four directions, one comparison each, no loop over the matrix — **O(1)** per cell. When every cell
does it, the total is four visits per cell, so still `O(rows × cols)` overall.

---

## 7. The traps

### The near-miss that destroys your grid: `[[0] * cols] * rows`

```python
grid = [[0] * 3] * 4
grid[1][2] = 7
for row in grid:
    print(row)
```

You set one cell. Here is what you get:

```
[0, 0, 7]
[0, 0, 7]
[0, 0, 7]
[0, 0, 7]
```

Four rows changed. The reason is that `* 4` does not make four rows — it makes **four references to
the same single row**. From [day 005](../day-005-python-lists-and-tuples/README.md), a list holds
references, and copying a reference does not copy the thing it points at. So `grid[0]`, `grid[1]`,
`grid[2]` and `grid[3]` are all the same list, and writing through any one of them is visible
through all four.

The fix builds a fresh list per row:

```python
grid = [[0] * 3 for _ in range(4)]
```

The comprehension evaluates `[0] * 3` once per iteration, producing four separate lists. Note that
the *inner* `[0] * 3` is perfectly safe, because `0` is a number and there is nothing to share.

This bug is nasty because a program with it often runs and produces a plausible-looking wrong
answer. If your grid updates seem to "leak" across rows, this is why.

### The real error: the two numbers the wrong way round

```python
matrix = [[1, 2, 3], [4, 5, 6]]
for c in range(len(matrix)):
    for r in range(len(matrix[0])):
        print(matrix[r][c], end=" ")
```

The intention was a column walk. The loop variables got renamed but the ranges did not follow.

```
1 4 Traceback (most recent call last):
  File "d16c.py", line 4, in <module>
    print(matrix[r][c], end=" ")
          ~~~~~~^^^
IndexError: list index out of range
```

It printed two correct values first, which is exactly why this is worth showing. `r` reached 2, but
there are only two rows, so `matrix[2]` does not exist. On a **square** matrix the same mistake
raises nothing at all and silently transposes your answer. Test on a non-square matrix, always.

### The real error: the empty matrix

```python
matrix = []
rows = len(matrix)
cols = len(matrix[0])
```

```
Traceback (most recent call last):
  File "d16d.py", line 3, in <module>
    cols = len(matrix[0])
               ~~~~~~^^^
IndexError: list index out of range
```

`len(matrix)` was happy and returned 0. `len(matrix[0])` reached into a row that is not there.
`[[]]` fails the same way one level down: there is a row, but it has no columns, so every later
`matrix[0][0]` breaks. Guard both, in one line: `if not matrix or not matrix[0]`.

### The real error: the tempting NumPy syntax

If you have seen NumPy, you may reach for this:

```python
n = [[1, 2], [3, 4]]
print(n[0, 1])
```

```
TypeError: list indices must be integers or slices, not tuple
```

`n[0, 1]` passes the tuple `(0, 1)` as a single subscript. NumPy arrays accept that; plain Python
lists do not. Interviews almost always want plain lists, so write `n[0][1]`.

### The near-miss: assuming the matrix is square

```python
for r in range(len(matrix)):
    for c in range(len(matrix)):     # should be len(matrix[0])
        ...
```

Correct on every square test case and broken on the first rectangular one — either an `IndexError`
if there are more rows than columns, or a silently truncated answer if there are more columns than
rows. **Compute `rows` and `cols` once, into named variables, before the loops.** Then this mistake
becomes impossible to make.

### The near-miss: negative indices do not raise

```python
r, c = 0, 0
print(matrix[r - 1][c])     # you meant "the row above" — there isn't one
```

There is no error. `matrix[-1]` is the *last* row, so a walk that steps off the top of the grid
quietly wraps round to the bottom and gives a confidently wrong answer. This is why the neighbour
helper checks `0 <= nr` before it reads anything, and it is the single biggest source of
hard-to-find bugs in grid problems later in the course.

---

## 8. In the interview

### How it gets asked

- *"Print the matrix in diagonal order."* — LeetCode 498. Usually with the zigzag, sometimes
  without; ask which.
- *"Sum each row, and each column."* — a warm-up, five minutes, testing only whether you keep the
  two numbers straight.
- *"Transpose this matrix."* — then, almost always, *"now do it in place"*, which is tomorrow's
  lesson.
- *"Given a grid of 0s and 1s, ..."* — the opening of every island, flood-fill and maze question.
  The traversal is today; the rest arrives with graphs.

### What to say out loud, in the first ninety seconds

1. **Fix the vocabulary before anything else.** *"Let me set my notation: `r` is the row index from
   0 to rows minus 1, `c` is the column index, and I access a cell as `matrix[r][c]` — row first."*
   Ten seconds, and it prevents the commonest bug live on the whiteboard.
2. **Ask whether it is square.** *"Can I assume it is square, or should I handle m by n?"* If they
   say rectangular, write `rows` and `cols` as separate variables immediately.
3. **Ask about empties.** *"What should I return for an empty matrix, or a matrix with empty rows?"*
4. **For the diagonal question, state the identity.** *"Every cell on a top-right-to-bottom-left
   diagonal has the same value of `r + c`. So I can group all cells by `r + c` in one pass, and
   there are exactly rows plus columns minus one groups."* This is the insight the question is
   testing, and saying it first means the code is then obvious.
5. **Name the zigzag as a separate concern.** *"The grouping gives each diagonal top to bottom. The
   alternating direction is then just reversing the even-numbered ones."* Splitting the problem in
   two is most of the battle.
6. **Give the cost.** *"One pass over every cell, so O(m × n) time — linear in the number of cells,
   which is the best possible since I have to look at all of them. O(m × n) extra space for the
   groups."*
7. **Offer the tightening.** *"If the extra space matters I can walk each diagonal directly with a
   moving row and column and emit as I go, which is O(1) extra."*

### The follow-ups

**"Can you do it without the extra space?"**
Yes. Instead of grouping, I walk each diagonal directly. For anti-diagonal number `s`, the cells
are those with `r + c == s`, so `r` ranges over `max(0, s - cols + 1)` to `min(s, rows - 1)` and `c`
is `s - r`. I emit that range forwards or backwards depending on whether `s` is even, and I never
store anything but the output. Same `O(m × n)` time, `O(1)` extra space. I would write the grouping
version first because it is far harder to get the bounds wrong, and tighten it only if asked —
those two `max`/`min` expressions are exactly where people lose ten minutes under pressure.

**"Why is walking by row faster than walking by column, if both are O(m × n)?"**
Because complexity classes count operations and hardware counts cache misses. A matrix is stored
row by row, so consecutive cells in a row are next to each other in memory, and reading one pulls
its neighbours into cache along with it. Walking down a column jumps a whole row's width between
reads, so most reads miss the cache and go to main memory, which is around a hundred times slower.
Both are linear in the number of cells; the constant factor differs by a factor of several. It is
the same reason a sequential disk read beats a random one.

**"How would you rotate the matrix by 90 degrees?"**
Transpose it, then reverse each row. Transposing swaps `matrix[r][c]` with `matrix[c][r]`, which
reflects across the main diagonal; reversing each row then reflects horizontally, and the two
reflections together are a 90-degree clockwise rotation. In place, the transpose loop must only
visit `c > r`, otherwise you swap every pair twice and end up back where you started. That is
`O(n²)` time and `O(1)` extra space, and it only works on a square matrix — a rectangular rotation
has to allocate, because the shape changes from `m × n` to `n × m`.

**"The grid is a million by a million. Now what?"**
Then a full traversal is a trillion cells and is off the table, so the question has changed shape.
Either the grid is sparse, in which case I would not store it as a list of lists at all — I would
keep a dictionary from `(r, c)` to value and only ever iterate over the entries that exist — or the
answer does not need every cell, in which case I would look for structure to exploit, such as
sortedness along rows and columns, and binary search instead of scanning. If it genuinely is dense
and every cell matters, it is not one machine's problem any more; you partition it into blocks and
process them in parallel.

### A model answer

> "First let me pin the notation, because this is where these questions go wrong. `r` is the row
> index, running 0 to rows minus 1. `c` is the column index, 0 to columns minus 1. A cell is
> `matrix[r][c]` — row first. And can I assume it is square, or should I handle m by n?
>
> ...Rectangular, fine, so I will keep `rows` and `cols` as separate variables.
>
> The observation the problem turns on is this: on any diagonal running top-right to bottom-left,
> each step goes one row down and one column left, so `r` increases by one while `c` decreases by
> one — which means `r + c` is the same for every cell on that diagonal. Cell `[0][2]`, cell
> `[1][1]` and cell `[2][0]` all have `r + c == 2`.
>
> So one pass over the whole matrix, putting each value into a bucket keyed by `r + c`, gives me
> every diagonal in one go. There are exactly `rows + cols - 1` of them, and because the loops go
> top to bottom, each bucket is already in top-to-bottom order.
>
> ```python
> def diagonal_order(matrix: list[list[int]]) -> list[int]:
>     if not matrix or not matrix[0]:
>         return []
>     rows, cols = len(matrix), len(matrix[0])
>     groups = defaultdict(list)
>     for r in range(rows):
>         for c in range(cols):
>             groups[r + c].append(matrix[r][c])
>     out = []
>     for s in range(rows + cols - 1):
>         band = groups[s]
>         out.extend(reversed(band) if s % 2 == 0 else band)
>     return out
> ```
>
> The zigzag is then a separate, easy concern: the buckets are all top-to-bottom, and the problem
> wants alternate ones bottom-to-top, so I reverse the even-numbered buckets.
>
> On the three by three, `[[1,2,3],[4,5,6],[7,8,9]]`, the buckets are `[1]`, `[2,4]`, `[3,5,7]`,
> `[6,8]`, `[9]`, and reversing buckets 0, 2 and 4 gives `1, 2, 4, 7, 5, 3, 6, 8, 9`.
>
> That is O(m × n) time — one visit per cell, and I have to look at every cell, so that is optimal —
> and O(m × n) extra space for the buckets. If the space matters, I can walk each diagonal directly
> with a moving row and column instead of bucketing, which brings the extra space to O(1). I would
> reach for that second version only if asked, because the bounds on each diagonal are the fiddly
> part and the bucketing version is much harder to get wrong."

---

## 9. Recall card

- **`matrix[row][column]`. Row first, always.** `rows = len(matrix)`, `cols = len(matrix[0])`.
- **Same expression, swapped loops:** outer `r` is row-major; outer `c` is column-major.
- **Down-right diagonal: `r - c` is constant. Down-left (anti-)diagonal: `r + c` is constant.**
  There are `rows + cols - 1` of each.
- **Never `[[0] * cols] * rows`** — it aliases one row. Use `[[0] * cols for _ in range(rows)]`.
- **O(rows × cols) time** for any full walk. Check `0 <= r < rows and 0 <= c < cols` before
  reading — negative indices wrap instead of raising.
