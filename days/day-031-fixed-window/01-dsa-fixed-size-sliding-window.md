---
day: 31
track: dsa
title: "Fixed-size sliding window"
phase: "Two pointers and sliding window"
status: written
---

# Day 031 · DSA — Fixed-size sliding window

**After today you can:** You can answer every window-of-size-k question in O(n) instead of O(n*k).

**The interviewer asks it as:** *Find the maximum sum of any subarray of size k.*

---

## 1. What this is, and why they ask it

A **sliding window** is a range of fixed width `k` that moves along the array one position at a time.
The whole technique is one observation:

> **Consecutive windows overlap in `k - 1` elements. So do not recompute — adjust.**

When the window moves one step right, exactly one element enters on the right and exactly one leaves
on the left. Everything else is unchanged. So instead of adding up `k` numbers again, you add the
entering one and subtract the leaving one: two operations instead of `k`.

That turns `O(n × k)` into `O(n)`, and the saving grows with `k`. On 100,000 elements with `k = 1,000`,
the brute force does about 100 million additions and the window does 200,000.

This is the same family as the two-pointer work of the last four days — the window is two indices
moving in the same direction — but the mental model is different enough to be worth its own day: you
think about *the range between them* rather than about the two indices. That reframing is what makes
tomorrow's variable-size windows possible.

Interviewers ask it because the brute force is obvious and the improvement is a genuine insight, and
because the follow-ups are excellent. *"Now find the maximum in each window"* is not a small change —
a sum can be adjusted by arithmetic and a maximum cannot, and the answer needs a data structure. That
follow-up, LeetCode 239, is a hard problem sitting one sentence away from an easy one.

---

## 2. The story

The Sunday match on the ground behind the water tank is a serious business, and Prasad has kept the
score for it for six years. He sits on a plastic chair under the one tree with the book on his knee
and he does not miss a ball.

The thing people ask him, every single week, is what the run rate has been over the last five overs.
It matters — it is how the captain decides whether to push or hold — and somebody shouts it up to him
about twice an hour.

For the first season he did it the obvious way. Somebody asked, and he added the last five overs and
divided. Eight, four, eleven, six, nine. Thirty-eight. Seven point six. It took maybe twenty seconds,
and he was doing it from scratch every single time, so by the fortieth over he had added up the same
numbers over and over.

What he does now takes him about two seconds and he does it without stopping watching the game.

He carries one number in his head: the total for the last five overs. When an over finishes, he adds
that over's runs to the number, and then he takes away the runs from the over that has just dropped
out of the five — the one that is now six back. Add one, take away one, and the number in his head is
correct again.

Somebody asks, he divides by five, done.

The part he had to get right, and got wrong twice in his first month, is *which* over drops out. After
the twelfth over finishes, the last five are eight, nine, ten, eleven and twelve — so the one leaving
is the seventh, not the eighth. He counts back five from the one that just went in. He says once you
have made that mistake in front of forty people you do not make it again.

There is one question he still cannot do this way, and it annoys him. Sometimes they ask for the
**biggest** over in the last five, not the total. Adding and subtracting does not work for that — if
the over that drops out happened to be the biggest one, the new biggest could be any of the other
four, and he has to look at them. So for that one he still looks.

---

## 3. The idea in plain English

Prasad's number is the window sum. Adding the new over and subtracting the one that dropped out is the
slide. And the question he cannot answer that way is §5's hard follow-up, which needs a structure
rather than arithmetic.

### The core move

```python
total = sum(nums[:k])          # build the first window
best = total
for i in range(k, len(nums)):
    total += nums[i] - nums[i - k]     # add entering, remove leaving
    best = max(best, total)
return best
```

Six lines. The whole technique is the one arithmetic line in the middle.

### The index that leaves — the part people get wrong

When `nums[i]` enters, **`nums[i - k]` leaves.**

Work it out on a small case rather than remembering it. With `k = 3` and the window currently covering
indices 0, 1, 2: bringing in index 3 must push out index 0, and `3 - 3 = 0`. Correct. Now index 4
enters and index 1 leaves: `4 - 3 = 1`. Correct.

