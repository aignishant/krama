---
day: 53
track: dsa
title: "Merge sort"
phase: "Sorting"
status: written
---

# Day 053 · DSA — Merge sort

**After today you can:** You can write merge sort and explain the divide-and-conquer shape it teaches.

**The interviewer asks it as:** *Write merge sort. Why is it O(n log n)?*

---

## 1. What this is, and why they ask it

Merge sort is the first sorting method that is genuinely fast. It works by cutting the list in half,
sorting each half, and then **merging** the two sorted halves back into one — and merging two already
sorted lists is cheap, because you only ever have to look at the front of each. It runs in
`O(n log n)` time on every input, with no bad cases at all, and it is stable.

They ask it for the same reason they ask about binary search: the pattern matters more than the
function. **Divide and conquer** — split the problem, solve the pieces, combine the answers — is the
shape behind quicksort tomorrow, behind most tree problems from
[day 098](../day-098-what-a-tree-is/README.md), and behind half of the interview questions that
sound nothing like sorting. And the merge step is a standalone skill: "merge two sorted lists" is
LeetCode 88 and LeetCode 21, it is the core of "merge k sorted lists"
([day 117](../day-117-merge-k-sorted/README.md)), and it is how a database joins two indexed tables.
Yesterday's three sorts were `O(n²)`. Today is the day the arithmetic changes, and being able to say
*why* it changes — not just that it does — is the whole question.

---

## 2. The story

Sarita teaches at a school in Nagpur, and every March the half-yearly exams finish and two hundred
and forty answer booklets land on the staff room table in one heap. They have to reach the head's
office in roll number order by the evening, and for her first two years she did that job alone.

She would pick up a booklet, find where it belonged in the little run she had built so far, and slot
it in. Two hours, every time, and by the end of it her back hurt from standing.

The third year Mrs Kulkarni came in, looked at the heap, and split it into four roughly equal piles.
One for Sarita, one for Girish, one for Anjali, one for herself. Everyone arranged their own quarter,
sixty booklets each, and that part took about fifteen minutes because sixty is nothing.

Then there were four neat piles in order and the office wanted one.

Sarita and Girish sat at one end of the long table with their two piles in front of them, and this is
the part she still thinks was clever. They never looked at more than two booklets. Whichever of the
two top booklets had the smaller roll number came off and went face down on a new pile between them.
Then they looked at the two new tops and did it again. Neither of them ever searched for anything,
because the top of a pile that is already in order is the smallest one left in it. When Girish's pile
ran out, Sarita picked up everything she had left and put it on the new pile in one movement, still
in order, without checking a single number.

Anjali and Mrs Kulkarni did the same thing at the other end of the table. Then the two of them
combined the two big piles the same way. Three combining sessions in all, and every booklet passed
through a hand exactly once in each session.

One thing they got wrong the first time and never again: they tried it on a small desk. You cannot
combine two piles into one without somewhere to build the new pile. They needed the space of the
whole table, empty, next to the piles they were working from.

The whole thing finished in twenty-five minutes. What Sarita noticed afterwards was that the
combining sessions were not the slow part at all. Every session touched all two hundred and forty
booklets, but there were only three sessions.

---

## 3. The idea in plain English

Sarita's four teachers are merge sort. Splitting the heap is the divide. Each teacher arranging her
own quarter is conquering a smaller version of the same problem. The two-piles-into-one sessions are
the **merge**, and the empty table is the extra memory merge sort needs.

There are three ideas here and they arrive in order.

### One: merging two sorted lists is cheap

This is the engine, so learn it on its own before the sort.

You have two lists, each already in order. You want one list containing everything, in order. Look
only at the front of each list. The smaller of those two is the smallest value remaining anywhere, so
it goes next into the output. Move past it, and look again.

```
 left   [ 2 , 5 , 9 ]        right  [ 1 , 6 , 7 ]        out  [ ]
          ^                           ^
   compare 2 and 1 -> take 1
 left   [ 2 , 5 , 9 ]        right  [ 1 , 6 , 7 ]        out  [ 1 ]
          ^                               ^
   compare 2 and 6 -> take 2
```

You never search. Each step takes one comparison and moves one value into the output, so merging two
lists of total length `n` costs `n` comparisons at worst. That is **O(n)**, and it is the fact
everything else today rests on. When one list runs out, the rest of the other is copied straight
across with no comparisons at all — Sarita picking up her remaining booklets in one movement.

### Two: a function that calls itself

