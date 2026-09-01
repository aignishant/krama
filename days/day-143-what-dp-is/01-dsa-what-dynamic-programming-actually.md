---
day: 143
track: dsa
title: "What dynamic programming actually is"
phase: "Dynamic programming"
status: written
---

# What dynamic programming actually is

## 1. What this is, and why they ask it

Dynamic programming is recursion plus memory. That is the whole definition, and everything else in the next
twenty days is a variation on it.

You already write recursion. You break a problem into smaller versions of itself and combine the answers.
What goes wrong — and what makes some recursive solutions take longer than the age of the universe — is that
the same smaller problem gets solved again and again through different routes. **DP is what you do about
that: solve each distinct subproblem once, write the answer down, and look it up thereafter.**

That is it. There is no cleverness in the definition. The difficulty of DP, and the reason it has a
reputation, is entirely in one step: **deciding what the subproblem is.** Once you can say "`dp[i]` means
___" as a complete sentence, the rest is mechanical.

They ask about DP constantly — it is probably the most common Hard-tagged category — and the first question
is almost always the same shape: *"why is this exponential, and how do you fix it?"* The interviewer wants to
see you write the naive recursion, notice the repetition, and add memory. **Not to leap straight to a table**,
which is where people get lost.

By the end of this lesson you can recognise the two conditions that make DP apply, write the recursion first
and add memory second, convert between the top-down and bottom-up forms, count how much work the naive
version wastes, and say what the state means as a sentence.

---

## 2. The story

There are twelve steps from Kaushalya's kitchen up to the terrace, and her grandson has decided he can go up
them taking either one step or two, and now he wants to know how many different ways there are.

She is seventy-one and she has been doing accounts for a family business since 1978, so she does not think
this is a silly question. She sits down on the third step and starts working it out.

She starts from the top, which turns out to be the right way round.

To get to step twelve, she has to have come from step eleven or step ten. So the number of ways to reach
twelve is the number of ways to reach eleven, plus the number of ways to reach ten. Fine. Now she needs eleven.
To reach eleven she must have come from ten or nine. So she needs ten and nine. To reach ten, nine or eight.

Ten minutes later she is annoyed.

She has worked out the number of ways to reach step eight **four separate times**. Once because eleven needed
ten which needed nine which needed eight. Once because eleven needed nine which needed eight. Once through a
different chain from ten. And once more from somewhere she has lost track of. Every time she got the same
answer, obviously, because it is the same question, and every time she did the whole thing from scratch
because she had not thought to hold on to it.

So she does the sensible thing, which she has been doing with invoices for forty years without ever calling it
anything.

She takes a piece of chalk from the shelf where the boy keeps it and writes on the step itself. On step one
she writes 1. On step two she writes 2. Then on step three: one plus two, three. On step four: two plus three,
five. Step five: eight.

Now she is not remembering anything and not working anything out twice. Each step needs only the two below
it, and both of those are already written on the steps, in front of her, where she can see them.

Twelve steps takes her about ninety seconds and the answer is two hundred and thirty-three.

Her grandson is unimpressed, having lost interest around step six.

What stays with her is not the number. It is that the second method was not cleverer than the first. It was
**the same method, with the answers written down instead of re-derived**, and that one change turned ten
minutes of increasing confusion into ninety seconds of arithmetic.

---

## 3. The idea in plain English

Kaushalya's chalk is dynamic programming, and her ten minutes of annoyance is why it exists.

**The recursion comes first, and it is usually easy.** To reach step 12, you came from 11 or from 10. So:

```
ways(12) = ways(11) + ways(10)
ways(n)  = ways(n-1) + ways(n-2)
ways(1)  = 1,   ways(2) = 2
```

**That is the whole problem, expressed.** The thing you write down first is not code, it is this — the
**recurrence**, which is a sentence saying how a bigger answer is built from smaller ones, plus the **base
cases**, which are the answers small enough to know outright.

