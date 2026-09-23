---
day: 111
track: dsa
title: "Serialising and deserialising a tree"
phase: "Trees and binary search trees"
status: written
---

# Day 111 · DSA — Serialising and deserialising a tree

**After today you can:** You can turn a tree into a string and back, preserving structure including nulls.

**The interviewer asks it as:** *Serialise this tree, then rebuild it from the string.*

---

## 1. What this is, and why they ask it

**Serialising** means turning a structure in memory into a flat sequence of characters — something you
could send over a network or write to a file. **Deserialising** is rebuilding the original from that
sequence.

Three sentences. [Yesterday](../day-110-trees-from-traversals/README.md) established that one traversal
does not determine a tree, and today is the exception that proves it: **a single traversal *does*
determine a tree if it records where the missing children are.** The whole problem is therefore about
what you write down for "nothing", and getting that right makes the reconstruction a straight walk with
no index arithmetic at all. And there is a second decision — the **delimiter** — which is invisible until
the values are more than one digit long, at which point it silently corrupts everything.

They ask it because it is a design question dressed as an implementation question. There is no clever
algorithm; there are four choices — traversal order, null marker, delimiter, and how you consume the
string on the way back — and a candidate who makes those four choices deliberately, out loud, is doing
exactly what the question is for.

---

## 2. The story

Ponnusamy was eighty-four and his brother's grandson was in Canada and had asked, twice, for the family
tree.

He could not write much any more, so he did it as a voice recording on his phone, and it took him three
attempts across two weeks.

The first attempt was useless and he knew it before he finished. He had gone across: all four of his
grandfather's sons first, then all of their children, then all of theirs. The boy in Canada wrote back
saying he had ninety names and no idea who belonged to whom.

The second attempt went down instead of across, which was better. He named a man, then that man's eldest
son, then that son's eldest, all the way to the bottom, then came back up and did the next one. It felt
right while he was recording it.

It was still wrong, and the reason took him a while to see.

The boy wrote back with the specific problem. He said: you say "Ranganathan, then Muthu, then Selvi, then
Anand" — and I do not know whether Selvi is Muthu's daughter or Ranganathan's second child. I cannot hear
you climbing back up. When you finish a line and go back to do the next one, nothing in your voice tells
me.

So the third attempt had one extra thing in it, and that is the one that worked.

Whenever a man had no more children to name, Ponnusamy said **"no one"** — out loud, deliberately, twice
if there had been two possible places. He felt ridiculous doing it. There were long stretches of the
recording that were just his voice saying "no one, no one" into the phone.

But it meant the boy could follow him. Every time he heard "no one", he knew a line had ended and the old
man was about to climb back up. He could rebuild the whole thing on the first pass, top to bottom, without
ever going back to check anything.

There was one other correction between the second and third attempt, and it was small and it mattered.

In the second recording Ponnusamy had run names together — "Ranganathan Muthu Selvi" — because that is how
people talk. The boy misheard "Ram Kumar" as one name in one place and two names in another. So on the
third attempt the old man paused firmly between every single name, and said so at the start of the
recording: *I am going to stop after each one, so you know where each name ends.*

The recording is eleven minutes long and about a third of it is the word "no one" and the pauses.

---

## 3. The idea in plain English

Ponnusamy's third recording is a preorder serialisation with null markers and a delimiter, and both of
his corrections are the two decisions the problem is really about.

- Going across was **level order**; going down was **preorder**.
- "No one" is the **null marker**, and it is what lets the reader know when to climb back up.
- Pausing between names is the **delimiter**.
- The boy rebuilding it in one pass, without going back, is what makes deserialisation `O(n)` with no index
  arithmetic.

### Why the markers are the whole problem

```
   1               1
    \             /
     2           2

 preorder without markers:   "1,2"    and   "1,2"      IDENTICAL
 preorder with markers:      "1,#,2,#,#"  and  "1,2,#,#,#"    distinct ✓
```

