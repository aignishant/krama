---
day: 24
track: dsa
title: "Substrings versus subsequences: the distinction they test"
phase: "Strings"
status: written
---

# Day 024 · DSA — Substrings versus subsequences: the distinction they test

**After today you can:** You never confuse the two again, and you know how many of each a string has.

**The interviewer asks it as:** *How many substrings does a string of length n have? How many subsequences?*

---

## 1. What this is, and why they ask it

A **substring** is a run of characters that are **next to each other** in the original string. A
**subsequence** is characters taken in order but **allowed to skip**. From `"abcde"`, `"bcd"` is a
substring and also a subsequence; `"ace"` is a subsequence and **not** a substring, because the
characters are not adjacent.

One word — *contiguous* — is the entire difference, and it decides everything downstream. It changes
how many there are: a string of length `n` has `n(n+1)/2` non-empty substrings and `2ⁿ` subsequences.
It changes which technique solves the problem: substrings are sliding windows and two pointers,
subsequences are dynamic programming or a greedy walk. And it changes what is even possible, because
you can enumerate every substring of a 1,000-character string and you cannot enumerate every
subsequence of a 100-character one.

Interviewers test this deliberately and often silently. They will say *"longest substring without
repeating characters"* and *"longest common subsequence"* in the same interview, and the words are the
only signal you get about which of two completely different techniques to reach for. Misreading it
costs you the whole question, and it happens constantly — which is exactly why this gets its own day
rather than a footnote.

---

## 2. The story

The market street behind the bus stand in Madurai is one straight lane with twelve shops down the
left-hand side, and Selvi and her mother go there most Saturday mornings.

The street only runs one way for them. They come in at the temple end and they walk down to the
junction, and they do not turn round — partly because it is crowded and partly because Selvi's mother
has a knee that does not like it. So whatever they do that morning, they do in the order the shops
happen to stand in.

Some mornings they only need one thing, and they walk in at shop four, buy it, and cut out at the
lane by shop six. They have covered shops four, five and six. Not four and six — they physically pass
five, whether they want to or not, because it is between the other two. Any walk they do is a
**stretch** of the street with nothing missing out of the middle of it.

But the shops they actually go into are a different matter. Last Saturday they went into the vegetable
shop, then the one that sells buttons and ribbon, and then the sweet shop right at the end, and they
walked past everything else without stopping. Vegetables, buttons, sweets — in that order, because
that is the order the shops stand in, but with plenty left out.

Selvi's daughter, who is fifteen and doing something with numbers at school, asked her two questions
on the way home and would not let it go.

First: how many different walks could you do? Selvi worked it out on her fingers. You pick where you
go in and you pick where you come out, and the second one has to be at or after the first. Seventy-
eight, they decided, for twelve shops.

Then: how many different sets of shops could you go into? That one is different, because for each of
the twelve shops the only question is in or not in, separately from all the others. Her daughter did
it on her phone. Four thousand and ninety-six.

Selvi said that could not possibly be right, and her daughter showed her the working, and it was.

---

## 3. The idea in plain English

Selvi's walk is a **substring**. The shops she went into are a **subsequence**. Both keep the order of
the street, and only one of them is allowed to leave gaps.

### The definitions, on one example

Take `"abcde"`.

| | Substring | Subsequence |
|---|---|---|
| must be adjacent? | **yes** | no |
| order preserved? | yes | yes |
| `"bcd"` | ✓ | ✓ |
| `"ace"` | ✗ — `b` and `d` are skipped | ✓ |
| `"eca"` | ✗ | ✗ — wrong order |
| `""` | ✓ (usually excluded) | ✓ |

**Every substring is a subsequence. The reverse is not true.** That one sentence, said out loud,
settles the definition for good.

There is a third word you will meet: a **subarray** is the same thing as a substring, for arrays.
Same rule, different container. And a **subset** would allow reordering, which neither of these does —
if a problem says "subset" about a string, ask what they mean, because they probably mean subsequence.

### How many substrings

A substring is fixed by two choices: where it starts and where it ends. Pick a start `i` from 0 to
`n-1`, and an end at or after it.

