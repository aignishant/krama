---
day: 178
track: cpp
title: "Stress testing, and reading a judge's verdict"
phase: "C++ and competitive programming"
status: written
---

# Day 178 · C++ — Stress testing, and reading a judge's verdict

**After today you can:** You can find the input that breaks your solution in about a minute instead of staring at it, and you know what TLE, WA, RE and MLE each tell you to check first.

**The interviewer asks it as:** *Your solution fails on test 14 of 60 and you cannot see the test. What do you do?*

---

> The last of the twelve C++ days. Every other day in this track taught you to write something.
> This one teaches you to find out that what you wrote is wrong, on purpose, before a judge tells
> you — which is the skill that turns the other eleven into results.

---

## 1. What this is, and why they ask it

You submit. The judge says **wrong answer on test 14 of 60**. It does not show you test 14. Your
code passes both samples. You have no idea what is wrong.

Most people respond by re-reading their code. That almost never works, because you wrote it and
you already believe it is right — you will read what you meant, not what you typed. Some people
add print statements to a case that works, which tells them nothing.

The technique that works is called a **stress test**, and it is the single highest-leverage thing
in competitive programming. You write a second solution that is obviously correct and far too slow.
You write a third program that makes random tiny inputs. Then you loop: generate, run both,
compare, stop when they disagree. Because the inputs are tiny — four elements, values under five —
the failing case that drops out is small enough to work through by hand in thirty seconds.

It takes about ten minutes to set up the first time and roughly ninety seconds every time
afterwards. It finds bugs that hours of staring will not.

Interviewers ask the "test 14" question because it separates people who debug by method from people
who debug by hope, and because the answer — "I would write a brute force and a generator and
compare them" — is a way of thinking that transfers directly to writing tests for real software.

---

## 2. The story

Ashok has scored for the same club side in Belgaum since 1994, and since about 2019 he has done it
on his phone, in the app, along with a college boy called Nikhil who scores the same match at the
same time from the other end of the bench.

Two people scoring one match sounds like a waste of one person. It is not, and Ashok will explain
why to anybody who sits near him.

A scorer working alone is never wrong. That is the problem. He has a number, the number came from
somewhere, and there is nothing in his own head that can tell him the number is bad. He only finds
out at the end, when the totals will not add up, or worse, when they do add up and are quietly
incorrect and nobody ever knows.

With two of them, a mistake shows up as a disagreement. Ashok is slow and careful and misses
almost nothing. Nikhil is quick and occasionally taps the wrong thing. When their numbers differ,
one of them is wrong, and — this is the part Ashok cares about — they now *know* it, immediately,
which is more than either of them could manage alone.

For the first two seasons they compared totals at tea. That was awful. By tea they might be eight
runs apart across a hundred and twenty balls, and finding where meant going back through the whole
morning, ball by ball, both of them tired and neither of them certain.

Now they compare at the end of every over. Six balls. If the numbers differ, the mistake happened
in the last six balls and they find it in about twenty seconds, usually before the bowler has
finished walking back.

Ashok says the mistake is nearly always something ordinary. A leg bye tapped in as a run. A wide
counted twice. Nothing clever, nothing you would ever have predicted — but obvious the moment you
are looking at the right six balls instead of the right two hundred.

The comparing is what finds it. The frequency is what makes it cheap.

---

## 3. The idea in plain English

### The three programs

A stress test is three small programs and a loop.

**`sol.cpp`** — your real solution. Fast, clever, and suspect. This is Nikhil.

**`brute.cpp`** — a second solution written to be *obviously* correct and as slow as you like.
Try every subset. Simulate every step. Sort and scan. It only has to work for n = 6, so it does not
matter that it is exponential. This is Ashok.

**`gen.cpp`** — makes one random test case, small, and takes a seed so the same seed makes the
same case.

Then a loop: generate a case, run both, compare, stop on the first disagreement.

### Why the inputs must be tiny

This is the part people get wrong, and it is the whole reason the technique works.

Generate with n up to 5 and values up to 4. Not n up to 1000. Two reasons:

**The failing case has to be readable.** A wrong answer on `[3, 1, 4, 1, 5]` is something you can
work through in your head in half a minute. A wrong answer on eight hundred numbers is another
problem to solve.

