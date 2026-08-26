---
day: 13
track: dsa
title: "Reversing, rotating, and swapping in place"
phase: "Arrays"
status: written
---

# Day 013 · DSA — Reversing, rotating, and swapping in place

**After today you can:** You can rotate an array by k using the three-reversal trick and explain why it works.

**The interviewer asks it as:** *Rotate the array to the right by k, in O(1) extra space.*

---

## 1. What this is, and why they ask it

**Rotating** an array means moving every element along by `k` positions, with the ones that
fall off the end wrapping round to the start. **Reversing** means turning the whole thing back
to front. Both can be done **in place** — changing the array you were given, using a fixed
handful of extra variables rather than building a second array.

The reason this is asked is the phrase *"in O(1) extra space"*. Every candidate can rotate an
array by building a new one. The interviewer removes that option and watches what happens. The
expected answer is a trick that looks like nothing at first sight — **reverse the whole array,
then reverse the two pieces** — and the follow-up is always the same: *why does that work?*
Being able to answer that, rather than having memorised three lines, is the entire test.

It appears constantly. LeetCode 189 is a standard phone-screen question at Amazon, Microsoft
and Google, and the reversal idea comes back on [day 017](../day-017-matrix-tricks/README.md)
for rotating a matrix, on [day 023](../day-023-palindromes/README.md) for palindromes, and on
[day 081](../day-081-reversing-a-list/README.md) for reversing a linked list. It is worth
paying for once.

---

## 2. The story

Nazia's grandmother turns eighty on a Sunday, and the whole family comes to the house in
Jaipur for it. At about six in the evening somebody says they should take one photo with
everyone in it, because the last one was nine years ago and two of the people in it have died
since.

Getting fifteen people to stand in a line takes twenty minutes. They end up standing by
height, tallest on the left, down to the four smallest children on the right. Then Nazia's
uncle, who is holding the camera, says the children cannot be at that end because nobody will
be able to see them, and asks for them at the front instead — in the same order they are
already standing in, because the two youngest are twins and their mother wants them next to
each other the way they are.

The obvious thing is to walk the last child up to the front, then the next one, then the next.
Nazia watches this start and stop. Each child has to squeeze past eleven adults, everybody
shuffles sideways to make room, one of them stands on her aunt's foot, and after two minutes
only one child has moved.

Her uncle puts the camera down and says three sentences instead.

"Everybody turn round, face the other way, and walk to the other end of the line without
changing who is beside you." The whole line turns itself back to front. The four children are
now on the left where he wants them, although among themselves they are the wrong way round,
and so is everybody else.

"Now the four of you on the left — you four only — do the same thing among yourselves." The
four children move round within their own little group, and now they are back in the order
they started in.

"And the eleven of you on the right, same thing." Eleven people turn themselves round.

It takes about forty seconds. Nobody squeezes past anybody. Everyone ends up exactly where he
wanted them, and the photo is taken before the light goes.

---

## 3. The idea in plain English

Nazia's uncle did a rotation in three reversals. Everything below is that, said carefully.

### First: swapping two elements

Every operation today is built out of one move — exchanging the values at two positions.

```python
items[0], items[6] = items[6], items[0]
```

Python builds the pair `(items[6], items[0])` on the right first, then unpacks it into the two
places on the left. Because the right-hand side is fully evaluated before anything is
assigned, no temporary variable of your own is needed. In Java or C you would need one:

```
temp = items[0]; items[0] = items[6]; items[6] = temp;
```

That is worth knowing, because an interviewer may ask you to write it in a language without
tuple unpacking, and because it explains what "constant extra space" means — one variable, no
matter how big the array is.

### Reversing in place

To reverse, put one marker at each end, swap what they are looking at, and walk them towards
each other until they meet.

```python
while left < right:
    items[left], items[right] = items[right], items[left]
    left += 1
    right -= 1
```

**`left < right`, not `left <= right`.** When the two meet in the middle of an odd-length
array they are on the same element, and swapping an element with itself is pointless. It is
not wrong — it just does nothing — but `<` says what you mean.

The number of swaps is `n // 2`, because each swap places two elements at once. Seven elements
need three swaps; the middle one never moves.

This is your first **two-pointer** loop, and the whole of days 27 to 36 is built on it. A
**pointer** here just means an integer holding a position — nothing to do with pointers in C.

### What "rotate right by k" actually means

Rotating right by 3 takes the last three elements and puts them at the front, keeping their
order:

```
[1, 2, 3, 4, 5, 6, 7]  rotate right by 3  ->  [5, 6, 7, 1, 2, 3, 4]
```

Every element moved three places to the right, and the three that ran off the end came back at
the beginning. The element that was at position `i` is now at position `(i + k) % n`.

