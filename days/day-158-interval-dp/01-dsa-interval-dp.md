---
day: 158
track: dsa
title: "Interval DP"
phase: "Dynamic programming"
status: written
---

# Interval DP

## 1. What this is, and why they ask it

**Interval DP is for problems where the state is a range — `dp[i][j]` describes the piece of the input from
`i` to `j` — and the answer depends on how you split that range.**

You met one already: the palindrome table on [day 155](../day-155-string-dp/README.md), where `dp[i][j]` said
whether a substring was a palindrome. **Today the range is not just examined but divided**, and the recurrence
tries every possible dividing point.

They ask it because **it is the hardest common DP shape and it has a recognisable signature.** Three nested
loops — length, start, split point — and an inner `min` or `max` over the split. Once you have written it
twice, you recognise it from the problem statement: **"combine adjacent things, and the cost of combining
depends on what you combined before."**

The other reason is that **it is where the fill order finally has a reason you must state.** `dp[i][j]` reads
`dp[i][k]` and `dp[k+1][j]` — **both strictly shorter ranges** — so you fill by increasing length, and getting it
wrong here produces an answer that is too cheap rather than too expensive, which is the harder direction to
notice.

And there is a third thing that makes these problems genuinely hard: **the trick of asking the question
backwards.** In burst balloons, thinking about which balloon to pop *first* leads nowhere, because popping
changes the neighbours. **Thinking about which one to pop *last* works immediately**, because the last one in
a range has fixed neighbours — the boundaries. That inversion is the whole difficulty of the problem, and it
is worth having met once.

By the end of this lesson you can recognise the shape, write the three-loop skeleton, do matrix chain
multiplication and burst balloons, explain the last-not-first inversion, and say what the cost is.

---

## 2. The story

The wedding was in four weeks and the argument at the table was about the order.

**Not the order of the ceremony. The order the tents came down in.**

Because Devrath had done seventy or eighty of these and he had learned a thing that none of the families ever
believed until it happened, which was that **taking the tents down was harder than putting them up, and the
sequence mattered more than the labour.**

The site had five sections. Dining, stage, kitchen, the covered walk between them, and the small one at the
back for storage.

**And here was the problem: you could only take down a whole section at a time, and you could only merge a
section into the one next to it.**

Which meant the men had to carry the poles and the sheets from wherever they finished to wherever they started
next. **And the cost of any move was how much you had accumulated so far.**

If you took down dining first — it was the biggest — **you were then carrying dining's load into every
subsequent move.** The whole afternoon, that weight, everywhere you went.

The nephew, who had been to college and was helping for the first time, said the obvious thing: **take the
smallest one first.**

Devrath said he had tried that for years, and it was sometimes right and often not, **because it depended on
what was next to what.**

And then the nephew, who was actually rather good at this, asked the question that made it work.

**"Forget which one you take down first. Which one is left standing at the end?"**

And Devrath stopped, because he had never once thought about it that way, and it was obviously the better
question.

**Because whichever section is last, everything to its left had to be cleared into one pile, and everything
to its right into another, and those two problems have nothing to do with each other.**

Two smaller versions of the same problem, and a known cost to join them.

**"You still have to try all five as the last one," the nephew said. "But then it is only five, and each one
splits into two easier days."**

---

## 3. The idea in plain English

Devrath's nephew has just described interval DP, including the inversion that makes the hard version work.

**The state is a range:**

> **`dp[i][j]` is the answer for the piece of the input from index `i` to index `j` inclusive.**

**That is a two-dimensional table where both indices point into the same array**, which is what distinguishes
it from yesterday's grid and from LCS — there, the two indices pointed into two different things.

**The recurrence tries every way of splitting the range.**

```
dp[i][j] = best over all k in [i, j-1] of:
             dp[i][k] + dp[k+1][j] + cost_of_joining(i, k, j)
```

**The `k` loop is the "which split" loop**, and it is the third nest that makes these `O(n³)`.

