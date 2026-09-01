---
day: 168
track: dsa
title: "Meeting rooms and the sweep line"
phase: "Greedy and intervals"
status: written
---

# Meeting rooms and the sweep line

## 1. What this is, and why they ask it

**A sweep line answers questions about *how many things are happening at once*, and it does it by throwing away
which things they are.**

The canonical form is meeting rooms: given a set of meetings, **how many rooms do you need?** And the answer is
not a scheduling algorithm — **it is a counting algorithm.**

They ask it because **the decomposition is a genuine idea rather than a pattern to memorise.** Break every
interval into two independent events, a start and an end. **Discard the association between them.** Sort all
the events by time and walk through, adding one and subtracting one. **The maximum the running total reaches is
the answer.**

**That "discard the association" step is what people do not think of**, and it is what turns a problem that
sounds like assignment into six lines of counting.

The second reason is that **it generalises much further than meeting rooms.** The same shape answers: the
busiest minute of the day, whether any two intervals overlap, the total covered length, how many people were in
the building at 3pm, and — with one change — the skyline problem, which is the hard version and appears in
senior interviews.

**And there is one specific detail that is wrong in about half of all implementations: the tie-break.** When a
meeting ends at four and another starts at four, **which event is processed first decides whether the answer is
one or two.** It is one comparison, it depends on the problem's convention, **and getting it backwards gives an
answer exactly one too high on the most realistic inputs there are.**

By the end of this lesson you can write the sweep, get the tie-break right, know the two equivalent forms,
extend it to the variants, and say when it is the wrong tool.

---

## 2. The story

The temple ran the free meal on festival days and the thing nobody outside the kitchen understood was that the
problem was never the food.

**It was the plates.**

Because they had four hundred and eleven steel plates, and about three thousand people came through over five
hours, **and a plate came back and was washed and went out again.** So three thousand people did not need three
thousand plates.

**They needed as many plates as there were people eating at the same moment.**

And for eleven years the way they worked that out was that Jagannath stood at the door and watched, **and when
the stack got low somebody ran to borrow from the next street.**

**Which worked, badly, and twice it did not work at all.**

What changed it was the boy who kept the register, who was doing his intermediate and had been made to help.

**He was not interested in the plates. He was interested in the door.**

Because at the door, **you did not need to know who anybody was.** He stopped writing names entirely and wrote
two things: **the time somebody went in, and the time somebody came out.** Two separate lines. **Not joined
up.**

And then he did something that took him an evening and that Jagannath thought was a waste of an evening.

**He put every one of those times in order — the going-ins and the coming-outs all mixed together — and walked
down the list with a pencil, adding one for each going-in and taking one away for each coming-out.**

The number went up and down all afternoon.

**And the biggest it ever got was three hundred and eighty-four.** At about half past one.

**Four hundred and eleven plates. They had never actually needed to borrow.**

Jagannath's objection, which he made immediately, was that the boy did not know which plate went to which
person and therefore could not possibly have worked it out.

**"I do not need to know which plate," the boy said. "I only need to know how many at once. Those are
different questions and I have been answering the easier one."**

---

## 3. The idea in plain English

The boy's two lines at the door are the decomposition, and his last sentence is the whole technique: **"how
many at once" is a different and much easier question than "which one is which".**

**Start with what the sweep actually is.**

> **Break every interval into two independent events: `+1` at its start and `-1` at its end. Throw away which
> interval they came from. Sort every event by time. Walk through, keeping a running total. The maximum is the
> answer.**

**The discarding is the idea.** Once the events are independent, **there is no assignment problem left** — only
a list of numbers and a running sum.

```
   meetings:  [1,4]  [2,5]  [7,9]  [3,6]

   events:    1:+1   2:+1   3:+1   4:-1   5:-1   6:-1   7:+1   9:-1

   running:    1      2      3      2      1      0      1      0
                             ^
                          maximum 3  ->  three rooms
```

**Six lines of code, and the hardest part is realising that the meetings can be taken apart.**

**Now the tie-break, which is where half of all implementations are wrong.**

**A meeting ends at 4 and another starts at 4. Is that one room or two?**

**For meeting rooms: one.** The first group leaves and the second arrives; the room is free. **So at equal
times, process the END first** — the counter goes down before it goes up, and it never reaches two.

**For a question where the endpoints are inclusive** — "how many people were present at time 4" — **both count,
so the start is processed first.**

**It is one comparison and the problem decides it.** And in Python there is a pleasant trick: **sort the events
as `(time, delta)` tuples.** Because `-1 < +1`, **ties are broken in favour of the end automatically**, which is
the meeting-rooms convention, for free.

**Encode the events as `(time, "start")` and `(time, "end")` instead and it happens to work** — `"end"` sorts
before `"start"` — **and that is a coincidence of the alphabet, not a design.** Use numbers.

**Getting it backwards gives an answer exactly one too high**, on exactly the inputs a real calendar produces,
where meetings abut on the hour.

**Then the second form, which is the same algorithm and reads differently.**

**Sort the start times and the end times into two separate arrays, and merge them with two pointers.**

```python
if starts[i] < ends[j]:
    rooms += 1; i += 1
else:
    rooms -= 1; j += 1
```

**Identical answer.** Some people find it clearer; **it also makes the tie-break explicit** — `<` against `<=`
— **rather than hiding it in a sort key.**

**And a third form, which answers a different question: the heap.**

**The sweep counts rooms. It cannot tell you which meeting is in which room**, because it threw that
information away — **which is precisely what made it cheap.**