Merge sort is defined in terms of itself. To sort a list, you sort two smaller lists and merge them.
That is **recursion**: a function whose body calls the same function on a smaller piece of the
problem.

If you have not met it before, here is the whole of it. When Python runs a function call it pauses the
current call, runs the new one, and then resumes exactly where it left off. There is no limit on
this in principle — a function can call itself, and each call gets its own private copy of its
variables. So `merge_sort` on eight elements pauses and calls `merge_sort` on four; that call pauses
and calls `merge_sort` on two; that one pauses and calls `merge_sort` on one, which does nothing
because a single element is already in order, and returns. Then everything resumes on the way back
up, merging as it goes.

Two things must be true or it never stops:

- **A base case.** A rule that returns without calling itself again. Here it is "a list of length 0
  or 1 is already sorted".
- **Progress towards it.** Each call must work on something strictly smaller. Here each call gets
  half the list, so after a handful of steps the length is 1.

Recursion gets a phase of its own from [day 087](../day-087-recursion-leap-of-faith/README.md). Today
you need only those two rules, and a version that avoids recursion entirely is in §5 so you can see
the same sort written as plain loops.

### Three: the halving is where `log n` comes from

Halve 240 and you get 120, then 60, then 30, 15, 8, 4, 2, 1. That is eight steps. Halving any number
down to 1 takes about `log₂ n` steps — the same fact that made binary search `O(log n)` on
[day 042](../day-042-binary-search-idea/README.md).

So the work stacks up like this. Each **level** of splitting has some number of pieces, and merging
all the pieces at that level touches every element exactly once — `n` work per level, no matter how
many pieces there are. And there are `log₂ n` levels. So the total is `n × log₂ n`.

That is the whole complexity argument, and it is worth saying in exactly that order: **n work per
level, log n levels.** Not "because it divides in half", which is only half the reason. Binary search
also divides in half and is `O(log n)`, because it *throws away* one half rather than sorting both.
Merge sort visits both halves, and that is the difference.

### What merge sort gives you that yesterday's sorts do not

- **`O(n log n)` on every input.** Best case, average case and worst case are the same. There is no
  input that makes merge sort slow, which is not true of quicksort tomorrow.
- **Stable.** Equal elements keep their original order, provided the merge takes from the left list
  when the two fronts are equal. That is one `<=` and it is in §7.
- **It works when the data does not fit in memory.** Sort chunks that fit, write them out, then merge
  the sorted chunks. That is **external merge sort**, and it is what a database does for a large
  `ORDER BY` — the sort you saw spilling to disk in a query plan on
  [day 032](../day-032-variable-window/README.md).

### What it costs you

**`O(n)` extra space.** The merge cannot be done in place with any reasonable code — you need
somewhere to build the output, which is Sarita's empty table. That is the one real drawback and it is
the first follow-up you will be asked.

---

## 4. The picture

The split, then the merge, on eight values. Read down, then back up:

```
                    [ 38, 27, 43,  3,  9, 82, 10 ]
                            /                 \
              [ 38, 27, 43 ]                 [  3,  9, 82, 10 ]
                 /       \                      /            \
          [ 38 ]      [ 27, 43 ]         [  3,  9 ]      [ 82, 10 ]
                        /    \             /     \         /     \
                   [ 27 ]  [ 43 ]      [ 3 ]   [ 9 ]   [ 82 ]  [ 10 ]

  ---------------------------- turn around here ----------------------------

                   [ 27 ]  [ 43 ]      [ 3 ]   [ 9 ]   [ 82 ]  [ 10 ]
                        \    /             \     /         \     /
          [ 38 ]      [ 27, 43 ]         [  3,  9 ]      [ 10, 82 ]
                 \       /                      \            /
              [ 27, 38, 43 ]                 [  3,  9, 10, 82 ]
                            \                 /
                    [  3,  9, 10, 27, 38, 43, 82 ]
```

**What to notice:** count the levels — four of them for seven elements, which is `log₂ 7` rounded up
plus one. Now look across any single level on the way back up: the total number of values being
merged is always seven. That is the `n` per level, and multiplying the two gives `n log n`. Notice
also that nothing is sorted on the way *down*; all the work happens on the way back up.

The merge step itself, in detail. Two positions walking forward, and an output being filled:

```
 left   index  0    1    2              right  index  0    1    2
              +----+----+----+                       +----+----+----+
       value  | 27 | 38 | 43 |                 value |  3 |  9 | 82 |
              +----+----+----+                       +----+----+----+
                 ^                                      ^
                 i                                      j

 out  [ ]              compare left[0]=27 with right[0]=3  ->  3 is smaller, take it, j++
 out  [ 3 ]            compare 27 with 9                   ->  9 is smaller, take it, j++
 out  [ 3, 9 ]         compare 27 with 82                  -> 27 is smaller, take it, i++
 out  [ 3, 9, 27 ]     compare 38 with 82                  -> 38 is smaller, take it, i++
 out  [ 3, 9, 27, 38 ] compare 43 with 82                  -> 43 is smaller, take it, i++
 out  [ 3, 9, 27, 38, 43 ]
                       i has run off the end of left
                       -> copy the whole remaining right in one go: 82
 out  [ 3, 9, 27, 38, 43, 82 ]
```

**What to notice:** six values, six steps, five comparisons. Every step consumes exactly one value.
That is why the merge is `O(n)` and not `O(n²)` — there is no searching anywhere in it. And notice
the last line: when one side empties, the rest of the other is appended with zero comparisons.

Where the memory goes, which is the follow-up question drawn:

```
  the input           [ 38, 27, 43,  3,  9, 82, 10 ]        n slots

  during a merge      left  [ 27, 38, 43 ]                  the two halves exist
                      right [  3,  9, 10, 82 ]              as separate lists
                      out   [  3,  9, 10, 27, 38, 43, 82 ]  plus the output

  peak extra memory:  O(n) -- one full extra copy of the data, at the top level
```

**What to notice:** merge sort is not in place. Yesterday's three sorts used `O(1)` extra space and
this uses `O(n)`. Say that out loud before the interviewer asks.

---

## 5. The code, built step by step

### The merge, on its own

Everything depends on this, so write it first and test it before you write the sort.

```python
def merge(left: list[int], right: list[int]) -> list[int]:
    out: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <= not < -- this is what keeps it stable
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])                   # whichever side is left over, in one go
    out.extend(right[j:])                  # exactly one of these two does anything
    return out
```

Three things to notice. The loop runs only while **both** lists have something left, which is why the
two `extend` lines afterwards are not optional — without them you silently lose the tail. The `<=`
rather than `<` is what makes the whole sort stable: when the two fronts are equal, taking from the
left preserves the original order. And `left[i:]` on a spent list is `[]`, so both `extend` calls are
always safe to run; exactly one of them ever has anything to add.

### The sort, in four lines

```python
def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:                     # base case: nothing to do
        return nums
    middle = len(nums) // 2
    return merge(merge_sort(nums[:middle]), merge_sort(nums[middle:]))
```

That really is the whole sort. Read it as a sentence: *a list of one is already sorted; otherwise
sort the left half, sort the right half, and merge them.*

`len(nums) // 2` uses integer division. Write `/` instead and you get a float, and slicing with a
float raises — the exact message is in §7. And note the base case is `<= 1`, not `== 1`: an empty
list must return too, or a list of odd length eventually produces an empty half and the recursion
never stops.

### Why it always makes progress

`nums[:middle]` and `nums[middle:]` between them contain every element exactly once, and both are
strictly shorter than `nums` whenever `len(nums) >= 2`. That guarantee is what makes the base case
reachable. If you wrote `nums[:middle]` and `nums[middle - 1:]` by mistake, one branch would stop
shrinking and Python would eventually raise `RecursionError`, which is also in §7.

### The in-place version, which is what interviewers usually want

The version above allocates a new list at every level. The standard version sorts one list in place
using a single scratch buffer, and it is what you should be able to produce if asked for the
"proper" implementation:

```python
def merge_sort_in_place(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Sorts nums[lo:hi] in place. Still O(n) extra space -- the buffer inside merge."""
    if hi is None:
        hi = len(nums)
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    merge_sort_in_place(nums, lo, mid)
    merge_sort_in_place(nums, mid, hi)
    _merge_range(nums, lo, mid, hi)
```

```python
def _merge_range(nums: list[int], lo: int, mid: int, hi: int) -> None:
    """Merge the two sorted runs nums[lo:mid] and nums[mid:hi] back into nums[lo:hi]."""
    buffer = nums[lo:mid]                  # copy only the LEFT half out
    i, j, k = 0, mid, lo
    while i < len(buffer) and j < hi:
        if buffer[i] <= nums[j]:
            nums[k] = buffer[i]
            i += 1
        else:
            nums[k] = nums[j]
            j += 1
        k += 1
    while i < len(buffer):                 # the right half is already in place
        nums[k] = buffer[i]
        i, k = i + 1, k + 1
```

