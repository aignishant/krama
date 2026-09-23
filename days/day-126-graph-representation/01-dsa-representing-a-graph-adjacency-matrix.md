---
day: 126
track: dsa
title: "Representing a graph: adjacency matrix versus adjacency list"
phase: "Graphs"
status: written
---

# Representing a graph: adjacency matrix versus adjacency list

## 1. What this is, and why they ask it

There are two ways to store a graph, and the choice is not a matter of taste. One of them uses a thousand
times more memory than the other on a typical real graph, and the other one is a thousand times slower at
one specific question. You pick by counting edges.

An **adjacency matrix** is a `V × V` grid where the cell at row `i`, column `j` says whether there is an edge
from `i` to `j`. An **adjacency list** stores, for each vertex, only the neighbours it actually has. That is
the whole distinction, and everything else in this lesson follows from it.

They ask this because it is the fastest way to find out whether a candidate thinks about resources. "How will
you store this graph?" is a question with a right answer and a reason, and the reason involves arithmetic you
can do out loud. It also comes up implicitly in every graph problem you will ever be given: the input arrives
in one form, and the first thing you do is decide what to convert it into. Getting that wrong costs you a
`MemoryError` on the large test case, and it is the most common way a correct graph algorithm fails a judge.

By the end of this lesson you can build both from an edge list, state what each costs for each of the three
operations that matter, choose between them from the density in one sentence, and recognise the three cases
where the matrix is genuinely the better answer.

---

## 2. The story

The chess club meets on Sunday mornings in the back room of the community centre, and the board on the wall
is older than most of the members.

It is a big square thing, painted white, with twenty-four names running down the left side and the same
twenty-four names running across the top. Where any two rows and columns meet there is a small brass hook.
When two people play a game, Anand — who has run the club for nineteen years — hangs a red tag on the hook
where their names cross.

He is fond of it. When somebody comes up and says "have I played Sunil?", he looks at the square where their
two names meet, sees a tag or no tag, and answers. It takes him a second and a half. It does not matter
whether there are twenty tags on the board or two hundred.

What the board is not good at is the other question.

Last Sunday a boy asked him who Ravi had played, because he wanted to know if Ravi was any good. Anand ran
his finger along Ravi's row — all twenty-four squares, one at a time, most of them empty — and found three
tags. Sixteen seconds to find three names out of twenty-four squares.

And here is the thing that bothers him, now that he has noticed it. The board has five hundred and
seventy-six hooks. By March, at the end of a season, there are usually about ninety tags on it. The rest of
the board is empty. It has always been empty. He is looking after five hundred hooks that will never hold
anything.

Farid, who is nineteen and joined in October, does not use the board at all. He keeps it in his phone. Under
each person's name he has a short list of who they have played, and nothing else — no empty spaces, because
he never writes down a game that did not happen.

Ask Farid who Ravi has played and he reads out three names in about two seconds.

Ask Farid whether Ravi has played Sunil, and he has to open Ravi's list and read down it until he finds Sunil
or reaches the end. Usually quick, because the lists are short. But he is reading, and Anand is glancing.

They argue about it in a friendly way most weeks. Anand says the board tells you everything at a glance.
Farid says the board is mostly empty and always will be.

They are both right, and neither of them has said the sentence that settles it, which is that a season has
ninety games and the board has five hundred and seventy-six hooks.

---

## 3. The idea in plain English

Anand's board and Farid's phone are the two representations, and the sentence neither of them said is the
rule for choosing.

**The board is an adjacency matrix.** An **adjacency matrix** for a graph with `V` vertices is a `V × V`
grid. The cell at row `i`, column `j` holds `1` if there is an edge from `i` to `j` and `0` if there is not.
Every possible connection has a place, whether or not it exists.

**Farid's phone is an adjacency list.** An **adjacency list** stores, for each vertex, a list of exactly the
neighbours it has. Nothing is stored for a connection that does not exist. In Python this is a dictionary
from a vertex to a list, or a list of lists when vertices are numbered `0` to `V−1`.

