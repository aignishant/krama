---
day: 43
track: dsa
title: "Writing binary search without off-by-one bugs"
phase: "Binary search"
status: written
---

# Day 043 · DSA — Writing binary search without off-by-one bugs

**After today you can:** You can write it correctly the first time, every time, using one template.

**The interviewer asks it as:** *Write binary search on the whiteboard. No compiler.*

---

## 1. What this is, and why they ask it

Yesterday's binary search finds *a* matching element. Today you learn a second template that finds a
**boundary** — the first position where something becomes true — and that template answers every
binary search question you will ever be asked, including yesterday's. It is four lines, it has one
invariant, and once it is in your hands the off-by-one bugs stop happening because there is nothing
left to get wrong.

They ask you to write it without a compiler because that is where the bugs live. A candidate who
knows only yesterday's three-way version has to re-derive the `+ 1` and `- 1` for every variant —
first occurrence, last occurrence, insertion point, rotated array, search on the answer — and
re-derives one of them wrong under pressure. A candidate with today's template writes the same four
lines every time and changes only one line: the question being asked of the middle. That is the
difference between remembering an algorithm and owning one.

---

## 2. The story

Vasu keeps a small boat tied at the ghat on the river at Ranganathittu, and he goes down to it most
mornings at about six.

The ghat is a long flight of stone steps running down to the water, sixty-odd of them, wide and worn
smooth. The river is not the same height two days running. After rain it climbs; in March it drops
so far that the bottom twenty steps bake dry and the weeds on them go brown.

Every morning Vasu has the same small job before he does anything else. He carries a cloth bag with
his flask and his slippers in it, and he wants to leave it on the lowest step that is still dry — as
close to the water as he can get without soaking it, because he is coming back up wet and does not
want to climb far.

He does not walk down testing every step. He learnt that when he was younger and it was cold.

What he does instead is this. He goes down to roughly the middle of the flight and puts his bare
foot on that step. If it comes up dry, he knows two things at once: that step is dry, and so is
every step above it, so there is no reason ever to look up there again. The step he is standing on
is not the one he wants either — he wants a lower one — so he moves on past it.

If it comes up wet, he knows the opposite: this step and everything below it is under water. But — and
this is the part he is careful about — he does *not* move past a wet step. The step he just touched
might be the very first wet one, the boundary itself, and the one he wants is directly above it. He
keeps it in mind and searches upward from there, but he does not throw it away.

Dry step: step past it. Wet step: keep it. He does that five or six times, the range closing in each
time, and then there is nothing left between his two marks, and the boundary is exactly there. Bag
down, into the boat, gone by ten past six.

---

## 3. The idea in plain English

Vasu's steps are the array. Wet or dry is a **yes-or-no question** asked of one position. And the
crucial asymmetry — *step past a dry one, keep a wet one* — is the whole template.

### The one property the steps have

Reading from the top down, the steps go dry, dry, dry, …, wet, wet, wet. They never go back. There
is no dry step below a wet one, because water does not work like that.

A yes-or-no question with that shape is called **monotone**: once the answer flips from no to yes,
it stays yes. Binary search does not actually need a sorted array. It needs a monotone question, and
a sorted array is simply the most common way to get one.

Write the question as a function of the index:

```python
def is_wet(i: int) -> bool:
    ...
```

and the array of answers looks like this:

```
 index   0      1      2      3      4      5      6      7
       False  False  False  False  True   True   True   True
                                    ^
                              the boundary: the first True
```

**The boundary is the answer to every binary search problem.** Yesterday's "find target" is one
instance of it, as you will see in a moment.

### The two marks, and what they mean

Two variables again, but they mean something different from yesterday:

- `low` — the first index that might still be True.
- `high` — one past the last index that might still be True.

So the live range is `[low, high)`: `low` included, `high` **not** included. That is called a
**half-open range**, and it is the same convention Python slicing already uses — `nums[2:5]` gives
you indices 2, 3 and 4, not 5. You have been using it since
[day 005](../day-005-python-lists-and-tuples/README.md).

