---
day: 147
track: dsa
title: "Finding the state: the hardest part of DP"
phase: "Dynamic programming"
status: written
---

# Finding the state: the hardest part of DP

## 1. What this is, and why they ask it

Everything else in dynamic programming is mechanical. Once you know what the subproblem is, the recurrence
follows from the last-move question, the base cases follow from the recurrence, and the code follows from
both.

**Deciding what the subproblem is — the state — is the part that is not mechanical**, and it is where every
hard DP problem is actually hard. A wrong state does not produce an error. It produces a solution that passes
the examples and is confidently wrong on the third test case, because two genuinely different situations were
treated as the same one.

They ask "what does `dp[i]` represent?" in almost every DP interview, and it is not a comprehension check. It
is the question, because a candidate who can state the state precisely has already done the hard part, and one
who cannot is about to write something that nearly works.

**The test is one sentence, and it is worth having as a reflex:** *given only the state, can I decide what
happens next without knowing anything else about how I got here?* If the answer is no, the state is
incomplete, and whatever is missing is the next dimension.

By the end of this lesson you can apply that test, recognise the five things that most often need to be in the
state, add a dimension without panicking, tell an incomplete state from a merely awkward one, and count the
state space before writing code.

---

## 2. The story

Ganpat has been a conductor on the Pune–Satara route for twenty-two years, and for the first two of them he
was, by his own account, useless.

The bus takes about seventy people and stops at fourteen places. The job is not the ticketing — anybody learns
that in a week. The job is standing at the door at each stop and deciding, in about four seconds, how many
people to let on.

What he did for two years was keep one number in his head: how many people were on board. Seventy is the
limit, so if he had fifty-eight, he let on twelve.

It went wrong constantly and he could not work out why.

At Shirwal he would let on twelve, and then at the next stop eighteen people would get off and the bus would
be half empty for the longest stretch of the route — money he could have had. Or he would refuse people at
Khambatki because he was at seventy, and then nobody got off for two stops and he had refused them for
nothing.

The change came from an older conductor who worked the same route and who said something Ganpat has repeated
many times since.

"You are counting the wrong thing. Count where they are going."

So he started keeping — and this took him a while, because it is more to hold — not one number but a small
set of them. Eleven for Shirwal. Twenty-two for Satara. Six for Wai. And so on down the route.

**Now the decision at the door is easy**, and it is easy because it is the same decision it always was, with
enough information to make it. Standing at Khambatki with sixty-six on board, he knows that twenty-nine of
them get off right here. So he can take on twenty-nine plus the four spare, and he does not have to guess, and
he is not refusing people he could carry.

The thing he says about it is that he did not get better at the job. **The job was always this. He was just
trying to do it with one number when the situation had never been one number.**

His son, who drives now, asked him once why nobody told him at the start. Ganpat said somebody probably did.

---

## 3. The idea in plain English

Ganpat's small set of numbers is the state, and his two useless years are what an incomplete state costs.

**The state is what identifies a subproblem.** It is the arguments to the recursive function, or the indices
into the table. `dp[i]`, `dp[i][j]`, `dp[i][j][k]`.

**And the whole of DP rests on one requirement: the state must be enough.** Enough for what? For deciding what
happens next, and for the answer to be the same every time you reach that state.

**The test, which is the reusable thing from today:**

> **Given only the state, can I decide what happens next without knowing anything else about how I got here?**

If yes, the state is complete and the DP will work. **If no, whatever you needed to know is the missing
dimension.**

Ganpat's total was not enough. Standing at the door with sixty-six on board, he could not decide how many to
let on, because he needed to know how many were getting off — and that was not derivable from sixty-six. So
sixty-six was an incomplete state, and the fix was not to think harder about sixty-six.

**Why an incomplete state fails silently is worth understanding.** If the state is missing something, then two
different situations map to the same table cell. The first one computed writes its answer there; the second
one reads it. **The second answer is not merely approximate — it is the answer to a different question**, and
nothing anywhere reports a problem.

**Five things most often need to be in the state**, and recognising them is most of the skill:

**One: a resource that is being consumed.** Remaining capacity in a knapsack, money left, moves left, fuel.
`dp[i]` is not enough because "at item `i` with 8 kg left" and "at item `i` with 3 kg left" have different
answers. → `dp[i][remaining]`.

**Two: a count of something limited.** Transactions used, stops taken, deletions allowed, jumps made.
"Reached Delhi in two stops" and "reached Delhi in four stops" have different futures. → `dp[i][used]`.

