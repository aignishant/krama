---
day: 89
track: dsa
title: "Writing a recursive function that terminates"
phase: "Recursion and backtracking"
status: written
---

# Day 089 · DSA — Writing a recursive function that terminates

**After today you can:** You can name the value that shrinks on every call, so your recursion always ends.

**The interviewer asks it as:** *Why does your recursion terminate?*

---

## 1. What this is, and why they ask it

A recursive function ends because something **gets smaller every time and cannot get smaller for ever**.
That is the whole idea, and being able to name that something — out loud, in one phrase — is the
difference between a recursion you trust and one you hope about.

The thing that shrinks has a name: the **measure**, or the **variant**. For summing a list it is the
number of remaining elements. For binary search it is the width of the interval. For Euclid's algorithm
it is the second argument. Three conditions have to hold, and all three are easy to state:

1. The measure **strictly decreases** on every recursive call.
2. It is **bounded below** — it cannot fall for ever.
3. The **base case triggers** at or before that bound.

Miss any one and the function does not terminate. And the interesting failures are not the obvious
ones: it is very easy to write a recursion with a perfectly good base case, on inputs that get
smaller, that still runs for ever — because "smaller" was not strict, or because the measure you had in
mind is not actually the one the code changes.

They ask it because `RecursionError` is the most common failure in this phase, because "why does it
terminate?" is a question with a crisp answer that most candidates cannot give, and because the moment
you meet graphs — where there is no natural measure at all — the answer becomes a design decision
rather than an observation.

---

## 2. The story

Kamala borrowed eighteen thousand rupees in 2019 for her daughter's admission, from a man who lends in
the lane behind the vegetable market, and she has been paying him nine hundred rupees every Friday
since.

That is a hundred and fifty-something Fridays. Well over a lakh, paid.

She still owes eighteen thousand rupees.

Her nephew Prashanth, who does accounts for a transport company, sat with her one Sunday because his
mother had asked him to, and it took him about ten minutes. Every Friday she pays nine hundred. Every
Friday nine hundred is added on. She is paying, on time, without fail, and the number at the bottom of
the page has not moved once in three years.

He said the thing she repeats now to anybody who will listen. It does not matter how many times you
pay. It matters whether the number gets smaller.

Her neighbour Zubeida borrowed from the co-operative society instead, and her arrangement is different
in one specific way. Her weekly payment covers what is added *and* takes at least five hundred rupees
off the balance. Not sometimes. Every week, at least five hundred.

Which means Zubeida can do something Kamala cannot: she can count. Thirty-six thousand, at least five
hundred off a week, is at most seventy-two weeks. She knows, on the day she borrows, that there is a
last Friday and roughly when it falls. She has it written in her phone.

There is a third thing Prashanth explained, and this is the one Kamala had not thought of. It is not
enough that the number goes down. It has to be able to reach the bottom. If a rule said the balance
halves every week, it would fall very fast — nine thousand, four and a half, two and a quarter — and
it would never actually be zero, and she would be paying small amounts for ever. So the society's rule
has a second half: once the balance is under a thousand, you pay it off and it is finished.

Kamala's arrangement fails on the first point. A halving rule would fail on the third. Zubeida's works
because it satisfies both.

---

## 3. The idea in plain English

Kamala's balance is the **measure** of the recursion, and it does not decrease. Zubeida's does, by at
least five hundred every week, and it has a floor with a rule for reaching it.

### The three conditions

Every terminating recursion satisfies all three. Say them in this order.

**1. Name the measure, and show it strictly decreases.**
Some number derived from the arguments must be smaller in the recursive call than it was in this one.
Not "different". Not "usually smaller". **Strictly smaller, every time.**

**2. It is bounded below.**
It cannot go down for ever. Usually it is a non-negative integer, which is why integer measures are so
much easier to reason about than floating-point ones.

**3. The base case triggers at or before the bound.**
The measure reaching its floor must actually stop the recursion. Zubeida's "under a thousand, pay it
off" rule.

