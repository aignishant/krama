---
day: 164
track: dsa
title: "Greedy: when taking the best option now is safe"
phase: "Greedy and intervals"
status: written
---

# Greedy: when taking the best option now is safe

## 1. What this is, and why they ask it

**A greedy algorithm makes the choice that looks best right now and never reconsiders it.**

It is the simplest possible approach and it is usually wrong. **When it is right, it is dramatically better
than the alternative** — one pass instead of a table, `O(n log n)` instead of `O(n²)`, constant space instead
of quadratic.

They ask it because **the interesting question is never "what is the greedy choice" — it is "why is that
choice safe".** Anybody can sort by something and take the first item. **The interview is whether you know
whether that works**, and yesterday's whole month of dynamic programming exists because usually it does not.

The other reason is that **greedy is where confident wrong answers live.** A candidate who writes a greedy
solution and moves on has produced something that passes the examples and fails the hidden tests. **A candidate
who says "greedy would take the largest first, and here is a five-element counter-example, so it must be DP"
has demonstrated more than either the greedy or the DP solution would.**

**The honest framing is that greedy is a claim, not a technique.** The claim is: *the locally best choice is
always part of some optimal solution.* **That claim is either true or false for a given problem, and there is
no way to tell by looking.** You either construct a counter-example or you argue.

By the end of this lesson you can state the two properties greedy needs, run the counter-example search,
recognise the four problems where greedy is provably right, and say precisely why it fails on the ones where it
does.

---

## 2. The story

There were forty-one seats on the bus and about sixty people at the stand, and Rukhsana had been selling the
tickets for six years.

**And the thing she did, which nobody had taught her and which she could not have explained, was decide who
got on.**

Not by queue. There had been a queue for a while and it did not survive contact with the bus.

**Her rule, in the early days, was simple: the ones going furthest.** The full fare was worth more than the
half fare, so fill the bus with people going to the end of the line and you take the most money.

**And it was right, and she did it for two years, and then somebody pointed out that it was not right at
all.**

Because the bus stopped seven times.

**Somebody going three stops got off, and their seat was sold again.** So a full-fare passenger occupying the
seat for the whole journey earned one fare, **and three short-distance passengers, one after another in the
same seat, earned three.**

She changed the rule and it took her about a week to settle on the new one, and it was not what she expected.

**The rule that worked was: whoever gets off soonest.**

Not the highest fare. Not the longest journey. **Whoever frees the seat first**, because a seat that comes back
early can be sold again, and a seat that comes back at the end cannot.

**And here is the part that mattered.** Her nephew, who thought about things, asked her how she knew it was
the best rule and not just a better one.

She said something that was almost a proof.

**"Take whichever way you think is best. Find the person in it who gets off latest, and put in the one who
gets off soonest instead. You have not lost a seat — you have gained the room they were taking up. So you can
never be worse off, and you might be better."**

Her nephew said that was the whole argument.

**"It is not an argument," she said. "It is just true. Try to make it wrong."**

---

## 3. The idea in plain English

Rukhsana's rule is the earliest-finishing-time greedy, and her sentence about swapping the latest for the
soonest **is an exchange argument** — which is the standard way of proving a greedy algorithm correct.

**Start with what greedy is, precisely.**

> **A greedy algorithm builds a solution one choice at a time, always taking the option that looks best by some
> local rule, and never undoing a choice.**

**Two things are hidden in that.** **The local rule** — what "best" means — which is usually the result of
sorting by something. **And "never undoes"**, which is what makes it fast and what makes it dangerous.

**Now the two properties greedy needs, and both are required.**

> **The greedy choice property: there is always an optimal solution that contains the locally best choice.**
>
> **Optimal substructure: after making that choice, what remains is the same problem on a smaller input.**

**Optimal substructure is shared with dynamic programming.** **The greedy choice property is what greedy adds,
and it is the one that is usually false.**

**And notice the exact phrasing: "there is always *an* optimal solution that contains it", not "the optimal
solution contains it".** There may be several optimal answers; **greedy needs only that one of them agrees with
its first choice.** That distinction is what makes the exchange argument work.

**Now the practical part: how to decide, in an interview, in thirty seconds.**

**Try to break it.**

**Construct small inputs where the locally best choice leads somewhere worse.** Three or four elements is
usually enough, and **the fastest place to look is where the greedy choice is large but blocks two smaller
things that together beat it.**

```
  coin change, coins [1, 5, 7], amount 10
     greedy: 7, then 1+1+1        -> 4 coins
     optimal: 5 + 5               -> 2 coins
     -> the 7 leaves a remainder only 1s can fill

  house robber, values [5, 10, 6]
     greedy: take 10, both neighbours forbidden   -> 10
     optimal: 5 + 6                               -> 11

  0/1 knapsack by value-per-kilo, capacity 10
     items (6kg, 60), (5kg, 40), (5kg, 40)
     greedy: the 6kg (ratio 10), then nothing fits  -> 60
     optimal: the two 5kg items                     -> 80
```

**Three counter-examples, none longer than three items.** **If you can build one, it is DP and you stop
looking.**

**And if you cannot build one, you owe an argument** — which is tomorrow's lesson in full, and the shape of
which is Rukhsana's sentence.

**The exchange argument, stated generally:**

> **Take any optimal solution. Show that you can swap the greedy choice into it — replacing whatever it used
> instead — without making it worse. Therefore there is an optimal solution containing the greedy choice, and
> by induction greedy is optimal.**

