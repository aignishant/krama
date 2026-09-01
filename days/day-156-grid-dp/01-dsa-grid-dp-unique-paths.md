---
day: 156
track: dsa
title: "Grid DP: unique paths"
phase: "Dynamic programming"
status: written
---

# Grid DP: unique paths

## 1. What this is, and why they ask it

**You are in the top-left corner of a grid. You may only move right or down. How many different routes reach
the bottom-right corner?**

For a 3×7 grid the answer is 28. The variants ask for the cheapest path instead of the count, or add obstacles,
or change the allowed moves.

They ask it because **the state is the most natural one in all of dynamic programming.** `dp[r][c]` is the
answer for the cell at row `r`, column `c`. There is no clever redefinition, no "ending exactly at", no prefix
lengths — **the grid is the table.** That makes it the best place to practise the mechanics without fighting
the state, which is why it appears constantly in first-round interviews.

The other reason is that **it is where the space collapse becomes obvious.** `dp[r][c]` depends only on the
cell above and the cell to the left, so one row of state is enough — and unlike knapsack, **you can see why
just by looking at the picture.** A candidate who writes the full table and then says "actually one row does
it, because the value in `row[c]` before I overwrite it *is* the cell above" has demonstrated the idea
properly.

And there is a third reason worth knowing: **for the plain counting version, there is a closed-form answer.**
The path is a sequence of moves, and choosing which of them are "down" is a binomial coefficient. **`O(1)`
memory, `O(min(m,n))` time, no table at all** — and mentioning it is a real signal, provided you also say why
it stops working the moment an obstacle appears.

By the end of this lesson you can write the counting and minimum-cost versions, handle obstacles correctly,
collapse to one row and explain why, give the combinatorial solution, and recognise the family.

---

## 2. The story

The new hospital block had four floors and Meenakshi had to work out how the trolleys would move through it,
and she had two weeks, and she had never done anything like it.

The plan was on the table in front of her. **Corridors going one way, corridors going the other, and junctions
where they crossed.** Rooms hanging off them. And somewhere in the middle, the lift.

**The rule that made it manageable came from the porters, not from her.**

Because the trolleys were long and the corners were tight, the porters had worked out years ago in the old
building that **you went along and then down, or down and then along, but you never doubled back.** Reversing a
loaded trolley in a corridor was how you knocked a drip stand over.

**So every route through the block only ever went in two directions.** Forwards and towards the lift. Never
back.

And the question the administrator kept asking, which Meenakshi could not answer, was how many ways there were
to get from admissions to the lift, **because he wanted to know how many of them went past the room where the
noise complaints were coming from.**

She tried to count them by tracing routes with her finger and lost her place four times.

**What worked was going backwards, and she found it by accident.**

She started writing a number at each junction. **Not the number of routes from admissions to that junction —
she tried that first and it was just as confusing. The number of routes from that junction onwards to the
lift.**

**At the lift itself: one.** You are there.

**At the junction just before it, in either direction: one.** Only one way to go.

And then at any junction with two exits — one forwards, one towards the lift — **the number was just the two
numbers she had already written, added together.** Because every route out of that junction begins with one
step or the other, and after that step it is a route she has already counted.

**It took her forty minutes to fill in the whole plan, and she never traced a single route with her finger.**

The administrator asked how she was so sure, and she said the thing that was actually the proof.

**"Because I never counted any route twice. Every route from here starts with exactly one of the two steps,
and I have counted each of those separately."**

---

## 3. The idea in plain English

Meenakshi's junction numbers are the DP table, and her last sentence is why the recurrence is an addition
rather than something harder.

**The state is as direct as it gets:**

> **`dp[r][c]` is the number of ways to reach the cell at row `r`, column `c` from the start.**

**No redefinition needed. The grid is the table.** After the last four days, that is a relief and it is worth
noticing why: the question already names a position, and the position is a complete state.

**The recurrence is the addition.** You can only arrive at a cell from above or from the left, so:

```
dp[r][c] = dp[r-1][c] + dp[r][c-1]
```

**Every path into this cell came through exactly one of those two neighbours**, so adding them counts each
path once — which is Meenakshi's proof, and it is why counting works here when counting is normally so easy
to get wrong.

**The base cases are the first row and first column.** In the top row you can only have come from the left, so
there is exactly one way to reach every cell: `dp[0][c] = 1`. Same down the first column. **And `dp[0][0] = 1`
— one way to be where you start, by doing nothing.**

**Initialise the whole table to 1 and the first row and column are handled for free**, which is a small,
genuinely useful trick.

**Now the three variants, which is what actually gets asked.**

**Minimum path sum.** Each cell has a cost; find the cheapest route. **Same state, `min` instead of `+`:**

```
dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
```

