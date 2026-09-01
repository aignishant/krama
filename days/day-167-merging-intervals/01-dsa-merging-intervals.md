---
day: 167
track: dsa
title: "Merging intervals"
phase: "Greedy and intervals"
status: written
---

# Merging intervals

## 1. What this is, and why they ask it

**Given a set of intervals, combine every group that overlaps into a single interval.** `[1,3]`, `[2,6]`,
`[8,10]` becomes `[1,6]`, `[8,10]`.

Yesterday classified it as one of three techniques. **Today is the technique itself, in full** — because
merging is the most-asked interval problem there is, it has five variants that all appear, **and it has one
specific bug that survives almost every test anybody writes by hand.**

They ask it because **it is short enough to write in five minutes and has enough detail to fill twenty.** The
core loop is six lines. **The follow-ups — insert into a sorted list, find the gaps, intersect two lists, do
it as a stream — are all natural, all different, and all reuse the same idea.** An interviewer can start easy
and go as deep as they like without changing problems.

**And the specific bug is worth naming immediately, because it is the point of the lesson.** When two intervals
overlap, the merged end is `max(current_end, next_end)` — **not `next_end`.** An interval entirely *inside* the
current block would otherwise shrink it. **Containment is much rarer than partial overlap in hand-written
tests**, so the wrong version passes, and it fails on real data where a long booking swallows a short one.

By the end of this lesson you can write the merge and defend the sort key, handle the five variants, get the
boundary convention right, and know what changes when the input arrives as a stream.

---

## 2. The story

The road was being dug up in four places by four different people and none of them knew about the others, and
this was the entire content of Hemalatha's job.

**She sat in the corporation office and issued the permits.**

The water people wanted from the junction to the school, for eleven days. The cable people wanted from the
school to the temple, starting on the fourth. The gas people wanted a stretch in the middle. **And somebody
was always relaying the surface afterwards.**

**Her predecessor had issued them as they came and the road had been dug eleven times in one year.**

What she did instead took her about a month to get right and it was not complicated.

**She stopped thinking about the permits and started thinking about the road.**

Every morning she laid the requests out **in order of where they started** — not who asked, not how long, not
how important. **Where they started.** And she ran a finger along.

*Junction to school. Then school to temple — that touches, so it is one stretch: junction to temple.*

*Then nothing until the bus stand.*

**And the thing that caught her out, in the second month, was the small one.**

Because the gas people wanted forty metres in the middle of a stretch she had already joined up — **entirely
inside it** — and she wrote down the new stretch as ending where the gas work ended.

**Which was two hundred metres shorter than what she had already agreed.**

The men turned up, dug their forty metres, relaid it, and **the stretch beyond it — which was already
permitted and already dug — got resurfaced by nobody**, because her book said the work had ended.

**It was a small mistake and it cost four months.**

After that she said the same six words to herself on every single one, and she was still saying them eleven
years later.

**"Further of the two. Not the new one."**

Her assistant thought it was a strange thing to keep saying about something so obvious.

**"It is obvious," she said. "It is also the only mistake I have ever made in this job, and I made it because
the small one came along and I stopped thinking."**

---

## 3. The idea in plain English

Hemalatha's finger along the road is the algorithm, and her six words are the bug.

**The algorithm, in full.**

> **Sort by start. Walk through. If the next interval begins at or before the current block ends, extend the
> block to the further of the two ends. Otherwise close the block and begin a new one.**

**That is it, and the sort is what makes the single pass legal.**

**Why sorting by start is the right key**, precisely: **with intervals in start order, anything that overlaps
the current merged block must begin before that block ends.** So **one comparison per interval is enough** —
you never have to look backwards, and you never have to reconsider a block once it is closed.

**Sorted by end, that property does not hold.** An interval can start before the current block and extend past
everything seen so far, **and the single pass misses it.**

**Now the bug, which is the point of the day.**

```
   current block:  [1, 10]
   next interval:  [2,  3]        entirely INSIDE the block

   extend to max(10, 3) = 10      CORRECT   -> [1, 10]
   extend to 3                    WRONG     -> [1,  3]
```

**The block shrank.** And the version that shrinks it **passes almost every hand-written test**, because
people write overlapping intervals that extend each other — `[1,3]` and `[2,6]` — and rarely write one that is
entirely contained.

**Say Hemalatha's words while writing the line: "further of the two, not the new one."**

**Then the boundary convention, which is the second most common bug.**

**Do `[1,3]` and `[3,5]` merge?**

**For time slots and road stretches: yes** — they touch, and there is no gap. **`start <= current_end`.**

**For sets of discrete integers where the endpoints are exclusive: no** — `[1,3)` and `[3,5)` are adjacent and
do not overlap. **`start < current_end`.**

**One character, and the problem statement decides it.** LeetCode's Merge Intervals treats touching as
overlapping; **some interviewers deliberately ask about the other convention to see whether you ask.**

**Now the five variants, which is why this fills twenty minutes.**

**One: insert into a sorted, disjoint list.** The input is already sorted and non-overlapping — **so re-sorting
is `O(n log n)` where the answer is `O(n)`, and noticing that is what the problem tests.**

**Three phases, written as three loops rather than one loop with branches:** everything entirely before the new
interval, copied; everything overlapping it, absorbed; everything after, copied.

