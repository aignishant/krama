---
day: 12
track: dsa
title: "Searching an array: linear search, done properly"
phase: "Arrays"
status: written
---

# Day 012 · DSA — Searching an array: linear search, done properly

**After today you can:** You can write a search that handles not-found, duplicates and empty input correctly.

**The interviewer asks it as:** *Find the index of a target. What do you return if it is not there?*

---

## 1. What this is, and why they ask it

**Linear search** is looking at each element in turn until you find what you want or run out.
It is four lines of code, it works on any array in any order, and it is `O(n)`.

The four lines are not the point. The point is everything around them: what you return when
the value is absent, which position you return when the value appears three times, what
happens on an empty array, and why "I return 0" is a bug rather than a choice.

Interviewers ask this as an opener, and they ask the second half — *"what do you return if it
is not there?"* — because it is the smallest possible test of whether you think about
contracts. A candidate who writes the loop and stops has written half a function. A candidate
who says "I'd return −1 by convention, but I'd check with you, because if the array can
contain −1 as a value that gets confusing, and in Python I'd prefer None" has demonstrated the
habit from [day 008](../day-008-reading-a-problem/README.md) on a problem small enough that
there is nowhere to hide.

---

## 2. The story

Ilyas is on the gate at a hospital car park in Kozhikode. Six rows, thirty spaces to a row,
and by eleven in the morning on a weekday every one of them is taken.

At about half past eleven a woman comes to his cabin. Her father is being discharged, her
brother parked the car at seven and has now gone to fetch the medicines, and she has no idea
where in the car park it is. She gives him the number plate and the fact that it is a grey
Ertiga.

So Ilyas walks. He starts at the first space in row A and goes along, looking at each plate.
Grey Ertigas are common enough that he checks the whole number, not just the first few
characters, because there is a grey Ertiga in row B whose plate differs from hers in one
digit and he has been caught by that before. He finds it in row C, the fourteenth space —
about the seventieth car he has looked at. Eight minutes.

The other kind of afternoon is the one that sticks with him. Three weeks ago a man asked him
to find a car and Ilyas walked the whole thing — all six rows, all hundred and eighty spaces —
and it was not there. It had been towed at nine that morning from outside the blood bank. And
the thing about that walk is that it was the **longest possible** walk. Finding a car can be
quick if it happens to be near the entrance. Being certain a car is *not* there takes every
single space, every single time. There is no shortcut for absence.

Then there is what he actually says when he gets back. He cannot say "row A, space one",
because there is a row A and there is a space one and she would go and stand there. He has to
say something that is not a place at all — "it's not in the car park" — and that is a
different kind of answer to the question he was asked.

Not every question wants one car, either. The Sunday before, a woman from the ward asked him
how many white Swifts were in the car park, because someone had left their lights on and she
wanted to warn them. That is not "find me the car". That is "find me all of them", and he came
back with nine spaces rather than one. Same walk, different answer.

And at four in the morning, when the last relative has gone home and the car park is empty,
somebody occasionally asks him about a car anyway. That walk takes no time at all, and the
answer is still "it's not here".

---

## 3. The idea in plain English

Ilyas walking the rows is linear search, and the four things he ran into are the four things
the code has to get right.

### The search itself

```python
def find(items: list[int], target: int) -> int:
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1
```

Walk from the start. Compare each element to the target. **Return the moment you find it** —
that is the early exit, and it is what makes the best case one step. If the loop finishes
without returning, the value is not there.

That last `return -1` is outside the loop. Getting it inside the loop is a real and common
bug, and it makes the function report "not found" after checking only the first element.

### What "not found" should be

Ilyas cannot say "row A, space one". You cannot return `0`, because `0` is a perfectly good
index — it means "the first element". Something that is not an index is needed.

| Convention | When to use it |
|---|---|
| `-1` | The universal convention across C, Java, JavaScript, and most interview answers. Not a valid index, so unambiguous. |
| `None` | The Pythonic choice, and unambiguous even if `-1` appears in the data. |
| Raise an exception | What `list.index()` does. Right when absence is genuinely exceptional; wrong when it is expected. |

**`-1` is the safe answer in an interview, and asking is the better one.** "I'll return −1
unless you'd prefer None — is not-found an expected case or an error case?" takes four seconds
and is exactly the behaviour [day 008](../day-008-reading-a-problem/README.md) described.