**And the base cases change completely.** They are no longer `1` — they are **running sums**, because in the
first row there is only one route and its cost is everything before it. **This is the most common error in the
variant**: keeping the counting base cases and getting answers that are far too small.

**Obstacles.** Some cells are blocked. **A blocked cell has zero ways through it**, so set `dp[r][c] = 0` and
carry on — the addition propagates the zero automatically.

**And the base case now has a trap.** The first row is not all ones any more: **once you hit an obstacle in the
top row, every cell after it is unreachable**, because you cannot go round. So the first row is ones until the
first obstacle and zeros thereafter. **Initialising the whole table to 1 is now wrong**, which is exactly why
the trick above needs a caveat.

**The space collapse, and this is where the picture does the work.**

`dp[r][c]` reads only the cell above and the cell to the left. **So keep one row and update it left to right:**

```python
for r in range(1, rows):
    for c in range(1, cols):
        row[c] = row[c] + row[c - 1]
```

**`row[c]`, before you overwrite it, still holds the previous row's value — the cell above. `row[c-1]` has
already been updated this pass — the cell to the left.** Both are exactly what the recurrence wants, and you
get them from one array.

**That is `O(cols)` space instead of `O(rows × cols)`**, and it is the clearest instance of the trick in the
course, because you can point at the two values and say what each one is.

**Finally, the closed form, which applies only to the plain counting version.**

**Every path from corner to corner of an `m × n` grid makes exactly `m - 1` downward moves and `n - 1`
rightward moves, in some order.** So a path *is* a sequence of `(m-1) + (n-2)`... — carefully: a sequence of
`m + n - 2` moves, of which `m - 1` are down.

**Counting the ways to choose which moves are down is a binomial coefficient:**

```
paths = C(m + n - 2, m - 1)
```

**For a 3×7 grid: `C(8, 2) = 28`.** Which is the answer, computed with no table at all.

**`math.comb` does it in `O(min(m, n))` time and `O(1)` space** — and mentioning it is a genuine signal.

**But say the limitation in the same breath**: it counts *all* paths, so **one obstacle destroys it entirely.**
There is no closed form for the obstacle version, and the DP is the answer. **That is the honest framing, and
offering the formula without it looks like a memorised trick.**

**And the family, which is larger than it looks.** Minimum path sum, obstacle grids, cherry pickup (two paths
at once), dungeon game (which is filled backwards), triangle, maximal square. **They all share the state and
differ in the move set, the operator, and occasionally the direction of the fill.**

---

## 4. The picture

The table filling in, for a 3×7 grid:

```
        c=0  1   2   3   4   5   6
  r=0    1   1   1   1   1   1   1     top row: one way to each
  r=1    1   2   3   4   5   6   7     each = above + left
  r=2    1   3   6  10  15  21  28     answer = dp[2][6] = 28
         ^
    first column: one way to each

  dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
  dp[2][3] = dp[1][3] + dp[2][2] = 4 + 6 = 10

  Every path into a cell arrives from ABOVE or from the LEFT,
  never both, so adding counts each path exactly once.
```

Meenakshi's version, counted backwards from the destination:

```
  same grid, numbers = routes from HERE to the lift

  r=0   28  21  15  10   6   3   1
  r=1    7   6   5   4   3   2   1
  r=2    1   1   1   1   1   1   1  <- the lift is at the bottom right
                                      the bottom row: only one way, along

  The answer is the same 28, read from the START instead of the END.
  Forwards from the start or backwards from the goal — both work,
  and which is more natural depends on where the base case is obvious.
```

The space collapse, which you can see:

```
  ONE ROW, updated LEFT TO RIGHT

  row after r=0:  [ 1  1  1  1  1  1  1 ]

  processing r=1, at c=3:
     row = [ 1  2  3  ?  1  1  1 ]
                   ^  ^
                   |  +-- row[3] still holds the PREVIOUS row's value = 1
                   |      that is the cell ABOVE
                   +----- row[2] was updated THIS pass = 3
                          that is the cell to the LEFT

     row[3] = row[3] + row[2] = 1 + 3 = 4     correct

  The array holds the previous row to the right of the cursor
  and the current row to the left of it. That is the whole trick.
```

Obstacles, and why the first row breaks:

```
  grid  ( X = obstacle )

     .  .  X  .
     .  .  .  .
     .  .  .  .

  first row: 1  1  0  0       <- NOT 1 1 1 1
                    ^
     once blocked, everything after it in the top row is
     unreachable — you cannot go round, because you cannot go up.

  full table:
     1  1  0  0
     1  2  2  2
     1  3  5  7

  answer 7. Initialising the whole table to 1 would give 10 — exactly
  the no-obstacle answer, because the block in the top row was ignored.
```

