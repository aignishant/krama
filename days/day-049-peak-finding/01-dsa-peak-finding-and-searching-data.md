---
day: 49
track: dsa
title: "Peak finding, and searching data that is structured but not sorted"
phase: "Binary search"
status: written
---

# Day 049 · DSA — Peak finding, and searching data that is structured but not sorted

**After today you can:** You can binary search using local structure alone, with no global ordering.

**The interviewer asks it as:** *Find a peak element in O(log n).*

---

## 1. What this is, and why they ask it

A **peak** is an element bigger than both its neighbours. Given an array with no order to it at all —
values going up and down at random — you can find one in `O(log n)`. Not the largest element: *a*
peak, any peak. The array is not sorted, nothing about it is monotone, and binary search still works,
because the only thing binary search has ever needed is a rule that lets you throw half away with a
guarantee.

They ask it because it breaks the mental model most candidates have built. Ask "can I binary search
this?" and the reflex answer is "only if it's sorted", which is wrong and has been wrong since
[day 045](../day-045-rotated-array-search/README.md)'s rotated array. LeetCode 162 is the cleanest
demonstration: the input is deliberately unsorted, the answer is deliberately not unique, and the
`O(log n)` requirement is deliberately stated so you cannot scan. Candidates who have understood the
invariant get it in three minutes; candidates who memorised a template stare at it. It is also the
day the phase's real lesson lands — **binary search is about discarding halves with proof, not about
sortedness.**

---

## 2. The story

Kunjappan has four acres of areca on the slope above his house in Wayanad, and in December he goes up
before six, when it is still dark and the mist has come down.

The mist there is not like rain. It is a solid white thing that sits on the hill until about half past
eight, and on a bad morning he can see perhaps two arm-lengths ahead of him. He has walked that hill
for thirty years and he still cannot see it in December.

There is a bund running along the top edge of the plot, a raised earth path about half a kilometre
long that the water follows. It is not level. Whoever cut it followed the ground, so it climbs and
drops the whole way along — small rises, small dips, one big hump near the middle where a rock is.

What he wants, at half past five in the morning, is a signal on his phone to call his brother in
Kannur. He does not need the highest point on the bund. He needs *any* high point, because from the
top of any rise on that hill the signal comes and in the dips it does not.

So he does this.

He walks out to about the middle of the bund and puts his foot forward, feeling with his toe. The
ground ahead of him rises. That one small fact tells him something much bigger than it looks, and it
is the thing he has never had to explain to himself: if the ground goes up from here, then somewhere
ahead there is a top. It has to be. The bund cannot go on climbing forever — it ends at the fence.
So it must climb for a while and then stop climbing, and where it stops climbing is a rise, and that
is all he wants.

Which means the whole half of the bund behind him is finished with. He does not need to walk it, feel
it, or think about it again. He has not seen any of it and he does not care.

He goes forward, roughly to the middle of what is left, and feels again. This time the ground drops
ahead of him. Same argument in the other direction: if it falls from here going forward, then behind
him — between where he stopped last time and here — the ground must have come up and turned over
somewhere. There is a top back there. So the stretch in front is finished with instead.

Six or seven of these, each one throwing away half the bund he has not walked, and he is standing on
a rise with two bars on the phone.

He has walked maybe eighty steps on a bund of six hundred, and he still could not draw the shape of
it if you asked him.

---

## 3. The idea in plain English

Kunjappan's bund is the array. The slope under his toe is a comparison between two neighbours. And
the sentence he has never had to explain — *it cannot keep climbing forever* — is the entire proof
that the method works.

### What a peak is

```python
nums = [1, 2, 1, 3, 5, 6, 4]
```

An element is a **peak** if it is strictly greater than the element on each side. Here index 1 (value
2) is a peak, because 2 > 1 and 2 > 1. Index 5 (value 6) is also a peak, because 6 > 5 and 6 > 4.
**There are two, and either is an acceptable answer.** That is unusual and it is part of the problem's
design: an answer that is not unique is a signal that you are not being asked to search for a specific
thing.

