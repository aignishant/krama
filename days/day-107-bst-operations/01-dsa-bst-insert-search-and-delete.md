---
day: 107
track: dsa
title: "BST insert, search, and delete"
phase: "Trees and binary search trees"
status: written
---

# Day 107 · DSA — BST insert, search, and delete

**After today you can:** You can delete a node with two children and explain the successor swap.

**The interviewer asks it as:** *Delete this node from the BST. It has two children.*

---

## 1. What this is, and why they ask it

Three operations on a binary search tree. **Search** walks down comparing. **Insert** walks down to where
the value belongs and puts a leaf there. **Delete** is the hard one, and it is the whole lesson.

Three sentences. Search and insert are four lines each and nobody gets them wrong. Delete has **three
cases** — no children, one child, two children — and the third one cannot simply remove the node, because
something has to occupy that position and almost nothing may. And the value that may is **the node's
inorder neighbour**: the smallest value in its right subtree, or the largest in its left. There is no
other choice, and being able to say *why* there is no other choice is what the question is for.

They ask it because it is the first tree operation that **modifies structure**, and modifying a
pointer-based structure with recursion has a specific idiom — `node.left = delete(node.left, key)` — that
people either know or fight against for ten minutes. And because "delete a node with two children" has a
one-sentence answer that most candidates arrive at by trial and error rather than by reasoning.

---

## 2. The story

The photographs were on the long shelf in the front room and there were nineteen of them, in order, from
the oldest at the left end to the newest at the right.

Sarojini had put them in that order in 1998 and had been maintaining it ever since. It was not decorative
— it was how she found things. If somebody asked which year her brother-in-law's daughter got married,
she went to roughly the middle and worked outwards, and she never had to look at more than four or five.

In March, one of them — the wedding group from 1974, in the heavy black frame — had to go to the man in
the market to have the glass replaced.

That left a gap in the middle of the shelf, and Sarojini's daughter-in-law, trying to be helpful, closed
the gap by sliding everything after it one place to the left.

Sarojini was not pleased, and her objection was not about tidiness. She said: now the whole right half of
the shelf has moved. Everything I knew about where things were is wrong. For one photograph.

What she did instead, the next time a frame went away — and it happened twice a year — was to move
exactly one photograph into the gap, and choose it carefully.

Her rule was that it had to be the picture that had been **immediately next to it in time**. Either the
one just before it or the one just after it. Nothing else would do.

Her daughter-in-law asked why not just take one from the end, since the end was easy to reach.

Sarojini said: because then the end one would be sitting in the middle, and everything to its left would
be older and everything to its right would be older too, and the shelf would stop meaning anything. The
only picture that can sit in that gap is one that was already touching it, because that is the only one
with nothing between it and the gap.

Then she said the part that took her a while to work out, years ago.

When you move the one from just after, that leaves a gap where **it** was. But that is a much easier gap,
because a photograph at the very start of a run has nothing before it — there is at most one side to
worry about. So you never have this problem twice. The second gap always closes by itself, or by sliding
one thing.

They did it that way for years, and the shelf stayed readable through about thirty repairs.

---

## 3. The idea in plain English

Sarojini has derived BST deletion, including the reason the successor is the only candidate and the
reason the second removal is easy.

- The shelf in date order is the BST, with **inorder** as the order on the shelf.
- Removing a frame is deleting a node.
- Sliding everything along is what a sorted array does — `O(n)` — and it is what a BST avoids.
- "It has to be the one immediately next to it in time" is the **inorder successor or predecessor**.
- "The second gap is easier" is the fact that **the successor has no left child**, so the second deletion
  is never the hard case.

### Search and insert: the easy half

```python
    def search(node, target):
        while node:
            if target == node.val:
                return node
            node = node.left if target < node.val else node.right
        return None
```

```python
    def insert(node, value):
        if node is None:
            return TreeNode(value)          # this is where it BELONGS
        if value < node.val:
            node.left = insert(node.left, value)
        elif value > node.val:
            node.right = insert(node.right, value)
        return node                         # unchanged, but reattached
```

**The idiom to learn is `node.left = insert(node.left, value)`.** The recursive call returns the
(possibly new) subtree root, and the caller reattaches it. That single pattern is how you modify a
pointer-based structure recursively without needing parent pointers, and it is exactly what delete needs
too.

