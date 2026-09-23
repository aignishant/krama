---
day: 55
track: dsa
title: "Quickselect: finding the Kth largest without sorting"
phase: "Sorting"
status: written
---

# Day 055 · DSA — Quickselect: finding the Kth largest without sorting

**After today you can:** You can find the Kth largest in expected O(n) and say why the expectation matters.

**The interviewer asks it as:** *Find the Kth largest element. Can you beat O(n log n)?*

---

## 1. What this is, and why they ask it

Quickselect finds the k-th smallest or k-th largest value in a list without sorting the list. It uses
exactly the partition step from [day 054](../day-054-quicksort/README.md), and it makes one change
that changes everything: after partitioning, you know which side of the pivot the answer is on, so
you **throw the other side away** instead of recursing into it. That one difference takes the cost
from `O(n log n)` down to an expected `O(n)`.

They ask it because "find the k-th largest" is one of the most common medium-difficulty interview
questions there is — LeetCode 215, asked at almost every product company — and because it has three
correct answers with different costs. Sorting is `O(n log n)` and everybody gets there. A heap of
size `k` is `O(n log k)` and most good candidates get there. Quickselect is `O(n)` expected, and
getting there means you understood that you were being asked for *one* value rather than an ordering.
The follow-ups are predictable and sharp: what is the worst case, why does randomising help, what
does "expected" actually promise, and when would you choose the heap anyway. This is also the last
new sorting-family algorithm in the phase, and it is the one that shows sorting is sometimes more
than you needed.

---

## 2. The story

Zubeida runs the auditions for the annual day dance item at a school in Hyderabad, and this year a
hundred and eighty girls signed up for eight places in the troupe.

She had two afternoons. In her first year she tried to do it properly — watch everybody, put them in
order from best to worst, and take the top eight. She got about forty in and realised she was arguing
with herself about whether number seventeen was better than number twenty-three, which was a
completely useless thing to be deciding, because neither of them was getting in.

So the second year she did it differently, and now she does it this way every time.

She calls up one girl, more or less at random from the middle of the list, and watches her do the
piece. That girl becomes the mark. This year it was a girl called Sania, and Sania was decent —
neither obviously brilliant nor obviously struggling.

Then everybody else dances, one after another, and Zubeida makes exactly one decision about each of
them. Better than Sania, or not as good as Sania. That is all. She does not compare anyone with
anyone else, and she does not put the "better" group in any kind of order. Two groups, one look each.

At the end of the afternoon there were thirty-one girls in the better group and a hundred and
forty-eight in the other one, and Sania in between.

And here is the thing she does that saves her the second afternoon. The eight places have to come out
of those thirty-one. All of them. There is no argument to be had about the hundred and forty-eight —
not one of them is going to be in the top eight, and it does not matter in the slightest which of
them is better than which. She thanks them and they go home, and she never thinks about them again.

Then she does exactly the same thing inside the thirty-one. Picks one, makes it the mark, splits them
into better and worse, and drops whichever half cannot contain the eighth place. Thirty-one becomes
eleven. Eleven becomes eight.

Her sister asked her once whether it would go wrong if she picked badly, and it does. One year she
happened to choose a girl who turned out to be the strongest dancer of the lot, so everybody went
into the "not as good" group and nothing was eliminated at all. She had spent an hour and cut the
field by one. She just started again with someone else. Now she deliberately picks from the middle of
the list rather than from the top of it, where the keen ones sign up first.

---

## 3. The idea in plain English

Zubeida is running quickselect. Sania is the pivot. Splitting the girls into "better" and "not as
good" is the partition. And thanking a hundred and forty-eight girls and never thinking about them
again is the one step that separates today from yesterday.

### The problem

Given a list of numbers and a number `k`, find the k-th largest value. For
`nums = [3, 2, 1, 5, 6, 4]` and `k = 2`, the answer is `5` — the second largest.

Note what is *not* being asked. You are not asked for the whole order. You are not even asked for the
top `k`. You are asked for **one value**. Any work that produces more than that is work you did not
have to do, and noticing that is the entire insight.

### The three answers, in the order candidates find them

