---
day: 5
track: dsa
title: "Python for DSA I: lists, tuples, and slicing"
phase: "Foundations: how code costs"
status: written
---

# Day 005 · DSA — Python for DSA I: lists, tuples, and slicing

**After today you can:** You know the real cost of append, pop, insert and a slice, so you stop writing accidental O(n^2).

**The interviewer asks it as:** *What is the complexity of inserting at the front of a Python list?*

---

## 1. What this is, and why they ask it

A Python **list** is not a linked chain of items. It is one solid run of slots in memory,
with the items sitting side by side in order. That single fact decides the cost of every
operation you can perform on it.

Adding to the end is nearly free. Adding to the front is not, because everything already
there has to shuffle along to make room. Taking a slice does not point at part of the list —
it builds a whole new one.

Interviewers ask because this is where good candidates lose otherwise-correct solutions.
You write a clean `O(n)` loop, put a `list.pop(0)` inside it, and you have silently written
`O(n²)`. Nothing looks wrong. The code reads beautifully. It times out on the large test
case, and if you cannot say why, the interviewer learns that you do not know what your own
tools cost. Every language has this lesson; today you learn Python's version of it.

---

## 2. The story

Rakesh looks after the community hall on the ground floor of a housing society in Nagpur.
There is a meeting every Sunday at ten, and setting out the chairs is his job.

He starts at twenty past eight. The chairs live in a store room at the back, stacked. He
carries them out in stacks of twenty, because carrying them one at a time would mean twenty
walks across the hall instead of one. He sets out four stacks — eighty chairs — in rows of
twenty, and he chalks the seat numbers on the floor at the end of each row so people can
find a place without asking.

By half past nine the hall is nearly full. People are still arriving, and every one of them
does the same thing: walks to the end of the last row and sits in the next free chair. That
takes Rakesh no work at all. He stands at the side and watches.

At ten to ten the eightieth person sits down, and the next man through the door has nowhere
to go. Rakesh walks to the store room and brings out another stack of twenty. It takes him
four minutes and he is sweating afterwards. Then, for the next twenty people, he does
nothing again.

At ten past ten the chief guest's mother arrives. She is eighty-one, she has come from
Amravati, and she cannot sit at the back.

There is one free chair, in the middle of the front row, four seats in — and there is
somebody in it. So Rakesh does the only thing that can be done. He asks everyone in the
front row from the fourth seat onwards to stand up, pick up their bag, and move one seat
along. Nineteen people. Bags, phones, a walking stick, one child asleep on his father's
shoulder. It takes almost seven minutes and two people end up in the wrong row.

Rakesh thinks about this afterwards, over tea. Eighty people sat down that morning and
seventy-nine of them cost him nothing. One person needed a seat in the middle, and that one
cost him seven minutes and a certain amount of goodwill.

The seat numbers, at least, worked. When a woman rang the hall phone to ask where her
husband was sitting, Rakesh did not walk down the row counting. She said fourteen, and he
looked at the chalk marks and went straight there.

---

## 3. The idea in plain English

Rakesh's hall is a Python list, exactly. Let us go through it.

### A list is a row, not a chain

A Python **list** is stored as one continuous run of slots in memory, in order, like the
chairs in a row. Item 0 is next to item 1, which is next to item 2. Nothing is scattered.

That is why the seat numbers worked. Because the row is continuous and every slot is the
same size, the machine can work out where item 14 lives with one multiplication — start of
the row, plus fourteen slot-widths — and go straight there. It never walks the row counting.
So `items[14]` is `O(1)`, and so is `items[999999]`.
[Day 009](../day-009-what-an-array-is/README.md) does the memory picture properly.

### Adding at the end is free. Adding anywhere else is not.

`items.append(x)` puts the value in the next free slot. Nobody moves. That is `O(1)`.

`items.insert(0, x)` puts the value at the front, which means **every single item already in
the list must move one slot along** to make room. That is `O(n)`. It is the front row
standing up with their bags.

