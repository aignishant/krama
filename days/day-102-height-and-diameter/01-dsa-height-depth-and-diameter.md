---
day: 102
track: dsa
title: "Height, depth, and diameter"
phase: "Trees and binary search trees"
status: written
---

# Day 102 · DSA — Height, depth, and diameter

**After today you can:** You can compute the diameter in one pass, using the height as a by-product.

**The interviewer asks it as:** *Find the diameter of the binary tree in O(n).*

---

## 1. What this is, and why they ask it

The **diameter** of a tree is the length of the longest path between any two nodes in it. The path does
not have to pass through the root, and it does not have to end at a leaf on both sides — though in
practice it always does.

Three sentences. The obvious solution computes, at every node, the height of its left subtree plus the
height of its right subtree, and takes the largest — which is correct and is `O(n²)`, because computing a
height is itself a walk of a whole subtree. The fix is the technique this whole phase turns on: **a
function that returns one thing to its parent while recording a different thing in an outer variable.**
Here it returns the height and records the diameter. And once you have seen that trick, five more
problems become one-pass instead of two-pass.

They ask it because the `O(n²)` version looks completely reasonable and passes small tests, so the
question is really *"can you see that `height` is being recomputed?"* — and then *"can you restructure
the recursion so that the thing you need is already being calculated?"* The follow-ups are the same trick
applied elsewhere: balanced-tree checking, maximum path sum, and the largest subtree satisfying some
property.

---

## 2. The story

The house had been added to four times since it was built, and by the time Zubeida inherited it, it
sprawled.

There was the original bit at the front with three rooms. Somebody had built two rooms off the side in
the sixties. Her father had added a kitchen and a store behind that, and then the long room at the back
for her brother's family, which had its own two small rooms off it.

She wanted an intercom put in, the kind with handsets in each room, and the man who came to do it stood
in the front doorway and asked her one question that took the whole afternoon to answer: **what is the
longest run of wire I will need, from any one room to any other?**

Her first thought was that it must be from the front room to the back room, because those were the two
ends of the house. But it was not, and she worked out why while walking around.

The front rooms were all close together. The long run was actually from the small room off her brother's
end, all the way through the middle, and out to the second room of the sixties extension — and neither
of those was the front or the back of the house.

The man had a method that she liked, and it was the reason the afternoon ended at four rather than at
midnight.

He did not measure between pairs of rooms. There were fourteen rooms, and measuring every pair would
have been ninety-one measurements.

Instead he stood at each junction — each place where the house split into two or more directions — and
asked only one thing: **going that way, how far is the furthest room? And going that way?** Then he added
the two answers together, and that was the longest run passing through that junction.

He wrote each one down as he went, in his phone, and at the end he took the biggest of them.

And there was one economy in it that Zubeida did not spot until he explained it. When he stood at a
junction and worked out "the furthest room in that direction", he was really asking the same question he
would ask standing at the next junction along, plus a few steps. So he never measured a corridor twice.
He started at the far ends and worked back towards the front door, and each junction's answer was built
out of the answers he already had.

He said the men who do it the other way — measuring from every room to every room — are still there at
nine at night, and they get the same number.

---

## 3. The idea in plain English

The electrician has computed a diameter, and his economy — "each junction's answer is built out of the
answers I already have" — is the whole technique.

- Each room and junction is a node.
- "How far is the furthest room going that way" is the **height** of that subtree.
- The longest run **through** a junction is `left height + right height`.
- The answer for the whole house is the largest of those, over every junction.

### The definition, and its two conventions

**Diameter = the number of edges on the longest path between any two nodes.**

```
        1
       / \
      2   3
     / \
    4   5

 the longest path: 4 -> 2 -> 5   (2 edges)
                or 4 -> 2 -> 1 -> 3  (3 edges)   <- longer

 diameter = 3 edges  =  4 nodes
```

**LeetCode 543 counts edges**, so a single node has diameter 0 and the example above is 3. Some textbooks
count nodes, giving 4. **Say which you are using**, exactly as with height on
[day 098](../day-098-what-a-tree-is/README.md). The relationship is always `nodes = edges + 1`.

