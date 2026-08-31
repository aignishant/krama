---
day: 109
track: dsa
title: "Balanced trees, and why balance matters"
phase: "Trees and binary search trees"
status: written
---

# Day 109 · DSA — Balanced trees, and why balance matters

**After today you can:** You can show the input that turns a BST into a linked list, and name the fix.

**The interviewer asks it as:** *What is the worst case for a BST? How do real databases avoid it?*

---

## 1. What this is, and why they ask it

A tree is **balanced** when its height stays close to `log n` instead of growing towards `n`. Every
`O(log n)` claim about a binary search tree depends on it, and nothing in
[insert](../day-107-bst-operations/README.md) or delete does anything to make it true.

Three sentences. The failing input is not exotic — **sorted data**, which is how data usually arrives —
and it turns a million-node tree into a chain where every operation is a million steps. The fix is a
**rotation**: a local rearrangement of three or four pointers that reduces the height by one without
touching the rest of the tree or changing the inorder order. And the two families of self-balancing tree —
AVL and red-black — differ in how strictly they enforce balance, which is a straight trade between read
speed and write cost.

They ask it because the previous three days all quietly assumed balance and this is where the assumption
gets paid for. The expected answer has three parts: **the input that breaks it**, **what a rotation does**,
and **which structure you would actually use** — and for the last part the correct answer includes "I would
not implement a red-black tree in an interview, and here is what I would do instead."

---

## 2. The story

Ilango's cart was a two-wheeled hand cart with the wheels in the middle, and he sold fruit from it on the
road outside the college.

The way it worked was that the load sat over the axle and he lifted the handles to move it. If the weight
was spread evenly on both sides of the wheels, the handles were light — he could lift them with one hand
and push the cart with the other on his phone.

If everything was piled at the far end, the handles wanted to fly up, and he had to hang his whole weight
on them to keep the cart level. Twenty minutes of that and his arms were finished.

The problem was that a morning's selling did it to him automatically.

He loaded properly at four in the morning — front and back matched. Then customers bought, and they did not
buy evenly. Everybody wanted the sweet limes at the front, so by ten the front was empty and there were
still forty kilos of oranges over the back wheel, and the cart was unusable.

The obvious fix, which he did for the first year, was to stop, take everything off, and repack the whole
cart. That took twenty minutes and he could not sell during it.

What he learned from the man who sold him the cart was much smaller.

You do not repack. You move **one crate**. You pick the crate nearest the wheels on the heavy side and you
lift it across to the other side. Ten seconds. The cart is level again, nothing else has been touched, and
the fruit is still in the same order — sweet limes at the front, oranges at the back, because you only
moved something that was already in the middle.

He said the trick is that it has to be a crate near the middle. If you take one from the far end and carry
it all the way across, you have changed the arrangement and now you cannot find anything. Take the one at
the pivot; that one can go either way without disturbing the order.

Ilango did that maybe six or seven times a day, ten seconds each. Total, about a minute. Against twenty
minutes of repacking, twice.

And he said one more thing about it that took him a season to understand. He did not wait until the cart
was unusable. He checked after every few sales, and if it was starting to lean, he moved a crate then. If
you wait, one crate is not enough and you are back to repacking.

---

## 3. The idea in plain English

Ilango's crate is a rotation, and the two things he learned — move something near the pivot, and correct
early — are the two things that make self-balancing trees work.

- Weight all at one end is a **degenerate tree**.
- Repacking the whole cart is **rebuilding the tree** — `O(n)`.
- Moving one crate near the wheels is a **rotation** — `O(1)`, and it changes nothing else.
- "The fruit is still in the same order" is the crucial property: **a rotation preserves the inorder
  sequence.**
- Checking after every few sales is **rebalancing on every insertion**, rather than when it is already
  broken.

### The failing input

```python
    for value in [1, 2, 3, 4, 5, 6, 7]:
        insert(tree, value)
```

Every value is larger than everything already there, so it goes to the far right, every time.

```
   1
    \
     2
      \
       3
        \
         4        height = n - 1
          \       every operation = O(n)
           5      this is a linked list with an unused pointer per node
            \
             6
              \
               7
```

**Sorted input is the normal case, not an adversarial one.** Data arrives sorted by id, by timestamp, by
name, by creation order — far more often than randomly. And reverse-sorted does the same thing to the
left.

```
 n = 1,000,000
   balanced:    ~20 comparisons per lookup
   degenerate:  1,000,000
   ratio:       50,000×
```

**Also**: a recursive traversal of a chain of 10,000 nodes raises `RecursionError`. So the failure is not
only slow, it can be fatal.

The one piece of good news, worth saying: **a randomly built BST is fine.** Its expected height is about
`2 log n` — around 40 for a million nodes — so the enemy is *order*, not adversarial data.

### What "balanced" means

The usual definition is **height-balanced**:

> At **every** node, the heights of the left and right subtrees differ by at most 1.

**"Every node", not just the root** — the same whole-subtree distinction as the
[BST invariant](../day-106-bst-property/README.md), and it fails in the same way if you check only the top.

```
 a tree whose ROOT is balanced but which is not balanced:

           1
         /   \
        2     3
       /       \
      4         5
     /           \
    6             7

 root: left height 2, right height 2  -> difference 0  ✓
 node 2: left height 1, right height -1 -> difference 2  ✗
```

Checking this naively calls `height` at every node, which is `O(n²)` — the
[day 102](../day-102-height-and-diameter/README.md) mistake. The one-pass version returns the height, or a
sentinel meaning "already unbalanced", and short-circuits.

### Rotations

A **rotation** rearranges three or four pointers around one node so that a child moves up and the node
moves down. It reduces the height on one side by one, and — this is the property everything depends on —
**it does not change the inorder sequence**, so the tree is still a valid BST afterwards.

```
 RIGHT ROTATION about y            LEFT ROTATION about x

        y                                 x
       / \                               / \
      x   C        ──────►              A   y
     / \           ◄──────                 / \
    A   B                                 B   C

 inorder before: A x B y C
 inorder after:  A x B y C          IDENTICAL. That is why it is legal.
```

The code is four lines and worth knowing by heart:

```python
    def rotate_right(y):
        x = y.left
        y.left = x.right        # B moves across
        x.right = y             # y goes down
        return x                # x is the new subtree root
```

**`return x` matters**: the caller must reattach, exactly as with
[deletion](../day-107-bst-operations/README.md). `node.left = rotate_right(node.left)`.

Ilango's crate: **only the thing at the pivot moves**, and the order is preserved.

### The four cases

After inserting, one node becomes unbalanced. There are four shapes and two of them need two rotations.

```
 LEFT-LEFT     inserted into the left child's LEFT subtree     -> one RIGHT rotation
 RIGHT-RIGHT   inserted into the right child's RIGHT subtree   -> one LEFT rotation
 LEFT-RIGHT    inserted into the left child's RIGHT subtree    -> LEFT on the child, then RIGHT
 RIGHT-LEFT    inserted into the right child's LEFT subtree    -> RIGHT on the child, then LEFT
```

**The zig-zag cases need two rotations**, and the reason is worth one sentence: a single rotation on a
zig-zag shape just produces the mirror-image zig-zag. The first rotation straightens it into a
left-left or right-right, and the second fixes it.

### AVL and red-black: the same idea, two settings

Both are BSTs that rotate on insertion and deletion. They differ in **how strict** the balance rule is.

| | **AVL** | **Red-black** |
|---|---|---|
| Rule | heights differ by ≤ 1 at every node | no red node has a red child; every root-to-leaf path has the same number of black nodes |
| Height bound | ≤ 1.44 log n | ≤ 2 log n |
| Lookups | faster (shorter tree) | slightly slower |
| Insert/delete | more rotations | fewer rotations |
| Used by | in-memory indexes, read-heavy structures | **`std::map`, Java's `TreeMap`, the Linux kernel scheduler** |

**Red-black wins in practice** because most workloads mix reads and writes, and its looser rule means far
less rotation on write. **AVL wins when reads dominate heavily.**

**Do not implement either in an interview.** The honest answer is: *"I would use the language's ordered
map, which is a red-black tree. If I had to hand-build something with these guarantees I would write a
treap or a skip list, because they are twenty lines instead of two hundred."*

### The alternatives that are actually writable

**Treap.** A BST by key and a heap by a random priority. Insert normally, then rotate up while the
priority is out of order. Because the priorities are random, the shape is a randomly built BST, whose
expected height is `O(log n)`. **About twenty-five lines**, and it is the answer to "implement a balanced
tree" in a real interview.

**Skip list.** Not a tree at all — a linked list with random express lanes. Same `O(log n)` expected
bounds, much simpler code, and it is what **Redis uses for sorted sets**.

**Both are randomised**: they guarantee `O(log n)` *expected*, not worst case. **Say that**; it is the
trade you are making for the simplicity.

### And what databases actually do

Not binary trees at all. A database index is a **B-tree** (or B+ tree), which is the same idea with a much
higher branching factor: each node holds hundreds of keys and fills one disk page.

```
 binary tree,  1,000,000 keys:  height ~20  ->  20 disk reads
 B-tree, 500 keys per node:     height ~3   ->  3 disk reads
```

**A disk read is about 10 ms and a memory read is 100 ns, so the height *is* the cost.** Reducing 20 reads
to 3 is the entire reason B-trees exist, and it is the answer to "how do real databases avoid it?"

---

## 4. The picture

The failing input, drawn against what it should be.

