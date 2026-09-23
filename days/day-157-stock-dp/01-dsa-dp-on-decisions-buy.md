---
day: 157
track: dsa
title: "DP on decisions: buy and sell stock"
phase: "Dynamic programming"
status: written
---

# DP on decisions: buy and sell stock

## 1. What this is, and why they ask it

**You have the price of something on each of `n` days. You may buy and sell. Maximise your profit.**

That one sentence is a whole family of interview questions, and the family is the point. **One transaction.
Unlimited transactions. At most `k` transactions. With a cooldown. With a fee.** Six problems that look
different and are the same problem with the state adjusted.

They ask it because **it is the cleanest example of a state that is not a position.** Every DP so far has been
indexed by where you are — an amount, a cell, an index into a string. **Here the state is `(day, what you are
currently holding)`**, and that second component is a *mode*, not a place. Learning to say "I need a dimension
for which situation I am in" is the skill, and once you have it, the cooldown and the transaction-limit
variants follow in about a minute each.

The other reason is that **the variants are a ladder, and the interviewer walks up it.** They start with one
transaction, which greedy solves. Then unlimited, which greedy also solves and DP explains. Then `k`
transactions, where greedy dies and you need the third dimension. **A candidate who has one memorised solution
falls off the ladder at step three;** a candidate who has the state framework answers all of them from the same
starting point.

By the end of this lesson you can write the two-state machine, extend it to `k` transactions and to a cooldown
and a fee, say where the transaction count is consumed and why that must be stated, and know which variants
greedy solves.

---

## 2. The story

Sarala bought and sold gold, in very small amounts, and she was the only person in her family who understood
why she was not doing what they thought she was doing.

**The shop bought at one price and sold at another and the difference was the shop's.** Everybody knew that.
What her brother did not understand, and asked about at every function for eleven years, was why she did not
simply buy when it was cheap and sell when it was dear.

**"That is exactly what I do," she said. "The difficulty is that I only know it was cheap afterwards."**

But that was not the real difficulty, and it took her a while to be able to say what was.

**The real difficulty was that on any given morning she was in one of two situations, and they were completely
different.**

Either she had money and no gold. **Then the only question was whether to buy.**

Or she had gold and no money. **Then the only question was whether to sell.**

**And she could not do both on the same morning.** She could not sell gold she had not bought. She could not
buy again while everything she had was already gold.

Her brother said this was obvious.

**"Then tell me what I should do on Thursday."**

And he could not, because the answer depended on which of the two situations she would be in on Thursday, and
that depended on what she did on Wednesday, and Tuesday, all the way back.

There was a third thing, which came later and which she only mentioned once.

**The dealer she used had a rule that after you sold to him you could not buy from him again the next day.**
Not a real rule, just how he was. **So selling on Monday did not put her back in the buying situation on
Tuesday. It put her in a third situation — no gold, no buying — that lasted one day and then became the
ordinary one.**

Her brother, who by this point had stopped asking, said it sounded complicated.

**"It is three situations instead of two," she said. "That is all. The question on each morning is the same
question. It is just that there are three of them now."**

---

## 3. The idea in plain English

Sarala's two situations are the two states, her third one is the cooldown, and her sentence at the end is the
whole method.

**Start with the state, because it is what makes this family tractable.**

> **`dp[day][holding]` is the most money you can have at the end of `day`, given that `holding` is 1 if you
> currently own the stock and 0 if you do not.**

**That second dimension is a *mode*, not a position** — and this is the new idea. Every previous DP indexed by
where you are. **Here you also need to know what situation you are in**, because it determines which moves are
legal.

**Why the naive state fails.** `dp[day]` alone — "the best profit using the first `day` days" — cannot express
the recurrence, because **you cannot decide whether selling today is legal without knowing whether you are
holding.** Same failure as longest increasing subsequence: the state is incomplete, and it fails silently.

**The transitions are Sarala's two questions.**

**If you are not holding at the end of today, either you were not holding yesterday and did nothing, or you
were holding and sold:**

```
dp[day][0] = max( dp[day-1][0],                    do nothing
                  dp[day-1][1] + price[day] )      sell
```

**If you are holding at the end of today, either you were holding and kept it, or you were not and bought:**

```
dp[day][1] = max( dp[day-1][1],                    do nothing
                  dp[day-1][0] - price[day] )      buy
```

**Buying subtracts, selling adds.** Track *money*, not profit, and the arithmetic never confuses you.

**The base cases.** On day 0, not holding means you have zero: `dp[0][0] = 0`. Holding means you bought today:
`dp[0][1] = -price[0]`.

**And the answer is `dp[n-1][0]`, not the maximum of the two.** **Ending while still holding is never
optimal** — you paid for something and did not sell it — so the answer is always the not-holding state.

