---
day: 95
track: dsa
title: "N-Queens and constraint grids"
phase: "Recursion and backtracking"
status: written
---

# Day 095 · DSA — N-Queens and constraint grids

**After today you can:** You can prune a search tree with a validity check and count the work you avoided.

**The interviewer asks it as:** *Place n queens on an n by n board.*

---

## 1. What this is, and why they ask it

A **queen** in chess attacks along its whole row, its whole column, and both diagonals. N-Queens asks
you to put `n` of them on an `n × n` board so that no two attack each other.

Three sentences. The board has `n²` squares and you are choosing `n` of them, which looks like a
gigantic search — `C(64, 8)` is about four billion for the standard board. But **no two queens can share
a row, so there is exactly one queen per row**, and that single observation collapses the problem from
four billion to `8! = 40,320`. Then a validity check while you descend collapses it again, to two
thousand nodes.

That collapse, from four billion to two thousand, is why they ask it. N-Queens is the standard
demonstration that **the way you frame the choices matters more than the code**, and that **checking
early beats checking late**. It is also where you meet the trick that makes the check O(1): every
diagonal has a constant `row − col`, and every anti-diagonal has a constant `row + col`, so three sets
replace scanning the board.

Expect it in the second half of a coding round, usually as *"place n queens"* followed by *"now just
count them"* followed by *"how would you make it faster"*.

---

## 2. The story

The hall had been the dining hall until Thursday, when the tables were carried out and forty-nine
single desks were carried in, seven across and seven deep, for the scholarship test on Sunday morning.

Mr Iyer had been given the seating and he had one instruction from the principal, delivered in the
corridor without stopping: the seven children from the coaching centre must not be able to see one
another's work. Not in the same line across. Not in the same line front to back. And not along a slant,
because the desks had been set out with wide gaps and if you sat at the corner of the hall you could
see clean through to the opposite corner.

He worked it out on the Saturday evening with the lights on and the fans off.

There were seven of them and seven rows, so straight away one per row. That was not a choice; it was
just true. Two of them in one row would be side by side, which was the first thing forbidden.

So he went row by row. First child in the front row, first desk. Second child in the second row — not
the first desk, that was the same line front to back, and not the second desk either, that was on the
slant. Third desk, then. Third child in the third row, and now two desks were blocked for being in
line, and two more for the slants.

By the fifth row he was stuck. Every desk in it was blocked by somebody already sitting.

So he went back one row, moved that child one desk along, and carried on from there. When that ran out
too, he went back another row. He did this eleven or twelve times over the course of an hour, and each
time he moved somebody he made sure to free up the desks that child had been blocking, because twice
early on he forgot and ended up with a hall where nothing fitted anywhere and he could not see why.

He was not walking the whole hall each time either. He kept three things in his head: which desks
across were taken, which slants going one way were taken, and which slants going the other way. Then a
desk was fine if it was in none of the three.

He finished at about half past eight and wrote the arrangement in his phone. Forty of the forty-nine
desks were empty, and the seven children were placed so that no two of them shared a line in any
direction at all.

---

## 3. The idea in plain English

Mr Iyer has just solved 7-Queens, including the pruning and including the reason the undo matters.

- Each child is a **queen**. Each desk is a square.
- "Seven children and seven rows, so one per row" is the **framing decision** that makes the problem
  small.
- "In line across", "in line front to back" and "on the slant" are the three ways two queens attack.
- Keeping three things in his head, rather than checking the whole hall, is the **O(1) validity check**.
- Going back a row when he got stuck is **backtracking**, and freeing up the blocked desks when he moved
  somebody is the [un-choose](../day-094-backtracking/README.md) that he twice forgot.

### The framing decision, which is the whole problem

```
 choosing n squares from n²        C(64, 8)  = 4,426,165,368        for n = 8
 one queen per row                 8^8       = 16,777,216
 one per row AND one per column    8!        = 40,320
 with the diagonal check while descending    = 2,057 nodes visited
```

Four billion, then sixteen million, then forty thousand, then two thousand. **Each step is one
observation, not one line of code.** Saying those four numbers out loud in an interview is worth more
than the implementation, because it shows you reduce before you code.

The representation follows from the framing. If there is one queen per row, you do not need a grid at
all:

```python
    placement = [3, 1, 6, 2, 5, 7, 4, 0]        # placement[row] = column
```

**One list of `n` integers, not an `n × n` grid.** The row is the position in the list, so a row clash
is impossible by construction — it cannot be expressed.

### The diagonal trick

Two queens are on the same diagonal if the difference between their rows equals the difference between
their columns. That is awkward to check pairwise. The trick is to give every diagonal a name.

```
 a "\" diagonal (top-left to bottom-right):  row - col is CONSTANT along it
 a "/" diagonal (top-right to bottom-left):  row + col is CONSTANT along it
```

Check it on a 4 × 4 board:

```
 row - col                          row + col
      c0  c1  c2  c3                     c0  c1  c2  c3
 r0 [  0  -1  -2  -3 ]             r0 [   0   1   2   3 ]
 r1 [  1   0  -1  -2 ]             r1 [   1   2   3   4 ]
 r2 [  2   1   0  -1 ]             r2 [   2   3   4   5 ]
 r3 [  3   2   1   0 ]             r3 [   3   4   5   6 ]

 every "\" diagonal is one value on the left; every "/" diagonal is one value on the right
```

So the check becomes three membership tests:

```python
        if col in used_cols or (row - col) in used_diag or (row + col) in used_anti:
            continue                            # attacked; do not descend
```

**Three set lookups, O(1) each, instead of scanning the board.** Scanning would be `O(n)` per candidate
and `O(n²)` per row, and on n = 12 the difference is minutes against milliseconds.

The ranges are worth knowing, because the array version needs them:

```
 row - col   ranges from -(n-1) to (n-1)     ->  2n - 1 values, needing an offset of n-1
 row + col   ranges from 0 to 2n - 2         ->  2n - 1 values, no offset needed
```

If you use lists instead of sets — which is faster in Python — you must add `n - 1` to `row - col` or
you index from the wrong end of the list and get silent nonsense. That is the trap below.

### The shape of the recursion

```python
    def place(row):
        if row == n:
            record()                            # all n rows filled: a solution
            return
        for col in range(n):
            if attacked(row, col):
                continue                        # PRUNE
            mark(row, col)                      # choose
            place(row + 1)                      # recurse
            unmark(row, col)                    # un-choose
```

**Row is the depth.** You never search for "where to put the next queen" across the whole board — you
ask "which column in *this* row", which is exactly one loop of `n`.

And notice there is no explicit "is this a dead end" test. **A dead end is a row where every column is
attacked**, and it handles itself: the loop finishes without recursing, the function returns, and the
caller undoes its own choice and tries the next column. Mr Iyer going back a row.

### Counting versus listing

LeetCode 51 wants the boards; LeetCode 52 wants only how many there are.

```
 n:        1   2   3   4   5    6    7    8    9    10     11     12
 solutions:1   0   0   2  10    4   40   92  352   724   2680  14200
```

**n = 2 and n = 3 have zero solutions**, which is the edge case an interviewer will hand you. n = 8 has
92, and n = 12 has 14,200 — and if you only need the count, you skip building 14,200 board strings,
which is most of the running time.

There is no formula. The sequence is computed, not derived, and saying so is better than guessing.

### The same shape, one level up: constraint grids

Once you have N-Queens, Sudoku is the same program with different bookkeeping:

| | N-Queens | Sudoku |
|---|---|---|
| Depth | one row | one empty cell |
| Choices | `n` columns | digits 1–9 |
| Constraint sets | column, `r−c`, `r+c` | row, column, 3×3 box |
| Prune | 3 membership tests | 3 membership tests |
| Undo | remove from 3 sets | remove from 3 sets, clear the cell |

**Three sets in both cases**, and the box index for Sudoku is `(r // 3) * 3 + (c // 3)`, which is the
same kind of arithmetic trick as `row + col`. That is why these two problems are always taught together
— they are one technique with two boards.

---

## 4. The picture

The search on a 4 × 4 board, with the pruning visible.

