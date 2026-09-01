---
day: 141
track: dsa
title: "Multi-source BFS and 0-1 BFS"
phase: "Graphs"
status: written
---

# Multi-source BFS and 0-1 BFS

## 1. What this is, and why they ask it

Two small variations on breadth-first search, and each one collapses a whole family of problems that look hard
into problems that are not.

**Multi-source BFS** starts from many vertices at once instead of one. You push *all* the sources into the
queue before the loop begins, and the search spreads outward from every one of them simultaneously. Every
vertex ends up with its distance to the **nearest** source — with no comparison, no minimum, no repeated runs.

**0-1 BFS** handles the case where edges cost either 0 or 1. Plain BFS is wrong there and Dijkstra is more than
you need; the answer is a deque, pushing zero-cost neighbours to the **front** and one-cost neighbours to the
**back**. Still `O(V + E)`, still no heap.

They ask these because both are one-line changes to code you already have, and because both have a
recognisable tell in the problem statement. "How long until every orange rots", "distance from each cell to
the nearest gate", "the shortest path if you may break at most one wall" — those are three different-looking
problems and two small variations.

The multi-source one in particular is the difference between an `O(k × (V + E))` solution and an `O(V + E)`
one, where `k` is the number of sources. **With 500 sources on a million-cell grid that is five hundred
million steps against one million**, and candidates who do not see it write the slow version and cannot
explain why it times out.

By the end of this lesson you can spot both from the phrasing, write each from memory, say precisely why
multi-source costs the same as single-source, and explain why the deque keeps 0-1 BFS linear.

---

## 2. The story

The water in Sarita's part of the city comes for ninety minutes in the morning and it has never been enough,
so from March to June the society hires tankers.

Three of them, and where they park is Sarita's decision because she is the secretary and because the first
year nobody decided and it was a disaster.

There are about two hundred and ten flats spread over six buildings and a lane that goes round the back, and
everybody has to walk to a tanker with whatever they can carry. So the question is simple to say and was hard
the first time: given three tankers parked at three places, how far does each flat have to walk?

The way she did it in the first year was one tanker at a time. She walked the whole colony imagining the
tanker at the front gate and worked out how far every flat was from it. Then she did the whole colony again
for the second tanker. Then again for the third. Three complete rounds, and at the end she had three numbers
for every flat and had to take the smallest.

It took her most of a Sunday and she got two of the numbers wrong.

The second year she did something different and it took twenty minutes.

She did not think about the tankers separately at all. She stood the three of them in her head at their three
spots, and then asked: which flats are right next to *a* tanker — any of them? Those are at distance one. Then:
which flats are next to *those*? Those are at distance two, and it does not matter which tanker they trace back
to. Then the next ring, and the next.

**Each flat is claimed by whichever tanker's ring reaches it first**, and she never once compared three
numbers, because a flat that has already been claimed is not looked at again.

The whole colony was covered in five rings.

The other thing that year taught her was about the back lane. There is a gate between the second building and
the back lane, and it is usually open, so from the second building the back lane is essentially free — you walk
through. When it is padlocked you have to go all the way round the front, which is a proper walk.

So the distances are not really all the same. Most steps between two adjacent points cost something and a few
of them cost nothing at all, and if you work with the gate open you get quite a different set of numbers from
the ones you get with it shut.

---

## 3. The idea in plain English

Sarita's second year is multi-source BFS, and the gate is 0-1 BFS.

**Ordinary BFS starts from one vertex.** Push the start, then repeatedly pop and push unseen neighbours, and
every vertex ends up with its distance from that one start —
[day 127](../day-127-graph-bfs/README.md), unchanged.

**Multi-source BFS starts from all of them.** Push **every** source into the queue before the loop begins, each
at distance zero. Everything else is identical.

**And each vertex ends up with the distance to its nearest source, with no comparison anywhere.** That is the
part worth understanding rather than memorising. BFS marks a vertex the first time it reaches it, and the
first ring to reach a vertex is the one from whichever source is nearest. **The minimum falls out of the
order, exactly as Sarita's flats were claimed by whichever ring got there first.**