That is Prasad counting back five from the over that just went in. `i - k`, not `i - k + 1` and not
`i - k - 1`.

After the line runs, the window covers `nums[i - k + 1 .. i]`, which is `k` elements. **State that
range out loud when you write the loop** — it is the fastest way to check yourself.

### Why the loop starts at `k`

The first `k` elements form the first window, and it is built before the loop by `sum(nums[:k])`. The
loop then produces windows 2, 3, 4 and so on, so it starts at index `k`. Starting at 0 or 1 either
double-counts or produces a window of the wrong size, and both are silent.

### Why it is `O(n)`

Each element enters the window exactly once and leaves exactly once. So across the whole run there are
`n` additions and `n` subtractions — `2n` operations regardless of `k`.

**The brute force is `O(n × k)`** because it recomputes all `k` elements at each of the roughly `n`
positions, and it re-adds each overlapping element `k` times.

Say it as: *"the windows overlap in `k - 1` elements, so recomputing throws away almost all the work
you just did."*

### What can be maintained incrementally, and what cannot

This is the real content of the day, and it decides which follow-up you can answer.

| Quantity | Maintainable in `O(1)` per slide? | Why |
|---|---|---|
| **sum** | yes | add and subtract are exact inverses |
| **average** | yes | it is the sum ÷ `k` |
| **count of a value** | yes | increment and decrement a counter |
| **set of distinct values** | yes, with a count map | decrement, and delete the key at zero |
| **whether a duplicate exists** | yes, with a set | add entering, discard leaving |
| **maximum / minimum** | **no** | removing the maximum tells you nothing about the next one |

**Subtraction only works when the operation has an inverse.** Addition does; `max` does not. If the
element leaving was the maximum, the new maximum could be any of the remaining `k - 1`, and you have
thrown away the information needed to know which. That is exactly Prasad's complaint.

### The maximum, and the monotonic deque

The fix for `max` is to keep a **deque** — a double-ended queue, from
[day 074](../day-074-deques-and-window-max/README.md) — holding **indices**, arranged so that their values
are decreasing from front to back.

```python
while dq and nums[dq[-1]] <= x:
    dq.pop()                    # anything smaller than x can never be the max again
dq.append(i)
if dq[0] <= i - k:
    dq.popleft()                # the front has fallen out of the window
```

Two rules, and both have a one-line reason.

**Pop from the back while the back is smaller than the entering value.** Those elements are both older
*and* smaller than `x`, so `x` outlives them and beats them — they can never be the maximum of any
future window. Discard them for good.

**Pop from the front when it has fallen out of the window.** The front holds the largest value; if its
index is `<= i - k`, it is no longer inside.

Then **`nums[dq[0]]` is the maximum of the current window**, always, because the deque holds exactly
the elements that could still be a maximum, in decreasing order.

Each index is pushed once and popped at most once, so the total work is `O(n)` even though there is a
`while` inside a `for`. **That is the argument to give**, and it is the same "count the travel, not the
nesting" reasoning as [day 023](../day-023-palindromes/README.md).

### The counting variants

When the window's content matters rather than its sum, carry a `Counter` and update two entries:

```python
window[s[i]] += 1                    # entering
left = s[i - k]
window[left] -= 1                    # leaving
if window[left] == 0:
    del window[left]                 # delete at zero, or the comparison fails
```

**The `del` is not optional.** `Counter({'a': 1, 'b': 0})` does not equal `Counter({'a': 1})`, so
leaving zero-count keys behind makes every comparison fail. This is the single most common bug in
window-plus-map problems, and it is why *Find All Anagrams* — LeetCode 438 — catches people.

---

## 4. The picture

The window sliding, and what changes:

```
  nums   2    1    5    1    3    2        k = 3
       +----+----+----+----+----+----+
       |  2 |  1 |  5 |  1 |  3 |  2 |
       +----+----+----+----+----+----+
       |<------ 8 ----->|                  first window: 2+1+5 = 8

            |<------ 7 ----->|             +1 (enters), -2 (leaves)  ->  8 + 1 - 2 = 7
                             ^        ^
                          leaves    enters

                 |<------ 9 ----->|        +3, -1  ->  7 + 3 - 1 = 9

                      |<------ 6 ---->|    +2, -5  ->  9 + 2 - 5 = 6

  best = 9
  Each step: TWO operations, not three. With k = 1000: two, not a thousand.
```