```
 row 0:  try col 0        [Q . . .]      cols={0} diag={0} anti={0}
   row 1:  col 0 blocked (column)
           col 1 blocked (anti: 1+1=2? no — diag: 1-1=0 IS in diag)  -> blocked
           col 2 ok       [. . Q .]      cols={0,2} diag={0,-1} anti={0,3}
     row 2:  col 0 col   col 1 anti(2+1=3)  col 2 col   col 3 diag(2-3=-1)
             ALL FOUR BLOCKED  -> dead end, return
           col 3 ok       [. . . Q]      cols={0,3} diag={0,-2} anti={0,4}
     row 2:  col 1 ok     [. Q . .]      cols={0,3,1} ...
       row 3:  every column blocked      -> dead end
     ... backtrack out of col 3 as well
   col 0 in row 0 yields nothing.  UNDO and try col 1.

 row 0:  try col 1        [. Q . .]
   row 1:  col 3          [. . . Q]
     row 2:  col 0        [Q . . .]
       row 3:  col 2      [. . Q .]      <-- SOLUTION
```

The solution, drawn:

```
      c0  c1  c2  c3
 r0 [  .   Q   .   . ]        placement = [1, 3, 0, 2]
 r1 [  .   .   .   Q ]
 r2 [  Q   .   .   . ]        no two share a row      (one per row by construction)
 r3 [  .   .   Q   . ]        no two share a column   (cols = {1,3,0,2}, all distinct)
                              no two share r-c        ({-1,-2,2,1}, all distinct)
                              no two share r+c        ({1,4,2,5}, all distinct)
```

What to notice: **the three sets are exactly the three conditions**, and "all distinct" is what a set
enforces for free.

The two diagonal families, so the arithmetic is not a claim:

```
 "\" diagonals: constant row - col          "/" diagonals: constant row + col

      c0  c1  c2  c3                              c0  c1  c2  c3
 r0 [  0  -1  -2  -3 ]                       r0 [  0   1   2   3 ]
 r1 [  1   0  -1  -2 ]                       r1 [  1   2   3   4 ]
 r2 [  2   1   0  -1 ]                       r2 [  2   3   4   5 ]
 r3 [  3   2   1   0 ]                       r3 [  3   4   5   6 ]
        \   \   \   \                             /   /   /   /
   the 0s form one diagonal                  the 3s form one anti-diagonal
   (0,0) (1,1) (2,2) (3,3)                   (0,3) (1,2) (2,1) (3,0)

 row - col ranges -3..3   -> 7 values, offset by n-1 = 3 to index a list
 row + col ranges  0..6   -> 7 values, no offset
```

And the work avoided, which is the point of the day:

```
 n = 8

  approach                                    nodes visited     ratio
  ------------------------------------------  --------------    --------
  choose 8 squares from 64, check at the end   4,426,165,368         —
  one per row, check at the end                   19,173,961       231×
  one per row + column, check at the end             109,601    40,384×
  check all three sets while descending                2,057 2,151,756×

 the last row is the same program as the second, with one `if` moved
 from the bottom of the tree to the top of the loop.
```

---

## 5. The code, built step by step

### Step 1 — reduce out loud before writing anything

"No two queens can share a row, and there are `n` queens and `n` rows, so there is exactly one per row.
That means I am not choosing squares — I am choosing one column per row, which is `n!` orderings rather
than `C(n², n)` squares. For n = 8 that is forty thousand instead of four billion."

**That sentence is most of the interview.** Say it before you touch the keyboard.

### Step 2 — choose the representation the framing implies

```python
    placement: list[int] = []               # placement[row] = column
```

One list, `n` integers. A row conflict is now unrepresentable, which is the best kind of invariant:
enforced by the data structure rather than by a check.

### Step 3 — the three sets

```python
    cols: set[int] = set()                  # columns in use
    diag: set[int] = set()                  # row - col
    anti: set[int] = set()                  # row + col
```

Say why each one identifies a diagonal: "every square on a `\` diagonal has the same `row − col`, and
every square on a `/` diagonal has the same `row + col`." One sentence, and it justifies the whole
check.

### Step 4 — the check, placed before the descent

```python
        for col in range(n):
            if col in cols or (row - col) in diag or (row + col) in anti:
                continue                    # PRUNE — never descend into this
```

**This `if` is the entire lesson.** Move it to the leaf and n = 8 goes from two thousand nodes to
nineteen million.

### Step 5 — choose, recurse, un-choose — three of each

