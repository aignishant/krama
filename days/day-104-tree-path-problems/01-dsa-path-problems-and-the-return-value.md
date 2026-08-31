---
day: 104
track: dsa
title: "Path problems, and the return-value trick"
phase: "Trees and binary search trees"
status: written
---

# Day 104 · DSA — Path problems, and the return-value trick

**After today you can:** You can return one thing to the parent while tracking another in an outer variable.

**The interviewer asks it as:** *Find the maximum path sum in the binary tree.*

---

## 1. What this is, and why they ask it

A **path** in a tree is a sequence of nodes where each one is connected to the next. Path problems ask
you to find one — the longest, the heaviest, the one that adds to a target — and they are the hardest
family in the topic because **the answer you want and the answer your parent needs are different
things**.

Three sentences. You met the shape on [day 102](../day-102-height-and-diameter/README.md) with diameter:
return the height, record the bend. Today it does real work, because the values can be **negative**, and
that introduces a decision at every node — *is this branch worth taking at all?* And there are two
different definitions of "path" in circulation, so the first thing to do is establish which one is meant.

They ask maximum path sum because it is one of the hardest problems that still fits in fifteen minutes,
and it fails in three distinct ways: returning the bent path to the parent, forgetting that a negative
branch should be dropped, and forgetting that the answer itself can be negative. Get those three right
and the code is nine lines. Get any of them wrong and it is confidently, silently wrong on exactly the
inputs the tests use.

---

## 2. The story

Devaraj collected for the temple fund and his territory was the seven villages off the Kalyanpur road.

It was not a straight road. It forked twice, and the branches forked again, so what he was really working
was a set of lanes spreading out from the junction near the water tank.

Every village was worth something to him, and the figure he had in his book was not the donation — it was
the donation **minus** what it cost him to get there and back. The two big villages were plus four
hundred and plus three hundred. But the one at the top of the north lane was minus sixty, because it was
eleven kilometres of bad road for a family that gave twenty rupees, and the little settlement past the
quarry was minus a hundred and ten.

He could not do all of them in a day. What he did was pick a single run — go up one lane, come back down
through a junction, and out along another — and he wanted the best run he could get.

The way he worked it out was the thing his nephew found strange.

He would stand at a junction and ask, for each lane going out of it, one question only: **is there
anything worth having down there, and how much?** Not "what is down there" — how much, as a single
number, and never less than zero. If the best he could do down the north lane was minus sixty, he wrote
zero, because he was not obliged to go down it at all. Zero was always available.

Then, standing at that junction, the best run **through** it was the north lane's number plus the south
lane's number plus whatever the junction village itself was worth.

But — and this is the part his nephew kept getting wrong — when he then walked back to the *previous*
junction and it asked him "how much is down your lane?", he could not give that number. Because a run
that goes up the north lane and down the south lane has already used the junction in the middle. He
cannot then also carry on backwards out of it. From the previous junction's point of view, all he can
offer is **one** arm: the junction village plus the better of its two lanes.

So there were two numbers at every junction. The best run that turned around there — which he wrote down
in his book and never used again except to compare. And the best single arm going down — which was the
only thing he could report upwards.

His nephew, who did this for a season, kept reporting the first number, and kept coming home with routes
that doubled back on themselves and could not actually be walked.

---

## 3. The idea in plain English

Devaraj has solved maximum path sum, and both of the things his nephew got wrong are the traps.

- Each village is a node; its value is the node's value, and it can be **negative**.
- "Is there anything worth having down there, and never less than zero" is **`max(0, arm)`** — the floor.
- The best run **turning around** at a junction is `left + right + node.val`, and it is **recorded**.
- The best **single arm** to offer upwards is `node.val + max(left, right)`, and it is **returned**.
- Reporting the turning-around number upwards is the nephew's mistake, and it produces paths that cannot
  exist.

### First: which definition of "path"?

Two are in use and they need different code.

```
 ROOT-TO-LEAF PATH       starts at the root, ends at a leaf, always goes down
                         LeetCode 112, 113, 257

 ANY-TO-ANY PATH         starts anywhere, ends anywhere, may bend at one node
                         LeetCode 124, 543, 687
```

**Ask which one, or state your assumption.** They are different problems: root-to-leaf is a preorder walk
carrying state down, and any-to-any is the postorder return-value trick.

There is a third variant that catches people: **downward but not necessarily root-to-leaf** — LeetCode
437, path sum III, where a path can start and end anywhere as long as it goes downwards. That one has a
completely different best solution, and it is at the end of this lesson.

