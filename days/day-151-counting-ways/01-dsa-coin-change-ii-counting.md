---
day: 151
track: dsa
title: "Coin Change II: counting"
phase: "Dynamic programming"
status: written
---

# Coin Change II: counting

## 1. What this is, and why they ask it

Yesterday you found the *best* answer. Today you count *how many* answers there are.

**That is a different question and it needs a different discipline.** Minimising is forgiving — if two paths
reach the same amount, taking either one gives the same minimum, so double-counting is invisible. **Counting is
not forgiving.** If two paths reach the same amount and you count both, the answer is wrong, and the only
symptom is a number that is too large.

They ask counting problems because **they are where DP stops being mechanical.** The recurrence is easy. The
hard part is answering one question precisely: *am I counting sets or sequences?* Get that wrong and you
produce a correct program that answers a different question, with no error to warn you.

The other reason is that counting is where **overcounting and undercounting are both silent**. There is no
`IndexError`, no exception, no crash — just a number. A candidate who can say "I count combinations, and I
know this because the coin loop is outside" is demonstrating exactly the care the problem is testing for.

By the end of this lesson you can count combinations and permutations and say which is which, explain the loop
nesting from first principles, handle the modulus correctly, and recognise the counting family — ways to climb
stairs, ways to decode a string, ways to reach a cell.

---

## 2. The story

Bhanumati had been making the same four things for the wedding season for eleven years and the argument was
always about the boxes.

Two hundred boxes. Four sweets. And the family who ordered them always said the same sentence, which was
**"make sure they are not all the same."**

So she and her daughter sat down the week before, as they did every year, and worked out what could go in a
box, and every year it took the whole evening because they kept losing count.

The rule was simple. Six pieces in a box. Any mix of the four kinds.

Her daughter started listing. Six laddoos. Five laddoos and a barfi. Five laddoos and a peda. Four laddoos and
two barfis. Four laddoos, one barfi, one peda —

**"You said that one."**

She had not. She had said four laddoos, one peda, one barfi, twenty minutes earlier, and it had gone on the
list as a separate line, and it was the same box.

**Because a box is not a sequence. Nobody opens a box and finds the sweets in an order.**

They started again with a rule Bhanumati made up on the spot, and it was the rule that finally worked.
**"Decide all the laddoos first. Every box, all of them. Then move to barfi and never go back."**

So: how many laddoos — six, five, four, down to none. **Then** for each of those, how many barfis. **Then**
pedas. **Then** whatever is left is the last kind.

And because they never went back to laddoos after starting on barfi, **there was no way to write down the same
box twice.** The order was fixed by the method, not by the box.

The daughter, who was seventeen and argumentative, pointed out that this was a completely different question
from the one the shop next door had to answer, because next door made a plate where the sweets were laid out
in a row and **there the order was the whole point** — laddoo-barfi-laddoo was a different plate from
laddoo-laddoo-barfi, and they were paid for the arrangement.

**Same six sweets. Same four kinds. Two completely different numbers.**

---

## 3. The idea in plain English

Bhanumati's rule is the loop nesting, and her daughter has just stated the entire lesson.

**Two questions look identical and are not:**

- **Combinations.** *How many different sets of coins make the amount?* `{1, 2}` is one answer. Order does not
  exist. **The box.**
- **Permutations.** *How many different sequences of coins make the amount?* `1 then 2` and `2 then 1` are two
  answers. **The plate.**

**Coin Change II asks for combinations.** Climbing stairs asks for permutations — taking a 1-step then a
2-step is a genuinely different way to climb than 2 then 1. **Combination Sum IV asks for permutations despite
its name**, which is the most reliably misleading title on LeetCode.

**The code for both is the same six lines, with the two loops swapped.**

```python
# COMBINATIONS — coins outside
for coin in coins:
    for t in range(coin, amount + 1):
        ways[t] += ways[t - coin]

# PERMUTATIONS — amount outside
for t in range(1, amount + 1):
    for coin in coins:
        if coin <= t:
            ways[t] += ways[t - coin]
```