**Rotating left is the same operation with a different `k`.** Rotating left by 3 on seven
elements gives the same result as rotating right by 4, because `7 - 3 = 4`. So:

```
rotate left by k   ==   rotate right by (n - k)
```

If a problem says "left" and you only remember "right", convert and say so out loud. That is a
better answer than getting the direction wrong.

### `k` can be bigger than the array

If you rotate seven elements by seven, you get back exactly what you started with. So rotating
by 10 is the same as rotating by 3. The first real line of every rotate function is therefore:

```python
k %= n
```

Miss it and you get an `IndexError` on a bigger `k`, which §7 shows in full. This is the single
most common reason a correct-looking rotate fails the hidden tests.

Two things to be careful about. `n` must not be zero, because `k % 0` raises
`ZeroDivisionError` — so check for the empty array first. And in Python, `%` on a negative `k`
already returns a non-negative result: `-3 % 7` is `4`, which is exactly the "rotate left by 3"
answer. That is a convenient accident, and it is not true in C or Java, where `-3 % 7` is `-3`.

### The three ways to rotate, and why only one of them is the answer

**Way one — build a new array.** Take the last `k`, then the first `n - k`, and stick them
together.

```python
items[:] = items[n - k:] + items[:n - k]
```

Correct, one line, `O(n)` time. It uses `O(n)` extra space, which is exactly what the question
forbade. Note `items[:] =` and not `items =` — that difference is trap two in §7 and it is
worth more marks than the rest of the line.

**Way two — move one element at a time, `k` times.** Take the last element off, put it at the
front, repeat.

```python
for _ in range(k):
    items.insert(0, items.pop())
```

`O(1)` space and honest, but each `insert(0, ...)` shifts every element right by one, which is
the `O(n)` cost from [day 011](../day-011-insert-and-delete/README.md). Doing that `k` times is
`O(n × k)`. At `n = 1,000,000` and `k = 500,000` that is 5 × 10¹¹ moves — hours, not seconds.

**Way three — three reversals.** `O(n)` time, `O(1)` space, and the answer they want.

```python
reverse(items, 0, n - 1)      # the whole thing
reverse(items, 0, k - 1)      # the first k
reverse(items, k, n - 1)      # the rest
```

### Why the three reversals work

This is the part to be able to explain, and it is easier than it looks if you say it in two
steps.

**Step one: reversing the whole array gets the right elements onto the right side.** The last
`k` elements were at the back; after a full reversal they are at the front. That is the part
you wanted. The elements that were at the front are now at the back, which is also what you
wanted.

**Step two: but reversing scrambled the order inside each group.** The last three of
`[1,2,3,4,5,6,7]` are `[5,6,7]`. After reversing everything they sit at the front as `[7,6,5]`
— right place, wrong order. Reversing that group of three on its own turns `[7,6,5]` back into
`[5,6,7]`. Do the same to the other group and both are correct.

Said in one sentence for the interview: **"reversing the whole array puts both groups on the
correct side but back to front within themselves, so I reverse each group again to undo
that."**

There is a second way to see it, which some interviewers prefer. Reversing twice returns you
to where you started. The three reversals reverse each element exactly twice — once as part of
the whole, once as part of its group — so within a group nothing has changed, while the groups
themselves have swapped places.

### The fourth way, which is worth knowing about

**Cyclic replacement** moves each element straight to its final home in one hop and carries the
element it displaced. It touches each element exactly once, so it does `n` writes rather than
about `n` swaps.

The catch is that following `i -> (i + k) % n` repeatedly does not always visit everything. If
`n = 6` and `k = 2`, you visit `0, 2, 4, 0` and stop — you have to start again from 1. The
number of separate cycles is `gcd(n, k)`, which is why the code needs an outer loop and a
counter.

It is genuinely harder to get right under pressure, and it is not faster in any way that
matters. **Mention it, do not lead with it.** "There is also a cyclic-replacement version that
does n writes instead of about n swaps, but it needs a gcd argument to show it terminates, so
I would write the reversal one" is a strong sentence.

---

## 4. The picture

The two-pointer reversal, on seven elements:

```
   position   0     1     2     3     4     5     6
           +-----+-----+-----+-----+-----+-----+-----+
   value   |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
           +-----+-----+-----+-----+-----+-----+-----+
              L                                   R      swap 1 and 7
                    L                       R            swap 2 and 6
                          L           R                  swap 3 and 5
                                L=R                      stop: left < right is false

           +-----+-----+-----+-----+-----+-----+-----+
           |  7  |  6  |  5  |  4  |  3  |  2  |  1  |
           +-----+-----+-----+-----+-----+-----+-----+

   7 elements, 3 swaps. The middle one never moved.
```