**There is a third form you get handed but rarely keep: the edge list.** An **edge list** is just a list of
pairs — `[(0,1), (1,2), (0,3)]`. It is how graph problems almost always give you the input, and it is almost
never what you want to work with, because answering "who are the neighbours of vertex 3" means scanning every
edge. **Your first line of code in most graph problems is converting an edge list into an adjacency list.**

**Three operations decide everything.** Every difference between the two comes down to these:

1. **"Is there an edge from A to B?"** The matrix does this in one step — go to the cell, read it. The list
   has to scan A's neighbours, which costs the degree of A.
2. **"Give me all the neighbours of A."** The list does this in one step — hand back A's list, which is
   exactly as long as A has neighbours. The matrix has to scan A's entire row, all `V` cells, most of which
   are empty.
3. **"How much memory?"** The matrix always takes `V²` cells, whether the graph has a million edges or none.
   The list takes about `V + 2E` entries.

That is the whole comparison, and it is worth memorising as three lines rather than as prose.

**Now the sentence that settles it.** Almost every algorithm you will write — breadth-first search,
depth-first search, Dijkstra, topological sort — spends its whole life asking question 2. It walks to a
vertex and asks "what is next to you". It almost never asks question 1.

**So the adjacency list wins by default, and the interesting question is when it does not.**

**The deciding number is density.** With `V` vertices the most edges you can have is about `V²`. If `E` is
close to that, the graph is **dense**, the matrix's `V²` cells are mostly full, and it is not wasting
anything. If `E` is closer to `V`, the graph is **sparse**, and the matrix is a board with five hundred empty
hooks.

Real graphs are overwhelmingly sparse. A city's roads, a social network, a package dependency tree, a course
catalogue — in every one of them each vertex touches a handful of others, not all of them. **Assume sparse,
use a list, and justify the matrix when you choose it.**

**When the matrix is genuinely right**, and there are three cases worth knowing:

1. **The graph really is dense** — `E` close to `V²`, which usually means a "everything is related to
   everything, with weights" problem such as distances between all cities.
2. **`V` is small and fixed** — if `V ≤ 100`, `V²` is ten thousand cells, which is nothing, and the matrix is
   simpler to write and faster in practice because it is one contiguous block of memory.
3. **You need question 1 constantly** — some algorithms, notably Floyd-Warshall for all-pairs shortest paths,
   are *defined* on a matrix and ask "is there an edge from `i` to `j`" in their innermost loop.

**And weights change nothing structurally.** A weighted matrix stores the weight in the cell instead of `1`,
with some agreed value — usually infinity — meaning "no edge". A weighted list stores pairs: `graph[a]` is a
list of `(neighbour, weight)`. Everything above still applies.

---

## 4. The picture

Five vertices and five edges — Anand's board shrunk to something you can read.

```
edges: 0-1, 0-3, 1-2, 2-3, 3-4      (undirected)

ADJACENCY MATRIX                      ADJACENCY LIST

      0  1  2  3  4                   0 -> [1, 3]
    +---------------                  1 -> [0, 2]
  0 | 0  1  0  1  0                   2 -> [1, 3]
  1 | 1  0  1  0  0                   3 -> [0, 2, 4]
  2 | 0  1  0  1  0                   4 -> [3]
  3 | 1  0  1  0  1
  4 | 0  0  0  1  0                   10 entries total
                                      (each edge stored twice)
  25 cells, 10 of them 1
```

**What to notice.** Twenty-five cells to hold five edges. The matrix is symmetric across the diagonal —
`cell[0][1]` and `cell[1][0]` both say `1` — because the graph is undirected, and that symmetry is exactly the
duplicate storage the list also has. The diagonal is all zeros because there are no self-loops.

Now scale it, which is where the argument stops being about taste:

```
V = 1,000 vertices, E = 3,000 edges (a realistic sparse graph)

MATRIX                                 LIST
1,000 x 1,000 = 1,000,000 cells        1,000 lists + 6,000 entries
of which 6,000 are 1                   = 7,000 slots
                                       
0.6% full                              100% full
99.4% of the memory holds zeros        143x smaller
```

**What to notice.** The matrix is not slightly worse here. It is a hundred and forty times worse, and the
gap widens as `V` grows because the matrix grows with `V²` while the list grows with `E`.

Directed changes only the symmetry:

```
directed edges: 0->1, 1->2, 2->0

MATRIX                    LIST
      0  1  2             0 -> [1]
    +---------            1 -> [2]
  0 | 0  1  0             2 -> [0]
  1 | 0  0  1
  2 | 1  0  0             3 entries, not 6

  NOT symmetric.
  cell[0][1] = 1 but cell[1][0] = 0
```

**What to notice.** Each directed edge appears once, in both representations. The matrix's asymmetry *is* the
direction. If you build a directed graph and your matrix comes out symmetric, you have written the assignment
twice by accident, which is the mirror image of the bug from [day 125](../day-125-what-a-graph-is/README.md).

And the operation that decides it, drawn as the work each one does:

```
"who are the neighbours of vertex 3?"

MATRIX: scan the whole row
  row 3:  [ 1 ][ 0 ][ 1 ][ 0 ][ 1 ][ 0 ][ 0 ] ... 1,000 cells
            ^         ^         ^
          read all 1,000 to find 3 neighbours

LIST: hand back the list
  graph[3] = [0, 2, 4]
            3 entries, done
```

**What to notice.** A traversal asks this question once per vertex. Over a whole BFS the matrix does
`V × V = 1,000,000` cell reads and the list does `2E = 6,000` entry reads. That is the same 143× again, now
in time instead of memory.

---

## 5. The code, built step by step

Start with what you are given. Graph problems hand you an edge list and a vertex count.

```python
n = 5
edges = [(0, 1), (0, 3), (1, 2), (2, 3), (3, 4)]
```

Build the matrix first, and immediately meet the trap.

```python
def build_matrix(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """A V x V grid. matrix[a][b] == 1 means there is an edge a -> b."""
    matrix = [[0] * n for _ in range(n)]      # NOT [[0] * n] * n
    for a, b in edges:
        matrix[a][b] = 1
        matrix[b][a] = 1                      # drop this line for directed
    return matrix
```

The comment on line one is the most important line in this lesson. `[[0] * n] * n` creates **one** row and
then makes `n` references to that same row, so setting `matrix[0][1] = 1` sets it in every row at once.
Section 7 shows exactly what that looks like. The comprehension makes `n` distinct rows.

The adjacency list, which you already wrote yesterday:

```python
from collections import defaultdict

def build_list(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """One list per vertex, holding only the neighbours that exist."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)                    # drop for directed
    return graph
```

A list of lists rather than a dictionary because the vertices are numbered `0..n-1`. Use a `defaultdict` when
the vertices are strings or arbitrary labels. **Build from `range(n)`, not from the edges**, so that a vertex
appearing in no edge still exists — the bug from yesterday.

Now the three operations, side by side, which is the whole comparison in twelve lines.

```python
def has_edge_matrix(matrix: list[list[int]], a: int, b: int) -> bool:
    return matrix[a][b] == 1                                    # O(1)

def has_edge_list(graph: list[list[int]], a: int, b: int) -> bool:
    return b in graph[a]                                        # O(degree(a))
```

```python
def neighbours_matrix(matrix: list[list[int]], a: int) -> list[int]:
    return [b for b in range(len(matrix)) if matrix[a][b]]       # O(V)

def neighbours_list(graph: list[list[int]], a: int) -> list[int]:
    return graph[a]                                             # O(1), no copy
```

Read `neighbours_matrix` carefully: it loops over every vertex in the graph to find the few that are
neighbours. That loop is inside every traversal you will ever write, which is why the choice matters far more
than it looks.

Weighted versions, because most real graphs are:

```python
INF = float("inf")

def build_weighted_matrix(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
    """No edge is INF, not 0 — because 0 is a legitimate weight."""
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0                      # distance from a vertex to itself
    for a, b, weight in edges:
        matrix[a][b] = weight
        matrix[b][a] = weight
    return matrix
```

Using `0` to mean "no edge" is a real bug, not a stylistic point: an edge of weight zero is perfectly legal —
a free flight, a zero-cost transition — and it becomes invisible. `INF` is unambiguous, and it is also exactly
what shortest-path algorithms want to start from.

```python
def build_weighted_list(n: int, edges: list[tuple[int, int, int]]) -> list[list[tuple[int, int]]]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b, weight in edges:
        graph[a].append((b, weight))
        graph[b].append((a, weight))
    return graph
```

