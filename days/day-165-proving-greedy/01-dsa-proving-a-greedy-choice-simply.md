---
day: 165
track: dsa
title: "Proving a greedy choice, simply"
phase: "Greedy and intervals"
status: written
---

# Proving a greedy choice, simply

## 1. What this is, and why they ask it

Yesterday ended with a gap: **if you cannot find a counter-example, you owe an argument.** Today is the
argument.

**There are exactly two, they are both short, and neither is a formal proof.** They are the sentences you say
out loud in an interview when asked "why does that work" — and **being able to say one of them is the
difference between "I think greedy works here" and "greedy works here, and here is why".**

They ask it because **it is the highest-value thirty seconds in an algorithms interview.** A candidate who
writes a correct greedy solution has produced code. **A candidate who writes it and then justifies it in two
sentences has demonstrated that they know it is correct rather than hoping** — and that distinction is
precisely what the interviewer is trying to measure and usually cannot.

The other reason is that **the argument is also a debugging tool.** Trying to construct the exchange argument
and failing is the fastest way to discover that greedy does not work. **The proof attempt and the
counter-example search are the same activity from opposite ends**, and doing both takes about a minute.

**One thing to be clear about, because it matters for how you use this day.** These are not proofs in the
mathematical sense — **they are proof *sketches*, and that is what is wanted.** Nobody expects induction on
paper. **They expect you to be able to say why the first choice cannot hurt.**

By the end of this lesson you can produce both arguments for any greedy algorithm, know which to reach for,
recognise when neither works, and say the whole thing in under thirty seconds.

---

## 2. The story

The dispute was about a wall and it had been going for two years and Fatima had been asked to settle it because
everybody trusted her and nobody else was speaking.

**Two brothers, one plot, one wall between them, and the wall was eleven inches onto one side.**

The younger brother had documents. The elder brother had a different set of documents. **Both sets were real
and neither settled anything**, because they described the plot from different corners.

And the meeting she called went the way those meetings go, which is that each of them explained why he was
right for forty minutes.

**What she did in the end was not adjudicate. It was something smaller and it worked.**

She turned to the elder brother and said: **"Suppose your brother is right. Suppose the wall is his. Show me
what you lose."**

And he started to say something about principle, and she stopped him, and made him actually walk it. **Eleven
inches along thirty feet. A strip you could not stand in.**

Then she turned to the younger one. **"Now suppose your brother is right. Show me what you lose."**

The same strip.

**"So whichever way I decide, neither of you loses anything you can use."**

Which did not settle it, and it changed the argument entirely, **because both of them had been assuming the
other was gaining something.**

Then she did the second thing, and it was the one that actually ended it.

**"Take whatever arrangement you both think is fairest. Any arrangement. Now move the wall eleven inches. Tell
me what gets worse."**

And they could not find anything.

**"Then it does not matter,"** she said. **"You have been arguing for two years about a change that makes no
arrangement worse. Put it where it is and go home."**

Her son asked her afterwards how she had known that would work.

**"I did not know. I asked them to make it worse and they could not. That is not the same as being sure. It is
just the only thing you can actually check."**

---

## 3. The idea in plain English

Fatima's second question — **take any arrangement, make the change, and show me what gets worse** — is the
exchange argument, and it is the more useful of the two.

**Start with what you are trying to establish, precisely.**

**Greedy makes a first choice. Everything after that is the same problem on a smaller input.** So **if the
first choice is safe, and the same argument applies to what remains, the whole thing is optimal by
induction.**

> **"Safe" means: there is at least one optimal solution that contains this choice.**

**Not that every optimal solution contains it.** Not that the choice is "the best". **Only that you have not
ruled out optimality by making it** — which is a much weaker and much more provable claim.

**Now the two arguments.**

**Argument one: the exchange argument. "Any optimal solution can be modified to include my choice, without
getting worse."**

**The shape is always the same, in three steps:**

```
1. Take ANY optimal solution O. (Not the greedy one. Any.)
2. If O already contains my greedy choice g, done.
3. If not, O contains something else, x, where g would go.
   SWAP x for g, and show the result is still valid and no worse.
   -> so there IS an optimal solution containing g.
```

**Step three is the whole argument**, and it has two halves that must both be shown: **the swapped solution is
still legal** — it does not violate a constraint — **and it is no worse** — the objective did not decrease.

**Activity selection, done properly:**

> **Claim: the interval that finishes earliest is in some optimal selection.**
>
> Take any optimal selection `O`, and look at its first interval `x`. **My greedy choice `g` finishes no later
> than `x`** — because `g` finishes earliest of all of them.
>
> **Swap `x` for `g`.** Is it still legal? **Yes** — everything in `O` after `x` started at or after `x`
> finished, and `g` finishes no later than `x`, so nothing overlaps.
>
> **Is it worse? No** — it has exactly the same number of intervals.
>
> **So `O` with `g` swapped in is still optimal, and it contains `g`.**

**Six sentences, and that is a complete argument for the canonical greedy.** In an interview it compresses to
**"swapping in the earliest finisher cannot create a conflict, because it finishes no later than whatever it
replaced".**

**Argument two: "greedy stays ahead". "At every step, my partial solution is at least as good as anyone
else's."**

**Instead of modifying an optimal solution, you compare progress directly:**

```
1. Let g1, g2, g3, ... be greedy's choices in order.
2. Let o1, o2, o3, ... be any other valid solution's, in order.
3. Show by induction: after k choices, greedy is at least as far along
   as the other solution.
4. Therefore greedy cannot run out of room sooner, so it makes at
   least as many choices.
```

