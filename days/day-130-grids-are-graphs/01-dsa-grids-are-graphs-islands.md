---
day: 130
track: dsa
title: "Grids are graphs: islands and flood fill"
phase: "Graphs"
status: written
---

# Grids are graphs: islands and flood fill

## 1. What this is, and why they ask it

A grid is a graph. Every cell is a vertex, and every pair of touching cells is an edge. That sentence is the
entire lesson, and once you have it, every grid problem in every interview becomes a traversal you already
know how to write.

The reason it needs its own day is that grid problems do not look like graph problems. There is no edge list,
no adjacency structure, nothing to build. The graph is **implicit** — the neighbours of a cell are computed
from its coordinates, not looked up — and a large number of candidates never make the connection at all. They
write nested loops and clever conditions and get lost, when the answer was BFS with a four-line neighbour
function.

They ask grid problems constantly, more than any other kind of graph problem. Number of Islands is probably
the single most-asked graph question in the industry. Flood fill, rotting oranges, surrounded regions, maximum
island area, shortest path in a maze, walls and gates — all the same shape, all worth about twenty minutes,
all solved by the same twenty lines.

There is also one specific detail that decides whether your code works, and it is not the traversal: **the
bounds check**. Off the grid by one cell is an `IndexError` if you are lucky and a wrong answer if you are
not, because Python's negative indices wrap around silently.

By the end of this lesson you can write the neighbour function from memory, choose between BFS and DFS for a
grid on the right grounds, handle four-way and eight-way adjacency, recognise the multi-source variant, and
name the two ways grid solutions crash on large inputs.

---

## 2. The story

It rained hard on Tuesday night and Ramesh goes up to the terrace on Wednesday morning to push the water off,
the way he does after every serious rain.

The terrace is about forty feet by twenty-five, done in grey tiles, and it is not flat. It has never been
flat. There is a slope towards the drain in the far corner that works reasonably well over most of the
surface, and then there are the parts where it does not work at all.

He stands at the top of the stairs with the rubber squeegee and looks at what he has got.

There is a big one in the middle, roughly the shape of a comma, maybe fifteen feet across at its widest. There
is a long thin one running along the parapet on the left where the tiles have sunk. There is a small round one
near the water tank, and two more small ones over by the corner that he cannot see properly from here.

He starts with the big one. He puts the squeegee down at the near edge and pushes, and the whole thing moves —
all of it, together, because it is all one body of water. Push, and the far end of the comma shifts too. That
is the thing about a puddle: you cannot move part of it. It is one thing.

Eight minutes and it is gone down the drain.

Then he walks over to the long one by the parapet and starts again, and nothing he did to the first one had
any effect on this one at all. They are three feet apart with a dry ridge between them, and they might as
well be on different buildings.

By the time he has done all five he has been up there for half an hour, and the count is the count: five
separate puddles, five separate jobs, and the size of the job for each one was however far the water spread
before it stopped.

The one thing he does that his son does not, when his son is sent up instead, is that Ramesh works the terrace
in strips. Left to right, top to bottom, and when he reaches water he clears it completely before he moves on.
His son wanders about and pushes bits of different puddles and then cannot remember which ones he has done,
and comes down after forty minutes having cleared perhaps three of them and made a mess of the fourth.

---

## 3. The idea in plain English

Ramesh's terrace is a grid, and his method is the algorithm.

**Each tile is a vertex.** A grid of `r` rows and `c` columns has `r × c` vertices, and each one is identified
by a pair of numbers — its row and its column. Not a name, not an integer index. `(3, 7)` is the vertex.

**Two tiles that touch are joined by an edge.** Usually that means the four tiles directly above, below, left
and right — **four-way adjacency**. Sometimes the problem also counts the four diagonals, giving
**eight-way adjacency**. Read the statement and decide which, because the answer changes: a diagonal
connection joins two islands that four-way adjacency keeps separate.

