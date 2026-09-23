---
day: 110
track: dsa
title: "Building a tree from its traversals"
phase: "Trees and binary search trees"
status: written
---

# Day 110 · DSA — Building a tree from its traversals

**After today you can:** You can reconstruct a tree from preorder plus inorder, and say why postorder plus preorder fails.

**The interviewer asks it as:** *Build the tree from its preorder and inorder traversals.*

---

## 1. What this is, and why they ask it

Given two lists of the same values — the tree read in two different orders — rebuild the tree that
produced them.

Three sentences. **One traversal is never enough**: several different trees share the same preorder, so
the question always gives you two. The pair works because each list answers a different question —
**preorder tells you which node is the root, and inorder tells you where the split between the two
subtrees is** — and neither alone answers both. And the pair that does *not* work is preorder plus
postorder, because both of them say "root first" or "root last" and neither says where the boundary
falls.

They ask it because the idea is three lines and the implementation is bookkeeping, so it separates people
who can hold index ranges in their head under pressure. And because the obvious version is `O(n²)` — it
scans the inorder list to find the root every time — and the fix is a hash map built once, which is the
same "stop recomputing what you already know" move as [day 102](../day-102-height-and-diameter/README.md).

---

## 2. The story

At the seventieth-birthday function there was a photograph of about forty relatives on a long stage, and
the argument afterwards was about who was who.

Half the people in it were dead and the rest were guessing. Somebody's phone had the picture and nobody
could agree on the man third from the left in the back row.

Old Kamalam, who was the only person there over eighty, settled it, and the way she did it was what
Sridhar remembered.

She did not look at the photograph much. She said she had two things in her head from that day and either
one alone was useless, and the two together were enough.

The first was the order the photographer had called people up. He had done it by family, starting from
the eldest: he called a man, and then that man's people, and then went back and called the next man and
his people. So her first list was a chain of names in the order they were shouted.

The second was the order they were standing, left to right, which is what the photograph itself shows.

She said the calling order tells you who is senior — the first name shouted in any group is the head of
that group. And the standing order tells you where the group splits, because a man's people stood
around him, some to his left and some to his right, and everybody to his left in the picture belongs to
one side of his family and everybody to his right belongs to the other.

So she did it like this. The first name in the calling list was Ranganathan — so Ranganathan is the
senior man. Then she found Ranganathan in the standing order. Eleven people were standing to his left.
So those eleven are his one branch, and everybody after him is the other branch.

And then she said, and this is the part that made it work: those eleven people appear in the calling list
too, immediately after Ranganathan — the next eleven names. Because the photographer called a man and
then finished his people before moving on.

So she split both lists at the same time. Eleven names from each side, and she did the same thing again
inside them.

Sridhar's cousin asked whether she could do it from the calling order alone.

She said no — the calling order tells you the seniors but not where anybody stood, and there are dozens of
arrangements that would produce the same shouting. And the standing order alone tells you the arrangement
but not who is senior. Either one on its own is nothing. It is the two together.

---

## 3. The idea in plain English

Kamalam has just reconstructed a binary tree from preorder and inorder, and her explanation of why one
list is useless is the reason the problem gives you two.

- The calling order is **preorder**: root, then left subtree, then right subtree.
- The standing order is **inorder**: left subtree, then root, then right subtree.
- "The first name shouted is the head" is: **preorder[0] is the root.**
- "Everybody to his left in the picture is one branch" is: **the root's position in the inorder list
  splits it into the left and right subtrees.**
- "Those eleven appear next in the calling list" is the index bookkeeping, and it is the fiddly part.

### Why one traversal is not enough

```
   1               1
    \             /
     2           2

 preorder:  [1, 2]   and   [1, 2]      identical
 inorder:   [1, 2]   and   [2, 1]      different  ← this is what distinguishes them
 postorder: [2, 1]   and   [2, 1]      identical
```

**Two different trees, the same preorder.** So a single traversal cannot determine a tree, and any
solution that claims otherwise is wrong. (The exception: a traversal that also records the `None`s does
determine it, which is [serialisation](../day-111-serialise-a-tree/README.md).)

### What each traversal actually tells you

```
 PREORDER    root, left, right     ->  the FIRST element is the root
 POSTORDER   left, right, root     ->  the LAST element is the root
 INORDER     left, root, right     ->  finds the BOUNDARY between the subtrees
```

