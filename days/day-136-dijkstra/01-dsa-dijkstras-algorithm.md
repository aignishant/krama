---
day: 136
track: dsa
title: "Dijkstra's algorithm"
phase: "Graphs"
status: written
---

# Dijkstra's algorithm

## 1. What this is, and why they ask it

Dijkstra's algorithm finds the cheapest path from one vertex to every other, when the edges have costs. It is
BFS with one substitution: instead of a queue, which hands back whatever arrived first, you use a **priority
queue**, which hands back whatever is cheapest so far.

That single change is the whole algorithm. Everything else — the distance map, the relaxation, the early
exit — you already have from [day 127](../day-127-graph-bfs/README.md).

They ask it constantly, and the reason is that the answer has two halves and most candidates give only one.
Writing Dijkstra is twenty lines. **Saying why the greedy choice is correct**, and **naming the exact
assumption that makes it correct**, is the half that separates people. The assumption is that every edge cost
is non-negative, and if you cannot say what breaks without it, you have memorised an algorithm rather than
understood one.

There is also a specific implementation detail — what to do when you find a shorter route to a vertex already
sitting in the heap — that has a right answer, a wrong answer that is slow, and a wrong answer that crashes.

By the end of this lesson you can write it from memory with the lazy-deletion pattern, prove the greedy choice
in three sentences, give its cost with both heap types, reconstruct the path, and name the four situations
where it is the wrong tool.

---

## 2. The story

Farhan has been delivering documents on a motorbike for eleven years, and he does not think about the city in
kilometres.

He thinks in minutes, and the two are not the same thing at all. The route from the office to Lower Parel that
looks direct on the map goes through the market, and between eleven and two that is forty minutes for three
kilometres. The long way round by the flyover is eleven kilometres and it is fifteen minutes.

New riders take the short one, every time, for about the first month.

What Farhan has in his head is a set of small facts. Not routes — pairs. From the office to the signal is
four minutes. Signal to the bridge, seven. Bridge to Lower Parel, five. Office to the market entrance, two.
Market entrance to Lower Parel, thirty-eight. Two hundred or so of these, built up over years.

When somebody hands him an address he has not been to, he does something quite specific and he does it fast.

He starts from where he is and looks at the places he can reach directly. The nearest is two minutes away, so
he takes that one first — not because it is on the way, but because two minutes is the smallest number he has.
He has now settled that place: whatever else he discovers, no route to it can beat two minutes, because
everything else starts at four minutes or more.

Then from there, and from everywhere else he has settled, he looks at what is newly reachable and picks the
smallest total again. Four minutes to the signal. Then two plus five is seven to the flyover entrance. Then
four plus seven is eleven to the bridge.

He works outwards by *total time from the start*, never by distance and never by the order the roads happen to
run in, and he stops the moment the address he wants comes up as the smallest remaining number.

His nephew, who joined last year, asked him why he does not just follow the shortest route on the phone and
Farhan said something that took the boy a while to understand: the phone is doing the same thing, it just has
more numbers than he does.

The one thing that would break his method — and this is the part that has never come up, because it cannot —
is a road that gave you time back. If riding down one particular lane somehow made it earlier than when you
started, then a place he had settled at two minutes might turn out to be reachable in less, and everything he
had already decided would have to be reconsidered. Every road costs something. That is why the method works.

---

## 3. The idea in plain English

Farhan's method is Dijkstra's algorithm, and his last paragraph is the proof.

**A weighted graph has a number on each edge.** The **weight** is a cost — minutes, rupees, distance, risk.
Shortest path now means **cheapest total**, the sum of the weights along the way, not the fewest edges.

**BFS is wrong the moment weights appear**, and this is worth being blunt about. BFS minimises the *number* of
edges. A one-edge road costing 38 minutes and a two-edge route costing 7 are the same to BFS, and it picks the
38. It runs, it returns a path, and the path is wrong. That is
[day 131](../day-131-unweighted-shortest-path/README.md)'s boundary, and today is what sits on the other side
of it.

**The fix is one substitution: a priority queue instead of a queue.** A **priority queue** hands back the
smallest item rather than the oldest. In Python that is `heapq`, from [day 115](../day-115-heapq/README.md).
Instead of expanding whatever arrived first, you expand whatever is **cheapest so far**.

