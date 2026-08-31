---
day: 74
track: dsa
title: "Deques and the sliding-window maximum"
phase: "Stacks and queues"
status: written
---

# Day 074 · DSA — Deques and the sliding-window maximum

**After today you can:** You can maintain a window maximum in O(n) total using a monotonic deque.

**The interviewer asks it as:** *Find the maximum in every window of size k.*

---

## 1. What this is, and why they ask it

A **deque** — "double-ended queue", pronounced "deck" — lets you add and remove at *both* ends in
O(1). A stack uses one end. A queue uses one end for adding and the other for removing. A deque uses
all four operations, and today is the problem that needs all four.

The problem: given `[1, 3, -1, -3, 5, 3, 6, 7]` and `k = 3`, report the maximum of every window of
three consecutive elements, as the window slides one step at a time. The answer is
`[3, 3, 5, 5, 6, 7]`. The obvious solution recomputes the maximum for each window, which is O(n·k).
The good solution keeps a small **monotonic deque** of "elements that could still be the maximum" and
is O(n) overall.

They ask it because it is the hardest sliding-window problem that still fits in twenty minutes, and
because the reasoning is not about code at all. It is one idea: **when a big number arrives, every
smaller number before it is worthless for ever** — because the big one is in every future window that
contains any of them, and it outlives them all. Candidates who reach for a heap get O(n log k) and a
lecture about why the deque is better. Expect it at Amazon, Google, Microsoft and any company using
LeetCode-hard rotation; it is LeetCode 239.

---

## 2. The story

Lakshmi has had the snack cart outside the college gate for eleven years, and the only number she
cares about is the best day in the last week.

Her rule came from her husband and she has never changed it. If the best day in the last seven has
been over two thousand rupees, she buys the good sev, which costs more. If not, she buys the ordinary
one. So every evening, after she has scraped down the tava and put the shutters on the cart, she puts
the day's takings into her phone, and then she wants to know the best of the last seven.

For years she did it the slow way. Scroll back, read seven numbers, pick the biggest. Seven numbers
every evening, at half past nine, tired, and twice she read the wrong week.

Her son showed her something she now does without thinking.

She keeps a very short second list. On the day he explained it, it had three numbers on it: Tuesday's
2,400, Friday's 1,850, and Saturday's 1,600. Only three, in falling order, and she keeps it for one
reason: those are the only days that could still be the best of some future week.

Every evening she does two small things before writing the day down.

First she looks at the end of her short list, at the smallest numbers, and crosses off anything below
today's. On the Sunday she took 1,900, so Saturday's 1,600 and Friday's 1,850 both went. They are
smaller than today, and they will fall out of the week before today does, so there is no week left in
which either of them wins. Gone for good.

Second she looks at the front, at Tuesday's 2,400, and checks the date. Once it is more than seven
days back it goes, because it is not in the week any more, however big it was.

Then she adds today at the end.

And now the answer is just the first number on the short list. She does not read seven numbers. She
reads one. On a bad week the list has one number on it; on a slowly falling week it has seven. Most
evenings it has two or three, and the whole thing takes her four seconds.

---

## 3. The idea in plain English

Lakshmi's short list is a **monotonic deque**: a double-ended queue whose contents are always in
falling order, kept that way by throwing things out of the back before anything new goes on.

### The deque itself

A **deque** is a queue you can push to and pop from at either end, all in O(1):

```python
from collections import deque

d = deque()
d.append(5)       # add at the BACK          -> [5]
d.appendleft(9)   # add at the FRONT         -> [9, 5]
d.pop()           # remove from the BACK     -> 5, leaving [9]
d.popleft()       # remove from the FRONT    -> 9, leaving []
d[0], d[-1]       # look at front and back
```

You met it in passing on [day 031](../day-031-fixed-window/README.md) and as the right queue on
[day 073](../day-073-queues/README.md). Today it earns its two ends.

### The one idea

Say this before writing any code, because it *is* the solution:

> **When a new element arrives, every earlier element smaller than it can be thrown away for ever.**

Why "for ever"? Take Friday's 1,850 and Sunday's 1,900. Any future week that contains Friday also
contains Sunday, because Sunday is later. Sunday is bigger. So Friday can never be the maximum of any
window from now on. It is not merely unlikely — it is impossible, and that is what lets you delete it
rather than store it.