**What to notice:** the loop stops when the two markers meet, not when either of them has
crossed the whole array. Running to the end would reverse it and then reverse it back — that is
trap three.

Now the rotation, drawn as the three reversals with `k = 3`:

```
   want: rotate right by 3

   start          [ 1   2   3   4 | 5   6   7 ]
                    the first 4     the last 3
                                      ^ these three must end up at the front

   reverse all    [ 7   6   5 | 4   3   2   1 ]
                    ^^^^^^^^^   ^^^^^^^^^^^^^
                    right side   right side
                    wrong order  wrong order

   reverse [0..2] [ 5   6   7 | 4   3   2   1 ]
                    ^^^^^^^^^ fixed

   reverse [3..6] [ 5   6   7 | 1   2   3   4 ]
                                ^^^^^^^^^^^^^ fixed

   done           [ 5   6   7   1   2   3   4 ]
```

**What to notice:** after the first line every element is already on the side it belongs on.
The two reversals that follow do not move anything across the boundary — they only tidy up
inside each side. That is the whole proof, and it fits in a picture.

The `k % n` reduction, drawn:

```
   n = 7, k = 10

   rotating by 7 returns the array to exactly where it started.
   10 = 7 + 3, so rotating by 10 is one free full turn plus a rotation by 3.

   k:   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14
        |___________________________|   |___________________|   |
        one full turn                   another one             and so on

   10 % 7 = 3     -->  do the work for k = 3
```

**What to notice:** without this line, `reverse(items, 0, k - 1)` is asked to reverse the first
ten elements of a seven-element array, and the crash is immediate.

And the three methods against each other, so the choice is visible:

```
   n = 1,000,000, k = 500,000

   build a new array   time O(n)    :           1,000,000 moves   space 8 MB extra
   one at a time       time O(n*k)  :     500,000,000,000 moves   space O(1)
   three reversals     time O(n)    :           1,000,000 swaps   space O(1)   <-- the answer
```

**What to notice:** the middle row is not slightly worse, it is five hundred thousand times
worse. This is the [day 004](../day-004-the-growth-curves/README.md) point arriving inside a
real question.

---

## 5. The code, built step by step

Start with the one operation everything is made of.

```python
items[a], items[b] = items[b], items[a]
```

The right-hand side is evaluated into a pair before either assignment happens, so this is a
true exchange with no temporary of your own. In a language without it, you write three lines
and one temporary variable — still `O(1)` space.

Now reversing a slice, given the two positions.

```python
def reverse_in_place(items: list[int], left: int, right: int) -> None:
    """Reverse items[left..right] inclusive. O(right - left) time, O(1) space."""
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1
```

Taking `left` and `right` as arguments rather than always reversing the whole list is what
makes it reusable three times. `right` is **inclusive**, so the caller passes `n - 1`, not `n`.
Pick one convention and write it in the docstring; mixing them up is a real source of
off-by-one bugs.

The version that uses extra space, so the comparison is honest.

```python
def rotate_extra_space(items: list[int], k: int) -> None:
    """Rotate right by k using a second list. O(n) time, O(n) extra space."""
    n = len(items)
    if n == 0:
        return
    k %= n
    items[:] = items[n - k:] + items[:n - k]
```

`items[:] = ...` writes through into the caller's list. `items = ...` would only rebind the
local name and the caller would see nothing change. Guarding `n == 0` first matters because
`k % 0` raises `ZeroDivisionError`.

The naive one, which is correct and too slow.

```python
def rotate_one_by_one(items: list[int], k: int) -> None:
    """Rotate right by k, one step at a time. O(n * k) time, O(1) space."""
    n = len(items)
    if n == 0:
        return
    k %= n
    for _ in range(k):
        items.insert(0, items.pop())
```

`pop()` from the end is `O(1)`; `insert(0, ...)` shifts everything and is `O(n)`. Say this out
loud in an interview before you are asked — knowing that your own first idea is too slow is
worth more than not having noticed.

And the one they want.

```python
def rotate_three_reversals(items: list[int], k: int) -> None:
    """Rotate right by k. O(n) time, O(1) extra space."""
    n = len(items)
    if n == 0:
        return
    k %= n
    reverse_in_place(items, 0, n - 1)
    reverse_in_place(items, 0, k - 1)
    reverse_in_place(items, k, n - 1)
```

Check the `k = 0` case by hand: `reverse_in_place(items, 0, -1)` has `left = 0` and
`right = -1`, so `left < right` is false and it does nothing. The first and third reversals
then undo each other. No special case needed, which is what a correct bound looks like.

The cyclic version, for completeness.