**Inorder is the one that locates the split, and the other two identify the root.** That is why every
working pair contains inorder, and it is the sentence that answers the follow-up.

### The algorithm

```
 1. the root is preorder[0]
 2. find the root in the inorder list; say it is at position k
 3. everything before k in inorder  =  the LEFT subtree  (k elements)
    everything after  k in inorder  =  the RIGHT subtree
 4. in preorder, the next k elements are the left subtree,
    and everything after them is the right subtree
 5. recurse on both halves
```

**Step 4 is the one to say out loud**, because it is not obvious and it is what makes the split possible
on both lists at once: preorder visits a node then finishes its *entire* left subtree before starting the
right, so the left subtree occupies a contiguous run immediately after the root.

Kamalam: *"those eleven appear in the calling list immediately after him."*

### Worked, on the standard example

```
 preorder = [3, 9, 20, 15, 7]
 inorder  = [9, 3, 15, 20, 7]

 root = preorder[0] = 3
 find 3 in inorder -> position 1
   -> left subtree has 1 element:   inorder[0:1] = [9]
   -> right subtree has 3 elements: inorder[2:5] = [15, 20, 7]
   -> in preorder: left is the next 1 element  = [9]
                   right is the rest           = [20, 15, 7]

 recurse left:  preorder [9],        inorder [9]        -> leaf 9
 recurse right: preorder [20,15,7],  inorder [15,20,7]
   root = 20, found at inorder position 1 (within that slice)
   left = [15], right = [7]

 result:      3
            /   \
           9     20
                /  \
              15    7
```

### The naive version, and why it is `O(n²)`

```python
    k = inorder.index(root_value)           # a LINEAR SCAN, at every node
```

`list.index` walks the list, so finding the root costs `O(n)` and it happens `n` times.

```
 balanced tree:   O(n log n)
 degenerate tree: O(n^2)
 n = 10,000, a chain:  ~50,000,000 operations
```

**The fix is one line**: build a dictionary from value to index, once, before starting.

```python
    position = {value: i for i, value in enumerate(inorder)}
```

Then each lookup is `O(1)` and the whole thing is `O(n)`. **This requires the values to be unique**, which
the problem guarantees and which is worth stating.

### The bookkeeping, which is the actual difficulty

Slicing the lists is easy to write and allocates a new list at every node — `O(n²)` memory and time again.
**Pass index ranges instead.**

```python
    def build(pre_start, in_start, in_end):
        ...
```

Only three parameters are needed, not four: **the preorder end is implied**, because the size of the
subtree is `in_end - in_start`.

And the one line people get wrong:

```python
        left_size = k - in_start
        right_pre_start = pre_start + 1 + left_size
```

**`pre_start + 1 + left_size`**: skip the root, then skip the entire left subtree. Getting this wrong
does not raise — it builds a wrong tree.

The cleanest version avoids the arithmetic entirely by walking preorder with a moving pointer:

```python
    index = 0                               # a cursor into preorder

    def build(in_start, in_end):
        nonlocal index
        if in_start > in_end:
            return None
        root = TreeNode(preorder[index])
        index += 1                          # consume one preorder element
        k = position[root.val]
        root.left = build(in_start, k - 1)  # LEFT FIRST — this is essential
        root.right = build(k + 1, in_end)
        return root
```

**The left recursion must come first**, because it consumes exactly the preorder elements belonging to the
left subtree, leaving the cursor at the start of the right subtree. Swap the two lines and the tree is
built from the wrong values with no error at all.

### Postorder plus inorder

Same idea, mirrored:

```
 the root is postorder[-1]  (the LAST element)
 walk postorder BACKWARDS, and build the RIGHT subtree FIRST
```

**Right first**, for exactly the same reason: walking backwards through postorder, the right subtree's
elements come immediately before the root.

### Why preorder plus postorder fails

```
   1               1
    \             /
     2           2

 preorder:  [1, 2]  and  [1, 2]      identical
 postorder: [2, 1]  and  [2, 1]      identical
```

**Two different trees, identical in both lists.** Neither traversal says where the boundary is: preorder
says "root first" and postorder says "root last", and with a single child there is no way to tell which
side it is on.

The exception is worth knowing because interviewers ask it: **if every node has zero or two children — a
full binary tree — then preorder plus postorder does determine the tree**, because the ambiguous
single-child case cannot occur. LeetCode 889 is exactly that problem.

