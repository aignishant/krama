---
day: 34
track: dsa
title: "At-most-K, and the exactly-K trick"
phase: "Two pointers and sliding window"
status: written
---

# Day 034 · DSA — At-most-K, and the exactly-K trick

**After today you can:** You can turn an exactly-K problem into two at-most-K problems and explain the subtraction.

**The interviewer asks it as:** *Count the subarrays with exactly k distinct integers.*

---

## 1. What this is, and why they ask it

Every window so far has answered "what is the **longest**?" or "what is the **shortest**?". Today's
windows answer "**how many**?" — count the subarrays that satisfy a condition, not find the best one.
The counting version has its own one-line trick: **the number of valid subarrays ending at `right` is
the window length**, so you add `right - left + 1` instead of taking a `max`. And when the question
says **exactly k** instead of **at most k**, you do not fight the window — you count *at most k*, count
*at most k − 1*, and subtract.

Interviewers love this family because it looks like yesterday's material and is not. A candidate who
has only memorised the longest-substring skeleton walks straight into it, writes a `max` where a sum
belongs, and produces code that runs cleanly and answers a different question. *Subarrays with K
Different Integers* — LeetCode 992 — is the standard hard version, and *Count Number of Nice
Subarrays* and *Binary Subarrays With Sum* are the same trick asked at medium. The subtraction is the
part they actually want to hear you explain.

---

## 2. The story

Sports day at the school where Shanti has taught for eleven years, and forty children are standing in
one long line on the field, each wearing a house colour — red, blue, yellow or green.

The first game needs a team, and a team is any run of children standing next to each other. The rule
this year is that a team must have children from **exactly two** houses in it. Not one, not three.
The younger teacher, Priya, has been given the job of counting how many different teams are possible,
and she has started badly. She walks the line trying to spot runs with exactly two colours, and she
keeps losing her place, because inside every run that works there are shorter runs that have only one
colour, and runs that start one child earlier suddenly have three.

Shanti watches for a minute and then tells her the trick she always uses. Stop counting the thing you
want. Count something easier, twice.

First, count the runs with **at most two** colours. That one is friendly. Walk the line child by
child, and for each child, work out how far back you can go before a third colour sneaks in. If you
can go back five children, then five teams end at this child — the one of length one, the one of
length two, up to the one of length five. Add five and move on. The nice part, she says, is that the
starting place never moves backwards as you walk forward, so you are never redoing work.

Then count the runs with **at most one** colour, the same way. Even friendlier.

Now subtract. Every run you counted the first time has one colour or two. Every run you counted the
second time has one. What survives the subtraction is the runs with exactly two — which is the number
the game needed, and neither count ever made you think about "exactly" at all.

Priya asks why she cannot just count exactly-two directly. Shanti says: because "too many colours" is
a clean thing to fix — you shrink from the back until it is fixed, and it stays fixed. "Not enough
colours" and "too many colours" at the same time is two jobs, and a walk in one direction does one job
well.

---

## 3. The idea in plain English

Shanti's line of children is the array. A run of children standing together is a **subarray** — from
[day 024](../day-024-substrings-vs-subsequences/README.md), a contiguous slice. Houses are values, and
"how many houses in this run" is how many **distinct** values the window holds — `len(count)`, from
[day 033](../day-033-window-with-a-map/README.md). Today changes only the question: not *how long is
the best window* but *how many windows qualify*.

### Counting at-most-k: the window-length insight

Keep exactly yesterday's window: grow `right`, and shrink from `left` while the window holds more than
`k` distinct values. After the shrink, the window `nums[left..right]` is the **longest** valid window
ending at `right`.

Here is the insight that turns a longest-finder into a counter. Every subarray that **ends at
`right`** and starts at `left` or later is also valid — because dropping elements off the front can
only remove values, never add new distinct ones. And every subarray ending at `right` that starts
*before* `left` is invalid — that is exactly why `left` moved. So the valid subarrays ending at
`right` are:

```
nums[left..right], nums[left+1..right], ..., nums[right..right]
```

and there are `right - left + 1` of them — **the window length**. Add that to a running total at every
step, and the total is the number of valid subarrays anywhere, because every subarray ends somewhere,
and each is counted at the one step where `right` sits on its last element.

One line changes from yesterday:

```python
best = max(best, right - left + 1)     # yesterday: the longest
total += right - left + 1              # today: the count
```

That is Shanti's "if you can go back five children, five teams end here".

### Why exactly-k resists a direct window

Yesterday's shrink loop repairs one kind of wrongness: **too many**. The condition is monotonic —
shrinking always moves you toward valid, and once valid you stop. "Exactly k" is wrong in two
directions at once. A window can have too many distinct values *or too few*, and shrinking a too-many
window can overshoot straight past "exactly k" into "too few". The single `left` boundary cannot serve
both jobs. That is Shanti's "two jobs, one walk".

### The subtraction

So do not count exactly. Count at-most, twice:

```
exactly(k)  =  at_most(k) - at_most(k - 1)
```

The argument is one sentence of set thinking. Every subarray with at most `k` distinct values has
either at most `k − 1` of them, or exactly `k` — those two groups do not overlap, and together they
are everything `at_most(k)` counted. Subtract the first group and the second remains.

For `[1, 2, 1, 2, 3]` and `k = 2`: `at_most(2)` is 12, `at_most(1)` is 5, so `exactly(2)` is
`12 - 5 = 7`. §4 counts all twelve and all five in front of you.

### The same trick beyond distinct counts

"At most" is not about distinct values — it is about any condition where shrinking helps, the
**monotonic** conditions from [day 032](../day-032-variable-window/README.md). Each of these is the
identical skeleton with a different thing counted:

| Problem | "Exactly k" of what | What the window carries |
|---|---|---|
| Subarrays with K Different Integers (992) | distinct values | a count map |
| Count Number of Nice Subarrays (1248) | odd numbers | one integer: odds in the window |
| Binary Subarrays With Sum (930) | ones (the sum) | one integer: the window sum |
| Subarray Product Less Than K (713) | — already an at-most question | one integer: the product |

The last row is the gift version: the question already says "less than k", so there is no subtraction
at all — just the counting window. And rows two and three show
[day 033](../day-033-window-with-a-map/README.md)'s observation again: when the property tracks one
kind of thing, the map collapses to a single integer.

### The one guard the subtraction needs

`exactly(k)` calls `at_most(k - 1)`. When `k` is 0 — or the target sum is 0 in problem 930 — that
inner call receives **−1**, and no window has at most −1 of anything. The function must return 0 for a
negative `k`, and §7 shows what happens when it does not. It is one `if` at the top, and forgetting it
is the most common way this family goes wrong.

---

## 4. The picture

Counting `at_most(2)` on `[1, 2, 1, 2, 3]` — watch the running total, not a best:

```
 index   0    1    2    3    4
       +----+----+----+----+----+
 value |  1 |  2 |  1 |  2 |  3 |
       +----+----+----+----+----+

 right  window after shrink   left   adds   subarrays ending here
 -----  -------------------   ----   ----   ------------------------------
   0    [1]                    0      1     [1]
   1    [1,2]                  0      2     [2] [1,2]
   2    [1,2,1]                0      3     [1] [2,1] [1,2,1]
   3    [1,2,1,2]              0      4     [2] [1,2] [2,1,2] [1,2,1,2]
   4    [2,3]                  3      2     [3] [2,3]
                                     ----
                                      12   =  at_most(2)
```

**What to notice:** at `right = 4`, the value 3 arrives, the window briefly holds three distinct
values, and `left` walks from 0 to 3 to repair it. The two subarrays counted there start at or after
`left` — everything starting earlier would still contain all three values, which is exactly why
`left` moved past it.

The same array, `at_most(1)`:

```
 right  window   left   adds        (only single-value runs survive)
   0    [1]       0      1
   1    [2]       1      1
   2    [1]       2      1
   3    [2]       3      1
   4    [3]       4      1
                        ----
                          5   =  at_most(1)
```

And the subtraction, as two nested boxes:

```
   +--------------------------------------------------+
   |  at_most(2)  =  12 subarrays                     |
   |                                                  |
   |   +------------------------+                     |
   |   |  at_most(1) = 5        |   the ring between  |
   |   |  (one distinct value)  |   the boxes is      |
   |   +------------------------+   exactly(2) = 7    |
   +--------------------------------------------------+

   12 - 5 = 7:  [1,2] [2,1] [1,2,1] [2,1,2] [1,2,1,2] [1,2] [2,3]
```