The same thing happens in reverse when you remove:

- `items.pop()` takes the last item. Nobody moves. `O(1)`.
- `items.pop(0)` takes the first item, and everything after it shuffles back one place.
  `O(n)`.

**This is the whole lesson.** The end of a list is cheap. The front is expensive. The middle
is expensive. And "expensive" here means proportional to how much is sitting after the
place you touched.

### The stack of twenty: why append is *usually* free

Rakesh does not fetch one chair at a time. He fetches twenty, so that the next nineteen
arrivals cost him nothing at all.

Python does the same. A list keeps a **capacity** — how many slots it has room for — which
is bigger than its **length**, the number of slots actually used. When you append and there
is spare capacity, it is genuinely one step. When capacity runs out, Python allocates a
bigger run of memory, copies everything across, and carries on. That copy is `O(n)`, and it
is the four-minute walk to the store room.

The growth is by roughly one-eighth each time, so the expensive copies get rarer and rarer as
the list grows. Averaged over many appends, the cost per append works out to a constant. The
word for that is **amortised**: `list.append` is **O(1) amortised**, meaning any single
append might be expensive but a long run of them averages out to constant time.

Say it that way in an interview. "Append is O(1) amortised, because the list over-allocates
and only occasionally has to copy" is a complete and correct answer.

### A slice makes a copy

This is the one that surprises people.

```python
first_half = items[:500]
```

That does not create a window onto the first five hundred items. It builds a **new list**
and copies five hundred values into it. The cost is `O(k)`, where `k` is the length of the
slice, in both time and memory.

So `items[:]` copies the whole thing — `O(n)`. And `items[1:]`, which looks like a harmless
way to say "everything except the first", is `O(n)` too. Put that inside a loop and you have
written a quadratic without noticing.

### Tuples: the same row, nailed down

A **tuple** is written with round brackets — `(3, 7, 2)` — and is a list you cannot change.
No append, no assignment to a position, no sorting in place. Reading is identical and
identically fast.

Two reasons you will actually use them:

**They can be dictionary keys and set members.** A list cannot. `seen.add((row, col))` works;
`seen.add([row, col])` raises an error. Every grid problem in this course uses tuple
coordinates for exactly this reason.

**They say "this will not change".** A pair of coordinates, a return of two values, a fixed
record. The immutability is documentation that the machine enforces.

### The operations that are secretly loops

These read like single steps and are not:

| Looks like one step | Actually costs |
|---|---|
| `x in items` | `O(n)` — walks until found |
| `items.index(x)` | `O(n)` |
| `items.count(x)` | `O(n)` |
| `items.remove(x)` | `O(n)` to find, then `O(n)` to shift |
| `min(items)`, `max(items)`, `sum(items)` | `O(n)` |
| `items[a:b]` | `O(b − a)` |
| `sorted(items)` | `O(n log n)` |
| `len(items)` | `O(1)` — this one really is free |

`len()` is `O(1)` because the list stores its own length. That is worth knowing, because it
means there is never a reason to keep your own counter alongside a list.

---

## 4. The picture

What a list actually looks like in memory, with capacity drawn in:

```
  length = 5, capacity = 8

  index      0      1      2      3      4      5      6      7
          +------+------+------+------+------+------+------+------+
  slots   |  12  |  45  |   7  |  99  |  23  |      |      |      |
          +------+------+------+------+------+------+------+------+
                                              ^^^^^^^^^^^^^^^^^^^^
                                              spare room, already paid for

  append(31)  ->  goes straight into slot 5.  Nothing moves.  O(1)
```

**What to notice:** the three empty slots are the stack of chairs Rakesh already carried out.
Appending is free precisely because the room was taken in advance.

Now what `insert(0, 99)` does:

```
  before
  index      0      1      2      3      4
          +------+------+------+------+------+
          |  12  |  45  |   7  |  99  |  23  |
          +------+------+------+------+------+

  every item slides one place right, starting from the back
          +------+------+------+------+------+------+
          |      |  12  |  45  |   7  |  99  |  23  |
          +------+------+------+------+------+------+
             ^
             then the new value drops in

  after
  index      0      1      2      3      4      5
          +------+------+------+------+------+------+
          |  99  |  12  |  45  |   7  |  99  |  23  |
          +------+------+------+------+------+------+

  5 items moved for 1 insert.  With n items, n moves.  O(n)
```

**What to notice:** the work is not in placing the new value. It is in the shuffling that has
to happen first, and there is exactly one shuffle per item already present.

And `pop(0)`, which is the same problem walking the other way:

```
          +------+------+------+------+------+
          |  12  |  45  |   7  |  99  |  23  |
          +------+------+------+------+------+
             ^
             take this out...

          +------+------+------+------+------+
          |  45  |   7  |  99  |  23  |      |
          +------+------+------+------+------+
          <-----  everything shifts left  -----

  pop() from the end instead:
          +------+------+------+------+------+
          |  12  |  45  |   7  |  99  |      |
          +------+------+------+------+------+
                                       ^
                                  nothing moved at all
```

**What to notice:** `pop()` and `pop(0)` differ by three characters and by a factor of n.

Finally, what a slice really produces:

```
  items = [12, 45, 7, 99, 23]
  part  = items[1:4]

  items  +------+------+------+------+------+
         |  12  |  45  |   7  |  99  |  23  |      original, untouched
         +------+------+------+------+------+
                   \      \      \
                    \      \      \    copied, one by one
                     v      v      v
  part   +------+------+------+
         |  45  |   7  |  99  |                    a whole new list
         +------+------+------+
```

**What to notice:** there are now two lists. Changing `part[0]` does not change `items[1]`.
And building `part` cost three copies, which is why a slice inside a loop is dangerous.

---

## 5. The code, built step by step

The point of today is to *measure* these costs rather than believe them, so build a timing
harness and run each operation through it.

Start with the timer.

```python
import time

def time_it(label: str, fn) -> float:
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    print(f"  {label:<34}{elapsed:>10.4f} s")
    return elapsed
```

`time.perf_counter()` is the right clock for measuring short durations — it is monotonic and
high-resolution, unlike `time.time()`. The function takes another function and runs it, which
lets the same timer measure anything.

Now the two ways of building a list.

```python
def build_by_append(n: int) -> list[int]:
    out = []
    for i in range(n):
        out.append(i)          # O(1) amortised
    return out


def build_by_insert(n: int) -> list[int]:
    out = []
    for i in range(n):
        out.insert(0, i)       # O(n) — everything shifts
    return out
```

These two functions produce the same values in opposite orders and differ enormously in
cost. `build_by_append` is `n` steps. `build_by_insert` is `0 + 1 + 2 + ... + (n − 1)`, the
staircase from day 002, which is `n × (n − 1) / 2` — quadratic.

Now the two ways of draining one, which is the trap that actually catches people.

```python
from collections import deque

def drain_from_front_list(n: int) -> None:
    items = list(range(n))
    while items:
        items.pop(0)           # O(n) each time -> O(n^2) total


def drain_from_front_deque(n: int) -> None:
    items = deque(range(n))
    while items:
        items.popleft()        # O(1) each time -> O(n) total
```

A **deque** — say "deck", short for double-ended queue — is a standard-library structure
built for exactly this. It is a chain of small blocks rather than one run, so both ends are
cheap and the middle is not. It is the right answer whenever you need a queue, and you will
use it for breadth-first search from [day 101](../day-101-bfs-level-order/README.md) onwards.

Now the slice trap.

```python
def sum_by_slicing(items: list[int]) -> int:
    total = 0
    while items:
        total += items[0]
        items = items[1:]      # copies the whole rest, every time
    return total
```

