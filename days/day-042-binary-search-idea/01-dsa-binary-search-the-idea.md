---
day: 42
track: dsa
title: "Binary search: the idea and the invariant"
phase: "Binary search"
status: written
---

# Day 042 · DSA — Binary search: the idea and the invariant

**After today you can:** You can state, at every step, which half of the array still contains the answer.

**The interviewer asks it as:** *Search a sorted array. Why is it O(log n)?*

---

## 1. What this is, and why they ask it

**Binary search** finds a value in a **sorted** list by looking at the middle element and throwing
away the half that cannot contain the answer. Each look halves what is left, so a million elements
are settled in twenty looks instead of a million. The whole method rests on one sentence you must be
able to say at every step: *if the answer exists at all, it is still inside the stretch I am
holding.*

They ask it because it is the shortest interview problem that most candidates get wrong. Everyone
knows the idea; a large fraction cannot write it without an off-by-one bug or an infinite loop, and
interviewers know that. It also opens the largest pattern family in this course — days 043 to 050
are all binary search wearing different clothes, and by
[day 046](../day-046-binary-search-on-the-answer/README.md) the thing being searched is not even an
array. So today is not "learn a trick". Today is where the idea and its guarantee get nailed down,
because everything after leans on both.

---

## 2. The story

Shobha is going to a wedding at half past eleven, and the address on the invitation says house
number 214, Second Cross Lane. She gets off the bus at the top of the lane at ten to eleven, in a
silk sari and the wrong shoes, holding a gift box with both hands.

The lane is long. It runs straight for nearly a kilometre and there are gates down both sides, four
hundred of them at least, and the numbers climb steadily as you walk. The first gate says 2. She
cannot see the far end.

The obvious thing is to start walking and read every gate until 214 comes up. She has done that
before, in another lane, in the rain, and it took twenty minutes.

So she does something else. She walks to roughly the middle of the lane — a stretch of shuttered
shops, about five minutes — and reads the nearest gate. It says 260. That one number tells her
something large: 214 is *behind* her. Everything in front of her, half the lane, is finished with.
She does not have to look at any of it again.

She turns and walks back, but not all the way. She goes to the middle of what is left, between the
top of the lane and where she is standing, and reads that gate. 130. Too small. So 214 is ahead of
this gate and behind the one that said 260. She now knows two things at once, and she says them to
herself: after 130, before 260.

She keeps doing it. Halfway between: 196. Too small — after 196, before 260. Halfway: 228. Too big —
after 196, before 228. Halfway: 212. Then the next gate but one is 214, with a shamiana out front
and the sound of a nadaswaram.

Six stops. Not two hundred.

One stretch nearly ruined it. Near the school there is a block a builder renumbered, where 88 sits
between 300 and 74. Where the numbers climb steadily, the trick works. Where they jump about, it is
worth nothing, and Shobha has learnt to check that before she starts.

---

## 3. The idea in plain English

Shobha's lane is a sorted array. Her two remembered gates — *after 130, before 260* — are the two
variables the code keeps. And the renumbered block near the school is the precondition: **the trick
requires order, and gives nothing without it.**

### The setup

Take a seven-element sorted array and look for the value 23:

```python
nums   = [3, 9, 14, 23, 31, 42, 55]
target = 23
```

**Sorted** means: reading left to right, the values never go down. That is the only thing binary
search needs. It does not need them evenly spaced, it does not need them positive, and it does not
need them to be numbers at all — only that "less than" means something and the list respects it.

You keep two variables:

- `low` — the leftmost index that could still hold the answer.
- `high` — the rightmost index that could still hold the answer.

They start at the two ends: `low = 0`, `high = 6`. The stretch `nums[low..high]` is called the
**search space** — the part of the array you have not ruled out yet. At the start it is everything.

### The invariant

An **invariant** — a word you met on [day 028](../day-028-opposite-ends/README.md) — is a statement
that is true before the loop starts, stays true after every pass, and is therefore true when the
loop ends. Binary search has exactly one, and it is the whole lesson:

> **If `target` is anywhere in the array, its index is between `low` and `high`, both included.**

Say it out loud. Every line of the code exists to keep it true. When it stops being true, the search
breaks; when it stays true and the space empties, the honest conclusion is that the target was never
there.

### One step

Look at the middle of the current stretch:

```
middle = (low + high) // 2
```

`//` is integer division, so `(0 + 6) // 2 = 3`. Now compare `nums[3]`, which is 23, with the target
23. Three things can happen, and only three:

- **`nums[middle] == target`.** Found it. Return `middle`.
- **`nums[middle] < target`.** The middle value is too small. Because the array is sorted,
  *everything at or to the left of `middle`* is also too small. None of it can be the answer, so the
  new search space starts one past the middle: `low = middle + 1`.
- **`nums[middle] > target`.** The middle is too big, so is everything to its right, and
  `high = middle - 1`.

The `+ 1` and the `- 1` are not decoration. The middle has been checked; leaving it in the space is
how infinite loops happen, and §7 shows exactly that.

### When to stop

The loop runs while `low <= high` — while the stretch still holds at least one index. If `low` ever
passes `high`, the stretch is empty, the invariant says the target would have been inside it, and
therefore the target is not in the array at all. Return `-1`.

That is the part people skate over. The failure case is not a guess; it is the invariant reporting a
fact.

### Why it is fast

Each pass throws away half. Starting from 7 elements: 7 → 3 → 1 → 0. Starting from a million:
1,000,000 → 500,000 → 250,000 → … → 1, which takes twenty steps. The number of halvings needed to
get from `n` down to 1 is the **base-2 logarithm** of `n`, written `log₂ n` — the growth curve you
met on [day 004](../day-004-the-growth-curves/README.md). That is where **O(log n)** comes from, and
in an interview you say it by counting halvings, not by naming the curve.

---

## 4. The picture

The array, and the three variables that matter:

```
 index         0     1     2     3     4     5     6
             +-----+-----+-----+-----+-----+-----+-----+
 value       |  3  |  9  | 14  | 23  | 31  | 42  | 55  |
             +-----+-----+-----+-----+-----+-----+-----+
                ^                 ^                 ^
              low=0          middle=3            high=6

 search space = nums[0..6], everything. target = 42.
```

**What to notice:** `middle` is not a third traveller. It is recomputed from `low` and `high` on
every pass and forgotten immediately after.

Searching for 42, pass by pass:

```
 pass 1   low=0  high=6   middle=3   nums[3]=23  < 42   -> go right, low = 4
             [  3    9   14   23 ]  31   42   55
              ^^^^^^^^^^^^^^^^^^^^  all thrown away, never read

 pass 2   low=4  high=6   middle=5   nums[5]=42  = 42   -> found, return 5
                             31  [ 42 ]  55

 two comparisons for seven elements.
```

**What to notice:** in pass 1 the four discarded cells were never visited. That is what "throwing
away half" costs — nothing.

And the failure case, searching for 40:

```
 pass 1   low=0 high=6  middle=3  nums[3]=23 < 40  -> low = 4
 pass 2   low=4 high=6  middle=5  nums[5]=42 > 40  -> high = 4
 pass 3   low=4 high=4  middle=4  nums[4]=31 < 40  -> low = 5

 now low=5, high=4. low > high, the stretch is empty. 40 is not here.
```

**What to notice:** `low` ends up sitting exactly where 40 *would* go if you inserted it. That is
not a coincidence, and [day 043](../day-043-binary-search-without-bugs/README.md) turns it into a
tool.

---

## 5. The code, built step by step

### The two ends

```python
low, high = 0, len(nums) - 1
```

`high` is the last **valid index**, not the length. `len(nums)` is 7; the last index is 6. Getting
this wrong is the most common first-line mistake, and it costs you an `IndexError` on the very first
pass when the target is large.

### The loop condition

```python
while low <= high:
    ...
```

`<=`, not `<`. When `low == high` the stretch still holds one index, and that one index might be the
answer. Stopping at `low < high` skips it — a bug that is invisible on most inputs and fires on
single-element searches. §7 shows it failing.

### The middle, and the three-way comparison

```python
middle = (low + high) // 2
if nums[middle] == target:
    return middle
if nums[middle] < target:
    low = middle + 1
else:
    high = middle - 1
```

Read the two assignments as sentences. `low = middle + 1` says "everything up to and including the
middle is too small, so the space now starts after it". `high = middle - 1` says the mirror image.
Both shrink the space by at least one element, which is what guarantees the loop ends.

### The empty answer

```python
return -1
```

Reached only when `low > high` — the space is empty. By the invariant, the target was never in the
array.

### The complete solution