**It costs the same as one source.** Every vertex is still dequeued exactly once and every edge examined once,
so it is `O(V + E)` regardless of whether there is one source or five hundred. Running a separate BFS per
source and taking the minimum is `O(k × (V + E))`, and on a million-cell grid with 500 gates that is five
hundred million steps against one million.

**The tell in a problem statement is the word "nearest", or "any of these", or "how long until everything".**
Rotting oranges — every rotten orange is a source. Walls and gates — every gate is a source. Distance from
each cell to the nearest zero — every zero is a source. **They are all the same eight lines.**

**Counting rounds rather than steps** is the small extra move that these problems usually need. Process the
queue **one whole level at a time** — take its current length, pop exactly that many — and each pass is one
minute, one round, one step of the simulation.

**And "what never gets reached" needs an explicit answer.** A fresh orange walled off from every rotten one
never rots. The problem wants `-1`, not the time the reachable ones took, and the check is a counter examined
after the loop, not something inside it.

**Now the gate, which is the second idea.**

**BFS's guarantee depends on every edge costing the same** — that is why the rings are rings. The moment an
edge is free, a vertex two edges away can be closer than a vertex one edge away, and BFS's ordering is wrong.

**Dijkstra fixes it and is more machinery than the problem needs.** With only two distinct costs, a priority
queue is doing work that a much simpler structure can do.

**0-1 BFS uses a deque and one rule: a zero-cost edge pushes to the front, a one-cost edge pushes to the
back.**

Why that works is worth saying in one sentence: **the deque always holds at most two distinct distance values —
`d` and `d + 1` — with all the `d`s in front.** A zero-cost neighbour has the same distance as the vertex you
are standing on, so it belongs with the current group at the front. A one-cost neighbour belongs with the next
group at the back. **That is exactly the invariant a plain queue maintains for uniform weights**, and
maintaining it by hand is what removes the need for a heap.

**So it stays `O(V + E)` — no `log` factor.** Against Dijkstra's `O((V + E) log V)` that is a real saving, and
more importantly it is much less code.

**The tell for 0-1 BFS is a problem where a move is either free or costs one:** "minimum walls to break",
"minimum sign flips", "you may reverse at most some edges", "cells of two types". **The moment there are three
distinct costs the invariant breaks and it is Dijkstra.**

**One more thing about multi-source that is worth carrying: the sources do not have to be real vertices.** A
common trick is to add a **virtual source** connected to all the real sources with zero-cost edges, run
ordinary single-source BFS from it, and get the same answer. That is the same reframing as
[day 139](../day-139-minimum-spanning-trees/README.md)'s wells, and it is useful when a library or an existing
function only accepts one start.

---

## 4. The picture

Sarita's two approaches, on a small grid. `T` marks a tanker.

```
        col:   0    1    2    3    4
      row 0    T    .    .    .    T
      row 1    .    .    .    .    .
      row 2    .    .    T    .    .
      row 3    .    .    .    .    .


  ONE BFS PER TANKER, then take the minimum:

    from (0,0):        from (0,4):        from (2,2):
     0  1  2  3  4      4  3  2  1  0      4  3  2  3  4
     1  2  3  4  5      5  4  3  2  1      3  2  1  2  3
     2  3  4  5  6      6  5  4  3  2      2  1  0  1  2
     3  4  5  6  7      7  6  5  4  3      3  2  1  2  3

    then, cell by cell, min of the three:
     0  1  2  1  0
     1  2  1  2  1
     2  1  0  1  2
     3  2  1  2  3

    cost: 3 full traversals + 20 comparisons


  MULTI-SOURCE, all three pushed before the loop:

     0  1  2  1  0
     1  2  1  2  1
     2  1  0  1  2
     3  2  1  2  3

    cost: ONE traversal. No comparisons at all.
```

**What to notice.** The answers are identical, and the second version never computed the three separate
distances that the first version then had to compare. **The minimum was never taken; it fell out of the order
in which the rings arrived.**

The rings, drawn:

```
ring 0:  the three tankers themselves
ring 1:  everything adjacent to any tanker
ring 2:  everything adjacent to ring 1 and not already claimed
...

     0  1  2  1  0        <- 0s are sources, 1s are ring 1
     1  2  1  2  1
     2  1  0  1  2
     3  2  1  2  3        <- ring 3, the furthest anything is from water

  the largest number in the grid is how far the worst-off flat must walk.
  For "how long until everything is covered", that IS the answer.
```