- Starting at 0: `n` choices of end.
- Starting at 1: `n-1` choices.
- ... down to starting at `n-1`: 1 choice.

```
n + (n-1) + (n-2) + ... + 1  =  n(n + 1) / 2
```

That is Selvi picking where to go in and where to come out. For `n = 3` it is `3 × 4 / 2 = 6`, and
here they are for `"abc"`: `a, ab, abc, b, bc, c`. For `n = 12` it is `78`.

The count is **quadratic**, and that is a friendly number. A 1,000-character string has about 500,000
substrings — you can list them all if you have to.

### How many subsequences

A subsequence is fixed by a completely different kind of choice: for **each character
independently**, in or out.

```
2 × 2 × 2 × ... × 2   (n times)   =  2ⁿ
```

Including the empty one. For `"abc"` that is 8: `"", a, b, c, ab, ac, bc, abc`. For `n = 12` it is
4,096. **The count is exponential**, and that is a hostile number: a 100-character string has about
10³⁰ subsequences, which is more than the number of atoms you could count in a lifetime.

**This is why the two words lead to different techniques.** Enumerating substrings is sometimes
reasonable. Enumerating subsequences essentially never is, so any subsequence problem has to be
solved without listing them — which is what dynamic programming is for, and why the DP phase from
[day 143](../day-143-what-dp-is/README.md) is full of subsequence problems.

Put the two side by side and the gap is the whole lesson:

| n | substrings `n(n+1)/2` | subsequences `2ⁿ` |
|---:|---:|---:|
| 3 | 6 | 8 |
| 5 | 15 | 32 |
| 10 | 55 | 1,024 |
| 20 | 210 | 1,048,576 |
| 50 | 1,275 | ~10¹⁵ |
| 100 | 5,050 | ~10³⁰ |

### How to tell which one you are being asked about

The word itself, if it is there. When it is not, these are the tells:

| The problem says | It means | Reach for |
|---|---|---|
| "substring", "subarray", "contiguous", "window" | substring | sliding window, two pointers |
| "subsequence", "in order", "delete some characters" | subsequence | DP, or a greedy two-index walk |
| "longest ... without repeating characters" | substring | sliding window ([day 032](../day-032-variable-window/README.md)) |
| "longest common ..." | almost always subsequence | 2-D DP |
| "is A a subsequence of B" | subsequence | greedy, one pass |
| "count subarrays summing to k" | substring | prefix sums ([day 038](../day-038-subarray-sum-k/README.md)) |

If you genuinely cannot tell, **ask**. *"Does that need to be contiguous?"* takes three seconds and
decides which of two unrelated solutions you are about to write.

### The two techniques, in one line each

**Substrings: a sliding window.** Because substrings are contiguous, you can hold one with two indices
and move them. Extend the right edge to grow, advance the left edge to shrink, and never look at the
same character more than a constant number of times. That gives `O(n)` for problems whose brute force
is `O(n²)` or worse. It is the whole of days [031](../day-031-fixed-window/README.md) to
[035](../day-035-choosing-the-pattern/README.md).

**Subsequences: a greedy walk or a table.** *Is A a subsequence of B?* is a single greedy pass with an
index into each — take the next character of A whenever B offers it. *Longest common subsequence*
needs a 2-D table, because at each pair of positions you either match and move both, or skip one of
them, and you cannot tell which is better without looking ahead. That is `O(m × n)` and it is the
canonical DP problem.

---

## 4. The picture

`"abc"`, both lists in full:

```
   SUBSTRINGS — pick a start, pick an end          SUBSEQUENCES — each character: in or out
   n(n+1)/2 = 6                                     2^n = 8

   a . .   -> "a"                                   . . .   -> ""
   a b .   -> "ab"                                  a . .   -> "a"
   a b c   -> "abc"                                 . b .   -> "b"
   . b .   -> "b"                                   . . c   -> "c"
   . b c   -> "bc"                                  a b .   -> "ab"
   . . c   -> "c"                                   a . c   -> "ac"   <- NOT a substring
                                                    . b c   -> "bc"
                                                    a b c   -> "abc"
```

