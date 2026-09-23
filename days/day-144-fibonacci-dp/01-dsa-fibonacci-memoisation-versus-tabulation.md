---
day: 144
track: dsa
title: "Fibonacci: memoisation versus tabulation"
phase: "Dynamic programming"
status: written
---

# Fibonacci: memoisation versus tabulation

## 1. What this is, and why they ask it

Every dynamic programming problem can be written two ways, and you should be able to write both and convert
between them mechanically.

**Memoisation** — top-down — is the recursion you derived, with a cache bolted on. You start at the answer you
want and recurse down to the base cases, and the cache fills as the calls unwind.

**Tabulation** — bottom-up — starts at the base cases and fills an array forwards until it reaches the answer.
No recursion at all.

They compute the same values in a different order, and the conversion between them is a fixed procedure rather
than a fresh insight each time. **Learning that procedure is what today is for**, because "write it top-down,
now write it bottom-up" is one of the most common DP follow-ups there is, and fumbling the conversion after a
correct memoised solution is a bad way to lose a round.

The other reason is that the two forms are good at different things. Top-down is easier to derive and only
computes what it needs. Bottom-up has no recursion limit and makes the space optimisation obvious. **Neither
is better; knowing which to reach for is the skill.**

By the end of this lesson you can write both forms of any DP, convert between them by a fixed set of steps,
work out the fill order for bottom-up, collapse a table to a fixed window, and say which form you would choose
and why.

---

## 2. The story

Prabhakar took a loan for the scooter in 2019 — thirty-six months, and the bank gave him a small booklet with
a row for every month.

He did not trust it. Not because he thought the bank was cheating him, but because he had never in his life
taken a number on trust that he could work out himself, and thirty-six rows is not so many.

So he sat down on a Sunday with the interest rate and the instalment amount and worked it out.

The first way he tried was backwards, and it was how the question naturally came to him, because what he
actually wanted to know was the balance at the end of month thirty-six.

To know that, he needed the balance at the end of month thirty-five, plus the interest on it, minus the
instalment. To know *that*, he needed month thirty-four. Which needed thirty-three. He went down and down and
down until he reached month zero, which he knew — that was the loan amount — and then he came back up the
chain doing the arithmetic on the way.

It worked. It took him about forty minutes and he lost his place twice, because holding thirty-six half-finished
calculations in his head while going down the chain is genuinely hard, and he had to start again from month
thirty each time.

Then he did it the other way and it took eleven minutes.

He started at month one, which needed only the loan amount — a number he already had. He worked out the
balance and wrote it in the row. Then month two, which needed only month one, which was written in the row
above. Then month three. Straight down the page, thirty-six rows, never looking further back than the line
immediately above.

Same numbers. Same arithmetic. Different direction, and the second one never required him to hold anything in
his head at all.

The thing that struck him afterwards — and he mentioned it to his brother, who was not interested — is that
once he was working forwards, he did not actually need the booklet. **Each row only needed the row above it.**
He could have covered everything except the last line he wrote and carried on perfectly well. The thirty-five
rows above were a record, not a requirement.

He keeps the booklet anyway. It is nice to be able to see the whole thing.

---

## 3. The idea in plain English

Prabhakar's two Sundays are the two forms, and his last observation is the space optimisation.

**Top-down is starting at the question and working towards what you know.** "I want month 36. That needs month
35. That needs month 34..." — down to a base case, then back up. In code that is recursion with a cache:

```
solve(n):
    if n is a base case:  return the known answer
    if n is in the cache: return it
    answer = combine(solve(smaller), solve(smaller))
    cache[n] = answer
    return answer
```

**Bottom-up is starting at what you know and working towards the question.** "Month 1 needs only the loan
amount. Month 2 needs month 1." Fill an array from the base cases upwards:

```
dp[base cases] = known answers
for i in the right order:
    dp[i] = combine(dp[smaller], dp[smaller])
return dp[n]
```

**They compute exactly the same values.** The recurrence is identical; only the order differs, and which
direction you approach it from.