**Every vertex has a tentative distance, and it only ever goes down.** Start everything at infinity except the
source, which is zero. As you discover routes, you improve the numbers.

**Relaxation is the one operation.** Standing at `u` with a known distance, look at an edge `u → v` with
weight `w`. If `distance[u] + w` is less than the best you knew for `v`, you have found a better route — record
it, and put `v` in the priority queue with its new cost. **That is the entire body of the loop.**

**Settling is the idea that makes it correct.** When a vertex comes out of the priority queue, its distance is
**final**. Not provisional — final. Farhan taking the two-minute place first and knowing nothing can beat it.

**And here is the three-sentence proof, which is the half of the answer people miss.** Suppose you pop vertex
`v` with tentative distance `d`, and suppose some cheaper route to `v` exists. That route must leave the
settled set at some point, through a vertex `x` still in the queue — and `x`'s tentative distance is at least
`d`, because `v` was the smallest in the queue. **Since no edge has negative weight, the rest of the route from
`x` to `v` cannot reduce the total below `d`.** So no cheaper route exists, and `d` is final.

**That proof is where the non-negative requirement lives.** Every step of it is fine except the last sentence,
and the last sentence is exactly "the rest of the journey cannot give time back". With a negative edge, a
longer route through `x` could still end up cheaper, a settled vertex would need reopening, and the algorithm's
central promise fails. **Dijkstra does not merely give a worse answer with negative weights — the reasoning it
is built on stops holding**, and the fix is Bellman-Ford, which is
[tomorrow](../day-137-bellman-ford/README.md).

**Now the implementation detail that has a right answer.** When you find a better route to a vertex already
sitting in the heap, you would ideally *decrease* its key. Python's `heapq` has no such operation. Three
options:

1. **Lazy deletion.** Push the vertex again with the new smaller cost, and when popping, skip anything whose
   popped distance is worse than the recorded best. The heap holds stale entries, and they are harmless.
   **This is the standard answer and the one to write.**
2. **A `visited` set** to skip vertices already settled — equivalent, and slightly less precise because it does
   not catch a stale entry for an unsettled vertex.
3. **An indexed heap** supporting `decrease-key`. Fewer heap entries, considerably more code, and almost never
   worth it in an interview.

**With lazy deletion the heap can hold up to `E` entries rather than `V`**, and that is fine: the cost is
`O(E log E)`, and since `E ≤ V²`, `log E ≤ 2 log V`, so it is the same as `O(E log V)`. Say that if asked; it
is the sort of detail that shows you have thought about it.

**Early exit is legitimate.** If you only want the distance to one target, return the moment you pop it —
because popping means settled means final.

**And the path, not just the distance, is a `parent` map**, exactly as in BFS: record who improved you, and
walk backwards at the end.

---

## 4. The picture

Farhan's city, with minutes on the edges:

```
                    (7)
        signal ------------- bridge
       /                        \
    (4)                          (5)
     /                             \
  office                          Lower Parel
     \                             /
    (2)                          (38)
       \                        /
        market ----------------
                   
    also: office --(3)-- flyover --(9)-- bridge
```

```
DIJKSTRA from office:

settled   heap (cost, vertex)                    distances
--------  --------------------------------      -------------------------------
{}        [(0,office)]                          office 0, rest inf
office    [(2,market), (3,flyover), (4,signal)] market 2, flyover 3, signal 4
market    [(3,flyover), (4,signal), (40,LP)]    LP 40  (2 + 38)
flyover   [(4,signal), (12,bridge), (40,LP)]    bridge 12  (3 + 9)
signal    [(11,bridge), (12,bridge), (40,LP)]   bridge 11  (4 + 7)  <- improved
bridge    [(12,bridge stale), (16,LP), (40,LP)] LP 16  (11 + 5)     <- improved
                                                pop (12,bridge) -> STALE, skip
LP        answer: 16 minutes via signal and bridge
```

**What to notice.** Two things. `bridge` is pushed twice — at 12 via the flyover and at 11 via the signal —
and the stale 12 is popped later and skipped. That is lazy deletion in action, and the heap holding both is
normal rather than a bug.

And `Lower Parel` was first discovered at 40 through the market. If this were BFS, the market route is **one
edge** and would have won. Dijkstra finds 16.

BFS against Dijkstra on exactly that:

```
   office --(38)-- Lower Parel          BFS:      1 edge   -> picks this, cost 38
   office --(4)-- signal --(7)--
          bridge --(5)-- Lower Parel    Dijkstra: 3 edges  -> cost 16
```

**What to notice.** BFS is not approximately wrong here, it is wrong by a factor of two and a bit, and nothing
about its output says so.

The settling frontier, which is the mental picture worth keeping:

```
        settled (final)          frontier (in the heap)      unseen
      +-------------------+     +--------------------+
      | office 0          |     | signal 4           |     everything
      | market 2          | --> | bridge 12          |     else at inf
      | flyover 3         |     | Lower Parel 40     |
      +-------------------+     +--------------------+
           ^                            ^
           |                            |
    distances are FINAL          distances are the best
    and never change             route found SO FAR

    the next pop is always the smallest number in the frontier,
    and it moves to the settled set permanently.
```

---

## 5. The code, built step by step

Start with the graph shape. Weighted adjacency lists hold pairs.

```python
graph: dict[int, list[tuple[int, int]]] = {
    0: [(1, 4), (2, 2)],        # (neighbour, weight)
    1: [(3, 7)],
    2: [(3, 38)],
    3: [],
}
```

Now the core loop, and it is BFS with the queue swapped.

```python
import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], n: int, source: int) -> list[float]:
    distance = [float("inf")] * n
    distance[source] = 0
    heap = [(0, source)]                              # (cost so far, vertex)
    while heap:
        cost, vertex = heapq.heappop(heap)
        if cost > distance[vertex]:
            continue                                  # a stale entry: skip it
        for neighbour, weight in graph[vertex]:
            candidate = cost + weight
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate       # relax
                heapq.heappush(heap, (candidate, neighbour))
    return distance
```

Eleven lines, and three of them carry the whole thing.

**`heapq.heappop` gives the smallest**, which is the substitution. The tuple is `(cost, vertex)` in that order
so the heap sorts by cost.

**`if cost > distance[vertex]: continue` is lazy deletion.** When a vertex was improved after being pushed,
the old, larger entry is still in the heap. Popping it and finding that its cost is worse than the recorded
distance means it is stale, and skipping it is correct and cheap. **Without this line the algorithm is still
correct** — the relaxation check `candidate < distance[neighbour]` prevents any damage — **but you re-scan the
neighbours of stale vertices for nothing.**

**`if candidate < distance[neighbour]` is relaxation**, and it is the only place distances change.

Now the version that stops early, when you want one target:

```python
def dijkstra_to(graph, n: int, source: int, target: int) -> float:
    distance = [float("inf")] * n
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        cost, vertex = heapq.heappop(heap)
        if vertex == target:
            return cost                               # popped == settled == final
        if cost > distance[vertex]:
            continue
        for neighbour, weight in graph[vertex]:
            if cost + weight < distance[neighbour]:
                distance[neighbour] = cost + weight
                heapq.heappush(heap, (cost + weight, neighbour))
    return float("inf")
```

Returning on the **pop**, not on the relaxation. Returning when the target is first *discovered* would be
wrong — a cheaper route to it may still be found. Popping it means it is settled.

And the path:

```python
def dijkstra_path(graph, n: int, source: int, target: int) -> tuple[float, list[int]]:
    distance = [float("inf")] * n
    parent: list[int | None] = [None] * n
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        cost, vertex = heapq.heappop(heap)
        if vertex == target:
            break
        if cost > distance[vertex]:
            continue
        for neighbour, weight in graph[vertex]:
            if cost + weight < distance[neighbour]:
                distance[neighbour] = cost + weight
                parent[neighbour] = vertex            # who improved me
                heapq.heappush(heap, (cost + weight, neighbour))

    if distance[target] == float("inf"):
        return float("inf"), []
    path, node = [], target
    while node is not None:
        path.append(node)
        node = parent[node]
    return distance[target], path[::-1]
```

`parent[neighbour] = vertex` goes **inside** the relaxation, so it is only updated when the route actually
improves. Putting it outside records the last vertex that looked at the neighbour, which is usually not the one
on the best path.

**The variant worth knowing: a state that is more than a vertex.** Many interview problems are Dijkstra where
the "vertex" is a pair — position plus something else.

