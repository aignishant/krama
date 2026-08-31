---
day: 52
track: dsa
title: "Bubble, selection and insertion sort, and what each one teaches"
phase: "Sorting"
status: written
---

# Day 052 · DSA — Bubble, selection and insertion sort, and what each one teaches

**After today you can:** You can write all three and say the one case where insertion sort genuinely wins.

**The interviewer asks it as:** *Write insertion sort. When would you actually use it?*

---

## 1. What this is, and why they ask it

Bubble sort, selection sort and insertion sort are the three simple sorting methods. All three take
`O(n²)` time, all three fit in about eight lines, and all three sort in place — they rearrange the
list you were given rather than building a new one. They are the sorts you can write from memory
under pressure, and one of them is genuinely the fastest thing available in a real situation you will
meet.

They ask about them for three reasons, and only one of them is "can you code". The first is that
insertion sort is a real answer: it is what every serious sorting library, Python's included, drops
into for small pieces of data, and knowing *why* is a proper answer to a proper question. The second
is that these three differ in exactly the ways interviewers like to probe — number of comparisons
against number of moves, best case against worst case, stable against unstable — so one small
function opens four follow-ups. The third is that insertion sort is the first place you meet the idea
of a **sorted region that grows**, which comes back on
[day 053](../day-053-merge-sort/README.md) as merging and on
[day 114](../day-114-heapify/README.md) as heapify. Write the three, and the rest of the phase has
something to stand on.

---

## 2. The story

Meera has taught at a school in Trichy for nine years, and every December the annual day happens, and
class six has to walk on stage in height order. Fifty children. It falls to whoever is free.

Her first year she did it the obvious way. She stood the children in a line as they came out, then
walked from one end to the other looking at two children at a time. If the taller one was standing in
front of the shorter one, she made the two of them change places, and then she looked at the next
two. One walk down the line did not fix it, so she walked it again. And again. She kept walking until
she got all the way down without having to move anybody, and then she knew it was right. It took her
most of a lunch break, and she remembers being surprised how many times she had to send the same
child backwards.

The next year Fathima did it, and Fathima did not walk up and down at all. She looked at the whole
group, found the shortest child anywhere in it, and brought that child to the front. Then she looked
at everybody who was left, found the shortest of those, and stood her second. Then third. Each child,
once placed, never moved again. It took about the same amount of time, but the children liked it
more, because nobody got shuffled back and forth.

The third year was different, because that year the children came out of the classroom one at a time
instead of all at once. Anand took the first child and stood her by the wall. When the second came
out, he held him against the first, and put him on the correct side of her. The third child walked
along the little line that already existed, starting from the tall end, until he found the place
where he was shorter than the one on his left and taller than the one on his right, and he stepped in
there. Everybody after that shuffled one step along to make room.

And then it rained, and the children came out in the order they had been sitting in — which was more
or less last year's height order already. Anand finished in under two minutes. Each child walked one
or two places and stopped. The line was almost right before he started, and his way of doing it was
the only one that noticed.

---

## 3. The idea in plain English

Three teachers, three methods, one job. Every one of them is a sorting method you can write in eight
lines, and the differences between them are exactly what gets asked about.

Some vocabulary first, because all three share it.

A **comparison** is one question: *is this one bigger than that one?* A **swap** is exchanging two
values so each sits where the other was. **In place** means you rearrange the list you were handed
and use only a fixed amount of extra room — a couple of variables, not a second list. All three sorts
today are in place. And the **sorted region** is the part of the list you have already finished; every
one of these methods grows a sorted region and shrinks an unsorted one, and they differ in *which
end* the region grows from and *how* the next value gets there.

### Bubble sort — Meera's method

Walk the list from left to right. Look at each neighbouring pair. If the left one is bigger than the
right one, swap them. When you get to the end, go back to the start and do it again. Stop when you
manage a whole walk without swapping anything.

The name comes from what you see: on each walk, the biggest value still out of place gets carried all
the way to the right end, like a bubble rising. After the first walk the largest value is definitely
at the far right and never has to move again. After the second walk, the two largest are. So the
sorted region grows at the **right** end, one value per walk.

The stopping rule matters and it is the part beginners drop. If you finish a walk having made zero
swaps, the list is in order, and you can stop early. Without that check, bubble sort always does the
full `n` walks even on already-sorted input.

### Selection sort — Fathima's method

Look through the whole unsorted region and find the smallest value in it. Swap it into the first
unsorted position. Now the sorted region at the **left** end is one longer. Repeat.

