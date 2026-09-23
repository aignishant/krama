---
day: 171
track: dsa
title: "Binary, bits, and why they matter"
phase: "Bits and maths"
status: written
---

# Binary, bits, and why they matter

## 1. What this is, and why they ask it

**Binary is how numbers actually are inside a machine.** Not a representation of them — **the thing itself.**
Every number, every character, every colour, every instruction is a run of on-and-off switches.

**A bit is one switch: zero or one.** Eight of them make a **byte**. That is the entire vocabulary, and
everything else in this phase is built from it.

They ask it because **bit questions are common, short, and completely unbluffable.** "Count the set bits."
"Is this a power of two?" "Find the one number that appears once." **You either know what `n & (n - 1)` does
or you do not**, and there is no way to talk around it.

**And because it explains things you have already used.** Why `Set` lookups are fast. Why a bitmask can stand
in for a subset — the trick from bitmask DP. Why hash tables use `& (size - 1)` instead of `% size`. **Those
were all bits, and you have been using them without seeing the machinery.**

**There is also an honest reason it is worth a day.** Bit manipulation is where beginners freeze in interviews
— **not because it is hard, but because it is unfamiliar** and the notation looks like line noise. `x ^= 1 <<
i` is three ideas in eight characters. **Once you can read it slowly and correctly, the freezing stops.**

By the end of this lesson you can convert both ways by hand, read a bit pattern without panic, use all six
operators and say what each does in one sentence, explain what shifting really means, handle negative numbers,
and know the three tricks that come up again and again.

---

## 2. The story

The weights lived in a wooden box under Nagappa's counter, and there were six of them.

The boy who swept the shop had counted them a hundred times without ever thinking about it. A very small one.
One about twice that. Then bigger, then bigger, then bigger, then one so heavy he needed both hands to lift
out.

**What he could not work out was how six were enough.**

Because people came in and asked for all sorts. Eleven of this. Thirty-seven of that. And Nagappa never once
said he could not do it. He would reach into the box, put two or three on one side, tip the grain in on the
other, and the arms would come level, and that was that.

One slow afternoon the boy asked him how he knew which ones to take.

Nagappa said it like it was nothing. **"Take the biggest one that is not too heavy. Put it on. Now you need
less than you did. Take the biggest one that is not too heavy for what is left. Keep going."**

The boy tried it with thirty-seven, and it worked, and then he noticed the thing that actually surprised him.

**He had never once needed the same weight twice.**

He asked about that too.

Nagappa laughed at him. **"Of course not. Two of any one of them is the next one up. If you ever wanted two,
you would have taken the bigger one instead."**

The boy went and sat on the step and worked his way through every amount from one up to sixty-three, and there
was not one he could not make. **And not one he could make in two different ways.**

**Six weights. Sixty-three amounts. Each one either out on the scale or still in the box, and nothing in
between.**

Years afterwards somebody asked him how he had kept all of it in his head.

He said it was not much to keep.

**"You are not remembering the amount," he said. "You are remembering which ones are out of the box."**

---

## 3. The idea in plain English

**Nagappa's weights are binary.** Each weight is a **bit**. Out on the scale is `1`, still in the box is `0`.
And the reason six weights cover everything up to sixty-three, exactly once each, **is the reason binary
works.**

### Place value

**You already know place value in base ten.** In `1101`, the digits mean thousands, hundreds, tens, ones —
**each place is ten times the one on its right.**

**Binary is the same idea with two instead of ten.** Each place is **twice** the one on its right, and each
digit is only ever `0` or `1`.

```
   the number 13, in base ten

     1     3
     |     |
    tens  ones
    10    1
    = 10 + 3 = 13


   the number 13, in binary

     1     1     0     1
     |     |     |     |
     8     4     2     1
    = 8  +  4  +  0  +  1 = 13

   So 13 is 1101.

   Those are Nagappa's weights: the 8, the 4 and the 1 out
   on the scale; the 2 still in the box.
```

**Nagappa's rule — "take the biggest one that is not too heavy" — is exactly how you convert by hand**, and it
is worth doing that way once because it makes binary feel like counting rather than magic.

### Converting, both directions

**Decimal to binary, the reliable way: divide by two repeatedly and keep the remainders.**

```
   13 / 2 = 6 remainder 1     <- the LAST bit
    6 / 2 = 3 remainder 0
    3 / 2 = 1 remainder 1
    1 / 2 = 0 remainder 1     <- the FIRST bit

   READ THE REMAINDERS UPWARDS: 1101

   Reading them downwards gives 1011, which is 11.
   This is the single most common conversion mistake, and it
   is why the direction is worth saying out loud every time.
```

**Binary to decimal, the reliable way: left to right, double what you have and add the next bit.**

```
   1101

   start with 0
   see 1:  0 x 2 + 1 = 1
   see 1:  1 x 2 + 1 = 3
   see 0:  3 x 2 + 0 = 6
   see 1:  6 x 2 + 1 = 13

   No powers to remember, no place values to line up.
   One rule, applied four times.
```

### The powers of two, which you should know cold

```
   2^0  = 1          2^8  = 256
   2^1  = 2          2^10 = 1,024            ~ a thousand
   2^2  = 4          2^16 = 65,536
   2^3  = 8          2^20 = 1,048,576        ~ a million
   2^4  = 16         2^30 = 1,073,741,824    ~ a billion
   2^5  = 32         2^32 = 4,294,967,296    ~ 4 billion
   2^6  = 64         2^64 ~ 1.8 x 10^19
   2^7  = 128

   2^10 ~ a thousand, 2^20 ~ a million, 2^30 ~ a billion.
   Those three cover almost every estimate you will make.
```