**A new value always becomes a leaf.** You never insert into the middle — you walk until you fall off the
bottom, and that is where it goes.

### Delete: three cases

**Case 1 — no children.** Remove it. Return `None` to the parent, which reattaches `None`.

**Case 2 — one child.** The child takes its place. Return the child; the parent reattaches it. Both
sub-cases — only-left and only-right — are the same line if you write it right.

**Case 3 — two children.** You cannot just remove it, because two subtrees need a parent and there is one
slot. **So do not remove the node — replace its value, and then delete the node you took the value
from.**

```python
        successor = minimum(node.right)     # the smallest thing bigger than me
        node.val = successor.val            # overwrite the value
        node.right = delete(node.right, successor.val)   # now delete THAT node
```

### Why the successor, and why nothing else

This is the part to be able to argue rather than recite.

The tree must remain a BST, so whatever ends up in this position must be **larger than everything in the
left subtree and smaller than everything in the right subtree**. How many values satisfy both?

```
        deleted node's position
             /            \
   left subtree        right subtree
   (all smaller)       (all larger)

 the replacement must be > every value on the left AND < every value on the right.

 the largest value on the left  = the PREDECESSOR
 the smallest value on the right = the SUCCESSOR

 those two are the only values in the whole tree with nothing between them
 and the gap. Anything else has some other value strictly between it and
 the gap, and that value would end up on the wrong side.
```

**There are exactly two candidates, and they are the inorder neighbours.** Sarojini's rule.

Using the successor by convention, though the predecessor is equally valid; and **always using the same
one makes the tree lean over time**, which real implementations alternate to avoid.

### Why the second deletion is easy

The successor is the **minimum** of the right subtree, so it is as far left as you can go — which means
**it has no left child**. So deleting it is case 1 or case 2, never case 3.

**The recursion cannot nest more than one level deep.** That is Sarojini's "you never have this problem
twice", and it is worth stating, because it looks like the code might recurse forever.

### The reattachment idiom, which is the real skill

```python
    def delete(node, key):
        if node is None:
            return None
        if key < node.val:
            node.left = delete(node.left, key)      # REATTACH
        elif key > node.val:
            node.right = delete(node.right, key)    # REATTACH
        else:
            ...                                     # found it: the three cases
        return node
```

**Every recursive call's result is assigned back into the parent's pointer.** That is what makes
structural modification work without parent pointers, and it is why the function returns a node rather
than nothing.

**Deleting the root is handled for free** by this shape, because the top-level caller does
`root = delete(root, key)`. A version that returns nothing cannot delete the root, which is trap 3.

### The alternative: lazy deletion

Real systems often do not remove the node at all. They mark it deleted and leave it in place.

```
 + O(height) with no restructuring, and no pointer surgery at all
 + safe when other things hold references to nodes
 - the tree grows with tombstones and must be rebuilt periodically
 - search must skip deleted nodes
```

**Worth naming.** It is what many databases and indexes actually do — the *tombstone* idea from
[day 011](../day-011-insert-and-delete/README.md) — and it is a good answer to "how would you do this in
production?"

### Successor, in general

Finding the inorder successor of an arbitrary node is a separate small problem worth knowing:

```
 if the node has a right subtree   -> the minimum of that subtree
 if it does not                    -> the lowest ancestor for which this node
                                      is in the LEFT subtree
```

Without parent pointers, the second case is found on the way down from the root: remember the last node
where you turned left.

---

## 4. The picture

The three deletion cases.

```
 CASE 1 — no children (delete 3)

        10                    10
       /  \                  /  \
      5    15      -->      5    15
     / \                     \
    3   7                     7          return None to the parent


 CASE 2 — one child (delete 5)

        10                    10
       /  \                  /  \
      5    15      -->      7    15
       \
        7                                return the child; the parent reattaches it


 CASE 3 — two children (delete 10)

        10                    12                     the successor of 10
       /  \                  /  \                    is min(right subtree) = 12
      5    15      -->      5    15
     / \   / \             / \     \                 copy 12 into the node,
    3   7 12  18          3   7     18               then delete 12 from the right

                                                     12 had NO LEFT CHILD
                                                     (it is a minimum), so the
                                                     second delete is case 1 or 2
```

