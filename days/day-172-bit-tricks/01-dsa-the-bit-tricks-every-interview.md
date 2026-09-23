---
day: 172
track: dsa
title: "The bit tricks every interview uses"
phase: "Bits and maths"
status: written
---

# The bit tricks every interview uses

## 1. What this is, and why they ask it

**There are about ten bit expressions that cover almost every bit question ever asked.** `n & (n - 1)`.
`n & -n`. `1 << k`. `(1 << k) - 1`. `a ^ b`. That is most of it.

**Each one is short, each one has a one-line reason, and the reason is the part that matters.** Anybody can
memorise `n & (n - 1)`. **Only the person who can say why it works can use it on a problem they have not
seen.**

[Yesterday](../day-171-binary-and-bits/01-dsa-binary-bits-and-why-they.md) you learnt what the operators do.
**Today is the small kit of moves built out of them**, and the habit of naming the reason out loud.

They ask it because **these questions are short, unbluffable, and used as filters.** "Count the set bits" takes
four minutes to ask and answer. **In a phone screen that is exactly what an interviewer wants**: a question
where you either have the machinery or you do not, and no amount of talking around it helps.

**And because bit tricks appear inside bigger answers.** Enumerating subsets in a backtracking problem. The
mask in bitmask DP. Hashing into a power-of-two table. **The trick is rarely the question — it is a line
inside the question**, and if you have to stop and derive it, you lose the thread of the real problem.

By the end of this lesson you can write all ten from memory, say the one-line reason for each, use them to
solve five named interview problems, and enumerate the subsets of a set and the submasks of a mask — which is
where the tricks stop being tricks and start being a technique.

---

## 2. The story

The shop had three chairs and two of them had been broken for years, and Mahadevan cut hair in the middle one.

Shivu had swept that floor since he was eleven. What he watched, forty times a day, was the same twenty
minutes: the sheet snapped open, the comb, the scissors going like an insect, and the man in the chair
standing up looking like a slightly different man.

**What Shivu could not work out was how few things Mahadevan actually did.**

He counted them once, on a slow Monday afternoon. The comb lifted a section of hair and held it out flat. The
scissors went across the top of the comb. The comb came down half its own width and did the same thing again.
**That was it. That was most of a haircut.**

There were four or five other moves for the edges — the thing he did at the neck with the back of the blade,
the two fingers he put against the ear.

**Nine or ten moves in the whole trade, and Shivu had watched every one of them a thousand times.**

So one evening he asked if he could try, on a boy from the next lane who was not paying anyway.

It went badly, and it went badly in a way that surprised him. **He knew all the moves. He could do each one
on its own, and they looked right.** What he could not do was look at a head and know which move it wanted.

Mahadevan watched from the doorway and did not laugh, which Shivu was grateful for. Then he said a thing that
took about two years to land properly.

**"You have learnt what my hands do. You have not learnt why they do it."**

He picked up the comb.

**"This one is for taking length off the top and keeping it even. And it works because the comb decides how
much hair sticks out, not me. My hand only has to stay straight."**

He put it down again.

**"Learn why a move works and you know what it is for. After that the head tells you which one."**

---

## 3. The idea in plain English

**Every trick below is one expression and one sentence.** The expression is what your hands do. The sentence
is why. **Learn them in pairs, and never one without the other.**

### The two core moves

Everything in this lesson is built on two facts about what happens near the lowest `1` in a number.

**`n - 1` flips the lowest set bit to zero and turns everything below it into ones.** That is just borrowing,
the same borrowing you do in ordinary subtraction.

```
   n     = 10110000
   n - 1 = 10101111
                ^^^^ the lowest 1 became 0, and everything
                     under it became 1
```

**So `n & (n - 1)` clears the lowest set bit.** Above the lowest one, the two numbers are identical, so AND
keeps them. At the lowest one, one number has `1` and the other has `0`, so it goes. Below it, one number has
all zeros, so those stay zero.

**And `n & -n` keeps only the lowest set bit.** `-n` in two's complement is "flip everything and add one",
which is exactly `~n + 1` — and adding one to a flipped number ripples up to the first place that was a `1`.
**Everything above the lowest set bit ends up flipped, everything below stays zero, and the lowest set bit
itself survives in both.**

```
   n      = 10110000
   -n     = 01010000
   n & -n = 00010000    only the lowest 1 is left
```

**Those two are opposites and you should say them as a pair.** One removes the lowest one. One keeps only the
lowest one. **Almost every counting or set-walking trick is one of these in a loop.**

### The masks

**A mask is a number you AND or OR against, chosen so that it lets through exactly the bits you care about.**

```
   1 << k          a single 1, in place k         1 << 4 = 00010000
   (1 << k) - 1    k ones at the bottom           (1<<4)-1 = 00001111
   ~(1 << k)       all ones EXCEPT place k        a hole
```

**`(1 << k) - 1` is the workhorse.** It is "the bottom `k` bits", and you use it to cut a number down to a
fixed width, to take a remainder, and to say "just this part".

**Bracket it. Always.** `1 << k - 1` means `1 << (k - 1)` — a single bit rather than a run of ones — because
subtraction binds tighter than shifting. **Nothing errors. You get a plausible wrong number.**

### The one-line tests

```
   n > 0 and n & (n - 1) == 0     n is a POWER OF TWO
                                  exactly one bit set, so clearing it leaves 0

   n >= 0 and n & (n + 1) == 0    n is ALL ONES: 0, 1, 3, 7, 15, 31 ...
                                  adding one carries all the way past the top

   n & 1                          the last bit: 1 if odd, 0 if even
```