**Nothing is stored.** This is the part to hold on to. There is no adjacency list. The neighbours of `(3, 7)`
are `(2, 7)`, `(4, 7)`, `(3, 6)` and `(3, 8)`, and you *compute* them by adding and subtracting one. This is
an **implicit graph** — the edges exist by rule rather than by record — and you met the idea on
[day 125](../day-125-what-a-graph-is/README.md).

**The water is a connected component.** All the tiles a puddle covers are reachable from each other by
touching, and none of them touches the next puddle. So counting puddles is counting connected components —
[day 129](../day-129-connected-components/README.md) — and clearing one puddle is a single traversal.

**Pushing the squeegee is a flood fill.** A **flood fill** starts at one cell and spreads to every connected
cell that satisfies some condition — same colour, also land, also water. It is exactly BFS or DFS, and the
name is worth knowing because problems use it: "flood fill" and "paint bucket" mean this.

**Working in strips is the outer loop.** Ramesh scans the terrace left to right, top to bottom, and every time
he meets water he has not cleared, that is a new puddle. In code that is the double `for` loop over every row
and column, with a check for "have I already dealt with this cell". **His son's wandering is what happens
without a `seen` record.**

**Marking is usually done in the grid itself.** When Ramesh clears a puddle it is gone, so he will not clear it
twice. In code you can overwrite a visited land cell with water, which costs no extra memory and destroys the
caller's input. The alternative is a separate `visited` grid of booleans, which costs `r × c` and leaves the
input alone. **Say which you are doing before you write it** — an interviewer may care.

**Now the detail that decides whether your code works: the bounds check.** Before you touch `grid[nr][nc]` you
must confirm that `0 <= nr < rows` and `0 <= nc < cols`. Miss it and Python does something worse than
crashing: `grid[-1]` is the *last* row, so falling off the top of the grid silently wraps to the bottom, and
your islands connect across the edge of the world. **The check has four comparisons and all four are
necessary.**

**BFS or DFS?** Both work and both are `O(rows × cols)`. The deciding argument is not elegance, it is depth: a
1,000 × 1,000 grid of all one colour is a single component whose depth-first path is a million cells long, and
recursion dies at about a thousand. **On a grid, write it iteratively** — either BFS with a queue or DFS with
an explicit stack — and use BFS specifically when the question asks for *distance*, because only BFS gives
you shortest paths.

**And the variant worth recognising immediately: many starting points.** "How long until every orange rots",
"how far is each cell from the nearest gate", "how far is each land cell from water" — these start from
*every* source at once. You push all the sources into the queue before the loop begins, and the BFS spreads
from all of them simultaneously. That is **multi-source BFS**, it is a one-line change, and it turns a family
of problems that look hard into problems that are not. It is
[day 141](../day-141-multi-source-bfs/README.md), and today you should be able to spot it.

---

## 4. The picture

Ramesh's terrace, as a grid:

```
        0   1   2   3   4   5   6
      +---+---+---+---+---+---+---+
  0   | W | W | . | . | . | W | . |     W = water
      +---+---+---+---+---+---+---+     . = dry
  1   | W | W | . | . | . | . | . |
      +---+---+---+---+---+---+---+
  2   | . | . | . | W | W | W | . |
      +---+---+---+---+---+---+---+
  3   | . | . | . | . | W | . | . |
      +---+---+---+---+---+---+---+
  4   | W | . | . | . | . | . | W |
      +---+---+---+---+---+---+---+

  four-way adjacency  ->  5 puddles:
     A: (0,0)(0,1)(1,0)(1,1)          size 4
     B: (0,5)                          size 1
     C: (2,3)(2,4)(2,5)(3,4)           size 4
     D: (4,0)                          size 1
     E: (4,6)                          size 1
```

**What to notice.** `(0,5)` and `(1,5)`... look again: `(1,5)` is dry, so `(0,5)` is alone. And `(2,5)` is
water but does not touch `(0,5)` — they are two rows apart. Being close on the page is not being adjacent; only
sharing an edge counts.

Now the same grid with eight-way adjacency:

```
  four-way: 5 puddles          eight-way: 4 puddles

  (0,5) and (2,5)?  not adjacent either way — two rows apart.
  But (1,4)? dry.   (2,3) touches (1,2)? dry.
  
  The change: (0,5) is diagonal to (1,4) and (1,6), both dry — still alone.
  (4,0) is diagonal to (3,1), dry — still alone.
  
  ... on THIS grid four-way and eight-way agree except where a
  diagonal bridge exists. Change (1,4) to water and:

  four-way:  (1,4) joins nothing new — (0,4) dry, (2,4) water -> joins C
  eight-way: (1,4) also touches (0,5) diagonally -> B and C MERGE
```

**What to notice.** One cell changing from dry to water merges two components under eight-way adjacency and not
under four-way. The problem statement decides this and you must read it. "Connected horizontally or
vertically" means four. "Connected in any of the eight directions" means eight.

The neighbour offsets, which you should be able to type without thinking:

```
FOUR-WAY                          EIGHT-WAY

      (-1, 0)                     (-1,-1) (-1, 0) (-1,+1)
         |                             \     |     /
(0,-1) --+-- (0,+1)               (0,-1) -- CELL -- (0,+1)
         |                             /     |     \
      (+1, 0)                     (+1,-1) (+1, 0) (+1,+1)

((-1,0), (1,0), (0,-1), (0,1))    all 9 offsets except (0,0)
```

And the bounds trap, drawn:

```
  cell (0, 3), moving up:  nr = -1

  WITHOUT the check:
      grid[-1][3]  ->  Python reads the LAST row
      ->  the top of the grid is connected to the bottom
      ->  no error, wrong answer

  WITH the check:
      0 <= -1  is False  ->  skipped
```

**What to notice.** There is no `IndexError` here. Negative indices are legal Python and mean "from the end",
so the failure is silent and produces a grid that wraps like the surface of a doughnut. Falling off the
*right* edge does raise `IndexError`, so half your bugs crash and half do not.

---

## 5. The code, built step by step

Start with the neighbour function, because it is the only genuinely new thing.

```python
FOUR = ((-1, 0), (1, 0), (0, -1), (0, 1))

def neighbours(row: int, col: int, rows: int, cols: int):
    """Yield the in-bounds cells adjacent to (row, col)."""
    for delta_row, delta_col in FOUR:
        r, c = row + delta_row, col + delta_col
        if 0 <= r < rows and 0 <= c < cols:
            yield r, c
```

Four comparisons, and all four are necessary. Writing this as a generator means every algorithm below reads
the same regardless of four-way or eight-way, and swapping `FOUR` for the eight-offset tuple changes the
adjacency everywhere at once.

Now the flood fill, iteratively, because a grid can be deep.

```python
def flood(grid: list[list[str]], row: int, col: int, target: str) -> int:
    """Clear the whole connected region of `target` starting here. Returns its size."""
    rows, cols = len(grid), len(grid[0])
    stack = [(row, col)]
    grid[row][col] = "0"                       # mark on PUSH
    size = 0
    while stack:
        r, c = stack.pop()
        size += 1
        for nr, nc in neighbours(r, c, rows, cols):
            if grid[nr][nc] == target:
                grid[nr][nc] = "0"             # mark on PUSH, not on pop
                stack.append((nr, nc))
    return size
```

`grid[nr][nc] = "0"` sits immediately before the append. On a grid this matters more than anywhere else,
because a cell has up to four neighbours that could each push it, so marking on pop lets the stack grow to
four times the number of cells.

Overwriting the grid is the `seen` set. No extra memory, and it destroys the input.

Then the outer loop, which is Ramesh working in strips:

```python
def count_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for row in range(rows):                    # every cell, in order
        for col in range(cols):
            if grid[row][col] == "1":
                count += 1
                flood(grid, row, col, "1")
    return count
```

Nine lines and the problem is solved. The double loop is the outer loop over all vertices from
[day 129](../day-129-connected-components/README.md); the `if` is the seen check; `flood` is the traversal.

