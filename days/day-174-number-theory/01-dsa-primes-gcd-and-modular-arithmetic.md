---
day: 174
track: dsa
title: "Primes, GCD, and modular arithmetic"
phase: "Bits and maths"
status: written
---

# Primes, GCD, and modular arithmetic

## 1. What this is, and why they ask it

**A prime is a number with exactly two divisors: one and itself.** **A GCD is the largest number that divides
two others exactly.** **Modular arithmetic is arithmetic that wraps round, the way a clock does.**

Those three ideas cover almost all the mathematics an interview will ask you for, **and each of them has one
technique attached that is far faster than the obvious approach.**

**The sieve, instead of testing each number.** **Euclid's algorithm, instead of listing divisors.** **Square
and multiply, instead of multiplying a billion times.** Each one turns something impossible into something
instant, **and each one is about six lines.**

They ask it because **these appear as sub-steps inside larger problems far more often than as questions of
their own.** A counting problem says "answer modulo 10^9 + 7" — **that is this lesson.** A problem about
repeating patterns turns out to be about a GCD. A problem about arrangements needs a fast power.

**And because they are a fair test of whether you reach for the obvious loop.** "Find all primes below a
million" has an answer that takes a second and an answer that takes twenty minutes, **and the difference is a
single change of viewpoint: stop asking about each number, and start crossing off.**

By the end of this lesson you can test primality properly, sieve a million primes, factorise any number
instantly after one preparation pass, compute a GCD and an LCM without overflowing, do arithmetic under a
modulus including division, and say why `10^9 + 7` is on every competitive problem you have ever read.

---

## 2. The story

There were about sixty names in Ashfaq's phone under a group called SUNDAY, and getting eleven of them onto
the maidan by six in the morning was the hardest thing he did all week.

For two years he did it by asking. He would start on Thursday evening and go down the group, one call at a
time. **"Are you free on Sunday?"** Sixty calls, of which perhaps forty were answered, of which about eleven
said yes — **and by the time he got to the end it was Friday night and two of the eleven had changed their
minds.**

What fixed it was a conversation at the tea stall with a man who ran the shifts at the mill.

Ashfaq was complaining, at some length. The man listened and then asked something that sounded almost rude.

**"Why are you asking the people? Ask the reasons."**

And once he said it, it was obvious. **Almost everybody who could not come was unable for one of about five
reasons, and each reason had one person who already knew the whole list.**

The mill ran a Sunday shift, and the supervisor could say who was on it. The eight or nine who drove for the
travel company were all on one roster, and one man had it. The students had their tuition on Sunday mornings,
all of them, at the same place. **Four or five of them were the sort whose in-laws visited, and their wives
were all in one group that knew everything.**

So on Thursday, Ashfaq sent five messages instead of making sixty calls.

Each one came back with names. He took those names out of the group as they arrived. **The mill supervisor
alone removed fourteen.**

**What was left was nineteen names, and those he actually rang.** Eleven yeses in about forty minutes, and he
was finished before the shop shut.

The thing that stayed with him was what the man said afterwards, when Ashfaq told him it had worked.

**"You were asking sixty questions to find eleven answers. Ask five questions that each rule out ten people,
and you are done before the tea goes cold."**

---

## 3. The idea in plain English

**Ashfaq's five messages are a sieve.** He did not examine each of the sixty. **He took whole groups of them
off the list at once, using something that was already known.** That is the difference between testing every
number for primality and crossing off multiples.

### What a prime is

**A prime has exactly two divisors: 1 and itself.** 2, 3, 5, 7, 11, 13, 17.

**Two things people get wrong and interviewers check.** **1 is not prime** — it has one divisor, not two.
**2 is prime, and it is the only even prime**, which is why every prime routine has a special case for it.

### Testing one number

**The obvious test tries every divisor from 2 up to n − 1.** For 1,000,003 that is a million divisions.

**You only need to go up to the square root, and the reason is worth saying out loud.**

```
   If n = a x b, then a and b cannot BOTH be bigger
   than sqrt(n) - because then a x b would be bigger than n.

   So EVERY composite number has a divisor at or below
   its square root. If you find none there, there is none.

   n = 1,000,003
     testing to n-1     -> 1,000,002 divisions
     testing to sqrt(n) ->     1,000 divisions
                        -> 1,000x fewer
```

**And you can do better with almost no effort.** After ruling out 2 and 3, **every prime is one either side of
a multiple of six** — 5, 7, 11, 13, 17, 19. Anything else is divisible by 2 or by 3.

```
   6k     divisible by 6
   6k + 1   <- can be prime
   6k + 2   divisible by 2
   6k + 3   divisible by 3
   6k + 4   divisible by 2
   6k + 5   <- can be prime   (same as 6k - 1)

   -> step by 6 and test two candidates each time:
      a third of the work again.
```

### The sieve, which is the real idea

**Ashfaq's move.** To find every prime below a million, **do not ask a million questions. Cross off.**

```
   Write down 2 to 30.
   Take 2. Cross off 4, 6, 8, 10 ...  everything left is
     not divisible by 2.
   Take 3, the next survivor. Cross off 9, 15, 21, 27.
   Take 5. Cross off 25.
   Stop - 7 x 7 is 49, past the end.

   WHAT SURVIVES IS THE ANSWER:
   2 3 5 7 11 13 17 19 23 29
```

**This is the Sieve of Eratosthenes**, and it is about two thousand two hundred years old.

**Two details make it fast, and both are asked about.**

**Start crossing off at `p × p`, not at `2p`.** Every multiple of 5 below 25 — 10, 15, 20 — **was already
crossed off by 2 and by 3.** Starting at the square skips work you have already done.

**Stop when `p × p` exceeds the limit.** If a number below the limit has any factor at all, it has one at or
below the square root, **so by the time you have sieved up to the square root, everything composite is already
gone.**

### Factorising, after one sieve

**A small variation makes factorising instant.** Instead of storing "is it prime", store **the smallest prime
that divides each number.**