**If you need the assignment**, process the meetings in start order and keep a min-heap of the rooms' end
times: **reuse the earliest-freeing room if it is free by now, otherwise open a new one.** The heap's size is
the room count, **so it agrees with the sweep and also gives you the answer to "which room".**

**Now the variants, because the sweep generalises much further than meeting rooms.**

**The busiest moment**, not just the maximum count — track *when* the maximum occurred, which is one extra
variable.

**Does anything overlap at all?** — the maximum reaching two. **Though for that specific question, sorting the
intervals and checking adjacent pairs is simpler.**

**Total covered length** — sum the time between events while the counter is above zero. **Which is merging,
done differently**, and it is worth noticing that the sweep can do it.

**Weighted sweeps**, where events carry a value rather than one — how much bandwidth is in use, how many
people are in the building weighted by group size. **The `+1` and `-1` become `+w` and `-w` and nothing else
changes.**

**And the skyline problem, which is the hard version.** Buildings as intervals with heights; **produce the
outline.** The sweep is the same, **but the running total is not a sum — it is the *maximum* of the active
heights**, so instead of a counter you need a multiset that can report its maximum and remove an arbitrary
element. **A heap with lazy deletion is the usual answer**, and knowing that it is "the same sweep with a
different accumulator" is what makes the problem approachable.

**Finally: when the sweep is the wrong tool.**

**When you need to know which interval is which** — the assignment — **it has thrown that away.**

**When the events are not points in one dimension.** Rectangles overlapping in two dimensions need a sweep in
one axis with a *structure* over the other, **which is a substantially harder algorithm.**

**And when the coordinates are dense and small.** If times are minutes in a day, **a plain array of 1,440
counters is simpler and faster than sorting events** — increment a range, then scan. **That is a difference
prefix-sum, and reaching for a sweep when a small array suffices is over-engineering.**

---

## 4. The picture

The decomposition, which is the idea:

```
   MEETINGS (paired)              EVENTS (independent)

   [1 ----------- 4]              1:+1        4:-1
      [2 ------------ 5]          2:+1              5:-1
         [3 ------------- 6]      3:+1                    6:-1
                    [7 -- 9]                  7:+1            9:-1

   THROW AWAY WHICH IS WHICH.

   sorted:  1:+1  2:+1  3:+1  4:-1  5:-1  6:-1  7:+1  9:-1
   running:  1     2     3     2     1     0     1     0
                         ^
                      MAXIMUM 3

   "I do not need to know which plate. I only need to know how many
    at once. Those are different questions."
```

The tie-break, which is where half of implementations are wrong:

```
   meeting A ends at 4.  meeting B starts at 4.

   PROCESS THE END FIRST (meeting rooms — the room is freed):

     ... 4:-1   4:+1 ...
     running:  1  ->  0  ->  1        MAXIMUM 1     ONE ROOM

   PROCESS THE START FIRST (inclusive endpoints — both present at 4):

     ... 4:+1   4:-1 ...
     running:  1  ->  2  ->  1        MAXIMUM 2     TWO

   ONE COMPARISON, AND THE PROBLEM DECIDES IT.

   IN PYTHON: sort (time, delta) tuples.
     -1 < +1, so the END sorts first automatically
     -> the meeting-rooms convention, for free

   Encoding as (time, "start") / (time, "end") happens to work
   because "end" < "start" alphabetically. That is a coincidence
   of the alphabet, not a design. USE NUMBERS.
```

The two equivalent forms:

```
   EVENT LIST                        TWO POINTERS

   events = []                       starts = sorted(all starts)
   for s, e in meetings:             ends   = sorted(all ends)
       events.append((s, +1))
       events.append((e, -1))        i = j = rooms = best = 0
   events.sort()                     while i < len(starts):
                                         if starts[i] < ends[j]:
   for _, d in events:                       rooms += 1
       current += d                          best = max(best, rooms)
       best = max(best, current)              i += 1
                                          else:
                                              rooms -= 1
                                              j += 1

   sorts 2n events                   sorts two arrays of n
   the tie-break is in the sort      the tie-break is the < vs <=
   -> SAME ANSWER, same complexity. Pick whichever is clearer.
```

What the sweep cannot do, and what can:

```
   THE SWEEP                         THE HEAP

   "how many rooms?"                 "WHICH room for each meeting?"

   discards the association          keeps it:
   -> cheap                            process in START order
   -> and cannot answer                keep a min-heap of room END times
      the assignment                   reuse the earliest-freeing room
                                       if free, else open a new one

   3                                 [1, 2, 3, 1]
                                     ^ the heap SIZE equals the sweep's
                                       answer, so they agree
```

The variants, all the same shape:

```
   question                       what changes
   -------------------------------------------------------------
   how many rooms                 the maximum of the running total
   the BUSIEST moment             also record WHEN the max occurred
   does anything overlap          the maximum reaching 2
   total covered length           sum the time while the total > 0
   weighted (bandwidth, people)   +w and -w instead of +1 and -1
   THE SKYLINE                    the accumulator is a MAX, not a sum
                                  -> a multiset / heap with lazy deletion

   -> the sweep is a FRAMEWORK: sort events, walk, accumulate.
      Only the accumulator changes.
```

When not to sweep:

```
   DENSE, SMALL COORDINATES

     times are minutes in a day: 1,440 possible values

     sweep:            sort 2n events           O(n log n)
     difference array: counts[start] += 1
                       counts[end]   -= 1
                       then one prefix sum      O(n + 1440)

     -> for n = 10,000 meetings the array version is FASTER and
        simpler. Reaching for a sweep here is over-engineering.

   TWO DIMENSIONS

     overlapping RECTANGLES need a sweep in x with a STRUCTURE
     over y (a segment tree) — a substantially harder algorithm,
     not a small extension.

   WHEN YOU NEED THE ASSIGNMENT

     the sweep threw it away. Use the heap.
```

