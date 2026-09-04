---
day: 2
track: cpp
title: "Types, numbers, and the overflow that costs contests"
phase: "C++ and competitive programming"
status: written
---

# Day 002 · C++ — Types, numbers, and the overflow that costs contests

**After today you can:** You can choose int or long long correctly, and spot the multiplication that will overflow before you run it.

**The interviewer asks it as:** *What is the range of an int, and what happens when you go past it?*

---

> Second of the ten C++ days. Yesterday you got a compiler working. Today you learn the one
> bug that will cost you more contest points than every other mistake combined.

---

## 1. What this is, and why they ask it

In Python, a whole number has no maximum. You can multiply two twenty-digit numbers and get a
forty-digit answer, and Python grows the number to fit.

C++ does not do this. In C++ every number lives in a box of a fixed size, decided when you
compile, and it cannot hold a value bigger than that box. An `int` is a box thirty-two bits
wide, and the largest number it can hold is 2,147,483,647. Ask it to hold 3,000,000,000 and you
do not get an error, an exception, or a warning while it runs. You get a wrong number and a
program that carries on cheerfully.

This is the single most expensive bug in competitive programming. It is not a hard concept. It
is not subtle. It costs more points than every mistake about method combined, because it
produces a wrong answer on test 14 of 60 with no clue as to why.

Interviewers ask about it because it is the fastest way to find out whether you have actually
written C++ or only read about it — and because the overflow in a binary search midpoint is a
famous bug that shipped in the Java standard library for nine years. Today's DSA lesson counts
the steps a loop takes. This counts the *values* a number can take, which is the other half of
the same honesty.

---

## 2. The story

Kaushik's father bought a Bajaj Chetak in 1994 and rode it to the same office in Pune for
twenty-six years. When he stopped riding, in 2020, he told Kaushik to sell it.

The scooter had a little window on the dial that showed the distance travelled. Five white
digits on black drums, and a sixth in a different colour for the tenths, which nobody ever
looked at. When Kaushik cleaned it up and photographed it for the listing, the window read
`03412`. Three thousand four hundred and twelve kilometres.

He put it up at a price that matched. A man came on a Sunday morning, walked around it twice,
started it, listened to it, and looked at the window for a long moment. Then he said, quite
mildly, that his uncle had owned the same model, and that the meter on it only went to `99999`.

Kaushik did not follow at first.

The man explained it the way you would explain it to a child, without being unkind about it.
There are five drums. The last one turns once for every kilometre. When it goes past nine it
comes back to zero and nudges the drum to its left. Fine. But when all five are showing nine,
and the scooter travels one more kilometre, there is no sixth drum for the leftmost one to
nudge. So all five simply come back to zero, and the scooter starts counting again from
nothing.

His father had ridden that Chetak nine kilometres each way, six days a week, for twenty-six
years. A hundred and three thousand, four hundred and twelve kilometres. The window said
`03412` because the hundred thousand had nowhere to go.

What stayed with Kaushik afterwards was not that he had nearly overcharged a stranger. It was
that the meter never gave the slightest sign. It did not stick, or flash, or make a noise, or
show a row of dashes. It rolled from `99999` to `00000` in the same smooth quarter-turn it made
every other kilometre, somewhere on the Nagar road on an ordinary Tuesday in 2011, and then
reported a confident, precise, completely wrong number for nine more years.

---

## 3. The idea in plain English

The scooter meter is a C++ number type, exactly.

### A type is a box of a fixed width

When you write `int x = 5;` in C++, you are not just saying "x is 5". You are saying "reserve a
box thirty-two **bits** wide and call it x". A **bit** is one binary digit, a 0 or a 1.
Thirty-two of them can be arranged in 2^32 ways, which is 4,294,967,296 distinct values — about
4.3 billion — and no more. Five drums give you 100,000 readings and no more. Same idea.

The width is fixed when you compile and never changes. This is a large part of why C++ is fast:
the machine knows the exact size and layout of everything before the program starts.

### The types you will actually use

