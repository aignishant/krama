---
day: 149
track: dsa
title: "Subset sum and partition problems"
phase: "Dynamic programming"
status: written
---

# Subset sum and partition problems

## 1. What this is, and why they ask it

Subset sum asks one question: **given a list of numbers, can you pick some of them that add up to exactly
`T`?** Not the biggest total, not the best value — just yes or no.

It is knapsack with the value column deleted. Yesterday's table held the best value you could reach; today's
holds a single boolean, `True` if the total is reachable and `False` if it is not.

They ask it because **it is the disguise family**. Almost nobody asks "solve subset sum". They ask *can this
array be split into two equal halves*, or *what is the smallest difference between two groups*, or *how many
ways can you assign plus and minus signs to reach a target* — and every one of those is subset sum after two
lines of algebra. **The skill being tested is recognising it**, and a candidate who does the algebra out loud
in thirty seconds is demonstrating something a candidate who starts writing a recursive brute force is not.

The other reason is that **it is the cheapest place to talk about NP-hardness honestly**. Subset sum is one of
the classic NP-complete problems, and you are about to solve it with a table in `O(n × T)`. Being able to say
why those two facts do not contradict each other is a real conversation, and it is short.

By the end of this lesson you can write the boolean table, collapse it to one row, recognise the four
disguises, do the algebra for each, and say exactly what pseudo-polynomial means.

---

## 2. The story

The two brothers had spent eleven years not talking about the shop and then their father died and they had to.

The shop was one room, and the stock in it was the whole of what he had left. Neither of them wanted to sell
it. Both of them wanted half.

So they did what their aunt suggested, which was to make two piles.

Everything came off the shelves onto the floor. The steel almirah. The two ceiling fans still in their boxes.
The mixer. The four rolls of cloth. The scooter, which did not come off the shelves but which counted. The
sewing machine their mother had used. Twenty-two things in all, and beside each one a number, because the man
from the next lane who dealt in second-hand goods had come and looked at everything and written down what he
would pay.

The numbers added to four lakh sixteen thousand.

**Half was two lakh eight.**

And here is where the afternoon went. **You cannot cut a scooter in half.** The scooter was seventy-two
thousand. The almirah was thirty-one. The fans were nine each. Every single thing was a whole thing, and the
question was not what half was — they both knew what half was — but **whether any collection of these
particular objects came to exactly that number.**

Vinod tried first. He took the scooter, then the almirah, then the mixer, and he was at a lakh and thirty-one,
and he added the cloth, and he was at one lakh eighty-three, and the smallest thing left was nine thousand,
which took him to one lakh ninety-two, and the next smallest was twenty-two, which took him past.

So he put the mixer back and started again.

**By six o'clock they had been at it for three hours and neither of them had a system.** They were guessing,
and each guess was one arrangement out of a number of arrangements neither of them could have said.

The aunt, who had watched all of it, made the only useful observation of the day. **"You keep asking whether
you can get to two lakh eight. Ask something smaller first. Can you get to a thousand? Can you get to two?"**

Vinod said that was a stupid question, because obviously they could not, and then he sat down, because he had
understood what she meant.

---

## 3. The idea in plain English

The aunt has just described the DP table.

**The question "can I hit exactly `T`?" is hard to attack directly, and easy to attack if you already know
the answer for every smaller total.**

**So build up.** Ask, for every total from `0` to `T`, whether that total is reachable — and answer them in
order, smallest first, using only items you have looked at so far.

**The state, said as a full sentence, is: `dp[i][t]` is `True` if some subset of the first `i` numbers adds up
to exactly `t`.**

That sentence is the whole lesson. Everything else is mechanics.

**The recurrence has two ways to reach `t` using the first `i` numbers**, exactly as in knapsack:

- **Skip number `i`.** Then `t` must already have been reachable using the first `i - 1`. That is
  `dp[i-1][t]`.
- **Take number `i`.** Then before taking it you must have been at `t - nums[i]`, using the first `i - 1`.
  That is `dp[i-1][t - nums[i]]`, and it only makes sense when `nums[i] <= t`.

```
dp[i][t] = dp[i-1][t]  OR  dp[i-1][t - nums[i]]
```

