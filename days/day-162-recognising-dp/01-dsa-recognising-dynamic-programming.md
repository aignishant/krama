---
day: 162
track: dsa
title: "Recognising dynamic programming"
phase: "Dynamic programming"
status: written
---

# Recognising dynamic programming

## 1. What this is, and why they ask it

You have spent nineteen days writing dynamic programming. **This is the day you learn to notice that you
should.**

That sounds like the smaller skill and it is the larger one. **In an interview nobody says "solve this with
dynamic programming".** They describe a problem, and you have perhaps ninety seconds to decide whether it is DP
at all — and if it is, whether it is one dimension or two, a table or a tree, a set or a range.

**Getting that wrong costs the interview, in both directions.** Reaching for DP on something greedy solves in
one line wastes twenty minutes on a table nobody needed. **Missing DP on something that needs it leads to an
exponential brute force**, and the follow-up will be "can you do better", which you will then have to do under
pressure.

They ask it — implicitly, in every DP question — because **recognition is what distinguishes someone who has
memorised twenty solutions from someone who can solve the twenty-first.** The problems on LeetCode are
finite; the problems in an interview are drawn from a larger pool, and **the pattern-matching is the
transferable part.**

There is a real procedure and it is short: **four signals that say "maybe DP", one test that says "yes,
definitely", and a decision tree for what shape.** Applied out loud in ninety seconds, it is also a strong
signal in itself — **an interviewer watching you diagnose a problem learns more than from watching you recall
one.**

By the end of this lesson you can run the four signals, apply the optimal-substructure test, choose the state
from a decision tree, distinguish DP from greedy and from graph search, and say the whole thing out loud in
under two minutes.

---

## 2. The story

The garage took whatever came through the door and the thing that made Fazal worth what they paid him was that
he could stand at the gate and tell you, before anybody opened anything, roughly what kind of afternoon it was
going to be.

**Not what was wrong. What kind of wrong.**

He had four questions and he had never written them down and he asked all four in about a minute, standing
next to the car with his hands behind his back.

**"When does it happen?"** Because a noise only when cold, a noise only over bumps and a noise all the time are
three completely different afternoons.

**"Has anything been done to it recently?"** Half of everything was somebody else's work from last month.

**"Does it get worse or does it stay the same?"** A thing that got steadily worse was wearing out. A thing that
stayed exactly the same was set up wrong.

**"And does it happen when the engine is off?"** Which sorted the electrical from everything else in one
question.

**Four questions, one minute, and by the end he knew which of about six kinds of job it was.**

The apprentice, who was quick and impatient, thought this was a waste of a minute. **He would open the bonnet
immediately.** And he was right about as often as he was wrong, and when he was wrong he had spent two hours
on it before finding out.

The argument they had about it, in the second year, was the one worth remembering.

**"You are guessing," the boy said. "You just guess faster than me."**

**"I am not guessing what is wrong,"** Fazal said. **"I am working out which drawer to open. There are six
drawers. If I open the right one, everything in it fits the tools I already have."**

And then, because the boy was still unconvinced, he added the thing that was actually the point.

**"You know how to fix all six. That is not your problem. Your problem is that you find out which one at four
o'clock instead of at ten past nine."**

---

## 3. The idea in plain English

Fazal's four questions are the recognition procedure, and his sentence about the drawers is why it matters:
**you already know how to solve all the shapes. The skill is choosing the drawer in ninety seconds rather than
in forty minutes.**

**Start with the four signals. Any one of them means "consider DP".**

**Signal one: the problem asks for an optimum or a count over choices.**

Look for the words. **"Maximum", "minimum", "longest", "shortest", "fewest", "how many ways", "is it
possible".** DP problems almost always ask for one of those, and they ask it about a sequence of decisions.

**"Find the maximum profit", "the fewest coins", "the number of ways", "the longest subsequence".**

**And the counter-signal is just as useful: "list all", "return every", "find one".** Those are backtracking,
not DP — **DP gives you the value, not the collection**, and reconstructing one answer is an add-on rather than
the point.

**Signal two: at each step there is a small set of choices.**

**Take it or leave it. Move right or move down. Buy, sell, or do nothing. Match the characters or skip one of
them.** DP problems are made of repeated small decisions, and the answer is the best sequence of them.

**If there are no discrete choices — if the answer is computed by a formula, or found by sorting — it is not
DP.**

**Signal three: the naive solution is exponential and repeats work.**

**Write the brute-force recursion in your head.** If it branches — two calls, or `n` calls, per level — the
naive cost is `2^n` or `n!`. **And then ask whether those branches overlap**, which is the real question.

**Signal four: the constraint on `n` is small in a specific way.**

This is the crudest signal and it is remarkably reliable:

```
n <= 20            bitmask DP — subsets are the state
n <= 100           O(n^3) is fine — interval DP, or three loops
n <= 1,000         O(n^2) expected — two-dimensional table
n <= 100,000       O(n log n) or O(n) — DP is possible but must be
                   one-dimensional, or it is not DP at all
n <= 10^9          NOT DP. A formula, binary search, or maths.
```

**A problem with `n <= 20` about orderings or subsets is bitmask DP roughly every time**, and reading that off
the constraints before reading the problem statement properly is legitimate and fast.

**Now the test that turns "maybe" into "yes", and it has two parts.**

> **Optimal substructure: the best answer to the whole problem contains the best answers to its parts.**
>
> **Overlapping subproblems: the same smaller problem is asked more than once.**

**Both are needed, and the second is what makes DP a technique rather than a description.**

