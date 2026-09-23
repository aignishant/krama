---
day: 94
track: dsa
title: "Backtracking: the undo step"
phase: "Recursion and backtracking"
status: written
---

# Day 094 · DSA — Backtracking: the undo step

**After today you can:** You can add, recurse, and remove, and say why the removal is the whole pattern.

**The interviewer asks it as:** *Why did you pop that element after the recursive call?*

---

## 1. What this is, and why they ask it

**Backtracking** is depth-first search over a tree of choices, where you make a choice, explore
everything that follows from it, and then **put the state back exactly as it was** before making the
next choice.

You have written the pattern three times already — [subsets](../day-091-subsets/README.md),
[permutations](../day-092-permutations/README.md),
[combination sum](../day-093-combinations/README.md) — and each time the un-choose was one line at the
bottom of the loop. Today is about that line on its own, because it is the line the interviewer asks
about, and because every remaining problem in this phase has *more state to undo* than a single list.

The three sentences that matter. **Anything you change before the recursive call must be changed back
after it.** That includes the partial answer, the availability marks, and every derived counter you are
keeping. And the alternative — passing a fresh copy down instead of mutating and restoring — is correct
too, costs `O(depth)` extra allocation per node, and is worth knowing so that you can say why you did
not choose it.

They ask *"why did you pop that element?"* because the answer separates two kinds of candidate. One
says "to clean up". The other says "because `current` is a single object shared by every branch of the
tree, and the pop is what makes it correct for the next branch — without it the sibling branch inherits
a choice it never made." Only the second person has understood what they wrote.

---

## 2. The story

Meena decided on a Sunday morning that the hall was wrong and had been wrong for four years.

There were three big things in it — the sofa, the low wooden table, and the corner shelf with the
television on it — and four places they could sensibly go: the wall with the window, the wall by the
kitchen door, the long blank wall, and the corner near the passage.

Her plan was to try every way round, properly, and then pick.

She started with the sofa on the window wall. Then, with the sofa there, she tried the table by the
kitchen door, and with those two settled she put the shelf on the long wall and stood at the doorway
and looked. Too dark. She moved the shelf to the corner instead and looked again. Better, but the
television faced the window and you would see nothing in the afternoon.

Then she wanted to try the table somewhere else. And this is the part she had learned from doing it
badly the year before.

Before she moved the table, she carried the shelf back to where it had been standing when she started.
Not roughly. Exactly. Because if she left the shelf in the corner and then moved the table, she would
be looking at an arrangement that was half of one idea and half of another, and she would have no way
of telling which of the two changes had made it worse.

She did the same with the sofa. When she had finished every arrangement with the sofa on the window
wall, she put the table and the shelf back where they had been at the start, and only then moved the
sofa to the kitchen wall.

Her husband came in at about eleven, saw the sofa in a new place and the room otherwise untouched, and
asked whether she had actually done anything.

She said she had done nine of them so far, and that the room looking normal in between was the only
reason she could tell one from another.

By two o'clock she had been through all of them. The room, at that moment, looked exactly as it had at
nine in the morning. Then she put the sofa on the long wall, the table in front of it, the shelf in the
corner, and stopped.

---

## 3. The idea in plain English

Meena has just run a backtracking search, and the thing she learned the hard way is the whole lesson.

- Each big piece of furniture is a **level** of the recursion. The sofa is decided first, then the
  table, then the shelf.
- Putting a piece somewhere is the **choose** step.
- Trying everything that follows from that placement is the **recurse** step.
- **Carrying it back to exactly where it was is the un-choose step**, and her reason is precisely the
  technical reason: without it, the next branch starts from a state that no branch actually chose.

### The template, and it never changes

```python
    def explore(state):
        if is_complete(state):
            record(copy_of(state))
            return
        for choice in options(state):
            if not is_valid(choice, state):
                continue                    # prune
            apply(choice, state)            # choose
            explore(state)                  # recurse
            undo(choice, state)             # un-choose
```

Seven lines. **Every problem for the rest of this phase is this template with different `options`,
`is_valid` and `apply`.** N-Queens, Sudoku, word search, palindrome partitioning — all of them.

### What counts as "state"

This is the part people get wrong once they move past subsets, because in subsets there was only one
thing to undo.

**State is anything the recursion can see that you changed.** It comes in three kinds:

1. **The partial answer.** The working list — `current`. Undone with `pop()`.
2. **Availability marks.** `used[i] = True`, `visited[row][col] = True`, `board[r][c] = digit`. Undone
   by setting them back.
3. **Derived bookkeeping.** A running sum, a set of occupied columns, a count of remaining blanks.
   Undone by subtracting, discarding, incrementing.

The third kind is where the bugs live, because it does not look like state. If you write
`running_total += value` before the call, you owe a `running_total -= value` after it — unless you
passed it as an argument instead, which is the trick below.

**The rule, in one sentence: for every line before the recursive call that changes something the
recursion can see, there is a line after it that changes it back.** Count them. They should match.

### Two styles, and why the mutating one wins

**Style A — mutate and undo.** One shared object, restored after every branch.

```python
        current.append(x)
        explore(...)
        current.pop()
```

**Style B — pass a fresh copy.** Nothing is shared, so nothing needs undoing.

```python
        explore(current + [x])              # a NEW list; the caller's is untouched
```

Style B is shorter and cannot be got wrong. It also allocates a new list of length up to `k` at
**every node of the tree**, not every leaf. For subsets at n = 20 that is two million allocations
averaging ten elements each — twenty million element copies that style A does not do.

**Write style A in an interview, and say that style B exists.** The sentence to have ready: *"I mutate
one working list and undo, because copying at every node would multiply the work by the depth. The
copy-based version is easier to get right and I would use it if the state were small or if I needed the
partial answers to be immutable."*

Note the exception that makes style B free: **immutable values need no undo.** If you pass an integer,
a string, or a tuple, the callee physically cannot change yours.

```python
        explore(index + 1, remaining - value)       # nothing to undo: ints are values
        explore(prefix + character)                 # nothing to undo: strings are immutable
```

That is why `combination_sum` never undoes `remaining` — it was passed as an argument, not mutated in
place. **Passing by argument *is* the undo.** Recognising which pieces of state you can move into the
argument list is the single best way to reduce the number of things you can forget.

### What makes it "backtracking" rather than "enumeration"

One line: **`if not is_valid(...): continue`**.

Subsets and permutations walk the whole tree — every leaf is an answer, nothing is rejected. That is
**enumeration**. Backtracking proper adds a check *before* recursing, so branches that cannot lead to a
valid answer are never walked at all. That check is called **pruning**, and it is where all the speed
comes from.

```
 N-Queens, n = 8:
   all placements, no check:  8^8 = 16,777,216 leaves
   one queen per row:         8! =      40,320
   with the column/diagonal check while descending:  2,057 nodes visited
```

**Sixteen million down to two thousand, from one `if`.** The check has to happen *before* the recursive
call — checking at the leaf gives you the 40,320, checking on the way down gives you the 2,057.

### Where the undo goes, exactly

Immediately after the recursive call, inside the loop, before the next iteration.

```python
        for choice in options:
            apply(choice)
            explore()
            undo(choice)                    # <- here. Not after the loop, not at the top.
```

Putting it after the loop undoes only the last choice. Putting a "reset everything" at the top of the
function is worse: it works, hides the pairing, and quietly costs `O(state)` per node.

---

## 4. The picture

The state of `current` through a small search, with the undo marked. This is the diagram to be able to
draw from memory.

```
 subsets of [1, 2, 3], template form

 depth  action              current      result
 -----  ------------------  -----------  ---------------------------
   0    record              []           [[]]
   0    choose 1            [1]
   1      record            [1]          [[], [1]]
   1      choose 2          [1,2]
   2        record          [1,2]        [[], [1], [1,2]]
   2        choose 3        [1,2,3]
   3          record        [1,2,3]      [[], [1], [1,2], [1,2,3]]
   2        UNDO 3          [1,2]                                    <-- back to depth 2's state
   1      UNDO 2            [1]                                      <-- back to depth 1's state
   1      choose 3          [1,3]
   ...

 Notice: after every UNDO, `current` is EXACTLY what it was when that
 level started. That is the invariant, and it is the only one.
```

The invariant, stated properly:

```
 +---------------------------------------------------------------+
 |  When explore() returns, every piece of shared state is        |
 |  byte-for-byte what it was when explore() was called.          |
 +---------------------------------------------------------------+

 If that holds at every level, the tree is correct.
 If it fails at ONE node, every sibling after it is wrong.
```

What the failure looks like, drawn:

```
 permutations of [1,2,3] with `used[i] = False` forgotten

           build()            used = [F,F,F]
             |
          take 1              used = [T,F,F]
             |
          take 2              used = [T,T,F]
             |
          take 3              used = [T,T,T]   -> record [1,2,3]
             |
          return              used = [T,T,T]   <-- NOT restored
             |
      try to take 3 here      used[2] is True  -> skipped
             |
      nothing available       -> branch dies with no answer

 One missing line, and 5 of the 6 answers vanish. No error is raised.
```

And the two styles, side by side:

```
 style A: mutate + undo                style B: pass a copy
 ---------------------------           ---------------------------
 current.append(x)                     explore(current + [x])
 explore()
 current.pop()

 one list, reused                      one new list per NODE
 O(1) per node                         O(len(current)) per node
 O(depth) total memory                 O(depth^2) live at once
 must not forget the undo              cannot be got wrong
```

---

## 5. The code, built step by step

### Step 1 — write the three lines as one unit, always

```python
        apply(choice)
        explore(...)
        undo(choice)
```

Type all three before you type anything inside them. It is a physical habit, and it is the reason
experienced people do not forget the undo: they never wrote the two-line version in the first place.

### Step 2 — count your chooses and your undoes

Before running anything, look at the block and count. Two lines that change shared state before the
call means two lines after it.

```python
        used[i] = True              # change 1
        current.append(items[i])    # change 2
        build()
        current.pop()               # undo 2
        used[i] = False             # undo 1
```

**Undo in reverse order.** It does not matter for independent state, and it matters enormously for
anything stacked — and doing it in reverse always is one less thing to think about.

### Step 3 — move what you can into the arguments

```python
        build(i + 1, remaining - candidates[i])       # nothing to undo
```

versus

```python
        self.remaining -= candidates[i]              # needs an undo
        build(i + 1)
        self.remaining += candidates[i]
```

Both correct. The first cannot be got wrong. **Every piece of state you can pass as a value is a piece
of state you cannot forget to restore**, and it costs nothing when the value is an integer or a string.

### Step 4 — the validity check goes *before* the apply

```python
        for choice in options:
            if not is_valid(choice):
                continue                    # prune: never walked at all
            apply(choice)
            explore()
            undo(choice)
```

Not inside `explore`, and not at the leaf. Checking on the way down is what takes N-Queens from
forty thousand leaves to two thousand nodes.

### Step 5 — the early-return trap

Search problems return `True` the moment they find an answer, and that `return` skips the undo:

```python
            apply(choice)
            if explore():
                return True                 # <- the undo below never runs
            undo(choice)
```

**This is correct if you are unwinding all the way out and never touching the state again**, which is
the usual case for "does a solution exist". It is a bug if the caller inspects the state afterwards, or
if the same board is reused for a second query. When in doubt, undo before returning:

```python
            apply(choice)
            found = explore()
            undo(choice)
            if found:
                return True
```

Two extra lines, and it removes an entire class of "works the first time, fails the second time" bugs.

### The complete solution

A generic template plus the three problems you already know, all written against it, so you can see
that they are the same code.

