---
day: 17
track: dsa
title: "Matrix tricks: rotate, spiral, transpose"
phase: "Arrays"
status: written
---

# Day 017 · DSA — Matrix tricks: rotate, spiral, transpose

**After today you can:** You can rotate a matrix ninety degrees in place and print it in spiral order.

**The interviewer asks it as:** *Rotate the image ninety degrees clockwise, in place.*

---

## 1. What this is, and why they ask it

Yesterday you learned to walk a matrix. Today you rearrange one. Three operations come up again and
again, and all three are pure index bookkeeping with no algorithmic idea hiding inside them:
**transpose** (reflect the matrix across its top-left-to-bottom-right diagonal), **rotate** (turn it
a quarter turn), and **spiral order** (read it round and round from the outside inward).

The reason rotation is asked so often is that the obvious solution — allocate a new matrix and copy
each cell to its new home — is easy, and the words *in place* rule it out. The elegant answer is
that a quarter turn is two reflections: transpose the matrix, then reverse each row. Nobody derives
that under pressure. You either know it or you flounder, and interviewers know that, which is
exactly why it is a good filter for *did this person prepare*.

Spiral order is asked for a different reason. It has no trick at all. It is four loops and four
boundary variables, and it tests whether you can keep four moving numbers straight while somebody
watches. More candidates fail spiral order than fail rotation, and they fail it on the two guard
conditions in §5 that stop a single leftover row being printed twice.

Both are LeetCode staples — 48 (Rotate Image), 54 (Spiral Matrix), 59 (Spiral Matrix II), 867
(Transpose Matrix) — and both appear in real interviews at product companies as the fifteen-minute
warm-up before something harder.

---

## 2. The story

Ismail has been the attender at a school in Vijayawada for nineteen years, and every March the same
job comes round. Thirty-six desks in the tenth standard room, six rows of six, all facing the
blackboard on the north wall. For the public exam they cannot face the blackboard, because the
invigilator's table has to go by the east window where the light is. So the whole block has to be
turned a quarter turn.

The first year he did it desk by desk. He picked up a desk, thought about where it should end up,
carried it, put it down, and went back for the next one. It took him the whole of an afternoon, two
desks finished up in the wrong place, and a teacher had to come and sort it out on the morning of
the exam.

Now he does not think about desks at all. He thinks about lines.

He stands at the front and works it out once, out loud, the way he always does. The line of six
nearest the blackboard — that whole line, in order — becomes the line along the east wall, top to
bottom. The boy who sat at the left-hand end of the front line will now be sitting nearest the
window at the front. Then the second line from the blackboard becomes the next line in from the
window. Then the third. And the line right at the back, by the door, ends up along the west wall.

Six moves instead of thirty-six decisions. It takes him twenty minutes and nothing ends up in the
wrong place, because he is never choosing where one desk goes — he is only ever moving one whole
line into the place a whole line goes.

Then he sweeps, and he sweeps the same way he always has. He starts along the north wall and goes
right to the corner, then down the east wall, then back along the south wall, then up the west wall
— all the way round the outside. Then he does it again, one step further in, and again, and again,
each round a little smaller than the last, until everything is in one heap in the middle of the
floor and he can pick it up in one go.

---

## 3. The idea in plain English

Ismail's two habits are today's two problems. Turning the block of desks is **rotation**. Sweeping
round and round inward is **spiral order**.

Everything below uses `n` for the size of a square matrix, and `r` and `c` exactly as
[day 016](../day-016-2d-arrays/README.md) defined them: `r` is the row, `c` is the column, and a
cell is `matrix[r][c]`.

### Transpose: the fold along the diagonal

To **transpose** a matrix is to swap `matrix[r][c]` with `matrix[c][r]` for every pair. Row 0
becomes column 0, row 1 becomes column 1, and so on. Visually it is a fold along the line running
from the top-left corner to the bottom-right corner.

```
   1  2  3            1  4  7
   4  5  6    ->      2  5  8
   7  8  9            3  6  9
```

Two things to notice immediately.

**The cells on the diagonal itself do not move.** Where `r == c`, swapping a cell with itself does
nothing. That is 1, 5 and 9 above.