**Divide and conquer has optimal substructure and no overlap** — merge sort's two halves are never the same
problem twice, which is why it needs no table. **DP is what you use when the recursion tree revisits states.**

**The practical way to check overlap: draw two levels of the recursion tree and look for a repeated argument.**
If `f(5)` appears under both `f(7)` and `f(6)`, you have overlap and a table will pay for itself.

**And the practical way to check optimal substructure: try to break it.** Ask whether a locally worse choice
could lead to a globally better answer *through the same subproblem*. **If the subproblem's answer depends on
how you arrived at it, the substructure is broken and your state is incomplete** — which is the
[day 147](../day-147-finding-the-state/README.md) failure, and the fix is a bigger state, not a different
technique.

**Then, once it is DP: which shape?** This is the decision tree, and it is short.

```
What does the answer depend on?

  a POSITION in one sequence, and a bounded lookback
      -> dp[i], one dimension            (stairs, house robber, LIS)

  a POSITION and a RESOURCE being consumed
      -> dp[i][capacity]                 (knapsack, subset sum, coin change)

  a POSITION and a MODE you are in
      -> dp[i][mode]                     (stock problems, cooldown)

  TWO sequences, independently
      -> dp[i][j], two pointers into two things   (LCS, edit distance)

  a POSITION in a GRID
      -> dp[r][c]                        (unique paths, min path sum)

  a RANGE, and how you split it
      -> dp[i][j], both into ONE thing   (interval DP, burst balloons)

  a SUBTREE
      -> recursion, post-order           (tree DP)

  a SET of used things, n <= 20
      -> dp[mask]                        (bitmask DP, TSP)
```

**Eight shapes, and you have written all eight.** The question is only which drawer.

**And then the three things DP is most often confused with.**

**Greedy.** Greedy makes the locally best choice and never reconsiders. **It is correct only when the local
choice is provably safe** — and the test is whether you can construct a counter-example. **Coin change with
arbitrary denominations is the standard one**: greedy takes 7 from `[1, 5, 7]` for amount 10 and gets four
coins; the answer is two. **If you can build a counter-example in thirty seconds, it is DP. If you try and
fail, it may be greedy — and tomorrow's lesson is about proving it.**

**Graph shortest path.** If the states are nodes and the transitions have costs, **DP and Dijkstra are close
relatives** — DP is what you use when the graph is acyclic and the order is obvious; **Dijkstra is what you
use when it is not.** Coin change is genuinely both: a DP table, or a BFS over amounts.

**Backtracking.** If the problem wants *every* solution rather than the best or the count, **no table helps**,
because the output is the size of the answer. **Count with DP, enumerate with backtracking**, and knowing
which was asked decides everything.

**Finally: what to do when you have recognised it, in order.**

**One: say the state as a full sentence.** "`dp[i][j]` is the minimum cost to..." **If you cannot finish the
sentence, you do not have the state yet, and writing code will not help.**

**Two: check the state is complete.** Given only the state, can you decide what happens next? **If not, add a
dimension or redefine.**

**Three: count the states and the work per state.** **If the product is over about ten million, the state is
wrong or the problem is not DP.**

**Four: write the recurrence and the base cases.** **Five: write it memoised**, because then the fill order
cannot be wrong. **Six: convert to a table and collapse the space, if asked.**

**In that order, every time.** The first three take ninety seconds and they are what stops the twenty-minute
mistakes.

---

## 4. The picture

The recognition flow:

```
   read the problem
        |
        v
   FOUR SIGNALS — any one means "consider DP"
     1. asks for max / min / count / possible?
     2. small set of choices at each step?
     3. naive solution is exponential?
     4. constraint on n is small in a telling way?
        |
        v
   THE TEST — both parts required
     optimal substructure?   (best whole contains best parts)
     overlapping subproblems? (same subproblem asked twice)
        |
        +--- no overlap ----> divide and conquer (no table needed)
        +--- no substructure -> your STATE is incomplete: enlarge it
        |
        v
   WHICH SHAPE? (the decision tree)
        |
        v
   state as a SENTENCE -> completeness check -> COUNT the states
        |
        v
   recurrence -> base cases -> memoise -> tabulate -> collapse
```

The constraint table, which is the fastest signal:

```
  n            expected complexity      likely shape
  ------------------------------------------------------------
  <= 20        O(2^n) or O(2^n * n)     BITMASK DP
  <= 100       O(n^3)                   interval DP, or 3 loops
  <= 1,000     O(n^2)                   2-D table
  <= 100,000   O(n log n) / O(n)        1-D DP, or greedy, or
                                        not DP at all
  <= 10^9      O(log n) / O(1)          maths, binary search,
                                        matrix exponentiation

  READ THE CONSTRAINT FIRST. It is not a hint, it is a specification.
```

Overlapping subproblems, drawn:

```
  MERGE SORT — optimal substructure, NO overlap

              sort(0..7)
             /          \
      sort(0..3)      sort(4..7)
       /     \          /     \
    (0..1) (2..3)   (4..5)  (6..7)

  every subproblem is DIFFERENT -> a table would never be read twice
  -> divide and conquer, no memoisation


  FIBONACCI — optimal substructure AND overlap

                f(5)
              /      \
           f(4)      f(3)      <- f(3) appears twice
          /    \     /   \
       f(3)   f(2) f(2) f(1)   <- f(2) appears three times
       ...

  the SAME subproblem recurs -> a table pays for itself
  -> DP
```

The eight shapes, and how to tell them apart:

```
  what varies?                        state              example
  ---------------------------------------------------------------------
  one position                        dp[i]              climbing stairs
  position + resource left            dp[i][cap]         knapsack
  position + which mode I am in       dp[i][mode]        buy/sell stock
  two independent positions           dp[i][j]           edit distance
  a cell in a grid                    dp[r][c]           unique paths
  a range, split somewhere            dp[i][j] (one seq) burst balloons
  a subtree                           recursion          tree DP
  a set of used items (n<=20)         dp[mask]           TSP

  THE QUESTION TO ASK: "what do I need to know to decide the
  next step?" The answer IS the state.
```

DP against its three neighbours:

```
  GREEDY                    DP
  local choice, never       tries all choices, keeps the best
  reconsidered
  correct only when         always correct if the state is complete
  provably safe
  TEST: can I build a       coins [1,5,7], amount 10:
  counter-example?          greedy 4, optimal 2  -> DP

  DIJKSTRA                  DP
  graph with costs,         graph with costs, ACYCLIC
  cycles allowed            and an obvious order
  a priority queue          a loop
  -> coin change is BOTH: a table, or BFS over amounts

  BACKTRACKING              DP
  wants EVERY solution      wants the best, or the COUNT
  output-sized              answer-sized
  no table helps            a table is the whole technique
  "list all subsets that    "how many subsets sum to X"
   sum to X"
```

The order of operations, which is what actually saves time:

```
  1. state as a SENTENCE           "dp[i][j] is the minimum cost to..."
                                   cannot finish it? you have no state yet
  2. completeness check            given only the state, can I decide
                                   the next step?
  3. COUNT the states x the work   > ~10^7 ? the state is wrong
  4. recurrence + base cases
  5. write it MEMOISED             the fill order cannot be wrong
  6. tabulate, then collapse       only if asked

  STEPS 1-3 TAKE NINETY SECONDS and prevent the twenty-minute mistakes.
```

---

## 5. The code, built step by step

### The diagnostic, written down

```python
def diagnose(problem: str) -> None:
    """The four signals and the test, as a checklist you say out loud."""
    print("1. asks for max/min/count/possible?")
    print("2. small set of choices at each step?")
    print("3. naive recursion exponential?")
    print("4. what is the constraint on n?")
    print("-> optimal substructure? overlapping subproblems?")
```

**That is not real code, and writing the checklist down once makes it a habit.** In an interview it is spoken,
not typed.

### Detecting overlap empirically

```python
from collections import Counter

def count_calls(fn):
    """Wrap a recursion and count how often each argument recurs."""
    calls: Counter = Counter()

    def wrapped(*args):
        calls[args] += 1
        return fn(wrapped, *args)

    wrapped.calls = calls
    return wrapped


def fib_body(recurse, n):
    return n if n < 2 else recurse(n - 1) + recurse(n - 2)


def merge_sort_body(recurse, lo, hi):
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    recurse(lo, mid)
    recurse(mid, hi)
```

**Running both and looking at the counters answers the overlap question directly** — Fibonacci's arguments
repeat, merge sort's never do. **It is a five-minute experiment that makes the distinction concrete once and
for all.**

### The state-space audit

```python
def audit(name: str, states: int, work_per_state: int) -> None:
    total = states * work_per_state
    verdict = "fine" if total < 10_000_000 else "TOO BIG — rethink the state"
    print(f"{name:28} {states:>15,} x {work_per_state:>6} = {total:>18,}  {verdict}")
```

**This is the third step, and it is thirty seconds that prevents the largest category of mistake.** If the
product is over about ten million, **either the state has a dimension it does not need, or the problem is not
DP at all.**

### Greedy versus DP, tested

```python
def greedy_coins(coins: list[int], amount: int) -> int:
    count, left = 0, amount
    for coin in sorted(coins, reverse=True):
        take = left // coin
        count += take
        left -= take * coin
    return count if left == 0 else -1


def dp_coins(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for t in range(coin, amount + 1):
            dp[t] = min(dp[t], dp[t - coin] + 1)
    return int(dp[amount]) if dp[amount] != float("inf") else -1


def find_greedy_counterexample(coins: list[int], limit: int = 100):
    """Search for an amount where greedy is worse. Thirty seconds of work."""
    for amount in range(1, limit):
        g, d = greedy_coins(coins, amount), dp_coins(coins, amount)
        if g != -1 and d != -1 and g > d:
            return amount, g, d
    return None
```

**This is a genuinely useful interview habit**: when you suspect greedy, **spend thirty seconds looking for a
counter-example.** If you find one, it is DP. **If you cannot, greedy may be right and you have to argue for
it**, which is tomorrow's lesson.

### The template you write once you have decided

```python
from functools import lru_cache

def solve(inputs):
    # 1. STATE: dp(i, j) is <finish this sentence before writing anything>
    # 2. is it complete? given only (i, j), can I decide the next step?
    # 3. states x work = ? (must be under ~10^7)

    @lru_cache(maxsize=None)
    def dp(i, j):
        if base_case(i, j):
            return base_value(i, j)
        return best(
            dp(next_i, next_j) + cost
            for choice in choices(i, j)
        )

    return dp(*start)
```

**Write it memoised first, every time.** Same complexity, **and the fill order cannot be wrong** — which after
interval DP is worth real money. **Convert to a table only if asked to reduce the space.**

### Worked recognition: five problems

