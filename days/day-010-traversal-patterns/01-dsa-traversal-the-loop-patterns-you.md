---
day: 10
track: dsa
title: "Traversal: the loop patterns you will reuse forever"
phase: "Arrays"
status: written
---

# Day 010 · DSA — Traversal: the loop patterns you will reuse forever

**After today you can:** You can write forward, backward, paired and windowed loops without fighting the indices.

**The interviewer asks it as:** *Iterate over every adjacent pair in the array.*

---

## 1. What this is, and why they ask it

There are about seven ways to walk along an array, and you will use every one of them for the
next 170 days. Forwards. Backwards. Every position with its own number attached. Every
adjacent pair. Every group of `k` in a row. Two positions moving towards each other from the
ends. Every position with a step of more than one.

None of them is difficult. All of them have an off-by-one waiting in the loop bounds, and
that off-by-one is what actually costs people interviews.

Interviewers ask "iterate over every adjacent pair" because it is the smallest question that
exposes the problem. The obvious loop reads `for i in range(len(items))` and then touches
`items[i + 1]`, which runs off the end. Getting the bound right first time, and being able to
say *why* it is `len(items) - 1`, tells the interviewer that you think about index ranges
deliberately rather than adjusting them until the tests pass.

---

## 2. The story

It is four in the afternoon and Latha is on the terrace, taking in the washing before the
evening damp comes.

There are two lines running the width of the terrace, and she starts at the left-hand end of
the near one and works along it. Shirt, shirt, her son's trousers, two pillow covers, and so
on to the far end. She does not skip about. She takes each thing as she comes to it, and when
she reaches the wall she is done with that line.

The second line still has the morning's load to go up, and this she does the other way round,
starting at the far end and working back towards the stairs. It is not a preference. The tap
and the bucket are by the stairs, so if she started at the stairs she would spend the whole
time walking back past wet washing she had already hung.

The socks are their own job. There are eleven pairs on the second line and they are not in
order, so she goes along looking at each sock and the one next to it. Same colour, same
length — fold them together. Not a match — leave the first one and shift her attention along
by one, so that the sock she just rejected is now the left-hand one of the next comparison.
She works through the whole line that way and ends with two odd socks, which is normal.

Then there is the thing she learnt about this terrace over two monsoons. If three heavy items
hang next to each other — jeans, a towel, a bedsheet — the middle one does not dry, because
nothing gets past on either side. So before she leaves she walks the line once more and looks
at every run of three in a row: items one, two and three; then two, three and four; then
three, four and five. Each time she is looking at a group of three, and each time the group
slides along by one. If a group is all heavy, she moves the middle one to the end of the
line.

Her daughter comes up to help with the big bedsheet, which needs two people. Latha takes one
end and the girl takes the other, and they walk towards each other folding as they go until
their hands meet in the middle. That takes one crossing, not two.

The only thing that catches her out, every single time, is the pegs. There are fourteen pegs
on the near line and she always thinks there are fourteen gaps between them. There are
thirteen. She has been hanging washing on this terrace for nineteen years and she still has to
stop and count on her fingers.

---

## 3. The idea in plain English

Latha used five different ways of moving along a line, and every one of them is a loop you
will write dozens of times.

### 1. Forward, by position

The plain walk. Left to right, one at a time.

```python
for i in range(len(items)):
    print(items[i])
```

`range(len(items))` produces `0, 1, ..., n-1`. Exactly `n` values, and the last one is
`n − 1`, never `n`.

### 2. Forward, by value

When you do not need the position, ask for the values directly. This is the Python way and it
cannot go out of range.

```python
for x in items:
    print(x)
```

### 3. Forward, with both

`enumerate` gives you the position and the value together, which is what you want most of the
time.

```python
for i, x in enumerate(items):
    print(i, x)
```

`enumerate(items, start=1)` numbers from 1 if you need it. **Prefer this to
`range(len(items))` whenever you need both** — it is shorter, and it removes one place where
an index can be wrong.

### 4. Backward

Latha's second line. Three ways, all correct:

```python
for i in range(len(items) - 1, -1, -1):     # by position: start, stop-before, step
    print(items[i])

for x in reversed(items):                    # by value, no copy made
    print(x)

for i, x in reversed(list(enumerate(items))):  # both, at the cost of a copy
    print(i, x)
```