```python
def total(numbers: list[int], start: int = 0) -> int:
    if start == len(numbers):        # 3. the base case fires when the measure is 0
        return 0
    return numbers[start] + total(numbers, start + 1)
    #                             ^ 1. the measure is len(numbers) - start,
    #                                  and it drops by exactly 1
    #                             2. it is a non-negative integer, so it has a floor
```

**The measure is `len(numbers) - start`**, and that phrase is what you say when asked why it
terminates. Not "because there is a base case" — that is only the third condition.

### Naming the measure for things you have already written

| Function | The measure | Why it strictly decreases |
|---|---|---|
| `total(numbers, start)` | `len(numbers) - start` | `start` goes up by exactly 1 |
| `reverse(text)` | `len(text)` | the slice is one character shorter |
| `power(base, n)` | `n` | `n − 1` |
| `fast_power(base, n)` | `n` | `n // 2`, and `n // 2 < n` for `n ≥ 1` |
| `binary_search(low, high)` | `high - low` | the interval halves |
| `merge sort` | the list's length | each half is strictly shorter |
| `factorial(n)` | `n` | `n − 1` |
| `count_nodes(node)` | nodes remaining ahead | one node consumed per call |

**Every one of those is a non-negative integer.** That is not a coincidence: integers give you all
three conditions almost for free, because "strictly smaller non-negative integer" cannot go on for
ever.

### Euclid's algorithm, which is the interesting one

```python
def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)
```

What shrinks? Not `a` — the first argument becomes `b`, which may be larger. The measure is **`b`**,
and it strictly decreases because `a % b` is always in the range `0` to `b − 1`, so the new second
argument is strictly less than the old one. It is bounded below by zero, and the base case is exactly
`b == 0`.

**Two arguments, and only one of them is the measure.** That is the shape of most non-obvious
termination arguments, and being able to point at which argument is doing the work is exactly what the
question is asking.

### When the measure is a combination

Sometimes no single argument decreases:

```python
def paths(row: int, col: int) -> int:
    """How many ways to reach (0,0) moving only up or left."""
    if row == 0 or col == 0:
        return 1
    return paths(row - 1, col) + paths(row, col - 1)
```

Neither `row` nor `col` decreases on every call — the first branch leaves `col` alone. But **`row +
col` decreases by exactly one on every call**, and it is bounded below by zero.

The measure does not have to be an argument. It has to be **a non-negative integer function of the
arguments that strictly decreases**. Sums, differences, list lengths, "cells not yet filled",
"unvisited nodes" — all legitimate.

### The three ways termination fails

**Failure one: the measure does not decrease.** Kamala's balance.

```python
def total(numbers, start=0):
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start)     # `start` never moves
```

Perfect base case. Never reached.

**Failure two: it decreases but steps over the base case.**

```python
def power(base, n):
    if n == 0:
        return 1
    return base * power(base, n - 2)      # 5, 3, 1, -1, -3, ...
```

The measure decreases beautifully. It is not bounded below by the base case, because on odd `n` it
never equals zero. **Bound with `n <= 0`, or fix the step** — and fixing the step is the real repair,
because the guard hides a genuine bug.

**Failure three: it decreases but never reaches the floor.** Zubeida's halving rule.

```python
def find_root(low: float, high: float) -> float:
    middle = (low + high) / 2
    if f(middle) == 0:                    # exact equality on a float: almost never
        return middle
    return find_root(low, middle) if f(middle) > 0 else find_root(middle, high)
```

The interval halves every time — strictly decreasing — and with floating point it eventually stops
changing at all, so the recursion neither terminates nor progresses. **The fix is an epsilon**: stop
when `high - low < 1e-9`. This is exactly the relative-epsilon discussion from
[day 048](../day-048-binary-search-on-floats/README.md), and here it is a termination question rather
than a precision one.

**Real measures are non-negative integers.** When they are not, you have to supply the floor yourself.

### Graphs: when there is no measure at all

```python
def visit(node):
    for neighbour in node.neighbours:
        visit(neighbour)                  # a cycle makes this run for ever
```

There is nothing that shrinks. Walking a graph with a cycle revisits the same nodes, and no argument
gets smaller.

The fix **creates** a measure that did not exist:

```python
def visit(node, seen: set):
    if node in seen:
        return
    seen.add(node)                        # the measure is |V| - |seen|
    for neighbour in node.neighbours:
        visit(neighbour, seen)
```

