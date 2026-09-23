---
day: 146
track: dsa
title: "House robber and the choice at each step"
phase: "Dynamic programming"
status: written
---

# House robber and the choice at each step

## 1. What this is, and why they ask it

Yesterday's problems had a fixed set of last moves. Today there is a **decision**: at every position you either
take the thing in front of you or you do not, and taking it forbids something.

That is a different shape and it is worth its own day, because it is the first one where **greedy is wrong**.
Always taking the largest available number looks obviously correct and is not — a single large item can block
two slightly smaller ones. Being able to produce that counter-example on demand is half of what this question
is testing.

The recurrence is one line and it is the template for a whole family: paint houses, delete and earn, stock
problems with a cooldown, and every problem phrased as "choose a subset with no two adjacent".

They ask it because it is short, because the greedy trap is real, and because the follow-up — **"now the
houses are in a circle"** — has a genuinely elegant answer that separates people who understand the structure
from people who memorised the line.

By the end of this lesson you can write the take-or-skip recurrence from the choice, produce the greedy
counter-example, handle the circular variant with the two-run trick, recognise the family in problems that do
not mention adjacency, and reconstruct which items were chosen rather than just the total.

---

## 2. The story

Ashok whitewashes houses, and in the six weeks before Diwali he turns down more work than he takes.

The reason is the lime. It has to be slaked the night before, which means the drum is set up at whichever
house he is doing tomorrow, and it cannot be in two places. So he cannot work two days running. One day on, one
day off, always — the off day is moving the drum, the ladders and the sheets, and setting up for the next
one.

By the second week of October he has offers for most days of the month, and they are not the same size. A
two-room flat is eight hundred. A bungalow with a compound wall is two thousand two hundred. Somebody's
staircase is four hundred.

The first year he did it, he took the biggest ones. It seemed obvious. You cannot do everything, so do the
valuable ones.

He remembers the specific week that taught him otherwise. There was a job on the Wednesday for one thousand
six hundred, which was the largest that week, and jobs on the Tuesday and the Thursday for nine hundred each.
He took the Wednesday, because sixteen hundred is more than nine hundred, and that ruled out both the others.

Eighteen hundred was sitting there in two jobs he could have done, and he made sixteen.

What he does now takes him about ten minutes with the list in front of him, and he does it backwards, which
also surprised him.

He starts at the last day of the month and asks a single question about it: **if I take this job, what is the
best I could have done up to two days before? And if I skip it, what is the best I could have done up to
yesterday?** Whichever is larger is the best possible from the start of the month up to that day.

Then he asks the same question about the day before, and the day before that, all the way back.

The thing he finds hard to explain to people is that he is not deciding anything while he does this. He is not
choosing the Wednesday job or not choosing it. **He is working out, for each day, what the best possible total
is up to that day** — and only at the very end, when he has the number for the last day, does he walk back
through to see which jobs it actually implies.

His nephew, who is at college and did some computing, told him there was a name for it. Ashok said there is a
name for everything.

---

## 3. The idea in plain English

Ashok's ten minutes is house robber, and his bad week is the greedy counter-example.

**The shape: at each position you make a binary choice, and one option forbids something.** Take this house
and you cannot take the previous one. Take this job and Tuesday is gone. **The forbidding is what makes it
interesting** — without it you would take everything and there would be no problem.

**The last-move question from [day 145](../day-145-climbing-stairs/README.md) still produces the recurrence**,
and here the last move is the choice itself:

> To have the best possible total considering houses `0..i`, either I took house `i` or I did not.
>
> **If I took it**, house `i-1` was forbidden, so my situation before was the best over `0..i-2`, and my total
> is `money[i] + best(i-2)`.
>
> **If I skipped it**, my situation is exactly the best over `0..i-1`, unchanged.

```
best(i) = max( money[i] + best(i-2),   best(i-1) )
               \___ take ___/          \_ skip _/
```

**One line, two branches, and every problem in this family is a variation on it.**

**The state sentence matters and it is subtle here.** `dp[i]` is **the maximum obtainable considering houses
0 through `i`** — not "the maximum if I rob house `i`". Those are different states, and the second one leads
to a correct but more awkward recurrence. **Say the sentence, and the base cases follow from it.**