| Type | Width | Range | When |
|---|---|---|---|
| `int` | 32 bits | −2,147,483,648 to **2,147,483,647** | the default for counters, positions, small values |
| `long long` | 64 bits | ±**9,223,372,036,854,775,807** | any sum or product that might exceed 2 × 10^9 |
| `unsigned int` | 32 bits | 0 to 4,294,967,295 | bit work. Otherwise avoid |
| `size_t` | 64 bits, unsigned | 0 to 1.8 × 10^19 | what `.size()` returns. Read the trap in §7 |
| `char` | 8 bits | −128 to 127 | one character, and also a small number |
| `bool` | 8 bits | `true` or `false` | conditions |
| `double` | 64 bits | ±1.8 × 10^308, ~15-16 significant digits | real numbers. Never money, never equality |
| `float` | 32 bits | ~7 significant digits | almost never. Use `double` |

Two numbers to memorise, and they are the only two:

> **`int` holds about 2 × 10^9. `long long` holds about 9 × 10^18.**

Say those out loud until they are automatic. Every overflow decision you will ever make is one
comparison against one of those two numbers.

### What happens when you go past

Here the scooter and the language part company, and the difference matters.

For **unsigned** types, C++ does exactly what the meter does: it wraps around. 4,294,967,295
plus one is 0. This is defined, guaranteed behaviour, and bit-twiddling code relies on it.

For **signed** types — `int`, `long long` — going past the maximum is **undefined behaviour**.
That phrase has a precise meaning in C++ and it is worse than "wraps around": it means the
standard imposes no requirement at all. In practice, on your machine, it usually wraps to a
large negative number, and 2,147,483,647 + 1 comes out as −2,147,483,648. But the compiler is
entitled to assume it never happens, and `-O2` does assume it. A loop written
`for (int i = 1; i > 0; i++)` can be optimised into an endless loop, because the compiler
reasons that a positive `int` plus one is always positive.

You do not need to fear that in a contest. You need to know it, because "signed overflow is
undefined behaviour, not wraparound" is a sentence that marks you as somebody who has read the
language rather than guessed at it.

### The trap is in the middle of the expression, not the end

This is the thing that actually bites, and it is not obvious.

```cpp
long long area = width * height;   // width and height are int
```

You wrote `long long` on the left. You were being careful. It does not help.

C++ works out the type of the right-hand side **first**, entirely on its own, and only then
converts it to fit the left. Both `width` and `height` are `int`, so `width * height` is
computed as an `int` multiplication, in a 32-bit box. If width is 100,000 and height is 100,000,
the true answer is 10^10, the 32-bit box overflows, and the wrong number — some value near
1.4 × 10^9 — is then faithfully widened into your 64-bit `long long`.

The fix is to make one side 64-bit **before** the multiplication:

```cpp
long long area = 1LL * width * height;      // or (long long)width * height
```

`1LL` is the number one, written as a `long long`. Multiplying by it costs nothing and forces
the whole expression into 64-bit arithmetic, because when C++ combines two different numeric
types it promotes the narrower one to the wider. This idiom — a stray `1LL *` at the front of a
product — is everywhere in competitive C++, and now you know why.

### Integer division truncates

`7 / 2` is `3`. Both sides are whole numbers, so C++ divides them as whole numbers and discards
the fraction. It **truncates towards zero**, which is not the same as rounding down:

```cpp
 7 / 2   ==  3       //  3.5 -> 3
-7 / 2   == -3       // -3.5 -> -3, NOT -4
 7 % 2   ==  1
-7 % 2   == -1       // the remainder takes the sign of the LEFT side
```

Python differs on both of the negative cases — `-7 // 2` is `-4` and `-7 % 2` is `1` — because
Python rounds down and takes the sign of the right side. If you are porting a solution from
Python, this is where it will silently change answers. The fix for a remainder you need
non-negative is `((a % m) + m) % m`.

To get a real division, make one side real: `7 / 2.0` is `3.5`.

### `double` is not a real number

A `double` stores a value in 64 bits as a sign, an exponent and a fraction, which gives about
**15 to 16 significant decimal digits**. Two consequences you must know:

**0.1 + 0.2 is not 0.3.** It is 0.30000000000000004, because 0.1 has no exact binary form,
exactly as 1/3 has no exact decimal one. So `if (a == b)` on two `double`s is almost always a
bug. Compare with a tolerance: `if (fabs(a - b) < 1e-9)`.

**Past 2^53 — about 9 × 10^15 — a `double` cannot represent every whole number.** So a `double`
is not a safe substitute for a `long long`, even though its maximum is enormously larger. It has
more range and less precision.

Never use floating point for money, for counters, or for anything where two values must compare
exactly equal.

---

## 4. The picture