**For activity selection, "at least as far along" means "greedy's k-th interval finishes no later than yours
does".** Which is true at `k = 1` by definition, **and stays true because greedy always picks the earliest
compatible interval.**

**And then the conclusion: if greedy's k-th choice always finishes earliest, greedy can never be forced to
stop before you.**

**When to use which.**

```
  EXCHANGE ARGUMENT              STAYS AHEAD
  "I can swap my choice into     "My partial answer is always at
   any optimal solution"          least as good as yours"

  good for: selection problems    good for: problems with a natural
  where the answer is a SET       ORDER and a running measure

  activity selection              activity selection (both work)
  MST (the cut property)          shortest path
  Huffman                         scheduling by deadline
  fractional knapsack

  MOST OF THE TIME, USE EXCHANGE. It is shorter to say and it
  applies more widely.
```

**Now the third thing, which is what makes this practical: the failed proof is a counter-example generator.**

**When you try to construct the exchange argument and cannot, the place where it fails tells you what the
counter-example looks like.**

**Try it on 0/1 knapsack with the ratio rule:**

> Take any optimal solution `O`. My greedy choice `g` is the item with the best value per kilo. If `O` does not
> contain `g`, swap something out for `g`.
>
> **But what do I swap out?** `g` might be heavier than any single item in `O`, **so removing one item might
> not make room.** And removing two might lose more value than `g` adds.
>
> **The argument fails exactly there — at "might not make room" — and that is the counter-example.**

**A heavy high-ratio item, and two lighter items that together fill the bag better.** `(6kg, 60)` against two
`(5kg, 40)` items in a ten-kilo bag. **The failure of the proof told you the shape of the input.**

**And the contrast with the fractional version is the whole lesson**: there, **you can always swap in a
*fraction* of `g`**, so "might not make room" never arises. **The exchange goes through, and the algorithm is
correct.**

**Finally: what to actually say, and how long it should take.**

**Thirty seconds, three sentences:**

> **"The greedy choice is X. Take any optimal solution — if it does not contain X, swap X in for whatever it
> used instead. That swap is still legal because [reason], and no worse because [reason], so there is an
> optimal solution containing X."**

**Fill in the two bracketed reasons and you are done.** If you cannot fill them in, **say so** — "I cannot
construct the exchange argument, which makes me suspect greedy fails here, so I will write the DP" **is an
excellent answer**, and it is honest.

---

## 4. The picture

The exchange argument, drawn:

```
   ANY OPTIMAL SOLUTION O          AFTER THE SWAP

   [ x ][ b ][ c ][ d ]            [ g ][ b ][ c ][ d ]
     ^                               ^
   whatever O used                 my greedy choice
   in the first slot

   TWO THINGS TO SHOW:
     1. STILL LEGAL   — no constraint is violated
     2. NO WORSE      — the objective did not decrease

   -> therefore SOME optimal solution contains g
   -> repeat on the remainder. Induction does the rest.

   Note what is NOT claimed: that every optimal solution contains g,
   or that g is "the best". Only that choosing g does not rule out
   optimality.
```

Activity selection, the swap in detail:

```
   time ------------------------------------------->

   O's first choice x:      [-------x-------]
   greedy's choice g:   [--g--]
                             ^ g finishes NO LATER than x

   the rest of O:                        [--b--] [--c--]
                                          ^ starts at or after x ends

   swap x -> g:         [--g--]          [--b--] [--c--]
                             ^ g ends even earlier, so b still fits

   LEGAL: yes — g ends no later than x, so nothing that fitted
          after x can now conflict
   WORSE: no — same count

   That is the entire proof, in one picture.
```

"Greedy stays ahead", drawn:

```
   step:        1        2        3        4
   greedy:   ends 4   ends 7   ends 9   ends 12
   any other: ends 6   ends 8   ends 11  ends 15
              ^        ^        ^        ^
              <=       <=       <=       <=      at EVERY step

   greedy's k-th choice always finishes no later than yours.

   -> greedy is never the one that runs out of room first
   -> so it makes at least as many choices
   -> so it is optimal

   USE THIS when there is a natural ORDER and a running MEASURE.
   Use EXCHANGE otherwise — it is shorter and applies more widely.
```

The failed proof as a counter-example generator:

```
   0/1 KNAPSACK, greedy by value per kilo

   attempt the exchange:
     take any optimal O. If it lacks g (the best ratio), swap g in.
     what comes out?
       - g may be HEAVIER than any single item in O
       - so removing ONE may not make room                  <-- FAILS HERE
       - and removing TWO may lose more than g adds

   THE FAILURE POINT IS THE COUNTER-EXAMPLE:
     a HEAVY high-ratio item, and TWO lighter items that together
     do better

     capacity 10:  (6kg, 60) ratio 10
                   (5kg, 40) ratio 8
                   (5kg, 40) ratio 8
     greedy: 60.  optimal: 80.

   AND THE FRACTIONAL VERSION:
     you can swap in a FRACTION of g, so "may not make room"
     never arises -> the exchange goes through -> correct.

   The proof attempt and the counter-example search are the SAME
   ACTIVITY from opposite ends.
```

The four canonical arguments, side by side:

```
  ACTIVITY SELECTION (sort by end time)
    swap in the earliest finisher: it ends no later, so nothing
    that fitted before still conflicts. Same count.

  FRACTIONAL KNAPSACK (sort by ratio)
    if O uses a worse ratio anywhere, replace some of it with an
    equal WEIGHT of the best ratio. Same weight, more value.
    (Works only because you can take a fraction.)

  HUFFMAN (merge the two rarest)
    in any optimal tree, the two deepest leaves are siblings.
    Swap the two rarest symbols into those positions: total cost
    cannot increase, because rarer symbols moved deeper.

  SHORTEST JOB FIRST (sort by duration)
    if any adjacent pair is out of order, swapping them reduces
    the total wait by the difference. So sorted order is optimal.
    (This one is an EXCHANGE on ADJACENT elements — the simplest form.)
```

What to say, and how long:

```
   THIRTY SECONDS, THREE SENTENCES:

   "The greedy choice is X."
   "Take any optimal solution; if it does not contain X, swap X in
    for whatever it used there."
   "That is still legal because ___, and no worse because ___ —
    so some optimal solution contains X."

   FILL IN THE TWO BLANKS. If you cannot:
     "I cannot construct the exchange argument, which makes me
      suspect greedy fails, so I will write the DP."

   That is an EXCELLENT answer. It is honest, it is specific, and
   it names the reason.
```

---

## 5. The code, built step by step

**This lesson is about arguments rather than algorithms, so the code here does two things: it *checks* the
arguments empirically, and it makes the failure points visible.**

### Verifying an exchange argument empirically

```python
def exchange_holds(problem, greedy_choice, is_valid, value, trials=2000):
    """For random optimal solutions, can the greedy choice be swapped in?"""
    failures = []
    for _ in range(trials):
        instance = problem.generate()
        best = problem.brute_force_optimal(instance)      # a full optimal solution
        g = greedy_choice(instance)
        if g in best:
            continue                                       # already contains it
        for x in best:
            swapped = (best - {x}) | {g}
            if is_valid(instance, swapped) and value(swapped) >= value(best):
                break                                      # the exchange worked
        else:
            failures.append((instance, best, g))           # NO swap worked
    return failures
```

**This does not prove anything**, and it does something almost as useful: **it finds the instances where no
swap works**, which is exactly where your intuition is wrong.

**The `for ... else` is doing real work here** — the `else` runs only if no `break` happened, meaning **every
possible swap failed.**

### Activity selection, with the argument as a comment

```python
def max_activities(intervals: list[tuple[int, int]]) -> int:
    """
    Greedy: always take the compatible interval that finishes earliest.

    EXCHANGE ARGUMENT
      Take any optimal selection O and its first interval x.
      The earliest-finishing interval g ends no later than x.
      Swapping x for g is still LEGAL: everything O scheduled after x
      began at or after x ended, and g ends no later than x.
      It is NO WORSE: the count is unchanged.
      So some optimal solution contains g. Induct on the remainder.
    """
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

**Writing the argument as a docstring is a habit worth having**, and not for the reader — **for you.** If you
cannot write it, you do not know the algorithm is correct, **and you find that out while writing rather than
in an interview.**

### Shortest job first: the adjacent-swap argument, which is the simplest form

```python
def min_total_waiting(durations: list[int]) -> int:
    """
    Greedy: shortest job first.

    ADJACENT EXCHANGE ARGUMENT
      Suppose two adjacent jobs are out of order: a longer job of
      length L before a shorter one of length S.
      Swapping them changes only THOSE TWO jobs' waiting times, and
      it reduces the total by (L - S) > 0.
      So any schedule with an out-of-order adjacent pair is NOT
      optimal. Therefore the sorted order is optimal.
    """
    elapsed, total = 0, 0
    for d in sorted(durations):
        total += elapsed
        elapsed += d
    return total


def waiting_time(order: list[int]) -> int:
    elapsed, total = 0, 0
    for d in order:
        total += elapsed
        elapsed += d
    return total
```

**The adjacent-swap form is the easiest exchange argument to construct**, because **you only have to reason
about two elements** — everything else in the schedule is unaffected. **Look for it first.**

### Demonstrating the adjacent swap

```python
def show_adjacent_swap(durations: list[int]) -> None:
    """Every out-of-order adjacent pair can be improved. Show it."""
    for i in range(len(durations) - 1):
        if durations[i] > durations[i + 1]:
            swapped = durations[:]
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            before, after = waiting_time(durations), waiting_time(swapped)
            print(f"  swapping positions {i},{i+1}: {before} -> {after}"
                  f"  (saved {before - after}, = {durations[i]}-{durations[i+1]})")
            return
    print("  already sorted — no adjacent pair is out of order")
```

**The saving is exactly the difference between the two durations**, which is the arithmetic the argument
depends on — **and seeing it come out exactly right is more convincing than the algebra.**

### Where the argument fails: 0/1 knapsack

```python
def why_ratio_fails_for_01() -> None:
    """The exchange breaks at 'swapping in g may not make room'."""
    weights, values, capacity = [6, 5, 5], [60, 40, 40], 10
    ratios = [v / w for w, v in zip(weights, values)]
    print(f"  ratios: {[round(r, 1) for r in ratios]}")
    print(f"  greedy takes item 0 (ratio {ratios[0]}), leaving room 4 — nothing fits")
    print(f"  greedy value : {60}")
    print(f"  optimal      : {80}  (items 1 and 2)")
    print("  THE EXCHANGE FAILS AT: 'swap g in for one item of O'")
    print("  -> g weighs 6; removing ONE 5kg item leaves room 5, not 6")
    print("  -> removing BOTH loses 80 to gain 60")
    print("  -> the failure point IS the counter-example's shape")