**Small cases find bugs faster.** Most bugs are in the boundaries — the empty case, the single
element, all values equal, two things tied. With n ≤ 5 and values ≤ 4, ties and repeats happen
constantly. With n = 1000 and values up to 10^9, no two values are ever equal and you will never
generate the case that breaks your tie-breaking.

That is Ashok comparing every over rather than at tea. Small and often beats big and rare.

### The generator needs a seed

```cpp
// gen.cpp
#include <bits/stdc++.h>
using namespace std;
int main(int argc, char* argv[]) {
    mt19937 rng(atoi(argv[1]));          // the seed comes from the command line
    int n = rng() % 5 + 1;               // 1..5
    cout << n << "\n";
    for (int i = 0; i < n; i++) cout << rng() % 5 << " \n"[i == n - 1];
    return 0;
}
```

`mt19937` is the standard Mersenne Twister generator, from `<random>`. It is far better than
`rand()` and, more importantly, **seeding it from the command line makes every case
reproducible** — once the loop stops on seed 4471, you can regenerate exactly that case as many
times as you like while you fix the bug.

`" \n"[i == n - 1]` prints a space between values and a newline after the last. It is a common
contest idiom: the condition is `0` or `1`, used to index a two-character string.

### The loop

On Linux, macOS, WSL or Git Bash:

```bash
#!/bin/bash
g++ -std=c++20 -O2 -o gen gen.cpp
g++ -std=c++20 -O2 -o brute brute.cpp
g++ -std=c++20 -O2 -o sol sol.cpp

for i in $(seq 1 10000); do
    ./gen $i > in.txt
    ./sol   < in.txt > out_sol.txt
    ./brute < in.txt > out_brute.txt
    if ! diff -q out_sol.txt out_brute.txt > /dev/null; then
        echo "FAILED on seed $i"
        echo "--- input ---";    cat in.txt
        echo "--- yours ---";    cat out_sol.txt
        echo "--- correct ---";  cat out_brute.txt
        break
    fi
done
echo "done"
```

That is the whole thing. Ten thousand cases run in a few seconds because each one is five numbers.

In PowerShell, if you are not using WSL:

```powershell
for ($i = 1; $i -le 10000; $i++) {
    .\gen.exe $i > in.txt
    .\sol.exe   < in.txt > out_sol.txt
    .\brute.exe < in.txt > out_brute.txt
    if (Compare-Object (Get-Content out_sol.txt) (Get-Content out_brute.txt)) {
        Write-Host "FAILED on seed $i"; Get-Content in.txt; break
    }
}
```

**Save this once and reuse it forever.** The only things that change per problem are the generator
and the brute force.

### What to do when it stops

You now have a five-number input where your solution is wrong. Three steps:

1. **Work the case out by hand** and confirm the brute force is the one that is right. Sometimes it
   is your brute force that is wrong, and you have learned something anyway.
2. **Shrink it further.** Change n from 5 to 3 in the generator and run again. A three-element
   failing case is usually enough to see the bug without any debugging at all.
3. **Only then look at your code**, with a specific question — "why does this return 4 on `[2,2,2]`"
   — instead of the useless general one, "where is the bug".

### Reading the judge's verdict

Before you stress test, read what the judge told you. Each verdict points somewhere specific.

| Verdict | Means | Check first |
|---|---|---|
| **WA** wrong answer | output differs on some test | stress test. And re-read the statement — it is often a misread, not a bug |
| **TLE** time limit | too slow, or an endless loop | is your complexity right for the constraint? Is fast I/O on? Passing containers by value? An endless `while`? |
| **RE** runtime error | crashed, or returned non-zero | out of range, division by zero, stack overflow from deep recursion, `top()` on an empty container |
| **MLE** memory limit | allocated too much | do the table arithmetic. 10^8 ints is 400 MB |
| **PE** presentation | right values, wrong formatting | trailing spaces, missing newline, wrong case in "YES" |
| **IL** idleness limit | interactive problem, you did not flush | you needed `endl` or `cout.flush()` |

Three of those are worth expanding.

**WA on test 1** is almost never a subtle bug. It means you misread the problem, printed the wrong
thing, or got the output format wrong. Re-read the statement before you touch the code.

**WA on a late test but not the samples** is the stress-test case.

**RE where you expected WA** is very often stack overflow from recursion — which
[day 125](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md) covers — or reading past the
end of a container, which `-fsanitize=address` finds in one run.

### `assert` — the cheapest tool here

```cpp
#include <cassert>
assert(k <= n);
assert(!v.empty());
```