**The `n > 0` guard on the power-of-two test is not decoration.** `0 & -1` is `0`, so without it zero passes.
**It is the single most common one-character bug in this whole topic.**

### Counting, and the two ways to say it

**Set bits are counted by removing them one at a time.**

```
   count = 0
   while n:
       n &= n - 1     removes exactly one set bit
       count += 1
```

**One iteration per *set* bit**, not per bit position. This is **Brian Kernighan's algorithm** and it is worth
knowing by name, because interviewers recognise it.

**And there is a second way, which matters when you need the answer for every number up to some limit.**

```
   bits[i] = bits[i & (i - 1)] + 1
```

**Read it as a sentence: the number of set bits in `i` is one more than the number in `i` with its lowest set
bit removed.** And `i & (i - 1)` is always smaller than `i`, so the smaller answer is already there. **That is
a one-line dynamic programme**, and it is LeetCode 338 in its entirety.

### XOR, and what it is really for

**XOR is "exactly one", which is the same as "different".** So `a ^ b` has a `1` in every place where `a` and
`b` disagree.

**Three consequences, and each one is a named interview problem.**

**Counting the differences is counting the set bits of the XOR.** That is **Hamming distance**, LeetCode 461,
one line.

**`a ^ a` is 0 and `a ^ 0` is a.** So XORing a whole list together **cancels everything that appears twice**
and leaves the one that does not. That is the single-number family, and
[tomorrow](../day-173-xor/README.md) is entirely about it.

**Swapping without a temporary** — `a ^= b; b ^= a; a ^= b` — is a party trick, and you should know it and
also know that **it silently zeroes the value if the two are the same variable.** Say both halves.

### Walking a set, and the subset trick

**Here is where the tricks become a technique.** A subset of `n` items is an `n`-bit number: **bit `i` set
means item `i` is in.** You met this in [bitmask DP](../day-160-bitmask-dp/README.md); this is the mechanics
under it.

```
   for mask in range(1 << n):        every subset of n items
       for i in range(n):
           if mask >> i & 1:         is item i in this subset?
               ...
```

**`1 << n` is `2^n`, so the outer loop is every possible subset**, and `mask >> i & 1` is the get-bit
one-liner from yesterday.

**If a mask is sparse, walk only its set bits instead of all `n` positions.**

```
   while mask:
       low = mask & -mask            isolate the lowest set bit
       position = low.bit_length() - 1
       mask &= mask - 1              clear it and go again
```

**Both core moves, in four lines.** Isolate to read it, clear to move on.

**And the one that looks like magic: every submask of a mask, in descending order.**

```
   sub = mask
   while True:
       ...use sub...
       if sub == 0: break
       sub = (sub - 1) & mask
```

**`sub - 1` borrows into the bits below**, and `& mask` throws away everything that was never part of the mask
in the first place — **so you land on the next smaller subset without ever visiting a number that is not one.**
It is worth having, because it turns an enumeration that looks like `2^n × 2^n` into `3^n`.

### The small ones worth knowing

```
   n >> 1              halve, rounding down
   n << 1              double
   n & (size - 1)      n % size, when size is a power of two
   ord(c) ^ 32         swap the case of an ASCII letter
   x | (x + 1)         set the lowest zero bit
```

**The case one is a nice example of the whole lesson's point.** `'a'` is 97 and `'A'` is 65, and the
difference is 32, **which is one bit** — so the cases of every ASCII letter differ in exactly one place.
**Knowing that is a trick. Knowing why is a fact about the character table**, and the fact is what lets you
answer when someone asks about digits or punctuation.

---

## 4. The picture

The two core moves, side by side:

```
   CLEAR the lowest set bit              ISOLATE the lowest set bit

   n     = 1 0 1 1 0 0 0 0               n      = 1 0 1 1 0 0 0 0
   n - 1 = 1 0 1 0 1 1 1 1               -n     = 0 1 0 1 0 0 0 0
           ----------------                       ----------------
   n&(n-1)= 1 0 1 0 0 0 0 0              n & -n = 0 0 0 1 0 0 0 0
                 ^                                     ^
            it is GONE                          only IT is left

   Same bit. One move takes it away, one move keeps
   only it. Say them as a pair and you will never mix
   them up.
```

Why `n - 1` behaves like that — the borrowing, drawn out:

```
   176   1 0 1 1 0 0 0 0
   -  1

   the last place is 0, so you borrow from the left
   ... and keep borrowing until you find a 1

   1 0 1 1 0 0 0 0
         ^ this is the first 1 you meet
           it becomes 0
           and every 0 you passed becomes 1

   175   1 0 1 0 1 1 1 1

   THAT IS THE WHOLE REASON n & (n-1) WORKS.
   Nothing above the lowest 1 changed, so AND keeps it.
   The lowest 1 changed, so AND kills it.
   Below it, one side is all 0s, so AND gives 0.
```

The masks, drawn:

```
   place    7 6 5 4 3 2 1 0

   1 << 4   0 0 0 1 0 0 0 0     one bit, in place 4
   (1<<4)-1 0 0 0 0 1 1 1 1     the bottom four bits
   ~(1<<4)  1 1 1 0 1 1 1 1     everything EXCEPT place 4

   1 << 4 - 1                   0 0 0 0 1 0 0 0    <- the trap
                                this is 1 << 3, not (1<<4)-1
```