```python
PROBLEMS = [
    ("Given prices, max profit with at most k transactions",
     "max + choices + n small",
     "position + count + mode",
     "dp[day][k][holding]",
     "O(n*k*2)"),

    ("Given a string, count palindromic substrings",
     "count, but NO sequential choices",
     "expand around centre — NOT a table",
     "no dp needed",
     "O(n^2) time, O(1) space"),

    ("n <= 18 cities, shortest tour",
     "n <= 20 + orderings",
     "a SET of visited + where I am",
     "dp[mask][last]",
     "O(2^n * n^2)"),

    ("Given costs, min cost to reach the last stone, jumps of 1 or 2",
     "min + choices + bounded lookback",
     "one position",
     "dp[i]",
     "O(n) time, O(1) space"),

    ("List every subset summing to target",
     "LIST ALL — not an optimum or a count",
     "backtracking, no table",
     "no dp",
     "O(2^n) output-bound"),
]


def show_recognition() -> None:
    for statement, signals, shape, state, cost in PROBLEMS:
        print(f"\n{statement}")
        print(f"   signals : {signals}")
        print(f"   varies  : {shape}")
        print(f"   state   : {state}")
        print(f"   cost    : {cost}")
```

**Two of the five are not DP**, and that is deliberate: **recognising that a problem is *not* DP is half the
skill**, and the palindrome one in particular is a table that people write when they should not.

### The complete solution

```python
"""Recognising DP: the signals, the test, the shapes, and the audit."""

from collections import Counter
from functools import lru_cache


def count_calls(fn):
    """Instrument a recursion to see whether subproblems repeat."""
    calls: Counter = Counter()

    def wrapped(*args):
        calls[args] += 1
        return fn(wrapped, *args)

    wrapped.calls = calls
    return wrapped


def fib_body(recurse, n):
    return n if n < 2 else recurse(n - 1) + recurse(n - 2)


def merge_sort_body(recurse, lo, hi):
    if hi - lo <= 1:
        return 0
    mid = (lo + hi) // 2
    return recurse(lo, mid) + recurse(mid, hi)


def audit(name: str, states: int, work_per_state: int) -> None:
    """Step 3 of the procedure: count before you code."""
    total = states * work_per_state
    verdict = "fine" if total < 10_000_000 else "TOO BIG — rethink the state"
    print(f"  {name:26} {states:>13,} x {work_per_state:>5} = "
          f"{total:>17,}  {verdict}")


def greedy_coins(coins: list[int], amount: int) -> int:
    count, left = 0, amount
    for coin in sorted(coins, reverse=True):
        take = left // coin
        count += take
        left -= take * coin
    return count if left == 0 else -1


def dp_coins(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for t in range(coin, amount + 1):
            dp[t] = min(dp[t], dp[t - coin] + 1)
    return int(dp[amount]) if dp[amount] != float("inf") else -1


def find_greedy_counterexample(coins: list[int], limit: int = 200):
    """If this finds something in thirty seconds, the answer is DP."""
    for amount in range(1, limit):
        g, d = greedy_coins(coins, amount), dp_coins(coins, amount)
        if g != -1 and d != -1 and g > d:
            return amount, g, d
    return None


def constraint_hint(n: int) -> str:
    """The crudest signal, and remarkably reliable."""
    if n <= 20:
        return "O(2^n) — bitmask DP"
    if n <= 100:
        return "O(n^3) — interval DP or three loops"
    if n <= 1_000:
        return "O(n^2) — a two-dimensional table"
    if n <= 100_000:
        return "O(n log n) or O(n) — 1-D DP, greedy, or not DP"
    return "O(log n) or O(1) — maths, binary search, not DP"


PROBLEMS = [
    ("max profit, at most k transactions",
     "max + choices + n small", "position + count + mode",
     "dp[day][k][holding]", "O(n*k*2)"),
    ("count palindromic substrings",
     "count, but NO sequential choices", "expand around centre",
     "no dp needed", "O(n^2) time, O(1) space"),
    ("n <= 18 cities, shortest tour",
     "n <= 20 + orderings", "set of visited + where I am",
     "dp[mask][last]", "O(2^n * n^2)"),
    ("min cost, jumps of 1 or 2",
     "min + choices + bounded lookback", "one position",
     "dp[i]", "O(n) time, O(1) space"),
    ("list every subset summing to target",
     "LIST ALL — not an optimum", "backtracking, no table",
     "no dp", "O(2^n), output-bound"),
]


if __name__ == "__main__":
    print("OVERLAP: does the same subproblem recur?")
    f = count_calls(fib_body)
    f(20)
    print(f"  fibonacci(20) : {sum(f.calls.values()):,} calls for "
          f"{len(f.calls)} distinct arguments  -> OVERLAP -> DP")

    m = count_calls(merge_sort_body)
    m(0, 1024)
    print(f"  merge sort    : {sum(m.calls.values()):,} calls for "
          f"{len(m.calls)} distinct arguments  -> none repeat -> "
          f"divide and conquer")

    print("\nSTATE-SPACE AUDIT (step 3, before coding):")
    audit("stairs, n=10^5", 100_000, 2)
    audit("knapsack, n=100 W=10^4", 100 * 10_000, 2)
    audit("LCS, 1000 x 1000", 1_000_000, 3)
    audit("interval, n=500", 500 * 500, 500)
    audit("bitmask TSP, n=20", (1 << 20) * 20, 20)
    audit("knapsack, W=10^9", 100 * 1_000_000_000, 2)

    print("\nGREEDY OR DP? look for a counter-example:")
    for coins in ([1, 2, 5], [1, 5, 7], [1, 3, 4]):
        found = find_greedy_counterexample(coins)
        if found:
            amount, g, d = found
            print(f"  {str(coins):12} amount {amount:3}: greedy {g}, "
                  f"optimal {d}  -> DP")
        else:
            print(f"  {str(coins):12} no counter-example found "
                  f"-> greedy may be safe")

    print("\nCONSTRAINT -> SHAPE:")
    for n in (18, 90, 900, 90_000, 10**9):
        print(f"  n = {n:>12,}  ->  {constraint_hint(n)}")

    print("\nWORKED RECOGNITION:")
    for statement, signals, varies, state, cost in PROBLEMS:
        print(f"\n  {statement}")
        print(f"     signals : {signals}")
        print(f"     varies  : {varies}")
        print(f"     state   : {state}")
        print(f"     cost    : {cost}")
```