So what remains is exactly: **the elements that are the maximum of the window starting at their own
position**. And they are automatically in falling order, because anything that broke the order was
deleted on arrival.

### The two removals, and why you need both ends

- **From the back** — throw out elements smaller than the newcomer. That is the rule above. This is
  the *stack* half of the structure, exactly the monotonic stack of
  [day 071](../day-071-monotonic-stack/README.md).
- **From the front** — throw out the element that has slid out of the window. Being big does not save
  you from being old. This is the *queue* half.

One structure, both behaviours, which is precisely why a deque and not a stack or a queue.

### Store indices, not values

The front removal asks "is this element still inside the window?", and you cannot answer that from a
value. You need the position. So the deque holds indices, and you compare with `numbers[index]` when
you need the value. Same rule as day 071, for the same reason, and it is the first thing that breaks
if you ignore it.

The expiry check is: the window covering positions `i-k+1 … i` no longer contains index `j` when
`j <= i - k`.

### The three lines, per element

```python
        if window and window[0] <= index - k:      # 1. drop the expired front
            window.popleft()
        while window and numbers[window[-1]] <= value:   # 2. drop the smaller backs
            window.pop()
        window.append(index)                       # 3. the newcomer joins
```

Then the answer for this window, once there is a full window to answer for, is `numbers[window[0]]`.

Step 1 uses `if`, not `while`, and that is worth a sentence: the window slides by exactly one
position per step, so at most one index can expire per step. A `while` is also correct and costs
nothing; use it if it makes you feel safer, and say why the `if` is enough.

### Why not a heap?

A max-heap gives you the maximum in O(1) and insertion in O(log k), but it cannot remove the element
that just left the window, because that element is buried somewhere in the middle. Two workarounds:

- **Lazy deletion** — push `(-value, index)`, and before reading the top, pop anything whose index has
  expired. Correct, O(n log n), and it works. Measured below at about **1.8× the deque's runtime**.
- **A heap with a position map** — more code, more bugs, no better complexity.

The deque wins because it never stores anything it will not use. Say that: *the heap keeps everything
and filters at read time; the deque throws away at write time, so it only ever holds elements that
still have a chance.*

The heap answer is still worth mentioning in the interview. It shows you know the alternative, and
"correct at O(n log k), and here is why I would not" is stronger than never mentioning it.

### The family

- **Sliding-window minimum** — flip the comparison; the deque becomes increasing.
- **Longest subarray where max − min ≤ limit** (LeetCode 1438) — run *two* deques at once, one for
  the max and one for the min, and shrink the window while their fronts differ by more than the
  limit.
- **Shortest subarray with sum at least K** (LeetCode 862) — a monotonic deque over prefix sums,
  with negatives allowed, which is why a plain sliding window fails there.
- **Jump Game VI** and **Constrained Subsequence Sum** — dynamic programming where the transition is
  "the best value in the last k cells", which is this exact structure.

---

## 4. The picture

`numbers = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`. The deque holds **indices**; the values are shown
beneath in brackets.

```
 index    0    1    2    3    4    5    6    7
 value    1    3   -1   -3    5    3    6    7

 i=0 v=1   nothing expires; nothing smaller       push 0   deque: [0]        (1)
 i=1 v=3   nothing expires; 1 <= 3 -> pop 0       push 1   deque: [1]        (3)
 i=2 v=-1  nothing expires; 3 > -1, keep          push 2   deque: [1,2]      (3,-1)
           window 0..2 full  ->  answer 3
 i=3 v=-3  front is 1, 1 > 3-3=0, stays
           -1 > -3, keep                          push 3   deque: [1,2,3]    (3,-1,-3)
           window 1..3        ->  answer 3
 i=4 v=5   front is 1, 1 <= 4-3=1 -> EXPIRED, popleft
           -3 <= 5 -> pop 3 ; -1 <= 5 -> pop 2    push 4   deque: [4]        (5)
           window 2..4        ->  answer 5
 i=5 v=3   front is 4, still inside; 5 > 3, keep  push 5   deque: [4,5]      (5,3)
           window 3..5        ->  answer 5
 i=6 v=6   front is 4, still inside
           3 <= 6 -> pop 5 ; 5 <= 6 -> pop 4      push 6   deque: [6]        (6)
           window 4..6        ->  answer 6
 i=7 v=7   6 <= 7 -> pop 6                        push 7   deque: [7]        (7)
           window 5..7        ->  answer 7

 answers: [3, 3, 5, 5, 6, 7]
```

