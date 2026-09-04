---
day: 171
track: cpp
title: "Shifts, builtins, and bitset"
phase: "C++ and competitive programming"
status: written
---

# Day 171 · C++ — Shifts, builtins, and bitset

**After today you can:** You can use every bit trick the course needs without the shift that silently overflows, and you know the four builtins that replace a loop with one instruction.

**The interviewer asks it as:** *What does 1 << 40 give you, and why?*

---

> Eleventh of the twelve C++ days. Today's DSA lesson teaches you what bits are. This is the phase
> where C++ has the most that Python does not — four processor instructions with no Python
> equivalent, one container that packs a million values into 125 kilobytes, and one shift that
> looks obviously correct and is undefined behaviour.

---

## 1. What this is, and why they ask it

A bit is one yes-or-no. An `int` is thirty-two of them in a row. Once you can see a number that
way, a whole class of problems becomes a single operation: which of these forty items did I
choose, is this number a power of two, how many switches are on, what is the smallest one that is
on.

C++ gives you three things here that Python does not. **The builtins** — `__builtin_popcount` and
its relatives — are single processor instructions that replace a thirty-two-iteration loop.
**`std::bitset`** packs one bit per element, so a million flags cost 125 kilobytes rather than a
megabyte, and operations on the whole thing run sixty-four bits at a time. And **fixed-width
types**, which is the cost side: your row of switches has exactly thirty-two places, and asking
for the forty-first is not an error.

`1 << 40` is the question interviewers ask because it looks completely reasonable and is
undefined behaviour. Most candidates say "about a trillion". The answer is that the expression is
computed in an `int`, an `int` has thirty-two bits, and shifting by forty is off the end of the
type — so the standard says nothing about what happens. Knowing that, and knowing the one-letter
fix, is the whole question.

---

## 2. The story

Bhaskar has run a lodge near the bus stand in Kolhapur since his father handed it over in 2003.
Thirty-two rooms, and behind the desk there is a panel his father had made in the eighties: a
small wooden board with thirty-two switches on it in four rows of eight, one per room. Switch up,
somebody is in. Switch down, the room is free.

He does not think of it as thirty-two separate switches any more. He looks at the board and sees a
shape. A busy Friday looks one way, a dead Tuesday in June looks another, and if the third row is
mostly up he knows without checking that the wedding party is still in.

When somebody rings to ask if there is a room, he does not go through them one at a time. He
glances.

The one thing the board could not do was tell him how many. For years, whenever the owner's
accountant wanted the count, Bhaskar went along the rows with his finger, one to thirty-two,
counting the ones that were up. It took maybe twenty seconds and he lost his place often enough
to have to start again.

The electrician who rewired the place in 2016, a man called Pravin, watched him do this once and
put a small meter on the side of the board. One reading, and it shows how many are up. Bhaskar
says it is the single best rupee his family ever spent, and he is not entirely joking.

The other thing Pravin told him was in 2018, when they built the extension and the rooms went up
to forty.

Bhaskar asked whether the old board could take the new eight. Pravin said no — there are
thirty-two places on it and there is no thirty-third, the board is what it is. And then he said
something Bhaskar repeated for years afterwards, because it had not occurred to him.

He said: do not let anybody just wire it on anyway. If you wire a switch to a place that is not
there, it does not do nothing. Nothing would be fine — you would see it and know. What it does is
find something. Last year in a place in Ichalkaranji somebody did exactly this, and a switch on
the second floor turned on a light in the office, and it took four months and a small fire to work
out why.

---

## 3. The idea in plain English

### The number is the board

An `int` is thirty-two switches. Bit 0 is the rightmost, bit 31 the leftmost.

```
  the number 13, as a board

  bit    7  6  5  4  3  2  1  0
       +--+--+--+--+--+--+--+--+
       | 0| 0| 0| 0| 1| 1| 0| 1|      8 + 4 + 1 = 13
       +--+--+--+--+--+--+--+--+
                    ^     ^  ^
                  bit 3  bit 2  bit 0   are "up"
```

Bit `i` is worth 2^i. That is the whole encoding.

### The five operators

