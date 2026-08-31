---
day: 72
track: dsa
title: "Largest rectangle in a histogram"
phase: "Stacks and queues"
status: written
---

# Day 072 · DSA — Largest rectangle in a histogram

**After today you can:** You can solve the hardest classic monotonic-stack problem and explain each pop.

**The interviewer asks it as:** *Find the largest rectangle in the histogram.*

---

## 1. What this is, and why they ask it

You are given a row of bars standing side by side, each one unit wide, with heights like
`[2, 1, 5, 6, 2, 3]`. Find the largest rectangle you can draw that fits entirely inside the bars. The
rectangle can span several bars, but it can only be as tall as the shortest bar it spans.

The whole problem collapses to one sentence: **for every bar, find the widest stretch in which that
bar is the shortest one.** The area for that bar is its height times that width, and the answer is
the biggest of those. Once you believe that sentence, the code is the monotonic stack from
[day 071](../day-071-monotonic-stack/README.md) with one extra line of arithmetic.

They ask it because it is the hardest thing you can build out of a single stack, and because the
brute force is so obviously quadratic that there is nowhere to hide. It is also the engine behind
"maximal rectangle in a binary matrix", which is a common follow-up in the same round. Expect it at
the harder end of a coding round — Google, Amazon, Microsoft, and most product companies that ask
LeetCode-hard questions. The off-by-one in the width is where most candidates lose it, so the width
formula is worth memorising as a sentence, not as a symbol.

---

## 2. The story

Basheer paints banners in a market street, and every year before the festival the shopkeepers'
committee gives him the same job: put up the biggest cloth banner he can across the front of the
shops.

There are eight shops in a row on that side of the street, and they are all different heights. Two of
them are proper two-storey buildings. One is a tiny box of a shop with a roof you can touch standing
flat on the road. The rest are somewhere in between.

The banner is a single piece of cloth, one rectangle, and it has to hang flat. The bottom edge sits
at road level. The top edge has to be one straight line all the way across. And every shop the banner
covers has to be tall enough to take a nail at that height, because Basheer will not tie a corner to
nothing.

So he has a choice to make. He can hang it low and wide, running past the tiny shop and covering all
eight fronts. Or he can hang it high, up at the level of the two-storey buildings, but then it covers
only those two, because the moment he reaches a lower roof there is nowhere to fix the top edge.

He walks the street once, slowly, with a rolled-up measuring tape in his hand. At each shop he asks
himself the same question: if the top edge were exactly at this roof, how far left and how far right
could the cloth run before it met a shorter roof? That stretch, times that height, is the size of the
banner.

The tiny shop gives him a very wide answer and almost no height. The tall one gives him a tall answer
and almost no width. Somewhere in the middle, four shops of roughly the same height standing
together, gives him the biggest piece of cloth he has ever hung on that street.

He does not measure every possible stretch, and this is the part his son never understands. He asks
the question eight times, once per roof, and stops. Because whatever the biggest banner turns out to
be, its top edge is level with somebody's roof. It has to be. If the top edge were below every roof
it touched, he could have raised it a little and got a bigger banner.

---

## 3. The idea in plain English

The bars are the shop fronts. The rectangle is the banner. And Basheer's last paragraph is the whole
solution.

### The claim that makes it finite

There are infinitely many rectangles you could draw, because the height can be any number. Basheer's
observation removes all but `n` of them:

> **The best rectangle's height is equal to the height of some bar.**

Why: take any rectangle that fits. If its top edge is strictly below every bar it spans, push the top
edge upward until it touches the lowest of those bars. It still fits, and it is now taller, so it is
bigger. So the best rectangle always has its top edge resting on at least one bar — and that bar is
the shortest bar in its span.

That turns "try all rectangles" into "try `n` rectangles": one per bar, where that bar is the
shortest one in the span.

### The question, per bar