Three things to notice.

At `i=4`, **both** removals happened in one step: one index expired off the front, and two were
crushed off the back by the 5. That is the only step in this trace where both ends were used, and it
is why the structure needs both.

The deque never held more than three indices, even though the array has eight elements. Its size is
bounded by `k`, and usually far below it.

And the values in the deque, read front to back, are always falling: `(3, -1, -3)`, `(5, 3)`. Nobody
sorted them. Anything that would have broken the order was popped before it could join.

Now the shape of the structure itself:

```
        front                                   back
      (the answer)                        (the newest)
          |                                     |
          v                                     v
        +-----+-----+-----+-----+-----+-----+-----+
        |  9  |  7  |  7  |  4  |  4  |  2  |  1  |
        +-----+-----+-----+-----+-----+-----+-----+
          ^                                     ^
   popleft when this               pop while these are
   index has slid out              <= the arriving value
   of the window
```

The front is the only place you ever *read*. The back is the only place you ever *push*. Both ends
are places you remove from, for two completely different reasons — too old at the front, too small at
the back.

---

## 5. The code, built step by step

### Step 1 — the brute force, with a number

```python
def max_window_brute(numbers: list[int], k: int) -> list[int]:
    return [max(numbers[i:i + k]) for i in range(len(numbers) - k + 1)]
```

One line, obviously correct, and O(n·k). At n = 200,000 and k = 1,000 that is two hundred million
comparisons — measured at **1.98 seconds** below. Write it as the reference implementation, say the
number, and move on.

### Step 2 — the observation, said before any code

"If a new number arrives that is bigger than something already waiting, that older, smaller number
can never be the answer again. Every future window containing it also contains the new one, because
the new one is later. So I can delete it rather than remember it."

That sentence is the whole interview. Everything after it is typing.

### Step 3 — expire the front

```python
        if window and window[0] <= index - k:
            window.popleft()
```

The window at position `index` covers `index - k + 1 … index`. An index at or below `index - k` has
fallen out. Only one can fall out per step, because the window moves by one.

### Step 4 — crush the back

```python
        while window and numbers[window[-1]] <= value:
            window.pop()
```

`<=` rather than `<` throws out equal values too. Both are correct — equal elements are
interchangeable as maxima — but `<=` keeps the deque smaller, so use it and be able to say why the
choice does not affect the answer.

### Step 5 — record, once the window is real

```python
        if index >= k - 1:
            answers.append(numbers[window[0]])
```

The first complete window ends at index `k - 1`. Before that there is nothing to report. Forgetting
this guard is the most common wrong answer: you get `n` results instead of `n - k + 1`.

### The complete solution