```
   spf[12] = 2      spf[35] = 5      spf[97] = 97

   To factorise 360:
     spf[360] = 2   ->  360 / 2 = 180
     spf[180] = 2   ->  180 / 2 = 90
     spf[90]  = 2   ->  90 / 2  = 45
     spf[45]  = 3   ->  45 / 3  = 15
     spf[15]  = 3   ->  15 / 3  = 5
     spf[5]   = 5   ->  5 / 5   = 1

   -> 360 = 2^3 x 3^2 x 5
```

**Each step at least halves the number, so it takes at most `log2(n)` steps** — about twenty for a million.
**One sieve, then any number factorised in twenty operations.**

### The GCD, and Euclid

**The greatest common divisor of 1071 and 462 is the biggest number that divides both.**

**The naive answer tries every number from the smaller one downwards.** The good answer is one line, and it is
about as old as the sieve.

**Euclid's insight: the common divisors of `a` and `b` are exactly the common divisors of `b` and `a mod b`.**

**Here is why, and it is worth being able to say.** If some number `d` divides both `a` and `b`, then **it also
divides whatever is left over when you take `b` out of `a` as many times as you can** — because you removed a
pile of things that `d` already divided. **So the set of common divisors never changes**, and each step makes
the numbers smaller.

```
   gcd(1071, 462)  ->  1071 mod 462 = 147
   gcd( 462, 147)  ->   462 mod 147 = 21
   gcd( 147,  21)  ->   147 mod  21 = 0
   gcd(  21,   0)  ->   21

   Three steps. The naive search would have tried
   462 candidates.
```

**And the LCM comes free**: `a × b = gcd(a, b) × lcm(a, b)`, so **`lcm = a / gcd × b`.**

**Divide first.** `a * b // gcd` computes the product before dividing, **and in any language with fixed-width
integers that product overflows for large inputs.** `a // gcd * b` never gets bigger than the answer.

### Modular arithmetic

**Arithmetic that wraps.** On a clock, 10 o'clock plus 5 hours is 3 o'clock: **15 mod 12 = 3.**

**Three rules survive the wrap, and one does not.**

```
   (a + b) % m  ==  ((a % m) + (b % m)) % m       yes
   (a - b) % m  ==  ((a % m) - (b % m)) % m       yes*
   (a * b) % m  ==  ((a % m) * (b % m)) % m       yes

   (a / b) % m  ==  ((a % m) / (b % m)) % m       NO
```

**Addition, subtraction and multiplication all pass through the modulus.** **Division does not, and that is
the whole reason modular inverses exist.**

**The asterisk on subtraction is a language difference, not a maths one.** **In Python, `-7 % 10` is `3`** —
the result always has the sign of the modulus. **In C, C++, Java and Go it is `-7`.** So in those languages you
write `((a - b) % m + m) % m`, **and forgetting it produces negative answers on a problem that promised
non-negative ones.**

### Why 10^9 + 7

**Because counting problems produce enormous answers, and the setter wants a fixed-width answer.**

**Three properties, and it is worth knowing all three.** **It is prime**, which is what makes division work via
Fermat's theorem below. **It is just over a billion, so it fits in a 32-bit signed integer.** **And two values
under it multiply to just under 10^18, which still fits in a 64-bit integer** — so `a * b % m` is safe in C++
and Java without any special handling. **That last one is why it is exactly this number and not some other
prime.**

### Fast power: square and multiply

**Computing `3^13` by multiplying thirteen times is fine. Computing `2^1000000000` that way is not.**

**Use the binary expansion of the exponent.**

```
   13 = 1101 in binary = 8 + 4 + 1

   3^13 = 3^8 x 3^4 x 3^1

   and you get 3^1, 3^2, 3^4, 3^8 by squaring repeatedly:
     3^1 = 3
     3^2 = 9
     3^4 = 81
     3^8 = 6561

   -> four squarings and two multiplications,
      instead of thirteen multiplications.
```

**For an exponent of a billion that is thirty squarings instead of a billion multiplications.** **The loop is
"if the low bit is set, multiply it in; then square the base and shift the exponent right"** — which is
yesterday's bit walk doing real work.

### Division under a modulus

**You cannot divide, so you multiply by an inverse.** **The inverse of `a` is the number `x` with
`a × x ≡ 1 (mod m)`** — the modular version of `1/a`.

**Fermat's little theorem gives it in one line when the modulus is prime**: `a^(m−2) mod m` is the inverse of
`a`. **And you compute that with the fast power you just wrote.**

```
   inverse of 3 mod 1,000,000,007 = 3^1000000005 mod m
                                  = 333,333,336

   check: 3 x 333,333,336 mod m = 1     correct

   so "10 / 2" under the modulus is
     10 x inverse(2) mod m = 5
```

**Two conditions, and both matter.** **The modulus must be prime** for Fermat. **And `a` must not be a multiple
of the modulus**, or no inverse exists at all.

**If the modulus is not prime, use the extended Euclidean algorithm instead** — it finds `x` and `y` with
`ax + my = gcd(a, m)`, **and when the gcd is 1, that `x` is the inverse.** **This is the safe general answer,
and it is worth naming even if you write the Fermat version.**

---

## 4. The picture

The sieve, crossing off:

```
   2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
   ------------------------------------------------------

   take 2, cross from 2x2 = 4, step 2:
   2  3  X  5  X  7  X  9  X 11  X 13  X 15  X 17  X 19  X

   take 3, cross from 3x3 = 9, step 3:
   2  3  X  5  X  7  X  X  X 11  X 13  X  X  X 17  X 19  X

   take 5? 5x5 = 25, past the end. STOP.

   survivors: 2 3 5 7 11 13 17 19

   TWO THINGS TO NOTICE

   Starting at p x p, not 2p: when we reached 3, the numbers
   6 and 3x2 were already gone - 2 killed them. Every multiple
   of p below p x p has a smaller prime factor, so it is
   already crossed off.

   Stopping at sqrt: any composite below 20 has a factor at or
   below 4.47, so 2 and 3 between them have already killed
   every composite here.
```

Euclid, as squares cut off a rectangle:

```
   gcd(1071, 462) - lay out a rectangle 1071 long and 462 high
   and cut off the biggest squares you can.

   +---------+---------+-----+
   |  462    |  462    | 147 |   1071 = 2 x 462 + 147
   |         |         |     |
   +---------+---------+-----+
                        <-->
                    what is left is 147 high... no,
                    147 WIDE and 462 high. Turn it:

   +-----+-----+-----+---+
   | 147 | 147 | 147 |21 |         462 = 3 x 147 + 21
   +-----+-----+-----+---+

   +--+--+--+--+--+--+--+
   |21|21|21|21|21|21|21|          147 = 7 x 21 + 0
   +--+--+--+--+--+--+--+
                                   NOTHING LEFT OVER.

   -> 21 is the largest square that tiles the original
      rectangle exactly. That is the GCD.

   Each step: replace the rectangle with the leftover strip.
   Three steps to go from 1071 to 21.
```

Square and multiply, drawn:

```
   3^13,  and 13 = 1 1 0 1
                   8 4 2 1

   exponent  bit   base        result
   --------  ---   ---------   ------------------
   13        1     3           3                 (multiply in)
   6         0     9           3                 (skip)
   3         1     81          3 x 81 = 243      (multiply in)
   1         1     6561        243 x 6561        (multiply in)
                               = 1,594,323

   check: 3^13 = 1,594,323

   The base column is repeated squaring: 3, 9, 81, 6561.
   The bit column is just the binary of 13, read from the
   bottom up.

   -> exponent of 1,000,000,000 -> 30 rows, not a billion.
```

The three-way relationship worth carrying:

```
   a x b = gcd(a, b) x lcm(a, b)

   1071 x 462 = 494,802
   gcd = 21, lcm = 23,562
   21 x 23,562 = 494,802            correct

   -> lcm(a, b) = a / gcd x b

   DIVIDE FIRST. a x b overflows a 64-bit integer for
   a, b around 10^10; a / gcd x b never exceeds the answer.
```

---

## 5. The code, built step by step

### Testing one number

```python
def is_prime(n: int) -> bool:
    """Trial division, but only up to the square root, and only over 6k +/- 1."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    factor = 5
    while factor * factor <= n:
        if n % factor == 0 or n % (factor + 2) == 0:
            return False
        factor += 6
    return True
```

**The first three lines are the whole edge-case story**: `1` is not prime, `2` and `3` are, everything else
even or divisible by three is not. **Write those before the loop, always.**

**`factor * factor <= n` rather than `factor <= sqrt(n)` keeps you in integers.** **One multiplication per
iteration is cheaper than a square root, and there is no floating-point rounding to worry about.** If you
prefer the square root, use `math.isqrt(n)`, which is exact.

### The sieve

```python
def sieve(limit: int) -> list[int]:
    """Every prime below `limit`. Do not test each number - cross off the multiples."""
    if limit < 3:
        return []
    prime = [True] * limit
    prime[0] = prime[1] = False
    p = 2
    while p * p < limit:
        if prime[p]:
            prime[p * p:limit:p] = [False] * len(range(p * p, limit, p))
        p += 1
    return [i for i, still in enumerate(prime) if still]
```

**`prime[p*p:limit:p] = [False] * ...` is a slice assignment, and it is the reason this is fast in Python.**
A plain `for` loop over the multiples does the same work in interpreted code; **the slice does it in C.** On a
million-element sieve that is roughly a fivefold difference.

**`while p * p < limit` is the stopping rule from section 3**, and **`p * p` is the starting point.** Both are
the same fact seen from two ends.

### Factorising with a prepared table

```python
def smallest_prime_factors(limit: int) -> list[int]:
    """spf[n] is the smallest prime dividing n. One sieve, then factorise anything fast."""
    spf = list(range(limit))
    p = 2
    while p * p < limit:
        if spf[p] == p:
            for multiple in range(p * p, limit, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
        p += 1
    return spf
```

**`spf[p] == p` is how you ask "is `p` still prime?"** — nothing has claimed it yet. **And `if spf[multiple] ==
multiple` is what keeps the *smallest* factor**: once something has written there, a later, larger prime must
not overwrite it.

```python
def factorise(n: int, spf: list[int]) -> dict[int, int]:
    """Divide out the smallest prime factor, over and over. At most log2(n) steps."""
    factors: dict[int, int] = {}
    while n > 1:
        p = spf[n]
        factors[p] = factors.get(p, 0) + 1
        n //= p
    return factors
```

**Each division at least halves `n`**, because the smallest prime factor is at least 2. **So the loop runs at
most `log2(n)` times — twenty for a million** — regardless of how ugly the number is.

### Euclid, and the LCM

```python
def gcd(a: int, b: int) -> int:
    """Euclid: the common measure of (a, b) is the common measure of (b, a mod b)."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Divide FIRST, or a * b overflows in every fixed-width language."""
    return a // gcd(a, b) * b
```

**Two lines, and the tuple assignment does the shuffle without a temporary.** **It works with the arguments in
either order** — if `a < b`, the first iteration simply swaps them, at the cost of one wasted step.

**`gcd(a, 0)` is `a`, and that is correct rather than a special case**: every number divides zero, so the
greatest common divisor of `a` and nothing is `a` itself. **`gcd(0, 0)` is `0`, which is the conventional
answer.**

### Fast power

```python
def power_mod(base: int, exponent: int, modulus: int) -> int:
    """Square and multiply. 30 steps for an exponent of a billion, not a billion steps."""
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result
```

**Read it against the table in section 4 and it maps line for line.** `exponent & 1` asks whether this power of
the base is one of the ones you need. `base = base * base` climbs to the next power. `exponent >>= 1` moves to
the next bit.

**The `% modulus` after every multiplication is not optional.** **Without it the numbers grow to millions of
digits** — Python will not overflow, it will simply get slower and slower until it stops being useful.

### The modular inverse

```python
def inverse_mod(a: int, modulus: int = MOD) -> int:
    """Fermat: when the modulus is prime, a^(m-2) is a's inverse. Division, at last."""
    return power_mod(a, modulus - 2, modulus)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Returns (g, x, y) with a*x + b*y = g. The x is the modular inverse when g is 1."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y
```

**One line, and it costs one fast power.** **In an interview, say the precondition out loud as you write it:
"this needs the modulus to be prime, which `10^9 + 7` is."**