The distinguishing feature is the number of swaps. Selection sort does exactly **n−1** swaps, ever —
one per position — no matter how jumbled the input is. It still does the same huge number of
comparisons, but it barely moves anything. That matters when a "swap" is expensive: writing to flash
memory, moving a large record, or anything where reading is cheap and writing is not.

### Insertion sort — Anand's method

Take the next unsorted value. Walk it backwards through the sorted region until you find where it
belongs, shifting each larger value one place to the right to make room. Drop it in.

The sorted region grows at the **left** end, and — this is the difference that matters — the amount
of work per value depends on how far back it has to walk. If it is already bigger than everything in
the sorted region, it walks zero steps and stops immediately.

That is why Anand finished in two minutes when it rained. On input that is already nearly in order,
every value walks one or two places and stops, so the total work is close to `n` rather than `n²`. A
method whose running time gets better when the input is already partly ordered is called
**adaptive**. Insertion sort is adaptive; bubble sort is adaptive only if you remember the early-stop
check; selection sort is never adaptive, because it must scan the entire unsorted region to be sure
it has found the smallest, and being nearly sorted does not shorten that scan by a single step.

### Which one to actually use

Insertion sort. Not as a general sort — for anything large you call `sorted()` and say `O(n log n)`,
as on [day 051](../day-051-why-sorting-matters/README.md). But insertion sort is the right answer in
three specific places, and being able to name them is what the question is really testing:

1. **Small inputs.** Under roughly 30 to 60 elements, insertion sort beats merge sort and quicksort
   in real time, because its per-element work is tiny and it does no allocation and no function
   calls. Python's Timsort sorts short runs with a form of insertion sort for exactly this reason.
2. **Nearly-sorted input.** A list with a handful of elements out of place is sorted in close to
   `O(n)`.
3. **Data arriving one at a time.** If you must keep a list ordered while new values keep coming, the
   insertion step *is* the method. There is nothing to sort; there is one value to place.

Bubble sort is the one you should be able to write and then say honestly is never the right choice.
It has selection sort's comparison count and a far worse move count. It survives because it is easy
to explain, not because anybody runs it.

---

## 4. The picture

Bubble sort, first walk over seven values. Watch the biggest value get carried right:

```
 start   [ 5 , 1 , 4 , 2 , 8 , 0 , 2 ]
           ^^^^^                          5 > 1, swap
         [ 1 , 5 , 4 , 2 , 8 , 0 , 2 ]
               ^^^^^                      5 > 4, swap
         [ 1 , 4 , 5 , 2 , 8 , 0 , 2 ]
                   ^^^^^                  5 > 2, swap
         [ 1 , 4 , 2 , 5 , 8 , 0 , 2 ]
                       ^^^^^              5 < 8, leave it
         [ 1 , 4 , 2 , 5 , 8 , 0 , 2 ]
                           ^^^^^          8 > 0, swap
         [ 1 , 4 , 2 , 5 , 0 , 8 , 2 ]
                               ^^^^^      8 > 2, swap
 after   [ 1 , 4 , 2 , 5 , 0 , 2 | 8 ]
                                    ^
                              LOCKED — the largest value is home after one walk
```

**What to notice:** one walk places exactly one value for certain. That is why you need `n−1` walks,
and it is where the `n²` comes from. Note also how far `5` travelled and how much shuffling that
caused — bubble sort's problem is not comparisons, it is moves.

Selection sort, same input. Watch the left end grow:

```
 pass 0  [ 5 , 1 , 4 , 2 , 8 , 0 , 2 ]    smallest of all 7 is 0, at position 5
          swap positions 0 and 5
 pass 1  [ 0 | 1 , 4 , 2 , 8 , 5 , 2 ]    smallest of the rest is 1, already in place
 pass 2  [ 0 , 1 | 4 , 2 , 8 , 5 , 2 ]    smallest of the rest is 2, at position 3
 pass 3  [ 0 , 1 , 2 | 8 , 5 , 4 , 2 ]    smallest of the rest is 2, at position 6
 pass 4  [ 0 , 1 , 2 , 2 | 5 , 4 , 8 ]    smallest of the rest is 4
 pass 5  [ 0 , 1 , 2 , 2 , 4 | 5 , 8 ]    smallest of the rest is 5, already in place
 done    [ 0 , 1 , 2 , 2 , 4 , 5 , 8 ]
              sorted  |  unsorted
```