Subsets as numbers — three items, eight subsets:

```
   items:  [3, 5, 7]
            ^  ^  ^
   bit:     0  1  2

   mask 000  ->  []              0
   mask 001  ->  [3]             1
   mask 010  ->  [5]             2
   mask 011  ->  [3, 5]          3
   mask 100  ->  [7]             4
   mask 101  ->  [3, 7]          5
   mask 110  ->  [5, 7]          6
   mask 111  ->  [3, 5, 7]       7

   Counting from 0 to 2^n - 1 IS listing every subset.
   No recursion, no extra structure - the number is the subset.
```

---

## 5. The code, built step by step

### A way to see what happened

```python
def show(number: int, width: int = 8) -> str:
    """The bit pattern of `number` in `width` bits, so you can see what happened."""
    return format(number & ((1 << width) - 1), f"0{width}b")
```

**Write this first, before any of the tricks.** Bit code is unreadable when it goes wrong, and the difference
between a five-minute bug and a fifty-minute one is whether you can see the pattern.

**`number & ((1 << width) - 1)` is the mask trick doing real work**: it cuts an arbitrary-width Python integer
down to `width` bits, **which is also how you make a negative number show its two's complement pattern.**

### The two core moves

```python
def lowest_set_bit(number: int) -> int:
    """n & -n keeps ONLY the lowest set bit. -n is ~n + 1, so it flips everything above."""
    return number & -number


def clear_lowest_set_bit(number: int) -> int:
    """n & (n - 1) REMOVES the lowest set bit. Borrowing does the work."""
    return number & (number - 1)
```

**Two functions, four words of difference, opposite jobs.** In an interview you would inline both — the point
of naming them here is that **the name is the sentence you have to be able to say.**

### Counting, with the guard that matters

```python
def count_set_bits(number: int) -> int:
    """Kernighan: one iteration per SET bit. Guarded, because negatives never terminate."""
    if number < 0:
        raise ValueError("count_set_bits needs a non-negative number")
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count
```

**The guard is the interesting line and section 7 is about it.** On a negative Python integer this loop does
not crash — **it runs forever**, drifting to −16, −32, −64 and never reaching zero.

### The one-line tests

```python
def is_power_of_two(number: int) -> bool:
    """Exactly one set bit. The `> 0` guard is not decoration: 0 & -1 == 0."""
    return number > 0 and (number & (number - 1)) == 0


def is_all_ones(number: int) -> bool:
    """0, 1, 3, 7, 15 ... - one less than a power of two. Adding one carries all the way."""
    return number >= 0 and (number & (number + 1)) == 0
```

**These two are a matched pair and interviewers like the second one**, because almost nobody has it. **`n + 1`
on a run of ones carries all the way past the top**, leaving a single high bit that shares nothing with `n`.

### Hamming distance, in one line

```python
def hamming_distance(a: int, b: int) -> int:
    """XOR marks every place they differ; count those places."""
    return count_set_bits(a ^ b)
```

**Say the sentence before you write the line.** "XOR is 'different', so the set bits of the XOR are exactly
the disagreements." **That sentence is the answer to LeetCode 461**, and the code is a formality.

### Counting bits for every number at once

```python
def counting_bits(limit: int) -> list[int]:
    """bits[i] = bits[i with its lowest set bit removed] + 1. One smaller answer, always."""
    bits = [0] * (limit + 1)
    for i in range(1, limit + 1):
        bits[i] = bits[i & (i - 1)] + 1
    return bits
```

**`i & (i - 1)` is strictly smaller than `i` for every positive `i`**, so the value you need has already been
filled in. **That is the whole of the correctness argument**, and it is worth saying out loud because it is
what makes this a dynamic programme rather than a coincidence.

**There is a second recurrence — `bits[i] = bits[i >> 1] + (i & 1)`** — "the bits of `i` are the bits of `i`
without its last one, plus that last one". **Both are one line. Know both, and say what each is claiming.**

### Reversing bits, and why width has to be stated

```python
def reverse_bits(number: int, width: int = 32) -> int:
    """Take the bottom bit off `number` and push it onto the bottom of the answer."""
    result = 0
    for _ in range(width):
        result = (result << 1) | (number & 1)
        number >>= 1
    return result
```

**The loop runs exactly `width` times, not "until the number runs out".** That is the point of this problem:
**reversing `00000001` in eight bits gives `10000000`, and reversing it in "as many bits as it needs" gives
`1`.** Python has no width, so **you must supply one**, and saying that out loud is most of the credit.

### Subsets, and walking only what is set

```python
def subsets(items: list[int]) -> list[list[int]]:
    """Every subset of n items is an n-bit number: bit i means 'item i is in'."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        out.append([items[i] for i in range(n) if mask >> i & 1])
    return out
```

**Two loops and no recursion.** The outer one counts from `0` to `2^n - 1`; the inner one asks the get-bit
question of each place. **`mask >> i & 1` needs no brackets — `>>` binds tighter than `&` — but write them
anyway.**

```python
def set_bit_positions(mask: int) -> list[int]:
    """Walk only the set bits. Each step isolates the lowest one and then clears it."""
    positions = []
    while mask:
        low = mask & -mask
        positions.append(low.bit_length() - 1)
        mask &= mask - 1
    return positions
```

**Both core moves in one loop, doing different jobs.** Isolate to find out *where* the bit is; clear to move
past it. **`bit_length() - 1` turns a single-bit number into its place**, because a lone bit in place 4 is the
number 16, whose bit length is 5.