**The path does not have to go through the root**, and that is the point of the problem. A tree with a
deep left subtree and nothing on the right has its diameter entirely inside the left subtree.

### The key observation

For any node, the longest path **whose highest point is that node** is:

```
 height(left subtree) + height(right subtree) + 2        (in edges, where an empty subtree is -1)
```

Every path has exactly one highest point — one node on it that is closer to the root than all the others.
So if you compute that quantity at every node and take the maximum, you have considered every possible
path exactly once.

**That is the whole algorithm**, and stating it in that form — *every path has a unique highest node, so
I evaluate every node as the top of a path* — is what makes the solution sound derived rather than
recalled.

### Why the obvious version is `O(n²)`

```python
    def diameter(node):
        if node is None:
            return 0
        through = height(node.left) + height(node.right) + 2
        return max(through, diameter(node.left), diameter(node.right))
```

Correct. And `height` walks an entire subtree, and it is called at every node, so the total work is the
sum of all the subtree sizes:

```
 balanced tree:    O(n log n)
 degenerate tree:  O(n^2)
```

```
 n = 10,000, a chain
   O(n^2)  ->  ~50,000,000 operations   — seconds
   O(n)    ->  ~10,000                  — instant
```

Zubeida's electrician measuring every corridor once per junction instead of once, ever.

### The trick: return one thing, record another

The insight is that `height` **already visits every node once** and already knows both children's
heights at the moment it needs them. So the diameter can be computed *inside* the height function, and
stored somewhere outside.

```python
    def diameter_of_binary_tree(root):
        best = 0                            # the OUTER variable

        def height(node):
            nonlocal best
            if node is None:
                return -1
            left = height(node.left)
            right = height(node.right)
            best = max(best, left + right + 2)      # RECORD the diameter here
            return 1 + max(left, right)             # RETURN the height

        height(root)
        return best
```

**Two different quantities, and they must not be confused:**

- **Returned to the parent:** the height. This is what the parent needs — "how far down does your side
  go".
- **Recorded in `best`:** the diameter through this node. The parent has no use for this, because a path
  bending at a child cannot be extended upward.

**That is the sentence to say out loud in the interview.** *"The value I return is not the value I am
looking for. I return the height because that is what my parent needs, and I record the diameter on the
side, because a path that bends here cannot be part of a longer path through my parent."*

Once you have that sentence, this whole family of problems is the same code with two lines changed.

### The family

| Problem | Return to the parent | Record on the side |
|---|---|---|
| Diameter (543) | height | `left + right + 2` |
| Balanced tree (110) | height, or `-2` meaning "already unbalanced" | — (short-circuit instead) |
| Maximum path sum (124) | best downward sum, floored at 0 | `left + right + node.val` |
| Longest univalue path (687) | longest same-value arm | `left + right` |
| Largest BST subtree (333) | `(min, max, size, is_bst)` | `size` when `is_bst` |

**Five interview problems, one shape.** [Day 104](../day-104-tree-path-problems/README.md) does maximum
path sum properly; today is the shape.

### Balanced, in one pass, as the second example

The naive check calls `height` at every node — the same `O(n²)`. The one-pass version returns the height
normally, and returns a **sentinel** when it has already found an imbalance:

```python
        if left == -2 or right == -2 or abs(left - right) > 1:
            return -2                       # -2 means "unbalanced somewhere below"
        return 1 + max(left, right)
```

**The sentinel propagates all the way up without any further work being done**, which is what makes it a
single pass. `-2` is chosen because a real height is never less than `-1`.

An alternative that some prefer is returning a tuple `(height, is_balanced)`. It is clearer and it
allocates a tuple per node. **Either is fine; say which you are doing and why.**

### The relationship between height and diameter

Two facts worth having, because interviewers probe them:

```
 diameter >= height          always
 diameter <= 2 × height      always
```

The first because the path from the root to the deepest leaf is itself a path. The second because any
path is two downward paths glued at their highest node, and each is at most the height.

And the case people get wrong: **the diameter can be entirely inside one subtree and not touch the root
at all.**

---

## 4. The picture

Zubeida's house, and why the answer is not front-to-back.