**One `OR` instead of yesterday's `max`.** That is the only difference between subset sum and knapsack. Same
table, same two branches, same guard — a boolean where a value used to be.

**The base cases.** `dp[0][0] = True`: the empty subset adds to zero, always, and this is the case people
forget. `dp[0][t] = False` for every `t > 0`: with no numbers you cannot reach a positive total.

**And the same one-row collapse as yesterday**, for the same reason: row `i` reads only row `i - 1`, so keep
one row and update it in place, **backwards**.

```python
for number in nums:
    for t in range(target, number - 1, -1):
        reachable[t] = reachable[t] or reachable[t - number]
```

**Backwards, because `reachable[t - number]` must still hold the previous row's answer** — the answer from
before this number was available. Forwards would let the same number be used twice, which is a different
problem, and tomorrow's.

**Now the four disguises**, which is the reason this topic is asked.

**Disguise one: equal partition.** *Can the array be split into two subsets with equal sums?* If the total is
`S`, each half must be `S / 2`, so it is subset sum with `T = S / 2`. **And if `S` is odd, the answer is `False`
immediately** — you cannot split an odd number into two equal integers. That check costs one line and it is
the first thing to say out loud.

**Disguise two: minimum difference.** *Split into two groups so the difference between their sums is as small
as possible.* If one group sums to `a`, the other sums to `S - a`, so the difference is `|S - 2a|`. To make
that small, **make `a` as close to `S / 2` as possible without exceeding it.** So: run subset sum up to `S / 2`,
find the largest reachable `a`, and the answer is `S - 2a`. **Same table, read differently** — you scan the
finished row instead of reading one cell.

**Disguise three: target sum.** *Assign `+` or `-` to every number to reach `target`.* Let `P` be the numbers
you make positive and `N` the ones you make negative. Then:

```
P - N = target
P + N = total          (every number is in one group or the other)
```

Add them: `2P = target + total`, so **`P = (target + total) / 2`**. Count the subsets summing to `P`.

**Two conditions make it zero immediately:** if `target + total` is odd, or if `|target| > total`. Say both.

**And this one counts rather than decides**, so the table holds an integer count and the `OR` becomes `+`:

```
ways[t] += ways[t - number]
```

**Disguise four: last stone weight II.** *Repeatedly smash two stones together; the difference survives.* Each
smash is assigning a sign, so the final stone is `|sum of one group − sum of the other|`, minimised. **That is
disguise two.** It is the best-hidden of the four and it is worth doing immediately after disguise three so
the shape is obvious.

**Finally, the honest complexity conversation.** The table is `n × T`, so the running time is `O(n × T)`, which
looks polynomial. **It is not.** `T` is a *number* in the input, and a number of `b` bits can be as large as
`2^b`. So the running time is exponential in the *size* of the input, which is what "polynomial" is measured
against. **That is what pseudo-polynomial means**, and it is why subset sum can be NP-complete and still have
this table.

**Practically:** `T = 10,000` is instant, `T = 10^9` is impossible, and **the size of the numbers decides
whether this approach exists at all.** Check it before you write anything.

---

## 4. The picture

The table filling in, for `nums = [3, 34, 4, 12, 5, 2]` and `target = 9`:

```
             t = 0  1  2  3  4  5  6  7  8  9
  {}            T   F  F  F  F  F  F  F  F  F     empty subset makes 0
  +3            T   F  F  T  F  F  F  F  F  F     3 now reachable
  +34           T   F  F  T  F  F  F  F  F  F     34 > 9, changes nothing
  +4            T   F  F  T  T  F  F  T  F  F     4, and 3+4=7
  +12           T   F  F  T  T  F  F  T  F  F     12 > 9, nothing
  +5            T   F  F  T  T  T  F  T  T  T     5, 3+5=8, 4+5=9  <-- found
  +2            T   F  T  T  T  T  T  T  T  T

  Notice: each row copies the row above, then turns on t and t+number
  for every t that was already True. Nothing ever turns OFF.
```

The one-row version, and why it runs backwards:

```
  adding number = 5 to the row [T F F T T F F T F F]
                                0 1 2 3 4 5 6 7 8 9

  BACKWARDS  t = 9, 8, 7, ... 5
    t=9: reachable[9] |= reachable[4]  -> reachable[4] is T (from before 5) -> T
    t=8: reachable[8] |= reachable[3]  -> T
    t=5: reachable[5] |= reachable[0]  -> T
    every read is from a cell 5 to the LEFT, which this pass has not touched yet.
    -> each number used at most once. 0/1.

  FORWARDS   t = 5, 6, 7, ... 9
    t=5:  reachable[5] |= reachable[0]  -> T
    t=10: reachable[10] |= reachable[5] -> reachable[5] was just set by THIS pass
    -> 5 used twice. That is the unbounded problem, not this one.
```

The two brothers' problem, drawn as the recurrence:

```
  can I make 208000 from {scooter 72000, almirah 31000, ...} ?

                  can I make 208000?
                 /                  \
      skip scooter                take scooter
     can I make 208000            can I make 136000
     from the rest?               from the rest?
       /        \                   /        \
    skip       take              skip       take
   almirah    almirah           almirah    almirah
   208000     177000            136000     105000

  The tree is 2^22 leaves. The table is 22 x 208001 cells.
  Both explore the same space; the table just never asks the same
  question twice.
```

Minimum difference, read off the finished row:

```
  nums = [1, 6, 11, 5], total = 23, half = 11

  finished reachable row up to 11:
    t:  0  1  2  3  4  5  6  7  8  9 10 11
        T  T  F  F  F  T  T  T  F  F  F  T
                                          ^
  largest reachable a <= 11  is  a = 11
  difference = total - 2a = 23 - 22 = 1

  Same table. You scan it instead of indexing it.
```

---

## 5. The code, built step by step

### The plain table, straight from the sentence

```python
def subset_sum_table(nums: list[int], target: int) -> bool:
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True                       # empty subset makes 0
    return dp[n][target]                      # (loops next)
```

**`dp[i][0] = True` for every `i`** is the base case, and it is the one people miss. Zero is always reachable,
whatever numbers you have, because you can take none of them.

Now the two branches:

```python
    for i in range(1, n + 1):
        number = nums[i - 1]
        for t in range(1, target + 1):
            dp[i][t] = dp[i - 1][t]           # skip
            if number <= t:
                dp[i][t] = dp[i][t] or dp[i - 1][t - number]
```

**`number <= t` is the guard**, and without it `t - number` is negative and Python silently indexes from the
end of the row. No error, wrong answer — the same failure as yesterday's missing capacity check.

### The one-row version, which is what you write in an interview

```python
def subset_sum(nums: list[int], target: int) -> bool:
    if target < 0:
        return False
    reachable = [False] * (target + 1)
    reachable[0] = True
    for number in nums:
        for t in range(target, number - 1, -1):
            if reachable[t - number]:
                reachable[t] = True
    return reachable[target]
```

**Three lines shorter than the table and the same answer.** The `range(target, number - 1, -1)` stops at
`number` rather than `0`, because below `number` nothing can change — and that also removes the need for the
guard, since `t >= number` is now guaranteed by the range itself.

**Say the direction out loud while you write it.** "Backwards, so each number is used at most once."

### The early exit that matters

```python
    for number in nums:
        for t in range(target, number - 1, -1):
            if reachable[t - number]:
                reachable[t] = True
        if reachable[target]:
            return True                       # stop as soon as it is found
```

**Worth adding when the target is reachable early**, and it costs one line. It does not change the worst case.