Why only two values can fill the gap:

```
                        [ GAP ]
                      /         \
          left subtree           right subtree
          3  5  7                12  15  18
                ^                ^
          predecessor         successor

 inorder:  3  5  7  [GAP]  12  15  18

 the value in the gap must be > 7 and < 12.
 Look at the sorted order: the ONLY values with nothing between them and
 the gap are 7 and 12. Put 15 there and 12 would be to its left — broken.
```

The reattachment idiom, drawn:

```
 delete(root, 5)  on   10
                      /  \
                     5    15
                      \
                       7

 delete(10, 5):  5 < 10  ->  node.left = delete(node.left, 5)
                                        │
                         delete(5, 5):  │ found. one child (7).
                                        │ return 7
                                        ▼
                 node.left = 7

 result:   10
          /  \
         7    15

 the ASSIGNMENT is what rewires the tree. Without it, delete(node.left, 5)
 computes the right answer and throws it away.
```

The successor-only lean, which is why implementations alternate:

```
 always taking the successor pulls values from the RIGHT subtree,
 so the right side shrinks faster over many deletions:

 after 1,000 random insert/delete pairs, always using the successor:
   observed height drift upward, and a left-leaning shape

 real implementations alternate successor and predecessor,
 or pick based on which subtree is taller.
```

---

## 5. The code, built step by step

### Step 1 — write the reattachment shape first

```python
    def delete(node, key):
        if node is None:
            return None
        if key < node.val:
            node.left = delete(node.left, key)
        elif key > node.val:
            node.right = delete(node.right, key)
        else:
            ...
        return node
```

**Write this frame before thinking about the cases.** The assignments are the whole mechanism, and
`return node` at the end is what keeps unchanged subtrees attached.

### Step 2 — the two easy cases, as one line each

```python
            if node.left is None:
                return node.right           # covers "no children" too: returns None
            if node.right is None:
                return node.left
```

**Two lines cover three situations**, because "no children" means `node.right` is also `None`, so the
first line returns `None`, which is exactly right.

### Step 3 — the two-child case, and say why

```python
            successor = node.right
            while successor.left:
                successor = successor.left  # the minimum of the right subtree
            node.val = successor.val
            node.right = delete(node.right, successor.val)
```

Say the argument as you write it: *"The replacement must be larger than everything on the left and
smaller than everything on the right. Exactly two values satisfy that — the largest on the left and the
smallest on the right. I will take the smallest on the right."*

### Step 4 — say why it does not recurse forever

"The successor is a minimum, so it has no left child, so deleting it is case one or case two. The
recursion goes at most one level deeper."

**Say this unprompted.** It is the question the interviewer was about to ask.

### Step 5 — assign at the top level

```python
    root = delete(root, 10)
```

**Deleting the root only works if the caller reassigns.** A `delete` that returns nothing cannot remove
the root, and that is the first test case anyone runs.

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


def search(root: TreeNode | None, target: int) -> TreeNode | None:
    """O(height), O(1) space. Iterative: there is nothing to combine going up."""
    node = root
    while node:
        if target == node.val:
            return node
        node = node.left if target < node.val else node.right
    return None


def insert(node: TreeNode | None, value: int) -> TreeNode:
    """LeetCode 701. A new value ALWAYS becomes a leaf — walk until you fall
    off the bottom, and that is where it belongs.

    The idiom `node.left = insert(node.left, value)` is the whole technique:
    the call returns the (possibly new) subtree root and the caller reattaches
    it. That is how you restructure a pointer tree without parent pointers.
    """
    if node is None:
        return TreeNode(value)
    if value < node.val:
        node.left = insert(node.left, value)
    elif value > node.val:
        node.right = insert(node.right, value)
    return node                             # unchanged, but reattached


def insert_iterative(root: TreeNode | None, value: int) -> TreeNode:
    """The same, without recursion. O(1) space."""
    if root is None:
        return TreeNode(value)
    node = root
    while True:
        if value < node.val:
            if node.left is None:
                node.left = TreeNode(value)
                return root
            node = node.left
        elif value > node.val:
            if node.right is None:
                node.right = TreeNode(value)
                return root
            node = node.right
        else:
            return root                     # duplicate: ignored