**Why coins-outside counts each set once**, said the way Bhanumati said it: **coin 1 is completely finished
before coin 2 is ever considered.** By the time the algorithm looks at 2, every count in the table describes
using only 1s. Adding a 2 extends those, and there is no route back to adding a 1 afterwards. **The coin order
is imposed by the loop, so every set is built in exactly one order and counted exactly once.**

**Why amount-outside counts sequences**, said the same way: **at every amount, every coin is offered.** So
`ways[3]` is built from `ways[2]` (add a 1) and from `ways[1]` (add a 2), and those two routes describe
`1,1,1` / `1,2` and `2,1` — the last coin is what distinguishes them, so orderings are separate.

**The base case is `ways[0] = 1` in both**, and this is the line that carries the meaning. **There is exactly
one way to make nothing: take no coins.** Every other count is that `1` propagated forwards. Set it to zero
and the entire table is zero.

**And the counting family is larger than coins.** Once you see the shape, these are all the same problem:

```
climbing stairs           coins = [1, 2], count PERMUTATIONS
                          (1-then-2 is a different climb from 2-then-1)
ways to decode "226"      coins are "take 1 digit" or "take 2", with validity
unique paths in a grid    ways[cell] = ways[above] + ways[left]
ways to make change       coins = denominations, COMBINATIONS
dice roll sums            coins = [1..6], PERMUTATIONS, with a count limit
```

**The recurrence is always the same sentence: sum over every last move.** What differs is what a move is, and
whether moves are ordered.

**Two mechanical things that matter more in counting than anywhere else.**

**The modulus.** Counts grow fast — genuinely fast. The number of ways to make 5,000 from coins 1 to 200 has
hundreds of digits. **Problems ask for the answer modulo `10^9 + 7`**, and the rule is to take the modulus at
every addition, not at the end. In Python nothing overflows so forgetting it merely makes things slow; **in
Java or C++ it wraps silently and the answer is wrong.**

**And the sanity check that catches almost every counting bug: run it on a tiny input you can enumerate by
hand.** Coins `[1, 2]`, amount 3. Two combinations, three permutations. **If your program says 3 when you wanted
combinations, your loops are the wrong way round** — and that six-second test is worth more than re-reading the
code.

---

## 4. The picture

The two nestings on the same input, filled in step by step:

```
  coins [1, 2], amount 3

  COMBINATIONS — coins outside
     start:            ways = [1, 0, 0, 0]
     process coin 1:   ways = [1, 1, 1, 1]     only 1s exist yet
     process coin 2:   ways[2] += ways[0] -> 2
                       ways[3] += ways[1] -> 2
                       ways = [1, 1, 2, 2]
     answer 2:  {1,1,1}  {1,2}

  PERMUTATIONS — amount outside
     start:            ways = [1, 0, 0, 0]
     t=1: +coin1       ways[1] = ways[0]            = 1
     t=2: +coin1 +coin2 ways[2] = ways[1] + ways[0] = 2
     t=3: +coin1 +coin2 ways[3] = ways[2] + ways[1] = 3
                       ways = [1, 1, 2, 3]
     answer 3:  {1,1,1}  {1,2}  {2,1}

  Same six lines. Two loops swapped. 2 against 3.
```

Why coins-outside cannot produce `2+1`:

```
  TIME -->

  coins outside:
    [--------- all of coin 1 --------][--------- all of coin 2 --------]
                                       ^
    by the time coin 2 is used, no more 1s will EVER be added.
    So every set is built as: (some 1s) then (some 2s).
    ONE canonical order per set. Counted once.

  amount outside:
    t=1: [coin1][coin2]
    t=2: [coin1][coin2]
    t=3: [coin1][coin2]
             ^
    a 1 can follow a 2 and a 2 can follow a 1.
    Both orders exist in the table. Counted separately.
```

Bhanumati's box, as the loop:

```
  6 sweets, kinds L B P K

  laddoos: 6 5 4 3 2 1 0        <- decide ALL of these first
             |
             +-- barfis: 0..(6 - laddoos)   <- never go back to laddoos
                   |
                   +-- pedas: 0..(what's left)
                         |
                         +-- kaju: whatever remains

  (4,1,1,0) is reached exactly once, via laddoo=4, barfi=1, peda=1.
  There is no path that places the peda before the barfi,
  because the loop order forbids it.
```