**Base cases, derived from the sentence rather than guessed:**

```
dp[0] = money[0]                        the best from one house is that house
dp[1] = max(money[0], money[1])         the best from two houses, taking at most one
```

**`dp[1]` is the one people get wrong.** Writing `money[1]` looks like the pattern and contradicts the
sentence — "the best from houses 0 and 1" is obviously the larger of the two, not the second one.

**Now the greedy trap, which is the actual content of this problem.**

The obvious approach is to sort by value and take greedily, skipping anything adjacent to something already
taken. **It is wrong**, and Ashok's week is the smallest interesting counter-example:

```
[900, 1600, 900]

greedy: take 1600 (the largest), which blocks both neighbours   -> 1600
correct: take 900 and 900                                        -> 1800
```

**The general reason greedy fails: a local choice that looks best can foreclose two options that are together
worth more.** And you cannot fix it with a smarter greedy rule, because the same shape recurs at every scale.

**The other tempting wrong answer is "take alternate houses".** Take all the even indices, or all the odd
indices, and pick the better:

```
[2, 1, 1, 2]
evens: 2 + 1 = 3
odds:  1 + 2 = 3
correct: 2 + 2 = 4       <- indices 0 and 3, which are neither pattern
```

**Non-adjacent does not mean alternating.** You may leave a gap of two, and the optimal solution often does.
That counter-example is worth having ready because the alternating idea is very common and sounds plausible.

**The space collapses to two variables**, because the recurrence reaches back exactly two. And unusually, the
optimised version is the one most people write, because it reads naturally: keep "the best including up to the
previous house" and "the best including up to the one before that", and roll them forward.

**And then the follow-up: the houses are in a circle**, so the first and last are adjacent.

**The elegant answer is to run the linear version twice.** If the houses are in a circle, then the first and
last cannot both be taken. So either the last house is excluded, or the first is. Run house robber on
`houses[0 : n-1]`, run it on `houses[1 : n]`, and take the larger.

**Why that is correct is worth being able to say:** every valid circular selection excludes at least one of the
two, so it is covered by at least one of the two runs; and every selection produced by either run is valid on
the circle, because neither run contains both endpoints. **Two runs of an `O(n)` algorithm, so still `O(n)`,
and about four extra lines.**

**The single-house case breaks it** — `houses[0:0]` is empty — so `n == 1` needs handling before the two runs.

**Recognising the family** is the last piece, because it rarely says "adjacent":

- **"No two adjacent"** — the direct version.
- **"Delete and earn"**: pick a number and all copies of it, but then you cannot pick `value-1` or `value+1`.
  **Transform to counts indexed by value**, and it *is* house robber over that array.
- **"Cooldown after selling"**: you cannot buy on the day after a sale, which is the same forbidding.
- **"Paint the fence with no three in a row"** — same shape with a longer forbidden window.

**The tell: a binary choice per position where taking forbids a nearby position.**

---

## 4. The picture

The choice at each step, drawn:

```
  houses:   [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
   index:     0     1     2     3     4

  at house 2, two options:

    TAKE 9:   ... best over 0..0 ... [skip 1] [TAKE 2]   =  9 + dp[0] = 9 + 2 = 11
    SKIP 9:   ... best over 0..1 .............. [skip 2] =      dp[1]      =      7

    dp[2] = max(11, 7) = 11
```

The table filling:

```
  money:   2    7    9    3    1
  dp:      2    7   11   11   12
           |    |    |    |    |
           |    |    |    |    +-- max(1 + dp[2]=11+1=12,  dp[3]=11)  = 12
           |    |    |    +------- max(3 + dp[1]=7+3=10,   dp[2]=11)  = 11
           |    |    +------------ max(9 + dp[0]=2+9=11,   dp[1]=7)   = 11
           |    +----------------- max(money[0], money[1]) = max(2,7) = 7
           +---------------------- money[0] = 2

  answer: dp[4] = 12, from houses 1 and 3... no: 7 + 3 = 10.
                       from houses 0, 2 and 4: 2 + 9 + 1 = 12.   <- that one
```

**What to notice on the last line.** The optimal selection is `{0, 2, 4}` — three houses, not the two largest.
**The table gives the total; working out which houses is a separate backward walk**, and section 5 does it.