def minimum(node: TreeNode) -> TreeNode:
    while node.left:
        node = node.left
    return node


def maximum(node: TreeNode) -> TreeNode:
    while node.right:
        node = node.right
    return node


def delete(node: TreeNode | None, key: int) -> TreeNode | None:
    """LeetCode 450. THREE cases, and the third is the lesson.

    WHY the successor and nothing else: the value that replaces this node
    must be larger than EVERY value in the left subtree and smaller than
    EVERY value in the right subtree. Exactly two values in the whole tree
    satisfy that — the largest on the left (the predecessor) and the
    smallest on the right (the successor). Anything else has some value
    strictly between it and the gap, which would then be on the wrong side.

    WHY it does not recurse forever: the successor is a MINIMUM, so it has
    no left child, so deleting it is case 1 or case 2. At most one extra
    level.

    The caller must write `root = delete(root, key)`, or deleting the root
    does nothing.
    """
    if node is None:
        return None

    if key < node.val:
        node.left = delete(node.left, key)          # REATTACH
    elif key > node.val:
        node.right = delete(node.right, key)        # REATTACH
    else:
        # found it
        if node.left is None:
            return node.right               # covers no-children (returns None)
        if node.right is None:
            return node.left
        successor = minimum(node.right)     # smallest value bigger than me
        node.val = successor.val            # overwrite the VALUE, keep the node
        node.right = delete(node.right, successor.val)

    return node


def delete_using_predecessor(node: TreeNode | None, key: int) -> TreeNode | None:
    """The mirror image, and equally correct. Always using ONE of the two
    makes the tree lean over many deletions, so real implementations
    alternate, or pick based on which subtree is taller."""
    if node is None:
        return None
    if key < node.val:
        node.left = delete_using_predecessor(node.left, key)
    elif key > node.val:
        node.right = delete_using_predecessor(node.right, key)
    else:
        if node.right is None:
            return node.left
        if node.left is None:
            return node.right
        predecessor = maximum(node.left)    # largest value smaller than me
        node.val = predecessor.val
        node.left = delete_using_predecessor(node.left, predecessor.val)
    return node


def delete_iterative(root: TreeNode | None, key: int) -> TreeNode | None:
    """Without recursion, which means tracking the parent by hand — and that
    is exactly the bookkeeping the reattachment idiom removes. Written out
    so the contrast is visible."""
    parent: TreeNode | None = None
    node = root
    while node and node.val != key:
        parent = node
        node = node.left if key < node.val else node.right
    if node is None:
        return root                         # not found

    if node.left and node.right:            # case 3: reduce to case 1 or 2
        succ_parent, succ = node, node.right
        while succ.left:
            succ_parent, succ = succ, succ.left
        node.val = succ.val
        parent, node = succ_parent, succ    # now delete `succ` instead

    child = node.left or node.right         # case 1 or 2
    if parent is None:
        return child                        # deleting the root
    if parent.left is node:
        parent.left = child
    else:
        parent.right = child
    return root


class LazyBST:
    """Lazy deletion: mark, do not remove. What many real indexes do.

    O(height) with no pointer surgery, safe when other code holds node
    references — at the cost of tombstones accumulating, so the tree must be
    rebuilt when they dominate.
    """

    class Node:
        def __init__(self, val: int) -> None:
            self.val = val
            self.deleted = False
            self.left: "LazyBST.Node | None" = None
            self.right: "LazyBST.Node | None" = None

    def __init__(self) -> None:
        self.root: "LazyBST.Node | None" = None
        self.live = 0
        self.tombstones = 0

    def add(self, value: int) -> None:
        if self.root is None:
            self.root = self.Node(value)
            self.live += 1
            return
        node = self.root
        while True:
            if value == node.val:
                if node.deleted:
                    node.deleted = False    # resurrect
                    self.tombstones -= 1
                    self.live += 1
                return
            side = "left" if value < node.val else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, self.Node(value))
                self.live += 1
                return
            node = child

    def remove(self, value: int) -> bool:
        node = self.root
        while node:
            if value == node.val:
                if node.deleted:
                    return False
                node.deleted = True
                self.tombstones += 1
                self.live -= 1
                return True
            node = node.left if value < node.val else node.right
        return False

    def contains(self, value: int) -> bool:
        node = self.root
        while node:
            if value == node.val:
                return not node.deleted
            node = node.left if value < node.val else node.right
        return False

    def should_rebuild(self) -> bool:
        return self.tombstones > self.live      # more dead than alive