```python
from collections import deque


def max_sliding_window(numbers: list[int], k: int) -> list[int]:
    """The maximum of every window of k consecutive elements.

    The deque holds INDICES of elements that could still be the maximum of
    some future window, with their values falling from front to back.

    Two removals, for two different reasons:
      front — the index has slid out of the window (too old)
      back  — the value is <= the arriving value (too small, for ever)

    Each index is appended once and removed at most once, so this is O(n)
    despite the inner while loop. Space is O(k).
    """
    if k <= 0 or not numbers:
        return []

    window: deque[int] = deque()        # indices, values falling front->back
    answers: list[int] = []

    for index, value in enumerate(numbers):
        if window and window[0] <= index - k:       # 1. too old
            window.popleft()

        while window and numbers[window[-1]] <= value:   # 2. too small, for ever
            window.pop()

        window.append(index)                        # 3. the newcomer

        if index >= k - 1:                          # 4. a full window exists
            answers.append(numbers[window[0]])

    return answers


def min_sliding_window(numbers: list[int], k: int) -> list[int]:
    """The same thing with the comparison flipped. The deque is now RISING
    from front to back, and the front is the minimum."""
    if k <= 0 or not numbers:
        return []

    window: deque[int] = deque()
    answers: list[int] = []

    for index, value in enumerate(numbers):
        if window and window[0] <= index - k:
            window.popleft()
        while window and numbers[window[-1]] >= value:   # >= instead of <=
            window.pop()
        window.append(index)
        if index >= k - 1:
            answers.append(numbers[window[0]])

    return answers


def max_window_brute(numbers: list[int], k: int) -> list[int]:
    """O(n*k) reference. Correct, obvious, and far too slow."""
    if k <= 0 or not numbers:
        return []
    return [max(numbers[i:i + k]) for i in range(len(numbers) - k + 1)]


def max_window_heap(numbers: list[int], k: int) -> list[int]:
    """The alternative worth naming and then rejecting.

    A heap cannot remove the element that just left the window, so you push
    (-value, index) and discard expired entries lazily from the top. Correct,
    O(n log n), measured at about 1.8x the deque's runtime.
    """
    import heapq

    if k <= 0 or not numbers:
        return []

    heap: list[tuple[int, int]] = []
    answers: list[int] = []
    for index, value in enumerate(numbers):
        heapq.heappush(heap, (-value, index))
        while heap[0][1] <= index - k:       # discard whatever has expired
            heapq.heappop(heap)
        if index >= k - 1:
            answers.append(-heap[0][0])
    return answers


def longest_subarray_within_limit(numbers: list[int], limit: int) -> int:
    """LeetCode 1438: the longest window where max - min <= limit.

    Two deques at once — one falling for the maximum, one rising for the
    minimum — and the window shrinks from the left while their fronts differ
    by more than the limit.
    """
    highs: deque[int] = deque()      # indices, values falling
    lows: deque[int] = deque()       # indices, values rising
    left = 0
    best = 0

    for right, value in enumerate(numbers):
        while highs and numbers[highs[-1]] <= value:
            highs.pop()
        highs.append(right)
        while lows and numbers[lows[-1]] >= value:
            lows.pop()
        lows.append(right)

        while numbers[highs[0]] - numbers[lows[0]] > limit:
            left += 1                                  # shrink from the left
            if highs[0] < left:
                highs.popleft()
            if lows[0] < left:
                lows.popleft()

        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
    print(max_sliding_window([9, 8, 7, 6], 2))                 # [9, 8, 7]
    print(max_sliding_window([1, 2, 3, 4], 2))                 # [2, 3, 4]
    print(max_sliding_window([5, 5, 5, 5], 2))                 # [5, 5, 5]
    print(max_sliding_window([7], 1))                          # [7]
    print(max_sliding_window([], 3))                           # []
    print(min_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [-1, -3, -3, -3, 3, 3]
    print(longest_subarray_within_limit([8, 2, 4, 7], 4))      # 2

    import random
    for _ in range(3000):
        n = random.randint(1, 12)
        k = random.randint(1, n)
        sample = [random.randint(-5, 5) for _ in range(n)]
        assert max_sliding_window(sample, k) == max_window_brute(sample, k), (sample, k)
        assert max_window_heap(sample, k) == max_window_brute(sample, k), (sample, k)
    print("agreed with brute force on 3000 random inputs")
```

The random cross-check is worth twenty seconds in an interview. This problem has three separate
off-by-one opportunities — the expiry comparison, the record guard, and the window arithmetic — and
small random inputs catch all three immediately.

---

## 6. What it costs

### Time

The `for` loop runs `n` times, so there are exactly `n` appends — one per element.

The `while` and the `popleft` only remove. **An index that has been removed never returns.** So
across the whole run, removals are at most `n`.

```
 appends across the whole run:   exactly n
 removals across the whole run:  at most  n
 ------------------------------------------
 total deque operations:         <= 2n    ->  O(n)
```

Same counting argument as the monotonic stack, and it needs saying with the same confidence: **the
inner `while` is bounded in total, not per iteration.** One arrival can crush ten thousand elements
off the back, and that is fine, because those ten thousand were each appended exactly once.

### Against the alternatives, measured

n = 200,000, k = 1,000, on this machine:

```
 brute force, max() per window        1.984 s      O(n*k)  = 2 x 10^8 comparisons
 heap with lazy deletion              0.0922 s     O(n log n)
 monotonic deque                      0.0500 s     O(n)
 -----------------------------------------------------------
 deque vs brute force:  about 40x
 deque vs heap:         about 1.8x
```