**Two: the gaps — the complement.** "When is the room free?" is the merged blocks inverted: **the space between
consecutive merged blocks, plus the space before the first and after the last.** **The two boundary cases at
the ends are where the bugs are**, and they need an explicit range to complement within.

**Three: intersecting two lists.** Two people's calendars; when are both free, or both busy? **Two pointers,
and the intersection of `[a,b]` and `[c,d]` is `[max(a,c), min(b,d)]`, valid when that start is at most that
end.** **Advance whichever interval ends first**, because it can intersect nothing further.

**Four: counting the merged blocks, or the total covered length.** Falls out of the merge — **`sum(end - start)`
over the merged blocks**, and doing it over the *unmerged* ones double-counts the overlaps, which is the whole
reason to merge first.

**Five: the streaming version, which is the interesting one.** **If intervals arrive one at a time and you
cannot sort, the algorithm does not apply** — the single pass depends on start order.

**What you use instead is a sorted structure**: keep the merged blocks in a balanced tree or sorted list keyed
by start, and on each arrival **binary search for the neighbours, then merge with any that overlap.**
`O(log n)` to find, and **the merge can absorb several blocks at once**, so it is `O(log n + k)` where `k` is
how many it swallows.

**And the amortised total is `O(n log n)`**, because each block can be absorbed only once.

**Finally, the representation detail that causes real bugs.**

**`sorted(intervals)` in Python sorts by start and then by end**, which is what merging wants — **so the
default is correct here and is wrong for selection.** Being explicit with `key=lambda x: x[0]` says which you
meant and costs nothing.

**And build the output as a list of mutable lists**, or use an explicit `current_start, current_end` pair —
**because tuples cannot be extended in place**, and the version that appends a tuple and then tries to modify
it is a real and common mistake.

---

## 4. The picture

The algorithm, walked:

```
   input (sorted by START):  [1,3]  [2,6]  [8,10]  [15,18]

   current = [1,3]
   [2,6]:   2 <= 3   -> overlap  -> extend to max(3, 6)  = 6   [1,6]
   [8,10]:  8 >  6   -> gap      -> close [1,6], current = [8,10]
   [15,18]: 15 > 10  -> gap      -> close [8,10], current = [15,18]
   end:                          -> close [15,18]

   output: [1,6]  [8,10]  [15,18]

   ONE PASS. Never look backwards, never reopen a closed block.
   That is what sorting by START buys.
```

The bug, which is the point of the lesson:

```
   current block:   [1 ==================== 10]
   next interval:        [2 = 3]                  ENTIRELY INSIDE

   max(current_end, next_end) = max(10, 3) = 10
        -> [1, 10]    CORRECT

   next_end = 3
        -> [1,  3]    WRONG — the block SHRANK

   AND IT PASSES YOUR TESTS, because hand-written cases look like
   [1,3] and [2,6] — partial overlap, where the new end IS further.

   Containment is rare in test data and common in real data,
   where a long booking swallows a short one.

   "Further of the two. Not the new one."
```

Why sorting by start, and not by end:

```
   BY START — the invariant that makes one pass work

     anything overlapping the current block must BEGIN before it ends
     -> one comparison per interval decides it
     -> never look backwards

   BY END — the invariant does not hold

     input [1,10] [2,3] [11,12], sorted by end: [2,3] [1,10] [11,12]

     current = [2,3]
     [1,10]: 1 <= 3 -> extend END to 10 -> [2,10]
                       but the START should have been 1
     -> [2,10] [11,12]

     THE BLOCK STARTS AT 2 INSTEAD OF 1.
     There is no code path that reaches backwards to fix a start,
     and the block COUNT is right, so a test counting blocks passes.
```

The boundary convention:

```
   [1, 3]  and  [3, 5]

   TOUCHING COUNTS AS OVERLAPPING (time slots, road stretches):
     start <= current_end        -> merges to [1, 5]

   TOUCHING DOES NOT (half-open ranges, discrete sets):
     start <  current_end        -> stays as [1,3] [3,5]

   ONE CHARACTER. The problem statement decides.
   LeetCode 56 merges them. Ask if it is not stated.
```

The variants, on one page:

```
   MERGE            sort by start, one pass                O(n log n)
   INSERT           input ALREADY sorted -> three phases    O(n)
                    (re-sorting is the mistake being tested)
   GAPS             the complement of the merged blocks     O(n log n)
                    (the two ends are where the bugs are)
   INTERSECT TWO    two pointers, [max(a,c), min(b,d)]      O(n + m)
                    advance whichever ENDS first
   TOTAL COVERED    sum(end - start) over MERGED blocks     O(n log n)
                    (over unmerged blocks it double-counts)
   STREAMING        a sorted structure + binary search      O(log n + k)
                    (the one-pass algorithm does not apply)
```

Intersecting two lists, and the pointer rule:

```
   A:   [0,2]      [5,10]        [13,23]     [24,25]
   B:      [1,5]      [8,12]         [15,24]  [25,26]

   at each step:
     lo = max(a.start, b.start)
     hi = min(a.end,   b.end)
     if lo <= hi: emit [lo, hi]
     ADVANCE WHICHEVER ENDS FIRST

   [0,2] & [1,5]   -> [1,2]    a ends first  -> advance a
   [5,10] & [1,5]  -> [5,5]    b ends first  -> advance b
   [5,10] & [8,12] -> [8,10]   a ends first  -> advance a
   ...

   WHY advance the one that ends first: it cannot intersect
   anything further in the other list, so it is finished.
```

