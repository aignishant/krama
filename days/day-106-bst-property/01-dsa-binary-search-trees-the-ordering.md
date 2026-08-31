---
day: 106
track: dsa
title: "Binary search trees: the ordering property"
phase: "Trees and binary search trees"
status: written
---

# Day 106 · DSA — Binary search trees: the ordering property

**After today you can:** You can state the BST invariant precisely, including the whole-subtree part.

**The interviewer asks it as:** *What makes a tree a binary search tree?*

---

## 1. What this is, and why they ask it

A **binary search tree** is a binary tree with one extra rule about the values: at every node, everything
in the left subtree is smaller and everything in the right subtree is larger.

Three sentences. That single rule turns a structure where finding a value costs `O(n)` into one where it
costs `O(height)`, because one comparison eliminates an entire subtree. **The rule is about whole
subtrees, not about the immediate children**, and confusing those two is the single most common error in
the topic — it produces a tree that looks correct locally and is broken globally. And the guarantee is
conditional: `O(log n)` only holds while the tree is **balanced**, which nothing so far forces.

They ask *"what makes a tree a binary search tree?"* as a warm-up and they are listening for one specific
thing: whether you say **"all of the left subtree"** or **"the left child"**. The second answer is wrong,
it is the answer most people give, and [day 108](../day-108-validating-a-bst/README.md) exists entirely
to punish it. Everything else in the phase — insert, delete, validate, balance, k-th smallest — depends
on stating the invariant correctly first.

---

## 2. The story

The three of them played the number game on every long bus journey, and Anitha, who was eleven, had made
up a rule that ruined it for her brother.

The game was that one person thought of a number between one and a hundred and the others guessed, and
after each guess they were told higher or lower.

Anitha was very good at it. She always guessed fifty first, and then twenty-five or seventy-five, and she
usually had it in six or seven guesses while her brother was still working upwards from four.

Her brother, who was eight, could not see why she did that, so on the way back from Trichy she made him
be the one thinking of the number, and she explained what she was doing as she went.

She said: when you tell me higher than fifty, I am not just learning something about fifty. I am throwing
away half of everything. One to fifty is gone. It is not coming back. It cannot be the number.

Then when you say lower than seventy-five, I have thrown away seventy-six to a hundred as well, so the
number is somewhere between fifty and seventy-five, and I only have twenty-five things left.

And this is the part he got wrong when it was his turn to answer.

He had thought of sixty. She guessed fifty; he said higher. She guessed seventy-five; he said lower.
She guessed sixty-two; he said lower — correct. She guessed fifty-five; and he said **higher**, which
was true of fifty-five and sixty, so he thought he was being honest.

But he had already said lower than sixty-two, and now he was saying higher than fifty-five, and Anitha
did the arithmetic and said fifty-eight.

He said no, sixty.

She said you told me lower than sixty-two, and you told me higher than fifty-five, and sixty is inside
that, so how is fifty-eight wrong.

And it took them ten minutes to work out what had happened: on the guess before, he had said **lower**
when the guess was fifty-one, because fifty-one was lower than sixty-two, which was the last thing he
had been thinking about. He had been answering each guess against the guess before it instead of against
his actual number.

Every single answer he gave was consistent with the one before it. Every one of them, checked against
its neighbour, was fine. And the answers taken together described a number that did not exist.

Anitha's rule after that was one sentence, and she made him repeat it: **every answer has to be true
about the number, not about the last thing you said.**

---

## 3. The idea in plain English

Anitha's brother has committed exactly the classic BST error, and her rule is the invariant.

### The invariant, stated correctly

> **For every node: every value in its left subtree is less than the node, and every value in its right
> subtree is greater than the node.**

**"Every value in the subtree", not "the child".** That word is the entire lesson.

```
 CORRECT                          WRONG BUT LOOKS FINE

        10                               10
       /  \                             /  \
      5    15                          5    15
     / \   / \                        / \   / \
    3   7 12  18                     3   7 8   18
                                            ^
 every node's left subtree is         8 < 15, so the LOCAL rule holds
 entirely smaller, every right         at node 15 — but 8 is in the RIGHT
 subtree entirely larger               subtree of 10 and 8 < 10.
                                       NOT a BST.
```