The greedy trap, and the alternating trap:

```
GREEDY BY VALUE                        ALTERNATE INDICES

[ 900, 1600, 900 ]                     [ 2, 1, 1, 2 ]

take 1600 -> blocks both               evens: 2 + 1 = 3
total 1600                             odds:  1 + 2 = 3

correct: 900 + 900 = 1800              correct: indices 0 and 3 -> 2 + 2 = 4
                                       a gap of TWO, which neither pattern allows
```

**What to notice.** Both wrong approaches are natural, both fail on four-element inputs, and neither failure is
visible on the standard example. **Have both counter-examples ready.**

The circular variant:

```
  houses in a circle: 0 - 1 - 2 - 3 - 0

  the first and the last are now adjacent, so they cannot BOTH be taken.

  RUN A: houses[0 .. n-2]     ->  the last house is excluded
         [ h0  h1  h2 ]  h3

  RUN B: houses[1 .. n-1]     ->  the first house is excluded
          h0  [ h1  h2  h3 ]

  answer = max(A, B)

  every valid circular selection excludes at least one endpoint,
  so it appears in at least one run.
  and neither run can produce an invalid selection,
  because neither contains both endpoints.
```

---

## 5. The code, built step by step

**Start with the choice, said out loud.**

> "At house `i` I either take it or I skip it. If I take it, `i-1` was forbidden, so I add to the best over
> `0..i-2`. If I skip it, I keep the best over `0..i-1`."

**Then the state sentence:**

```python
# dp[i] = the maximum money obtainable considering houses 0..i
```

**Then the base cases, from the sentence:**

```python
dp[0] = money[0]                      # one house: take it
dp[1] = max(money[0], money[1])       # two houses: the larger, not the second
```

**Then the loop:**

```python
def rob_table(money: list[int]) -> int:
    # dp[i] = the maximum obtainable considering houses 0..i
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]
    dp = [0] * n
    dp[0] = money[0]
    dp[1] = max(money[0], money[1])
    for i in range(2, n):
        dp[i] = max(money[i] + dp[i - 2],     # take i: i-1 is forbidden
                    dp[i - 1])                # skip i
    return dp[n - 1]
```

**The two `if`s at the top are not optional.** Every problem in this family has an empty and a single-element
case that the recurrence cannot express, and they are the two hidden tests.

**Now the space optimisation**, which is how most people write it:

```python
def rob(money: list[int]) -> int:
    take_previous = skip_previous = 0      # dp[i-2] and dp[i-1], conceptually
    for value in money:
        take_previous, skip_previous = skip_previous, max(value + take_previous, skip_previous)
    return skip_previous
```

**Read the two names.** `take_previous` holds the best up to two houses back, `skip_previous` holds the best up
to one house back, and each round shifts the window forward. **Starting both at zero handles the empty and
single-element cases automatically**, which is why this version needs no guards — a genuinely nice property
that the table version does not have.

**The simultaneous assignment is load-bearing.** Written as two statements the first overwrites what the second
needs.

**Now the circular version**, which is the follow-up:

```python
def rob_circular(money: list[int]) -> int:
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]                    # the two-run trick breaks on n == 1
    return max(rob(money[:-1]),            # exclude the last house
               rob(money[1:]))             # exclude the first house
```

**Four lines, and the `n == 1` guard is the whole subtlety** — with one house, `money[:-1]` is empty and
`money[1:]` is empty, so both runs return 0 and the answer is wrong.

**And reconstructing which houses were chosen**, which is the other common follow-up:

```python
def rob_with_houses(money: list[int]) -> tuple[int, list[int]]:
    n = len(money)
    if n == 0:
        return 0, []
    if n == 1:
        return money[0], [0]
    dp = [0] * n
    dp[0] = money[0]
    dp[1] = max(money[0], money[1])
    for i in range(2, n):
        dp[i] = max(money[i] + dp[i - 2], dp[i - 1])

    chosen: list[int] = []
    i = n - 1
    while i >= 0:
        if i == 0:
            chosen.append(0)
            break
        if i == 1:
            chosen.append(0 if money[0] > money[1] else 1)
            break
        if dp[i] == dp[i - 1]:
            i -= 1                          # house i was skipped
        else:
            chosen.append(i)                # house i was taken
            i -= 2                          # so i-1 was forbidden
    return dp[n - 1], chosen[::-1]
```