The streaming version:

```
   ONE-PASS MERGE                    STREAMING

   needs the whole input             intervals arrive one at a time
   sorts once                        cannot sort
   O(n log n), one scan              a sorted structure, keyed by start

   on each arrival:
     binary search for the neighbours          O(log n)
     merge with any that overlap               O(k)
     (it may absorb SEVERAL at once)

   -> O(log n + k) per insert
   -> amortised O(n log n) total, because each block can be
      absorbed only ONCE
```

---

## 5. The code, built step by step

### The merge

```python
def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Sort by START. Extend to the FURTHER of the two ends."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:                    # touching counts
            merged[-1][1] = max(merged[-1][1], end)   # FURTHER OF THE TWO
        else:
            merged.append([start, end])
    return [tuple(block) for block in merged]
```

**`max(merged[-1][1], end)` is the line.** Say Hemalatha's words while writing it.

**`list(ordered[0])` and the list-of-lists** are deliberate: **tuples cannot be modified in place**, and the
version that appends a tuple and then tries to extend it is a real mistake. **Converting back at the end keeps
the interface clean.**

**And `start <= merged[-1][1]` is the boundary convention** — `<=` merges touching intervals, `<` does not.

### The variant without a mutable list

```python
def merge_pairs(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Same algorithm, carrying the current block in two variables."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    result: list[tuple[int, int]] = []
    current_start, current_end = ordered[0]
    for start, end in ordered[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            result.append((current_start, current_end))
            current_start, current_end = start, end
    result.append((current_start, current_end))       # the LAST block
    return result
```

**`result.append(...)` after the loop is the line people forget**, and it silently drops the final block —
**which on a single-block input returns an empty list.**

**This form is slightly clearer about what "the current block" is**, at the cost of remembering the flush.

### Inserting into a sorted list

```python
def insert_interval(intervals: list[tuple[int, int]],
                    new: tuple[int, int]) -> list[tuple[int, int]]:
    """Input is ALREADY sorted and disjoint. Three phases. O(n), not O(n log n)."""
    result: list[tuple[int, int]] = []
    start, end = new
    i, n = 0, len(intervals)

    while i < n and intervals[i][1] < start:          # entirely before
        result.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= end:           # overlapping: absorb
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1

    result.append((start, end))
    result.extend(intervals[i:])                      # entirely after
    return result
```

**Three loops rather than one loop with branches** is what makes this readable, and the phases are exactly the
three cases.

**The absorbing loop widens in both directions** — `min` on the start and `max` on the end — **because the new
interval can extend past existing blocks on either side.**

**And `O(n)` rather than `O(n log n)` is the whole point of the problem**: the input being sorted is stated,
and re-sorting throws that away.

### The gaps

```python
def free_time(intervals: list[tuple[int, int]],
              lower: int, upper: int) -> list[tuple[int, int]]:
    """The complement of the merged blocks, within [lower, upper]."""
    blocks = merge(intervals)
    gaps: list[tuple[int, int]] = []
    cursor = lower
    for start, end in blocks:
        if start > cursor:
            gaps.append((cursor, start))              # the gap BEFORE this block
        cursor = max(cursor, end)
    if cursor < upper:
        gaps.append((cursor, upper))                  # the gap AFTER the last
    return gaps
```

**The two boundary cases are where the bugs are**: the gap before the first block and the gap after the last.
**Both need an explicit range to complement within** — "when is the room free" is meaningless without knowing
the day's bounds.

**`cursor = max(cursor, end)` rather than `cursor = end`** guards against a block that lies entirely before
`lower`, **which is the same containment mistake in a different place.**

### Intersecting two lists

```python
def intersect(a: list[tuple[int, int]],
              b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Both already sorted and disjoint. Two pointers. O(n + m)."""
    result: list[tuple[int, int]] = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            result.append((lo, hi))
        if a[i][1] < b[j][1]:                         # advance whichever ENDS first
            i += 1
        else:
            j += 1
    return result
```

**`[max(start, start), min(end, end)]` is the intersection of two intervals**, valid exactly when the result is
non-empty.

**And advancing whichever ends first is the correctness argument**: **that interval cannot intersect anything
later in the other list**, because the other list is sorted and everything after starts later.

### Total covered length

```python
def total_covered(intervals: list[tuple[int, int]]) -> int:
    """Merge first. Summing the raw intervals double-counts overlaps."""
    return sum(end - start for start, end in merge(intervals))


def total_raw(intervals: list[tuple[int, int]]) -> int:
    """For contrast: what NOT merging gives you."""
    return sum(end - start for start, end in intervals)
```

**Two lines, and the difference between them is the entire reason to merge** — `[1,10]` and `[2,3]` cover nine
units, not ten.

### The streaming version

```python
import bisect

class StreamingMerger:
    """Intervals arrive one at a time. The one-pass algorithm does not apply."""

    def __init__(self) -> None:
        self.starts: list[int] = []
        self.ends: list[int] = []

    def add(self, start: int, end: int) -> None:
        # the first block that could possibly overlap
        i = bisect.bisect_left(self.ends, start)
        # absorb every block that begins at or before our end
        j = i
        while j < len(self.starts) and self.starts[j] <= end:
            start = min(start, self.starts[j])
            end = max(end, self.ends[j])
            j += 1
        self.starts[i:j] = [start]
        self.ends[i:j] = [end]

    def blocks(self) -> list[tuple[int, int]]:
        return list(zip(self.starts, self.ends))
```