What a 32-bit signed `int` actually looks like, with the sign bit called out:

```
  int, 32 bits.  The leftmost bit is the sign.

   bit  31  30 29 28 ................................. 2  1  0
       +---+--------------------------------------------------+
       | S |            31 bits of magnitude                  |
       +---+--------------------------------------------------+
         ^
         0 = positive or zero,  1 = negative

  largest positive:  0 1111111 11111111 11111111 11111111  =  2,147,483,647
  add 1:             1 0000000 00000000 00000000 00000000  = -2,147,483,648
                     ^
                     the carry landed in the sign bit
```

**What to notice:** nothing broke. No storage was exceeded, no memory was damaged. A carry
arrived in the leftmost bit, which happens to be the bit that means "negative", and the number
flipped from the largest positive value to the smallest negative one. That is the quarter-turn
on the Nagar road.

The same thing drawn as the meter, so the shape is memorable:

```
   ... 2147483645   2147483646   2147483647   -2147483648   -2147483647 ...
                                       |
                                       +-- one single addition happens here
                                           and the value drops by 4,294,967,295

   the number line is not a line.  It is a ring.

                    +2,147,483,647
                          /  \
                         /    \
                        0      | <- one step across this gap
                         \    /
                          \  /
                    -2,147,483,648
```

**What to notice:** every value is reachable from every other by adding. There is no edge and no
error, only one place on the ring where a single `+1` moves you the whole way round.

And where the trap actually lives in an expression:

```
  long long area = width * height;
                   \_____________/
                          |
                    computed FIRST, as int x int -> int
                    the box is 32 bits HERE
                          |
                          v
                    then widened to 64 bits
                    (too late; the damage is done)

  long long area = 1LL * width * height;
                   \_/
                    |
              this makes the first multiply 64-bit,
              and the result of that is 64-bit,
              so the second multiply is 64-bit too
```

**What to notice:** the type on the left of the `=` has no influence on how the right-hand side
is computed. C++ evaluates the expression on its own terms and converts afterwards.

---

## 5. The code, built step by step

### Ask the machine, do not trust the table

Never memorise limits you can print.

```cpp
#include <iostream>
#include <limits>

int main() {
    std::cout << "int max       " << std::numeric_limits<int>::max() << "\n";
    std::cout << "long long max " << std::numeric_limits<long long>::max() << "\n";
    return 0;
}
```

`std::numeric_limits<T>::max()` is the standard way to get a type's largest value. It is in
`<limits>`. There is `::min()` too, but be careful: for whole-number types `min()` is the most
negative value, while for `double` it is the smallest *positive* value — use
`std::numeric_limits<double>::lowest()` for the most negative one.

### Watch it wrap

```cpp
int big = 2147483647;      // the maximum
std::cout << big << "\n";  //  2147483647
big = big + 1;
std::cout << big << "\n";  // -2147483648
```

No exception. No message. The second line prints a negative number and the program returns 0 for
success. This is the meter rolling over, and it is why you cannot rely on noticing it.

### The multiplication that eats contests

```cpp
int n = 100000;
int wrong = n * n;                 // 32-bit multiply. Overflows.
long long still_wrong = n * n;     // ALSO overflows: the right side is still int
long long right = 1LL * n * n;     // 64-bit multiply. Correct.

std::cout << wrong       << "\n";  // 1410065408
std::cout << still_wrong << "\n";  // 1410065408
std::cout << right       << "\n";  // 10000000000
```

The middle line is the one worth staring at. It looks careful and it is wrong, and it is the
most common form of this bug in real submissions.

### The sum that overflows even when every value is small

```cpp
std::vector<int> a(100000, 100000);   // 100,000 values, each 100,000

int bad = 0;
for (int x : a) bad += x;             // overflows after ~21,475 of them

long long good = 0;
for (int x : a) good += x;            // fine: += widens x to long long
```

Each value fits in an `int` comfortably. The **sum** is 10^10, which does not. The rule: **the
running total overflows, not the data.** Any variable that adds up a whole collection should be
`long long` unless you have proved otherwise, and proving otherwise takes longer than typing
`long long`.

### Modular arithmetic, which is where 1LL lives

Nearly every counting problem asks for the answer modulo 1,000,000,007. Here is why that
constant, and how to multiply safely under it.