Now "the number of unvisited nodes" strictly decreases on every call that does real work, and it is
bounded below by zero. **The visited set is not an optimisation; it is the termination argument.** That
is worth understanding now, because it is the entire reason depth-first search on a graph looks
different from depth-first search on a tree — a tree has no cycles, so the measure already exists.

### Mutual recursion

```python
def is_even(n: int) -> bool:
    return True if n == 0 else is_odd(n - 1)

def is_odd(n: int) -> bool:
    return False if n == 0 else is_even(n - 1)
```

Neither function calls itself. The measure is still `n`, and it decreases across the *pair*. The rule
generalises: **the measure must decrease around every cycle in the call graph**, not merely within one
function. This is where termination bugs hide, because each function looks fine on its own.

### And the one nobody can answer

```python
def collatz(n: int) -> int:
    if n == 1:
        return 0
    return 1 + collatz(n // 2 if n % 2 == 0 else 3 * n + 1)
```

Does it terminate? **Nobody knows.** It has been checked for every starting value up to about 2⁶⁸ and
always ends at 1, and there is no proof. `3n + 1` makes the value jump *up*, so there is no obvious
measure at all.

Worth knowing for one reason: it is the clearest possible demonstration that "it works on the inputs I
tried" is not a termination argument. If you cannot name the measure, you do not know it terminates —
you have only observed that it did.

---

## 4. The picture

The three conditions, and how each one fails.

```
 WORKS — measure strictly decreases, bounded below, base case at the bound

   measure:  5 -> 4 -> 3 -> 2 -> 1 -> 0
                                       ^ base case fires here.  Terminates.

 FAILS 1 — the measure does not decrease  (Kamala)

   measure:  5 -> 5 -> 5 -> 5 -> ...
             the base case at 0 is perfect, and unreachable

 FAILS 2 — it decreases but steps over the bound  (power(base, n-2) on odd n)

   measure:  5 -> 3 -> 1 -> -1 -> -3 -> ...
                            ^ passed 0 without touching it

 FAILS 3 — it decreases and never reaches the floor  (float halving)

   measure:  1.0 -> 0.5 -> 0.25 -> ... -> 1e-17 -> 5e-18 -> ...
             strictly decreasing for ever.  Needs an epsilon.
```

Euclid's algorithm, where only one argument is the measure:

```
 gcd(48, 18)
   a=48  b=18     b decreases: 18
 gcd(18, 12)
   a=18  b=12     b decreases: 12      <- `a` went DOWN here, but that is not the point
 gcd(12, 6)
   a=12  b=6      b decreases: 6
 gcd(6, 0)
   b == 0 -> return 6

 measure = b.  Strictly decreases because a % b is in [0, b-1].
 `a` is irrelevant to termination: it can grow, as in gcd(3, 100) -> gcd(100, 3).
```

And the graph case, where the measure has to be manufactured:

```
 NO MEASURE                              MEASURE CREATED BY THE VISITED SET

   A -> B -> C                             A -> B -> C
   ^         |                             ^         |
   +---------+                             +---------+

   visit(A) -> visit(B) -> visit(C)        seen = {}       unvisited = 3
   -> visit(A) -> ... for ever             seen = {A}      unvisited = 2
                                           seen = {A,B}    unvisited = 1
                                           seen = {A,B,C}  unvisited = 0
                                           visit(A) returns immediately

   the visited set IS the termination argument, not an optimisation
```

---

## 5. The code, built step by step

### Step 1 — write the measure down as a comment, first

Before the base case, before anything:

```python
def total(numbers: list[int], start: int = 0) -> int:
    # measure: len(numbers) - start, decreases by 1, bounded below by 0
```

Ten seconds, and it forces the question that catches most termination bugs. If you cannot write that
comment, you do not yet know whether the function ends.

### Step 2 — make the base case fire *at* the bound

```python
    if start == len(numbers):        # measure == 0
        return 0
```

The condition should be the measure hitting its floor, stated as directly as the code allows. When the
base case and the measure are written in different vocabularies — `if not numbers` while the measure is
an index — that is where "reachable" quietly stops being true.

