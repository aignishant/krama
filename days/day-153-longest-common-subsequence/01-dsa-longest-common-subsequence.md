---
day: 153
track: dsa
title: "Longest common subsequence"
phase: "Dynamic programming"
status: written
---

# Longest common subsequence

## 1. What this is, and why they ask it

Given two strings, find the length of the longest sequence of characters that appears in **both**, in order,
not necessarily contiguously.

`"abcde"` and `"ace"` share `"ace"` — length 3. The `b` and `d` are skipped in the first string, and that is
allowed, because a subsequence keeps order and may skip.

**This is the first two-dimensional DP in the course**, and that is why it is asked. Every problem so far has
had a table indexed by one thing — an amount, a position, a capacity. **Here the state is a pair: how far you
are through string one, and how far through string two.** Learning to say "`dp[i][j]` is the answer for the
first `i` characters of `a` and the first `j` of `b`" is the skill, and once you have it, edit distance, string
matching, and half the hard string problems become the same shape.

They also ask it because **it is what `diff` is.** Git's diff, the side-by-side comparison in a code review,
the DNA alignment tools in bioinformatics — all of them are LCS or a close relative. **The characters not in
the LCS are exactly the additions and deletions**, which is a genuinely satisfying thing to be able to say out
loud.

And there is one specific trap that catches almost everyone, every time: **`dp[i][j]` refers to prefix lengths,
so `dp[i][j]` compares `a[i-1]` with `b[j-1]`, not `a[i]` with `b[j]`.** That off-by-one is the entire
difficulty of implementing this correctly under pressure.

By the end of this lesson you can write the two-dimensional table and explain both branches, reconstruct the
actual subsequence, collapse the space to two rows, connect it to `diff`, and handle the family — longest
common substring, shortest common supersequence, and the palindrome trick.

---

## 2. The story

The tailor had two lists and they did not agree, and the customer was standing there.

The first list was the one Rehmat had written in his own book in March, when the order was placed. Nine items.
Two shirts, cream, full sleeve. A pair of trousers, grey. A blazer. The kurta for the boy. And so on down the
page.

The second list was the one the customer had on her phone, which she had typed the same evening from what she
remembered.

**And now, six weeks later, there was an argument about whether the blazer had ever been ordered.**

So they did the only sensible thing, which was to go through both, together, from the top.

"Two shirts, cream." — **On both. Fine.**

"Trousers, grey." — On both.

Rehmat's next line was the blazer. Her next line was the kurta.

**And here is where they stopped, because there were two ways to go.**

Either the blazer was on his list and not on hers — he had added something — **and you skip his line and carry
on comparing.** Or the kurta was on hers and not his — she had added something — **and you skip her line
instead.**

**They could not tell which, from where they were standing.** The only way to know was to try one, keep going,
and see which choice let more of the rest of the two lists line up.

So that is what they did, and it took twenty minutes and involved starting over twice.

What they ended up with, by the time the tea came, was a middle list. **Six items that were definitely on both,
in the same order.** And what was left over — the blazer on his side, the kurta and a petticoat on hers — was
the actual disagreement, and there were only three things in it instead of nine.

The customer's observation, which was the useful one, was that they had never actually needed to settle the
argument. **They only needed to find the largest part where the two lists agreed, and everything not in it was
the problem.**

---

## 3. The idea in plain English

Rehmat and his customer have just run the LCS algorithm by hand, including the moment where it branches.

**First, the definition, precisely.** A **subsequence** keeps order and may skip. A **common** subsequence is
one that appears in both strings. The **longest** common subsequence is the biggest such thing, and the
question usually asks only for its length.

**Now the state, and it is a pair, which is new.**

> **`dp[i][j]` is the length of the longest common subsequence of the first `i` characters of `a` and the first
> `j` characters of `b`.**

**Prefix lengths, not indices.** `i = 3` means "the first three characters", which are `a[0]`, `a[1]`, `a[2]`.
**So the character that `i` refers to is `a[i-1]`**, and that single fact is where every off-by-one in this
problem comes from.

**Why prefix lengths rather than indices?** Because `i = 0` then means "the empty prefix", which gives a clean
base case with no special handling. **Using indices forces you to guard against `-1` everywhere.** It is worth
choosing the convention deliberately and writing it down before coding.

**The recurrence has two cases and they map exactly onto Rehmat's two situations.**

