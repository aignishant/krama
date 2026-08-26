---
day: 7
track: dsa
title: "Space complexity, and what in-place really means"
phase: "Foundations: how code costs"
status: written
---

# Day 007 · DSA — Space complexity, and what in-place really means

**After today you can:** You can state the extra memory your solution uses and rewrite it to use less.

**The interviewer asks it as:** *Can you do that in O(1) extra space?*

---

## 1. What this is, and why they ask it

**Space complexity** is the same idea as time complexity, applied to memory: how much extra
storage your solution needs as the input grows. **Extra space** — also called **auxiliary
space** — means everything you allocate, not counting the input you were handed.

A solution uses **O(1) extra space** when the amount it allocates does not depend on the
input size. Ten items or ten million, it keeps the same handful of variables. That is what
**in-place** means, and it is the phrase interviewers use when they want you to stop
allocating.

They ask because "can you do it in O(1) extra space?" is the cleanest second question in
existence. Your first solution works and you have stated its time complexity. Now the
interviewer applies one more constraint, and it separates two things: whether you know what
your own code allocates, and whether you can restructure a solution rather than rewrite it.
A candidate who says "sure — I'd swap in place with two indices instead of building a new
array" has answered in one sentence. A candidate who says "it's O(n) time" has answered a
different question.

---

## 2. The story

Farida has one narrow cupboard in her kitchen, and every steel vessel she owns lives in it.
Two shelves, and on the lower one, twenty-two vessels standing in a row.

They have been in no order for years. On Sunday morning she decides she has had enough of
reaching past the big handi for the small tumbler, and she is going to put them in order of
size, smallest on the left.

Her usual way of doing a job like this is to take everything out first. She would put all
twenty-two on the counter, look at them all together, and put them back one at a time in the
right order. It is easy. She has done it before, and it takes about fifteen minutes.

But this is a Sunday in September, and her sister-in-law is in the kitchen making biryani for
eleven people. Every inch of counter is taken. There are three vessels of half-cut onions, a
tray of marinated chicken, the big pot, two mixing bowls and a plate she is not allowed to
move. There is no counter. There is not going to be a counter until three in the afternoon.

So she has to do the whole thing inside the cupboard.

It turns out to be possible, and the way it works is this. There is one gap at the right-hand
end of the shelf, about the width of one vessel — a space that has always been there because
twenty-two vessels do not quite fill twenty-three vessels' worth of shelf. That gap is the
only free space she has.

To swap two vessels she moves the first one into the gap, slides the second into the space
the first left, and puts the one from the gap into the second's old place. Three moves, and
the gap ends up back where it started. It is slower than the counter method — she does a
great deal more lifting — but at no point does she need anywhere to put anything except that
one gap.

She finishes at half past eleven. It took her thirty-five minutes rather than fifteen, and
the shelf is in order.

What stays with her, drinking tea afterwards, is that the job was never impossible. It was
only impossible *the way she usually did it*. The counter was not part of the job. It was a
habit she had never noticed she had.

---

## 3. The idea in plain English

Farida's cupboard is space complexity, and the gap at the end of the shelf is `O(1)` extra
space.

### Two kinds of space, and only one of them is being asked about

**Input space** is the memory the input already occupies. Farida's twenty-two vessels. You
did not allocate it, you were handed it, and you cannot avoid it.

**Extra space**, or **auxiliary space**, is everything your solution allocates on top of
that. Farida's counter. **When an interviewer asks about space complexity, this is what they
mean**, unless they specifically say "total space".

So the answer to "what's the space complexity?" for a function that walks an array keeping
a running total is **O(1)**, not O(n). The array was already there.

Say which one you mean. "O(1) extra space — I'm not counting the input array" is precise and
takes two extra seconds.

### O(1) extra space means a fixed number of variables

```python
def total(items: list[int]) -> int:
    running = 0                 # one integer
    for x in items:             # one loop variable
        running += x
    return running
```

Two variables. That does not change when `items` gets longer. **O(1) extra space.**

Now the version that is not:

```python
def doubled(items: list[int]) -> list[int]:
    out = []                    # this grows with the input
    for x in items:
        out.append(x * 2)
    return out
```

`out` ends up as long as `items`. **O(n) extra space.**

### The gap: why a swap needs exactly one spare place

Farida could not exchange two vessels without somewhere to put one of them for a moment.
Neither can a computer. Swapping `a` and `b` needs a temporary:

```python
temp = items[i]
items[i] = items[j]
items[j] = temp
```