**One: sort and take it.** `sorted(nums)[-k]`. Correct, `O(n log n)`, one line. Always say this
first — it is the baseline, it takes five seconds, and starting from a correct answer is better than
starting from a clever one.

**Two: a heap of size k.** Keep the `k` largest values seen so far in a structure that can cheaply
give up its smallest. That is `O(n log k)`, and in Python it is
`heapq.nlargest(k, nums)[-1]`. Heaps arrive properly on
[day 113](../day-113-the-heap/README.md); today, know the cost and that the library call exists.

**Three: quickselect.** `O(n)` expected. This is the answer they are fishing for.

### The one idea

Partition the list around a pivot, exactly as yesterday. The pivot lands at some position `p`, and
after partitioning you know three things:

- everything before `p` is smaller than the pivot,
- everything after `p` is larger,
- **the pivot is at its final sorted position.**

That last fact is the key. If you are looking for the value that belongs at position `target`, then:

```
 p == target   ->  the pivot IS the answer. Stop. Return it.
 p >  target   ->  the answer is to the LEFT.  Search lo..p-1.  Discard everything right.
 p <  target   ->  the answer is to the RIGHT. Search p+1..hi.  Discard everything left.
```

Quicksort recurses into **both** sides. Quickselect recurses into **one**. That is the whole
difference, and it is the sentence to say out loud.

### Turning "k-th largest" into a position

This is where people make an off-by-one error, so do it deliberately and out loud.

In a list sorted ascending, of length `n`:

- the 1st **smallest** is at position `0`, so the k-th smallest is at position `k - 1`;
- the 1st **largest** is at position `n - 1`, so the k-th largest is at position `n - k`.

```
 nums   = [3, 2, 1, 5, 6, 4]           n = 6
 sorted = [1, 2, 3, 4, 5, 6]
 index     0  1  2  3  4  5

 k = 2 (second largest) -> target index = n - k = 6 - 2 = 4 -> value 5.  Correct.
 k = 1 (largest)        -> target index = 5                 -> value 6.  Correct.
 k = 6 (smallest)       -> target index = 0                 -> value 1.  Correct.
```

Write `target = len(nums) - k` on the board before writing the loop, and check it against `k = 1` and
`k = n`. That takes ten seconds and prevents the commonest failure on this problem.

### Why throwing half away gives you `O(n)`

The arithmetic is short and it is the answer to the main follow-up.

Partitioning `n` elements costs `n` comparisons. If the pivot lands near the middle, the next
partition is on `n/2` elements, then `n/4`, and so on — because each time you discard one side:

```
 n + n/2 + n/4 + n/8 + ... + 1  =  2n
```

That sum is one of the few pieces of arithmetic worth memorising, because it appears everywhere.
Halving repeatedly and adding it all up gives you **twice the first term**, not `n log n`. So
quickselect is `O(n)`.

Compare it with quicksort, which does not discard:

```
 quicksort   : n + (n/2 + n/2) + (n/4 x 4) + ...  = n per level x log n levels = n log n
 quickselect : n +  n/2        +  n/4      + ...  = 2n
```

The whole `log n` factor disappears because only one branch survives at each level.

### The catch, said plainly

Quickselect is `O(n)` **expected**, not guaranteed. If the pivot is the largest or smallest value
every time, each partition removes exactly one element and you are back to
`n + (n−1) + (n−2) + … = O(n²)`. That is Zubeida's bad year, when she picked the best dancer as the
mark and eliminated nobody.

The fix is the same as yesterday: **choose the pivot at random.** Then the running time depends on
your random numbers rather than on the arrangement of the input, so there is no particular input that
is bad.

There is also a deterministic worst-case `O(n)` method — **median of medians**, which chooses a pivot
guaranteed to be near the middle by splitting the list into groups of five, taking each group's
median, and recursively taking the median of those. It genuinely gives `O(n)` in the worst case. It
is also so much slower in practice, because of the constant factor, that nobody uses it for real
selection. Know the name, know that it exists, and say you would use the randomised version.

---

## 4. The picture

One run, looking for the 2nd largest of six values:

```
 nums = [ 3, 2, 1, 5, 6, 4 ]   n = 6, k = 2  ->  target index = 6 - 2 = 4

 STEP 1   partition the whole range around pivot 4 (say the random choice landed there)

          [ 3, 2, 1, 4, 6, 5 ]
                     ^
                   p = 3          p (3) < target (4)  ->  answer is to the RIGHT
                                  DISCARD indices 0..3 -- four values, gone forever
          [ x, x, x, x, 6, 5 ]
                        ^--^
                    search here

 STEP 2   partition indices 4..5 around pivot 5

          [ x, x, x, x, 5, 6 ]
                        ^
                      p = 4       p (4) == target (4)  ->  STOP
                                  the answer is nums[4] = 5
```

**What to notice:** step 1 threw away four of the six values after a single pass, and nothing in that
discarded half was ever compared with anything again. Notice also that the list is left in a strange
half-sorted state — quickselect mutates its input and does not sort it, which is a real property to
mention.

Quicksort against quickselect, drawn as the shape of the recursion:

```
 QUICKSORT — both sides survive                QUICKSELECT — one side survives

          [ n elements ]                              [ n elements ]
           /          \                                /          \
      [ n/2 ]      [ n/2 ]                        [ n/2 ]        (gone)
       /   \        /   \                          /   \
   [n/4] [n/4]  [n/4] [n/4]                    (gone)  [ n/4 ]
                                                          \
                                                        [ n/8 ]

 work: n per level x log n levels           work: n + n/2 + n/4 + ... = 2n
     = n log n                                  = O(n)
```

**What to notice:** the left tree is bushy and the right one is a single path. The `log n` factor in
quicksort comes from the number of *levels* multiplied by full work at each level; quickselect has
the same number of levels but the work halves down each one, and a halving sum converges.

The three answers, priced on the same input:

```
 n = 1,000,000 values, k = 10

 sort then index      1,000,000 x 20  =  20,000,000 operations   O(n log n)
 heap of size k       1,000,000 x 3.3 =   3,300,000              O(n log k)
 quickselect          ~2 x 1,000,000  =   2,000,000              O(n) expected

 and if k = 500,000 (the median):
 sort                 20,000,000                                 O(n log n)
 heap of size k       1,000,000 x 19  =  19,000,000              O(n log k) -- no better
 quickselect          ~2,000,000                                 O(n) -- unchanged
```

**What to notice:** the heap's advantage disappears as `k` grows, because `log k` approaches
`log n`. Quickselect does not care what `k` is. That is the case to raise when the interviewer asks
"what if k is n/2".

---

## 5. The code, built step by step

### The partition, unchanged from yesterday

```python
import random

def partition(nums: list[int], lo: int, hi: int) -> int:
    """Rearrange nums[lo..hi] around a random pivot. Return the pivot's final index."""
    r = random.randint(lo, hi)
    nums[r], nums[hi] = nums[hi], nums[r]       # random pivot, moved to the end
    pivot = nums[hi]
    i = lo
    for j in range(lo, hi):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i
```

This is exactly the code from [day 054](../day-054-quicksort/README.md), with the randomisation built
in rather than bolted on. Nothing about it changes for selection.

### The select, recursive

```python
def select(nums: list[int], lo: int, hi: int, target: int) -> int:
    """The value that would sit at index `target` if nums were sorted."""
    if lo == hi:
        return nums[lo]                          # one element left: it must be the answer
    p = partition(nums, lo, hi)
    if p == target:
        return nums[p]                           # the pivot IS the answer
    if target < p:
        return select(nums, lo, p - 1, target)   # discard everything from p rightwards
    return select(nums, p + 1, hi, target)       # discard everything from p leftwards
```

Read the three branches out loud as you write them. **Exactly one recursive call in each path** —
that is the whole difference from quicksort, and it is worth pointing at.

The base case is `lo == hi`, a single element. It cannot be `lo >= hi` returning something else,
because the range always contains the target by construction, so it is never empty.

### The iterative version, which is better

Because there is only one recursive call and it is the last thing the function does, the recursion
can be replaced by a loop mechanically. That removes the stack entirely:

```python
def select_iterative(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        p = partition(nums, lo, hi)
        if p == target:
            return nums[p]
        if target < p:
            hi = p - 1
        else:
            lo = p + 1
    return nums[lo]
```

Same algorithm, `O(1)` stack, no `RecursionError` on any input. Offer this version if the interviewer
asks about deep recursion — a function whose only recursive call is the final statement can always be
turned into a loop, and saying so is worth a mark.

### The public function, with the index arithmetic done carefully

```python
def kth_largest(nums: list[int], k: int) -> int:
    """LeetCode 215. The k-th largest value. Mutates nums."""
    if not 1 <= k <= len(nums):
        raise ValueError(f"k must be between 1 and {len(nums)}, got {k}")
    return select_iterative(nums, len(nums) - k)      # k-th largest = index n - k
```

`len(nums) - k`, checked against both ends: `k = 1` gives `n - 1`, the last index, the largest.
`k = n` gives `0`, the smallest. Both correct.

### Handling many duplicates

LeetCode 215 has test cases full of repeated values, specifically to break the two-way partition. Use
the three-way version, which places all copies of the pivot at once:

```python
def select_three_way(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while True:
        if lo == hi:
            return nums[lo]
        pivot = nums[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi
        while i <= gt:                            # Dutch national flag
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]
                lt, i = lt + 1, i + 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1
            else:
                i += 1
        if lt <= target <= gt:                    # target is inside the equal block
            return pivot                          # ... so the pivot is the answer
        if target < lt:
            hi = lt - 1
        else:
            lo = gt + 1
```

The line that matters is `if lt <= target <= gt`. When the target lands anywhere inside the block of
values equal to the pivot, the answer is the pivot — and on an input of a million identical values
that happens on the first pass, so the whole thing is one `O(n)` sweep.

### The complete file

```python
"""Quickselect: the k-th largest in expected O(n), using quicksort's partition."""

import heapq
import random


def partition(nums: list[int], lo: int, hi: int) -> int:
    """Lomuto partition with a random pivot. Returns the pivot's final index."""
    r = random.randint(lo, hi)
    nums[r], nums[hi] = nums[hi], nums[r]
    pivot = nums[hi]
    i = lo
    for j in range(lo, hi):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i


def select(nums: list[int], target: int) -> int:
    """The value that would be at index `target` in the sorted list.

    Expected O(n): n + n/2 + n/4 + ... = 2n, because one side is discarded each time.
    Worst case O(n^2), made vanishingly unlikely by the random pivot.
    Mutates nums, and leaves it partially ordered.
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        p = partition(nums, lo, hi)
        if p == target:
            return nums[p]
        if target < p:
            hi = p - 1
        else:
            lo = p + 1
    return nums[lo]


def select_three_way(nums: list[int], target: int) -> int:
    """Quickselect that stays O(n) when the input is mostly duplicates."""
    lo, hi = 0, len(nums) - 1
    while True:
        if lo == hi:
            return nums[lo]
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
        if lt <= target <= gt:
            return pivot
        if target < lt:
            hi = lt - 1
        else:
            lo = gt + 1


def kth_largest(nums: list[int], k: int) -> int:
    """LeetCode 215. k = 1 is the largest. Mutates nums."""
    if not 1 <= k <= len(nums):
        raise ValueError(f"k must be between 1 and {len(nums)}, got {k}")
    return select_three_way(list(nums), len(nums) - k)


def kth_smallest(nums: list[int], k: int) -> int:
    """k = 1 is the smallest."""
    if not 1 <= k <= len(nums):
        raise ValueError(f"k must be between 1 and {len(nums)}, got {k}")
    return select_three_way(list(nums), k - 1)


def top_k(nums: list[int], k: int) -> list[int]:
    """The k largest values, unordered. O(n) expected -- the partition leaves them
    all in the last k positions, which is often all the caller needs."""
    if k <= 0:
        return []
    values = list(nums)
    select(values, len(values) - k)
    return values[len(values) - k:]


def kth_largest_heap(nums: list[int], k: int) -> int:
    """The other correct answer: O(n log k) time, O(k) space.

    Better when the data is a stream, or when nums must not be mutated.
    """
    smallest_k_largest: list[int] = []
    for x in nums:
        heapq.heappush(smallest_k_largest, x)
        if len(smallest_k_largest) > k:
            heapq.heappop(smallest_k_largest)     # drop the smallest of the k+1
    return smallest_k_largest[0]


def median(nums: list[int]) -> float:
    """Quickselect's natural application: the median in O(n) rather than O(n log n)."""
    values = list(nums)
    n = len(values)
    if n % 2 == 1:
        return float(select_three_way(values, n // 2))
    lower = select_three_way(values, n // 2 - 1)
    upper = select_three_way(list(nums), n // 2)
    return (lower + upper) / 2


if __name__ == "__main__":
    print(kth_largest([3, 2, 1, 5, 6, 4], 2))                  # 5
    print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))         # 4
    print(kth_largest([1], 1))                                 # 1
    print(kth_smallest([3, 2, 1, 5, 6, 4], 1))                 # 1

    print(sorted(top_k([3, 2, 1, 5, 6, 4], 3)))                # [4, 5, 6]
    print(kth_largest_heap([3, 2, 1, 5, 6, 4], 2))             # 5
    print(median([7, 1, 3, 9, 5]))                             # 5.0
    print(median([4, 1, 3, 2]))                                # 2.5

    # the duplicate-heavy case that breaks the two-way version
    heavy = [7] * 200_000 + [9]
    print(kth_largest(heavy, 1))                               # 9    -- one O(n) pass

    # the input is mutated and left partly ordered -- say this out loud
    data = [3, 2, 1, 5, 6, 4]
    print(select(data, 4), data)                               # 5 [3, 2, 1, 4, 5, 6]
```