**What to notice:** the inner box sits entirely inside the outer one — every one-colour run is also an
at-most-two-colours run. That containment is what makes the subtraction legal. Subtracting two counts
that overlap only partially would be meaningless.

---

## 5. The code, built step by step

### The counting window

```python
def at_most_k_distinct(nums: list[int], k: int) -> int:
    if k < 0:
        return 0
    count: defaultdict[int, int] = defaultdict(int)
    left = 0
    total = 0
```

The guard comes first, because `exactly` is about to call this with `k - 1`. An at-most-minus-one
window can never exist, so the count is 0.

```python
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]
            left += 1
        total += right - left + 1
    return total
```

Yesterday's skeleton, line for line — including the `del` at zero, which is mandatory here for
yesterday's reason: `len(count)` is the condition. The only new line is the last one. After the
shrink, `nums[left..right]` is the longest valid window ending at `right`, and every later start also
works, so `right - left + 1` subarrays end here. No `max`, no `best`.

### The subtraction

```python
def exactly_k_distinct(nums: list[int], k: int) -> int:
    return at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)
```

Two passes over the array, one subtraction. This two-line function is the answer to a problem
LeetCode marks **hard**.

### Nice subarrays: the map collapses

*Count Number of Nice Subarrays* — LeetCode 1248 — asks for subarrays with exactly `k` **odd**
numbers. Odd or even is two kinds of thing, so the map collapses to one integer, as in
[day 033](../day-033-window-with-a-map/README.md):

```python
def at_most(nums: list[int], k: int) -> int:
    if k < 0:
        return 0
    left = odds = total = 0
    for right, x in enumerate(nums):
        odds += x % 2
        while odds > k:
            odds -= nums[left] % 2
            left += 1
        total += right - left + 1
    return total
```

`x % 2` is 1 for odd and 0 for even, so `odds` is a count of odd values in the window. Everything
else is unchanged.

### Binary subarrays with sum: the same collapse

*Binary Subarrays With Sum* — LeetCode 930 — counts subarrays of 0s and 1s summing to exactly
`goal`. The sum of 0s and 1s *is* a count of 1s, so this is the previous problem wearing different
clothes — and here the `goal = 0` case makes the negative guard load-bearing, because
`exactly(0)` calls `at_most(-1)`.

### Product less than k: no subtraction needed

*Subarray Product Less Than K* — LeetCode 713 — is already an at-most question, with one edge of its
own:

```python
def num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0
    left = total = 0
    product = 1
    for right, x in enumerate(nums):
        product *= x
        while product >= k:
            product //= nums[left]
            left += 1
        total += right - left + 1
    return total
```

The guard is `k <= 1` this time. The values are positive integers, so every window's product is at
least 1, and "product strictly less than 1" can never be satisfied — without the guard the shrink
loop runs off the end of the array. §7 has the crash.

### The complete solutions

```python
from collections import defaultdict


def at_most_k_distinct(nums: list[int], k: int) -> int:
    """Count subarrays holding at most k distinct values. The guard feeds exactly()."""
    if k < 0:
        return 0
    count: defaultdict[int, int] = defaultdict(int)
    left = 0
    total = 0
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]        # len(count) is the condition: del is mandatory
            left += 1
        total += right - left + 1            # every start from left to right works
    return total


def exactly_k_distinct(nums: list[int], k: int) -> int:
    """LeetCode 992. The whole trick."""
    return at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)


def number_of_nice_subarrays(nums: list[int], k: int) -> int:
    """LeetCode 1248. Exactly k odd numbers: the map collapses to one integer."""
    def at_most(k: int) -> int:
        if k < 0:
            return 0
        left = odds = total = 0
        for right, x in enumerate(nums):
            odds += x % 2
            while odds > k:
                odds -= nums[left] % 2
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)


def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
    """LeetCode 930. Sum of 0s and 1s is a count of 1s; goal = 0 needs the guard."""
    def at_most(goal: int) -> int:
        if goal < 0:
            return 0
        left = window_sum = total = 0
        for right, x in enumerate(nums):
            window_sum += x
            while window_sum > goal:
                window_sum -= nums[left]
                left += 1
            total += right - left + 1
        return total

    return at_most(goal) - at_most(goal - 1)


def num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
    """LeetCode 713. Already an at-most question; k <= 1 can never be satisfied."""
    if k <= 1:
        return 0
    left = total = 0
    product = 1
    for right, x in enumerate(nums):
        product *= x
        while product >= k:
            product //= nums[left]
            left += 1
        total += right - left + 1
    return total


if __name__ == "__main__":
    print(exactly_k_distinct([1, 2, 1, 2, 3], 2))                    # 7
    print(exactly_k_distinct([1, 2, 1, 3, 4], 3))                    # 3

    print(number_of_nice_subarrays([1, 1, 2, 1, 1], 3))              # 2
    print(number_of_nice_subarrays([2, 4, 6], 1))                    # 0
    print(number_of_nice_subarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2))  # 16

    print(num_subarrays_with_sum([1, 0, 1, 0, 1], 2))                # 4
    print(num_subarrays_with_sum([0, 0, 0, 0, 0], 0))                # 15  <- the guard at work

    print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))      # 8
    print(num_subarray_product_less_than_k([1, 2, 3], 0))            # 0
```