```

**Printing the failure point rather than only the numbers** is the pedagogical bit: **the counter-example is
not a coincidence, it is what the broken step describes.**

### And where it succeeds: fractional knapsack

```python
def why_ratio_works_for_fractional() -> None:
    """The same exchange, with fractions allowed, goes through."""
    print("  take any optimal solution O")
    print("  if O contains ANY item with a worse ratio than g,")
    print("    remove an equal WEIGHT of it and add that weight of g")
    print("  -> same total weight (so still legal)")
    print("  -> more value (so no worse)")
    print("  'may not make room' NEVER ARISES, because fractions exist")
    print("  -> the exchange goes through -> greedy is optimal")
```

**Putting the two side by side is the point of the lesson**: **the same sort rule, the same attempted
argument, and one word of difference in the problem statement decides whether it works.**

### Huffman: the argument that is not obvious

```python
import heapq
from collections import Counter

def huffman_cost(text: str) -> int:
    """
    Greedy: repeatedly merge the two least frequent symbols.

    EXCHANGE ARGUMENT
      In any optimal prefix code, the two DEEPEST leaves are siblings
      (otherwise you could move one up and do better).
      If the two rarest symbols are not already there, swap them into
      those positions.
      Swapping a rarer symbol DEEPER and a commoner one SHALLOWER
      cannot increase the total cost, because cost = sum of
      frequency x depth.
      So some optimal tree has the two rarest as sibling leaves —
      which is exactly what merging them assumes.
    """
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
```

**"Swapping a rarer symbol deeper and a commoner one shallower cannot increase the total" is the whole
argument**, and it is one sentence — **which is what makes Huffman a good thing to have rehearsed.**

### The complete solution

```python
"""Proving greedy: the two arguments, and what a failed proof tells you."""

import heapq
import random
from collections import Counter
from itertools import combinations


# ---------- the algorithms, each with its argument ----------

def max_activities(intervals: list[tuple[int, int]]) -> int:
    """
    EXCHANGE: swap in the earliest finisher. It ends no later than
    whatever it replaced, so nothing that fitted after still conflicts,
    and the count is unchanged.
    """
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count


def waiting_time(order: list[int]) -> int:
    elapsed, total = 0, 0
    for d in order:
        total += elapsed
        elapsed += d
    return total


def min_total_waiting(durations: list[int]) -> int:
    """
    ADJACENT EXCHANGE: any out-of-order adjacent pair can be swapped
    to reduce the total by exactly (longer - shorter). So a schedule
    with any such pair is not optimal.
    """
    return waiting_time(sorted(durations))


def huffman_cost(text: str) -> int:
    """
    EXCHANGE: in any optimal tree the two deepest leaves are siblings.
    Moving the two rarest symbols there cannot increase
    sum(frequency x depth).
    """
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


# ---------- making the arguments visible ----------

def show_adjacent_swap(durations: list[int]) -> None:
    for i in range(len(durations) - 1):
        if durations[i] > durations[i + 1]:
            swapped = durations[:]
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            before, after = waiting_time(durations), waiting_time(swapped)
            print(f"    {durations} -> {swapped}")
            print(f"    total wait {before} -> {after}, saved {before - after} "
                  f"= {durations[i]} - {durations[i+1]}")
            return
    print("    already sorted")


def stays_ahead_table(intervals: list[tuple[int, int]],
                      other: list[tuple[int, int]]) -> None:
    """Greedy's k-th choice finishes no later than any other schedule's."""
    greedy: list[tuple[int, int]] = []
    last = float("-inf")
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s >= last:
            greedy.append((s, e))
            last = e
    print(f"    {'step':>5} {'greedy ends':>12} {'other ends':>12}")
    for k in range(max(len(greedy), len(other))):
        g = greedy[k][1] if k < len(greedy) else "-"
        o = other[k][1] if k < len(other) else "-"
        mark = "<=" if isinstance(g, int) and isinstance(o, int) and g <= o else ""
        print(f"    {k+1:>5} {str(g):>12} {str(o):>12}  {mark}")


def why_ratio_fails_for_01() -> None:
    print("    ratios: 6kg/60 = 10.0,  5kg/40 = 8.0,  5kg/40 = 8.0")
    print("    greedy takes the 6kg item; 4kg of room left; nothing fits -> 60")
    print("    optimal takes both 5kg items                              -> 80")
    print("    THE EXCHANGE FAILS AT: 'swap g in for one item of O'")
    print("      g weighs 6; removing one 5kg item leaves room 5, not 6")
    print("      removing both loses 80 to gain 60")
    print("    -> the failure point IS the shape of the counter-example")


def why_ratio_works_for_fractional() -> None:
    print("    if O contains any item with a worse ratio than g,")
    print("      remove an equal WEIGHT of it and add that weight of g")
    print("    same total weight (legal), more value (no worse)")
    print("    'may not make room' never arises, because fractions exist")
    print("    -> the exchange goes through -> greedy is optimal")


# ---------- the empirical check ----------

def brute_force_activities(intervals: list[tuple[int, int]]) -> set:
    """The largest compatible subset. Exponential and obviously correct."""
    best: set = set()
    n = len(intervals)
    for size in range(n, 0, -1):
        for combo in combinations(range(n), size):
            chosen = sorted(intervals[i] for i in combo)
            if all(chosen[i][1] <= chosen[i + 1][0] for i in range(len(chosen) - 1)):
                return set(combo)
    return best