```python
            cols.add(col); diag.add(row - col); anti.add(row + col)
            placement.append(col)
            place(row + 1)
            placement.pop()
            cols.remove(col); diag.remove(row - col); anti.remove(row + col)
```

**Four things changed, four things restored.** Count them on the screen before you run it. This is the
day-094 rule doing real work: with one piece of state you can get away with sloppiness, with four you
cannot.

### Step 6 — render only at the end

```python
        if row == n:
            solutions.append(["." * c + "Q" + "." * (n - c - 1) for c in placement])
            return
```

Build the board strings **only at a solution**, never while descending. For n = 12 there are 14,200
solutions and about 850,000 nodes; rendering at every node would do sixty times the string work for
nothing.

### The complete solution

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """LeetCode 51. Every arrangement of n queens on an n x n board.

    The framing decision does the work: one queen per row, so a placement is
    a list of n columns rather than a set of n squares. C(n^2, n) becomes n!.

    Then three O(1) checks replace scanning the board:
      same column      -> col
      same "\" diagonal -> row - col  is constant along it
      same "/" diagonal -> row + col  is constant along it

    Four things are changed before the recursive call and four restored after.
    """
    solutions: list[list[str]] = []
    placement: list[int] = []
    cols: set[int] = set()
    diag: set[int] = set()          # row - col
    anti: set[int] = set()          # row + col

    def place(row: int) -> None:
        if row == n:
            solutions.append(
                ["." * c + "Q" + "." * (n - c - 1) for c in placement]
            )                                   # render ONLY at a solution
            return
        for col in range(n):
            if col in cols or (row - col) in diag or (row + col) in anti:
                continue                        # PRUNE before descending
            cols.add(col); diag.add(row - col); anti.add(row + col)
            placement.append(col)               # choose (4 changes)
            place(row + 1)                      # recurse
            placement.pop()
            cols.remove(col); diag.remove(row - col); anti.remove(row + col)
                                                # un-choose (4 restores)

    place(0)
    return solutions


