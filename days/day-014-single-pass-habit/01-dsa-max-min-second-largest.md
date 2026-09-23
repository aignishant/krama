---
day: 14
track: dsa
title: "Max, min, second largest: the single-pass habit"
phase: "Arrays"
status: written
---

# Day 014 · DSA — Max, min, second largest: the single-pass habit

**After today you can:** You solve find-the-two-largest in one pass instead of reaching for sort.

**The interviewer asks it as:** *Find the second largest element without sorting.*

---

## 1. What this is, and why they ask it

If a question asks you for a **small, fixed number of extreme values** — the largest, the
largest and the smallest, the two largest — you do not need the data in order. You need one
walk through it, carrying that many variables. Sorting puts every element in its place; you
only ever wanted two of them.

The words *"without sorting"* in the question are not an arbitrary restriction. They are the
whole test. `sorted(items)[-2]` is `O(n log n)` and one line, and any candidate can produce it.
The interviewer wants to see whether you can get the same answer in `O(n)` with two variables,
and — far more revealing — whether you notice that **"second largest" is ambiguous** and ask
which one they mean before writing anything.

This appears as the opening question in phone screens everywhere, and the "find the k-th
largest" family it belongs to runs all the way to
[day 055](../day-055-quickselect/README.md) and
[day 113](../day-113-the-heap/README.md). It is also the day the single-pass reflex gets
installed: **when the answer is a handful of values, make one pass and keep a handful of
trackers.**

---

## 2. The story

Ravi teaches games at a school in Nagpur, and the annual sports day is the second Saturday of
December. The long jump is his event. Forty-eight children in the under-fourteen group, one
jump each, and he needs to be able to say who came first and who came second before the parents
start leaving at four.

For the first few years he did it the obvious way. Every child jumped, he measured, and he
typed the number into his phone. Then at the end he had forty-eight numbers to put in order,
with three teachers talking to him and a child crying about a foul, and it took him longer to
sort out the list than it had taken to run the whole event.

Now he does something else, and he does not keep forty-eight numbers at all. He keeps two,
in his head.

Before the first child jumps, he has nothing. The first child jumps 3.72 metres, so that is the
best so far, and there is no second best yet. The next child jumps 3.55, which is not better
than 3.72, so it becomes the second best. The third jumps 4.12, and this is the moment that
matters: the old best, 3.72, does not disappear. **It slides down and becomes the second best,
and 4.12 becomes the best.** The fourth child jumps 3.90, which is not better than 4.12 but is
better than 3.72, so it takes the second place and 3.72 is gone for good.

He carries on like that. Most jumps change nothing at all — he hears the number, sees that it
is smaller than both, and forgets it before the child is out of the pit. By the forty-eighth
jump he has the two numbers he needs and he never had to put anything in order.

One thing did catch him out, the year a boy and a girl both jumped exactly 4.55. He announced
the boy first and the girl second, and the girl's father asked, quite reasonably, how she could
be second with the same jump. Now, before the event starts, Ravi asks the head teacher which
way they want it: two firsts and no second, or a second place that has to be a genuinely
shorter jump. It takes ten seconds to ask and it saves the argument.

---

## 3. The idea in plain English

Ravi's two numbers are two variables, and his forty-eight jumps are one pass over an array.
That is the whole technique. What is left is getting the details right, and there are four of
them.

### One pass, one tracker: the maximum

```python
best = items[0]
for x in items[1:]:
    if x > best:
        best = x
```

Start with the first element, walk the rest, keep the bigger. After the loop, `best` holds the
largest. That is `n - 1` comparisons, `O(n)` time, and `O(1)` extra space — one variable,
however long the list is.

**Notice what `best` starts as.** It starts as a real element of the list, not as `0`. Starting
at `0` is the single most common bug in this family, and §7 shows it breaking on an all-negative
input.

If you must start from something that is not an element, use `float('-inf')` — a value
guaranteed to be smaller than every real number, so the first comparison always wins. There is
`float('inf')` for the other direction.

### Two trackers: the largest and the smallest, together

You do not need two passes for two answers.

```python
biggest = smallest = items[0]
for x in items[1:]:
    if x > biggest:
        biggest = x
    elif x < smallest:
        smallest = x
```