`(neighbour, weight)` pairs, and the order matters for a reason you will meet on
[day 136](../day-136-dijkstra/README.md): when these tuples go into a heap you usually want
`(weight, neighbour)` instead, so that the heap orders by weight. Store them the way you will use them.

And the memory measurement, which is the thing to actually run:

```python
import sys

def matrix_bytes(matrix: list[list[int]]) -> int:
    return sys.getsizeof(matrix) + sum(sys.getsizeof(row) for row in matrix)

def list_bytes(graph: list[list[int]]) -> int:
    return sys.getsizeof(graph) + sum(sys.getsizeof(row) for row in graph)
```

This does not count the integer objects themselves, which Python shares for small values, so it undercounts
both. It is still enough to show the shape of the difference, and running it is more convincing than reading
about it.

### The complete solution

```python
"""Both graph representations, the three operations, and the memory comparison."""

from __future__ import annotations

import random
import sys

INF = float("inf")


def build_matrix(n: int, edges: list[tuple[int, int]], directed: bool = False) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]          # n distinct rows
    for a, b in edges:
        matrix[a][b] = 1
        if not directed:
            matrix[b][a] = 1
    return matrix


def build_list(n: int, edges: list[tuple[int, int]], directed: bool = False) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        if not directed:
            graph[b].append(a)
    return graph


def has_edge_matrix(matrix: list[list[int]], a: int, b: int) -> bool:
    return matrix[a][b] == 1                       # O(1)


def has_edge_list(graph: list[list[int]], a: int, b: int) -> bool:
    return b in graph[a]                           # O(degree(a))


def neighbours_matrix(matrix: list[list[int]], a: int) -> list[int]:
    return [b for b in range(len(matrix)) if matrix[a][b]]      # O(V)


def neighbours_list(graph: list[list[int]], a: int) -> list[int]:
    return graph[a]                                # O(1)


def sizes(n: int, edges: list[tuple[int, int]]) -> None:
    matrix = build_matrix(n, edges)
    graph = build_list(n, edges)
    matrix_bytes = sys.getsizeof(matrix) + sum(sys.getsizeof(r) for r in matrix)
    list_bytes = sys.getsizeof(graph) + sum(sys.getsizeof(r) for r in graph)
    cells = n * n
    entries = sum(len(r) for r in graph)
    print(f"V = {n:>5}  E = {len(edges):>6}")
    print(f"  matrix: {cells:>10,} cells   {matrix_bytes:>10,} bytes")
    print(f"  list:   {entries:>10,} entries {list_bytes:>10,} bytes")
    print(f"  ratio:  {matrix_bytes / list_bytes:.1f}x")


if __name__ == "__main__":
    small_edges = [(0, 1), (0, 3), (1, 2), (2, 3), (3, 4)]
    m = build_matrix(5, small_edges)
    g = build_list(5, small_edges)

    for row in m:
        print(row)
    print(g)
    print("edge 0-3?", has_edge_matrix(m, 0, 3), has_edge_list(g, 0, 3))
    print("edge 0-2?", has_edge_matrix(m, 0, 2), has_edge_list(g, 0, 2))
    print("nbrs(3) :", neighbours_matrix(m, 3), neighbours_list(g, 3))

    print()
    random.seed(0)
    for n, e in ((100, 300), (1000, 3000), (1000, 400_000)):
        pairs = {(min(a, b), max(a, b))
                 for a, b in ((random.randrange(n), random.randrange(n)) for _ in range(e * 2))
                 if a != b}
        sizes(n, sorted(pairs)[:e])
```

Running it:

```
[0, 1, 0, 1, 0]
[1, 0, 1, 0, 0]
[0, 1, 0, 1, 0]
[1, 0, 1, 0, 1]
[0, 0, 0, 1, 0]
[[1, 3], [0, 2], [1, 3], [0, 2, 4], [3]]
edge 0-3? True True
edge 0-2? False False
nbrs(3) : [0, 2, 4] [0, 2, 4]

V =   100  E =    300
  matrix:     10,000 cells        9,656 bytes
  list:          600 entries      6,232 bytes
  ratio:  1.5x

V =  1000  E =   3000
  matrix:  1,000,000 cells      864,056 bytes
  list:        6,000 entries    64,264 bytes
  ratio:  13.4x

V =  1000  E = 400000
  matrix:  1,000,000 cells      864,056 bytes
  list:      800,000 entries  7,272,264 bytes
  ratio:  0.1x
```