If the condition is false the program stops and tells you where:

```
sol: sol.cpp:24: int main(): Assertion `k <= n' failed.
Aborted (core dumped)
```

Put asserts on the things you believe about your own data — array bounds, non-empty containers,
values in range. A failed assert turns a mysterious wrong answer into a named line number. Compile
them out with `-DNDEBUG` if you ever need the speed, but on a judge an assert failure shows as a
runtime error, which is a much clearer signal than a wrong answer.

### The compile command, one last time

```
g++ -std=c++20 -g -Wall -Wextra -fsanitize=address,undefined -o sol sol.cpp && ./sol < in.txt
```

`-fsanitize=address,undefined` finds out-of-range access, use-after-free, memory leaks, signed
overflow, and shifts past the width of a type — every trap in this track — and names the exact
line. It makes the program two to three times slower, so it is for local runs only, never for
submission.

**Use it every single time you run locally.** It costs nothing you care about and it converts the
worst class of bug in C++ into a line number.

---

## 4. The picture

The loop:

```
                  +----------------+
     seed i --->  |    gen.cpp     |  ---> in.txt   (n <= 5, values <= 4)
                  +----------------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
      +---------------+       +---------------+
      |    sol.cpp    |       |   brute.cpp   |
      |  fast, clever |       |  slow, simple |
      |    SUSPECT    |       |   TRUSTED     |
      +---------------+       +---------------+
              |                       |
          out_sol.txt            out_brute.txt
              |                       |
              +-----------+-----------+
                          v
                       +------+
                       | diff |
                       +------+
                        /    \
                  same /      \ different
                      /        \
            next seed            STOP.
                                 print the input.
                                 it has five numbers in it.
```

**What to notice:** nothing here understands the problem. The loop has no idea what you are
computing. It only knows that two programs which should agree do not — which is exactly what Ashok
and Nikhil have, and it is enough.

Why small inputs win, drawn as the thing you end up staring at:

```
  generator with n <= 1000, values <= 10^9

      FAILED on seed 3391
      --- input ---
      847
      918273645 12938471 5 662891234 ... (843 more numbers)
      --- yours ---   9182736451
      --- correct --- 9182736450

      now you have a second problem to solve.


  generator with n <= 5, values <= 4

      FAILED on seed 12
      --- input ---
      3
      2 2 1
      --- yours ---   4
      --- correct --- 3

      you can do this one in your head.  And "2 2 1" is telling you
      something: the bug involves a repeated value.
```

**What to notice:** the small case is not just easier to read. Its *shape* is a clue. `2 2 1`
appearing as the smallest failure says the bug is about ties, and you often know what is wrong
before opening the file.

---

## 5. The code, built step by step

A worked example, end to end. The problem: **given n numbers, find the largest sum of a
subsequence with no two adjacent elements taken.** That is house robber, from
[day 146](../day-146-house-robber/README.md).

### The solution you suspect

```cpp
// sol.cpp — the O(n) DP. Fast, and it has a bug in it on purpose.
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;
    if (n == 0) { cout << 0 << "\n"; return 0; }

    long long take = a[0], skip = 0;
    for (int i = 1; i < n; i++) {
        long long new_take = skip + a[i];
        long long new_skip = take;              // BUG: should be max(take, skip)
        take = new_take;
        skip = new_skip;
    }
    cout << max(take, skip) << "\n";
    return 0;
}
```

That bug is realistic — it is the kind of thing you write at minute forty of a contest, and it
passes small hand-made tests.

### The brute force

Write it stupidly. Do not be clever. Its only job is to be right.

```cpp
// brute.cpp — try every subset. O(2^n). Correct by construction.
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;

    long long best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        if (mask & (mask >> 1)) continue;       // two adjacent bits set -> not allowed
        long long sum = 0;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i)) sum += a[i];
        best = max(best, sum);
    }
    cout << best << "\n";
    return 0;
}
```

`mask & (mask >> 1)` is non-zero exactly when two adjacent bits are both set — which is
[day 171's](../day-171-binary-and-bits/04-cpp-shifts-builtins.md) bit trick doing the adjacency
check in one operation. At n ≤ 5 this examines thirty-two subsets, which is instant.

**Write the brute force by a different route from the real one.** If both are DP with the same
recurrence, they will share the same bug and agree with each other all day. Ashok is useful
because he scores differently, not because he scores twice.

### The generator

```cpp
// gen.cpp — one small random case. Seeded, so failures are reproducible.
#include <bits/stdc++.h>
using namespace std;
int main(int argc, char* argv[]) {
    mt19937 rng(atoi(argv[1]));
    int n = rng() % 5 + 1;                 // 1..5 — deliberately tiny
    cout << n << "\n";
    for (int i = 0; i < n; i++)
        cout << rng() % 5 << " \n"[i == n - 1];   // values 0..4 — ties are common
    return 0;
}
```

### The runner

```bash
#!/bin/bash
# stress.sh — save this once and reuse it for every problem.
set -e
g++ -std=c++20 -O2 -o gen   gen.cpp
g++ -std=c++20 -O2 -o brute brute.cpp
g++ -std=c++20 -O2 -o sol   sol.cpp