The counting recurrence as a tree, showing the sum:

```
                  ways(3)
        /            |            \
   last coin 1   last coin 2   last coin 3
   ways(2)       ways(1)       ways(0)=1
    / \            |
  ...             ...

  ways(t) = SUM over every possible LAST move of ways(t - move)

  Minimising took the BEST child. Counting ADDS ALL of them.
  That is the whole difference, and it is why double-counting
  is invisible when minimising and fatal when counting.
```

---

## 5. The code, built step by step

### Combinations, from the sentence

```python
def change(amount: int, coins: list[int]) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1                               # one way to make nothing
    return ways[amount]                       # (loops next)
```

**`ways[0] = 1` is the seed.** Every count in the finished table is that single `1`, propagated forwards
through additions. Set it to `0` and the whole table stays zero.

```python
    for coin in coins:                        # OUTSIDE: fixes the coin order
        for t in range(coin, amount + 1):
            ways[t] += ways[t - coin]
```

**Coins outside. Say it out loud as you write it: "coins outside, so this counts combinations."**

`range(coin, ...)` starts at the coin's value, which removes the need for a `coin <= t` guard.

### Permutations, for contrast

```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    ways = [0] * (target + 1)
    ways[0] = 1
    for t in range(1, target + 1):            # OUTSIDE: every coin at every amount
        for number in nums:
            if number <= t:
                ways[t] += ways[t - number]
    return ways[target]
```

**The guard comes back**, because the inner loop is now over numbers rather than over amounts, so `t - number`
can go negative.

### The modulus, done correctly

```python
MOD = 10**9 + 7

def change_mod(amount: int, coins: list[int]) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1
    for coin in coins:
        for t in range(coin, amount + 1):
            ways[t] = (ways[t] + ways[t - coin]) % MOD    # at EVERY addition
    return ways[amount]
```

**At every addition, not at the end.** Taking it once at the return gives the right answer in Python — where
integers never overflow — and the wrong answer in every other language, where the intermediate value has
already wrapped.

### Climbing stairs, which is permutations in disguise

```python
def climb_stairs(n: int) -> int:
    ways = [0] * (n + 1)
    ways[0] = 1
    for t in range(1, n + 1):                 # amount outside -> permutations
        for step in (1, 2):
            if step <= t:
                ways[t] += ways[t - step]
    return ways[n]
```

**Stairs is permutations and that is correct**, because stepping 1-then-2 is a genuinely different climb from
2-then-1. **The problem's meaning decides the nesting**, not a rule you memorise.

**And this is Fibonacci** — `ways[t] = ways[t-1] + ways[t-2]` — which is a nice thing to notice out loud.

### Decode ways, where the moves have conditions

```python
def num_decodings(s: str) -> int:
    n = len(s)
    ways = [0] * (n + 1)
    ways[0] = 1                               # one way to decode nothing
    for i in range(1, n + 1):
        if s[i - 1] != '0':                   # take one digit: 1-9
            ways[i] += ways[i - 1]
        if i >= 2 and '10' <= s[i - 2:i] <= '26':   # take two digits: 10-26
            ways[i] += ways[i - 2]
    return ways[n]
```

**The same sum-over-last-moves**, with exactly two moves and a validity condition on each. **`'0'` alone is not
a letter**, and `'06'` is not a valid two-digit code — which is why the string comparison starts at `'10'`.

### Unique paths, which is counting on a grid

```python
def unique_paths(rows: int, cols: int) -> int:
    ways = [1] * cols                         # top row: one way to each cell
    for _ in range(1, rows):
        for c in range(1, cols):
            ways[c] += ways[c - 1]            # from above (ways[c]) + from left
    return ways[-1]
```

**One row of state**, because `ways[c]` before the update is the cell above and `ways[c-1]` is the cell to the
left. **The same forwards-in-place trick as unbounded knapsack**, doing a different job.