There is one genuine trap in `-1`, and it is worth naming: **in Python, `-1` is a valid index**
that means the last element. So a caller that does `items[find(items, x)]` without checking
will silently read the last element when the value is absent, instead of failing. That alone
is a decent argument for `None` in Python.

### Duplicates: which one do you want?

Ilyas found one grey Ertiga; the woman on Sunday wanted all nine white Swifts. Same walk,
three possible contracts:

**First occurrence** — return as soon as you match. This is the default and the cheapest,
because it exits early.

**Last occurrence** — either walk backwards, or walk forwards and keep overwriting a
remembered index. Walking backwards can exit early; walking forwards cannot.

**All occurrences** — collect them into a list. No early exit is possible, so this is always
`n` comparisons.

The problem statement usually does not say which. **Ask.**

### The empty array

`range(0)` produces nothing, the loop body never runs, and the function falls through to
`return -1`. Correct, with no special case needed — which is what a well-derived bound looks
like, from [day 010](../day-010-traversal-patterns/README.md).

That is worth checking rather than assuming, because the near-miss versions do need a guard.
A function that starts with `best = items[0]` raises `IndexError` on an empty list, and a
function that returns `items[found]` at the end has the same problem.

### What it costs, and why absence is the worst case

| Case | Comparisons | When |
|---|---|---|
| Best | 1 | the target is first |
| Average (present) | `n / 2` | uniformly likely positions |
| Worst | `n` | the target is last, **or not there at all** |

**Absence is always the worst case.** There is no way to be sure something is missing without
looking everywhere. That single sentence answers a surprising number of follow-up questions,
and it is why the "not found" path is the one worth reasoning about.

The complexity is `O(n)` time and `O(1)` extra space.

### When linear search is the right answer

It is not a placeholder for something better. It is correct when:

- **The data is unsorted** and you are searching once. Sorting to enable binary search costs
  `O(n log n)`, which is worse than a single `O(n)` scan.
- **`n` is small.** Below a few dozen elements, a linear scan often beats anything cleverer
  because of constant factors and cache behaviour.
- **You are searching by a condition**, not by equality — "the first element greater than the
  running average" cannot be binary-searched.
- **The data is a linked list or a stream**, where random access does not exist.

And it is the wrong answer when you will search **many times** over the same data. Then you
pay once to prepare and search cheaply thereafter:

```
search once     : linear O(n) wins
search k times  : sort O(n log n) + k x O(log n)   -- day 042
                  or build a hash set O(n) + k x O(1)   -- day 060
```

The break-even is done with real numbers in §6.

### The built-ins, and what they cost

```python
target in items        # O(n), returns True/False
items.index(target)    # O(n), returns the index, RAISES if absent
items.count(target)    # O(n), counts all occurrences
```

All three are linear search written in C, so they run several times faster than your Python
loop and have exactly the same complexity. `items.index()` is the one to be careful
with, because its failure mode is an exception rather than a value — §7 shows what that looks
like.

---

## 4. The picture

The walk, on a seven-element array, looking for 13:

```
   index      0     1     2     3     4     5     6
           +-----+-----+-----+-----+-----+-----+-----+
   value   |  2  |  9  |  5  | 13  |  7  | 13  |  4  |
           +-----+-----+-----+-----+-----+-----+-----+
              ^
            i=0: 2 == 13?  no
                    ^
                  i=1: 9 == 13?  no
                          ^
                        i=2: 5 == 13?  no
                                ^
                              i=3: 13 == 13?  YES -> return 3

   4 comparisons. Stops immediately. Never sees index 4, 5 or 6.
```

**What to notice:** the loop stops at the first match, so the second 13 at index 5 is never
examined. That is correct for "first occurrence" and wrong for "all occurrences", and nothing
in the code says which one you meant.

Now the same array, looking for 8:

```
   index      0     1     2     3     4     5     6
           +-----+-----+-----+-----+-----+-----+-----+
   value   |  2  |  9  |  5  | 13  |  7  | 13  |  4  |
           +-----+-----+-----+-----+-----+-----+-----+
              ^     ^     ^     ^     ^     ^     ^
              no    no    no    no    no    no    no

   7 comparisons, then return -1.
   To be sure it is ABSENT you must look at every single one.
```

