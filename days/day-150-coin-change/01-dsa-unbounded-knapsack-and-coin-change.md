---
day: 150
track: dsa
title: "Unbounded knapsack and coin change"
phase: "Dynamic programming"
status: written
---

# Unbounded knapsack and coin change

## 1. What this is, and why they ask it

Unbounded knapsack is yesterday's problem with one word changed: **you may take each item as many times as you
like.**

That one word changes exactly one character in the code. The inner loop runs forwards instead of backwards.
Everything else — the state, the recurrence, the base case, the complexity — is identical.

They ask it because **that single character is the cleanest test in dynamic programming of whether you
understood the loop or memorised it.** A candidate who says "forwards, because `dp[t - coin]` should already
include this coin" has understood. A candidate who writes it forwards and cannot say why got lucky, and the
interviewer will find out within one follow-up.

The other reason is coin change, which is the most-asked DP problem after Fibonacci. **Fewest coins to make an
amount** is unbounded knapsack minimising a count, and **the greedy algorithm you have used your whole life at
a shop counter is wrong** — which makes it a small, sharp lesson about why DP exists at all. Indian currency
happens to be one of the denomination systems where greedy works, which is exactly why the counter-example is
worth having ready.

By the end of this lesson you can write both loop directions and say what each means, solve minimum-coins and
count-ways, explain why greedy fails with specific numbers, and say why the counting version needs the loops in
one particular order.

---

## 2. The story

The tea shop had one price for four years and then the milk went up and Chandrakant had to think about change.

Nine rupees. That was the new price, and it was the first time it had not been a round number, and by the
second morning he understood what he had done to himself.

Because everyone paid with a ten, or a twenty, or a fifty, and he had to give back one rupee, or eleven, or
forty-one, and **the tin he kept the change in did not refill itself.**

He started counting what was in it. Coins of one, two, five and ten. Notes above that. And by Thursday he had
worked out the thing that actually mattered, which was not how much money was in the tin but **how many pieces**
were in it, because a customer waiting while you count out eleven single-rupee coins is a customer who goes to
the other shop.

So he began giving change the way anyone would: biggest first. Forty-one rupees, and he would put down two
twenties and a one. Three pieces. Clean.

And that worked, every single time, for four years, and he never once thought about it.

Then his cousin came for a month from a place where the coins were different — they had a seven and a
five and a one there, and no two — and Chandrakant, out of habit, gave someone ten with the same method.
**A seven, then a one, then a one, then a one.** Four pieces.

His cousin, who had been watching without saying anything, put down two fives.

**Two pieces. And the method had picked four.**

Chandrakant stood there for a while with the tin open. He had used that rule every day for four years and it
had never been wrong once, and it had never been wrong **because of the coins he happened to have**, not
because the rule was good.

**Nobody had told him the rule only worked here.**

---

## 3. The idea in plain English

Chandrakant's rule is the greedy algorithm, and his cousin has just produced the counter-example.

**Greedy on coins means: take the largest coin that fits, repeat.** With Indian denominations — 1, 2, 5, 10, 20,
50 — it is optimal for every amount, and you can go a lifetime without discovering that this is a property of
those particular numbers rather than of the method.

**With coins `[1, 5, 7]` and amount 10, greedy gives `7 + 1 + 1 + 1` — four coins. The answer is `5 + 5` — two.**

Say that example out loud until it is automatic. It is the whole reason this problem is DP and not one line.

**Now the DP.**

**The state, as a full sentence: `dp[t]` is the fewest coins that make exactly `t`.**

**The recurrence asks one question: what was the last coin?** If the last coin was `c`, then before it you had
made `t - c`, and that took `dp[t - c]` coins. So:

```
dp[t] = 1 + min(dp[t - c]) over every coin c that fits
```

**Try every coin as the last one and take the best.** That is the entire algorithm.

**The base case is `dp[0] = 0`** — zero coins make zero — and everything else starts at infinity, meaning "not
reachable yet".

**Infinity matters.** If you initialise to zero instead, every amount looks free and the answer is zero
everywhere. If you initialise to `-1`, the `min` picks `-1` and you get nonsense. **Use `float('inf')`, or a
sentinel larger than any possible answer**, and check at the end whether it is still infinite.

**Now the loop direction, which is the point of today.**

Yesterday's 0/1 knapsack ran the inner loop **backwards**, so that `dp[t - w]` still held the value from before
this item existed — each item usable once.