**What to notice:** the only extra one on the right, apart from the empty string, is `"ac"` — and it
is the one with a hole in the middle. That hole is the entire distinction, and at `n = 3` it costs you
two extra items. At `n = 20` it costs you a million.

The two growth curves, from [day 004](../day-004-the-growth-curves/README.md):

```
   count
     |
 2^n |                                        *
     |                                    *
     |                              *
     |                    *
     |          *                                     n(n+1)/2
     |     *                              . . . . . . . . . .
     |  *    . . . . . . . . . . . . . . .
     |*. . .
     +-------------------------------------------------- n
      0    5    10   15   20   25   30

   at n=20:  substrings 210          subsequences 1,048,576
```

**What to notice:** the dotted line is flat enough to enumerate. The starred one is not, at any size
worth calling a string. That is why "enumerate them all" is a plan for one and never for the other.

A sliding window over substrings, which is what contiguity buys you:

```
  "a b c a b c b b"
   ^     ^
   L     R          window "abc", all distinct, length 3

  "a b c a b c b b"
   ^       ^
   L       R        'a' repeats -> move L past the old 'a'

  "a b c a b c b b"
     ^     ^
     L     R        window "bca", still length 3
```

**What to notice:** neither index ever moves backwards, so each character is visited at most twice
across the whole run. That is what makes it `O(n)` — and it only works because a substring is
contiguous, so a window can represent it. There is no equivalent trick for subsequences.

---

## 5. The code, built step by step

### Listing every substring

```python
for i in range(len(s)):
    for j in range(i + 1, len(s) + 1):
        print(s[i:j])
```

Two loops: `i` picks the start, `j` picks one past the end. `j` starts at `i + 1` so the empty string
is excluded, and goes to `len(s) + 1` so the last character is included — that upper bound is the
off-by-one people get wrong.

Count the iterations and you get `n(n+1)/2`, which is the formula from §3, derived rather than
remembered.

### Listing every subsequence

```python
out = [""]
for ch in s:
    out += [prev + ch for prev in out]
```

Beautifully small, and worth understanding because it *is* the `2ⁿ`. Start with one thing, the empty
subsequence. For each character, every subsequence you already have gives rise to two: itself, and
itself plus this character. So the list doubles on every character.

```
start        ['']
after 'a'    ['', 'a']
after 'b'    ['', 'a', 'b', 'ab']
after 'c'    ['', 'a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']
```

Watch it double: 1, 2, 4, 8. **Never run this on a long string.** At `n = 30` it needs a billion
strings, and at `n = 40` your machine dies. It is here to make the number real, not to be used.

### Is A a subsequence of B?

The greedy walk, LeetCode 392, and it is much simpler than people expect:

```python
def is_subsequence(a: str, b: str) -> bool:
    i = 0
    for ch in b:
        if i < len(a) and a[i] == ch:
            i += 1
    return i == len(a)
```

*Walk through B once. Keep an index into A. Whenever B offers the character A is waiting for, take it
and move on. A is a subsequence of B exactly when you got all the way through A.*

**Why is greedy correct here?** Because taking the *earliest* possible match is never worse. If some
solution matches `a[i]` at a later position in B, replacing it with the earlier one leaves at least as
much of B available for the rest of A. There is nothing to be gained by waiting, so there is no choice
to agonise over — which is exactly why this is `O(n)` while longest-common-subsequence is not.

That argument is the interesting part of the question, and saying it is worth more than the code.

### Longest substring without repeating characters

LeetCode 3, and it is a substring problem, so: sliding window.

```python
last: dict[str, int] = {}
start = 0
best = 0
```

`last[ch]` records the most recent position of each character; `start` is the left edge of the window.

```python
for i, ch in enumerate(s):
    if ch in last and last[ch] >= start:
        start = last[ch] + 1
    last[ch] = i
    best = max(best, i - start + 1)
```

*If this character was seen before, and that sighting is inside the current window, move the left edge
just past it. Then record where we saw it, and update the best length.*

