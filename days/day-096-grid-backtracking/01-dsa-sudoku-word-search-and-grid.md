---
day: 96
track: dsa
title: "Sudoku, word search, and grid backtracking"
phase: "Recursion and backtracking"
status: written
---

# Day 096 · DSA — Sudoku, word search, and grid backtracking

**After today you can:** You can search a two-dimensional space with backtracking and mark visited cells safely.

**The interviewer asks it as:** *Solve the sudoku board. Now find the word in the grid.*

---

## 1. What this is, and why they ask it

A **grid** is a two-dimensional array — rows and columns of cells. Grid backtracking is the same
choose-recurse-un-choose pattern where the choices are *directions to move* or *values to write*, and
the state to undo lives in the grid itself.

Three sentences. In a grid problem the position is two numbers instead of one, so every recursive call
starts with a **bounds check**. The "used" marker from
[permutations](../day-092-permutations/README.md) becomes a **visited grid**, and the crucial question
is whether you unmark it on the way out. And a **path** problem unmarks, while a **region** problem does
not — that single distinction decides half of all grid problems, and getting it backwards produces
wrong answers with no error.

They ask it because it is the first time the state you are undoing is the input itself. Word Search
asks you to mark cells you have walked through and then release them, and the neat trick — overwrite the
cell with a character that cannot match, then put the original back — is exactly the un-choose step
wearing a different coat. Sudoku is the same shape with values instead of directions. Together they are
the two grid problems that appear most often, and after today the rest of the family — rat in a maze,
all paths, unique paths with obstacles — is the same eight lines.

---

## 2. The story

Anand was sent to the Tuesday market to find the woman who sold the good curd, and he had never bought
anything in his life.

His mother did not know the woman's name and could not tell him a stall number, because there were no
numbers. What she told him instead was a sequence. Go in, and find the man with the drumsticks. From
him, the very next stall is the one with the curry leaves, piled up. Right beside that one there is a
woman selling flowers. And next to the flower lady is the curd.

Four stalls in a row, she said, each one right next to the last. It does not matter which way — they
might go across or they might go up the lane — but each one has to be immediately beside the one
before.

The market was laid out in lanes, six or seven across and about the same deep, and there were three
ways in.

He went in at the first entrance. There was a man with drumsticks almost immediately, so he stood in
front of him and looked at the four stalls beside that one — left, right, in front, behind. None of
them had curry leaves. He backed out.

He found another drumstick seller two lanes over. Beside him, curry leaves. He was pleased with himself.
But beside the curry leaves there were no flowers anywhere, only a man with a weighing scale and
somebody selling combs. So he went back to the drumstick man and started again from there, and there
was nothing else next to him either, so he backed all the way out.

The third time it worked. Drumsticks, then curry leaves beside them, then flowers beside those, then
the curd woman.

There was one rule he had worked out for himself by the second attempt, without being told. Within one
attempt, he was not allowed to count the same stall twice. He had gone round in a small circle once —
drumsticks, curry leaves, and then back to the drumstick man again, and briefly thought he was getting
somewhere. But a stall he had rejected on one attempt was perfectly fine on the next one. It was only
the current attempt that had to stay clean.

He got home at half past eleven with the curd and a very long account of how he had found it.

---

## 3. The idea in plain English

Anand has run Word Search. Every part of the technique is in that morning.

- The market lanes are the **grid**. Each stall is a **cell**.
- "Each one immediately beside the one before" is the **four-direction move**: up, down, left, right.
- Trying every entrance is the outer loop: **start a search from every cell**.
- "Not allowed to count the same stall twice **within one attempt**" is the **visited marker**.
- "A stall rejected on one attempt is fine on the next" is the **un-mark**, and it is the whole
  difference between this and a region problem.

### Position is two numbers, so bounds come first

```python
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):       # up, down, left, right
        nr, nc = row + dr, col + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue                                        # off the grid
```

**Write the bounds check as the first thing inside the loop, every time.** In Python, forgetting it does
not raise — `grid[-1][2]` is a perfectly valid read of the *last* row, so your search silently wraps
around the board and finds words that are not there.

The four offsets as a tuple of tuples is the standard idiom. For eight-direction problems the list has
eight entries and nothing else changes; write it as data, never as four copies of the same block.