for i in $(seq 1 10000); do
    ./gen "$i" > in.txt
    ./sol   < in.txt > out_sol.txt
    ./brute < in.txt > out_brute.txt
    if ! diff -q out_sol.txt out_brute.txt > /dev/null; then
        echo "FAILED on seed $i"
        echo "--- input ---";   cat in.txt
        echo "--- yours ---";   cat out_sol.txt
        echo "--- correct ---"; cat out_brute.txt
        exit 1
    fi
    [ $((i % 500)) -eq 0 ] && echo "  $i cases ok"
done
echo "10000 cases, no disagreement"
```

### What it prints

```
$ bash stress.sh
FAILED on seed 7
--- input ---
4
3 1 1 4
--- yours ---
7
--- correct ---
7
```

— no, it agrees there. It stops a little later:

```
FAILED on seed 23
--- input ---
5
2 1 1 1 3
--- yours ---
5
--- correct ---
6
```

Five numbers. Work it out by hand: take positions 0, 2 and 4 — that is 2 + 1 + 3 = 6, and no two
are adjacent. Your program said 5. Now look at the loop with a specific question, and
`new_skip = take` is visibly wrong: skipping element `i` should keep the best of *either* previous
state, not just the one where you took the last element. `max(take, skip)` fixes it, the loop runs
ten thousand cases clean, and the whole exercise took four minutes.

### When the two programs disagree on formatting, not values

If the answer is a `double`, `diff` is the wrong comparison — `3.0000000001` and `3.0` are both
correct and differ as text. Compare with a tolerance instead:

```bash
./sol < in.txt | awk -v ok="$(./brute < in.txt)" \
  '{ if (($1-ok)^2 > 1e-12) { print "MISMATCH", $1, ok; exit 1 } }'
```

The same applies when a problem has several valid answers — "print any shortest path". Then a
plain `diff` is useless and you need a **checker**: a fourth program that reads the input and your
output and verifies your answer is valid, rather than comparing it with someone else's.

---

## 6. What it costs

### How long the loop takes

```
  per case:  3 process launches + 3 tiny runs   ≈ 3 milliseconds

  10,000 cases  x  3 ms  =  30 seconds
   1,000 cases  x  3 ms  =   3 seconds
```

Almost all of that is starting processes, not running your code, because the cases are five numbers
long. **A thousand cases in three seconds** is the practical loop, and if a thousand tiny random
cases do not find it, the bug is probably not a logic bug — it is an overflow, a limit, or a
misread statement.

### Why small inputs find bugs faster

Most bugs live at a boundary — a tie, a repeat, an empty case, a single element. So the question is
how often a random case *contains* a boundary.

```
  values drawn from 0..4, n = 5
    probability that some two values are equal:  about 96%
    ties happen in nearly every case.

  values drawn from 0..10^9, n = 5
    probability that some two values are equal:  about 0.000001%
    you will never generate a tie.

  and for the empty / single-element boundary, with n drawn from 1..5:
    n == 1 in 20% of cases  ->  seen within the first handful
  with n drawn from 1..1000:
    n == 1 in 0.1% of cases ->  1,000 cases to see it once
```

**That is the entire argument for tiny generators.** It is not about readability alone; it is that
small ranges make the interesting cases common instead of astronomically rare.

### What it costs to set up

```
  first time, on a new problem:
    write brute.cpp     3-5 minutes   (it is meant to be dumb)
    write gen.cpp       1-2 minutes
    reuse stress.sh     0 minutes     (you saved it)
    ------------------------------
    total               ~5 minutes

  compare with: re-reading a 60-line solution looking for a bug you
  already believe is not there — routinely 30+ minutes, often unsuccessful.