Read the first one carefully, because it is the one people get wrong. Start at `n − 1`, stop
**before** `−1` (so `0` is included), step by `−1`. Writing `range(len(items) - 1, 0, -1)`
silently skips element 0, and nothing will tell you.

`reversed(items)` does not build a reversed copy; it walks the original from the back. So it
is `O(1)` extra space, unlike `items[::-1]`, which is `O(n)`.

**When you actually need backwards:** when you are removing or overwriting elements and want
to avoid disturbing positions you have not visited yet, and when the answer depends on what
comes *after* each element — suffix sums, next-greater-element, and most of
[day 071](../day-071-monotonic-stack/README.md).

### 5. Adjacent pairs — and the off-by-one

This is today's interview question, and it is Latha's socks.

```python
for i in range(len(items) - 1):
    left, right = items[i], items[i + 1]
```

**The bound is `len(items) - 1`, and here is why.** The largest valid value of `i + 1` is
`n − 1`. So the largest valid `i` is `n − 2`. And `range(n - 1)` stops at `n − 2`. That is
exactly right.

It is the pegs and the gaps. `n` items have `n − 1` gaps between them. Fourteen pegs,
thirteen gaps. Say that sentence to yourself every time you write a pairs loop.

There is also a version with no arithmetic at all, which is worth knowing because it cannot
be off by one:

```python
for left, right in zip(items, items[1:]):
    ...
```

`zip` stops when the shorter sequence runs out, so the bound takes care of itself. The cost
is that `items[1:]` is a copy — `O(n)` extra space. For an interview, either is fine; say
which trade you are making.

### 6. A window of `k` in a row

Latha's three heavy items. A group of `k` consecutive elements, sliding along by one.

```python
k = 3
for start in range(len(items) - k + 1):
    window = items[start:start + k]
```

**The bound is `len(items) - k + 1`.** Check it with numbers rather than trusting it: with
`n = 5` and `k = 3`, that is `5 − 3 + 1 = 3` windows, starting at positions 0, 1 and 2, which
cover elements 0-1-2, 1-2-3 and 2-3-4. Three windows. Correct.

And notice that adjacent pairs is this with `k = 2`: `n − 2 + 1 = n − 1`. The two formulas are
the same formula.

Taking the slice each time costs `O(k)`, which makes the whole loop `O(n × k)`. The way to
keep it `O(n)` is to update a running total as the window moves — add the entering element,
subtract the leaving one. That is the sliding window technique, and it gets its own days from
[day 031](../day-031-fixed-window/README.md).

### 7. Two positions moving towards each other

Latha and her daughter and the bedsheet. One index at each end, both moving inward.

```python
left, right = 0, len(items) - 1
while left < right:
    ...
    left += 1
    right -= 1
```

`while left < right` stops when they meet. Use `left <= right` instead when the middle element
also needs handling. One crossing, `n / 2` steps, `O(n)` time and `O(1)` space — which is why
[day 007](../day-007-space-complexity/README.md)'s in-place reversal used it. This is the
two-pointer pattern, and it owns [day 027](../day-027-two-pointers-idea/README.md) onwards.

### 8. Stepping by more than one

```python
for i in range(0, len(items), 2):       # 0, 2, 4, ... every second element
for i in range(1, len(items), 2):       # 1, 3, 5, ... the odd positions
```

`range(start, stop, step)`. The third argument is the stride. Still `O(n / step)` iterations,
which is still `O(n)`.

### The one rule that prevents every off-by-one

Before writing a loop bound, ask: **what is the largest index I will actually touch inside the
body?** Then make the range stop one past it.

- Body touches `items[i]` → largest index `n − 1` → `range(n)`.
- Body touches `items[i + 1]` → largest index `n − 1`, so largest `i` is `n − 2` →
  `range(n - 1)`.
- Body touches `items[i + k - 1]` → largest `i` is `n − k` → `range(n - k + 1)`.

Three lines. Every array off-by-one you will ever write is one of these.

---

## 4. The picture

All seven patterns on the same seven-element array, showing which positions get visited and
in what order:

```
   index      0     1     2     3     4     5     6
           +-----+-----+-----+-----+-----+-----+-----+
   value   |  2  |  3  |  5  |  8  | 13  | 21  | 34  |
           +-----+-----+-----+-----+-----+-----+-----+

 1. forward           1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7      range(7)
                      0     1     2     3     4     5     6

 2. backward          7 <-- 6 <-- 5 <-- 4 <-- 3 <-- 2 <-- 1      range(6, -1, -1)
                      0     1     2     3     4     5     6

 3. adjacent pairs   [0,1] [1,2] [2,3] [3,4] [4,5] [5,6]         range(6)
                       ^                                          6 pairs, not 7
                     7 items, 6 gaps between them

 4. window of k=3    [0,1,2]
                       [1,2,3]
                         [2,3,4]
                           [3,4,5]
                             [4,5,6]                              range(7-3+1) = 5

 5. two pointers      L---------------------------->R
                      0                             6
                            L------------->R
                            1              5
                                  L-->R
                                  2    4
                                    meet at 3                     while left < right

 6. step of 2         *     .     *     .     *     .     *      range(0, 7, 2)
                      0           2           4           6

 7. nested (pairs)    i=0: j = 1,2,3,4,5,6
                      i=1: j = 2,3,4,5,6
                      i=2: j = 3,4,5,6      ...                   the staircase, O(n^2)
```

**What to notice in row 3:** six brackets under seven boxes. The pegs and the gaps. Every time
your loop body reaches for `items[i + 1]`, the number of iterations drops by exactly one.

**What to notice in row 4:** five windows over seven elements with `k = 3`, and the last window
starts at index 4, which is `n − k`. Count them on the picture rather than trusting the
formula, and the formula becomes obvious instead of memorised.

And here is the failure, drawn:

```
   for i in range(7):          <- WRONG bound for a pairs loop
       compare items[i], items[i + 1]

   i = 5:  items[5], items[6]     fine
   i = 6:  items[6], items[7]     <-- there is no items[7]
                          ^^^^
                          IndexError
```

**What to notice:** the loop is correct for six of its seven iterations. That is what makes
off-by-one errors so easy to write and so hard to spot by reading.

---

## 5. The code, built step by step

Write each pattern once, and make each one report the positions it visited, so that the bounds
are visible rather than assumed.

Start with the plain walk and the value walk.

```python
def forward_positions(items: list[int]) -> list[int]:
    visited = []
    for i in range(len(items)):
        visited.append(i)
    return visited
```

`range(len(items))` gives `0` to `n − 1`. Seven elements, seven visits.

Now backwards, with the bound that people get wrong.

```python
def backward_positions(items: list[int]) -> list[int]:
    visited = []
    for i in range(len(items) - 1, -1, -1):
        visited.append(i)
    return visited
```

Stop-before `−1` so that index `0` is included. Writing `-1` as the second argument looks odd
the first ten times and is exactly right.

Now the pairs loop, which is today's question.

```python
def adjacent_pairs(items: list[int]) -> list[tuple[int, int]]:
    pairs = []
    for i in range(len(items) - 1):
        pairs.append((items[i], items[i + 1]))
    return pairs
```

`len(items) - 1` because the body reaches for `i + 1`. Seven elements give six pairs.

Now the same thing with no arithmetic, for comparison.

```python
def adjacent_pairs_zip(items: list[int]) -> list[tuple[int, int]]:
    return list(zip(items, items[1:]))
```

`zip` stops at the shorter of the two, so the bound is automatic. `items[1:]` is a copy, so
this is `O(n)` extra space where the loop version is `O(1)`.

Now the sliding window.

```python
def windows_of(items: list[int], k: int) -> list[list[int]]:
    out = []
    for start in range(len(items) - k + 1):
        out.append(items[start:start + k])
    return out
```

If `k > len(items)` then `len(items) - k + 1` is zero or negative, `range` produces nothing,
and the function correctly returns an empty list. That is worth checking rather than assuming
— it is the kind of edge case
[day 008](../day-008-reading-a-problem/README.md) told you to write down.

And the window done properly, in `O(n)` rather than `O(n × k)`.

```python
def window_sums(items: list[int], k: int) -> list[int]:
    if k > len(items):
        return []
    total = sum(items[:k])                    # the first window, O(k)
    sums = [total]
    for i in range(k, len(items)):
        total += items[i] - items[i - k]      # add the new, drop the old
        sums.append(total)
    return sums
```

One line does the work: `items[i]` is entering the window and `items[i - k]` is leaving it.
That is the whole sliding-window idea, and everything from day 031 onwards is a variation of
it.

Now two pointers.