The ends need a convention. LeetCode 162 states it: treat `nums[-1]` and `nums[n]` as
**negative infinity** — imaginary values smaller than anything real, just off each end. With that
convention:

- The first element is a peak if it is bigger than the second. Nothing to its left can beat it.
- The last element is a peak if it is bigger than the second-last.
- **Every array has at least one peak.** A finite list of values has a maximum, and the maximum beats
  both its neighbours, so it is a peak. So there is no "not found" case, ever.

The problem also guarantees `nums[i] != nums[i + 1]` for all `i` — no two adjacent values are equal.
That matters, and §7 shows what happens without it.

### The rule that discards half

Stand at `mid` and compare it with its right-hand neighbour only:

```python
if nums[mid] < nums[mid + 1]:
    # the ground rises to the right -> a peak exists in [mid + 1, hi]
    lo = mid + 1
else:
    # the ground falls to the right -> a peak exists in [lo, mid]
    hi = mid
```

Two branches, one comparison, and each one is Kunjappan's argument.

**If `nums[mid] < nums[mid + 1]`** — it climbs to the right. Now walk right in your head. Either the
values keep climbing all the way to the end, in which case the last element is bigger than its left
neighbour and bigger than the imaginary negative infinity on its right, so it is a peak; or somewhere
they stop climbing, and the element where they turn over is bigger than both its neighbours, so *it*
is a peak. **Either way there is a peak strictly to the right of `mid`.** So everything from `lo` to
`mid` can go.

**If `nums[mid] > nums[mid + 1]`** — it falls to the right. Mirror the argument leftwards from `mid`:
either the values keep climbing all the way back to `lo` and beyond, in which case `nums[lo]` beats
the negative infinity on its left and is a peak, or they turn over somewhere in between. **Either way
there is a peak in `[lo, mid]`, and `mid` itself may be it** — which is why `hi = mid` and not
`hi = mid - 1`.

### The invariant

Say this out loud in the interview, because it is what the question is testing:

> **The range `[lo, hi]` always contains at least one peak.**

It is true at the start, because the whole array contains one. Each branch preserves it, by the
argument above. When `lo == hi` the range holds exactly one element, and that element must be the
peak.

Notice how this differs from every previous day. There is no target. There is no monotone question.
There is only a claim about the range that stays true — and that is enough.

### Why this is [day 043](../day-043-binary-search-without-bugs/README.md)'s template

It is the half-open shape you already know:

```python
lo, hi = 0, len(nums) - 1
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] < nums[mid + 1]:
        lo = mid + 1
    else:
        hi = mid
return lo
```

`while lo < hi` with `hi = mid` — the pairing from day 043, and the reason it terminates is the same
inequality: `mid < hi` always, because `lo < hi`. And `mid + 1` is always a valid index, for the same
reason: `mid < hi <= len(nums) - 1`, so `mid + 1 <= len(nums) - 1`.

### Not the maximum — and why that is the point

The function returns *a* peak, not *the* maximum. On `[1, 2, 1, 3, 5, 6, 4]` it may return index 5,
and on `[1, 2, 1, 3, 5, 6, 4]` it may return index 1, depending on where the halving lands.

Finding the *maximum* of an unsorted array is `O(n)` and cannot be beaten — you must look at every
element, because any one you skip could be the largest. Finding *a peak* is `O(log n)`. That gap is
the whole lesson: **weakening what you ask for from "the best" to "a local best" changes the
complexity class.** Say that sentence; interviewers like it because it is the actual insight.

### The family this opens

Once you see that "local structure plus a discard proof" is enough, several problems join up:

- **LeetCode 852, peak in a mountain array.** Guaranteed to rise then fall, so there is exactly one
  peak. Identical code, and the guarantee only makes the answer unique.
- **LeetCode 153, minimum in a rotated array**, from
  [day 045](../day-045-rotated-array-search/README.md). That is a *valley* — the same argument
  upside-down.