**One traversal plus the nulls determines the tree completely.** That is the exception to
[yesterday's](../day-110-trees-from-traversals/README.md) rule, and it is worth stating explicitly,
because the two facts sound contradictory until you see why: without markers you cannot tell a missing
left child from a missing right one, and the marker is exactly that information.

The count is worth knowing: **a tree with `n` nodes has `n + 1` null positions**, so the serialised form
has `2n + 1` tokens. Every node has two child slots, `n − 1` of them are filled by other nodes, so
`2n − (n − 1) = n + 1` are empty.

### Preorder, and why it makes deserialisation trivial

```python
    def serialise(node):
        if node is None:
            return "#"
        return f"{node.val},{serialise(node.left)},{serialise(node.right)}"
```

```python
    def deserialise(tokens):                # tokens is an ITERATOR
        value = next(tokens)
        if value == "#":
            return None
        node = TreeNode(int(value))
        node.left = deserialise(tokens)
        node.right = deserialise(tokens)
        return node
```

**Six lines each, and no index arithmetic anywhere.** That is the reason to choose preorder.

The mechanism is worth saying precisely: **the reader consumes tokens in exactly the order the writer
produced them**, so an iterator (or a single moving index) is all the bookkeeping required. The recursion
itself remembers where it was — the boy following the recording without notes.

**Use an iterator, not a list with `pop(0)`.** `list.pop(0)` shifts every remaining element, turning an
`O(n)` deserialisation into `O(n²)`. `iter()` plus `next()` is `O(1)` per token.

### The delimiter, which is invisible until it is not

```
 without a delimiter:   "12##2##"
   is that the value 12, or a 1 and a 2?

 with a delimiter:      "12,#,#,2,#,#"
   unambiguous
```

**Any value longer than one character makes this a real bug**, and so does any negative value: `-1`
without a delimiter is indistinguishable from a `-` and a `1`.

Two rules:

- **Pick a delimiter that cannot appear in a value.** A comma is fine for integers. If values were
  arbitrary strings, you would need escaping or a length prefix.
- **Pick a null marker that cannot be a value.** `#` or `null` is safe; `-1` is not, because `-1` might be
  in the tree. **This is the same class of mistake as using `INT_MIN` as a sentinel** on
  [day 108](../day-108-validating-a-bst/README.md).

### Level order: the other correct answer

LeetCode displays trees in level order with nulls, and serialising that way is equally valid.

```
        1
       / \
      2   3
         / \
        4   5

 preorder:     1,2,#,#,3,4,#,#,5,#,#
 level order:  1,2,3,#,#,4,5
```

**Level order is often shorter**, because trailing nulls can be trimmed and because a wide shallow tree
has its nulls clustered at the end. **Preorder is shorter for a deep narrow tree.** Neither dominates.

The trade to state:

```
 PREORDER      recursion, an iterator, six lines each way
               deserialisation needs no queue and no index arithmetic

 LEVEL ORDER   a queue both ways, and the format humans and LeetCode use
               deserialisation must pair each node with its two waiting values
```

**Write preorder; mention that level order is what the platform displays.**

### The BST special case: no markers at all

For a binary search tree you can serialise the preorder **without any nulls** and still rebuild it
uniquely, because the ordering supplies the missing information.

```
 preorder of a BST:  8,5,1,7,10,12        no markers, no delimiter problems
 rebuild: walk the list with a permitted RANGE, exactly as on day 110
```

```
 general tree:  2n + 1 tokens
 BST:           n tokens
 -> roughly HALF the size
```

**That is a real compression and a good answer to "can you make it smaller?"** It is LeetCode 449, and the
reason it works is that a BST's inorder is implied by sorting, so one traversal is already two.

### Making it genuinely compact

If asked for a compact format rather than a readable one:

```
 1. use the BST trick where applicable                    ~50% saving
 2. binary encoding: 4 bytes per int, 1 bit per null      vs ~7 bytes per token as text
 3. structure and values as separate streams              nulls compress extremely well
 4. succinct encoding: 2 bits per node for the shape      2n + o(n) BITS total
```

**Point 4 is the theoretical answer and worth naming**: the number of distinct binary trees with `n` nodes
is the Catalan number, which is about `4ⁿ`, so `2n` bits is information-theoretically necessary and
sufficient for the shape. **You would not implement it**; naming it shows you know where the floor is.

### The design decisions, as a list

This is what the question is actually asking you to do:

```
 1. TRAVERSAL ORDER     preorder (simple recursion) or level order (platform format)
 2. NULL MARKER         a token that cannot be a value — "#", not "-1"
 3. DELIMITER           a character that cannot appear in a value — "," for integers
 4. CONSUMPTION         an iterator or a moving index, NEVER list.pop(0)
 5. VALIDATION          what do you do with malformed input?
```

**Say all five out loud as choices**, with the reason for each. That is the performance.

---

## 4. The picture

The same tree, both formats, with the nulls visible.

```
        1
       / \
      2   3
         / \
        4   5

 PREORDER with markers, read as the recursion runs:

   1  →  2  →  #   #   →  3  →  4  →  #   #   →  5  →  #   #
   │     │     └───┴──┐    │     │     └───┴──┐    │     └───┴──┐
   root  left  2's two    right  left  4's two    right  5's two
               children         children                children

   "1,2,#,#,3,4,#,#,5,#,#"        11 tokens = 2n + 1, with n = 5

 LEVEL ORDER with markers:

   level 0:  1
   level 1:  2  3
   level 2:  #  #  4  5        (2's two missing children, then 3's two)

   "1,2,3,#,#,4,5"             7 tokens after trimming trailing nulls
```

Why the markers are load-bearing:

```
   1                    1
    \                  /
     2                2

 WITHOUT markers
   preorder: 1,2        preorder: 1,2        ← identical, two different trees

 WITH markers
   preorder: 1,#,2,#,#  preorder: 1,2,#,#,#  ← distinct
             ^                      ^
        "no left child"        "a left child follows"

 the marker is EXACTLY the information that distinguishes them.
 A tree of n nodes has n+1 empty slots, so the string has 2n+1 tokens.
```

Deserialisation as a single forward walk — no arithmetic, no going back:

```
 tokens: 1 , 2 , # , # , 3 , 4 , # , # , 5 , # , #
         │
 next() → 1   make node 1
              build 1.left:
 next() → 2     make node 2
                build 2.left:
 next() → #       None                    ← "no one"
                build 2.right:
 next() → #       None                    ← "no one"
                return 2
              build 1.right:
 next() → 3     make node 3
                build 3.left:
 next() → 4       make node 4
 next() → #         None
 next() → #         None
                  return 4
                build 3.right:
 next() → 5       make node 5
 next() → #         None
 next() → #         None
                  return 5
                return 3
              return 1

 the CURSOR only ever moves forward. The recursion remembers the position.
 Ponnusamy's nephew, writing it down on the first pass.
```

The delimiter problem:

```
 tree containing 12 and 2

 WITHOUT a delimiter:  "12##2##"
   read one character at a time: 1, 2, #, #, 2, #, #   -> a THREE-node tree, wrong
   read greedily:                12, #, #, 2, #, #     -> right, but how would
                                                          you know where to stop?

 WITH a delimiter:     "12,#,#,2,#,#"     -> unambiguous

 and negatives make it worse: "-1" without a delimiter is a "-" and a "1".
```

---

## 5. The code, built step by step

### Step 1 — announce the four decisions

"There is no clever algorithm here — there are four choices. Traversal order, the null marker, the
delimiter, and how I consume the string coming back. Let me make each one deliberately."

**That framing is most of the answer.**

### Step 2 — choose preorder, and say why

"Preorder, because the reader can consume the tokens in exactly the order the writer produced them — so
deserialisation is a single forward walk with no index arithmetic. Level order also works and is what the
platform displays, but it needs a queue on both sides."

### Step 3 — the markers, and the count

```python
        if node is None:
            return "#"
```

"Every missing child gets an explicit marker. That is what makes one traversal sufficient — without it, a
node with only a left child and one with only a right child produce the same string. A tree of `n` nodes
has `n + 1` empty slots, so the output is `2n + 1` tokens."

### Step 4 — the delimiter, with the reason

"A comma between every token. It is invisible with single-digit values and it is a real bug the moment a
value has two digits or a minus sign — `12` and `-1` are both unreadable without it."

### Step 5 — an iterator, never `pop(0)`

```python
    tokens = iter(data.split(","))
```

"I deserialise from an iterator. Using a list and `pop(0)` shifts every remaining element on each call,
which turns an `O(n)` reconstruction into `O(n²)` — correct output, and a hundred times slower on a
hundred-thousand-node tree."

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


class Codec:
    """LeetCode 297. Preorder with explicit null markers.

    THE FOUR DECISIONS:
      1. traversal   preorder — the reader consumes tokens in the order the
                     writer produced them, so no index arithmetic is needed
      2. null marker "#" — a token that CANNOT be a value. Not -1.
      3. delimiter   "," — a character that cannot appear in a value
      4. consumption an ITERATOR, never list.pop(0), which is O(n) per call

    A tree of n nodes has n+1 empty child slots, so the output is 2n+1 tokens.
    O(n) time and O(n) space both ways.
    """

    NULL = "#"
    SEP = ","

    def serialise(self, root: TreeNode | None) -> str:
        parts: list[str] = []

        def walk(node: TreeNode | None) -> None:
            if node is None:
                parts.append(self.NULL)     # THE marker — without it, ambiguous
                return
            parts.append(str(node.val))
            walk(node.left)
            walk(node.right)

        walk(root)
        return self.SEP.join(parts)         # join once: O(n), not O(n^2)

    def deserialise(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(self.SEP))     # an ITERATOR, not a list

        def build() -> TreeNode | None:
            value = next(tokens)
            if value == self.NULL:
                return None
            node = TreeNode(int(value))
            node.left = build()             # consumes exactly the left subtree
            node.right = build()
            return node

        return build()


class LevelOrderCodec:
    """The other correct answer, and the format LeetCode displays.

    Needs a QUEUE on both sides. Often shorter for a wide shallow tree
    (trailing nulls can be trimmed); longer for a deep narrow one.
    """

    NULL = "#"
    SEP = ","

    def serialise(self, root: TreeNode | None) -> str:
        if root is None:
            return ""
        parts: list[str] = []
        queue: deque[TreeNode | None] = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                parts.append(self.NULL)
                continue
            parts.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        while parts and parts[-1] == self.NULL:     # trim trailing nulls
            parts.pop()
        return self.SEP.join(parts)

    def deserialise(self, data: str) -> TreeNode | None:
        if not data:
            return None
        values = data.split(self.SEP)
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            if i < len(values) and values[i] != self.NULL:
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] != self.NULL:
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        return root


