---
day: 152
track: dsa
title: "Longest increasing subsequence"
phase: "Dynamic programming"
status: written
---

# Longest increasing subsequence

## 1. What this is, and why they ask it

Given a list of numbers, find the length of the longest run you can pick out — **keeping their original order,
but not requiring them to be next to each other** — that increases the whole way.

`[10, 9, 2, 5, 3, 7, 101, 18]` has a longest increasing subsequence of length 4: `2, 3, 7, 18`. Or `2, 3, 7,
101`. Both are length 4, and the length is what is asked for.

They ask it for two reasons and they are unusually different from each other.

**The first is the state.** The obvious state — "the longest increasing subsequence in the first `i`
elements" — **does not work**, and discovering why is the cleanest lesson in DP state design there is. The
state that works is "the longest increasing subsequence **ending exactly at** `i`", and the difference between
those two sentences is the entire topic. **Yesterday's lessons taught adding a dimension; this one teaches
redefining instead.**

**The second is the `O(n log n)` solution**, which is genuinely surprising, mildly beautiful, and asked as a
follow-up almost every time. It maintains an array that **is not the answer and never was** — its contents are
not a valid subsequence — and yet its length is exactly right. Being able to say what that array actually
holds is the difference between having understood it and having memorised it.

By the end of this lesson you can write the `O(n²)` version and defend the state, derive the `O(n log n)`
version and say precisely what its array means, reconstruct the actual subsequence, and recognise the family —
box stacking, Russian dolls, and the ones that are LIS in disguise.

---

## 2. The story

The photographs were in four biscuit tins and Sumitra had said she would sort them, which she now regretted.

There was no date on any of them. A few had something written on the back in her mother's hand, and most had
nothing, and the ones that did say something said things like "at the wedding" without saying whose.

So she did what you do, which was to lay them out and work from what she could see.

**The children were the clock.** Her brother in shorts. Her brother taller. Her brother with the beginnings of
a moustache and a very bad shirt. If she could put the pictures in an order where he only ever got older, she
had something.

And the difficulty was immediately obvious, and it was not the one she expected.

It was not that she could not order them. **It was that she could not use all of them.**

Because there were photographs of cousins she could not place at all, and one of a house they had lived in for
two years and she did not know which two, and a picture of her grandmother that could have been any year in a
decade. **Putting those in the line meant guessing, and one wrong guess broke the whole thing.**

So she started leaving them out.

**And the question changed shape completely.** It was no longer "what order do these go in". It was **"what is
the largest number of them I can put in a line where each one is definitely later than the one before"** — and
everything else goes back in the tin.

Her son, who was eleven and was helping in the way eleven-year-olds help, asked why she did not just start at
the first photograph and keep going.

She had already tried that. **The first photograph was her brother at about fifteen, and if she started there,
everything from before that was unusable.** Twenty-odd pictures thrown away because of where she happened to
start.

**The picture you start from decides how long the line can be, and you cannot know which one to start from
until you have tried.**

That was the sentence she said out loud, to nobody, at about eleven at night, and it is why she was still at
it at one.

---

## 3. The idea in plain English

Sumitra's sentence at eleven at night is the state definition, and her failed attempt at starting from the
first photograph is the wrong state.

**First, what "subsequence" means, because it is not "substring".** A subsequence keeps the original order and
is allowed to skip. In `[10, 9, 2, 5, 3, 7]`, the values `2, 5, 7` form a subsequence — they appear in that
order — even though `3` sits between the `5` and the `7`. **A substring would have to be contiguous. A
subsequence does not.**

**Now the state that does not work.** The natural first attempt is:

> `dp[i]` is the length of the longest increasing subsequence in the first `i` elements.

**Try to write the recurrence and you get stuck immediately.** You are at element `i` and you want to know
whether you can extend the best subsequence found so far. **And you cannot, because `dp[i-1]` tells you the
length and nothing else** — not what the last value was, and the last value is exactly what decides whether
`nums[i]` can follow it.

**That is an incomplete state**, and it fails silently: you can write code from it that runs and returns
numbers.

**The state that works redefines rather than extends:**

> **`dp[i]` is the length of the longest increasing subsequence that ends exactly at index `i`.**

**Now the last value is known — it is `nums[i]`.** The state carries it, because ending-exactly-here is part of
the definition. **That is the whole fix**, and it is worth noticing that the state space did not grow: still
`n` cells. **Redefining was free; adding a dimension would not have been.**

**The recurrence follows in one line.** To build a subsequence ending at `i`, look at every earlier index `j`.
If `nums[j] < nums[i]`, the subsequence ending at `j` can be extended by `nums[i]`.

```
dp[i] = 1 + max(dp[j]) over all j < i where nums[j] < nums[i]
        (and 1 if there is no such j — the element alone)
```

