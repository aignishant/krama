---
day: 91
track: dsa
title: "Subsets: the include-or-exclude tree"
phase: "Recursion and backtracking"
status: written
---

# Day 091 · DSA — Subsets: the include-or-exclude tree

**After today you can:** You can generate every subset and draw the decision tree that produced them.

**The interviewer asks it as:** *Generate all subsets of this array.*

---

## 1. What this is, and why they ask it

Given `[1, 2, 3]`, produce every subset: the empty one, `[1]`, `[2]`, `[3]`, `[1,2]`, `[1,3]`,
`[2,3]`, and `[1,2,3]`. Eight of them, and eight is not a coincidence — it is 2³.

The reason is the shape of the problem, and the shape is the lesson. **For each element there are
exactly two choices: take it, or leave it.** Three elements, three independent yes-or-no decisions, 2³
combinations. Draw those decisions as a tree and every leaf is one subset, produced exactly once.

That tree is the first **backtracking** problem, and backtracking is the next six days. The pattern —
*choose, recurse, un-choose* — is the same for subsets, permutations, combinations, N-Queens, Sudoku
and word search. Subsets is where you meet it because it is the smallest possible instance: the choice
is binary and there is nothing to check.

They ask it because the recursion is six lines and there are three traps in them, one of which —
appending the same list object over and over — produces a result that is confidently, uniformly wrong
in a way that is very hard to see. And because "now do it with duplicates" is a one-line change that
almost nobody gets right first time.

---

## 2. The story

The lunch at Sridhar's cousin's wedding was served the way those lunches always are: everyone sitting
in a long row, and the men coming down the line one at a time, each carrying one vessel.

Six of them, in a fixed order. Rice. Then the sambar man. Then palya. Then the fried thing. Then curd.
Then payasa at the end.

Each one stops in front of you and you either nod or you put your hand over the plate. That is the
whole interaction. Six of them, six yes-or-no decisions, and whatever ends up on your plate is the
result.

Sridhar's nephew Karthik, who is fourteen and had been made to sit at the end of the row, worked
something out during the meal and would not let it go afterwards.

He said: everybody in this row is getting a different plate, and there are exactly sixty-four possible
plates, and that is all there are.

His argument was that the first man splits the whole row into two kinds of people — those who took
rice and those who did not. Then the second one splits each of those two groups into two again. Six of
them, doubling each time: two, four, eight, sixteen, thirty-two, sixty-four.

His uncle did not believe it, so Karthik listed them. He went along an imaginary row saying yes to
every one of them, then yes to five and no to the last, then yes to four and no to the fifth, and so
on — walking the decisions in order, changing the last one first. It took him about ten minutes and he got
sixty-four, with no plate said twice and none missing.

The only part he got wrong at first was the recording. He was calling each plate out to his cousin,
who was keeping a list on her phone, and he kept saying "and now add the payasa" and "now take off the
payasa" — describing changes to the same plate rather than the finished plate itself. Halfway through
she pointed out that her list was sixty-four lines and every line said the same thing, because she had
only ever been told about one plate that kept changing.

After that he read out the whole plate, from the beginning, each time.

---

## 3. The idea in plain English

Each man with a vessel is one element. Nodding or covering your plate is **include or exclude**. And Karthik's
cousin's list is the copy trap, which is the trap of this whole day.

### Why 2ⁿ

There are `n` elements and each one is an independent yes-or-no decision, so the number of
combinations is `2 × 2 × … × 2 = 2ⁿ`. Six vessels, sixty-four plates.

That is not a bound to be improved on. **The output *is* 2ⁿ things**, so no algorithm can be faster
than 2ⁿ — it has to at least write them down. Saying that early is what stops an interviewer asking
"can you do better?"

```
 n = 10   ->  1,024 subsets
 n = 20   ->  1,048,576
 n = 30   ->  1,073,741,824    — about a billion; not going to happen
```

**Subsets problems have small `n`, always.** If a problem says `n ≤ 20`, that constraint is telling you
it expects an exponential solution.

