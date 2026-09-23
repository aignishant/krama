---
day: 45
track: dsa
title: "Search in a rotated sorted array"
phase: "Binary search"
status: written
---

# Day 045 · DSA — Search in a rotated sorted array

**After today you can:** You can binary search data that is sorted, but not from the start.

**The interviewer asks it as:** *Search a rotated sorted array in O(log n).*

---

## 1. What this is, and why they ask it

A **rotated sorted array** is a sorted array that has been cut at one point and had its front piece
moved to the back. `[1, 3, 5, 7, 9, 11]` rotated at index 4 becomes `[9, 11, 1, 3, 5, 7]`. It is not
sorted, so [day 042](../day-042-binary-search-idea/README.md)'s test — *is the middle smaller than the
target?* — no longer tells you which way to go. But one fact survives the rotation and is enough:
**at least one of the two halves is still properly sorted**, and you can find out which in one
comparison.

They ask it constantly. It is a top-five interview question at product companies, and it exists to
separate two kinds of candidate: the one who memorised binary search, and the one who understands
what binary search actually needs. The template does not need a sorted array; it needs a way to
discard half. That is a different requirement, and this problem is the first place the difference
bites. Expect it as the medium after a warm-up, expect the follow-up about duplicates, and expect to
be asked why your answer is still `O(log n)` when the array is not sorted.

---

## 2. The story

Prithvi is a volunteer at his school's annual day, and his job for the evening is showing parents to
their chairs.

The parents' block is four hundred plastic chairs in one long row along the side of the ground,
brought out that afternoon from the store room behind the stage. Every chair has a number stuck on
the back in white tape, 1 to 400.

The boys who laid them out worked from a stack, and the stack had been put away the wrong way round
the year before. So the row does not start at 1. It starts at 240. From the left end it goes 240,
241, 242, and climbs steadily all the way to 400 — and then, with no warning at all, the next chair
says 1, and from there it climbs again, 2, 3, 4, up to 239 at the far right end.

Nobody is going to move four hundred chairs at six in the evening.

A man arrives with a ticket for chair 88 and Prithvi walks him down the row.

He does not read every number. He walks to roughly the middle and reads the chair there: 330. Then he
does the thing that makes this work. He already knows what the chair at the left end says, because he
checked it when he started — 240. So he asks himself one question: *from the left end to where I am
standing, do the numbers only climb?* The left end says 240, here it says 330, 240 is smaller than
330, and there is no way for the numbers to have jumped down and come back up in between. So yes,
that whole left stretch runs 240 up to 330, in order, with nothing missing.

Now the easy part. Is 88 between 240 and 330? It is not. So 88 cannot be anywhere in that left
stretch, and he can forget all of it. He walks right.

He does it again. Middle of what is left, chair 20. Left mark now says 331, and 331 is bigger than 20,
so *that* stretch is the one with the jump in it — no use to him. But the other side, from here to the
right end, must then be in order: 20 climbing up to 239. Is 88 between 20 and 239? Yes. Go right.

Four or five walks, and he is standing at chair 88. The man sits down and the show starts.

---

## 3. The idea in plain English

Prithvi's row is the rotated array. The one place where 400 is followed by 1 is the **pivot**. And
his question — *does this stretch only climb?* — is the single comparison that replaces the sorted
test.

### What rotation does, exactly

Take a sorted array and move the front `k` elements to the back:

```python
sorted_arr  = [1, 3, 5, 7, 9, 11]
rotated     = [9, 11, 1, 3, 5, 7]     # rotated by 4, or equivalently cut before 9
```

The result has one **break point** — one place where a value is followed by a smaller value.
`11` followed by `1`. Everywhere else the values climb. That is the definition, and everything today
follows from it.

Two edge cases worth naming now, because they are what interviewers test:

- Rotated by 0 (or by `n`) gives back the original sorted array. There is no break point. Your code
  must handle that without a special case.
- Rotated by 1 gives `[3, 5, 7, 9, 11, 1]`, where the break is at the very end.

### The fact that survives

Pick any middle index. The array splits into `left = nums[low..mid]` and `right = nums[mid..high]`.
The break point sits in exactly one of them — it cannot be in both, because there is only one break.
Therefore **the other half has no break in it, which means the other half is properly sorted.**

