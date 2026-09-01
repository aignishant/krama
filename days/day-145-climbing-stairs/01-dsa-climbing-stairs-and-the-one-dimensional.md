---
day: 145
track: dsa
title: "Climbing stairs and the one-dimensional habit"
phase: "Dynamic programming"
status: written
---

# Climbing stairs and the one-dimensional habit

## 1. What this is, and why they ask it

Most dynamic programming problems you will meet are one-dimensional: a single index walking along an array or
a sequence, with one number stored per position. Climbing stairs, house robber, minimum cost climbing stairs,
decode ways, longest increasing subsequence, word break, jump game, maximum subarray. **Eight of the most
commonly asked DP problems are the same shape.**

And that shape has one habit that produces the recurrence every time, without insight:

> **What was the last move, and what state was I in before it?**

Ask that, enumerate the possible last moves, and the recurrence writes itself. It is not a trick and it is not
specific to stairs — it works on every problem in this family, and having it as a reflex is the difference
between a blank editor and a solution in four minutes.

They ask these constantly because they are short enough to finish in twenty minutes and because the interviewer
can watch you derive rather than recall. **The question that follows is always "what does `dp[i]` represent?"**,
and that is the real test.

By the end of this lesson you can apply the last-move habit to any linear problem, write the four-line
template that fits nearly all of them, choose the right base cases, recognise the three variations the family
comes in, and say why an answer sometimes lives somewhere other than `dp[n-1]`.

---

## 2. The story

Vimala realises the earring is gone while she is standing at the bus stop at Sion, and her hand is already at
her ear because that is what everybody does.

The left one is there. The right one is not.

Her first instinct is the useless one — to look at the ground around her feet, which she does for about four
seconds, and then she stops, because the ground at a bus stop is not where things are and she knows it.

What she does instead is the thing her mother taught her, and she says it out loud without meaning to.

"Where was I last?"

Not "where could it be", which is the whole of Bombay. **Where was I immediately before this.**

She was at the vegetable stall on the corner, two minutes ago, paying. And she remembers — genuinely
remembers, not guesses — the woman there commenting on the earrings, which means both were there at the
stall. So it went between the stall and here, which is a hundred and forty feet of pavement, and that is a
completely different problem from the one she had ten seconds ago.

She walks it back slowly, looking down, and does not find it.

So she asks again. Where was I before the stall? The chemist. And before the chemist? The bank, where she had
been at the counter and had leaned down to sign, and where — she is now fairly sure — she had put her hand up
to her ear at some point.

She does not go back to the bank first. She does the stretch between the chemist and the stall, because it is
nearer and it is on the way, and then the stretch between the bank and the chemist.

The earring is on the second step outside the bank, on the flat part where the two steps meet, sitting in
plain view where four hundred people have walked past it and not one has noticed, which she thinks about for
some time afterwards.

The thing that got her there was not searching harder. It was that at every point she asked only about **the
one step before** — not about the whole afternoon. Each answer gave her one short stretch to look at, and
when that failed, the same question again gave her the next one.

---

## 3. The idea in plain English

Vimala's question is the one-dimensional DP habit.

**The habit, stated once:** to compute the answer at position `i`, ask **what the last move was**. Enumerate
every possible last move. Each one leaves you at some earlier position with a known answer. Combine them.

That is it. It produces the recurrence for every problem in this family, and it works because it turns "how do
I solve this" — which is unbounded — into "what are the two or three ways I could have arrived here", which is
a short list you can write down.

**On stairs:** to be standing on step `i`, my last move was a single step from `i-1` or a double step from
`i-2`. Two possible last moves, so:

```
ways(i) = ways(i-1) + ways(i-2)
```

**On house robber:** at house `i` I either robbed it or I did not. If I robbed it, my previous state was the
best I could do up to `i-2`, because `i-1` is forbidden. If I did not, my state is the best up to `i-1`.

```
best(i) = max( money[i] + best(i-2),   best(i-1) )
              \___ robbed ___/        \_ skipped _/
```

**On maximum subarray:** the subarray ending at `i` either extends the one ending at `i-1`, or starts fresh at
`i`.

