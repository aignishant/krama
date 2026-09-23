---
day: 54
track: dsa
title: "Quicksort and partitioning"
phase: "Sorting"
status: written
---

# Day 054 · DSA — Quicksort and partitioning

**After today you can:** You can partition an array in place and explain the worst case and how to avoid it.

**The interviewer asks it as:** *Write quicksort. What is its worst case, and when does it happen?*

---

## 1. What this is, and why they ask it

Quicksort picks one value out of the list — the **pivot** — and rearranges everything so that
smaller values sit to its left and larger values to its right. After that one rearrangement, the
pivot is in its final position forever, and the two sides can be sorted independently by the same
method. That rearrangement is called **partitioning**, and it is the whole algorithm.

They ask it because it is the sort that is actually used, and because it is the one with an
interesting failure. Quicksort is `O(n log n)` on average, sorts in place with `O(1)` extra data
space, and beats merge sort by a factor of two or three in practice — so it is what C's `qsort`,
Java's primitive sort and C++'s `std::sort` are built on. But its worst case is `O(n²)`, and the
input that triggers it is the one people least expect: an already sorted list. Being able to say
which pivot choice causes that, why randomising fixes it, and what "expected `O(n log n)`" actually
promises is the difference between reciting quicksort and understanding it. The partition step is
also a skill on its own — it is exactly what
[day 055](../day-055-quickselect/README.md) uses to find the k-th largest in linear time, and the
three-way version is the Dutch national flag problem.

---

## 2. The story

There is a man called Selvam who sells potatoes from a cart on the road outside the market in
Madurai, and on Monday mornings a lorry drops about eighty kilos of them in one heap on the tray at
the back of his cart. Big ones, small ones, everything mixed together. The hotels want the big ones
and pay more for them, so the heap has to end up graded.

The way he does it is worth watching.

He reaches into the heap and picks up one potato — not the top one, one from somewhere in the middle
— and he holds it in his left hand. That one is the measure. Then, with his right hand, he takes
every other potato in turn, holds it briefly next to the one in his left hand, and drops it into one
of two crates: the crate on his left if it is smaller than the one he is holding, the crate on his
right if it is bigger. He does not compare it to anything else. One look, one crate.

When the heap is gone, he puts the potato from his left hand down in the gap between the two crates,
and that potato is finished. He knows, without checking anything else, that everything to its left is
smaller and everything to its right is bigger. It will not move again.

Then he does exactly the same thing inside the left crate. Picks one out, splits the rest into two
around it, puts it down in its place. And inside the right crate. And inside each of those. The
crates keep getting smaller until there is nothing left to split.

His brother-in-law tried to help one week and did it badly, and Selvam still brings it up. Instead of
reaching into the middle, the brother-in-law kept grabbing whichever potato was nearest — which,
because the lorry tips them out roughly graded, was almost always one of the smallest in the heap. So
every single other potato went into the crate on the right. Nothing went left. The heap had not been
split at all; it had just moved. He did that over and over, and after an hour he had compared nearly
every potato to nearly every other potato and the tray was still a mess.

Selvam's rule, which he told him afterwards and repeats to anyone who will listen: never take the one
that is closest to your hand. Reach in and take one from the middle of the heap, where you cannot see
what you are getting.

---

## 3. The idea in plain English

Selvam is running quicksort. The potato in his left hand is the **pivot**. Splitting the heap into
two crates around it is the **partition**. Putting the pivot down between the crates is the moment it
reaches its final position. Doing the same thing inside each crate is the recursion. And his
brother-in-law is the `O(n²)` worst case.

### The one idea: partitioning

Everything today rests on this, so learn it separately from the sort.

**Partitioning** means rearranging a list around a chosen value so that everything smaller than it
comes first, then the value itself, then everything larger. It takes one pass and `O(n)` time,
because each element is looked at once and compared to one thing.

```
 before   [ 7 , 2 , 9 , 4 , 1 , 8 , 3 ]        pivot = 4
 after    [ 2 , 1 , 3 , 4 , 7 , 9 , 8 ]
            \______/    ^   \______/
            smaller   final    larger
                      place
```

Two facts about that result matter, and they are worth saying out loud because candidates often only
say the first:

1. **The pivot is now in its final sorted position.** Not approximately — exactly. Three values are
   smaller than 4, so 4 belongs at position 3, and that is where it is. It never has to be looked at
   again.
