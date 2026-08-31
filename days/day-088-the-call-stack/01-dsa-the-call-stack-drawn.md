---
day: 88
track: dsa
title: "The call stack, drawn"
phase: "Recursion and backtracking"
status: written
---

# Day 088 · DSA — The call stack, drawn

**After today you can:** You can trace a recursive call by hand and read a RecursionError correctly.

**The interviewer asks it as:** *Trace this recursion. What is on the stack at the deepest point?*

---

## 1. What this is, and why they ask it

Yesterday you learned not to trace recursion. Today you learn to trace it anyway — because an
interviewer will ask you to, because a bug eventually forces you to, and because understanding what
the machine is actually doing is what turns `RecursionError` from a mystery into a diagnosis.

When a function calls another, the machine has to remember three things about the caller: **its
arguments and local variables**, and **where to resume** when the call returns. That bundle is a
**stack frame**, and the frames pile up in a stack — the same last-in-first-out structure from
[day 068](../day-068-stacks/README.md), except this one is built into the language.

Two ideas do most of the work today. **The recursion tree and the call stack are different things**:
the tree is every call that ever happens, and the stack is only the calls that are live at one instant.
Fibonacci of twenty makes 21,891 calls and never has more than twenty frames on the stack. And **the
depth is the space cost**, which is why a function making a billion calls can be fine and a function
making five thousand can crash.

They ask it because "trace this" is a five-minute question that instantly separates people, because
reading a traceback correctly is a daily skill, and because "convert this recursion to an iteration" —
which is the same question wearing a hat — comes up whenever depth is a problem.

---

## 2. The story

Vasant's workshop is one room off the main road with a shutter that only half opens, and he has been
repairing scooters in it since 1994.

The work never goes in a straight line. A man brings a scooter that will not start. To check the
plug, Vasant has to get the side panel off. To get the side panel off he has to take out two screws
that are behind the footboard, and one of them is rounded, so now he has to find the extractor, and
the extractor is in the box under the bench that has the chain tool sitting on top of it.

So at any moment he is not doing one job. He is in the middle of four.

What he does — and he has done it so long that he does not think of it as a system — is the shelf of
trays. There are nine metal trays on a shelf behind him. When he has to stop what he is doing to do
something else first, everything from the current job goes in a tray: the screws, the washer, the
spanner he was using, all of it. And on the side of the tray he writes one line in chalk. Not what
the job is. **What he was in the middle of when he stopped.** "Second screw, footboard, left." That
line is the whole point of the tray.

Then the tray goes on the shelf and he starts the next thing with clean hands.

When that next thing is finished, he takes the top tray down — always the top one, never one from the
middle — reads the chalk, and carries on from exactly there. He does not re-read the whole job. He
does not work out where he was. The line tells him.

Two things about the shelf. It holds nine trays, and that is a real limit. Twice in thirty years a job
has gone so deep that he ran out of shelf, and both times the answer was to stop, put everything on
the floor in order, and start again more carefully — not to balance a tenth tray on top of the ninth.

And the trays come down in the opposite order to the way they went up. Always. The last thing he set
aside is the first thing he comes back to, and the scooter that started the whole afternoon is the
last tray, at the bottom, with a chalk line on it that says "plug".

---

## 3. The idea in plain English

Each tray is a **stack frame**. The chalk line is the **return address**. The shelf is the **call
stack**. And the nine trays are Python's recursion limit.

### What is in a frame

When a function is called, the machine creates a frame holding:

- **the arguments** it was called with,
- **the local variables** it creates,
- **the return address** — the exact point in the caller to resume at,
- and a link to the frame below it.

```
   +---------------------------+
   | total(numbers, start=2)   |  <- top of stack: the call running right now
   |   locals: start=2         |
   |   return to: line 4 of    |
   |              the frame    |
   |              below        |
   +---------------------------+
   | total(numbers, start=1)   |  <- suspended, mid-addition
   +---------------------------+
   | total(numbers, start=0)   |  <- suspended, mid-addition
   +---------------------------+
   | main()                    |
   +---------------------------+
```