```cpp
const long long MOD = 1000000007;    // 1e9 + 7, a prime just under 2^30

long long a = 999999999;
long long b = 999999999;

long long ok   = (a * b) % MOD;               // a*b is ~1e18 — fits in long long
long long ugly = (int)a * (int)b % MOD;       // 32-bit multiply — destroyed
```

Two values below 10^9 multiply to below 10^18, and `long long` holds 9.2 × 10^18, so the product
of two already-reduced values is safe in 64 bits — with about nine times headroom. That headroom
is the entire reason the modulus is around 10^9 and not 10^18.

The two rules that follow:

- **Reduce after every operation**, so both sides are always below MOD before you multiply.
- **Never let three things multiply before a `%`.** `a * b * c` with each near 10^9 is 10^27 and
  overflows `long long` too. Write `(a * b % MOD) * c % MOD`.

And subtraction needs the non-negative fix, because C++ `%` keeps the sign of the left side:

```cpp
long long diff = ((a - b) % MOD + MOD) % MOD;   // always in [0, MOD)
```

### The complete program

```cpp
// numbers.cpp — every overflow trap in this lesson, demonstrated.
//   g++ -std=c++20 -O2 -Wall -Wextra -o numbers numbers.cpp && ./numbers

#include <bits/stdc++.h>
using namespace std;

int main() {
    // ---- 1. the two numbers you must know ----
    cout << "int max        = " << numeric_limits<int>::max()       << "\n";
    cout << "long long max  = " << numeric_limits<long long>::max() << "\n\n";

    // ---- 2. the wrap ----
    int big = numeric_limits<int>::max();
    cout << "int max + 1    = " << big + 1 << "   (no error, just wrong)\n\n";

    // ---- 3. the mid-expression trap ----
    int n = 100000;
    long long still_wrong = n * n;       // int * int, computed in 32 bits
    long long right       = 1LL * n * n; // forced to 64 bits before multiplying
    cout << "n*n as int     = " << still_wrong << "   (wrong)\n";
    cout << "1LL*n*n        = " << right       << "   (right)\n\n";

    // ---- 4. the running total, not the data ----
    vector<int> a(100000, 100000);
    int       bad  = 0;
    long long good = 0;
    for (int x : a) { bad += x; good += x; }
    cout << "sum in int       = " << bad  << "   (wrong)\n";
    cout << "sum in long long = " << good << "   (right)\n\n";

    // ---- 5. the binary search midpoint ----
    int lo = 2000000000, hi = 2000000001;
    cout << "(lo+hi)/2      = " << (lo + hi) / 2      << "   (wrong: overflowed)\n";
    cout << "lo+(hi-lo)/2   = " << lo + (hi - lo) / 2 << "   (right)\n\n";

    // ---- 6. division truncates towards zero ----
    cout << " 7/2 = " <<  7 / 2 << "    -7/2 = " << -7 / 2 << "\n";
    cout << " 7%2 = " <<  7 % 2 << "    -7%2 = " << -7 % 2 << "\n\n";

    // ---- 7. doubles are not real numbers ----
    double x = 0.1 + 0.2;
    cout.precision(17);
    cout << "0.1 + 0.2      = " << x << "\n";
    cout << "x == 0.3       = " << (x == 0.3 ? "true" : "false") << "\n";
    cout << "close enough   = " << (fabs(x - 0.3) < 1e-9 ? "true" : "false") << "\n\n";

    // ---- 8. modular arithmetic done safely ----
    const long long MOD = 1000000007;
    long long p = 999999999, q = 999999999;
    cout << "p*q % MOD      = " << p * q % MOD << "\n";
    cout << "(p-q-1) fixed  = " << ((p - q - 1) % MOD + MOD) % MOD << "\n";

    return 0;
}
```

Expected output:

```
int max        = 2147483647
long long max  = 9223372036854775807

int max + 1    = -2147483648   (no error, just wrong)

n*n as int     = 1410065408   (wrong)
1LL*n*n        = 10000000000   (right)

sum in int       = 1410065408   (wrong)
sum in long long = 10000000000   (right)

(lo+hi)/2      = -147483648   (wrong: overflowed)
lo+(hi-lo)/2   = 2000000000   (right)

 7/2 = 3    -7/2 = -3
 7%2 = 1    -7%2 = -1

0.1 + 0.2      = 0.30000000000000004
x == 0.3       = false
close enough   = true

p*q % MOD      = 999999986
(p-q-1) fixed  = 1000000006
```