- **LeetCode 1901, a peak in a 2D grid.** Binary search the columns; in each candidate column take
  the row-maximum, and compare it left and right. `O(rows × log cols)`.
- **Ternary search**, for a genuinely unimodal function, which finds the *actual* maximum rather than
  a local one — worth naming as the neighbouring tool.

---

## 4. The picture

The bund, and the two arguments:

```
 index      0    1    2    3    4    5    6    7    8
 value      1    3    2    4    7    9    5    6    2
                 ^                   ^         ^
              peak(3>1,3>2)     peak(9>7,9>5)  peak(6>5,6>2)

 three peaks. ANY of them is a correct answer.
 the ends: imagine -inf just off each side.
       -inf | 1  3  2  4  7  9  5  6  2 | -inf
```

**What to notice:** there is no order here at all. The values go up, down, up, up, down, up, down.
Nothing is sorted and nothing is monotone.

One step of the search, both branches:

```
 lo=0                    mid=4                     hi=8
  [ 1    3    2    4  |  7  | 9    5    6    2 ]
                          nums[4]=7 < nums[5]=9   -> it RISES to the right

  going right from 7:  9, then 5 -- so it turned over at 9.
  (and if it had never turned over, the last element would beat -inf and be a peak)
  => a peak EXISTS in [5, 8].  Discard [0, 4] without looking at it.

  lo = 5
                              [ 9    5    6    2 ]
                                  mid=6, nums[6]=5 < nums[7]=6  -> rises right
  lo = 7
                                        [ 6    2 ]
                                  mid=7, nums[7]=6 > nums[8]=2  -> falls right
  hi = 7      lo == hi == 7. Return 7. nums[7] = 6, and 6 > 5 and 6 > 2. A peak.
```

**What to notice:** the search never looked at indices 0 to 3 and never needed to. The discard was
justified by an argument about what *must* exist, not by any value it read.

Why "rises to the right" guarantees a peak to the right:

```
 case A: it never stops rising                case B: it stops rising somewhere
   mid                          end             mid              j
    |                            |               |               |
    7 -> 9 -> 11 -> 14 -> 20 -> 31 | -inf        7 -> 9 -> 14 -> 20 -> 6
                                ^                                ^
                    the last element beats -inf        20 > 14 and 20 > 6
                    -> it is a peak                    -> it is a peak

 there is no third case. The array is finite, so it cannot rise forever.
```

**What to notice:** the whole method rests on "the array is finite". That is Kunjappan's *the bund
ends at the fence*, and it is the sentence to say when an interviewer asks you to justify the discard.

---

## 5. The code, built step by step

### The bounds and the loop shape

```python
lo, hi = 0, len(nums) - 1
while lo < hi:
    ...
return lo
```

Closed range at both ends this time — `hi` is the last valid index — but the loop condition is
strictly `<`, because the branch that keeps `mid` writes `hi = mid`. That is the day 043 pairing:
whenever a branch keeps the middle, the loop condition must be strict.

There is no `return -1`. Every array has a peak, so the loop always ends on one.

### The single comparison

```python
    mid = (lo + hi) // 2
    if nums[mid] < nums[mid + 1]:
        lo = mid + 1
    else:
        hi = mid
```

Compare with the **right** neighbour only. Comparing with both neighbours is the trap in §7 — it is
unnecessary, and it introduces an index that can go out of range.

`mid + 1` is always safe here. `mid` is the floor of `(lo + hi) / 2` and `lo < hi`, so `mid < hi`, so
`mid + 1 <= hi <= len(nums) - 1`.

### The complete solution