**The conversion is mechanical, and this is the part worth memorising.** Given a working memoised function,
bottom-up follows in five steps:

1. **The function's parameters become the table's dimensions.** `solve(i)` becomes `dp[i]`. `solve(i, j)`
   becomes `dp[i][j]`.
2. **The base cases become the initial values**, written into the table before the loop.
3. **The recursive calls become table reads.** `solve(i-1)` becomes `dp[i-1]`.
4. **Work out the loop order** so that every cell a formula reads is already filled. This is the only step
   that requires thought.
5. **Return `dp[the original argument]`** instead of `solve(n)`.

**Step four is the whole difficulty, and it has a simple rule: iterate in the direction the recursion goes
*towards*.** If `solve(i)` calls `solve(i-1)`, the recursion goes downwards, so the loop goes upwards. If it
calls `solve(i+1)`, the loop goes downwards. **The loop always runs opposite to the recursion.**

**Now the real differences, because "they are the same" is only true of the values.**

**Top-down only computes states it actually reaches.** If the reachable states are a small fraction of the
table — a sparse state space — bottom-up fills the whole thing and wastes the difference. Coin change with
huge denominations is the standard example.

**Bottom-up has no recursion.** Python allows about 960 nested calls, so a memoised solution with `n = 100,000`
dies before the cache helps — the *first* chain of calls goes all the way down before anything is stored.
**That is one of the two reasons to convert**, and it is the one that shows up as a crash.

**Bottom-up makes the space optimisation obvious**, which is the other reason. With the table written out you
can see that `dp[i]` reads only `dp[i-1]` and `dp[i-2]`, so thirty-four of the thirty-six rows are history.
In the recursive form that is genuinely hard to see.

**And the space optimisation has a rule too: keep a window as deep as the recurrence reaches back.** Reads
`dp[i-1]` and `dp[i-2]` → two variables. Reads all of `dp[i-1][*]` → one row. Reads `dp[i-1][*]` and
`dp[i][*]` → two rows, or one row updated in a careful direction.

**The thing you give up by optimising** is the ability to reconstruct *how* the answer was reached. The table
recorded the choices; two variables do not. **If the problem asks for the actual path, subset or sequence,
keep the table** — or store parent pointers, which costs the memory you were saving.

---

## 4. The picture

The two directions, on the same computation:

```
TOP-DOWN: start at the answer, recurse down, cache on the way back up

    solve(6)
      -> solve(5)
           -> solve(4)
                -> solve(3)
                     -> solve(2)  = 1   [base]
                     -> solve(1)  = 1   [base]
                     <- 2, cached
                -> solve(2)       cache HIT
                <- 3, cached
           -> solve(3)            cache HIT
           <- 5, cached
      -> solve(4)                 cache HIT
      <- 8

    calls go DOWN, answers come UP, the cache fills bottom-first anyway


BOTTOM-UP: start at the base cases, fill forwards

    i:      0   1   2   3   4   5   6
    dp:     0   1   1   2   3   5   8
                    ^
                    dp[2] = dp[1] + dp[0], and both are already there

    one pass, left to right, nothing held in the head
```

**What to notice.** The cache in the top-down version ends up filled from the bottom regardless — the values
are computed smallest-first either way. **The difference is entirely in who drives the order**: the recursion
discovers it, or you write it down.

The conversion, side by side:

```
  MEMOISED                              TABULATED

  @lru_cache                            dp = [0] * (n + 1)
  def solve(i):
      if i <= 1:                        dp[0], dp[1] = 0, 1        <- (2) base cases
          return i
      return solve(i-1) + solve(i-2)    for i in range(2, n+1):    <- (4) loop order
                                            dp[i] = dp[i-1] + dp[i-2]   <- (3) reads
  return solve(n)                       return dp[n]               <- (5)
         ^                                     ^
         (1) parameter -> index

  the recursion goes DOWN (i-1, i-2)  ->  the loop goes UP
```

And the space collapse:

```
  full table, n = 8:
     0   1   1   2   3   5   8  13  21
                             ^   ^   ^
                             |   |   |
     to compute this one ----+---+---+
     I only ever read these two

  so keep two variables:

     prev, curr = 0, 1
     repeat:  prev, curr = curr, prev + curr

  O(n) space  ->  O(1) space.
  The other n-2 cells were a record, not a requirement.
```

**What to notice.** The window is two wide because the recurrence reaches back two. A recurrence reaching back
`k` needs `k` values; a two-dimensional one reading only the previous row needs one row.

---

## 5. The code, built step by step

Start with the memoised version, because that is the one you write first.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n <= 1:
        return n                          # base cases: fib(0)=0, fib(1)=1
    return fib_memo(n - 1) + fib_memo(n - 2)
```

**Now convert it, step by step, saying each step out loud.**

**Step 1: the parameter becomes the index.** `fib_memo(n)` takes one integer, so the table is one-dimensional,
of size `n + 1`.

```python
dp = [0] * (n + 1)
```

**Step 2: the base cases become the initial values.**

```python
dp[0], dp[1] = 0, 1
```

**Step 3: the recursive calls become table reads.** `fib_memo(i-1)` becomes `dp[i-1]`.

**Step 4: the loop order.** The recursion goes downwards — `i` calls `i-1` and `i-2` — so the loop goes
upwards, and it starts after the base cases.

```python
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]
```

**Step 5: return the cell for the original argument.**

```python
return dp[n]
```

Put together:

```python
def fib_table(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)                    # dp[i] = the i-th Fibonacci number
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**The comment on the `dp` line is not decoration.** It is the state, written as a sentence, and it is the thing
you will have forgotten in ten minutes.

**Now the space optimisation.** Look at what `dp[i]` reads: `dp[i-1]` and `dp[i-2]`. Nothing else. So keep
two:

```python
def fib_two_vars(n: int) -> int:
    if n <= 1:
        return n
    prev, curr = 0, 1                     # dp[i-2], dp[i-1]
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr    # shift the window forward
    return curr
```

**The simultaneous assignment matters.** Written as two statements in the wrong order:

```python
curr = prev + curr
prev = curr                               # WRONG: prev now holds the NEW curr
```

That is a real bug and it produces powers of two rather than Fibonacci numbers. Either use the tuple form, or
use a temporary.

**Now the same conversion on a two-dimensional problem**, because that is where the loop order actually
requires thought. Unique paths in a grid:

```python
@lru_cache(maxsize=None)
def paths_memo(i: int, j: int) -> int:
    if i == 0 or j == 0:
        return 1                          # first row or column: one way
    return paths_memo(i - 1, j) + paths_memo(i, j - 1)
```

**Two parameters, so a two-dimensional table. The recursion decreases both, so both loops go upwards.**

```python
def paths_table(m: int, n: int) -> int:
    dp = [[0] * n for _ in range(m)]      # dp[i][j] = paths from (0,0) to (i,j)
    for i in range(m):
        for j in range(n):
            if i == 0 or j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

**And the space optimisation here is a row rather than two variables**, because `dp[i][j]` reads the whole
previous row:

```python
def paths_one_row(m: int, n: int) -> int:
    row = [1] * n                         # the first row: all ones
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]          # row[j] is the row ABOVE; row[j-1] is the LEFT
    return row[-1]
```

**Read that `+=` carefully, because it is the whole trick.** At the moment of the update, `row[j]` still holds
the value from the previous row — that is `dp[i-1][j]` — and `row[j-1]` has already been updated this pass, so
it holds `dp[i][j-1]`. **One array, updated left to right, doing the work of two.**

**And the direction is load-bearing.** Left to right works here because we want the *new* left value and the
*old* above value. Reverse the direction and `row[j-1]` would still hold the old row, which is a different and
wrong recurrence. **Whenever a table collapses to one row, the iteration direction becomes part of the
correctness.**

### The complete solution

```python
"""Memoisation and tabulation: the same recurrence, both directions, and the conversion."""

from __future__ import annotations

import sys
from functools import lru_cache


# ---- one dimension -------------------------------------------------------

