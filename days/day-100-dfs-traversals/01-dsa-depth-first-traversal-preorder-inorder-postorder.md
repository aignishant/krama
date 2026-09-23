---
day: 100
track: dsa
title: "Depth-first traversal: preorder, inorder, postorder"
phase: "Trees and binary search trees"
status: written
---

# Day 100 · DSA — Depth-first traversal: preorder, inorder, postorder

**After today you can:** You can write all three recursively and say which problem needs which order.

**The interviewer asks it as:** *Print the tree in inorder. Now do it iteratively.*

---

## 1. What this is, and why they ask it

To **traverse** a tree is to visit every node exactly once. Going **depth-first** means you follow one
branch all the way to the bottom before backing up and trying the next one, and there are exactly three
places you can do the visiting: before the children, between them, or after them.

Three sentences. Those three placements are called **preorder**, **inorder** and **postorder**, and the
only difference between them is **which line of the function the work is on** — the recursion is
identical. They are not three techniques to memorise; they are one technique with the work at three
different moments. And the choice is never arbitrary: **preorder is for anything the parent must decide
before the children, postorder is for anything computed from the children, and inorder gives you a
binary search tree in sorted order.**

They ask it because the recursive versions are four lines each and the iterative versions are genuinely
different from one another — preorder is easy, inorder needs a specific loop shape, and postorder is
awkward enough that there are three standard tricks for it. *"Now do it iteratively"* is one of the most
reliable follow-ups in tree interviews, and it is the point at which people who memorised three
functions come apart.

---

## 2. The story

The wedding date moved.

The hall had a problem with its licence and the whole thing shifted from the eleventh to the
eighteenth, and Krishnan found out on a Monday evening. Everybody had to be told — the caterer, the
lights man, the woman making the sweets, all thirty-odd people who had been given a job.

He did it in about forty minutes and he did it without ringing thirty people.

He rang his four. Told each of them the new date, and told them to tell theirs. Ravi's father rang the
caterer, the two cousins doing the snacks, and the sweet woman, and told them; the caterer rang his
assistant, and the assistant rang the boy.

Each person heard it, and then passed it on. That order mattered. You cannot tell somebody to pass on a
message you have not been given yet.

Three weeks later, after the wedding, they did the accounts, and that went the other way round entirely.

Krishnan wanted one number: what the whole thing had cost. He rang his four and asked. Ravi's father
could not answer. He had not spent the money himself — the caterer had, and the sweet woman had, and the
two cousins had. So he rang them first and asked what each had spent, and only when he had all four
numbers could he add his own and give Krishnan a total for food.

The caterer had the same problem one level further down. He could not say what he had spent until his
assistant had told him, and the assistant could not say until the boy had.

So the answer came up from the bottom. The boy first, then the assistant, then the caterer, then Ravi's
father, then Krishnan. And it took two days rather than forty minutes, because every person had to wait
for everybody under them.

Krishnan's sister said afterwards that it was the same tree of people both times, so why had one taken
forty minutes and the other two days.

Krishnan said it was the same people but the opposite direction. Telling goes down and each person can
speak the moment they hear. Asking goes up and nobody can speak until everyone below them has.

---

## 3. The idea in plain English

Telling the date is a **preorder** traversal. Collecting the accounts is a **postorder** traversal. Same
tree, same visits, opposite moments.

### The three orders are one function with the work in three places

```python
    def walk(node):
        if node is None:
            return
        # A  <- preorder:  visit HERE, before the children
        walk(node.left)
        # B  <- inorder:   visit HERE, between the children
        walk(node.right)
        # C  <- postorder: visit HERE, after the children
```

**That is the entire lesson.** The recursion never changes. Move one line and the order changes.

```
 preorder    node, left, right      "tell them, then pass it on"
 inorder     left, node, right      "left half, me, right half"
 postorder   left, right, node      "hear from everyone below, then speak"
```

Say them as *where the node goes*: **pre** = node first, **in** = node in the middle, **post** = node
last. The children are always left before right in all three.

### Which order for which problem — this is the part that matters

**Preorder — the parent decides something the children need.**

- Copying a tree: you must create a node before you can attach its children to it.
- Serialising a tree: the reader needs the root before it can place anything under it.
- Anything carrying information *down* — a depth, a running path, a running sum, a permitted range.

**Postorder — the answer is computed from the children.**