And the gate, which is 0-1 BFS:

```
    A --0-- B --1-- D          A to D:  via B, cost 0 + 1 = 1
    |               |
    +------1--------+          A to D:  direct,   cost 1

    plain BFS sees TWO edges via B and ONE direct
      -> it reports the direct route as "closer"
      -> both cost 1 here, but change the direct edge to cost 1
         and the two-edge route to 0+0 and BFS is simply wrong


  THE DEQUE, traced on:  S --0-- A --1-- B,  S --1-- C

    deque         pop   relax                          deque after
    -----------   ---   ----------------------------   -----------------
    [S(0)]         S    A via 0-edge -> dist 0, FRONT   [A(0), C(1)]
                        C via 1-edge -> dist 1, BACK
    [A(0), C(1)]   A    B via 1-edge -> dist 1, BACK    [C(1), B(1)]
    [C(1), B(1)]   C    ...                             [B(1)]
    [B(1)]         B    ...                             []

  at every moment the deque holds only 0s then 1s, or only 1s then 2s.
  Two distinct values, in order. That is the whole invariant.
```

---

## 5. The code, built step by step

Multi-source first. Start from the ordinary version and change one thing.

```python
from collections import deque

def distance_to_nearest(graph: dict[int, list[int]], sources: list[int]) -> dict[int, int]:
    """Distance from every vertex to its nearest source. O(V + E), any number of sources."""
    distance = {s: 0 for s in sources}             # ALL sources, distance zero
    queue = deque(sources)                         # ALL sources, before the loop
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in distance:
                distance[neighbour] = distance[vertex] + 1
                queue.append(neighbour)
    return distance
```

**Two lines differ from single-source BFS**, and both are on the way in: the dictionary is seeded with every
source rather than one, and the queue starts holding all of them.

**Nothing inside the loop changed at all.** No minimum, no comparison, no tracking of which source a vertex
came from. The marking-on-first-arrival that BFS already does is what produces the nearest-source answer.

On a grid, which is where this appears most often:

```python
def nearest_on_grid(grid: list[list[int]], source_value: int, passable: int) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]      # -1 means unreachable
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source_value:
                dist[r][c] = 0
                queue.append((r, c))               # every source, before the loop
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == passable and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist
```

The double loop that finds the sources runs **before** the BFS loop, not inside it. That placement is the
entire algorithm.

Now the level-counting version, for "how many rounds":

```python
def rounds_until_done(grid: list[list[int]]) -> int:
    """2 = rotten, 1 = fresh, 0 = empty. Minutes until nothing fresh remains, or -1."""
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):                # exactly one whole level
            r, c = queue.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes
```

Three details carry it. **`for _ in range(len(queue))` freezes the level size** before the loop begins, so
newly pushed vertices are processed in the *next* round. **`while queue and fresh`** stops as soon as nothing
fresh remains, so the count is not inflated by a final empty round. And **`return -1 if fresh else minutes`**
is the unreachable check, after the loop.

Now 0-1 BFS.

```python
def zero_one_bfs(graph: dict[int, list[tuple[int, int]]], n: int, source: int) -> list[float]:
    """Shortest paths when every edge costs 0 or 1. O(V + E) — no heap."""
    INF = float("inf")
    distance = [INF] * n
    distance[source] = 0
    deq = deque([source])
    while deq:
        vertex = deq.popleft()
        for neighbour, weight in graph[vertex]:
            candidate = distance[vertex] + weight
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate
                if weight == 0:
                    deq.appendleft(neighbour)      # same distance: the FRONT
                else:
                    deq.append(neighbour)          # one more: the BACK
    return distance
```

**The `if weight == 0` is the whole algorithm.** A zero-cost neighbour has the same distance as the vertex you
are standing on, so it belongs at the front with the current group; a one-cost neighbour belongs at the back
with the next group.

**Note there is no `visited` set**, and that is deliberate. A vertex can be improved after it has been popped —
reached again by a cheaper route — so the guard is the relaxation `candidate < distance[neighbour]`, exactly as
in Dijkstra. A vertex can enter the deque more than once, and it is bounded because each entry requires a
strict improvement.

