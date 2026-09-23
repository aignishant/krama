---
day: 4
track: dsa
title: "The growth curves you will meet again and again"
phase: "Foundations: how code costs"
status: written
---

# Day 004 · DSA — The growth curves you will meet again and again

**After today you can:** You can rank O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n) and know what input size each survives.

**The interviewer asks it as:** *n is 100000. Will an O(n^2) solution pass?*

---

## 1. What this is, and why they ask it

There are about seven growth curves in all of interview preparation, and you will meet the
same seven for the next 176 days. Today you learn them in order, and — this is the part
that actually decides interviews — you learn **the largest input each one survives**.

Yesterday you learnt to name a shape. Today you learn to use the name to make a decision
before writing any code. The constraint at the bottom of the problem is not decoration. It
is the interviewer telling you which shape they will accept.

They ask "n is a hundred thousand, will O(n²) pass?" because the answer separates two kinds
of candidate cleanly. One kind writes a solution, submits it, sees "Time Limit Exceeded",
and starts again. The other kind reads `1 <= n <= 10^5`, works out that a quadratic is ten
billion operations, and never writes the quadratic at all. The second kind looks
experienced, because that is exactly what experience looks like.

---

## 2. The story

Anil cooks the evening meal at home. There are four of them — himself, his wife, his mother
and their daughter — and he has done it so often that it needs no thought at all. One pan,
one gas ring, forty minutes from walking into the kitchen to putting it on the table.

In June his sister comes to stay and brings her husband and two children. Eight people now.
Anil does exactly the same thing, twice over: two rounds in the same pan, about eighty
minutes. It is longer and he is tired at the end, but nothing has actually changed. The
method still works. It just takes proportionally more of it.

In November his daughter's naming ceremony brings sixty people to the house.

Anil starts the way he always has, and by half past nine in the morning he knows it is not
going to happen. Sixty people is fifteen rounds in that pan. Fifteen rounds is ten hours,
and there are five. But that is not really the problem. The problem is that the first round
would be stone cold by the time the fifteenth was ready, and there is no point serving cold
food to sixty people.

So he does something different. He borrows the big aluminium vessel from the neighbours, the
one they use for functions, and puts it on the outdoor gas burner in the yard. Everything
goes in at once. His wife and his sister chop for an hour beforehand so that nothing is
waiting. It works, and it works well, and it is a completely different way of cooking rather
than the same way scaled up.

The following March, his nephew's wedding. Six hundred guests.

Anil does not even consider doing it himself, and he is not being modest. The big vessel
holds enough for about eighty. Ten of those vessels means ten fires, and he does not have
ten fires or twenty hands. He rings the caterer his neighbour used, and the caterer arrives
at four in the morning with a truck, four industrial burners, vessels a man could sit in,
and eleven people who each do one thing.

Three sizes. Three completely different methods. And the honest thing about it is that
Anil's method for four was not a bad method. It was a good method, right up to the point
where it was not.

---

## 3. The idea in plain English

Anil's kitchen contains the whole lesson. **Every method has a ceiling.** The pan was fine
to eight and hopeless at sixty. The big vessel was fine to eighty and hopeless at six
hundred. Nothing was wrong with either of them; they simply ran out.

Your solutions have ceilings too, and the ceiling depends only on the shape. Here are the
seven curves in order, from best to worst.

### The seven, in order

**`O(1)` — constant.** The work does not depend on the input at all. Reading `items[5]`,
adding two numbers, looking a key up in a dictionary. Anil's method for a family of four is
not this — but "reach into the fridge and take out one bottle" is. The size of the fridge
does not matter.

**`O(log n)` — logarithmic.** Each step throws away a fixed fraction of what is left, usually
half. Binary search is the example you will meet a hundred times. This is very close to free:
a million items takes twenty steps, a billion takes thirty.

**`O(n)` — linear.** One pass. Double the input, double the work. This is Anil cooking twice
over for eight people — the same method, proportionally more of it.