class BSTCodec:
    """LeetCode 449. A binary SEARCH tree needs NO null markers at all.

    The ordering supplies the missing information: walk the preorder with a
    permitted RANGE and take elements while they fit — exactly the day 108
    validation idea, and the day 110 reconstruction.

    n tokens instead of 2n+1: roughly HALF the size. That is the answer to
    "can you make it more compact?"
    """

    def serialise(self, root: TreeNode | None) -> str:
        parts: list[str] = []

        def walk(node: TreeNode | None) -> None:
            if node is None:
                return                      # NO marker
            parts.append(str(node.val))
            walk(node.left)
            walk(node.right)

        walk(root)
        return ",".join(parts)

    def deserialise(self, data: str) -> TreeNode | None:
        if not data:
            return None
        values = [int(v) for v in data.split(",")]
        index = 0

        def build(low: float, high: float) -> TreeNode | None:
            nonlocal index
            if index >= len(values):
                return None
            value = values[index]
            if not (low < value < high):
                return None                 # belongs to an ancestor's other side
            index += 1
            node = TreeNode(value)
            node.left = build(low, value)
            node.right = build(value, high)
            return node

        return build(float("-inf"), float("inf"))


class IterativeCodec:
    """Preorder serialisation without recursion, for very deep trees.

    A recursive codec on a 10,000-node chain raises RecursionError, and a
    chain is exactly what a BST built from sorted data looks like.
    """

    NULL = "#"

    def serialise(self, root: TreeNode | None) -> str:
        parts: list[str] = []
        stack: list[TreeNode | None] = [root]
        while stack:
            node = stack.pop()
            if node is None:
                parts.append(self.NULL)
                continue
            parts.append(str(node.val))
            stack.append(node.right)        # RIGHT first: a stack reverses
            stack.append(node.left)
        return ",".join(parts)

    def deserialise(self, data: str) -> TreeNode | None:
        tokens = data.split(",")
        if not tokens or tokens[0] == self.NULL:
            return None
        root = TreeNode(int(tokens[0]))
        # stack of (node, which_child_is_next)
        stack: list[list] = [[root, "left"]]
        i = 1
        while stack and i < len(tokens):
            node, side = stack[-1]
            token = tokens[i]
            i += 1
            child = None if token == self.NULL else TreeNode(int(token))
            if side == "left":
                node.left = child
                stack[-1][1] = "right"
            else:
                node.right = child
                stack.pop()
            if child is not None:
                stack.append([child, "left"])
        return root


