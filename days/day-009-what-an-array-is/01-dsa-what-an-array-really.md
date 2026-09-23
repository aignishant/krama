---
day: 9
track: dsa
title: "What an array really is in memory"
phase: "Arrays"
status: written
---

# Day 009 · DSA — What an array really is in memory

**After today you can:** You can explain why arr[500000] is as fast as arr[0], using one picture.

**The interviewer asks it as:** *Why is array indexing O(1)?*

---

## 1. What this is, and why they ask it

An **array** is a run of slots in memory, all the same size, laid side by side with nothing in
between. Because they are the same size and side by side, the position of slot number `i` can
be **calculated** rather than searched for.

That calculation is one multiplication and one addition. It does not get longer when the array
does. That is the entire reason `arr[500000]` costs the same as `arr[0]`, and it is the answer
to today's question.

Interviewers ask this because it is the foundation under everything else. Why is inserting at
the front `O(n)`? Because of the layout. Why is a linked list `O(n)` to index but `O(1)` to
insert? Because of the layout. Why is a hash table fast? Because it turns a key into an array
position. A candidate who says "indexing is O(1) because arrays are random access" has given
a name instead of a reason. A candidate who says "address equals base plus i times element
size, which is one multiply and one add" has actually answered.

---

## 2. The story

Ganesh has been an usher at the cinema on M.G. Road for eleven years. There are four hundred
and eighty seats downstairs, in twenty rows of twenty-four, and the rows are lettered A to T
with the numbers running left to right.

His job during a show is mostly latecomers, and latecomers are easy. A man comes in twelve
minutes after the start, holding up his phone with the booking on it, and Ganesh looks at it
for about a second. H-14. He walks the man down the aisle to row H, points, and goes back to
the door. It takes fourteen seconds and he does not think about it at all.

He does not start at row A and count. He does not look at seat H-1, then H-2, then H-3. He
knows that H is the eighth letter, so it is the eighth row back, and every row is the same
depth. He knows every seat is the same width, so seat 14 is thirteen seats along. Both of
those are sums he does without noticing he is doing them, and the answer is the same amount
of work whether the ticket says H-14 or A-1 or T-24.

The thing that makes it work, and Ganesh has thought about this because he was asked once, is
that **every seat is exactly the same size**.

There was a proposal two years ago to put in six wider seats for couples, at the back of row
M. The manager wanted it. Ganesh said one thing in the meeting, which was that if six seats
in row M are wider, then row M holds twenty-one seats instead of twenty-four, and M-14 is no
longer where M-14 has always been, and the seat you reach by walking thirteen widths along is
not the seat printed on the ticket any more. In the end they built the wide seats as a
separate section upstairs with its own numbering, which is exactly the right answer and is
also what a computer does.

He also knows the other kind of hall, because the cinema does private hires. Last November a
company booked the whole place, no allocated seating, sit where you like. At the end somebody
found a phone left on a seat, and finding out whose it was meant Ganesh walking the aisles
and asking. Four hundred and eighty seats, no numbers, and there is nothing to calculate. You
just look, and look, and look.

One more thing about his walking. When four people come in together for H-14 to H-17, he
takes them down in one trip. When four people come in one at a time over twenty minutes for
H-14, then C-2, then Q-19, then F-8, that is four trips down the aisle and back, and it is
a much longer twenty minutes even though it is the same four seats.

---

## 3. The idea in plain English

The cinema hall is an array, and Ganesh's fourteen seconds is `O(1)` indexing.

### The three things that make it work

An array has three properties, and all three are required. Remove any one and the arithmetic
stops working.

**1. The slots are contiguous.** They sit next to each other in memory with no gaps. Row H
starts where row G ends.

**2. Every slot is the same size.** Every seat is the same width. In memory, every element of
an array of 32-bit integers takes exactly 4 bytes.