def exchange_check(trials: int = 400) -> tuple[int, int]:
    """For random optima not containing the greedy choice, can we swap it in?"""
    worked = failed = 0
    for _ in range(trials):
        n = random.randint(2, 7)
        intervals = []
        for _ in range(n):
            s = random.randint(0, 10)
            intervals.append((s, s + random.randint(1, 5)))
        best = brute_force_activities(intervals)
        g = min(range(n), key=lambda i: intervals[i][1])   # earliest finisher
        if g in best:
            continue
        for x in best:
            swapped = sorted(intervals[i] for i in (best - {x}) | {g})
            if all(swapped[i][1] <= swapped[i + 1][0]
                   for i in range(len(swapped) - 1)):
                worked += 1
                break
        else:
            failed += 1
    return worked, failed


if __name__ == "__main__":
    random.seed(0)

    print("ARGUMENT 1 — ADJACENT EXCHANGE (shortest job first)")
    show_adjacent_swap([3, 1, 2])
    print(f"    sorted total wait: {min_total_waiting([3, 1, 2])}")
    print(f"    worst order      : {waiting_time(sorted([3, 1, 2], reverse=True))}")

    print("\nARGUMENT 2 — GREEDY STAYS AHEAD (activity selection)")
    acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
    stays_ahead_table(acts, [(0, 6), (6, 10)])

    print("\nTHE EXCHANGE, CHECKED EMPIRICALLY (activity selection)")
    worked, failed = exchange_check()
    print(f"    optima not containing the greedy choice: {worked + failed}")
    print(f"    a swap worked: {worked}    no swap worked: {failed}")
    print("    (failures would mean the exchange argument is WRONG)")

    print("\nWHERE THE ARGUMENT FAILS — 0/1 knapsack by ratio")
    why_ratio_fails_for_01()

    print("\nWHERE THE SAME ARGUMENT SUCCEEDS — fractional knapsack")
    why_ratio_works_for_fractional()

    print("\nHUFFMAN — one sentence")
    print("    swapping a rarer symbol DEEPER and a commoner one")
    print("    SHALLOWER cannot increase sum(frequency x depth)")
    print(f"    cost of 'aaabbc': {huffman_cost('aaabbc')} bits")
```

Run it and you get:

```
ARGUMENT 1 — ADJACENT EXCHANGE (shortest job first)
    [3, 1, 2] -> [1, 3, 2]
    total wait 7 -> 5, saved 2 = 3 - 1
    sorted total wait: 4
    worst order      : 8

ARGUMENT 2 — GREEDY STAYS AHEAD (activity selection)
     step  greedy ends   other ends
        1            4            6  <=
        2            7           10  <=
        3           11            -

THE EXCHANGE, CHECKED EMPIRICALLY (activity selection)
    optima not containing the greedy choice: 81
    a swap worked: 81    no swap worked: 0
    (failures would mean the exchange argument is WRONG)

WHERE THE ARGUMENT FAILS — 0/1 knapsack by ratio
    ratios: 6kg/60 = 10.0,  5kg/40 = 8.0,  5kg/40 = 8.0
    greedy takes the 6kg item; 4kg of room left; nothing fits -> 60
    optimal takes both 5kg items                              -> 80
    THE EXCHANGE FAILS AT: 'swap g in for one item of O'
      g weighs 6; removing one 5kg item leaves room 5, not 6
      removing both loses 80 to gain 60
    -> the failure point IS the shape of the counter-example

WHERE THE SAME ARGUMENT SUCCEEDS — fractional knapsack
    if O contains any item with a worse ratio than g,
      remove an equal WEIGHT of it and add that weight of g
    same total weight (legal), more value (no worse)
    'may not make room' never arises, because fractions exist
    -> the exchange goes through -> greedy is optimal

HUFFMAN — one sentence
    swapping a rarer symbol DEEPER and a commoner one
    SHALLOWER cannot increase sum(frequency x depth)
    cost of 'aaabbc': 9 bits
```

**`a swap worked: 81, no swap worked: 0`** is the exchange argument checked rather than asserted. **A single
failure there would mean the argument is wrong**, and running it once is worth more than reading the proof
twice.

**And the adjacent swap saving exactly `3 - 1 = 2`** is the arithmetic the argument depends on, coming out
exactly as predicted.

---

## 6. What it costs

**The arguments cost nothing to run and about thirty seconds to say.**

```
  construct the exchange argument:   ~30 seconds, out loud
  write it as a docstring:           ~1 minute
  check it empirically:              ~10 minutes to write, seconds to run
```

**Against what it buys:**

```
  a correct greedy with no justification:
    -> the interviewer cannot tell whether you knew or guessed
    -> and the follow-up "why does that work?" is coming

  a correct greedy WITH the argument:
    -> demonstrably knew
    -> and the same 30 seconds would have caught it if it were wrong
```

**The asymmetry between the two directions:**

```
  finding a counter-example         PROVES greedy is wrong
  constructing the exchange         STRONGLY suggests it is right
                                    (it is a sketch, not a formal proof)
  neither one                       -> write the DP, and say why

  cost of unnecessary DP:           some code, same complexity often
  cost of unjustified greedy:       a wrong answer
