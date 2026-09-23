---
day: 108
track: dsa
title: "Validating a binary search tree"
phase: "Trees and binary search trees"
status: written
---

# Day 108 · DSA — Validating a binary search tree

**After today you can:** You avoid the classic wrong answer and can show the input that kills it.

**The interviewer asks it as:** *Is this a valid BST? Are you sure your check is correct?*

---

## 1. What this is, and why they ask it

Given a binary tree, decide whether it satisfies the [BST invariant](../day-106-bst-property/README.md):
at every node, **all** values in the left subtree are smaller and **all** values in the right subtree are
larger.

Three sentences. There is one wrong answer that almost everybody writes first — checking each node
against its immediate children — and it is wrong in a specific, demonstrable way that the interviewer
already has a test case for. There are two correct answers: **carry a permitted range down from the
ancestors**, or **walk inorder and check the values strictly increase**. And there is a third thing being
tested, which is whether you notice the edge cases: duplicates, and using a sentinel like `INT_MIN` as a
starting bound when the tree can contain `INT_MIN`.

They ask it because *"are you sure your check is correct?"* is one of the few interview questions where
the interviewer knows in advance that most candidates will be wrong, and the follow-up is not a hint — it
is the question. Being able to produce the failing input yourself, before being shown it, is the whole
performance.

---

## 2. The story

The hostel had three blocks off a central corridor and Prakash had been the warden's assistant for a year
and a half.

The rules had accumulated over about thirty years and they were all painted on boards at the point where
the rule started applying.

At the entrance to the whole building: *residents only*.

At the mouth of B block: *second and third year only*.

Halfway down B block, where the corridor split: *rooms 40 to 60, third year only*.

And then on individual doors, occasionally, something like *two occupants maximum*.

The point of putting the signs at the junctions was that every sign you walked past still applied. By the
time you were standing outside room 47, four rules were in force at once — the entrance rule, the block
rule, the corridor rule and the door rule — and you had passed all four of them to get there.

In September there was a mess, and it happened because of how the checking was done.

A second-year student, Faisal, was given room 47. The clerk who allocated it had looked at the sign on the
door, which said nothing about year, and at the sign at the corridor split, which he had misread, and he
had signed the form.

Prakash caught it in October during the inspection, and what he found interesting was that the clerk had
not been careless in the way you would expect. The clerk had checked a sign. He had checked the nearest
one. What he had not done was carry the earlier ones with him.

Prakash's rule after that, which he explained to every new clerk, was that you do not check the sign on
the door. You **walk in from the gate**, and at every board you pass, you make the rule narrower, and you
keep all of it in your head until you reach the room.

You start at the gate with no restriction at all — anybody. At the entrance you are down to residents. At
B block you are down to second and third years. At the corridor split you are down to third years only.
And *then* you look at the boy.

He said the mistake is not that people ignore signs. It is that they read the last one and assume it
contains the others, and it does not — it only narrows what was already there.

There was a second way to check the same thing, which the old warden had used and which Prakash also
kept, because it caught different mistakes. Once a term, he walked the entire building in one fixed
order — block A room 1 to the end, then B, then C — and read out the year of every occupant in turn. If
that sequence ever went backwards, something was wrong somewhere, and he did not need to know the rules at
all to see it.

---

## 3. The idea in plain English

Prakash has both correct algorithms, and the clerk has the classic bug.

- The signs are the BST constraints, and **each one narrows what the previous ones allowed**.
- Checking only the door sign is **the local check**, and it is the wrong answer.
- Walking in from the gate carrying every rule is the **range** method.
- Reading every occupant in one fixed order and noticing when it goes backwards is the **inorder** method.

### The wrong answer, and exactly why

```python
    def is_bst_wrong(node):
        if node is None:
            return True
        if node.left and node.left.val >= node.val:
            return False
        if node.right and node.right.val <= node.val:
            return False
        return is_bst_wrong(node.left) and is_bst_wrong(node.right)
```

Every parent-child pair is checked and every one of them passes on this tree:

```
        10
       /  \
      5    15
          /  \
         6    20
         ^
   6 < 15, so node 15 is satisfied
   but 6 is in the RIGHT subtree of 10, and 6 < 10
   -> NOT a BST
```

**The check is local; the invariant is global.** A node must be consistent with **every ancestor**, not
just its parent — the clerk reading only the door sign.