**`O(n log n)` — linearithmic.** A full pass, repeated once for each halving level. This is
what sorting costs, and it is the ceiling of what you can do when a problem genuinely
requires ordering. It is only a little worse than linear: at a million items it is twenty
times `O(n)`, not a million times.

**`O(n²)` — quadratic.** Every item against every item. Two nested loops. This is the pan at
sixty people — the method that quietly stops being a method.

**`O(n³)` — cubic.** Three nested loops. Rare, and almost always a sign you have missed
something, except in a few matrix and interval problems.

**`O(2ⁿ)` — exponential.** For each item, two choices, so the count doubles with every item
added. Generating every subset. This is the wedding: no amount of effort makes the old
approach work, and you need a different idea entirely — which is usually **dynamic
programming**, starting on [day 143](../day-143-what-dp-is/README.md).

**`O(n!)` — factorial.** Every ordering of n items. Generating all permutations. At n = 12
that is 479 million; at n = 20 the universe is not old enough.

### The table that decides interviews

This is the one to memorise. Assume roughly **10⁸ simple operations per second**.

| Constraint you see | Largest shape that fits | Typical technique |
|---|---|---|
| `n ≤ 10` | `O(n!)` | try every ordering |
| `n ≤ 20` | `O(2ⁿ)` | every subset, bitmask DP |
| `n ≤ 500` | `O(n³)` | three nested loops, interval DP |
| `n ≤ 5,000` | `O(n²)` | two nested loops, most DP |
| `n ≤ 10⁵` | `O(n log n)` | sorting, heaps, binary search |
| `n ≤ 10⁶` | `O(n)` | one pass, hash maps, two pointers |
| `n ≤ 10⁹` | `O(log n)` | binary search on the answer, maths |
| `n` is enormous | `O(1)` | a formula |

Read it from the left. **The constraint names the shape, and the shape names the
technique.** That chain is the most valuable single thing in this course's first month.

### Why `log n` is so small

This is the part beginners take on trust and should not. `log₂ n` is the number of times you
can halve `n` before you reach 1.

Start at 1,000,000. Halve it: 500,000. Again: 250,000. Keep going. You reach 1 after
**twenty** halvings. Now start at 1,000,000,000 — a thousand times bigger. You reach 1 after
**thirty**. A thousandfold increase in the input cost you ten extra steps.

That is why `O(log n)` and `O(1)` sit next to each other in practice, and it is why binary
search is worth the trouble of getting right.

### Why `n log n` is so close to `n`

At n = 1,000,000, `log₂ n` is 20. So `n log n` is twenty million against `n`'s one million.
Twenty times more work — noticeable, and nothing like the gap between `n` and `n²`, which at
the same size is a factor of a million.

The practical consequence: **if you cannot find an `O(n)` solution, sorting first is usually
free.** An interviewer who says "you can sort if you need to" has just told you the target
is `O(n log n)`.

---

## 4. The picture

The ladder, with the actual step counts. This is the table worth being able to reproduce.

```
                    n=10        n=100      n=1,000     n=100,000    n=1,000,000
  O(1)                 1            1            1             1              1
  O(log n)             3            7           10            17             20
  O(n)                10          100        1,000       100,000      1,000,000
  O(n log n)          33          664        9,966     1,700,000     20,000,000
  O(n^2)             100       10,000    1,000,000   10,000,000,000    10^12
  O(2^n)           1,024      10^30       forever       forever        forever
  O(n!)        3,628,800      10^157      forever       forever        forever

                  <-- everything fits -->  <-- the line moves --> <-- only the top three -->
```

**What to notice:** the bottom-left corner is fine. At n = 10 even `O(n!)` finishes. The
damage is all on the right-hand side, and it arrives suddenly. `O(n²)` is perfectly
comfortable at n = 1,000 and completely dead at n = 100,000 — and those are only two steps
apart in how a problem is worded.