@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    """Top-down. Easy to derive; limited by the recursion depth."""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def fib_table(n: int) -> int:
    """Bottom-up. dp[i] = the i-th Fibonacci number. No recursion."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):             # recursion goes DOWN, so the loop goes UP
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_two_vars(n: int) -> int:
    """dp[i] reads only i-1 and i-2, so the window is 2 wide. O(1) space."""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr    # simultaneous: order matters
    return curr


# ---- two dimensions ------------------------------------------------------

@lru_cache(maxsize=None)
def paths_memo(i: int, j: int) -> int:
    if i == 0 or j == 0:
        return 1
    return paths_memo(i - 1, j) + paths_memo(i, j - 1)


def paths_table(m: int, n: int) -> int:
    """dp[i][j] = distinct paths from (0,0) to (i,j)."""
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            dp[i][j] = 1 if (i == 0 or j == 0) else dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


def paths_one_row(m: int, n: int) -> int:
    """dp[i][j] reads the previous row, so one row suffices. Direction is load-bearing."""
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]          # old row[j] = above, new row[j-1] = left
    return row[-1]


if __name__ == "__main__":
    print("fib agree :", [f(30) for f in (fib_memo, fib_table, fib_two_vars)])
    print("paths agree:", paths_memo(6, 6), paths_table(7, 7), paths_one_row(7, 7))
    print()

    # Where top-down stops working.
    print("table(5000)    :", str(fib_table(5000))[:20], "...")
    print("two_vars(5000) :", str(fib_two_vars(5000))[:20], "...")
    try:
        fib_memo.cache_clear()
        fib_memo(5000)
    except RecursionError as error:
        print("memo(5000)     :", type(error).__name__, "-", error)
    print()

    # Where top-down wins: a sparse state space.
    @lru_cache(maxsize=None)
    def coins_memo(amount: int) -> int:
        if amount == 0:
            return 0
        if amount < 0:
            return 10**9
        return 1 + min(coins_memo(amount - c) for c in (1000, 5000))

    print("states a table would fill for amount=100000:", 100001)
    coins_memo(100000)
    print("states top-down actually visited          :", coins_memo.cache_info().currsize)
```

Running it:

```
fib agree : [832040, 832040, 832040]
paths agree: 924 924 924

table(5000)    : 38789684543883256337 ...
two_vars(5000) : 38789684543883256337 ...
memo(5000)     : RecursionError - maximum recursion depth exceeded

states a table would fill for amount=100000: 100001
states top-down actually visited          : 105
```

Three things to look at. **All three Fibonacci versions agree**, and both grid versions agree — the conversion
did not change the answer.

**`fib_memo(5000)` raises `RecursionError` while the two bottom-up versions return instantly.** The cache does
not help, because the very first call chain descends fifty thousand levels before a single value is stored.
**That is the crash that forces the conversion.**

And the last two lines are the case that goes the other way. With coin denominations of 1000 and 5000, only
amounts that are multiples of 1000 are ever reachable — so a table over `0..100000` fills a hundred thousand
and one cells, and top-down visits **105**. **The reachable state space is a fraction of a percent of the
table**, and top-down gets that for free.

---

## 6. What it costs

**Time is identical.** Both forms compute each distinct state once and do the same work per state.

```
time = (number of distinct states) x (work per state)
```

```
Fibonacci        n states x O(1)       = O(n)
Unique paths     m*n states x O(1)     = O(m*n)
```

**Space is where they differ, and in three ways.**

```
                        cache/table        stack        total
top-down (memo)         O(states)          O(depth)     O(states + depth)
bottom-up (table)       O(states)          0            O(states)
bottom-up (optimised)   O(window)          0            O(window)
```

```
Fibonacci, n = 100,000
  memoised     100,000 cache entries + 100,000 stack frames  -> CRASH at ~960
  table        100,000 ints in a list                        ~4 MB
  two vars     2 ints                                        ~56 bytes
```

**The recursion depth is the hard limit and it is not negotiable:**

```
Python usable frames                   ~960
sys.setrecursionlimit(200_000)         -> Segmentation fault (no traceback)
```

**So the rule is: `n` up to a couple of thousand, top-down is fine. Beyond that, bottom-up.**

**And the case that goes the other way — a sparse state space:**

```
coin change, amount = 100,000, denominations 1000 and 5000
  table fills                          100,001 cells
  reachable states                     105
                                       -> the table is 99.9% waste
```

```
in general:
  dense state space (every cell reachable)     -> bottom-up, no waste
  sparse state space (few cells reachable)     -> top-down wins, possibly hugely
```

**The constant factors, which are real but usually not decisive:**

```
bottom-up      an array index and an addition
top-down       a function call, a hash of the arguments, a dict lookup
               -> roughly 2-5x slower per state in Python
```

```
n = 1,000,000 states
  fib_table       ~0.15 s
  fib_memo        would crash, but at a depth that fits: ~0.6 s
```

**So bottom-up is faster per state and top-down may visit far fewer states.** Which wins depends entirely on
how sparse the state space is, and that is the question to ask rather than assuming.

**The space optimisation, sized:**

```
1D, window 2            O(n) -> O(1)          100,000 ints -> 2
2D, previous row only   O(m*n) -> O(n)        1,000,000 -> 1,000
2D, two rows needed     O(m*n) -> O(2n)       1,000,000 -> 2,000
```

**And what optimising costs you:**

```
full table    can reconstruct the path/subset/sequence by walking back
one row       only the final value survives
              -> reconstruction needs the table, or parent pointers
                 (which cost the memory you just saved)
```

**One more cost worth naming: `lru_cache` holds references.** A memoised function at module level keeps its
cache alive for the process, so a second test case sees the first one's entries. That is correct for pure
functions of their arguments and a real source of wrong answers when the function closes over changing data.
`cache_clear()` between cases, or build the cache inside the call.

---

## 7. The traps

### The loop running in the wrong direction

The conversion's only real difficulty, and it produces wrong answers with no error:

```python
for i in range(n, 1, -1):                 # recursion goes DOWN, so this is backwards
    dp[i] = dp[i - 1] + dp[i - 2]
```

```
>>> fib_backwards(10)
0                                          # everything read uninitialised zeros
```

**The rule: the loop runs opposite to the recursion.** `solve(i)` calls `solve(i-1)` → the loop goes upwards.
`solve(i)` calls `solve(i+1)` → the loop goes downwards. And when in doubt, check on `n = 3` by hand.

### The non-simultaneous assignment

```python
curr = prev + curr
prev = curr                               # prev gets the NEW curr
```

```
>>> fib_broken(10)
512                                        # powers of two, not Fibonacci
```

The tuple form `prev, curr = curr, prev + curr` evaluates the right side fully before assigning, which is
exactly what is needed. Two separate statements need a temporary.

### The one-row collapse in the wrong direction

```python
for j in range(n - 1, 0, -1):             # right to left
    row[j] += row[j - 1]
```

Correct for *some* recurrences and wrong for this one. Left to right gives `dp[i][j-1]` from the current row
and `dp[i-1][j]` from the previous; right to left gives `dp[i-1][j-1]` instead of `dp[i][j-1]`.

```
>>> paths_one_row_reversed(3, 3)
3                                          # the answer is 6
```

**Whenever a table collapses to one row, write down which of the two values each read is supposed to be**, and
choose the direction that delivers it. This is the knapsack subtlety and it is a silent wrong answer.

### Converting without the base cases

```python
dp = [0] * (n + 1)
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]          # dp[0] and dp[1] never set
return dp[n]
```

```
>>> fib_no_base(10)
0
```

Everything reads zeros and the whole table is zeros. **The base cases are step 2 of the conversion for a
reason** — they are the only values that do not come from the recurrence.

### Assuming the table is fully reachable

```python
dp = [0] * (amount + 1)
for i in range(1, amount + 1):
    ...                                    # fills 100,001 cells
```

Correct, and on a sparse problem it is almost entirely wasted work. **If the reachable states are a small
fraction of the table, top-down is not merely more convenient — it is asymptotically better in practice.** Ask
which states are reachable before choosing the form.

### `RecursionError` on the memoised version

```
Traceback (most recent call last):
  File "dp.py", line 8, in fib_memo
    return fib_memo(n - 1) + fib_memo(n - 2)
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

**The cache does not save you**, because the first descent reaches the base case before anything is stored.
Memoisation reduces the *number* of computations, not the *depth* of the first chain.

The workaround that is worse than the problem:

```python
sys.setrecursionlimit(1_000_000)
```

```
Segmentation fault (core dumped)
```

### Optimising space and then being asked for the path

```python
prev, curr = 0, 1
# ... "now show me which items you chose"
```

You cannot. The table recorded the decisions and you threw it away. **Ask whether the value alone is
sufficient before optimising**, and if the path is needed, either keep the table or store parent pointers —
which cost the memory the optimisation saved.

### A stale `lru_cache` across test cases

```python
@lru_cache(maxsize=None)
def solve(i):
    return grid[i] + solve(i - 1)          # closes over a MUTABLE global
```

The second test case changes `grid` and gets the first case's cached answers. No error, and the failure looks
like a wrong algorithm. **Memoise only pure functions of their arguments**, or clear the cache, or build it
inside the call.

---

## 8. In the interview

### How it gets asked

- *"Write it top-down. Now write it bottom-up."* — the direct version, and the most common DP follow-up.
- *"Can you reduce the space?"*
- *"Which would you use here, and why?"*
- *"Your solution crashes on the large input."* — the recursion depth.
- *"Now return the actual sequence, not just the length."* — the reconstruction question.

### The first ninety seconds

> "I would write the memoised version first, because it is the recursion I derived with a cache added, so it is
> much harder to get wrong under pressure — and then convert, because the conversion is mechanical.
>
> **The conversion is five steps.** The function's parameters become the table's dimensions. The base cases
> become the initial values. The recursive calls become table reads. Then the loop order — and this is the only
> step that requires thought. And finally return the cell for the original argument instead of calling the
> function.
>
> **The rule for the loop order is that the loop runs opposite to the recursion.** If `solve(i)` calls
> `solve(i-1)`, the recursion goes downwards, so the loop goes upwards — that way every cell a formula reads is
> already filled. Getting it backwards reads uninitialised zeros and gives a wrong answer with no error, so I
> would check it on `n = 3` by hand.
>
> **They compute the same values in a different order**, so the time is identical: states times work per state.
>
> **Two reasons I would convert.** Recursion depth — Python gives me about 960 usable frames, and the cache
> does not help because the first descent reaches the base case before anything is stored. So `n = 100,000`
> crashes memoised and is instant tabulated. And the space optimisation becomes visible: with the table in
> front of me I can see that each cell reads only the two below it, so I keep two variables instead of `n`.
>
> **And one reason I would not.** Top-down only computes the states it actually reaches. If the reachable
> states are a small fraction of the table — coin change with large denominations, say — bottom-up fills the
> whole thing and top-down visits a fraction of a percent of it. **Dense state space, bottom-up; sparse state
> space, top-down.**
>
> How large can `n` get? Because that usually settles it."

### The follow-ups

**"Reduce the space."**

> "By looking at what each cell actually reads, and keeping a window that wide.
>
> **Here `dp[i]` reads `dp[i-1]` and `dp[i-2]` and nothing else**, so at any moment I need two numbers and the
> rest of the array is history. Two variables rolled forward, `O(n)` to `O(1)`.
>
> **The general rule: the window is as deep as the recurrence reaches back.** Reaching back `k` means `k`
> values. In two dimensions, if `dp[i][j]` reads only row `i-1`, I keep one row instead of `m` — `O(m·n)`
> becomes `O(n)`.
>
> **And when it collapses to a single row, the iteration direction becomes part of the correctness.** Updating
> left to right means `row[j]` still holds the previous row's value when I read it, while `row[j-1]` already
> holds this row's — so I get 'above' and 'left', which is what unique paths needs. Right to left would give me
> 'above' and 'above-left', which is a different recurrence. **That is the classic knapsack subtlety, and it is
> a silent wrong answer**, so I would write down what each read is meant to be and pick the direction that
> delivers it.
>
> **What I give up:** the ability to say *which* choices produced the answer. The table recorded them and I
> threw it away. So if the problem wants the actual subset or path, I either keep the full table or store
> parent pointers — which cost the memory I just saved. **I would ask whether the value alone is enough before
> optimising**, because otherwise I optimise and then have to undo it."

**"Your solution crashes on the large input."**

> "Recursion depth, almost certainly, and the important part is that **memoisation does not prevent it.**
>
> The cache reduces how many computations happen, not how deep the first one goes. Calling `solve(100000)`
> descends a hundred thousand levels to reach the base case before a single value is stored, and Python gives
> me about 960 usable frames.
>
> **The fix is the bottom-up conversion**, which has no recursion at all.
>
> **The fix I would not use is raising the limit.** Past roughly a hundred thousand frames Python exhausts the
> C stack and you get a segmentation fault instead of a `RecursionError` — no traceback, nothing to debug.
> That is a worse failure, not a solution.
>
> **The alternative, if the state space is genuinely sparse and I want to keep top-down's advantage**, is to
> convert the recursion to an explicit stack — push the state, and if its dependencies are not yet computed,
> push them and revisit. That keeps the on-demand property without the frame limit, at the cost of noticeably
> more code. I would only reach for it if the table were mostly unreachable.
>
> **And I would check the other candidate before assuming:** if the crash is a `MemoryError` rather than a
> `RecursionError`, the problem is the cache or table size, not the depth, and the answer is the space
> optimisation instead."

**"Which form would you use, and why?"**

> "It depends on two things, and I would ask about both rather than have a default.
>
> **How big can the state space get?** Beyond a couple of thousand in any dimension that can recurse, top-down
> hits the frame limit and I convert. That is not a preference, it is a crash.
>
> **How much of the state space is actually reachable?** This is the one people miss. Bottom-up fills every
> cell; top-down visits only the states it reaches. For coin change with denominations of a thousand and five
> thousand and an amount of a hundred thousand, the table has a hundred thousand and one cells and only about
> a hundred and twenty are reachable — **the table is 99.9% waste.** Top-down gets that for free.
>
> **Beyond those two, top-down is easier to get right** and bottom-up is a bit faster per state — an array
> index and an addition against a function call, an argument hash and a dictionary lookup, so maybe two to five
> times per state in Python. That constant rarely decides anything.
>
> **In an interview I would write memoised first regardless**, because deriving the recurrence and adding a
> cache in front of someone shows the reasoning, whereas a table appearing fully formed does not. Then I would
> offer the conversion and the space optimisation as improvements, which is a better narrative than starting
> with the optimised version and being asked where it came from."

**"Now return the actual sequence, not just the length."**

> "Then I need the table, and I would say that before optimising rather than after.
>
> **With the full table, reconstruction is a backward walk.** Start at the answer cell and, at each step, work
> out which predecessor could have produced it — for a `max` recurrence, whichever branch equals the recorded
> value; for a counting one, follow whichever contributed. Push each choice onto a list and reverse at the end.
> `O(path length)` and no extra memory.
>
> **With parent pointers it is simpler and costs memory.** Store, alongside each cell, which predecessor it
> came from, and the walk is direct. That costs a second table the same size as the first, which is exactly the
> memory the space optimisation was saving — so parent pointers and space optimisation are mutually exclusive.
>
> **The thing to be careful about is ties.** If two predecessors give the same value, the reconstruction picks
> one arbitrarily and that is fine — but it means the returned sequence is *a* valid answer, not *the* answer,
> so a test asserting one specific sequence will be flaky. I would assert the length, or membership in a set of
> valid answers.
>
> **And there is a middle option worth knowing** when the table does not fit: divide and conquer over the DP —
> Hirschberg's approach for edit distance — which reconstructs the path in `O(n)` space rather than `O(n·m)` at
> the cost of recomputing halves. It is genuinely clever, rarely needed, and worth naming rather than
> attempting."

### The model answer

*"Given a staircase where step `i` costs `cost[i]`, and you may climb one or two steps at a time starting from
step 0 or step 1, find the minimum cost to reach the top. Write it both ways and reduce the space."*

> "Let me derive the recurrence first, then do both forms, because the conversion is mechanical once the
> recurrence is right.
>
> **The recurrence.** To stand on step `i`, I arrived from `i-1` or `i-2`, and I pay `cost[i]` to be here. So
> **`min_cost(i) = cost[i] + min(min_cost(i-1), min_cost(i-2))`**.
>
> **`dp[i]` = the minimum total cost to stand on step `i`.** I would write that as a comment, because the thing
> that catches people here is the difference between 'to stand on step `i`' and 'to get past step `i`'.
>
> **Base cases:** `dp[0] = cost[0]` and `dp[1] = cost[1]`, because the problem lets me start on either without
> paying to get there.
>
> **And the answer is `min(dp[n-1], dp[n-2])`, not `dp[n-1]`** — the top is *past* the last step, so I can
> finish from either of the last two. **That is the actual trap in this problem** and it is a modelling
> question, not a coding one; I would state it explicitly and check it against the two-element example by
> hand.
>
> **Top-down:**
>
> ```python
> @lru_cache(maxsize=None)
> def go(i):
>     if i < 0:   return 0
>     if i <= 1:  return cost[i]
>     return cost[i] + min(go(i-1), go(i-2))
> return min(go(n-1), go(n-2))
> ```
>
> **Then the conversion, five steps.** One parameter, so a one-dimensional table of size `n`. Base cases into
> `dp[0]` and `dp[1]`. Recursive calls become `dp[i-1]` and `dp[i-2]`. **The recursion goes downwards, so the
> loop goes upwards**, from index 2. And the answer is `min(dp[n-1], dp[n-2])`.
>
> ```python
> dp = [0] * n
> dp[0], dp[1] = cost[0], cost[1]
> for i in range(2, n):
>     dp[i] = cost[i] + min(dp[i-1], dp[i-2])
> return min(dp[n-1], dp[n-2])
> ```
>
> **Then the space.** `dp[i]` reads only `dp[i-1]` and `dp[i-2]`, so the window is two wide:
>
> ```python
> prev, curr = cost[0], cost[1]
> for i in range(2, n):
>     prev, curr = curr, cost[i] + min(prev, curr)
> return min(prev, curr)
> ```
>
> **Simultaneous assignment**, because writing it as two statements overwrites `prev` before it is read.
>
> **Cost:** `O(n)` time in every version — `n` states, constant work each. Space goes `O(n)` for the table,
> `O(n)` cache plus `O(n)` stack for the memoised version, and `O(1)` optimised.
>
> **Which I would ship:** the two-variable version, because the state space is dense so top-down has no
> advantage, and `n` could be large enough to matter for the recursion depth. **Which I would write in an
> interview:** the memoised one first, then convert out loud, because that shows the reasoning rather than
> presenting a result.
>
> **And if you asked me which steps to actually take** — I would need the table back, or parent pointers, and I
> would say that rather than pretend the optimised version can answer it."

---

## 9. Recall card

**Same recurrence, two directions.** Top-down starts at the answer and recurses to the base cases; bottom-up
starts at the base cases and fills forwards. **Identical time** — states × work per state.

**The conversion is five mechanical steps:** parameters → dimensions; base cases → initial values; recursive
calls → table reads; **work out the loop order**; return `dp[original argument]`. **The loop always runs
opposite to the recursion.**

**Convert for two reasons:** the recursion depth (~960 frames, and **memoisation does not help** — the first
descent reaches the base before anything is cached), and because the space optimisation becomes visible.

**Do not convert when the state space is sparse.** Coin change with denominations of 1000 and 5000 at amount
100,000: a table fills 100,001 cells, top-down visits **105**.

**Space window = how far back the recurrence reaches.** Two variables for `i-1, i-2`; one row when only the
previous row is read — and then **the iteration direction is part of the correctness**. Optimising throws away
the ability to reconstruct the path, so ask whether the value alone is enough first.