- Height, size, sum of a subtree: you cannot know yours until you know theirs.
- Deleting a tree: free the children before the parent, or you lose the pointers to them.
- Diameter, balance, maximum path sum — all of
  [days 102](../day-102-height-and-diameter/README.md) and
  [104](../day-104-tree-path-problems/README.md) are postorder.

**Inorder — only interesting for a binary search tree, where it produces sorted order.**

That single fact is why inorder exists as a named thing. In a BST everything left is smaller and
everything right is larger, so "left, me, right" is exactly ascending order. It is the basis of
[validating a BST](../day-108-validating-a-bst/README.md), of finding the *k*-th smallest element, and
of the BST iterator. **On a tree that is not a BST, inorder has no particular meaning**, and saying so
is a good sign.

The one-line test to say out loud:

> **Does the parent need something from the children? Postorder. Do the children need something from the
> parent? Preorder. Is it a BST and do I want sorted order? Inorder.**

### Why the recursion works at all

Because every child is the root of its own subtree, and "visit every node in this tree" is exactly
"visit this node, and visit every node in each subtree". That is
[the leap of faith](../day-087-recursion-leap-of-faith/README.md), and trees are where it stops feeling
like a trick.

The base case is `None`, and it is doing real work: it is both "this branch is empty" and "we have
reached the bottom".

### Doing it without recursion

The recursion is using the call stack to remember where to come back to. To do it iteratively you keep
that stack yourself.

**Preorder is easy**, because you visit a node the moment you meet it:

```python
    stack = [root]
    while stack:
        node = stack.pop()
        visit(node)
        if node.right: stack.append(node.right)      # right FIRST
        if node.left:  stack.append(node.left)       # so left comes off first
```

**Push right before left**, because a stack reverses what you put in it.

**Inorder is the one with a specific shape**, and it is worth learning as a shape rather than deriving
it each time:

```python
    stack, node = [], root
    while stack or node:
        while node:                    # go as far left as possible, remembering the way
            stack.append(node)
            node = node.left
        node = stack.pop()             # nothing further left: this one is next
        visit(node)
        node = node.right              # then do its right subtree
```

The idea in one sentence: **walk left as far as you can, pushing everything you pass; when you cannot go
further left, the top of the stack is the next node in order; then start again from its right child.**

**Postorder is awkward**, because a node must be visited *after* both children — so when you pop it you
do not yet know whether you have already done its right subtree. Three standard answers:

1. **The trick**: do a preorder as *node, right, left*, then **reverse the whole output**. That reversed
   order is exactly `left, right, node`. Two lines longer than preorder, and it is what to write under
   time pressure.
2. **Two stacks**: push to a second stack instead of a list, then drain it. Same idea, more obvious.
3. **The honest one**: keep a `last_visited` pointer, and only visit a node when its right child is
   `None` or was the last thing visited. This is the version to describe if the interviewer says "without
   reversing".

**Say the reversal trick, then offer the honest version.** Interviewers like the trick and then ask
whether you can do it properly.

### The unified template, if you want one function for all three

```python
    stack = [(root, False)]                 # (node, have its children been queued?)
    while stack:
        node, expanded = stack.pop()
        if node is None:
            continue
        if expanded:
            visit(node)                     # second time we see it: do the work
        else:
            # push in REVERSE of the order you want
            stack.append((node.right, False))
            stack.append((node, True))      # <- move this line for pre/in/post
            stack.append((node.left, False))
```

**Moving that one line changes the order**, exactly as in the recursive version. It is slower than the
specialised versions and it is one thing to remember instead of three, which is a fair trade in an
interview.

### Depth-first and breadth-first

All three of today's are **depth-first**: go deep, then back up. The other family is **breadth-first** —
one whole level at a time — which needs a **queue** instead of a stack and is
[tomorrow](../day-101-bfs-level-order/README.md).

The distinction to hold on to: **depth-first costs `O(height)` memory, breadth-first costs `O(width)`.**
For a perfect tree the widest level holds half the nodes, so on a million-node tree depth-first holds
about twenty frames and breadth-first holds half a million nodes.

---

## 4. The picture

One tree, three orders.

```
              1
            /   \
           2     3
          / \   /
         4   5 6

 PREORDER   (node, left, right)   ->  1  2  4  5  3  6
 INORDER    (left, node, right)   ->  4  2  5  1  6  3
 POSTORDER  (left, right, node)   ->  4  5  2  6  3  1
                                                     ^ the root is LAST in postorder
                                      ^ the root is FIRST in preorder
```