**Three: a mode you are currently in.** Holding a stock or not. Inside a group or not. On a cooldown or not.
**The tell is a rule that says "after you do X you cannot do Y"** — the "after X" is a mode. →
`dp[i][holding]`.

**Four: a position in a second sequence.** Every problem comparing two strings — edit distance, longest common
subsequence — needs both positions, because "at index 4 of the first string" says nothing without knowing
where you are in the second. → `dp[i][j]`.

**Five: a set of things already used**, when there are few enough of them. Cities visited in a travelling
salesman route, people already matched. → a bitmask, `dp[i][mask]`, and only when `n` is about twenty or less
because the state space is `2^n`.

**Now the distinction that matters most: an *incomplete* state and an *awkward* state are different problems.**

**Incomplete** means the answer genuinely depends on something you have not recorded, and the fix is another
dimension. There is no way round it.

**Awkward** means the state is sufficient but the recurrence is unpleasant — and the fix is to redefine what
`dp[i]` *means*, not to add to it. Maximum subarray is the standard example: "the best subarray using elements
up to `i`" is complete but leads nowhere, while "the best subarray **ending exactly at** `i`" is the same
amount of information and gives a one-line recurrence. **Changing the meaning is often more powerful than
adding a dimension**, and it is the move people do not think of.

**Adding a dimension is not a defeat and it is not expensive to think about.** The recurrence changes in one
predictable way: every branch now says what happens to the new dimension as well. Take the item → `remaining`
drops by its weight. Sell the stock → `holding` becomes false. **The last-move question still produces it**;
there is just more to say about each move.

**And before writing anything, count the state space and say the number.** States times work per state is the
cost, and both terms come from the state you just defined:

```
dp[i]            n states
dp[i][j]         n x m
dp[i][capacity]  n x W          <- W is the CAPACITY, not the item count
dp[i][mask]      n x 2^n        <- fine at n=20, impossible at n=40
```

**That last line is why the counting matters.** A state that is correct and has `2^40` cells is not a
solution, and noticing that before writing is much better than noticing it afterwards.

---

## 4. The picture

The test, applied:

```
  "Given only the state, can I decide what happens next?"

  CLIMBING STAIRS,  state = i
     at step 8, how many ways to finish?
     -> depends only on 8.  COMPLETE.

  KNAPSACK,  state = i
     at item 5, what is the best I can do?
     -> depends on how much capacity is LEFT, which is not in the state.
     -> INCOMPLETE.  Add it:  dp[i][remaining]

  STOCK WITH ONE TRANSACTION,  state = day
     on day 9, what is the best profit from here?
     -> depends on whether I am currently HOLDING a share.
     -> INCOMPLETE.  Add it:  dp[day][holding]

  EDIT DISTANCE,  state = i
     at index 4 of the first string, what is the cost?
     -> meaningless without knowing where I am in the SECOND string.
     -> INCOMPLETE.  Add it:  dp[i][j]
```

What an incomplete state does, concretely:

```
  knapsack with state = i only, items (weight, value):
     A(3, 4)   B(4, 5)   C(2, 3)     capacity 5

  path 1: take A          -> at item 1, remaining 2
  path 2: skip A          -> at item 1, remaining 5

  BOTH write to dp[1].

  whichever runs first wins, and the other reads an answer
  computed under a completely different amount of capacity.

  no error. the table is full. the number is wrong.
```

Adding a dimension, drawn:

```
  ONE DIMENSION                     TWO DIMENSIONS

  dp[i]                             dp[i][remaining]

  i:  0   1   2   3                        remaining
      .   .   .   .                     0  1  2  3  4  5
                                  i=0  .  .  .  .  .  .
  one answer per item          -> i=1  .  .  .  .  .  .
                                  i=2  .  .  .  .  .  .
                                  i=3  .  .  .  .  .  .

  "at item 2"                       "at item 2 with 3 kg left"
  -> not a question                 -> a question with one answer
```

Redefining rather than extending:

```
  MAXIMUM SUBARRAY

  state A: dp[i] = the best subarray using elements 0..i
    -> complete, and useless:
       to extend it I need to know whether the best one
       ENDS at i, and that is not recorded.

  state B: dp[i] = the best subarray ENDING EXACTLY at i
    -> same amount of information, one-line recurrence:
       dp[i] = max(dp[i-1] + nums[i], nums[i])
    -> and the answer is max(dp), not dp[n-1]

  SAME dimension count. Different meaning. That is the move.
```

---

## 5. The code, built step by step