**What to notice:** absence costs the full `n`. There is no early exit for "not there", and
there never can be without extra structure.

The three contracts, side by side:

```
   value   |  2  |  9  |  5  | 13  |  7  | 13  |  4  |    target = 13
   index      0     1     2     3     4     5     6

   first    ------------------>|                          returns 3, 4 comparisons
   last                        |----------->|             returns 5, 7 comparisons forwards
                                                                     (or 2 backwards)
   all      ---------------------------------------->     returns [3, 5], 7 comparisons
```

**What to notice:** three different correct answers to "find 13". The problem statement decides
which, and if it does not say, you ask.

And the cost curve, which is the thing to have in mind when comparing with binary search:

```
  comparisons
     n |                                        * linear (worst / absent)
       |                                   *
   n/2 |                              *              linear (average, present)
       |                         *
       |                    *
       |               *
       |          *
       |     *
 log n |*  *  *  *  *  *  *  *  *  *  *  *  *  *  binary search (day 042)
       +--------------------------------------> n

   at n = 1,000,000:  linear = 1,000,000 comparisons
                      binary =        20 comparisons
```

**What to notice:** the gap is enormous and it costs `O(n log n)` to unlock. That is why
"should I sort first?" is a question about **how many times you will search**, not about how
big the array is.

---

## 5. The code, built step by step

Build the four contracts, then a table of edge cases, because the edge cases are the lesson.

The basic search, returning `-1`.

```python
def find_first(items: list[int], target: int) -> int:
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1
```

`enumerate` rather than `range(len(items))`, from
[day 010](../day-010-traversal-patterns/README.md) — shorter, faster, and one fewer thing to
get wrong. The `return -1` sits **outside** the loop, which is the whole correctness of the
function.

The Pythonic version, returning `None`.

```python
def find_first_or_none(items: list[int], target: int) -> int | None:
    for i, x in enumerate(items):
        if x == target:
            return i
    return None
```

`int | None` in the signature is the honest type. A caller now has to check before using the
result, which is exactly what you want, and `None` cannot be mistaken for a valid index the
way `-1` can in Python.

The last occurrence, walking backwards so it can still exit early.

```python
def find_last(items: list[int], target: int) -> int:
    for i in range(len(items) - 1, -1, -1):
        if items[i] == target:
            return i
    return -1
```

`range(n - 1, -1, -1)` — stop-before `−1`, so index 0 is included. Getting that second
argument wrong silently misses the first element.

All occurrences, which cannot exit early.

```python
def find_all(items: list[int], target: int) -> list[int]:
    return [i for i, x in enumerate(items) if x == target]
```

Always `n` comparisons, and `O(k)` extra space for the `k` matches.

Search by a condition rather than by equality — the version binary search cannot do.

```python
def find_where(items: list[int], predicate) -> int:
    for i, x in enumerate(items):
        if predicate(x):
            return i
    return -1
```

`predicate` is a function returning `True` or `False`. `find_where(items, lambda x: x > 100)`
finds the first element over 100. This generality is a real reason linear search survives.

And the built-in, with its failure mode made safe.

```python
def find_with_builtin(items: list[int], target: int) -> int:
    try:
        return items.index(target)
    except ValueError:
        return -1
```

`items.index()` is the same `O(n)` scan implemented in C, so it is much faster in practice. It
raises when absent, so it must be wrapped if absence is expected.

Here is the complete program.

