---
day: 131
track: dsa
title: "Shortest path in an unweighted graph"
phase: "Graphs"
status: written
---

# Shortest path in an unweighted graph

## 1. What this is, and why they ask it

When every edge costs the same, breadth-first search finds the shortest path. Not usually — always, and by a
guarantee you can prove in three sentences.

You wrote BFS on [day 127](../day-127-graph-bfs/README.md) and used the property in passing. Today it is the
subject. There is a difference between *using* an algorithm and being able to say why it is correct, and this
is the one place in the graph phase where interviewers actually ask for the argument. "Find the shortest path
from A to B. Why does BFS work here?" is a real question with a real second half.

Today also covers what you do around the search rather than inside it: returning the path and not just its
length, handling several shortest paths, searching from both ends when the graph is large, and — most
importantly — recognising the exact moment the guarantee stops holding. **The instant edges have different
costs, BFS is confidently wrong**, and knowing where that line sits is worth more than the algorithm.

By the end of this lesson you can state and prove the guarantee, reconstruct any shortest path, count how many
there are, implement bidirectional search and say what it buys, and name the three variants that look
unweighted and are not.

---

## 2. The story

Ammu's father is under the scooter in the compound and he needs a twelve spanner, and the hardware shop shuts
at eight.

It is twenty to eight. She is fourteen and she has been sent out to find one.

The obvious thing, and what she does first, is go next door to the Josephs. Uncle Joseph looks in his box and
says no, only up to ten, but try the Nairs at the end because their son works on bikes.

Now, if she goes straight to the Nairs, she has done a sensible thing and possibly a slow one. The Nairs are
at the end of the lane. If they do not have it either they will send her somewhere else, and by then it will
be ten to eight and she will be three houses deep in a chain that started with a guess.

What she does instead — and she did not think about it, she just did it, because she wanted to be quick — is
finish the lane first.

She goes to the Josephs. Then the Pillais on the other side. Then the flat above the Josephs. Then the shop at
the corner that is not really a hardware shop but has a toolbox. Four places, all of them within thirty
seconds of her own gate, before she walks anywhere at all.

The corner shop does not have a twelve. But the man there says his brother-in-law two lanes over definitely
has a full set.

By then it is a quarter to eight and she has four suggestions, all of them one step away: the Nairs at the
end, the brother-in-law two lanes over, somebody's cousin, and a mechanic near the main road.

She does the near ones first again.

She finds it at the Nairs, at eight minutes to eight. Their son had the whole set in a cloth roll under his
bed, and it took her one step from Uncle Joseph's suggestion.

Walking back she works out that if she had followed the first suggestion straight through, she would have
gone to the Nairs anyway — so it would have been fine. But if the Josephs had said "try the mechanic near the
main road", she would have walked ten minutes each way to be told to try somebody else, and the spanner would
have been two doors down the whole time.

Doing the near ones first is not cleverness. It just means that when you find the thing, you know nothing
closer was missed.

---

## 3. The idea in plain English

Ammu's method is breadth-first search, and the last line of the story is the guarantee.

**Unweighted means every step costs the same.** An **unweighted graph** is one where an edge is just a
connection — no distance, no price, no time on it. Walking from one house to the next costs one step whether
the house is next door or at the end of the lane. That single assumption is what everything today rests on.

**The shortest path is the one with the fewest edges.** With every edge costing one, "shortest" means "fewest
steps", and that is a much easier question than "cheapest".

**BFS explores in rings.** All the houses one step from Ammu's gate, then all the houses one step from those,
and so on. You met this on [day 127](../day-127-graph-bfs/README.md), and the queue produces the rings by
itself.

**The guarantee, stated precisely: the first time BFS reaches a vertex, it has reached it by the fewest
possible edges.** Not "usually". Always, on an unweighted graph.

