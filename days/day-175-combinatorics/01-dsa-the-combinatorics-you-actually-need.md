---
day: 175
track: dsa
title: "The combinatorics you actually need"
phase: "Bits and maths"
status: written
---

# The combinatorics you actually need

## 1. What this is, and why they ask it

**Combinatorics is counting without listing.** How many ways can these things be arranged? How many ways can
you choose five of them? **The answer is a number, and you must produce it without generating every
possibility** — because there are usually more possibilities than atoms available.

**Almost all of it comes from one rule.** **If a choice has 4 options and an independent second choice has 6,
there are 24 combinations.** Multiply. Everything else in this lesson is that rule with a correction applied.

**And one question decides which formula you need: does order matter?** "Pick three people for a committee" and
"pick three people for first, second and third place" are different questions with different answers, **and
they differ by exactly a factor of `3!`.**

They ask it because **counting problems are everywhere and the arithmetic goes wrong quietly.** "How many
unique paths across this grid?" is a combinatorics question wearing a dynamic programming costume. **"Return
the answer modulo 10^9 + 7" is a counting problem by definition** — nobody asks for a modulus unless the answer
is enormous.

**And because `n!` overflows almost immediately.** **`21!` does not fit in a 64-bit integer.** A candidate who
writes `factorial(n) // (factorial(r) * factorial(n - r))` has written something that is mathematically correct
and breaks at `n = 21`, **while the answer they wanted was 210.**

By the end of this lesson you can decide in one question which formula a problem needs, compute `nCr` without
ever forming a factorial, do it under a modulus with three lookups per query, count arrangements with repeated
items, and recognise the four or five standard shapes that hide inside interview problems.

---

## 2. The story

The wedding was on the twelfth and Renuka's daughter had been asking the same question for four days.

**"How many do you actually need to take?"**

Renuka had six sarees she was prepared to be seen in, and four blouses that went under more than one of them.
Her daughter looked at the pile on the bed and saw ten things. **Renuka looked at the same pile and saw
twenty-four.**

The girl did not believe her, so Renuka made her count it out loud.

"Take the green one. Which blouses can go under it?"

All four, the girl said.

"So that is four different ways somebody at the wedding sees me. Now the maroon."

All four again.

**Six sarees, four blouses each. Twenty-four.**

"So if you put in one more blouse," the girl said, working it through, "that is twenty-five."

**"Thirty," said Renuka.**

And that was the part the girl actually remembered afterwards. **One extra blouse in the bag was not one more
outfit. It was six more — one for every saree.**

On the day itself there was a second argument, and it turned out to be the other half of the same idea.

The photographer wanted the five of them in a line — Renuka, her husband, the two girls, and her
mother-in-law. He put them in an order. Then he changed it. Then he tried the old lady in the middle instead of
on the end. Then he went back to something close to the first one.

Renuka's daughter, who by now had started noticing this sort of thing, worked it out while she was standing
there in the sun.

**Any of the five of them could stand at the left end. Then four people were left for the next place. Then
three. Then two. Then the last one had nowhere else to go.**

Five times four times three times two.

**A hundred and twenty.**

She said it out loud. The photographer did not find it as interesting as she did, **and took the fourth
arrangement he had tried.**

---

## 3. The idea in plain English

**Renuka's two arguments are the whole subject.** **The sarees and blouses are the multiplication principle.
The photograph is a permutation.** And the difference between them is the one question you always ask first.

### The multiplication principle

**If one choice has `a` options and an independent second choice has `b` options, together they have
`a × b`.**

```
   4 breads x 6 curries x 3 sweets = 72 different meals

   and "no sweet" is a fourth option for the third choice:
   4 x 6 x 4 = 96
```

**"Independent" is the word doing the work.** It means the second choice is not limited by the first. **If two
of the blouses only go with three of the sarees, you cannot simply multiply** — and noticing that is usually
where a counting problem becomes hard.

### The one question: does order matter?

**Ask it before writing anything.**

```
   "Pick 3 people for a committee"
     -> Asha, Biju, Chetan is the SAME committee as
        Chetan, Biju, Asha.
     -> ORDER DOES NOT MATTER.

   "Pick 3 people for gold, silver and bronze"
     -> Asha-Biju-Chetan is a DIFFERENT result from
        Chetan-Biju-Asha.
     -> ORDER MATTERS.
```

**And there is a second question: can you repeat?** Together they give four cases, **and every basic counting
problem is one of these four.**

```
                        ORDER MATTERS       ORDER DOES NOT

   NO REPEATS           nPr                 nCr
                        n!/(n-r)!           n!/(r!(n-r)!)

   REPEATS ALLOWED      n^r                 C(n+r-1, r)
                        (r independent      "stars and bars"
                         choices from n)
```

**Learn the table as four questions, not four formulas.** In an interview you will not remember which formula
is which; **you will remember "does order matter, can I repeat", and then derive the right one in ten
seconds.**

### Permutations, from Renuka's photograph

**Arranging `n` distinct things in a row: `n!`.**

**The reasoning is the girl's reasoning and it is better than the formula.** Five choices for the first
position, then four remain, then three, then two, then one. **5 × 4 × 3 × 2 × 1 = 120.**

**Arranging only `r` of them: stop early.** `nPr = n × (n−1) × ... × (n−r+1)`, which is `r` factors.

```
   10 people, 3 prizes:
     10 x 9 x 8 = 720
```

### Combinations, and where the division comes from

**`nCr` is `nPr` divided by `r!`, and the reason is worth saying rather than memorising.**

```
   Pick 3 of 10 with order:  10 x 9 x 8 = 720

   But each GROUP of three has been counted once for
   every ORDER it could appear in - and three things
   can be ordered 3! = 6 ways.

   So each committee was counted 6 times.

   720 / 6 = 120 committees.
```

**"I have counted each answer once per arrangement, so I divide by the number of arrangements" is the most
useful sentence in this lesson.** It is how you fix over-counting in problems that have no named formula at
all.