The `(lo+hi)/2` line printing a negative number is the whole of section 7 in one line of output.
Read it twice.

---

## 6. What it costs

Types cost memory, and memory costs speed, so the sizes are worth knowing.

```
  bool          1 byte
  char          1 byte
  int           4 bytes
  long long     8 bytes
  double        8 bytes
  a pointer     8 bytes   (on any 64-bit machine)
```

An online judge typically gives you 256 MB. So:

```
  256 MB / 4 bytes   =  67,108,864 ints        about 6.7 x 10^7
  256 MB / 8 bytes   =  33,554,432 long longs  about 3.3 x 10^7
```

That is the real constraint behind a lot of problem limits. A table of size 10^4 × 10^4 is 10^8
ints, which is 400 MB, and it will not fit. Switching it to `short` — 2 bytes — halves it to
200 MB and might. This is a real technique, and it is why the sizes matter.

**Does `long long` make your program slower?** Barely, on a 64-bit machine — a 64-bit add is one
instruction, same as a 32-bit add. What it does cost is memory traffic: 10^7 `long long`s take
80 MB where the `int` version takes 40 MB, and half as many values fit in the processor's fast
memory. For a large collection scanned repeatedly, that is a genuine two-times slowdown, and
today's DSA lesson on counting steps is where that intuition belongs.

**So the rule is not "use `long long` everywhere".** It is: **`long long` for anything that
accumulates or multiplies; `int` for positions, loop counters, and values you have bounded.**

The precision arithmetic, once, so the 2^53 claim is not a bare assertion:

```
  a double has 52 stored fraction bits, plus 1 implied leading bit = 53 bits of precision

  2^53 = 9,007,199,254,740,992   about 9.0 x 10^15

  below that: every whole number is exactly representable
  above that: they start to skip.  2^53 + 1 cannot be stored, and rounds to 2^53.
```

So a `double` is exact for whole numbers up to about 9 × 10^15, and a `long long` is exact up to
9.2 × 10^18. A thousand times further.

---

## 7. The traps

### The near-miss: the binary search midpoint

This is the famous one.
[Day 043](../day-043-binary-search-without-bugs/README.md) writes binary search properly; here
is the arithmetic that breaks it.

```cpp
int mid = (lo + hi) / 2;    // looks right. Is wrong.
```

For ordinary positions in a list this is fine, because nobody has a two-billion-element list.
But binary search is not only used that way.
[Day 046](../day-046-binary-search-on-the-answer/README.md) searches **on the answer** — the
range is a range of values, not of positions, and it can be up to 10^9 on each side.

The input that kills it: `lo = 2000000000`, `hi = 2000000001`. Both fit in an `int` easily.
Their sum is 4,000,000,001, which does not — the maximum is 2,147,483,647. It wraps, `mid` comes
out as −147,483,648, and you either look up a negative position or loop forever.

The fix is one of these two, and they are equivalent:

```cpp
int mid = lo + (hi - lo) / 2;    // the standard idiom
int mid = (lo + hi) >> 1;        // only if lo and hi are known non-negative
```

`hi - lo` is a difference between two in-range values, so it is in range. Adding half of it to
`lo` never exceeds `hi`. **Write it this way always, so you never have to decide whether this is
a case where it matters.**

This exact bug lived in `java.util.Arrays.binarySearch` in the Java standard library from 1997
until it was found and fixed in 2006. Joshua Bloch wrote it up publicly. Mentioning that in an
interview is worth a small amount; knowing the fix is worth a lot.

### The near-miss: `.size()` is unsigned

This one produces a crash that seems to come from nowhere.

```cpp
std::vector<int> v;                       // empty
for (int i = 0; i < v.size() - 1; i++) {  // intended: do nothing
    std::cout << v[i];
}
```

`v.size()` returns `size_t`, which is **unsigned** 64-bit. For an empty collection it is 0. So
`v.size() - 1` is `0 - 1` in unsigned arithmetic, which does not go negative — it wraps to
**18,446,744,073,709,551,615**. The condition is true, the body runs, `v[0]` on an empty
collection reads memory that is not yours, and the program either prints rubbish or crashes.

Three fixes, in order of preference:

```cpp
for (size_t i = 0; i + 1 < v.size(); i++)              // best: no subtraction at all
for (int i = 0; i + 1 < (int)v.size(); i++)            // cast to signed, then it is safe
if (!v.empty()) for (...)                              // guard the empty case
```