def serialise_broken_no_markers(node: TreeNode | None) -> str:
    """The trap, written out: no markers, so different trees collide."""
    if node is None:
        return ""
    parts = [str(node.val)]
    left = serialise_broken_no_markers(node.left)
    right = serialise_broken_no_markers(node.right)
    return ",".join(p for p in (parts[0], left, right) if p)


def serialise_slow(node: TreeNode | None) -> str:
    """The other trap: building the string by concatenation.

    Each += copies the whole string, so this is O(n^2) in copying. Collect
    into a list and join ONCE.
    """
    if node is None:
        return "#,"
    return str(node.val) + "," + serialise_slow(node.left) + serialise_slow(node.right)


def count_nodes(node: TreeNode | None) -> int:
    return 0 if node is None else 1 + count_nodes(node.left) + count_nodes(node.right)


def same(a: TreeNode | None, b: TreeNode | None) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


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
    codec = Codec()
    tree = from_list([1, 2, 3, None, None, 4, 5])

    s = codec.serialise(tree)
    print(s)                                # 1,2,#,#,3,4,#,#,5,#,#
    print(len(s.split(",")), 2 * count_nodes(tree) + 1)     # 11 11
    print(same(codec.deserialise(s), tree))                 # True — round trip

    # WHY THE MARKERS MATTER
    left_only = TreeNode(1, TreeNode(2))
    right_only = TreeNode(1, None, TreeNode(2))
    print(codec.serialise(left_only))                       # 1,2,#,#,#
    print(codec.serialise(right_only))                      # 1,#,2,#,#
    print(serialise_broken_no_markers(left_only))           # 1,2
    print(serialise_broken_no_markers(right_only))          # 1,2   <- COLLIDES

    # level order
    lo = LevelOrderCodec()
    print(lo.serialise(tree))                               # 1,2,3,#,#,4,5
    print(same(lo.deserialise(lo.serialise(tree)), tree))   # True

    # the BST version needs no markers and is half the size
    bst = from_list([8, 5, 10, 1, 7, None, 12])
    bc = BSTCodec()
    print(bc.serialise(bst))                                # 8,5,1,7,10,12
    print(codec.serialise(bst))                             # 8,5,1,#,#,7,#,#,10,#,12,#,#
    print(len(bc.serialise(bst).split(",")),
          len(codec.serialise(bst).split(",")))             # 6 13
    print(same(bc.deserialise(bc.serialise(bst)), bst))     # True

    # iterative, for deep trees
    it = IterativeCodec()
    print(same(it.deserialise(it.serialise(tree)), tree))   # True

    chain = None
    for v in range(2000, 0, -1):
        chain = TreeNode(v, None, chain)
    print(len(it.serialise(chain).split(",")))              # 4001 = 2n+1
    print(same(it.deserialise(it.serialise(chain)), chain)) # True

    # edge cases
    print(repr(codec.serialise(None)))                      # '#'
    print(codec.deserialise("#"))                           # None
    print(codec.serialise(TreeNode(-1)))                    # -1,#,#
    print(same(codec.deserialise("-1,#,#"), TreeNode(-1)))  # True

    # negative values and multi-digit values need the delimiter
    tricky = from_list([12, -1, 250])
    print(codec.serialise(tricky))                          # 12,-1,#,#,250,#,#
    print(same(codec.deserialise(codec.serialise(tricky)), tricky))     # True