```
                      hall (junction)
                     /       |        \
              front wing   kitchen   long room
                /    \        |        /     \
             r1      r2     store    b1      b2
                      |
                     r3

 heights (edges to the deepest room below):
   front wing: 2   (via r2 -> r3)
   kitchen:    1
   long room:  1

 longest path THROUGH the hall = 2 + 1 + 2 = 5 edges
                                  ^   ^   ^
                    front wing's height + long room's height + the two edges

 path: r3 -> r2 -> front wing -> hall -> long room -> b1

 NOT front-to-back: r1 -> ... -> b1 is only 4 edges.
```

The two quantities, at one node:

```
                        node
                       /    \
            left subtree      right subtree
            height = 3        height = 1

    RETURNED to the parent:  1 + max(3, 1)  =  4
                             "my side goes 4 deep"

    RECORDED in `best`:      3 + 1 + 2      =  6
                             "the longest path bending here is 6 edges"

 the parent CANNOT use the 6. A path that bends here has already used
 both of my children, so it cannot also go up through me.
```

The `O(n²)` version, drawn as wasted work:

```
 a chain of 5 nodes:  1 - 2 - 3 - 4 - 5

 height() is called at every node by diameter():
   at node 1: walks 5 nodes
   at node 2: walks 4
   at node 3: walks 3
   at node 4: walks 2
   at node 5: walks 1
                    ---
                     15 node visits for 5 nodes

 n = 10,000  ->  ~50,000,000 visits
 one pass    ->      10,000
```

The one-pass version, traced:

```
        1
       / \
      2   3
     / \
    4   5

 call order (postorder — children first):

 height(4): left=-1 right=-1  best = max(0, -1+-1+2)=0   returns 0
 height(5): left=-1 right=-1  best = max(0, 0)     = 0   returns 0
 height(2): left=0  right=0   best = max(0, 0+0+2) = 2   returns 1
 height(3): left=-1 right=-1  best = max(2, 0)     = 2   returns 0
 height(1): left=1  right=0   best = max(2, 1+0+2) = 3   returns 2

 answer: 3    (the path 4 -> 2 -> 1 -> 3)

 note `best` only ever goes UP, and each node is visited exactly once.
```

---

## 5. The code, built step by step

### Step 1 — say the key observation before writing anything

"Every path has exactly one highest point — one node on the path that is nearest the root. So if I
evaluate every node as the top of a path, I have considered every path exactly once. At a node, the
longest path bending there is the left subtree's height plus the right subtree's height plus two."

**That sentence is the solution.** Everything after it is bookkeeping.

### Step 2 — write the naive version and then criticise it

```python
    through = height(node.left) + height(node.right) + 2
    return max(through, diameter(node.left), diameter(node.right))
```

"That is correct, and it is `O(n²)` on a skewed tree, because `height` walks a whole subtree and I am
calling it at every node. On a ten-thousand-node chain that is fifty million operations instead of ten
thousand."

**Writing the wrong version deliberately and naming its cost is a strong move**, because it shows you
found the improvement rather than remembered it.

### Step 3 — notice what the height function already knows

"`height` visits every node once and, at the moment it computes a node's height, it already has both
children's heights. So the diameter through that node is available for free, right there. I do not need a
second traversal — I need a place to put the answer."

### Step 4 — the outer variable

```python
        best = 0
        def height(node):
            nonlocal best
```

`nonlocal` is required to assign to a variable from the enclosing function. Without it, Python treats
`best` as a new local and the outer one never changes — **a silent zero**, which is trap 2 below.

The alternatives are a one-element list (`best = [0]`, mutated as `best[0] = ...`) or a class attribute.
`nonlocal` is cleanest in Python 3.

### Step 5 — get the base case right for the convention

```python
        if node is None:
            return -1                       # EDGE convention
```

Then a leaf returns `1 + max(-1, -1) = 0`, and `best` at a leaf is `-1 + -1 + 2 = 0`. Both correct.

**If you return `0` for `None` instead, the formula becomes `left + right` with no `+ 2`.** Both work,
and mixing them gives an answer that is off by two, which is exactly the kind of bug that survives small
tests.

### The complete solution