**Have this counter-example ready before they ask for it.** `[10, 5, 15, null, null, 6, 20]` is the
standard one and it is worth memorising, because producing it yourself is what the question rewards.

### Correct method one: carry the range down

Every node inherits a permitted open interval from its ancestors. Going **left** tightens the upper bound;
going **right** tightens the lower bound.

```python
    def is_bst(node, low=None, high=None):
        if node is None:
            return True                     # an empty tree is a valid BST
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        return (is_bst(node.left, low, node.val)        # upper bound tightens
                and is_bst(node.right, node.val, high)) # lower bound tightens
```

**Read the two recursive calls aloud**: *"everything on my left must also be below me; everything on my
right must also be above me."* The bounds accumulate exactly as Prakash's signs do.

On the counter-example: node 6 arrives with the range `(10, 15)` — lower bound 10 from turning right at
the root, upper bound 15 from turning left at 15 — and `6 <= 10`, so it fails. **The root's constraint
survived two levels**, which is precisely what the local check loses.

**Use `None` for "unbounded", not `INT_MIN` and `INT_MAX`.** That is trap 3, and it is a real failure:
LeetCode's constraints allow node values equal to `-2³¹`, so a tree containing exactly that value is
rejected by a version seeded with `INT_MIN`. `float("-inf")` also works in Python; `None` is clearer and
language-independent.

### Correct method two: inorder must strictly increase

From [day 100](../day-100-dfs-traversals/README.md): an inorder traversal of a BST produces sorted order.
So walk inorder and check each value against the one before it.

```python
    def is_bst_inorder(root):
        previous = None

        def walk(node):
            nonlocal previous
            if node is None:
                return True
            if not walk(node.left):
                return False                # short-circuit
            if previous is not None and node.val <= previous:
                return False
            previous = node.val
            return walk(node.right)

        return walk(root)
```

**Keep only the previous value, not the whole list.** Building the list first and then checking it is
correct and uses `O(n)` extra space; tracking one variable uses `O(height)`.

**`<=`, not `<`.** Equal values break the invariant under the usual "no duplicates" convention, and using
`<` silently accepts a tree with repeats.

The two methods catch the same errors, and the inorder one has a nice property: **it needs no knowledge of
the rules at all** — Prakash's termly walk. Anything out of order is wrong, whatever caused it.

### Which to write

```
 range method     O(n) time, O(height) space, no shared state
                  -> the one to write; it expresses the invariant directly

 inorder method   O(n) time, O(height) space, one mutable variable
                  -> shorter, and the natural answer if you have just done traversals
                  -> also the basis for "find the two swapped nodes" (LeetCode 99)
```

**Write the range version and mention the inorder one.** The range version *is* the invariant, so
explaining it explains the definition; the inorder version relies on a fact you then have to justify.

### The edge cases they will probe

**Duplicates.** The standard problem says values are unique and a duplicate makes it invalid, which is why
both methods use `<=` and `>=` rather than `<` and `>`. If the convention were "duplicates go left", the
left comparison would loosen to `<` and the right would stay strict. **Say which convention you are
assuming.**

**Integer bounds.** Covered above — `None`, not `INT_MIN`.

**The empty tree and a single node.** Both valid. The range version handles them without a special case,
which is a small point in its favour.

**A very deep tree.** Both are `O(height)` on the stack, so a chain of ten thousand raises
`RecursionError`. The iterative inorder version — the stack-based walk from
[day 100](../day-100-dfs-traversals/README.md) — is immune, and it is the version to offer if the
constraint allows a chain.

### The sibling problem worth knowing

**LeetCode 99, "Recover Binary Search Tree":** exactly two nodes have been swapped; put them back. It is
the inorder method with one extra idea — walk inorder, and every place the sequence goes backwards is a
**violation**. There are either one or two violations:

```
 two ADJACENT nodes swapped:      1 violation   -> the two nodes are that pair
 two NON-ADJACENT nodes swapped:  2 violations  -> take the FIRST node of the first
                                                   and the SECOND node of the second
```

**Swap their values and the tree is repaired in `O(n)` time and `O(height)` space.** Knowing that "one or
two violations" rule is the whole problem.

---

## 4. The picture

The counter-example that kills the local check. **Learn this tree.**