**Every `dp[i]` starts at 1**, because a single element is an increasing subsequence of length one.

**And the answer is `max(dp)`, not `dp[n-1]`.** That is Sumitra's point: the best line does not have to end at
the last photograph. **This is the second-most-common bug in the problem** and it produces plausible numbers.

**That is `O(n²)`** — for each `i`, scan every `j` before it — and for `n` up to a few thousand it is what to
write.

**Now the `O(n log n)` version**, which is the follow-up.

**Keep an array called `tails`, where `tails[k]` is the smallest possible value that can end an increasing
subsequence of length `k + 1`.**

Read that twice. **`tails` is not a subsequence.** Its contents may not appear together in the input in that
order at all. It is a summary: for each achievable length, the best (smallest) value you could be sitting on.

**Why smallest is best:** if you can end a length-3 subsequence on a 7 or on a 9, **the 7 is strictly better**,
because anything that could extend the 9 could also extend the 7, and some things that could extend the 7
could not extend the 9. **Smaller endings are never worse.**

**And `tails` is always sorted**, which is what makes binary search legal. It has to be: a longer subsequence
ends on a value at least as large as the shorter one it contains.

**The algorithm is four lines.** For each number, binary search `tails` for the first entry **greater than or
equal to** it.

- **If there is none** — the number is larger than everything — **append it.** The longest achievable length
  just grew by one.
- **Otherwise, overwrite that entry.** You have found a smaller value that can end a subsequence of that
  length, which is an improvement for the future and changes nothing about the past.

**The answer is `len(tails)`.**

**And this is the part to say out loud in an interview: `tails` is not the answer, its length is.** If you need
the actual subsequence you must record parent pointers separately, because reading `tails` at the end can give
you a sequence that does not exist in the input.

**Finally, the variants, which are the same algorithm with one symbol changed.**

```
strictly increasing      bisect_left    (>= replaced)   the standard
non-decreasing           bisect_right   (>  replaced)   allows equal values
longest DEcreasing       reverse the input, or flip the comparison
longest bitonic          LIS from the left + LIS from the right at each i
```

**And the disguises.** *Russian Doll Envelopes* is LIS on heights after sorting by width — **with the widths
sorted ascending and the heights descending within equal widths**, so that two envelopes of the same width can
never both be picked. *Maximum Height by Stacking Cuboids*, *Number of Longest Increasing Subsequences*, and
the minimum-number-of-decreasing-subsequences problem are all this.

---

## 4. The picture

The `O(n²)` table filling in, for `[10, 9, 2, 5, 3, 7, 101, 18]`:

```
  index:  0    1   2   3   4   5   6    7
  value: 10    9   2   5   3   7  101   18

  dp[0] = 1   nothing before it
  dp[1] = 1   9 > nothing earlier that is smaller
  dp[2] = 1   2 is smaller than everything before
  dp[3] = 2   5 extends [2]                         -> 2,5
  dp[4] = 2   3 extends [2]                         -> 2,3
  dp[5] = 3   7 extends [2,5] or [2,3]              -> 2,3,7
  dp[6] = 4   101 extends [2,3,7]                   -> 2,3,7,101
  dp[7] = 4   18 extends [2,3,7]                    -> 2,3,7,18

  dp =  [1,   1,  1,  2,  2,  3,  4,   4]
                                   ^    ^
  answer = max(dp) = 4, NOT dp[-1].
  Here they happen to agree. On [1,2,3,0] they do not:
     dp = [1, 2, 3, 1]  -> max is 3, dp[-1] is 1.
```

Why the natural state fails:

```
  WRONG: dp[i] = longest LIS in the first i elements

  nums = [2, 5, 3, 7]
  dp[3] = 2      (that is [2,5])
  now element 3 arrives. Can 3 extend it?

  -> dp[3] says "the best so far is length 2"
  -> it does NOT say what that subsequence ENDS on
  -> 3 can follow a 2 but not a 5, and I cannot tell which

  The state is INCOMPLETE. You can still write code from it.
  It just gives wrong answers, with no error.

  RIGHT: dp[i] = longest LIS ENDING EXACTLY at i
  -> the last value is nums[i], carried by the definition itself.
  -> same n cells. Redefining cost nothing.
```

The `tails` array evolving, on the same input:

```
  nums = [10, 9, 2, 5, 3, 7, 101, 18]

  10   -> tails empty, append            tails = [10]
   9   -> first >= 9 is 10, at index 0   tails = [9]
   2   -> first >= 2 is 9,  at index 0   tails = [2]
   5   -> nothing >= 5, append           tails = [2, 5]
   3   -> first >= 3 is 5,  at index 1   tails = [2, 3]
   7   -> nothing >= 7, append           tails = [2, 3, 7]
 101   -> nothing >= 101, append         tails = [2, 3, 7, 101]
  18   -> first >= 18 is 101, index 3    tails = [2, 3, 7, 18]

  answer = len(tails) = 4                         CORRECT

  and note: [2, 3, 7, 18] IS a real subsequence here, by luck.
```