**What to notice:** six passes, six swaps. Total. Selection sort scans an enormous number of values
and moves almost nothing — the exact opposite trade from bubble sort. Notice also that in pass 2 the
`2` at position 3 jumped over the `2` at position 6, so the two equal values ended up in the opposite
order from how they started. That is what "not stable" means, and it is the subject of
[day 057](../day-057-stability-and-pythons-sort/README.md).

Insertion sort, the same input. Watch each new value walk backwards:

```
                    sorted region  |  next value to place
 step 1   [ 5 ] | 1 , 4 , 2 , 8 , 0 , 2      take 1, walk it past 5
 step 2   [ 1 , 5 ] | 4 , 2 , 8 , 0 , 2      take 4, walk it past 5, stop at 1
 step 3   [ 1 , 4 , 5 ] | 2 , 8 , 0 , 2      take 2, walk past 5 and 4, stop at 1
 step 4   [ 1 , 2 , 4 , 5 ] | 8 , 0 , 2      take 8, ZERO steps -- already biggest
 step 5   [ 1 , 2 , 4 , 5 , 8 ] | 0 , 2      take 0, walk all the way to the front
 step 6   [ 0 , 1 , 2 , 4 , 5 , 8 ] | 2      take 2, walk past 8, 5, 4, stop after 2
 done     [ 0 , 1 , 2 , 2 , 4 , 5 , 8 ]
```

**What to notice:** step 4 costs one comparison and no moves, and step 5 costs five of each. The work
is *per value*, and it depends on the data. That single fact is the whole reason insertion sort is
worth knowing — on nearly-sorted input every step looks like step 4.

The same three methods, side by side on the question that matters:

```
                  comparisons        swaps / moves       best case      adaptive?
 bubble sort      ~ n^2 / 2          up to n^2 / 2       O(n) *         only with the flag
 selection sort   exactly n^2 / 2    exactly n - 1       O(n^2)         no, never
 insertion sort   up to n^2 / 2      up to n^2 / 2       O(n)           yes, naturally

 * with the early-stop check, and only on input that is already sorted
```

**What to notice:** three sorts with the same complexity class are not three of the same thing. The
column that separates them in practice is the one on the right.

---

## 5. The code, built step by step

### Bubble sort, one walk at a time

Start with the inner walk — one pass over neighbouring pairs:

```python
def one_pass(nums: list[int]) -> bool:
    """One left-to-right walk. Returns True if anything was swapped."""
    swapped = False
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
            swapped = True
    return swapped
```

Note `len(nums) - 1`, not `len(nums)`. The loop reads `nums[i + 1]`, so the last valid `i` is one
before the end. Getting that wrong is the single commonest bug in bubble sort and it raises a real
error, shown in §7. Note also `nums[i], nums[i + 1] = nums[i + 1], nums[i]` — Python evaluates the
right side fully before assigning, so this is a genuine swap with no temporary variable.

Now repeat the walk until nothing moves:

```python
def bubble_sort(nums: list[int]) -> None:
    """Sorts in place. Stops as soon as a full pass makes no swaps."""
    n = len(nums)
    for end in range(n - 1, 0, -1):        # the last unsorted position, shrinking
        swapped = False
        for i in range(end):               # never look past the sorted tail
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:
            return                         # already in order: stop
```

Two improvements over the naive version, and both get asked about. `range(end)` shrinks the walk each
pass, because after pass one the last value is known to be correct and re-checking it is wasted work.
The `swapped` flag is what makes bubble sort `O(n)` on already-sorted input rather than `O(n²)` — if
a whole walk changes nothing, nothing further can change.

### Selection sort

```python
def selection_sort(nums: list[int]) -> None:
    """Sorts in place. Exactly len(nums) - 1 swaps, always."""
    n = len(nums)
    for start in range(n - 1):
        smallest = start                       # assume the first unsorted one is smallest
        for i in range(start + 1, n):
            if nums[i] < nums[smallest]:
                smallest = i                   # remember WHERE, not the value
        nums[start], nums[smallest] = nums[smallest], nums[start]
```

The important line is `smallest = i`. You track the *position* of the smallest value, not the value
itself, because you need to know where to swap from. Beginners write `smallest = nums[i]` and then
cannot complete the swap.

`range(n - 1)` rather than `range(n)`: once the first `n−1` positions hold the right values, the last
one has nothing left to compete with. One free pass saved.

### Insertion sort

This is the one to learn properly. Build the inner walk first:

```python
def place(nums: list[int], j: int) -> None:
    """Walk nums[j] backwards into the sorted region nums[0:j]."""
    value = nums[j]
    i = j - 1
    while i >= 0 and nums[i] > value:
        nums[i + 1] = nums[i]      # shift the larger value one step right
        i -= 1
    nums[i + 1] = value            # the gap left behind is where it belongs
```

Read the loop condition in the right order. `i >= 0` must come first, because Python's `and` stops
evaluating as soon as the left side is false — so when `i` reaches `-1` the comparison `nums[i]` is
never attempted. Swap the two conditions round and you get a silent wrong answer, because `nums[-1]`
is the last element in Python rather than an error. That trap is in §7 with its output.

Notice there is no swapping here at all. Each larger value is copied one step right, and the value
being placed is written once, at the end. That is half the moves of a swap-based version.

The full sort is that fragment in a loop:

```python
def insertion_sort(nums: list[int]) -> None:
    """Sorts in place. O(n) on nearly-sorted input, O(n^2) worst case."""
    for j in range(1, len(nums)):
        value = nums[j]
        i = j - 1
        while i >= 0 and nums[i] > value:
            nums[i + 1] = nums[i]
            i -= 1
        nums[i + 1] = value
```

`range(1, len(nums))` starts at 1, because a single element is already a sorted region of size one.
That is the invariant, in the sense of [day 028](../day-028-opposite-ends/README.md): **before each
step, `nums[0:j]` holds the first `j` values in sorted order.** Say that sentence out loud when you
write this in an interview; it is the thing that proves you understand it rather than remember it.

### The condition that keeps it stable

`nums[i] > value` uses a strict `>`. If you write `>=` instead, an incoming value walks *past* values
equal to it, and two equal elements come out in the opposite order from how they went in. The sort
still returns a correctly ordered list, so nothing fails — it silently stops being stable. One
character.

### Binary insertion sort, and why it does not help much

An obvious-looking improvement: instead of walking backwards to find the spot, binary search for it.

```python
from bisect import bisect_right

def binary_insertion_sort(nums: list[int]) -> None:
    for j in range(1, len(nums)):
        value = nums[j]
        pos = bisect_right(nums, value, 0, j)   # where it belongs, in O(log j)
        nums[pos + 1 : j + 1] = nums[pos:j]     # shift the block right by one
        nums[pos] = value
```

This cuts comparisons from `O(n²)` to `O(n log n)` — and the running time stays `O(n²)`, because you
still have to *shift* every larger element to make room, and shifting is the expensive part. Worth
knowing as a follow-up answer: it is a real improvement only when comparing two elements is far more
expensive than moving them, such as sorting long strings by content.

### The complete file

