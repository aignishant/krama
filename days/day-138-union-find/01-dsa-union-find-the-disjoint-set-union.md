---
day: 138
track: dsa
title: "Union-Find: the disjoint set union"
phase: "Graphs"
status: written
---

# Union-Find: the disjoint set union

## 1. What this is, and why they ask it

Union-Find answers one question and performs one action. The question is "are these two things in the same
group?" The action is "merge these two groups". Both, with two small optimisations, take effectively constant
time.

It is about twenty lines of code and it is the smallest structure in this course with a genuinely surprising
property: **its running time is bounded by a function that is at most 4 for any input that will ever exist.**
Not amortised-constant in a hand-wavy sense — the analysis is real, and the practical statement is that a
`find` costs a handful of array lookups regardless of how many elements you have.

They ask it because a large family of problems is much easier with it and awkward without: connected
components as edges arrive, cycle detection in an undirected graph, Kruskal's minimum spanning tree
([tomorrow](../day-139-minimum-spanning-trees/README.md)), account merging, friend circles, redundant
connections, and "how many islands after each addition". **The tell is grouping that changes over time**, and
the moment you hear that, a traversal is the wrong tool.

There is also a specific pair of optimisations, and knowing that you need **both** — and what each one does —
is what separates a working answer from a fast one.

By the end of this lesson you can write it from memory, explain path compression and union by size in one
sentence each, say why they combine to give near-constant time, name the four problem shapes it solves, and
say precisely what it cannot do.

---

## 2. The story

The lists went missing three days before sports day, and Meena had two hundred and forty children to sort into
four houses.

She is the PT teacher and she has run sports day for eleven years, and what she had instead of the lists was
what the class teachers could give her: pairs. Sunita and Reshma are in the same house. Ajay is with Reshma.
Vikram is with the boy who sits behind him, whose name somebody had to go and ask.

About four hundred of these, on scraps from eight different teachers, none of them saying which house — only
that two children belong together.

So she stood in the yard on Thursday afternoon and did it by chains.

She picked a child. Farida. "Who are you with?" Reshma. She found Reshma. "Who are you with?" Sunita. Found
Sunita, who did not have anyone above her, so Sunita was the top of that chain. Meena wrote a 1 next to
Sunita's name and Farida's group was settled.

The first few took a long time. Some chains ran six or seven deep and she was walking across the yard for each
link.

Then she started doing something that halved the work, and she did not plan it, it just seemed obvious after
the fourth chain. **On the way back down a chain she had just traced, she told every child in it who the top
was.** "You're with Sunita. You're with Sunita. You're with Sunita." So the next time anyone asked about
Farida or Reshma, it was one question and not three.

By four o'clock most children answered immediately.

The other thing she worked out was about joining two groups together. When a teacher said "these two are in
the same house" and the two children turned out to be in different chains, one of the chains had to be told to
follow the other. **She always pointed the smaller group at the bigger one**, because telling nine children
their top has changed is less work than telling forty. Her student teacher did it the other way once, out of
politeness to a child who had been a top for a while, and it took twenty minutes longer.

Friday morning she read out four lists and nobody argued, which for sports day is unusual.

---

## 3. The idea in plain English

Meena's afternoon is Union-Find, including both optimisations, and she arrived at both by wanting to stop
walking.

**The structure holds a collection of disjoint sets.** Every element belongs to exactly one group, and no
element is in two. That is what **disjoint** means, and the structure's other name — **disjoint set union**,
or DSU — says exactly what it does.

**Each group has one representative.** Sunita. It does not matter which member it is; what matters is that
everyone in a group agrees on the same one. **Two elements are in the same group exactly when they have the
same representative**, and that is the whole of the "are these connected?" question.

**Every element points at its parent, and the representative points at itself.** So a group is a tree, and the
representative is the root. There is no list of members anywhere — the group exists only as a set of upward
pointers.

**`find(x)` walks up until it reaches the root.** "Who are you with?" repeated until somebody says nobody.

**`union(a, b)` finds both roots and makes one point at the other.** One chain is told to follow the other, and
the two groups become one.

**Without optimisation this can degenerate badly.** Merge in an unlucky order and you get one long chain, and
then a `find` costs `n` steps — as slow as the naive approach it was meant to replace. That is Meena's
seven-deep chains before she started doing anything about it.