Only the left half is copied out. The right half never needs copying, because anything still unread
in it sits at or beyond the write position `k` — a value can never be overwritten before it is read.
That is a genuinely subtle point and worth saying out loud if you write this version.

### Bottom-up merge sort, with no recursion at all

Same algorithm, written as loops. Merge every neighbouring pair of runs of size 1, then of size 2,
then 4, and so on:

```python
def merge_sort_bottom_up(nums: list[int]) -> list[int]:
    """No recursion. Merge runs of width 1, then 2, then 4 ... until width >= n."""
    out = list(nums)
    n = len(out)
    width = 1
    while width < n:
        for lo in range(0, n, width * 2):
            mid = min(lo + width, n)
            hi = min(lo + width * 2, n)
            out[lo:hi] = merge(out[lo:mid], out[mid:hi])
        width *= 2
    return out
```

The `min` calls handle the last group when `n` is not a power of two — the final piece is simply
shorter, and merging a list with an empty list returns it unchanged. This version has the same
`O(n log n)` cost and no recursion depth at all, which makes it the safe choice for very large inputs
in Python.

### The complete file

```python
"""Merge sort: divide, conquer, and the merge that makes it O(n log n)."""


def merge(left: list[int], right: list[int]) -> list[int]:
    """Combine two sorted lists into one sorted list. O(len(left) + len(right)).

    Stable: when the fronts are equal, the LEFT value is taken first.
    """
    out: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(nums: list[int]) -> list[int]:
    """O(n log n) always -- best, average and worst. O(n) extra space. Stable.

    n work per level of merging, log2(n) levels.
    """
    if len(nums) <= 1:
        return nums
    middle = len(nums) // 2
    return merge(merge_sort(nums[:middle]), merge_sort(nums[middle:]))


def merge_sort_bottom_up(nums: list[int]) -> list[int]:
    """The same sort with no recursion -- safe for inputs deeper than Python's limit."""
    out = list(nums)
    n = len(out)
    width = 1
    while width < n:
        for lo in range(0, n, width * 2):
            mid = min(lo + width, n)
            hi = min(lo + width * 2, n)
            out[lo:hi] = merge(out[lo:mid], out[mid:hi])
        width *= 2
    return out


def _merge_range(nums: list[int], lo: int, mid: int, hi: int) -> None:
    buffer = nums[lo:mid]
    i, j, k = 0, mid, lo
    while i < len(buffer) and j < hi:
        if buffer[i] <= nums[j]:
            nums[k] = buffer[i]
            i += 1
        else:
            nums[k] = nums[j]
            j += 1
        k += 1
    while i < len(buffer):
        nums[k] = buffer[i]
        i, k = i + 1, k + 1


def merge_sort_in_place(nums: list[int], lo: int = 0, hi: int | None = None) -> None:
    """Sort nums[lo:hi] in place. Copies only the left half in each merge."""
    if hi is None:
        hi = len(nums)
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    merge_sort_in_place(nums, lo, mid)
    merge_sort_in_place(nums, mid, hi)
    _merge_range(nums, lo, mid, hi)


def merge_into(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """LeetCode 88. nums1 has m values then n empty slots; nums2 has n values.

    Merge BACKWARDS, from the largest, so nothing is overwritten before it is read.
    O(m + n) time, O(1) extra space -- the one merge that IS in place.
    """
    i, j, write = m - 1, n - 1, m + n - 1
    while j >= 0:                                  # nums2 must be exhausted
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1


def count_inversions(nums: list[int]) -> int:
    """How many pairs are out of order. The classic merge-sort follow-up.

    O(n log n) instead of the O(n^2) double loop: when a value is taken from the
    right half, every value still left in the left half forms an inversion with it.
    """

    def sort_and_count(values: list[int]) -> tuple[list[int], int]:
        if len(values) <= 1:
            return values, 0
        middle = len(values) // 2
        left, a = sort_and_count(values[:middle])
        right, b = sort_and_count(values[middle:])
        out: list[int] = []
        i = j = 0
        crossing = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
                crossing += len(left) - i      # the whole rest of left is greater
        out.extend(left[i:])
        out.extend(right[j:])
        return out, a + b + crossing

    return sort_and_count(nums)[1]


if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]

    print(merge([27, 38, 43], [3, 9, 82]))        # [3, 9, 27, 38, 43, 82]
    print(merge([1, 2], []))                      # [1, 2]
    print(merge_sort(data))                       # [3, 9, 10, 27, 38, 43, 82]
    print(merge_sort([]))                         # []
    print(merge_sort([5]))                        # [5]
    print(merge_sort_bottom_up(data))             # [3, 9, 10, 27, 38, 43, 82]

    in_place = list(data)
    merge_sort_in_place(in_place)
    print(in_place)                               # [3, 9, 10, 27, 38, 43, 82]

    a = [1, 2, 3, 0, 0, 0]
    merge_into(a, 3, [2, 5, 6], 3)
    print(a)                                      # [1, 2, 2, 3, 5, 6]

    print(count_inversions([2, 4, 1, 3, 5]))      # 3
    print(count_inversions([5, 4, 3, 2, 1]))      # 10  -- reversed: n(n-1)/2

    # stability, demonstrated
    pairs = [("b", 1), ("a", 2), ("c", 1)]
    print(merge_sort_pairs := sorted(pairs, key=lambda p: p[1]))
    # [('b', 1), ('c', 1), ('a', 2)]  -- b before c, as in the input
```