If the input must survive, swap the marking for a separate grid:

```python
def count_islands_pure(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]     # NOT [[False]*cols]*rows
    count = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1" and not visited[row][col]:
                count += 1
                _flood_visited(grid, visited, row, col, rows, cols)
    return count
```

`[[False] * cols for _ in range(rows)]` and not `[[False] * cols] * rows`, for the aliasing reason from
[day 126](../day-126-graph-representation/README.md). On a grid problem that bug marks every row visited at
once and reports one island.

Now BFS, which you need whenever the question asks about distance:

```python
from collections import deque

def shortest_path(grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]) -> int:
    """Fewest steps from start to goal through cells equal to 0. -1 if unreachable."""
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] != 0:
        return -1
    distance = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return distance[(r, c)]
        for nr, nc in neighbours(r, c, rows, cols):
            if grid[nr][nc] == 0 and (nr, nc) not in distance:
                distance[(nr, nc)] = distance[(r, c)] + 1
                queue.append((nr, nc))
    return -1
```

Identical to [day 127](../day-127-graph-bfs/README.md)'s BFS with `neighbours` in place of `graph[vertex]`.
**That substitution is the whole of "grids are graphs"** — every algorithm from the rest of this phase works
on a grid by changing one line.

And multi-source, which is the variant worth recognising:

```python
def rot_time(grid: list[list[int]]) -> int:
    """Minutes until no fresh orange remains, or -1. 2 = rotten, 1 = fresh, 0 = empty."""
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))           # EVERY source goes in first
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):            # one whole level = one minute
            r, c = queue.popleft()
            for nr, nc in neighbours(r, c, rows, cols):
                if grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes
```

Two things are new. Every rotten orange goes into the queue *before* the loop starts, so the search spreads
from all of them at once — that is the one-line change that defines multi-source BFS. And
`for _ in range(len(queue))` processes exactly one ring per iteration, which is how you count minutes rather
than steps.

`return -1 if fresh else minutes` is the check people forget: a fresh orange walled off from every rotten one
never rots, and the problem wants `-1`, not the time the rest took.

### The complete solution

```python
"""Grids as graphs: flood fill, island counting, BFS distance, multi-source."""

from __future__ import annotations

from collections import deque

FOUR = ((-1, 0), (1, 0), (0, -1), (0, 1))
EIGHT = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def neighbours(row: int, col: int, rows: int, cols: int, offsets=FOUR):
    """In-bounds neighbours. All four comparisons matter: -1 is a legal index."""
    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            yield r, c


def island_sizes(grid: list[list[str]], offsets=FOUR) -> list[int]:
    """Sizes of every island. Does NOT modify the caller's grid."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]     # distinct rows
    sizes: list[int] = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "1" or visited[row][col]:
                continue
            size = 0
            stack = [(row, col)]
            visited[row][col] = True
            while stack:
                r, c = stack.pop()
                size += 1
                for nr, nc in neighbours(r, c, rows, cols, offsets):
                    if grid[nr][nc] == "1" and not visited[nr][nc]:
                        visited[nr][nc] = True          # mark on push
                        stack.append((nr, nc))
            sizes.append(size)
    return sizes


def nearest_distance(grid: list[list[int]], source: int, passable: int) -> list[list[int]]:
    """Multi-source BFS: distance from every cell to the nearest source. -1 if unreachable."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source:
                dist[r][c] = 0
                queue.append((r, c))                    # all sources, before the loop
    while queue:
        r, c = queue.popleft()
        for nr, nc in neighbours(r, c, rows, cols):
            if grid[nr][nc] == passable and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


if __name__ == "__main__":
    terrace = [
        list("1100010"),
        list("1100000"),
        list("0001110"),
        list("0000100"),
        list("1000001"),
    ]
    print("four-way sizes :", island_sizes(terrace))
    print("eight-way sizes:", island_sizes(terrace, EIGHT))
    print("grid intact    :", "".join(terrace[0]))

    maze = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    for row in nearest_distance(maze, source=1, passable=0):
        print("   ", row)
```