**Today it runs forwards**, so that `dp[t - c]` holds a value that **may already include this coin** — which is
exactly what "use it as many times as you like" means.

```python
for coin in coins:
    for t in range(coin, amount + 1):        # FORWARDS
        dp[t] = min(dp[t], dp[t - coin] + 1)
```

**Same six lines as yesterday. One range reversed. A different problem.** And neither version errors, so the
only defence is saying the direction and its reason as you write.

**Now the second question they ask: count the ways instead.**

*How many different combinations of coins make the amount?* Same table, but the cell holds a count:

```python
ways[0] = 1
for coin in coins:
    for t in range(coin, amount + 1):
        ways[t] += ways[t - coin]
```

**`ways[0] = 1`, because there is exactly one way to make nothing: take no coins.** Every count is built by
adding that one up.

**And here is the trap that catches almost everyone: the loop order matters, and it is not the direction this
time — it is which loop is outside.**

```
coins outside, amount inside   -> counts COMBINATIONS  {1,2} once
amount outside, coins inside   -> counts PERMUTATIONS  {1,2} and {2,1} separately
```

**With coins `[1, 2]` and amount 3:** combinations are `1+1+1` and `1+2` — **two**. Permutations are `1+1+1`,
`1+2`, `2+1` — **three**.

**Why:** with coins outside, coin 1 is fully processed before coin 2 is ever considered, so no arrangement can
ever place a 1 after a 2. The order is fixed by the loop, so each *set* is counted once. With amount outside,
every coin is offered at every amount, so orderings are counted separately.

**Both are correct programs.** Coin Change II asks for combinations; Combination Sum IV asks for permutations,
and its name is a lie. **Read the examples in the problem to decide which**, every time.

**Finally: minimising uses `min`, counting uses `+=`, and reachability uses `or`.** Three problems, one table,
three operators — and that is the family this week has been building towards.

---

## 4. The picture

The two loop directions, side by side, on the same six lines:

```
  0/1 KNAPSACK (yesterday)          UNBOUNDED (today)

  for item in items:                for coin in coins:
    for t in range(T, w-1, -1):       for t in range(coin, T+1):
      dp[t] = f(dp[t], dp[t-w])         dp[t] = f(dp[t], dp[t-coin])
              ^                                 ^
      reads a cell to the LEFT          reads a cell to the LEFT
      that this pass has NOT            that this pass MAY HAVE
      touched -> previous row           already updated -> this coin
      -> item used ONCE                 counted again -> UNLIMITED

  One range reversed. Two different problems. No error either way.
```

The minimum-coins table filling, `coins = [1, 5, 7]`, `amount = 10`:

```
  after coin 1:   t: 0  1  2  3  4  5  6  7  8  9 10
                     0  1  2  3  4  5  6  7  8  9 10     all ones

  after coin 5:   t: 0  1  2  3  4  5  6  7  8  9 10
                     0  1  2  3  4  1  2  3  4  5  2     dp[5]=1, dp[10]=2
                                    ^              ^
                              5 = one coin    10 = dp[5]+1 = 2

  after coin 7:   t: 0  1  2  3  4  5  6  7  8  9 10
                     0  1  2  3  4  1  2  1  2  3  2
                                          ^
                                    7 = one coin, better than 3

  answer dp[10] = 2  (5 + 5)

  Greedy would take 7 first, then 1+1+1. Four coins.
  The table never commits to a first choice, so it finds 5+5.
```

Why greedy fails, drawn as the two paths:

```
  amount 10, coins [1, 5, 7]

  GREEDY                          OPTIMAL
   take 7  -> 3 left               take 5  -> 5 left
   take 1  -> 2 left               take 5  -> 0 left
   take 1  -> 1 left               DONE. 2 coins.
   take 1  -> 0 left
   DONE. 4 coins.

  The greedy step "take 7" is locally the biggest reduction and
  globally wrong, because it leaves a remainder (3) that only
  1-rupee coins can fill.
```

Combinations against permutations, and where they diverge:

```
  coins [1, 2], amount 3

  COINS OUTSIDE (combinations)
    process coin 1 fully:   ways = [1, 1, 1, 1]
    process coin 2 fully:   ways = [1, 1, 2, 2]
                                            ^
    answer 2:  {1,1,1} and {1,2}
    Coin 2 is only ever added AFTER coin 1 is finished,
    so 2-then-1 can never be formed.

  AMOUNT OUTSIDE (permutations)
    t=1: from coin 1        ways[1] = 1
    t=2: from 1 and from 2  ways[2] = ways[1] + ways[0] = 2
    t=3: from 1 and from 2  ways[3] = ways[2] + ways[1] = 3
                                            ^
    answer 3:  {1,1,1}, {1,2}, {2,1}
    Both coins are offered at every amount, so order counts.
```