**3. You know where it starts.** Ganesh knows where row A is. The program holds the **base
address** — the memory address of element 0.

Given those three, the position of element `i` is:

```
address of items[i] = base_address + (i x size_of_one_element)
```

One multiplication, one addition. **That is the whole answer to today's question.**

Put real numbers on it, because concrete beats symbolic. An array of 4-byte integers starting
at address 1000:

```
items[0]  ->  1000 + (0 x 4)  =  1000
items[1]  ->  1000 + (1 x 4)  =  1004
items[7]  ->  1000 + (7 x 4)  =  1028
items[500000] -> 1000 + (500000 x 4) = 2,001,000
```

The last line is the same two operations as the first. Nothing was walked. Nothing was
compared. **This is what "random access" means**: you may reach any position directly, in the
same time, in any order.

### Why counting starts at zero

Because element 0 is at `base + 0 × size`, which is exactly the base address. Zero-indexing
makes the first element's offset zero, so the formula has no `− 1` in it. If arrays started
at 1, every access would be `base + (i − 1) × size`, and the world would have a billion more
off-by-one errors than it already does.

### What a search costs, by contrast

The private hire with no seat numbers is a list you have to scan. If you do not know where
something is, you look at position 0, then 1, then 2, until you find it or run out. That is
`O(n)`, and it is what `x in items` does. From
[day 006](../day-006-python-strings-dicts-sets/README.md) you know the fix when you need
this often, which is a hash table — and a hash table is a **computed index into an array**.
It is the cinema seat number, worked out from the person's name.

### What Python actually stores, which is not what C stores

This matters, and interviewers who use Python will ask about it.

A **C array** of integers stores the integers themselves, side by side:

```
   +----+----+----+----+
   | 12 | 45 |  7 | 99 |     4 bytes each, values in the slots
   +----+----+----+----+
```

A **Python list** stores **references** — memory addresses of objects that live elsewhere:

```
   +--------+--------+--------+--------+
   | ptr    | ptr    | ptr    | ptr    |     8 bytes each, addresses in the slots
   +---|----+---|----+---|----+---|----+
       |        |        |        |
       v        v        v        v
     int 12   int 45   int 7   int 99      objects scattered on the heap
```

The slots are still uniform (8 bytes each) and still contiguous, so **indexing is still
`O(1)`** — the formula is unchanged. What you lose is that the *values* are not next to each
other, only the addresses are. Two consequences:

- A Python list can hold mixed types, because every slot holds an address of the same size
  whatever it points at.
- Walking a Python list touches memory all over the place, which is slower than walking a C
  array for reasons covered next.

When you genuinely need packed numbers in Python, that is what **NumPy** arrays and the
standard library's `array` module are for.

### Ganesh's trips down the aisle: locality

The last part of the story is the part nobody expects to matter and which matters enormously.

Memory is not read one byte at a time. The processor fetches a whole block — a **cache
line**, typically **64 bytes** — and keeps it in a small fast store called a **cache**. So
reading `items[0]` also brings `items[1]` through `items[15]` along for free, if they are
4-byte integers.

Reading an array **in order** therefore costs one fetch per sixteen elements. Reading it in a
random order costs one fetch per element. Same number of accesses, same `O(n)`, and up to ten
times the wall-clock time.

That is Ganesh taking four people down in one trip against four separate trips. The Big-O is
identical. The afternoon is not. [Day 010](../day-010-traversal-patterns/README.md) makes
this practical, and the system design lesson today puts numbers on the whole hierarchy.

---

## 4. The picture

The array in memory, with real addresses:

```
   base address = 1000, each element is 4 bytes

   index        0      1      2      3      4      5      6
             +------+------+------+------+------+------+------+
   value     |  12  |  45  |   7  |  99  |  23  |  81  |  64  |
             +------+------+------+------+------+------+------+
   address    1000   1004   1008   1012   1016   1020   1024

   items[4]:  1000 + 4 x 4 = 1016.  Go there. Read. Done.
              ^^^^^^^^^^^^
              one multiply, one add — for ANY value of the index
```