**Every other cell belongs to exactly one pair.** `matrix[0][2]` and `matrix[2][0]` are partners.
So if you loop over *every* cell and swap, you will visit each pair twice — swapping it back —
and end up exactly where you started. This is the single most common bug in the topic, and §7 shows
what it produces. The fix is to visit each pair once, by only looking at cells **above** the
diagonal:

```python
for r in range(n):
    for c in range(r + 1, n):     # c starts at r + 1, not 0
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
```

`range(r + 1, n)` starts one past the diagonal. On row 0 it covers columns 1 and 2; on row 1, just
column 2; on row 2, nothing. Three swaps for a `3 × 3`, which is exactly the number of off-diagonal
pairs.

**A transpose in place only works on a square matrix.** A `2 × 3` matrix transposes into a `3 × 2`
one, and the shape of the outer list would have to change, so it cannot be done by swapping. You
have to build a new matrix — which is what `zip(*matrix)` does.

### Rotation: a quarter turn is two flips

Here is the fact worth memorising, because it is the whole question:

> **Rotate 90° clockwise = transpose, then reverse each row.**

Watch it happen:

```
   original        transpose        reverse each row
   1  2  3          1  4  7            7  4  1
   4  5  6    ->    2  5  8     ->     8  5  2
   7  8  9          3  6  9            9  6  3
```

The bottom-left corner, 7, has arrived at the top-left. The top-left, 1, has gone to the top-right.
That is a clockwise quarter turn.

**Why it works**, in one line each. Transposing sends the cell at `(r, c)` to `(c, r)` — a
reflection across the main diagonal. Reversing every row then sends `(c, r)` to `(c, n - 1 - r)` — a
reflection left-to-right. Do both and the cell at `(r, c)` finishes at `(c, n - 1 - r)`, and that
is precisely the formula for a clockwise quarter turn. Two reflections about lines that meet at
45° compose into a rotation of 90°.

You do not need to say that last sentence in an interview. You do need to be able to check the
formula on one corner, out loud: *"cell (0,0) should end up at (0, n-1) — top-left goes to
top-right — and the formula gives (0, n-1-0), which is (0, n-1). Correct."* Checking one corner
takes five seconds and catches a wrong direction instantly.

And that is Ismail's front row becoming the right-hand column.

### The other three turns

Once you have the clockwise one, the rest are free:

| Turn | Recipe |
|---|---|
| 90° clockwise | transpose, then reverse each row |
| 90° anticlockwise | transpose, then reverse the **order of the rows** |
| 180° | reverse the order of the rows, then reverse each row |
| 270° clockwise | same as 90° anticlockwise |

Note the difference between the first two. `row.reverse()` on each row flips left-to-right.
`matrix.reverse()` flips top-to-bottom. One character of difference in intent, opposite directions
of turn. Say which one you mean while you write it.

### Spiral order: four walls that close in

Ismail's sweep is four boundaries, not four directions. Keep four numbers:

- `top` — the topmost row not yet swept
- `bottom` — the bottommost row not yet swept
- `left` — the leftmost column not yet swept
- `right` — the rightmost column not yet swept

Then repeat four passes: go **right** along row `top`, then **down** column `right`, then **left**
along row `bottom`, then **up** column `left`. After each pass, move that boundary inward by one,
because the line you just swept is finished.

Stop when the boundaries cross — when `top > bottom` or `left > right`. There is nothing left in
between.

The subtlety, and it is the whole difficulty of the problem: **after the first two passes the
remaining block may be a single row or a single column**, and then the third and fourth passes
would walk back along the line you have just done. So the third and fourth passes need guards:
sweep the bottom row only `if top <= bottom`, and the left column only `if left <= right`. §7 shows
exactly what you get without them.

---

## 4. The picture

The transpose, with the fold line drawn in:

```
                c=0  c=1  c=2                       c=0  c=1  c=2
              +----+----+----+                    +----+----+----+
        r=0   |  1 \  2 |  3 |              r=0   |  1 \  4 |  7 |
              +-----\---+----+                    +-----\---+----+
        r=1   |  4 |  5 \  6 |     ------>  r=1   |  2 |  5 \  8 |
              +----+-----\---+                    +----+-----\---+
        r=2   |  7 |  8 |  9 \                    |  3 |  6 |  9 \
              +----+----+----+                    +----+----+----+

   the diagonal (1, 5, 9) does not move.
   2 <-> 4,  3 <-> 7,  6 <-> 8.  Three swaps, not six.
```

**What to notice:** three swaps for a `3 × 3`. If you count six, you have swapped every pair twice
and the matrix is unchanged.

The full clockwise rotation, in two moves:

```
   start            after transpose       after reversing each row
   +---+---+---+    +---+---+---+          +---+---+---+
   | 1 | 2 | 3 |    | 1 | 4 | 7 |          | 7 | 4 | 1 |
   +---+---+---+    +---+---+---+          +---+---+---+
   | 4 | 5 | 6 | -> | 2 | 5 | 8 |    ->    | 8 | 5 | 2 |
   +---+---+---+    +---+---+---+          +---+---+---+
   | 7 | 8 | 9 |    | 3 | 6 | 9 |          | 9 | 6 | 3 |
   +---+---+---+    +---+---+---+          +---+---+---+
      ^                                       ^
      1 was here                              1 ends here
```

**What to notice:** follow one value, not the whole grid. The 1 goes top-left → top-left →
top-right. The 7 goes bottom-left → top-right → top-left. Tracking a single corner is how you check
the direction in an interview without redrawing anything.

The spiral, as closing walls:

```
   +---------------------------+
   |  1 -> 2 -> 3 -> 4         |   pass 1: right along top,   then top++
   |                     |     |
   |  ^  +---------+     v     |   pass 2: down the right,    then right--
   | 12  | 13  14  |     5     |
   |  ^  |         |     v     |   pass 3: left along bottom, then bottom--
   | 11  | 16  15  |     6     |
   |  ^  +---------+     v     |   pass 4: up the left,       then left++
   |                           |
   | 10 <- 9 <- 8 <- 7         |   then repeat on the smaller box
   +---------------------------+
```

**What to notice:** each pass finishes a whole line and then retires that line for good. The inner
`13, 14, 15, 16` block is the same problem on a smaller box, which is why one `while` loop handles
any size.

---

## 5. The code, built step by step

### Transposing in place

```python
n = len(matrix)
for r in range(n):
    for c in range(r + 1, n):
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
```

Three lines. The only thing to get right is `r + 1`. Write `range(n)` there and you get the
identity — §7 shows the exact output.

The tuple swap works the same way it did on
[day 013](../day-013-reverse-and-rotate/README.md): the right-hand side is fully evaluated before
anything is assigned, so no temporary variable is needed.

### Reversing each row

```python
for row in matrix:
    row.reverse()
```

`row` is a reference to the actual inner list, not a copy — from
[day 005](../day-005-python-lists-and-tuples/README.md) — so `row.reverse()` modifies the matrix.
`reversed(row)` would not; it returns a new iterator and leaves the row alone. That one-character
difference between `reverse` and `reversed` is a real interview slip.

### Putting the rotation together

```python
def rotate(matrix: list[list[int]]) -> None:
    """LeetCode 48. Rotate a square matrix 90 degrees clockwise, in place."""
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()
```

Six lines, no extra memory, and it is the complete answer to one of the most-asked matrix questions
there is.

### The one-liner, and when to use it

```python
rotated = [list(r) for r in zip(*matrix[::-1])]
```

`matrix[::-1]` reverses the row order; `zip(*...)` transposes. Reversing then transposing gives the
same clockwise turn as transposing then reversing rows. It is neat, it is correct, and it is **not
in place** — it builds a whole new matrix, which is `O(n²)` extra space. Write it, then say: *"but
the question said in place, so here is the two-flip version."* Showing both is strictly better than
showing either.

### Spiral order: the four passes

Start with the boundaries.

```python
top, bottom = 0, len(matrix) - 1
left, right = 0, len(matrix[0]) - 1
out: list[int] = []
```

Then the first two passes, which never need a guard because the loop condition already promised
there is at least one row and one column left.