```python
from collections import deque


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def diameter_naive(root: TreeNode | None) -> int:
    """The version to write, criticise, and then replace.

    Correct, and O(n^2) on a skewed tree: height() walks an entire subtree
    and is called at every node. On a 10,000-node chain that is ~50 million
    operations instead of 10,000.
    """
    def height(node: TreeNode | None) -> int:
        if node is None:
            return -1
        return 1 + max(height(node.left), height(node.right))

    def walk(node: TreeNode | None) -> int:
        if node is None:
            return 0
        through = height(node.left) + height(node.right) + 2
        return max(through, walk(node.left), walk(node.right))

    return walk(root)


def diameter(root: TreeNode | None) -> int:
    """LeetCode 543, in one pass.

    THE IDEA: every path has exactly one highest node, so evaluating every
    node as the top of a path considers every path exactly once.

    THE TRICK: the function RETURNS the height (what the parent needs) and
    RECORDS the diameter in an outer variable (what the parent cannot use,
    because a path bending here has already spent both of my children).

    Edge convention: empty tree is -1, a leaf has height 0, so the path
    through a node is left + right + 2.

    Time O(n) — one visit per node. Space O(height) for the stack.
    """
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best                       # without this, `best` stays 0
        if node is None:
            return -1
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right + 2)  # RECORD: the path bending here
        return 1 + max(left, right)         # RETURN: what my parent needs

    height(root)
    return best


def is_balanced_naive(root: TreeNode | None) -> bool:
    """Same O(n^2) mistake, same fix available."""
    def height(node: TreeNode | None) -> int:
        if node is None:
            return -1
        return 1 + max(height(node.left), height(node.right))

    def check(node: TreeNode | None) -> bool:
        if node is None:
            return True
        if abs(height(node.left) - height(node.right)) > 1:
            return False
        return check(node.left) and check(node.right)

    return check(root)


def is_balanced(root: TreeNode | None) -> bool:
    """LeetCode 110, in one pass, using a SENTINEL.

    -2 means "unbalanced somewhere below me". It propagates all the way up
    without any further work, which is what makes this a single pass.
    -2 is safe because a genuine height is never below -1.
    """
    UNBALANCED = -2

    def height(node: TreeNode | None) -> int:
        if node is None:
            return -1
        left = height(node.left)
        if left == UNBALANCED:
            return UNBALANCED               # short-circuit: stop working
        right = height(node.right)
        if right == UNBALANCED or abs(left - right) > 1:
            return UNBALANCED
        return 1 + max(left, right)

    return height(root) != UNBALANCED


def is_balanced_tuple(root: TreeNode | None) -> bool:
    """The same, returning (height, is_balanced) instead of a sentinel.

    Clearer, and it allocates a tuple per node. Either is fine — say which
    you are doing and why.
    """
    def check(node: TreeNode | None) -> tuple[int, bool]:
        if node is None:
            return -1, True
        lh, lb = check(node.left)
        if not lb:
            return 0, False
        rh, rb = check(node.right)
        if not rb or abs(lh - rh) > 1:
            return 0, False
        return 1 + max(lh, rh), True

    return check(root)[1]


def diameter_with_path(root: TreeNode | None) -> tuple[int, list[int]]:
    """The follow-up: return the path itself, not just its length.

    Same shape, but now the recursion returns (height, the deepest downward
    path from here) so the winning pair can be glued together at the node
    where the best diameter was found.
    """
    best = 0
    best_path: list[int] = []

    def walk(node: TreeNode | None) -> tuple[int, list[int]]:
        nonlocal best, best_path
        if node is None:
            return -1, []
        lh, lpath = walk(node.left)
        rh, rpath = walk(node.right)
        if lh + rh + 2 > best:
            best = lh + rh + 2
            best_path = lpath[::-1] + [node.val] + rpath
        if lh >= rh:
            return lh + 1, lpath + [node.val]
        return rh + 1, rpath + [node.val]

    walk(root)
    return best, best_path


def longest_univalue_path(root: TreeNode | None) -> int:
    """LeetCode 687. The same shape with one condition added: an arm only
    counts if the child's value equals mine."""
    best = 0

    def arm(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = arm(node.left)
        right = arm(node.right)
        left = left + 1 if node.left and node.left.val == node.val else 0
        right = right + 1 if node.right and node.right.val == node.val else 0
        best = max(best, left + right)      # RECORD
        return max(left, right)             # RETURN

    arm(root)
    return best


def height(node: TreeNode | None) -> int:
    """Plain height, for comparison. Edge convention."""
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def diameter_broken_no_nonlocal(root: TreeNode | None) -> int:
    """The trap, written out. Without `nonlocal`, the assignment creates a
    NEW local `best` inside height(), and the outer one is never touched."""
    best = 0

    def h(node: TreeNode | None) -> int:
        if node is None:
            return -1
        left = h(node.left)
        right = h(node.right)
        # best = max(best, left + right + 2)   <- would raise UnboundLocalError
        return 1 + max(left, right)

    h(root)
    return best                             # always 0


def from_list(values: list[int | None]) -> TreeNode | None:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    root = from_list([1, 2, 3, 4, 5])
    print(diameter(root), diameter_naive(root))          # 3 3
    print(height(root))                                  # 2
    print(diameter_with_path(root))                      # (3, [4, 2, 1, 3])

    # the diameter does NOT have to pass through the root
    lopsided = from_list([1, 2, None, 3, 4, 5, 6])
    print(diameter(lopsided))                            # 4  <- 5->3->2->4->6
    print(height(lopsided))                              # 3
    print(diameter(lopsided) >= height(lopsided))        # True, always
    print(diameter(lopsided) <= 2 * height(lopsided))    # True, always

    print(diameter(None), diameter(TreeNode(1)))         # 0 0
    print(diameter(TreeNode(1, TreeNode(2))))            # 1

    print(is_balanced(root), is_balanced_tuple(root))    # True True
    chain = from_list([1, 2, None, 3, None, 4])
    print(is_balanced(chain))                            # False

    print(longest_univalue_path(from_list([5, 4, 5, 1, 1, None, 5])))    # 2

    print(diameter_broken_no_nonlocal(root))             # 0  <- silently wrong

    # the cost difference, on a chain
    import time
    long_chain = TreeNode(0)
    node = long_chain
    for i in range(1, 2000):
        node.right = TreeNode(i)
        node = node.right
    t = time.perf_counter(); diameter(long_chain); fast = time.perf_counter() - t
    t = time.perf_counter(); diameter_naive(long_chain); slow = time.perf_counter() - t
    print(f"one pass {fast:.4f}s vs naive {slow:.4f}s  ({slow / fast:.0f}x)")
```