For bar `i` with height `heights[i]`, you want the widest span in which `heights[i]` is the minimum.
Walk left from `i` until you meet a bar shorter than `heights[i]`; walk right until you meet a bar
shorter than `heights[i]`. Everything strictly between those two shorter bars is your span.

So you need two numbers for every bar:

- **`left[i]`** — the index of the nearest bar to the left that is **strictly shorter**. If there is
  none, use `-1`, meaning "the wall at the start of the street".
- **`right[i]`** — the index of the nearest bar to the right that is **strictly shorter**. If there
  is none, use `n`, meaning "the wall past the end".

Then:

```
 width = right[i] - left[i] - 1
 area  = heights[i] * width
```

The `- 1` is because `left[i]` and `right[i]` are the shorter bars themselves, which are *not* part
of the span. Say it as a sentence and you will never get it wrong: **the span is everything strictly
between the two shorter bars, so its width is the gap between them minus one.**

Sanity check on `heights = [2, 1, 5, 6, 2, 3]`, for the bar of height 5 at index 2. To its left, the
nearest strictly shorter bar is the 1 at index 1. To its right, the nearest strictly shorter bar is
the 2 at index 4. Width is `4 - 1 - 1 = 2`, covering indices 2 and 3. Area is `5 × 2 = 10`.

### And you already know how to find those two numbers

"Nearest strictly smaller element to the left" and "nearest strictly smaller element to the right"
are two of the four variants from [day 071](../day-071-monotonic-stack/README.md). Each is one pass
of a monotonic stack. So a perfectly good solution is: one pass for `left`, one pass for `right`, one
pass for the arithmetic. Three passes, O(n), and very easy to explain.

The famous version does it in **one** pass, and here is the trick that makes it possible.

### The one-pass insight

In the next-smaller pass, the moment a bar gets popped is the moment you have found its
right-hand boundary — the current bar is the first shorter thing to its right. And at that instant,
whatever is left underneath it in the stack is its left-hand boundary, because the stack holds bars
in increasing order of height. So both boundaries are available at the moment of the pop.

That is the sentence to say out loud: **when a bar is popped, both of its boundaries are known at
once — the current index on the right, and the new top of the stack on the left.**

So the pop does all the work:

```python
        height = heights[stack.pop()]
        left = stack[-1] if stack else -1     # nearest shorter on the left
        width = index - left - 1              # `index` is the shorter one on the right
        best = max(best, height * width)
```

Read `left = stack[-1] if stack else -1` carefully. After the pop, the new top of the stack is a bar
that was **not** popped, which means it is not taller than the current bar — and since the stack is
increasing, it is shorter than the bar we just popped. If the stack is empty, nothing to the left is
shorter, so the span runs back to the start of the row, and `-1` makes the arithmetic come out right.

### The sentinel

When the loop over the real bars ends, some bars are still in the stack — the ones that never met
anything shorter on their right. They still need their areas computed, with `right = n`.

You can write a second loop for that. Or you can add one imaginary bar of height `0` at the end,
which is shorter than everything and therefore forces every remaining bar out of the stack with the
correct right boundary. That is a **sentinel** — a fake value added to the data so the main loop
handles a case that would otherwise need special code. You have seen one before, in the `prefix[0] =
1` of [day 038](../day-038-subarray-sum-k/README.md).

One extra element removes an entire loop. Say that you are doing it, and why, or the interviewer will
think you forgot the leftovers.

---

## 4. The picture

`heights = [2, 1, 5, 6, 2, 3]`. Indices above, heights below, and the bars drawn.

```
 index      0    1    2    3    4    5
 height     2    1    5    6    2    3

                          #
                     #    #
                     #    #
                     #    #
            #        #    #         #
            #        #    #    #    #
            #   #    #    #    #    #
          +----+----+----+----+----+----+
 index      0    1    2    3    4    5
```

The best rectangle is height 5 across indices 2 and 3 — area 10. Notice it is **not** the tallest bar
alone (6 × 1 = 6), and **not** the full width at the lowest height (1 × 6 = 6). It is a bar in the
middle, extended sideways as far as it can go.