`elif` and not a second `if`, and it is worth knowing why: if `x` is bigger than the biggest so
far, it cannot possibly be smaller than the smallest so far, so checking is wasted work. That
makes it 1 comparison in the good case and 2 in the bad one, which is between `n` and `2n`
comparisons overall rather than the `2n` you would pay with two separate loops.

Both versions are `O(n)`. The reason to prefer one pass is not the complexity class — it is that
you touch the data once, which matters when "the data" is a file being streamed or a result set
arriving over the network and you cannot walk it twice.

### The second largest, and the question you must ask first

Here is `[5, 5, 3]`. What is the second largest?

- **5**, if "second largest" means the second element when you lay them out in order.
- **3**, if it means the second largest *distinct value*.

Both are defensible, both appear in real problem statements, and the two answers are different.
**Ask.** This is exactly Ravi and the father at the sand pit, and it is exactly the habit from
[day 008](../day-008-reading-a-problem/README.md).

The distinct version, which is what interviewers usually mean:

```python
first = second = None
for x in items:
    if first is None or x > first:
        first, second = x, first      # the old best slides down
    elif x != first and (second is None or x > second):
        second = x
```

Read the two branches carefully, because between them they are the whole problem.

**The first branch fires when `x` beats the current best.** The important half is
`second = first` — the old champion is not thrown away, it becomes the runner-up. Ravi's 3.72
sliding down to second place when 4.12 arrives is this line. Writing `first = x` and then
`second = first` on a separate line is a real bug, because by then `first` is already the new
value; §7 shows it returning the largest twice.

**The second branch fires when `x` is not the best but might be the runner-up.** Missing this
branch entirely is the other classic bug: on `[10, 1, 2]` the first branch fires only once, on
the 10, and `second` is never touched again.

The `x != first` test is what makes it *distinct*. Drop it and you get the by-position version:

```python
if first is None or x > first:
    first, second = x, first
elif second is None or x > second:
    second = x
```

Two lines apart, two different contracts, and the problem statement decides.

### The habit, stated generally

> **If the answer is a fixed, small number of extreme values, use one pass and that many
> trackers.** Sorting arranges all `n`; you only wanted `k` of them.

For `k = 1`, `2` or `3`, write the trackers by hand. Beyond that the code becomes unreadable
and error-prone, and the right structure is a **heap** of size `k`, giving `O(n log k)` — that
is [day 113](../day-113-the-heap/README.md). And if `k` is a large fraction of `n`, sorting is
genuinely the right call, or **quickselect** in `O(n)` average, which is
[day 055](../day-055-quickselect/README.md).

```
k = 1 or 2 or 3   ->  trackers, O(n)
k small but > 3   ->  heap of size k, O(n log k)
k close to n      ->  just sort, O(n log n)
```

### The comparison-count question

Some interviewers push further: *"can you find both the max and the min in fewer than 2n
comparisons?"* Yes, and the trick is to take elements **in pairs**.

Compare the two elements of a pair to each other first — one comparison. The winner can only
ever be the new maximum, and the loser can only ever be the new minimum, so each needs one
comparison instead of two. That is **3 comparisons per 2 elements**, so `3n/2` rather than `2n`:

```
n = 1,000,000   naive pairwise loop : 1,999,986 comparisons
                pairwise version    : 1,499,998 comparisons   -> 25% fewer
```

It is the same `O(n)`. Mention it as a refinement if asked for fewer comparisons; do not lead
with it.

### The library versions, and their cost

```python
max(items)              # O(n), raises ValueError on empty
min(items)              # O(n), raises ValueError on empty
max(items, default=0)   # O(n), returns the default instead of raising
sorted(items)[-2]       # O(n log n), IndexError if len < 2
heapq.nlargest(2, items)  # O(n log 2), returns a list
```

`max` and `min` are the same single pass written in C, so use them when the contract fits.
Their failure mode on an empty list is an exception, which is the same shape of problem as
`list.index()` on [day 012](../day-012-linear-search/README.md), and `default=` is the clean fix.

---

## 4. The picture

