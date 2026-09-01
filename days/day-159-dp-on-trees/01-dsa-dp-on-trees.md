---
day: 159
track: dsa
title: "DP on trees"
phase: "Dynamic programming"
status: written
---

# DP on trees

## 1. What this is, and why they ask it

**Tree DP is dynamic programming where the subproblems are subtrees**, and the answer for a node is computed
from the answers for its children.

Every DP so far has had a table you filled with loops. **Here there is no table and there are no loops** — the
recursion *is* the fill order, because a post-order traversal visits every child before its parent, which is
exactly the dependency direction. **You get the hardest part of DP for free, from the shape of the data.**

They ask it because **it is where two topics you already know join up.** You have done trees since day 100 and
DP since day 143, and tree DP is the point at which "solve the subproblems first" and "recurse into the
children first" turn out to be the same instruction. **A candidate who sees that connection explains tree DP
in one sentence; a candidate who does not treats every tree problem as a new puzzle.**

The other reason is a specific, recurring difficulty: **the answer at a node is often not the value you return
to its parent.** In the diameter problem, the longest path through a node uses two of its children, but the
value the parent needs is a path going down through only one. **Two different quantities, computed in the same
function** — and confusing them is the defining bug of the topic.

By the end of this lesson you can write the post-order pattern, handle the include/exclude state, compute
diameters and path sums, explain the return-versus-record distinction, and say what recursion depth costs.

---

## 2. The story

The land had been divided four times in eighty years and the family that farmed it had a problem that took an
afternoon and a very patient uncle to solve.

**Every plot had been split among the sons, and their plots split again**, so the whole holding was a shape
like a tree — the original field at the top, and below it the divisions, and below those the divisions of
those.

And now the government was offering a payment for planting a particular kind of tree, **with one condition:
you could not take the payment for a plot and also for the plot it had been split off from.** Parent or child,
not both.

**The family wanted the largest total payment.**

The eldest brother started at the top, on the original field, because it was the biggest and it seemed
obvious.

The uncle stopped him.

**"You cannot know about the top until you know about everything under it."**

So they started at the bottom instead — **the smallest plots, the ones with nothing below them.**

For each of those the answer was easy. **Take the payment. There is nothing under you to lose.**

Then one level up. And here the uncle made them write down two numbers for every plot instead of one, which
the brother thought was a waste of paper until he saw why.

**"For each plot, write down the best total if you take this plot's payment, and the best total if you do
not."**

Because if you take it, you cannot take any of the plots immediately below — **so the total is this payment
plus, for each child, the best it can do while not taking its own.**

And if you do not take it, **each child is free to do whatever is best for it** — take or not, whichever is
larger.

**Two numbers per plot, computed from the two numbers of each of its children.** They went up the tree that
way, level by level, and by evening they had the answer for the original field at the top.

The brother's question, at the end, was the good one.

**"Why two numbers? Why not just the best?"**

**"Because your father cannot use your best,"** the uncle said. **"He can only use your best-without-you. If
you only wrote down one number he would not know which kind it was."**

---

## 3. The idea in plain English

The uncle's two numbers are the state, and his last sentence is the whole lesson.

**Start with the shape, because it is what makes tree DP easy.**

**A subtree is a subproblem.** The answer for a node depends on the answers for its children, and nothing
else — **so the dependency graph is the tree itself, pointing upwards.**

**And post-order traversal visits every child before its parent.** So:

```python
def solve(node):
    if node is None:
        return base_case
    left = solve(node.left)                   # children first
    right = solve(node.right)
    return combine(node, left, right)         # then this node
```

**That is the entire pattern.** There is no table to allocate and **no fill order to get wrong**, because the
recursion enforces it. After the last four days, that is worth pausing on: **the hardest mechanical part of DP
disappears when the data is a tree.**

**Now the state, and it is usually not a single number.**

**House robber on a tree** — the uncle's problem — is the canonical example. You cannot take a node and its
child. **The state per node is a pair:**

```
(best if I TAKE this node, best if I SKIP this node)
```

**If you take it:** `value + sum over children of (child's skip value)`.
**If you skip it:** `sum over children of max(child's take, child's skip)`.

**The answer at the root is `max(take, skip)`.**

**Why two numbers rather than one is the uncle's point**: a parent that takes itself needs its child's
*skip* value specifically, and a single "best" would not say which case produced it. **The extra dimension
exists because the parent's options depend on the child's choice, not only on its score.**

**That is exactly the mode dimension from [day 157](../day-157-stock-dp/README.md)**, in a different shape.

**Now the second idea, which is where the bugs live.**

**In many tree problems, the answer you record is different from the value you return.**

**Diameter of a tree** — the longest path between any two nodes — is the clearest case. Consider a node:

- **The longest path *through* this node** goes down one side, up through the node, and down the other. That is
  `left_depth + right_depth`. **That is a candidate for the answer.**
- **The value the parent needs** is the longest path going *down* from this node, which can use only one side:
  `1 + max(left_depth, right_depth)`. **A path cannot go down the left, come back up, and then continue up to
  the parent** — it would visit this node twice.

**So the function returns one thing and records another.**

```python
best = 0                                      # recorded, in an outer variable

def depth(node):
    nonlocal best
    if node is None:
        return 0
    left, right = depth(node.left), depth(node.right)
    best = max(best, left + right)            # RECORD: path THROUGH here
    return 1 + max(left, right)               # RETURN: path DOWN from here
```

**Returning `left + right` instead is the defining bug of tree DP.** It compiles, it runs, and it produces a
number that is too large — because it lets a path fork at a node and still continue upwards, which is not a
path.

**Say the two sentences out loud as you write them:** "I record the best path through this node; I return the
best path down from this node."

**Maximum path sum** — LeetCode 124 — is the same structure with two extra details. **Negative values mean a
branch can be worth skipping**, so clamp each child's contribution at zero: `max(0, child)`. **And the path
need not touch the root**, which is why the answer is recorded rather than returned.

**Now the third idea: rerooting, which is the step up.**

Some problems ask for an answer *at every node*, not just at the root. **"For each node, the sum of distances
to all other nodes."**

**The naive approach runs the whole traversal from each node: `O(n²)`.** For a tree with 30,000 nodes that is
900 million operations.

**The rerooting technique does it in `O(n)` with two passes.** The first is an ordinary post-order pass
computing, for each node, the answer *within its own subtree*. **The second is a pre-order pass pushing
information down** — at each child, the answer for the whole tree can be computed from the parent's answer
plus what changes when you move the root across that one edge.

**The insight is that moving the root by one edge changes the answer in a way you can compute in constant
time**, so you never recompute from scratch.

**It is genuinely harder than everything else here**, and the right level of preparation is to **know it exists,
know the two-pass shape, and be able to say what the second pass does.**

**Finally: the practical thing that bites in Python.**

**Recursion depth.** A tree with 10,000 nodes in a line — a degenerate tree, which is just a linked list — is
10,000 stack frames. **Python's default limit is 1,000**, so it raises `RecursionError` on inputs a real test
suite will contain.

**Two answers.** `sys.setrecursionlimit(200000)` is the quick one, and it can segfault because the C stack is
also finite. **The robust answer is an explicit stack**, which is more code and always works. **Say which you
are doing and why**, because an interviewer with a 10⁵-node constraint is testing exactly this.

---

## 4. The picture

The post-order pattern, and why it is the fill order:

```
            A
           / \
          B   C
         / \
        D   E

  post-order visit sequence:  D, E, B, C, A

  D and E finish before B needs them.
  B and C finish before A needs them.

  -> the traversal order IS the dependency order
  -> no table, no loops, no fill order to get wrong

  Compare interval DP, where getting the fill order right was
  the whole difficulty. Here the data structure does it.
```

The uncle's two numbers, on a small tree:

```
  values on the nodes:

            3
           / \
          2   3
           \    \
            3    1

  leaf 3 (left):  take = 3,  skip = 0
  leaf 1 (right): take = 1,  skip = 0

  node 2:  take = 2 + (child's SKIP = 0)          = 2
           skip = max(child take, child skip) = 3 = 3
           -> (2, 3)

  node 3 (right): take = 3 + 0 = 3
                  skip = max(1, 0) = 1
                  -> (3, 1)

  root 3:  take = 3 + left.skip + right.skip = 3 + 3 + 1 = 7
           skip = max(2,3) + max(3,1)        = 3 + 3     = 6
           -> answer max(7, 6) = 7

  THE PARENT NEEDS THE CHILD'S "SKIP" SPECIFICALLY.
  A single "best" number would not say which case produced it.
```

The record-versus-return distinction, which is the defining bug:

```
            A
           / \
          B   C
         /     \
        D       E

  at node A:

  PATH THROUGH A:  D - B - A - C - E        length = left_depth + right_depth
                   ^^^^^^^^^^^^^^^^^        <- RECORD this as a candidate

  PATH DOWN FROM A (what A's parent can use):
                   A - B - D                 = 1 + max(left, right)
                   ^^^^^^^^^^                <- RETURN this

  WHY they differ: a path that goes down the left, back up through A,
  and down the right CANNOT then continue up to A's parent —
  it would pass through A twice.

  Returning left + right instead:
     no error, and every ancestor's number is too large.
```

Maximum path sum, and where the clamp goes:

```
  values:
            -10
            /  \
           9    20
               /  \
              15   7

  at node 20:  left = 15, right = 7
               record: 20 + 15 + 7 = 42          <- the answer
               return: 20 + max(15, 7) = 35

  at node -10: left = 9, right = 35
               record: -10 + 9 + 35 = 34
               return: -10 + max(9, 35) = 25

  answer = max(42, 34, ...) = 42

  THE CLAMP: if a child's contribution is NEGATIVE, use 0 instead —
  the path simply does not go that way.
     node with value 5, left child contributing -3:
        without clamp: 5 + (-3) = 2
        with clamp:    5 + 0    = 5     <- correct: skip that branch
```

Rerooting, in outline:

```
  question: for EVERY node, the sum of distances to all others

  NAIVE: run a traversal from each node          O(n^2)
         n = 30,000 -> 900,000,000 operations

  REROOTING, two passes, O(n):

  PASS 1 (post-order, upwards):
     count[v]  = nodes in v's subtree
     within[v] = sum of distances from v to its own subtree

  PASS 2 (pre-order, downwards):
     answer[root] = within[root]
     moving the root from u to its child v:
        - every node IN v's subtree gets 1 CLOSER   (count[v] nodes)
        - every node NOT in v's subtree gets 1 FURTHER  (n - count[v])

     answer[v] = answer[u] - count[v] + (n - count[v])

  ONE SUBTRACTION per edge. That is the whole technique.
```

---

## 5. The code, built step by step

### The pattern, which every tree DP shares

```python
def tree_dp(node):
    if node is None:
        return base_case                      # the empty subtree
    left = tree_dp(node.left)                 # children FIRST
    right = tree_dp(node.right)
    return combine(node.value, left, right)   # then this node
```

**Write this before anything else.** The only decisions are what the base case is and what `combine` does, and
**the fill order is handled by the call stack.**

### House robber on a tree

```python
def rob_tree(root) -> int:
    def solve(node) -> tuple[int, int]:
        """Returns (best if we TAKE this node, best if we SKIP it)."""
        if node is None:
            return 0, 0
        left_take, left_skip = solve(node.left)
        right_take, right_skip = solve(node.right)

        take = node.value + left_skip + right_skip        # children must skip
        skip = max(left_take, left_skip) + max(right_take, right_skip)
        return take, skip

    return max(solve(root))
```

**Returning a tuple is the state.** The parent's `take` branch reads only the children's `skip` values —
**which is precisely why one number would not be enough.**

**`max(solve(root))` at the end**, because the root itself may or may not be taken.

### Diameter, with the record-versus-return split

```python
def diameter(root) -> int:
    best = 0

    def depth(node) -> int:
        nonlocal best
        if node is None:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        best = max(best, left + right)        # RECORD: the path THROUGH here
        return 1 + max(left, right)           # RETURN: the path DOWN from here

    depth(root)
    return best
```

**Two different quantities, three lines apart**, and the comments are not decoration — **they are what stops
you returning the wrong one.**

**`nonlocal best` rather than returning a pair** is a style choice; the pair version is equally correct and
slightly more verbose.

### Maximum path sum

```python
def max_path_sum(root) -> int:
    best = float("-inf")

    def gain(node) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))        # CLAMP: skip a negative branch
        right = max(0, gain(node.right))
        best = max(best, node.value + left + right)       # record
        return node.value + max(left, right)              # return

    gain(root)
    return int(best)
```

**The `max(0, ...)` is the one line that handles negative values**, and forgetting it makes the answer too
small on any tree with negatives — **because the path is forced through branches it should avoid.**

**`best` starts at negative infinity**, not zero: **a tree of all-negative values has a negative answer**, and
zero would win every comparison.

### Counting and summing over subtrees

```python
def subtree_sums(root) -> dict:
    sums = {}

    def total(node) -> int:
        if node is None:
            return 0
        s = node.value + total(node.left) + total(node.right)
        sums[node] = s
        return s

    total(root)
    return sums
```

**The simplest possible tree DP**, and worth writing once because so many problems reduce to it — most
frequently-asked-subtree-sum problems are this plus a `Counter`.

### Rerooting: sum of distances to every node

```python
def sum_of_distances(n: int, edges: list[tuple[int, int]]) -> list[int]:
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    count = [1] * n                           # nodes in each subtree
    within = [0] * n                          # distance sum within each subtree

    def pass_one(node: int, parent: int) -> None:
        for child in graph[node]:
            if child != parent:
                pass_one(child, node)
                count[node] += count[child]
                within[node] += within[child] + count[child]

    def pass_two(node: int, parent: int, answer: list[int]) -> None:
        for child in graph[node]:
            if child != parent:
                # move the root across one edge:
                #   count[child] nodes get closer, n - count[child] get further
                answer[child] = answer[node] - count[child] + (n - count[child])
                pass_two(child, node, answer)

    pass_one(0, -1)
    answer = [0] * n
    answer[0] = within[0]
    pass_two(0, -1, answer)
    return answer
```