```

---

## 6. What it costs

### Both directions

```
 serialise    O(n) time — each node visited once
              O(n) space for the output, plus O(height) stack

 deserialise  O(n) time — each token consumed once
              O(n) space for the token list, plus O(height) stack
```

**Both linear, and there is nothing better**: the output must contain every value, so `O(n)` is the floor.

### Size

```
 general tree, preorder with markers:  2n + 1 tokens
 BST, no markers:                      n tokens
```

```
 n = 1,000,000 integers averaging 6 characters plus a comma:
   general:  2,000,001 tokens  ≈  10 MB of text
   BST:      1,000,000 tokens  ≈   7 MB
   binary (4 bytes per int + 1 bit per null):  ~4.3 MB
   succinct (2 bits per node for the shape + values):  ~4 MB
```

**The BST trick roughly halves it**, and that is the practical answer to "make it smaller". The succinct
bound — `2n` bits for the shape — is the theoretical floor, because there are about `4ⁿ` distinct binary
trees with `n` nodes.

### The two `O(n²)` traps

```
 string concatenation instead of join:
   each += copies the whole string so far
   n = 100,000 tokens of ~7 chars  ->  ~35 GB of copying
   with join:                          ~700 KB, once

 list.pop(0) instead of an iterator:
   each pop shifts every remaining element
   n = 100,000 tokens  ->  ~5,000,000,000 element moves
   with an iterator:      100,000