**And note what `n` bits gives you: `2^n` different values, from `0` to `2^n - 1`.** Six weights, sixty-three
amounts — **because `2^6 - 1 = 63`.** Nagappa's box was a six-bit number.

### The six operators

**Every one of them works on the bits independently, place by place.**

```
   a = 12 = 1100
   b = 10 = 1010

   a & b   AND     1 only where BOTH are 1     1000  =  8
   a | b   OR      1 where EITHER is 1         1110  = 14
   a ^ b   XOR     1 where EXACTLY ONE is 1    0110  =  6
   ~a      NOT     flip every bit              (see below)
   a << 1  SHIFT LEFT   everything moves left  11000 = 24
   a >> 1  SHIFT RIGHT  everything moves right  0110 =  6
```

**Say each one as a sentence and you will not confuse them.** AND is **both**. OR is **either**. XOR is
**exactly one** — which is the same as **"different"**, and that is the property the whole of the next XOR day
rests on.

### What shifting really means

**Shifting left by one doubles. Shifting right by one halves, rounding down.**

**And it is worth seeing why, rather than memorising it.** In base ten, moving every digit one place left
multiplies by ten, because each place is ten times its neighbour. **In binary each place is twice its
neighbour, so moving left multiplies by two.** It is the same fact.

```
   1 << 0 =  1    000001
   1 << 1 =  2    000010
   1 << 2 =  4    000100
   1 << 3 =  8    001000
   1 << 4 = 16    010000
   1 << 5 = 32    100000

   1 << k IS 2^k. This is how you build a mask with a single
   bit set, and it appears in almost every bit problem.
```

**Right shift throws away what falls off the end**, which is why it is division rounded *down*: `7 >> 1` is
`3`, not `3.5`.

### The four edits

**Reading and changing one bit are four one-liners, and they are worth knowing by heart.**

```
   GET     (n >> position) & 1        shift it to the bottom, mask
   SET     n | (1 << position)        OR forces a 1
   CLEAR   n & ~(1 << position)       AND with all-1s-except-there
   TOGGLE  n ^ (1 << position)        XOR flips
```

**Each one builds `1 << position` — a mask with exactly one bit set — and then applies the operator whose
sentence matches what you want.** OR forces on. AND with a hole forces off. XOR flips. **That is not four
things to memorise; it is one thing and three sentences.**

### Negative numbers, and two's complement

**A fixed-width machine has no minus sign — only bits.** So negatives are stored using **two's complement**:
**flip every bit and add one.**

```
   in 8 bits

     5  = 00000101
   flip = 11111010
   add 1= 11111011  = -5

   check: 5 + (-5) should be 0
     00000101
   + 11111011
   -----------
    100000000     the ninth bit falls off the end
   = 00000000     = 0. Correct.
```

**Two properties follow, and both matter.** **The top bit is the sign** — `1` means negative. And **addition
just works**: the same circuit adds positives and negatives, which is the entire reason this scheme was
chosen over anything more obvious.

**Python does something different and it catches people.** Python integers are **arbitrary width** — there is
no top bit, because there is no top. So `~5` is **not** an eight-bit pattern; it is `-6`.

```
   ~x == -x - 1        always, in Python

   ~5  = -6
   ~0  = -1
   ~-1 =  0

   To get the fixed-width pattern you must MASK:
     ~5 & 0xFF = 250 = 11111010
```

**And `1 << 64` in Python is a perfectly good number**, where in C or Java it would overflow. **This makes
Python friendly to learn on and slightly misleading**, so when a problem says "32-bit integer", **mask with
`& 0xFFFFFFFF` and say that you are doing so.**

### The three tricks worth knowing today

**`n & (n - 1)` clears the lowest set bit.**

```
   n     = 10110000
   n - 1 = 10101111     borrowing flips the lowest 1 and
                        everything below it
   n & (n-1)= 10100000  <- the lowest 1 is gone
```

**Two things fall straight out.** **Counting set bits in one iteration per *set* bit** rather than one per
bit — thirty-two iterations become one, for a number like `1024`. And **`n & (n - 1) == 0` tests for a power
of two**, because a power of two has exactly one set bit, so clearing it leaves zero.

**`n & -n` isolates the lowest set bit** — the same fact wearing the other hat, and the thing a Fenwick tree
is built on.

**`x & (size - 1)` is `x % size` when `size` is a power of two.** This is why hash tables and buffers use
power-of-two sizes: **a mask is one instruction and a division is roughly twenty.**

### Where you have already met bits

```
   BITMASK DP           a subset of n items as an n-bit number —
                        exactly Nagappa's box
   HASH TABLES          & (capacity - 1) instead of % capacity
   PERMISSIONS          read/write/execute as three bits: 7 = rwx
   COLOURS              #FF8800 is three bytes: red, green, blue
   NETWORK MASKS        /24 means "the top 24 bits identify the network"
   FLAGS                one integer carrying 32 independent yes/no answers
```

**All of them are Nagappa's answer: you are not remembering the amount, you are remembering which ones are out
of the box.**

---

## 4. The picture

Place value, side by side:

```
   BASE TEN                    BASE TWO

   1  3                        1  1  0  1
   |  |                        |  |  |  |
   10 1                        8  4  2  1
                               ^  ^  ^  ^
   each place is 10x           each place is 2x
   the one on its right        the one on its right

   = 10 + 3 = 13               = 8 + 4 + 0 + 1 = 13

   SAME IDEA. Only the multiplier changed.
```