### The decision tree

At index `i`, two branches: take `items[i]`, or do not. Each branch recurses on `i + 1`. When `i`
reaches the end, one complete decision path has been made, and that path *is* a subset.

```python
def subsets(items):
    result = []
    current = []

    def choose(index):
        if index == len(items):
            result.append(current[:])       # a COPY of the finished plate
            return
        current.append(items[index])        # 1. take it
        choose(index + 1)
        current.pop()                       # 2. un-take it
        choose(index + 1)                   # 3. and go on without it

    choose(0)
    return result
```

Six lines of body, and they are the pattern the next six days are built on:

> **choose · recurse · un-choose**

The `current.pop()` is the un-choose, and it is what makes one list serve every branch. Without it,
the left branch's choice leaks into the right branch and you get nonsense.

### The copy, which is the trap

```python
        result.append(current)              # WRONG — appends a REFERENCE
```

`current` is one list object that is mutated throughout the entire recursion. Appending it stores a
*pointer* to it, so `result` ends up holding 2ⁿ references to the same list — and that list is empty
when the recursion finishes, because every `append` was matched by a `pop`.

```
 subsets([1, 2, 3])  with `result.append(current)`
   -> [[], [], [], [], [], [], [], []]
```

Eight subsets, all empty, all the same object. Karthik's cousin's list with sixty-four identical
lines.

**`current[:]` — or `list(current)`, or `current.copy()` — takes a snapshot.** Say "copy" out loud as
you type it; this is the single most common backtracking bug and it is completely silent.

### The other two formulations, both worth knowing

**Iterative doubling.** Karthik's actual argument: each new element doubles the answer.

```python
    result = [[]]
    for item in items:
        result += [subset + [item] for subset in result]
```

Two lines. Start with the empty subset; for each element, take everything you have and add a copy with
that element appended. `[[]] → [[], [1]] → [[], [1], [2], [1,2]] → …`

No recursion, no stack, no copy trap — the list comprehension builds new lists. This is often the
version to write in an interview, and then say the recursive one is the shape that generalises.

**Bitmasks.** There are 2ⁿ subsets and 2ⁿ numbers with `n` bits, so number them:

```python
    for mask in range(1 << len(items)):
        subset = [items[i] for i in range(len(items)) if mask & (1 << i)]
```

Bit `i` of the mask says whether element `i` is in. `mask = 5` is binary `101`, which is `[items[0],
items[2]]`. Elegant, O(n·2ⁿ), and it only works when `n ≤ 63` — which for a subsets problem it always
is.

**Three ways, same answer.** Interviewers ask for the recursive one because it is the one that
generalises to permutations, combinations and constrained search.

### Subsets with duplicates

`[1, 2, 2]` has 2³ = 8 decision paths but only **six distinct subsets**, because `[1, 2]` can be made
two ways. The fix is two lines, and the second is the one people get wrong:

```python
    items.sort()                            # 1. equal elements become adjacent
    ...
    for i in range(index, len(items)):
        if i > index and items[i] == items[i - 1]:
            continue                        # 2. skip a duplicate at the SAME level
        ...
```

**`i > index`, not `i > 0`.** The condition means "this is not the first choice being considered at
this position in the tree". Using `i > 0` would also skip the *second* `2` when it legitimately follows
the first inside a subset, and you would lose `[2, 2]` entirely.

That single comparison is the whole duplicate-handling idea, and it reappears in Combination Sum II,
Permutations II and Subsets II. Get it right once.

### The relationship to what comes next

- **Subsets** — two choices per element: in or out. Today.
- **Combinations** (choose `k` from `n`) — the same tree, pruned when the subset reaches size `k`.
- **Permutations** — `n` choices at the first level, `n−1` at the second: a different tree, same
  choose-recurse-un-choose.
- **N-Queens, Sudoku, word search** — the same tree with a *validity check* before recursing, which is
  what makes it "backtracking" rather than "enumeration".