### Root-to-leaf: information goes down

```python
    def walk(node, remaining):
        if node is None:
            return False
        remaining -= node.val
        if node.left is None and node.right is None:     # a LEAF
            return remaining == 0
        return walk(node.left, remaining) or walk(node.right, remaining)
```

**The state is carried down as an argument**, so there is nothing to undo — the
[day 094](../day-094-backtracking/README.md) rule. And the leaf test is `both children are None`, never
`node is None`, which is trap 1.

For "collect all such paths" you also carry the path itself, and that *does* need choose-recurse-un-choose
plus the copy:

```python
        trail.append(node.val)              # choose
        ...
        trail.pop()                         # un-choose
```

### Any-to-any: the return-value trick, doing real work

Every path has exactly one **highest node** — the point where it turns around. So evaluate every node as
that turning point, and you have considered every path exactly once. Same observation as
[day 102](../day-102-height-and-diameter/README.md).

At a node, two different quantities exist and **they must not be confused**:

```
 RECORD (the answer):   left_arm + right_arm + node.val
                        the best path that TURNS AROUND here

 RETURN (to the parent): node.val + max(left_arm, right_arm)
                        the best SINGLE ARM going down from here
```

**The parent cannot use the recorded value**, because a path that turns around at me has already used
both of my children — it cannot also continue upward through me. That is the sentence to say.

### The floor at zero, which is what negatives add

```python
        left = max(0, arm(node.left))
        right = max(0, arm(node.right))
```

**`max(0, ...)` means "I am not obliged to take this branch".** If the best the left subtree can offer is
negative, taking nothing is better, and taking nothing contributes zero.

Without the floor:

```
 tree:   -10
        /    \
      9      20
            /   \
          15     7

 with max(0, ...):     15 + 7 + 20 = 42        correct
 without:              the -10 root drags everything through it, and the
                       answer comes out wrong on any tree with negatives
```

This is exactly Kadane's algorithm from the array world — *drop the prefix when it turns negative* —
applied to two branches instead of one.

### And the trap the floor creates

```python
    best = 0                                # WRONG
```

If every node is negative, the answer is negative — a single node, the least bad one. Initialising `best`
to `0` returns 0 for `[-3]`, which is not a path.

```python
    best = float("-inf")                    # correct
```

**The floor applies to the arms, never to the answer.** A path must contain at least one node, so the
answer is at worst the largest single value. Saying that distinction out loud is what separates people who
understand the floor from people who copied it.

### The family, one table

| Problem | Return to parent | Record on the side | Floor? |
|---|---|---|---|
| Diameter (543) | height | `left + right + 2` | no |
| Max path sum (124) | `val + max(left, right)` | `left + right + val` | **yes**, `max(0, arm)` |
| Longest univalue path (687) | longest matching arm | `left + right` | no |
| Max sum root-to-leaf | — | carried down | no |
| Largest BST subtree (333) | `(min, max, size, ok)` | `size` when `ok` | no |

**One shape, five problems.** If you can fill this table in, you have the technique.

### Path sum III: the one that is not this shape at all

*"Count the paths summing to a target, where a path goes downwards but need not start at the root."*

The obvious solution runs the root-to-leaf walk starting from every node: `O(n²)`, or `O(n log n)` on a
balanced tree.

The good solution is **prefix sums with a hash map**, exactly as on
[day 038](../day-038-subarray-sum-k/README.md), applied to the current root-to-node path:

```python
        running += node.val
        count += seen[running - target]     # how many earlier prefixes make a valid path
        seen[running] += 1                  # choose
        ...recurse...
        seen[running] -= 1                  # UN-CHOOSE — this is essential
```