**That is the unlimited-transactions version**, LeetCode 122, and it is two lines.

**Now the ladder, and each rung changes exactly one thing.**

**At most `k` transactions.** Add a third dimension: `dp[day][transactions_used][holding]`.

**And here is the detail that must be stated out loud: where is a transaction consumed?** A transaction is a
buy and a matching sell. **Count it on the buy, or count it on the sell — either is correct, and you must pick
one and be consistent.** Counting on both halves the effective limit, which is the standard bug, and it gives a
plausible smaller number.

**One optimisation matters here.** If `k >= n/2`, you can never use more transactions than that anyway — each
one needs at least two days — **so the limit is not binding and you fall back to the unlimited version.**
Without that check, `k = 10^9` allocates a table with a billion rows and dies.

**With a cooldown.** Sarala's dealer. After selling you must wait one day before buying. **Three states instead
of two**: holding, not-holding-and-free-to-buy, and just-sold. Selling moves you into the third; the third
moves into the second the next day and nowhere else.

**With a transaction fee.** Subtract the fee once per transaction — **on the sell, conventionally, because
that is where the round trip completes.** No new dimension at all: **just a constant in one transition**,
which is worth noticing, because it is the only variant that costs nothing.

**Exactly one transaction.** The most restrictive, and greedy solves it: **track the minimum price seen so far
and the best profit against it, in one pass.** The DP also works, and the greedy version is what to write.

**Now: which variants greedy solves, because the interviewer will ask.**

**One transaction: greedy works** — min-so-far and best-difference.

**Unlimited transactions: greedy works, and the reason is neat.** Sum every positive day-to-day difference.
`sum(max(0, price[i] - price[i-1]))`. **Because with unlimited transactions, capturing every upward step is
the same as capturing every rising run** — buying and selling on consecutive days telescopes into buying at
the bottom and selling at the top.

**Two or more limited transactions: greedy fails.** There is no local rule that knows whether to spend one of
your limited transactions on a small rise now or save it for a bigger one later. **That is where the DP earns
its place**, and saying it is a better answer than writing the code.

**Cooldown and fee: greedy fails too**, for the same reason — a local decision cannot account for a cost that
falls in the future.

**Finally, the space collapse.** Every transition reads only yesterday, so **you keep a constant number of
variables**, not a table. The unlimited version becomes two variables; the cooldown version three; the
`k`-transaction version two arrays of length `k+1`. **`O(1)` or `O(k)` space instead of `O(n × k)`**, and it is
the natural way to write these once the state is clear.

---

## 4. The picture

The two-state machine:

```
                 buy: -price[day]
        +--------------------------------+
        |                                v
   [ NOT HOLDING ]                  [ HOLDING ]
    (cash in hand)                   (own the stock)
        ^                                |
        +--------------------------------+
                 sell: +price[day]

   both states also have a "do nothing" self-loop

   dp[day][0] = max( dp[day-1][0],  dp[day-1][1] + price[day] )
   dp[day][1] = max( dp[day-1][1],  dp[day-1][0] - price[day] )

   The answer is dp[n-1][0]. Ending while HOLDING is never optimal —
   you paid for something and did not sell it.
```

The table filling, for `prices = [7, 1, 5, 3, 6, 4]`, unlimited transactions:

```
  day      0    1    2    3    4    5
  price    7    1    5    3    6    4

  not      0    0    4    4    7    7      <- answer 7
  holding -7   -1   -1    1    1    3

  day 1: holding = max(-7, 0 - 1) = -1     bought at 1
  day 2: not     = max(0, -1 + 5) = 4      sold at 5
  day 3: holding = max(-1, 4 - 3) = 1      bought at 3
  day 4: not     = max(4, 1 + 6) = 7       sold at 6

  profit 7 = (5-1) + (6-3). Two transactions.
```

Why greedy works for unlimited, and only for unlimited:

```
  prices  7  1  5  3  6  4
  diffs     -6 +4 -2 +3 -2

  sum of POSITIVE diffs = 4 + 3 = 7        same answer

  WHY: with unlimited transactions, buying and selling every day
  telescopes:
     buy@1 sell@3, buy@3 sell@5  ==  buy@1 sell@5
  so capturing every up-step is the same as capturing every run.

  WITH A LIMIT OF 1 TRANSACTION:
     greedy on diffs still says 7. The real answer is 5 (buy 1, sell 6).
     -> greedy is WRONG the moment transactions are limited,
        because no local rule knows whether to spend one.
```

The cooldown, as Sarala's three situations:

```
                   buy
      [ FREE ] ----------> [ HOLDING ]
         ^                      |
         |                      | sell
         | (one day passes)     v
      [ COOLING ] <-------------+

   FREE     = no stock, may buy today
   HOLDING  = own stock
   COOLING  = just sold, may NOT buy today

   free[d]    = max( free[d-1],  cooling[d-1] )
   holding[d] = max( holding[d-1], free[d-1] - price[d] )
   cooling[d] = holding[d-1] + price[d]

   Three states instead of two. Same question on each morning.
```

Where the transaction is consumed, which must be stated:

```
  a TRANSACTION = one buy + one matching sell

  COUNT ON THE BUY                COUNT ON THE SELL
  buy[t]  uses one of the t       buy[t]  is free
  sell[t] is free                 sell[t] uses one of the t

  BOTH ARE CORRECT. Pick one, say which, be consistent.

  COUNTING ON BOTH:
     k = 2 behaves like k = 1
     -> a smaller, entirely plausible answer
     -> no error anywhere

  This is the single most common bug in the k-transaction variant.
```

The whole family, on one page:

```
  variant                what changes                 greedy?
  ------------------------------------------------------------
  1 transaction          k = 1                        YES (min-so-far)
  unlimited              the base machine             YES (positive diffs)
  at most k              + a transactions dimension   NO
  with cooldown          2 states -> 3 states         NO
  with a fee             subtract a constant on sell  NO
  (nothing else changes in any of them)
```

---

## 5. The code, built step by step

### One transaction, where greedy wins

```python
def max_profit_one(prices: list[int]) -> int:
    cheapest = float("inf")
    best = 0
    for price in prices:
        cheapest = min(cheapest, price)       # the best day to have bought
        best = max(best, price - cheapest)    # selling here
    return best
```

**One pass, `O(1)` space, and no DP needed.** **Track the minimum so far and the best difference against it** —
the two lines are independent and the order matters: update `cheapest` first, so selling on the same day you
bought gives zero rather than a negative.

### Unlimited transactions, the base machine

```python
def max_profit_unlimited(prices: list[int]) -> int:
    not_holding, holding = 0, -prices[0]
    for price in prices[1:]:
        not_holding = max(not_holding, holding + price)     # sell
        holding = max(holding, not_holding - price)         # buy
    return not_holding
```

**Two variables. That is the whole DP.**

**And there is a subtlety in the order of those two lines.** `holding` is computed from the `not_holding` that
was **just updated this iteration** — meaning it allows buying on the same day you sold. **For the unlimited
version that is harmless**, because buying and selling the same stock on the same day nets zero. **In the
cooldown version it would be a bug**, which is why that one uses a saved copy.

### The greedy version, for contrast

```python
def max_profit_unlimited_greedy(prices: list[int]) -> int:
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
```

**One line, same answer, and only for the unlimited case.** Say why it works — telescoping — and say that it
breaks the moment a transaction limit appears.

### At most `k` transactions

```python
def max_profit_k(prices: list[int], k: int) -> int:
    n = len(prices)
    if n < 2 or k == 0:
        return 0
    if k >= n // 2:                           # limit not binding
        return max_profit_unlimited(prices)   # avoids a huge table
```

**That early return is not an optimisation, it is a requirement.** `k = 10^9` otherwise allocates a table with
a billion rows and raises `MemoryError` — **and LeetCode 188 deliberately includes such an input.**

```python
    # buy[t]  = best money holding stock, having STARTED t transactions
    # sell[t] = best money holding nothing, having COMPLETED t transactions
    buy = [-prices[0]] * (k + 1)
    sell = [0] * (k + 1)
    for price in prices[1:]:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)   # the buy STARTS t
            sell[t] = max(sell[t], buy[t] + price)      # the sell COMPLETES it
    return sell[k]
```

**The comments are the answer to "where is the transaction consumed".** `buy[t]` comes from `sell[t-1]` — **the
buy is what increments the count** — and the matching sell stays at `t`. **Consistent, stated, and it is what
makes the code readable.**

**And iterating `t` from 1 upwards while reading `buy[t]` in the same pass is deliberate**: it allows the
same-day buy-then-sell, which nets zero and is harmless, exactly as in the unlimited version.

### With a cooldown

```python
def max_profit_cooldown(prices: list[int]) -> int:
    free, holding, cooling = 0, -prices[0], float("-inf")
    for price in prices[1:]:
        previous_free, previous_holding = free, holding
        free = max(previous_free, cooling)             # cooldown expired
        holding = max(previous_holding, previous_free - price)
        cooling = previous_holding + price             # sold today
    return max(free, cooling)
```

**Saving yesterday's values is the whole point.** In the unlimited version, reading the freshly-updated value
was harmless; **here it would let you sell and buy on the same day, which is exactly what the cooldown
forbids.**

**And the answer is `max(free, cooling)`**, because the last day might end with a sale — which leaves you in
`cooling`, still holding nothing.