The two trackers walking the jumps, one child at a time:

```
   jump    3.72   3.55   4.12   3.90   3.61   4.55   3.44
           ----   ----   ----   ----   ----   ----   ----
   first   3.72   3.72   4.12   4.12   4.12   4.55   4.55
   second   --    3.55   3.72   3.90   3.90   4.12   4.12
                         ^^^^          ^^^^
                         the old first slides down
                                       nothing changes: 3.61 beats neither

   7 jumps, 2 variables, 1 walk. Nothing is ever put in order.
```

**What to notice:** the third column. When a new best arrives, the old best does not vanish —
it moves into second place. That single line, `second = first`, is what the whole exercise is
about, and it is the line people write in the wrong order.

The two branches, drawn as a decision:

```
   for each x:

              is x > first ?
             /             \
          yes               no
           |                 \
   second = first        is x > second (and, if distinct, x != first) ?
   first  = x               /              \
                          yes               no
                           |                 |
                     second = x          do nothing
                                         (most elements land here)
```

**What to notice:** there are three outcomes, not two, and the third one — do nothing — is where
the great majority of elements go. Forgetting the middle branch is the bug that survives the
example the interviewer showed you, because it only appears when the largest element comes
early.

Why sorting is the wrong tool, drawn:

```
   you asked for   :  the top 2 of 1,000,000

   sorting gives   :  [ #1  #2  #3  #4  #5 ....................... #1,000,000 ]
                        ^^^^^^^
                        you wanted these two
                                999,998 positions you paid for and did not use

   one pass gives  :  first = #1, second = #2
                      1,000,000 comparisons, 2 variables
```

**What to notice:** sorting solves a strictly larger problem than the one you were asked. The
cost of the extra work is the `log n` factor — 20 at a million elements — and `O(n)` extra
space, since `sorted()` builds a new list.

And the ambiguity, which is the part to raise out loud:

```
   items = [5, 5, 3]

   "second largest" as second in sorted order  ->  5   (5, 5, 3)
                                                        ^
   "second largest DISTINCT value"             ->  3   (5, 3)
                                                          ^
   items = [4, 4, 4, 4]

   as second in sorted order  ->  4
   as second distinct value   ->  there isn't one. None? An exception? Ask.
```

**What to notice:** on `[4, 4, 4, 4]` the distinct contract has no answer at all, so the
function needs a return convention for "does not exist" — the same conversation as
[day 012](../day-012-linear-search/README.md).

---

## 5. The code, built step by step

The maximum, with the initialisation done properly.

```python
def largest(items: list[int]) -> int:
    """The maximum. O(n) time, O(1) space. Raises on empty input."""
    if not items:
        raise ValueError("largest() of an empty list")
    best = items[0]
    for x in items[1:]:
        if x > best:
            best = x
    return best
```

`best = items[0]` rather than `best = 0`. The empty case is checked explicitly and raises,
matching what `max()` itself does — an empty list has no maximum, and inventing one is worse
than refusing.

Both extremes in one walk.

```python
def largest_and_smallest(items: list[int]) -> tuple[int, int]:
    """Both, in one pass. Two trackers, one walk. O(n) time, O(1) space."""
    if not items:
        raise ValueError("largest_and_smallest() of an empty list")
    biggest = smallest = items[0]
    for x in items[1:]:
        if x > biggest:
            biggest = x
        elif x < smallest:
            smallest = x
    return biggest, smallest
```

`biggest = smallest = items[0]` sets both to a real element, so neither can be wrong for lack of
a starting point. The `elif` saves a comparison whenever the first test succeeds.

The second largest, distinct values.

```python
def second_largest_distinct(items: list[int]) -> int | None:
    """Second largest DISTINCT value. None if there are fewer than two distinct values."""
    first = second = None
    for x in items:
        if first is None or x > first:
            first, second = x, first        # the old best slides down
        elif x != first and (second is None or x > second):
            second = x
    return second
```

`first, second = x, first` is one statement, so the right-hand side is built before either
assignment happens — no ordering bug is possible. Using `None` rather than `float('-inf')`
means the function works on any comparable type, not only numbers, and makes "there is no
answer" explicit in the return type.