**Written directly as a function, it is correct and catastrophically slow.** Not slightly slow. `ways(50)`
makes about two and a half billion calls, because the tree of calls branches twice at every level and never
notices that it is asking the same questions over and over.

**Those repeated questions are the whole opportunity, and they have a name: overlapping subproblems.**
Kaushalya computing step 8 four times. `ways(8)` is needed by `ways(9)` and by `ways(10)`, and both of those
are needed higher up, so the same call happens again and again down different branches.

**DP is: write each answer down the first time you compute it, and look it up afterwards.** That is
memoisation, and it turns two and a half billion calls into fifty.

**Two conditions have to hold for this to work**, and being able to state them is what "recognising DP" means:

**One: optimal substructure.** The answer to the big problem is built from answers to smaller versions of the
*same* problem. Ways-to-reach-12 is genuinely made out of ways-to-reach-11 and ways-to-reach-10 — you do not
need to know *how* you got to step 11, only how many ways there are.

**Two: overlapping subproblems.** The same smaller problem comes up repeatedly. If every subproblem were
different, memory would buy you nothing, and you would have plain divide-and-conquer — which is what merge
sort is. **That is the difference between DP and divide-and-conquer: whether the subproblems repeat.**

**And the state is the thing to get right.** The **state** is what identifies a subproblem — the arguments to
the recursive function. For the stairs it is one number: which step. **`dp[i]` = the number of ways to reach
step `i`.** Say it as a full sentence, out loud, before writing anything. If you cannot, you do not have the
state yet, and [day 147](../day-147-finding-the-state/README.md) is entirely about that.

**There are two forms and they compute the same thing.**

**Top-down, or memoised recursion:** write the recursion exactly as you derived it, and add a cache. You keep
the shape of your thinking, you only compute the subproblems you actually need, and it is much easier to get
right the first time.

**Bottom-up, or tabulation:** work out the order in which subproblems depend on each other, and fill an array
from the smallest upwards. That is Kaushalya's chalk on the steps. No recursion, so no stack limit, usually a
little faster, and it makes the space optimisation obvious.

**Write top-down first.** In an interview, derive the recurrence, code it recursively, add `@lru_cache`, and
*then* offer the bottom-up version. **Trying to write a table before you have the recurrence is how people get
stuck**, because the table is a consequence of the recurrence, not a substitute for it.

**The last idea, and it is the one that makes DP feel like a trick when it should not: the table is often
smaller than it looks.** Kaushalya only ever needs the two steps below the one she is on, so she does not need
twelve numbers, she needs two. That is [day 161](../day-161-dp-space-optimisation/README.md), and it is worth
knowing now that it exists, so you are not surprised when a two-dimensional table collapses into one row.

---

## 4. The picture

The naive call tree for `ways(6)`, with the repetition marked:

```
                        ways(6)
                     /          \
              ways(5)            ways(4)*
             /       \           /      \
       ways(4)*   ways(3)*  ways(3)*  ways(2)
        /    \      /   \     /   \
   ways(3)* ways(2) w(2) w(1) w(2) w(1)
    /    \
 w(2)   w(1)

  ways(4) computed 2 times
  ways(3) computed 3 times
  ways(2) computed 5 times
  ways(1) computed 3 times

  total calls for ways(6):  15
  total calls for ways(50): ~2,500,000,000
```

**What to notice.** The tree branches twice at every level, so it has about `2^n` nodes — but there are only
`n` *distinct* questions in it. **That gap between `2^n` calls and `n` distinct answers is exactly the waste
DP removes.**

The same computation with memory:

```
                        ways(6)
                     /          \
              ways(5)            [ways(4)]      <- cached, returns instantly
             /       \
       ways(4)      [ways(3)]                   <- cached
        /    \
   ways(3)   [ways(2)]                          <- cached
    /    \
 ways(2)  ways(1)

  6 real computations, 4 cache hits.
  total calls for ways(50): 50 computations.
```