**Rukhsana's version:** take any seating you like, find the passenger who gets off latest, replace them with
the one who gets off soonest. **You have not lost a passenger and you have freed the seat earlier, so the
result is at least as good.**

**Now the four problems where greedy is provably right.** These are worth knowing by name, because **they are
the ones interviewers use to test whether you reach for DP unnecessarily.**

**Activity selection — the maximum number of non-overlapping intervals.** **Sort by end time, take greedily.**
Rukhsana's bus. **`O(n log n)`, and the DP alternative is `O(n²)`.**

**Fractional knapsack** — where items can be cut. **Sort by value per kilo, take greedily, cut the last one.**
**And the contrast is the whole lesson: 0/1 knapsack, where items cannot be cut, defeats the same rule.**
**Indivisibility is what breaks it.**

**Huffman coding** — building the optimal prefix code. **Repeatedly merge the two least frequent symbols.**
The exchange argument here is that the two rarest symbols can always be placed deepest.

**Minimum spanning trees** — Kruskal and Prim, from
[day 139](../day-139-minimum-spanning-trees/README.md). **Both are greedy and both are provably optimal**,
which is the most surprising entry on this list because MSTs feel like they should need more.

**And the three where greedy nearly works, which are the traps.**

**Coin change** works for canonical systems — one, two, five, ten — **which is why the intuition feels so
reliable.** It is a property of those numbers, not of the method.

**Interval scheduling by *start* time or by *shortest* interval** both fail, and **only end time works**, which
is the point of tomorrow's lesson.

**And the scheduling problems where you must sort by a *ratio* rather than by either quantity alone** — like
minimising total waiting time — are greedy with a non-obvious rule, **and the obvious rules are wrong.**

**Finally: the shape of a greedy solution, which is almost always the same.**

```
1. sort by the right thing            O(n log n) — usually the whole cost
2. one pass, taking or skipping       O(n)
3. maintain one or two variables      O(1) space
```

**The sort dominates**, so greedy solutions are `O(n log n)` and the DP alternatives are `O(n²)` or worse.
**And "the right thing" to sort by is the entire difficulty** — it is never obvious, and getting it wrong
produces a plausible answer.

---

## 4. The picture

The greedy choice property, and why the phrasing matters:

```
  ALL SOLUTIONS
  +------------------------------------------+
  |                                          |
  |   OPTIMAL SOLUTIONS (there may be many)  |
  |   +----------------------------------+   |
  |   |  A     B     C                   |   |
  |   +----------------------------------+   |
  |                                          |
  +------------------------------------------+

  GREEDY NEEDS: at least ONE of A, B, C contains the greedy choice.

  NOT: "every optimal solution contains it"
  NOT: "the greedy choice is in the best solution"

  It only needs SOME optimal solution to agree, which is exactly
  what the exchange argument establishes.
```

Rukhsana's exchange argument, drawn:

```
  SOME OPTIMAL SEATING              AFTER THE SWAP

  passenger P (gets off LAST)       passenger G (gets off SOONEST)
  ...plus others                    ...plus the SAME others

  swap P out, G in:
    - still the same number of passengers   (no loss)
    - the seat is free EARLIER              (a gain, or at worst equal)

  -> the swapped version is at least as good
  -> so there IS an optimal solution containing the greedy choice
  -> repeat on what remains. Greedy is optimal.

  "It is not an argument. It is just true. Try to make it wrong."
```

The three counter-examples, side by side:

```
  COIN CHANGE, coins [1,5,7], amount 10

     greedy:  7  1  1  1        4 coins
     optimal: 5  5              2 coins
     WHY: the biggest coin leaves a remainder that only 1s fit


  HOUSE ROBBER, values [5, 10, 6]

     greedy:  take 10, neighbours forbidden       = 10
     optimal: 5 + 6 (not adjacent to each other)  = 11
     WHY: the biggest value blocks TWO others that together beat it


  0/1 KNAPSACK by ratio, capacity 10
     (6kg, 60) ratio 10   (5kg, 40) ratio 8   (5kg, 40) ratio 8

     greedy:  6kg item, then nothing fits in 4kg  = 60
     optimal: both 5kg items                      = 80
     WHY: INDIVISIBILITY. The same rule is PROVABLY OPTIMAL
          for the fractional version.

  ALL THREE ARE THREE ITEMS LONG. That is how fast this check is.
```

The four where greedy is provably right:

```
  problem                  sort by              why it is safe
  --------------------------------------------------------------------
  activity selection       END time             frees the resource
                                                soonest; swap in the
                                                earliest finisher
  fractional knapsack      value per kilo       you can cut, so the
                                                best ratio always fills
  Huffman coding           frequency (merge     the two rarest can
                           the two smallest)    always go deepest
  minimum spanning tree    edge weight          the cut property:
                           (Kruskal / Prim)     the lightest edge
                                                crossing any cut is
                                                in some MST

  AND THE NEAR MISSES:
  coin change              only for CANONICAL systems (1,2,5,10...)
  interval scheduling      ONLY by end time — start time and
                           shortest-first both FAIL
```

The shape of every greedy solution:

```
   sort by the right thing         O(n log n)  <- dominates
        |
        v
   one pass, take or skip          O(n)
        |
        v
   one or two running variables    O(1) space

   THE HARD PART IS LINE ONE, and it is never obvious.
   Getting "the right thing" wrong produces a plausible answer
   with no error.
```