Read those three blocks in order, because they are the entire lesson. At `V = 100` the matrix is barely
worse and is simpler to write. At `V = 1000` with a sparse graph it is thirteen times worse. And at
`V = 1000` with four hundred thousand edges — a dense graph — **the matrix is ten times better than the list**,
because Python's per-list and per-tuple overhead now dominates. The right answer flipped, and it flipped on
density.

---

## 6. What it costs

The table you should be able to write from memory:

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | `O(V²)` always | `O(V + E)` |
| Is there an edge A→B? | `O(1)` | `O(degree(A))` |
| All neighbours of A | `O(V)` | `O(degree(A))` |
| Add an edge | `O(1)` | `O(1)` |
| Remove an edge | `O(1)` | `O(degree(A))` |
| Add a vertex | `O(V²)` — rebuild | `O(1)` |
| Iterate every edge | `O(V²)` | `O(V + E)` |
| Whole BFS or DFS | `O(V²)` | `O(V + E)` |

**The bottom row is the one that decides it**, because a traversal is what you will actually run.

**Space, in bytes, worked out three ways.** Take `V = 10,000` vertices with `E = 50,000` edges — a
five-neighbour average, which is typical.

```
MATRIX, Python list of lists
  10,000 x 10,000 = 100,000,000 cells
  each cell a reference          8 bytes
                                 = 800 MB
```

```
MATRIX, one bit per cell (bytearray or an integer bitmask per row)
  100,000,000 bits / 8           = 12.5 MB
```

```
LIST, Python list of lists
  10,000 list objects            10,000 x 56    = 0.56 MB
  100,000 entries (2E)           100,000 x 8    = 0.8 MB
  plus list over-allocation      ~ 2x on entries
                                 ~ 2.2 MB
```

**Eight hundred megabytes against two.** That is not a tuning difference; it is the difference between
running and not running. And note the middle line: **bit-packing the matrix cuts it by 64×**, which is the
answer when someone insists on a matrix for a large sparse graph. `12.5 MB` is perfectly workable, and it is
worth knowing as the escape hatch.

**Time, counted from the loops.** A BFS over the whole graph:

```
LIST
  each vertex popped once                     V
  for each, iterate its own list              sum of degrees = 2E
                                              ---------------------
                                              V + 2E = O(V + E)
  V = 10,000, E = 50,000  ->  110,000 steps
```

```
MATRIX
  each vertex popped once                     V
  for each, scan the whole row                V
                                              ---------------------
                                              V x V = O(V^2)
  V = 10,000              ->  100,000,000 steps
```

**Nine hundred times more work** for the same traversal on the same graph. In Python, at roughly ten million
simple operations a second, that is 0.01 seconds against 10 seconds.

**The crossover.** The matrix stops being wasteful when `E` approaches `V²/2`:

```
V = 1,000
matrix cells                     1,000,000
list entries at E edges          2E
equal when 2E = 1,000,000        E = 500,000
maximum possible E               499,500
```

So for `V = 1,000` the list only loses when the graph is essentially complete. Accounting for Python's
per-object overhead — which the measured output above shows — the practical crossover is much earlier, around
`E ≈ V²/20`. **The rule to say out loud: use a list unless the graph is dense or `V` is under a few hundred.**

**One more cost nobody mentions.** `has_edge_list` is `O(degree)` because it scans. If your algorithm asks
that question a lot, store each vertex's neighbours as a **set** instead of a list:

```
list of neighbours    membership test O(degree),  iteration in insertion order
set  of neighbours    membership test O(1),       iteration in arbitrary order
                      ~4x the memory per entry
```

That gives you the matrix's `O(1)` edge test at the list's `O(V + E)` memory, and it is the correct answer
when somebody argues for a matrix purely on the edge-lookup point.

---

## 7. The traps

### `[[0] * n] * n`

The one that catches everybody, exactly once, and costs an hour when it does.