```

**The empirical check, costed:**

```
  brute force for n <= 8:                 ~5 minutes to write
  400 random instances:                   < 1 second to run
  what it tests: whether ANY swap works for real optima

  and the result is binary and informative:
    0 failures  -> the exchange holds on everything tested
    1 failure   -> the argument is WRONG, and you have the instance
```

**The four canonical arguments, by length:**

```
  shortest job first     1 sentence  (adjacent swap; the simplest form)
  activity selection     2 sentences (swap in the earliest finisher)
  Huffman                2 sentences (rarest symbols go deepest)
  fractional knapsack    2 sentences (swap an equal WEIGHT)
  MST cut property       2 sentences (the lightest edge across any cut)

  -> all five fit in under thirty seconds of speech.
     That is the entire memorisation burden of this lesson.
```

**And the algorithms themselves, for reference:**

```
  activity selection    O(n log n), dominated by the sort
  shortest job first    O(n log n), dominated by the sort
  Huffman               O(n log n), dominated by the heap
  fractional knapsack   O(n log n), dominated by the sort

  the ARGUMENT costs nothing at runtime. It is entirely a
  design-time and interview-time activity.
```

**Where the DP alternative sits, when greedy fails:**

```
  0/1 knapsack       greedy O(n log n) and WRONG
                     DP     O(n x W) and correct
  weighted intervals greedy O(n log n) and WRONG
                     DP     O(n log n) and correct   <- same complexity!

-> the cost of greedy failing is sometimes zero asymptotically.
   Weighted interval scheduling is the same O(n log n) as the
   unweighted greedy, because both are dominated by the sort.
```

**That last line is worth having ready**, because it means **"greedy does not work here" is often not bad
news** — it is a table instead of a loop at the same complexity.

---

## 7. The traps

**Claiming greedy works because it passed the examples.**

```python
>>> # sorting activity selection by DURATION gives the right answer
>>> # on many inputs, including the standard example
>>> # -> the tests pass, and the algorithm is wrong
```

**Passing tests is not an argument.** **The failing inputs for a wrong greedy are often unusual shapes** — a
short interval overlapping two longer disjoint ones — **which random or hand-written tests rarely contain.**

**Proving the wrong thing.**

```
  WRONG: "the greedy choice is in THE optimal solution"
         -> often false, because there may be several optima and
            some do not contain it

  RIGHT: "there is AN optimal solution containing the greedy choice"
         -> what the exchange argument actually establishes
```

**The stronger claim is usually false and always harder**, and trying to prove it is how the argument gets
stuck.

**Forgetting to show the swap is legal.**

```
  "swapping in the earliest finisher gives the same count, so it is
   no worse"
   -> that is HALF the argument

  you must ALSO show the result is still a valid solution:
   -> g ends no later than x, so nothing that fitted after x conflicts

  omitting the legality half is the most common incomplete argument.
```

**Both halves, every time: still legal, and no worse.**

**Using "stays ahead" where there is no natural order.**

```
  stays ahead needs: a sequence of choices, and a measure that can
                     be compared step by step

  0/1 knapsack has no such order — items are a SET, not a sequence
  -> the argument does not even typecheck
  -> use exchange, or discover that neither works
```

**Assuming the exchange argument exists.**

```
  most greedy rules are WRONG, so most attempted exchange arguments
  SHOULD fail
  -> if yours goes through suspiciously easily, check that you
     did not skip the legality half
  -> and if it fails, that is INFORMATION, not a dead end
```

**Treating a failed proof as inconclusive.**

```python
>>> # the exchange fails at "swapping g in may not make room"
>>> # -> that is not "I could not prove it"
>>> # -> that is "here is exactly the input that breaks it":
>>> #    a heavy high-ratio item and two lighter ones
```

**The failure point names the counter-example.** **Reading it as a dead end rather than as a description is
the wasted opportunity.**

**Over-formalising in an interview.**

```
  what is wanted:   two sentences, out loud, thirty seconds
  what is not:      induction written out, base case and step,
                    formal notation

  a candidate who starts writing "let O be an optimal solution and
  let k be the smallest index such that..." has misjudged the
  question and is burning minutes.
```

**Say the sketch. If they want more, they will ask.**

**Not saying anything at all.**

```
  the single most common failure is writing a correct greedy
  solution and moving straight on to the complexity

  -> the interviewer now cannot distinguish you from someone who
     guessed and was lucky
  -> and "why does that work?" is the next question anyway