```python
from typing import Any, Callable, Iterable


def backtrack(
    is_complete: Callable[[Any], bool],
    record: Callable[[Any], None],
    options: Callable[[Any], Iterable[Any]],
    is_valid: Callable[[Any, Any], bool],
    apply: Callable[[Any, Any], None],
    undo: Callable[[Any, Any], None],
    state: Any,
) -> None:
    """The seven-line pattern, written once.

    You would not literally use this in an interview — you would inline it —
    but writing it out once makes the shape impossible to forget.
    """
    if is_complete(state):
        record(state)
        return
    for choice in options(state):
        if not is_valid(choice, state):
            continue                        # PRUNE — the branch is never walked
        apply(choice, state)                # CHOOSE
        backtrack(is_complete, record, options, is_valid, apply, undo, state)
        undo(choice, state)                 # UN-CHOOSE


def subsets(items: list[int]) -> list[list[int]]:
    """One kind of state: the partial answer. One undo."""
    result: list[list[int]] = []
    current: list[int] = []

    def explore(start: int) -> None:
        result.append(current[:])           # every node is an answer
        for i in range(start, len(items)):
            current.append(items[i])        # choose
            explore(i + 1)                  # recurse
            current.pop()                   # un-choose

    explore(0)
    return result


def permutations(items: list[int]) -> list[list[int]]:
    """Two kinds of state: the partial answer AND the availability marks.
    Two chooses, two undoes, undone in reverse order."""
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def explore() -> None:
        if len(current) == len(items):
            result.append(current[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue                    # prune: already placed
            used[i] = True                  # choose 1
            current.append(items[i])        # choose 2
            explore()
            current.pop()                   # undo 2
            used[i] = False                 # undo 1

    explore()
    return result


def path_exists(grid: list[list[int]], target: tuple[int, int]) -> bool:
    """Three kinds of state, and the early-return trap made safe.

    The `visited` grid is marked on the way in and cleared on the way out, so
    a cell blocked on one path is free on another. Forget the clear and you
    are computing "is there a path that never revisits a cell ACROSS ALL
    ATTEMPTS", which is not a question anybody asked.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def explore(r: int, c: int) -> bool:
        if (r, c) == target:
            return True
        visited[r][c] = True                                # choose
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue                                    # prune: off the grid
            if visited[nr][nc] or grid[nr][nc] == 1:
                continue                                    # prune: seen, or a wall
            if explore(nr, nc):
                visited[r][c] = False                       # undo BEFORE returning
                return True
        visited[r][c] = False                               # un-choose
        return False

    return explore(0, 0)


def subsets_by_copy(items: list[int]) -> list[list[int]]:
    """Style B: pass a fresh list down, so there is nothing to undo.

    Correct, shorter, and impossible to get wrong. It also allocates a new
    list at EVERY NODE — 2^n of them for subsets — where style A allocates
    only at the leaves. Know it; usually do not write it.
    """
    result: list[list[int]] = []

    def explore(start: int, current: list[int]) -> None:
        result.append(current)              # already a private list; no copy needed
        for i in range(start, len(items)):
            explore(i + 1, current + [items[i]])    # a NEW list each time

    explore(0, [])
    return result


def permutations_broken(items: list[int]) -> list[list[int]]:
    """The failure, written out so you can run it: one missing undo."""
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def explore() -> None:
        if len(current) == len(items):
            result.append(current[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            used[i] = True
            current.append(items[i])
            explore()
            current.pop()
            # missing: used[i] = False

    explore()
    return result


def count_nodes_with_and_without_pruning(n: int) -> tuple[int, int]:
    """N-Queens, counted both ways, so the number is yours and not a claim.

    Without pruning: place a queen in every row, check only at the bottom.
    With pruning:    reject a column or diagonal clash before descending.
    """
    without = 0
    with_prune = 0

    def blind(row: int, cols: list[int]) -> None:
        nonlocal without
        without += 1
        if row == n:
            return
        for c in range(n):
            cols.append(c)
            blind(row + 1, cols)
            cols.pop()

    def pruned(row: int, cols: set[int], diag: set[int], anti: set[int]) -> None:
        nonlocal with_prune
        with_prune += 1
        if row == n:
            return
        for c in range(n):
            if c in cols or (row - c) in diag or (row + c) in anti:
                continue                    # THE line that does all the work
            cols.add(c); diag.add(row - c); anti.add(row + c)
            pruned(row + 1, cols, diag, anti)
            cols.remove(c); diag.remove(row - c); anti.remove(row + c)

    blind(0, [])
    pruned(0, set(), set(), set())
    return without, with_prune


if __name__ == "__main__":
    print(len(subsets([1, 2, 3])), len(subsets_by_copy([1, 2, 3])))       # 8 8

    print(permutations([1, 2, 3]))
    # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    print(permutations_broken([1, 2, 3]))
    # [[1, 2, 3]]        <- one missing line, five answers gone, no error

    maze = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    print(path_exists(maze, (3, 3)))                                      # True

    print(count_nodes_with_and_without_pruning(6))
    # (55987, 543)   <- the whole argument for checking on the way down
    print(count_nodes_with_and_without_pruning(8))
    # (19173961, 2057)
```

---

## 6. What it costs

### The undo itself

```
 current.pop()          O(1)
 used[i] = False        O(1)
 cols.remove(c)         O(1)   — set removal
 board[r][c] = "."      O(1)
```

**Every undo in this phase is O(1).** That is not a coincidence — it is a design requirement. If your
undo is `O(k)`, you have chosen the wrong representation, and the classic example is undoing by
recomputing:

```python
        current = current[:-1]              # O(k): builds a new list every time
        current.pop()                       # O(1): the right way
```

So the undo adds `O(1)` per node to a tree that already costs `O(1)` per node to walk. **The un-choose
is free.**

### Mutate-and-undo versus copy-down

```
 style A:  one list, O(1) per node,   O(depth) memory live
 style B:  a new list per node,       O(depth) per node,   O(depth^2) live on one path
```

Concretely, subsets at n = 20:

```
 nodes in the tree                      2^20      = 1,048,576
 average length of `current`            10
 style A copies                         only at record time     ~10 million elements
 style B copies                         at every node           ~10 million elements  + 1M allocations
```

For subsets they end up close, because every node records. For permutations they do not:

```
 permutations, n = 9
   nodes                       ~ 986,000
   leaves                        362,880
   style A element copies        362,880 × 9   ≈  3.3 million
   style B element copies        986,000 × ~5  ≈  4.9 million, plus 986,000 allocations
```

**Roughly a 1.5× to 3× difference, and it grows with depth.** Not the difference between passing and
failing — but "I mutate and undo because copying at every node multiplies the work by the depth" is a
better sentence than "I just do it this way".

### Pruning, which is the real number

This is the one to memorise, because it is the argument for the whole technique.

```
 N-Queens          nodes without pruning     nodes with pruning     ratio
 ---------------   ----------------------    -------------------    --------
 n = 6                        55,987                     543          103×
 n = 8                    19,173,961                   2,057        9,321×
 n = 10                6,257,890,000 (est.)            35,538      176,000×
```

**One `if` before the recursive call, and n = 8 goes from nineteen million nodes to two thousand.** The
undo is what makes the pruning possible — you can only afford to check "is this column free?" cheaply if
the column set is kept correct as you descend, and it is only kept correct because you remove from it on
the way out.

### Space

```
 shared state (current, used, sets)     O(n)     — one copy, reused
 stack                                  O(depth)
 ------------------------------------------------
 extra space:  O(n + depth)
```

Backtracking's memory is the *deepest path*, never the tree. That is what makes it usable at all: the
tree can have nineteen million nodes while the memory never exceeds a few dozen frames.

---

## 7. The traps

### Trap 1 — forgetting one of two undoes

```python
            used[i] = True
            current.append(items[i])
            explore()
            current.pop()
                                            # missing: used[i] = False
```

```
 permutations([1, 2, 3])  ->  [[1, 2, 3]]
```

One answer instead of six, no error. **Count the chooses, count the undoes, make them match** — before
you run it.

### Trap 2 — undoing after the loop instead of inside it

```python
        for i in range(len(items)):
            current.append(items[i])
            explore()
        current.pop()                       # WRONG: outside the loop
```

Every iteration appends and only the last one is removed, so `current` grows without bound.

```
 subsets([1,2,3])  ->  [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 3], ...]
```

Nonsense answers, growing lengths, and eventually:

```
 RecursionError: maximum recursion depth exceeded
```

### Trap 3 — returning early past the undo

```python
            visited[r][c] = True
            if explore(nr, nc):
                return True                 # visited[r][c] stays True for ever
            visited[r][c] = False
```

Correct for a single query, wrong the moment the same grid is reused — the second call finds cells
already marked and returns `False` for a path that exists. It is the classic "passes the first test,
fails the test suite" bug. Undo, then return.

### Trap 4 — undoing a copy, which does nothing

```python
        explore(current + [x])              # style B: the callee got its OWN list
        current.pop()                       # removes something the callee never saw
```

Mixing the two styles. The `pop` now removes an element from `current` that was never appended to it:

```
 IndexError: pop from empty list
```

**Pick one style per function.** If you pass a copy, there is nothing to undo; if you mutate, undo
exactly what you mutated.

### Trap 5 — shallow copies of nested state

```python
        snapshot = board[:]                 # a NEW outer list of the SAME inner lists
        explore()
        board = snapshot                    # restores nothing at all
```

`board[:]` copies the outer list only. Every row is still the same object, so a change to
`board[2][3]` is visible in the "snapshot". You need `copy.deepcopy`, which is expensive, or — better —
do not snapshot at all: **mutate one cell and set that one cell back.**

```python
        board[r][c] = digit
        explore()
        board[r][c] = "."                   # O(1), correct, no copying
```

### Trap 6 — mutating a collection while looping over it