Three moves, one temporary variable. Python lets you write it on one line —
`items[i], items[j] = items[j], items[i]` — and it does the same thing underneath. The
important point is that **one** temporary is enough, and one temporary is `O(1)` however
long the array is.

That single fact is why almost every in-place algorithm you will meet is built out of swaps.

### In-place means you modify what you were given

An **in-place** operation changes the input itself rather than producing a new thing.
`items.sort()` is in place. `sorted(items)` is not — it returns a new list and leaves the
original alone.

| In place (modifies) | Not in place (returns new) |
|---|---|
| `items.sort()` | `sorted(items)` |
| `items.reverse()` | `items[::-1]` |
| `items.append(x)` | `items + [x]` |
| `items[i] = v` | `items[:i] + [v] + items[i+1:]` |

The right-hand column all cost `O(n)` extra space. The left-hand column costs `O(1)`.

There is one important caveat, and interviewers like it: **`items.sort()` is in place but not
`O(1)` space.** Python's Timsort needs a temporary area of up to `n/2`, so it is `O(n)`
auxiliary. If somebody insists on strictly `O(1)` extra space, sorting is off the table, and
heapsort is the standard `O(n log n)` answer with genuinely constant extra space.

### The space you did not know you were allocating

Three sources of hidden memory, all of which come up.

**Slicing.** `items[1:]` copies. From
[day 005](../day-005-python-lists-and-tuples/README.md): a slice is a new list, so a
function that slices is not `O(1)` space no matter how it looks.

**Recursion.** Every pending function call occupies a frame in memory until it returns. A
recursion that goes `n` deep uses **`O(n)` space** even if it allocates nothing itself. This
is the one people miss most often, and it is why "recursive binary search is O(1) space" is
wrong — it is `O(log n)` space, because of the frames.
[Day 088](../day-088-the-call-stack/README.md) covers this properly.

**Sets and dictionaries you built to be fast.** Yesterday's duplicate-detection answer spends
`O(n)` space deliberately. That is the right call and it is still `O(n)`.

### Does the output count?

By convention, **no** — the space required to hold the answer is not counted as extra space,
because you have no choice about it. If a problem asks you to return a new array of n
elements, that array is not held against you.

But anything *beyond* the output does count. Building a dictionary in order to produce a
list is `O(n)` extra even though the list itself is free. Say it explicitly: "O(n) for the
output, plus O(n) for the hash map I used along the way" is unambiguous, and unambiguous is
what you want.

---

## 4. The picture

Reversing an array with the counter, and then inside the cupboard:

```
  NOT IN PLACE — O(n) extra space

  input   +----+----+----+----+----+----+
          |  3 |  8 |  1 |  9 |  4 |  7 |     the vessels
          +----+----+----+----+----+----+
                     |  copy each one
                     v
  new     +----+----+----+----+----+----+
          |  7 |  4 |  9 |  1 |  8 |  3 |     the counter: a whole second shelf
          +----+----+----+----+----+----+


  IN PLACE — O(1) extra space

          +----+----+----+----+----+----+
          |  3 |  8 |  1 |  9 |  4 |  7 |     one temp variable: []
          +----+----+----+----+----+----+
            ^                        ^
           left                    right      swap them, move both inward

          +----+----+----+----+----+----+
          |  7 |  8 |  1 |  9 |  4 |  3 |
          +----+----+----+----+----+----+
                 ^                ^
                left            right         swap, move inward

          +----+----+----+----+----+----+
          |  7 |  4 |  1 |  9 |  8 |  3 |
          +----+----+----+----+----+----+
                      ^     ^
                     left right                swap, and they cross — done

          +----+----+----+----+----+----+
          |  7 |  4 |  9 |  1 |  8 |  3 |     same answer, no second shelf
          +----+----+----+----+----+----+
```

**What to notice:** both pictures end with the same values. The top one needed a second array
of six slots; the bottom one needed one temporary variable and two indices, and would need
exactly the same for six million.

Now the hidden space in recursion, which is the one people forget:

```
  countdown(4)

  memory (the call stack)          what is waiting
  +---------------------------+
  | countdown(0)  <- running  |    nothing pending
  +---------------------------+
  | countdown(1)              |    waiting to add 1
  +---------------------------+
  | countdown(2)              |    waiting to add 1
  +---------------------------+
  | countdown(3)              |    waiting to add 1
  +---------------------------+
  | countdown(4)              |    waiting to add 1
  +---------------------------+

  5 frames alive at once, for n = 4.  n frames for n.  O(n) space,
  even though not one line of that function allocates anything.
```