---

## 5. The code, built step by step

### The sweep

```python
def min_rooms(intervals: list[tuple[int, int]]) -> int:
    """
    How many at once? Break into events; discard which is which.

    (time, delta) sorting puts -1 before +1 at equal times, which is
    the meeting-rooms convention: a room freed at 4 is reusable at 4.
    """
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, +1))
        events.append((end, -1))
    events.sort()

    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best
```

**Six lines of work, and the comment is the important part.** **`events.sort()` on tuples sorts by time and
then by delta**, and since `-1 < +1` the end is processed first — **exactly the convention meeting rooms
needs, with no explicit tie-break code.**

### The other convention

```python
def max_concurrent_inclusive(intervals: list[tuple[int, int]]) -> int:
    """Endpoints INCLUSIVE: both a start and an end at time t count."""
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 0, +1))         # 0 sorts before 1
        events.append((end, 1, -1))
    events.sort()

    current = best = 0
    for _, _, delta in events:
        current += delta
        best = max(best, current)
    return best
```

**An explicit priority field is the honest way to express the other convention** — `0` for starts and `1` for
ends — **rather than relying on the sign of the delta.**

**Writing both versions once is worth doing**, because the difference between them is exactly the question the
interviewer is checking you asked.

### The two-pointer form

```python
def min_rooms_two_pointer(intervals: list[tuple[int, int]]) -> int:
    """The same algorithm; the tie-break is the `<` rather than a sort key."""
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = best = 0
    i = j = 0
    while i < len(starts):
        if starts[i] < ends[j]:               # `<`: a room freed at 4 is reusable
            rooms += 1
            best = max(best, rooms)
            i += 1
        else:
            rooms -= 1
            j += 1
    return best
```

**`starts[i] < ends[j]` is the same decision as the sort key**, expressed where you can see it. **Change it to
`<=` and you get the inclusive convention.**

**And the loop condition is `i < len(starts)` alone**, because once every meeting has started the remaining
ends cannot raise the maximum — **iterating both to exhaustion is harmless and wasteful.**

### The busiest moment, not just the count

```python
def busiest_moment(intervals: list[tuple[int, int]]) -> tuple[int, int]:
    """Returns (peak_count, when). One extra variable."""
    events = sorted([(s, +1) for s, _ in intervals] +
                    [(e, -1) for _, e in intervals])
    current = best = at = 0
    for time, delta in events:
        current += delta
        if current > best:                    # `>` records the FIRST peak
            best, at = current, time
    return best, at
```

**`if current > best` rather than `>=` records the *first* moment the peak is reached**, which is usually what
"when were we busiest" means — **and `>=` would report the last, which is a defensible different answer worth
naming.**

### Total covered length, via the sweep

```python
def total_covered(intervals: list[tuple[int, int]]) -> int:
    """Sum the time while the counter is above zero. Merging, differently."""
    events = sorted([(s, +1) for s, _ in intervals] +
                    [(e, -1) for _, e in intervals])
    current = total = 0
    previous_time = 0
    for time, delta in events:
        if current > 0:
            total += time - previous_time     # this stretch was covered
        current += delta
        previous_time = time
    return total
```

**Accumulating *before* applying the delta is the ordering that matters**: the stretch between the previous
event and this one was covered at the *old* count, not the new one.

**And this is the merge from yesterday, computed without producing the blocks** — which is worth noticing,
because it means the sweep subsumes it.

### A weighted sweep

```python
def peak_bandwidth(streams: list[tuple[int, int, int]]) -> int:
    """(start, end, mbps). +w and -w instead of +1 and -1. Nothing else changes."""
    events = sorted([(s, +w) for s, _, w in streams] +
                    [(e, -w) for _, e, w in streams])
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best
```

**The only change is the magnitude of the delta**, which is the clearest demonstration that the sweep is a
framework rather than one algorithm.

### The heap, when you need the assignment

```python
import heapq

def assign_rooms(intervals: list[tuple[int, int]]) -> list[int]:
    """The sweep COUNTS; the heap ASSIGNS. Same answer for the count."""
    order = sorted(range(len(intervals)), key=lambda i: intervals[i][0])
    free: list[tuple[int, int]] = []          # (end_time, room_number)
    assignment = [0] * len(intervals)
    rooms_used = 0
    for i in order:
        start, end = intervals[i]
        if free and free[0][0] <= start:      # the earliest-freeing room is ready
            _, room = heapq.heappop(free)
        else:
            rooms_used += 1
            room = rooms_used
        assignment[i] = room
        heapq.heappush(free, (end, room))
    return assignment
```

**`free[0][0] <= start` is the tie-break again** — a room freed at 4 is reusable at 4 — **and it must match
whatever the sweep uses**, or the two disagree.

**`rooms_used` ends equal to the sweep's answer**, which is a free consistency check worth running.

### The difference array, for dense coordinates

```python
def min_rooms_dense(intervals: list[tuple[int, int]], horizon: int = 1440) -> int:
    """Times are minutes in a day: an array beats sorting events."""
    counts = [0] * (horizon + 1)
    for start, end in intervals:
        counts[start] += 1
        counts[end] -= 1                      # exclusive end: freed at `end`
    current = best = 0
    for delta in counts:
        current += delta
        best = max(best, current)
    return best
```

**`O(n + horizon)` rather than `O(n log n)`**, and for ten thousand meetings across 1,440 minutes it is
**faster and simpler than sorting events.**