The other contract, one condition apart.

```python
def second_largest_by_position(items: list[int]) -> int | None:
    """Second element in sorted order, duplicates counted. [5, 5, 3] -> 5."""
    if len(items) < 2:
        return None
    first = second = None
    for x in items:
        if first is None or x > first:
            first, second = x, first
        elif second is None or x > second:
            second = x
    return second
```

The only differences are the `len(items) < 2` guard and the missing `x != first`. Put both
functions side by side in an interview and the interviewer can see you understood the question
rather than guessed at it.

Here is the complete program.

```python
"""Day 14 — one pass, a few trackers, no sorting."""

import random
import time


def largest(items: list[int]) -> int:
    """The maximum. O(n) time, O(1) space. Raises on empty input."""
    if not items:
        raise ValueError("largest() of an empty list")
    best = items[0]
    for x in items[1:]:
        if x > best:
            best = x
    return best


def largest_and_smallest(items: list[int]) -> tuple[int, int]:
    """Both, in one pass. Two trackers, one walk. O(n) time, O(1) space."""
    if not items:
        raise ValueError("largest_and_smallest() of an empty list")
    biggest = smallest = items[0]
    for x in items[1:]:
        if x > biggest:
            biggest = x
        elif x < smallest:
            smallest = x
    return biggest, smallest


def second_largest_distinct(items: list[int]) -> int | None:
    """Second largest DISTINCT value. None if there are fewer than two distinct values."""
    first = second = None
    for x in items:
        if first is None or x > first:
            first, second = x, first        # the old best slides down
        elif x != first and (second is None or x > second):
            second = x
    return second


def second_largest_by_position(items: list[int]) -> int | None:
    """Second element in sorted order, duplicates counted. [5, 5, 3] -> 5."""
    if len(items) < 2:
        return None
    first = second = None
    for x in items:
        if first is None or x > first:
            first, second = x, first
        elif second is None or x > second:
            second = x
    return second


def count_comparisons_naive(items: list[int]) -> int:
    """Comparisons used by the obvious two-tracker loop."""
    if not items:
        return 0
    biggest = smallest = items[0]
    used = 0
    for x in items[1:]:
        used += 1
        if x > biggest:
            biggest = x
        else:
            used += 1
            if x < smallest:
                smallest = x
    return used


def count_comparisons_pairs(items: list[int]) -> int:
    """Comparisons used by the pairwise version: compare two, then each to one end."""
    n = len(items)
    if n == 0:
        return 0
    used = 0
    if n % 2 == 1:
        i = 1
    else:
        used += 1
        i = 2
    while i < n:
        used += 3                           # x vs y, then loser vs smallest, winner vs biggest
        i += 2
    return used


if __name__ == "__main__":
    jumps = [412, 388, 455, 455, 390, 401, 372]
    print(f"jumps            : {jumps}")
    print(f"largest          : {largest(jumps)}")
    print(f"largest, smallest: {largest_and_smallest(jumps)}")
    print(f"second (distinct): {second_largest_distinct(jumps)}")
    print(f"second (position): {second_largest_by_position(jumps)}")

    print("\nthe two contracts disagree, and the problem statement decides")
    CASES: list[tuple[str, list[int]]] = [
        ("normal",              [3, 9, 1, 7]),
        ("top value repeated",  [5, 5, 3]),
        ("all identical",       [4, 4, 4, 4]),
        ("two elements",        [2, 8]),
        ("one element",         [6]),
        ("empty",               []),
        ("all negative",        [-7, -2, -9]),
        ("zero and negatives",  [0, -3, -1]),
        ("largest is first",    [10, 1, 2]),
        ("largest is last",     [1, 2, 10]),
    ]
    print(f"  {'case':<20}{'input':<18}{'distinct':>10}{'by position':>14}")
    for label, data in CASES:
        d = second_largest_distinct(data)
        p = second_largest_by_position(data)
        print(f"  {label:<20}{str(data):<18}{str(d):>10}{str(p):>14}")

    print("\ncomparisons: naive two-tracker vs pairwise")
    random.seed(14)
    for n in (10, 1_000, 1_000_000):
        data = [random.randint(0, 10**9) for _ in range(n)]
        naive = count_comparisons_naive(data)
        pairs = count_comparisons_pairs(data)
        print(f"  n = {n:>9,}   naive {naive:>10,}   pairwise {pairs:>10,}"
              f"   saved {100 * (naive - pairs) / naive:>4.0f}%")

    print("\nsingle pass vs sorting (n = 2,000,000)")
    data = [random.randint(0, 10**9) for _ in range(2_000_000)]
    t0 = time.perf_counter(); a = second_largest_distinct(data); onepass = time.perf_counter() - t0
    t0 = time.perf_counter(); b = sorted(set(data))[-2];         bysort = time.perf_counter() - t0
    print(f"  one pass         : {onepass:>8.4f} s  -> {a}")
    print(f"  sorted(set(...)) : {bysort:>8.4f} s  -> {b}")
    print(f"  same answer?     : {a == b}")
    print(f"  one pass is {bysort / onepass:.1f}x faster and uses O(1) extra space")

    print("\nis the one-pass version right? 5000 random cases against a slow reference")
    mismatches = 0
    for _ in range(5000):
        size = random.randint(0, 8)
        data = [random.randint(-5, 5) for _ in range(size)]
        distinct = sorted(set(data), reverse=True)
        expected = distinct[1] if len(distinct) >= 2 else None
        if second_largest_distinct(data) != expected:
            mismatches += 1
    print(f"  mismatches: {mismatches}")
```