Run it and you get:

```
OVERLAP: does the same subproblem recur?
  fibonacci(20) : 21,891 calls for 21 distinct arguments  -> OVERLAP -> DP
  merge sort    : 2,047 calls for 2047 distinct arguments  -> none repeat -> divide and conquer

STATE-SPACE AUDIT (step 3, before coding):
  stairs, n=10^5                   100,000 x     2 =           200,000  fine
  knapsack, n=100 W=10^4         1,000,000 x     2 =         2,000,000  fine
  LCS, 1000 x 1000               1,000,000 x     3 =         3,000,000  fine
  interval, n=500                  250,000 x   500 =       125,000,000  TOO BIG — rethink the state
  bitmask TSP, n=20             20,971,520 x    20 =       419,430,400  TOO BIG — rethink the state
  knapsack, W=10^9         100,000,000,000 x     2 =   200,000,000,000  TOO BIG — rethink the state

GREEDY OR DP? look for a counter-example:
  [1, 2, 5]    no counter-example found -> greedy may be safe
  [1, 5, 7]    amount  10: greedy 4, optimal 2  -> DP
  [1, 3, 4]    amount   6: greedy 3, optimal 2  -> DP

CONSTRAINT -> SHAPE:
  n =           18  ->  O(2^n) — bitmask DP
  n =           90  ->  O(n^3) — interval DP or three loops
  n =          900  ->  O(n^2) — a two-dimensional table
  n =       90,000  ->  O(n log n) or O(n) — 1-D DP, greedy, or not DP
  n = 1,000,000,000  ->  O(log n) or O(1) — maths, binary search, not DP

WORKED RECOGNITION:

  max profit, at most k transactions
     signals : max + choices + n small
     varies  : position + count + mode
     state   : dp[day][k][holding]
     cost    : O(n*k*2)
...
```

**The first two lines are the overlap test made concrete.** Fibonacci makes nearly twenty-two thousand calls
for **twenty-one distinct arguments** — about a thousand calls per subproblem, so a table saves almost
everything. **Merge sort makes
2,047 calls for 2,047 distinct arguments** — no repeats at all, so memoising it would be pure overhead.

**And the audit is worth reading carefully**, because two of the "too big" lines are genuinely fine in practice
— interval DP at `n = 500` and bitmask TSP at `n = 20` are both at the edge, **which is exactly what "about ten
million" means as a soft threshold rather than a rule.**

---

## 6. What it costs

**The recognition itself: about ninety seconds.**

```
read the constraints              10 s
four signals                      20 s
optimal substructure + overlap    20 s
pick the shape                    20 s
state as a sentence               20 s
                                 ------
                                  90 s
```

**Against what it saves:**

```
recognising DP when it is greedy      ~20 minutes writing an unnecessary table
missing DP when it is DP              ~15 minutes on an exponential solution,
                                      then having to find the table under
                                      pressure after "can you do better?"
wrong SHAPE (1-D when you need 2-D)   ~10 minutes, and the bug is silent
wrong state (incomplete)              the whole interview — it produces
                                      plausible wrong answers with no error
```

**The last one is the expensive one**, and it is what steps one and two prevent.

**The state-space audit, which is thirty seconds:**

```
states x work per state, compared against ~10^7

  under 10^6      instant, no concern
  10^6 - 10^7     fine in Python
  10^7 - 10^8     fine in C, slow in Python
  over 10^8       the state is probably wrong

Python does roughly 10^7 simple loop iterations per second.
C does roughly 10^9.
```

**That single ratio — a hundred to one — is worth memorising**, because it converts a state-space count into a
yes or no in one division.

**The constraint signal, quantified:**

```
n <= 20:      2^20 = 1,048,576        bitmask fits
n <= 100:     100^3 = 1,000,000       cubic fits
n <= 1,000:   1,000^2 = 1,000,000     quadratic fits
n <= 100,000: 100,000^2 = 10^10       quadratic does NOT fit
              100,000 x 17 = 1.7e6    n log n does

-> every row lands near 10^6-10^7. That is not a coincidence:
   the constraint is CHOSEN so the intended solution fits and the
   next-worse one does not.
```

**That is why the constraint is a specification rather than a hint**, and reading it first is legitimate.

**The overlap measurement:**

```
fibonacci(20):
  21,891 calls, 21 distinct arguments
  -> ~1,042 calls per distinct subproblem
  -> memoisation removes 99.9% of the work

fibonacci(40) without memoisation: ~331,000,000 calls  (~30 s)
fibonacci(40) with memoisation:    41 calls            (instant)

merge sort on 1,024 elements:
  2,047 calls, 2,047 distinct arguments
  -> 1.0 calls per subproblem
  -> memoisation removes NOTHING and costs a dictionary
```

**Those two ratios — about a thousand against exactly one — are the whole difference between DP and divide
and conquer**, measured rather than asserted.

**Memoised against tabulated, on cost:**