**Reaching for the sweep when the coordinate space is small is over-engineering**, and noticing that is worth a
sentence in an interview.

### The skyline: the same sweep, a different accumulator

```python
import heapq

def skyline(buildings: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    """
    (left, right, height) -> the outline.

    THE SAME SWEEP. The accumulator is a MAX rather than a sum, so
    it needs a heap with lazy deletion instead of an integer.
    """
    events = sorted([(l, -h, r) for l, r, h in buildings] +
                    [(r, 0, 0) for _, r, _ in buildings])
    result: list[tuple[int, int]] = []
    live = [(0, float("inf"))]                # (-height, end): a ground plane
    for x, negative_height, right in events:
        while live[0][1] <= x:                # LAZY DELETION: drop the expired
            heapq.heappop(live)
        if negative_height:
            heapq.heappush(live, (negative_height, right))
        current = -live[0][0]
        if not result or result[-1][1] != current:
            result.append((x, current))
    return result
```

**`while live[0][1] <= x` is lazy deletion**, and it is the trick: **a heap cannot remove an arbitrary element,
so instead you leave expired entries in and discard them when they surface.** Each entry is popped at most
once, so the total cost stays `O(n log n)`.

**`(l, -h, r)` sorts taller buildings first at the same x**, which is what makes the outline correct when
several begin together.

**And the framing is the useful part: this is the meeting-rooms sweep with `max` instead of `+`.** Seeing that
makes a Hard problem approachable.

### The complete solution

```python
"""The sweep line: break intervals into events, discard which is which."""

import heapq
import random


def min_rooms(intervals: list[tuple[int, int]]) -> int:
    """(time, delta) sorting puts -1 before +1: a room freed at 4 is reusable."""
    events = sorted([(s, +1) for s, _ in intervals] +
                    [(e, -1) for _, e in intervals])
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best


def max_concurrent_inclusive(intervals: list[tuple[int, int]]) -> int:
    """The OTHER convention: both endpoints count at the same instant."""
    events = sorted([(s, 0, +1) for s, _ in intervals] +
                    [(e, 1, -1) for _, e in intervals])
    current = best = 0
    for _, _, delta in events:
        current += delta
        best = max(best, current)
    return best


def min_rooms_two_pointer(intervals: list[tuple[int, int]]) -> int:
    """The same algorithm; the tie-break is visible as `<`."""
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = best = 0
    i = j = 0
    while i < len(starts):
        if starts[i] < ends[j]:
            rooms += 1
            best = max(best, rooms)
            i += 1
        else:
            rooms -= 1
            j += 1
    return best


def busiest_moment(intervals: list[tuple[int, int]]) -> tuple[int, int]:
    """`>` records the FIRST moment the peak is reached; `>=` the last."""
    events = sorted([(s, +1) for s, _ in intervals] +
                    [(e, -1) for _, e in intervals])
    current = best = at = 0
    for time, delta in events:
        current += delta
        if current > best:
            best, at = current, time
    return best, at


def total_covered(intervals: list[tuple[int, int]]) -> int:
    """Accumulate BEFORE applying the delta: the stretch had the old count."""
    events = sorted([(s, +1) for s, _ in intervals] +
                    [(e, -1) for _, e in intervals])
    current = total = previous_time = 0
    for time, delta in events:
        if current > 0:
            total += time - previous_time
        current += delta
        previous_time = time
    return total


def peak_weighted(items: list[tuple[int, int, int]]) -> int:
    """(start, end, weight). Only the magnitude of the delta changes."""
    events = sorted([(s, +w) for s, _, w in items] +
                    [(e, -w) for _, e, w in items])
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best


def assign_rooms(intervals: list[tuple[int, int]]) -> list[int]:
    """The heap ASSIGNS what the sweep only COUNTS."""
    order = sorted(range(len(intervals)), key=lambda i: intervals[i][0])
    free: list[tuple[int, int]] = []
    assignment = [0] * len(intervals)
    rooms_used = 0
    for i in order:
        start, end = intervals[i]
        if free and free[0][0] <= start:
            _, room = heapq.heappop(free)
        else:
            rooms_used += 1
            room = rooms_used
        assignment[i] = room
        heapq.heappush(free, (end, room))
    return assignment


def min_rooms_dense(intervals: list[tuple[int, int]], horizon: int = 1440) -> int:
    """Small coordinate space: a difference array beats sorting events."""
    counts = [0] * (horizon + 2)
    for start, end in intervals:
        counts[start] += 1
        counts[end] -= 1
    current = best = 0
    for delta in counts:
        current += delta
        best = max(best, current)
    return best


def skyline(buildings: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    """The same sweep with MAX as the accumulator: a heap with lazy deletion."""
    events = sorted([(l, -h, r) for l, r, h in buildings] +
                    [(r, 0, 0) for _, r, _ in buildings])
    result: list[tuple[int, int]] = []
    live: list[tuple[float, float]] = [(0, float("inf"))]
    for x, negative_height, right in events:
        while live[0][1] <= x:                # lazy deletion
            heapq.heappop(live)
        if negative_height:
            heapq.heappush(live, (negative_height, right))
        current = int(-live[0][0])
        if not result or result[-1][1] != current:
            result.append((x, current))
    return result


def brute_max_concurrent(intervals: list[tuple[int, int]]) -> int:
    """Check every interval's start as a candidate instant. Obviously correct."""
    best = 0
    for s, _ in intervals:
        overlapping = sum(1 for a, b in intervals if a <= s < b)
        best = max(best, overlapping)
    return best


if __name__ == "__main__":
    random.seed(0)
    meetings = [(1, 4), (2, 5), (3, 6), (7, 9)]
    print("THE SWEEP")
    print("  meetings          :", meetings)
    print("  rooms needed      :", min_rooms(meetings))
    print("  two-pointer agrees:", min_rooms_two_pointer(meetings))
    print("  busiest moment    :", busiest_moment(meetings))
    print("  assignment        :", assign_rooms(meetings))

    print("\nTHE TIE-BREAK — meetings that abut")
    abutting = [(1, 4), (4, 6), (6, 9)]
    print("  meetings              :", abutting)
    print("  end first (rooms)     :", min_rooms(abutting))
    print("  start first (inclusive):", max_concurrent_inclusive(abutting))

    print("\nTHE VARIANTS")
    print("  total covered     :", total_covered(meetings))
    streams = [(0, 10, 100), (5, 15, 250), (12, 20, 400)]
    print("  peak bandwidth    :", peak_weighted(streams), "mbps")
    print("  dense array agrees:", min_rooms_dense(meetings, horizon=20))

    print("\nTHE SKYLINE — the same sweep, MAX instead of sum")
    print("  buildings :", [(2, 9, 10), (3, 7, 15), (5, 12, 12),
                            (15, 20, 10), (19, 24, 8)])
    print("  outline   :", skyline([(2, 9, 10), (3, 7, 15), (5, 12, 12),
                                    (15, 20, 10), (19, 24, 8)]))

    print("\nVERIFICATION")
    mismatches = 0
    for _ in range(500):
        n = random.randint(1, 10)
        ivs = [(lambda s: (s, s + random.randint(1, 8)))(random.randint(0, 15))
               for _ in range(n)]
        if min_rooms(ivs) != brute_max_concurrent(ivs):
            mismatches += 1
    print(f"  sweep vs brute force: {mismatches} mismatches in 500 cases")
```