```python
        for choice in available:
            available.remove(choice)        # modifying the thing being iterated
            explore()
            available.add(choice)
```

```
 RuntimeError: Set changed size during iteration
```

Loop over a snapshot — `for choice in list(available):` — or, better, loop over the indices and use a
boolean array, which is what `used` is for.

### Trap 7 — checking validity at the leaf instead of on the way down

```python
        if row == n:
            if is_valid_board(placement):   # checking only at the bottom
                record()
            return
```

Correct answer, catastrophically slow. On N-Queens at n = 8 it is 19 million nodes instead of 2,057.
**The check must happen before you descend**, because the whole point is to not walk the branch.

### Trap 8 — thinking the undo is "cleanup"

It is not cleanup, and calling it that in an interview costs you. Nothing is leaked and nothing is
tidied. The pop is **what makes the sibling branch correct**: `current` is one object shared by every
branch of the tree, and the un-choose is what restores it to the state that branch is entitled to see.

---

## 8. In the interview

### How it gets asked

- Directly, after you write any backtracking solution: *"Why did you pop that element after the
  recursive call?"*
- The variation: *"What happens if you leave that line out?"* — they want the specific wrong output,
  not "it breaks".
- The design probe: *"Could you write this without mutating anything?"*
- The efficiency probe: *"Where does the pruning happen, and how much does it save?"*
- The definitional one: *"What is the difference between backtracking and brute force?"*

### What to say out loud, in the first ninety seconds

1. **State the invariant.** "When a call returns, every piece of shared state is exactly what it was
   when the call started. That is the only invariant, and if it holds at every node the tree is
   correct."
2. **Say what the pop is, and is not.** "It is not cleanup. `current` is a single object shared by
   every branch. The pop is what makes the *next* branch see the state it is entitled to see."
3. **Enumerate your state.** "I am changing three things before I recurse: the partial answer, the used
   flags, and the column set. So there are three lines after the call, undoing them in reverse."
4. **Name what you moved into the arguments.** "`remaining` is a parameter, not a mutation, so there is
   nothing to undo for it. Anything I can pass by value is one thing I cannot forget to restore."
5. **Point at the pruning line.** "The `continue` before the apply is what makes this backtracking
   rather than enumeration. Checking on the way down instead of at the leaf is the whole speed-up."
6. **Give the alternative and dismiss it with a reason.** "I could pass a fresh copy down and never
   undo anything. That is impossible to get wrong, and it allocates at every node rather than every
   leaf, so it multiplies the work by the depth."

### The follow-ups

**"What happens if you leave the pop out?"**
"For subsets, the 'skip this element' branch still contains the element, so about half the answers are
wrong — and the count is still 2ⁿ, so nothing looks obviously broken. For permutations, if it is the
`used[i] = False` I forget, elements are consumed permanently and I get exactly one answer instead of
`n!`. Neither raises an error. That is the thing worth saying: **the missing undo is always silent**,
which is why I write the choose, the recurse and the undo as one block rather than three decisions."

**"Could you write it without mutating anything?"**
"Yes. Pass `current + [x]` down instead of appending, and the callee gets its own list, so there is
nothing to restore. It is shorter and it cannot be got wrong. The cost is that it allocates a new list
at every *node*, not every leaf — for permutations at n = 9 that is nearly a million allocations against
360,000 in the mutating version. I would use it if the state were tiny, or if I wanted the partial
answers to be immutable so I could share them. And I would never mix the two styles in one function: if
you pass a copy and then also pop, you get an `IndexError` from popping something the callee never saw."

**"What is the difference between backtracking and brute force?"**
"One line: the validity check before the recursive call. Brute force generates every candidate and
tests it at the end; backtracking rejects a partial candidate as soon as it cannot possibly lead to a
solution, so entire subtrees are never walked. On N-Queens at n = 8, testing at the leaf visits about
nineteen million nodes and pruning on the way down visits two thousand and fifty-seven. Same answer, a
factor of nine thousand. And the pruning is only affordable because the undo keeps the running checks —
the column set, the diagonal sets — correct as you descend."

**"How do you decide what needs undoing?"**
"I list everything the recursion can see that I changed. It is three kinds: the partial answer, the
availability marks, and derived bookkeeping like a running total or a set of occupied diagonals. The
third kind is where bugs live, because it does not feel like state. Then I count: lines that change
something before the call must equal lines that change it back after, and I undo in reverse order. And
wherever I can, I move state into the parameter list instead, because a value passed by argument
physically cannot need undoing."

