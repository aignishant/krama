---
day: 103
track: dsa
title: "Same tree, symmetric tree, and subtree"
phase: "Trees and binary search trees"
status: written
---

# Day 103 · DSA — Same tree, symmetric tree, and subtree

**After today you can:** You can compare two trees structurally and handle the null cases without crashing.

**The interviewer asks it as:** *Are these two trees identical? Is this tree a subtree of that one?*

---

## 1. What this is, and why they ask it

Three problems that share one idea: a recursion that walks **two trees at once**, in step, comparing as
it goes.

Three sentences. Everything so far has recursed on one tree; today the function takes two nodes and asks
whether the subtrees below them match. That change makes the **base cases** the whole difficulty — there
are three of them, not two, and the one people forget is *"exactly one of them is `None`"*. And once you
have the two-tree walk, symmetry is the same function with the arguments crossed over, and "is this a
subtree" is that function called at every node of the bigger tree.

They ask it because it is the cleanest test of null-handling in the whole topic. Almost every wrong
answer here is a crash, not a wrong result — and the crash is always the same one, on the same line. It
is also where candidates first meet a problem whose obvious `O(n × m)` solution has a much better answer
if you are willing to change representation, which is the serialisation trick at the end.

---

## 2. The story

Kamala had been embroidering for thirty-one years and the shop sent her the work that needed checking,
because she was quick and she did not miss things.

Three jobs came on the same Thursday and they were three different kinds of looking.

The first was a pair of pillow covers that were supposed to be identical. Two pieces, same design, one
for each side of the bed. She did not look at them as pictures — she put them next to each other and
went through them together, stitch group by stitch group, in the same order on both. Flower here, flower
there, same colour, same size. Move on. The moment two things did not match she stopped, because there
was no point continuing.

The second was a table runner with a border that was meant to be a mirror. Whatever was on the left of
the middle was supposed to be reflected on the right. This one she did differently, and she was
particular about it. She did not compare the left half with the left half. She put her left thumb at the
outermost point of the left side and her right thumb at the outermost point of the right side, and
walked them **towards each other** at the same speed. The far left against the far right. Then the next
one in from each side. That is what mirror means, she said — it is not the same order, it is the
opposite order.

The third took her most of the afternoon. A large bedspread had come back from a customer who said a
particular motif on it was wrong. She had the correct motif on a small square in her hand, about the
size of a postcard, and she had to find whether that exact thing appeared anywhere in a bedspread the
size of a door.

There was no clever way. She went across the bedspread, and at every place a motif started, she held the
small square against it and checked the whole thing, stitch by stitch. Most of them failed on the first
or second stitch and she moved on in a second. Two of them looked promising and she had to go all the
way through before finding a difference.

She said afterwards that the third job was the same as the first job, done many times over.

And she made one point about the third that mattered. When she found a place where the motif started
correctly, she had to check that it matched **completely** — all of it, right down to the last stitch,
with nothing extra hanging off the bottom. A motif that matched for most of the way and then continued
into something else was not the motif.

---

## 3. The idea in plain English

Kamala's three jobs are LeetCode 100, 101 and 572, and her method for each is the algorithm.

### Same tree: walk two trees in step

The recursion takes **two nodes** instead of one:

```python
    def is_same(a, b):
        if a is None and b is None:
            return True                     # both ran out together
        if a is None or b is None:
            return False                    # one ran out first
        return (a.val == b.val
                and is_same(a.left, b.left)
                and is_same(a.right, b.right))
```

**Three base cases, and the middle one is the whole lesson.**

```
 both None      -> True    two empty subtrees are the same
 one None       -> False   different SHAPE, so they cannot match
 neither None   -> compare the values, then both pairs of children
```

The `or` case is the one people leave out, and leaving it out does not give a wrong answer — it gives:

```
 AttributeError: 'NoneType' object has no attribute 'val'
```

because the next line reads `a.val` when `a` is `None`.

**Order matters in the `and` chain.** Python short-circuits, so `a.val == b.val` is only evaluated after
both null checks have passed, and the recursive calls are only made if the values match. That is
Kamala stopping the moment two things did not match.