The way to read them off a drawing without running any code:

```
 Draw a loop around the whole tree, starting left of the root, going
 anticlockwise, hugging every node. Each node is passed THREE times.

              1
            /   \
           2     3
          / \   /
         4   5 6

 PREORDER:   write a node the FIRST time the loop passes it (on its left)
 INORDER:    write a node the SECOND time (underneath it)
 POSTORDER:  write a node the THIRD time (on its right)

 One drawing, all three answers, and it is how to check yourself in an interview.
```

Krishnan's two jobs, drawn:

```
 TELLING THE DATE (preorder)              COLLECTING THE ACCOUNTS (postorder)
 information flows DOWN                   information flows UP

        Krishnan (1st)                           Krishnan (last)
        /    |    \                              /    |    \
   Father  Meena  Sudhir                    Father  Meena  Sudhir
   (2nd)                                    (after its children)
    /  |  \                                   /  |  \
 Caterer Snacks Sweets                   Caterer Snacks Sweets
 (3rd)                                   (must answer BEFORE Father can)
   |                                        |
 Assistant (4th)                        Assistant
   |                                        |
  Boy (5th)                               Boy (FIRST to answer)

 nobody can pass on a message               nobody can give a total
 they have not received                     until everyone below has
```

The iterative inorder, traced, because the shape is the thing to remember:

```
 tree:        1
             / \
            2   3
           /
          4

 stack   node   action
 ------  -----  -----------------------------------------
 []      1      go left: push 1
 [1]     2      go left: push 2
 [1,2]   4      go left: push 4
 [1,2,4] None   cannot go left -> pop 4, VISIT 4, node = 4.right = None
 [1,2]   None   cannot go left -> pop 2, VISIT 2, node = 2.right = None
 [1]     None   cannot go left -> pop 1, VISIT 1, node = 1.right = 3
 []      3      go left: push 3
 [3]     None   cannot go left -> pop 3, VISIT 3, node = None
 []      None   stack empty and node is None -> done

 output: 4 2 1 3
```

And the postorder trick:

```
 modified preorder:  node, RIGHT, left      ->  1  3  6  2  5  4
 reverse it                                 ->  4  5  2  6  3  1
                                                ^^^^^^^^^^^^^^^^ = postorder
```

---

## 5. The code, built step by step

### Step 1 — write the skeleton once and move one line

```python
    def walk(node):
        if node is None:
            return
        walk(node.left)
        walk(node.right)
```

Then put `out.append(node.val)` in one of the three positions. **Do not memorise three functions.**
Write the skeleton, then decide where the visit goes by asking who needs what.

### Step 2 — say which order the problem wants, and why

"The parent has to exist before I can attach children to it, so this is preorder." / "I cannot know my
height until I know my children's, so this is postorder." **Say the reason, not the name** — the name
is a label on the reason.

### Step 3 — iterative preorder, and the reversal detail

```python
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)        # RIGHT first
        if node.left:
            stack.append(node.left)         # so LEFT is popped first
```

Push right then left. Getting this backwards gives you `node, right, left`, which is a real order — it
is just not the one asked for, and the output looks plausible enough to miss.

### Step 4 — iterative inorder, as a shape

```python
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
```

**Learn these five lines as one unit.** The outer condition is `while stack or node`, and forgetting the
`or node` means the loop never starts, because the stack is empty at the beginning.

### Step 5 — postorder, the trick and the honest version

```python
        # trick: preorder as node, RIGHT, left — then reverse
        out.append(node.val)
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
        ...
        return out[::-1]
```

Then, if asked for it without the reversal:

```python
        peeked = stack[-1]
        if peeked.right and last_visited is not peeked.right:
            node = peeked.right             # right subtree not done yet
        else:
            out.append(peeked.val)
            last_visited = stack.pop()
```

The condition means **"my right subtree is either empty or already finished, so it is my turn"**.

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


# --------------------------------------------------------------------------
# Recursive: ONE function, the visit line in three different places.
# --------------------------------------------------------------------------

def preorder(root: TreeNode | None) -> list[int]:
    """node, left, right. For anything the PARENT must do first:
    copying, serialising, carrying a depth or a path DOWN."""
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        out.append(node.val)                # <- visit BEFORE the children
        walk(node.left)
        walk(node.right)

    walk(root)
    return out


