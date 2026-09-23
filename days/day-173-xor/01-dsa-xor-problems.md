---
day: 173
track: dsa
title: "XOR problems"
phase: "Bits and maths"
status: written
---

# XOR problems

## 1. What this is, and why they ask it

**XOR has one property that matters, and it solves a whole family of interview questions: `a ^ a` is zero.**
A thing XORed with itself disappears.

**So if you XOR a whole list together, everything that appears twice cancels itself out, and what is left is
whatever had no partner.** No extra memory. One pass. No sorting.

**And because XOR does not care about order** — `(5 ^ 3) ^ 9` and `9 ^ (3 ^ 5)` are both 15 — **you never have
to know which pair cancelled which.** That is the part that makes it feel like a trick, and it is the part
worth being able to explain.

They ask it because **the constraint gives it away and candidates still miss it.** "Find the number that
appears once, in linear time and constant extra space." **Linear time and constant space rules out sorting and
rules out a frequency map**, and once those are gone, XOR is essentially the only tool left. **An interviewer
saying "O(1) space" out loud is saying the word XOR without saying it.**

**And because the family goes deeper than the famous one.** One loner is easy. **Two loners is the question
that separates people**, and it needs a second idea: split the list into two piles on a bit where the two
answers differ, then run the easy version on each pile.

By the end of this lesson you can solve the whole family — one loner, one missing, two loners, everything
three times, one doubled and one missing — plus the XOR of any range in constant time, prefix XOR for subarray
questions, and the biggest XOR pair in a list.

---

## 2. The story

There were sixty-one children going to Mysore and Rajeshwari had done this trip eleven times.

The other teachers wrote lists. She had tried lists in her second year and given them up, **because a list of
who is sitting with whom goes out of date about four minutes after you write it.** Children swap. They swap at
the tea stop, they swap when somebody feels sick, and they swap for no reason anybody can explain.

So she had one rule instead, and she said it at the gate before anybody got on the bus.

**"Find one person. Hold their hand. That is your partner for the whole day."**

At every stop — the tea stall past Channapatna, the zoo gate, the place with the fountain — she did the same
thing, and it took under a minute.

**"Everybody. Find your partner. Hands up."**

And then she did not count. **Counting sixty-one moving children is hopeless, and she had learnt that the hard
way in her first year.**

**She looked for the one child standing with nobody.**

Sixty-one is an odd number, so there was always exactly one. That year it was a boy called Vishnu, who did not
mind at all, and who had worked out by the second stop that his entire job for the day was to stand still and
be easy to see.

**If Vishnu was there, everybody was there.** If Vishnu was not there, or if there was a second child standing
loose beside him, something had happened.

At the fountain, that afternoon, there were two children standing alone.

The other teacher started shouting names off her list, one after another, and got to about eleven before she
lost her place.

Rajeshwari did something else.

**"Blue shirts, this side. Everybody not in blue, that side."**

Two smaller crowds. And in each one, she said the same sentence she had said all day.

**"Find your partner. Hands up."**

One child left over on the blue side. One child left over on the other.

**Two names, in about ninety seconds, and she had still not written a single thing down.**

---

## 3. The idea in plain English

**Holding hands is XOR.** Two children who pair up become invisible to Rajeshwari — **they cancel.** The one
left standing is the answer. **And she never had to know who paired with whom**, which is exactly why she
needed no list.

### The three facts

**Everything in this lesson comes from three lines.**

```
   a ^ a = 0          a thing XORed with itself vanishes
   a ^ 0 = a          zero changes nothing
   order does not matter, and grouping does not matter

     (5 ^ 3) ^ 9  =  15
     5 ^ (3 ^ 9)  =  15
     9 ^ (3 ^ 5)  =  15
```

**The first is the pairing. The second is the empty room — start from nothing.** **The third is the reason you
do not need a list**: you can XOR the numbers in any order at all and get the same answer, so the pairs find
each other without your help.

**Say the third one out loud in an interview**, because it is the fact that turns the trick into an argument.

### One loner

```
   [4, 1, 2, 1, 2]

   0 ^ 4 = 4
   4 ^ 1 = 5
   5 ^ 2 = 7
   7 ^ 1 = 6
   6 ^ 2 = 4

   -> 4
```

**Look at the middle numbers: 5, 7, 6.** They are meaningless. **The partial answers are not partial answers**
— nothing is true until the end, when every pair has cancelled. **That is uncomfortable and it is worth saying
so**, because it is why people do not trust this the first time they see it.

**Rearrange the same list and you can see why it must work:**

```
   [4, 1, 2, 1, 2]   ->   4 ^ (1 ^ 1) ^ (2 ^ 2)
                     ->   4 ^    0    ^    0
                     ->   4
```

**You are allowed to rearrange it because order does not matter.** That is the whole proof, and it is one
line.

### One missing from 0 to n

**Same idea, but now you have to supply the partners yourself.**

```
   given [3, 0, 1], the full set is 0, 1, 2, 3

   XOR the numbers you HAVE     3 ^ 0 ^ 1
   XOR the numbers you EXPECT   0 ^ 1 ^ 2 ^ 3
   -------------------------------------------
   everything present appears TWICE and cancels
   what is absent appears ONCE

   -> 2
```

**Every value that is present gets XORed twice — once from the list, once from the range — so it pairs with
itself and disappears.** The missing value only appears on the "expected" side, so it survives.

**This is worth preferring to the sum formula.** `n(n+1)/2 - sum(numbers)` also works, **and it overflows in
languages with fixed-width integers.** XOR cannot overflow, because it never carries. **Say that.**