This looks functional and tidy. Each `items[1:]` copies `n − 1`, then `n − 2`, then `n − 3`
values. It is the staircase again: `O(n²)` time, and it allocates `O(n²)` bytes in total
along the way.

And the check that a slice really is a copy.

```python
original = [1, 2, 3, 4]
part = original[1:3]
part[0] = 99
print(original)     # [1, 2, 3, 4]  — unchanged
print(part)         # [99, 3]
```

If a slice were a view, `original` would now read `[1, 99, 3, 4]`. It does not. Two separate
lists exist.

Here is the complete program. It measures everything above at a size large enough for the
difference to be undeniable.

```python
"""Day 5 — what Python list operations actually cost. Measure, do not guess."""

import time
from collections import deque


def time_it(label: str, fn) -> float:
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    print(f"  {label:<34}{elapsed:>10.4f} s")
    return elapsed


# ---- building ------------------------------------------------------------

def build_by_append(n: int) -> list[int]:
    """O(n): each append is O(1) amortised."""
    out: list[int] = []
    for i in range(n):
        out.append(i)
    return out


def build_by_insert(n: int) -> list[int]:
    """O(n^2): each insert at the front shifts everything already there."""
    out: list[int] = []
    for i in range(n):
        out.insert(0, i)
    return out


# ---- draining ------------------------------------------------------------

def drain_list_front(n: int) -> None:
    """O(n^2): pop(0) shifts the whole remaining list every time."""
    items = list(range(n))
    while items:
        items.pop(0)


def drain_list_back(n: int) -> None:
    """O(n): pop() from the end moves nothing."""
    items = list(range(n))
    while items:
        items.pop()


def drain_deque_front(n: int) -> None:
    """O(n): a deque is cheap at both ends."""
    items = deque(range(n))
    while items:
        items.popleft()


# ---- slicing -------------------------------------------------------------

def sum_by_slicing(n: int) -> int:
    """O(n^2): every slice copies the rest of the list."""
    items = list(range(n))
    total = 0
    while items:
        total += items[0]
        items = items[1:]
    return total


def sum_by_index(n: int) -> int:
    """O(n): walk it once, copy nothing."""
    items = list(range(n))
    total = 0
    for x in items:
        total += x
    return total


def show_slice_is_a_copy() -> None:
    original = [1, 2, 3, 4]
    part = original[1:3]
    part[0] = 99
    print(f"  original after changing the slice : {original}")
    print(f"  the slice itself                  : {part}")


if __name__ == "__main__":
    N = 50_000

    print(f"building a list of {N:,}")
    a = time_it("append at the end   O(1)", lambda: build_by_append(N))
    b = time_it("insert at the front O(n)", lambda: build_by_insert(N))
    print(f"  insert is {b / a:,.0f}x slower\n")

    print(f"draining a list of {N:,}")
    c = time_it("list.pop()      from the back", lambda: drain_list_back(N))
    d = time_it("list.pop(0)     from the front", lambda: drain_list_front(N))
    e = time_it("deque.popleft() from the front", lambda: drain_deque_front(N))
    print(f"  pop(0) is {d / e:,.0f}x slower than popleft()\n")

    print(f"summing a list of {N:,}")
    f = time_it("walk it once        O(n)", lambda: sum_by_index(N))
    g = time_it("re-slice each time  O(n^2)", lambda: sum_by_slicing(N))
    print(f"  slicing is {g / f:,.0f}x slower\n")

    print("is a slice a copy or a view?")
    show_slice_is_a_copy()
```

This is exactly what it printed:

```
building a list of 50,000
  append at the end   O(1)              0.0053 s
  insert at the front O(n)              0.9690 s
  insert is 181x slower

draining a list of 50,000
  list.pop()      from the back         0.0063 s
  list.pop(0)     from the front        7.8440 s
  deque.popleft() from the front        0.0049 s
  pop(0) is 1,606x slower than popleft()

summing a list of 50,000
  walk it once        O(n)              0.0055 s
  re-slice each time  O(n^2)            7.4298 s
  slicing is 1,349x slower

is a slice a copy or a view?
  original after changing the slice : [1, 2, 3, 4]
  the slice itself                  : [99, 3]
```