```
        10
       /  \
      5    15
          /  \
         6    20

 LOCAL CHECK (wrong):
   node 10:  left 5 < 10 ✓   right 15 > 10 ✓
   node 15:  left 6 < 15 ✓   right 20 > 15 ✓
   node 5, 6, 20: leaves ✓
   -> every parent-child pair passes  ->  reports VALID

 THE TRUTH:
   6 is in the RIGHT subtree of 10, and 6 < 10
   -> NOT a BST
   -> search(6) at the root goes LEFT (6 < 10) and never finds it
```

The range method on the same tree:

```
                     10          allowed: (-inf, +inf)   ✓
                   /    \
                  /      \
        5  (-inf, 10) ✓   15  (10, +inf) ✓
                         /    \
            6  (10, 15)  ✗    20  (15, +inf) ✓
               ^
               6 <= 10, and the lower bound 10 came from the ROOT,
               two levels up. That is the constraint the local check loses.

 going LEFT  -> the HIGH bound becomes the parent's value
 going RIGHT -> the LOW  bound becomes the parent's value
 bounds NARROW as you descend and are never widened.
```

Prakash's corridor, as the same picture:

```
 gate           anybody
   │
 entrance       residents only                    ← narrows
   │
 B block        2nd and 3rd year                  ← narrows again
   │
 corridor split 3rd year only                     ← narrows again
   │
 room 47        [check the student HERE]

 the clerk checked only the last sign.
 Faisal (2nd year) passes the door sign and fails the corridor sign
 he had already walked past.
```

The inorder method, on both trees:

```
 VALID                            INVALID (the counter-example)
        10                               10
       /  \                             /  \
      5    15                          5    15
     / \   / \                             /  \
    3   7 12  18                          6    20

 inorder: 3 5 7 10 12 15 18       inorder: 5 10 6 15 20
          strictly increasing ✓                 ^
                                            6 < 10 — the sequence went BACKWARDS
                                            -> invalid, and you did not need to
                                               know a single rule to see it
```

The swapped-nodes problem, and the one-or-two rule:

```
 correct:   1  3  5  7  9  11

 ADJACENT swap (5 and 7):
   1  3  7  5  9  11
            ^
   ONE violation. The two culprits are that pair: 7 and 5.

 NON-ADJACENT swap (3 and 11):
   1  11  5  7  9  3
        ^           ^
   TWO violations. Take the FIRST element of the first violation (11)
   and the SECOND element of the second (3). Swap them back.
```

---

## 5. The code, built step by step

### Step 1 — say the wrong answer out loud, and kill it

"The version people write first checks each node against its immediate children. That is not the
invariant — the invariant is about whole subtrees. Here is a tree that passes it and is not a BST." Then
draw `[10, 5, 15, null, null, 6, 20]`.

**Producing the counter-example yourself, unprompted, is the single highest-value thing you can do in this
question.**

### Step 2 — state the invariant as a range

"Every node lives inside an open interval inherited from all of its ancestors. Going left tightens the
upper bound to the parent's value; going right tightens the lower bound. So I pass the interval down."

### Step 3 — write the bounds as `None`, and say why

```python
    def check(node, low=None, high=None):
```

"I use `None` for unbounded rather than `INT_MIN` and `INT_MAX`, because the tree is allowed to contain
those values, and seeding with them would reject a perfectly valid tree."

### Step 4 — the two recursive calls, read aloud

```python
        return (check(node.left, low, node.val)
                and check(node.right, node.val, high))
```

"Everything on my left must also be below me. Everything on my right must also be above me. The bounds
only ever narrow."

### Step 5 — offer the inorder alternative

"There is a second method: walk inorder and check the values strictly increase, keeping only the previous
value rather than the whole list. It is shorter, and it is the basis for the follow-up where two nodes
have been swapped."

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


def is_bst_wrong(node: TreeNode | None) -> bool:
    """THE CLASSIC WRONG ANSWER. Checks each node against its immediate
    children only.

    Every parent-child pair can pass while the tree is still not a BST,
    because a node must satisfy EVERY ancestor, not just its parent.

    Killer input: [10, 5, 15, None, None, 6, 20] — reports True, and
    search(6) cannot find 6.
    """
    if node is None:
        return True
    if node.left and node.left.val >= node.val:
        return False
    if node.right and node.right.val <= node.val:
        return False
    return is_bst_wrong(node.left) and is_bst_wrong(node.right)