### Equal partition, which is two lines on top

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2 == 1:
        return False                          # odd totals never split evenly
    return subset_sum(nums, total // 2)
```

**The odd check is the whole trick**, and it is the first sentence of the answer.

### Minimum difference, which scans instead of indexing

```python
def minimum_difference(nums: list[int]) -> int:
    total = sum(nums)
    half = total // 2
    reachable = [False] * (half + 1)
    reachable[0] = True
    for number in nums:
        for t in range(half, number - 1, -1):
            if reachable[t - number]:
                reachable[t] = True
    for a in range(half, -1, -1):             # largest reachable a <= half
        if reachable[a]:
            return total - 2 * a
    return total
```

**The scan runs downwards** so the first `True` it meets is the largest reachable subset sum at or below half,
which is the closest you can get to an even split from below.

### Target sum, which counts instead of deciding

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    if abs(target) > total or (target + total) % 2 == 1:
        return 0                              # unreachable, or not an integer
    positive = (target + total) // 2
    ways = [0] * (positive + 1)
    ways[0] = 1                               # one way to make 0: take nothing
    for number in nums:
        for t in range(positive, number - 1, -1):
            ways[t] += ways[t - number]
    return ways[positive]
```

**`ways[0] = 1`, not `True`** — there is exactly one empty subset, and that `1` is what every count is
ultimately built from. **And `+=` where the boolean version had `or`.** Everything else is identical.

**The guard `abs(target) > total` matters**, because without it `positive` can be negative and `[0] * (negative)`
gives an empty list rather than an error.

### The bitset version, which is worth knowing

```python
def subset_sum_bitset(nums: list[int], target: int) -> bool:
    reachable = 1                             # bit 0 set: total 0 is reachable
    for number in nums:
        reachable |= reachable << number
    return (reachable >> target) & 1 == 1
```

**Six lines, and it is the same algorithm.** Each bit position is a total; shifting left by `number` is
"every reachable total, plus this number"; `|=` merges that with what was already reachable.

**Python integers are arbitrary-precision, so this works for any target**, and the shift moves 64 bits per
machine word rather than one boolean per loop iteration — **roughly a 30–60× speedup** on large inputs. Mention
it as an optimisation; write the loop version first.

### The complete solution

```python
"""Subset sum and its four disguises."""


def subset_sum(nums: list[int], target: int) -> bool:
    """True if some subset of nums adds up to exactly target."""
    if target < 0:
        return False
    reachable = [False] * (target + 1)
    reachable[0] = True                       # empty subset makes 0
    for number in nums:
        # backwards: each number is used at most once
        for t in range(target, number - 1, -1):
            if reachable[t - number]:
                reachable[t] = True
        if reachable[target]:
            return True
    return reachable[target]


def subset_sum_with_items(nums: list[int], target: int) -> list[int] | None:
    """The subset itself, or None. Keeps every row, so O(n x target) space."""
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True
    for i in range(1, n + 1):
        number = nums[i - 1]
        for t in range(1, target + 1):
            dp[i][t] = dp[i - 1][t]
            if number <= t and dp[i - 1][t - number]:
                dp[i][t] = True

    if not dp[n][target]:
        return None

    chosen, t = [], target
    for i in range(n, 0, -1):
        if not dp[i - 1][t]:                  # could not have skipped it
            chosen.append(nums[i - 1])
            t -= nums[i - 1]
    return chosen[::-1]


def can_partition(nums: list[int]) -> bool:
    """Disguise 1: split into two subsets with equal sums."""
    total = sum(nums)
    if total % 2 == 1:
        return False
    return subset_sum(nums, total // 2)


def minimum_difference(nums: list[int]) -> int:
    """Disguise 2: smallest possible difference between two groups."""
    total = sum(nums)
    half = total // 2
    reachable = [False] * (half + 1)
    reachable[0] = True
    for number in nums:
        for t in range(half, number - 1, -1):
            if reachable[t - number]:
                reachable[t] = True
    for a in range(half, -1, -1):
        if reachable[a]:
            return total - 2 * a
    return total


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """Disguise 3: count the +/- assignments reaching target."""
    total = sum(nums)
    if abs(target) > total or (target + total) % 2 == 1:
        return 0
    positive = (target + total) // 2
    ways = [0] * (positive + 1)
    ways[0] = 1                               # exactly one empty subset
    for number in nums:
        for t in range(positive, number - 1, -1):
            ways[t] += ways[t - number]
    return ways[positive]


def last_stone_weight_ii(stones: list[int]) -> int:
    """Disguise 4: it is minimum_difference, wearing a hat."""
    return minimum_difference(stones)


def subset_sum_bitset(nums: list[int], target: int) -> bool:
    """The same algorithm, 30-60x faster, using Python's big integers."""
    reachable = 1
    for number in nums:
        reachable |= reachable << number
    return (reachable >> target) & 1 == 1


if __name__ == "__main__":
    nums = [3, 34, 4, 12, 5, 2]
    print("reach 9      :", subset_sum(nums, 9))
    print("reach 30     :", subset_sum(nums, 30))
    print("which items  :", subset_sum_with_items(nums, 9))
    print("bitset agrees:", subset_sum_bitset(nums, 9), subset_sum_bitset(nums, 30))

    print("partition [1,5,11,5]:", can_partition([1, 5, 11, 5]))
    print("partition [1,2,3,5] :", can_partition([1, 2, 3, 5]))

    print("min diff [1,6,11,5] :", minimum_difference([1, 6, 11, 5]))
    print("stones [2,7,4,1,8,1]:", last_stone_weight_ii([2, 7, 4, 1, 8, 1]))

    print("target sum [1,1,1,1,1] -> 3:", find_target_sum_ways([1, 1, 1, 1, 1], 3))
    print("target sum [1] -> 2       :", find_target_sum_ways([1], 2))
```

Run it and you get:

```
reach 9      : True
reach 30     : False
which items  : [4, 5]
bitset agrees: True False
partition [1,5,11,5]: True
partition [1,2,3,5] : False
min diff [1,6,11,5] : 1
stones [2,7,4,1,8,1]: 1
target sum [1,1,1,1,1] -> 3: 5
target sum [1] -> 2       : 0
```

**`which items` returning `[4, 5]` is the walk-back working.** Those two numbers do add to 9, and note it did
not find `[3, 4, 2]`, which also adds to 9 — the walk-back returns *a* valid subset, not all of them, and
which one depends on the order the table was filled.

**`reach 30` is `False`**, which is worth checking by hand: the numbers total 60, and no combination of
`[3, 34, 4, 12, 5, 2]` lands on 30 exactly. **And `target sum [1] -> 2` gives 0**, caught by the
`abs(target) > total` guard rather than by a crash.

---

## 6. What it costs

**Time.** Two nested loops.

```
outer loop: once per number                     n iterations
inner loop: once per total from target down     target iterations

n numbers x target totals = n x target cells
each cell: one comparison and one assignment    O(1)

TOTAL: O(n x target)
```

**Concretely, for `n = 200` numbers and `target = 10,000`:**

```
200 x 10,000 = 2,000,000 cells
Python does roughly 10 million simple loop steps per second
-> about 0.2-0.5 seconds. Fine.
```

**And for `target = 10^9`:**

```
200 x 1,000,000,000 = 200,000,000,000 cells
-> about six thousand years, and the list allocation fails first:

MemoryError
```

**The size of the target decides whether this algorithm exists.** Check it before writing.

**Space.**

```
full table     (n + 1) x (target + 1) booleans
               201 x 10,001 = 2,010,201 booleans
               Python bools in a list of lists: ~8 bytes per pointer
               -> about 16 MB

one row        target + 1 booleans
               10,001 -> about 80 KB

               200x less, same answer.
```

**Use the one row unless you need to reconstruct the subset**, which needs every row.

**The bitset version, measured:**

```
n = 200, values up to 1,000, target = 100,000

loop version    200 x 100,000 = 20,000,000 Python-level steps   ~4 s
bitset version  200 shifts of a 100,000-bit integer
                = 200 x (100,000 / 64) ~ 312,500 word operations  ~0.05 s

roughly 80x faster, and the same answer.
```

**Why it is faster is worth one sentence:** the loop moves one boolean per Python instruction; the shift moves
sixty-four bits per machine instruction, in C.

**And the pseudo-polynomial point, arithmetically:**

```
input size (bits) = n numbers x bits per number
                  = 200 x 30 bits  = 6,000 bits

running time      = n x target
                  = 200 x 2^30     = 200 billion

The input is 6,000 bits. The running time is 2^30.
Exponential in the SIZE of the input, polynomial in its VALUE.
That is pseudo-polynomial, and it is why NP-completeness and this
table are both true at once.
```

---

## 7. The traps

**The forward loop, which solves a different problem in silence.** Write `range(number, target + 1)` instead of
`range(target, number - 1, -1)` and each number can be reused any number of times.

```python
>>> reachable = [False] * 11
>>> reachable[0] = True
>>> for t in range(3, 11):          # forwards, number = 3
...     if reachable[t - 3]:
...         reachable[t] = True
>>> [i for i, r in enumerate(reachable) if r]
[0, 3, 6, 9]
```

**One number, `3`, and it has reached 6 and 9.** No error, no warning, and `subset_sum([3], 9)` now returns
`True` when it should return `False`. **This is the single most common bug in the topic**, and the only
defence is to say the direction out loud as you write it.

**Forgetting `reachable[0] = True`.**

```python
>>> reachable = [False] * 11        # no base case
>>> for number in [3, 4, 5]:
...     for t in range(10, number - 1, -1):
...         if reachable[t - number]:
...             reachable[t] = True
>>> reachable[9]
False
```

**Everything is `False` forever**, because nothing was ever `True` to build from. The table fills correctly and
answers `False` to every question. **It looks like "no subset exists" rather than like a bug.**

**Negative targets, and Python's helpful indexing.** Without the guard:

```python
>>> reachable = [False, True, False, True]
>>> t, number = 1, 3
>>> reachable[t - number]           # reachable[-2]
False
```

`reachable[-2]` is a perfectly legal read from the end of the list. **No `IndexError`** — that is what makes it
dangerous. The `range(target, number - 1, -1)` form removes the risk structurally, which is why it is the
version to write.

**Forgetting the odd-total check on partition.** It is not a correctness bug — `subset_sum(nums, total // 2)`
with an odd total will simply fail to find anything — but it is a **wasted `O(n × total)` pass** on an input
you could have rejected in one comparison, and the interviewer is listening for it.

**Floats.**

```python
>>> reachable = [False] * 11
>>> reachable[0] = True
>>> for t in range(10, int(2.5) - 1, -1):
...     reachable[t - 2.5]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: list indices must be integers or slices, not float
```

**The table is indexed by the total, so the totals must be integers.** If the input has decimals, multiply
everything by 100 first and say so.

**Target sum without the parity guard.**

```python
>>> nums, target = [1, 2, 3], 1
>>> total = 6
>>> positive = (target + total) // 2        # (1 + 6) // 2 = 3
>>> # but 1 + 6 = 7 is odd -> no integer split exists
```

`7 // 2` is `3`, silently, and the function returns a count for the wrong sub-problem. **Check
`(target + total) % 2 == 1` first**, and say why: `P` must be an integer, and it cannot be if `target + total`
is odd.

**Building the table when the target is enormous.**

```python
>>> reachable = [False] * (10**9 + 1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**Eight gigabytes for the list of pointers alone.** The moment you see `1 <= nums[i] <= 10^9` in the
constraints, the table is off the menu and you say so before writing.

**Reconstructing from the one-row version.** You cannot. The row has been overwritten `n` times and holds no
history at all — there is no walk-back to do. **If they ask which items, you need the full table**, and saying
"the space collapse costs me the reconstruction" is the right way to raise it.

---

## 8. In the interview

### How it gets asked

- *"Can this array be split into two subsets with equal sums?"* — LeetCode 416, the most common form.
- *"Split the array into two groups so the difference of their sums is minimised."*
- *"Assign a plus or minus to each number so the total is `target`. How many ways?"* — LeetCode 494.
- *"You have stones; smash two together and the difference survives. What is the smallest possible last
  stone?"* — LeetCode 1049, the best disguise.
- *"Subset sum is NP-complete. You just solved it in `O(n × T)`. Explain."*

### The first ninety seconds

> "This is subset sum. Let me say the reduction first, because the algorithm is the same for all of these.
>
> **If the whole array sums to `S`, then two equal halves each sum to `S / 2`** — so the question 'can it be
> split evenly' is exactly 'is there a subset adding up to `S / 2`'.
>
> **And if `S` is odd, the answer is no, immediately**, because you cannot split an odd integer into two equal
> integers. That is one comparison and it saves the whole computation.
>
> **The state is: `dp[t]` is true if some subset of the numbers I have seen so far adds up to exactly `t`.**
> One boolean per total from zero to `S / 2`.
>
> **The base case is `dp[0] = True`** — the empty subset makes zero, always, and that is the one everything
> else is built from.
>
> **For each number, I ask: which totals become reachable now?** A total `t` is reachable if it was already
> reachable without this number, or if `t - number` was reachable before this number. So it is
> `dp[t] = dp[t] or dp[t - number]` — **the same two branches as knapsack, with an OR where the `max` was.**
>
> **And I run the inner loop backwards, from `S / 2` down to the number.** That matters: `dp[t - number]` has to
> still hold the answer from *before* this number was available. If I ran forwards I would read a cell this
> same pass had already updated, and the number would be usable twice — which is the unbounded problem, not
> this one. **No error either way, just a wrong answer**, so I state the direction as I write it.
>
> **Cost is `O(n × S/2)` time and `O(S)` space**, one row. For a couple of hundred numbers summing to twenty
> thousand that is two million operations — instant.
>
> **One thing I would check first:** how large can the numbers be? If they go up to a billion the table is
> eight gigabytes and this approach does not exist."

### The follow-ups

**"Why does the inner loop run backwards?"**

> "Because of what the cell I am reading has to mean.
>
> The one-row version is a squashed two-row version. `dp[t] = dp[t] or dp[t - number]` — and both of those
> reads are supposed to come from the **previous** row, the state of things before this number was available.
>
> **Running backwards, from the target down to the number, every read is from a cell to the left**, and this
> pass has not touched anything to the left yet. So `dp[t - number]` still holds the previous row's value.
> Correct.
>
> **Running forwards, `dp[t - number]` may already have been updated by this same pass** — meaning it already
> counts this number once. Adding the number again uses it twice.
>
> Concretely: one number, `3`, target 9, forwards. `dp[3]` becomes true from `dp[0]`. Then `dp[6]` becomes true
> from `dp[3]`, which I just set. Then `dp[9]` from `dp[6]`. **I have made 9 out of a single 3.**
>
> **And that is not a bug in general — it is the correct algorithm for the unbounded problem**, where items can
> be reused. Two loop directions, two different problems, both correct programs, no error to distinguish them.
> Which is why I say the direction out loud when I write it."

**"Now count the number of ways instead of just yes or no."**

> "Almost the same code. The table holds an integer count instead of a boolean, the `or` becomes `+=`, and the
> base case becomes `ways[0] = 1` instead of `True`.
>
> **`ways[0] = 1` is the meaningful change:** there is exactly one way to make zero, which is to take nothing,
> and every other count is built by adding that one up.
>
> ```
> ways[t] += ways[t - number]
> ```
>
> **Same backwards loop, same reason.**
>
> The version they usually ask is Target Sum: assign a plus or minus to every number to reach `target`. That
> needs two lines of algebra first. **Call `P` the numbers I make positive and `N` the ones I make negative.
> Then `P - N = target`, and `P + N = total`, because every number is in exactly one group.** Add those:
> `2P = target + total`, so `P = (target + total) / 2`.
>
> **So it is: count the subsets summing to `P`.** One subset-sum-counting pass.
>
> **And two things make it zero straight away** — if `|target| > total` it is unreachable, and if
> `target + total` is odd then `P` is not an integer, so no assignment exists. **Both need stating, because
> without the parity check the integer division silently rounds and I answer a different question.**"

**"Subset sum is NP-complete. You just solved it in `O(n × T)`. Which is it?"**

> "Both, and they do not conflict — the resolution is what 'polynomial' is measured against.
>
> **Complexity is measured against the number of bits in the input, not the numerical values in it.**
>
> The input here is `n` numbers. If each is up to `T`, writing them down takes about `n × log₂(T)` bits. So the
> input size is `n log T`.
>
> **My running time is `n × T`, which is `n × 2^(log T)` — exponential in `log T`, and `log T` is the input
> size.** So `O(n × T)` is exponential in the size of the input, even though it looks polynomial. **That is
> what pseudo-polynomial means.**
>
> The practical version is more useful: **the algorithm is fast when the numbers are small and impossible when
> they are large.** Two hundred numbers summing to ten thousand is two million cells, instant. Two hundred
> numbers up to a billion is two hundred billion cells and eight gigabytes of memory before the first
> comparison.
>
> **So the constraint I look for is the bound on the values, not on `n`** — which is the reverse of most
> problems, and it is why I ask about it before writing anything.
>
> **And if the numbers are large there is no exact polynomial algorithm** — that is what NP-completeness is
> telling me. What exists is approximation: scale the values down, accept an answer within a fixed percentage
> of optimal. Worth naming as the fallback."

### The model answer

*"Given a list of stones, you repeatedly pick two and smash them; if they are equal both are destroyed, and if
not the difference remains. Return the smallest possible weight of the last stone."*

> "Let me work out what the smashing actually does, because the algorithm falls out of that and not out of
> simulating it.
>
> **Every smash takes two stones `a` and `b` and leaves `|a - b|`.** That is the same as writing `a - b`, or
> `b - a` — I am choosing a sign. And if I keep smashing, the final stone is some expression where every
> original stone appears exactly once with either a plus or a minus in front of it.
>
> **So: assign a `+` or a `-` to every stone, and minimise the absolute value of the total.**
>
> **Which means splitting the stones into two groups and minimising the difference between their sums.** The
> plus group and the minus group.
>
> **Now the algebra.** If the whole set sums to `S` and one group sums to `a`, the other sums to `S - a`, and
> the difference is `|S - 2a|`. To make that as small as possible I want `a` as close to `S / 2` as I can get.
>
> **And 'which totals near `S / 2` are actually achievable' is subset sum.**
>
> So: build the reachable table up to `S / 2`. `dp[0] = True` for the empty subset, then for each stone, going
> backwards from `S / 2` down to the stone's weight, mark `t` reachable if `t - stone` was. Then scan the
> finished row downwards from `S / 2` and take the first reachable `a`. **The answer is `S - 2a`.**
>
> **Scanning downwards matters** — the first `True` I meet going down is the largest achievable total at or
> below half, which is the closest split from below. And I only need to search up to `S / 2` because the two
> groups are symmetric: every split below half has a mirror above it.
>
> **Cost: `O(n × S/2)` time, `O(S)` space.** With a hundred stones of at most a hundred each, `S` is at most
> ten thousand, so five thousand columns and a hundred rows — half a million operations. Instant.
>
> **The backwards loop is the part I would say out loud while writing it**, because each stone can be used
> once. Forwards would let a stone appear in the group twice, which silently solves a different problem.
>
> **Two edge cases:** one stone, where the answer is that stone; and an even split existing, where `a = S / 2`
> and the answer is zero.
>
> **And the thing I would check before writing anything** is the bound on the stone weights. This works because
> `S` is at most ten thousand. If the weights could be a billion, the table is eight gigabytes and I would need
> a different approach — which is worth saying, because it is the constraint that decides whether this
> algorithm exists at all."

---

## 9. Recall card

**Subset sum is knapsack with the value column deleted:** `dp[t]` is `True` if some subset of the numbers seen
so far adds to exactly `t`. Same two branches, **`or` where the `max` was**, base case **`dp[0] = True`** — the
empty subset makes zero.

**One row, inner loop backwards**, `range(target, number - 1, -1)`, so `dp[t - number]` still holds the value
from before this number existed. **Forwards solves the unbounded problem instead, with no error either way** —
say the direction out loud as you write it.

**Four disguises, all the same table.** Equal partition = subset sum to `S/2`, **odd `S` fails immediately**.
Minimum difference = scan the finished row downwards for the largest reachable `a ≤ S/2`, answer `S - 2a`.
Target sum = `P = (target + total)/2` by algebra, count instead of decide (`ways[0] = 1`, `+=`), zero if
`target + total` is odd or `|target| > total`. Last Stone Weight II = minimum difference.

**`O(n × T)` time, `O(T)` space** — 200 numbers to target 10,000 is 2M cells and instant; target 10⁹ is a
`MemoryError` before the first comparison. **The bound on the values, not on `n`, decides whether this
approach exists.**

**Pseudo-polynomial:** input size is `n log T` bits, running time is `n × T = n × 2^(log T)` — exponential in
the input size, which is how NP-completeness and this table are both true. **Bitset trick:**
`reachable |= reachable << number`, roughly 80× faster for free.