Every frame except the top one is **suspended in the middle of an expression**, waiting for the frame
above it to return a value. That is Vasant's tray with the screws still in it and the chalk line
saying where he stopped.

### Tracing, properly

The method: **draw the stack growing downward, and write what each frame is waiting for.**

`total([4, 7, 2])` where `total` returns `numbers[start] + total(numbers, start + 1)`:

```
 CALL PHASE — frames pile up, each suspended mid-addition

   total(start=0)   waiting on:  4 + ?
   total(start=1)   waiting on:  7 + ?
   total(start=2)   waiting on:  2 + ?
   total(start=3)   base case -> returns 0        <- deepest point: 4 frames

 RETURN PHASE — frames come off in reverse order, each completing its addition

   total(start=3) -> 0
   total(start=2) -> 2 + 0 = 2
   total(start=1) -> 7 + 2 = 9
   total(start=0) -> 4 + 9 = 13
```

**The work happens on the way back up.** On the way down nothing is computed — every call just gets
suspended. That is why a recursion of depth `n` holds `n` frames of memory at its deepest moment, and
why a recursion that does its work on the way *down* and returns nothing useful can sometimes be
rewritten as a loop with no stack at all.

### The recursion tree is not the call stack

This is the idea that answers most interview questions in this area.

The **recursion tree** shows every call that ever happens, laid out over time. The **call stack** shows
only the calls that are alive at one instant — which is a single root-to-current path in that tree.

```
 fib(5) — the TREE has 15 nodes (measured)

                 fib(5)
                /      \
           fib(4)      fib(3)
           /    \      /    \
      fib(3)  fib(2) fib(2) fib(1)
      /   \    ...
   fib(2) fib(1)

 the STACK, at its deepest, holds 5 frames:  fib(5) -> fib(4) -> fib(3) -> fib(2) -> fib(1)
```

```
 fib(20):  21,891 calls  (measured)   but the stack never exceeds 20 frames
```

So:

> **Total calls determine the time. Maximum depth determines the space.**

`fib` is exponential in time and only linear in space, because it finishes the whole left branch —
and pops all those frames — before it starts the right one. Being able to say that sentence is worth
more than any amount of tracing.

### Reading a `RecursionError`

```
  File "shop.py", line 7, in total
    return numbers[start] + total(numbers, start + 1)
  File "shop.py", line 7, in total
    return numbers[start] + total(numbers, start + 1)
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Three things to read out of that.

**In Python, the most recent call is at the bottom.** The traceback reads oldest first, so the line
just above the error is where it actually broke. (C and Java print it the other way round; knowing
which you are looking at saves five minutes.)

**"Previous line repeated 995 more times"** means the same line, which means a genuine recursion rather
than deep mutual calls.

**And it is a limit, not a crash.** Python counts frames and raises at 1,000 — and the depth your own
function actually reaches is a few short of that, measured at **996** from inside a script and **998**
from a bare prompt, because the interpreter and your harness are already using frames. Nothing has
overflowed yet; Python stopped you before it could.

### The limit, and why you must not raise it

```python
    sys.getrecursionlimit()          # 1000
    sys.setrecursionlimit(1_000_000) # do NOT
```

The limit exists so that a runaway recursion produces a catchable Python exception instead of
exhausting the **C stack** underneath, which is a fixed-size block of memory the operating system gave
the thread. Overflow that and the process dies with a segmentation fault: no traceback, no exception,
nothing in the log.

So the limit is a guard rail, and moving the guard rail does not move the cliff. Vasant putting a
tenth tray on top of a shelf that holds nine.

If the depth is genuinely large, **convert to iteration**.

### Converting recursion to iteration

The call stack is a stack, so you can always build your own. The recipe:

1. Make a list to hold the work items — the things that were arguments.
2. Push the initial call.
3. Loop while the list is not empty: pop an item, do the work, and push the sub-calls.

```python
def count_nodes_iterative(root) -> int:
    stack = [root]                   # your own stack instead of the machine's
    count = 0
    while stack:
        node = stack.pop()
        if node is None:
            continue
        count += 1
        stack.append(node.left)
        stack.append(node.right)
    return count
