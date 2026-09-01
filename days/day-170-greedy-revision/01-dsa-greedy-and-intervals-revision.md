---
day: 170
track: dsa
title: "Greedy and intervals revision and mock round"
phase: "Greedy and intervals"
status: written
---

# Greedy and intervals revision and mock round

## 1. What this is, and why they ask it

This is the last day of greedy, and it is a **mock round**: three unseen problems under the clock, talked
through out loud, with the solutions afterwards.

The revision half is one thing — **a decision procedure**. Given an unseen problem, **how do you decide, in
under two minutes, whether greedy is safe?** And if it is, **which key do you sort by?**

Because those two questions are the whole of this phase. **Almost every greedy problem you will meet is
"sort by the right thing, then take"**, and almost every greedy *failure* is either the wrong sort key or a
greedy choice that was never safe.

They ask it because **greedy is the technique candidates most often get right for the wrong reason.** You
write it, it passes the examples, and the interviewer asks "why does that work?" — **and there is nothing
there.** A candidate who says "sort by end time, and here is the exchange argument" is in a different
category from one who says "it seemed right".

**And the mock format matters as much as the problems.** In a real interview you are choosing out loud, under
time, without being able to run the code — **and the failure is almost never the technique. It is freezing,
or going silent, or writing before deciding.**

By the end of this lesson you have the decision procedure, a sort-key table you can recall under pressure, the
exchange argument in a form you can say in thirty seconds, the "greedy with an undo" family that bridges to
DP, and three solved mock problems with a self-scoring rule.

---

## 2. The story

Anasuya had failed the driving test once, and it was not the driving.

Her uncle, who had taught her in the empty ground behind the sugar factory, said the same thing every evening
for a month.

**"Say it out loud. Whatever you are looking at, say it."**

She thought it was silly. She could see the gap. Why say it?

The second test was on a Tuesday morning and the examiner was a small man with a clipboard who said good
morning and then nothing at all for eleven minutes.

**And the silence was the hard part.** Because with nobody speaking, her own head got loud, and the loudness
was always the same shape — *was that the right moment, should I have waited, is he writing something down.*

**So she did what her uncle had drilled into her, and she felt foolish doing it.**

"Bike on the left, I am staying wide of him." "Slowing for the school gate." "There is a gap coming, I am
taking it."

At the roundabout by the bus stand there was a gap — **not a lovely gap, an adequate one** — and she took it,
and she said why. *"That one is big enough and the next one might not come."*

**The examiner still said nothing.** But she noticed, afterwards, that he had stopped writing at about the
point she started talking.

At the end he signed the sheet and handed it over and said one thing, and she thought about it for years.

**"Most of the people I fail can drive perfectly well."**

"They freeze at the junction. Not because they do not know what to do — **because they are waiting for a
better moment than the one in front of them.** And the moment goes."

**"You took an ordinary gap and you told me why. That is the whole test."**

---

## 3. The idea in plain English

**Greedy is: take the best-looking option now, and never revisit it.** No stack of alternatives, no undoing —
one pass, one decision at each step, committed.

**That is why it is fast, and that is why it is usually wrong.** Anasuya's ordinary gap is right in traffic
and wrong in a great many problems, **and the entire skill is telling the two apart before you write code.**

### The decision procedure

**Four questions, in this order. It takes under two minutes.**

**One: is there an obvious best-looking choice at each step?** If you cannot name it in a sentence — "take the
one that finishes earliest", "take the largest coin" — **there is no greedy to try.**

**Two: try to build a counter-example.** Take the greedy choice, and ask **whether taking it can ever prevent
a better total later.** Try small: three items, two of them conflicting. **This is where most greedy attempts
die, and it should take thirty seconds.**

**Three: state the exchange argument.** *"Take any optimal solution. If it does not start with my greedy
choice, I can swap my choice in for its first choice without making it worse. So there is an optimal solution
starting with my choice, and by induction greedy is optimal."* **If you can fill in the swap concretely, greedy
is proved.** If you cannot, you do not have it.

**Four: if two or three failed, it is DP.** Greedy failing is not a dead end — **it is the signal that
subproblems overlap and you need the table.**

**Say all four out loud in an interview.** The candidate who says "greedy fails here, and here is the
three-element input where it fails, so I will do the DP" **is better than the one who guesses correctly**,
because the reasoning transfers to a problem you have not seen.

### The sort-key table

**Almost every interval problem is "sort by the right key, then one pass."** The whole difficulty is choosing
the key, so this is the thing to be able to recall cold:

```
   THE QUESTION                          SORT BY       WHY

   most non-overlapping intervals        END           earliest finish leaves
   (activity selection, arrows,                        the most room behind it
    non-overlapping intervals)

   merge overlapping intervals           START         you can only merge with
   (insert, merge, free slots)                         something already seen

   how many overlap at once              BOTH, as      a start is +1, an end
   (rooms, peak load, skyline)           EVENTS        is -1; sweep and track
                                                       the running total

   can I reach the end / fewest jumps    NOTHING       the reachable set is a
   (jump game, gas station)              (one pass)    prefix, so it collapses
                                                       to one frontier number

   fit as many deadlines as possible     DEADLINE      take everything, then
   (course schedule III)                 + A HEAP      UNDO the longest when
                                                       you overrun

   minimum stops with fuel/refuels       POSITION      pass everything, then
   (refuelling, IPO)                     + A HEAP      take the biggest you
                                                       passed, retroactively
```

