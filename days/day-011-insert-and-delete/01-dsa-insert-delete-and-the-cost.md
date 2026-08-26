---
day: 11
track: dsa
title: "Insert, delete, and the cost of the middle"
phase: "Arrays"
status: written
---

# Day 011 · DSA — Insert, delete, and the cost of the middle

**After today you can:** You can say why adding to the end is cheap and adding to the middle is not.

**The interviewer asks it as:** *What is the cost of deleting an element from the middle of an array?*

---

## 1. What this is, and why they ask it

Deleting from position `i` of an array costs `n − i − 1` moves, because every element after
the hole has to slide back one slot to close it. Inserting at position `i` costs `n − i` moves
for the same reason, in the other direction.

So the cost is not a single number. It depends entirely on **where**. At the very end it is
zero moves and `O(1)`. At the very front it is every element and `O(n)`. In the middle it is
half of them, which is still `O(n)`.

Interviewers ask because it is the first question where "it depends" is the correct answer and
most candidates give a single number instead. It is also the question underneath a whole
family of later ones: why a queue needs a deque, why a linked list exists at all, why
removing k elements one at a time is quadratic and removing them in one pass is linear. Get
this right and a dozen later answers become obvious.

---

## 2. The story

The gas agency office on Station Road opens its complaints counter at ten. Vasanti gets there
at twenty past nine and there are already thirty-one people ahead of her.

The queue is orderly because of the floor. Somebody painted white circles on the concrete, a
metre apart, running from the counter to the door and then doubling back along the wall.
Sixty of them, numbered. You stand on a circle. There is no arguing about who was first,
because you can see it.

Vasanti is on circle 32.

At twenty to ten the man on circle 5 takes a phone call, listens, says something short and
walks out of the building. And then the whole queue moves. The man on 6 steps onto 5, the
woman on 7 steps onto 6, and it ripples all the way down past Vasanti to the last person on
43. Thirty-eight people pick up their bags and shuffle one circle forward. It takes about
forty seconds and everybody does it without being asked, because leaving a gap would be worse.

Twenty minutes later, a woman near the back — circle 40 — gives up and leaves. Three people
move. Nobody else even notices it happened.

And at half past ten the man at the very end walks off to buy a tea. Nobody moves at all. His
circle was the last one, so there was nothing behind it to close up.

Vasanti finds herself thinking about this because it is the third time she has been here in
two months. The cost is not the leaving. The cost is **everyone standing behind the person
who left**.

The other direction happens at a quarter to eleven, when a clerk comes out with an old man
who has a hospital appointment and puts him on circle 3. Now the shuffle runs the other way.
Everyone from circle 3 to circle 41 steps *back* one, so that a circle is free for him.
Thirty-nine people, and this time there is grumbling.

There is one more thing, and it is the reason nobody simply leaves a gap. At about eleven the
clerk comes to the door and shouts that only the first twenty will be seen before lunch.
Twenty from the front. If there were empty circles scattered through the queue, "the first
twenty" would mean nothing — you would have to walk down the line counting people rather than
just looking at circle 20 and drawing a line. The numbering only means something if there are
no holes in it.

By the time Vasanti gets to the counter it is ten past twelve and she is on circle 4.

---

## 3. The idea in plain English

The painted circles are an array, and the shuffling is the whole lesson.

### The cost is what is behind you

Removing the element at position `i` from an array of `n` elements leaves a hole. Everything
after it must move one slot back to close the hole. How many elements are after position `i`?

```
n - i - 1
```

Put numbers on it. In an array of 44 (the queue, positions 0 to 43):

| Remove from | Elements that move | Cost |
|---|---|---|
| position 4 (circle 5) | 39 | expensive |
| position 39 (circle 40) | 4 | cheap |
| position 43 (the last) | 0 | free |
| position 0 (the front) | 43 | worst |

**Same operation, four different costs, and the only thing that changed is where.**

Inserting is the mirror image. To insert at position `i`, everything from `i` onwards must
move one slot forward to make room:

```
n - i
```

### Why we call it O(n) anyway

Big-O reports the worst case unless told otherwise. The worst position is the front, which
moves all `n` elements. So:

- `items.insert(i, x)` → **`O(n)`**
- `items.pop(i)` or `del items[i]` → **`O(n)`**
- `items.append(x)` → **`O(1)`** amortised
- `items.pop()` → **`O(1)`**