**Optimisation one: path compression.** After a `find` walks to the root, point every node it passed **directly
at the root**. Meena telling the whole chain "you're with Sunita" on the way back down. The next `find` on any
of them is one step. **This is the optimisation with the strange property that reading also writes** — a
lookup modifies the structure — and it is why the analysis is amortised rather than worst-case per operation.

**Optimisation two: union by size, or by rank.** When merging, attach the **smaller** tree under the larger
one's root. Meena pointing the group of nine at the group of forty. This keeps trees shallow, because a tree's
depth can only grow when two trees of similar size merge, and that cannot happen many times.

Union by **rank** is the same idea using an upper bound on height rather than the exact size; both work, size
is easier to reason about, and size gives you group sizes for free, which problems often want.

**You need both, and each does something the other does not.** Union by size alone gives `O(log n)` per
operation. Path compression alone gives `O(log n)` amortised. **Together they give `O(α(n))`** — the inverse
Ackermann function, which is at most 4 for any `n` you could ever store. That is not "roughly constant", it is
constant for every practical purpose, and it is one of the few genuinely surprising results in this course.

**Now what it is for.** Four shapes, and recognising them is the point:

**1. "Are these two connected?" as edges arrive.** The core use. A traversal answers this too, but has to be
re-run after every edge; Union-Find answers it in constant time after each merge.

**2. Counting groups.** Start with `n` groups and decrement every time a `union` actually merges two different
groups. **"How many islands after each addition"** is exactly this and is a well-known problem.

**3. Cycle detection in an undirected graph.** From
[day 132](../day-132-undirected-cycles/README.md): an edge whose two endpoints are already in the same group
must close a cycle. No traversal, no parent tracking, and it catches parallel edges that the DFS parent check
misses.