**What to notice:** the two shaded elements at each step are all that changed. Everything in the
overlap was already counted and is left alone — that is the entire idea.

The index bookkeeping, which is where the bugs are:

```
   i enters   ->   i - k leaves      window afterwards is [i-k+1 .. i]

   k = 3:
   i = 3 enters,  0 leaves    window = [1, 2, 3]
   i = 4 enters,  1 leaves    window = [2, 3, 4]
   i = 5 enters,  2 leaves    window = [3, 4, 5]
                                       ^^^^^^^^^  always exactly k = 3 wide
```

The monotonic deque, on `[1, 3, -1, -3, 5, 3, 6, 7]` with `k = 3`:

```
  i=0  x=1    deque empty        push 0        dq: [0]        values (1)
  i=1  x=3    back is 1 <= 3     pop 0, push 1 dq: [1]        values (3)
  i=2  x=-1   back is 3 > -1     push 2        dq: [1,2]      values (3,-1)   -> max 3
  i=3  x=-3   back is -1 > -3    push 3        dq: [1,2,3]    values (3,-1,-3)-> max 3
  i=4  x=5    pop 3, pop 2, pop 1              dq: [4]        values (5)      -> max 5
  i=5  x=3    back is 5 > 3      push 5        dq: [4,5]      values (5,3)    -> max 5
  i=6  x=6    pop 5, pop 4       push 6        dq: [6]        values (6)      -> max 6
  i=7  x=7    pop 6, push 7      dq: [7]                                      -> max 7

  answers: [3, 3, 5, 5, 6, 7]
```

**What to notice at `i = 4`:** three indices are popped at once, and that looks expensive. It is not,
because each of those was pushed exactly once and can only be popped once — across the whole run there
are `n` pushes and at most `n` pops. **Count the pushes, not the loop nesting.**

And notice what the deque holds: at any moment, exactly the elements that are still *candidates* to be
a future maximum. Anything both older and smaller than something else is gone for good.

---

## 5. The code, built step by step

### Building the first window

```python
if k <= 0 or len(nums) < k:
    return None
total = sum(nums[:k])
best = total
```

The guard first — a window bigger than the array has no answer, and asking for one is a real test
case. `sum(nums[:k])` builds window one; `best` starts as that rather than as `0`, for the same reason
trackers never start at zero on [day 014](../day-014-single-pass-habit/README.md): the array may be
all negative.

### The slide

```python
for i in range(k, len(nums)):
    total += nums[i] - nums[i - k]
    best = max(best, total)
return best
```

`range(k, ...)` because windows 2 onwards start when index `k` enters. The single arithmetic line is
the technique. Writing it as `total += nums[i] - nums[i - k]` rather than two statements makes the
"one in, one out" symmetry visible, which helps you check it.

### Maximum average — the same thing with a division at the end

```python
return best / k
```

Divide **once, at the end**, not inside the loop. Dividing each window introduces floating-point error
`n` times and buys nothing, because dividing every candidate by the same positive constant does not
change which is largest.

### Maximum of each window: the deque version

```python
from collections import deque

dq: deque[int] = deque()      # holds INDICES, values decreasing front to back
out: list[int] = []
```

Indices and not values, because you need to know when something falls out of the window, and only the
index tells you that.

```python
for i, x in enumerate(nums):
    while dq and nums[dq[-1]] <= x:
        dq.pop()
    dq.append(i)
```

*Anything at the back that is smaller than or equal to the entering value is finished* — it is older
and smaller, so `x` beats it in every window they could both be in. `<=` rather than `<` also discards
equal values, which is fine and keeps the deque smaller.

```python
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        out.append(nums[dq[0]])
```

The front is the maximum. Remove it if it has aged out; record an answer once the first full window
exists, which is from index `k - 1`.