```python
def find_peak_element(nums: list[int]) -> int:
    """LeetCode 162. Index of ANY peak: an element strictly greater than both neighbours.

    Treats nums[-1] and nums[n] as negative infinity, so the first and last elements
    can be peaks. Every array has at least one peak, so there is no not-found case.

    Invariant: the range [lo, hi] always contains at least one peak.
    """
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2               # mid < hi, so mid + 1 is always valid
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1                   # it rises right: a peak must exist to the right
        else:
            hi = mid                       # it falls right: a peak exists at mid or left of it

    return lo                              # lo == hi, and that element is a peak


def peak_index_in_mountain(arr: list[int]) -> int:
    """LeetCode 852. Guaranteed to rise then fall, so the peak is unique.

    Identical code. The guarantee changes the answer's uniqueness, not the method.
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def find_valley(nums: list[int]) -> int:
    """The mirror: an element smaller than both neighbours. One comparison flipped."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[mid + 1]:      # it FALLS right -> a valley exists to the right
            lo = mid + 1
        else:
            hi = mid
    return lo


def is_peak(nums: list[int], i: int) -> bool:
    """Check the answer, using the -inf convention at both ends."""
    left = nums[i - 1] if i > 0 else float("-inf")
    right = nums[i + 1] if i < len(nums) - 1 else float("-inf")
    return nums[i] > left and nums[i] > right


if __name__ == "__main__":
    for nums in (
        [1, 3, 2, 4, 7, 9, 5, 6, 2],
        [1, 2, 1, 3, 5, 6, 4],
        [1, 2, 3, 4, 5],            # strictly rising: the last element is the peak
        [5, 4, 3, 2, 1],            # strictly falling: the first element is the peak
        [7],                        # single element: it beats -inf on both sides
        [2, 1],                     # two elements
        [1, 2],                     # two elements, the other way
    ):
        i = find_peak_element(nums)
        print(nums, "-> index", i, "value", nums[i], "| is a peak:", is_peak(nums, i))

    print(peak_index_in_mountain([0, 2, 5, 3, 1]))     # 2
    print(find_valley([9, 7, 4, 6, 8]))                # 2
```

Run it. The five inputs that decide correctness are the strictly rising array, the strictly falling
array, the single element, and both two-element arrays. Those cover every place the negative-infinity
convention does real work, and a solution that handles all five almost certainly handles everything.

### The 2D version, named

```python
def find_peak_grid(mat: list[list[int]]) -> list[int]:
    """LeetCode 1901. A peak in a grid: greater than its four neighbours.

    Binary search the COLUMNS. In each candidate column, take the row with the largest
    value -- that element already beats its up and down neighbours -- then compare it
    left and right, exactly as in 1D.  O(rows x log cols).
    """
    lo, hi = 0, len(mat[0]) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        best_row = max(range(len(mat)), key=lambda r: mat[r][mid])
        if mat[best_row][mid] < mat[best_row][mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    best_row = max(range(len(mat)), key=lambda r: mat[r][lo])
    return [best_row, lo]
```

The trick worth understanding: taking the column's maximum settles the vertical direction for free,
so the two-dimensional problem collapses to the one-dimensional argument. Mention it if asked; do not
volunteer it unless there is time.

---

## 6. What it costs

### Time

```
each pass: one midpoint, one comparison, one assignment    -> O(1)
each pass discards at least half the range                 -> log2(n) passes
                                                           -> O(log n)
```

```
n = 1,000           10 comparisons
n = 1,000,000       20 comparisons
n = 1,000,000,000   30 comparisons
```

### Against the honest alternative

```
find A PEAK          : O(log n)     -- 20 comparisons at a million
find THE MAXIMUM     : O(n)         -- 1,000,000 comparisons at a million

and the maximum cannot be done faster: any element you do not look at could be
the largest, so an adversary can always place the maximum where you did not look.
```

**Fifty thousand times fewer comparisons, bought by asking for something weaker.** That trade — a
local best instead of a global best — is the sentence to have ready, and it is the reason the problem
exists.

### Space

```
lo, hi, mid: three integers    -> O(1) extra space
```

### The 2D version

```
find_peak_grid: log2(cols) passes, each scanning one column of `rows` values
                -> O(rows x log cols)

a 1,000 x 1,000 grid:
    scan everything : 1,000,000 reads
    this            : 1,000 x 10 = 10,000 reads      -- 100x fewer
```