```
best_ending_at(i) = max( best_ending_at(i-1) + nums[i],   nums[i] )
```

**Three different problems, one question.** Notice that in each case the "last move" enumeration is two or
three options, and each option points at a strictly earlier index. **That is what makes it one-dimensional.**

**Now the second half of the habit, and it is the half people skip: say what `dp[i]` means, as a full English
sentence, before writing the loop.**

The three problems above have three genuinely different meanings, and they are not interchangeable:

```
stairs      dp[i] = the number of distinct ways to REACH step i
robber      dp[i] = the maximum money obtainable from houses 0..i
max subarray dp[i] = the maximum sum of a subarray ENDING EXACTLY at i
```

**The third one is the one that catches people.** "Ending exactly at `i`" is not the same as "using elements up
to `i`", and if you write the recurrence for one while thinking of the other, it is wrong in a way that is
hard to see. **And it has a consequence: the answer is not `dp[n-1]`, it is `max(dp)`** — because the best
subarray ends somewhere, and you do not know where.

**So: where the answer lives is part of the state's definition.** Three possibilities, and you decide which by
reading your own sentence:

- `dp[n-1]` — when the state means "using everything up to here", so the last cell is the whole answer.
- `max(dp)` or `min(dp)` — when the state means "ending exactly here", so the answer could be at any position.
- Something else — minimum cost climbing stairs finishes *past* the last step, so the answer is
  `min(dp[n-1], dp[n-2])`.

**Base cases come from the recurrence, not from intuition.** Write the recurrence first, then look at the
smallest `i` for which it would read a negative index. Every index below that needs an explicit value.
`dp[i] = dp[i-1] + dp[i-2]` reads `i-2`, so `dp[0]` and `dp[1]` must be set by hand.

**And getting them wrong is silent.** Setting `ways(2) = 1` instead of 2 gives you the whole Fibonacci sequence
shifted by one position, and every answer is wrong by exactly one place with no error anywhere.

**The template that fits nearly all of them is four lines:**

```python
dp = [initial] * n
dp[base indices] = base values
for i in range(first_real_index, n):
    dp[i] = combine over each possible last move
return dp[n-1]  # or max(dp), depending on what dp means
```

**The variations are only in `combine`.** Counting problems use `+`. Optimisation problems use `max` or `min`.
Feasibility problems use `any` or `or`. **Same skeleton, different operator**, and recognising which of the
three you have is another thing to say out loud.

**And the last idea: almost all of these collapse to `O(1)` space**, because `dp[i]` typically reads only the
last one or two cells. Keep a window as deep as the recurrence reaches back, which is
[day 144](../day-144-fibonacci-dp/README.md).

---

## 4. The picture

The last-move question, drawn on three problems:

```
CLIMBING STAIRS — how did I arrive at step i?

        i-2       i-1        i
         o---------o---------o
          \                 /
           \_______________/
            a double step

    two ways in  ->  ways(i) = ways(i-1) + ways(i-2)


HOUSE ROBBER — did I rob house i or not?

    ROBBED i:     ... best up to i-2 ... [skip i-1] [ROB i]
    SKIPPED i:    ... best up to i-1 ................ [skip i]

    best(i) = max( money[i] + best(i-2),  best(i-1) )


MAX SUBARRAY — does the subarray ending at i extend, or restart?

    EXTEND:   [ ---- best ending at i-1 ---- ][ i ]
    RESTART:                                 [ i ]

    best_at(i) = max( best_at(i-1) + nums[i],  nums[i] )
```

**What to notice.** In every case the enumeration is short — two options — and every option points at a
strictly smaller index. **When the enumeration is short and points backwards, the problem is one-dimensional
DP.**

Where the answer lives, which depends on what `dp[i]` means:

```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

MAX SUBARRAY, dp[i] = best sum ENDING EXACTLY at i

  i:       0    1    2    3    4    5    6    7    8
  nums:   -2    1   -3    4   -1    2    1   -5    4
  dp:     -2    1   -2    4    3    5    6    1    5
                                       ^
                                       max(dp) = 6, at i = 6

  the answer is NOT dp[8] = 5.
  the best subarray is [4, -1, 2, 1], and it ends at index 6.


HOUSE ROBBER, dp[i] = best from houses 0..i

  money:   2    7    9    3    1
  dp:      2    7   11   11   12
                                ^
                                dp[n-1] = 12, and that IS the answer

  because "0..i" means the last cell covers everything.
```

**What to notice.** Same skeleton, same loop, and the answer is in a different place — because the two states
mean different things. **Reading your own sentence tells you where to look**, and guessing does not.

The base cases, derived rather than guessed:

```
  recurrence:  dp[i] = dp[i-1] + dp[i-2]

  at i = 2:  reads dp[1] and dp[0]     -> both must exist
  at i = 1:  would read dp[-1]         -> so i = 1 is a BASE case
  at i = 0:  would read dp[-2], dp[-1] -> so i = 0 is a BASE case

  => base cases are exactly the indices the recurrence cannot compute.
     The loop starts at 2.
```

---

## 5. The code, built step by step

**Start with the habit, out loud, before any code.**

> "To be on step `i`, my last move was one step from `i-1` or two steps from `i-2`. Those are the only
> possibilities. So `ways(i) = ways(i-1) + ways(i-2)`."

**Then say what the state means.**

```python
# dp[i] = the number of distinct ways to reach step i
```

**Then derive the base cases from the recurrence.** It reads `i-1` and `i-2`, so indices 0 and 1 must be set
by hand:

```python
dp[0] = 1          # one way to be at the bottom: do nothing
dp[1] = 1          # one way to reach step 1: a single step
```

**Then the loop, starting at the first index the recurrence can compute:**

```python
def climb(n: int) -> int:
    # dp[i] = the number of distinct ways to reach step i
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]        # last move: one step, or two
    return dp[n]
```

**Now the same four lines with a different operator.** House robber — the recurrence is a `max` rather than a
sum, because we are optimising rather than counting:

```python
def rob(money: list[int]) -> int:
    # dp[i] = the maximum money obtainable from houses 0..i
    n = len(money)
    if n == 0:
        return 0
    dp = [0] * n
    dp[0] = money[0]
    dp[1] = max(money[0], money[1]) if n > 1 else dp[0]
    for i in range(2, n):
        dp[i] = max(money[i] + dp[i - 2],    # rob i: i-1 is forbidden
                    dp[i - 1])               # skip i
    return dp[n - 1]
```

**Note `dp[1] = max(money[0], money[1])`, not `money[1]`.** The state says "the best from houses 0..1", and the
best of two houses when you may take only one is the larger. **Deriving the base case from the sentence rather
than from the pattern is what gets this right.**

**And the third operator — a feasibility problem, where `combine` is `any`.** Word break:

```python
def word_break(text: str, words: list[str]) -> bool:
    # dp[i] = can text[0:i] be split entirely into dictionary words?
    vocabulary = set(words)
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True                             # the empty prefix is trivially splittable
    for i in range(1, n + 1):
        dp[i] = any(dp[j] and text[j:i] in vocabulary   # last move: the word text[j:i]
                    for j in range(i))
    return dp[n]
```

**The last-move question again:** to split `text[0:i]`, the final word ends at `i` and starts somewhere at
`j`. So enumerate every `j`, and the split works if the prefix up to `j` works and `text[j:i]` is a word.
**Here the enumeration is not two options but `i` of them**, which is why this one is `O(n²)` rather than
`O(n)` — the state count is the same, the work per state is not.

**Now the case where the answer is not in the last cell.** Maximum subarray:

```python
def max_subarray(nums: list[int]) -> int:
    # dp[i] = the maximum sum of a subarray ENDING EXACTLY at index i
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = max(dp[i - 1] + nums[i],     # extend the subarray ending at i-1
                    nums[i])                 # start a new one at i
    return max(dp)                           # NOT dp[n-1] — it ends somewhere
```

**`return max(dp)` follows directly from the sentence.** "Ending exactly at `i`" means each cell is a
candidate, and the best one could be anywhere. **If the sentence had said "using elements up to `i`", the
answer would be `dp[n-1]`.**