This is exactly what it printed:

```
jumps            : [412, 388, 455, 455, 390, 401, 372]
largest          : 455
largest, smallest: (455, 372)
second (distinct): 412
second (position): 455

the two contracts disagree, and the problem statement decides
  case                input               distinct   by position
  normal              [3, 9, 1, 7]               7             7
  top value repeated  [5, 5, 3]                  3             5
  all identical       [4, 4, 4, 4]            None             4
  two elements        [2, 8]                     2             2
  one element         [6]                     None          None
  empty               []                      None          None
  all negative        [-7, -2, -9]              -7            -7
  zero and negatives  [0, -3, -1]               -1            -1
  largest is first    [10, 1, 2]                 2             2
  largest is last     [1, 2, 10]                 2             2

comparisons: naive two-tracker vs pairwise
  n =        10   naive         15   pairwise         13   saved   13%
  n =     1,000   naive      1,991   pairwise      1,498   saved   25%
  n = 1,000,000   naive  1,999,986   pairwise  1,499,998   saved   25%

single pass vs sorting (n = 2,000,000)
  one pass         :   0.2250 s  -> 999998818
  sorted(set(...)) :   1.5771 s  -> 999998818
  same answer?     : True
  one pass is 7.0x faster and uses O(1) extra space

is the one-pass version right? 5000 random cases against a slow reference
  mismatches: 0
```

**Look at the two rows `top value repeated` and `all identical`.** Same input, two different
answers, and on `[4, 4, 4, 4]` one of the contracts has no answer at all. That is the sentence
to open the interview with.

**Look at `all negative`.** The answer is `-7`, and any version that starts its trackers at `0`
returns `0` — a number that is not in the list.

**Look at the timing.** Seven times faster, and the one-pass version also uses `O(1)` extra
space against the `O(n)` that `sorted(set(...))` needs for two new collections. The gap is
partly the `log n` factor and partly that sorting moves every element.

---

## 6. What it costs

**The maximum.** The loop body runs once per element after the first, and does one comparison:

```
n - 1 comparisons, exactly. Always. Best case = worst case.
```

`O(n)` time, `O(1)` extra space — one variable. There is **no way to do better**, and the
reason is worth being able to say: any element you have not looked at could be the largest, so
you must look at all of them. Same argument as absence in linear search on
[day 012](../day-012-linear-search/README.md).

**Both extremes, naively.** Two comparisons per element in the worst case:

```
2 x (n - 1) = 2n - 2 comparisons
```

The measured run gave 1,999,986 at `n = 1,000,000`, which is `2n - 14` — a handful fewer,
because sometimes the first test succeeds and the second is skipped.