**Two families are worth naming separately, because they are the ones people do not recognise.**

### Greedy with an undo

**Course Schedule III is the shape.** Sort by deadline, **take every course**, and **when the running total
overruns the current deadline, remove the longest course you have already taken.**

**That removal is the exchange argument made executable.** You are saying: *given that I must drop one, the
longest is never a worse thing to drop* — because dropping it frees the most time and costs the same one
course.

**This is not pure greedy** — it revisits decisions. **And it is not DP** — it never builds a table. It is the
middle ground, and **it exists precisely where the greedy choice is right about "how many" but wrong about
"which".**

### Regret greedy

**Minimum Refuelling Stops is the shape.** You do not decide at each station whether to stop. **You drive
past everything you can reach, keeping what you passed, and when you run dry you retroactively take the
biggest tank you went by.**

**The trick is deferring the decision until you know you needed it.** At the moment you run out of fuel you
know exactly which stations were available, **so you can pick the best one with hindsight rather than
guessing.**

**Both families use a heap, and the heap is the tell.** If a problem feels greedy but the greedy choice is
clearly sometimes wrong, **ask whether you can defer or undo the choice with a heap** before reaching for DP.

### Where greedy definitively dies

**Add a cost to the choice and greedy usually dies.** Jump Game is greedy; jump game *with a cost per landing*
is DP. Coin change with the Indian coin set is greedy; **coin change with `[1, 3, 4]` and target 6 is not** —
greedy gives `4+1+1` and the answer is `3+3`.

**The pattern is: greedy survives when the choice affects only what is still available, and dies when the
choice also carries a value you are optimising.**

---

## 4. The picture

The decision procedure, as a chart:

```
   an unseen problem
        |
        v
   Can I name an obvious best-looking choice in one sentence?
        |
        +-- NO ----> not greedy. Look for DP state.
        |
       YES
        |
        v
   Can I build a small counter-example in 30 seconds?
        |
        +-- YES ---> greedy is WRONG. Say so out loud, show the
        |            counter-example, and go to DP.
        |
        NO
        |
        v
   Can I state the exchange argument concretely?
        |
        +-- NO ----> I do not have it. Try harder for a counter-
        |            example; one of the two will give way.
        |
       YES
        |
        v
   GREEDY, and I can defend it.

   The middle branch is worth as many marks as the last one.
   "Greedy fails, here is the input" is a correct answer.
```

The exchange argument in one picture:

```
   greedy picks  A  (the earliest-finishing interval)
   some optimal  B  ...  (starts with something else)

   OPTIMAL:   [-----B-----][---C---][--D--]
   GREEDY:    [--A--]

   A finishes no later than B, because greedy took the
   earliest finish.
        |
        v
   SWAP: replace B with A in the optimal solution

   SWAPPED:   [--A--]     [---C---][--D--]
                    ^
              A ends EARLIER than B did, so nothing that
              followed B can now conflict.

   -> same number of intervals, still valid
   -> so there IS an optimal solution starting with A
   -> induct on the rest

   THAT IS THE WHOLE PROOF. It fits in thirty seconds
   out loud, and it is what "why does that work?" wants.
```

Why "sort by end" and not "sort by start":

```
   [[1, 100], [11, 22], [1, 11], [2, 12]]

   BY START:  [1,100] [1,11] [2,12] [11,22]
              take [1,100] first -> it blocks EVERYTHING
              keeps 1, removes 3          <- WRONG

   BY END:    [1,11] [2,12] [11,22] [1,100]
              take [1,11], then [11,22]
              keeps 2, removes 2          <- CORRECT

   The greedy choice must be the one that COSTS THE LEAST
   FUTURE. Earliest finish costs the least future. Earliest
   start costs nothing predictable at all.
```

Greedy with an undo:

```
   courses (duration, deadline), sorted by DEADLINE

   [5, 5]   take it.  total 5.   5 <= 5   ok
   [4, 6]   take it.  total 9.   9 >  6   OVERRUN
                                 |
                                 v
                      undo the LONGEST taken (5)
                      total 4.  count still 2 in the heap? no —
                      one was pushed and one popped, so 1... then
   [2, 6]   take it.  total 6.   6 <= 6   ok

   -> 2 courses

   TAKE-AND-NEVER-UNDO gives 1: it takes [5,5], then nothing
   else fits.

   The undo is the exchange argument, executed: given that
   I must drop one, dropping the LONGEST frees the most time
   at the same cost of one course.
```

Regret greedy:

```
   target 100, start with 10 fuel
   stations (position, fuel): [10,60] [20,30] [30,30] [60,40]

   fuel 10  --> can reach position 10
                pass [10,60], bank it            banked: {60}
                out of range. run dry.
                TAKE THE BIGGEST BANKED: 60
                fuel 70, stops 1

   fuel 70  --> can reach 20, 30, 60
                bank [20,30] [30,30] [60,40]     banked: {30,30,40}
                still short of 100. run dry.
                TAKE THE BIGGEST BANKED: 40
                fuel 110, stops 2

   -> 2 stops

   You never DECIDE at a station. You drive past everything,
   and you buy fuel WITH HINDSIGHT, at the moment you know
   you needed it.
```

---

## 5. The code, built step by step

**This is a mock round.** Read the problem, set a clock, and **say your decision procedure out loud before
writing anything.** The solutions are below each one — do not read ahead.

### Mock problem one, warm-up: fifteen minutes

> *Given a set of intervals, remove the minimum number so that the rest do not overlap.*
> (Non-overlapping Intervals, LeetCode 435.)

**The two minutes of thinking first.** "Remove the fewest" is "**keep the most**", which is activity selection.
**The greedy choice is the earliest finishing time**, because it leaves the most room behind it. **The exchange
argument: swap the earliest finisher into any optimal solution's first slot; it ends no later, so nothing
conflicts.**

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """SORT BY END. Keep greedily, count what you dropped."""
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda pair: pair[1])
    kept, kept_end = 1, intervals[0][1]
    for start, end in intervals[1:]:
        if start >= kept_end:            # no overlap with the last one kept
            kept += 1
            kept_end = end
    return len(intervals) - kept
```

**`start >= kept_end` is the tie-break**, and it says touching intervals do not conflict — **which is what this
problem wants, and is a sentence worth saying out loud** rather than assuming.

**And answering "keep the most" and subtracting is easier than counting removals directly**, which is worth
noticing: **the greedy is on the keeping, and the removal count falls out.**

### Mock problem two, the main one: twenty-five minutes

> *Each course takes some days and must finish by a deadline. Starting on day 1, take as many as possible.*
> (Course Schedule III, LeetCode 630.)

**The two minutes.** Sorting by deadline is obviously right — **you must attempt earlier deadlines earlier,
because a course you can take later you can also take now.**

**But then the greedy choice fails**, and you should find this yourself: `[[5,5],[4,6],[2,6]]`. Take-if-it-fits
takes `[5,5]` and then nothing. **The answer is 2** — take `[4,6]` and `[2,6]`.

**So greedy is right about the ordering and wrong about the commitment.** Which is the tell for an undo.

```python
import heapq

def schedule_course(courses: list[list[int]]) -> int:
    """SORT BY DEADLINE. Take everything; when you overrun, undo the longest."""
    courses = sorted(courses, key=lambda course: course[1])
    taken: list[int] = []                # a max-heap of durations, negated
    total = 0
    for duration, deadline in courses:
        heapq.heappush(taken, -duration)
        total += duration
        if total > deadline:             # the undo — the exchange argument, executed
            total += heapq.heappop(taken)
    return len(taken)
```

**`total += heapq.heappop(taken)` subtracts**, because the heap holds negated durations. **Write the comment,
because you will misread it otherwise.**

**And the argument for undoing the *longest* is the whole solution**, so say it: **when you must drop one
course, dropping the longest frees the most days and costs exactly the same one course.** There is never a
reason to drop a shorter one.

**Note what the counter is.** `len(taken)` — **the heap's size is the answer**, because every push that
survived is a course you kept.

### Mock problem three, the hard one: twenty minutes

> *A car starts with some fuel and must reach a target. Stations along the way each give a fixed amount.
> Fewest stops?* (Minimum Number of Refueling Stops, LeetCode 871.)

**The two minutes.** The obvious greedy — "stop when you are about to run out" — **is a decision you cannot
make correctly at the time**, because you do not yet know how far you must go.

**So defer it.** Drive as far as the fuel allows, **banking every station you pass**, and when you run dry,
**buy the biggest tank you went past.**

```python
def min_refuel_stops(target: int, start_fuel: int,
                     stations: list[list[int]]) -> int:
    """REGRET GREEDY. Drive past everything; refuel retroactively, biggest first."""
    passed: list[int] = []               # fuel you drove past and could still take
    fuel, stops, i = start_fuel, 0, 0
    while fuel < target:
        while i < len(stations) and stations[i][0] <= fuel:
            heapq.heappush(passed, -stations[i][1])
            i += 1
        if not passed:
            return -1
        fuel += -heapq.heappop(passed)
        stops += 1
    return stops