**`last[ch] >= start` is the whole problem.** Without it, a character seen long ago — before the window
began — drags `start` backwards, and the window grows instead of shrinking. The input that proves it
is `"dvdf"`: the answer is 3 (`"vdf"`), and a version without the guard returns 2. Test with `"abba"`
too, which fails the same way.

### Longest common subsequence

LeetCode 1143, and the shape of every subsequence DP problem:

```python
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
return dp[m][n]
```

`dp[i][j]` is the answer for the first `i` characters of `a` and the first `j` of `b`. If the current
characters match, they can both be used, so it is one more than the answer without either. If they do
not, you must drop one of them, and you take whichever gives more.

**Notice why greedy fails here and worked above.** In `is_subsequence` there was only one string to
match, so taking the earliest match was always safe. Here there are two, and skipping a character in
`a` might unlock a longer match later in `b` — you cannot know without trying, so you try both and
keep the better. That is the difference between an `O(n)` problem and an `O(m × n)` one, and it is a
good thing to be able to explain.

`[[0] * (n + 1) for _ in range(m + 1)]`, never `[[0] * (n+1)] * (m+1)` — the aliasing trap from
[day 016](../day-016-2d-arrays/README.md), and it bites in every DP problem you will ever write.

### The complete solutions

```python
def all_substrings(s: str) -> list[str]:
    """Every non-empty substring. There are n(n+1)/2 of them."""
    out: list[str] = []
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):   # j is one PAST the end
            out.append(s[i:j])
    return out


def all_subsequences(s: str) -> list[str]:
    """Every subsequence, including the empty one. There are 2**n of them.

    Demonstration only — never run this on a long string.
    """
    out = [""]
    for ch in s:
        out += [prev + ch for prev in out]   # the list doubles per character
    return out


def is_subsequence(a: str, b: str) -> bool:
    """LeetCode 392. Greedy: take the earliest match, which is never worse."""
    i = 0
    for ch in b:
        if i < len(a) and a[i] == ch:
            i += 1
    return i == len(a)


def length_of_longest_substring(s: str) -> int:
    """LeetCode 3. A SUBSTRING problem, so: sliding window. O(n)."""
    last: dict[str, int] = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:   # >= start: only if it is INSIDE the window
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


def longest_common_subsequence(a: str, b: str) -> int:
    """LeetCode 1143. A SUBSEQUENCE problem, so: a table. O(m*n)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]   # never [[0]*(n+1)] * (m+1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


if __name__ == "__main__":
    print(all_substrings("abc"))
    # ['a', 'ab', 'abc', 'b', 'bc', 'c']            6 = 3*4/2
    print(sorted(all_subsequences("abc"), key=lambda x: (len(x), x)))
    # ['', 'a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']  8 = 2**3

    for n in (1, 2, 3, 5, 10, 20):
        print(f"n={n:>3}  substrings {n*(n+1)//2:>5}   subsequences {2**n:>10}")

    print([is_subsequence(x, y) for x, y in
           (("abc", "ahbgdc"), ("axc", "ahbgdc"), ("", "abc"), ("abc", ""), ("abc", "abc"))])
    # [True, False, True, False, True]

    print([length_of_longest_substring(x) for x in
           ("abcabcbb", "bbbbb", "pwwkew", "", "au", "dvdf")])
    # [3, 1, 3, 0, 2, 3]

    print(longest_common_subsequence("abcde", "ace"))   # 3
    print(longest_common_subsequence("abc", "def"))     # 0
```

---

## 6. What it costs

### Listing them

**Substrings.** The outer loop runs `n` times; for start `i` the inner loop runs `n - i` times. Adding
those up gives `n(n+1)/2` iterations — but each iteration also **builds** a slice, and a slice of
length `k` costs `O(k)` to copy, from [day 019](../day-019-what-a-string-is/README.md). The total
length of all substrings is about `n³/6`, so listing them all is **O(n³) time** and **O(n³) space**.

That surprises people. *Counting* them is `O(n²)` — or `O(1)` with the formula — but *materialising*
them is cubic. At `n = 1,000` that is around 170 million characters, which is a few hundred megabytes.
**If a problem asks you to examine every substring, work with indices, not copies.**