```python
"""The three quadratic sorts, in place, with the properties that distinguish them."""

from bisect import bisect_right


def bubble_sort(nums: list[int]) -> None:
    """Repeatedly swap out-of-order neighbours. O(n^2); O(n) if already sorted.

    Stable. In place. Never the right choice in production -- learn it to explain it.
    """
    for end in range(len(nums) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:
            return


def selection_sort(nums: list[int]) -> None:
    """Repeatedly move the smallest remaining value to the front. Always O(n^2).

    NOT stable. Exactly n - 1 swaps -- the fewest writes of any comparison sort,
    which is the one situation where it wins.
    """
    n = len(nums)
    for start in range(n - 1):
        smallest = start
        for i in range(start + 1, n):
            if nums[i] < nums[smallest]:
                smallest = i
        if smallest != start:                       # skip the pointless self-swap
            nums[start], nums[smallest] = nums[smallest], nums[start]


def insertion_sort(nums: list[int]) -> None:
    """Grow a sorted prefix by walking each new value back into it.

    Stable (because the comparison is strict >). In place. O(n) on nearly-sorted
    input, which is why real libraries use it for small and almost-ordered runs.
    Invariant: before step j, nums[0:j] holds the first j values in sorted order.
    """
    for j in range(1, len(nums)):
        value = nums[j]
        i = j - 1
        while i >= 0 and nums[i] > value:
            nums[i + 1] = nums[i]
            i -= 1
        nums[i + 1] = value


def binary_insertion_sort(nums: list[int]) -> None:
    """Insertion sort with a binary search for the position.

    O(n log n) comparisons but still O(n^2) moves -- worth it only when a
    comparison costs far more than a move.
    """
    for j in range(1, len(nums)):
        value = nums[j]
        pos = bisect_right(nums, value, 0, j)
        nums[pos + 1 : j + 1] = nums[pos:j]
        nums[pos] = value


def insert_into_sorted(sorted_nums: list[int], value: int) -> None:
    """The real use of the insertion idea: keep a list ordered as values arrive.

    O(n) per value because of the shift, but there is no sort here at all --
    one value, one placement.
    """
    i = len(sorted_nums) - 1
    sorted_nums.append(value)
    while i >= 0 and sorted_nums[i] > value:
        sorted_nums[i + 1] = sorted_nums[i]
        i -= 1
    sorted_nums[i + 1] = value


if __name__ == "__main__":
    from copy import deepcopy

    data = [5, 1, 4, 2, 8, 0, 2]

    for sort in (bubble_sort, selection_sort, insertion_sort, binary_insertion_sort):
        nums = deepcopy(data)
        sort(nums)
        print(f"{sort.__name__:24} {nums}")
    # bubble_sort              [0, 1, 2, 2, 4, 5, 8]
    # selection_sort           [0, 1, 2, 2, 4, 5, 8]
    # insertion_sort           [0, 1, 2, 2, 4, 5, 8]
    # binary_insertion_sort    [0, 1, 2, 2, 4, 5, 8]

    # the adaptive difference, made visible by counting shifts
    def count_shifts(nums: list[int]) -> int:
        shifts = 0
        for j in range(1, len(nums)):
            value = nums[j]
            i = j - 1
            while i >= 0 and nums[i] > value:
                nums[i + 1] = nums[i]
                i -= 1
                shifts += 1
            nums[i + 1] = value
        return shifts

    print(count_shifts(list(range(1000))))            # 0      -- already sorted
    print(count_shifts(list(range(1000, 0, -1))))     # 499500 -- exactly reversed
    nearly = list(range(1000))
    nearly[100], nearly[103] = nearly[103], nearly[100]
    print(count_shifts(nearly))                       # 6      -- nearly sorted

    # keeping a list ordered as data arrives
    running: list[int] = []
    for x in [7, 3, 9, 1, 5]:
        insert_into_sorted(running, x)
        print(running)
    # [7] / [3, 7] / [3, 7, 9] / [1, 3, 7, 9] / [1, 3, 5, 7, 9]
```

---

## 6. What it costs

### Counting the comparisons

Take selection sort, because it is the easiest to count exactly and the count is the same for all
three in the worst case.

The outer loop runs with `start = 0, 1, 2, ..., n−2`. For `start = 0`, the inner loop runs from 1 to
`n−1`, which is `n−1` comparisons. For `start = 1` it is `n−2`. And so on down to 1.

```
 (n-1) + (n-2) + (n-3) + ... + 2 + 1  =  n(n-1)/2

 n =    10  ->      45 comparisons
 n =   100  ->   4,950
 n = 1,000  ->  499,500
 n = 10,000 ->  49,995,000
```

That sum, `n(n−1)/2`, is `(n² − n)/2`. Drop the constant and the lower-order term and it is
**O(n²)**. Ten times the data is a hundred times the work, and that is the sentence to say out loud.

### The three, priced separately

The complexity class is the same. The actual work is not.

```
                       comparisons              element moves          best case
 bubble sort           up to n(n-1)/2           up to 3 x n(n-1)/2 *   O(n) with the flag
 selection sort        exactly  n(n-1)/2        exactly 3(n-1) *       O(n^2) always
 insertion sort        up to n(n-1)/2           up to n(n-1)/2         O(n)

 * a swap is three writes: temp = a; a = b; b = temp.
   Insertion sort SHIFTS rather than swaps, so it writes once per displaced element.
```

At `n = 1,000` on reversed input:

```
 bubble sort      499,500 comparisons  +  1,498,500 writes
 selection sort   499,500 comparisons  +      2,997 writes
 insertion sort   499,500 comparisons  +    500,499 writes
```

Selection sort does five hundred times fewer writes than bubble sort for the same answer. If you are
sorting records of two kilobytes each, or writing to storage where each write wears the hardware out,
that column is the only one that matters. This is the honest case for selection sort, and it is the
one thing it is good at.

### The adaptive case, which is why insertion sort survives

```
 n = 1,000

 already sorted        insertion sort:      999 comparisons, 0 moves      -> O(n)
                       selection sort:  499,500 comparisons               -> O(n^2)

 10 elements out of place, each by 3 positions
                       insertion sort:  ~1,030 comparisons, ~30 moves     -> O(n)
                       selection sort:  499,500 comparisons               -> O(n^2)
```