2. **The two sides are not sorted.** `[2, 1, 3]` is not in order. All that is known is that
   everything on the left is smaller than the pivot and everything on the right is larger.

That second fact is what makes the recursion honest: each side is a smaller version of the same
problem, and no element ever has to cross the pivot.

### The sort, in one sentence

> Partition, then quicksort the left part, then quicksort the right part.

There is no merge step. That is the structural difference from merge sort on
[day 053](../day-053-merge-sort/README.md), and it is why quicksort sorts in place. Merge sort does
its work on the way *back up* the recursion, when it combines. Quicksort does its work on the way
*down*, when it partitions, and the way back up does nothing at all.

### The pivot choice, which is the whole story

Whichever value you choose as the pivot ends up between the two sides, so the *size* of the two sides
depends entirely on how central the pivot's value is.

```
 a good pivot: the median
   n elements  ->  two sides of n/2 each  ->  depth log2(n)  ->  n log n total

 a bad pivot: the smallest value
   n elements  ->  sides of 0 and n-1     ->  depth n        ->  n^2 total
```

If you always pick the first element as the pivot, then on an **already sorted list** the first
element is always the smallest, every partition produces one empty side, and quicksort degenerates
into something with the shape of selection sort — `n(n−1)/2` comparisons. Sorted input is a common
input. That is the trap, and it is exactly the brother-in-law grabbing the nearest potato.

Three fixes, in increasing order of how much interviewers like them:

- **Random pivot.** Choose a position uniformly at random and swap it to the end before
  partitioning. No fixed input can be bad, because the behaviour no longer depends on the input's
  arrangement. This is the answer to give.
- **Median of three.** Look at the first, middle and last elements and use the middle-valued one.
  Cheap, deterministic, and it handles sorted and reverse-sorted input — but a determined adversary
  who knows your rule can still construct a bad input.
- **Introsort.** Count the recursion depth, and if it exceeds about `2 log₂ n`, stop and finish with
  heapsort. That gives a hard `O(n log n)` guarantee. It is what `std::sort` in C++ actually does.

### The other bad input: many duplicates

A list where every value is the same is the second worst case, and it surprises people. With the
simple partition scheme, every element compares equal to the pivot, they all go to one side, and you
get the `O(n²)` behaviour again on input that is trivially sorted.

The fix is a **three-way partition**: split into *less than*, *equal to*, and *greater than*, and
recurse only into the outer two. All the equal values land in their final positions at once. This is
the Dutch national flag problem and it is worth having in your hands — it turns a list of one million
identical values from `O(n²)` into `O(n)`.

### The two things quicksort gives up

- **It is not stable.** Partitioning swaps elements across long distances, so equal elements change
  relative order. Merge sort is stable; quicksort is not, and no simple fix keeps its in-place
  property.
- **The worst case is real.** `O(n²)` is not merely theoretical if the pivot rule is deterministic
  and the input can be chosen by someone else. There was a well-known denial-of-service class of bug
  built exactly on this.

### The thing it gives you

**Speed, from staying in place.** Quicksort touches memory that is already nearby, so the processor's
memory cache — the small fast store described on
[day 003](../day-003-big-o-in-plain-english/README.md) — keeps working for it. Merge sort allocates
new lists at every level and walks between them. Both are `n log n`, and quicksort is typically two
to three times faster in wall-clock time on an array of numbers.

---

## 4. The picture

One partition, step by step. The pivot is the last element; `i` marks the boundary of the
"smaller" region, and `j` scans:

```
 pivot = 3 (the last element)

 index    0    1    2    3    4    5    6
        +----+----+----+----+----+----+----+
        |  7 |  2 |  9 |  4 |  1 |  8 |  3 |
        +----+----+----+----+----+----+----+
          ^                              ^
          i                            pivot
          j scans from 0 to 5

 j=0  7 > 3   leave it.               i stays at 0
 j=1  2 < 3   swap nums[0], nums[1] -> [2, 7, 9, 4, 1, 8, 3],  i -> 1
 j=2  9 > 3   leave it.
 j=3  4 > 3   leave it.
 j=4  1 < 3   swap nums[1], nums[4] -> [2, 1, 9, 4, 7, 8, 3],  i -> 2
 j=5  8 > 3   leave it.

 finally, swap the pivot into position i:
        swap nums[2], nums[6]        -> [2, 1, 3, 4, 7, 8, 9]
                        ^
                      pivot is HOME at index 2

 index    0    1    2    3    4    5    6
        +----+----+----+----+----+----+----+
        |  2 |  1 |  3 |  4 |  7 |  8 |  9 |
        +----+----+----+----+----+----+----+
          \_______/   ^    \______________/
           < pivot  FINAL       > pivot
           (unsorted)          (unsorted)
```