```python
def rotate_cyclic(items: list[int], k: int) -> None:
    """Move each element straight to its final place, carrying the one it displaces."""
    n = len(items)
    if n == 0:
        return
    k %= n
    if k == 0:
        return
    moved, start = 0, 0
    while moved < n:
        current, carried = start, items[start]
        while True:
            nxt = (current + k) % n
            items[nxt], carried = carried, items[nxt]
            current, moved = nxt, moved + 1
            if current == start:
                break
        start += 1
```

The outer `while moved < n` is the part people forget. With `n = 6, k = 2` the inner loop
visits only `0, 2, 4` and returns to the start, so the outer loop has to begin a second cycle
at position 1.

Here is the complete program.

```python
"""Day 13 — reverse, rotate and swap, all in place."""

import random
import time


def reverse_in_place(items: list[int], left: int, right: int) -> None:
    """Reverse items[left..right] inclusive. O(right - left) time, O(1) space."""
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


def rotate_extra_space(items: list[int], k: int) -> None:
    """Rotate right by k using a second list. O(n) time, O(n) extra space."""
    n = len(items)
    if n == 0:
        return
    k %= n
    items[:] = items[n - k:] + items[:n - k]   # items[:] mutates, items = rebinds


def rotate_one_by_one(items: list[int], k: int) -> None:
    """Rotate right by k, one step at a time. O(n * k) time, O(1) space."""
    n = len(items)
    if n == 0:
        return
    k %= n
    for _ in range(k):
        items.insert(0, items.pop())           # pop is O(1), insert(0) is O(n)


def rotate_three_reversals(items: list[int], k: int) -> None:
    """Rotate right by k. O(n) time, O(1) extra space. The answer."""
    n = len(items)
    if n == 0:
        return
    k %= n                                     # k = 10 on 7 items is the same as k = 3
    reverse_in_place(items, 0, n - 1)          # whole thing
    reverse_in_place(items, 0, k - 1)          # the k that are now at the front
    reverse_in_place(items, k, n - 1)          # the n - k that are now at the back


def rotate_cyclic(items: list[int], k: int) -> None:
    """Rotate right by k by moving each element straight to its final place."""
    n = len(items)
    if n == 0:
        return
    k %= n
    if k == 0:
        return
    moved = 0
    start = 0
    while moved < n:
        current = start
        carried = items[start]
        while True:
            nxt = (current + k) % n
            items[nxt], carried = carried, items[nxt]
            current = nxt
            moved += 1
            if current == start:
                break
        start += 1


def count_swaps(n: int, k: int) -> int:
    """How many two-element swaps the three-reversal version performs."""
    k %= n
    return (n // 2) + (k // 2) + ((n - k) // 2)


if __name__ == "__main__":
    print("reversing a slice in place")
    row = [10, 20, 30, 40, 50, 60, 70]
    print(f"  before          : {row}")
    reverse_in_place(row, 0, len(row) - 1)
    print(f"  whole reversed  : {row}")
    reverse_in_place(row, 2, 4)
    print(f"  middle reversed : {row}")

    print("\nthe three reversals, one at a time (k = 3, right)")
    row = [1, 2, 3, 4, 5, 6, 7]
    n, k = len(row), 3
    print(f"  start           : {row}")
    reverse_in_place(row, 0, n - 1)
    print(f"  reverse all     : {row}")
    reverse_in_place(row, 0, k - 1)
    print(f"  reverse first {k} : {row}")
    reverse_in_place(row, k, n - 1)
    print(f"  reverse last  {n - k} : {row}")

    print("\nfour ways to rotate, same answer")
    for name, fn in (("extra space", rotate_extra_space),
                     ("one by one", rotate_one_by_one),
                     ("three reversals", rotate_three_reversals),
                     ("cyclic", rotate_cyclic)):
        items = [1, 2, 3, 4, 5, 6, 7]
        fn(items, 3)
        print(f"  {name:<16}: {items}")

    print("\nthe edge cases")
    EDGE: list[tuple[str, list[int], int]] = [
        ("empty list",        [],                 3),
        ("single element",    [9],                3),
        ("k is zero",         [1, 2, 3, 4],       0),
        ("k equals n",        [1, 2, 3, 4],       4),
        ("k is bigger than n",[1, 2, 3, 4],      10),
        ("k is n minus one",  [1, 2, 3, 4],       3),
        ("all identical",     [7, 7, 7],          2),
    ]
    print(f"  {'case':<20}{'input':<16}{'k':>4}   result")
    for label, data, kk in EDGE:
        items = list(data)
        rotate_three_reversals(items, kk)
        print(f"  {label:<20}{str(data):<16}{kk:>4}   {items}")

    print("\ndo all four agree? 2000 random cases")
    random.seed(13)
    disagreements = 0
    for _ in range(2000):
        size = random.randint(0, 12)
        data = [random.randint(0, 9) for _ in range(size)]
        kk = random.randint(0, 30)
        answers = []
        for fn in (rotate_extra_space, rotate_one_by_one,
                   rotate_three_reversals, rotate_cyclic):
            items = list(data)
            fn(items, kk)
            answers.append(items)
        if any(a != answers[0] for a in answers):
            disagreements += 1
    print(f"  disagreements: {disagreements}")

    print("\nswaps performed by the three reversals (n = 1,000,000)")
    for kk in (1, 250_000, 500_000, 999_999):
        print(f"  k = {kk:>9,}  ->  {count_swaps(1_000_000, kk):>10,} swaps")

    print("\none-by-one vs three reversals (n = 20,000, k = 10,000)")
    base = list(range(20_000))
    a = list(base)
    t0 = time.perf_counter(); rotate_one_by_one(a, 10_000); slow = time.perf_counter() - t0
    b = list(base)
    t0 = time.perf_counter(); rotate_three_reversals(b, 10_000); fast = time.perf_counter() - t0
    print(f"  one by one       : {slow:>8.4f} s")
    print(f"  three reversals  : {fast:>8.4f} s   -> {slow / fast:>6.0f}x faster")
    print(f"  same answer?     : {a == b}")

    print("\nat a million elements, where one-by-one is not an option")
    big = list(range(1_000_000))
    t0 = time.perf_counter(); rotate_three_reversals(big, 333_333); r3 = time.perf_counter() - t0
    big2 = list(range(1_000_000))
    t0 = time.perf_counter(); rotate_extra_space(big2, 333_333); rs = time.perf_counter() - t0
    print(f"  three reversals  : {r3:>8.4f} s   O(1) extra space")
    print(f"  slice + rebuild  : {rs:>8.4f} s   O(n) extra space (~8 MB here)")
    print(f"  same answer?     : {big == big2}")
```