**What to notice:** the function body has no list, no set, no slice. The memory is spent by
the calls themselves. Every recursive solution owes an answer to "how deep does it go?".

---

## 5. The code, built step by step

Build the same job three ways and measure the memory, because arguing about space without
measuring it is how people convince themselves they are in place when they are not.

Python has a memory tracker in the standard library:

```python
import tracemalloc

def peak_kb(fn) -> float:
    tracemalloc.start()
    fn()
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024
```

`tracemalloc.get_traced_memory()` returns the current and the **peak** allocation since
tracking started. Peak is the number that matters: it is the high-water mark, and it is what
a memory limit actually tests against.

Now three reversals. First, the one that builds a new list.

```python
def reverse_new(items: list[int]) -> list[int]:
    out = []
    for i in range(len(items) - 1, -1, -1):
        out.append(items[i])
    return out
```

`range(len(items) - 1, -1, -1)` counts down: start at the last index, stop before −1, step by
−1. `out` grows to length n, so this is **O(n) extra space**.

Second, the one-liner, which is the same cost wearing better clothes.

```python
def reverse_slice(items: list[int]) -> list[int]:
    return items[::-1]
```

`[::-1]` is a slice with a step of −1. It is a slice, so it copies. **O(n) extra space**, and
it is worth knowing that the tidiest-looking solution here is not the cheapest one.

Third, in the cupboard.

```python
def reverse_in_place(items: list[int]) -> None:
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1
```

Two indices and the temporary that the swap uses internally. **O(1) extra space.** Note the
return type is `None`: it changes the caller's list and returns nothing, which is the Python
convention for in-place operations and is exactly what `list.sort()` does.

Now the same three-way comparison for a harder job — removing duplicates from a sorted array.

```python
def dedupe_new(items: list[int]) -> list[int]:
    out = []
    for x in items:
        if not out or out[-1] != x:
            out.append(x)
    return out
```

`out[-1]` is the last element. This is clear and it allocates a full second array.

```python
def dedupe_in_place(items: list[int]) -> int:
    """Compact in place. Returns the new length; items[:length] is the answer."""
    if not items:
        return 0
    write = 1                              # where the next kept value goes
    for read in range(1, len(items)):
        if items[read] != items[write - 1]:
            items[write] = items[read]
            write += 1
    return write
```

This is the **write pointer**, and it is the single most reusable in-place pattern there is.
One index reads forward through everything; another marks where the next keeper belongs.
Because `write` never overtakes `read`, you are always writing into a slot you have already
passed. `O(1)` extra space, and it is the whole subject of
[day 015](../day-015-the-write-pointer/README.md).

Here is the complete program.

```python
"""Day 7 — measure what your solution actually allocates."""

import sys
import tracemalloc


def peak_kb(fn) -> float:
    """Peak extra memory allocated while fn runs, in kilobytes."""
    tracemalloc.start()
    fn()
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024


# ---- reversing -----------------------------------------------------------

def reverse_new(items: list[int]) -> list[int]:
    """O(n) extra: builds a second list."""
    out: list[int] = []
    for i in range(len(items) - 1, -1, -1):
        out.append(items[i])
    return out


def reverse_slice(items: list[int]) -> list[int]:
    """O(n) extra: a slice is a copy, however short the line is."""
    return items[::-1]


def reverse_in_place(items: list[int]) -> None:
    """O(1) extra: two indices and one swap temporary."""
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


# ---- removing duplicates from a sorted array -----------------------------

def dedupe_new(items: list[int]) -> list[int]:
    """O(n) extra."""
    out: list[int] = []
    for x in items:
        if not out or out[-1] != x:
            out.append(x)
    return out


def dedupe_in_place(items: list[int]) -> int:
    """O(1) extra. Returns the new length; items[:length] holds the answer."""
    if not items:
        return 0
    write = 1
    for read in range(1, len(items)):
        if items[read] != items[write - 1]:
            items[write] = items[read]
            write += 1
    return write


# ---- the hidden space in recursion ---------------------------------------

def depth_of(n: int) -> int:
    """O(n) space in call frames, even though it allocates nothing itself."""
    if n == 0:
        return 0
    return 1 + depth_of(n - 1)


if __name__ == "__main__":
    N = 200_000
    data = list(range(N))
    sorted_with_dupes = sorted([i // 3 for i in range(N)])

    # The fresh copy is made BEFORE tracing starts. Otherwise the copy itself
    # shows up as the function's allocation and every row looks like O(n).
    print(f"reversing {N:,} integers")
    for label, fn in (("build a new list   O(n)", reverse_new),
                      ("slice [::-1]       O(n)", reverse_slice),
                      ("two pointers       O(1)", reverse_in_place)):
        work = list(data)
        print(f"  {label} : {peak_kb(lambda: fn(work)):>9,.0f} KB")

    print(f"\nremoving duplicates from {N:,} sorted integers")
    for label, fn in (("build a new list   O(n)", dedupe_new),
                      ("write pointer      O(1)", dedupe_in_place)):
        work = list(sorted_with_dupes)
        print(f"  {label} : {peak_kb(lambda: fn(work)):>9,.0f} KB")

    print("\nchecking the in-place versions are correct")
    small = [3, 8, 1, 9, 4, 7]
    reverse_in_place(small)
    print(f"  reversed in place        : {small}")
    dupes = [1, 1, 2, 2, 2, 3, 4, 4]
    length = dedupe_in_place(dupes)
    print(f"  deduped in place         : length {length}, values {dupes[:length]}")

    print("\nhow deep can recursion go before Python stops it?")
    print(f"  the limit                : {sys.getrecursionlimit():,} frames")
    print(f"  depth_of(900)            : {depth_of(900)}")
```