Greedy against DP, as a decision:

```
   can I construct a counter-example in 30 seconds?
        |
        +-- YES --> it is DP. Stop looking. State the counter-example
        |           out loud — it is the justification for the table.
        |
        +-- NO  --> greedy MIGHT work. Now I owe an argument:
                      exchange argument, or "stays ahead"
                    and if I cannot produce one, I say so and
                    write the DP, which is always correct.

   THE ASYMMETRY: a counter-example is PROOF that greedy fails.
   Failing to find one is NOT proof that it works.
```

---

## 5. The code, built step by step

### Activity selection: the canonical correct greedy

```python
def max_activities(intervals: list[tuple[int, int]]) -> int:
    """The most non-overlapping intervals. Sort by END time."""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])         # by END, not start
    count, last_end = 0, float("-inf")
    for start, end in intervals:
        if start >= last_end:                  # does not overlap what we have
            count += 1
            last_end = end
    return count
```

**Six lines, `O(n log n)`, and the whole difficulty is `key=lambda x: x[1]`.**

**Sorting by start time gives a wrong answer** — a long interval starting early blocks everything. **Sorting by
duration also gives a wrong answer.** **Only end time works**, and the reason is Rukhsana's: **finishing
earliest leaves the most room for whatever comes next.**

### The three wrong rules, so you can see them fail

```python
def max_activities_by_start(intervals: list[tuple[int, int]]) -> int:
    intervals.sort(key=lambda x: x[0])         # WRONG
    count, last_end = 0, float("-inf")
    for start, end in intervals:
        if start >= last_end:
            count, last_end = count + 1, end
    return count


def max_activities_by_length(intervals: list[tuple[int, int]]) -> int:
    intervals.sort(key=lambda x: x[1] - x[0])  # WRONG
    chosen: list[tuple[int, int]] = []
    for start, end in intervals:
        if all(end <= s or start >= e for s, e in chosen):
            chosen.append((start, end))
    return len(chosen)
```

**Writing the wrong versions and running them is worth five minutes**, because the failure is not obvious from
reading and is immediate from testing.

### Fractional knapsack: the ratio rule, where it is correct

```python
def fractional_knapsack(weights: list[int], values: list[int],
                        capacity: float) -> float:
    """Items CAN be cut. Sort by value per kilo. Provably optimal."""
    order = sorted(range(len(weights)),
                   key=lambda i: values[i] / weights[i], reverse=True)
    total, room = 0.0, capacity
    for i in order:
        if weights[i] <= room:
            total += values[i]
            room -= weights[i]
        else:
            total += values[i] * (room / weights[i])   # take a FRACTION
            break
    return total
```

**`total += values[i] * (room / weights[i])` is the line that makes greedy correct here**, and it is exactly
the line that does not exist in the 0/1 version.

**Say the contrast out loud:** **the same sort rule, provably optimal when you can cut and provably wrong when
you cannot.** **Indivisibility is the whole difference.**

### The counter-example finder

```python
import itertools

def find_counterexample(greedy, optimal, generate, trials: int = 2000):
    """Thirty seconds of work that decides greedy versus DP."""
    for _ in range(trials):
        case = generate()
        g, o = greedy(*case), optimal(*case)
        if g != o:
            return case, g, o
    return None
```

**This is the habit worth taking away from the whole lesson.** **A brute force for a five-element input takes
five minutes to write**, and comparing against it on a couple of thousand random small inputs **settles the
question definitively.**

**And the asymmetry matters**: finding a mismatch **proves** greedy is wrong. **Finding none proves nothing** —
it makes greedy plausible, and you still owe an argument.

### Exhaustive verification for small inputs

```python
def best_activities_brute(intervals: list[tuple[int, int]]) -> int:
    """Try every subset. Correct by construction, useless above n = 20."""
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        chosen = [intervals[i] for i in range(n) if mask >> i & 1]
        chosen.sort()
        if all(chosen[i][1] <= chosen[i + 1][0] for i in range(len(chosen) - 1)):
            best = max(best, len(chosen))
    return best
```

**Exponential and obviously correct**, which is exactly what a reference implementation should be. **Do not
optimise it** — its only job is to be right.

### Two more provably-correct greedies worth knowing

```python
import heapq
from collections import Counter

def huffman_cost(text: str) -> int:
    """Total encoded bits. Repeatedly merge the two least frequent."""
    frequencies = list(Counter(text).values())
    if len(frequencies) <= 1:
        return len(text)
    heapq.heapify(frequencies)
    total = 0
    while len(frequencies) > 1:
        a = heapq.heappop(frequencies)
        b = heapq.heappop(frequencies)
        total += a + b                          # the merge cost IS the answer
        heapq.heappush(frequencies, a + b)
    return total


def min_total_waiting(durations: list[int]) -> int:
    """Shortest job first minimises total waiting time. Exchange argument."""
    durations.sort()
    elapsed, total_wait = 0, 0
    for d in durations:
        total_wait += elapsed                   # everybody before me waited
        elapsed += d
    return total_wait
```

**`total += a + b` in Huffman is subtle and worth a comment**: the sum of all merge costs equals the total
encoded length, **because every merge adds one bit to every symbol beneath it.**

**And shortest-job-first has a one-line exchange argument**: swapping any adjacent pair out of sorted order
**strictly increases the total wait**, so sorted order is optimal.