```cpp
a & b      AND   — bit is 1 only where BOTH are 1
a | b      OR    — bit is 1 where EITHER is 1
a ^ b      XOR   — bit is 1 where they DIFFER
~a         NOT   — flips every bit
a << k     shift left  — every bit moves k places left.  Same as a * 2^k
a >> k     shift right — every bit moves k places right. Same as a / 2^k, rounded down
```

`&&` and `||` are the *logical* ones and work on whole true/false values. `&` and `|` work on
every bit separately. Mixing them up is a real bug and the compiler will not always warn.

### The four operations on one bit

Memorise these four lines. Everything else is built from them.

```cpp
bool on = (x >> i) & 1;      // is bit i up?
x |=  (1 << i);              // turn bit i on
x &= ~(1 << i);              // turn bit i off
x ^=  (1 << i);              // flip bit i
```

Read `(x >> i) & 1` as: slide bit `i` down to the rightmost place, then keep only that place.

Read `x &= ~(1 << i)` inside out: `1 << i` is a number with only bit `i` up; `~` flips it to a
number with only bit `i` down; `&` keeps everything except that bit.

### The shift that is the whole interview question

```cpp
long long big = 1 << 40;     // WRONG. Undefined behaviour.
long long ok  = 1LL << 40;   // right.
```

`1` is an `int`. Shifting an `int` by 40 when an `int` has 32 bits is undefined behaviour — not
"gives zero", not "wraps", **undefined**. It is Pravin's forty-first switch: it does not do
nothing, it finds something. On x86 the processor's shift instruction only looks at the bottom
five bits of the count, so a shift by 40 is executed as a shift by 8 and you get 256. On other
hardware you get something else.

Note that writing `long long` on the left does not save you, for exactly the reason
[day 002](../day-002-counting-steps/04-cpp-types-numbers.md) gave: C++ computes the right-hand
side on its own terms first, and only then converts.

**The rule: any shift by 31 or more needs `1LL`.** And `1 << 31` is already wrong on its own —
that lands in the sign bit of a signed `int`, which is also undefined.

Where this actually bites is bitmask problems:

```cpp
for (int mask = 0; mask < (1 << n); mask++)      // fine while n <= 30
for (long long mask = 0; mask < (1LL << n); mask++)   // needed at n >= 31
```

At n = 20 the first line is correct and 2^20 is a million. Nobody enumerates 2^40 subsets anyway,
so in a loop bound the plain version is usually safe — it is when you are *setting bit 40 of a
long long identifier* that this fires, and that happens constantly in hashing and in packing two
numbers into one.

### The four builtins — Pravin's meter

These are single processor instructions. There is no Python equivalent and no way to write
anything as fast by hand.

```cpp
__builtin_popcount(x)    // how many bits are up.        int
__builtin_popcountll(x)  // ... for long long
__builtin_clz(x)         // count leading zeros  (from the left)
__builtin_ctz(x)         // count trailing zeros (from the right)
__builtin_parity(x)      // 1 if an odd number of bits are up
```

`popcount` in one instruction replaces this:

```cpp
int count = 0;
while (x) { count += x & 1; x >>= 1; }    // up to 32 iterations
```

Two things to be careful of. **`__builtin_clz(0)` and `__builtin_ctz(0)` are undefined** — there
are no set bits to find, and the instruction returns rubbish. Guard the zero case. And
`__builtin_popcount` on a `long long` silently truncates to the bottom 32 bits, so a `long long`
needs the `ll` version. That is a genuinely nasty silent bug.

Two useful things they give you directly:

```cpp
int highest_bit = 31 - __builtin_clz(x);      // floor(log2(x)), for x > 0
int lowest_bit  = __builtin_ctz(x);           // position of the lowest set bit
```

Since C++20 there are standard spellings in `<bit>`, which work on every compiler and are what you
would write in code that ships:

```cpp
#include <bit>
std::popcount(x)          // same as __builtin_popcount, but standard and unsigned-only
std::countl_zero(x)       // leading zeros
std::countr_zero(x)       // trailing zeros
std::has_single_bit(x)    // is it a power of two?
std::bit_width(x)         // how many bits are needed
```

Use `std::` when your judge is on C++20 and `__builtin_` otherwise. Both compile to the same
instruction.

### The three identities worth knowing

```cpp
x & (x - 1)      // clears the LOWEST set bit
x & (-x)         // isolates the lowest set bit (gives just that bit)
x & (x - 1) == 0 // ... is x a power of two? (careful: see the precedence trap)
```