```python
# "cheapest flight with at most k stops": the state is (city, stops used)
heap = [(0, source, 0)]
best: dict[tuple[int, int], float] = {(source, 0): 0}
while heap:
    cost, city, stops = heapq.heappop(heap)
    if city == target:
        return cost
    if stops == limit + 1:
        continue
    for nxt, price in graph[city]:
        if cost + price < best.get((nxt, stops + 1), float("inf")):
            best[(nxt, stops + 1)] = cost + price
            heapq.heappush(heap, (cost + price, nxt, stops + 1))
```

**The algorithm is unchanged; only the definition of a vertex expanded.** Recognising that a problem is
"Dijkstra over states" rather than "Dijkstra over places" is one of the most valuable things in this phase.

### The complete solution

```python
"""Dijkstra's algorithm: distances, path, and the state-space variant."""

from __future__ import annotations

import heapq

INF = float("inf")


def build(edges: list[tuple[int, int, int]], n: int, directed: bool = False):
    """edges are (a, b, weight). Adjacency of (neighbour, weight) pairs."""
    graph: dict[int, list[tuple[int, int]]] = {v: [] for v in range(n)}
    for a, b, weight in edges:
        graph[a].append((b, weight))
        if not directed:
            graph[b].append((a, weight))
    return graph


def dijkstra(graph, n: int, source: int) -> list[float]:
    """Cheapest cost from source to every vertex. O((V + E) log V)."""
    distance = [INF] * n
    distance[source] = 0
    heap = [(0.0, source)]
    while heap:
        cost, vertex = heapq.heappop(heap)
        if cost > distance[vertex]:
            continue                                  # stale heap entry
        for neighbour, weight in graph[vertex]:
            candidate = cost + weight
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate
                heapq.heappush(heap, (candidate, neighbour))
    return distance


def dijkstra_path(graph, n: int, source: int, target: int) -> tuple[float, list[int]]:
    """Cheapest cost and one cheapest path. Stops as soon as target is settled."""
    distance = [INF] * n
    parent: list[int | None] = [None] * n
    distance[source] = 0
    heap = [(0.0, source)]
    while heap:
        cost, vertex = heapq.heappop(heap)
        if vertex == target:
            break
        if cost > distance[vertex]:
            continue
        for neighbour, weight in graph[vertex]:
            candidate = cost + weight
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate
                parent[neighbour] = vertex
                heapq.heappush(heap, (candidate, neighbour))
    if distance[target] == INF:
        return INF, []
    path: list[int] = []
    node: int | None = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return distance[target], path[::-1]


def cheapest_with_stops(graph, source: int, target: int, limit: int) -> float:
    """Dijkstra where the state is (city, stops used) — the shape to recognise."""
    heap: list[tuple[float, int, int]] = [(0.0, source, 0)]
    best: dict[tuple[int, int], float] = {(source, 0): 0.0}
    while heap:
        cost, city, stops = heapq.heappop(heap)
        if city == target:
            return cost
        if stops > limit:
            continue
        for nxt, price in graph[city]:
            state = (nxt, stops + 1)
            if cost + price < best.get(state, INF):
                best[state] = cost + price
                heapq.heappush(heap, (cost + price, nxt, stops + 1))
    return INF


if __name__ == "__main__":
    # Farhan's city.  0 office, 1 signal, 2 market, 3 flyover, 4 bridge, 5 Lower Parel
    city = build([
        (0, 1, 4), (0, 2, 2), (0, 3, 3),
        (1, 4, 7), (3, 4, 9), (4, 5, 5),
        (2, 5, 38),
    ], n=6)

    print("distances:", dijkstra(city, 6, 0))
    cost, path = dijkstra_path(city, 6, 0, 5)
    print("best to LP:", cost, path)

    flights = {0: [(1, 100), (2, 500)], 1: [(2, 100)], 2: []}
    print("<=0 stops :", cheapest_with_stops(flights, 0, 2, 0))
    print("<=1 stop  :", cheapest_with_stops(flights, 0, 2, 1))
```

Running it:

```
distances: [0, 4, 2, 3, 11, 16]
best to LP: 16 [0, 1, 4, 5]
<=0 stops : 500
<=1 stop  : 200
```

Two things to look at. `bridge` (vertex 4) settles at **11**, via the signal, not at 12 via the flyover — and
both were in the heap at once, with the 12 popped later and skipped as stale.