Nearly-sorted input makes insertion sort roughly **five hundred times faster** than selection sort at
`n = 1,000`, and selection sort does not get one comparison cheaper. That gap is the answer to "when
would you actually use it".

### Against the real sorts

```
 n = 1,000    insertion sort  ~ 500,000 operations
              merge sort      ~ 1,000 x 10 = 10,000 operations     -> 50x faster

 n = 30       insertion sort  ~ 30 x 29 / 2 = 435 operations, no allocation, no calls
              merge sort      ~ 30 x 5 = 150 "operations", plus 30 list allocations
                                 and ~60 function calls
                                                       -> insertion sort WINS in real time
```

The crossover in real implementations sits somewhere between 30 and 60 elements, depending on the
language. Below it, `n²` with a tiny constant beats `n log n` with a large one. Above it, nothing
saves you. Python's Timsort uses 64 as its threshold and sorts anything shorter with a binary
insertion sort — the full story is on
[day 057](../day-057-stability-and-pythons-sort/README.md).

### Space

All three are **O(1) extra space**. They mutate the list they are given and hold at most a couple of
loop variables. That is worth saying explicitly in an interview, because merge sort tomorrow is not,
and the contrast is one of the standard follow-ups.

---

## 7. The traps

### The real error: walking one step too far

```python
def bubble_broken(nums):
    for _ in range(len(nums)):
        for i in range(len(nums)):        # <-- should be len(nums) - 1
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]

bubble_broken([5, 1, 4])
```

```
Traceback (most recent call last):
  File "day52.py", line 8, in <module>
    bubble_broken([5, 1, 4])
    ~~~~~~~~~~~~~^^^^^^^^^^^
  File "day52.py", line 4, in bubble_broken
    if nums[i] > nums[i + 1]:
                 ~~~~^^^^^^^
IndexError: list index out of range
```

The rule, and it is worth saying as a rule: **if the body reads `nums[i + 1]`, the loop stops at
`len(nums) - 1`.** Any time you compare an element with its neighbour, the range shrinks by one.

### The near-miss that gives a wrong answer with no error

This is the one that costs interviews, because nothing crashes.

```python
def insertion_broken(nums):
    for j in range(1, len(nums)):
        value = nums[j]
        i = j - 1
        while nums[i] > value and i >= 0:      # <-- conditions in the wrong order
            nums[i + 1] = nums[i]
            i -= 1
        nums[i + 1] = value
    return nums

print(insertion_broken([3, 1, 2]))
```

```
[1, 2, 3]
```

It worked. Run it on the input that exposes it — one where the smallest value is not first:

```python
print(insertion_broken([2, 3, 1]))
```

```
[3, 1, 2]
```

Wrong, and no exception. Here is why. When `i` reaches `-1`, Python evaluates `nums[-1] > value`
first, and `nums[-1]` is the **last element of the list**, not an error. That comparison happens to
be true, so the loop runs one more time, writes into `nums[0]`, and `i` becomes `-2`. Then `nums[-2]`
is the second-to-last element. The walk wraps around the end of the list and corrupts it.

`i >= 0` must come first. Python's `and` short-circuits — it never evaluates the right side if the
left side is false — and that is exactly what protects the lookup. **When one condition guards
another, the guard goes first.**

### The near-miss: bubble sort without the flag

```python
def bubble_no_flag(nums):
    for end in range(len(nums) - 1, 0, -1):
        for i in range(end):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
```

Correct output, always. But hand it a sorted list of a thousand elements and it performs 499,500
comparisons to discover that there was nothing to do. With the flag it performs 999 and returns. The
interviewer will ask "what is the best case?" and the honest answer for this version is `O(n²)`, not
`O(n)`. One boolean is the difference between the two answers.

### The trap: tracking the value instead of the position

```python
def selection_broken(nums):
    for start in range(len(nums) - 1):
        smallest = nums[start]                  # <-- the value, not the position
        for i in range(start + 1, len(nums)):
            if nums[i] < smallest:
                smallest = nums[i]
        nums[start], nums[smallest] = nums[smallest], nums[start]
    return nums

print(selection_broken([5, 1, 4]))
```

```
Traceback (most recent call last):
  File "day52.py", line 9, in <module>
    print(selection_broken([5, 1, 4]))
          ~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "day52.py", line 7, in selection_broken
    nums[start], nums[smallest] = nums[smallest], nums[start]
                                  ~~~~^^^^^^^^^^
IndexError: list index out of range
```

You cannot swap using a value; you need to know where it lives. And when the values happen to be
small non-negative integers this bug does *not* raise — it silently swaps the wrong pair. Track
positions.