### Where greedy fails: the same rules, defeated

```python
def coin_change_greedy(coins: list[int], amount: int) -> int:
    count, left = 0, amount
    for coin in sorted(coins, reverse=True):
        take = left // coin
        count += take
        left -= take * coin
    return count if left == 0 else -1


def coin_change_dp(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for t in range(coin, amount + 1):
            dp[t] = min(dp[t], dp[t - coin] + 1)
    return int(dp[amount]) if dp[amount] != float("inf") else -1


def knapsack_greedy_by_ratio(weights, values, capacity):
    order = sorted(range(len(weights)),
                   key=lambda i: values[i] / weights[i], reverse=True)
    total, room = 0, capacity
    for i in order:
        if weights[i] <= room:                  # NO fractions allowed
            total += values[i]
            room -= weights[i]
    return total


def knapsack_dp(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):    # backwards: each item once
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]
```

**Putting the greedy and the DP side by side and running both is the point of this section.** **The greedy is
shorter and faster and wrong**, and seeing the two numbers differ on a three-item input is more convincing than
any explanation.

### The complete solution

```python
"""Greedy: the four that work, the three that do not, and how to tell."""

import heapq
import random
from collections import Counter


# ---------- provably correct ----------

def max_activities(intervals: list[tuple[int, int]]) -> int:
    """Sort by END time. The canonical correct greedy."""
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda x: x[1])
    count, last_end = 0, float("-inf")
    for start, end in ordered:
        if start >= last_end:
            count += 1
            last_end = end
    return count


def fractional_knapsack(weights, values, capacity: float) -> float:
    """Items CAN be cut -> the ratio rule is provably optimal."""
    order = sorted(range(len(weights)),
                   key=lambda i: values[i] / weights[i], reverse=True)
    total, room = 0.0, float(capacity)
    for i in order:
        if weights[i] <= room:
            total += values[i]
            room -= weights[i]
        else:
            total += values[i] * (room / weights[i])
            break
    return total


def huffman_cost(text: str) -> int:
    """Merge the two least frequent, repeatedly. The merge costs sum to the answer."""
    frequencies = list(Counter(text).values())
    if len(frequencies) <= 1:
        return len(text)
    heapq.heapify(frequencies)
    total = 0
    while len(frequencies) > 1:
        a, b = heapq.heappop(frequencies), heapq.heappop(frequencies)
        total += a + b
        heapq.heappush(frequencies, a + b)
    return total


def min_total_waiting(durations: list[int]) -> int:
    """Shortest job first. Swapping any out-of-order pair strictly hurts."""
    elapsed, total_wait = 0, 0
    for d in sorted(durations):
        total_wait += elapsed
        elapsed += d
    return total_wait


# ---------- the wrong rules, for the same problem ----------

def max_activities_by_start(intervals) -> int:
    ordered = sorted(intervals, key=lambda x: x[0])
    count, last_end = 0, float("-inf")
    for start, end in ordered:
        if start >= last_end:
            count, last_end = count + 1, end
    return count


def max_activities_by_length(intervals) -> int:
    chosen: list[tuple[int, int]] = []
    for start, end in sorted(intervals, key=lambda x: x[1] - x[0]):
        if all(end <= s or start >= e for s, e in chosen):
            chosen.append((start, end))
    return len(chosen)


def best_activities_brute(intervals) -> int:
    """Exponential and obviously correct. Do not optimise it."""
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        chosen = sorted(intervals[i] for i in range(n) if mask >> i & 1)
        if all(chosen[i][1] <= chosen[i + 1][0] for i in range(len(chosen) - 1)):
            best = max(best, len(chosen))
    return best


# ---------- where greedy fails ----------

def coin_change_greedy(coins: list[int], amount: int) -> int:
    count, left = 0, amount
    for coin in sorted(coins, reverse=True):
        take = left // coin
        count += take
        left -= take * coin
    return count if left == 0 else -1


def coin_change_dp(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for t in range(coin, amount + 1):
            dp[t] = min(dp[t], dp[t - coin] + 1)
    return int(dp[amount]) if dp[amount] != float("inf") else -1


def knapsack_greedy_by_ratio(weights, values, capacity: int) -> int:
    order = sorted(range(len(weights)),
                   key=lambda i: values[i] / weights[i], reverse=True)
    total, room = 0, capacity
    for i in order:
        if weights[i] <= room:
            total += values[i]
            room -= weights[i]
    return total


def knapsack_dp(weights, values, capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def rob_greedy(values: list[int]) -> int:
    """Take the largest, forbid its neighbours, repeat."""
    remaining = list(values)
    total = 0
    while any(v is not None for v in remaining):
        best = max((i for i, v in enumerate(remaining) if v is not None),
                   key=lambda i: remaining[i])
        total += remaining[best]
        for j in (best - 1, best, best + 1):
            if 0 <= j < len(remaining):
                remaining[j] = None
    return total


def rob_dp(values: list[int]) -> int:
    take, skip = 0, 0
    for v in values:
        take, skip = skip + v, max(take, skip)
    return max(take, skip)


# ---------- the decision procedure ----------

def find_counterexample(greedy, optimal, generate, trials: int = 3000):
    """Finding one PROVES greedy wrong. Finding none proves nothing."""
    for _ in range(trials):
        case = generate()
        g, o = greedy(*case), optimal(*case)
        if g != o:
            return case, g, o
    return None


if __name__ == "__main__":
    random.seed(0)                                # deterministic output
    print("PROVABLY CORRECT GREEDY")
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
                  (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    print("  activities, by end   :", max_activities(activities))
    print("  activities, by start :", max_activities_by_start(activities))
    print("  activities, by length:", max_activities_by_length(activities))
    print("  brute force says     :", best_activities_brute(activities))

    print("  fractional knapsack  :",
          fractional_knapsack([10, 20, 30], [60, 100, 120], 50))
    print("  huffman 'aaabbc'     :", huffman_cost("aaabbc"), "bits")
    print("  waiting [3,1,2]      :", min_total_waiting([3, 1, 2]))

    print("\nWHERE GREEDY FAILS — same input, both algorithms")
    print("  coins [1,5,7] -> 10  : greedy", coin_change_greedy([1, 5, 7], 10),
          " dp", coin_change_dp([1, 5, 7], 10))
    print("  knapsack by ratio    : greedy",
          knapsack_greedy_by_ratio([6, 5, 5], [60, 40, 40], 10),
          " dp", knapsack_dp([6, 5, 5], [60, 40, 40], 10))
    print("  robber [5,10,6]      : greedy", rob_greedy([5, 10, 6]),
          " dp", rob_dp([5, 10, 6]))

    print("\nTHE SEARCH — does a counter-example exist?")
    found = find_counterexample(
        max_activities, best_activities_brute,
        lambda: ([(lambda s: (s, s + random.randint(1, 6)))(random.randint(0, 10))
                  for _ in range(random.randint(1, 8))],))
    print("  activities by end time:",
          "counter-example found!" if found else "none in 3,000 trials -> plausible")

    found = find_counterexample(
        rob_greedy, rob_dp,
        lambda: ([random.randint(0, 20) for _ in range(random.randint(1, 6))],))
    print("  house robber greedily :",
          f"BROKEN by {found[0][0]}: greedy {found[1]}, optimal {found[2]}"
          if found else "none found")
```