### Symmetric tree: the same function, with the arguments crossed

A tree is **symmetric** if its left subtree is a mirror image of its right subtree. The trap is that
"mirror" is not "same".

```python
    def is_mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (a.val == b.val
                and is_mirror(a.left, b.right)      # LEFT against RIGHT
                and is_mirror(a.right, b.left))     # RIGHT against LEFT
```

**One line different from `is_same`: the children are crossed.** `a.left` is compared with `b.right`,
not with `b.left`.

That is Kamala's thumbs walking towards each other. The outermost on the left matches the outermost on
the right, not the innermost.

The common wrong answer:

```python
    return is_same(root.left, root.right)           # WRONG
```

This says the two halves are *identical*, not mirrored — which is a different property. On this tree:

```
        1
       / \
      2   2
       \    \
        3    3

 is_same(left, right)  -> True     (both halves are identical)
 is_symmetric          -> False    (a mirror would need 3 on the OUTSIDE of one side)
```

**Identical halves are a translation; symmetric halves are a reflection.** They coincide only when each
half is itself symmetric.

### Subtree: the same function, called everywhere

```python
    def is_subtree(big, small):
        if small is None:
            return True
        if big is None:
            return False
        return (is_same(big, small)
                or is_subtree(big.left, small)
                or is_subtree(big.right, small))
```

At every node of the big tree, ask "does the small tree match starting here?" — Kamala holding the
square against every place a motif starts.

**The word "subtree" is stricter than it sounds**, and this is the trap. A subtree means **a node and
*everything* below it** — you cannot stop partway.

```
 big:      1              small:    1
          / \                      /
         2   3                    2

 is_subtree -> FALSE
```

The `1` in the big tree has a right child; the `1` in the small tree does not. `is_same` correctly
returns `False` at the `or` base case. This is "nothing extra hanging off the bottom".

### The `O(n × m)` problem, and the trick

`is_subtree` calls `is_same` at every node, and each call can walk the whole small tree, so the worst
case is `O(n × m)`.

The trick: **serialise both trees to strings and ask whether one string contains the other.** Then
`str.find` does the work in `O(n + m)`.

Two details make it correct, and both are the point of the exercise:

```
 1. include the NULLS, or different trees serialise the same way
       preorder of  1->2  (left child)   is "1,2"
       preorder of  1->2  (right child)  is "1,2"     <- same string, different trees
       with nulls:  "1,2,#,#,#"   vs   "1,#,2,#,#"    <- now distinct

 2. put a DELIMITER before every value, or numbers merge
       tree containing 12 serialises to "...,12,..."
       tree containing  2 serialises to "...,2,..."
       "2" is a substring of "12"  ->  a FALSE MATCH
       fix: use ",12," and ",2," — the commas make the boundary explicit
```

**Both of those are silent wrong answers**, not crashes, which is why they are worth knowing.

The honest complexity: `str.find` in CPython is not a naive scan, but the guaranteed-linear version needs
a proper string-matching algorithm. **Say `O(n + m)` with KMP, and note that the built-in is usually fine
in practice.**

### The shape all three share

```python
    def compare(a, b):
        if a is None and b is None: return True
        if a is None or b is None:  return False
        return a.val == b.val and compare(...) and compare(...)
```

**Write those three lines first, every time.** Then decide what goes in the two recursive calls: straight
for `is_same`, crossed for `is_mirror`. That is the whole family.

---

## 4. The picture

Same against mirror, which is the distinction the day turns on.

```
 IS_SAME(a, b) compares:               IS_MIRROR(a, b) compares:

      a         b                           a         b
     / \       / \                         / \       / \
    L   R     L'  R'                      L   R     L'  R'

    L with L'   (left with left)          L with R'   (left with RIGHT)
    R with R'   (right with right)        R with L'   (right with LEFT)

         │ │                                    ╲   ╱
         │ │   parallel                          ╲ ╱   crossed
         │ │                                     ╱ ╲
```

Kamala's two methods, drawn:

```
 PILLOW COVERS (same)              TABLE RUNNER BORDER (mirror)

 piece 1: A B C D                  left half:  A B C  │  C B A  :right half
 piece 2: A B C D                              →  →   │   ←  ←
          ↓ ↓ ↓ ↓                              thumbs walk TOWARDS each other
          same order, both                     outermost against outermost
```

A tree that is symmetric, and one that is not but has identical halves:

```
 SYMMETRIC                          IDENTICAL HALVES, NOT SYMMETRIC

        1                                     1
      /   \                                 /   \
     2     2                               2     2
    / \   / \                               \     \
   3   4 4   3                               3     3

 left half:  2(3,4)                  left half:  2(_,3)
 right half: 2(4,3)                  right half: 2(_,3)
 -> mirrored ✓                       -> identical, but a mirror would need
                                        the right half to be 2(3,_)
 is_symmetric -> True                 is_same(left, right) -> True   ← the trap
                                      is_symmetric        -> False
```

Why "subtree" is strict:

```
 BIG                     SMALL                  is_subtree?

    1                      1                    NO
   / \                    /                     the 1 in BIG has a right child;
  2   3                  2                      the 1 in SMALL does not.
                                                A subtree is a node AND EVERYTHING
                                                below it — nothing extra allowed.

    1                      2                    YES
   / \                                          node 2 and everything below it
  2   3                                         (which is nothing) matches.
```

The serialisation traps, both of them:

```
 TRAP 1 — no null markers

   tree A:  1            tree B:  1
           /                       \
          2                         2

   preorder without nulls:  "1,2"   and   "1,2"     ← identical strings!
   preorder with nulls:     "1,2,#,#,#"  vs  "1,#,2,#,#"   ← distinct ✓

 TRAP 2 — no delimiters

   big  contains ... 12 ...   ->  serialises with "12"
   small is        2          ->  serialises with "2"
   "2" in "12"  ->  TRUE      ← a match that does not exist

   fix: emit ",12," and ",2,"  ->  ",2," is not in ",12,"  ✓
```

---

## 5. The code, built step by step

### Step 1 — write the three base cases before anything else

```python
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
```

**Two lines, always, in that order.** The `and` case first, then the `or` case. After those two lines
both `a` and `b` are guaranteed non-`None`, so every line below can dereference freely.

Say it out loud: *"both empty is a match; one empty is a mismatch of shape; after that both exist."*

### Step 2 — compare the value, then recurse

```python
        return (a.val == b.val
                and is_same(a.left, b.left)
                and is_same(a.right, b.right))
```

The `and` short-circuits, so a value mismatch stops immediately and neither subtree is walked. That is
not an optimisation you add — it is what `and` already does, and it is why this is fast on the common
case.

### Step 3 — symmetry is the same function with the arguments crossed

```python
        return (a.val == b.val
                and is_mirror(a.left, b.right)
                and is_mirror(a.right, b.left))
```

**Write `is_same` first, then copy it and cross the arguments.** Do not try to write `is_mirror` from
scratch; the whole point is that it is one change.

And the entry point:

```python
    def is_symmetric(root):
        return root is None or is_mirror(root.left, root.right)
```

An empty tree is symmetric. A single node is symmetric, because `is_mirror(None, None)` is `True`.

### Step 4 — subtree is `is_same` called at every node

```python
        return (is_same(big, small)
                or is_subtree(big.left, small)
                or is_subtree(big.right, small))
```

Note the base cases here are **not** the same as `is_same`'s:

```python
        if small is None:
            return True                     # an empty tree is a subtree of anything
        if big is None:
            return False                    # ran out of big tree, small is not empty
```

**The asymmetry is deliberate**, and getting it backwards is trap 5 below.

### Step 5 — the serialisation version, with both fixes

```python
        return f",{node.val}," if leaf else ...
```

Emit a delimiter around every value, and a marker for every `None`. Then:

```python
        return serialise(small) in serialise(big)
```

**Say both fixes out loud as you write them**: "nulls, so different shapes give different strings;
delimiters, so 2 does not match inside 12."

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


