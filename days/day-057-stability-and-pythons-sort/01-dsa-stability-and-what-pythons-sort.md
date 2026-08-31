---
day: 57
track: dsa
title: "Stability, and what Python's sort actually does"
phase: "Sorting"
status: written
---

# Day 057 · DSA — Stability, and what Python's sort actually does

**After today you can:** You know what stable means, why it matters, and roughly how Timsort works.

**The interviewer asks it as:** *Is Python's sort stable? Why do you care?*

---

## 1. What this is, and why they ask it

A sort is **stable** if two elements that compare equal come out in the same order they went in. That
is the whole definition, and it sounds like a detail until you need to sort by two things at once —
at which point it is the only thing holding your answer together. Python's sort is stable, and it is
guaranteed in the language documentation rather than being an accident of the implementation.

They ask it because it is a small question with a large answer. "Is it stable" takes one word. "Why
do you care" is where the interview happens, and the answer is multi-key sorting: sort by name, then
sort by department, and only a stable sort leaves the names in order within each department. Get it
wrong and nothing raises — you simply get an ordering you cannot explain, in production, on data
somebody is looking at. The second half of today is what Python actually runs. **Timsort** is not a
textbook algorithm; it was written for Python in 2002 and then adopted by Java, Android, V8 and Rust,
and interviewers who have heard of it like asking about it. Knowing that it finds existing runs,
insertion-sorts short ones, and merges the rest is a real answer to a real question, and it explains
why `sorted()` is fast on data that is almost in order.

---

## 2. The story

Vasanthi has worked the counter at a government office in Belgaum for eleven years, and the queue
outside starts before she does. On a pension day there are forty people on the bench by half past
eight, and everybody knows exactly who came before them and who came after. That is the one thing a
queue is for.

At about ten o'clock the officer came out and said that from now on people bringing the yellow form
should be dealt with before people bringing the white form, because the yellow ones needed a
signature from him and he was leaving at noon.

Now there were two ways to do that, and Vasanthi has seen both.

The first way, which is what happened the day a new clerk tried it, was to stand up and announce it.
Yellow forms come to the front. Fourteen people got up at once and went forward, and where they ended
up depended entirely on who was quickest off the bench and who was sitting nearest the door. A man
who had come at half past eight ended up sixth among the yellow forms, behind a woman who had walked
in twenty minutes earlier. He said so. Loudly. And he was right, and there was no possible answer,
because nobody could reconstruct who had arrived when — the bench had been the record, and standing
up had destroyed it.

The second way is what Vasanthi does, and it takes slightly longer and has never once caused an
argument.

She walks the bench from the front, in order, and taps each yellow form on the shoulder as she
reaches them, and they get up one at a time and stand behind whoever she tapped before. She does not
skip anybody and she does not go back. When she reaches the end of the bench, she has fourteen people
in a new line, and the man who came at half past eight is first among them, because he was first on
the bench.

Then the white forms follow, in exactly the same order they were sitting in.

Nobody has to be told any of this. They can all see it. The bench said who came first, the new line
still says who came first, and the only thing that changed is the thing the officer asked to change.

---

## 3. The idea in plain English

Vasanthi walking the bench in order is a stable sort. The new clerk shouting is an unstable one. And
the man who arrived at half past eight is the equal element whose original position was thrown away.

### The definition

> **A sort is stable if elements that compare equal keep their original relative order.**

Note the words *compare equal*. Stability says nothing about elements with different keys — those get
reordered, obviously, that is what sorting is. It is only about ties.

```
 input     ("Asha", 34)  ("Bala", 12)  ("Chitra", 34)  ("Devi", 7)

 sort by AGE, stable:
           ("Devi", 7)   ("Bala", 12)  ("Asha", 34)   ("Chitra", 34)
                                        ^^^^^^^^^^^^   ^^^^^^^^^^^^^^
                            Asha before Chitra -- as in the input

 sort by AGE, unstable -- also a correct sort by age:
           ("Devi", 7)   ("Bala", 12)  ("Chitra", 34) ("Asha", 34)
                                        ^^^^^^^^^^^^^  ^^^^^^^^^^^^
                            Chitra first now. No error. Just different.
```

Both outputs are correctly sorted by age. Only one of them preserved information you had.

### Why anybody cares: sorting by two things

This is the reason stability exists, and it is the answer to give.

You want employees sorted by department, and within each department by name. There are two ways.

**One: a tuple key.** One pass, one sort:

```python
people.sort(key=lambda p: (p.department, p.name))
```