```

Now the depth is limited by memory, not by 1,000 frames.

**The catch, and it is a real one:** this transformation is easy when the work happens *before* the
recursive calls, and genuinely fiddly when it happens *after* — because then you have to remember
"which child am I up to", which is exactly the return address that the machine was storing for you.
That is why an iterative in-order tree traversal is harder than a recursive one, and it is worth
saying rather than claiming the conversion is always mechanical.

### Tail calls, and why Python will not help

A **tail call** is a recursive call whose result is returned directly, with nothing left to do
afterwards:

```python
def total_tail(numbers, start=0, running=0):
    if start == len(numbers):
        return running
    return total_tail(numbers, start + 1, running + numbers[start])   # nothing after it
```

There is nothing waiting in the caller's frame, so in principle the machine could reuse it rather than
stacking a new one — **tail call elimination**, which Scheme and most functional languages do, turning
the recursion into a loop for free.

**Python deliberately does not**, and the reason is the traceback: eliminating frames would mean the
error above could not show you where it came from. Guido van Rossum has written about choosing
debuggability over the optimisation.

So in Python, a tail-recursive function stacks exactly like any other and dies at the same depth. Know
the term, know that it does not help you here, and write the loop.

---

## 4. The picture

`factorial(4)`, drawn as the shelf filling and emptying.

```
 GOING DOWN                                    the shelf, top at the top

 factorial(4)  = 4 * factorial(3)     ->    | factorial(1)  waiting: 1 * ?  |  <- top
 factorial(3)  = 3 * factorial(2)           | factorial(2)  waiting: 2 * ?  |
 factorial(2)  = 2 * factorial(1)           | factorial(3)  waiting: 3 * ?  |
 factorial(1)  = 1  (base case)             | factorial(4)  waiting: 4 * ?  |  <- bottom
                                            +--------------------------------+
                                              deepest point: 4 frames

 COMING BACK UP — always the top tray, never one from the middle

 factorial(1) -> 1
 factorial(2) -> 2 * 1 = 2
 factorial(3) -> 3 * 2 = 6
 factorial(4) -> 4 * 6 = 24
```

What to notice: at the deepest point, **all four frames exist simultaneously**, each holding its own
`n` and each suspended in the middle of a multiplication. That simultaneity is the memory cost.

The tree against the stack, which is the picture to be able to draw:

```
 fib(4)  — TREE: every call that ever happens (9 nodes)

              fib(4)
             /      \
        fib(3)      fib(2)
        /    \      /    \
   fib(2)  fib(1) fib(1) fib(0)
   /    \
 fib(1) fib(0)


 fib(4)  — STACK at four different moments (never more than 4 frames)

   t1              t2              t3              t4
 +--------+      +--------+      +--------+      +--------+
 | fib(1) |      | fib(0) |      | fib(1) |      | fib(2) |
 | fib(2) |      | fib(2) |      | fib(3) |      | fib(4) |
 | fib(3) |      | fib(3) |      | fib(4) |      +--------+
 | fib(4) |      | fib(4) |      +--------+
 +--------+      +--------+

 9 calls over time.  4 frames at once.
 TIME is the tree.  SPACE is the deepest path through it.
```

And the two shapes of recursion, side by side, because the difference decides everything:

```
 LINEAR                            BRANCHING
 one call per frame                two calls per frame

 depth n, total calls n            depth n, total calls ~2^n
 O(n) time, O(n) space             O(2^n) time, O(n) space

 total(), factorial(), length()    fib(), subsets(), permutations()
```

---

## 5. The code, built step by step

### Step 1 — make the stack visible

The fastest way to understand a recursion is to print the depth:

```python
def total(numbers, start=0, depth=0):
    print("  " * depth + f"-> total(start={start})")
    if start == len(numbers):
        print("  " * depth + "<- 0   (base case)")
        return 0
    result = numbers[start] + total(numbers, start + 1, depth + 1)
    print("  " * depth + f"<- {result}")
    return result
