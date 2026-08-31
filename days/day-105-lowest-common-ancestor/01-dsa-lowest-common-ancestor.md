---
day: 105
track: dsa
title: "Lowest common ancestor"
phase: "Trees and binary search trees"
status: written
---

# Day 105 · DSA — Lowest common ancestor

**After today you can:** You can find the LCA in a general binary tree and in a BST, and know why they differ.

**The interviewer asks it as:** *Find the lowest common ancestor of these two nodes.*

---

## 1. What this is, and why they ask it

The **lowest common ancestor** of two nodes is the deepest node that has both of them somewhere beneath
it. "Deepest" is the whole point — the root is always *a* common ancestor, and it is almost never the
answer.

Three sentences. In a **general binary tree** you have to search, because nothing about the values tells
you where anything is, and the solution is a postorder walk that returns a node upward and lets the
answer emerge at the place where two different children both report success. In a **binary search tree**
you do not search at all — the ordering tells you which way to go, so it is a walk down from the root
with no recursion and no extra space. And there is a hidden assumption in the standard problem that
changes the code completely when it is removed: **both nodes are guaranteed to be in the tree.**

They ask it because the general-tree solution is six lines that are genuinely hard to derive and trivial
to recognise, so it separates people who have understood the postorder return pattern from people who
have memorised a snippet. The BST version then checks whether you notice that the extra structure makes
the search unnecessary — and *"why is your BST answer different?"* is the follow-up that decides the
round.

---

## 2. The story

The engagement was in the morning and the lunch went on until four, and by two o'clock the two young men
sitting near the fan had established that they were somehow related and could not work out how.

One was from the Salem side. The other had come with the bride's people from Pollachi. They had worked
out that both of their families had once been in the same village, and then they had got stuck, because
neither of them knew more than three generations back.

Somebody sent them to Ponnamma, who was eighty-six and sitting in the good chair by the window, and who
had been asked this question at every function for forty years.

She did not do it the way they had been trying. They had been listing names at each other — my father,
his father, his father — and hoping to hit a match, which works but takes a long time when neither
person is sure of the spellings.

What she did was ask about the branches.

She named her husband's four brothers, and asked, one at a time: is this boy from your line? Is that boy
from your line?

For the eldest brother's line, the answer was no to both. Nothing there — stop, do not go further down
it.

For the second brother, one of them was in it. Just one.

For the third brother, the other one was in it. Also just one.

And at that point she stopped and said: then it is my husband's father. Because one of you comes down
through one son and the other comes down through a different son, and the first place you are both
underneath is the man those two sons belonged to.

Somebody asked what if they had both been under the second brother.

She said then the answer would not be her husband's father at all, it would be somewhere down inside
that line, and you would have to go and ask the same question again down there. You keep going down as
long as they are both on the same side. The moment they split, you have found it.

And she added the other case, which took her one sentence. If she had asked the four brothers and one of
them had said "this boy is my grandson, and the other boy is *me*" — then the answer is that brother
himself. A person can be their own ancestor for this purpose. Otherwise you would go looking past him and
find nothing.

---

## 3. The idea in plain English

Ponnamma has just described the general-tree algorithm exactly, including the case people forget.

- Each brother's line is a **subtree**.
- "Is either of these two in your line?" is the recursive call.
- **Two different children both say yes → this node is the answer.**
- **Only one child says yes → the answer is inside that child**, so pass its answer upward unchanged.
- "The other boy is me" → **a node can be its own ancestor**, and that is the base case people omit.

### The general binary tree

```python
    def lca(node, p, q):
        if node is None or node is p or node is q:
            return node                     # found one, or ran out
        left = lca(node.left, p, q)
        right = lca(node.right, p, q)
        if left and right:
            return node                     # they SPLIT here — this is the answer
        return left or right                # both on one side, or neither
```

Six lines. Read them as Ponnamma's questions:

```
 `node is p or node is q`     "the other boy is me"       -> report myself upward
 left and right both non-None "they came down two lines"  -> I am the answer
 only one non-None            "both are in that one line" -> pass its answer up
 both None                    "neither is under me"       -> report nothing
```