### The BST special case

For a **binary search tree** you only need **one** traversal, because inorder is implied — it is the
sorted order of the values.

```
 preorder of a BST  ->  sort it to get the inorder  ->  reconstruct
 or, better: use the BST range property directly, in O(n)
```

**LeetCode 1008** is this, and the good solution does not sort at all: walk the preorder with a permitted
range, exactly as in [validation](../day-108-validating-a-bst/README.md), and take elements while they
fit.

---

## 4. The picture

The split, drawn on both lists at once. **This is the diagram to reproduce.**

```
 preorder = [ 3 | 9 | 20  15   7 ]
              ^   ^   ^^^^^^^^^^^
            root  |   right subtree
                  left subtree (1 element)

 inorder  = [ 9 | 3 | 15  20   7 ]
              ^    ^   ^^^^^^^^^^^
              |   root  right subtree
            left subtree

 STEP 1: the root is preorder[0] = 3
 STEP 2: find 3 in inorder -> position 1
 STEP 3: inorder splits: 1 element left, 3 elements right
 STEP 4: preorder splits at the SAME SIZES: 1 element then 3
         -> because preorder finishes the ENTIRE left subtree
            before starting the right one

 both lists are now cut into matching pieces. Recurse.
```

Kamalam's two lists:

```
 CALLING ORDER (preorder)
   Ranganathan, [his 11 people ...], [the rest ...]
   ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^
   the head     one branch, all      the other branch
                together

 STANDING ORDER (inorder)
   [11 people ...], Ranganathan, [the rest ...]
   ^^^^^^^^^^^^^^^  ^^^^^^^^^^^  ^^^^^^^^^^^^^
   to his left      him          to his right

 the SAME eleven people, in both lists, in different places.
 Finding him in the standing order tells you the number ELEVEN,
 and that number cuts the calling list too.
```

Why one list is not enough, and why preorder plus postorder is not either:

```
        1                 1
         \               /
          2             2

 preorder    [1, 2]        [1, 2]        SAME
 inorder     [1, 2]        [2, 1]        DIFFERENT  ← only this distinguishes
 postorder   [2, 1]        [2, 1]        SAME

 pre + in    -> works      (inorder disagrees)
 post + in   -> works      (inorder disagrees)
 pre + post  -> FAILS      (both agree, and the trees differ)

 the reason in one line: INORDER is the only traversal that says where the
 BOUNDARY between the two subtrees falls. The other two only say where the
 root is.
```

The cursor version, traced:

```
 preorder = [3, 9, 20, 15, 7],  index = 0
 inorder  = [9, 3, 15, 20, 7],  position = {9:0, 3:1, 15:2, 20:3, 7:4}

 build(0, 4):  root = pre[0] = 3,  index -> 1,  k = 1
   build(0, 0):  root = pre[1] = 9,  index -> 2,  k = 0
     build(0, -1) -> None
     build(1, 0)  -> None
     returns 9
   build(2, 4):  root = pre[2] = 20, index -> 3,  k = 3
     build(2, 2):  root = pre[3] = 15, index -> 4   -> leaf 15
     build(4, 4):  root = pre[4] = 7,  index -> 5   -> leaf 7
     returns 20
   returns 3

 the CURSOR only moves forward, and the LEFT call must run first —
 it consumes exactly the left subtree's preorder elements, leaving the
 cursor at the start of the right subtree.
```

---

## 5. The code, built step by step

### Step 1 — say why two traversals

"One traversal never determines a tree — a node with only a left child and a node with only a right child
have the same preorder. So the question gives two, and they do different jobs: preorder identifies the
root, and inorder locates the boundary between the subtrees."

### Step 2 — the recursive idea, before any indices

"The root is the first preorder element. Find it in inorder; everything to its left is the left subtree
and everything to its right is the right. And because preorder finishes the entire left subtree before
starting the right, the same sizes cut the preorder list too."

### Step 3 — kill the `O(n²)` before writing it

```python
    position = {value: i for i, value in enumerate(inorder)}
```

"Searching inorder for the root with `.index` is a linear scan at every node — `O(n²)` on a chain. One
dictionary, built once, makes each lookup `O(1)` and the whole thing `O(n)`. This needs the values to be
unique, which the problem guarantees."

### Step 4 — pass indices, not slices

```python
    def build(in_start, in_end):
```