```python
for c in range(left, right + 1):        # go right along the top row
    out.append(matrix[top][c])
top += 1

for r in range(top, bottom + 1):        # go down the right column
    out.append(matrix[r][right])
right -= 1
```

Notice the second loop starts at the **new** `top`, the one already moved down. The corner cell was
taken by the first pass and must not be taken again.

Now the two that need guards.

```python
if top <= bottom:                       # is there still a bottom row?
    for c in range(right, left - 1, -1):
        out.append(matrix[bottom][c])
    bottom -= 1

if left <= right:                       # is there still a left column?
    for r in range(bottom, top - 1, -1):
        out.append(matrix[r][left])
    left += 1
```

`range(right, left - 1, -1)` counts **down** from `right` to `left` inclusive; the `left - 1` is
the exclusive end, so `left` itself is included. Getting that `- 1` wrong drops a corner.

Those two `if`s are the whole exam. On a `1 × 4` matrix, the first pass takes all four values and
sets `top = 1`, which is now greater than `bottom = 0`. Without the guard, the third pass walks the
bottom row — which is the same row — backwards, and you emit `1 2 3 4 3 2 1`.

### The complete solutions

```python
def transpose_in_place(matrix: list[list[int]]) -> None:
    """Square matrices only. Reflects across the main diagonal."""
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):       # c > r: visit each pair exactly once
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Any shape. Returns a new n x m matrix; the input is untouched."""
    return [list(t) for t in zip(*matrix)]


def rotate(matrix: list[list[int]]) -> None:
    """LeetCode 48. 90 degrees clockwise, in place. Square only."""
    transpose_in_place(matrix)
    for row in matrix:
        row.reverse()                   # left-to-right flip


def rotate_anticlockwise(matrix: list[list[int]]) -> None:
    """90 degrees anticlockwise, in place. Same transpose, other flip."""
    transpose_in_place(matrix)
    matrix.reverse()                    # top-to-bottom flip


def rotate_180(matrix: list[list[int]]) -> None:
    """Half turn. No transpose needed — both flips, no fold."""
    matrix.reverse()
    for row in matrix:
        row.reverse()


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """LeetCode 54. Any shape, outside inwards, clockwise."""
    if not matrix or not matrix[0]:
        return []

    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    out: list[int] = []

    while top <= bottom and left <= right:
        for c in range(left, right + 1):            # right along the top
            out.append(matrix[top][c])
        top += 1

        for r in range(top, bottom + 1):            # down the right side
            out.append(matrix[r][right])
        right -= 1

        if top <= bottom:                           # left along the bottom
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:                           # up the left side
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1

    return out


def generate_spiral(n: int) -> list[list[int]]:
    """LeetCode 59. Fill an n x n matrix with 1..n*n in spiral order."""
    matrix = [[0] * n for _ in range(n)]            # never [[0] * n] * n
    top, bottom, left, right = 0, n - 1, 0, n - 1
    value = 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            matrix[top][c] = value
            value += 1
        top += 1

        for r in range(top, bottom + 1):
            matrix[r][right] = value
            value += 1
        right -= 1

        if top <= bottom:
            for c in range(right, left - 1, -1):
                matrix[bottom][c] = value
                value += 1
            bottom -= 1

        if left <= right:
            for r in range(bottom, top - 1, -1):
                matrix[r][left] = value
                value += 1
            left += 1

    return matrix


if __name__ == "__main__":
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate(m)
    print(m)                     # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_anticlockwise(m2)
    print(m2)                    # [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

    big = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    rotate(big)
    print(big)                   # [[13, 9, 5, 1], [14, 10, 6, 2], ...]

    print(spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # [1, 2, 3, 6, 9, 8, 7, 4, 5]
    print(spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
    # [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    print(spiral_order([[1, 2, 3, 4]]))          # [1, 2, 3, 4]  — the guard earns its keep
    print(spiral_order([[1], [2], [3], [4]]))    # [1, 2, 3, 4]
    print(spiral_order([]), spiral_order([[]]))  # [] []

    print(generate_spiral(3))    # [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
```

---

## 6. What it costs

### The rotation