**The subtle part is what the function returns.** It is not "the LCA of this subtree". It is:

> *"If I have found the answer below me, the answer. Otherwise, whichever of `p` or `q` I have found, if
> any. Otherwise `None`."*

Three different meanings from one return value. That overloading is why the code is short and why it is
hard to derive. **Say the three meanings out loud in the interview** — it is the thing being tested.

### Why it is correct

Consider where `p` and `q` sit relative to a node:

```
 both in the left subtree    -> left is non-None, right is None -> return left (the answer is deeper)
 both in the right subtree   -> mirror image
 one in each                 -> both non-None -> THIS node is the answer
 p is this node, q below it  -> return this node immediately; the parent sees one non-None child
 neither below               -> None
```

**The fourth case is the ancestor case**, and the early return handles it: if `node is p`, we stop and
report `p` upward without looking for `q` at all. That is correct precisely *because* both nodes are
guaranteed to exist — if `q` is anywhere, it must be below `p`, so `p` is the answer.

### The assumption that changes everything

```
 "Both p and q exist in the tree."
```

Every standard solution relies on it. Remove it and the code above is wrong:

```
 tree: 1 -> 2 (left child)
 lca(tree, node2, node_not_in_tree)  ->  returns node 2

 but node 2 is NOT the LCA of anything, because the other node does not exist.
 The correct answer is None.
```

The fix is to **count what you actually found**, and check at the end:

```python
        found = 0
        ...
        if node is p or node is q:
            found += 1
        ...
        return answer if found == 2 else None
```

**LeetCode 1644 is exactly this variant**, and asking *"can I assume both nodes are present?"* before you
start is one of the cheapest good impressions available in this problem.

### The binary search tree: no search at all

In a BST everything left of a node is smaller and everything right is larger. So you never have to look
for anything — the values tell you where they are.

```python
    def lca_bst(node, p, q):
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left            # both smaller: the answer is left
            elif p.val > node.val and q.val > node.val:
                node = node.right           # both larger: the answer is right
            else:
                return node                 # they SPLIT here (or one IS here)
```

**The split point is the answer.** Walk down while both are on the same side; the first node where they
diverge — or where one of them *is* the node — is the LCA.

That `else` branch quietly covers three cases at once: `p < node < q`, `q < node < p`, and `node` being
`p` or `q` itself. It is worth pointing out, because it looks like a case has been missed.

```
 general tree:  O(n) time, O(height) space, must visit every node in the worst case
 BST:           O(height) time, O(1) space, iterative, no recursion at all
```

**On a balanced BST of a million nodes that is twenty comparisons against a million.** The reason for the
difference, stated properly: *in a general tree you must search because nothing tells you where the nodes
are; in a BST the ordering is a map.*

### With parent pointers, it is a different problem entirely

If each node knows its parent, you can walk **upwards** from both nodes, and the problem becomes finding
where two paths merge — which is the intersection of two linked lists.

```
 method 1: put p's ancestors in a set, walk up from q until you hit one    O(height) time and space
 method 2: measure both depths, advance the deeper one, then move together O(height) time, O(1) space
 method 3: the two-pointer swap — walk up from p, and when you run out,
           restart from q, and vice versa. They meet at the LCA.           O(height) time, O(1) space
```

**Method 3 is the same trick as the linked-list intersection problem** from
[day 083](../day-083-cycle-detection/README.md), and recognising that is a strong answer.

### If you have to answer many queries

One LCA is `O(n)`. A thousand LCA queries on the same tree is `O(1000n)`, and there is a much better
answer, worth naming rather than implementing:

```
 binary lifting        preprocess O(n log n), each query O(log n)
                       store, for every node, its 2^k-th ancestor
 Euler tour + sparse   preprocess O(n log n), each query O(1)
   table (RMQ)
 Tarjan's offline      O(n α(n)) for all queries at once, using union-find
```

**"For a single query, the postorder walk. For many queries on a static tree, binary lifting."** That
sentence is the complete answer to the follow-up.

---

## 4. The picture

Ponnamma's four questions, drawn.