Run it. Eight answers, all correct, including the two edge rows the guards exist for.

---

## 6. What it costs

### One at-most pass

The counting window is [day 032](../day-032-variable-window/README.md)'s argument unchanged: `right`
advances exactly `n` times, `left` only ever advances and never passes `right`, so at most `n` moves.
At most `2n` pointer moves, each with constant map work. **O(n) time.** Space is the map:
**O(k)** entries at most — and O(1) when the map has collapsed to an integer.

### The subtraction doubles it, and no more

`exactly(k)` runs the pass twice:

```
at_most(k)     : up to 2n moves
at_most(k - 1) : up to 2n moves
total          : 4n moves            -> still O(n)
```

Two passes is a constant factor, not a complexity change — the same distinction
[day 033](../day-033-window-with-a-map/README.md) drew for `max_freq`. Say "two linear passes" and
nobody will blink.

### Against the brute force

Counting by checking every subarray: `n(n+1)/2` subarrays, and checking the distinct count of each
from scratch costs up to `O(n)` more:

```
n = 10,000:   brute  ≈ 50,000,000 subarrays × up to 10,000 each ≈ 5 × 10¹¹ ops
              window ≈ 40,000 pointer moves
```

Even the smarter brute force — fix the start, extend the end, grow a set as you go — is
`n²/2 = 50,000,000` steps against 40,000. That is the gap the interviewer wants named.

### The number to have ready

> Two at-most passes, each `O(n)` because both pointers only move forward, then one subtraction —
> `O(n)` time, `O(k)` space for the map. The brute force enumerates `n²/2` subarrays, which at
> `n = 10,000` is fifty million against forty thousand pointer moves.

---

## 7. The traps

### The near-miss: `max` where the sum belongs

Yesterday's reflex, applied to today's question:

```python
while len(count) > k:
    ...
best = max(best, right - left + 1)      # counting problem, longest-window line
```

On `[1, 2, 1, 2, 3]` with `k = 2` this returns **4** — the length of `[1,2,1,2]` — when the question
asked for the count 7. It runs, it looks like every window you have ever written, and it answers the
wrong question. **Read the ask: "how many" means `total +=`, "longest" means `max`.** Say which one
you are doing before you type it.

### The near-miss: at-most where exactly was asked

The counting window alone, with `len(count) > k` as the condition, happily returns 12 for
`[1, 2, 1, 2, 3]`, `k = 2` — the at-most count, not the exactly count of 7. Nothing crashes. The
tell is in your own test: build one tiny example by hand, count the qualifying subarrays with your
eyes, and 12 against 7 exposes it immediately. This is why the two-minute hand-count is not optional.

### The real error: the missing negative guard

`exactly(0)` — or `goal = 0` in Binary Subarrays With Sum — calls `at_most(-1)`. Without the guard,
the shrink loop can never be satisfied: the window sum is always at least 0, which is greater than
−1, so `left` marches past `right`, keeps subtracting elements it never should, and runs off the end:

```
Traceback (most recent call last):
  File "day34.py", line 20, in <module>
    print(at_most([0, 0, 1, 0], 0) - at_most([0, 0, 1, 0], -1))
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "day34.py", line 14, in at_most
    window_sum -= nums[left]
                  ~~~~^^^^^^
IndexError: list index out of range
```