### Step 3 — check the recursive call actually moves the measure

```python
    return numbers[start] + total(numbers, start + 1)
    #                                      ^^^^^^^^^ measure drops by exactly 1
```

Point at it. The failure is nearly always here: `start` instead of `start + 1`, or `n - 2` instead of
`n - 1`, or a slice that is empty and therefore not smaller.

### Step 4 — for multiple arguments, find the combination

```python
def paths(row: int, col: int) -> int:
    # measure: row + col, decreases by exactly 1 on every call
    if row == 0 or col == 0:
        return 1
    return paths(row - 1, col) + paths(row, col - 1)
```

Neither argument decreases on every branch; their **sum** does. Write the combination in the comment
and the function becomes obviously terminating.

### Step 5 — when there is no measure, create one

```python
def reachable(start, edges: dict, seen: set | None = None) -> set:
    if seen is None:
        seen = set()                 # NOT a mutable default
    if start in seen:
        return seen                  # the base case, in terms of the measure
    seen.add(start)                  # measure: |V| - |seen|, strictly decreases
    for neighbour in edges.get(start, ()):
        reachable(neighbour, edges, seen)
    return seen
```

Two things worth narrating. `seen=None` rather than `seen=set()`, because a mutable default is created
once at definition time and shared between calls. And `seen.add(start)` **before** the loop, not after
— adding afterwards means a cycle re-enters the node before it was ever marked, and the whole
mechanism fails.

### The complete solution