def inorder(root: TreeNode | None) -> list[int]:
    """left, node, right. On a BST this is SORTED ORDER, which is the only
    reason inorder is a named thing."""
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        walk(node.left)
        out.append(node.val)                # <- visit BETWEEN the children
        walk(node.right)

    walk(root)
    return out


def postorder(root: TreeNode | None) -> list[int]:
    """left, right, node. For anything computed FROM the children:
    height, size, subtree sums, deletion, diameter, max path sum."""
    out: list[int] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            return
        walk(node.left)
        walk(node.right)
        out.append(node.val)                # <- visit AFTER the children

    walk(root)
    return out


# --------------------------------------------------------------------------
# Iterative: the interviewer's follow-up.
# --------------------------------------------------------------------------

def preorder_iterative(root: TreeNode | None) -> list[int]:
    """Easiest of the three: visit a node the moment you pop it.

    Push RIGHT before LEFT, because a stack reverses. Getting that backwards
    gives node-right-left, which looks plausible and is wrong.
    """
    if root is None:
        return []
    out: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


def inorder_iterative(root: TreeNode | None) -> list[int]:
    """The one with a specific shape. Learn it as a shape.

    Walk left as far as possible, pushing everything you pass. When you can
    go no further left, the top of the stack is the next node in order.
    Then start again from its right child.

    Note `while stack or node` — with only `while stack` the loop never
    starts, because the stack is empty at the beginning.
    """
    out: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


def postorder_iterative(root: TreeNode | None) -> list[int]:
    """The trick: preorder as node-RIGHT-left, then reverse the output.
    Reversing node-right-left gives left-right-node, which is postorder.

    Two lines longer than preorder. This is what to write under time
    pressure; postorder_iterative_honest is what to describe if the
    interviewer asks for it without the reversal.
    """
    if root is None:
        return []
    out: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:
            stack.append(node.left)         # LEFT first now — deliberately mirrored
        if node.right:
            stack.append(node.right)
    return out[::-1]


def postorder_iterative_honest(root: TreeNode | None) -> list[int]:
    """Genuine postorder, no reversal.

    A node may only be visited when its right subtree is empty or was the
    last thing visited — that is exactly what `last_visited` is tracking.
    """
    out: list[int] = []
    stack: list[TreeNode] = []
    node = root
    last_visited: TreeNode | None = None

    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        peeked = stack[-1]
        if peeked.right is not None and last_visited is not peeked.right:
            node = peeked.right             # right subtree still to do
        else:
            out.append(peeked.val)
            last_visited = stack.pop()
    return out


def traverse(root: TreeNode | None, order: str = "in") -> list[int]:
    """All three from one loop, using a flag meaning "children already queued".

    Move the (node, True) line to change the order — exactly as moving the
    visit line does in the recursive version. Slower than the specialised
    versions; one thing to remember instead of three.
    """
    out: list[int] = []
    stack: list[tuple[TreeNode | None, bool]] = [(root, False)]

    while stack:
        node, expanded = stack.pop()
        if node is None:
            continue
        if expanded:
            out.append(node.val)
            continue
        if order == "pre":
            stack.append((node.right, False))
            stack.append((node.left, False))
            stack.append((node, True))
        elif order == "in":
            stack.append((node.right, False))
            stack.append((node, True))
            stack.append((node.left, False))
        else:                               # post
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
    return out


# --------------------------------------------------------------------------
# Why the order matters: the same walk, three real jobs.
# --------------------------------------------------------------------------

def copy_tree(node: TreeNode | None) -> TreeNode | None:
    """PREORDER: the node must exist before its children can be attached."""
    if node is None:
        return None
    new = TreeNode(node.val)                # create FIRST
    new.left = copy_tree(node.left)
    new.right = copy_tree(node.right)
    return new


def height(node: TreeNode | None) -> int:
    """POSTORDER: cannot know mine until I know both of theirs."""
    if node is None:
        return -1
    left = height(node.left)                # ask the children FIRST
    right = height(node.right)
    return 1 + max(left, right)


def subtree_sums(node: TreeNode | None, out: list[int]) -> int:
    """POSTORDER, and Krishnan's accounts exactly: each total needs the
    totals below it before it can be computed."""
    if node is None:
        return 0
    total = node.val + subtree_sums(node.left, out) + subtree_sums(node.right, out)
    out.append(total)                       # recorded AFTER the children
    return total