```
                         grandfather  ← the answer
                    /        |       |       \
              son A       son B    son C    son D
              (no, no)   (yes, no) (no, yes) (no, no)
                            |          |
                           ...        ...
                            p          q

 son A: neither -> None
 son B: found p -> reports p upward
 son C: found q -> reports q upward
 son D: neither -> None

 at the grandfather: TWO children returned something  ->  the grandfather is the LCA
```

And the case where the answer is deeper:

```
                         grandfather
                    /        |       |       \
              son A       son B    son C    son D
                          (yes, yes)
                             |
                          uncle X  ← the real answer is somewhere in here
                          /      \
                        p         q

 only ONE child returned something -> pass it upward unchanged,
 because the split happened further down, inside son B's line.
```

The three meanings of the return value:

```
 return value      means
 --------------    ---------------------------------------------------
 None              neither p nor q is anywhere below me
 p (or q)          I found exactly one of them, and no split below me
 some other node   that node is the LCA, found below me — pass it up

 ONE return value, THREE meanings. That overloading is why the code is
 six lines and why it is hard to derive from scratch.
```

The general tree traced, on the standard example:

```
            3
          /   \
        5      1
       / \    / \
      6   2  0   8
         / \
        7   4

 lca(3, p=5, q=1):

   lca(5, ...)  -> node IS p  -> return 5           (stop; do not look inside)
   lca(1, ...)  -> node IS q  -> return 1
   both non-None -> return 3                        ANSWER: 3

 lca(3, p=5, q=4):

   lca(5, ...)  -> node IS p  -> return 5           (4 is below, but we stop —
                                                     correct BECAUSE both are
                                                     guaranteed to exist)
   lca(1, ...)  -> None
   only left non-None -> return 5                   ANSWER: 5
```

The BST version, which needs no search:

```
            6
          /   \
        2      8
       / \    / \
      0   4  7   9
         / \
        3   5

 lca_bst(p=2, q=8):
   at 6:  2 < 6 and 8 > 6  ->  they SPLIT  ->  answer is 6

 lca_bst(p=2, q=4):
   at 6:  both < 6         ->  go left
   at 2:  p IS this node   ->  answer is 2

 lca_bst(p=3, q=5):
   at 6:  both < 6         ->  go left
   at 2:  both > 2         ->  go right
   at 4:  3 < 4 and 5 > 4  ->  SPLIT  ->  answer is 4

 three comparisons, no recursion, O(1) space.
```

---

## 5. The code, built step by step

### Step 1 — ask about the assumption

"Are both nodes guaranteed to be in the tree? And is it a plain binary tree or a search tree? Those
change the solution completely."

**Ten seconds, and both answers change the code.**

### Step 2 — the base case, which is two things at once

```python
        if node is None or node is p or node is q:
            return node
```

`None` means "ran out". `node is p` means "found one — report it upward". **Combining them into one line
is correct and it hides that there are two ideas**, so say both out loud as you write it.

Note `is`, not `==`. The problem gives you node *objects*, and values may repeat.

### Step 3 — recurse both sides unconditionally

```python
        left = lca(node.left, p, q)
        right = lca(node.right, p, q)
```

**Both, always.** You cannot short-circuit on the left result, because "found something on the left" is
exactly the case where you still need to know about the right.

### Step 4 — the two-line decision

```python
        if left and right:
            return node                     # a split: I am the answer
        return left or right                # one side, or neither
```

Say what each line means. **`left and right` is the whole algorithm**; the second line is just passing
the message up.

### Step 5 — for the BST, throw the recursion away

```python
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
```

