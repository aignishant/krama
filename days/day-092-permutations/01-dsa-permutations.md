---
day: 92
track: dsa
title: "Permutations"
phase: "Recursion and backtracking"
status: written
---

# Day 092 · DSA — Permutations

**After today you can:** You can generate every ordering, with and without duplicates.

**The interviewer asks it as:** *Generate all permutations. Now handle duplicate values.*

---

## 1. What this is, and why they ask it

Given `[1, 2, 3]`, produce every ordering: `[1,2,3]`, `[1,3,2]`, `[2,1,3]`, `[2,3,1]`, `[3,1,2]`,
`[3,2,1]`. Six of them, and six is not a coincidence — it is 3 × 2 × 1.

A **permutation** is an arrangement of all the elements in some order. Nothing is left out and nothing
is repeated; only the order changes. That is the difference from yesterday: a subset asks *which
elements*, a permutation asks *in what order*.

The shape is the lesson. **At the first position you have `n` choices. Once you commit to one, the
second position has `n − 1` choices left, then `n − 2`, and so on.** Multiply them and you get
`n × (n−1) × … × 1`, which is written `n!` and said "n factorial". Three elements, six orderings. Four
elements, twenty-four.

They ask it because it is [yesterday's tree](../day-091-subsets/README.md) with one thing changed —
the branching factor is no longer two, and it shrinks as you descend — and because that change breaks
the `start` index that made subsets work. You now have to track *which elements are still available*,
and there are two completely different ways to do that. Then they say "now the input has duplicates",
and the fix that worked for subsets is wrong here, for a reason worth understanding.

---

## 2. The story

The photo happened at the end, the way it always does, when everyone had eaten and the hall was half
empty.

Ravi's four children were being lined up in front of the stage. Anu, Bharat, Chitra and Deepak. The
photographer, a thin man in a blue shirt who had been there since seven that morning, said "stand in a
line", and they did, and then the trouble started.

Anu wanted to be on the end. Bharat said he was always put on the end. Chitra said that last time she
had been standing directly behind Deepak and you could only see her shoulder. Deepak said nothing and
walked to the middle.

The photographer had clearly seen this before. He lowered the camera and said: fine. We will do all of
them.

Ravi laughed and asked how many that was.

The man worked it out standing there, holding the camera against his chest. He said, look. The first
spot in the line can be any one of the four. Once that is settled, the second spot can be any of the
three who are left. Then two. Then one. Four times three times two times one. Twenty-four.

Then he actually did it. He put Anu on the far left and made the other three run through their six
orders. Then Bharat on the far left, and the same six behind him. Then Chitra. Then Deepak.

He was careful about one thing, and he said so out loud while he worked. Each time he pulled a child
out of the line and moved them to the front, he put them back in exactly the spot they had come from
before he pulled the next one out. The line always looked the same as it had a moment ago.

He said if you do not put them back, you lose track of who is still waiting. You take the same photo
twice and you miss another one completely, and you do not notice, because twenty-four photos of four
children all look the same afterwards.

It took eleven minutes. Nobody complained, because everybody had been on the end of the line once.

---

## 3. The idea in plain English

The four children are the elements. A finished line is one permutation. And putting each child back
where they came from is the un-choose step — the same one from
[day 091](../day-091-subsets/README.md), now doing visible work.

### Why n!

At the first position, any of the `n` elements may go. Having placed one, `n − 1` remain for the second
position, then `n − 2`, and so on until one element is left with nowhere else to go.

```
 n = 3   ->  3 × 2 × 1                 =  6
 n = 4   ->  4 × 3 × 2 × 1             =  24
 n = 5   ->  5 × 4 × 3 × 2 × 1         =  120
 n = 10  ->  3,628,800
 n = 12  ->  479,001,600                — about half a billion; minutes
 n = 13  ->  6,227,020,800              — not going to finish
```

**`n!` grows faster than `2ⁿ`.** At n = 20, subsets is a million and permutations is 2.4 × 10¹⁸. A
permutations problem always has a tiny `n`. LeetCode 46 bounds it at 6. When you see `n ≤ 8`, the
constraint is telling you the answer is factorial.

And as with subsets, **you cannot beat `n!`, because the output is `n!` things.** Say that first.

### Why `start` no longer works

Yesterday's template walked `for i in range(start, len(items))`, and `start` meant "do not look
backwards". That was correct for subsets because `[1, 2]` and `[2, 1]` are the *same* subset, so
looking backwards would only produce repeats.

For permutations, `[1, 2]` and `[2, 1]` are **different answers**. You must look backwards. So `start`
is gone, and something has to replace it — something that says *which elements are already in the line*
rather than *how far along the list you are*.

There are two standard replacements, and interviewers ask about both.

### Replacement one: a `used` list

Keep one boolean per element. `used[i]` is `True` when element `i` is already standing in the line.

```python
    for i in range(len(items)):
        if used[i]:
            continue                    # already in the line; skip
        used[i] = True                  # choose
        current.append(items[i])
        build()                         # recurse
        current.pop()                   # un-choose
        used[i] = False                 # un-choose
```

**Two things are chosen and two things must be un-chosen.** That symmetry is the whole discipline of
backtracking. Miss the `used[i] = False` and the element is marked as used forever, so every branch
after the first is missing elements and you get far fewer than `n!` answers.

This is the version to write in an interview. It is obvious, it handles duplicates cleanly, and the
`used` list costs `n` booleans.

### Replacement two: swapping in place

The photographer's actual method. Do not build a separate line — rearrange the one you already have.

```python
    def build(first):
        if first == len(items):
            result.append(items[:])
            return
        for i in range(first, len(items)):
            items[first], items[i] = items[i], items[first]      # choose
            build(first + 1)
            items[first], items[i] = items[i], items[first]      # un-choose
```

At depth `first`, everything before `first` is already fixed and everything from `first` onward is
still available. Swapping element `i` into position `first` says "this one goes here next". The second
swap puts it back — the child returning to exactly the spot they came from.

No extra list, no `used` array. It is what people mean by "the in-place version". It also has a defect
that matters, and it is the third trap below: **it cannot handle duplicates**.

### Duplicates: `[1, 1, 2]`

Three elements, so `3! = 6` decision paths — but only **three distinct orderings**: `[1,1,2]`,
`[1,2,1]`, `[2,1,1]`. Each one is produced twice, because the two `1`s can swap places without
changing anything you can see.

The fix looks like yesterday's and is not.

```python
    items.sort()                        # 1. equal elements become adjacent
    ...
        if used[i]:
            continue
        if i > 0 and items[i] == items[i - 1] and not used[i - 1]:
            continue                    # 2. the previous equal one is NOT placed
```

Read the second condition slowly, because it is the hardest single line in the phase.

`items[i] == items[i - 1]` means "this element is interchangeable with the one before it".
`not used[i - 1]` means "the one before it is **not** currently in the line".

Put together: *I am about to place a duplicate whose identical twin is still sitting unused.* If I do
that, I am starting a branch identical to the branch I already started when I placed the twin here. So
skip it.

**The rule that comes out of it: among identical elements, always place them left to right.** The
second `1` may only be used if the first `1` has already been used. That forces exactly one
representative of each group of identical arrangements.

Yesterday's condition was `i > start`. Today's is `not used[i - 1]`. They are doing the same job — "do
not re-explore a branch already explored at this level" — in two different tree shapes.

### The library call

```python
    from itertools import permutations
    list(permutations([1, 2, 3]))
    # [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]
```

Tuples, not lists, and it does **not** de-duplicate: `permutations([1,1,2])` gives six tuples with
repeats. Know it exists, mention it, then write the recursive one, because the interviewer is asking
about the tree and not about the standard library.

---

## 4. The picture

The tree for `[1, 2, 3]`. Notice the branching factor shrinking as you go down — three, then two, then
one. That shrinking is the difference from yesterday.

```
                             build(), current = []
                    /                  |                  \
                 take 1             take 2              take 3
                  /                    |                    \
           current=[1]            current=[2]           current=[3]
            /      \               /      \              /      \
        take 2   take 3        take 1   take 3       take 1   take 2
          /          \           /          \          /          \
      [1,2]        [1,3]      [2,1]       [2,3]     [3,1]       [3,2]
        |            |          |           |         |           |
      take 3       take 2     take 3      take 1    take 2      take 1
        |            |          |           |         |           |
    [1,2,3]      [1,3,2]    [2,1,3]     [2,3,1]   [3,1,2]     [3,2,1]

 6 leaves = 3!            depth = 3 = n
 branching: 3 at the top, 2 in the middle, 1 at the bottom  ->  3 × 2 × 1
```

What to notice: **subsets branched two ways at every level; permutations branch `n` ways at the top and
one way at the bottom.** Same depth, different width, and the width is what makes `n!` bigger than
`2ⁿ`.

The swap version, traced. The bar marks the boundary: fixed on the left, still available on the right.

```
 items = [1, 2, 3]

 first=0   [ | 1  2  3 ]     three choices: swap position 0 with 0, 1, or 2

   swap(0,0)  [ 1 | 2  3 ]   -> first=1
       swap(1,1)  [ 1  2 | 3 ]  -> [1,2,3]   LEAF
       swap(1,2)  [ 1  3 | 2 ]  -> [1,3,2]   LEAF
       swap(1,2)  [ 1  2  3 ]   undo, back to how it was
   swap(0,0)  [ 1  2  3 ]       undo

   swap(0,1)  [ 2 | 1  3 ]   -> first=1
       ...        [2,1,3], [2,3,1]
   swap(0,1)  [ 1  2  3 ]       undo — the line is exactly as it started

   swap(0,2)  [ 3 | 2  1 ]   -> [3,2,1], [3,1,2]
   swap(0,2)  [ 1  2  3 ]       undo

 The array is back to [1, 2, 3] at the end. Every child returned to their spot.
```

And the duplicate rule, which is the fiddly part:

```
 items = [1a, 1b, 2]   (the letters are only for us; the code cannot tell them apart)

 at the top level, position 0:
   place 1a   ->  used = [T, F, F]                      allowed
   place 1b   ->  items[1]==items[0] and used[0] is F   SKIP
                  (this branch would be identical to the 1a branch)
   place 2    ->  different value                       allowed

 one level down, having placed 1a:
   place 1b   ->  items[1]==items[0] and used[0] is T   ALLOWED
                  (the twin is already in the line, so this is
                   "the second 1 following the first", not a repeat branch)

 rule in one sentence: among equal elements, use them LEFT TO RIGHT.
```

---

## 5. The code, built step by step

### Step 1 — say the size before writing anything

"There are `n!` permutations, so the output alone is factorial and no algorithm can be faster. At n = 10
that is 3.6 million, which is fine. At n = 13 it is 6 billion, which is not. So I am expecting a small
`n`."

Thirty seconds, and it removes "can you do better?" from the conversation.

### Step 2 — say why yesterday's `start` is gone

```python
    for i in range(start, len(items)):          # subsets: never look backwards
    for i in range(len(items)):                 # permutations: look everywhere
```

"For subsets, `[1,2]` and `[2,1]` are the same answer, so I only look forward. For permutations they
are different answers, so I have to look at every element every time — which means I need to know which
ones are already placed."

That sentence is the whole design decision, and saying it out loud is worth more than the code.

### Step 3 — the `used` list, and the two un-chooses

```python
        used[i] = True
        current.append(items[i])
        build()
        current.pop()
        used[i] = False
```

Five lines: choose twice, recurse, un-choose twice. **Write them as one block, always.** The two
un-chooses mirror the two chooses in reverse order. It is a habit rather than a rule, and the habit is
what stops you forgetting one under pressure.

### Step 4 — the base case, and the copy

```python
        if len(current) == len(items):
            result.append(current[:])       # COPY. Say the word as you type it.
            return
```

Same copy trap as [day 091](../day-091-subsets/README.md), same silent failure. `current` is one list
mutated all the way through; appending it stores a reference, and every reference points at the same
list, which is empty by the end.

The base case here is `len(current) == len(items)` rather than an index reaching the end, because there
is no index walking to the end — you are not traversing the input in order.

### Step 5 — the swap version, if they ask for less space

```python
        for i in range(first, len(items)):
            items[first], items[i] = items[i], items[first]
            build(first + 1)
            items[first], items[i] = items[i], items[first]
```

The loop starts at `first`, and the first iteration swaps a position with itself — that is the "leave
this one where it is" branch, and it is not a wasted step.

**The second swap is mandatory.** Without it the input is scrambled for the next iteration and you
produce a mixture of wrong orderings, silently.

### Step 6 — duplicates, the hardest line in the phase

```python
        if i > 0 and items[i] == items[i - 1] and not used[i - 1]:
            continue
```

With `items.sort()` first. Say the meaning out loud rather than memorising the symbols: **"skip a
duplicate whose identical twin has not been placed yet."** Equivalently: among equal elements, use them
left to right.

### The complete solution

```python
import math
from itertools import permutations as itertools_permutations


def permutations(items: list[int]) -> list[list[int]]:
    """Every ordering, via a used-list. The version to write in an interview.

    n! permutations, so the output alone is factorial — nothing can beat it.
    Branching is n at the top, n-1 next, down to 1: n × (n-1) × ... × 1.

    TWO things are chosen and TWO must be un-chosen. That symmetry is the
    discipline of the whole phase.
    """
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def build() -> None:
        if len(current) == len(items):
            result.append(current[:])       # COPY — current is one mutating list
            return
        for i in range(len(items)):         # every element, not range(start, n)
            if used[i]:
                continue
            used[i] = True                  # choose
            current.append(items[i])        # choose
            build()                         # recurse
            current.pop()                   # un-choose
            used[i] = False                 # un-choose

    build()
    return result


def permutations_swap(items: list[int]) -> list[list[int]]:
    """The in-place version: no used-list, no working list, O(n) stack only.

    Everything before `first` is fixed; everything from `first` on is still
    available. Swapping i into position `first` says "this one goes next".
    The second swap puts it back, exactly where it came from.

    Cannot handle duplicates — see permutations_unique for why.
    """
    result: list[list[int]] = []

    def build(first: int) -> None:
        if first == len(items):
            result.append(items[:])         # COPY of the array as it stands
            return
        for i in range(first, len(items)):
            items[first], items[i] = items[i], items[first]      # choose
            build(first + 1)                                     # recurse
            items[first], items[i] = items[i], items[first]      # un-choose

    build(0)
    return result


def permutations_unique(items: list[int]) -> list[list[int]]:
    """Permutations II. Two changes from the plain version.

    1. SORT, so equal elements are adjacent.
    2. Skip a duplicate whose identical twin has NOT been placed yet:
       `not used[i - 1]`. Among equal elements, use them LEFT TO RIGHT.

    This is NOT yesterday's `i > start` condition. Different tree shape,
    same job: do not re-explore a branch already explored at this level.
    """
    items = sorted(items)
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def build() -> None:
        if len(current) == len(items):
            result.append(current[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            if i > 0 and items[i] == items[i - 1] and not used[i - 1]:
                continue                    # twin still unused: repeat branch
            used[i] = True
            current.append(items[i])
            build()
            current.pop()
            used[i] = False

    build()
    return result


def permutations_of_length(items: list[int], k: int) -> list[list[int]]:
    """Orderings of exactly k elements out of n — "partial permutations".

    Only the base case changes: stop at k rather than at n. The count is
    n × (n-1) × ... × (n-k+1), which is n! / (n-k)!.
    """
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def build() -> None:
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            used[i] = True
            current.append(items[i])
            build()
            current.pop()
            used[i] = False

    build()
    return result


def permutations_broken_no_unmark(items: list[int]) -> list[list[int]]:
    """The trap, written out so you can run it: `used[i]` is never reset.
    Elements are consumed permanently, so every branch after the first
    dead-ends without ever reaching the base case."""
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def build() -> None:
        if len(current) == len(items):
            result.append(current[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            used[i] = True
            current.append(items[i])
            build()
            current.pop()
            # missing: used[i] = False

    build()
    return result


if __name__ == "__main__":
    print(permutations([1, 2, 3]))
    # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    print(len(permutations([1, 2, 3, 4])), "==", 4 * 3 * 2 * 1)     # 24 == 24
    print(permutations([]), permutations([7]))                      # [[]] [[7]]

    print(sorted(permutations_swap([1, 2, 3])) == sorted(permutations([1, 2, 3])))   # True

    print(permutations_unique([1, 1, 2]))
    # [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    print(len(permutations_unique([1, 1, 2])), "distinct, vs", 3 * 2 * 1, "paths")
    # 3 distinct, vs 6 paths

    print(permutations_of_length([1, 2, 3], 2))
    # [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

    print(permutations_broken_no_unmark([1, 2, 3]))
    # [[1, 2, 3]]        <- one answer instead of six

    print([list(t) for t in itertools_permutations([1, 1, 2])])
    # [[1, 1, 2], [1, 2, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 1, 1]]
    #  ^ six tuples, three distinct: itertools does NOT de-duplicate

    for n in (8, 10, 12, 13):
        print(f"n = {n}: {math.factorial(n):,} permutations")
```

---

## 6. What it costs

### Time

```
 permutations produced:   n!
 length of each:          n
 copying them out:        n! × n
 -> O(n × n!) total work
```

The `n!` is the number of answers; the `n` is the cost of copying each one into the result. **You cannot
beat `n!` because the output is `n!` things.**

There is a second `n` hiding in the `used` version — the loop scans all `n` elements at every node, even
though most are already used. That does not change the big-O, because the copy already costs `n`, but
it is worth being able to say why the two versions are the same complexity.

```
 n = 8:   40,320 permutations,      ~320,000 elements written
 n = 10:  3,628,800,               ~36,000,000 elements       — a few seconds
 n = 11:  39,916,800,             ~440,000,000                — a minute or more
 n = 12:  479,001,600                                         — minutes
 n = 13:  6,227,020,800                                       — not going to finish
```

**Ten is comfortable, eleven is painful, thirteen is impossible.** Compare with subsets, where twenty
was comfortable:

```
 n     2^n (subsets)        n! (permutations)
 ---   ------------------   -----------------------
  5    32                   120
 10    1,024                3,628,800
 15    32,768               1,307,674,368,000
 20    1,048,576            2,432,902,008,176,640,000
```

At n = 20 subsets is a million and permutations is 2.4 quintillion. **`n!` overtakes `2ⁿ` at n = 4 and
never looks back.** That gap is why a permutations problem always has a smaller bound than a subsets
problem, and noticing the bound is how you know which one is wanted.

### Calls versus depth

```
 tree nodes:   1 + n + n(n-1) + ... ≈ e × n!     n = 10 -> ~9.9 million calls
 depth:        n                                  n = 10 -> 10 frames
```

Ten million calls, ten stack frames. Time is the whole tree; space is the deepest path — the
[day 088](../day-088-the-call-stack/README.md) distinction again, and the reason permutations never
hits the recursion limit however slow it gets.

### Space

```
 output:    n! lists of length n         ->  O(n × n!)   — unavoidable
 current:   one list of at most n        ->  O(n)
 used:      n booleans                   ->  O(n)
 stack:     n frames                     ->  O(n)
 -----------------------------------------------------------
 extra space beyond the output:  O(n)
```

**The extra space is O(n), not O(n!).** Say the two separately. The swap version drops `current` and
`used` and is O(n) for the stack alone — genuinely less memory, and the honest reason to prefer it if
someone asks for the in-place solution.

```
 n = 10, integers:  3,628,800 lists × ~136 B  ≈  490 MB just for the result
```

Which is why real code that needs permutations *yields* them one at a time rather than building the
whole list. If the interviewer says "for each permutation, check something", say "I would make this a
generator so we never hold `n!` lists in memory at once".

### Duplicates

```
 [1, 1, 2]:      3! = 6 paths,  3 distinct
 [1, 1, 1]:      6 paths,       1 distinct
 [1, 1, 2, 2]:  4! = 24 paths,  6 distinct       (24 / (2! × 2!))
```

The general count is `n!` divided by the factorial of each group size. The skip prunes the repeated
branches **before** walking them, which is the point: filtering a list of `n!` results afterwards costs
the full `n!` in time and memory, and also requires the results to be hashable — `set(list_of_lists)`
does not even run.

---

## 7. The traps

### Trap 1 — appending the list instead of a copy

```python
        result.append(current)              # a REFERENCE to one mutating list
```

```
 permutations([1, 2, 3])  ->  [[], [], [], [], [], []]
```

Six results, all the same object, all empty, no error. Identical to yesterday's trap and just as
silent. `current[:]`.

In the swap version the same trap wears a different coat: `result.append(items)` appends the input list
itself, and since the recursion restores it, every entry reads `[1, 2, 3]`.

### Trap 2 — forgetting `used[i] = False`

```python
            used[i] = True
            current.append(items[i])
            build()
            current.pop()
                                            # missing: used[i] = False
```

```
 permutations([1, 2, 3])  ->  [[1, 2, 3]]
```

One answer instead of six. Every element is consumed permanently, so after the first full line is
built, nothing is available to anyone and every other branch dead-ends without reaching the base case.

**Two chooses need two un-chooses.** The `pop` on its own is not enough here, and this is the specific
thing that changes from subsets.

### Trap 3 — the swap version with duplicates

```python
    permutations_swap([1, 1, 2])
    # [[1, 1, 2], [1, 2, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 1, 1]]
```

Six answers, three distinct. And the fix that works for the `used` version **cannot be applied here**,
because swapping destroys the sorted order — after one swap, equal elements are no longer adjacent, so
"compare with the previous element" is meaningless.

The usual patch is a per-level `set` of values already tried:

```python
        seen = set()
        for i in range(first, len(items)):
            if items[i] in seen:
                continue
            seen.add(items[i])
```

That works, and it costs a set per node. **If the input has duplicates, use the `used` version.** Say
that out loud rather than trying to rescue the swap version under time pressure.

### Trap 4 — using yesterday's duplicate condition

```python
            if i > 0 and items[i] == items[i - 1]:
                continue                    # subsets' rule, wrong here
```

Missing `and not used[i - 1]`. This skips the second `1` *always*, including when it should legitimately
follow the first one inside a line. The branch that would place both `1`s can never complete, so the
base case is never reached down that path.

Test it on `[1, 1]`. The right answer is `[[1, 1]]` — one permutation. The wrong condition gives `[]`.

### Trap 5 — forgetting to sort first

```python
    # items = [2, 1, 1]  — not sorted
            if i > 0 and items[i] == items[i - 1] and not used[i - 1]:
```

The rule compares **adjacent** elements, so equal values must be adjacent. Unsorted, the check finds
nothing to skip and duplicates come out anyway. `sorted(items)` first, every time.

### Trap 6 — trying to de-duplicate with a set

```python
    >>> set(permutations([1, 1, 2]))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unhashable type: 'list'
```

Lists are not hashable, so you cannot put them in a set. The workaround is `{tuple(p) for p in ...}`,
which does run — and which builds all `n!` results first. On `[1] * 11` that is forty million lines
generated to return one. **Prune in the tree; never filter the result.**

### Trap 7 — mutating the caller's list

The swap version rearranges the list it was given. It puts everything back by the end, so the caller
usually never notices — but if the recursion raises part-way through, or you return early from inside
it, the caller's list is left scrambled. If that matters, copy the input once at the top:
`items = items[:]`.

### Trap 8 — saying "2ⁿ" when they asked for permutations

Under pressure, people say "exponential" for both. `n!` is not exponential; it is worse. Saying "2ⁿ" for
permutations tells the interviewer you have pattern-matched rather than counted. **Count it out loud:
`n` choices, then `n − 1`, then `n − 2`.**

---

## 8. In the interview

### How it gets asked

- The base: *"Generate all permutations of this array."* LeetCode 46.
- Immediately after: *"Now the array can contain duplicates and the permutations must be unique."*
  LeetCode 47.
- The memory probe: *"Can you do it without the extra `used` array?"* — they want the swap version.
- The scale probe: *"What if n is 12? What if n is 20?"*
- The disguise: *"Find all valid arrangements such that…"* — Beautiful Arrangement, LeetCode 526, which
  is permutations with a check before recursing.

### What to say out loud, in the first ninety seconds

1. **Count the size, do not name it.** "At the first position there are `n` choices, then `n − 1`, then
   `n − 2` — so `n!` permutations. The output alone is factorial, so nothing can beat it. n = 10 is 3.6
   million and fine; n = 13 is 6 billion and not."
2. **Say what changes from subsets.** "For subsets I walked forward with a `start` index because
   `[1,2]` and `[2,1]` are the same answer. Here they are different answers, so I have to consider
   every element at every position — which means tracking which ones are already placed."
3. **Pick the representation and justify it.** "I will keep a boolean per element. There is also an
   in-place swap version that needs no extra array, and I will mention it, but the boolean version
   handles duplicates cleanly and that is usually the follow-up."
4. **Say the symmetry.** "Choose, choose, recurse, un-choose, un-choose. Two things are marked and both
   have to be unmarked. Forgetting `used[i] = False` gives one permutation instead of `n!`, with no
   error."
5. **Flag the copy before writing it.** "I append a copy when the line is complete, because `current` is
   one list being mutated throughout."
6. **Give both complexities separately.** "O(n × n!) time — `n!` answers, each costing `n` to copy — and
   O(n) extra space beyond the output: one working list, `n` booleans, `n` stack frames."

### The follow-ups

**"What is the complexity?"**
"O(n × n!). There are `n!` permutations and writing each one out costs `n`. And no, you cannot do
better, because the output itself is `n!` things — any correct solution has to produce all of them.
Extra space beyond the output is O(n): the working list, the `used` array and `n` stack frames. Worth
separating, because at n = 10 the tree has roughly ten million calls and the stack never exceeds ten
frames."

**"Now handle duplicates."**
"Two changes. Sort the input so equal elements are adjacent. Then, before placing element `i`, skip it
if it equals the previous element **and the previous element is not currently used**. The meaning is:
among identical elements, always place them left to right. If I let the second `1` go first while the
first `1` is still sitting unused, I am starting a branch identical to one I have already walked. Note
this is *not* the `i > start` rule from subsets — different tree shape, same job. And it prunes rather
than filters: filtering afterwards would build all `n!` results, and you cannot even put lists in a
set, so you would have to convert to tuples first."

**"Can you avoid the extra `used` array?"**
"Yes — swap in place. At depth `first`, everything before `first` is fixed and everything from `first`
on is available. Loop `i` from `first`, swap `i` into position `first`, recurse on `first + 1`, then
swap back. The swap back is essential; without it the array is scrambled for the next iteration. That
gets extra space down to just the O(n) stack. The catch is duplicates: swapping destroys sorted order,
so the adjacency rule stops working, and you need a per-level set of values already tried instead. If
duplicates are in scope I would use the `used` version and say why."

**"What if n is 20?"**
"Then generating all permutations is not the question, because 20! is 2.4 quintillion — you would not
finish this century. If someone asks about permutations at n = 20 they want something else: a *count*,
which is arithmetic and needs no enumeration; or the *k-th* permutation in order, which you build one
position at a time using factorials and never enumerate; or a *best* permutation under some criterion,
which is usually bitmask dynamic programming — 2ⁿ × n states rather than n!, and at n = 20 that is
about twenty million, which is fine."

**"What about permutations of a string with repeated characters?"**
"Same problem. Sort the characters, use the `used`-with-`not used[i-1]` rule, and join at the end. The
count is `n!` divided by the factorial of each character's frequency — `'aab'` has 3!/2! = 3."

**"Would you actually use your own implementation?"**
"In production, no — `itertools.permutations` is C and it is a generator, so it does not hold `n!`
results in memory. Two things to know about it: it yields tuples, not lists, and it does **not**
de-duplicate, so `permutations([1,1,2])` gives six tuples with repeats. In an interview I write the
recursive one, because the question is about the tree."

### A model answer

Asked: *generate all permutations of this array.*

> "Let me count the size first, because it decides everything. The first position can hold any of the
> `n` elements. Once that is fixed, the second position can hold any of the `n − 1` that are left, then
> `n − 2`, and so on. So there are `n!` permutations. That is not a bound I can improve on — **the
> output is `n!` things**, so any correct solution has to write them all out. Practically that means n =
> 10 is 3.6 million and fine, and n = 13 is 6 billion and hopeless, so I am assuming a small `n`.
>
> The important difference from subsets is this. For subsets I walked the array forward with a `start`
> index, because `[1,2]` and `[2,1]` are the *same* subset and looking backwards would only repeat
> myself. Here they are **different** answers, so I have to consider every element at every position.
> `start` is gone, and I need something else to tell me which elements are already in the arrangement.
>
> I will keep one boolean per element. At each level I loop over all `n` elements, skip the ones already
> marked used, and for the rest: mark it used, append it, recurse, pop it, unmark it. **Two things are
> chosen and both have to be un-chosen** — that symmetry is the discipline of the whole pattern. If I
> forget the unmark, elements are consumed permanently and I get exactly one permutation instead of
> `n!`, with no error at all.
>
> When the working list reaches full length, I record a **copy**. `current` is a single list being
> mutated throughout, so appending it directly would store `n!` references to one list that is empty at
> the end.
>
> Complexity is O(n × n!) time — `n!` answers, `n` to copy each — and O(n) extra space beyond the
> output: the working list, the booleans, and `n` stack frames. Worth separating those, because at n =
> 10 the tree has about ten million calls and the stack never goes past ten deep.
>
> If you want it without the extra array, there is an in-place version: at depth `first`, swap each
> candidate into position `first`, recurse, and swap it back. It is the same tree, and the swap-back is
> the un-choose. I would still write the boolean version first, because if you then tell me the input
> has duplicates, the boolean version takes two clean lines — sort, and skip a duplicate whose identical
> twin is still unused — whereas the swap version breaks, because swapping destroys the sorted order
> that rule depends on."

---

## 9. Recall card

- **`n` choices, then `n − 1`, then `n − 2` — so `n!` permutations, and you cannot beat `n!` because the
  output *is* `n!` things.** Count it out loud; never say "exponential", because **`n!` is worse than
  `2ⁿ` and overtakes it at n = 4**. n = 10 is 3.6 million and fine; **n = 13 is 6 billion and
  impossible**, so the bound in the question tells you which of the two is wanted.
- **`start` does not work here.** For subsets `[1,2]` and `[2,1]` are the same answer; for permutations
  they are different, so you look at every element every time and must track **which are already
  placed** — a `used` boolean per element.
- **Two chooses, two un-chooses: `used[i] = True`, append, recurse, pop, `used[i] = False`.** Forgetting
  the unmark gives **one permutation instead of `n!`**, silently. And append `current[:]` — a **copy** —
  or you get `n!` references to one empty list.
- **Duplicates: sort, then skip when `items[i] == items[i-1]` AND `not used[i-1]`** — meaning *"my
  identical twin has not been placed yet, so this branch is a repeat"*. In one sentence: **among equal
  elements, place them left to right.** This is **not** subsets' `i > start`. Prune, never filter —
  `set(list_of_lists)` raises `TypeError: unhashable type: 'list'`.
- **The swap version needs no `used` array**: fix positions left to right, swap `i` into `first`,
  recurse, **swap back**. O(n) space total. But it **cannot use the adjacency rule for duplicates**,
  because swapping destroys sorted order — use a per-level `set`, or use the `used` version. And
  `itertools.permutations` exists, yields **tuples**, and does **not** de-duplicate.