The grid version, which is how it usually appears:

```python
def min_walls_to_break(grid: list[list[int]]) -> int:
    """0 = open, 1 = wall. Fewest walls to break walking from the top-left to the bottom-right."""
    rows, cols = len(grid), len(grid[0])
    INF = float("inf")
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = grid[0][0]                        # breaking into the start cell, if it is a wall
    deq = deque([(0, 0)])
    while deq:
        r, c = deq.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            cost = grid[nr][nc]                    # 1 to enter a wall, 0 otherwise
            if dist[r][c] + cost < dist[nr][nc]:
                dist[nr][nc] = dist[r][c] + cost
                if cost == 0:
                    deq.appendleft((nr, nc))
                else:
                    deq.append((nr, nc))
    return dist[rows - 1][cols - 1]
```

### The complete solution

```python
"""Multi-source BFS and 0-1 BFS: two one-line variations on breadth-first search."""

from __future__ import annotations

from collections import deque

INF = float("inf")


def multi_source(graph: dict[int, list[int]], sources: list[int]) -> dict[int, int]:
    """Distance to the NEAREST source. Costs the same as one source: O(V + E)."""
    distance = {s: 0 for s in sources}
    queue = deque(sources)                          # every source, before the loop
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in distance:
                distance[neighbour] = distance[vertex] + 1
                queue.append(neighbour)
    return distance


def nearest_on_grid(grid: list[list[int]], source: int, passable: int) -> list[list[int]]:
    """Grid version. -1 for anything the sources cannot reach."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == passable and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


def rounds_until_done(grid: list[list[int]]) -> int:
    """Level-by-level multi-source: 2 rotten, 1 fresh, 0 empty. Minutes, or -1."""
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):                 # freeze the level size
            r, c = queue.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes


def zero_one_bfs(graph: dict[int, list[tuple[int, int]]], n: int, source: int) -> list[float]:
    """Weights of 0 or 1 only. Deque: 0-edges to the front, 1-edges to the back. O(V + E)."""
    distance = [INF] * n
    distance[source] = 0
    deq = deque([source])
    while deq:
        vertex = deq.popleft()
        for neighbour, weight in graph[vertex]:
            candidate = distance[vertex] + weight
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate
                (deq.appendleft if weight == 0 else deq.append)(neighbour)
    return distance


if __name__ == "__main__":
    # Sarita's colony: T = 2 (tanker), . = 0 (walkable)
    colony = [
        [2, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    for row in nearest_on_grid(colony, source=2, passable=0):
        print("   ", row)
    print("worst walk:", max(max(r) for r in nearest_on_grid(colony, 2, 0)))
    print()

    oranges = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    print("rot time  :", rounds_until_done([row[:] for row in oranges]))
    sealed = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    print("impossible:", rounds_until_done([row[:] for row in sealed]))
    print()

    # 0-1 BFS: S->A free, A->B costs 1, S->C costs 1, C->B free
    zero_one = {0: [(1, 0), (2, 1)], 1: [(3, 1)], 2: [(3, 0)], 3: []}
    print("0-1 dists :", zero_one_bfs(zero_one, 4, 0))
```

Running it:

```
    [0, 1, 2, 1, 0]
    [1, 2, 1, 2, 1]
    [2, 1, 0, 1, 2]
    [3, 2, 1, 2, 3]
worst walk: 3

rot time  : 4
impossible: -1

0-1 dists : [0, 0, 1, 1]
```

Three things to look at. The colony grid matches the hand-computed one in section 4 exactly, from **one**
traversal — and `worst walk: 3` is the number Sarita actually wanted, which is just the maximum of the grid.

`impossible` returns `-1`: there is a fresh orange the rot cannot reach, and the answer is not "the time the
reachable ones took".

And the 0-1 result: vertex 1 is at distance **0** because the edge to it is free, and vertex 3 is at distance
1 — reachable either as `0→1→3` (0 + 1) or `0→2→3` (1 + 0). Plain BFS would have called vertex 1 "one step
away" and got both of those wrong.

---

## 6. What it costs

**Multi-source BFS.**

```
every vertex is dequeued at most once            V
every edge is examined once from each end        2E
                                                 -----------------
                                                 O(V + E) time
distance map + queue                             O(V) space
```