def paths_to_leaves(node: TreeNode | None,
                    trail: list[int] | None = None,
                    out: list[list[int]] | None = None) -> list[list[int]]:
    """PREORDER: the path is carried DOWN, so the node is appended before
    the recursion. This is choose-recurse-un-choose from day 094."""
    trail = [] if trail is None else trail
    out = [] if out is None else out
    if node is None:
        return out
    trail.append(node.val)                  # choose (preorder position)
    if node.left is None and node.right is None:
        out.append(trail[:])                # COPY
    else:
        paths_to_leaves(node.left, trail, out)
        paths_to_leaves(node.right, trail, out)
    trail.pop()                             # un-choose
    return out


def kth_smallest(root: TreeNode | None, k: int) -> int | None:
    """INORDER on a BST is sorted order, so this stops after k nodes rather
    than walking the whole tree. O(height + k), not O(n)."""
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


def morris_inorder(root: TreeNode | None) -> list[int]:
    """Inorder in O(1) extra space — no stack and no recursion.

    It temporarily links each node's rightmost left-descendant back to the
    node ("a threaded tree"), walks, then removes the link. Worth being able
    to NAME; rarely worth writing, because it mutates the tree while running,
    which is unsafe if anything else can see it.
    """
    out: list[int] = []
    node = root
    while node:
        if node.left is None:
            out.append(node.val)
            node = node.right
            continue
        predecessor = node.left
        while predecessor.right is not None and predecessor.right is not node:
            predecessor = predecessor.right
        if predecessor.right is None:
            predecessor.right = node        # make the temporary link
            node = node.left
        else:
            predecessor.right = None        # remove it again
            out.append(node.val)
            node = node.right
    return out


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
    root = from_list([1, 2, 3, 4, 5, 6])

    print(preorder(root))       # [1, 2, 4, 5, 3, 6]
    print(inorder(root))        # [4, 2, 5, 1, 6, 3]
    print(postorder(root))      # [4, 5, 2, 6, 3, 1]

    print(preorder_iterative(root) == preorder(root))            # True
    print(inorder_iterative(root) == inorder(root))              # True
    print(postorder_iterative(root) == postorder(root))          # True
    print(postorder_iterative_honest(root) == postorder(root))   # True
    print(morris_inorder(root) == inorder(root))                 # True

    for order in ("pre", "in", "post"):
        print(order, traverse(root, order))

    # a BST: inorder is sorted
    bst = from_list([5, 3, 8, 2, 4, 7, 9])
    print(inorder(bst))                     # [2, 3, 4, 5, 7, 8, 9]  <- sorted
    print(kth_smallest(bst, 3))             # 4

    # the same tree, three jobs
    sums: list[int] = []
    subtree_sums(root, sums)
    print(sums)                             # [4, 5, 11, 6, 9, 21]  <- children first
    print(paths_to_leaves(root))            # [[1,2,4],[1,2,5],[1,3,6]]
    print(inorder(copy_tree(root)) == inorder(root))             # True

    print(preorder(None), inorder(None), postorder(None))        # [] [] []
    single = TreeNode(7)
    print(preorder(single), inorder(single), postorder(single))  # [7] [7] [7]
```

---

## 6. What it costs

### Time

```
 every traversal:  each node is visited exactly once  ->  O(n)
```

**All six functions are `O(n)`, recursive and iterative alike.** There is no order that is faster; they
differ only in *when* the work happens. If an interviewer asks which is fastest, that is the answer.

More precisely, the recursion makes `2n + 1` calls — one per node plus one per `None` child — so the
constant factor includes the empty calls. That is why some implementations check the child for `None`
before recursing rather than at the top of the function; it halves the call count and makes the code
uglier.

### Space

```
 recursive:            O(height) call stack
 iterative pre/in/post O(height) explicit stack
 Morris inorder        O(1)      — no stack at all
 output list           O(n)      — usually not counted as "extra"
```

```
 balanced tree, n = 1,000,000    height ~20     ->  ~20 frames
 degenerate tree, n = 10,000     height 9,999   ->  RecursionError
```

**`O(height)`, not `O(n)`** — and that is the difference from tomorrow's level-order walk, which is
`O(width)`:

```
 perfect tree, n = 1,000,000
   depth-first (today)      ~20 nodes held at once
   breadth-first (tomorrow) ~500,000 nodes held at once