def successor_of(root: TreeNode | None, target: int) -> TreeNode | None:
    """The inorder successor of a value, without parent pointers.

    If the node has a right subtree, it is that subtree's minimum.
    Otherwise it is the lowest ancestor from which we turned LEFT — which is
    found on the way down by remembering the last left turn.
    """
    best: TreeNode | None = None
    node = root
    while node:
        if target < node.val:
            best = node                     # a candidate: remember the left turn
            node = node.left
        else:
            node = node.right
    return best


def inorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        walk(node.left)
        out.append(node.val)
        walk(node.right)

    walk(root)
    return out


def is_bst(root: TreeNode | None) -> bool:
    values = inorder(root)
    return all(a < b for a, b in zip(values, values[1:]))


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
    root = from_list([10, 5, 15, 3, 7, 12, 18])
    print(inorder(root))                    # [3, 5, 7, 10, 12, 15, 18]

    # case 1: a leaf
    root = delete(root, 3)
    print(inorder(root), is_bst(root))      # [5, 7, 10, 12, 15, 18] True

    # case 2: one child
    root = delete(root, 5)
    print(inorder(root), is_bst(root))      # [7, 10, 12, 15, 18] True

    # case 3: two children — and it is the ROOT
    root = delete(root, 10)
    print(inorder(root), is_bst(root))      # [7, 12, 15, 18] True
    print(root)                             # TreeNode(12)  <- the successor took over

    # the predecessor version gives a different tree, equally valid
    a = from_list([10, 5, 15, 3, 7, 12, 18])
    b = from_list([10, 5, 15, 3, 7, 12, 18])
    a = delete(a, 10)
    b = delete_using_predecessor(b, 10)
    print(a.val, b.val)                     # 12 7
    print(inorder(a) == inorder(b), is_bst(a), is_bst(b))   # True True True

    # iterative delete agrees
    c = from_list([10, 5, 15, 3, 7, 12, 18])
    c = delete_iterative(c, 10)
    print(inorder(c), is_bst(c))            # [3, 5, 7, 12, 15, 18] True

    # deleting the last node, and a missing key
    single = TreeNode(1)
    print(delete(single, 1))                # None
    print(inorder(delete(from_list([2, 1, 3]), 99)))        # [1, 2, 3]

    print(successor_of(from_list([10, 5, 15, 3, 7, 12, 18]), 7))    # TreeNode(10)
    print(successor_of(from_list([10, 5, 15, 3, 7, 12, 18]), 18))   # None

    # lazy deletion
    lazy = LazyBST()
    for v in (10, 5, 15, 3, 7):
        lazy.add(v)
    lazy.remove(5)
    print(lazy.contains(5), lazy.contains(7))               # False True
    print(lazy.live, lazy.tombstones, lazy.should_rebuild())    # 4 1 False
```

---

## 6. What it costs

### The three operations

```
 search   O(height)   one comparison per level
 insert   O(height)   walk down, attach a leaf
 delete   O(height)   walk down, plus at most one walk to a minimum
```

**Delete's extra walk does not change the complexity.** Finding the successor is a walk down the right
subtree, which is at most `height` more steps, so the total is still `O(height)`.

```
 balanced, n = 1,000,000     ~20 steps for all three
 degenerate, n = 1,000,000   ~1,000,000
```

### Space

```
 recursive insert/delete   O(height) stack
 iterative versions        O(1)
```

**The iterative delete is `O(1)` space and needs explicit parent tracking**, which is exactly the
bookkeeping the reattachment idiom removes. Worth showing both and saying that the recursive one is
shorter *because* the assignment does the parent's work.

### Against a sorted array

This is the comparison that justifies the structure:

```
                        search      insert          delete
 sorted array           O(log n)    O(n)            O(n)
 balanced BST           O(log n)    O(log n)        O(log n)
```

```
 n = 1,000,000, deleting one element
   sorted array:  up to 1,000,000 element moves   ~1 ms of memory traffic
   balanced BST:  ~20 comparisons + 2 pointer writes