They start at `low = 0` and `high = len(nums)` — note, the *length*, not the last index. That is not
a bug. `high` is deliberately one past the end, because the honest answer to "where is the first
True?" when there is no True at all is *"one past the end"*.

### The invariant

> **Everything at an index below `low` is False. Everything at an index at or above `high` is True.
> The boundary is somewhere in `[low, high)`.**

That is the sentence to say in the interview. It is stronger than yesterday's, and it is what makes
the code write itself.

### The four lines

```python
while low < high:
    middle = (low + high) // 2
    if question(middle):
        high = middle          # middle might BE the boundary — keep it
    else:
        low = middle + 1       # middle is definitely not — step past it
```

Read the two branches as Vasu's two rules.

- The question is **True** at `middle` — the step is wet. Then `middle` is a True, and the first
  True is at `middle` or earlier. So the range shrinks to `[low, middle)`… except `middle` itself
  must stay in play, and it does, because the range is half-open: `high = middle` means "everything
  from `middle` on is known True", and `middle` is still reachable through `low`.
- The question is **False** — the step is dry. Then `middle` is not the boundary and neither is
  anything before it, so `low = middle + 1`.

When the loop ends, `low == high`, the range is empty, and by the invariant everything below `low`
is False and everything from `low` on is True. **`low` is the boundary.** No `-1`, no special case,
no "did I find it" flag.

### Why `while low < high` this time, and not `<=`

Yesterday's range was `[low, high]` with both ends included, so `low == high` still held one live
index and the loop had to run. Today's range is `[low, high)`, so `low == high` holds *nothing* and
the loop must stop. The comparison follows from the convention, which is why you should pick one
convention and never mix them. Mixing is the actual source of nearly every off-by-one bug in this
subject.

### Everything else is this template with a different question

```
question(i) = nums[i] >= target     ->  low = first index whose value is >= target   (lower bound)
question(i) = nums[i] >  target     ->  low = first index whose value is >  target   (upper bound)
```

And from those two:

- **Does `target` exist?** Take the lower bound `i`, then check `i < len(nums) and nums[i] == target`.
- **Where would `target` be inserted?** The lower bound, unchanged. That is LeetCode 35.
- **First occurrence of `target`?** The lower bound, when it matches.
- **Last occurrence?** The upper bound minus one.
- **How many equal `target`?** Upper bound minus lower bound. One subtraction.

Five problems, one template, one changed line. That is why today exists.

---

## 4. The picture

The question's answers, and what the two marks mean:

```
 index        0      1      2      3      4      5      6      7
            +------+------+------+------+------+------+------+------+
 nums       |  2   |  4   |  4   |  4   |  7   |  9   | 11   | 15   |
            +------+------+------+------+------+------+------+------+
 >= 4 ?     | no   | YES  | YES  | YES  | YES  | YES  | YES  | YES  |
 >  4 ?     | no   | no   | no   | no   | YES  | YES  | YES  | YES  |
                      ^                    ^
                lower bound = 1      upper bound = 4

 count of 4s = upper - lower = 4 - 1 = 3.
```

**What to notice:** both rows are monotone — once they turn to YES they stay. That, and nothing
else, is what binary search requires.

The half-open range closing in, searching for the lower bound of 7:

```
 start   low=0                                   high=8   (one past the end)
         [ 2    4    4    4    7    9   11   15 )

 pass 1  middle=4, nums[4]=7 >= 7  -> YES  -> high = 4     (keep 4: it might be it)
         [ 2    4    4    4 ) 7    9   11   15

 pass 2  middle=2, nums[2]=4 >= 7  -> no   -> low = 3      (step past it)
                        [ 4 ) 7    9   11   15

 pass 3  middle=3, nums[3]=4 >= 7  -> no   -> low = 4
                             ) low = high = 4, loop ends

 answer: low = 4.
```

**What to notice:** on pass 1 `high` became 4 and the answer *is* 4. If the code had written
`high = middle - 1` — yesterday's reflex — it would have thrown away the answer on the first pass.
That single line is the difference between the two templates.