**The extended version is the general answer** — it works for any modulus coprime with `a`, and it does not
need a prime. **The swap in the return line is where people get lost**, so if you write it, **write the base
case first and trace one small example.**

### The complete solution

```python
"""Day 174 - primes, GCD, and modular arithmetic. The maths interviews actually use."""

from __future__ import annotations

MOD = 1_000_000_007


def is_prime(n: int) -> bool:
    """Trial division, but only up to the square root, and only over 6k +/- 1."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    factor = 5
    while factor * factor <= n:
        if n % factor == 0 or n % (factor + 2) == 0:
            return False
        factor += 6
    return True


def sieve(limit: int) -> list[int]:
    """Every prime below `limit`. Do not test each number - cross off the multiples."""
    if limit < 3:
        return []
    prime = [True] * limit
    prime[0] = prime[1] = False
    p = 2
    while p * p < limit:
        if prime[p]:
            prime[p * p:limit:p] = [False] * len(range(p * p, limit, p))
        p += 1
    return [i for i, still in enumerate(prime) if still]


def smallest_prime_factors(limit: int) -> list[int]:
    """spf[n] is the smallest prime dividing n. One sieve, then factorise anything fast."""
    spf = list(range(limit))
    p = 2
    while p * p < limit:
        if spf[p] == p:
            for multiple in range(p * p, limit, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
        p += 1
    return spf


def factorise(n: int, spf: list[int]) -> dict[int, int]:
    """Divide out the smallest prime factor, over and over. At most log2(n) steps."""
    factors: dict[int, int] = {}
    while n > 1:
        p = spf[n]
        factors[p] = factors.get(p, 0) + 1
        n //= p
    return factors


def gcd(a: int, b: int) -> int:
    """Euclid: the common measure of (a, b) is the common measure of (b, a mod b)."""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Divide FIRST, or a * b overflows in every fixed-width language."""
    return a // gcd(a, b) * b


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Returns (g, x, y) with a*x + b*y = g. The x is the modular inverse when g is 1."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def power_mod(base: int, exponent: int, modulus: int) -> int:
    """Square and multiply. 30 steps for an exponent of a billion, not a billion steps."""
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def inverse_mod(a: int, modulus: int = MOD) -> int:
    """Fermat: when the modulus is prime, a^(m-2) is a's inverse. Division, at last."""
    return power_mod(a, modulus - 2, modulus)


if __name__ == "__main__":
    print("IS IT PRIME - stop at the square root")
    for n in (1, 2, 17, 91, 97, 1_000_003):
        root = int(n ** 0.5)
        print(f"  {n:>9}  prime={str(is_prime(n)):<5}  sqrt={root:>4}"
              f"  trial divisions saved: {n} -> ~{root // 3}")

    print()
    print("THE SIEVE - cross off multiples instead of testing numbers")
    print(f"  primes below 50: {sieve(50)}")
    print(f"  how many below 1,000,000: {len(sieve(1_000_000)):,}")
    print(f"  how many below 10,000,000: {len(sieve(10_000_000)):,}")

    print()
    print("CROSSING OFF, STEP BY STEP, BELOW 30")
    limit = 30
    flags = [True] * limit
    flags[0] = flags[1] = False
    for p in (2, 3, 5):
        killed = [m for m in range(p * p, limit, p) if flags[m]]
        for m in killed:
            flags[m] = False
        print(f"  start at {p}x{p}={p * p}, cross off every {p}: {killed}")
    print(f"  what survives: {[i for i, f in enumerate(flags) if f]}")

    print()
    print("FACTORISING WITH A SIEVE")
    spf = smallest_prime_factors(1000)
    for n in (12, 97, 360, 999):
        print(f"  {n:>4} = {factorise(n, spf)}")

    print()
    print("EUCLID - each step is one remainder")
    a, b = 1071, 462
    steps = 0
    x, y = a, b
    while y:
        print(f"  gcd({x:>5}, {y:>4})  ->  {x} mod {y} = {x % y}")
        x, y = y, x % y
        steps += 1
    print(f"  gcd = {x}, in {steps} steps")
    print(f"  lcm(1071, 462) = {lcm(1071, 462)}")
    print(f"  gcd(0, 5) = {gcd(0, 5)}   gcd(5, 0) = {gcd(5, 0)}   gcd(0, 0) = {gcd(0, 0)}")

    print()
    print("FAST POWER - square and multiply")
    print(f"  3^13 the long way = {3 ** 13}")
    print(f"  power_mod(3, 13, 1000000007) = {power_mod(3, 13, MOD)}")
    print("  13 = 1101 in binary, so:")
    print("    3^13 = 3^8 * 3^4 * 3^1 = 6561 * 81 * 3 = 1594323")
    print(f"  power_mod(2, 1000000000, MOD) = {power_mod(2, 1_000_000_000, MOD)}"
          f"   in {1_000_000_000 .bit_length()} squarings")

    print()
    print("MODULAR ARITHMETIC - what survives and what does not")
    big_a, big_b = 987_654_321_987, 123_456_789_123
    print(f"  (a + b) % m == (a%m + b%m) % m   -> "
          f"{(big_a + big_b) % MOD == (big_a % MOD + big_b % MOD) % MOD}")
    print(f"  (a * b) % m == (a%m * b%m) % m   -> "
          f"{(big_a * big_b) % MOD == (big_a % MOD * (big_b % MOD)) % MOD}")
    print(f"  (a - b) % m works in Python     -> {(3 - 10) % MOD}")
    print("  ... but in C/Java (3 - 10) % m is -7, so you add m and take % again")
    print("  (a / b) % m is NOT (a%m / b%m)  -> division needs an INVERSE")

    print()
    print("DIVISION UNDER A MODULUS, VIA FERMAT")
    inv3 = inverse_mod(3)
    print(f"  inverse of 3 mod 1e9+7 = {inv3}")
    print(f"  check: 3 * inv3 % MOD  = {3 * inv3 % MOD}")
    print(f"  10 / 2 under the modulus = {10 * inverse_mod(2) % MOD}")
    print(f"  1 / 7 under the modulus  = {inverse_mod(7)}"
          f"   and 7 * that = {7 * inverse_mod(7) % MOD}")

    print()
    print("EXTENDED EUCLID gives the same inverse without a prime modulus")
    g, x, y = extended_gcd(3, MOD)
    print(f"  3*x + MOD*y = {g},  x = {x % MOD}")
    print(f"  matches Fermat: {x % MOD == inv3}")

    print()
    print("VERIFICATION")
    import math
    import random

    bad = 0
    primes_below = set(sieve(20_000))
    for n in range(2, 20_000):
        if is_prime(n) != (n in primes_below):
            bad += 1
    spf_big = smallest_prime_factors(50_000)
    for _ in range(2000):
        n = random.randint(2, 49_999)
        product = 1
        for p, e in factorise(n, spf_big).items():
            product *= p ** e
        if product != n:
            bad += 1
        a = random.randint(0, 10 ** 12)
        b = random.randint(1, 10 ** 12)
        if gcd(a, b) != math.gcd(a, b):
            bad += 1
        if lcm(a, b) != math.lcm(a, b):
            bad += 1
        base = random.randint(1, 10 ** 9)
        exp = random.randint(0, 10 ** 6)
        if power_mod(base, exp, MOD) != pow(base, exp, MOD):
            bad += 1
        if base % MOD and base * inverse_mod(base) % MOD != 1:
            bad += 1
    print(f"  {bad} mismatches: 20,000 primality checks and 2,000 random cases, 5 checks each")
```