The `8` there is the brother's fifty-one: correct relative to its immediate neighbour, and wrong relative
to everything it is really underneath.

**Every node lives inside a range**, inherited from every ancestor above it — and that is the precise way
to say the invariant:

```
                     10            range: (-inf, +inf)
                   /    \
                  5      15        5 in (-inf, 10)   15 in (10, +inf)
                 / \    /  \
                3   7  12   18     7 in (5, 10)      12 in (10, 15)

 a node's range is NARROWED by every ancestor, not just its parent.
 going left  -> the upper bound becomes the parent's value
 going right -> the lower bound becomes the parent's value
```

**"Every answer has to be true about the number, not about the last thing you said."**

### What the rule buys

One comparison eliminates a whole subtree.

```python
    def search(node, target):
        while node:
            if target == node.val:
                return node
            node = node.left if target < node.val else node.right
```

**Four lines, and no recursion.** At each step you discard everything on one side. That is
[binary search](../day-042-binary-search-idea/README.md) from day 42, on a structure that supports
insertion and deletion.

```
 plain binary tree, find a value:   O(n)   — you must look in both subtrees
 BST, find a value:                 O(height)
 balanced BST:                      O(log n)  — 20 steps in a million nodes
 degenerate BST:                    O(n)      — a chain, and you are back where you started
```

### Inorder is sorted, and it is the definition in another form

Walk left, node, right — from [day 100](../day-100-dfs-traversals/README.md) — and on a BST the values
come out in ascending order.

```
        10
       /  \
      5    15
     / \   / \
    3   7 12  18

 inorder: 3, 5, 7, 10, 12, 15, 18       <- sorted
```

This is not a coincidence; it is the invariant restated. **"Everything left is smaller" *is* "the left
subtree comes first in sorted order".** And it gives you a second, very clean way to check whether a tree
is a BST: walk it inorder and confirm the values increase. That is
[day 108](../day-108-validating-a-bst/README.md).

### Duplicates: a decision you must state

The invariant as written says "less than" and "greater than", which leaves equal values undefined. Four
conventions exist and **you must say which one you are using**:

```
 1. NOT ALLOWED           the simplest, and what most interview problems assume
 2. equal goes LEFT       left subtree is <= node
 3. equal goes RIGHT      right subtree is >= node
 4. a COUNT on the node   the tree holds distinct values, each with a multiplicity
```

**Option 4 is the best real answer** — it keeps the tree smaller and makes deletion of one occurrence
trivial — and option 1 is what the problems assume. What you must not do is allow duplicates on both
sides, because then search cannot know which way to go and the structure loses its point.

### Why a BST rather than the alternatives

The comparison table is the reason anyone uses one, and it is the answer to "why not just use a hash
map?"

```
                       search      insert      delete    sorted order   min/max
 sorted array          O(log n)    O(n)        O(n)      free           O(1)
 linked list           O(n)        O(1)*       O(1)*     no             O(n)
 hash map              O(1)        O(1)        O(1)      NO             O(n)
 balanced BST          O(log n)    O(log n)    O(log n)  free           O(log n)
                                                          ^^^^^^^^^^^^
 (* given the position)
```

**A hash map beats a BST on every single-key operation and cannot do ordered ones at all.** That is the
whole argument:

- *"Give me everything between 20 and 40"* — a BST does it in `O(log n + k)`; a hash map must scan
  everything.
- *"What is the smallest value?"* — a BST walks left; a hash map scans everything.
- *"Give me them in order"* — a BST walks inorder; a hash map has no order.
- *"What is the next value above 37, if 37 is not present?"* — a BST answers it; a hash map cannot.

**Say it as one sentence: use a hash map unless you need order, and then use a BST.** That sentence is
worth more than any implementation detail.

### The catch: balance is not guaranteed

Nothing in the definition says a BST is balanced. Insert sorted data and you get a chain:

```
 insert 1, 2, 3, 4, 5 in order:

   1
    \
     2
      \
       3
        \
         4
          \
           5

 height = n - 1.  Every operation is O(n). This is a linked list with extra fields.
```

**And sorted input is not an unusual case — it is the most common one**, because data arrives sorted by
id, by timestamp, or by name far more often than randomly. That is why real systems use **self-balancing**
BSTs — AVL trees, red-black trees — which rotate to keep the height at `O(log n)`, and it is
[day 109](../day-109-balanced-trees/README.md).