**The transpose loop.** The outer loop runs `n` times. For `r = 0` the inner loop runs `n - 1`
times, for `r = 1` it runs `n - 2` times, and so on down to 0. Adding those up:

```
(n-1) + (n-2) + ... + 1 + 0  =  n(n-1)/2
```

For `n = 3` that is `3 × 2 / 2 = 3` swaps, which matches the three swaps in the picture. For
`n = 1000` it is 499,500 swaps.

**The reversal loop.** `n` rows, and reversing a row of length `n` costs `n/2` swaps, so
`n × n/2 = n²/2` more.

**Total:** about `n²/2 + n²/2 = n²` swaps, so **O(n²) time**. Which is the floor for this problem —
every one of the `n²` cells has to move, so you cannot do better than linear in the number of cells.

**Space:** the swaps use one temporary at a time and the reversals use none. **O(1) extra space**,
which is the entire point of the two-flip version. The `zip(*matrix[::-1])` one-liner is the same
`O(n²)` time but `O(n²)` extra space.

### Spiral order

Every cell is appended exactly once and no cell is visited twice, because each pass retires its
line. So the total work is `rows × cols` appends: **O(rows × cols) time**.

Space is `O(1)` extra — four integer boundaries — beyond the output list, which necessarily holds
`rows × cols` values. When an interviewer asks about space here, say *"O(1) auxiliary, not counting
the output"*, because "counting the output" is the ambiguity they are probing.

### A number to have ready

A `1000 × 1000` image is a million pixels. Rotating it touches each one about twice, so a couple of
million operations — well under a second in Python, and microseconds in C. A `10,000 × 10,000`
image is a hundred million pixels, which is where you stop rotating in Python and start using a
library that does it in one memory-order-friendly pass.

---

## 7. The traps

### The near-miss: transposing over the full range

```python
def rotate(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(n):              # should be range(r + 1, n)
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()
    return matrix

print(rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
```

```
[[3, 2, 1], [6, 5, 4], [9, 8, 7]]
```

That is not a rotation. It is the original matrix with each row reversed — a left-to-right mirror.
The transpose ran, then ran again in the opposite direction, and the two cancelled exactly, leaving
only the row reversals to take effect.

There is no error and the output looks structured, which is what makes this dangerous. **The
cheapest check is to count swaps**: a `3 × 3` transpose does three, and this version does nine.

### The real error: rotating a rectangular matrix

```python
print(rotate([[1, 2], [3, 4], [5, 6]]))
```

```
Traceback (most recent call last):
  File "d17d.py", line 9, in <module>
    print(rotate([[1, 2], [3, 4], [5, 6]]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d17d.py", line 5, in rotate
    matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
                                               ~~~~~~~~~^^^
IndexError: list index out of range
```

`n = len(matrix)` is 3, but each row only has 2 columns, so `matrix[0][2]` does not exist.

Now the more alarming direction — more columns than rows:

```python
print(rotate([[1, 2, 3], [4, 5, 6]]))
```

```
[[3, 4, 1], [6, 5, 2]]
```

**No error at all**, and complete nonsense. `n` was 2, so only the top-left `2 × 2` corner got
transposed and the third column was never touched. In-place rotation is **only defined for square
matrices** — a rectangular one changes shape from `m × n` to `n × m`, so the outer list itself
would have to grow or shrink. Ask "is it square?" before you write a line, and if it is not,
allocate.

### The near-miss: dropping the spiral guards

```python
def spiral_buggy(matrix):
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        for c in range(right, left - 1, -1):        # no guard
            out.append(matrix[bottom][c])
        bottom -= 1
        for r in range(bottom, top - 1, -1):        # no guard
            out.append(matrix[r][left])
        left += 1
    return out

print(spiral_buggy([[1, 2, 3, 4]]))
print(spiral_buggy([[1], [2], [3], [4]]))
print(spiral_buggy([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
```

```
[1, 2, 3, 4, 3, 2, 1]
[1, 2, 3, 4, 3, 2]
[1, 2, 3, 6, 9, 8, 7, 4, 5]
```

