---
day: 99
track: dsa
title: "Binary trees in code"
phase: "Trees and binary search trees"
status: written
---

# Day 099 · DSA — Binary trees in code

**After today you can:** You can define a node class and build a tree by hand for testing.

**The interviewer asks it as:** *Build this tree in code. Now print it.*

---

## 1. What this is, and why they ask it

Yesterday was the words. Today is the four lines of Python that hold a tree, and the two things you will
do with them in every single tree interview: **build a small tree by hand to test on**, and **read the
tree the interviewer has written on the whiteboard**.

Three sentences. A binary tree in code is one class with a value and two references, and there is no
`Tree` object at all — **a tree is a reference to its root node**, and `None` is the empty tree. The
interviewer will hand you a tree written as a flat list like `[3, 9, 20, None, None, 15, 7]`, and that
list is the tree read out **level by level, including the gaps**, which is a format worth being able to
convert both ways without thinking. And a node has no reference to its parent unless you add one, which
is the single most consequential fact about the structure.

They ask it because a candidate who cannot construct a test tree in thirty seconds ends up debugging
their algorithm on the interviewer's one example, in their head, with no way to try anything. It is the
plumbing, and being slow at plumbing costs you the part of the round where you were supposed to be
thinking.

---

## 2. The story

The school sent a message home in June saying that if the school ever had to shut suddenly, there was
now a chain for telling people, and Sudha's mother had been put in it.

The way it worked was this. The headmistress rang two people. Those two each rang two more. Those four
each rang two more, and so on down, until everybody had been rung. Nobody had to make more than two
calls, and the whole school of about two hundred and forty families would know inside twenty minutes.

Sudha's mother was one of the four in the third row, and she had two names under her: Mrs Pillai and a
number that belonged to a family in the flats behind the temple.

In August they tried it out on a Saturday morning to see whether it worked, and it mostly did, except
for one thing.

Somebody in the second row had moved to Bangalore in July. Her two names had been given to somebody
else, but nobody had told the woman above her, so the woman above her rang a number that no longer
worked, said "no answer", and stopped. Eleven families never got the call.

At the meeting afterwards they decided that everyone should have the whole chain, not just their own
two names, so that if a call did not connect you could go round it.

That turned out to be harder than anybody expected, because saying the chain out loud on the phone is
not easy. Sudha's mother tried it with a neighbour and got confused within about a minute, because she
was going down one branch all the way to the bottom and then coming back up, and the neighbour could not
tell where she was.

The teacher who had made the chain in the first place had a better way. She read it **row by row**. The
headmistress. Then the two people she calls. Then those two people's four. Then the eight.

And the important part, which she was strict about, was that when somebody in a row had nobody under
them, you still said so. You said "nobody" and moved on. Because if you skipped them, the person
listening would put the next name in the wrong place and the whole row after that would be shifted
across by one.

Nobody, nobody, then the next two names.

Read that way, on the phone, in order, with the gaps said out loud, a person could write down the entire
chain correctly the first time.

---

## 3. The idea in plain English

The phone chain is a binary tree, and the teacher's rules are the two things you have to be able to do
with one in code.

### The node, which is the whole data structure

```python
class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: "TreeNode | None" = None
        self.right: "TreeNode | None" = None
```

Four lines. **There is no `Tree` class.** A tree *is* a node — the root — and every node is the root of
its own subtree. `None` means "no subtree here", which is both "this branch is empty" and "the whole
tree is empty", depending on where you are.

That double meaning is deliberate and useful: every tree function's base case is `if node is None`, and
it correctly handles both an empty tree and the bottom of a branch with the same line.

**LeetCode's version has a different constructor**, and knowing it saves you thirty seconds:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val                      # `val`, not `value`
        self.left = left
        self.right = right