Now Anil's ceilings, drawn as the same idea:

```
   people:   4       8      16      60      80     600
             |       |       |       |       |       |
   one pan   [===============]       X       X       X     ceiling: about 8
                             ^
                    still fine, just longer

   big vessel[=============================]  X       X    ceiling: about 80
                                          ^
                              a different method, not a bigger pan

   caterer   [=====================================]  ok   ceiling: thousands
```

**What to notice:** each bar ends. It does not slope off gently — it stops. And the fix at
each boundary is never "the same thing but harder". It is a different method.

Here is the one picture that makes `log n` believable:

```
  n = 1,000,000
      |
      +--> 500,000        1
           +--> 250,000   2
                +--> 125,000    3
                     +--> 62,500     4
                          +--> 31,250     5
                               +--> 15,625     6
                                    +--> 7,812   7
                                         ... 
                                            +--> 1     20

  twenty steps to go from a million to one.
  n = 1,000,000,000 takes thirty. A thousand times the input, ten more steps.
```

**What to notice:** the arrows get shorter and shorter but there are only twenty of them.
Halving is brutal, in a good way.

---

## 5. The code, built step by step

The useful thing to build today is not a sorting routine. It is the calculator you run in
your head at the start of every problem: **given this constraint, which shapes survive?**

Start with the shapes as formulas rather than as loops, because at n = 10⁹ you cannot run
the loop.

```python
import math

def steps_for(shape: str, n: int) -> float:
    """How many operations this shape does at size n."""
    match shape:
        case "O(1)":        return 1
        case "O(log n)":    return math.log2(n)
        case "O(n)":        return n
        case "O(n log n)":  return n * math.log2(n)
        case _:             raise ValueError(shape)
```

`match` is Python's version of a switch. `math.log2(n)` gives the number of halvings. This
already covers the four cheap shapes; the expensive ones need care, because their values
overflow into numbers no computer will finish.

```python
        case "O(n^2)":      return n ** 2
        case "O(n^3)":      return n ** 3
        case "O(2^n)":      return 2.0 ** n if n < 1000 else math.inf
        case "O(n!)":       return math.inf if n > 170 else math.factorial(n)
```

`math.inf` is Python's infinity. Using it for the impossible cases is honest — the answer
really is "more than you will ever do" — and it stops the program from trying to compute a
number with three hundred digits.

Now turn a step count into a verdict.

```python
OPS_PER_SECOND = 100_000_000     # 10^8, the working assumption
TIME_LIMIT_SECONDS = 1.0

def verdict(steps: float) -> str:
    seconds = steps / OPS_PER_SECOND
    if seconds <= TIME_LIMIT_SECONDS * 0.1:
        return "comfortable"
    if seconds <= TIME_LIMIT_SECONDS:
        return "tight"
    return "TLE"
```

Three verdicts, not two. **Tight** matters: a solution that theoretically fits in one second
will fail in Python, which is roughly ten to a hundred times slower than C++. If your
arithmetic says "tight", treat it as a fail and look for a better shape.

And the formatting, so the output is readable.

```python
def human(steps: float) -> str:
    if steps == math.inf:
        return "forever"
    if steps < 1e6:
        return f"{int(steps):,}"
    return f"{steps:.1e}"
```

`1e6` is scientific notation for 1,000,000. `f"{steps:.1e}"` prints large numbers as
`1.0e+10` instead of a wall of digits.

Here is the complete program.