**Say the reason for the difference**: "in a general tree I have to search, because nothing tells me
where the nodes are. In a BST the ordering tells me, so I walk down — `O(height)` time and `O(1)`
space."

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

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def lca(node: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    """LeetCode 236. General binary tree. Assumes BOTH p and q exist.

    The return value has THREE meanings, and that overloading is the whole
    trick:
      None        neither is below me
      p or q      I found exactly one, with no split below me
      other node  that is the LCA, found below me — pass it upward

    `node is p` returns immediately without looking for q. That is correct
    ONLY because both are guaranteed present: if q exists at all, it must be
    below p, so p is the answer.

    Time O(n), space O(height).
    """
    if node is None or node is p or node is q:
        return node                         # ran out, or found one
    left = lca(node.left, p, q)
    right = lca(node.right, p, q)
    if left and right:
        return node                         # they SPLIT here
    return left or right                    # one side, or neither


def lca_may_not_exist(root: TreeNode | None, p: TreeNode, q: TreeNode
                      ) -> TreeNode | None:
    """LeetCode 1644. WITHOUT the guarantee that both nodes are present.

    The plain version returns p when q is absent, which is wrong. So count
    what was actually found and check at the end. Note the count must happen
    AFTER recursing, or an early return skips the other node's tally.
    """
    found = 0

    def walk(node: TreeNode | None) -> TreeNode | None:
        nonlocal found
        if node is None:
            return None
        left = walk(node.left)
        right = walk(node.right)
        if node is p or node is q:
            found += 1
            return node                     # still report myself upward
        if left and right:
            return node
        return left or right

    answer = walk(root)
    return answer if found == 2 else None


def lca_bst(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    """LeetCode 235. Binary SEARCH tree — no searching required.

    Walk down while both targets are on the same side. The first node where
    they diverge, or where one of them IS the node, is the answer.

    The `else` covers three cases at once: p < node < q, q < node < p, and
    node being p or q itself.

    Time O(height) — 20 comparisons on a balanced million-node tree, against
    O(n) for the general version. Space O(1): no recursion at all.
    """
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node                     # the split point
    return None


def lca_bst_recursive(node: TreeNode | None, p: TreeNode, q: TreeNode
                      ) -> TreeNode | None:
    """The same, recursively. Shorter to read, O(height) space instead of O(1)."""
    if node is None:
        return None
    if p.val < node.val and q.val < node.val:
        return lca_bst_recursive(node.left, p, q)
    if p.val > node.val and q.val > node.val:
        return lca_bst_recursive(node.right, p, q)
    return node


def lca_by_paths(root: TreeNode | None, p: TreeNode, q: TreeNode
                 ) -> TreeNode | None:
    """The version people invent first: find both root-to-node paths, then
    walk them together until they diverge.

    Correct, easy to explain, and it costs O(n) EXTRA space for the two
    paths where the postorder version costs only the stack. Worth mentioning
    as the intuition and then replacing.
    """
    def path_to(node: TreeNode | None, target: TreeNode,
                trail: list[TreeNode]) -> bool:
        if node is None:
            return False
        trail.append(node)                  # choose
        if node is target:
            return True
        if path_to(node.left, target, trail) or path_to(node.right, target, trail):
            return True
        trail.pop()                         # un-choose
        return False

    path_p: list[TreeNode] = []
    path_q: list[TreeNode] = []
    if not path_to(root, p, path_p) or not path_to(root, q, path_q):
        return None                         # handles absence for free

    answer = None
    for a, b in zip(path_p, path_q):
        if a is not b:
            break
        answer = a
    return answer


def lca_with_parents(p: "ParentNode", q: "ParentNode") -> "ParentNode | None":
    """LeetCode 1650: nodes carry a parent pointer.

    This is the LINKED LIST INTERSECTION problem: walk up from p, and when
    you run out, continue from q — and vice versa. Both pointers travel
    exactly (depth_p + depth_q) steps, so they arrive together at the merge
    point.

    O(height) time, O(1) space, and no set.
    """
    a, b = p, q
    while a is not b:
        a = a.parent if a.parent else q
        b = b.parent if b.parent else p
    return a


class ParentNode:
    def __init__(self, val: int) -> None:
        self.val = val
        self.left: "ParentNode | None" = None
        self.right: "ParentNode | None" = None
        self.parent: "ParentNode | None" = None


def lca_deepest_leaves(root: TreeNode | None) -> TreeNode | None:
    """LeetCode 1123: the LCA of all the deepest leaves.

    A different use of the same postorder shape: return (depth, lca) and
    combine — if the two sides are equally deep, this node is the answer.
    """
    def walk(node: TreeNode | None) -> tuple[int, TreeNode | None]:
        if node is None:
            return 0, None
        ld, la = walk(node.left)
        rd, ra = walk(node.right)
        if ld == rd:
            return ld + 1, node             # equally deep: I am the LCA
        if ld > rd:
            return ld + 1, la
        return rd + 1, ra

    return walk(root)[1]


def find(node: TreeNode | None, value: int) -> TreeNode | None:
    if node is None:
        return None
    if node.val == value:
        return node
    return find(node.left, value) or find(node.right, value)


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
    tree = from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])

    p, q = find(tree, 5), find(tree, 1)
    print(lca(tree, p, q))                          # TreeNode(3)

    p, q = find(tree, 5), find(tree, 4)
    print(lca(tree, p, q))                          # TreeNode(5) — a node is its own ancestor

    p, q = find(tree, 7), find(tree, 4)
    print(lca(tree, p, q))                          # TreeNode(2)

    print(lca_by_paths(tree, find(tree, 7), find(tree, 8)))    # TreeNode(3)

    # the assumption, and what breaks without it
    stray = TreeNode(99)
    print(lca(tree, find(tree, 5), stray))          # TreeNode(5)   <- WRONG
    print(lca_may_not_exist(tree, find(tree, 5), stray))        # None  <- correct
    print(lca_may_not_exist(tree, find(tree, 5), find(tree, 4)))  # TreeNode(5)

    # the BST version
    bst = from_list([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    print(lca_bst(bst, find(bst, 2), find(bst, 8)))     # TreeNode(6)
    print(lca_bst(bst, find(bst, 2), find(bst, 4)))     # TreeNode(2)
    print(lca_bst(bst, find(bst, 3), find(bst, 5)))     # TreeNode(4)
    print(lca_bst_recursive(bst, find(bst, 3), find(bst, 5)))   # TreeNode(4)

    print(lca_deepest_leaves(from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])))
    # TreeNode(2)

    # parent pointers: the linked-list intersection trick
    a = ParentNode(1); b = ParentNode(2); c = ParentNode(3)
    d = ParentNode(4); e = ParentNode(5)
    a.left, a.right = b, c
    b.parent = c.parent = a
    b.left, b.right = d, e
    d.parent = e.parent = b
    print(lca_with_parents(d, c).val)               # 1
    print(lca_with_parents(d, e).val)               # 2