def is_bst(node: TreeNode | None,
           low: int | None = None,
           high: int | None = None) -> bool:
    """LeetCode 98, method one: carry the permitted RANGE down.

    Every node inherits an open interval from ALL its ancestors:
      going left  -> the HIGH bound becomes the parent's value
      going right -> the LOW  bound becomes the parent's value

    `None` means unbounded, NOT INT_MIN/INT_MAX — the tree is allowed to
    contain those values, and seeding with them rejects valid trees.

    `<=` and `>=` because equal values are invalid under the no-duplicates
    convention. Say which convention you are assuming.

    Time O(n), space O(height).
    """
    if node is None:
        return True                         # an empty tree is a valid BST
    if low is not None and node.val <= low:
        return False
    if high is not None and node.val >= high:
        return False
    return (is_bst(node.left, low, node.val)        # left: below me too
            and is_bst(node.right, node.val, high)) # right: above me too


def is_bst_inorder(root: TreeNode | None) -> bool:
    """Method two: inorder must be STRICTLY increasing.

    Keep only the PREVIOUS value, not the whole list — O(height) instead of
    O(n) extra space. And `<=`, not `<`, or duplicates slip through.
    """
    previous: int | None = None

    def walk(node: TreeNode | None) -> bool:
        nonlocal previous
        if node is None:
            return True
        if not walk(node.left):
            return False                    # short-circuit on the first failure
        if previous is not None and node.val <= previous:
            return False
        previous = node.val
        return walk(node.right)

    return walk(root)


def is_bst_iterative(root: TreeNode | None) -> bool:
    """The inorder method with an explicit stack. Immune to deep trees, which
    matters when the input can be a chain of 10,000 nodes."""
    stack: list[TreeNode] = []
    node = root
    previous: int | None = None

    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if previous is not None and node.val <= previous:
            return False
        previous = node.val
        node = node.right

    return True


def is_bst_allowing_duplicates_left(node: TreeNode | None,
                                    low: int | None = None,
                                    high: int | None = None) -> bool:
    """The same, under the "equal values go LEFT" convention.

    Only ONE comparison loosens: the left bound allows equality.
    Worth writing once, to see that the convention lives in the operators.
    """
    if node is None:
        return True
    if low is not None and node.val <= low:
        return False
    if high is not None and node.val > high:         # was >=
        return False
    return (is_bst_allowing_duplicates_left(node.left, low, node.val)
            and is_bst_allowing_duplicates_left(node.right, node.val, high))


def recover_bst(root: TreeNode | None) -> None:
    """LeetCode 99. Exactly two nodes were swapped. Put them back, in place.

    Walk inorder and find where the sequence goes BACKWARDS:
      two ADJACENT nodes swapped     -> ONE violation; the pair is that pair
      two NON-ADJACENT nodes swapped -> TWO violations; take the FIRST node
                                        of the first and the SECOND of the second

    O(n) time, O(height) space. Swapping the VALUES avoids all pointer surgery.
    """
    first: TreeNode | None = None
    second: TreeNode | None = None
    previous: TreeNode | None = None

    def walk(node: TreeNode | None) -> None:
        nonlocal first, second, previous
        if node is None:
            return
        walk(node.left)
        if previous is not None and previous.val > node.val:
            if first is None:
                first = previous            # the FIRST of the first violation
            second = node                   # the SECOND of the latest violation
        previous = node
        walk(node.right)

    walk(root)
    if first and second:
        first.val, second.val = second.val, first.val


def find_violations(root: TreeNode | None) -> list[tuple[int, int]]:
    """A debugging helper: every place the inorder sequence goes backwards.
    Useful for showing an interviewer WHERE a tree is broken, not just that
    it is."""
    out: list[tuple[int, int]] = []
    previous: int | None = None

    def walk(node: TreeNode | None) -> None:
        nonlocal previous
        if node is None:
            return
        walk(node.left)
        if previous is not None and node.val <= previous:
            out.append((previous, node.val))
        previous = node.val
        walk(node.right)

    walk(root)
    return out