```

The indentation *is* the stack depth, and the two arrows are the two phases. This is five minutes of
work and it replaces an hour of confusion — do it once for every new recursive shape you meet.

### Step 2 — inspect the real stack

```python
import inspect

def depth_now() -> int:
    return len(inspect.stack())
```

`inspect.stack()` returns the live frames, so `len` is the current depth. Slow, and useful exactly
once: to confirm that your mental model matches the machine's.

### Step 3 — find the real limit

```python
def deepest() -> int:
    def go(n=0):
        try:
            return go(n + 1)
        except RecursionError:
            return n
    return go()
```

Measured: **996** from inside a script, **998** from a bare prompt — never 1,000, because the
interpreter and whatever called you are already a few frames deep. Worth knowing when you are told
"the limit is 1000" and watch it fail at 996.

### Step 4 — the mechanical conversion

```python
    stack = [initial_work]
    while stack:
        item = stack.pop()
        ...do the work...
        stack.append(sub_item_1)
        stack.append(sub_item_2)
```

Work first, then push. When the work must happen *after* the children — an in-order traversal, or
anything that combines results — you additionally need to record how far through each frame you are,
which is the return address by hand.

### The complete solution

```python
import inspect
import sys


def total(numbers: list[int], start: int = 0) -> int:
    """Linear recursion: one call per frame. depth = n, total calls = n."""
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start + 1)


def total_traced(numbers: list[int], start: int = 0, depth: int = 0) -> int:
    """The same function with the stack made visible.

    The indentation IS the depth. The two arrows are the two phases: nothing is
    computed on the way down, and everything is computed on the way back up.
    """
    print("  " * depth + f"-> total(start={start})")
    if start == len(numbers):
        print("  " * depth + "<- 0  (base case)")
        return 0
    result = numbers[start] + total_traced(numbers, start + 1, depth + 1)
    print("  " * depth + f"<- {result}")
    return result


CALLS = 0
MAX_DEPTH = 0


def fib_counted(n: int, depth: int = 1) -> int:
    """Counts total calls AND maximum depth, to show they are different things.

    Branching recursion: 2 calls per frame. Total calls ~2^n, but the stack
    never exceeds n frames, because the left branch finishes and pops before
    the right one starts.
    """
    global CALLS, MAX_DEPTH
    CALLS += 1
    MAX_DEPTH = max(MAX_DEPTH, depth)
    if n <= 1:
        return n
    return fib_counted(n - 1, depth + 1) + fib_counted(n - 2, depth + 1)


def deepest_reachable() -> int:
    """The real limit, which is a little under sys.getrecursionlimit() because
    the interpreter is already a few frames deep."""
    def go(n: int = 0) -> int:
        try:
            return go(n + 1)
        except RecursionError:
            return n
    return go()


def depth_now() -> int:
    """The live stack depth, straight from the interpreter."""
    return len(inspect.stack())


def total_tail(numbers: list[int], start: int = 0, running: int = 0) -> int:
    """A TAIL-recursive version: nothing happens after the recursive call.

    A language with tail-call elimination would reuse the frame and turn this
    into a loop. Python deliberately does not — it keeps the frames so that
    tracebacks stay readable — so this dies at the same depth as any other
    recursion. Know the term; write the loop.
    """
    if start == len(numbers):
        return running
    return total_tail(numbers, start + 1, running + numbers[start])


def total_iterative(numbers: list[int]) -> int:
    """What tail-call elimination would have produced. O(1) space, no limit."""
    running = 0
    for value in numbers:
        running += value
    return running


class TreeNode:
    __slots__ = ("value", "left", "right")

    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


def count_recursive(node: TreeNode | None) -> int:
    """Work happens AFTER the recursive calls — the hard shape to convert."""
    if node is None:
        return 0
    return 1 + count_recursive(node.left) + count_recursive(node.right)