And the case with no True at all:

```
 nums = [2, 4, 4], question = "nums[i] >= 9"
 every answer is no, low climbs to 3, high stays 3, loop ends, low = 3 = len(nums)

 "one past the end" is the boundary's honest answer for "there is no True".
```

**What to notice:** no special case handled it. The convention handled it.

---

## 5. The code, built step by step

### The template, alone

```python
def first_true(lo: int, hi: int, question) -> int:
    """Smallest i in [lo, hi) where question(i) is True, or hi if none is."""
    while lo < hi:
        mid = (lo + hi) // 2
        if question(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Six lines, and they never change. Everything below is a different `question`.

### Lower bound

```python
def lower_bound(nums: list[int], target: int) -> int:
    """First index whose value is >= target; len(nums) if there is none."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

The only line carrying any thought is `nums[mid] >= target`. Say it out loud as a question — *is
this position at or past where the target belongs?* — and the branch that follows is obvious.

### Upper bound: change one character

```python
        if nums[mid] > target:      # was >=
            hi = mid
```

`>` instead of `>=`. Now positions holding the target itself answer "no", so `low` walks past all of
them and lands one past the last copy.

### Search, insertion point, and the count

```python
def search(nums: list[int], target: int) -> int:
    i = lower_bound(nums, target)
    return i if i < len(nums) and nums[i] == target else -1

def insert_position(nums: list[int], target: int) -> int:
    return lower_bound(nums, target)                      # LeetCode 35, entire answer

def count_of(nums: list[int], target: int) -> int:
    return upper_bound(nums, target) - lower_bound(nums, target)
```

Note the guard in `search`: `i < len(nums)` **before** `nums[i]`. If the target is bigger than
everything, `i` is `len(nums)` and indexing it raises. The `and` short-circuits, so the order of the
two conditions is doing real work.

### The complete solution

```python
from bisect import bisect_left, bisect_right


def first_true(lo: int, hi: int, question) -> int:
    """The template. Smallest i in [lo, hi) with question(i) True, else hi.

    Invariant: everything below lo answers False, everything from hi up answers True.
    """
    while lo < hi:
        mid = (lo + hi) // 2            # mid < hi always, so hi = mid strictly shrinks
        if question(mid):
            hi = mid                    # mid might be the boundary: keep it
        else:
            lo = mid + 1                # mid is not the boundary: step past it
    return lo


def lower_bound(nums: list[int], target: int) -> int:
    """First index with nums[i] >= target. len(nums) if every value is smaller."""
    return first_true(0, len(nums), lambda i: nums[i] >= target)


def upper_bound(nums: list[int], target: int) -> int:
    """First index with nums[i] > target. len(nums) if no value is bigger."""
    return first_true(0, len(nums), lambda i: nums[i] > target)


def search(nums: list[int], target: int) -> int:
    """LeetCode 704, rebuilt on the boundary template."""
    i = lower_bound(nums, target)
    return i if i < len(nums) and nums[i] == target else -1


def insert_position(nums: list[int], target: int) -> int:
    """LeetCode 35. The lower bound, with no extra work at all."""
    return lower_bound(nums, target)


def count_of(nums: list[int], target: int) -> int:
    """How many copies of target the sorted list holds."""
    return upper_bound(nums, target) - lower_bound(nums, target)


if __name__ == "__main__":
    nums = [2, 4, 4, 4, 7, 9, 11, 15]

    print(lower_bound(nums, 4), upper_bound(nums, 4))    # 1 4
    print(count_of(nums, 4))                             # 3
    print(count_of(nums, 5))                             # 0   <- absent, no special case
    print(lower_bound(nums, 1), lower_bound(nums, 99))    # 0 8 <- below all, above all
    print(search(nums, 9), search(nums, 10))              # 5 -1
    print(insert_position([1, 3, 5, 6], 2))               # 1
    print(insert_position([1, 3, 5, 6], 7))               # 4   <- one past the end
    print(lower_bound([], 5))                             # 0   <- empty input, no crash

    # The standard library is this template, already written.
    print(bisect_left(nums, 4), bisect_right(nums, 4))    # 1 4
```

`bisect_left` **is** `lower_bound` and `bisect_right` **is** `upper_bound`. They are written in C
and they are correct. Write the template when the interviewer asks you to write binary search; call
`bisect` when binary search is a step inside a bigger problem and nobody is testing your loop.

---

## 6. What it costs

### Time

Identical to yesterday, because it is the same halving:

```
range size:   n  ->  n/2  ->  n/4  ->  ...  ->  1  ->  0
passes:            log2(n) + 1
work per pass:     one midpoint, one question, one assignment  -> O(1)
```

**O(log n)**, and the count is the same twenty comparisons at a million, thirty at a billion. One
caveat worth saying: the cost is `O(log n)` **questions**, and if the question itself is expensive —
which it will be from [day 046](../day-046-binary-search-on-the-answer/README.md), where answering it
means scanning the array — the real cost is `O(log n × cost of one question)`.

### Space

```
lo, hi, mid: three integers    -> O(1) extra space
```

### Why it always terminates

This is the part interviewers probe, because "it hangs" is the most common failure and candidates
rarely know why theirs does not.

The loop runs only while `lo < hi`, so `lo + hi < 2 × hi`, so `mid = (lo + hi) // 2 < hi`. Therefore
`hi = mid` strictly *decreases* `hi`. And `mid >= lo` always, so `lo = mid + 1` strictly *increases*
`lo`. Every pass moves one of the two marks toward the other by at least one, and they cannot cross
without the loop stopping. **The range shrinks by at least one every pass, so it cannot run more
than n times, and in fact runs log n times.**

Say that in one sentence: *`mid` is always strictly less than `hi`, so `hi = mid` always makes
progress.* That sentence is the reason `high = middle` is safe here and would hang in yesterday's
`[low, high]` template — where `mid` can equal `hi`, and assigning `hi = mid` changes nothing.

### The comparison worth naming

```
yesterday's template : 3-way compare, returns -1 when absent, needs re-derivation per variant
today's template     : 2-way question, returns a POSITION always, one line changes per variant

five problems solved by changing one character:
    exists / insert position / first occurrence / last occurrence / count
```

---

## 7. The traps

### The near-miss: `high = middle - 1` inside the boundary template

The reflex from yesterday, dropped into today's code:

```python
def broken(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid - 1                # <-- yesterday's habit
        else:
            lo = mid + 1
    return lo

print(broken([2, 4, 4, 4, 7], 7))       # 5   should be 4
print(broken([1, 3, 5, 6], 3))          # 2   should be 1
```

```
5
2
```

It throws away the answer. `mid` was the first True — the very thing being looked for — and
`hi = mid - 1` puts it outside the range. The rule that prevents this: **`- 1` belongs to closed
ranges, never to half-open ones.** In `[lo, hi)`, `hi = mid` already excludes nothing you needed.

### The near-miss: half-open range with `<=`

```python
    lo, hi = 0, len(nums)
    while lo <= hi:                     # <-- yesterday's condition, today's range
```

Now the loop keeps running when `lo == hi == len(nums)`, `mid` becomes `len(nums)`, and
`nums[mid]` raises. Or, in the version where the question never touches the array, it simply hangs.
**The range convention and the loop condition are a set**, exactly as the sentinel and the formula
were a set on [day 037](../day-037-prefix-sums/README.md). Closed `[lo, hi]` goes with `<=` and
`± 1`. Half-open `[lo, hi)` goes with `<` and `hi = mid`. Pick one. Never blend them.

### The real error: forgetting the bounds check after the lower bound

```python
nums = [2, 4, 4, 4, 7]
i = lower_bound(nums, 99)
print(i)                                # 5
print(nums[i] == 99)                    # boom
```

```
5
Traceback (most recent call last):
  File "day43.py", line 4, in <module>
    print(nums[i] == 99)                 # boom
          ~~~~^^^
IndexError: list index out of range
```

The lower bound is a *position*, and the position "one past the end" is a legitimate answer. Any
code that turns a position into a value must check `i < len(nums)` first. This is the price of a
template that never returns `-1`: it hands you an index you must validate.

### The trap that returns a plausible lie: a question that is not monotone

```python
nums = [1, 5, 2, 8, 3]
print(first_true(0, 5, lambda i: nums[i] >= 4))     # 3
```

Index 1 holds 5, which is `>= 4`, so the true answer to "first index whose value is at least 4" is
1. The template says 3. No error, no warning. The template's contract is *monotone question*; this
question is not, so the answer is meaningless. Before you use it, say out loud what the question is
and why it can never flip back — that ten-second check is the same one as yesterday's "is the array
sorted?", and it catches strictly more bugs.

### The subtle one: `lambda i: nums[i] >= target` captures `target`

```python
questions = [lambda i: nums[i] >= t for t in (4, 7)]     # both close over the SAME t
print([lower_bound(nums, 4), lower_bound(nums, 7)])      # fine — passed as arguments
```

Building a list of questions in a loop and expecting each to remember its own `target` is Python's
late-binding closure trap, and it produces two identical questions. It is not a binary search bug,
but it is how people break this template when they try to be clever with it. Pass the target as an
argument, as the code in §5 does, and it cannot happen.

---

## 8. In the interview

### How it gets asked

- *"Write binary search. No IDE."* — and then, thirty seconds later, *"now return the first
  occurrence instead."* The second half is the real question, and it is where the three-way template
  falls over.
- *"Find the position where this value should be inserted to keep the list sorted."* — LeetCode 35,
  the lower bound with no extra code.
- *"How many times does x appear in this sorted array, in better than linear time?"* — upper bound
  minus lower bound, and they are checking whether you say "one subtraction" or start writing a
  scan.
- *"Your loop hangs. Why?"* — a live-debugging prompt. The answer is about `mid` and `hi`, and §6
  has it.

### What to say out loud, in the first ninety seconds

1. **Declare the convention before writing.** *"I'll use a half-open range, low inclusive and high
   exclusive, so high starts at len(nums). That means the loop condition is strictly less-than, and
   I never write minus one."*
2. **Turn the problem into a yes-or-no question.** *"I'm looking for the first index where
   `nums[i] >= target` is true. That question is monotone on a sorted array — once true, always
   true — which is all binary search needs."*
3. **State the invariant.** *"Everything below low answers false, everything from high up answers
   true. When they meet, low is the boundary."*
4. **Say the asymmetry, because it is the bug everyone makes.** *"If the middle answers true I set
   high to middle, not middle minus one — the middle might be the boundary itself. If it answers
   false I set low to middle plus one, because the middle definitely isn't."*
5. **Say what the return value is.** *"It returns a position, always — never minus one. If the
   target is bigger than everything, it returns len(nums), which is the correct insertion point. So
   any caller that wants a value has to check the bound first."*

### The follow-ups

**"Now give me the first and the last occurrence, and tell me the cost."**
Both are this template with one character changed. The first occurrence is the lower bound — the
first index where `nums[i] >= target` — and it is a genuine match only if that index is in range and
holds the target. The last occurrence is the upper bound minus one: the upper bound is the first
index where `nums[i] > target`, so the position just before it is the last copy. Two independent
binary searches, so O(log n) plus O(log n), which is still O(log n), and O(1) space. The reason I'd
do two searches rather than one search plus a walk is the all-duplicates case: on an array of a
million identical values, find-then-walk is O(n) and this stays at forty comparisons. And the count
of copies is the two bounds subtracted, which is worth pointing out because interviewers often
expect a third pass for it.

**"Why does your loop terminate? Convince me."**
Because `mid` is strictly less than `hi` on every pass, and that is not an accident of the input. The
loop only runs while `lo < hi`, so `lo + hi` is strictly less than `2 × hi`, so the floor of
`(lo + hi) / 2` is strictly less than `hi`. That means the assignment `hi = mid` always makes `hi`
smaller. The other branch, `lo = mid + 1`, always makes `lo` bigger, because `mid` is at least `lo`.
So every single pass narrows the range by at least one, and a range of size n cannot narrow more than
n times. It actually halves, so it is log n. The place this argument breaks — and it is worth
mentioning because it is the bug people hit — is if you write `hi = mid` inside a *closed*-range
loop with `lo <= hi`. There `mid` can equal `hi`, the assignment changes nothing, and it hangs
forever. The termination argument belongs to the convention, not to binary search in general.

**"Can you use this when there is no array — say, the input is a function or a stream?"**
Yes, and that is the reason I write it this way. Nothing in the template touches an array; it takes a
range of integers and a question, and the question happens to consult an array today. If the input is
an API that answers "is version i broken?", the same six lines find the first broken version — that
is LeetCode 278, and it is exactly this. If the question is "can all packages ship within d days
using capacity c?", the range becomes the possible capacities and the answer is the smallest c that
works, which is
[day 046](../day-046-binary-search-on-the-answer/README.md). The two things I would check before
using it anywhere are: is the question monotone over the range, and how expensive is one call —
because the cost is log n *questions*, and if each question is an O(n) scan then the total is
O(n log n), not O(log n).

### A model answer

> "Let me set the convention first, because that's where the off-by-one bugs come from. I'll use a
> half-open range: low is inclusive, high is exclusive, so high starts at len(nums) rather than the
> last index. With that convention the loop condition is strictly less-than and I never write a
> minus one anywhere.
>
> Then I turn the problem into a yes-or-no question about a position. For 'find the target' the
> question is: is `nums[i] >= target`? On a sorted array that's monotone — once it's true it stays
> true — and monotone is the only thing binary search actually needs. Sorted is just the usual way
> to get it.
>
> The invariant is: everything below low answers false, everything from high upward answers true, so
> the boundary is inside [low, high).
>
> ```python
> def lower_bound(nums: list[int], target: int) -> int:
>     lo, hi = 0, len(nums)
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if nums[mid] >= target:
>             hi = mid          # mid might be the boundary — keep it
>         else:
>             lo = mid + 1      # mid is definitely not — step past it
>     return lo
> ```
>
> The asymmetry in those two branches is the whole thing. If the middle answers true, the middle
> itself might be the first true, so I keep it by setting high to middle — not middle minus one,
> which is the classic bug and throws away the answer. If it answers false, the middle is ruled out,
> so low goes one past it.
>
> When the loop ends low equals high, and low is the boundary. It always returns a position, never
> minus one, so 'does the target exist' is a check afterwards: `i < len(nums) and nums[i] == target`,
> in that order, because a target above everything gives me len(nums) and indexing that would raise.
>
> That's O(log n) time and O(1) space. And it's worth saying what I get for free: change `>=` to `>`
> and I have the upper bound, so the last occurrence is upper bound minus one and the number of
> copies is upper minus lower. Insertion position is this function unchanged — that's LeetCode 35.
> Five problems, one template, one character. In production I'd call `bisect_left` and
> `bisect_right`, which are exactly these two."

---

## 9. Recall card

- **One template, forever:** half-open `[lo, hi)`, `hi = len(nums)`, `while lo < hi`, `mid` in the
  middle, `question(mid)` → `hi = mid` else `lo = mid + 1`. Return `lo`.
- **The asymmetry is the lesson:** True keeps the middle (`hi = mid`), False steps past it
  (`lo = mid + 1`). `- 1` belongs to closed ranges only; blending the two conventions is the bug.
- **Invariant:** below `lo` all False, from `hi` up all True — so `lo` is the first True, and
  `len(nums)` is the honest answer for "no True at all".
- **Change one character, get five problems:** `>=` is lower bound (first occurrence, insert
  position, exists); `>` is upper bound (last occurrence = upper − 1, count = upper − lower).
  `bisect_left` / `bisect_right` are these two.
- **It needs a monotone question, not a sorted array** — and it returns a *position*, so check
  `i < len(nums)` before reading `nums[i]`. Termination: `mid < hi` always, so `hi = mid` shrinks.