**The walk is backwards and it needs the full table**, which is why reconstruction and space optimisation are
mutually exclusive. The test `dp[i] == dp[i-1]` means "taking house `i` did not improve anything", so it was
skipped; otherwise it was taken and we jump back two.

**Ties make the reconstruction non-unique**, so this returns *a* valid selection rather than *the* one.

**And the transformation that turns a different-looking problem into this one** — delete and earn:

```python
def delete_and_earn(nums: list[int]) -> int:
    """Take a number and all its copies, but then value-1 and value+1 are forbidden."""
    from collections import Counter
    counts = Counter(nums)
    highest = max(nums)
    # earnings[v] = the total money from taking every copy of v
    earnings = [0] * (highest + 1)
    for value, count in counts.items():
        earnings[value] = value * count
    return rob(earnings)                   # ... and now it IS house robber
```

**Index by value, not by position.** Once you do that, "cannot take `v-1` or `v+1`" becomes "cannot take
adjacent indices", and the problem is solved by a function you already have. **Spotting that transformation is
the whole problem**, and the DP is four lines you did not have to write.

### The complete solution

```python
"""House robber: the take-or-skip choice, the circular variant, and reconstruction."""

from __future__ import annotations

from collections import Counter


def rob(money: list[int]) -> int:
    """Maximum with no two adjacent. O(n) time, O(1) space.

    take_previous  = the best considering houses up to i-2
    skip_previous  = the best considering houses up to i-1
    """
    take_previous = skip_previous = 0
    for value in money:
        take_previous, skip_previous = skip_previous, max(value + take_previous, skip_previous)
    return skip_previous


def rob_table(money: list[int]) -> int:
    """The same, with the table. dp[i] = the best considering houses 0..i."""
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]
    dp = [0] * n
    dp[0] = money[0]
    dp[1] = max(money[0], money[1])          # the LARGER, not money[1]
    for i in range(2, n):
        dp[i] = max(money[i] + dp[i - 2], dp[i - 1])
    return dp[n - 1]


def rob_circular(money: list[int]) -> int:
    """First and last are adjacent. Every valid selection excludes one of them."""
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]                      # the two-run trick needs n >= 2
    return max(rob(money[:-1]), rob(money[1:]))


def rob_with_houses(money: list[int]) -> tuple[int, list[int]]:
    """The total AND which houses. Needs the full table — no space optimisation."""
    n = len(money)
    if n == 0:
        return 0, []
    if n == 1:
        return money[0], [0]
    dp = [0] * n
    dp[0], dp[1] = money[0], max(money[0], money[1])
    for i in range(2, n):
        dp[i] = max(money[i] + dp[i - 2], dp[i - 1])

    chosen: list[int] = []
    i = n - 1
    while i >= 0:
        if i == 0:
            chosen.append(0)
            break
        if i == 1:
            chosen.append(0 if money[0] >= money[1] else 1)
            break
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            chosen.append(i)
            i -= 2
    return dp[n - 1], chosen[::-1]


def delete_and_earn(nums: list[int]) -> int:
    """Index by VALUE, and the adjacency constraint becomes house robber."""
    if not nums:
        return 0
    counts = Counter(nums)
    earnings = [0] * (max(nums) + 1)
    for value, count in counts.items():
        earnings[value] = value * count
    return rob(earnings)


if __name__ == "__main__":
    print("rob [2,7,9,3,1]   :", rob([2, 7, 9, 3, 1]))
    print("  which houses    :", rob_with_houses([2, 7, 9, 3, 1]))
    print()
    print("greedy trap       :", rob([900, 1600, 900]), "(greedy would say 1600)")
    print("alternating trap  :", rob([2, 1, 1, 2]), "(alternating would say 3)")
    print()
    print("circular [2,3,2]  :", rob_circular([2, 3, 2]))
    print("circular [1,2,3,1]:", rob_circular([1, 2, 3, 1]))
    print("circular [5]      :", rob_circular([5]))
    print()
    print("delete_and_earn   :", delete_and_earn([3, 4, 2]))
    print("delete_and_earn   :", delete_and_earn([2, 2, 3, 3, 3, 4]))
```

