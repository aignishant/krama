---
day: 44
track: dsa
title: "First and last occurrence"
phase: "Binary search"
status: written
---

# Day 044 · DSA — First and last occurrence

**After today you can:** You can find the boundaries of a repeated value in O(log n).

**The interviewer asks it as:** *Find the first and last position of a target in a sorted array.*

---

## 1. What this is, and why they ask it

A sorted array can hold the same value many times, and those copies always sit together in one
unbroken run. Today you find both ends of that run — the index of the first copy and the index of
the last — in `O(log n)`, using yesterday's template twice with one character different between the
two calls. Everything else about the problem is a consequence of that.

They ask it because it is the shortest problem that punishes the obvious answer. Almost every
candidate's instinct is to binary search for any copy and then walk outward to the edges, and that
instinct is correct on the test cases and catastrophic on the input the interviewer is actually
holding: an array of a million identical values, where the walk is `O(n)` and undoes the whole point
of the search. LeetCode 34 is a top-thirty interview question at product companies, and it is asked
precisely to see whether you notice. It also unlocks a family — counting occurrences, finding the
range of a value, and every "how many things satisfy this" question that reduces to two boundaries
subtracted.

---

## 2. The story

Reshma needs a plain white shirt for her brother, and the shop on the second floor of the mall has
one long rail of them against the back wall, maybe four hundred shirts, all the same design.

They are hung by size, smallest at the left, largest at the right. The tag is a small card sewn into
the collar and you have to lift the shoulder to read it. Her brother takes a 38.

The first time she did this she started at the left end and flicked along, shirt by shirt, lifting
collars. It took eleven minutes and her arms ached, and the 38s did not begin until nearly the middle
of the rail.

Now she does something else, and she does it twice.

The first hunt is for the place the 38s begin. She pushes into the middle of the rail and lifts a
collar: 42. Too big, so every shirt from here rightwards is 42 or more and none of them is what she
wants. She moves left, into the middle of what is left: 34. Too small — so this one is not the start
either, and neither is anything to its left. She keeps closing in, four or five lifts, until the two
edges of her search meet, and that is where the 38s start.

The second hunt is for the place they stop, and it is the same hunt with the question changed. Not
"where does 38 begin" but "where does anything bigger than 38 begin". Middle, lift, too small, move
right. Middle, lift, 40 — bigger than 38, so the 38s have ended at or before here. Four or five lifts
again, and she has the far edge.

Two hunts, about ten collars lifted, and she knows exactly which stretch of the rail is hers. She
takes the four shirts in it to the light by the window and picks one.

She learnt to do it as two hunts on the day the shop had a delivery and there were nearly two hundred
38s hanging in a row. She had found one 38 quickly enough, in the middle of the run, and then walked
left to find where it started — and walking left through a hundred and something shirts took as long
as flicking the whole rail had. Finding one of them is easy. Finding the *edge* is the job.

---

## 3. The idea in plain English