Nagappa's box, drawn:

```
                32   16    8    4    2    1
   thirty-seven [X]  [ ]  [ ]  [X]  [ ]  [X]   = 32 + 4 + 1 = 37
                                                 100101

   thirteen     [ ]  [ ]  [X]  [X]  [ ]  [X]   = 8 + 4 + 1 = 13
                                                 001101

   sixty-three  [X]  [X]  [X]  [X]  [X]  [X]   = everything out
                                                 111111

   zero         [ ]  [ ]  [ ]  [ ]  [ ]  [ ]   = nothing out
                                                 000000

   SIX weights, 2^6 = 64 arrangements, covering 0 to 63.
   Each amount ONE way only — because two of any weight is
   the next one up, so you would have taken that instead.
```

The three operators, bit by bit:

```
        a = 1 1 0 0   (12)
        b = 1 0 1 0   (10)
            -------
   a & b  = 1 0 0 0   ( 8)   BOTH
   a | b  = 1 1 1 0   (14)   EITHER
   a ^ b  = 0 1 1 0   ( 6)   EXACTLY ONE  (= "different")

   Read each column on its own. Nothing carries, nothing
   borrows — that is what makes these fast and what makes
   them easy to reason about.
```

Shifting:

```
   12 << 1

     1 1 0 0        everything moves one place LEFT
     |/|/|/|        a 0 comes in at the right
     v v v v
   1 1 0 0 0   = 24    DOUBLED


   12 >> 1

     1 1 0 0        everything moves one place RIGHT
      \|\|\|        the rightmost bit FALLS OFF
       v v v
     0 1 1 0   =  6    HALVED


   7 >> 1

     0 1 1 1
        \|\|
      0 0 1 1   =  3    not 3.5 — the 1 that fell off is GONE

   Right shift is division ROUNDED DOWN, and the rounding is
   simply the bit you dropped.
```

`n & (n - 1)`, the trick worth the day:

```
   n     = 1 0 1 1 0 0 0 0    (176)
   n - 1 = 1 0 1 0 1 1 1 1    borrowing flips the lowest 1
                              and turns everything below it to 1
           -----------------
   n&(n-1)= 1 0 1 0 0 0 0 0    (160)   the lowest 1 is GONE


   Keep going until zero, counting:

     10110000  = 176
     10100000  = 160
     10000000  = 128
     00000000  =   0

   THREE steps -> three set bits.

   The naive loop would take EIGHT steps here, and
   thirty-two on a 32-bit number, every time, regardless.

   And n & (n-1) == 0 means "exactly one bit was set"
   -> a POWER OF TWO.
```

Two's complement:

```
   8 bits, so 256 patterns. Split them down the middle:

   00000000  =    0
   00000001  =    1
      ...
   01111111  =  127        top bit 0 -> POSITIVE
   ---------------------
   10000000  = -128        top bit 1 -> NEGATIVE
   10000001  = -127
      ...
   11111111  =   -1

   TO NEGATE: flip every bit, add one.
     5     00000101
     flip  11111010
     +1    11111011  = -5

   WHY THIS SCHEME: addition needs no special case.
     00000101 + 11111011 = 100000000
     the ninth bit falls off -> 0. Correct, with an
     ordinary adder.

   PYTHON HAS NO TOP BIT — integers are arbitrary width.
     ~5 is -6, not 11111010.
     ~5 & 0xFF is 250, which IS 11111010.
   When a problem says "32-bit", mask, and say you are masking.
```

---

## 5. The code, built step by step

### Converting, by hand

```python
def to_binary(number: int, width: int = 8) -> str:
    """Repeated division by two. The remainders, read UPWARDS, are the answer."""
    if number == 0:
        return "0".rjust(width, "0")
    bits = ""
    while number > 0:
        bits = str(number % 2) + bits      # newest remainder goes on the LEFT
        number //= 2
    return bits.rjust(width, "0")
```

**`str(number % 2) + bits` — prepending, not appending — is the whole correctness of this function.** The
remainders come out in reverse order, **so each new one belongs at the front.** Appending gives `1011` for
`13`, which is `11`, **and is the single most common mistake in this conversion.**

```python
def from_binary(bits: str) -> int:
    """Left to right: double what you have, then add the next bit."""
    value = 0
    for bit in bits:
        value = value * 2 + int(bit)
    return value
```

**No powers, no place values, no indexing from the right.** One rule applied once per character — **and it is
much harder to get wrong under pressure than `sum(int(b) * 2**i ...)`.**

### The four edits

```python
def get_bit(number: int, position: int) -> int:
    return (number >> position) & 1

def set_bit(number: int, position: int) -> int:
    return number | (1 << position)

def clear_bit(number: int, position: int) -> int:
    return number & ~(1 << position)

def toggle_bit(number: int, position: int) -> int:
    return number ^ (1 << position)
```

**Every one of them builds `1 << position` — a mask with exactly one bit set — then applies the operator whose
sentence matches the intent.** OR forces on, AND-with-a-hole forces off, XOR flips.

**`~(1 << position)` is "all ones except there"**, and in Python that is a negative number of unbounded width
— **which is fine, because AND against a finite number only ever looks at the bits that exist.**

### Counting set bits, two ways

```python
def count_bits_loop(number: int) -> int:
    """Look at every bit. 32 iterations for a 32-bit number, always."""
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count
```

**This is the honest first answer and you should write it first.** It is correct, it is obvious, **and it does
work proportional to the position of the highest set bit** — thirty-two steps for `1 << 31`, however few bits
are actually set.