Running it:

```
four-way sizes : [4, 1, 4, 1, 1]
eight-way sizes: [4, 1, 4, 1, 1]
grid intact    : 1100010
    [1, 1, 0, 1]
    [0, 1, 0, 1]
    [1, 1, 1, 2]
    [1, 0, 0, 1]
```

Two things to look at. `grid intact` prints the original first row unchanged, because this version uses a
separate `visited` grid — the version that overwrites the input would print `0000000`.

And the distance grid answers "how far is each cell from the nearest `1`". The `1` cells themselves come out
as `0`, because they *are* sources and start at distance zero. Cell `(2,3)` is the only `2` on the board: it
is two steps from every source, and every other passable cell is directly beside one. **The important part is
that this is a single BFS**, and it would still be a single BFS with five hundred sources instead of five.

---

## 6. What it costs

**The two numbers.**

```
V = rows x cols                       every cell is a vertex
E <= 2 x rows x cols                  4 neighbours each, each edge shared by 2 cells
```

So `O(V + E)` collapses to something simple:

```
O(rows x cols + 2 x rows x cols) = O(rows x cols)
```

**Every grid traversal is linear in the number of cells.** Say it that way rather than `O(V + E)` — it is more
concrete and it is what the interviewer wants to hear.

Put numbers on it:

```
1,000 x 1,000 grid
cells                    1,000,000
neighbour checks         1,000,000 x 4 = 4,000,000
                         ------------------------
total                    ~5,000,000 operations   ->  about half a second in Python
```

**Space, and the choice you make.**

```
overwriting the grid       O(1) extra      destroys the input
separate visited grid      rows x cols     input preserved
  as a list of lists       1,000,000 x 8 bytes  = 8 MB
  as a bytearray           1,000,000 x 1 byte   = 1 MB
```

```
the stack or queue         O(rows x cols) worst case
```

**The worst case for the frontier is worth knowing precisely**, because it differs between the two traversals:

```
BFS on a 1,000 x 1,000 open grid
  the widest ring is the diagonal   ->  ~1,000 cells in the queue
  as (int, int) tuples              ->  1,000 x ~72 bytes = 72 KB

DFS on the same grid
  the deepest path snakes everywhere ->  up to 1,000,000 cells on the stack
                                     ->  72 MB
```

**On an open grid, BFS's frontier is tiny and DFS's is enormous.** That is a genuine reason to prefer BFS on
grids, and it is the opposite of the general graph case where BFS's ring can be the expensive one. Say it if
asked which to use.

**And the recursion arithmetic that fails:**

```
recursive DFS on a 1,000 x 1,000 all-land grid
  depth needed              up to 1,000,000 frames
  Python's usable limit     ~960
                            -> RecursionError
```

**Multi-source costs the same as single-source**, which surprises people:

```
k sources, all pushed before the loop
each cell is still dequeued exactly once
                            -> O(rows x cols), independent of k
```

Running `k` separate BFS runs and taking the minimum would be `O(k × rows × cols)`. With 500 gates on a
million-cell grid that is 500 million steps against 1 million. **A five-hundred-fold difference from moving
one loop before another**, and it is the single best reason to recognise the multi-source shape.

**Eight-way costs the same order and 2× the constant:**

```
four-way    4 neighbour checks per cell
eight-way   8 neighbour checks per cell
            -> same O(rows x cols), twice the work
```

---

## 7. The traps

### The missing bounds check

The one that produces a wrong answer instead of a crash:

```python
for dr, dc in FOUR:
    if grid[r + dr][c + dc] == "1":      # no bounds check
        ...
```

From cell `(0, 3)`, going up gives `grid[-1][3]`, which Python cheerfully returns — the last row. So the top
edge of your grid is glued to the bottom edge:

```
grid = ["1001",
        "0000",
        "0000",
        "1001"]

correct answer (four-way): 4 islands
without the bounds check:  2 islands   <- the corners "connect" through the wrap
```