Run it and you get:

```
THE SWEEP
  meetings          : [(1, 4), (2, 5), (3, 6), (7, 9)]
  rooms needed      : 3
  two-pointer agrees: 3
  busiest moment    : (3, 3)
  assignment        : [1, 2, 3, 1]

THE TIE-BREAK — meetings that abut
  meetings              : [(1, 4), (4, 6), (6, 9)]
  end first (rooms)     : 1
  start first (inclusive): 2

THE VARIANTS
  total covered     : 7
  peak bandwidth    : 650 mbps
  dense array agrees: 3

THE SKYLINE — the same sweep, MAX instead of sum
  buildings : [(2, 9, 10), (3, 7, 15), (5, 12, 12), (15, 20, 10), (19, 24, 8)]
  outline   : [(2, 10), (3, 15), (7, 12), (12, 0), (15, 10), (20, 8), (24, 0)]

VERIFICATION
  sweep vs brute force: 0 mismatches in 500 cases
```

**`end first : 1` against `start first : 2`** on three abutting meetings is the tie-break, made visible —
**one comparison, and the answer doubles.** And abutting meetings are what a real calendar looks like.

**And the skyline output is the same sweep with a different accumulator**, which is the framing that makes a
Hard problem tractable: **sort events, walk, accumulate — and only the accumulator changed.**

---

## 6. What it costs

**The sweep.**

```
   build 2n events    O(n)
   sort them          O(n log n)    <- dominates
   one pass           O(n)
   space              O(n) for the events

   TOTAL: O(n log n) time, O(n) space
```

**The two-pointer form, for comparison:**

```
   sort two arrays of n:   2 x O(n log n)
   against sorting 2n:     O(2n log 2n)

   -> 2n log n against 2n log n + 2n
   -> marginally better, same complexity, under 10% in practice

   Pick whichever reads more clearly. The difference is not real.
```

**Concretely:**

```
   n = 1,000        instant
   n = 100,000      sort 200,000 events ~0.2 s in Python
   n = 10,000,000   sort 20,000,000 events ~25 s

   -> the sweep scales exactly as well as sorting, because it IS
      sorting plus a linear pass
```

**The difference array, when coordinates are dense:**

```
   sweep:            O(n log n)
   difference array: O(n + horizon)

   n = 10,000 meetings, horizon = 1,440 minutes:
     sweep:  20,000 events sorted  ~200,000 operations
     array:  10,000 updates + 1,440 scan  ~11,440 operations

   -> ~18x faster AND simpler

   and it inverts when the horizon is large:
     n = 100 meetings over a year in seconds (horizon 31,536,000):
       sweep:  200 events    -> trivial
       array:  31.5M entries -> 250 MB and pointless
```

**The crossover is roughly `horizon < n log n`**, and knowing which side you are on is worth ten seconds of
arithmetic.

**The heap version:**

```
   sort by start           O(n log n)
   n heap pushes/pops      O(n log k), k = rooms
   -> O(n log n) overall

   space: O(k), the number of rooms — often far smaller than n

   -> same complexity as the sweep, and it produces the ASSIGNMENT
   -> so the sweep's only advantage is simplicity and O(1) working state
```

**The skyline:**

```
   2n events sorted            O(n log n)
   each pushed once, popped at most once (LAZY DELETION)
   -> O(n log n) total

   the lazy deletion is what keeps it O(n log n):
     a heap cannot remove an arbitrary element, so expired entries
     stay in and are discarded when they surface
     -> the heap can hold up to n entries, but each is popped once

   without lazy deletion you would need a structure supporting
   arbitrary removal — a balanced BST or an indexed heap — which
   is the same complexity and considerably more code.
```

**Space, across the variants:**

```
   sweep, counting only    O(n) events, O(1) working state
   two-pointer             O(n) for two arrays, O(1) working
   difference array        O(horizon)
   heap assignment         O(k) where k = rooms
   skyline                 O(n) for the heap in the worst case
```