```

---

## 6. What it costs

### General binary tree

```
 time    O(n)        every node may have to be visited
 space   O(height)   the recursion stack
```

**`O(n)` and there is no better single-query answer for a general tree**, and the reason is worth saying:
you cannot rule out any subtree without looking in it, because nothing about a node tells you what is
below it.

The best case is much better — if both nodes are near the root, the early return stops immediately — but
the worst case is a full traversal.

### Binary search tree

```
 time    O(height)   -> O(log n) balanced, O(n) degenerate
 space   O(1)        iterative, no stack
```

```
 n = 1,000,000, balanced
   general tree version:  1,000,000 node visits, ~20 stack frames
   BST version:                  20 comparisons,   0 extra space

 a factor of 50,000 in time and unbounded in space
```

**That contrast is the answer to "why is the BST version different?"** The ordering is a map; without it
you are searching blind.

### The path-based version

```
 time    O(n)        two searches
 space   O(n)        two paths, each up to `height`, plus the stack
```

Correct and easy to explain, and it uses `O(height)` *extra* space for the paths on top of the stack. **On
a degenerate tree that is `O(n)` extra**, where the postorder version uses only the stack. It also handles
the "node may not exist" case for free, which is a genuine advantage worth mentioning.

### With parent pointers

```
 set-based        O(height) time, O(height) space
 depth-align      O(height) time, O(1) space
 two-pointer swap O(height) time, O(1) space
```

The swap version: each pointer travels `depth_p + depth_q` steps in total, so they arrive at the merge
point together. **Same as the linked-list intersection trick**, and it needs no depth computation at all.

### Many queries

```
 k queries, one at a time            O(k · n)
 binary lifting                      O(n log n) preprocess, O(log n) per query
 Euler tour + sparse table           O(n log n) preprocess, O(1) per query
 Tarjan's offline (union-find)       O((n + k) α(n)) for all of them together