```python
matrix = [[0] * 3] * 3
matrix[0][1] = 1
print(matrix)
```

```
[[0, 1, 0], [0, 1, 0], [0, 1, 0]]
```

One assignment, three rows changed. `[row] * 3` does not copy the row — it makes three references to the same
list object. Setting a cell in "row 0" sets it in all of them, because there is only one row.

```
>>> matrix[0] is matrix[1]
True
```

The fix is a comprehension, which evaluates `[0] * n` afresh each time:

```python
matrix = [[0] * n for _ in range(n)]
```

```
>>> matrix[0] is matrix[1]
False
```

The reason this is so expensive is that the symptom looks like a graph bug. Your traversal visits vertices it
should not, and you spend the hour reading the traversal.

### The matrix that will not fit

```python
n = 100_000
matrix = [[0] * n for _ in range(n)]
```

```
Traceback (most recent call last):
  File "graph.py", line 3, in <module>
    matrix = [[0] * n for _ in range(n)]
MemoryError
```

Ten billion cells. Eighty gigabytes at eight bytes each. This is the failure mode on a judge's large test
case, and it arrives with no warning after your solution passed every small test. **Before writing a matrix,
compute `V²` in your head.** Ten thousand vertices is the point where you should stop.

### The zero that means two things

```python
matrix = [[0] * n for _ in range(n)]
matrix[a][b] = weight              # what if weight is 0?
```

An edge of weight zero is indistinguishable from no edge. Then:

```
>>> shortest_path(matrix, 0, 4)
inf                                # there is a path, it just costs nothing
```

Use `INF` for "no edge" in a weighted matrix, always, and set the diagonal to `0` deliberately.

### The neighbour scan hidden inside a loop

```python
for vertex in range(n):
    for neighbour in range(n):          # <- this is O(V), every time
        if matrix[vertex][neighbour]:
            ...
```

This looks like an adjacency scan and it is a full `V²` sweep. It is correct, and on a sparse graph it does a
thousand times more work than necessary. The tell is a nested `range(n)` in a function whose complexity you
claimed was `O(V + E)`. If you say `O(V + E)` in an interview and then write this, you will be asked about
it.

### Building the adjacency list from the edges only

```python
graph = defaultdict(list)
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)
for vertex in graph:                    # misses isolated vertices
    ...
```

The same trap as yesterday, and it is worth repeating because it survives into every problem in this phase.
A vertex in no edge never becomes a key. Build from `range(n)` whenever you are given `n`.

### The symmetric directed matrix

```python
for a, b in edges:
    matrix[a][b] = 1
    matrix[b][a] = 1        # left in by accident on a DIRECTED graph
```

No error. Your one-way streets are now two-way, your prerequisite graph has cycles it should not have, and
your topological sort reports that the courses cannot be ordered. **Check the symmetry deliberately**: for a
directed graph, assert that `matrix[a][b] != matrix[b][a]` for at least one pair in your sample.

---

## 8. In the interview

### How it gets asked

- *"How will you store this graph? Why not the other way?"* — the direct version, usually asked immediately
  after you say "I will build an adjacency list".
- *"You have a million users and their friendships. How much memory?"*
- *"Your solution passed the small cases and got a memory limit error. What happened?"*
- *"When would you use a matrix?"* — a real question with three real answers, and "never" is the wrong one.
- *"How would you make the edge lookup fast without a matrix?"* — the sets answer.

### The first ninety seconds