```python
"""Day 4 — will it pass? The calculator you run before writing any code."""

import math

OPS_PER_SECOND = 100_000_000      # 10^8: the working assumption for one second
TIME_LIMIT_SECONDS = 1.0

SHAPES = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(n^3)", "O(2^n)", "O(n!)"]


def steps_for(shape: str, n: int) -> float:
    """How many operations this shape does at size n."""
    match shape:
        case "O(1)":        return 1
        case "O(log n)":    return math.log2(n)
        case "O(n)":        return n
        case "O(n log n)":  return n * math.log2(n)
        case "O(n^2)":      return float(n) ** 2
        case "O(n^3)":      return float(n) ** 3
        case "O(2^n)":      return 2.0 ** n if n < 1000 else math.inf
        case "O(n!)":       return float(math.factorial(n)) if n <= 170 else math.inf
        case _:             raise ValueError(f"unknown shape: {shape}")


def verdict(steps: float) -> str:
    """comfortable / tight / TLE, against a one-second limit."""
    seconds = steps / OPS_PER_SECOND
    if seconds <= TIME_LIMIT_SECONDS * 0.1:
        return "comfortable"
    if seconds <= TIME_LIMIT_SECONDS:
        return "tight"
    return "TLE"


def human(steps: float) -> str:
    if steps == math.inf:
        return "forever"
    if steps < 1e6:
        return f"{int(steps):,}"
    return f"{steps:.1e}"


def largest_n(shape: str) -> int:
    """The biggest input this shape still handles comfortably."""
    n = 1
    while n < 2_000_000_000 and verdict(steps_for(shape, n * 2)) != "TLE":
        n *= 2
    return n


def report(n: int) -> None:
    print(f"\nn = {n:,}")
    print(f"  {'shape':<12}{'operations':>14}   verdict")
    print("  " + "-" * 40)
    for shape in SHAPES:
        s = steps_for(shape, n)
        print(f"  {shape:<12}{human(s):>14}   {verdict(s)}")


if __name__ == "__main__":
    for size in (20, 5_000, 100_000, 1_000_000):
        report(size)

    print("\nlargest n each shape survives comfortably:")
    for shape in SHAPES:
        print(f"  {shape:<12}{largest_n(shape):>16,}")
```

This is exactly what it printed:

```

n = 20
  shape           operations   verdict
  ----------------------------------------
  O(1)                     1   comfortable
  O(log n)                 4   comfortable
  O(n)                    20   comfortable
  O(n log n)              86   comfortable
  O(n^2)                 400   comfortable
  O(n^3)               8,000   comfortable
  O(2^n)             1.0e+06   comfortable
  O(n!)              2.4e+18   TLE

n = 5,000
  shape           operations   verdict
  ----------------------------------------
  O(1)                     1   comfortable
  O(log n)                12   comfortable
  O(n)                 5,000   comfortable
  O(n log n)          61,438   comfortable
  O(n^2)             2.5e+07   tight
  O(n^3)             1.2e+11   TLE
  O(2^n)             forever   TLE
  O(n!)              forever   TLE

n = 100,000
  shape           operations   verdict
  ----------------------------------------
  O(1)                     1   comfortable
  O(log n)                16   comfortable
  O(n)               100,000   comfortable
  O(n log n)         1.7e+06   comfortable
  O(n^2)             1.0e+10   TLE
  O(n^3)             1.0e+15   TLE
  O(2^n)             forever   TLE
  O(n!)              forever   TLE

n = 1,000,000
  shape           operations   verdict
  ----------------------------------------
  O(1)                     1   comfortable
  O(log n)                19   comfortable
  O(n)               1.0e+06   comfortable
  O(n log n)         2.0e+07   tight
  O(n^2)             1.0e+12   TLE
  O(n^3)             1.0e+18   TLE
  O(2^n)             forever   TLE
  O(n!)              forever   TLE

largest n each shape survives comfortably:
  O(1)           2,147,483,648
  O(log n)       2,147,483,648
  O(n)              67,108,864
  O(n log n)         4,194,304
  O(n^2)                 8,192
  O(n^3)                   256
  O(2^n)                    16
  O(n!)                      8
```