The precise statement, which is better to say out loud, is: **`O(n − i)`, which is `O(n)` in
the worst case and `O(1)` at the end.** Say the precise version and then the summary. It shows
you know why.

### Why you cannot just leave the hole

This is the part of the story that people skip, and it is the reason the whole shuffle is
necessary.

An array's superpower is that position `i` is found by arithmetic —
`base + i × element_size`, from [day 009](../day-009-what-an-array-is/README.md). That formula
assumes **no gaps**. Leave one hole at position 5 and every element after it is at an address
one slot lower than its index says. The arithmetic now gives wrong answers, and `len()` no
longer tells you how many real elements there are.

"The first twenty" only means something if the numbering is unbroken.

There is a real technique that does leave holes — marking a slot as deleted instead of
removing it, called a **tombstone** — and databases and hash tables use it constantly. The
price is that you now need a separate way to know which slots are real, and you must
eventually **compact**: one pass that closes all the holes at once. That compaction is exactly
the write-pointer pattern from
[day 007](../day-007-space-complexity/README.md), and it is why the pattern matters.

### The trick when order does not matter

If you do not care about the order of the elements, deletion becomes `O(1)`:

```python
def remove_at_unordered(items: list[int], i: int) -> None:
    items[i] = items[-1]        # copy the last element over the hole
    items.pop()                 # then drop the last slot
```

One copy and one cheap pop. Nothing shuffles. It is the queue equivalent of telling the person
at the very back to come and stand on circle 5 — which would be outrageous in a queue and is
perfectly fine when the collection is a *set* of things rather than an *order* of things.

**Always ask whether order matters.** It is the difference between `O(n)` and `O(1)`, and it
is a question the problem statement often does not answer.

### Removing many: one pass, not many

Removing `k` elements one at a time costs `k × O(n)`, which for `k` proportional to `n` is
`O(n²)`. Removing them all in one pass costs `O(n)`.

```python
def remove_all(items: list[int], value: int) -> int:
    write = 0
    for read in range(len(items)):
        if items[read] != value:
            items[write] = items[read]
            write += 1
    return write                # items[:write] is the answer
```

One index reads every element; another marks where the next keeper goes. Nothing is ever
shifted more than once. This is the **write pointer**, it is `O(n)` time and `O(1)` space, and
it owns [day 015](../day-015-the-write-pointer/README.md).

### What to use instead when the middle really is the problem

If your workload genuinely inserts and deletes in the middle constantly, an array is the wrong
structure and no amount of care will fix it.

| Structure | Insert/delete in the middle | Index by position | Notes |
|---|---|---|---|
| Array / Python list | `O(n)` | `O(1)` | the default, and usually right |
| `collections.deque` | `O(n)` | `O(n)` | but `O(1)` at **both ends** |
| Linked list | `O(1)` *once you hold the node* | `O(n)` | [day 078](../day-078-nodes-and-links/README.md) |
| Balanced tree / sorted structure | `O(log n)` | `O(log n)` | ordered operations |

The linked list row has an important caveat in it. Insertion is `O(1)` **only if you already
have a reference to the node**. If you have to find position `i` first, that is `O(n)`, and
the total is no better than the array — with worse cache behaviour.
[Day 009](../day-009-what-an-array-is/README.md)'s locality argument is why arrays win in
practice far more often than the complexity table suggests.

---

## 4. The picture

Deleting from the middle, drawn move by move:

```
   before, n = 7, remove position 2
   index      0     1     2     3     4     5     6
           +-----+-----+-----+-----+-----+-----+-----+
           |  A  |  B  |  C  |  D  |  E  |  F  |  G  |
           +-----+-----+-----+-----+-----+-----+-----+
                         ^
                       remove

   the hole must be closed: everything after slides one left
           +-----+-----+-----+-----+-----+-----+-----+
           |  A  |  B  |  D  |  E  |  F  |  G  |     |
           +-----+-----+-----+-----+-----+-----+-----+
                          <---  <---  <---  <---
                          4 elements moved = n - i - 1 = 7 - 2 - 1
```

**What to notice:** four moves for one deletion, and the four are everything that was standing
behind the hole. That is the ripple down the queue.

The cost against position, drawn as a graph:

```
  moves
   6 |*
   5 | *
   4 |  *
   3 |   *
   2 |    *
   1 |     *
   0 |      *
     +-------------> position deleted
      0 1 2 3 4 5 6

   delete at 0 -> 6 moves     delete at 6 -> 0 moves
   O(n)                       O(1)
```

**What to notice:** it is a straight line, not a step. There is no single "cost of deletion" —
there is a cost per position, and Big-O quotes the left-hand end of this line.

Inserting, which is the same picture reversed:

```
   insert X at position 2, n = 6

           +-----+-----+-----+-----+-----+-----+-----+
           |  A  |  B  |  C  |  D  |  E  |  F  |     |
           +-----+-----+-----+-----+-----+-----+-----+
                         --->  --->  --->  --->
                    everything from position 2 moves right

           +-----+-----+-----+-----+-----+-----+-----+
           |  A  |  B  |     |  C  |  D  |  E  |  F  |
           +-----+-----+-----+-----+-----+-----+-----+
                         ^
                    now X drops in

   4 elements moved = n - i = 6 - 2
```

**What to notice:** the moves happen **back to front**. Copying `C` into slot 3 before moving
`D` out of slot 3 would destroy `D`. Direction matters when shifting in place, and getting it
backwards is a classic bug.

And the unordered trick, which avoids all of it:

```
   remove position 2, order does not matter

           +-----+-----+-----+-----+-----+-----+-----+
           |  A  |  B  |  C  |  D  |  E  |  F  |  G  |
           +-----+-----+-----+-----+-----+-----+-----+
                         ^                       |
                         +-----------------------+
                              copy G over C

           +-----+-----+-----+-----+-----+-----+
           |  A  |  B  |  G  |  D  |  E  |  F  |
           +-----+-----+-----+-----+-----+-----+

   1 move, whatever n is.  O(1).
```

**What to notice:** one arrow instead of four, and it would still be one arrow with a million
elements. The entire cost of ordering, made visible.

---

## 5. The code, built step by step

Measure the cost against position, because the whole point is that it varies.

Start with deletion at three different positions.

```python
import time

def time_delete_at(n: int, position: str) -> float:
    items = list(range(n))
    index = {"front": 0, "middle": n // 2, "end": n - 1}[position]
    start = time.perf_counter()
    for _ in range(20_000):
        items.insert(index, 0)      # put one back so the list length is stable
        del items[index]
    return time.perf_counter() - start
```

Inserting then deleting at the same position keeps the length constant, so every repetition
costs the same and the measurement is fair.

Now the write pointer, which is how you remove many things at once.

```python
def remove_all_write_pointer(items: list[int], value: int) -> int:
    write = 0
    for read in range(len(items)):
        if items[read] != value:
            items[write] = items[read]
            write += 1
    return write
```

`write` never overtakes `read`, so you are always writing into a slot already passed. `O(n)`
time and `O(1)` extra space, and it returns the new length rather than resizing — which is
exactly what LeetCode problems in this family ask for.

Compare it with the natural-looking version.

```python
def remove_all_repeated(items: list[int], value: int) -> None:
    while value in items:
        items.remove(value)          # O(n) to find + O(n) to shift, each time
```

`value in items` is `O(n)` and `items.remove(value)` is another `O(n)`. If half the list
matches, that is `n/2` repetitions of `O(n)` work — `O(n²)`.

Now the unordered trick.

```python
def remove_at_unordered(items: list[int], i: int) -> None:
    """O(1), at the cost of scrambling the order."""
    items[i] = items[-1]
    items.pop()
```

And the manual shift, so that the mechanism is not hidden inside a built-in.

```python
def delete_by_hand(items: list[int], i: int) -> int:
    """Exactly what del items[i] does. Returns how many elements moved."""
    n = len(items)
    for j in range(i, n - 1):
        items[j] = items[j + 1]     # slide each one back
    items.pop()                     # drop the now-duplicated last slot
    return n - i - 1
```

Note the direction: for deletion you copy **forwards**, from `j + 1` into `j`, starting at the
hole. For insertion you must copy **backwards**, or you overwrite values you still need.

Here is the complete program.