Look at the third line: the square case is **completely correct**. So a candidate who tests only on
`3 × 3` ships this and it fails on the first single-row input the grader sends. `[1, 2, 3, 4]`
comes back with seven values instead of four, because after the first pass there is no row left and
the code sweeps the same row backwards.

**Always test spiral code on a single row and a single column.** Those two inputs, and nothing else,
find this bug.

### The near-miss: `reversed` instead of `reverse`

```python
for row in matrix:
    reversed(row)          # does nothing to the matrix
```

No error, no effect. `reversed(row)` returns a lazy iterator and throws it away; `row.reverse()`
modifies the list. If your rotation comes out as a plain transpose, this is why.

### The near-miss: `zip(*matrix)` is not in place

```python
def rotate(matrix):
    matrix = [list(r) for r in zip(*matrix[::-1])]   # rebinds the local name only
```

The caller's matrix is unchanged. Assigning to a parameter name inside a function rebinds that
local name; it does not modify the object the caller holds. If the question says *in place* and the
grader checks the input array afterwards, this silently fails every test. Either mutate the rows
you were given, or return the new matrix and say clearly that it is not in place.

---

## 8. In the interview

### How it gets asked

- *"Rotate the image 90 degrees clockwise, in place."* — LeetCode 48. The phrase *in place* is the
  entire question; without it this is a two-line problem.
- *"Print the matrix in spiral order."* — LeetCode 54. Usually rectangular, deliberately.
- *"Generate an n by n matrix filled with 1 to n² in spiral order."* — LeetCode 59, the same four
  passes writing instead of reading.
- *"Transpose this matrix."* — the warm-up, and then *"now without extra space"*, which forces the
  square-only conversation.

### What to say out loud, in the first ninety seconds

1. **Ask the shape question first.** *"Is it guaranteed square? In-place rotation only works on a
   square matrix — a rectangular one changes shape from m by n to n by m, so the outer list itself
   would have to change and I would have to allocate."* This single sentence is worth a lot; most
   candidates never mention it.
2. **State the decomposition before writing anything.** *"A ninety-degree clockwise rotation is two
   reflections: transpose the matrix, then reverse each row."*
3. **Check the direction on one corner, out loud.** *"Let me sanity-check with the bottom-left cell.
   After a clockwise turn it should be top-left. Transpose sends (n-1, 0) to (0, n-1), then
   reversing that row sends it to (0, 0). Yes, top-left. Right direction."*
4. **Name the `r + 1`, before you write it.** *"In the transpose loop, the inner index starts at
   `r + 1`, not 0. If I loop over every cell I swap each pair twice and get the original matrix
   back."*
5. **Give the cost.** *"O(n²) time, which is optimal since every cell has to move, and O(1) extra
   space, which is what in place means here."*
6. **Offer the alternative.** *"There is a one-liner — `[list(r) for r in zip(*matrix[::-1])]` — but
   it builds a new matrix, so it is O(n²) space and does not satisfy in place."*

For spiral, the script is different because there is no insight to state:

1. *"I'll keep four boundaries — top, bottom, left, right — and do four passes per lap: right along
   the top, down the right, left along the bottom, up the left, shrinking each boundary as I finish
   with it."*
2. *"The part that needs care is that after the first two passes there may be only one row or one
   column left, so the bottom and left passes each need a guard, otherwise I re-emit a line."*
3. *"I'll test on a single row and a single column, since those are exactly the inputs that expose
   that."*

### The follow-ups

**"Now do it anticlockwise."**
Same transpose, the other flip. For clockwise I reverse each row, which is a left-to-right mirror.
For anticlockwise I reverse the order of the rows instead — `matrix.reverse()` — which is a
top-to-bottom mirror. I would check it on a corner the same way: the top-left cell should end up
bottom-left after an anticlockwise turn, and it does. And 180 degrees needs no transpose at all,
just both flips: reverse the row order and reverse each row.