def count_iterative(node: TreeNode | None) -> int:
    """The mechanical conversion: your own stack instead of the machine's.

    Easy here because the work (counting) does not depend on the children's
    results. When it does — an in-order traversal, or combining returns — you
    also have to record HOW FAR THROUGH each frame you are, which is the return
    address the machine was storing for you.
    """
    stack = [node]
    count = 0
    while stack:
        current = stack.pop()
        if current is None:
            continue
        count += 1
        stack.append(current.left)
        stack.append(current.right)
    return count


def sum_iterative_hard(node: TreeNode | None) -> int:
    """A conversion where the work DOES depend on the children, done with an
    explicit stack of (node, visited) — `visited` is the return address."""
    stack: list[tuple[TreeNode | None, bool]] = [(node, False)]
    total_value = 0
    while stack:
        current, visited = stack.pop()
        if current is None:
            continue
        if visited:                      # children are done; do my work
            total_value += current.value
        else:
            stack.append((current, True))    # come back to me afterwards
            stack.append((current.left, False))
            stack.append((current.right, False))
    return total_value


if __name__ == "__main__":
    total_traced([4, 7, 2])
    # -> total(start=0)
    #   -> total(start=1)
    #     -> total(start=2)
    #       -> total(start=3)
    #       <- 0  (base case)
    #     <- 2
    #   <- 9
    # <- 13

    for n in (5, 10, 20):
        CALLS = MAX_DEPTH = 0
        value = fib_counted(n)
        print(f"fib({n}) = {value}: {CALLS} calls, max depth {MAX_DEPTH}")
    # fib(5) = 5: 15 calls, max depth 5
    # fib(10) = 55: 177 calls, max depth 10
    # fib(20) = 6765: 21891 calls, max depth 20

    print("limit:", sys.getrecursionlimit(), " deepest reachable:", deepest_reachable())
    print("depth at module level:", depth_now())

    print(total_tail([4, 7, 2]), total_iterative([4, 7, 2]))       # 13 13
    try:
        total_tail(list(range(5000)))
    except RecursionError as error:
        print(f"RecursionError: {error}")   # tail recursion does NOT help in Python
    print(total_iterative(list(range(5000))))                      # 12497500

    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(count_recursive(root), count_iterative(root))            # 5 5
    print(sum_iterative_hard(root))                                # 15

    # a deep tree that recursion cannot handle, and iteration can
    deep = TreeNode(1)
    node = deep
    for _ in range(5000):
        node.left = TreeNode(1)
        node = node.left
    try:
        count_recursive(deep)
    except RecursionError as error:
        print(f"RecursionError: {error}")
    print("iterative count on the same tree:", count_iterative(deep))   # 5001
```

---

## 6. What it costs

### Frames, and what a frame costs

```
 measured: about 830 KB of Python-level allocation for 20,000 frames
           -> roughly 40 bytes each of traced Python objects
 plus:     a slice of the thread's C stack per call, which is the thing the
           recursion limit actually protects
```

The Python-object part is small. The C stack is the binding constraint, and it is a **fixed-size block
the operating system gave the thread** — typically 8 MB on Linux for the main thread. That is why the
limit is a count of frames rather than a measure of memory: Python cannot easily know how much C stack
each frame consumed, so it counts conservatively.

### The two complexities, kept apart

```
 total(n)      calls: n         depth: n        O(n) time,     O(n) space
 factorial(n)  calls: n         depth: n        O(n) time,     O(n) space
 binary search calls: log n     depth: log n    O(log n) time, O(log n) space
 fib(n)        calls: ~2^n      depth: n        O(2^n) time,   O(n) space
```

Measured, so the last line is not hand-waving:

```
 fib(5)   =    5 :     15 calls, max depth  5
 fib(10)  =   55 :    177 calls, max depth 10
 fib(20)  = 6765 : 21,891 calls, max depth 20
```

**Twenty-one thousand calls, twenty frames.** Time is the whole tree; space is the deepest path
through it. This is the single most useful distinction in the lesson.

### The limit, exactly

```
 sys.getrecursionlimit()   ->  1000
 deepest reachable         ->  996     (measured in a script; 998 from a bare prompt)
