---
day: 48
track: dsa
title: "Binary search on floats, and the epsilon question"
phase: "Binary search"
status: written
---

# Day 048 · DSA — Binary search on floats, and the epsilon question

**After today you can:** You can binary search a continuous range and decide when to stop.

**The interviewer asks it as:** *Find the square root of a number to six decimal places, without the library call.*

---

## 1. What this is, and why they ask it

Every binary search so far has run over whole numbers, and it stopped because the range eventually
held nothing. On a **continuous** range — real numbers rather than integers — that never happens. You
can always halve again, forever, and the range never becomes empty. So the halving is unchanged and
**the stopping rule is a new decision you have to make and defend**.

They ask it because it is the shortest problem where "correct" stops being a yes-or-no property. A
candidate who writes `while lo < hi` on floats produces a program that hangs; a candidate who writes
`while hi - lo > 1e-15` produces one that sometimes hangs, depending on the input; and a candidate who
says "I'll run a hundred iterations, because a hundred halvings takes any starting range below what a
double can even represent" has answered the actual question. Square root without `math.sqrt` is the
standard vehicle — LeetCode 69 in its integer form, and the six-decimal form as the follow-up — and
the same stopping decision shows up in every optimisation problem with a real-valued answer.

---

## 2. The story

Anitha's son is fourteen months old and he has his bath at about half past four, before it gets cool.

The bucket is a red plastic one that lives in the corner of the bathroom. There is a hot tap, and
there is a drum of water in the other corner that has been standing since morning and is cold.

She starts by knowing two things without testing anything at all. Water straight from the hot tap is
too hot for him — she has never had to check that. And water straight from the drum is too cold. So
whatever she wants is somewhere between the two, and she does not have to consider anything outside
that.

She half fills the bucket from the hot tap and pours in a good mug of cold, then puts her elbow in.
Still too warm. So she adds cold again — but only about half as much as last time, because the last
pour clearly overshot in the right direction and a full mug would take her past. Elbow in. Now it is
slightly cool. So a small splash back from the hot tap, smaller again than the last correction.
Elbow.

Each correction is about half the size of the one before it. That is not something she thinks about.
It is just that after the first pour she knows which side she is on, and the amount left to fix is
smaller than it was.

The interesting part is where she stops, and it is not where you would guess.

She does not stop when the water is exactly right, because there is no such moment. Her elbow cannot
tell one small difference from another. What happens is that after four or five corrections she puts
her elbow in and simply cannot tell any more whether it is a shade warm or a shade cool. That is the
signal. Not *it is correct* — *I can no longer tell the difference, and neither will he.*

Her mother-in-law, who has done this for four children and eleven grandchildren, does it in four
pours. Always four. She does not test at the end. She has done it so many times that she knows four
corrections from those two starting points is past the point where anybody's elbow could complain,
and she picks the baby up and gets on with it.

---

## 3. The idea in plain English

The hot tap and the cold drum are `lo` and `hi`. Each correction is a halving. And the difference
between Anitha's elbow-test and her mother-in-law's four pours is exactly the two stopping rules you
have to choose between.

### What changes, and what does not

The halving is identical to every day this week:

```python
lo, hi = 0.0, x
for _ in range(100):
    mid = (lo + hi) / 2          # NOT // -- this is real division now
    if mid * mid < x:
        lo = mid
    else:
        hi = mid
```

Two small differences from the integer version and one large one.

- `/` instead of `//`. Integer division would floor every midpoint and the search would stall.
- No `+ 1` or `- 1` anywhere. Between any two distinct real numbers there is another one, so there is
  no "next" value to step past. `lo = mid` and `hi = mid` are correct here and would hang on integers.
- And the large one: **the loop condition is no longer about the range being empty.** It cannot become
  empty.

### Why `while lo < hi` hangs

```python
lo, hi = 0.0, 2.0
while lo < hi:                   # <-- never becomes false
    mid = (lo + hi) / 2
    ...
```