**"Rotate it without transposing — do it as one pass of four-way swaps."**
Yes, and it is the version worth knowing because it does each cell exactly once instead of touching
it twice. Work in rings from the outside in. For ring `layer`, walk `i` from `layer` to
`n - 1 - layer - 1`, and rotate the four cells that map onto each other in a single four-way swap:
top goes to right, right to bottom, bottom to left, left back to top, saving one value in a
temporary. Same `O(n²)` and `O(1)`, roughly half the writes. It is materially harder to get the
four index expressions right under pressure, so I would write the transpose version first, state
that this alternative exists, and only code it if you want to see it.

**"The matrix is a large image and does not fit in memory. Now what?"**
Then the operation is I/O-bound, not compute-bound, and the two-flip approach is actively bad
because reversing rows and transposing have completely different memory access patterns — the
transpose reads down columns, which on a file means seeking. The standard answer is to work in
tiles: read a block that does fit, say 512 by 512, rotate it in memory, and write it to the
transposed block position in the output. That turns a huge number of random accesses into a modest
number of sequential ones, which by the latency ladder from
[day 010](../day-010-traversal-patterns/README.md) is the difference that matters. Real image
libraries do exactly this.

**"Spiral order, but the matrix is rectangular. What changes?"**
Nothing in the structure — the four-boundary version already handles it, because `top`/`bottom`
come from the row count and `left`/`right` from the column count independently. What changes is
that the guards start mattering much sooner: on a `1 × n` or `n × 1` matrix the very first lap
exhausts the grid, and without the two `if`s you emit values twice. That is why I test those two
shapes specifically.

### A model answer

> "First, is the matrix guaranteed square? In-place rotation only makes sense for a square matrix —
> rotating an m by n gives an n by m, so the shape changes and I would have to allocate a new one.
>
> ...Square, good.
>
> The key idea is that a ninety-degree clockwise rotation is two reflections. First transpose —
> reflect across the main diagonal, so the cell at (r, c) swaps with the cell at (c, r). Then
> reverse each row — reflect left to right. Composing those two gives the quarter turn.
>
> Let me check the direction before I write it. The bottom-left corner should finish at the top-left
> after a clockwise turn. Transposing sends (n-1, 0) to (0, n-1). Reversing that row sends column
> n-1 to column 0. So it lands at (0, 0), the top-left. That is right.
>
> ```python
> def rotate(matrix: list[list[int]]) -> None:
>     n = len(matrix)
>     for r in range(n):
>         for c in range(r + 1, n):      # r + 1, so each pair is swapped once
>             matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
>     for row in matrix:
>         row.reverse()
> ```
>
> The detail I want to call out is the `r + 1` in the inner range. Every off-diagonal cell belongs
> to exactly one pair, so if I looped over all n columns I would swap each pair twice and get the
> original matrix back — and there is no error to tell me, the output just comes out as a mirror
> instead of a rotation. The cells on the diagonal never move, which is why starting at `r + 1` is
> exactly right rather than merely an optimisation.
>
> On the three by three, transposing gives rows `1 4 7 / 2 5 8 / 3 6 9`, and reversing each row
> gives `7 4 1 / 8 5 2 / 9 6 3` — the bottom-left 7 is now top-left, which is the clockwise turn.
>
> That is O(n²) time, which is the best possible since every cell has to move, and O(1) extra space.
>
> There is a Python one-liner, `[list(r) for r in zip(*matrix[::-1])]`, which is the same operation
> written as reverse-then-transpose. I would mention it, but it allocates a whole new matrix, so it
> is O(n²) space and does not meet the in-place requirement. And if you wanted fewer writes there is
> a ring-by-ring version doing four-way swaps, which touches each cell once instead of twice — same
> complexity, harder to get the indices right, so I would only reach for it if you asked."

---

## 9. Recall card

- **Rotate 90° clockwise = transpose, then reverse each row.** Anticlockwise = transpose, then
  `matrix.reverse()`. 180° = both flips, no transpose.
- **The transpose loop is `for c in range(r + 1, n)`.** Full range swaps every pair twice and gives
  you a mirror, with no error.
- **In-place rotation is square-only.** Rectangular changes shape, so it must allocate.
- **Spiral is four boundaries and four passes**, each shrinking as it finishes — with a guard before
  the bottom pass and before the left pass.
- **Test spiral on a single row and a single column.** The square case passes even when the code is
  wrong.