**And the fill order is forced.** `dp[i][j]` reads `dp[i][k]` and `dp[k+1][j]`, **both strictly shorter than
`i..j`**. So every shorter range must already be computed:

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            ...
```

**Length outermost, always.** Fill in the natural row-by-row order and a cell reads shorter ranges that have
not been computed yet, so it sees zeros — **and a zero does not mean "costs nothing", it means "not done".**
**The result is a total that is too CHEAP**, which is the direction that makes it hard to spot: a plan that
looks better than it should does not raise suspicion the way one that looks worse would.

**Now the two problems that define the shape.**

**Matrix chain multiplication.** You have matrices to multiply in a fixed order, and matrix multiplication is
associative — `(AB)C` and `A(BC)` give the same result — **but they cost different amounts.** Multiplying a
`10×100` by a `100×5` costs `10 × 100 × 5 = 5,000` scalar multiplications. **Find the cheapest
parenthesisation.**

**The state is exactly the shape above**: `dp[i][j]` is the cheapest way to multiply matrices `i` through `j`.
The split `k` is where the outermost multiplication happens — **you compute `i..k` into one matrix, `k+1..j`
into another, and multiply those two.**

**The joining cost is `dims[i] × dims[k+1] × dims[j+1]`**, which is the size of the two resulting matrices.
**Getting those three indices right is the fiddly part**, and the trick is to store dimensions as a single
array where matrix `i` is `dims[i] × dims[i+1]`.

**Burst balloons, which is the one that teaches the inversion.**

You have balloons with numbers. Bursting balloon `i` earns `left × i × right`, where left and right are its
current neighbours. **After bursting, the neighbours become adjacent.** Maximise your total.

**The obvious state is "which balloon do I burst first in this range", and it does not work.** If you burst
balloon `k` first, the range splits into `i..k-1` and `k+1..j` — **but those two halves are no longer
independent**, because when you later burst the last balloon of the left half, its right neighbour is
whatever survives in the right half. **The subproblems are entangled, and DP needs them not to be.**

**The fix is Devrath's nephew: ask which balloon is burst LAST.**

**If `k` is the last balloon burst in the range `i..j`, then when you burst it, everything else in the range
is already gone** — so its neighbours are exactly the boundaries, `i-1` and `j+1`, which are outside the range
and therefore fixed.

```
dp[i][j] = max over k in [i, j] of:
             dp[i][k-1] + dp[k+1][j] + nums[i-1] * nums[k] * nums[j+1]
```

**Now the two halves are genuinely independent**, because each one's boundaries are fixed and known. **That is
the whole problem**, and the code afterwards is fifteen lines.

**Say this out loud in an interview**: "thinking about the first one to burst leaves the subproblems entangled;
thinking about the last one fixes the boundaries and makes them independent."

**Two mechanical details for burst balloons.** **Pad the array with a 1 at each end**, so `nums[i-1]` and
`nums[j+1]` always exist — that removes every boundary special case. And **the `k` loop runs over `[i, j]`
inclusive**, not `[i, j-1]`, because `k` is a member of the range rather than a split between two halves.

**And the family, which is larger than it looks.**

```
matrix chain          which multiplication is OUTERMOST
burst balloons        which balloon is burst LAST
stone game            which move is optimal, alternating players
optimal BST           which key is the ROOT
palindrome partition  where the cuts go
minimum score triangulation  which triangle contains the base edge
```

**Every one of them asks "what is the last/outermost/root thing", and every one splits into two independent
ranges.** Recognising that phrasing is most of the work.

**Finally, the cost, which is why these are Hard.**

**`O(n³)` time**: `n²` ranges, and `O(n)` split points for each. **`O(n²)` space.**

**At `n = 100` that is a million operations — instant. At `n = 500` it is 125 million — about a minute in
Python.** So the constraint on `n` is usually small, and **seeing `n <= 100` or `n <= 500` in the problem
statement is itself a hint that the answer is cubic.**

---

## 4. The picture

The shape of the recurrence:

```
   range i..j

   i-----------------j
   |        |        |
   +--------+--------+
   dp[i][k]   dp[k+1][j]        <- both STRICTLY SHORTER
             ^
             the split point k, tried at EVERY position

   dp[i][j] = best over k of  dp[i][k] + dp[k+1][j] + join(i,k,j)

   Three nested loops:
     length   (outermost, and it MUST be)
     i        (the start; j follows from i and length)
     k        (the split)
   -> O(n^3)
```

Why the fill order is forced:

```
        j ->
        0    1    2    3
   i  +----+----+----+----+
   0  |    | L2 | L3 | L4 |     the number is the RANGE LENGTH
      +----+----+----+----+
   1  |    |    | L2 | L3 |
      +----+----+----+----+
   2  |    |    |    | L2 |
      +----+----+----+----+

   dp[0][3] (length 4) needs dp[0][k] and dp[k+1][3]
                            -> lengths 1..3, all SHORTER

   filling row by row reaches dp[0][3] while dp[1][3] is still zero
   -> reads a zero that means "not computed", not "cost zero"
   -> the answer is nonsense, LOUDLY (unlike the palindrome table)

   FILL BY INCREASING LENGTH. Diagonal by diagonal, upwards.
```

Matrix chain, and where the join cost comes from:

```
  dims = [10, 100, 5, 50]
  matrix 0 is 10x100,  matrix 1 is 100x5,  matrix 2 is 5x50

  ((A B) C):   A B  = 10x100 x 100x5  -> 10 x 100 x 5  = 5,000
               (AB)C = 10x5   x 5x50  -> 10 x 5 x 50   = 2,500
                                                  total  7,500

  (A (B C)):   B C  = 100x5  x 5x50   -> 100 x 5 x 50  = 25,000
               A(BC) = 10x100 x 100x50 -> 10 x 100 x 50 = 50,000
                                                  total 75,000

  SAME RESULT. 10x the cost. That is the whole problem.

  join(i, k, j) = dims[i] * dims[k+1] * dims[j+1]
                  ^          ^            ^
                  rows of    the shared   columns of
                  i..k       dimension    k+1..j