Running it:

```
rob [2,7,9,3,1]   : 12
  which houses    : (12, [0, 2, 4])

greedy trap       : 1800 (greedy would say 1600)
alternating trap  : 4 (alternating would say 3)

circular [2,3,2]  : 3
circular [1,2,3,1]: 4
circular [5]      : 5

delete_and_earn   : 6
delete_and_earn   : 9
```

Three things to look at. **The chosen houses are `[0, 2, 4]`** — three houses totalling 12, not the two
largest. That is what the greedy approach cannot find.

**`circular [2,3,2]` returns 3, not 4.** In a line, houses 0 and 2 give 4; in a circle they are adjacent, so
the best is the single 3. **That input is the one that catches implementations which forgot the circle.**

And `delete_and_earn([2,2,3,3,3,4])` returns 9: taking both 2s and the 4 gives `4 + 4 = 8`, while taking all
three 3s gives 9 — and taking the 3s forbids both the 2s and the 4. **The transformation to `earnings` indexed
by value is what makes that a one-liner.**

---

## 6. What it costs

**Time and space.**

```
n states, each with a constant-size choice (two options)
                                            -> O(n) time
full table                                  -> O(n) space
window of 2 (the recurrence reaches back 2) -> O(1) space
```

**The circular version:**

```
two runs of an O(n) algorithm    -> O(n), with a constant factor of 2
space                            -> O(1), unchanged
```

**Reconstruction:**

```
needs the full table             -> O(n) space, not O(1)
the backward walk                -> O(n) time
                                 -> so asking for the houses costs the space optimisation
```

**Delete and earn:**

```
counting                         O(n)
the earnings array               O(max value)          <- NOT O(n)
house robber over it             O(max value)
                                 -----------------------
                                 O(n + max value) time and space
```

**That `max value` is worth flagging**, because it is a different variable from `n`:

```
nums = [1, 1000000]
  n = 2
  earnings array = 1,000,001 entries
```

**The array is sized by the largest value, not by the count**, so sparse large values are wasteful. The fix is
to sort the distinct values and run a modified recurrence that checks whether consecutive distinct values
actually differ by one — which is `O(n log n)` and independent of the magnitudes. **Worth naming as the fix
when values can be large.**

**Against the naive alternatives:**

```
try every subset                 2^n subsets x O(n) to validate  = O(2^n * n)
  n = 30                         ~32,000,000,000 operations
  DP                             30 operations
```

**Against greedy**, which is not slower but wrong:

```
greedy by value    O(n log n) to sort   -> WRONG on [900, 1600, 900]
alternating        O(n)                 -> WRONG on [2, 1, 1, 2]
DP                 O(n)                 -> correct
```

**The DP is the same order as the wrong greedy and cheaper than the wrong alternating.** There is no
efficiency argument for the wrong answers, which is worth pointing out — they are attractive only because they
look simpler.

**Sizing at realistic limits:**

```
n = 100,000 (a typical constraint)
  DP           100,000 operations, two variables
  runtime      ~10 ms in Python
```

**And the whole family's costs:**

```
house robber                     O(n) time, O(1) space
house robber II (circular)       O(n) time, O(1) space
delete and earn                  O(n + max) time and space
paint fence (no 3 in a row)      O(n) time, O(1) space  -- window of 3
stock with cooldown              O(n) time, O(1) space  -- 3 states per day
```

**All of them are linear**, and all of them collapse to constant space, because the forbidden window is fixed.

---

## 7. The traps

### Greedy by value

The natural wrong answer, and the reason this problem exists:

```python
# sort by value, take greedily, skip anything adjacent to something taken
```

```
>>> greedy([900, 1600, 900])
1600                                       # the answer is 1800
```

**Taking the largest forecloses two options worth more together.** And no smarter greedy rule fixes it,
because the same shape recurs at every scale. **Have this three-element counter-example ready** — being able
to produce it immediately is most of the credit for this question.

### Taking alternate indices

```python
return max(sum(money[0::2]), sum(money[1::2]))
```

```
>>> alternating([2, 1, 1, 2])
3                                          # the answer is 4, from indices 0 and 3
```