Run it and you get:

```
PROVABLY CORRECT GREEDY
  activities, by end   : 4
  activities, by start : 3
  activities, by length: 4
  brute force says     : 4
  fractional knapsack  : 240.0
  huffman 'aaabbc'     : 9 bits
  waiting [3,1,2]      : 4

WHERE GREEDY FAILS — same input, both algorithms
  coins [1,5,7] -> 10  : greedy 4  dp 2
  knapsack by ratio    : greedy 60  dp 80
  robber [5,10,6]      : greedy 10  dp 11

THE SEARCH — does a counter-example exist?
  activities by end time: none in 3,000 trials -> plausible
  house robber greedily : BROKEN by [6, 16, 20, 19, 1]: greedy 27, optimal 35
```

**`activities, by start : 3` against the correct `4`** is the wrong sort rule, made visible — **and by-length
happening to give 4 on this input is the more dangerous case**, because a rule that is wrong in general can
easily be right on your test.

**And the last two lines are the whole method.** Three thousand random trials found no counter-example for
sorting by end time — **which makes it plausible and is not a proof.** For house robber it found one
immediately, **and that is a proof: greedy is wrong, so write the DP.**

---

## 6. What it costs

**The shape of every greedy solution:**

```
  sort                     O(n log n)   <- dominates
  one pass                 O(n)
  running state            O(1)

  TOTAL: O(n log n) time, O(1) extra space
```

**Against the DP alternative, on the same problems:**

```
  problem                greedy         DP alternative
  ------------------------------------------------------------
  activity selection     O(n log n)     O(n^2) — check every pair
  fractional knapsack    O(n log n)     no DP needed (it is easier)
  Huffman                O(n log n)     no simple DP at all
  MST                    O(E log E)     no DP formulation
  shortest job first     O(n log n)     O(n!) by brute force
```

**Concretely, at `n = 100,000`:**

```
  greedy: 100,000 x 17 = 1,700,000 operations       ~0.3 s in Python
  DP:     100,000^2   = 10,000,000,000              ~3 hours

  and the DP would need 10^10 cells of memory, which does not exist.

-> when greedy is correct, it is not a constant-factor improvement.
   It is the difference between solvable and not.
```

**That gap is why identifying a correct greedy is worth the thirty seconds of checking.**

**The counter-example search, costed:**

```
  writing a brute force for n <= 12:      ~5 minutes
  3,000 random trials at n <= 8:          < 1 second

  what it settles: whether greedy is wrong (definitively)
  what it does not settle: whether greedy is right
```

**And the asymmetry is worth restating in cost terms:**

```
  finding a counter-example:  30 seconds, and you are DONE — write the DP
  failing to find one:        30 seconds, and you now owe an ARGUMENT
                              which may take another 5 minutes,
                              or may not exist

-> so the search is always worth running first, because half the
   time it ends the question immediately.
```

**Sorting cost, when the key is expensive:**

```
  sorting by a computed key — value/weight, or end - start —
  computes the key n log n times unless you use `key=`

  Python's sort computes `key` exactly n times (a Schwartzian transform):
    sorted(items, key=lambda x: expensive(x))   -> n evaluations
    sorted(items, cmp_to_key(...))              -> n log n comparisons

-> always use `key=`, never a comparator, when the key is computed
```

**The four correct greedies, by cost:**