This works with any sort, stable or not, because the key makes the comparison total — no two people
compare equal unless both fields match. Prefer this when you can.

**Two: two passes, which is where stability is compulsory.**

```python
people.sort(key=lambda p: p.name)          # the LESS significant key first
people.sort(key=lambda p: p.department)    # the MORE significant key second
```

Read that order carefully, because it is backwards from how people expect. Sort by the *least*
significant key first. Then the final sort by department only reorders people in different
departments; within a department everyone compares equal, so a stable sort leaves them exactly as the
first pass arranged them — in name order.

With an unstable sort, the second pass is entitled to shuffle people inside a department, and the
first pass's work is gone. **No exception, no warning, just an order nobody can explain.**

You need the two-pass version whenever you cannot express the ordering as one key: when a field must
be sorted descending and it is a string, when the keys come from expensive lookups you do not want in
one tuple, or when the second sort happens somewhere else entirely — in a different function, or on
data that arrived already sorted.

### The other reason: the input order means something

Sometimes the original order is itself information. Log lines arrive in time order; sort them by
severity and a stable sort keeps each severity group in time order for free. Search results arrive by
relevance; sort by price and equally-priced results stay in relevance order. Rows come out of a
database in insertion order; sort by status and equal-status rows stay in insertion order.

In every one of those, an unstable sort silently throws away an ordering you were relying on.

### Which sorts are stable

| Sort | Stable? | Why |
|---|---|---|
| Insertion sort | **Yes** | The walk stops at the first element that is not *strictly* greater, so nothing passes an equal. |
| Bubble sort | **Yes** | It only swaps when the left element is strictly greater. |
| Merge sort | **Yes** | The merge takes from the left list when the fronts are equal. |
| Counting sort | **Yes**, if written correctly | Placing backwards into end positions preserves order. |
| Radix sort | **Yes**, and it *depends* on it | It is stability applied `d` times. |
| **Selection sort** | **No** | It swaps across long distances, throwing an equal element past its twin. |
| **Quicksort** | **No** | Partitioning swaps across long distances, for the same reason. |
| **Heapsort** | **No** | The heap reorders equal elements arbitrarily. |

The pattern is worth naming: **sorts that only ever swap neighbours are stable; sorts that move
elements long distances are not.** That single sentence lets you work out the answer for a sort you
have never seen.

The counter-example for selection sort takes three elements and it is worth memorising:

```
 input   [ 2a , 2b , 1 ]        (2a and 2b are distinct records that compare equal)

 pass 1: the smallest is 1, at position 2. Swap positions 0 and 2:
         [ 1 , 2b , 2a ]
                    ^^^ 2a has been thrown behind 2b

 result  [ 1 , 2b , 2a ]        the twos have swapped order
```

### What Python actually does

`list.sort()` and `sorted()` are **guaranteed stable**. That is documented behaviour, not an
implementation accident, so you may rely on it.

Two details that get asked and that people get wrong:

**`reverse=True` does not reverse ties.** It is not the same as sorting and then reversing the list.
Equal elements keep their original order in both directions:

```python
people = [("Asha", 34), ("Bala", 12), ("Chitra", 34)]
sorted(people, key=lambda p: p[1], reverse=True)
# [('Asha', 34), ('Chitra', 34), ('Bala', 12)]     <- Asha still before Chitra

list(reversed(sorted(people, key=lambda p: p[1])))
# [('Chitra', 34), ('Asha', 34), ('Bala', 12)]     <- ties reversed. Different!
```

**`min` and `max` return the first of the equals.** Which is stability applied to a single answer,
and it matters when you are picking a winner by score.

### Timsort, in the amount of detail an interview wants

Python's sort is **Timsort**, written by Tim Peters in 2002. It is a merge sort with three practical
additions, and it is now the standard sort in Java (for objects), Android, V8, Swift and Rust.

**One: it looks for runs that are already ordered.** It walks the list and finds a maximal stretch
that is already ascending, or strictly descending — and a descending run is reversed in place, which
is cheap and keeps stability because the reversal is only applied to strictly decreasing elements,
where there are no ties to disturb.

**Two: short runs are extended with binary insertion sort.** If a natural run is shorter than
`minrun` — a computed value between 32 and 64 — Timsort grabs the next few elements and
insertion-sorts them into it. That is [day 052](../day-052-quadratic-sorts/README.md)'s insertion
sort, used exactly where it is genuinely the fastest thing available.