**`within[node] += within[child] + count[child]`** is the first pass's key line: every node in the child's
subtree is one edge further from `node` than it was from `child`, and there are `count[child]` of them.

**`answer[child] = answer[node] - count[child] + (n - count[child])`** is the whole rerooting insight in one
line — **and it is why this is `O(n)` and not `O(n²)`.**

### The iterative version, for deep trees

```python
def diameter_iterative(root) -> int:
    if root is None:
        return 0
    best = 0
    depths = {None: 0}
    stack = [(root, False)]                   # (node, children_processed)
    while stack:
        node, processed = stack.pop()
        if processed:
            left, right = depths[node.left], depths[node.right]
            best = max(best, left + right)
            depths[node] = 1 + max(left, right)
        else:
            stack.append((node, True))        # revisit AFTER the children
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return best
```

**The `(node, processed)` flag is how you get post-order from an explicit stack**: push the node back marked
as processed, then push its children, so the children are popped first.

**This is what you write when the tree can be 100,000 deep**, and knowing the pattern is worth more than
`setrecursionlimit`.

### The complete solution

```python
"""DP on trees: the pattern, the state, and the record/return distinction."""

from dataclasses import dataclass


@dataclass(eq=False)                          # eq=False keeps Node hashable
class Node:
    value: int
    left: "Node | None" = None
    right: "Node | None" = None


def rob_tree(root: Node | None) -> int:
    """Cannot take a node and its child. State = (take, skip)."""
    def solve(node: Node | None) -> tuple[int, int]:
        if node is None:
            return 0, 0
        left_take, left_skip = solve(node.left)
        right_take, right_skip = solve(node.right)
        take = node.value + left_skip + right_skip     # children must SKIP
        skip = max(left_take, left_skip) + max(right_take, right_skip)
        return take, skip

    return max(solve(root))


def diameter(root: Node | None) -> int:
    """Longest path between any two nodes, counted in edges."""
    best = 0

    def depth(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right)        # RECORD: path THROUGH this node
        return 1 + max(left, right)           # RETURN: path DOWN from it

    depth(root)
    return best


def max_path_sum(root: Node | None) -> int:
    """Any node to any node. Negative branches are clamped away."""
    best = float("-inf")

    def gain(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))        # a negative branch is skipped
        right = max(0, gain(node.right))
        best = max(best, node.value + left + right)
        return node.value + max(left, right)

    gain(root)
    return int(best)


def height(root: Node | None) -> int:
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def count_nodes(root: Node | None) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def diameter_iterative(root: Node | None) -> int:
    """No recursion. For trees deeper than the stack limit."""
    if root is None:
        return 0
    best = 0
    depths: dict = {None: 0}
    stack: list[tuple[Node, bool]] = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if processed:
            left, right = depths[node.left], depths[node.right]
            best = max(best, left + right)
            depths[node] = 1 + max(left, right)
        else:
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return best


def sum_of_distances(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """For every node, the sum of distances to all others. Rerooting: O(n)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    count = [1] * n
    within = [0] * n

    def pass_one(node: int, parent: int) -> None:
        for child in graph[node]:
            if child != parent:
                pass_one(child, node)
                count[node] += count[child]
                within[node] += within[child] + count[child]

    def pass_two(node: int, parent: int, answer: list[int]) -> None:
        for child in graph[node]:
            if child != parent:
                answer[child] = answer[node] - count[child] + (n - count[child])
                pass_two(child, node, answer)

    pass_one(0, -1)
    answer = [0] * n
    answer[0] = within[0]
    pass_two(0, -1, answer)
    return answer


def build_line(depth: int) -> Node:
    """A degenerate tree: n nodes in a straight line."""
    root = Node(1)
    current = root
    for _ in range(depth - 1):
        current.left = Node(1)
        current = current.left
    return root


if __name__ == "__main__":
    #        3
    #       / \
    #      2   3
    #       \    \
    #        3    1
    tree = Node(3, Node(2, None, Node(3)), Node(3, None, Node(1)))
    print("rob tree        :", rob_tree(tree))
    print("height          :", height(tree))
    print("node count      :", count_nodes(tree))

    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    d = Node(1, Node(2, Node(4), Node(5)), Node(3))
    print("diameter        :", diameter(d))
    print("iterative agrees:", diameter_iterative(d))

    #      -10
    #      /  \
    #     9    20
    #         /  \
    #        15   7
    p = Node(-10, Node(9), Node(20, Node(15), Node(7)))
    print("max path sum    :", max_path_sum(p))
    print("all negative    :", max_path_sum(Node(-3, Node(-2), Node(-5))))

    edges = [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)]
    print("sum of distances:", sum_of_distances(6, edges))

    line = build_line(2000)
    try:
        print("deep recursive  :", diameter(line))
    except RecursionError as e:
        print("deep recursive  : RecursionError:", e)
    print("deep iterative  :", diameter_iterative(line))
```