```python
def count_bits_kernighan(number: int) -> int:
    """n & (n - 1) clears the LOWEST set bit. One iteration per SET bit."""
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count
```

**One iteration per *set* bit rather than per bit.** For `1024` that is one step instead of eleven; for a
sparse 64-bit value it is the difference between two steps and sixty-four.

**Say the name — Brian Kernighan's algorithm — because interviewers recognise it**, and say what it does in
one sentence: **subtracting one flips the lowest set bit and turns everything below it to ones, so ANDing
removes exactly that bit.**

### Powers of two

```python
def is_power_of_two(number: int) -> bool:
    """A power of two has exactly one set bit, so clearing it leaves zero."""
    return number > 0 and (number & (number - 1)) == 0
```

**The `number > 0` guard is not decoration.** `0 & -1` is `0`, so **without it zero reports as a power of
two** — and negative numbers in two's complement do strange things here too.

### Two's complement, made visible

```python
def to_twos_complement(number: int, width: int = 8) -> str:
    """How a fixed-width machine stores a negative number."""
    mask = (1 << width) - 1
    return to_binary(number & mask, width)
```

**`(1 << width) - 1` is the all-ones mask** — eight ones for `width = 8`. **And this is the expression whose
precedence trap is in section 7**, so look at the brackets carefully.

**`number & mask` on a negative Python integer produces the fixed-width pattern**, because Python's negatives
behave as though they have infinitely many leading ones — **which is exactly what two's complement means.**

### The complete solution

```python
"""Day 171 — reading, writing, and manipulating bit patterns."""

from __future__ import annotations


def to_binary(number: int, width: int = 8) -> str:
    """Repeated division by two. The remainders, read UPWARDS, are the answer."""
    if number == 0:
        return "0".rjust(width, "0")
    bits = ""
    while number > 0:
        bits = str(number % 2) + bits      # newest remainder goes on the LEFT
        number //= 2
    return bits.rjust(width, "0")


def from_binary(bits: str) -> int:
    """Left to right: double what you have, then add the next bit."""
    value = 0
    for bit in bits:
        value = value * 2 + int(bit)
    return value


def get_bit(number: int, position: int) -> int:
    """Is bit `position` set? Shift it down to the bottom and mask."""
    return (number >> position) & 1


def set_bit(number: int, position: int) -> int:
    """Turn bit `position` ON. OR with a single 1 in that place."""
    return number | (1 << position)


def clear_bit(number: int, position: int) -> int:
    """Turn bit `position` OFF. AND with a mask of all 1s except there."""
    return number & ~(1 << position)


def toggle_bit(number: int, position: int) -> int:
    """Flip bit `position`. XOR is the flip operator."""
    return number ^ (1 << position)


def count_bits_loop(number: int) -> int:
    """Look at every bit. 32 iterations for a 32-bit number, always."""
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count


def count_bits_kernighan(number: int) -> int:
    """n & (n - 1) clears the LOWEST set bit. One iteration per SET bit."""
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count


def is_power_of_two(number: int) -> bool:
    """A power of two has exactly one set bit, so clearing it leaves zero."""
    return number > 0 and (number & (number - 1)) == 0


def to_twos_complement(number: int, width: int = 8) -> str:
    """How a fixed-width machine stores a negative number."""
    mask = (1 << width) - 1
    return to_binary(number & mask, width)


if __name__ == "__main__":
    print("PLACE VALUE — 13 in binary")
    print(f"  to_binary(13, 4)   = {to_binary(13, 4)}   (8 + 4 + 0 + 1)")
    print(f"  from_binary('1101') = {from_binary('1101')}")
    print(f"  Python agrees: bin(13) = {bin(13)}")

    print()
    print("THE FIVE OPERATORS on 12 (1100) and 10 (1010)")
    a, b = 12, 10
    print(f"  a     = {to_binary(a, 4)}  = {a}")
    print(f"  b     = {to_binary(b, 4)}  = {b}")
    print(f"  a & b = {to_binary(a & b, 4)}  = {a & b}   (both)")
    print(f"  a | b = {to_binary(a | b, 4)}  = {a | b}   (either)")
    print(f"  a ^ b = {to_binary(a ^ b, 4)}  = {a ^ b}   (exactly one)")
    print(f"  a << 1= {to_binary(a << 1, 5)} = {a << 1}  (doubled)")
    print(f"  a >> 1= {to_binary(a >> 1, 4)}  = {a >> 1}   (halved, rounded down)")

    print()
    print("SHIFTING IS DOUBLING")
    for k in range(6):
        print(f"  1 << {k} = {1 << k:>2}   {to_binary(1 << k, 6)}")

    print()
    print("THE FOUR EDITS on 0b1010 (10), position 2")
    n = 0b1010
    print(f"  start          {to_binary(n, 4)}  = {n}")
    print(f"  get_bit(n, 2)  = {get_bit(n, 2)}")
    print(f"  set_bit(n, 2)  {to_binary(set_bit(n, 2), 4)}  = {set_bit(n, 2)}")
    print(f"  clear_bit(n,1) {to_binary(clear_bit(n, 1), 4)}  = {clear_bit(n, 1)}")
    print(f"  toggle_bit(n,0){to_binary(toggle_bit(n, 0), 4)}  = {toggle_bit(n, 0)}")

    print()
    print("COUNTING SET BITS")
    for value in (0, 1, 7, 8, 255, 1024):
        print(f"  {value:>5}  {to_binary(value, 11)}  loop={count_bits_loop(value)}"
              f"  kernighan={count_bits_kernighan(value)}"
              f"  python={value.bit_count()}")

    print()
    print("n & (n - 1) CLEARS THE LOWEST SET BIT")
    n = 0b10110000
    while n:
        print(f"  {to_binary(n, 8)}  = {n:>3}")
        n &= n - 1
    print(f"  {to_binary(0, 8)}  =   0")

    print()
    print("POWERS OF TWO")
    for value in (1, 2, 3, 16, 63, 64):
        print(f"  {value:>3} -> {is_power_of_two(value)}")

    print()
    print("NEGATIVE NUMBERS — two's complement in 8 bits")
    for value in (5, -5, 1, -1, 127, -128):
        print(f"  {value:>5}  stored as {to_twos_complement(value)}")
    print(f"  Python's ~5 = {~5}   (that is -5-1, not an 8-bit pattern)")
    print(f"  masked to 8 bits: {to_binary(~5 & 0xFF, 8)} = {~5 & 0xFF}")

    print()
    print("VERIFICATION")
    bad = 0
    for value in range(0, 5000):
        if to_binary(value, 1) != bin(value)[2:]:
            bad += 1
        if from_binary(bin(value)[2:]) != value:
            bad += 1
        if count_bits_loop(value) != value.bit_count():
            bad += 1
        if count_bits_kernighan(value) != value.bit_count():
            bad += 1
        if is_power_of_two(value) != (value > 0 and bin(value).count("1") == 1):
            bad += 1
    print(f"  {bad} mismatches over 5,000 values, 5 checks each")
```