Halving a positive gap gives a smaller positive gap. In exact arithmetic this runs forever. In
floating point it runs until `lo` and `hi` become adjacent representable numbers and `mid` equals one
of them — which happens after about fifty iterations for values near 1, and after a different number
for values near 10¹⁵. So it either hangs or terminates at an unpredictable point, and neither is
something you want to explain in an interview.

### Stopping rule one: an epsilon

**Epsilon**, written `eps`, is the size of the gap you are willing to accept:

```python
while hi - lo > 1e-9:
    ...
```

Read it as *"stop when the answer is pinned down to within a billionth."* It is Anitha's elbow.

The problem asks for six decimal places, so `1e-7` would do; `1e-9` gives two spare digits and costs
about seven extra iterations, which is nothing.

Two ways to get this wrong, and both are worth knowing:

- **Too large.** `1e-4` and the sixth decimal place is unreliable.
- **Too small.** `1e-18` is below what a 64-bit double can distinguish for numbers around 1, so
  `hi - lo` never gets there and the loop never ends. This is the failure that hangs.

### The absolute-versus-relative trap

An absolute epsilon means different things at different magnitudes:

```
answer near 1:            1e-9 is a billionth of the answer. Excellent.
answer near 10^15:        1e-9 is smaller than the gap between neighbouring
                          representable doubles at that size. Unreachable -> hangs.
```

A double holds about 15-17 significant decimal digits, so near 10¹⁵ the smallest distinguishable step
is about 0.125. Demanding `hi - lo > 1e-9` there is asking for something the number system cannot
express.

The fix is a **relative epsilon** — stop when the gap is small *compared to the value*:

```python
while hi - lo > 1e-9 * max(1.0, abs(lo)):
    ...
```

The `max(1.0, ...)` keeps it sane when the answer is near zero, where a relative test would demand
infinite precision.

### Stopping rule two: a fixed number of iterations

This is the mother-in-law, and it is what to write in an interview:

```python
for _ in range(100):
    ...
```

No condition, no epsilon, no hang. Every iteration halves the range, so after `k` iterations the
starting range has shrunk by a factor of `2^k`:

```
100 iterations:  range / 2^100  =  range / 1.27e30
```

Starting from a range of 10¹⁸, a hundred halvings leaves an interval of about 10⁻¹², which is far
below what a double can distinguish at any magnitude. **The loop cannot fail to converge and cannot
hang, on any input, ever.**

The cost is that it always does a hundred iterations even when ten would do. A hundred iterations of a
two-line body is a few microseconds. Say the trade out loud: *"I'd rather pay a fixed few microseconds
than debug a stopping condition."*

In practice 50 to 100 is the range people use. Fifty halvings is a factor of 10¹⁵, enough for almost
anything; a hundred is enough for everything.

### Prefer integers when you can

Before reaching for floats at all, ask whether the problem really needs them. LeetCode 69 asks for the
integer square root — the floor of the true root — and the whole thing can be done in integers:

```python
lo, hi = 0, x
while lo < hi:
    mid = (lo + hi + 1) // 2         # ceiling: this is "last True"
    if mid * mid <= x:
        lo = mid
    else:
        hi = mid - 1
return lo
```

Python's integers are exact and unbounded, so `mid * mid` is exact however large `x` is. The float
version of the same problem can return 2 for `x = 4` in some languages and 1.9999999999 in others.
**If the answer is an integer, search the integers.** It is one of the most reliable pieces of advice
in this subject.

### The one bound everyone gets wrong

For square root, the tempting range is `[0, x]`. It is wrong for `x < 1`:

```
x = 0.25   ->  sqrt(0.25) = 0.5, which is BIGGER than x
```

So the upper bound must be `max(1.0, x)`. This is the same lesson as
[day 046](../day-046-binary-search-on-the-answer/README.md)'s "if `works(hi)` is false, your range is
wrong", arriving in a new costume — and it is the input an interviewer will hand you.