**`bisect_left(self.ends, start)` finds the first block whose end reaches our start** — everything before it is
entirely to the left and cannot overlap.

**The `while` loop absorbs several blocks at once**, which is the case people miss: **a new interval spanning a
gap swallows the blocks on both sides.**

**And `self.starts[i:j] = [start]` replaces the whole absorbed range with one block in a single slice
assignment**, which is both correct and much cleaner than deleting in a loop.

**Amortised `O(n log n)`**, because a block can be absorbed only once.

### The wrong versions, for comparison

```python
def merge_shrinking(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """THE BUG: `= end` instead of `max(...)`."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = end                       # WRONG
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def merge_by_end(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """THE OTHER BUG: the wrong sort key."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[1])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]
```

**Keeping the broken versions next to the correct one and running all three** is worth five minutes, **because
the failures are invisible from reading and immediate from testing.**

### The complete solution

```python
"""Merging intervals: the algorithm, the bug, and the five variants."""

import bisect
import random


def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Sort by START; extend to the FURTHER of the two ends."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:                    # <= : touching merges
            merged[-1][1] = max(merged[-1][1], end)   # "further of the two"
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def merge_strict(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """The other convention: touching does NOT merge."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start < merged[-1][1]:                     # < : touching stays apart
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def insert_interval(intervals: list[tuple[int, int]],
                    new: tuple[int, int]) -> list[tuple[int, int]]:
    """Input already sorted and disjoint -> O(n), three phases."""
    result: list[tuple[int, int]] = []
    start, end = new
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start, end = min(start, intervals[i][0]), max(end, intervals[i][1])
        i += 1
    result.append((start, end))
    result.extend(intervals[i:])
    return result


def free_time(intervals: list[tuple[int, int]],
              lower: int, upper: int) -> list[tuple[int, int]]:
    """The gaps. The two ends are where the bugs live."""
    gaps: list[tuple[int, int]] = []
    cursor = lower
    for start, end in merge(intervals):
        if start > cursor:
            gaps.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < upper:
        gaps.append((cursor, upper))
    return gaps


def intersect(a: list[tuple[int, int]],
              b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Two sorted disjoint lists. Advance whichever ENDS first."""
    result: list[tuple[int, int]] = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            result.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result


def total_covered(intervals: list[tuple[int, int]]) -> int:
    return sum(e - s for s, e in merge(intervals))


def total_raw(intervals: list[tuple[int, int]]) -> int:
    return sum(e - s for s, e in intervals)


class StreamingMerger:
    """Arrivals one at a time: a sorted structure, not a single pass."""

    def __init__(self) -> None:
        self.starts: list[int] = []
        self.ends: list[int] = []

    def add(self, start: int, end: int) -> None:
        i = bisect.bisect_left(self.ends, start)
        j = i
        while j < len(self.starts) and self.starts[j] <= end:
            start = min(start, self.starts[j])
            end = max(end, self.ends[j])
            j += 1
        self.starts[i:j] = [start]
        self.ends[i:j] = [end]

    def blocks(self) -> list[tuple[int, int]]:
        return list(zip(self.starts, self.ends))


# ---------- the broken versions, for comparison ----------

def merge_shrinking(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = end                       # THE BUG
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def merge_by_end(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[1])   # THE OTHER BUG
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def check_against_brute(trials: int = 500) -> str:
    """Merge by marking a small number line. Obviously correct, useless at scale."""
    for _ in range(trials):
        n = random.randint(1, 8)
        ivs = []
        for _ in range(n):
            s = random.randint(0, 20)
            ivs.append((s, s + random.randint(0, 8)))

        covered = set()
        for s, e in ivs:
            covered.update(range(s, e))               # half-open marking
        expected = []
        for point in sorted(covered):
            if expected and expected[-1][1] == point:
                expected[-1][1] = point + 1
            else:
                expected.append([point, point + 1])
        expected = [tuple(b) for b in expected]

        # half-open marking treats touching ranges as contiguous,
        # so compare against the `<=` version
        got = [b for b in merge(ivs) if b[0] != b[1]]
        if got != expected:
            return f"MISMATCH on {ivs}: got {got}, expected {expected}"
    return f"agreed on {trials} random cases"


if __name__ == "__main__":
    random.seed(0)
    ivs = [(1, 3), (2, 6), (8, 10), (15, 18)]
    print("THE ALGORITHM")
    print("  input       :", ivs)
    print("  merged      :", merge(ivs))

    print("\nTHE BUG — an interval CONTAINED in the current block")
    contained = [(1, 10), (2, 3), (11, 12)]
    print("  input       :", contained)
    print("  correct     :", merge(contained))
    print("  with `= end`:", merge_shrinking(contained))
    print("  by END sort :", merge_by_end(contained))

    print("\n  ...and on a typical hand-written test, the bug is INVISIBLE:")
    typical = [(1, 3), (2, 6), (8, 10)]
    print("  input       :", typical)
    print("  correct     :", merge(typical))
    print("  with `= end`:", merge_shrinking(typical))

    print("\nTHE BOUNDARY CONVENTION")
    touching = [(1, 3), (3, 5), (6, 8)]
    print("  input               :", touching)
    print("  touching MERGES     :", merge(touching))
    print("  touching stays apart:", merge_strict(touching))

    print("\nTHE VARIANTS")
    sorted_disjoint = [(1, 3), (6, 9)]
    print("  insert (2,5)  :", insert_interval(sorted_disjoint, (2, 5)))
    print("  insert (4,5)  :", insert_interval(sorted_disjoint, (4, 5)))
    print("  insert (0,20) :", insert_interval(sorted_disjoint, (0, 20)))
    print("  free time     :", free_time(ivs, 0, 24))
    print("  intersect     :", intersect([(0, 2), (5, 10), (13, 23), (24, 25)],
                                         [(1, 5), (8, 12), (15, 24), (25, 26)]))
    print("  covered       :", total_covered(contained),
          " (unmerged would say", total_raw(contained), ")")

    print("\nSTREAMING")
    stream = StreamingMerger()
    for pair in [(8, 10), (1, 3), (15, 18), (2, 6), (4, 16)]:
        stream.add(*pair)
        print(f"  after {str(pair):8} -> {stream.blocks()}")

    print("\nVERIFICATION")
    print(" ", check_against_brute())
```