**"Your search returns True early. Is the undo still correct?"**
"It is skipped, and whether that matters depends on the caller. If I am unwinding straight out and
nobody looks at the state again, it is fine and it saves a little work. If the same grid or board is
reused for a second query, it is a real bug — cells stay marked and the second call reports no path when
one exists. The safe habit is to capture the result, undo, and then return, which is two extra lines
and removes an entire category of works-once bugs."

**"Where would this pattern not be the right tool?"**
"When the same subproblem is reached by many different paths. Backtracking has no memory — it will
re-solve an identical state every time it arrives there. The moment I notice that the state can be
described by a few numbers and is reached repeatedly, that is dynamic programming, and the tree collapses
from exponential to polynomial. Backtracking is for problems where I genuinely need to enumerate or
where the pruning is strong enough that the tree stays small."

### A model answer

Asked: *why did you pop that element after the recursive call?*

> "Because `current` is one list object shared by every branch of the tree, and the pop is what makes
> the **next** branch correct. It is not cleanup — nothing is leaked if I skip it.
>
> The invariant I am maintaining is this: **when a recursive call returns, every piece of shared state
> is exactly what it was when that call started.** If that holds at every node, then each branch sees
> only the choices on its own path from the root, which is precisely what 'explore this subtree' means.
> If it fails at one node, every sibling after that node is exploring a state that no branch actually
> chose — and the answers are wrong with no error at all.
>
> Concretely: I append the element, recurse to explore everything that follows from taking it, and pop
> so that the sibling branch — the one that does *not* take it — starts from the same list I started
> from. Leave the pop out and the skip branch still contains the element, so half the subsets are
> wrong, and the count is still 2ⁿ so nothing looks broken.
>
> The rule I actually apply while writing is to count. Every line before the recursive call that changes
> something the recursion can see needs a matching line after it, undone in reverse order. In the
> permutations version there are two — the `used` flag and the append — so there are two undoes. In
> N-Queens there are four: the row's column, the two diagonal sets, and the placement. And I move
> whatever I can into the parameter list instead, because a value passed as an argument cannot need
> undoing — that is why `remaining` in combination sum has no undo line.
>
> The alternative is to pass a fresh copy down: `explore(current + [x])`. Then nothing is shared and
> nothing needs restoring. It is shorter and impossible to get wrong, and it allocates at every node
> instead of every leaf, so it multiplies the work by roughly the depth. I would use it for very small
> state.
>
> One more thing the undo buys, which is really the point of the whole technique. Because the state is
> kept correct as I descend, I can run cheap validity checks *on the way down* and skip whole subtrees.
> On N-Queens at n = 8 that is the difference between about nineteen million nodes and two thousand and
> fifty-seven. The undo is what makes that check affordable."

---

## 9. Recall card

- **The invariant, and there is only one: when a call returns, every piece of shared state is exactly
  what it was when the call started.** The pop is **not cleanup** — `current` is one object shared by
  every branch, and the un-choose is what makes the *sibling* branch correct. A missing undo is
  **always silent**: subsets gets half its answers wrong, permutations returns **one answer instead of
  `n!`**.
- **State is three kinds: the partial answer, the availability marks, and derived bookkeeping** (a
  running sum, an occupied-column set). The third is where the bugs live. **Count the lines before the
  call and the lines after; they must match, and undo in reverse order.**
- **Anything passed as an argument needs no undo** — ints, strings and tuples are values, so
  `build(i+1, remaining - c)` has nothing to restore. Move state into the parameter list wherever you
  can; it is state you cannot forget.
- **The `if not is_valid: continue` BEFORE the apply is what makes it backtracking rather than
  enumeration.** Check on the way down, never at the leaf: **N-Queens at n = 8 is 19,173,961 nodes
  without it and 2,057 with it.** Every undo must be **O(1)** — `board[r][c] = "."`, not a fresh copy —
  or the pruning stops being affordable.
- **Two styles: mutate-and-undo (O(1) per node, must not forget) or pass-a-copy (`explore(current +
  [x])`, cannot be got wrong, allocates at every node).** Never mix them — popping after passing a copy
  gives `IndexError: pop from empty list`. And **undo before an early `return`**, or a reused grid
  reports no path when one exists.