Two useful things in those numbers. The deque beats the brute force by a factor that grows with `k` —
at k = 10,000 the gap would be ten times wider again. And the heap is only 1.8× slower, which is
worth knowing honestly: if you can only remember the heap version under pressure, write it. It is a
correct answer, and 1.8× is not the difference between passing and failing. The deque is the better
answer; the heap is not a wrong one.

### Space

```
 deque:    O(k)   at most k indices
 answers:  O(n-k+1)  — the output, so it does not count as extra
```

The deque holds `k` indices in the worst case, which is a strictly decreasing input like
`[9, 8, 7, 6, 5]` where nothing is ever crushed off the back. On a strictly increasing input it holds
exactly one, because every arrival wipes the whole thing out. Name both.

Note that this is **O(k)**, not O(n). For n = 10⁶ and k = 3 the deque holds three indices. That
independence from `n` is a genuine selling point when the interviewer asks about streaming data.

---

## 7. The traps

### Trap 1 — storing values instead of indices

```python
        window.append(value)                    # instead of index
```

Everything still runs. The back removal works fine. But the front removal now has no way to ask "has
this slid out of the window?", because a value carries no position. People patch it by also tracking
a count, and the patch is always wrong on duplicates. **Store indices.** It costs one extra lookup,
`numbers[window[-1]]`, and it is the same rule as every monotonic-structure problem.

### Trap 2 — recording before the window is full

```python
        window.append(index)
        answers.append(numbers[window[0]])      # no `if index >= k - 1`
```

Returns `n` answers instead of `n - k + 1`. On `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3 you get
`[1, 3, 3, 3, 5, 5, 6, 7]` — eight values where six were asked for, and the first two are maxima of
partial windows nobody wanted.

### Trap 3 — the expiry comparison off by one

```python
        if window and window[0] < index - k:     # `<` instead of `<=`
```

Off by one, so an index one step too old stays in the deque for one extra step. It is a nasty bug
because it is invisible on most inputs: on `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3 it gives exactly
the right answers. The smallest input that exposes it is `[8, 3, 2]` with k = 2, where the correct
answer is `[8, 3]` and this version returns `[8, 8]` — reporting an 8 that left the window a step
ago.

Derive it rather than remember it. The window ending at `index` starts at `index - k + 1`. An index
`j` is out when `j < index - k + 1`, which is `j <= index - k`.

### Trap 4 — the empty-deque guard

```python
        while numbers[window[-1]] <= value:      # no `window and`
```

```
IndexError: deque index out of range
```

Fires on the very first element, since the deque starts empty. The same guard as every stack and
queue problem in this phase, and it must be the first half of the `and`.

### Trap 5 — using a plain list and `pop(0)`

```python
        window = []
        ...
        window.pop(0)                           # instead of deque.popleft()
```

Correct answers, quietly quadratic in `k`, for exactly the reason in
[day 073](../day-073-queues/README.md): removing from the front of a list shifts everything left.
The deque exists precisely so this operation is O(1). If you have written the deque solution and then
used a list to hold it, you have thrown away the entire point.

### Trap 6 — `while` versus `if` on the front, and why it does not matter

```python
        while window and window[0] <= index - k:   # `while` instead of `if`
            window.popleft()
```

This is **correct**. Only one index can ever expire per step, because the window moves by one, so the
`while` runs at most once. Use whichever you find clearer, but know why the `if` is enough — being
asked "are you sure one is enough?" and answering "yes, the window moves by exactly one position per
step" is a small, cheap win.

What *is* wrong is doing the front expiry **after** appending and reading:

```python
        window.append(index)
        answers.append(numbers[window[0]])
        if window[0] <= index - k:              # WRONG ORDER — read a stale front
            window.popleft()
```

Now the answer for this window can come from an element that has already left it. Expire first, then
crush, then push, then read.

### Trap 7 — `k` larger than the array, or `k = 0`

```python
    max_sliding_window([1, 2, 3], 5)
```