```
  activity selection     sort O(n log n) + one pass          O(n log n)
  fractional knapsack    sort by ratio + one pass            O(n log n)
  Huffman                n heap operations                   O(n log n)
  Kruskal MST            sort edges + union-find             O(E log E)
  Prim MST               heap over edges                     O(E log V)

  ALL of them are dominated by a sort or a heap.
  That is not a coincidence: greedy IS "process in the right order".
```

**And the memory difference, which is often the real win:**

```
  activity selection greedy:   O(1) — two variables
  the DP alternative:          O(n) or O(n^2)

  0/1 knapsack DP:             O(W) after the collapse
  fractional knapsack greedy:  O(1)

-> greedy solutions are usually constant-space, which matters more
   at scale than the time difference does.
```

---

## 7. The traps

**Writing greedy and not checking.**

```python
>>> coin_change_greedy([1, 5, 7], 10)
4
>>> coin_change_dp([1, 5, 7], 10)
2
```

**Four against two, on a three-coin input.** The greedy version is shorter, faster and wrong, **and it passes
every test built from ordinary denominations** — which is where the intuition comes from and why it survives
review.

**Assuming greedy fails because it is greedy.**

```python
>>> max_activities([(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,12),(2,14),(12,16)])
4
>>> best_activities_brute([(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,12),(2,14),(12,16)])
4
```

**Greedy is exactly right here**, and writing an `O(n²)` DP for it is twenty wasted minutes. **The mistake goes
both ways**, and after a month of dynamic programming the bias runs towards over-engineering.

**Sorting by the wrong thing.**

```python
>>> activities = [(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,12),(2,14),(12,16)]
>>> max_activities(activities)               # by end
4
>>> max_activities_by_start(activities)      # by start
3
```

**Three against four.** **The sort key is the entire algorithm**, and there is no error — just a smaller answer.
**And by-length gives the right answer on this input while being wrong in general**, which is worse, because
your test passes.

**Confusing fractional with 0/1.**

```python
>>> fractional_knapsack([6, 5, 5], [60, 40, 40], 10)
100.0
>>> knapsack_greedy_by_ratio([6, 5, 5], [60, 40, 40], 10)
60
>>> knapsack_dp([6, 5, 5], [60, 40, 40], 10)
80
```

**Three different numbers for three different problems.** **The ratio rule is provably optimal for the
fractional version and provably wrong for the 0/1 version**, and the only difference is whether you may cut an
item. **Check that first.**

**Taking "no counter-example found" as proof.**

```python
>>> # 3,000 random trials, no mismatch
>>> # -> greedy is PLAUSIBLE
>>> # -> it is NOT proved
>>> # random small inputs may simply not contain the failing shape
```

**The asymmetry is the whole point.** **One counter-example is proof of failure; a thousand successes are
evidence and not proof.** If you cannot construct the argument, **say so and write the DP**, which is always
correct.

**Greedy that is right for the count and wrong for the set.**

```python
>>> # "the maximum NUMBER of non-overlapping intervals" -> greedy by end time
>>> # "the maximum TOTAL VALUE of non-overlapping intervals" -> NOT greedy
>>> #   a single high-value long interval can beat three short ones
>>> #   -> weighted interval scheduling is DP
```

**Adding weights breaks it**, and the two problems read almost identically. **Look for "maximum number" against
"maximum value" in the statement.**

**Not sorting at all.**

```python
>>> intervals = [(3, 5), (1, 4)]
>>> count, last_end = 0, float("-inf")
>>> for s, e in intervals:                   # unsorted!
...     if s >= last_end:
...         count, last_end = count + 1, e
>>> count
1
```

**One instead of two.** **A greedy algorithm is "process in the right order"** — without the sort there is no
algorithm, only a loop.

**Mutating the caller's list.**

```python
>>> data = [(3, 5), (1, 4)]
>>> max_activities(data)      # if it used data.sort() in place
2
>>> data
[(1, 4), (3, 5)]              # reordered, silently
```

**`sorted()` rather than `.sort()`** unless you mean to reorder the input — **and in an interview, saying "I
will not mutate the input" is a small, cheap signal.**

---

## 8. In the interview

### How it gets asked

- *"Can you solve this greedily?"* — asked directly, and the answer is a counter-example or an argument.
- *"Why does sorting by end time work?"* — the exchange argument.
- *"Why not sort by start time, or by duration?"* — the counter-examples.
- *"Is this greedy or DP?"* — the diagnostic.
- *"Prove your greedy choice is safe."* — tomorrow's lesson, and the shape is worth having today.
- *"What if the intervals have values?"* — the trap that turns greedy into DP.

### The first ninety seconds