**And the space optimisation**, which nearly all of these admit:

```python
def max_subarray_optimised(nums: list[int]) -> int:
    best_ending_here = best_overall = nums[0]
    for value in nums[1:]:
        best_ending_here = max(best_ending_here + value, value)
        best_overall = max(best_overall, best_ending_here)
    return best_overall
```

**Two variables, because the recurrence reaches back exactly one.** And `best_overall` is the `max(dp)`,
maintained as we go rather than computed at the end — which is necessary once the table is gone.

### The complete solution

```python
"""The one-dimensional habit: 'what was the last move?', on four problems."""

from __future__ import annotations


def climb(n: int) -> int:
    """dp[i] = distinct ways to reach step i.  combine = +  (counting)."""
    if n <= 1:
        return 1
    prev, curr = 1, 1                        # dp[0], dp[1]
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def rob(money: list[int]) -> int:
    """dp[i] = max money from houses 0..i.  combine = max  (optimisation)."""
    if not money:
        return 0
    if len(money) == 1:
        return money[0]
    two_back, one_back = money[0], max(money[0], money[1])
    for i in range(2, len(money)):
        two_back, one_back = one_back, max(money[i] + two_back, one_back)
    return one_back


def word_break(text: str, words: list[str]) -> bool:
    """dp[i] = can text[0:i] be split?  combine = any  (feasibility)."""
    vocabulary = set(words)
    longest = max((len(w) for w in vocabulary), default=0)
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        # the last word ends at i and starts at j; it cannot be longer than `longest`
        dp[i] = any(dp[j] and text[j:i] in vocabulary
                    for j in range(max(0, i - longest), i))
    return dp[n]


def max_subarray(nums: list[int]) -> int:
    """dp[i] = best sum of a subarray ENDING AT i.  The answer is max(dp), not dp[-1]."""
    best_ending_here = best_overall = nums[0]
    for value in nums[1:]:
        best_ending_here = max(best_ending_here + value, value)
        best_overall = max(best_overall, best_ending_here)
    return best_overall


def min_cost_climbing(cost: list[int]) -> int:
    """dp[i] = min cost to STAND ON step i.  The top is PAST the last step."""
    n = len(cost)
    two_back, one_back = cost[0], cost[1]
    for i in range(2, n):
        two_back, one_back = one_back, cost[i] + min(two_back, one_back)
    return min(two_back, one_back)           # finish from either of the last two


if __name__ == "__main__":
    print("climb(12)        :", climb(12))
    print("rob              :", rob([2, 7, 9, 3, 1]))
    print("word_break       :", word_break("applepenapple", ["apple", "pen"]))
    print("word_break (no)  :", word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))
    print("max_subarray     :", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print("max_subarray (-) :", max_subarray([-3, -1, -7]))
    print("min_cost         :", min_cost_climbing([10, 15, 20]))
    print("min_cost (long)  :", min_cost_climbing([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))
```

Running it:

```
climb(12)        : 233
rob              : 12
word_break       : True
word_break (no)  : False
max_subarray     : 6
max_subarray (-) : -1
min_cost         : 15
min_cost (long)  : 6
```

Three things to look at. **`max_subarray` on all-negative input returns `-1`, not 0** — because a subarray must
be non-empty, so the answer is the least-bad single element. **Initialising `best_overall = 0` instead of
`nums[0]` is the classic bug here**, and it only shows on all-negative input.

**`min_cost` returns 15 for `[10, 15, 20]`**: start on step 1, pay 15, and step straight past the top. The
answer is `min(dp[n-1], dp[n-2])` because the top is one step beyond the array — **not `dp[n-1]`**, which
would be 30.

And `word_break` correctly rejects `"catsandog"`: every prefix is splittable up to `"catsand"`, and then
nothing completes it. **That is `dp[i]` being `True` for several `i` and still `False` at `n`**, which is what
makes the feasibility form worth writing out rather than shortcutting.

---

## 6. What it costs

**The general formula, from [day 143](../day-143-what-dp-is/README.md):**