Now the one-pass run, with a sentinel `0` appended at index 6. The stack holds indices, heights
increasing from bottom to top.

```
 i=0 h=2   stack empty                     push 0        stack: [0]        (2)
 i=1 h=1   top is 2 > 1  -> pop 0
             height 2, left = -1, width = 1 - (-1) - 1 = 1,  area  2
           stack empty                     push 1        stack: [1]        (1)
 i=2 h=5   top is 1, not > 5               push 2        stack: [1,2]      (1,5)
 i=3 h=6   top is 5, not > 6               push 3        stack: [1,2,3]    (1,5,6)
 i=4 h=2   top is 6 > 2  -> pop 3
             height 6, left = 2, width = 4 - 2 - 1 = 1,     area  6
           top is 5 > 2  -> pop 2
             height 5, left = 1, width = 4 - 1 - 1 = 2,     area 10   <-- best
           top is 1, not > 2               push 4        stack: [1,4]      (1,2)
 i=5 h=3   top is 2, not > 3               push 5        stack: [1,4,5]    (1,2,3)
 i=6 h=0   top is 3 > 0  -> pop 5
             height 3, left = 4, width = 6 - 4 - 1 = 1,     area  3
           top is 2 > 0  -> pop 4
             height 2, left = 1, width = 6 - 1 - 1 = 4,     area  8
           top is 1 > 0  -> pop 1
             height 1, left = -1, width = 6 - (-1) - 1 = 6, area  6
           stack empty                     push 6

 answer: 10
```

Three things to notice.

At `i=4`, **one arrival closed two bars**, and the second of them produced the winner. This is the
same "one element answers many" behaviour as day 071, and it is why the inner `while` does not make
this quadratic.

At `i=6`, the sentinel emptied the stack. Without it, bars 1, 4 and 5 would never have been measured,
and the answer would have come out as 6 instead of 10.

And look at the width for the bar of height 2 at index 4: it is **4**, not 2. When bar 4 is finally
popped, everything to its right that was taller has already gone, and the span runs from index 2 to
index 5. A bar can be the shortest bar over a stretch that includes bars that were pushed after it.

---

## 5. The code, built step by step

### Step 1 — the brute force, said out loud and rejected

"For every pair of start and end, find the minimum height in that stretch and multiply." That is
`n(n+1)/2` stretches, each needing a scan, so O(n³). At n = 1000 that is about 500 million
operations. Say the number, then improve it once before improving it properly.

The easy improvement: fix the left end, walk right, and keep a running minimum.

```python
def largest_rectangle_brute(heights: list[int]) -> int:
    best = 0
    for start in range(len(heights)):
        smallest = heights[start]
        for end in range(start, len(heights)):
            smallest = min(smallest, heights[end])       # running minimum
            best = max(best, smallest * (end - start + 1))
    return best
```

That is O(n²) — at n = 100,000, ten billion operations. Correct, and far too slow. Use it as the
reference implementation to check the fast one against.

### Step 2 — the two-array version, which is the one to explain first

If you are nervous, write this one. It is three simple passes and each pass is something you already
know.

```python
    n = len(heights)
    left = [-1] * n                      # nearest strictly shorter bar to the left
    stack: list[int] = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
```

This is "previous smaller element", written so that the answer is the *index* rather than the value.
Note `>=`: bars of equal height pop each other, so `left[i]` is the nearest **strictly** shorter bar.

```python
    right = [n] * n                      # nearest strictly shorter bar to the right
    stack = []
    for i in range(n - 1, -1, -1):       # walk backwards
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
```

The same loop walking the other way. `n` is the "wall past the end" default, matching `-1` at the
start.

```python
    return max(
        (heights[i] * (right[i] - left[i] - 1) for i in range(n)),
        default=0,
    )
```

One line of arithmetic per bar. `default=0` covers the empty input, where `max` of an empty sequence
would otherwise raise.

### Step 3 — collapsing it to one pass