---

## 6. What it costs

### The two versions

```
 one pass:   each node visited exactly once            O(n)
 naive:      height() called at every node, and each
             call walks that node's whole subtree
             = the sum of all subtree sizes
```

```
 balanced tree:    sum of subtree sizes = O(n log n)
 degenerate tree:  n + (n-1) + (n-2) + ... = n(n+1)/2 = O(n^2)
```

```
 n = 1,000    one pass 1,000        naive ~500,000        500×
 n = 10,000   one pass 10,000       naive ~50,000,000   5,000×
 n = 100,000  one pass 100,000      naive ~5×10^9      50,000×  — will not finish
```

**The measurement is in the code above.** Run it rather than trusting the table; at 2,000 nodes the
difference is already a few hundred times.

### Space

```
 recursion stack        O(height)
 outer variable         O(1)
 -----------------------------------
 extra space            O(height)
```

```
 balanced, n = 1,000,000      ~20 frames
 degenerate, n = 10,000       10,000 frames  ->  RecursionError
```

Same warning as every tree problem. **A skewed tree is exactly the worst case for both the naive time and
the recursive space**, which is worth noticing: the input that makes the naive version `O(n²)` is the same
input that overflows the stack.

The `diameter_with_path` variant is different: it builds lists as it goes, so its space is `O(n)` in the
worst case, not `O(height)`. **Returning a path costs more than returning a number**, and saying so is
the right answer if asked to produce the path.

### The bounds

```
 height    <=  diameter  <=  2 × height
```