```python
def two_pointer_steps(items: list[int]) -> list[tuple[int, int]]:
    steps = []
    left, right = 0, len(items) - 1
    while left < right:
        steps.append((left, right))
        left += 1
        right -= 1
    return steps
```

Here is the complete program.

```python
"""Day 10 — the seven ways to walk an array, with the bounds made visible."""


def forward_positions(items: list[int]) -> list[int]:
    """range(n): 0 .. n-1"""
    return [i for i in range(len(items))]


def backward_positions(items: list[int]) -> list[int]:
    """range(n-1, -1, -1): n-1 .. 0. Stop-before is -1, so 0 is included."""
    return [i for i in range(len(items) - 1, -1, -1)]


def with_index(items: list[int]) -> list[tuple[int, int]]:
    """enumerate: position and value together, no manual indexing."""
    return [(i, x) for i, x in enumerate(items)]


def adjacent_pairs(items: list[int]) -> list[tuple[int, int]]:
    """range(n-1), because the body reaches for i+1. n items, n-1 gaps."""
    return [(items[i], items[i + 1]) for i in range(len(items) - 1)]


def windows_of(items: list[int], k: int) -> list[list[int]]:
    """range(n-k+1). O(n*k) because each slice costs O(k)."""
    return [items[s:s + k] for s in range(len(items) - k + 1)]


def window_sums(items: list[int], k: int) -> list[int]:
    """The same windows in O(n): add the entering element, subtract the leaving one."""
    if k <= 0 or k > len(items):
        return []
    total = sum(items[:k])
    sums = [total]
    for i in range(k, len(items)):
        total += items[i] - items[i - k]
        sums.append(total)
    return sums


def two_pointer_steps(items: list[int]) -> list[tuple[int, int]]:
    """From both ends, inward. n/2 iterations, O(1) space."""
    steps = []
    left, right = 0, len(items) - 1
    while left < right:
        steps.append((left, right))
        left += 1
        right -= 1
    return steps


def every_second(items: list[int]) -> list[int]:
    """range(0, n, 2): stride of 2."""
    return [items[i] for i in range(0, len(items), 2)]


if __name__ == "__main__":
    data = [2, 3, 5, 8, 13, 21, 34]
    n = len(data)
    print(f"array: {data}   (n = {n})\n")

    print(f"1. forward positions      : {forward_positions(data)}   -> {n} visits")
    print(f"2. backward positions     : {backward_positions(data)}   -> {n} visits")
    print(f"3. enumerate              : {with_index(data)[:3]} ...")
    pairs = adjacent_pairs(data)
    print(f"4. adjacent pairs         : {pairs}")
    print(f"                            -> {len(pairs)} pairs from {n} items. n-1, not n.")
    wins = windows_of(data, 3)
    print(f"5. windows of 3           : {wins}")
    print(f"                            -> {len(wins)} windows = n - k + 1 = {n} - 3 + 1")
    print(f"6. window sums, O(n)      : {window_sums(data, 3)}")
    print(f"                            -> matches {[sum(w) for w in wins]}")
    print(f"7. two pointers           : {two_pointer_steps(data)}")
    print(f"8. every second           : {every_second(data)}")

    print("\nthe edge cases that break careless bounds")
    for items, k in (([], 3), ([5], 3), ([1, 2], 3), ([1, 2, 3], 3)):
        print(f"  windows_of({str(items):<10}, k=3) -> {windows_of(items, k)}")
    print(f"  adjacent_pairs([])        -> {adjacent_pairs([])}")
    print(f"  adjacent_pairs([5])       -> {adjacent_pairs([5])}")
    print(f"  two_pointer_steps([5])    -> {two_pointer_steps([5])}")
```

This is exactly what it printed:

```
array: [2, 3, 5, 8, 13, 21, 34]   (n = 7)

1. forward positions      : [0, 1, 2, 3, 4, 5, 6]   -> 7 visits
2. backward positions     : [6, 5, 4, 3, 2, 1, 0]   -> 7 visits
3. enumerate              : [(0, 2), (1, 3), (2, 5)] ...
4. adjacent pairs         : [(2, 3), (3, 5), (5, 8), (8, 13), (13, 21), (21, 34)]
                            -> 6 pairs from 7 items. n-1, not n.
5. windows of 3           : [[2, 3, 5], [3, 5, 8], [5, 8, 13], [8, 13, 21], [13, 21, 34]]
                            -> 5 windows = n - k + 1 = 7 - 3 + 1
6. window sums, O(n)      : [10, 16, 26, 42, 68]
                            -> matches [10, 16, 26, 42, 68]
7. two pointers           : [(0, 6), (1, 5), (2, 4)]
8. every second           : [2, 5, 13, 34]

the edge cases that break careless bounds
  windows_of([]        , k=3) -> []
  windows_of([5]       , k=3) -> []
  windows_of([1, 2]    , k=3) -> []
  windows_of([1, 2, 3] , k=3) -> [[1, 2, 3]]
  adjacent_pairs([])        -> []
  adjacent_pairs([5])       -> []
  two_pointer_steps([5])    -> []
```