The two-array version computes `right[i]` in its own backwards pass. But the forward pass already
discovers `right[i]` — it is exactly the index that causes `i` to be popped. So do the arithmetic at
the moment of the pop instead of storing it.

```python
    for index in range(n + 1):
        current = heights[index] if index < n else 0        # sentinel 0 at the end
        while stack and heights[stack[-1]] > current:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (index - left - 1))
        stack.append(index)
```

Five lines carry the whole algorithm. `index` is the right boundary because it is the first bar
strictly shorter than the popped one. `left` is the left boundary because the stack is increasing, so
whatever survived underneath is shorter still.

### Step 4 — why `>` and not `>=` here, and why equal bars are still safe

The pop condition is `heights[stack[-1]] > current`, so equal-height bars do **not** pop each other.
That means the bar underneath a popped bar might be exactly the same height rather than strictly
shorter, and the width computed for the upper one is too small.

That is fine, and here is why: the lower of the two equal bars is still in the stack, and when *it*
is popped it gets the full span — the same height, a bigger width, a bigger area. So the correct
answer is still found; only a duplicate, smaller measurement was thrown in along the way, and `max`
ignores it.

Check it on `[2, 2]`. Bar 1 is popped by the sentinel with `left = 0`, width 1, area 2. Then bar 0 is
popped with `left = -1`, width 2, area 4. The answer is 4.

This is worth saying out loud in the interview, because "what about equal heights?" is the first
follow-up and most candidates have not thought about it.

### Step 5 — the escalation: maximal rectangle in a binary matrix

Given a grid of `0`s and `1`s, find the largest rectangle made only of `1`s. Treat each row as the
ground line of a histogram: the height of column `c` is how many consecutive `1`s sit directly above
and including row `r`. Then run the histogram solver on every row.

```python
    heights = [0] * len(matrix[0])
    for row in matrix:
        for c, cell in enumerate(row):
            heights[c] = heights[c] + 1 if cell == "1" else 0   # reset on a zero
        best = max(best, largest_rectangle(heights))
```

Building each row's heights is O(columns), and each histogram solve is O(columns), so the whole thing
is O(rows × columns). Say that, because it sounds expensive and is not.

### The complete solution

```python
def largest_rectangle(heights: list[int]) -> int:
    """The area of the largest rectangle that fits inside the histogram.

    For every bar, find the widest span in which that bar is the shortest, and
    take the best area. The stack holds INDICES of bars whose right-hand
    boundary is not yet known, with heights increasing from bottom to top.

    When a bar is popped, both of its boundaries are known at that instant:
    the current index on the right (the first strictly shorter bar), and the
    new top of the stack on the left. A sentinel height of 0 at the end forces
    every remaining bar out with the right boundary set past the end.
    """
    n = len(heights)
    stack: list[int] = []                     # indices, heights increasing bottom->top
    best = 0

    for index in range(n + 1):
        current = heights[index] if index < n else 0        # the sentinel

        while stack and heights[stack[-1]] > current:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1               # -1 = the wall at the start
            width = index - left - 1                        # strictly between the two
            best = max(best, height * width)

        stack.append(index)

    return best


def largest_rectangle_two_pass(heights: list[int]) -> int:
    """The same answer, computed with explicit boundary arrays.

    Slower by a constant factor and easier to explain. Write this one if the
    one-pass width formula is not solid in your head under pressure.
    """
    n = len(heights)
    if n == 0:
        return 0

    left = [-1] * n                           # nearest strictly shorter to the left
    stack: list[int] = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    right = [n] * n                           # nearest strictly shorter to the right
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    return max(heights[i] * (right[i] - left[i] - 1) for i in range(n))


def largest_rectangle_brute(heights: list[int]) -> int:
    """O(n^2) reference. Fix the left end, walk right, keep a running minimum."""
    best = 0
    for start in range(len(heights)):
        smallest = heights[start]
        for end in range(start, len(heights)):
            smallest = min(smallest, heights[end])
            best = max(best, smallest * (end - start + 1))
    return best


def maximal_rectangle(matrix: list[list[str]]) -> int:
    """Largest rectangle of '1's in a binary grid.

    Each row becomes the ground line of a histogram whose column heights count
    the consecutive '1's directly above. A '0' resets that column to zero.
    """
    if not matrix or not matrix[0]:
        return 0

    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for column, cell in enumerate(row):
            heights[column] = heights[column] + 1 if cell == "1" else 0
        best = max(best, largest_rectangle(heights))
    return best


if __name__ == "__main__":
    print(largest_rectangle([2, 1, 5, 6, 2, 3]))      # 10
    print(largest_rectangle([2, 4]))                  # 4
    print(largest_rectangle([2, 2]))                  # 4
    print(largest_rectangle([5]))                     # 5
    print(largest_rectangle([]))                      # 0
    print(largest_rectangle([0, 0, 0]))               # 0
    print(largest_rectangle([1, 2, 3, 4, 5]))         # 9   (3+4+5 at height 3)
    print(largest_rectangle([5, 4, 3, 2, 1]))         # 9
    print(largest_rectangle([3, 3, 3, 3]))            # 12

    # the two implementations must agree, on every shape
    import random
    for _ in range(2000):
        sample = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
        assert largest_rectangle(sample) == largest_rectangle_brute(sample), sample
        assert largest_rectangle_two_pass(sample) == largest_rectangle_brute(sample), sample
    print("agreed on 2000 random inputs")

    grid = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    print(maximal_rectangle(grid))                    # 6
```