---

## 4. The picture

The two starting facts, and the halving:

```
 lo = 0.0                                                     hi = max(1.0, x) = 10.0
  |------------------------------------------------------------------|
  |                    searching for sqrt(10) = 3.16227766...        |

 pass 1   mid = 5.0     5.0^2 = 25.0  > 10  ->  hi = 5.0
  |------------------------------|
 pass 2   mid = 2.5     2.5^2 = 6.25  < 10  ->  lo = 2.5
                 |--------------|
 pass 3   mid = 3.75    14.06        > 10  ->  hi = 3.75
                 |------|
 pass 4   mid = 3.125    9.77        < 10  ->  lo = 3.125
                     |--|
 pass 5   mid = 3.4375  11.82        > 10  ->  hi = 3.4375
                     |-|
  ...
 pass 30                                        lo ~ hi ~ 3.16227766017
```

**What to notice:** `lo = mid` and `hi = mid`, with no `+ 1` or `- 1` anywhere. On integers that would
hang; on reals it is the only correct move, because there is no "next" real number to step to.

Where the two stopping rules stop:

```
 gap after k halvings, starting from a range of 10:

 k =  10    gap ~ 0.0098          -- 2 decimal places
 k =  20    gap ~ 9.5e-6          -- 5 decimal places
 k =  30    gap ~ 9.3e-9          -- 8 decimal places   <- an eps of 1e-9 stops near here
 k =  50    gap ~ 8.9e-15         -- at the edge of double precision for values near 10
 k = 100    gap ~ 7.9e-30         -- far below anything representable. Cannot fail.

 asking for eps = 1e-18 with an answer near 10^15:
     smallest representable step at 10^15 is ~0.125
     hi - lo can NEVER get below 1e-18       -> infinite loop
```

**What to notice:** the fixed count has no input it can fail on. The epsilon has one, and it is the
input where the answer is large.

---

## 5. The code, built step by step

### The bounds

```python
lo, hi = 0.0, max(1.0, x)
```

`0.0` because a square root is never negative. `max(1.0, x)` because for `x` between 0 and 1 the root
is bigger than `x` itself, and an upper bound that excludes the answer makes the whole search
meaningless.

### The loop, with a fixed count

```python
for _ in range(100):
    mid = (lo + hi) / 2
    if mid * mid < x:
        lo = mid
    else:
        hi = mid
```

Two branches, no equality test. Note there is no `if mid * mid == x: return mid` — comparing floats
for equality is very nearly never right, and the loop converges on the exact value anyway.

### Returning the answer

```python
return (lo + hi) / 2
```

The midpoint of the final interval, not `lo` or `hi`. It halves the worst-case error at no cost, and
it is one of those small things an interviewer notices.

### The complete solution