And Lower Parel is 16 via `[office, signal, bridge, LP]`, a three-edge route, when a one-edge route existed at
38. **BFS would have returned that one-edge route**, which is the whole reason this algorithm exists.

The flights output shows the state variant working: with no stops allowed the only option is the direct 500;
with one stop allowed, 100 + 100 = 200 wins.

---

## 6. What it costs

**Count it from the operations.**

```
each vertex is pushed at least once                    V pushes
each successful relaxation pushes once                 up to E pushes
                                                       ----------------
heap entries                                           O(V + E) = O(E)
each push and pop                                      log(heap size)
                                                       ----------------
total                                                  O(E log E)
```

And since `E ≤ V²`, `log E ≤ 2 log V`, so this is conventionally written:

```
O((V + E) log V)      binary heap (Python's heapq)
```

**With a Fibonacci heap it is `O(E + V log V)`**, which is asymptotically better and slower in practice for
every realistic input because of its constant factors. **Mention it and say you would not use it** — that is
the right answer, not reciting it as though it were the default.

**On a dense graph, the array version wins:**

```
no heap: scan all V vertices to find the minimum each time
    V iterations x V scan = O(V^2)

compare on a dense graph, E ~ V^2:
    heap:  E log V = V^2 log V
    array: V^2
    -> the ARRAY version is faster by a log factor
```

```
V = 1,000, E = 500,000 (dense)
heap  500,000 x 10 = 5,000,000
array 1,000,000
```

**Sparse graphs — which is nearly everything real — favour the heap:**

```
V = 100,000, E = 300,000 (sparse, E/V = 3)
heap  300,000 x 17 = 5,100,000
array 100,000^2    = 10,000,000,000
```

**Two thousand times faster on a sparse graph, and two times slower on a dense one.** That is the whole
comparison and it is worth having ready.

**Against BFS on the same graph:**

```
V = 100,000, E = 300,000
BFS        400,000 steps
Dijkstra   5,100,000 steps       ->  ~13x more work
```

**Which is the reason to say "BFS, because the graph is unweighted" rather than reaching for Dijkstra by
default.**

**Space:**

```
distance array          O(V)
parent array            O(V)
heap                    up to O(E) with lazy deletion
                        ------------------------------
                        O(V + E)
```

```
V = 1,000,000, E = 5,000,000
distance + parent       ~16 MB
heap at worst           5,000,000 tuples x ~72 bytes = 360 MB
```

**The heap is the memory**, and that is a real consideration at scale. The `visited`-set variant bounds pushes
better in practice, and an indexed heap bounds them to `V` at the cost of complexity.

**Early exit, measured:**

```
target 3 hops away in a graph with average degree 10
without early exit    the whole graph
with early exit       1 + 10 + 100 + 1,000 = ~1,111 vertices
                      -> on a million-vertex graph, ~900x less work
```

**And the comparison table to have ready:**

```
BFS               O(V + E)              unweighted only
0-1 BFS (deque)   O(V + E)              weights only 0 and 1
Dijkstra          O((V + E) log V)      non-negative weights
Bellman-Ford      O(V x E)              negative weights, detects negative cycles
Floyd-Warshall    O(V^3)                all pairs, small V, negatives allowed
A*                O((V + E) log V)      Dijkstra plus a heuristic; much faster in practice
```

---

## 7. The traps

### Negative weights

The near-miss that runs and lies:

```python
graph = {0: [(1, 5), (2, 2)], 2: [(1, -10)], 1: []}
```

```
>>> dijkstra(graph, 3, 0)
[0, 5, 2]
```

The true distance to vertex 1 is `2 + (-10) = -8`. Dijkstra says 5. What happened: vertex 1 was settled at 5
before vertex 2 was expanded, and **settled means never reconsidered**.

There is no error and no warning. **The only defence is to check the input**, and the answer when weights can
be negative is Bellman-Ford.

The subtler version: some problems have negative weights hidden in a transformation — "maximise profit" turned
into "minimise negative profit". **If you negate weights to turn a maximisation into a minimisation, you have
just created negative weights and Dijkstra is no longer valid.**

### Returning on discovery instead of on pop

```python
for neighbour, weight in graph[vertex]:
    if neighbour == target:
        return cost + weight              # WRONG
```