**Subsets is the version with no constraint at all**, which is why it is first. Everything after adds
a condition on when you may take a branch.

---

## 4. The picture

The decision tree for `[1, 2, 3]`. Left branch takes the element, right branch skips it.

```
                          choose(0), current = []
                         /                        \
                    take 1                      skip 1
                       /                            \
            choose(1) [1]                      choose(1) []
             /        \                        /        \
        take 2      skip 2                take 2      skip 2
          /             \                  /             \
   choose(2) [1,2]  choose(2) [1]   choose(2) [2]   choose(2) []
      /     \          /     \         /     \         /     \
 [1,2,3]  [1,2]     [1,3]   [1]     [2,3]   [2]     [3]     []

 8 leaves = 2^3 subsets, each produced exactly once
 depth = 3 = n           (the stack never exceeds n frames)
 nodes = 2^(n+1) - 1 = 15 calls
```

What to notice: **the depth is `n` and the leaf count is 2ⁿ.** Time is the whole tree; space is the
deepest path — the distinction from [day 088](../day-088-the-call-stack/README.md), in its most
dramatic form. Fifteen calls, three frames.

The `current` list over time, which is why the copy matters:

```
 step   action              current       result
 ----   ------------------  ------------  --------------------------------
   1    append 1            [1]
   2    append 2            [1,2]
   3    append 3            [1,2,3]
   4    LEAF -> copy        [1,2,3]       [[1,2,3]]
   5    pop                 [1,2]
   6    LEAF -> copy        [1,2]         [[1,2,3], [1,2]]
   7    pop                 [1]
   8    append 3            [1,3]
   9    LEAF -> copy        [1,3]         [[1,2,3], [1,2], [1,3]]
  ...
  end                       []            8 subsets

 `current` is ONE list, mutated all the way through, and it is EMPTY at the end.
 Storing it instead of a copy stores 8 pointers to that one empty list.
```

And the duplicate skip, which is the fiddly part:

```
 items = [1, 2, 2]  (sorted)

   index 0:  i=0 take 1 ┐   i=1 take 2 ┐   i=2 take 2  <- i > index and items[2]==items[1]
                        │              │                  SKIP: it would repeat the
                        │              │                  subset already made at i=1
                        v              v
   index 1:      i=1 take 2      i=2 take 2  <- i == index here, so NOT skipped
                                                and [2,2] is correctly produced

 the condition is `i > index`, not `i > 0`:
   i > index  means "another choice at the SAME tree level"  -> skip
   i == index means "the next element inside this subset"    -> keep
```

---

## 5. The code, built step by step

### Step 1 — say the size before writing anything

"There are 2ⁿ subsets, so any solution is at least 2ⁿ — the output alone is that big. For n = 20 that
is a million, which is fine; for n = 30 it is a billion, which is not. So I would expect n to be small,
and I will not be looking for something sub-exponential."

That sentence prevents the "can you do better?" exchange entirely.

### Step 2 — the shape: choose, recurse, un-choose

```python
        current.append(items[index])        # choose
        choose(index + 1)                   # recurse
        current.pop()                       # un-choose
```

Write those three lines as a unit, every time, in that order. **The `pop` is not cleanup — it is what
lets one list serve the whole tree.** Forgetting it is not a leak; it is a wrong answer.

### Step 3 — the base case, and the copy

```python
        if index == len(items):
            result.append(current[:])       # COPY. Say the word as you type it.
            return
```

The base case is the measure — `len(items) - index` — reaching zero, exactly as on
[day 089](../day-089-recursion-that-terminates/README.md).

### Step 4 — the other arrangement, which some find clearer

The version above has the leaf at the bottom. There is an equivalent formulation where **every node is
a subset**, not just the leaves:

```python
    def build(start):
        result.append(current[:])           # every node counts, including the root
        for i in range(start, len(items)):
            current.append(items[i])
            build(i + 1)
            current.pop()
```