Kaushalya's chalk, which is the bottom-up form:

```
  step:    1   2   3   4   5   6   7   8   9  10  11  12
  chalk:   1   2   3   5   8  13  21  34  55  89 144 233
                   ^
                   |
              1 + 2, and every number after it
              is the two before it added

  each cell computed ONCE, in order, reading only what is already written
```

And the two forms side by side, computing the same thing:

```
  TOP-DOWN (memoised recursion)          BOTTOM-UP (tabulation)

  start at 12, recurse downwards          start at 1, build upwards
  the cache fills as you unwind           the array fills in order
  only the states you NEED                ALL states up to n
  natural to write from the recurrence    needs the dependency order worked out
  recursion depth = n                     no recursion at all
```

---

## 5. The code, built step by step

**Step one is always the recurrence, in words, before any code.**

> To reach step `n` I must have come from `n-1` or `n-2`. So `ways(n) = ways(n-1) + ways(n-2)`, with
> `ways(1) = 1` and `ways(2) = 2`.

Now write it exactly as stated:

```python
def ways(n: int) -> int:
    if n <= 2:
        return n                          # ways(1) = 1, ways(2) = 2
    return ways(n - 1) + ways(n - 2)
```

**Four lines, correct, and unusable past about `n = 40`.** Write this first anyway — it is the thing you are
about to fix, and in an interview it demonstrates that you have the recurrence right before you complicate it.

Now measure the damage:

```python
calls = 0

def ways_counted(n: int) -> int:
    global calls
    calls += 1
    if n <= 2:
        return n
    return ways_counted(n - 1) + ways_counted(n - 2)
```

```
n = 10  ->  109 calls
n = 20  ->  13,529 calls
n = 30  ->  1,664,079 calls
n = 40  ->  204,668,309 calls
```

**Each `+10` multiplies the work by roughly 123.** That is the shape of exponential growth, and seeing the
numbers is more convincing than the notation.

**Now add memory. One decorator:**

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways_memo(n: int) -> int:
    if n <= 2:
        return n
    return ways_memo(n - 1) + ways_memo(n - 2)
```

**The function body is byte-for-byte identical.** That is worth pointing at: the algorithm did not change,
only whether it remembers. `n = 40` goes from 204 million calls to 40.

The explicit version, for when the arguments are not hashable or you want to see the machinery:

```python
def ways_memo_manual(n: int, cache: dict[int, int] | None = None) -> int:
    if cache is None:
        cache = {}
    if n <= 2:
        return n
    if n in cache:
        return cache[n]                   # already solved: look it up
    cache[n] = ways_memo_manual(n - 1, cache) + ways_memo_manual(n - 2, cache)
    return cache[n]
```

**Three added lines: check, compute, store.** Every top-down DP has exactly this shape, and once you see it
you can add memory to any recursion in thirty seconds.

**Now bottom-up — Kaushalya's chalk.** The question is: in what order can I fill this so that everything I
read is already written?

```python
def ways_table(n: int) -> int:
    if n <= 2:
        return n
    dp = [0] * (n + 1)                    # dp[i] = ways to reach step i
    dp[1], dp[2] = 1, 2                   # base cases, written down first
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]     # reads only smaller indices
    return dp[n]
```

**`dp[i]` means "the number of ways to reach step `i`".** Write that as a comment. It is the single most
useful line in any DP solution, because six months later — or ten minutes later, under pressure — it is the
thing you will have forgotten.

The loop goes upwards because `dp[i]` reads `dp[i-1]` and `dp[i-2]`, so the smaller indices must be filled
first. **Working out that order is the only extra thinking bottom-up requires**, and it is why top-down is
easier to write first.

**And the space optimisation**, which is obvious once the table is in front of you:

```python
def ways_two_vars(n: int) -> int:
    if n <= 2:
        return n
    prev, curr = 1, 2                     # dp[i-2], dp[i-1]
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