**Read the last block.** Those eight numbers are the whole lesson in a form you can carry
into an interview. `O(n²)` runs out around eight thousand, `O(n³)` around 256, `O(2ⁿ)` around
16, and `O(n!)` around 8. Note that the program's figures are stricter than the rule-of-thumb
table above, because `largest_n` demands "comfortable" — a tenfold margin — rather than "just
fits". Both are useful: the table is what you quote, and these are what you would actually bet
on. When a problem says `n ≤ 12` and you are stuck, that is not a coincidence — it is the
setter telling you that trying every ordering is the intended solution.

---

## 6. What it costs

The arithmetic behind each row, done longhand once, so that you can redo it under pressure.

**Will `O(n²)` pass at n = 100,000?**

```
100,000 x 100,000        = 10,000,000,000 operations
10,000,000,000 / 10^8    = 100 seconds
limit                    = 1 second
```

No, by a factor of one hundred. And in Python, which is perhaps 30 times slower than C++
for tight loops, by a factor of a few thousand. The answer is not "probably not". It is
"no, by two orders of magnitude", and saying it with the number attached is the point.

**Will `O(n log n)` pass at n = 100,000?**

```
log2(100,000)            = 16.6, call it 17
100,000 x 17             = 1,700,000 operations
1,700,000 / 10^8         = 0.017 seconds
```

Yes, with a factor of about sixty to spare. Sorting a hundred thousand items is not
something to worry about.

**Where exactly does `O(n²)` stop working?** Set the operation count equal to the budget and
solve:

```
n^2 = 10^8   ->   n = 10,000        (one full second, no margin)
n^2 = 10^7   ->   n = 3,162         (comfortable, tenfold margin)
```

So **`O(n²)` is safe to about 3,000–5,000 and dangerous beyond 10,000.** That single
boundary answers most of the "will it pass" questions you will ever be asked.

**Where does `O(2ⁿ)` stop?**

```
2^20 = 1,048,576         -> fine
2^25 = 33,554,432        -> tight
2^30 = 1,073,741,824     -> 10 seconds, dead
```

So `O(2ⁿ)` is safe to about **20** and dead by **30**. This is why constraints like
`n ≤ 20` in a subsets problem are a standing invitation.

**What Python costs you on top.** The 10⁸ figure is generous for pure Python. A realistic
range:

| Language | Simple operations per second |
|---|---|
| C, C++, Rust | 10⁸ – 10⁹ |
| Java, Go, C# | 10⁸ |
| Python | 10⁶ – 10⁷ |

Python is roughly **10 to 100 times slower**. Two consequences worth knowing. First, treat
"tight" as "fail". Second, work done inside a built-in — `sum()`, `sorted()`, `min()`, a
slice, a set lookup — runs at C speed, not Python speed. `sum(items)` and a hand-written
loop have the same Big-O and differ by perhaps thirtyfold in practice.

**Space has its own ceiling, and it is lower than people expect.** A Python integer in a
list costs about 8 bytes for the reference plus 28 for the object. A memory limit of 256 MB
therefore means:

```
256 MB / 36 bytes = about 7,000,000 Python integers in a list
```

So an `O(n²)` **space** solution at n = 10,000 wants 100 million entries, which is several
gigabytes, and it dies before the time limit ever comes into play.
[Day 007](../day-007-space-complexity/README.md) is about exactly this.

---

## 7. The traps

### Trap one: reading the wrong `n`

Here is a constraint block, copied from the kind of problem that catches people:

```
1 <= t <= 10^5                  (number of test cases)
1 <= n <= 10^5                  (array length per test case)
sum of n over all test cases <= 2 * 10^5
```

The naive read is "n is 10⁵, so `O(n log n)` is fine". That is right, but only because of
the third line. Without it, 10⁵ test cases each with 10⁵ elements would be 10¹⁰ elements to
even read, and no shape survives that.