### Two loners, which is the real question

**Rajeshwari's blue shirts.** XORing everything gives you `a ^ b` — the two answers mixed together — **and you
cannot pull them apart directly.**

**But you can split the list.**

```
   [1, 2, 1, 3, 2, 5]

   XOR everything      -> 6 = 0110      this is 3 ^ 5
   lowest set bit      -> 2 = 0010
```

**A set bit in `a ^ b` means the two answers DISAGREE in that place.** So pick any one of them — the lowest is
easiest, `both & -both` — and use it as the shirt colour.

```
   has the 2s bit set:  [2, 3, 2]     -> XOR -> 3
   does not:            [1, 1, 5]     -> XOR -> 5
```

**Every duplicate pair lands in the same pile**, because two equal numbers agree in every place. **And the two
loners land in different piles**, because they were chosen to disagree exactly there. **So each pile is now the
easy problem.**

**That is the whole of LeetCode 260**, and it is the moment the XOR family stops being a party trick.

### Everything three times except one

**Pairing does not help — three of a thing is not zero.** So you count instead, **place by place.**

```
   [2, 2, 3, 2]        in binary: 10, 10, 11, 10

   place 0 (the 1s):   0 + 0 + 1 + 0 = 1   ->  1 % 3 = 1  -> set it
   place 1 (the 2s):   1 + 1 + 1 + 1 = 4   ->  4 % 3 = 1  -> set it

   -> 11 = 3
```

**Every number that appears three times contributes three to some columns and zero to others**, so **every
column is a multiple of three, plus whatever the loner contributed.** Take the remainder modulo three and you
have the loner's bits back.

**This generalises: appearing `k` times means counting modulo `k`.** Say that — it shows you understand the
mechanism rather than the special case.

### The XOR of a whole range, in constant time

```
   0^1       = 1
   0^1^2     = 3
   0^1^2^3   = 0
   0^1^2^3^4 = 4
   ... ^5    = 1
   ... ^6    = 7
   ... ^7    = 0

   THE PATTERN REPEATS EVERY FOUR:

     n % 4 == 0  ->  n
     n % 4 == 1  ->  1
     n % 4 == 2  ->  n + 1
     n % 4 == 3  ->  0
```

**And any range is two of those**: `low ^ ... ^ high` is `xor_to(high) ^ xor_to(low - 1)`, **because everything
below `low` appears in both and cancels.** That is the same subtraction trick as prefix sums, wearing XOR
instead of addition.

### Prefix XOR

**XOR has the property prefix sums need: it can be undone.** `x ^ y ^ y` is `x`. So:

```
   prefix[0] = 0
   prefix[i] = a[0] ^ a[1] ^ ... ^ a[i-1]

   XOR of a[l..r] = prefix[r+1] ^ prefix[l]
```

**And the useful consequence: `prefix[i] == prefix[k]` means the whole stretch between them XORs to zero**,
which is how a family of "count the subarrays where..." problems collapses to counting equal prefix values.

### The biggest XOR pair

**Build the answer one bit at a time, starting from the top, and at each step ask whether the next bit can be a
one.**

```
   want the highest bit set? Take every number's top-k bits.
   If any two of those prefixes XOR to the target, yes.
   Then move down one place and try again.
```

**Thirty-two rounds, each a set lookup.** That is LeetCode 421, and the same answer can be written with a trie
— **and if you say "the trie version stores the numbers bit by bit and walks the opposite branch at every
step", you have said the thing they wanted to hear.**

---

## 4. The picture

Pairs cancelling, column by column:

```
   [4, 1, 2, 1, 2]

        4   1   2   1   2
      100 001 010 001 010
      --- --- --- --- ---

   place 0 (the 1s):   0 + 1 + 0 + 1 + 0
                       two 1s -> cancel     -> 0
   place 1 (the 2s):   0 + 0 + 1 + 0 + 1
                       two 1s -> cancel     -> 0
   place 2 (the 4s):   1 + 0 + 0 + 0 + 0
                       one 1  -> survives   -> 1

   answer 100 = 4

   XOR is just "is the count of 1s in this column odd?"
   asked independently in every column. Nothing carries,
   nothing is remembered between columns.
```

The split, drawn — Rajeshwari's blue shirts:

```
   [1, 2, 1, 3, 2, 5]        the loners are 3 and 5

   XOR of everything = 6 = 0110
                            ^
                            |
   pick ANY set bit. The lowest is easiest: both & -both = 0010

   Now sort the list by "does it have the 2s bit set?"

     2s bit SET          2s bit CLEAR
     ----------          ------------
       2 = 0010            1 = 0001
       3 = 0011            1 = 0001
       2 = 0010            5 = 0101

     XOR -> 3            XOR -> 5


   WHY EVERY PAIR STAYS TOGETHER:
     two equal numbers agree in EVERY place, so they
     always land in the same pile and cancel there.

   WHY THE LONERS SPLIT:
     the bit was chosen because they DISAGREE there.
     That is what a 1 in a ^ b means.
```

Counting modulo three:

```
   [2, 2, 3, 2]

           place 1   place 0
   2  =       1         0
   2  =       1         0
   3  =       1         1
   2  =       1         0
          --------  --------
   column     4         1
   mod 3      1         1

   answer =   1         1     = 11 = 3

   The three 2s put a 1 in place 1 three times, and 3 mod 3
   is 0 - they vanish. Everything left is the loner.

   Appearing k times -> count mod k. Twice is just k = 2,
   and mod 2 is exactly what XOR already does.
```