**What to notice:** `i` is not a scanner, it is a **boundary**. Everything before `i` is known to be
smaller than the pivot; everything from `i` to `j` is known to be larger. The invariant is the whole
trick, and it is the thing to state out loud before you write the loop.

A good pivot against a bad one, drawn as trees:

```
 GOOD: pivot is the median every time
                       [ 8 elements ]
                     /                \
              [ 4 ]                    [ 4 ]  (minus the pivot)
             /     \                  /     \
          [ 2 ]   [ 2 ]            [ 2 ]   [ 2 ]

  depth = log2(8) = 3.   Work per level = n.   Total = n log n.


 BAD: pivot is the smallest value every time (sorted input, first-element pivot)
       [ 8 ]
          \
          [ 7 ]
             \
             [ 6 ]
                \
                [ 5 ]
                   \
                   [ 4 ] ... and so on

  depth = n = 8.   Work per level = n, n-1, n-2 ...   Total = n(n-1)/2 = n^2.
```

**What to notice:** the good tree is bushy and shallow; the bad one is a straight line. The total
work per level is the same in both — the difference is entirely the number of levels, and the pivot
choice decides that.

Three-way partitioning, for when duplicates are everywhere:

```
 before   [ 2 , 5 , 2 , 9 , 2 , 1 , 2 ]        pivot value = 2

 after    [ 1 | 2 , 2 , 2 , 2 | 9 , 5 ]
            ^   \___________/   ^
          less     EQUAL       greater
                 all four in their FINAL positions at once

 recurse into  [1]  and  [9, 5]  only.
 With a two-way partition, those four 2s would be split and re-split
 log n times for nothing.
```

**What to notice:** the equal block is skipped entirely by the recursion. A list of a million
identical values goes from `O(n²)` to a single `O(n)` pass.

---

## 5. The code, built step by step

### The partition, on its own

This is the Lomuto scheme — one scanning position, one boundary. It is the one to write in an
interview because the loop has a single moving part.

```python
def partition(nums: list[int], lo: int, hi: int) -> int:
    """Rearrange nums[lo:hi+1] around nums[hi]. Return the pivot's final position."""
    pivot = nums[hi]
    i = lo                                     # boundary: everything < i is smaller
    for j in range(lo, hi):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]      # put the pivot at the boundary
    return i
```

Read the invariant, because it is what makes the code obviously correct: **at every point in the
loop, `nums[lo:i]` holds values smaller than the pivot and `nums[i:j]` holds values that are not.**
When `j` reaches `hi`, everything has been classified, and swapping the pivot into position `i` puts
it exactly between the two groups.

The returned value is the pivot's final position. That is the only thing the caller needs.

### The sort

```python
def quicksort(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Sorts in place. Average O(n log n); worst case O(n^2) with a fixed pivot."""
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:                               # 0 or 1 elements: nothing to do
        return
    p = partition(nums, lo, hi)
    quicksort(nums, lo, p - 1)                 # NOT p -- the pivot is already home
    quicksort(nums, p + 1, hi)
```

Note `p - 1` and `p + 1`. The pivot is finished, so it is excluded from both sides. Writing
`quicksort(nums, lo, p)` instead is the classic infinite-recursion bug, and the error is in §7.

Note also that `lo >= hi` is the base case rather than `lo == hi`. An empty range has `lo > hi`, which
happens whenever the pivot lands at either end.

### Randomising the pivot, which is not optional

```python
import random

def partition_random(nums: list[int], lo: int, hi: int) -> int:
    r = random.randint(lo, hi)                 # choose a position, not a value
    nums[r], nums[hi] = nums[hi], nums[r]      # move it to the end, then proceed as before
    return partition(nums, lo, hi)
```

Two lines, and they change the worst case from "sorted input" to "an outcome with probability
roughly `1 / n!`". Say why it works: the running time now depends on the random numbers, not on the
arrangement of the input, so **no particular input is bad** — a person who can choose your input
cannot choose your dice.

### Median of three, the deterministic alternative