```python
"""Day 12 — linear search, and the four things around it that actually matter."""

import time
from collections.abc import Callable


def find_first(items: list[int], target: int) -> int:
    """First occurrence, or -1. O(n) time, O(1) space."""
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1                      # OUTSIDE the loop. This is the whole function.


def find_first_or_none(items: list[int], target: int) -> int | None:
    """The Pythonic contract: None cannot be mistaken for an index."""
    for i, x in enumerate(items):
        if x == target:
            return i
    return None


def find_last(items: list[int], target: int) -> int:
    """Last occurrence. Backwards, so it can still exit early."""
    for i in range(len(items) - 1, -1, -1):
        if items[i] == target:
            return i
    return -1


def find_all(items: list[int], target: int) -> list[int]:
    """Every occurrence. No early exit is possible: always n comparisons."""
    return [i for i, x in enumerate(items) if x == target]


def find_where(items: list[int], predicate: Callable[[int], bool]) -> int:
    """Search by condition — the case binary search cannot handle."""
    for i, x in enumerate(items):
        if predicate(x):
            return i
    return -1


def find_with_builtin(items: list[int], target: int) -> int:
    """Same O(n), written in C, so roughly 30x faster in practice."""
    try:
        return items.index(target)
    except ValueError:
        return -1


def count_comparisons(items: list[int], target: int) -> int:
    """How many elements did we actually look at?"""
    looked = 0
    for x in items:
        looked += 1
        if x == target:
            return looked
    return looked


# The edge cases. Written before the solution, not after it.
CASES: list[tuple[str, list[int], int]] = [
    ("empty array",          [],                    5),
    ("one element, match",   [5],                   5),
    ("one element, no match",[9],                   5),
    ("target is first",      [5, 1, 2, 3],          5),
    ("target is last",       [1, 2, 3, 5],          5),
    ("target absent",        [1, 2, 3, 4],          5),
    ("duplicates",           [1, 5, 2, 5, 3, 5],    5),
    ("all identical",        [5, 5, 5, 5],          5),
    ("negative target",      [1, -5, 2],           -5),
    ("target is zero",       [3, 0, 7],             0),
    ("minus one in data",    [3, -1, 7],           -1),
]

if __name__ == "__main__":
    print(f"{'case':<24}{'array':<20}{'target':>7}{'first':>7}{'last':>7}"
          f"{'all':>10}{'looked':>8}")
    print("-" * 83)
    for name, items, target in CASES:
        print(f"{name:<24}{str(items):<20}{target:>7}"
              f"{find_first(items, target):>7}"
              f"{find_last(items, target):>7}"
              f"{str(find_all(items, target)):>10}"
              f"{count_comparisons(items, target):>8}")

    print("\nwhy 'not found' is the worst case")
    n = 1_000_000
    data = list(range(n))
    for label, target in (("first element", 0),
                          ("middle element", n // 2),
                          ("last element", n - 1),
                          ("absent", -99)):
        print(f"  {label:<16}: {count_comparisons(data, target):>10,} comparisons")

    print("\nsearch by condition (binary search cannot do this)")
    readings = [12, 45, 7, 99, 23, 81, 64]
    i = find_where(readings, lambda x: x > 50)
    print(f"  first reading over 50 in {readings} -> index {i}, value {readings[i]}")

    print("\nyour loop vs the built-in — same O(n), different constant")
    t0 = time.perf_counter(); find_first(data, -99);       mine = time.perf_counter() - t0
    t0 = time.perf_counter(); find_with_builtin(data, -99); builtin = time.perf_counter() - t0
    print(f"  find_first (Python loop) : {mine:>8.4f} s")
    print(f"  list.index (C)           : {builtin:>8.4f} s   -> {mine / builtin:.0f}x faster")

    print("\nis it worth sorting first? (day 042 territory)")
    for searches in (1, 10, 1_000, 100_000):
        linear = searches * n
        prepared = n * 20 + searches * 20          # n log n to sort, log n per search
        winner = "linear" if linear < prepared else "sort + binary search"
        print(f"  {searches:>7,} searches over {n:,}: "
              f"linear {linear:>14,} vs sorted {prepared:>14,}  -> {winner}")
```

This is exactly what it printed:

```
case                    array                target  first   last       all  looked
-----------------------------------------------------------------------------------
empty array             []                        5     -1     -1        []       0
one element, match      [5]                       5      0      0       [0]       1
one element, no match   [9]                       5     -1     -1        []       1
target is first         [5, 1, 2, 3]              5      0      0       [0]       1
target is last          [1, 2, 3, 5]              5      3      3       [3]       4
target absent           [1, 2, 3, 4]              5     -1     -1        []       4
duplicates              [1, 5, 2, 5, 3, 5]        5      1      5 [1, 3, 5]       2
all identical           [5, 5, 5, 5]              5      0      3[0, 1, 2, 3]       1
negative target         [1, -5, 2]               -5      1      1       [1]       2
target is zero          [3, 0, 7]                 0      1      1       [1]       2
minus one in data       [3, -1, 7]               -1      1      1       [1]       2

why 'not found' is the worst case
  first element   :          1 comparisons
  middle element  :    500,001 comparisons
  last element    :  1,000,000 comparisons
  absent          :  1,000,000 comparisons

search by condition (binary search cannot do this)
  first reading over 50 in [12, 45, 7, 99, 23, 81, 64] -> index 3, value 99

your loop vs the built-in — same O(n), different constant
  find_first (Python loop) :   0.1342 s
  list.index (C)           :   0.0226 s   -> 6x faster

is it worth sorting first? (day 042 territory)
        1 searches over 1,000,000: linear      1,000,000 vs sorted     20,000,020  -> linear
       10 searches over 1,000,000: linear     10,000,000 vs sorted     20,000,200  -> linear
    1,000 searches over 1,000,000: linear  1,000,000,000 vs sorted     20,020,000  -> sort + binary search
  100,000 searches over 1,000,000: linear 100,000,000,000 vs sorted     22,000,000  -> sort + binary search
```