**What to notice:** the address row goes up by exactly 4 each time, without exception. That
regularity is the whole trick. Break it — make one element a different size — and the
arithmetic gives you a wrong address, which is why arrays hold one type.

Now the contrast, which is what indexing would cost without those properties:

```
   ARRAY (numbered seats)                LINKED LIST (day 078)

   items[4] -> compute -> read            head -> [12] -> [45] -> [7] -> [99] -> [23]
                                                    1       2      3      4      5
   one step, any index                    five steps to reach the fifth

   O(1)                                   O(n)
```

**What to notice:** the linked list has no formula available, because its pieces are scattered
and each one only knows where the next is. It buys something in return, which is
[day 011](../day-011-insert-and-delete/README.md)'s subject.

And the cache line, which is Ganesh's trips:

```
   one fetch brings 64 bytes = 16 four-byte integers

   +---------------- one cache line, 64 bytes ----------------+
   | i0 | i1 | i2 | i3 | i4 | i5 | i6 | i7 | ... | i14 | i15  |
   +----------------------------------------------------------+

   walking in order  : read i0 (fetch), i1..i15 free, read i16 (fetch), ...
                       1 fetch per 16 reads

   random order      : read i9000 (fetch), i22 (fetch), i7401 (fetch), ...
                       1 fetch per read, and each fetch is ~100x slower than the cache
```

**What to notice:** both patterns do `n` reads and both are `O(n)`. The order decides whether
you pay for `n/16` fetches or `n` of them.

---

## 5. The code, built step by step

The point today is to see that the address formula is real, and to measure that position does
not affect cost.

Start by doing the arithmetic yourself.

```python
def address_of(base: int, index: int, element_size: int) -> int:
    """The formula the machine uses. One multiply, one add."""
    return base + index * element_size
```

That is the whole mechanism. Everything else in this section is evidence that it is what
really happens.

Now confirm that the position does not matter.

```python
import time

def time_reads(items: list[int], index: int, repeats: int = 2_000_000) -> float:
    start = time.perf_counter()
    for _ in range(repeats):
        _ = items[index]
    return time.perf_counter() - start
```

Reading the same index two million times, at different positions in a ten-million-element
list. If indexing were a walk, reading position 9,999,999 would take ten million times as
long as position 0.

Now show what Python actually stores, using the standard library.

```python
import sys

nums = [1, 2, 3, 4, 5]
print(sys.getsizeof(nums))          # the list object: slots for 5 references
print(sys.getsizeof(nums[0]))       # the integer object itself, held elsewhere
```

`sys.getsizeof` reports the size of one object and does **not** follow references. So the
list's own size counts 8 bytes per slot, and each integer's 28 bytes are separate. That is
the two-level picture from §3, made visible.

Now the packed version, for comparison.

```python
import array

packed = array.array("i", range(1000))     # 'i' = 4-byte signed integers
print(packed.itemsize)                     # 4
print(sys.getsizeof(packed))               # about 4000 + a small header
```

`array.array` stores the values themselves, exactly like a C array. Same `O(1)` indexing, a
fraction of the memory, and only one type allowed — which is the trade.

Now the locality demonstration, which is the part people find surprising.

```python
def sum_in_order(items: list[int]) -> int:
    total = 0
    for i in range(len(items)):
        total += items[i]
    return total


def sum_strided(items: list[int], stride: int) -> int:
    """Same number of reads, jumping by `stride` each time."""
    total = 0
    n = len(items)
    for start in range(stride):
        for i in range(start, n, stride):
            total += items[i]
    return total
```

Both functions read every element exactly once. `sum_strided` reads them in an order that
jumps by `stride` positions, which defeats the cache line when the stride is large enough.

Here is the complete program.

