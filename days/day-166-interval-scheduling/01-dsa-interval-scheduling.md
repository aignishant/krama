---
day: 166
track: dsa
title: "Interval scheduling"
phase: "Greedy and intervals"
status: written
---

# Interval scheduling

## 1. What this is, and why they ask it

**An interval is a pair of numbers: a start and an end.** Interval problems ask you to select, merge, count or
schedule them, and there are perhaps eight of them that appear over and over.

They ask it because **it is the highest-density topic in the interview canon.** Eight problems, three
techniques, and the techniques are short — **so the whole family is learnable in a day and it appears in
almost every interview loop.**

The other reason is that **the first move is always the same and it is where the marks are.** **Sort.** And the
entire difficulty is **sort by what** — because start, end and duration all seem plausible, **and which one is
correct depends on the question in a way that is not obvious.**

```
   "how many can I fit?"                  sort by END
   "merge the overlapping ones"           sort by START
   "how many rooms do I need?"            neither — sweep the endpoints
```

**Three questions, three different answers, and they read almost identically.** A candidate who sorts by end
time reflexively gets the merging problem wrong; **a candidate who sorts by start time reflexively gets the
selection problem wrong**, and both produce plausible numbers with no error.

And there is a third reason worth naming: **intervals are where greedy and DP sit next to each other.**
Unweighted selection is greedy and `O(n log n)`. **Add a value to each interval and greedy breaks and it
becomes DP — at the same `O(n log n)`, because the sort dominates both.** That pair is the cleanest
demonstration in the course of yesterday's lesson.

By the end of this lesson you can classify any interval problem into one of the three techniques, know which
sort each needs and why, handle the boundary conventions, and recognise the weighted variant that turns greedy
into DP.

---

## 2. The story

The community hall had one room and Padmavathi kept the diary, and in eleven years she had worked out that
there were only ever three arguments.

**The first was about how many things she could fit in.**

Somebody would want the hall on Saturday afternoon, and somebody else, and a third person, and their times
overlapped in a tangle. **And she had learned — badly, over about two years — that you do not start with the
big bookings.**

The wedding reception wanted two till nine. **If she said yes to that, the whole afternoon was gone for one
booking.** Whereas the naming ceremony from two till four, and the meeting from four till six, and the class
from six till seven-thirty — **three bookings in the same space.**

**So her rule was: whoever finishes first.** Not whoever asks first. Not the shortest. **Whoever gives the room
back soonest.**

**The second argument was completely different and she kept confusing it with the first.**

The committee wanted to know **when the hall was busy** — not how many bookings, but which stretches of the
day were occupied at all, so they could plan the cleaning.

And for that, **finishing first was the wrong thing to look at entirely.** She had to go through the bookings
**in the order they started**, and run a finger along, joining anything that touched.

*Two till four, and four till six — that is one stretch, two till six.* *Then nothing until seven.*

**Three arguments, and the third one took her the longest to see was different at all.**

Because after the extension there were three rooms, and the question changed to **"can we take all of these,
and how many rooms do we need at once".**

And here neither of the first two rules helped, **because she did not care which booking was which.** She only
cared **how many were happening at the same time.**

What she ended up doing was writing every start and every end on separate slips — **just the times, not whose
booking they were** — putting them all in order, and walking down the list. **Plus one for a start, minus one
for an end.** The biggest the running total ever got was the number of rooms she needed.

**"They sound like the same question," her daughter said.**

**"They sound like it," she said. "Fitting the most in, joining up what touches, and counting how many at
once. I did the first one's method on the second one's question for a year and a half."**

---

## 3. The idea in plain English

Padmavathi's three arguments are the three techniques, and her last sentence is the reason this topic is worth
a whole day: **the questions sound identical and the methods share nothing.**

**Start with the classification, because it is the whole lesson.**

```
   QUESTION                                TECHNIQUE           SORT BY
   -------------------------------------------------------------------
   maximum number of non-overlapping       greedy select       END
   minimum removals to make disjoint       greedy select       END
                                           (the same problem)
   merge overlapping intervals             merge               START
   insert an interval into a sorted list   merge               (already sorted)
   do any two overlap?                     merge               START
   minimum rooms / maximum concurrent      sweep line          endpoints
   busiest time / peak load                sweep line          endpoints
   maximum VALUE of non-overlapping        DP                  END
```

**Three techniques. Learn which question maps to which, and the code is short.**

**Technique one: greedy selection. Sort by END time.**

**The question is "how many can I fit".** Sort by end time, keep a running `last_end`, and take any interval
that starts at or after it.

**Why end time is the correct key** is yesterday's exchange argument: **the only thing about an interval that
constrains the future is when the resource becomes free**, and finishing earliest leaves the most room.

**And "minimum removals to make them disjoint" is the same problem**: `n` minus the maximum you can keep.
**Recognising that saves you from writing a second algorithm** — LeetCode asks it both ways.

**Technique two: merging. Sort by START time.**

**The question is "join up what touches".** Sort by start, then walk through: **if the next interval starts
before the current one ends, extend the current one; otherwise close it and begin a new one.**

**Sorting by start is what makes the single pass work.** With intervals in start order, **anything that
overlaps the current merged block must start before its end** — so one comparison per interval decides it.
**Sorted by end, that property does not hold** and the algorithm is wrong.

**And the one line people get wrong is the extension:** `current_end = max(current_end, next_end)`, **not
`= next_end`.** An interval entirely contained inside the current block would otherwise shrink it.