---

## 7. The traps

### The near-miss: comparing with the left neighbour

The mirror of the correct rule looks equally reasonable and is not:

```python
def broken_left(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid - 1]:      # <-- LEFT neighbour
            hi = mid - 1
        else:
            lo = mid
    return lo

print(broken_left([1, 2]))
```

```
0
```

Index 0 holds 1, and `nums[1]` is 2, so 1 is not a peak. The cause is that at `mid = 0`,
`nums[mid - 1]` is `nums[-1]` — Python's *last* element — so the comparison is against a value from
the wrong end of the array, silently. Sixth appearance of an index reaching −1, and the fifth time it
has produced a wrong answer rather than a crash.

On other inputs the same function hangs, because `lo = mid` with a floor midpoint makes no progress
when `hi == lo + 1`. **Compare with the right neighbour only** — `mid + 1` is always valid because
`lo < hi` forces `mid < hi`, and there is no `mid - 1` to go wrong.

### The real error: `while lo <= hi` with `hi = mid`

```python
def broken(nums):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:                     # <-- non-strict, with hi = mid
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo

print(broken([1, 2, 3]))
```

```
Traceback (most recent call last):
  File "day49.py", line 11, in <module>
    print(broken([1, 2, 3]))
          ^^^^^^^^^^^^^^^^^
  File "day49.py", line 5, in broken
    if nums[mid] < nums[mid + 1]:
                   ~~~~^^^^^^^^^
IndexError: list index out of range
```

The non-strict condition lets `lo` and `hi` both reach the last index, so `mid` becomes the last index
and `mid + 1` is off the end. On other inputs the same bug hangs instead, because `hi = mid` when
`lo == hi == mid` changes nothing. [Day 043](../day-043-binary-search-without-bugs/README.md)'s pairing
rule, and it costs you both failure modes at once: **a branch that keeps the middle requires a strict
loop condition.**

### The near-miss: `hi = mid - 1`

```python
def broken_minus_one(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid - 1                 # <-- throws away mid, which may BE the peak
    return lo

print(broken_minus_one([1, 2, 1, 3, 5, 6, 4]))
```

```
4
```

Index 4 holds 5, and its right neighbour is 6, so it is not a peak. When the values fall to the right
of `mid`, `mid` itself is a candidate — the turning point may be exactly there — and `- 1` discards
it. Note that this version happens to be right on `[5, 4, 3, 2, 1]` and on `[1, 2, 3, 4, 5]`, which is
what lets it survive a casual test.

### The needless check: comparing both sides for an early return

```python
        if nums[mid - 1] < nums[mid] > nums[mid + 1]:
            return mid                    # "found one early"
```

This one is not wrong — it returns early on a genuine peak and otherwise falls through — but it earns
nothing. The one-sided rule already drives the range onto a peak in the same number of passes, and the
extra line reintroduces `nums[mid - 1]`, with the `-1` wrap waiting at `mid = 0`. **A correct branch
you do not need is still a branch you can get wrong**, and in a whiteboard answer it is two more lines
to defend.

### The trap: equal adjacent values

LeetCode 162 guarantees `nums[i] != nums[i + 1]`. Remove that guarantee and the method breaks:

```python
nums = [1, 2, 2, 2, 1]
```

At `mid = 2`, `nums[2]` is not less than `nums[3]` — they are equal — so the code goes left, and it
would go left just as happily from `mid = 1`. The plateau carries no information about which side the
peak is on, exactly as
[day 045](../day-045-rotated-array-search/README.md)'s duplicates did. There is no `O(log n)` answer
on a flat plateau: an adversary can hide the rise at either end of it, so the worst case is `O(n)`.
**Read the constraint, and if it is missing, ask.**

### The trap: reading "peak" as "maximum"

```python
print(find_peak_element([1, 3, 2, 4, 7, 9, 5, 6, 2]))     # may return 7, not 5
```