---

## 6. What it costs

### The expected case, counted

Partitioning a range of `m` elements costs `m − 1` comparisons. With a random pivot, the pivot lands
near the middle on average, so the surviving side is about half the size.

```
 pass 1:  compare  n        elements
 pass 2:  compare  n/2
 pass 3:  compare  n/4
 pass 4:  compare  n/8
   ...
          ----------------------------
 total  =  n(1 + 1/2 + 1/4 + 1/8 + ...) = n x 2 = 2n
```

**`O(n)`.** The exact expected count with a uniformly random pivot is about `3.4n` comparisons for
the median and about `2n` for a value near an end — the constant depends on `k`, but it is a
constant.

```
 n = 1,000,000

 quickselect (median)   ~3,400,000 comparisons
 quickselect (k = 10)   ~2,000,000
 full sort              ~20,000,000
 heap of size 10        ~3,300,000
 heap of size 500,000   ~19,000,000
```

### Why the sum stops at `2n`

This is the piece of arithmetic to have ready, because interviewers ask candidates to justify the
`O(n)` and most of them cannot.

```
 S = 1 + 1/2 + 1/4 + 1/8 + 1/16 + ...

 2S = 2 + 1 + 1/2 + 1/4 + 1/8 + ...
 2S = 2 + S
  S = 2

 So n + n/2 + n/4 + ... = 2n. Halving and summing gives twice the first term.
```

Say it as: *"the sum of a halving series is twice the first term, so the total work is 2n, not
n log n. The log factor in quicksort comes from having to do full work at every level, and I only do
work on one side."*

### The worst case

```
 pivot is always the largest (or smallest) value:

 pass 1: n-1 comparisons, one element removed
 pass 2: n-2
   ...
 total = n(n-1)/2 = O(n^2)

 n = 100,000 : 5,000,000,000 comparisons -- minutes, not milliseconds
```

With a random pivot the probability of this is on the order of `1/n!`, which for a hundred thousand
elements is a number with hundreds of thousands of digits in the denominator. It does not happen. But
it is not *impossible*, and the honest phrase is **"expected `O(n)`"**, not "`O(n)`".

### Space

```
 select_iterative  : O(1) extra -- one loop, no stack, in place
 select (recursive): O(log n) stack expected, O(n) worst case
 heap of size k    : O(k)
 sorted(nums)[-k]  : O(n) for the copy

 quickselect MUTATES the input. If the caller needs the original order,
 copy first -- and then it is O(n) space like everything else.
```