```python
def sqrt_float(x: float, iterations: int = 100) -> float:
    """Square root of x >= 0, to full double precision, without math.sqrt.

    A fixed iteration count rather than an epsilon: 100 halvings shrink any starting
    range by a factor of 2^100, which is below what a double can represent at any
    magnitude. It cannot hang, on any input.
    """
    if x < 0:
        raise ValueError("no real square root of a negative number")
    if x == 0:
        return 0.0

    lo, hi = 0.0, max(1.0, x)          # max(1, x): for x < 1 the root EXCEEDS x
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2               # the midpoint halves the worst-case error


def sqrt_epsilon(x: float, eps: float = 1e-9) -> float:
    """The same search with a RELATIVE epsilon.

    The max(1.0, lo) is what stops it hanging when the answer is large: an absolute
    1e-9 is smaller than the gap between representable doubles above about 10^7.
    """
    if x < 0:
        raise ValueError("no real square root of a negative number")
    lo, hi = 0.0, max(1.0, x)
    while hi - lo > eps * max(1.0, lo):
        mid = (lo + hi) / 2
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def isqrt_int(x: int) -> int:
    """LeetCode 69. The FLOOR of the square root, computed entirely in integers.

    'Last True' form: the largest m with m*m <= x. Note the ceiling midpoint --
    without the + 1 this hangs when hi == lo + 1.
    """
    if x < 2:
        return x
    lo, hi = 1, x // 2                 # for x >= 2 the root is at most x // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def nth_root(x: float, n: int, iterations: int = 100) -> float:
    """The n-th root of x >= 0. Exactly the same search with a different question."""
    lo, hi = 0.0, max(1.0, x)
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if mid ** n < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    print(f"{sqrt_float(10):.10f}")        # 3.1622776602
    print(f"{sqrt_float(2):.10f}")         # 1.4142135624
    print(f"{sqrt_float(0.25):.10f}")      # 0.5000000000  <- the x < 1 case
    print(f"{sqrt_float(1e18):.4f}")       # 1000000000.0000
    print(sqrt_float(0), sqrt_float(1))    # 0.0 1.0

    print(f"{sqrt_epsilon(10):.10f}")      # 3.1622776610   <- eps stopped early: 9 digits, not 16
    print(f"{sqrt_epsilon(1e18):.4f}")     # 999999999.9073 <- relative eps survives, but loosely

    print(isqrt_int(8), isqrt_int(9), isqrt_int(10))     # 2 3 3
    print(isqrt_int(0), isqrt_int(1), isqrt_int(2))      # 0 1 1
    print(isqrt_int(10**18))                             # 1000000000

    print(f"{nth_root(27, 3):.6f}")        # 3.000000
    print(f"{nth_root(2, 10):.6f}")        # 1.071773
```

Run it. Three lines are worth watching. `sqrt_float(0.25)` is wrong on any version that uses
`hi = x`. `sqrt_epsilon(1e18)` hangs on any version with an *absolute* epsilon and merely loses
precision with a relative one. And compare the two `sqrt_epsilon` outputs against `sqrt_float` — the
epsilon version stops as soon as its tolerance is met, so it gives about nine good digits where the
fixed count gives every digit a double has. That is the second reason to prefer the fixed count: it
is not only safer, it is more accurate.

### The comparison you should never write

```python
if mid * mid == x:      # <-- do not
    return mid
```

`0.1 + 0.2 == 0.3` is `False` in Python, and for exactly the same reason `mid * mid` almost never
lands on `x` exactly. The test either never fires — costing nothing but noise — or fires accidentally
on a value that happens to round right. If you genuinely need to compare floats, compare with a
tolerance:

```python
from math import isclose
if isclose(mid * mid, x, rel_tol=1e-12):
    ...
```

---

## 6. What it costs

### Time, with a fixed count

```
100 iterations, each doing one division, one multiplication and one comparison
    -> 100 x O(1) = O(1) time, regardless of x
```

It is genuinely constant time, and saying so is worth a moment: the input's *size* does not change
the work, because the range is halved by a fixed factor each pass and the count is fixed.

### Time, with an epsilon

```
iterations = log2( (hi - lo) / eps )

range = 10,     eps = 1e-9   ->  log2(10 / 1e-9)   = log2(1e10)  ~ 34 iterations
range = 10^18,  eps = 1e-9   ->  log2(1e27)                      ~ 90 iterations
range = 10,     eps = 1e-18  ->                                  NEVER (unreachable)
```

So the epsilon version is `O(log((hi - lo) / eps))` and the fixed version is `O(1)` with a larger
constant. In practice:

```
34 iterations x ~3 float operations   ~ 100 operations   ~ 0.1 microseconds
100 iterations x ~3                   ~ 300 operations   ~ 0.3 microseconds
```

The difference between a smart stopping rule and a dumb one is two tenths of a microsecond. That is
the whole argument for the fixed count.

### Space

```
lo, hi, mid: three floats   -> O(1)
```