Why `x & (x-1)` clears the lowest set bit: subtracting 1 flips the lowest set bit to 0 and turns
every 0 below it into 1. The `&` then keeps only the bits above, which were unchanged. So
`12 & 11` is `1100 & 1011` = `1000` = 8.

That gives you a popcount loop that runs once per *set* bit rather than once per bit, which is how
you count bits on a compiler with no builtin:

```cpp
int count = 0;
while (x) { x &= x - 1; count++; }
```

### XOR, and why day 173 exists

Three facts, and they are the entire single-number family:

```
  x ^ x  =  0        anything XOR itself is zero
  x ^ 0  =  x        anything XOR zero is itself
  XOR is commutative and associative — order does not matter
```

So XOR everything together, the pairs cancel, and the one unpaired value survives. That is
[day 173](../day-173-xor/README.md) in three lines, and in C++ it is:

```cpp
int single = 0;
for (int v : values) single ^= v;
```

### `std::bitset` — a board with a million switches

```cpp
#include <bitset>

std::bitset<1000000> flags;      // size fixed at COMPILE time
flags.set(42);                   // turn bit 42 on
flags.reset(42);                 // off
flags.flip(42);
bool on = flags[42];
int  n  = flags.count();         // popcount of the whole thing
bool any = flags.any();
```

Two reasons it matters.

**Memory.** One bit per element rather than one byte:

```
  10^6 flags as vector<char>    = 1,000,000 bytes  = 1 MB
  10^6 flags as bitset          =   125,000 bytes  = 125 KB
```

**Speed on whole-set operations.** `a |= b` on two bitsets of a million bits processes 64 bits per
instruction, so it is roughly 64 times faster than a loop. That is what turns an O(n²) subset-DP
or reachability problem into O(n²/64), which at n = 10^4 is the difference between 10^8 and
1.5 × 10^6.

The catch: **the size must be a compile-time constant.** `std::bitset<n>` with a variable `n` does
not compile. When the size is only known while running, use `vector<bool>`, which packs bits too
but is slower and has the proxy-reference oddity from
[day 125](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md).

### Enumerating subsets

Every subset of n items, as a mask:

```cpp
for (int mask = 0; mask < (1 << n); mask++) {
    for (int i = 0; i < n; i++)
        if (mask & (1 << i)) { /* item i is in this subset */ }
}
```