```python
"""Day 9 — the address formula is real, and position does not cost anything."""

import array
import random
import sys
import time


def address_of(base: int, index: int, element_size: int) -> int:
    """What the machine computes for items[index]. Two operations, always."""
    return base + index * element_size


def time_reads(items: list[int], index: int, repeats: int = 2_000_000) -> float:
    start = time.perf_counter()
    for _ in range(repeats):
        _ = items[index]
    return time.perf_counter() - start


def sum_in_order(items: list[int]) -> int:
    """O(n) reads, in address order — one cache line fetch per 8 references."""
    total = 0
    for i in range(len(items)):
        total += items[i]
    return total


def sum_shuffled(items: list[int], order: list[int]) -> int:
    """O(n) reads, in a random order — a fetch per read."""
    total = 0
    for i in order:
        total += items[i]
    return total


if __name__ == "__main__":
    print("the address formula, by hand (base 1000, 4-byte elements)")
    for i in (0, 1, 7, 500_000):
        print(f"  items[{i:<8}] -> 1000 + {i} x 4 = {address_of(1000, i, 4):,}")

    print("\nis reading position 0 faster than position 9,999,999?")
    big = list(range(10_000_000))
    for index in (0, 1_000, 5_000_000, 9_999_999):
        secs = time_reads(big, index)
        print(f"  items[{index:<9,}] : {secs:.4f} s for 2,000,000 reads")

    print("\nwhat a Python list really holds")
    nums = [1, 2, 3, 4, 5]
    print(f"  sys.getsizeof(list of 5)     : {sys.getsizeof(nums)} bytes"
          f"  (header + 5 references)")
    print(f"  sys.getsizeof(one int)       : {sys.getsizeof(nums[0])} bytes"
          f"  (stored elsewhere, not in the list)")
    packed = array.array("i", range(5))
    print(f"  array.array('i') itemsize    : {packed.itemsize} bytes"
          f"  (the value itself, packed)")
    print(f"  sys.getsizeof(array of 1000) : {sys.getsizeof(array.array('i', range(1000))):,}"
          f" bytes vs list {sys.getsizeof(list(range(1000))):,}")

    print("\nsame number of reads, different order (cache locality)")
    n = 4_000_000
    data = list(range(n))
    order = list(range(n))
    random.seed(7)
    random.shuffle(order)

    t0 = time.perf_counter(); sum_in_order(data);      a = time.perf_counter() - t0
    t0 = time.perf_counter(); sum_shuffled(data, order); b = time.perf_counter() - t0
    print(f"  in address order : {a:.4f} s")
    print(f"  in random order  : {b:.4f} s")
    print(f"  same O(n), {b / a:.1f}x the wall-clock time")
```

This is exactly what it printed:

```
the address formula, by hand (base 1000, 4-byte elements)
  items[0       ] -> 1000 + 0 x 4 = 1,000
  items[1       ] -> 1000 + 1 x 4 = 1,004
  items[7       ] -> 1000 + 7 x 4 = 1,028
  items[500000  ] -> 1000 + 500000 x 4 = 2,001,000

is reading position 0 faster than position 9,999,999?
  items[0        ] : 0.1589 s for 2,000,000 reads
  items[1,000    ] : 0.1571 s for 2,000,000 reads
  items[5,000,000] : 0.1966 s for 2,000,000 reads
  items[9,999,999] : 0.1614 s for 2,000,000 reads

what a Python list really holds
  sys.getsizeof(list of 5)     : 104 bytes  (header + 5 references)
  sys.getsizeof(one int)       : 28 bytes  (stored elsewhere, not in the list)
  array.array('i') itemsize    : 4 bytes  (the value itself, packed)
  sys.getsizeof(array of 1000) : 4,200 bytes vs list 8,056

same number of reads, different order (cache locality)
  in address order : 0.5647 s
  in random order  : 2.9137 s
  same O(n), 5.2x the wall-clock time
```