```
 insert 1..7 IN ORDER                 insert 4,2,6,1,3,5,7

   1                                          4
    \                                       /   \
     2                                     2     6
      \                                   / \   / \
       3                                 1   3 5   7
        \
         4        height 6                height 2
          \       search: up to 7 steps    search: up to 3 steps
           5
            \     SAME SEVEN VALUES.
             6    SAME RULE.
              \   Only the ORDER OF INSERTION differs.
               7
```

A rotation, with the inorder sequence written underneath — which is the point.

```
 BEFORE (right-heavy)                AFTER a LEFT rotation about x

      x                                    y
     / \                                  / \
    A   y          ────────►             x   C
       / \                              / \
      B   C                            A   B

 inorder:  A  x  B  y  C            inorder:  A  x  B  y  C
           ^^^^^^^^^^^^^                      ^^^^^^^^^^^^^
           IDENTICAL — which is why the tree is still a valid BST.

 height on the right: reduced by one.
 nodes touched: three pointers. Everything else in the tree is untouched.
```

The four cases:

```
 LEFT-LEFT                     RIGHT-RIGHT
      z                             z
     /                               \
    y          rotate RIGHT(z)        y        rotate LEFT(z)
   /                                   \
  x                                     x


 LEFT-RIGHT                    RIGHT-LEFT
      z                             z
     /                               \
    y    step 1: LEFT(y)              y     step 1: RIGHT(y)
     \   step 2: RIGHT(z)            /      step 2: LEFT(z)
      x                             x

 the zig-zag cases need TWO rotations, because ONE rotation on a zig-zag
 produces the mirror-image zig-zag — it has to be straightened first.
```

Ilango's cart, as the same picture:

```
 BEFORE                              AFTER moving ONE crate at the pivot

   [   ][   ][ o ][ o ][ o ]           [ o ][   ][ o ][ o ][   ]
             ▲                                   ▲
           wheels                              wheels
   heavy behind the axle               level, and the ORDER of the
   handles fly up                      crates along the cart is unchanged

 what he did NOT do: unload and repack (O(n))
 what he did:        move the crate AT the pivot (O(1))
```

Where the height goes:

```
 n = 1,000,000

 structure              height        lookup
 --------------------   -----------   -------------------------
 degenerate BST         999,999       1,000,000 comparisons
 random BST             ~40           ~40
 red-black tree         ≤ 40          ≤ 40
 AVL tree               ≤ 29          ≤ 29
 B-tree (500/node)      3             3 DISK READS  ← the one that matters
```

---

## 5. The code, built step by step

### Step 1 — show the failing input first

"The worst case is sorted input, and it is not adversarial — data arrives sorted by id or timestamp far
more often than randomly. Insert one to a million in order and you have a chain: every operation is a
million steps instead of twenty, and a recursive traversal raises `RecursionError`."

**Demonstrate it rather than describe it.** Building the chain takes three lines.

### Step 2 — define balanced with "every node"

```python
        abs(height(node.left) - height(node.right)) <= 1
```

...at **every** node, not just the root. And write the check in one pass, with a sentinel — the
[day 102](../day-102-height-and-diameter/README.md) technique — because the naive version is `O(n²)`.

### Step 3 — the rotation, and the property that makes it legal

```python
    def rotate_right(y):
        x = y.left
        y.left = x.right
        x.right = y
        return x
```

**Say the property as you write it**: *"This does not change the inorder sequence, so the tree is still a
valid BST. It just moves one node up and one down."* That is the sentence the whole topic rests on.

### Step 4 — name the four cases and why two need two rotations

"Left-left and right-right are one rotation. Left-right and right-left are zig-zags, and a single rotation
on a zig-zag gives you the mirror-image zig-zag — so you straighten it first with a rotation on the child,
then fix it with a rotation on the node."

### Step 5 — say what you would actually use

"I would not hand-write a red-black tree. In production I would use the language's ordered map. If I had
to implement something with these guarantees, I would write a **treap** — a BST by key and a heap by a
random priority — which is about twenty-five lines and gives `O(log n)` expected, or a **skip list**,
which is what Redis uses for sorted sets."

### The complete solution