That is O(2^n × n), which is fine to n = 20 and tight at n = 22. It is the shape of
[day 160's bitmask DP](../day-160-bitmask-dp/README.md).

And every subset **of a given mask**, which is the trick people do not know:

```cpp
for (int sub = mask; sub; sub = (sub - 1) & mask) { /* sub is a subset of mask */ }
// note: this misses the empty set — handle sub == 0 separately
```

Summed over all masks that is O(3^n), not O(4^n), which is the difference between feasible and not
at n = 18.

---

## 4. The picture

The four single-bit operations, drawn:

```
  x = 13                      bit  7 6 5 4 3 2 1 0
                                  [0 0 0 0 1 1 0 1]

  TEST bit 2:   (x >> 2) & 1
     x >> 2                       [0 0 0 0 0 0 1 1]     slide it to the right end
     & 1                          [0 0 0 0 0 0 0 1]     keep only that place  -> 1

  SET bit 4:    x |= (1 << 4)
     1 << 4                       [0 0 0 1 0 0 0 0]
     x |  that                    [0 0 0 1 1 1 0 1]     = 29

  CLEAR bit 0:  x &= ~(1 << 0)
     1 << 0                       [0 0 0 0 0 0 0 1]
     ~(1 << 0)                    [1 1 1 1 1 1 1 0]     everything EXCEPT bit 0
     x &  that                    [0 0 0 0 1 1 0 0]     = 12

  LOWEST SET BIT:  x & (x - 1)  clears it
     x   = 13                     [0 0 0 0 1 1 0 1]
     x-1 = 12                     [0 0 0 0 1 1 0 0]     the lowest 1 became 0
     &                            [0 0 0 0 1 1 0 0]     = 12.  bit 0 is gone.
```

**What to notice:** every one of them is "build a number with the right bits, then combine". There
is nothing to remember except which combiner keeps what.

Now the shift off the end of the board:

```
  1 << 40, computed in an int

  the int has 32 places:
        bit 31 ....................... bit 0
       [ .  .  .  .  .  .  .  .  .  .  1 ]

  shifting left by 40 asks for place 40.

       place 40  ->  |  there is no place 40.
                     v
       +----------------------------------+
       |  bits 31 ... 0                   |   the board ends here
       +----------------------------------+

  What actually happens on x86:
       the shift instruction reads only the bottom 5 bits of the count
       40 in binary = 101000.  bottom 5 bits = 01000 = 8.
       so it shifts by 8, and 1 << 40 evaluates to 256.

  Not zero. Not a trillion. 256.
  And on other hardware, something else. That is what "undefined" means.
```

**What to notice:** the wrong answer is not obviously wrong. 256 is a perfectly plausible-looking
number, which is Pravin's point about the switch that finds something rather than doing nothing.

---

## 5. The code, built step by step

### Packing yes-or-no facts into one number

The core use, and the one that makes bitmask DP possible.

```cpp
int chosen = 0;
chosen |= (1 << 3);              // item 3 is in
chosen |= (1 << 7);              // item 7 is in

bool has_3 = (chosen >> 3) & 1;  // true
int  how_many = __builtin_popcount(chosen);   // 2
```

One `int` now holds a set of up to 31 items, comparable with `==`, usable as a `map` key, and
copyable for free. That is why bitmask DP indexes its table by a mask.

### Powers of two, and the precedence trap

```cpp
bool is_power_of_two(int x) {
    return x > 0 && (x & (x - 1)) == 0;
}
```

The `x > 0` matters: `x & (x-1)` is 0 for `x = 0` too, and zero is not a power of two.

The brackets around `(x & (x - 1))` also matter, and section 7 shows what happens without them.
`&` binds **looser** than `==` in C++, which is a genuine language wart inherited from C.

### Every subset

```cpp
// the maximum sum of any subset with at most k items chosen — n <= 20
int best_subset(const std::vector<int>& v, int k) {
    int n = (int)v.size();
    int best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        if (__builtin_popcount(mask) > k) continue;    // one instruction, not a loop
        int sum = 0;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i)) sum += v[i];
        best = std::max(best, sum);
    }
    return best;
}
```

`__builtin_popcount(mask) > k` is the line that shows why the builtin is worth knowing: it runs
2^n times, and replacing it with a 20-iteration loop makes the whole function twenty times slower.

### `bitset` for a sieve

The classic place where the memory saving decides whether it fits.

```cpp
const int N = 10000000;
std::bitset<N + 1> composite;                 // 10^7 bits = 1.25 MB, not 10 MB

for (int i = 2; 1LL * i * i <= N; i++)        // 1LL: i*i overflows int near 10^7
    if (!composite[i])
        for (int j = i * i; j <= N; j += i)
            composite[j] = true;
```

Note the `1LL * i * i` in the loop condition — at N = 10^7, `i` reaches about 3163 and `i * i` is
fine, but push N to 10^9 and it is not. Making it a habit costs nothing.

### The complete program

```cpp
// bits.cpp — every bit operation the course needs, and the shift that is a bug.
//   g++ -std=c++20 -O2 -Wall -Wextra -o bits bits.cpp && ./bits

#include <bits/stdc++.h>
using namespace std;

bool is_power_of_two(int x) {
    return x > 0 && (x & (x - 1)) == 0;      // brackets required: & binds looser than ==
}

// The one number that appears an odd number of times. Day 173.
int single_number(const vector<int>& v) {
    int result = 0;
    for (int x : v) result ^= x;             // pairs cancel to 0
    return result;
}

// Largest subset sum using at most k items. n <= 20.
int best_subset(const vector<int>& v, int k) {
    int n = (int)v.size(), best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        if (__builtin_popcount(mask) > k) continue;
        int sum = 0;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i)) sum += v[i];
        best = max(best, sum);
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ---- the four operations ----
    int x = 13;                                       // 0b1101
    cout << "x            = " << x << "  (" << bitset<8>(x) << ")\n";
    cout << "bit 2 up?      " << ((x >> 2) & 1) << "\n";
    cout << "set bit 4    = " << (x | (1 << 4))  << "  (" << bitset<8>(x | (1 << 4)) << ")\n";
    cout << "clear bit 0  = " << (x & ~(1 << 0)) << "  (" << bitset<8>(x & ~(1 << 0)) << ")\n";
    cout << "flip bit 1   = " << (x ^ (1 << 1))  << "  (" << bitset<8>(x ^ (1 << 1)) << ")\n\n";

    // ---- the builtins ----
    cout << "popcount(13)   = " << __builtin_popcount(13) << "\n";
    cout << "ctz(12)        = " << __builtin_ctz(12)      << "   (lowest set bit position)\n";
    cout << "31-clz(13)     = " << 31 - __builtin_clz(13) << "   (floor of log2)\n";
    cout << "13 & 12        = " << (13 & 12) << "   (x & (x-1) clears the lowest set bit)\n";
    cout << "12 & -12       = " << (12 & -12) << "   (x & -x isolates it)\n\n";

    // ---- the shift ----
    long long wrong = 1   << 30;      // fine: 30 < 31
    long long right = 1LL << 40;      // fine: computed in 64 bits
    cout << "1   << 30 = " << wrong << "\n";
    cout << "1LL << 40 = " << right << "   (1 << 40 would be undefined)\n\n";

    // ---- powers of two ----
    for (int v : {1, 8, 12, 1024, 0})
        cout << v << " power of two? " << (is_power_of_two(v) ? "yes" : "no") << "\n";
    cout << "\n";

    // ---- xor ----
    cout << "single number in {4,1,2,1,2} = " << single_number({4, 1, 2, 1, 2}) << "\n";

    // ---- subsets ----
    cout << "best subset of {5,1,9,3} with <= 2 items = "
         << best_subset({5, 1, 9, 3}, 2) << "\n\n";

    // ---- bitset: a sieve, in a fraction of the memory ----
    const int N = 1000000;
    bitset<N + 1> composite;
    for (int i = 2; 1LL * i * i <= N; i++)
        if (!composite[i])
            for (int j = i * i; j <= N; j += i) composite[j] = true;
    cout << "primes below 10^6 = " << (N - 1 - (int)composite.count() + 1 - 1) << "\n";
    cout << "bitset<10^6> uses " << sizeof(composite) << " bytes"
         << "   (vector<char> would use " << N + 1 << ")\n";

    return 0;
}
```

Expected output:

```
x            = 13  (00001101)
bit 2 up?      1
set bit 4    = 29  (00011101)
clear bit 0  = 12  (00001100)
flip bit 1   = 15  (00001111)

popcount(13)   = 3
ctz(12)        = 2   (lowest set bit position)
31-clz(13)     = 3   (floor of log2)
13 & 12        = 12   (x & (x-1) clears the lowest set bit)
12 & -12       = 4   (x & -x isolates it)

1   << 30 = 1073741824
1LL << 40 = 1099511627776   (1 << 40 would be undefined)

1 power of two? yes
8 power of two? yes
12 power of two? no
1024 power of two? yes
0 power of two? no

single number in {4,1,2,1,2} = 4

best subset of {5,1,9,3} with <= 2 items = 14

primes below 10^6 = 78498
bitset<10^6> uses 125008 bytes   (vector<char> would use 1000001)
```

The last line is the whole argument for `bitset` in one comparison: 125 kilobytes against a
megabyte, for the same information.

---

## 6. What it costs

### The builtins against the loop

```
  counting the set bits of 10^7 numbers

  while (x) { count += x & 1; x >>= 1; }      ~32 iterations each   ~0.35 s
  while (x) { x &= x - 1; count++; }          ~popcount iterations  ~0.10 s
  __builtin_popcount(x)                       ONE instruction       ~0.01 s
```

**Thirty-five times.** On modern x86 `popcount` is a single instruction with a latency of about
three cycles, and GCC emits it directly when compiling for a processor that has it. The middle row
is what to write if you are ever on a target without it.

### `bitset` against the alternatives

```
  n = 10^6 flags

  memory:
    vector<int>    4,000,000 bytes    4 MB
    vector<char>   1,000,000 bytes    1 MB
    vector<bool>     125,000 bytes  125 KB   (packed, but slow: proxy + masking per access)
    bitset<10^6>     125,000 bytes  125 KB   (packed, and fast)

  whole-set OR of two of them (a |= b):
    a loop over 10^6 chars      10^6 operations       ~1.0 ms
    bitset |=                   10^6 / 64 = 15,625    ~0.02 ms       ~60x
```

That 64-times factor on whole-set operations is what makes some solutions possible at all:

```
  reachability DP, n = 10^4 states, n transitions each
    plain:   10^4 x 10^4        =  10^8      ->  ~1.0 s     too slow
    bitset:  10^4 x 10^4 / 64   =  1.6x10^6  ->  ~0.02 s    comfortable
```

### Subset enumeration

```
  all 2^n subsets, with an inner loop over n bits:  O(2^n x n)

    n = 15    32,768 x 15      =  5 x 10^5    ->  instant
    n = 20     10^6   x 20     =  2 x 10^7    ->  ~0.2 s
    n = 22     4x10^6 x 22     =  9 x 10^7    ->  ~0.9 s     tight
    n = 25     3x10^7 x 25     =  8 x 10^8    ->  ~8 s       no

  so n <= 20 is the bitmask range, and n <= 22 at a push.

  all subsets of all masks:  sum over masks of 2^popcount(mask)  =  3^n, not 4^n
    n = 18:   3^18  =  3.9 x 10^8   ->  ~4 s     borderline
    n = 15:   3^15  =  1.4 x 10^7   ->  ~0.15 s  fine
```

Those two numbers — **20 for subsets, 18 for subsets-of-subsets** — are what you check the
constraint against before deciding this is a bitmask problem.

---

## 7. The traps

### The real error: shifting past the width

```cpp
long long x = 1 << 40;
```

g++ catches the constant case:

```
main.cpp:6:21: warning: left shift count >= width of type [-Wshift-count-overflow]
    6 |     long long x = 1 << 40;
      |                     ^~
```

A **warning**, not an error. The program compiles and `x` comes out as 256 on x86. And when the
shift count is a variable it cannot warn at all, which is the case that actually reaches a judge:

```cpp
long long bit = 1 << i;      // silently wrong for i >= 31, no warning
```

Compile with the undefined-behaviour sanitiser and it reports itself while running:

```
main.cpp:7:23: runtime error: left shift of 1 by 40 places cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior main.cpp:7:23
```

**The fix is one character: `1LL << i`.** Make it your default and you never have to think about
whether this is a case where it matters.

`1 << 31` is the same bug one step earlier — that shifts into the sign bit of a signed `int`,
which is also undefined. If you want the top bit of a 32-bit value, use `1u << 31` or `1LL << 31`.

### The real error: `&` binds looser than `==`

```cpp
if (x & 1 == 0) { /* intended: is x even */ }
```

```
main.cpp:8:14: warning: suggest parentheses around comparison in operand of '&' [-Wparentheses]
    8 |     if (x & 1 == 0) {
      |         ~~^~~~~~~~
```

C++ parses this as `x & (1 == 0)`, which is `x & 0`, which is always 0, which is always false. The
branch never runs. This is a genuine C language design mistake that C++ inherited and cannot fix.

**Bracket every bitwise operation used in a comparison:** `if ((x & 1) == 0)`.

The same applies to `x >> i & 1` — that one happens to parse correctly, because `>>` binds tighter
than `&`, but bracket it anyway rather than remembering a table.

### The near-miss: `popcount` on a `long long`

```cpp
long long mask = 1LL << 40;
int bits = __builtin_popcount(mask);       // 0. Wrong.
int ok   = __builtin_popcountll(mask);     // 1. Right.
```

`__builtin_popcount` takes an `unsigned int`, so a `long long` is silently truncated to its bottom
32 bits. Bit 40 is not in there, so the answer is 0. `-Wall` says nothing, because narrowing in a
function call is legal.

**Any builtin on a `long long` needs the `ll` suffix**: `popcountll`, `clzll`, `ctzll`. C++20's
`std::popcount` has no such problem, because it is a template and deduces the width.

### The near-miss: `clz` and `ctz` of zero

```cpp
int highest = 31 - __builtin_clz(x);     // undefined when x == 0
```

There is no leading-zero count for a value with no set bits, and the instruction's behaviour is
undefined for zero. In practice it returns whatever was in the register, so you get a plausible
number and a wrong answer.

```cpp
int highest = (x == 0) ? -1 : 31 - __builtin_clz(x);
```

`__builtin_popcount(0)` is fine — it is 0. Only `clz` and `ctz` have this hole.

### The near-miss: `bitset` needs a compile-time size

```cpp
int n;
std::cin >> n;
std::bitset<n> flags;        // does not compile
```

```
main.cpp:9:20: error: the value of 'n' is not usable in a constant expression
    9 |     std::bitset<n> flags;
      |                    ^~~~~
main.cpp:8:9: note: 'int n' is not const
    8 |     int n;
      |         ^
```

The size is part of the type, so it must be known when you compile. **Declare it at the maximum
the constraints allow** — `bitset<200005>` — and only use the first `n` bits. The unused ones cost
one bit each, which is nothing.

### The quiet one: right-shifting a negative number

```cpp
int x = -8;
std::cout << (x >> 1);      // -4 on every mainstream compiler
```

This is **implementation-defined**, not undefined — the standard permits either an arithmetic
shift, which keeps the sign, or a logical one, which does not. Every compiler you will meet does
the arithmetic shift, and C++20 finally made it required. But for bit manipulation, use `unsigned`
or `uint64_t` and the question does not arise. That is the one place where reaching for `unsigned`
is right, as [day 002](../day-002-counting-steps/04-cpp-types-numbers.md) said.

---

## 8. In the interview

### How it gets asked

- *"What does `1 << 40` give you?"* — the direct version, and the answer most people get wrong.
- *"Count the set bits in an integer."* — where the loop is acceptable and the builtin plus
  `x & (x-1)` is better.
- *"Check whether a number is a power of two, without a loop."* — the classic one-liner.
- *"How would you represent a set of twenty items so you can compare and hash it cheaply?"* — the
  applied version, and the real reason bitmasks exist.

### What to say out loud, in the first ninety seconds

1. **Name the type of the literal.** *"`1` is an `int`, so `1 << 40` is a shift of a 32-bit value
   by 40, which is undefined behaviour."*
2. **Say what undefined means here.** *"Not zero, not a wrap — the standard says nothing. On x86
   the shift instruction masks the count to its bottom five bits, so it actually shifts by 8 and
   gives 256."*
3. **Note that the target type does not help.** *"Assigning it to a `long long` does not fix it,
   because C++ evaluates the right-hand side entirely on its own before converting."*
4. **Give the fix.** *"`1LL << 40`. One character, and I write it by default so I never have to
   decide whether the count could reach 31."*
5. **Add the neighbouring case.** *"`1 << 31` is the same bug one step earlier — that shifts into
   the sign bit of a signed int, which is also undefined. `1u << 31` or `1LL << 31` if I want that
   bit."*
6. **Say how you would catch it.** *"g++ warns with `-Wshift-count-overflow` when the count is a
   constant, but not when it is a variable. `-fsanitize=undefined` catches the variable case at run
   time and names the line."*

Step 2 is what separates a real answer from a memorised one. "It's undefined" is correct and
slightly empty; "and here is what the hardware actually does, which is why the wrong answer looks
plausible" is the answer of someone who has debugged it.

### The follow-ups

**"How would you count the set bits?"**
`__builtin_popcount`, which is a single instruction on any modern processor — or `std::popcount`
from `<bit>` in C++20, which is the standard spelling and deduces the width so it cannot be
silently truncated. If I had to write it, I would use `while (x) { x &= x - 1; count++; }` rather
than shifting through all thirty-two positions, because `x & (x-1)` clears the lowest set bit, so
the loop runs once per set bit instead of once per bit. On a sparse value that is a large
difference. The one thing I would watch is that `__builtin_popcount` takes an `unsigned int`, so a
`long long` needs `__builtin_popcountll` — otherwise the top thirty-two bits are silently dropped.

**"Why is `x & (x - 1) == 0` not a power-of-two test?"**
Two reasons. The brackets: `&` binds looser than `==` in C++, so that parses as `x & (1 == 0)`,
which is `x & 0`, which is always false. It needs to be `(x & (x - 1)) == 0`, and `-Wparentheses`
warns about exactly this. And even bracketed it is incomplete, because zero passes it — `0 & -1`
is 0 — and zero is not a power of two. The correct test is
`x > 0 && (x & (x - 1)) == 0`, or `std::has_single_bit(x)` in C++20.

**"When would you use `std::bitset` over `vector<bool>`?"**
Whenever the size is a compile-time constant, which in competitive programming it usually can be —
I declare it at the constraint maximum and use a prefix. Both pack one bit per element, so the
memory is the same, but `bitset` is much faster: it supports whole-set operations like `|=`, `&=`
and `count()` that process sixty-four bits per instruction, where `vector<bool>` gives you a proxy
object per access and masks one bit at a time. That 64-times factor is what turns an O(n²)
reachability or subset DP into O(n²/64) — at n = 10^4 that is 10^8 operations against 1.6 × 10^6.
`vector<bool>` is what I use when the size is only known while running.

**"When is a bitmask the right representation at all?"**
When the set is small and fixed — up to about twenty items, sometimes twenty-two. Then a whole
subset is one `int`, which means I can compare subsets with `==`, use one as a `map` key or a DP
table index, copy one for free, and union or intersect two with a single instruction. That is
exactly what bitmask DP needs. The limit is the exponential: 2^20 is a million and fine, 2^25 is
thirty-three million times whatever I do per subset and is not. So I check the constraint first —
n ≤ 20 in a problem statement is very often the author telling me it is a bitmask problem.

### A model answer

> "`1 << 40` is undefined behaviour, and it does not give a trillion.
>
> The reason is the type of the literal. `1` is an `int`, which is thirty-two bits, so the whole
> expression is a shift of a thirty-two-bit value by forty places. The standard says that shifting
> by more than the width of the type is undefined — not that it gives zero, not that it wraps, but
> that there is no defined result at all.
>
> What actually happens on x86 is worth knowing, because it explains why this survives testing. The
> processor's shift instruction only looks at the bottom five bits of the shift count. Forty in
> binary is 101000, and its bottom five bits are 01000, which is eight. So `1 << 40` is executed as
> `1 << 8` and evaluates to 256. That is a perfectly ordinary-looking number, which is why the bug
> gets through — you do not get a crash, you get a plausible wrong answer.
>
> Writing `long long x = 1 << 40;` does not help, and that is the part people miss. C++ evaluates
> the right-hand side entirely on its own terms and only converts afterwards, so the damage is done
> in thirty-two bits before the assignment happens. It is the same shape as the classic
> `long long area = width * height;` overflow.
>
> The fix is one character: `1LL << 40`. I write `1LL` by default for any shift where the count is
> a variable, so I never have to work out whether it could reach thirty-one. And `1 << 31` is the
> same bug one step earlier — that lands in the sign bit of a signed int, which is also undefined,
> so if I want the top bit of a thirty-two-bit value I use `1u << 31`.
>
> On catching it: g++ warns with `-Wshift-count-overflow` when the count is a literal, but it
> cannot when the count is a variable, which is the case that actually reaches production.
> `-fsanitize=undefined` catches that at run time and prints the line and the values — it reports
> it as 'left shift of 1 by 40 places cannot be represented in type int'."

That answer gives the rule, the mechanism, the actual observed wrong value and why it is
dangerous, the near-miss fix that does not work, the real fix, the adjacent case, and the tooling.

---

## 9. Recall card

1. **`1 << 40` is undefined behaviour — `1` is an `int`.** On x86 it silently gives 256. Write
   `1LL << i` by default, and never `1 << 31` on a signed type.
2. **The four operations:** test `(x >> i) & 1`, set `x |= 1 << i`, clear `x &= ~(1 << i)`, flip
   `x ^= 1 << i`.
3. **`__builtin_popcount`, `clz`, `ctz` are single instructions** — thirty-five times faster than
   the loop. Use the `ll` versions for `long long`, and never `clz`/`ctz` of zero.
4. **`x & (x - 1)` clears the lowest set bit; `x & -x` isolates it.** Power of two is
   `x > 0 && (x & (x - 1)) == 0` — and `&` binds looser than `==`, so the brackets are required.
5. **`bitset<N>` is one bit per flag and 64× faster on whole-set operations**, but N must be a
   compile-time constant. Bitmask subsets are feasible to n ≈ 20; subsets-of-subsets to n ≈ 18.

---

**Next in C++:** [day 178 — stress testing, and reading a judge's
verdict](../day-178-thinking-out-loud/04-cpp-stress-testing.md).