### The complete solution

```python
"""Counting problems: combinations, permutations, and the family."""

MOD = 10**9 + 7


def change(amount: int, coins: list[int]) -> int:
    """How many COMBINATIONS of coins make amount. Coins outside."""
    ways = [0] * (amount + 1)
    ways[0] = 1                               # exactly one way to make nothing
    for coin in coins:                        # each coin fully processed in turn
        for t in range(coin, amount + 1):
            ways[t] += ways[t - coin]
    return ways[amount]


def change_mod(amount: int, coins: list[int]) -> int:
    """The same, taking the modulus at every addition."""
    ways = [0] * (amount + 1)
    ways[0] = 1
    for coin in coins:
        for t in range(coin, amount + 1):
            ways[t] = (ways[t] + ways[t - coin]) % MOD
    return ways[amount]


def combination_sum_iv(nums: list[int], target: int) -> int:
    """How many PERMUTATIONS make target. Amount outside. (Name is misleading.)"""
    ways = [0] * (target + 1)
    ways[0] = 1
    for t in range(1, target + 1):            # every number offered at every t
        for number in nums:
            if number <= t:
                ways[t] += ways[t - number]
    return ways[target]


def change_with_lists(amount: int, coins: list[int]) -> list[list[int]]:
    """The actual combinations, for checking small cases by eye."""
    result: list[list[int]] = []

    def build(index: int, left: int, current: list[int]) -> None:
        if left == 0:
            result.append(current[:])
            return
        if index == len(coins):
            return
        build(index + 1, left, current)                  # skip this coin
        if coins[index] <= left:
            current.append(coins[index])
            build(index, left - coins[index], current)   # reuse it
            current.pop()

    build(0, amount, [])
    return result


def climb_stairs(n: int) -> int:
    """Permutations of 1s and 2s. 1-then-2 differs from 2-then-1."""
    ways = [0] * (n + 1)
    ways[0] = 1
    for t in range(1, n + 1):
        for step in (1, 2):
            if step <= t:
                ways[t] += ways[t - step]
    return ways[n]


def num_decodings(s: str) -> int:
    """Sum over last moves, where a move is 1 digit (1-9) or 2 digits (10-26)."""
    n = len(s)
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        if s[i - 1] != '0':
            ways[i] += ways[i - 1]
        if i >= 2 and '10' <= s[i - 2:i] <= '26':
            ways[i] += ways[i - 2]
    return ways[n]


def unique_paths(rows: int, cols: int) -> int:
    """ways[cell] = ways[above] + ways[left], one row of state."""
    ways = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            ways[c] += ways[c - 1]
    return ways[-1]


if __name__ == "__main__":
    print("combinations [1,2] -> 3 :", change(3, [1, 2]))
    print("permutations [1,2] -> 3 :", combination_sum_iv([1, 2], 3))
    print("the combinations        :", change_with_lists(3, [1, 2]))

    print("combinations [1,2,5]->5 :", change(5, [1, 2, 5]))
    print("the combinations        :", change_with_lists(5, [1, 2, 5]))
    print("impossible [2] -> 3     :", change(3, [2]))

    print("climb 5 stairs          :", climb_stairs(5))
    print("decode '226'            :", num_decodings("226"))
    print("decode '06'             :", num_decodings("06"))
    print("paths 3x7               :", unique_paths(3, 7))

    big = change_mod(5000, list(range(1, 201)))
    print("ways to make 5000 mod   :", big)
    print("digits without the mod  :", len(str(change(5000, list(range(1, 201))))))
```

Run it and you get:

```
combinations [1,2] -> 3 : 2
permutations [1,2] -> 3 : 3
the combinations        : [[1, 2], [1, 1, 1]]
combinations [1,2,5]->5 : 4
the combinations        : [[5], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]
impossible [2] -> 3     : 0
climb 5 stairs          : 8
decode '226'            : 3
decode '06'             : 0
paths 3x7               : 28
ways to make 5000 mod   : 696884557
digits without the mod  : 74
```

**Line one against line two is the whole lesson**, and `change_with_lists` proves it — two lists, not three.