One line prevents it: `if goal < 0: return 0`. And note the sneakier variant: add a `left <= right`
guard to the `while` instead, and the crash disappears but the counting silently continues with an
empty window — plausible numbers, wrong answer, no traceback.

### The real error: product less than 1

The same failure wears a second costume in LeetCode 713. Positive integers mean every product is at
least 1, so `k = 1` can never be satisfied and the shrink loop eats the whole array:

```python
print(count([1, 1, 1], 1))       # no k <= 1 guard
```

```
Traceback (most recent call last):
  File "day34.py", line 14, in <module>
    print(count([1, 1, 1], 1))
  File "day34.py", line 9, in count
    product //= nums[left]
IndexError: list index out of range
```

And on `[2, 3]` with `k = 1` the same code does not crash — it returns **−1**. A count of minus one
subarrays, delivered with a straight face. `right - left + 1` goes negative once `left` passes
`right`, and the total absorbs it silently. **Guard `k <= 1` with `return 0`.**

### The near-miss: forgetting the `del`, again

The condition is `len(count) > k`, so [day 033](../day-033-window-with-a-map/README.md)'s rule
applies with full force: decrement, then delete at zero. Leave zero entries behind and `len(count)`
counts ghosts, the shrink loop overshrinks, and every window's contribution is too small. The count
comes out wrong with no error — and because it is a count, not a length, you cannot eyeball it from
the output the way you could spot a too-short "longest".

### The contract corner: what exactly counts

Ask what `k = 0` should return — for distinct values it is 0 by convention, for a sum it is a real
question with real subarrays answering it, as `[0,0,0,0,0]` with `goal = 0` returning 15 shows. And
confirm whether "integers" can be negative: for *distinct counts* negatives change nothing, but the
moment the condition is a **sum** of arbitrary integers, monotonicity dies —
[day 032](../day-032-variable-window/README.md)'s rule — and this whole family hands over to prefix
sums, which arrive on [day 038](../day-038-subarray-sum-k/README.md).

---

## 8. In the interview

### How it gets asked

- *"Count the subarrays with exactly k distinct integers."* — LeetCode 992, marked hard, and two
  lines once you own the trick.
- *"Count the subarrays containing exactly k odd numbers."* — LeetCode 1248, the same problem after
  one observation.
- *"How many subarrays of this 0/1 array sum to the target?"* — LeetCode 930, where the target 0 edge
  hides.
- *"Count the subarrays whose product is under 100."* — LeetCode 713, the version with no subtraction
  needed.
- And the follow-up form: you solve "longest with at most k distinct", and the interviewer leans in —
  *"now count the subarrays with exactly k."*

### What to say out loud, in the first ninety seconds

1. **Name the shift.** *"This is a counting question, not a longest question — so I'll accumulate,
   not take a max."*
2. **State the counting insight.** *"With an at-most window, after the shrink, every subarray ending
   at `right` and starting at or after `left` is valid — that's `right - left + 1` new subarrays per
   step, because removing elements from the front can never add distinct values."*
3. **Explain why exactly resists.** *"Exactly-k is wrong in two directions — too many and too few —
   and one left boundary can only repair one of them."*
4. **Give the subtraction.** *"So: subarrays with at most k, minus subarrays with at most k − 1.
   Those with at most k − 1 sit entirely inside those with at most k, so the difference is exactly
   k."*
5. **Flag the guard.** *"at_most(k − 1) gets −1 when k is 0, and my helper returns 0 for negative k —
   otherwise the shrink loop runs off the array."*
6. **Give the costs.** *"Two linear passes and a subtraction — O(n) time, O(k) space for the map."*

### The follow-ups

**"Why is the number of valid subarrays ending at `right` equal to the window length?"**
Because validity here survives shortening. After the shrink, `nums[left..right]` has at most `k`
distinct values. Any subarray ending at `right` that starts later than `left` is that window with
elements removed from the front — and removing elements can only lose values, never introduce new
ones, so its distinct count is at most the window's. That gives one valid subarray per start position
from `left` to `right`: `right - left + 1` of them. And nothing starting before `left` qualifies,
because `left` only moved when the window holding those elements exceeded `k`. Both halves matter —
the count is not just an upper bound, it is exact — and the property doing the work is monotonicity:
the condition can only improve as the window shortens. A condition without that property, say "the
window's maximum minus minimum is exactly 5", would not let me count this way.