This is exactly what it printed:

```
reversing 200,000 integers
  build a new list   O(n) :     1,586 KB
  slice [::-1]       O(n) :     1,562 KB
  two pointers       O(1) :         0 KB

removing duplicates from 200,000 sorted integers
  build a new list   O(n) :       549 KB
  write pointer      O(1) :         0 KB

checking the in-place versions are correct
  reversed in place        : [7, 4, 9, 1, 8, 3]
  deduped in place         : length 4, values [1, 2, 3, 4]

how deep can recursion go before Python stops it?
  the limit                : 1,000 frames
  depth_of(900)            : 900
```

**Look at the zeros.** They are not rounding. The in-place versions allocate nothing that
grows with the input — two integers, and those live on the stack rather than in tracked
allocations. Now change `N` to 400,000 and run it again: the `O(n)` rows double and the zeros
stay zero. That is the doubling test from
[day 003](../day-003-big-o-in-plain-english/README.md), applied to memory.

---

## 6. What it costs

**The space table for the operations you use most.**

| Operation | Extra space |
|---|---|
| `items[i], items[j] = items[j], items[i]` | `O(1)` |
| `items.reverse()`, `items.append()`, `items.pop()` | `O(1)` |
| `items[::-1]`, `items[a:b]`, `items.copy()` | `O(k)` — a copy |
| `sorted(items)` | `O(n)` — a new list |
| `items.sort()` | `O(n)` — in place, but Timsort needs a buffer |
| Heapsort | `O(1)` — the genuinely constant-space `O(n log n)` sort |
| `set(items)`, `Counter(items)` | `O(n)` |
| Recursion `n` deep | `O(n)` in call frames |
| Recursion `log n` deep (binary search) | `O(log n)` |
| Merge sort | `O(n)` |
| Quicksort | `O(log n)` — for the recursion, if you recurse on the smaller side |

**What memory actually costs, in bytes.** Python objects are not small:

```
a Python int object            28 bytes
a reference in a list           8 bytes
so one integer in a list       36 bytes
a small tuple (2 ints)         56 bytes + the ints
one entry in a set             ~60 bytes with the table overhead
one entry in a dict            ~100 bytes with the table overhead
```

Now the number that decides submissions. A typical memory limit is 256 MB:

```
256 MB / 36 bytes per int in a list = about 7,000,000 integers
256 MB / 100 bytes per dict entry   = about 2,700,000 dictionary entries
```

So at `n = 10⁶` a list of integers is comfortable, a dictionary keyed by every element is
comfortable, and an `n × n` grid is not:

```
1,000,000 x 1,000,000 = 10^12 cells. Not close. Not even for booleans.
```

An `O(n²)` space solution dies at about `n = 2,500`, well before an `O(n²)` **time** solution
dies at about 5,000. **Space is usually the tighter constraint, and people check it second.**

**The recursion arithmetic.** Each Python call frame is roughly 500 bytes:

```
1,000 frames (the default limit) x 500 bytes  =  500 KB    fine
100,000 frames                                =   50 MB    would be fine, if allowed
```