> "Adjacency list, and the reason is density. Let me put a number on it rather than assert it.
>
> A matrix is `V × V` cells regardless of how many edges exist. A list is `V` lists plus `2E` entries. So the
> comparison is `V²` against `V + 2E`, and for a typical graph — say a thousand vertices with three thousand
> edges — that is a million cells against about seven thousand slots. A hundred and forty times more memory to
> hold the same information, of which 99.4% is zeros.
>
> And the time argument is the same argument. Every algorithm I am going to run here — BFS, DFS, topological
> sort, Dijkstra — spends its life asking one question: 'what are the neighbours of this vertex'. A list
> answers that in `O(degree)`; a matrix scans the whole row in `O(V)`. So a traversal is `O(V + E)` on a list
> and `O(V²)` on a matrix, which on those numbers is a hundred and ten thousand steps against a hundred
> million.
>
> The matrix is not always wrong, though, and I would name when I would use it. Three cases: the graph is
> genuinely dense, with `E` near `V²`; `V` is small and fixed, say under a couple of hundred, where `V²` is
> nothing and the matrix is simpler and has better memory locality; or the algorithm itself is defined on a
> matrix, like Floyd-Warshall, which asks 'is there an edge from i to j' in its innermost loop.
>
> The one thing the matrix genuinely has is the `O(1)` edge test. If I needed that and the graph were sparse,
> I would not switch to a matrix — I would store each vertex's neighbours as a set instead of a list. That is
> `O(1)` membership at `O(V + E)` memory, which is the best of both.
>
> Shall I write the build?"

### The follow-ups

**"A million users, two hundred friends each. Which one, and how much memory?"**

> "List, and it is not close. Let me do both.
>
> Matrix: a million by a million is `10¹²` cells. At one byte each that is a terabyte, and in Python where a
> cell is an eight-byte reference it is eight terabytes. It does not exist.
>
> Even bit-packed — one bit per cell — it is `10¹²` bits, which is 125 gigabytes. Still no.
>
> List: `E` is a million times two hundred over two, so a hundred million edges, stored twice, so two hundred
> million entries. At eight bytes that is 1.6 gigabytes for the edges, plus a million list objects at about
> 56 bytes, which is 56 megabytes. Call it two gigabytes, and it fits on one machine.
>
> The number worth noticing is that the edges are the memory and the vertices are a rounding error — 1.6 GB
> against 56 MB. So 'can I fit this graph' is always a question about `E`.
>
> If two gigabytes were too much, the next step is compressed sparse row: two flat arrays, one holding all
> neighbours concatenated and one holding the offset where each vertex's slice begins. That removes every
> per-list object and gets a hundred million edges into about 800 megabytes of contiguous integers, with much
> better cache behaviour. The cost is that it is static — you cannot add an edge without rebuilding."

**"When would you actually reach for a matrix?"**

> "Three situations, and I would recognise them rather than derive them each time.
>
> One, a genuinely dense graph. All-pairs distances between forty cities is a complete weighted graph: `E` is
> essentially `V²`, so the list has no advantage and the matrix is simpler and faster. In Python the crossover
> comes earlier than the theory says, because a list of lists of integers carries enormous per-object
> overhead — I measured a case at a thousand vertices and four hundred thousand edges where the matrix was
> ten times *smaller*.
>
> Two, small fixed `V`. Under about two hundred vertices, `V²` is forty thousand cells and none of this
> matters. I take the matrix because it is fewer lines and harder to get wrong.
>
> Three, the algorithm demands it. Floyd-Warshall is three nested loops over `V` reading `dist[i][k] +
> dist[k][j]`; it is a matrix algorithm and rewriting it for a list makes it worse. Same for anything that
> uses matrix multiplication to count paths.
>
> And the honest fourth case: when I am writing it on a whiteboard under time pressure and `V` is small,
> because a matrix is four lines and I will not make a mistake in it."

**"Your BFS is `O(V + E)`. Prove it, given your representation."**

> "Each vertex is pushed to the queue at most once, because I mark it seen when I push it — so at most `V`
> pushes and `V` pops. When I pop a vertex I iterate exactly its own adjacency list, which has `degree(v)`
> entries. Summed over all vertices, the degrees add up to `2E` in an undirected graph, because each edge
> contributes one entry at each of its two ends — or `E` in a directed one.
>
> So the total is `V + 2E` operations, which is `O(V + E)`. Note it is a sum, not a product: a million
> vertices and three million edges is seven million steps, not three trillion.
>
> If I had used a matrix, the second half changes: instead of iterating `degree(v)` entries I scan `V` cells,
> so the total becomes `V + V×V`, which is `O(V²)`. Same algorithm, same graph, different representation, and
> the complexity class changed. That is why the representation question comes before the algorithm question."

**"The input is an edge list. Do you always convert?"**