**"Can you do exactly-k in one pass instead of two?"**
Yes — keep two left boundaries over the same walk. `left1` is the tightest start with at most `k`
distinct values, `left2` the tightest with at most `k − 1`; every start in between gives exactly `k`,
so each step adds `left2 - left1`. It is one pass with two maps, against two passes each with one —
the same total work, `O(n)` either way, so it is a constant-factor rearrangement rather than an
improvement. I would write the subtraction version in an interview: two calls to a helper I have
already tested, one line of arithmetic, and far less state to get wrong under pressure. I would name
the three-pointer version only to show I know the trade I am making.

**"What if the array contains negative numbers?"**
For distinct-count conditions, nothing changes — distinctness does not care about sign, and the
monotonicity that justifies the counting still holds. But if the condition is a *sum* — count the
subarrays summing to exactly `k` over arbitrary integers — the trick dies, because with negatives a
window's sum does not shrink as the window shrinks, so "at most" is no longer a monotonic condition
and the two-boundary walk is unjustified. That is day 032's rule surfacing again. The right tool
there is a prefix-sum map — count, for each position, how many earlier prefix totals differ from the
current one by exactly `k` — which is O(n) with a hash map and handles negatives natively. That
technique is a few days ahead of me in this course, but I would name it as the correct escape hatch.

### A model answer

> "Count the subarrays with exactly k distinct integers — this is a counting problem, so I will not be
> taking a max of window lengths; I will accumulate a total.
>
> The direct version is awkward, because 'exactly k' can be violated in two directions — too many
> distinct values or too few — and a sliding window's left edge only knows how to repair 'too many'.
> So I'll use the standard decomposition: the answer is the number of subarrays with at most k
> distinct values, minus the number with at most k − 1. Every at-most-(k−1) subarray is also an
> at-most-k subarray, so the subtraction leaves exactly the exactly-k ones.
>
> Counting at-most is where the window earns its keep. I grow `right`, shrink while the map holds
> more than k distinct values, and then every subarray ending at `right` starting anywhere from
> `left` onward is valid — shortening from the front can only remove values. So each step contributes
> the window length, `right - left + 1`.
>
> ```python
> def at_most(nums, k):
>     if k < 0:
>         return 0
>     count, left, total = defaultdict(int), 0, 0
>     for right, x in enumerate(nums):
>         count[x] += 1
>         while len(count) > k:
>             count[nums[left]] -= 1
>             if count[nums[left]] == 0:
>                 del count[nums[left]]
>             left += 1
>         total += right - left + 1
>     return total
>
> def exactly_k(nums, k):
>     return at_most(nums, k) - at_most(nums, k - 1)
> ```
>
> Two details are load-bearing. The `k < 0` guard: `exactly(0)` calls `at_most(-1)`, and without the
> guard the shrink loop can never be satisfied and walks off the array. And the `del` when a count
> hits zero, because `len(count)` is the loop condition — leave ghosts behind and it overshrinks.
>
> Cost: each pass is O(n) — both pointers only move forward, at most 2n moves — so two passes and a
> subtraction is O(n) time, O(k) space. On [1,2,1,2,3] with k = 2: at-most-2 is 12, at-most-1 is 5,
> answer 7 — and I'd check that little example by hand before trusting the code."

---

## 9. Recall card

- **Counting window: `total += right - left + 1`** — after the shrink, every start from `left` to
  `right` gives a valid subarray ending here.
- **Why it works: shortening never hurts** — removing front elements cannot add distinct values.
  Monotonicity is the licence to count this way.
- **`exactly(k) = at_most(k) - at_most(k - 1)`** — at-most-(k−1) nests inside at-most-k, so the
  difference is exactly-k. Two linear passes, still `O(n)`.
- **Guard the inner call: negative k returns 0** — else `at_most(-1)` walks off the array
  (`IndexError`), and product-less-than-k needs `k <= 1 → 0` for the same reason.
- **"How many" → accumulate; "longest" → max.** Say which before typing. And sums with negatives
  break the trick — that is prefix sums, [day 038](../day-038-subarray-sum-k/README.md).