With no guard, `index >= k - 1` is never true and you get `[]`, which is arguably right. With `k = 0`
you get `[]` as well, but `window[0] <= index - 0` expires the element you just pushed on some inputs,
which is a confusing way to be right. Guard explicitly at the top and say what you decided — an empty
list, or an error. Deciding out loud is worth more than the decision.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Given an array and a window size k, return the maximum of every window."*
  LeetCode 239, Hard.
- The streaming version: *"Temperature readings arrive one per second. At any moment, report the
  highest reading in the last sixty seconds."* Same structure, and O(k) space is the selling point.
- The two-deque version: *"Find the longest subarray where the difference between the maximum and the
  minimum is at most `limit`."* LeetCode 1438.
- The disguised version, in a dynamic-programming round: *"You may jump at most k steps forward. What
  is the maximum score?"* LeetCode 1696 — the transition is "the best of the last k cells", which is
  this.

### What to say out loud, in the first ninety seconds

1. **State the brute force with a number.** "Recomputing the max for each window is O(n·k). At two
   hundred thousand elements with a window of a thousand, that is two hundred million comparisons —
   about two seconds."
2. **Say the observation, not the data structure.** "Here is the key: when a new element arrives, any
   earlier element smaller than it is worthless for ever. Every future window that contains the old
   one also contains the new one, because the new one is later, and the new one is bigger. So I can
   delete it, not just deprioritise it."
3. **Say what survives.** "So what I keep is exactly the elements that are still candidates, and they
   are automatically in falling order — I never sort anything."
4. **Say why it is a deque, in one sentence.** "I remove from the back when something bigger arrives,
   and from the front when something slides out of the window. Two ends, two different reasons.
   That is why it is a deque and not a stack or a queue."
5. **Say indices, and why.** "I store indices, because the front check is 'has this left the window',
   and a value cannot tell me that."
6. **Pre-empt the heap.** "A heap also works — push value and index, discard expired entries lazily —
   but that is O(n log n) and it keeps elements it will never use. The deque throws them away at
   write time, so it only ever holds live candidates."
7. **Pre-empt the complexity question.** "One `while` inside the `for`, still O(n): each index is
   appended once and removed at most once. Space is O(k), not O(n), which matters if this is a
   stream."

### The follow-ups

**"Why not a heap?"**
"A heap gives me the maximum immediately, but it cannot remove the element that has just left the
window, because that element is somewhere in the middle of the heap. So I would push `(-value,
index)` and lazily discard expired entries from the top before reading. That is correct and it is
O(n log n). I measured both once: the heap ran about 1.8 times the deque's time. The real difference
is conceptual — the heap stores everything and filters at read time, the deque discards at write time
and therefore only ever holds elements that still have a chance. That also makes the deque's space
O(k) rather than O(n)."

**"There is a `while` inside the `for`. Is that not O(n·k)?"**
"No. Count operations rather than nesting. Every index is appended exactly once by the outer loop,
and removed at most once, because once it is out of the deque it never returns. So total deque
operations are bounded by 2n across the whole run, however unevenly they land. One arrival can crush
a thousand elements off the back, and that arrival has used up a thousand removals the rest of the
run was going to do."

**"Now give me the minimum instead."**
"Flip the back comparison from `<=` to `>=`. The deque becomes rising instead of falling, and the
front is the minimum. Nothing else changes. And if I need both at once — for 'longest subarray where
max minus min is at most limit' — I run two deques side by side and compare their fronts."

**"The data is a stream and never ends. Does anything change?"**
"Almost nothing, and that is the strength of this solution. Space is O(k), independent of how much
data has gone past, so a window of sixty over a stream of a billion readings holds at most sixty
indices. The only change is that indices grow without bound, so in a long-running system I would
store timestamps, or wrap the index into a ring buffer of size k, rather than let an integer counter
run for months."

**"What if the elements are equal?"**
"It does not matter for correctness, because equal elements are interchangeable as maxima. I use `<=`
on the back removal so equals are discarded, which keeps the deque smaller. Using `<` keeps them,
which is also correct and slightly more memory. What I would not do is use `<` and then assume the
deque is strictly decreasing, because it is not."

**"Can you do it in O(1) space?"**
"Not for the general problem, no. There is a neat O(n) block-partition trick — split the array into
blocks of k, precompute prefix maxima and suffix maxima within each block, and answer any window with
one of each — but that uses O(n) extra space too, and it needs the whole array up front, so it cannot
stream. The deque's O(k) is the better bound in practice."