At least one half is always sorted. That is the whole idea, and it is worth saying in exactly those
words.

### Finding out which half

One comparison:

```python
if nums[low] <= nums[mid]:
    # the left half climbs steadily -> left is sorted
else:
    # the left half contains the break -> right must be sorted
```

Prithvi's question. If the value at the left mark is smaller than the value at the middle, the stretch
between them only climbs, so it holds no break. If it is bigger, the break is in there somewhere, so
it is in the left and therefore not in the right.

The `<=` rather than `<` matters. When the range has shrunk to one element, `low == mid`, and
`nums[low] <= nums[mid]` is true — a single element is trivially sorted, which is the correct answer.
Using `<` there makes a one-element range take the wrong branch.

### Deciding where to go

Once you know which half is sorted, you can use ordinary range logic on it, because inside a sorted
half the plain comparison works again:

```python
if left half is sorted:
    if nums[low] <= target < nums[mid]:      # target lies inside the sorted left
        high = mid - 1                       # search left
    else:
        low = mid + 1                        # it cannot be there, so search right
else:                                        # right half is sorted
    if nums[mid] < target <= nums[high]:      # target lies inside the sorted right
        low = mid + 1
    else:
        high = mid - 1
```

Read it as Prithvi does. *Which stretch is in order? Is the target inside that stretch's range? If
yes, go there. If no, go to the other one.* The half you discard is discarded on a proof, not a
guess: a sorted stretch running 240 to 330 cannot contain 88, full stop.

Note the asymmetry in the two range checks — `nums[low] <= target < nums[mid]` on the left,
`nums[mid] < target <= nums[high]` on the right. `mid` is excluded from both because it has already
been compared to the target and did not match. The endpoints `low` and `high` are included because
they have not.

### Finding the smallest element instead

A close cousin, LeetCode 153, and it is cleaner than the search:

> The minimum is the element just after the break — the only element smaller than the one before it.

That is a monotone question, so [day 043](../day-043-binary-search-without-bugs/README.md)'s template
applies directly. The question is *is `nums[i]` less than or equal to the last element?*

```
nums     =  [ 9, 11,  1,  3,  5,  7]     last = 7
<= 7 ?      | no| no |YES|YES|YES|YES|
                       ^
                 first True = index 2 = the minimum
```

One template call and no branching at all. Compare `nums[mid]` with `nums[high]`, never with
`nums[low]` — comparing against `low` fails on a non-rotated array, and §7 shows it failing.

---

## 4. The picture

The rotation, drawn:

```
 sorted        [  1    3    5    7    9   11 ]
                                    ^ cut here, move the front to the back

 rotated       [  9   11    1    3    5    7 ]
 index            0    1    2    3    4    5
                       ^----^
                    the break: 11 followed by 1. Exactly one, ever.
```

**What to notice:** everywhere except that one join, the values climb. One break is the entire
structure of the problem.

Choosing a half, searching for 3:

```
 index         0     1     2     3     4     5
             +-----+-----+-----+-----+-----+-----+
 nums        |  9  | 11  |  1  |  3  |  5  |  7  |
             +-----+-----+-----+-----+-----+-----+
               low=0           mid=2         high=5

 nums[low]=9, nums[mid]=1.   9 <= 1 ?  NO
     -> the break is in the LEFT half, so the RIGHT half is sorted.

 right half runs nums[2]=1 up to nums[5]=7, in order.
 Is 3 in (1, 7] ?  yes.  ->  low = mid + 1 = 3.

 next pass:  low=3, high=5, mid=4, nums[4]=5
 nums[3]=3 <= nums[4]=5 ?  YES -> left half sorted, runs 3..5
 Is 3 in [3, 5) ?  yes -> high = mid - 1 = 3

 next pass:  low=3, high=3, mid=3, nums[3]=3 == target. Return 3.
```

**What to notice:** every discard is justified by a range, never by a single comparison. That is the
difference from plain binary search, and it is the sentence to say out loud.

Where the break can sit, and why it does not matter:

```
 break in the LEFT half             break in the RIGHT half
 [ 9  11 | 1  3  5  7 ]             [ 5  7  9 | 1  3  4 ]
   ^^^^^   ^^^^^^^^^^                 ^^^^^^^   ^^^^^^^
   broken   SORTED                    SORTED     broken

 not rotated at all: no break anywhere, so BOTH halves are sorted
 [ 1  3  5 | 7  9  11 ]   -- nums[low] <= nums[mid] is true, left branch taken, correct
```

**What to notice:** the un-rotated case takes the "left is sorted" branch and behaves like ordinary
binary search. No special case is needed, and adding one is how people break it.

---

## 5. The code, built step by step

### The frame is unchanged

```python
low, high = 0, len(nums) - 1
while low <= high:
    mid = (low + high) // 2
    if nums[mid] == target:
        return mid
```

Closed range, `<=`, exactly as [day 042](../day-042-binary-search-idea/README.md). Only the decision
about which half to keep changes.

### Which half is sorted

```python
    if nums[low] <= nums[mid]:
        ...     # left half is sorted
    else:
        ...     # right half is sorted
```

One comparison, and it is total: one of the two branches is always correct. `<=` handles the
one-element range, where `low == mid`.

### Inside the sorted left half

```python
        if nums[low] <= target < nums[mid]:
            high = mid - 1
        else:
            low = mid + 1
```

If the target's value falls inside the sorted stretch's range, it is in there if it is anywhere. If it
does not, it cannot be in there, so the other half is the only remaining possibility.

### Inside the sorted right half

```python
        if nums[mid] < target <= nums[high]:
            low = mid + 1
        else:
            high = mid - 1
```

The mirror image. Note `nums[mid] <` on this side and `< nums[mid]` on the other — `mid` is excluded
from both because it was already checked and did not match.

### The complete solution

```python
def search_rotated(nums: list[int], target: int) -> int:
    """LeetCode 33. Index of target in a rotated sorted array of DISTINCT values, else -1.

    Invariant: if target is in nums, its index is in nums[low..high].
    At every pass at least one half is properly sorted; the discard is proved by a range.
    """
    low, high = 0, len(nums) - 1

    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid

        if nums[low] <= nums[mid]:                    # left half is sorted
            if nums[low] <= target < nums[mid]:       # target lies inside it
                high = mid - 1
            else:
                low = mid + 1
        else:                                         # right half is sorted
            if nums[mid] < target <= nums[high]:      # target lies inside it
                low = mid + 1
            else:
                high = mid - 1

    return -1


def find_min_rotated(nums: list[int]) -> int:
    """LeetCode 153. The smallest value in a rotated sorted array of distinct values.

    The minimum is the first index whose value is <= the last value: a monotone question,
    so the boundary template applies with no branching at all.
    """
    low, high = 0, len(nums) - 1
    while low < high:                                 # half-open on the right
        mid = (low + high) // 2
        if nums[mid] > nums[high]:                    # the break is to the right of mid
            low = mid + 1
        else:                                         # mid could be the minimum: keep it
            high = mid
    return nums[low]


if __name__ == "__main__":
    print(search_rotated([9, 11, 1, 3, 5, 7], 3))     # 3
    print(search_rotated([9, 11, 1, 3, 5, 7], 9))     # 0   <- first element
    print(search_rotated([9, 11, 1, 3, 5, 7], 7))     # 5   <- last element
    print(search_rotated([9, 11, 1, 3, 5, 7], 4))     # -1  <- absent
    print(search_rotated([1, 3, 5, 7, 9, 11], 7))     # 3   <- NOT rotated at all
    print(search_rotated([3, 5, 7, 9, 11, 1], 1))     # 5   <- break at the very end
    print(search_rotated([5], 5), search_rotated([5], 6))    # 0 -1
    print(search_rotated([], 1))                      # -1

    print(find_min_rotated([9, 11, 1, 3, 5, 7]))      # 1
    print(find_min_rotated([1, 3, 5, 7, 9, 11]))      # 1   <- not rotated
    print(find_min_rotated([2, 1]))                   # 1   <- two elements
```

The three inputs that matter are the not-rotated array, the break-at-the-end array, and the
single-element array. A version that passes those three is almost certainly correct; a version that
special-cases any of them is almost certainly wrong.

### With duplicates, the guarantee breaks

LeetCode 81 allows repeats, and it changes the answer in a way worth understanding rather than
patching:

```python
nums = [3, 1, 3, 3, 3]
# low=0, mid=2, high=4:  nums[0]=3, nums[2]=3, nums[4]=3 -- all equal.
# Which half is sorted? There is no way to tell.
```

When `nums[low] == nums[mid]`, the comparison carries no information. The only safe move is to shrink
the range by one and try again:

```python
def search_rotated_dupes(nums: list[int], target: int) -> bool:
    """LeetCode 81. Worst case O(n) -- and that is unavoidable, not a flaw in this code."""
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return True
        if nums[low] == nums[mid] == nums[high]:      # no information: shrink both ends
            low += 1
            high -= 1
        elif nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return False
```

On `[1] * 100000 + [2]` searching for 2, that degrades to a linear scan. Say why in the interview:
**with duplicates, no comparison can distinguish `[1,1,1,1,2]` from `[1,1,2,1,1]` without looking at
more elements**, so `O(n)` worst case is a property of the problem, not of the solution.

---

## 6. What it costs

### Time

```
each pass:  1 equality check, 1 sortedness check, 1 range check  -> O(1)
each pass discards at least half the remaining range             -> log2(n) passes
                                                                 -> O(log n)
```

The comparisons per pass went from one to about three. The class did not move, and the number is
still small:

```
n = 1,000,000      20 passes x ~3 comparisons  = ~60 comparisons
n = 1,000,000,000  30 passes x ~3 comparisons  = ~90 comparisons
```

Say the constant honestly — "three comparisons a pass instead of one, so about three times the work
of plain binary search, and still logarithmic" — rather than pretending it is free.

### Space

```
low, high, mid: three integers     -> O(1) extra space
```

### With duplicates

```
best/average: O(log n)
worst:        O(n)   -- [1] * 100000 + [2], searching for 2

why: when nums[low] == nums[mid] == nums[high], no half can be ruled out,
     so the only safe step removes one element from each end.
```

### The alternative that is worth naming and rejecting

Find the pivot first with one binary search, then binary search the correct piece:

```
find_min:      log2(n) passes
then search:   log2(n) passes
               -----------------
               2 log2(n)  -- same class, twice the passes, two functions to get right
```

It is easier to reason about and slower by a constant, and some interviewers prefer it because the
two halves are each plainly correct. Know both. Offer the one-pass version, and mention the two-pass
version as the clearer alternative if they want to see the pivot found explicitly.

---

## 7. The traps

### The near-miss: comparing `nums[mid]` against the target instead of a range

```python
def broken(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:        # <-- plain binary search logic on rotated data
            low = mid + 1
        else:
            high = mid - 1
    return -1

print(broken([9, 11, 1, 3, 5, 7], 9))     # -1   should be 0
```

```
-1
```

The array is not sorted, so "the middle is smaller than the target" says nothing about where the
target is. `nums[mid] = 1`, which is less than 9, so it goes right — into the half that does not
contain 9. No error, wrong answer. **A discard must be justified by a sorted range, never by a single
comparison.**

### The near-miss: `<` instead of `<=` in the sortedness test

```python
        if nums[low] < nums[mid]:       # <-- should be <=
```

On a two-element range where `low == mid`, `nums[low] < nums[mid]` is false, so the code decides the
right half is sorted when in fact `mid == low` and the "right half" claim is meaningless:

```python
print(broken_lt([3, 1], 1))       # -1   should be 1
print(broken_lt([1], 1))          # 0    this one happens to work
```

A single element is sorted. The `<=` says so. This is the single most common bug in this problem, and
it only shows up on ranges of size one or two — which is exactly what the last two passes always are.

### The real error: comparing against `nums[low]` in find-minimum

```python
def broken_min(nums):
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] > nums[low]:        # <-- against low, not high
            low = mid + 1
        else:
            high = mid
    return nums[low]

print(broken_min([1, 3, 5, 7, 9, 11]))   # 11   should be 1
```

```
11
```

On an array that is not rotated, every middle is bigger than `nums[low]`, so `low` marches all the
way to the end and returns the maximum. Comparing against `nums[high]` is correct because the
question *"is `nums[mid]` at or below the last element?"* is monotone in both the rotated and the
un-rotated case. **Compare against `high` for the minimum. Always.**

### The real error: the empty array

