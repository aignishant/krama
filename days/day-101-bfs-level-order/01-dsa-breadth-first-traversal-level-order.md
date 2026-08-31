---
day: 101
track: dsa
title: "Breadth-first traversal: level order"
phase: "Trees and binary search trees"
status: written
---

# Day 101 · DSA — Breadth-first traversal: level order

**After today you can:** You can process a tree level by level and know exactly where the level boundary is.

**The interviewer asks it as:** *Print the tree level by level. Now print each level as its own list.*

---

## 1. What this is, and why they ask it

**Breadth-first traversal** visits every node at depth 0, then every node at depth 1, then depth 2, and
so on. It is the other way of walking a tree — [yesterday's](../day-100-dfs-traversals/README.md) three
orders all went deep first, and this one goes wide.

Three sentences. It uses a **queue** where depth-first used a stack, and that single swap is the whole
difference. The version that prints the values in level order is six lines and everybody gets it; the
version that returns **each level as its own list** requires knowing where one level ends and the next
begins, and there is exactly one clean way to do that. And breadth-first is not an alternative to
depth-first — **it is the right answer for a specific family of questions**, the ones about levels,
about the shallowest anything, and about shortest paths.

They ask it because the follow-up — *"now group them by level"* — separates people. The answer is one
line: **capture the length of the queue before you start draining it.** That number is exactly one level,
because everything you add during the loop belongs to the next one. Candidates who have not seen the
trick invent something with sentinel values or a dictionary keyed by depth, both of which work and both
of which are three times the code.

---

## 2. The story

The tanker came on Tuesdays and Fridays at about six in the morning, and by half past five there were
already thirty people standing with pots.

Selvam had been given the job of managing it after the argument in April, which had been about exactly
one thing: some families were getting three pots and some were getting none.

What had been happening was obvious once you watched it. A man would fill his pot, walk twenty steps to
his house, put it down, and come straight back and join the end of the queue with a second pot. The
queue never got shorter. People who had been standing there since half past five were still standing
there at seven, because there was always somebody rejoining the back.

Selvam's rule was very simple and he announced it every time before he started.

He would look at the line and count it. Not roughly — he counted heads, out loud, and then he said the
number. Forty-one. And then he said: forty-one people, one pot each, and when I have done forty-one I
stop and count again.

Anyone who joined after he had counted was not part of that forty-one. They were part of the next count.
It did not matter that they were standing in the same line — the number had already been fixed.

So it went in rounds. Forty-one, then he counted again and it was twenty-six, then nine, then four.
Everybody in a round got one pot before anybody got a second one.

The part he was strict about was the counting. He would not let himself start filling until he had said
the number out loud, because the one time he had tried to just work down the line and stop "when it
seemed right", it had gone exactly the way it did in April.

There was a boy who asked him once why he did not just tell people not to rejoin the line.

Selvam said he had tried that and it had made everybody angry, because a family of eight genuinely does
need three pots. The point was never to stop them coming back. The point was to make sure the second pot
came after everybody else's first one.

---

## 3. The idea in plain English

Selvam is doing a breadth-first traversal, and the head count before each round is the one line that
matters.

- The queue of people is a **queue** in the code — first in, first out.
- One round is one **level** of the tree.
- Counting heads before starting the round is **capturing the level size**, and it is the whole trick.
- People rejoining the back during a round are the **children** you add while draining the current level;
  they belong to the next level, not this one.

### Why a queue, and why that changes everything

```
 depth-first    uses a STACK   -> last in, first out  -> you go deeper
 breadth-first  uses a QUEUE   -> first in, first out -> you go wider
```

**That is the only structural difference.** Take yesterday's iterative preorder, change the stack to a
queue and `pop()` to `popleft()`, and you have a level-order traversal. Nothing else changes.

```python
    queue = deque([root])
    while queue:
        node = queue.popleft()              # popleft, not pop
        visit(node)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
```

Six lines, and it visits every node in level order: `1, 2, 3, 4, 5, 6`. **But it does not tell you where
one level ends.** The output is flat.

### The level boundary, which is the actual lesson

The question is almost always *"return each level as its own list"* — `[[1], [2,3], [4,5,6]]`. And the
answer is Selvam's head count:

```python
    while queue:
        level_size = len(queue)             # <- COUNT FIRST, before draining
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
```

**Why it works, in one sentence: at the top of the outer loop the queue contains exactly one complete
level, so its length is that level's size, and everything appended during the inner loop belongs to the
next level.**

That invariant is worth stating out loud in an interview, because it is the thing being tested. The
`level_size` variable is not an optimisation — **without capturing it, `len(queue)` changes underneath
you as you append**, and the inner loop never ends the way it should.

### The other two ways, and why they are worse

**A sentinel.** Put a `None` in the queue as a level marker; when you pop it, the level is over, and you
push another `None` if the queue is not empty.

Works, and it needs careful handling of the final marker to avoid an infinite loop. More state, more
edge cases.

**A dictionary keyed by depth.** Do a depth-first walk carrying the depth down, and append each value to
`levels[depth]`.

Also works, and it is genuinely useful — it is the shortest way to answer "give me every level" when you
already have a recursive walk. Two things to know: it visits in depth-first order, so within a level the
values still come out left to right (because the left subtree is always recursed first), and it uses
`O(height)` stack instead of `O(width)` queue.

**Know all three; write the `level_size` one.**

### Which problems need breadth-first

The rule: **anything about levels, anything about the shallowest, and anything about shortest paths.**

| Problem | Why BFS |
|---|---|
| Level order traversal | the levels are the answer |
| Right side view | the last node of each level |
| Level averages, level maximums | one level at a time |
| **Minimum depth** | **stops at the first leaf; DFS explores the whole tree** |
| Zigzag / spiral order | levels, alternately reversed |
| Connect each node to its next right | the level *is* the linked list |
| Shortest path in an unweighted graph | the first time you reach a node is the shortest way |

**Minimum depth is the one to remember**, because it is where BFS is not merely tidier but genuinely
faster. A tree whose left branch is 10,000 deep and whose right child is a leaf: depth-first walks the
whole left branch first and then finds the answer is 1. Breadth-first finds it in three steps.

And the counterpart: **use depth-first for anything computed from the children** — height, sums,
diameter, balance — because those are naturally postorder and breadth-first has no convenient way to
combine a node's answer from its children's.

### Depth-first or breadth-first: the memory question

```
 depth-first    O(height) — one frame per level of the current path
 breadth-first  O(width)  — the widest level, held all at once
```

For a **perfect** tree the widest level is the bottom one, holding about `n/2` nodes:

```
 perfect tree, n = 1,000,000
   depth-first    ~20 frames
   breadth-first  ~500,000 nodes in the queue
```

For a **degenerate** tree it reverses completely:

```
 chain, n = 10,000
   depth-first    10,000 frames  ->  RecursionError
   breadth-first  1 node in the queue at any time
```

**Neither is universally cheaper, and which one is safe depends entirely on the shape.** That contrast is
the answer to "what is the space complexity", and giving both halves of it is what makes the answer
sound considered.

### The `deque`, and why not a list

```python
    from collections import deque
    queue = deque([root])
    node = queue.popleft()                  # O(1)
```

```python
    queue = [root]
    node = queue.pop(0)                     # O(n) — every remaining element shifts
```

`list.pop(0)` moves every other element down by one, so a level-order traversal built on a list is
`O(n²)` rather than `O(n)`.

```
 n = 100,000 nodes
   deque:  ~100,000 operations
   list:   ~5,000,000,000 element moves    — minutes instead of milliseconds
```

**`from collections import deque` is the first line of every BFS you write.** It is the same `deque` from
[day 073](../day-073-queues/README.md).

---

## 4. The picture

The queue over time, with the level boundaries marked. This is the diagram to be able to draw.

```
              1
            /   \
           2     3
          / \   /
         4   5 6

 outer   queue at the TOP of the loop     level_size   level produced
 -----   ---------------------------      ----------   --------------
   1     [1]                                   1        [1]
   2     [2, 3]                                2        [2, 3]
   3     [4, 5, 6]                             3        [4, 5, 6]
   4     []                                    -        stop

 result: [[1], [2, 3], [4, 5, 6]]

 the invariant, stated:
   AT THE TOP OF THE OUTER LOOP, THE QUEUE HOLDS EXACTLY ONE COMPLETE LEVEL.
   So len(queue) is that level's size, and everything appended during the
   inner loop belongs to the NEXT level.
```

Selvam's rounds, drawn the same way:

```
 6:00   line: 41 people        count = 41   -> serve exactly 41
        (during those 41, 26 more join the back)
 6:35   line: 26 people        count = 26   -> serve exactly 26
        (during those 26, 9 more join)
 6:52   line: 9               count = 9
 6:58   line: 4               count = 4
 7:01   line: 0               -> done

 the man who rejoins the queue during round 1 is served in round 2.
 that is EXACTLY a node's children being appended during its own level.
```

Why capturing the size is not optional:

```
 WITHOUT capturing:                        WITH capturing:

 while queue:                              while queue:
     for _ in range(len(queue)):               n = len(queue)
         node = queue.popleft()                for _ in range(n):
         queue.append(node.left)                   node = queue.popleft()
         ...                                       queue.append(node.left)

 range(len(queue)) is evaluated ONCE       n is fixed before any appends
 in Python, so this happens to work —      -> correct, and obviously correct
 but the moment it becomes a while
 loop testing len(queue), the level
 never ends because appends keep
 topping it up.
```

Depth-first against breadth-first, on the two extreme shapes:

```
 PERFECT TREE (n = 15)                    DEGENERATE TREE (n = 5)

         1                                     1
       /   \                                    \
      2     3                                    2
     / \   / \                                    \
    4  5  6  7                                     3
   /|  |\ /| |\                                     \
  8 9 10 ...15                                       4
                                                      \
 DFS stack:  4 frames                                  5
 BFS queue:  8 nodes (the bottom level)
                                          DFS stack:  5 frames
 -> DFS wins on memory                    BFS queue:  1 node

                                          -> BFS wins on memory
```

Minimum depth, which is the case where the choice changes the running time:

```
        1
       / \
      2   3        <- 3 is a leaf at depth 1: the ANSWER
     /
    4
   /
  ...  (10,000 more)

 DFS: walks the entire left branch (10,000 nodes) before it ever sees node 3
 BFS: level 0 -> level 1 -> finds a leaf immediately. 3 nodes visited.
```

---

## 5. The code, built step by step

### Step 1 — `deque`, always

```python
    from collections import deque
    queue = deque([root])
```

**Never a list with `pop(0)`.** It turns an `O(n)` traversal into `O(n²)` with no error to tell you.

### Step 2 — guard the empty tree first

```python
    if root is None:
        return []
```

A `deque([None])` will happily give you a `None` to call `.val` on. Handle it before the loop rather than
checking inside it.

### Step 3 — capture the size, and say why

```python
        level_size = len(queue)             # exactly one level, fixed before we append
```

Say the invariant out loud as you write it: *"at this point the queue holds exactly one complete level."*
That sentence is what the question is testing.

### Step 4 — drain exactly that many

```python
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
```

**Check for `None` before appending**, not after popping. Pushing `None`s and filtering later works and
makes every subsequent line have to think about it.

### Step 5 — the variants are all one line each

Once the skeleton is right, the family falls out:

```python
    result.append(level)                    # level order
    result.append(level[-1])                # right side view
    result.append(sum(level) / len(level))  # level averages
    result.append(max(level))               # level maximums
    result.append(level if depth % 2 == 0 else level[::-1])     # zigzag
```

**That is why the skeleton is worth memorising rather than the problems.** Five interview questions, one
loop, one differing line.

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


def level_order_flat(root: TreeNode | None) -> list[int]:
    """Breadth-first, but the output is flat — no level boundaries.

    This is yesterday's iterative preorder with a QUEUE instead of a STACK.
    That single swap is the entire difference between the two families.
    """
    if root is None:
        return []
    out: list[int] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()              # popleft, not pop
        out.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return out


def level_order(root: TreeNode | None) -> list[list[int]]:
    """LeetCode 102. Each level as its own list.

    THE LINE THAT MATTERS: level_size = len(queue), captured BEFORE draining.

    Invariant: at the top of the outer loop the queue holds exactly one
    complete level. So its length is that level's size, and everything
    appended during the inner loop belongs to the NEXT level.
    """
    if root is None:
        return []
    result: list[list[int]] = []
    queue = deque([root])

    while queue:
        level_size = len(queue)             # <- count the heads first
        level: list[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result


def right_side_view(root: TreeNode | None) -> list[int]:
    """LeetCode 199. What you see standing to the right of the tree:
    the LAST node of each level. One line different from level_order."""
    if root is None:
        return []
    view: list[int] = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:         # the last one in this level
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return view


def level_averages(root: TreeNode | None) -> list[float]:
    """LeetCode 637. Same skeleton, one differing line."""
    if root is None:
        return []
    out: list[float] = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        total = 0
        for _ in range(level_size):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(total / level_size)
    return out


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    """LeetCode 103. Left to right, then right to left, alternating.

    Reverse the LIST, not the traversal. Trying to alternate the queue
    order itself is a classic way to lose an afternoon.
    """
    if root is None:
        return []
    result: list[list[int]] = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        level: list[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right

    return result


def min_depth(root: TreeNode | None) -> int:
    """LeetCode 111. THE case where BFS is genuinely faster than DFS.

    BFS stops at the first leaf it meets. DFS would walk an entire deep
    branch before discovering the answer was 1.

    Note "leaf" means BOTH children are None — a node with one child is not
    a leaf, and `1 + min(left, right)` gets that wrong.
    """
    if root is None:
        return 0
    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                    # first leaf found: shallowest
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0


def max_width(root: TreeNode | None) -> int:
    """The widest level — which is also the peak size of the BFS queue,
    so this function measures its own space complexity."""
    if root is None:
        return 0
    widest = 0
    queue = deque([root])
    while queue:
        level_size = len(queue)
        widest = max(widest, level_size)
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return widest


def levels_by_dfs(root: TreeNode | None) -> list[list[int]]:
    """The third way: depth-first, carrying the depth DOWN as an argument.

    Same answer, and left-to-right within each level comes free because the
    left subtree is always recursed first. Uses O(height) stack instead of
    O(width) queue — which is the better choice on a WIDE tree and the
    worse one on a DEEP tree.
    """
    result: list[list[int]] = []

    def walk(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth == len(result):
            result.append([])               # first node seen at this depth
        result[depth].append(node.val)
        walk(node.left, depth + 1)
        walk(node.right, depth + 1)

    walk(root, 0)
    return result


def connect_next_right(root: TreeNode | None) -> TreeNode | None:
    """LeetCode 116/117: link every node to the next one on its level.

    The level IS the linked list, so this is level order with one extra
    line — join consecutive nodes as you drain each level.
    """
    if root is None:
        return None
    queue = deque([root])
    while queue:
        level_size = len(queue)
        previous: TreeNode | None = None
        for _ in range(level_size):
            node = queue.popleft()
            if previous is not None:
                previous.next = node        # type: ignore[attr-defined]
            previous = node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        previous.next = None                # type: ignore[attr-defined]
    return root


def level_order_slow(root: TreeNode | None) -> list[int]:
    """The trap, written out so you can time it: a list with pop(0).

    Every pop(0) shifts every remaining element down by one, so this is
    O(n^2). On 100,000 nodes that is ~5 billion element moves.
    """
    if root is None:
        return []
    out: list[int] = []
    queue = [root]
    while queue:
        node = queue.pop(0)                 # O(n), not O(1)
        out.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
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

    print(level_order_flat(root))       # [1, 2, 3, 4, 5, 6]
    print(level_order(root))            # [[1], [2, 3], [4, 5, 6]]
    print(right_side_view(root))        # [1, 3, 6]
    print(level_averages(root))         # [1.0, 2.5, 5.0]
    print(zigzag_level_order(root))     # [[1], [3, 2], [4, 5, 6]]
    print(max_width(root))              # 3
    print(levels_by_dfs(root) == level_order(root))     # True

    # minimum depth: the case where BFS is genuinely faster
    lopsided = TreeNode(1, TreeNode(2, TreeNode(4, TreeNode(8))), TreeNode(3))
    print(min_depth(lopsided))          # 2   <- via node 3, found immediately
    print(level_order(lopsided))        # [[1], [2, 3], [4], [8]]

    print(level_order(None), min_depth(None))          # [] 0
    print(level_order(TreeNode(7)))                    # [[7]]

    # the two shapes, and what each traversal costs
    chain = from_list([1, 2, None, 3, None, 4])
    print(max_width(chain))             # 1  <- BFS queue never exceeds one node
```

---

## 6. What it costs

### Time

```
 every node is enqueued exactly once and dequeued exactly once
 -> O(n)
```

**Identical to depth-first.** Neither family is faster in the general case; they differ in *which node
they reach first*, which is why minimum depth is faster with BFS and height is more natural with DFS.

### Space — the number that actually differs

```
 breadth-first:  O(width)   — the widest level, held in the queue at once
 depth-first:    O(height)  — one frame per level of the current path
```

For the two extreme shapes:

```
 PERFECT tree, n = 1,000,000
   width of the bottom level    ~500,000 nodes
   height                       ~20
   -> BFS holds 500,000 references (~4 MB of pointers)
   -> DFS holds 20 frames

 DEGENERATE tree (a chain), n = 10,000
   width                        1
   height                       10,000
   -> BFS holds 1 node
   -> DFS: RecursionError: maximum recursion depth exceeded
```

**A factor of twenty-five thousand, in opposite directions.** The honest answer to "which is more
memory-efficient" is *"it depends on the shape, and here are the two extremes"*.

For a random or roughly balanced tree, the widest level is still around `n/2`, so **BFS is usually the
more memory-hungry of the two** — and it is the one that is *safe* from stack overflow.

### The `deque` versus `list` difference, measured

```
 deque.popleft()   O(1)
 list.pop(0)       O(n)   — every remaining element shifts down one slot

 n = 1,000       deque ~1,000 ops       list ~500,000 element moves
 n = 100,000     deque ~100,000         list ~5,000,000,000
                                         -> minutes, not milliseconds
```

**This is a silent `O(n²)`.** The code is correct and the tests on a ten-node tree pass instantly.

### Minimum depth: where the choice changes the complexity

```
 tree with a leaf at depth 1 and a left branch 10,000 deep

 BFS:  visits 3 nodes                      O(1) in practice
 DFS:  visits all 10,002 nodes             O(n)
```

More generally, for the shallowest leaf at depth `d` in a tree with branching factor `b`:

```
 BFS visits O(b^d) nodes — everything above the answer, and no more
 DFS visits O(n) — potentially the whole tree
```

**When the answer is shallow and the tree is deep, BFS is not tidier, it is faster.**

### Queue memory, concretely

```
 a deque entry is one pointer          8 bytes
 plus deque block overhead             ~10-20% 
 500,000 entries                       ~4-5 MB
```

Small in absolute terms — the point is not that BFS runs out of memory on a million-node tree, it is that
**the growth is in `width`, so it is unbounded in a way `O(height)` is not** for shapes like a
wide-and-shallow tree.

---

## 7. The traps

### Trap 1 — a list instead of a deque

```python
    queue = [root]
    node = queue.pop(0)
```

Correct output, `O(n²)` running time, no error. On a hundred thousand nodes it is the difference between
milliseconds and minutes. **`from collections import deque` first, every time.**

### Trap 2 — not capturing the level size

```python
        while queue:
            level = []
            while queue:                    # WRONG: appends keep topping it up
                node = queue.popleft()
                level.append(node.val)
                queue.append(node.left)
                ...
```

The inner loop drains the queue *and everything added to it*, so the first "level" is the entire tree and
the result is `[[1, 2, 3, 4, 5, 6]]`. One level, all the nodes. **Selvam's April.**

### Trap 3 — appending `None` children

```python
            queue.append(node.left)         # might be None
            queue.append(node.right)
```

```
 AttributeError: 'NoneType' object has no attribute 'val'
```

on the next `popleft`. Check before appending. And note that a `None` in the queue also corrupts
`len(queue)`, so the level sizes are wrong even if you filter later.

### Trap 4 — forgetting the empty-tree guard

```python
    queue = deque([root])                   # root is None
```

Same `AttributeError`, on the very first iteration. `if root is None: return []` before the loop.

### Trap 5 — `min` for minimum depth

```python
    def min_depth(node):
        if node is None:
            return 0
        return 1 + min(min_depth(node.left), min_depth(node.right))
```

```
 min_depth(TreeNode(1, None, TreeNode(2)))  ->  1        correct answer: 2
```

A node with one child is **not a leaf**, but `min` treats the missing child as a depth-0 branch and
returns 1. This is the most-failed easy tree problem, and BFS avoids it entirely by checking "both
children are `None`" explicitly.

### Trap 6 — trying to zigzag by reversing the traversal

```python
        if not left_to_right:
            queue.appendleft(node.right)    # trying to alternate the queue itself
```

It can be made to work with two stacks, and doing it by manipulating one queue is a reliable way to lose
twenty minutes. **Collect the level normally and reverse the list.** `level[::-1]` is `O(width)` and
costs nothing that matters.

### Trap 7 — assuming BFS gives you a parent's answer from its children

```python
        # trying to compute height with BFS
```

You can count levels, and that gives the height — but anything that *combines* children's results (sums,
diameter, balance) has no natural place to do the combining in a level-order loop, because a parent is
long gone by the time its children are processed. **Those are depth-first, postorder, problems.**

### Trap 8 — quoting `O(n)` space for BFS without saying why

`O(n)` is technically true — the queue never exceeds `n` — but it hides the real answer. **The space is
`O(width)`**, which is `n/2` for a perfect tree and `1` for a chain. Saying `O(width)` and then giving
both extremes is the answer that sounds like you have thought about it.

---

## 8. In the interview

### How it gets asked

- The pair: *"Print the tree level by level. Now print each level as its own list."* LeetCode 102.
- The variants, which are the same loop: right side view (199), level averages (637), zigzag (103),
  connect next pointers (116/117).
- The one where it matters: *"Find the minimum depth."* LeetCode 111.
- The comparison: *"When would you use BFS instead of DFS?"*
- The space probe: *"What is the space complexity, and how does it compare to DFS?"*

### What to say out loud, in the first ninety seconds

1. **Name the one structural difference.** "Breadth-first is the same walk as iterative preorder with a
   queue instead of a stack. That single swap is what makes it go wide instead of deep."
2. **State the invariant before writing the loop.** "At the top of each outer iteration, the queue holds
   exactly one complete level. So I capture its length first — that number is the level size — and
   everything I append while draining belongs to the next level."
3. **Use a `deque`, and say why.** "A `deque`, not a list — `list.pop(0)` shifts every element and turns
   this into `O(n²)` with no error to tell you."
4. **Give the space as `O(width)`, with both extremes.** "`O(n)` time, and `O(width)` space — about half
   the nodes for a perfect tree, and one node for a chain. Depth-first is the opposite: `O(height)`, so
   twenty frames on a balanced million-node tree and a million on a chain."
5. **Say when BFS is the right tool.** "Levels, the shallowest anything, and shortest paths. Minimum
   depth is the case where it is genuinely faster, not just tidier."
6. **Say when it is not.** "Anything computed from the children — height, sums, diameter, balance — is
   depth-first postorder, because BFS has nowhere natural to combine a parent's answer from its
   children's."

### The follow-ups

**"Now group them by level."**
"One line: capture `len(queue)` into a variable at the top of the outer loop, before draining anything.
The reason it works is the invariant — at that moment the queue contains exactly one complete level, so
its length *is* the level size, and every child appended during the inner loop belongs to the next level.
Without the capture, the inner loop keeps draining a queue that is being topped up, so the first 'level'
is the whole tree. There are two other ways: a `None` sentinel pushed as a level marker, which works and
needs care to avoid an infinite loop at the end; and a depth-first walk carrying the depth down and
appending into `levels[depth]`, which is genuinely neat and uses `O(height)` stack instead of `O(width)`
queue. I would write the `level_size` version because it is the shortest and the invariant is easy to
state."

**"What is the space complexity, and how does it compare to DFS?"**
"BFS is `O(width)` — the widest level, held in the queue at once. DFS is `O(height)`. Those are opposite
and neither wins in general. On a **perfect** million-node tree, the bottom level holds about five
hundred thousand nodes, so BFS holds half a million references while DFS holds about twenty frames. On a
**chain** of ten thousand nodes it reverses completely: BFS holds one node and DFS overflows the stack —
Python's default limit is a thousand. So the practical rule is that BFS is usually the heavier of the two
on memory and the safer of the two against stack overflow. I would say `O(width)` rather than `O(n)`,
because `O(n)` is true and hides all of that."

**"When would you use BFS instead of DFS?"**
"Three families. Anything where **the levels are the answer** — level order, right side view, level
averages, zigzag, connecting each node to its next right neighbour. Anything asking for **the shallowest**
something, where BFS stops the moment it finds it. And **shortest paths in an unweighted graph**, where
the first time you reach a node is guaranteed to be by the shortest route — that is the same algorithm on
a different structure. Minimum depth is the clearest example of the second family: if the left branch is
ten thousand deep and the right child is a leaf, DFS walks the entire left branch before discovering the
answer is 2, and BFS finds it in three nodes. Conversely, I would use DFS for anything computed from the
children — height, subtree sums, diameter, balance — because those are postorder and BFS has no natural
place to do the combining."

**"Find the minimum depth."**
"BFS, and I would say why rather than just doing it. Walk level by level carrying the depth, and return
as soon as I meet a node with **both** children `None`. That is the first leaf in level order, which is
the shallowest leaf by definition, and I stop there rather than exploring the rest. The recursive version
has a trap that catches almost everybody: `1 + min(left, right)` is wrong, because a node with exactly one
child is **not a leaf**, and `min` treats the missing side as a zero-depth branch. On a root with only a
right child it returns 1 instead of 2. You have to special-case the one-child node, and BFS avoids the
whole thing because 'both children are None' is an explicit test."

**"Do it with `O(1)` extra space."**
"Not possible with a queue — the queue is the algorithm. There is one special case: if the nodes have a
`next` pointer, as in the 'connect each node to its next right node' problem, then once one level is
linked you can walk it as a linked list and build the next level's links, which gives level-by-level
processing in `O(1)` extra space. That is a genuinely clever trick and it only works because the tree has
been augmented. For a plain binary tree, level order needs the queue."

**"How would you do zigzag order?"**
"Same skeleton, and I would **reverse the list, not the traversal**. Collect each level left to right as
usual, and append it reversed on alternate levels. Trying to alternate the queue's direction is possible
with two stacks and is a reliable way to spend twenty minutes on something that is one `[::-1]`. The
reversal is `O(width)` per level, so the total is still `O(n)`."

### A model answer

Asked: *print the tree level by level — and then print each level as its own list.*

> "Level order is breadth-first, and the useful way to see it is that it is **the iterative preorder from
> yesterday with a queue instead of a stack**. A stack is last-in-first-out so you go deeper; a queue is
> first-in-first-out so you go wider. That one swap is the entire difference between the two families.
>
> The flat version is six lines: put the root in a queue, and while the queue is not empty, take from the
> front, record it, and push its children on the back.
>
> The grouped version is what the question is really about, and it comes down to one line. **At the top of
> each outer iteration, the queue holds exactly one complete level.** So I capture its length into a
> variable *before* draining anything — that number is the size of this level — and then I take exactly
> that many nodes. Everything I append while doing so is a child, so it belongs to the *next* level, and
> it is safely sitting behind the ones I am still to process.
>
> That capture is not an optimisation; it is the correctness. Without it, the inner loop drains a queue
> that is being topped up as it goes, and the first 'level' turns out to be the entire tree.
>
> Two implementation details I would say aloud. I use a `deque`, because `list.pop(0)` shifts every
> remaining element and quietly turns this into `O(n²)` — on a hundred thousand nodes that is billions of
> element moves and no error to tell you. And I check each child for `None` **before** appending, rather
> than filtering after popping, because a `None` in the queue also corrupts the level sizes.
>
> Complexity: `O(n)` time, since every node is enqueued and dequeued exactly once — the same as
> depth-first. Space is **`O(width)`**, which I would give rather than `O(n)` because the contrast is the
> interesting part. On a perfect million-node tree, the bottom level holds about five hundred thousand
> nodes, so BFS holds half a million while a depth-first walk holds about twenty stack frames. On a chain
> it reverses entirely: BFS holds one node and DFS overflows the stack. Neither is universally cheaper.
>
> Once this skeleton is right, a family of interview questions is one differing line each: append the
> last element of each level for the right side view, the average for level averages, the level reversed
> on alternate rows for zigzag. And the one where the choice genuinely matters is minimum depth — BFS
> returns at the first leaf it meets, where a depth-first walk might explore a ten-thousand-node branch
> before discovering the answer was 2."

---

## 9. Recall card

- **Breadth-first is iterative preorder with a QUEUE instead of a STACK.** That one swap is the whole
  difference: last-in-first-out goes deep, first-in-first-out goes wide. Use `collections.deque` —
  **`list.pop(0)` is `O(n)` and silently makes the traversal `O(n²)`** (~5 billion moves at n = 100,000).
- **The one line that matters: `level_size = len(queue)`, captured BEFORE draining.** The invariant:
  *at the top of the outer loop the queue holds exactly one complete level*, so its length is that
  level's size and everything appended inside belongs to the next. Without it, the first "level" is the
  entire tree.
- **`O(n)` time — same as DFS. Space is `O(width)`, not `O(n)`** — ~**500,000** nodes for a perfect
  million-node tree against ~**20** DFS frames, and **1** node for a chain where DFS raises
  `RecursionError`. Opposite directions; neither wins in general.
- **Use BFS for: levels are the answer** (level order, right side view, averages, zigzag, next-right
  pointers), **the shallowest anything**, and **shortest paths in an unweighted graph**. **Minimum depth
  is where it is genuinely faster** — 3 nodes against 10,002. **Use DFS for anything computed from the
  children** (height, sums, diameter, balance): BFS has nowhere to combine them.
- **Check children for `None` before appending** (a `None` in the queue corrupts the level sizes too),
  guard the empty tree before the loop, and **zigzag by reversing the LIST, not the traversal**. And the
  recursive `min_depth` trap: **`1 + min(left, right)` is wrong** — a node with one child is not a leaf,
  and it returns 1 instead of 2.