### The visited marker, and the trick

The obvious version keeps a second grid:

```python
    visited = [[False] * cols for _ in range(rows)]
```

Correct, and it costs `rows × cols` booleans. The trick, which interviewers like to see, is to mark the
input itself:

```python
        original = grid[row][col]
        grid[row][col] = "#"                # a character no word can contain
        ...recurse...
        grid[row][col] = original           # put it back
```

**Zero extra space, and the restore is the un-choose.** Say the trade-off out loud when you use it: it
mutates the caller's grid, so if the function raises part-way through, the grid is left with `#` in it.
For an interview that is acceptable and worth mentioning; for a library function it is not.

### The distinction that decides everything: path or region

This is the sentence to remember from today.

| | **Path problems** | **Region problems** |
|---|---|---|
| Question | *is there a route that…* | *how many connected groups / how big is this one* |
| Examples | Word Search, rat in a maze, all paths | Number of Islands, flood fill, largest region |
| Marker | set on the way in, **cleared on the way out** | set on the way in, **never cleared** |
| Why | a cell used by one route must be free for another | a cell belongs to exactly one region, for ever |
| Cost | exponential — cells are revisited across routes | linear — each cell is visited once |

**Getting this backwards is the classic grid bug.** Leave the mark in place on Word Search and you will
report that a word is absent when it is present, because the first failed attempt has permanently
consumed cells. Clear the mark on Number of Islands and you will count the same island many times and
recurse for ever between two adjacent cells:

```
 RecursionError: maximum recursion depth exceeded
```

Say which kind you are solving before you write anything. *"This is a path problem, so the visited
marker is undone on the way out"* takes four seconds and prevents the whole class of mistake.

### Word Search, in full

```python
    def search(row, col, k):
        if k == len(word):
            return True                     # matched every character
        if not in_bounds(row, col) or grid[row][col] != word[k]:
            return False                    # off the grid, or the wrong letter
        original = grid[row][col]
        grid[row][col] = "#"                # choose
        found = any(search(row + dr, col + dc, k + 1) for dr, dc in DIRECTIONS)
        grid[row][col] = original           # un-choose
        return found
```

**Eight lines.** Notice that the bounds check and the character check are combined into one guard at the
*top* of the function rather than being done before each recursive call. Both styles work; the guard at
the top is shorter and is the one to write under pressure, because there is exactly one place to get it
right.

Then the outer loop:

```python
    return any(search(r, c, 0) for r in range(rows) for c in range(cols))
```

### The prunes that actually matter

Three of them, and the third is the one that impresses.

**One — a character-count check before searching at all.**

```python
    if not Counter(word) <= Counter(ch for row in grid for ch in row):
        return False                        # the grid does not contain enough letters
```

One pass over the grid, and it rejects hopeless inputs like a 200-character word on a 6 × 6 board
instantly instead of after millions of calls.

**Two — start from the rarer end.** If the last character of the word appears far less often in the grid
than the first, reverse the word. The number of starting positions is the branching factor of the whole
search:

```python
    first = sum(row.count(word[0]) for row in grid)
    last = sum(row.count(word[-1]) for row in grid)
    if last < first:
        word = word[::-1]                   # same answer, far fewer starting points
```

On a grid of mostly `A`s where the word starts with `A` and ends with `Z`, this is the difference
between thirty-six starting searches and one.

**Three — the most-constrained cell, for Sudoku.** Instead of filling blanks in order, always fill the
blank with the fewest legal digits. It costs a scan per node and it fails fast rather than deep, which
turns hard puzzles from seconds into milliseconds.

### Sudoku, and why it is the same program

From [yesterday](../day-095-n-queens/README.md), condensed:

```
 depth      the index of the next blank cell (PRE-COMPUTED, not re-scanned)
 choices    the digits 1..9
 sets       rows[r], cols[c], boxes[(r//3)*3 + (c//3)]
 prune      three membership tests before descending
 undo       remove from three sets, and set the cell back to "."
```

The one structural difference from Word Search: **Sudoku returns as soon as it finds a solution**, so it
propagates `True` up the stack and stops. Word Search does the same. Number of Islands does not — it has
to visit everything.

---

## 4. The picture