Python's limit is about 1,000, and it exists to turn runaway recursion into an error rather
than a crash. You can raise it with `sys.setrecursionlimit(200000)`, and you usually should
not: the real C stack underneath has its own limit, and exceeding that gives you a hard
segmentation fault instead of a clean exception. **Rewrite deep recursion as a loop.**

**The trade, stated as arithmetic.** Two Sum with a hash map, at `n = 10⁶`:

```
time  : 10^6 steps            instead of 10^12       a million times faster
space : 10^6 x 100 bytes      = 100 MB extra          from ~0
```

That is the shape of nearly every interesting decision in this course: **spend `O(n)` memory
to remove a factor of `n` from the time.** When the interviewer asks for `O(1)` space, they
are asking you to give that trade back and find another route — usually sorting first, or
two pointers, or using the input array itself as storage.

---

## 7. The traps

### Trap one: the "in-place" function that changes nothing

This is the one that produces a silent wrong answer and looks completely correct.

```python
def reverse_in_place(items: list[int]) -> None:
    items = items[::-1]          # looks like it reverses the caller's list


nums = [1, 2, 3, 4]
reverse_in_place(nums)
print(nums)
```

```
[1, 2, 3, 4]
```

Nothing happened. The function ran, no error was raised, and the list is untouched.

The reason is that `items = ...` **rebinds the local name** `items` to a brand-new list. The
caller's list is not involved. Assignment to a name never affects the caller; only mutation
of the object does.

These two lines look almost identical and behave completely differently:

```python
items = items[::-1]      # rebinds a local name. Caller sees nothing.
items[:] = items[::-1]   # writes INTO the caller's list. Caller sees it.
```

`items[:] = ...` is slice assignment, and it does modify in place — though note it still
builds the reversed copy first, so it is `O(n)` extra space, not `O(1)`. The genuinely
constant-space version is the two-pointer swap loop.

**How to catch it every time:** an in-place function returns `None` and its body contains
`items[i] = ...`, `items[:] = ...`, or a method like `.sort()` or `.append()`. If the only
assignment is to the bare parameter name, it is not in place.

### Trap two: the space you allocate without an allocation

Here is a solution to "find all pairs that sum to a target". The time complexity is fine. The
memory is not.

```python
def all_pairs(items: list[int], target: int) -> list[tuple[int, int]]:
    pairs = [(a, b) for a in items for b in items if a + b == target]
    return pairs
```

The list comprehension is neat, and it evaluates `a + b == target` for every ordered pair
before filtering. At `n = 50,000`:

```
Traceback (most recent call last):
  File "d7.py", line 6, in <module>
    print(len(all_pairs(list(range(50000)), 99999)))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d7.py", line 2, in all_pairs
    pairs = [(a, b) for a in items for b in items if a + b == target]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
MemoryError
```

`MemoryError` is Python telling you it asked the operating system for memory and was refused.
There is no line number inside a loop to blame, because the loop is the problem: 2.5 billion
comparisons producing 50,000 tuples at 56 bytes each was never the issue — it was that the
answer here really can be `O(n²)` tuples for other inputs, and the interpreter died trying.

The fix is a hash map, one pass, and yielding results instead of accumulating them:

```python
def all_pairs(items: list[int], target: int) -> list[tuple[int, int]]:
    seen: set[int] = set()
    out: list[tuple[int, int]] = []
    for x in items:
        if target - x in seen:
            out.append((target - x, x))
        seen.add(x)
    return out
```

`O(n)` time and `O(n)` space, and it produces each pair once instead of twice.

**How to catch it every time:** before writing a comprehension with two `for` clauses in it,
say the size out loud. Two `for` clauses over the same list is `n²` items considered, and if
you are storing them rather than filtering to a few, it is `n²` in memory as well.

---

## 8. In the interview

### How it gets asked

- *"Can you do that in O(1) extra space?"* — the standard second question, after your
  solution works.
- *"What's the space complexity?"* — the second half of "what's the time complexity?".
  Answer both without being asked twice.
- *"Does the output count towards the space?"* — a precision check.
- *"Your solution is recursive. What does that cost in memory?"* — the one people miss.

### What to say out loud, in the first ninety seconds

1. **Separate the two kinds.** *"Extra space is O(1) — I'm not counting the input array,
   which is O(n) and was given to me."*
2. **List what you allocated.** *"I keep two indices and a temporary for the swap. That's
   it, and it doesn't grow with n."*
3. **If you allocated something that grows, say so plainly.** *"The hash set is O(n) extra,
   in the worst case where everything is distinct."*