```python
def total(numbers: list[int], start: int = 0) -> int:
    """MEASURE: len(numbers) - start. Decreases by exactly 1. Floor 0."""
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start + 1)


def gcd(a: int, b: int) -> int:
    """Euclid. MEASURE: b — NOT a, which can grow: gcd(3, 100) -> gcd(100, 3).

    b strictly decreases because a % b is always in [0, b-1]. Floor 0, and the
    base case is exactly b == 0.
    """
    if b == 0:
        return abs(a)
    return gcd(b, a % b)


def paths(row: int, col: int) -> int:
    """MEASURE: row + col. Neither argument decreases on every branch; their
    SUM decreases by exactly 1 on every call. Floor 0."""
    if row < 0 or col < 0:
        raise ValueError("grid coordinates must be non-negative")
    if row == 0 or col == 0:
        return 1
    return paths(row - 1, col) + paths(row, col - 1)


def is_even(n: int) -> bool:
    """MUTUAL recursion. The measure is n, and it decreases around the CYCLE
    is_even -> is_odd -> is_even, not within either function."""
    if n < 0:
        n = -n
    return True if n == 0 else is_odd(n - 1)


def is_odd(n: int) -> bool:
    if n < 0:
        n = -n
    return False if n == 0 else is_even(n - 1)


def reachable(start: str, edges: dict[str, list[str]], seen: set[str] | None = None) -> set[str]:
    """A graph has NO natural measure — a cycle revisits the same nodes for ever.

    The visited set CREATES one: |V| - |seen| strictly decreases on every call
    that does work. It is the termination argument, not an optimisation.

    `seen=None` because a mutable default is created once at definition time.
    `seen.add` BEFORE the loop, or a cycle re-enters before the node is marked.
    """
    if seen is None:
        seen = set()
    if start in seen:
        return seen
    seen.add(start)
    for neighbour in edges.get(start, ()):
        reachable(neighbour, edges, seen)
    return seen


def bisect_root(f, low: float, high: float, epsilon: float = 1e-9, depth: int = 0) -> float:
    """MEASURE: high - low, which halves each time — but a float interval never
    reaches zero, so the floor must be supplied: stop below epsilon.

    The depth guard is a second, independent bound: 1e-9 relative to a starting
    width of 1 is about 30 halvings, so 200 is generous and still finite.
    """
    if depth > 200:
        raise RuntimeError("bisection did not converge")
    if high - low < epsilon:
        return (low + high) / 2
    middle = (low + high) / 2
    if f(low) * f(middle) <= 0:
        return bisect_root(f, low, middle, epsilon, depth + 1)
    return bisect_root(f, middle, high, epsilon, depth + 1)


def ackermann(m: int, n: int) -> int:
    """The standard example where NO single argument decreases, and the measure
    is the PAIR (m, n) compared lexicographically: either m drops, or m stays
    and n drops. It terminates, and it grows absurdly fast — ackermann(3, 3) is
    61 and ackermann(4, 2) has 19,729 digits. Keep the arguments tiny."""
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)          # m decreases
    return ackermann(m - 1, ackermann(m, n - 1))   # inner: m same, n decreases


def collatz_steps(n: int, limit: int = 1000) -> int:
    """NO KNOWN MEASURE. 3n+1 makes the value jump UP, and whether this always
    terminates is an open problem — verified past 2^68, never proved.

    So this one gets an explicit limit, which is the honest thing to do when you
    cannot name a measure.
    """
    steps = 0
    while n != 1:
        if steps > limit:
            raise RuntimeError(f"no termination within {limit} steps from this start")
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


# ---- the three failures, written out so you can run them ----------------

def broken_no_decrease(numbers: list[int], start: int = 0) -> int:
    """FAILURE 1: perfect base case, measure never moves."""
    if start == len(numbers):
        return 0
    return numbers[start] + broken_no_decrease(numbers, start)      # start, not start + 1


def broken_steps_over(base: int, n: int) -> int:
    """FAILURE 2: measure decreases, but odd n steps over the base case."""
    if n == 0:
        return 1
    return base * broken_steps_over(base, n - 2)


def broken_no_visited(start: str, edges: dict[str, list[str]]) -> int:
    """FAILURE 3 for graphs: no measure exists at all, so a cycle runs for ever."""
    return 1 + sum(broken_no_visited(n, edges) for n in edges.get(start, ()))


if __name__ == "__main__":
    print(total([4, 7, 2]))                        # 13
    print(gcd(48, 18), gcd(3, 100), gcd(17, 0))    # 6 1 17
    print(paths(3, 3), paths(0, 5))                # 20 1
    print(is_even(10), is_odd(10), is_even(0))     # True False True

    graph = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}   # A->B->C->A is a cycle
    print(sorted(reachable("A", graph)))           # ['A', 'B', 'C', 'D']

    print(round(bisect_root(lambda x: x * x - 2, 0.0, 2.0), 9))   # 1.414213562
    print(ackermann(2, 3), ackermann(3, 3))        # 9 61
    print(collatz_steps(27))                       # 111

    for name, call in (
        ("no decrease", lambda: broken_no_decrease([1, 2, 3])),
        ("steps over", lambda: broken_steps_over(2, 5)),
        ("no visited set", lambda: broken_no_visited("A", graph)),
    ):
        try:
            call()
        except RecursionError:
            print(f"{name}: RecursionError: maximum recursion depth exceeded")
```

---

## 6. What it costs

### Proving termination costs nothing at run time

The measure is a comment and an argument you were passing anyway. **Naming it is free**, and it
converts a class of bug that only appears on certain inputs into something you can check by reading.
That is a very good trade and it is the reason this lesson exists.

### The two cases where termination has a real price

**The visited set** on a graph is O(V) memory and O(1) per lookup:

```
 a graph of 1,000,000 nodes
 visited set of ids:  ~32 B per entry in a Python set  ->  ~32 MB
 without it:          does not terminate at all
```

Thirty-two megabytes to convert "runs for ever" into "runs". Not a trade-off — a requirement.

**The epsilon** on a float recursion costs precision:

```
 bisection on [0, 2], epsilon = 1e-9
 halvings needed: log2(2 / 1e-9) ≈ 31
 -> 31 calls, and an answer accurate to about 9 decimal places
 epsilon = 1e-15:  ~51 calls, and near the limit of double precision
```

Smaller epsilon buys precision at about one extra call per bit. The floor is where doubles stop
distinguishing values at all — which is why an absolute epsilon fails on very large numbers and a
relative one is safer, as on [day 048](../day-048-binary-search-on-floats/README.md).

### How the measure predicts the complexity

The measure does more than prove termination — **the way it shrinks tells you the running time.**