The recurrence as a tree, showing what memoisation removes:

```
              make(10)
       /         |         \
   coin 1      coin 5      coin 7
   make(9)     make(5)     make(3)
   / | \        / | \       / \
 ...        make(4) ...   make(2) ...
              |
            make(3)   <-- also reached from make(10) via coin 7
                          computed twice without a table,
                          once with one.

  The table has 11 cells. The tree has thousands of nodes.
  Same search, no repeats.
```

---

## 5. The code, built step by step

### Minimum coins, straight from the sentence

```python
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0                                 # zero coins make zero
    return dp[amount]                         # (loops next)
```

**`float('inf')` means "not reachable yet"**, and it is what makes the `min` behave. Zero would say every
amount is free; `-1` would win every `min` and poison the table.

Now the two loops:

```python
    for coin in coins:
        for t in range(coin, amount + 1):     # FORWARDS: coin reusable
            if dp[t - coin] + 1 < dp[t]:
                dp[t] = dp[t - coin] + 1
```

**`range(coin, amount + 1)` starts at `coin`**, because below that the coin cannot be used, and that also
removes the need for a `t >= coin` guard.

**Forwards is the whole lesson.** `dp[t - coin]` may already have this coin counted in it, and that is exactly
what unlimited supply means.

And the unreachable case:

```python
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Amount 3 with coins `[2]` is genuinely impossible**, and the problem asks for `-1`. Checking for infinity is
how you know.

### Counting the ways

```python
def coin_change_ii(coins: list[int], amount: int) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1                               # exactly one way to make nothing
    for coin in coins:                        # COINS OUTSIDE -> combinations
        for t in range(coin, amount + 1):
            ways[t] += ways[t - coin]
    return ways[amount]
```

**`ways[0] = 1` is the seed every count grows from.** Set it to zero and the answer is zero for every amount.

**Coins outside, amount inside.** Swap those two lines and you count permutations instead — a different, also
correct, answer to a different question.

### The permutation version, for contrast

```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    ways = [0] * (target + 1)
    ways[0] = 1
    for t in range(1, target + 1):            # AMOUNT OUTSIDE -> permutations
        for number in nums:
            if number <= t:
                ways[t] += ways[t - number]
    return ways[target]
```

**Every number is offered at every amount**, so `1+2` and `2+1` are counted separately. **The guard comes back**
because the inner loop is now over coins, not over amounts.

### Unbounded knapsack, maximising value

```python
def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for c in range(1, capacity + 1):
        for i, w in enumerate(weights):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + values[i])
    return dp[capacity]
```

**`dp[c] = 0` everywhere is right here**, not infinity, because taking nothing is always allowed and gives zero
value. **Compare that with `coin_change`, where taking nothing does not reach the amount** — the base case
follows from the question, not from habit.

### Reconstructing which coins were used

```python
def coin_change_with_coins(coins: list[int], amount: int) -> list[int] | None:
    dp = [float('inf')] * (amount + 1)
    choice: list[int | None] = [None] * (amount + 1)
    dp[0] = 0
    for t in range(1, amount + 1):
        for coin in coins:
            if coin <= t and dp[t - coin] + 1 < dp[t]:
                dp[t] = dp[t - coin] + 1
                choice[t] = coin              # remember the last coin used
    if dp[amount] == float('inf'):
        return None
    used, t = [], amount
    while t > 0:
        used.append(choice[t])
        t -= choice[t]
    return used
```

**One extra array holding the last coin for each amount**, and the walk-back subtracts coins until it reaches
zero. **`O(amount)` extra space** — cheap, unlike yesterday's reconstruction which needed every row.

### The BFS view, which is worth knowing

```python
from collections import deque

def coin_change_bfs(coins: list[int], amount: int) -> int:
    if amount == 0:
        return 0
    seen, queue, depth = {0}, deque([0]), 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            t = queue.popleft()
            for coin in coins:
                nxt = t + coin
                if nxt == amount:
                    return depth
                if nxt < amount and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return -1