```

**Both are correct and both are catastrophically slow**, and neither raises anything. They are the two
performance bugs this problem is designed to surface.

### Recursion depth

```
 a chain of 10,000 nodes:
   recursive serialise    RecursionError: maximum recursion depth exceeded
   iterative serialise    fine
```

**And a chain is exactly what a BST built from sorted data looks like**, so this is not an exotic input.
The iterative version is in the code above.

### Preorder against level order, by size

```
 shape                    preorder tokens   level-order tokens (trimmed)
 ----------------------   ---------------   ----------------------------
 perfect, n = 7           15                7
 chain of 7 (all right)   15                13
 the example above        11                7
```

**Level order wins on wide shallow trees; preorder wins on deep narrow ones**, and preorder wins on code
simplicity in both cases. Neither dominates, which is why the answer is "either, and here is why I chose
this one".

---

## 7. The traps

### Trap 1 — no null markers

```python
    if node is None:
        return ""
```

```
 serialise(TreeNode(1, TreeNode(2)))        -> "1,2"
 serialise(TreeNode(1, None, TreeNode(2)))  -> "1,2"     <- IDENTICAL
```

Two different trees, one string. **The markers are not padding — they are the information that makes a
single traversal sufficient.**

### Trap 2 — no delimiter

```python
    return f"{node.val}{serialise(node.left)}{serialise(node.right)}"
```

Works perfectly on single-digit values and fails on everything else:

```
 a tree containing 12  ->  "12##"  -> reads as 1, 2, #, #: a two-node tree
 a tree containing -1  ->  "-1##"  -> reads as -, 1, ...
```

**Silent corruption, and it passes every small test.**

### Trap 3 — a null marker that could be a value

```python
    NULL = "-1"
```

The moment the tree contains `-1`, deserialisation stops there and truncates the tree. **Same class of
mistake as `INT_MIN` as a sentinel** on [day 108](../day-108-validating-a-bst/README.md). Use a token that
cannot be parsed as a value at all.

### Trap 4 — `list.pop(0)` when deserialising

```python
    values = data.split(",")
    value = values.pop(0)                   # O(n) per call
```

Correct output, `O(n²)` running time, no error. **Five billion element moves on a hundred thousand
tokens.** Use `iter()` and `next()`, or a `deque`, or an index.

### Trap 5 — string concatenation when serialising

```python
    result += str(node.val) + ","
```

Each `+=` builds a new string. `O(n²)` in copying. **Collect into a list and `join` once.**

### Trap 6 — recursing right before left on the way back

```python
        node.right = build()
        node.left = build()                 # WRONG ORDER
```

The tokens are consumed in the order they were written, so the right call takes the left subtree's tokens.
**A valid-looking tree with everything mirrored, and no error.** Exactly the
[day 110](../day-110-trees-from-traversals/README.md) cursor trap.

### Trap 7 — forgetting the empty tree

```python
    codec.deserialise("")                   # ValueError or StopIteration