The reverse mistake is worse and more common. When there is **no** line bounding the sum, an
`O(n log n)` solution per test case costs `t × n log n = 10⁵ × 1.7 × 10⁶`, which is 10¹¹.
Your per-test-case shape was fine and your total was not.

**How to catch it every time:** find every variable in the constraints, not just the one
called `n`. Multiply the per-case cost by the number of cases. If a `sum of n` line exists,
use it — it is there precisely because the setter needed it to be.

### Trap two: the exponential that does not look exponential

This is the classic, and it is worth meeting properly because it is the reason dynamic
programming exists.

```python
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Six lines. No loops at all. It looks cheaper than a loop, and it is `O(2ⁿ)`, because each
call makes two more.

```
fib(10)  ->  177 calls          0.000 s
fib(20)  ->  21,891 calls       0.006 s
fib(25)  ->  242,785 calls      0.063 s
fib(30)  ->  2,692,537 calls    0.670 s
fib(40)  ->  331,160,281        about 80 seconds
fib(50)  ->  4.1e+10            about 3 hours
```

Ten more in the input, a hundredfold more work. That is what exponential feels like from the
inside — everything is fine, and then one more step and it is over.

And here is the other exponential failure, which does produce a real error. Try to fix `fib`
by making it walk down one at a time instead:

```python
def countdown(n: int) -> int:
    if n == 0:
        return 0
    return 1 + countdown(n - 1)

print(countdown(100000))
```

```
Traceback (most recent call last):
  File "d4.py", line 6, in <module>
    print(countdown(100000))
          ^^^^^^^^^^^^^^^^^
  File "d4.py", line 4, in countdown
    return 1 + countdown(n - 1)
               ^^^^^^^^^^^^^^^^
  File "d4.py", line 4, in countdown
    return 1 + countdown(n - 1)
               ^^^^^^^^^^^^^^^^
  File "d4.py", line 4, in countdown
    return 1 + countdown(n - 1)
               ^^^^^^^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Read it literally. Python allows about **1,000** nested calls by default, and this needed
100,000. The `[Previous line repeated 995 more times]` is Python being merciful about the
output. This one is a **space** limit rather than a time limit — every pending call is
sitting in memory waiting — and it is the reason a recursive solution over an array of
100,000 elements must be rewritten as a loop.
[Day 088](../day-088-the-call-stack/README.md) covers the call stack properly.

**The habit that prevents both traps:** before writing anything, say out loud: "n is at most
X, so I have about 10⁸ operations, so I need `O(...)` or better." Thirty seconds, and it
changes what you write.

---

## 8. In the interview

### How it gets asked

- *"n is 100,000. Will an O(n²) solution pass?"* — the direct version. The expected answer
  has a number in it.
- *"What's the largest n this solution handles?"* — the same question turned around.
- *"The constraint says n ≤ 20. What does that suggest to you?"* — a hint disguised as a
  question. It means "try every subset".
- *"Your solution is O(n log n). Can you get O(n)?"* — asking whether you know that sorting
  is sometimes avoidable with a hash map or counting.

### What to say out loud, in the first ninety seconds

This one is short, and it belongs at the **start** of the problem, not the end.

1. **Read the constraint aloud.** *"n is up to a hundred thousand."*
2. **State the budget.** *"So I've got roughly ten to the eight operations to play with."*
3. **Divide.** *"That rules out O(n squared) — that would be ten to the ten, about a hundred
   seconds. It comfortably allows O(n log n), which is about 1.7 million."*
4. **Name the target.** *"So I'm aiming for O(n log n) or better. Sorting is affordable
   here."*
5. **Then start solving**, with the target already agreed.
6. **If you get stuck, say the budget again.** *"Since sorting is free at this size, let me
   see what the sorted order gives me."* Constraints are hints, and using them out loud is
   the behaviour being assessed.

Doing this at the start costs you fifteen seconds and buys you the interviewer's confidence
for the rest of the round.

### The follow-ups