```python
def median_of_three(nums: list[int], lo: int, hi: int) -> None:
    """Put the median of nums[lo], nums[mid], nums[hi] at position hi."""
    mid = (lo + hi) // 2
    a, b, c = nums[lo], nums[mid], nums[hi]
    if (a <= b <= c) or (c <= b <= a):
        nums[mid], nums[hi] = nums[hi], nums[mid]
    elif (b <= a <= c) or (c <= a <= b):
        nums[lo], nums[hi] = nums[hi], nums[lo]
```

Cheap and it kills the sorted-input case completely, since the middle element of a sorted range *is*
the median. It does not survive a deliberately constructed input, which is why library
implementations combine it with a depth limit.

### Three-way partitioning, for duplicates

```python
def quicksort_three_way(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Dutch national flag. O(n) on a list of identical values."""
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return
    pivot = nums[random.randint(lo, hi)]
    lt, i, gt = lo, lo, hi                     # [lo,lt) < pivot, [lt,i) == pivot, (gt,hi] > pivot
    while i <= gt:
        if nums[i] < pivot:
            nums[lt], nums[i] = nums[i], nums[lt]
            lt, i = lt + 1, i + 1
        elif nums[i] > pivot:
            nums[i], nums[gt] = nums[gt], nums[i]
            gt -= 1                            # i does NOT advance -- the swapped-in value is new
        else:
            i += 1
    quicksort_three_way(nums, lo, lt - 1)
    quicksort_three_way(nums, gt + 1, hi)
```

The line people get wrong is `gt -= 1` without advancing `i`. The value that was just swapped in from
the right end has never been looked at, so `i` must stay where it is and examine it next time round.

### Keeping the recursion depth at `O(log n)`

Worst-case recursion depth is `O(n)`, which raises `RecursionError` in Python on large inputs. The
standard fix is to recurse into the **smaller** side and loop on the larger one:

```python
def quicksort_bounded(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Recursion depth is O(log n) even in the worst case."""
    if hi is None:
        hi = len(nums) - 1
    while lo < hi:
        p = partition_random(nums, lo, hi)
        if p - lo < hi - p:                    # recurse into the smaller half
            quicksort_bounded(nums, lo, p - 1)
            lo = p + 1                         # loop on the larger half
        else:
            quicksort_bounded(nums, p + 1, hi)
            hi = p - 1
```

Because the recursive call always gets at most half the range, the depth cannot exceed `log₂ n`. The
time complexity is unchanged; only the stack is bounded. This is a good thing to mention unprompted.

### The complete file