```

**`fuel` is doing two jobs and that is the elegant part**: it is the fuel in the tank *and* the furthest
position reachable, **because starting from zero they are the same number.** Say that out loud — it is the
observation the whole solution rests on.

**`stations[i][0] <= fuel` with `<=`, not `<`.** A station exactly at the limit of your range **is
reachable** — you arrive with an empty tank, which is fine. **With `<` the whole thing returns `-1` on the
example**, and it is the single most likely bug here.

**And `i` never resets.** Each station is banked once, so the inner loop is amortised — **the two loops
together are one pass, not a nested one.**

### The self-scoring harness

**Score yourself honestly on four things per problem**, because the technique is rarely what fails:

```
   1. Did I say the decision procedure OUT LOUD before writing?     yes / no
   2. Did I name the sort key and JUSTIFY it?                       yes / no
   3. Did I try a counter-example before committing?                yes / no
   4. Did I state the complexity without being asked?               yes / no
```

**Three out of four on all three problems is an interview pass.** Getting all three problems right silently
is not.

### The verification habit

**Every greedy you write should be checked against a brute force on small random inputs.** It takes four
minutes, it is the only evidence you will ever have, **and it has caught more wrong sort keys than reasoning
ever has.**

The complete file below does exactly that for all three.

### The complete solution

```python
"""Day 170 — the greedy mock round, solved, checked, and timed."""

from __future__ import annotations

import heapq
import itertools
import random


# ---------------------------------------------------------------- problem one
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """SORT BY END. Keep greedily, count what you dropped."""
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda pair: pair[1])
    kept, kept_end = 1, intervals[0][1]
    for start, end in intervals[1:]:
        if start >= kept_end:            # no overlap with the last one kept
            kept += 1
            kept_end = end
    return len(intervals) - kept


# ---------------------------------------------------------------- problem two
def schedule_course(courses: list[list[int]]) -> int:
    """SORT BY DEADLINE. Take everything; when you overrun, undo the longest."""
    courses = sorted(courses, key=lambda course: course[1])
    taken: list[int] = []                # a max-heap of durations, negated
    total = 0
    for duration, deadline in courses:
        heapq.heappush(taken, -duration)
        total += duration
        if total > deadline:             # the undo — this is the exchange argument
            total += heapq.heappop(taken)
    return len(taken)


# -------------------------------------------------------------- problem three
def min_refuel_stops(target: int, start_fuel: int,
                     stations: list[list[int]]) -> int:
    """REGRET GREEDY. Drive past everything; refuel retroactively, biggest first."""
    passed: list[int] = []               # fuel you drove past and could still take
    fuel, stops, i = start_fuel, 0, 0
    while fuel < target:
        while i < len(stations) and stations[i][0] <= fuel:
            heapq.heappush(passed, -stations[i][1])
            i += 1
        if not passed:
            return -1
        fuel += -heapq.heappop(passed)
        stops += 1
    return stops


# ------------------------------------------------------------ the brute forces
def erase_brute(intervals: list[list[int]]) -> int:
    """Every subset. Correct, and unusable past about eighteen intervals."""
    n = len(intervals)
    best = 0
    for size in range(n, 0, -1):
        for combo in itertools.combinations(intervals, size):
            ordered = sorted(combo)
            if all(ordered[i][1] <= ordered[i + 1][0] for i in range(len(ordered) - 1)):
                best = size
                break
        if best:
            break
    return n - best


def schedule_brute(courses: list[list[int]]) -> int:
    """Every subset in every order. Correct, and factorial."""
    best = 0
    n = len(courses)
    for size in range(n, 0, -1):
        found = False
        for combo in itertools.combinations(courses, size):
            for order in itertools.permutations(combo):
                clock = 0
                if all((clock := clock + d) <= dl for d, dl in order):
                    found = True
                    break
            if found:
                break
        if found:
            best = size
            break
    return best


def refuel_brute(target: int, start_fuel: int, stations: list[list[int]]) -> int:
    """DP: furthest reachable with exactly k stops."""
    n = len(stations)
    reach = [start_fuel] + [0] * n
    for position, fuel in stations:
        for k in range(n - 1, -1, -1):
            if reach[k] >= position:
                reach[k + 1] = max(reach[k + 1], reach[k] + fuel)
    for k, distance in enumerate(reach):
        if distance >= target:
            return k
    return -1


# ------------------------------------------------------------------ the checks
def check_erase(trials: int = 2000) -> int:
    bad = 0
    for _ in range(trials):
        n = random.randint(1, 8)
        intervals = []
        for _ in range(n):
            a = random.randint(0, 12)
            intervals.append([a, a + random.randint(1, 5)])
        if erase_overlap_intervals(intervals) != erase_brute(intervals):
            bad += 1
    return bad


def check_schedule(trials: int = 400) -> int:
    bad = 0
    for _ in range(trials):
        n = random.randint(1, 6)
        courses = [[random.randint(1, 6), random.randint(1, 15)] for _ in range(n)]
        if schedule_course(courses) != schedule_brute(courses):
            bad += 1
    return bad


def check_refuel(trials: int = 2000) -> int:
    bad = 0
    for _ in range(trials):
        n = random.randint(0, 6)
        target = random.randint(1, 40)
        start = random.randint(0, 20)
        positions = sorted(random.sample(range(1, 40), n))
        stations = [[p, random.randint(1, 15)] for p in positions]
        if min_refuel_stops(target, start, stations) != refuel_brute(target, start, stations):
            bad += 1
    return bad