```
 a chain of n nodes:      height = n-1,   diameter = n-1        (diameter = height)
 a perfect tree, h=3:     height = 3,     diameter = 6          (diameter = 2 × height)
```

Both bounds are tight, and being able to give the shape that achieves each is a good answer to "how do
those two relate?".

### Why `+ 2` and not `+ 1`

```
 edge convention, empty subtree = -1

 leaf:              left = -1, right = -1  ->  -1 + -1 + 2 = 0    correct
 node with 1 child: left =  0, right = -1  ->   0 + -1 + 2 = 1    correct
 node with 2 leaves:left =  0, right =  0  ->   0 +  0 + 2 = 2    correct
```

The `+ 2` is **the two edges from the node down into each subtree**. With the node convention (empty = 0)
the formula is `left + right` with no addition, and mixing the two gives an answer off by exactly two —
which passes on a single node and fails on everything else.

---

## 7. The traps

### Trap 1 — assuming the diameter passes through the root

```python
    return height(root.left) + height(root.right) + 2        # WRONG
```

```
 diameter(from_list([1, 2, None, 3, 4, 5, 6]))
   this version -> 3
   correct      -> 4          (the path 5 -> 3 -> 2 -> 4 -> 6, which never touches the root)
```

**The path bends at some node; there is no reason it is the root.** This is the single most common wrong
answer, and it passes on symmetric test trees.

### Trap 2 — forgetting `nonlocal`

```python
        best = max(best, left + right + 2)
```

```
 UnboundLocalError: cannot access local variable 'best' where it is not associated with a value
```

Python sees an assignment to `best` and makes it a local, so the read on the right-hand side fails. With
a read-only reference it would not error — it would silently use the outer value and never update it,
returning 0. **Declare `nonlocal best` at the top of the inner function.**

### Trap 3 — returning the diameter instead of the height

```python
        return max(left, right, left + right + 2)            # WRONG
```

This returns something the parent cannot use. A path that bends at this node has already used both
children, so it cannot continue upward — **the parent needs a single downward arm, not a bent path.**
The result is an answer that is too large and grows nonsensically with depth.

**Say the sentence: "what I return and what I record are different quantities."**

### Trap 4 — mixing the two conventions

```python
        if node is None:
            return 0                        # node convention
        best = max(best, left + right + 2)  # edge convention's formula
```

Off by two on every non-trivial tree, and correct on a single node. **Pick edges or nodes, and make the
base case and the formula agree.**

### Trap 5 — `is_balanced` calling `height` at every node

```python
        if abs(height(node.left) - height(node.right)) > 1:
```

The same `O(n²)`, in a different problem. The interviewer will accept it and then ask for one pass. Use
the sentinel, or the tuple.

### Trap 6 — a sentinel value that a real height could take

```python
        return -1                           # as "unbalanced"
```

`-1` is the height of an empty tree, so this is indistinguishable from a legitimate answer and the check
silently reports unbalanced trees as balanced. **`-2` is safe because a real height is never below `-1`;**
with the node convention, `-1` is safe because a real height is never below `0`.

### Trap 7 — recursion on a deep tree

```python
    diameter(chain_of_10000_nodes)
```

```
 RecursionError: maximum recursion depth exceeded
```

The `O(n)` version fixes the time and not the space. If `n` can be 10⁵ with no balance guarantee, either
convert to an explicit stack with a postorder walk, or say the risk out loud.

### Trap 8 — reporting the number of nodes when asked for edges

```
 diameter(from_list([1,2,3,4,5]))
   edges: 3
   nodes: 4
```

Both are defensible answers to "the diameter"; only one matches the tests. **Ask, or state which you are
giving.**

---

## 8. In the interview

### How it gets asked

- The base: *"Find the diameter of the binary tree."* LeetCode 543.
- The constraint: *"Now do it in `O(n)`."* — which is the real question.
- The sibling: *"Is this tree height-balanced?"* LeetCode 110, and the same one-pass fix.
- The escalation: *"Maximum path sum."* LeetCode 124, which is
  [day 104](../day-104-tree-path-problems/README.md).
- The extension: *"Return the path, not just its length."*

### What to say out loud, in the first ninety seconds