**Subsequences.** `2ⁿ` of them, so listing them is **O(2ⁿ)** at best. At `n = 30` that is a billion
strings; at `n = 40`, a trillion. There is no machine and no patience that makes this work.

### The techniques

| Problem | Kind | Approach | Time | Space |
|---|---|---|---|---|
| longest substring without repeats | substring | sliding window | `O(n)` | `O(k)`, alphabet size |
| all substrings, examined | substring | two loops over indices | `O(n²)` | `O(1)` |
| is A a subsequence of B | subsequence | greedy, one pass | `O(n)` | `O(1)` |
| longest common subsequence | subsequence | 2-D table | `O(m·n)` | `O(m·n)`, or `O(n)` rolled |
| longest palindromic subsequence | subsequence | 2-D table | `O(n²)` | `O(n²)` |

**The pattern to notice:** substring problems are usually `O(n)` once you spot the window, because
contiguity lets two indices represent the whole thing. Subsequence problems are usually `O(n²)` or
`O(m·n)`, because there is no window that can represent a set with holes in it, so you pay for a
table.

### `length_of_longest_substring`

One pass over `n` characters. Each turn does a dictionary lookup, an assignment and a `max` — all
`O(1)`. So **O(n) time**. `start` only ever increases, so the window's left edge also travels at most
`n` positions overall, exactly the argument from
[day 023](../day-023-palindromes/README.md).

Space: one entry per distinct character. **O(min(n, k))** where `k` is the alphabet size — `O(1)` for
a fixed alphabet.

Against the brute force, which is to check every substring for repeats: `n²/2` substrings, each
checked in `O(n)`, so `O(n³)`. At `n = 1,000` that is a billion operations against a thousand.

### `longest_common_subsequence`

`m × n` table cells, each filled with constant work: **O(m·n) time**, **O(m·n) space**. For two
1,000-character strings that is a million cells — fine. For two 100,000-character strings it is 10
billion cells, which is neither fast enough nor small enough, and that is when you say so and talk
about rolling the table down to two rows for `O(n)` space, or about specialised algorithms.

The brute force — generate every subsequence of `a` and check each against `b` — is `O(2ᵐ · n)`. At
`m = 30` that is already unrunnable. **The table is not an optimisation; it is the difference between
possible and impossible.**

### The number to have ready

> A string of length `n` has `n(n+1)/2` substrings and `2ⁿ` subsequences. At `n = 20` that is 210
> against a million. That gap is why substring problems get sliding windows and subsequence problems
> get dynamic programming.

---

## 7. The traps

### The big one: solving the wrong problem

The most expensive mistake in this topic is not a bug. It is reading *"longest common substring"* and
writing the DP for *"longest common subsequence"*, or the reverse. They differ by one line:

```python
# longest common SUBSEQUENCE
else:
    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])     # carry the best from either side

# longest common SUBSTRING
else:
    dp[i][j] = 0                                   # a mismatch BREAKS the run — reset
```

Because a substring must be contiguous, a mismatch ends the run and the count resets to zero — and
the answer is the maximum cell anywhere in the table, not the bottom-right corner. **Read the word.
If it is not there, ask.**

### The near-miss: the sliding-window guard

```python
def length_of_longest_substring(s):
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last:                 # missing: and last[ch] >= start
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best

print(length_of_longest_substring("dvdf"))
```

```
2
```

The answer is 3 — `"vdf"`. Here is what went wrong. At the second `d`, position 2, the code sets
`start = 1`, correctly. Then at `f`, position 3, nothing repeats and all is well. But run it on
`"abba"`: at the second `a`, position 3, `last["a"]` is 0 — a sighting from **before** the window
started — and `start` is dragged backwards from 2 to 1, so the window now contains a repeated `b`.

**`start` must never move backwards.** Either guard with `last[ch] >= start`, or write
`start = max(start, last[ch] + 1)`. Both are correct; the second says the intent more plainly.

### The near-miss: the substring loop bound

```python
for i in range(len(s)):
    for j in range(i + 1, len(s)):      # should be len(s) + 1
        out.append(s[i:j])
```