```python
"""Day 11 — the cost of insert and delete depends entirely on where."""

import time


def delete_by_hand(items: list[int], i: int) -> int:
    """What `del items[i]` really does. Returns the number of elements moved."""
    n = len(items)
    for j in range(i, n - 1):
        items[j] = items[j + 1]
    items.pop()
    return n - i - 1


def insert_by_hand(items: list[int], i: int, value: int) -> int:
    """What `items.insert(i, v)` really does. Note: shifts BACK to FRONT."""
    n = len(items)
    items.append(None)                      # make room at the end
    for j in range(n, i, -1):               # walk backwards, or you clobber data
        items[j] = items[j - 1]
    items[i] = value
    return n - i


def remove_at_unordered(items: list[int], i: int) -> None:
    """O(1) deletion when order does not matter."""
    items[i] = items[-1]
    items.pop()


def remove_all_write_pointer(items: list[int], value: int) -> int:
    """Remove every occurrence in ONE pass. O(n) time, O(1) space."""
    write = 0
    for read in range(len(items)):
        if items[read] != value:
            items[write] = items[read]
            write += 1
    return write


def remove_all_repeated(items: list[int], value: int) -> None:
    """The natural version. O(n^2)."""
    while value in items:
        items.remove(value)


def time_delete_at(n: int, index: int, repeats: int = 20_000) -> float:
    items = list(range(n))
    start = time.perf_counter()
    for _ in range(repeats):
        items.insert(index, 0)
        del items[index]
    return time.perf_counter() - start


if __name__ == "__main__":
    print("what actually moves")
    for i in (0, 2, 5, 6):
        row = ["A", "B", "C", "D", "E", "F", "G"]
        moved = delete_by_hand(row, i)
        print(f"  delete position {i} of 7 -> {moved} elements moved, result {row}")

    print()
    row = ["A", "B", "C", "D", "E", "F"]
    moved = insert_by_hand(row, 2, "X")
    print(f"  insert X at position 2 of 6 -> {moved} elements moved, result {row}")

    print(f"\ndeleting 20,000 times from a list of 100,000")
    n = 100_000
    for label, index in (("front  (i = 0)", 0),
                         ("middle (i = n/2)", n // 2),
                         ("end    (i = n-1)", n - 1)):
        secs = time_delete_at(n, index)
        print(f"  {label:<20} {secs:>8.4f} s")

    print("\nunordered deletion: one move, whatever n is")
    row = ["A", "B", "C", "D", "E", "F", "G"]
    remove_at_unordered(row, 2)
    print(f"  remove position 2, order not preserved -> {row}")

    print("\nremoving many: one pass vs one at a time")
    for size in (20_000, 40_000):
        data = [i % 4 for i in range(size)]          # a quarter of them are 0

        a = list(data)
        t0 = time.perf_counter(); remove_all_repeated(a, 0); slow = time.perf_counter() - t0

        b = list(data)
        t0 = time.perf_counter(); length = remove_all_write_pointer(b, 0)
        fast = time.perf_counter() - t0

        print(f"  n = {size:,}")
        print(f"    remove() in a loop  O(n^2) : {slow:>8.4f} s")
        print(f"    write pointer       O(n)   : {fast:>8.4f} s   -> {slow / fast:,.0f}x faster")
        print(f"    same answer? {a == b[:length]}")
```

This is exactly what it printed:

```
what actually moves
  delete position 0 of 7 -> 6 elements moved, result ['B', 'C', 'D', 'E', 'F', 'G']
  delete position 2 of 7 -> 4 elements moved, result ['A', 'B', 'D', 'E', 'F', 'G']
  delete position 5 of 7 -> 1 elements moved, result ['A', 'B', 'C', 'D', 'E', 'G']
  delete position 6 of 7 -> 0 elements moved, result ['A', 'B', 'C', 'D', 'E', 'F']

  insert X at position 2 of 6 -> 4 elements moved, result ['A', 'B', 'X', 'C', 'D', 'E', 'F']

deleting 20,000 times from a list of 100,000
  front  (i = 0)        13.7170 s
  middle (i = n/2)       6.8679 s
  end    (i = n-1)       0.0043 s

unordered deletion: one move, whatever n is
  remove position 2, order not preserved -> ['A', 'B', 'G', 'D', 'E', 'F']

removing many: one pass vs one at a time
  n = 20,000
    remove() in a loop  O(n^2) :   1.6118 s
    write pointer       O(n)   :   0.0027 s   -> 588x faster
    same answer? True
  n = 40,000
    remove() in a loop  O(n^2) :   6.6065 s
    write pointer       O(n)   :   0.0062 s   -> 1,073x faster
    same answer? True
```