```
 measure drops by 1        ->  n calls           ->  O(n)      total, factorial
 measure halves            ->  log2(n) calls     ->  O(log n)  binary search, fast_power
 measure drops by 1 with
   TWO calls per level     ->  ~2^n calls        ->  O(2^n)    naive fib
 measure = row + col,
   two calls per level     ->  C(row+col, row)   ->  exponential  paths(n, n)
```

`paths(3, 3)` is 20 and `paths(10, 10)` is 184,756 — the number of calls is a binomial coefficient. So
"what shrinks, and by how much, and how many calls per level" gives you both the termination proof and
the complexity, from the same sentence.

### Euclid, priced

```
 gcd(a, b): the measure b at least HALVES every two calls
 -> O(log(min(a, b))) calls
 gcd of two numbers near 10^18:  about 90 calls
```

The worst case is consecutive Fibonacci numbers, which is a pleasing fact and the reason the bound is
logarithmic rather than linear.

### Ackermann, as the limiting case

```
 ackermann(3, 3) = 61
 ackermann(4, 2) = 2^65536 - 3, which has 19,729 digits
```

It terminates — the pair `(m, n)` decreases lexicographically on every call — and it is not
*computable in practice* past tiny arguments. **Termination and feasibility are different properties**,
and Ackermann is the clean example: a proof that a function ends tells you nothing about whether you
can wait.

---

## 7. The traps

### Trap 1 — "it terminates because there is a base case"

The most common wrong answer, and it only covers the third condition. A base case that is never reached
is worth nothing — Kamala's arrangement had a perfectly good rule for what happens at zero. **The
answer to "why does it terminate?" starts with "the measure is…", not with "there is a base case at…".**

### Trap 2 — the measure that does not move

```python
    return numbers[start] + total(numbers, start)
```

```
RecursionError: maximum recursion depth exceeded
```

Usually a typo — `start` for `start + 1`, or `node` for `node.next`. Point at the recursive call and
ask "which argument is smaller here?" every single time.

### Trap 3 — stepping over the bound

```python
    return base * power(base, n - 2)
```

The measure decreases and misses zero on odd inputs. Guarding with `n <= 0` stops the crash and leaves
the real bug — the function now returns a wrong answer for odd exponents. **Fix the step, not the
guard.**

### Trap 4 — a float measure with no floor

```python
    if low == high:                       # equality on floats: essentially never true
        return low
```

The interval halves for ever and the base case never fires. Then, worse, at some point `(low + high) /
2` equals `low` exactly and the recursion stops making progress while still recursing. **Use an epsilon,
and add a depth guard as an independent bound.**

### Trap 5 — no visited set on a graph

```python
    for neighbour in node.neighbours:
        visit(neighbour)
```

Terminates on a tree and runs for ever on anything with a cycle — so it passes every test written
against sample data and fails on production data with one back-edge. **The visited set is the
termination argument.**

And the subtler version: adding to `seen` *after* the recursive loop instead of before. The node is
re-entered on a cycle before it was ever marked, and nothing changes.

### Trap 6 — mutual recursion where each function looks fine

```python
def is_even(n): return True if n == 0 else is_odd(n)     # note: n, not n - 1
def is_odd(n):  return False if n == 0 else is_even(n - 1)
```

`is_even` alone looks correct. `is_odd` alone looks correct. The measure has to decrease **around the
cycle**, and here it drops on one leg and not the other, so pairs of calls make no progress. When
functions call each other, draw the cycle and check the measure across the whole loop.

### Trap 7 — a mutable default as the accumulator

```python
def reachable(start, edges, seen=set()):        # created ONCE at definition time
```

The second top-level call inherits the first call's `seen`, so it returns immediately having "already
visited" everything. Silent, and the function *looks* like it terminated correctly. Use `None` and
create it inside.

### Trap 8 — believing an empirical check

Collatz has been verified for every starting value below about 2⁶⁸ and is not proved. Your function
working on the fifty inputs you tried is exactly as strong an argument. **If you cannot name the
measure, add an explicit limit and raise** — that is the honest thing to do, and it turns an infinite
loop into a diagnosable error.

---

## 8. In the interview

### How it gets asked