Running it:

```
PLACE VALUE — 13 in binary
  to_binary(13, 4)   = 1101   (8 + 4 + 0 + 1)
  from_binary('1101') = 13
  Python agrees: bin(13) = 0b1101

THE FIVE OPERATORS on 12 (1100) and 10 (1010)
  a     = 1100  = 12
  b     = 1010  = 10
  a & b = 1000  = 8   (both)
  a | b = 1110  = 14   (either)
  a ^ b = 0110  = 6   (exactly one)
  a << 1= 11000 = 24  (doubled)
  a >> 1= 0110  = 6   (halved, rounded down)

SHIFTING IS DOUBLING
  1 << 0 =  1   000001
  1 << 1 =  2   000010
  1 << 2 =  4   000100
  1 << 3 =  8   001000
  1 << 4 = 16   010000
  1 << 5 = 32   100000

THE FOUR EDITS on 0b1010 (10), position 2
  start          1010  = 10
  get_bit(n, 2)  = 0
  set_bit(n, 2)  1110  = 14
  clear_bit(n,1) 1000  = 8
  toggle_bit(n,0)1011  = 11

COUNTING SET BITS
      0  00000000000  loop=0  kernighan=0  python=0
      1  00000000001  loop=1  kernighan=1  python=1
      7  00000000111  loop=3  kernighan=3  python=3
      8  00000001000  loop=1  kernighan=1  python=1
    255  00011111111  loop=8  kernighan=8  python=8
   1024  10000000000  loop=1  kernighan=1  python=1

n & (n - 1) CLEARS THE LOWEST SET BIT
  10110000  = 176
  10100000  = 160
  10000000  = 128
  00000000  =   0

POWERS OF TWO
    1 -> True
    2 -> True
    3 -> False
   16 -> True
   63 -> False
   64 -> True

NEGATIVE NUMBERS — two's complement in 8 bits
      5  stored as 00000101
     -5  stored as 11111011
      1  stored as 00000001
     -1  stored as 11111111
    127  stored as 01111111
   -128  stored as 10000000
  Python's ~5 = -6   (that is -5-1, not an 8-bit pattern)
  masked to 8 bits: 11111010 = 250

VERIFICATION
  0 mismatches over 5,000 values, 5 checks each
```

**Look at the `255` line: the naive loop takes eight steps and Kernighan also takes eight**, because every bit
is set. **And on `1024` the loop takes eleven and Kernighan takes one.** That contrast is the whole argument
for the trick, and it is worth having both numbers to hand.

**In an interview you would use `n.bit_count()`** (Python 3.10 and later), and say so — **but write Kernighan
first**, because the question is almost never really about counting.

---

## 6. What it costs

**Converting.**

```
to_binary(n): one division per bit
  13   -> 4 divisions
  1000 -> 10 divisions
  10^9 -> 30 divisions

-> O(log n) in the VALUE of n, or O(b) in its bit-length.

This is the distinction that matters and interviewers probe it:
a loop over the BITS of n is logarithmic in n, not linear.
```

**Counting set bits — count the iterations out loud.**

```
NAIVE LOOP: one iteration per bit position, up to the highest set bit

  1024 = 10000000000
  -> 11 iterations, to find ONE set bit

  1 << 31
  -> 32 iterations, to find ONE set bit


KERNIGHAN: one iteration per SET bit

  1024 -> 1 iteration
  255  -> 8 iterations       (every bit set — no better)
  176  -> 3 iterations

  1 << 31 -> 1 iteration


-> naive is O(b), where b is the bit-length: 32 or 64
-> Kernighan is O(s), where s is the number of set bits

WORST CASE THEY ARE THE SAME (all bits set).
TYPICALLY Kernighan is far fewer, and on sparse values
it is 1 against 64.
```

**And the honest framing: both are constant time on fixed-width integers**, because thirty-two is a constant.
**Say that** — it is the more accurate statement, and then say that the constant still matters when you are
doing it in a loop over a million values.

**The bitmask-DP connection, since the arithmetic is the same.**