```
same asymptotic complexity
memoised is ~2-3x slower in Python (function call overhead)
memoised computes ONLY the reachable states — sometimes far fewer
tabulated allows the space collapse; memoised does not

-> memoise first (the fill order cannot be wrong),
   tabulate if asked for the space.
```

**And one case where memoisation is genuinely better:**

```
a DP whose reachable states are sparse — coin change with coins
[7, 11] and amount 10,000

  tabulated: fills all 10,001 cells
  memoised:  visits only amounts reachable as 7a + 11b
             -> a fraction of them

for dense problems tabulation wins on constants; for sparse ones
memoisation wins outright.
```

---

## 7. The traps

**Reaching for DP when greedy solves it.**

```python
>>> find_greedy_counterexample([1, 2, 5])
>>> # None — no counter-example under 200
>>> # Indian denominations are canonical: greedy is provably optimal
>>> # writing a DP table here is 20 wasted minutes
```

**The check costs thirty seconds.** And the reverse is worse: greedy on `[1, 5, 7]` is wrong at amount 10, and
**a solution that passes the sample tests and fails the hidden ones is the worst outcome.**

**Reaching for DP when the answer is a formula.**

```python
>>> # "how many paths across an m x n grid?"
>>> import math
>>> math.comb(3 + 7 - 2, 3 - 1)
28
>>> # a table computes the same number in 21 cells instead of 8
>>> #   multiplications — and at m = n = 10^6 the table is impossible
```

**Check for a closed form before building a table**, especially when the problem is about counting arrangements
— **combinatorics often collapses a DP to one line.**

**Not checking the state-space size.**

```python
>>> # knapsack with W = 10^9
>>> dp = [0] * (10**9 + 1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**Thirty seconds of arithmetic before coding would have caught it**, and the fix is not a faster table — **it
is that the approach is wrong for that constraint.**

**Using an incomplete state, which is the expensive one.**

```python
>>> # "dp[i] = the best in the first i elements" for LIS
>>> # you cannot write the recurrence, because you do not know
>>> # what the best subsequence ENDS ON
>>> # -> but you CAN write code from it, and it runs, and it is wrong
```

**No error, plausible numbers, and it survives small tests.** **The completeness check — "given only the
state, can I decide the next step?" — is twenty seconds and it catches this.**

**Confusing "count" with "list".**

```python
>>> # "how many subsets sum to X"        -> DP, one integer
>>> # "list all subsets that sum to X"   -> backtracking, and the
>>> #   output can be gigabytes
>>> # the words differ by one; the algorithms share nothing
```

**Read the output type before choosing the technique.** A table cannot enumerate, and backtracking cannot
count efficiently.

**Missing that the recursion has no overlap.**

```python
>>> m = count_calls(merge_sort_body)
>>> m(0, 1024)
>>> sum(m.calls.values()), len(m.calls)
(2047, 2047)
```

**Every argument is distinct, so a cache is never read.** Memoising divide and conquer **costs a dictionary and
saves nothing** — and it is a common instinct once you have spent a month on DP.

**Choosing the wrong shape.**

```python
>>> # buy and sell stock with dp[day] alone:
>>> # runs, returns a number, and cannot express "am I holding?"
>>> # -> silently wrong, and it passes tests where the answer
>>> #    happens not to depend on the mode
```

**The decision tree exists to prevent this**, and the question that drives it is always the same: **what do I
need to know to decide the next step?**

**Not reading the constraints first.**

```
"n <= 20" with a problem about orderings   -> bitmask, every time
"n <= 10^5" with a problem about pairs     -> NOT an n^2 table