The `O(1)` space of the iterative version is a genuine selling point over the heap, and worth saying.

### Against the alternatives, decided by k

```
                     time            space     mutates?   stream?
 sorted()[-k]        O(n log n)      O(n)      no         no
 heapq.nlargest      O(n log k)      O(k)      no         YES
 quickselect         O(n) expected   O(1)      YES        no

 k = 10 of 10^6      heap 3.3M  vs quickselect 2M    -> similar
 k = 500,000         heap  19M  vs quickselect 3.4M  -> quickselect wins 6x
 data is a stream    heap works, quickselect cannot  -> heap, always
```

---

## 7. The traps

### The real error: the wrong index for "k-th largest"

```python
def kth_largest_broken(nums, k):
    return select(nums, k)              # <-- k, not len(nums) - k

print(kth_largest_broken([3, 2, 1, 5, 6, 4], 2))
```

```
3
```

No exception. `3` is the third *smallest*, and the answer should be `5`. This is the commonest bug on
this problem, and it produces a plausible number rather than a crash. The defence is to write
`target = len(nums) - k` and immediately check the two ends out loud: *"k = 1 should give index n−1,
the largest — yes. k = n should give index 0, the smallest — yes."*

With `k` out of range it does raise, which is a small mercy:

```python
print(kth_largest_broken([1, 2, 3], 3))
```

```
Traceback (most recent call last):
  File "day55.py", line 5, in <module>
    print(kth_largest_broken([1, 2, 3], 3))
          ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "day55.py", line 12, in select
    return nums[lo]
           ~~~~^^^^
IndexError: list index out of range
```

### The near-miss: recursing into both sides

```python
def select_broken(nums, lo, hi, target):
    if lo >= hi:
        return nums[lo]
    p = partition(nums, lo, hi)
    left = select_broken(nums, lo, p - 1, target)      # <-- both branches
    right = select_broken(nums, p + 1, hi, target)
    return nums[target]
```

This still returns the right answer, and it is `O(n log n)` — you have written quicksort with extra
steps. The interviewer will ask for the complexity, and the honest answer is that discarding a side
is the entire optimisation. **If your code has two recursive calls, it is not quickselect.**

### The real error: `O(n²)` on duplicates

```python
import sys
sys.setrecursionlimit(3000)
print(kth_largest_two_way([7] * 200_000 + [9], 1))
```

```
Killed
```

or, with a recursive implementation:

```
RecursionError: maximum recursion depth exceeded
```

With a two-way partition and `<`, a list of identical values partitions into one empty side and one
side of `n − 1`, every single time, whatever the random pivot is — because randomising the *position*
does not help when every *value* is the same. This is the case the three-way partition exists for,
and LeetCode 215 has test cases designed to trigger it.

### The trap: forgetting that it mutates

```python
scores = [88, 95, 71, 64, 99]
print(kth_largest_inplace(scores, 2))
print(scores)
```

```
95
[88, 71, 64, 95, 99]
```

The caller's list has been rearranged. Sometimes that is fine and sometimes it is a bug three
functions away. Either copy inside the function — `select(list(nums), target)` — or say clearly in
the docstring that the argument is mutated. The same discipline as `.sort()` against `sorted()` from
[day 051](../day-051-why-sorting-matters/README.md).

### The trap: claiming a guaranteed `O(n)`

```
Candidate: "Quickselect is O(n)."
Interviewer: "Always?"
```

No. It is `O(n)` **expected**, `O(n²)` worst case. Median of medians gives a deterministic `O(n)`, but
with a constant factor large enough that it is slower than the randomised version on real data, so it
is a theoretical answer rather than an engineering one. Volunteer the distinction before you are
pushed on it; a candidate who says "expected O(n), worst case quadratic, and here is why I am
comfortable with that" is ahead of one who has to be corrected.

### The trap: using quickselect on a stream

Quickselect needs the whole list present and it needs random access, because it rearranges elements.
If the data arrives one value at a time and will not fit in memory, quickselect is not available at
all, and the answer is a heap of size `k` — `O(n log k)` time, `O(k)` space, one pass, and it never
holds more than `k + 1` items. That is an important boundary to know, because "what if the data is a
stream" is the standard third follow-up.