**`O(n)` memory becomes `O(1)`**, because each cell only ever reads the two below it. The rest of the table
was never needed.

### The complete solution

```python
"""What dynamic programming is: the same recursion, with and without memory."""

from __future__ import annotations

import time
from functools import lru_cache


def ways_naive(n: int) -> int:
    """The recurrence, written directly. Correct. O(2^n)."""
    if n <= 2:
        return n
    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n: int) -> int:
    """The SAME body. One decorator. O(n)."""
    if n <= 2:
        return n
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_table(n: int) -> int:
    """Bottom-up. dp[i] = the number of ways to reach step i. O(n) time, O(n) space."""
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def ways_optimised(n: int) -> int:
    """Only the last two cells are ever read. O(n) time, O(1) space."""
    if n <= 2:
        return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


def count_calls(n: int) -> int:
    """How many calls the naive version makes."""
    calls = 0

    def go(k: int) -> int:
        nonlocal calls
        calls += 1
        if k <= 2:
            return k
        return go(k - 1) + go(k - 2)

    go(n)
    return calls


if __name__ == "__main__":
    print("all four agree:", [f(12) for f in (ways_naive, ways_memo, ways_table, ways_optimised)])
    print()

    print("  n   naive calls        distinct subproblems")
    for n in (10, 20, 30, 35):
        print(f"{n:3}   {count_calls(n):>12,}   {n:>12}")
    print()

    start = time.perf_counter()
    ways_naive(32)
    naive_time = time.perf_counter() - start
    start = time.perf_counter()
    ways_optimised(32)
    fast_time = time.perf_counter() - start
    print(f"naive(32)     {naive_time * 1000:8.1f} ms")
    print(f"optimised(32) {fast_time * 1000:8.4f} ms")
    print(f"ratio         {naive_time / fast_time:8.0f}x")
    print()
    print("optimised(500) =", str(ways_optimised(500))[:40], "... (105 digits)")
```

Running it:

```
all four agree: [233, 233, 233, 233]

  n   naive calls        distinct subproblems
 10            109             10
 20         13,529             20
 30      1,664,079             30
 35     18,454,929             35

naive(32)       1893.4 ms
optimised(32)     0.0032 ms
ratio            591688x

optimised(500) = 2255915161619363308725126950360720720460 ... (105 digits)
```

Three things to look at. **All four functions agree**, which is the point — the algorithm never changed, only
whether it remembered.

**The two columns in the table are the whole lesson.** At `n = 35`, eighteen million calls to answer
thirty-five distinct questions. The ratio of those columns is what memory removes.

And `ways_optimised(500)` returns a 105-digit number instantly, while `ways_naive(500)` would not finish
before the sun burned out. **Same recurrence.**

---

## 6. What it costs

**The naive recursion.**

```
each call makes 2 more calls
depth n
                                    -> O(2^n) calls
```

More precisely, the number of calls follows the Fibonacci numbers themselves, so it grows by a factor of
about **1.618 per step** — the golden ratio — which is why `+10` multiplies the work by roughly 123.

```
n = 30    1,664,079 calls        ~0.5 s
n = 40    204,668,309            ~60 s
n = 50    ~25,000,000,000        ~2 hours
n = 100   ~10^21                 longer than the age of the universe
```

**With memoisation.**

```
distinct subproblems        n
work per subproblem         O(1)  (one addition)
                            -------------------
                            O(n) time
cache                       O(n) entries
recursion depth             O(n) frames
                            -------------------
                            O(n) space
```

**The general formula for any DP, and this is the one to memorise:**

```
time  = (number of distinct states) x (work per state)
space = (number of distinct states)   [before optimisation]
```

**That formula is how you cost a DP solution in an interview without thinking hard.** Count the states, count
the work inside one, multiply.

```
1D over n:            n states x O(1)      = O(n)
2D over n and m:      n*m states x O(1)    = O(n*m)
2D with a loop inside: n*m states x O(k)   = O(n*m*k)
subsets of n items:   2^n states x O(n)    = O(2^n * n)
```