**Read the timing block.** Front, middle and end are 13.7, 6.9 and 0.004 seconds. The middle
is almost exactly half the front, which is what `n − i − 1` predicts. The end is over three
thousand times faster than the front, because zero elements move.

**Read the last block, and notice the ratio between the two sizes.** Doubling `n` from 20,000
to 40,000 took the slow version from 1.61 s to 6.61 s — four times, which is the quadratic
signature from [day 003](../day-003-big-o-in-plain-english/README.md). The write pointer went
from 0.0027 to 0.0062 — roughly double, which is linear.

---

## 6. What it costs

**The exact counts**, which is what you should say before you say the Big-O:

| Operation | Elements moved | Complexity |
|---|---|---|
| `items.append(x)` | 0 | `O(1)` amortised |
| `items.pop()` | 0 | `O(1)` |
| `items.insert(i, x)` | `n − i` | `O(n − i)`, worst `O(n)` |
| `items.pop(i)` / `del items[i]` | `n − i − 1` | `O(n − i)`, worst `O(n)` |
| `items.insert(0, x)` | `n` | `O(n)` |
| `items.pop(0)` | `n − 1` | `O(n)` |
| `items.remove(x)` | `O(n)` to find + `n − i − 1` to shift | `O(n)` |
| Unordered delete (swap with last) | 1 | `O(1)` |
| Remove all matches, write pointer | `n` total | `O(n)` |
| Remove all matches, one at a time | up to `n²/2` | `O(n²)` |

**The arithmetic on the quadratic**, because this is the one that shows up in real code.
Removing 5,000 elements one at a time from a list of 20,000:

```
each remove() : O(n) to find + O(n) to shift, so about 20,000 operations
5,000 removes : 5,000 x 20,000 = 100,000,000 element operations
```

One hundred million, for a job that needs twenty thousand. The write pointer does:

```
one pass  : 20,000 reads + at most 20,000 writes = 40,000 operations
```

**A factor of 2,500 in operation count**, and you measured 588× and 1,073× in wall-clock,
because the built-in `remove` runs at C speed and the Python loop does not. The Big-O gap is
real; the constant partly hides it, and the gap widens as `n` grows.

**What "amortised O(1)" means for append**, restated because it belongs next to these numbers.
From [day 005](../day-005-python-lists-and-tuples/README.md): the list over-allocates by about
12.5%, so most appends land in spare capacity and occasionally one triggers a full copy.
Building a list of a million by appending copies about 1.9 million elements in total, so
**about two extra operations per append**, averaged.

**Space.** All of these are `O(1)` extra space — the shifting happens inside the existing
block. The one exception is anything that builds a new list:

```
[x for x in items if x != value]   ->  O(n) extra space, O(n) time
write pointer                      ->  O(1) extra space, O(n) time
```

Both are `O(n)` time. Choose by whether you may modify the input, which is a question for the
interviewer.

**When the middle really is your workload.** If you insert or delete in the middle `m` times
on an array of `n`:

```
array       : m x O(n)      = O(m x n)
linked list : m x O(1)      = O(m)      -- but only if you already hold the node
```

The caveat is doing real work in that sentence. Finding position `i` in a linked list is
`O(n)`, so unless you got the node from somewhere else — an iterator you are already holding,
or a hash map pointing at nodes, which is exactly how an LRU cache works
([day 076](../day-076-lru-cache/README.md)) — the linked list is not faster, and it has worse
cache behaviour on top.

---

## 7. The traps

### Trap one: removing in a loop, forwards

The classic. You want to remove every negative number:

```python
items = [1, -2, -3, 4, -5, 6]
for i in range(len(items)):
    if items[i] < 0:
        del items[i]
print(items)
```

```
Traceback (most recent call last):
  File "d11.py", line 3, in <module>
    if items[i] < 0:
       ~~~~~^^^
IndexError: list index out of range
```

Two separate bugs in three lines. The list shrinks while `range(len(items))` was computed once
at the start, so `i` eventually exceeds the new length — that is the `IndexError`. And even
before it crashes, deleting at `i` shifts the next element **into** position `i`, which the
loop then skips over by advancing.

Watch it happen: `i = 1` deletes `−2`, so the list becomes `[1, -3, 4, -5, 6]` and `−3` is now
at position 1. The loop moves to `i = 2`, which is `4`. `−3` is never examined.