---

## 8. In the interview

### How it gets asked

- *"Find the k-th largest element in an array."* — LeetCode 215, asked constantly.
- *"Can you do better than sorting?"* — the prompt that means "I want quickselect or a heap".
- *"Find the top k elements."* — same machinery; quickselect leaves them in the last `k` slots.
- *"Find the median of an unsorted array in O(n)."* — quickselect with `target = n // 2`.
- *"What if the array is a stream of a billion numbers?"* — the heap, and knowing why quickselect
  cannot be used.
- *"What is the worst case? Can you make it O(n) guaranteed?"* — median of medians, named and then
  set aside.

### What to say out loud, in the first ninety seconds

1. **Give the baseline first.** *"The simple answer is `sorted(nums)[-k]`, which is O(n log n). I can
   do better, and I'll say why sorting is more than I need: I'm being asked for one value, not an
   ordering."*
2. **Name the two better answers and their costs.** *"A heap of size k is O(n log k). Quickselect is
   O(n) expected. I'll write quickselect and mention where the heap would win."*
3. **Do the index arithmetic out loud.** *"The k-th largest sits at index n − k in the sorted array.
   Check: k = 1 gives n − 1, the largest — correct. k = n gives 0, the smallest — correct."*
4. **State the one difference from quicksort.** *"Same partition, but after it I know which side the
   target is on, so I recurse into one side and discard the other. That's what removes the log
   factor."*
5. **Give the cost with the arithmetic.** *"n + n/2 + n/4 + … = 2n, because a halving series sums to
   twice the first term. That's O(n) expected. Worst case is O(n²) if the pivot is always extreme, so
   I randomise the pivot."*

### The follow-ups

**"Why is it O(n) and not O(n log n)? Both halve."**
Because of what happens to the work at each level, not to the size. In quicksort, after partitioning
I recurse into *both* halves, so every level of the recursion still processes all n elements in total
— n at the top, two lots of n/2 below it, four lots of n/4 below that — and with log n levels that
multiplies out to n log n. In quickselect I know which side the target is on, because the pivot lands
at its final sorted position and I can compare that position with my target index. So I discard the
other side entirely and never look at it again. The work per level is therefore n, then n/2, then
n/4, and the total is the sum of that halving series, which is 2n — a halving series sums to twice
its first term. So the log factor is not something I optimised away cleverly; it never appears,
because there is only ever one live branch. That is also why the code has exactly one recursive call
per path, and a good check on an implementation: if there are two recursive calls in it, it is
quicksort wearing the wrong name.

**"What's the worst case, and can you make it O(n) guaranteed?"**
The worst case is O(n²), and it happens when the pivot is the largest or smallest value in the range
every time — each partition then removes exactly one element, so the sizes go n, n−1, n−2 and the sum
is n(n−1)/2. With a fixed pivot rule such as "always the last element", the input that triggers it is
an already sorted array, which is a very likely input. I randomise the pivot position, which means
the running time depends on my random numbers rather than on the arrangement of the input, so no
particular input is bad and the probability of the quadratic case is on the order of 1/n!. There is a
separate bad case that randomisation does *not* fix: an array where all the values are equal, because
randomising the position does not help when every value is the same. For that I use a three-way
partition, and check whether the target index falls inside the block of values equal to the pivot —
if it does, the pivot is the answer, so a million identical values is a single linear pass. As for a
deterministic guarantee, yes, there is one: median of medians, which splits the array into groups of
five, takes each group's median, and recursively selects the median of those as the pivot. That pivot
is provably near the middle, so the worst case is O(n). In practice it is slower than the randomised
version on real data because of the constant factor, so I would name it and then say I would still
ship the randomised one.