**Bottom-up costs the same time and can cost less space:**

```
top-down     O(n) cache + O(n) recursion stack
bottom-up    O(n) array, no stack
optimised    O(1)   -- when each cell reads only a fixed window below it
```

**And the recursion depth is a real constraint on top-down:**

```
Python usable frames      ~960
n = 100,000               -> RecursionError

sys.setrecursionlimit(200_000)  -> Segmentation fault
```

**So: `n` up to a few thousand, top-down is fine and easier. Beyond that, bottom-up**, which is one of the
two real reasons to convert.

**What memory actually buys, in one comparison:**

```
n = 35
  naive        18,454,929 calls
  memoised             35 computations + 34 cache hits
                       -> ~270,000x fewer
```

**The space optimisation, sized:**

```
n = 1,000,000
  full table   1,000,000 Python ints in a list  ~40 MB
  two variables                                 ~56 bytes
```

**And the case where memoisation buys nothing** — worth knowing so you do not apply it reflexively:

```
merge sort: T(n) = 2*T(n/2) + O(n)
  subproblems: sort(0..4), sort(5..9), sort(0..9) ...
  every subproblem is DIFFERENT. Nothing repeats.
  -> a cache would fill with entries that are never read again
  -> that is divide-and-conquer, not DP
```

---

## 7. The traps

### Writing the table before the recurrence

The most common way to get stuck, and it does not produce an error — it produces an empty editor and a
stopped clock.

```python
dp = [[0] * (m + 1) for _ in range(n + 1)]
# ... now what?
```

**The table is a consequence of the recurrence, not a substitute for it.** Derive the recurrence in words
first — "to reach `i` I must have come from ___" — write it as plain recursion, check it on `n = 3` by hand,
and only then decide how to store the answers. Reversing that order is why DP feels impossible.

### No base case, or the wrong one

```python
@lru_cache(maxsize=None)
def ways(n):
    return ways(n - 1) + ways(n - 2)      # no base case
```

```
RecursionError: maximum recursion depth exceeded
```

And the subtler version — a base case that is off by one:

```python
if n <= 2:
    return 1                              # ways(2) is 2, not 1
```

```
>>> ways(12)
144                                       # should be 233
```

**No error, just a wrong number**, and it is off by exactly one position in the sequence. **Check the base
cases by hand on the smallest inputs**, always: `n = 1`, `n = 2`, and `n = 3`.

### Memoising on the wrong key

```python
@lru_cache(maxsize=None)
def solve(i, remaining, used_list):       # a list is not hashable
    ...
```

```
TypeError: unhashable type: 'list'
```

And the more dangerous version — a key that omits part of the state:

```python
cache = {}
def solve(i, budget):
    if i in cache:                        # keyed on i alone, but budget matters too
        return cache[i]
    ...
```

**No error, and confidently wrong answers**, because two genuinely different subproblems share a cache entry.
**The cache key must be the complete state** — every argument that can change the answer.

### Mutable default arguments

```python
def solve(n, cache={}):                   # shared across ALL calls, forever
    ...
```

The cache persists between separate top-level calls, which is sometimes what you want and usually a source of
mystifying test failures — the second test sees the first test's results. Use `cache=None` and create it
inside, or `@lru_cache`, or pass it explicitly.

### `lru_cache` on a method with `self`

```python
class Solution:
    @lru_cache(maxsize=None)
    def solve(self, n): ...
```

Works, and caches on `(self, n)` — so the cache lives as long as the object and keeps it alive. On a judge
that reuses the object across test cases, **results leak between tests**. Use a local function inside the
method, or `functools.cache` on a nested function, and the problem disappears.

### Recursion depth on a large `n`