```

`val`, and the children can be passed in. Use their names when solving their problems; nothing is more
irritating than an `AttributeError` on `.value` at minute twenty.

### Building one by hand

Two ways, and you want the second.

**Nested, which reads like the tree looks:**

```python
    root = TreeNode(3,
                    TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))
```

Indent it so the shape is visible and it is genuinely readable. One expression, no temporary names.

**Assignment, which is what you write when the shape is irregular:**

```python
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
```

Verbose, but you can put a node anywhere without restructuring the expression. **Use nested for a tree
you are typing once, and assignment for a tree you are going to modify.**

### The list format, which is what the interviewer will hand you

```
 [3, 9, 20, None, None, 15, 7]
```

That is the tree **read level by level, left to right, with `None` for every missing child** — the
teacher's rule about saying "nobody" out loud.

```
        3
       / \
      9   20
         /  \
        15   7

 level 0:  3
 level 1:  9, 20
 level 2:  None, None, 15, 7      <- 9's two missing children ARE recorded
```

**The `None`s are load-bearing.** Drop them and 15 and 7 become 9's children instead of 20's, which is a
different tree. That is exactly the mistake the neighbour made with the phone chain.

Two things to know about the format, because both come up:

- **LeetCode trims trailing `None`s.** `[1, 2]` means a root with only a left child; there is no need to
  write `[1, 2, None]`.
- **It is not the array-index formula.** For a *complete* tree you can store a tree in an array where
  node `i`'s children are at `2i + 1` and `2i + 2` — that is the [heap](../day-113-the-heap/README.md)
  layout, and it is compact. But for a sparse tree that wastes a catastrophic amount of space: a
  degenerate tree of 20 nodes needs an array of about a million entries. **LeetCode's format skips the
  gaps below a `None`, so it stays proportional to the number of nodes.**

### The fact that decides everything: no parent pointer

```python
    node.left      # yes
    node.right     # yes
    node.parent    # AttributeError — it does not exist
```

A node knows its children and **nothing about who points at it**. Three consequences that come up
constantly:

1. **You cannot go up.** Anything needing an ancestor either passes information down as an argument, or
   reconstructs the path on the way back up the recursion.
2. **You cannot delete a node given only that node.** You need its parent to change a pointer, so
   deletion functions take the root and search from the top.
3. **A node cannot know its own depth.** Depth is carried down;
   [yesterday's](../day-098-what-a-tree-is/README.md) asymmetry, restated as a fact about the object.

You *can* add a `parent` field, and some designs do — a doubly linked tree. The price is that every
insertion and every removal has to maintain it, and a stale parent pointer is a silent bug. **Do not add
one in an interview unless the problem needs it; say instead that you would carry the parent as an
argument.**

### Printing a tree, which you will want within five minutes

Three ways, in increasing order of usefulness:

```python
    print(root.value, root.left.value, root.right.value)    # useless past 3 nodes
```

```python
    def as_list(node):                      # matches the interviewer's format
        ...                                 # level order with Nones
```

```python
    def show(node, indent=0):               # sideways, and instantly readable
        if node is None:
            return
        show(node.right, indent + 1)
        print("    " * indent + str(node.value))
        show(node.left, indent + 1)
```

**That third one is nine lines and it is the best thirty seconds you can spend in a tree interview.** It
prints the tree rotated ninety degrees — right subtree on top, root in the middle, left subtree below —
so you can actually see what your code built. Write it once, remember it.

### The equality trap

```python
    TreeNode(1) == TreeNode(1)              # False