**The number of sources does not appear.** That is the whole point, and it is worth stating explicitly rather
than letting it be inferred: `k` sources cost the same as one, because seeding the queue with `k` entries does
not change how many times each vertex is dequeued.

**Against the naive version:**

```
k separate BFS runs, then a minimum per vertex
                                                 O(k x (V + E) + k x V)
```

```
1,000 x 1,000 grid, 500 gates
  V = 1,000,000, E ~ 2,000,000

  multi-source     3,000,000 steps
  one per gate     500 x 3,000,000 = 1,500,000,000 steps
                                     -> 500x
```

**Five hundred times, from moving one loop before another.** On a judge that is `Time Limit Exceeded` against
a comfortable pass.

**The level-counting version costs the same** — freezing `len(queue)` and looping does not visit anything
twice:

```
sum over all levels of (level size) = V
                                      -> still O(V + E)
```

**0-1 BFS.**

```
each vertex can enter the deque more than once,
but only on a strict improvement, and distances only
ever decrease through at most 2 distinct values
                                                 O(V + E) time
distance array + deque                           O(V) space
```

**Against Dijkstra on the same graph:**

```
V = 100,000, E = 300,000
  0-1 BFS       400,000 steps
  Dijkstra      300,000 x 17 = 5,100,000 steps
                              -> ~13x more work, for the same answer
```

**And the reason the `log` disappears** is worth being able to say: Dijkstra's heap exists to find the smallest
tentative distance among many different values. With only two distinct values in flight, "smallest" is just
"whatever is at the front", and a deque maintains that in constant time.

**The whole family, side by side:**

```
BFS, one source                O(V + E)
BFS, k sources                 O(V + E)          -- k does not appear
k separate BFS runs            O(k x (V + E))    -- what not to write
0-1 BFS                        O(V + E)
Dijkstra                       O((V + E) log V)
```

**Space, on a large grid:**

```
1,000 x 1,000 grid
  distance as a list of lists of ints    ~8 MB
  queue at peak (one ring)               ~1,000-4,000 entries with many sources
```

**With many sources the first ring can be large** — 500 gates means 500 entries before a single pop — but it is
still bounded by `V`, and in practice a multi-source BFS has a *shallower* and *wider* frontier than a
single-source one, which is if anything better for memory locality.

**And the number that justifies the level-counting form:**

```
"how many minutes" from a distance grid = max(dist)
"how many minutes" from level counting  = the loop counter

both O(V + E); the level version avoids materialising the grid
when you only want the number
```

---

## 7. The traps

### Running one BFS per source

The correct-but-fatal version:

```python
best = [[INF] * cols for _ in range(rows)]
for gate in gates:
    d = bfs_from(grid, gate)
    for r in range(rows):
        for c in range(cols):
            best[r][c] = min(best[r][c], d[r][c])
```

```
500 gates on a 1,000 x 1,000 grid
500 x 1,000,000 = 500,000,000 cell visits
```

```
Time Limit Exceeded
```

**The fix is to move the source-collection loop above the BFS loop.** The tell in the statement is "nearest",
"any of these", or "until everything is".

### Pushing sources inside the loop

```python
queue = deque([sources[0]])
while queue:
    ...
    for s in sources:                    # pushing the rest as you go
        queue.append(s)
```

This does not produce nearest-source distances — later sources enter the queue behind vertices that are
already at distance 2 or 3, so their rings start at the wrong offset. **All sources must be at distance zero
before anything is popped.**

### Not freezing the level size

```python
while queue:
    for _ in range(len(queue)):          # correct
        ...
```

```python
while queue:
    while queue:                          # WRONG: consumes newly pushed vertices too
        ...
    minutes += 1
```

The inner `while` drains everything, including the vertices this round just pushed, so the whole search
finishes in one "minute". **`len(queue)` must be evaluated once, before the inner loop.**

### Counting an extra round

```python
while queue:                             # no `and fresh`
    for _ in range(len(queue)):
        ...
    minutes += 1
```

The last level pushes nothing, but the loop still runs once more for it and increments the counter:

```
>>> rounds_until_done_no_fresh_check([[2, 1]])
2                                        # the answer is 1
```