```python
def binary_search(nums: list[int], target: int) -> int:
    """Index of target in the sorted list nums, or -1 if it is not there.

    Invariant: if target is in nums, its index is in nums[low..high].
    """
    low, high = 0, len(nums) - 1

    while low <= high:                      # stretch still holds at least one index
        middle = (low + high) // 2          # integer division: floor of the midpoint
        if nums[middle] == target:
            return middle
        if nums[middle] < target:
            low = middle + 1                # middle and everything left of it is too small
        else:
            high = middle - 1               # middle and everything right of it is too big

    return -1                               # low passed high: the space is empty


if __name__ == "__main__":
    nums = [3, 9, 14, 23, 31, 42, 55]
    print(binary_search(nums, 42))          # 5
    print(binary_search(nums, 3))           # 0   <- first element
    print(binary_search(nums, 55))          # 6   <- last element
    print(binary_search(nums, 40))          # -1  <- absent, between two present values
    print(binary_search(nums, 1))           # -1  <- absent, below everything
    print(binary_search(nums, 99))          # -1  <- absent, above everything
    print(binary_search([], 5))             # -1  <- empty input, no crash
    print(binary_search([7], 7))            # 0   <- single element, found
    print(binary_search([7], 8))            # -1  <- single element, absent
```

Run it. The last four lines are the ones worth watching: an empty list must not crash, and a
one-element list must be able to answer both ways. Those three inputs catch most beginner versions.

### The recursive form, and why the loop is preferred

```python
def binary_search_rec(nums: list[int], target: int, low: int, high: int) -> int:
    if low > high:
        return -1
    middle = (low + high) // 2
    if nums[middle] == target:
        return middle
    if nums[middle] < target:
        return binary_search_rec(nums, target, middle + 1, high)
    return binary_search_rec(nums, target, low, middle - 1)
```

Identical logic, and some interviewers ask for it. It costs `O(log n)` **stack space** — each call
waits for the one below it — where the loop costs `O(1)`. Say that trade if you write this version.
Recursion gets its own phase from [day 087](../day-087-recursion-leap-of-faith/README.md); today,
prefer the loop.

### In an interview you would use this

```python
from bisect import bisect_left

def binary_search_lib(nums: list[int], target: int) -> int:
    i = bisect_left(nums, target)                       # first index where target could go
    return i if i < len(nums) and nums[i] == target else -1
```

`bisect_left` returns the **insertion point**: the leftmost index where `target` could be placed
while keeping the list sorted. It does not tell you whether the value is there, which is why the
check after it exists. Write the loop when asked to write binary search; reach for `bisect` when
binary search is a step inside a larger problem.
[Day 043](../day-043-binary-search-without-bugs/README.md) is entirely about that insertion-point
idea.

---

## 6. What it costs

### Time, counted by halving

The search space starts at `n` and at least halves every pass:

```
pass:      0      1      2      3      4     ...
size:      n     n/2    n/4    n/8   n/16    ...
```

The loop ends when the size reaches 0, so the number of passes is the number of halvings that take
`n` to 1, plus one. That count is `log₂ n`. Each pass does a fixed amount of work — one addition,
one division, one or two comparisons, one assignment — so the total is **O(log n)**.

Put real numbers on it, because the interviewer wants the number, not the letter:

```
n = 1,000                     10 comparisons     (2^10 = 1,024)
n = 1,000,000                 20 comparisons     (2^20 ~ 1.05 million)
n = 1,000,000,000             30 comparisons     (2^30 ~ 1.07 billion)
n = 8,000,000,000             33 comparisons     (every person alive)
```

Thirty-three looks to find one person among eight billion, sorted. Against
[day 012](../day-012-linear-search/README.md)'s linear search, which averages four billion. The
sentence to have ready: **every doubling of the input adds one comparison.**

### Space

```
low, high, middle: three integers, whatever n is   -> O(1) extra space
```

The iterative version allocates nothing. The recursive version holds one stack frame per pass, so
`O(log n)` — thirty frames at a billion elements, which is nothing, but it is not `O(1)` and saying
so is free marks.

### The cost that is not in the loop

Binary search needs a sorted array. If the array arrives unsorted, sorting it costs `O(n log n)` —
more than a single linear scan. So:

```
one search on unsorted data   : scan it, O(n). Sorting first is a loss.
many searches on fixed data   : sort once, O(n log n), then O(log n) each.
                                A win by the second or third search.
```

That is [day 037](../day-037-prefix-sums/README.md)'s trade again, in new clothes: **pay a
preparation cost once, buy cheap answers forever.** Say it that way and you have connected two
phases in one sentence.

---

## 7. The traps