```

**Sarojini's daughter-in-law sliding the whole shelf.** Same answer, `O(n)` versus `O(log n)` work.

### The successor lean

```
 always taking the successor, 100,000 random insert/delete pairs
   -> the tree drifts left-leaning; measured height grows a few levels
      above the balanced ideal

 alternating successor and predecessor
   -> the drift largely cancels
```

**It does not change the complexity class** — an unbalanced BST is already `O(n)` in the worst case — but
it is a real, measurable effect and it is why textbook implementations alternate.

### Lazy deletion

```
 delete           O(height), no restructuring
 search           O(height), plus skipping tombstones
 space            grows: tombstones are never freed until a rebuild
 rebuild          O(n), triggered when tombstones exceed live nodes
```

```
 1,000,000 live nodes + 1,000,000 tombstones
   memory:  240 MB instead of 120 MB
   height:  unchanged, but every operation walks past dead nodes
```

**The rebuild threshold is the design decision**, and "when tombstones outnumber live nodes" is the
standard rule.

### Why none of this is `O(log n)` without balance

```
 insert 1..n in order, then delete anything
   height = n - 1
   every operation = O(n)
   and a recursive delete on a 10,000-node chain:
     RecursionError: maximum recursion depth exceeded
```

**All three operations inherit the balance problem**, which is
[day 109](../day-109-balanced-trees/README.md).

---

## 7. The traps

### Trap 1 — not reattaching the result

```python
        if key < node.val:
            delete(node.left, key)          # result thrown away
```

The recursion computes the correct new subtree and nobody stores it. **The tree is unchanged and there is
no error** — the function returns and the value is still there.

```
 delete(root, 5); inorder(root)  ->  5 is still present
```

**Assign every recursive call's result.** That is the idiom.

### Trap 2 — replacing with an arbitrary node

```python
            node.val = maximum(node.right).val       # WRONG
```

Taking the *largest* of the right subtree instead of the smallest. The tree is left broken:

```
 delete 10 from [10, 5, 15, 3, 7, 12, 18] using max(right) = 18
   -> 18 in the middle, with 12 and 15 in its right subtree
   -> inorder: 3, 5, 7, 18, 12, 15   — not sorted
```

**Only the two inorder neighbours work.** Anything else has a value strictly between it and the gap.

### Trap 3 — a `delete` that returns nothing

```python
    def delete(node, key) -> None:
        ...
```

Then deleting the root is impossible, because the caller's `root` variable still points at the old node.
**The function must return the new subtree root and the caller must write `root = delete(root, key)`.**

### Trap 4 — deleting the successor by value when duplicates exist

```python
            node.right = delete(node.right, successor.val)
```

If duplicates are allowed and the right subtree contains two copies of the successor's value, this may
delete the wrong one. **With the counting-node convention from
[day 106](../day-106-bst-property/README.md) this cannot happen**, which is another reason to prefer it.
Say the assumption.

### Trap 5 — the one-child case written as two separate branches badly

```python
            if node.left is None and node.right is None:
                return None
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
```

Correct, and the first branch is redundant: `return node.right` already returns `None` when there are no
children. **Three cases collapse into two lines**, and noticing that is a small, real signal.

### Trap 6 — forgetting that the value moved but the node did not

```python
            node.val = successor.val
```

The **node object stays**; only its value changed. If anything outside held a reference to that node
expecting a particular value, it is now wrong. In an interview this does not matter; in real code it is
exactly why lazy deletion or genuine node-splicing is used instead.

### Trap 7 — searching for the successor from the root

```python
            successor = minimum(root.right)          # from the ROOT, not the node
```

A copy-paste slip that produces a value from the wrong subtree entirely. **`minimum(node.right)`** — the
right subtree of the node being deleted.

### Trap 8 — recursion on a deep tree

```
 delete(chain_of_10000_nodes, 5000)
 RecursionError: maximum recursion depth exceeded