Running it:

```
IS IT PRIME - stop at the square root
          1  prime=False  sqrt=   1  trial divisions saved: 1 -> ~0
          2  prime=True   sqrt=   1  trial divisions saved: 2 -> ~0
         17  prime=True   sqrt=   4  trial divisions saved: 17 -> ~1
         91  prime=False  sqrt=   9  trial divisions saved: 91 -> ~3
         97  prime=True   sqrt=   9  trial divisions saved: 97 -> ~3
    1000003  prime=True   sqrt=1000  trial divisions saved: 1000003 -> ~333

THE SIEVE - cross off multiples instead of testing numbers
  primes below 50: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
  how many below 1,000,000: 78,498
  how many below 10,000,000: 664,579

CROSSING OFF, STEP BY STEP, BELOW 30
  start at 2x2=4, cross off every 2: [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
  start at 3x3=9, cross off every 3: [9, 15, 21, 27]
  start at 5x5=25, cross off every 5: [25]
  what survives: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

FACTORISING WITH A SIEVE
    12 = {2: 2, 3: 1}
    97 = {97: 1}
   360 = {2: 3, 3: 2, 5: 1}
   999 = {3: 3, 37: 1}

EUCLID - each step is one remainder
  gcd( 1071,  462)  ->  1071 mod 462 = 147
  gcd(  462,  147)  ->  462 mod 147 = 21
  gcd(  147,   21)  ->  147 mod 21 = 0
  gcd = 21, in 3 steps
  lcm(1071, 462) = 23562
  gcd(0, 5) = 5   gcd(5, 0) = 5   gcd(0, 0) = 0

FAST POWER - square and multiply
  3^13 the long way = 1594323
  power_mod(3, 13, 1000000007) = 1594323
  13 = 1101 in binary, so:
    3^13 = 3^8 * 3^4 * 3^1 = 6561 * 81 * 3 = 1594323
  power_mod(2, 1000000000, MOD) = 140625001   in 30 squarings

MODULAR ARITHMETIC - what survives and what does not
  (a + b) % m == (a%m + b%m) % m   -> True
  (a * b) % m == (a%m * b%m) % m   -> True
  (a - b) % m works in Python     -> 1000000000
  ... but in C/Java (3 - 10) % m is -7, so you add m and take % again
  (a / b) % m is NOT (a%m / b%m)  -> division needs an INVERSE

DIVISION UNDER A MODULUS, VIA FERMAT
  inverse of 3 mod 1e9+7 = 333333336
  check: 3 * inv3 % MOD  = 1
  10 / 2 under the modulus = 5
  1 / 7 under the modulus  = 142857144   and 7 * that = 1

EXTENDED EUCLID gives the same inverse without a prime modulus
  3*x + MOD*y = 1,  x = 333333336
  matches Fermat: True

VERIFICATION
  0 mismatches: 20,000 primality checks and 2,000 random cases, 5 checks each
```

**Look at the crossing-off trace.** **Two crossed off thirteen numbers, three crossed off four more, and five
crossed off exactly one.** Each prime does progressively less work, because the earlier ones have already
killed most of its multiples — **and that is the intuition behind the sieve's surprising cost in section 6.**

**Look at the prime counts: 78,498 below a million and 664,579 below ten million.** **Ten times the range gives
only 8.5 times as many primes.** They thin out, slowly, and the density near `n` is about `1 / ln n`.

**And look at the modular subtraction line: `(3 - 10) % MOD` is 1,000,000,000 in Python.** **A large positive
number, which is the mathematically correct representative.** In C or Java the same expression gives −7.
**Same maths, different language convention, and it is a real source of wrong answers.**

---

## 6. What it costs

**Testing one number.**

```
naive: divide by 2, 3, 4, ..., n-1

  n = 1,000,003  ->  1,000,001 divisions

to the square root:

  n = 1,000,003  ->  ~1,000 divisions
  n = 10^12      ->  ~1,000,000 divisions
  n = 10^18      ->  ~1,000,000,000  - too slow

only 6k +/- 1:

  a third again: ~333 divisions for 1,000,003

-> O(sqrt(n)) time, O(1) space.
-> Fine up to about 10^14. Beyond that you need
   Miller-Rabin, and it is enough to name it.
```

**The sieve — and the counting here is the interesting part.**

```
for p = 2: cross off limit/2 numbers
for p = 3: cross off limit/3
for p = 5: cross off limit/5
...

total = limit x (1/2 + 1/3 + 1/5 + 1/7 + 1/11 + ...)

The sum of the reciprocals of the primes below n
grows like ln(ln(n)) - very slowly indeed.

-> O(n log log n), which for any practical n is
   "a small constant times n".

  limit = 1,000,000   ->  ~2.8 million operations   ~0.1 s
  limit = 10,000,000  ->  ~30 million operations    ~1-2 s
  limit = 100,000,000 ->  memory becomes the problem first

COMPARE: testing each number separately
  1,000,000 numbers x ~333 divisions each
  = 333,000,000 operations, roughly 100x slower.
```