### The near-miss: `while low < high`

```python
def broken(nums, target):
    low, high = 0, len(nums) - 1
    while low < high:                  # <-- strict, not <=
        middle = (low + high) // 2
        if nums[middle] == target:
            return middle
        if nums[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1

print(broken([3, 9, 14, 23, 31, 42, 55], 42))   # 5   looks fine
print(broken([3, 9, 14, 23, 31, 42, 55], 55))   # -1  WRONG, 55 is at index 6
print(broken([7], 7))                           # -1  WRONG, 7 is at index 0
```

```
5
-1
-1
```

It passes the case you test first and fails on the last element and on any single-element list. The
reason is exactly the invariant: when `low == high` the stretch still contains one index, and the
strict `<` refuses to look at it. **If the space is non-empty, look at it.** That is what `<=` means.

### The near-miss: forgetting the `+ 1`

```python
    if nums[middle] < target:
        low = middle                   # <-- should be middle + 1
```

On `[1, 3]` searching for 3: `low=0, high=1, middle=0`, `nums[0]=1 < 3`, so `low = 0`. Nothing
changed. The next pass computes the same middle, takes the same branch, and sets the same `low`. The
program does not crash — it hangs, silently, forever, and in an interview you will sit there
watching a blank terminal. The middle has already been compared; it must leave the space.

### The real error: `high = len(nums)`

```python
nums = [3, 9, 14, 23, 31, 42, 55]
low, high = 0, len(nums)               # <-- length, not last index
while low <= high:
    middle = (low + high) // 2
    if nums[middle] == 99:
        break
    low = middle + 1
```

```
Traceback (most recent call last):
  File "day42.py", line 6, in <module>
    if nums[middle] == 99:
       ~~~~^^^^^^^^
IndexError: list index out of range
```

`high` starts at 7, the loop allows `middle` to reach 7, and index 7 does not exist. This one at
least crashes. The `low < high` bug does not, which is why it is the more dangerous of the two.

### The trap that is not in the code: unsorted input

```python
print(binary_search([5, 2, 9, 1, 7], 9))    # -1
```

Nine is in the list. Binary search says it is not, returns quietly, and no exception is raised. The
function's contract says "sorted"; the input broke the contract; the answer is garbage. Shobha's
renumbered block. **Ask "is the input sorted?" before you write a line** — it is a ten-second
question that saves the whole answer.

### The overflow trap, which Python hides

`(low + high) // 2` can overflow a 32-bit integer in Java or C++ when both indices are near two
billion — a famous bug that sat in the Java standard library for nine years. The safe form is:

```python
middle = low + (high - low) // 2       # identical result, cannot overflow
```

Python's integers grow without limit, so it never bites here. Mention it anyway if the interviewer's
language is not Python: it takes one sentence and shows you know where the edge is.

---

## 8. In the interview

### How it gets asked

- *"Given a sorted array of integers and a target, return the index of the target, or -1."* —
  LeetCode 704, the direct form, often as a warm-up before something harder.
- *"How would you find a name in a sorted list of ten million? Why is that fast?"* — the same
  question wearing an explanation's clothes. They want the halving count out loud.
- *"Implement it, then tell me the invariant."* — the version that separates people. Many candidates
  can produce the code and cannot say what it maintains.
- And as a **component**: "first I'd sort, then binary search for each" appears inside dozens of
  harder problems from here on.

### What to say out loud, in the first ninety seconds

1. **Confirm the precondition.** *"Binary search needs the array sorted ascending — can I assume
   that? And are there duplicates, or do you want any matching index?"*
2. **State the invariant before writing anything.** *"I'll keep two indices, low and high. The
   invariant is: if the target is in the array at all, its index is between low and high inclusive.
   Every step preserves that."*
3. **Say what each step does.** *"I look at the middle. If it's too small, everything up to and
   including it is too small, so low becomes middle plus one. If it's too big, high becomes middle
   minus one. If it's equal, I'm done."*
4. **Say the termination condition and what it means.** *"The loop runs while low is less than or
   equal to high. If low passes high, the space is empty, and by the invariant the target isn't
   there — so I return minus one."*
5. **Give the cost with a number.** *"O(log n) time, O(1) space. A million elements is twenty
   comparisons; a billion is thirty."*

Then write it. The code takes ninety seconds because you have already said what every line does.

### The follow-ups