def largest_bst_subtree(root: TreeNode | None) -> int:
    """The escalation: the size of the largest subtree that IS a BST.
    LeetCode 333.

    The same postorder return-value trick as day 102: each call returns
    (is_bst, size, min, max) and the parent combines them. One pass, O(n).
    """
    best = 0

    def walk(node: TreeNode | None) -> tuple[bool, int, int, int]:
        nonlocal best
        if node is None:
            return True, 0, float("inf"), float("-inf")   # type: ignore[return-value]
        l_ok, l_size, l_min, l_max = walk(node.left)
        r_ok, r_size, r_min, r_max = walk(node.right)
        if l_ok and r_ok and l_max < node.val < r_min:
            size = l_size + r_size + 1
            best = max(best, size)
            return True, size, min(l_min, node.val), max(r_max, node.val)
        return False, 0, float("-inf"), float("inf")      # type: ignore[return-value]

    walk(root)
    return best


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


if __name__ == "__main__":
    valid = from_list([10, 5, 15, 3, 7, 12, 18])
    print(is_bst(valid), is_bst_inorder(valid), is_bst_iterative(valid))
    # True True True

    # THE COUNTER-EXAMPLE — memorise this tree
    killer = from_list([10, 5, 15, None, None, 6, 20])
    print(is_bst_wrong(killer))             # True   <- WRONG
    print(is_bst(killer))                   # False  <- correct
    print(is_bst_inorder(killer))           # False
    print(inorder(killer))                  # [5, 10, 6, 15, 20]  <- goes backwards
    print(find_violations(killer))          # [(10, 6)]

    # the simplest failing case for the local check
    small = from_list([5, 1, 4, None, None, 3, 6])
    print(is_bst_wrong(small), is_bst(small))               # True False

    # duplicates
    dup = from_list([2, 2, 2])
    print(is_bst(dup))                                      # False
    print(is_bst_allowing_duplicates_left(from_list([2, 2])))   # True

    # the INT_MIN trap, demonstrated
    edge = TreeNode(-2**31)
    print(is_bst(edge))                                     # True
    # a version seeded with low = -2**31 and using <= would return False here.

    # edge cases
    print(is_bst(None), is_bst(TreeNode(1)))                # True True

    # a valid BST whose child comparison alone would look suspicious
    print(is_bst(from_list([1, None, 2, None, 3])))         # True — a right chain

    # recover a swapped tree
    broken = from_list([3, 1, 4, None, None, 2])            # 2 and 3 swapped
    print(inorder(broken))                                  # [1, 3, 2, 4]
    recover_bst(broken)
    print(inorder(broken), is_bst(broken))                  # [1, 2, 3, 4] True

    far = from_list([1, None, 11, 5, None, None, 9, 3])     # non-adjacent swap
    print(inorder(far))
    recover_bst(far)
    print(inorder(far), is_bst(far))

    print(largest_bst_subtree(from_list([10, 5, 15, 1, 8, None, 7])))    # 3
```

---

## 6. What it costs

### Both correct methods

```
 time    O(n)        every node visited once
 space   O(height)   the recursion stack (or the explicit stack)
```

```
 balanced, n = 1,000,000     ~20 frames
 degenerate, n = 10,000      RecursionError at ~1,000
```

**Neither method is faster.** They differ in what they express and in what they generalise to, not in
cost. The range method states the invariant; the inorder method generalises to "find the swapped nodes"
and to "how many violations are there".

### The version that costs more

```python
    values = inorder(root)
    return all(a < b for a, b in zip(values, values[1:]))
```

Correct, and `O(n)` **extra space** for the list rather than `O(height)`.

```
 n = 1,000,000
   list version:      ~40 MB for the values
   previous-only:     one integer, plus ~20 stack frames
```

**Keeping only the previous value is the whole difference**, and it is worth doing even though the list
version is easier to write.

### Short-circuiting

Both methods stop at the first violation, and the `and` ordering matters:

```python
        if not walk(node.left):
            return False                    # do not walk the right subtree
```

```
 a violation in the leftmost leaf of a million-node tree
   with short-circuit:     ~20 nodes visited
   without (build the list first): 1,000,000
```

**The worst case is the same `O(n)`; the common case is very different.** An invalid tree usually fails
early.

### The largest-BST-subtree escalation

```
 naive:  for each node, check whether its subtree is a BST, then count
         -> is_bst is O(subtree), called at every node
         -> O(n log n) balanced, O(n^2) on a chain

 one pass: return (is_bst, size, min, max) upward
         -> O(n)