And compile with `-Wall`, because g++ warns about the mixed comparison:

```
main.cpp:7:23: warning: comparison of integer expressions of different signedness: 'int' and 'std::vector<int>::size_type' {aka 'long unsigned int'} [-Wsign-compare]
    7 |     for (int i = 0; i < v.size() - 1; i++) {
      |                     ~~^~~~~~~~~~~~~~
```

That warning appears in almost every beginner's C++ and almost every beginner ignores it. It is
telling you about exactly this bug.

### The real error: catching overflow while it runs

The compiler catches overflow in constant expressions:

```
main.cpp:5:26: warning: integer overflow in expression of type 'int' results in '1410065408' [-Woverflow]
    5 |     int x = 100000 * 100000;
      |             ~~~~~~~^~~~~~~~
```

But it cannot catch it when the values come from input, which is exactly when it matters. For
that there is a run-time tool. Compile with the **undefined behaviour sanitiser**:

```
g++ -std=c++17 -g -fsanitize=address,undefined -o prog prog.cpp && ./prog
```

Now the same overflow reports itself:

```
main.cpp:8:19: runtime error: signed integer overflow: 2000000000 + 2000000000 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior main.cpp:8:19
```

And reading past the end of a collection reports itself too:

```
=================================================================
==12841==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000014 at pc 0x0000004012a1
READ of size 4 at 0x602000000014 thread T0
    #0 0x4012a0 in main main.cpp:9
```

**This is the most useful debugging tool in competitive C++ and most beginners have never heard
of it.** It slows the program by roughly two to three times, so it is for local testing, never
for submission. Add it to your local compile command and leave it there.

### The one that is not an error and should be

```cpp
double balance = 0.0;
for (int i = 0; i < 10; i++) balance += 0.1;
if (balance == 1.0) std::cout << "settled\n";   // never prints
```

Ten additions of a value that cannot be represented exactly, and the total is
0.99999999999999989. No warning, no error, and the `if` is simply false forever. This is why
money is stored as a whole number of paise, and never as a `double`.

---

## 8. In the interview

### How it gets asked

- *"What's the range of an int?"* — the direct version, and they want the number, not "about two
  billion". Then they want to know what happens past it.
- *"Is there a bug in this binary search?"* — with `(lo + hi) / 2` on the screen. Extremely
  common, and it is a deliberate plant.
- *"This passes the samples and fails on test 14. What would you check first?"* — the applied
  version. Overflow is the correct first answer.
- *"Why do these problems always say modulo 10^9 + 7?"* — asked to see whether you know why that
  particular number.

### What to say out loud, in the first ninety seconds

1. **Give the number.** *"An `int` is 32 bits, so it goes up to 2,147,483,647 — a bit over two
   billion. A `long long` is 64 bits and goes to about 9.2 × 10^18."*
2. **Say what happens past it, precisely.** *"For signed types, overflow is undefined behaviour
   — not defined wraparound. In practice it wraps to a large negative number, but the optimiser
   is allowed to assume it never happens."*
3. **Name the silence.** *"There is no exception and no warning while it runs. You just get a
   wrong number, which is why it usually shows up as a wrong answer on a large test rather than
   a crash."*
4. **Name where it actually happens.** *"The trap is mid-expression. `long long x = a * b;` with
   two ints still overflows, because C++ computes the right-hand side as an `int` multiply
   before converting. You need `1LL * a * b`."*
5. **Give the working rule.** *"So my rule is: any running total or product goes in `long long`
   unless I have bounded it. Positions and loop counters stay `int`."*
6. **Offer the famous case.** *"The classic instance is `(lo + hi) / 2` in binary search — I
   always write `lo + (hi - lo) / 2`."*

Step 2 is the one that separates people. Almost everyone says "it wraps around". Saying
"undefined behaviour, and here is what that permits the compiler to do" is a different level of
answer.

### The follow-ups

**"How would you detect overflow before it happens?"**
Three ways, depending on the setting. In a contest, by estimating: if the largest possible
product exceeds 2 × 10^9, use `long long`; that check takes two seconds and is what I actually
do. In code that ships, with the compiler builtins — `__builtin_mul_overflow(a, b, &result)`
returns `true` if the multiplication overflowed, and both GCC and Clang provide it. And when
debugging, with `-fsanitize=undefined`, which reports the exact line and the exact values while
the program runs.