Minimum path sum, and why the base cases change:

```
  grid            dp (cheapest cost to reach)
  1  3  1          1  4  5
  1  5  1          2  7  6
  4  2  1          6  8  7

  first row is a RUNNING SUM: 1, 1+3=4, 4+1=5
  first column likewise:      1, 1+1=2, 2+4=6

  dp[1][1] = 5 + min(4, 2) = 7
  dp[2][2] = 1 + min(6, 8) = 7      answer 7

  Keeping the counting base cases (all 1s) would give nonsense.
  The base cases follow from the QUESTION, not from habit.
```

The closed form:

```
  3 x 7 grid: every path is 2 downs and 6 rights, in some order

     D D R R R R R R
     R D R D R R R R
     R R R R R R D D      ... all arrangements of the same multiset

  a path IS a sequence of 8 moves, of which 2 are down
  -> choose which 2 of the 8 are down
  -> C(8, 2) = 8 x 7 / 2 = 28

  m + n - 2 total moves, choose m - 1 of them.
  O(min(m,n)) time, O(1) space, no table.

  AND: one obstacle destroys this completely. There is no closed
  form once some paths are forbidden.
```

---

## 5. The code, built step by step

### Counting paths

```python
def unique_paths(rows: int, cols: int) -> int:
    dp = [[1] * cols for _ in range(rows)]    # first row and column: 1 way each
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[rows - 1][cols - 1]
```

**Initialising to `1` handles both base cases for free**, and the loops start at 1 so they never touch them.

**Three lines of actual work.** This is the cleanest DP in the course, and that is why it is asked first.

### The one-row version

```python
def unique_paths_one_row(rows: int, cols: int) -> int:
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            row[c] += row[c - 1]              # above + left, from one array
    return row[-1]
```

**`row[c]` is the cell above (not yet overwritten this pass); `row[c-1]` is the cell to the left (already
overwritten).** Say that out loud while writing it — it is the whole justification, and it is checkable by
pointing at the array.

**`O(cols)` space.** Swap the dimensions first if `rows < cols` and it becomes `O(min(rows, cols))`.

### The closed form

```python
import math

def unique_paths_formula(rows: int, cols: int) -> int:
    """A path is m+n-2 moves, of which m-1 are down. Choose which."""
    return math.comb(rows + cols - 2, rows - 1)
```

**One line, `O(1)` space.** Offer it as an aside, and immediately say that **it only works with no obstacles**.

### Obstacles

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return 0                              # start or end blocked
    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                row[c] = 0                    # blocked: no paths through it
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]
```

**`row[c] = 0` on an obstacle, and the addition propagates it** — every cell downstream loses those paths
automatically.

**`elif c > 0` skips column zero**, whose value carries down from the previous row unchanged, which is exactly
right: the only way into a first-column cell is from directly above.

**And the `row[0] = 1` before the loop with `r` starting at 0** means the first row is handled by the same
code as every other row — **no separate base-case pass, and the obstacle rule applies to it correctly.**

### Minimum path sum

```python
def min_path_sum(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    row = [0] * cols
    row[0] = grid[0][0]
    for c in range(1, cols):
        row[c] = row[c - 1] + grid[0][c]      # first row: a RUNNING SUM
    for r in range(1, rows):
        row[0] += grid[r][0]                  # first column: also a running sum
        for c in range(1, cols):
            row[c] = grid[r][c] + min(row[c], row[c - 1])
    return row[-1]
```

**The two base-case loops are the whole difference from the counting version**, and forgetting them is the
standard bug: the first row's costs must accumulate, because there is only one route along it.

**`min(row[c], row[c-1])` is above and left**, exactly as before — only the operator changed.

### Reconstructing the path

```python
def min_path_route(grid: list[list[int]]) -> list[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]    # full table needed for the walk-back
    dp[0][0] = grid[0][0]
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])

    path, r, c = [], rows - 1, cols - 1
    while (r, c) != (0, 0):
        path.append((r, c))
        if r == 0:
            c -= 1
        elif c == 0:
            r -= 1
        elif dp[r - 1][c] <= dp[r][c - 1]:
            r -= 1                            # came from above
        else:
            c -= 1                            # came from the left
    path.append((0, 0))
    return path[::-1]
```

**The full table is required**, same trade as every reconstruction this week. **The `r == 0` and `c == 0`
guards handle the edges**, where only one direction is possible.

### Two variants worth seeing

```python
def min_falling_path(grid: list[list[int]]) -> int:
    """Moves are down-left, down, down-right. Same state, different move set."""
    rows, cols = len(grid), len(grid[0])
    row = grid[0][:]
    for r in range(1, rows):
        nxt = [0] * cols
        for c in range(cols):
            best = min(row[max(c - 1, 0):min(c + 2, cols)])
            nxt[c] = grid[r][c] + best
        row = nxt
    return min(row)                           # may end anywhere in the last row