Same 2ⁿ answers, and this shape is the one that generalises to combinations — cap the loop and you get
"choose k" — and to Combination Sum, where you check a running total before recursing. If you can only
remember one, remember this one, because it is the template for the rest of the phase.

### Step 5 — duplicates

```python
        for i in range(start, len(items)):
            if i > start and items[i] == items[i - 1]:
                continue                    # `> start`, not `> 0`
```

With the array sorted first. Say the two halves out loud: **sort so equal elements are adjacent**, and
**skip a repeat only when it is another choice at the same level**.

### The complete solution

```python
def subsets(items: list[int]) -> list[list[int]]:
    """Every subset, via the include-or-exclude tree.

    2^n subsets, so the output alone is exponential — no algorithm can beat it.
    Depth n, leaves 2^n: TIME is the whole tree, SPACE is the deepest path.

    The pattern for the whole phase: choose, recurse, UN-choose.
    """
    result: list[list[int]] = []
    current: list[int] = []

    def choose(index: int) -> None:
        if index == len(items):
            result.append(current[:])       # COPY — `current` is one mutating list
            return
        current.append(items[index])        # choose
        choose(index + 1)                   # recurse
        current.pop()                       # un-choose
        choose(index + 1)                   # and the branch without it

    choose(0)
    return result


def subsets_template(items: list[int]) -> list[list[int]]:
    """The same answers, arranged so EVERY node is a subset rather than only
    the leaves. This is the template the rest of the phase uses: cap the loop
    and it becomes combinations; add a check and it becomes constrained search.
    """
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int) -> None:
        result.append(current[:])
        for i in range(start, len(items)):
            current.append(items[i])
            build(i + 1)
            current.pop()

    build(0)
    return result


def subsets_iterative(items: list[int]) -> list[list[int]]:
    """Karthik's argument, directly: each element doubles the answer.
    Two lines, no recursion, no stack, and no copy trap."""
    result: list[list[int]] = [[]]
    for item in items:
        result += [subset + [item] for subset in result]
    return result


def subsets_bitmask(items: list[int]) -> list[list[int]]:
    """2^n subsets and 2^n numbers with n bits, so number them.
    Bit i of the mask says whether element i is in. Works up to n = 63."""
    n = len(items)
    return [
        [items[i] for i in range(n) if mask & (1 << i)]
        for mask in range(1 << n)
    ]


def subsets_with_duplicates(items: list[int]) -> list[list[int]]:
    """Subsets II. Two lines of difference from the template.

    1. SORT, so equal elements are adjacent.
    2. Skip a repeat only when it is another choice at the SAME level:
       `i > start`, NOT `i > 0`. With `i > 0` you would also skip the second
       2 when it legitimately follows the first, losing [2, 2] entirely.
    """
    items = sorted(items)
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int) -> None:
        result.append(current[:])
        for i in range(start, len(items)):
            if i > start and items[i] == items[i - 1]:
                continue
            current.append(items[i])
            build(i + 1)
            current.pop()

    build(0)
    return result


def combinations(items: list[int], k: int) -> list[list[int]]:
    """The same tree with one cap: stop when the subset reaches size k.

    The extra `if` is PRUNING — if there are not enough elements left to reach
    k, the branch cannot possibly succeed, so do not walk it. That is the idea
    the rest of the phase is built on.
    """
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, len(items)):
            if len(current) + (len(items) - i) < k:
                break                       # not enough left: prune
            current.append(items[i])
            build(i + 1)
            current.pop()

    build(0)
    return result


def subsets_broken(items: list[int]) -> list[list[int]]:
    """The trap, written out so you can run it: appends a REFERENCE, not a copy.
    Every entry is the same object, and it is empty by the end."""
    result: list[list[int]] = []
    current: list[int] = []

    def choose(index: int) -> None:
        if index == len(items):
            result.append(current)          # no [:]
            return
        current.append(items[index])
        choose(index + 1)
        current.pop()
        choose(index + 1)

    choose(0)
    return result


if __name__ == "__main__":
    print(subsets([1, 2, 3]))
    # [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]

    print(sorted(map(sorted, subsets_template([1, 2, 3]))) ==
          sorted(map(sorted, subsets([1, 2, 3]))))                    # True
    print(sorted(map(sorted, subsets_iterative([1, 2, 3]))) ==
          sorted(map(sorted, subsets([1, 2, 3]))))                    # True
    print(sorted(map(sorted, subsets_bitmask([1, 2, 3]))) ==
          sorted(map(sorted, subsets([1, 2, 3]))))                    # True

    print(len(subsets([1, 2, 3, 4, 5])), 2 ** 5)                      # 32 32
    print(subsets([]), subsets([7]))                                  # [[]] [[7], []]

    print(subsets_with_duplicates([1, 2, 2]))
    # [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    print(len(subsets_with_duplicates([1, 2, 2])), "distinct, vs", 2 ** 3, "paths")
    # 6 distinct, vs 8 paths

    print(combinations([1, 2, 3, 4], 2))
    # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    print(subsets_broken([1, 2, 3]))
    # [[], [], [], [], [], [], [], []]   <- eight references to one empty list

    # the size, so you feel it
    for n in (10, 20, 22):
        print(f"n = {n}: {2 ** n:,} subsets")
```