```python
def submasks(mask: int) -> list[int]:
    """Every subset of a mask, biggest first. (sub - 1) & mask is the next one down."""
    out = []
    sub = mask
    while True:
        out.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return out
```

**The `if sub == 0: break` is inside the loop and after the append**, and that is deliberate: **zero is a
legitimate submask and must be visited, but `(0 - 1) & mask` is `mask` again**, so testing at the top gives you
an endless circle. **This is the one loop in the lesson whose shape you should memorise rather than re-derive
under pressure.**

### The complete solution

```python
"""Day 172 - the bit tricks, all of them, with the reason each one works."""

from __future__ import annotations


def show(number: int, width: int = 8) -> str:
    """The bit pattern of `number` in `width` bits, so you can see what happened."""
    return format(number & ((1 << width) - 1), f"0{width}b")


def lowest_set_bit(number: int) -> int:
    """n & -n keeps ONLY the lowest set bit. -n is ~n + 1, so it flips everything above."""
    return number & -number


def clear_lowest_set_bit(number: int) -> int:
    """n & (n - 1) REMOVES the lowest set bit. Borrowing does the work."""
    return number & (number - 1)


def count_set_bits(number: int) -> int:
    """Kernighan: one iteration per SET bit. Guarded, because negatives never terminate."""
    if number < 0:
        raise ValueError("count_set_bits needs a non-negative number")
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count


def is_power_of_two(number: int) -> bool:
    """Exactly one set bit. The `> 0` guard is not decoration: 0 & -1 == 0."""
    return number > 0 and (number & (number - 1)) == 0


def is_all_ones(number: int) -> bool:
    """0, 1, 3, 7, 15 ... - one less than a power of two. Adding one carries all the way."""
    return number >= 0 and (number & (number + 1)) == 0


def low_mask(width: int) -> int:
    """`width` ones at the bottom. Bracket the shift or you get a single bit instead."""
    return (1 << width) - 1


def hamming_distance(a: int, b: int) -> int:
    """XOR marks every place they differ; count those places."""
    return count_set_bits(a ^ b)


def counting_bits(limit: int) -> list[int]:
    """bits[i] = bits[i with its lowest set bit removed] + 1. One smaller answer, always."""
    bits = [0] * (limit + 1)
    for i in range(1, limit + 1):
        bits[i] = bits[i & (i - 1)] + 1
    return bits


def reverse_bits(number: int, width: int = 32) -> int:
    """Take the bottom bit off `number` and push it onto the bottom of the answer."""
    result = 0
    for _ in range(width):
        result = (result << 1) | (number & 1)
        number >>= 1
    return result


def subsets(items: list[int]) -> list[list[int]]:
    """Every subset of n items is an n-bit number: bit i means 'item i is in'."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        out.append([items[i] for i in range(n) if mask >> i & 1])
    return out


def set_bit_positions(mask: int) -> list[int]:
    """Walk only the set bits. Each step isolates the lowest one and then clears it."""
    positions = []
    while mask:
        low = mask & -mask
        positions.append(low.bit_length() - 1)
        mask &= mask - 1
    return positions


def submasks(mask: int) -> list[int]:
    """Every subset of a mask, biggest first. (sub - 1) & mask is the next one down."""
    out = []
    sub = mask
    while True:
        out.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return out


def single_number(numbers: list[int]) -> int:
    """Pairs cancel under XOR, so what is left is the one that had no pair."""
    answer = 0
    for value in numbers:
        answer ^= value
    return answer


def swap_case(letter: str) -> str:
    """Letters differ by exactly one bit between the cases: the 32s place."""
    return chr(ord(letter) ^ 32)


if __name__ == "__main__":
    print("THE TWO CORE MOVES, on 176 = 10110000")
    n = 0b10110000
    print(f"  n              {show(n)}  = {n}")
    print(f"  n - 1          {show(n - 1)}  = {n - 1}   (lowest 1 flipped, ones below)")
    print(f"  n & (n - 1)    {show(clear_lowest_set_bit(n))}  = {clear_lowest_set_bit(n)}"
          f"   CLEARS the lowest 1")
    print(f"  -n             {show(-n)}  = {-n}   (flip and add one)")
    print(f"  n & -n         {show(lowest_set_bit(n))}  = {lowest_set_bit(n)}"
          f"    ISOLATES the lowest 1")

    print()
    print("MASKS")
    for k in (1, 3, 4, 8):
        print(f"  low_mask({k})    {show(low_mask(k), 8)}  = {low_mask(k):>3}   ({k} ones)")
    print(f"  1 << 4         {show(1 << 4)}  = {1 << 4:>3}   (one bit)")
    print(f"  (1 << 4) - 1   {show((1 << 4) - 1)}  = {(1 << 4) - 1:>3}   (four ones)")
    print(f"  1 << 4 - 1     {show(1 << 4 - 1)}  = {1 << 4 - 1:>3}   THE PRECEDENCE TRAP")

    print()
    print("COUNTING, and the two one-line tests")
    for value in (0, 1, 7, 8, 176, 255, 1024):
        print(f"  {value:>5}  {show(value, 11)}  bits={count_set_bits(value)}"
              f"  power_of_two={is_power_of_two(value)}  all_ones={is_all_ones(value)}")

    print()
    print("HAMMING DISTANCE - count where they differ")
    for a, b in ((1, 4), (3, 1), (176, 160)):
        print(f"  {show(a)} ^ {show(b)} = {show(a ^ b)}  -> {hamming_distance(a, b)}")

    print()
    print("COUNTING BITS FOR 0..15 IN ONE PASS")
    print(f"  {counting_bits(15)}")

    print()
    print("REVERSE BITS, in 8 bits")
    for value in (1, 0b10110000, 0b11111111):
        print(f"  {show(value)} -> {show(reverse_bits(value, 8))}")

    print()
    print("SUBSETS OF [3, 5, 7] - the mask IS the subset")
    for mask, subset in enumerate(subsets([3, 5, 7])):
        print(f"  mask {mask:03b}  ->  {subset}")

    print()
    print("WALKING ONLY THE SET BITS of 176")
    print(f"  positions: {set_bit_positions(176)}   (8 bits wide, 3 steps taken)")

    print()
    print("EVERY SUBMASK OF 1011")
    print(f"  {[format(s, '04b') for s in submasks(0b1011)]}")

    print()
    print("PAIRS CANCEL")
    print(f"  single_number([4, 1, 2, 1, 2]) = {single_number([4, 1, 2, 1, 2])}")

    print()
    print("THE 32s PLACE IS THE CASE BIT")
    for letter in ("a", "Z", "k"):
        print(f"  {letter} = {ord(letter):>3} = {show(ord(letter))}"
              f"  ->  {swap_case(letter)} = {ord(swap_case(letter)):>3}"
              f" = {show(ord(swap_case(letter)))}")

    print()
    print("VERIFICATION")
    bad = 0
    for value in range(0, 5000):
        if count_set_bits(value) != value.bit_count():
            bad += 1
        if is_power_of_two(value) != (value > 0 and value.bit_count() == 1):
            bad += 1
        if is_all_ones(value) != (value == (1 << value.bit_length()) - 1):
            bad += 1
        if reverse_bits(reverse_bits(value, 16), 16) != value:
            bad += 1
    if counting_bits(4999) != [v.bit_count() for v in range(5000)]:
        bad += 1
    if len(subsets([1, 2, 3, 4, 5])) != 32:
        bad += 1
    if len(submasks(0b1011)) != 2 ** 3:
        bad += 1
    print(f"  {bad} mismatches over 5,000 values, 4 checks each, plus 3 whole-list checks")
```