Run it and you get:

```
rob tree        : 7
height          : 3
node count      : 5
diameter        : 3
iterative agrees: 3
max path sum    : 42
all negative    : -2
sum of distances: [8, 12, 6, 10, 10, 10]
deep recursive  : RecursionError: maximum recursion depth exceeded
deep iterative  : 1999
```

**The last two lines are the practical lesson**, and it is worth running yourself: **a two-thousand-node line
kills the recursive version and the iterative one handles it.** That is not a hypothetical — a linked-list
shaped tree is a standard test case.

**And `all negative : -2`** shows the clamp working correctly: the best path is the single node `-2`, not the
sum of anything.

---

## 6. What it costs

**Time: every node is visited once.**

```
one post-order traversal          O(n)
constant work per node            O(1)
-> O(n) total

n = 100,000 nodes: ~100,000 operations. Milliseconds.
```

**That is dramatically better than the table DPs of the last week**, and worth saying: **tree DP is linear
because the tree already encodes which subproblems exist.** There are exactly `n` subtrees, so there are
exactly `n` subproblems.

**Space: the recursion stack.**

```
balanced tree of n nodes:      depth ~ log2(n)
                               n = 1,000,000 -> depth ~20
                               -> negligible

degenerate tree (a line):      depth = n
                               n = 100,000 -> 100,000 frames
                               -> ~10-50 MB of stack, and Python
                                  raises long before that
```

**The gap between those two is the whole practical story**, and the constraint in the problem tells you which
you must survive.

**Python's recursion limit, concretely:**

```
>>> sys.getrecursionlimit()
1000

so ~1,000 nested calls, minus whatever frames are already used.
A line-shaped tree of 2,000 nodes fails.

sys.setrecursionlimit(200000):
  works up to the C stack limit, then SEGFAULTS rather than raising
  -> not safe for arbitrary depth

explicit stack:
  heap-allocated, so bounded only by memory
  -> 100,000 frames as tuples: ~10 MB. Fine.
```

**Rerooting, and why it is worth the complexity:**

```
naive, one traversal per node:    n x O(n) = O(n^2)
  n = 30,000  ->  900,000,000 operations  ~3 minutes in Python

rerooting, two traversals:        O(n)
  n = 30,000  ->  60,000 operations       ~0.02 s

15,000x faster, and LeetCode 834 caps n at 30,000 specifically
so that the quadratic version does not pass.
```

**The two-pass structure costs:**

```
pass 1 (post-order):   O(n), two arrays of size n
pass 2 (pre-order):    O(n), one more array
-> O(n) time, O(n) space, and ~3 arrays instead of 1
```

**Comparison with the table DPs this week:**

```
                    time        space       fill order
  grid DP           O(rows x cols)  O(cols)   loops, easy to get right
  interval DP       O(n^3)          O(n^2)    loops, easy to get WRONG
  tree DP           O(n)            O(depth)  FREE — the recursion does it

Tree DP is the cheapest shape in the family, and the fill order —
which was the whole difficulty of interval DP — costs nothing.
```

**The tuple-returning versions, on cost:**

```
returning (take, skip) allocates a tuple per node
  n = 100,000 -> 100,000 small tuples
  ~50 bytes each = 5 MB, all garbage-collected as you unwind

negligible, and much clearer than threading two nonlocal variables.
Prefer the tuple.
```

---

## 7. The traps

**Returning the recorded value instead of the returnable one.**

```python
>>> def bad_depth(node):
...     if node is None:
...         return 0
...     left, right = bad_depth(node.left), bad_depth(node.right)
...     return left + right + 1               # WRONG: this is a fork, not a path
>>> # on a balanced tree of 7 nodes this returns 7, not 3
```

**It returns the node count, not the depth**, because every ancestor adds both branches. **No error, and a
number that grows with the tree** — so it looks plausible on a small test.

**The rule is two sentences, and saying them prevents this:** *I record the best path through this node; I
return the best path down from this node.*

**Forgetting the clamp on negative values.**

```python
>>> tree = Node(2, Node(-5), Node(-3))
>>> # without max(0, ...):
>>> #   best = 2 + (-5) + (-3) = -6
>>> # with the clamp:
>>> #   best = 2 + 0 + 0 = 2
>>> max_path_sum(tree)
2
```