Run it and you get:

```
THE ALGORITHM
  input       : [(1, 3), (2, 6), (8, 10), (15, 18)]
  merged      : [(1, 6), (8, 10), (15, 18)]

THE BUG — an interval CONTAINED in the current block
  input       : [(1, 10), (2, 3), (11, 12)]
  correct     : [(1, 10), (11, 12)]
  with `= end`: [(1, 3), (11, 12)]
  by END sort : [(2, 10), (11, 12)]

  ...and on a typical hand-written test, the bug is INVISIBLE:
  input       : [(1, 3), (2, 6), (8, 10)]
  correct     : [(1, 6), (8, 10)]
  with `= end`: [(1, 6), (8, 10)]

THE BOUNDARY CONVENTION
  input               : [(1, 3), (3, 5), (6, 8)]
  touching MERGES     : [(1, 5), (6, 8)]
  touching stays apart: [(1, 3), (3, 5), (6, 8)]

THE VARIANTS
  insert (2,5)  : [(1, 5), (6, 9)]
  insert (4,5)  : [(1, 3), (4, 5), (6, 9)]
  insert (0,20) : [(0, 20)]
  free time     : [(0, 1), (6, 8), (10, 15), (18, 24)]
  intersect     : [(1, 2), (5, 5), (8, 10), (15, 23), (24, 24), (25, 25)]
  covered       : 10  (unmerged would say 11 )

STREAMING
  after (8, 10)  -> [(8, 10)]
  after (1, 3)   -> [(1, 3), (8, 10)]
  after (15, 18) -> [(1, 3), (8, 10), (15, 18)]
  after (2, 6)   -> [(1, 6), (8, 10), (15, 18)]
  after (4, 16)  -> [(1, 18)]

VERIFICATION
  agreed on 500 random cases
```

**The two blocks under "THE BUG" are the whole lesson.** On the contained input, `= end` gives `[(1,3)]` where
the answer is `[(1,10)]` — **the block shrank by seven.** **And on the typical hand-written input, the broken
version gives exactly the right answer**, which is why it survives.

**And the streaming trace's last line is the case people miss**: `(4,16)` arrives and **absorbs all three
existing blocks at once**, collapsing everything into `[1,18]`.

---

## 6. What it costs

**The merge.**

```
   sort         O(n log n)   <- dominates
   one pass     O(n)
   output       O(n) space

   TOTAL: O(n log n) time, O(n) space
```

**And if the input is already sorted — which several of the variants specify — it is `O(n)`.**

```
   n = 1,000        instant
   n = 1,000,000    sort ~1.5 s in Python, pass ~0.3 s
   n = 10,000,000   sort ~20 s

   -> merging scales well. There is no hidden quadratic anywhere
      in this family.
```

**The variants:**

```
   merge                 O(n log n)
   insert (sorted input) O(n)          <- re-sorting makes it O(n log n)
   gaps                  O(n log n)    (merge + one pass)
   intersect two lists   O(n + m)      <- both already sorted
   total covered         O(n log n)    (merge + a sum)
   streaming, per insert O(log n + k)  <- k = blocks absorbed
   streaming, total      O(n log n)    amortised
```

**The streaming amortisation, which is the interesting one:**

```
   each insert:  O(log n) to find the position
               + O(k) to absorb k blocks

   worst single insert: k = n, when one interval swallows everything
                        -> O(n) for that one call

   BUT each block can be absorbed only ONCE
   -> the total absorption work over n inserts is O(n)
   -> amortised O(log n) per insert, O(n log n) overall

   Same as sorting. Which is the right comparison: the streaming
   version costs no more in total, and pays it incrementally.
```

**The slice assignment, which matters in Python:**

```
   self.starts[i:j] = [start]

   this is O(n) in the worst case, because a list shifts its tail
   -> in a language with a balanced tree, the same operation is O(log n)

   for n up to ~100,000 the constant factor makes the list version
   faster anyway; above that, a real sorted container is worth it.
```

**Space:**

```
   merge            O(n) for the output (O(1) extra if in-place)
   insert           O(n) for the output
   intersect        O(min(n, m)) for the output
   streaming        O(b) where b is the number of merged blocks

   and b can be far smaller than n: heavily overlapping input
   collapses to a handful of blocks.
```

**The double-counting cost, which is why merging exists at all:**