**Case one: the characters match.** `a[i-1] == b[j-1]`. Then that character can be the last one in the common
subsequence, so:

```
dp[i][j] = dp[i-1][j-1] + 1
```

**Both lists advance together**, and you add one.

**Case two: they do not match.** Then the last character of at least one prefix is not in the LCS, and **you
cannot tell which** — that is exactly where they stopped. So try both:

```
dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**`dp[i-1][j]` skips a character of `a`. `dp[i][j-1]` skips a character of `b`.** Take whichever gives more.

**The base cases are the empty prefixes.** `dp[0][j] = 0` and `dp[i][0] = 0`: the LCS of anything with an empty
string is empty. **In code that is one row and one column of zeros, and if you allocate with `[[0] * (m+1) for
_ in range(n+1)]` you get them for free.**

**The answer is `dp[n][m]`** — the bottom-right cell, both strings fully consumed. **Unlike LIS, this one
really is the last cell**, because the state covers all of both strings rather than "ending exactly here".

**Now three things worth having ready.**

**Reconstruction.** Walk back from `dp[n][m]`. If the characters match, that character is in the LCS — record
it and move diagonally. If not, move to whichever of the two neighbours is larger. **When they are equal, pick
either; you get a different valid LCS, and there is usually more than one.**

**The space collapse.** Row `i` reads only row `i-1`, so keep two rows instead of `n+1`. `O(min(n, m))` space
by iterating with the shorter string as the inner dimension. **But you lose reconstruction** — same trade as
knapsack, and worth stating.

**And the `diff` connection**, which is what makes this feel useful rather than academic:

```
characters in the LCS         = unchanged lines
characters of a NOT in it     = DELETIONS
characters of b NOT in it     = INSERTIONS
```

**That is `diff`.** Run LCS on the lines of two files, and the reconstruction gives you the unified diff. Git
uses a refined version — Myers' algorithm — which is faster on the typical case where the files are similar,
**but the definition of "the right answer" is LCS.**

**Finally, the family, which is larger than it looks.**

**Longest common *substring*** — contiguous — is a different recurrence and easy to confuse. **On a mismatch,
the answer is 0, not the max of neighbours**, because contiguity is broken. And the answer is `max` over the
whole table, not the last cell.

**Shortest common supersequence** — the shortest string containing both as subsequences — is
`n + m - LCS(a, b)`, because the shared part is written once instead of twice. **One line, once you have LCS.**

**Longest palindromic subsequence of `s` is `LCS(s, reverse(s))`.** That is a genuinely surprising reduction
and it is asked; the reason is that a palindrome reads the same forwards and backwards, so a subsequence
common to `s` and its reverse is exactly a palindromic subsequence.

**And the minimum number of deletions to make two strings equal is `n + m - 2 × LCS`** — delete everything not
shared, from both.

---

## 4. The picture

The table for `a = "abcde"`, `b = "ace"`:

```
            ""   a    c    e         <- b, prefix lengths 0..3
       ""    0   0    0    0
        a    0   1    1    1
        b    0   1    1    1
        c    0   1    2    2
        d    0   1    2    2
        e    0   1    2    3
        ^                    ^
     a, prefix lengths    answer = dp[5][3] = 3
     0..5

  Reading one cell: dp[3][2] = 2 means
  "the LCS of 'abc' and 'ac' has length 2" — which is 'ac'.

  Row 0 and column 0 are zeros: nothing is common with an empty string.
```

The two branches, drawn on one cell:

```
                    dp[i-1][j-1]   dp[i-1][j]
                          \             |
                           \            |
                            v           v
                    dp[i][j-1] ----> dp[i][j]

  MATCH   a[i-1] == b[j-1]:
      dp[i][j] = dp[i-1][j-1] + 1        <- the DIAGONAL, plus one
      (both strings advance together)

  MISMATCH:
      dp[i][j] = max(dp[i-1][j],         <- skip a character of a
                     dp[i][j-1])         <- skip a character of b
      (Rehmat's blazer or the customer's kurta —
       you cannot tell which, so try both)
```

The off-by-one, which is the whole implementation difficulty:

```
  a = "abcde"
       01234        <- indices
       12345        <- prefix lengths

  dp[3][2] is about a[0..2] = "abc" and b[0..1] = "ac"

  the characters being COMPARED at dp[3][2] are
      a[3-1] = a[2] = 'c'
      b[2-1] = b[1] = 'c'

  NOT a[3] and b[2].

  Write "dp[i][j] uses a[i-1] and b[j-1]" at the top of your code
  before you write the loops.