```

The burst-balloons inversion, which is the point of the lesson:

```
  nums = [3, 1, 5, 8]        padded: [1, 3, 1, 5, 8, 1]

  THINKING "FIRST" — DOES NOT WORK

     burst 5 first, from range 3..8
        left half:  [3, 1]     right half: [8]
        but when I later burst the 1 in the left half,
        its right neighbour is... the 8? or whatever is left?
     -> the halves DEPEND ON EACH OTHER
     -> not subproblems at all

  THINKING "LAST" — WORKS

     if 5 is burst LAST in range [3,1,5,8], then when I burst it
     everything else in that range is already gone
     -> its neighbours are the BOUNDARIES: the padded 1 on the left
        and the padded 1 on the right. FIXED.
     -> reward = 1 * 5 * 1
     -> and [3,1] and [8] are now fully independent problems,
        each with its own fixed boundaries

  ONE CHANGE OF QUESTION. That is the entire difficulty.
```

The `k` loop differs between the two problems:

```
  MATRIX CHAIN                 BURST BALLOONS

  k is a SPLIT between         k is a MEMBER of the range
  two halves                   (the one burst last)

  for k in range(i, j):        for k in range(i, j + 1):
    dp[i][k] + dp[k+1][j]        dp[i][k-1] + dp[k+1][j]
       ^ k is in the LEFT half        ^ k is in NEITHER half

  Getting this wrong is a silent off-by-one that produces
  a plausible smaller answer.
```

The three loops, drawn as the diagonals they fill:

```
  n = 5

  length 1:  (0,0) (1,1) (2,2) (3,3) (4,4)     base cases
  length 2:  (0,1) (1,2) (2,3) (3,4)
  length 3:  (0,2) (1,3) (2,4)
  length 4:  (0,3) (1,4)
  length 5:  (0,4)                             <- the answer

  Each diagonal only reads diagonals ABOVE it (shorter ranges).
  That is why length is the outer loop.
```

---

## 5. The code, built step by step

### The skeleton, which every interval DP shares

```python
def interval_dp_skeleton(n: int):
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):            # LENGTH OUTERMOST. Always.
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")           # or -inf for maximising
            for k in range(i, j):             # every split point
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + join(i, k, j))
    return dp[0][n - 1]
```

**Write this skeleton first, then fill in `join` and the initialisation.** The three loops and their order are
the same in every problem of this family; only the joining cost and the direction of the optimisation change.

**`length` starts at 2** because ranges of length 1 are the base case — a single item needs no combining.

### Matrix chain multiplication

```python
def matrix_chain(dims: list[int]) -> int:
    """dims has n+1 entries; matrix i is dims[i] x dims[i+1]."""
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]          # dp[i][i] = 0: one matrix, no work
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j]
                        + dims[i] * dims[k + 1] * dims[j + 1])
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n - 1]
```

**The `dims` convention is what makes this manageable**: `n + 1` numbers for `n` matrices, so matrix `i` is
`dims[i] × dims[i+1]` and the shared dimension between the two halves is `dims[k+1]`.

**`dp[i][i] = 0`** — a single matrix costs nothing to "multiply".

### Recovering the parenthesisation

```python
def matrix_chain_order(dims: list[int]) -> str:
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]       # where the best k was
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j], split[i][j] = cost, k

    def build(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        return f"({build(i, k)} {build(k + 1, j)})"

    return build(0, n - 1)
```

**One extra table recording the winning `k`, and a recursive walk-down.** **This is the standard reconstruction
for interval DP**, and it is a walk *down* rather than back, because the structure is a tree.

### Burst balloons, with the padding

```python
def max_coins(nums: list[int]) -> int:
    values = [1] + [n for n in nums if n > 0] + [1]     # pad both ends
    n = len(values)
    dp = [[0] * n for _ in range(n)]
    for length in range(1, n - 1):            # length of the INNER range
        for i in range(1, n - length):
            j = i + length - 1
            for k in range(i, j + 1):         # k is a MEMBER, so j+1
                dp[i][j] = max(
                    dp[i][j],
                    dp[i][k - 1] + dp[k + 1][j]
                    + values[i - 1] * values[k] * values[j + 1],
                )
    return dp[1][n - 2]
```

**The padding is what removes every boundary case.** `values[i-1]` and `values[j+1]` always exist, so there is
no `if i == 0` anywhere.

**`for k in range(i, j + 1)` — inclusive — because `k` is the balloon burst last, which belongs to neither
half.** Writing `range(i, j)` here is the silent off-by-one that gives a plausible smaller answer.

**And `dp[1][n-2]` is the answer**, not `dp[0][n-1]`, because indices 0 and `n-1` are the padding.

### The memoised version, which some people find clearer

```python
from functools import lru_cache

def max_coins_memo(nums: list[int]) -> int:
    values = [1] + [n for n in nums if n > 0] + [1]

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> int:
        if i > j:
            return 0                          # empty range
        return max(
            best(i, k - 1) + best(k + 1, j)
            + values[i - 1] * values[k] * values[j + 1]
            for k in range(i, j + 1)
        )

    return best(1, len(values) - 2)
```

**Identical complexity, and the fill order is handled for you by the recursion** — which is a genuine argument
for writing interval DP top-down under time pressure. **Say that explicitly**: "I would write it memoised,
because then I cannot get the fill order wrong."

### Stone game, which is interval DP with two players

```python
def stone_game(piles: list[int]) -> int:
    """The first player's score minus the second's, both playing optimally."""
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]                   # one pile: take it
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] - dp[i + 1][j],       # take the left
                           piles[j] - dp[i][j - 1])       # take the right
    return dp[0][n - 1]