---

## 6. What it costs

### Time

```
 subsets produced:      2^n
 average subset length: n / 2
 elements written:      2^n × n/2  =  n · 2^(n-1)
 -> O(n · 2^n) total work
```

The `2ⁿ` is the number of answers and the `n` is the cost of copying each one. **You cannot beat 2ⁿ,
because the output is that big** — and saying so removes the "can you do better?" question.

```
 n = 10:  1,024 subsets,       ~5,000 elements written
 n = 20:  1,048,576 subsets,   ~10,000,000 elements
 n = 25:  33,554,432 subsets,  ~420,000,000 elements   — seconds to minutes
 n = 30:  1,073,741,824        — not going to finish
```

**Twenty is comfortable, twenty-five is painful, thirty is impossible.** A problem that asks for
subsets will bound `n` at twenty-something, and that bound is the hint.

### Calls versus depth

```
 tree nodes (calls):  2^(n+1) - 1     n = 20 -> ~2,000,000 calls
 depth:               n               n = 20 -> 20 frames
```

The most dramatic instance of the [day 088](../day-088-the-call-stack/README.md) distinction: **two
million calls, twenty frames.** A subsets recursion will never hit the recursion limit — the input
would have to be a thousand elements, and 2¹⁰⁰⁰ is not a number anyone is waiting for.

### Space

```
 output:    2^n lists, average length n/2  ->  O(n · 2^n)   — unavoidable
 current:   one list of at most n          ->  O(n)
 stack:     n frames                       ->  O(n)
 ---------------------------------------------------------
 extra space beyond the output:  O(n)
```

**The extra space is O(n), not O(2ⁿ)** — one working list and `n` frames. That is worth saying,
because it is the honest answer to "how much memory does this use?" and it separates the output from
the algorithm.

```
 n = 20, integers:  1,048,576 lists × ~120 B overhead  ≈  126 MB of Python list objects
```

Which is a real number, and the reason subsets problems generate rather than store when they can.

### The three formulations, compared

```
 recursive:   O(n · 2^n) time, O(n) extra   generalises to everything else
 iterative:   O(n · 2^n) time, O(n · 2^n)   two lines, no stack, builds all lists as it goes
 bitmask:     O(n · 2^n) time, O(n) extra   n <= 63; no recursion
```

Same complexity, and the difference is what they teach. **Write the recursive one if the interviewer
wants backtracking; write the iterative one if they want the answer.**

### Duplicates

```
 [1, 2, 2]:   2^3 = 8 decision paths, 6 distinct subsets
 [2, 2, 2]:   8 paths, 4 distinct       ([], [2], [2,2], [2,2,2])
 all distinct: 2^n paths, 2^n subsets
```