Index 7 (value 6) is a peak. Index 5 (value 9) is the maximum. Both are correct answers to the
question that was asked, and a solution that insists on returning 5 cannot be `O(log n)`. If you
believe the problem wants the maximum, you have misread it — and if the interviewer really does want
the maximum, the honest answer is that it is `O(n)` and cannot be beaten.

---

## 8. In the interview

### How it gets asked

- *"Find a peak element — one that's greater than its neighbours. The array isn't sorted. Do it in
  O(log n)."* — LeetCode 162, and the "isn't sorted" is said deliberately to see your reaction.
- *"This array increases then decreases. Find the turning point."* — LeetCode 852, the friendlier
  version, often asked first.
- *"Why does binary search work here? There's no order."* — the real question, and the answer is the
  discard proof.
- *"Now find a peak in a 2D grid."* — LeetCode 1901, the hard follow-up, and naming the
  column-maximum trick is enough even without writing it.

### What to say out loud, in the first ninety seconds

1. **Deal with the sortedness objection before they raise it.** *"The array isn't sorted, and it
   doesn't need to be. Binary search needs a rule that lets me discard half with a guarantee — sorted
   is just the usual way to get one."*
2. **Confirm the conventions.** *"Are the ends treated as negative infinity, so the first and last
   elements can be peaks? And are adjacent values guaranteed distinct? That second one matters — a
   plateau makes it O(n)."*
3. **State that an answer always exists.** *"Every array has at least one peak, because the maximum
   beats both its neighbours. So there's no not-found case."*
4. **Give the rule and the proof in one breath.** *"I compare the middle with its right neighbour
   only. If it rises to the right, then going right either it climbs to the end — in which case the
   last element beats the negative infinity beyond it and is a peak — or it turns over somewhere, and
   the turning point is a peak. Either way a peak exists to the right, so I discard everything up to
   and including the middle."*
5. **State the invariant.** *"The invariant is that `[lo, hi]` always contains at least one peak. When
   they meet, that element is one."*
6. **Give the cost and the contrast.** *"O(log n) time, O(1) space. Worth saying: finding the
   *maximum* is O(n) and can't be beaten — asking for a local best instead of a global best is what
   buys the logarithm."*

### The follow-ups

**"Prove that going uphill always finds a peak."**
The proof is one sentence plus a case split, and it turns entirely on the array being finite. Suppose
`nums[mid] < nums[mid+1]` — it rises to the right. Now walk rightwards from `mid+1`. There are exactly
two possibilities. Either the values keep increasing all the way to the last index, in which case the
last element is greater than its left neighbour and greater than the imaginary negative infinity just
past the end, so the last element is a peak. Or at some index j the sequence stops increasing, meaning
`nums[j-1] < nums[j]` and `nums[j] > nums[j+1]`, which makes j a peak by definition. There is no third
case, because a finite list cannot increase forever. So a peak exists strictly to the right of `mid`,
and discarding `[lo, mid]` cannot lose the only answer. The mirrored argument covers the falling
branch, except there `mid` itself might be the turning point, which is exactly why that branch writes
`hi = mid` rather than `hi = mid - 1`.

**"What if adjacent elements can be equal?"**
Then the method breaks, and I would say so rather than patch it. On `[1, 2, 2, 2, 1]` at a midpoint
inside the plateau, the comparison between the middle and its right neighbour is an equality, which
tells me nothing about which side holds a peak — and I can construct two arrays that look identical at
every position I have examined but have their peaks on opposite sides. That is the same structure as
duplicates in a rotated array from [day 045](../day-045-rotated-array-search/README.md): when a
comparison carries no information, no half can be discarded safely. The consequence is that the worst
case becomes O(n) — an adversary places the plateau across most of the array — and that is a property
of the problem rather than a weakness in my code. In practice I would ask about it in the clarifying
questions rather than discover it, because LeetCode 162 states the distinctness guarantee explicitly
and its presence is a hint that the setter knew it mattered.

