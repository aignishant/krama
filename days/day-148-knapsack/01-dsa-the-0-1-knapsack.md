---
day: 148
track: dsa
title: "The 0/1 knapsack"
phase: "Dynamic programming"
status: written
---

# The 0/1 knapsack

## 1. What this is, and why they ask it

You have a set of items, each with a weight and a value, and a bag that holds a fixed total weight. Take each
item at most once. Maximise the value you carry.

That is the 0/1 knapsack, and it is the most important single problem in dynamic programming — not because it
appears often by name, but because **an enormous number of problems are it in disguise**. Can this array be
split into two equal halves? Can I make exactly this total from these numbers? What is the closest I can get
to a target? All of them are knapsack with the value and the weight set to the same thing.

It is also the first problem in this phase where the state genuinely needs two dimensions, so it is
[yesterday's lesson](../day-147-finding-the-state/README.md) made concrete: `dp[i]` alone is not a question,
and `dp[i][remaining]` is.

**And greedy fails twice**, which is what makes it worth asking. Taking the most valuable item first is wrong.
Taking the best value-per-kilo first is also wrong — and that second one is subtle, because it is *correct* for
a slightly different problem, which is exactly why people believe it.

By the end of this lesson you can write it top-down and bottom-up, collapse it to one row and get the
iteration direction right, produce both greedy counter-examples, recognise the subset-sum family, and explain
why a polynomial-looking DP does not contradict the problem being NP-hard.

---

## 2. The story

Bhagwan sells at four weekly markets and everything he takes goes on the carrier of the cycle, which holds
about forty kilos before the frame starts to complain.

What he has in the room at home is always more than forty kilos. Steel tumblers, plastic buckets, cheap
torches, mosquito nets, a box of locks, two kinds of rope. Each one weighs what it weighs and each one makes
him a different amount of money at the market.

The first year he took the expensive things. It seemed like the whole answer — you can only carry so much, so
carry the valuable stuff.

**That was wrong and it was wrong in an obvious way.** The mosquito nets make eleven hundred rupees and weigh
twenty-two kilos, so a bundle of them fills over half the carrier. In the space left he could take a torch or
two. Meanwhile the locks are four hundred rupees for six kilos, the tumblers three hundred for four, and the
rope two hundred and fifty for three — and those three together are thirteen kilos and nine hundred and fifty
rupees, which is nearly the nets in a third of the weight.

So the second year he worked out the rupees per kilo and took things in that order, which felt much cleverer.

**And that is wrong too, and it took him longer to see because it is nearly right.**

The week it caught him out, the best thing per kilo was the rope at eighty-three a kilo, then the tumblers at
seventy-five, then the locks at sixty-seven. He loaded rope, tumblers, locks — thirteen kilos, nine hundred
and fifty rupees — and then had twenty-seven kilos of space and nothing that fitted well into it. The next
best per kilo was a crate of buckets at fifty a kilo, and it weighed thirty kilos, and thirty does not fit in
twenty-seven.

He went with a third of the carrier empty.

If he had left the locks behind — the worst of the three he took — he would have had thirty-three kilos free,
the buckets would have gone in, and he would have made fifteen hundred instead of nine-fifty.

**The thing that took him years to accept is that there is no order.** There is no rule of the form "take the
best X first" that works, because whether an item is worth taking depends entirely on what else fits around it,
and you cannot know that by looking at the item.

What he does now, on Thursday evenings, is go through the pile item by item and ask two questions about each
one: what is the best I can do with the rest of the pile if I take this, and what is the best if I leave it.
It takes him a while. It has never once been wrong.

---

## 3. The idea in plain English

Bhagwan's Thursday evening is the 0/1 knapsack, and both of his wrong years are the greedy counter-examples.

**The problem.** `n` items, each with a weight `w` and a value `v`. A capacity `W`. Take each item at most
once — that is the "0/1", zero or one of each. Maximise the total value with total weight at most `W`.

**The state, applying [yesterday's test](../day-147-finding-the-state/README.md).** Try `dp[i]` = the best from
items `i` onwards. "At item five, what is the best I can do?" — **that has no answer**, because it depends on
how much room is left, and the room is not in the state. Two paths reach item five having taken different
things and having different capacity, and they have different answers.

**So the state is two-dimensional:**

> **`dp[i][r]` = the maximum value obtainable using items `i` onwards, with `r` capacity remaining.**

**And the recurrence is the last-move question, which here is the choice at item `i`:**

```
skip it:   dp[i+1][r]
take it:   value[i] + dp[i+1][r - weight[i]]      -- only if weight[i] <= r

dp[i][r] = max(skip, take)
```

**Note what the new dimension does to the `take` branch: it can make it illegal**, not merely worse. If the
item does not fit, there is no choice to make. That is different from house robber, where both branches were
always available.

**Now why greedy fails, twice, and being able to give both is the point.**

**Greedy by value.** Take the most valuable item first.

```
capacity 10
items:  A(weight 10, value 60)   B(weight 5, value 50)   C(weight 5, value 50)

greedy by value: take A          -> 60
correct:         take B and C    -> 100
```

**Greedy by value-per-weight.** Take the best ratio first.

```
capacity 10
items:  A(weight 6, value 60, ratio 10)   B(weight 5, value 40, ratio 8)   C(weight 5, value 40, ratio 8)

greedy by ratio: take A (6 kg), then neither B nor C fits (4 kg left)   -> 60
correct:         take B and C                                            -> 80
```

**And here is why the second one is so persuasive: it is correct for the *fractional* knapsack**, where you may
take part of an item. If you can take four-fifths of a crate of buckets, then filling the bag with the best
ratio first is provably optimal, and it is a genuine greedy algorithm.

**The moment items are indivisible, that proof collapses**, because the last item cannot be trimmed to fit and
the leftover space is wasted. **That is Bhagwan's twenty-seven kilos**, and it is the single most useful thing
to be able to say about this problem.

**So there is no ordering rule, and that is the whole reason it needs DP.** Whether an item belongs in the
answer depends on what fits around it, which cannot be determined by examining the item.

**The bottom-up table is two-dimensional and standard:**

```
dp[i][r] = the best value using the FIRST i items with capacity r
```

**Note this is the other convention from the recursive version** — "the first `i` items" rather than "items `i`
onwards" — because it makes `dp[0][*] = 0` a natural base case, and the loops run forwards. **Either works;
mixing them is the source of every off-by-one in this problem**, so state which one you are using.

**And then the space collapse, which is where the real subtlety is.**

`dp[i][r]` reads only row `i-1`, so one row suffices. But **the iteration direction over the capacity decides
which problem you are solving**:

```
for r in range(W, weight-1, -1):     # DOWNWARDS  -> 0/1 knapsack
    row[r] = max(row[r], value + row[r - weight])

for r in range(weight, W+1):         # UPWARDS    -> UNBOUNDED knapsack
    row[r] = max(row[r], value + row[r - weight])
```

**Downwards, `row[r - weight]` still holds the previous item's value**, so the item is used at most once.
**Upwards, it may already have been updated by this same item**, so the item can be used repeatedly.

**Two correct programs for two different problems, differing by a `range` direction**, and no error either way.
That is the most dangerous line in dynamic programming and it is worth writing on something.

**And the family, which is why this problem matters more than its own statement.** Set `value = weight` and the
question "what is the largest total I can reach without exceeding `W`" becomes:

- **Subset sum:** can I hit exactly `W`? Same table, booleans instead of numbers.
- **Partition equal subset sum:** can I split the array into two equal halves? That is subset sum with a
  target of `total / 2` — and if the total is odd, the answer is no before you start.
- **Target sum:** assign `+` or `−` to each number to reach a target. Rearranges into subset sum.
- **Last stone weight II:** minimise the difference between two groups. Subset sum for the half closest to
  `total / 2`.

**The tell for the whole family: choose a subset, subject to a total, optimising or checking something.**

**Finally, the complexity point that comes up.** `O(n × W)` looks polynomial and the problem is NP-hard, which
seems contradictory. **It is not, because `W` is a number written in the input.** A capacity of a billion takes
ten characters to write and makes the table a billion cells wide. **The table is polynomial in the *value* of
`W`, not in the number of digits** — which is called **pseudo-polynomial**, and it is why this DP exists and
the problem is still hard.

---

## 4. The picture

The two greedy failures, side by side:

```
BY VALUE                                BY VALUE PER WEIGHT

capacity 10                             capacity 10
A(10 kg, 60)                            A(6 kg, 60, ratio 10)
B( 5 kg, 50)                            B(5 kg, 40, ratio 8)
C( 5 kg, 50)                            C(5 kg, 40, ratio 8)

greedy: A          -> 60                greedy: A (6kg), 4 left, nothing fits -> 60
best:   B + C      -> 100               best:   B + C (10 kg)                 -> 80

  one heavy item blocks two               the best ratio leaves a gap
  lighter ones worth more                 nothing can fill
```

**What to notice on the right.** The ratio rule is *correct* if items can be cut — take all of A and
four-fifths of B for 92. **Indivisibility is what breaks it**, and that is the sentence to say.

The table, filled by hand:

```
items: A(w2, v3)  B(w3, v4)  C(w4, v5)      capacity 5

dp[i][r] = the best using the FIRST i items with capacity r

            r=0  r=1  r=2  r=3  r=4  r=5
  i=0 (none)  0    0    0    0    0    0
  i=1 (A)     0    0    3    3    3    3
  i=2 (A,B)   0    0    3    4    4    7      <- 7 = A + B, 5 kg
  i=3 (+C)    0    0    3    4    5    7

  answer dp[3][5] = 7   (A and B: 2+3 = 5 kg, 3+4 = 7)

  note dp[3][4] = 5:  C alone beats A alone at capacity 4
  and dp[3][5] stayed 7: C(4kg, 5) + nothing else beats A+B
```

**What to notice.** Each row reads only the row above it — `dp[i][r]` looks at `dp[i-1][r]` and
`dp[i-1][r - w]`. **That is why one row suffices**, and the two cells it reads are why the direction matters.

The direction, drawn:

```
  one row, processing item with weight 2, value 3

  DOWNWARDS (0/1)                        UPWARDS (unbounded)

  r:  5   4   3   2                      r:  2   3   4   5
      ^                                      ^
  row[5] = max(row[5], 3 + row[3])       row[2] = max(row[2], 3 + row[0])
           row[3] is still the PREVIOUS           row[0] unchanged, fine
           item's value                  row[4] = max(row[4], 3 + row[2])
                                                  row[2] was JUST updated
                                                  -> the item is used TWICE
```

**What to notice.** The upward version is not broken — it correctly solves the unbounded knapsack, where each
item may be taken any number of times. **Two right answers to two different questions, and one `range` call
between them.**

The family:

```
  0/1 KNAPSACK          maximise value, weight <= W

  set value = weight:

  SUBSET SUM            can I reach exactly W?          -> booleans
  PARTITION             split into two equal halves?    -> subset sum for total/2
  TARGET SUM            +/- each number to reach T      -> rearranges to subset sum
  LAST STONE II         minimise the difference         -> closest reachable to total/2

  all the same table.
```

---

## 5. The code, built step by step

**Start with the state, said out loud.**

> "`dp[i][r]` is the maximum value obtainable from items `i` onwards with `r` capacity remaining. One index is
> not enough, because 'at item five' has no answer without knowing the room left."

**Top-down, straight from the recurrence:**

```python
from functools import lru_cache

def knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)

    @lru_cache(maxsize=None)
    def best(i: int, remaining: int) -> int:
        if i == n:
            return 0
        skip = best(i + 1, remaining)
        if weights[i] > remaining:
            return skip                              # the item does not fit: no choice
        take = values[i] + best(i + 1, remaining - weights[i])
        return max(take, skip)

    return best(0, capacity)
```

**Nine lines, and the `if weights[i] > remaining` is the new dimension pruning a branch.** Without it,
`remaining` goes negative and the whole thing is wrong.

**Now bottom-up, and note the convention change.** The table uses "the first `i` items" rather than "items `i`
onwards", because that makes the base row all zeros and the loops run forwards:

```python
def knapsack_table(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    # dp[i][r] = the best value using the FIRST i items with capacity r
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for r in range(capacity + 1):
            dp[i][r] = dp[i - 1][r]                  # skip item i
            if w <= r:
                dp[i][r] = max(dp[i][r], v + dp[i - 1][r - w])   # take it
    return dp[n][capacity]
```

**`weights[i - 1]` because `i` counts items and indices start at zero.** That off-by-one is the price of the
convention and it is worth the base case being free.

**Then the space collapse, and this is the line to be careful with:**

```python
def knapsack_one_row(weights: list[int], values: list[int], capacity: int) -> int:
    row = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for r in range(capacity, w - 1, -1):         # DOWNWARDS: each item once
            row[r] = max(row[r], v + row[r - w])
    return row[capacity]
```

**Read the range.** Going down from `capacity` to `w`, so that when `row[r - w]` is read it has not yet been
touched this round — it still holds the value from before this item was considered. **That is what makes the
item usable at most once.**

**And the one-character difference:**

```python
def unbounded_knapsack(weights, values, capacity):
    row = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for r in range(w, capacity + 1):             # UPWARDS: unlimited copies
            row[r] = max(row[r], v + row[r - w])
    return row[capacity]
```

**Same three lines, opposite direction, different problem.** I would write the direction as a comment every
time, because six months later it reads identically.

**Now the family. Subset sum is the same table with booleans:**

```python
def can_reach(nums: list[int], target: int) -> bool:
    # reachable[r] = can some subset sum to exactly r?
    reachable = [False] * (target + 1)
    reachable[0] = True                              # the empty subset makes 0
    for number in nums:
        for r in range(target, number - 1, -1):      # downwards: each number once
            reachable[r] = reachable[r] or reachable[r - number]
    return reachable[target]
```

**`reachable[0] = True` is the base case and it is the one people forget** — the empty subset sums to zero, and
without it every cell stays false.

**And partition equal subset sum is that, with one check first:**

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                                 # an odd total cannot be halved
    return can_reach(nums, total // 2)
```

**The odd check is not an optimisation, it is a correctness shortcut** — and it is free.

**And reconstructing which items were taken**, which needs the full table:

```python
def knapsack_with_items(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for r in range(capacity + 1):
            dp[i][r] = dp[i - 1][r]
            if w <= r:
                dp[i][r] = max(dp[i][r], v + dp[i - 1][r - w])

    chosen, r = [], capacity
    for i in range(n, 0, -1):
        if dp[i][r] != dp[i - 1][r]:                 # the value changed -> item i was taken
            chosen.append(i - 1)
            r -= weights[i - 1]
    return dp[n][capacity], chosen[::-1]
```

**The test `dp[i][r] != dp[i-1][r]` means "including item `i` improved things"**, so it was taken. Walk
backwards, reduce the capacity by its weight, continue. **`O(n)` for the walk, and it needs the `O(n × W)`
table — so reconstruction and the one-row optimisation are mutually exclusive.**

### The complete solution

```python
"""The 0/1 knapsack, its one-row form, the direction that changes the problem, and the family."""

from __future__ import annotations

from functools import lru_cache


def knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """Top-down. dp[i][r] = the best from items i.. with r capacity remaining."""
    n = len(weights)

    @lru_cache(maxsize=None)
    def best(i: int, remaining: int) -> int:
        if i == n:
            return 0
        skip = best(i + 1, remaining)
        if weights[i] > remaining:
            return skip
        return max(values[i] + best(i + 1, remaining - weights[i]), skip)

    return best(0, capacity)


def knapsack_table(weights: list[int], values: list[int], capacity: int) -> int:
    """Bottom-up. dp[i][r] = the best using the FIRST i items with capacity r."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for r in range(capacity + 1):
            dp[i][r] = dp[i - 1][r]
            if w <= r:
                dp[i][r] = max(dp[i][r], v + dp[i - 1][r - w])
    return dp[n][capacity]


def knapsack_one_row(weights: list[int], values: list[int], capacity: int) -> int:
    """One row. The DOWNWARD range is what makes each item usable at most once."""
    row = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for r in range(capacity, w - 1, -1):          # <-- 0/1
            row[r] = max(row[r], v + row[r - w])
    return row[capacity]


def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """The SAME code with the range reversed. Each item may be used any number of times."""
    row = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for r in range(w, capacity + 1):              # <-- unbounded
            row[r] = max(row[r], v + row[r - w])
    return row[capacity]


def knapsack_with_items(weights, values, capacity) -> tuple[int, list[int]]:
    """The value AND the items. Needs the full table."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for r in range(capacity + 1):
            dp[i][r] = dp[i - 1][r]
            if w <= r:
                dp[i][r] = max(dp[i][r], v + dp[i - 1][r - w])
    chosen, r = [], capacity
    for i in range(n, 0, -1):
        if dp[i][r] != dp[i - 1][r]:
            chosen.append(i - 1)
            r -= weights[i - 1]
    return dp[n][capacity], chosen[::-1]


def can_reach(nums: list[int], target: int) -> bool:
    """Subset sum: the same table with booleans. reachable[0] = True is the base case."""
    reachable = [False] * (target + 1)
    reachable[0] = True
    for number in nums:
        for r in range(target, number - 1, -1):
            if reachable[r - number]:
                reachable[r] = True
    return reachable[target]


def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    return total % 2 == 0 and can_reach(nums, total // 2)


def greedy_by_value(weights, values, capacity) -> int:
    order = sorted(range(len(weights)), key=lambda i: -values[i])
    total, room = 0, capacity
    for i in order:
        if weights[i] <= room:
            total += values[i]
            room -= weights[i]
    return total


def greedy_by_ratio(weights, values, capacity) -> int:
    order = sorted(range(len(weights)), key=lambda i: -values[i] / weights[i])
    total, room = 0, capacity
    for i in order:
        if weights[i] <= room:
            total += values[i]
            room -= weights[i]
    return total


if __name__ == "__main__":
    # Bhagwan's cycle, scaled down.
    w = [2, 3, 4]
    v = [3, 4, 5]
    print("all three agree :", knapsack_memo(w, v, 5), knapsack_table(w, v, 5), knapsack_one_row(w, v, 5))
    print("with items      :", knapsack_with_items(w, v, 5))
    print()

    # greedy by value fails
    w1, v1 = [10, 5, 5], [60, 50, 50]
    print("by value   greedy:", greedy_by_value(w1, v1, 10), " correct:", knapsack_one_row(w1, v1, 10))

    # greedy by ratio fails
    w2, v2 = [6, 5, 5], [60, 40, 40]
    print("by ratio   greedy:", greedy_by_ratio(w2, v2, 10), " correct:", knapsack_one_row(w2, v2, 10))
    print()

    # the direction that changes the problem
    print("0/1        :", knapsack_one_row([2], [3], 6))
    print("unbounded  :", unbounded_knapsack([2], [3], 6))
    print()

    print("partition [1,5,11,5] :", can_partition([1, 5, 11, 5]))
    print("partition [1,2,3,5]  :", can_partition([1, 2, 3, 5]))
```

Running it:

```
all three agree : 7 7 7
with items      : (7, [0, 1])

by value   greedy: 60  correct: 100
by ratio   greedy: 60  correct: 80

0/1        : 3
unbounded  : 9

partition [1,5,11,5] : True
partition [1,2,3,5]  : False
```

Three things to look at. **Both greedy versions return 60 and both are wrong**, by different amounts and for
different reasons. **Keep those two inputs** — producing them on demand is what the question is testing.

**`0/1` gives 3 and `unbounded` gives 9** on the identical input of one item weighing 2 and worth 3, with a
capacity of 6. One item taken once against the same item taken three times. **The only difference in the code
is the direction of a `range`.**

And `[1,5,11,5]` partitions into `{1,5,5}` and `{11}`, both summing to 11 — while `[1,2,3,5]` totals 11, which
is odd, so it is rejected before any table is built.

---

## 6. What it costs

**The two-dimensional table:**

```
states           n x (W + 1)
work per state   O(1)   -- two options
                 --------------------
time             O(n x W)
space            O(n x W), or O(W) with one row
```

**Concretely:**

```
n = 100 items, W = 1,000        100,000 cells       instant
n = 1,000,     W = 10,000       10,000,000          ~1-2 s in Python
n = 100,       W = 1,000,000    100,000,000         too slow
n = 100,       W = 10^9         10^11               impossible
```

**And that last row is the whole complexity story.** `W = 10^9` takes ten characters to write, so the *input*
grew by ten characters and the table grew to a hundred billion cells.

**This is pseudo-polynomial:** polynomial in the **value** of `W`, exponential in the number of **digits** of
`W`. **That is why a DP solution does not contradict the problem being NP-hard**, and it is worth being able to
say in one sentence.

**Space:**

```
full table, n = 1,000, W = 10,000
  Python list of lists of ints        ~10,000,000 x 8 B + overhead  ~400 MB
one row
  10,001 ints                         ~80 KB
```

**Five thousand times less**, which is why the one-row version is what you actually write — and why
reconstruction, which needs the table, is a genuine cost rather than a free extra.

**The greedy alternatives, which are not even faster in any useful sense:**

```
greedy by value      O(n log n) to sort      WRONG
greedy by ratio      O(n log n) to sort      WRONG (right for FRACTIONAL knapsack)
DP                   O(n x W)                correct
```

```
n = 100, W = 1,000
  greedy   ~700 operations
  DP       100,000 operations
```

**So greedy is genuinely faster and gives the wrong answer**, which is the honest position — there is a real
trade here, unlike house robber where the wrong answer was not even cheaper. **If an approximate answer is
acceptable, greedy by ratio is within a factor of two of optimal**, and there is a well-known scheme that gets
within any chosen epsilon in polynomial time. **Naming that is a strong answer to "what if `W` is enormous?"**

**Subset sum and partition:**

```
partition, n items summing to S
  target        S / 2
  table         n x (S/2)
```

```
n = 200, values <= 100    ->  S <= 20,000, table 200 x 10,000 = 2,000,000    fine
n = 200, values <= 10^9   ->  S <= 2x10^11, table impossible
```

**Which is why LeetCode's partition problem caps the values** — and noticing that constraint is how you know
the intended solution is this DP.

**With a bitset**, subset sum gets dramatically faster in practice:

```python
reachable = 1                                  # bit r set = sum r is reachable
for number in nums:
    reachable |= reachable << number
return (reachable >> target) & 1
```

```
Python big integers do 64 bits per word
  n x S/64 word operations instead of n x S
  -> ~64x faster, and much less memory
```

**Three lines, and it is the fastest practical subset sum in Python.** Worth knowing, and worth explaining
rather than presenting as magic: shifting the whole set of reachable sums left by `number` is exactly "every
previously reachable sum, plus this number".

**Reconstruction:**

```
needs the full table        O(n x W) space
the backward walk           O(n) time
```

**So asking for the items costs the space optimisation**, and at `n = 1,000, W = 10,000` that is 400 MB rather
than 80 KB.

---

## 7. The traps

### The upward range in the one-row version

**The most dangerous line in dynamic programming**, because both versions are correct programs:

```python
for r in range(w, capacity + 1):          # upwards
    row[r] = max(row[r], v + row[r - w])
```

```
>>> one_item_upward([2], [3], 6)
9                                          # took the item three times
>>> one_item_downward([2], [3], 6)
3                                          # correct for 0/1
```

**No error, no warning**, and the answer is larger rather than smaller, so it does not look obviously wrong.
**Write the direction as a comment saying which problem it solves**, every time.

### One-dimensional state

```python
@lru_cache(maxsize=None)
def best(i):
    return max(values[i] + best(i + 1), best(i + 1))
```

```
>>> broken([(3,4),(4,5),(2,3)], capacity=5)
12                                         # the sum of everything; total weight is 9
```

Nothing tracks the capacity, so nothing prevents taking every item. **[Yesterday's test](../day-147-finding-the-state/README.md)
catches it in five seconds**: "at item five, what is the best I can do?" has no answer.

### Missing the "does not fit" guard

```python
take = values[i] + best(i + 1, remaining - weights[i])   # no check
```

`remaining` goes negative, the cache fills with nonsense states, and the answer is too large. **In the
one-row version the equivalent is a range that starts below the weight**, which raises `IndexError` or, worse,
wraps to a negative index and reads from the far end of the row.

### `reachable[0] = False` in subset sum

```python
reachable = [False] * (target + 1)
# reachable[0] = True     <- forgotten
```

```
>>> can_reach_broken([1, 5, 11, 5], 11)
False                                      # every cell stays False
```

**The empty subset sums to zero**, and that is the only cell not derived from the recurrence. Without it
nothing is ever reachable, and the failure is total rather than subtle — which is at least easy to spot.

### Not checking the odd total in partition

```python
return can_reach(nums, total // 2)         # total = 11, so target = 5
```

Integer division silently answers a different question. `[1,2,3,5]` sums to 11; asking "can I reach 5" gives
`True`, and the answer to the actual question is `False`. **One line, and it is free.**

### Mixing the two table conventions

```python
dp = [[0] * (capacity + 1) for _ in range(n)]     # n rows, "items i onwards"
...
w = weights[i - 1]                                # but indexing as "the first i items"
```

```
IndexError: list index out of range
```

or, worse, a silently wrong answer where one item is skipped. **Pick "the first `i` items" with `n+1` rows, or
"items `i` onwards" with `n+1` rows and a different base row — and say which in a comment.**

### Assuming greedy is a reasonable approximation without saying so

```python
return greedy_by_ratio(weights, values, capacity)
```

It is a reasonable approximation — within a factor of two — and it is not the answer to the question asked.
**If an approximation is acceptable, say that it is an approximation and give the bound.** Presenting it as the
solution is the failure.

### Forgetting that `W` can make the DP impossible

```python
knapsack(weights, values, capacity=10**9)
```

The code is correct and the table has a hundred billion cells per item. **Compute `n × W` before writing**, and
if it is above about ten million, say so and discuss the alternatives — meet-in-the-middle for small `n`, or an
approximation scheme.

---

## 8. In the interview

### How it gets asked

- *"Maximise the value you can carry within the weight limit."* — the direct version.
- *"Can this array be split into two subsets with equal sums?"* — LeetCode 416, the most common disguise.
- *"Can any subset sum to exactly this target?"*
- *"Assign plus or minus to each number to reach a target."* — LeetCode 494.
- *"Why doesn't greedy work?"* — the question the problem exists for.
- *"Now items can be used more than once."* — the direction change.

### The first ninety seconds

> "The state needs two dimensions and I want to say why before writing anything. If the state is just the item
> index, then 'at item five, what is the best I can do?' has no answer — it depends on how much capacity is
> left, and two different paths reach item five with different amounts. **So `dp[i][r]` is the maximum value
> from items `i` onwards with `r` capacity remaining.**
>
> **The recurrence is the choice at each item:** skip it, and the answer is `dp[i+1][r]`; or take it, and it is
> `value[i] + dp[i+1][r - weight[i]]` — **but only if it fits**, and that is the new dimension making a branch
> illegal rather than merely worse.
>
> **The thing I would raise before you ask is why greedy fails, because it fails twice.**
>
> **By value:** capacity ten, one item weighing ten worth sixty, and two weighing five worth fifty each.
> Greedy takes the sixty and blocks both; the answer is a hundred.
>
> **By value per weight**, which is the persuasive one: capacity ten, an item of six kilos worth sixty — ratio
> ten — and two of five kilos worth forty, ratio eight. Greedy takes the best ratio, has four kilos left, and
> nothing fits. Sixty against eighty.
>
> **And the reason the ratio rule is so tempting is that it is provably correct for the *fractional* knapsack**,
> where you can take part of an item. The moment items are indivisible the proof collapses, because the last
> item cannot be trimmed and the leftover space is wasted. **That sentence is the real answer to 'why not
> greedy'.**
>
> `O(n × W)` time and `O(n × W)` space, collapsing to `O(W)` with one row — and I would note that `n × W` is
> *pseudo*-polynomial: `W` is a number in the input, so a capacity of a billion makes the table a hundred
> billion cells while the input grew by ten characters. That is why this DP does not contradict the problem
> being NP-hard.
>
> Shall I write the one-row version? There is a subtlety in the iteration direction I would want to explain."

### The follow-ups

**"Explain the iteration direction."**

> "It is the most dangerous line in dynamic programming, because both directions are correct programs for
> different problems.
>
> With one row, `row[r] = max(row[r], v + row[r - w])`. The question is what `row[r - w]` holds when I read
> it.
>
> **Going downwards, from capacity to the weight**, `row[r - w]` is a smaller index that this round has not
> reached yet, so it still holds the value from before this item was considered. **The item is used at most
> once. That is 0/1.**
>
> **Going upwards**, `row[r - w]` is a smaller index that this round has *already updated*, so it may already
> include this item. **The item can be used again. That is the unbounded knapsack.**
>
> On a single item weighing two and worth three, with capacity six: downwards gives three, upwards gives nine.
> **Same three lines of code.**
>
> **And neither raises an error**, and the wrong one gives a *larger* answer, which does not look obviously
> wrong. So I write the direction as a comment naming which problem it solves, every time — and if I am ever
> unsure, I test it on one item that fits several times, which distinguishes them immediately."

**"Can this array be split into two equal halves?"**

> "That is subset sum, which is this problem with the value equal to the weight.
>
> **The reduction:** if the two halves are equal, each sums to `total / 2`. So the question is 'is there a
> subset summing to exactly `total / 2`', and if such a subset exists the rest is automatically the other
> half.
>
> **First, and free: if the total is odd, the answer is no.** No two integers sum to an odd number equally. One
> line, before any table.
>
> **Then the table is booleans rather than numbers:** `reachable[r]` is whether some subset sums to exactly
> `r`. `reachable[0] = True`, because the empty subset sums to zero — **that is the only cell not derived from
> the recurrence and it is the one people forget**; without it everything stays false.
>
> Then the same downward loop per number, and the answer is `reachable[total // 2]`.
>
> **Cost is `n × total/2`**, and this is where the constraints matter: LeetCode caps the values at a hundred
> with two hundred numbers, so the total is at most twenty thousand and the table is two million cells.
> **Noticing that cap is how you know this DP is the intended solution** — with values up to a billion it would
> be impossible.
>
> **And there is a much faster version worth knowing:** represent the set of reachable sums as the bits of a
> single big integer, and each number is `reachable |= reachable << number`. Python does sixty-four bits per
> word, so it is about sixty-four times faster and far less memory, in three lines."

**"What if the capacity is a billion?"**

> "Then this DP is not the answer, and I would say so rather than write it.
>
> **`n × W` with `W = 10^9` is a hundred billion cells per item.** The table is impossible even though the code
> is correct, and this is exactly the pseudo-polynomial point: `W` is a *number in the input*, so writing a
> billion took ten characters and the table grew by a factor of a million.
>
> **Three alternatives depending on what else is small.**
>
> **If `n` is small — up to about forty — meet in the middle.** Split the items into two halves, enumerate all
> `2^(n/2)` subsets of each, sort one side by weight, and for each subset of the other side binary-search the
> best complement that fits. That is `O(2^(n/2) × n)`, so about a million operations at `n = 40` instead of a
> trillion.
>
> **If the values are small rather than the weights, swap the dimensions.** Make the table indexed by *value*
> — `dp[i][v]` is the minimum weight needed to achieve value `v` — and the answer is the largest `v` whose
> minimum weight fits. **That is `O(n × total value)`**, which is the right choice whenever the values are
> bounded and the weights are not. It is a genuinely useful move and it is the one people do not think of.
>
> **And if an approximation is acceptable**, greedy by ratio is within a factor of two, and there is a standard
> scheme that scales the values down and gets within any chosen epsilon in polynomial time.
>
> **The honest answer is that the problem is NP-hard**, so with both `n` and `W` large there is no efficient
> exact algorithm, and the question becomes which approximation is acceptable."

**"Now each item can be taken any number of times."**

> "The unbounded knapsack, and it is the *upward* iteration — literally the same three lines with the range
> reversed.
>
> **Why that works:** going upwards, when I read `row[r - w]` it may already include this item from earlier in
> the same pass, so the item accumulates. That is precisely the behaviour I now want.
>
> **And the state actually gets simpler**, which is worth noticing. For 0/1 I needed to know which items were
> still available, which is why the item index is in the state. For unbounded, every item is always available,
> so **the state collapses to just the remaining capacity** — `dp[r]` is the best achievable with capacity `r`,
> and the item index is a loop variable rather than a dimension.
>
> **That is why coin change is a one-dimensional DP** while the 0/1 version is two-dimensional, and it is a
> nice illustration that the state is determined by what you need to remember, not by the number of loops.
>
> **Cost is the same, `O(n × W)`**, and the space is `O(W)` either way.
>
> **The bounded version — at most `k` copies of each item — is the awkward middle.** The naive approach adds a
> loop over the count, making it `O(n × W × k)`. The standard trick is **binary splitting**: replace an item
> with `k` copies by items representing 1, 2, 4, 8, … copies, since any count up to `k` is a sum of those
> powers. **That turns `k` copies into `log k` items and the problem back into plain 0/1**, at `O(n × W ×
> log k)`."

### The model answer

*"Given an array of positive integers, determine whether it can be partitioned into two subsets with equal
sums."*

> "Let me reduce it before designing anything, because the reduction is most of the work.
>
> **If the array splits into two equal halves, each half sums to `total / 2`.** So the question is: is there a
> subset summing to exactly `total / 2`? And if one exists, its complement is automatically the other half, so
> I only have to find one.
>
> **Free check first: if the total is odd, the answer is no.** No two integer sums are equal and odd. One line
> before any work, and it also protects me from the integer-division bug where `11 // 2` silently becomes a
> question about 5.
>
> **Then it is subset sum, which is the knapsack with value equal to weight.** `reachable[r]` = can some subset
> sum to exactly `r`. The recurrence is the same choice: for each number, either it is in the subset making `r`
> — so `r - number` must have been reachable before — or it is not.
>
> **Base case: `reachable[0] = True`**, the empty subset. **That is the only cell not produced by the
> recurrence**, and without it nothing is ever reachable.
>
> **One row, iterating the target downwards**, because each number may be used at most once. **Going upwards
> would let a number be reused** and would answer 'can I reach the target using these numbers with
> repetition', which is a different and easier question — and it would return `True` on inputs where the answer
> is `False`. I would write the direction as a comment.
>
> **Cost: `O(n × total/2)` time and `O(total/2)` space.** With the usual constraints — two hundred numbers,
> each at most a hundred — the total is at most twenty thousand, so the table is ten thousand booleans and the
> work is two million operations. **The fact that the values are capped is the signal that this is the intended
> solution**; without that cap the approach would not be viable, because it is pseudo-polynomial.
>
> **Two refinements I would offer.** An early exit: once `reachable[target]` becomes true, stop. And the bitset
> version — hold the reachable sums as the bits of one big integer and do `reachable |= reachable << number`
> per number, which is about sixty-four times faster in Python and three lines. **I would write the clear
> version first and mention the bitset**, because presenting the bitset cold looks like a memorised trick
> rather than a derivation.
>
> **And if the follow-up is 'which numbers are in each half'**, I need the full two-dimensional table rather
> than one row, and I walk it backwards: at each item, if the cell differs from the one above, that item was
> used. That costs `O(n × total/2)` space rather than `O(total/2)`, and I would ask whether the boolean answer
> is sufficient before giving it up."

---

## 9. Recall card

**`dp[i][r]` = the best value from items `i` onwards with `r` capacity left.** One index is not a question —
"at item five" has no answer without the room remaining. Take (if it fits) or skip.

**Greedy fails twice, and both counter-examples are worth memorising.** By value: `W=10`, `(10,60)`,
`(5,50)`, `(5,50)` — 60 against 100. By ratio: `W=10`, `(6,60)`, `(5,40)`, `(5,40)` — 60 against 80. **The
ratio rule is correct for the *fractional* knapsack; indivisibility is what breaks it.**

**One row, and the direction is the problem.** `for r in range(W, w-1, -1)` is 0/1; `range(w, W+1)` is
**unbounded**. Same three lines, no error, and the wrong one gives a *larger* answer.

**`O(n × W)` is pseudo-polynomial** — polynomial in the *value* of `W`, not its digit count — which is why a DP
exists and the problem is still NP-hard. Compute `n × W` before writing; above ~10⁷, use meet-in-the-middle
(small `n`), swap the dimension to index by **value** (small values), or approximate.

**The family is the same table:** subset sum (booleans, and **`reachable[0] = True`** is the forgotten base
case), equal partition (target `total/2`, and **reject an odd total first**), target sum, minimum difference.
Reconstruction needs the full table, so it is mutually exclusive with the one-row form.