Going off the *right* edge does raise:

```
IndexError: list index out of range
```

So half the failures crash and half are silent, which is the worst possible combination. **All four
comparisons, every time.**

### Marking on pop

```python
while stack:
    r, c = stack.pop()
    if grid[r][c] == "0":
        continue
    grid[r][c] = "0"                     # marked on pop
    for nr, nc in neighbours(...):
        stack.append((nr, nc))           # pushed without checking
```

Correct answers. On a large grid:

```
1,000 x 1,000 all-land grid
mark on push:  stack peak ~2,000 entries
mark on pop:   stack peak ~4,000,000 entries    (each cell pushed by up to 4 neighbours)
```

```
MemoryError
```

### Recursion on a large grid

```python
def sink(grid, r, c):
    grid[r][c] = "0"
    for nr, nc in neighbours(r, c, rows, cols):
        if grid[nr][nc] == "1":
            sink(grid, nr, nc)
```

```
Traceback (most recent call last):
  File "islands.py", line 9, in sink
    sink(grid, nr, nc)
  [Previous line repeated 993 more times]
RecursionError: maximum recursion depth exceeded
```

And the "fix" that makes it worse:

```python
sys.setrecursionlimit(2_000_000)
```

```
Segmentation fault (core dumped)
```

No traceback, no message. **A grid problem with `m, n <= 300` is safe for recursion; anything above that is
not.** Read the constraints.

### `[[False] * cols] * rows`

```python
visited = [[False] * 3] * 3
visited[0][1] = True
print(visited)
```

```
[[False, True, False], [False, True, False], [False, True, False]]
```

One row, referenced three times. Marking one cell marks a whole column's worth across every row, and your
island count comes out as 1. The symptom looks like a traversal bug and the cause is one line of
initialisation. Always the comprehension.

### Running BFS once per source

```python
best = [[inf] * cols for _ in range(rows)]
for gate in gates:
    d = bfs_from(grid, gate)             # one full BFS per gate
    for r in range(rows):
        for c in range(cols):
            best[r][c] = min(best[r][c], d[r][c])
```

Correct, and:

```
500 gates on a 1,000 x 1,000 grid
500 x 1,000,000 = 500,000,000 cell visits
```

```
Time Limit Exceeded
```

Push every gate into the queue before the loop starts and it is 1,000,000 visits. **The tell is "nearest" or
"any of these sources" in the problem statement.**

### Forgetting what "unreachable" means

```python
return minutes                            # after the BFS finishes
```

On rotting oranges, a fresh orange in a sealed corner never rots, and the answer is `-1`, not the time the
reachable ones took. On walls-and-gates, a room no gate reaches keeps its initial value. **Every grid BFS needs
an explicit answer for the cells it never touched**, and it is almost always a counter checked after the loop.

---

## 8. In the interview

### How it gets asked

Grid problems are stated as stories, never as graphs:

- *"Count the number of islands."* — LeetCode 200, the most-asked graph question there is.
- *"Given a starting pixel and a new colour, fill the connected region."* — flood fill, LeetCode 733.
- *"How many minutes until every orange rots?"* — multi-source BFS, LeetCode 994.
- *"Fill each empty room with the distance to the nearest gate."* — multi-source again, LeetCode 286.
- *"Capture all regions surrounded by X."* — the inverted version: flood from the *edges*.
- *"Shortest path through the maze."* — BFS, and only BFS.
- *"What is the largest island you can make by flipping one water cell?"* — components plus labelling.

### The first ninety seconds