```

Two nodes with the same value are different objects, and Python compares objects by identity unless you
say otherwise. That is *correct* — a tree is about structure, not values — and it is why
[comparing two trees](../day-103-tree-comparisons/README.md) is its own problem with its own recursion,
rather than a `==`.

The same applies to `in`, to `set()`, and to using a node as a dictionary key: they all work, and they
all work **by identity**, which is usually what you want and occasionally is not.

---

## 4. The picture

The object graph, drawn as it is in memory. This is what "a tree is a reference to its root" means.

```
   root ──────► +-------------+
                | value:  3   |
                | left:   ●───┼──────► +-------------+
                | right:  ●───┼──┐     | value:  9   |
                +-------------+  │     | left:  None |
                                 │     | right: None |
                                 │     +-------------+
                                 │
                                 └───► +-------------+
                                       | value: 20   |
                                       | left:   ●───┼─────► +-------------+
                                       | right:  ●───┼──┐    | value: 15   |
                                       +-------------+  │    | left:  None |
                                                        │    | right: None |
                                                        │    +-------------+
                                                        └──► +-------------+
                                                             | value:  7   |
                                                             +-------------+

 Nothing points UPWARD. Every arrow goes down.
 `root` is an ordinary variable; lose it and the whole tree is unreachable.
```

The list format, and why the `None`s matter:

```
        3                    correct:  [3, 9, 20, None, None, 15, 7]
       / \
      9   20                 dropped:  [3, 9, 20, 15, 7]
         /  \                          reads as:
        15   7                                3
                                             / \
                                            9   20
                                           / \
                                          15  7        <- a DIFFERENT tree

 level 0:   3                     index 0
 level 1:   9        20           children of 3
 level 2:   _   _    15   7       children of 9 (both missing), then children of 20
            ^^^^^
            these two Nones are what keep 15 and 7 under 20
```

The sideways printer's output, which is what you actually look at while debugging:

```
    show(root)  prints:

            7
        20
            15
    3
        9

 read it with your head tilted left:
   - the deeper a node, the further right it is printed
   - the RIGHT subtree appears ABOVE, the left below
   - a 12-node tree fits on a screen; a horizontal drawing does not
```

Building the same tree three ways:

```
 NESTED                          ASSIGNMENT                    FROM A LIST
 root = TreeNode(3,              root = TreeNode(3)            root = from_list(
   TreeNode(9),                  root.left = TreeNode(9)         [3,9,20,None,None,15,7])
   TreeNode(20,                  root.right = TreeNode(20)
     TreeNode(15),               root.right.left = TreeNode(15)
     TreeNode(7)))               root.right.right = TreeNode(7)

 one expression                  one node per line             one line, and it
 shape is visible                easy to modify                matches the problem
 hard to change                  verbose                       write it ONCE, reuse