This is exactly what it printed:

```
reversing a slice in place
  before          : [10, 20, 30, 40, 50, 60, 70]
  whole reversed  : [70, 60, 50, 40, 30, 20, 10]
  middle reversed : [70, 60, 30, 40, 50, 20, 10]

the three reversals, one at a time (k = 3, right)
  start           : [1, 2, 3, 4, 5, 6, 7]
  reverse all     : [7, 6, 5, 4, 3, 2, 1]
  reverse first 3 : [5, 6, 7, 4, 3, 2, 1]
  reverse last  4 : [5, 6, 7, 1, 2, 3, 4]

four ways to rotate, same answer
  extra space     : [5, 6, 7, 1, 2, 3, 4]
  one by one      : [5, 6, 7, 1, 2, 3, 4]
  three reversals : [5, 6, 7, 1, 2, 3, 4]
  cyclic          : [5, 6, 7, 1, 2, 3, 4]

the edge cases
  case                input              k   result
  empty list          []                 3   []
  single element      [9]                3   [9]
  k is zero           [1, 2, 3, 4]       0   [1, 2, 3, 4]
  k equals n          [1, 2, 3, 4]       4   [1, 2, 3, 4]
  k is bigger than n  [1, 2, 3, 4]      10   [3, 4, 1, 2]
  k is n minus one    [1, 2, 3, 4]       3   [2, 3, 4, 1]
  all identical       [7, 7, 7]          2   [7, 7, 7]

do all four agree? 2000 random cases
  disagreements: 0

swaps performed by the three reversals (n = 1,000,000)
  k =         1  ->     999,999 swaps
  k =   250,000  ->   1,000,000 swaps
  k =   500,000  ->   1,000,000 swaps
  k =   999,999  ->     999,999 swaps

one-by-one vs three reversals (n = 20,000, k = 10,000)
  one by one       :   0.1496 s
  three reversals  :   0.0043 s   ->     35x faster
  same answer?     : True

at a million elements, where one-by-one is not an option
  three reversals  :   0.2036 s   O(1) extra space
  slice + rebuild  :   0.0468 s   O(n) extra space (~8 MB here)
  same answer?     : True
```

**Look at the edge-case table.** Every one of those falls out with no special case except the
empty check. `k = 0`, `k = n` and `k > n` are all handled by the single `k %= n` line.

**Look at the swap counts.** The total is essentially `n` regardless of `k`. That is the
sentence to say in the interview: *"about n swaps, whatever k is."*