**"Now do it on a 2D grid — an element greater than its four neighbours."**
The same argument survives, with one idea added, and the cost becomes O(rows × log cols). I binary
search over the *columns* rather than the elements. For a candidate column, I scan it and find the row
holding its largest value. That element already beats its up and down neighbours, because it is the
maximum of its column — so the vertical direction is settled for free, and I am back to a
one-dimensional problem about the horizontal direction. Then I compare it with the element to its
right: if the right one is bigger, a peak exists in the columns to the right, by exactly the argument
from the 1D case applied along that row; otherwise a peak exists at this column or to its left. The
column scan is O(rows) and I do log(cols) of them. On a 1,000 by 1,000 grid that is about ten thousand
reads against a million for scanning everything. The step people get wrong is scanning the row instead
of the column while searching over columns — that does not settle the perpendicular direction, and the
discard is no longer justified.

### A model answer

> "First thing worth saying: the array isn't sorted and it doesn't need to be. Binary search has never
> actually required sortedness — it requires a rule that lets me throw away half with a guarantee, and
> sorted is just the most common way to get one. Here the guarantee comes from local structure.
>
> Two clarifications. Are the ends treated as negative infinity, so the first and last elements can be
> peaks? And are adjacent values guaranteed distinct? That second one matters a lot — a plateau of
> equal values carries no information about which side a peak is on, and would push this to O(n).
>
> Given both, the key observation is that a peak always exists: the maximum of any finite array beats
> both its neighbours. So there's no not-found case.
>
> The rule is one comparison, with the right-hand neighbour only. If `nums[mid] < nums[mid+1]` — it
> rises to the right — then walking right, either the values climb all the way to the end, in which
> case the last element beats the negative infinity past it and is a peak, or they turn over
> somewhere, and the turning point is a peak. There's no third case, because the array is finite. So a
> peak definitely exists to the right, and I can discard everything up to and including the middle
> without looking at it. If it falls to the right, the mirrored argument puts a peak at `mid` or to
> its left — and `mid` itself might be it, which is why that branch keeps it.
>
> ```python
> def find_peak_element(nums: list[int]) -> int:
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if nums[mid] < nums[mid + 1]:
>             lo = mid + 1        # rises right: a peak must exist to the right
>         else:
>             hi = mid            # falls right: mid itself may be the peak
>     return lo
> ```
>
> The invariant is that `[lo, hi]` always contains at least one peak. It's true at the start, both
> branches preserve it, and when `lo` equals `hi` that single element must be one.
>
> Two details on the loop. `mid + 1` is always in range, because `lo < hi` forces `mid < hi`. And the
> condition is strictly less-than, because the else branch keeps `mid` — a branch that keeps the middle
> and a non-strict condition together give an infinite loop.
>
> O(log n) time, O(1) space. The sentence I'd close on: finding the *maximum* of an unsorted array is
> O(n) and cannot be beaten, because any element you skip could be the largest. Finding a *peak* is
> O(log n). Weakening the question from 'the global best' to 'a local best' is what buys the
> logarithm."

---

## 9. Recall card

- **Binary search needs a discard proof, not sortedness.** A peak is any element beating both
  neighbours; ends count as −∞, so **every array has one** and there is no not-found case.
- **One comparison, right neighbour only:** rises right → `lo = mid + 1`; otherwise → `hi = mid`
  (keep `mid`, it may be the peak). Never compare both sides — `nums[mid-1]` at `mid = 0` reads the
  *last* element silently.
- **The proof is one sentence: the array is finite.** Going uphill either reaches the end (which beats
  −∞) or turns over (which is a peak). Invariant: `[lo, hi]` always contains a peak.
- **`while lo < hi` with `hi = mid`** — day 043's pairing. Non-strict `<=` here hangs; `hi = mid - 1`
  throws away the answer.
- **A peak is not the maximum.** The maximum is O(n) and unbeatable; a *local* best is O(log n) — the
  weakening is what buys the logarithm. Equal adjacent values kill it (O(n)); 2D is
  `O(rows × log cols)` by searching columns and taking each column's max row.