```

The break-even is about five minutes. **If you have been staring for more than five minutes, stop
staring and write the generator.**

---

## 7. The traps

### The near-miss: the brute force has the same bug

```cpp
// sol.cpp   — DP, with an error in the recurrence
// brute.cpp — the SAME DP, written slightly differently
```

They agree on ten thousand cases and both are wrong. You have proved nothing, and worse, you now
believe your solution is correct.

**The brute force must reach the answer by a different route.** If the real solution is DP, the
brute force should be exhaustive search. If the real solution is a clever formula, the brute force
should simulate. If the real solution is a greedy, the brute force should try every order. The
whole value is in the independence — Ashok is useful because he scores by a different method, not
because he scores twice.

### The near-miss: the generator never makes the hard case

```cpp
int n = rng() % 100 + 50;        // n is always 50..149 — never 1, never 2
int x = rng() % 1000000 + 1;     // always positive — never 0, never negative
```

The loop runs a hundred thousand clean cases and the judge still says wrong answer, because the
failing test has n = 1, or a zero, or a negative number, and your generator cannot produce one.

**Read the constraints and make the generator match them, including the edges.** If the statement
allows `a[i] = 0`, generate zeros. If it allows negatives, generate negatives. If `n` can be 1,
make `n` be 1 sometimes. A generator that only makes comfortable cases is testing nothing.

### The near-miss: no seed, or the wrong random source

```cpp
srand(time(0));
int n = rand() % 5 + 1;
```

Two problems. Seeding from the clock means the failing case is **irreproducible** — the loop stops,
prints the input, and then you can never generate it again to test your fix. And `rand()` is a poor
generator whose low bits are notoriously non-random on some implementations, so `rand() % 2` can
alternate.

**Use `mt19937` seeded from `argv[1]`.** Reproducibility is the whole point: once you know it is
seed 23, you can run seed 23 as many times as you like.

### The real error: an assert that fires

```cpp
assert(k <= n);
```

```
sol: sol.cpp:24: int main(): Assertion `k <= n' failed.
Aborted (core dumped)
```

This is a *good* outcome, not a bad one. It has converted "wrong answer somewhere" into "line 24,
and `k` exceeded `n`". Put asserts on everything you believe about your own data, especially
container bounds, and leave them in — on a judge an assert failure shows as a runtime error, which
tells you far more than a wrong answer does.

### The one stress testing cannot find

```cpp
long long total = 0;
for (int x : a) total += 1LL * x * x;    // fine
int wrong = 0;
for (int x : a) wrong += x * x;          // overflows only when values are large
```

With a generator making values under 5, this never overflows and the stress test runs clean
forever. The bug only appears at the real constraints.

**Stress testing finds logic bugs. It does not find overflow, memory limits, or timeouts** —
because all three only appear at full size. Those are found by different tools: the arithmetic from
[day 002](../day-002-counting-steps/04-cpp-types-numbers.md), the memory sum from
[day 143](../day-143-what-dp-is/04-cpp-dp-tables.md), and one deliberately maximal test:

```cpp
// maxgen.cpp — one case at the stated limits, to time it and check the memory
int n = 200000;
cout << n << "\n";
for (int i = 0; i < n; i++) cout << 1000000000 << " \n"[i == n - 1];
```

Run that once, with `time ./sol < max.txt`. It answers TLE and MLE in one go, and it takes thirty
seconds to write.

### The one from day 001, which still catches people

You fix the bug, run `./stress.sh`, and it fails on the same seed with the same output.

You edited `sol.cpp` and the script rebuilt it — unless you were running `./sol` by hand outside
the script, in which case **you are running the old binary**. The `&&` habit from
[day 001](../day-001-how-your-code-actually-runs/04-cpp-compiling-and-running.md) exists for
exactly this:

```
g++ -std=c++20 -O2 -o sol sol.cpp && ./sol < in.txt
```

---

## 8. In the interview

### How it gets asked

- *"Your solution fails on a test you cannot see. What do you do?"* — the direct version.
- *"How do you know your code is correct?"* — the general version, in a design or a coding round.
- *"You've written this in five minutes — how would you test it?"* — asked at the end of a live
  coding round, and a lot of candidates have nothing to say.
- *"What's the difference between a wrong answer and a runtime error telling you?"* — the
  competitive-programming-specific one.