**Start with a problem where one dimension is not enough, and watch it fail.**

The 0/1 knapsack: items with weights and values, a capacity, take each item at most once, maximise value.

**The naive one-dimensional attempt:**

```python
@lru_cache(maxsize=None)
def best_wrong(i: int) -> int:
    """dp[i] = the best value from items i onwards.  INCOMPLETE."""
    if i == len(items):
        return 0
    weight, value = items[i]
    return max(value + best_wrong(i + 1),      # take it -- but with what capacity?
               best_wrong(i + 1))              # skip it
```

**Read the `take` branch.** It adds the value and moves on, and nothing anywhere records that capacity was
consumed. **So this takes every item**, and returns the sum of all values regardless of the capacity.

**Apply the test:** "at item 5, what is the best I can do?" — that depends on how much room is left, and the
state does not say. **Incomplete.**

**The fix, and the recurrence changes in exactly one predictable way:**

```python
@lru_cache(maxsize=None)
def best(i: int, remaining: int) -> int:
    """dp[i][remaining] = the best value from items i onwards, with `remaining` capacity."""
    if i == len(items):
        return 0
    weight, value = items[i]
    skip = best(i + 1, remaining)
    take = value + best(i + 1, remaining - weight) if weight <= remaining else 0
    return max(take, skip)
```

**Two things changed.** The state gained a dimension. And each branch now says what happens to it: skipping
leaves `remaining` alone, taking reduces it. **That is all adding a dimension ever means.**

**Note the `if weight <= remaining`**, which is the new dimension making a branch *illegal* rather than merely
worse. That is common and it is the thing to check when adding a resource.

**Now a mode dimension**, which looks different and is the same idea. Buying and selling a stock, at most one
transaction, and you cannot buy while holding:

```python
@lru_cache(maxsize=None)
def profit(day: int, holding: bool) -> int:
    """dp[day][holding] = the best profit from `day` onwards, given whether I hold a share."""
    if day == len(prices):
        return 0
    do_nothing = profit(day + 1, holding)
    if holding:
        act = prices[day] + profit(day + 1, False)      # sell
    else:
        act = -prices[day] + profit(day + 1, True)      # buy
    return max(do_nothing, act)
```

**"On day 9, what should I do?" is unanswerable without knowing whether I am holding**, so `holding` is in the
state. **Two values, so the state space only doubles** — a cheap dimension.

**And a count dimension**, which is the third kind. At most `k` transactions:

```python
@lru_cache(maxsize=None)
def profit_k(day: int, holding: bool, transactions_left: int) -> int:
    if day == len(prices) or transactions_left == 0:
        return 0
    do_nothing = profit_k(day + 1, holding, transactions_left)
    if holding:
        act = prices[day] + profit_k(day + 1, False, transactions_left - 1)   # a sale completes one
    else:
        act = -prices[day] + profit_k(day + 1, True, transactions_left)
    return max(do_nothing, act)
```

**Three dimensions, and the state space is `days × 2 × (k+1)`.** Count it before writing: at 1,000 days and
`k = 100`, that is 202,000 states — fine. **At `k` unbounded it would be 1,000 × 2 × 1,000 = two million**,
still fine, and worth having computed rather than assumed.

**Note where the transaction is counted** — on the sale, not the purchase. Either works as long as it is
consistent, and mixing them double-counts. **That is a decision to state, not a detail.**

**Now the redefinition move**, which is the alternative to adding a dimension. Maximum subarray, done the
awkward way first:

```python
# dp[i] = the best subarray among elements 0..i     -- complete, and useless
# to compute dp[i] I need to know whether the best subarray for i-1 ENDED at i-1,
# which dp[i-1] does not tell me.
```

**The state is sufficient in principle** — the answer for `0..i` is determined by `i` — but the *recurrence*
cannot be written, because extending requires information the state does not carry.

```python
def max_subarray(nums: list[int]) -> int:
    # dp[i] = the best sum of a subarray ENDING EXACTLY at i
    best_here = best_overall = nums[0]
    for value in nums[1:]:
        best_here = max(best_here + value, value)
        best_overall = max(best_overall, best_here)
    return best_overall
```

**Same one dimension. Different meaning. One-line recurrence.** And the consequence of the new meaning is that
the answer is the maximum over all cells rather than the last one.

**The check to run before coding anything: count the state space.**