```

```
 linear recursion on a list of 5,000     ->  RecursionError
 log-depth recursion on 1,000,000 items  ->  20 frames
```

**A recursion whose depth is the input size fails on inputs that are not large.** Five thousand
elements is nothing. That is the practical rule this lesson exists to establish.

### Recursion against iteration, priced

```
                    recursive             iterative
 sum a list         O(n) space, dies      O(1) space, no limit
                    at ~1000
 tree traversal     O(height) space       O(height) space with your own stack
                    dies on a degenerate  works to memory
                    tree of depth 1000
 binary search      O(log n) = 20 frames  O(1)  — the difference is irrelevant
```

The middle row is the one that matters in practice. A balanced tree of a million nodes has a height of
about twenty and recursion is completely safe. A **degenerate** tree — one where every node has a
single child, which is what an unbalanced binary search tree becomes when you insert sorted data — has
a height of a million, and recursion dies. Same code, same tree class, different data.

### The conversion's cost

```
 recursion:            frames managed by the machine, ~40 B of Python objects each
 explicit stack:       a Python list of your work items, ~8 B per entry plus the item
```

The explicit version is usually *cheaper* in memory as well as unlimited in depth — because your work
items are smaller than full frames. What it costs is clarity: an in-order traversal is four lines
recursively and about twelve with an explicit stack and a `visited` flag.

---

## 7. The traps

### Trap 1 — confusing total calls with depth

Saying "`fib(30)` will blow the stack" because it makes 2.7 million calls. It will not — the depth is
30. It will take a tenth of a second and finish. Conversely, `total` on a five-thousand-element list
makes only five thousand calls and *does* blow the stack, because they are all alive at once.

**Time is the tree. Space is the deepest path.** Getting these two backwards is the most common
misunderstanding in this area.

### Trap 2 — reading the traceback from the wrong end

In Python the **most recent call is last**. The line immediately above the error message is where it
broke. In C, Java and most debuggers it is the other way round. Reading a Python traceback top-down and
concluding the bug is in `main` costs five minutes every time.

### Trap 3 — raising the recursion limit

```python
    sys.setrecursionlimit(1_000_000)
```

Converts a clean, catchable `RecursionError` into a segmentation fault when the C stack runs out:

```
Segmentation fault (core dumped)
```

No traceback, no exception, nothing in the log, and in a server it takes the whole process down
including every other request in flight. The limit is a guard rail; moving it does not move the cliff.

### Trap 4 — assuming tail recursion helps in Python

```python
    return total_tail(numbers, start + 1, running + numbers[start])