### What to say out loud, in the first ninety seconds

1. **Read the verdict first.** *"First I'd use what the judge told me. Wrong answer on test 1 is
   usually a misread statement or an output format problem, not a logic bug — so I re-read the
   statement before touching the code."*
2. **Rule out the size-dependent failures.** *"Then I'd check the things a small test cannot show:
   does any sum or product overflow an `int`, does my table fit in the memory limit, is my
   complexity right for the constraint."*
3. **Name the technique.** *"If it is a genuine logic bug, I stress test. I write a second solution
   that is obviously correct and far too slow, a generator that makes tiny random cases, and a loop
   that compares them until they disagree."*
4. **Say why tiny.** *"Tiny is the important part — n up to five, values up to four. That makes the
   failing case small enough to work out by hand, and it makes ties and repeats common, which is
   where most bugs live."*
5. **Say why independent.** *"The brute force has to reach the answer a different way — exhaustive
   search against a DP, say. If I write the same approach twice I reproduce the same bug and prove
   nothing."*
6. **Name the tooling.** *"And I compile locally with `-fsanitize=address,undefined`, which turns
   out-of-range access, use-after-free and signed overflow into a line number instead of a wrong
   answer."*

Step 1 is the one that marks you out. Everybody jumps to debugging; reading the signal you were
already given is faster and free.

### The follow-ups

**"How do you know the brute force is right?"**
Because it is written to be obvious rather than fast — exhaustive search over every subset, or a
direct simulation of the process the statement describes. It has no optimisation in it, so there is
almost nothing to get wrong. I also check it against the provided samples first, before trusting
it. And if the stress test does find a disagreement, my first step is to work the tiny case out by
hand and confirm which of the two is actually right — sometimes it is the brute force that is
wrong, and I have still learned something, because now I know one of my two mental models of the
problem is broken.

**"What does a runtime error tell you that a wrong answer doesn't?"**
That the program stopped rather than finished, which narrows things a lot. In C++ the common causes
are reading past the end of a container, dividing by zero, stack overflow from recursion that is
too deep, and calling `top()` or `front()` on an empty container. The useful thing is that all of
those are found by `-fsanitize=address` in a single local run, with the exact line — whereas a
wrong answer gives you no location at all. So I would rather get a runtime error than a wrong
answer. That is also why I leave `assert` statements in: a failed assert turns a silent wrong
answer into a named line number, at the cost of showing as a runtime error on the judge.

**"When does stress testing not work?"**
Three cases. When the bug only appears at full size — overflow, memory, or a timeout — because a
generator making five small numbers will never trigger any of them; those need one deliberately
maximal test and the arithmetic done by hand. When there are several valid answers, like "print any
shortest path", because then comparing against another program's output is meaningless and I need a
checker that verifies my output is valid instead. And for interactive problems, where there is no
fixed input to generate — those need a simulated judge, which is more work than it is usually
worth.

**"How does this transfer outside competitive programming?"**
It is property-based testing, which is a real technique with real libraries — Hypothesis in Python,
QuickCheck in Haskell, RapidCheck in C++. The idea is identical: rather than writing example-based
tests by hand, you state a property that must always hold, generate random inputs, and let the
machine find a counterexample. The one thing those libraries add that a hand-rolled stress test
lacks is **shrinking** — when they find a failing case they automatically reduce it to the smallest
one that still fails, which is what I am doing by hand when I turn the generator's n down from five
to three.

### A model answer