```
   [1,10] and [2,3]

   sum of raw lengths:      9 + 1 = 10
   actual covered length:   9

   -> the error grows with the amount of overlap
   -> for calendar or coverage data, overlap is the normal case,
      so the raw sum can be off by a large factor
```

**Comparison with the naive approach:**

```
   "which intervals overlap?" by checking every pair:  O(n^2)
   sorting and checking adjacent pairs:                O(n log n)

   n = 100,000:  10^10 against 1.7 x 10^6   -> ~6,000x

   -> and the sorted version answers a STRONGER question:
      it produces the merged blocks, not just a yes or no.
```

---

## 7. The traps

**`= end` instead of `max(current_end, end)`.**

```python
>>> merge([(1, 10), (2, 3), (11, 12)])
[(1, 10), (11, 12)]
>>> merge_shrinking([(1, 10), (2, 3), (11, 12)])
[(1, 3), (11, 12)]
```

**The block shrank from ten to three.** And the reason it survives:

```python
>>> merge([(1, 3), (2, 6), (8, 10)])
[(1, 6), (8, 10)]
>>> merge_shrinking([(1, 3), (2, 6), (8, 10)])
[(1, 6), (8, 10)]
```

**Identical on the typical input**, because partial overlap is what people write by hand and **the new end
happens to be further.** **Containment is common in real data and rare in tests.**

**The wrong sort key.**

```python
>>> merge_by_end([(1, 10), (2, 3), (11, 12)])
[(2, 10), (11, 12)]
```

**The block starts at 2 instead of 1.** Sorted by end, the pass began with `[2,3]` and absorbed `[1,10]` by
extending the *end* — **and there is no code path that reaches backwards to fix a start.**

**The block count is right**, so a test asserting "two blocks" passes.

**Forgetting the final flush.**

```python
>>> # merge_pairs without the append after the loop:
>>> # on [(1,3)] -> returns []
>>> # on [(1,3),(2,6)] -> returns []
>>> # the LAST block is never emitted
```

**Every input loses its last block**, which on a single-interval input returns nothing at all. **The
list-of-lists version does not have this problem**, because the block is already in the list.

**The boundary convention, unstated.**

```python
>>> merge([(1, 3), (3, 5)])
[(1, 5)]
>>> merge_strict([(1, 3), (3, 5)])
[(1, 3), (3, 5)]
```

**Both are correct for different problems.** **The statement decides, and if it does not say, ask** — an
interviewer who left it out may well be checking.

**Re-sorting a sorted input.**

```python
>>> # "insert into a SORTED, DISJOINT list"
>>> # appending and re-sorting: O(n log n)
>>> # the three-phase scan:      O(n)
>>> # -> the problem is testing whether you read the word "sorted"
```

**Trying to modify a tuple.**