```

There is nothing after the call, so a language with tail-call elimination would reuse the frame. Python
does not, by an explicit design decision to keep tracebacks complete. This function dies at exactly the
same depth as the non-tail version. Know the term; do not rely on it.

### Trap 5 — recursion on a degenerate structure

A balanced tree of a million nodes has height ~20; recursion is safe. Insert a million *sorted* values
into an unbalanced binary search tree and the height is a million:

```
RecursionError: maximum recursion depth exceeded
```

Same code, same class, different data. **The depth is a property of the input, not of the algorithm**,
and that is why "it worked in testing" is such a common preface to this bug.

### Trap 6 — a mutable default in a traced helper

```python
def walk(node, path=[]):                 # created ONCE at definition time
```

The list is shared across every top-level call, so the second call sees the first one's path. Use
`None` and create it inside. This bites hardest here because path-tracking helpers are exactly the
things people add while debugging a recursion.

### Trap 7 — printing inside a hot recursion

Adding a `print` to `fib(30)` turns a tenth of a second into minutes and produces 2.7 million lines.
Trace on the smallest input that shows the shape — `fib(5)` — and read fifteen lines instead.

### Trap 8 — thinking the conversion to iteration is always mechanical

It is easy when the work happens *before* the recursive calls. When the work happens *after* — an
in-order traversal, combining children's return values — you must record how far through each frame you
are, which means pushing `(node, visited)` pairs and handling each twice. That is the return address,
by hand, and it is why the iterative version is three times the length.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Trace this function. What is on the stack when it is deepest?"*
- The distinction: *"How many calls does `fib(20)` make, and how much stack does it use?"*
- The diagnosis: *"Here is a `RecursionError`. What went wrong and how would you fix it?"*
- The conversion: *"Rewrite this recursion iteratively."*
- The sneaky one: *"This works in tests and crashes in production on the same code path. Why?"* — a
  degenerate structure.

### What to say out loud, in the first ninety seconds

1. **Say what a frame holds.** "Each call gets a frame with its arguments, its locals, and where to
   resume in the caller. They pile up and come off in reverse order."
2. **Separate the two costs immediately.** "Total calls determine the time; maximum depth determines the
   space. Those are different numbers — `fib(20)` makes about twenty-two thousand calls and never
   exceeds twenty frames."
3. **When tracing, draw and narrate the two phases.** "Going down, every frame is suspended in the
   middle of an expression. Coming back up is where all the arithmetic happens."
4. **Give the limit as a real number.** "Python's limit is a thousand frames — about 996 reachable in
   practice — so a recursion whose depth is the input size fails on a five-thousand-element list."
5. **Offer the conversion, and be honest about it.** "If the depth is a problem I would use my own
   stack. That is mechanical when the work happens before the recursive calls, and genuinely fiddlier
   when it happens after."

### The follow-ups

**"How many calls does `fib(20)` make, and how deep does the stack go?"**
"About twenty-two thousand calls — 21,891 exactly — and the stack never exceeds twenty frames. Those
are two different questions and the answers diverge enormously. The tree of calls is everything that
ever happens, which is what determines the time. The stack is only the calls alive at one instant,
which is a single path from the root to wherever you are, and that determines the space. `fib` finishes
its entire left branch and pops all those frames before it starts the right one, so it is exponential
in time and only linear in space."

**"What is on the stack at the deepest point?"**
"For a linear recursion like summing a list, the deepest point is one frame per element plus the base
case, and every frame except the top is suspended in the middle of an addition, waiting for the value
from above. Concretely, for a three-element list: the base-case call, plus three frames each holding
its own index and each about to add its element to whatever comes back. That simultaneity is the memory
cost — they all exist at once."

**"I got a `RecursionError`. What do I do?"**
"First, read it correctly: in Python the most recent call is *last*, so the line just above the message
is where it broke, and 'previous line repeated N times' tells me it is genuine recursion rather than
deep mutual calls. Then it is one of three things. A missing or unreachable base case, which is a bug —
fix that. Or genuinely deep data, like a degenerate tree, in which case I convert to an explicit stack.
Or the input is just large and the algorithm is linear-depth, which means the algorithm is wrong for
the input. What I would *not* do is raise the recursion limit — that converts a catchable exception
into a segmentation fault when the C stack runs out, which kills the process with no traceback."

**"Rewrite this recursively-defined traversal as a loop."**
"The call stack is a stack, so I build my own: a list of work items, push the initial call, then loop
popping items, doing the work and pushing the sub-calls. That is mechanical when the work happens
before the recursive calls. When it happens after — combining the children's results — I also have to
record how far through each frame I am, which means pushing `(node, visited)` pairs and handling each
node twice: once to schedule its children, once to do its own work. That flag is the return address the
machine was storing for me, and it is why the iterative version is about three times the length."

**"Does making it tail-recursive help?"**
"Not in Python. A tail call is one where nothing happens after the recursive call returns, so in
principle the frame could be reused — Scheme and most functional languages do that and turn the
recursion into a loop for free. Python deliberately does not, because eliminating frames would make
tracebacks incomplete, and that was an explicit trade in favour of debuggability. So a tail-recursive
function in Python dies at exactly the same depth. I would know the term and write the loop."

**"It works in tests and crashes in production on the same code path."**
"That is usually a degenerate structure. A balanced binary tree of a million nodes has a height of about
twenty and recursion is completely safe; the same tree class fed a million *sorted* insertions has a
height of a million and dies immediately. The depth is a property of the *input*, not of the algorithm,
which is why the test data hid it. Same story for a linked list built from user data, or a deeply
nested JSON document from an external source. If the depth can be attacker-controlled, that is a
denial-of-service vector and iteration is the fix rather than a bigger limit."

### A model answer

Asked: *trace this recursion. What is on the stack at the deepest point?*

> "Let me set up the vocabulary first, because it makes the trace short. Every call gets a stack frame
> holding three things: the arguments it was called with, its local variables, and the return address —
> the exact place in the caller to resume. The frames pile up and come off in the opposite order,
> always the top one.
>
> So for summing `[4, 7, 2]` with `total(numbers, start)`:
>
> Going down, four frames are created. `start=0` computes nothing — it evaluates `numbers[0]`, which
> is 4, and then suspends in the middle of the addition waiting for the recursive call. Same for
> `start=1` waiting on `7 + ?`, and `start=2` waiting on `2 + ?`. Then `start=3` hits the base case and
> returns 0 without calling anything.
>
> That is the deepest point: four frames alive simultaneously, three of them suspended mid-addition,
> each holding its own `start`. Their simultaneity is the memory cost — that is what O(n) space means
> here.
>
> Coming back up, each frame completes its addition and pops: 0, then 2, then 9, then 13. **All the
> arithmetic happens on the way back up.** Nothing was computed on the way down.
>
> The distinction I would want to make explicit, because it answers most questions in this area: the
> recursion *tree* and the call *stack* are different things. The tree is every call that ever happens
> and it determines the time. The stack is only the calls alive at one instant — a single path from the
> root — and it determines the space. `fib(20)` makes 21,891 calls and never has more than twenty
> frames, because it finishes the left branch and pops all of it before starting the right. Exponential
> in time, linear in space.
>
> On the practical side: Python's limit is a thousand frames, and about 996 are actually reachable
> from inside a script, because the interpreter and the caller are already a few frames deep. So a linear-depth recursion fails on a
> five-thousand-element list — which is not a large list. That limit exists to turn a C-stack overflow
> into a catchable Python exception, so raising it does not help; it just turns a `RecursionError` into
> a segmentation fault with no traceback.
>
> If I needed the depth, I would convert to an explicit stack — the call stack is a stack, so that
> transformation always exists. It is mechanical when the work happens before the recursive calls, and
> genuinely fiddlier when it happens after, because then I have to store how far through each frame I
> am, which is the return address the machine was keeping for me."

---

## 9. Recall card

- **A stack frame holds the arguments, the locals, and the return address** — where to resume in the
  caller. Frames pile up and come off in **reverse order**, and every frame except the top is
  **suspended mid-expression**. **All the work happens on the way back up**; nothing is computed on the
  way down.
- **The recursion TREE and the call STACK are different things, and this answers most questions here.**
  *Total calls determine the time; maximum depth determines the space.* Measured: **`fib(20)` = 21,891
  calls, max depth 20** — exponential in time, **linear** in space, because the left branch pops before
  the right one starts.
- **To trace, draw the stack downward and write what each frame is waiting for**, then read the two
  phases. The five-minute tool: add a `depth` parameter and indent the prints — the indentation *is*
  the depth. Trace the **smallest** input that shows the shape.
- **Python's limit is 1000 frames, ~996 reachable from a script, so a linear-depth recursion dies on a
  5,000-element list.** Read the traceback from the **bottom** (most recent call last). **Never raise
  the limit** — it exists to turn a C-stack overflow into a catchable exception, so raising it gives a
  **segmentation fault** with no traceback. **Tail recursion does not help in Python**, deliberately,
  to keep tracebacks complete.
- **The conversion to iteration always exists — build your own stack — but it is only mechanical when
  the work happens BEFORE the recursive calls.** When it happens after, you must push `(item, visited)`
  pairs and handle each item twice; that flag *is* the return address by hand. And watch for
  **degenerate structures**: a balanced tree of 10⁶ nodes has height ~20, the same class fed sorted
  insertions has height 10⁶ — **the depth is a property of the input, not the algorithm.**