The skip prunes whole branches rather than filtering at the end, which matters: filtering a
million-element result with a set costs the memory of the million *and* requires the subsets to be
hashable. **Prune, do not filter.**

---

## 7. The traps

### Trap 1 — appending the list instead of a copy

```python
        result.append(current)              # a REFERENCE to one mutating list
```

```
 subsets([1, 2, 3])  ->  [[], [], [], [], [], [], [], []]
```

Eight results, all the same object, all empty — because every `append` was undone by a `pop` before the
recursion finished. **The single most common backtracking bug**, it produces a uniformly wrong answer
with no error, and it looks fine until you print it.

`current[:]`, `list(current)` or `current.copy()`. Say "copy" as you type it.

### Trap 2 — forgetting to un-choose

```python
        current.append(items[index])
        choose(index + 1)
                                            # missing: current.pop()
        choose(index + 1)
```

The "skip this element" branch now runs with the element still in `current`, so both branches include
it and half the subsets are wrong. Not a crash — a wrong answer that looks plausible, because the
count is still 2ⁿ.

**Choose, recurse, un-choose. Write all three as one unit.**

### Trap 3 — `i > 0` instead of `i > start` in the duplicate skip

```python
            if i > 0 and items[i] == items[i - 1]:
                continue
```

On `[1, 2, 2]` this loses `[2, 2]` and `[1, 2, 2]`, because it skips the second `2` even when it is
being appended *after* the first inside the same subset. The condition must mean **"another choice at
this level"**, which is `i > start`.

Test it on `[2, 2]`: the right answer has three subsets — `[]`, `[2]`, `[2, 2]` — and the wrong one has
two.

### Trap 4 — forgetting to sort before de-duplicating

```python
    # items = [2, 1, 2]  — not sorted
            if i > start and items[i] == items[i - 1]:
```

The skip compares *adjacent* elements, so equal values must be adjacent. Unsorted, the two `2`s are
never neighbours and nothing is skipped, so duplicates come out anyway. `sort()` first, always.

### Trap 5 — filtering duplicates at the end

```python
    return [list(s) for s in {tuple(sorted(sub)) for sub in subsets(items)}]
```

Correct, and it builds all 2ⁿ subsets before removing any. On `[2] * 20` that is a million subsets
generated to return twenty-one. **Prune in the tree, do not filter the result.**

### Trap 6 — `[[]]` versus `[]` as the starting point

```python
    result = []                             # iterative version
    for item in items:
        result += [subset + [item] for subset in result]
    return result                           # -> [] for any input
```

Starting from an empty list means the comprehension never has anything to extend, so the answer is
always empty. The seed is `[[]]`: **one subset, the empty one.** And the empty subset is a real answer
that must appear in the output — `subsets([])` is `[[]]`, not `[]`.

### Trap 7 — expecting a particular order

The recursive version emits `[[1,2,3], [1,2], [1,3], [1], [2,3], [2], [3], []]`; the iterative one
emits `[[], [1], [2], [1,2], [3], …]`. Both are complete and correct. If a test compares against an
exact list, sort both sides — and if an interviewer's example is in a different order, say "the order
differs and the set is the same" rather than assuming you are wrong.

### Trap 8 — trying to be clever about the complexity

There are 2ⁿ subsets. Any correct solution must produce all of them, so **no algorithm is faster than
O(2ⁿ)**. Attempting to "optimise" is a misunderstanding of the problem, and saying the bound out loud
early is the way to avoid twenty minutes of it.

---

## 8. In the interview

### How it gets asked

- The base: *"Generate all subsets of this array."* LeetCode 78.
- Immediately after: *"Now the array can contain duplicates and the subsets must be unique."*
  LeetCode 90.
- The variation: *"All combinations of k elements from n."* LeetCode 77. Same tree, one cap.
- The escalation, which is the rest of the phase: *"All permutations."* *"All combinations that sum to
  a target."*