> "Before I choose an approach I want to settle whether greedy works, **because if it does the solution is one
> sort and one pass, and if it does not I need a table.**
>
> **The greedy candidate here is: sort by something and take items in order, never reconsidering.**
>
> **And greedy needs two properties, both of them.** **Optimal substructure** — after making a choice, what
> remains is the same problem on a smaller input — **which it shares with dynamic programming.** And **the
> greedy choice property**: there is always *an* optimal solution that contains the locally best choice.
> **That second one is what greedy adds, and it is the one that is usually false.**
>
> **So my first move is to try to break it, and I give myself about thirty seconds.**
>
> **I look for an input where the locally best choice blocks two smaller things that together beat it.** That
> is where counter-examples live, and they are usually three or four elements long.
>
> **For instance, on house robber: values five, ten, six.** Greedy takes the ten, which forbids both
> neighbours, giving ten. **Taking the five and the six — which are not adjacent — gives eleven.** **Broken, in
> three elements, so it is DP.**
>
> **If I find one, I stop and write the table, and I say the counter-example out loud** — it is the
> justification for the DP, and it is a better answer than the DP alone.
>
> **If I cannot find one, greedy is plausible and I owe an argument**, which is usually an exchange argument:
> take any optimal solution, swap the greedy choice into it, show it does not get worse. **Therefore some
> optimal solution contains the greedy choice, and induction does the rest.**
>
> **And I would be explicit about the asymmetry.** A counter-example is a proof of failure. **Failing to find
> one is evidence, not proof** — so if I cannot construct the argument either, **I say that and write the DP**,
> which is always correct.
>
> **Looking at this problem specifically**: it asks for the maximum *number* of non-overlapping intervals, not
> the maximum value. **That word matters** — with values it is dynamic programming, and without them I believe
> greedy by end time is correct, and I can argue why."

### The follow-ups

**"Why does sorting by end time work, and not by start time or duration?"**

> "The exchange argument, and I would give it as the intuition first and then the swap.
>
> **The intuition: choosing the interval that finishes earliest leaves the most room for everything after
> it.** Nothing else about an interval matters for what comes next — **only when the resource becomes free
> again.**
>
> **The formal version is a swap.** Take any optimal selection. Look at its first interval. **If it is not the
> globally earliest-finishing interval, replace it with that one.** The replacement finishes no later, so it
> cannot conflict with anything the original selection contained after it. **So the swapped selection is still
> valid and has the same size — it is still optimal.**
>
> **Therefore there is an optimal solution containing the greedy choice**, and repeating the argument on what
> remains gives the result by induction.
>
> **Now the wrong rules, and I would show rather than assert.**
>
> **Sorting by start time fails immediately.** One interval from zero to ten, and three short ones inside it.
> **The earliest-starting is the long one, it is taken, and it blocks all three** — greedy gets one, the answer
> is three.
>
> **Sorting by duration is the more interesting failure, because it feels right.** Take a short interval in the
> middle that overlaps two longer ones which do not overlap each other. **Greedy takes the short one and blocks
> both** — one instead of two.
>
> **And the reason both fail is the same**: neither start time nor duration tells you **when the resource
> becomes free**, which is the only thing that constrains the future.
>
> **One warning I would add: the wrong rules often give the right answer.** On a typical test input,
> sorting by duration frequently matches. **So the fact that your solution passes the examples tells you
> almost nothing** — which is why the argument matters more than the test."

**"What if the intervals have values, and you want the maximum total value?"**

> "Then greedy fails, and it is worth showing precisely how, because the two problems read almost identically.
>
> **With unweighted intervals, every interval is worth one, so more intervals is always better** — and
> finishing early always leaves more room. **The greedy choice is safe.**
>
> **With values, that stops being true.** **One interval worth a hundred can beat three worth ten each**, and
> no local rule sees that. Sorting by end time takes the three; sorting by value takes the hundred and might
> block four worth thirty each.
>
> **Concretely: an interval from zero to ten worth a hundred, and three from zero to three, three to six, six
> to nine, each worth ten.** Greedy by end time takes the three short ones for thirty. **The optimal answer is
> the long one, for a hundred.**
>
> **So it becomes weighted interval scheduling, which is dynamic programming.**
>
> **The state: sort by end time, and `dp[i]` is the best total value using the first `i` intervals.** For each
> interval, either skip it — `dp[i-1]` — or take it, in which case add its value to `dp[j]`, where `j` is the
> last interval that finishes before this one starts.
>
> **And finding `j` is a binary search over the sorted end times**, which keeps it `O(n log n)` rather than
> `O(n²)`.
>
> **Which is a nice outcome: the DP is the same complexity as the greedy here**, because the sort dominates
> both. **So the cost of the greedy failing is a table and some code, not an asymptotic penalty.**
>
> **The general lesson I would draw: 'maximum number' and 'maximum value' are one word apart in the problem
> statement and are different algorithms.** I read for that word specifically, **because the greedy solution
> passes the unweighted examples and silently fails the weighted ones.**"

**"How do you decide, in general, whether a problem is greedy?"**

> "I run a specific procedure, and it takes about thirty seconds, and the asymmetry in it is the important
> part.
>
> **First, I try to break it.** I construct small inputs — three or four elements — where the locally best
> choice leads somewhere worse. **The place to look is where the greedy choice is large and blocks two smaller
> things that together beat it**, which is the shape of almost every counter-example.
>
> **Coins one, five and seven, amount ten: greedy takes seven and needs three ones — four coins — and the
> answer is five plus five.** House robber with five, ten, six: **greedy takes ten and blocks both
> neighbours; five plus six is eleven.** Knapsack by value per kilo with a six-kilo item and two five-kilo
> items in a ten-kilo bag: **greedy takes the best ratio and then nothing fits.**
>
> **All three are three items long. This check is fast.**
>
> **If I find one, I am done: it is DP, and I say the counter-example out loud**, because it is the
> justification for the table and it demonstrates more than the table does.
>
> **If I cannot find one, greedy is plausible and I owe an argument.** The usual one is an exchange argument —
> **take any optimal solution, swap in the greedy choice, show it does not get worse** — and there is a
> variant, "greedy stays ahead", where you show greedy's partial solution is at least as good as any other's at
> every step.
>
> **And here is the asymmetry, which I would state explicitly.** **A counter-example is a proof that greedy
> fails. Failing to find one is not a proof that it works.** Random small inputs may simply not contain the
> failing shape.
>
> **So if I cannot construct the argument, I say so and write the DP.** The DP is always correct, and **the
> cost of unnecessary DP is some code, while the cost of unjustified greedy is a wrong answer.** Those are not
> symmetric either.
>
> **One practical habit: I would write a brute force for small inputs and check the greedy against it on a few
> thousand random cases.** Five minutes, and it settles the question in one direction definitively."