```python
def state_space_report(n: int, capacity: int, k: int) -> None:
    print(f"dp[i]            {n:>15,}")
    print(f"dp[i][j]         {n * n:>15,}")
    print(f"dp[i][capacity]  {n * (capacity + 1):>15,}")
    print(f"dp[i][k][mode]   {n * (k + 1) * 2:>15,}")
    print(f"dp[i][mask]      {n * 2 ** min(n, 40):>15,}")
```

**If the number is above about ten million, the state is wrong or the problem is not DP**, and finding that
out in ten seconds is much better than finding it out in twenty minutes.

### The complete solution

```python
"""Finding the state: the test, the five kinds of dimension, and what an incomplete state does."""

from __future__ import annotations

from functools import lru_cache


# ---- 1. a resource being consumed ---------------------------------------

def knapsack(items: list[tuple[int, int]], capacity: int) -> int:
    """dp[i][remaining] = the best value from items i.. with `remaining` capacity.

    One dimension is NOT enough: "at item 5" has no answer without knowing
    how much room is left.
    """
    @lru_cache(maxsize=None)
    def best(i: int, remaining: int) -> int:
        if i == len(items):
            return 0
        weight, value = items[i]
        skip = best(i + 1, remaining)
        if weight > remaining:
            return skip                       # the dimension makes this branch ILLEGAL
        return max(value + best(i + 1, remaining - weight), skip)

    return best(0, capacity)


def knapsack_broken(items: list[tuple[int, int]], capacity: int) -> int:
    """The one-dimensional attempt. Takes everything, because nothing tracks capacity."""
    @lru_cache(maxsize=None)
    def best(i: int) -> int:
        if i == len(items):
            return 0
        _, value = items[i]
        return max(value + best(i + 1), best(i + 1))

    return best(0)


# ---- 2. a mode you are in ------------------------------------------------

def one_transaction(prices: list[int]) -> int:
    """dp[day][holding]. "What now?" is unanswerable without knowing if I hold."""
    @lru_cache(maxsize=None)
    def profit(day: int, holding: bool) -> int:
        if day == len(prices):
            return 0
        wait = profit(day + 1, holding)
        if holding:
            return max(wait, prices[day] + profit(day + 1, False))
        return max(wait, -prices[day] + profit(day + 1, True))

    return profit(0, False)


# ---- 3. a count of something limited ------------------------------------

def at_most_k_transactions(prices: list[int], k: int) -> int:
    """dp[day][holding][left]. A sale consumes one transaction — state that, and be consistent."""
    @lru_cache(maxsize=None)
    def profit(day: int, holding: bool, left: int) -> int:
        if day == len(prices) or left == 0:
            return 0
        wait = profit(day + 1, holding, left)
        if holding:
            return max(wait, prices[day] + profit(day + 1, False, left - 1))
        return max(wait, -prices[day] + profit(day + 1, True, left))

    return profit(0, False, k)


# ---- 4. redefining rather than extending --------------------------------

def max_subarray(nums: list[int]) -> int:
    """dp[i] = best sum ENDING EXACTLY at i. Same dimension, different meaning."""
    best_here = best_overall = nums[0]
    for value in nums[1:]:
        best_here = max(best_here + value, value)
        best_overall = max(best_overall, best_here)
    return best_overall


# ---- the check to run before coding -------------------------------------

def state_space(n: int, capacity: int = 0, k: int = 0, mask_bits: int = 0) -> int:
    total = n
    if capacity:
        total *= capacity + 1
    if k:
        total *= k + 1
    if mask_bits:
        total *= 2 ** mask_bits
    return total


if __name__ == "__main__":
    items = [(3, 4), (4, 5), (2, 3)]
    print("knapsack correct :", knapsack(items, 5))
    print("knapsack broken  :", knapsack_broken(items, 5), " (it takes everything)")
    print("sum of all values:", sum(v for _, v in items))
    print()

    prices = [7, 1, 5, 3, 6, 4]
    print("one transaction  :", one_transaction(prices))
    print("k = 2            :", at_most_k_transactions(prices, 2))
    print("k = 100          :", at_most_k_transactions(prices, 100))
    print()

    print("max_subarray     :", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print()

    print("state space, n=1000, capacity=10000 :", f"{state_space(1000, capacity=10000):,}")
    print("state space, n=1000, k=100, mode    :", f"{state_space(1000, k=100) * 2:,}")
    print("state space, n=20,  bitmask         :", f"{state_space(20, mask_bits=20):,}")
    print("state space, n=40,  bitmask         :", f"{state_space(40, mask_bits=40):,}")
```

Running it:

```
knapsack correct : 7
knapsack broken  : 12  (it takes everything)
sum of all values: 12

one transaction  : 5
k = 2            : 7
k = 100          : 7

max_subarray     : 6

state space, n=1000, capacity=10000 : 10,001,000
state space, n=1000, k=100, mode    : 202,000
state space, n=20,  bitmask         : 20,971,520
state space, n=40,  bitmask         : 43,980,465,111,040
```

Three things to look at. **The broken knapsack returns 12, which is the sum of every value** — it took all
three items into a capacity of 5, because nothing in the state stopped it. **It did not crash and it did not
warn**, which is the failure mode this lesson exists for.

**`k = 100` gives the same answer as `k = 2`**, because there are only two profitable transactions available.
That is a good sanity check that the transaction counting is right.

And the last two lines are why you count before writing: **a bitmask at `n = 20` is twenty million cells and
viable; at `n = 40` it is forty-four trillion and is not.** The state is correct in both cases; only one of
them is a solution.

---

## 6. What it costs

**The formula, and both terms come from the state:**

```
time  = (number of states) x (work per state)
space = (number of states), before optimisation
```

**So counting the state space is costing the solution**, and it takes ten seconds:

```
dp[i]                     n
dp[i][j]                  n x m
dp[i][capacity]           n x (W + 1)
dp[i][k][mode]            n x (k + 1) x 2
dp[i][mask]               n x 2^n
```

**Concrete sizes, and where each one stops being viable:**

```
n = 1,000                                          1,000            trivial
n = 1,000, m = 1,000                               1,000,000        fine
n = 1,000, capacity = 10,000                       10,000,000       fine, ~1 s in Python
n = 1,000, capacity = 1,000,000                    1,000,000,000    too big
n = 20, bitmask                                    20,000,000       fine
n = 25, bitmask                                    800,000,000      borderline
n = 40, bitmask                                    4.4 x 10^13      impossible
```

**The practical ceiling in Python is around ten million states** with constant work each. **Above that, either
the state is wrong, the problem wants a different technique, or a dimension can be collapsed.**

**The knapsack's capacity dimension is worth a specific note**, because it is the classic surprise:

```
dp[i][capacity]  ->  O(n x W)
```

**That is *not* polynomial in the input size**, because `W` is a number written in the input, and writing
`W = 1,000,000` takes seven characters. **This is "pseudo-polynomial"**, and it is why knapsack is NP-hard
despite having a DP solution — the table is polynomial in the *value* of `W`, not in the number of digits.

```
W = 1,000        n x 1,000        fine
W = 10^9         n x 10^9         impossible, and the input got 6 characters longer
```

**Saying that sentence is a strong signal**, because it shows you know why a DP solution does not contradict
NP-hardness.

**Adding a dimension multiplies, it does not add:**

```
dp[i]              1,000 states
dp[i][j]           1,000 x 1,000 = 1,000,000        -> 1,000x
dp[i][j][k]        1,000 x 1,000 x 100 = 10^8       -> another 100x
```

**So a third dimension is usually the point where the approach needs rethinking**, and a fourth almost always
is.

**Which dimensions are cheap and which are expensive:**

```
a boolean mode        x2              always cheap
a small count (k)     x(k+1)          cheap when k is bounded
a second sequence     x m             usually fine
a capacity            x W             depends entirely on W's magnitude
a bitmask             x 2^n           only for n <= ~22
```

**The work per state matters as much as the count**, and it is the length of the last-move enumeration:

```
knapsack           2 branches            O(1) per state
coin change        one per coin          O(coins) per state
word break         one per split point   O(n) per state
interval DP        one per split point   O(n) per state -> O(n^3) overall
```

**And an incomplete state costs nothing and returns the wrong answer**, which is the whole point:

```
broken knapsack    n states, O(1) each   -> fast, and wrong
correct knapsack   n x W states          -> slower, and right
```

**There is no performance argument for the incomplete state.** It is not a trade-off; it is a bug that happens
to run quickly.

---

## 7. The traps

### The state that is missing a resource

```python
@lru_cache(maxsize=None)
def best(i):
    return max(value[i] + best(i + 1), best(i + 1))
```

```
>>> knapsack_broken([(3,4), (4,5), (2,3)], capacity=5)
12                                    # the sum of everything. Capacity 5, weight 9.
```

**Nothing tracks the resource, so nothing prevents taking every item.** The failure is not subtle once you see
it and is invisible while writing it, because the `take` branch looks complete — it adds the value and moves
on.

**The test catches it in five seconds:** "at item 5, what is the best I can do?" — it depends on the remaining
capacity, which is not in the state.