```
time  = (number of states) x (work per state)
space = (number of states), before optimisation
```

**For this family the state count is always `n`.** What varies is the work per state — which is the length of
the "last move" enumeration.

```
climbing stairs      n states x O(1)      2 possible last moves      = O(n)
house robber         n states x O(1)      2 possible last moves      = O(n)
max subarray         n states x O(1)      2 possible last moves      = O(n)
decode ways          n states x O(1)      2 possible last moves      = O(n)
word break           n states x O(n)      up to n last moves         = O(n^2)
LIS (simple)         n states x O(n)      up to n last moves         = O(n^2)
coin change          n states x O(coins)  one per coin               = O(n*c)
```

**So the cost is decided by how many ways there are to arrive**, and that number is visible in the recurrence
before you write any code. Two options means linear; "any earlier index" means quadratic.

**And a quadratic one can sometimes be improved by changing what the state means** — longest increasing
subsequence goes from `O(n²)` to `O(n log n)` by storing something cleverer, which is
[day 152](../day-152-longest-increasing-subsequence/README.md).

**Space:**

```
full table          O(n)
window of 2         O(1)      -- when dp[i] reads only i-1 and i-2
window of k         O(k)
```

```
n = 1,000,000
  full table (Python list of ints)   ~40 MB
  two variables                      ~56 bytes
```

**Word break is the exception in this family**, and it is worth noticing why:

```
dp[i] reads dp[j] for ALL j < i
   -> the whole table is live
   -> no space optimisation
```

**Unless you bound the enumeration**, which the code above does: the last word cannot be longer than the
longest dictionary word, so `j` only ranges over the last `L` positions.

```
n = 10,000 characters, longest word 20
  unbounded   10,000 x 10,000 = 100,000,000 substring checks
  bounded     10,000 x 20     = 200,000
                               -> 500x
```

**That bound is the single most valuable optimisation in this family** and it comes from thinking about the
last move rather than about the code.

**The substring cost, which is easy to miss:**

```
text[j:i] in vocabulary
   -> building the substring is O(i - j), not O(1)
   -> so word break is really O(n * L * L) with the bound, or O(n^3) without
```

For interview sizes that is fine; for very long strings the fix is a trie over the dictionary, walking forward
from `j` one character at a time — which is [day 122](../day-122-autocomplete/README.md)'s shape reused.

**Comparison with the naive recursion**, which is the reason any of this exists:

```
climbing stairs, n = 35
  naive        18,454,929 calls
  DP           35 computations
                              -> ~500,000x
```

**And the constant factors within DP, which occasionally matter:**

```
n = 1,000,000
  full table          ~0.15 s, 40 MB
  two variables       ~0.10 s, 56 bytes
  memoised recursion  crashes at ~960 depth
```

---

## 7. The traps

### Not saying what `dp[i]` means

The root cause of most of the others, and it produces an empty editor rather than an error.

```python
dp = [0] * n
for i in range(1, n):
    dp[i] = ...    # ... what?
```

**Write the sentence first, as a comment.** "The maximum sum of a subarray ending exactly at `i`." Then the
recurrence follows from the last-move question, and the base cases follow from the recurrence.

### The answer in the wrong place

```python
return dp[n - 1]        # when dp[i] means "ending exactly at i"
```

```
>>> max_subarray_wrong([-2, 1, -3, 4, -1, 2, 1, -5, 4])
5                        # the answer is 6, at index 6
```

**"Ending exactly at `i`" means every cell is a candidate**, so the answer is `max(dp)`. **"Using everything up
to `i`" means the last cell covers it all**, so the answer is `dp[n-1]`. The sentence tells you which, and
guessing has a fifty percent success rate.

### Base cases from intuition rather than from the recurrence

```python
dp[1] = money[1]         # house robber: "the best from house 1 is house 1"
```

```
>>> rob_wrong([5, 1, 5])
6                        # the answer is 10
```

The state says "the best from houses 0..1", and with two houses and only one allowed, that is `max(money[0],
money[1])`. **Derive the base case from the sentence, not from the pattern of the recurrence.**