The case that proves `tails` is not the answer:

```
  nums = [1, 6, 7, 2, 3]

   1 -> append              tails = [1]
   6 -> append              tails = [1, 6]
   7 -> append              tails = [1, 6, 7]
   2 -> replaces 6          tails = [1, 2, 7]
   3 -> replaces 7          tails = [1, 2, 3]

  len(tails) = 3            CORRECT (1,6,7 is length 3)

  but tails is [1, 2, 3], and 1,2,3 IS in the input...
  try nums = [1, 6, 7, 2]:
   tails ends as [1, 2, 7]
   -> 1, 2, 7 is NOT a subsequence: the 2 comes AFTER the 7.
   -> the LENGTH 3 is right. The CONTENTS are meaningless.
```

What `tails[k]` means, drawn:

```
  tails[0] = smallest value that can end an LIS of length 1
  tails[1] = smallest value that can end an LIS of length 2
  tails[2] = smallest value that can end an LIS of length 3

  "smallest" because a smaller ending is never worse:
     ending on 7 vs ending on 9, both length 3
     -> anything extending 9 also extends 7
     -> some things extend 7 and not 9
     -> keep 7, discard 9. Strictly better.

  and tails is ALWAYS SORTED, which is why binary search is legal:
     a length-3 subsequence contains a length-2 one, so its ending
     is at least as large.
```

---

## 5. The code, built step by step

### The `O(n²)` version, from the sentence

```python
def length_of_lis_quadratic(nums: list[int]) -> int:
    if not nums:
        return 0
    dp = [1] * len(nums)                      # every element alone is length 1
    return max(dp)                            # (loops next)
```

**`[1] * n` is the base case for all of them at once** — every element on its own is an increasing subsequence
of length one.

```python
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:             # can nums[i] follow nums[j]?
                dp[i] = max(dp[i], dp[j] + 1)
```

**`nums[j] < nums[i]` is strict**, which gives strictly increasing. Use `<=` and you get non-decreasing, which
is a different problem — read the statement.

**And `max(dp)`, not `dp[-1]`.** The best subsequence can end anywhere.

### The `O(n log n)` version

```python
import bisect

def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                     # tails[k] = smallest end of an LIS of length k+1
    for number in nums:
        position = bisect.bisect_left(tails, number)
        if position == len(tails):
            tails.append(number)              # extends the longest run so far
        else:
            tails[position] = number          # a smaller ending for that length
    return len(tails)
```

**Six lines, and the comment on line two is the whole explanation.**

**`bisect_left` finds the first entry `>= number`.** If nothing is `>=`, the number is bigger than everything
and the answer grows. Otherwise it replaces that entry with something smaller, which can only help later.

**`bisect_left` for strictly increasing; `bisect_right` for non-decreasing.** One character, two problems —
and it is worth saying which you wrote and why.

### Reconstructing the actual subsequence

**You cannot read it off `tails`.** Record parent pointers instead:

```python
def lis_sequence(nums: list[int]) -> list[int]:
    if not nums:
        return []
    tails: list[int] = []
    tail_index: list[int] = []                # tail_index[k] = index in nums of tails[k]
    parent = [-1] * len(nums)                 # parent[i] = previous index in the LIS ending at i

    for i, number in enumerate(nums):
        position = bisect.bisect_left(tails, number)
        if position > 0:
            parent[i] = tail_index[position - 1]
        if position == len(tails):
            tails.append(number)
            tail_index.append(i)
        else:
            tails[position] = number
            tail_index[position] = i

    result, i = [], tail_index[-1]
    while i != -1:
        result.append(nums[i])
        i = parent[i]
    return result[::-1]
```

**`parent[i] = tail_index[position - 1]`** says: the element before `nums[i]` in its subsequence is whatever
element currently ends the best run one shorter. **Then walk back from `tail_index[-1]`**, which is the index
of the element ending the longest run.

**Two extra arrays and `O(n)` more space**, and it produces a genuinely valid subsequence — unlike reading
`tails`.

### Russian doll envelopes, the disguise

```python
def max_envelopes(envelopes: list[tuple[int, int]]) -> int:
    envelopes.sort(key=lambda e: (e[0], -e[1]))    # width up, height DOWN
    return length_of_lis([height for _, height in envelopes])
```

**The `-e[1]` is the whole trick and it is easy to miss.** Sorting heights *descending* within equal widths
means two envelopes of the same width appear as a decreasing pair, **so LIS can never pick both** — which is
exactly the rule, since equal widths do not nest.