### Memoising on fewer arguments than the state has

```python
cache = {}
def best(i, remaining):
    if i in cache:                    # keyed on i ALONE
        return cache[i]
    ...
    cache[i] = answer
```

**This is the same bug wearing a disguise.** The function takes the right arguments; the cache does not. Two
different `remaining` values share a cell, and whichever runs first wins.

```
>>> knapsack_bad_cache([(3,4), (4,5), (2,3)], 5)
9                                     # neither 8 nor 12 — a mixture
```

**The cache key must be the complete state**, every time. `@lru_cache` does this automatically, which is a real
argument for using it over a hand-rolled dictionary.

### An unhashable argument

```python
@lru_cache(maxsize=None)
def solve(i, used: list[int]):
    ...
```

```
TypeError: unhashable type: 'list'
```

**Usually a signal that the state is wrong**, not merely awkwardly typed. If the state genuinely needs "which
items are used", that is a bitmask — an integer — and the state space is `2^n`, which you should count before
committing.

### Adding a dimension that is derivable

```python
dp[i][total_so_far]                   # when total_so_far is determined by i
```

If the extra value can be computed from the others, it is not a dimension — it is redundancy, and it multiplies
the state space for nothing.

**The test again:** *does the answer differ for two states that agree on everything else?* If not, drop it.
Adding dimensions defensively is a real habit and it turns a viable solution into an impossible one.

### Not counting the state space

```python
@lru_cache(maxsize=None)
def solve(i, mask):                   # n = 40
    ...
```

The code is correct. It never finishes, and there is no error — just a process that runs until it is killed,
or a `MemoryError` after several minutes.

```
n = 40 bitmask -> 4.4 x 10^13 states
```

**Ten seconds of arithmetic before writing would have said so**, and the correct response is to look for a
different formulation rather than to wait.

### Confusing an incomplete state with an awkward one

```python
# "dp[i] = the best subarray among 0..i doesn't work, so I need dp[i][j]"
```

**No.** That state is complete — the answer for `0..i` is determined by `i`. What is missing is a *usable
recurrence*, and the fix is to change what `dp[i]` means to "ending exactly at `i`", which is the same
dimension.

**Adding a dimension when a redefinition would do turns an `O(n)` solution into `O(n²)`**, and it is a common
over-reaction to being stuck.

### Inconsistent accounting on a count dimension

```python
if holding:
    return prices[day] + profit(day + 1, False, left - 1)     # sale consumes one
else:
    return -prices[day] + profit(day + 1, True, left - 1)     # ... and so does the purchase
```

Each round trip now consumes two transactions, so `k = 2` behaves like `k = 1`.

```
>>> at_most_k_double_count([7,1,5,3,6,4], 2)
5                                     # the answer is 7
```

**Decide whether a transaction is counted at the buy or the sell, state it, and do it in exactly one place.**
The bug returns a plausible smaller number, which is the worst kind.

### Off-by-one on a count's base case

```python
if left == 0:
    return 0
```

Correct if `left` means "transactions still available". **Wrong if it means "transactions used"**, where the
guard should be `left == k`. Both readings are natural; **the state sentence decides which**, and writing it
down prevents the confusion.

---

## 8. In the interview

### How it gets asked

- *"What does `dp[i]` represent in your solution?"* — asked in almost every DP round.
- *"Your solution gives the right answer on the example and the wrong one here."* — an incomplete state.
- *"Now there is a limit of at most `k` transactions."* — a count dimension.
- *"Now you cannot buy the day after selling."* — a mode dimension.
- *"How many states are there?"* — the sizing question.
- *"Can you do it with less memory?"* — which requires knowing what each cell depends on.

### The first ninety seconds

> "Before I write anything, let me work out what the subproblem is, because that is the part that is not
> mechanical — once the state is right, the recurrence and the base cases follow.
>
> **The test I use is: given only the state, can I decide what happens next without knowing anything else about
> how I got here?**
>
> So for this problem — if the state is just the item index, then 'at item 5, what is the best I can do?' has no
> answer, because it depends on how much capacity is left, and that is not in the state. **Two different paths
> reach item 5 with different amounts of room, and they have different answers, so they cannot share a table
> cell.**
>
> **That is the failure mode I want to avoid, and it is silent.** If the state is incomplete, two genuinely
> different situations write to and read from the same cell, and the result is not approximate — it is the
> answer to a different question, with nothing anywhere reporting a problem.
>
> **So the state is `(item index, remaining capacity)`**, and I would write that as a sentence: `dp[i][r]` is
> the best value obtainable from items `i` onwards with `r` capacity remaining.
>
> **Adding the dimension changes the recurrence in exactly one way:** each branch now says what happens to it.
> Skip the item and `r` is unchanged; take it and `r` drops by the weight — and taking becomes illegal if the
> weight exceeds `r`, which is the new dimension pruning branches rather than just costing them.
>
> **And before I write it, let me count the state space**, because that is the cost: `n` times `W + 1`. With a
> hundred items and a capacity of a thousand, that is a hundred thousand cells with constant work each —
> trivial. **If the capacity were a billion, this approach would not work at all**, and I would rather know
> that now.
>
> Shall I write the memoised version?"