**Read the ratios, not the times.** Every pair on this list does the same job and produces
the same answer. One member of each pair is hundreds to over a thousand times slower, and in
every case the difference is one method name or one piece of syntax. Now double `N` to
100,000 and run it again: the fast rows double and the slow rows quadruple, which is the
doubling test from [day 003](../day-003-big-o-in-plain-english/README.md) confirming the
shape.

---

## 6. What it costs

The full table. This is the one to know cold, because interviewers ask for individual rows
of it directly.

| Operation | Cost | Why |
|---|---|---|
| `items[i]` (read or write) | `O(1)` | position computed by arithmetic, no walking |
| `len(items)` | `O(1)` | the length is stored |
| `items.append(x)` | `O(1)` amortised | spare capacity; occasional resize and copy |
| `items.pop()` | `O(1)` | nothing after it to move |
| `items.insert(0, x)` | `O(n)` | everything shifts right |
| `items.insert(i, x)` | `O(n − i)` | everything after `i` shifts |
| `items.pop(0)` | `O(n)` | everything shifts left |
| `items.remove(x)` | `O(n)` | find it, then shift |
| `x in items` | `O(n)` | walks until found |
| `items.index(x)` | `O(n)` | same walk |
| `items[a:b]` | `O(b − a)` | builds and fills a new list |
| `items + other` | `O(n + m)` | builds a new list holding both |
| `items.sort()` | `O(n log n)` | Timsort, in place, `O(n)` extra space |
| `sorted(items)` | `O(n log n)` | same, plus a full copy |
| `items.reverse()` | `O(n)` | in place, `O(1)` extra |
| `min` / `max` / `sum` | `O(n)` | one pass each |
| `items.copy()` or `items[:]` | `O(n)` | full copy |

**The amortised argument, with the arithmetic.** Python grows a list by roughly 12.5% each
time it runs out, so the capacities go 0, 4, 8, 16, 25, 35, 46, and so on. Building a list of
one million by appending triggers around **80** resizes, and the total number of values
copied across all of them is under two million:

```
4 + 8 + 16 + 25 + ... (each about 1.125x the last, up to 1,000,000)
total copied  ~ 1.9 million
divided by    1,000,000 appends
            = about 2 extra copies per append, on average
```

Two extra operations per append is a constant. That is what "amortised `O(1)`" means, in
arithmetic rather than in words.

**Where the quadratics come from.** Any `O(n)` operation inside a loop that runs `n` times:

```
n iterations x O(n) work each = O(n^2)

  50,000 x 50,000 / 2 = 1.25 billion element moves
```

At Python's speed that is the 0.38 seconds you saw above, and at n = 1,000,000 it is over
two hours. This is the single most common accidental quadratic in Python, and every one of
them is a one-line fix.

**Space.** A slice of length `k` costs `k` slots. A list of a million integers costs roughly:

```
1,000,000 x 8 bytes per reference          =  8 MB for the list itself
1,000,000 x 28 bytes per small int object  = 28 MB for the objects
                                            -------
                                              36 MB
```

Small integers from −5 to 256 are shared by Python, so a list of a million zeros costs only
the 8 MB. That is why `[0] * 1_000_000` is cheap and `list(range(1_000_000))` is not.

---

## 7. The traps

### Trap one: the queue built out of a list

This is the one that will actually cost you an interview. You need a queue — first in, first
out — so you write the obvious thing:

```python
def process_in_order(jobs: list[str]) -> list[str]:
    done = []
    queue = list(jobs)
    while queue:
        job = queue.pop(0)        # <- O(n), every single time
        done.append(job)
    return done
```

It is correct. It reads well. It is `O(n²)`, because each `pop(0)` shifts the entire
remaining queue one slot left.