```python
import random
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


def height(node: TreeNode | None) -> int:
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def is_balanced(root: TreeNode | None) -> bool:
    """Height-balanced at EVERY node, in one pass.

    -2 is the sentinel for "already unbalanced". Safe because a real height
    is never below -1. The naive version calls height() at every node and is
    O(n^2) on a chain — the day 102 mistake.
    """
    UNBALANCED = -2

    def check(node: TreeNode | None) -> int:
        if node is None:
            return -1
        left = check(node.left)
        if left == UNBALANCED:
            return UNBALANCED               # short-circuit
        right = check(node.right)
        if right == UNBALANCED or abs(left - right) > 1:
            return UNBALANCED
        return 1 + max(left, right)

    return check(root) != UNBALANCED


# ---------------------------------------------------------------------------
# ROTATIONS — the whole technique, in eight lines.
# ---------------------------------------------------------------------------

def rotate_right(y: TreeNode) -> TreeNode:
    """y goes down, its left child x comes up. Returns the new subtree root.

    THE PROPERTY THAT MAKES IT LEGAL: the inorder sequence is unchanged.
        before:  A x B y C
        after:   A x B y C
    So the tree is still a valid BST. Only the SHAPE changed.

    O(1): three pointers. Nothing outside this subtree is touched.
    """
    x = y.left
    assert x is not None
    y.left = x.right                        # B moves across
    x.right = y                             # y goes down
    return x                                # the caller must REATTACH this


def rotate_left(x: TreeNode) -> TreeNode:
    """The mirror image."""
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    return y


# ---------------------------------------------------------------------------
# AVL — strict balance. Written out once so the four cases are concrete.
# ---------------------------------------------------------------------------

class AVLNode:
    __slots__ = ("val", "left", "right", "height")

    def __init__(self, val: int) -> None:
        self.val = val
        self.left: "AVLNode | None" = None
        self.right: "AVLNode | None" = None
        self.height = 0                     # a leaf has height 0


def _h(node: "AVLNode | None") -> int:
    return -1 if node is None else node.height


def _update(node: AVLNode) -> None:
    node.height = 1 + max(_h(node.left), _h(node.right))


def _balance_factor(node: AVLNode) -> int:
    return _h(node.left) - _h(node.right)


def _rotate_right(y: AVLNode) -> AVLNode:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    _update(y)                              # y first — it is now BELOW x
    _update(x)
    return x


def _rotate_left(x: AVLNode) -> AVLNode:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    _update(x)
    _update(y)
    return y


def avl_insert(node: "AVLNode | None", value: int) -> AVLNode:
    """Insert, then rebalance on the way back up.

    THE FOUR CASES:
      LL  left-heavy,  inserted left of the left child   -> rotate RIGHT
      RR  right-heavy, inserted right of the right child -> rotate LEFT
      LR  left-heavy,  inserted RIGHT of the left child  -> LEFT(child), RIGHT(node)
      RL  right-heavy, inserted LEFT of the right child  -> RIGHT(child), LEFT(node)

    The zig-zag cases need TWO rotations because one rotation on a zig-zag
    just produces the mirror-image zig-zag.
    """
    if node is None:
        return AVLNode(value)
    if value < node.val:
        node.left = avl_insert(node.left, value)
    elif value > node.val:
        node.right = avl_insert(node.right, value)
    else:
        return node                         # duplicate: ignored

    _update(node)
    balance = _balance_factor(node)

    if balance > 1:                                     # left-heavy
        assert node.left is not None
        if value > node.left.val:                       # LEFT-RIGHT
            node.left = _rotate_left(node.left)
        return _rotate_right(node)                      # LEFT-LEFT

    if balance < -1:                                    # right-heavy
        assert node.right is not None
        if value < node.right.val:                      # RIGHT-LEFT
            node.right = _rotate_right(node.right)
        return _rotate_left(node)                       # RIGHT-RIGHT

    return node


def avl_height(node: "AVLNode | None") -> int:
    return _h(node)


def avl_inorder(node: "AVLNode | None", out: list[int] | None = None) -> list[int]:
    out = [] if out is None else out
    if node is None:
        return out
    avl_inorder(node.left, out)
    out.append(node.val)
    avl_inorder(node.right, out)
    return out


# ---------------------------------------------------------------------------
# TREAP — the one to actually write in an interview. ~25 lines.
# ---------------------------------------------------------------------------

class TreapNode:
    __slots__ = ("val", "priority", "left", "right")

    def __init__(self, val: int) -> None:
        self.val = val
        self.priority = random.random()     # RANDOM: this is what balances it
        self.left: "TreapNode | None" = None
        self.right: "TreapNode | None" = None


def treap_insert(node: "TreapNode | None", value: int) -> TreapNode:
    """A BST by VALUE and a max-heap by PRIORITY.

    Insert as a normal BST leaf, then rotate it upward while its random
    priority is higher than its parent's. Because the priorities are random,
    the resulting shape is exactly a RANDOMLY BUILT BST — expected height
    O(log n) — regardless of the insertion order.

    O(log n) EXPECTED, not worst case. Say that; it is the trade for
    twenty-five lines instead of two hundred.
    """
    if node is None:
        return TreapNode(value)
    if value < node.val:
        node.left = treap_insert(node.left, value)
        if node.left.priority > node.priority:
            left = node.left
            node.left = left.right
            left.right = node
            node = left                     # rotate right
    elif value > node.val:
        node.right = treap_insert(node.right, value)
        if node.right.priority > node.priority:
            right = node.right
            node.right = right.left
            right.left = node
            node = right                    # rotate left
    return node


def treap_height(node: "TreapNode | None") -> int:
    if node is None:
        return -1
    return 1 + max(treap_height(node.left), treap_height(node.right))


def treap_inorder(node: "TreapNode | None", out: list[int] | None = None) -> list[int]:
    out = [] if out is None else out
    if node is None:
        return out
    treap_inorder(node.left, out)
    out.append(node.val)
    treap_inorder(node.right, out)
    return out


# ---------------------------------------------------------------------------
# The plain BST, for comparison, and the rebuild fix.
# ---------------------------------------------------------------------------

def bst_insert(node: TreeNode | None, value: int) -> TreeNode:
    if node is None:
        return TreeNode(value)
    if value < node.val:
        node.left = bst_insert(node.left, value)
    elif value > node.val:
        node.right = bst_insert(node.right, value)
    return node


def rebuild_balanced(root: TreeNode | None) -> TreeNode | None:
    """The O(n) alternative to rotations: flatten to sorted order, then
    rebuild from the middle. Ilango repacking the whole cart.

    Correct, simple, and O(n) — fine as an occasional maintenance operation,
    useless as a per-insertion strategy.
    """
    values: list[int] = []

    def flatten(node: TreeNode | None) -> None:
        if node is None:
            return
        flatten(node.left)
        values.append(node.val)
        flatten(node.right)

    flatten(root)

    def build(lo: int, hi: int) -> TreeNode | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(values[mid], build(lo, mid - 1), build(mid + 1, hi))

    return build(0, len(values) - 1)


if __name__ == "__main__":
    # THE FAILING INPUT — three lines, and it is the whole worst case
    chain: TreeNode | None = None
    for v in range(1, 8):
        chain = bst_insert(chain, v)
    print(height(chain), is_balanced(chain))            # 6 False

    # the same values, balanced
    good: TreeNode | None = None
    for v in (4, 2, 6, 1, 3, 5, 7):
        good = bst_insert(good, v)
    print(height(good), is_balanced(good))              # 2 True

    # rotations preserve inorder
    y = TreeNode(5, TreeNode(3, TreeNode(1), TreeNode(4)), TreeNode(8))

    def inorder(n: TreeNode | None, out=None):
        out = [] if out is None else out
        if n:
            inorder(n.left, out); out.append(n.val); inorder(n.right, out)
        return out

    before = inorder(y)
    y = rotate_right(y)
    print(before, inorder(y), before == inorder(y))     # same list, True
    print(y.val)                                        # 3 — the new root

    # AVL survives sorted input
    avl: AVLNode | None = None
    for v in range(1, 8):
        avl = avl_insert(avl, v)
    print(avl_height(avl), avl_inorder(avl))            # 2 [1..7]

    avl_big: AVLNode | None = None
    for v in range(1, 1001):
        avl_big = avl_insert(avl_big, v)
    print(avl_height(avl_big))                          # 9   (1.44 log2(1000) ≈ 14)

    # a plain BST with the same input
    plain: TreeNode | None = None
    for v in range(1, 1001):
        plain = bst_insert(plain, v)
    print(height(plain))                                # 999  <- the disaster

    # a treap does not care about insertion order
    random.seed(7)
    treap: TreapNode | None = None
    for v in range(1, 1001):
        treap = treap_insert(treap, v)
    print(treap_height(treap))                          # ~20, from SORTED input
    print(treap_inorder(treap)[:5])                     # [1, 2, 3, 4, 5]

    # and the O(n) rebuild
    fixed = rebuild_balanced(chain)
    print(height(fixed), is_balanced(fixed))            # 2 True

    # a randomly built BST is fine — the enemy is ORDER, not randomness
    values = list(range(1, 1001))
    random.shuffle(values)
    rnd: TreeNode | None = None
    for v in values:
        rnd = bst_insert(rnd, v)
    print(height(rnd))                                  # ~20, roughly 2*log2(1000)
```