if __name__ == "__main__":
    random.seed(0)

    print("PROBLEM ONE — Non-overlapping Intervals (sort by END)")
    one = [[1, 2], [2, 3], [3, 4], [1, 3]]
    print(f"  {one} -> remove {erase_overlap_intervals(one)}")
    two = [[1, 100], [11, 22], [1, 11], [2, 12]]
    print(f"  {two} -> remove {erase_overlap_intervals(two)}")
    print("  sorted by START instead:")
    by_start = sorted(two, key=lambda p: p[0])
    kept, kept_end = 1, by_start[0][1]
    for s, e in by_start[1:]:
        if s >= kept_end:
            kept += 1
            kept_end = e
    print(f"    keeps {kept}, so removes {len(two) - kept}  (correct answer: "
          f"{erase_overlap_intervals(two)})")

    print()
    print("PROBLEM TWO — Course Schedule III (sort by DEADLINE, undo the longest)")
    courses = [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
    print(f"  {courses} -> {schedule_course(courses)}")
    greedy_no_undo = [[5, 5], [4, 6], [2, 6]]
    print(f"  {greedy_no_undo} -> {schedule_course(greedy_no_undo)}")
    print("    take-and-never-undo would take [5,5] and then fit nothing: 1")

    print()
    print("PROBLEM THREE — Minimum Refueling Stops (regret greedy)")
    print(f"  target 100, start 10, stations [[10,60],[20,30],[30,30],[60,40]] -> "
          f"{min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]])}")
    print(f"  target 100, start 1,  stations [[10,100]] -> "
          f"{min_refuel_stops(100, 1, [[10, 100]])}")
    print(f"  target 1,   start 1,  stations []          -> "
          f"{min_refuel_stops(1, 1, [])}")

    print()
    print("VERIFICATION — greedy against brute force")
    print(f"  problem one:   {check_erase()} mismatches in 2,000 random cases")
    print(f"  problem two:   {check_schedule()} mismatches in 400 random cases")
    print(f"  problem three: {check_refuel()} mismatches in 2,000 random cases")
```

Running it:

```
PROBLEM ONE — Non-overlapping Intervals (sort by END)
  [[1, 2], [2, 3], [3, 4], [1, 3]] -> remove 1
  [[1, 100], [11, 22], [1, 11], [2, 12]] -> remove 2
  sorted by START instead:
    keeps 1, so removes 3  (correct answer: 2)

PROBLEM TWO — Course Schedule III (sort by DEADLINE, undo the longest)
  [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]] -> 3
  [[5, 5], [4, 6], [2, 6]] -> 2
    take-and-never-undo would take [5,5] and then fit nothing: 1

PROBLEM THREE — Minimum Refueling Stops (regret greedy)
  target 100, start 10, stations [[10,60],[20,30],[30,30],[60,40]] -> 2
  target 100, start 1,  stations [[10,100]] -> -1
  target 1,   start 1,  stations []          -> 0

VERIFICATION — greedy against brute force
  problem one:   0 mismatches in 2,000 random cases
  problem two:   0 mismatches in 400 random cases
  problem three: 0 mismatches in 2,000 random cases
```

**The `-1` case matters** — the first station is at 10 and you start with 1, **so you cannot even reach it**,
and the `if not passed: return -1` is what catches that. **And `target 1, start 1` with no stations gives 0**,
because the `while fuel < target` loop never runs.

---

## 6. What it costs

**Problem one.**

```
sort:          n log n
one pass:      n comparisons

total:         O(n log n) time, O(1) extra space
               (O(n) if the sort copies, which sorted() does)

THE SORT DOMINATES. Every interval problem in this phase
has the same sentence, and it is worth saying: the greedy
pass is linear and free; you pay for the ordering.
```

**Problem two.**

```
sort:                          n log n
one pass, n items:
  each push:                   log n
  at most n pops total:        n log n

total:                         O(n log n) time
                               O(n) space for the heap

Count it concretely: 10,000 courses
  sort:   10,000 x log2(10,000) ~= 10,000 x 13 = 130,000
  pushes: 10,000 x 13           = 130,000
  pops:   at most 10,000 x 13   = 130,000
  ~= 400,000 operations. Instant.
```

**The "at most n pops" is the amortised argument** and it is worth stating: **you cannot pop more than you
pushed**, so the total pop work over the whole run is bounded by the total push work — **not by n pops per
step.**

**Problem three.**

```
each station is pushed AT MOST ONCE:      n pushes, n log n
each pop is one stop, at most n stops:    n log n
the pointer i never resets:               n total advances

total:                                    O(n log n) time
                                          O(n) space

The two nested while loops LOOK quadratic. They are not,
because i only ever moves forward. Say this out loud —
the interviewer is often checking whether you noticed.
```

**Against the brute forces, so the verification cost is honest.**

```
problem one, brute force:   every subset = 2^n
  n = 8:   256 subsets              instant
  n = 20:  1,048,576                a second or two
  n = 40:  1,099,511,627,776        no