```
n = 100,000
  list.pop(0)     :  32.18 s
  deque.popleft() :   0.0182 s
  ratio           :  1,769 x
```

The fix is two lines:

```python
from collections import deque

def process_in_order(jobs: list[str]) -> list[str]:
    done = []
    queue = deque(jobs)           # a deque, not a list
    while queue:
        job = queue.popleft()     # O(1)
        done.append(job)
    return done
```

**Say this rule out loud until it is automatic: if you take from the front, use a `deque`.**
Every breadth-first search you write from day 101 onwards depends on it, and a BFS with
`pop(0)` in it will time out on any real graph.

### Trap two: the multiplication that shares one list

This one produces no error at all. It produces wrong answers, quietly.

```python
grid = [[0] * 3] * 3
grid[0][0] = 5
print(grid)
```

```
[[5, 0, 0], [5, 0, 0], [5, 0, 0]]
```

One assignment changed three rows. The reason is that `[[0] * 3] * 3` does not build three
rows. It builds **one** row and then puts three references to that same row in the outer
list. All three names point at the same object.

The inner `[0] * 3` is fine, because integers cannot be changed in place. It is the outer
multiplication that is the bug.

The fix is a list comprehension, which evaluates the inner expression fresh each time:

```python
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 5
print(grid)
```

```
[[5, 0, 0], [0, 0, 0], [0, 0, 0]]
```

This comes back with force on [day 016](../day-016-2d-arrays/README.md), and it is one of
the most common bugs in grid problems.

### The related error you will actually see

Having been bitten by the above, people sometimes over-correct and build an empty list, then
assign into it by position:

```python
result = []
for i in range(5):
    result[i] = i * i
```

```
Traceback (most recent call last):
  File "d5.py", line 3, in <module>
    result[i] = i * i
    ~~~~~~^^^
IndexError: list assignment index out of range
```

Read it precisely, because the wording is doing real work. It says **list assignment index**,
not just "index". A list can only be assigned to at a position that already exists. `result`
has length 0, so position 0 does not exist yet, and there is nothing to overwrite. Either
`append` instead, or pre-fill with `result = [0] * 5`.

The `~~~~~~^^^` marks under the traceback point at the exact expression Python objected to —
the `result[i]` on the left of the assignment, not the arithmetic on the right.

---

## 8. In the interview

### How it gets asked

- *"What's the complexity of inserting at the front of a Python list?"* — the direct
  version. The answer is `O(n)`, and the reason is the shifting.
- *"You're using pop(0) in that loop — what does that cost?"* — the live version, said
  gently, while you are writing. It is a rescue, not a trap. Take it.
- *"Why is append O(1) when the list sometimes has to be reallocated?"* — the amortised
  question.
- *"Does slicing copy?"* — a one-word answer, followed by "so what does that mean inside a
  loop?".

### What to say out loud, in the first ninety seconds

1. **Say what a list is.** *"A Python list is a dynamic array — one continuous run of
   references, so indexing is O(1) by arithmetic."*
2. **Say where the cheap end is.** *"Appending and popping at the end are O(1), because
   nothing after them has to move."*
3. **Say why the other end is not.** *"Inserting or popping at the front is O(n), because
   every remaining element shifts one slot."*
4. **Give the amortised answer before being asked.** *"Append is O(1) amortised — the list
   over-allocates, so most appends land in spare capacity and only occasionally does it
   resize and copy. Averaged out, that's a constant per append."*
5. **Name the fix.** *"So if I need a queue, I use `collections.deque`, which is O(1) at
   both ends."*
6. **Add the slice.** *"And slicing copies — `items[1:]` is O(n), so re-slicing inside a
   loop is an accidental quadratic."*

Steps 4 and 5 are the ones that make you sound like somebody who has shipped Python rather
than revised it.

### The follow-ups