`while queue and fresh` stops as soon as there is nothing left to spread to.

### Forgetting what was never reached

```python
return minutes
```

A fresh orange sealed off from every rotten one never rots, and the answer must be `-1`. The counter examined
**after** the loop is the check, and it is the hidden test on every problem in this family.

### 0-1 BFS with a `visited` set

```python
if neighbour not in visited:
    visited.add(neighbour)
    ...
```

**Wrong.** In 0-1 BFS a vertex can be reached again by a strictly cheaper route after it has been popped —
that is the whole reason the distances are not uniform. The guard must be the relaxation
`candidate < distance[neighbour]`, exactly as in Dijkstra. Adding a `visited` set silently locks in the first
distance found and produces answers that are too large.

### 0-1 BFS with three distinct weights

```python
graph = {0: [(1, 0), (2, 1), (3, 2)]}    # weights 0, 1 and 2
```

The deque invariant is that at most two distinct distance values are ever in flight. With a weight of 2, a
neighbour belongs neither at the front nor at the back of the current group, the deque stops being sorted, and
the answers are wrong with no error.

**Two weights, and only 0 and 1.** Otherwise it is Dijkstra — or, if the weights are small integers `0..k`,
a **dial** of `k+1` buckets, which is the generalisation and is worth naming.

### The mutated grid

```python
rounds_until_done(grid)                  # overwrites 1s with 2s
rounds_until_done(grid)                  # second call sees an all-rotten grid
```

The rot version marks visited cells by changing them, which destroys the caller's input. Copy it, or use a
separate distance grid, and **say which you are doing** — it is the same trade as
[day 130](../day-130-grids-are-graphs/README.md)'s islands.

---

## 8. In the interview

### How it gets asked

- *"How long until every orange rots?"* — LeetCode 994, the canonical multi-source problem.
- *"Fill each empty room with the distance to the nearest gate."* — LeetCode 286.
- *"01 Matrix: distance from each cell to the nearest 0."* — LeetCode 542.
- *"What is the largest distance from any land cell to the nearest water?"* — LeetCode 1162, "As Far from Land
  as Possible".
- *"Minimum number of walls to break to cross the grid."* — 0-1 BFS.
- *"You may reverse at most some edges. Fewest reversals to reach the target?"* — 0-1 BFS on a directed graph.

### The first ninety seconds

> "This is a nearest-source question, so it is multi-source BFS, and the change from ordinary BFS is one line:
> **push every source into the queue before the loop starts**, each at distance zero.
>
> The reason that works — and it is worth being precise, because it looks like it should need a minimum
> somewhere — is that BFS marks a vertex the first time it reaches it, and the first ring to reach a vertex
> comes from whichever source is nearest. **The minimum falls out of the ordering. There is no comparison
> anywhere in the code.**
>
> **And it costs the same as a single source.** Every vertex is still dequeued exactly once and every edge
> examined once, so it is `O(V + E)` whether there is one source or five hundred. The alternative — a separate
> BFS per source, then a minimum per cell — is `O(k × (V + E))`, and with 500 gates on a million-cell grid
> that is five hundred million steps against three million. **That factor of `k` is the whole point of
> recognising the shape.**
>
> If the question is 'how many rounds' rather than 'what is each distance', I process one whole level at a
> time — freeze `len(queue)` before the inner loop, pop exactly that many — and each pass is one minute.
>
> **Two things I would state before coding.** The tell for this shape is 'nearest', or 'any of these', or 'until
> everything is'. And whatever is never reached needs an explicit answer — a fresh orange sealed off never
> rots, and the expected result is `-1`, not the time the reachable ones took. That is a counter checked after
> the loop, and it is the hidden test on every problem in this family.
>
> Are all the moves the same cost? Because if some are free and some are not, plain BFS is wrong and I would
> use a deque instead of a queue."

### The follow-ups

**"Why does multi-source not need a minimum?"**