### Two facts about `nCr` worth having

**Symmetry: `C(n, r) = C(n, n − r)`.** **Choosing 3 to take is the same as choosing 17 to leave.** So
**always compute with the smaller of the two** — `C(20, 17)` in three steps rather than seventeen.

**Pascal's identity: `C(n, r) = C(n−1, r−1) + C(n−1, r)`.**

**Read it as a sentence about one particular item.** *Either that item is in the group — then choose the
remaining `r − 1` from the other `n − 1` — or it is out, and you choose all `r` from the other `n − 1`.* **In
or out, no overlap, nothing missed.**

**That sentence is why counting problems turn into dynamic programming.** **It is the same "take it or leave
it" split as the knapsack**, and Pascal's triangle is the DP table.

**And the row sums: row `n` of Pascal's triangle adds up to `2^n`.** **Because choosing 0, or 1, or 2, ... or
`n` items covers every possible subset**, and there are `2^n` subsets — which is [day 172's](../day-172-bit-tricks/README.md)
"a subset is a number", seen from the counting side.

### Never compute a factorial

**This is the practical heart of the lesson.**

```
   C(100, 50) = 100! / (50! 50!)

   100! has 158 digits.
   The answer has 30 digits.

   -> You would build two enormous numbers and divide them
      to get something far smaller than either.
```

**Build it up instead, one factor at a time:**

```
   result = 1
   for i in 0 .. r-1:
       result = result * (n - i) // (i + 1)

   C(5, 2):
     i=0:  1 * 5 // 1 = 5
     i=1:  5 * 4 // 2 = 10
```

**The division is exact at every step**, which is the part that looks suspicious and is not: **after `i + 1`
factors of the numerator, the running value is `C(n, i+1)`, which is a whole number by definition.**

**And the largest number the loop ever holds is the answer itself.** For `C(100, 50)` that is 30 digits rather
than 158.

### Arrangements when things repeat

**MISSISSIPPI has 11 letters: one M, four I, four S, two P.**

```
   If all 11 were distinct: 11! = 39,916,800

   But the four I's are identical, so every arrangement
   was counted 4! = 24 times over, once per shuffle of
   the I's. Same for the four S's, and 2! for the P's.

   11! / (1! x 4! x 4! x 2!) = 34,650
```

**Same sentence as before: counted once per arrangement of the identical things, so divide by it.**

### Stars and bars

**Distributing identical things into labelled boxes.** Ten identical sweets among four children.

```
   Write the sweets as stars and the divisions as bars:

     * * * | * * | * * * * | *
       3      2      4       1

   Ten stars and three bars, in a row: 13 positions,
   and you choose which 3 of them are bars.

   -> C(13, 3) = 286

   If every child must get at least one, give each one
   sweet first and share out the remaining six:
   -> C(9, 3) = 84
```

**The trick is turning an arrangement problem into a choosing problem**, and it is worth recognising because it
appears disguised — "how many ways to write `n` as a sum of `k` non-negative numbers" is exactly this.

### Under a modulus

**When the answer must be given modulo `10^9 + 7`, you cannot divide.** [Yesterday's](../day-174-number-theory/01-dsa-primes-gcd-and-modular-arithmetic.md)
inverse does the work.

```
   Precompute once, up to the largest n you will need:
     fact[i]     = i! mod m
     inv_fact[i] = the inverse of i! mod m

   Then every query is three lookups and two multiplications:
     C(n, r) = fact[n] * inv_fact[r] * inv_fact[n-r]  mod m
```

**And there is a trick for the inverse factorials that is worth knowing**, because the obvious way costs one
fast power per entry:

```
   inv_fact[N] = power_mod(fact[N], m - 2, m)     ONE fast power
   then walk DOWN:
     inv_fact[i-1] = inv_fact[i] * i mod m

   because 1/(i-1)! = 1/i! x i
```

**One fast power for the whole table instead of `N` of them** — at `N = 200,000` that is thirty multiplications
instead of six million.

### The shapes to recognise

```
   "how many paths across an m x n grid, right and down only"
     -> every path is (m-1) downs and (n-1) rights in some
        order; choose which steps are the downs
     -> C(m+n-2, m-1)

   "how many balanced bracket strings of length 2n"
   "how many shapes can a binary tree with n nodes have"
   "how many ways to fully parenthesise a product"
     -> all the SAME NUMBER: the nth Catalan number,
        C(2n, n) / (n + 1)
     -> 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862

   "how many subsets"        -> 2^n
   "how many subsets of size k" -> C(n, k)
```

**Catalan numbers are worth memorising up to about 42**, because recognising `1, 2, 5, 14, 42` in your own
small-case working is often how you spot the pattern in the first place.

---

## 4. The picture

The multiplication principle as a tree:

```
   6 sarees x 4 blouses

   green ---+--- blouse A
            +--- blouse B
            +--- blouse C
            +--- blouse D          4 outfits

   maroon --+--- blouse A
            +--- blouse B
            +--- blouse C
            +--- blouse D          4 outfits

   ... four more sarees ...

   6 branches, each splitting 4 ways = 24 leaves.

   ADD ONE BLOUSE: every branch splits 5 ways instead
   of 4 -> 30. The new blouse is worth SIX outfits,
   not one, because it appears under every saree.
```

Order matters, or it does not:

```
   Pick 2 from {A, B, C}

   ORDER MATTERS (3P2 = 6)      ORDER DOES NOT (3C2 = 3)
     AB  BA                       AB     <- same group
     AC  CA                       AC     <- same group
     BC  CB                       BC     <- same group

   Each unordered pair appears 2! = 2 times in the
   left-hand list.

   6 / 2 = 3.

   THAT DIVISION IS THE ONLY DIFFERENCE BETWEEN THE TWO
   COLUMNS, and it is r! every time.
```

Pascal's triangle, and the identity drawn on it:

```
                       1
                    1     1
                 1     2     1
              1     3     3     1
           1     4     6     4     1
        1     5    10    10     5     1
     1     6    15    20    15     6     1

   THE IDENTITY, on the 20:
        ...  10    10  ...          row 5
               \   /
     C(6,3) =    20                 row 6

     C(6,3) = C(5,2) + C(5,3)
              ^^^^^^   ^^^^^^
              item is  item is
              IN       OUT

   ROW SUMS:
     row 0: 1                 = 1  = 2^0
     row 1: 1+1               = 2  = 2^1
     row 2: 1+2+1             = 4  = 2^2
     row 3: 1+3+3+1           = 8  = 2^3
     row 6: 1+6+15+20+15+6+1  = 64 = 2^6

   -> every subset, sorted by its size. Which is the
      same 2^n as counting from 0 to 2^n - 1 in binary.
```

Stars and bars:

```
   10 identical sweets, 4 children

   * * * | * * | * * * * | *
   \_____/ \___/ \_______/ \_/
     3       2       4      1

   The row is 10 stars + 3 bars = 13 symbols.
   An arrangement is decided entirely by WHICH 3 of the
   13 positions hold bars.

   -> C(13, 3) = 286

   Note what the bars can do:
     | * * * * * * * * * * | |
     -> first child 0, second 10, third 0, fourth 0
   Adjacent bars mean an empty box, which is allowed here.

   "At least one each": hand out 4 sweets first, then
   share the remaining 6 the same way -> C(9, 3) = 84.
```

Grid paths, which is `nCr` in a costume:

```
   3 rows x 7 columns, moving only RIGHT and DOWN

   +---+---+---+---+---+---+---+
   | S |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+
   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+
   |   |   |   |   |   |   | E |
   +---+---+---+---+---+---+---+

   EVERY path is exactly 2 downs and 6 rights,
   in some order. 8 steps in total.

   A path IS a choice of which 2 of the 8 steps
   are the downs.

   -> C(8, 2) = 28

   The dynamic programming solution fills 21 cells.
   The counting solution is one line. Both are correct,
   and knowing they are the same problem is the point.
```

---

## 5. The code, built step by step

### The two that are just loops

```python
def factorial(n: int) -> int:
    """n! - the number of ways to put n distinct things in a row."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def permutations_count(n: int, r: int) -> int:
    """nPr: pick r from n where ORDER MATTERS. n x (n-1) x ... x (n-r+1)."""
    if r < 0 or r > n:
        return 0
    result = 1
    for i in range(r):
        result *= n - i
    return result
```

**`permutations_count` stops after `r` factors rather than computing `n!` and dividing.** **The formula
`n!/(n−r)!` is a description, not an instruction** — for `n = 100, r = 3` it says build a 158-digit number and
divide, when the answer is 970,200.

**Returning 0 for out-of-range `r` rather than raising is a choice, and it is usually the right one**, because
counting problems produce impossible cases naturally and zero is the honest answer.

### Combinations, without ever forming a factorial

```python
def combinations_count(n: int, r: int) -> int:
    """nCr, built up one factor at a time. Never forms n! - so it never explodes."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result
```

**Two lines carry all the value here.**

**`r = min(r, n - r)` uses the symmetry** — `C(20, 17)` becomes `C(20, 3)` and the loop runs three times instead
of seventeen.

**`result * (n - i) // (i + 1)` multiplies before it divides**, and **the division is exact every time**. After
`i + 1` steps the running value is exactly `C(n, i+1)`, which is a whole number. **If you divide first you get
a fraction; if you use `/` instead of `//` you get a float and you lose precision at around 15 digits.**

### Pascal's triangle, which is addition only

```python
def pascal_triangle(rows: int) -> list[list[int]]:
    """The whole triangle, by addition only. No multiplication, no division."""
    triangle: list[list[int]] = []
    for n in range(rows):
        row = [1] * (n + 1)
        for i in range(1, n):
            row[i] = triangle[n - 1][i - 1] + triangle[n - 1][i]
        triangle.append(row)
    return triangle
```

**The ends are always 1 — `C(n, 0)` and `C(n, n)`** — so the inner loop starts at 1 and stops before the end.
**No multiplication, no division, no overflow risk beyond the numbers themselves.**

**This is the right tool when you need many values of `nCr` with small `n`**, and the wrong one when `n` is
large: **the triangle for `n = 100,000` is five billion entries.**

### Under a modulus, with the walk-down trick

```python
def build_factorials(limit: int, modulus: int = MOD) -> tuple[list[int], list[int]]:
    """Factorials and their inverses, once, so every later nCr is three lookups."""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % modulus
    inverse_fact = [1] * (limit + 1)
    inverse_fact[limit] = power_mod(fact[limit], modulus - 2, modulus)
    for i in range(limit, 0, -1):
        inverse_fact[i - 1] = inverse_fact[i] * i % modulus
    return fact, inverse_fact
```

**One fast power for the whole table.** `1/(i−1)!` is `1/i! × i`, **so once you have the last inverse you can
walk backwards multiplying.** **At `limit = 200,000` that is thirty multiplications instead of six million.**

```python
def ncr_mod(n: int, r: int, fact: list[int], inverse_fact: list[int],
            modulus: int = MOD) -> int:
    """n! / (r! (n-r)!) under a modulus: multiply by inverses instead of dividing."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inverse_fact[r] % modulus * inverse_fact[n - r] % modulus
```

**Three lookups and two multiplications, after the one-off preparation.** **Take the modulus between the
multiplications, not only at the end** — in C++ the intermediate would overflow otherwise.

### The named shapes

```python
def multiset_permutations(counts: list[int]) -> int:
    """Arrangements of things with repeats: n! divided by the factorial of each count."""
    total = sum(counts)
    result = factorial(total)
    for c in counts:
        result //= factorial(c)
    return result


def stars_and_bars(items: int, boxes: int) -> int:
    """Ways to split `items` identical things into `boxes` labelled boxes, empties allowed."""
    return combinations_count(items + boxes - 1, boxes - 1)


def catalan(n: int) -> int:
    """C(2n, n) / (n + 1). Counts balanced brackets, and shapes of binary trees."""
    return combinations_count(2 * n, n) // (n + 1)


def unique_paths(rows: int, cols: int) -> int:
    """Only right and down moves: choose which of the steps are the downward ones."""
    return combinations_count(rows + cols - 2, rows - 1)
```

**Each of these is one line because the thinking happened before the code.** **`unique_paths` is the clearest
example**: the whole solution is the sentence "a path is a choice of which steps go down", and once you have
said it there is nothing left to write.

### The complete solution

```python
"""Day 175 - the combinatorics interviews actually use: count, choose, and do it safely."""

from __future__ import annotations

MOD = 1_000_000_007


def factorial(n: int) -> int:
    """n! - the number of ways to put n distinct things in a row."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def permutations_count(n: int, r: int) -> int:
    """nPr: pick r from n where ORDER MATTERS. n x (n-1) x ... x (n-r+1)."""
    if r < 0 or r > n:
        return 0
    result = 1
    for i in range(r):
        result *= n - i
    return result


def combinations_count(n: int, r: int) -> int:
    """nCr, built up one factor at a time. Never forms n! - so it never explodes."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result


def pascal_row(n: int) -> list[int]:
    """Row n of Pascal's triangle. Each entry is the sum of the two above it."""
    row = [1]
    for i in range(n):
        row.append(row[-1] * (n - i) // (i + 1))
    return row


def pascal_triangle(rows: int) -> list[list[int]]:
    """The whole triangle, by addition only. No multiplication, no division."""
    triangle: list[list[int]] = []
    for n in range(rows):
        row = [1] * (n + 1)
        for i in range(1, n):
            row[i] = triangle[n - 1][i - 1] + triangle[n - 1][i]
        triangle.append(row)
    return triangle


def power_mod(base: int, exponent: int, modulus: int) -> int:
    """Square and multiply, from yesterday. Needed for the modular inverse."""
    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def build_factorials(limit: int, modulus: int = MOD) -> tuple[list[int], list[int]]:
    """Factorials and their inverses, once, so every later nCr is three lookups."""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % modulus
    inverse_fact = [1] * (limit + 1)
    inverse_fact[limit] = power_mod(fact[limit], modulus - 2, modulus)
    for i in range(limit, 0, -1):
        inverse_fact[i - 1] = inverse_fact[i] * i % modulus
    return fact, inverse_fact


def ncr_mod(n: int, r: int, fact: list[int], inverse_fact: list[int],
            modulus: int = MOD) -> int:
    """n! / (r! (n-r)!) under a modulus: multiply by inverses instead of dividing."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inverse_fact[r] % modulus * inverse_fact[n - r] % modulus


def multiset_permutations(counts: list[int]) -> int:
    """Arrangements of things with repeats: n! divided by the factorial of each count."""
    total = sum(counts)
    result = factorial(total)
    for c in counts:
        result //= factorial(c)
    return result


def stars_and_bars(items: int, boxes: int) -> int:
    """Ways to split `items` identical things into `boxes` labelled boxes, empties allowed."""
    return combinations_count(items + boxes - 1, boxes - 1)


def catalan(n: int) -> int:
    """C(2n, n) / (n + 1). Counts balanced brackets, and shapes of binary trees."""
    return combinations_count(2 * n, n) // (n + 1)


def unique_paths(rows: int, cols: int) -> int:
    """Only right and down moves: choose which of the steps are the downward ones."""
    return combinations_count(rows + cols - 2, rows - 1)


if __name__ == "__main__":
    print("THE MULTIPLICATION PRINCIPLE")
    print("  4 breads x 6 curries x 3 sweets = ", 4 * 6 * 3)
    print("  and with a choice of 'no sweet': 4 x 6 x 4 =", 4 * 6 * 4)

    print()
    print("FACTORIALS GROW FASTER THAN ANYTHING YOU HAVE A NAME FOR")
    for n in (5, 10, 15, 20, 21, 25):
        f = factorial(n)
        fits = "fits in 64 bits" if f < 2 ** 63 else "OVERFLOWS 64 bits"
        print(f"  {n:>2}! = {f:>26,}   {fits}")

    print()
    print("ORDER MATTERS, OR IT DOES NOT")
    for n, r in ((5, 2), (5, 3), (10, 3), (52, 5)):
        print(f"  n={n:>2} r={r}   nPr = {permutations_count(n, r):>12,}"
              f"   nCr = {combinations_count(n, r):>10,}"
              f"   ratio = {r}! = {factorial(r)}")

    print()
    print("PASCAL'S TRIANGLE - every entry is the two above it")
    for row in pascal_triangle(8):
        print("   " + " ".join(f"{v:>4}" for v in row).center(44))

    print()
    print("THE SYMMETRY, AND WHY IT SAVES HALF THE WORK")
    print(f"  C(20, 3)  = {combinations_count(20, 3):,}")
    print(f"  C(20, 17) = {combinations_count(20, 17):,}   same number")
    print("  -> so always compute with the SMALLER of r and n-r")

    print()
    print("THE MULTIPLICATIVE FORM NEVER EXPLODES")
    print(f"  C(100, 50) = {combinations_count(100, 50):,}")
    print(f"  100! has {len(str(factorial(100)))} digits, and we never formed it")

    running = 1
    biggest = 1
    for i in range(50):
        running = running * (100 - i) // (i + 1)
        biggest = max(biggest, running)
    print(f"  largest intermediate value: {biggest:,} ({len(str(biggest))} digits)")

    print()
    print("nCr UNDER A MODULUS - precompute once, then three lookups")
    fact, inv_fact = build_factorials(200_000)
    for n, r in ((5, 2), (100, 50), (200_000, 100_000)):
        print(f"  C({n:,}, {r:,}) mod 1e9+7 = {ncr_mod(n, r, fact, inv_fact):,}")
    print(f"  check small case against exact: C(100,50) mod MOD = "
          f"{combinations_count(100, 50) % MOD:,}")

    print()
    print("ARRANGEMENTS WITH REPEATS")
    print("  MISSISSIPPI: 11 letters, M1 I4 S4 P2")
    print(f"    11! / (1! 4! 4! 2!) = {multiset_permutations([1, 4, 4, 2]):,}")
    print(f"    against 11! = {factorial(11):,} if every letter were distinct")

    print()
    print("STARS AND BARS - identical things into labelled boxes")
    print(f"  10 identical sweets among 4 children = C(13, 3) = "
          f"{stars_and_bars(10, 4)}")
    print(f"  10 sweets, 4 children, everyone gets at least one = C(9, 3) = "
          f"{combinations_count(9, 3)}")

    print()
    print("CATALAN NUMBERS - the same count wearing five hats")
    print(f"  {[catalan(n) for n in range(10)]}")
    print("  balanced bracket strings of length 2n; shapes of a binary tree")
    print("  with n nodes; ways to triangulate a polygon; ways to fully")
    print("  parenthesise a product.")

    print()
    print("GRID PATHS - the choose in disguise")
    for r, c in ((3, 7), (3, 3), (18, 18)):
        print(f"  {r} x {c} grid: C({r + c - 2}, {r - 1}) = {unique_paths(r, c):,}")

    print()
    print("VERIFICATION")
    import math
    import random

    bad = 0
    for _ in range(3000):
        n = random.randint(0, 300)
        r = random.randint(-2, n + 2)
        if combinations_count(n, r) != (math.comb(n, r) if 0 <= r <= n else 0):
            bad += 1
        if permutations_count(n, r) != (math.perm(n, r) if 0 <= r <= n else 0):
            bad += 1
        if r >= 0 and combinations_count(n, r) % MOD != ncr_mod(n, r, fact, inv_fact):
            bad += 1
    for n in range(0, 40):
        if pascal_row(n) != [math.comb(n, k) for k in range(n + 1)]:
            bad += 1
        if catalan(n) != math.comb(2 * n, n) // (n + 1):
            bad += 1
    if multiset_permutations([1, 4, 4, 2]) != 34650:
        bad += 1
    print(f"  {bad} mismatches over 3,000 random pairs (3 checks each) plus 40 rows")
```

Running it:

```
THE MULTIPLICATION PRINCIPLE
  4 breads x 6 curries x 3 sweets =  72
  and with a choice of 'no sweet': 4 x 6 x 4 = 96

FACTORIALS GROW FASTER THAN ANYTHING YOU HAVE A NAME FOR
   5! =                        120   fits in 64 bits
  10! =                  3,628,800   fits in 64 bits
  15! =          1,307,674,368,000   fits in 64 bits
  20! =  2,432,902,008,176,640,000   fits in 64 bits
  21! = 51,090,942,171,709,440,000   OVERFLOWS 64 bits
  25! = 15,511,210,043,330,985,984,000,000   OVERFLOWS 64 bits

ORDER MATTERS, OR IT DOES NOT
  n= 5 r=2   nPr =           20   nCr =         10   ratio = 2! = 2
  n= 5 r=3   nPr =           60   nCr =         10   ratio = 3! = 6
  n=10 r=3   nPr =          720   nCr =        120   ratio = 3! = 6
  n=52 r=5   nPr =  311,875,200   nCr =  2,598,960   ratio = 5! = 120

PASCAL'S TRIANGLE - every entry is the two above it
                          1
                       1    1
                     1    2    1
                  1    3    3    1
                1    4    6    4    1
             1    5   10   10    5    1
           1    6   15   20   15    6    1
        1    7   21   35   35   21    7    1

THE SYMMETRY, AND WHY IT SAVES HALF THE WORK
  C(20, 3)  = 1,140
  C(20, 17) = 1,140   same number
  -> so always compute with the SMALLER of r and n-r

THE MULTIPLICATIVE FORM NEVER EXPLODES
  C(100, 50) = 100,891,344,545,564,193,334,812,497,256
  100! has 158 digits, and we never formed it
  largest intermediate value: 100,891,344,545,564,193,334,812,497,256 (30 digits)

nCr UNDER A MODULUS - precompute once, then three lookups
  C(5, 2) mod 1e9+7 = 10
  C(100, 50) mod 1e9+7 = 538,992,043
  C(200,000, 100,000) mod 1e9+7 = 879,467,333
  check small case against exact: C(100,50) mod MOD = 538,992,043

ARRANGEMENTS WITH REPEATS
  MISSISSIPPI: 11 letters, M1 I4 S4 P2
    11! / (1! 4! 4! 2!) = 34,650
    against 11! = 39,916,800 if every letter were distinct

STARS AND BARS - identical things into labelled boxes
  10 identical sweets among 4 children = C(13, 3) = 286
  10 sweets, 4 children, everyone gets at least one = C(9, 3) = 84

CATALAN NUMBERS - the same count wearing five hats
  [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]
  balanced bracket strings of length 2n; shapes of a binary tree
  with n nodes; ways to triangulate a polygon; ways to fully
  parenthesise a product.

GRID PATHS - the choose in disguise
  3 x 7 grid: C(8, 2) = 28
  3 x 3 grid: C(4, 2) = 6
  18 x 18 grid: C(34, 17) = 2,333,606,220

VERIFICATION
  0 mismatches over 3,000 random pairs (3 checks each) plus 40 rows
```

**Look at the factorial table: `20!` fits in a 64-bit integer and `21!` does not.** **That is the entire
argument for the multiplicative form**, and it is a number worth being able to state.

**Look at "largest intermediate value": it is exactly the answer.** The loop for `C(100, 50)` never holds
anything bigger than the 30-digit result, **while the formula it implements mentions a 158-digit number
twice.**

**And look at the last grid line: an 18 by 18 grid has 2.3 billion paths.** **Enumerating them is impossible;
counting them is one line** — which is the whole reason this subject exists.

---

## 6. What it costs

**The basic three.**

```
factorial(n):              n - 1 multiplications
permutations_count(n, r):  r multiplications
combinations_count(n, r):  min(r, n-r) multiply-divide pairs

  C(20, 17) without the symmetry step: 17 iterations
  C(20, 17) with it:                    3 iterations

-> O(min(r, n-r)) time, O(1) space.
```

**But there is a catch that interviewers like, and it is worth naming.** **These are `O(r)` in the number of
*operations*, not in the amount of *work*** — because the numbers themselves grow. **`C(100, 50)` is a 30-digit
number, and multiplying 30-digit numbers is not one machine instruction.** **In a fixed-width language the
distinction vanishes, because you would have overflowed instead.**

**Pascal's triangle.**

```
rows x average row length:

  n rows -> 1 + 2 + 3 + ... + n = n(n+1)/2 entries

  n = 30    ->      465 entries
  n = 1,000 ->  500,500 entries       ~4 MB in Python
  n = 10,000 -> 50,005,000 entries    ~400 MB
  n = 100,000 -> 5,000,050,000        no

-> O(n^2) time AND O(n^2) space.
-> The right tool for many small queries, useless for
   large n. That crossover is the answer to "which
   method would you use?"
```

**Precomputed factorials under a modulus.**

```
PREPARATION, limit N:
  factorials:        N multiplications
  the one inverse:   ~30 multiplications (fast power)
  the walk down:     N multiplications
  ------------------------------------------------
                     2N + 30

  N = 200,000  ->  ~400,000 operations, well under a second

WITHOUT the walk-down trick:
  one fast power per entry: N x 30 = 6,000,000
  -> 15x slower, and it is a two-line change.

EACH QUERY AFTERWARDS:
  3 lookups, 2 multiplications, 2 modulo operations
  -> O(1)

  1,000,000 queries: 400,000 + 5,000,000 operations
  against Pascal's triangle, which cannot even be built.
```

**Space for the modular tables.**

```
two lists of N+1 integers

  N = 200,000  ->  400,002 entries  ~3 MB in Python
                                     3.2 MB in C++ (int64)
  N = 10,000,000 -> ~160 MB in C++

-> Size the table to the largest n in the problem
   statement, and no larger.
```

**The named shapes.**

```
multiset_permutations: one big factorial + k small ones
  -> O(n) multiplications, but on LARGE numbers

stars_and_bars:  one nCr             -> O(min(r, n-r))
catalan(n):      one nCr of size 2n  -> O(n)
unique_paths:    one nCr             -> O(min(m, n))

  unique_paths(18, 18) -> 17 iterations
  the dynamic programming version -> 324 cells

-> Both are instant here. At 1,000 x 1,000 the DP is a
   million cells and the formula is still 999 iterations.
```

---

## 7. The traps

**Computing the factorials in the formula.**

```python
def ncr_naive(n: int, r: int) -> int:
    return factorial(n) // (factorial(r) * factorial(n - r))
```

**In Python this is correct and wasteful.** `C(100, 50)` builds a 158-digit number twice. **In C++, Java or Go
it is simply wrong: `21!` overflows a 64-bit integer, so `C(21, 2)` — whose answer is 210 — produces
nonsense.** **Say "I never form a factorial" as you write the multiplicative version.**

**And if you reach for floats to escape it:**

```python
math.factorial(1000) / math.factorial(500)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OverflowError: integer division result too large for a float
```

**A clear error, which is lucky.** The dangerous version is the one that succeeds:

```python
def ncr_float(n, r):
    result = 1.0
    for i in range(r):
        result = result * (n - i) / (i + 1)      # / not //
    return result
```

```
ncr_float(50, 25)  = 126410606437752.0                 correct
ncr_float(30, 15)  = 155117520.0                       correct
ncr_float(100, 50) = 1.0089134454556418e+29
    exact answer   = 100891344545564193334812497256
```

**It looks right on small inputs and silently loses precision past about fifteen digits.** **One character —
`/` instead of `//` — and the failure only appears on the large cases.**

**Forgetting the symmetry.**

**`C(1000, 997)` computed with `r = 997` does 997 iterations for an answer that takes three.** **Not wrong, just
foolish**, and `r = min(r, n - r)` is one line.

**Dividing before multiplying.**

```python
result = result // (i + 1) * (n - i)      # WRONG
```

**Integer division truncates.** The running value is only guaranteed to be a whole number **after** the
multiplication, **so dividing first throws away a remainder and the answer comes out too small.** **Multiply,
then divide, in that order, every time.**

**Building Pascal's triangle for a large `n`.**

```python
pascal_triangle(100_000)
```

**Five billion entries.** In Python you will run out of memory long before it finishes; **the honest failure is
that the machine stops responding**, which is worse than an exception. **Recognise the crossover: Pascal for
many queries with small `n`, precomputed factorials for large `n`.**

**Negative or out-of-range arguments.**

```python
math.comb(5, -1)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: k must be a non-negative integer
```

**The library raises. Your own version should decide deliberately** — returning 0 is usually right, because
counting problems generate impossible cases and zero is the true count.

**Fractional inputs.**

```python
math.factorial(3.5)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'float' object cannot be interpreted as an integer
```

**This is what a stray `/` produces two lines earlier.**

**Assuming independence when there is none.**

```
   6 sarees, 4 blouses -> 24.

   But if two of the blouses only go with three of
   the sarees:
     4 sarees x 4 blouses = 16
     2 sarees x 2 blouses =  4
                            --
                            20, not 24.
```

**The multiplication principle needs the second choice to be unaffected by the first.** **Nothing will tell you
this is violated — the number simply comes out too large**, and this is by far the most common conceptual error
in real counting problems. **Check by counting a tiny case by hand.**

**`nCr` under a modulus when `n` is bigger than the modulus.**

**The factorial table approach requires `n < m`**, because `fact[m]` and everything after it is zero — **`m!`
contains `m` as a factor, so it is `0 mod m`.** **For `n ≥ 10^9 + 7` you need Lucas' theorem**, and naming it is
enough; the situation is rare and the interviewer mostly wants to know that you noticed.

**Double counting, which no formula protects you from.**

```
   "How many 3-letter strings from {A, B} with at least one A?"

   WRONG: choose one position for the A (3 ways), fill the
          rest freely (2 x 2) -> 12
   TRUTH: 2^3 = 8 strings in total, minus the one with no A
          -> 7

   The wrong method counts "AAB" once for the first A and
   again for the second.
```

**When a count is suspiciously large, you have double counted.** **The fix is usually to count the complement**
— total minus the bad ones — **which is nearly always easier than counting the good ones directly.**

---

## 8. In the interview

### How it gets asked

- *"How many unique paths are there across an m by n grid?"* — LeetCode 62, and the formula answer stands out.
- *"How many ways can you arrange these letters?"* — the repeats question.
- *"Compute nCr. Now for n up to 200,000, modulo 10^9 + 7."* — precomputed factorials.
- *"How many binary search trees with n nodes?"* — Catalan, LeetCode 96.
- *"How many ways to split n identical items among k people?"* — stars and bars.
- *"Return the number of ways ... the answer may be large."* — the modulus is the tell.

### The first ninety seconds

On "how many ways can you arrange these, and now with repetitions":

> "**The first question I ask is whether order matters, and the second is whether repeats are allowed.**
> **Those two answers pick the formula, and I would rather derive it than recall it.**
>
> **If order matters and there are no repeats, it is a permutation.** Arranging all `n` things is `n!` — **and
> the reasoning is better than the formula: `n` choices for the first position, `n − 1` left for the second,
> and so on down to one.** **If I only place `r` of them, I stop after `r` factors** — `n × (n−1) × ... ×
> (n−r+1)`.
>
> **If order does not matter, it is a combination, and it is the permutation divided by `r!`.** **Because
> every group of `r` has been counted once for each order it could appear in, and there are `r!` orders.**
> **That sentence — 'I counted each answer once per arrangement, so I divide by the number of arrangements' —
> is the one I actually use**, because it fixes over-counting in problems that have no named formula.
>
> **If repeats are allowed and order matters, it is `n^r`** — `r` independent choices, each with `n` options.
> **If repeats are allowed and order does not matter, it is stars and bars**, `C(n + r − 1, r)`.
>
> **On the repeats-in-the-items version — arranging MISSISSIPPI — it is the same division argument.** Eleven
> letters would be `11!` if they were all distinct, **but the four I's are identical, so every arrangement was
> counted `4!` times over; likewise `4!` for the S's and `2!` for the P's.** **So `11!` over `1!·4!·4!·2!`,
> which is 34,650 against 39,916,800.**
>
> **And one implementation point I would make immediately, because it is where most answers break: I never
> compute a factorial.** **`21!` overflows a 64-bit integer**, so `C(21, 2)` — which is 210 — would come out as
> nonsense. **I build it up one factor at a time instead**, and the largest number the loop holds is the answer
> itself."

### The follow-ups

**"Compute nCr, for n up to 200,000, modulo 10^9 + 7."**

> "**Precompute the factorials and their inverses once, then every query is three lookups.**
>
> **The formula needs a division and I cannot divide under a modulus, so each division becomes multiplication
> by a modular inverse** — which is yesterday's Fermat, `a^(m−2) mod m`, valid because `10^9 + 7` is prime.
>
> **So I build two tables up to 200,000: `fact[i] = i! mod m`, and `inv_fact[i]`, the inverse of that.** **Then
> `C(n, r) = fact[n] × inv_fact[r] × inv_fact[n−r]`, taking the modulus between the multiplications** — in C++
> the intermediate would otherwise overflow.
>
> **There is a trick for the inverse table that I would definitely use.** **The obvious way is one fast power
> per entry — 200,000 fast powers, about six million multiplications.** **Instead compute only the last one,
> `inv_fact[N]`, and walk backwards: `inv_fact[i−1] = inv_fact[i] × i`, because `1/(i−1)!` is `1/i!` times
> `i`.** **One fast power for the whole table — about fifteen times faster, for a two-line change.**
>
> **Preparation is roughly `2N` operations, so under a second, and every query afterwards is constant time.**
> **Pascal's triangle would be the alternative and it is impossible here — the triangle for `n = 200,000` is
> twenty billion entries.** **Pascal is the right answer when `n` is small and there are many queries; tables
> are the right answer when `n` is large.**
>
> **One limitation worth naming: this needs `n` to be smaller than the modulus**, because `m!` contains `m` as
> a factor and is therefore zero. **If `n` could exceed `10^9 + 7`, that is Lucas' theorem**, which I would
> mention rather than derive."

**"How many unique paths across a grid, moving only right and down?"**

> "**It is `C(m + n − 2, m − 1)`, and the reason is nicer than the formula.**
>
> **Every path from the top-left to the bottom-right of an `m` by `n` grid is exactly `m − 1` downward moves
> and `n − 1` rightward moves, in some order.** **Every path has the same length. The only thing that
> distinguishes one path from another is which of the steps are the downward ones.**
>
> **So a path *is* a choice of `m − 1` positions out of `m + n − 2`.** For a 3 by 7 grid that is
> `C(8, 2) = 28`.
>
> **I would also say that the dynamic programming answer is correct and is what most people write** — fill a
> grid where each cell is the sum of the one above and the one to the left. **And the interesting thing is that
> the DP table *is* Pascal's triangle, rotated.** **Which is not a coincidence: Pascal's identity says
> `C(n, r) = C(n−1, r−1) + C(n−1, r)`, and 'the cell above plus the cell to the left' is the same sentence.**
>
> **On cost: the formula is `O(min(m, n))` and constant space; the DP is `O(mn)` time and `O(n)` space with one
> row.** **At 1,000 by 1,000 that is 999 operations against a million.**
>
> **The reason I would still write the DP first in some interviews is that it survives a follow-up.** **Add an
> obstacle in the middle of the grid and the closed form is gone, while the DP changes by one line.** **So I
> would give the formula, say why it works, and then say which one I would actually ship and why.**"

**"How many different shapes can a binary tree with n nodes have?"**

> "**The nth Catalan number, `C(2n, n) / (n + 1)`.** For n from zero: **1, 1, 2, 5, 14, 42, 132, 429.**
>
> **The way to get there without recalling the formula is to set up the recurrence.** **Pick which node is the
> root; then `i` nodes go in the left subtree and `n − 1 − i` in the right, and the shapes multiply.** So
> `T(n) = sum over i of T(i) × T(n−1−i)`, **which is a dynamic programme in about four lines and is what I
> would write.**
>
> **Then I would say that this sequence is the Catalan numbers and has a closed form**, and that recognising
> `1, 2, 5, 14, 42` in my own small-case working is usually how I spot it in the first place.
>
> **The thing worth adding is how many different problems this same sequence answers**, because interviewers
> follow up along that line. **Balanced bracket strings of length `2n`. Shapes of a binary tree with `n` nodes.
> Ways to triangulate a polygon. Ways to fully parenthesise a product of `n + 1` factors. Monotone lattice
> paths that stay below the diagonal.**
>
> **They are all the same count because they all have the same recurrence: split into a left part and a right
> part, and multiply.** **If a problem's small cases are 1, 2, 5, 14, that is what is happening, and I would
> look for the split rather than keep enumerating.**"

### The model answer

*"Talk me through how you approach a counting problem."*

> "**Four steps, in this order, and I try not to skip the first one even when the answer looks obvious.**
>
> **First, I count a tiny case by hand.** Three items, four items. **Not to find the answer, but because an
> exhaustive count of a small case is the only check I have on a formula that produces a number too large to
> verify.** **And if my small cases come out 1, 2, 5, 14, I already know it is Catalan.**
>
> **Second, I ask the two questions: does order matter, and can things repeat.** **That picks the shape.**
> Order and no repeats is a permutation. No order and no repeats is a combination. Order with repeats is
> `n^r`. No order with repeats is stars and bars. **I derive rather than recall, because the derivation is
> short: `n` choices, then `n − 1`, and so on.**
>
> **Third, I look for over-counting, because that is where the real errors are.** **The sentence I use is: 'how
> many times has each answer been counted?' — and then I divide by that.** Combinations divide by `r!` because
> each group appears once per ordering. **MISSISSIPPI divides by `4!·4!·2!` because each arrangement appears
> once per shuffle of the identical letters.** **And when a count comes out suspiciously large, over-counting
> is nearly always the cause — the usual fix is to count the complement instead: total minus the bad ones.**
>
> **Fourth, I worry about the arithmetic, and this is where most solutions actually fail.** **`21!` overflows a
> 64-bit integer**, so I never compute a factorial: **I build `nCr` one factor at a time, multiplying then
> dividing, using the smaller of `r` and `n − r`.** **The largest value that loop ever holds is the answer
> itself.** **And if the problem says 'modulo 10^9 + 7', that is the tell that the answer is astronomically
> large — so precomputed factorial and inverse-factorial tables, with the inverses built by one fast power and
> a walk down.**
>
> **The judgement call I would flag is between a formula and a dynamic programme.** **Grid paths have a closed
> form and the DP is a million times slower — but put one obstacle in the grid and the closed form disappears
> while the DP changes by a single line.** **So I say which one I would write for the problem as stated, and
> which one I would write if I expected the requirements to move.**
>
> **And the one assumption I check explicitly is independence.** **The multiplication principle needs the
> second choice to be unaffected by the first.** **Nothing warns you when that fails — the number just comes
> out too big — and it is the most common conceptual mistake in this whole area.**"

---

## 9. Recall card

**Two questions decide everything: DOES ORDER MATTER, and CAN THINGS REPEAT.** Order + no repeats = **nPr**;
no order + no repeats = **nCr**; order + repeats = **nʳ**; no order + repeats = **stars and bars,
C(n+r−1, r)**. **Derive, do not recall: `n` choices, then `n−1`, then `n−2` — and stop after `r` factors.**

**The most useful sentence in the subject: "I counted each answer once per arrangement, so I divide by the
number of arrangements."** `nCr = nPr / r!`. **MISSISSIPPI = 11!/(1!·4!·4!·2!) = 34,650.** **When a count comes
out too big you have double counted — usually the fix is to count the COMPLEMENT.** And **the multiplication
principle needs independence**; nothing warns you when the second choice is limited by the first.

**NEVER COMPUTE A FACTORIAL. `21!` overflows a 64-bit integer**, so `C(21,2)` = 210 comes back as nonsense.
Build up: `result = result * (n - i) // (i + 1)`, **multiply before you divide** (the division is exact only
after the multiplication), and **use `r = min(r, n-r)`** — 3 iterations, not 17, for `C(20,17)`. **`//` not
`/`: the float version is right on small inputs and quietly wrong past ~15 digits.**

**`C(n,r) = C(n−1,r−1) + C(n−1,r)` is "the item is in, or it is out"** — which is why counting problems become
DP, and why Pascal's triangle IS the grid-paths table. **Row `n` sums to 2ⁿ, because it is every subset sorted
by size.** **Pascal is O(n²) time and space** — right for many small queries, impossible at n = 100,000.

**Modulo 10⁹+7 is the tell that the answer is astronomical.** Precompute `fact[]` and `inv_fact[]`, then
`C(n,r) = fact[n] · inv_fact[r] · inv_fact[n−r]` — **three lookups, O(1) per query.** Build the inverses with
**ONE fast power at the top and a walk down** (`inv_fact[i-1] = inv_fact[i] * i`), 15× faster than one power
each. Requires **n < modulus**, else Lucas' theorem. **Recognise the shapes: grid paths = C(m+n−2, m−1);
Catalan = C(2n,n)/(n+1) = 1, 1, 2, 5, 14, 42, 132 for brackets, tree shapes and parenthesisations; subsets =
2ⁿ.**