**"The data is a stream of a billion numbers that won't fit in memory. Now what?"**
Then quickselect is off the table, because it needs the entire array present and it works by
rearranging elements in place — it needs random access, and a stream gives neither. The answer is a
min-heap of size k. I read values one at a time, push each one, and pop whenever the heap exceeds k
elements, which always removes the smallest of the k+1 — so what remains is always the k largest
values seen so far, and at the end the root of the heap is the k-th largest. That is O(n log k) time,
O(k) space, one pass, and it never holds more than k+1 items regardless of how long the stream is.
For k = 10 out of a billion that is trivial memory and about 3.3 billion comparisons' worth of work
at log k = 3.3. If k were also enormous — say I wanted the millionth largest of a billion — the heap
stops being cheap and I would go to a different shape: either an approximate answer using a sketch
like t-digest, if the requirement allows it, which gives quantiles in constant memory, or an external
approach where I make one pass to build a histogram of value ranges, find which bucket the answer
falls in, and then make a second pass keeping only that bucket, which fits in memory. And if the data
is finite but merely bigger than RAM rather than a true stream, the honest answer is an external merge
sort, which is exactly what a database does for a large ORDER BY.

### A model answer

> "The straightforward answer is `sorted(nums)[-k]`, which is O(n log n), and I'd say that first. But
> sorting produces a full ordering and I've only been asked for one value, so it's more work than the
> question needs. There are two better answers: a heap of size k, which is O(n log k), and
> quickselect, which is O(n) expected. I'll write quickselect.
>
> It uses quicksort's partition. I pick a random pivot and rearrange so smaller values are left of it
> and larger ones right of it, which leaves the pivot at its final sorted position, at some index p.
> The k-th largest lives at index n − k in the sorted array — checking that: k = 1 gives n − 1, the
> largest, and k = n gives 0, the smallest, so it's right. Now if p equals my target index, the pivot
> is the answer. If the target is smaller, the answer is entirely to the left, so I discard everything
> from p rightwards. If it's larger, I discard everything left.
>
> ```python
> def select(nums: list[int], target: int) -> int:
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         p = partition(nums, lo, hi)
>         if p == target:
>             return nums[p]
>         if target < p:
>             hi = p - 1
>         else:
>             lo = p + 1
>     return nums[lo]
> ```
>
> I've written it iteratively because there's only one recursive call and it's the last statement, so
> it converts to a loop mechanically — that gives O(1) extra space and no recursion depth to worry
> about.
>
> The complexity is the interesting part. Quicksort recurses into both sides, so it does n work at
> every level for log n levels. Here I discard one side, so the work goes n, then n/2, then n/4, and
> that halving series sums to 2n — a halving series is twice its first term. So it's O(n), and the log
> factor never appears rather than being optimised away.
>
> Two honest caveats. It's O(n) *expected*, not guaranteed — if the pivot were extreme every time it
> would be O(n²), which is why the pivot is random. And on an array where every value is equal,
> randomising the position doesn't help, so I'd use a three-way partition and check whether the target
> falls inside the equal block, which makes that case a single linear pass. Also, this mutates the
> input and leaves it half-ordered, so I'd copy first if the caller needs the original. If the data
> were a stream I couldn't use this at all, and the answer would be the heap."

---

## 9. Recall card

- **Same partition as quicksort, one change: recurse into ONE side.** The pivot lands at its final
  index `p`; compare `p` with the target index. `p == target` → answer · `target < p` → search left,
  **discard the right** · else search right. Two recursive calls means you wrote quicksort.
- **The k-th largest is at index `n - k`.** Check both ends out loud: `k=1 → n-1` (largest),
  `k=n → 0` (smallest). Getting this wrong returns a plausible number with no error — the commonest
  bug on LeetCode 215.
- **Expected O(n), and the arithmetic is the answer:** `n + n/2 + n/4 + … = 2n`, because a halving
  series sums to **twice the first term**. Quicksort is n log n because it does full work at *every*
  level; here only one branch survives.
- **Worst case O(n²)** if the pivot is always extreme — fix with a **random pivot**. Randomising the
  *position* does not help when every *value* is equal, so use a **three-way partition** and return
  the pivot when `lt <= target <= gt`: a million identical values in one pass.
- **Three answers, chosen by k and by shape:** `sorted()[-k]` O(n log n) · heap O(n log k), O(k)
  space, **the only one that works on a stream** · quickselect O(n) expected, **O(1) space but it
  mutates**. At k = 10 of 10⁶ heap and quickselect are level; at k = n/2 quickselect wins six times
  over.