```

```
 n = 100,000, k = 100,000
   naive:            10^10 operations       — will not finish
   binary lifting:   ~1.7M preprocess + 1.7M queries  ≈  3.4M — instant
```

**Know the names and the trade; you will almost never be asked to implement them.**

### The absence check

```
 lca (assumes presence)       O(n), one pass
 lca_may_not_exist            O(n), one pass, plus a counter — same complexity
 lca_by_paths                 O(n), and absence detected for free
```

**Handling absence costs nothing asymptotically**, which is worth saying: there is no reason to avoid the
safer version other than that the question usually promises presence.

---

## 7. The traps

### Trap 1 — assuming both nodes are present when they are not

```
 tree: 1 with a left child 2
 lca(tree, node_2, node_not_in_tree)  ->  TreeNode(2)
```

The standard six-line solution returns the node it found, because it stopped as soon as it saw it. There
is no error and the answer looks plausible. **Ask about the guarantee, and if it is not there, count what
you found.**

### Trap 2 — comparing values instead of identity

```python
        if node.val == p.val:               # WRONG if values can repeat
```

The problem hands you node *objects*. If two nodes share a value, `==` matches the wrong one and the
answer is silently wrong. **Use `is`.** And if the interviewer says values are unique, say that you are
relying on it.

### Trap 3 — short-circuiting the second recursive call

```python
        left = lca(node.left, p, q)
        if left:
            return left                     # WRONG — never looks right
        return lca(node.right, p, q)
```

This returns the first node found rather than the ancestor. On the standard tree with `p = 5` and
`q = 1` it returns 5 instead of 3. **Both sides must be evaluated**, because "found something on the
left" is exactly the case where the right side still matters.

### Trap 4 — forgetting that a node is its own ancestor

```python
        if node is None:
            return None                     # missing the `node is p or node is q` case
```

Then `lca(tree, 5, 4)` where 4 is below 5 returns 4 or `None` rather than 5. **The problem statements say
so explicitly** — "a node can be a descendant of itself" — and it is the case people skip when deriving
the solution.

### Trap 5 — using the BST version on a tree that is not a BST

```python
    lca_bst(general_tree, p, q)
```

It walks down comparing values, takes a wrong turn immediately, and returns `None` or a wrong node. **No
error.** Always confirm which kind of tree you have; it is the difference between `O(log n)` and `O(n)`
and between right and wrong.

### Trap 6 — the BST version with `<=` instead of `<`

```python
        if p.val <= node.val and q.val <= node.val:
            node = node.left                # WRONG when p IS the node
```

If `p` is the current node, this walks past it into the left subtree and loses the answer. The condition
must be strict, so that "one of them is this node" falls into the `else`.

### Trap 7 — recursion depth

```
 lca(chain_of_10000_nodes, p, q)
 RecursionError: maximum recursion depth exceeded
```

The general version is `O(height)` deep. The BST version is iterative and immune, which is another point
in its favour.

### Trap 8 — counting `found` before recursing

```python
        if node is p or node is q:
            found += 1
            return node                     # returns BEFORE recursing