```

---

## 5. The code, built step by step

### Step 1 — the node, with LeetCode's names

```python
class TreeNode:
    def __init__(self, val: int = 0,
                 left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right
```

**`val`, and children in the constructor.** Matching their names means you can paste a solution straight
in, and it makes the nested building style possible in one expression.

### Step 2 — `__repr__`, which pays for itself immediately

```python
    def __repr__(self) -> str:
        return f"TreeNode({self.val})"
```

Without it, printing a list of nodes gives you `[<__main__.TreeNode object at 0x7f8b...>, ...]`, which
tells you nothing. One line, and every debugging print becomes readable.

### Step 3 — from a list, which you write once and reuse for ever

```python
    def from_list(values):
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            ...
```

The idea: **walk the list left to right, and give each value in turn to the next node that is waiting
for a child.** A queue holds the nodes waiting. Every node consumes exactly two entries from the list —
its left and its right — and a `None` entry means "no child", so nothing is enqueued for it.

That "nothing is enqueued for a `None`" is exactly why the format stays compact: a missing node has no
children to describe.

### Step 4 — back to a list, which is how you check your work

```python
        while queue:
            node = queue.popleft()
            if node is None:
                out.append(None)
                continue
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
```

Note this enqueues `None`s deliberately, so that the gaps are recorded. Then trim the trailing `None`s
at the end, to match LeetCode.

**Being able to go both ways is what lets you test.** Build from the interviewer's list, run your
function, convert back, and compare with what they expect.

### Step 5 — the sideways printer

```python
    def show(node, indent=0):
        if node is None:
            return
        show(node.right, indent + 1)                # right subtree ABOVE
        print("    " * indent + str(node.val))
        show(node.left, indent + 1)                 # left subtree BELOW
```

Right, then self, then left — a **reverse in-order** walk, which is
[tomorrow's](../day-100-dfs-traversals/README.md) subject arriving early. Nine lines, and it is the
difference between debugging by reasoning and debugging by looking.

### The complete solution

```python
from collections import deque


class TreeNode:
    """A binary tree node. Field names match LeetCode's (`val`, not `value`)
    so that solutions paste straight in.

    There is no Tree class. A tree IS a reference to its root, and `None` is
    the empty tree — which is also what "no child here" means, which is why
    one base case handles both.
    """

    def __init__(self, val: int = 0,
                 left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"      # or debugging prints are unreadable


def from_list(values: list[int | None]) -> TreeNode | None:
    """Build a tree from LeetCode's level-order-with-gaps format.

    [3, 9, 20, None, None, 15, 7]  ->
            3
           / \
          9   20
             /  \
            15   7

    Walk the list left to right; each waiting node consumes the next TWO
    entries as its children. A None entry creates no node and therefore
    enqueues nothing, which is why the format stays proportional to the
    number of real nodes rather than to 2^height.

    Write this ONCE. You will use it in every tree problem you ever practise.
    """
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def to_list(root: TreeNode | None) -> list[int | None]:
    """The inverse. Enqueues None deliberately so gaps are recorded, then
    trims the trailing Nones to match LeetCode's output."""
    if root is None:
        return []

    out: list[int | None] = []
    queue: deque[TreeNode | None] = deque([root])

    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)

    while out and out[-1] is None:          # LeetCode trims trailing gaps
        out.pop()
    return out


def show(node: TreeNode | None, indent: int = 0) -> None:
    """Print the tree rotated 90 degrees: right subtree above, left below.

    Nine lines, and the single most useful debugging tool in this topic —
    a 12-node tree fits on a screen where a horizontal drawing does not.
    """
    if node is None:
        return
    show(node.right, indent + 1)
    print("    " * indent + str(node.val))
    show(node.left, indent + 1)


def build_nested() -> TreeNode:
    """One expression, indented so the shape is visible.
    Use this for a tree you type once."""
    return TreeNode(3,
                    TreeNode(9),
                    TreeNode(20,
                             TreeNode(15),
                             TreeNode(7)))


def build_by_assignment() -> TreeNode:
    """One node per line. Use this when the shape is irregular or when you
    are going to modify it afterwards."""
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    return root


def find(node: TreeNode | None, target: int) -> TreeNode | None:
    """Find a node by value in a PLAIN binary tree: O(n).

    You must search both sides, because nothing about the values tells you
    which way to go. That is only O(log n) in a binary SEARCH tree.
    """
    if node is None:
        return None
    if node.val == target:
        return node
    return find(node.left, target) or find(node.right, target)


def find_with_parent(node: TreeNode | None, target: int,
                     parent: TreeNode | None = None
                     ) -> tuple[TreeNode | None, TreeNode | None]:
    """A node has NO parent pointer, so if you need the parent you carry it
    down as an argument. This is the standard workaround, and it is what you
    should say rather than adding a `parent` field."""
    if node is None:
        return None, None
    if node.val == target:
        return node, parent
    found, p = find_with_parent(node.left, target, node)
    if found:
        return found, p
    return find_with_parent(node.right, target, node)


def insert_level_order(root: TreeNode | None, value: int) -> TreeNode:
    """Add a node at the first free position, level by level.

    This is how you grow a COMPLETE tree, and it is the only "insert" that
    makes sense for a plain binary tree — a binary SEARCH tree inserts by
    value instead, which is day 107.
    """
    node = TreeNode(value)
    if root is None:
        return node

    queue = deque([root])
    while queue:
        current = queue.popleft()
        if current.left is None:
            current.left = node
            return root
        queue.append(current.left)
        if current.right is None:
            current.right = node
            return root
        queue.append(current.right)
    return root


def equal(a: TreeNode | None, b: TreeNode | None) -> bool:
    """Two nodes with the same value are DIFFERENT objects, so `==` is
    identity and structural comparison needs its own recursion. Day 103."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and equal(a.left, b.left) and equal(a.right, b.right)


def copy_tree(node: TreeNode | None) -> TreeNode | None:
    """A deep copy. Note that `root2 = root1` copies the REFERENCE — both
    names then point at the same tree and a change through one is visible
    through the other."""
    if node is None:
        return None
    return TreeNode(node.val, copy_tree(node.left), copy_tree(node.right))


if __name__ == "__main__":
    values = [3, 9, 20, None, None, 15, 7]
    root = from_list(values)

    print(to_list(root))                    # [3, 9, 20, None, None, 15, 7]
    print(to_list(root) == values)          # True — the round trip works

    show(root)
    #         7
    #     20
    #         15
    # 3
    #     9

    print(equal(root, build_nested()))              # True
    print(equal(root, build_by_assignment()))       # True

    print(TreeNode(1) == TreeNode(1))               # False — identity, not value
    print(equal(TreeNode(1), TreeNode(1)))          # True  — structure

    node, parent = find_with_parent(root, 15)
    print(node, parent)                             # TreeNode(15) TreeNode(20)

    print(to_list(from_list([1, 2])))               # [1, 2]  — trailing Nones trimmed
    print(from_list([]), from_list([None]))         # None None

    lopsided = None
    for v in (1, 2, 3, 4, 5, 6):
        lopsided = insert_level_order(lopsided, v)
    print(to_list(lopsided))                        # [1, 2, 3, 4, 5, 6]

    copy = copy_tree(root)
    copy.val = 999
    print(root.val, copy.val)                       # 3 999 — genuinely separate

    alias = root
    alias.val = 42
    print(root.val)                                 # 42 — the reference trap
```

---

## 6. What it costs

### Space per node

```
 Python object header                  ~16 bytes
 __dict__ for three attributes         ~104 bytes
 the three references themselves       included above
 ------------------------------------------------
 one TreeNode                          ~120 bytes
```

```
 1,000,000 nodes  ×  ~120 B  =  ~120 MB
```

**A million-node tree is about 120 MB in Python**, and almost all of it is object overhead rather than
data. `__slots__` cuts it substantially:

```python
class TreeNode:
    __slots__ = ("val", "left", "right")    # ~56 bytes per node instead of ~120
```

Worth knowing and worth mentioning; not worth writing in an interview unless memory is the question.

Compare with the array layout that a [heap](../day-113-the-heap/README.md) uses:

```
 pointer-based tree, 1M nodes    ~120 MB   works for ANY shape
 array-based complete tree, 1M    ~8 MB    only for a COMPLETE tree
```

**Fifteen times smaller, and it only works for one shape.** That is the trade the heap makes, and it is
why heaps are stored in arrays and general trees are not.

### The operations

```
 from_list(k values)      O(k)          each value handled once
 to_list(n nodes)         O(n)          plus up to n+1 Nones enqueued
 show(n nodes)            O(n)
 find in a plain tree     O(n)          both sides must be searched
 insert_level_order       O(n)          scans levels for the first gap
 copy_tree                O(n)
 equal                    O(n)          stops early on the first difference
```

**Everything is `O(n)`, and `find` being `O(n)` is the one to say out loud**, because people expect
`O(log n)` from anything shaped like a tree. You only get `O(log n)` in a binary *search* tree, and only
while it is balanced.

### Why the array format would be a disaster for sparse trees

The index formula — children of `i` at `2i + 1` and `2i + 2` — needs a slot for every possible position:

```
 array size needed = 2^(height+1) - 1

 a COMPLETE tree of 1,000 nodes       ->  ~1,024 slots        99% used
 a DEGENERATE tree of 20 nodes        ->  2^21 = 2,097,151    0.001% used
 a degenerate tree of 40 nodes        ->  ~1.1 × 10^12        impossible
```

**Forty nodes, a trillion slots.** LeetCode's format avoids this entirely by not describing the children
of a `None`, so its length is proportional to the number of real nodes plus their missing children —
`O(n)`, not `O(2ʰ)`.

### Recursion depth

```
 show, copy_tree, equal, find:  O(height) stack

 balanced 1M-node tree     ~20 frames
 degenerate 10,000-node    10,000 frames  ->  RecursionError
```

Same warning as yesterday, and it applies to every helper on this page.

---

## 7. The traps

### Trap 1 — `val` versus `value`

```python
    root.value
```

```
 AttributeError: 'TreeNode' object has no attribute 'value'
```

LeetCode's class uses `val`. If you define your own with `value` and then paste in one of their
snippets, or write a solution against `val` and test with your own class, you get this at minute twenty
when you least want it. **Pick `val` and never think about it again.**

### Trap 2 — dropping the `None`s from the list format

```
 [3, 9, 20, 15, 7]        is NOT   [3, 9, 20, None, None, 15, 7]
```

The first puts 15 and 7 under 9; the second puts them under 20. **No error, a different tree, and every
answer wrong.** The gaps are part of the description, exactly as the teacher insisted.

### Trap 3 — assignment copies the reference, not the tree

```python
    backup = root
    backup.val = 999
    print(root.val)                         # 999 — there was never a backup
```

`backup` and `root` are two names for one object. A real copy is a recursive walk, or
`copy.deepcopy(root)`. This is the same reference trap as
[day 091's](../day-091-subsets/README.md) `current[:]`, wearing a tree costume.

### Trap 4 — expecting `==` to compare structure

```python
    TreeNode(1) == TreeNode(1)              # False
    build_nested() == build_by_assignment() # False, and they ARE the same tree
```

Python compares by identity. Structural comparison is its own recursion. This trips people writing tests
more than it trips people writing solutions.

### Trap 5 — reaching for `.parent`

```python
    node.parent
```

```
 AttributeError: 'TreeNode' object has no attribute 'parent'
```

There is no parent pointer. **Carry the parent down as an argument** — which is four extra characters —
rather than adding a field you then have to maintain on every insertion and deletion.

### Trap 6 — assuming the values are unique

```python
    def find(node, target): ...
```

Nothing says the values in a binary tree are distinct. `find` returns the first match in its traversal
order, which may not be the one meant. **Ask** — "are values unique?" — because the answer changes
several problems, including
[lowest common ancestor](../day-105-lowest-common-ancestor/README.md).

### Trap 7 — the index formula on a sparse tree

```python
    tree = [None] * (2 ** (height + 1) - 1)     # for a degenerate tree of 40 nodes
```

```
 MemoryError
```

The array layout only works for complete trees. For anything else it is exponential in the height, and
forty nodes is already a trillion slots.

### Trap 8 — building a test tree that is too symmetric

```python
    root = TreeNode(1, TreeNode(2), TreeNode(3))
```

Perfectly balanced, three nodes, both children present everywhere. It will pass almost any wrong
solution. **A good test tree is lopsided, has a node with exactly one child, and has a value repeated**
— because the one-child case is where `min`, `max` and null-handling bugs live.

```python
    root = from_list([1, 2, 3, None, 4, None, None, 5])     # asymmetric, one-child, deep
```

---

## 8. In the interview

### How it gets asked

- The plumbing question, usually first: *"Build this tree in code."*
- The follow-up: *"Now print it so I can see it."*
- The format question: *"What does `[3, 9, 20, null, null, 15, 7]` mean?"*
- The design probe: *"Would you add a parent pointer?"*
- The trap: *"Find the node with value 15."* — checking whether you say `O(n)` or wrongly say
  `O(log n)`.

### What to say out loud, in the first ninety seconds

1. **Say what a tree is, as an object.** "There is no `Tree` class — a tree is a reference to its root
   node, and `None` is the empty tree. That is also what 'no child here' means, which is why one base
   case handles both."
2. **Use their field names.** "I will use `val`, `left` and `right`, matching the standard definition."
3. **Read the list format out loud.** "That list is the tree level by level, left to right, with `null`
   for missing children. The nulls matter — dropping them moves 15 and 7 under 9 instead of 20."
4. **Say the parent fact before it bites.** "Nodes have no parent pointer, so anything needing an
   ancestor either carries it down as an argument or reconstructs it on the way back up."
5. **Build a deliberately awkward test tree.** "I will make it lopsided with a node that has exactly one
   child, because that is where the null-handling bugs are."
6. **Write the printer.** "Let me spend thirty seconds on a sideways print so we can both see what the
   code is doing."

### The follow-ups

**"What does `[3, 9, 20, null, null, 15, 7]` mean?"**
"It is the tree read level by level, left to right, and every missing child is written as `null`. So the
root is 3; level one is 9 and 20; level two is 9's two children, both missing, then 20's children, 15
and 7. The nulls are load-bearing — if you drop them, 15 and 7 become children of 9 and it is a
completely different tree with no error to tell you. Two details: trailing nulls are trimmed, so `[1, 2]`
is a root with only a left child. And it is **not** the array-index layout where node `i`'s children are
at `2i + 1` and `2i + 2` — that one needs a slot for every possible position, so a degenerate tree of
forty nodes would need about a trillion entries. This format describes no children for a null, so its
length stays proportional to the number of real nodes."

**"Would you add a parent pointer?"**
"Not by default. It is genuinely useful for a few things — walking up from a node, deleting a node you
already hold, finding a successor in a BST iterator — but it has to be maintained on every insertion,
deletion and rotation, and a stale parent pointer is a silent bug that shows up somewhere far from where
it was created. In an interview I would instead carry the parent down as an argument, which is four
characters and cannot go stale. I would add the field if the problem required repeated upward traversal
from arbitrary nodes, and then I would say that maintaining it is now part of every mutation."

**"Find the node with value 15."**
"`O(n)`, and I want to be explicit about that because the shape suggests otherwise. In a plain binary
tree nothing about the values tells me which way to go, so I have to search the left subtree and, if it
is not there, the right — worst case every node. It is only `O(log n)` in a binary **search** tree, where
the ordering lets one comparison discard half the tree, and even then only while the tree is balanced.
One thing I would ask: are the values unique? If not, 'the node with value 15' is ambiguous and I would
need to know whether you want the first in traversal order or all of them."

**"How would you test your solution?"**
"I write two helpers first and reuse them for every tree problem. `from_list`, which builds a tree from
the level-order format you gave me, and `to_list`, which converts back — so I can build your example,
run my function, convert the result, and compare against what you expect. Then a nine-line sideways
printer that draws the tree rotated ninety degrees, right subtree above and left below, so I can see
what I actually built rather than reason about it. And I deliberately make my test tree awkward:
lopsided, with at least one node that has exactly one child and one repeated value. A perfectly balanced
three-node tree passes almost any wrong solution."

**"How much memory does a million-node tree use?"**
"In Python, roughly 120 MB — about 120 bytes a node, and most of that is object overhead rather than the
data. `__slots__` would take it to about 56 bytes a node. Worth comparing against the array layout used
by a heap: a complete tree of a million integers is about 8 MB with no pointers at all, so fifteen times
smaller — but that only works because a heap is always complete. The moment the tree can be sparse, the
array layout needs a slot for every possible position and becomes exponential in the height. That trade —
compact but shape-restricted, versus general but pointer-heavy — is the whole reason heaps and binary
search trees are stored differently."

### A model answer

Asked: *build this tree in code, then print it.*

> "First, what I am building. There is no `Tree` class — **a tree is a reference to its root node**, and
> `None` is the empty tree. That double meaning is useful rather than sloppy: `None` also means 'no child
> here', so a single base case, `if node is None`, correctly handles both the empty tree and the bottom of
> every branch.
>
> The node is four lines: a value and two references, `left` and `right`. I will call the value field
> `val` rather than `value`, because that is the standard definition and it means anything you hand me
> pastes straight in. I will also add a one-line `__repr__`, because without it printing a list of nodes
> gives me memory addresses and tells me nothing.
>
> The tree you have written as `[3, 9, 20, null, null, 15, 7]` is level order, left to right, with a
> `null` for each missing child. So: root 3; then its children 9 and 20; then 9's two children, which are
> both missing, and then 20's children, 15 and 7. **Those two nulls are doing real work** — if I dropped
> them the list would read as 15 and 7 being 9's children, which is a different tree and there would be
> no error to warn me.
>
> I will write `from_list` once rather than typing trees by hand, because I will reuse it for every tree
> problem. It walks the list left to right with a queue of nodes waiting for children; each waiting node
> consumes the next two entries. A `null` entry creates no node and therefore enqueues nothing, which is
> exactly why this format stays proportional to the number of real nodes instead of exploding like the
> array-index layout would.
>
> Then thirty seconds on a printer, because I would rather look at the tree than reason about it. Nine
> lines: recurse right with one more level of indent, print the value, recurse left. That draws the tree
> rotated ninety degrees — right subtree above, left below, depth going rightwards — and a dozen nodes fit
> on a screen where a proper drawing would not.
>
> Two things I would flag before we go further. **Nodes have no parent pointer**, so anything that needs
> an ancestor either carries it down as an argument or rebuilds the path on the way back up — I would not
> add a `parent` field unless the problem needs repeated upward walks, because then every mutation has to
> maintain it. And when I make my own test tree I will make it deliberately awkward: lopsided, with a node
> that has exactly one child, because a symmetric three-node tree will pass almost any wrong solution and
> the one-child case is where the bugs are."

---

## 9. Recall card

- **Four lines: `val`, `left`, `right`. There is no `Tree` class — a tree is a reference to its root, and
  `None` is both "empty tree" and "no child here"**, which is why one base case handles both. Use
  **`val`**, not `value`, and add a one-line `__repr__` or every debugging print is a memory address.
- **`[3, 9, 20, null, null, 15, 7]` is level order with a `null` for every missing child, and the nulls
  are load-bearing** — drop them and 15 and 7 move under 9, silently. Trailing nulls are trimmed. It is
  **not** the `2i+1 / 2i+2` array layout: that needs `2^(h+1)−1` slots, so a **degenerate tree of 40
  nodes would need ~10¹² entries**.
- **Write `from_list` and `to_list` once and reuse them for every tree problem**, plus the **nine-line
  sideways printer** (recurse right, print, recurse left) — the best thirty seconds available in a tree
  round. Make test trees **lopsided, with a one-child node and a repeated value**; a symmetric three-node
  tree passes almost any wrong solution.
- **There is no parent pointer.** So you cannot go up, cannot delete a node given only that node, and a
  node cannot know its own depth. **Carry the parent down as an argument** rather than adding a field
  that every mutation must maintain.
- **`TreeNode(1) == TreeNode(1)` is `False`** — Python compares identity, so structural equality is its
  own recursion — and **`backup = root` copies the reference, not the tree**. `find` in a plain binary
  tree is **`O(n)`**, not `O(log n)`. A million nodes is **~120 MB** in Python (~56 with `__slots__`),
  against **~8 MB** for the same as a complete-tree array.