```

Reconstruction, walking back:

```
  a = "abcde", b = "ace"

  start at dp[5][3] = 3
    a[4]='e', b[2]='e'  MATCH  -> take 'e', move to dp[4][2]
  dp[4][2] = 2
    a[3]='d', b[1]='c'  no     -> dp[3][2]=2 vs dp[4][1]=1 -> go UP to dp[3][2]
  dp[3][2] = 2
    a[2]='c', b[1]='c'  MATCH  -> take 'c', move to dp[2][1]
  dp[2][1] = 1
    a[1]='b', b[0]='a'  no     -> dp[1][1]=1 vs dp[2][0]=0 -> go UP to dp[1][1]
  dp[1][1] = 1
    a[0]='a', b[0]='a'  MATCH  -> take 'a', move to dp[0][0]
  dp[0][0] = 0  STOP

  collected 'e','c','a' -> reverse -> "ace"
```

LCS as diff:

```
  a = "abcde"   b = "ace"      LCS = "ace"

    a  ->  in LCS   keep
    b  ->  not      DELETE
    c  ->  in LCS   keep
    d  ->  not      DELETE
    e  ->  in LCS   keep

  as a unified diff:
      a
    - b
      c
    - d
      e

  Run this on the LINES of two files and you have written `diff`.
```

Common subsequence against common **substring**, which is the confusion:

```
  a = "abcdef"   b = "abzdef"

  longest common SUBSEQUENCE = "abdef", length 5   (skip the c and the z)
  longest common SUBSTRING   = "def",   length 3   (must be contiguous)

  the recurrences differ on ONE line:
     subsequence, mismatch:  dp[i][j] = max(dp[i-1][j], dp[i][j-1])
     substring,   mismatch:  dp[i][j] = 0            <- the run is broken

  and the ANSWER differs too:
     subsequence: dp[n][m]
     substring:   max over the WHOLE table
```

---

## 5. The code, built step by step

### The table, from the sentence

```python
def longest_common_subsequence(a: str, b: str) -> int:
    n, m = len(a), len(b)
    # dp[i][j] = LCS length of a's first i characters and b's first j
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    return dp[n][m]                           # (loops next)
```

**The `+1` in both dimensions is the empty prefix**, and allocating with zeros gives both base cases for free —
no special-case code at all.

Now the two branches:

```python
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:          # NOTE the -1 on both
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
```

**`a[i - 1]` and `b[j - 1]`.** Say it out loud while writing: "`i` is a length, so the character is at
`i` minus one."

**Loops from 1, not 0**, because row and column zero are the base cases and must not be overwritten.

### Reconstructing the subsequence

```python
def lcs_string(a: str, b: str) -> str:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result: list[str] = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])           # this character is in the LCS
            i, j = i - 1, j - 1               # move diagonally
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1                            # skipping a character of a was better
        else:
            j -= 1
    return "".join(reversed(result))