Every substring ending at the last character is missing, including the whole string itself. On
`"abc"` you get `['a', 'ab', 'b']` — three instead of six. `s[i:j]` excludes position `j`, so `j` must
be allowed to reach `len(s)`.

### The near-miss: `is_subsequence` without the bounds check

```python
def is_subsequence(a, b):
    i = 0
    for ch in b:
        if a[i] == ch:                  # no i < len(a) guard
            i += 1
    return i == len(a)

print(is_subsequence("ab", "abc"))
```

```
Traceback (most recent call last):
  ...
    if a[i] == ch:
       ~^^^
IndexError: string index out of range
```

Once all of `a` has been matched, `i` equals `len(a)` and the next character of `b` reads off the end.
The guard has to come first: `if i < len(a) and a[i] == ch`. Note that Python's `and` short-circuits,
so the second half is never evaluated when the first is false — that ordering is doing real work.

### The contract corner: empty strings

Both of these are true, and both catch people:

- `is_subsequence("", "abc")` is **True** — the empty string is a subsequence of everything.
- `is_subsequence("abc", "")` is **False**.

The first is the one that feels wrong and is right. It also falls out of the greedy code for free,
which is a small sign the code is correct.

### The vocabulary trap: "subarray"

For arrays, **subarray** means contiguous — it is the same idea as substring. **Subsequence** means the
same as it does for strings. But people say "subarray" loosely in conversation, so when an interviewer
says it, confirming *"contiguous, yes?"* costs three seconds and can save you fifteen minutes of the
wrong solution.

---

## 8. In the interview

### How it gets asked

- *"How many substrings does a string of length n have? How many subsequences?"* — the direct version,
  usually as a warm-up. `n(n+1)/2` and `2ⁿ`, derived rather than recited.
- *"Longest substring without repeating characters."* — LeetCode 3. Substring, so window.
- *"Is A a subsequence of B?"* — LeetCode 392. Subsequence, so a greedy pass.
- *"Longest common subsequence."* — LeetCode 1143. Table.
- *"Count the substrings that ..."* — where the answer is often to count as you go rather than to
  enumerate.

### What to say out loud, in the first ninety seconds

1. **Say the distinction before anything else.** *"Substring means contiguous; subsequence keeps the
   order but may skip. Every substring is a subsequence, not the other way round."*
2. **If the word is missing, ask.** *"Does that have to be contiguous?"* Three seconds, and it decides
   which technique you are about to spend twenty minutes on.
3. **Derive the counts, do not recite them.** *"A substring is fixed by a start and an end, so it's
   n + (n-1) + ... + 1 = n(n+1)/2. A subsequence is an independent in-or-out choice per character, so
   2ⁿ."*
4. **Say what the counts imply.** *"So enumerating substrings is sometimes reasonable — half a million
   for a thousand characters — and enumerating subsequences never is. That's why one gets a window and
   the other gets a table."*
5. **Name the technique that follows.** *"Because a substring is contiguous, two indices can represent
   it, so a sliding window gives O(n). A subsequence has holes, so nothing can represent it in two
   indices, which is why it costs a DP table."*
6. **Then solve the actual question**, having already told them you know which one it is.

### The follow-ups

**"Why is `is_subsequence` greedy but longest-common-subsequence needs DP?"**
Because of how many choices there are. In `is_subsequence` I am matching one fixed string into
another, and taking the earliest possible match is never worse — if some solution matches this
character later in B, swapping it for the earlier occurrence leaves at least as much of B for
everything that follows, so there is no decision to regret and one greedy pass suffices. In longest
common subsequence both strings are being chosen from, so when the current characters differ I have a
genuine choice: skip a character of A, or skip one of B. Skipping in A might unlock a longer match
later in B, and I cannot tell without exploring, so I evaluate both and keep the better. That is
exactly the situation dynamic programming exists for, and it takes the cost from `O(n)` to `O(m·n)`.