```

Same as every tree operation. The iterative version is immune and costs the explicit parent tracking.

---

## 8. In the interview

### How it gets asked

- The main one: *"Delete a node from a BST."* LeetCode 450, and they will hand you a node with two
  children.
- The probe, immediately: *"Why the successor? Why not any other node?"*
- The follow-up: *"Could you have used the predecessor instead?"*
- The worry: *"Does that recursive delete inside delete terminate?"*
- The practical one: *"How would a real database do this?"*

### What to say out loud, in the first ninety seconds

1. **Name the three cases before writing.** "Three cases: no children, one child, two children. The first
   two are one line each; the third is the actual problem."
2. **State the reattachment idiom.** "I write `node.left = delete(node.left, key)` — every recursive call
   returns the new subtree root and the caller reattaches it. That is what lets me restructure the tree
   without parent pointers, and it is what makes deleting the root work."
3. **Derive the successor rather than asserting it.** "For the two-child case, whatever ends up in this
   position must be larger than everything in the left subtree and smaller than everything in the right.
   Exactly two values in the tree satisfy that: the largest on the left and the smallest on the right —
   the inorder neighbours. Anything else has a value strictly between it and the gap."
4. **Say the trick.** "So I do not remove the node. I copy the successor's value into it and then delete
   the successor from the right subtree."
5. **Pre-empt the termination worry.** "That inner delete is easy, because the successor is a minimum, so
   it has no left child — case one or case two. The recursion goes at most one level deeper."
6. **Give the complexity and the caveat.** "`O(height)` for all three, so `O(log n)` if balanced and
   `O(n)` on a chain. Nothing here balances the tree."

### The follow-ups

**"Why the successor? Why not any other node?"**
"Because the position has a constraint that almost nothing satisfies. Whatever sits there must be larger
than **every** value in the left subtree and smaller than **every** value in the right subtree. Look at
the inorder sequence: the deleted node's slot has the left subtree entirely before it and the right
subtree entirely after it, so the only values with nothing between them and that slot are the two
immediate neighbours — the largest on the left and the smallest on the right. Pick anything else, say the
maximum of the right subtree, and there are values in the right subtree smaller than it, which would now
be on its left and larger than a node above them — the tree stops being a BST and inorder stops being
sorted. So there are exactly two legal choices and I take one of them."

**"Could you have used the predecessor instead?"**
"Yes, and it is exactly as correct — the largest value in the left subtree. The resulting tree is
different but equally valid, and the inorder sequence is identical either way. The reason it is worth
mentioning is that **always** using one of them makes the tree lean: taking the successor repeatedly pulls
values out of the right subtree, so over many deletions the right side shrinks and the tree drifts. Real
implementations alternate, or choose based on which subtree is taller, which also helps balance. It does
not change the complexity class, since a plain BST is already `O(n)` in the worst case, but it is a
measurable effect."

**"Does the recursive delete inside delete terminate?"**
"Yes, and it goes at most one extra level. The successor is the **minimum** of the right subtree, so by
definition it is as far left as you can go, which means it has **no left child**. Deleting a node with no
left child is case one or case two — return its right child, or `None` — so the inner call finds it and
returns immediately. There is no way to hit the two-child case twice in a row. I would say that
unprompted, because the code does look like it might nest."

**"How would a real database do this?"**
"Usually **not this way.** Two differences. First, database indexes are **B-trees** rather than binary
trees — high branching factor so each node fills a disk page — and deletion there is about merging
underfull pages rather than swapping a value. Second, and more relevant here, most real systems use
**lazy deletion**: mark the entry deleted and leave it in place, then rebuild or compact when the
tombstones outnumber the live entries. That is `O(height)` with no pointer surgery at all, it is safe when
other code holds references to nodes, and it turns many small restructurings into one big periodic one.
The cost is that the structure grows with dead entries and every search walks past them, so the rebuild
threshold — commonly 'when tombstones exceed live nodes' — becomes a real tuning decision."

**"Write it iteratively."**
"It is the same three cases, and the difference is that I now have to track the **parent** by hand,
because there is no return value being reattached. So: walk down remembering the parent; if the node has
two children, find the successor and its parent, copy the value, and then retarget the deletion at the
successor — which reduces it to the one-child or no-child case; then splice by setting the parent's left
or right pointer to the surviving child. The special case is that if there is no parent, I was deleting
the root, so I return the child instead. Writing both makes the point that the recursive version's
`node.left = delete(...)` is not stylistic — it is doing the parent bookkeeping for me."

**"What is the complexity, and what would you say about it?"**
"`O(height)` for all three operations, and `O(1)` extra space if written iteratively, `O(height)` if
recursively. Delete does one extra walk to find the successor, which is at most another `height` steps, so
it does not change the class. And the caveat I would give before being asked: `O(height)` is `O(log n)`
only if the tree is balanced, and nothing in insert or delete does anything to balance it — in fact
repeated deletion using only the successor actively makes it worse. Inserting sorted data gives a chain
where all three operations are `O(n)`, and a recursive delete on a ten-thousand-node chain raises
`RecursionError`."

### A model answer

Asked: *delete this node from the BST — it has two children.*

> "Let me do the three cases in order, because the third is the only interesting one.
>
> If the node has **no children**, remove it — return `None` to the parent. If it has **one child**, the
> child takes its place — return the child. Those two collapse into two lines, because 'return
> `node.right`' already returns `None` when there is no right child either.
>
> The **two-child** case is the real question, and I want to derive it rather than assert it. Whatever
> ends up in that position has to be larger than **every** value in the left subtree and smaller than
> **every** value in the right subtree. Now look at the inorder sequence: the left subtree comes entirely
> before this slot and the right subtree entirely after it. So the only values in the whole tree with
> nothing between them and the slot are the **immediate neighbours** — the largest value on the left and
> the smallest value on the right. Those are the inorder predecessor and successor, and there are exactly
> two legal choices. Anything else has some value strictly between it and the gap, and that value would
> end up on the wrong side.
>
> So I do not remove the node at all. I find the **successor** — the minimum of the right subtree, which
> is as far left as you can go from `node.right` — copy its value into this node, and then delete the
> successor from the right subtree.
>
> And that second deletion is guaranteed easy, which is worth saying before you ask: the successor is a
> minimum, so it **has no left child**, so removing it is case one or case two. The recursion can never
> hit the two-child case twice in a row.
>
> The mechanism that makes all of this work in a pointer tree is the idiom `node.left = delete(node.left,
> key)` — every recursive call returns the new root of that subtree and the caller reassigns it. That is
> how you restructure without parent pointers, and it is also why the top-level call has to be `root =
> delete(root, key)`: without that, deleting the root does nothing at all.
>
> Complexity is `O(height)` — the walk down, plus at most one more walk to find the minimum — so `O(log
> n)` on a balanced tree and `O(n)` on a chain. Compare that with a sorted array, where deleting one
> element moves up to a million others.
>
> Two things I would add. **The predecessor works equally well**, and always using the same side makes the
> tree lean over many deletions, so real implementations alternate. And in production, most systems do
> **lazy deletion** instead — mark it deleted, leave it in place, and rebuild when the tombstones outnumber
> the live nodes — because that avoids pointer surgery entirely and is safe when other code holds
> references."

---

## 9. Recall card

- **The idiom is the technique: `node.left = delete(node.left, key)`.** Every recursive call returns the
  new subtree root and the caller **reattaches** it — that is how you restructure without parent pointers,
  and it is why the top level must be `root = delete(root, key)` or **deleting the root silently does
  nothing**. Forgetting the assignment leaves the tree unchanged, with no error.
- **Three cases, two lines: `if node.left is None: return node.right` covers both "no children" and
  "only right"; then `if node.right is None: return node.left`.**
- **Two children: there are EXACTLY TWO legal replacements — the inorder neighbours.** The value must be
  greater than *all* of the left subtree and less than *all* of the right, and only the largest-on-the-left
  and smallest-on-the-right qualify. Copy the **successor's value** into the node, then **delete the
  successor from the right subtree**.
- **That inner delete goes at most one level deeper**, because a minimum **has no left child** — so it is
  always case 1 or case 2. Say this unprompted. And **the predecessor is equally valid**; always using one
  side makes the tree lean, so real implementations alternate.
- **All three are `O(height)`** — `O(log n)` balanced, `O(n)` on a chain, and nothing here balances
  anything. Against a sorted array: **`O(log n)` versus up to a million element moves** for one deletion.
  In production, prefer **lazy deletion** — mark a tombstone, rebuild when tombstones outnumber live nodes
  — which needs no pointer surgery and is safe when others hold node references.