Running it:

```
THE TWO CORE MOVES, on 176 = 10110000
  n              10110000  = 176
  n - 1          10101111  = 175   (lowest 1 flipped, ones below)
  n & (n - 1)    10100000  = 160   CLEARS the lowest 1
  -n             01010000  = -176   (flip and add one)
  n & -n         00010000  = 16    ISOLATES the lowest 1

MASKS
  low_mask(1)    00000001  =   1   (1 ones)
  low_mask(3)    00000111  =   7   (3 ones)
  low_mask(4)    00001111  =  15   (4 ones)
  low_mask(8)    11111111  = 255   (8 ones)
  1 << 4         00010000  =  16   (one bit)
  (1 << 4) - 1   00001111  =  15   (four ones)
  1 << 4 - 1     00001000  =   8   THE PRECEDENCE TRAP

COUNTING, and the two one-line tests
      0  00000000000  bits=0  power_of_two=False  all_ones=True
      1  00000000001  bits=1  power_of_two=True  all_ones=True
      7  00000000111  bits=3  power_of_two=False  all_ones=True
      8  00000001000  bits=1  power_of_two=True  all_ones=False
    176  00010110000  bits=3  power_of_two=False  all_ones=False
    255  00011111111  bits=8  power_of_two=False  all_ones=True
   1024  10000000000  bits=1  power_of_two=True  all_ones=False

HAMMING DISTANCE - count where they differ
  00000001 ^ 00000100 = 00000101  -> 2
  00000011 ^ 00000001 = 00000010  -> 1
  10110000 ^ 10100000 = 00010000  -> 1

COUNTING BITS FOR 0..15 IN ONE PASS
  [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]

REVERSE BITS, in 8 bits
  00000001 -> 10000000
  10110000 -> 00001101
  11111111 -> 11111111

SUBSETS OF [3, 5, 7] - the mask IS the subset
  mask 000  ->  []
  mask 001  ->  [3]
  mask 010  ->  [5]
  mask 011  ->  [3, 5]
  mask 100  ->  [7]
  mask 101  ->  [3, 7]
  mask 110  ->  [5, 7]
  mask 111  ->  [3, 5, 7]

WALKING ONLY THE SET BITS of 176
  positions: [4, 5, 7]   (8 bits wide, 3 steps taken)

EVERY SUBMASK OF 1011
  ['1011', '1010', '1001', '1000', '0011', '0010', '0001', '0000']

PAIRS CANCEL
  single_number([4, 1, 2, 1, 2]) = 4

THE 32s PLACE IS THE CASE BIT
  a =  97 = 01100001  ->  A =  65 = 01000001
  Z =  90 = 01011010  ->  z = 122 = 01111010
  k = 107 = 01101011  ->  K =  75 = 01001011

VERIFICATION
  0 mismatches over 5,000 values, 4 checks each, plus 3 whole-list checks
```

**Look at the `all_ones` column for `0` and `7`: both true.** Zero is the empty run of ones and seven is
`111`. **And look at `255`: eight set bits, all ones, not a power of two** — three tests disagreeing about the
same number is a good sign that they are testing different things.

**Look at the reverse of `10110000` in eight bits: `00001101`.** Reversed in thirty-two bits it would be a
number in the hundreds of millions. **The width is not a detail.**