### The maximum-subarray initialisation

```python
best_overall = 0         # instead of nums[0]
```

```
>>> max_subarray_zero_init([-3, -1, -7])
0                        # the answer is -1
```

A subarray must be non-empty, so the answer on all-negative input is the least-bad element. **Initialise from
the data, not from a neutral value**, and test with all-negative input — it is the hidden test on this problem
and on several others in the family.

### Off-by-one between `n` and `n + 1`

```python
dp = [0] * n             # but the recurrence indexes up to n
```

```
IndexError: list assignment index out of range
```

**Two conventions, and mixing them is the problem.** Either `dp[i]` means "the answer at position `i` of the
array", sized `n`; or `dp[i]` means "the answer using the first `i` elements", sized `n + 1` with `dp[0]` as
the empty case. **The second is usually cleaner for string and prefix problems** — word break's `dp[0] = True`
is the empty prefix — and the first for positional ones. Pick one, say which in the comment, and stay with it.

### Forgetting the empty or single-element input

```python
dp[0], dp[1] = money[0], max(money[0], money[1])
```

```
IndexError: list index out of range        # on a one-element input
```

Every problem in this family has `n = 0` and `n = 1` cases that the recurrence cannot express. **Handle them
before the table**, explicitly, rather than trying to make the loop cover them.

### The unbounded enumeration

```python
dp[i] = any(dp[j] and text[j:i] in vocabulary for j in range(i))
```

Correct, and `O(n²)` substring checks where `O(n·L)` would do:

```
n = 10,000, longest word 20
  unbounded   100,000,000 checks
  bounded     200,000
```

**The bound comes from the last-move question:** the final word cannot be longer than the longest word in the
dictionary, so `j` starts at `i - L`. **That is the recurrence telling you the loop range**, and it is free.

### Treating a two-dimensional problem as one-dimensional

```python
dp[i] = best answer at position i        # but the answer also depends on how much budget is left
```

If the last-move enumeration needs to know something *besides* the position — remaining capacity, how many
transactions used, whether you are currently holding something — **then the state is not one number and no
one-dimensional table can be correct.** The symptom is that you cannot finish the sentence "`dp[i]` is the
answer when ___" without adding a second clause. **That clause is the second dimension**, and it is
[day 147](../day-147-finding-the-state/README.md).

---

## 8. In the interview

### How it gets asked

- *"How many ways to climb `n` stairs taking one or two steps?"* — the canonical one.
- *"Maximise the sum with no two adjacent elements."* — house robber.
- *"Find the contiguous subarray with the largest sum."*
- *"How many ways can this digit string be decoded?"*
- *"Can this string be split into dictionary words?"*
- *"What does `dp[i]` represent?"* — the follow-up to all of them.

### The first ninety seconds

> "Let me get the recurrence with one question: **what was my last move, and where was I before it?**
>
> To be standing on step `i`, my last move was either a single step from `i-1` or a double step from `i-2`.
> Those are the only two possibilities. So the number of ways to reach `i` is the number of ways to reach
> `i-1` plus the number of ways to reach `i-2` — every way of getting to either of those extends to exactly one
> way of getting here.
>
> **And I would write down what the state means before the loop: `dp[i]` is the number of distinct ways to
> reach step `i`.** That sentence does two things for me. It tells me the base cases — the recurrence reads
> `i-1` and `i-2`, so indices 0 and 1 have to be set by hand, and 'one way to be at the bottom' and 'one way
> to reach step 1' both follow from the sentence rather than from the pattern. And it tells me where the answer
> lives: 'ways to reach step `i`' means `dp[n]` is exactly what was asked.
>
> **That last point is worth flagging because it is not always true.** If the state were 'the best subarray
> ending exactly at `i`', the answer would be `max(dp)`, because the best one ends somewhere and I do not know
> where. **Reading my own sentence is how I decide, and guessing is a coin flip.**
>
> Cost is `O(n)` — `n` states, constant work each, because the last-move enumeration has two options. Space is
> `O(n)` for the table, and then `O(1)` because `dp[i]` reads only the two cells below it, so two variables
> suffice.
>
> **The one thing I would check before coding** is `n = 0` and `n = 1`, because the recurrence cannot express
> them and every problem in this family has an edge case there.
>
> Shall I write it, or would you like the recurrence for a variation first?"