### The trap: `>=` instead of `>` quietly loses stability

```python
while i >= 0 and nums[i] >= value:      # <-- was >
```

The list still comes out correctly ordered, so no test on the numbers catches it. But sort a list of
`(name, score)` pairs by score and the names within each score come out reversed. Nothing fails until
somebody sorts by two fields in two passes, as on
[day 051](../day-051-why-sorting-matters/README.md), and gets an order they cannot explain. Strict
`>` keeps equal elements in their original order. One character, and it is worth pointing at
unprompted in an interview.

### The trap: sorting in place and then using the return value

```python
nums = [3, 1, 2]
result = insertion_sort(nums)
print(result[0])
```

```
Traceback (most recent call last):
  File "day52.py", line 3, in <module>
    print(result[0])
          ~~~~~~^^^
TypeError: 'NoneType' object is not subscriptable
```

All three functions here sort in place and return `None`, which is the same convention `list.sort()`
follows. Decide which you are writing, say so in the docstring, and be consistent. If the interviewer
expects a returned list, `return nums` at the end and say you are doing it.

---

## 8. In the interview

### How it gets asked

- *"Write insertion sort."* — asked plainly, often as a warm-up before something harder, and the real
  test is whether you can finish it without an off-by-one and then say something intelligent about
  it.
- *"When would you actually use insertion sort? It's O(n²)."* — the real question. Three answers:
  small inputs, nearly-sorted inputs, and data arriving one at a time.
- *"You have three O(n²) sorts. Why does anyone distinguish them?"* — comparisons against moves, best
  case, stability.
- *"Your data is almost sorted — a few elements are out of place. What do you use?"* — insertion
  sort, and the reason has to be the adaptive argument, not a preference.
- *"Which of these is stable?"* — insertion and bubble are; selection is not, and you should be able
  to give the two-element example that shows it.

### What to say out loud, in the first ninety seconds

1. **Name the shape before you write.** *"Insertion sort grows a sorted region at the front. For each
   new value I walk it backwards through that region, shifting larger values right, until it lands."*
2. **State the invariant.** *"Before step j, the first j elements are the original first j values, in
   sorted order. That is what I am maintaining."*
3. **Flag the guard as you write it.** *"The `i >= 0` has to come before the comparison, because
   `nums[-1]` is the last element in Python rather than an error — it would wrap round and corrupt
   the list."*
4. **Say shift, not swap.** *"I'm shifting rather than swapping, so each displaced element is written
   once instead of three times, and the value being placed is written once at the end."*
5. **Give the cost with the case attached.** *"O(n²) worst case, O(n) best case, O(1) extra space,
   and it is stable because the comparison is strict."*

### The follow-ups

**"It's O(n²). When would you actually use it?"**
Three situations, and the first is the one that matters most, because every real sorting library does
it. On small inputs insertion sort genuinely beats merge sort and quicksort in wall-clock time — the
constant factor is tiny, there is no allocation, no recursion and no function-call overhead, so
somewhere between thirty and sixty elements the `n²` with a small constant wins against `n log n`
with a large one. That is not a theoretical point: Python's Timsort splits the list into runs and
sorts anything under sixty-four elements with a binary insertion sort, and the same trick is in the
C++ and Java standard libraries. The second situation is nearly-sorted input. Insertion sort is
adaptive: each value walks backwards only as far as it needs to, so if ten elements out of a thousand
are three places out of position, the whole sort is about a thousand comparisons and thirty moves —
order `n`, not `n²`. That comes up more than people expect, because a log file that is almost in
timestamp order, or a list that was sorted and then had a few items updated, is a real thing. The
third is when the data arrives one at a time and you must keep the collection ordered as it does.
Then there is no sort at all — there is one value and one placement, and the insertion step is
exactly the operation you need. What I would not claim is that it is a general-purpose sort. For a
large unordered list I call `sorted()` and say `O(n log n)`.

**"Which of the three are stable, and why does it matter?"**
Insertion sort and bubble sort are stable; selection sort is not. Stable means two elements that
compare equal come out in the order they went in. Insertion sort is stable because the walk stops the
moment it meets a value that is not strictly greater — an incoming element never passes an equal one,
so equal elements keep their relative order. Bubble sort is stable for the same reason: it only swaps
when the left element is strictly greater. Selection sort is not, and the counter-example is small:
take `[2a, 2b, 1]`, where the two twos are distinct records that compare equal. The first pass finds
`1` as the smallest and swaps it with position zero, which throws `2a` to the back, and the result is
`[1, 2b, 2a]` — the twos have swapped order. The long-distance swap is what breaks it, and no version
of selection sort avoids that without giving up its one advantage, the `n−1` swap count. It matters
because of multi-pass sorting: if you sort by name and then by department, only a stable sort leaves
the names ordered within each department. That is the standard way to sort by several keys, and it
silently produces the wrong order with an unstable sort — no error, just an answer you cannot
explain.