---

## 6. What it costs

**Counting set bits — count the iterations out loud.**

```
KERNIGHAN, one iteration per SET bit

  176  = 10110000    ->  3 iterations
  255  = 11111111    ->  8 iterations
  1024 = 10000000000 ->  1 iteration
  1 << 31            ->  1 iteration

THE NAIVE SHIFT LOOP, one per bit POSITION

  176     ->  8 iterations
  255     ->  8 iterations
  1024    -> 11 iterations
  1 << 31 -> 32 iterations

-> They TIE when every bit is set (255).
-> They differ most when one bit is set high (1 << 31): 1 against 32.
```

**Both are O(1) on fixed-width integers, and you should say so** — thirty-two is a constant. **The constant is
the whole argument**, and it is real when you do this inside a loop over a million values.

**Counting bits for every number to `limit`.**

```
counting_bits(n): one table write per value, each O(1)

  n = 15      ->  15 writes
  n = 100,000 ->  100,000 writes

-> O(n) time, O(n) space for the table itself.

Compare with calling count_set_bits on each value:
  100,000 values x up to 17 iterations = ~1.7 million steps
  against 100,000.
```

**Subsets.**

```
for mask in range(1 << n): for i in range(n):

  outer loop: 2^n masks
  inner loop: n positions each

  -> n x 2^n

  n = 10  ->    10 x 1,024     =      10,240
  n = 15  ->    15 x 32,768    =     491,520
  n = 20  ->    20 x 1,048,576 =  20,971,520    about a second
  n = 25  ->    25 x 33,554,432 = 838 million   no

-> which is why "n <= 20" in a problem statement is a hint
   that the answer is a bitmask.
```

**Walking only the set bits changes the inner loop.**

```
  inner loop over all n positions:      n steps, always
  inner loop with mask &= mask - 1:     s steps, s = set bits

  a mask with 3 bits set out of 20:
    20 steps  ->  3 steps

-> nearly 7x, on the inner loop of a 2^n outer loop
```

**Submask enumeration, which is the surprising one.**

```
The naive way: for each mask, loop over all 2^n numbers and
keep the ones that are submasks.

  2^n masks x 2^n candidates = 4^n

  n = 12 -> 4^12 = 16.7 million
  n = 16 -> 4^16 = 4.3 billion


With sub = (sub - 1) & mask, you only ever visit real submasks.
Across the whole enumeration each of the n bits is in exactly
one of three states:
  out of the mask;
  in the mask and in the submask;
  in the mask and out of the submask.

Three states per bit:

  3^n

  n = 12 -> 3^12 = 531,441       31x better
  n = 16 -> 3^16 = 43 million    100x better
```

**Space.**

```
every trick here is O(1) extra space

  count_set_bits, is_power_of_two, hamming_distance,
  reverse_bits, set_bit_positions:  a few integers

counting_bits:   O(n) - the table IS the answer
subsets:         O(n x 2^n) - the output itself
show():          O(width) - a string
```

---

## 7. The traps

**The negative-number infinite loop, which is the worst one here.**

```python
count_set_bits(-8)     # without the guard
```

**This does not raise. It does not stop.** In Python, integers are arbitrary width and a negative number
behaves as though it has infinitely many leading ones, **so clearing the lowest set bit just moves the
problem left, forever.**

```
   -8  & -9  = -16
   -16 & -17 = -32
   -32 & -33 = -64
   ...
```

**A hang is worse than a crash**, because a crash tells you where it was. **Guard, or mask with `& 0xFFFFFFFF`
first** — and say which one you are doing and why.

**With the guard, you get something you can read:**

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in count_set_bits
ValueError: count_set_bits needs a non-negative number
```

**The precedence trap, again, because it is the one that keeps happening.**

```
1 << 4 - 1   = 8      this is 1 << (4 - 1)
(1 << 4) - 1 = 15     this is what you meant
```

**No error. A plausible number. Every downstream result quietly wrong.** Two brackets.

**The power-of-two guard.**

```
is_power_of_two(0)   without the `number > 0` guard  ->  True
```

**Because `0 & -1` is `0`.** Zero is not a power of two, `0` is the input every test suite includes, **and the
fix is eight characters.**

**Testing at the top of the submask loop.**

```python
sub = mask
while sub:                 # WRONG
    ...
    sub = (sub - 1) & mask
```

**This never visits the empty submask**, which is a legitimate answer and is usually the base case of whatever
you are enumerating. **And if you fix it by moving the test the other way you get an endless circle**, because
`(0 - 1) & mask` is `-1 & mask`, which is `mask` again. **The append-then-break shape is the correct one.**

**Reversing bits without stating the width.**

```python
def reverse_bits_wrong(number: int) -> int:
    result = 0
    while number:                    # "until it runs out"
        result = (result << 1) | (number & 1)
        number >>= 1
    return result
```

```
reverse_bits_wrong(1)      = 1        expected 2147483648
reverse_bits_wrong(0b1011) = 13       expected 3489660928
```

**Nothing errors, and small inputs even look right** — `0b1011` reversed is `1101`, which is 13, and that is a
perfectly sensible answer to a different question. **The problem says thirty-two bits. Loop thirty-two times.**

**The swap trick on the same variable.**

```python
values = [7, 9]
i = j = 0
values[i] ^= values[j]
values[j] ^= values[i]
values[i] ^= values[j]
```

```
values = [0, 0]
```

**`x ^ x` is zero, so swapping a slot with itself destroys it.** No error, no warning, and the bug only appears
when two positions happen to coincide — **which in a sorting routine is exactly the case nobody tests.**

**Bitwise operators on things that are not integers.**

```python
bin(5)[2] & 1
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for &: 'str' and 'int'
```

**`bin()` gives a string.** This catches people who reach for `bin()` to inspect a number and then keep going
with the result.

**And after any division:**

```python
1 << (6 / 2)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for <<: 'int' and 'float'
```

**`/` gives a float in Python 3. Use `//` anywhere near bit work.**