### The follow-ups

**"How did you get the recurrence?"**

> "By asking what the last move was, and I would say that this is a habit rather than an insight — it works on
> every problem of this shape.
>
> The question turns 'how do I solve this', which is unbounded, into 'what are the ways I could have arrived
> here', which is a short list I can write down. For stairs it is two: one step or two steps. Each one leaves
> me at a specific earlier position whose answer I already have, so I combine them.
>
> **The same question on house robber:** at house `i` I either robbed it or I did not. If I robbed it, then
> `i-1` was forbidden, so my previous state is the best up to `i-2`. If I skipped it, my state is the best up
> to `i-1`. Two options, `max` between them.
>
> **On maximum subarray:** the subarray ending at `i` either extends the one ending at `i-1` or starts fresh at
> `i`. Two options again.
>
> **What changes between problems is only the combining operator.** Counting problems add. Optimisation
> problems take a `max` or a `min`. Feasibility problems take an `any`. **Same skeleton, different operator**,
> and knowing which of the three I have is worth saying out loud because it also tells me what to initialise
> the table with — zero for counting, negative infinity or the first element for maximisation, `False` for
> feasibility."

**"What does `dp[i]` represent?"**

> "The number of distinct ways to reach step `i` — and I would say that this question is the one that actually
> separates people, more than the code.
>
> **The reason it matters is that similar-looking states behave completely differently.** 'The best subarray
> ending exactly at `i`' and 'the best subarray using elements up to `i`' are two different states, and the
> recurrence, the base cases and *where the answer lives* are all different. With the first, the answer is
> `max(dp)`; with the second, it is `dp[n-1]`. Write the recurrence for one while thinking of the other and it
> is wrong in a way that passes small tests.
>
> **The test I use** is: given only the state, can I compute the answer without knowing anything else about how
> I got here? For stairs, 'I am on step 8' is enough — the ways to finish from there do not depend on the route
> that reached it.
>
> **And the moment that test fails, I need another dimension.** If the answer also depends on how much budget
> is left, or how many transactions I have used, or whether I am currently holding something, then no
> one-dimensional table can be right. **The symptom is that I cannot finish the sentence '`dp[i]` is the answer
> when ___' without adding a second clause**, and that clause is the second index."

**"Reduce the space."**

> "By looking at what the recurrence reaches back to. Here `dp[i]` reads `dp[i-1]` and `dp[i-2]` and nothing
> else, so I need two numbers at any moment and the rest of the array is history — two variables rolled
> forward, `O(n)` to `O(1)`.
>
> **The rule is that the window is as deep as the recurrence reaches**, so reaching back `k` needs `k` values.
>
> **The one in this family that does not collapse is word break**, and it is worth saying why: `dp[i]` reads
> `dp[j]` for *every* `j` below it, so the whole table is live and there is no window. **But bounding the
> enumeration helps enormously anyway** — the final word cannot be longer than the longest dictionary word, so
> `j` only ranges over the last `L` positions. On a ten-thousand-character string with a longest word of
> twenty, that is two hundred thousand checks instead of a hundred million.
>
> **And when the answer is `max(dp)` rather than `dp[n-1]`, the optimisation needs one more variable** — I have
> to carry the running best as I go, because once the table is gone I cannot take a maximum over it. That is
> two variables instead of one and it is easy to forget.
>
> **What I give up** is the ability to say *which* choices produced the answer — which houses were robbed,
> which subarray was best. If that is wanted, I keep the table, or I track the start and end indices alongside
> the running maximum."

**"Now you can take one, two or three steps. And there are broken steps you cannot use."**