**Without the clamp the path is forced through branches that lose money**, and the answer is too small. **The
clamp says "this path simply does not go that way."**

**Initialising `best` to zero in max path sum.**

```python
>>> max_path_sum(Node(-3, Node(-2), Node(-5)))
-2
```

**Correct.** With `best = 0` it would return `0`, **which is not the value of any path** — an all-negative tree
has a negative answer, and zero corresponds to the empty path, which is not allowed.

**One number where two are needed.**

```python
>>> # rob_tree returning just max(take, skip):
>>> #   the parent cannot tell whether that best USED the child
>>> #   -> it may take itself AND count a child that was taken
>>> #   -> an answer that is too LARGE, silently
```

**The uncle's point exactly.** **When the parent's options depend on the child's choice and not only its
score, the state needs a dimension for that choice.**

**Recursion depth on a degenerate tree.**

```python
>>> line = build_line(2000)
>>> diameter(line)
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

**A tree that is a straight line is a valid tree** — and it is the shape a sorted insert sequence produces, so
it appears in real test suites. **The constraint `n <= 10^5` is a direct instruction to handle it.**

**`sys.setrecursionlimit` as the fix.**

```python
>>> sys.setrecursionlimit(200000)
>>> diameter(build_line(150000))
Segmentation fault
```

**It raises the Python limit and not the C stack limit**, so a deep enough tree crashes the interpreter
instead of raising. **A segfault is worse than an exception**, and an explicit stack is the answer when the
depth is genuinely unbounded.

**Mutating shared state across branches.**

```python
>>> def bad(node, path=[]):                   # mutable default argument
...     path.append(node.value)
...     ...
```

**The list persists between calls and accumulates across siblings.** In tree DP specifically, **anything
passed down must be copied or undone on the way back up** — append before the recursive call, pop after.

**Treating a graph as a tree.**

```python
>>> # sum_of_distances without the `if child != parent` guard
>>> # -> infinite recursion, because edges are bidirectional
RecursionError: maximum recursion depth exceeded
```

**A tree stored as an adjacency list has every edge twice**, so a traversal must remember where it came from.
**The `parent` parameter is not decoration** — without it, every recursion immediately walks back up.

**Assuming the root is the answer.**

```python
>>> # diameter, max path sum, and "largest subtree with X" all have
>>> # answers that may live anywhere in the tree
>>> # returning the root's value gives a plausible smaller number
```

**Ask whether the answer is a property of the root or of the whole tree.** If it is of the whole tree, **it
must be recorded during the traversal**, not returned from it.

---

## 8. In the interview

### How it gets asked

- *"Find the diameter of a binary tree."* — LeetCode 543, the standard opener.
- *"Maximum path sum, any node to any node."* — LeetCode 124, and it is Hard mainly for the two details.
- *"House robber, but on a tree."* — LeetCode 337, the include/exclude state.
- *"What do you return, and what do you record?"* — asked directly, sometimes.
- *"For every node, compute the sum of distances to all other nodes."* — LeetCode 834, the rerooting one.
- *"What happens if the tree has a hundred thousand nodes in a line?"*

### The first ninety seconds

> "Tree DP, and the nice thing about it is that **the hardest part of dynamic programming disappears**.
>
> **A subtree is a subproblem, and post-order traversal visits every child before its parent** — which is
> exactly the dependency direction. **So there is no table and no fill order to get wrong; the recursion does
> it for me.** After a week of interval DP where the fill order was the whole difficulty, that is worth
> saying.
>
> **The pattern is four lines: base case for the empty subtree, recurse into both children, then combine.**
>
> **The part that actually needs care is what the state is, and it is often not one number.**
>
> **For house robber on a tree — you cannot take a node and its child — the state per node is a pair: the best
> total if I take this node, and the best if I skip it.** If I take it, each child must contribute its *skip*
> value. If I skip it, each child contributes the better of its two.
>
> **And the reason for two numbers rather than one is the point:** the parent's options depend on the child's
> *choice*, not just its score. **A single 'best' would not say which case produced it.**
>
> **The other thing I would establish before writing code is the distinction between what I record and what I
> return**, because that is where the bugs are.
>
> **For diameter: the longest path *through* a node uses both children — `left + right` — and that is a
> candidate for the answer. But the value the parent needs is the longest path going *down*, which uses only
> one child — `1 + max(left, right)`** — because a path cannot fork at a node and still continue upwards.
>
> **So the function records one quantity in an outer variable and returns a different one**, and returning the
> recorded value is the defining bug of the topic: it compiles, runs, and gives numbers that are too large.
>
> **Cost: `O(n)` time — every node once — and `O(depth)` space for the stack.**
>
> **One question: how large can the tree be?** Because a hundred thousand nodes in a line is a valid tree, and
> Python's recursion limit is a thousand. **If the constraint allows that, I would write it with an explicit
> stack.**"

### The follow-ups

**"What is the difference between what you return and what you record?"**

> "They are two different quantities, and conflating them is the single most common bug in tree problems, so I
> say both out loud while writing.
>
> **Take diameter.** At a node, the longest path *through* it goes down the left subtree, up through the node,
> and down the right — **`left_depth + right_depth`.** That is a genuine candidate for the answer.
>
> **But that value is useless to the parent.** If the parent tried to extend it, the resulting walk would go
> down the left, back up through this node, down the right, back up through this node again, and on to the
> parent — **it would visit this node twice, so it is not a path.**
>
> **What the parent can use is the longest path going *down* from this node, which may use only one side:
> `1 + max(left, right)`.**
>
> **So: record `left + right`, return `1 + max(left, right)`.**
>
> **Returning the recorded value instead gives no error and numbers that are too large** — on a balanced
> seven-node tree it returns seven rather than three, because it has counted every node rather than measured a
> path. **And it grows with the tree, so it looks plausible.**
>
> **The same structure appears in maximum path sum**, with two extra details. **Clamp each child's contribution
> at zero**, because a branch with a negative sum should simply not be used — without it, the path is forced
> through losses. **And initialise the running best to negative infinity, not zero**, because an all-negative
> tree has a negative answer and zero corresponds to the empty path.
>
> **The general test I apply is: is the answer a property of the root, or of the whole tree?** Height is a
> property of the root, so I return it. **Diameter and max path sum can occur anywhere, so they are recorded
> during the traversal** — and any problem whose answer can occur anywhere needs that outer variable."

**"House robber on a tree. Why do you need two values per node?"**

> "Because the parent's options depend on **which choice** the child made, not just on how well the child did.
>
> **The rule is that I cannot take a node and its immediate child.** So when I am deciding about a node:
>
> **If I take it, every child must be skipped** — so I need each child's best total *given that the child was
> not taken*.
>
> **If I skip it, each child is free** — so I need each child's best total *either way*, which is the max of
> its two values.
>
> **A single 'best' number cannot serve both.** Suppose a child reports 10, and that 10 came from taking
> itself. **If I now take the parent, I cannot use that 10** — but the number gives me no way to know, so I add
> it anyway and produce an answer that is too large, silently, with an illegal selection behind it.
>
> **So the function returns a pair: `(take, skip)`.**
>
> **`take = node.value + left.skip + right.skip`.** **`skip = max(left.take, left.skip) + max(right.take,
> right.skip)`.** The answer at the root is the larger of its two.
>
> **This is the same idea as the mode dimension in the stock problems** — the state needs to record which
> situation you are in, because it determines what the next level can legally do. **Here the 'mode' is whether
> this node was used.**
>
> **Cost: `O(n)` time and `O(depth)` space**, and the tuple allocation per node is negligible.
>
> **And I would prefer returning a tuple to threading two `nonlocal` variables** — it is clearer, and it makes
> the state visible in the type signature, which is exactly where the difficulty of this problem lives."

**"The tree has a hundred thousand nodes and might be a straight line. What do you do?"**

> "That is a recursion-depth question, and it is deliberate — **a tree in a straight line is a valid binary
> tree**, and it is what a sorted insert sequence produces, so it appears in real test suites.
>
> **Python's default recursion limit is a thousand frames**, so a two-thousand-node line raises
> `RecursionError` before doing any useful work.
>
> **The quick fix is `sys.setrecursionlimit`, and I would mention it and then explain why I would not rely on
> it.** It raises Python's own limit but not the operating system's C stack limit, **so a deep enough tree
> segfaults the interpreter rather than raising an exception.** A crash is strictly worse than an error, and
> the depth at which it happens depends on the platform.
>
> **The robust answer is an explicit stack**, which moves the frames to the heap where they are bounded only by
> memory. A hundred thousand entries as tuples is about ten megabytes.
>
> **The pattern for getting post-order from a stack is worth knowing precisely**, because it is not obvious:
> **push each node twice — once marked unprocessed and once marked processed.** When you pop an unprocessed
> node, push it back as processed and then push its children. When you pop a processed node, both children are
> already done and their results are available.
>
> **That flag is what turns a stack into a post-order traversal**, and without it you get pre-order, which
> visits parents before children — exactly the wrong direction for DP.
>
> **The cost is that it is maybe twice the code and noticeably less readable**, so **I would write the
> recursive version first, say that it fails on a degenerate tree, and convert it if the constraint requires
> it.** Stating the trade is better than either silently using recursion or writing the harder version
> unprompted.
>
> **And for a balanced tree none of this matters** — depth is about seventeen for a hundred thousand nodes — so
> **the question is really whether the input can be adversarial**, and the constraint is where that is
> written."

### The model answer

*"You have an organisational hierarchy. Each employee has a manager, and each has a 'disruption score'. You
want to invite a set of people to a workshop such that no one is invited together with their direct manager,
maximising the total score. Then tell me, for every employee, how many people are under them."*

> "Two questions on the same tree, and they are different shapes of tree DP, so let me take them in order.
>
> **The first is house robber on a tree.** The hierarchy is a tree — each employee has one manager, the chief
> executive has none — and the constraint 'not with your direct manager' is exactly 'not a node and its
> parent'.
>
> **I would confirm one thing first: is it really a tree?** If someone can have two managers — a matrix
> organisation — **this is a graph, not a tree, and the problem becomes maximum weight independent set, which
> is NP-hard in general.** That is worth thirty seconds of asking, because the answer changes from linear-time
> to intractable.
>
> **Assuming a tree: the state per employee is a pair.** The best total for their subtree **if they are
> invited**, and the best **if they are not**.
>
> **If invited, none of their direct reports may be** — so each report contributes its 'not invited' value.
> **If not invited, each report is free** — so each contributes the better of its two.
>
> **The answer is the larger of the chief executive's two values.**
>
> **And the reason it must be a pair is the whole subtlety**: a single 'best' would not say whether that best
> included the person themselves, so their manager could not tell whether it was usable. **That would produce
> an answer that is too high with an illegal invitation list behind it** — and in this domain, an illegal list
> is a meeting where someone sits opposite their own manager, which is precisely what the constraint was for.
>
> **Cost: `O(n)`, one post-order traversal.** For any real organisation — tens of thousands of people — that is
> milliseconds.
>
> **The second question, headcount under each employee, is a simple subtree size**: one plus the sum of the
> children's counts, computed in the same post-order pass. **I would compute both in one traversal** rather
> than two, since they share the shape.
>
> **Now the practical points, which matter more here than the algorithm.**
>
> **Depth is not a problem.** Real hierarchies are shallow — even a very large company is under twenty levels —
> **so recursion is safe and I would not write the iterative version.** That is worth saying explicitly,
> because it is the opposite of the answer for an arbitrary binary tree, and knowing which situation you are in
> is the point.
>
> **But the data will not be clean.** **Cycles**: someone whose manager chain loops back, which happens in real
> HR data through bad records, **and which makes the recursion never terminate.** I would validate the
> structure first — a cycle check is one traversal — rather than discover it as a stack overflow in
> production.
>
> **And multiple roots**: contractors, or people whose manager has left. **The 'tree' is really a forest**, so
> I would run the traversal from every node with no manager and sum the results.
>
> **Finally, I would question the objective.** Maximising the total score subject to no-manager-pairs gives a
> mathematically optimal list, **and it will produce a group with strange gaps** — a whole team invited except
> one person, because their manager scored higher. **If the real goal is a useful workshop, the constraint is
> probably softer than stated**, and I would want to check that before shipping an optimiser that is
> technically correct and socially peculiar."

---

## 9. Recall card

**A subtree is a subproblem, and post-order traversal visits every child before its parent — so the recursion
IS the fill order.** No table, no loops, nothing to get wrong: **the hardest mechanical part of DP disappears
when the data is a tree.** `O(n)` time, `O(depth)` space.

**The state is often a pair, not a number.** House robber on a tree: `(take, skip)`, where
`take = value + Σ child.skip` and `skip = Σ max(child.take, child.skip)`. **One number fails because the
parent's options depend on the child's CHOICE, not just its score** — and it fails silently, too high, with an
illegal selection behind it.

**Record ≠ return, and this is the defining bug.** Diameter: **record `left + right`** (the path *through*
this node) and **return `1 + max(left, right)`** (the path *down* from it) — a path cannot fork at a node and
still continue upwards. Returning the recorded value gives no error and numbers that grow with the tree.

**Max path sum adds two details: clamp each child at `max(0, …)`** so a negative branch is skipped, and
**initialise `best` to `-inf`, not 0**, because an all-negative tree has a negative answer.

**Ask whether the answer is a property of the root or of the whole tree** — height is returned; diameter and
max path sum are **recorded**, because they can occur anywhere.

**Depth is the practical trap: a line-shaped tree is valid, and Python's limit is 1,000 frames.**
`setrecursionlimit` raises Python's limit but not the C stack, so it **segfaults instead of raising** — use an
explicit stack, pushing each node twice with a `processed` flag to get post-order. **Rerooting** answers a
question at *every* node in `O(n)` instead of `O(n²)`: one post-order pass for subtree answers, one pre-order
pass where moving the root across an edge costs one subtraction.