```
a subset of n items as an n-bit number:

  n = 20  ->  2^20 = 1,048,576 subsets        fine
  n = 25  ->  2^25 = 33,554,432               getting slow
  n = 30  ->  2^30 = 1,073,741,824            no
  n = 64  ->  2^64 = 18,446,744,073,709,551,616

-> which is why bitmask solutions cap around n = 20,
   and why "n <= 20" in a problem statement is a hint

That is Nagappa's box again: six weights, 2^6 arrangements.
Twenty items, 2^20.
```

**Space.**

```
every function here uses O(1) extra space

except to_binary, which builds a string:
  O(b) characters, so ~32 or ~64 bytes

Note that string CONCATENATION in a loop is O(b^2) work in
total, because each `+` copies. For 64 bits that is 2,048
character copies — irrelevant here, and worth knowing about
before you write the same loop over a million-character
string.
```

**Why powers of two are everywhere.**

```
x % size      ~ 20-40 CPU cycles   (integer division is slow)
x & (size-1)  ~ 1 CPU cycle        (when size is a power of two)

-> a 20-40x difference on an operation a hash table does on
   EVERY lookup

-> which is why hash tables, ring buffers and memory pages
   all have power-of-two sizes. It is not aesthetics.
```

---

## 7. The traps

**Reading the remainders downwards.**

```
13 / 2 = 6 r 1
 6 / 2 = 3 r 0
 3 / 2 = 1 r 1
 1 / 2 = 0 r 1

upwards:   1101  = 13   <- correct
downwards: 1011  = 11   <- wrong, and a perfectly plausible number
```

**Nothing errors.** You get a valid binary string for a different number. **Say the direction out loud every
time you do this by hand** — it is the one step of the conversion that has no self-check.

**The shift-precedence trap, which is the real one in Python.**

```python
n = 4
mask = 1 << n - 1        # meant to be "all ones in n bits"
```

```
1 << n - 1   = 8
(1 << n) - 1 = 15
```

**Subtraction binds tighter than shifting**, so `1 << n - 1` is `1 << (n - 1)`, **which is a single bit rather
than a full mask.** No error, a plausible number, and every downstream result is quietly wrong.

**Always bracket shifts.** `(1 << n) - 1`. It costs two characters.

**Assuming C's precedence rule.** In C, `x & 1 == 0` parses as `x & (1 == 0)` and is a famous bug. **In Python
`&` binds *tighter* than `==`**, so `x & 1 == 0` does mean `(x & 1) == 0` and works. **Know that this differs
between languages**, and bracket it anyway so the reader does not have to.

**`~` in Python is not the fixed-width complement.**

```
~5  = -6
~0  = -1
```

**Python integers have no top bit, so `~x` is always `-x - 1`.** If you want the eight-bit pattern you must
mask:

```
~5 & 0xFF = 250 = 11111010
```

**This bites hardest on LeetCode problems that say "32-bit signed integer".** The fix is `& 0xFFFFFFFF`, and
converting back to a signed value if the top bit is set — **and saying out loud that you are doing it, because
otherwise it looks like magic.**

**Right-shifting a negative number does not do what people expect.**

```
-8 >> 1 = -4
-7 >> 1 = -4      not -3
-1 >> 5 = -1      it never reaches zero
```

**Python's `>>` is an *arithmetic* shift: it copies the sign bit in from the left.** So **`while number:
number >>= 1` never terminates on a negative input** — the value stays `-1` forever. **A counting loop written
without a guard hangs rather than crashing**, which is the worst failure mode there is.

**Shifting by a negative amount.**

```python
1 << -1
```

```
Traceback (most recent call last):
  File "<stdin>", line 8, in <lambda>
ValueError: negative shift count
```

**Loud and clear, which puts it in the good category.**

**Shifting by a float.**

```python
1 << 2.0
```

```
Traceback (most recent call last):
  File "<stdin>", line 9, in <lambda>
TypeError: unsupported operand type(s) for <<: 'int' and 'float'
```

**This is the one that catches you after a division.** `n / 2` gives a float in Python 3; `n // 2` gives an
integer. **Use `//` anywhere near bit work.**

**Bitwise operators on floats at all.**

```python
1.5 & 1
```

```
Traceback (most recent call last):
  File "<stdin>", line 12, in <lambda>
TypeError: unsupported operand type(s) for &: 'float' and 'int'
```

**Forgetting the base in `int()`.**

```
int('1101')    = 1101       <- a thousand one hundred and one
int('1101', 2) = 13         <- correct
```

**No error, and the wrong number is a thousand times too big.** **`int(s, 2)` — the second argument is not
optional when you mean binary.**

**`bin()` on a negative number.**

```
bin(-5) = '-0b101'
```

**A minus sign and the magnitude — not two's complement.** Slicing off the first two characters with `[2:]`
gives `'b101'`, **which then fails or produces nonsense.** Use `bin(x & 0xFF)[2:]` when you want a pattern.

**Zero reporting as a power of two.** Without the `number > 0` guard, `is_power_of_two(0)` is `True`, because
`0 & -1 == 0`. **One comparison, and the test cases that catch it are `0` and negative inputs — both of which
people forget to try.**

---

## 8. In the interview

### How it gets asked

- *"What is 13 in binary?"* — the warm-up, and it is testing whether you can do it calmly.
- *"What does shifting left by one do?"* — and **why**.
- *"Count the number of set bits."* — then "can you do better?"
- *"Is this a power of two?"* — a one-liner if you know it.
- *"How are negative numbers stored?"* — two's complement.
- *"Why do hash tables use power-of-two sizes?"* — the mask against the division.