The range pattern:

```
   n     0  1  2  3  4  5  6  7  8  9 10 11
   xor   0  1  3  0  4  1  7  0  8  1 11  0
         ^        ^  ^        ^  ^        ^
         |        |  |        |  |        |
       n%4=0    n%4=3         every four, back to 0

   n%4 == 0 -> n        n%4 == 2 -> n+1
   n%4 == 1 -> 1        n%4 == 3 -> 0

   Four cases, no loop, and it is the kind of thing an
   interviewer asks as a follow-up to see whether you look
   for structure or reach for a loop.
```

---

## 5. The code, built step by step

### One loner

```python
def single_number(numbers: list[int]) -> int:
    """Everything appears twice except one. Pairs cancel; the loner survives."""
    answer = 0
    for value in numbers:
        answer ^= value
    return answer
```

**Three lines, and the only decision in them is starting at `0`.** That is `a ^ 0 = a` — **an empty pile XORs
to zero**, exactly as an empty pile sums to zero.

**In an interview, write it and then immediately say the rearrangement argument**: "order does not matter, so
I can group the duplicates together, and each group is `x ^ x`, which is zero."

### One missing

```python
def missing_number(numbers: list[int]) -> int:
    """0..n with one missing. XOR the full range against what you have."""
    answer = len(numbers)
    for i, value in enumerate(numbers):
        answer ^= i ^ value
    return answer
```

**Starting at `len(numbers)` is the whole subtlety.** The loop covers positions `0` to `n-1` and the values,
**but the range goes up to `n`** — so the top of the range has to be put in by hand. **Forget it and you get a
plausible wrong answer with no error.**

### Two loners

```python
def single_number_three(numbers: list[int]) -> tuple[int, int]:
    """Two loners. XOR everything, then split the list on one bit where they differ."""
    both = 0
    for value in numbers:
        both ^= value
    split = both & -both
    first = 0
    for value in numbers:
        if value & split:
            first ^= value
    return first, both ^ first
```

**`split = both & -both` is yesterday's isolate-the-lowest-set-bit**, and it is doing real work here: **it
picks one place where the two answers disagree.**

**And the last line is the nicest part.** Having found one answer, **you do not need a third pass** — `both` is
`a ^ b`, so `both ^ first` is `b`. **XOR undoes itself.**

### Everything three times

```python
def single_number_twice_over(numbers: list[int]) -> int:
    """Everything appears three times except one. Count each place modulo three."""
    answer = 0
    for position in range(32):
        column = sum((value >> position) & 1 for value in numbers)
        if column % 3:
            answer |= 1 << position
    return answer - (1 << 32) if answer >> 31 else answer
```

**Thirty-two columns, each counted independently, each taken modulo three.** Slower than the clever
two-variable state machine, **and far easier to explain under pressure** — which is the trade you want in an
interview.

**The last line is the Python tax.** Python integers have no top bit, so **a negative answer comes out as a
huge positive number** and you have to convert it back by hand. **Say "the input can be negative, so I have to
reinterpret the top bit as a sign" out loud** — otherwise that line looks like superstition.

### The range formula

```python
def xor_to(n: int) -> int:
    """0 ^ 1 ^ ... ^ n in O(1). The answer repeats with period four."""
    return (n, 1, n + 1, 0)[n % 4]


def xor_range(low: int, high: int) -> int:
    """low ^ ... ^ high. Everything below `low` cancels itself out."""
    return xor_to(high) ^ xor_to(low - 1)
```

**Derive the four cases at the desk rather than memorising them** — write out the XOR of 0 to 7 and the pattern
is obvious in about twenty seconds. **`xor_range` is the prefix-sum subtraction with XOR in place of minus**,
and it works for the same reason: **XOR is its own inverse.**

### The biggest XOR pair

```python
def maximum_xor_pair(numbers: list[int], width: int = 32) -> int:
    """Build the answer one bit at a time, highest first, and ask if it is reachable."""
    best = 0
    for position in range(width - 1, -1, -1):
        best <<= 1
        wanted = best | 1
        prefixes = {value >> position for value in numbers}
        if any(wanted ^ prefix in prefixes for prefix in prefixes):
            best = wanted
    return best
```

**Greedy from the top, and greedy is safe here for the reason greedy is ever safe: a higher bit outweighs every
lower bit combined.** `1000` is bigger than `0111`. **So if the top bit can be a one, take it, and never
reconsider.**

**`wanted ^ prefix in prefixes` is the trick inside the trick.** You are asking "is there a partner that would
give me this target?" — **and `x ^ y == target` means `y == target ^ x`**, so the question is a set lookup
rather than a second loop.

### The complete solution