**Three: the runs are merged, with galloping.** Runs are pushed onto a stack and merged under rules
that keep their sizes balanced. When merging, if one run keeps winning, Timsort switches to
**galloping mode** — it binary-searches ahead to find how many elements it can take in one go instead
of comparing one at a time. On data where one run is entirely smaller than the other, that turns `n`
comparisons into `log n`.

The results:

```
 already sorted        : ONE run found. O(n). No merging at all.
 reverse sorted        : one descending run, reversed. O(n).
 random                : O(n log n)
 nearly sorted         : close to O(n) -- a few long runs to merge
 two sorted lists
   concatenated        : ~O(n), thanks to galloping
```

And two properties: it is **stable**, and it uses `O(n)` extra space in the worst case, like merge
sort. It is written in C, so its constant factor is far below anything you write in Python.

---

## 4. The picture

The bench, and the two ways of pulling the yellow forms out:

```
 the queue, by arrival time (this order is INFORMATION)

   pos   1     2     3     4     5     6     7     8
        [Y]   [W]   [Y]   [W]   [W]   [Y]   [W]   [Y]
       8:30  8:35  8:40  8:50  9:05  9:10  9:20  9:40


 STABLE — walk the bench in order, tap each Y as you reach it

        [Y]   [Y]   [Y]   [Y]  |  [W]   [W]   [W]   [W]
       8:30  8:40  9:10  9:40    8:35  8:50  9:05  9:20
        ^^^^ arrival order preserved inside BOTH groups


 UNSTABLE — announce it and let people move

        [Y]   [Y]   [Y]   [Y]  |  [W]   [W]   [W]   [W]
       9:10  8:30  9:40  8:40    9:05  8:35  9:20  8:50
        ^^^^ correctly grouped, and the arrival order is GONE
```

**What to notice:** both results are correct sorts by form colour. An automated check on the form
colour passes for both. The difference is invisible unless you knew what the original order meant —
which is exactly why the bug is dangerous.

Two-pass sorting, and the moment stability does the work:

```
 input                    (Ravi, Sales)  (Anil, HR)  (Bina, Sales)  (Chandra, HR)

 pass 1 -- by NAME (the LESS significant key)
                          (Anil, HR)  (Bina, Sales)  (Chandra, HR)  (Ravi, Sales)

 pass 2 -- by DEPARTMENT (the MORE significant key)
   HR:    Anil and Chandra compare EQUAL here.
          A stable sort must not move them relative to each other.
   Sales: Bina and Ravi compare EQUAL here. Same.

                          (Anil, HR)  (Chandra, HR)  (Bina, Sales)  (Ravi, Sales)
                           ^^^^  ^^^^^^^                ^^^^  ^^^^
                           name order survived inside each department


 with an UNSTABLE pass 2, this is also allowed:
                          (Chandra, HR)  (Anil, HR)  (Ravi, Sales)  (Bina, Sales)
                           -- correctly sorted by department, names scrambled,
                              and pass 1 was a complete waste of time
```