**And the last two lines are the modulus argument, made concrete.** The real count of ways to make 5,000 from
coins 1 to 200 has **74 digits**. In Python that is fine. In Java, a `long` holds 19 digits and the answer
wrapped around fifty digits ago.

---

## 6. What it costs

**Time.** The same two nested loops as yesterday, and identical for both nestings.

```
combinations: len(coins) x amount cells
permutations: amount x len(coins) cells

Both are O(len(coins) x amount). Swapping the loops changes the
ANSWER, not the cost.
```

**Concretely:**

```
coins = 1..200, amount = 5,000
200 x 5,000 = 1,000,000 additions
-> about 0.15 seconds in Python
```

**Space.**

```
one row of amount + 1 integers
5,001 Python ints -> about 40 KB

WITHOUT the modulus, those integers grow to 74 digits:
  a 74-digit Python int is about 60 bytes rather than 28
  -> the arithmetic itself gets slower as the numbers grow

With the modulus, every value stays under 10^9 and fits in
a machine word. The modulus is a SPEED optimisation in Python
and a CORRECTNESS requirement everywhere else.
```

**How fast counts actually grow:**

```
ways to make 100 from coins 1..10          =  6,292,069        7 digits
ways to make 1,000 from coins 1..100       =  ~10^31          32 digits
ways to make 5,000 from coins 1..200       =  ~10^73          74 digits

a Java long holds up to  9,223,372,036,854,775,807   19 digits
-> overflows well before amount 1,000, silently, with no warning
```

**The enumeration cost, for contrast** — why you count instead of listing:

```
change_with_lists(5, [1,2,5])   -> 4 lists, instant
change_with_lists(100, [1..10]) -> 6,292,069 lists

  each list averages ~20 integers
  6,292,069 x 20 x 28 bytes  = ~3.5 GB

The COUNT is one integer. The LIST is three and a half gigabytes.
That gap is why counting is a separate problem from generating.
```

**The two nestings compared on real numbers:**

```
coins [1, 2, 5], amount 11
  combinations: 11
  permutations: 218

amount 30
  combinations: 58
  permutations: 5,508,222

Permutations explode because order multiplies. If your answer is
enormous and you expected a small one, check the nesting first.
```

**That last line is a genuinely useful debugging heuristic**, and it is faster than reading the loops.

---

## 7. The traps

**The swapped nesting, which produces a correct program answering the wrong question.**

```python
>>> ways = [0] * 4; ways[0] = 1
>>> for t in range(1, 4):                    # amount outside
...     for coin in [1, 2]:
...         if coin <= t:
...             ways[t] += ways[t - coin]
>>> ways[3]
3
```

Against the combinations answer of `2`. **No error, no warning, and both numbers look reasonable.** The only
defence is the hand-check: `[1,2]` to 3 is **2 combinations, 3 permutations**, and if you know that pair you
catch this in six seconds.

**Forgetting `ways[0] = 1`.**

```python
>>> ways = [0] * 6
>>> for coin in [1, 2]:
...     for t in range(coin, 6):
...         ways[t] += ways[t - coin]
>>> ways
[0, 0, 0, 0, 0, 0]
```

**Every count is zero**, because nothing was ever `1` to add up. **It reads as "no way to make this amount"**
rather than as a bug, which is what makes it survive review.

**Using the 0/1 direction by habit.**

```python
>>> ways = [0] * 6; ways[0] = 1
>>> for coin in [1, 2]:
...     for t in range(5, coin - 1, -1):     # backwards
...         ways[t] += ways[t - coin]
>>> ways[5]
0
```

**Zero ways to make 5 from 1s and 2s**, when there are three. Backwards means each coin is usable at most
once, so the only totals reachable at all are 1, 2 and 3 — and 5 is not among them. **It reads as
"impossible" rather than as a bug**, which is exactly how it survives review.

**Taking the modulus only at the end.**

```java
// Java
long[] ways = new long[amount + 1];
ways[0] = 1;
for (int coin : coins)
    for (int t = coin; t <= amount; t++)
        ways[t] += ways[t - coin];          // no modulus here
return (int)(ways[amount] % 1_000_000_007); // too late
```