> "Both changes are in the last-move enumeration, and neither changes the shape.
>
> **Three step sizes** means three possible last moves instead of two: `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`.
> The base cases extend to three indices, because the recurrence now reaches back three. Still `O(n)` — the
> work per state went from two additions to three, which is a constant. **And the space window becomes three
> variables rather than two.**
>
> **Broken steps** are a filter on the state rather than on the enumeration: if step `i` is broken, `dp[i] = 0`
> — there are zero ways to be standing on it — and the loop skips computing it. Everything above it then
> naturally sees zero ways through it, so the answer propagates correctly with no special cases.
>
> **The thing I would be careful about** is the base cases when a base index is itself broken. If step 1 is
> broken, `dp[1] = 0` rather than 1, and I would check the smallest inputs by hand rather than assume the
> pattern holds.
>
> **And the general point:** almost every variation on a one-dimensional DP is either a change to the
> enumeration — more moves, so more terms — or a filter on the state — some positions are invalid. **The
> skeleton does not change**, which is why the habit is worth more than any individual problem."

### The model answer

*"A string of digits was encoded with A=1 through Z=26. How many ways can it be decoded? For example, '226'
could be BZ, VF or BBF."*

> "Same habit: what was the last move?
>
> **To decode a string of length `i`, the last letter I produced used either the last one digit or the last two
> digits.** Those are the only options, because no letter uses three digits — Z is 26.
>
> **So `dp[i] = dp[i-1] + dp[i-2]`, conditionally** — and the conditions are the whole problem.
>
> **`dp[i-1]` counts only if `s[i-1]` is a valid single digit**, which means it is 1 to 9. **Zero is not a
> letter**, so a '0' contributes nothing on its own.
>
> **`dp[i-2]` counts only if `s[i-2:i]` is between 10 and 26.** That excludes '07' — which is not seven, it is
> invalid — and excludes '27' upwards.
>
> **`dp[i]` = the number of ways to decode the first `i` characters.** I would use the length convention rather
> than the position one, sizing the table `n + 1`, because the conditions are naturally about 'the last one or
> two characters' and that reads more cleanly.
>
> **Base case: `dp[0] = 1`.** There is exactly one way to decode the empty string — the empty decoding. That is
> not intuition; it is what makes `dp[2]` come out right for a two-digit input, and I would verify it by hand
> on '12' before trusting it.
>
> **The zeros are where every wrong answer in this problem comes from**, so I would enumerate them:
>
> - `'0'` alone → zero ways, because nothing decodes to a leading zero.
> - `'06'` → zero, because '06' is not 6.
> - `'10'` → one way, J, because the zero must pair with the 1.
> - `'100'` → zero, because the second zero has nothing valid to pair with.
>
> **A '0' can only ever be consumed as the second digit of a 10 or a 20**, and if it cannot be, the whole
> string has zero decodings from that point.
>
> **Cost:** `O(n)` time, `n` states with two constant-time checks each. `O(1)` space, because it reaches back
> two — and I would write the two-variable version after the table version.
>
> **What I would test before saying I am done:** `'0'`, `'06'`, `'10'`, `'100'`, `'226'`, and a long string of
> ones, which is the maximum-answer case and grows like Fibonacci. **Those six inputs cover every branch**, and
> for a problem where the recurrence is three lines and the conditions are five, the conditions are what the
> interview is about."

---

## 9. Recall card

**The habit: "what was the last move, and where was I before it?"** Enumerate the possible last moves — usually
two — and each points at a strictly earlier index. That produces the recurrence for every linear DP.

**Say what `dp[i]` means as a full sentence before the loop.** It gives you the base cases (the indices the
recurrence cannot compute) **and where the answer lives**: `dp[n-1]` for "using everything up to here",
`max(dp)` for "ending exactly here", something else when the finish is past the end.

**Same skeleton, three operators:** `+` for counting, `max`/`min` for optimisation, `any` for feasibility — and
the operator also tells you what to initialise the table with.

**Cost = `n` states × the length of the last-move enumeration.** Two options → `O(n)`; "any earlier index" →
`O(n²)`, and **bounding that enumeration** (the last word is at most `L` long) is often a 500× win for free.

**Nearly all of them collapse to `O(1)` space** — a window as deep as the recurrence reaches. And if the
answer is `max(dp)`, carry the running best in a second variable, because the table is gone.