The `remove`-based version fails differently and just as informatively:

```python
items = [1, -2, 4]
for x in items:
    if x < 0:
        items.remove(x)
        items.remove(x)      # a second remove, by mistake
```

```
Traceback (most recent call last):
  File "d11.py", line 5, in <module>
    items.remove(x)
    ~~~~~~~~~~~~^^^
ValueError: list.remove(x): x not in list
```

`ValueError` rather than `IndexError`, because `remove` searches by value and there is no
longer a match. The message names the method and the reason exactly.

**The three correct fixes**, in the order a reviewer would prefer them:

```python
items = [x for x in items if x >= 0]          # new list, O(n) time, O(n) space
```

```python
write = 0                                      # write pointer: O(n) time, O(1) space
for read in range(len(items)):
    if items[read] >= 0:
        items[write] = items[read]
        write += 1
del items[write:]
```

```python
for i in range(len(items) - 1, -1, -1):        # backwards: correct, but O(n^2)
    if items[i] < 0:
        del items[i]
```

The backward loop is correct because deleting at `i` only shifts elements after `i`, which are
already visited. It is still `O(n²)` because each `del` shifts. Use it when the list is small
and clarity matters; use the write pointer when it is not.

### Trap two: shifting in the wrong direction

This one produces no error at all. It produces a list full of duplicates.

```python
def insert_by_hand(items: list[str], i: int, value: str) -> None:
    items.append(None)
    for j in range(i, len(items) - 1):       # forwards — wrong direction
        items[j + 1] = items[j]
    items[i] = value

row = ["A", "B", "C", "D", "E"]
insert_by_hand(row, 1, "X")
print(row)
```

```
['A', 'X', 'B', 'B', 'B', 'B']
```

`C`, `D` and `E` are gone, replaced by copies of `B`. The reason is the order of the copies.
Copying `items[1]` into `items[2]` destroys `C` before anything has read it. Then `items[2]`
— which is now `B` — gets copied into `items[3]`, destroying `D`. Each step propagates the same
value forward.

**When you shift right, you must copy from the back.** When you shift left — which is what
deletion does — you must copy from the front. The rule is: **start at the end you are moving
towards**.

```python
    for j in range(len(items) - 1, i, -1):    # backwards — correct
        items[j] = items[j - 1]
```

This is the same failure mode as an overlapping `memcpy` in C, and it is the reason
`memmove` exists as a separate function. It comes back on
[day 084](../day-084-merging-and-sorting-lists/README.md), where merging two sorted arrays in
place must fill from the end for exactly this reason.

---

## 8. In the interview

### How it gets asked

- *"What's the cost of deleting an element from the middle of an array?"* — the direct
  version. "It depends where" is the start of the right answer, not a dodge.
- *"Why is appending O(1) but inserting at the front O(n)?"* — the same fact from the other
  side.
- *"Can you delete from an array in O(1)?"* — the unordered-trick question. The answer is yes,
  with a condition.
- *"Remove all occurrences of a value in place."* — the write-pointer question, and the naive
  answer is quadratic.

### What to say out loud, in the first ninety seconds

1. **Give the exact count first.** *"It's n minus i minus 1 moves, where i is the position —
   because everything after the hole has to slide back one slot to close it."*
2. **Give the range.** *"So deleting the last element is zero moves and O(1). Deleting the
   first is n minus 1 moves and O(n). The middle is n over 2, which is still O(n)."*
3. **Say why the shifting is unavoidable.** *"You can't leave the hole, because an array finds
   position i by arithmetic — base plus i times element size — and that only works if the
   slots are unbroken."*
4. **Offer the O(1) version with its condition.** *"If the order doesn't matter, I can do it in
   O(1): copy the last element over the hole and pop the end. One move, whatever n is. That's
   only valid if it's a collection rather than a sequence."*
5. **Pre-empt the multiple-deletion question.** *"And if I'm removing many elements, I'd do it
   in one pass with a write pointer rather than calling delete repeatedly — that's O(n)
   instead of O(n squared)."*
6. **Name the structural alternative.** *"If middle insertion were the dominant operation, an
   array is the wrong structure — that's what a linked list buys, at the cost of O(n) indexing
   and much worse cache locality."*

Steps 4 and 5 are what turn a definition into a design answer.

### The follow-ups