**And the proof, in three sentences.** BFS finishes every vertex at distance `k` before it looks at anything at
distance `k+1`. So when a vertex is first discovered, it is discovered from a vertex at some distance `d`, and
its own distance is `d+1`. If it could have been reached in fewer steps than that, it would have been
discovered while processing an earlier ring — which has already finished. **Therefore the first discovery is
the shortest.**

That is Ammu's last paragraph: because she does the near ones first, when she finds the spanner she knows
nothing closer was missed.

**The distance falls out of the search; the path takes one more field.** Store, for every vertex, which vertex
you reached it from — its **parent**. When you arrive at the goal, follow the parents back to the start and
reverse. Ammu can tell you the route she took because she remembers who sent her where.

**There can be several shortest paths, and BFS returns one of them.** If two neighbours of the goal are both
at distance 3, both give a path of length 4, and which one you get depends on the order the neighbours appear
in your adjacency list. **Say "a shortest path", not "the shortest path"** — and if a problem demands a
specific one, you need an explicit tie-break.

**Stopping early is legitimate.** Once you pop the goal from the queue, no later discovery can beat it, so you
can return immediately. On a large graph where the goal is close, that turns a full traversal into a small
one.

**Searching from both ends is the big optimisation.** If you know both the start and the goal, run two
searches — one forward from the start, one backward from the goal — one ring each, alternating, and stop when
they touch. Because the number of vertices in a ring grows with the branching factor, two half-depth searches
explore vastly fewer vertices than one full-depth search. This is **bidirectional BFS** and on a social graph
it is the difference between minutes and milliseconds.

**Now the boundary, and it is the important part of the lesson.** The guarantee needs *every edge to cost the
same*. Three situations look unweighted and are not:

- **Different edge costs.** A two-hop route that takes 10 minutes against a one-hop route that takes 90.
  BFS returns the one-hop route and is wrong. That is [day 136](../day-136-dijkstra/README.md), Dijkstra.
- **Costs of only 0 and 1.** A maze where moving is free and breaking a wall costs one. BFS is wrong and
  Dijkstra is overkill; the answer is **0-1 BFS** with a deque — push a zero-cost neighbour to the front and a
  one-cost neighbour to the back. Still `O(V + E)`, no heap.
- **A cost per vertex rather than per edge.** Waiting at a node, a toll for entering. Usually convertible by
  pushing the vertex cost onto its incoming edges, and worth spotting rather than fighting.

**The one-line test:** *does every move cost exactly the same?* Yes → BFS. No → something else, and say which.

---

## 4. The picture

Ammu's lane, with the rings marked:

```
              ring 0        ring 1                 ring 2

                        +-- Josephs -------------+-- Nairs (HAS IT)
                        |                        |
            Ammu -------+-- Pillais              |
                        |                        |
                        +-- upstairs flat        |
                        |                        |
                        +-- corner shop ---------+-- brother-in-law
                                                 |
                                                 +-- mechanic

  distance:   0             1                       2
```

**What to notice.** The Nairs are at distance 2, reached from the Josephs. The mechanic is also at distance 2.
Both were discovered in the same ring, and Ammu would have been equally happy with either — there are two
shortest paths of length 2 and no reason to prefer one.

The counter-example, which is what you must be able to draw:

```
  UNWEIGHTED — BFS is right           WEIGHTED — BFS is WRONG

     A ----- B ----- C                   A --1-- B --1-- C
     |               |                   |               |
     +-------------- +                   +------10-------+

   A to C: 1 step (direct)             A to C: BFS says 1 edge -> cost 10
           2 steps (via B)                     truth: 2 edges -> cost 2

   BFS returns the direct edge.        BFS returns the SAME path,
   Correct: 1 < 2.                     and it costs five times as much.
```

**What to notice.** The graph is identical. Only the numbers on the edges changed, and BFS's answer did not —
which is exactly the problem. It optimises the count of edges, and once edges are not interchangeable, the
count is the wrong thing to optimise.

And bidirectional search, which is the picture that explains the saving:

```
  branching factor b = 100, distance d = 6

  ONE-DIRECTIONAL
    ring 1: 100
    ring 2: 10,000
    ring 3: 1,000,000
    ring 4: 100,000,000
    ring 5: 10,000,000,000
    ring 6: 1,000,000,000,000        <- explores 10^12 vertices

  BIDIRECTIONAL — each side goes 3 deep, then they meet
    forward:  100 + 10,000 + 1,000,000  = ~1,010,100
    backward: same                       = ~1,010,100
                                          -------------
                                          ~2,000,000    <- 500,000x fewer
```

**What to notice.** The exponent halves. That is not a constant-factor improvement; it is the difference
between possible and impossible on a large sparse graph, and it costs about fifteen extra lines.

---

## 5. The code, built step by step

Start with the distance, which is BFS with one dictionary.

```python
from collections import deque

def shortest_distance(graph: dict[str, list[str]], start: str, goal: str) -> int:
    """Fewest edges from start to goal, or -1 if unreachable."""
    if start == goal:
        return 0
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour in distance:
                continue
            distance[neighbour] = distance[current] + 1
            if neighbour == goal:
                return distance[neighbour]       # stop the moment it is found
            queue.append(neighbour)
    return -1
```

The `start == goal` line first, because otherwise a start with no edges returns `-1` for a distance that is
obviously zero.

Returning as soon as the goal is *discovered* rather than when it is popped is a small extra saving and is
correct for the same reason: a vertex's distance is fixed the moment it is first reached.

Now the path itself, which needs one more field.

```python
def shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """One shortest path, or None. Ties broken by adjacency order."""
    if start == goal:
        return [start]
    parent: dict[str, str | None] = {start: None}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour in parent:
                continue
            parent[neighbour] = current
            if neighbour == goal:
                return _rebuild(parent, goal)
            queue.append(neighbour)
    return None
```

`parent` replaces `distance` and does three jobs: the seen set, the record of how each vertex was reached, and
the set of reachable vertices. The start's parent is `None`, which is what stops the rebuild.

```python
def _rebuild(parent: dict[str, str | None], goal: str) -> list[str]:
    path: list[str] = []
    node: str | None = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]                            # built backwards
```

Four lines. Everything else about paths is a variation on this.

**Counting all the shortest paths** is a different change, and the one people get wrong:

```python
def count_shortest_paths(graph: dict[str, list[str]], start: str, goal: str) -> int:
    distance = {start: 0}
    ways = {start: 1}                            # how many shortest paths reach it
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour not in distance:
                distance[neighbour] = distance[current] + 1
                ways[neighbour] = ways[current]
                queue.append(neighbour)
            elif distance[neighbour] == distance[current] + 1:
                ways[neighbour] += ways[current]   # ANOTHER equally short route
    return ways.get(goal, 0)
```

The `elif` is the whole thing. Seeing a vertex again is normally ignored; here, if the distance you would
assign *equals* the distance it already has, this is a second route of the same length and its count adds. If
the distance would be larger, it is a longer route and you ignore it as usual.

**All the shortest paths themselves** need a list of parents rather than one:

```python
from collections import defaultdict

def all_shortest_paths(graph, start, goal) -> list[list[str]]:
    distance = {start: 0}
    parents: dict[str, list[str]] = defaultdict(list)
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour not in distance:
                distance[neighbour] = distance[current] + 1
                parents[neighbour].append(current)
                queue.append(neighbour)
            elif distance[neighbour] == distance[current] + 1:
                parents[neighbour].append(current)
    ...
```

Then walk the parent structure backwards, branching at every vertex with more than one. **Flag the output size
before writing it:** the number of shortest paths can be exponential, so this is bounded by the output rather
than by the graph.

Now bidirectional search:

```python
def bidirectional(graph: dict[str, list[str]], start: str, goal: str) -> int:
    if start == goal:
        return 0
    front = {start: 0}
    back = {goal: 0}
    frontier_a, frontier_b = [start], [goal]
    while frontier_a and frontier_b:
        if len(frontier_a) > len(frontier_b):        # always expand the smaller side
            frontier_a, frontier_b = frontier_b, frontier_a
            front, back = back, front
        nxt = []
        for vertex in frontier_a:
            for neighbour in graph[vertex]:
                if neighbour in back:
                    return front[vertex] + 1 + back[neighbour]
                if neighbour not in front:
                    front[neighbour] = front[vertex] + 1
                    nxt.append(neighbour)
        frontier_a = nxt
    return -1
```

Two details carry the whole benefit. **Always expand the smaller frontier** — that is the swap at the top, and
without it a hub-heavy graph makes one side explode while the other sits still. And the meeting test is
`neighbour in back`, checked *before* adding to `front`, so you notice the moment the two searches touch.

This works on an undirected graph as written. On a directed graph the backward search must follow **reversed**
edges, which means either a reversed adjacency list or a graph structure that supports both directions — worth
saying out loud, because it is the thing that makes people's bidirectional implementations quietly wrong.

### The complete solution

```python
"""Shortest paths on an unweighted graph: distance, path, counting, bidirectional."""

from __future__ import annotations

from collections import defaultdict, deque


def build(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """One shortest path, or None. O(V + E)."""
    if start == goal:
        return [start]
    parent: dict[str, str | None] = {start: None}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour in parent:
                continue
            parent[neighbour] = current
            if neighbour == goal:
                path, node = [], neighbour
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return path[::-1]
            queue.append(neighbour)
    return None


def count_shortest_paths(graph: dict[str, list[str]], start: str, goal: str) -> int:
    """How many distinct shortest paths exist. The elif is the whole trick."""
    distance = {start: 0}
    ways = {start: 1}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph[current]:
            if neighbour not in distance:
                distance[neighbour] = distance[current] + 1
                ways[neighbour] = ways[current]
                queue.append(neighbour)
            elif distance[neighbour] == distance[current] + 1:
                ways[neighbour] += ways[current]
    return ways.get(goal, 0)


def bidirectional(graph: dict[str, list[str]], start: str, goal: str) -> int:
    """Search from both ends. Undirected only, as written. O(b^(d/2))."""
    if start == goal:
        return 0
    if start not in graph or goal not in graph:
        return -1
    front, back = {start: 0}, {goal: 0}
    frontier_a, frontier_b = [start], [goal]
    while frontier_a and frontier_b:
        if len(frontier_a) > len(frontier_b):
            frontier_a, frontier_b = frontier_b, frontier_a
            front, back = back, front
        nxt: list[str] = []
        for vertex in frontier_a:
            for neighbour in graph[vertex]:
                if neighbour in back:
                    return front[vertex] + 1 + back[neighbour]
                if neighbour not in front:
                    front[neighbour] = front[vertex] + 1
                    nxt.append(neighbour)
        frontier_a = nxt
    return -1


if __name__ == "__main__":
    lane = build([
        ("ammu", "josephs"), ("ammu", "pillais"),
        ("ammu", "upstairs"), ("ammu", "corner"),
        ("josephs", "nairs"), ("corner", "brother_in_law"),
        ("corner", "nairs"), ("corner", "mechanic"),
    ])
    print("path :", shortest_path(lane, "ammu", "nairs"))
    print("count:", count_shortest_paths(lane, "ammu", "nairs"))
    print("bidir:", bidirectional(lane, "ammu", "nairs"))
    print("gone :", shortest_path(lane, "ammu", "vasai"))

    # A diamond: four shortest paths of length 3 from s to t.
    diamond = build([
        ("s", "a"), ("s", "b"), ("a", "c"), ("a", "d"),
        ("b", "c"), ("b", "d"), ("c", "t"), ("d", "t"),
    ])
    print("diamond count:", count_shortest_paths(diamond, "s", "t"))
```

Running it:

```
path : ['ammu', 'josephs', 'nairs']
count: 2
bidir: 2
gone : None
diamond count: 4
```

Two things to look at. `count` is 2 — the Nairs are reachable in two steps via the Josephs *and* via the
corner shop, and `shortest_path` returned only one of them, chosen by adjacency order. And the diamond gives
4, because there are two ways into the middle layer and two ways out, and `2 × 2 = 4`. If your version
returns 2 there, the `elif` is missing.

---

## 6. What it costs

**Plain BFS.**

```
each vertex enters the queue once              V
each vertex's neighbours scanned once          2E undirected
                                               -------------
                                               O(V + E) time
distance / parent map                          O(V)
queue                                          O(widest level)
                                               -------------
                                               O(V) space
```

Early termination when the goal is found does not change the worst case — the goal might be the last vertex —
but in practice it is enormous:

```
social graph, V = 1,000,000, average degree 200
goal at distance 2
  vertices explored:  1 + 200 + 40,000 = ~40,000
  instead of                             1,000,000
                                         -> 25x less work
```

**Path reconstruction** adds nothing to the order:

```
parent map                O(V) space, already needed as the seen set
walking back              O(path length) <= O(V)
```

**Counting paths** is the same BFS with one extra dictionary, so still `O(V + E)`. **Enumerating all paths is
not**, and the difference is worth stating:

```
counting all shortest paths      O(V + E)              — a number
listing all shortest paths       O(paths x length)     — can be exponential
```

```
a chain of k diamonds:  2^k shortest paths
k = 30  ->  1,073,741,824 paths
```

**Bidirectional search** is where the interesting arithmetic is. With branching factor `b` and distance `d`:

```
one-directional     O(b^d)
bidirectional       O(2 x b^(d/2))
```

```
b = 200 (an average social degree), d = 6

one-directional     200^6 = 6.4 x 10^13     — the whole graph, many times over
bidirectional       2 x 200^3 = 16,000,000  — four million times fewer
```

In practice both are capped by `V`, so on a million-vertex graph the honest comparison is:

```
one-directional     up to 1,000,000 vertices explored
bidirectional       ~ 2 x sqrt-ish frontier, often tens of thousands
                    -> typically 10-100x on real graphs
```

**Bidirectional costs about fifteen extra lines and doubles the memory** — two distance maps instead of one —
and needs both endpoints, so it is useless for "distance from A to everything".

**Compared with the alternatives:**

```
BFS, unweighted              O(V + E)
0-1 BFS (deque)              O(V + E)
Dijkstra (binary heap)       O((V + E) log V)
Bellman-Ford                 O(V x E)
Floyd-Warshall (all pairs)   O(V^3)
```

```
V = 100,000, E = 500,000
BFS         600,000 steps
Dijkstra    600,000 x 17 = ~10,000,000 steps
```

**Dijkstra is roughly seventeen times more work here for an answer BFS already has.** That factor is the
reason to say "BFS, because the graph is unweighted" rather than reaching for the general tool.

---

## 7. The traps

### Using BFS on a weighted graph

The one that runs perfectly and returns the wrong answer:

```python
graph = {"A": ["B", "C"], "B": ["C"], "C": []}
costs = {("A", "B"): 1, ("B", "C"): 1, ("A", "C"): 10}
print(shortest_path(graph, "A", "C"))
```

```
['A', 'C']
```

One edge, and it costs 10. The two-edge route costs 2. **BFS minimises the number of edges, not the sum of the
weights**, and there is no warning of any kind. The tell in a problem statement is any number attached to a
connection: a distance, a price, a duration, a toll. If there is one, the answer is not plain BFS.

### Marking on pop

```python
while queue:
    current = queue.popleft()
    if current in seen:
        continue
    seen.add(current)
    for neighbour in graph[current]:
        queue.append(neighbour)          # no check before pushing
```

The answer stays correct. The queue fills with duplicates:

```
V = 5,000, E = 12,000,000
mark on push:  queue peak ~5,000
mark on pop:   queue peak ~12,000,000
```