---

## 6. What it costs

### Time, counted level by level

This is the argument to say out loud, and it has exactly two parts.

**Part one: each level costs `n`.** At the top there is one merge of `n` values. At the next level
down there are two merges of `n/2` values each, which is `n` values in total. Below that, four merges
of `n/4`. The number of pieces doubles and the size of each halves, so every level moves exactly `n`
values.

```
 level 0:  1 merge  x  n     values   =  n
 level 1:  2 merges x  n/2   values   =  n
 level 2:  4 merges x  n/4   values   =  n
 level 3:  8 merges x  n/8   values   =  n
                                        ---
                              each level: n
```

**Part two: there are `log₂ n` levels.** Halving `n` down to 1 takes `log₂ n` steps.

```
 n = 8         8 -> 4 -> 2 -> 1              3 levels    = log2(8)
 n = 1,000     1000 -> 500 -> ... -> 1      10 levels    ~ log2(1000)
 n = 1,000,000                              20 levels    ~ log2(10^6)
```

Multiply: **`n` per level × `log₂ n` levels = `O(n log n)`.**

```
 n =     1,000  ->  1,000 x 10 =     10,000 operations
 n =   100,000  ->  100,000 x 17 =  1,700,000
 n = 1,000,000  ->  1,000,000 x 20 = 20,000,000
```

### Against yesterday

```
 n = 100,000

 insertion sort  : n(n-1)/2      = 4,999,950,000 operations   -- about 80 minutes in Python
 merge sort      : n x log2(n)   =     1,700,000              -- about 0.5 seconds

 ~2,900x fewer operations.
```

That ratio is the reason the whole phase exists. And note it *grows*: at a million elements the ratio
is about 25,000.

### The best case is the worst case

Merge sort always splits down to single elements and always merges every level, regardless of the
input.

```
 already sorted   : n log n
 reversed         : n log n
 random           : n log n
 all identical    : n log n
```

That predictability is a selling point. Quicksort tomorrow has a better constant factor but a
possible `O(n²)`; merge sort has no bad input at all. When an interviewer asks "which would you pick
for sorting data an attacker can choose", this is the answer.

### Space

```
 merge_sort (the simple version)  : O(n) for the output lists,
                                    plus O(log n) call frames for the recursion
 merge_sort_in_place              : O(n/2) for the buffer at the top level, still O(n)
 merge_into (LeetCode 88)         : O(1) -- but only because the room already exists
                                    at the end of nums1, and you merge backwards
```

Say `O(n)` and mean it. The recursion depth is only `log₂ n` — twenty frames at a million elements —
so the call stack is never the problem; the data copies are.

### The number of comparisons, exactly

The merge of two runs of total length `m` uses at most `m − 1` comparisons and at least `m/2`. That
gives a real range for the whole sort, and it is a good answer to "is it exactly n log n":

```
 n = 1,024 (2^10 exactly)

 at most  : n log2(n) - n + 1 = 10,240 - 1,024 + 1 = 9,217 comparisons
 at least : (n log2(n)) / 2   = 5,120 comparisons  (when the halves interleave badly)
```

---

## 7. The traps

### The real error: dividing with `/` instead of `//`

```python
def merge_sort_broken(nums):
    if len(nums) <= 1:
        return nums
    middle = len(nums) / 2          # <-- float division
    return merge(merge_sort_broken(nums[:middle]), merge_sort_broken(nums[middle:]))

print(merge_sort_broken([3, 1, 2]))
```

