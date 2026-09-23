---
day: 139
track: dsa
title: "Minimum spanning trees: Kruskal and Prim"
phase: "Graphs"
status: written
---

# Minimum spanning trees: Kruskal and Prim

## 1. What this is, and why they ask it

A **spanning tree** connects every vertex of a graph using exactly `V − 1` edges and no cycles. A **minimum**
spanning tree is the cheapest one. The question it answers is: *connect all of these at the lowest total
cost.*

There are two algorithms and they are both greedy, which is unusual — most greedy algorithms are wrong, and
these two are provably right. **Kruskal's** sorts every edge and adds each one that does not create a cycle.
**Prim's** grows one connected blob outward, always adding the cheapest edge leaving it.

They ask this because it is one of the cleanest greedy proofs in the syllabus, because both algorithms are
short, and because the choice between them is a real decision driven by density. It is also where
[Union-Find](../day-138-union-find/README.md) earns its place — Kruskal's is essentially "sort the edges and
run Union-Find over them", and if you learned Union-Find yesterday you already have most of it.

The thing that separates candidates is the confusion that everybody has once: **a minimum spanning tree is not
a shortest-path tree.** The cheapest way to connect everything is not the same as the cheapest way to get from
A to everywhere, and being able to give a small graph where they differ is worth more than writing either
algorithm.

By the end of this lesson you can write both, state the cut property that makes them correct, choose between
them from the density, handle disconnected graphs, and say what changes when the graph is directed.

---

## 2. The story

Yusuf got the contract for the new colony in 2007, twenty-six houses on four lanes, and cable to every one of
them.

The cable came on drums and he paid for it by the metre, so the whole job was one question: what is the least
wire that reaches all twenty-six houses.

The signal comes in at the corner house on the main road. From there it can go to whichever house is nearest,
and from any house it has reached, it can go on to any other. What it cannot do — and this is the part his
assistant took a while to see — is form a loop. If the cable runs from house 4 to house 9 and also from house
9 back round to house 4, that second run is doing nothing at all. Every house it touches is already connected.
It is wire spent on nothing.

So: twenty-six houses, and twenty-five runs of cable. Never twenty-six.

He has done this two ways and he will tell you both.

The first way, which he did on that job, is to grow it. Start at the corner house. Look at every house not yet
connected and ask which one is nearest to anything already wired. Run cable to that one. Now there are two
connected houses; look again at everything unconnected and ask the same question. He worked outwards from the
corner and the wired part grew like a stain, and at every step he ran the shortest piece that reached
somebody new.

The second way he learned from a man in Bhiwandi and it feels wrong the first time. **You forget about
connectedness entirely and you sort every possible run of cable by length, shortest first.** Then you go down
the list. Nine metres between 12 and 13 — take it. Eleven metres between 4 and 5 — take it. Twelve metres
between 5 and 6 — take it. And every so often you come to a run and both of its houses are already joined up,
by some chain of other runs, and then you skip it, because it would be a loop.

What is strange about the second way is that for most of it you have several separate little islands of wired
houses and nothing joining them, and it looks like a mess. Then near the end the islands snap together and it
is finished. Same total length as the first method, every time. Yusuf measured it out both ways on two
different sites before he believed it.

He uses the growing method now because on a real site you want the wired part to be one piece as you go, so
you can test the signal. But the sorting method is faster to plan when he has all the distances in front of
him and the houses are spread out.

---

## 3. The idea in plain English

Yusuf's two methods are Prim's and Kruskal's, and his observation about loops is the whole constraint.

**A spanning tree connects every vertex with no cycles.** For `V` vertices that is exactly `V − 1` edges —
fewer leaves something disconnected, more creates a cycle. Twenty-six houses, twenty-five runs of cable.

**A minimum spanning tree is the one with the smallest total weight.** Not the shortest path to anywhere —
the cheapest total, for the whole structure.

**A cycle means wasted wire.** Every edge in a cycle can be removed without disconnecting anything, so a
minimum spanning tree never contains one. That is Yusuf's assistant's realisation, and it is why both
algorithms are fundamentally about avoiding cycles.

**Kruskal's is the sorting method.** Sort every edge by weight. Go down the list, and take each edge unless
its two endpoints are already connected. Stop when you have `V − 1` edges.

**"Already connected" is exactly `find(a) == find(b)`**, which is why this is Union-Find's home. Take the
edge → `union`. `union` returning `False` → skip it, it would make a cycle. **Kruskal's is about eight lines
once you have yesterday's structure.**