**Sort heights ascending instead and it silently overcounts**, giving a larger, wrong answer.

### Counting the longest ones

```python
def find_number_of_lis(nums: list[int]) -> int:
    n = len(nums)
    length = [1] * n
    count = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]        # a new best: inherit its count
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]       # another way to reach the same best
    best = max(length)
    return sum(c for l, c in zip(length, count) if l == best)
```

**Two arrays, and the `>` versus `==` branches are the whole problem.** A strictly better length **replaces**
the count; an equally good length **adds** to it. **Getting that backwards is the standard bug**, and it gives
plausible numbers.

### The complete solution

```python
"""Longest increasing subsequence: both algorithms, reconstruction, and the family."""

import bisect


def length_of_lis_quadratic(nums: list[int]) -> int:
    """O(n^2). dp[i] = longest LIS ENDING EXACTLY at i."""
    if not nums:
        return 0
    dp = [1] * len(nums)                      # each element alone
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:             # nums[i] can follow nums[j]
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)                            # NOT dp[-1]


def length_of_lis(nums: list[int]) -> int:
    """O(n log n). tails[k] = smallest value ending an LIS of length k+1."""
    tails: list[int] = []
    for number in nums:
        position = bisect.bisect_left(tails, number)   # first entry >= number
        if position == len(tails):
            tails.append(number)              # longer than anything so far
        else:
            tails[position] = number          # a smaller ending for that length
    return len(tails)                         # the LENGTH is the answer, not tails


def length_of_non_decreasing(nums: list[int]) -> int:
    """One character different: bisect_right allows equal values."""
    tails: list[int] = []
    for number in nums:
        position = bisect.bisect_right(tails, number)
        if position == len(tails):
            tails.append(number)
        else:
            tails[position] = number
    return len(tails)


def lis_sequence(nums: list[int]) -> list[int]:
    """The actual subsequence. tails cannot give it; parent pointers can."""
    if not nums:
        return []
    tails: list[int] = []
    tail_index: list[int] = []
    parent = [-1] * len(nums)

    for i, number in enumerate(nums):
        position = bisect.bisect_left(tails, number)
        if position > 0:
            parent[i] = tail_index[position - 1]
        if position == len(tails):
            tails.append(number)
            tail_index.append(i)
        else:
            tails[position] = number
            tail_index[position] = i

    result: list[int] = []
    i = tail_index[-1]
    while i != -1:
        result.append(nums[i])
        i = parent[i]
    return result[::-1]


def max_envelopes(envelopes: list[tuple[int, int]]) -> int:
    """LIS in disguise. Width ascending, height DESCENDING within equal widths."""
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    return length_of_lis([height for _, height in envelopes])


def find_number_of_lis(nums: list[int]) -> int:
    """How many longest increasing subsequences there are."""
    n = len(nums)
    if n == 0:
        return 0
    length = [1] * n
    count = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]       # strictly better: replace
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]      # equally good: add
    best = max(length)
    return sum(c for l, c in zip(length, count) if l == best)


def longest_bitonic(nums: list[int]) -> int:
    """Up then down. LIS from the left plus LIS from the right at each index."""
    n = len(nums)
    if n == 0:
        return 0
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                up[i] = max(up[i], up[j] + 1)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            if nums[j] < nums[i]:
                down[i] = max(down[i], down[j] + 1)
    return max(u + d - 1 for u, d in zip(up, down))   # -1: the peak is in both


if __name__ == "__main__":
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print("quadratic      :", length_of_lis_quadratic(nums))
    print("n log n        :", length_of_lis(nums))
    print("the subsequence:", lis_sequence(nums))

    tricky = [1, 6, 7, 2]
    print("tricky length  :", length_of_lis(tricky))
    print("tricky sequence:", lis_sequence(tricky))

    print("dp[-1] trap    :", length_of_lis([1, 2, 3, 0]))
    print("all decreasing :", length_of_lis([5, 4, 3, 2, 1]))
    print("empty          :", length_of_lis([]))

    print("non-decreasing :", length_of_non_decreasing([1, 3, 3, 5]))
    print("strict on same :", length_of_lis([1, 3, 3, 5]))

    print("envelopes      :", max_envelopes([(5, 4), (6, 4), (6, 7), (2, 3)]))
    print("count of LIS   :", find_number_of_lis([1, 3, 5, 4, 7]))
    print("bitonic        :", longest_bitonic([1, 11, 2, 10, 4, 5, 2, 1]))
```

Run it and you get:

```
quadratic      : 4
n log n        : 4
the subsequence: [2, 3, 7, 18]
tricky length  : 3
tricky sequence: [1, 6, 7]
dp[-1] trap    : 3
all decreasing : 1
empty          : 0
non-decreasing : 4
strict on same : 3
envelopes      : 3
count of LIS   : 2
bitonic        : 6
```