```

**A factor of twenty-five thousand, in opposite directions depending on the shape.** On a degenerate
tree the numbers swap: depth-first holds a million frames and breadth-first holds one node.

### The iterative versions, compared

```
 preorder iterative       one stack, visit on pop            simplest
 inorder iterative        one stack, the go-left loop        the shape to memorise
 postorder by reversal    one stack + one reversal           2 extra lines
 postorder honest         one stack + last_visited pointer   ~6 extra lines
 unified template         one stack of (node, flag) pairs    ~2x slower, one thing to remember
```

The unified version pushes each node twice and allocates a tuple per push, so it is roughly twice as
slow and allocates far more. **Fine in an interview, not what you would ship.**

### Morris traversal, since it always gets mentioned

```
 time   O(n)   — each edge is traversed at most three times, so still linear
 space  O(1)   — no stack, no recursion
```

It achieves `O(1)` by **temporarily modifying the tree**: linking a node's rightmost left-descendant
back to it, then removing the link on the way through. That is the catch worth stating: **the tree is
briefly in an inconsistent state, so it is unsafe if anything else can read the tree concurrently, and
it cannot be used on a read-only structure.**

**Know the name, know the cost, know the catch.** Writing it in an interview is almost never the right
use of ten minutes.

### The recursion limit, stated as a rule

```
 Python default recursion limit: 1000
 -> a recursive traversal fails on any tree taller than ~1000
 -> a tree of n nodes can be up to n tall
```

**If the constraint says `n ≤ 10⁵` and does not promise balance, the recursive version can fail.** Either
write it iteratively or say the risk out loud. Interviewers accept the recursive version plus that
sentence; they do not accept the recursive version plus silence.

---

## 7. The traps

### Trap 1 — pushing left before right in iterative preorder

```python
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
```

A stack reverses, so this produces `node, right, left`. **No error, and the output looks like a
traversal** — just not the one asked for. Check with a three-node tree: `[1,2,3]` must give `1 2 3`, and
this gives `1 3 2`.

### Trap 2 — `while stack` instead of `while stack or node` in iterative inorder

```python
    while stack:                            # WRONG
        while node:
            ...
```

```
 inorder_iterative(root)  ->  []
```

The stack is empty at the start, so the loop body never runs and you get nothing back. The `or node` is
what lets the first iteration happen.

### Trap 3 — thinking inorder means something on a non-BST

Inorder on an arbitrary binary tree produces a valid sequence with no useful property. If a candidate
says "I will use inorder to get the values in sorted order" about a tree that was never a BST, that is
a real misunderstanding. **Inorder is sorted order *because of the BST property*, not because of the
traversal.**

### Trap 4 — using preorder where the answer comes from the children

```python
    def height(node):
        if node is None:
            return -1
        h = 1 + max(...)                    # cannot be computed here
        height(node.left)
        height(node.right)
        return h
```

You cannot compute a height before asking the children. Anything of the form "combine my children's
answers" is postorder, and trying to do it in preorder position produces code that either does not
compile in your head or quietly returns nonsense.

### Trap 5 — freeing a node before its children

```python
    def destroy(node):
        free(node)                          # preorder
        destroy(node.left)                  # the pointer is already gone
```

In a language with manual memory management this is a use-after-free. **Deletion is postorder**, always:
children first, then the parent. Python's garbage collector hides this, which is exactly why it is worth
knowing — it is the standard C++ interview version of the same question.

### Trap 6 — forgetting the copy when carrying a path down

```python
        if is_leaf(node):
            out.append(trail)               # a REFERENCE to the mutating list
```

```
 paths_to_leaves(root)  ->  [[], [], []]
```

[Day 091's](../day-091-subsets/README.md) trap, in a tree. Preorder traversals that carry state down are
backtracking, and they need the copy and the un-choose.

### Trap 7 — recursion on a deep tree

```python
    preorder(chain_of_10000_nodes)
```

```
 RecursionError: maximum recursion depth exceeded