def is_same(a: TreeNode | None, b: TreeNode | None) -> bool:
    """LeetCode 100. Two trees, walked in step.

    THREE base cases, and the middle one is what everyone forgets:
      both None      -> True   (ran out together)
      exactly one    -> False  (different shape)
      neither        -> compare values, then both pairs of children

    Omitting the `or` line does not give a wrong answer — it gives
    AttributeError: 'NoneType' object has no attribute 'val'.

    Time O(min(n, m)) — `and` short-circuits at the first difference.
    Space O(min(height))
    """
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (a.val == b.val
            and is_same(a.left, b.left)
            and is_same(a.right, b.right))


def is_mirror(a: TreeNode | None, b: TreeNode | None) -> bool:
    """is_same with the arguments CROSSED. That is the only difference.

    left against RIGHT, right against LEFT — the outermost of one side
    matched with the outermost of the other.
    """
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (a.val == b.val
            and is_mirror(a.left, b.right)      # crossed
            and is_mirror(a.right, b.left))     # crossed


def is_symmetric(root: TreeNode | None) -> bool:
    """LeetCode 101. An empty tree is symmetric; so is a single node.

    NOT is_same(root.left, root.right) — that tests whether the halves are
    IDENTICAL, which is a translation, not a reflection.
    """
    return root is None or is_mirror(root.left, root.right)


def is_symmetric_iterative(root: TreeNode | None) -> bool:
    """The same, with a queue holding PAIRS. Useful when the tree may be
    deep enough to overflow the stack."""
    if root is None:
        return True
    queue = deque([(root.left, root.right)])
    while queue:
        a, b = queue.popleft()
        if a is None and b is None:
            continue
        if a is None or b is None:
            return False
        if a.val != b.val:
            return False
        queue.append((a.left, b.right))     # crossed
        queue.append((a.right, b.left))     # crossed
    return True


def is_subtree(big: TreeNode | None, small: TreeNode | None) -> bool:
    """LeetCode 572. is_same, tried at every node of the big tree.

    NOTE the base cases differ from is_same's, and deliberately:
      small is None -> True   (an empty tree is a subtree of anything)
      big is None   -> False  (ran out of tree, and small is not empty)

    "Subtree" means a node AND EVERYTHING below it. A match that continues
    into extra nodes is not a match.

    Time O(n × m) worst case. See is_subtree_by_string for O(n + m).
    """
    if small is None:
        return True
    if big is None:
        return False
    return (is_same(big, small)
            or is_subtree(big.left, small)
            or is_subtree(big.right, small))


def serialise(node: TreeNode | None) -> str:
    """Preorder with TWO essential details.

    1. NULL MARKERS, or different trees serialise identically:
         1 with a left child   -> "1,2"      without markers
         1 with a right child  -> "1,2"      ... the same string.
    2. DELIMITERS around every value, or numbers merge:
         a tree containing 12 gives "...12..."
         searching for a tree containing 2 finds "2" inside "12"
         -> a false match. ",2," is not inside ",12,".
    """
    if node is None:
        return ",#"
    return f",{node.val}" + serialise(node.left) + serialise(node.right)


def is_subtree_by_string(big: TreeNode | None, small: TreeNode | None) -> bool:
    """O(n + m) with a linear substring search, instead of O(n × m).

    CPython's `in` is not a naive scan, but the guaranteed-linear version
    needs KMP. Say "O(n + m) with KMP" rather than claiming it for `in`.
    """
    if small is None:
        return True
    return serialise(small) in serialise(big)


def invert(node: TreeNode | None) -> TreeNode | None:
    """LeetCode 226. The mirror OF a tree, rather than a test.

    is_symmetric(t) is exactly is_same(t, invert(copy_of(t))) — but doing it
    that way allocates a whole second tree, where is_mirror allocates
    nothing.
    """
    if node is None:
        return None
    node.left, node.right = invert(node.right), invert(node.left)
    return node