**Non-adjacent does not mean alternating.** The optimal solution frequently leaves a gap of two, and neither
alternating pattern can express that. This one sounds even more plausible than greedy-by-value and fails on a
four-element input.

### `dp[1] = money[1]`

```python
dp[0], dp[1] = money[0], money[1]
```

```
>>> rob_wrong([5, 1, 5])
6                                          # the answer is 10
```

The state sentence says "the best considering houses 0 and 1", which is the *larger* of the two.
**Deriving the base case from the sentence rather than from the shape of the recurrence gets this right**, and
guessing gets it wrong about half the time.

### Forgetting the empty and single-element cases

```python
dp = [0] * n
dp[0] = money[0]
dp[1] = max(money[0], money[1])
```

```
IndexError: list index out of range        # on a one-element input
```

**The two-variable version avoids this entirely** by starting both at zero, which is a real argument for
writing it that way — the guards become unnecessary rather than merely handled.

### The circular version on a single house

```python
return max(rob(money[:-1]), rob(money[1:]))
```

```
>>> rob_circular_wrong([5])
0                                          # the answer is 5
```

With one house both slices are empty. **The `n == 1` guard is the whole subtlety of the circular variant**,
and it is the case the tests check.

### The circular version done as one pass

```python
# "just check that houses 0 and n-1 aren't both taken at the end"
```

There is no local way to enforce a constraint between the first and last elements while scanning once — by the
time you reach the end, the decision about the first was made without knowing this. **Two runs is not a
workaround, it is the correct decomposition**, and the argument for it is that every valid circular selection
must exclude at least one endpoint.

### Sizing `delete_and_earn` by `n`

```python
earnings = [0] * (len(nums) + 1)           # should be max(nums) + 1
```

```
IndexError: list assignment index out of range
```

The array is indexed by **value**, not by position, so it must be as long as the largest value. And when values
can be up to `10^9`, the array approach is not viable at all — sort the distinct values instead and check
whether consecutive ones differ by exactly one.

### Optimising space and then being asked which houses

```python
take_previous, skip_previous = ...
# "and which houses did you rob?"
```

You cannot say. The table recorded the decisions and there is no table. **Ask whether the total is enough
before optimising**, because retrofitting the reconstruction means putting the table back.

---

## 8. In the interview

### How it gets asked

- *"Maximise the sum with no two adjacent elements."* — the direct version.
- *"You cannot rob two adjacent houses."* — LeetCode 198.
- *"Now the houses are in a circle."* — LeetCode 213, the standard follow-up.
- *"Delete a number and earn its value, but then you cannot take value±1."* — LeetCode 740.
- *"Why doesn't greedy work?"* — the question the problem exists for.
- *"Which houses did you rob?"* — the reconstruction follow-up.

### The first ninety seconds

> "At each house there is a binary choice — take it or skip it — and taking it forbids the previous one. So
> the last-move question gives me the recurrence directly.
>
> **If I take house `i`, then `i-1` was forbidden, so my best is `money[i]` plus the best over houses 0 to
> `i-2`. If I skip it, my best is unchanged from the best over 0 to `i-1`.** So `dp[i] = max(money[i] +
> dp[i-2], dp[i-1])`.
>
> **`dp[i]` means the maximum obtainable considering houses 0 through `i`** — not 'the maximum if I rob house
> `i`'. That distinction matters because it decides the base cases: `dp[0]` is `money[0]`, and `dp[1]` is
> `max(money[0], money[1])`, the *larger* of the two, not the second one. Writing `money[1]` there is the
> common bug and it comes from copying the recurrence's shape instead of reading the sentence.
>
> **The thing I would flag before you ask is why greedy fails**, because it is the natural first instinct.
> Take the largest available and skip its neighbours: on `[900, 1600, 900]` that takes 1600 and blocks both,
> giving 1600, when 900 plus 900 is 1800. **One large item forecloses two smaller ones worth more together**,
> and no smarter greedy rule fixes it because the shape recurs at every scale.
>
> **And the other tempting wrong answer is alternating indices** — take all evens or all odds. On `[2, 1, 1,
> 2]` both give 3, and the answer is 4 from indices 0 and 3. **Non-adjacent does not mean alternating**; the
> optimal solution often leaves a gap of two.
>
> `O(n)` time and `O(1)` space, because the recurrence reaches back exactly two, so I keep two variables. And
> starting both at zero handles the empty and single-element inputs without guards.
>
> Shall I write it, and would you like the circular version after?"