1. **Define it, and flag the two conventions.** "The diameter is the longest path between any two nodes. I
   will count edges, so a single node is 0 — tell me if you want the node count and I will add one."
2. **Say the thing people get wrong, before you get it wrong.** "It does not have to pass through the
   root. The path bends at some node, and that node can be anywhere."
3. **State the key observation.** "Every path has exactly one highest node. So if I evaluate every node as
   the top of a path, I consider every path exactly once. At a node, the bent path is
   `left height + right height + 2`."
4. **Write the naive version and name its cost.** "The direct version calls `height` at every node, and
   `height` walks a whole subtree — so it is `O(n log n)` on a balanced tree and `O(n²)` on a chain."
5. **State the trick precisely.** "The improvement is that `height` already visits every node once and
   already has both children's heights when it needs them. So I compute the diameter inside the height
   function and record it in an outer variable. **The value I return and the value I am looking for are
   different**: I return the height because that is what my parent needs, and I record the diameter,
   because a path bending here cannot be extended upward through my parent."
6. **Give both complexities.** "`O(n)` time, one visit per node. `O(height)` space for the stack — twenty
   frames on a balanced million-node tree, and a million on a chain."

### The follow-ups

**"Why is the naive version `O(n²)`?"**
"Because `height` is itself a full walk of a subtree, and I am calling it once per node. The total work
is the sum of every subtree's size. On a balanced tree that sums to `O(n log n)`; on a skewed tree it is
`n + (n−1) + (n−2) + …`, which is `O(n²)`. Concretely, on a ten-thousand-node chain that is about fifty
million operations against ten thousand for the one-pass version. And it is worth noticing that the input
that makes it quadratic — a chain — is the same input that overflows the recursion stack, so a skewed
tree is the worst case for both."

**"How does the one-pass version work?"**
"The observation is that I am already computing every height, and at the moment I compute a node's height
I have both children's heights sitting in local variables. The diameter through that node is exactly
those two added together, plus two edges. So there is nothing more to compute — I just need somewhere to
put it. I keep an outer variable and update it at every node. The part worth stating explicitly is that
**the returned value and the recorded value are different quantities**: I return the height, because that
is what my parent needs to know about my side; I record the bent path, because my parent cannot use it —
a path that bends at me has already consumed both of my children, so it cannot also go up through me."

**"Now check whether the tree is balanced, in one pass."**
"Same shape. The naive version calls `height` at every node and is `O(n²)` for the same reason. In one
pass, the function returns the height, but returns a **sentinel** as soon as it discovers an imbalance —
I use `-2`, because a genuine height with the edge convention is never below `-1`. Once a `-2` appears it
propagates straight to the top with no further work, which is what makes it a single pass. The
alternative is returning a tuple of `(height, is_balanced)`, which is clearer and allocates a tuple per
node. I would use the sentinel and say why the specific value is safe — using `-1` there would be
indistinguishable from the empty-tree height and would silently report unbalanced trees as balanced."

**"Return the actual path, not just its length."**
"Same recursion with a bigger return value: instead of returning just the height, return the height and
the deepest downward path from this node. Then when a node beats the best diameter, the winning path is
the left arm reversed, plus this node, plus the right arm. The cost changes though, and I would say so:
building those lists makes the space `O(n)` in the worst case rather than `O(height)`, because every
frame is holding a path. If that mattered, the alternative is to record only the *node* where the best
diameter was found in the first pass, then do a second short walk from there to reconstruct the two arms
— two passes, but `O(height)` space."

**"What is the relationship between the height and the diameter?"**
"`height ≤ diameter ≤ 2 × height`, and both bounds are tight. The lower bound because the root-to-deepest-
leaf path is itself a path, so the diameter is at least the height. The upper bound because every path is
two downward arms glued at its highest node, and each arm is at most the height. A chain achieves the
lower bound — its diameter equals its height. A perfect tree achieves the upper bound — the path between
two opposite leaves is exactly twice the height."