The random cross-check at the bottom is worth writing in the interview too, if there is time. "Let me
check the fast one against the obvious one on small random inputs" is a sentence that buys a lot of
trust, and it catches the width off-by-one immediately.

---

## 6. What it costs

### Time

The `for` loop runs `n + 1` times, so there are exactly `n + 1` pushes — every index goes on once,
including the sentinel.

The `while` loop only pops. **An index that has been popped never goes back on the stack.** So across
the whole run, the total number of pops is at most `n + 1`.

```
 pushes across the whole run:  exactly  n + 1
 pops   across the whole run:  at most  n + 1
 --------------------------------------------
 total stack operations:       <= 2n + 2   ->  O(n)
```

Each pop does three arithmetic operations and one comparison, all constant. So the whole thing is
**O(n)**.

It is the same counting argument as day 071 and it needs saying with the same confidence: the inner
loop is bounded **in total**, not per iteration. At `i=4` in the trace above, one iteration popped two
bars; a single iteration could pop a hundred thousand, and it would still be linear overall, because
those pops were paid for by pushes that already happened.

### Against the alternatives

```
 all pairs, minimum rescanned:  O(n^3)
 all pairs, running minimum:    O(n^2)
 monotonic stack:               O(n)

 n = 100,000
   O(n^2):  10,000,000,000 operations   — minutes
   O(n)  :         200,000 operations   — a few milliseconds
```

Fifty thousand times fewer operations. That is the difference between a submission that times out and
one that does not.

### Space

```
 stack:   O(n)  worst case
 output:  O(1)  — a single integer
```

The stack holds every bar at once when the heights are strictly increasing, like `[1, 2, 3, 4, 5]` —
nothing is ever popped until the sentinel arrives. On strictly decreasing heights it never holds more
than two, because each bar pops the one before it. Name both inputs; it takes five seconds.

The two-array version uses `O(n)` for `left`, `O(n)` for `right` and `O(n)` for the stack — three
arrays instead of one. Same complexity class, three times the memory, and it is a reasonable trade if
it means you get the width right.

### Maximal rectangle in a grid

`rows × columns` to build the height arrays, plus one O(columns) histogram solve per row, so
**O(rows × columns)** total, with **O(columns)** extra space. For a 200 × 200 grid that is 40,000
operations. Say the number — it sounds like it should be much worse than it is.

---

## 7. The traps

### Trap 1 — the width off-by-one

This is the one that costs people the question.