**`tricky` is the line that proves the point.** For `[1, 6, 7, 2]` the `tails` array finishes as `[1, 2, 7]` —
which is **not** a subsequence, because the 2 comes after the 7 in the input. **The length 3 is correct; the
contents are not an answer.** And `lis_sequence` returns `[1, 6, 7]`, which is real.

**`non-decreasing 4` against `strict on same 3`** is the one-character difference, made visible.

---

## 6. What it costs

**The `O(n²)` version.**

```
outer loop over i:              n iterations
inner loop over j < i:          i iterations

total comparisons = 0 + 1 + 2 + ... + (n-1)
                  = n(n-1)/2
                  ~ n^2 / 2

space: one array of n integers  = O(n)
```

**Concretely:**

```
n = 1,000     500,000 comparisons        ~0.1 s in Python.  Fine.
n = 10,000    50,000,000 comparisons     ~10 s.             Too slow.
n = 100,000   5,000,000,000              ~17 minutes.       Impossible.
```

**`n = 2,500` is LeetCode 300's constraint**, which is deliberately set so the quadratic version passes — and
the follow-up asks for better anyway.

**The `O(n log n)` version.**

```
for each of n numbers:
  one binary search over tails          log2(len(tails)) <= log2(n)
  one append or one assignment          O(1)

total: n log n

space: tails is at most n               O(n)
```

**Concretely:**

```
n = 100,000    100,000 x 17 = 1,700,000 operations   ~0.3 s.  Fine.
n = 1,000,000  1,000,000 x 20 = 20,000,000           ~4 s.    Fine.

against 17 minutes and ~14 days for the quadratic version.
```

**The gap at `n = 100,000` is roughly 3,000×**, which is why the follow-up is asked.

**Reconstruction's extra cost:**

```
two extra arrays of n            O(n) space
one extra assignment per element O(1) time
the walk-back                    O(length of the answer) <= O(n)

-> same complexity, about 2x the memory, and it gives a real answer
   instead of tails' meaningless contents.
```

**Counting the longest ones:**

```
two arrays instead of one, same O(n^2) loops
-> O(n^2) time, O(n) space

there is an O(n log n) version using a segment tree, and it is
rarely worth writing in an interview. Say it exists.
```

**Russian doll envelopes:**

```
sort               O(n log n)
LIS on heights     O(n log n)
-> O(n log n) total, dominated by neither

n = 100,000 envelopes: sub-second.
```

**And the bitonic version:**

```
LIS from the left     O(n^2) as written, O(n log n) with tails
LIS from the right    same
combine               O(n)

The -1 in `u + d - 1` matters: the peak element is counted in both
arrays, so adding them double-counts it exactly once.
```

---

## 7. The traps

**Returning `dp[-1]` instead of `max(dp)`.**

```python
>>> nums = [1, 2, 3, 0]
>>> dp = [1] * 4
>>> for i in range(1, 4):
...     for j in range(i):
...         if nums[j] < nums[i]:
...             dp[i] = max(dp[i], dp[j] + 1)
>>> dp
[1, 2, 3, 1]
>>> dp[-1]
1
>>> max(dp)
3
```

**`1` against `3`.** The state is "ending exactly at `i`", so the last cell only describes subsequences that
end at the last element — and the best one often does not. **No error, and the number looks like an answer.**

**Using the incomplete state and not noticing.** If `dp[i]` means "the best in the first `i` elements", you
cannot write a correct recurrence at all — but you *can* write one that runs:

```python
>>> nums = [2, 5, 3, 7]
>>> dp = [1] * 4
>>> for i in range(1, 4):
...     dp[i] = dp[i-1] + 1 if nums[i] > nums[i-1] else dp[i-1]
>>> dp[-1]
3
```

**It gives 3, and the answer is 3.** It is also wrong in general — it only compares each element with the one
immediately before it, so it happily chains `3, 4` and then `1, 2, 5` into a single count:

```python
>>> nums = [3, 4, 1, 2, 5]
>>> dp = [1] * 5
>>> for i in range(1, 5):
...     dp[i] = dp[i-1] + 1 if nums[i] > nums[i-1] else dp[i-1]
>>> dp[-1]
4
```

**Four, when the answer is three** — `1, 2, 5` and `3, 4, 5` are both length three and there is nothing of
length four. **A state that produces the right answer on your first test is the most dangerous kind.**

**`bisect_right` when you wanted strictly increasing.**

```python
>>> length_of_lis([1, 3, 3, 5])
3
>>> length_of_non_decreasing([1, 3, 3, 5])
4
```

**Both are correct programs.** `1,3,5` is the strictly increasing answer; `1,3,3,5` is the non-decreasing one.
**Read the problem statement for the word "strictly"**, and say which you wrote.