```
MemoryError
```

And when it does not run out of memory, it is `Time Limit Exceeded` on a solution you are sure is `O(V + E)`.

### Computing the distance when you dequeue instead of when you discover

```python
while queue:
    current = queue.popleft()
    for neighbour in graph[current]:
        if neighbour not in seen:
            seen.add(neighbour)
            queue.append(neighbour)
    distance[current] = ...              # too late, and from what?
```

Distances belong on discovery — `distance[neighbour] = distance[current] + 1` at the moment you push. Trying
to compute them on the way out means you no longer know which vertex reached this one.

### Forgetting `start == goal`

```python
>>> shortest_distance(graph, "ammu", "ammu")
-1
```

The loop pops `ammu`, scans its neighbours, none of them is `ammu` because `ammu` is already in `distance`,
and the queue empties. The answer should obviously be 0. One line at the top, and it is the first thing a
hidden test checks.

### The `KeyError` on an isolated vertex

```python
for neighbour in graph[current]:
```

```
Traceback (most recent call last):
  File "sp.py", line 12, in shortest_path
    for neighbour in graph[current]:
KeyError: 'vasai'
```

A plain `dict` raises for a vertex that appears in no edge. A `defaultdict(list)` returns an empty list — but
silently creates the key, which then makes the graph grow as you traverse it. `graph.get(current, [])` is the
version that does neither.

### Bidirectional search on a directed graph

```python
bidirectional(directed_graph, "A", "Z")
```

The backward half follows forward edges, so it explores everything that `Z` points *to* rather than everything
that points *to* `Z`. No error, and the answer is wrong whenever the graph is not symmetric. **The backward
search needs a reversed adjacency list**, built once up front — one extra pass and `O(V + E)` extra memory.

### Assuming the returned path is canonical

```python
assert shortest_path(graph, "ammu", "nairs") == ["ammu", "corner", "nairs"]
```

It might be `["ammu", "josephs", "nairs"]`. Both are length 3, both are correct, and which one comes back
depends on the order neighbours were appended when the graph was built. **Tests should assert the length, or
assert membership in a set of valid answers** — never a specific path, unless the problem defines a tie-break
and you implemented it.

---

## 8. In the interview

### How it gets asked

- *"Find the shortest path from A to B. Why does BFS work here?"* — the direct version, and the second half is
  the actual question.
- *"What is the minimum number of moves to..."* — puzzles, knight moves, lock combinations.
- *"How many degrees of separation between these two people?"*
- *"Find the shortest transformation sequence between two words."*
- *"There are several shortest paths. Return all of them."* — or, better, "how many are there?"
- *"The graph has ten million vertices. Now what?"* — bidirectional.

### The first ninety seconds

> "Every edge costs the same here, so shortest means fewest edges, and that is breadth-first search.
>
> The guarantee I am relying on is that **the first time BFS reaches a vertex, it has reached it by the fewest
> possible edges** — and the reason is that BFS finishes every vertex at distance `k` before it looks at
> anything at distance `k+1`. So when a vertex is first discovered from something at distance `d`, its own
> distance is `d+1`; it cannot be less, because a shorter route would have been found in an earlier ring, and
> those rings are already finished.
>
> Implementation: a queue and a `parent` dictionary that doubles as the seen set. Mark a vertex when I push it,
> not when I pop it — otherwise a vertex with a hundred edges pointing at it gets queued a hundred times, and
> on a dense graph that is a memory-limit failure rather than a slow solution.
>
> For the path itself I walk the parents back from the goal and reverse. And I would say 'a shortest path'
> rather than 'the shortest path', because there can be several and which one I return depends on adjacency
> order — if you want a specific one I need a tie-break rule.
>
> `O(V + E)` time, `O(V)` space, and I would stop as soon as the goal is discovered rather than finishing the
> traversal.
>
> **The assumption I want to state before you ask** is that this only works because every edge costs one. If
> there were weights, a two-edge path could be cheaper than a one-edge path, the argument breaks at the first
> step, and BFS would return a confidently wrong answer with no warning. That would be Dijkstra — or, if the
> only weights were 0 and 1, a deque-based 0-1 BFS which is still linear."