### The first ninety seconds

On "what is 13 in binary, and what does shifting do":

> "**Thirteen is 1101.**
>
> **I would get there by place value.** In binary each place is twice the one to its right, so the places are
> 8, 4, 2, 1. **Thirteen is 8 plus 4 plus 1** — so ones in the 8, 4 and 1 places, and a zero in the 2 place.
> **1101.**
>
> **The mechanical way, if the number is bigger, is repeated division by two, keeping the remainders.**
> Thirteen over two is six remainder one; six over two is three remainder nought; three over two is one
> remainder one; one over two is nought remainder one. **And you read the remainders upwards — 1101.**
>
> **Upwards, not downwards, and I say that out loud every time** — reading them downwards gives 1011, which is
> eleven, **and it is a completely plausible-looking wrong answer with no self-check.**
>
> **Shifting left by one doubles. Shifting right by one halves, rounded down.**
>
> **And the reason is the same fact as place value.** In base ten, moving every digit one place left multiplies
> by ten, because each place is ten times its neighbour. **In binary each place is twice its neighbour, so
> moving left multiplies by two.**
>
> **`1 << k` is `2^k`** — that is how you build a mask with one bit set, and it is in essentially every bit
> problem.
>
> **The rounding down in right-shift is just the bit that fell off the end.** `7 >> 1` is 3, not 3.5 — **the
> one you dropped was the half.**
>
> **One caveat about Python I would mention: integers are arbitrary width**, so `1 << 64` is a perfectly good
> number here where in C or Java it would overflow. **If the problem says thirty-two bits, I would mask with
> `& 0xFFFFFFFF` and say that I am doing it.**"

### The follow-ups

**"Count the set bits. Now do it faster."**

> "**The obvious version looks at every bit**: mask the bottom one, add it, shift right, repeat until zero.
> **I would write that first**, because it is correct and clear.
>
> **Its cost is one iteration per bit position, up to the highest set bit** — so **thirty-two iterations to
> find one set bit in `1 << 31`.** The work depends on where the highest bit is, **not on how many bits are
> set**, and that is the inefficiency.
>
> **The faster version is `n &= n - 1` in a loop, counting iterations. That is Brian Kernighan's algorithm.**
>
> **Here is why it works.** Subtracting one **flips the lowest set bit to zero and turns everything below it
> into ones** — that is what borrowing does. **So ANDing the original with it clears exactly the lowest set
> bit and leaves everything above untouched.**
>
> **So you get one iteration per *set* bit.** For `1024` that is one step instead of eleven. For `1 << 31`,
> one instead of thirty-two.
>
> **I would be honest about the worst case: if every bit is set they are identical.** `255` takes eight steps
> either way. **The gain is on sparse values, which is most real data.**
>
> **And strictly both are constant time on fixed-width integers**, since thirty-two is a constant — **but the
> constant matters when you are doing this inside a loop over a million values.**
>
> **The same identity gives you a power-of-two test for free.** A power of two has exactly one set bit, **so
> clearing it must leave zero**: `n > 0 and (n & (n - 1)) == 0`. **The `n > 0` is not decoration** — without
> it, zero reports as a power of two.
>
> **In production I would write `n.bit_count()`** — Python 3.10 and later, and it compiles to a single CPU
> instruction. **I would say that, and then write Kernighan anyway, because the question is not really about
> counting.**"

**"How are negative numbers stored?"**

> "**Two's complement: flip every bit and add one.**
>
> **In eight bits, five is 00000101.** Flip it: 11111010. Add one: **11111011, which is minus five.**
>
> **The check is that they must add to zero.** 00000101 plus 11111011 is 100000000 — **nine bits, and the top
> one falls off the end**, leaving 00000000. **Zero. Correct.**
>
> **And that falling-off is the entire reason this scheme won**, over anything more obvious like a sign bit.
> **The same adder circuit handles positives and negatives with no special case.** Sign-and-magnitude would
> need the hardware to check signs and branch, **and it also gives you two different zeros**, which causes
> problems everywhere.
>
> **Two consequences worth knowing.** **The top bit is the sign** — one means negative. **And the range is
> asymmetric**: eight bits gives minus 128 to plus 127, **because zero takes up one of the positive slots.**
> That asymmetry is why `abs(-2**31)` overflows a 32-bit integer, which is a real bug people hit.
>
> **Python is the exception and it catches people.** Python integers are **arbitrary width**, so there is no
> top bit at all. **`~5` is minus six, not an eight-bit pattern** — the rule is `~x == -x - 1`.
>
> **To get the fixed-width pattern you mask: `~5 & 0xFF` is 250, which is 11111010.**
>
> **And there is a related trap: Python's right shift is arithmetic — it copies the sign bit in from the
> left.** So `-1 >> 5` is still minus one, **and a `while number: number >>= 1` loop never terminates on a
> negative input.** It hangs rather than crashing, **which is the worst way for a bug to behave**, so I would
> guard or mask before any bit loop that might see a negative."

**"Why do hash tables use power-of-two sizes?"**