**Reading the answer off `tails`.**

```python
>>> nums = [1, 6, 7, 2]
>>> tails = []
>>> for x in nums:
...     p = bisect.bisect_left(tails, x)
...     tails.append(x) if p == len(tails) else tails.__setitem__(p, x)
>>> tails
[1, 2, 7]
```

**`[1, 2, 7]` is not a subsequence of `[1, 6, 7, 2]`** — the 2 appears after the 7. **The length is right and
the contents are not an answer**, and returning them is a real bug that passes any test that only checks the
length.

**Forgetting the empty input.** Without the `if not nums` guard, the quadratic version ends on `max(dp)` with
an empty `dp`:

```python
>>> max([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: max() iterable argument is empty
```

**The `tails` version returns `0` naturally**, because `len([])` is zero — one small argument for it, and a
reminder that the guard is not optional in the quadratic one.

**Sorting envelopes by height ascending within equal widths.**

```python
>>> max_envelopes_wrong = lambda e: length_of_lis(
...     [h for _, h in sorted(e, key=lambda x: (x[0], x[1]))])
>>> max_envelopes_wrong([(1, 1), (1, 2), (1, 3)])
3
```

**Three, when the answer is one** — all three envelopes have width 1, so none nests inside another. **Sorting
heights descending within equal widths makes them a decreasing run that LIS cannot pick twice from.** One
minus sign.

**Comparing floats.**

```python
>>> length_of_lis([0.3, 0.1 + 0.2])
2
```

**Two, because `0.1 + 0.2` is `0.30000000000000004`**, which is strictly greater than `0.3` — so two values
that were meant to be equal look like an increase. **It is arguably correct and it is almost certainly not what
was meant.** If the input is floats, ask about tolerance.

**Very large `n` with the quadratic version.**

```
n = 100,000 -> 5,000,000,000 comparisons

No error. It just does not finish, and on LeetCode:
Time Limit Exceeded
```

**The constraint tells you which version to write**, so read it before choosing.

---

## 8. In the interview

### How it gets asked

- *"Find the length of the longest strictly increasing subsequence."* — LeetCode 300, the standard.
- *"Can you do better than `O(n²)`?"* — always the follow-up.
- *"What does that array you are keeping actually contain?"* — the question that separates people.
- *"Return the subsequence, not just its length."*
- *"You have envelopes with widths and heights; how many can you nest?"* — LeetCode 354.
- *"Why doesn't `dp[i] = best in the first i elements` work?"*

### The first ninety seconds

> "Let me get the state right first, because the obvious state does not work and that is the interesting part
> of this problem.
>
> **The natural attempt is `dp[i]` = the longest increasing subsequence in the first `i` elements.** And I get
> stuck immediately: element `i` arrives and I want to know whether it can extend what I have, but **`dp[i-1]`
> tells me a length and not what that subsequence ended on** — and the ending value is exactly what decides
> whether the new element can follow. **The state is incomplete, and it fails silently**, because I can still
> write code from it that runs.
>
> **The fix is to redefine rather than to add a dimension. `dp[i]` is the longest increasing subsequence that
> ends exactly at index `i`.** Now the last value is `nums[i]` — carried by the definition itself. **And the
> state space did not grow: still `n` cells.** That is worth noticing, because adding a dimension would have
> cost me a factor of `n`.
>
> **The recurrence is one line.** For each `i`, look at every `j` before it; if `nums[j] < nums[i]`, then
> `dp[i]` can be `dp[j] + 1`. Take the best. Every cell starts at 1, because a single element is a valid
> subsequence.
>
> **And the answer is `max(dp)`, not `dp[n-1]`** — the best subsequence does not have to end at the last
> element. **On `[1, 2, 3, 0]`, `dp` is `[1, 2, 3, 1]`: the last cell says 1 and the answer is 3.** That is the
> second most common bug here and it produces a plausible number.
>
> **That is `O(n²)` time and `O(n)` space**, and for `n` up to a few thousand it is what I would write.
>
> **There is an `O(n log n)` version** and I would offer it, because it is what the follow-up asks for. It
> keeps an array where **the entry at index `k` is the smallest value that can end an increasing subsequence
> of length `k + 1`** — and for each number, binary search for the first entry at least as large, then either
> append or overwrite. **The answer is the length of that array.**
>
> **The thing I would flag before they ask: that array is not the answer.** Its contents may not even be a
> subsequence of the input. Only its length is meaningful, and if they want the actual subsequence I need
> parent pointers.
>
> **One question first: strictly increasing, or is equal allowed?** It is one character in the binary search
> and two different answers."

### The follow-ups

**"Can you do better than `O(n²)`? Explain what your array holds."**