### Where you have already met them

- **`sortedcontainers.SortedList`** in Python and `std::map` / `std::set` in C++ are ordered structures
  with exactly these guarantees. Python's own `dict` and `set` are hash-based and unordered by value.
- **Database indexes** are B-trees, which are BSTs with a high branching factor so that each node fills a
  disk page. Same invariant, tuned for disk.
- **`bisect`** on a sorted list gives you `O(log n)` search with `O(n)` insertion — the right choice when
  the data barely changes, and the wrong one when it does.

---

## 4. The picture

The invariant, drawn as ranges rather than as comparisons. **This is the diagram to be able to produce**,
because it makes both the rule and the classic error obvious.

```
                          10                  (-inf, +inf)
                        /    \
                       /      \
                      5        15             5 in (-inf, 10)   15 in (10, +inf)
                     / \      /  \
                    3   7   12    18          3 in (-inf, 5)    12 in (10, 15)
                                              7 in (5, 10)      18 in (15, +inf)

 going LEFT  narrows the UPPER bound to the parent's value
 going RIGHT narrows the LOWER bound to the parent's value

 the bounds accumulate from EVERY ancestor, not just the parent.
```

The classic error, drawn the same way:

```
                          10                  (-inf, +inf)
                        /    \
                       5      15              15 in (10, +inf)     ✓
                      / \    /  \
                     3   7  8    18           8 must be in (10, 15)
                             ^
                             8 < 15, so its PARENT is happy
                             8 < 10, so its GRANDPARENT is not
                             -> NOT a BST

 search(8) at the root: 8 < 10, so go LEFT — and 8 is on the right.
 The value is in the tree and the search cannot find it.
```

**That last line is why it matters.** A locally-correct, globally-broken BST does not raise anything — it
just fails to find values that are present.

Anitha's game, as the same picture:

```
 guess 50, "higher"   ->  the number is in (50, 100]
 guess 75, "lower"    ->  the number is in (50, 75)
 guess 62, "lower"    ->  the number is in (50, 62)
 guess 55, "higher"   ->  the number is in (55, 62)     -> 56..61

 the brother's error: he answered 51 against 62 rather than against 60.
 Each answer was consistent with its NEIGHBOUR and the set of answers
 described no number at all.
```

What one comparison buys:

```
 searching for 12 in a balanced BST of 1,000,000 nodes

 step 1:  compare with the root      -> discard 500,000 nodes
 step 2:  compare                    -> discard 250,000
 step 3:                             -> discard 125,000
 ...
 step 20:                            -> found

 20 comparisons.  In a plain binary tree of the same size: up to 1,000,000.
```

And the degenerate case, which is not exotic:

```
 inserting 1..7 in order          inserting 4,2,6,1,3,5,7

   1                                     4
    \                                  /   \
     2                                2     6
      \                              / \   / \
       3                            1   3 5   7
        \
         4                          height 2, search = 3 steps
          \
           5                        SAME VALUES, SAME RULE
            \                       the ORDER OF INSERTION decides everything
             6
              \
               7

   height 6, search = 7 steps
```

---

## 5. The code, built step by step

### Step 1 — state the invariant before writing anything

"At every node, **all** values in the left subtree are smaller and **all** values in the right subtree are
larger. Not just the immediate children — the whole subtree. Equivalently, every node lives inside a
range inherited from all of its ancestors."

**Say "all" and say "subtree".** That sentence is what the question is checking.

### Step 2 — search, which is the whole point of the structure

```python
        while node:
            if target == node.val:
                return node
            node = node.left if target < node.val else node.right
```

Iterative, four lines, `O(1)` space. **There is no reason to write this recursively** — there is nothing
to combine on the way back up, so the recursion would only cost stack frames.

### Step 3 — min and max are walks, not searches

```python
        while node.left:
            node = node.left            # the minimum is the leftmost node
```

**The smallest value is as far left as you can go**; the largest is as far right. `O(height)`, and this
is one of the ordered operations a hash map simply cannot do.

### Step 4 — say the duplicates policy out loud

"I will assume values are distinct, which is what the problem usually means. If duplicates are possible I
would keep a count on each node rather than allowing equal values on both sides, because equal values on
both sides means a search cannot know which way to go."