**Compared with the naive approach:**

```
   "maximum concurrent" by checking every instant against every interval:
     O(n^2)

   n = 100,000:  10^10 against 3.4 x 10^6   -> ~3,000x

   and the naive version also has to CHOOSE the instants to check,
   which is only correct if you check every interval's start —
   a subtlety that the sweep removes entirely.
```

**And the framework property, in cost terms:**

```
   changing the accumulator costs NOTHING asymptotically:

     count   -> an integer         O(1) per event
     weighted-> an integer         O(1) per event
     maximum -> a heap             O(log n) per event
     -> the last one adds a log factor and stays O(n log n)
        because the sort already costs that
```

---

## 7. The traps

**The tie-break, backwards.**

```python
>>> min_rooms([(1, 4), (4, 6), (6, 9)])
1
>>> max_concurrent_inclusive([(1, 4), (4, 6), (6, 9)])
2
```

**One against two, on three meetings that abut.** **Both are correct for different questions**, and the
meeting-rooms answer is one — **the room is freed at four and immediately reused.**

**And abutting meetings are what a real calendar looks like**, so this fails on the most realistic input there
is, **by exactly one.**

**Encoding events as strings.**

```python
>>> sorted([(4, "start"), (4, "end")])
[(4, 'end'), (4, 'start')]
```

**It happens to give the meeting-rooms convention**, because `"end"` sorts before `"start"`. **That is a
coincidence of the alphabet.** Rename them to `"begin"` and `"finish"` and it silently reverses. **Use numbers,
where the ordering is intentional.**

**Forgetting that the sweep discards the assignment.**

```python
>>> min_rooms([(1, 4), (2, 5), (3, 6), (7, 9)])
3
>>> # "which room is the 7-9 meeting in?"
>>> # the sweep cannot say. It threw that away — which is what
>>> # made it cheap.
```

**If the question asks which meeting goes where, the counter is not enough**, and the heap is the answer.
**Reading the question for "how many" against "which" decides the algorithm.**

**Accumulating covered time in the wrong order.**

```python
>>> # if you apply the delta BEFORE adding the stretch:
>>> # the stretch between the previous event and this one gets
>>> # counted at the NEW count, not the old one
>>> # -> the first and last stretches are wrong
```

**The stretch that just ended had the *previous* count**, so add it first and then apply the delta. **It is one
line's ordering and it produces an answer that is close and wrong.**

**Using a difference array when the horizon is huge.**

```python
>>> counts = [0] * (31_536_000 + 2)     # a year in seconds
>>> # 250 MB for 100 meetings
```

**No error, and it is absurd.** **The array version is right when the coordinate space is small and dense** —
minutes in a day — and wrong otherwise. **Compare `horizon` against `n log n` before choosing.**

**Comparing floating-point times.**

```python
>>> events = sorted([(0.1 + 0.2, +1), (0.3, -1)])
>>> events
[(0.3, -1), (0.30000000000000004, 1)]
```

**`0.1 + 0.2` is not `0.3`**, so two events that should be simultaneous are ordered — **and the tie-break you
carefully designed does not apply, because there is no tie.** **Work in integers** — minutes, seconds,
milliseconds — **not in floating-point hours.**

**Mismatched conventions between the sweep and the heap.**

```python
>>> # sweep uses (time, delta) -> end before start -> 1 room
>>> # heap uses `free[0][0] < start` (strict) -> does NOT reuse at 4
>>> #                                        -> 2 rooms
>>> # the two now DISAGREE, and both look right in isolation
```

**If you implement both, they must use the same convention**, and **checking that they agree is a free
consistency test** worth running.

**The skyline without lazy deletion.**

```python
>>> # trying to remove a specific building from a heap when it ends:
>>> # heapq has no such operation
>>> # -> people write a linear scan-and-remove, which is O(n) per event
>>> # -> O(n^2) overall
```

**Lazy deletion — leave expired entries in and discard them when they surface — keeps it `O(n log n)`**,
because each entry is popped at most once.

**Not checking whether an array beats the sort.**

```
   10,000 meetings, minutes in a day:
     sweep: ~200,000 operations
     array: ~11,400 operations

   -> 18x, and the array version is fewer lines
```

**Reaching for the sweep reflexively when the coordinates are small is over-engineering**, and noticing it is a
real signal.

---

## 8. In the interview

### How it gets asked

- *"How many meeting rooms do you need?"* — LeetCode 253, the canonical form.
- *"Do these meetings conflict?"* — LeetCode 252, the easy opener.
- *"What was the busiest minute?"* — the variant.
- *"Given buildings, produce the skyline."* — LeetCode 218, the hard version.
- *"Which meeting goes in which room?"* — the follow-up the sweep cannot answer.
- *"Does `[2,4]` conflict with `[4,6]`?"* — checking whether you ask.

### The first ninety seconds