```

```
 n = 10,000, a chain
   naive:    ~50,000,000 operations
   one pass:      10,000
```

**Same shape as [day 102's](../day-102-height-and-diameter/README.md) diameter fix** — the information the
parent needs is already being computed, so return it instead of recomputing.

### Why the local check is not merely slower

It is not a performance question at all. **It returns the wrong answer**, in `O(n)`, with no error. That
distinction is worth stating: this is not an optimisation problem, it is a correctness problem.

---

## 7. The traps

### Trap 1 — the local check

```python
        if node.left and node.left.val >= node.val:
            return False
```

```
 is_bst_wrong(from_list([10, 5, 15, None, None, 6, 20]))  ->  True
 the correct answer is False
```

**The invariant is about subtrees, not children.** Every parent-child pair can pass while a node violates
its grandparent. Have the counter-example ready.

### Trap 2 — checking only against the parent's value in a range version

```python
        return (is_bst(node.left, low, node.val)
                and is_bst(node.right, node.val, node.val))    # `high` dropped
```

A subtler version of the same bug: the upper bound from an ancestor is lost, so a value that is too large
for a grandparent slips through on the right. **The bounds must be threaded through unchanged where they
are not being narrowed.**

### Trap 3 — `INT_MIN` and `INT_MAX` as the initial bounds

```python
    return check(root, -2**31, 2**31 - 1)
```

LeetCode's constraints allow node values in exactly that range, so a tree consisting of the single node
`-2³¹` is rejected by a version that compares with `<=` against a seed of `-2³¹`.

```
 is_bst_with_intmin(TreeNode(-2**31))  ->  False
 the correct answer is True
```

**Use `None`, or `float("-inf")`.** This is the specific edge case interviewers use to separate careful
candidates.

### Trap 4 — `<` instead of `<=`

```python
        if previous is not None and node.val < previous:
            return False                    # allows equality
```

```
 is_bst_inorder(from_list([2, 2, 2]))  with `<`  ->  True
 correct under the no-duplicates convention      ->  False
```

**Equal values violate the standard invariant.** If the convention allows duplicates on one side, exactly
one comparison loosens — say which convention you are using rather than guessing.

### Trap 5 — building the whole inorder list

```python
    values = inorder(root)
    return values == sorted(values)
```

Correct, `O(n)` extra space, and `O(n log n)` if you actually sort. **Track the previous value.** And
`values == sorted(values)` also accepts duplicates, so it fails trap 4 too.

### Trap 6 — a global `previous` that is not reset

```python
    previous = None                         # module level

    def is_bst_inorder(root):
        def walk(node): ...
```

The second call to the function sees the last value from the first call and can wrongly reject a valid
tree. **Declare `previous` inside the function**, which the version above does. This is the kind of bug
that passes one test and fails a suite.

### Trap 7 — recursion depth

```
 is_bst(chain_of_10000_nodes)
 RecursionError: maximum recursion depth exceeded