**Space is what actually stops the sieve.**

```
a Python list of booleans: ~8 bytes per entry (a pointer)

  limit = 1,000,000    ->  ~8 MB       fine
  limit = 10,000,000   ->  ~80 MB      fine
  limit = 100,000,000  ->  ~800 MB     painful
  limit = 1,000,000,000 -> ~8 GB       no

a bytearray: 1 byte per entry
  limit = 100,000,000  ->  100 MB      workable

a bitset: 1 bit per entry
  limit = 1,000,000,000 -> 125 MB      workable

-> The time is fine long before the memory is.
   If asked for primes below 10^9, say "segmented sieve":
   sieve in blocks that fit in cache, using the primes
   below sqrt(10^9) = 31,623.
```

**Factorising.**

```
with the spf table, each step at least halves n:

  n = 1,000,000  ->  at most 20 steps
  n = 2^20       ->  exactly 20 steps (all 2s)
  n = 999,983 (prime) -> 1 step

-> O(log n) per number, after an O(n log log n) sieve.

without the table, trial division per number:
  O(sqrt(n)) each -> 1,000 steps for a million.

-> 50x per query, so the table pays for itself
   after about 3,000 queries.
```

**Euclid.**

```
gcd(1071, 462): 3 steps
gcd(10^18, 10^18 - 1): 2 steps

WORST CASE is consecutive Fibonacci numbers - each step
reduces by the smallest possible amount:

  gcd(89, 55) -> 55, 34 -> 34, 21 -> 21, 13 -> 13, 8
              -> 8, 5 -> 5, 3 -> 3, 2 -> 2, 1 -> 1, 0
  9 steps for numbers under 100

-> O(log min(a, b)). Concretely, at most about 5 times
   the number of decimal digits.

  a, b around 10^18  ->  at most ~90 steps

Compare with "try every divisor downwards":
  10^18 candidates. Not a competition.
```

**Fast power.**

```
one squaring per bit of the exponent:

  exponent 13            ->  4 steps
  exponent 1,000         ->  10 steps
  exponent 1,000,000,000 ->  30 steps
  exponent 10^18         ->  60 steps

-> O(log exponent) multiplications, each on numbers
   below the modulus.

the naive loop for 10^9: 1,000,000,000 multiplications
-> about 33 million times more work.
```

**Modular inverse via Fermat is one fast power**, so `O(log m)` — **about thirty multiplications for
`10^9 + 7`.** **Extended Euclid is `O(log m)` too and is usually a little faster**, so the choice between them
is about preconditions, not speed.

**Space, across the lesson.**

```
is_prime, gcd, lcm, power_mod, inverse_mod:   O(1)
sieve:                                        O(n)
smallest_prime_factors:                       O(n)
factorise:                                    O(log n) for the result
extended_gcd:                                 O(log n) stack frames
```

---

## 7. The traps

**Forgetting that 1 is not prime, and that 2 is.**

```
without the n < 2 check:  is_prime(1)  -> True    WRONG
without the n < 4 check:  is_prime(2)  -> the loop
                                          never runs
                                       -> True, by luck
                          is_prime(3)  -> True, by luck
```

**The `1` case is a genuine wrong answer and it is in every test suite.** **The `2` and `3` cases happen to
come out right here because the loop starts at 5 and never runs** — but rely on luck and the version you write
next week will not have it. **Write the base cases first.**

**Starting the sieve at `2p` instead of `p*p`.**

**This is not wrong — it is just slower**, and an interviewer will ask about it specifically. **Every multiple
of `p` below `p × p` has a prime factor smaller than `p`, so it has already been crossed off.** Starting at
`p × p` skips that duplicated work.

**Sieving the wrong size.**

```python
sieve(1000)      # primes below 1000, so 997 is the last one
sieve(1001)      # if you want 1000 itself considered
```

**Off-by-one on whether the limit is included is the commonest bug in this function**, and it produces an
answer that is right except at one end. **Decide out loud which convention you are using and put it in the
docstring.**

**Building a sieve that does not fit.**

```python
prime = [True] * (10 ** 11)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**No message, no advice, just `MemoryError`.** **The time was never the problem — the memory was.** If the
limit is large, say "segmented sieve" and explain that you sieve a block at a time using the primes below the
square root.

**`lcm` written the obvious way.**

```
lcm = a * b // gcd(a, b)          overflows
lcm = a // gcd(a, b) * b          safe
```

**In Python both give the right answer**, because integers are arbitrary width. **In C++, Java, Go or Rust, `a
* b` overflows silently for `a, b` around `3 × 10^9`**, and you get a plausible wrong number. **Say "divide
first" as you write it, because that is a sentence the interviewer is listening for.**

**Negative results from `%` in other languages.**

```
Python:      (3 - 10) % 7   ->  3
C, Java, Go: (3 - 10) % 7   -> -7 % 7 -> 0 ... and
             (2 - 10) % 7   -> -8 % 7 -> -1

-> the fix in those languages: ((a - b) % m + m) % m
```

**Python's `%` always returns something with the modulus's sign, so it is non-negative for a positive
modulus.** **Most other languages take the sign of the dividend.** **A negative answer on a problem that asked
for a value in `[0, m)` is this, essentially every time.**

**Forgetting the modulus inside the fast-power loop.**

```python
base = base * base            # missing % modulus
```

**In Python this does not crash. It gets catastrophically slow.** `2^(2^30)` has about 323 million digits, and
each squaring doubles that. **The program does not fail — it stops finishing**, which is a much harder thing to
debug than an exception.

**Using Fermat's inverse when the modulus is not prime.**

```
inverse of 3 mod 10:
  the true answer is 7, because 3 x 7 = 21 = 1 mod 10
  Fermat gives 3^8 mod 10 = 1
  check: 3 x 1 mod 10 = 3, not 1        WRONG

inverse of 5 mod 12:
  Fermat gives 5^10 mod 12 = 1
  check: 5 x 1 mod 12 = 5, not 1        WRONG