**"What if the tree is very deep?"**
"Then the `O(n)` fix does not help me, because it fixed the time and not the space — the recursion is
still `O(height)`, and a chain of ten thousand nodes exceeds Python's default limit of a thousand. Two
options. Raise the limit, which is honest but fragile. Or do the postorder walk with an explicit stack: I
push each node with a flag, and on the second visit I have both children's heights available from a
dictionary or a value stack, and I do exactly the same two operations. That is more code and it is what
I would write if the constraint said `n ≤ 10⁵` with no balance guarantee."

### A model answer

Asked: *find the diameter of the binary tree in `O(n)`.*

> "The diameter is the longest path between any two nodes. Two things to pin down first. I will count
> **edges**, so a single node has diameter 0 — say if you want the node count and it is one more. And the
> path **does not have to pass through the root**; it bends at some node, and that node can be anywhere.
> A tree with a deep left subtree and one node on the right has its diameter entirely inside the left
> side.
>
> The observation that makes this tractable: **every path has exactly one highest node** — one node on it
> that is closer to the root than all the others. So if I evaluate every node as the top of a path, I have
> considered every possible path exactly once, with no duplication. And at a given node, the longest path
> bending there is simply `height of the left subtree + height of the right subtree + 2`.
>
> The direct implementation of that is to write a `height` function and call it at every node. It is
> correct, and it is `O(n²)` on a skewed tree, because `height` is itself a walk of a whole subtree and I
> am doing it once per node — the total is the sum of all subtree sizes. On a ten-thousand-node chain that
> is around fifty million operations against ten thousand.
>
> The fix is to notice that `height` **already** visits every node exactly once, and at the moment it
> computes a node's height it already has both children's heights sitting in local variables. So the
> diameter through that node is available right there, for free. There is nothing extra to compute — I
> only need somewhere to put it. So I keep a variable outside the recursion and update it at every node.
>
> The part I want to say precisely, because it is the whole technique: **the value I return and the value
> I am looking for are different.** I return the **height**, because that is what my parent needs — 'how
> far down does your side go'. I record the **bent path** on the side, because my parent has no use for
> it: a path that bends at me has already consumed both of my children, so it cannot also travel upward
> through me. Confusing those two — returning the bent path — gives an answer that is too large and grows
> with depth.
>
> One Python detail: the inner function needs `nonlocal` to assign to that outer variable, otherwise
> Python makes it a new local and you get an `UnboundLocalError` — or, if you only read it, a silent zero.
>
> Complexity is `O(n)` time, one visit per node, and `O(height)` space for the call stack — about twenty
> frames on a balanced million-node tree and a million on a chain, so if the input can be skewed and large
> I would either raise the recursion limit or do the postorder walk with an explicit stack.
>
> And the same shape solves several neighbouring problems: balanced-tree checking with a sentinel instead
> of a recorded maximum, maximum path sum with the arms floored at zero, and longest same-value path with
> one extra condition on each arm. It is one technique, not four."

---

## 9. Recall card

- **Diameter = the longest path between any two nodes, and it does NOT have to pass through the root** —
  that is the most common wrong answer and it passes on symmetric tests. Count **edges** by default
  (LeetCode 543): a single node is 0, and `nodes = edges + 1`.
- **The key observation: every path has exactly one highest node**, so evaluating every node as the top of
  a path considers every path exactly once. At a node the bent path is
  **`left height + right height + 2`** (edge convention, empty = −1).
- **The naive version calls `height` at every node → `O(n log n)` balanced, `O(n²)` on a chain** — 50
  million operations at n = 10,000 against 10,000. **The same skewed input is also the stack-overflow
  case.**
- **The trick, and it is the whole phase: RETURN one quantity, RECORD another.** Return the **height**
  (what the parent needs); record the **bent path** in an outer variable (the parent cannot use it — a
  path bending here has already spent both children). Returning the bent path instead gives an answer
  that grows with depth. Python needs **`nonlocal`**, or you get `UnboundLocalError` or a silent 0.
- **The same shape solves five problems**: diameter, **balanced in one pass** (return a **`-2` sentinel** —
  `-1` is a real height and would silently pass), maximum path sum, longest univalue path, largest BST
  subtree. `O(n)` time, **`O(height)` space** — and returning the *path* rather than the length costs
  `O(n)` space instead. Bounds: **`height ≤ diameter ≤ 2 × height`**, both tight.