### Duplicate within distance k

```python
seen: set[int] = set()
for i, x in enumerate(nums):
    if i > k:
        seen.discard(nums[i - k - 1])
    if x in seen:
        return True
    seen.add(x)
return False
```

Here the window is `k + 1` wide, because "within distance `k`" means indices `i - k` to `i`
inclusive — so the element leaving is at `i - k - 1`. **Read the problem's definition of the window
before choosing the index**; LeetCode 219 is off by one from the sum problems for exactly this reason.

`discard` rather than `remove`, because `remove` raises when the element is absent and duplicates in
the array make that possible.

### Anagram windows: window plus a Counter

```python
need = Counter(p)
window = Counter(s[:len(p)])
out = [0] if window == need else []

for i in range(len(p), len(s)):
    window[s[i]] += 1
    left = s[i - len(p)]
    window[left] -= 1
    if window[left] == 0:
        del window[left]
    if window == need:
        out.append(i - len(p) + 1)
```

The `del` at zero is mandatory, as above. And the recorded index is `i - len(p) + 1`, the **start** of
the window, not `i`.

Comparing two `Counter`s of at most 26 keys is constant work, so this stays `O(n)`.

### The complete solutions

```python
from collections import Counter, deque


def max_sum_of_size_k(nums: list[int], k: int) -> int | None:
    """Maximum sum of any window of exactly k elements. O(n) time, O(1) space."""
    if k <= 0 or len(nums) < k:
        return None
    total = sum(nums[:k])              # window 1
    best = total                       # never start at 0 — values may be negative
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]  # i enters, i-k leaves
        best = max(best, total)
    return best


def max_average_of_size_k(nums: list[int], k: int) -> float:
    """LeetCode 643. Divide once, at the end."""
    total = sum(nums[:k])
    best = total
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        best = max(best, total)
    return best / k


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """LeetCode 239. Maximum of every window. O(n) time, O(k) space.

    The deque holds INDICES whose values decrease from front to back —
    exactly the elements that could still be a future maximum.
    """
    dq: deque[int] = deque()
    out: list[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                   # older AND smaller: can never win again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()               # the front has aged out of the window
        if i >= k - 1:
            out.append(nums[dq[0]])    # the front is the window maximum
    return out


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """LeetCode 219. A duplicate within index distance k. Window is k+1 wide."""
    seen: set[int] = set()
    for i, x in enumerate(nums):
        if i > k:
            seen.discard(nums[i - k - 1])   # note: k+1 wide, so i-k-1 leaves
        if x in seen:
            return True
        seen.add(x)
    return False


def find_anagrams(s: str, p: str) -> list[int]:
    """LeetCode 438. Start indices of every anagram of p inside s."""
    if len(p) > len(s):
        return []
    need = Counter(p)
    window = Counter(s[:len(p)])
    out: list[int] = [0] if window == need else []

    for i in range(len(p), len(s)):
        window[s[i]] += 1
        left = s[i - len(p)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]           # MANDATORY: a zero entry breaks equality
        if window == need:
            out.append(i - len(p) + 1)  # the START of the window
    return out


if __name__ == "__main__":
    print([max_sum_of_size_k(a, k) for a, k in
           (([2, 1, 5, 1, 3, 2], 3), ([2, 3, 4, 1, 5], 2), ([1], 1),
            ([1, 2], 3), ([-1, -2, -3], 2))])
    # [9, 7, 1, None, -3]

    print(max_average_of_size_k([1, 12, -5, -6, 50, 3], 4))     # 12.75

    print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))    # [3, 3, 5, 5, 6, 7]
    print(max_sliding_window([1], 1), max_sliding_window([9, 11], 2))   # [1] [11]

    print([contains_nearby_duplicate(a, k) for a, k in
           (([1, 2, 3, 1], 3), ([1, 0, 1, 1], 1), ([1, 2, 3, 1, 2, 3], 2))])
    # [True, True, False]

    print(find_anagrams("cbaebabacd", "abc"))     # [0, 6]
    print(find_anagrams("abab", "ab"))            # [0, 1, 2]
    print(find_anagrams("a", "ab"))               # []
```