def maximal_square(matrix: list[list[str]]) -> int:
    """dp[r][c] = side of the largest all-1 square ENDING at (r,c)."""
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1":
                if r == 0 or c == 0:
                    dp[r][c] = 1
                else:
                    dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
    return best * best
```

**`min_falling_path` needs a second array**, because a cell reads three cells from the previous row including
one to its right — **which the one-row trick has already overwritten.** That is a good check on whether you
understand the collapse rather than copying it.

**`maximal_square` reads three neighbours including the diagonal**, and the `min` of three is the constraint
that all three smaller squares must be present. **Its answer is `max(dp)`, not the last cell** — the state is
"ending at", like longest increasing subsequence.

### The complete solution

```python
"""Grid DP: counting, costs, obstacles, and the closed form."""

import math


def unique_paths(rows: int, cols: int) -> int:
    """dp[r][c] = ways to reach (r, c). Every path arrives from above or left."""
    dp = [[1] * cols for _ in range(rows)]    # first row/column: one way each
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[rows - 1][cols - 1]


def unique_paths_one_row(rows: int, cols: int) -> int:
    """row[c] is the cell ABOVE until overwritten; row[c-1] is the cell LEFT."""
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            row[c] += row[c - 1]
    return row[-1]


def unique_paths_formula(rows: int, cols: int) -> int:
    """m+n-2 moves, m-1 of them down. No table. Breaks with any obstacle."""
    return math.comb(rows + cols - 2, rows - 1)


def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    """A blocked cell has 0 paths; the addition propagates the zero."""
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return 0
    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                row[c] = 0
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]


def min_path_sum(grid: list[list[int]]) -> int:
    """Same state, min instead of +. The base cases become RUNNING SUMS."""
    rows, cols = len(grid), len(grid[0])
    row = [0] * cols
    row[0] = grid[0][0]
    for c in range(1, cols):
        row[c] = row[c - 1] + grid[0][c]
    for r in range(1, rows):
        row[0] += grid[r][0]
        for c in range(1, cols):
            row[c] = grid[r][c] + min(row[c], row[c - 1])
    return row[-1]


def min_path_route(grid: list[list[int]]) -> list[tuple[int, int]]:
    """The cheapest route itself. Needs the full table."""
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])

    path: list[tuple[int, int]] = []
    r, c = rows - 1, cols - 1
    while (r, c) != (0, 0):
        path.append((r, c))
        if r == 0:
            c -= 1
        elif c == 0:
            r -= 1
        elif dp[r - 1][c] <= dp[r][c - 1]:
            r -= 1
        else:
            c -= 1
    path.append((0, 0))
    return path[::-1]


def min_falling_path(grid: list[list[int]]) -> int:
    """Down-left, down, down-right. Needs TWO rows: it reads to the right."""
    rows, cols = len(grid), len(grid[0])
    row = grid[0][:]
    for r in range(1, rows):
        nxt = [0] * cols
        for c in range(cols):
            nxt[c] = grid[r][c] + min(row[max(c - 1, 0):min(c + 2, cols)])
        row = nxt
    return min(row)