**"Where does the ten-to-the-eight number come from?"**
It is a rule of thumb for how many simple operations a machine gets through in a second —
loop iterations, comparisons, integer arithmetic. It is deliberately rough. In C++ it is
optimistic-to-fair, and in Python it is optimistic by ten to a hundred times, so I treat
anything within a factor of ten of the limit as a fail rather than a pass. The point is not
precision; it is that the difference between shapes is measured in factors of a thousand,
so a rough number is enough to decide.

**"The constraint says n ≤ 20. What does that tell you?"**
That an exponential solution is intended. Two to the twenty is about a million, which is
nothing. When I see n ≤ 20 or n ≤ 25, I stop looking for a clever polynomial answer and
start thinking about subsets, bitmasks, or trying every assignment. Constraints that small
appear precisely because the polynomial solution does not exist.

**"Is O(n log n) ever worse than O(n²) in practice?"**
Yes, for small inputs, because of constants. Sorting has real overhead per element, so at
n = 20 a tight quadratic loop can genuinely beat it. That is not a theoretical curiosity —
Python's own sort uses insertion sort, which is quadratic, on runs shorter than 64 elements,
for exactly this reason. Big-O describes what happens as n grows, and when n is small and
fixed, it is answering a question you did not ask.

**"How much slower is Python?"**
Roughly ten to a hundred times, for interpreted loops. But work that happens inside a
built-in runs at C speed — `sum()`, `sorted()`, `min()`, set membership, slicing. So the
practical move is to keep the Python-level loop count down and push work into built-ins
where the shape allows it. It never changes the Big-O; it changes the constant by enough to
matter.

### A model answer

The interviewer has shown a problem: given an array of up to 100,000 integers, find whether
any two of them sum to a target.

> "Before I solve it, let me look at the constraint. n is up to ten to the fifth. My rule of
> thumb is about ten to the eight operations in a second, so an O(n squared) approach would
> be ten to the tenth — around a hundred seconds against a one-second limit. That's dead by
> two orders of magnitude, and in Python it's worse than that. So the brute force isn't a
> candidate; I'll mention it and move on.
>
> That leaves O(n log n) or O(n). O(n log n) is 100,000 times 17, so about 1.7 million
> operations — comfortably fine. So sorting is affordable here, which means one approach is
> to sort and then walk two pointers in from both ends. That's O(n log n) time and O(1)
> extra space.
>
> But I think O(n) is available. One pass with a hash set: for each element, check whether
> target minus that element is already in the set, then add it. Set membership is O(1) on
> average, so that's O(n) time and O(n) space.
>
> I'd go with the hash set version. If the array were already sorted, or if memory were the
> tight constraint rather than time, I'd take the two-pointer version instead — same time
> bound for a sorted input, and constant space.
>
> One thing I'd want to confirm: is that ten-to-the-fifth per test case, and is there a
> bound on the total across test cases? If there are many cases and no bound on the sum, the
> per-case shape isn't the number that matters."

That last question is the one that marks the candidate out. They read the constraints as a
specification rather than as scenery.

---

## 9. Recall card

1. **The order, best to worst:** `O(1)`, `O(log n)`, `O(n)`, `O(n log n)`, `O(n²)`, `O(n³)`,
   `O(2ⁿ)`, `O(n!)`.
2. **The budget is 10⁸ operations per second.** Divide the constraint into it and the shape
   names itself.
3. **The ceilings:** `O(n!)` dies at 11, `O(2ⁿ)` at 20, `O(n³)` at 500, `O(n²)` at 5,000,
   `O(n log n)` at 10⁶, `O(n)` at 10⁷.
4. **The constraint is a hint.** `n ≤ 20` means try every subset. `n ≤ 10⁵` means sort or
   use a hash map. `n ≤ 10⁹` means binary search or a formula.
5. **Python is 10–100× slower**, so treat "just fits" as "fails". And read *every* variable
   in the constraints, not only the one called n.