### Precision, stated properly

```
a 64-bit double holds ~15-17 significant decimal digits
machine epsilon (the smallest e with 1 + e != 1) ~ 2.22e-16

so near 1.0        the smallest distinguishable step is ~2.2e-16
   near 1e6                                              ~1.2e-10
   near 1e15                                             ~0.125
   near 1e18                                             ~128
```

That last line is why an absolute epsilon of `1e-9` is unreachable for large answers, and it is the
number to have ready if an interviewer pushes on precision.

---

## 7. The traps

### The real error: `while lo < hi` on floats

```python
lo, hi = 0.0, 10.0
count = 0
while lo < hi:
    mid = (lo + hi) / 2
    count += 1
    if mid * mid < 10:
        lo = mid
    else:
        hi = mid
print(count)
```

```
^C
Traceback (most recent call last):
  File "day48.py", line 3, in <module>
    while lo < hi:
KeyboardInterrupt
```

Nothing printed, no error, one core at 100%. Halving a positive gap gives a positive gap; the
condition is never false. The `+ 1` and `- 1` that made the integer version terminate do not exist on
reals, so the termination has to come from somewhere else — the count, or the epsilon.

### The near-miss: an absolute epsilon with a large answer

```python
def sqrt_absolute(x, eps=1e-9):
    lo, hi = 0.0, max(1.0, x)
    while hi - lo > eps:            # <-- absolute
        mid = (lo + hi) / 2
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

print(sqrt_absolute(10))            # 3.1622776601683795 -- fine
print(sqrt_absolute(1e18))          # hangs
```

It works on every small test and hangs on the large one. Above about 10⁷ the gap between neighbouring
doubles exceeds `1e-9`, so `hi - lo` reaches a floor it can never go below. The fix is
`eps * max(1.0, lo)` — a relative tolerance — or, better, the fixed count.

### The near-miss: `hi = x` when `x < 1`

```python
def sqrt_bad_bound(x):
    lo, hi = 0.0, x                 # <-- should be max(1.0, x)
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

print(sqrt_bad_bound(0.25))         # 0.25   should be 0.5
```

```
0.25
```

`sqrt(0.25)` is 0.5, which is outside `[0, 0.25]`. Every candidate in the range answers "too small",
`lo` climbs to the top of the range, and the function returns the top with total confidence. Same
failure as a wrong upper bound on [day 046](../day-046-binary-search-on-the-answer/README.md), and it
is the input the interviewer will hand you after your first three tests pass.

### The near-miss: float equality

```python
print(0.1 + 0.2 == 0.3)
print(0.1 + 0.2)
```

```
False
0.30000000000000004
```

`0.1` and `0.2` cannot be written exactly in binary, so their sum is not exactly `0.3`. Any binary
search that tries `if mid * mid == x: return mid` is relying on an event that almost never happens.
Delete the branch; the loop converges anyway.

### The trap: `//` left in by habit

```python
mid = (lo + hi) // 2               # <-- integer division on floats
```

This does not raise. `(0.0 + 10.0) // 2` is `5.0`, and `(3.0 + 4.0) // 2` is `3.0` — it floors. The
search stalls at whole numbers and returns an integer-valued answer for a problem asking for six
decimal places. It is a silent single-character bug, and the symptom is an answer that is right to
zero decimal places.

### The trap that is not really a trap: `mid` computed as `(lo + hi) / 2`

For integers this could overflow in a fixed-width language, and the safe form was
`lo + (hi - lo) / 2`. For doubles, `(lo + hi) / 2` can overflow only if both are near the maximum
double, around 10³⁰⁸, which does not happen in these problems. Use whichever you like, and mention
you know the difference.

---

## 8. In the interview

### How it gets asked

- *"Implement square root without the library function."* — and then, immediately, *"to six decimal
  places"*, which is where the interesting half starts.
- *"Return the integer square root."* — LeetCode 69, and the right first sentence is "I'll do this in
  integers".