---

## 6. What it costs

### The height, which is everything

```
 structure          worst-case height      lookup at n = 1,000,000
 ----------------   --------------------   -----------------------
 degenerate BST     n - 1                  1,000,000
 random BST         ~2 log n  (expected)   ~40
 red-black tree     ≤ 2 log n              ≤ 40
 AVL tree           ≤ 1.44 log n           ≤ 29
 perfect            log n                  20
```

**The AVL bound of `1.44 log n` is worth knowing** — it comes from the Fibonacci-shaped worst case, the
sparsest tree that still satisfies the AVL rule.

### Rotations, and the write cost

```
 AVL insert:        up to 2 rotations, then the height updates propagate up
 AVL delete:        up to O(log n) rotations — this is the AVL weakness
 red-black insert:  at most 2 rotations
 red-black delete:  at most 3 rotations
```

```
 1,000,000 sequential insertions
   AVL:         ~1,000,000 rotations   (roughly one per insert on sorted input)
   red-black:   ~600,000
   plain BST:   0 rotations, and a chain
```

**That is the trade in one table: AVL gives shorter trees and does more work on writes.**

### The measurement that decides it

```
 read-heavy (95% reads)      AVL wins:  shorter tree, rotations rarely paid
 write-heavy (50%+ writes)   red-black wins: far fewer rotations
 general purpose             red-black — which is why std::map, Java's
                             TreeMap and the Linux scheduler all use it
```