```

`serialise(None)` must produce something that `deserialise` accepts. With preorder that is naturally `"#"`,
which round-trips cleanly. With level order you have to decide, and the empty string needs an explicit
check.

### Trap 8 — assuming values are small non-negative integers

Negative numbers, multi-digit numbers, and — if the values were strings — values containing the delimiter
itself. **Say the assumption**: *"I am assuming integer values, so a comma is a safe delimiter. If values
could be arbitrary strings I would need escaping or a length prefix."*

---

## 8. In the interview

### How it gets asked

- The main one: *"Serialise and deserialise a binary tree."* LeetCode 297.
- The BST version: *"Now it is a BST. Can you do better?"* LeetCode 449.
- The size probe: *"How big is your output? Can you make it smaller?"*
- The format probe: *"Why preorder and not level order?"*
- The robustness probe: *"What if the input is malformed?"*

### What to say out loud, in the first ninety seconds

1. **Frame it as design, not algorithm.** "There is no clever algorithm here — there are four decisions:
   the traversal order, the null marker, the delimiter, and how I consume the string coming back. Let me
   make each one deliberately."
2. **State the key fact.** "A single traversal does not determine a tree — but a single traversal **plus
   explicit markers for the missing children** does. That is the whole idea, and the markers are what
   carry the structure."
3. **Choose preorder with the reason.** "Preorder, because the reader consumes tokens in exactly the order
   the writer produced them, so deserialisation is one forward walk with no index arithmetic and no
   queue."
4. **Say the marker constraint.** "The null token has to be something that cannot be a value — `#`, not
   `-1`, because `-1` might be in the tree."
5. **Say the delimiter constraint.** "And a delimiter that cannot appear in a value. That is invisible
   with single digits and it is a real bug the moment there is a two-digit or negative value."
6. **Give the size.** "A tree of `n` nodes has `n + 1` empty child slots, so the output is `2n + 1`
   tokens. Both directions are `O(n)`."

### The follow-ups

**"Why do you need the null markers?"**
"Because without them a single traversal is ambiguous, and I can show the smallest case: a root with only
a left child and a root with only a right child both have preorder `[1, 2]`. Same string, two different
trees. The marker is exactly the information that distinguishes them — it says *which* child is missing,
not just that one is. That is also the resolution of something that sounds contradictory: reconstructing
from traversals needs **two** lists, but serialisation needs only **one**. The difference is the nulls. A
tree with `n` nodes has `n + 1` empty child slots — every node has two, and `n − 1` of them are occupied by
other nodes — so the output is `2n + 1` tokens, and roughly half of them are markers."

**"Why preorder rather than level order?"**
"Mainly because deserialisation becomes trivial. In preorder the reader consumes tokens in exactly the
order the writer produced them, so a single forward iterator is all the state required — the recursion
itself remembers where it is, and there is no index arithmetic and no queue. Level order is equally
correct and it is the format LeetCode displays, but it needs a queue on both sides and the deserialiser
has to pair each dequeued node with the next two tokens. On size neither dominates: level order is shorter
for a wide shallow tree, because trailing nulls can be trimmed, and preorder is shorter for a deep narrow
one. So I would choose preorder for the code and mention that level order is the human-readable format."

**"Now it is a BST. Can you do better?"**
"Yes — for a BST I can drop the markers entirely and serialise just the preorder values, which is `n`
tokens instead of `2n + 1`, so roughly half the size. It works because the ordering supplies the
information the markers were carrying: on the way back I walk the values with a permitted **range**,
exactly like validating a BST. Each value becomes a node only if it falls inside the current range;
otherwise it belongs to some ancestor's other side and I return. Each value is consumed exactly once, so
it is still `O(n)`, with `O(height)` extra space and no marker tokens at all. That is LeetCode 449."

**"How would you make it more compact still?"**
"Three steps, in increasing order of effort. **Binary encoding** instead of text: four bytes per integer
and one bit per null, against roughly seven characters per token as text — that is about a 2.5 times
saving on its own. **Separate the structure from the values** into two streams, because the structure
stream is a bit sequence that compresses extremely well while the values may not. And the theoretical
answer, which I would name rather than implement: a **succinct encoding** uses `2n` bits for the shape,
and that is the information-theoretic floor, because the number of distinct binary trees with `n` nodes is
the Catalan number, which grows like `4ⁿ` — so you need about `2n` bits and no fewer. Knowing where the
floor is tells you when to stop optimising."

**"What are the performance traps here?"**
"Two, and both are silent — correct output, catastrophically slow. **String concatenation** when
serialising: each `+=` copies the entire string built so far, so a hundred thousand tokens is tens of
gigabytes of copying. I collect into a list and `join` once. And **`list.pop(0)`** when deserialising:
each pop shifts every remaining element, so a hundred thousand tokens is around five billion element
moves. I use an iterator with `next()`, which is constant per token. Neither of those raises anything, and
both pass a ten-node test instantly, which is exactly why they are worth calling out before writing the
code."