> "Because BFS's ordering already computes it.
>
> The invariant is that BFS pops vertices in non-decreasing order of distance and marks each one the first time
> it is reached. With several sources all seeded at distance zero, ring one is 'everything adjacent to *any*
> source', ring two is 'everything adjacent to ring one and not already claimed', and so on. **A vertex is
> claimed by whichever ring reaches it first, and that ring came from the nearest source.**
>
> So the minimum is not computed, it is a consequence of the order. If I later reach the same vertex from a
> different source, that route is by definition no shorter — the ring structure guarantees it — and the
> already-marked check discards it.
>
> **The same argument tells me what it costs:** each vertex is dequeued once and each edge examined once, and
> seeding `k` entries instead of one does not change either count. So `k` never appears in the complexity.
>
> And if I need to know *which* source claimed each vertex — 'which tanker should this flat walk to' rather
> than 'how far' — that is one extra array carrying the source id along with the distance, and it is still one
> pass."

**"Why does plain BFS break when an edge is free, and why is Dijkstra overkill?"**

> "BFS's correctness rests on every edge costing the same — that is why the rings are rings, and why the first
> arrival is the cheapest. With a free edge, a vertex two edges away can be genuinely closer than a vertex one
> edge away, so 'fewest edges' and 'cheapest' stop being the same question, and BFS optimises the wrong one.
>
> **Dijkstra fixes it and pays for generality it does not need here.** Its heap exists to find the smallest
> tentative distance among many different values. With only two distinct edge costs, at any moment the frontier
> contains only two distinct distances — `d` and `d + 1`. So 'the smallest' is just 'whatever is at the front',
> if I keep the front sorted by hand.
>
> **That is the deque rule: a zero-cost edge pushes to the front, a one-cost edge pushes to the back.** A
> zero-cost neighbour has the same distance as where I am standing, so it joins the current group; a one-cost
> neighbour joins the next group. The invariant — all the `d`s in front, then the `d+1`s — is exactly what a
> plain queue maintains for uniform weights, maintained manually.
>
> `O(V + E)` with no log factor, against Dijkstra's `O((V + E) log V)` — about thirteen times less work on a
> hundred-thousand-vertex graph, and considerably less code.
>
> **The one thing I would flag: there is no `visited` set.** A vertex can be popped and then improved by a
> cheaper route, so the guard is the relaxation `new < distance[v]`, as in Dijkstra. A `visited` set locks in
> the first distance and gives answers that are too large, with no error."

**"The costs are 0, 1 and 2. Now what?"**

> "The deque invariant breaks, so 0-1 BFS is out — a weight-2 neighbour belongs neither at the front nor at the
> back of the current group, and the deque stops being sorted with no warning.
>
> Two answers depending on the range.
>
> **If the weights are small integers `0..k`, use a dial** — sometimes called dial's algorithm or a bucket
> queue. Keep `k+1` buckets indexed by `distance mod (k+1)`, process them in cyclic order, and each relaxation
> puts the neighbour in the bucket for its new distance. That is `O(V + E + k × V)` — still effectively linear
> for small `k`, and it is the natural generalisation of the deque, which is just the case `k = 1`.
>
> **If the weights are arbitrary, it is Dijkstra**, and I would not try to be clever.
>
> **And there is a third option worth knowing when there are exactly two costs but they are not 0 and 1** —
> say 3 and 7. Subtracting the smaller from every edge does not preserve shortest paths, because paths with
> different edge counts shift by different amounts. So that transformation is wrong, and it is a tempting
> mistake. It is Dijkstra, or a dial if the range is small."

**"Find the land cell furthest from any water."**

> "Multi-source BFS from all the water cells, and then the answer is the **maximum** of the resulting distance
> grid — which is one of the nicest examples of this shape, because the naive reading suggests something much
> harder.
>
> The naive version is: for each land cell, find its nearest water. That is one BFS per land cell — `O(V²)` —
> and on a hundred-by-hundred grid it is a hundred million cell visits.
>
> **Inverting it is the whole trick.** Instead of 'for each land cell, find the nearest water', do 'from all
> water at once, spread outward'. Every land cell gets its distance to the nearest water in one pass, and the
> answer is the largest of them. `O(V + E)`.
>
> **Two edge cases the problem is actually testing.** If there is no water at all, or no land at all, the
> answer is `-1` — nothing to spread from, or nothing to reach. And the grid may be entirely one or the other,
> so both checks are needed before the traversal.
>
> **The general pattern is worth naming**, because it recurs: **when a question is 'for every X, find the
> nearest Y', flip it and spread from all the Ys at once.** That turns `k` traversals into one, and it is the
> same move as flooding from the border on the surrounded-regions problem — start from the things you have
> few of."