```python
nums = []
low, high = 0, len(nums) - 1        # high = -1
mid = (low + high) // 2             # mid = -1
print(nums[mid])
```

```
Traceback (most recent call last):
  File "day45.py", line 4, in <module>
    print(nums[mid])
          ~~~~^^^^^
IndexError: list index out of range
```

The `while low <= high` in the real solution never runs on an empty array, because `0 <= -1` is
false — so the correct code handles it for free. The crash above is what happens if you hoist the
midpoint out of the loop, or write a `do-while`-shaped version. Fourth appearance of an index that
reaches `-1`; in Python it wraps rather than crashing, and here it happens to crash only because the
list is empty.

### The trap: assuming a rotation exists

Half the failing submissions on this problem contain a special case for "if the array is not
rotated". It is unnecessary — the un-rotated array takes the left-is-sorted branch on every pass and
behaves exactly like plain binary search — and the special case is another place to be wrong. Test
the un-rotated input; do not branch on it.

---

## 8. In the interview

### How it gets asked

- *"You have a sorted array that's been rotated at an unknown pivot. Find the target in O(log n)."* —
  LeetCode 33, word for word, and one of the most-asked medium questions anywhere.
- *"Find the minimum in a rotated sorted array."* — LeetCode 153, usually first, as the easier warm-up
  that establishes the break-point idea.
- *"Now the array can contain duplicates."* — LeetCode 81, the follow-up that comes ninety seconds
  after you finish, and the correct answer includes the words "O(n) worst case".
- *"How many times was this array rotated?"* — the same find-minimum search; the answer is the index
  of the minimum.

### What to say out loud, in the first ninety seconds

1. **Say the structure before the code.** *"A rotated sorted array has exactly one break point — one
   place where a value is followed by a smaller one. Everywhere else it climbs."*
2. **Say the fact that makes it work.** *"The break sits in one half or the other, never both. So at
   any midpoint, at least one half is properly sorted, and I can find out which in one comparison:
   is `nums[low] <= nums[mid]`?"*
3. **Say how you discard.** *"Once I know which half is sorted, I check whether the target's value
   falls inside that half's range. If it does, I search there. If it doesn't, it can't be there, so I
   search the other one. Every discard is justified by a range, not by one comparison — that's the
   part plain binary search gets to skip."*
4. **Ask the question that changes the answer.** *"Can the array contain duplicates? If it can, the
   worst case becomes O(n) and I'd write it differently."*
5. **State the cost.** *"O(log n) time, about three comparisons per pass instead of one, O(1) space."*

### The follow-ups

**"Now there can be duplicates. What breaks?"**
The comparison that tells me which half is sorted stops carrying information. Concretely, on
`[3, 1, 3, 3, 3]` with low at 0, mid at 2 and high at 4, all three values are 3, and there is no way
to tell whether the break is left or right of the middle — the array `[3, 3, 3, 1, 3]` looks
identical at those three positions and has the break on the other side. Since neither half can be
ruled out, the only safe move is to shrink the range by one from each end and try again, which makes
the worst case O(n) — an array of a hundred thousand ones with a single two in it. I want to be
precise that this is a property of the problem and not a weakness in my code: no comparison-based
method can distinguish those two arrays without looking at more elements, so O(n) is a lower bound
here. In the average case with few duplicates it is still logarithmic, and the one-line guard —
`if nums[low] == nums[mid] == nums[high]: low += 1; high -= 1` — is the entire difference between the
two solutions. LeetCode 81 also changes the return type to a boolean, because with duplicates "the
index" is not well defined.

**"Could you find the pivot first and then binary search normally? Which do you prefer?"**
Yes, and it is often the clearer answer, so I would offer both. Finding the pivot is its own binary
search: the minimum is the first index whose value is at most the last element, which is a monotone
question, so the boundary template handles it with no branching — compare `nums[mid]` against
`nums[high]`, and if it is bigger the break is to the right, otherwise keep the middle. That gives me
the index of the minimum, which is also the rotation count. Then I decide which piece the target
lives in by comparing it to the array's ends, and run a plain binary search on that piece — or,
more neatly, I search the whole array with index arithmetic, mapping index `i` to
`(i + pivot) % n`, which lets me use a completely unmodified binary search on a virtual sorted array.
The cost is 2 log n instead of log n, so the same class with twice the passes. I'd use the one-pass
version by default because it is a single loop, but I'd say that the two-pass version is easier to
prove correct under time pressure, and if I were writing this for a codebase where someone else has
to maintain it, that readability would probably win.