### The model answer

*"You run a single meeting room. You are given a list of requested meetings, each with a start and end time.
Schedule as many as possible."*

> "This is activity selection, and I want to establish whether greedy works before writing anything, **because
> if it does this is six lines and if it does not it is a table.**
>
> **One clarification first: as many *meetings* as possible, or as much *value* as possible?** If the meetings
> have priorities or lengths that matter, this is a different problem. **Taking it as: maximise the count, all
> meetings equal.** And I would confirm whether a meeting ending at three and another starting at three
> conflict — **I will assume they do not, and say so, because it changes one comparison.**
>
> **The greedy candidate is: sort by something and take meetings in order, skipping any that conflict with
> what I have already taken.**
>
> **The question is what to sort by, and there are three plausible answers.**
>
> **By start time**, which fails immediately: a meeting from nine to five is the earliest to start and blocks
> the whole day. **Greedy gets one; the answer might be eight.**
>
> **By duration**, which feels right and is wrong. **A short meeting in the middle of the day can overlap two
> longer ones that do not overlap each other** — greedy takes the short one and gets one instead of two.
>
> **By end time, which is correct**, and I can argue it.
>
> **The intuition: the only thing about a meeting that constrains the future is when the room becomes free
> again.** Not when it starts, not how long it is. **So take the one that frees the room soonest.**
>
> **The exchange argument, properly.** Take any optimal schedule. **If its first meeting is not the
> earliest-finishing one, swap that in.** The replacement finishes no later, so it cannot conflict with
> anything that came after in the original schedule. **Same number of meetings, still valid, still optimal.**
> So some optimal schedule contains my greedy choice, **and the same argument applies to what remains.**
>
> **The algorithm: sort by end time, keep a running `last_end`, and take any meeting whose start is at least
> `last_end`.** Six lines.
>
> **Cost: `O(n log n)` for the sort, `O(n)` for the pass, `O(1)` extra space.** The sort dominates. **The DP
> alternative is `O(n²)`, so at a hundred thousand meetings greedy is a fraction of a second and the DP is
> hours** — this is not a constant-factor difference.
>
> **Two edge cases I would handle: an empty list gives zero, and meetings that touch at an endpoint** — which
> is the clarification I asked about, and it is a `>=` rather than a `>`.
>
> **And two follow-ups I would raise myself, because they are where this problem usually goes.**
>
> **If the meetings have values, greedy breaks.** One meeting worth a hundred beats three worth ten, and no
> local rule sees it. **That becomes weighted interval scheduling: sort by end time, and `dp[i]` is the best
> value using the first `i`, with a binary search to find the last compatible meeting.** Still `O(n log n)`,
> **so the cost of greedy failing here is a table, not a worse complexity.**
>
> **And if there are several rooms, the question changes entirely** — "how many rooms do I need" is a
> sweep-line problem, counting the maximum number of simultaneous meetings, **which is a different algorithm
> with a different correctness argument.** I would want to know which of the three questions is being asked
> before committing."

---

## 9. Recall card

**Greedy is a CLAIM, not a technique: the locally best choice is always part of *some* optimal solution.**
Two properties are needed — **optimal substructure** (shared with DP) and **the greedy choice property** (what
greedy adds, and what is usually false). Note the phrasing: *some* optimal solution, not *the* one.

**The decision procedure is thirty seconds: TRY TO BREAK IT.** Look where the greedy choice is large and
blocks two smaller things that together beat it. **Coins `[1,5,7]` to 10: greedy 4, optimal 2. House robber
`[5,10,6]`: greedy 10, optimal 11. 0/1 knapsack by ratio, cap 10, `(6,60),(5,40),(5,40)`: greedy 60, optimal
80.** All three are three items long.

**The asymmetry is the whole point: a counter-example PROVES greedy fails; failing to find one proves
nothing.** If you cannot construct the exchange argument either, say so and write the DP — **unnecessary DP
costs code; unjustified greedy costs a wrong answer.**

**The exchange argument: take any optimal solution, swap the greedy choice in, show it does not get worse.**
For activity selection — swap in the earliest finisher; it finishes no later, so it conflicts with nothing that
followed.

**Four provably-correct greedies: activity selection (sort by END time), fractional knapsack (value per kilo —
and the SAME rule fails for 0/1, because indivisibility is the difference), Huffman (merge the two rarest),
and MST (Kruskal/Prim).** All are dominated by a sort or a heap, because **greedy is "process in the right
order".**

**The sort key IS the algorithm.** By start time or by duration both fail on activity selection, **and by
duration often gives the right answer on your test**, which is worse. **And "maximum NUMBER" versus "maximum
VALUE" is one word apart and is greedy versus DP** — with values, weighted interval scheduling, still
`O(n log n)`.