```

**Minimum coins is a shortest path**, where each amount is a node and each coin is an edge of weight one.
[Day 131](../day-131-unweighted-shortest-path/README.md)'s BFS finds it, and the level counter is the coin
count. **Same complexity, and it stops early** when the amount is reachable in few coins. Mention it; write the
DP.

### The complete solution

```python
"""Unbounded knapsack: coin change, counting, and the loop-order trap."""

from collections import deque


def coin_change(coins: list[int], amount: int) -> int:
    """Fewest coins making exactly amount, or -1 if impossible."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0                                 # zero coins make zero
    for coin in coins:
        # FORWARDS: dp[t - coin] may already include this coin -> unlimited use
        for t in range(coin, amount + 1):
            if dp[t - coin] + 1 < dp[t]:
                dp[t] = dp[t - coin] + 1
    return int(dp[amount]) if dp[amount] != float('inf') else -1


def coin_change_with_coins(coins: list[int], amount: int) -> list[int] | None:
    """The actual coins, or None. One extra O(amount) array."""
    dp = [float('inf')] * (amount + 1)
    choice: list[int | None] = [None] * (amount + 1)
    dp[0] = 0
    for t in range(1, amount + 1):
        for coin in coins:
            if coin <= t and dp[t - coin] + 1 < dp[t]:
                dp[t] = dp[t - coin] + 1
                choice[t] = coin
    if dp[amount] == float('inf'):
        return None
    used: list[int] = []
    t = amount
    while t > 0:
        coin = choice[t]
        assert coin is not None
        used.append(coin)
        t -= coin
    return sorted(used)


def coin_change_ii(coins: list[int], amount: int) -> int:
    """How many COMBINATIONS make amount. Coins outside."""
    ways = [0] * (amount + 1)
    ways[0] = 1                               # one way to make nothing
    for coin in coins:
        for t in range(coin, amount + 1):
            ways[t] += ways[t - coin]
    return ways[amount]


def combination_sum_iv(nums: list[int], target: int) -> int:
    """How many PERMUTATIONS make target. Amount outside."""
    ways = [0] * (target + 1)
    ways[0] = 1
    for t in range(1, target + 1):
        for number in nums:
            if number <= t:
                ways[t] += ways[t - number]
    return ways[target]


def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """Best value, each item reusable."""
    dp = [0] * (capacity + 1)                 # taking nothing gives 0, always
    for c in range(1, capacity + 1):
        for i, w in enumerate(weights):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + values[i])
    return dp[capacity]


def greedy_coins(coins: list[int], amount: int) -> int:
    """Biggest coin first. Correct for Indian denominations, wrong in general."""
    count, left = 0, amount
    for coin in sorted(coins, reverse=True):
        take = left // coin
        count += take
        left -= take * coin
    return count if left == 0 else -1


def coin_change_bfs(coins: list[int], amount: int) -> int:
    """Minimum coins as a shortest path. Each coin is an edge of weight 1."""
    if amount == 0:
        return 0
    seen, queue, depth = {0}, deque([0]), 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            t = queue.popleft()
            for coin in coins:
                nxt = t + coin
                if nxt == amount:
                    return depth
                if nxt < amount and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return -1


if __name__ == "__main__":
    print("min coins [1,5,7] -> 10 :", coin_change([1, 5, 7], 10))
    print("greedy    [1,5,7] -> 10 :", greedy_coins([1, 5, 7], 10))
    print("which coins             :", coin_change_with_coins([1, 5, 7], 10))
    print("bfs agrees              :", coin_change_bfs([1, 5, 7], 10))

    print("min coins [1,2,5] -> 11 :", coin_change([1, 2, 5], 11))
    print("greedy    [1,2,5] -> 11 :", greedy_coins([1, 2, 5], 11))
    print("impossible [2] -> 3     :", coin_change([2], 3))

    print("combinations [1,2] -> 3 :", coin_change_ii([1, 2], 3))
    print("permutations [1,2] -> 3 :", combination_sum_iv([1, 2], 3))
    print("combinations [1,2,5]->5 :", coin_change_ii([1, 2, 5], 5))

    print("unbounded knapsack      :", unbounded_knapsack([2, 3, 4], [4, 5, 7], 9))
```

Run it and you get:

```
min coins [1,5,7] -> 10 : 2
greedy    [1,5,7] -> 10 : 4
which coins             : [5, 5]
bfs agrees              : 2
min coins [1,2,5] -> 11 : 3
greedy    [1,2,5] -> 11 : 3
impossible [2] -> 3     : -1
combinations [1,2] -> 3 : 2
permutations [1,2] -> 3 : 3
combinations [1,2,5]->5 : 4
unbounded knapsack      : 17
```

**Line one against line two is the lesson.** Same coins, same amount, and greedy is twice as expensive. **Lines
five and six show why nobody noticed** — on `[1, 2, 5]`, which is how Indian change actually works, greedy and
DP agree exactly.

**And `combinations` 2 against `permutations` 3** on the same input is the loop-order trap, made visible.

---

## 6. What it costs

**Time.** The same two nested loops as yesterday.

```
outer loop: once per coin                    len(coins) iterations
inner loop: once per amount from coin up     amount iterations

TOTAL: O(len(coins) x amount)
```

**Concretely, for the standard LeetCode constraints — 12 coins, amount up to 10,000:**

```
12 x 10,000 = 120,000 cells
each cell: one comparison, one possible assignment
-> about 0.02 seconds in Python. Instant.
```

**And where it stops:**

```
amount = 10^9
12 x 1,000,000,000 = 12,000,000,000 cells
-> hours, and the allocation fails first:

MemoryError
```

**Pseudo-polynomial again**, for exactly yesterday's reason: `amount` is a value in the input, not a size.

**Space.**

```
one row of amount + 1 cells
10,001 floats in a Python list -> about 80 KB

with reconstruction: one more array of the same size -> 160 KB
```

**Reconstruction is cheap here**, unlike yesterday, because you store one coin per amount rather than an entire
table of rows.

**Compare the three problems in the family:**

```
                     table cell    operator   base case
subset sum           boolean       or         dp[0] = True
count the ways       integer       +=         dp[0] = 1
minimum coins        integer       min        dp[0] = 0, rest inf
maximum value        integer       max        dp[c] = 0 everywhere

Same two loops every time. The operator and the base case
follow from the question.
```

**The BFS version, counted:**

```
worst case: every amount from 0 to amount is enqueued once
            each dequeue tries len(coins) edges
-> O(len(coins) x amount), the same as the DP

BUT it stops at the first level that reaches the amount.
coins [1, 5000], amount 10,000:
  DP   fills all 10,001 cells                = 20,002 operations
  BFS  finds 5000 + 5000 at depth 2          = ~4 nodes explored

For small answers with large amounts, BFS wins enormously.
For dense answers it is the same, with more overhead.
```

**Greedy's cost, for contrast:**

```
sort the coins            O(k log k)
one division per coin     O(k)
-> essentially free, and wrong.

The whole cost of DP here is the price of correctness on
denomination systems where greedy fails.
```

---

## 7. The traps

**The backwards loop, silently solving yesterday's problem.**

```python
>>> dp = [float('inf')] * 10
>>> dp[0] = 0
>>> for t in range(9, 2, -1):                     # BACKWARDS by mistake
...     dp[t] = min(dp[t], dp[t - 3] + 1)
>>> dp[9]
inf
```

**`inf` — meaning "impossible" — when the answer is obviously three coins of 3.** Each pass can use the coin
once, so 3 is reachable and 6 and 9 are not.

The same mistake on the fuller input:

```python
>>> coins, amount = [1, 5, 7], 10
>>> dp = [float('inf')] * 11
>>> dp[0] = 0
>>> for coin in coins:
...     for t in range(amount, coin - 1, -1):
...         dp[t] = min(dp[t], dp[t - coin] + 1)
>>> dp[10]
inf
```

**Also `inf`, because `5 + 5` needs the coin twice** and this version has forbidden that. No error, no warning,
just a claim that the amount cannot be made. **And note what would have hidden it:** on `coins = [1, 2, 5]`
with amount 8, where the answer `5 + 2 + 1` uses each coin once, both directions give 3 and the test passes.
**Test with an input that needs a repeat**, or the bug survives.

**Initialising `dp` to zero instead of infinity.**

```python
>>> dp = [0] * 11                    # wrong sentinel
>>> for coin in [1, 5, 7]:
...     for t in range(coin, 11):
...         dp[t] = min(dp[t], dp[t - coin] + 1)
>>> dp[10]
0
```

**Zero coins make ten.** Every `min` compares against a zero that was never earned, so nothing ever improves on
it. **The output is a plausible number**, which is what makes it dangerous.

**Initialising to `-1` because the problem returns `-1`.**

```python
>>> dp = [-1] * 11
>>> dp[0] = 0
>>> for coin in [1, 5, 7]:
...     for t in range(coin, 11):
...         dp[t] = min(dp[t], dp[t - coin] + 1)
>>> dp[10]
-1
```

**`-1` beats every real answer in a `min`.** Use infinity internally and convert to `-1` only at the return.

**Forgetting `ways[0] = 1` in the counting version.**

```python
>>> ways = [0] * 4
>>> for coin in [1, 2]:
...     for t in range(coin, 4):
...         ways[t] += ways[t - coin]
>>> ways[3]
0
```

**Zero ways to make three**, when there are two. Nothing was ever `1`, so nothing could be added up.

**The loop order, which produces a different correct answer.**

```python
>>> ways = [0] * 4; ways[0] = 1
>>> for t in range(1, 4):                    # amount outside
...     for coin in [1, 2]:
...         if coin <= t:
...             ways[t] += ways[t - coin]
>>> ways[3]
3
```

Against the combinations version's `2`. **Neither is a bug. They answer different questions**, and the only way
to know which one is wanted is to read the problem's examples. **LeetCode 377 is called Combination Sum IV and
wants permutations**, which is worth knowing precisely because the name is misleading.

**Integer overflow, in other languages.** The counting version grows fast:

```
coins [1..200], amount 1000  ->  the count exceeds 2^63
```

Python integers are unlimited so nothing happens. **In Java or C++ this silently wraps**, and the problem
usually asks for the answer modulo `10^9 + 7` precisely because of that. **Read the problem statement for a
modulus** before assuming.

**`float('inf')` arithmetic leaking into the answer.**

```python
>>> float('inf') + 1
inf
>>> int(float('inf'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OverflowError: cannot convert float infinity to integer
```

**`inf + 1` stays `inf`, which is what makes the sentinel work.** But `int()` on it raises — so check for
infinity *before* converting, which is why the return line is written the way it is.

**Amount zero.**

```python
>>> coin_change([1, 5, 7], 0)
0
```

**Correct, and worth checking**, because a solution that starts its loop at `t = 1` and returns `dp[amount]`
handles it for free, while a recursive version without a base case for zero recurses forever.

---

## 8. In the interview

### How it gets asked

- *"Given coins and an amount, return the fewest coins that make it, or -1."* — LeetCode 322, the standard.
- *"Why can't you just take the largest coin first?"* — the greedy question, and it always comes.
- *"Now count how many different combinations make the amount."* — LeetCode 518.
- *"Does the order of the loops matter?"* — the trap, asked directly.
- *"How is this different from yesterday's knapsack?"* — the one-character answer.
- *"What if the amount is a billion?"*

### The first ninety seconds

> "This is unbounded knapsack — each coin is available in unlimited supply — and I want to start with why it is
> not greedy, because that is the reason it needs DP at all.
>
> **Greedy means take the biggest coin that fits and repeat. With coins one, five and seven, and an amount of
> ten, greedy takes seven, then one, one, one — four coins. The right answer is five plus five, which is two.**
> The greedy step is the biggest single reduction and it leaves a remainder that only one-rupee coins can fill.
>
> **It works for Indian denominations** — one, two, five, ten, twenty, fifty — which is why the intuition feels
> so reliable. That is a property of those particular numbers, not of the method.
>
> **So, DP. The state is: `dp[t]` is the fewest coins that make exactly `t`.**
>
> **The recurrence asks what the last coin was.** If the last coin was `c`, I was at `t - c` before it, so
> `dp[t] = 1 + min(dp[t - c])` over every coin that fits. **Try every coin as the last one, take the best.**
>
> **Base case `dp[0] = 0`, everything else infinity**, meaning not yet reachable. Infinity matters: zero would
> say every amount is free, and minus one would win every `min` and poison the table. I convert to `-1` only at
> the return.
>
> **And the loop runs forwards, which is the one thing that differs from 0/1 knapsack.** Yesterday it ran
> backwards so that `dp[t - w]` held the value from before the item existed — each item once. **Today I want
> `dp[t - c]` to possibly already include this coin, because unlimited supply is exactly that.** Same six
> lines, one range reversed, and no error either way — so I say the direction out loud as I write it.
>
> **Cost is `O(coins × amount)` time and `O(amount)` space.** Twelve coins and an amount of ten thousand is
> a hundred and twenty thousand cells — instant.
>
> **The constraint I would check first is the size of the amount**, not the number of coins. At a billion the
> table is eight gigabytes and this approach does not exist."

### The follow-ups

**"Why does the loop run forwards here and backwards yesterday?"**

> "Because of what the cell I read is supposed to mean, and it is the only difference between the two problems.
>
> `dp[t] = f(dp[t], dp[t - c])`. The question is whether `dp[t - c]` should already account for the current
> item.
>
> **Backwards, from the target down, every read is from a cell to the left that this pass has not touched
> yet** — so `dp[t - w]` still holds the previous row's value, the state before this item existed. **The item
> gets used at most once.** That is 0/1.
>
> **Forwards, `dp[t - c]` may already have been updated by this same pass** — meaning it already counts this
> coin. Adding the coin again uses it twice, and again, and again. **That is unlimited supply**, and it is
> exactly what I want today.
>
> **Concretely: one coin of three, amount nine, forwards.** `dp[3]` becomes 1 from `dp[0]`. Then `dp[6]`
> becomes 2 from `dp[3]`, which I just set. Then `dp[9]` becomes 3. **Three coins of three, from one coin.**
>
> **Backwards on the same input gives infinity** — impossible — because each pass can only use the coin once.
>
> **Neither raises an error.** Both are correct programs; they solve different problems. Which is why I state
> the direction and its reason while writing rather than after, and why I would test with an input that needs a
> repeat — because a test where the answer uses each coin once passes under both."

**"Now count how many combinations make the amount. Does the loop order matter?"**

> "It matters enormously, and it is not the direction this time — it is **which loop is on the outside**.
>
> The counting version is the same table with `+=` instead of `min`, and the base case becomes `ways[0] = 1`
> instead of `0`: **there is exactly one way to make nothing, which is to take no coins**, and every count is
> built by adding that one up.
>
> **Coins outside, amounts inside, counts combinations.** Coin one is fully processed before coin two is
> considered at all, so no arrangement can place a one after a two — **each set is counted exactly once.**
>
> **Amounts outside, coins inside, counts permutations.** Every coin is offered at every amount, so one-then-two
> and two-then-one are both formed and both counted.
>
> **Coins one and two, amount three.** Combinations: `1+1+1` and `1+2` — **two.** Permutations: `1+1+1`, `1+2`,
> `2+1` — **three.**
>
> **Both are correct programs for different questions**, and there is no error to tell them apart — the answer
> is just a different number. **Coin Change II wants combinations. Combination Sum IV wants permutations**,
> despite its name, which is worth remembering precisely because the name points the wrong way.
>
> **So I read the problem's examples before writing the loops**, every time. If the examples list `{1,2}` once,
> it is combinations; if they list it twice, it is permutations.
>
> **One more thing:** the permutation count grows very fast and problems usually ask for it modulo `10^9 + 7`.
> Python integers are unbounded so I would not notice, but in Java it wraps silently."

**"The amount is a billion. Now what?"**

> "Then this table does not exist, and I would say so before writing anything.
>
> **The table is `amount + 1` cells.** A billion cells is about eight gigabytes for the Python list of
> pointers alone, and it raises `MemoryError` before the first comparison. And the time is twelve billion
> operations — hours.
>
> **This is pseudo-polynomial**, the same point as subset sum: `amount` is a *value* in the input, not a size.
> Writing a billion down takes thirty bits, so the input is tiny and the running time is `2^30`. **Exponential
> in the input size.**
>
> **What I would do instead depends on the coins.**
>
> **If the denominations are the canonical kind — one, two, five, ten and so on — greedy is provably optimal**
> and runs in the number of coins, regardless of the amount. There is a known check for whether a system is
> canonical, and for the fixed real-world sets it simply is. **So: verify the system is canonical, then use
> greedy, and the billion stops mattering.**
>
> **If the coins are arbitrary, there is a number-theoretic route.** Above a threshold — the Frobenius number
> for the coin set — every amount is representable, and the optimal solution for a large amount is the optimal
> solution for `amount mod L` plus a pile of the most efficient coin, where `L` is the least common multiple of
> the denominations. **So I solve the small residue problem with DP and add the rest arithmetically.** That is
> genuinely harder and I would only reach for it if the constraints forced me to.
>
> **And if it is minimum coins with few coins and a small answer, BFS wins** — each amount is a node, each coin
> an edge of weight one, and BFS stops at the first level that reaches the amount. With coins one and five
> thousand and an amount of ten thousand, the DP fills ten thousand cells and BFS explores about four nodes.
>
> **The general point is that the constraint on the amount decides the algorithm**, which is the reverse of
> most problems, and it is the first thing I check."

### The model answer

*"You are writing the change-dispensing logic for a vending machine. Given the coins it holds and the change
owed, return the fewest coins to dispense, or say it cannot make exact change."*

> "Let me be explicit about one assumption first, because it changes the algorithm: **do I have unlimited coins
> of each denomination, or a finite number in the hopper?** A real vending machine has a finite count, which
> makes this bounded knapsack. **I will solve the unlimited version, which is the standard problem, and then
> say what changes.**
>
> **Why not greedy, first, because that is what a vending machine would naively do.** Take the biggest coin
> that fits, repeat. **With coins one, five and seven and change of ten, greedy gives seven-one-one-one — four
> coins — and the answer is five-five, two.** For Indian or US denominations greedy happens to be optimal, so
> it works until the machine is deployed somewhere the coins differ, and then it quietly dispenses twice as
> many coins as it needs. **That is a bug that only shows up in one country.**
>
> **The DP. `dp[t]` is the fewest coins making exactly `t`.** `dp[0] = 0` — no coins make nothing. Everything
> else starts at infinity, meaning unreachable.
>
> **For each coin, going forwards from the coin's value up to the amount, `dp[t] = min(dp[t], dp[t - coin] +
> 1)`.** Forwards, because a coin is reusable and `dp[t - coin]` should be allowed to already include it.
> Backwards would silently solve the each-coin-once problem, and with coins of three and change of nine it
> would report impossible.
>
> **At the end, if `dp[amount]` is still infinity, exact change cannot be made** — coins of two and change of
> three, for instance — and the machine should say so rather than dispense something close.
>
> **Cost: `O(coins × amount)` time, `O(amount)` space.** Six denominations and change up to a hundred rupees in
> paise is six hundred cells. Nothing.
>
> **And I would keep the reconstruction**, because a vending machine has to actually dispense the coins, not
> just count them. **One extra array recording the last coin used for each amount**, then walk back from the
> amount subtracting coins until zero. `O(amount)` extra space, which is cheap here — unlike the 0/1 case,
> where reconstruction needs the whole table.
>
> **Now the finite-hopper version, which is the real machine.** Each denomination has a count, so it is bounded
> knapsack: either expand each coin into `count` separate items and run the 0/1 version — simple, and it costs
> `O(total_coins × amount)` — or add a dimension for how many of each coin remain. **I would expand, because
> hopper counts are small, and say that if they were large I would use the binary-splitting trick: represent a
> count of thirteen as items of one, two, four and six, which can form any total from zero to thirteen in
> `log` items rather than thirteen.**
>
> **Two operational things I would raise**, because they are what actually breaks. **The hopper runs out
> mid-transaction**, so the count must be read at the start and the dispense must be atomic — decide the full
> set of coins before releasing any. **And the machine should prefer to keep small coins**, because running out
> of ones makes many later amounts impossible; so the real objective might be 'fewest coins, tie-broken by
> preserving small denominations', which is a second value in the same table rather than a different
> algorithm."

---

## 9. Recall card

**Unbounded knapsack is 0/1 with the inner loop forwards.** `range(coin, amount + 1)` so `dp[t - coin]` may
already include this coin — that *is* unlimited supply. Backwards means each item once. **One range reversed,
two different problems, no error either way** — say the direction out loud as you write it.

**Minimum coins: `dp[t] = 1 + min(dp[t - c])` over coins that fit.** Base `dp[0] = 0`, rest **`float('inf')`** —
zero makes every amount free, `-1` wins every `min`. Convert to `-1` only at the return, and check for infinity
*before* `int()`, which raises `OverflowError`.

**Greedy is wrong: coins `[1,5,7]`, amount 10 → greedy 4 (`7+1+1+1`), optimal 2 (`5+5`).** It is correct for
canonical systems like Indian denominations, which is why nobody notices.

**Counting: `ways[0] = 1`, `+=` instead of `min`, and the loop order decides the question.** Coins outside =
**combinations** (`[1,2]`→3 gives 2); amount outside = **permutations** (gives 3). Coin Change II wants
combinations; Combination Sum IV wants permutations despite its name. Read the examples.

**`O(coins × amount)` time, `O(amount)` space** — pseudo-polynomial, so **the size of the amount, not the
number of coins, decides whether this works.** Reconstruction is cheap here: one array of last-coin-used.
**Minimum coins is also a BFS** over amounts with unit edges, and it wins hugely when the answer is small and
the amount is large.