```

**`>=` rather than `>` in the tie-break is arbitrary** and it decides *which* LCS you get when several have the
same length. **Both are correct; say that rather than pretending there is one answer.**

**The walk-back is `O(n + m)`** — each step decreases `i` or `j` or both.

### The space collapse

```python
def lcs_length_two_rows(a: str, b: str) -> int:
    if len(b) > len(a):
        a, b = b, a                           # make b the shorter one
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[len(b)]
```

**`O(min(n, m))` space** after the swap, and the swap is worth doing: two strings of 10,000 and 10 characters
need 11 cells per row, not 10,001.

**And reconstruction is gone.** The rows are overwritten, so there is no table to walk back through. **If they
ask for the string, you need the full table** — or Hirschberg's algorithm, which recovers it in linear space by
divide and conquer, and is worth naming but not worth writing in an interview.

### Longest common substring, which differs on one line

```python
def longest_common_substring(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                best = max(best, dp[i][j])    # answer is the MAX, not the last cell
            # else: dp[i][j] stays 0 — the run is broken
    return best
```

**Two differences and both matter.** The mismatch case is `0`, not a `max` — contiguity is broken. And the
answer is the running maximum, not `dp[n][m]`, because the best run can end anywhere.

### The derived problems

```python
def shortest_common_supersequence_length(a: str, b: str) -> int:
    return len(a) + len(b) - longest_common_subsequence(a, b)

def min_deletions_to_make_equal(a: str, b: str) -> int:
    return len(a) + len(b) - 2 * longest_common_subsequence(a, b)

def longest_palindromic_subsequence(s: str) -> int:
    return longest_common_subsequence(s, s[::-1])
```

**Three one-liners.** The supersequence writes the shared part once instead of twice; the deletions remove
everything unshared from both sides; **and the palindrome one works because a subsequence common to `s` and its
reverse reads the same in both directions.**

### The complete solution

```python
"""Longest common subsequence, its reconstruction, and its family."""


def longest_common_subsequence(a: str, b: str) -> int:
    """dp[i][j] = LCS of a's first i characters and b's first j."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]     # row/col 0 = empty prefix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:               # i is a LENGTH, so index i-1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def lcs_string(a: str, b: str) -> str:
    """One longest common subsequence. There may be several of equal length."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result: list[str] = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(result))


def lcs_length_two_rows(a: str, b: str) -> int:
    """O(min(n, m)) space. Reconstruction is not possible from this."""
    if len(b) > len(a):
        a, b = b, a
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[len(b)]


def longest_common_substring(a: str, b: str) -> int:
    """CONTIGUOUS. Mismatch resets to 0; the answer is the table maximum."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                best = max(best, dp[i][j])
    return best


def shortest_common_supersequence_length(a: str, b: str) -> int:
    """The shared part is written once instead of twice."""
    return len(a) + len(b) - longest_common_subsequence(a, b)


def min_deletions_to_make_equal(a: str, b: str) -> int:
    """Delete everything not shared, from both sides."""
    return len(a) + len(b) - 2 * longest_common_subsequence(a, b)


def longest_palindromic_subsequence(s: str) -> int:
    """A subsequence common to s and its reverse reads the same both ways."""
    return longest_common_subsequence(s, s[::-1])


def diff(a_lines: list[str], b_lines: list[str]) -> list[str]:
    """LCS on lines is exactly what `diff` computes."""
    n, m = len(a_lines), len(b_lines)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a_lines[i - 1] == b_lines[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    out: list[str] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a_lines[i - 1] == b_lines[j - 1]:
            out.append("  " + a_lines[i - 1])
            i, j = i - 1, j - 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            out.append("+ " + b_lines[j - 1])
            j -= 1
        else:
            out.append("- " + a_lines[i - 1])
            i -= 1
    return list(reversed(out))


if __name__ == "__main__":
    print("lcs abcde/ace     :", longest_common_subsequence("abcde", "ace"))
    print("the subsequence   :", lcs_string("abcde", "ace"))
    print("two rows agrees   :", lcs_length_two_rows("abcde", "ace"))
    print("no overlap        :", longest_common_subsequence("abc", "def"))
    print("identical         :", longest_common_subsequence("abc", "abc"))
    print("empty             :", longest_common_subsequence("", "abc"))

    print("subsequence       :", longest_common_subsequence("abcdef", "abzdef"))
    print("substring         :", longest_common_substring("abcdef", "abzdef"))

    print("supersequence len :", shortest_common_supersequence_length("abac", "cab"))
    print("min deletions     :", min_deletions_to_make_equal("sea", "eat"))
    print("palindromic sub   :", longest_palindromic_subsequence("bbbab"))

    print("diff:")
    for line in diff(["import os", "x = 1", "y = 2", "print(x)"],
                     ["import os", "import sys", "y = 2", "print(y)"]):
        print("   ", line)
```

Run it and you get:

```
lcs abcde/ace     : 3
the subsequence   : ace
two rows agrees   : 3
no overlap        : 0
identical         : 3
empty             : 0
subsequence       : 5
substring         : 3
supersequence len : 5
min deletions     : 2
palindromic sub   : 4
diff:
      import os
    - x = 1
    + import sys
      y = 2
    - print(x)
    + print(y)
```

**`subsequence 5` against `substring 3` on the same input** is the distinction, made visible: `"abdef"` versus
`"def"`.

**And the `diff` output is the point of the whole lesson.** That is a real unified diff, produced by walking
back through an LCS table — the same output `git diff` gives, from thirty lines.

---

## 6. What it costs

**Time.** Two nested loops over the two lengths.

```
n rows x m columns = n x m cells
each cell: one comparison, one addition or one max     O(1)

TOTAL: O(n x m)
```

**Concretely:**

```
two strings of 1,000       1,000,000 cells      ~0.3 s in Python.  Fine.
two strings of 10,000      100,000,000 cells    ~40 s.             Too slow.
two files of 10,000 lines  100,000,000 cells    same problem.
```

**LeetCode 1143's constraint is 1,000 characters**, which is set exactly so the quadratic table passes.

**Space.**

```
full table     (n+1) x (m+1) integers
               1,001 x 1,001 = 1,002,001 cells
               Python list of lists, ~8 bytes per pointer + int objects
               -> about 40 MB

two rows       2 x (min(n,m) + 1)
               2 x 1,001 = 2,002 cells
               -> about 80 KB

500x less, same answer, and no reconstruction.
```

**And the swap matters more than it looks:**

```
a = 10,000 characters, b = 10 characters

without the swap: rows of 10,001 -> 2 x 10,001 = 20,002 cells
with the swap:    rows of 11     -> 2 x 11     = 22 cells

900x less, from one `if`.
```

**Why `diff` on real files needs something better:**

```
two source files of 5,000 lines each
  5,000 x 5,000 = 25,000,000 cells
  at 8 bytes per cell in a compact representation = 200 MB
  and ~10 seconds

Git uses MYERS' ALGORITHM instead: O((n + m) x D) where D is the
number of differences.

  two nearly-identical 5,000-line files, D = 20:
    Myers: (5,000 + 5,000) x 20 = 200,000 operations
    LCS table: 25,000,000

  125x faster, and it gets BETTER the more similar the files are —
  which is the normal case for source control.
```

**That last sentence is the good thing to say**: Myers is not a different answer, it is the same answer found
by exploring only the region of the table near the diagonal, and real diffs live near the diagonal.

**The derived problems cost nothing extra:**

```
shortest common supersequence   one LCS + one subtraction
minimum deletions               one LCS + one subtraction
longest palindromic subsequence one LCS on s and reversed(s)
                                -> O(n^2) time, O(n) space with two rows

reconstruction                  O(n + m) walk-back after the table
                                -> free in time, needs the FULL table in space
```

**And the substring version:**

```
same O(n x m) time and space
but a mismatch writes 0 instead of a max, so it is marginally faster
in practice — no max() call on the common path.
```

---

## 7. The traps

**The off-by-one, which is the defining bug of this problem.**

```python
>>> a, b = "abcde", "ace"
>>> dp = [[0] * 4 for _ in range(6)]
>>> for i in range(1, 6):
...     for j in range(1, 4):
...         if a[i] == b[j]:               # WRONG: should be a[i-1], b[j-1]
...             dp[i][j] = dp[i-1][j-1] + 1
...         else:
...             dp[i][j] = max(dp[i-1][j], dp[i][j-1])
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
IndexError: string index out of range
```

**Here it happens to raise**, because `i` reaches 5 and `a[5]` is past the end. **On other inputs it does not
raise and quietly compares the wrong characters** — which is worse. **Write "`i` is a length, so the character
is `a[i-1]`" before the loops.**

**Looping from 0 and destroying the base case.**

```python
>>> dp = [[0] * 4 for _ in range(6)]
>>> for i in range(0, 6):                  # starts at 0
...     for j in range(0, 4):
...         if i == 0 or j == 0:
...             continue                   # you now need this guard
```

**Starting at 0 forces a guard on every iteration.** Starting at 1 makes row and column zero permanently the
base case, with no runtime check at all. **One character, and it removes a whole class of bug.**

**Confusing subsequence with substring.**

```python
>>> longest_common_subsequence("abcdef", "abzdef")
5
>>> longest_common_substring("abcdef", "abzdef")
3
```

**Both are correct programs for different questions.** The word to look for in the statement is
**"contiguous"** — if it is there, a mismatch resets to zero and the answer is the table maximum, not the last
cell.

**Returning `dp[n][m]` from the substring version.**

```python
>>> # substring table for "abcdef" / "abzdef", last cell:
>>> # dp[6][6] = 3 here by luck, but on "abc"/"cba" it is 0
>>> # while the real answer is 1
```

**The substring answer can be anywhere in the table**, because the best run ends where it ends. **The
subsequence answer really is the last cell** — this is the one place where the two conventions genuinely
differ, and mixing them up gives plausible numbers.

**Expecting a unique LCS.**

```python
>>> lcs_string("abcbdab", "bdcaba")
'bcba'
```

**`"bcab"` and `"bdab"` are also length 4 and equally valid.** The tie-break in the walk-back decides which one
you get. **If a test asserts a specific string, it is asserting your tie-break, not the answer** — which is
worth saying if an interviewer challenges your output.

**Reconstruction after the space collapse.**

```python
>>> # you have `previous`, a single row of numbers.
>>> # there is nothing to walk back through.
```

**No error — you simply cannot do it.** The rows have been overwritten. **State the trade when you collapse:
"this gives me the length in linear space and gives up the reconstruction."**

**Two long strings.**

```python
>>> a = "x" * 20000
>>> b = "y" * 20000
>>> dp = [[0] * 20001 for _ in range(20001)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**400 million cells.** Read the constraint before choosing the full table — and if reconstruction is needed at
that size, the answer is Hirschberg's algorithm, not a bigger machine.

**The empty string.**

```python
>>> longest_common_subsequence("", "abc")
0
>>> lcs_string("", "abc")
''
```

**Both correct, and both free** — the `range(1, 1)` loop simply does not execute and `dp[0][3]` is already 0.
**This is the reward for choosing prefix lengths over indices**, and it is worth pointing at when explaining
the convention.

---

## 8. In the interview

### How it gets asked

- *"Find the length of the longest common subsequence of two strings."* — LeetCode 1143, the standard.
- *"Return the subsequence itself."*
- *"How is this different from longest common substring?"* — the one-line difference.
- *"Can you reduce the space?"* — and the follow-up about what you lose.
- *"How would you implement `diff`?"*
- *"Find the longest palindromic subsequence."* — the surprising reduction.

### The first ninety seconds

> "This is my first genuinely two-dimensional DP, so let me set the state up carefully, because the convention
> I choose decides how painful the code is.
>
> **`dp[i][j]` is the length of the longest common subsequence of the first `i` characters of `a` and the
> first `j` characters of `b`.**
>
> **Prefix lengths, not indices** — and I choose that deliberately. It means `i = 0` is the empty prefix, so
> the base cases are a row and a column of zeros that I get for free from the allocation. **With indices I
> would be guarding against minus one everywhere.** The price is one off-by-one: **the character `i` refers to
> is `a[i-1]`**, and I would write that down before the loops, because it is where every bug in this problem
> lives.
>
> **The recurrence has two cases.**
>
> **If `a[i-1] == b[j-1]`, that character can end the common subsequence**, so `dp[i][j] = dp[i-1][j-1] + 1` —
> the diagonal, plus one. Both strings advance together.
>
> **If they differ, then at least one of those two characters is not in the LCS, and I cannot tell which.** So
> I try both: `max(dp[i-1][j], dp[i][j-1])` — skip a character of `a`, or skip a character of `b`, whichever
> gives more.
>
> **Base cases: `dp[0][j] = dp[i][0] = 0`**, because nothing is common with an empty string.
>
> **The answer is `dp[n][m]`** — and unlike longest increasing subsequence, here it really is the last cell,
> because the state covers all of both strings rather than 'ending exactly here'.
>
> **`O(n × m)` time and space.** Two strings of a thousand is a million cells — fine. Ten thousand each is a
> hundred million and about forty seconds, so **I would check the constraints before choosing the full table.**
>
> **And I can reduce the space to two rows**, `O(min(n, m))` after swapping so the shorter string is the inner
> dimension. **But that gives up reconstruction**, so I would ask first whether they want the length or the
> string."

### The follow-ups

**"Return the subsequence itself, not just the length."**

> "That needs the full table, and the walk-back is the reverse of how it was filled.
>
> **Start at `dp[n][m]` and move backwards.** At each cell, ask the same question the fill asked.
>
> **If `a[i-1] == b[j-1]`, that character is in the LCS** — record it, and move diagonally to `dp[i-1][j-1]`,
> because that is where this cell's value came from.
>
> **Otherwise, move to whichever neighbour is larger** — up if `dp[i-1][j]` is bigger, left if `dp[i][j-1]` is.
> That retraces the `max` that was taken during the fill.
>
> **Stop when either index hits zero**, and reverse what I collected, because I built it from the end.
>
> **Cost is `O(n + m)`** — each step decreases `i` or `j` or both — so reconstruction is free in time. **What
> it costs is space**: I need the whole table, which is `O(n × m)`, so I cannot use the two-row version.
>
> **Two honest points.** **The LCS is not unique.** On `"abcbdab"` and `"bdcaba"`, `"bcba"`, `"bcab"` and
> `"bdab"` are all length four. **My tie-break — whether I go up or left when the neighbours are equal —
> decides which one I return**, and both directions are correct. If a test asserts a specific string, it is
> asserting my tie-break rather than the answer.
>
> **And if the strings are large and I need both the string and linear space**, that is Hirschberg's
> algorithm: divide and conquer on the midpoint of one string, using the two-row version to find where the
> optimal path crosses. **`O(n × m)` time and `O(min(n, m))` space.** I would name it and say I would not write
> it under time pressure unless asked."

**"How is this different from longest common substring?"**

> "One line in the recurrence and one line in the answer, and mixing them up gives plausible wrong numbers,
> so it is worth being precise.
>
> **A substring is contiguous. A subsequence is not.** On `"abcdef"` and `"abzdef"`, the longest common
> subsequence is `"abdef"`, length five — I skip the `c` and the `z`. **The longest common substring is
> `"def"`, length three**, because contiguity means the run stops dead at the mismatch.
>
> **First difference: the mismatch case.** For subsequences it is `max(dp[i-1][j], dp[i][j-1])` — I skip a
> character and carry on. **For substrings it is zero**, because a broken run is a broken run and there is
> nothing to carry.
>
> **Second difference: where the answer is.** The subsequence answer is `dp[n][m]`, the bottom-right cell,
> because the state covers both entire strings. **The substring answer is the maximum over the whole table**,
> because the best run can end anywhere and the last cell only describes runs ending at the very end of both
> strings.
>
> **Getting the second one wrong is the sneaky bug**, because on many inputs the last cell happens to be
> right.
>
> **The word to look for in the statement is 'contiguous'**, or 'substring' used precisely. And I would ask
> if it is ambiguous, because the two answers can differ by a lot.
>
> **One more thing about the substring version: there is a better algorithm.** Suffix automata or suffix
> arrays solve longest common substring in linear time, and the DP is `O(n × m)`. **For an interview the DP is
> the expected answer**, but knowing the better one exists is worth a sentence."

**"How would you implement `diff`?"**

> "`diff` **is** LCS, and I find that genuinely satisfying, so let me say why.
>
> **Run LCS on the lines of the two files rather than on characters.** The longest common subsequence of the
> lines is the set of lines that are unchanged, in order.
>
> **Then everything not in it is the change.** A line of the old file that is not in the LCS was **deleted**.
> A line of the new file that is not in the LCS was **inserted**. **That is the entire definition of a diff**,
> and the walk-back produces it directly — I just emit `-` when I move up, `+` when I move left, and a space
> when I move diagonally.
>
> **Hashing the lines first is worth doing**, because comparing line hashes is cheap and comparing long
> strings repeatedly is not.
>
> **Where the plain table fails is size.** Two source files of five thousand lines is twenty-five million
> cells — a couple of hundred megabytes and about ten seconds. **That is unacceptable for something that runs
> on every commit.**
>
> **So Git uses Myers' algorithm**, which is `O((n + m) × D)` where `D` is the number of differences. **The
> insight is that a typical diff is small** — two versions of a file differ in a handful of lines — so the
> optimal path through the table hugs the diagonal, and Myers explores outward from the diagonal instead of
> filling everything.
>
> **Concretely: two five-thousand-line files differing in twenty lines is two hundred thousand operations
> against twenty-five million. About a hundred and twenty-five times faster** — and crucially, **it gets faster
> the more similar the files are**, which is exactly the case source control cares about.
>
> **And a practical detail real diffs add: heuristics for readability.** The minimal diff is often not the most
> readable one — moving a hunk boundary by a line can make a change obviously a function insertion rather than
> a scattered set of edits. **Git's `--patience` and `--histogram` algorithms trade minimality for
> comprehensibility**, which is a nice reminder that the mathematically optimal answer is not always the
> product requirement."

### The model answer

*"You are building a plagiarism checker for student submissions. Given two documents, report how similar they
are and show which parts overlap."*

> "Let me separate the two things asked for, because they need different outputs from the same computation:
> **a similarity number, and the overlapping parts themselves.**
>
> **The core is longest common subsequence, and I would run it on tokens rather than characters.** Splitting
> into words — lowercased, punctuation stripped — means a changed comma does not break a match, and it cuts
> the input size by roughly a factor of five, which matters because the algorithm is quadratic.
>
> **The state: `dp[i][j]` is the length of the longest common token subsequence of the first `i` tokens of the
> first document and the first `j` of the second.** Prefix lengths, so `i = 0` is the empty prefix and the base
> row and column are zeros.
>
> **Match: `dp[i-1][j-1] + 1`. Mismatch: `max(dp[i-1][j], dp[i][j-1])`.** Answer at `dp[n][m]`.
>
> **The similarity score.** I would report `2 × LCS / (n + m)` — the shared fraction of the total material —
> rather than `LCS / n`, because dividing by one document's length is asymmetric and a short quote inside a
> long essay would score very differently depending on which way round you asked. **And the minimum number of
> edits to make them identical is `n + m - 2 × LCS`**, which is the same information stated as a distance.
>
> **For showing the overlaps, I need the walk-back, so I need the full table** — that rules out the two-row
> version, and I would say that explicitly as the reason.
>
> **Now the sizing, which is where the real design decision is.** Two thousand-word essays is a million cells
> — fine, a fraction of a second. **Two ten-thousand-word dissertations is a hundred million cells, about forty
> seconds and hundreds of megabytes** — and a plagiarism checker compares each submission against every other
> one. **Thirty students is 435 pairs**, and at forty seconds each that is five hours.
>
> **So the real system needs a cheap filter before the expensive comparison.** I would fingerprint each
> document — hash overlapping k-grams of tokens and keep a sample, which is winnowing — and **only run the full
> LCS on pairs whose fingerprint sets overlap enough to be worth it.** That turns 435 quadratic comparisons
> into 435 cheap set intersections plus a handful of expensive ones.
>
> **And I would raise a subtlety about what LCS actually measures here**, because it matters for the product.
> **LCS is order-sensitive and gap-tolerant**, which means it catches a copied passage with words changed
> throughout — which is what paraphrasing looks like, and is the case you most want to catch. **It does not
> catch reordered paragraphs**, because a swapped block breaks the order the algorithm depends on.
>
> **For that I would run LCS per paragraph pair rather than on the whole document**, which detects a matched
> paragraph wherever it moved to, at the cost of missing overlaps that straddle a paragraph boundary. **That is
> a real trade and I would want the product to decide it**, not the algorithm.
>
> **What I would not do is report the score alone.** Every one of these systems is wrong sometimes — shared
> quotations, standard phrasing, boilerplate assignment text — so **the output has to be the highlighted
> overlapping passages for a human to judge**, which is exactly what the reconstruction gives me and is the
> reason I kept the full table."

---

## 9. Recall card

**The first two-dimensional state: `dp[i][j]` = LCS of `a`'s first `i` characters and `b`'s first `j`.**
**Prefix lengths, not indices** — so `i = 0` is the empty prefix and the zero row and column *are* the base
cases, free from the allocation. **The price is one off-by-one: the character is `a[i-1]`**, and that is where
every bug lives.

**Match → `dp[i-1][j-1] + 1` (the diagonal). Mismatch → `max(dp[i-1][j], dp[i][j-1])`** — skip a character of
`a` or of `b`, because you cannot tell which is out. **The answer is `dp[n][m]`**, genuinely the last cell,
unlike LIS.

**`O(n × m)` time and space; two rows gives `O(min(n, m))` after swapping so the shorter string is inner** —
10,000 × 10 becomes 22 cells instead of 20,002. **The collapse gives up reconstruction** (Hirschberg's
algorithm recovers it in linear space).

**Reconstruction walks back from `dp[n][m]`:** match → take the character, move diagonally; else move to the
larger neighbour. `O(n + m)`. **The LCS is not unique** — the tie-break picks which one.

**Substring differs on exactly two lines:** mismatch writes **0** (contiguity broken) and the answer is the
**table maximum**, not the last cell. `"abcdef"`/`"abzdef"` → subsequence 5, substring 3.

**LCS is `diff`:** in the LCS = unchanged, unmatched in `a` = deletions, unmatched in `b` = insertions. **Git
uses Myers, `O((n+m)×D)`**, which gets faster the more similar the files are — 125× on two 5,000-line files
differing in 20. **Derived one-liners: supersequence `n+m-LCS`; min deletions `n+m-2·LCS`; longest palindromic
subsequence `LCS(s, reversed(s))`.**