**Look at the row `minus one in data`.** The array contains `−1` as a value, and the search for
it correctly returns index 1. But now imagine `find_first` had returned `-1` for "not found"
on a different call — a caller comparing the two results cannot tell them apart by looking at
the data. That is exactly why the return convention is a question, not an assumption.

**Look at the comparison block.** Absent costs the same as last: the full million. There is no
version of this that is faster, and that fact is the reason the whole binary search phase
exists.

**Look at the last block.** One search: scan it. A thousand searches: sort first. The crossover
is not about `n`, it is about how many times you ask.

---

## 6. What it costs

**Time.** One comparison per element, up to `n`:

```
best case    : 1        target is first
average      : n / 2    target present, position uniformly likely
worst case   : n        target last, OR ABSENT
```

`O(n)` in all the ways that matter, and `O(1)` extra space — three variables regardless of
size.

**Why the average is `n/2` when found.** If the target is equally likely to be at any of the
`n` positions:

```
(1 + 2 + 3 + ... + n) / n = (n(n+1)/2) / n = (n+1)/2
```

Just over half, which is the staircase from
[day 002](../day-002-counting-steps/README.md) again. And the constant `1/2` is dropped, so
it is still `O(n)` — which is why an interviewer will not accept "it's O(n/2)".

**Absence has no average.** It is always `n`. Any workload that mostly asks about things that
are not there gets the worst case every single time, and that is a genuinely useful thing to
notice about a real system: a cache lookup that usually misses is paying full price on every
call.

**The break-even against sorting**, done properly. Searching `k` times over an array of
`n = 1,000,000`, where `log₂ n ≈ 20`:

```
linear         : k x n           = k x 1,000,000
sort + binary  : n log n + k log n = 20,000,000 + k x 20
```

Set them equal:

```
k x 1,000,000 = 20,000,000 + 20k
k x 999,980   = 20,000,000
k             = about 20
```

**Twenty searches.** Below that, scan. Above it, sort once. Now the same with a hash set,
which is `O(n)` to build and `O(1)` per lookup:

```
hash set : n + k x 1 = 1,000,000 + k
linear   : k x 1,000,000

break-even at k = about 2
```

**Two searches.** If you are going to look twice and you can afford `O(n)` memory, build a set.
That is the day 006 reflex, and this is the arithmetic behind it.

**The constant factor of the built-in.** `list.index()` is the same algorithm in C:

```
Python loop : 0.1362 s over 1,000,000
list.index  : 0.0220 s over 1,000,000   -> 6x
```

Same `O(n)`, six times faster here and often far more on tighter loops. It never changes
which shape you should choose, and it is free, so use it when the contract fits.

**Cache behaviour.** Linear search reads memory in address order, so it gets the full benefit
of the 64-byte cache line from [day 009](../day-009-what-an-array-is/README.md) — roughly
sixteen 4-byte values per fetch. This is why, for small `n`, a linear scan of a contiguous
array frequently beats a binary search that jumps around, and why real sorting
implementations switch to insertion sort below about 64 elements.

---

## 7. The traps

### Trap one: index 0 is falsy

This one produces a wrong answer with no error at all, and it catches experienced people.

```python
def find(items: list[int], target: int) -> int | None:
    for i, x in enumerate(items):
        if x == target:
            return i
    return None


items = [7, 3, 9]
result = find(items, 7)
if result:                      # <- the bug
    print(f"found at {result}")
else:
    print("not found")
```