### The follow-ups

**"Prove it."**

> "Induction on the ring number.
>
> Base case: the start is at distance 0 and is correct.
>
> Inductive step: suppose every vertex at true distance `k` has been assigned `k` and sits in the queue before
> anything at distance `k+1`. Now I pop a vertex `u` at distance `k` and look at an unvisited neighbour `v`. I
> assign `v` distance `k+1`. Is that right? It is at most `k+1`, because there is a path of that length through
> `u`. And it is at least `k+1`, because if `v` were reachable in `j ≤ k` steps it would have been discovered
> while I was processing ring `j−1`, which has already finished — and then it would not be unvisited now.
>
> So it is exactly `k+1`.
>
> The property the queue gives me is that all of ring `k` is popped before any of ring `k+1`, which follows
> from first-in-first-out: I only push ring `k+1` vertices while popping ring `k` vertices, so they all go
> behind the ring-`k` entries that are still waiting.
>
> The step that fails with weights is 'at least `k+1`'. With different edge costs, a path through more edges
> can be cheaper, so a vertex's cheapest route need not go through the ring that discovered it."

**"How many shortest paths are there?"**

> "One extra dictionary and one `elif`, and it stays `O(V + E)`.
>
> Alongside the distance I keep `ways[v]` — the number of shortest paths that reach `v`. The start has one. When
> I discover a new vertex from `u`, it inherits `ways[u]`. And when I encounter a vertex I have already seen,
> I normally skip it — but here I check whether `distance[v] == distance[u] + 1`. If it is, this is a *second
> route of the same length*, so `ways[v] += ways[u]`. If the distance would be larger, it is a longer route and
> I ignore it as usual.
>
> That `elif` is the whole algorithm and it is the part people miss, because every other BFS they have written
> ignores an already-seen vertex unconditionally.
>
> If they want the paths themselves rather than the count, I keep a *list* of parents instead of one, and walk
> it backwards branching at every fork. But I would flag that the number of shortest paths can be exponential
> — a chain of thirty diamonds has a billion of them — so listing them is bounded by the output, not by the
> graph, and I would ask whether the count is enough."

**"Ten million vertices and you need the distance between two specific people."**

> "Bidirectional BFS, and the exponent is the reason.
>
> A one-directional search explores roughly `b^d` vertices, where `b` is the branching factor and `d` the
> distance. On a social graph `b` is a couple of hundred and `d` is about six, so that is `200^6` — far more
> than the graph contains, meaning I explore essentially all of it.
>
> Searching from both ends, each side only goes half as deep, so it is `2 × b^(d/2)` — two times `200³`, about
> sixteen million rather than sixty-four trillion. The exponent halves, which is a completely different class
> of improvement from a constant factor.
>
> Two implementation details carry the benefit. **Always expand the smaller frontier**, alternating sides,
> because on a graph with hubs one side can explode while the other stays tiny. And check for the meeting
> point when I *generate* a neighbour, not when I dequeue it, so I stop the instant the two searches touch.
>
> Two caveats I would state. It needs both endpoints, so it is useless for 'distance from A to everyone'. And
> on a directed graph the backward search must follow **reversed** edges, which means building a reversed
> adjacency list up front — implementations that forget this are silently wrong on any asymmetric graph."

**"What if some moves cost more than others?"**