**"Why is inserting at the front O(n) but appending O(1)?"**
Because a list is one contiguous block, and the position of every element is its offset from
the start. Insert at the front and every element's correct position changes, so every one of
them has to be physically moved. Append at the end and nobody's position changes — the new
value goes into the next free slot. The asymmetry is a consequence of the memory layout, not
a design choice about the API.

**"Then why is append only *amortised* O(1)?"**
Because when the spare capacity runs out, Python has to allocate a bigger block and copy
everything across, which is O(n) for that one append. It grows by about 12.5%, so those
copies get proportionally rarer as the list grows. Adding up the cost of every copy while
building a list of n and dividing by n gives a constant of about two, so the average per
append is O(1) even though individual appends are not.

**"Does slicing create a copy or a view?"**
A copy, always, for lists. `items[a:b]` allocates a new list of length `b − a` and copies the
references in. That matters twice: mutating a slice never affects the original, and slicing
inside a loop is O(n) work inside an O(n) loop. If you want a view without copying, you use
indices — `left` and `right` variables — which is exactly what the two-pointer pattern from
[day 027](../day-027-two-pointers-idea/README.md) is. Note that NumPy slices *are* views,
which is the opposite convention and a common source of confusion.

**"When would you use a tuple instead of a list?"**
Two reasons. When I need it as a dictionary key or a set member — a list is unhashable and
raises `TypeError: unhashable type: 'list'`, so grid coordinates go in as `(row, col)`. And
when I want to state that a group of values is fixed, like a returned pair or a fixed
record. Tuples are also slightly smaller and marginally faster to build, but that is never
the reason I would choose one.

### A model answer

The interviewer has watched the candidate write a breadth-first search using
`queue.pop(0)` and asks about the complexity.

> "Let me look at that line again, because I think I've got a problem there.
>
> A Python list is a dynamic array — one contiguous block, with elements laid out in order.
> That's what makes `items[i]` O(1): it's a multiplication and an offset, not a walk. But it
> also means that removing from the front is O(n), because every remaining element has to
> shift one slot left to close the gap.
>
> So `queue.pop(0)` is O(n), and it's inside a loop that runs once per element. That makes
> the BFS O(V²) on the queue operations alone rather than O(V + E). On a graph with a
> hundred thousand vertices, that's about five billion element moves — it will time out.
>
> The fix is `collections.deque`, which is a doubly-linked list of blocks rather than one
> contiguous run. Both ends are O(1), so `popleft` is constant time, and the BFS goes back to
> O(V + E). The trade is that a deque doesn't give you O(1) indexing into the middle — but a
> queue never needs that.
>
> While I'm on it, two related things I'd watch for. `append` is O(1) amortised, not strictly
> O(1) — the list over-allocates by about an eighth, so most appends are free and occasionally
> one triggers a resize and a full copy. Averaged out it's constant, which is what matters
> here.
>
> And slicing copies. If I'd written `queue = queue[1:]` instead of popping, that would be
> O(n) per iteration too, and it would also allocate a new list every time — so quadratic in
> memory traffic as well as in time."

That answer diagnoses a live bug, gives the fix, states the trade-off of the fix, and adds
two adjacent facts without padding. It is what fluency in a language sounds like.

---

## 9. Recall card

1. A Python list is a **dynamic array**: one contiguous block. `items[i]` and `len()` are
   `O(1)`.
2. **The end is cheap, the front is expensive.** `append` and `pop()` are `O(1)`.
   `insert(0, x)` and `pop(0)` are `O(n)`, because everything shifts.
3. **`append` is `O(1)` amortised** — the list over-allocates by about 12.5%, so resizes get
   rarer and average out to a constant.
4. **Take from the front → use `collections.deque`.** `popleft()` is `O(1)`. Every BFS
   depends on this.
5. **Slicing copies.** `items[1:]` is `O(n)` in time and memory. And `[[0]*3]*3` makes three
   references to one row — use `[[0]*3 for _ in range(3)]`.