**"Why modulo 10^9 + 7?"**
Three properties at once. It is prime, which means every non-zero value has a modular inverse,
so division under the modulus works via Fermat's little theorem. It is just under 2^30, so any
two reduced values multiply to under 2^60, which fits in a signed 64-bit `long long` with about
nine times headroom. And it is big enough that accidental collisions are unlikely. 998,244,353
is the other one you will see — also prime, and of the form 119 × 2^23 + 1, which makes it
usable for the number-theoretic transform.

**"What is `size_t` and why does it cause bugs?"**
It is the unsigned whole-number type big enough to hold the size of any object — 64-bit unsigned
on a normal machine — and it is what every container's `.size()` returns. It causes bugs because
unsigned subtraction never goes negative: `v.size() - 1` on an empty container is
18,446,744,073,709,551,615, not −1. Any condition with a subtraction on a `.size()` is suspect.
I write `i + 1 < v.size()` instead, and I leave `-Wsign-compare` on so the compiler tells me
when I have mixed signed and unsigned.

**"Would you ever use `unsigned` deliberately?"**
For bit work, yes — shifting into the sign bit of a signed type is undefined, so masks and
hashes should be `unsigned` or `uint64_t`. And where wraparound is genuinely the point. Not for
"this value cannot be negative": the compiler will not enforce that usefully, and it turns every
accidental subtraction into a silent enormous number. Google's C++ style guide says the same
thing, and so do the Core Guidelines.

### A model answer

The interviewer puts up a binary search with `int mid = (lo + hi) / 2;` and asks if anything is
wrong.

> "Yes — the midpoint can overflow.
>
> `lo` and `hi` are both `int`, so they each go up to 2,147,483,647. But their sum can be nearly
> twice that, and a 32-bit `int` cannot hold it. Concretely, if `lo` is 2,000,000,000 and `hi`
> is 2,000,000,001 — both perfectly legal ints — the sum is 4,000,000,001, which overflows.
> Signed overflow is undefined behaviour; in practice it wraps to about −294,967,295, and `mid`
> comes out negative. Then either I look up a negative position, which is undefined behaviour
> again, or the search never converges.
>
> The fix is `int mid = lo + (hi - lo) / 2;`. `hi - lo` is a difference between two in-range
> values, so it is in range. Half of it added to `lo` cannot exceed `hi`. Same answer, no
> intermediate that can overflow.
>
> I would say this matters more than it looks. Searching positions in a list, it never triggers,
> because nobody has a two-billion-element list. But binary searching on the answer — the
> minimum capacity, the smallest feasible time — puts real value ranges in `lo` and `hi`, and
> those genuinely reach 10^9. That is where it fires.
>
> It is also not hypothetical. This exact bug was in `Arrays.binarySearch` in the Java standard
> library for about nine years before anyone found it. So I write the subtraction form every
> time rather than deciding case by case whether it matters.
>
> While I am looking at this — I would also check the running totals. If anywhere in this
> function I am summing or multiplying values, I want those in `long long`, because `int` runs
> out at 2 × 10^9 and a hundred thousand values of a hundred thousand each is 10^10."

That answer names the bug, gives a concrete failing input, explains the mechanism, gives the fix
and why it works, says when it does and does not matter, cites the real-world instance, and
volunteers an adjacent check.

---

## 9. Recall card

1. **`int` holds about 2 × 10^9. `long long` holds about 9 × 10^18.** Those two numbers decide
   every overflow question you will ever be asked.
2. **Signed overflow is undefined behaviour, not wraparound.** No exception, no warning, just a
   wrong number — and the optimiser may assume it never happens.
3. **The trap is mid-expression.** `long long x = a * b;` with two ints still overflows. Write
   `1LL * a * b`. The running total overflows, not the data.
4. **Binary search: `lo + (hi - lo) / 2`, never `(lo + hi) / 2`.** And `.size()` is unsigned, so
   `v.size() - 1` on an empty container is 1.8 × 10^19.
5. **`-fsanitize=address,undefined` finds all of it while the program runs**, with the exact
   line. Use it locally, never on submission. And never compare two `double`s with `==`.

---

**Next in C++:** [day 003 — input, output, and the competitive
template](../day-003-big-o-in-plain-english/04-cpp-input-output.md).