```

**Volunteer the argument.** It costs thirty seconds and it is the thing being measured.

---

## 8. In the interview

### How it gets asked

- *"Why does that work?"* — the direct form, after any greedy solution.
- *"Prove your greedy choice is correct."* — the same question, more formally phrased.
- *"How do you know sorting by end time is right?"* — the specific form.
- *"Convince me."* — which is asking for the sketch, not a proof.
- *"What if you sorted by X instead?"* — which is asking for the counter-example.

### The first ninety seconds

> **This is what to say immediately after writing any greedy solution, unprompted.**
>
> "Let me justify the greedy choice, because that is the part that is not obvious.
>
> **The claim I need is not that my choice is the best one.** It is weaker than that: **there is at least one
> optimal solution that contains my choice.** That is enough, because if choosing it does not rule out
> optimality, and what remains is the same problem on a smaller input, then induction gives the result.
>
> **The argument is an exchange.** Take any optimal solution. **If it already contains my choice, there is
> nothing to prove.** If it does not, it used something else where my choice would go — **so swap them, and
> show two things.**
>
> **First, that the result is still legal** — no constraint is violated by the substitution.
>
> **Second, that it is no worse** — the objective did not decrease.
>
> **If both hold, then I have produced an optimal solution containing my choice**, which is exactly the claim.
>
> **For this problem specifically:** my choice is the interval that finishes earliest. Take any optimal
> selection and look at its first interval. **Mine finishes no later than that one, by definition.** So
> swapping mine in cannot create a conflict — **everything scheduled after that interval began at or after it
> ended, and mine ends even earlier.** And the count is unchanged, so it is no worse.
>
> **That is the whole argument, and it is two sentences.**
>
> **There is a second form worth knowing, 'greedy stays ahead'**, where instead of modifying an optimal
> solution you show that after every step, greedy's partial answer is at least as good as anyone else's.
> **For this problem: greedy's k-th interval always finishes no later than yours, so greedy can never be the
> one to run out of room first.**
>
> **I would use exchange by default** — it is shorter to state and it applies to problems where the answer is a
> set rather than a sequence."

### The follow-ups

**"Give me the exchange argument in full."**

> "Three steps, and step three has two halves that both have to be shown.
>
> **Step one: take any optimal solution.** Not the greedy one — an arbitrary optimal one. **This matters: the
> argument must work for every optimum, not for a convenient one.**
>
> **Step two: if it already contains my greedy choice, I am done for this step.**
>
> **Step three: if it does not, it contains something else where my choice would go. Swap them.** Then show:
>
> **That the swapped solution is still valid.** This is the half people forget, and it is where the argument
> usually breaks. **For activity selection: my interval finishes no later than the one I replaced, so anything
> that fitted after the old one still fits.**
>
> **And that it is no worse.** For activity selection this is trivial — the count is identical. **For a
> weighted problem it would not be trivial, which is precisely why greedy fails there.**
>
> **Then the conclusion: I have constructed an optimal solution containing my greedy choice.** So making that
> choice does not rule out optimality. **And what remains after it is the same problem on a smaller input, so
> the same argument applies — induction finishes it.**
>
> **The simplest form of this is the adjacent swap**, and I would look for it first because it is much easier
> to reason about. **For shortest-job-first scheduling: if any two adjacent jobs are out of order — a long one
> before a short one — swapping them changes only those two jobs' contributions and reduces the total wait by
> exactly the difference in their lengths.** So any schedule with an out-of-order adjacent pair is not optimal,
> **which means the sorted order is.**
>
> **That is one sentence and it is a complete argument**, because you only have to reason about two elements —
> everything else in the schedule is unaffected by the swap. **Whenever the adjacent form applies, use it.**"

**"What if you cannot construct the argument?"**

> "Then that is information, and I would use it rather than treat it as a dead end.
>
> **The place where the argument breaks tells me what the counter-example looks like.** The proof attempt and
> the counter-example search are the same activity from opposite ends.
>
> **Concretely, 0/1 knapsack with the value-per-kilo rule.** I try the exchange: take any optimal solution; if
> it does not contain my best-ratio item, swap it in for something.
>
> **And I get stuck immediately at 'swap it in for what?'** My item might be heavier than any single item in
> the optimal solution, **so removing one might not make room** — and removing two might lose more value than
> mine adds.
>
> **That failure point is a description of the counter-example.** A heavy, high-ratio item, and two lighter
> items that together do better. **Six kilos worth sixty against two five-kilo items worth forty each, in a
> ten-kilo bag** — greedy gets sixty and the answer is eighty. **The proof told me where to look.**
>
> **And the contrast is the whole lesson.** For the **fractional** version, the same argument goes through
> perfectly: **if the optimal solution uses any worse ratio, I remove an equal *weight* of it and add that
> weight of mine.** Same total weight, so it is still legal; more value, so it is no worse. **'Might not make
> room' never arises, because I can take a fraction.**
>
> **One word of difference in the problem statement, and the same sort rule goes from provably optimal to
> provably wrong.**
>
> **So my procedure when I cannot construct the argument is: look at where it broke, build the input it
> describes, and check.** If that produces a counter-example, **it is DP and I say so.**
>
> **And if I can neither construct the argument nor find a counter-example, I say exactly that** — 'I cannot
> justify the greedy choice, so I will write the DP, which is always correct'. **That is honest, it is
> specific, and it is a much better answer than an unjustified greedy solution.**"

**"Why does Huffman coding work?"**

> "It is an exchange argument and it is the least obvious of the standard ones, so it is worth having
> rehearsed.
>
> **The greedy step is: repeatedly take the two least frequent symbols and merge them into a single node whose
> frequency is their sum.**
>
> **The claim to justify is: the two rarest symbols are siblings at the deepest level of some optimal tree.**
>
> **The argument comes in two parts.**
>
> **First: in any optimal prefix code, the two deepest leaves are siblings.** Because if the deepest leaf had
> no sibling, you could move it up one level — **shortening its code without lengthening anything else** —
> which contradicts optimality.
>
> **Second: the exchange.** Take any optimal tree. If the two rarest symbols are not in those deepest sibling
> positions, **swap them with whatever is there.**
>
> **Why that does not increase the cost:** the total cost is the sum over symbols of frequency times depth.
> **Swapping moves a rarer symbol deeper and a commoner one shallower.** The commoner symbol's contribution
> falls by more than the rarer one's rises — **because the depth change is the same for both, and the
> frequencies differ in the right direction.**
>
> **So the cost cannot increase, and the tree is still valid** — you have only relabelled leaves.
>
> **Therefore some optimal tree has the two rarest symbols as sibling leaves at the maximum depth**, which is
> exactly what merging them assumes. **And after merging, the remaining problem is the same problem with one
> fewer symbol, so induction applies.**
>
> **Two sentences of intuition, if I had to compress it: rarer symbols should have longer codes, and the two
> rarest can always be pushed to the bottom without harm.**
>
> **One implementation note, since it comes up: the total cost equals the sum of all the merge values**,
> because every merge adds one bit to every symbol underneath it. **That is why the algorithm can compute the
> encoded length without ever building the tree.**"

### The model answer

*"Here is the problem: you have a set of jobs, each with a deadline and a profit, and each takes exactly one
unit of time. You have one machine. Schedule jobs to maximise total profit — a job earns its profit only if it
finishes by its deadline. Solve it, and convince me your approach is correct."*

> "Let me diagnose first, then solve, then justify — **and I suspect the justification is the point of the
> question.**
>
> **The greedy candidate is: sort the jobs by profit, highest first, and schedule each one as late as possible
> before its deadline.**
>
> **My first move is to try to break it, and I would spend thirty seconds.** I look for a case where taking
> the most profitable job blocks two others that together beat it. **A job worth a hundred with deadline one,
> and two jobs worth sixty each with deadlines one and two.** Greedy takes the hundred, which occupies slot
> one, **and then the sixty with deadline one cannot be placed** — total one hundred and sixty. The
> alternative is sixty plus sixty, which is worse. **So that attempt does not break it.**
>
> **I would try a few more and, not finding one, move to the argument** — because failing to find a
> counter-example is not evidence, it just means I now owe a proof.
>
> **The exchange argument.** Take any optimal schedule `O`, and let `g` be the highest-profit job.
>
> **If `O` contains `g`, nothing to show.**
>
> **If it does not**, then either there is a free slot before `g`'s deadline — in which case adding `g` makes
> `O` strictly better, contradicting optimality — **or every slot before `g`'s deadline is occupied.** In that
> case, take any job `x` in one of those slots. **Swap `x` out and `g` in.**
>
> **Is it legal?** Yes — `g` is being placed in a slot before its own deadline, and removing `x` cannot make
> any other job late.
>
> **Is it worse?** No — `g` has the highest profit of all jobs, so `g`'s profit is at least `x`'s. **The total
> did not decrease.**
>
> **So some optimal schedule contains `g`, and induction on the remaining jobs finishes it.**
>
> **Now the implementation detail that the argument does not settle: where to put each job.** **As late as
> possible before its deadline** — because that keeps the early slots free for jobs with tighter deadlines.
> **And that is a second small exchange argument**: if a job is placed earlier than necessary and this blocks a
> tighter-deadline job, moving it later frees the slot and cannot make it late.
>
> **The algorithm: sort by profit descending, and for each job scan backwards from its deadline for a free
> slot.** That is `O(n²)` naively, **and union-find makes it near-linear** — each slot points to the next free
> slot at or before it, which is the same 'find the next available' pattern as disjoint-set union.
>
> **Cost: `O(n log n)` for the sort plus near-linear for the placement.**
>
> **And two things I would flag.**
>
> **If jobs took different amounts of time, this breaks.** The exchange argument depended on every job
> occupying exactly one slot — **swapping `g` for `x` worked because they are the same size.** With variable
> durations, `g` might not fit where `x` was, **which is precisely the 0/1 knapsack failure**, and it becomes
> a much harder problem.
>
> **And if I had failed to construct the argument, I would have said so** and written the DP instead — **the
> cost of an unnecessary table is some code; the cost of an unjustified greedy is a wrong answer.**"

---

## 9. Recall card

**Two arguments, both short, both proof *sketches* rather than proofs.** What you must establish is weaker
than it looks: **there is AT LEAST ONE optimal solution containing your choice** — not that every optimum
contains it, and not that the choice is "best".

**THE EXCHANGE ARGUMENT (use this by default), in three steps:** take *any* optimal solution; if it contains
your choice you are done; **otherwise swap your choice in for whatever it used there, and show BOTH that the
result is still LEGAL and that it is NO WORSE.** Omitting the legality half is the most common incomplete
argument.

**Activity selection in two sentences:** the earliest finisher ends no later than whatever it replaced, **so
nothing that fitted after the old one now conflicts**, and the count is unchanged.

**The ADJACENT-SWAP form is the easiest — look for it first**, because you only reason about two elements.
Shortest job first: any out-of-order adjacent pair can be swapped to reduce the total wait by exactly
(longer − shorter), **so a schedule containing one is not optimal.**

**"GREEDY STAYS AHEAD" is the other form:** after every step, greedy's partial answer is at least as good as
anyone else's, **so greedy can never run out of room first.** Use it when there is a natural order and a
running measure; use exchange when the answer is a set.

**A FAILED PROOF NAMES THE COUNTER-EXAMPLE.** 0/1 knapsack by ratio breaks at *"swapping g in may not make
room"* — which describes a heavy high-ratio item plus two lighter ones: `(6,60)` against two `(5,40)` in a
10-kg bag, 60 against 80. **The fractional version survives the same argument because you can swap an equal
WEIGHT** — one word in the statement decides it.

**Say it in thirty seconds, three sentences, unprompted.** And **"I cannot construct the exchange argument, so
I will write the DP" is an excellent answer** — an unnecessary table costs code, an unjustified greedy costs
a wrong answer, and those are not symmetric.