```
Traceback (most recent call last):
  File "dp.py", line 6, in ways_memo
    return ways_memo(n - 1) + ways_memo(n - 2)
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Even with memoisation, the *first* call chain goes all the way down before anything is cached. `n = 100,000`
is a hundred thousand frames. **Bottom-up has no recursion at all**, which is one of the two reasons to
convert.

### Applying DP where subproblems do not overlap

```python
@lru_cache(maxsize=None)
def merge_sort(items_tuple):
    ...
```

Correct, and the cache never gets a hit, because every subproblem is a different slice. **You have added
memory overhead to divide-and-conquer.** The test is: *does the same subproblem come up more than once?* If
not, it is not DP.

### Integer overflow — in other languages

Python integers are unbounded, so `ways(500)` returns a 105-digit number. **In Java or C++ this overflows
silently at `n = 92`**, and problems that ask for an answer "modulo 10⁹+7" are telling you exactly that. Worth
knowing, because interviewers sometimes ask what changes in another language.

---

## 8. In the interview

### How it gets asked

- *"Why is this exponential, and how do you fix it?"* — the direct version, and the one this lesson answers.
- *"Write it top-down. Now write it bottom-up."* — [day 144](../day-144-fibonacci-dp/README.md).
- *"How many ways to climb `n` stairs taking one or two steps?"*
- *"What does `dp[i]` represent in your solution?"* — the state question, and the one that finds people out.
- *"Can you reduce the space?"*
- *"Is this DP or greedy?"* — [day 162](../day-162-recognising-dp/README.md).

### The first ninety seconds

> "Let me get the recurrence first and worry about efficiency second, because the recurrence is the problem
> and the efficiency is mechanical.
>
> **To reach step `n`, my last move was either one step or two steps. So I came from `n-1` or from `n-2`, and
> those are the only possibilities.** That means `ways(n) = ways(n-1) + ways(n-2)`, with `ways(1) = 1` and
> `ways(2) = 2` — one step in one way, two steps in two ways.
>
> Written directly that is four lines and it is correct. It is also `O(2^n)`, because the call tree branches
> twice at every level. At `n = 35` that is about eighteen and a half million calls — and there are only
> **thirty-five distinct questions** in the whole tree. `ways(8)` gets computed dozens of times through
> different branches.
>
> **That gap is the entire opportunity: exponentially many calls, linearly many distinct answers.** So I
> memoise — compute each one once, store it, look it up thereafter. In Python that is one decorator and the
> function body does not change at all, which I think is the clearest way to see that the algorithm is the
> same and only the remembering is new.
>
> `O(n)` time and `O(n)` space now, because there are `n` states and each costs one addition. **The general
> formula is states times work per state**, and that is how I would cost any DP.
>
> **Then two improvements I would offer.** Bottom-up: fill an array from 1 upwards, because `dp[i]` only reads
> smaller indices — same complexity, no recursion, and no depth limit, which matters if `n` can be a hundred
> thousand. And then the space: each cell reads only the two below it, so I never need the array at all — two
> variables, `O(1)` space.
>
> **And the sentence I would write as a comment before anything else** is what `dp[i]` means: the number of
> distinct ways to reach step `i`. If I cannot say that, I do not have the state yet."

### The follow-ups

**"Why is the naive version exponential? Be precise."**

> "Because the call tree branches twice at every level and never notices repetition.
>
> `ways(n)` calls `ways(n-1)` and `ways(n-2)`. Each of those does the same. So the tree has depth `n` and
> roughly two children per node, which is about `2^n` nodes. More precisely the call count follows the
> Fibonacci sequence itself, growing by a factor of about 1.618 per step — the golden ratio — so every ten
> steps multiplies the work by about a hundred and twenty.
>
> **The important part is the contrast.** That tree has exponentially many *nodes* and only `n` distinct
> *questions* in it, because the argument is a single integer between 1 and `n`. `ways(8)` appears in the tree
> dozens of times and gives the same answer every time.
>
> **So the fix is not a better algorithm, it is memory.** Solve each of the `n` distinct subproblems once,
> store the result, and return the stored one thereafter. Eighteen million calls become thirty-five
> computations and thirty-four lookups.
>
> **And that is what dynamic programming is** — recursion plus memory. The two conditions it needs are optimal
> substructure, meaning the big answer is built from smaller answers to the same problem, and overlapping
> subproblems, meaning those smaller problems repeat. **If they do not repeat, memory buys nothing and it is
> divide-and-conquer, not DP** — merge sort is the standard example, where every subproblem is a different
> slice and a cache would never get a hit."

**"Top-down or bottom-up? Which would you write?"**

> "Top-down first, always, and then convert if there is a reason.
>
> **Top-down is the recursion I already derived, plus a cache.** The code has the same shape as my reasoning,
> so it is much harder to get wrong under pressure. It also computes only the states I actually reach, which
> for a sparse state space can be a large saving — if the reachable states are a small fraction of the table,
> bottom-up fills the whole thing and top-down does not.
>
> **Two reasons to convert to bottom-up.** Recursion depth: even memoised, the first chain of calls goes all
> the way down before anything is cached, so `n = 100,000` is a hundred thousand frames and Python dies at
> about a thousand. And the space optimisation: with the table written out it is obvious that each row only
> reads the previous one, so I can drop from `O(n·m)` to `O(m)` — which is not obvious at all in the recursive
> form.
>
> **Bottom-up costs me one thing: I have to work out the fill order** so that everything a cell reads is
> already written. For a one-dimensional table that is trivial; for interval DP the order is by length rather
> than by index, and getting it wrong reads uninitialised cells and produces wrong answers with no error.
>
> **In an interview I would say all of that and then write the memoised version**, because deriving the
> recurrence in front of someone and adding a cache is a clearer demonstration than producing a table that
> appears from nowhere."

**"Reduce the space."**

> "Look at what each cell actually reads.
>
> Here `dp[i]` reads `dp[i-1]` and `dp[i-2]` and nothing else, so at any moment I need exactly two numbers.
> The rest of the array is history I will never look at again. Two variables, rolled forward — `O(n)` becomes
> `O(1)`.
>
> **The general rule is: keep a window as wide as the deepest thing the recurrence reaches back to.** If
> `dp[i]` depends on `dp[i-1]` through `dp[i-k]`, I need `k` values, not `n`.
>
> **In two dimensions the same argument gives a bigger win.** If `dp[i][j]` reads only row `i-1`, I keep two
> rows instead of `n` — `O(n·m)` becomes `O(m)`. And sometimes one row suffices, updating in place, though
> **the iteration direction then matters**: if the cell reads `dp[i-1][j-1]` I must go right to left, or I
> overwrite the value I am about to need. That is the classic knapsack subtlety and it is a silent wrong
> answer when it is wrong.
>
> **The one thing I would give up by optimising**: I can no longer reconstruct *which* choices produced the
> answer, only its value, because I threw away the table that recorded them. So if the problem wants the
> actual path or the actual subset, I keep the full table — or I store parent pointers, which costs the same
> memory I was trying to save. **I would ask whether the value alone is enough before optimising.**"

**"What does `dp[i]` represent?"**

> "The number of distinct ways to reach step `i`. And I would say that this question is the one that actually
> matters, more than the code.
>
> The state is what identifies a subproblem — the arguments to the recursive function, or the indices into the
> table. Getting it wrong is the main way DP solutions fail, and it fails silently: **if the state omits
> something that affects the answer, two genuinely different subproblems share a cache entry and the result is
> confidently wrong.**
>
> The test I use is: *given only the state, can I compute the answer without knowing anything else about how I
> got here?* For the stairs, knowing 'I am at step 8' is enough — the number of ways to finish from there does
> not depend on the route that reached it. If it did, the route would have to be part of the state.
>
> **The moment that test fails, the state needs another dimension.** 'Cheapest flight with at most `k` stops'
> is the standard example: the city alone is not enough, because reaching Delhi in two stops and in four stops
> are different situations with different futures. So the state becomes `(city, stops used)`.
>
> **And I would write it as a comment above the table**, as a full English sentence, before writing the loop.
> Not as documentation — as a check that I know what I am computing."

### The model answer

*"A robot is at the top-left of an `m × n` grid and can only move right or down. How many distinct paths are
there to the bottom-right? Then: some cells are blocked."*

> "Let me derive the recurrence before touching a table, because the table is the easy part.
>
> **To arrive at cell `(i, j)`, my last move was either from the left or from above** — those are the only two
> moves that end there. So the number of paths to `(i, j)` is the number of paths to `(i, j-1)` plus the number
> to `(i-1, j)`.
>
> **`dp[i][j]` = the number of distinct paths from the start to cell `(i, j)`.** I would write that as a
> comment first.
>
> **Base cases:** the first row can only be reached by moving right the whole way, so every cell in it has
> exactly one path; the same for the first column. And `dp[0][0] = 1` — one way to be where you started, which
> is worth stating because 'zero moves is one path' trips people up.
>
> **Why it is DP:** the same subproblem appears repeatedly. `dp[3][4]` is needed by `dp[3][5]` and by
> `dp[4][4]`, and those are needed further along — so the naive recursion recomputes the same cells
> exponentially many times, and there are only `m × n` distinct questions.
>
> **Cost: states times work per state.** `m × n` states, one addition each, so `O(m·n)` time and `O(m·n)`
> space.
>
> **The blocked-cells version changes one line and the base cases**, and that is the interesting part. A
> blocked cell has zero paths through it: `dp[i][j] = 0` if the cell is blocked, else the sum as before.
>
> **The base cases stop being trivial**, and this is where people go wrong. The first row is no longer all
> ones — once you hit a blocked cell, every cell after it in that row is unreachable along the row, so it is
> ones up to the obstacle and zeros after. Handling that by initialising with a loop that breaks at the first
> obstacle is clearer than special-casing inside the main loop.
>
> **And if the start or the end is itself blocked, the answer is zero**, which I would check first rather than
> discover through the arithmetic.
>
> **Space:** each row reads only the row above and the cell to the left, so I can keep one row and update it
> in place, going left to right — `O(n)` instead of `O(m·n)`. Direction matters: left to right is correct here
> because `dp[j]` should already hold the *new* value from the left and the *old* value from above, which is
> exactly what in-place left-to-right gives.
>
> **One thing worth mentioning for the unblocked version:** it has a closed form. The path is `m-1` downs and
> `n-1` rights in some order, so the answer is `C(m+n-2, m-1)` — a single binomial coefficient, `O(min(m,n))`
> to compute and no table at all. **I would mention it and still write the DP**, because the moment obstacles
> appear the formula is useless and the DP is not."

---

## 9. Recall card

**DP is recursion plus memory.** Two conditions: **optimal substructure** (the big answer is built from
smaller answers to the same problem) and **overlapping subproblems** (those smaller problems repeat). No
overlap means divide-and-conquer, not DP — a cache would never get a hit.

**Derive the recurrence in words first, write it as plain recursion, then add memory.** Writing the table
before the recurrence is how people get stuck. And **say what `dp[i]` means as a full sentence** before the
loop — if the state omits something that affects the answer, two subproblems share a cache entry and you get
a confident wrong number.

**Cost = (number of distinct states) × (work per state).** `n` states × `O(1)` is `O(n)`; `n·m` states with a
`k`-loop inside is `O(n·m·k)`.

**Top-down first:** same shape as your reasoning, and it only computes reachable states. **Convert to
bottom-up for two reasons only:** recursion depth (~960 frames in Python), and because the space optimisation
becomes obvious.

**The numbers:** naive stairs at `n=35` is 18.5 million calls for **35 distinct answers**; memoised it is 35
computations. And each cell reading only a fixed window below it means `O(n)` space collapses to `O(1)`.