**Look at line 4 and line 5.** Six pairs from seven items; five windows of three from seven
items. Neither number is seven, and both formulas are the same formula with different `k`.

**Look at the edge cases block.** Every one returns an empty list rather than raising, and none
of them needed a special case — the arithmetic in the range bound handles them. That is what a
correct bound looks like: it degrades to "no iterations" instead of to an exception.

---

## 6. What it costs

Every pattern here is one pass, so every one is `O(n)` time. The differences are in the
constant and in the space.

| Pattern | Iterations | Time | Extra space |
|---|---|---|---|
| Forward, `range(n)` | `n` | `O(n)` | `O(1)` |
| Forward, `for x in items` | `n` | `O(n)` | `O(1)` |
| `enumerate(items)` | `n` | `O(n)` | `O(1)` |
| Backward, `reversed(items)` | `n` | `O(n)` | `O(1)` |
| Backward, `items[::-1]` | `n` | `O(n)` | **`O(n)`** — it copies |
| Adjacent pairs, index | `n − 1` | `O(n)` | `O(1)` |
| Adjacent pairs, `zip(items, items[1:])` | `n − 1` | `O(n)` | **`O(n)`** — the slice copies |
| Window of `k`, slicing | `n − k + 1` | **`O(n × k)`** | `O(k)` |
| Window of `k`, running total | `n − k + 1` | `O(n)` | `O(1)` |
| Two pointers | `n / 2` | `O(n)` | `O(1)` |
| Step of `s` | `n / s` | `O(n)` | `O(1)` |
| Nested pairs | `n(n − 1)/2` | `O(n²)` | `O(1)` |

**The two rows worth staring at are the window rows.** Same output, and one is `O(n × k)`
because it takes a fresh slice each time. At `n = 100,000` and `k = 1,000`:

```
slicing        : 100,000 x 1,000 = 100,000,000 element copies -> about 10 s in Python
running total  : 100,000 x 2     =       200,000 operations   -> about 0.02 s
```

**Five hundred times faster, for the same answer.** The `k` disappears because the running
total does two operations per step regardless of window size.

**Constant factors between the forward patterns.** All three are `O(n)` and they are not
equally fast, because `range(len(items))` plus `items[i]` does a bound check and an index
computation per element, while `for x in items` does neither:

```
n = 5,000,000
  for x in items              : 0.99 s
  for i, x in enumerate(items): 1.79 s
  for i in range(len(items))  : 1.77 s     (with items[i] in the body)
```

Nearly twice, purely from how the loop is written. Note that `enumerate` and
`range(len(...))` come out about level here — the saving is in not indexing at all. It never changes the Big-O and it is
free to get right, so the rule is: **iterate by value unless you need the index, and use
`enumerate` when you need both.**

**Why backwards costs nothing extra.** `reversed(items)` walks from the last address to the
first without building anything. `items[::-1]` allocates a whole second list. Same `O(n)`
time, and `O(1)` against `O(n)` space:

```
n = 1,000,000
  reversed(items)  :      0 KB extra
  items[::-1]      :  7,812 KB extra
```

**The bounds, as arithmetic.** Worth being able to derive rather than recall:

```
body touches items[i]           -> max index n-1 -> range(n)         -> n iterations
body touches items[i+1]         -> max i is n-2  -> range(n-1)       -> n-1 iterations
body touches items[i+k-1]       -> max i is n-k  -> range(n-k+1)     -> n-k+1 iterations
two pointers, left < right      ->                                   -> n/2 iterations
```

---

## 7. The traps

### Trap one: the pairs loop with the wrong bound

The one the interview question is designed to catch.