```
graph: 0 -> 1 (cost 100), 0 -> 2 (cost 1), 2 -> 1 (cost 1)
>>> wrong_version(graph, 0, 1)
100                                       # the answer is 2
```

Discovering a vertex means you have *a* route to it. **Only popping it means you have the cheapest.** Return
on the pop.

### Forgetting the stale check

```python
while heap:
    cost, vertex = heapq.heappop(heap)
    # no stale check
    for neighbour, weight in graph[vertex]:
        ...
```

Still **correct**, because relaxation guards against damage — but every stale entry causes a full re-scan of a
vertex's neighbours:

```
V = 100,000, E = 500,000, many improvements
with the check       ~500,000 neighbour scans
without              up to 2-3x more, and worse on graphs with many improvements
```

Not a crash, just slower, and on a judge it is the difference between passing and timing out.

### Pushing an object with no tie-breaker

```python
heapq.heappush(heap, (cost, node_object))
```

```
Traceback (most recent call last):
  File "dij.py", line 18, in dijkstra
    heapq.heappush(heap, (candidate, neighbour))
TypeError: '<' not supported between instances of 'Node' and 'Node'
```

Two entries with equal cost make Python compare the second element. With integers that is fine; with objects
it raises. Put an integer id between the cost and the object. **You met this on
[day 116](../day-116-top-k/README.md) and it will keep finding you.**

### Mutable state in the heap

```python
heapq.heappush(heap, (distance[v], v))
distance[v] = smaller                     # the heap entry does NOT update
```

The tuple captured the old value. This is not a bug in itself — it is exactly why lazy deletion exists — but
people write code assuming the heap re-sorts when the distance array changes. **It does not.** The heap holds
snapshots.

### Using Dijkstra when BFS would do

```python
dijkstra(unweighted_graph, n, source)     # all weights are 1
```

Correct, and about thirteen times slower on a typical sparse graph. **If every edge costs the same, say
"BFS" and say why** — reaching for the general tool when the special one applies is a real signal in an
interview.

### The state-space explosion

```python
# "cheapest path with at most k stops", k = 100, V = 100,000
```

The state is `(vertex, stops)`, so the state space is `V × (k + 1)` — ten million states here. That is still
tractable, but it is worth computing before writing, because with two extra dimensions it stops being.
**Always multiply out the state space and say the number.**

---

## 8. In the interview

### How it gets asked

- *"Find the shortest path in a weighted graph."* — the direct version.
- *"Cheapest flight from A to B."* — often with a stop limit, which is the state variant.
- *"Network delay time: how long until every node receives the signal?"* — Dijkstra, take the maximum.
- *"Path with the minimum effort / maximum minimum weight."* — Dijkstra with a different combining rule.
- *"Why can't you use BFS here?"* — the boundary question.
- *"Why does your algorithm need non-negative weights?"* — the proof question, and it is the one that sorts
  candidates.

### The first ninety seconds

> "Weights, so BFS is out — it minimises the number of edges, and with weights a three-edge route can easily be
> cheaper than a one-edge route. This is Dijkstra.
>
> It is BFS with one substitution: a priority queue instead of a queue, so instead of expanding whatever
> arrived first I expand whatever is **cheapest so far**. Everything else is the same shape — a distance map, a
> relaxation step, and an optional parent map for the path.
>
> The invariant is that **when a vertex comes out of the heap, its distance is final**, and I would give the
> reason because that is the algorithm. Suppose I pop `v` at cost `d` and a cheaper route existed. That route
> has to leave the settled set through some vertex still in the heap, and that vertex costs at least `d`,
> because `v` was the smallest. Since **no edge is negative**, the rest of the route cannot bring the total
> below `d`. So no cheaper route exists.
>
> **That last sentence is where the non-negative requirement lives.** With a negative edge, a longer route can
> still get cheaper, a settled vertex would need reopening, and the whole argument collapses — so Dijkstra is
> not just less accurate with negative weights, its reasoning stops holding. That case is Bellman-Ford.
>
> Implementation detail worth stating: Python's `heapq` has no decrease-key, so when I find a better route to a
> vertex already in the heap, I push it again and skip stale entries on pop by checking whether the popped cost
> is worse than the recorded distance. **Lazy deletion.** It means the heap can hold up to `E` entries rather
> than `V`, which is fine — `O(E log E)` is `O(E log V)` since `E ≤ V²`.
>
> `O((V + E) log V)` time, `O(V + E)` space, and if I only want one target I return the moment I **pop** it —
> not when I first discover it, because discovery only gives me *a* route.
>
> Are the weights guaranteed non-negative?"