> "This sounds like a scheduling problem and it is a counting problem, **and noticing that is the whole
> technique.**
>
> **I do not need to know which meeting is in which room. I need to know how many are happening at the busiest
> moment.** Those are different questions and the second one is much easier.
>
> **So: break every meeting into two independent events.** Plus one at its start, minus one at its end. **Throw
> away which meeting they came from.** Sort every event by time, walk through with a running total, **and the
> maximum it reaches is the number of rooms.**
>
> **Six lines, and the discarding is the idea** — once the events are independent there is no assignment
> problem left, only a list of numbers and a running sum.
>
> **The detail that matters is the tie-break, and I would settle it before writing.** A meeting ends at four
> and another starts at four: **for rooms that is one room, because the first group leaves and the second
> arrives.** So at equal times, **process the end before the start** — the counter goes down before it goes up
> and never reaches two.
>
> **In Python that comes free by sorting `(time, delta)` tuples**, because minus one sorts before plus one.
>
> **And getting it backwards gives an answer exactly one too high** — on meetings that abut on the hour, which
> is what every real calendar looks like.
>
> **I would not encode the events as strings.** `"end"` happens to sort before `"start"`, **which is a
> coincidence of the alphabet**, and renaming them silently reverses the convention.
>
> **Cost: `O(n log n)` dominated by sorting the events, `O(n)` space, `O(1)` working state.**
>
> **There is an equivalent two-pointer form** — sort the starts and ends separately and merge them — **which
> makes the tie-break visible as a `<` rather than hiding it in a sort key.** Same answer, same complexity.
>
> **And one question before I code: does the answer need to say which room each meeting is in?** Because the
> sweep threw that away — **that is exactly what made it cheap** — and if you want the assignment I would use a
> min-heap of room end times instead."

### The follow-ups

**"Why does the tie-break matter, and which way should it go?"**

> "Because it changes the answer by exactly one, on the most realistic input there is.
>
> **The situation: a meeting ends at four and another starts at four.**
>
> **For meeting rooms, that is one room.** The first group walks out, the second walks in, and the room was
> never occupied by both. **So the end event must be processed first** — the counter drops to zero and then
> rises to one, and never reaches two.
>
> **Process the start first and the counter goes one, two, one** — and the maximum is two, **so the answer says
> two rooms where one is enough.**
>
> **And this fails on abutting meetings, which is what a real calendar is made of** — nine to ten, ten to
> eleven, eleven to twelve. **So the wrong convention is wrong on almost every real input, by exactly one.**
>
> **The other convention is right for a different question.** If I ask 'how many people were present at time
> four' with inclusive endpoints, **both the person leaving and the person arriving are present at that
> instant**, and the start should go first.
>
> **So the problem decides it, and I would ask if it is not stated** — and say which I assumed either way.
>
> **On implementation: in Python, sorting `(time, delta)` tuples gives the meeting-rooms convention for
> free**, because minus one sorts before plus one. **If I need the other convention I would add an explicit
> priority field** — zero for starts, one for ends — **rather than relying on the sign.**
>
> **And I would specifically not encode the events as strings.** `(4, "end")` sorts before `(4, "start")`
> because `"e"` comes before `"s"` — **which gives the right answer for the wrong reason**, and renaming them
> to `"begin"` and `"finish"` silently reverses it.
>
> **One more: work in integers.** Floating-point times break the tie-break entirely, because `0.1 + 0.2` is not
> `0.3` — **two events that should be simultaneous get ordered, and the tie-break you designed never
> applies.**"

**"Now tell me which room each meeting is in."**

> "Then the sweep cannot help, **and the reason is the interesting part: it discarded exactly that
> information, and that is what made it cheap.**
>
> **The sweep breaks meetings into independent events and throws away which meeting each event came from.**
> That is why it is six lines and constant working state — **and it is why it can only ever answer 'how many'.**
>
> **For the assignment I would use a min-heap of room end times.**
>
> **Process the meetings in start order.** Keep a heap of `(end_time, room_number)` for the rooms currently in
> use. **For each meeting, look at the room that frees earliest: if it is free by now, reuse it; otherwise open
> a new room.** Then push this meeting's end time with whichever room it got.
>
> **The heap's maximum size is the number of rooms**, which agrees with the sweep's answer — **and that
> agreement is a free consistency check I would actually run**, because if the two disagree it is almost
> always because their tie-break conventions differ.
>
> **The condition is `free[0][0] <= start`** — a room freed at four is reusable at four — **and it must match
> the sweep's convention exactly.**
>
> **Cost: `O(n log n)` for the sort plus `O(n log k)` for the heap operations, where `k` is the number of
> rooms.** Same complexity as the sweep, **and `O(k)` space rather than `O(n)`, which is often much smaller.**
>
> **So the honest comparison is: the heap gives strictly more information at the same complexity.** **The
> sweep's only advantages are that it is simpler and has constant working state** — and if the question only
> asks for a count, simpler is worth something.
>
> **One product note: 'reuse the earliest-freeing room' produces a valid assignment and not a nice one.**
> Meetings hop between rooms in a way that looks arbitrary. **If the requirement is that a series should stay
> in one room, that is a different and harder problem**, and worth asking about rather than assuming."

**"Given buildings with heights, produce the skyline."**

> "This is the same sweep with one thing changed, **and saying that is what makes a Hard problem approachable
> rather than a new algorithm to learn.**
>
> **The framework is identical: break each building into two events — one where it begins and one where it
> ends — sort them by position, and walk through maintaining an accumulator.**
>
> **What changes is the accumulator.** For meeting rooms it is a running sum, and an integer suffices.
> **Here the outline at any point is the *maximum* height among the buildings currently active** — so I need a
> structure that can give me the maximum, add a height, and remove a height.
>
> **A max-heap gives me the maximum and insertion cheaply, and it cannot remove an arbitrary element** — which
> is the problem, because when a building ends I need to take its height out.
>
> **The answer is lazy deletion.** Store `(height, right_edge)` in the heap. **When I look at the top, first
> discard anything whose right edge is already behind me.** Expired entries stay in the heap until they surface
> and are then dropped.
>
> **That keeps it `O(n log n)`, because every entry is pushed once and popped at most once** — even though the
> heap can temporarily hold entries that are no longer relevant.
>
> **Without lazy deletion the usual mistake is a linear scan to remove the element**, which is `O(n)` per event
> and `O(n²)` overall.
>
> **Two details.** **Sort so that taller buildings come first at the same position** — encoding the height as
> negative does that — **so that when several buildings start together the outline jumps straight to the
> tallest.** **And emit a point only when the current maximum actually changes**, or the output is full of
> duplicate heights.
>
> **A ground plane in the heap — height zero with an infinite right edge — removes the empty-heap special
> case**, which is a small thing that removes a whole branch.
>
> **The framing I would give first, though, is the one sentence: it is the meeting-rooms sweep with `max`
> instead of `+`.**"