- The complexity probe: *"What is the complexity, and can you do better?"*

### What to say out loud, in the first ninety seconds

1. **Name the shape and the size together.** "Every element is an independent take-it-or-leave-it
   decision, so there are 2ⁿ subsets. The output alone is exponential, so no solution can be faster
   than that — I would expect `n` to be small."
2. **Describe the tree before writing code.** "I will walk a decision tree: at each index, one branch
   takes the element and one skips it. Each leaf is a complete set of decisions, which is one subset."
3. **Say the pattern by name.** "Choose, recurse, un-choose. The un-choose is what lets a single
   working list serve every branch."
4. **Flag the copy before you write it.** "When I record a subset I have to append a *copy*, because
   the working list keeps mutating — appending the list itself gives 2ⁿ references to one list that
   ends up empty."
5. **Give both complexities separately.** "O(n · 2ⁿ) time — 2ⁿ subsets, each costing n/2 to copy — and
   O(n) extra space beyond the output: one working list and n stack frames."
6. **Offer the iterative one.** "There is also a two-line iterative version: start with the empty
   subset and double it with each element. Same complexity, no recursion. I will write the recursive
   one because it is the shape that generalises."

### The follow-ups

**"What is the complexity, and can you do better?"**
"O(n · 2ⁿ) — there are 2ⁿ subsets and each takes on average n/2 element copies to write out. And no,
you cannot do better, because **the output itself is 2ⁿ things** — any correct algorithm has to produce
all of them. Extra space beyond the output is only O(n): one working list of at most n elements, and n
stack frames. Worth separating those, because the tree has about two million *calls* at n = 20 and only
twenty frames — time is the whole tree, space is the deepest path."

**"Now the input has duplicates and the subsets must be unique."**
"Two changes. Sort the array first, so equal elements are adjacent. Then, inside the loop over
candidates, skip an element if it equals the previous one **and** it is not the first candidate at this
level — `i > start`, not `i > 0`. That condition means 'another choice at the same position in the
tree'. With `i > 0` you would also skip the second 2 when it legitimately follows the first inside a
subset, and you would lose `[2, 2]` entirely. The important part is that this prunes branches rather
than filtering afterwards — filtering would build all 2ⁿ subsets and then throw most away."

**"Why do you need the copy?"**
"Because `current` is a single list object that is mutated all the way through the recursion. Appending
it stores a reference, so the result holds 2ⁿ pointers to the same list — and by the time the recursion
finishes, every append has been matched by a pop, so that list is empty. You get 2ⁿ empty lists and no
error at all. `current[:]` takes a snapshot of what it holds at that moment."

**"Now do combinations of size k."**
"The same tree with a cap: record when the working list reaches size k and return, rather than at the
leaves. And I would add a prune — if the number of elements remaining is not enough to reach k, break
out of the loop, because that branch cannot possibly succeed. That pruning is really the point of the
whole phase: subsets is the version with no constraint, and everything after it adds a condition that
lets you cut off branches early."

**"Which version would you actually write?"**
"For subsets alone, the two-line iterative one — start with the empty subset and double it for each
element. Same complexity, no recursion, no copy trap. But I would write the recursive version in an
interview, because it is the template: cap the depth and it is combinations, change the loop and it is
permutations, add a validity check before recursing and it is N-Queens. Nobody asks about subsets
because they want subsets."

**"What if n is 40?"**
"Then the question is not really 'generate all subsets', because 2⁴⁰ is a trillion and the output would
be tens of terabytes. If somebody asks for subsets at n = 40, they want something else — a count, which
is 2ⁿ and needs no enumeration; or a *best* subset under some criterion, which is dynamic programming
or meet-in-the-middle, where you split into two halves of twenty, enumerate each in a million, and
combine. Meet-in-the-middle turns 2ⁿ into 2^(n/2) and is the standard trick when n is around forty."

### A model answer

Asked: *generate all subsets of this array.*