> "Almost always, and I would say why rather than doing it reflexively. An edge list answers 'iterate every
> edge' perfectly and answers 'who are the neighbours of vertex 7' terribly — it costs a full scan, `O(E)`, and
> a traversal asks that once per vertex, so a traversal on a raw edge list is `O(V × E)`.
>
> The exceptions are real, though. Kruskal's algorithm for minimum spanning trees sorts the edges and
> processes them in order; it never asks for neighbours, so an edge list is exactly right and converting would
> be wasted work. Bellman-Ford relaxes every edge `V` times, same story. So the rule is: convert when the
> algorithm walks the graph, keep the edge list when the algorithm processes edges as a collection.
>
> Conversion is one pass, `O(V + E)`, so when in doubt it is cheap enough to just do."

### The model answer

*"You are given the road network of a country — 200,000 junctions and 500,000 roads, each with a length. You
need to answer 'shortest route from A to B' many times a second. How do you store it?"*

> "Let me settle the representation first, then say what else the access pattern forces.
>
> **Adjacency list, weighted, and the arithmetic makes it obvious.** A matrix would be 200,000 × 200,000 =
> 4×10¹⁰ cells. At even one byte per cell that is 40 gigabytes, and I need weights, so it is realistically
> 160 gigabytes or more. It does not fit. The list is 200,000 vertices plus a million directed entries — each
> road stored at both ends — and each entry is a neighbour and a weight, so roughly 16 bytes: about 16
> megabytes for the edges plus the per-vertex overhead. Four orders of magnitude apart, and one of them
> exists.
>
> **The density confirms it.** `E/V` is 2.5 — each junction touches two or three roads, which is what road
> networks look like. That is about as sparse as a connected graph gets. A matrix would be 0.00125% full.
>
> **I would not use Python lists of tuples for this, though, and that is the second half of the answer.** For
> a static graph queried at high rate, compressed sparse row is the right layout: one flat array of a million
> neighbour indices, one flat array of a million weights, and one array of 200,001 offsets marking where each
> junction's slice begins. Total around 12 megabytes of contiguous integers, no per-object overhead, and the
> neighbours of a junction are adjacent in memory, so a traversal reads sequentially instead of chasing
> references. On a graph this size that is often a five-to-ten-times speed difference and it comes purely
> from layout.
>
> **The price of CSR is that it is immutable.** Adding a road means rebuilding both arrays. For a road network
> that is fine — roads change monthly, not per second — and I would rebuild offline and swap the new arrays
> in, the same pattern as the autocomplete rebuild on
> [day 122](../day-122-autocomplete/README.md). If roads changed constantly I would go back to lists of
> tuples and accept the overhead.
>
> **What I would keep an edge list for.** Nothing in the query path, but if I ever need to recompute a
> minimum spanning tree or run an offline analysis over all roads, the edge list is the better input and I
> would keep the original around rather than reconstruct it.
>
> **And one thing I would flag as out of scope but real.** At 200,000 junctions, plain Dijkstra per query is
> too slow for 'many times a second', and the fix is not the representation — it is precomputation:
> contraction hierarchies or a landmark-based heuristic. I mention it because I do not want to leave you
> thinking the storage choice alone makes this fast. The storage choice makes it *possible*; the
> precomputation makes it *fast*."

---

## 9. Recall card

**Matrix is `V × V` cells, always. List is `V + 2E` entries.** For `V = 1,000` and `E = 3,000` that is a
million against seven thousand — 140× — and the gap grows with `V`.

**Three operations decide it:** edge test is `O(1)` on a matrix and `O(degree)` on a list; neighbours are
`O(V)` on a matrix and `O(degree)` on a list; memory is `O(V²)` against `O(V + E)`. Traversals only ever ask
the second one, so **traversal is `O(V²)` on a matrix and `O(V + E)` on a list.**

**Use a list by default.** Use a matrix when the graph is genuinely dense, when `V` is under a couple of
hundred, or when the algorithm is defined on a matrix (Floyd-Warshall).

**Need `O(1)` edge tests on a sparse graph?** Store neighbours as sets, not a matrix. `O(1)` membership at
`O(V + E)` memory.

**The bug: `[[0] * n] * n` makes one row referenced `n` times.** One assignment changes every row, and the
symptom looks like a traversal bug. Always `[[0] * n for _ in range(n)]`.