### A model answer

Asked: *find the maximum in every window of size k.*

> "The obvious version calls `max` on each window, which is O(n·k) — about two hundred million
> comparisons at two hundred thousand elements with a window of a thousand, and I measured that at
> roughly two seconds. So I want to reuse work between windows.
>
> Here is the observation that lets me. When a new element arrives, every earlier element smaller
> than it becomes worthless for ever. Not unlikely to be needed — impossible to need. Any future
> window that still contains the old element must also contain the new one, because the new one is
> later, and the new one is bigger. So the old one can never be a maximum again, and I can delete it
> rather than store it.
>
> So the structure I keep is: the elements that could still be the maximum of some window. And they
> are automatically in falling order, because anything that broke the order was deleted the moment
> something bigger arrived. I never sort.
>
> Now, why a deque. There are two reasons to remove something, and they happen at opposite ends. From
> the back, I remove elements smaller than the arriving one — that is the rule I just described. From
> the front, I remove the element that has slid out of the window, because being big does not save
> you from being old. Two ends, two reasons, so a stack is not enough and a queue is not enough.
>
> I store indices, not values, because the front check is 'is this still inside the window', and only
> a position can answer that. The element at index j is out when j is at most the current index minus
> k — I would derive that rather than memorise it: the window ending at i starts at i minus k plus
> one.
>
> The loop is four steps per element. Expire the front if it has aged out — one `if` is enough,
> because the window moves by exactly one position at a time. Crush the back while its values are at
> most the new value. Append the new index. And then, only once the current index has reached k minus
> one, record the front as the answer for this window. That last guard is what stops me returning n
> answers instead of n minus k plus one.
>
> On complexity: there is a `while` inside a `for` and it is still O(n). Every index is appended
> exactly once and removed at most once, so there are at most 2n deque operations across the whole
> run, however unevenly they fall. Space is O(k) — at most k indices, in the worst case of a strictly
> decreasing array; on an increasing array the deque holds exactly one. O(k) rather than O(n) matters
> if this is a stream.
>
> I should mention the alternative. A max-heap of value and index, discarding expired entries lazily
> from the top, is correct at O(n log n), and I measured it at about 1.8 times the deque's runtime.
> The reason I prefer the deque is that the heap keeps everything and filters when reading, whereas
> the deque throws things away when writing, so it only ever holds elements that still have a chance.
>
> One thing I would check before writing: are equal values fine to discard? They are, since equal
> elements are interchangeable as maxima, so I use less-than-or-equal on the back removal to keep the
> deque smaller."

---

## 9. Recall card

- **The whole problem is one sentence: when a bigger element arrives, every earlier smaller element is
  worthless for ever** — every future window containing the old one also contains the new one, and
  the new one is bigger. So **delete, do not deprioritise.** What survives is exactly the live
  candidates, automatically **falling front to back**.
- **Two removals at two ends, for two different reasons** — that is why it is a **deque**:
  `popleft` when the front index has **slid out** (`window[0] <= index - k`), `pop` while the back is
  **too small** (`numbers[window[-1]] <= value`). **Store indices**, because a value cannot tell you
  whether it is still in the window.
- **Four steps per element, in this order: expire front · crush back · append · record.** One `if`
  suffices for the expiry because the window moves by exactly one. **Record only when
  `index >= k - 1`**, or you return `n` answers instead of `n - k + 1`.
- **O(n) time** — n appends, each index removed at most once, ≤ 2n operations, **bounded in total not
  per iteration**. **O(k) space**, not O(n): worst case a strictly decreasing array, best case one
  index on a rising one. Measured at n = 200,000, k = 1,000: brute **1.98 s**, heap **0.092 s**, deque
  **0.050 s** — **40× the brute force, 1.8× the heap**.
- **Name the heap and reject it properly:** push `(-value, index)` and discard expired entries lazily
  — correct, O(n log n), O(n) space. *The heap keeps everything and filters at read time; the deque
  discards at write time.* The family: sliding-window **minimum** (flip to `>=`) · **two deques** for
  max − min ≤ limit · DP transitions that need "the best of the last k".