---

## 6. What it costs

### The sum version

Building the first window is `k` additions. The loop then runs `n - k` times, each doing one addition,
one subtraction and one comparison — constant work.

```
k + 3(n - k) operations  ->  O(n) time
```

Space: `total` and `best`. **O(1) extra space.**

### Against the brute force

Recomputing each window is `k` additions at each of `n - k + 1` positions:

```
(n - k + 1) × k  ->  O(n × k)
```

Measured, on random arrays:

```
n =  10,000  k =   100   window 0.00170 s   brute 0.0108 s    6x
n =  50,000  k =   500   window 0.00911 s   brute 0.1901 s   21x
n = 100,000  k = 1,000   window 0.01722 s   brute 0.7111 s   41x
```

**The ratio grows with `k`, exactly as `O(n·k)` versus `O(n)` predicts** — roughly 6, 21, 41 as `k`
goes 100, 500, 1,000.

An honest note worth making in an interview: the brute-force numbers here use Python's `sum()` on a
slice, which runs as compiled C. A hand-written inner loop would be several times slower again, so the
*true* gap between the two ideas is larger than the measured one. The operation counts are the honest
comparison: at `n = 100,000` and `k = 1,000`, that is about **100 million** element additions against
**200,000**.

### `max_sliding_window`

The `while` inside the `for` looks like it could be quadratic and is not. **Each index is appended
exactly once and popped at most once**, so across the entire run there are at most `n` pushes and `n`
pops. Total **O(n) time**.

Space: the deque holds at most `k` indices, so **O(k)**.

Against the naive version — `max(nums[i:i+k])` at every position — which is `O(n × k)`:

```
n = 100,000, k = 1,000:
  naive : ~100,000,000 comparisons
  deque : ~200,000 deque operations
```

There is a middle answer worth naming: a **max-heap** of size `k` gives `O(n log k)`, which is better
than `O(n·k)` and worse than `O(n)`, and it needs extra work to remove elements that have aged out.
Heaps arrive on [day 113](../day-113-the-heap/README.md). **Mention it, then give the deque.**

### The counting variants

`find_anagrams` does two `Counter` updates per step and one comparison of two dictionaries with at most
26 keys — all constant. **O(n) time, O(1) space** for a bounded alphabet, `O(k)` in general.

`contains_nearby_duplicate` is one set add, one discard and one membership test per step: **O(n) time,
O(k) space** for the window's worth of values.

### The number to have ready

> Windows of size `k` overlap in `k - 1` elements, so recomputing throws away almost all the work. One
> in and one out makes it `O(n)` instead of `O(n·k)` — at `n = 100,000` and `k = 1,000`, 200,000
> operations against 100 million.

---

## 7. The traps

### The near-miss: the wrong element leaving

```python
total += nums[i] - nums[i - k + 1]      # off by one
```

The window is now `k - 1` or `k + 1` wide depending on which way you got it wrong, and — this is the
problem — **the answer still looks plausible**. There is no error, no crash, and the sums are in the
right ballpark.

The check that catches it in five seconds: after the line runs, the window should be
`nums[i - k + 1 .. i]`. Count the elements in that range: `i - (i - k + 1) + 1 = k`. **State the range
out loud as you write the line.**

### The near-miss: `best = 0`

```python
best = 0                               # instead of the first window's total
```

On an all-negative array — `[-1, -2, -3]` with `k = 2` — this returns `0`, which is not the sum of any
window. The same bug as [day 014](../day-014-single-pass-habit/README.md): a tracker must start as a
real value, not a convenient constant. `best = total` after building the first window.

### The near-miss: starting the loop in the wrong place

```python
for i in range(1, len(nums)):          # should be range(k, ...)
```

The first few iterations use a negative `i - k`, which in Python indexes from the **end** of the array
rather than raising. So it silently subtracts elements from the far end of the input. No error, a
completely wrong answer, and it is the negative-index trap from
[day 016](../day-016-2d-arrays/README.md) again.