```python
def is_sorted(items: list[int]) -> bool:
    for i in range(len(items)):          # should be len(items) - 1
        if items[i] > items[i + 1]:
            return False
    return True

print(is_sorted([1, 2, 3, 4, 5]))
```

```
Traceback (most recent call last):
  File "d10.py", line 7, in <module>
    print(is_sorted([1, 2, 3, 4, 5]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d10.py", line 3, in is_sorted
    if items[i] > items[i + 1]:
       ~~~~~^^^
IndexError: list index out of range
```

Read where the `~~~~~^^^` marks point: at `items[i]`, which is the first subscript on that
line. On the final iteration `i` is 4 and `i + 1` is 5, and the list ends at 4.

The nastier version of this bug is the one that does **not** raise:

```python
def is_sorted(items: list[int]) -> bool:
    for i in range(len(items)):
        if items[i] > items[i - 1]:      # i - 1, not i + 1
            return False
    return True

print(is_sorted([5, 1, 2, 3]))     # prints True. It is not sorted.
```

No error at all, and a wrong answer. On the first iteration `i` is 0, so `items[i - 1]` is
`items[-1]` — which in Python is the **last** element, not an error. The comparison silently
wraps around the array. This is the single most dangerous thing about Python's negative
indexing, and it is why an off-by-one in Python can be quieter than the same bug in C.

**How to catch it every time:** before writing the range, name the largest index the body will
touch. `items[i + 1]` means `i` stops at `n − 2`, so the bound is `n − 1`. And when a loop
could produce `i - 1` on the first pass, start the loop at 1 instead of guarding inside it.

### Trap two: changing the list you are walking

This produces no error and skips elements, silently.

```python
items = [1, 2, 2, 3, 2, 4]
for x in items:
    if x == 2:
        items.remove(x)
print(items)
```

```
[1, 3, 2, 4]
```

One `2` survived. The reason is that the loop keeps an internal position that moves forward
while the list shrinks underneath it. Removing element 1 shifts everything left, so the next
step to position 2 skips what is now at position 1.

Walked through: position 0 is `1`, keep. Position 1 is `2`, removed — the list becomes
`[1, 2, 3, 2, 4]` and the loop advances to position 2, which is now `3`, so the `2` that slid
into position 1 is never examined.

Two correct fixes:

```python
items = [x for x in items if x != 2]        # build a new list — clear, O(n) space
```

```python
for i in range(len(items) - 1, -1, -1):     # walk backwards — in place, O(1) space
    if items[i] == 2:
        items.pop(i)
```

The backward version works because removing at position `i` only shifts elements *after* `i`,
and those are the ones already visited. **This is the main practical reason to walk backwards**,
and it is worth remembering as a rule: *if you are deleting while iterating, iterate
backwards.*

The genuinely `O(n)`-time, `O(1)`-space answer is the write pointer from
[day 007](../day-007-space-complexity/README.md), because `pop(i)` is itself `O(n)`, making
the backward loop `O(n²)`.

---

## 8. In the interview

### How it gets asked

- *"Iterate over every adjacent pair in the array."* — the direct version. The bound is the
  whole question.
- *"Check whether the array is sorted."* — the same question with a reason attached.
- *"Find the maximum sum of any k consecutive elements."* — the window version, and the good
  answer is `O(n)`, not `O(n × k)`.
- *"Why did you loop backwards there?"* — asked when you do it. Have the reason ready:
  deletion, or dependence on later elements.

### What to say out loud, in the first ninety seconds

1. **State the bound and its reason, before writing it.** *"I'll loop `i` from 0 to n minus
   2, because the body reaches for `i + 1` and the largest valid index is n minus 1."*
2. **Give the count.** *"So n items give n minus 1 pairs. Seven elements, six pairs."*
3. **Handle the small cases out loud.** *"With zero or one element there are no pairs, and
   `range(n - 1)` gives an empty range for both, so no special case is needed."*
4. **Mention the alternative and its trade.** *"`zip(items, items[1:])` does the same thing
   with no index arithmetic, but the slice is an O(n) copy. The index version is O(1)
   space."*
5. **State the complexity.** *"O(n) time, O(1) extra space."*
6. **If it is a window, offer the improvement unprompted.** *"For a window of k, slicing each
   time would be O(n×k). I'd keep a running total instead — add the entering element,
   subtract the leaving one — which is O(n) regardless of k."*