### The rebuild alternative

```
 rotation:  O(1) per fix, applied on every insertion
 rebuild:   O(n), applied occasionally

 rebuilding a 1,000,000-node tree:  ~1,000,000 operations, and the tree is
                                    unusable during it
```

**Rebuilding is right as maintenance and wrong as a strategy** — Ilango unloading the cart. There is a
middle ground, **scapegoat trees**, which rebuild only the subtree that went out of balance and achieve
`O(log n)` amortised with no per-node bookkeeping.

### Treap and skip list

```
 treap        O(log n) EXPECTED, ~25 lines, one random number per node
 skip list    O(log n) EXPECTED, ~40 lines, no rotations at all
 AVL          O(log n) WORST CASE, ~150 lines
 red-black    O(log n) WORST CASE, ~250 lines and famously fiddly deletion
```

```
 probability a treap of 1,000,000 nodes exceeds height 100:  vanishingly small
 (the expected height is ~40, and the tail falls off exponentially)
```

**"Expected" is a real caveat and it almost never bites.** Say it, then say you would still use the treap.

### B-trees, and why databases are different

```
 the cost model changes completely once the data is on disk:

 memory read       ~100 ns
 SSD read          ~100 µs      1,000×
 disk seek         ~10 ms       100,000×

 so the number of NODE VISITS is the cost, and reducing height is everything.
```

```
 1,000,000 keys
   binary tree:              height ~20   ->  20 reads   ->  200 µs on SSD
   B-tree, 500 keys/node:    height  3    ->   3 reads   ->   30 µs
   B-tree, 1,000 keys/node:  height  2    ->   2 reads
```

**A B-tree node is sized to one disk page — typically 4 KB or 16 KB** — so it holds hundreds of keys, and
the tree is three levels deep for a billion rows. That is the answer to "how do real databases avoid the
worst case", and it is not "they use AVL trees".

---

## 7. The traps

### Trap 1 — assuming balance without saying so

```python
    # "BST operations are O(log n)"
```

Only if balanced. **Say `O(height)` and then say what makes the height what it is.** An interviewer who
hears an unqualified `O(log n)` will produce the sorted-input case.

### Trap 2 — checking balance only at the root

```python
    return abs(height(root.left) - height(root.right)) <= 1
```

Balance is required at **every** node. The tree in the picture has a balanced root and is not balanced.
Same whole-subtree distinction as the BST invariant itself.

### Trap 3 — the `O(n²)` balance check

```python
        if abs(height(node.left) - height(node.right)) > 1:
            return False
        return is_balanced(node.left) and is_balanced(node.right)
```