```

**The minus sign is the whole trick.** `dp[i][j]` is the *difference* the current player can achieve, so the
opponent's best difference on the remaining range is subtracted. **One expression handles both players**, which
is much cleaner than tracking whose turn it is.

**And note this one has no `k` loop** — the split is always at an end, so it is `O(n²)` rather than `O(n³)`.

### The complete solution

```python
"""Interval DP: the shape, the classics, and the last-not-first inversion."""

from functools import lru_cache


def matrix_chain(dims: list[int]) -> int:
    """dims has n+1 entries; matrix i is dims[i] x dims[i+1]."""
    n = len(dims) - 1
    if n < 2:
        return 0
    dp = [[0] * n for _ in range(n)]          # one matrix costs nothing
    for length in range(2, n + 1):            # LENGTH OUTERMOST
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):             # k is a SPLIT: [i..k] [k+1..j]
                cost = (dp[i][k] + dp[k + 1][j]
                        + dims[i] * dims[k + 1] * dims[j + 1])
                dp[i][j] = min(dp[i][j], cost)
    return int(dp[0][n - 1])


def matrix_chain_order(dims: list[int]) -> str:
    """The cheapest parenthesisation itself."""
    n = len(dims) - 1
    if n == 1:
        return "A0"
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j], split[i][j] = cost, k

    def build(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        return f"({build(i, k)} {build(k + 1, j)})"

    return build(0, n - 1)


def max_coins(nums: list[int]) -> int:
    """Burst balloons. k is the balloon burst LAST, not first."""
    values = [1] + [x for x in nums if x > 0] + [1]     # padding kills edge cases
    n = len(values)
    dp = [[0] * n for _ in range(n)]
    for length in range(1, n - 1):
        for i in range(1, n - length):
            j = i + length - 1
            for k in range(i, j + 1):         # INCLUSIVE: k is a member
                dp[i][j] = max(
                    dp[i][j],
                    dp[i][k - 1] + dp[k + 1][j]
                    + values[i - 1] * values[k] * values[j + 1],
                )
    return dp[1][n - 2]                       # 0 and n-1 are the padding


def max_coins_memo(nums: list[int]) -> int:
    """The same, top-down. The recursion handles the fill order for you."""
    values = [1] + [x for x in nums if x > 0] + [1]

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> int:
        if i > j:
            return 0
        return max(
            best(i, k - 1) + best(k + 1, j)
            + values[i - 1] * values[k] * values[j + 1]
            for k in range(i, j + 1)
        )

    return best(1, len(values) - 2)


def stone_game(piles: list[int]) -> int:
    """First player's score minus the second's. No k loop: O(n^2)."""
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])
    return dp[0][n - 1]


def min_score_triangulation(values: list[int]) -> int:
    """Which triangle contains the edge i..j? Same shape again."""
    n = len(values)
    dp = [[0] * n for _ in range(n)]
    for length in range(3, n + 1):            # a triangle needs 3 vertices
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k][j] + values[i] * values[k] * values[j])
    return int(dp[0][n - 1])


def min_cut_palindrome(s: str) -> int:
    """Palindrome partitioning: interval DP for the table, 1-D for the cuts."""
    n = len(s)
    if n < 2:
        return 0
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True
    cuts = [0] * n
    for j in range(n):
        cuts[j] = 0 if is_pal[0][j] else min(
            cuts[i - 1] + 1 for i in range(1, j + 1) if is_pal[i][j])
    return cuts[n - 1]


if __name__ == "__main__":
    dims = [10, 100, 5, 50]
    print("matrix chain cost  :", matrix_chain(dims))
    print("the parenthesising :", matrix_chain_order(dims))
    print("bigger chain       :", matrix_chain([40, 20, 30, 10, 30]))
    print("its order          :", matrix_chain_order([40, 20, 30, 10, 30]))

    print("burst [3,1,5,8]    :", max_coins([3, 1, 5, 8]))
    print("memo agrees        :", max_coins_memo([3, 1, 5, 8]))
    print("burst [1,5]        :", max_coins([1, 5]))
    print("burst single       :", max_coins([7]))

    print("stone game [5,3,4,5]:", stone_game([5, 3, 4, 5]))
    print("stone game [3,7,2,3]:", stone_game([3, 7, 2, 3]))

    print("triangulation      :", min_score_triangulation([1, 3, 1, 4, 1, 5]))
    print("palindrome cuts    :", min_cut_palindrome("aab"))