**"Why is it O(log n)? Prove it to me without hand-waving."**
Because the search space at least halves every pass, and I can count the halvings. It starts at n.
After one pass it is at most n/2, after two at most n/4, after k passes at most n divided by 2 to
the k. The loop stops when that reaches 1, so 2 to the k equals n, so k equals log base 2 of n. Each
pass does constant work — one midpoint calculation and at most two comparisons — so the total is
O(log n). The sentence I'd actually use in a room is shorter: every time the input doubles, I pay
exactly one more comparison. A thousand elements is ten comparisons, a million is twenty, a billion
is thirty. That is why it stays usable at sizes where a linear scan has stopped being an option.

**"What if the array has duplicates? Which index do you return?"**
As written, an arbitrary one — whichever the halving lands on first — and that is worth saying
explicitly rather than pretending it is deterministic. If the question wants the *first* occurrence,
the change is small but the shape is different: on a match I don't return, I record the index and
keep searching left by setting high to middle minus one. The mirror gives the last occurrence. Both
still cost O(log n), because I still halve every pass, I just refuse to stop early. That pair is a
standard follow-up, LeetCode 34, and Python's `bisect_left` and `bisect_right` are exactly those two
answers in the standard library. I'd also flag the naive alternative and why it is bad: find any
match, then walk left. That is O(log n) plus O(k) for k duplicates, and degrades to O(n) when the
array is all one value.

**"The array is rotated — sorted, but starting from somewhere in the middle. Now what?"**
The invariant survives, but the test that decides which half to keep does not, because
`nums[middle] < target` no longer implies the answer is to the right. What is still true is that at
least one of the two halves is properly sorted — compare `nums[low]` with `nums[middle]` to find out
which. Then check whether the target lies inside that sorted half's range; if it does, search there,
and if it doesn't, search the other half. Still O(log n), still one loop, and the extra work is a
range check rather than a scan. That is the whole of
[day 045](../day-045-rotated-array-search/README.md), and it is a top-five interview question at
product companies precisely because it tests whether you understand the invariant or memorised the
template.

### A model answer

> "Sorted array, so binary search. Before I write anything, let me state what the code maintains:
> two indices, low and high, and the invariant that if the target is in the array, its index is
> between them inclusive. That single sentence decides every line.
>
> I start with low at 0 and high at the last index — the last index, not the length. Then I loop
> while low is less than or equal to high, because as long as low equals high there is still one
> cell I haven't looked at.
>
> Each pass I take the middle. If it equals the target I return it. If it's smaller, then it and
> everything to its left is too small, so low becomes middle plus one. If it's bigger, high becomes
> middle minus one. Both branches shrink the space by at least one, which is why the loop always
> terminates.
>
> ```python
> def binary_search(nums: list[int], target: int) -> int:
>     low, high = 0, len(nums) - 1
>     while low <= high:
>         middle = (low + high) // 2
>         if nums[middle] == target:
>             return middle
>         if nums[middle] < target:
>             low = middle + 1
>         else:
>             high = middle - 1
>     return -1
> ```
>
> If low passes high the space is empty, and the invariant tells me the target was never there, so
> minus one is a conclusion rather than a guess.
>
> Cost is O(log n) time — twenty comparisons at a million elements, thirty at a billion — and O(1)
> extra space, since it's three integers regardless of n. A recursive version would be O(log n)
> stack instead.
>
> Two things I'd flag. This is silently wrong on unsorted input — it returns minus one for values
> that are present — so 'is it sorted?' is my first clarifying question. And in Java or C++ I'd
> write the midpoint as low plus high-minus-low over two, because low plus high can overflow a
> 32-bit int; Python doesn't have that problem, but the habit is worth keeping."

---

## 9. Recall card

- **The invariant is the lesson:** *if the target is anywhere, its index is in `nums[low..high]`.*
  Every line exists to keep it true; an empty space is a conclusion, not a guess.
- **Four details, all off-by-one:** `high = len(nums) - 1`, `while low <= high`, `low = middle + 1`,
  `high = middle - 1`. Drop the `+1` and it hangs; use `<` and it misses the last element.
- **O(log n) time, O(1) space** — count halvings out loud: 1,000 → 10, a million → 20, a billion →
  30. Every doubling costs one more comparison.
- **Sorted is a precondition, not a hint.** On unsorted input it returns −1 for values that are
  there, with no error. Ask before you write.
- **`bisect_left` is the library answer** and returns an *insertion point*, not a found flag — check
  `nums[i] == target` after. Tomorrow: one template that removes the off-by-ones for good.