```python
"""Day 173 - the XOR family. Pairs cancel, and that one fact solves all of it."""

from __future__ import annotations


def single_number(numbers: list[int]) -> int:
    """Everything appears twice except one. Pairs cancel; the loner survives."""
    answer = 0
    for value in numbers:
        answer ^= value
    return answer


def missing_number(numbers: list[int]) -> int:
    """0..n with one missing. XOR the full range against what you have."""
    answer = len(numbers)
    for i, value in enumerate(numbers):
        answer ^= i ^ value
    return answer


def single_number_three(numbers: list[int]) -> tuple[int, int]:
    """Two loners. XOR everything, then split the list on one bit where they differ."""
    both = 0
    for value in numbers:
        both ^= value
    split = both & -both
    first = 0
    for value in numbers:
        if value & split:
            first ^= value
    return first, both ^ first


def single_number_twice_over(numbers: list[int]) -> int:
    """Everything appears three times except one. Count each place modulo three."""
    answer = 0
    for position in range(32):
        column = sum((value >> position) & 1 for value in numbers)
        if column % 3:
            answer |= 1 << position
    return answer - (1 << 32) if answer >> 31 else answer


def find_duplicate_and_missing(numbers: list[int]) -> tuple[int, int]:
    """1..n with one number doubled and one absent. Same split trick as two loners."""
    both = 0
    for i, value in enumerate(numbers, start=1):
        both ^= i ^ value
    split = both & -both
    first = 0
    for value in numbers:
        if value & split:
            first ^= value
    for i in range(1, len(numbers) + 1):
        if i & split:
            first ^= i
    duplicate = first if numbers.count(first) == 2 else both ^ first
    return duplicate, both ^ duplicate


def xor_to(n: int) -> int:
    """0 ^ 1 ^ ... ^ n in O(1). The answer repeats with period four."""
    return (n, 1, n + 1, 0)[n % 4]


def xor_range(low: int, high: int) -> int:
    """low ^ ... ^ high. Everything below `low` cancels itself out."""
    return xor_to(high) ^ xor_to(low - 1)


def count_equal_split_triplets(numbers: list[int]) -> int:
    """Count i < j <= k with a[i..j-1] == a[j..k]. That means prefix[i] == prefix[k+1]."""
    prefix = [0]
    for value in numbers:
        prefix.append(prefix[-1] ^ value)
    total = 0
    for i in range(len(prefix)):
        for k in range(i + 1, len(prefix)):
            if prefix[i] == prefix[k]:
                total += k - i - 1
    return total


def maximum_xor_pair(numbers: list[int], width: int = 32) -> int:
    """Build the answer one bit at a time, highest first, and ask if it is reachable."""
    best = 0
    for position in range(width - 1, -1, -1):
        best <<= 1
        wanted = best | 1
        prefixes = {value >> position for value in numbers}
        if any(wanted ^ prefix in prefixes for prefix in prefixes):
            best = wanted
    return best


def gray_code(bits: int) -> list[int]:
    """Every number 0..2^bits-1, each differing from the last in exactly one place."""
    return [i ^ (i >> 1) for i in range(1 << bits)]


if __name__ == "__main__":
    print("THE THREE FACTS")
    print(f"  7 ^ 7      = {7 ^ 7}      a ^ a = 0")
    print(f"  7 ^ 0      = {7 ^ 0}      a ^ 0 = a")
    print(f"  (5^3)^9    = {(5 ^ 3) ^ 9}     order does not matter")
    print(f"  5^(3^9)    = {5 ^ (3 ^ 9)}")
    print(f"  9^(3^5)    = {9 ^ (3 ^ 5)}")

    print()
    print("ONE LONER")
    print(f"  single_number([4,1,2,1,2])        = {single_number([4, 1, 2, 1, 2])}")
    print(f"  single_number([2,2,1])            = {single_number([2, 2, 1])}")
    print(f"  single_number([7])                = {single_number([7])}")

    print()
    print("ONE MISSING FROM 0..n")
    print(f"  missing_number([3,0,1])           = {missing_number([3, 0, 1])}")
    print(f"  missing_number([0,1])             = {missing_number([0, 1])}")
    print(f"  missing_number([9,6,4,2,3,5,7,0,1]) = {missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1])}")

    print()
    print("TWO LONERS - the split bit does the work")
    values = [1, 2, 1, 3, 2, 5]
    both = 0
    for v in values:
        both ^= v
    print(f"  list                  {values}")
    print(f"  XOR of everything     {both} = {both:04b}   (this is 3 ^ 5)")
    print(f"  lowest set bit        {both & -both} = {both & -both:04b}   they differ HERE")
    print(f"  single_number_three   {single_number_three(values)}")

    print()
    print("EVERYTHING THREE TIMES EXCEPT ONE")
    print(f"  [2,2,3,2]             = {single_number_twice_over([2, 2, 3, 2])}")
    print(f"  [0,1,0,1,0,1,99]      = {single_number_twice_over([0, 1, 0, 1, 0, 1, 99])}")
    print(f"  [-2,-2,1,-2]          = {single_number_twice_over([-2, -2, 1, -2])}")

    print()
    print("ONE DOUBLED, ONE MISSING, IN 1..n")
    print(f"  [1,2,2,4]             = {find_duplicate_and_missing([1, 2, 2, 4])}   (dup, missing)")
    print(f"  [1,1]                 = {find_duplicate_and_missing([1, 1])}")

    print()
    print("XOR OF A RANGE, IN CONSTANT TIME")
    for n in range(0, 9):
        brute = 0
        for i in range(n + 1):
            brute ^= i
        print(f"  0..{n:>2}  formula={xor_to(n):>3}  brute={brute:>3}  n%4={n % 4}")
    print(f"  xor_range(3, 9) = {xor_range(3, 9)}")

    print()
    print("PREFIX XOR - counting equal splits")
    print(f"  [2,3,1,6,7]  -> {count_equal_split_triplets([2, 3, 1, 6, 7])}")
    print(f"  [1,1,1,1,1]  -> {count_equal_split_triplets([1, 1, 1, 1, 1])}")

    print()
    print("BIGGEST XOR IN THE LIST")
    print(f"  [3,10,5,25,2,8] -> {maximum_xor_pair([3, 10, 5, 25, 2, 8])}   (5 ^ 25)")
    print(f"  5 ^ 25 = {5 ^ 25}")

    print()
    print("GRAY CODE - one bit changes each step")
    for i, value in enumerate(gray_code(3)):
        print(f"  i={i}  i>>1={i >> 1}  i^(i>>1) = {value}  = {value:03b}")

    print()
    print("VERIFICATION")
    import random

    bad = 0
    for _ in range(2000):
        n = random.randint(1, 40)
        loner = random.randint(0, 10_000)
        pool = [random.randint(0, 10_000) for _ in range(n)]
        data = pool + pool + [loner]
        random.shuffle(data)
        if single_number(data) != loner:
            bad += 1

        size = random.randint(1, 60)
        gone = random.randint(0, size)
        if missing_number([v for v in range(size + 1) if v != gone]) != gone:
            bad += 1

        a, b = random.sample(range(0, 10_000), 2)
        pool = [random.randint(0, 10_000) for _ in range(n)]
        data = pool + pool + [a, b]
        random.shuffle(data)
        if sorted(single_number_three(data)) != sorted([a, b]):
            bad += 1

        triple = [random.randint(0, 10_000) for _ in range(n)]
        data = triple * 3 + [loner]
        random.shuffle(data)
        if single_number_twice_over(data) != loner:
            bad += 1

        top = random.randint(1, 500)
        brute = 0
        for v in range(top + 1):
            brute ^= v
        if xor_to(top) != brute:
            bad += 1

        sample = [random.randint(0, 255) for _ in range(random.randint(2, 12))]
        best = max(x ^ y for x in sample for y in sample)
        if maximum_xor_pair(sample, 8) != best:
            bad += 1
    codes = gray_code(6)
    if len(set(codes)) != 64 or any((codes[i] ^ codes[i + 1]).bit_count() != 1 for i in range(63)):
        bad += 1
    print(f"  {bad} mismatches over 2,000 random cases, 6 checks each, plus gray code")
```