### The follow-ups

**"What does `dp[i][j]` represent? Be precise."**

> "For edit distance: **the minimum number of operations to turn the first `i` characters of string A into the
> first `j` characters of string B.**
>
> **And the precision matters in two specific ways.** 'The first `i` characters' rather than 'up to index `i`'
> — that is a prefix-length convention, so the table is `(n+1) × (m+1)` and `dp[0][0]` is the empty-to-empty
> case, which is zero. If I said 'up to index `i`' the table would be `n × m` and I would have nowhere to put
> the empty prefixes.
>
> **And 'turn A into B' rather than 'the difference between them'** — the operations are directional, so I need
> to know which way round, otherwise insert and delete get confused.
>
> **The reason I labour this is that the sentence produces the rest of the solution.** The base cases fall out:
> `dp[i][0]` is `i`, because turning `i` characters into nothing means `i` deletions. `dp[0][j]` is `j`. And
> the answer is `dp[n][m]`, the full lengths, which follows from 'the first `i`' meaning a length.
>
> **A vaguer sentence gives a vaguer table**, and the off-by-one errors in this problem all come from not
> having decided whether the index is a position or a length."

**"My solution passes the example and fails the third test case."**

> "Almost always an incomplete state, and I would check that before anything else.
>
> **The way it fails is diagnostic.** If the answer is too large in a maximisation, some constraint is not
> being enforced — which usually means the resource being consumed is not in the state, so the recursion is
> taking things it cannot afford. If it is too small, a branch is being wrongly pruned or a mode is being
> lost.
>
> **The check is to apply the test to my own state.** Pick a middle cell and ask: could two genuinely different
> situations reach here? If yes, what distinguishes them, and is it recorded? That question finds it in about
> a minute, and it is faster than tracing the recursion.
>
> **A concrete way to confirm it** is to print the arguments on every call and look for two calls with the same
> arguments that ought to have different answers. If the cache is returning a hit for something that should be
> different, the state is short.
>
> **The other candidate**, and I would check it second, is that the cache key does not match the function's
> arguments — a hand-rolled dictionary keyed on `i` when the function takes `(i, remaining)`. That produces
> exactly the same symptom and is easy to miss, which is one reason I prefer `lru_cache`: it keys on everything
> automatically."

**"Now there is a limit of at most `k` transactions."**

> "A count dimension. The state becomes `(day, holding, transactions_left)`, and everything else is unchanged
> in structure.
>
> **Why it has to be in the state:** 'on day 9, holding a share' is no longer enough, because reaching that
> point with four transactions left and with zero left have completely different futures. Two different
> situations, so two different cells.
>
> **The decision I would state explicitly is where the transaction is counted** — at the buy or at the sell. I
> would count it at the sell, because a completed transaction is a round trip. **Whichever I choose, it must
> happen in exactly one place**; decrementing on both halves makes each round trip cost two, and then `k = 2`
> behaves like `k = 1` and returns a plausible smaller number.
>
> **State space: days × 2 × (k+1).** At a thousand days and `k = 100` that is two hundred and two thousand
> cells, which is nothing. **And there is a nice observation worth making: `k` above `n/2` is the same as
> unlimited**, because you cannot complete more than `n/2` round trips in `n` days — so I would cap `k` at
> `n/2` up front, which turns a potentially huge `k` into a bounded one and handles the 'unlimited
> transactions' variant with the same code."

**"Reduce the memory."**