Correct, and `height` walks a whole subtree at every node — `O(n log n)` balanced, `O(n²)` on a chain.
[Day 102's](../day-102-height-and-diameter/README.md) fix: return the height, or a sentinel.

### Trap 4 — a rotation that loses a subtree

```python
    def rotate_right(y):
        x = y.left
        x.right = y             # WRONG ORDER — B is lost
        y.left = x.right
        return x
```

Setting `x.right = y` before rescuing `x.right` throws away the middle subtree. **The order of the two
assignments is the whole rotation**, and getting it wrong silently deletes nodes.

Write it as: *"rescue B, then swing y down."*

### Trap 5 — forgetting to reattach the rotation's result

```python
        rotate_right(node.left)             # result discarded
```

Same trap as [deletion](../day-107-bst-operations/README.md). The rotation returns the new subtree root
and the caller must assign it. Without that, the tree is unchanged and there is no error.

### Trap 6 — updating heights in the wrong order

```python
        _update(x)                          # x first
        _update(y)
```

After a right rotation, `y` is **below** `x`, so `y`'s height must be recomputed first. Updating `x`
first uses `y`'s stale height and the whole tree's heights drift, which silently breaks the balance logic
without breaking the BST property.

### Trap 7 — using one rotation on a zig-zag

```python
    if balance > 1:
        return _rotate_right(node)          # no LR check
```

On a left-right shape, a single right rotation produces the mirror-image right-left shape — still
unbalanced. **Check the direction of the insertion relative to the child**, and do the child rotation
first.

### Trap 8 — offering to implement a red-black tree

You will not finish it, and deletion has cases that are genuinely hard to get right under time pressure.
**Say what you would use instead.** "I would use the language's ordered map; if I had to write one, a
treap or a skip list" is a better answer than a half-finished red-black tree.

---

## 8. In the interview

### How it gets asked

- The pair: *"What is the worst case for a BST? How do real databases avoid it?"*
- The demonstration: *"Show me an input that makes it degenerate."*
- The mechanism: *"What is a rotation, and why is it allowed?"*
- The choice: *"AVL or red-black?"*
- The challenge: *"Implement a self-balancing tree."*

### What to say out loud, in the first ninety seconds

1. **Give the failing input immediately, and say it is ordinary.** "Insert sorted data and every value
   goes to the far right — you get a chain of height `n − 1`. And sorted input is the *normal* case: data
   arrives ordered by id or timestamp far more often than randomly."
2. **Give the number.** "At a million nodes that is a million comparisons instead of twenty — a factor of
   fifty thousand — and a recursive traversal raises `RecursionError` past about a thousand."
3. **Say the one piece of good news.** "A *randomly* built BST is fine — expected height about `2 log n`.
   So the enemy is order, not adversaries."
4. **Define balanced with "every node".** "Height-balanced means the two subtree heights differ by at most
   one at **every** node, not just the root."
5. **Explain a rotation by its property.** "A rotation moves one node up and one down by rewiring three
   pointers, and the reason it is legal is that **it does not change the inorder sequence** — so the tree
   is still a valid BST. It is `O(1)` and it touches nothing outside that subtree."
6. **Say what you would use.** "In production, the language's ordered map, which is a red-black tree. If I
   had to write one here, a treap — twenty-five lines, `O(log n)` expected."

### The follow-ups

**"Show me the input."**
"`for v in range(1, n): insert(tree, v)`. Every value is larger than everything already in the tree, so it
goes to the far right every time, and the result is a chain with height `n − 1` — a linked list with an
unused pointer per node. Reverse-sorted does the same thing to the left. And I would stress that this is
not an adversarial input: data arrives sorted by primary key, by timestamp, by name or by creation order
far more often than it arrives shuffled, so a plain BST built from a database dump degenerates by default.
The one reassuring fact is that a genuinely *random* insertion order gives an expected height of about
`2 log n`, so the problem is order rather than malice."

**"What is a rotation and why is it allowed?"**
"It is a local rearrangement of three pointers that moves a child up and its parent down. Right-rotating
`y` with left child `x`: `x`'s right subtree becomes `y`'s left, `y` becomes `x`'s right, and `x` is the
new subtree root. The reason it is legal is the property worth stating explicitly: **the inorder sequence
is identical before and after.** Before it reads A, x, B, y, C; afterwards it reads A, x, B, y, C. So the
BST invariant still holds — only the shape changed. It is `O(1)`, it touches nothing outside the subtree,
and the caller must reattach the returned node, exactly like the deletion idiom. Two ways to get it wrong:
assigning in the wrong order, which silently discards the middle subtree; and updating cached heights in
the wrong order, since after the rotation the old parent is now the child."

**"AVL or red-black?"**
"They are the same idea with different strictness. **AVL** requires the subtree heights to differ by at
most one at every node, which bounds the height at `1.44 log n` — a shorter tree, so faster lookups — and
it pays for that with more rotations on writes, up to `O(log n)` of them on a delete. **Red-black** uses a
looser colouring rule that bounds the height at `2 log n`, so lookups are slightly slower, but insertion
needs at most two rotations and deletion at most three. For a mixed or write-heavy workload red-black
wins, which is why `std::map`, Java's `TreeMap` and the Linux kernel's scheduler all use it. AVL wins when
reads dominate heavily — an index that is built once and read constantly. And I would say I would not
hand-write either: red-black deletion in particular has cases that are hard to get right under time
pressure."

**"Implement a self-balancing tree."**
"I would write a **treap**, and say why. It is a BST by key and a max-heap by a **random** priority: insert
as a normal leaf, then rotate it upward while its priority exceeds its parent's. Because the priorities
are random, the resulting shape is statistically identical to a randomly built BST — expected height
`O(log n)` — **regardless of the insertion order**, which is exactly the property I need. That is about
twenty-five lines against two hundred and fifty for red-black. The trade I would state honestly is that it
is `O(log n)` **expected**, not worst case — though for a million nodes the probability of exceeding, say,
height 100 is vanishingly small. The other twenty-line option is a **skip list**, which is not a tree at
all — a linked list with random express lanes — and it is what Redis uses for sorted sets."

**"How do real databases avoid this?"**
"They do not use binary trees at all. A database index is a **B-tree**, which is the same balancing idea
with a much higher branching factor: each node is sized to one disk page — typically 4 or 16 kilobytes —
so it holds hundreds of keys rather than one. The reason is the cost model: on disk, the number of **node
visits** is the cost, because a read is ten milliseconds against a hundred nanoseconds in memory. A binary
tree over a million keys has height twenty, so twenty reads. A B-tree with five hundred keys per node has
height three. For a billion rows it is still only four. That reduction in height is the entire point, and
it is why 'use an AVL tree' is the wrong answer to a database question."

**"Is there an alternative to rotating on every insert?"**
"Two. **Rebuild** — flatten the tree to sorted order and rebuild from the middle, which is `O(n)` and
correct and completely wrong as a per-insertion strategy, though perfectly reasonable as occasional
maintenance on a mostly-read structure. And the middle ground, **scapegoat trees**, which do no
bookkeeping at all until a subtree goes too far out of balance, then rebuild just that subtree — `O(log n)`
amortised, no colours or heights stored per node. Worth naming because it shows the design space is not
just 'rotate always or never'."

### A model answer

Asked: *what is the worst case for a BST, and how do real databases avoid it?*

> "The worst case is a **chain**, and the input that produces it is sorted data.
>
> Insert one through a million in order into a plain BST. Every value is larger than everything already
> there, so it goes to the far right, every time, and you end up with a tree of height `n − 1` — a linked
> list with an unused pointer per node. Every operation that was supposed to be twenty comparisons is now a
> million, a factor of fifty thousand, and a recursive traversal raises `RecursionError` at about a
> thousand nodes.
>
> The thing I would emphasise is that this is not an adversarial input. **Data arrives sorted** — by
> primary key, by timestamp, by name, by creation order — far more often than it arrives shuffled. A tree
> built from a database dump degenerates by default. The one reassuring fact is that a genuinely *random*
> insertion order is fine: expected height about `2 log n`. So the enemy is order, not malice.
>
> The fix inside the tree is a **rotation**. It rewires three pointers so that a child moves up and its
> parent moves down, and the reason it is legal is the property everything rests on: **it does not change
> the inorder sequence.** Before and after, the tree reads the same left to right, so it is still a valid
> BST — only the shape has changed. It is `O(1)` and touches nothing outside that subtree. There are four
> cases: two straight ones needing a single rotation, and two zig-zags needing two, because one rotation on
> a zig-zag just gives you the mirror-image zig-zag.
>
> Self-balancing trees rotate on every insertion so the tree never gets far out of shape. **AVL** enforces
> a height difference of at most one at every node, bounding the height at `1.44 log n` — shorter tree,
> faster reads, more rotations on writes. **Red-black** uses a looser rule bounding it at `2 log n`, with at
> most two rotations per insert — which is why it is what `std::map`, Java's `TreeMap` and the Linux
> scheduler actually use.
>
> But for the database half of your question: **they do not use binary trees.** An index is a **B-tree**,
> which is the same balancing idea with a branching factor of hundreds — each node sized to one disk page.
> The reason is the cost model. On disk, the cost is the number of node visits, because a read is ten
> milliseconds against a hundred nanoseconds in memory, so the height *is* the running time. A binary tree
> over a million keys is twenty levels deep, so twenty reads; a B-tree with five hundred keys per node is
> three levels, so three reads. Over a billion rows it is four. That is the whole reason B-trees exist.
>
> And if you asked me to implement something balanced right now, I would not write a red-black tree —
> deletion has cases that are genuinely hard under time pressure. I would write a **treap**: a BST by key
> and a heap by a random priority, about twenty-five lines, which gives the shape of a randomly built tree
> regardless of insertion order. `O(log n)` expected rather than worst case, and I would say so."

---

## 9. Recall card

- **The worst case is a CHAIN, and the input is SORTED DATA — which is the normal case**, since data
  arrives ordered by id or timestamp far more often than randomly. At n = 1,000,000 that is **1,000,000
  comparisons instead of ~20**, plus `RecursionError` past ~1,000. **A randomly built BST is fine**
  (expected height ~`2 log n`): the enemy is order, not adversaries.
- **Balanced means the subtree heights differ by ≤ 1 at EVERY node, not just the root** — and check it in
  **one pass with a sentinel**, because calling `height` at every node is `O(n²)` on a chain.
- **A rotation rewires three pointers to move a child up and its parent down, and it is legal because IT
  DOES NOT CHANGE THE INORDER SEQUENCE.** `O(1)`, touches nothing outside the subtree, and the caller must
  **reattach** the returned root. Four cases: **LL and RR need one rotation; LR and RL are zig-zags and
  need two**, because one rotation on a zig-zag gives the mirror-image zig-zag.
- **AVL: height ≤ `1.44 log n`, faster reads, more rotations on writes. Red-black: height ≤ `2 log n`, ≤ 2
  rotations per insert** — which is why `std::map`, Java's `TreeMap` and the Linux scheduler use it.
  **Do not hand-write either.** Write a **treap** (BST by key, heap by a *random* priority, ~25 lines,
  `O(log n)` **expected**, immune to insertion order) or a **skip list** (what Redis uses for sorted sets).
- **Databases do not use binary trees — they use B-trees**, because on disk the cost is the number of node
  visits (**10 ms a read against 100 ns in memory**). A node is sized to one page and holds hundreds of
  keys: **1,000,000 keys is height 20 in a binary tree and height 3 in a B-tree**; a billion rows is four
  levels.