> "The first thing I would do is not debug at all — I would use the information the verdict already
> gives me.
>
> If it were wrong answer on test 1, I would assume I have misread the statement or got the output
> format wrong, because a subtle logic bug almost never fails the first test. Failing at test 14
> means the samples and the first thirteen tests pass, so the shape of the solution is broadly
> right and something specific is wrong.
>
> Before writing any test infrastructure I would check the three things a small test can never
> reveal. Whether any sum or product overflows a 32-bit `int` — that is the most common cause of a
> late wrong answer in C++, and a sum of 10^5 values at 10^5 each is already 10^10. Whether my
> table fits the memory limit. And whether my complexity actually fits the constraint, because a
> late wrong answer is sometimes a timeout in disguise on a judge that reports them oddly.
>
> If those are clean, it is a logic bug and I stress test. Three programs: my real solution; a
> brute force written to be obviously correct and as slow as I like, because it only has to handle
> n = 5; and a generator that produces one tiny random case from a command-line seed. Then a shell
> loop that runs both on each generated case and stops the moment they disagree.
>
> Two details matter more than the rest. The generator has to make *tiny* cases — n up to five,
> values up to four. That is partly so the failing case is small enough to reason about by hand,
> and mostly because most bugs are at boundaries: ties, repeats, single elements. With values from
> zero to four, nearly every case has a tie; with values up to 10^9, I would never generate one. And
> the brute force has to reach the answer by a *different route* from the real solution — exhaustive
> search against a DP. If I write the same approach twice, I reproduce the same bug and the two
> agree happily while both are wrong.
>
> A thousand cases runs in about three seconds, and when it stops I have a five-number input where
> I know the right answer and my answer. That is usually solvable by inspection.
>
> Separately, I compile locally with `-fsanitize=address,undefined` as a habit. It converts
> out-of-range access, use-after-free and signed overflow from a silent wrong answer into a line
> number, and it costs nothing except local run time."

That answer starts by using free information, rules out the size-dependent failures first, names
the technique, gives the two details that make it work and the reasons for both, quantifies the
cost, and adds the tooling.

---

## 9. Recall card

1. **Read the verdict before debugging.** WA on test 1 is a misread statement. RE is usually
   out-of-range or stack overflow. TLE is complexity or missing fast I/O. MLE is table arithmetic.
2. **Stress test = three programs and a loop.** `sol` (fast, suspect), `brute` (slow, obviously
   correct), `gen` (tiny random case, seeded from `argv[1]`), and `diff` until they disagree.
3. **Make the cases tiny — n ≤ 5, values ≤ 4.** Not for readability alone: small ranges make ties
   and repeats common, and that is where the bugs are.
4. **The brute force must use a different method**, or it shares the bug and proves nothing.
   Exhaustive search against DP, simulation against a formula.
5. **Stress testing cannot find overflow, MLE or TLE** — those need one deliberately maximal test
   and the arithmetic done by hand. And run everything locally under
   `-fsanitize=address,undefined`.

---

## The twelve C++ days, in order

That is the track.

| Day | Lesson |
|---:|---|
| [001](../day-001-how-your-code-actually-runs/04-cpp-compiling-and-running.md) | Compiling and running your first program |
| [002](../day-002-counting-steps/04-cpp-types-numbers.md) | Types, numbers, and the overflow that costs contests |
| [003](../day-003-big-o-in-plain-english/04-cpp-input-output.md) | Input, output, and the competitive template |
| [005](../day-005-python-lists-and-tuples/04-cpp-vector-references.md) | `vector`, references, and the array you use for everything |
| [006](../day-006-python-strings-dicts-sets/04-cpp-string-map-set.md) | `string`, `map`, `set`, and `pair` |
| [042](../day-042-binary-search-idea/04-cpp-sort-lambdas.md) | `sort`, lambdas, and `lower_bound` |
| [068](../day-068-stacks/04-cpp-stack-queue-deque.md) | `stack`, `queue`, `deque`, and `priority_queue` |
| [078](../day-078-nodes-and-links/04-cpp-structs-pointers.md) | structs, pointers, and building your own nodes |
| [125](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md) | Graphs and recursion: adjacency lists, depth, and DSU |
| [143](../day-143-what-dp-is/04-cpp-dp-tables.md) | DP tables, and the contest traps that are left |
| [171](../day-171-binary-and-bits/04-cpp-shifts-builtins.md) | Shifts, builtins, and bitset |
| **178** | Stress testing, and reading a judge's verdict |

Twelve days out of a hundred and eighty, and they are enough to solve every problem in this course
in C++ and to compete seriously.

What they are not is enough for a C++-specific **design** round: classes and RAII, virtual
functions and vtables, `unique_ptr` and `shared_ptr` ownership, SOLID and the design patterns in
C++. The course teaches all of those ideas in the system design track from
[day 043](../day-043-binary-search-without-bugs/README.md) onwards, in Python. If your interviews
will be in C++, translate those days as you go — the same way this track has had you translating
the DSA days.

For practice: Codeforces Div. 3 and Div. 4 first, then Div. 2 A and B. AtCoder Beginner Contests
are gentler and better written. Read the constraint before you read the statement, use the template
from [day 003](../day-003-big-o-in-plain-english/04-cpp-input-output.md), and keep `stress.sh` in
the same folder as everything else.