**"Why can't you just mark it as deleted and leave a hole?"**
You can, and real systems do — it is called a tombstone, and hash tables and databases rely on
it. The cost is that you have broken the array's core property: position no longer maps
directly to index, so `len` no longer tells you how many real elements there are, and any code
that indexes into it needs a way to skip holes. So you defer the shifting and eventually pay
it all at once in a compaction pass. That is often the right trade when deletions are frequent
and reads can tolerate the extra check — a batched `O(n)` compaction beats `k` separate `O(n)`
shifts. But it is a trade, not a free win.

**"Can you delete from an array in O(1)?"**
Yes, if order doesn't matter: copy the last element into the slot being deleted and pop the
end. One assignment and one `O(1)` pop, regardless of size. The condition is the whole answer
— it works for a set of things and destroys a sequence of things. I'd ask explicitly whether
order matters before using it, because a problem statement often doesn't say, and the
difference between `O(n)` and `O(1)` is worth one question.

**"You called remove in a loop. What's the complexity?"**
`O(n²)`. Each `remove` is `O(n)` to find the value plus `O(n)` to shift what's behind it, and
doing that a number of times proportional to `n` squares it. I'd replace it with a single pass
using a write pointer: one index reads everything, another marks where the next kept element
goes, so nothing moves more than once. That's `O(n)` time and `O(1)` extra space. If I'm
allowed to allocate, a list comprehension is `O(n)` time and `O(n)` space and reads better.

**"When would you use a linked list instead?"**
When insertions and deletions in the middle dominate **and** I already hold a reference to the
node, so I'm not paying `O(n)` to find it. In practice that means the linked list is part of a
larger structure — an LRU cache where a hash map points at nodes, or an iterator I'm already
walking. If I'd have to search for the position first, the linked list is `O(n)` too, with
worse cache behaviour, because its nodes are scattered rather than contiguous. That's why
arrays beat linked lists in real benchmarks far more often than the complexity table suggests.

### A model answer

> "It depends on the position, and I'd give the exact count rather than just the Big-O.
>
> Deleting at position i costs n minus i minus 1 element moves, because everything after the
> hole has to slide one slot back to close it. So in a list of 44, deleting position 4 moves
> 39 elements, deleting position 39 moves 4, and deleting the last element moves nothing at
> all. Worst case is the front at n minus 1 moves, so we call it O(n) — but at the end it's
> genuinely O(1), and it's worth saying both.
>
> The reason the shifting is unavoidable is the array's layout. Position i is found by
> arithmetic — base address plus i times the element size — and that only works if the slots
> are contiguous with no gaps. Leave a hole and every subsequent element is at an address that
> disagrees with its index. So it's the same contiguity that makes indexing O(1) that makes
> deletion O(n). They're two sides of one design decision.
>
> There is an O(1) version if order doesn't matter: copy the last element over the slot being
> deleted and then pop the end. One move regardless of size. I'd ask whether order matters
> before using it, because for a collection it's free and for a sequence it's a bug.
>
> And if I'm deleting many elements rather than one, I wouldn't call delete repeatedly —
> that's O(n) each and O(n²) overall. I'd do a single pass with a write pointer: one index
> reads every element, another marks where the next keeper goes, so nothing moves twice. O(n)
> time, O(1) extra space. I've measured that at nearly 600× faster on 20,000 elements, and the
> gap widens as n grows because one is quadratic and one is linear.
>
> If middle insertion were genuinely the dominant operation in the workload, I'd change the
> structure rather than the code — a linked list gives O(1) insertion, but only once you hold
> the node, and it costs you O(1) indexing and cache locality. So I'd want to see the access
> pattern before making that trade."

---

## 9. Recall card

1. **Delete at `i` costs `n − i − 1` moves. Insert at `i` costs `n − i`.** The cost is
   everything standing behind the position.
2. **The end is free, the front is `O(n)`.** `append` and `pop()` move nothing; `insert(0, x)`
   and `pop(0)` move everything.
3. **The holes cannot stay** — indexing is `base + i × size`, which needs unbroken slots. That
   is the same property that makes indexing `O(1)`.
4. **If order does not matter, deletion is `O(1)`:** copy the last element over the hole and
   pop the end. Always ask whether order matters.
5. **Removing many is one pass, not many deletes.** Write pointer: `O(n)` and `O(1)` space
   against `O(n²)`. And when shifting in place, **start at the end you are moving towards**.