**Look at the last block, and be honest about it.** The three-reversal version is the answer to
the question as asked, and the slice version is **four times faster in wall-clock time**,
because it is a handful of C-level memory copies while the reversal is a Python loop running a
million iterations. Same `O(n)`, very different constant. The reversal wins on the thing the
question actually constrained — memory — and loses on speed. Saying that out loud is a strong
move, because it shows you know what a complexity class does and does not promise.

---

## 6. What it costs

**Reversing a slice of length `m`.** The two markers start `m - 1` apart and move one step each
per iteration, so the loop runs `m // 2` times and does one swap each time.

```
m = 7  ->  3 swaps    (the middle element never moves)
m = 8  ->  4 swaps
```

`O(m)` time, `O(1)` space — three integers, whatever `m` is.

**The three reversals, counted.** Lengths `n`, then `k`, then `n - k`:

```
n // 2  +  k // 2  +  (n - k) // 2
```

With `n = 1,000,000` and `k = 250,000`:

```
500,000 + 125,000 + 375,000 = 1,000,000 swaps
```

So **about `n` swaps in total, for any `k`** — each element is moved twice, and each swap moves
two elements, so `2n / 2 = n`. `O(n)` time, `O(1)` extra space. That last part is the whole
point of the question.

**The one-at-a-time version.** Each `insert(0, x)` shifts every element one place right, which
is `n` moves, and you do it `k` times:

```
k x n moves
```

At `n = 1,000,000` and `k = 500,000`:

```
500,000 x 1,000,000 = 500,000,000,000 moves
```

Five hundred billion. At roughly 10⁸ operations per second that is about **an hour and a half**.
The measured version above, scaled down to `n = 20,000`, already took 35 times longer than the
reversals — and the gap grows with `n`, because one method is linear and the other is not.

**The extra-space version.** `O(n)` time and `O(n)` extra space. How much memory is that,
concretely? A Python list of a million small integers holds a million 8-byte references:

```
1,000,000 x 8 bytes = 8 MB for the new list
```

Eight megabytes is nothing on a laptop and is a real problem in a memory-constrained service
holding many such arrays, which is why the constraint exists in the first place. This is the
[day 007](../day-007-space-complexity/README.md) distinction: `O(1)` **extra** space, not
`O(1)` total — the input array itself still occupies `O(n)`, and nobody counts that.

**The cyclic version.** Exactly `n` writes and one carried variable, so `O(n)` time and `O(1)`
space, with a slightly smaller constant than the reversals. It is not worth the risk of getting
the cycle count wrong under time pressure.

**Summary, which is what you should be able to produce on demand:**

| Method | Time | Extra space | Would you write it? |
|---|---|---|---|
| Build a new array | `O(n)` | `O(n)` | Only if space is not constrained. Fastest in practice. |
| One element at a time | `O(n × k)` | `O(1)` | No. Correct and unusably slow. |
| **Three reversals** | **`O(n)`** | **`O(1)`** | **Yes. This is the answer.** |
| Cyclic replacement | `O(n)` | `O(1)` | Mention it. Do not lead with it. |

---

## 7. The traps

### Trap one: forgetting `k %= n`

The most common failure on this question, and it does not fail quietly.

```python
def reverse_in_place(items, left, right):
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


def rotate(items, k):
    n = len(items)
    reverse_in_place(items, 0, n - 1)
    reverse_in_place(items, 0, k - 1)      # k is not reduced
    reverse_in_place(items, k, n - 1)


items = [1, 2, 3, 4, 5]
rotate(items, 10)
print(items)
```

```
Traceback (most recent call last):
  File "t1.py", line 16, in <module>
    rotate(items, 10)
  File "t1.py", line 11, in rotate
    reverse_in_place(items, 0, k - 1)      # k is not reduced
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "t1.py", line 3, in reverse_in_place
    items[left], items[right] = items[right], items[left]
                                ~~~~~^^^^^^^
IndexError: list index out of range
```

`IndexError: list index out of range`, from asking for `items[9]` in a five-element list. The
fix is one line, `k %= n`, before anything else, and a guard for the empty array before that
because `k % 0` raises `ZeroDivisionError`.

**Say it before you are asked.** *"First line: k modulo n, because rotating by the length is a
no-op and the tests will send a k larger than the array."*

### Trap two: rebinding instead of mutating

This one produces no error at all. The function runs, returns, and changes nothing.

```python
def rotate(items, k):
    k %= len(items)
    items = items[-k:] + items[:-k]        # rebinds the local name
    return None


data = [1, 2, 3, 4, 5, 6, 7]
rotate(data, 3)
print(data)
```

```
[1, 2, 3, 4, 5, 6, 7]
```

Unchanged. `items` inside the function is a local name that starts out referring to the
caller's list. `items = ...` makes that local name refer to a brand new list and drops the
connection. The caller still has the old one.