**The intermediate values already overflowed.** A `long` wraps at about 9.2 × 10^18, and once it wraps the
subsequent additions are meaningless — the final modulus is applied to garbage. **In Python this cannot happen,
which makes it easy to forget when you switch languages.**

**Applying the modulus when the problem asked for the real number.**

```python
>>> change_mod(5000, list(range(1, 201)))
696884557
```

**A perfectly plausible-looking answer that is not the count.** If a problem does not mention a modulus, do not
add one — and if the expected answer fits in the language's integer type, the modulus is wrong, not merely
unnecessary.

**Counting permutations when the problem wants combinations, on a large input.**

```python
>>> change(30, [1, 2, 5])
58
>>> combination_sum_iv([1, 2, 5], 30)
5508222
```

**Five orders of magnitude apart.** If your answer is enormous and the expected one is small, the nesting is
the first thing to check.

**A zero coin, which gives an answer rather than an error.**

```python
>>> change(3, [0, 1])
2
```

**Two, when the true answer is infinite** — a coin of zero can be inserted any number of times, so there are
infinitely many combinations and the question has no answer. What the code does instead is
`ways[t] += ways[t - 0]`, which doubles each cell once and then propagates that, giving a finite number with
no meaning. **Validate the denominations**: every coin must be positive, and that is one `if` at the top.

**Very large amounts.**