**"Why is your discard safe? Convince me you're not throwing away the answer."**
Because I never discard on a single comparison — I discard on a range, and the range is a proof.
Suppose the left half is sorted, so it runs from `nums[low]` up to `nums[mid]` with nothing out of
order in between. If the target is smaller than `nums[low]` or bigger than or equal to `nums[mid]`,
then it is outside the closed interval that half spans, and a sorted stretch contains exactly the
values inside its own range — so the target is provably not in there, and discarding it loses
nothing. If instead the target is inside that interval, the other half is the one I can discard, by
the same argument applied to whichever values it holds. The invariant is unchanged from plain binary
search: if the target is anywhere, its index is between low and high. What changed is only the
evidence I use to shrink that range. And the reason at least one half is always sorted is that there
is exactly one break point in the whole array, and one point cannot be in two halves at once.

### A model answer

> "First, the structure. A rotated sorted array has exactly one break point — one position where a
> value is followed by a smaller value. `[9, 11, 1, 3, 5, 7]` breaks between 11 and 1. Everywhere else
> it climbs.
>
> That single break gives me the key fact: whatever midpoint I pick, the break is in one half or the
> other, never both. So at least one half is properly sorted, always. And I can tell which in one
> comparison — if `nums[low] <= nums[mid]`, the left half climbs steadily, so it's the sorted one;
> otherwise the break is in the left, so the right one is sorted.
>
> Once I know which half is sorted, I use its *range* to decide. A sorted stretch running from 240 to
> 330 contains exactly the values in that interval, so if my target isn't in that interval it is
> provably not in that half, and I discard it. That's the difference from plain binary search: the
> discard is justified by a range rather than by one comparison.
>
> ```python
> def search_rotated(nums: list[int], target: int) -> int:
>     low, high = 0, len(nums) - 1
>     while low <= high:
>         mid = (low + high) // 2
>         if nums[mid] == target:
>             return mid
>         if nums[low] <= nums[mid]:                # left half sorted
>             if nums[low] <= target < nums[mid]:
>                 high = mid - 1
>             else:
>                 low = mid + 1
>         else:                                     # right half sorted
>             if nums[mid] < target <= nums[high]:
>                 low = mid + 1
>             else:
>                 high = mid - 1
>     return -1
> ```
>
> Two details I'd point at. The sortedness test is `<=`, not `<`, because when the range shrinks to
> one element low equals mid and a single element is sorted — that's the bug people hit, and it only
> shows up on the last two passes. And `mid` is excluded from both range checks, since I've already
> compared it to the target and it didn't match.
>
> No special case for an un-rotated array: it takes the left-is-sorted branch every pass and behaves
> exactly like ordinary binary search.
>
> Cost is O(log n) — about three comparisons per pass instead of one, so a constant factor of three —
> and O(1) space. One clarifying question I'd want answered before committing: can the values repeat?
> If they can, `nums[low] == nums[mid] == nums[high]` carries no information, the only safe move is to
> shrink both ends by one, and the worst case becomes O(n) — which is a property of the problem, not
> of the solution."

---

## 9. Recall card

- **One break point, ever.** So at any midpoint the break is in one half only, which means **at least
  one half is properly sorted** — that single fact is the whole problem.
- **`nums[low] <= nums[mid]` picks the sorted half.** `<=`, not `<`: a one-element range has
  `low == mid` and is trivially sorted. This is the bug everyone writes.
- **Discard on a range, never on one comparison.** Target inside the sorted half's interval → go
  there; outside → it is provably elsewhere. `mid` is excluded from both intervals.
- **Find-minimum is the clean cousin:** compare `nums[mid]` against **`nums[high]`** (never `low`) —
  monotone, so [day 043](../day-043-binary-search-without-bugs/README.md)'s template, no branching.
  The min's index is also the rotation count.
- **Duplicates → O(n) worst case, unavoidably.** When `nums[low] == nums[mid] == nums[high]`, shrink
  both ends by one; `[1]*100000 + [2]` is the killer, and no comparison-based method can do better.