```

In the absence-checking version, returning early means you never look below this node — so if the *other*
target is a descendant, it is never counted, and `found` stays at 1. **Recurse first, then tally**, which
is why `lca_may_not_exist` above looks different from the plain version.

---

## 8. In the interview

### How it gets asked

- The general one: *"Find the lowest common ancestor of two nodes in a binary tree."* LeetCode 236.
- The BST one, usually first: *"Same question, but it is a binary search tree."* LeetCode 235.
- The comparison: *"Why is your BST answer different?"*
- The removal of the guarantee: *"What if one of the nodes might not be in the tree?"* LeetCode 1644.
- The variation: *"Each node has a parent pointer."* LeetCode 1650.
- The scaling one: *"Now answer a hundred thousand LCA queries on the same tree."*

### What to say out loud, in the first ninety seconds

1. **Ask the two questions.** "Is it a plain binary tree or a search tree? And are both nodes guaranteed
   to be in it? Both change the solution."
2. **State the definition precisely.** "The deepest node with both of them beneath it — and a node counts
   as its own descendant, so if one is an ancestor of the other, that one is the answer."
3. **Describe the general algorithm as a question asked of each side.** "At each node I ask both subtrees:
   is either target below you? If two different children come back with something, the paths split here,
   so this node is the answer. If only one does, the answer is inside it, so I pass it up unchanged."
4. **Name the overloaded return value.** "The return value means three things: `None` for nothing found,
   one of the targets if I found exactly one, or the answer itself. That overloading is why it is six
   lines."
5. **For the BST, say why it is different.** "In a general tree I must search, because nothing tells me
   where the nodes are. In a BST the ordering is a map — I walk down while both are on the same side, and
   the first node where they split is the answer. `O(height)` time, `O(1)` space, no recursion."
6. **Give both complexities.** "General: `O(n)` time, `O(height)` space. BST: `O(height)` time, `O(1)`
   space — twenty comparisons instead of a million node visits on a balanced million-node tree."

### The follow-ups

**"Why is the BST version different?"**
"Because a BST's ordering tells you where things are, and a general binary tree's values tell you nothing.
In a general tree, to know whether `p` is in the left subtree I have to look in the left subtree — there
is no shortcut, so the worst case is visiting every node. In a BST, if both targets are smaller than the
current node, they are both in the left subtree, definitively, without looking. So I walk down from the
root while both are on the same side, and the first node where they diverge — or where one of them *is*
the node — is the answer. That makes it `O(height)` instead of `O(n)`, and `O(1)` space instead of
`O(height)`, because it is a loop rather than a recursion. On a balanced million-node tree that is about
twenty comparisons against a million visits."

**"What if one of the nodes might not be in the tree?"**
"Then the standard solution is wrong, and it is wrong silently. It returns as soon as it sees either
target, so if I ask for the LCA of a node in the tree and one that is not, it returns the first one — a
plausible-looking node that is not an ancestor of anything relevant. The fix is to **count what I actually
found** and check at the end that it was two. One detail matters there: the count has to happen *after*
recursing into both children, not before returning early — otherwise a target that is a descendant of the
other is never counted and the tally stops at one. The path-based version handles this for free, because
if the search for a node fails there is no path, so that is another reason to mention it."

**"Each node has a parent pointer. Does that change anything?"**
"Completely — it becomes the linked-list intersection problem. Walking up from each node gives two paths
that merge at the LCA, so I want the first common node of two converging lists. Three ways. Put all of
`p`'s ancestors in a set and walk up from `q` until I hit one, which is `O(height)` time and space.
Compute both depths, advance the deeper one until they are level, then move together, which is `O(1)`
space. Or the two-pointer swap: walk up from `p`, and when it runs out, continue from `q`; do the mirror
for the other pointer. Each travels `depth_p + depth_q` steps in total, so they arrive at the merge point
together — `O(1)` space and no depth computation. That last one is the same trick as finding where two
linked lists intersect."

**"Now answer a hundred thousand queries on the same tree."**
"Then a per-query `O(n)` walk is `10¹⁰` operations and will not finish, so I would preprocess. The
standard answer is **binary lifting**: for every node, store its 2⁰-th, 2¹-th, 2²-th ancestor and so on —
`O(n log n)` to build. Then a query lifts the deeper node up to the other's depth, and lifts both together
in decreasing powers of two until they are one step below the answer, which is `O(log n)` per query. For a
hundred thousand nodes and queries that is a few million operations rather than ten billion. If I need
`O(1)` per query there is the Euler tour plus a sparse table for range-minimum, and if all the queries are
known in advance there is Tarjan's offline algorithm with union-find. I would name these rather than write
one out unless you want it — the important part is recognising that the answer changes from 'walk' to
'preprocess'."

**"What does your function actually return?"**
"Three different things, which is what makes it short and hard to derive. `None` means neither target is
below me. A target node means I found exactly one of them and no split has happened below me — so I am
reporting it upward for an ancestor to use. Any other node means the answer was found below me and I am
passing it up unchanged. The whole algorithm is then two lines: if both children returned something, the
paths split here so I am the answer; otherwise pass along whichever one returned something. And the early
return when the node *is* a target is correct only because both nodes are guaranteed present — if the
other one exists at all it must be below this one, so this one is the answer."

**"Could you do it by finding both paths from the root?"**
"Yes, and it is the version most people invent first, so it is worth offering as the intuition. Find the
root-to-node path for each target, then walk the two lists together and take the last node they agree on.
It is `O(n)` time, easy to explain, and it detects a missing node for free. The cost is `O(height)` extra
space for the two paths, on top of the recursion stack — so on a skewed tree that is `O(n)` extra memory
where the postorder version uses only the stack. I would describe this one, then write the postorder
version, and say the trade."

### A model answer

Asked: *find the lowest common ancestor of these two nodes.*

> "Two questions first, because both change the answer. **Is this a plain binary tree or a binary search
> tree?** And **are both nodes guaranteed to be in the tree?**
>
> Taking the general binary tree with both nodes present. The definition is the deepest node that has both
> of them beneath it — and importantly, a node counts as a descendant of itself, so if one target is an
> ancestor of the other, that one is the answer.
>
> The way I would describe the algorithm before writing it: at every node, I ask each subtree one question
> — *is either target somewhere below you?* If **two different children** both come back with something,
> then the two targets are on opposite sides, which means the paths split exactly here, so **this node is
> the answer**. If only **one** child comes back with something, both targets are inside that child, so
> the answer is deeper and I pass what it gave me straight up. If neither does, I report nothing.
>
> That is six lines, and the reason it is hard to derive is that **the return value means three different
> things**: `None` for 'nothing below me'; one of the targets for 'I found exactly one and there was no
> split'; and any other node for 'that is the answer, found below me'. One value, three meanings.
>
> The base case combines two ideas: if the node is `None` I have run out, and if the node **is** one of the
> targets I stop and report it upward without looking further. That early return is correct **only because
> both nodes are guaranteed present** — if the other one exists anywhere, it must be below this one, so
> this one is the answer. If you remove that guarantee, this solution silently returns a node that is not
> an ancestor of anything, and the fix is to count what I actually found and return `None` unless it was
> two.
>
> One implementation detail: I compare with `is`, not `==`, because the problem hands me node objects and
> values may repeat.
>
> That is `O(n)` time — I may have to visit every node, because in a general tree nothing tells me where
> anything is — and `O(height)` space for the stack.
>
> **If it is a binary search tree, I would not search at all**, and this is the difference worth stating.
> The ordering is a map: if both targets are smaller than the current node, they are both in the left
> subtree, definitively, without looking. So I walk down from the root while they are on the same side, and
> the first node where they diverge — or where one of them *is* the node — is the answer. That is
> `O(height)` time and `O(1)` space with no recursion at all: about twenty comparisons on a balanced
> million-node tree, against a million node visits for the general version."

---

## 9. Recall card

- **LCA = the deepest node with both targets beneath it, and a node counts as its own descendant** — so if
  one is an ancestor of the other, that one is the answer. Ask two questions first: **plain tree or BST?**
  and **are both nodes guaranteed present?**
- **General tree, six lines: base case `node is None or node is p or node is q` → return it; recurse BOTH
  sides; `if left and right: return node` (they split here); else `return left or right`.** The return
  value carries **three meanings**: nothing found · exactly one target found · the answer itself. Use
  `is`, not `==` — values may repeat.
- **The early return on `node is p` is correct ONLY because both nodes are guaranteed present.** Without
  that guarantee it silently returns a non-ancestor: **count what you found and require 2**, tallying
  *after* recursing, not before an early return.
- **In a BST there is no search: walk down while both targets are on the same side, and the first split —
  or a node that IS a target — is the answer.** `O(height)` time, **`O(1)` space, no recursion** — about
  **20 comparisons against 1,000,000 node visits** on a balanced million-node tree. Use strict `<` and
  `>`, or a node that *is* a target gets walked past.
- **With parent pointers it becomes linked-list intersection** — the two-pointer swap (walk up from `p`,
  then continue from `q`, and vice versa) meets at the LCA in `O(1)` space. And for **many queries**,
  switch from walking to preprocessing: **binary lifting**, `O(n log n)` build and `O(log n)` per query —
  10¹⁰ operations becomes a few million.