**"How would you count substrings with some property, without enumerating them?"**
Enumerating is `O(n²)` at best and `O(n³)` if you materialise them, so for anything large I count as I
go. The general move is: for each right endpoint, count how many left endpoints make a valid
substring, and add that to a running total. With a sliding window, if the window from `left` to
`right` is valid then every window starting at or after `left` and ending at `right` is also valid —
so this endpoint contributes `right - left + 1` to the answer in `O(1)`, and the whole thing is
`O(n)`. That trick — counting `right - left + 1` per position instead of enumerating — turns a large
family of "count the subarrays where..." problems from quadratic into linear, and it is the heart of
[day 034](../day-034-at-most-k/README.md).

**"What's the difference between longest common substring and longest common subsequence?"**
One line of the recurrence, and it follows directly from contiguity. Both build a table where
`dp[i][j]` is the answer for the first `i` characters of one string and the first `j` of the other, and
both do `dp[i-1][j-1] + 1` when the characters match. The difference is the mismatch case. For a
subsequence I carry forward the best I had — `max(dp[i-1][j], dp[i][j-1])` — because skipping a
character is allowed and does not destroy what I have built. For a substring a mismatch **breaks the
run**, so `dp[i][j] = 0` and I start again. And the answer is in a different place: for the
subsequence it is the bottom-right cell, because it is about the whole of both strings; for the
substring it is the maximum cell anywhere in the table, because the best run may have ended in the
middle.

**"A string of a million characters — how do you handle the substring problems then?"**
`O(n²)` is a trillion operations, so anything that touches every substring is out, and I need a
technique that is linear or close to it. For most of these problems the sliding window already is
linear, so it holds up: longest substring without repeats on a million characters is a million
dictionary operations, which is well under a second. What I would watch is memory rather than time —
specifically, never slicing. `s[i:j]` copies, so building substrings inside a loop turns a linear
algorithm into a quadratic one silently. I would work with the two indices and only materialise the
single answer at the end.

### A model answer

> "The distinction is one word: contiguous. A substring is a run of characters that are next to each
> other in the original. A subsequence keeps their order but is allowed to skip. So in `abcde`, `bcd`
> is both, and `ace` is a subsequence but not a substring, because `b` and `d` are missing from the
> middle. Every substring is a subsequence; the reverse is not true.
>
> For the counts: a substring is completely determined by where it starts and where it ends, and the
> end has to be at or after the start. So it's n choices of end for a start at position 0, n-1 for
> position 1, and so on — which sums to n(n+1)/2.
>
> A subsequence is a different kind of choice: for each character, independently, it's in or out. That
> is 2 multiplied by itself n times, so 2ⁿ, including the empty subsequence.
>
> The reason I'd bother deriving them rather than just stating them is that the *shape* of those two
> numbers is what decides the technique. At n = 20 it's 210 against a million. Substrings are
> quadratic, so enumerating them is sometimes a legitimate plan — half a million for a thousand-
> character string. Subsequences are exponential, so enumerating them is never a plan at any useful
> size.
>
> That falls straight out of contiguity. Because a substring is a contiguous run, two indices can
> represent it completely, which is why substring problems collapse into sliding windows and come out
> at O(n) — longest substring without repeating characters is one pass with a dictionary of last
> positions. A subsequence has holes in it, so no pair of indices can describe it, which is why
> subsequence problems need a table over pairs of positions and land at O(m·n) — longest common
> subsequence is the standard example.
>
> The one place this genuinely costs people marks is that the two words look alike in a problem
> statement. Longest common substring and longest common subsequence differ by a single line in the
> recurrence: on a mismatch, the subsequence version carries forward the best it has, and the
> substring version resets to zero because the run is broken. So the first thing I do with any of
> these is check which word was used, and if it isn't there, ask whether it has to be contiguous."

---

## 9. Recall card

- **Substring = contiguous. Subsequence = order kept, gaps allowed.** Every substring is a
  subsequence.
- **Counts: `n(n+1)/2` substrings, `2ⁿ` subsequences.** At `n = 20`, 210 against a million.
- **Contiguous → sliding window, `O(n)`. Gaps allowed → DP table, `O(m·n)`.**
- **If the word is missing, ask "does it have to be contiguous?"** — it decides the whole solution.
- **Substring vs subsequence DP differ in the mismatch line:** reset to 0, or carry the max forward.