```python
            width = index - left                    # WRONG, misses the - 1
```

On `[2, 1, 5, 6, 2, 3]` this returns `15` instead of `10`, because every span is measured one bar too
wide. It is not obviously wrong — the answer is a plausible number and the code runs clean.

The fix is to say the sentence rather than trust the symbols: **`left` and `index` are the shorter
bars on either side, and neither of them is inside the span.** The span is what is strictly between
them, so its width is `index - left - 1`.

Check it once by hand on a two-bar case. For `[5]` with the sentinel, the bar is popped at `index =
1` with `left = -1`, so `width = 1 - (-1) - 1 = 1`, area 5. Correct.

### Trap 2 — using the popped index as the left boundary

```python
            popped = stack.pop()
            width = index - popped                  # WRONG
```

This measures from the popped bar itself rather than from the bar to its left, so it can never look
backwards past its own position. The popped bar's span usually extends to the **left** of it as well —
look at bar 4 in the trace, whose span runs from index 2 even though it sits at index 4.

What makes this one dangerous is that it gives the right answer on the sample input. On
`[2, 1, 5, 6, 2, 3]` it returns `10`, exactly like the correct version. The smallest input that
exposes it is `[4, 3]`, where the answer is `6` — height 3 across both bars — and this version
returns `4`. Always test a two-element input where the first bar is taller.

### Trap 3 — reading `stack[-1]` when the stack is empty

```python
            left = stack[-1]                        # no `if stack else -1`
```

```
IndexError: list index out of range
```

Fires the first time a bar is popped that has nothing shorter to its left — on `[2, 1, 5, 6, 2, 3]`
that is index 0, popped at `index = 1`, on the second iteration. Every stack problem in this phase has
the same guard, and here it appears twice: once in the `while` condition and once in the `left`
lookup.

### Trap 4 — forgetting the leftovers

```python
    for index in range(n):                          # no sentinel, no flush loop
        current = heights[index]
        ...
```

The bars still in the stack when the loop ends are never measured. On `[2, 2]` this returns `0`
instead of `4`, because neither bar ever pops the other. On a strictly increasing input like
`[1, 2, 3, 4, 5]` *every* bar is still in the stack at the end, so it returns `0` as well.

It is worth running this one to see how quietly it fails: on `[2, 1, 5, 6, 2, 3]` it happens to
return the correct `10`, because the bar that wins is popped in the middle of the walk. A missing
flush is invisible on exactly the inputs people test with.

Two fixes and both are fine: iterate to `n + 1` with a sentinel of `0`, or add a second loop after the
first that drains the stack with `index = n`. The sentinel is fewer lines and fewer chances to get the
right boundary wrong.

If the problem allowed negative heights, a sentinel of `0` would not be shorter than everything. It
does not — heights are non-negative — but say so, because noticing the assumption is the point.

### Trap 5 — `>=` in the one-pass version, without thinking

```python
        while stack and heights[stack[-1]] >= current:
```

This also produces the right answer, but for a different reason, and if you cannot say the reason you
should not write it. With `>=`, equal bars pop each other, so a popped bar's right boundary may be an
equal bar rather than a strictly shorter one, and the width is too small for the earlier duplicates —
but the *last* bar of an equal run gets the full span. Under `>`, the situation is mirrored: the
*first* bar of the run gets the full span.

Either way the maximum survives. Pick one, and be able to say which duplicate carries the real answer.

### Trap 6 — the empty input

```python
    return max(heights[i] * (right[i] - left[i] - 1) for i in range(n))
```

```
ValueError: max() arg is an empty sequence
```

Fires on `largest_rectangle_two_pass([])`. The one-pass version does not have this problem, because
`best` starts at `0` and is simply never updated. Guard the two-array version with an early
`if n == 0: return 0`, or pass `default=0` to `max`.

### Trap 7 — assuming the answer contains the tallest bar