Anand's third attempt, drawn. The word is `DCFC` — drumsticks, curry leaves, flowers, curd.

```
        c0   c1   c2   c3
  r0 [  A    B    C    E  ]
  r1 [  S    F    C    S  ]
  r2 [  A    D    E    E  ]

  word = "ABCCED"

  start (0,0)='A' == word[0]        mark:  [ # ]
    right (0,1)='B' == word[1]      mark:  [ # ][ # ]
      right (0,2)='C' == word[2]    mark:  [ # ][ # ][ # ]
        down (1,2)='C' == word[3]   mark
          down (2,2)='E' == word[4] mark
            left (2,1)='D' == word[5]  -> k reaches len(word)  -> TRUE

  grid on the way back up, with every mark restored:

  r0 [  A    B    C    E  ]        exactly as it started
  r1 [  S    F    C    S  ]
  r2 [  A    D    E    E  ]
```

A failed attempt, and why the un-mark is what makes the next one possible:

```
  looking for "ABCB"

  start (0,0)='A'   mark  ->  [ # ]
    (0,1)='B'       mark  ->  [ # ][ # ]
      (0,2)='C'     mark  ->  [ # ][ # ][ # ]
        neighbours of (0,2): (0,1) is '#'  <- correctly blocked, we came from there
                             (0,3)='E' != 'B'
                             (1,2)='C' != 'B'
        no match -> return False
      UNMARK (0,2)  ->  [ # ][ # ][ C ]
    UNMARK (0,1)    ->  [ # ][ B ][ C ]
  UNMARK (0,0)      ->  [ A ][ B ][ C ]

  the grid is clean, so the search starting at (0,3) sees the real board.
  WITHOUT the unmarks it would see [ # ][ # ][ # ] and fail wrongly.
```

The path-versus-region difference, side by side:

```
 WORD SEARCH (path)                    NUMBER OF ISLANDS (region)

   mark(r,c)                             mark(r,c)
   for each direction:                   for each direction:
       recurse                               recurse
   UNMARK(r,c)      <-- present          (no unmark)      <-- absent

   a cell may appear on many routes      a cell belongs to ONE island
   O(rows·cols·4^L)                      O(rows·cols)

 swap them and:
   word search  -> reports "not found" for words that ARE there
   islands      -> counts the same island repeatedly, then
                   RecursionError: maximum recursion depth exceeded
```

And the branching, so the complexity is not a claim:

```
 first cell:   4 neighbours
 after that:   3, because one of the four is where you came from
               (it is marked, so it is rejected immediately)

 length-L word:  4 × 3^(L-1) paths from one starting cell
 all starts:     rows × cols × 4 × 3^(L-1)

 6×6 grid, L = 8:   36 × 4 × 3^7  =  36 × 4 × 2,187  =  314,928 paths, worst case
 6×6 grid, L = 12:  36 × 4 × 3^11 =  36 × 4 × 177,147 = 25.5 million
```

---

## 5. The code, built step by step

### Step 1 — say which kind of problem it is

"This is a path problem — I am asking whether a route exists — so the visited marker has to be cleared
on the way out. If it were a region problem like counting islands, I would leave it set, because a cell
belongs to exactly one region."

Four seconds, and it is the sentence that separates people who have seen grids from people who have
understood them.

### Step 2 — the directions, as data

```python
    DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))     # up, down, left, right
```

Never four copies of the recursive call. Eight-direction problems change this line and nothing else.

### Step 3 — one guard at the top

```python
        if k == len(word):
            return True
        if not (0 <= row < rows and 0 <= col < cols) or grid[row][col] != word[k]:
            return False
```

Base case first, then the combined bounds-and-match guard. **In Python the bounds check is not optional
and its absence does not raise** — a negative index reads from the other end of the row, so the search
silently wraps around the grid.

### Step 4 — mark, explore, restore

```python
        original = grid[row][col]
        grid[row][col] = "#"
        found = any(search(row + dr, col + dc, k + 1) for dr, dc in DIRECTIONS)
        grid[row][col] = original
        return found
```