**Both extremes, pairwise.** Take elements two at a time. One comparison to see which of the
pair is larger, then one comparison of the winner against the running maximum and one of the
loser against the running minimum:

```
3 comparisons for every 2 elements

n / 2 pairs x 3 = 3n / 2 comparisons
```

At `n = 1,000,000`:

```
3 x 1,000,000 / 2 = 1,500,000     against 2,000,000
                                  -> 25% fewer, which is what the run measured
```

Still `O(n)`. This is a constant-factor improvement, and the honest framing is: *"same
complexity, 25% fewer comparisons, and it is the answer if you're asked to minimise
comparisons."*

**The second largest.** One pass, at most two comparisons per element:

```
between n and 2n comparisons
O(n) time, O(1) extra space — two variables
```

**Against sorting.** At `n = 2,000,000`:

```
one pass       :  ~2,000,000 comparisons, 2 extra variables
sorted()       :  n log2 n = 2,000,000 x 21 = 42,000,000 comparisons,
                  plus a new list of 2,000,000 references = 16 MB
```

Twenty-one times the comparisons by that count; seven times slower when measured, because Python's
`sorted` is heavily optimised C and the one-pass loop is interpreted. **Both numbers are worth
saying.** The `log n` factor is real, and the constant factors work against you, which is why
the honest claim is "asymptotically better and measurably faster here", not "twenty-one times
faster".

**The general shape, which is the thing to remember:**

| You want | Method | Time | Extra space |
|---|---|---|---|
| The largest | 1 tracker, one pass | `O(n)` | `O(1)` |
| Largest and smallest | 2 trackers, one pass | `O(n)`, `3n/2` comparisons at best | `O(1)` |
| The two or three largest | 2–3 trackers, one pass | `O(n)` | `O(1)` |
| The `k` largest, `k` small | Heap of size `k` — [day 113](../day-113-the-heap/README.md) | `O(n log k)` | `O(k)` |
| The `k`-th largest, any `k` | Quickselect — [day 055](../day-055-quickselect/README.md) | `O(n)` average | `O(1)` |
| Everything in order | Sort | `O(n log n)` | `O(n)` |

---

## 7. The traps

### Trap one: initialising the tracker to zero

It looks harmless, it passes every example an interviewer is likely to show you, and it is
wrong.

```python
def largest(items):
    best = 0                            # looks harmless
    for x in items:
        if x > best:
            best = x
    return best


print(largest([-7, -2, -9]))
```

```
0
```

`0` is not in the list. Every element failed the `x > best` test, so the starting value was
returned unchanged. Temperatures, account balances, profit-and-loss figures and coordinates are
all routinely negative, and this bug ships.

Two correct fixes. Start from a real element:

```python
best = items[0]
```

Or start from something guaranteed to lose:

```python
best = float("-inf")
```

**The rule:** never initialise an extreme-value tracker to a made-up number. Use the first
element, or use infinity, and handle the empty case separately.

### Trap two: assigning in the wrong order

The near-miss. It runs, it returns a number, and the number is wrong.

```python
def second_largest(items):
    first = second = float("-inf")
    for x in items:
        if x > first:
            first = x
            second = first          # assigns the NEW first, not the old one
    return second


print(second_largest([3, 9, 1, 7]))
```

```
9
```

It returned the **largest**, twice. By the time `second = first` runs, `first` has already been
overwritten with `x`, so the old value is gone. The two lines are in the order they read in
English and the wrong order for the machine.

Two fixes. Save the old value first:

```python
second = first
first = x                            # order reversed
```

Or use one statement, so the ordering question cannot arise:

```python
first, second = x, first             # right-hand side is built before anything is assigned
```

The second form is the one to write. It is the same tuple-unpacking rule as the swap on
[day 013](../day-013-reverse-and-rotate/README.md).

### Trap three: no second branch

Also silent, and it only fails on inputs where the largest element comes early — which is not
the example anyone tests with.

```python
def second_largest(items):
    first = second = float("-inf")
    for x in items:
        if x > first:
            first, second = x, first
    return second                      # no elif branch at all


print(second_largest([10, 1, 2]))
```

```
-inf
```