> "Yes — `O(n log n)` — and the array is the part worth explaining carefully, because it is easy to write and
> hard to justify.
>
> **`tails[k]` is the smallest value that can end an increasing subsequence of length `k + 1`.**
>
> **Why smallest is the right thing to keep:** suppose I can end a length-three subsequence on a 7 or on a 9.
> **The 7 is strictly better.** Anything that can extend the 9 can also extend the 7, and some things can
> extend the 7 but not the 9. So keeping the smaller ending never loses me an option, and sometimes gains one.
> **There is no reason to remember the 9 at all.**
>
> **And `tails` is always sorted**, which is what makes binary search legal, and it has to be — a length-three
> subsequence contains a length-two one, so its ending value is at least as large.
>
> **The loop is four lines.** For each number, binary search for the first entry greater than or equal to it.
> **If there is none, the number beats everything and I append** — the longest achievable length just grew.
> **Otherwise I overwrite that entry**, because I have found a smaller value that ends a subsequence of that
> length. That changes nothing about the past and improves my options for the future.
>
> **The answer is `len(tails)`.**
>
> **Now the thing I would say before being asked: `tails` is not a subsequence.** On `[1, 6, 7, 2]` it finishes
> as `[1, 2, 7]`, and that is not a subsequence of the input — the 2 comes after the 7. **The length, 3, is
> correct. The contents are meaningless.** Returning them is a bug that passes every test that only checks the
> length.
>
> **Cost: `n` binary searches over an array of at most `n`, so `O(n log n)` time and `O(n)` space.** At a
> hundred thousand elements that is under a second, against about seventeen minutes for the quadratic version
> — roughly three thousand times faster, which is why the follow-up exists.
>
> **And the variant: `bisect_left` gives strictly increasing, `bisect_right` gives non-decreasing.** On
> `[1, 3, 3, 5]` that is 3 against 4. **One character, two different correct answers**, so I would confirm
> which the problem wants."

**"Return the actual subsequence, not the length."**

> "Then I cannot use `tails`, and that constraint is the interesting part of the answer.
>
> **`tails` holds values, not positions, and it is overwritten as it goes**, so at the end it has no memory of
> which elements were actually chosen. On `[1, 6, 7, 2]` it says `[1, 2, 7]`, which is not a valid answer.
>
> **What I do instead is record parent pointers during the same pass.** Two extra arrays: one mapping each
> position in `tails` to the index in `nums` of the element currently sitting there, and one giving, for every
> element, the index of the element before it in the best subsequence ending there.
>
> **The rule is one line.** When element `i` lands at position `p` in `tails`, its predecessor is whatever
> element currently ends the best run of length `p` — that is, the element recorded at `tails` position
> `p - 1`. If `p` is zero, there is no predecessor.
>
> **Then walk back from the element recorded at the last position of `tails`**, following parents, and reverse
> what you collect.
>
> **Cost: `O(n)` extra space and one extra assignment per element** — the complexity does not change. And the
> result is a genuine subsequence, in the right order, of the right length.
>
> **With the `O(n²)` version reconstruction is easier** — record which `j` gave each `dp[i]` its value, find
> the index with the maximum `dp`, and walk back. **I would mention that**, because if they ask for the
> subsequence and `n` is small, the quadratic version with reconstruction is less code to get wrong under
> time pressure.
>
> **And I would ask whether they want *a* longest subsequence or *all* of them**, because all of them can be
> exponentially many — `[1,1,1,...]` with distinct-but-equal-length runs — and that is a different problem
> with a different answer."

**"You have envelopes with widths and heights. One fits inside another if both dimensions are strictly
smaller. How many can you nest?"**

> "This is LIS wearing a hat, and there is exactly one subtle step.
>
> **The problem is two-dimensional and LIS is one-dimensional, so I sort on one dimension to remove it.** Sort
> the envelopes by width ascending. Now, reading left to right, widths are non-decreasing, so **the only
> remaining question is the heights** — and the answer is the longest strictly increasing subsequence of the
> heights.
>
> **The subtlety is what to do with equal widths.** Two envelopes of the same width can never nest, whatever
> their heights. But after sorting by width they sit next to each other, and if their heights happen to
> increase, LIS will happily pick both — **and that is wrong.**
>
> **The fix is to sort heights descending within equal widths.** Then a group of same-width envelopes appears
> as a strictly decreasing run of heights, and **an increasing subsequence can pick at most one from it, by
> construction.** One minus sign in the sort key, and the whole class of errors disappears.
>
> **Concretely: three envelopes all of width 1, heights 1, 2 and 3.** Sorted heights ascending gives
> `[1, 2, 3]` and LIS says three — wrong, since none nests. Sorted descending gives `[3, 2, 1]` and LIS says
> one, which is right.
>
> **Then run the `O(n log n)` LIS on the height list.** Total cost is `O(n log n)` for the sort plus
> `O(n log n)` for the LIS — a hundred thousand envelopes in well under a second.
>
> **The general shape is worth naming**, because it recurs: **sort to remove one dimension, then run a
> one-dimensional algorithm on what is left.** The same trick solves box stacking and the cuboid problem.
> **And the tie-breaking rule in the sort is always where the bug lives.**"