```
not found
```

The value **is** at index 0, and the function returned `0` correctly. Then `if result:` treated
`0` as false, because in Python `0`, `None`, `""`, `[]` and `{}` are all falsy. The check
cannot distinguish "found at position 0" from "not found".

The fix is to test against the sentinel explicitly rather than for truthiness:

```python
if result is not None:          # explicit, and correct for index 0
    print(f"found at {result}")
```

And with the `-1` convention:

```python
if result != -1:                # not `if result:`
```

**How to catch it every time:** when a function can return `0`, `False` or an empty container
as a legitimate value, never test the result for truthiness. Test `is not None`, or compare to
the sentinel. This is one of the most common bug classes in Python and it is invisible in code
review unless you are looking for it.

### Trap two: `.index()` raises

The built-in has a failure mode that a hand-written loop does not.

```python
items = [1, 2, 3, 4]
position = items.index(7)
print(position)
```

```
Traceback (most recent call last):
  File "d12.py", line 2, in <module>
    position = items.index(7)
               ~~~~~~~~~~~^^^
ValueError: 7 is not in list
```

`ValueError`, not `IndexError` — the message even quotes the value it was looking for. That is
useful for debugging and fatal in production if you did not expect it.

Two correct fixes. Wrap it:

```python
try:
    position = items.index(7)
except ValueError:
    position = -1
```

Or check first — noting that this costs **two** passes, because `in` is itself an `O(n)` scan:

```python
position = items.index(7) if 7 in items else -1     # O(n) + O(n)
```

For a single lookup the hand-written loop is one pass and is the better answer. For repeated
lookups, neither is right — build a dictionary from value to index once, and look up in
`O(1)`.

### The near-miss worth naming

Putting the `return` in the wrong place:

```python
def find(items: list[int], target: int) -> int:
    for i, x in enumerate(items):
        if x == target:
            return i
        return -1               # <- indented one level too far
```

```python
print(find([7, 3, 9], 3))       # prints -1. The 3 is at index 1.
```

No error. The function checks element 0, does not match, and returns `-1` immediately. It is
correct whenever the target happens to be first, which means it passes the example the
interviewer showed you.

**The `return` for "not found" belongs after the loop has finished**, at the function's
indentation level. When reading a search function, check that line's indentation first — it is
where the bug lives.

---

## 8. In the interview

### How it gets asked

- *"Find the index of a target. What do you return if it isn't there?"* — the direct version.
  The second sentence is the real question.
- *"What if the target appears multiple times?"* — the contract question. First, last, or all?
- *"Can you do better than O(n)?"* — the answer is "not on unsorted data with one search", and
  saying why is the point.
- *"Should you sort first?"* — a question about how many searches, not about `n`.

### What to say out loud, in the first ninety seconds

1. **Ask the contract question before writing.** *"Before I write it — what should I return if
   the target isn't present? I'd default to −1, or None in Python. And if it appears more than
   once, do you want the first, the last, or all of them?"*
2. **State the approach.** *"Assuming first occurrence and −1 for absent: one pass, comparing
   each element, returning the index on the first match."*
3. **Say where the fallback goes.** *"The −1 goes after the loop, not inside it — inside, it
   would bail out after checking the first element."*
4. **Give the three cases.** *"Best case one comparison if it's first. Average n over 2 if it's
   present. Worst case n — and importantly, 'not present' is always the worst case, because
   you can't be sure something's absent without looking at everything."*
5. **Give both complexities.** *"O(n) time, O(1) extra space. Empty array falls out correctly
   with no special case, because the loop just doesn't run."*
6. **Pre-empt "can you do better".** *"If I'm going to search this array many times, I'd pay
   once up front — a hash set makes each lookup O(1), or sorting makes it O(log n). The
   break-even against a hash set is about two searches; against sorting it's around twenty at
   a million elements. For a single search on unsorted data, O(n) is optimal — you have to
   look at every element to rule it out."*

Step 6 is what turns the simplest question in the course into a conversation worth having.

### The follow-ups