```python
"""Quicksort: partition in place, recurse into both sides, and choose the pivot properly."""

import random


def partition(nums: list[int], lo: int, hi: int) -> int:
    """Lomuto. Rearrange nums[lo..hi] around nums[hi]; return the pivot's final index.

    Invariant: nums[lo:i] < pivot, and nums[i:j] >= pivot.
    """
    pivot = nums[hi]
    i = lo
    for j in range(lo, hi):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i


def partition_random(nums: list[int], lo: int, hi: int) -> int:
    """Same, with a randomly chosen pivot -- so no fixed input is a bad input."""
    r = random.randint(lo, hi)
    nums[r], nums[hi] = nums[hi], nums[r]
    return partition(nums, lo, hi)


def partition_hoare(nums: list[int], lo: int, hi: int) -> int:
    """Hoare's original: two positions walking toward each other.

    Does about 3x fewer swaps than Lomuto. Returns a SPLIT POINT, not the pivot's
    index -- so the caller must recurse on [lo, p] and [p+1, hi], not p-1 and p+1.
    """
    pivot = nums[(lo + hi) // 2]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while nums[i] < pivot:
            i += 1
        j -= 1
        while nums[j] > pivot:
            j -= 1
        if i >= j:
            return j
        nums[i], nums[j] = nums[j], nums[i]


def quicksort(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """In place. Expected O(n log n), worst case O(n^2). Not stable.

    Recursion depth is bounded to O(log n) by always recursing into the smaller side.
    """
    if hi is None:
        hi = len(nums) - 1
    while lo < hi:
        p = partition_random(nums, lo, hi)
        if p - lo < hi - p:
            quicksort(nums, lo, p - 1)
            lo = p + 1
        else:
            quicksort(nums, p + 1, hi)
            hi = p - 1


def quicksort_three_way(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Dutch national flag partitioning. O(n) when the values are mostly duplicates."""
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return
    pivot = nums[random.randint(lo, hi)]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if nums[i] < pivot:
            nums[lt], nums[i] = nums[i], nums[lt]
            lt, i = lt + 1, i + 1
        elif nums[i] > pivot:
            nums[i], nums[gt] = nums[gt], nums[i]
            gt -= 1
        else:
            i += 1
    quicksort_three_way(nums, lo, lt - 1)
    quicksort_three_way(nums, gt + 1, hi)


def sort_colors(nums: list[int]) -> None:
    """LeetCode 75. Exactly a three-way partition around the value 1, in one pass."""
    low, i, high = 0, 0, len(nums) - 1
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low, i = low + 1, i + 1
        elif nums[i] == 2:
            nums[i], nums[high] = nums[high], nums[i]
            high -= 1
        else:
            i += 1


if __name__ == "__main__":
    data = [7, 2, 9, 4, 1, 8, 3]

    trial = list(data)
    p = partition(trial, 0, len(trial) - 1)
    print(p, trial)                       # 2 [2, 1, 3, 4, 7, 8, 9]  -- pivot 3 is home

    trial = list(data)
    quicksort(trial)
    print(trial)                          # [1, 2, 3, 4, 7, 8, 9]

    trial = [4, 4, 4, 4, 4, 4]
    quicksort_three_way(trial)
    print(trial)                          # [4, 4, 4, 4, 4, 4]  -- in ONE pass

    colors = [2, 0, 2, 1, 1, 0]
    sort_colors(colors)
    print(colors)                         # [0, 0, 1, 1, 2, 2]

    # the worst case, made visible
    def count_comparisons(nums: list[int], first_pivot: bool) -> int:
        count = 0

        def go(lo: int, hi: int) -> None:
            nonlocal count
            if lo >= hi:
                return
            if first_pivot:
                nums[lo], nums[hi] = nums[hi], nums[lo]   # pivot = the FIRST element
            else:
                r = random.randint(lo, hi)
                nums[r], nums[hi] = nums[hi], nums[r]
            count += hi - lo
            p = partition(nums, lo, hi)
            go(lo, p - 1)
            go(p + 1, hi)

        go(0, len(nums) - 1)
        return count

    import sys
    sys.setrecursionlimit(10000)
    print(count_comparisons(list(range(500)), first_pivot=True))    # 124750  = n(n-1)/2
    print(count_comparisons(list(range(500)), first_pivot=False))   # ~4000   = ~n log2 n
```

---

## 6. What it costs

### The average case, counted

Partitioning a range of `m` elements costs `m − 1` comparisons: every element except the pivot is
compared with the pivot exactly once.

If the pivot lands near the middle each time, the picture is merge sort's picture:

```
 level 0:  1 partition  of n        =  n comparisons
 level 1:  2 partitions of n/2      =  n
 level 2:  4 partitions of n/4      =  n
   ...
 depth log2(n) levels

 total = n x log2(n)
```

```
 n =     1,000  ->  ~10,000 comparisons
 n = 1,000,000  ->  ~20,000,000
```

The exact expected number with a random pivot is about `1.39 n log₂ n` — roughly 39% more
comparisons than merge sort's `n log₂ n`. Quicksort is still faster in practice because it does no
allocation and its memory access pattern is friendlier, so each comparison is cheaper.

### The worst case, counted

Pivot always smallest (or always largest):

```
 level 0:  partition of n      = n-1 comparisons
 level 1:  partition of n-1    = n-2
 level 2:  partition of n-2    = n-3
   ...
 depth = n levels

 total = (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n^2)
```

```
 n = 500 sorted values, first-element pivot : 124,750 comparisons
 n = 500 sorted values, random pivot        :   ~4,000 comparisons

 31x more work, on the input people are most likely to hand you.
```

### How unlikely is the bad case, really?

With a random pivot, the probability that every one of the `n` partitions is maximally unbalanced is
astronomically small — on the order of `1/n!`. A more useful number is that the probability of
exceeding `2 × 1.39 n log₂ n` comparisons is below one in a million for `n` in the thousands.

```
 n = 1,000,000, random pivot:
   expected comparisons              ~ 28,000,000
   P(more than 2x the expectation)   < 1 in 10^6

 Compare: the chance of a specific bit in RAM flipping from cosmic radiation
 in an hour is higher than that.
```

That is the honest way to say "expected `O(n log n)`". It is not a guarantee, and if the requirement
is a guarantee, use merge sort or heapsort.

### The duplicates case

```
 1,000,000 identical values:

 two-way partition   : every element goes to one side  -> n(n-1)/2 = 5 x 10^11 comparisons
 three-way partition : one pass, all equal values placed -> 1,000,000 comparisons

 500,000x difference on input that requires no sorting at all.
```