> "**Because `x % size` becomes `x & (size - 1)` when the size is a power of two, and that is a twenty- to
> forty-fold speedup on an operation the table does on every single lookup.**
>
> **The reason it works is place value.** In a power-of-two size, **the remainder is exactly the low bits** —
> the higher bits are all multiples of the size and contribute nothing to the remainder. **So masking off
> everything above them gives the same answer as dividing.**
>
> **Concretely: `size = 16` means `size - 1` is 15, which is 1111.** ANDing with 1111 keeps the bottom four
> bits, **and the bottom four bits of any number are precisely that number modulo 16.**
>
> **The cost difference is real.** Integer division is roughly twenty to forty CPU cycles; **a bitwise AND is
> one.** For an operation on the hot path of every lookup, that is not a micro-optimisation.
>
> **It is the same reason ring buffers and memory pages are powers of two.** Wrapping an offset is a mask, not
> a division.
>
> **And there is a cost, which is worth naming.** Masking **only looks at the low bits**, so if the hash
> function produces values whose low bits are poorly distributed — object addresses, or sequential ids
> multiplied by something — **every key lands in a few buckets.** Modulo by a prime is more forgiving of a bad
> hash.
>
> **Which is why Java's HashMap mixes the high bits down into the low ones before masking**: `h ^ (h >>> 16)`.
> **It buys the speed of the mask and pays for it with one extra XOR to protect against a weak hash.** That
> trade is the actual answer to the question."

### The model answer

*"Explain binary to me as though I have never seen it, then tell me why it matters."*

> "**Binary is place value with two instead of ten.**
>
> **In base ten, the places are 1, 10, 100 — each one ten times the last, and each digit runs 0 to 9.** In
> binary the places are **1, 2, 4, 8, 16** — each one twice the last — **and each digit is only ever 0 or 1.**
>
> **So 1101 means 8 plus 4 plus 0 plus 1, which is 13.**
>
> **The reason it is two and not ten is physical.** A wire is either carrying current or it is not. **Two
> states are easy to build reliably and ten are not**, so everything above is built on the two.
>
> **A bit is one of those switches. Eight bits is a byte.** And **n bits gives 2^n different values, from 0 to
> 2^n − 1** — which is why eight bits covers 0 to 255, and why you see 255 everywhere.
>
> **Converting is two rules.** Going in: **divide by two repeatedly and read the remainders upwards.** Coming
> out: **left to right, double what you have and add the next bit.** I say 'upwards' out loud every time,
> because reading them downwards gives a plausible wrong number with no self-check.
>
> **There are six operators and each is one sentence.** **AND is both. OR is either. XOR is exactly one —
> which is the same as 'different', and that is the property the whole XOR family of problems rests on.** NOT
> flips everything. **Left shift doubles, right shift halves rounding down** — and that is the same place-value
> fact, because moving left multiplies by whatever each place is worth.
>
> **Negative numbers are two's complement: flip and add one.** The point of it is that **addition then needs no
> special case** — the same circuit handles both signs, and the carry that falls off the end does the work.
>
> **Why it matters, in three places I have already used it.**
>
> **A subset of twenty items is a twenty-bit number** — that is what bitmask DP is, and it is why those
> problems cap around twenty, because 2^20 is a million and 2^30 is a billion.
>
> **Hash tables use power-of-two sizes so that modulo becomes a mask** — `x & (size - 1)` — which is one CPU
> cycle instead of twenty to forty, on an operation done at every lookup.
>
> **And `n & (n - 1)` clears the lowest set bit**, which gives you set-bit counting in one step per set bit
> and a power-of-two test as a one-liner.
>
> **The thing I would want to leave you with is the shift in view.** A number is not a quantity that happens to
> be stored somehow. **It is a pattern of switches, and the operators let you work on the pattern directly
> rather than through arithmetic.** Once that lands, these problems stop looking like tricks."

---

## 9. Recall card

**Binary is place value with two instead of ten**: the places are 1, 2, 4, 8, 16, each twice the last, each
digit 0 or 1. **13 = 8 + 4 + 1 = 1101.** **n bits gives 2^n values, 0 to 2^n − 1.** Know `2^10 ≈ a thousand,
2^20 ≈ a million, 2^30 ≈ a billion`.

**Converting, two rules.** In: **divide by two, read the remainders UPWARDS** (downwards gives 1011 = 11, a
plausible wrong answer with no self-check). Out: **left to right, double and add the next bit.**

**Six operators, one sentence each.** AND = **both**. OR = **either**. XOR = **exactly one**, which is the same
as **different**. NOT flips. **`<< 1` doubles, `>> 1` halves rounding down** — the same place-value fact, and
the rounding is just the bit that fell off. **`1 << k` is `2^k`, the single-bit mask.**

**The four edits, all built from `1 << position`:** GET `(n >> p) & 1`; SET `n | (1 << p)`; CLEAR
`n & ~(1 << p)`; TOGGLE `n ^ (1 << p)`.

**Three tricks.** **`n & (n - 1)` clears the lowest set bit** — subtracting one flips it and ones-fills below,
so ANDing removes exactly it. That gives **Kernighan's count** (one step per SET bit: 1 instead of 32 for
`1 << 31`, but no better when all bits are set) and **`n > 0 and (n & (n-1)) == 0`** for powers of two — **the
guard is not decoration, or zero passes.** **`x & (size - 1)` is `x % size` for power-of-two sizes**: one CPU
cycle against twenty to forty, which is why hash tables and ring buffers are sized that way.

**Negatives are two's complement — flip and add one — so one adder handles both signs and the carry falls off
the end.** The range is asymmetric (−128 to 127). **Python is arbitrary-width, so `~x == -x - 1`, not a
pattern — mask with `& 0xFF` or `& 0xFFFFFFFF`.** And **`>>` is arithmetic: `-1 >> 5` is still −1, so a
`while n: n >>= 1` loop HANGS on a negative.** **Always bracket shifts — `1 << n - 1` is `1 << (n-1)`, not
`(1 << n) - 1`.**