**"What if the tree is very deep?"**
"Then the recursive version raises `RecursionError` at about a thousand nodes, and this is not an exotic
input — a BST built from sorted data is a chain, which is precisely the shape. The iterative serialiser is
straightforward: a stack, pushing right before left because a stack reverses. The iterative deserialiser
is fiddlier, because you have to remember for each node on the stack whether the next token is its left or
its right child — so the stack holds pairs of node and which-side-is-next. I would write the recursive
version first, say the risk out loud, and offer the iterative one."

### A model answer

Asked: *serialise this tree, then rebuild it from the string.*

> "Let me frame this as what it actually is, which is a design question rather than an algorithm question.
> There is no clever trick — there are **four decisions**: the traversal order, what I write for a missing
> child, the delimiter between tokens, and how I consume the string on the way back. Let me make each one
> deliberately, because that is where all the bugs live.
>
> First, the fact the whole thing rests on. A single traversal does **not** determine a tree — a root with
> only a left child and a root with only a right child both have preorder `[1, 2]`. But a single traversal
> **plus an explicit marker for every missing child** does. The marker is exactly the information that
> distinguishes those two trees, and once it is there, one list is enough. A tree with `n` nodes has
> `n + 1` empty child slots, so the output is `2n + 1` tokens and about half of them are markers.
>
> I will use **preorder**, and the reason is what it does to the reconstruction: the reader consumes tokens
> in exactly the order the writer produced them, so deserialisation is a single forward walk — take a
> token; if it is the marker return nothing; otherwise make a node, build its left subtree, then its right.
> No index arithmetic, no queue, and the recursion itself keeps track of the position. Level order is
> equally valid and is the format the platform displays, but it needs a queue on both sides.
>
> Two constraints on the tokens, and both are invisible until they bite. The **null marker must be
> something that cannot be a value** — I will use `#`, and specifically not `-1`, because `-1` might be in
> the tree and deserialisation would stop dead there. And there must be a **delimiter that cannot appear in
> a value** — a comma is fine for integers. Without one, a tree containing `12` serialises to a string that
> reads back as a `1` and a `2`, and a negative number reads as a minus sign and a digit. That passes every
> single-digit test and corrupts everything else.
>
> Two implementation details I would say while writing. I **collect into a list and join once** rather than
> concatenating, because each `+=` copies the whole string and makes it quadratic. And I deserialise from
> an **iterator**, not a list with `pop(0)`, because each pop shifts every remaining element — five billion
> moves on a hundred-thousand-token string, with no error to tell you.
>
> Both directions are `O(n)` time and `O(n)` space, which is the floor, since the output has to contain
> every value.
>
> And if you tell me it is a **binary search tree**, I can drop the markers entirely and emit just the
> values — `n` tokens instead of `2n + 1`, so about half the size — because the ordering carries the
> structure. On the way back I walk the values with a permitted range and take each one only if it fits,
> which is the same idea as validating a BST."

---

## 9. Recall card

- **It is a DESIGN question with four decisions: traversal order · null marker · delimiter · how you
  consume the string.** Say all four as choices, with reasons — that is the performance.
- **A single traversal does not determine a tree; a single traversal PLUS explicit null markers does.** The
  marker says *which* child is missing, which is exactly what distinguishes `1→left 2` from `1→right 2`.
  **`n` nodes have `n+1` empty slots, so the output is `2n + 1` tokens.**
- **Choose preorder because the reader consumes tokens in the order the writer wrote them** — one forward
  walk, no index arithmetic, no queue. Level order is equally valid and is the platform's display format;
  it is shorter for wide shallow trees and longer for deep narrow ones.
- **The null marker must not be parseable as a value (`#`, never `-1`) and the delimiter must not appear
  in a value.** Without a delimiter, `12` reads back as `1, 2` and `-1` as `-, 1` — silent corruption that
  passes every single-digit test.
- **Two silent `O(n²)` traps: string `+=` instead of `join` (~35 GB of copying at 100k tokens) and
  `list.pop(0)` instead of an iterator (~5 billion element moves).** Both directions are `O(n)`. And **a
  BST needs NO markers — `n` tokens instead of `2n+1`, roughly half** — rebuilt by walking the values with
  a permitted **range**. The theoretical floor is **`2n` bits** for the shape, since there are ~`4ⁿ` binary
  trees.