### Space

```
 data       : O(1) extra -- it sorts in place, unlike merge sort's O(n)
 call stack : O(log n) if you recurse into the smaller side
              O(n)     if you do not, and that raises RecursionError in Python
```

The `O(1)` data space is the reason quicksort exists. Say it as the direct contrast with yesterday:
**merge sort buys a guaranteed worst case with `O(n)` memory; quicksort buys `O(1)` memory and speed
by giving the guarantee up.**

---

## 7. The traps

### The real error: recursing on the pivot itself

```python
def quicksort_broken(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return
    p = partition(nums, lo, hi)
    quicksort_broken(nums, lo, p)        # <-- should be p - 1
    quicksort_broken(nums, p + 1, hi)

quicksort_broken([2, 1])
```

```
Traceback (most recent call last):
  File "day54.py", line 9, in <module>
    quicksort_broken([2, 1])
    ~~~~~~~~~~~~~~~~^^^^^^^^
  File "day54.py", line 7, in quicksort_broken
    quicksort_broken(nums, lo, p)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

If the pivot lands at position `lo`, then `quicksort(nums, lo, p)` is the same range you started
with, and nothing shrinks. **The pivot is finished — exclude it from both sides.** This is the
single commonest quicksort bug.

### The real error: `O(n²)` on sorted input, in the wild

```python
import sys
sys.setrecursionlimit(2000)