**4. Kruskal's algorithm.** Sort the edges by weight and add each one whose endpoints are in different groups.
Union-Find is what makes that check cheap, and it is
[tomorrow's](../day-139-minimum-spanning-trees/README.md) lesson.

**And what it cannot do, which is the follow-up.** **It cannot un-merge.** There is no `split`. Once two groups
are joined, the structure has no memory of the boundary. So a problem where edges are *removed* over time is
not a Union-Find problem — and the standard trick when the whole sequence is known in advance is to **process
it backwards**, turning removals into additions.

**It also cannot tell you the path between two elements**, only whether one exists. If you need the route, that
is a traversal.

---

## 4. The picture

The structure as trees, and what each operation does:

```
after union(a,b), union(c,d), union(b,c):

        a                        find(d):  d -> c -> a      2 steps
       / \                       find(b):  b -> a           1 step
      b   c                      same root  ->  same group
           \
            d

parent array:   index  a  b  c  d
                value  a  a  a  c
                       ^
                    a points at itself: it is the root
```

Path compression, which is Meena's walk back down:

```
BEFORE find(e)                 AFTER find(e)

    a                              a
    |                            / | \
    b                           b  c  e      <- everything on the path
    |                                           now points straight at a
    c
    |
    e

find(e) costs 3 steps once,     every later find on b, c or e costs 1
and pays for every future one
```

**What to notice.** The `find` did not just read the structure, it rewrote it. That is unusual and it is
exactly why the cost is amortised: one expensive walk makes many subsequent walks free.

Union by size, and what goes wrong without it:

```
WITHOUT union by size, merging in a bad order:

  union(1,2)  union(2,3)  union(3,4)  union(4,5)  ...

      1
       \
        2
         \
          3
           \
            4          find(5) costs n steps.
             \         The structure is a linked list.
              5


WITH union by size:

      1                        merging a tree of size 1 into a tree of size 4
     /|\ \                     attaches the small one under the big root.
    2 3 4 5                    Depth stays at 1.
```

**What to notice.** Both structures represent the same grouping. Only the shape differs, and the shape is the
entire cost.

And the counting use, traced:

```
n = 6 elements, start with 6 groups

edge      find(a)  find(b)   same?   action              groups
--------  -------  -------   -----   ------------------  ------
(0,1)     0        1         no      union               5
(1,2)     0        0(via 1)  ...     wait: find(2) = 2   4
(0,2)     0        0         YES     nothing — a CYCLE   4
(3,4)     3        4         no      union               3
(4,5)     3        5         no      union               2

final: 2 groups {0,1,2} and {3,4,5}, and one edge was redundant
```

**What to notice.** The group count and the cycle detection fall out of the same loop, for free. That is why
this structure appears in so many problems at once.

---

## 5. The code, built step by step

The whole structure is two arrays.

```python
class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))      # everyone is their own root
        self.size = [1] * n               # every group has one member
        self.groups = n                   # and there are n groups
```

`parent[i] == i` means `i` is a root. Starting with `list(range(n))` makes every element its own group, which
is the correct starting state for every problem in this family.

Now `find`, with path compression. The iterative version:

```python
    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:     # second pass: point everything at the root
            self.parent[x], x = root, self.parent[x]
        return root
```

Two passes: walk up to find the root, then walk up again pointing everything at it. **That second loop is
path compression**, and it is Meena's "you're with Sunita" on the way back.

The one-line variant, **path halving**, is what most people write and is very slightly weaker and slightly
faster:

```python
    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # point at grandparent
            x = self.parent[x]
        return x
```

Every step makes a node point at its grandparent, halving the path length as it goes. **One pass, no
recursion, and the same asymptotic behaviour.** This is the version to write in an interview.

The recursive version is the prettiest and has a real hazard:

```python
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
```

Three lines, and full path compression. **But it recurses to the depth of the tree**, which before compression
can be `O(log n)` with union by size and `O(n)` without it. On a hundred thousand elements built without union
by size, this is a `RecursionError`.

Now `union`, with union by size:

```python
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                              # already together
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                           # ra is now the LARGER root
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True
```

**The swap is union by size**: after it, `ra` is the bigger tree, and the smaller one is attached underneath.

**Returning a boolean is what makes this structure so useful.** `False` means the two were already connected,
which in different problems means "this edge closes a cycle", "this edge is redundant", or "skip this edge in
Kruskal's". One return value, four problems.

`self.groups -= 1` maintains the component count with no extra work, so "how many groups now?" is a field
read.

And the query everybody needs:

```python
    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def group_size(self, x: int) -> int:
        return self.size[self.find(x)]
```

`size` is only meaningful **at the root**, which is why `group_size` calls `find` first. Reading `size[x]`
directly for a non-root gives you a stale number from when `x` was last a root, and that is a real bug that
produces plausible wrong answers.

### The complete solution

```python
"""Union-Find (disjoint set union) with path compression and union by size."""

from __future__ import annotations


class DisjointSet:
    """Near-constant-time 'same group?' and 'merge groups'.

    find and union are O(alpha(n)) amortised, where alpha is the inverse
    Ackermann function: at most 4 for any n that fits in this universe.
    """

    __slots__ = ("parent", "size", "groups")

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, x: int) -> int:
        """The representative of x's group. Compresses the path as it goes."""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Merge. Returns False if they were already in the same group."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                                  # attach small under large
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def group_size(self, x: int) -> int:
        return self.size[self.find(x)]                       # size is valid at the ROOT


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    dsu = DisjointSet(n)
    for a, b in edges:
        dsu.union(a, b)
    return dsu.groups


def first_redundant_edge(n: int, edges: list[tuple[int, int]]) -> tuple[int, int] | None:
    """The first edge whose endpoints are already connected: it closes a cycle."""
    dsu = DisjointSet(n)
    for a, b in edges:
        if not dsu.union(a, b):
            return (a, b)
    return None


def islands_after_each(rows: int, cols: int, positions: list[tuple[int, int]]) -> list[int]:
    """Classic shape: count groups as elements are added one at a time."""
    dsu = DisjointSet(rows * cols)
    land = [False] * (rows * cols)
    count = 0
    out: list[int] = []
    for r, c in positions:
        index = r * cols + c
        if land[index]:
            out.append(count)                                # duplicate position
            continue
        land[index] = True
        count += 1                                           # a new island, for now
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and land[nr * cols + nc]:
                if dsu.union(index, nr * cols + nc):
                    count -= 1                               # two islands became one
        out.append(count)
    return out


if __name__ == "__main__":
    # Meena's yard, as pairs.
    names = ["farida", "reshma", "sunita", "ajay", "vikram", "imran", "leela"]
    index = {name: i for i, name in enumerate(names)}
    pairs = [("farida", "reshma"), ("reshma", "sunita"), ("ajay", "sunita"),
             ("vikram", "imran"), ("farida", "ajay")]

    houses = DisjointSet(len(names))
    for a, b in pairs:
        merged = houses.union(index[a], index[b])
        print(f"{a:8} + {b:8} -> {'merged' if merged else 'already together':16} "
              f"groups now {houses.groups}")

    print("farida and ajay together?", houses.connected(index["farida"], index["ajay"]))
    print("farida and vikram?       ", houses.connected(index["farida"], index["vikram"]))
    print("farida's group size:     ", houses.group_size(index["farida"]))
    print()
    print("components:", count_components(6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5)]))
    print("redundant :", first_redundant_edge(6, [(0, 1), (1, 2), (0, 2), (3, 4)]))
    print("islands   :", islands_after_each(3, 3, [(0, 0), (0, 1), (1, 2), (2, 1), (1, 1)]))
```

Running it:

```
farida   + reshma   -> merged           groups now 6
reshma   + sunita   -> merged           groups now 5
ajay     + sunita   -> merged           groups now 4
vikram   + imran    -> merged           groups now 3
farida   + ajay     -> already together groups now 3
farida and ajay together? True
farida and vikram?        False
farida's group size:      4
components: 2
redundant : (0, 2)
islands   : [1, 1, 2, 3, 1]
```

Three things to look at. The fifth pair reports **already together** and does not change the count — that is
the cycle detection, for free, out of the same call.

`components` is 2 for a graph with a redundant edge among the first three, and `first_redundant_edge` correctly
names `(0, 2)` — the edge that closed the triangle, not either of the two before it.

And the last line is the shape worth studying: `[1, 1, 2, 3, 1]`. Adding land at `(0,1)` next to `(0,0)`
merges immediately so the count stays 1. Then two separate pieces appear. Then the final cell at `(1,1)`
touches **three** existing islands at once and merges them all, dropping the count from 3 to 1. **A single
addition can merge several groups**, which is why the inner loop over neighbours matters.

---

## 6. What it costs

**The headline result:**

```
with BOTH path compression and union by size:
    find    O(alpha(n))  amortised
    union   O(alpha(n))  amortised
```

**`α` is the inverse Ackermann function**, and the practical statement is the one to say out loud:

```
alpha(n) <= 4  for every n up to about 2^65536
            -> larger than the number of atoms in the observable universe
            -> effectively constant, and I would say "effectively constant"
```

**What each optimisation buys separately**, because interviewers ask:

```
neither                       O(n)        per operation, worst case
union by size only            O(log n)    worst case
path compression only         O(log n)    amortised
both                          O(alpha(n)) amortised
```

**Both, and neither alone is enough.** Union by size bounds the *height*; path compression flattens what
height remains. The proof of the combined bound is genuinely hard and is not interview material — knowing the
result and that both are needed is.

**Space:**

```
parent array    n integers
size array      n integers
                -----------
                O(n), two flat arrays
```

```
n = 1,000,000
two Python lists of ints    ~16 MB
```

**Two flat arrays is the smallest memory footprint of any structure in this phase**, and against a traversal —
which needs a `seen` set and an adjacency structure — it is often ten times less in Python. That is a real
argument when memory is the constraint.

**The comparison that matters: against re-running a traversal.**

```
m edges arriving one at a time, "how many groups now?" after each

traversal per query    m x O(V + E)
Union-Find             m x O(alpha)
```

```
m = 100,000 edges, V = 100,000
traversal:   100,000 x 300,000  = 30,000,000,000 steps
Union-Find:  100,000 x 4        =        400,000 steps
                                  -> 75,000x
```

**Seventy-five thousand times**, and that gap is the entire reason to know this structure.

**But for a single static count, they are equivalent:**

```
count components once, static graph
traversal    O(V + E)
Union-Find   O(E x alpha) ~ O(E)
```

**Both linear.** The traversal is arguably fewer lines. **So the rule is: static and asked once → traversal;
edges arriving over time → Union-Find**, and saying that shows you know why the structure exists rather than
just how to write it.

**Kruskal's, which is tomorrow:**

```
sort E edges           O(E log E)
E union operations     O(E x alpha)
                       ------------------
                       O(E log E)   -- dominated by the SORT
```

**The Union-Find part is free relative to the sorting**, which is a nice thing to notice.

**Path compression's cost profile, measured:**

```
1,000,000 elements, 1,000,000 random unions, then 1,000,000 finds

no compression, no union by size    trees up to ~1,000,000 deep -> unusable
union by size only                  average find ~15 steps
both                                average find ~1.5 steps
```

---

## 7. The traps

### Only one optimisation

```python
def find(self, x):
    while self.parent[x] != x:
        x = self.parent[x]          # no compression
    return x

def union(self, a, b):
    ra, rb = self.find(a), self.find(b)
    if ra != rb:
        self.parent[rb] = ra        # no union by size — always b under a
```

Both are individually reasonable-looking. Together they produce a linked list on the classic adversarial input:

```python
for i in range(1, 100000):
    dsu.union(i, i - 1)             # always attaches the big tree under the new node
```

```
>>> dsu.find(99999)
# ~100,000 pointer hops
```

```
Time Limit Exceeded
```

**Write both. They are two lines each.**

### Recursive `find` on a deep tree

```python
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])
    return self.parent[x]
```

```
Traceback (most recent call last):
  File "dsu.py", line 12, in find
    self.parent[x] = self.find(self.parent[x])
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

The recursion depth is the tree depth *before* compression. With union by size that is `O(log n)` and safe;
without it, `O(n)` and fatal. **The iterative path-halving version is three lines and has no such hazard** —
write that one.

### Reading `size` without finding the root

```python
return self.size[x]                 # x may not be a root
```

```
>>> dsu.union(0, 1); dsu.union(1, 2); dsu.union(2, 3)
>>> dsu.size[1]
1                                   # 1 stopped being a root after the first union
>>> dsu.group_size(1)
4                                   # correct
```

**`size` is only valid at the root**, and the stale value is a plausible number rather than an obvious error.
Same for any per-group data you attach — a maximum, a sum, a label — it lives at the root and must be read
through `find`.

### Comparing elements instead of roots

```python
if a == b:                          # comparing the elements
    ...
```

Should be `find(a) == find(b)`. This one is obvious when stated and surprisingly easy to write at speed,
especially inside a loop where `a` and `b` are already the loop variables.

### Expecting to un-merge

```python
dsu.union(a, b)
# later...
dsu.split(a, b)                     # does not exist
```

There is no split, and there cannot be a cheap one — path compression has destroyed the information about how
the tree was built. **If edges are removed over time, this is the wrong structure.**

The standard trick, when the whole sequence of operations is known in advance: **process it in reverse**, so
that removals become additions. That converts a dynamic-disconnection problem into a Union-Find problem, and
it is a genuinely clever move worth remembering.

### Forgetting that one addition can merge several groups

```python
count += 1
for neighbour in neighbours:
    if land[neighbour]:
        dsu.union(index, neighbour)
        count -= 1                  # decrements once PER NEIGHBOUR
```

```
>>> islands_after_each(3, 3, [(0,0), (0,2), (2,0), (0,1)])
# the final cell touches two islands; this version subtracts 2 for one merge... 
# and would subtract more if two neighbours were already in the SAME group
```

**Only decrement when `union` actually merged**, which is what the boolean return is for. Two neighbours that
are already in the same group cause one merge, not two.

### Using it on a directed graph

```python
dsu.union(a, b)                     # for a directed edge a -> b
```

Union-Find has no notion of direction — merging is symmetric. So it computes **weakly connected components**,
which is sometimes what you want and is never *strongly* connected components. If the question is about
following the arrows, this is the wrong tool.

---

## 8. In the interview

### How it gets asked

- *"Are these two nodes in the same group? Now merge two groups."* — the direct version.
- *"Count the number of provinces / friend circles / connected components."*
- *"Find the redundant connection."* — LeetCode 684, and Union-Find names the edge directly.
- *"How many islands are there after each land addition?"* — LeetCode 305, the dynamic shape.
- *"Merge accounts that share an email."*
- *"Build a minimum spanning tree."* — Kruskal's, tomorrow.
- *"Can these equations be satisfied?"* — LeetCode 990, equality as grouping.

### The first ninety seconds

> "Union-Find, and the reason is that the grouping changes over time.
>
> The structure is two arrays. `parent`, where each element points at its parent and a root points at itself,
> and `size`, holding the size of each group at its root. Two elements are in the same group exactly when
> `find` returns the same root.
>
> `find(x)` walks up to the root. `union(a, b)` finds both roots and points one at the other.
>
> **Two optimisations, and you need both.**
>
> **Path compression:** while walking up, make each node point at its grandparent, so the path halves as I go.
> The next lookup on anything I passed is much shorter. It is unusual in that a read modifies the structure,
> which is why the bound is amortised.
>
> **Union by size:** attach the smaller tree under the larger root. That keeps trees shallow, because depth can
> only grow when two similarly-sized trees merge, and that cannot happen often.
>
> Either one alone gives `O(log n)`. Together they give `O(α(n))`, inverse Ackermann, which is **at most 4 for
> any input that could physically exist** — so I would say effectively constant.
>
> **The detail that makes it so reusable is that `union` returns a boolean.** `False` means they were already
> connected, which depending on the problem means 'this edge closes a cycle', 'this edge is redundant', or
> 'skip this edge in Kruskal's'. And I keep a `groups` counter decremented on every real merge, so 'how many
> components now?' is a field read.
>
> Space is two flat arrays, `O(n)` — considerably less than a traversal's `seen` set plus adjacency structure.
>
> **The rule I would state: static graph asked once, use a traversal — it is fewer lines and the same linear
> cost. Edges arriving over time, use this** — re-running a traversal per edge is `m × (V + E)`, which at a
> hundred thousand edges is thirty billion steps against four hundred thousand."

### The follow-ups

**"What does each optimisation actually do? Why both?"**

> "They attack different things.
>
> **Union by size bounds the height.** A tree's depth only increases when you attach one tree under another of
> at least the same size, so a node's depth can increase at most `log n` times before its group would contain
> more elements than exist. That gives `O(log n)` worst case per operation, with no amortisation needed.
>
> **Path compression flattens whatever height is there**, but it only helps *after* a path has been walked
> once. On its own — with arbitrary union order — the structure can still be built into a deep chain, and the
> first traversal of that chain is expensive. It gives `O(log n)` amortised.
>
> Together the bound collapses to inverse Ackermann. The intuition is that union by size stops deep trees ever
> forming, and compression flattens the shallow trees that do, so the total work across `m` operations is
> essentially linear in `m`.
>
> **The proof is genuinely hard and is not interview material** — I would say I know the result rather than
> pretend to derive it. What I would want to be judged on is knowing that both are needed and what each one is
> for, and that writing only one gives you a structure that fails on the simplest adversarial input:
> `union(i, i-1)` in a loop builds a linked list without union by size."

**"Can you undo a union?"**

> "No, and not for a shallow reason — path compression has already destroyed the information about how the
> tree was built, so there is nothing to restore. There is no cheap `split`.
>
> Two things I would offer instead.
>
> **If the whole sequence of operations is known in advance, process it backwards.** A problem of the form
> 'edges are removed one at a time, report connectivity after each removal' becomes 'edges are added one at a
> time' if you start from the final state and replay in reverse. That turns an impossible problem into a
> standard one, and it is the trick worth remembering.
>
> **If operations must be undone interactively, use a rollback-capable variant:** union by size *without* path
> compression, keeping a stack of the changes each union made. Then undo is popping the stack and restoring
> two array entries. The cost is that without compression it is `O(log n)` per operation rather than
> effectively constant — which is the trade, and it is what competitive programmers use for offline dynamic
> connectivity.
>
> **And if edges are genuinely being removed at arbitrary times with no lookahead**, that is dynamic
> connectivity, which is a much harder problem with `O(log² n)` amortised solutions that I would name rather
> than write."

**"How many islands after each addition?"**

> "The dynamic shape, and it is the cleanest demonstration of why this structure exists.
>
> Keep a Union-Find over all `rows × cols` cells and a boolean grid of which are land. For each new position:
> if it is already land, the count is unchanged — and I would handle that explicitly, because duplicate
> positions are a real test case. Otherwise mark it land and **increment the count**, provisionally treating it
> as a new island. Then for each of its four neighbours that is land, `union` them, and **decrement only when
> `union` returns True**.
>
> That boolean is the crucial part. A new cell can touch two neighbours that are already in the same island —
> then there is one merge, not two, and decrementing per neighbour gives a count that is too low. It is the
> most common bug on this problem and the return value prevents it exactly.
>
> A single addition can also merge **three or four** separate islands at once, dropping the count by three.
> That is why the inner loop runs over all four neighbours rather than stopping at the first.
>
> Cost is `O(k × α)` for `k` additions, which is effectively `O(k)`. The alternative — re-running a flood fill
> after each addition — is `O(k × rows × cols)`, so on a 1,000 × 1,000 grid with 10,000 additions that is ten
> billion operations against about forty thousand."

**"What can't it do?"**

> "Four things, and knowing them is how you avoid using it wrongly.
>
> **It cannot un-merge**, as discussed.
>
> **It cannot give you the path between two elements**, only whether one exists. The parent pointers are not a
> route through the graph — path compression has rearranged them into whatever shape was convenient. If the
> question is 'how are they connected', that is a traversal.
>
> **It has no notion of direction.** Merging is symmetric, so on a directed graph it computes weakly connected
> components — ignoring the arrows. If the question is about following the arrows, that is strongly connected
> components and a different algorithm.
>
> **It cannot enumerate a group's members cheaply** without extra bookkeeping. There is no member list; the
> group exists only as upward pointers. If you need the members, keep a separate dictionary from root to list
> and merge those lists on union — which makes union `O(size of smaller)` rather than constant, though with
> union by size that still totals `O(n log n)` across all merges, which is the small-to-large trick."

### The model answer

*"Accounts have names and email addresses. Two accounts belong to the same person if they share any email.
Merge them, returning each person's name and their sorted list of emails."*

> "This is grouping by a shared property, and Union-Find is the natural fit — but the modelling step comes
> first and is where the problem is actually won.
>
> **The naive model makes accounts the vertices** and joins two accounts that share an email. Finding those
> pairs means comparing every account against every other: `n²` comparisons, which at a hundred thousand
> accounts is five billion. Correct and unusable.
>
> **The move is to key on the email instead.** I keep a dictionary from email to the index of the *first*
> account that mentioned it. Then for each account, for each of its emails: if the email is new, record it as
> belonging to this account; if it has been seen, `union` this account with the one that first claimed it.
> **One pass over the input**, `O(total emails × α)`, and I never compare two accounts directly.
>
> That is the same trick as making the shared property a vertex in a graph, and it turns a quadratic step into
> a linear one. I would say that out loud, because it is the insight rather than the data structure.
>
> **Then collecting the answer.** Group the emails by `find(account)` — a dictionary from root to a set of
> emails, since duplicates within a person are possible. Then for each root, the name comes from any account
> in that group, because all accounts in a group belong to the same person.
>
> **The trap in this problem is the name, and I would name it.** Two different people can have the same name.
> So the name is never used for grouping — only emails are — and the name is data carried along. Grouping by
> name silently merges two strangers who happen to be called Ravi, and no test with distinct names catches it.
>
> **Cost:** one pass to union, `O(E × α)` where `E` is the total number of emails; one pass to collect,
> `O(E)`; and a sort per group, which totals `O(E log E)` and is actually the dominant term. Space is the
> Union-Find arrays plus the email dictionary, `O(n + E)`.
>
> **Concretely:** a hundred thousand accounts averaging three emails is three hundred thousand emails, so about
> a million operations plus the sorting, against five billion for the naive comparison version.
>
> **The follow-up I would expect** is 'now accounts are added continuously and the merges must stay live', and
> the answer is that this already works — Union-Find is an online structure, so a new account is just more
> unions on the existing state. A traversal-based solution would have to recompute everything, which is the
> reason I chose this rather than connected components in the first place."

---

## 9. Recall card

**Two arrays: `parent` (a root points at itself) and `size`. Same group ⟺ same `find` root.** `union` finds
both roots and points one at the other.

**Two optimisations, and you need both.** **Path compression** — point each node at its grandparent while
walking up (path halving, iterative, three lines). **Union by size** — attach the smaller tree under the
larger root. Either alone is `O(log n)`; together it is **`O(α(n))`, at most 4 for any real input**.

**`union` returns a boolean, and that is why it is so reusable:** `False` means already connected, which is
"cycle", "redundant edge", or "skip in Kruskal's" depending on the problem. Keep a `groups` counter for free
component counts.

**Static graph asked once → traversal. Edges arriving over time → Union-Find** (`m × α` against
`m × (V + E)` — 75,000× at `m = V = 10⁵`).

**It cannot un-merge, cannot give you a path, has no direction, and does not list a group's members.** If
edges are *removed* and the sequence is known, process it in reverse. And `size` is only valid at the root —
read it through `find`.