**The `seen[running] -= 1` on the way out is the whole trick.** The map must contain only the prefixes on
the *current* root-to-node path — a prefix from a sibling branch is not reachable from here. It is
[day 094's](../day-094-backtracking/README.md) un-choose, applied to a dictionary instead of a list, and
forgetting it counts paths that bend, which is not what was asked.

That takes it from `O(n²)` to `O(n)`, and it is the strongest single thing you can show in this family.

---

## 4. The picture

Devaraj's junction, and the two numbers.

```
                        junction (value 20)
                       /                    \
            north lane                       south lane
            best arm: -60                    best arm: 15
            -> max(0, -60) = 0               -> max(0, 15) = 15

    RECORD (turns around here):  0 + 15 + 20  =  35
    RETURN (one arm, upwards):   20 + max(0, 15)  =  35
                                 (they coincide here only because one arm is 0)

 with both arms positive:
                        junction (value 20)
                       /                    \
              best arm: 15                   best arm: 7

    RECORD:  15 + 7 + 20  =  42     <- the answer candidate
    RETURN:  20 + max(15, 7)  =  35 <- what the parent may use

    the parent CANNOT have 42: a path bending here has spent BOTH children.
```

The classic tree, traced:

```
        -10
       /    \
      9      20
            /   \
          15     7

 arm(9):   left=max(0,-inf...)=0, right=0
           RECORD 0 + 0 + 9 = 9        best = 9
           RETURN 9 + max(0,0) = 9

 arm(15):  RECORD 15, RETURN 15        best = 15
 arm(7):   RECORD 7,  RETURN 7         best = 15

 arm(20):  left = max(0, 15) = 15
           right = max(0, 7) = 7
           RECORD 15 + 7 + 20 = 42     best = 42     <- the answer
           RETURN 20 + max(15, 7) = 35

 arm(-10): left = max(0, 9) = 9
           right = max(0, 35) = 35
           RECORD 9 + 35 + (-10) = 34  best stays 42
           RETURN -10 + 35 = 25

 answer: 42   (the path 15 -> 20 -> 7, which never touches the root)
```

What the floor does, drawn:

```
        5
       / \
    -100  3

 WITHOUT the floor:                WITH the floor:
   left arm  = -100                  left arm  = max(0, -100) = 0
   right arm =    3                  right arm = max(0, 3)    = 3
   RECORD -100 + 3 + 5 = -92         RECORD 0 + 3 + 5 = 8
   RETURN 5 + max(-100, 3) = 8       RETURN 5 + max(0, 3) = 8

 the recorded value is wrong without the floor: the real best path
 through 5 is [5, 3] = 8, not [-100, 5, 3] = -92.
 Nothing forces you to walk down a lane that loses money.
```

The two definitions of "path", side by side:

```
 ROOT-TO-LEAF (112, 113, 257)          ANY-TO-ANY (124, 543, 687)

        1                                     1
       / \                                   / \
      2   3      valid: 1-2, 1-3            2   3   valid: 2-1-3, 2, 1-2, 3, ...
                 invalid: 2-1-3                     invalid: nothing that
                          (does not start                    revisits a node
                           at the root)

 state goes DOWN as an argument         state comes UP as a return value
 preorder                               postorder
 no undo needed (values are passed)     the RECORD/RETURN split
```

Path sum III's map, and why the un-choose matters:

```
        10
       /  \
      5    -3
     / \      \
    3   2      11

 walking down 10 -> 5 -> 3, `seen` holds the prefixes {0:1, 10:1, 15:1}
 walking back up to 5 and down to 2, `seen` must NO LONGER contain 18
 (the prefix from the 3 branch) — 3 is not on the path to 2.

 without seen[running] -= 1 on the way out:
   the map accumulates prefixes from sibling branches
   -> counts "paths" that bend, which are not downward paths
   -> an over-count with no error
```

---

## 5. The code, built step by step

### Step 1 — establish which "path" is meant

"Is the path root-to-leaf, or can it start and end anywhere? And can it bend at a node, or must it go
strictly downwards?" **Three different problems, and asking costs ten seconds.**

### Step 2 — for root-to-leaf, carry the state down

```python
        remaining -= node.val
        if node.left is None and node.right is None:
            return remaining == 0
```

**A leaf is a node whose two children are both `None`.** Not `node is None` — that is trap 1 and it makes
a one-sided node look like a leaf.

### Step 3 — for any-to-any, write the two lines and label them

```python
        best = max(best, left + right + node.val)       # RECORD
        return node.val + max(left, right)              # RETURN
```

Write them adjacent, with those two words in your head. **The recorded line is the answer; the returned
line is what the parent can use.** Say the reason: a path bending here has already spent both children.

### Step 4 — the floor on the arms

```python
        left = max(0, arm(node.left))
        right = max(0, arm(node.right))
```

Say what it means: *"I am not obliged to take a branch. If the best it offers is negative, I take nothing,
which contributes zero."*

### Step 5 — initialise the answer to negative infinity, not zero

```python
        best = float("-inf")
```

Because the answer itself can be negative — a tree of all-negative values has a best path of one node.
**The floor applies to the arms, not to the answer.**

### The complete solution

```python
from collections import defaultdict, deque


class TreeNode:
    def __init__(self, val: int = 0,
                 left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# ROOT-TO-LEAF: state travels DOWN as an argument. Preorder. No undo needed.
# ---------------------------------------------------------------------------

def has_path_sum(root: TreeNode | None, target: int) -> bool:
    """LeetCode 112. Does any root-to-leaf path add to `target`?

    A LEAF is a node with BOTH children None. Using `node is None` as the
    base case makes a one-sided node look like a leaf and gives wrong
    answers on trees with single children.
    """
    if root is None:
        return False
    remaining = target - root.val
    if root.left is None and root.right is None:
        return remaining == 0
    return (has_path_sum(root.left, remaining)
            or has_path_sum(root.right, remaining))


def all_path_sums(root: TreeNode | None, target: int) -> list[list[int]]:
    """LeetCode 113. Every root-to-leaf path adding to `target`.

    Now the path itself is state, so this IS choose-recurse-un-choose, and
    the recorded path must be a COPY.
    """
    result: list[list[int]] = []
    trail: list[int] = []

    def walk(node: TreeNode | None, remaining: int) -> None:
        if node is None:
            return
        trail.append(node.val)                          # choose
        remaining -= node.val
        if node.left is None and node.right is None and remaining == 0:
            result.append(trail[:])                     # COPY
        else:
            walk(node.left, remaining)
            walk(node.right, remaining)
        trail.pop()                                     # un-choose

    walk(root, target)
    return result


def binary_tree_paths(root: TreeNode | None) -> list[str]:
    """LeetCode 257. Every root-to-leaf path, as strings.

    Note this version passes the path as a STRING argument, so there is
    nothing to undo — the day-094 rule that values passed as arguments
    cannot need restoring.
    """
    paths: list[str] = []

    def walk(node: TreeNode | None, so_far: str) -> None:
        if node is None:
            return
        so_far = f"{so_far}->{node.val}" if so_far else str(node.val)
        if node.left is None and node.right is None:
            paths.append(so_far)
            return
        walk(node.left, so_far)
        walk(node.right, so_far)

    walk(root, "")
    return paths


# ---------------------------------------------------------------------------
# ANY-TO-ANY: the RECORD / RETURN split. Postorder.
# ---------------------------------------------------------------------------

def max_path_sum(root: TreeNode | None) -> int:
    """LeetCode 124. The hardest of the family, in nine lines.

    THREE things must be right, and each fails silently:

    1. RECORD `left + right + val`, RETURN `val + max(left, right)`.
       The parent cannot use the recorded value — a path bending here has
       already spent both children, so it cannot continue upward.

    2. FLOOR each arm at 0: max(0, arm). You are never obliged to take a
       branch, so a negative arm contributes nothing. This is Kadane's
       "drop the prefix when it goes negative", on two branches.

    3. Initialise `best` to -inf, NOT 0. The floor applies to the ARMS, not
       to the ANSWER — an all-negative tree has a best path of one node.

    Time O(n). Space O(height).
    """
    best = float("-inf")

    def arm(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(0, arm(node.left))       # never obliged to take a branch
        right = max(0, arm(node.right))
        best = max(best, left + right + node.val)       # RECORD: bends here
        return node.val + max(left, right)              # RETURN: one arm

    arm(root)
    return int(best)


def max_path_sum_with_path(root: TreeNode | None) -> tuple[int, list[int]]:
    """The follow-up: return the path, not just the sum.

    Same shape, bigger return value. Costs O(n) space instead of O(height),
    because every frame now holds a list.
    """
    best = float("-inf")
    best_path: list[int] = []

    def arm(node: TreeNode | None) -> tuple[int, list[int]]:
        nonlocal best, best_path
        if node is None:
            return 0, []
        ls, lp = arm(node.left)
        rs, rp = arm(node.right)
        if ls < 0:
            ls, lp = 0, []
        if rs < 0:
            rs, rp = 0, []
        if ls + rs + node.val > best:
            best = ls + rs + node.val
            best_path = lp + [node.val] + rp[::-1]
        if ls >= rs:
            return node.val + ls, [node.val] + lp
        return node.val + rs, [node.val] + rp

    arm(root)
    return int(best), best_path


def max_root_to_leaf(root: TreeNode | None) -> int:
    """For contrast: root-to-leaf only. NO floor, because you MUST reach a
    leaf — you cannot decline a branch when there is only one."""
    if root is None:
        return 0
    if root.left is None:
        return root.val + max_root_to_leaf(root.right)
    if root.right is None:
        return root.val + max_root_to_leaf(root.left)
    return root.val + max(max_root_to_leaf(root.left),
                          max_root_to_leaf(root.right))


# ---------------------------------------------------------------------------
# DOWNWARD, ANYWHERE TO ANYWHERE: prefix sums on a tree.
# ---------------------------------------------------------------------------

def path_sum_iii_naive(root: TreeNode | None, target: int) -> int:
    """LeetCode 437, the obvious way: start a downward walk at every node.
    O(n^2) worst case, O(n log n) on a balanced tree."""
    def down_from(node: TreeNode | None, remaining: int) -> int:
        if node is None:
            return 0
        remaining -= node.val
        return ((1 if remaining == 0 else 0)
                + down_from(node.left, remaining)
                + down_from(node.right, remaining))

    if root is None:
        return 0
    return (down_from(root, target)
            + path_sum_iii_naive(root.left, target)
            + path_sum_iii_naive(root.right, target))


def path_sum_iii(root: TreeNode | None, target: int) -> int:
    """LeetCode 437 in O(n), with prefix sums and a hash map.

    Exactly day 038's subarray-sum-equals-k, applied to the current
    root-to-node path.

    THE CRITICAL LINE is `seen[running] -= 1` on the way out. The map must
    hold ONLY the prefixes on the current path — a prefix from a sibling
    branch is not reachable from here. Without it you count "paths" that
    bend, which the question did not ask for, and there is no error.
    """
    seen: dict[int, int] = defaultdict(int)
    seen[0] = 1                             # the empty prefix
    count = 0

    def walk(node: TreeNode | None, running: int) -> None:
        nonlocal count
        if node is None:
            return
        running += node.val
        count += seen[running - target]     # earlier prefixes that complete a path
        seen[running] += 1                  # choose
        walk(node.left, running)
        walk(node.right, running)
        seen[running] -= 1                  # UN-CHOOSE — the whole trick

    walk(root, 0)
    return count


def sum_root_to_leaf_numbers(root: TreeNode | None) -> int:
    """LeetCode 129. Each root-to-leaf path spells a number; sum them.
    State carried down, so nothing to undo."""
    def walk(node: TreeNode | None, so_far: int) -> int:
        if node is None:
            return 0
        so_far = so_far * 10 + node.val
        if node.left is None and node.right is None:
            return so_far
        return walk(node.left, so_far) + walk(node.right, so_far)

    return walk(root, 0)


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
    classic = from_list([-10, 9, 20, None, None, 15, 7])
    print(max_path_sum(classic))                    # 42   (15 -> 20 -> 7)
    print(max_path_sum_with_path(classic))          # (42, [15, 20, 7])

    # the floor matters
    print(max_path_sum(from_list([5, -100, 3])))    # 8    (5 -> 3), not -92

    # the answer can be negative: -inf, not 0
    print(max_path_sum(from_list([-3])))            # -3
    print(max_path_sum(from_list([-2, -1])))        # -1

    print(max_path_sum(from_list([1, 2, 3])))       # 6

    # root-to-leaf family
    t = from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    print(has_path_sum(t, 22))                      # True
    print(all_path_sums(t, 22))                     # [[5, 4, 11, 2]]
    print(binary_tree_paths(from_list([1, 2, 3, None, 5])))
    # ['1->2->5', '1->3']
    print(sum_root_to_leaf_numbers(from_list([1, 2, 3])))    # 25  (12 + 13)

    # the leaf trap: a one-sided node is NOT a leaf
    one_sided = from_list([1, 2])
    print(has_path_sum(one_sided, 1))               # False — 1 alone is not a path to a leaf
    print(has_path_sum(one_sided, 3))               # True

    # path sum III
    p = from_list([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    print(path_sum_iii(p, 8), path_sum_iii_naive(p, 8))      # 3 3
    print(path_sum_iii(from_list([1, None, 2, None, 3]), 3)) # 2
```

---

## 6. What it costs

### Maximum path sum

```
 time    O(n)      every node visited once
 space   O(height) the recursion stack
```

**One pass, one visit per node**, because the arm value each node needs from its children is computed
exactly once and returned upward. There is no recomputation to eliminate — unlike the naive diameter,
this problem has no obvious quadratic version to fall into.

### Root-to-leaf

```
 has_path_sum      O(n) time, O(height) space
 all_path_sums     O(n × height) time in the worst case, because each recorded
                   path is copied and a path is up to `height` long
                   O(n × height) space for the output
```

```
 a perfect tree of 1,000,000 nodes
   leaves        500,000
   path length   20
   output        500,000 × 20 = 10,000,000 integers  ≈  400 MB in Python
```

**Collecting all paths is `O(n × height)`, not `O(n)`**, and it is worth saying, because the output alone
can be enormous.

`binary_tree_paths` passing a string down is worse than it looks: each concatenation builds a new string,
so it is `O(n × height)` in copying too. Passing a list and joining once at a leaf is the faster version,
at the cost of an un-choose.

### Path sum III: the improvement worth showing

```
 naive:  a downward walk started at every node
           balanced tree:  O(n log n)
           degenerate:     O(n^2)

 prefix sums with a map:  O(n) time, O(height) extra space for the map
```

```
 n = 1,000       naive ~10,000        prefix ~1,000
 n = 100,000     naive ~1,700,000     prefix ~100,000
 n = 100,000 (a chain)  naive ~5,000,000,000   — will not finish
```

**The map holds at most `height` entries at any moment**, because entries are removed on the way out.
That is worth stating: it is `O(height)`, not `O(n)`, and the reason is the un-choose.

### The floor, and why it is not just an optimisation

```
 a tree of 1,000 nodes, values uniformly in [-100, 100]
   with the floor:     the answer is a genuinely positive path
   without:            the answer is dragged down by forced negative branches
                       and is simply WRONG, not slow
```

**`max(0, arm)` changes the answer, not the speed.** It is not an optimisation and calling it one in an
interview is a tell.

### Space, and the deep-tree warning

```
 max_path_sum           O(height)
 max_path_sum_with_path O(n)        every frame holds a list
 all_path_sums          O(n × height) for the output
```

```
 a chain of 10,000 nodes -> RecursionError: maximum recursion depth exceeded
```

Same as every tree problem. If the constraint allows a chain, either convert to an explicit postorder
stack or say the risk.

---

## 7. The traps

### Trap 1 — `node is None` as the leaf test

```python
        if node is None:
            return remaining == 0           # WRONG
```

A node with one child has a `None` on the other side, so this reports a "path" that stops halfway.

```
 has_path_sum(from_list([1, 2]), 1)
   this version -> True        (it "found" the path [1], stopping at the missing right child)
   correct      -> False       (1 is not a leaf)
```

**A leaf is a node with both children `None`.** Test it on the node, not on the recursion.

### Trap 2 — returning the bent path to the parent

```python
        return max(left + right + node.val, node.val + max(left, right))     # WRONG
```

Devaraj's nephew. The parent may then build on a path that has already used both of my children, giving
routes that double back. The result is too large and grows with depth — no error, and it passes on trees
where one child is always missing.

**Return one arm. Record the bend. Say the reason.**

### Trap 3 — no floor on the arms

```python
        left = arm(node.left)
        right = arm(node.right)
```

```
 max_path_sum(from_list([5, -100, 3]))
   without the floor -> -92
   correct           ->   8
```

A negative branch is dragged into every path through the node. **You are never obliged to take a
branch.**

### Trap 4 — flooring the answer instead of the arms

```python
    best = 0                                # WRONG
```

```
 max_path_sum(from_list([-3]))
   with best = 0    ->  0        — but 0 is not a path; there is no empty path
   correct          -> -3
```

The floor says "an *arm* may contribute nothing". It does not say "the answer may be nothing", because a
path must contain at least one node. **`float("-inf")`.**

### Trap 5 — the wrong definition of "path"

Solving root-to-leaf when they meant any-to-any, or the reverse, produces a completely different answer
with confident code. **Ask, or state the assumption in your first sentence.**

### Trap 6 — forgetting the un-choose in path sum III

```python
        seen[running] += 1
        walk(node.left, running)
        walk(node.right, running)
                                            # missing: seen[running] -= 1
```

The map accumulates prefixes from sibling branches, so it counts paths that bend — which is not what
"downward path" means.

```
 path_sum_iii(from_list([1, -1, 1]), 1)
   without the un-choose: an over-count
   with:                  correct
```

**No error, just a number that is too large.** [Day 094's](../day-094-backtracking/README.md) rule applied
to a dictionary.

### Trap 7 — forgetting `seen[0] = 1`

```python
    seen = defaultdict(int)                 # missing seen[0] = 1
```

Every path that starts at the root is missed, because there is no empty prefix to subtract. Exactly the
same sentinel as [day 037](../day-037-prefix-sums/README.md)'s `prefix[0] = 0`.

### Trap 8 — string concatenation down a deep tree

```python
        so_far = so_far + "->" + str(node.val)
```

Each concatenation copies the whole string, so on a chain of `n` nodes this is `O(n²)` in copying alone.
Correct, and slow enough to time out on a large skewed tree. Pass a list and join once at the leaf.

---

## 8. In the interview

### How it gets asked

- The hard one: *"Find the maximum path sum. A path can start and end at any node."* LeetCode 124.
- The easier opener: *"Does any root-to-leaf path sum to this target?"* LeetCode 112, then 113 for all of
  them.
- The one with a trick: *"Count the paths summing to a target, going downwards."* LeetCode 437.
- The follow-up: *"Return the path, not just the sum."*
- The probe: *"What does your function return, and why is that not the answer?"*

### What to say out loud, in the first ninety seconds

1. **Pin down "path" first.** "Can the path start and end anywhere, or is it root-to-leaf? And can it bend
   at a node? Those are three different problems."
2. **State the key observation.** "Every path has exactly one highest node — the point where it turns
   around. So I evaluate every node as that turning point and I have considered every path exactly once."
3. **Name the two quantities, and say they differ.** "At each node there are two numbers. The best path
   that *bends* here, which is `left + right + value` — that is the answer candidate, and I record it. And
   the best single *arm* going down, which is `value + max(left, right)` — that is what I return, because
   my parent can only extend one arm."
4. **Say why the parent cannot use the recorded value.** "A path that bends at me has already used both my
   children, so it cannot also continue upward through me."
5. **Introduce the floor with its reason.** "I floor each arm at zero, because I am never obliged to take a
   branch — if the best it offers is negative, taking nothing is better and contributes zero. That is
   Kadane's rule on two branches."
6. **Flag the initialisation.** "And `best` starts at negative infinity, not zero — the floor applies to
   the arms, not to the answer. An all-negative tree has a best path of one node."

### The follow-ups

**"What does your function return, and why is that not the answer?"**
"It returns the best single downward arm from this node — the node's value plus the better of its two
children's arms. That is not the answer, because the answer is the best path that *bends* somewhere, and a
bent path uses both children. My parent can only extend a path that comes up through me on one side, so a
bent path is useless to it. So I keep the two apart: I **record** `left + right + value` in an outer
variable as a candidate answer, and I **return** `value + max(left, right)` for my parent to build on.
Merging them — returning the larger of the two — is the classic bug: it lets a parent extend a path that
has already turned around, producing routes that revisit nodes, and the answer comes out too large with no
error at all."

**"Why the `max(0, ...)`?"**
"Because a branch is optional. If the best the left subtree can offer is negative, I do not take it — the
path simply does not go that way, and 'not going that way' contributes zero. Without the floor, a single
very negative node poisons every path through its parent: on `[5, -100, 3]` the answer comes out as −92
instead of 8. It is exactly Kadane's algorithm from the array world — drop the running sum when it goes
negative — applied to two branches instead of one. And the important distinction is that the floor applies
to the **arms**, not to the **answer**: `best` must start at negative infinity, because a path has to
contain at least one node, so an all-negative tree's answer is the least-negative single value, not zero."

**"Count the downward paths summing to k."**
"The obvious solution starts a downward walk at every node — `O(n log n)` on a balanced tree and `O(n²)`
on a chain. The better one is prefix sums with a hash map, which is exactly the subarray-sum-equals-k
technique on the current root-to-node path: keep a running sum, and at each node add the number of
earlier prefixes equal to `running − target`. The critical detail is that I **remove the prefix on the way
back out** — `seen[running] -= 1`. The map must contain only the prefixes on the current path, because a
prefix from a sibling branch is not reachable going downward from here. Without that line, the count
includes paths that bend, which is not what was asked, and there is no error — just a number that is too
big. It also means the map holds at most `height` entries, so the extra space is `O(height)` rather than
`O(n)`. And I need `seen[0] = 1` for the empty prefix, or every path starting at the root is missed."

**"Return the path itself."**
"Same shape with a bigger return value: each call returns both the arm sum and the list of nodes on that
arm, and when a node beats the best, the winning path is the left arm plus this node plus the right arm
reversed. The cost changes and I would say so — every frame now holds a list, so the space goes from
`O(height)` to `O(n)`. If that mattered, the alternative is to record only the *node* where the best bend
occurred in the first pass, then do a second short walk from there to reconstruct both arms — two passes,
`O(height)` space."

**"What is the complexity?"**
"`O(n)` time — every node visited exactly once, and each node's arm value is computed once and returned
upward, so there is nothing to recompute. `O(height)` space for the recursion stack, which is about twenty
frames on a balanced million-node tree and a million on a chain — and Python's default recursion limit is a
thousand, so if the input can be skewed and large I would either write it with an explicit postorder stack
or say the risk out loud."

**"How is this different from the root-to-leaf version?"**
"The direction the information travels, and therefore the traversal. Root-to-leaf carries the remaining
target **down** as an argument — preorder, and nothing needs undoing because a value passed as an argument
cannot be modified by the callee. Any-to-any brings the arm sums **up** as return values — postorder, with
the record/return split. There is one more difference that catches people: root-to-leaf has **no floor**,
because you are obliged to reach a leaf and cannot decline the only branch available. The floor exists
precisely because an any-to-any path may stop anywhere."

### A model answer

Asked: *find the maximum path sum in the binary tree, where a path may start and end at any node.*

> "First, let me pin down 'path', because there are three versions of this question. Root-to-leaf, which
> must start at the root and end at a leaf. Strictly downward but starting anywhere. And any-to-any, where
> the path may **bend** at one node. You have said any-to-any, so the path goes up one side, turns around
> at some node, and comes down the other.
>
> The observation that makes it tractable: **every path has exactly one highest node** — the point where
> it turns. So if I evaluate every node as that turning point, I have considered every possible path
> exactly once, with no duplication.
>
> At each node there are **two different numbers**, and keeping them apart is the whole problem. The best
> path that **bends** here is `left arm + right arm + my value` — that is a candidate for the answer, so I
> **record** it in a variable outside the recursion. The best single **arm** going down from here is
> `my value + max(left arm, right arm)` — and that is what I **return**, because my parent can only extend
> a path that arrives through me on one side. My parent cannot use the bent number: a path that turns
> around at me has already spent both of my children, so it cannot also continue upward.
>
> Confusing those two is the classic failure — it lets a parent build on a path that has already turned
> around, so you get routes that revisit nodes, and the answer is too large with no error.
>
> Then the part that negative values force. I **floor each arm at zero**: `max(0, arm)`. I am never obliged
> to take a branch, so if the best the left subtree offers is negative, I take nothing and that contributes
> zero. Without it, one very negative node poisons every path through its parent — on `[5, -100, 3]` you
> get −92 instead of 8. It is Kadane's rule, on two branches instead of one.
>
> And the trap that the floor creates: `best` must start at **negative infinity**, not zero. The floor says
> an *arm* may contribute nothing; it does not say the *answer* may be nothing, because a path must contain
> at least one node. On a tree of all-negative values the answer is the least-negative single node, and
> initialising to zero returns zero, which is not a path.
>
> That is nine lines. `O(n)` time — one visit per node, and each arm computed once — and `O(height)` space
> for the stack, so about twenty frames on a balanced million-node tree and a million on a chain, which is
> the case where I would want an explicit stack instead."

---

## 9. Recall card

- **Pin down "path" first: root-to-leaf (state goes DOWN as an argument, preorder, no undo) or any-to-any
  (arms come UP as return values, postorder, the record/return split).** They are different problems, and
  root-to-leaf has **no floor** because you cannot decline the only branch.
- **Every path has exactly one highest node**, so evaluate every node as the turning point. Then keep two
  quantities apart: **RECORD `left + right + val`** (the bend — the answer candidate) and **RETURN
  `val + max(left, right)`** (one arm — all the parent can extend). Merging them lets a parent build on a
  path that has already turned around: too large, no error.
- **Floor each arm: `max(0, arm)`** — you are never obliged to take a branch, so a negative arm contributes
  nothing. Without it, `[5, -100, 3]` gives **−92 instead of 8**. This is Kadane's rule on two branches.
- **But initialise `best` to `-inf`, not 0** — the floor applies to the **arms**, not the **answer**. A
  path must contain a node, so `[-3]` answers **−3**, and starting at 0 answers 0, which is not a path.
- **A leaf is a node with BOTH children `None`** — `node is None` makes a one-sided node look like a leaf.
  And **path sum III is not this shape**: it is **prefix sums with a hash map** on the current root-to-node
  path (`seen[0] = 1`, `count += seen[running - target]`), with **`seen[running] -= 1` on the way out** —
  which keeps it `O(n)` time, `O(height)` space, and without it you silently count paths that bend.