Running it:

```
THE THREE FACTS
  7 ^ 7      = 0      a ^ a = 0
  7 ^ 0      = 7      a ^ 0 = a
  (5^3)^9    = 15     order does not matter
  5^(3^9)    = 15
  9^(3^5)    = 15

ONE LONER
  single_number([4,1,2,1,2])        = 4
  single_number([2,2,1])            = 1
  single_number([7])                = 7

ONE MISSING FROM 0..n
  missing_number([3,0,1])           = 2
  missing_number([0,1])             = 2
  missing_number([9,6,4,2,3,5,7,0,1]) = 8

TWO LONERS - the split bit does the work
  list                  [1, 2, 1, 3, 2, 5]
  XOR of everything     6 = 0110   (this is 3 ^ 5)
  lowest set bit        2 = 0010   they differ HERE
  single_number_three   (3, 5)

EVERYTHING THREE TIMES EXCEPT ONE
  [2,2,3,2]             = 3
  [0,1,0,1,0,1,99]      = 99
  [-2,-2,1,-2]          = 1

ONE DOUBLED, ONE MISSING, IN 1..n
  [1,2,2,4]             = (2, 3)   (dup, missing)
  [1,1]                 = (1, 2)

XOR OF A RANGE, IN CONSTANT TIME
  0.. 0  formula=  0  brute=  0  n%4=0
  0.. 1  formula=  1  brute=  1  n%4=1
  0.. 2  formula=  3  brute=  3  n%4=2
  0.. 3  formula=  0  brute=  0  n%4=3
  0.. 4  formula=  4  brute=  4  n%4=0
  0.. 5  formula=  1  brute=  1  n%4=1
  0.. 6  formula=  7  brute=  7  n%4=2
  0.. 7  formula=  0  brute=  0  n%4=3
  0.. 8  formula=  8  brute=  8  n%4=0
  xor_range(3, 9) = 2

PREFIX XOR - counting equal splits
  [2,3,1,6,7]  -> 4
  [1,1,1,1,1]  -> 10

BIGGEST XOR IN THE LIST
  [3,10,5,25,2,8] -> 28   (5 ^ 25)
  5 ^ 25 = 28

GRAY CODE - one bit changes each step
  i=0  i>>1=0  i^(i>>1) = 0  = 000
  i=1  i>>1=0  i^(i>>1) = 1  = 001
  i=2  i>>1=1  i^(i>>1) = 3  = 011
  i=3  i>>1=1  i^(i>>1) = 2  = 010
  i=4  i>>1=2  i^(i>>1) = 6  = 110
  i=5  i>>1=2  i^(i>>1) = 7  = 111
  i=6  i>>1=3  i^(i>>1) = 5  = 101
  i=7  i>>1=3  i^(i>>1) = 4  = 100

VERIFICATION
  0 mismatches over 2,000 random cases, 6 checks each, plus gray code
```

**Look at `single_number([7])`: the answer is 7.** A list of one is the base case and it comes out right for
free, **because you started at zero and `7 ^ 0` is 7.**

**Look at the two-loner trace.** The XOR of everything is `0110`, which is `3 ^ 5` — the two answers mixed
together and unusable on their own. **The isolated lowest bit, `0010`, is the only extra thing needed**, and it
turns one unsolvable problem into two easy ones.

**And look at the gray code column.** `i` counts 0, 1, 2, 3, 4 — but `i ^ (i >> 1)` gives 0, 1, 3, 2, 6, and
**every consecutive pair differs in exactly one place.** One XOR, and an ordering that would otherwise take
real work.

---

## 6. What it costs

**One loner.**