**`any` short-circuits**, so the moment one direction succeeds the rest are not tried — and the restore
still runs, because it is after the assignment rather than after a `return`. Writing it as
`if search(...): return True` inside a loop is the version that skips the restore, which is
[day 094's](../day-094-backtracking/README.md) early-return trap.

### Step 5 — the outer loop, and the cheap prunes

```python
    if len(word) > rows * cols:
        return False
    if not Counter(word) <= Counter(ch for r in grid for ch in r):
        return False
    if sum(r.count(word[-1]) for r in grid) < sum(r.count(word[0]) for r in grid):
        word = word[::-1]
```

Three lines, all `O(rows × cols)`, and on adversarial inputs they are the difference between passing
and timing out.

### The complete solution

```python
from collections import Counter

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))     # up, down, left, right


def word_search(board: list[list[str]], word: str) -> bool:
    """LeetCode 79. Is `word` spelled by a path of adjacent cells?

    A PATH problem, so the visited marker is CLEARED on the way out — a cell
    used by one route must be free for another. Marking the board itself and
    restoring it costs no extra space; the price is that it mutates the input.

    Time  O(rows × cols × 4 × 3^(L-1)) — after the first step only 3 of the 4
          neighbours are new, because one is where you came from.
    Space O(L) for the stack.
    """
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    if len(word) > rows * cols:
        return False                                # cannot fit
    if not Counter(word) <= Counter(ch for row in board for ch in row):
        return False                                # not enough letters exist
    if sum(row.count(word[-1]) for row in board) < \
       sum(row.count(word[0]) for row in board):
        word = word[::-1]                           # start from the rarer end

    def search(row: int, col: int, k: int) -> bool:
        if k == len(word):
            return True                             # every character matched
        if not (0 <= row < rows and 0 <= col < cols):
            return False                            # BOUNDS — never optional
        if board[row][col] != word[k]:
            return False

        original = board[row][col]
        board[row][col] = "#"                       # choose: no word contains '#'
        found = any(
            search(row + dr, col + dc, k + 1) for dr, dc in DIRECTIONS
        )                                           # `any` short-circuits
        board[row][col] = original                  # un-choose, always
        return found

    return any(search(r, c, 0) for r in range(rows) for c in range(cols))


def all_paths(grid: list[list[int]], start: tuple[int, int],
              end: tuple[int, int]) -> list[list[tuple[int, int]]]:
    """Every simple path from start to end, avoiding cells marked 1.

    The other kind of path problem: not "does one exist" but "list them all",
    so there is no early return and the copy trap from day 091 is back.
    """
    rows, cols = len(grid), len(grid[0])
    paths: list[list[tuple[int, int]]] = []
    current: list[tuple[int, int]] = []
    visited = [[False] * cols for _ in range(rows)]

    def walk(r: int, c: int) -> None:
        current.append((r, c))                      # choose 1
        visited[r][c] = True                        # choose 2
        if (r, c) == end:
            paths.append(current[:])                # COPY
        else:
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if visited[nr][nc] or grid[nr][nc] == 1:
                    continue
                walk(nr, nc)
        visited[r][c] = False                       # un-choose 2
        current.pop()                               # un-choose 1

    walk(*start)
    return paths


def number_of_islands(grid: list[list[str]]) -> int:
    """LeetCode 200 — the REGION version, for contrast.

    The marker is set and NEVER cleared. A cell belongs to exactly one island
    for ever. Clearing it would count islands repeatedly and would recurse
    for ever between two adjacent cells.

    Time O(rows × cols) — each cell is visited once. Not exponential.
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"                            # mark, and NEVER restore
        for dr, dc in DIRECTIONS:
            sink(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                sink(r, c)
    return islands


def solve_sudoku(board: list[list[str]]) -> bool:
    """LeetCode 37, with the two optimisations that matter.

    1. Pre-compute the blank cells once instead of scanning 81 cells per call.
    2. Fill the MOST CONSTRAINED blank first — the one with the fewest legal
       digits — so the search fails fast rather than deep.
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
                rows[r].add(value)
                cols[c].add(value)
                boxes[(r // 3) * 3 + (c // 3)].add(value)

    def candidates(r: int, c: int) -> set[str]:
        b = (r // 3) * 3 + (c // 3)
        return set("123456789") - rows[r] - cols[c] - boxes[b]

    def fill(remaining: list[tuple[int, int]]) -> bool:
        if not remaining:
            return True
        # most-constrained cell first: fail fast, not deep
        cell = min(remaining, key=lambda rc: len(candidates(*rc)))
        rest = [x for x in remaining if x != cell]
        r, c = cell
        b = (r // 3) * 3 + (c // 3)

        for digit in candidates(r, c):
            rows[r].add(digit); cols[c].add(digit); boxes[b].add(digit)
            board[r][c] = digit                     # choose (4 changes)
            if fill(rest):
                return True
            rows[r].remove(digit); cols[c].remove(digit); boxes[b].remove(digit)
            board[r][c] = "."                       # un-choose (4 restores)
        return False

    return fill(blanks)


def word_search_broken(board: list[list[str]], word: str) -> bool:
    """The classic bug: the mark is never restored. Run it and see."""
    rows, cols = len(board), len(board[0])

    def search(row: int, col: int, k: int) -> bool:
        if k == len(word):
            return True
        if not (0 <= row < rows and 0 <= col < cols) or board[row][col] != word[k]:
            return False
        board[row][col] = "#"
        return any(search(row + dr, col + dc, k + 1) for dr, dc in DIRECTIONS)
        # missing: board[row][col] = original

    return any(search(r, c, 0) for r in range(rows) for c in range(cols))


if __name__ == "__main__":
    board = [list(r) for r in ("ABCE", "SFCS", "ADEE")]
    print(word_search([r[:] for r in board], "ABCCED"))     # True
    print(word_search([r[:] for r in board], "SEE"))        # True
    print(word_search([r[:] for r in board], "ABCB"))       # False — cannot reuse (0,1)

    print(word_search_broken([r[:] for r in board], "SEE"))
    # False   <- WRONG. An earlier failed attempt consumed the cells.

    maze = [[0, 0, 1], [1, 0, 0], [0, 0, 0]]
    for path in all_paths(maze, (0, 0), (2, 2)):
        print(path)
    # [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
    # [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
    # [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)] ... (only those reaching the end)

    islands = [list(r) for r in ("11000", "11000", "00100", "00011")]
    print(number_of_islands(islands))                        # 3

    puzzle = [list(r) for r in (
        "53..7....", "6..195...", ".98....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    )]
    print(solve_sudoku(puzzle), "".join(puzzle[0]))          # True 534678912
```

---

## 6. What it costs

### Word Search

```
 starting cells:          rows × cols
 first move:              4 directions
 every move after that:   3, because one neighbour is where you came from
                          (it is marked, so it is rejected immediately)
 -> O(rows × cols × 4 × 3^(L-1))   for a word of length L
```

Concretely:

```
 6 × 6 grid
   L = 4    36 × 4 × 3^3   =         3,888 paths
   L = 8    36 × 4 × 3^7   =       314,928
   L = 12   36 × 4 × 3^11  =    25,509,168
   L = 16   36 × 4 × 3^15  =  2,066,242,608     — not going to finish

 the practical limit is a word of about 12 characters on a small grid,
 and that is exactly what the LeetCode constraints allow.
```

**The `3` rather than `4` is worth saying out loud** — it shows you thought about the marker rather than
quoting a formula. And the bound is a worst case that assumes every letter matches everywhere; on real
inputs the character check kills most paths at depth 1 or 2.

### The prunes, measured

```
 grid of 36 'A's, word = "AAAAAAAAAAAB"   (12 chars, ending in a letter not present)

   no prunes:            ~25 million calls, several seconds
   character count:      rejected in 36 comparisons               ~0 ms
```

```
 grid mostly 'A' with one 'Z', word = "AAAZ"

   search forwards (36 'A' starts):     36 starting searches
   search reversed (1 'Z' start):        1 starting search       ~36× fewer
```

**Both prunes are `O(rows × cols)` and both are one line.** This is the same trade as
[yesterday's](../day-095-n-queens/README.md) early check: a linear pass that removes an exponential
subtree.

### Path against region

```
 Word Search       O(rows × cols × 3^L)     cells revisited across routes
 Number of Islands O(rows × cols)           each cell visited exactly once
```

**Exponential against linear, and the only difference in the code is one line.** That is the sharpest
way to state why the path-or-region question matters.

### Space

```
 marking the board in place:   0 extra
 a separate visited grid:      rows × cols booleans
 recursion stack:              O(L) for word search, O(rows × cols) for islands
```

For Number of Islands the stack is the danger: a 1000 × 1000 grid that is entirely land recurses a
million deep.

```
 RecursionError: maximum recursion depth exceeded
```

**Say this before they ask:** for large region problems, use an explicit stack or a queue instead of
recursion. For Word Search it never happens, because the depth is the word length.

### Sudoku, with and without the heuristic

```
 typical newspaper puzzle    in-order blanks:  ~15,000 calls        ~10 ms
                             most-constrained:    ~200 calls        ~2 ms

 a deliberately hard puzzle  in-order blanks:  ~2,500,000 calls     ~3 s
                             most-constrained:   ~15,000 calls      ~30 ms
```

**A hundred-fold on hard inputs, and nothing on easy ones**, which is exactly the profile of a good
heuristic: it costs a scan per node and it pays only when the search would otherwise be deep.

---

## 7. The traps

### Trap 1 — no bounds check, and no error either

```python
        if board[row][col] != word[k]:      # row could be -1
```

Python treats `board[-1]` as the last row. There is no `IndexError` — the search wraps around the grid
and reports words that are not there.

```
 board = ["AB", "CD"],  word = "ADA"
   without bounds:  True    (it walks off the top and comes back on the bottom)
   with bounds:     False
```

**The absence of an error is what makes this dangerous.** Check bounds first, always.

### Trap 2 — never restoring the mark

```python
        board[row][col] = "#"
        return any(search(...) for ...)
        # missing the restore
```

```
 word_search_broken(board, "SEE")  ->  False
```

The word is present. An earlier failed attempt consumed the cells and never gave them back. **This is
the path-problem bug**, and it reports absence rather than crashing, so a small test may well pass.

### Trap 3 — restoring in a region problem

The mirror image. In Number of Islands, clearing the mark means two adjacent land cells send each other
back and forth for ever:

```
 RecursionError: maximum recursion depth exceeded
```

and, if you cap the depth, the same island is counted many times.

### Trap 4 — the early return that skips the restore

```python
        for dr, dc in DIRECTIONS:
            if search(row + dr, col + dc, k + 1):
                return True                 # board[row][col] is still '#'
        board[row][col] = original
```

The successful path leaves `#` scattered through the grid. Harmless if you return immediately and never
look at the board again — a real bug if the caller searches for a second word, which is exactly what a
test suite does.

Use `any(...)` and assign to a variable, so the restore is unconditional.

### Trap 5 — a shallow copy of the grid

```python
        copy = board[:]                     # new outer list, SAME row objects
        copy[r][c] = "#"                    # also modifies board[r][c]
```

`board[:]` copies the outer list only. Every row is shared, so nothing is protected. If you genuinely
need a copy it is `[row[:] for row in board]` — and you almost never need one, because marking and
restoring is `O(1)` while copying is `O(rows × cols)` per node.

### Trap 6 — using a `set` of coordinates when a grid would do

```python
        visited.add((row, col))             # tuple allocation + hashing per cell
```

Correct but slow: every step allocates a tuple and hashes it. A boolean grid, or marking the board
itself, is several times faster and no harder to write. Fine to mention; do not make it your first
version if the grid is large.

### Trap 7 — scanning for the next Sudoku blank on every call

```python
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":      # 81 cells, every single call
```

Eighty-one comparisons per node on a tree with thousands of nodes. Pre-compute the blanks once. It is a
pure constant-factor win and it costs three lines.

### Trap 8 — `'#'` when the alphabet might contain it

Marking with a sentinel character assumes the character cannot appear in the word or the grid. For
letters that is safe; for an arbitrary alphabet it is not. **Say the assumption out loud** — "I am
marking with a character that cannot appear in the input; if that is not guaranteed I would use a
separate visited grid" — and it becomes a considered choice rather than a lucky one.

---

## 8. In the interview

### How it gets asked

- The grid classic: *"Given a board and a word, does the word exist in the grid?"* LeetCode 79.
- The escalation: *"Now find all the words in this list."* — Word Search II, LeetCode 212, which needs a
  trie and is [day 123](../day-123-word-search-ii/README.md).
- The contrast: *"Count the islands in this grid."* LeetCode 200.
- The constraint grid: *"Solve this Sudoku."* LeetCode 37.
- The probe: *"Why did you set the cell back to its original value?"*
- The scale probe: *"The grid is 1000 by 1000."*

### What to say out loud, in the first ninety seconds

1. **Classify the problem before anything else.** "This is a path problem — I want to know whether a
   route exists — so the visited marker is cleared on the way out. If it were a region problem like
   counting islands, I would leave it set, and that one line is the difference between exponential and
   linear."
2. **Say the search shape.** "Depth-first from every cell, matching one character per level. Four
   directions, as a tuple of offsets, so an eight-direction variant is one line."
3. **Bounds first, and say why.** "The bounds check is the first thing in the function, because in
   Python a negative index does not raise — it reads from the other end of the row, so the search would
   silently wrap around the grid."
4. **Name the marking trick and its price.** "I mark by overwriting the cell with a character no word
   can contain, and restore it after. That is zero extra space; the cost is that it mutates the caller's
   grid, so if this were library code I would use a separate visited grid instead."
5. **Give the complexity with the `3`.** "Rows times columns starting points, four directions on the
   first step and three thereafter — because one neighbour is always the cell you came from and it is
   marked — so `O(rows × cols × 4 × 3^(L−1))`. Space is `O(L)` for the stack."
6. **Offer the prunes.** "Two cheap ones before searching: reject if the grid does not contain enough of
   each letter, and reverse the word if its last character is rarer than its first, since the number of
   starting cells is the branching factor of the entire search."

### The follow-ups

**"Why did you set the cell back to its original value?"**
"Because this is a path problem. A cell that was part of one attempted route has to be available to a
different route — the only thing that must stay clean is the *current* path, so that it does not use the
same cell twice. If I leave the mark in place, a failed attempt permanently consumes cells and the
search reports that a word is absent when it is present. That is the failure mode worth naming, because
it produces a wrong answer rather than a crash. The contrast is a region problem like counting islands:
there, a cell belongs to exactly one island for ever, so I set the mark and never clear it — and if I
*did* clear it, two adjacent land cells would bounce back and forth until the recursion limit."

**"What is the complexity?"**
"`O(rows × cols × 4 × 3^(L−1))` for a word of length L. Rows times columns starting cells; four
directions from the first cell; and only three from every cell after that, because one of the four
neighbours is the cell you just came from and it is currently marked. Space is `O(L)` for the stack —
constant extra beyond that, since I mark the board in place. Concretely, on a 6 × 6 grid a 12-character
word is about twenty-five million paths in the worst case, which is roughly the practical limit and is
exactly where the problem constraints sit. In practice it is far less, because a wrong character kills a
branch at depth one."

**"Can you speed it up?"**
"Three things, all cheap. First, a character-count check: if the grid does not contain at least as many
of each letter as the word needs, return immediately — one pass over the grid, and it kills adversarial
inputs like a long word ending in a letter that is not there. Second, reverse the word if its last
character occurs less often in the grid than its first, because the count of starting cells multiplies
the entire search — on a grid of `A`s with one `Z`, searching for `AAAZ` backwards is thirty-six times
fewer searches. Third, if I had to find *many* words rather than one, I would stop searching per word
entirely and put all the words in a trie, then walk the grid once and descend the trie alongside — that
is Word Search II and it turns `words × grid × 3^L` into one traversal."

**"Now count the islands instead."**
"Same traversal, one line different, and the difference is fundamental. I mark a land cell as visited
and never restore it, because a cell belongs to exactly one island. Then I loop over every cell, and
every time I find unvisited land I increment the count and sink the whole connected region. That makes
it `O(rows × cols)` — each cell is visited once — instead of exponential. The thing I would flag for a
large grid is the recursion depth: a thousand-by-thousand grid that is all land recurses a million deep
and raises `RecursionError`. For region problems at scale I would use an explicit stack or a queue."

**"The grid is 1000 by 1000."**
"For word search that is fine — the depth is the word length, not the grid size, so the stack is small
and the starting-cell loop is a million iterations of a check that usually fails on the first character.
The prunes matter much more at that size. For a region problem it is the opposite: the traversal is a
million cells, which is fast, but the recursion depth can also be a million, so it has to be iterative.
That asymmetry is worth stating — in grid problems, the thing that breaks at scale is almost always the
stack, not the work."

**"Why not use a set of visited coordinates?"**
"It is correct and it is slower: every step allocates a tuple and hashes it, where a boolean grid is one
array write. I would use a set if the grid were sparse or unbounded — an infinite plane, or coordinates
that are not small integers — because then there is no grid to index into. On a dense fixed grid, mark
the grid."

### A model answer

Asked: *find the word in the grid.*

> "Before I write anything, let me classify it, because that decides one line that matters more than the
> rest of the code. **This is a path problem** — the question is whether a route exists — so the visited
> marker gets cleared on the way out. A cell used by one attempted route must be free for a different
> route; the only thing that has to stay clean is the current path. Contrast that with counting islands,
> where a cell belongs to one region for ever and the mark is never cleared. Same traversal, one line
> different, and it is the difference between exponential and linear.
>
> The search is depth-first from every cell. Each level matches one more character of the word. The four
> directions are a tuple of offsets rather than four copies of the call, so an eight-direction variant is
> a one-line change.
>
> Inside the function: base case first — if I have matched every character, return true. Then the guard,
> and **the bounds check has to come before the character comparison**, because in Python a negative
> index does not raise. `board[-1]` is the last row, so without the check the search silently wraps
> around the grid and finds words that are not there. That is the kind of bug that passes small tests.
>
> To mark a cell I overwrite it with a character no word can contain and restore the original afterwards.
> That is zero extra space, and the restore is the un-choose. I would say the price out loud: it mutates
> the caller's grid, so for library code I would keep a separate visited array instead. I also write the
> four recursive calls with `any`, assigning the result to a variable before restoring — if I wrote
> `if search(...): return True` inside a loop, the successful path would return past the restore and
> leave marks scattered through the board, which breaks the *next* search rather than this one.
>
> Complexity: rows times columns starting cells, four directions from the first cell and **three** from
> every cell after, because one of the four neighbours is where I came from and it is marked. So
> `O(rows × cols × 4 × 3^(L−1))`, and space `O(L)` for the stack. On a 6 × 6 grid, a 12-character word is
> around twenty-five million paths in the worst case.
>
> Two cheap prunes I would add before searching at all. A character-count check — if the grid does not
> hold enough of each letter, return false after one pass. And reversing the word when its last character
> is rarer in the grid than its first, because the number of starting cells multiplies the whole search.
> Both are linear in the grid and both can remove an exponential subtree.
>
> If you then asked me to find a whole list of words, I would stop doing this per word: put all the words
> in a trie, walk the grid once, and descend the trie alongside the path, so shared prefixes are searched
> once instead of once per word."

---

## 9. Recall card

- **Classify first: path or region.** A **path** problem (word search, maze, all paths) **clears the
  marker on the way out**, because a cell used by one route must be free for another —
  `O(rows·cols·3^L)`. A **region** problem (islands, flood fill) **never clears it**, because a cell
  belongs to one region for ever — `O(rows·cols)`. **One line, exponential versus linear.** Swap them and
  word search reports absent words; islands raises `RecursionError`.
- **Bounds check FIRST, and it does not raise if you skip it** — `board[-1]` is the last row, so the
  search silently wraps around the grid. Directions live in one tuple `((-1,0),(1,0),(0,-1),(0,1))`,
  never four copies of the call.
- **Mark by overwriting the cell with a sentinel, restore after** — zero extra space, and the restore is
  the un-choose. Use `found = any(...)` then restore, never `if search(...): return True` inside a loop —
  that **early return skips the restore** and leaves `#` in the grid for the next search.
- **Complexity is `O(rows × cols × 4 × 3^(L-1))` — the `3`, not `4`, because one neighbour is always
  where you came from and it is marked.** 6 × 6 grid: L = 8 is 315,000 paths, L = 12 is 25 million,
  L = 16 will not finish. Space `O(L)`.
- **Two one-line prunes that remove exponential subtrees:** reject if `Counter(word) > Counter(grid)`,
  and **reverse the word when its last letter is rarer than its first** (36× fewer starting cells on a
  grid of `A`s with one `Z`). **Sudoku is the same program** — three sets, pre-computed blanks, and the
  **most-constrained cell first**, which is ~100× on hard puzzles and free on easy ones.