Reshma's rail is the sorted array, the size on the tag is the value, and her two hunts are two calls
to [yesterday's template](../day-043-binary-search-without-bugs/README.md). The delivery day is the
input that kills the shortcut.

### The run is unbroken

In a sorted array, equal values are adjacent. There is no way to have a 4 at index 1 and another 4 at
index 6 with a 7 in between, because that would break the ordering. So the copies of a value form one
**run**: a contiguous stretch, described completely by its two ends.

```python
nums = [2, 4, 4, 4, 7, 9, 11]
```

The run of 4s is indices 1 to 3. Two numbers describe it. That is the entire problem.

### Two boundaries, one template

Yesterday's template finds the **first index where a yes-or-no question becomes true**, and it needs
the question to be monotone. Here are the two questions:

```
question A:  nums[i] >= 4      no, YES, YES, YES, YES, YES, YES     first True at 1
question B:  nums[i] >  4      no, no,  no,  no,  YES, YES, YES     first True at 4
```

- The first `4` sits at the first index where `nums[i] >= 4`. That is the **lower bound**, and it is
  index 1.
- The **upper bound** is the first index where `nums[i] > 4`, which is index 4 — one past the run.
  So the last `4` is at `upper_bound - 1` = 3.

Both questions are monotone on a sorted array, so both are one call to the same six lines.

### The check that must not be skipped

The lower bound always returns a position, even when the target is absent. Search for 5 in that
array and you get 4 — the position where 5 *would* go. That index is in range and holds a 7, not a 5.

So the answer is only valid if:

```python
first < len(nums) and nums[first] == target
```

Both halves matter. `first < len(nums)` guards the "target bigger than everything" case, where the
lower bound is `len(nums)` and indexing it raises. `nums[first] == target` guards the "target absent
but in range" case, which raises nothing at all and quietly returns a wrong answer. The `and`
short-circuits, so the order is load-bearing.

If the check fails, return `[-1, -1]`. And note: you only need to run it once. If the lower bound is
not a real match, there are no copies at all, so the upper bound cannot rescue it.

### What falls out for free

```
count of target      = upper_bound - lower_bound
last occurrence      = upper_bound - 1
does target exist    = lower_bound is valid
how many are < x     = lower_bound(x)
how many are <= x    = upper_bound(x)
how many are in [a,b] = upper_bound(b) - lower_bound(a)
```

That last one is worth stopping on. "How many values lie between 10 and 20 inclusive" is two binary
searches and a subtraction — `O(log n)` — where the obvious answer is a scan. This is the shape
behind a large number of "count the things that satisfy a range condition" interview questions.

### Why not find-then-walk

The tempting version: binary search for any copy, then walk left while the value is the same, then
walk right. It is correct. It is also `O(log n + k)` where `k` is the number of copies, and `k` can
be `n`. On `[8] * 1_000_000` searching for 8, the search takes twenty comparisons and the walk takes
a million. **The cost of the walk is exactly the thing the problem is about**, which is why the
interviewer chose an array with duplicates in it.

---

## 4. The picture

The two questions, drawn on the same array:

```
 index        0     1     2     3     4     5     6
            +-----+-----+-----+-----+-----+-----+-----+
 nums       |  2  |  4  |  4  |  4  |  7  |  9  | 11  |
            +-----+-----+-----+-----+-----+-----+-----+
 >= 4 ?     | no  | YES | YES | YES | YES | YES | YES |
 >  4 ?     | no  | no  | no  | no  | YES | YES | YES |
                    ^                 ^
             lower_bound = 1    upper_bound = 4

                    |<--- the run --->|
                     first = 1   last = upper - 1 = 3
                     count = 4 - 1 = 3
```

**What to notice:** the two rows are the same array asked two different questions, and both rows are
monotone. Nothing else about the array matters.

The half-open range as a picture of ownership:

```
        [ lower_bound , upper_bound )
              1              4
        indices 1, 2, 3 -- exactly the copies of 4

 the run is a half-open slice. nums[1:4] is [4, 4, 4].
 That is not a coincidence: Python slicing uses the same convention.
```

**What to notice:** `nums[lower:upper]` *is* the run. If you can write the slice, you have the
answer, and the `- 1` for "last index" is a display detail rather than part of the reasoning.

And the absent case, searching for 5:

```
 lower_bound(5) = 4     nums[4] = 7, not 5    -> no copies
 upper_bound(5) = 4     count = 4 - 4 = 0     -> the subtraction agrees, with no special case
```

**What to notice:** when the target is absent both bounds land on the same index, so the count is
zero automatically. The `[-1, -1]` requirement is the problem's output format, not a case the
algorithm has to think about.

---

## 5. The code, built step by step

### The template, once more

```python
def _first_true(lo: int, hi: int, question) -> int:
    while lo < hi:
        mid = (lo + hi) // 2
        if question(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Unchanged from [day 043](../day-043-binary-search-without-bugs/README.md). It will stay unchanged for
the rest of the phase.

### The two bounds

```python
def lower_bound(nums: list[int], target: int) -> int:
    return _first_true(0, len(nums), lambda i: nums[i] >= target)

def upper_bound(nums: list[int], target: int) -> int:
    return _first_true(0, len(nums), lambda i: nums[i] > target)
```

One character apart. Say that out loud in the interview — it is the sentence that shows you
understand the template rather than having memorised two functions.

### The validity check

```python
first = lower_bound(nums, target)
if first == len(nums) or nums[first] != target:
    return [-1, -1]
```

Written as an early return, which is easier to read than nesting the happy path inside an `if`. Note
`first == len(nums)` comes first, so `nums[first]` is never evaluated on an out-of-range index.

### The last index

```python
last = upper_bound(nums, target) - 1
```

Only reached when at least one copy exists, so the `- 1` cannot produce `-1` by accident. That
ordering — check first, then compute last — is what makes the minus one safe.

### The complete solution

```python
from bisect import bisect_left, bisect_right


def _first_true(lo: int, hi: int, question) -> int:
    """Smallest i in [lo, hi) where question(i) is True, or hi if none is."""
    while lo < hi:
        mid = (lo + hi) // 2
        if question(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def lower_bound(nums: list[int], target: int) -> int:
    """First index with nums[i] >= target; len(nums) if every value is smaller."""
    return _first_true(0, len(nums), lambda i: nums[i] >= target)


def upper_bound(nums: list[int], target: int) -> int:
    """First index with nums[i] > target; len(nums) if no value is bigger."""
    return _first_true(0, len(nums), lambda i: nums[i] > target)


def search_range(nums: list[int], target: int) -> list[int]:
    """LeetCode 34. First and last index of target, or [-1, -1].

    Two independent binary searches: O(log n) even when every value is the target.
    """
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]                       # no copies at all; upper cannot help
    last = upper_bound(nums, target) - 1      # safe: at least one copy exists
    return [first, last]


def count_of(nums: list[int], target: int) -> int:
    """How many copies. Zero falls out with no special case."""
    return upper_bound(nums, target) - lower_bound(nums, target)


def count_in_range(nums: list[int], low: int, high: int) -> int:
    """How many values lie in [low, high] inclusive. Two searches, one subtraction."""
    return upper_bound(nums, high) - lower_bound(nums, low)


if __name__ == "__main__":
    nums = [2, 4, 4, 4, 7, 9, 11]

    print(search_range(nums, 4))          # [1, 3]
    print(search_range(nums, 2))          # [0, 0]   <- run of one, at the very start
    print(search_range(nums, 11))         # [6, 6]   <- run of one, at the very end
    print(search_range(nums, 5))          # [-1, -1] <- absent, inside the range
    print(search_range(nums, 1))          # [-1, -1] <- below everything
    print(search_range(nums, 99))         # [-1, -1] <- above everything, lower = len(nums)
    print(search_range([], 4))            # [-1, -1] <- empty input
    print(search_range([4, 4, 4], 4))     # [0, 2]   <- every element is the target

    print(count_of(nums, 4), count_of(nums, 5))        # 3 0
    print(count_in_range(nums, 4, 9))                  # 5  -> 4,4,4,7,9

    # The standard library is these two functions.
    print(bisect_left(nums, 4), bisect_right(nums, 4)) # 1 4
```

Run it. The three inputs that matter are the last three of the `search_range` block: an empty list, a
target above everything, and an array that is nothing but the target. A version that passes those
three is almost certainly right.

### The other formulation, and why it is worth knowing

Some interviewers want to see the three-way comparison rather than the boundary template. The trick
there is **record and keep going** instead of returning on a match:

```python
def first_occurrence_three_way(nums: list[int], target: int) -> int:
    low, high, answer = 0, len(nums) - 1, -1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            answer = mid                 # a match, but maybe not the leftmost
            high = mid - 1               # so keep looking left
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return answer
```

The one line that carries the idea is `answer = mid` followed by `high = mid - 1`: on a match you
refuse to stop. Mirror it — `low = mid + 1` — for the last occurrence. It is the same `O(log n)`.
Know it, because it gets asked; prefer the boundary template, because it is one function instead of
two and it does not need an `answer` variable that starts as a lie.

### In an interview you would use this

```python
def search_range_lib(nums: list[int], target: int) -> list[int]:
    left = bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    return [left, bisect_right(nums, target) - 1]
```

Two library calls and the same validity check. Say "in production this is `bisect_left` and
`bisect_right`" after you have written the loop by hand — it shows you know the loop is a teaching
exercise, not a preference.

---

## 6. What it costs

### Time

Two independent binary searches over the same array:

```
lower_bound:  log2(n) passes
upper_bound:  log2(n) passes
              -----------------
total:        2 x log2(n) = O(log n)
```

Constants do not change the class, and it is worth saying the number rather than the letter:

```
n = 1,000,000   ->  20 + 20 = 40 comparisons
n = 1,000,000,000 -> 30 + 30 = 60 comparisons
```

Sixty comparisons to find both edges of a run inside a billion elements.

### Against the shortcut

This is the comparison the whole problem exists for:

```
array = [8] * 1,000,000, target = 8

find-then-walk:  20 comparisons to land in the middle
                 + ~500,000 steps left  + ~500,000 steps right
                 = ~1,000,020 operations           -> O(log n + k), k = n here

two bounds:      20 + 20 = 40 operations            -> O(log n)

25,000 times fewer operations, on the input the interviewer will hand you.
```

The general statement: **find-then-walk is `O(log n + k)` where `k` is the number of copies, and `k`
is unbounded.** Say that sentence rather than "the walk is slow" — the variable is the point.

### Space

```
lo, hi, mid, first, last: five integers, whatever n is    -> O(1) extra space
```

No allocation, and the two searches do not interact, so nothing accumulates.

### The build cost, when the array is not already sorted

Same warning as [day 042](../day-042-binary-search-idea/README.md). If you have to sort first, that
is `O(n log n)` and dominates everything here. Two binary searches on an unsorted array are two wrong
answers, delivered quickly.

---

## 7. The traps

### The near-miss: find-then-walk

```python
def walker(nums, target):
    i = lower_bound(nums, target)
    if i == len(nums) or nums[i] != target:
        return [-1, -1]
    j = i
    while j + 1 < len(nums) and nums[j + 1] == target:   # <-- the walk
        j += 1
    return [i, j]

import time
big = [8] * 1_000_000
start = time.perf_counter(); walker(big, 8); print(f"{time.perf_counter() - start:.4f}s")
start = time.perf_counter(); search_range(big, 8); print(f"{time.perf_counter() - start:.6f}s")
```

```
0.0621s
0.000009s
```

Correct answers, both of them. One is roughly seven thousand times slower, and it is the one most
candidates write. The interviewer does not have to say anything; they just ask "what's the complexity
of that?" and wait.

### The real error: skipping the range guard

```python
nums = [2, 4, 4, 4, 7]
first = lower_bound(nums, 99)
print(first)
print(nums[first] == 99)
```

```
5
Traceback (most recent call last):
  File "day44.py", line 4, in <module>
    print(nums[first] == 99)
          ~~~~^^^^^^^
IndexError: list index out of range
```

The lower bound returned 5, which is `len(nums)` — the honest "it would go at the end" answer — and
indexing it raises. Always `first < len(nums)` **before** `nums[first]`, in that order.

### The near-miss that raises nothing: skipping the equality check

```python
def broken(nums, target):
    first = lower_bound(nums, target)
    last = upper_bound(nums, target) - 1
    return [first, last]

print(broken([2, 4, 4, 4, 7], 5))     # [4, 3]
print(broken([2, 4, 4, 4, 7], 3))     # [1, 0]
```

```
[4, 3]
[1, 0]
```

No exception, and the numbers look like indices. They are nonsense: `last` is less than `first`,
because the run is empty. That inversion is actually the tell — **when the target is absent, both
bounds are equal, so `last` comes out one less than `first`.** You could test for it, but the
equality check is clearer and says what you mean.

### The trap: `- 1` computed before the check

```python
first = lower_bound(nums, target)
last = upper_bound(nums, target) - 1
if first == len(nums) or nums[first] != target:
    return [-1, -1]
```

Correct output, wrong shape — and on a large input it does a second binary search that it then throws
away. Worse, in a variant where `upper_bound` is expensive (which it will be from
[day 046](../day-046-binary-search-on-the-answer/README.md), where a "comparison" means scanning the
whole array), that wasted call doubles the runtime. Check, then compute.

### The trap: assuming a sorted-by-something-else array

```python
people = [("Asha", 31), ("Bala", 24), ("Chetan", 45)]     # sorted by name
```

The array is sorted, so binary search is available — but only on the name. Searching it by age with
`p[1] >= 30` gives a meaningless answer, because that question is not monotone here. **The monotone
question must match the ordering the array actually has.** Ask which key the array is sorted on; it
is the same ten-second question as "is it sorted?", one level deeper.

---

## 8. In the interview

### How it gets asked

- *"Find the first and last position of a target in a sorted array. Return [-1, -1] if it isn't
  there."* — LeetCode 34, word for word.
- *"How many times does x appear in this sorted array? Better than linear, please."* — the same two
  searches, subtracted.
- *"Here's a sorted list of timestamps. How many events happened between 9am and 5pm?"* — the range
  count, and the most realistic phrasing of the three.
- As a **follow-up to LeetCode 704**: they ask plain binary search first, then say "now the array has
  duplicates and I want the leftmost". That is the whole of today, and it arrives ninety seconds
  after you thought you were finished.

### What to say out loud, in the first ninety seconds

1. **Name the structure.** *"Sorted array, so equal values form one contiguous run. The answer is
   completely described by two indices, so I'll find them independently."*
2. **Say the two questions.** *"The first copy is the first index where `nums[i] >= target` — the
   lower bound. The last copy is one before the first index where `nums[i] > target` — the upper
   bound minus one. Same template, one character different."*
3. **Pre-empt the shortcut, out loud.** *"I'm deliberately not finding any match and walking outward.
   That's O(log n + k) and k can be the whole array — on a million identical values it's a linear
   scan."*
4. **State the guard.** *"The lower bound always returns a position, even when the target is absent,
   so I check `first < len(nums) and nums[first] == target` before trusting it. If that fails, no
   copies exist and I return [-1, -1] without the second search."*
5. **Give the cost.** *"Two binary searches, so O(log n) — about forty comparisons at a million
   elements — and O(1) space."*

### The follow-ups

**"Can you do it in one pass instead of two searches?"**
Not meaningfully, and I'd explain why rather than trying. The two boundaries are answers to two
different monotone questions, and a single binary search converges on one boundary — the moment it
commits to going left it has stopped being able to find the right-hand edge. There is a version that
shares the first few levels of the search: run one search until the range splits around the target,
then run a lower bound on the left part and an upper bound on the right part. It saves a handful of
comparisons in the average case, it is strictly more code, it has more edge cases, and it is still
O(log n) — so it is a worse answer to the same question. What I would say is that two searches at 2
log n is already optimal in the asymptotic sense, since you cannot identify a boundary in fewer than
log n comparisons and there are two boundaries. If they are asking because they want fewer *array
accesses* specifically, I'd mention that `bisect_left` and `bisect_right` in C are so much faster per
comparison than anything hand-written that the constant factor conversation stops being interesting.

**"The array is huge and lives on disk, so every comparison is a page read. Does your answer
change?"**
The shape does not, but the accounting does, and this is a good question because it moves the cost
from comparisons to reads. Two searches at thirty reads each is sixty page reads on a billion
elements, and a page read is about 0.1 ms from
[day 031](../day-031-fixed-window/README.md), so six milliseconds — against a sequential scan of a
billion elements, which is hours. So binary search still wins by an enormous margin. But I would say
two things. First, binary search on disk has terrible locality: each read lands in an unrelated part
of the file, so none of the operating system's read-ahead helps, and that is exactly the reason real
databases use B-trees rather than binary search over a sorted file — a B-tree node is one page holding
hundreds of keys, so a fanout of 500 covers ten million rows in three reads instead of twenty-four.
Second, if the two searches are close together in the file, the second one will hit pages the first
one already warmed, so the real cost of the second search is often much less than thirty reads.

**"Now the values aren't numbers — they're records, and 'equal' means equal on one field. Anything
change?"**
The template does not care what is being compared; it needs one monotone question and nothing else.
So if the records are sorted by the same field I'm searching on, the question becomes
`records[i].field >= target` and everything works unchanged. The two things I'd check before writing
it are: is the array sorted by *that* field, because an array sorted by name gives me nothing when I
search by age, and is the field's ordering total — no `None`s mixed in, no comparison that raises. In
Python I'd also mention that `bisect` has a `key` argument since 3.10, so
`bisect_left(records, target, key=lambda r: r.field)` does this natively without building a
projection list. The last thing worth flagging is that the *result* is a range of records with equal
keys, and within that range the order is whatever the sort produced — so if the caller needs a
specific one of them, that is a stability question about the sort, which is
[day 057](../day-057-stability-and-pythons-sort/README.md), not about the search.

### A model answer

> "Sorted array, so the copies of the target are contiguous — one unbroken run — and two indices
> describe it completely. I'll find each one with its own binary search rather than finding a match
> and walking, and let me say why up front: walking outward from a match is O(log n + k) where k is
> the number of copies, and on an array of a million identical values that's a linear scan. The
> duplicates are the whole point of the question.
>
> Both searches are the same boundary template with one character different. The first copy is the
> first index where `nums[i] >= target`. The last copy is one before the first index where
> `nums[i] > target`.
>
> ```python
> def search_range(nums: list[int], target: int) -> list[int]:
>     first = lower_bound(nums, target)
>     if first == len(nums) or nums[first] != target:
>         return [-1, -1]
>     return [first, upper_bound(nums, target) - 1]
> ```
>
> The guard matters and it has two halves. The lower bound always returns a *position*, even when the
> target isn't present — for a target bigger than everything it returns len(nums), and indexing that
> raises an IndexError. And for a target that's absent but in range it returns a perfectly valid index
> holding some other value, which raises nothing and quietly gives a wrong answer. So I check the
> bound first and the equality second, in that order, and I do it before the second search — if
> there's no first copy there's no last one either.
>
> Cost is two binary searches, so O(log n) — about forty comparisons at a million elements — and O(1)
> space.
>
> Two things I get for free and would mention. The number of copies is upper bound minus lower bound,
> with no third pass and no special case for zero, because when the target is absent both bounds land
> on the same index. And 'how many values are between a and b inclusive' is upper bound of b minus
> lower bound of a — which is the shape behind a lot of range-counting questions that look harder than
> they are. In production these two are `bisect_left` and `bisect_right`."

---

## 9. Recall card

- **Equal values in a sorted array form one contiguous run** — two indices describe it, so run
  [yesterday's template](../day-043-binary-search-without-bugs/README.md) twice, one character apart.
- **first = lower_bound (`>= target`); last = upper_bound (`> target`) − 1.** And
  `nums[lower:upper]` *is* the run — the slice, not the minus one, is the idea.
- **The guard is two halves, in order:** `first < len(nums)` (or it raises) **and**
  `nums[first] == target` (or it lies). Check before computing `last`.
- **Never find-then-walk.** That is O(log n + k) with k unbounded — a million identical values makes
  it a linear scan, and that is the input you will be given.
- **Free from the same two calls:** count = upper − lower (zero needs no special case); values in
  [a, b] = upper(b) − lower(a). `bisect_left` / `bisect_right` in production.