> "Let me start with the size, because it settles the whole approach. Every element is an independent
> decision — take it or leave it — so with n elements there are 2ⁿ combinations. That is not a bound I
> can improve on: **the output itself is 2ⁿ things**, so any correct algorithm has to write them all
> out. If you tell me n could be thirty, I would say that is a billion subsets and we should talk about
> what you actually need.
>
> The structure is a decision tree. At index zero there are two branches: one where I take the first
> element and one where I do not. Each branch does the same at index one, and so on. When I reach the
> end of the array, one complete set of decisions has been made, and that is one subset. Eight leaves
> for three elements.
>
> The code is the pattern I will use for the rest of this topic: **choose, recurse, un-choose.** Append
> the element to a working list, recurse on the next index, then pop it off and recurse again without
> it. The pop is not tidying up — it is what lets a single working list serve every branch of the tree.
> Leave it out and the 'skip' branch still contains the element, so half the answers are wrong, with no
> error.
>
> The one trap I would flag before writing it: when I record a subset, I append a **copy**, not the
> working list itself. The working list is one object being mutated throughout, so appending it stores
> a pointer — and by the end, every append has been matched by a pop, so all 2ⁿ entries point at the
> same empty list. It is completely silent and it is the classic bug here.
>
> Complexity: O(n · 2ⁿ) time, because there are 2ⁿ subsets and each costs about n/2 element copies to
> write. Extra space beyond the output is only O(n) — one working list and n stack frames. Those two
> are worth separating: at n = 20 the tree has about two million calls and the stack never exceeds
> twenty frames.
>
> There is also a two-line iterative version — start with a list containing the empty subset, and for
> each element add a copy of everything you have with that element appended. Same complexity, no
> recursion, no copy trap, and it is what I would write if I only needed subsets. I have written the
> recursive one because it is the shape that generalises: cap the size and it is combinations, add a
> validity check before recursing and it is N-Queens.
>
> If the array can contain duplicates, it is two more lines: sort it first so equal elements are
> adjacent, then skip a candidate that equals the previous one when it is not the first candidate at
> that level — `i > start`, not `i > 0`. That distinction is the whole thing: `i > start` means 'another
> choice at the same position in the tree', whereas `i > 0` would also block the second 2 from following
> the first inside a subset and lose `[2, 2]`."

---

## 9. Recall card

- **Every element is an independent take-it-or-leave-it decision, so there are exactly 2ⁿ subsets** —
  and **you cannot beat 2ⁿ because the output *is* 2ⁿ things.** Say the size first and the "can you do
  better?" question never happens. n = 20 is a million and comfortable; **n = 30 is a billion and
  impossible**, so a subsets problem always bounds n at twenty-something.
- **The pattern for the whole phase: choose · recurse · un-choose.** Write the three lines as one unit.
  The `pop` is **not cleanup** — it is what lets one working list serve every branch, and omitting it
  makes the "skip" branch still contain the element, with no error.
- **Append a COPY — `current[:]` — never the list itself.** `current` is one object mutated throughout,
  so appending it gives **2ⁿ references to one list that is empty at the end**: `[[], [], [], …]`, and
  no error. Say "copy" as you type it. This is the defining backtracking bug.
- **Duplicates take two lines: SORT first, then skip when `items[i] == items[i-1]` AND `i > start`** —
  `i > start` means "another choice at this *level*", while `i > 0` would also block the second 2 from
  following the first and lose `[2, 2]`. **Prune in the tree; never filter the result** — filtering
  builds all 2ⁿ before discarding.
- **Time is the whole tree, space is the deepest path: ~2 million calls at n = 20, and only 20
  frames.** O(n · 2ⁿ) time; **O(n) extra space beyond the output.** Three formulations, same complexity:
  the **recursive** one generalises (cap it → combinations, add a check → N-Queens), the **iterative
  doubling** one is two lines and has no copy trap (seed it `[[]]`, not `[]`), and the **bitmask** one
  works to n ≤ 63.