```python
>>> ways = [0] * (10**9 + 1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**Same pseudo-polynomial ceiling as the last two days.** The table is indexed by the amount, so the amount's
magnitude decides whether the approach exists.

---

## 8. In the interview

### How it gets asked

- *"How many combinations of coins make the amount?"* — LeetCode 518, the standard.
- *"Does the order of the loops matter?"* — asked directly, and it is the whole point.
- *"Now count sequences instead of sets."* — LeetCode 377.
- *"How many ways can you climb `n` stairs taking 1 or 2 at a time?"* — permutations, and it is Fibonacci.
- *"Why the modulus?"*
- *"Can you list them instead of counting them?"*

### The first ninety seconds

> "Before I write anything I want to settle one question, because it changes the answer and not the code:
> **am I counting sets or sequences?**
>
> **With coins one and two making three:** the sets are `{1,1,1}` and `{1,2}` — **two.** The sequences are
> `1,1,1`, `1,2` and `2,1` — **three.** Coin Change II wants sets, so **two**.
>
> **The state is: `ways[t]` is the number of ways to make exactly `t`.**
>
> **The base case is `ways[0] = 1` — there is exactly one way to make nothing, which is to take no coins.**
> That single one is the seed; every other count in the table is it, propagated forwards through additions. If
> I set it to zero the entire table stays zero and the program reports that nothing is makeable.
>
> **The recurrence is: sum over every possible last coin.** `ways[t] += ways[t - coin]`. Minimising took the
> best child; counting adds all of them, and that is the real difference — **when minimising, reaching the same
> state twice is harmless, and when counting it is fatal.**
>
> **So the nesting. Coins on the outside, amounts on the inside, and that is what makes it count sets.**
> Coin one is completely processed before coin two is ever considered, so every combination is built in one
> fixed order — all the ones, then all the twos — and there is no path that adds a one after a two. **One
> canonical order per set, so each set is counted exactly once.**
>
> **Swap the loops and every coin is offered at every amount**, so a one can follow a two and a two can follow
> a one, and I count sequences instead. **Both are correct programs. They answer different questions, and
> there is no error to tell them apart** — just a different number.
>
> **Cost is `O(coins × amount)` time and `O(amount)` space**, identical for both nestings — swapping the loops
> changes the answer, not the cost.
>
> **And the check I would actually run: coins one and two, amount three.** If it says three, my loops are the
> wrong way round."

### The follow-ups

**"Explain why the loop order changes the answer."**

> "It is about which orderings the algorithm is capable of building, and the loop imposes that.
>
> **Coins outside.** The algorithm processes coin one entirely — every amount from one to the target — and then
> moves to coin two and never returns. **So by the time a two is ever added, no more ones will ever be added
> after it.** Every combination therefore gets built in exactly one order: all its ones, then all its twos,
> then all its fives. **A canonical order, imposed by the loop, so each set is reached by exactly one path and
> counted once.**
>
> **Amounts outside.** At every amount, every coin is offered. So `ways[3]` gets a contribution from `ways[2]`
> by adding a one, and from `ways[1]` by adding a two. **Those describe two different last moves**, and
> `1,1,1` / `1,2` come from the first while `2,1` comes from the second. Orderings are distinguished, so they
> are counted separately.
>
> **The way I would put it in one sentence: coins-outside fixes an order and counts each set once;
> amounts-outside lets every order happen and counts each one.**
>
> **And there is a debugging heuristic worth knowing.** Permutations explode much faster than combinations,
> because order multiplies. Coins one, two and five to thirty: **fifty-eight combinations, five and a half
> million permutations.** So if my answer is enormous and I expected a small one, the nesting is the first thing I
> check — faster than re-reading the loops.
>
> **The sanity test is coins one and two, amount three: two against three.** Six seconds, and it catches this
> every time."

**"Why the modulus, and where exactly does it go?"**

> "Because the counts get genuinely enormous, and in most languages they overflow silently.
>
> **The number of ways to make five thousand from coins one to two hundred has seventy-four digits.** A
> Java `long` holds nineteen. So the answer wrapped around seventy digits before it finished, and everything
> after that point is meaningless.
>
> **`10^9 + 7` is the usual modulus because it is prime and its square fits in a 64-bit integer** — so you can
> multiply two reduced values without overflowing, which matters in problems that multiply. Here I only add,
> so the requirement is just that two reduced values sum without overflowing, which any modulus around a
> billion satisfies.
>
> **It goes at every addition, not at the end.** `ways[t] = (ways[t] + ways[t - coin]) % MOD`. If I only take
> it at the return, the intermediate values have already wrapped and I am applying a modulus to garbage.
>
> **Python is the trap here**, because integers never overflow, so the version with the modulus only at the end
> gives the right answer and I would not notice the bug until I wrote the same code in Java. **What the modulus
> does buy in Python is speed** — a ninety-one-digit integer is slower to add than a machine word, so the
> modulus keeps the arithmetic fast.
>
> **And the reverse mistake matters too: do not add a modulus the problem did not ask for.** If the expected
> answer fits in the language's integer type, a modulus produces a plausible-looking number that is simply
> wrong."

**"Could you list the combinations instead of counting them?"**

> "Yes, and it is a different algorithm with a completely different cost, which is the interesting part.
>
> **Counting is DP: one table, one integer per amount, `O(coins × amount)`.**
>
> **Listing is backtracking**, and no table helps, because the output itself is the size of the answer. I would
> recurse with an index and a remaining amount, and at each step either skip the current coin — moving to the
> next index — or take it and stay at the same index, since coins are reusable. **Staying at the same index on
> a take and never going back is the same canonical-order trick as coins-outside**, and it is what stops the
> same combination being emitted twice.
>
> **The cost difference is the point.** The number of ways to make a hundred from coins one to ten is about
> **six point three million**. As a count, that is one integer. As a list, each combination averages about
> twenty numbers, so it is roughly **three and a half gigabytes** of output. **Same problem, one integer
> against three and a half gigabytes.**
>
> **So the practical answer is: list only when the count is small, and check the count first.** If an interview
> asks me to enumerate, I would say that out loud — run the counting version, and if the answer is in the
> thousands, enumerate; if it is in the millions, ask what they actually want to do with them, because they
> almost certainly want the count, or the top few by some criterion, rather than all of them.
>
> **And if they want just one combination rather than all of them**, that is a third algorithm again — keep a
> parent pointer during the DP and walk back, which is `O(amount)` extra space and gives one answer
> immediately."

### The model answer

*"A vending machine has to report, for a given price, how many distinct ways a customer could pay it using the
denominations the machine accepts. Design and implement it."*

> "The first thing I want to pin down is what 'distinct ways' means, because there are two reasonable readings
> and they give different numbers.
>
> **Does inserting a five then a two count as different from a two then a five?** For a vending machine I would
> say no — the customer paid two coins, and the order they went in is not part of the answer. **So:
> combinations, not permutations.** I would state that assumption explicitly, because if the machine were
> logging insertion sequences the answer would be different.
>
> **Concretely, with coins of one and two and a price of three: two ways** — three ones, or a one and a two.
> Not three.
>
> **The state: `ways[t]` is the number of distinct sets of coins that total exactly `t`.**
>
> **Base case `ways[0] = 1`** — one way to pay nothing, by inserting nothing — and that single one is what
> every other count is built from.
>
> **Recurrence: sum over every possible last coin.** For each coin, going forwards from the coin's value to the
> price, `ways[t] += ways[t - coin]`. **Forwards because coins are reusable** — a customer can insert three
> ones — which is the unbounded direction, not the each-coin-once direction.
>
> **And the coin loop is on the outside.** That is the decision that makes it count sets: coin one is fully
> processed before coin two is considered, so every set is built as all-the-ones-then-all-the-twos, in one
> fixed order, and counted exactly once. **Swapping those loops would count insertion sequences instead**, and
> nothing would report the difference — so I would say the nesting out loud while writing it, and test with
> one-and-two-to-three, which must give two.
>
> **Cost: `O(denominations × price)` time, `O(price)` space.** Six denominations and a price of a hundred
> rupees expressed in rupees is six hundred additions. Instant, and I could precompute the whole table once at
> startup since the denominations do not change.
>
> **Two things about the numbers.** For realistic vending-machine prices the counts are small — tens or
> hundreds — so **no modulus**, and I would not add one, because a modulus the problem did not ask for turns a
> correct answer into a plausible wrong one. **If the price were in paise and the denominations were fine, the
> counts would grow fast**, and then I would ask whether the answer needs to be exact.
>
> **What I would flag as the real-world gap:** this counts ways ignoring how many coins the machine actually
> holds. **A real machine has a finite hopper**, so 'you could pay with a hundred one-rupee coins' is not a
> real option if the customer does not have a hundred coins. **If the question is about what the customer can
> do, this is right; if it is about what the machine can accept, there is a per-coin limit and it becomes
> bounded rather than unbounded** — either expand each coin into its available count and run the each-coin-once
> version, or add a dimension for coins remaining.
>
> **And if they asked me to list the ways rather than count them**, that is backtracking, not DP, and the
> output can be enormous — eight point seven million combinations for a hundred from coins one to ten, about
> three and a half gigabytes. **I would count first and only enumerate if the count is small.**"

---

## 9. Recall card

**Counting is unforgiving where minimising is not:** two paths to the same state are harmless for `min` and
fatal for a count. The recurrence is always **sum over every possible last move**, and the base case is always
**`ways[0] = 1`** — one way to make nothing — which is the seed every count grows from.

**The loop nesting decides the question, and both versions are correct programs.** Coins outside =
**combinations** (each coin fully processed before the next, so every set is built in one canonical order);
amount outside = **permutations** (every coin offered at every amount, so orderings separate). **`[1,2]` to 3
gives 2 and 3** — that six-second hand-check catches the mistake every time.

**Coin Change II wants combinations. Combination Sum IV wants permutations despite its name. Climbing stairs
wants permutations** (1-then-2 is a different climb) and is Fibonacci.

**Permutations explode**: coins `[1,2,5]` to 30 is **58 combinations against 5,508,222 permutations** — so an
answer far larger than expected means the nesting, before anything else.

**Modulus at every addition, never only at the end** — ways to make 5,000 from coins 1–200 has **74 digits**
and a Java `long` holds 19. `10^9 + 7` because it is prime and its square fits in 64 bits. **In Python nothing
overflows, so the bug only appears when you port the code** — and never add a modulus the problem did not ask
for.

**Counting is one integer; listing is backtracking and can be gigabytes** (6.3M combinations ≈ 3.5 GB). **Count
first, enumerate only if the count is small.**