**What to notice:** the second pass is where stability is spent, not the first. And the *order* of
the passes is least-significant-first, which is backwards from how it reads in English ("sort by
department, then by name").

What Timsort does to a real list:

```
 input:  [ 5, 7, 9, 2, 4, 1, 1, 3, 8, 6, 6, 6, 6, 6, 0 ]

 step 1 — find natural runs
          [ 5, 7, 9 ]          ascending run
          [ 2, 4 ]             ascending run
          [ 1, 1, 3, 8 ]       ascending run
          [ 6, 6, 6, 6, 6 ]    ascending (equal counts as ascending — stability!)
          [ 0 ]                trailing single

 step 2 — any run shorter than minrun (32-64) is EXTENDED by binary
          insertion sort until it reaches minrun, or the list ends.
          For a real list of thousands, this is where insertion sort earns its place.

 step 3 — push runs on a stack, merge under size rules, galloping when
          one side keeps winning.

 the point: a list that is already sorted is ONE run. Zero merges. O(n).
```

**What to notice:** `[6, 6, 6, 6, 6]` counts as an ascending run. That is deliberate — treating
equals as ascending is what keeps Timsort stable, and treating a *strictly* descending stretch as a
run is what makes reversing it safe.

---

## 5. The code, built step by step

### Proving stability to yourself

The test that catches every stability bug is four lines, and you should write it every time you
implement a sort:

```python
def is_stable(sort_fn) -> bool:
    """Sort (key, tag) pairs by key and check the tags stayed in order."""
    data = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    out = sort_fn(data)
    ones = [tag for key, tag in out if key == 1]
    twos = [tag for key, tag in out if key == 2]
    return ones == ["a", "c", "e"] and twos == ["b", "d"]
```

The key is the number; the tag records where the element came from. If the tags come back in their
original relative order within each key group, the sort is stable. This catches the one-character
`<` / `<=` bugs from [day 052](../day-052-quadratic-sorts/README.md) and
[day 053](../day-053-merge-sort/README.md).

### Sorting by two keys, both ways

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
    name: str
    department: str
    age: int
```

```python
def by_tuple_key(people: list[Person]) -> list[Person]:
    """One pass. Works with any sort, stable or not. Prefer this."""
    return sorted(people, key=lambda p: (p.department, p.name))
```

```python
def by_two_passes(people: list[Person]) -> list[Person]:
    """Two passes. Correct ONLY because Python's sort is stable.

    Sort by the LEAST significant key first.
    """
    out = sorted(people, key=lambda p: p.name)          # less significant
    return sorted(out, key=lambda p: p.department)      # more significant
```

Both produce the same answer. The tuple version is what you write when you control both keys in one
place; the two-pass version is what you need when you do not.

### Mixed directions, which is where tuple keys run out

Sort by department ascending and age descending:

```python
sorted(people, key=lambda p: (p.department, -p.age))       # works: age is a number
```

The minus sign reverses one field inside a tuple key. But it only works on numbers — you cannot
negate a string:

```python
sorted(people, key=lambda p: (p.department, -p.name))
```

```
Traceback (most recent call last):
  File "day57.py", line 1, in <module>
    sorted(people, key=lambda p: (p.department, -p.name))
                                                ^^^^^^^
TypeError: bad operand type for unary -: 'str'
```

For a descending string field, use two passes and stability:

```python
def by_dept_then_name_descending(people: list[Person]) -> list[Person]:
    out = sorted(people, key=lambda p: p.name, reverse=True)   # least significant, reversed
    return sorted(out, key=lambda p: p.department)             # most significant
```

This is the standard answer to "sort by score descending, then by name ascending" when one of them is
a string, and it is [day 058](../day-058-custom-comparators/README.md)'s main subject.

### Where `reverse=True` differs from reversing

```python
def reverse_flag_vs_reversed(people: list[Person]) -> None:
    a = sorted(people, key=lambda p: p.age, reverse=True)
    b = list(reversed(sorted(people, key=lambda p: p.age)))
    # a and b agree on the ordering by age
    # they DISAGREE on the order of people with the same age
```

`reverse=True` sorts descending while still preserving the original order of ties. Reversing a sorted
list flips the ties too. Interviewers ask this specifically because it looks like it should not
matter.

### A stable sort you write yourself

If you are ever asked to make an unstable sort stable, the trick is to break every tie with the
original position:

```python
def stable_with_any_sort(items: list, key) -> list:
    """Make ANY sort stable by attaching the original position as a tie-breaker."""
    decorated = [(key(item), i, item) for i, item in enumerate(items)]
    decorated.sort()                      # ties on key(item) are broken by i
    return [item for _, _, item in decorated]
```

Now no two entries compare equal, so no sort has any freedom to reorder them. This is called the
**decorate-sort-undecorate** pattern, and it is what Python did before `key=` existed. It costs
`O(n)` extra space and it is the correct answer to "how would you get stability out of a sort that
does not have it" — which is a real question when you are using C++'s `std::sort` or Java's
`Arrays.sort` on primitives.

### The complete file

```python
"""Stability: what it means, why two-pass sorting depends on it, and what Python runs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    name: str
    department: str
    age: int


def is_stable(sort_fn) -> bool:
    """The four-line test that catches every stability bug."""
    data = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    out = sort_fn(list(data))
    ones = [tag for key, tag in out if key == 1]
    twos = [tag for key, tag in out if key == 2]
    return ones == ["a", "c", "e"] and twos == ["b", "d"]


def merge_sort(nums: list) -> list:
    """Stable: the merge takes from the LEFT on a tie."""
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left, right = merge_sort(nums[:mid]), merge_sort(nums[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                 # <= keeps it stable; < does not
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def selection_sort(nums: list) -> list:
    """NOT stable: it swaps across long distances."""
    nums = list(nums)
    for start in range(len(nums) - 1):
        smallest = start
        for i in range(start + 1, len(nums)):
            if nums[i] < nums[smallest]:
                smallest = i
        nums[start], nums[smallest] = nums[smallest], nums[start]
    return nums


def stable_with_any_sort(items: list, key) -> list:
    """Decorate-sort-undecorate: make ANY sort stable by breaking ties on position."""
    decorated = [(key(item), i, item) for i, item in enumerate(items)]
    decorated.sort()
    return [item for _, _, item in decorated]


def by_tuple_key(people: list[Person]) -> list[Person]:
    """One pass. Works with any sort. The default choice."""
    return sorted(people, key=lambda p: (p.department, p.name))


def by_two_passes(people: list[Person]) -> list[Person]:
    """Two passes, LEAST significant key first. Correct only because sort is stable."""
    out = sorted(people, key=lambda p: p.name)
    return sorted(out, key=lambda p: p.department)


def dept_then_name_descending(people: list[Person]) -> list[Person]:
    """Mixed directions on a string field: tuple keys cannot do this."""
    out = sorted(people, key=lambda p: p.name, reverse=True)
    return sorted(out, key=lambda p: p.department)


if __name__ == "__main__":
    print(is_stable(merge_sort))          # True
    print(is_stable(selection_sort))      # False
    print(is_stable(sorted))              # True  -- guaranteed by the language

    print(selection_sort([(2, "a"), (2, "b"), (1, "c")]))
    # [(1, 'c'), (2, 'b'), (2, 'a')]   <- a and b swapped. The classic counter-example.

    print(stable_with_any_sort([(2, "a"), (2, "b"), (1, "c")], key=lambda p: p[0]))
    # [(1, 'c'), (2, 'a'), (2, 'b')]   <- the original position breaks the tie

    staff = [
        Person("Ravi", "Sales", 34),
        Person("Anil", "HR", 28),
        Person("Bina", "Sales", 41),
        Person("Chandra", "HR", 28),
    ]
    for p in by_tuple_key(staff):
        print(p.department, p.name)
    # HR Anil / HR Chandra / Sales Bina / Sales Ravi
    assert by_tuple_key(staff) == by_two_passes(staff)

    # reverse=True does NOT reverse ties
    ages = [("Asha", 34), ("Bala", 12), ("Chitra", 34)]
    print(sorted(ages, key=lambda p: p[1], reverse=True))
    # [('Asha', 34), ('Chitra', 34), ('Bala', 12)]
    print(list(reversed(sorted(ages, key=lambda p: p[1]))))
    # [('Chitra', 34), ('Asha', 34), ('Bala', 12)]     <- different!

    # min and max return the FIRST of the equals
    print(max(ages, key=lambda p: p[1]))       # ('Asha', 34)

    # Timsort's adaptivity, visible on the clock
    import random, time
    n = 2_000_000
    ordered = list(range(n))
    shuffled = ordered[:]
    random.shuffle(shuffled)
    for label, data in (("already sorted", ordered), ("random", shuffled)):
        copy = data[:]
        start = time.perf_counter()
        copy.sort()
        print(f"{label:16} {time.perf_counter() - start:.3f}s")
    # already sorted   ~0.02s   <- one run found, no merging
    # random           ~1.10s
```

---

## 6. What it costs

### Stability is free in merge sort and impossible in quicksort

```
 merge sort  : the merge already compares left[i] with right[j].
               Using <= instead of < costs NOTHING and buys stability.

 quicksort   : partitioning swaps elements across arbitrary distances.
               There is no cheap fix. A stable quicksort needs O(n) extra
               space to build the two sides separately -- at which point
               you have written merge sort with a worse pivot.
```

That asymmetry is the answer to "can you make quicksort stable?" — yes, by giving up the property
that made you choose quicksort.

### Making an unstable sort stable, priced

```
 decorate-sort-undecorate on n = 1,000,000:

   build the decorated list  : 1,000,000 tuple allocations
   extra memory              : ~3 x 8 bytes per element = 24 MB
   sort                      : same n log n, but comparing tuples is
                               ~1.5x slower than comparing bare numbers
   undecorate                : 1,000,000 more allocations

 total: roughly 2x the time and 3x the memory, to buy stability.
```

Worth knowing, because it is the honest cost of "just add the index as a tie-breaker".

### Timsort's adaptivity, measured

```
 n = 2,000,000 integers, Python's list.sort()

 already sorted        ~0.02 s      one run, zero merges       -> O(n)
 reverse sorted        ~0.03 s      one descending run, reversed -> O(n)
 nearly sorted
   (1000 out of place) ~0.09 s      a few long runs to merge
 random                ~1.10 s      full n log n
 all identical         ~0.02 s      equals count as ascending  -> ONE run

 -> 55x faster on sorted input than on random input, for the same n.
```

That is not a micro-optimisation. Real data is very often nearly sorted — log files, database rows in
insertion order, a list that was sorted and then had ten items appended — and Timsort makes those
cases linear.

### Galloping, priced

```
 merging [1..1000] with [2000..3000]:

 plain merge : compare 1 with 2000, take 1.  compare 2 with 2000, take 2.  ...
               1,000 comparisons to discover that ALL of the left run
               comes first.

 galloping   : after 7 consecutive wins, binary search ahead:
               "how many of the left run are below 2000?" -> ~10 comparisons
               then copy the block in one memmove.

 1,000 comparisons -> ~17. And this pattern (two sorted lists concatenated)
 is extremely common in real data.
```

### The one-character bugs, priced

```
 merge sort with < instead of <=       : still O(n log n), still correct order,
                                         silently unstable
 insertion sort with >= instead of >   : same
 counting sort placed forwards         : same

 cost of the bug: 0 failing tests, and a wrong two-pass sort in production.
 cost of the fix: 1 character, plus the 4-line is_stable test.
```

---

## 7. The traps

### The near-miss: two-pass sorting with an unstable sort

```python
def sort_broken(people):
    out = selection_sort_by(people, key=lambda p: p.name)         # unstable
    return selection_sort_by(out, key=lambda p: p.department)

staff = [Person("Ravi", "Sales", 34), Person("Anil", "HR", 28),
         Person("Bina", "Sales", 41), Person("Chandra", "HR", 28)]
for p in sort_broken(staff):
    print(p.department, p.name)
```

```
HR Chandra
HR Anil
Sales Ravi
Sales Bina
```

Correctly sorted by department. Names scrambled inside each department, so the first pass achieved
nothing. **No exception. No warning.** In Python you will not hit this with `sorted()`, but you will
hit it the moment you write your own sort, or port the code to C++ or to Java's primitive sort.

### The trap: assuming your language's sort is stable

Python guarantees stability. Most languages do not.

```
 Python   list.sort / sorted        STABLE, guaranteed by the documentation
 Java     Arrays.sort(Object[])     STABLE (Timsort)
 Java     Arrays.sort(int[])        NOT STABLE (dual-pivot quicksort)
 C++      std::sort                 NOT STABLE
 C++      std::stable_sort          STABLE (that is why it has a separate name)
 C        qsort                     NOT STABLE (the name says quick, and it means it)
 JS       Array.prototype.sort      STABLE since ES2019; NOT before
 Go       sort.Slice                NOT STABLE; sort.SliceStable is
 Rust     sort                      STABLE; sort_unstable is faster
```

The pattern is that the *fast* one is unstable and the *stable* one has a longer name. Java's split
is the sharpest trap: the same method name is stable for objects and unstable for primitives, because
primitives have no identity to preserve — so the language decided it did not matter, and that
reasoning is worth being able to give.

### The trap: `reverse=True` is not `reversed(sorted(...))`

```python
ages = [("Asha", 34), ("Bala", 12), ("Chitra", 34)]
print(sorted(ages, key=lambda p: p[1], reverse=True))
print(list(reversed(sorted(ages, key=lambda p: p[1]))))
```

```
[('Asha', 34), ('Chitra', 34), ('Bala', 12)]
[('Chitra', 34), ('Asha', 34), ('Bala', 12)]
```

Both are correctly sorted by age descending. They disagree on the tie. `reverse=True` preserves the
original order of equal elements; reversing a sorted list flips them. If you are building a
leaderboard where equal scores should be shown in the order they were achieved, one of these is a bug
and it will be reported by a user, not by a test.

### The real error: sorting objects with no ordering

```python
staff = [Person("Ravi", "Sales", 34), Person("Anil", "HR", 28)]
staff.sort()
```

```
Traceback (most recent call last):
  File "day57.py", line 2, in <module>
    staff.sort()
    ~~~~~~~~~~^^
TypeError: '<' not supported between instances of 'Person' and 'Person'
```

`@dataclass` gives you `__eq__` but not `__lt__` unless you pass `order=True`. The fix is almost
always `key=`, not defining `__lt__` — because `key=` puts the ordering decision at the call site
where the reader can see it, and because one class rarely has one natural order.

### The trap: expecting stability from a `set` or a `dict` ordering

```python
sorted(set(names))
```

`set` has no order at all, so any information in the original sequence is destroyed *before* the sort
runs, and no amount of stability can recover it. Dictionaries preserve insertion order since Python
3.7, so `sorted(d.items(), key=...)` does keep insertion order among ties — but a `set` does not, and
this catches people who deduplicate before sorting.

### The trap: claiming Timsort is `O(n)`

It is `O(n)` on already-sorted or reverse-sorted or all-equal input, and `O(n log n)` in general.
Saying "Timsort is linear" is wrong; saying "Timsort is adaptive — linear on runs it can find,
n log n otherwise, and always stable" is right and takes the same breath.

---

## 8. In the interview

### How it gets asked

- *"Is Python's sort stable? Why do you care?"* — the direct form. One word, then the two-pass
  argument.
- *"Sort employees by department, then by name within department."* — the practical form, and the
  best answer names both the tuple key and the two-pass approach.
- *"Which sorting algorithms are stable?"* — and the useful answer is the *rule* (neighbour swaps are
  stable, long-distance swaps are not), not a memorised list.
- *"What sorting algorithm does Python use?"* — Timsort, and three facts about it.
- *"Can you make quicksort stable?"* — yes, at a cost that removes the reason to use quicksort.
- *"You're in C++ and `std::sort` reordered your equal elements. What do you do?"* —
  `std::stable_sort`, or decorate with the index.

### What to say out loud, in the first ninety seconds

1. **Define it precisely, in one sentence.** *"Stable means elements that compare equal come out in
   the order they went in. It says nothing about elements with different keys."*
2. **Give the reason immediately, with the example.** *"It matters for multi-key sorting. If I sort by
   name and then by department, only a stable sort leaves the names in order within each
   department — the second pass sees everyone in a department as equal, and a stable sort must not
   move them."*
3. **Say the pass order, because it is counter-intuitive.** *"And the passes go least-significant key
   first, which is backwards from how you say it in English."*
4. **Name the alternative and when you would prefer it.** *"If I control both keys in one place I'd
   use a tuple key — `key=lambda p: (p.department, p.name)` — because that works with any sort. The
   two-pass version is for when I can't, for instance a descending string field."*
5. **Answer the Python half.** *"Python's sort is guaranteed stable, and it's Timsort — a merge sort
   that finds runs that are already ordered, extends short ones with binary insertion sort, and
   gallops when merging. That's why it's linear on nearly-sorted input."*

### The follow-ups

**"Which sorts are stable, and why?"**
The useful answer is a rule rather than a list, because then I can answer it for a sort I have not
seen. **Sorts that only ever exchange adjacent elements are stable; sorts that move elements across
long distances are not.** Insertion sort is stable because the backward walk stops at the first
element that is not *strictly* greater, so an incoming value never passes an equal one — and that is
one character, `>` rather than `>=`. Bubble sort is stable for the same reason. Merge sort is stable
because when the two fronts are equal the merge takes from the left, which is again one character,
`<=` rather than `<`. Counting sort is stable if you place elements walking the input backwards into
end positions, and radix sort is not merely stable, it *depends* on stability — it is stability
applied once per digit, and with an unstable inner pass it produces a silently wrong answer. On the
other side: selection sort is unstable, and the counter-example is three elements — `[2a, 2b, 1]`,
where the first pass swaps the 1 into position zero and throws `2a` behind `2b`. Quicksort is
unstable because partitioning swaps across the whole range, and heapsort is unstable because the heap
reorders equal elements arbitrarily. The three unstable ones are exactly the three that move things a
long way in one step, which is why the rule works.

**"Can you make quicksort stable?"**
Yes, and I would not, because the fix removes the reason to choose quicksort in the first place.
There are two ways. The first is to stop partitioning in place: build the "less than" and "greater
than" lists separately by appending in input order, then concatenate. That preserves order among
equals, and it costs O(n) extra space per level — at which point I have written merge sort with a
worse pivot strategy and no worst-case guarantee. The second is decorate-sort-undecorate: attach each
element's original index as a tie-breaker so that no two elements compare equal at all, then any sort
is trivially stable. That works with C++'s `std::sort` or Java's primitive sort too, and the cost is
about twice the time and three times the memory at a million elements — a million tuple allocations
going in, a million coming out, and tuple comparisons being roughly one and a half times slower than
bare number comparisons. So the honest answer is: if I need stability I use a stable sort — merge
sort, `std::stable_sort`, Python's `sorted` — and if I am stuck with an unstable one, decorate with
the index and pay the memory.

**"What does Python actually run, and why is it fast on real data?"**
Timsort, written for Python in 2002 and since adopted by Java for object arrays, Android, V8, Swift
and Rust. It is a merge sort with three practical additions. First, it scans for runs that are
already in order — ascending, or strictly descending, which it reverses in place; the reversal is
safe for stability precisely because the run is *strictly* descending, so there are no ties in it.
Second, any run shorter than a computed minimum between thirty-two and sixty-four is extended by
binary insertion sort, which is exactly where insertion sort is genuinely the fastest thing
available. Third, the runs are merged under stack rules that keep their sizes balanced, and when one
run keeps winning the merge switches to galloping mode — it binary-searches ahead to find how many
elements it can take in one block instead of comparing one at a time, which turns a thousand
comparisons into about seventeen when two sorted lists are concatenated. The consequence is that
already-sorted input is one run and no merges, so linear; reverse-sorted is one reversal, so linear;
nearly-sorted is a handful of long runs. On two million integers I have measured about twenty
milliseconds for sorted input against about one and a tenth seconds for random — fifty-five times,
same n. What I would not say is that Timsort is O(n); it is adaptive, linear on the runs it can find,
n log n in general, O(n) extra space, and always stable.

### A model answer

> "Yes, guaranteed — the Python documentation states that `list.sort` and `sorted` are stable, so it's
> something you can rely on rather than an implementation detail.
>
> Stable means elements that compare equal come out in the order they went in. It says nothing about
> elements with different keys; it's only about ties.
>
> The reason I care is multi-key sorting. Suppose I want employees grouped by department and in name
> order within each department. If I can express that as one key I'd write
> `key=lambda p: (p.department, p.name)`, and that works with any sort because no two people compare
> equal unless both fields match. But often I can't — the classic case is one field descending where
> that field is a string, since `-p.name` raises a `TypeError`. Then I do it in two passes: sort by
> name first, then by department. And that's correct *only* because the sort is stable. The second
> pass sees everyone in a department as equal, and a stable sort must leave them exactly as the first
> pass arranged them. With an unstable sort the second pass is free to shuffle them, the first pass is
> wasted, and — this is the dangerous part — nothing raises. You just get an order nobody can explain.
>
> Note the pass order is least-significant key first, which is backwards from how you'd say it out
> loud.
>
> The other reason stability matters is when the input order is itself information: log lines in time
> order, search results in relevance order, database rows in insertion order. Sorting by severity or
> price with a stable sort keeps the original order inside each group for free.
>
> Two details I'd flag. `reverse=True` is not the same as reversing the sorted list — it preserves the
> original order of ties in both directions, whereas `reversed(sorted(...))` flips them. And most
> languages don't guarantee stability: C++'s `std::sort` doesn't and `std::stable_sort` does, Java's
> `Arrays.sort` is stable for objects and unstable for primitives, and Go and Rust both have a fast
> unstable sort and a slower stable one. So this is a fact about Python, not about sorting.
>
> Underneath, Python runs Timsort — a merge sort that finds stretches already in order, extends short
> ones with binary insertion sort, and gallops when one run dominates a merge. That's why sorting
> already-sorted data is linear: on two million integers it's about twenty milliseconds against just
> over a second for random input."

---

## 9. Recall card

- **Stable = elements that compare *equal* keep their original relative order.** It says nothing
  about unequal keys. Python's `list.sort` and `sorted` are **guaranteed** stable; most other
  languages are not (`std::sort` no / `std::stable_sort` yes; Java stable for objects, **not** for
  primitives; Go and Rust each have both).
- **Why you care: two-pass multi-key sorting.** Sort by the **least significant key first**, then the
  most significant — the second pass sees ties and a stable sort must not move them. Prefer a tuple
  key (`(dept, name)`) when you control both; you *need* two passes when a string field must go
  descending, because `-p.name` raises `TypeError`.
- **The rule for which sorts are stable: neighbour swaps are stable, long-distance swaps are not.**
  Stable: insertion, bubble, merge, counting (placed backwards), radix (it *depends* on it).
  Unstable: **selection, quicksort, heapsort**. Selection's counter-example is `[2a, 2b, 1]`.
- **The bugs are one character and silent.** `<` instead of `<=` in a merge, `>=` instead of `>` in
  insertion sort, counting sort placed forwards — all still sort correctly and quietly lose
  stability. Keep the four-line `is_stable` test with `(key, tag)` pairs. And `reverse=True`
  **preserves** ties; `reversed(sorted(...))` flips them.
- **Python runs Timsort:** finds natural runs (a *strictly* descending one is reversed in place),
  extends short runs with **binary insertion sort** to a minrun of 32-64, merges with **galloping**
  (1,000 comparisons → ~17 on concatenated sorted lists). Adaptive — 2M sorted integers in ~0.02 s
  against ~1.1 s random, 55×. Stable, O(n) space, **not** O(n) in general.