**And the strange part is that it does not stay connected while it runs.** For most of the process you have
several separate fragments — Yusuf's islands — which merge near the end. That is fine, and it is what makes it
work on a graph you have not thought about globally.

**Prim's is the growing method.** Start anywhere. Keep a set of vertices already in the tree. Repeatedly take
the cheapest edge that leads from the tree to a vertex **not** in it, and add that vertex. Stop when everything
is in.

**The tree is always one connected piece**, growing outward, which is Yusuf's stain. Finding "the cheapest edge
leaving the tree" efficiently means a **priority queue** — which makes Prim's structurally almost identical to
[Dijkstra's](../day-136-dijkstra/README.md).

**And that near-identity is the trap.** The two differ in **one line**:

```
Dijkstra:  key[v] = distance_from_source_to_u + weight(u, v)
Prim:      key[v] = weight(u, v)
```

**Dijkstra accumulates the path cost; Prim's only looks at the single edge.** That is the entire difference,
and it is why the answers differ.

**So a minimum spanning tree is not a shortest-path tree**, and it is worth being able to show that on three
vertices rather than asserting it. Section 4 does.

**Now why greedy is correct here, which is the actual interview content.** It rests on the **cut property**:

> Take any way of splitting the vertices into two groups. The cheapest edge crossing between the groups is in
> some minimum spanning tree.

The argument is short. Suppose the cheapest crossing edge `e` is not in the tree. The tree still connects the
two groups somehow, so it uses some other crossing edge `f`, which costs at least as much. Swap `f` for `e`:
the result is still a spanning tree — still connected, still `V − 1` edges — and its total is no larger. **So
a minimum spanning tree containing `e` exists.**

**Both algorithms are just repeated applications of this.** Prim's cut is "in the tree" against "not in the
tree", and it takes the cheapest crossing edge. Kruskal's cut is around whichever fragment the next edge would
join. **Say the cut property and the swap argument, and you have answered "why does greedy work here", which
is the question.**

**Ties are worth knowing about.** If all edge weights are distinct, the minimum spanning tree is **unique**.
With ties there may be several, all of the same total weight, and different algorithms — or the same algorithm
with a different sort order — will return different ones.

**And if the graph is not connected**, there is no spanning tree at all. Both algorithms then produce a
**minimum spanning forest** — one tree per component — and you detect it by counting: fewer than `V − 1` edges
taken means the graph was disconnected.

---

## 4. The picture

Yusuf's colony, cut down to six houses:

```
        A ----1---- B
        |  \        |
        4    3      2
        |      \    |
        C ----5---- D
        |           |
        6           7
        |           |
        E ----2---- F

edges sorted:  AB 1, BD 2, EF 2, AD 3, AC 4, CD 5, CE 6, DF 7
```

Kruskal's, step by step:

```
edge   weight  find(a)  find(b)  same?  action        fragments
-----  ------  -------  -------  -----  ------------  --------------------
A-B      1        A        B      no    TAKE          {AB} {C} {D} {E} {F}
B-D      2        A        D      no    TAKE          {ABD} {C} {E} {F}
E-F      2        E        F      no    TAKE          {ABD} {C} {EF}
A-D      3        A        A      YES   skip (cycle)  {ABD} {C} {EF}
A-C      4        A        C      no    TAKE          {ABCD} {EF}
C-D      5        A        A      YES   skip (cycle)  {ABCD} {EF}
C-E      6        A        E      no    TAKE          {ABCDEF}   <- 5 edges, done

total = 1 + 2 + 2 + 4 + 6 = 15
```

**What to notice.** After three edges there were three separate fragments — `{ABD}`, `{C}`, `{EF}` — and
nothing connecting them. Kruskal's does not care. It also skipped `A-D` at weight 3, which is cheaper than the
`A-C` at 4 that it later took, because by then `A` and `D` were already connected. **Cheaper is not the same as
useful.**

Prim's from `A`, on the same graph:

```
in tree        cheapest edge leaving it        take        total
------------   ----------------------------    ---------   -----
{A}            A-B 1, A-C 4, A-D 3             A-B (1)       1
{A,B}          B-D 2, A-C 4, A-D 3             B-D (2)       3
{A,B,D}        A-C 4, C-D 5, D-F 7             A-C (4)       7
{A,B,C,D}      C-E 6, D-F 7                    C-E (6)      13
{A,B,C,D,E}    E-F 2, D-F 7                    E-F (2)      15
{A,B,C,D,E,F}  done                                         15
```

**What to notice.** Same total, 15, and the same set of edges — but discovered in a different order, and the
tree was connected at every step. And at the fourth row Prim's took `C-E` at 6 while an edge of weight 2
(`E-F`) existed in the graph — because `E-F` did not touch the tree yet. **Prim's can only take edges leaving
the current blob.**

And now the thing everyone gets wrong once:

```
MINIMUM SPANNING TREE  is  NOT  SHORTEST PATH TREE

        A
       / \
     1/   \1
     /     \
    B ------ C
        1

  MST from any start:  any two of the three edges, total 2
                       say A-B and A-C

  Shortest paths from B:  B->A = 1,  B->C = 1   (direct)
  In the MST above:       B->A = 1,  B->C = 2   (via A)

  The MST made B-to-C twice as expensive as it needs to be.
```

```
And more starkly:

    A --1-- B --1-- C
    |               |
    +------10-------+          MST: takes A-B and B-C, total 2
                               Shortest path A to C: 2, via B  -- fine here

    A --1-- B --1-- C
    |               |
    +-------3-------+          MST: A-B, B-C, total 2
                               Shortest A->C = 2 via B, or 3 direct. Still fine.

    the divergence needs a star:

         hub
       /  |  \
      5   5   5              MST: the three spokes, total 15
     /    |    \             Shortest path leaf-to-leaf via hub: 10
    L1   L2   L3
     \___6___/               but a 6-edge L1-L2 exists!
                             MST ignores it (cycle). Shortest path uses it.
```

**What to notice.** A minimum spanning tree minimises the **total** weight of the structure. A shortest-path
tree minimises **each vertex's distance from one source**. Those are different objectives and they produce
different trees.

---

## 5. The code, built step by step

Kruskal's first, because with yesterday's Union-Find it is almost nothing.

```python
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> tuple[int, list]:
    """edges are (weight, a, b). Returns (total, chosen edges)."""
    edges.sort()                                  # cheapest first
    dsu = DisjointSet(n)
    total, chosen = 0, []
    for weight, a, b in edges:
        if dsu.union(a, b):                       # False means already connected
            total += weight
            chosen.append((a, b, weight))
            if len(chosen) == n - 1:
                break                             # a spanning tree is complete
    return total, chosen
```

**Eight lines.** The sort puts the cheapest edges first; `dsu.union` returns `False` exactly when the edge
would close a cycle; and the early `break` stops once `V − 1` edges are in, because nothing more can be
added.

Storing edges as `(weight, a, b)` rather than `(a, b, weight)` means a plain `sort()` sorts by weight with no
key function — a small thing that removes a place to make a mistake.

**Detecting a disconnected graph is one line**, and it is the check people forget:

```python
    if len(chosen) != n - 1:
        return -1, chosen                         # not connected: a forest, not a tree
```

Prim's next, with a heap.

```python
import heapq

def prim(n: int, graph: dict[int, list[tuple[int, int]]], start: int = 0):
    """graph[v] holds (neighbour, weight) pairs."""
    in_tree = [False] * n
    heap: list[tuple[int, int, int]] = [(0, start, -1)]   # (weight, vertex, came_from)
    total, chosen = 0, []
    while heap and len(chosen) < n - 1:
        weight, vertex, came_from = heapq.heappop(heap)
        if in_tree[vertex]:
            continue                              # stale entry
        in_tree[vertex] = True
        if came_from != -1:
            total += weight
            chosen.append((came_from, vertex, weight))
        for neighbour, w in graph[vertex]:
            if not in_tree[neighbour]:
                heapq.heappush(heap, (w, neighbour, vertex))
    return total, chosen
```

**Compare this with Dijkstra line by line** and the only real difference is what goes into the heap:

```python
# Dijkstra:  heapq.heappush(heap, (cost + w, neighbour))       accumulated
# Prim:      heapq.heappush(heap, (w, neighbour, vertex))      the edge alone
```

**One term.** Everything else — the stale-entry skip, the `in_tree` marking, the pop-the-cheapest — is
identical. Saying that out loud shows you see the shared shape rather than having memorised two things.

The `if in_tree[vertex]: continue` is lazy deletion, exactly as in Dijkstra: the heap can hold several entries
for the same vertex and the later ones are skipped.

**The dense version of Prim's has no heap at all**, and it is genuinely better on a complete graph:

```python
def prim_dense(n: int, matrix: list[list[float]]) -> float:
    """O(V^2). Better than the heap version when E is close to V^2."""
    in_tree = [False] * n
    best = [float("inf")] * n                     # cheapest edge reaching each vertex
    best[0] = 0
    total = 0.0
    for _ in range(n):
        u = min((v for v in range(n) if not in_tree[v]), key=lambda v: best[v])
        in_tree[u] = True
        total += best[u]
        for v in range(n):                        # relax against the whole row
            if not in_tree[v] and matrix[u][v] < best[v]:
                best[v] = matrix[u][v]
    return total
```

`best[v]` is "the cheapest single edge from the current tree to `v`", and each round takes the smallest of
those. **No heap, `O(V²)`, and on a graph where `E ≈ V²` that beats `O(E log V) = O(V² log V)`.**

### The complete solution

```python
"""Minimum spanning trees: Kruskal's with Union-Find, and Prim's with a heap."""

from __future__ import annotations

import heapq


class DisjointSet:
    __slots__ = ("parent", "size", "groups")

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True


def kruskal(n: int, edges: list[tuple[int, int, int]]) -> tuple[int, list]:
    """Sort every edge, take each that does not close a cycle. O(E log E)."""
    dsu = DisjointSet(n)
    total, chosen = 0, []
    for weight, a, b in sorted(edges):
        if dsu.union(a, b):
            total += weight
            chosen.append((a, b, weight))
            if len(chosen) == n - 1:
                break
    if len(chosen) != n - 1:
        return -1, chosen                         # disconnected: a forest
    return total, chosen


def prim(n: int, graph: dict[int, list[tuple[int, int]]], start: int = 0) -> tuple[int, list]:
    """Grow one connected tree, always taking the cheapest edge leaving it.

    Structurally identical to Dijkstra except for what is pushed:
        Dijkstra pushes (cost_so_far + w, ...)   -- accumulated
        Prim     pushes (w, ...)                 -- the single edge
    """
    in_tree = [False] * n
    heap: list[tuple[int, int, int]] = [(0, start, -1)]
    total, chosen = 0, []
    while heap and len(chosen) < n - 1:
        weight, vertex, came_from = heapq.heappop(heap)
        if in_tree[vertex]:
            continue
        in_tree[vertex] = True
        if came_from != -1:
            total += weight
            chosen.append((came_from, vertex, weight))
        for neighbour, w in graph[vertex]:
            if not in_tree[neighbour]:
                heapq.heappush(heap, (w, neighbour, vertex))
    if len(chosen) != n - 1:
        return -1, chosen
    return total, chosen


if __name__ == "__main__":
    # Yusuf's six houses. 0=A 1=B 2=C 3=D 4=E 5=F
    edge_list = [
        (1, 0, 1), (3, 0, 3), (4, 0, 2),
        (2, 1, 3), (5, 2, 3), (6, 2, 4),
        (7, 3, 5), (2, 4, 5),
    ]
    adjacency: dict[int, list[tuple[int, int]]] = {v: [] for v in range(6)}
    for w, a, b in edge_list:
        adjacency[a].append((b, w))
        adjacency[b].append((a, w))

    k_total, k_edges = kruskal(6, edge_list)
    p_total, p_edges = prim(6, adjacency)
    print("kruskal:", k_total, sorted((min(a, b), max(a, b)) for a, b, _ in k_edges))
    print("prim   :", p_total, sorted((min(a, b), max(a, b)) for a, b, _ in p_edges))

    # Disconnected: two components, no spanning tree exists.
    print("forest :", kruskal(4, [(1, 0, 1), (1, 2, 3)])[0])

    # MST is not a shortest-path tree.
    triangle = [(1, 0, 1), (1, 0, 2), (1, 1, 2)]
    print("triangle MST total:", kruskal(3, triangle)[0], "(any two of three edges)")
```

Running it:

```
kruskal: 15 [(0, 1), (0, 2), (1, 3), (2, 4), (4, 5)]
prim   : 15 [(0, 1), (0, 2), (1, 3), (2, 4), (4, 5)]
forest : -1
triangle MST total: 2 (any two of three edges)
```

Three things to look at. **Both algorithms found the same total and the same edge set** — because on this
graph the weights are distinct, so the minimum spanning tree is unique. With ties they could legitimately
differ.

`forest` returns `-1`: four vertices, two edges, two components, and no spanning tree exists. **The check is
`len(chosen) != n - 1`** and it is the line most people leave out.

And the triangle: total 2, using two of the three unit edges. Every vertex is connected, and the pair not
directly joined now costs 2 to travel between instead of 1 — which is the MST-is-not-shortest-path point,
made concrete.

---

## 6. What it costs

**Kruskal's.**

```
sort the edges                    O(E log E)
E union operations at O(alpha)    O(E x alpha) ~ O(E)
                                  ---------------------
                                  O(E log E)  -- the SORT dominates
space: the DSU arrays             O(V)
```

**The Union-Find part is effectively free relative to the sorting.** And since `E ≤ V²`, `log E ≤ 2 log V`, so
this is often written `O(E log V)` — the same thing.

**If the edges are already sorted, or can be sorted in linear time** — small integer weights, counting sort —
Kruskal's becomes `O(E × α)`, effectively linear. That is a real optimisation and worth mentioning.

**Prim's, with a binary heap.**

```
each vertex popped once                       V
each edge pushed at most once                 E
each push and pop                             log(heap size) = log E
                                              --------------------
                                              O(E log V)
space: heap up to E entries                   O(E)
```

**Prim's, dense version with no heap.**

```
V rounds, each scanning V vertices             V x V
plus relaxing a row of V                       V x V
                                               -----------
                                               O(V^2)
space: two arrays of V                         O(V)
```

**Now the comparison that decides which to use.**

```
SPARSE:  V = 100,000, E = 300,000
  Kruskal      300,000 x log(300,000) = 300,000 x 18  = 5,400,000
  Prim (heap)  300,000 x 17                           = 5,100,000
  Prim (dense) 100,000^2                              = 10,000,000,000
```

```
DENSE:   V = 5,000, E = 12,500,000  (complete graph)
  Kruskal      12,500,000 x 24                        = 300,000,000
  Prim (heap)  12,500,000 x 12                        = 150,000,000
  Prim (dense) 5,000^2                                = 25,000,000
```

**On a sparse graph, Kruskal's and heap-Prim's are equivalent and the dense version is hopeless. On a dense
graph, the dense version wins by an order of magnitude.**

**The rule to say:**

```
sparse graph, edges given as a list   ->  Kruskal   (and the sort is the cost)
dense graph, or an adjacency matrix   ->  Prim, O(V^2), no heap
edges arriving over time              ->  Kruskal, because Union-Find is online
need the tree connected as it grows   ->  Prim
```

**Memory, at scale:**

```
V = 1,000,000, E = 5,000,000
Kruskal   edge list 5,000,000 tuples   ~360 MB
          DSU arrays                   ~16 MB
          plus the sort's working space
Prim      adjacency 5,000,000 entries  ~400 MB
          heap up to E                 ~360 MB
```

**Kruskal's needs all the edges in memory to sort them**, which is its main practical constraint. Prim's needs
the adjacency structure plus the heap. Neither is obviously better; Kruskal's sort can be done externally if
it truly does not fit.

**Against Dijkstra**, since the code is nearly identical:

```
same graph, V = 100,000, E = 300,000
Dijkstra      5,100,000
Prim          5,100,000
```

**Identical cost, different answer.** That is worth saying, because it makes clear that the difference is
semantic and not a performance trade.

---

## 7. The traps

### Confusing a minimum spanning tree with shortest paths

The conceptual error, and it produces confidently wrong answers:

```python
tree = prim(n, graph, start=source)
# "now I have the shortest path from source to everything"
```

```
triangle: A-B = 1, A-C = 1, B-C = 1
MST from A: {A-B, A-C}, total 2
distance B to C in the MST: 2
true shortest path B to C:  1
```

**A minimum spanning tree minimises the total; a shortest-path tree minimises each vertex's distance from one
source.** Different objectives. The tell is the one-line difference in what goes into the heap, and if you
copied Dijkstra to write Prim's, check that line.

### Prim's written with Dijkstra's key

```python
heapq.heappush(heap, (weight + w, neighbour, vertex))     # accumulated: WRONG for Prim
```

This runs, produces a spanning tree, and produces the wrong one:

```
A --1-- B --1-- C,  A --3-- C
correct MST:   A-B, B-C, total 2
with the bug:  A-B (1), then from B the key for C is 1+1=2, and A-C is 3
               -> still picks B-C. Same answer here.

A --1-- B --5-- C,  A --4-- C
correct MST:   A-B (1), A-C (4), total 5
with the bug:  A-B (1), then key(C) via B = 1+5 = 6, via A = 4 -> picks A-C. Same.
```

It agrees surprisingly often, which is what makes it dangerous — **on a graph where an expensive early edge
leads to cheap later ones, the accumulated version starts preferring different edges.** Test with a long chain
of small weights against a single medium edge.

### Forgetting the connectivity check

```python
return total
```

On a disconnected graph both algorithms terminate happily, having built a spanning **forest**:

```
>>> kruskal_no_check(4, [(1, 0, 1), (1, 2, 3)])
2                                   # a total, for a graph with no spanning tree
```

The number looks fine. **`len(chosen) != n - 1` is the check**, and the convention in most problems is to
return `-1`.

### The stale-entry skip missing from Prim's

```python
while heap:
    weight, vertex, came_from = heapq.heappop(heap)
    in_tree[vertex] = True                # no check
    total += weight
```

A vertex can be pushed many times, once per edge reaching it, and without the skip you add several of those
edges — producing a structure with cycles and a total that is too large. **The check is one line and it is the
same lazy deletion as Dijkstra's.**

### Sorting with a key function unnecessarily

```python
edges.sort(key=lambda e: e[2])            # (a, b, weight)
```

Correct, and slower, and it invites the mistake of forgetting the key. **Store edges as `(weight, a, b)` and a
plain `sort()` does the right thing** — one less thing to get wrong, and measurably faster on large inputs
because it avoids a Python-level call per comparison.

### Using it on a directed graph

```python
kruskal(n, directed_edges)
```

Union-Find has no notion of direction, so this computes a minimum spanning tree of the **undirected** version
of the graph and reports it as though the directions were respected. The directed analogue is a **minimum
spanning arborescence** — every vertex reachable from a chosen root, following the arrows — and it needs a
completely different algorithm (Chu–Liu/Edmonds'). **Name it and do not attempt it**; the point is knowing that
Kruskal's and Prim's do not apply.

### Assuming the tree is unique

```python
assert kruskal(n, edges)[1] == expected_edges
```

With tied weights there can be many minimum spanning trees, all of the same total. **Assert the total, not the
edge set** — the total is unique, the tree is not.

---

## 8. In the interview

### How it gets asked

- *"Connect all the cities at minimum cost."* — the direct version.
- *"Min Cost to Connect All Points."* — LeetCode 1584, and the graph is implicit.
- *"Given a network of cables with costs, which do you lay?"*
- *"Optimize water distribution in a village."* — LeetCode 1168, with the virtual-vertex trick.
- *"Which edges are critical?"* — LeetCode 1489, and the answer runs Kruskal's many times.
- *"Why does the greedy choice work?"* — the cut property question.

### The first ninety seconds

> "Minimum spanning tree — connect every vertex with `V − 1` edges at the lowest total cost, and no cycles,
> because every edge in a cycle can be removed without disconnecting anything.
>
> Two algorithms, both greedy and both provably correct.
>
> **Kruskal's** sorts every edge by weight and takes each one whose endpoints are not already connected.
> 'Already connected' is a Union-Find query, so this is about eight lines: sort, then loop, and `union`
> returning `False` means this edge would close a cycle and I skip it. `O(E log E)`, dominated entirely by the
> sort — the Union-Find part is effectively free.
>
> **Prim's** grows one connected tree, repeatedly taking the cheapest edge that leaves it. That needs a
> priority queue, and the code is almost exactly Dijkstra's — **the only difference is what goes into the
> heap.** Dijkstra pushes the accumulated cost from the source; Prim's pushes the single edge weight. One term,
> and it is the difference between two different answers.
>
> **Which one depends on density.** On a sparse graph both are about `E log V` and I would use Kruskal's,
> because it is shorter and because the edges usually arrive as a list anyway. On a dense graph — or when I am
> handed an adjacency matrix — the `O(V²)` version of Prim's with no heap wins: at five thousand vertices
> complete, that is twenty-five million operations against a hundred and fifty million for the heap version.
>
> **Two things I would state before coding.** If fewer than `V − 1` edges get taken, the graph was
> disconnected and there is no spanning tree — I would return `-1` rather than a total for a forest. And with
> tied weights there can be several minimum spanning trees of the same total, so I would assert the total in
> tests, not the edge set.
>
> **And the thing I would say before you ask: this is not a shortest-path tree.** On a triangle with all edges
> of weight 1, the MST takes two of them, and the two vertices not directly joined are now distance 2 apart
> instead of 1. Different objective."

### The follow-ups

**"Why does the greedy choice work? Prove it."**

> "The cut property, and the argument is a swap.
>
> **The cut property:** split the vertices into any two groups. The cheapest edge crossing between them is in
> some minimum spanning tree.
>
> **The proof:** suppose the cheapest crossing edge `e` is not in a given minimum spanning tree `T`. `T` still
> connects the two groups, so it contains some other crossing edge `f`, and `f` costs at least as much as `e`
> because `e` was the cheapest crossing edge. Now remove `f` from `T` and add `e`. The result is still
> connected — `e` reconnects the two halves that removing `f` separated — and it still has `V − 1` edges, so it
> is still a spanning tree, and its total weight is no larger. So a minimum spanning tree containing `e`
> exists.
>
> **Both algorithms are repeated applications of that.** Prim's cut is 'in the tree' against 'not in the tree',
> and it takes the cheapest edge crossing it — which the cut property says is safe. Kruskal's cut is around
> whichever fragment the next edge would attach to; every edge it takes is the cheapest one leaving that
> fragment, because anything cheaper has already been considered and either taken or rejected as a cycle.
>
> **The related property, for the other direction, is the cycle property:** the heaviest edge in any cycle is
> not in any minimum spanning tree. That is what justifies skipping — an edge whose endpoints are already
> connected closes a cycle, and being last in the sorted order makes it the heaviest in that cycle."

**"Kruskal's or Prim's? What decides it?"**

> "Density, and what form the input arrives in.
>
> **Sparse** — `E` close to `V` — both are about `E log V` and I would take Kruskal's, because it is shorter,
> because the input is usually already an edge list, and because it reuses Union-Find which I probably have
> anyway.
>
> **Dense** — `E` close to `V²`, or an adjacency matrix — the `O(V²)` Prim's without a heap. On a complete
> graph of five thousand vertices that is twenty-five million operations, against a hundred and fifty million
> for heap-Prim's and three hundred million for Kruskal's. **The heap becomes the overhead when almost every
> pair is an edge.**
>
> **Two more considerations.** If edges arrive over time, Kruskal's fits naturally because Union-Find is an
> online structure — although a true incremental MST needs more care than just re-running it. And if I need the
> tree to be connected at every stage — laying cable, and wanting to test the signal as I go — Prim's gives me
> that and Kruskal's does not, because Kruskal's has disconnected fragments for most of its run.
>
> **One more, on memory:** Kruskal's needs every edge in memory to sort them. On a graph with fifty million
> edges that is the binding constraint, and Prim's streaming over an adjacency structure may be the only
> option — or an external sort."

**"The points are on a plane and any two can be connected, with cost equal to the distance."**

> "Then the graph is **implicit and complete**, and the first thing I would say is the edge count: `n` points
> means `n(n−1)/2` edges. At a thousand points that is half a million — fine. At a hundred thousand it is five
> billion, and building the edge list is impossible.
>
> **For `n` up to a few thousand: the dense Prim's, `O(n²)`, and never build the edge list at all.** Keep an
> array of 'cheapest distance from the tree to each point', pick the minimum each round, add it, and update
> every remaining point against the newly added one. Two arrays, no heap, `n²` distance computations, and the
> memory is `O(n)` rather than `O(n²)`. **That is the answer to LeetCode 1584 and it is worth recognising
> immediately** — Kruskal's here would build and sort half a million edges to solve something that needs a
> million distance calculations and no storage.
>
> **Beyond a few thousand points**, the geometry helps: the minimum spanning tree of points on a plane is a
> subgraph of the **Delaunay triangulation**, which has only `O(n)` edges. So compute that first — `O(n log
> n)` — and run Kruskal's over its edges. That takes a hundred thousand points from impossible to routine. I
> would name it rather than implement it, but knowing that the complete graph is not necessary is the
> insight."

**"Which edges must be in every minimum spanning tree, and which are in none?"**

> "Three categories, and the standard approach runs the algorithm repeatedly.
>
> **Critical** — removing it increases the MST's total, so it is in every minimum spanning tree. Test: compute
> the MST weight normally; then compute it again with that edge **excluded**. If the total goes up, or the
> graph becomes disconnected, the edge is critical.
>
> **Pseudo-critical** — it is in *some* minimum spanning tree but not all. Test: compute the MST weight with
> that edge **forced in** — take it first, then run Kruskal's on the rest. If the total equals the normal
> minimum, it belongs to some MST.
>
> **Neither** — in no minimum spanning tree at all.
>
> That is `O(E)` runs of Kruskal's, so `O(E² log E)`, which is fine for the few hundred edges these problems
> use and would not scale. **The linear-time answer uses the cycle property**: an edge is in no MST exactly
> when it is the unique heaviest edge on some cycle, and Tarjan's approach finds all of them together — I
> would name that as what I would reach for if `E` were large.
>
> **The one implementation detail worth stating:** when forcing an edge in, you must add it before sorting the
> rest, and when excluding one, you must skip it entirely rather than just deprioritise it. Both are easy to
> get subtly wrong and both produce plausible totals."

### The model answer

*"A village has `n` houses. You can dig a well in any house for a cost, or lay a pipe between two houses for a
cost. Every house must have water. Minimise the total cost."*

> "This looks like it has two different kinds of decision — dig or connect — and the whole problem is noticing
> that it does not. Let me build it up.
>
> **The naive reading is that this is not a spanning tree problem at all**, because a spanning tree connects
> things and digging a well connects nothing. And if I try to model it as 'find the MST and then decide where
> to dig', the two decisions interact and there is no clean way to separate them.
>
> **The move is a virtual vertex.** Add one extra node — call it node 0, the water source — and turn every
> well into an **edge** from node 0 to that house, with weight equal to the well's cost. Now there is only one
> kind of decision: which edges to take. Digging a well in house `i` is 'connect house `i` to the source', and
> laying a pipe is 'connect house `i` to house `j`'.
>
> **And now the problem is exactly a minimum spanning tree** over `n + 1` vertices. Every house must end up
> connected to the source, directly or through other houses; the cheapest way to connect everything is the
> MST; and it will contain `n` edges, some of which are wells and some pipes — which is precisely the answer,
> and I never had to decide the two things separately.
>
> **That reframing is the entire problem**, and I would spend the first ninety seconds on it rather than on the
> algorithm, because the algorithm is then eight lines.
>
> **Implementation: Kruskal's.** Build the edge list — `n` well edges from node 0, plus the given pipe edges —
> sort by cost, and take each edge whose endpoints are not already connected. Union-Find over `n + 1` elements.
> Stop at `n` edges.
>
> **Cost:** with `n` houses and `m` possible pipes, the edge list is `n + m`, so `O((n + m) log(n + m))`,
> dominated by the sort. For a village that is trivially fast. Space is `O(n + m)` for the edges plus `O(n)`
> for the Union-Find.
>
> **Two things I would check.** The graph is now guaranteed connected — every house has a well edge to node 0,
> so a spanning tree always exists and I will never return `-1`. That is a nice property of the reframing and
> worth noticing. And node 0 must be included in the vertex count, so the Union-Find is sized `n + 1` and the
> target is `n` edges, not `n − 1` — the classic off-by-one here.
>
> **The general pattern I would name**, because it recurs: **when a problem has a 'do it standalone' option
> alongside a 'connect to something' option, model standalone as an edge to a virtual source.** The same trick
> turns 'build a warehouse here or ship from an existing one' and 'run a generator or connect to the grid' into
> plain spanning-tree problems."

---

## 9. Recall card

**A spanning tree is `V − 1` edges, connected, no cycles.** Minimum = cheapest total. **A cycle is wasted
weight**, which is why both algorithms are about avoiding one.

**Kruskal's: sort all edges, take each one where `union` returns `True`.** `O(E log E)` — the **sort**
dominates; Union-Find is free. Fragments stay disconnected for most of the run, and that is fine.

**Prim's: grow one blob, always taking the cheapest edge leaving it.** Structurally identical to Dijkstra
except for **one line** — Dijkstra pushes `cost_so_far + w`, Prim pushes `w`. Sparse → either; **dense or a
matrix → the `O(V²)` Prim with no heap.**

**Why greedy is correct: the cut property.** Split the vertices any way; the cheapest crossing edge is in some
MST — proved by swapping it for whatever crossing edge the tree used. Both algorithms are repeated
applications of it.

**Three things to state:** an MST is **not** a shortest-path tree (triangle of 1s: MST makes two vertices
distance 2 apart); fewer than `V − 1` edges means **disconnected**, return `-1`; and with tied weights the tree
is not unique, so assert the **total**.