### The follow-ups

**"Now the houses are in a circle."**

> "Then the first and last are adjacent, and the elegant answer is to run the linear version twice.
>
> **Since houses 0 and `n-1` cannot both be taken, every valid selection excludes at least one of them.** So I
> run house robber on `houses[0 : n-1]` — which excludes the last — and on `houses[1 : n]` — which excludes the
> first — and take the larger.
>
> **The correctness argument has two halves and I would give both.** Every valid circular selection omits at
> least one endpoint, so it is a valid selection in at least one of the two ranges and is therefore considered.
> And conversely, nothing either run produces can be invalid on the circle, because neither range contains both
> endpoints — so I am not over-counting.
>
> Two runs of a linear algorithm, so still `O(n)`, `O(1)` space, and about four extra lines.
>
> **The case that breaks it is `n == 1`**: both slices are empty and both runs return zero, so the answer comes
> out as zero instead of the single house's value. That needs an explicit guard, and it is what the tests
> check.
>
> **What I would not try** is enforcing the constraint in a single pass. There is no local way to say 'do not
> take the last one if I took the first', because by the time I reach the end the decision about the first was
> made without that information. **The two-run decomposition is not a workaround, it is the correct way to
> split the problem** — and I think being able to say why is more valuable than the four lines."

**"Which houses did you rob?"**

> "Then I need the full table, and I would say that up front because it undoes the space optimisation.
>
> **The walk is backwards from the last cell.** At position `i`, if `dp[i] == dp[i-1]`, then taking house `i`
> did not improve anything, so it was skipped and I move to `i-1`. Otherwise it was taken, so I record `i` and
> jump to `i-2`, because `i-1` was forbidden. Handle `i == 0` and `i == 1` explicitly at the end, and reverse
> the list.
>
> `O(n)` time for the walk and `O(n)` space for the table.
>
> **The alternative is parent pointers** — store, alongside each cell, whether it took or skipped — which is
> the same `O(n)` space and slightly clearer. Either way, **reconstruction and constant space are mutually
> exclusive**, and that is worth asking about before optimising rather than after.
>
> **And ties make the answer non-unique.** If taking and skipping give the same total, my walk picks one
> arbitrarily. So I would return *a* valid selection and say so, and a test should assert the total or check
> validity rather than compare against a fixed list of indices."

**"Here is an array; you can take a number and all its copies, but then you cannot take value minus one or
value plus one."**

> "That is house robber with one transformation in front of it, and the transformation is the whole problem.
>
> **The key move is to index by value rather than by position.** Build an array where `earnings[v]` is `v`
> times how many copies of `v` there are — the total money from choosing value `v`. Then 'cannot take `v-1` or
> `v+1`' is exactly 'cannot take adjacent indices', and I run the house robber function I already have.
>
> So on `[2, 2, 3, 3, 3, 4]`: earnings are `[0, 0, 4, 9, 4]`, and house robber over that gives 9 — taking all
> three 3s, which forbids the 2s and the 4. Taking the 2s and the 4 would give 8.
>
> **The cost is different from house robber's, though, and that is worth stating.** The array is sized by the
> *largest value*, not by `n`, so it is `O(n + max)` in time and space. With `n = 2` and values `[1,
> 1000000]`, that is a million-entry array for two numbers.
>
> **The fix when values can be large** is to sort the distinct values and walk them, checking whether
> consecutive distinct values differ by exactly one — if they do, the adjacency constraint applies and the
> recurrence uses the `i-2` term; if they do not, the previous value is not forbidden and you can simply add.
> That is `O(n log n)` and independent of the magnitudes. I would mention it if the constraints allow large
> values, and use the array version otherwise because it is four lines."

**"What if it were 'no two within three positions'?"**