```

Run it and you get:

```
matrix chain cost  : 7500
the parenthesising : ((A0 A1) A2)
bigger chain       : 26000
its order          : ((A0 (A1 A2)) A3)
burst [3,1,5,8]    : 167
memo agrees        : 167
burst [1,5]        : 10
burst single       : 7
stone game [5,3,4,5]: 1
stone game [3,7,2,3]: 5
triangulation      : 13
palindrome cuts    : 1
```

**`matrix chain cost 7500` against the 75,000 of the other order** is the point of that problem: **ten times
the work for the same answer.**

**And `burst [3,1,5,8] = 167`** is the classic — burst 1 first, then 5, then 3, then 8, which is a sequence you
would never find by thinking forwards.

---

## 6. What it costs

**Time: three nested loops.**

```
length   n values
i        up to n values for each length
k        up to n values for each (i, j)

-> O(n^3)

more precisely: sum over lengths L of (n - L + 1) x (L - 1)
              ~ n^3 / 6
```

**Concretely:**

```
n = 50     50^3 / 6  = ~21,000 operations      instant
n = 100    ~167,000                            instant
n = 500    ~21,000,000                         ~5 s in Python
n = 1,000  ~167,000,000                        ~40 s. Too slow.
n = 5,000  ~2 x 10^10                          hours
```

**So the constraint tells you the shape.** LeetCode's burst balloons caps `n` at 500, matrix chain problems
usually cap at 100. **If you see `n <= 100` with a range-shaped problem, cubic is expected** — and if you see
`n <= 10^5`, interval DP is not the answer and you should look for something else.

**Space: `O(n²)`.**

```
n = 500:  250,000 cells
          Python list of lists of ints: ~28 bytes per int object
          -> ~7 MB. Fine.

n = 5,000: 25,000,000 cells -> ~700 MB. Not fine.
```

**And unlike the last few days, there is no space collapse.** `dp[i][j]` reads cells from many different rows —
`dp[i][k]` for every `k` — so **you cannot keep one row.** **Saying that explicitly when asked to reduce the
space is the right answer**, rather than searching for a trick that is not there.

**The reconstruction cost:**

```
one extra n x n table storing the winning k
-> O(n^2) more space, no extra time
-> the walk-down is O(n): each call splits into two, and there are
   n leaves
```

**Compared with brute force:**

```
the number of ways to parenthesise n matrices is the (n-1)th
Catalan number:

  n = 5    14 ways
  n = 10   4,862
  n = 15   2,674,440
  n = 20   1,767,263,190
  n = 25   ~1.3 x 10^12

DP at n = 25:  25^3 / 6 = ~2,600 operations

-> 10^12 against 10^3. Nine orders of magnitude, which is why
   this problem is in every textbook.
```

**Stone game, for contrast:**

```
no k loop — the split is always at an end
-> O(n^2) time, O(n^2) space

n = 5,000: 25,000,000 operations, ~5 s. Viable where the cubic
version would not be.
```

**And a note on the memoised version:**

```
same O(n^3) calls, plus function-call overhead
in Python: roughly 2-3x slower than the bottom-up loops
in exchange for: the fill order cannot be wrong

for n <= 500 the difference is seconds, and the correctness
guarantee is usually worth more.
```

---

## 7. The traps

**Filling row by row instead of by length.**

```python
>>> dims = [10, 100, 5, 50]
>>> n = 3
>>> dp = [[0] * n for _ in range(n)]
>>> for i in range(n):                        # natural order: WRONG
...     for j in range(i + 1, n):
...         dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1]
...                        for k in range(i, j))
>>> dp[0][2]
7500
```

**Here it happens to be right**, because `n = 3` is small enough that the dependencies are satisfied by
accident. **On a longer chain it is not:**

```python
>>> dims = [40, 20, 30, 10, 30]
>>> n = 4
>>> dp = [[0] * n for _ in range(n)]
>>> for i in range(n):
...     for j in range(i + 1, n):
...         dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1]
...                        for k in range(i, j))
>>> dp[0][3]
20000
```

**Twenty thousand, when the true minimum is twenty-six thousand** — and note it came out *lower* than the real
answer, because it read a `dp[1][3]` that was still zero and therefore looked free. **A cost that is too cheap
is the direction that makes this hard to spot**, since a plan that looks better than possible does not raise
suspicion the way a plan that looks worse would.

**And a dependency satisfied by an accident of size is the worst kind of bug**, because the three-matrix test
passes. **Write `for length in ...` first, every time.**

**Using `range(i, j)` for `k` in burst balloons.**

```python
>>> # k is the balloon burst LAST — it is a MEMBER of [i, j]
>>> # range(i, j) excludes j, so the rightmost balloon is never
>>> # considered as the last one burst
>>> # -> a plausible SMALLER answer, no error
```

**Matrix chain uses `range(i, j)` because `k` is a split; burst balloons uses `range(i, j+1)` because `k` is a
member.** They look identical and are not, and this is the single most common bug in the topic.

**Thinking "first" in burst balloons.**

```
burst k first:  left half i..k-1,  right half k+1..j
                but the left half's rightmost balloon will,
                when burst, have a right neighbour that depends
                on what is left in the RIGHT half