The `if` fired once, on the 10. After that nothing beat `first`, so `second` was never updated
and the starting sentinel leaked out into the answer. On `[1, 2, 10]` the same function returns
`2` and looks perfectly correct, which is exactly why this survives casual testing.

The fix is the branch that handles "not the best, but maybe the runner-up":

```python
elif x != first and (second is None or x > second):
    second = x
```

**How to catch it every time:** test with the largest element first in the list. That input
breaks more second-largest implementations than any other.

### Trap four: the built-ins on short input

Both convenient one-liners have a failure mode on small lists.

```python
scores = []
print(max(scores))
```

```
Traceback (most recent call last):
  File "t14d.py", line 2, in <module>
    print(max(scores))
          ^^^^^^^^^^^
ValueError: max() iterable argument is empty
```

```python
scores = [6]
print(sorted(scores)[-2])
```

```
Traceback (most recent call last):
  File "t14e.py", line 2, in <module>
    print(sorted(scores)[-2])
          ~~~~~~~~~~~~~~^^^^
IndexError: list index out of range
```

Two different exceptions from two different one-liners, both on input a real caller will
eventually send. `max(items, default=None)` fixes the first. The second needs a length check —
and if you were going to write the check anyway, the hand-written pass is no longer any longer
than the shortcut.

---

## 8. In the interview

### How it gets asked

- *"Find the second largest element without sorting."* — the direct version. The last three
  words are the constraint that makes it a question at all.
- *"Find the maximum and the minimum in one pass. Can you do it in fewer than 2n
  comparisons?"* — the comparison-count version.
- *"Find the k-th largest element."* — the same family, one step harder. For small `k`, trackers;
  otherwise a heap or quickselect.
- *"What's the second highest salary?"* — the SQL phrasing of exactly this, and it has the same
  duplicates question hiding inside it.

### What to say out loud, in the first ninety seconds

1. **Ask the ambiguity question before anything else.** *"Quick check on the contract — for
   `[5, 5, 3]`, do you want 5 or 3? That is, second largest by position, or second largest
   distinct value?"* This is the sentence the question exists to elicit.
2. **Ask about the empty and one-element cases.** *"And if there aren't two distinct values —
   should I return None or raise?"*
3. **State the approach.** *"One pass, two variables: the best so far and the second best so
   far. No sorting needed, because I only want two of the n positions sorting would give me."*
4. **Name the tricky line before you write it.** *"The step people get wrong is that when a new
   maximum arrives, the old maximum has to slide down into second place. I'll write it as a
   single tuple assignment so the ordering can't bite me."*
5. **Name the second branch.** *"And there's a second case: a value that doesn't beat the best
   but does beat the runner-up. Missing that branch is why `[10, 1, 2]` fails while `[1, 2, 10]`
   passes."*
6. **Give the costs, and the comparison to sorting.** *"O(n) time, O(1) extra space — two
   variables regardless of size. Sorting would be O(n log n) and O(n) space to solve a strictly
   bigger problem than the one I was asked."*
7. **Say what you would do for general `k`.** *"For the k-th largest with k small, a heap of size
   k is O(n log k). For arbitrary k, quickselect is O(n) on average."*

### The follow-ups

**"What does `[5, 5, 3]` return?"**
That depends on the contract, and it is the first thing I would pin down. If "second largest"
means the second element in sorted order, the answer is 5, because the two 5s occupy the first
two places. If it means the second largest distinct value, the answer is 3. Both are used in
real problem statements. The implementations differ by one condition — `x != first` in the
second branch — so I would write whichever you want and note the other. And on `[4, 4, 4, 4]`
the distinct version has no answer, so it needs a return convention: I would use `None`, with
`int | None` on the signature so the caller is forced to check.

**"Can you find the max and min in fewer than 2n comparisons?"**
Yes, in `3n/2`. Take the elements in pairs. Compare the two members of the pair to each other
first — that costs one comparison and tells you which of them could possibly be a new maximum
and which could possibly be a new minimum. Then compare only the winner against the running
maximum and only the loser against the running minimum. Three comparisons for every two
elements instead of four. At a million elements that is 1.5 million rather than 2 million,
about 25% fewer. It is the same `O(n)`; it is a constant-factor answer to a constant-factor
question.