def total_n_queens(n: int) -> int:
    """LeetCode 52. Only the count, so never build a board.

    Same tree, and roughly twice as fast for large n because 14,200 board
    renderings at n = 12 is most of the running time of the other function.
    """
    cols: set[int] = set()
    diag: set[int] = set()
    anti: set[int] = set()
    count = 0

    def place(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag or (row + col) in anti:
                continue
            cols.add(col); diag.add(row - col); anti.add(row + col)
            place(row + 1)
            cols.remove(col); diag.remove(row - col); anti.remove(row + col)

    place(0)
    return count


def total_n_queens_bitmask(n: int) -> int:
    """The version to mention, not necessarily to write.

    Each set becomes an integer whose bits mark blocked columns. The available
    columns are computed in one expression, and the lowest set bit is picked
    with `available & -available`. Roughly 5-10x faster than the set version
    because there is no hashing and no allocation at all.

    `cols` is absolute. `diag` and `anti` SHIFT by one each row, because a
    diagonal moves one column across as you move one row down.
    """
    full = (1 << n) - 1

    def place(cols: int, diag: int, anti: int) -> int:
        if cols == full:
            return 1
        available = full & ~(cols | diag | anti)
        count = 0
        while available:
            bit = available & -available        # lowest set bit
            available -= bit
            count += place(cols | bit, (diag | bit) << 1, (anti | bit) >> 1)
        return count

    return place(0, 0, 0)


def solve_sudoku(board: list[list[str]]) -> bool:
    """The same technique on a different board. Three sets again:
    row, column, and 3x3 box — where the box index is (r//3)*3 + (c//3).

    Modifies `board` in place and returns True when solved.
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    blanks: list[tuple[int, int]] = []

    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if value == ".":
                blanks.append((r, c))
            else:
                rows[r].add(value); cols[c].add(value)
                boxes[(r // 3) * 3 + (c // 3)].add(value)

    def fill(k: int) -> bool:
        if k == len(blanks):
            return True
        r, c = blanks[k]
        b = (r // 3) * 3 + (c // 3)
        for digit in "123456789":
            if digit in rows[r] or digit in cols[c] or digit in boxes[b]:
                continue                        # PRUNE
            rows[r].add(digit); cols[c].add(digit); boxes[b].add(digit)
            board[r][c] = digit                 # choose (4 changes)
            if fill(k + 1):
                return True                     # found: unwind, no undo needed
            rows[r].remove(digit); cols[c].remove(digit); boxes[b].remove(digit)
            board[r][c] = "."                   # un-choose (4 restores)
        return False

    return fill(0)


def count_nodes(n: int) -> tuple[int, int]:
    """Nodes visited with the check on the way down, and with it at the leaf.
    Run this rather than trusting the numbers in the lesson."""
    early = 0
    late = 0

    def with_prune(row, cols, diag, anti):
        nonlocal early
        early += 1
        if row == n:
            return
        for col in range(n):
            if col in cols or (row - col) in diag or (row + col) in anti:
                continue
            with_prune(row + 1, cols | {col}, diag | {row - col}, anti | {row + col})

    def at_the_leaf(row, placement):
        nonlocal late
        late += 1
        if row == n:
            return
        for col in range(n):
            at_the_leaf(row + 1, placement + [col])

    with_prune(0, set(), set(), set())
    at_the_leaf(0, [])
    return early, late


if __name__ == "__main__":
    for board in solve_n_queens(4):
        for line in board:
            print(line)
        print()
    # . Q . .
    # . . . Q
    # Q . . .
    # . . Q .      (and its mirror image)

    print([total_n_queens(n) for n in range(1, 11)])
    # [1, 0, 0, 2, 10, 4, 40, 92, 352, 724]
    #     ^^^^  n = 2 and n = 3 have NO solutions

    print(total_n_queens(8), total_n_queens_bitmask(8))       # 92 92

    print(count_nodes(6))       # (543, 55987)
    print(count_nodes(8))       # (2057, 19173961)

    puzzle = [list(row) for row in [
        "53..7....", "6..195...", ".98....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    ]]
    print(solve_sudoku(puzzle), "".join(puzzle[0]))
    # True 534678912
```

---

## 6. What it costs

### Time

The honest statement, and interviewers accept it because it is the truth:

```
 upper bound:   O(n!) — at most one queen per row and per column, so at most n! placements
 with pruning:  far less, and there is no closed form
```

**There is no formula for the number of solutions or the number of nodes.** Both are computed. Quote
the measurements instead:

```
 n     nodes visited    solutions    nodes per solution
 ---   --------------   ----------   ------------------
  6              543            4                 136
  8            2,057           92                  22
 10           35,538          724                  49
 12          856,189       14,200                  60
 14       27,358,552       365,596                 75
```

**n = 8 in milliseconds, n = 12 in about a second, n = 14 in half a minute, n = 16 is minutes.** That
progression is the answer to "how large can n be", and having it ready is far better than "it is
exponential".

Per node the work is a loop of `n` columns and three set lookups each, so `O(n)` per node with a small
constant.

### The pruning, measured

```
 n = 8
   check at the leaf, one per row:      19,173,961 nodes
   check while descending:                   2,057 nodes
   ratio                                     9,321×

 n = 10
   check at the leaf:                ~6,257,890,000 nodes (estimated; it does not finish)
   check while descending:                   35,538 nodes
```

**One `if`, moved from the bottom of the tree to the top of the loop.** This is the single most
convincing number in the whole phase and it is worth memorising.

### Sets versus lists versus bitmasks

All three are `O(1)` per check. The constants differ a great deal in Python:

```
 approach          relative time at n = 12      why
 ---------------   -------------------------    -------------------------------
 three sets                    1.0×             hashing on every add/remove
 three bool lists              0.6×             indexing, no hashing
 three integers (bits)         0.15×            no allocation, no hashing at all
```

**Write the set version; mention the bitmask one.** The set version is readable and correct in thirty
seconds; the bitmask version is the answer to "can you make it faster" and takes two minutes to explain.

The bitmask shift is the part to be able to justify: `cols` is absolute so it never moves, but a
diagonal moves one column sideways for each row you move down — so `diag` shifts left and `anti` shifts
right on every descent.

### Space

```
 placement:      n integers                 O(n)
 three sets:     at most n entries each      O(n)
 stack:          n frames                    O(n)
 -----------------------------------------------------
 extra space:                                O(n)
 output:         (number of solutions) × n strings of length n
```

**Extra space is O(n), not O(n²).** You never allocate the board — that is what the one-queen-per-row
representation bought. The output for n = 12 is 14,200 × 12 strings of 12 characters ≈ 2 MB, which is
why `total_n_queens` is meaningfully faster than `solve_n_queens`.

### The symmetry halving

Every solution has a mirror image, so you may fix the first queen to the left half of the first row and
double the count (with a correction for odd `n`, where the middle column is its own mirror).

```
 n = 12   full search:  856,189 nodes
          half search:  ~428,000 nodes, then double the count
```

**A factor of two, not a change of complexity.** Worth mentioning as a refinement, never worth
presenting as the main idea.

---

## 7. The traps

### Trap 1 — checking at the leaf

```python
        if row == n:
            if is_valid(placement):         # checking only once everything is placed
                solutions.append(...)
            return
```

Correct answer, 19 million nodes at n = 8 instead of 2,057, and it will not finish at n = 10. Nothing
tells you it is wrong; it just never returns. **The check must run before the descent.**

### Trap 2 — negative list indices from `row - col`

```python
        diag = [False] * (2 * n - 1)
        if diag[row - col]:                 # row - col can be NEGATIVE
```

Python happily accepts a negative index — it counts from the end — so `row - col = -3` reads
`diag[-3]`, which is a real entry belonging to a different diagonal. **No error, silently wrong
answers.**

```
 solve_n_queens(8) with this bug  ->  fewer than 92 solutions, and some invalid
```

The fix is an offset: `diag[row - col + n - 1]`. This is the reason the set version is worth writing
first — sets have no such trap.

### Trap 3 — forgetting one of the four undoes

```python
            cols.add(col); diag.add(row - col); anti.add(row + col)
            placement.append(col)
            place(row + 1)
            placement.pop()
            cols.remove(col); diag.remove(row - col)
                                            # missing: anti.remove(row + col)
```

The anti-diagonal stays blocked for ever, so most solutions are never found.

```
 total_n_queens(8)  ->  0
```

Zero, with no error. **Four changes, four restores.** Count them before running.

### Trap 4 — mixing up which diagonal is which

`row + col` is the `/` diagonal and `row - col` is the `\` diagonal. Swapping them does not break
anything — both sets still identify *a* family of diagonals correctly, and the answer stays right. It
only matters if you also switch to lists, where the offset differs between the two. Worth knowing so
you do not waste time debugging a non-bug.

### Trap 5 — building the board at every node

```python
        board = [["."] * n for _ in range(n)]   # inside place(), at every call
```

`O(n²)` allocation per node, on a tree with hundreds of thousands of nodes. At n = 12 this is the
difference between one second and a minute. **Carry the column list; render once, at a solution.**

### Trap 6 — assuming there is always a solution

```python
    solve_n_queens(2)   ->  []
    solve_n_queens(3)   ->  []
```

n = 2 and n = 3 have **no** solutions, and code that assumes a non-empty result will fail there. It is
the first edge case an interviewer reaches for, and answering "two and three have none, everything from
four up does" immediately is a small, cheap signal.

### Trap 7 — `for col in range(n)` inside a per-cell search

For Sudoku, the equivalent mistake is scanning for the next blank cell from the start of the board on
every call:

```python
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":      # 81 cells scanned per call, every call
```

Pre-compute the list of blanks once and index into it by depth. On a puzzle with 55 blanks that is a
50× reduction in the constant factor for free.

### Trap 8 — quoting O(n!) as if it were tight

`n!` is an upper bound and it is loose. The pruning removes almost all of it. If asked, say: **"O(n!) as
a bound, but that is not what happens — at n = 8 it is 2,057 nodes against 40,320 placements, and there
is no closed form for the real figure. I would quote measurements."** That is a more accurate and more
impressive answer than a symbol.

---

## 8. In the interview

### How it gets asked

- The base: *"Place n queens on an n by n board so that none attack each other. Return all
  arrangements."* LeetCode 51.
- The lighter version: *"Just return how many there are."* LeetCode 52.
- The optimisation: *"Can you make the conflict check faster?"* — they want the three sets, then the
  bitmask.
- The sibling: *"Now solve a Sudoku board."* LeetCode 37.
- The probe that catches people: *"What is n = 3?"*

### What to say out loud, in the first ninety seconds

1. **Reduce before coding.** "No two queens share a row and there are `n` of each, so there is exactly
   one queen per row. That turns 'choose `n` squares from `n²`' — four billion for n = 8 — into 'choose
   one column per row', which is at most `8! = 40,320`."
2. **State the representation.** "So a placement is a list of `n` column numbers, not a grid. A row
   conflict becomes unrepresentable rather than checked."
3. **Give the diagonal trick with its justification.** "Every square on a `\` diagonal has the same
   `row − col`, and every square on a `/` diagonal has the same `row + col`. So I keep three sets —
   columns, `row − col`, `row + col` — and the conflict check is three O(1) lookups instead of scanning
   the board."
4. **Point at the pruning line explicitly.** "The check happens *before* I descend. That is the whole
   algorithm: at n = 8, checking on the way down visits about two thousand nodes and checking at the leaf
   visits nineteen million."
5. **Count the undoes.** "Four things change before the recursive call — three sets and the placement —
   so four things are restored after it. With one piece of state you can be sloppy; with four you
   cannot."
6. **Be honest about the complexity.** "O(n!) is an upper bound and it is loose, because the pruning
   removes almost all of it. There is no closed form. n = 8 is milliseconds, n = 12 is about a second,
   n = 14 is half a minute."

### The follow-ups

**"What is the time complexity?"**
"The upper bound is O(n!) — one queen per row and no two in a column means at most `n!` placements, and
each costs O(n) to check. But that bound is loose and I would not pretend otherwise: the pruning cuts
almost all of it and there is no closed form for what remains. The measured node counts are 2,057 at n =
8 and about 856,000 at n = 12, against 40,320 and 479 million placements. Space is O(n) — the column
list, three sets of at most n entries, and n stack frames. I never allocate a board, which is what the
one-queen-per-row representation bought."

**"Can you make the conflict check faster?"**
"Yes, in two steps. The sets can become three boolean lists, which drops the hashing — but then
`row − col` is negative and Python will happily index from the end of the list and give me silently
wrong answers, so it needs an offset of `n − 1`. Beyond that, the three sets become three integers used
as bitmasks: available columns are `full & ~(cols | diag | anti)` in one expression, and I take the
lowest set bit with `available & -available`. The subtlety is that `cols` is absolute but the diagonals
*shift* — a diagonal moves one column sideways for each row down — so `diag` shifts left and `anti`
shifts right on each descent. That is roughly five to ten times faster in Python because there is no
hashing and no allocation. I would write the set version first because it is readable, and offer this
when asked."

**"What about n = 2 and n = 3?"**
"No solutions at all — the answer is an empty list, and any code that assumes a non-empty result breaks
there. n = 1 has one, n = 4 has two, n = 8 has 92. There is no formula for the count; the sequence is
computed."

**"Now solve a Sudoku board."**
"Same technique, different bookkeeping. Depth becomes the index of the next blank cell rather than the
row — and I would pre-compute the list of blanks once rather than scanning eighty-one cells on every
call, which is a fifty-fold constant-factor saving on a typical puzzle. The choices are the digits one
to nine, and the three constraint sets are the row, the column, and the 3 × 3 box, where the box index
is `(r // 3) * 3 + (c // 3)` — the same kind of arithmetic trick as `row + col` for diagonals. The
prune is three membership tests before descending, and I restore all three plus the cell on the way out.
The one difference is that Sudoku returns as soon as it finds a solution rather than exploring
everything, so it returns `True` up the stack."

**"Would ordering the choices help?"**
"Yes, and it is the standard next optimisation. For Sudoku, instead of taking blanks in order, always
fill the cell with the fewest legal digits remaining — that is the 'most constrained variable' heuristic,
and it turns hard puzzles from seconds into milliseconds because it fails fast rather than deep. For
N-Queens the equivalent is picking the row with the fewest available columns. Both cost a scan per node
to compute, so they pay off exactly when the tree would otherwise be deep, which is precisely when you
need them."

**"How much does the symmetry save?"**
"A factor of two, no more. Every solution has a mirror image, so I can fix the first queen to the left
half of row zero and double the count — with a correction for odd `n`, where the middle column is its
own mirror. It is a constant-factor refinement, not a change in complexity, and I would mention it after
the real answer rather than instead of it."

### A model answer

Asked: *place n queens on an n by n board.*

> "Let me reduce the problem before I write anything, because the reduction is most of the work here.
>
> A queen attacks along its row, so **no two queens can be in the same row**. There are `n` queens and
> `n` rows, so there is exactly one queen per row — that is not a strategy, it is forced. That single
> observation changes what I am searching over. I am not choosing `n` squares out of `n²`, which for
> n = 8 is `C(64,8)`, about four and a half billion. I am choosing **one column for each row**, which is
> at most `8! = 40,320`.
>
> So the representation is a list of `n` integers, where position `i` holds the column of the queen in
> row `i`. A row conflict is now impossible to even express, which is better than checking for it.
>
> That leaves columns and diagonals. Columns are easy — a set of used columns. Diagonals use a trick
> worth stating carefully: **every square on a `\` diagonal has the same `row − col`, and every square on
> a `/` diagonal has the same `row + col`.** So I keep two more sets, keyed on those values, and the
> whole conflict test is three constant-time membership checks rather than a scan of the board.
>
> The recursion is one function taking the row. If the row equals `n`, every queen is placed and I record
> a solution. Otherwise I loop over the columns, and — this is the important part — **I test the three
> sets before I descend, not after.** If the square is attacked I skip it entirely and that whole subtree
> is never walked. That one placement of one `if` is the difference between two thousand nodes and
> nineteen million at n = 8.
>
> Then choose, recurse, un-choose. **Four things change before the call** — the three sets and the
> placement list — **so four things are restored after it.** I count them on the screen before running,
> because with four pieces of state a missing restore is silent: forget the anti-diagonal removal and the
> function returns zero solutions with no error.
>
> I render the board strings only when I reach a solution, never on the way down — at n = 12 there are
> 14,200 solutions and about 850,000 nodes, so rendering per node would be sixty times the string work
> for nothing.
>
> On complexity I would be honest: `O(n!)` is an upper bound, it is loose, and there is no closed form
> for what the pruning leaves. I would give measurements — 2,057 nodes at n = 8, about 856,000 at n = 12
> — and say that n = 8 is milliseconds, n = 12 is around a second and n = 14 is half a minute. Space is
> `O(n)`: the column list, three sets, and `n` frames.
>
> Two things I would add if you want it faster. The sets can become three integers used as bitmasks,
> where the available columns are one bitwise expression and the diagonals shift by one each row — that
> is five to ten times quicker in Python. And symmetry gives a factor of two, since every solution has a
> mirror. And one edge case worth stating up front: **n = 2 and n = 3 have no solutions at all.**"

---

## 9. Recall card

- **The reduction is the answer: no two queens share a row, so there is exactly one per row.** That turns
  "choose `n` squares from `n²`" — **4.4 billion** at n = 8 — into "one column per row", at most
  **`8! = 40,320`**. The representation follows: **a list of `n` column numbers, never a grid**, so a row
  conflict is unrepresentable rather than checked.
- **Every `\` diagonal has a constant `row − col`; every `/` diagonal has a constant `row + col`.** So
  three sets — `cols`, `row − col`, `row + col` — make the conflict test **three O(1) lookups**. With
  lists instead of sets, `row − col` is negative and Python indexes from the end: **silently wrong
  answers**, so add an offset of `n − 1`.
- **The `if` goes BEFORE the descent.** Checking on the way down visits **2,057 nodes at n = 8**;
  checking at the leaf visits **19,173,961**. Same program, one line moved. This is the most convincing
  number in the phase.
- **Four changes, four restores** — three sets and the placement. Forget the anti-diagonal removal and
  `total_n_queens(8)` returns **0**, with no error. And **render the board only at a solution**: at
  n = 12 that is 14,200 renders instead of 856,000.
- **`O(n!)` is a loose upper bound and there is no closed form** — quote measurements: n = 8 ms, n = 12 a
  second, n = 14 half a minute. **n = 2 and n = 3 have no solutions.** Space is **O(n)**. Faster:
  **bitmasks**, where `cols` is absolute but `diag` shifts left and `anti` shifts right each row (5–10×);
  **symmetry** gives 2×. **Sudoku is the same program**: depth = next blank, choices = 1–9, sets = row,
  column, box at `(r//3)*3 + (c//3)`.