- *"When does your loop stop, and why is that the right condition?"* — the real question, asked
  directly.
- As a **component**: any binary-search-on-the-answer problem where the answer is a real number —
  minimising the maximum distance to a petrol pump, maximising the average of a subarray — brings this
  stopping decision with it.

### What to say out loud, in the first ninety seconds

1. **Ask what kind of answer is wanted.** *"Do you want the integer square root, or a real number to a
   given precision? Those are different problems and I'd write them differently."*
2. **If integer, say so and stay in integers.** *"Then I'll search integers and keep the exactness —
   `mid * mid <= x` with Python's unbounded ints is exact at any size, and I avoid float rounding
   entirely."*
3. **State the bounds with the awkward case named.** *"Zero to max(1, x) — not zero to x, because for
   x below 1 the root is bigger than x and the answer would be outside my range."*
4. **Say what changes on floats.** *"No plus-one or minus-one, because between any two reals there's
   another one. `lo = mid` and `hi = mid` are correct here, and would hang on integers."*
5. **Announce the stopping rule and defend it.** *"I'll run a fixed hundred iterations rather than test
   an epsilon. A hundred halvings shrink any starting range by a factor of 2¹⁰⁰, which is far below
   what a double can distinguish at any magnitude — so it can't hang on any input. An epsilon can, if
   the answer is large."*

### The follow-ups

**"Why a fixed iteration count rather than an epsilon? Isn't that wasteful?"**
It is a little wasteful and it is a trade I would make every time. The epsilon version stops when
`hi - lo` falls below some tolerance, and the failure mode is that on some inputs it never does. A
64-bit double holds about fifteen to seventeen significant digits, so near 10¹⁵ the smallest gap
between two representable numbers is roughly 0.125 — asking for `hi - lo` below 1e-9 there is asking
for a number the format cannot express, and the loop spins forever. That bug passes every small test
and fails on the large input, which is the worst kind. A fixed hundred iterations shrinks any starting
range by 2¹⁰⁰, about 10³⁰, so it converges to full double precision from any starting range and
cannot hang on any input at all. The cost is a hundred iterations of a three-operation body — about
0.3 microseconds — where a smart epsilon might use thirty-four. I would rather pay two tenths of a
microsecond than own a stopping condition that has an input class it fails on. If I did want the
epsilon, I'd make it relative — `eps * max(1.0, lo)` — because that scales with the magnitude of the
answer and removes the failure.

**"Do it without floating point at all."**
For the integer square root that is straightforwardly better, and it is what I would reach for first.
The question becomes "the largest m with `m*m <= x`", which is a last-True boundary search over
integers, and in Python `m * m` is exact for any size of integer, so there is no rounding to reason
about. The one detail is the ceiling midpoint — `(lo + hi + 1) // 2` — because this is the maximise
form, and with a floor midpoint it hangs when `hi` is `lo + 1`. For a *fractional* answer without
floats, the honest route is fixed-point: decide the precision up front, multiply by 10⁶, and search
for the largest integer `m` with `m*m <= x * 10¹²`. That gives six exact decimal places with exact
integer arithmetic and no epsilon question at all. It is more code and it is the right answer when
the result feeds a financial calculation, where accumulated float error is a real problem — the same
reason money is stored as `NUMERIC` rather than `FLOAT`, which was
[day 026](../day-026-strings-revision/README.md)'s rule.