### The model answer

*"You are given a list of software versions deployed to a server over time, each with a compatibility number.
A rollback plan must consist of versions in the order they were deployed, each strictly more compatible than
the last. What is the longest such plan, and which versions are in it?"*

> "This is longest increasing subsequence, and the prompt asks for the sequence as well as the length, which
> changes which algorithm I write.
>
> **Let me confirm the reading first: the versions must stay in deployment order — I cannot reorder them — and
> I may skip any I like.** That is exactly a subsequence, not a substring. **And 'strictly more compatible'
> means strictly increasing, so two versions with the same compatibility number cannot both be in the plan.**
> I would state that, because it is the one-character difference in the implementation.
>
> **The state, and I want to be careful here because the natural one fails.** 'The longest plan using the
> first `i` versions' does not work: when version `i` arrives I need to know what compatibility number the
> current best plan ends on, and a length does not tell me that. **So: `dp[i]` is the longest valid plan that
> ends exactly at version `i`.** The ending value is then `compat[i]`, carried by the definition.
>
> **Recurrence: for each `i`, look at every earlier `j` with `compat[j] < compat[i]`, and take the best
> `dp[j] + 1`.** Each starts at 1. **The answer is `max(dp)`, not the last cell** — the best plan need not end
> at the most recent deployment, and given that deployments often regress in compatibility, it usually will
> not.
>
> **That is `O(n²)`, and here I would ask how many deployments there are.** A server's deployment history is
> realistically hundreds or low thousands, where quadratic is instant and the reconstruction is trivially
> easy — record which `j` won for each `i`, then walk back from the argmax. **If it were a hundred thousand, I
> would use the `O(n log n)` version**, which keeps an array whose entry `k` is the smallest compatibility
> number that can end a plan of length `k + 1`, binary searching for each element.
>
> **And I would raise the trap in that version, because the prompt asks for the versions themselves.** That
> array's contents are not a valid plan — on `[1, 6, 7, 2]` it ends as `[1, 2, 7]`, which is not in that order
> in the input. **Its length is right and its contents are not an answer**, so reconstruction needs parent
> pointers recorded during the pass, not a read of the array at the end.
>
> **Given the realistic size, I would write the quadratic version with reconstruction** — it is less code, the
> walk-back is obvious, and at a few thousand deployments it runs in milliseconds. **I would say out loud that
> I know the `O(n log n)` version and why I am not using it**, which is a better signal than using it
> unnecessarily.
>
> **Two things about the problem domain I would flag.** **Ties matter and the specification is ambiguous** —
> if two versions have the same compatibility number, 'strictly more' excludes both from following each other,
> and if the real rule is 'at least as compatible', that is `bisect_right` and a different answer. **I would
> ask rather than assume.**
>
> **And there may be more than one longest plan**, all of the same length. If the operator needs to choose
> among them — preferring more recent versions, say — that is a second criterion, and I would handle it as a
> tie-break in the `max`, not as a separate pass."

---

## 9. Recall card

**The natural state fails: "longest LIS in the first `i` elements" is incomplete** — it gives a length and not
the ending value, which is what decides whether the next element can follow. **Redefine, don't extend:
`dp[i]` = the longest increasing subsequence ending *exactly* at `i`.** Same `n` cells; redefining is free.

**`dp[i] = 1 + max(dp[j])` over `j < i` with `nums[j] < nums[i]`, each starting at 1. The answer is `max(dp)`,
never `dp[-1]`** — on `[1,2,3,0]`, `dp` is `[1,2,3,1]`.

**`O(n log n)`: `tails[k]` is the smallest value that can end an LIS of length `k+1`.** Smaller endings are
never worse (anything extending 9 also extends 7); `tails` is therefore sorted, so binary search is legal.
Per number: **`bisect_left` → append if past the end, else overwrite. The answer is `len(tails)`.**

**`tails` is NOT the subsequence** — on `[1,6,7,2]` it ends as `[1,2,7]`, which is not in that order in the
input. **Length right, contents meaningless.** For the actual sequence, record **parent pointers** during the
pass.

**`bisect_left` = strictly increasing; `bisect_right` = non-decreasing** — `[1,3,3,5]` gives 3 and 4.
**Russian doll envelopes = sort width ascending, height DESCENDING within equal widths**, then LIS on heights:
the minus sign is what stops two same-width envelopes both being picked. **`n²` at n=100,000 is ~17 minutes;
`n log n` is under a second.**