### The near-miss: forgetting to delete zero counts

```python
window[left] -= 1
# no deletion at zero
if window == need:                     # never true again
```

`Counter({'a': 2, 'b': 0})` is not equal to `Counter({'a': 2})`, so once any character's count reaches
zero the comparison fails forever. On `"cbaebabacd"` with `"abc"` you get `[0]` instead of `[0, 6]` —
the first match is found before any count hits zero, and nothing is found afterwards. **A partly-right
answer, which is the hardest kind to notice.**

### The near-miss: `remove` instead of `discard`

```python
seen.remove(nums[i - k - 1])
```

```
KeyError: 1
```

On `[1, 1, 1]`, the value leaving the window may already have been removed, or may equal a value still
present. `discard` does nothing when the element is absent; `remove` raises.

### The near-miss: the deque holding values instead of indices

```python
while dq and dq[-1] <= x:
    dq.pop()
dq.append(x)                           # values, not indices
```

Everything works until you need to know whether the front has aged out — and with only values you
cannot tell, because a value does not say where it came from. **Store indices, read values through
them.**

### The contract corner: `k` larger than the array

```python
max_sum_of_size_k([1, 2], 3)
```

There is no window of size 3, so the answer is undefined. Return `None`, raise, or return 0 — but
**decide, and say which**. Without a guard, `sum(nums[:3])` quietly returns `3` (the sum of the whole
array) and the loop never runs, so you get a confident answer to a question with no answer.

---

## 8. In the interview

### How it gets asked

- *"Find the maximum sum of any subarray of size k."* — the base version, and the one where you say the
  overlap insight.
- *"Find the maximum average of any k consecutive elements."* — LeetCode 643, the same thing with one
  division.
- *"Find the maximum in every window of size k."* — LeetCode 239, and a genuinely harder problem hiding
  one sentence away.
- *"Find all anagrams of p in s."* — LeetCode 438, window plus a counter.
- *"Does the array contain a duplicate within k positions?"* — LeetCode 219, window plus a set, and
  off by one from the rest.

### What to say out loud, in the first ninety seconds

1. **State the brute force and its cost.** *"The obvious approach recomputes the sum of each window,
   which is O(n·k)."*
2. **Say the insight in one sentence.** *"But consecutive windows overlap in k−1 elements, so
   recomputing throws away almost all the work I just did."*
3. **Say the move.** *"Instead I keep a running total: when the window slides, one element enters on
   the right and one leaves on the left, so I add one and subtract one. Two operations instead of k."*
4. **Say the index rule, and check it aloud.** *"When index i enters, index i−k leaves — so afterwards
   the window covers i−k+1 through i, which is exactly k elements."*
5. **Give the cost with the counting.** *"Each element enters once and leaves once, so 2n operations
   regardless of k. O(n) time, O(1) space."*
6. **Flag the boundary cases.** *"I'll guard k larger than the array, and start `best` from the first
   window rather than zero, in case the values are negative."*
7. **Anticipate the follow-up.** *"If you ask for the maximum of each window rather than the sum, this
   arithmetic won't work — subtraction has an inverse and max doesn't — and I'd need a monotonic
   deque."*

### The follow-ups

**"Now find the maximum in each window instead of the sum."**
That is a genuinely different problem, and the reason is worth stating: a sum can be maintained
incrementally because addition has an inverse — subtracting the leaving element exactly undoes adding
it. Maximum has no inverse. If the element leaving happens to be the maximum, the new maximum could be
any of the remaining k−1 and I have kept no information about them. So I need a structure: a deque of
**indices** whose values decrease from front to back. When a new value arrives I pop from the back
everything smaller than it, because those elements are both older and smaller, so they can never be the
maximum of any window that also contains the new one. Then I pop the front if it has aged out of the
window, and the front is the answer. Each index is pushed once and popped at most once, so it is O(n)
overall despite the inner `while` — and O(k) space. A max-heap of size k is a legitimate middle answer
at O(n log k), but it needs extra bookkeeping to evict aged-out elements lazily.