**"Why would anyone use selection sort at all?"**
For exactly one property: it performs the fewest writes of any comparison sort. Exactly `n−1` swaps,
which is `3(n−1)` element writes, regardless of the input. Bubble sort on reversed data of a thousand
elements does about a million and a half writes; selection sort does two thousand nine hundred and
ninety-seven. That matters whenever a write is much more expensive than a read: sorting large records
in place where each move copies kilobytes, or writing to flash memory or EEPROM, where each cell
tolerates a limited number of erase cycles and the hardware physically wears out. Outside of that, no
— it is strictly worse than insertion sort, because it has the same comparison count, is not
adaptive, and is not stable. I would name the write-count argument and then say plainly that on a
normal list in memory I would not use it.

### A model answer

> "Insertion sort keeps a sorted region at the front of the list and grows it by one element at a
> time. For each new value I copy it out, then walk backwards through the sorted region shifting every
> larger element one place to the right, and when I find one that isn't larger — or run off the front
> — I drop the value into the gap.
>
> ```python
> def insertion_sort(nums: list[int]) -> None:
>     for j in range(1, len(nums)):
>         value = nums[j]
>         i = j - 1
>         while i >= 0 and nums[i] > value:
>             nums[i + 1] = nums[i]
>             i -= 1
>         nums[i + 1] = value
> ```
>
> Two things in there I'd point at. The `i >= 0` comes first deliberately — `and` short-circuits, and
> if the comparison ran first then at `i = -1` Python would read the *last* element of the list rather
> than raising, and the walk would wrap round and corrupt it. And the comparison is a strict `>`,
> which is what makes this stable: an incoming value never walks past a value equal to it, so equal
> elements keep their original order. With `>=` it still sorts correctly but silently stops being
> stable, and that breaks multi-pass sorting by two keys.
>
> The invariant is: before step j, the first j elements are the original first j values in sorted
> order. Cost is O(n²) worst case — reversed input, where every value walks the whole way back, giving
> n(n−1)/2 comparisons, about half a million at a thousand elements. Best case is O(n): on already
> sorted input each value fails the comparison immediately and does zero moves, so it's n−1
> comparisons. Space is O(1) — it's in place, unlike merge sort.
>
> As for when I'd use it: not as a general sort, I'd call `sorted()` for that. But three real cases.
> Small inputs, under about fifty elements, where the tiny constant factor beats an O(n log n) sort
> with allocation and recursion — Python's Timsort does exactly this, it insertion-sorts runs shorter
> than sixty-four. Nearly-sorted input, because it's adaptive: ten elements a few places out of a
> thousand costs about a thousand comparisons, not half a million. And streaming data, where I need to
> keep a list ordered as values arrive — then the insertion step is the whole operation and there's no
> sort to speak of."

---

## 9. Recall card

- **All three are O(n²), in place, O(1) space — and they differ where it counts.** Bubble: swap
  out-of-order neighbours, largest sinks right, needs the `swapped` flag to be O(n) on sorted input.
  Selection: find the smallest, swap it forward — **exactly n−1 swaps**, never adaptive, **not
  stable**. Insertion: walk each value back into the sorted prefix, shifting as you go.
- **Insertion sort is the only one with a real answer to "when would you use it":** small inputs
  (under ~50; Timsort's threshold is 64), nearly-sorted input (**adaptive** — O(n)), and values
  arriving one at a time.
- **The invariant to say out loud:** *before step j, `nums[0:j]` holds the first j values in sorted
  order.* And it **shifts rather than swaps** — one write per displaced element instead of three.
- **Two one-character traps.** `while i >= 0 and nums[i] > value` — the guard must come first or
  `nums[-1]` wraps round and corrupts the list, silently. And `>` not `>=`, or you lose **stability**
  with no visible failure.
- **The arithmetic:** n(n−1)/2 = 499,500 comparisons at n = 1,000. Writes on reversed input:
  bubble 1,498,500 · insertion 500,499 · **selection 2,997** — selection sort's only virtue, and it
  matters for flash memory and large records.