The fix is one character:

```python
items[:] = items[-k:] + items[:-k]         # writes through into the caller's list
```

`items[:] = ...` is **slice assignment**: it replaces the contents of the existing list object
rather than creating a new one. Any in-place function — this, `reverse`, the compaction loops
on [day 015](../day-015-the-write-pointer/README.md) — has to mutate, and `=` on the bare name
never does.

**How to catch it every time:** if a function's job is to modify its argument and its body
contains `argument_name = `, it is wrong.

### Trap three: reversing all the way to the end

The near-miss that looks correct, produces no error, and gives you back exactly what you
started with.

```python
def reverse(items):
    n = len(items)
    for i in range(n):                      # should be range(n // 2)
        items[i], items[n - 1 - i] = items[n - 1 - i], items[i]


data = [1, 2, 3, 4, 5, 6]
reverse(data)
print(data)
```

```
[1, 2, 3, 4, 5, 6]
```

The loop reverses the array in its first half and then reverses it back in its second half.
Every pair is swapped twice. With an odd-length array the middle element is swapped with itself
and the result is still the original.

This is worse than a crash, because it looks like the function was never called. **The bound is
`n // 2`, and the reason is that each swap fixes two positions at once.** The
`while left < right` form makes the bug impossible, which is why it is the form worth writing.

### The direction trap

"Rotate left by 3" and "rotate right by 3" are different answers, and half of candidates give
the wrong one under pressure. There is no error message; the tests simply fail.

```
[1, 2, 3, 4, 5, 6, 7]  right by 3  ->  [5, 6, 7, 1, 2, 3, 4]
[1, 2, 3, 4, 5, 6, 7]  left  by 3  ->  [4, 5, 6, 7, 1, 2, 3]
```

Two defences. Read the direction out of the statement and repeat it back before writing. And
remember the conversion — **left by `k` is right by `n - k`** — so you only ever need one
implementation.

---

## 8. In the interview

### How it gets asked

- *"Rotate the array to the right by k. Can you do it in O(1) extra space?"* — LeetCode 189,
  and the second sentence is the whole question.
- *"Reverse the array in place."* — the warm-up, often the first thirty seconds of a phone
  screen.
- *"Reverse the words in a sentence, but keep the words themselves the right way round."* — the
  same three-reversal idea wearing a hat. Reverse everything, then reverse each word.
- *"Why does reversing three times give you a rotation?"* — the follow-up that decides the
  question.

### What to say out loud, in the first ninety seconds

1. **Repeat the direction and the constraint.** *"Right by k, in place, constant extra space.
   And k could be larger than the array, so the first thing I do is k modulo n."*
2. **Name the naive options and reject them, briefly.** *"I could build a new array with a
   slice — that's O(n) time but O(n) space, which the constraint rules out. I could rotate one
   step at a time k times, but each of those shifts everything, so it's O(n × k)."*
3. **State the trick before writing it.** *"The in-place answer is three reversals. Reverse the
   whole array, then reverse the first k, then reverse the rest."*
4. **Explain why, in one sentence.** *"Reversing the whole array puts the last k elements at the
   front where they belong, but back to front within themselves. Reversing each group again
   undoes exactly that, and doesn't move anything across the boundary."*
5. **Write it, and read the edge cases off the code.** *"Empty list returns early. k = 0 makes
   the second reversal a no-op, with left = 0 and right = −1, and the first and third undo each
   other, so it's correct with no special case."*
6. **Give both costs.** *"About n swaps in total, whatever k is — n over 2, plus k over 2, plus
   n − k over 2. So O(n) time and O(1) extra space: three integer variables regardless of size."*

If you have time, add step 7: *"There's also a cyclic-replacement version that does n writes
instead of n swaps, but showing it visits everything needs a gcd argument, so under time
pressure I'd write the reversals."*

### The follow-ups

**"Why does the three-reversal trick work?"**
Two reasons said together. First, reversing the whole array is what gets the last `k` elements
to the front and the first `n − k` to the back — that is the movement between the two groups,
and it happens in one step. Second, a full reversal also flips the order inside each group, so
`[5,6,7]` arrives as `[7,6,5]`. Reversing each group on its own puts that back. Another way to
say it: every element is reversed exactly twice, once as part of the whole and once as part of
its group, and two reversals cancel — so within a group nothing changed, while the groups
themselves swapped sides.