```

A valid BST built from sorted data is exactly this shape, so it is not an unusual input. The iterative
inorder version is immune.

### Trap 8 — forgetting that `is_bst_wrong` also passes many *invalid* trees silently

The reason this matters beyond the interview: a tree that fails the global invariant but passes the local
one is one where **`search` cannot find values that are present**, as on
[day 106](../day-106-bst-property/README.md). The local check would certify such a tree as fine, which is
the worst possible outcome for a validation function.

---

## 8. In the interview

### How it gets asked

- The question: *"Determine whether this binary tree is a valid BST."* LeetCode 98.
- The follow-up, which is the real question: *"Are you sure your check is correct?"*
- The edge case: *"What if a node's value is `INT_MIN`?"*
- The convention: *"What about duplicate values?"*
- The escalation: *"Two nodes have been swapped. Repair the tree."* LeetCode 99.
- The harder one: *"Find the largest subtree that is a BST."* LeetCode 333.

### What to say out loud, in the first ninety seconds

1. **Restate the invariant with the word that matters.** "A BST requires that at every node, **all** the
   values in the left subtree are smaller and **all** in the right are larger. Not just the immediate
   children."
2. **Kill the wrong answer before writing anything.** "The version most people write checks each node
   against its two children. That is not the invariant, and here is a tree that passes it and is not a
   BST" — and draw `[10, 5, 15, null, null, 6, 20]`.
3. **Give the correct formulation.** "Every node lives inside an open interval inherited from **all** its
   ancestors. Going left tightens the upper bound; going right tightens the lower bound. So I pass the
   interval down and check the node against both ends."
4. **Pre-empt the sentinel trap.** "I use `None` for unbounded rather than `INT_MIN` and `INT_MAX`,
   because node values are allowed to be exactly those, and seeding with them would reject a valid tree."
5. **State the duplicate convention.** "I assume values are unique, so I use `<=` and `>=` — equal values
   are invalid. If duplicates are allowed on one side, exactly one comparison loosens."
6. **Offer the second method.** "There is an equivalent check: walk inorder and confirm the values
   strictly increase, keeping only the previous value. `O(n)` time and `O(height)` space either way, and
   the inorder one is what the swapped-nodes follow-up builds on."

### The follow-ups

**"Are you sure your check is correct?"**
"I would answer that by showing you the input that breaks the version I am *not* writing. Take
`[10, 5, 15, null, null, 6, 20]`. Node 15 has a left child of 6, and 6 is less than 15, so that pair
passes. Node 10 has children 5 and 15, which also pass. Every parent-child comparison in the tree is
satisfied — and it is not a BST, because 6 sits in the **right subtree of 10** and is less than 10. The
practical consequence is worse than the abstract one: `search(6)` starts at the root, sees 6 < 10, goes
left, and never finds a value that is in the tree. So the local check certifies exactly the trees whose
brokenness is most dangerous. My version passes a range down from every ancestor, so 6 arrives with a
lower bound of 10 — set two levels above it — and fails."

**"What if a node's value is `INT_MIN`?"**
"That is why I use `None` for the initial bounds rather than `INT_MIN` and `INT_MAX`. The constraints on
this problem allow node values down to `-2³¹`, so a tree consisting of the single node `-2³¹` is a
perfectly valid BST — and a version seeded with `low = -2³¹` and comparing `node.val <= low` rejects it.
`float("-inf")` also works in Python, but `None` is clearer and does not depend on the language having an
infinity. It is a small thing, and it is exactly the sort of thing that turns a correct-looking solution
into a failing submission."

**"What about duplicates?"**
"Under the standard convention — which is what this problem assumes — duplicates make the tree invalid, so
both my comparisons are `<=` and `>=` rather than `<` and `>`. Using strict inequalities there silently
accepts `[2, 2, 2]`. If the convention were 'equal values go left', then exactly one comparison loosens:
the upper-bound check becomes `>` instead of `>=`, and everything else is unchanged. The point I would make
is that the convention lives entirely in two operators, so I would rather state which one I am assuming
than guess — and in a real implementation I would keep a count on each node instead, which sidesteps the
question."

**"Do it without recursion."**
"The inorder method, with an explicit stack — the same go-left-pushing loop from the traversal lesson. Push
nodes as I walk left, pop, compare with the previous value, then move to the right child. That is `O(n)`
time and `O(height)` space in the stack rather than the call stack, and it is immune to the recursion
limit. That matters here more than usual, because a **valid** BST built by inserting sorted data is a
chain — so the deep-tree case is not an adversarial input, it is the most natural one."

**"Two nodes have been swapped. Repair the tree."**
"That is the inorder method with one extra observation. Walk inorder and record every place the sequence
goes **backwards**. There will be either one violation or two. If the two swapped nodes were **adjacent**
in the sorted order, there is exactly one violation and the culprits are that pair. If they were **not
adjacent**, there are exactly two violations, and the culprits are the **first** element of the first
violation and the **second** element of the second. Then swap their values — swapping values rather than
nodes avoids all the pointer surgery. `O(n)` time, `O(height)` space, and it is `O(1)` space if you use
Morris traversal, which is the follow-up to the follow-up."

**"Now find the largest subtree that is a BST."**
"The naive version checks each subtree independently, which recomputes the same work at every level —
`O(n log n)` on a balanced tree and `O(n²)` on a chain. The one-pass version is the same return-value trick
as the diameter problem: each call returns four things — whether this subtree is a BST, its size, its
minimum and its maximum — and the parent combines them. A node forms a BST if both children do **and** the
left subtree's maximum is less than the node, which is less than the right subtree's minimum. I record the
size in an outer variable when it qualifies. One pass, `O(n)`."

### A model answer

Asked: *is this a valid BST — and are you sure your check is correct?*

> "Let me start by ruling out the answer I am *not* going to write, because that is really what the second
> half of your question is about.
>
> The version most people write first checks each node against its two children: left child smaller, right
> child larger, then recurse. That is not the invariant. The invariant is that **all** the values in the
> left subtree are smaller and **all** in the right subtree are larger, and 'all the subtree' is doing the
> work in that sentence.
>
> Here is the tree that separates them. Root 10, with 5 on the left and 15 on the right; and under 15, a
> left child of 6 and a right child of 20. Check every parent-child pair: 5 < 10, 15 > 10, 6 < 15, 20 > 15.
> All fine. And it is **not** a BST, because 6 is in the right subtree of 10 and 6 is less than 10. The
> practical consequence is the part I would emphasise: `search(6)` starts at the root, sees that 6 is less
> than 10, goes left, and never finds a value that is sitting in the tree. So the local check certifies
> precisely the trees whose brokenness is hardest to debug.
>
> The correct formulation is that **every node lives inside an open interval inherited from all of its
> ancestors**. The root's interval is unbounded. Going left tightens the upper bound to the parent's value;
> going right tightens the lower bound. Bounds only ever narrow. So I pass `low` and `high` down and check
> the node against both. In that tree, 6 arrives with a lower bound of 10 — set two levels above it by the
> root — and fails immediately.
>
> Two details I would call out while writing it. I use **`None`** for unbounded rather than `INT_MIN` and
> `INT_MAX`, because node values are allowed to be exactly those, so seeding with them would reject a
> single-node tree containing `-2³¹`. And I use **`<=` and `>=`**, not strict comparisons, because equal
> values violate the invariant under the usual no-duplicates convention — strict comparisons silently
> accept `[2, 2, 2]`.
>
> There is an equivalent second method worth mentioning: walk **inorder** and check that the values
> strictly increase, keeping only the previous value rather than building the list. It works because
> inorder on a BST *is* sorted order, and it has a nice property — it needs no knowledge of the structure
> at all, so anything wrong shows up as the sequence going backwards. It is also the basis for the
> follow-up where two nodes have been swapped: every backwards step is a violation, there are either one or
> two of them, and that tells you exactly which nodes to swap back.
>
> Both are `O(n)` time and `O(height)` space. I would write the range version, because it *is* the
> invariant restated, and I would offer the iterative inorder one if the tree might be a chain — which is
> not exotic here, since a valid BST built from sorted input is exactly that shape."

---

## 9. Recall card

- **The classic wrong answer checks each node against its immediate CHILDREN.** Have the killer input
  ready and produce it unprompted: **`[10, 5, 15, null, null, 6, 20]`** — every parent-child pair passes,
  and 6 sits in the right subtree of 10. Worse than a wrong answer: **`search(6)` cannot find a value that
  is in the tree.**
- **Method one — carry the RANGE down.** Every node lives in an open interval inherited from **all**
  ancestors: going left tightens `high` to the parent's value, going right tightens `low`. **This IS the
  invariant restated**, so writing it explains the definition.
- **Use `None` (or `-inf`) for unbounded, NEVER `INT_MIN`/`INT_MAX`** — node values may equal them, so a
  single node `-2³¹` gets rejected. And use **`<=` / `>=`**, not strict comparisons, or `[2, 2, 2]` passes.
  State the duplicates convention; it lives entirely in one operator.
- **Method two — inorder must STRICTLY increase, keeping only the previous value** (`O(height)` space, not
  `O(n)` for a list). It needs no knowledge of the rules — anything wrong shows up as the sequence going
  backwards — and it is the basis for **LeetCode 99**: every backwards step is a violation, there are
  **one or two**, and you take the **first node of the first** and the **second node of the second**.
- **Both are `O(n)` time and `O(height)` space; the local check is not slower, it is WRONG.** Offer the
  **iterative** inorder version when the tree may be a chain — which is not exotic, since a valid BST built
  from sorted input *is* a chain. And **largest BST subtree** is the day-102 trick again: return
  `(is_bst, size, min, max)` upward for `O(n)` instead of `O(n²)`.