### The follow-ups

**"Why does it need non-negative weights? Give me a concrete failure."**

> "Smallest possible example. Source `S`, with `S → A` costing 5 and `S → B` costing 2, and then `B → A`
> costing −10.
>
> Dijkstra pops `S` at 0, relaxes both, and the heap holds `(2, B)` and `(5, A)`. It pops `B` at 2 — correct —
> and relaxes `B → A`, finding `2 − 10 = −8`, which improves `A`. But if `A` had been popped first, or if the
> negative edge had been discovered after `A` was settled, `A` would be locked at 5.
>
> Make it slightly bigger and it definitely breaks: `S → A` at 1, `S → B` at 2, `B → A` at −5. `A` is popped
> first at 1 and settled. Then `B` is popped and offers `A` a route at −3, and `A` is never reconsidered. The
> answer comes back as 1 and the truth is −3.
>
> **The general statement is that Dijkstra never revisits a settled vertex, and a negative edge is exactly a
> reason to revisit one.**
>
> The trap I would watch for in a real problem is negative weights arriving through a transformation. If
> someone asks for the *maximum* profit path and I negate the weights to make it a minimisation, I have
> created negative weights and invalidated the algorithm. On a DAG that is fine — one pass in topological order
> handles any weights — but on a general graph it is Bellman-Ford, and if there is a negative *cycle* there is
> no answer at all."

**"There is a limit of at most k stops. How does that change things?"**