> "That requires knowing exactly what each cell depends on, which is another reason the state sentence is worth
> writing.
>
> **For the knapsack, `dp[i][r]` reads only row `i+1`** — nothing from `i+2` or earlier. So I keep one row
> instead of `n`, and the space goes from `O(n·W)` to `O(W)`.
>
> **And then the iteration direction becomes part of the correctness**, which is the subtlety. For 0/1
> knapsack, where each item may be used once, I iterate capacity **downwards**, so that when I read
> `row[r - weight]` it still holds the previous item's value. **Iterating upwards makes it the unbounded
> knapsack** — the same code, silently solving a different problem, because the item can then be re-used within
> the same row.
>
> **That is a genuinely nasty bug** because both versions are correct programs for different problems, and the
> only difference is a `range` direction.
>
> **What I give up** is the ability to say *which* items were chosen, because the table recorded that and I
> discarded it. So I would ask whether the value alone is enough before optimising — and if the items are
> wanted, keep the full table and walk it backwards, comparing each cell against the row above to see whether
> the item was taken."

### The model answer

*"You are given an array of prices and may complete at most two transactions, buying and selling one share at a
time. Maximise your profit. Walk me through how you decide the state."*

> "Let me do this slowly, because deciding the state is the whole problem and the code is short once it is
> right.
>
> **First attempt: `dp[day]` — the best profit from this day onwards.** Apply the test: on day 9, what is the
> best I can do? **That depends on whether I currently hold a share**, because if I do, my options are sell or
> wait, and if I do not, they are buy or wait. Different options means different answers, so `day` alone is
> incomplete.
>
> **Second attempt: `dp[day][holding]`.** Now 'day 9, holding' is a question with an answer. **And this is
> exactly right for the unlimited-transactions version.** But here there is a limit of two.
>
> **Apply the test again: on day 9, holding a share, what is the best I can do?** That depends on how many
> transactions I have already used — reaching that point having used none and having used two are completely
> different situations, and the second one has no future at all.
>
> **So the state is `(day, holding, transactions_left)`**, and the sentence is: the maximum additional profit
> obtainable from `day` onwards, given whether I currently hold a share and how many transactions remain.
>
> **Three dimensions, and I would count the space before writing: `n × 2 × 3`.** For a thousand days that is
> six thousand states with constant work each — trivial. **Counting it also tells me the general version is
> fine**: at most `k` transactions is `n × 2 × (k+1)`, and since `k` above `n/2` is equivalent to unlimited, I
> can cap it and the state space never exceeds `n²`.
>
> **The recurrence, from the last-move question at each state.** On any day I either do nothing — same state,
> next day — or I act. If holding, acting means selling: gain the price, stop holding, and **consume one
> transaction**. If not holding, acting means buying: pay the price and start holding. **I count the
> transaction at the sell**, and I would say that out loud because counting it at both ends is the bug that
> makes `k = 2` behave like `k = 1`.
>
> **Base cases:** past the last day, or no transactions left, the profit from here is zero.
>
> **The alternative formulation worth mentioning** is four explicit variables — the best balance after the
> first buy, after the first sell, after the second buy, after the second sell — updated in one pass. That is
> `O(1)` space and it is the version people memorise. **I would derive the general one first**, because it
> extends to any `k` and to the cooldown and transaction-fee variants without rethinking, whereas the four
> variables do not.
>
> **And the cooldown variant is exactly a fourth dimension — or rather a third state value rather than a
> boolean:** instead of holding or not, the modes become holding, free-to-buy, and resting. **That is a mode
> dimension growing from two values to three**, which is the smallest possible change, and it is a good example
> of why getting the state framework right is worth more than memorising any individual solution."

---

## 9. Recall card

**The state is what identifies a subproblem, and the test is one sentence:** *given only the state, can I
decide what happens next without knowing anything else about how I got here?* If no, whatever is missing is the
next dimension.

**An incomplete state fails silently** — two different situations share a cell, and the answer is not
approximate, it is the answer to a different question.

**Five things that usually need to be in the state:** a **resource** being consumed (capacity, money), a
**count** of something limited (transactions, stops), a **mode** you are in (holding, on cooldown), a position
in a **second sequence**, and a **set already used** (bitmask, only for `n ≲ 22`).

**Incomplete and awkward are different.** Incomplete needs another dimension; awkward needs the *meaning*
changed — "best subarray **ending exactly at** `i`" instead of "using elements up to `i`". **Redefining is
often better than extending**, and adding a dimension when redefining would do turns `O(n)` into `O(n²)`.

**Count the state space before writing.** Adding a dimension **multiplies**; the practical ceiling is ~10⁷
states in Python; and `dp[i][capacity]` is **pseudo-polynomial** — polynomial in the *value* of `W`, not in its
number of digits, which is why knapsack has a DP solution and is still NP-hard.