### With a transaction fee

```python
def max_profit_fee(prices: list[int], fee: int) -> int:
    not_holding, holding = 0, -prices[0]
    for price in prices[1:]:
        not_holding = max(not_holding, holding + price - fee)   # pay on the sell
        holding = max(holding, not_holding - price)
    return not_holding
```

**One constant, one transition, no new dimension.** **Charging on the sell is the convention** because the
round trip completes there — charging on the buy also works and gives the same total, provided you do not
charge on both.

### The complete solution

```python
"""Buy and sell stock: one state machine, five variants."""


def max_profit_one(prices: list[int]) -> int:
    """At most ONE transaction. Greedy: min so far, best difference."""
    cheapest, best = float("inf"), 0
    for price in prices:
        cheapest = min(cheapest, price)
        best = max(best, price - cheapest)
    return int(best)


def max_profit_unlimited(prices: list[int]) -> int:
    """Unlimited transactions. The base two-state machine."""
    if not prices:
        return 0
    not_holding, holding = 0, -prices[0]
    for price in prices[1:]:
        not_holding = max(not_holding, holding + price)     # sell
        holding = max(holding, not_holding - price)         # buy
    return not_holding


def max_profit_unlimited_greedy(prices: list[int]) -> int:
    """Same answer, one line. Works ONLY because transactions are unlimited."""
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))


def max_profit_k(prices: list[int], k: int) -> int:
    """At most k transactions. A transaction is CONSUMED ON THE BUY."""
    n = len(prices)
    if n < 2 or k == 0:
        return 0
    if k >= n // 2:                           # not binding: avoids a huge table
        return max_profit_unlimited(prices)

    buy = [-prices[0]] * (k + 1)              # holding, having STARTED t
    sell = [0] * (k + 1)                      # holding nothing, t COMPLETED
    for price in prices[1:]:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)
    return sell[k]


def max_profit_cooldown(prices: list[int]) -> int:
    """One day of cooldown after selling. Three states, not two."""
    if not prices:
        return 0
    free, holding, cooling = 0, -prices[0], float("-inf")
    for price in prices[1:]:
        previous_free, previous_holding = free, holding    # yesterday's values
        free = max(previous_free, cooling)
        holding = max(previous_holding, previous_free - price)
        cooling = previous_holding + price
    return int(max(free, cooling))


def max_profit_fee(prices: list[int], fee: int) -> int:
    """A fee per transaction. No new dimension — one constant."""
    if not prices:
        return 0
    not_holding, holding = 0, -prices[0]
    for price in prices[1:]:
        not_holding = max(not_holding, holding + price - fee)
        holding = max(holding, not_holding - price)
    return not_holding


def max_profit_with_trades(prices: list[int]) -> tuple[int, list[tuple[int, int]]]:
    """Unlimited, and report the actual buy/sell day pairs."""
    trades: list[tuple[int, int]] = []
    i, n = 0, len(prices)
    while i < n - 1:
        while i < n - 1 and prices[i + 1] <= prices[i]:
            i += 1                            # walk down to a local minimum
        if i == n - 1:
            break
        buy_day = i
        while i < n - 1 and prices[i + 1] > prices[i]:
            i += 1                            # walk up to a local maximum
        trades.append((buy_day, i))
    return sum(prices[s] - prices[b] for b, s in trades), trades


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print("one transaction  :", max_profit_one(prices))
    print("unlimited (dp)   :", max_profit_unlimited(prices))
    print("unlimited (greedy):", max_profit_unlimited_greedy(prices))
    print("with trades      :", max_profit_with_trades(prices))
    print("k = 1            :", max_profit_k(prices, 1))
    print("k = 2            :", max_profit_k(prices, 2))
    print("k = 1000000000   :", max_profit_k(prices, 1_000_000_000))
    print("cooldown         :", max_profit_cooldown(prices))
    print("fee of 2         :", max_profit_fee(prices, 2))

    falling = [7, 6, 4, 3, 1]
    print("falling, one     :", max_profit_one(falling))
    print("falling, unlimited:", max_profit_unlimited(falling))

    two_peaks = [3, 3, 5, 0, 0, 3, 1, 4]
    print("two peaks, k=2   :", max_profit_k(two_peaks, 2))
    print("two peaks, k=1   :", max_profit_k(two_peaks, 1))
    print("two peaks, greedy:", max_profit_unlimited_greedy(two_peaks))
    print("two peaks, cooldown:", max_profit_cooldown(two_peaks))
```

Run it and you get:

```
one transaction  : 5
unlimited (dp)   : 7
unlimited (greedy): 7
with trades      : (7, [(1, 2), (3, 4)])
k = 1            : 5
k = 2            : 7
k = 1000000000   : 7
cooldown         : 5
fee of 2         : 3
falling, one     : 0
falling, unlimited: 0
two peaks, k=2   : 6
two peaks, k=1   : 4
two peaks, greedy: 8
two peaks, cooldown: 6
```

**`one transaction 5` against `unlimited 7`** is the whole family in two lines: buying at 1 and selling at 6
gives 5; taking both rises gives 7.

**And `two peaks` gives 4 at `k=1`, 6 at `k=2`, and 8 from greedy** — which is the case that proves greedy
fails when transactions are limited. **The greedy sum of positive differences ignores the limit entirely**, so
it reports the unlimited answer whatever `k` says.

---

## 6. What it costs

**The unlimited version.**

```
one pass over n days, two max operations each
-> O(n) time
-> O(1) space — two variables, no array at all
```

**The `k`-transaction version.**

```
for each of n days, for each of k transaction counts
-> O(n x k) time
-> O(k) space — two arrays of length k+1
```

**Concretely:**

```
n = 100,000 days, k = 100
  100,000 x 100 = 10,000,000 operations   ~2 s in Python. Fine.

n = 100,000, k = 1,000,000,000
  WITHOUT the k >= n/2 check:
    a table with 10^9 rows -> MemoryError
  WITH it:
    falls through to the O(n) unlimited version -> instant

The check turns an impossible input into a trivial one, and
LeetCode 188 includes exactly that input.
```

**Why `k >= n/2` is the right threshold:**

```
each transaction needs at least 2 days: one to buy, one to sell
so in n days you can complete at most floor(n/2) transactions

k >= n/2  =>  the limit can never bind  =>  it IS the unlimited problem
```

**The cooldown version.**

```
three variables, one pass
-> O(n) time, O(1) space

exactly the same cost as the two-state version. Adding a state
to a state MACHINE is free; adding a DIMENSION to a table is not.
```

**That distinction is worth having ready**, because it explains why the cooldown is easy and the `k`-limit is
not: **the cooldown adds a third mode; `k` adds a whole axis.**

**The fee version.**

```
identical to unlimited: O(n) time, O(1) space
one extra subtraction per iteration

-> the cheapest variant in the family. No new state at all.
```

**Compared with the naive recursion:**

```
without memoisation, at each day you branch on buy / sell / do nothing
-> O(3^n)

n = 30:  ~2 x 10^14 calls. Hours.
n = 30 with the state machine: 30 iterations. Microseconds.
```

**The full table, if you write it that way:**

```
dp[n][k+1][2] integers

n = 100,000, k = 100:
  100,000 x 101 x 2 = 20,200,000 cells
  at ~28 bytes per Python int object    = ~570 MB

against O(k) space: 2 x 101 = 202 values = ~6 KB

-> 100,000x less, and the same answer.
```

**And the reconstruction cost:**

```
to report which days you traded on, you need the full table
-> O(n x k) space, back to 570 MB at those sizes

for the UNLIMITED version there is a shortcut: walk the price
series finding local minima and maxima directly.
-> O(n) time, O(1) extra space, and it gives the trades
```

---

## 7. The traps

**Counting the transaction on both the buy and the sell.**

```python
>>> # buy[t]  = max(buy[t],  sell[t-1] - price)
>>> # sell[t] = max(sell[t], buy[t-1] + price)     <- WRONG: t-1 again
>>> # with k = 2 on [3,3,5,0,0,3,1,4] this gives 4, not 6
```

**Four instead of six, and four is the `k = 1` answer** — the limit has been silently halved. **No error, and
a completely plausible number.** Decide where the transaction is consumed, write it in a comment, and be
consistent.

**Forgetting the `k >= n/2` shortcut.**