- The direct version, usually right after you write a recursive function: *"Why does that terminate?"*
- The debugging version: *"This gives a `RecursionError`. Find the bug."*
- The graph version, which is the important one: *"Write a depth-first search."* — and the visited set
  is the answer to a termination question, not a performance one.
- The trap version: *"Does this terminate?"* on something with a non-obvious measure — Euclid,
  Ackermann, or Collatz.
- The design version: *"How would you make sure this always finishes?"*

### What to say out loud, in the first ninety seconds

1. **Answer with the measure, not with the base case.** "It terminates because `len(numbers) - start`
   strictly decreases by one on every call, it is a non-negative integer so it has a floor, and the
   base case fires exactly when it reaches zero."
2. **Point at the argument that moves.** "This is the one that shrinks" — and if two arguments are
   involved, say which, or name the combination.
3. **Say all three conditions, briefly.** Strictly decreasing, bounded below, base case at the bound.
4. **For a graph, say why a set is required rather than helpful.** "A graph has no natural measure, so
   the visited set creates one: the number of unvisited nodes. It is the termination argument."
5. **For floats, name the floor you supplied.** "A halving interval never reaches zero, so I stop below
   an epsilon and I would also add a depth guard as an independent bound."

### The follow-ups

**"Why does that terminate?"**
"Because there is a value that strictly decreases on every call and cannot decrease for ever. Here it
is `len(numbers) - start`, which drops by exactly one and is bounded below by zero, and the base case
fires precisely when it reaches zero. Those are the three conditions: strictly decreasing, bounded
below, and a base case that triggers at the bound. Saying 'there is a base case' only answers the
third — Kamala's loan had a perfectly good rule for reaching zero and never got there."

**"What about Euclid's algorithm? `a` can get bigger."**
"It can — `gcd(3, 100)` calls `gcd(100, 3)` — and that is fine, because `a` is not the measure. **`b`
is.** The new second argument is `a % b`, which is always between zero and `b − 1`, so `b` strictly
decreases. It is bounded below by zero and the base case is exactly `b == 0`. That is the general
shape of a non-obvious termination argument: several arguments, and only one of them, or one
combination, is doing the work. Incidentally the same measure gives you the complexity — `b` at least
halves every two steps, so it is O(log min(a, b)), about ninety calls on numbers near 10¹⁸."

**"Write a depth-first search on a graph."**
"The visited set is the first thing I write, and I would say why: a graph has no natural measure. On a
tree, 'nodes below me' shrinks automatically; on a graph with a cycle, nothing shrinks and the
traversal runs for ever. The set manufactures a measure — the number of unvisited nodes — which
strictly decreases on every call that does work. So it is the termination argument, not an
optimisation. Two details: mark the node *before* recursing into its neighbours, or a cycle re-enters
before it is marked; and pass the set explicitly rather than as a mutable default, which would be
shared across calls."

**"This recursion crashes on some inputs and not others."**
"That is almost always condition two or three rather than condition one — the measure does decrease,
but it steps over the base case, or the base case is stated in different terms from the measure. The
classic is decrementing by two towards an equality test at zero: it terminates for even inputs and
never for odd. I would look at the recursive call, name the measure, and check that the base-case
condition is exactly the measure hitting its floor. And I would fix the step rather than widening the
guard to `<= 0`, because the wider guard turns a crash into a wrong answer."

**"Does Collatz terminate?"**
"Nobody knows. It has been verified for every starting value up to about 2⁶⁸ and there is no proof —
`3n + 1` makes the value jump upward, so there is no obvious measure. I like it as an example because
it makes the point that 'it worked on the inputs I tried' is not a termination argument. If I had to
ship something like that, I would give it an explicit step limit and raise, which turns an infinite
loop into a diagnosable error."

**"Give me a recursion where no single argument decreases."**
"Counting paths in a grid: from `(row, col)` you recurse to `(row - 1, col)` and `(row, col - 1)`, so
neither argument decreases on every branch — but `row + col` decreases by exactly one on every call
and is bounded below by zero. The measure does not have to be an argument; it has to be a non-negative
integer function of the arguments that strictly decreases. The extreme case is Ackermann, where the
measure is the *pair* compared lexicographically: either `m` drops, or `m` stays the same and `n`
drops. It terminates and it is still completely infeasible past tiny arguments, which is a nice
reminder that termination and practicality are different questions."