**The second block is the answer to the interview question, measured.** Four positions, ten
million apart, and the times agree to within a few percent — noise, not a trend. Position does
not cost anything, because position is computed rather than reached. If indexing were a walk,
the last row would be ten million times the first.

**The last block is the answer to the question they ask next.** Same `O(n)`, same number of
reads, and five times the time — purely because of the order. Big-O is right and it is not the
only thing that is true.

**And note the memory block.** A list of five holds 104 bytes for its header and five
references; each integer is a further 28 bytes living elsewhere. A thousand values packed in an
`array.array` is 4,200 bytes against the list's 8,056 — and the list's figure still does not
include the integer objects it points at.

---

## 6. What it costs

**Indexing.** One multiply, one add, one memory read:

```
items[i]  ->  base + i x size    2 arithmetic operations
              read that address  1 memory access
```

Constant, for any `i`, in any array, of any length. **`O(1)` time, `O(1)` space.**

**What a memory access actually costs**, which is where the constant hides:

| Where the data is | Time | In "if one cycle were one second" terms |
|---|---|---|
| Register | 0 cycles | now |
| L1 cache | ~1 ns | 1 second |
| L2 cache | ~4 ns | 4 seconds |
| L3 cache | ~15 ns | 15 seconds |
| Main memory (RAM) | ~80 ns | 1.5 minutes |

So `items[i]` is `O(1)`, and the constant varies by a factor of **eighty** depending on
whether the value is already in cache. Walking in order keeps you in the left-hand rows.
Jumping about puts you in the right-hand one.

**The cache-line arithmetic.** A 64-byte line holding 4-byte integers:

```
64 / 4 = 16 integers per fetch

sequential : 1,000,000 reads / 16 = 62,500 fetches
random     : 1,000,000 reads      = 1,000,000 fetches
                                    -----------
                                    16x more memory traffic
```

You measured about 5× rather than 16× because Python's interpreter overhead dominates and
hides some of it. In C the same experiment gives close to the full factor.

**Memory used by an array of n elements:**

```
C array of 4-byte ints, n = 1,000,000       :  4 MB
Python list of ints,    n = 1,000,000       :  8 MB of references
                                             + 28 MB of int objects  = 36 MB
array.array('i'),       n = 1,000,000       :  4 MB
NumPy int32 array,      n = 1,000,000       :  4 MB
```

**Nine times the memory** for the ordinary Python list. For interview problems this never
matters. For anything numerical at scale it decides the design, and it is why NumPy exists.

**Why the layout decides the other operations.** Everything on
[day 011](../day-011-insert-and-delete/README.md) follows from this section:

```
read  items[i]      -> compute address                       O(1)
write items[i] = v  -> compute address, store                O(1)
append              -> write at the end (capacity allowing)  O(1) amortised
insert at front     -> move n elements one slot along        O(n)
delete from front   -> move n-1 elements back one slot       O(n)
search for a value  -> no formula available; look at each    O(n)
```

Notice that the first two are fast *because* of contiguity, and the middle two are slow for
exactly the same reason. **Contiguity is not a free win. It is a trade**, and the thing it
trades away is cheap insertion in the middle.

---

## 7. The traps

### Trap one: the index that is one too far

The formula does not check anything. `base + i × size` produces an address for any `i` at
all, including ones outside the array. In C, reading it gives you whatever happens to be
there — a silent, undebuggable wrong answer, or a crash if the address is not yours. That
class of bug is called a **buffer overflow** and it is the source of a large fraction of all
security vulnerabilities ever recorded.

Python checks the bound for you, and tells you plainly:

```python
items = [10, 20, 30, 40, 50]
for i in range(len(items) + 1):
    print(items[i])
```

```
10
20
30
40
50
Traceback (most recent call last):
  File "d9.py", line 3, in <module>
    print(items[i])
          ~~~~~^^^
IndexError: list index out of range
```