def count_matching_subtrees(big: TreeNode | None, small: TreeNode | None) -> int:
    """The follow-up: not "is it there" but "how many times".
    Cannot short-circuit, so it is the full O(n × m)."""
    if big is None:
        return 0
    return (int(is_same(big, small))
            + count_matching_subtrees(big.left, small)
            + count_matching_subtrees(big.right, small))


def is_same_iterative(a: TreeNode | None, b: TreeNode | None) -> bool:
    """Two trees, one stack of pairs. No recursion depth risk."""
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if x is None and y is None:
            continue
        if x is None or y is None:
            return False
        if x.val != y.val:
            return False
        stack.append((x.left, y.left))
        stack.append((x.right, y.right))
    return True


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
    a = from_list([1, 2, 3])
    b = from_list([1, 2, 3])
    c = from_list([1, 2, None, 3])

    print(is_same(a, b))                            # True
    print(is_same(a, c))                            # False
    print(is_same(None, None), is_same(a, None))    # True False
    print(is_same_iterative(a, b))                  # True

    print(is_symmetric(from_list([1, 2, 2, 3, 4, 4, 3])))       # True
    print(is_symmetric(from_list([1, 2, 2, None, 3, None, 3]))) # False
    print(is_symmetric(None), is_symmetric(TreeNode(1)))        # True True
    print(is_symmetric_iterative(from_list([1, 2, 2, 3, 4, 4, 3])))  # True

    # the trap: identical halves are NOT symmetry
    trap = from_list([1, 2, 2, None, 3, None, 3])
    print(is_same(trap.left, trap.right))           # True   <- the wrong test
    print(is_symmetric(trap))                       # False  <- the right answer

    big = from_list([3, 4, 5, 1, 2])
    small = from_list([4, 1, 2])
    print(is_subtree(big, small))                   # True
    print(is_subtree_by_string(big, small))         # True

    # "subtree" is strict: nothing extra below
    print(is_subtree(from_list([1, 2, 3]), from_list([1, 2])))  # False

    # the delimiter trap, demonstrated
    print(serialise(TreeNode(12)))                  # ,12,#,#
    print(serialise(TreeNode(2)))                   # ,2,#,#
    print(serialise(TreeNode(2)) in serialise(TreeNode(12)))    # False — correct
    #  without the leading comma it would be "2,#,#" in "12,#,#"  ->  True, wrong

    print(count_matching_subtrees(from_list([1, 1, 1]), TreeNode(1)))   # 2
```

---

## 6. What it costs

### Same tree

```
 time   O(min(n, m))   — `and` stops at the first mismatch
 space  O(min(h1, h2)) — the recursion stack
```

**`min`, not `max`**, and it is worth saying: the walk stops as soon as one tree runs out or a value
differs, so it can never visit more nodes than the smaller tree has.

In practice, the common case is much better than the bound:

```
 two random trees of 1,000 nodes:  usually a mismatch within the first few nodes
 two identical trees of 1,000:     all 1,000 visited
```

### Symmetric tree

```
 time   O(n)   — every node visited once, in pairs
 space  O(h)
```

Each node is compared exactly once, against its mirror partner.

### Subtree — the interesting one

```
 naive:        O(n × m)
   n = nodes in the big tree, m = nodes in the small tree
   is_same is called at each of n nodes and can walk m nodes
```

```
 n = 1,000, m = 100     ->  up to 100,000 comparisons
 n = 10,000, m = 1,000  ->  up to 10,000,000
```

**In practice it is far better**, because most `is_same` calls fail on the root value immediately —
Kamala moving on after one stitch. The worst case needs an adversarial input:

```
 big:    a chain of 10,000 nodes all valued 1
 small:  a chain of 100 nodes all valued 1, then a 2 at the end
 -> every position matches for 100 steps before failing
 -> ~1,000,000 comparisons, and this is a real LeetCode test case
```

The string version:

```
 serialise both       O(n + m)
 substring search     O(n + m) with KMP
 -----------------------------------
 total                O(n + m) time, O(n + m) space