```
single_number: one XOR per element

  n = 5        ->  5 operations
  n = 1,000,000 -> 1,000,000 operations

-> O(n) time, O(1) extra space.

Compare with the two answers people reach for first:

  SORT then scan:      O(n log n) time, and it MUTATES the input
  FREQUENCY MAP:       O(n) time but O(n) space -
                       1,000,000 entries at ~50 bytes each = 50 MB

-> the constraint "O(1) space" is what rules out the map,
   and it is the interviewer telling you the answer.
```

**Two loners — three passes, still linear.**

```
pass 1: XOR everything            n operations
pass 2: XOR the matching pile     n operations
        (one comparison each)
-------------------------------------------------
                                  2n operations

-> O(n) time, O(1) space. The extra pass costs a constant
   factor of two and buys the entire problem.
```

**Everything three times — count the loops out loud.**

```
for position in range(32):            32 iterations
    sum over every value               n operations each
--------------------------------------------------------
                                       32 x n

  n = 1,000,000  ->  32,000,000 operations

-> O(32n), which is O(n), but the constant 32 is REAL.

The two-variable state-machine version is a single pass:
  n operations, so 32x fewer.

-> In an interview, write the column version and SAY the
   state machine exists. Correct and explainable beats
   clever and shaky.
```

**The range formula.**

```
xor_to(n): one modulo, one lookup

  n = 10             ->  1 operation
  n = 1,000,000,000  ->  1 operation

  the loop it replaces:
  n = 1,000,000,000  ->  1,000,000,000 operations

-> O(1) against O(n). This is the largest single saving
   in the lesson, and it comes from noticing a pattern
   rather than from a technique.
```

**Prefix XOR.**

```
build the table:     n operations, n+1 slots
answer one query:    1 XOR

  1,000 queries on a 100,000-element list:
    naive:   1,000 x 100,000 = 100,000,000
    prefix:  100,000 + 1,000  =    101,000

-> ~1,000x, for O(n) extra space.
```

**The biggest XOR pair.**

```
for each of 32 bit positions:
    build a set of n prefixes      n operations
    check each prefix against it   n lookups
------------------------------------------------
                                   32 x 2n

  n = 200,000  ->  ~12,800,000 operations   fine

against the brute force:
  every pair: n(n-1)/2
  n = 200,000  ->  20,000,000,000   no

-> O(32n) against O(n^2). The trie version has the same
   cost and a nicer explanation.
```

**Space, across the whole lesson.**

```
single_number, missing_number,
single_number_three, xor_to:          O(1)
single_number_twice_over:             O(1)
maximum_xor_pair:                     O(n) for the set
prefix XOR:                           O(n) for the table

-> Every headline problem in this family is O(1) space,
   and that is precisely why they are asked.
```

---

## 7. The traps

**Assuming "appears twice" when the problem said something else.**

```
single_number([2, 2, 3])        ->  3     correct - two copies cancel
single_number([2, 2, 2, 2, 3])  ->  3     correct - four copies cancel
single_number([4, 4, 4, 4, 7])  ->  7     correct

single_number([2, 2, 2, 3])     ->  1     WRONG, and it is a
                                          perfectly plausible number
single_number([1, 1, 1, 3])     ->  2     WRONG
single_number([5, 5, 5, 5, 5, 9]) -> 12   WRONG
```

**An even number of copies cancels; an odd number leaves one behind.** So the plain XOR answer **happens to be
right whenever every repeat count is even**, and quietly wrong otherwise. **The wrong answers are small,
ordinary-looking numbers** — 1, 2, 12 — **not obvious failures.** It passes the hand-made test with two copies
and fails the real input with three, **which is the worst shape a bug can have. Read the repeat count out of
the problem statement and say it out loud before you write a line.**

**Forgetting the top of the range in the missing-number version.**

```python
def missing_number_wrong(numbers: list[int]) -> int:
    answer = 0                     # should start at len(numbers)
    for i, value in enumerate(numbers):
        answer ^= i ^ value
    return answer
```

```
missing_number_wrong([3, 0, 1])              ->  1   correct answer is 2
missing_number_wrong([0, 1])                 ->  0   correct answer is 2
missing_number_wrong([9,6,4,2,3,5,7,0,1])    ->  1   correct answer is 8
```

**Positions run 0 to n-1 and values run 0 to n**, so the value `n` has no position to pair with. **Seeding the
accumulator with `len(numbers)` supplies it.** Nothing errors; you just get a number from the right range that
is not the answer.

**The split bit when there is nothing to split.**

```python
single_number_three([1, 1, 2, 2])
```

```
both  = 0
split = 0 & -0 = 0
first = 0            (nothing has bit 0 set)
returns (0, 0)
```

**No error, and two answers that were never in the list.** **The precondition — exactly two loners — is doing
real work**, and if the input might not satisfy it you have to check `both != 0` yourself.

**The negative-number tax in the modulo-three version.**

```
without the final sign correction:

  single_number_twice_over([-2, -2, 1, -2])  ->  1          fine
  single_number_twice_over([2, 2, -3, 2])    ->  4294967293
                                                 expected -3
```

**Python integers are arbitrary width, so setting bit 31 does not make a number negative** — it makes it a
large positive one. **The correction is `answer - (1 << 32)` when bit 31 is set**, and it exists purely because
of Python. **In Java or C++ this line does not appear at all, and saying that is worth a mark.**

**Trying to recover both numbers from `a ^ b`.**

```
a ^ b = 6

  a = 3, b = 5   ->  6
  a = 1, b = 7   ->  6
  a = 0, b = 6   ->  6
  a = 2, b = 4   ->  6
```