```
Traceback (most recent call last):
  File "day53.py", line 6, in <module>
    print(merge_sort_broken([3, 1, 2]))
          ~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "day53.py", line 5, in merge_sort_broken
    return merge(merge_sort_broken(nums[:middle]), merge_sort_broken(nums[middle:]))
                                   ~~~~^^^^^^^^^
TypeError: slice indices must be integers or None or have an __index__ method
```

In Python 3, `/` always produces a float, even for `4 / 2`. Positions into a list must be integers,
so the rule is: **any division that produces a position uses `//`.** The same trap bit binary search
on [day 043](../day-043-binary-search-without-bugs/README.md).

### The real error: a base case that is never reached

```python
def merge_sort_broken2(nums):
    if len(nums) == 1:              # <-- == instead of <=
        return nums
    middle = len(nums) // 2
    return merge(merge_sort_broken2(nums[:middle]), merge_sort_broken2(nums[middle:]))

print(merge_sort_broken2([]))
```

```
Traceback (most recent call last):
  File "day53.py", line 6, in <module>
    print(merge_sort_broken2([]))
          ~~~~~~~~~~~~~~~~~~^^^^
  File "day53.py", line 5, in merge_sort_broken2
    return merge(merge_sort_broken2(nums[:middle]), merge_sort_broken2(nums[middle:]))
  File "day53.py", line 5, in merge_sort_broken2
    return merge(merge_sort_broken2(nums[:middle]), merge_sort_broken2(nums[middle:]))
  File "day53.py", line 5, in merge_sort_broken2
    return merge(merge_sort_broken2(nums[:middle]), merge_sort_broken2(nums[middle:]))
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

An empty list has `middle = 0`, so `nums[:0]` is `[]` and `nums[0:]` is `[]` — the same size, forever.
This is the general recursion failure and you will meet it again on
[day 089](../day-089-recursion-that-terminates/README.md): **the base case must cover every input
that cannot shrink further, not just the one you had in mind.** `<= 1` covers both 0 and 1.

Python's default recursion limit is 1,000 frames, which for merge sort would mean a list of about
`2¹⁰⁰⁰` elements — so if you see `RecursionError` from a merge sort, it is a bug, never a size
problem.

### The near-miss: forgetting the leftovers

```python
def merge_broken(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out                            # <-- no extend

print(merge_broken([1, 2, 9], [3, 4]))
```

```
[1, 2, 3, 4]
```

The `9` is gone, and nothing raised. The loop condition needs **both** lists to be non-empty, so it
exits the moment either one is spent — and whatever is left in the other is simply dropped. This is
the commonest merge bug and it produces a shorter list that still looks plausible. **Check the length
of your output against the sum of the inputs**; it is a one-line assertion that catches it instantly.

### The near-miss: `<` instead of `<=` silently loses stability

```python
if left[i] < right[j]:        # <-- was <=
```

With `<`, an equal value on the right is taken first, so two equal elements swap order. The numbers
still come out sorted. Sort a list of `(name, score)` by score, and the names inside each score come
out in an order you cannot explain. As on [day 052](../day-052-quadratic-sorts/README.md), stability
is one character and it never announces itself.

### The trap: merging forwards when the output shares memory with the input

LeetCode 88 gives you `nums1 = [1, 2, 3, 0, 0, 0]` and asks you to merge `nums2 = [2, 5, 6]` into it
in place. The obvious forward merge destroys the data:

```python
def merge_into_broken(nums1, m, nums2, n):
    i = j = k = 0
    while j < n:
        if i < m and nums1[i] <= nums2[j]:
            nums1[k] = nums1[i]; i += 1
        else:
            nums1[k] = nums2[j]; j += 1
        k += 1

a = [1, 2, 3, 0, 0, 0]
merge_into_broken(a, 3, [2, 5, 6], 3)
print(a)
```

```
[1, 2, 2, 3, 5, 6]
```

That one happens to be right — which is exactly why it is dangerous. Try an input where a write
lands on an unread value:

```python
a = [4, 5, 6, 0, 0, 0]
merge_into_broken(a, 3, [1, 2, 3], 3)
print(a)
```

```
[1, 2, 3, 1, 2, 3]
```

Writing `1` into position 0 destroyed the `4` that had not been read yet. The fix is to merge
**backwards** from the largest value, filling the empty space at the end first, so a write never
lands anywhere still unread. That is `merge_into` in §5, and it is a favourite interview question
precisely because the forward version passes the sample case.

### The trap: claiming merge sort is in place

It is not, and the interviewer will check. The simple version allocates a new list at every level.
The "in-place" version still copies half the range into a buffer at each merge. There is a genuine
in-place merge algorithm, but it is `O(n log² n)` or needs block-swapping tricks that nobody writes
from memory. **The honest answer is: `O(n)` extra space, and if you need in-place with `O(n log n)`
guaranteed, use heapsort.**

---

## 8. In the interview

### How it gets asked

- *"Write merge sort."* — asked directly, extremely often, usually as the first `O(n log n)` sort
  they check you can produce.
- *"Why is it O(n log n)?"* — the real question, and the answer must be "n work per level, log n
  levels", not "because it divides in half".
- *"Merge two sorted arrays."* — LeetCode 88 and 21. The merge step alone, and the in-place version
  needs the backwards trick.
- *"Merge sort or quicksort — which would you use?"* — expect this tomorrow too. The answer is about
  guaranteed worst case, stability and memory.
- *"Count the inversions in this array."* — the standard follow-up that only merge sort answers in
  `n log n`.
- *"Sort a linked list."* — LeetCode 148. Merge sort is the right answer, because merging linked
  lists needs no extra space at all, and quicksort needs random access it does not have.

### What to say out loud, in the first ninety seconds

1. **Say the sentence version before writing anything.** *"A list of one is already sorted. Otherwise
   sort the left half, sort the right half, and merge the two sorted halves. The merge is the part
   that does the work."*
2. **Write the merge first, and say why it is cheap.** *"Merging two sorted lists is O(n) because I
   only ever compare the two fronts — the smaller of them is the smallest value remaining anywhere,
   so there is no searching."*
3. **Name the base case and the progress.** *"Base case is length 0 or 1. Each call gets a strictly
   smaller half, so it terminates."*
4. **Give the complexity as two facts.** *"Each level of merging touches all n elements, and there
   are log₂ n levels of halving, so n log n. And it is the same on every input — there is no bad
   case."*
5. **Volunteer the cost.** *"It's O(n) extra space, unlike the quadratic sorts, and it is stable
   because the merge takes from the left when the fronts are equal."*

### The follow-ups

**"Why is it O(n log n)? Explain it without saying 'because it divides in half'."**
Because there are two separate quantities and the answer is their product. The first is the cost of
one level of merging. At the top there is a single merge of all n elements. One level down there are
two merges of n/2 each, which is still n elements moved in total. Below that, four merges of n/4 —
again n. The number of pieces doubles at each level and the size of each piece halves, so those two
cancel and every level costs exactly n. The second quantity is how many levels there are, and that is
how many times you can halve n before reaching 1, which is log₂ n — twenty for a million elements.
Multiply them: n per level times log n levels is n log n. The reason "it divides in half" is not
sufficient on its own is that binary search also divides in half and is O(log n), not O(n log n) —
the difference is that binary search throws one half away and recurses into a single side, so it does
constant work per level, whereas merge sort recurses into both halves and does linear work per level.
The shape of the recursion, not the halving, is what decides it.

**"It uses O(n) extra space. Can you avoid that?"**
Not really, and I would rather say so than pretend. The merge fundamentally needs somewhere to write
the combined result, because the two sorted runs sit next to each other in the array and writing the
output over them would destroy values that have not been read yet. The best I can do in the standard
implementation is copy only the *left* half into a buffer — the right half never needs copying,
because anything still unread in it lies at or beyond the write position, so it cannot be clobbered.
That halves the constant but it is still O(n). There are genuine in-place merge algorithms using
block rotations, but they are O(n log² n) or have constants bad enough that nobody uses them, and I
would not attempt one from memory in an interview. If the requirement is truly O(n log n) time with
O(1) space, the right answer is heapsort. There are two important exceptions in the other direction.
Sorting a linked list with merge sort needs no extra space at all beyond the recursion, because
merging two linked lists is pure relinking — that is why merge sort is the standard answer to
LeetCode 148. And merging into an array that already has room at the end, like LeetCode 88, is O(1)
extra space if you merge backwards from the largest value, so nothing is written over an unread slot.

**"Merge sort or quicksort?"**
Quicksort by default for arrays in memory, merge sort when one of three things is true. Quicksort
wins on the constant factor: it sorts in place, so it touches less memory and gets far better cache
behaviour, and in practice it runs about two to three times faster than merge sort on the same array
even though both are n log n. What you give up is the guarantee — quicksort's worst case is O(n²),
and although a randomised pivot makes that astronomically unlikely, "unlikely" is not "impossible",
and with a deterministic pivot an adversary who can choose the input can force it. So I choose merge
sort when the worst case actually matters — data that comes from outside and could be chosen against
me, or a latency budget where a rare slow case is a broken promise rather than an average. Second,
when I need stability: merge sort is stable and quicksort is not, and if I am sorting records by a
second key after a first, that is not optional. Third, when the data does not fit in memory or is a
linked list. External sorting is merge sort — sort chunks that fit in RAM, write them out, then merge
the runs — and that is exactly what Postgres or MySQL does for a large ORDER BY that spills to disk.
For linked lists, merge sort needs no random access and no extra space, and quicksort needs both.

### A model answer

> "Merge sort is divide and conquer. A list of zero or one elements is already sorted — that's the
> base case. Otherwise I split the list in half, sort each half by the same method, and then merge the
> two sorted halves into one.
>
> The merge is where all the work happens, so I'd write that first:
>
> ```python
> def merge(left: list[int], right: list[int]) -> list[int]:
>     out, i, j = [], 0, 0
>     while i < len(left) and j < len(right):
>         if left[i] <= right[j]:
>             out.append(left[i]); i += 1
>         else:
>             out.append(right[j]); j += 1
>     out.extend(left[i:])
>     out.extend(right[j:])
>     return out
>
> def merge_sort(nums: list[int]) -> list[int]:
>     if len(nums) <= 1:
>         return nums
>     middle = len(nums) // 2
>     return merge(merge_sort(nums[:middle]), merge_sort(nums[middle:]))
> ```
>
> Two details in the merge I'd point at. Those two `extend` lines are not optional — the loop stops as
> soon as *either* list is empty, so whatever remains in the other has to be copied across, and
> forgetting that silently returns a shorter list. And the comparison is `<=` rather than `<`, which
> is what makes the sort stable: when the two fronts are equal I take from the left, so equal elements
> keep their original order.
>
> On the complexity — it's O(n log n) and the argument is two facts multiplied. Each level of merging
> touches every element exactly once: one merge of n at the top, two merges of n/2 below it, four of
> n/4 below that, so n per level regardless of how many pieces there are. And there are log₂ n levels,
> because that's how many times you can halve n down to 1 — twenty levels at a million elements. n per
> level times log n levels is n log n. That's also why 'it divides in half' isn't the full answer:
> binary search divides in half too and is O(log n), because it discards one side instead of
> recursing into both.
>
> The cost is O(n) extra space for the merge buffers, plus O(log n) stack frames, and that's the main
> thing merge sort gives up against quicksort. What it buys is a guaranteed worst case — every input
> is n log n, there's no bad case — and stability. So I'd reach for it when the input could be chosen
> adversarially, when I need stability, or when the data doesn't fit in memory, which is exactly the
> external merge sort a database runs for a large ORDER BY."

---

## 9. Recall card

- **The sentence:** *a list of 0 or 1 is sorted; otherwise sort both halves and **merge** them.* The
  merge is the engine — compare only the two fronts, take the smaller, and when one side empties copy
  the rest across with no comparisons. Merging is **O(n)** because nothing is ever searched for.
- **Why O(n log n), in two facts multiplied:** every level of merging moves all **n** elements (1×n,
  then 2×n/2, then 4×n/4 …), and there are **log₂ n** levels of halving. Not "because it halves" —
  binary search halves too and is O(log n), because it discards one side.
- **No bad input.** Best = average = worst = n log n, and it is **stable** because the merge uses
  `<=` and takes from the left on a tie. Quicksort is faster in practice but can hit O(n²) and is not
  stable.
- **The cost is O(n) extra space** — the merge cannot write over its own inputs. Copy only the *left*
  half into the buffer; the right half is always at or beyond the write position. Two exceptions:
  linked lists (pure relinking, O(1)) and LeetCode 88 (merge **backwards** into the free tail).
- **Three traps:** `//` not `/` for the middle (`TypeError: slice indices must be integers`) · base
  case `<= 1` not `== 1` or an empty half recurses forever (`RecursionError`) · the two `extend`
  lines, or the tail is silently dropped. And the free follow-up: **count inversions** in n log n by
  adding `len(left) - i` whenever you take from the right.