```python
>>> buy = [-7] * (1_000_000_001)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**Eight gigabytes for the pointer array alone.** The check is three lines and it is the difference between
passing and crashing on a deliberately-included test case.

**Reading the freshly-updated value in the cooldown version.**

```python
>>> free, holding, cooling = 0, -1, float("-inf")
>>> for price in [2, 3]:
...     free = max(free, cooling)
...     holding = max(holding, free - price)      # `free` was JUST updated
...     cooling = holding + price                 # `holding` was JUST updated
```

**This lets you sell and buy on the same day, which is exactly what the cooldown forbids** — and it gives a
profit that is too high. **Save yesterday's values at the top of the loop.** In the unlimited version the same
pattern is harmless, which is why the habit carries over and bites.

**Returning `max(dp[n-1][0], dp[n-1][1])` in the plain versions.**

```python
>>> # holding at the end means you bought and never sold
>>> # that money is spent, so dp[n-1][1] is always <= dp[n-1][0]
>>> # taking the max is harmless here — but it signals you have not
>>> # thought about why, and the interviewer will ask
```

**The answer is `dp[n-1][0]`.** In the cooldown version, though, **`max(free, cooling)` is genuinely
required**, because ending on a sale leaves you in `cooling` — so the rule is not "always index 0", it is
"every state where you hold nothing".

**Using profit instead of money.**

```python
>>> # holding = max(holding, -price)          <- tracks "cost", loses history
>>> # on [1, 2, 3, 4] this gives 3, not 3... check it on [7,1,5,3,6,4]
```

**Tracking money — where buying subtracts and selling adds — keeps the arithmetic uniform** and makes the
transitions obviously correct. **Tracking "profit so far" needs a separate notion of your entry price and is
where sign errors live.**

**Greedy on an input with a transaction limit.**

```python
>>> max_profit_unlimited_greedy([3, 3, 5, 0, 0, 3, 1, 4])
8
>>> max_profit_k([3, 3, 5, 0, 0, 3, 1, 4], 2)
6
>>> max_profit_k([3, 3, 5, 0, 0, 3, 1, 4], 1)
4
```

**Eight, six and four for the same prices.** The greedy sum of positive differences **ignores `k` entirely** —
it reports the unlimited answer whatever the limit says — and **it will pass any test whose `k` happens to be
large enough not to bind.**

**An empty or single-element list.**

```python
>>> max_profit_unlimited([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in max_profit_unlimited
    not_holding, holding = 0, -prices[0]
IndexError: list index out of range
```

**`prices[0]` on an empty list.** One guard, and it is a standard added test case.

**A fee charged on both halves.**

```python
>>> max_profit_fee([1, 3, 7, 5, 10, 3], 3)
6
>>> # charging on buy AND sell would give 0 here — the fee is doubled,
>>> # and every trade looks unprofitable
```

**A doubled fee makes marginal trades look bad and the answer collapses towards zero**, which reads like "the
fee is high" rather than like a bug.

---

## 8. In the interview

### How it gets asked

- *"Best time to buy and sell stock."* — LeetCode 121, one transaction.
- *"Now you can buy and sell as many times as you like."* — LeetCode 122.
- *"At most `k` transactions."* — LeetCode 188, and the ladder's hard rung.
- *"With a one-day cooldown after selling."* — LeetCode 309.
- *"With a fee per transaction."* — LeetCode 714.
- *"Which of these can you solve greedily?"*

### The first ninety seconds

> "This is a family of about six problems and they share one state, so let me set that up rather than solve
> the specific one — it makes every variant a small edit.
>
> **The state is `(day, whether I am currently holding the stock)`.** And the second part is the idea worth
> naming: **it is a *mode*, not a position.** Every DP so far has been indexed by where I am; here I also need
> to know **which situation I am in**, because it decides which moves are legal.
>
> **Without it the state is incomplete.** 'The best profit in the first `n` days' cannot express a recurrence,
> because **I cannot tell whether selling today is even legal without knowing whether I own anything** — and
> that fails silently, like every incomplete state.
>
> **Two transitions, and I would track money rather than profit** so buying subtracts and selling adds and the
> signs never confuse me.
>
> **Not holding at the end of today: either I was not holding and did nothing, or I was holding and sold.**
> `max(dp[d-1][0], dp[d-1][1] + price)`.
>
> **Holding at the end of today: either I was holding and kept it, or I was not and bought.**
> `max(dp[d-1][1], dp[d-1][0] - price)`.
>
> **Base cases: on day zero, not holding is zero and holding is minus the first price.**
>
> **The answer is the not-holding state, not the maximum of the two** — ending while still holding means I
> bought something and never sold it, which is never better.
>
> **`O(n)` time and `O(1)` space** — two variables, no table.
>
> **And then the variants are each one change.** A fee is a constant subtracted on the sell, with no new state
> at all. A cooldown is a third state — free, holding, just-sold. **At most `k` transactions is the only one
> that adds a dimension**, and it is the only one that costs anything.
>
> **One thing I would ask: is there a limit on transactions?** Because with no limit, greedy solves it in one
> line — sum every positive day-to-day difference — **and the moment there is a limit, greedy is wrong**, which
> is the interesting part."

### The follow-ups

**"At most `k` transactions. What changes?"**

> "A third dimension, and one decision I have to state explicitly before writing anything.
>
> **The state becomes `(day, transactions used, holding)`.** Same two transitions, indexed by how many
> transactions I have spent.
>
> **The decision: where is a transaction consumed?** A transaction is a buy plus its matching sell. **I can
> count it on the buy or on the sell — both are correct — and I must pick one and be consistent.**
>
> **I count it on the buy.** So `buy[t]` comes from `sell[t-1]` minus the price — starting transaction `t` —
> and the matching `sell[t]` comes from `buy[t]` plus the price, staying at `t`.
>
> **Counting it on both is the standard bug**, and it halves the effective limit: `k = 2` behaves like `k = 1`.
> On `[3,3,5,0,0,3,1,4]` that gives four instead of six, **and four is a completely plausible answer** — it is
> the correct answer to a different question. **No error anywhere**, which is why I write the meaning of each
> array in a comment before the loop.
>
> **The other thing that must be there is the `k >= n/2` shortcut.** Each transaction needs at least two days,
> so in `n` days I can complete at most `n/2`. **If `k` is at least that, the limit can never bind and the
> answer is the unlimited version.**
>
> **That is not an optimisation — it is required.** LeetCode 188 includes `k = 10^9`, and without the check I
> allocate a billion-row array and get a `MemoryError` before doing any work.
>
> **Cost: `O(n × k)` time and `O(k)` space** with two arrays of length `k+1`, since each day reads only
> yesterday. **The full table would be `n × k × 2` — at `n = 100,000` and `k = 100` that is about 570
> megabytes against six kilobytes**, for the same answer.
>
> **And if they want the actual trades, I need the full table** — same trade as every reconstruction."

**"Which of these can you solve greedily, and why does greedy break?"**

> "Two of them, and the reason it breaks is worth stating precisely because it is the justification for the DP.
>
> **One transaction: greedy works.** Track the minimum price seen so far and the best difference against it, in
> one pass. `O(n)` time, `O(1)` space, and the DP would be overkill.
>
> **Unlimited transactions: greedy works, and the reason is telescoping.** Sum every positive day-to-day
> difference. **Buying at 1 and selling at 3, then buying at 3 and selling at 5, is identical to buying at 1
> and selling at 5** — so capturing every upward step is the same as capturing every rising run, and it is
> one line.
>
> **A limited number of transactions: greedy fails, and here is exactly why.** With a limit, each transaction
> is a scarce resource. **A local rule cannot know whether to spend one on a small rise today or save it for a
> bigger rise later**, because that depends on the whole rest of the series.
>
> **Concretely, on `[3,3,5,0,0,3,1,4]`: greedy on differences says eight** — it takes every rise, three of them.
> **With `k = 2` the answer is six, and with `k = 1` it is four**, because one transaction buys me only the best
> single trade, which is buying at zero and selling at four. **Greedy reports the same eight in all three
> cases**, because nothing in it looks at `k`.
>
> **And greedy will pass any test where `k` happens to be large enough not to bind**, which makes it a
> dangerous thing to submit.
>
> **The cooldown and the fee also break greedy**, for the same underlying reason: **a local decision cannot
> account for a cost that lands in the future.** Selling today might be locally profitable and lock me out of a
> much better trade tomorrow.
>
> **So my rule is: greedy for one transaction and for unlimited, the state machine for everything else** — and
> I would offer both for the unlimited case, since the greedy one-liner is genuinely better and knowing the DP
> is what lets me handle the next question."

**"Now add a one-day cooldown after selling."**

> "A third state, and that is genuinely all — which is worth contrasting with the `k`-transaction case, because
> the costs are completely different.
>
> **Adding a state to a state machine is free. Adding a dimension to a table is not.** The cooldown stays
> `O(n)` time and `O(1)` space; the transaction limit becomes `O(n × k)`.
>
> **Three states: free, holding, and cooling.** **Free** means I own nothing and may buy today. **Holding**
> means I own the stock. **Cooling** means I sold today, so I own nothing and may *not* buy.
>
> **The transitions:**
>
> **Free today** means either I was free yesterday and did nothing, or I was cooling yesterday and the
> cooldown has now expired.
>
> **Holding today** means either I was holding and kept it, or I was **free** yesterday and bought — not
> cooling, which is the entire point.
>
> **Cooling today** means I was holding yesterday and sold today. Only one way in.
>
> **The implementation detail that matters: I must save yesterday's values at the top of the loop.** In the
> unlimited version I read freshly-updated values and it was harmless, because buying and selling the same
> stock on the same day nets zero. **Here it would let me sell and immediately buy, which is exactly what the
> cooldown forbids**, and the answer comes out too high with no error.
>
> **And the answer is `max(free, cooling)`, not just `free`.** The last day might end with a sale, which leaves
> me in `cooling` — holding nothing, which is what I want, but in the other state.
>
> **So the general rule is not 'return index zero'** — it is **'return the best over every state in which I
> hold nothing'**, and in the two-state version that happens to be one state."

### The model answer

*"You are given the hourly electricity price for the next week, and a battery that can be fully charged or
fully discharged in one hour. Charging costs you the price; discharging earns it. The battery can do at most
`k` full cycles before it needs servicing. Maximise your earnings."*

> "This is buy-and-sell stock with at most `k` transactions, and I want to establish that mapping explicitly
> before writing anything, because getting it right makes the rest mechanical.
>
> **A charge is a buy. A discharge is a sell. A full cycle is one transaction.** The hourly prices are the
> price series. **Maximising earnings is maximising profit.**
>
> **And the constraint that makes it this problem rather than a simpler one is that the battery is either
> charged or empty** — there is no partial state. **That is exactly the holding / not-holding mode.**
>
> **The state: `(hour, cycles used, charged)`.** Same two transitions as the stock problem: at each hour I can
> do nothing, charge if empty, or discharge if charged.
>
> **And I would state where the cycle is consumed: on the charge.** So `charged[t]` comes from `empty[t-1]`
> minus the price — starting cycle `t` — and `empty[t]` comes from `charged[t]` plus the price, staying at
> `t`. **Counting it on both halves the limit and gives a smaller, entirely plausible answer**, which is the
> bug I would be watching for.
>
> **Base cases: at hour zero, empty is zero earnings and charged is minus the first hour's price.**
>
> **The answer is `empty[k]`** — the battery should end discharged, because energy left in it at the end is
> money spent and not recovered. **If the problem said the battery must end charged, that would be
> `charged[k]` instead**, and I would ask.
>
> **Sizing: a week of hourly prices is 168 hours.** With `k` cycles that is `168 × k` operations — trivial for
> any realistic `k`. **And I would still include the `k >= n/2` shortcut**, because if `k` is large the limit
> cannot bind — each cycle needs at least two hours — **and it turns a potentially enormous table into an
> `O(n)` pass.**
>
> **Space: two arrays of length `k+1`**, since each hour reads only the previous one.
>
> **Now three things about the domain that I would raise, because the stock mapping hides them.**
>
> **First, the battery probably is not perfectly efficient.** Real batteries lose energy on a round trip —
> typically ten to fifteen percent. **That is exactly the transaction-fee variant**: multiply the discharge
> earnings by the efficiency, or subtract a fee. **No new dimension, one constant** — which is a nice
> demonstration that the mapping is doing real work.
>
> **Second, the prices are a forecast, not a fact.** This computes the optimal plan for a price series I do not
> actually know. **In practice you would re-solve every hour with updated prices**, which is cheap here, and
> accept that the realised profit is below the theoretical optimum. **I would say that rather than present the
> number as achievable.**
>
> **Third, and I would flag it as a question rather than assume: can the battery charge and discharge in the
> same hour?** The stock version implicitly allows a same-day buy-and-sell that nets zero and is harmless.
> **A physical battery cannot**, and if there is also a minimum rest period after discharging, **that is the
> cooldown variant — a third state, still `O(n)` time and constant space.**
>
> **Which is the general point I would close on: charge-or-empty, cycle limit, efficiency loss and rest period
> are four different-sounding constraints, and they are the same four variants of one state machine.**"

---

## 9. Recall card

**The state is `(day, holding)` — and the second dimension is a MODE, not a position.** "Best profit in the
first `n` days" is incomplete: you cannot tell whether selling is legal without knowing whether you hold.
**Track money, not profit** — buying subtracts, selling adds.

**`dp[d][0] = max(dp[d-1][0], dp[d-1][1] + price)` (sell); `dp[d][1] = max(dp[d-1][1], dp[d-1][0] - price)`
(buy).** Base: `dp[0][0] = 0`, `dp[0][1] = -price[0]`. **The answer is the not-holding state** — ending while
holding is never optimal. `O(n)` time, `O(1)` space, two variables.

**Greedy solves exactly two variants.** One transaction: min-so-far and best difference. **Unlimited: sum the
positive day-to-day differences, because buy@1/sell@3 then buy@3/sell@5 telescopes into buy@1/sell@5.** **Any
transaction limit breaks greedy** — on `[3,3,5,0,0,3,1,4]` greedy says 8 whatever `k` is, while the answers
are 6 at `k=2` and 4 at `k=1`.

**At most `k`: add a dimension, and STATE where the transaction is consumed.** Count it on the buy
(`buy[t]` from `sell[t-1]`); **counting on both halves the limit and gives a plausible smaller number with no
error.** **The `k >= n/2` shortcut is required, not an optimisation** — each transaction needs two days, and
`k = 10^9` otherwise means `MemoryError`.

**A fee is one constant on the sell — no new state.** **A cooldown is a third state** (free / holding /
cooling), still `O(n)` and `O(1)` — **adding a state to a machine is free; adding a dimension to a table is
not.** In the cooldown version **save yesterday's values**, or you sell and buy on the same day; and the answer
is **`max(free, cooling)`** — every state where you hold nothing.