> "The same shape with a wider forbidden window: `dp[i] = max(money[i] + dp[i-4], dp[i-1])`, because taking `i`
> now forbids `i-1`, `i-2` and `i-3`, so the last usable position is `i-4`.
>
> **The base cases extend correspondingly** — the recurrence reaches back four, so indices 0 through 3 need
> explicit values, and each is 'the best from the first `k` positions taking at most one', which is the running
> maximum.
>
> **And the space window becomes four variables** rather than two. Still `O(1)`, still `O(n)` time.
>
> **The general statement:** a fixed forbidden window of width `w` gives `dp[i] = max(money[i] + dp[i-w-1],
> dp[i-1])`, needs `w+1` base cases, and keeps a window of `w+1` values. **The problem does not get harder as
> `w` grows** — which is worth saying, because people expect it to.
>
> **What *would* make it harder** is a forbidding rule that is not a fixed window — 'you cannot take two houses
> whose values differ by less than ten', say. That is not positional at all, the one-dimensional state stops
> being sufficient, and it becomes a genuinely different problem."

### The model answer

*"You are scheduling jobs. Each job takes one day and pays a known amount, and after any job you need a day to
recover, so you cannot work two consecutive days. Maximise your earnings over `n` days, where some days have
no job offered."*

> "This is house robber with two small dressings, and I would name that immediately rather than treat it as
> new.
>
> **The model.** `pay[i]` is what day `i` offers, and a day with no job is simply `pay[i] = 0`. **That is the
> first dressing and it needs no special handling at all** — a zero-paying day is taken or skipped by the same
> recurrence and the arithmetic works out. I would say that explicitly, because the instinct is to filter those
> days out, and filtering would break the adjacency relationship between the days that remain.
>
> **The choice at each day:** work it or do not. Working day `i` means day `i-1` was a recovery day, so my best
> is `pay[i] + dp[i-2]`. Not working means `dp[i-1]`. So `dp[i] = max(pay[i] + dp[i-2], dp[i-1])`, and
> **`dp[i]` is the maximum earnings considering days 0 through `i`**.
>
> **Base cases from the sentence:** `dp[0] = pay[0]`, and `dp[1] = max(pay[0], pay[1])` — the better of the
> first two days, since I can work at most one of them.
>
> **`O(n)` time, `O(1)` space** with two variables, and I would write that version because it also removes the
> empty and single-day guards.
>
> **Why not greedy**, and I would raise it unprompted because it is the plausible wrong answer here: taking the
> highest-paying day first blocks its neighbours, and on `[900, 1600, 900]` that earns 1600 where 1800 was
> available. **A single good day can foreclose two decent ones worth more together.**
>
> **The follow-up I would expect** is that the schedule wraps — a rolling four-week roster where the last day
> and the first day are also consecutive. **That is the circular variant: run it once excluding the last day
> and once excluding the first, and take the larger**, because any valid schedule must skip at least one of
> them. With the `n == 1` guard.
>
> **And the practical question I would ask before writing anything:** does the recovery day depend on the job?
> A large job might need two days off, and if the recovery period varies per job, the forbidden window is no
> longer fixed — `dp[i] = max(pay[i] + dp[i - recovery[i] - 1], dp[i-1])` — which is still `O(n)` and still
> one-dimensional, but the space no longer collapses to a fixed window because the reach-back varies. **That is
> a genuinely different answer to 'can you reduce the space', and I would rather know before promising it.**"

---

## 9. Recall card

**A binary choice per position where taking forbids a neighbour:**
`dp[i] = max(money[i] + dp[i-2], dp[i-1])` — take, or skip.

**`dp[i]` = the maximum considering houses 0..i** (not "if I rob `i`"), which is what makes `dp[1] =
max(money[0], money[1])` — the **larger**, not the second. Derive base cases from the sentence.

**Two counter-examples to have ready.** Greedy by value fails on `[900, 1600, 900]` (1600 vs 1800). Alternating
indices fails on `[2, 1, 1, 2]` (3 vs 4) — **non-adjacent does not mean alternating.**

**Circular: run the linear version twice**, excluding the last house and excluding the first, and take the max
— because every valid selection omits at least one endpoint, and neither run can produce an invalid one.
**Guard `n == 1`.**

**`O(n)` time, `O(1)` space with two variables** (which also removes the empty/single guards). Reconstruction
needs the **full table** — walk backwards, `dp[i] == dp[i-1]` means skipped — so it is mutually exclusive with
the space optimisation. And **delete-and-earn is this problem after indexing by value**, at `O(n + max)`.