**Technique three: the sweep line. Sort the endpoints, not the intervals.**

**The question is "how many at once".** And the key move is that **you stop caring which interval is which.**

**Break every interval into two events** — a start and an end — **throw away the association**, sort all the
events by time, and walk through with a counter: **plus one on a start, minus one on an end.** The maximum the
counter reaches is the answer.

**That decomposition is the idea.** "Minimum meeting rooms" sounds like a scheduling problem and is a counting
problem, **and once the intervals become independent events it is six lines.**

**And there is an equivalent formulation worth knowing**: **sort the starts and the ends into two separate
arrays and merge them with two pointers.** Same answer, and some people find it clearer.

**Now the boundary convention, which is the most common bug in the whole topic.**

**Does an interval ending at 4 conflict with one starting at 4?**

**For meeting rooms: no.** One meeting ends and the next begins; the room is free.
**For "do these two number ranges overlap": possibly yes**, depending on whether the ranges are inclusive.

**It is one comparison — `>=` against `>`** — and **the problem statement decides it.** **Ask, and say which
you assumed.** In the sweep line it appears as the tie-break: **when a start and an end share a time, process
the END first** if touching intervals do not conflict.

**Getting that backwards gives an answer exactly one too high**, on inputs where meetings abut — which is most
realistic inputs.

**Then the fourth thing, which is the greedy-to-DP transition.**

**Unweighted selection is greedy.** Add a value to each interval — **"maximise total value, not count" — and
greedy fails**, because one valuable long interval can beat three cheap short ones and no local rule sees it.

**That is weighted interval scheduling, and it is DP:**

```
   sort by end time
   dp[i] = max( dp[i-1],                          skip interval i
                value[i] + dp[ p(i) ] )           take it
   where p(i) = the last interval that ends before interval i starts
```

**And `p(i)` is a binary search over the sorted end times**, which keeps the whole thing `O(n log n)` — **the
same complexity as the greedy version, because both are dominated by the sort.**

**That is the point worth making out loud: greedy failing here costs you a table and some code, and nothing
asymptotically.**

**Finally: the representation details that cause real bugs.**

**Sorting tuples in Python sorts lexicographically**, so `sorted(intervals)` sorts by start and then by end —
**which is what you want for merging and not for selection.** Being explicit with `key=` says which you meant.

**And `sorted()` rather than `.sort()`**, unless mutating the caller's list is intended.

---

## 4. The picture

The three questions, on the same input:

```
   intervals:   [1,4] [2,5] [7,9] [3,6]

   drawn:       1---4
                 2----5
                  3----6
                             7--9

   Q1: MAXIMUM NON-OVERLAPPING?          -> 2   ([1,4] and [7,9])
   Q2: MERGED into blocks?               -> [1,6] and [7,9]
   Q3: MAXIMUM CONCURRENT (rooms)?       -> 3   (at time 3.5)

   THREE ANSWERS. THREE ALGORITHMS. THREE SORT KEYS.
   And the questions read almost identically.
```

Technique one: greedy selection, sorted by END:

```
   sorted by end:  [1,4] [2,5] [3,6] [7,9]

   take [1,4]                    last_end = 4
   [2,5] starts at 2 < 4         skip
   [3,6] starts at 3 < 4         skip
   [7,9] starts at 7 >= 4        take     last_end = 9

   answer 2

   WHY END TIME: the only thing that constrains the future is when
   the resource becomes free. Finishing earliest leaves the most room.

   SORTED BY START instead:
     take [1,4], skip [2,5], skip [3,6], take [7,9]  -> 2 here
   but on [0,10] [1,2] [3,4] [5,6]:
     by start:  take [0,10] -> blocks everything     -> 1
     by end:    take [1,2] [3,4] [5,6]               -> 3
```

Technique two: merging, sorted by START:

```
   sorted by start: [1,4] [2,5] [3,6] [7,9]

   current = [1,4]
   [2,5]: starts at 2 <= 4    -> extend: current = [1, max(4,5)] = [1,5]
   [3,6]: starts at 3 <= 5    -> extend: current = [1, max(5,6)] = [1,6]
   [7,9]: starts at 7 >  6    -> close [1,6], current = [7,9]

   answer [1,6] [7,9]

   THE LINE PEOPLE GET WRONG:
     current_end = max(current_end, next_end)     CORRECT
     current_end = next_end                       WRONG

   on [1,10] [2,3]:  correct gives [1,10]; wrong gives [1,3]
   -> an interval CONTAINED in the current block would shrink it
```

Technique three: the sweep line — stop caring which interval is which:

```
   intervals:  [1,4] [2,5] [3,6] [7,9]

   BREAK INTO EVENTS, discarding the association:

     +1 at 1     +1 at 2     +1 at 3     +1 at 7
     -1 at 4     -1 at 5     -1 at 6     -1 at 9

   SORT ALL EVENTS BY TIME:
     1:+1   2:+1   3:+1   4:-1   5:-1   6:-1   7:+1   9:-1

   WALK, keeping a running total:
     1: 1
     2: 2
     3: 3   <- the maximum
     4: 2
     5: 1
     6: 0
     7: 1
     9: 0

   answer 3 rooms

   THE IDEA: "minimum meeting rooms" sounds like scheduling and is
   COUNTING. Once the intervals become independent events, it is
   six lines.
```

The boundary convention, which is the commonest bug:

```
   meeting A: [2, 4]        meeting B: [4, 6]

   DO THEY CONFLICT?

   MEETING ROOMS: no — one ends as the other begins, the room is free
     -> selection uses  start >= last_end
     -> the sweep processes the END before the START at time 4

   INCLUSIVE RANGES: possibly yes — both occupy the point 4
     -> selection uses  start > last_end
     -> the sweep processes the START before the END

   IT IS ONE COMPARISON, AND THE PROBLEM STATEMENT DECIDES IT.

   Getting it backwards gives an answer exactly ONE too high,
   on inputs where intervals abut — which is most real inputs.
```

Where greedy stops and DP begins:

```
   UNWEIGHTED — greedy by end time

     [0,10]  [0,3]  [3,6]  [6,9]
     answer: 3 intervals

   WEIGHTED — greedy FAILS

     [0,10] worth 100
     [0,3] worth 10, [3,6] worth 10, [6,9] worth 10

     greedy by end time: takes the three short ones  -> 30
     optimal:            takes the long one          -> 100

   -> weighted interval scheduling is DP:

      sort by end time
      dp[i] = max( dp[i-1],  value[i] + dp[p(i)] )
      p(i) = last interval ending before interval i starts
             (found by BINARY SEARCH over the sorted end times)

      O(n log n) — THE SAME as the greedy version, because both
      are dominated by the sort.

   -> greedy failing here costs a table, not a worse complexity.
```

---

## 5. The code, built step by step

### Greedy selection: sort by end

```python
def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    """
    How many can I fit? Sort by END time.

    EXCHANGE ARGUMENT: swapping in the earliest finisher cannot create
    a conflict, because it ends no later than whatever it replaced.
    """
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:                 # >= : touching is fine
            count += 1
            last_end = end
    return count


def min_removals(intervals: list[tuple[int, int]]) -> int:
    """The SAME problem: n minus the most you can keep."""
    return len(intervals) - max_non_overlapping(intervals)
```

**`min_removals` being one line is the point.** LeetCode asks this both ways — **452 and 435 are the same
algorithm** — and recognising it saves writing a second one.

### Merging: sort by start

```python
def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Join up what touches. Sort by START.

    Sorted by start, anything overlapping the current block must
    begin before the block ends — so one comparison decides it.
    """
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:            # overlaps or touches
            merged[-1][1] = max(merged[-1][1], end)     # NOT `= end`
        else:
            merged.append([start, end])
    return [tuple(block) for block in merged]
```

**`max(merged[-1][1], end)` is the line that matters.** With `= end`, an interval entirely inside the current
block **shrinks it** — `[1,10]` followed by `[2,3]` becomes `[1,3]`.

**And it is invisible on most test inputs**, because containment is less common than partial overlap.

### The sweep line: sort the endpoints

```python
def min_rooms(intervals: list[tuple[int, int]]) -> int:
    """
    How many at once? Break into EVENTS and forget which interval is which.

    The tie-break matters: at equal times, process the END first,
    because a room freed at 4 can be reused at 4.
    """
    events = []
    for start, end in intervals:
        events.append((start, +1))
        events.append((end, -1))
    events.sort()                             # (time, delta): -1 sorts before +1

    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best
```

**`events.sort()` on `(time, delta)` tuples does the tie-break for free**, because `-1 < +1` — **so at equal
times the end is processed first, which is what "the room is free" means.**

**Swap the signs and you get an answer exactly one too high** on any input where meetings abut.

### The two-pointer form, which some prefer

```python
def min_rooms_two_pointer(intervals: list[tuple[int, int]]) -> int:
    """The same answer: merge the sorted starts and ends."""
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = best = 0
    i = j = 0
    while i < len(starts):
        if starts[i] < ends[j]:               # a meeting begins before one ends
            rooms += 1
            best = max(best, rooms)
            i += 1
        else:
            rooms -= 1
            j += 1
    return best
```

**`starts[i] < ends[j]` rather than `<=` is the same boundary decision**, expressed differently — **and it is
worth writing both forms once to see that they are the same algorithm.**

### The heap form, when you need which room

```python
import heapq

def assign_rooms(intervals: list[tuple[int, int]]) -> list[int]:
    """Which room does each meeting get? A heap of end times."""
    ordered = sorted(range(len(intervals)), key=lambda i: intervals[i][0])
    free: list[tuple[int, int]] = []          # (end_time, room_number)
    assignment = [0] * len(intervals)
    rooms_used = 0
    for i in ordered:
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

**The sweep line counts rooms; the heap assigns them.** **If the question asks which meeting goes where, the
counter is not enough** — and this is the natural follow-up.

### Overlap detection and insertion

```python
def has_overlap(intervals: list[tuple[int, int]]) -> bool:
    """Sort by start; adjacent pairs are the only ones that can conflict."""
    ordered = sorted(intervals, key=lambda x: x[0])
    return any(ordered[i][1] > ordered[i + 1][0] for i in range(len(ordered) - 1))


def insert_interval(intervals: list[tuple[int, int]],
                    new: tuple[int, int]) -> list[tuple[int, int]]:
    """Already sorted and disjoint: three phases, no re-sort. O(n)."""
    result: list[tuple[int, int]] = []
    start, end = new
    i, n = 0, len(intervals)

    while i < n and intervals[i][1] < start:  # entirely before
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:   # overlapping: absorb
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append((start, end))
    result.extend(intervals[i:])              # entirely after
    return result