**"What do you return if it's not there?"**
`-1` by convention — it is not a valid index in most languages, so it is unambiguous, and it is
what `indexOf` returns in Java and JavaScript. In Python I would lean towards `None`, for a
specific reason: `-1` **is** a valid index in Python, meaning the last element, so a caller who
forgets to check gets the last element instead of an error. The third option is raising, which
is what `list.index()` does, and I would only choose it if absence is genuinely exceptional
rather than expected. Whichever I pick, I would document it and be consistent, and I would ask
rather than assume.

**"Can you do better than O(n)?"**
Not for a single search on unsorted data, and the reason is information-theoretic rather than
about cleverness: any element you have not examined could be the target, so to correctly
return "not found" you must examine all of them. What you can do is change the problem. If I
will search repeatedly, I pay `O(n)` once to build a hash set and then each lookup is `O(1)`,
or `O(n log n)` to sort and then `O(log n)` per lookup. The question is how many searches, not
how big the array is — the break-even against a hash set is about two searches.

**"The array is sorted. Does that change anything?"**
Yes, twice over. Binary search becomes available, taking it to `O(log n)` — 20 comparisons
instead of a million. And even linear search improves for the absent case: you can stop as soon
as you pass a value greater than the target, because everything after it is larger too. That
takes the average for absent targets from `n` to `n/2` while staying `O(n)`. But if the array
is sorted, binary search is the answer, and that is
[day 042](../day-042-binary-search-idea/README.md).

**"When would you actually use linear search?"**
More often than people expect. When the data is unsorted and I am searching once — sorting
first would cost more than the scan. When `n` is small, where constant factors and cache
locality mean a linear scan of contiguous memory beats a binary search that jumps around;
real sort implementations switch to insertion sort below about 64 elements for this reason.
When I am searching by a **condition** rather than by equality — "the first element greater
than the running average" cannot be binary-searched at all. And when the structure has no
random access, like a linked list or a stream.

### A model answer

> "Before I write it, two things. What should I return when the target isn't present? And if
> it appears more than once, do you want the first occurrence, the last, or all of them?
>
> ...Right, first occurrence and −1 for not found.
>
> ```python
> def find(items: list[int], target: int) -> int:
>     for i, x in enumerate(items):
>         if x == target:
>             return i
>     return -1
> ```
>
> One pass, returning the index at the first match. The `return -1` is after the loop, at the
> function's indentation — if it were inside the loop, it would bail out after checking only
> the first element, and that version still passes any example where the target happens to be
> first, so it's an easy bug to miss.
>
> Complexity: O(n) time, O(1) extra space. Best case one comparison, average n over 2 when
> present. Worst case n — and the case worth flagging is that 'not present' is *always* the
> worst case. You can't be certain something is absent without looking at everything, so a
> workload that mostly asks about missing keys pays full price on every call.
>
> The empty array works with no special case: the loop body never runs and it falls through
> to −1.
>
> One note on the −1 convention in Python specifically: −1 is a valid index here, meaning the
> last element. So a caller who does `items[find(items, x)]` without checking gets the last
> element rather than an error. In Python I'd usually return None for that reason, and I'd put
> `int | None` in the signature so the type system makes the caller check.
>
> On doing better — not for a single search on unsorted data, because any element you haven't
> examined could be the target. But if we're searching repeatedly, I'd pay once up front: a
> hash set gives O(1) lookups after an O(n) build, which pays for itself after about two
> searches. Sorting gives O(log n) lookups after O(n log n), which at a million elements pays
> for itself after about twenty. So the question is how many times we search, not how big the
> array is."

That answer opens with the contract question, gets the fallback placement right and explains
why it matters, gives all three cases, names the Python-specific hazard, and finishes with the
break-even arithmetic rather than a vague "use a hash map".

---

## 9. Recall card

1. **Walk, compare, return on the first match, and put the "not found" return AFTER the
   loop.** Inside the loop it bails out after one element.
2. **`-1` by convention, `None` in Python** — because `-1` is a valid index in Python and will
   silently read the last element. Ask which the interviewer wants.
3. **Absence is always the worst case: `n` comparisons.** You cannot be sure something is
   missing without looking everywhere. Best 1, average `n/2`, worst `n`. `O(n)` time, `O(1)`
   space.
4. **Ask about duplicates.** First, last, or all — three different correct answers, and only
   "all" loses the early exit.
5. **Never test the result for truthiness.** `if result:` is false for index 0. Use
   `if result is not None:` or compare against the sentinel.