```

**The trade is explicit: linear time, at the cost of linear extra memory for the two strings.** On a
million-node tree the serialisation is several megabytes of string, where the naive version uses only the
stack.

### Why serialisation needs both fixes, in numbers

```
 without null markers:
   number of distinct trees with n nodes:   the Catalan number, ~4^n / n^1.5
   number of distinct null-free preorders:  n! / (repeats)
   -> many trees collide. The 2-node example collides immediately.

 without delimiters:
   any small tree whose values are suffixes of the big tree's values
   can produce a false match:  2 inside 12, 3 inside 13 or 23, and so on
   -> on values up to 10^4, collisions are common rather than exotic
```

### Recursion depth

```
 all three problems:  O(height) frames
 degenerate trees:    RecursionError past ~1,000
```

The iterative versions with a stack or queue of **pairs** are in the code above, and they are the answer
if the constraint allows a chain.

---

## 7. The traps

### Trap 1 — forgetting the "exactly one is `None`" case

```python
    def is_same(a, b):
        if a is None and b is None:
            return True
        return a.val == b.val and ...       # a might still be None
```

```
 AttributeError: 'NoneType' object has no attribute 'val'
```

**The most common crash in this topic.** Write both base-case lines together as a unit, before anything
else.

### Trap 2 — writing symmetry as `is_same(root.left, root.right)`

```python
    return is_same(root.left, root.right)               # WRONG
```

```
 is_symmetric(from_list([1, 2, 2, None, 3, None, 3]))
   this version -> True
   correct      -> False
```

Identical halves are a **translation**; symmetry is a **reflection**. They coincide only when each half
is itself symmetric, which is why the wrong version passes on so many test cases.

### Trap 3 — crossing only one of the two recursive calls

```python
        return (a.val == b.val
                and is_mirror(a.left, b.right)
                and is_mirror(a.right, b.right))        # should be b.left
```

Half-mirrored, and it produces `True` for some asymmetric trees and `False` for some symmetric ones.
**Write the two crossed calls as a pair and read them back**: left-right, right-left.

### Trap 4 — comparing values without comparing shape

```python
    return inorder(a) == inorder(b)                     # WRONG
```

Two different trees can share a traversal:

```
   1              1
    \            /
     2          2

 preorder without nulls:  [1, 2]  and  [1, 2]   ->  "equal"
```

Same list, different trees. **One traversal never determines a tree** — the same fact as
[day 100](../day-100-dfs-traversals/README.md), and it is why the serialisation trick needs null markers.

### Trap 5 — the subtree base cases backwards

```python
        if big is None:
            return True                     # WRONG
        if small is None:
            return False                    # WRONG
```

An empty small tree is a subtree of anything; an empty big tree contains nothing but the empty tree.
Getting these round the wrong way makes `is_subtree` return `True` for everything, which passes the first
test case and nothing else.

### Trap 6 — thinking "subtree" means "appears somewhere"

```
 big:   1              small:  1
       / \                    /
      2   3                  2

 many people expect True; the answer is FALSE
```

A subtree is a node **and everything below it**. The `1` in the big tree has a right child that the small
tree does not, so it is not the same subtree. If the question genuinely means "does this pattern appear
partway down", that is a different and harder problem — **ask**.

### Trap 7 — serialising without null markers

```python
    def serialise(node):
        if node is None:
            return ""                       # no marker
        return f",{node.val}" + serialise(node.left) + serialise(node.right)
```

```
 serialise(1 with left child 2)   ->  ",1,2"
 serialise(1 with right child 2)  ->  ",1,2"      ← identical
```

Different trees, same string, silent wrong answer.

### Trap 8 — serialising without delimiters

```python
        return f"{node.val}" + ...
```

```
 big contains 12, small is 2
 "2#,#" in "12#,#"  ->  True         ← a match that does not exist