The five correct values print first, then it fails on the sixth. `range(len(items))` gives
`0..4`; adding one gives `0..5`, and there is no slot 5.

The check costs a comparison on every access, which is a real cost Python pays for safety.
And note that Python has a second, sneakier behaviour: **negative indices are legal**.
`items[-1]` is the last element, which is convenient and means a bug that produces `-1`
silently reads the wrong end instead of raising.

**How to catch it every time:** the valid indices of a list of length `n` are `0` to `n − 1`.
When you write a loop bound, say those two numbers out loud. And when an index could be
negative, check `0 <= i < len(items)` explicitly rather than trusting an exception you will
not get.

### Trap two: assuming a Python list is packed

Here is a function meant to be memory-efficient for a large numeric dataset:

```python
def load_readings(n: int) -> list[int]:
    return [i * 3 for i in range(n)]

readings = load_readings(50_000_000)
```

The expectation is 50 million × 4 bytes = 200 MB. The reality:

```
Traceback (most recent call last):
  File "d9.py", line 5, in <module>
    readings = load_readings(50_000_000)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d9.py", line 2, in load_readings
    return [i * 3 for i in range(n)]
           ^^^^^^^^^^^^^^^^^^^^^^^^^
MemoryError
```

50 million references is 400 MB, plus 50 million integer objects at 28 bytes each is another
1.4 GB. Nearly 1.8 GB for data that would be 200 MB packed.

The fix, when the data is genuinely numeric and large:

```python
import array
readings = array.array("i", (i * 3 for i in range(50_000_000)))   # 200 MB
```

or NumPy, which is what real numerical code uses.

**The general point:** every element of a Python list is an object with its own header, and
the list holds only the addresses. `sys.getsizeof(a_list)` will happily tell you 400 MB while
the process uses 1.8 GB, because it does not follow the references. When memory matters,
measure the process, not the object.

---

## 8. In the interview

### How it gets asked

- *"Why is array indexing O(1)?"* — the direct version. Give the formula, not the phrase
  "random access".
- *"What's the difference between an array and a linked list?"* — the comparison version.
  Layout first, then the consequences.
- *"Why is inserting at the front of an array O(n)?"* — the same knowledge, applied. It is
  contiguity's bill.
- *"Two loops do the same number of operations but one is five times slower. Why?"* — the
  cache-locality version, and it is a senior-level question.

### What to say out loud, in the first ninety seconds

1. **State the layout.** *"An array is a contiguous block of equal-sized slots, and the
   program knows the address it starts at."*
2. **Give the formula.** *"So the address of element i is base plus i times the element size.
   One multiply and one add."*
3. **Say why that ends the question.** *"That's the same two operations whatever i is. There's
   no walking, no comparison, no search — so index 500,000 costs exactly what index 0 costs."*
4. **Name the requirement.** *"It only works because every element is the same size. That's
   why an array holds one type — if elements varied in size the arithmetic wouldn't land in
   the right place."*
5. **Give the cost of the same property.** *"The same contiguity is why inserting at the front
   is O(n): every element after the insertion point has to physically move, because their
   correct addresses all changed."*
6. **Add the Python detail if it applies.** *"In Python a list stores references rather than
   the values, so the slots are 8 bytes each and the objects live elsewhere. Indexing is
   still O(1) — the slots are still uniform and contiguous — but the values aren't adjacent,
   which costs you cache locality."*

Steps 5 and 6 are what make this an answer rather than a definition.

### The follow-ups

**"Then why is a linked list O(n) to index?"**
Because there is no formula available. A linked list's nodes are scattered wherever the
allocator put them, and each one only knows the address of the next. So to reach the fifth
element you have to visit the first four — there is no arithmetic that jumps you there. What
it buys is the other side: inserting into the middle is O(1) once you hold the node, because
nothing has to move, only two references change. Array and linked list are the same trade in
opposite directions: arrays pay at insertion to make access free, linked lists pay at access
to make insertion free.