def maximal_square(matrix: list[list[str]]) -> int:
    """dp[r][c] = side of the largest all-1 square ENDING at (r,c). Answer is max."""
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1":
                dp[r][c] = 1 if r == 0 or c == 0 else 1 + min(
                    dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
    return best * best


if __name__ == "__main__":
    print("paths 3x7 table  :", unique_paths(3, 7))
    print("paths 3x7 one row:", unique_paths_one_row(3, 7))
    print("paths 3x7 formula:", unique_paths_formula(3, 7))
    print("paths 1x1        :", unique_paths(1, 1))
    print("paths 23x12      :", unique_paths_formula(23, 12))

    blocked = [[0, 0, 1, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
    print("with obstacle    :", unique_paths_with_obstacles(blocked))
    print("no obstacle      :", unique_paths(3, 4))
    print("start blocked    :", unique_paths_with_obstacles([[1, 0], [0, 0]]))

    cost = [[1, 3, 1],
            [1, 5, 1],
            [4, 2, 1]]
    print("min path sum     :", min_path_sum(cost))
    print("the route        :", min_path_route(cost))

    print("falling path     :", min_falling_path([[2, 1, 3], [6, 5, 4], [7, 8, 9]]))
    print("maximal square   :", maximal_square([
        list("10100"), list("10111"), list("11111"), list("10010")]))
```

Run it and you get:

```
paths 3x7 table  : 28
paths 3x7 one row: 28
paths 3x7 formula: 28
paths 1x1        : 1
paths 23x12      : 193536720
with obstacle    : 7
no obstacle      : 10
start blocked    : 0
min path sum     : 7
the route        : [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
falling path     : 13
maximal square   : 4
```

**`with obstacle 7` against `no obstacle 10`** is the cost of the single blocked cell, made visible — and note
it is not a simple subtraction, because the block also removes paths that would have gone through cells
downstream of it.

**And `paths 23x12` being 193 million** is worth noticing: **the counts grow very fast**, which is why the
counting version sometimes asks for a modulus.

---

## 6. What it costs

**Time and space, both versions.**

```
full table:   rows x cols cells, O(1) each     = O(rows x cols) time
              rows x cols integers             = O(rows x cols) space

one row:      same time
              cols integers                    = O(cols) space
              (swap first for O(min(rows, cols)))

formula:      math.comb is O(min(m, n)) multiplications
              O(1) space
```

**Concretely:**

```
100 x 100        10,000 cells        instant
1,000 x 1,000    1,000,000 cells     ~0.3 s in Python
                 full table:  ~40 MB
                 one row:     ~8 KB       5,000x less

10,000 x 10,000  100,000,000 cells   ~40 s
                 full table:  ~4 GB -> MemoryError
                 one row:     ~80 KB      still fine
```

**The one-row version is what makes large grids possible at all**, and that is a stronger argument than the
constant factor.

**The formula, for contrast:**

```
unique_paths_formula(1000, 1000)
  = C(1998, 999)
  math.comb does ~999 multiplications and divisions
  -> microseconds, against 0.3 seconds and a million cells

and the answer has 600 digits, which Python handles and a
64-bit integer does not — worth checking if the problem
specifies a modulus.
```

**How fast the counts grow:**

```
3 x 7      = 28
10 x 10    = 48,620
20 x 20    = 35,345,263,800                  ~3.5 x 10^10
50 x 50    ~ 2.5 x 10^28                     28 digits
100 x 100  ~ 2.2 x 10^58                     59 digits

a Java long holds 19 digits -> overflows before a 40 x 40 grid.
Python is fine; the problem may still ask for mod 10^9 + 7.
```

**Reconstruction:**

```
the walk-back is O(rows + cols) — each step decreases r or c
but it needs the FULL table: O(rows x cols) space

so: the length, in O(cols) space
    or the path, in O(rows x cols) space
    not both, unless you use divide and conquer
```

**The variants:**

```
min path sum          same O(rows x cols) time, O(cols) space
obstacles             same, plus one branch per cell
min falling path      O(rows x cols) time, O(cols) space
                      but TWO arrays, because it reads to the right
maximal square        same, and reads three neighbours
cherry pickup (two    O(rows x cols^2) — the state gains a dimension
paths at once)        for the second walker's column
```

**Cherry pickup is the one worth naming as the step up**: two paths at once means the state is `(row, col1,
col2)`, and that extra dimension is the whole difficulty.

---

## 7. The traps

**Initialising to 1 when there are obstacles.**

```python
>>> grid = [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
>>> dp = [[1] * 4 for _ in range(3)]          # the free base-case trick
>>> for r in range(1, 3):
...     for c in range(1, 4):
...         dp[r][c] = 0 if grid[r][c] else dp[r-1][c] + dp[r][c-1]
>>> dp[2][3]
10
```

**Ten, when the answer is seven — and ten is exactly the answer for this grid with no obstacle at all.** The
top row was left as all ones, so the cell after the obstacle was treated as reachable and the block might as
well not have been there. **You cannot go round it, because you cannot move up.** The trick that is free
without obstacles is wrong with them.

**Keeping the counting base cases in min-path-sum.**

```python
>>> grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
>>> dp = [[0] * 3 for _ in range(3)]          # zeros, no running sums
>>> for r in range(1, 3):
...     for c in range(1, 3):
...         dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
>>> dp[2][2]
2
```

**Two, when the answer is seven.** The first row and column were left as zeros, so the algorithm believes it
can reach any edge cell for free and then drop straight into the corner. **The base cases follow from the
question, not from the last problem you solved.**

**Applying the one-row trick where a cell reads to the right.**

```python
>>> # min falling path: dp[r][c] reads row[c-1], row[c], row[c+1]
>>> row = [2, 1, 3]
>>> for c in range(3):                        # in place: WRONG
...     row[c] = min(row[max(c-1,0):min(c+2,3)])
>>> row
[1, 1, 1]
```

**`row[c-1]` has already been overwritten with this row's value**, so the recurrence reads the wrong
generation. **The one-row trick works only when every dependency is above or to the left** — and this variant
reads to the right, so it needs two arrays.

**Returning the last cell from `maximal_square`.**

```python
>>> # dp[r][c] is the largest square ENDING at (r,c)
>>> # the largest square in the grid can end anywhere
>>> # returning dp[-1][-1] gives the square in the bottom-right corner only
```

**"Ending exactly at" states need `max` over the table**, exactly like longest increasing subsequence. **The
plain path-counting state does not**, because it covers the whole journey. **Knowing which kind you have is
the point.**

**Off-by-one in the formula.**

```python
>>> math.comb(3 + 7, 3)                       # forgot the -2 and the -1
120
>>> math.comb(3 + 7 - 2, 3 - 1)
28
```

**120 against 28.** The moves are `m + n - 2` because you start on a cell rather than before one, and you
choose `m - 1` downs, not `m`. **Check it against a 2×2 grid, where the answer is obviously 2**, before
trusting it.

**Offering the formula on an obstacle grid.**

```python
>>> unique_paths_formula(3, 4)
10
>>> unique_paths_with_obstacles([[0,0,1,0],[0,0,0,0],[0,0,0,0]])
7
```

**The formula counts all paths and knows nothing about blocking.** Offering it without saying "no obstacles"
is worse than not offering it, because it looks like a memorised trick rather than an understood one.

**Overflow, in other languages.**

```
a 40 x 40 grid has C(78, 39) ~ 1.1 x 10^22 paths
a Java long holds up to 9.2 x 10^18

-> silent wraparound, and a plausible negative number
```

**Python is unbounded so this cannot happen there**, which makes it easy to forget when porting. **If the
problem mentions a modulus, that is why.**

**An empty grid.**

```python
>>> min_path_sum([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in min_path_sum
    rows, cols = len(grid), len(grid[0])
IndexError: list index out of range
```

**`grid[0]` on an empty list.** One guard at the top, and it is the kind of thing an interviewer adds as a
test case at the end.

---

## 8. In the interview

### How it gets asked

- *"How many unique paths are there from the top-left to the bottom-right, moving only right and down?"* —
  LeetCode 62.
- *"Now some cells are blocked."* — LeetCode 63, and the base case is the trap.
- *"Find the path with the smallest sum."* — LeetCode 64.
- *"Can you reduce the space?"* — the one-row question, and it is always asked.
- *"Is there a solution without any table at all?"* — the combinatorics question.
- *"What if you can also move diagonally?"*

### The first ninety seconds

> "The state here is the most direct one in dynamic programming, which is worth saying because the last few
> problems have all needed careful redefinition. **`dp[r][c]` is the number of ways to reach the cell at row
> `r`, column `c`.** The grid is the table.
>
> **The recurrence is an addition.** You can only arrive at a cell from above or from the left, so
> `dp[r][c] = dp[r-1][c] + dp[r][c-1]`.
>
> **And the reason adding is correct is worth one sentence**, because counting problems are usually where
> double-counting hides: **every path into this cell arrived through exactly one of those two neighbours, never
> both, so adding counts each path once.**
>
> **Base cases: the first row and the first column are all ones.** In the top row you can only have come from
> the left, so there is exactly one route to each cell. **And `dp[0][0] = 1` — one way to be where you start.**
> Initialising the whole table to one gives me both for free.
>
> **`O(rows × cols)` time and space.**
>
> **And I would reduce the space immediately, because it is unusually clear here.** `dp[r][c]` reads only the
> cell above and the cell to the left, so **one array is enough**: iterate left to right, and `row[c]` before I
> overwrite it still holds the previous row's value — **that is the cell above** — while `row[c-1]` has already
> been updated this pass — **that is the cell to the left.** Both are exactly what I need.
>
> **`O(cols)` space, and `O(min(rows, cols))` if I swap the dimensions first.** At a thousand by a thousand
> that is eight kilobytes instead of forty megabytes.
>
> **There is also a closed form for this exact version.** Every path is `m + n - 2` moves of which `m - 1` are
> down, so the count is `C(m + n - 2, m - 1)` — **twenty-eight for a three by seven grid** — computable in
> `O(min(m, n))` with no table.
>
> **And I would immediately say the limitation: it counts all paths, so a single obstacle destroys it.** There
> is no closed form once some cells are blocked, and then the DP is the only answer.
>
> **Which version would you like — the plain count, obstacles, or minimum cost? Because the base cases differ
> between them, and that is where the bugs are.**"

### The follow-ups

**"Now some cells are blocked."**

> "The recurrence barely changes and the base case changes completely, which is the opposite of what people
> expect.
>
> **The recurrence: a blocked cell has zero paths through it**, so `dp[r][c] = 0`. And that is all — **the
> addition propagates the zero automatically** to every cell downstream, because those paths simply are not
> there to be added.
>
> **The base case is the trap.** Without obstacles, the first row is all ones. **With obstacles, it is ones
> until the first blocked cell and zeros after it** — because you cannot go round an obstacle in the top row,
> since going round would require moving up, and up is not a legal move.
>
> **So the trick of initialising the whole table to one is now wrong**, and it gives a plausible answer rather
> than an error. On a three-by-four grid with one obstacle in the top row it says ten — which is exactly the
> answer for the same grid with no obstacle at all — and the answer is seven.
>
> **The clean way to write it is to handle the first row inside the same loop as every other row** — set
> `row[0] = 1` before starting, iterate `r` from zero, and let the obstacle check apply uniformly. **No separate
> base-case pass means no separate base-case bug.**
>
> **Two edge cases I would check explicitly**: the start blocked, and the destination blocked. **Both are zero**,
> and the start one in particular will otherwise propagate a `1` from an initialisation that should never have
> happened.
>
> **And this is where the combinatorial formula dies.** `C(m+n-2, m-1)` counts every arrangement of moves, and
> it has no way to express 'except the ones through this cell'. **You could try inclusion-exclusion for a
> single obstacle, and it becomes intractable for several** — so the DP is not a fallback here, it is the
> answer."

**"Reduce the space."**

> "One array instead of the table, and this is the clearest example of the trick in the whole subject because
> you can point at the two values.
>
> **`dp[r][c]` reads exactly two cells: the one above and the one to the left.** Nothing else. So I never need
> more than one row of history.
>
> **Keep one array of length `cols`, and iterate left to right.** When I am at column `c`:
>
> **`row[c]`, which I have not yet overwritten on this pass, still holds the value from the previous row —
> that is the cell above.** **`row[c-1]`, which I overwrote a moment ago, holds this row's value — that is the
> cell to the left.**
>
> **So `row[c] += row[c-1]` is exactly the recurrence**, and the array holds the previous row to the right of
> the cursor and the current row to the left of it.
>
> **`O(cols)` space, and I would swap the dimensions first if `rows < cols`** so it becomes `O(min(rows,
> cols))`. At a thousand by a thousand that is eight kilobytes against forty megabytes; at ten thousand square
> it is the difference between eighty kilobytes and four gigabytes — **so it is not a constant-factor tidy-up,
> it is what makes large grids possible at all.**
>
> **Two things I would flag.** **Reconstruction is gone** — if you want the actual path and not just the count
> or cost, you need the full table, or Hirschberg-style divide and conquer.
>
> **And the trick has a precondition that is easy to violate.** It works because every dependency is above or
> to the left. **In a variant where a cell reads the previous row's cell to its right** — minimum falling path,
> where the moves are down-left, down and down-right — **that cell has already been overwritten with the
> current row's value**, and the in-place version silently computes the wrong thing. **That one needs two
> arrays**, and noticing why is a better demonstration than the collapse itself."

**"Is there a way to do this without a table at all?"**

> "Yes, for the plain counting version, and it is combinatorics rather than dynamic programming.
>
> **Every path from the top-left to the bottom-right of an `m × n` grid consists of exactly `m - 1` downward
> moves and `n - 1` rightward moves**, in some order. It cannot be otherwise — you must descend `m-1` rows and
> cross `n-1` columns, and no move is ever wasted because you can never go back.
>
> **So a path *is* a sequence of `m + n - 2` moves, and it is completely determined by which of them are
> down.** Counting paths is counting which positions in that sequence are the downs.
>
> **That is `C(m + n - 2, m - 1)`.** For three by seven: `C(8, 2)` = 28. Same answer as the table.
>
> **`math.comb` computes it with about `min(m, n)` multiplications and constant space** — microseconds against
> a million cells for a thousand-square grid.
>
> **And I would immediately state the limitation, because offering this without it looks like a memorised
> trick.** It counts *every* arrangement of moves. **The moment a cell is blocked, some arrangements are
> illegal and the formula has no way to express that.** You could handle one obstacle with inclusion-exclusion
> — count all paths, subtract those through the obstacle — and with several obstacles the number of terms
> explodes and it becomes worse than the DP.
>
> **Same for costs.** Minimum path sum has no closed form at all, because the answer depends on the actual
> values in the grid rather than only on its shape.
>
> **One practical note: the numbers get large fast.** A forty-by-forty grid has about 10²² paths, which
> overflows a 64-bit integer silently. **Python is unbounded, so I would not notice — which is exactly why the
> problem sometimes asks for the answer modulo 10⁹+7**, and if it does, the formula needs modular inverses
> while the DP just takes the modulus at each addition. **That would push me back to the DP.**"

### The model answer

*"A delivery robot moves through a warehouse laid out as a grid. It can only move east or south. Some cells
are blocked by shelving, and each open cell has a cost representing how congested it is. Find the cheapest
route, and tell me how many equally cheap routes there are."*

> "Two questions on the same grid, and they need slightly different machinery, so let me take them in order.
>
> **The state is the position: `dp[r][c]` is the cheapest cost to reach cell `(r, c)` from the start.** No
> redefinition needed — the grid is the table, and the position is a complete state, because how the robot got
> there does not affect what it can do next.
>
> **The recurrence: `dp[r][c] = cost[r][c] + min(dp[r-1][c], dp[r][c-1])`** — arrive from above or from the
> left, take the cheaper, add this cell's congestion.
>
> **Blocked cells are infinity, not zero**, and that distinction matters here. In the counting version a
> blocked cell is zero because it contributes no paths. **In the cost version zero would mean 'free to pass
> through', which is the opposite of blocked** — so I use `float('inf')`, and the `min` naturally refuses to
> route through it.
>
> **Base cases, and this is where the bug usually is.** The first row and column are **running sums**, not
> ones and not zeros: along the top edge there is exactly one route, so its cost is everything before it
> accumulated. **And once the top row hits a shelf, everything after it in that row is unreachable** —
> infinity, propagated.
>
> **Now the second question, the count of equally cheap routes**, which needs a second table alongside.
>
> **`ways[r][c]` is the number of cheapest routes reaching `(r, c)`.** When I compute the cost I compare the
> two predecessors: **if one is strictly cheaper, this cell inherits its count. If they are equal, it gets the
> sum of both.** That replace-versus-add distinction is exactly the one from counting longest increasing
> subsequences, and getting it backwards gives plausible wrong numbers.
>
> **Two tables, same loops, one pass.**
>
> **Cost: `O(rows × cols)` time.** For a warehouse that is realistically a few hundred by a few hundred — under
> a hundred thousand cells — that is instant, and **I would use the full tables rather than the one-row
> collapse**, because the prompt asks for the route, and reconstruction needs the table. **I would say that
> trade explicitly**: the one-row version is `O(cols)` space and cannot tell me the path.
>
> **Reconstruction: walk back from the destination**, at each step moving to whichever predecessor produced the
> value, with guards for the top row and left column where only one direction exists.
>
> **Three things about the problem domain I would raise.**
>
> **The move restriction is doing a lot of work and I would check it is real.** East-and-south-only is what
> makes this a DP with no cycles. **If the robot can also go west or north, this is not a grid DP at all — it
> is Dijkstra on a graph**, because paths can revisit regions and there is no acyclic ordering to fill in. That
> is a completely different algorithm and it is worth confirming before writing anything.
>
> **The congestion costs presumably change over time**, and the table is a snapshot. If congestion updates
> every few seconds, recomputing a hundred thousand cells is cheap enough to just redo — **but a route computed
> at the start may be stale by the time the robot is halfway**, so I would recompute from the robot's current
> position rather than committing to the whole route up front.
>
> **And the count of equally cheap routes is more useful than it sounds.** If there are many, the robot has
> flexibility and I can pick one that avoids other robots. **If there is exactly one, that route is a
> bottleneck** and worth flagging to whoever laid out the shelving."

---

## 9. Recall card

**The most direct state in DP: `dp[r][c]` is the answer for that cell — the grid is the table.** Every path
arrives from **above or left, never both**, so `dp[r][c] = dp[r-1][c] + dp[r][c-1]` counts each path exactly
once. Base cases: **first row and column are 1** (initialise the whole table to 1 and get them free).

**The one-row collapse is clearest here:** iterate left to right, and **`row[c]` (not yet overwritten) is the
cell above while `row[c-1]` (just overwritten) is the cell to the left.** `O(cols)` space — 8 KB against 40 MB
at 1,000², and 80 KB against 4 GB at 10,000². **It fails when a cell reads the previous row to its *right*
(minimum falling path) — that needs two arrays.**

**Obstacles: a blocked cell is 0 and the addition propagates it — but the first row is now ones until the
first block and zeros after**, because you cannot go round. **The initialise-to-1 trick becomes wrong**, giving
11 instead of 7.

**Minimum path sum: same state, `min` instead of `+`, and the base cases become RUNNING SUMS** — keeping the
counting base cases is the standard bug. **A blocked cell is `inf` here, not 0** — zero would mean free.

**Closed form for the plain count: a path is `m+n-2` moves of which `m-1` are down, so `C(m+n-2, m-1)`** —
28 for 3×7, `O(1)` space. **Always say the limitation in the same breath: one obstacle destroys it**, and
costs have no closed form at all.

**Counts grow fast** (40×40 ≈ 10²², overflowing a 64-bit integer silently) — which is why a modulus appears.
**And `maximal_square`'s state is "ending at", so its answer is `max` over the table, not the last cell.**