It very often does not. On `[2, 1, 5, 6, 2, 3]` the tallest bar is 6 and the answer is a rectangle of
height 5. On `[1, 1, 1, 1, 1, 1, 1, 1, 1, 9]` the answer is `10` — the flat stretch of ten bars at
height 1, not the 9 standing alone. Any greedy idea that
starts from the tallest bar and grows outward is wrong, and it is worth having that counter-example
ready, because "why not just start from the maximum?" is a question interviewers ask to see if you
will defend the approach.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Given an array of heights where each bar has width 1, find the area of the
  largest rectangle in the histogram."* LeetCode 84, Hard.
- The matrix version, often as the follow-up ten minutes later: *"Given a binary matrix, find the
  largest rectangle containing only 1s."* LeetCode 85, Hard.
- The disguised version: *"Here is the profile of a city skyline. What is the biggest billboard you
  can mount flat against it?"* Same problem, different words.
- The softer sibling, sometimes asked first as a warm-up: *"how much rain water is trapped between
  these bars?"* LeetCode 42 — same stack, different bookkeeping.

### What to say out loud, in the first ninety seconds

1. **Reduce the problem before writing anything.** "The best rectangle's top edge must be level with
   some bar. If it were below every bar it spans, I could raise it and get a bigger one. So there are
   only n candidates, not infinitely many — one per bar."
2. **State the per-bar question.** "For each bar, I want the widest stretch where that bar is the
   shortest. That means: how far left until something shorter, and how far right until something
   shorter."
3. **Name what that is.** "Those two are previous-smaller and next-smaller, which are monotonic-stack
   passes. So a clean solution is three passes: left boundaries, right boundaries, then the
   arithmetic."
4. **Then offer the one-pass version.** "I can fold it into one pass. In a next-smaller pass, the
   moment a bar is popped, the current index *is* its right boundary, and the new top of the stack
   *is* its left boundary. So I compute the area at the moment of the pop."
5. **State the width formula as a sentence.** "Width is `index - left - 1`, because both boundaries
   are the shorter bars themselves and neither is inside the span."
6. **Pre-empt the complexity question.** "One pass, each index pushed once and popped at most once, so
   O(n) time and O(n) space."

Write the width formula down before you write the loop. Under pressure it is the thing that goes.

### The follow-ups

**"What about bars of equal height?"**
"They are safe, but for a reason worth stating. With a strict `>` in the pop condition, equal bars do
not pop each other, so when the upper one of a pair is popped its left boundary is an equal bar rather
than a shorter one, and its width comes out too small. But the lower one is still in the stack, and
when it is popped it gets the full span at the same height. So the correct area is still measured, and
the too-small one is discarded by the `max`."

**"How do you handle the bars left in the stack at the end?"**
"I append a sentinel bar of height zero. It is shorter than every real bar, so it forces the whole
stack out with the right boundary set to `n`. It removes an entire drain loop. It works because
heights are non-negative — if they could be negative, I would use minus infinity or write the loop."

**"Now solve maximal rectangle in a binary matrix."**
"Treat each row as the ground of a histogram. The height of a column is the number of consecutive 1s
directly above and including that row; a 0 resets it to zero. Then run this solver once per row and
take the best. Building the heights is O(columns) per row and the solve is O(columns) per row, so the
whole thing is O(rows × columns) — no worse than reading the input."

**"Is a loop inside a loop not quadratic?"**
"No. There are exactly n+1 pushes, and an index once popped never returns, so there are at most n+1
pops. Total stack operations are bounded by about 2n across the whole run, however unevenly they are
spread. One iteration might pop a hundred thousand bars; that iteration has used up all the pops the
rest of the run was going to do."

**"Can you do it in O(1) extra space?"**
"Not with this approach, and I would not claim to. There is a divide-and-conquer solution that
recurses on the minimum bar, which is O(n log n) on average and O(n²) in the worst case — worse in
time and it still uses stack depth. For this problem the monotonic stack at O(n) time and O(n) space
is the right answer, and the O(n) space is a genuine requirement, not laziness."

### A model answer