```

**`insert_interval` is `O(n)` because the input is already sorted**, and sorting it again would be `O(n log n)`
— **a small thing, and it is exactly what the problem is testing.**

**The three phases — before, overlapping, after — are the whole structure**, and writing them as three loops
rather than one loop with branches is what makes it readable.

### Weighted interval scheduling: where greedy fails

```python
import bisect

def max_weight_intervals(intervals: list[tuple[int, int, int]]) -> int:
    """
    (start, end, value). Greedy FAILS: one valuable long interval can
    beat three cheap short ones. This is DP, and still O(n log n).
    """
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda x: x[1])       # by END
    ends = [e for _, e, _ in ordered]

    dp = [0] * (len(ordered) + 1)
    for i, (start, _, value) in enumerate(ordered, start=1):
        # p = the last interval that ends at or before this one starts
        p = bisect.bisect_right(ends, start, 0, i - 1)
        dp[i] = max(dp[i - 1], value + dp[p])
    return dp[-1]
```

**`bisect_right(ends, start)` is what keeps this `O(n log n)`** — a linear scan for the last compatible
interval would make it quadratic.

**And `dp[i] = max(skip, take)` is the standard two-branch recurrence**, which after a month of dynamic
programming needs no explanation — **the interesting part is that it costs the same as the greedy version.**

### The complete solution

```python
"""Interval scheduling: three techniques, and which question needs which."""

import bisect
import heapq


# ---------- technique 1: greedy selection, sort by END ----------

def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    """How many can I fit? EXCHANGE: the earliest finisher ends no later."""
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count


def min_removals(intervals: list[tuple[int, int]]) -> int:
    """The same problem, phrased as a subtraction."""
    return len(intervals) - max_non_overlapping(intervals)


# ---------- technique 2: merging, sort by START ----------

def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Join what touches. `max` on the extension, never `=`."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


def has_overlap(intervals: list[tuple[int, int]]) -> bool:
    ordered = sorted(intervals, key=lambda x: x[0])
    return any(ordered[i][1] > ordered[i + 1][0] for i in range(len(ordered) - 1))


def insert_interval(intervals: list[tuple[int, int]],
                    new: tuple[int, int]) -> list[tuple[int, int]]:
    """Input already sorted and disjoint -> O(n), three phases."""
    result: list[tuple[int, int]] = []
    start, end = new
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start, end = min(start, intervals[i][0]), max(end, intervals[i][1])
        i += 1
    result.append((start, end))
    result.extend(intervals[i:])
    return result


# ---------- technique 3: the sweep line, sort the ENDPOINTS ----------

def min_rooms(intervals: list[tuple[int, int]]) -> int:
    """How many at once? (time, delta) sorting puts -1 before +1 at ties."""
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


def min_rooms_two_pointer(intervals: list[tuple[int, int]]) -> int:
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


def assign_rooms(intervals: list[tuple[int, int]]) -> list[int]:
    """The sweep COUNTS rooms; a heap ASSIGNS them."""
    ordered = sorted(range(len(intervals)), key=lambda i: intervals[i][0])
    free: list[tuple[int, int]] = []
    assignment = [0] * len(intervals)
    rooms_used = 0
    for i in ordered:
        start, end = intervals[i]
        if free and free[0][0] <= start:
            _, room = heapq.heappop(free)
        else:
            rooms_used += 1
            room = rooms_used
        assignment[i] = room
        heapq.heappush(free, (end, room))
    return assignment


# ---------- the weighted version: DP, same complexity ----------

def max_weight_intervals(intervals: list[tuple[int, int, int]]) -> int:
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda x: x[1])
    ends = [e for _, e, _ in ordered]
    dp = [0] * (len(ordered) + 1)
    for i, (start, _, value) in enumerate(ordered, start=1):
        p = bisect.bisect_right(ends, start, 0, i - 1)
        dp[i] = max(dp[i - 1], value + dp[p])
    return dp[-1]


def max_weight_greedy(intervals: list[tuple[int, int, int]]) -> int:
    """The greedy that fails, for comparison."""
    total, last_end = 0, float("-inf")
    for start, end, value in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            total += value
            last_end = end
    return total


# ---------- the wrong sort keys, to see them fail ----------

def max_non_overlapping_by_start(intervals: list[tuple[int, int]]) -> int:
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[0]):
        if start >= last_end:
            count, last_end = count + 1, end
    return count