**Shifting by a negative amount:**

```python
1 << -1
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: negative shift count
```

**Loud and immediate, which puts it in the good category.**

**And the ASCII case trick outside ASCII.** `ord('a') ^ 32` is `'A'`, but **`ord('1') ^ 32` is `17`, a control
character**, and on anything outside the plain English letters the trick produces nonsense with no complaint.
**Say "for ASCII letters" out loud when you use it.**

---

## 8. In the interview

### How it gets asked

- *"Count the number of 1 bits."* — LeetCode 191, and the follow-up is always "can you do better?"
- *"Is this a power of two?"* — a one-liner, and they are watching for the guard.
- *"Return a list where the i-th element is the number of 1s in i."* — LeetCode 338.
- *"How many bit positions differ between these two numbers?"* — Hamming distance.
- *"Reverse the bits of a 32-bit unsigned integer."* — LeetCode 190, and width is the whole question.
- *"Generate all subsets of this list."* — and the bitmask answer is the one that gets remembered.

### The first ninety seconds

On "count the set bits, and can you do better":

> "**The obvious version looks at every bit**: `n & 1` to read the bottom one, add it, shift right, repeat
> until the number is zero. **I would write that first — it is correct and anybody can read it.**
>
> **Its cost is one iteration per bit position, up to the highest set bit.** So for `1 << 31` it takes
> thirty-two iterations to find one set bit. **The work depends on where the highest bit is, not on how many
> bits are set**, and that is the inefficiency.
>
> **The better version is `n &= n - 1` in a loop, counting the iterations. That is Kernighan's algorithm.**
>
> **Here is why it works, and this is the part I would want to say properly.** Subtracting one from a number
> **flips its lowest set bit to zero and turns everything below that into ones** — that is ordinary borrowing.
> **Above the lowest set bit, nothing changed, so ANDing keeps it. At the lowest set bit, one side is now zero,
> so ANDing removes exactly that bit.** Below it, one side is all zeros. **So `n & (n - 1)` clears the lowest
> set bit and nothing else.**
>
> **That gives one iteration per *set* bit.** `1024` takes one step instead of eleven. `1 << 31` takes one
> instead of thirty-two.
>
> **I would be honest about the worst case: if every bit is set they are identical.** `255` is eight steps
> either way. **The gain is on sparse numbers.**
>
> **And strictly both are constant time on fixed-width integers**, since thirty-two is a constant — **but the
> constant is real if this sits inside a loop over a million values.**
>
> **One Python caveat: this loop never terminates on a negative number**, because Python integers have no top
> bit. **I would guard, or mask with `& 0xFFFFFFFF`.**
>
> **In production I would write `n.bit_count()`.**"

### The follow-ups

**"Now give me the count for every number from 0 to n."**

> "**Not by calling the counter n times.** That is up to seventeen steps per value at `n = 100,000`, so about
> 1.7 million steps, **when there is a one-line recurrence that does it in 100,000.**
>
> **`bits[i] = bits[i & (i - 1)] + 1`.**
>
> **Read it as a sentence: the number of set bits in `i` is one more than the number in `i` with its lowest
> set bit removed.** And that is exactly what `i & (i - 1)` gives me.
>
> **The reason this is a valid dynamic programme is that `i & (i - 1)` is strictly smaller than `i`**, so by
> the time I reach `i`, the value I need is already in the table. **I would say that out loud, because
> otherwise it looks like a coincidence.**
>
> **There is a second recurrence and it is worth knowing both**: `bits[i] = bits[i >> 1] + (i & 1)` —
> "the bits of `i` are the bits of `i` with its last bit chopped off, plus that last bit". **Same cost, and
> some people find it easier to justify.**
>
> **O(n) time and O(n) space, and the space is the answer itself**, so there is nothing to optimise away."

**"How would you generate every subset of a list?"**

> "**A subset of `n` items is an `n`-bit number.** Bit `i` set means item `i` is in. **So counting from `0` to
> `2^n - 1` lists every subset exactly once**, with no recursion and no bookkeeping.
>
> **Outer loop over `range(1 << n)`, inner loop over the `n` positions, and `mask >> i & 1` asks whether item
> `i` is in this one.**
>
> **The cost is `n × 2^n`, and I want to be concrete about that.** At `n = 20` that is about twenty-one
> million operations — **a second or so.** At `n = 25` it is 838 million, **which is out of reach.** So
> **`n <= 20` in a problem statement is a strong hint that the intended answer is a bitmask.**
>
> **If the masks are sparse I would walk only the set bits instead** — `low = mask & -mask` to isolate one,
> `mask &= mask - 1` to move past it. **Three bits set out of twenty turns twenty inner steps into three.**
>
> **And if I need every *subset of a mask* rather than every subset of the list**, the loop is
> `sub = (sub - 1) & mask`, **which visits only real submasks and turns `4^n` into `3^n`** — at `n = 16` that
> is 4.3 billion against 43 million. **The subtraction borrows into the lower bits and the AND throws away
> anything that was never in the mask.**
>
> **The one thing I would be careful about is the loop shape**: append, then break on zero, then step.
> **Testing at the top skips the empty submask, and `(0 - 1) & mask` is `mask` again**, so the obvious fix
> gives you an endless circle."