**The XOR of two numbers does not determine them.** People try to "unmix" it and there is nothing to unmix.
**You need the split, and the split needs the original list** — that is why the two-loner solution has a second
pass and cannot avoid one.

**XOR is not addition, and the swap trick proves it.**

```
5 + 3 = 8      5 ^ 3 = 6
```

**XOR is "addition without carrying".** In a single column it is the same; across columns it is not. **This
matters when somebody offers you the sum-based missing-number formula: it is correct, and it overflows.** XOR
never overflows because it never carries — **say that as the reason you prefer it.**

**Mixing types, which is how this fails at the keyboard.**

```python
answer = 0
answer ^= "3"
```

```
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: unsupported operand type(s) for ^=: 'int' and 'str'
```

**Reading numbers from input and forgetting to convert them is the single most common way this loop fails.**

```python
3 ^ 2.0
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for ^: 'int' and 'float'
```

**Anything that has been through a `/` division is a float.** Use `//`.

**The range formula on a negative input.**

```
xor_to(-1)   ->  0      no error at all
```

**Python's `%` is always non-negative, so `-1 % 4` is `3` and you get the `n % 4 == 3` case.** **A silently
plausible answer to a question that had no meaning.** The formula is defined for `n >= 0`; guard it, or say so.

---

## 8. In the interview

### How it gets asked

- *"Every number appears twice except one. Find it, in linear time and constant space."* — LeetCode 136.
- *"An array of 0 to n with one missing. Find it, without extra space."* — LeetCode 268.
- *"Now two numbers appear once and the rest twice."* — LeetCode 260, and this is the real question.
- *"Every number appears three times except one."* — LeetCode 137.
- *"Find the maximum XOR of any two numbers in the array."* — LeetCode 421.
- *"What is 1 XOR 2 XOR ... XOR n?"* — the constant-time follow-up.

### The first ninety seconds

On "every number appears twice except one, O(1) space":

> "**The constraint tells me the answer.** Constant extra space rules out a frequency map, and linear time
> rules out sorting. **That leaves XOR, and XOR is exactly right here.**
>
> **The property I need is that `a ^ a` is zero.** A number XORed with itself vanishes. **And `a ^ 0` is `a`,
> so starting from zero costs nothing.**
>
> **So I XOR the whole list together and return the result.**
>
> **The reason that works — and this is the part I want to say properly — is that XOR does not care about
> order or grouping.** So I am allowed to imagine the list rearranged with every duplicate pair side by side.
> **Then it reads as `loner ^ (x ^ x) ^ (y ^ y) ^ ...`, every bracket is zero, and the loner is all that is
> left.**
>
> **I would point out one thing that makes people distrust this.** The intermediate values are meaningless —
> on `[4,1,2,1,2]` you pass through 4, 5, 7, 6 and land on 4. **Nothing is true until the last element**,
> because the pairs have not all cancelled yet.
>
> **One pass, one integer, so O(n) time and O(1) space.**
>
> **A useful way to see why it works at all: XOR is asking, independently in each bit position, 'is the number
> of ones in this column odd?'** Duplicates contribute an even number to every column. **Only the loner makes a
> column odd.**"

### The follow-ups

**"Now two numbers appear once and everything else twice."**

> "**XORing everything still works, but it gives me `a ^ b` — the two answers mixed together — and there is
> nothing I can do with that directly.** `a ^ b == 6` could be 3 and 5, or 1 and 7, or 2 and 4. **The XOR does
> not determine the pair.**
>
> **So I split the list into two piles and run the easy version on each.**
>
> **The insight is what a set bit in `a ^ b` means: it means the two answers DISAGREE in that place.** So I
> pick any set bit — **the lowest, with `both & -both`, which isolates it in one operation** — and I use it to
> decide which pile each number goes into.
>
> **Two things make this work, and I would state both.** **Every duplicate pair lands in the same pile**,
> because two equal numbers agree in every place, so they cancel wherever they land. **And the two loners land
> in different piles**, because I chose a place where they differ. **So each pile is exactly the original
> problem: one loner, everything else in pairs.**
>
> **Then a small nicety: I do not need a third pass.** Once I have one answer, **the other is `both ^ first`,
> because `both` is `a ^ b` and XOR undoes itself.**
>
> **Two passes, so still O(n) time, and O(1) space.**
>
> **And I would name the assumption**: this needs exactly two loners. **If there were none, `both` would be
> zero, the split bit would be zero, and it would return a pair of zeros without complaining.**"

**"Every number appears three times except one. Now what?"**

> "**Pairing is no use — three of a thing does not cancel.** So I stop thinking about the numbers and think
> about the bit positions instead.
>
> **For each of the thirty-two places, I count how many numbers have a one there.** **Every value that appears
> three times contributes either three or zero to that column**, so the whole column is a multiple of three
> plus whatever the loner contributed. **Take the count modulo three and you have the loner's bit.**
>
> **Do that thirty-two times and you have rebuilt the loner.**
>
> **The general statement is nicer than the special case: appearing `k` times means counting modulo `k`.** And
> the twice case is just `k = 2` — **modulo two is precisely what XOR already does, which is why the first
> problem needed no counting at all.**
>
> **Cost: thirty-two passes over the list, so O(32n) — linear, but with a real constant.** **There is a
> single-pass version using two variables as a small state machine that tracks 'seen once' and 'seen twice',
> and it is thirty-two times faster.** **I would mention it and still write the column version**, because I can
> explain the column version under pressure and the state machine is the kind of code that is easy to write
> subtly wrong.
>
> **One Python-specific point: if the input can be negative I have to fix the sign at the end**, subtracting
> `1 << 32` when bit 31 is set, **because Python integers have no top bit and would otherwise return four
> billion instead of minus three.**"