> "This is a graph problem and the graph is the grid. A vertex is a cell, identified by its row and column, and
> an edge joins two cells that touch — I would confirm whether that means four directions or eight, because
> diagonals merge islands that four-way adjacency keeps separate.
>
> Nothing is built. The graph is implicit: the neighbours of a cell are the four coordinate offsets, computed
> rather than stored. So I write a neighbour function with the bounds check in it and then every algorithm from
> the graph phase works unchanged — I substitute `neighbours(r, c)` for `graph[vertex]` and that is the whole
> translation.
>
> Counting islands is counting connected components, so it is the double loop over every cell, and whenever I
> find land I have not visited, that is one more island and I flood from it.
>
> Three things I would be deliberate about.
>
> **The bounds check is four comparisons and all four matter.** In Python a negative index is legal and means
> from the end, so falling off the top of the grid silently connects it to the bottom. That is a wrong answer
> rather than an error, which is worse.
>
> **I would write it iteratively, not recursively.** A thousand-by-thousand grid of all land is one island a
> million cells deep and recursion dies at about a thousand frames. Raising the limit turns that into a
> segmentation fault.
>
> **I mark cells when I push them, not when I pop them**, because on a grid each cell has up to four neighbours
> that could push it, so marking on pop lets the stack reach four times the number of cells.
>
> Cost is `O(rows × cols)` time — every cell visited once, four neighbour checks each. Space depends on whether
> I may modify the input: overwriting visited land with water is free, a separate visited grid is
> `rows × cols`. Which would you prefer?"

### The follow-ups

**"BFS or DFS for this?"**

> "Both are `O(rows × cols)` and both give the same components, so it comes down to two things.
>
> If the question asks about **distance** — fewest steps, minutes, nearest anything — it must be BFS, because
> only BFS gives shortest paths on an unweighted graph.
>
> If it is just connectivity, I would still lean BFS on a grid, and the reason is the frontier size. On an
> open thousand-by-thousand grid, BFS's queue holds one ring, which is roughly the diagonal — about a thousand
> cells, seventy kilobytes. DFS's stack holds the deepest path, which on an open grid can snake through every
> cell — a million entries, seventy megabytes. That is the opposite of the general graph case, where BFS's ring
> is the expensive one, and it is because grids have bounded degree and large diameter.
>
> DFS is two lines shorter and I would use it when the grid is small and the question is just 'how many'."

**"There are five hundred gates and you need each room's distance to the nearest one."**

> "Multi-source BFS, and the change from what I have written is one line: push **all** the gates into the
> queue before the loop starts, each at distance zero.
>
> The search then spreads outward from every gate simultaneously, and because BFS marks a cell the first time
> it reaches it, each cell gets the distance from whichever gate reached it first — which is the nearest one.
> No comparison, no minimum, it falls out of the order.
>
> The arithmetic is the argument. Running a separate BFS per gate and taking the minimum is 500 million cell
> visits on a million-cell grid. Multi-source is one million, because every cell is still dequeued exactly
> once. **The cost is independent of the number of sources**, which is the surprising part and the reason to
> recognise the shape.
>
> The tell in a problem statement is the word 'nearest', or 'any of these', or a start condition that is a set
> rather than a point. Rotting oranges, walls and gates, distance to the nearest zero, and 'how far is each
> land cell from water' are all this."

**"The grid is 10,000 by 10,000. Does anything change?"**

> "A hundred million cells, so the algorithm is fine — still linear, about half a billion operations, which is
> minutes in Python and seconds in a compiled language. What changes is memory.
>
> A separate visited grid as a list of lists is a hundred million Python objects and references — several
> gigabytes. So I would use a `bytearray` of a hundred million bytes, which is 100 MB, or overwrite the input
> if I am allowed. A single flat `bytearray` indexed as `r * cols + c` is also much better for cache locality
> than a list of lists.
>
> The frontier is fine either way with BFS — the ring is about ten thousand cells.
>
> If the grid were larger still, or sparse, I would stop materialising it: represent only the interesting cells
> in a set of coordinates and compute neighbours from that. A grid that is mostly empty does not need a
> hundred million entries.
>
> And I would ask whether the grid actually needs to be traversed in one piece. Many real grid problems —
> image segmentation, map tiles — partition naturally, and processing tiles independently with a merge step at
> the boundaries parallelises trivially."

**"Capture all regions surrounded by X. How is that different?"**