### The model answer

*"You run a car park with a single entrance. You have a log of every vehicle's arrival and departure time for
the last month. Tell me how many spaces you actually needed, when the peak was, and how much of the day the
car park was completely empty."*

> "Three questions, and **all three are one sweep** — which is worth saying up front, because it means I write
> one pass and read three answers out of it.
>
> **The key move is that I do not care which car is which.** The log pairs arrivals with departures, **and for
> all three questions I can throw that pairing away.** What I need is a list of times, each marked as an
> arrival or a departure.
>
> **So: plus one at every arrival, minus one at every departure, sorted by time, one pass with a running
> total.**
>
> **Question one — how many spaces — is the maximum the running total reaches.**
>
> **Question two — when the peak was — is one extra variable**: record the time whenever the running total sets
> a new maximum. **And I would use a strict greater-than so it records the *first* moment the peak occurred**,
> which is what 'when were we busiest' usually means. **Greater-or-equal would report the last, which is a
> defensible different answer** — worth stating rather than choosing silently.
>
> **Question three — how long it was empty — is the sum of the stretches where the running total is zero.**
> And the ordering matters: **the stretch between the previous event and this one had the *previous* count**, so
> I accumulate before applying the delta. **Getting that backwards gives an answer that is close and wrong.**
>
> **The tie-break, which I would settle explicitly.** A car leaves at ten past two and another arrives at ten
> past two: **is that one space or two?** For a car park, one — **the space is freed and taken.** So at equal
> times, **process the departure first**, which sorting `(time, delta)` tuples gives me free because minus one
> sorts before plus one.
>
> **And I would ask about this rather than assume**, because if the log records to the second, exact ties are
> rare and it barely matters; **if it records to the minute, ties are constant and the convention changes the
> answer.**
>
> **Now the sizing, which changes the choice of algorithm.** A month of a busy car park might be a hundred
> thousand vehicles — two hundred thousand events, sorted in a fraction of a second. **The sweep is
> comfortable.**
>
> **But if the times are recorded to the minute, there are only 43,200 minutes in a month** — **and a
> difference array over those minutes is `O(n + 43,200)` rather than `O(n log n)`, and it is simpler.**
> Increment at each arrival minute, decrement at each departure minute, one prefix sum. **At a hundred thousand
> vehicles that is about eighteen times fewer operations.**
>
> **So I would ask what resolution the timestamps have**, because dense small coordinates make the array
> version strictly better — **and reaching for the sweep reflexively there would be over-engineering.**
>
> **Two things I would raise.**
>
> **Work in integers.** If the log has times as floating-point hours, **two events that should be simultaneous
> get ordered by rounding error and the tie-break never applies.** Convert to minutes or seconds on the way in.
>
> **And if they later ask which space each car was in** — for a numbered car park — **the sweep cannot answer,
> because it discarded exactly that.** That is a min-heap of space-free times: reuse the earliest-freeing space
> if it is free, otherwise open a new one. **Same complexity, and the heap's size agrees with the sweep's
> answer**, which is a consistency check worth running once."

---

## 9. Recall card

**The sweep is a COUNTING technique, and the idea is to discard which interval is which.** Break each into
`+1` at the start and `-1` at the end, **throw away the association**, sort by time, and take the running
maximum. Six lines. **"How many at once" and "which one is which" are different questions, and the first is far
easier.**

**The tie-break is where half of implementations are wrong.** For meeting rooms, an end at time 4 must be
processed **before** a start at 4 — the room is freed and reused, giving one room, not two. **Sorting
`(time, delta)` tuples gives this for free** because `-1 < +1`. **Getting it backwards is exactly one too high
on abutting meetings**, which is what every real calendar looks like. **Never encode events as strings** —
`"end" < "start"` is a coincidence of the alphabet — **and work in integers**, because floating-point times
destroy the tie entirely.

**Two equivalent forms:** the event list (tie-break in the sort key) and **two pointers over sorted starts and
ends** (tie-break visible as `<` against `<=`). Same answer, same complexity.

**The sweep cannot give the ASSIGNMENT** — it discarded it, which is what made it cheap. **For "which room",
use a min-heap of end times**: reuse the earliest-freeing room if free, else open a new one. Same `O(n log n)`,
`O(k)` space, **and the heap's size agrees with the sweep — a free consistency check** (they disagree only when
their conventions differ).

**It is a framework: sort events, walk, accumulate — only the ACCUMULATOR changes.** Count → integer; weighted
(bandwidth) → `+w`/`-w`; total covered → sum the stretches while the count is positive (**accumulate BEFORE
applying the delta**); **the SKYLINE → `max` instead of `+`, so the accumulator becomes a heap with LAZY
DELETION** (leave expired entries in, discard them when they surface — each popped once, so still
`O(n log n)`).

**And when the coordinate space is small and dense, a difference array beats the sweep** — `O(n + horizon)`
against `O(n log n)`, ~18× faster for 10,000 meetings over 1,440 minutes. **Compare `horizon` against
`n log n` before choosing.**