-> the subproblems are not independent
-> the recurrence you write is simply wrong, and it produces
   a plausible number
```

**No error. A wrong answer.** And it is very hard to debug, because the code looks correct — **the mistake is in
the modelling, not the implementation.**

**Forgetting the padding.**

```python
>>> nums = [3, 1, 5, 8]
>>> # without padding, dp[0][j] needs nums[-1]
>>> nums[-1]
8
```

**Python's negative indexing does not raise — it wraps to the end of the list**, so the boundary silently uses
the wrong balloon. **Pad with 1s and the problem cannot occur.**

**Initialising to 0 when minimising.**

```python
>>> dp = [[0] * 3 for _ in range(3)]
>>> # dp[i][j] = min(dp[i][j], cost)  with dp[i][j] starting at 0
>>> # 0 wins every min -> every answer is 0
```

**Set the cell to infinity before the `k` loop when minimising**, and to zero only when maximising. **The base
cases — length 1 — are genuinely zero in both, which is what makes the confusion easy.**

**Getting the matrix chain dimension indices wrong.**

```python
>>> # dims[i] * dims[k+1] * dims[j+1]      correct
>>> # dims[i] * dims[k] * dims[j]          WRONG, and it runs
```

**All three are valid indices, so there is no error** — just a cost function computing the wrong thing.
**Derive them from the convention out loud**: the left result is `dims[i] × dims[k+1]`, the right is
`dims[k+1] × dims[j+1]`, so the multiplication costs `dims[i] × dims[k+1] × dims[j+1]`.

**Trying to collapse the space.**

```python
>>> # dp[i][j] reads dp[i][k] for EVERY k in [i, j-1]
>>> # those live in row i, spread across many columns
>>> # and dp[k+1][j] lives in many DIFFERENT ROWS
>>> # -> there is no one-row version. Do not look for one.
```

**Saying "there is no space collapse here, because the recurrence reads many rows" is the correct answer** to
the reduce-the-space question, and it is better than an incorrect attempt.

**`n` too large.**

```python
>>> dp = [[0] * 5000 for _ in range(5000)]
>>> # 25,000,000 cells, ~700 MB, and n^3/6 = 2 x 10^10 operations
```

**No error at `n = 5,000` for the allocation on a large machine — it just never finishes.** **The constraint in
the problem is the signal**, and reading it before choosing the approach is the whole defence.

---

## 8. In the interview

### How it gets asked

- *"Given a chain of matrices, find the cheapest order to multiply them."* — matrix chain, the classic.
- *"Burst balloons to maximise coins."* — LeetCode 312, and the inversion is the whole question.
- *"Two players take stones from either end of a row. Who wins?"* — LeetCode 877 / 486.
- *"What is the fill order, and why?"*
- *"Can you reduce the space?"* — where the right answer is "no, and here is why".
- *"Minimum score triangulation of a polygon."* — LeetCode 1039, the same shape again.

### The first ninety seconds

> "This is interval DP, and the signature is that **the state is a range and the answer depends on how I split
> it.**
>
> **`dp[i][j]` is the answer for the piece of the input from `i` to `j` inclusive.** Both indices point into the
> same array, which is what distinguishes this from something like longest common subsequence where they
> pointed into two different strings.
>
> **The recurrence tries every split point.** `dp[i][j]` is the best over all `k` of `dp[i][k]` plus
> `dp[k+1][j]` plus whatever it costs to join those two halves. **That `k` loop is the third nest, and it is
> what makes these cubic.**
>
> **And the fill order is forced, which is the part I would state before writing any loops.** `dp[i][j]` reads
> `dp[i][k]` and `dp[k+1][j]`, **both strictly shorter ranges** — so every shorter range must already be
> computed. **Length is the outermost loop, then the start, then the split.** Filling row by row reads cells
> that do not exist yet.
>
> **Base cases are ranges of length one**, which need no combining and cost nothing.
>
> **`O(n³)` time and `O(n²)` space** — `n²` ranges, `O(n)` splits each.
>
> **And there is no space collapse here**, which is worth saying up front because it is usually the next
> question: `dp[i][j]` reads many different rows, not just the previous one, **so keeping a single row is not
> possible.** That is a real difference from the grid problems.
>
> **One practical thing: I would write it memoised, top-down, rather than bottom-up.** Same complexity, and
> **the recursion handles the fill order for me, so I cannot get it wrong under time pressure.** In Python it
> is two or three times slower from call overhead, which for the `n ≤ 500` these problems come with is
> seconds.
>
> **What is the constraint on `n`?** Because cubic means `n` in the hundreds, and if it is a hundred thousand
> then this is not the right shape and I should be looking for something else."

### The follow-ups

**"Walk me through burst balloons."**

> "This one has a single idea in it, and everything else is fifteen lines of code, so let me spend the time on
> the idea.
>
> **The obvious approach is to ask which balloon I burst first, and it does not work.** If I burst balloon `k`
> first, the range appears to split into everything left of `k` and everything right of `k`. **But those two
> halves are not independent.** When I later burst the rightmost balloon of the left half, its right neighbour
> is whatever is still standing in the right half — **so the two subproblems depend on each other**, and
> dynamic programming needs them not to.
>
> **The fix is to ask which balloon is burst last.**
>
> **If `k` is the last one burst in the range `i..j`, then at the moment I burst it, everything else in that
> range is already gone.** So its neighbours are exactly the boundaries — the elements just outside the range —
> **which are fixed and known.** The reward is `nums[i-1] × nums[k] × nums[j+1]`.
>
> **And now the two halves are genuinely independent**, because each has fixed boundaries of its own.
>
> **`dp[i][j] = max over k of dp[i][k-1] + dp[k+1][j] + nums[i-1]*nums[k]*nums[j+1]`.**
>
> **Two mechanical details.** **Pad the array with a 1 at each end**, so `nums[i-1]` and `nums[j+1]` always
> exist — otherwise Python's negative indexing silently wraps to the end of the list and uses the wrong
> balloon, with no error.
>
> **And the `k` loop is inclusive of `j`**, unlike matrix chain. **Here `k` is a member of the range — the one
> burst last — so it belongs to neither half.** In matrix chain, `k` is a split point and belongs to the left
> half, so the loop excludes `j`. **They look identical and they are not, and writing `range(i, j)` here gives
> a plausible smaller answer with no error.**
>
> **`O(n³)` time, `O(n²)` space**, and the answer is `dp[1][n-2]` because the outer indices are padding.
>
> **The general lesson is worth naming: when the obvious decomposition leaves the subproblems entangled, try
> asking about the last thing rather than the first.** The same inversion solves matrix chain — which
> multiplication is outermost — and optimal binary search trees — which key is the root."

**"What is the fill order and why does it matter here more than usual?"**

> "Because the dependency points at strictly shorter ranges, and the natural loop order does not respect that.
>
> **`dp[i][j]` reads `dp[i][k]` and `dp[k+1][j]` for every split `k`.** Both of those are strictly shorter than
> `i..j` — the first ends earlier, the second starts later. **So every shorter range must be finished first.**
>
> **The correct order is by increasing length**: all ranges of length two, then three, and so on. Geometrically
> that is filling the table **diagonal by diagonal, moving away from the main diagonal**, and each diagonal
> reads only the ones above it.
>
> **Filling row by row breaks it.** Going along row zero, I reach `dp[0][4]` while `dp[1][4]` — which it needs —
> is still zero. **And zero does not mean 'costs nothing', it means 'not computed'**, so the answer is wrong.
>
> **What makes this nastier than usual is that a small test can pass by accident.** With three matrices, the
> natural order happens to satisfy the dependencies, so a three-element test passes and a five-element one
> fails. **A dependency satisfied by an accident of size is the worst kind of bug.**
>
> **There is a second correct order** — `i` descending, `j` ascending from `i` — which also works, because row
> `i+1` is complete before row `i` starts. **But the length version makes the reason visible in the loop
> itself**, so it is the one I would write.
>
> **And the honest practical answer: I would write it memoised.** A top-down recursion with a cache explores
> the dependencies in whatever order it needs, **so the fill order cannot be wrong.** Same complexity, and in
> an interview that is worth two or three times the constant factor."

**"Can you reduce the space?"**

> "No, and I think saying so clearly is a better answer than attempting something that does not work.
>
> **In the grid problems, the collapse worked because `dp[r][c]` read exactly two cells — the one above and the
> one to the left — so one row of history was enough.**
>
> **Here `dp[i][j]` reads `dp[i][k]` for every `k` from `i` to `j-1`, and `dp[k+1][j]` for every one of those
> too.** The first group is spread across row `i`; the second group is **spread across many different rows**.
> **There is no single row, or pair of rows, that contains what I need**, so the whole `O(n²)` table has to be
> live.
>
> **What I can do is smaller than that, and worth mentioning.**
>
> **Only half the table is ever used** — cells where `i > j` are meaningless — so a triangular representation
> saves about half the memory. **In Python that costs more in overhead than it saves; in C it is worth doing.**
>
> **And if I need the reconstruction I need a second table anyway**, so I would raise that trade: the answer
> alone is `O(n²)`, and the answer plus the parenthesisation is two `O(n²)` tables.
>
> **The real limit is the time, not the space.** At `n = 500`, `n³/6` is about twenty-one million operations
> and the table is seven megabytes — **so I run out of patience long before I run out of memory.** At
> `n = 5,000` it is two times ten to the ten operations, which is hours, and the seven hundred megabytes is the
> lesser problem.
>
> **So if someone needs `n = 10,000`, the answer is not a better constant factor — it is that interval DP is
> the wrong approach and there must be extra structure in the problem to exploit.** Matrix chain specifically
> has an `O(n log n)` algorithm — Hu and Shing — which I know exists and would not write."

### The model answer

*"You are compiling a query plan. A query joins `n` tables in a fixed logical order, and joining two
intermediate results costs the product of their row counts. Find the cheapest order to perform the joins."*

> "This is matrix chain multiplication with different words, and I want to establish the mapping before writing
> anything, because that is where the value is.
>
> **A join of two intermediate results is a binary operation whose cost depends on the sizes of both operands
> — and those sizes depend on which joins you did earlier.** That is exactly the matrix chain structure:
> **associative, so every order gives the same answer, and the orders cost wildly different amounts.**
>
> **And the fixed logical order matters.** Because the tables must be joined in sequence — table one with two,
> that with three — **the only freedom is the parenthesisation**, which is what makes it an interval problem
> rather than a general search over join trees. **I would confirm that**, because if any table can join any
> other, this is a completely different and much harder problem — that is the general join-ordering problem,
> which is exponential and is why real optimisers use heuristics.
>
> **The state: `dp[i][j]` is the cheapest cost to join tables `i` through `j` into one intermediate result.**
>
> **The recurrence tries every split.** For each `k`, compute `i..k` into one result and `k+1..j` into another,
> then join those two. **`dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + cost_of_joining(i, k, j)`.**
>
> **The joining cost needs the sizes of the two intermediates**, and that is the modelling question I would
> raise: **for matrices the resulting dimensions are determined; for joins they are estimated.** I would need a
> cardinality estimate for the result of joining `i..k` — from statistics, or a selectivity assumption — and
> **that estimate is where real query planners are wrong**, far more often than the search is.
>
> **Fill order: by increasing length**, because `dp[i][j]` reads only strictly shorter ranges. **Base case:
> a single table costs nothing to 'join'.**
>
> **Reconstruction matters more here than in the textbook version**, because the planner needs the plan, not
> the cost. **One extra table recording the winning `k`, then a recursive walk down** producing the join tree.
>
> **Cost: `O(n³)` time and `O(n²)` space.** For a query joining ten tables that is about 170 operations —
> nothing. **For fifty tables it is 21,000 — still nothing.** **And that is the point I would make about
> feasibility: query plans are small.** The cubic bound that limits this algorithm in the abstract is
> irrelevant when `n` is under a hundred, which it always is.
>
> **Two things I would say beyond the algorithm.**
>
> **First, this finds the optimal plan under the cost model, and the cost model is the weak link.** A plan that
> is optimal for wrong cardinality estimates is not optimal. **I would spend more effort on the estimates than
> on the search**, and I would want the planner to be robust to being wrong — preferring plans that are
> acceptable across a range of estimates rather than optimal for one.
>
> **Second, real optimisers memoise this exactly like the DP** — that is what a Selinger-style bottom-up
> planner is — **but they also prune aggressively**, discarding subplans that are dominated, because the real
> problem has more freedom than a fixed order and the search space is larger than `n³`.
>
> **And I would write it memoised rather than bottom-up.** Same complexity, the fill order cannot be wrong,
> and **a top-down formulation makes it much easier to add pruning later**, which is the direction this would
> actually grow."

---

## 9. Recall card

**Interval DP: `dp[i][j]` is the answer for the range `i..j`, and the recurrence tries every split.**
`dp[i][j] = best over k of dp[i][k] + dp[k+1][j] + join(i,k,j)`. **Three nested loops — length, start, split —
and length MUST be outermost**, because both dependencies are strictly shorter ranges. **A small test can pass
by accident with the wrong order**, which is the worst kind of bug.

**`O(n³)` time, `O(n²)` space, and there is NO space collapse** — `dp[i][j]` reads many different rows, not
just the previous one. **Saying that is the right answer to "reduce the space".** `n ≤ 100` or `n ≤ 500` in the
constraints is the signal that cubic is expected.

**Matrix chain: `join = dims[i] × dims[k+1] × dims[j+1]`** with matrix `i` being `dims[i] × dims[i+1]`.
`[10,100,5,50]` costs 7,500 one way and 75,000 the other — **ten times, for the same answer.** Brute force is
the Catalan numbers: 1.3 × 10¹² at `n = 25` against ~2,600 for the DP.

**Burst balloons is the inversion, and it is the whole problem: ask which balloon is burst LAST, not first.**
Thinking "first" leaves the two halves entangled, because the left half's last burst depends on what survives
on the right. **Thinking "last" fixes its neighbours to the range boundaries**, so the halves become
independent. **Pad both ends with 1** (negative indexing silently wraps otherwise), and **the `k` loop is
INCLUSIVE of `j`** — `k` is a member, not a split — unlike matrix chain, which is the most common bug here.

**Initialise to `inf` before the `k` loop when minimising** (0 wins every `min`). **Write it memoised
top-down**, because then the fill order cannot be wrong. **Stone game has no `k` loop** — the split is always
at an end — so it is `O(n²)`, and the minus sign (`piles[i] - dp[i+1][j]`) handles both players in one
expression.