> "The algorithm does not change at all; **the definition of a vertex does.** The state becomes `(city, stops
> used)` rather than just `city`, and everything else is identical.
>
> The reason it has to is that the cheapest way to reach a city is no longer a single fact about that city.
> Reaching Delhi in two stops for ₹300 and in four stops for ₹100 are both useful, and plain Dijkstra would
> settle Delhi once and discard one of them. With the state expanded, `(Delhi, 2)` and `(Delhi, 4)` are
> different vertices and both survive.
>
> The cost I would compute before writing it: the state space is `V × (k + 1)`, and the edges are `E × (k + 1)`,
> so it is `O(E·k log(V·k))`. With a hundred thousand cities and ten stops that is a million states and a few
> million edges — fine. With two extra dimensions it would not be, so **I would multiply it out and say the
> number rather than assume.**
>
> The alternative for this specific problem is Bellman-Ford run exactly `k + 1` times, which is `O(k × E)` and
> is often simpler because the stop limit maps directly onto the number of relaxation rounds. For LeetCode's
> cheapest-flights problem that is the neater solution, and I would mention both."

**"The graph is a road network with ten million intersections and you need one route, fast."**

> "Dijkstra explores in expanding circles from the source, so on a road network it explores a huge disc of
> roads in every direction, including directly away from the destination. For a city-scale query that is
> wasteful and for a country-scale one it is unusable.
>
> **A\* is the direct improvement.** Same algorithm, but the priority is `distance so far + an estimate of the
> distance remaining` — for a road network, straight-line distance to the target, which is easy to compute
> from coordinates. That biases the search towards the goal, and the exploration becomes an ellipse rather
> than a circle. On real road networks it typically cuts the explored set by an order of magnitude or more.
>
> The requirement for A\* to still be *correct* is that the estimate never overestimates the true remaining
> distance — it must be **admissible**. Straight-line distance qualifies, because no road is shorter than the
> straight line. An estimate that overestimates makes it fast and wrong.
>
> **Bidirectional search also helps**, for the same reason as in BFS: two half-radius searches explore far
> less than one full-radius one. Combining bidirectional with A\* needs care about the stopping condition, so
> I would do one or the other unless I had time to get it right.
>
> **And for a production routing system, none of the above is the real answer** — it is precomputation.
> Contraction hierarchies preprocess the network once, adding shortcut edges, and then answer queries in
> microseconds rather than seconds. That is what a real map service does, and I would name it so you know I
> know the algorithm alone is not the product."

**"What if the cost is not a sum? Say I want the path whose worst segment is as good as possible."**

> "Dijkstra generalises further than people expect, and this is a nice example of that.
>
> The standard version accumulates with addition and compares with less-than. If instead I accumulate with
> `max` — the cost of a path is its worst edge — and still pick the smallest such value from the heap, the
> algorithm finds the path minimising the maximum edge. That is the 'path with minimum effort' or 'swim in
> rising water' family, and the code change is one line: `candidate = max(cost, weight)` instead of `cost +
> weight`.
>
> The reason it still works is that the proof only needs one property: **extending a path must never make it
> better.** Addition with non-negative weights has that. So does `max`. So does multiplication by
> probabilities in `[0, 1]` if you are maximising reliability and take the largest each time.
>
> **What fails is anything where extending can improve the total** — which is exactly negative weights again,
> stated more generally. So the honest version of 'Dijkstra needs non-negative weights' is 'Dijkstra needs a
> combining rule under which paths never get better as they get longer', and non-negative addition is the
> common case."

### The model answer

*"Given `n` network nodes and travel times between them, find how long it takes for a signal sent from node
`k` to reach every node. Return −1 if some node is unreachable."*

> "Single source, weighted edges, all distances — that is Dijkstra, and the answer is the **maximum** of the
> distances rather than any single one. Let me set it up.
>
> **The model.** A vertex is a node. A directed edge from `u` to `v` with weight `w` means a signal takes `w`
> time to travel that way. Directed matters — the input gives `(u, v, w)` triples and the signal does not
> travel back — so one append, not two.
>
> **Then Dijkstra from `k`.** Distance array initialised to infinity except the source at zero, a heap of
> `(cost, vertex)`, pop the cheapest, skip stale entries, relax each outgoing edge.
>
> **The answer is `max(distance)`**, because the signal has reached everything when the last node receives it.
> And if any distance is still infinity, that node is unreachable and the answer is −1 — so the check is one
> line: `return -1 if INF in distance else max(distance)`.
>
> **Two things I would state before coding.** Weights are travel times and therefore non-negative, which is
> what makes Dijkstra valid — I would confirm that rather than assume it. And I would **not** exit early here,
> because I need every distance, not one; the early-exit version is for single-target queries.
>
> **Cost:** `O((V + E) log V)`. On the LeetCode constraints — 100 nodes, 6,000 edges — that is trivial, and I
> would note that at `V = 100` with `E = 6,000` the graph is dense enough that the simple `O(V²)` array version
> without a heap would actually be faster: ten thousand operations against sixty thousand heap operations.
> **I would still write the heap version**, because it is the one that generalises, but saying that I know the
> crossover exists is worth more than the micro-optimisation.
>
> **The bugs I would be watching for as I write it.** Building the graph undirected when the input is directed
> — one wrong line, and the answer is too small with no error. Returning when the target is discovered rather
> than popped, which does not apply here since I want all distances but is the reflex to suppress. And
> pushing `(vertex, cost)` instead of `(cost, vertex)`, which makes the heap order by vertex id and produces a
> confidently wrong answer — I would write the tuple and immediately say 'cost first' out loud.
>
> **The follow-up I would expect** is 'what if some links can be down' or 'what if there are at most `k` hops',
> and both are the state-space variant: the vertex becomes `(node, something)`, and the algorithm is unchanged.
> I would mention that so you know I have the general shape rather than the one problem."

---

## 9. Recall card

**Dijkstra is BFS with a priority queue instead of a queue** — expand the cheapest-so-far rather than the
oldest. Relaxation `if dist[u] + w < dist[v]` is the only place distances change.

**Popped means settled means final**, and the three-sentence proof is: a cheaper route would have to leave the
settled set through a vertex costing at least as much, and **since no edge is negative**, the remainder cannot
bring it below. That last clause is the whole non-negative requirement.

**Lazy deletion:** no decrease-key in `heapq`, so push again and `if cost > distance[vertex]: continue` on pop.
The heap holds up to `E` entries; `O(E log E) = O(E log V)`.

**Return on the pop, not on the discovery.** Discovery gives you *a* route; popping gives you the cheapest.
And `parent[v] = u` goes **inside** the relaxation.

**`O((V + E) log V)` — about 13× BFS, so use BFS when weights are equal.** Negative weights → Bellman-Ford. A
stop limit or any extra condition → expand the *state*, not the algorithm. And the proof only needs "extending
a path never improves it", so `max` instead of `+` solves the minimise-the-worst-edge family unchanged.