"Slicing allocates a new list at every node, which puts the `O(n²)` back in memory. I pass index ranges
instead."

### Step 5 — the cursor, and the ordering rule

```python
        root = TreeNode(preorder[index])
        index += 1
        root.left = build(in_start, k - 1)      # LEFT FIRST
        root.right = build(k + 1, in_end)
```

**"The left call must come first."** It consumes exactly the preorder elements of the left subtree,
leaving the cursor pointing at the start of the right subtree. Swapping the two lines builds a wrong tree
silently.

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


def build_from_pre_in(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    """LeetCode 105. Preorder + inorder -> the unique tree.

    WHY TWO LISTS: preorder says which node is the ROOT; inorder says where
    the BOUNDARY between the subtrees is. Neither alone answers both, and a
    single traversal never determines a tree.

    THE KEY STEP: preorder finishes the ENTIRE left subtree before starting
    the right, so the size found in inorder cuts the preorder list too.

    O(n) time and O(n) space, thanks to the position map. Without it,
    `inorder.index(...)` makes it O(n^2) on a skewed tree.

    Requires UNIQUE values — say so.
    """
    position = {value: i for i, value in enumerate(inorder)}
    index = 0                               # a cursor into preorder

    def build(in_start: int, in_end: int) -> TreeNode | None:
        nonlocal index
        if in_start > in_end:
            return None
        root = TreeNode(preorder[index])
        index += 1                          # consume one preorder element
        k = position[root.val]
        root.left = build(in_start, k - 1)  # LEFT FIRST — essential
        root.right = build(k + 1, in_end)
        return root

    return build(0, len(inorder) - 1)


def build_from_pre_in_explicit(preorder: list[int],
                               inorder: list[int]) -> TreeNode | None:
    """The same, with the preorder index computed rather than carried.

    The line people get wrong is `pre_start + 1 + left_size`: skip the root,
    then skip the WHOLE left subtree. Getting it wrong builds a wrong tree
    with no error.
    """
    position = {value: i for i, value in enumerate(inorder)}

    def build(pre_start: int, in_start: int, in_end: int) -> TreeNode | None:
        if in_start > in_end:
            return None
        root = TreeNode(preorder[pre_start])
        k = position[root.val]
        left_size = k - in_start
        root.left = build(pre_start + 1, in_start, k - 1)
        root.right = build(pre_start + 1 + left_size, k + 1, in_end)
        return root

    return build(0, 0, len(inorder) - 1)


def build_from_post_in(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    """LeetCode 106. Postorder + inorder. The mirror image.

    The root is the LAST postorder element, so walk postorder BACKWARDS —
    and build the RIGHT subtree FIRST, because going backwards the right
    subtree's elements come immediately before the root.
    """
    position = {value: i for i, value in enumerate(inorder)}
    index = len(postorder) - 1              # a cursor, moving BACKWARDS

    def build(in_start: int, in_end: int) -> TreeNode | None:
        nonlocal index
        if in_start > in_end:
            return None
        root = TreeNode(postorder[index])
        index -= 1
        k = position[root.val]
        root.right = build(k + 1, in_end)   # RIGHT FIRST — the mirror of above
        root.left = build(in_start, k - 1)
        return root

    return build(0, len(inorder) - 1)


def build_from_pre_post(preorder: list[int],
                        postorder: list[int]) -> TreeNode | None:
    """LeetCode 889. Preorder + postorder — which is AMBIGUOUS in general.

    It works ONLY for a FULL binary tree (every node has 0 or 2 children),
    because the ambiguous single-child case cannot occur. For any other tree
    this returns ONE valid answer among several.

    The trick: preorder[index + 1] is the root of the left subtree; find it
    in postorder to learn the left subtree's size.
    """
    position = {value: i for i, value in enumerate(postorder)}
    index = 0

    def build(post_start: int, post_end: int) -> TreeNode | None:
        nonlocal index
        if post_start > post_end:
            return None
        root = TreeNode(preorder[index])
        index += 1
        if post_start == post_end:
            return root                     # a leaf
        left_root_pos = position[preorder[index]]
        root.left = build(post_start, left_root_pos)
        root.right = build(left_root_pos + 1, post_end - 1)
        return root

    return build(0, len(postorder) - 1)


def build_bst_from_preorder(preorder: list[int]) -> TreeNode | None:
    """LeetCode 1008. For a BST, ONE traversal is enough.

    Inorder is implied — it is the sorted order — so no second list is
    needed. And you do not have to sort: walk the preorder with a permitted
    RANGE, exactly like validation, taking elements while they fit.

    O(n) time, O(height) space. Each element is consumed exactly once.
    """
    index = 0

    def build(low: float, high: float) -> TreeNode | None:
        nonlocal index
        if index >= len(preorder):
            return None
        value = preorder[index]
        if not (low < value < high):
            return None                     # belongs to an ancestor's other side
        index += 1
        node = TreeNode(value)
        node.left = build(low, value)
        node.right = build(value, high)
        return node

    return build(float("-inf"), float("inf"))


def build_naive(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    """The O(n^2) version, written out so you can time it.

    `inorder.index(...)` is a linear scan, done once per node, and slicing
    allocates a new pair of lists at every node.
    """
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    k = inorder.index(preorder[0])          # O(n) scan, at EVERY node
    root.left = build_naive(preorder[1:k + 1], inorder[:k])
    root.right = build_naive(preorder[k + 1:], inorder[k + 1:])
    return root


def preorder_of(node: TreeNode | None, out: list[int] | None = None) -> list[int]:
    out = [] if out is None else out
    if node:
        out.append(node.val); preorder_of(node.left, out); preorder_of(node.right, out)
    return out


def inorder_of(node: TreeNode | None, out: list[int] | None = None) -> list[int]:
    out = [] if out is None else out
    if node:
        inorder_of(node.left, out); out.append(node.val); inorder_of(node.right, out)
    return out


def postorder_of(node: TreeNode | None, out: list[int] | None = None) -> list[int]:
    out = [] if out is None else out
    if node:
        postorder_of(node.left, out); postorder_of(node.right, out); out.append(node.val)
    return out


def to_list(root: TreeNode | None) -> list[int | None]:
    if root is None:
        return []
    out: list[int | None] = []
    queue: deque[TreeNode | None] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None); continue
        out.append(node.val); queue.append(node.left); queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    pre = [3, 9, 20, 15, 7]
    ino = [9, 3, 15, 20, 7]
    post = [9, 15, 7, 20, 3]

    tree = build_from_pre_in(pre, ino)
    print(to_list(tree))                    # [3, 9, 20, None, None, 15, 7]
    print(preorder_of(tree) == pre and inorder_of(tree) == ino)      # True

    print(to_list(build_from_pre_in_explicit(pre, ino)) == to_list(tree))   # True
    print(to_list(build_from_post_in(ino, post)) == to_list(tree))          # True

    # WHY ONE TRAVERSAL IS NOT ENOUGH
    left_only = TreeNode(1, TreeNode(2))
    right_only = TreeNode(1, None, TreeNode(2))
    print(preorder_of(left_only), preorder_of(right_only))          # [1,2] [1,2] — same
    print(inorder_of(left_only), inorder_of(right_only))            # [2,1] [1,2] — DIFFER
    print(postorder_of(left_only), postorder_of(right_only))        # [2,1] [2,1] — same

    # so pre + post is ambiguous, and the two trees are indistinguishable
    print(preorder_of(left_only) == preorder_of(right_only)
          and postorder_of(left_only) == postorder_of(right_only))  # True

    # ...but it works for a FULL binary tree
    full = build_from_pre_post([1, 2, 4, 5, 3, 6, 7], [4, 5, 2, 6, 7, 3, 1])
    print(to_list(full))                    # [1, 2, 3, 4, 5, 6, 7]

    # a BST needs only ONE traversal
    bst = build_bst_from_preorder([8, 5, 1, 7, 10, 12])
    print(inorder_of(bst))                  # [1, 5, 7, 8, 10, 12] — sorted
    print(preorder_of(bst))                 # [8, 5, 1, 7, 10, 12] — round trips

    # edge cases
    print(to_list(build_from_pre_in([], [])))               # []
    print(to_list(build_from_pre_in([1], [1])))             # [1]

    # a skewed tree — the O(n^2) case
    n = 2000
    skew_pre = list(range(n))
    skew_in = list(range(n))
    import time
    t = time.perf_counter(); build_from_pre_in(skew_pre, skew_in)
    fast = time.perf_counter() - t
    t = time.perf_counter(); build_naive(skew_pre, skew_in)
    slow = time.perf_counter() - t
    print(f"O(n) {fast:.4f}s vs naive {slow:.4f}s  ({slow / fast:.0f}x)")
```

---

## 6. What it costs

### The two implementations

```
 with a position map, index ranges:
   time    O(n)        each node created once, each lookup O(1)
   space   O(n)        the map, plus O(height) stack

 naive (index + slicing):
   time    O(n^2)      an O(n) scan and O(n) slicing, at every node
   space   O(n^2)      new lists allocated at every node
```

```
 n = 2,000, a skewed tree
   O(n):     ~2,000 operations          instant
   naive:    ~4,000,000 + allocations   noticeably slow

 n = 10,000, skewed
   naive:    ~100,000,000               seconds
```

**The measurement is in the code above** — run it rather than taking the ratio on trust.

### Where each cost comes from

```
 inorder.index(root)   O(n) per node   ->  O(n^2) total on a chain
 preorder[1:k+1]       O(k) per node   ->  O(n^2) total, and the same again in memory
 position map          O(n) once       ->  O(1) per node
 index ranges          O(1) per node   ->  no allocation at all
```

**Two separate `O(n²)`s, and both are removed by the same two changes.**

### Space, honestly

```
 the position map      n entries       ~50 bytes each in Python  ->  ~500 KB at n = 10,000
 the recursion stack   O(height)
 the output tree       n nodes         unavoidable
```

The map is `O(n)` extra space that the naive version does not use — so this is a genuine time-for-space
trade, and it is overwhelmingly worth it. **Say it as a trade rather than as a free win.**

### The BST version

```
 preorder of a BST, range-based:  O(n) time, O(height) space, no map at all
 sort-then-reconstruct:           O(n log n) time
```

**Half the work and no map**, because the ordering supplies the inorder for free. Worth knowing that the
sort version exists and is worse.

### Recursion depth

```
 a skewed tree of 10,000 nodes:
   RecursionError: maximum recursion depth exceeded
```

Same as every tree problem, and this one is particularly exposed because the input that makes it slow —
a chain — is the same input that overflows.

---

## 7. The traps

### Trap 1 — claiming one traversal is enough

```python
    def build(preorder): ...
```

A node with only a left child and a node with only a right child both give preorder `[1, 2]`. **No single
traversal determines a tree**, unless it also records the `None`s.

### Trap 2 — recursing right before left with the cursor version

```python
        root.right = build(k + 1, in_end)   # WRONG ORDER
        root.left = build(in_start, k - 1)
```

The cursor consumes preorder elements in order, so the right call takes the elements that belong to the
left subtree. **The tree is built from the wrong values and nothing raises** — the output is a valid tree
with the values scrambled.

### Trap 3 — `pre_start + left_size` instead of `pre_start + 1 + left_size`

```python
        root.right = build(pre_start + left_size, k + 1, in_end)     # missing the +1
```

Off by one: the right subtree starts one element too early, so it re-uses the last element of the left
subtree. **A wrong tree, no error.** Say the formula in words as you write it: *skip the root, then skip
the whole left subtree.*

### Trap 4 — the `O(n²)` scan

```python
    k = inorder.index(preorder[0])
```

Correct, and quadratic on a skewed tree. **One dictionary comprehension removes it.** This is what the
interviewer means by "can you do better".

### Trap 5 — slicing instead of passing indices

```python
    build(preorder[1:k + 1], inorder[:k])
```

Correct, and it allocates two new lists at every node — `O(n²)` time *and* memory. Even with the position
map, slicing keeps the quadratic behaviour, so **both fixes are needed**.

### Trap 6 — assuming values are unique when they might not be

```python
    position = {value: i for i, value in enumerate(inorder)}
```

With duplicates, the map keeps only the last occurrence and the reconstruction picks the wrong split
point. **More fundamentally, duplicates make the answer ambiguous** — there may be several valid trees.
LeetCode guarantees uniqueness; **say that you are relying on it.**

### Trap 7 — trying preorder plus postorder in general

```python
    build_from_pre_post([1, 2], [2, 1])
```

Returns *a* valid tree, and there are two. **It is only unique for a full binary tree**, where every node
has zero or two children. Presenting it as a general solution is wrong.

### Trap 8 — not validating that the inputs are consistent

If the two lists are not actually traversals of the same tree — different lengths, or a value in one and
not the other — the code either raises a `KeyError` from the position map or builds nonsense. In an
interview it is enough to **state the assumption**; in real code you would check the lengths and the
multiset of values first.

---

## 8. In the interview

### How it gets asked

- The main one: *"Build the tree from its preorder and inorder traversals."* LeetCode 105.
- The mirror: *"Now from inorder and postorder."* LeetCode 106.
- The trap question: *"Could you do it from preorder and postorder?"*
- The optimisation: *"Your solution is `O(n²)`. Can you make it linear?"*
- The special case: *"What if it is a BST? How many traversals do you need?"*

### What to say out loud, in the first ninety seconds

1. **Say why there are two lists.** "One traversal never determines a tree — a node with only a left child
   and one with only a right child have the same preorder. So the two lists do different jobs."
2. **Say what each one does.** "**Preorder identifies the root** — it is the first element. **Inorder
   locates the boundary** — the root's position in it splits the remaining values into the left and right
   subtrees."
3. **Give the step that is not obvious.** "And because preorder finishes the *entire* left subtree before
   starting the right, the size I learn from inorder cuts the preorder list in the same place."
4. **Kill the quadratic version before writing it.** "The obvious implementation searches inorder for the
   root at every node, which is `O(n²)` on a skewed tree. I build a value-to-index map once, so each
   lookup is `O(1)`."
5. **Say you will pass indices.** "And I pass index ranges rather than slicing, because slicing allocates
   a new pair of lists at every node and puts the quadratic behaviour back."
6. **Flag the ordering rule.** "I keep a cursor into the preorder list, and the left recursion must happen
   before the right — it consumes exactly the left subtree's elements and leaves the cursor at the start of
   the right."

### The follow-ups

**"Could you do it from preorder and postorder?"**
"Not in general, and the counter-example is small: a root with only a left child and a root with only a
right child have preorder `[1, 2]` and postorder `[2, 1]` — **both lists identical, two different trees**.
The reason is structural rather than incidental: preorder says the root is first, postorder says it is
last, and **neither says where the boundary between the subtrees falls**. Inorder is the only traversal
that locates that boundary, which is why every working pair contains it. There is one exception worth
knowing: if the tree is **full** — every node has zero or two children — then the ambiguous single-child
case cannot arise and preorder plus postorder does determine the tree. That is LeetCode 889, and the trick
is that the element right after the root in preorder is the left subtree's root, so finding it in postorder
gives you the left subtree's size."

**"Your solution is `O(n²)`. Make it linear."**
"There are two separate quadratic costs and both need fixing. The first is **finding the root in the
inorder list** — `inorder.index(...)` is a linear scan done once per node, so `O(n²)` on a chain. I build a
dictionary from value to index once, before starting, and every lookup becomes `O(1)`. The second is
**slicing**: passing `preorder[1:k+1]` allocates a new list at every node, which is quadratic in time and
memory even with the map. So I pass **index ranges** instead and never copy anything. Together those make
it `O(n)` time and `O(n)` space for the map. The trade to state honestly: the map is `O(n)` extra memory
the naive version does not use, and it is obviously worth it. And the map requires the values to be
**unique**, which the problem guarantees."

**"What if it is a binary search tree?"**
"Then **one traversal is enough**, because inorder is implied — it is just the sorted order of the values.
So given the preorder of a BST I could sort it to obtain the inorder and run the same algorithm, which is
`O(n log n)`. But there is a better way that does not sort at all: walk the preorder list once with a
**permitted range**, exactly like validating a BST. The current element becomes a node only if it falls
inside the range; otherwise it belongs to some ancestor's other side and I return. That consumes each
element exactly once, so it is `O(n)` time and `O(height)` space with no map. That is LeetCode 1008."

**"Do it from inorder and postorder."**
"The same idea mirrored. The root is now the **last** postorder element rather than the first preorder one,
so I walk postorder **backwards** with a cursor moving down. And critically I build the **right subtree
first**, because going backwards through postorder the right subtree's elements are the ones immediately
before the root. Everything else — the position map, the index ranges, the split at the root's inorder
position — is identical. If I built left first, the cursor would hand the right subtree's values to the
left, and the result would be a valid-looking tree with the values in the wrong places and no error."

**"What breaks if the values are not unique?"**
"Two things, and the second is more fundamental. The **implementation** breaks, because the position map
keeps only one index per value, so finding 'the' root in the inorder list picks an arbitrary occurrence and
splits in the wrong place. But even with a perfect implementation, **the answer becomes ambiguous** —
with repeated values there can be several distinct trees producing the same pair of traversals, so there is
no unique tree to return. That is why the problem guarantees distinct values, and it is worth stating the
assumption rather than silently relying on it."

**"How would you verify your answer?"**
"Round-trip it: traverse the tree I just built in preorder and in inorder, and check that both match the
inputs exactly. That is `O(n)` and it catches every class of bug here — the swapped recursion order, the
off-by-one in the preorder index, and a wrong split point — because all of them produce a tree whose
traversals differ from the inputs. I would write that check first, before the reconstruction, because
without it a wrong tree is very hard to spot by eye."

### A model answer

Asked: *build the tree from its preorder and inorder traversals.*

> "First, why the question gives me two lists. **One traversal never determines a tree.** A root with only
> a left child and a root with only a right child both have the preorder `[1, 2]` — same list, different
> trees. So a single traversal is not enough, and the two I am given do different jobs.
>
> **Preorder tells me which node is the root**: it is the first element, because preorder visits the root
> before anything else. **Inorder tells me where the boundary is**: once I know the root, its position in
> the inorder list splits everything else into the values that are in the left subtree and the values that
> are in the right.
>
> And then the step that is not obvious, which is what makes both lists usable at once: **preorder finishes
> the entire left subtree before it starts the right one.** So if inorder tells me the left subtree has
> eleven values, then in preorder the eleven elements immediately after the root are exactly those eleven,
> and everything after them is the right subtree. One number cuts both lists.
>
> That is the algorithm: take the root from preorder, find it in inorder, split both lists at the matching
> sizes, recurse.
>
> The straightforward implementation of that is `O(n²)`, and I would rather say so than have you point it
> out. Two costs. Searching the inorder list for the root is a linear scan done once per node — quadratic
> on a skewed tree. And slicing the lists allocates a new pair at every node, which is quadratic again, in
> memory as well as time. So: I build a **value-to-index dictionary** once at the start, which makes each
> lookup constant, and I **pass index ranges** rather than slices, so nothing is copied. That is `O(n)`
> time and `O(n)` space for the map — a real trade, and clearly the right one.
>
> The version I would write keeps a **cursor** into the preorder list rather than computing preorder
> offsets by arithmetic, because the arithmetic — skip the root, then skip the whole left subtree — is
> where the off-by-one lives. With a cursor, the rule to be careful about is that the **left recursion must
> run before the right**: it consumes exactly the left subtree's preorder elements and leaves the cursor
> sitting at the start of the right subtree. Swap those two lines and you get a perfectly valid tree built
> from the wrong values, with nothing raised.
>
> Two things I would add. This assumes the **values are unique** — with duplicates the map is wrong and,
> more importantly, the answer is genuinely ambiguous. And if you asked whether I could do it from
> **preorder and postorder** instead, the answer is no in general: both of those say where the root is and
> neither says where the boundary falls, so those same two one-child trees are indistinguishable. It works
> only if the tree is full."

---

## 9. Recall card

- **One traversal NEVER determines a tree** — a left-only and a right-only child both give preorder
  `[1, 2]`. The two lists do different jobs: **preorder identifies the ROOT (first element); inorder
  locates the BOUNDARY between the subtrees.**
- **The non-obvious step: preorder finishes the ENTIRE left subtree before starting the right**, so the
  size learned from inorder cuts the preorder list at the same place. One number splits both lists.
- **Two separate `O(n²)`s, and both must be fixed: `inorder.index()` (a scan per node) → a value-to-index
  map built once; and SLICING (a new list per node) → pass INDEX RANGES.** Together: `O(n)` time, `O(n)`
  space. Requires **unique values** — say so.
- **With a cursor into preorder, the LEFT recursion must run first** — it consumes exactly the left
  subtree's elements. Swapping the lines builds a valid tree from the wrong values, silently. For
  **postorder + inorder**, mirror it: root is the **last** element, walk **backwards**, and build the
  **RIGHT** subtree first.
- **Preorder + postorder is AMBIGUOUS** — both say where the root is, neither says where the boundary is —
  **except for a full binary tree** (every node has 0 or 2 children). And **a BST needs only ONE
  traversal**, because inorder is implied by the ordering: walk the preorder with a permitted **range**,
  `O(n)` and no map. Verify any answer by **round-tripping** both traversals.