def quicksort_first_pivot(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return
    nums[lo], nums[hi] = nums[hi], nums[lo]      # pivot = the first element
    p = partition(nums, lo, hi)
    quicksort_first_pivot(nums, lo, p - 1)
    quicksort_first_pivot(nums, p + 1, hi)

quicksort_first_pivot(list(range(5000)))          # an already sorted list
```

```
Traceback (most recent call last):
  File "day54.py", line 14, in <module>
    quicksort_first_pivot(list(range(5000)))
  File "day54.py", line 11, in quicksort_first_pivot
    quicksort_first_pivot(nums, p + 1, hi)
  [Previous line repeated 1994 more times]
RecursionError: maximum recursion depth exceeded
```

Read what happened: sorting an **already sorted list** crashed. Every partition put the pivot at the
left end, so the right side shrank by exactly one each time and the recursion went 5,000 deep. In a
language without a recursion limit it would not crash — it would just take `n²` time and look like a
hang. **Two lines of randomisation prevent this entirely.**

### The near-miss: `<=` instead of `<` in the partition

```python
if nums[j] <= pivot:        # <-- was <
```

The sort still produces correct output. But on a list where every value is equal, every element now
satisfies the condition, `i` advances every time, and the pivot ends up at the far right — one side
empty, `O(n²)`, on input that needs no work at all:

```python
quicksort_le(list([7] * 3000))
```

```
RecursionError: maximum recursion depth exceeded
```

With strict `<`, equal values are left in place and the pivot lands in the middle of them, which
splits the range roughly in half. It is one character, and it decides whether a million duplicates
take one second or five days.

### The trap: assuming Hoare's partition returns the pivot's index

```python
p = partition_hoare(nums, lo, hi)
quicksort(nums, lo, p - 1)          # <-- WRONG for Hoare
quicksort(nums, p + 1, hi)
```

Hoare's scheme returns a **split point**, not the pivot's final position — the pivot may be anywhere
in either part. The correct recursion is `(lo, p)` and `(p + 1, hi)`. Mixing the two schemes' calling
conventions produces a sort that is wrong on some inputs and right on others, which is the worst kind
of bug. Pick one scheme, and say which one you are writing.

### The trap: claiming quicksort is stable

It is not. Partitioning swaps elements across arbitrary distances:

```python
pairs = [(3, "first"), (1, "x"), (3, "second")]
# a quicksort by the number can produce:
[(1, 'x'), (3, 'second'), (3, 'first')]
```

The two 3s have swapped. If you need stability — sorting by a second key after a first, as on
[day 051](../day-051-why-sorting-matters/README.md) — quicksort is the wrong choice and merge sort
is the right one.

### The trap: `random.shuffle` instead of a random pivot

Shuffling the whole list first also defeats the sorted-input case, and it is `O(n)`, so it does not
change the complexity. But it destroys any existing partial order, which makes the sort slower on
nearly-sorted data, and it changes the caller's list in a way they may not expect. Randomise the
pivot, not the input.

---

## 8. In the interview

### How it gets asked

- *"Write quicksort."* — asked as often as merge sort, and the partition is what they watch.
- *"What is quicksort's worst case, and when does it happen?"* — `O(n²)`, on already-sorted input
  with a first-element or last-element pivot. Say *sorted* out loud; that is the part candidates miss.
- *"How do you avoid the worst case?"* — random pivot, and be able to explain *why* randomising
  works.
- *"Quicksort or merge sort?"* — the comparison question. In place and fast against guaranteed and
  stable.
- *"Sort an array of 0s, 1s and 2s in one pass."* — LeetCode 75, which is exactly a three-way
  partition.
- *"Partition an array around a value."* — the partition alone, which is also the engine of
  quickselect tomorrow.

### What to say out loud, in the first ninety seconds

1. **Name the one idea before writing.** *"Quicksort is really one operation — partition. I pick a
   pivot and rearrange so everything smaller is left of it and everything larger is right of it.
   After that the pivot is in its final position and I never touch it again."*
2. **State the partition invariant.** *"I'll keep a boundary `i`. Everything before `i` is smaller
   than the pivot; everything from `i` up to the scanner is not."*
3. **Randomise the pivot before you are asked.** *"I'll pick a random position and swap it to the
   end. Otherwise a sorted input gives O(n²), and sorted input is common."*
4. **Say what happens to the pivot in the recursion.** *"I recurse on `lo` to `p-1` and `p+1` to
   `hi` — the pivot is excluded, because it's finished. Including it is an infinite recursion."*
5. **Volunteer the properties.** *"In place, O(1) extra data space, O(log n) stack if I recurse into
   the smaller side. Expected O(n log n), worst case O(n²). Not stable."*

### The follow-ups

**"What is the worst case, and what input causes it?"**
`O(n²)`, and it happens when the pivot is the smallest or largest value in the range every time,
because then one side of the partition is empty and the other has `n−1` elements, so the recursion is
`n` levels deep instead of `log n`, with `n`, `n−1`, `n−2` … comparisons per level — that sum is
`n(n−1)/2`. The input that causes it is the one people find surprising: if the pivot rule is "take
the first element" or "take the last element", then an **already sorted** array is the worst case,
and so is a reverse-sorted one. That is not a rare input; it is one of the most likely inputs a
function ever receives. The second worst case is an array where all the values are equal, if the
partition uses `<=` rather than `<` — every element goes to one side and you get the same quadratic
behaviour on data that needs no sorting at all. In Python both of those manifest as `RecursionError`
rather than slowness, because the recursion goes `n` deep and the default limit is a thousand frames.

**"How do you avoid it?"**
Three answers, and I would give them in this order. First, choose the pivot position at random and
swap it to the end before partitioning — two lines. That works because the running time now depends
on my random numbers rather than on the arrangement of the input, so there is no *particular* input
that is bad; the probability of hitting the quadratic case is on the order of `1/n!`, and the
probability of exceeding twice the expected comparison count is under one in a million for realistic
sizes. That distinction matters if the input can come from outside the system, because a
deterministic pivot rule is something an attacker can construct against, and that has been a real
denial-of-service class of bug. Second, median-of-three: take the first, middle and last elements and
use the median of those. It is deterministic and cheap and it completely kills the sorted-input case,
since the middle element of a sorted range *is* the median — but someone who knows the rule can still
build a bad input. Third, and this is what production libraries actually do: introsort. Count the
recursion depth, and if it exceeds about `2 log₂ n`, abandon quicksort for that subrange and finish
with heapsort. That gives a hard `O(n log n)` guarantee with quicksort's constant factor almost
everywhere, and it is what `std::sort` in C++ does. I would also mention the separate fix for
duplicates — three-way partitioning, which puts all the equal values in their final positions at once
and turns a million identical values from `O(n²)` into a single linear pass.

**"Quicksort or merge sort? Justify it."**
Quicksort for arrays in memory, merge sort when I need a guarantee or stability or the data does not
fit. The case for quicksort is the constant factor: it sorts in place, so it needs `O(1)` extra data
space instead of merge sort's `O(n)`, and it keeps touching memory that is already close by, which
means the processor cache stays useful — in practice that is a two-to-three-times speed difference on
the same array even though both are `n log n`. Interestingly quicksort does *more* comparisons on
average, about `1.39 n log₂ n` against merge sort's `n log₂ n`; it wins anyway because each
comparison is cheaper and there is no allocation. What I give up is the guarantee — the worst case is
`O(n²)`, and a randomised pivot makes it very unlikely rather than impossible — and stability, which
quicksort cannot provide, because partitioning swaps elements across long distances. So I choose
merge sort in three situations. When the input could be chosen adversarially and a rare quadratic
case would be an outage rather than a slow query. When I need stability, for instance sorting records
by a second key after a first. And when the data is a linked list or does not fit in memory, because
merging is sequential and quicksort needs random access — external sorting and linked-list sorting
are both merge sort. In Python, of course, I would call `sorted()`, which is Timsort: stable,
adaptive, `O(n log n)` worst case, and written in C.

### A model answer

> "Quicksort is one operation repeated. I pick a value called the pivot, then rearrange the array so
> that everything smaller than it comes before it and everything larger comes after — that step is
> called partitioning. Once it's done, the pivot is in its final sorted position and I never look at
> it again, and the two sides are independent subproblems.
>
> ```python
> def partition(nums: list[int], lo: int, hi: int) -> int:
>     pivot = nums[hi]
>     i = lo                              # boundary: nums[lo:i] is all < pivot
>     for j in range(lo, hi):
>         if nums[j] < pivot:
>             nums[i], nums[j] = nums[j], nums[i]
>             i += 1
>     nums[i], nums[hi] = nums[hi], nums[i]
>     return i
>
> def quicksort(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
>     if hi is None:
>         hi = len(nums) - 1
>     if lo >= hi:
>         return
>     r = random.randint(lo, hi)
>     nums[r], nums[hi] = nums[hi], nums[r]     # random pivot -- not optional
>     p = partition(nums, lo, hi)
>     quicksort(nums, lo, p - 1)
>     quicksort(nums, p + 1, hi)
> ```
>
> The invariant in the partition is that everything before `i` is smaller than the pivot, and
> everything from `i` to `j` is not — so when the scan finishes, swapping the pivot into `i` puts it
> exactly between the two groups. And the recursion excludes the pivot: `p - 1` and `p + 1`. If I
> wrote `quicksort(nums, lo, p)` and the pivot happened to land at `lo`, the range wouldn't shrink and
> it would recurse forever.
>
> I randomised the pivot deliberately, and I'd say why. The worst case is O(n²), and it happens when
> the pivot is the smallest or largest value every time — which, with a first- or last-element pivot,
> means an already sorted array. That's a common input, not a rare one. Randomising means the running
> time depends on my dice rather than on the input's arrangement, so no particular input is bad.
>
> Cost: expected O(n log n) — about 1.39 n log₂ n comparisons — worst case O(n²), O(1) extra data
> space, and O(log n) stack depth if I always recurse into the smaller side and loop on the larger.
> It is not stable, because partitioning swaps across long distances. If I needed a guaranteed worst
> case or stability I'd use merge sort, and if the array were full of duplicates I'd switch to a
> three-way partition, which places all the equal values at once and turns that case from O(n²) into
> a single linear pass."

---

## 9. Recall card

- **Quicksort is one operation: partition.** Pick a pivot, rearrange so smaller is left and larger is
  right — the pivot is then in its **final** position, and the two sides are independent. No merge
  step; the work happens on the way *down*, which is why it sorts **in place**.
- **The invariant to say out loud:** `nums[lo:i]` is all `< pivot`, `nums[i:j]` is all `>= pivot`;
  at the end swap the pivot into `i`. Recurse on `p-1` and `p+1` — **excluding the pivot**, or it
  recurses forever.
- **Worst case O(n²), and the input is an already sorted list** with a first- or last-element pivot:
  one side empty, depth n, n(n−1)/2 comparisons. 500 sorted values: 124,750 comparisons against
  ~4,000 with a random pivot.
- **Fix it with two lines of randomisation** — the time now depends on your dice, not on the input,
  so no *particular* input is bad. Then median-of-three (deterministic, beatable) and **introsort**
  (bail to heapsort past depth 2 log n — what `std::sort` does). Separately, **three-way partition**
  for duplicates: a million equal values goes from O(n²) to one pass.
- **Against merge sort:** quicksort is in place (O(1) data, O(log n) stack if you recurse into the
  smaller side) and 2-3× faster despite ~39% more comparisons. It gives up the **guarantee** and
  **stability**. Choose merge sort for adversarial input, multi-key sorting, linked lists, and data
  too big for memory.