problem two, brute force:   every subset IN EVERY ORDER
  n = 6:   sum over sizes of C(6,k) x k!  = 1,957 orderings
  n = 10:  ~9,864,101
  n = 12:  ~1.3 billion             no

-> which is exactly why the checks in the file use n <= 8
   and n <= 6. The brute force is the ORACLE, not the
   solution, and it only has to be right on small inputs.
```

**The whole phase, in one table.**

```
   PROBLEM FAMILY              TIME          SPACE    DOMINATED BY

   activity selection          n log n       O(1)     the sort
   merging intervals           n log n       O(n)     the sort
   sweep line                  n log n       O(n)     the sort
   jump game / reachability    O(n)          O(1)     NOTHING — no sort!
   greedy with an undo         n log n       O(n)     sort + heap
   regret greedy               n log n       O(n)     sort + heap

   Jump game is the odd one out, and that is the point of
   it: when the greedy structure collapses to ONE NUMBER,
   you do not even pay for the sort.
```

---

## 7. The traps

**The wrong sort key, which is silent.**

Sorting by start on problem one:

```
[[1, 100], [11, 22], [1, 11], [2, 12]]
  by START: keeps 1, so removes 3
  by END:   keeps 2, so removes 2      <- correct
```

**Nothing errors.** The code runs, the answer is a plausible integer, **and it passes `[[1,2],[2,3],[3,4]]` and
every other example where the intervals happen to be in start order already.** This is the trap of the phase:
**the wrong key is right on tidy inputs and wrong on real ones.**

Sorting courses by duration instead of deadline:

```
[[1, 5], [2, 10], [6, 8]]
  by deadline: 3     <- correct
  by duration: 2
```

**By duration takes 1, then 2 (total 3), then tries 6 — total 9, over the deadline of 8 — and undoes the 6.**
Two courses. **By deadline it attempts the tight one while there is still room.**

**Take-and-never-undo on problem two.**

```
[[5, 5], [4, 6], [2, 6]]
  with the undo:  2
  without it:     1
```

**And the `>` in `if total > deadline` must not be `>=`:**

```
[[5, 5], [4, 6], [2, 6]]
  with `>`:   2      <- correct
  with `>=`:  1
```

**A course finishing exactly on its deadline is fine**, and `>=` throws it away. **One character, and it costs
you a course on every input where the fit is exact** — which is most of the interesting ones.

**`<` instead of `<=` on problem three.**

```
target 100, start 10, stations [[10,60],[20,30],[30,30],[60,40]]
  with `<=`:  2      <- correct
  with `<`:  -1
```

**A station exactly at the edge of your range is reachable.** You arrive with an empty tank, which is legal.
**With `<` you never bank the first station, `passed` is empty, and the function reports the target
unreachable** — a wrong answer that looks like a legitimate "impossible".

**No guard on the empty input.**

```python
intervals = []
intervals.sort(key=lambda p: p[1])
kept_end = intervals[0][1]
```

```
Traceback (most recent call last):
  File "<stdin>", line 14, in empty_first
IndexError: list index out of range
```

**This one at least announces itself**, which puts it in the good category. The silent ones are worse.

**Negating the wrong thing in the heap.**

```python
for course in courses:
    heapq.heappush(taken, -course)     # course is [duration, deadline]
```

```
Traceback (most recent call last):
  File "<stdin>", line 30, in heap_of_lists
TypeError: bad operand type for unary -: 'list'
```

**Loud, and easy.** The dangerous version is pushing `+duration` instead of `-duration`: **no error, and the
heap now pops the *shortest* course**, so the undo removes the wrong one and the answer is quietly too small.

**Reaching into the wrong tuple position.**

```python
courses.sort(key=lambda c: c[2])
```

```
Traceback (most recent call last):
  File "<stdin>", line 36, in sort_no_key
  File "<stdin>", line 36, in <lambda>
IndexError: list index out of range
```

**And the two-subscript slip, which is the most common typing error under time pressure:**

```python
while i < len(stations) and stations[i, 0] <= fuel:
```

```
Traceback (most recent call last):
  File "<stdin>", line 22, in tuple_index