### The model answer

*"A city grid where some cells are hospitals and some are blocked. For every residential cell, find the walking
distance to the nearest hospital. Then tell me where to put one more hospital to minimise the worst distance."*

> "Two parts, and the first is a straightforward multi-source BFS while the second is where the interesting
> reasoning is. Let me do them in order.
>
> **Part one.** Vertices are cells, edges are 'adjacent and both passable', and every hospital is a source.
> Push all of them into the queue at distance zero before the loop, then ordinary BFS. Every residential cell
> ends up with its distance to the nearest hospital, in one pass, `O(rows × cols)`.
>
> **I would say explicitly why there is no minimum in the code**, because it is the part that looks wrong: BFS
> claims each cell on first arrival, and the first ring to arrive comes from the nearest hospital. The
> alternative — one BFS per hospital and then a per-cell minimum — is `O(h × rows × cols)`, so with fifty
> hospitals on a thousand-by-thousand grid that is fifty billion cell visits against a million.
>
> **Blocked cells are simply not passable**, so they are never enqueued, and a residential cell that no
> hospital can reach keeps its `-1`. That case needs a decision from the product rather than from me — is an
> unreachable neighbourhood an error, or is it expected? — and I would ask rather than assume.
>
> **Part two is a different problem and I would say so.** 'Where to put one more to minimise the worst
> distance' is a minimax question, and the brute-force reading is: for every candidate cell, add a hospital
> there and recompute. That is `rows × cols` multi-source BFS runs — a million runs of a million cells on a
> thousand-by-thousand grid, which is `10¹²` and impossible.
>
> **So I would narrow the search before optimising the search.** Three observations, in order of how much they
> buy.
>
> First, **only the currently-worst cells matter.** Adding a hospital can only reduce the maximum if it helps
> the cells that are currently at the maximum. So compute the distance grid once, find the worst distance `D`
> and the set of cells achieving it, and only consider placements that improve at least one of those.
>
> Second, **binary search on the answer.** 'Can the worst distance be brought down to `d`?' is a much easier
> question than 'what is the best achievable?'. For a candidate `d`, every cell currently worse than `d` must
> be within `d` of the new hospital — so the new hospital must lie in the intersection of the `d`-radius
> neighbourhoods of all those cells. That intersection is computed with one more multi-source BFS, from the
> currently-too-far cells, and it is either empty or not. Binary searching `d` over `0..D` is `log D` such
> checks, so about ten or twelve passes rather than a million.
>
> Third, and I would offer this as the practical fallback: **if the grid is small, or if an approximate answer
> is acceptable, just try the top few hundred candidates** — cells near the centroid of the worst region — and
> take the best. That is a heuristic, it is honest about being one, and for a real city-planning tool it is
> probably what ships.
>
> **The thing I would not do is pretend part two is the same problem as part one.** Part one is a linear-time
> classic. Part two is an optimisation over placements, and recognising that the naive version is `10¹²` before
> writing it is most of the answer."

---

## 9. Recall card

**Multi-source BFS: push every source into the queue before the loop, each at distance zero.** One line, and
every vertex gets its distance to the **nearest** source — the minimum falls out of the ring order, so there is
no comparison anywhere.

**It costs `O(V + E)` regardless of the number of sources.** One BFS per source is `O(k × (V + E))` — 500 gates
on a million-cell grid is 500× more work. **The tell is "nearest", "any of these", or "until everything is".**

**For "how many rounds", freeze `len(queue)` and process one whole level per pass** — and use `while queue and
fresh`, or the last empty round inflates the count. **Whatever is never reached needs an explicit `-1`,
checked after the loop.**

**0-1 BFS: a deque, zero-cost edges to the front and one-cost edges to the back.** The frontier only ever holds
two distinct distances, which is what a plain queue gives you for uniform weights — so it stays `O(V + E)`,
about 13× cheaper than Dijkstra.

**No `visited` set in 0-1 BFS** — a vertex can be improved after being popped, so the guard is the relaxation.
And with three or more distinct weights the invariant breaks: use a bucket dial for small integers, Dijkstra
otherwise.