> "Then BFS is wrong and I would say so immediately rather than patch it.
>
> If the costs are arbitrary positive numbers, it is Dijkstra: a priority queue instead of a plain queue, so I
> always expand the cheapest known vertex rather than the nearest by edge count. `O((V + E) log V)`.
>
> If the only costs are 0 and 1 — which is common, things like 'moving is free, breaking a wall costs one' — I
> would use **0-1 BFS**: a deque, pushing zero-cost neighbours to the **front** and one-cost neighbours to the
> **back**. That keeps the deque holding at most two distinct distance values, which is exactly the invariant
> a plain queue gives for uniform weights, so it stays `O(V + E)` with no heap and no log factor.
>
> And if there were negative weights, neither works and it is Bellman-Ford at `O(V × E)`.
>
> The general point I would make is that the cheapest correct algorithm depends entirely on the weight
> structure, and 'is every edge the same cost' is the first question I ask about any shortest-path problem —
> before I ask anything about the size of the graph."

### The model answer

*"Two words of the same length, and a dictionary. Each step you may change one letter, and the result must be
in the dictionary. Find the length of the shortest transformation sequence."*

> "Shortest, with every step costing the same, so this is BFS. The interesting part is the modelling, and the
> naive model is the trap.
>
> **A vertex is a word. An edge joins two words that differ in exactly one letter.** Undirected, unweighted.
>
> **I would not build the graph.** With `n` words of length `L`, comparing every pair is `n²` comparisons at
> `L` each — ten thousand words is a hundred million comparisons before the search starts. The graph is
> implicit and I generate neighbours on demand.
>
> **Generating them: from a word of length `L`, produce the `L × 25` strings that differ in one position and
> keep those present in a set of the dictionary.** For five-letter words that is 125 candidate strings and 125
> set lookups per word — a constant, completely independent of dictionary size. So the whole search is
> `O(V × L × 25)` rather than `O(V² × L)`, which at ten thousand five-letter words is about 1.25 million
> operations against 500 million.
>
> **If `L` were large — say fifty — the direct generation gets expensive**, and the alternative is a wildcard
> bucket: index every word under patterns like `h*t`, `*ot`, `ho*`, so all words sharing a pattern are
> neighbours. That is `O(V × L)` to build and `O(L)` per lookup. The crossover is around `L = 25`, and I would
> mention it rather than pretend one model always wins.
>
> **Then it is plain BFS**: distance dictionary as the seen set, mark on push, `deque`, return the distance
> when the end word is discovered, 0 if the queue empties.
>
> **Two edge cases before I code.** The end word may not be in the dictionary at all, in which case the answer
> is 0 and I check that in one line rather than discovering it after a full traversal. And the start word is
> conventionally not required to be in the dictionary, which is worth confirming.
>
> **The optimisation I would offer next is bidirectional search**, and here it is a genuine win rather than a
> flourish: the branching factor for a common five-letter word is dozens, so meeting in the middle roughly
> square-roots the explored set. Two frontiers as sets, always expand the smaller one, stop when a generated
> word appears in the other side's map. About fifteen extra lines, and on the standard version of this problem
> it is the difference between passing comfortably and timing out.
>
> **Cost:** `O(V × L × 25)` time, `O(V × L)` space for the dictionary set and the frontiers. I would state `L`
> explicitly rather than hide it in a constant, because for this problem the word length is a real parameter
> and the interviewer is likely to change it."

---

## 9. Recall card

**Every edge costs the same → shortest means fewest edges → BFS**, and the first time BFS reaches a vertex is
by the fewest possible edges.

**The proof in one sentence:** ring `k` finishes before ring `k+1` begins, so a shorter route would already
have been found. That step is exactly what breaks when edges have different costs.

**Path:** keep a `parent` map — it is also the seen set — and walk it backwards from the goal, then reverse.
Say "**a** shortest path", because ties are resolved by adjacency order.

**Counting all shortest paths is one `elif`:** when an already-seen vertex has `distance == distance[current] +
1`, add the counts. Still `O(V + E)`; *listing* them can be exponential.

**Bidirectional halves the exponent** — `2 × b^(d/2)` instead of `b^d`, four million times fewer on `b=200,
d=6`. Always expand the smaller frontier, and on a directed graph the backward search needs **reversed**
edges.