Step 3 is the one candidates skip and interviewers notice. Saying that the bound handles the
empty case *without* a special case is a small demonstration that you derived it rather than
recalled it.

### The follow-ups

**"Why `len(items) - 1` and not `len(items)`?"**
Because the body touches `items[i + 1]`, so the largest `i` I can allow is one less than the
largest valid index. The largest valid index is `n − 1`, so `i` must stop at `n − 2`, and
`range(n - 1)` stops at `n − 2`. The way I remember it is pegs and gaps: `n` items have
`n − 1` gaps between them. And it is the general formula — for a window of `k` the bound is
`n − k + 1`, and pairs are just `k = 2`.

**"What happens with an empty list?"**
`range(-1)` produces no values, so the loop body never runs and the function returns whatever
it should for "no pairs" — an empty list, or `True` for is-sorted. That is worth checking
rather than assuming, and it is the reason I prefer to derive the bound rather than write
`n - 1` from memory: a derived bound tends to degrade correctly at the edges.

**"When would you iterate backwards?"**
Three cases. When I'm deleting or shifting elements and don't want to disturb positions I have
not visited — removing forwards skips elements silently, removing backwards does not. When
the answer for each element depends on what comes after it: suffix sums, next-greater-element,
and most monotonic-stack problems. And when I'm filling an array in place from the end, as in
merging two sorted arrays into the first one, where writing forwards would overwrite data I
still need.

**"Your window solution slices each time. What does that cost?"**
`O(k)` per window and `O(n × k)` overall, which at n of a hundred thousand and k of a
thousand is 10⁸ element copies — several seconds in Python. The fix is to maintain a running
total instead of rebuilding the window: when the window moves right by one, add the element
entering and subtract the one leaving. That is two operations per step regardless of `k`, so
it is `O(n)` and `O(1)` space. It only works for quantities you can undo — sums and counts
yes, maximum no, which is why sliding-window maximum needs a deque instead.

### A model answer

> "Sure. The key decision is the loop bound, so let me say it before I write it: the body
> reaches for `items[i + 1]`, and the largest valid index is `n − 1`, so `i` has to stop at
> `n − 2`. That means `range(len(items) - 1)`.
>
> ```python
> for i in range(len(items) - 1):
>     left, right = items[i], items[i + 1]
> ```
>
> Seven elements give six pairs — `n` items have `n − 1` gaps between them, like pegs on a
> line. And the bound handles the small cases without a guard: for an empty list or a single
> element, `range(-1)` and `range(0)` both produce nothing, so the body never runs and there
> are correctly no pairs.
>
> That's O(n) time and O(1) extra space.
>
> There's an alternative with no arithmetic at all — `zip(items, items[1:])` — which is
> harder to get wrong because `zip` stops at the shorter sequence. The trade is that
> `items[1:]` is a full copy, so it's O(n) space instead of O(1). I'd use the index version
> when space matters and the zip version when clarity matters more.
>
> One thing I'd flag if the loop were doing deletion rather than comparison: iterating
> forwards while removing elements silently skips items, because the list shrinks under the
> loop's position. For that case I'd iterate backwards, or use a write pointer, which is O(n)
> rather than the O(n²) you get from repeated `pop`.
>
> And if this generalises to a window of `k` rather than pairs, the bound becomes
> `range(n - k + 1)` — the same derivation — and I'd maintain a running total rather than
> re-slicing, to keep it O(n) instead of O(n × k)."

That answer derives the bound rather than stating it, checks the edges, gives an alternative
with its trade, and generalises — all in about ninety seconds.

---

## 9. Recall card

1. **Derive the bound, do not recall it.** Ask what the largest index the body touches is, and
   stop one past it. `items[i]` → `range(n)`. `items[i+1]` → `range(n-1)`. `items[i+k-1]` →
   `range(n-k+1)`.
2. **`n` items have `n − 1` gaps.** Seven elements, six adjacent pairs. Pegs and gaps.
3. **Backwards is `range(n-1, -1, -1)`** — stop-before is `−1` so index 0 is included. Or
   `reversed(items)`, which copies nothing.
4. **Iterate by value; use `enumerate` when you need the index.** `range(len(items))` with
   `items[i]` is nearly 2× slower and has one more thing to get wrong.
5. **Never delete while iterating forwards** — it skips elements silently. Go backwards, or
   use a write pointer. And a sliding window should keep a running total, not re-slice.