### A model answer

Asked: *why does your recursion terminate?*

> "Because there is a value that gets strictly smaller on every call and cannot get smaller for ever.
> That value has a name — the measure — and naming it is the answer.
>
> For this function the measure is `len(numbers) - start`. Three things have to be true about it, and
> I would check all three explicitly.
>
> First, it strictly decreases. The recursive call passes `start + 1`, so the measure drops by exactly
> one. Not 'usually smaller' — every call, without exception.
>
> Second, it is bounded below. It is a non-negative integer, so it cannot fall for ever. That is why
> integer measures are so much easier to reason about than floating-point ones: a strictly decreasing
> non-negative integer has to stop.
>
> Third, the base case fires at that bound. `start == len(numbers)` is exactly the measure reaching
> zero. This is the condition people give as the whole answer, and on its own it is worth nothing — a
> base case that is never reached does not help. The classic failure is decrementing by two towards an
> equality test at zero: it works for even inputs and recurses for ever on odd ones, and the base case
> looks perfectly correct while it happens.
>
> The measure is not always an argument. In Euclid's algorithm, `a` can grow — `gcd(3, 100)` becomes
> `gcd(100, 3)` — and the measure is `b`, which strictly decreases because `a % b` is always less than
> `b`. In a grid-path count neither coordinate decreases on every branch, but their *sum* does. So the
> real definition is: a non-negative integer function of the arguments that strictly decreases.
>
> Two cases are worth calling out because they are where this stops being theory.
>
> On a graph, there is no natural measure at all — a cycle brings you back to the same node with the
> same arguments. The visited set *creates* one: the number of unvisited nodes, which strictly
> decreases on every call that does work. So the set is the termination argument, not a performance
> optimisation, and it has to be updated before recursing rather than after.
>
> And with floating point, a halving interval decreases strictly and never reaches zero, so there is no
> floor unless I supply one. That is what an epsilon is for, and I would also add a depth guard as an
> independent bound, because two independent reasons to stop is cheap insurance.
>
> The last thing I would say is that the measure gives me the complexity as well as the proof. Drops by
> one, one call per level: linear. Halves: logarithmic. Drops by one with two calls per level:
> exponential. Same sentence, two answers."

---

## 9. Recall card

- **"Why does it terminate?" is answered with the MEASURE, not the base case.** Three conditions, all
  three needed: it **strictly decreases** every call · it is **bounded below** · the **base case fires
  at that bound**. "There is a base case" only covers the third — and an unreachable one is worth
  nothing.
- **The measure need not be an argument** — it is any **non-negative integer function of the
  arguments** that strictly decreases. Euclid's is **`b`**, not `a` (which can grow: `gcd(3,100) →
  gcd(100,3)`); a grid path's is **`row + col`**; Ackermann's is the **pair, lexicographically**. And
  in **mutual recursion** it must decrease **around the cycle**, not within one function.
- **Three ways it fails, and only the first is obvious.** The measure never moves (`start` instead of
  `start + 1`) · it decreases but **steps over** the bound (`n - 2` towards `== 0` on odd inputs — works
  for even, never for odd) · it decreases and **never reaches** the floor (a halving float interval).
  **Fix the step, not the guard** — widening to `<= 0` turns a crash into a wrong answer.
- **A graph has NO natural measure, so the visited set creates one: `|V| − |seen|`.** It is the
  **termination argument, not an optimisation** — which is the whole reason graph DFS differs from tree
  DFS. Mark the node **before** recursing, and pass the set explicitly (**never a mutable default**).
- **The measure also gives you the complexity, from the same sentence.** Drops by 1, one call per
  level → **O(n)**. Halves → **O(log n)** (Euclid: ~90 calls at 10¹⁸). Drops by 1 with two calls per
  level → **O(2ⁿ)**. And **termination ≠ feasibility**: Ackermann provably terminates and `ackermann(4,2)`
  has 19,729 digits. If you cannot name a measure — **Collatz**, verified past 2⁶⁸ and unproved — add an
  explicit limit and raise.