Spending ten minutes designing an n^2 solution for n = 10^5 is
a category error, and the constraint said so on the first line.
```

**Read the constraints before the problem statement.** It is not cheating; it is the fastest available signal.

---

## 8. In the interview

### How it gets asked

- It is never asked directly. **It is asked implicitly in every DP question**, in the first ninety seconds.
- *"How would you approach this?"* — before any code.
- *"Why dynamic programming?"* — after you propose it.
- *"Could greedy work here?"* — the question that tests whether you checked.
- *"What is your state?"* — the one that exposes whether you have one.

### The first ninety seconds

> "Before I write anything I want to work out what kind of problem this is, because that decides everything
> else and it takes about a minute.
>
> **First, the constraints.** `n` is at most a thousand, which points at a quadratic solution — **so a
> two-dimensional table is affordable and anything exponential is not.** That is the fastest signal available
> and I would read it before the problem statement.
>
> **Second, four things that suggest dynamic programming.** **It asks for a minimum** — that is the first
> signal. **There is a small set of choices at each step** — take this or skip it. **The naive recursion
> branches two ways per element, so it is `2^n`.** And **the constraint is small in exactly the way that says
> a table is expected.**
>
> **Third, the test, which has two halves and both matter.** **Optimal substructure**: is the best answer to
> the whole made of best answers to parts? **And overlapping subproblems**: does the same smaller problem come
> up more than once?
>
> **The second half is what makes it DP rather than divide and conquer.** Merge sort has optimal substructure
> and never sees the same subproblem twice, so a table would never be read. **Here, sketching two levels of the
> recursion tree, I can see the same arguments appearing under different branches — so a table pays for
> itself.**
>
> **Fourth, which shape.** The question I ask is: **what do I need to know to decide the next step?** Here it
> is where I am in the sequence and how much capacity is left — **so the state is two-dimensional: position
> and resource.**
>
> **And then the state as a full sentence: `dp[i][c]` is the best value using the first `i` items with `c`
> capacity remaining.** If I cannot finish that sentence, I do not have a state yet and writing code will not
> help.
>
> **Then a completeness check** — given only `i` and `c`, can I decide what happens next? Yes. **And a count:
> `n × W` states with constant work each, so a million operations — comfortable.**
>
> **One thing I would rule out explicitly: could greedy work?** Take the highest-value item first — **and I can
> construct a counter-example in about twenty seconds, so no.** That check is worth doing, because if greedy
> did work, the table would be twenty wasted minutes.
>
> **Now I will write it memoised**, because the fill order cannot be wrong that way, and convert it to a table
> if you want the space reduced."

### The follow-ups

**"How do you know it is dynamic programming and not greedy?"**

> "I try to break greedy, and I give myself about thirty seconds to do it.
>
> **Greedy makes the locally best choice and never reconsiders. It is correct only when that local choice is
> provably safe** — meaning there is always an optimal solution that agrees with it.
>
> **So the test is: can I construct an input where the locally best choice leads to a worse total?**
>
> **The canonical example is coin change.** With denominations one, five and seven, and an amount of ten,
> **greedy takes the seven — the biggest that fits — then needs three ones. Four coins.** The optimal answer is
> five plus five. **Two.** The greedy step is the largest single reduction and it strands a remainder that only
> ones can fill.
>
> **And the reason this matters more than it looks is that greedy works for the coins we actually use.** One,
> two, five, ten, twenty — greedy is optimal for every amount, **so the intuition feels reliable and is a
> property of those specific numbers rather than of the method.**
>
> **If I find a counter-example in thirty seconds, it is DP and I stop looking.**
>
> **If I cannot find one, that is not proof** — it means greedy might be right, and I would need an argument.
> **The usual shape of that argument is an exchange argument**: show that any optimal solution can be
> transformed into one containing the greedy choice, without getting worse.
>
> **In an interview I would say which of those two situations I am in.** 'I found a counter-example, so it is
> DP' is definitive. **'I tried and failed, so I think greedy works, and here is the sketch of why' is honest**
> and much better than asserting it.
>
> **There is a third option worth naming: do both.** The DP is always correct, and if I suspect greedy I can
> write the greedy solution and check it against the DP on random inputs. **That is a real technique and it
> takes five minutes.**"

**"What is your state, and how do you know it is enough?"**

> "Two questions, and the second is the one that catches the expensive mistakes.
>
> **I state it as a full sentence: `dp[i][j]` is the minimum number of operations to turn the first `i`
> characters of `a` into the first `j` of `b`.** **If I cannot finish that sentence, I do not have a state
> yet** — and writing code before I can is how twenty minutes disappear.
>
> **Then the completeness check: given only the values in the state, can I decide what happens next, without
> knowing anything about how I got here?**
>
> **If the answer is no, the state is incomplete, and it fails silently.** That is the worst failure mode in
> dynamic programming, because **you can write code from an incomplete state, and it runs, and it produces
> plausible numbers.**
>
> **The clearest example is longest increasing subsequence.** The natural state is 'the longest increasing
> subsequence in the first `i` elements' — **and when element `i` arrives I cannot tell whether it extends
> anything, because I know a length and not what that subsequence ended on.** The fix is to redefine: 'ending
> exactly at `i`', which carries the ending value in the definition itself.
>
> **And notice the fix cost nothing** — still `n` cells. **Redefining is often free where adding a dimension is
> not**, and trying to redefine first is worth thirty seconds.
>
> **Then the third step, which is arithmetic: count the states and multiply by the work per state.** Python
> does roughly ten million simple operations a second, so **if the product is much over ten million, either
> the state has a dimension it does not need, or this is not DP.**
>
> **That count has saved me from the knapsack-with-a-billion-capacity mistake**, where the table is eight
> gigabytes and the approach is simply wrong for the constraint.
>
> **Those three steps take ninety seconds and they prevent the mistakes that cost twenty minutes.**"

**"When is it not dynamic programming?"**

> "Four cases, and I check for all of them, because reaching for a table when something simpler works is as
> bad as missing DP.
>
> **One: when there is no overlap.** If the recursion never asks the same subproblem twice, **a table is never
> read and memoising costs a dictionary for nothing.** Merge sort is the example: it has perfect optimal
> substructure and every subproblem is distinct. **That is divide and conquer**, and the test is to sketch two
> levels and look for a repeated argument.
>
> **Two: when greedy is provably safe.** If the local choice can be shown never to hurt, **one pass beats a
> table.** Interval scheduling by earliest end time, or Huffman coding. **The check is to try to construct a
> counter-example, and if I fail I look for the exchange argument.**
>
> **Three: when there is a closed form.** Counting paths across a grid is a binomial coefficient — **`O(1)`
> space and `O(min(m,n))` time against a full table.** Combinatorics collapses a lot of counting DPs to one
> line, **and I would check for that before building anything, especially when the problem is about
> arrangements.**
>
> **Four: when the problem wants every solution rather than the best or the count.** 'List all subsets summing
> to X' is backtracking, **and no table helps, because the output is the size of the answer** — eight million
> subsets is gigabytes of output whatever algorithm produced it. **'How many subsets sum to X' is DP and the
> answer is one integer.** The two statements differ by a word and share no algorithm.
>
> **And a fifth, which is really about constraints.** **If `n` is a hundred thousand and the natural state is
> two-dimensional, it is not DP as stated** — a quadratic table is 10¹⁰ cells. **Either there is a
> one-dimensional formulation, or the intended answer is something else entirely**, and the constraint is
> telling me which."

### The model answer

*"Here is a problem: you have a row of houses with values, you may not take two adjacent ones, and you want the
maximum total. Talk me through how you would approach it — I am more interested in your reasoning than the
code."*

> "Then let me diagnose it out loud, because that is what you have asked for, and I would do this before
> writing anything anyway.
>
> **First, the constraints — and I would ask if they are not given.** Say `n` is up to a hundred thousand.
> **That immediately rules out anything quadratic and points at a linear solution**, which is useful before I
> know what the solution is.
>
> **Now the four signals.**
>
> **It asks for a maximum** — signal one. **There is a small set of choices at each house: take it or skip
> it** — signal two. **The naive recursion branches two ways per house, so it is `2^n`** — signal three. And
> **the constraint is consistent with a linear DP** — signal four. **All four fire, so I am fairly confident
> before doing any real thinking.**
>
> **Now the test, both halves.**
>
> **Optimal substructure: is the best answer for houses one to `n` built from best answers to shorter
> prefixes?** Yes — if I decide about the last house, the rest is the same problem on a shorter row.
>
> **Overlap: does the same subproblem recur?** Sketching two levels: the answer for the first `n` houses calls
> the first `n-1` and the first `n-2`; the first `n-1` calls `n-2` and `n-3`. **`n-2` appears under both.**
> Overlap, so a table pays for itself. **That is Fibonacci's shape exactly, and it is worth noticing out
> loud.**
>
> **Now the shape.** My question is: **what do I need to know to decide about the next house?** Just where I
> am — because the constraint only reaches back one house. **So it is one-dimensional: `dp[i]`.**
>
> **The state as a sentence: `dp[i]` is the maximum total obtainable from the first `i` houses.**
>
> **Completeness check: given only `i` and that value, can I decide about house `i+1`?** Almost — **I need to
> know whether house `i` was taken.** And here I have a choice, which is the interesting moment.
>
> **I could add a mode dimension: `dp[i][took_it]`.** That works and is two cells per house.
>
> **Or I can redefine so the information is carried implicitly:** `dp[i]` is the best for the first `i` houses
> **where I am free to choose about house `i`**, and the recurrence is `max(dp[i-1], dp[i-2] + value[i])` —
> **skip this house, or take it and jump back two.** The 'not adjacent' constraint is expressed by the jump.
>
> **I would take the redefinition**, and say why: **it is the same number of cells and it makes the recurrence
> read as the decision.** That is the day-147 lesson — **try redefining before adding a dimension.**
>
> **Count the states: `n` states, constant work each. A hundred thousand operations. Comfortable.**
>
> **Base cases: `dp[0]` is the first house's value, `dp[1]` is the larger of the first two.**
>
> **Then two more things I would say before coding.**
>
> **Could greedy work?** Take the largest value, then the largest remaining non-adjacent one, and so on.
> **I can break it with three houses: five, ten, six.** Greedy takes the ten, which forbids both neighbours, so
> it gets ten. **Taking the five and the six — which are not adjacent — gives eleven.** So greedy is wrong,
> and it is DP.
>
> **I would spend those thirty seconds constructing a real counter-example rather than asserting one**, because
> the small cases are where greedy usually survives and a hand-waved example proves nothing. **And if I had
> failed to break it, that would change the answer** — greedy might be right, and I would owe you an
> argument instead of a table.
>
> **And the space.** The recurrence reads only `dp[i-1]` and `dp[i-2]`, **so two variables are enough — `O(1)`
> space.** I would write the array version first for clarity and offer the collapse.
>
> **The whole diagnosis took about ninety seconds, and it produced: one-dimensional DP, state as a sentence,
> `n` states, a checked greedy alternative, and a known space optimisation — before a line of code.** That is
> the part I would want to be judged on."

---

## 9. Recall card

**Four signals — any one means "consider DP":** it asks for **max/min/count/possible**; there is a **small set
of choices** at each step; the **naive recursion is exponential**; and the **constraint on `n`** is small in a
telling way. **Read the constraints first** — `n ≤ 20` → bitmask, `≤ 100` → `O(n³)`, `≤ 1,000` → `O(n²)`,
`≤ 10⁵` → one-dimensional or not DP at all. Every row lands near 10⁶–10⁷, because the constraint is chosen so
the intended solution fits and the next-worse one does not.

**Then the test, and BOTH halves matter: optimal substructure AND overlapping subproblems.** No overlap =
divide and conquer (merge sort: 2,047 calls, 2,047 distinct arguments — a table would never be read). Overlap
= DP (fib(20): 13,529 calls, **21 distinct arguments**). **Broken substructure means your STATE is incomplete,
not that DP is wrong.**

**The shape follows one question: what do I need to know to decide the next step?** Position → `dp[i]`;
position + resource → `dp[i][cap]`; position + mode → `dp[i][mode]`; two sequences → `dp[i][j]`; a grid →
`dp[r][c]`; a **range and how you split it** → interval DP; a subtree → recursion; a **set**, `n ≤ 20` →
`dp[mask]`.

**Then, in order and in ninety seconds: (1) state as a full SENTENCE** — cannot finish it, you have no state;
**(2) completeness check** — given only the state, can you decide the next step; **(3) count states × work
against ~10⁷** (Python does ~10⁷ ops/second, C ~10⁹). **Then recurrence, base cases, memoise** (the fill order
cannot be wrong), tabulate and collapse only if asked.

**Not DP when:** no overlap (divide and conquer); greedy is provably safe (**spend 30 seconds trying to build a
counter-example** — coins `[1,5,7]`, amount 10: greedy 4, optimal 2); **a closed form exists** (grid paths are
a binomial coefficient); or the problem says **"list all"** rather than "how many" — that is backtracking, and
the output is gigabytes whatever you do.