**"Two functions read the same million elements and one is five times slower. What's
happening?"**
Almost certainly cache locality. Memory is fetched in 64-byte lines, so reading in address
order gets roughly sixteen 4-byte integers per fetch, while reading in a scattered order
costs a fetch per element — and a main-memory fetch is about eighty times slower than an L1
cache hit. Both are O(n) and both do the same number of logical reads; only the order differs.
This is also why iterating a 2D array row by row beats column by column, and why array-based
structures often beat linked ones in practice despite identical complexity.

**"Why do arrays hold only one type?"**
Because the address formula multiplies by a fixed element size. If elements varied in size,
`base + i × size` would land in the middle of some element rather than at the start of the
one you asked for, and there would be no way to compute a position without walking. Python
sidesteps this by storing uniform 8-byte references and letting the objects themselves vary,
which is exactly how it gets heterogeneous lists while keeping O(1) indexing.

**"Why do arrays start at zero?"**
Because the offset of the first element is zero — it lives at the base address itself. So
`base + i × size` works with no adjustment. Starting at 1 would put a `− 1` in every single
memory access ever performed. It is an arithmetic convenience that became a convention.

### A model answer

> "Indexing is O(1) because the position is computed, not searched for.
>
> An array is one contiguous block of memory divided into slots that are all exactly the same
> size, and the program holds the base address — where element 0 starts. So the address of
> element i is base plus i times the element size. If the array starts at address 1000 and
> holds 4-byte integers, element 0 is at 1000, element 7 is at 1028, and element 500,000 is
> at 2,001,000. That's one multiplication and one addition in every case.
>
> Nothing about that gets longer as the array grows. There's no traversal and no comparison,
> which is why arr[500000] and arr[0] cost the same — and I've measured that: two million
> reads at four positions ten million apart came out within half a percent of each other.
>
> Two things follow that I'd want to mention. First, it only works because every element is
> the same size, which is why a C array holds one type. Python gets around that by storing
> 8-byte references in the slots and letting the actual objects live on the heap — so
> indexing is still O(1), and the values aren't adjacent in memory, which costs you cache
> performance.
>
> Second, that same contiguity is what makes insertion expensive. Inserting at the front means
> every element after it now belongs at a different address, so every one of them physically
> moves. That's O(n), and it's not a separate fact — it's the bill for O(1) access. A linked
> list makes the opposite trade: O(1) insertion once you hold the node, O(n) access, because
> its pieces are scattered and there's no formula to compute.
>
> And in practice there's a constant hiding inside that O(1). A cache hit is about a
> nanosecond and a main-memory read is about eighty, and memory comes in 64-byte lines. So
> walking an array in order gets sixteen integers per fetch, while jumping around gets one.
> Same complexity, and I've seen a five-fold difference in wall-clock time from that alone."

That answer gives the formula with real addresses, cites a measurement, explains the
precondition, derives the cost of insertion from the same fact, and finishes on the constant
factor that Big-O deliberately ignores.

---

## 9. Recall card

1. **`address = base + i × element_size`.** One multiply, one add, for any `i`. That is why
   indexing is `O(1)`, and it is the whole answer.
2. **Three requirements: contiguous, equal-sized slots, known base address.** Break any one
   and the arithmetic fails — which is why an array holds one type.
3. **Counting starts at zero** because element 0's offset is zero, so the formula needs no
   adjustment.
4. **A Python list stores references, not values.** 8 bytes per slot, objects elsewhere.
   Still `O(1)` indexing, nine times the memory, worse locality. Use `array` or NumPy when
   that matters.
5. **Contiguity is a trade.** It buys `O(1)` access and charges `O(n)` for insertion in the
   middle. And a cache line is 64 bytes, so reading in order can be five times faster than
   reading the same elements out of order.