4. **If it is recursive, count the depth.** *"It recurses to depth log n, so that's O(log n)
   in call frames even though the body allocates nothing."*
5. **Name the trade.** *"I'm spending O(n) memory to get the time from O(n²) to O(n). If
   memory were the tighter constraint I'd sort first and use two pointers — O(n log n) time,
   O(1) extra space."*
6. **Offer the conversion.** *"Want me to do the constant-space version?"*

Step 5 is what makes you sound like an engineer rather than a candidate. You are not
defending a solution; you are describing a position on a curve.

### The follow-ups

**"Does the space taken by the input count?"**
By convention, no — space complexity means auxiliary space, the memory you allocate on top
of the input. The same goes for the output: if the problem asks for an array of n results,
that array is not held against you. What does count is anything beyond those two. So if I
build a dictionary in order to produce the output list, I'd state it as "O(n) for the output,
plus O(n) for the map I used along the way". I'd always say which convention I'm using rather
than assume we agree.

**"Your solution is recursive. What does that cost in memory?"**
Every pending call keeps a frame alive until it returns, so the space is the maximum depth of
the recursion. Binary search recursively is O(log n) space, not O(1). A recursion that walks
an array one element at a time is O(n) space, and in Python it hits `RecursionError` at about
a thousand frames. That is a real limit rather than a theoretical one, so for an input of a
hundred thousand I'd convert it to an explicit loop, or to a loop with my own stack — which
is O(n) heap instead of O(n) frames, but at least it does not crash.

**"Is `items.sort()` O(1) space?"**
No, and it is a nice question because the obvious answer is wrong. It sorts in place, so it
does not return a new list, but Timsort needs a temporary buffer of up to n/2 for merging.
So it is O(n) auxiliary. If someone genuinely requires O(1) extra space with O(n log n) time,
heapsort is the answer — it sorts in place with constant extra space, at the cost of being
slower in practice and not stable.

**"How would you turn this O(n) space solution into O(1)?"**
There are about four moves, and I'd look for them in this order. Sort the input first, if
sorting is allowed, and then use two pointers or adjacent comparison. Use the input array
itself as storage — for problems where values are in the range 1 to n, you can mark presence
by negating a value or by swapping elements into position. Replace the recursion with a
loop. Or reformulate the state entirely, like Boyer-Moore for majority element, which
replaces a whole count map with one candidate and one counter.

### A model answer

The candidate has solved "reverse the words in a string" by building a list and joining, and
is asked to do it in constant extra space.

> "Right now I'm O(n) extra: I split into a list of words, reverse the list, and join. The
> list and the joined result are both proportional to the input.
>
> To get to O(1) extra space I'd need to modify the input in place, which in Python means
> the input has to be a list of characters rather than a string, since strings are immutable.
> Given that, there's a standard two-step trick.
>
> First, reverse the entire array in place with two pointers — left at 0, right at the end,
> swap and move both inward until they cross. That's one temporary variable for the swap, so
> O(1) space, and n/2 swaps, so O(n) time.
>
> After that the words are in the right order but each word is backwards. So second, walk
> through and reverse each word individually, in place, using the same two-pointer swap
> between the word's boundaries. Also O(1) space, also O(n) time.
>
> Two passes, O(n) time, O(1) extra space, and the total is two indices and one temporary
> regardless of how long the input is.
>
> The thing I'd flag is that this only works because the input is mutable. If the signature
> gives me a Python string, O(1) extra space is not achievable at all — I have to build a
> new string, and that's O(n) by definition. So I'd check whether the problem intends a
> character array. In an interview I'd rather ask that than silently solve a different
> problem."

That answer converts the solution, states both complexities at each step, and ends by naming
the precondition that makes the whole thing possible. That last paragraph is the difference
between reciting a trick and understanding it.

---

## 9. Recall card

1. **Space complexity means extra space.** The input does not count; the output usually does
   not either. Say which convention you are using.
2. **O(1) extra space = a fixed number of variables**, whatever `n` is. That is what
   **in-place** means, and it is built out of swaps.
3. **Slicing, `sorted()`, sets and dicts all allocate `O(n)`.** `items.sort()` is in place and
   still `O(n)` auxiliary; heapsort is the `O(1)`-space sort.
4. **Recursion costs `O(depth)` in call frames** even when the body allocates nothing.
   Python stops at about 1,000.
5. **`items = items[::-1]` inside a function changes nothing for the caller.** Rebinding a
   name is not mutation. Use `items[i] = ...` or `items[:] = ...`.