def merge_by_end(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merging with the WRONG sort key."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[1])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(b) for b in merged]


if __name__ == "__main__":
    ivs = [(1, 4), (2, 5), (3, 6), (7, 9)]
    print("THE SAME INPUT, THREE QUESTIONS")
    print("  intervals            :", ivs)
    print("  max non-overlapping  :", max_non_overlapping(ivs))
    print("  merged               :", merge(ivs))
    print("  minimum rooms        :", min_rooms(ivs))
    print("  two-pointer agrees   :", min_rooms_two_pointer(ivs))
    print("  room assignment      :", assign_rooms(ivs))

    print("\nTHE WRONG SORT KEY")
    blocking = [(0, 10), (1, 2), (3, 4), (5, 6)]
    print("  input                :", blocking)
    print("  by END   (correct)   :", max_non_overlapping(blocking))
    print("  by START (wrong)     :", max_non_overlapping_by_start(blocking))

    contained = [(1, 10), (2, 3), (11, 12)]
    print("  merge by START (right):", merge(contained))
    print("  merge by END   (wrong):", merge_by_end(contained))

    print("\nTHE BOUNDARY CONVENTION")
    abutting = [(1, 4), (4, 6), (6, 9)]
    print("  abutting meetings    :", abutting)
    print("  rooms needed         :", min_rooms(abutting), "(ends before starts)")
    print("  max non-overlapping  :", max_non_overlapping(abutting))

    print("\nGREEDY BREAKS WHEN VALUES APPEAR")
    weighted = [(0, 10, 100), (0, 3, 10), (3, 6, 10), (6, 9, 10)]
    print("  weighted intervals   :", weighted)
    print("  greedy by end time   :", max_weight_greedy(weighted))
    print("  DP (correct)         :", max_weight_intervals(weighted))

    print("\nINSERTION INTO A SORTED LIST")
    sorted_disjoint = [(1, 3), (6, 9)]
    print("  insert (2,5) into", sorted_disjoint, "->",
          insert_interval(sorted_disjoint, (2, 5)))
    print("  insert (4,5) into", sorted_disjoint, "->",
          insert_interval(sorted_disjoint, (4, 5)))
```

Run it and you get:

```
THE SAME INPUT, THREE QUESTIONS
  intervals            : [(1, 4), (2, 5), (3, 6), (7, 9)]
  max non-overlapping  : 2
  merged               : [(1, 6), (7, 9)]
  minimum rooms        : 3
  two-pointer agrees   : 3
  room assignment      : [1, 2, 3, 1]

THE WRONG SORT KEY
  input                : [(0, 10), (1, 2), (3, 4), (5, 6)]
  by END   (correct)   : 3
  by START (wrong)     : 1
  merge by START (right): [(1, 10), (11, 12)]
  merge by END   (wrong): [(2, 10), (11, 12)]

THE BOUNDARY CONVENTION
  abutting meetings    : [(1, 4), (4, 6), (6, 9)]
  rooms needed         : 1 (ends before starts)
  max non-overlapping  : 3

GREEDY BREAKS WHEN VALUES APPEAR
  weighted intervals   : [(0, 10, 100), (0, 3, 10), (3, 6, 10), (6, 9, 10)]
  greedy by end time   : 30
  DP (correct)         : 100

INSERTION INTO A SORTED LIST
  insert (2,5) into [(1, 3), (6, 9)] -> [(1, 5), (6, 9)]
  insert (4,5) into [(1, 3), (6, 9)] -> [(1, 3), (4, 5), (6, 9)]
```

**The first block is the whole lesson in four lines**: the same four intervals give **2, two merged blocks, and
3 rooms** — three different answers to three questions that read almost the same.

**`by START (wrong) : 1` against `by END (correct) : 3`** is the sort key made visible. **And the merge-by-end
block starts at 2 rather than 1** — it began with `[2,3]`, absorbed `[1,10]`, and **silently discarded the
start of the very interval it was merging.** The two techniques are not interchangeable, and the failure is a
quiet wrong number rather than a crash.

**And `greedy 30 against DP 100`** is yesterday's lesson in one line: **adding values breaks greedy, and the DP
that replaces it is the same complexity.**

---

## 6. What it costs

**All three techniques are dominated by the sort.**

```
   greedy selection    sort O(n log n) + one pass O(n)      = O(n log n)
   merging             sort O(n log n) + one pass O(n)      = O(n log n)
   sweep line          sort 2n events O(n log n) + one pass = O(n log n)
   weighted DP         sort + n binary searches             = O(n log n)

   ALL FOUR ARE O(n log n), AND THE SORT IS THE WHOLE COST.
```

**Which means the interesting comparison is not between the techniques — it is against the naive versions:**

```
   "do any two overlap?"
     naive: check every pair                O(n^2)
     sorted: adjacent pairs only            O(n log n)
     n = 100,000: 10^10 against 1.7 x 10^6  -> ~6,000x

   "maximum concurrent"
     naive: for each interval, count overlaps   O(n^2)
     sweep line                                 O(n log n)
     same ratio
```

**Space:**

```
   greedy selection    O(1) beyond the sort — two variables
   merging             O(n) for the output
   sweep line          O(n) for the events (2n of them)
   weighted DP         O(n) for the table
   heap assignment     O(k) where k is the number of rooms
```

**Concretely, at realistic sizes:**

```
   n = 1,000        sorting: microseconds. Everything is instant.
   n = 100,000      sort ~0.1 s in Python; the pass ~0.02 s
   n = 10,000,000   sort ~15 s in Python; still linear afterwards

   -> intervals scale well. The techniques are all one sort plus
      one pass, and nothing here has a hidden quadratic.
```

**The sweep line's constant factor:**

```
   2n events instead of n intervals
   -> twice the sorting work

   the two-pointer form sorts two arrays of n instead of one of 2n
   -> n log n + n log n against 2n log(2n)
   -> marginally better, and the same complexity

   in practice: use whichever you find clearer. The difference is
   under 10%.
```

**Weighted DP against unweighted greedy, which is the point:**

```
   unweighted greedy    O(n log n) time, O(1) space
   weighted DP          O(n log n) time, O(n) space

   -> the SAME time complexity, because both are dominated by
      the sort.

   The DP costs:
     one array of n
     a binary search per interval (log n each)

   -> greedy failing here is a table and about eight lines,
      not an asymptotic penalty. That is unusual and worth knowing.
```

**Binary search versus linear scan for `p(i)`:**

```
   linear scan backwards for the last compatible interval:
     worst case O(n) per interval -> O(n^2) overall
     n = 100,000 -> 10^10. Not viable.

   bisect over the sorted end times:
     O(log n) per interval -> O(n log n)
     n = 100,000 -> 1.7 million. Instant.

   -> the binary search is not an optimisation; it is what makes
      the weighted version tractable.
```

**And the cost of the wrong sort key, which is not a performance cost:**

```
   sorting by start instead of end:  SAME complexity, WRONG answer
   sorting by end instead of start:  SAME complexity, WRONG answer

   -> there is no performance signal to warn you.
      Both run in O(n log n) and both return a plausible number.
```

---

## 7. The traps

**The wrong sort key for selection.**

```python
>>> intervals = [(0, 10), (1, 2), (3, 4), (5, 6)]
>>> max_non_overlapping(intervals)              # by end
3
>>> max_non_overlapping_by_start(intervals)     # by start
1
```

**Three against one.** The long interval starts earliest and blocks everything. **Same complexity, no error,
and the answer is a third of the correct one.**

**The wrong sort key for merging.**

```python
>>> merge([(1, 10), (2, 3), (11, 12)])          # by start
[(1, 10), (11, 12)]
>>> merge_by_end([(1, 10), (2, 3), (11, 12)])   # by end
[(2, 10), (11, 12)]
```

**The block starts at 2 rather than 1.** Sorted by end, the pass began with `[2,3]`, then absorbed `[1,10]` by
extending the *end* — **and there is no code path that reaches backwards to fix the start.** **The count is
right and the answer is wrong**, so a test checking only the number of blocks passes.

**`= end` instead of `max(current_end, end)` when merging.**

```python
>>> # merging [(1,10), (2,3)] with `current_end = end`:
>>> # [1,10] then [2,3] starts at 2 <= 10, so extend to end=3
>>> # -> [(1, 3)]   WRONG: the block SHRANK
```

**An interval contained entirely within the current block shrinks it.** **Containment is less common than
partial overlap in test data**, which is exactly why this survives.

**The boundary convention, backwards.**

```python
>>> min_rooms([(1, 4), (4, 6), (6, 9)])
1
>>> # with the sweep processing STARTS before ENDS at equal times:
>>> # -> 2, because the room is counted as occupied at time 4
```

**One too high**, on the most realistic input there is — meetings that abut. **The `(time, delta)` sort gives
the right convention for free because `-1 < +1`**, and writing the events as `(time, "start")` and
`(time, "end")` gets it backwards, because `"end" < "start"` alphabetically happens to be right and
`"begin" < "finish"` would not be. **Use numbers.**

**Assuming the answer is a count when it is an assignment.**

```python
>>> min_rooms([(1, 4), (2, 5), (3, 6), (7, 9)])
3
>>> assign_rooms([(1, 4), (2, 5), (3, 6), (7, 9)])
[1, 2, 3, 1]
```

**The sweep line tells you how many rooms and cannot tell you which meeting goes where.** **If the question
asks for the assignment, you need the heap** — and that is the standard follow-up.

**Re-sorting an already sorted input.**

```python
>>> # "insert an interval into a sorted, disjoint list"
>>> # sorting again: O(n log n)
>>> # the three-phase scan: O(n)
>>> # -> the problem is TESTING whether you noticed
```

**The input being sorted is stated in the problem and is the whole point.**

**Greedy on the weighted version.**

```python
>>> weighted = [(0, 10, 100), (0, 3, 10), (3, 6, 10), (6, 9, 10)]
>>> max_weight_greedy(weighted)
30
>>> max_weight_intervals(weighted)
100
```

**Thirty against a hundred.** **One word in the problem statement — "number" against "value" — changes the
algorithm entirely**, and greedy passes every unweighted test.

**Linear search for the compatible interval in the DP.**

```python
>>> # scanning backwards for the last interval ending before this starts:
>>> # O(n) per interval -> O(n^2) overall
>>> # n = 100,000 -> 10^10 operations
```

**No error, and it does not finish.** **The binary search is what makes the weighted version tractable**, not a
tidy-up.

**Mutating the caller's list.**

```python
>>> data = [(3, 5), (1, 4)]
>>> # if merge used data.sort() rather than sorted(data):
>>> data
[(1, 4), (3, 5)]              # reordered, silently
```

**`sorted()` unless you mean to reorder the input** — and saying "I will not mutate the input" costs two words
and is a small, real signal.

---

## 8. In the interview

### How it gets asked

- *"Merge overlapping intervals."* — LeetCode 56, the most-asked of the family.
- *"How many meeting rooms do you need?"* — LeetCode 253, the sweep line.
- *"What is the maximum number of non-overlapping intervals?"* — LeetCode 435, greedy.
- *"Insert an interval into a sorted list."* — LeetCode 57, and it tests whether you re-sort.
- *"Do the meetings conflict?"* — the easy opener.
- *"Now each meeting has a value."* — the greedy-to-DP transition.

### The first ninety seconds

> "Interval problems all start the same way — **sort** — and the entire difficulty is **sort by what**, because
> start, end and duration all seem plausible and the right answer depends on the question.
>
> **There are three techniques and I would classify the problem before writing anything.**
>
> **If the question is 'how many can I fit', it is greedy, sorted by END time.** Keep a running last-end and
> take anything that starts at or after it. **End time is correct because the only thing about an interval that
> constrains the future is when the resource becomes free** — finishing earliest leaves the most room. **And
> 'minimum removals to make them disjoint' is the same problem**, phrased as `n` minus the answer.
>
> **If the question is 'merge what overlaps', it is a single pass, sorted by START.** With intervals in start
> order, anything overlapping the current block must begin before that block ends — **so one comparison per
> interval decides it.** Sorted by end, that property does not hold and the algorithm is simply wrong.
>
> **If the question is 'how many at once' — meeting rooms, peak concurrency — it is a sweep line, and the key
> move is that you stop caring which interval is which.** Break each into two events, plus one at the start and
> minus one at the end, sort all the events by time, and take the running maximum. **A scheduling-sounding
> question turns into a counting problem, and it is six lines.**
>
> **One thing I would settle before coding: does an interval ending at four conflict with one starting at
> four?** For meeting rooms, no — the room is free. **It is one comparison, the problem decides it, and getting
> it backwards gives an answer exactly one too high** on inputs where meetings abut, which is most real
> inputs.
>
> **All three are `O(n log n)`, dominated by the sort**, and `O(1)` to `O(n)` space.
>
> **And I would ask one question: do the intervals have values, or am I just counting them?** Because with
> values greedy breaks and it becomes dynamic programming — **at the same `O(n log n)`, since the sort dominates
> both.**"

### The follow-ups

**"Why sort by end time here and by start time for merging?"**

> "Because the two algorithms need different things to be true, and each sort key establishes exactly one of
> them.
>
> **For selection, sorting by end time is what makes the greedy choice safe.** The exchange argument: take any
> optimal selection and its first interval; the earliest-finishing interval ends no later, **so swapping it in
> cannot create a conflict with anything that came after** — and the count is unchanged. **So some optimal
> solution contains the greedy choice.**
>
> **And the intuition behind that: the only property of an interval that constrains the future is when it
> releases the resource.** Not when it starts, not how long it is. So take the one that releases soonest.
>
> **Sorting by start fails immediately** — one interval from zero to ten starts earliest and blocks the whole
> range. Greedy gets one where the answer is three.
>
> **For merging, sorting by start establishes a different property**: that anything overlapping the current
> merged block must *begin* before the block ends. **That is what makes a single comparison per interval
> sufficient** — I never have to look backwards.
>
> **Sorted by end, that property does not hold.** An interval can begin before the current block and end after
> everything I have seen, and I would miss the overlap. **And the output is not even sorted, which is a good
> way to notice.**
>
> **So it is not that one key is 'better'** — each establishes the invariant its algorithm depends on. **When I
> pick a sort key I try to say what invariant it gives me**, and if I cannot, I have not understood the
> algorithm.
>
> **One implementation note: in Python, `sorted(intervals)` sorts lexicographically — by start, then end.**
> That happens to be right for merging and wrong for selection, **so I write the `key=` explicitly either way**,
> because it says which I meant."

**"How many meeting rooms do you need?"**

> "This sounds like the selection problem and it is a different question entirely, **and the key move is that
> you stop caring which meeting is which.**
>
> **I do not need to know that meeting A is in room two. I need to know how many meetings are happening at the
> busiest moment.** That is a counting problem, not a scheduling one.
>
> **So: break every meeting into two events.** A start event, worth plus one, and an end event, worth minus
> one. **Throw away which meeting they belonged to.** Sort all two-n events by time, walk through with a running
> counter, and take the maximum it reaches.
>
> **Six lines, `O(n log n)` dominated by sorting the events.**
>
> **The detail that matters is the tie-break.** When a meeting ends at four and another starts at four, **the
> end must be processed first** — the room is freed and immediately reused, so it is one room, not two.
>
> **In Python that comes free by sorting `(time, delta)` tuples**, because minus one sorts before plus one.
> **If I encoded the events as strings I would have to think about it**, and getting it backwards gives an
> answer exactly one too high on any input where meetings abut — which is most realistic inputs.
>
> **There is an equivalent form** — sort the starts and the ends into two separate arrays and merge them with
> two pointers — **which some people find clearer and which is the same algorithm.**
>
> **And the natural follow-up: which meeting goes in which room?** **The sweep counts and cannot assign**, so
> for that I would use a min-heap of end times: for each meeting in start order, **reuse the room that frees
> earliest if it is free by now, otherwise open a new one.** The heap size is the number of rooms, which agrees
> with the sweep — and now I also know the assignment."

**"Now each meeting has a value, and you want the maximum total value."**

> "Then greedy breaks, and the demonstration is small enough to give immediately.
>
> **One interval from zero to ten worth a hundred, and three short ones — zero to three, three to six, six to
> nine — worth ten each.** Greedy by end time takes the three short ones for thirty. **The answer is the long
> one, for a hundred.**
>
> **And no local rule fixes it**, because whether to take a long valuable interval depends on what is available
> for the rest of the range, which is exactly the information a greedy choice does not have.
>
> **So it becomes weighted interval scheduling, which is dynamic programming.**
>
> **Sort by end time — the same sort — and let `dp[i]` be the best total value using the first `i` intervals.**
> For each interval, two branches: **skip it, giving `dp[i-1]`; or take it, giving its value plus `dp[p]`,
> where `p` is the last interval that ends before this one starts.**
>
> **And finding `p` is a binary search over the sorted end times**, which is not an optimisation — **a linear
> scan makes it `O(n²)`, which at a hundred thousand intervals is ten to the ten and does not finish.**
>
> **The outcome is the interesting part: `O(n log n)`, exactly the same as the greedy version**, because both
> are dominated by the sort. **So greedy failing here costs me a table and about eight lines and nothing
> asymptotically**, which is unusual — most of the time greedy failing means a real complexity penalty.
>
> **The lesson I would draw out loud: 'maximum number' and 'maximum value' are one word apart in the problem
> statement and are different algorithms.** I read for that word specifically, **because the greedy solution
> passes every unweighted test and silently fails the weighted ones.**"

### The model answer

*"You are building the scheduling backend for a co-working space. Given the day's booking requests, each with
a start time and an end time, answer three questions: which requests can we accept if we have one room, how
many rooms would we need to accept all of them, and what are the busy periods for the cleaning schedule."*

> "Three questions, and **they sound similar and need three completely different algorithms** — so let me take
> them one at a time and say which technique each needs.
>
> **One clarification first, which affects all three: does a booking ending at four conflict with one starting
> at four?** For a room, I would say no — one group leaves, the next arrives. **It is one comparison and I will
> assume touching is fine, and say so.**
>
> **Question one: which requests can we accept with one room?** This is **maximise the number of
> non-overlapping intervals**, which is greedy, **sorted by end time.**
>
> Keep a running last-end and accept any booking that starts at or after it. **End time is correct because the
> only thing that constrains the future is when the room becomes free** — and the exchange argument is that
> swapping in the earliest finisher cannot create a conflict, since it ends no later than whatever it
> replaced.
>
> **I would not sort by start**, because one all-day booking would block everything — greedy would accept one
> where three were possible.
>
> **`O(n log n)`, `O(1)` space beyond the sort, and I would return the actual list rather than the count**,
> since the business needs to know which bookings to confirm.
>
> **Question two: how many rooms to accept all of them?** **A different question entirely** — this is maximum
> concurrency, and it is a **sweep line.**
>
> **The key move is that I stop caring which booking is which.** Break each into a plus-one at its start and a
> minus-one at its end, discard the association, sort all the events, and take the running maximum. **A
> scheduling-sounding question becomes counting, in six lines.**
>
> **And the tie-break is where the bug lives**: at equal times, process the end before the start, because the
> room is freed and reused. **Sorting `(time, delta)` tuples gives that for free, since minus one sorts before
> plus one** — and getting it backwards gives one room too many on exactly the inputs a co-working space
> generates, where bookings abut on the hour.
>
> **And since this is a real business, they will want the assignment too**, not just the count. **For that I
> would use a min-heap of room end times**: process bookings in start order, reuse the earliest-freeing room if
> it is available, otherwise open a new one. **The heap size is the room count, agreeing with the sweep, and
> now every booking has a room number.**
>
> **Question three: the busy periods for cleaning.** This is **merging**, and it is the third technique —
> **sorted by start.**
>
> Walk through in start order; if the next booking begins at or before the current block ends, extend the
> block; otherwise close it and start a new one. **And the extension is `max(current_end, next_end)`, never
> `= next_end`** — a short booking entirely inside a long one would otherwise shrink the block, **which is
> invisible on most test data and wrong.**
>
> **The output is the occupied stretches, and the gaps between them are when the cleaners can work** — which is
> what they actually asked for, so I would return the gaps rather than making them compute the complement.
>
> **All three are `O(n log n)` and dominated by the sort**, so for a day's bookings — hundreds — everything is
> instant.
>
> **Two things I would raise.**
>
> **If the bookings have values — a premium room, or a longer booking worth more — question one changes
> completely.** Greedy fails, because one valuable all-day booking can beat three cheap short ones, **and it
> becomes weighted interval scheduling: DP with a binary search, still `O(n log n)`.** **I would ask whether
> acceptance is by count or by revenue, because that single word changes the algorithm.**
>
> **And I would ask about the multi-room version of question one**, which is neither of the three: **accepting
> as many bookings as possible given three rooms** is a genuinely harder problem than any of these, and I would
> not want to discover that assumption late."

---

## 9. Recall card

**Every interval problem starts with a sort, and the whole difficulty is SORT BY WHAT.** Three questions that
read almost identically need three different keys — and the wrong key gives a plausible answer with no error
and the same complexity.

**"How many can I fit?" → greedy, sort by END.** Take anything starting at or after `last_end`. End time is
correct because **the only thing constraining the future is when the resource becomes free.** "Minimum removals
to make disjoint" is **the same problem**: `n` minus the answer.

**"Merge what overlaps" → one pass, sort by START.** Start order guarantees that anything overlapping the
current block *begins* before it ends, which is what makes one comparison enough. **The extension is
`max(current_end, next_end)`, never `= next_end`** — a contained interval would shrink the block, and
containment is rare in test data.

**"How many at once?" → SWEEP LINE, and the move is to stop caring which interval is which.** Break each into
`+1` at the start and `-1` at the end, sort the events, take the running maximum. **Sorting `(time, delta)`
tuples gives the right tie-break free** (`-1 < +1`), so an end at time 4 is processed before a start at 4 —
getting it backwards is **exactly one too high** on abutting inputs. **The sweep COUNTS; a min-heap of end
times ASSIGNS.**

**Settle the boundary convention before coding** — `>=` against `>` — the problem decides it, and say which you
assumed.

**All techniques are `O(n log n)`, dominated by the sort.** **Add values and greedy breaks**: `[0,10]` worth
100 against three worth 10 gives greedy 30 and the answer 100. **Weighted interval scheduling is DP —
`dp[i] = max(dp[i-1], value + dp[p(i)])` with `p(i)` found by BINARY SEARCH** (a linear scan makes it `O(n²)`)
— **and it is the same `O(n log n)`, so greedy failing costs a table, not a complexity penalty.**