**"How do you know the deque version is O(n) and not O(n·k)?"**
Because I count the pushes rather than the loop nesting. Every index is appended to the deque exactly
once, and once popped it never returns. So across the entire run there are at most n pushes and at most
n pops, which bounds all the work in the inner `while` loops added together — even though a single
iteration can pop many elements at once. That is the same argument as any amortised bound: the
expensive step is paid for by the cheap steps that preceded it. If I look at just one iteration it
seems it could be O(k); looking at the whole run, the total is linear.

**"What if the window size changes, or the condition is 'the longest window with at most k distinct
characters'?"**
Then it is a variable-size window rather than a fixed one, and the structure changes: instead of
sliding both edges together in lockstep, I extend the right edge to grow the window and advance the
left edge only while some condition is violated. The cost argument is the same — each index is visited
at most twice, once by each edge — so it stays O(n). The fixed version is the easy case because the
left edge's position is completely determined by the right edge's; in the variable version it is
decided by the condition, which is what makes those problems harder.

**"The array is a stream — you can't index backwards. What changes?"**
The sum version needs the leaving element, so I must remember the last k values, which means a deque
or a circular buffer of size k. That takes the space from O(1) to O(k), which is unavoidable — you
cannot subtract something you have not kept. The maximum version already keeps a deque of up to k
indices, so it works on a stream with no change at all beyond storing the values alongside. And a
useful thing to say: this is exactly what a moving average in a monitoring system is, and why those
systems have a configured window size — the window size is the memory cost.

### A model answer

> "The brute force is to compute the sum of each window separately: for each of the n−k+1 starting
> positions, add up k elements. That's O(n·k), and at a hundred thousand elements with k a thousand it's
> about a hundred million additions.
>
> But consecutive windows overlap in k−1 elements. So recomputing throws away almost everything I just
> calculated. Instead I keep a running total and adjust it: when the window slides one step, exactly one
> element enters on the right and exactly one leaves on the left.
>
> ```python
> def max_sum_of_size_k(nums: list[int], k: int) -> int | None:
>     if k <= 0 or len(nums) < k:
>         return None
>     total = sum(nums[:k])
>     best = total
>     for i in range(k, len(nums)):
>         total += nums[i] - nums[i - k]
>         best = max(best, total)
>     return best
> ```
>
> Three details worth calling out. When index i enters, index i−k leaves — so after that line the
> window covers i−k+1 through i, which is exactly k elements. I check that by counting the range out
> loud, because getting it wrong by one gives a plausible-looking answer with no error.
>
> The loop starts at k, because the first window was built before the loop. Starting earlier makes i−k
> negative, and in Python a negative index reads from the *end* of the array rather than raising, so
> that's another silent wrong answer.
>
> And `best` starts as the first window's total, not zero — otherwise an all-negative array returns
> zero, which isn't the sum of any window.
>
> Cost: each element enters once and leaves once, so 2n operations regardless of k. O(n) time and O(1)
> extra space, against O(n·k) for the brute force. I measured that: at a hundred thousand elements with
> k of a thousand it was about forty times faster, and the ratio grows with k exactly as you'd expect.
>
> If you changed the question to the maximum of each window rather than the sum, this wouldn't work.
> Subtraction undoes addition exactly, but there's no way to 'un-maximum' — if the element leaving was
> the largest, the next largest could be any of the others and I've kept nothing about them. That one
> needs a deque of indices with decreasing values, and it's still O(n) because each index is pushed and
> popped at most once."

---

## 9. Recall card

- **Consecutive windows overlap in `k - 1` elements.** Do not recompute — **add the entering, subtract
  the leaving**. `O(n·k)` becomes `O(n)`.
- **When `i` enters, `i - k` leaves**, and the window is then `nums[i-k+1 .. i]`. Say that range out
  loud to check yourself.
- **Build the first window before the loop; start the loop at `k`; start `best` from that window**, not
  from 0.
- **Sums, counts and sets slide; `max` does not** — subtraction needs an inverse. `max` needs a
  monotonic deque of indices, still `O(n)`.
- **With a `Counter`, delete keys at zero** — a zero entry makes every equality comparison fail.