**"Is this a power of two? What about a number that is all ones?"**

> "**Power of two: `n > 0 and (n & (n - 1)) == 0`.** A power of two has exactly one set bit, **so clearing the
> lowest set bit must leave zero.**
>
> **The `n > 0` is not decoration.** Without it, `is_power_of_two(0)` returns `True`, because `0 & -1` is `0`
> — **and zero is in every test suite.**
>
> **All ones — 0, 1, 3, 7, 15, 31 — is the matching pair: `n & (n + 1) == 0`.** **Adding one to a run of ones
> carries all the way past the top**, leaving a single high bit that shares no place with the original, **so
> the AND is zero.** That is one less than a power of two, and it is the shape of every low mask you build.
>
> **The related pair I would mention is `n & -n`, which keeps only the lowest set bit** instead of clearing it.
> **The reason is two's complement: `-n` is `~n + 1`, and adding one to the flipped number ripples up to the
> first place that was a one** — so above the lowest set bit everything is flipped and shares nothing, below it
> is all zeros, **and the lowest set bit itself is one in both.** That one is what a Fenwick tree is built on."

### The model answer

*"Talk me through the bit tricks you actually know, and why each one works."*

> "**I would group them, because they are not ten unrelated facts.**
>
> **First, the two moves on the lowest set bit, and they are opposites.** **`n & (n - 1)` removes it.**
> **`n & -n` keeps only it.**
>
> **Both come from what subtraction does.** `n - 1` borrows: **the lowest one becomes zero and everything
> under it becomes one.** So above the lowest one both numbers agree and AND keeps it; at the lowest one they
> disagree and AND kills it. **`-n` is `~n + 1`, which is the same ripple from the other side**, so everything
> above the lowest one is flipped and shares nothing, and only the lowest one survives.
>
> **Second, the masks.** **`1 << k` is one bit in place `k`. `(1 << k) - 1` is `k` ones at the bottom.
> `~(1 << k)` is all ones with a hole.** Those three build every get, set, clear and toggle, and every
> fixed-width truncation. **And I bracket the shift every time, because `1 << k - 1` is `1 << (k - 1)` and it
> fails silently.**
>
> **Third, the one-line tests.** **Power of two is `n > 0 and n & (n - 1) == 0`** — exactly one bit, so
> clearing it leaves nothing, **and the guard matters because zero would otherwise pass.** **All ones is
> `n & (n + 1) == 0`** — the carry runs off the top. **Odd is `n & 1`.**
>
> **Fourth, XOR, which is 'different'.** **`a ^ b` marks every place they disagree**, so Hamming distance is
> the set-bit count of the XOR. **And `a ^ a` is zero**, so XORing a whole list cancels every pair and leaves
> the unpaired one.
>
> **Fifth, and this is the one that stops being a trick: a subset is a number.** **Bit `i` set means item `i`
> is in**, so counting from `0` to `2^n - 1` enumerates every subset with no recursion. **That is what makes
> bitmask DP possible, and it is why those problems cap around `n = 20` — `2^20` is a million and `2^30` is a
> billion.**
>
> **If I had to give you the single most useful line, it is `n & (n - 1)`**, because counting set bits, testing
> powers of two, the counting-bits recurrence and walking a sparse mask are all the same expression **wearing
> four different hats.**
>
> **And the thing I would want to be judged on is not that I remember them.** **It is that each one is a
> sentence about borrowing or about flipping, and once you have the sentence, you can rebuild the expression
> at the desk.**"

---

## 9. Recall card

**Two core moves, and they are opposites.** **`n & (n - 1)` CLEARS the lowest set bit** — `n - 1` borrows, so
the lowest 1 flips and everything below fills with ones; above it nothing changed. **`n & -n` KEEPS ONLY the
lowest set bit** — `-n` is `~n + 1`, the same ripple from the other side. Almost every trick is one of these
in a loop.

**Masks: `1 << k` is one bit; `(1 << k) - 1` is `k` ones at the bottom; `~(1 << k)` is a hole.** **Always
bracket — `1 << k - 1` is `1 << (k-1)`, silently wrong.**

**One-line tests.** Power of two: **`n > 0 and n & (n-1) == 0`** — the guard is not decoration, `0 & -1 == 0`.
All ones (0, 1, 3, 7, 15): **`n & (n+1) == 0`** — the carry runs off the top. Odd: `n & 1`.

**Counting.** Kernighan `while n: n &= n-1` — **one step per SET bit** (1 against 32 for `1 << 31`, tied at
255), and it **HANGS on a negative in Python**, so guard or mask. Every count at once:
**`bits[i] = bits[i & (i-1)] + 1`**, valid because `i & (i-1) < i`. Hamming distance = set bits of `a ^ b`,
because **XOR is "different"**.

**A subset IS a number.** `for mask in range(1 << n)` lists all `2^n` subsets; `mask >> i & 1` tests item `i`;
`n × 2^n` is why bitmask problems stop at **n = 20**. Walk sparse masks with isolate-then-clear. Every submask:
**`sub = (sub - 1) & mask`, append-then-break-on-zero** — `3^n`, not `4^n`, and testing at the top skips the
empty submask.