**"Now find the k-th largest."**
Three answers, depending on `k`. If `k` is 2 or 3, extend the trackers — still `O(n)` and
`O(1)`. If `k` is small relative to `n`, keep a min-heap of size `k`: push each element, and
pop when the heap grows past `k`, so the heap always holds the `k` largest seen so far and its
root is the answer. That is `O(n log k)` time and `O(k)` space. If `k` is arbitrary or close to
`n`, quickselect partitions around a pivot and recurses into one side only, giving `O(n)` on
average and `O(n²)` in the worst case unless you randomise the pivot. In production Python I
would write `heapq.nlargest(k, items)` and say so.

**"What if the data doesn't fit in memory, or arrives as a stream?"**
The one-pass version is already the answer, and that is its real advantage over sorting. It
needs `O(1)` memory and touches each element exactly once, so it works on a file read line by
line, or on records arriving over a socket, where you cannot go back and look again. Sorting
needs the whole dataset at once — for data that does not fit, that means an external merge
sort with disk passes. This is the case where the two approaches are not merely different in
complexity but different in what is possible.

### A model answer

> "First, a contract question, because 'second largest' is ambiguous. On `[5, 5, 3]`, do you
> want 5 — the second element in sorted order — or 3, the second largest distinct value? And if
> there is no such element, should I return None or raise?
>
> ...Right, distinct values, and None if there isn't one.
>
> I don't need the data sorted. Sorting arranges all n elements and I only want two of them, so
> that's O(n log n) and O(n) extra space to solve a bigger problem than I was asked. One pass
> with two variables does it in O(n) and O(1).
>
> ```python
> def second_largest(items: list[int]) -> int | None:
>     first = second = None
>     for x in items:
>         if first is None or x > first:
>             first, second = x, first
>         elif x != first and (second is None or x > second):
>             second = x
>     return second
> ```
>
> Two branches, and both matter. The first fires when x beats the current best — and the
> important half is that the old best slides down into second place rather than being thrown
> away. I've written it as a single tuple assignment, because writing `first = x` and then
> `second = first` on separate lines gives you the new value twice; that's a real bug and it
> returns the maximum rather than the runner-up.
>
> The second branch fires when x isn't the best but might be the runner-up. Leaving it out is
> the classic failure: `[1, 2, 10]` still works, but `[10, 1, 2]` returns the sentinel, because
> after the first element nothing ever beats the maximum again.
>
> The `x != first` is what makes it distinct — drop it and you get the by-position contract.
>
> Edge cases: empty list returns None. One element returns None. All-equal returns None, which
> is right for the distinct contract. Starting from None rather than 0 matters — a tracker
> initialised to 0 returns 0 on an all-negative list, which is a value that isn't in the input.
>
> Cost: n comparisons in the good case, up to 2n in the bad one. O(n) time, O(1) extra space —
> two variables however big the list is. And it works on a stream, which sorting doesn't,
> because it touches each element once and never looks back.
>
> If you wanted the k-th largest instead: for small k, a min-heap of size k gives O(n log k);
> for arbitrary k, quickselect gives O(n) on average."

That answer opens with the ambiguity, rejects sorting with a reason rather than a rule, names
both bug-prone lines *before* writing them, checks the edges, gives both costs, and generalises
at the end.

---

## 9. Recall card

1. **A fixed number of extreme values needs one pass and that many trackers.** Sorting arranges
   all `n` when you wanted `k`. `O(n)` time, `O(1)` space.
2. **Ask what "second largest" means on `[5, 5, 3]`** — 5 by position, 3 by distinct value. Two
   contracts, one condition apart, and `[4, 4, 4, 4]` has no distinct answer at all.
3. **When a new best arrives, the old best slides down.** Write it as `first, second = x, first`
   so the ordering bug cannot happen.
4. **The second branch is not optional.** Without `elif ... x > second`, `[10, 1, 2]` returns
   the sentinel. Always test with the largest element first.
5. **Never initialise a tracker to 0.** Use `items[0]` or `float('-inf')`, and handle empty
   separately — `max([])` raises `ValueError: max() iterable argument is empty`.