TypeError: list indices must be integers or slices, not tuple
```

**"It worked on the examples" as a proof.** The deepest trap of the phase. **Every wrong sort key passes the
examples**, because example inputs are small and tidy and usually already in the right order. **The only
evidence is a brute-force check on random inputs**, and the only *argument* is the exchange argument. **Have
one of the two, and say which one you have.**

---

## 8. In the interview

### How it gets asked

- *"Two problems, no hints, talk as you go."* — the mock format itself.
- *"Why does sorting by end time work?"* — the exchange argument, and the real question of the phase.
- *"How do you know greedy is correct here?"*
- *"Can you do better than the DP?"* — often a hint that greedy exists.
- *"What if each choice also had a cost?"* — usually a hint that greedy just died.

### The first ninety seconds

Said before writing anything, on any greedy-looking problem:

> "Before I write, let me decide whether greedy is even safe here, because that is where these problems are won
> or lost.
>
> **First: is there an obvious best-looking choice at each step?** Here it is **the interval that finishes
> earliest** — I can say it in a sentence, so there is a greedy to try.
>
> **Second: can I break it?** Let me try three intervals with two of them conflicting... **I cannot construct
> a counter-example**, which is encouraging but not sufficient.
>
> **Third, and this is the real test: can I state the exchange argument?**
>
> **Take any optimal solution. If it does not start with the earliest-finishing interval, swap that interval
> in for whatever it does start with.** My interval finishes no later, **so nothing that followed can now
> conflict** — the solution is still valid and still the same size. **So there is an optimal solution starting
> with my greedy choice, and the same argument applies to what remains.**
>
> **That is a proof, and it is why I am confident rather than hopeful.**
>
> **So: sort by end time, one pass, keep anything that starts at or after the last kept end.** `O(n log n)`,
> dominated entirely by the sort — the greedy pass itself is linear.
>
> **One clarification before I write: do intervals that touch count as overlapping?** `[1,2]` and `[2,3]` —
> **it is one comparison and the problem decides it**, so I would rather ask than assume.
>
> **And when I am done I would check it against a brute force on small random inputs**, because a wrong sort
> key passes every example and fails on real data."

### The follow-ups

**"How do you decide whether greedy works, in general?"**

> "Four questions, in order, and it takes under two minutes.
>
> **One: can I name an obvious best-looking choice in one sentence?** 'Take the earliest finisher.' 'Take the
> largest coin.' **If I cannot say it in a sentence, there is no greedy to try** and I go straight to DP state.
>
> **Two: can I build a small counter-example?** I try three items with two of them in conflict. **This is where
> most greedy attempts die, and it should take thirty seconds.** Coin change is the standard example — greedy
> works for the coins in your pocket, **and `[1,3,4]` with a target of 6 gives `4+1+1` when the answer is
> `3+3`.**
>
> **Three: can I state the exchange argument concretely?** Not the shape of one — **the actual swap.** 'Replace
> the optimal's first choice with mine; mine finishes no later; therefore nothing conflicts.' **If I cannot
> fill in that middle clause, I do not have the argument** and I go back to hunting for a counter-example. One
> of the two always gives way.
>
> **Four: if two or three failed, it is DP** — and I say that out loud rather than treating it as a failure.
> **'Greedy fails here and here is the three-element input where it fails' is a correct answer**, and it is
> worth as much as getting greedy right.
>
> **The pattern behind all of it: greedy survives when the choice affects only what is still available, and
> dies when the choice also carries a value you are optimising.** Jump Game is greedy; **jump game where each
> landing costs something is DP.**
>
> **And there is a middle ground people forget.** If greedy feels right but the choice is clearly sometimes
> wrong, **ask whether you can defer or undo it with a heap** before reaching for a table."

**"Which sort key, and why?"**

> "There are about five, and I would rather recall the reason than the key.
>
> **The rule underneath is: sort so the greedy choice costs the least future.**
>
> **Sort by end** when you want the most non-overlapping intervals — activity selection, arrows, non-overlapping
> intervals. **Earliest finish leaves the most room behind it**, which is precisely 'costs the least future'.
>
> **Sort by start** when merging. **You can only merge with something you have already seen**, so you need
> them in the order they begin.
>
> **Sort as events — a start is `+1`, an end is `-1`** — when the question is 'how many at once'. Rooms, peak
> load, the skyline. **And the tie-break at equal times is the whole difficulty there.**
>
> **Do not sort at all** for reachability. **Jump Game is `O(n)`** because the reachable set is a prefix and
> collapses to one frontier number — **the odd one out in the phase, and the one worth remembering for that
> reason.**
>
> **Sort by deadline plus a heap** when you want to fit as many deadlines as possible and pure greedy fails.
>
> **And here is the concrete evidence for why the key matters.** On `[[1,100],[11,22],[1,11],[2,12]]`, **sorting
> by start keeps one interval and sorting by end keeps two.** Nothing errors. **The wrong key is silent, and it
> is right on every tidy example** — which is why I check against a brute force rather than against the
> samples."

**"What if each choice also had a cost?"**

> "Then greedy is probably dead, and I would say so immediately rather than trying to patch it.
>
> **The reason is structural.** Greedy works when the choice only affects **what is still available**. As soon
> as the choice also carries **a value you are optimising**, the locally cheapest choice can lock you out of a
> globally cheaper path, **and there is no exchange argument** — the swap changes the total.
>
> **Concretely: Jump Game II is greedy and `O(n)`.** Add a cost per landing and it is DP. **On `[3,1,3,1,1,1]`
> with costs `[1,1,100,1,1,0]`, greedy jumps to the position that reaches furthest — and that landing costs a
> hundred.** Three cheap hops down the middle cost three.
>
> **But before conceding to DP I would check for the two middle-ground families, because they catch a lot of
> problems that look like this.**
>
> **Greedy with an undo.** Course Schedule III: sort by deadline, take everything, **and when you overrun,
> remove the longest course you already took.** That removal is the exchange argument executed — **given that I
> must drop one, dropping the longest frees the most time at the same cost of one course.**
>
> **Regret greedy.** Minimum Refuelling Stops: **do not decide at each station**, because you cannot yet know
> how far you must go. **Drive past everything, bank what you passed, and when you run dry take the biggest
> tank you went by** — deferring the decision until hindsight is available.
>
> **Both use a heap, and the heap is the tell.** If a problem feels greedy but the choice is sometimes clearly
> wrong, **try deferring or undoing it before building a table.** If neither works, it is DP, and that is a
> fine place to end up."

### The model answer

*"Here is a problem you have not seen. Talk me through it: given courses with a duration and a deadline,
starting on day one, take as many as you can."*

> "Let me decide the technique before I write anything.
>
> **Is there an obvious best-looking choice?** Something about deadlines — **and I can justify the ordering
> straight away.** Sort by deadline, **because a course you can take later you can also take now**, so
> attempting tight deadlines first can never hurt.
>
> **Now can I break the naive greedy — sort by deadline and take anything that fits?** Let me try three.
> `[[5,5],[4,6],[2,6]]`. **Take `[5,5]`: five days used, deadline five, fine. Then `[4,6]` needs day nine —
> too late. `[2,6]` needs day seven — too late. So one course.**
>
> **But `[4,6]` and `[2,6]` together take six days and both meet their deadlines. The answer is two.**
>
> **So greedy is right about the ordering and wrong about the commitment.** And that is a specific diagnosis
> rather than 'greedy fails' — **which tells me to try the undo family before reaching for DP.**
>
> **Here is the fix.** Sort by deadline. **Take every course as you meet it.** When the running total exceeds
> the current deadline, **remove the longest course you have already taken.**
>
> **And the justification is the exchange argument, made executable: given that I must drop exactly one course,
> dropping the longest frees the most days at exactly the same cost of one course.** There is never a reason to
> drop a shorter one. **So the count is never worse and the remaining budget is never tighter.**
>
> **A max-heap of durations gives me the longest in log n.** In Python that is `heapq` with negated values,
> and I will comment the sign because it is genuinely easy to misread.
>
> **The answer is the heap's size** — every push that survived is a course kept.
>
> **Cost: `O(n log n)`.** Sort, then n pushes and **at most n pops in total, not n pops per step** — you cannot
> pop more than you pushed. **`O(n)` space for the heap.**
>
> **Two things I would check before saying I am done.**
>
> **The comparison is `total > deadline`, not `>=`.** A course finishing exactly on its deadline is fine, and
> `>=` throws it away — **on that same `[[5,5],[4,6],[2,6]]` it gives one instead of two.** One character.
>
> **And I would run it against a brute force** — every subset in every order, on inputs of six or fewer — for a
> few hundred random cases. **Because a wrong sort key here is completely silent.** Sorting by duration instead
> of deadline gives two on `[[1,5],[2,10],[6,8]]` where the answer is three, **and nothing errors and every
> tidy example still passes.**
>
> **That check is the only evidence I have that the greedy is right, other than the exchange argument — and I
> would rather have both.**"

---

## 9. Recall card

**The decision procedure, four questions, under two minutes.** (1) Can I name the best-looking choice in one
sentence? (2) Can I build a counter-example in thirty seconds? (3) Can I state the **exchange argument
concretely** — the actual swap, not its shape? (4) If 2 or 3 failed, **it is DP — and saying so with the
counter-example is a correct answer.**

**The exchange argument in thirty seconds:** *take any optimal solution; swap my greedy choice in for its first
choice; mine finishes no later, so nothing that followed can conflict; same size, still valid; induct.* **This
is what "why does that work?" wants.**

**The sort-key table, and the rule underneath it — sort so the greedy choice costs the least future.** **END**
for most non-overlapping. **START** for merging. **EVENTS (+1/−1)** for how-many-at-once. **NO SORT, `O(n)`**
for reachability — the frontier collapses to one number. **DEADLINE + heap** for fitting deadlines. **POSITION
+ heap** for regret greedy.

**Two middle-ground families, and the heap is the tell.** **Greedy with an undo** (Course Schedule III: take
everything, drop the longest on overrun — dropping the longest frees the most time at the same cost of one
course). **Regret greedy** (refuelling: never decide at a station, drive past, buy the biggest tank you passed
once you know you needed it). **Try these before reaching for DP.**

**Greedy survives when the choice affects only what is still available; it dies when the choice carries a value
you are optimising.** Jump Game is `O(n)` greedy; jump game with a cost per landing is DP.

**The wrong sort key is SILENT and passes every tidy example.** By start instead of end: keeps 1 not 2. By
duration instead of deadline: 2 not 3. `>=` instead of `>`: 1 not 2. `<` instead of `<=` in refuelling: `-1`
not 2. **Your only evidence is a brute-force check on small random inputs; your only argument is the exchange.
Have one, and say which.**