```python
>>> merged = [(1, 3)]
>>> merged[-1][1] = 6
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

**This one at least errors**, which makes it the friendliest bug in the lesson. **Build with lists and convert
at the end**, or carry the current block in two variables.

**The gaps, without an explicit range.**

```python
>>> free_time([(2, 4), (6, 8)], 0, 24)
[(0, 2), (4, 6), (8, 24)]
>>> # without lower and upper, what is "free" before 2 and after 8?
>>> # the question is meaningless without bounds
```

**"When is the room free" needs the day's bounds**, and the two boundary gaps — before the first block and
after the last — **are where the off-by-one errors live.**

**Streaming with the one-pass algorithm.**

```python
>>> # re-sorting and re-merging on every arrival:
>>> # O(n log n) per insert -> O(n^2 log n) over n arrivals
>>> # n = 100,000 -> not viable
```

**The single-pass merge depends on having the whole input in start order**, and it is not incremental. **A
sorted structure with a binary search is the answer**, and it is amortised `O(n log n)` overall — **the same
total as sorting once.**

**Missing the multi-block absorption in the streaming version.**

```python
>>> stream = StreamingMerger()
>>> for p in [(1, 3), (8, 10), (15, 18)]:
...     stream.add(*p)
>>> stream.add(4, 16)
>>> stream.blocks()
[(1, 18)]
```

**One arrival absorbed all three blocks.** A version that merges with only the nearest neighbour **leaves
overlapping blocks in the structure**, and the corruption compounds silently with every later insert.

---

## 8. In the interview

### How it gets asked

- *"Merge overlapping intervals."* — LeetCode 56, and it is the most-asked interval problem there is.
- *"Insert an interval into a sorted list."* — LeetCode 57, testing whether you re-sort.
- *"Find the free time common to several people's calendars."* — LeetCode 759, the gaps.
- *"Given two lists of intervals, find their intersection."* — LeetCode 986.
- *"What if the intervals arrive one at a time?"* — the streaming follow-up.
- *"Do `[1,3]` and `[3,5]` overlap?"* — checking whether you ask.

### The first ninety seconds

> "Merging is one pass after a sort, and I want to be precise about which sort and about one line in the loop.
>
> **Sort by start.** That is what makes a single pass legal: **with intervals in start order, anything that
> overlaps the current merged block must begin before that block ends** — so one comparison per interval
> decides it, and I never have to look backwards or reopen a closed block.
>
> **Sorted by end, that property does not hold**, and the algorithm is silently wrong — it produces blocks
> whose starts are too late, and there is no code path that could fix them.
>
> **Then the loop: if the next interval starts at or before the current block's end, extend the block.
> Otherwise close it and start a new one.**
>
> **And the extension is `max(current_end, next_end)`, not `next_end`** — that is the line I would say out
> loud while writing it. **An interval entirely inside the current block would otherwise shrink it.**
>
> **`[1,10]` followed by `[2,3]` becomes `[1,3]` with the wrong version**, and the reason it survives is that
> **it gives exactly the right answer on typical hand-written tests**, where intervals partially overlap and
> the new end genuinely is further. **Containment is rare in tests and common in real data.**
>
> **One thing I would settle first: do `[1,3]` and `[3,5]` merge?** For time slots, yes — they touch and there
> is no gap. **For half-open ranges, no.** It is one character, `<=` against `<`, **and the problem decides
> it.**
>
> **Cost: `O(n log n)`, dominated by the sort, and `O(n)` for the output.** If the input is already sorted —
> which several of the variants specify — **it is `O(n)`, and noticing that is usually what those variants are
> testing.**
>
> **And I would build the output as lists rather than tuples**, or carry the current block in two variables,
> because a tuple cannot be extended in place."

### The follow-ups

**"Why does sorting by start make this work?"**

> "Because it establishes exactly the invariant the single pass needs, and I would state the invariant rather
> than just the key.
>
> **With intervals in start order, any interval that overlaps the current merged block must *begin* before that
> block ends.** That is what lets one comparison decide the whole question — **I never have to look backwards
> at closed blocks, and I never have to reopen one.**
>
> **And the reason a closed block stays closed: everything remaining starts at or after the current
> interval's start**, which is already past the closed block's end. **So nothing later can reach back into
> it.**
>
> **Sorted by end, that fails.** Take `[1,10]`, `[2,3]` and `[11,12]`. By end they order as `[2,3]`, `[1,10]`,
> `[11,12]`. **The pass begins with `[2,3]`, sees that `[1,10]` starts at 1 which is inside it, and extends the
> end to 10** — giving `[2,10]`.
>
> **The block starts at 2 when it should start at 1**, and there is no code path that reaches backwards to fix
> a start. **And the block count is still two, so a test asserting the number of blocks passes.**
>
> **The general habit I would name: when I pick a sort key, I try to say what invariant it gives me.** For
> merging it is 'overlapping intervals begin before the block ends'. **For selection it is 'the earliest
> finisher leaves the most room'.** Different invariants, different keys — **and if I cannot state the
> invariant, I have not understood why the algorithm is correct.**
>
> **One implementation note: in Python, `sorted(intervals)` on tuples sorts by start then end**, which happens
> to be right here. **I still write the key explicitly**, because it says which I meant and because the same
> default is wrong for the selection problem."

**"What if the intervals arrive one at a time and you cannot sort?"**

> "Then the single-pass algorithm does not apply at all, **because it depends on having the whole input in
> start order** — and I would say that first, because the instinct is to try to adapt it.
>
> **The naive adaptation is to re-sort and re-merge on every arrival**, which is `O(n log n)` per insert and
> `O(n² log n)` overall. **At a hundred thousand arrivals that does not finish.**
>
> **What I would use is a sorted structure keyed by start** — a balanced tree, or a sorted list with binary
> search — **holding the currently merged blocks.**
>
> **On each arrival: binary search for the first block that could overlap**, which is the first block whose
> end reaches the new interval's start. **Then absorb every block that begins at or before the new interval's
> end**, widening in both directions as I go. **Replace the whole absorbed range with one block.**
>
> **The case people miss is that one arrival can absorb several blocks at once.** If I have `[1,3]`, `[8,10]`
> and `[15,18]`, **and `[4,16]` arrives, it swallows all three** and everything collapses to `[1,18]`. **A
> version that merges with only the nearest neighbour leaves overlapping blocks in the structure**, and the
> corruption compounds silently with every later insert.
>
> **Cost: `O(log n)` to find the position plus `O(k)` to absorb `k` blocks.** **The worst single insert is
> `O(n)`** when one interval swallows everything.
>
> **But the amortised total is `O(n log n)`, because a block can be absorbed only once.** So over `n` arrivals
> the total absorption work is `O(n)`. **Which is the right comparison to make: the streaming version costs no
> more in total than sorting once — it just pays it incrementally.**
>
> **One Python note: a slice assignment on a list is `O(n)` because the tail shifts.** For up to about a
> hundred thousand blocks the constant factor makes that faster than a tree anyway; **above that, a real sorted
> container is worth the dependency.**"

**"Now find the free time — when is nobody busy?"**

> "That is the complement of the merged blocks, and it is a two-step answer where the second step is where the
> bugs are.
>
> **Step one: merge.** Take everyone's busy intervals, put them all in one list, and merge them. **The merged
> blocks are the times when at least one person is busy.**
>
> **Step two: walk the blocks and emit the space between them.** Keep a cursor; for each block, if it starts
> after the cursor, that space is free; then move the cursor to the block's end.
>
> **And there are two boundary cases that are where every bug in this variant lives.**
>
> **The gap before the first block, and the gap after the last one.** Both need **an explicit range to
> complement within** — 'when is the room free' is meaningless without knowing the day's bounds. **So the
> function takes a lower and an upper bound**, and I would ask for them rather than assume the first and last
> busy times, **because free time before anyone starts is usually exactly what the caller wants.**
>
> **One more subtlety: `cursor = max(cursor, end)` rather than `cursor = end`.** A block lying entirely before
> the cursor — which can happen if the bounds are inside the data — **would otherwise move the cursor
> backwards** and emit a nonsensical gap. **It is the same containment mistake as the merge bug, in a different
> place.**
>
> **Cost: `O(n log n)` for the merge and `O(n)` for the walk.**
>
> **And the related variant is intersecting two calendars rather than complementing one**: given two sorted
> disjoint lists, find where they overlap. **Two pointers, and the intersection of two intervals is
> `[max(starts), min(ends)]`, valid when that is non-empty.** **Advance whichever interval ends first**, because
> it cannot intersect anything further in the other list. `O(n + m)`, no sorting needed since both inputs are
> already ordered."

### The model answer

*"You are building a scheduling assistant. Given several people's busy calendars — each a list of intervals —
find all the slots of at least thirty minutes where everyone is free, within working hours."*

> "Three steps, and the third is where the requirement actually bites, so let me name all three before
> starting.
>
> **Step one: combine everyone's busy intervals into one list and merge them.** I do not care whose meeting is
> whose — **if anybody is busy, the slot is unavailable** — so the union of everyone's busy time is exactly
> what I need, and merging it gives the blocks when at least one person is occupied.
>
> **That is the classic merge: sort by start, one pass, extend to the further of the two ends.** And I would
> say the extension out loud, because **`max(current_end, next_end)` rather than `next_end` is the bug that
> passes typical tests** — a short meeting entirely inside a long one would otherwise shrink the block, **and
> calendars are full of exactly that shape.**
>
> **Step two: complement the merged blocks within working hours.** The gaps between consecutive blocks, **plus
> the gap from the start of the working day to the first block and from the last block to the end of the
> day.**
>
> **The bounds have to be explicit** — nine to five, or whatever the calendars use — **because free time before
> anyone's first meeting is usually the answer people want, and without bounds the question has no answer at
> the edges.**
>
> **Step three, which is the actual requirement: filter for gaps of at least thirty minutes.** One line, and it
> is the reason the whole thing is asked — **a slot of four minutes is not a slot.**
>
> **Cost: `O(n log n)` where `n` is the total number of busy intervals across everyone**, dominated by the
> sort. For a dozen people with a dozen meetings each that is instant.
>
> **Now the details I would raise, because a scheduling assistant is full of them.**
>
> **Time zones.** If the participants are in different zones, **everything must be converted to a common
> instant before merging** — merging local times across zones is a wrong-answer bug that looks like a
> correctness bug and is a data bug. **I would normalise to UTC on the way in and convert back only for
> display.**
>
> **The boundary convention.** A meeting ending at ten and one starting at ten do not overlap — **the room is
> free at ten.** So `start <= current_end` merges them, which is what I want here, **and I would state the
> assumption.**
>
> **And working hours differ per person**, which is the version of the problem that is actually asked in
> practice. **That is not a filter at the end — it is an extra set of busy intervals per person**, covering
> everything outside their working day. **Which is a nice outcome: it needs no new algorithm, just more
> intervals into the same merge.**
>
> **Two follow-ups I would offer.**
>
> **If the calendars are large and the query is repeated** — 'find me a slot' asked many times a day for the
> same people — **I would keep each person's merged busy blocks cached and merge the merged lists**, which is
> cheaper than starting from raw meetings each time.
>
> **And if meetings arrive continuously rather than being fetched as a batch, the single pass does not
> apply.** **That is the streaming version**: keep the merged blocks in a sorted structure and, on each new
> meeting, binary search for the position and absorb any overlapping blocks — **remembering that one meeting
> can absorb several blocks at once.** `O(log n)` per arrival amortised, **the same total as sorting once.**"

---

## 9. Recall card

**Sort by START, one pass: if the next interval begins at or before the current block ends, extend the block;
otherwise close it and start a new one.** Sorting by start is what makes a single pass legal — **anything
overlapping the current block must BEGIN before it ends**, so you never look backwards and never reopen a
closed block.

**The bug, and it is the point of the lesson: extend to `max(current_end, next_end)`, NEVER `= next_end`.** An
interval entirely inside the block would otherwise shrink it — `[1,10]` then `[2,3]` becomes `[1,3]`. **And it
gives exactly the right answer on typical hand-written tests**, because partial overlap is what people write
and containment is what real data contains.

**Sorted by END the invariant fails**: `[1,10]`, `[2,3]`, `[11,12]` gives `[(2,10)]` — **the block starts at 2
and no code path reaches backwards to fix a start**, while the block *count* stays right.

**The boundary convention is one character** — `<=` merges touching intervals, `<` does not — and the problem
decides it. **Ask if it is not stated.**

**Five variants: insert into a sorted list (`O(n)`, three phases — re-sorting is the mistake being tested);
gaps (the complement, and the two ends are where the bugs live — needs explicit bounds, and
`cursor = max(cursor, end)`); intersect two lists (two pointers, `[max(starts), min(ends)]`, advance whichever
ENDS first); total covered (merge first, or overlaps are double-counted); and streaming.**

**Streaming: the one-pass algorithm does not apply.** Keep the blocks in a sorted structure, binary search for
the position, **and absorb every overlapping block — one arrival can swallow several at once.**
`O(log n + k)` per insert, **amortised `O(n log n)` overall because a block can be absorbed only once** — the
same total as sorting once, paid incrementally.