**"What is 1 XOR 2 XOR ... XOR n?"**

> "**In constant time, and the way to get there is to write out the first eight and look.**
>
> **0, 1, 3, 0, 4, 1, 7, 0.** **It resets to zero every fourth step**, and the four cases are:
> `n % 4 == 0` gives `n`; `1` gives `1`; `2` gives `n + 1`; `3` gives `0`.
>
> **I would derive that at the desk rather than claim to remember it** — it takes about twenty seconds and it
> is much more convincing than reciting.
>
> **And an arbitrary range is two of those: `xor_to(high) ^ xor_to(low - 1)`**, because everything below `low`
> appears in both terms and cancels. **That is the prefix-sum subtraction with XOR instead of minus, and it
> works for the same reason — XOR is its own inverse.**
>
> **That inverse property is worth one more sentence, because it is what makes prefix XOR a real technique.**
> **`prefix[r+1] ^ prefix[l]` is the XOR of a subarray**, so a thousand range questions on a hundred-thousand
> element list go from a hundred million operations to about a hundred thousand. **And `prefix[i] ==
> prefix[k]` means the stretch between them XORs to zero**, which is how a whole family of 'count the
> subarrays where...' problems collapses into counting equal prefix values."

### The model answer

*"Talk me through the XOR family of problems and what connects them."*

> "**They are all one fact: `a ^ a` is zero, so things that come in pairs disappear.**
>
> **The base case is one loner in a list of pairs.** XOR everything; the pairs cancel; the loner survives.
> **Linear time, constant space, and the reason it works is that XOR ignores order — so I can imagine the
> duplicates grouped together and every group is zero.**
>
> **The second case is one number missing from zero to n.** Now I have to supply the partners: **XOR the list
> together with the full range.** Everything present appears twice and cancels; the absent one appears once
> and survives. **The sum formula also works and can overflow. XOR cannot overflow, because it never
> carries.**
>
> **The third case is two loners, and this is the one that is actually a question.** XORing everything gives
> `a ^ b`, which does not determine either. **So I split.** A set bit in `a ^ b` marks a place where the two
> answers disagree, **so I isolate the lowest one with `both & -both` and use it to divide the list.** Equal
> numbers agree everywhere, so pairs stay together and still cancel. **The loners are guaranteed to separate.**
> Two easy problems, and the second answer falls out as `both ^ first`.
>
> **The fourth case breaks the pattern deliberately: everything three times.** Pairing cannot help, **so I
> count each bit position modulo three.** **The general rule is that `k` copies means counting modulo `k`, and
> XOR is just the `k = 2` case done for free.**
>
> **Then two things that are the same idea at a different scale.** **The XOR of a range is periodic with period
> four**, so it is constant time rather than a loop. **And prefix XOR gives subarray XOR in one operation**,
> because XOR is its own inverse — the same trick as prefix sums.
>
> **What ties it together is a habit rather than a formula.** **Whenever a problem says 'constant extra space'
> and involves things that repeat, I ask what cancels.** **If the answer is 'pairs', it is XOR. If it is
> 'triples', it is counting modulo three. If nothing cancels, it is a different technique entirely and I stop
> trying.**
>
> **The failure mode I watch for is assuming the repeat count.** **Plain XOR gives a right-looking answer
> whenever the repeats happen to be even**, so a hand-made test with two copies passes and the real input with
> three copies fails. **I read the repeat count out of the problem statement and say it out loud before I write
> a line.**"

---

## 9. Recall card

**One fact runs the whole family: `a ^ a = 0`, `a ^ 0 = a`, and order does not matter.** So XORing a list
cancels everything that comes in pairs. **The rearrangement argument IS the proof** — group the duplicates,
every bracket is zero. **XOR is "is the count of ones in this column odd?", asked independently per column, so
nothing carries and nothing overflows.**

**One loner: XOR the list. One missing from 0..n: XOR the list against the range** (seed the accumulator with
`len(numbers)`, or the top of the range has no partner). **Prefer this to the sum formula, which overflows.**

**Two loners is the real question.** XORing everything gives `a ^ b`, which **does not determine the pair** —
6 could be 3^5 or 1^7. **A set bit in `a ^ b` means they DISAGREE there**, so isolate one with `both & -both`
and split the list on it: **duplicates agree everywhere so pairs stay together; the loners are forced apart.**
Then `second = both ^ first` — no third pass. **Needs exactly two loners, or it silently returns `(0, 0)`.**

**k copies means counting modulo k.** Three times each: count every bit position mod 3, 32 passes, O(32n).
XOR is the `k = 2` case for free. **In Python, fix the sign at the end (`answer - (1 << 32)` when bit 31 is
set) or minus three comes back as 4,294,967,293.**

**XOR is its own inverse, so it does prefix sums.** `xor(l..r) = prefix[r+1] ^ prefix[l]`, and
`prefix[i] == prefix[k]` means that stretch XORs to zero. **The XOR of 0..n has period four**: `n, 1, n+1, 0`
for `n%4 = 0,1,2,3`. **Biggest XOR pair: build the answer from the top bit down and ask `wanted ^ prefix in
prefixes` — O(32n), not O(n²).** **And the trap that passes small tests: plain XOR looks correct whenever
every repeat count happens to be even.**