**"What if the function isn't `mid * mid` — what if it's something expensive?"**
Then the cost model changes and the stopping rule becomes a real decision rather than a free one. The
search is `O(iterations × cost of one evaluation)`, so if evaluating the predicate means a pass over
an array, a hundred iterations is a hundred passes. In that case I would tune the count rather than
leave it at a hundred: work out what precision the problem actually needs, take the log base two of
the starting range divided by that precision, and use that number with a small margin. For a
"minimise the maximum distance between petrol pumps" problem where the answer needs three decimal
places and the range is a thousand, that is log₂(10⁶), about twenty iterations, not a hundred — a
five-fold saving on real work. I would also say what I would *not* do, which is switch to an epsilon
loop to save iterations, because that reintroduces the hang. And if the predicate is smooth and I
need many digits, Newton's method converges quadratically — the number of correct digits doubles each
step, so about five steps instead of fifty — but it needs a derivative and a good starting guess, and
it is the wrong answer to a question about binary search unless the interviewer asks for the fastest
possible method.

### A model answer

> "First a clarifying question: do you want the integer square root, or a real number to a given
> precision? They're different problems. If it's the integer floor, I'd do it entirely in integers and
> avoid floats altogether — Python's integers are exact at any size, so `mid * mid <= x` never lies.
> Let me do the six-decimal version, since that's the harder one.
>
> The bounds are zero to max(1, x). Not zero to x — for x below 1, like 0.25, the root is 0.5, which
> is bigger than x, so a range of [0, x] wouldn't contain the answer and I'd return the top of the
> range with total confidence.
>
> The halving is the same as any binary search, with one change: no plus-one or minus-one. Between any
> two reals there's another one, so there's no 'next value' to step past — `lo = mid` and `hi = mid`
> are correct on floats and would hang on integers.
>
> Then the interesting decision, which is when to stop. `while lo < hi` never terminates, because
> halving a positive gap gives a positive gap. So I'll use a fixed iteration count:
>
> ```python
> def sqrt_float(x: float) -> float:
>     if x < 0:
>         raise ValueError("no real square root of a negative number")
>     lo, hi = 0.0, max(1.0, x)
>     for _ in range(100):
>         mid = (lo + hi) / 2
>         if mid * mid < x:
>             lo = mid
>         else:
>             hi = mid
>     return (lo + hi) / 2
> ```
>
> A hundred halvings shrink any starting range by 2¹⁰⁰ — about 10³⁰ — so it converges to full double
> precision whatever the input, and it cannot hang. The alternative is an epsilon, and I'd avoid the
> absolute version specifically: a double has about fifteen significant digits, so near 10¹⁵ the gap
> between representable numbers is roughly 0.125, and `while hi - lo > 1e-9` there spins forever. If I
> wanted an epsilon I'd make it relative — `eps * max(1.0, lo)`.
>
> I return the midpoint of the final interval rather than `lo`, which halves the worst-case error for
> free. And I've deliberately not written `if mid * mid == x: return mid` — float equality almost
> never fires, and the loop converges without it.
>
> Cost is O(1) — a hundred iterations regardless of input — and O(1) space. If the predicate were
> expensive rather than a multiplication, I'd size the count from the precision I actually need
> instead of leaving it at a hundred."

---

## 9. Recall card

- **On reals the range never empties**, so `while lo < hi` hangs and there is no `± 1` — `lo = mid`
  and `hi = mid` are correct. The stopping rule is a decision you must make and defend.
- **Prefer a fixed count: `for _ in range(100)`.** A hundred halvings shrink any range by 2¹⁰⁰, below
  double precision at every magnitude, so it cannot hang on any input. O(1) time, ~0.3 µs.
- **An absolute epsilon has an input class that hangs.** A double holds ~15-17 digits, so near 10¹⁵
  the smallest step is ~0.125 and `hi - lo > 1e-9` is unreachable. Use `eps * max(1.0, lo)` if you
  must use one.
- **`hi = max(1.0, x)`, never `hi = x`** — for `x < 1` the root exceeds `x`, and a range missing the
  answer returns its own edge, confidently. Return `(lo + hi) / 2`, and never test floats with `==`.
- **If the answer is an integer, search integers** — exact, no epsilon question, and remember the
  ceiling midpoint `(lo + hi + 1) // 2` for the last-True form. Fixed-point (× 10⁶) gives exact
  decimals without floats.