```

**A leading comma before every value is the fix**, and it costs one character. This is the classic "my
solution passes 130 of 182 test cases" bug.

---

## 8. In the interview

### How it gets asked

- The warm-up: *"Are these two trees identical?"* LeetCode 100.
- The twist: *"Is this tree symmetric about its centre?"* LeetCode 101.
- The composition: *"Is this tree a subtree of that one?"* LeetCode 572.
- The optimisation: *"Your subtree solution is `O(n × m)`. Can you do better?"*
- The related: *"Invert a binary tree."* LeetCode 226 — famously.

### What to say out loud, in the first ninety seconds

1. **Name the shape.** "This is a recursion over **two** trees at once — the function takes a node from
   each and asks whether the subtrees below them match."
2. **State the three base cases before writing them.** "Both `None` is a match. Exactly one `None` is a
   mismatch, because the shapes differ. After those two lines, both are guaranteed to exist and I can
   dereference freely."
3. **Say what happens if you skip the middle one.** "Leaving out the 'exactly one' case does not give a
   wrong answer, it gives an `AttributeError` on the value comparison."
4. **For symmetry, say the difference explicitly.** "Symmetry is the same function with the arguments
   crossed — left against right and right against left. It is *not* checking that the two halves are
   identical; identical halves are a translation and symmetry is a reflection."
5. **For subtree, define the word.** "A subtree means a node **and everything below it**, so a match that
   continues into extra nodes is not a match."
6. **Give the complexity and flag the improvement.** "Same tree is `O(min(n, m))` because the `and`
   short-circuits. Subtree is `O(n × m)` naively, and there is a linear alternative via serialisation."

### The follow-ups

**"What are the base cases, and why three?"**
"Because two nodes can be `None` in three combinations, and they mean different things. **Both `None`** —
two empty subtrees, which match, so `True`. **Exactly one `None`** — the shapes differ, so `False`, and
this is the one people leave out. **Neither `None`** — now I can safely compare values and recurse. The
reason the middle one matters so much is that omitting it does not produce a wrong answer; it produces an
`AttributeError` when the next line reads `.val` on a `None`. I write both base-case lines as a unit
before anything else, so that everything below them is guaranteed safe."

**"Is symmetry just comparing the two halves?"**
"No, and this is the trap. Comparing the halves with `is_same` asks whether they are **identical**, which
is a translation. Symmetry is a **reflection**: the outermost node on the left must match the outermost
node on the right, so the recursion crosses the arguments — my left child against your right child, my
right against your left. The counter-example is a tree where both halves are `2` with a right child `3`:
the halves are identical, so the naive test says symmetric, but a mirror would need the `3` on the
outside of one side and the inside of the other. The two tests agree only when each half is itself
symmetric, which is why the wrong version passes a lot of test cases."

**"Your subtree solution is `O(n × m)`. Can you do better?"**
"Yes — serialise both trees to strings and ask whether one contains the other, which is `O(n + m)` with a
linear string search. Two details make it correct and both are silent if you get them wrong. **Null
markers**: without them, a node with only a left child and a node with only a right child serialise to
the same string, so different trees compare equal. **Delimiters around every value**: without them, a
tree containing the value 2 matches inside a tree containing 12, because `"2"` is a substring of `"12"` —
so I emit a comma before every value and `",2,"` is not inside `",12,"`. The trade is explicit: linear
time for linear extra memory, since I am now holding two strings proportional to the trees. And I would
say `O(n + m)` *with KMP* rather than claiming it for Python's `in`, which is fast but not guaranteed
linear."

**"What is the complexity of the naive version really?"**
"`O(n × m)` as a bound, and much better in practice, because almost every `is_same` call fails on the
root value comparison and returns after one step. The worst case needs an adversarial input — a big tree
that is a chain of ten thousand identical values and a small tree that is a hundred of the same value
followed by a difference. Then every position matches for a hundred steps before failing, and that is
about a million comparisons. That input exists in the LeetCode test set, which is why the string version
is worth knowing."

**"Could you compare the trees by their traversals instead?"**
"Only if the traversal records the nulls. A single traversal without nulls does not determine a tree —
a node with one left child and a node with one right child both give the preorder `[1, 2]`. With null
markers, a preorder does determine the tree uniquely, which is exactly what makes the serialisation trick
work. The other way is two traversals, one of which must be inorder, which is the reconstruction problem
rather than this one."

**"How would you handle a very deep tree?"**
"Both problems recurse to the height, so a ten-thousand-node chain exceeds Python's default limit. The
iterative version is straightforward here because the state is just a pair of nodes: a stack — or a queue,
which is what I would use for the symmetric version — holding **pairs**, popping a pair, applying the same
three base cases, and pushing the two child pairs. For symmetry the pushes are crossed exactly as in the
recursion. It is barely longer than the recursive version and removes the depth risk entirely."

### A model answer

Asked: *are these two trees identical? And is this tree a subtree of that one?*

> "Both are the same idea: a recursion that walks **two trees at once**, taking a node from each and
> asking whether what hangs below them matches.
>
> The whole difficulty is in the base cases, and there are **three**, because two nodes can be `None` in
> three different combinations. **Both `None`** means two empty subtrees, which match. **Exactly one
> `None`** means the shapes differ, so they cannot match — and this is the case people leave out. Leaving
> it out does not give a wrong answer; it gives an `AttributeError`, because the next line reads `.val` on
> a `None`. **Neither `None`** means I can safely compare the values and recurse on both pairs of
> children. I write the first two lines as a unit before anything else, so everything below is guaranteed
> safe.
>
> The comparison itself is `a.val == b.val and same(left, left) and same(right, right)`, and the `and`
> short-circuits, so a mismatch stops the walk immediately. That is why the complexity is
> `O(min(n, m))` rather than `O(n)` — it can never visit more nodes than the smaller tree has.
>
> If you then ask about symmetry, it is the same function with **the arguments crossed**: my left against
> your right, my right against your left. I would flag the trap explicitly, because it is the most common
> wrong answer here — checking that the two halves are *identical* is not the same thing. Identical halves
> are a translation, symmetry is a reflection, and they only coincide when each half is itself symmetric.
>
> For subtree, it is `is_same` tried at every node of the bigger tree. Two things to pin down. The base
> cases are **not** the same as `is_same`'s: an empty small tree is a subtree of anything, and an empty
> big tree contains nothing. And 'subtree' is stricter than people expect — it means a node **and
> everything below it**, so if the small tree is a `1` with a left child and the big tree's `1` also has a
> right child, that is not a match. Nothing extra is allowed to hang off the bottom.
>
> That is `O(n × m)` in the worst case, and much better in practice because most attempts fail on the
> first value. If you want a guaranteed improvement, I would serialise both trees and ask whether one
> string contains the other — `O(n + m)` with a linear string search. Two details are essential and both
> fail silently: **null markers**, or a left-only child and a right-only child produce the same string;
> and **a delimiter before every value**, or a tree containing 2 matches inside one containing 12. The
> cost is holding two strings proportional to the trees, where the naive version uses only the stack."

---

## 9. Recall card

- **All three problems are one recursion over TWO trees, and the base cases are the whole difficulty.
  THREE of them: both `None` → True · exactly one `None` → False · neither → compare values then both
  child pairs.** Omitting the middle line gives **`AttributeError: 'NoneType' object has no attribute
  'val'`**, not a wrong answer. Write both base lines as a unit first.
- **Symmetry is `is_same` with the arguments CROSSED** — left against right, right against left. It is
  **not** `is_same(root.left, root.right)`: identical halves are a *translation*, symmetry is a
  *reflection*, and the wrong version returns `True` on `[1,2,2,null,3,null,3]`.
- **"Subtree" means a node AND EVERYTHING below it** — nothing extra may hang off the bottom, so a `1`
  with a left child is not a subtree of a `1` with both children. And its base cases are the **opposite**
  way round: **empty small → True, empty big → False**.
- **Same tree is `O(min(n, m))`** because `and` short-circuits. **Subtree is `O(n × m)`** — bad in the
  worst case (a chain of identical values), fine in practice because most attempts fail on the first
  value.
- **The `O(n + m)` alternative: serialise both trees and search for one string inside the other — and it
  needs BOTH fixes, each silent if missed.** **Null markers**, or a left-only and a right-only child give
  the same string; **a delimiter before every value**, or `"2"` matches inside `"12"`. Say **`O(n + m)`
  with KMP**, and note the cost is `O(n + m)` extra memory.