### Step 5 — flag the balance assumption

"All of this is `O(height)`. That is `O(log n)` only if the tree is balanced, and nothing so far
guarantees that — inserting sorted data gives a chain and every operation becomes `O(n)`. Real
implementations self-balance."

**Saying this before being asked is the difference between quoting a fact and understanding it.**

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
    """LeetCode 700. One comparison discards a whole subtree.

    Iterative on purpose: there is nothing to combine on the way back up,
    so recursion would only cost stack frames. O(height) time, O(1) space.
    """
    node = root
    while node:
        if target == node.val:
            return node
        node = node.left if target < node.val else node.right
    return None


def contains(root: TreeNode | None, target: int) -> bool:
    return search(root, target) is not None


def minimum(root: TreeNode | None) -> TreeNode | None:
    """The leftmost node. A hash map cannot answer this without a full scan."""
    if root is None:
        return None
    node = root
    while node.left:
        node = node.left
    return node


def maximum(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    node = root
    while node.right:
        node = node.right
    return node


def insert(root: TreeNode | None, value: int) -> TreeNode:
    """LeetCode 701. Walk to where the value BELONGS and put a leaf there.

    Note this does no balancing at all, so inserting sorted data builds a
    chain — and sorted input is the COMMON case, not an exotic one.
    """
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
            return root                 # duplicate: this version ignores it


def inorder(root: TreeNode | None) -> list[int]:
    """On a BST this is SORTED ORDER — the invariant restated."""
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        walk(node.left)
        out.append(node.val)
        walk(node.right)

    walk(root)
    return out


def range_query(root: TreeNode | None, low: int, high: int) -> list[int]:
    """Everything in [low, high], in order. O(height + k).

    THE operation a hash map cannot do: whole subtrees are skipped without
    being visited, because the ordering says they cannot contain anything
    in range.
    """
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        if node.val > low:
            walk(node.left)             # only if something left could qualify
        if low <= node.val <= high:
            out.append(node.val)
        if node.val < high:
            walk(node.right)

    walk(root)
    return out


def ceiling(root: TreeNode | None, target: int) -> int | None:
    """The smallest value >= target. Another hash-map impossibility.

    Walk down remembering the best candidate seen while going left.
    """
    best: int | None = None
    node = root
    while node:
        if node.val == target:
            return node.val
        if node.val > target:
            best = node.val             # a candidate; something smaller may exist
            node = node.left
        else:
            node = node.right
    return best


def floor_value(root: TreeNode | None, target: int) -> int | None:
    """The largest value <= target. The mirror image."""
    best: int | None = None
    node = root
    while node:
        if node.val == target:
            return node.val
        if node.val < target:
            best = node.val
            node = node.right
        else:
            node = node.left
    return best


def kth_smallest(root: TreeNode | None, k: int) -> int | None:
    """LeetCode 230. Inorder, stopping after k nodes.

    Iterative so it can stop: a recursive inorder naturally wants to finish
    the whole tree. O(height + k), not O(n).
    """
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return None


def height(node: TreeNode | None) -> int:
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def build_from_sorted(values: list[int]) -> TreeNode | None:
    """LeetCode 108. Build a BALANCED BST from sorted values.

    Take the middle as the root, then recurse on each half. This is the
    answer to "your tree degenerated" when you control the insertion order.
    O(n) time, height exactly floor(log2(n)).
    """
    def build(lo: int, hi: int) -> TreeNode | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(values[mid], build(lo, mid - 1), build(mid + 1, hi))

    return build(0, len(values) - 1)


class CountingBST:
    """The right way to handle duplicates: distinct values, each with a count.

    Keeps the tree smaller, makes "remove one occurrence" trivial, and never
    leaves a search unsure which way to go — which is what happens if equal
    values are allowed on both sides.
    """

    class Node:
        def __init__(self, val: int) -> None:
            self.val = val
            self.count = 1
            self.left: "CountingBST.Node | None" = None
            self.right: "CountingBST.Node | None" = None

    def __init__(self) -> None:
        self.root: "CountingBST.Node | None" = None

    def add(self, value: int) -> None:
        if self.root is None:
            self.root = self.Node(value)
            return
        node = self.root
        while True:
            if value == node.val:
                node.count += 1
                return
            if value < node.val:
                if node.left is None:
                    node.left = self.Node(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = self.Node(value)
                    return
                node = node.right

    def count_of(self, value: int) -> int:
        node = self.root
        while node:
            if value == node.val:
                return node.count
            node = node.left if value < node.val else node.right
        return 0


def find_in_plain_tree(node: TreeNode | None, target: int) -> TreeNode | None:
    """For contrast: without the ordering, BOTH subtrees must be searched.
    O(n), and this is what the BST rule buys you."""
    if node is None:
        return None
    if node.val == target:
        return node
    return (find_in_plain_tree(node.left, target)
            or find_in_plain_tree(node.right, target))


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
    bst = from_list([10, 5, 15, 3, 7, 12, 18])

    print(inorder(bst))                     # [3, 5, 7, 10, 12, 15, 18] — sorted
    print(search(bst, 7), search(bst, 99))  # TreeNode(7) None
    print(minimum(bst).val, maximum(bst).val)               # 3 18
    print(range_query(bst, 6, 13))          # [7, 10, 12]
    print(ceiling(bst, 11), floor_value(bst, 11))           # 12 10
    print(ceiling(bst, 19), floor_value(bst, 2))            # None None
    print(kth_smallest(bst, 3))             # 7

    # THE CLASSIC ERROR: locally fine, globally broken
    broken = from_list([10, 5, 15, 3, 7, 8, 18])
    print(inorder(broken))                  # [3, 5, 7, 10, 8, 15, 18] — NOT sorted
    print(search(broken, 8))                # None  <- 8 IS in the tree
    print(find_in_plain_tree(broken, 8))    # TreeNode(8)  <- the exhaustive search finds it

    # insertion order decides the shape
    sorted_inserts = None
    for v in range(1, 8):
        sorted_inserts = insert(sorted_inserts, v)
    print(height(sorted_inserts))           # 6   <- a chain

    balanced = build_from_sorted([1, 2, 3, 4, 5, 6, 7])
    print(height(balanced), inorder(balanced))              # 2 [1..7]

    print(height(sorted_inserts), height(balanced))         # 6 2 — same values

    # duplicates, done properly
    counting = CountingBST()
    for v in (5, 3, 5, 8, 5, 3):
        counting.add(v)
    print(counting.count_of(5), counting.count_of(3), counting.count_of(9))  # 3 2 0

    # the comparison that justifies the structure
    import bisect
    values = list(range(0, 1000, 2))
    print(bisect.bisect_left(values, 500))  # a sorted list: O(log n) search, O(n) insert
```

---

## 6. What it costs

### Everything is `O(height)`

```
 search        O(height)
 insert        O(height)
 delete        O(height)      — day 107
 min / max     O(height)
 successor     O(height)
 ceiling/floor O(height)
 range query   O(height + k)  — k results
 inorder       O(n)
```

**And `height` is the whole question.**

```
 balanced      height = log2(n)
   n = 1,000            10
   n = 1,000,000        20
   n = 1,000,000,000    30

 degenerate    height = n - 1
   n = 1,000,000        999,999
```

```
 n = 1,000,000
   balanced BST search:    ~20 comparisons
   degenerate BST search:  ~1,000,000 comparisons
   ratio:                  50,000×
```

**Say `O(height)` and then say what makes the height what it is.** Saying `O(log n)` without the
condition is the answer that gets challenged.

### Against the alternatives

```
                      search     insert     delete     ordered ops
 sorted array         O(log n)   O(n)       O(n)       excellent
 hash map             O(1)       O(1)       O(1)       IMPOSSIBLE
 balanced BST         O(log n)   O(log n)   O(log n)   excellent
```

```
 n = 1,000,000, one insertion
   sorted array:  up to 1,000,000 element moves
   balanced BST:  ~20 comparisons and one pointer change
```

**That row is why BSTs exist**: a sorted array matches them on search and is catastrophic on insertion.

And the ordered operations, which is why hash maps do not replace them:

```
 "everything between 20 and 40"
   BST:       O(log n + k)   ~20 steps plus the results
   hash map:  O(n)           scan all 1,000,000 keys

 "the smallest key"
   BST:       O(log n)       walk left
   hash map:  O(n)           scan everything

 "the next key above 37"
   BST:       O(log n)
   hash map:  cannot be done at all without scanning
```

### Space

```
 per node in Python:  ~120 bytes (value + two references + object overhead)
 1,000,000 nodes:     ~120 MB

 the same values in a sorted Python list of ints:  ~40 MB
 the same values in a set:                          ~60 MB
```

**A BST costs about three times a sorted array in memory** — the price of the pointers. That is the
trade: memory and pointer-chasing, in exchange for insertion staying logarithmic.

### Insertion order, measured

```
 inserting 1,000 values

 random order            expected height ~2 × log2(n)  ≈ 20
 sorted order            height 999
 sorted then reversed    height 999
 alternating outward     height ~log2(n)

 random insertion is FINE — the expected height is about 2 log n.
 the danger is not randomness, it is ORDER, and real data arrives ordered.
```

**That is the point worth making**: a randomly built BST is fine without any balancing. The reason
self-balancing trees exist is that real input is sorted by id, by timestamp, or by name far more often
than it is random.

---

## 7. The traps

### Trap 1 — stating the invariant about children instead of subtrees

```
 "the left child is smaller and the right child is larger"
```

**Wrong, and it is the most common answer.** It permits the tree from the picture, where 8 sits in the
right subtree of 10. Every local comparison passes; the structure is broken.

```
 search(broken_tree, 8)  ->  None
 the value IS in the tree, and the search cannot reach it.
```

No exception, no error — just a lookup that fails for a value that is present.

### Trap 2 — assuming `O(log n)`

```python
    # "BST search is O(log n)"
```

Only if balanced. A BST built by inserting sorted values is a chain, and sorted insertion is the common
case, not a corner case.

```
 for i in range(100000): insert(tree, i)
 -> height 99,999
 -> search is O(n)
 -> and a recursive traversal raises RecursionError
```

**Say `O(height)`, then say what determines the height.**

### Trap 3 — duplicates allowed on both sides

```python
        if value <= node.val:
            go left
        else:
            go right
```

...in one function, and the reverse somewhere else. Now equal values exist on both sides and a search
does not know which way to go, so it finds some of them and not others.

**Pick one convention and apply it everywhere, or keep a count on the node.**

### Trap 4 — comparing types that do not order

```python
    insert(tree, "banana")      # into a tree of integers
```

```
 TypeError: '<' not supported between instances of 'str' and 'int'
```

A BST requires a **total order**. Anything comparable works — integers, strings, tuples — and anything
mixed does not. Worth a sentence when the values are not numbers.

### Trap 5 — using a BST when a hash map would do

If the only operations are "insert", "delete" and "is it there", **a hash map is `O(1)` and simpler.**
Choosing a BST there is a worse answer, and an interviewer may be checking exactly that.

**The BST is justified by the ordered operations**: range, min, max, successor, sorted iteration, k-th
smallest. If none of those appear in the requirements, say so and use a hash map.

### Trap 6 — assuming inorder sorted means it is a BST

It does, actually — and that is a valid check. But the reverse mistake is common: **checking only that
each node's children are correctly placed does not prove sortedness.** The inorder check is
`O(n)` and correct; the local check is `O(n)` and wrong.

### Trap 7 — forgetting that the shape depends on insertion order

```
 insert 4,2,6,1,3,5,7  ->  a perfect tree, height 2
 insert 1,2,3,4,5,6,7  ->  a chain, height 6
```

Same values, same rule, same final set. **The tree is not determined by its contents** — a fact that
surprises people and matters for the next several days.

### Trap 8 — searching for a value using `==` on objects

If nodes hold objects rather than numbers, `<` must be defined and `==` must agree with it. A class with
a custom `__lt__` and a default `__eq__` produces a tree where a search descends correctly and then fails
the equality test. **Comparison and equality must be consistent**, which is what `functools.total_ordering`
is for.

---

## 8. In the interview

### How it gets asked

- The definitional one, usually first: *"What makes a tree a binary search tree?"*
- The operation: *"Search for a value in this BST."* LeetCode 700.
- The comparison: *"Why would you use a BST instead of a hash map?"*
- The catch: *"What is the worst case for a BST?"*
- The construction: *"Build a balanced BST from this sorted array."* LeetCode 108.

### What to say out loud, in the first ninety seconds

1. **State the invariant with the word "all".** "At every node, **all** the values in the left subtree are
   smaller and **all** the values in the right subtree are larger. Not just the immediate children — that
   is the distinction that matters, and it is what makes validating a BST a real problem."
2. **Give the equivalent formulation.** "Equivalently, every node lives inside a range inherited from all
   of its ancestors: going left narrows the upper bound, going right narrows the lower bound."
3. **Say what it buys.** "One comparison at each node discards an entire subtree, so search is
   `O(height)` instead of `O(n)`."
4. **Immediately qualify it.** "`O(height)`, not `O(log n)` — that only holds if the tree is balanced, and
   nothing in the definition forces that. Inserting sorted data gives a chain."
5. **Give the third formulation.** "An inorder traversal of a BST produces sorted order, which is the same
   rule stated differently and is the cleanest way to check one."
6. **Say when you would not use one.** "If I only need insert, delete and lookup, a hash map is `O(1)` and
   simpler. A BST earns its place when I need order — ranges, minimum, successor, sorted iteration."

### The follow-ups

**"Why would you use a BST instead of a hash map?"**
"For the ordered operations, and only for those. A hash map beats a BST on every single-key operation —
`O(1)` against `O(log n)` — so if all I need is insert, delete and lookup, the hash map is both faster and
simpler and I would say so. What it cannot do at all is anything involving order. 'Give me everything
between 20 and 40' is `O(log n + k)` in a BST and a full scan in a hash map. 'What is the smallest key' is
a walk down the left spine against a full scan. 'What is the next key above 37, given 37 is not present'
is answerable in a BST and simply not answerable in a hash map without looking at everything. And sorted
iteration is free from a BST and impossible from a hash map. So: **hash map unless I need order, then
BST.**"

**"What is the worst case?"**
"A chain — height `n − 1` — and every operation becomes `O(n)`, which is a linked list with extra fields.
The important part is that this is not an exotic input: it happens whenever values are inserted in sorted
order, and real data arrives sorted by id, by timestamp or by name far more often than randomly. It is
worth saying that a **randomly** built BST is fine — the expected height is about `2 log n` — so the enemy
is not adversarial data, it is ordinary ordered data. That is why production implementations self-balance:
AVL and red-black trees rotate on insertion to keep the height at `O(log n)`, and B-trees do the same idea
on disk for database indexes."

**"How do you handle duplicates?"**
"That is a decision I would state rather than assume, because the invariant as usually written says
strictly less and strictly greater and leaves equality undefined. Four options: disallow them, which is
what most interview problems assume; send equal values consistently left; send them consistently right;
or — the one I would actually build — **keep a count on each node**, so the tree holds distinct values
with multiplicities. The count version keeps the tree smaller, makes 'remove one occurrence' trivial, and
avoids the real failure mode, which is allowing equal values on both sides. If that happens, a search
cannot know which way to go, and it finds some occurrences and not others."

**"Build a balanced BST from a sorted array."**
"Take the middle element as the root, then recursively build the left subtree from the left half and the
right from the right half. `O(n)` time, and the height is exactly `⌊log₂ n⌋`, so it is optimally balanced.
The insight worth stating is *why* this is the answer to the degenerate-tree problem: inserting a sorted
array one value at a time gives a chain, because each new value is larger than everything already there.
Taking the middle first is precisely what stops that. It also shows that the shape of a BST is decided by
the **insertion order**, not by the set of values — the same seven numbers can give a chain of height 6 or
a perfect tree of height 2."

**"Prove your tree is actually a BST."**
"Two correct ways and one wrong one. The wrong one, which is what most people write, is checking at each
node that the left child is smaller and the right child is larger — that is local and it passes on trees
that are globally broken, where a value sits in the right subtree of an ancestor it should be left of. The
first correct way is to pass a **range** down: every node must lie strictly inside `(low, high)`, where
going left sets `high` to the parent's value and going right sets `low` to it. The second is to do an
**inorder traversal and check that the values strictly increase**, which works because inorder on a BST is
sorted order by definition. Both are `O(n)`; the inorder one is easier to get right and the range one uses
`O(height)` space instead of `O(n)`."

**"What does a broken BST actually do?"**
"It silently fails to find values that are present, and that is worth demonstrating rather than describing.
If an 8 ends up in the right subtree of a 10, then a search for 8 compares with 10, goes left because 8 is
smaller, and never looks at the branch where the 8 actually is. It returns 'not found' for a value that is
in the structure. No exception, no error — and an exhaustive traversal would find it, which makes the bug
look impossible when you are debugging."

### A model answer

Asked: *what makes a tree a binary search tree?*

> "The ordering rule, and the precise wording matters more here than in almost any other definition in the
> subject.
>
> **At every node, all the values in its left subtree are smaller than it, and all the values in its right
> subtree are larger.** Not the left *child* — the whole left *subtree*. That distinction is the entire
> content of the definition, and getting it wrong gives you a tree that satisfies every local comparison
> and is globally broken.
>
> Another way to say the same thing, which I find clearer: **every node lives inside a range inherited
> from all of its ancestors.** The root's range is unbounded. Going left narrows the upper bound to the
> parent's value; going right narrows the lower bound. So a node in the right subtree of the root and the
> left subtree of that node has both bounds set by two different ancestors, and it must satisfy both. The
> classic failure is a node that satisfies its parent and violates its grandparent.
>
> And a third equivalent statement: **an inorder traversal of a BST produces the values in sorted order.**
> That is not a consequence, it is the same rule restated, and it is the cleanest way to verify one.
>
> What the rule buys is that a single comparison eliminates an entire subtree. Searching is a walk down
> from the root — if the target is smaller, everything to the right is irrelevant and you never look at
> it. That makes search `O(height)` instead of the `O(n)` you would pay in a plain binary tree, where
> nothing about the values tells you which way to go.
>
> I would immediately qualify that, though, because it is the thing people quote wrongly: it is
> **`O(height)`, not `O(log n)`**. Nothing in the definition says the tree is balanced. If you insert
> values in sorted order, every new value is larger than everything already there, so it goes to the far
> right and you build a chain of height `n − 1` — a linked list with extra fields, where every operation is
> `O(n)`. And sorted insertion is not an unusual case; real data arrives sorted by id or timestamp far more
> often than randomly. A **randomly** built tree is fine — its expected height is about `2 log n` — so the
> problem is order, not adversaries. That is why production implementations self-balance with rotations,
> and why database indexes are B-trees.
>
> Finally, when I would use one. A hash map beats a BST on every single-key operation — `O(1)` against
> `O(log n)` — so if all I need is insert, delete and lookup, I would use the hash map. The BST earns its
> place when I need **order**: range queries, minimum and maximum, the next value above a key that is not
> present, sorted iteration, k-th smallest. Those are `O(log n)` in a BST and impossible in a hash map
> without scanning everything."

---

## 9. Recall card

- **The invariant, with the word that matters: at every node, ALL values in the LEFT SUBTREE are smaller
  and ALL values in the RIGHT SUBTREE are larger.** Not the immediate children — that answer permits a
  globally broken tree in which **`search` returns `None` for a value that is present**, with no error.
- **Equivalent formulations: every node lies inside a RANGE inherited from ALL its ancestors** (left
  narrows the upper bound, right narrows the lower), **and an INORDER traversal gives sorted order.** Both
  are the same rule and both give correct validations.
- **One comparison discards a whole subtree → `O(height)`. Say `O(height)`, not `O(log n)`** — that needs
  **balance**, which nothing guarantees. **Sorted insertion builds a chain** (height `n−1`, every operation
  `O(n)`), and sorted input is the *common* case. A **randomly** built BST is fine: expected height
  ~`2 log n`. **The shape depends on insertion order, not on the set of values** — the same 7 values give
  height 6 or height 2.
- **Use a hash map unless you need order.** A hash map wins every single-key operation (`O(1)`) and cannot
  do **ranges, min/max, successor/ceiling, sorted iteration or k-th smallest** at all. Those are what a
  BST is for. Against a sorted array: same `O(log n)` search, but insertion is **`O(log n)` versus up to a
  million element moves**.
- **State a duplicates policy**: disallow, always-left, always-right, or — best — **a count on each node**.
  Equal values on both sides means a search cannot know which way to go and finds some occurrences and not
  others. And **build a balanced BST from sorted data by taking the middle as the root** — `O(n)`, height
  exactly `⌊log₂ n⌋`.