**"What if k is bigger than the array? What if k is negative?"**
`k %= n` handles both. Rotating by `n` returns the array to its starting position, so only the
remainder matters, and `10 % 7 = 3`. For negative `k`, Python's `%` already returns a
non-negative result — `-3 % 7` is `4`, which is exactly "rotate right by 4", which is "rotate
left by 3". That is the correct answer, though I would confirm the intended meaning rather than
rely on it, and in Java or C the same expression gives `-3` and I would have to normalise it
myself. I would also guard `n == 0` before the modulo, because `k % 0` raises
`ZeroDivisionError`.

**"Rotate left instead."**
Same function, different `k`: rotating left by `k` is rotating right by `n − k`. Or, written
directly, the three reversals happen in a different order — reverse the first `k`, reverse the
rest, then reverse the whole thing. I would write one implementation and convert, because two
near-identical functions is two chances to get the direction wrong.

**"Can you do it in one pass instead of three?"**
Yes — cyclic replacement. Start at position 0, move that element to `(0 + k) % n`, carry the
element it displaced, and keep going until you return to where you started. Each element is
written exactly once, so it is `n` writes against roughly `n` swaps, a slightly better constant.
The catch is that the chain of hops does not always cover the array: with `n = 6` and `k = 2`
you visit only `0, 2, 4` before looping back, and the number of separate cycles is `gcd(n, k)`.
So it needs an outer loop and a counter, and it is much easier to get subtly wrong. Same
complexity, more risk — I would write the reversals.

**"What if it were a linked list rather than an array?"**
A different problem, because there is no random access and nothing to swap by position. For a
singly linked list you walk to the end, join it into a ring, walk `n − k` steps from the head,
and break the ring there. That is `O(n)` time and `O(1)` space too, but it is link surgery
rather than position arithmetic, and it is
[day 081](../day-081-reversing-a-list/README.md).

### A model answer

> "Right by k, in place, O(1) extra space. Before I write anything: k could be bigger than the
> array, and rotating by exactly the length gets you back where you started, so the first line
> is `k %= n`. And I need to guard the empty array before that, because `k % 0` raises.
>
> The version I'm not allowed to use is the one-liner — take the last k, put the first n − k
> after it — because that builds a second array and costs O(n) space. The other naive one is
> rotating a single step k times, but each step shifts every element, so that's O(n × k). At a
> million elements with k a half-million that's 5 × 10¹¹ moves.
>
> The in-place answer is three reversals:
>
> ```python
> def rotate(items: list[int], k: int) -> None:
>     n = len(items)
>     if n == 0:
>         return
>     k %= n
>     reverse(items, 0, n - 1)
>     reverse(items, 0, k - 1)
>     reverse(items, k, n - 1)
> ```
>
> where `reverse` is the standard two-pointer loop — one marker at each end, swap, walk them
> inwards while `left < right`.
>
> Why it works: reversing the whole array is the step that actually moves elements between the
> two groups — the last k end up at the front, the first n − k end up at the back. But a full
> reversal also flips the order *inside* each group, so the last three arrive as 7, 6, 5
> instead of 5, 6, 7. Reversing each group separately undoes exactly that and doesn't move
> anything across the boundary. Equivalently, each element gets reversed twice — once in the
> whole, once in its group — and two reversals cancel.
>
> Edge cases fall out. Empty returns early. k = 0 makes the middle call `reverse(items, 0, -1)`,
> where `left < right` is immediately false, and the first and third reversals undo each other.
> k = n is the same case after the modulo.
>
> Cost: n over 2 swaps for the whole, plus k over 2, plus n − k over 2 — about n swaps in
> total, for any k. So O(n) time, O(1) extra space; three integers regardless of how big the
> array is.
>
> One honest note — if the space constraint weren't there, the slice version is the same O(n)
> but several times faster in wall-clock, because it's C-level memory copying rather than a
> million-iteration Python loop. Same complexity class, very different constant."

That answer states the constraint back, rejects the two naive options with numbers, gives the
trick, **explains why it works**, checks the edges from the code, gives both costs, and ends
with a remark that shows the candidate knows what big-O does not tell you.

---

## 9. Recall card

1. **Rotate right by k = three reversals.** Reverse the whole thing, reverse the first `k`,
   reverse the last `n − k`. `O(n)` time, `O(1)` extra space.
2. **`k %= n` is the first line, after guarding the empty array.** Rotating by the length is a
   no-op; without the modulo a large `k` gives `IndexError: list index out of range`.
3. **Why it works:** the full reversal moves the two groups to the right sides but flips them
   internally; reversing each group undoes exactly that. Every element is reversed twice.
4. **Reverse in place is `left < right`, swap, step both inwards** — `n // 2` swaps, because
   each swap fixes two positions. Looping to `n` reverses it back to the original.
5. **In place means mutate.** `items[:] = ...` writes through to the caller; `items = ...` only
   rebinds a local name and silently changes nothing.