Asked: *find the largest rectangle in a histogram given `[2, 1, 5, 6, 2, 3]`.*

> "First let me cut the problem down, because as stated there are infinitely many rectangles — the
> height can be anything.
>
> Claim: the best rectangle's top edge is level with the top of some bar. Suppose it were strictly
> below every bar it spans. Then I could push the top edge up until it touched the lowest of those
> bars, and it would still fit and be bigger. So the best rectangle always rests on at least one bar,
> and that bar is the shortest one in its span. That gives me exactly n candidates: for each bar, the
> widest stretch in which that bar is the minimum.
>
> So for each bar I need two things: how far left I can go before hitting something shorter, and how
> far right. Those are 'previous smaller element' and 'next smaller element', and each one is a
> monotonic stack pass. Once I have them, the area for bar `i` is `heights[i] × (right[i] - left[i] -
> 1)`. The minus one is because `left` and `right` are the shorter bars themselves, and neither of
> them is inside the span.
>
> That is a perfectly good three-pass O(n) solution and I am happy to write it. But I can fold it into
> one pass, and I think that is what you are looking for.
>
> In the next-smaller pass, the moment a bar gets popped is exactly the moment I have found its right
> boundary — the current bar is the first shorter thing to its right. And at that same instant, the
> new top of the stack is its left boundary, because the stack is increasing by height, so whatever is
> underneath a popped bar is shorter than it. Both boundaries, at the moment of the pop. So I compute
> the area right there and never store the arrays.
>
> The stack holds indices, not heights, because I need positions to compute widths. If the stack is
> empty after popping, there is nothing shorter to the left at all, so I use minus one as the
> boundary and the arithmetic still comes out right.
>
> For the bars that never meet anything shorter on their right, I append one sentinel bar of height
> zero. It is shorter than everything, so it drains the stack with the right boundary set past the
> end, and I do not need a separate cleanup loop.
>
> On `[2, 1, 5, 6, 2, 3]` the answer is 10 — height 5 across indices 2 and 3. Worth noticing that it
> is neither the tallest bar alone, which gives 6, nor the full width at the lowest height, which also
> gives 6.
>
> Complexity: every index is pushed exactly once and popped at most once, so at most about 2n stack
> operations across the whole run. O(n) time. O(n) space for the stack, which is genuinely needed —
> worst case is strictly increasing heights, where nothing pops until the sentinel arrives.
>
> One thing I would want to confirm: heights are non-negative, yes? That is what makes a zero sentinel
> safe. And if there are equal heights, the code is still correct — the lower bar of an equal pair
> picks up the full span when it is popped."

---

## 9. Recall card

- **Kill the infinity first: the best rectangle's top edge is level with some bar** — otherwise you
  could raise it. So there are exactly `n` candidates, one per bar: **the widest stretch in which that
  bar is the shortest.**
- **Per bar you need two boundaries — nearest strictly shorter on the left and on the right — and both
  are monotonic-stack passes.** `width = right - left - 1`, because **both boundaries are the shorter
  bars themselves and neither is inside the span.** That `- 1` is where the question is lost.
- **One pass, because the pop knows both boundaries at once:** the current index is the right
  boundary, `stack[-1] if stack else -1` is the left. Stack holds **indices**, heights **increasing**
  bottom to top. Five lines: pop, `left`, `width`, `max`, push.
- **A sentinel height of `0` at the end drains the leftovers** with the right boundary at `n`, and
  removes the whole cleanup loop. Without it, `[1, 2, 3, 4, 5]` returns **0**. Safe only because
  heights are non-negative.
- **O(n) time** — `n + 1` pushes, each index popped at most once, ≤ 2n operations, bounded in total
  not per iteration (10¹⁰ vs 2 × 10⁵ at n = 100,000). **O(n) space** (strictly increasing input).
  Equal bars are safe: the lower one collects the full span. Escalation: **maximal rectangle in a
  binary grid** = one histogram per row, **O(rows × columns)**.