```

Not a hypothetical: a BST built by inserting sorted values is exactly this shape, and it is a common test
case.

### Trap 8 — assuming the traversal order identifies the tree

**One traversal is not enough to reconstruct a tree.** `[1, 2, 3]` as a preorder could be several
different trees. You need **two** traversals, one of which must be inorder — which is
[day 110](../day-110-trees-from-traversals/README.md) — or a traversal that records the `None`s, which is
[day 111](../day-111-serialise-a-tree/README.md). Claiming that preorder alone determines the tree is a
common and confident error.

---

## 8. In the interview

### How it gets asked

- The pair: *"Print the tree in inorder. Now do it iteratively."* LeetCode 94, and 144 and 145 for the
  other two.
- The choice question: *"Which traversal would you use for this, and why?"*
- The BST link: *"Find the k-th smallest element in a BST."* LeetCode 230.
- The space probe: *"Can you do it in `O(1)` space?"*
- The stack probe: *"What is the space complexity of your recursion?"*

### What to say out loud, in the first ninety seconds

1. **Say that it is one function, not three.** "All three traversals are the same recursion with the
   visit on a different line — before the children, between them, or after. So I will write the skeleton
   and then decide where the work goes."
2. **Choose by reason, not by name.** "The parent needs to exist before I attach children, so this is
   preorder." Or: "I cannot compute my answer until I have both children's, so this is postorder."
3. **Say what inorder is actually for.** "Inorder is only interesting on a binary search tree, where it
   gives sorted order. On an arbitrary tree it has no particular meaning."
4. **Give the complexity in both parts.** "`O(n)` time — every node once — and `O(height)` space for the
   stack. That is about twenty frames on a balanced million-node tree and a million on a degenerate
   one."
5. **Flag the recursion limit before they do.** "If the tree can be a chain and `n` is 10⁵, the recursive
   version exceeds Python's limit, so I would either write it iteratively or say I would raise the
   limit."
6. **Offer the iterative version.** "Preorder is the easy one; inorder has a specific loop shape;
   postorder I would do as a reversed node-right-left preorder, and I can do it properly with a
   last-visited pointer if you prefer."

### The follow-ups

**"Now do it iteratively."**
"Which one? They are genuinely different. **Preorder** is easiest: a stack, pop, visit, push right then
left — right first because a stack reverses. **Inorder** has a specific shape: walk left as far as you
can pushing everything you pass, and when you cannot go further left, the top of the stack is the next
node in order; visit it and move to its right child. The detail that catches people is the loop
condition — it has to be `while stack or node`, because the stack is empty when you start, so `while
stack` alone never enters the loop and you get an empty list. **Postorder** is the awkward one, because
when you pop a node you do not know whether its right subtree is done. The quick answer is to do a
preorder as node-right-left and reverse the output — reversing node-right-left gives left-right-node. If
you want it without reversing, I keep a `last_visited` pointer and only visit a node when its right child
is empty or was the last thing visited."

**"Which traversal would you use, and why?"**
"I decide by asking who needs what. If the **parent must do something before the children** — create a
node so children can be attached to it, or carry a depth or a running path downward — that is
**preorder**. If the **answer is computed from the children** — height, subtree size, subtree sum,
diameter, whether the subtree is balanced — that is **postorder**, because you cannot combine answers you
have not asked for yet. And **inorder** if it is a binary search tree and I want the values in sorted
order. Deletion is also postorder, and that one is worth saying because in a language without garbage
collection, freeing a parent before its children is a use-after-free."

**"What is the space complexity?"**
"`O(height)`, not `O(n)` — the stack holds one frame per level of the current path. On a balanced
million-node tree that is about twenty; on a degenerate tree it is a million, and Python's default
recursion limit is a thousand, so a chain of ten thousand nodes raises `RecursionError`. Worth
contrasting with breadth-first, which holds `O(width)` — on a perfect million-node tree the widest level
has half a million nodes, so level-order holds five hundred thousand where depth-first holds twenty. The
two are opposite, and which is cheaper depends entirely on the shape."

**"Can you do it in `O(1)` space?"**
"For inorder, yes — Morris traversal. It temporarily links each node's rightmost left-descendant back to
the node, so it can find its way back up without a stack, then removes the link on the way through.
Still `O(n)` time, because each edge is traversed at most three times. The catch, and I would state it
rather than presenting it as free: **it mutates the tree while running**, so the tree is briefly in an
inconsistent state. That makes it unsafe if anything else can read the tree at the same time, and
impossible on a read-only structure. I would name it as the answer and write the stack version unless you
specifically want it."

**"Find the k-th smallest in a BST."**
"Inorder gives sorted order in a BST, so I walk inorder and stop after `k` nodes. Written iteratively
that is `O(height + k)` rather than `O(n)`, because I never touch the right part of the tree — which is
the real reason to do this iteratively rather than recursively, since a recursive inorder naturally wants
to finish. If the question is asked many times on a changing tree, I would augment each node with the
size of its subtree, which makes each query `O(height)` and makes insertion and deletion maintain one
extra field."

**"Can you rebuild the tree from its preorder traversal?"**
"No, not from one traversal alone — several different trees have the same preorder. You need two, and one
of them must be **inorder**, because inorder is what tells you where the split between the left and right
subtrees is. Preorder plus postorder is not enough for a general binary tree, though it is enough if
every node has zero or two children. The other way to make one traversal sufficient is to record the
`None`s as well — then a single preorder with null markers determines the tree completely, which is how
serialisation works."

### A model answer

Asked: *print the tree in inorder — and then do it iteratively.*

> "First, the thing that makes all three traversals one idea rather than three. The recursion is
> identical in every case: handle `None`, recurse left, recurse right. **The only difference is which
> line the visit is on** — before the children is preorder, between them is inorder, after them is
> postorder. So I write the skeleton and then move one line, rather than remembering three functions.
>
> Inorder specifically is *left, node, right*. And I want to say why anyone cares, because on an
> arbitrary binary tree it has no particular meaning: **on a binary search tree, inorder is sorted
> order**, since everything to the left is smaller and everything to the right is larger. That is the
> whole reason it is a named traversal, and it is the basis of validating a BST, of finding the k-th
> smallest, and of a BST iterator.
>
> Recursively it is four lines. `O(n)` time, because every node is visited once, and `O(height)` space for
> the call stack — about twenty frames on a balanced million-node tree, but a million on a degenerate one,
> and Python's limit is a thousand. So if this tree can be a chain and `n` is large, the recursive version
> is a real risk and I would go iterative anyway.
>
> Iteratively, inorder is the one with a shape worth memorising. I keep a stack and a current node.
> **Walk left as far as I can, pushing every node I pass. When I cannot go further left, the top of the
> stack is the next node in order** — pop it, visit it, and then continue from its right child. Repeat
> until both the stack and the current node are exhausted.
>
> The detail that catches people is the loop condition: it must be `while stack or node`. With `while
> stack` alone the loop never starts, because the stack is empty at the beginning, and the function
> silently returns an empty list.
>
> If you want the other two iteratively: preorder is the easy one — pop, visit, push right then left,
> right first because a stack reverses. Postorder is the awkward one, because when you pop a node you do
> not know whether its right subtree is finished. The quick way is to run a preorder as node-right-left
> and reverse the output, since reversing that gives left-right-node. If you want it done properly I keep
> a `last_visited` pointer and only visit a node once its right child is empty or was the last thing
> visited.
>
> And if you want `O(1)` space for inorder, that is Morris traversal — it threads each node's rightmost
> left-descendant back to the node so it can find its way up without a stack, and unthreads it on the way
> through. Still linear time. The honest caveat is that it mutates the tree while running, so it is unsafe
> if anything else can read the tree concurrently."

---

## 9. Recall card

- **All three traversals are ONE function with the visit line in a different place** — before the
  children (**preorder**: node, left, right), between them (**inorder**: left, node, right), after them
  (**postorder**: left, right, node). Do not memorise three functions; move one line.
- **Choose by reason, not by name. Parent needs to act first → preorder** (copying, serialising, carrying
  a depth/path/range *down*). **Answer computed from the children → postorder** (height, size, sums,
  diameter, balance, and **deletion** — freeing a parent first is a use-after-free). **BST and you want
  sorted order → inorder**; on a non-BST, inorder means nothing.
- **Iterative: preorder pops and visits, pushing RIGHT then LEFT** (a stack reverses). **Inorder is a
  shape** — go left pushing everything, pop when you cannot, then go right — and the condition must be
  **`while stack or node`** or the loop never starts and you get `[]`. **Postorder = node-right-left
  preorder, reversed**; the honest version needs a `last_visited` pointer.
- **`O(n)` time for all of them; `O(height)` space** — ~20 frames on a balanced million-node tree,
  **1,000,000 on a degenerate one** (`RecursionError` past ~1,000). **Depth-first is `O(height)`,
  breadth-first is `O(width)`** — on a perfect million-node tree that is 20 against 500,000, in opposite
  directions depending on shape.
- **Morris inorder is `O(1)` space** by temporarily threading each node's rightmost left-descendant back
  to it — still `O(n)` time, and the catch is that it **mutates the tree while running**. And **one
  traversal never determines the tree**: you need two, one of which must be **inorder**, or a traversal
  that records the `None`s.