```

**No error. A small, plausible number that is simply not the inverse.** **Fermat needs a prime modulus**, and
`10^9 + 7` is prime, which is exactly why problems use it. **If the modulus is composite, use extended Euclid
— and if `a` shares a factor with the modulus, there is no inverse at all.**

**Dividing by zero, under any modulus.**

```python
5 % 0
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: integer modulo by zero
```

**Loud, immediate, and the good kind of failure.**

**Using a float step or a float bound.**

```python
list(range(2, 10, 0.5))
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'float' object cannot be interpreted as an integer
```

**This is what happens when a square root gets into a loop bound.** **Use `factor * factor <= n`, or
`math.isqrt(n)`, and keep floats out of number theory entirely.**

---

## 8. In the interview

### How it gets asked

- *"Find all the primes below one million."* — the sieve, and they will ask why you start at `p × p`.
- *"Is this number prime?"* — trial division to the square root, and the reason for the square root.
- *"Find the GCD of two numbers."* — Euclid, and why each step preserves the answer.
- *"Compute a^b mod m for very large b."* — square and multiply.
- *"The answer may be large, so return it modulo 10^9 + 7."* — everything in section 3.
- *"How would you compute nCr modulo a prime?"* — inverses, and tomorrow's lesson.

### The first ninety seconds

On "find all the primes below one million":

> "**I would sieve, and the reason is a change of viewpoint: instead of asking a million questions, I cross
> off.**
>
> **Concretely, the Sieve of Eratosthenes.** Start with every number from 2 to a million marked as possibly
> prime. **Take 2 — cross off every multiple of 2. Take 3, the next survivor — cross off every multiple of 3.**
> Keep going. **Whatever survives is prime.**
>
> **Two details make it fast, and I would mention both because they are what gets asked.**
>
> **I start crossing off at `p × p`, not at `2p`.** Every multiple of `p` below `p × p` has a prime factor
> smaller than `p`, **so it has already been crossed off by that smaller prime.** For 5, the numbers 10, 15 and
> 20 were killed by 2 and 3 already.
>
> **And I stop when `p × p` exceeds the limit.** **Any composite number below the limit has a factor at or
> below its square root**, so once I have sieved past the square root, everything composite is gone.
>
> **The cost is the interesting part.** For each prime I cross off `n/p` numbers, **so the total is `n` times
> the sum of the reciprocals of the primes** — and that sum grows like `ln ln n`, which is tiny. **So it is
> `O(n log log n)`, which for practical purposes is a small constant times `n`.** About 2.8 million operations
> for a million, well under a second.
>
> **Testing each number individually would be about a thousand divisions each, so 333 million operations —
> roughly a hundred times slower.**
>
> **The thing that actually limits it is memory, not time.** A Python list of a hundred million booleans is
> about 800 megabytes. **A `bytearray` is one byte each, and a bitset is one bit.** **And if you asked for
> primes below a billion, I would use a segmented sieve** — sieve in blocks that fit in cache, using the primes
> below 31,623.
>
> **There are 78,498 primes below a million**, if you want the answer as a check."

### The follow-ups

**"Compute the GCD, and tell me why your method works."**

> "**Euclid's algorithm: `gcd(a, b) = gcd(b, a mod b)`, until the second one is zero.**
>
> **The reason is one sentence and I would want to say it properly.** **If some number divides both `a` and
> `b`, then it also divides what is left over after you take `b` out of `a` as many times as possible** —
> because you removed a pile of things it already divided. **So the set of common divisors is exactly the same
> before and after the step**, and each step makes the numbers strictly smaller. **It has to end, and it ends
> at the answer.**
>
> **There is a picture that makes it obvious.** Lay out a rectangle 1071 by 462 and cut off the biggest squares
> you can. You get two 462-squares and a strip 147 wide. **Do the same to the strip: three 147-squares and a
> 21-strip. Then seven 21-squares and nothing left.** **21 is the largest square that tiles the original
> exactly — that is the GCD.**
>
> **The cost is `O(log min(a, b))`** — at most about five times the number of decimal digits. **The worst case
> is consecutive Fibonacci numbers**, because each step then removes as little as possible. **For numbers
> around `10^18` that is under about ninety steps**, against `10^18` candidates for the naive search.
>
> **And the LCM comes free, because `a × b = gcd × lcm`.** **So `lcm = a / gcd × b` — and I divide first.** In
> Python it makes no difference, **but in C++ or Java `a * b` overflows a 64-bit integer for values around
> three billion**, and dividing first never produces anything larger than the answer.
>
> **One edge case: `gcd(a, 0)` is `a`, and that is correct rather than a special case** — every number divides
> zero."

**"Compute `a^b mod m` where `b` can be a billion."**

> "**Square and multiply, using the binary expansion of the exponent.**
>
> **The idea: `13` is `1101` in binary, which is `8 + 4 + 1`, so `3^13 = 3^8 × 3^4 × 3^1`.** **And I get
> `3^1, 3^2, 3^4, 3^8` by repeatedly squaring** — four squarings rather than thirteen multiplications.
>
> **The loop is: if the low bit of the exponent is set, multiply the current base into the result; then square
> the base and shift the exponent right.** **One iteration per bit.**
>
> **For an exponent of a billion that is thirty iterations rather than a billion multiplications** — about
> thirty-three million times less work.
>
> **The line that must not be forgotten is the `% m` after every multiplication.** **Without it the numbers
> grow without limit** — `2^(2^30)` has hundreds of millions of digits — **and in Python that does not
> overflow, it just stops finishing.** **A program that gets slower and slower is harder to debug than one that
> crashes**, so that modulus is doing more work than it looks.
>
> **Python has `pow(base, exp, mod)` built in and it does exactly this**, and in production I would use it.
> **I would still write the loop, because the question is testing whether I know why it is thirty steps.**"

**"The answer may be large — return it modulo 10^9 + 7. What does that change?"**

> "**Three things pass through a modulus and one does not.** **Addition, subtraction and multiplication are all
> safe**: I can take the modulus at every step and the answer is the same. **Division is not.**
>
> **So wherever the formula divides, I multiply by a modular inverse instead.** **The inverse of `a` is the `x`
> with `a × x ≡ 1`, which is what `1/a` means when you are wrapping round.**
>
> **When the modulus is prime — and `10^9 + 7` is prime — Fermat's little theorem gives it in one line:
> `a^(m−2) mod m`**, which is one fast power, about thirty multiplications. **The precondition matters and I
> would say it out loud: prime modulus, and `a` not a multiple of it.**
>
> **If the modulus is composite, Fermat quietly gives the wrong answer** — the 'inverse' of 3 mod 10 comes out
> as 1, and 3 × 1 is 3, not 1. **No error, just a wrong number.** **The general answer is the extended
> Euclidean algorithm**, which finds `x` and `y` with `ax + my = gcd(a, m)`; when that gcd is 1, `x` is the
> inverse. **And if `a` shares a factor with the modulus, there is no inverse at all.**
>
> **Why this particular number, since I am usually asked: three reasons.** **It is prime, which makes Fermat
> work.** **It is just over a billion, so it fits in a signed 32-bit integer.** **And two values below it
> multiply to just under `10^18`, which still fits in a signed 64-bit integer** — so `a * b % m` is safe in
> C++ or Java with no special handling. **That third reason is why it is exactly `10^9 + 7` and not some other
> prime.**
>
> **One language trap worth naming: in C, Java and Go, `%` takes the sign of the dividend**, so a subtraction
> can produce a negative result on a problem that wanted something in `[0, m)`. **The fix is
> `((a - b) % m + m) % m`.** **Python is the exception — its `%` is always non-negative for a positive
> modulus.**"

### The model answer

*"What number theory do you actually need for interviews, and why?"*

> "**Four things, and each one replaces an obvious loop with something logarithmic or near-linear.**
>
> **Primality, and the square-root bound.** To test one number I divide only up to its square root, **because
> if `n = a × b` then they cannot both exceed the square root.** For a million that is a thousand divisions
> instead of a million. **Skipping even numbers and multiples of three cuts it by another third — every prime
> above 3 is one either side of a multiple of six.**
>
> **The sieve, when I need many primes rather than one.** **Do not test each number; cross off the multiples.**
> Start at `p × p` because everything smaller has already been struck out by a smaller prime, and stop at the
> square root of the limit. **`O(n log log n)`, about a hundred times faster than testing each number, and
> memory rather than time is what limits it** — a bitset or a segmented sieve if the range is huge.
>
> **Euclid, for the GCD.** `gcd(a, b) = gcd(b, a mod b)`, **because a common divisor of the two also divides
> the remainder, so the set of common divisors never changes.** Logarithmic — worst case consecutive
> Fibonacci numbers. **LCM from `a × b = gcd × lcm`, dividing first to avoid overflow.**
>
> **Modular arithmetic, because half of all counting problems end with 'modulo 10^9 + 7'.** **Addition,
> subtraction and multiplication pass through the modulus; division does not.** **So division becomes
> multiplication by an inverse, and the inverse comes from Fermat when the modulus is prime — one fast power —
> or extended Euclid when it is not.**
>
> **And the fast power itself, which is the piece all of that rests on.** **Square and multiply, one step per
> bit of the exponent** — thirty steps for an exponent of a billion. **It is really yesterday's bit walk: read
> the exponent's binary digits and decide whether to multiply this power in.**
>
> **What I would want you to take from that is that they are not five separate facts.** **They are the same
> move each time: stop doing the thing once per unit, and find the structure that lets you do it once per
> group, or once per digit.** **Ask about the reasons instead of about each person, and sixty questions become
> five.**
>
> **The two things I would be most careful about in a real answer are the preconditions.** **Fermat needs a
> prime modulus and silently lies otherwise.** **And `%` is negative for negative inputs in most languages,
> which quietly breaks answers that were supposed to be non-negative.** **Both are wrong answers rather than
> crashes, and that is what makes them worth saying out loud.**"

---

## 9. Recall card

**Primality: test only to the SQUARE ROOT** — if `n = a×b`, they cannot both exceed `√n`, so 1,000 divisions
instead of a million. **Then step by 6 and test `6k ± 1`, a third again.** **1 is not prime; 2 is, and is the
only even prime — write the base cases first.** Beyond ~10^14, name **Miller–Rabin**.

**The SIEVE is the change of viewpoint: cross off multiples instead of testing numbers.** **Start at `p × p`**
(everything smaller already has a smaller prime factor) and **stop when `p × p > limit`**. **O(n log log n)** —
~2.8M operations for a million, about **100× faster** than testing each — and **memory limits it before time
does** (8 MB / 80 MB / 800 MB in Python; use a bytearray, a bitset, or a **segmented sieve** for 10^9).
**78,498 primes below a million.** A **smallest-prime-factor** sieve then factorises anything in **≤ log₂n**
steps.

**Euclid: `gcd(a, b) = gcd(b, a mod b)`, because a common divisor of both also divides the remainder — so the
set of common divisors never changes.** The picture is cutting the largest squares off a rectangle. **O(log
min(a,b))**, worst case consecutive Fibonacci numbers; `gcd(a, 0) = a`. **`lcm = a // gcd * b` — DIVIDE FIRST,
or `a*b` overflows 64 bits around 3×10⁹.**

**Under a modulus: +, − and × pass through; ÷ does NOT.** **Division becomes multiplication by an inverse.**
**Fermat, when the modulus is prime: `a^(m−2) mod m`** — one fast power. **On a composite modulus it silently
returns a wrong number** (the "inverse" of 3 mod 10 comes out as 1); use **extended Euclid** there, and note
there is no inverse at all when `a` shares a factor with `m`. **In C/Java/Go `%` takes the dividend's sign, so
write `((a-b) % m + m) % m`; Python's `%` is already non-negative.**

**Fast power: square and multiply, one step per BIT of the exponent** — 30 steps for 10⁹, 60 for 10¹⁸.
**Forgetting `% m` inside the loop does not crash, it just stops finishing.** **`10^9 + 7` is used because it
is prime (Fermat works), fits in a signed 32-bit integer, and two values under it multiply to under 10¹⁸ so
`a*b % m` is safe in 64 bits.**