> "It is the inverted version and it is worth recognising because the direct approach is much harder.
>
> The direct approach is: for each region of `O`, check whether it touches the border, and if not, flip it.
> That works but requires flooding a region and *then* deciding, which means collecting the cells and going
> back over them.
>
> The move is to flip the question. A region survives exactly when it touches the border. So: flood from
> every `O` on the **border**, mark everything reachable as safe, and then in one final pass flip every `O`
> that was not marked. Two passes, no collecting, no second thoughts.
>
> That is a general trick for grid problems and I would name it as one: **when a condition is about reaching
> the edge, start from the edge.** Pacific-Atlantic water flow is the same idea run twice, once from each
> ocean's border, taking the intersection — and the naive version there, flooding from every cell to see where
> the water goes, is `rows × cols` traversals instead of two."

### The model answer

*"Given a grid where 1 is land and 0 is water, return the size of the largest island you could create by
changing exactly one water cell to land."*

> "Let me name the shape first: this is connected components plus labelling, and the labelling is what makes
> the efficient version possible.
>
> **The naive version is: for every water cell, flip it, count the island it now belongs to, flip it back.**
> That is one traversal per water cell — `rows × cols` traversals, each `O(rows × cols)`, so quadratic in the
> number of cells. On a 500 × 500 grid that is 62 billion operations. Correct and unusable, and I would say
> so rather than write it.
>
> **The fix is two passes.** First pass: label every island with an id and record each id's size — a
> dictionary from island id to cell count. That is one traversal over the whole grid, `O(rows × cols)`, using
> the component-labelling version rather than the counting version.
>
> Second pass: for every water cell, look at its four neighbours, collect the **distinct** island ids among
> them, and the candidate answer is one plus the sum of those islands' sizes. Take the maximum over all water
> cells. That is four lookups per cell, so also `O(rows × cols)`.
>
> **The word 'distinct' is the whole bug in this problem.** If two neighbours of a water cell belong to the
> same island — which happens constantly, for instance in a U shape — adding both sizes counts that island
> twice and the answer is too large. So the neighbours' ids go into a set before summing. I would write that
> as a set from the start and say why, because it is the thing the test cases are built to catch.
>
> **Two edge cases.** A grid that is entirely land: there is no water cell to flip, and the answer is
> `rows × cols`. A grid that is entirely water: the answer is 1, from flipping any single cell. Both fall out
> naturally if I initialise the best answer to the largest existing island and then let the second pass
> improve on it, rather than starting from zero.
>
> **Cost:** two linear passes, so `O(rows × cols)` time. Space is one integer label per cell — a flat array of
> `rows × cols` — plus the size dictionary, which has at most one entry per island. On a 500 × 500 grid that
> is 250,000 labels rather than 62 billion operations.
>
> **Implementation notes I would state while writing:** labels start at 2, so they never collide with 0 for
> water and 1 for unlabelled land; the flood is iterative with marking on push; and the neighbour function
> carries the bounds check so neither pass repeats it."

---

## 9. Recall card

**A grid is a graph: a cell is a vertex, touching cells are edges, and nothing is stored** — the neighbours are
computed from the coordinates. Substitute `neighbours(r, c)` for `graph[v]` and every graph algorithm works
unchanged.

**The bounds check is four comparisons and all four matter.** `grid[-1]` is the last row, so a missing check
wraps the grid instead of crashing — a wrong answer, not an error.

**Write it iteratively and mark on push.** A million-cell island is a million frames deep (`RecursionError`,
or a segfault if you raise the limit), and marking on pop lets the stack reach four times the cell count.

**Cost is `O(rows × cols)`.** On an open grid, BFS's queue holds one ring (~`rows` cells) and DFS's stack can
hold the whole snaking path — the opposite of the general graph case.

**Multi-source BFS is one line — push every source before the loop — and costs the same as one source.** The
tells are "nearest", "any of these", or "how long until everything". And when the condition is about reaching
the edge, **start from the edge.**
