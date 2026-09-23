---
day: 155
track: dsa
title: "String DP: palindromic substrings"
phase: "Dynamic programming"
status: written
---

# String DP: palindromic substrings

## 1. What this is, and why they ask it

**A palindrome reads the same forwards and backwards.** `"racecar"`, `"abba"`, `"a"`. The questions are: how
many palindromic substrings does a string contain, and what is the longest one?

They ask it because **it is the first DP where the table is not filled row by row.** Everything so far has
gone left to right, top to bottom. **Here, `dp[i][j]` depends on `dp[i+1][j-1]` — a cell below and to the
left** — so filling in the natural order reads cells that have not been computed yet. **You have to fill by
substring length, shortest first**, and working out that you must is the lesson.

The other reason is that **the best solution is not the DP at all.** Expand-around-centre uses no table, is
five lines shorter, runs in the same `O(n²)` time and uses `O(1)` space instead of `O(n²)`. **A candidate who
writes the table and then says "actually there is a better way" is demonstrating exactly the judgement being
tested** — and a candidate who only knows the table will be asked to reduce the space and will not be able to.

And there is a third solution, Manacher's algorithm, which is genuinely `O(n)`. **You will not be asked to
write it.** You may well be asked whether you know it exists, and the right answer is a sentence.

By the end of this lesson you can write the interval DP and explain the fill order, write expand-around-centre
and say why it is better, handle the even/odd centre problem, count palindromic substrings, and name where
each approach stops.

---

## 2. The story

Ilyas painted signboards, and the man who came in on Tuesday wanted his shop name painted on both sides of a
board that would hang out over the street.

**Both sides. So people walking up the road and people walking down it would both see it.**

Ilyas said that was fine and it would cost double, because it was two paintings.

And the man, who had clearly thought about this, said no it would not, because he had chosen the name so that
it did not need two.

He wrote it out. **MALAYALAM.**

Ilyas looked at it for a while, and then did the thing he had done for twenty years without ever having a name
for it. **He put a finger at each end of the word and moved them inwards.**

M and M. Same.

A and A. Same.

L and L. Same.

A and A. Same.

**And the Y in the middle, on its own, with nothing to match against.**

"It works," he said.

Then, because it was Tuesday afternoon and there was nothing else to do, they started trying other names, and
this is where it got interesting.

Because the man's brother's shop was called **KANAKA**, and Ilyas put his fingers on the ends — K and A, no —
and said it did not work. **But the man pointed out that ANA in the middle of it did.** And so did KANAK if
you dropped the last letter.

**So one word had bits inside it that worked, even though the whole thing did not.**

They spent about an hour on it. And the method they ended up with, without discussing it, was this: **check
the little ones first.** Every single letter works on its own, obviously. Then every pair — same letter twice
or nothing. **And then, for anything longer, you only had to check the two ends, because you had already
worked out whether the bit inside was good.**

Ilyas's wife, who came in at five and was told about the afternoon, said the obvious thing.

**"Why are you starting from the ends? Start in the middle and walk outwards. That is where it is either going
to work or not."**

---

## 3. The idea in plain English

Ilyas has just described the DP, his wife has just described expand-around-centre, and she is right.

**First the definitions.** A **substring** is contiguous — `"aba"` is a substring of `"xabay"`, but `"aa"` is
not. That matters, because a **subsequence** may skip and gives a different answer to almost every question
here.

**The DP first, because it is what gets asked.**

> **`dp[i][j]` is `True` if the substring from index `i` to index `j` inclusive is a palindrome.**

**The recurrence is Ilyas's method, exactly:**

```
dp[i][j] = (s[i] == s[j]) AND dp[i+1][j-1]
```

**The two ends must match, and the bit inside must already be a palindrome.** That is the whole rule.

**And the base cases are the small ones he did first.** Every single character is a palindrome: `dp[i][i] =
True`. Every pair is a palindrome exactly when the two characters are equal: `dp[i][i+1] = (s[i] == s[i+1])`.

**Now the part that is new: the fill order.**

**`dp[i][j]` reads `dp[i+1][j-1]`** — a larger `i` and a smaller `j`. **In a table filled left to right, top to
bottom, that cell has not been computed yet.** Fill in the natural order and you read a `False` that means
"not yet computed" rather than "not a palindrome", and every long palindrome is missed.

**No error. Just answers that are too small.**

**Two fill orders work, and both are worth knowing:**

- **By length.** Handle all substrings of length 1, then all of length 2, then 3, and so on. **When you reach
  length `L`, everything of length `L-2` is done.** This is the version to write, because the reason is
  visible in the loop.
- **By decreasing `i`.** Loop `i` from `n-1` down to 0, and `j` from `i` upwards. Then `dp[i+1][...]` — the row
  below — is always already complete. **Shorter to write, and the reason is less obvious**, which is why the
  length version is better in an interview.

**That is `O(n²)` time and `O(n²)` space.**

**And now the better solution, which is Ilyas's wife.**

**Every palindrome has a centre.** Stand at the centre and walk outwards while the characters match. **When
they stop matching, you have found the longest palindrome centred there.** Do that for every possible centre
and take the best.

**The catch is that there are two kinds of centre**, and this is the detail that catches people.

**An odd-length palindrome has a character at its centre** — `"aba"` is centred on the `b`. **An even-length
one has a gap** — `"abba"` is centred between the two `b`s, on nothing.

**So there are `2n - 1` centres**, not `n`: `n` characters and `n - 1` gaps. **Checking only the characters
finds every odd palindrome and misses every even one**, which means `"abba"` reports 2 instead of 4 — and,
again, no error.

**The cost is the same `O(n²)` in time** — `2n - 1` centres, each expanding up to `n/2` — **and `O(1)` in
space, because there is no table at all.**

**So the DP costs `n²` memory and buys nothing.** At `n = 1000` that is a million booleans against four
variables. **Say that out loud when you offer the second solution; it is the point.**

**Counting palindromic substrings falls out of either.** With the DP, count the `True` cells. With expansion,
count every successful step outwards — **each one is a distinct palindromic substring**, so incrementing inside
the while loop is the entire change.

**And the third solution: Manacher's algorithm, which is `O(n)`.**

The idea in one sentence: **as you scan left to right, you keep track of the rightmost palindrome found so
far, and inside it you can reuse the answer from the mirrored position instead of expanding from scratch.**

**Nobody expects you to write it.** They may ask whether an `O(n)` solution exists, and "yes, Manacher's, it
reuses mirrored results inside a known palindrome, and I would not write it from memory" is a complete and
honest answer.

**Finally, the neighbouring problems, because they are easy to confuse.**

**Longest palindromic *subsequence*** — may skip characters — is **not** this. It is `LCS(s, reversed(s))` from
[day 153](../day-153-longest-common-subsequence/README.md), and it is a different table with a different
recurrence. `"character"` has a longest palindromic substring of `"carac"`, length 5, and a longest palindromic
*subsequence* of `"carac"` too — but on `"bbbab"` the substring is `"bbb"` (3) and the subsequence is `"bbbb"`
(4).

**Palindrome partitioning** — the fewest cuts to split a string into palindromes — uses this exact table as a
subroutine, which is the most common way the table actually earns its place.

---

## 4. The picture

The dependency that forces the fill order:

```
        j ->
        0    1    2    3    4
   i  +----+----+----+----+----+
   0  |    |    |  ? |    |    |     dp[0][2] needs dp[1][1]
      +----+----+----+----+----+
   1  |    | X  |    |    |    |     X is BELOW and to the LEFT
      +----+----+----+----+----+
   2  |    |    |    |    |    |
      +----+----+----+----+----+

  Filling left-to-right, top-to-bottom reaches dp[0][2] BEFORE dp[1][1].
  It reads False meaning "not computed yet", not "not a palindrome".

  -> every palindrome longer than 2 is missed
  -> no error, just answers that are too small
```

Filling by length, which makes the reason visible:

```
  s = "aabaa"

  length 1:  dp[0][0] dp[1][1] dp[2][2] dp[3][3] dp[4][4]   all True
  length 2:  dp[0][1]='aa' T   dp[1][2]='ab' F
             dp[2][3]='ba' F   dp[3][4]='aa' T
  length 3:  dp[0][2]='aab': s[0]='a', s[2]='b'  ->  F
             dp[1][3]='aba': s[1]=s[3]='a' AND dp[2][2]=T  ->  T
             dp[2][4]='baa': s[2]='b', s[4]='a'  ->  F
  length 4:  dp[0][3]='aaba': s[0]='a', s[3]='a' AND dp[1][2]=F  ->  F
             dp[1][4]='abaa': s[1]='a', s[4]='a' AND dp[2][3]=F  ->  F
  length 5:  dp[0][4]='aabaa': s[0]=s[4]='a' AND dp[1][3]=T  ->  T

  answer: longest is "aabaa", length 5
  count of True cells = 5 + 2 + 1 + 0 + 1 = 9 palindromic substrings
```

Expand around centre, and the two kinds:

```
  s = "aba"                        s = "abba"

  ODD centre, at index 1:          EVEN centre, between 1 and 2:

    a  b  a                          a  b  b  a
       ^                                ^  ^
    left=1, right=1                  left=1, right=2
    expand: s[0]='a' == s[2]='a'     expand: s[1]='b' == s[2]='b'  ok
    -> "aba", length 3               -> "bb", length 2
                                     expand: s[0]='a' == s[3]='a'  ok
                                     -> "abba", length 4

  THERE ARE 2n - 1 CENTRES:
     n characters (odd palindromes)
     n - 1 gaps   (even palindromes)

  Checking only characters finds "aba" and reports 2 for "abba".
  No error. Just wrong.
```

The centres, enumerated:

```
  s = a  b  b  a
      0  1  2  3

  centres:  [0]  [0,1]  [1]  [1,2]  [2]  [2,3]  [3]
             ^     ^                  ^
           char   gap                gap between the two b's
                                     -> this is the one that finds "abba"

  7 centres for a 4-character string. 2n - 1.
```

Counting, which is one line inside the expansion:

```
  s = "aaa", expanding from centre 1 (the middle 'a'):

    step 0: "a"    at [1,1]   -> count 1
    step 1: "aaa"  at [0,2]   -> count 1

  every successful expansion IS a distinct palindromic substring,
  so `count += 1` inside the while loop is the whole change.

  total for "aaa":
    centres [0]:"a"  [0,1]:"aa"  [1]:"a","aaa"  [1,2]:"aa"  [2]:"a"
    = 6 palindromic substrings
```

The three approaches, compared:

```
                        time        space      lines   would I write it?
  interval DP           O(n^2)      O(n^2)     ~12     if partitioning too
  expand around centre  O(n^2)      O(1)       ~10     YES — default
  Manacher              O(n)        O(n)       ~30     no, but I'd name it

  The DP costs n^2 memory and buys nothing over expansion.
  At n = 1,000 that is 1,000,000 booleans against 4 variables.
```

---

## 5. The code, built step by step

### The interval DP, filled by length

```python
def longest_palindrome_dp(s: str) -> str:
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True                       # every character alone
    start, best = 0, 1
```

**Length-1 first**, because everything longer depends on it. **`best = 1` because any non-empty string has a
palindrome of at least one character.**

```python
    for i in range(n - 1):                    # length 2
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, best = i, 2
```

**Length 2 is a separate base case**, because `dp[i+1][j-1]` for a length-2 substring would be `dp[i+1][i]` —
an empty range, with `i+1 > j-1` — and reading it is meaningless.

```python
    for length in range(3, n + 1):            # THEN by increasing length
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > best:
                    start, best = i, length
    return s[start:start + best]
```

**`for length in range(3, n+1)` is the whole point.** When you compute a substring of length `L`, everything
of length `L-2` is already done — **which is exactly what `dp[i+1][j-1]` is.**

### Expand around centre, which is what to write

```python
def expand(s: str, left: int, right: int) -> tuple[int, int]:
    """Widen while the ends match. Returns the widest [start, end) found."""
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right                    # step back inside the last match
```

**`left + 1` and `right` because the loop overshoots by one on each side** before it stops — that off-by-one is
the only fiddly part, and returning a half-open range makes the arithmetic clean.

```python
def longest_palindrome(s: str) -> str:
    if len(s) < 2:
        return s
    start, end = 0, 1
    for centre in range(len(s)):
        for lo, hi in (expand(s, centre, centre),        # odd: on a character
                       expand(s, centre, centre + 1)):   # even: on the gap
            if hi - lo > end - start:
                start, end = lo, hi
    return s[start:end]
```

**Two expansions per index — one odd, one even — is the `2n - 1` centres.** **Doing only the first finds every
odd palindrome and misses every even one**, and `"abba"` returns `"bb"`.

**`O(1)` space. No table.**

### Counting palindromic substrings

```python
def count_palindromic_substrings(s: str) -> int:
    total = 0
    for centre in range(len(s)):
        for left, right in ((centre, centre), (centre, centre + 1)):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                total += 1                    # each expansion is one substring
                left -= 1
                right += 1
    return total
```

**`total += 1` inside the while loop is the entire difference from the previous function.** Every successful
step outwards is one more distinct palindromic substring.

### Palindrome partitioning, where the table earns its place

```python
def min_cut(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):            # decreasing i: row below is done
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    cuts = [0] * n
    for j in range(n):
        if is_pal[0][j]:
            cuts[j] = 0                       # the whole prefix is a palindrome
        else:
            cuts[j] = min(cuts[i - 1] + 1 for i in range(1, j + 1) if is_pal[i][j])
    return cuts[n - 1]
```

**This is why you learn the table.** Expansion gives you the longest palindrome; **it does not give you
constant-time "is `s[i..j]` a palindrome?"**, and partitioning asks that `O(n²)` times.

**Note the alternative fill order here — `i` decreasing** — with `j - i < 2` folding both base cases into one
condition.

### The complete solution

```python
"""Palindromic substrings: three approaches, and where each one belongs."""


def expand(s: str, left: int, right: int) -> tuple[int, int]:
    """Widen while the ends match. Returns a half-open [start, end)."""
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right                    # the loop overshoots by one


def longest_palindrome(s: str) -> str:
    """Expand around centre. O(n^2) time, O(1) space. The default answer."""
    if len(s) < 2:
        return s
    start, end = 0, 1
    for centre in range(len(s)):
        for lo, hi in (expand(s, centre, centre),        # odd-length
                       expand(s, centre, centre + 1)):   # even-length
            if hi - lo > end - start:
                start, end = lo, hi
    return s[start:end]


def count_palindromic_substrings(s: str) -> int:
    """Every successful expansion is one distinct palindromic substring."""
    total = 0
    for centre in range(len(s)):
        for left, right in ((centre, centre), (centre, centre + 1)):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                total += 1
                left -= 1
                right += 1
    return total


def longest_palindrome_dp(s: str) -> str:
    """The interval DP. O(n^2) space, filled by INCREASING LENGTH."""
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True                       # length 1
    start, best = 0, 1
    for i in range(n - 1):                    # length 2 — its own base case
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, best = i, 2
    for length in range(3, n + 1):            # then longest last
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > best:
                    start, best = i, length
    return s[start:start + best]


def palindrome_table(s: str) -> list[list[bool]]:
    """is_pal[i][j] for every pair. Filled with DECREASING i."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):            # row i+1 is already complete
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True
    return is_pal


def min_cut(s: str) -> int:
    """Fewest cuts so every piece is a palindrome. Needs the TABLE, not expansion."""
    n = len(s)
    if n < 2:
        return 0
    is_pal = palindrome_table(s)
    cuts = [0] * n
    for j in range(n):
        if is_pal[0][j]:
            cuts[j] = 0
        else:
            cuts[j] = min(cuts[i - 1] + 1 for i in range(1, j + 1) if is_pal[i][j])
    return cuts[n - 1]


def longest_palindromic_subsequence(s: str) -> int:
    """NOT the same problem: a subsequence may skip. This is LCS(s, reversed(s))."""
    t = s[::-1]
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][n]


if __name__ == "__main__":
    for word in ["malayalam", "kanaka", "babad", "cbbd", "abba", "a", ""]:
        print(f"{word!r:12} longest: {longest_palindrome(word)!r:12}"
              f" count: {count_palindromic_substrings(word)}")

    print("dp agrees on babad :", longest_palindrome_dp("babad"))
    print("dp agrees on abba  :", longest_palindrome_dp("abba"))

    print("odd-only on 'abba' :", max(
        (expand("abba", c, c) for c in range(4)), key=lambda p: p[1] - p[0]))

    print("min cuts 'aab'     :", min_cut("aab"))
    print("min cuts 'abccbaa' :", min_cut("abccbaa"))

    print("substring  'bbbab' :", longest_palindrome("bbbab"))
    print("subsequence 'bbbab':", longest_palindromic_subsequence("bbbab"))
```

Run it and you get:

```
'malayalam'  longest: 'malayalam'  count: 15
'kanaka'     longest: 'kanak'      count: 9
'babad'      longest: 'bab'        count: 7
'cbbd'       longest: 'bb'         count: 5
'abba'       longest: 'abba'       count: 6
'a'          longest: 'a'          count: 1
''           longest: ''           count: 0
dp agrees on babad : bab
dp agrees on abba  : abba
odd-only on 'abba' : (0, 1)
min cuts 'aab'     : 1
min cuts 'abccbaa' : 1
substring  'bbbab' : bbb
subsequence 'bbbab': 4
```

**`odd-only on 'abba'` returning a length-1 result is the even-centre bug, made visible** — without the second
expansion, the longest palindrome in `"abba"` is reported as a single character.

**And the last two lines are the substring/subsequence distinction**: `"bbb"` is 3 as a substring, and the
subsequence `"bbbb"` is 4.

---

## 6. What it costs

**Expand around centre.**

```
centres: 2n - 1
each expansion: at most n/2 steps

worst case ("aaaa...a", all identical):
  2n - 1 centres x n/2 steps = O(n^2)

typical case (random text):
  most expansions stop after 1-2 steps
  -> close to O(n) in practice
```

**Concretely:**

```
n = 1,000     worst case ~1,000,000 steps    ~0.2 s
n = 10,000    worst case ~100,000,000        ~20 s
n = 100,000   worst case ~10^10              impossible

on ordinary English text, n = 100,000 finishes in well under a second,
because expansions terminate almost immediately.
```

**That gap between worst case and typical is worth mentioning**: the quadratic bound is real and almost never
reached outside adversarial input.

**Space: `O(1)`.** Four integers. **No allocation at all**, which is the whole argument.

**The interval DP.**

```
time:  n^2 / 2 cells, O(1) each        = O(n^2)   — same as expansion
space: n x n booleans                  = O(n^2)   — and this is the problem

n = 1,000:   1,000,000 booleans
             Python list of lists: ~8 bytes per pointer + shared bool objects
             -> about 40 MB

against expansion's 4 integers.
```

```
n = 10,000:  100,000,000 cells -> ~4 GB
             MemoryError before it starts
```

**Same time, `n²` more memory, and no additional answer.** That comparison is the whole reason to offer
expansion.

**Where the table does earn its place:**

```
palindrome partitioning: needs "is s[i..j] a palindrome?" answered
                         O(n^2) times

  with the table:      O(1) per question, after O(n^2) to build
  with expansion:      O(n) per question -> O(n^3) overall

  n = 1,000:  10^6 with the table, 10^9 without.
```

**Counting palindromic substrings:**

```
same expansion, one increment inside the loop
-> O(n^2) worst case, O(1) space, identical constants

the DP version counts True cells: O(n^2) time AND space
-> the same answer for n^2 more memory
```

**Manacher's algorithm:**

```
O(n) time, O(n) space

n = 1,000,000:
  Manacher:  ~1,000,000 steps        ~0.5 s
  expansion: worst case ~10^12       impossible
             typical text ~2,000,000  ~1 s

-> Manacher wins decisively only on ADVERSARIAL input at large n.
   On real text, expansion is already near-linear.
```

**That is the honest framing**, and it is why nobody makes you write Manacher: the case where it matters is
rare.

**The subsequence version, for contrast:**

```
longest palindromic SUBSEQUENCE = LCS(s, reversed(s))
  O(n^2) time, O(n^2) space (or O(n) with two rows)

  and there is no expand-around-centre equivalent, because
  a subsequence has no contiguous centre to expand from.
```

---

## 7. The traps

**Filling the table in the natural order.**

```python
>>> s = "aabaa"
>>> n = 5
>>> dp = [[False] * n for _ in range(n)]
>>> for i in range(n):
...     dp[i][i] = True
>>> for i in range(n):                        # natural order: WRONG
...     for j in range(i + 1, n):
...         dp[i][j] = s[i] == s[j] and (j - i == 1 or dp[i+1][j-1])
>>> dp[0][4]
False
```

**`"aabaa"` is a palindrome and the table says it is not.** `dp[0][4]` needs `dp[1][3]`, which is computed
later in this order, so it reads `False` meaning "not yet". **No error, an answer that is too small**, and it
only shows on palindromes longer than three.

**Missing the even centres.**

```python
>>> max((expand("abba", c, c) for c in range(4)), key=lambda p: p[1] - p[0])
(0, 1)
```

**One character, for a string that is entirely a palindrome.** **`2n - 1` centres, not `n`** — and the version
that only checks characters passes every test whose answer happens to be odd-length.

**The off-by-one when the expansion stops.**

```python
>>> def bad_expand(s, left, right):
...     while left >= 0 and right < len(s) and s[left] == s[right]:
...         left -= 1
...         right += 1
...     return left, right                    # forgot the step back
>>> bad_expand("aba", 1, 1)
(-1, 3)
>>> "aba"[-1:3]
'a'
```

**The loop always overshoots by one on each side before the condition fails.** Return `left + 1, right` — and
note that the negative index does not raise, it silently slices from the end.

**Confusing substring with subsequence.**

```python
>>> longest_palindrome("bbbab")
'bbb'
>>> longest_palindromic_subsequence("bbbab")
4
```

**3 against 4.** `"bbbb"` is a valid subsequence — skipping the `a` — and not a substring. **Read the problem
statement for the word "contiguous" or "substring"**, because the two answers differ and both look right.

**Treating length 2 with the general rule.**

```python
>>> # dp[i][j] = s[i] == s[j] and dp[i+1][j-1]
>>> # for j = i + 1, that is dp[i+1][i] — an empty range, i+1 > i
>>> dp = [[False] * 3 for _ in range(3)]
>>> dp[2][1]                                  # never set, and meaningless
False
```

**`dp[i+1][j-1]` with `j = i+1` reads a cell where the start is past the end.** It is `False` by default, so
`"aa"` is reported as not a palindrome. **Either handle length 2 as its own base case, or use the
`j - i < 2 or ...` guard** — both work, and the guard is shorter.

**Case and punctuation, which is the real-world version.**

```python
>>> longest_palindrome("A man, a plan, a canal: Panama")
' a '
```

**Correct for the string as given, and not what anyone means.** The classic palindrome question normalises
first — lowercase, keep only alphanumerics — and **doing that unasked is wrong too.** Ask.

**Very long strings with the DP.**

```python
>>> dp = [[False] * 50000 for _ in range(50000)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**2.5 billion cells.** Expansion handles the same input in constant space, which is why the constraint on `n`
should decide the approach before you start.

**The empty string.**

```python
>>> longest_palindrome("")
''
>>> count_palindromic_substrings("")
0
```

**Both correct and both free**, because the guard returns early and the loop does not execute. **The DP
version without its `if n < 2` guard would raise on `s[start:start+best]` with `best = 1`** — worth checking.

---

## 8. In the interview

### How it gets asked

- *"Find the longest palindromic substring."* — LeetCode 5, one of the most-asked problems anywhere.
- *"Count the palindromic substrings."* — LeetCode 647.
- *"Can you do it in `O(1)` space?"* — the follow-up that expansion answers and the DP cannot.
- *"Is there a linear solution?"* — the Manacher question.
- *"What is the fewest cuts to split it into palindromes?"* — where the table is required.
- *"How is this different from the longest palindromic subsequence?"*

### The first ninety seconds

> "I would offer two solutions, because the obvious DP is not the one I would write, and the reason is worth
> stating.
>
> **The DP first.** `dp[i][j]` is true if the substring from `i` to `j` is a palindrome. **The recurrence is:
> the two ends match and the bit inside is already a palindrome** — `s[i] == s[j] and dp[i+1][j-1]`. Base
> cases: every single character is a palindrome, and a pair is one when the characters are equal.
>
> **The interesting part is the fill order**, and this is the thing that is new here. **`dp[i][j]` depends on
> `dp[i+1][j-1]`, which is below and to the left** — so if I fill left to right, top to bottom, I read a cell
> that has not been computed yet. **It is `False` meaning 'not yet', not `False` meaning 'not a palindrome',
> and every long palindrome is silently missed.**
>
> **So I fill by increasing substring length** — all the length-1s, then all the length-2s, then 3 — because
> when I compute a substring of length `L`, everything of length `L-2` is already done. **That is exactly what
> the recurrence reads.**
>
> **`O(n²)` time and `O(n²)` space.**
>
> **And now the better solution, which I would actually write.** **Every palindrome has a centre.** Stand at
> the centre, walk outwards while the characters match, and when they stop you have the longest palindrome
> centred there. Do it for every centre.
>
> **The catch is that there are two kinds of centre and it is easy to miss one.** An odd-length palindrome is
> centred on a character; an even-length one is centred on the gap between two characters. **So there are
> `2n - 1` centres, not `n`** — and checking only the characters reports `"abba"` as a single letter, with no
> error.
>
> **Same `O(n²)` time, and `O(1)` space** — four variables instead of a million booleans at `n = 1,000. So the
> DP costs `n²` memory and buys nothing.**
>
> **The one case where I would build the table anyway is palindrome partitioning**, where I need constant-time
> 'is this range a palindrome' answered `O(n²)` times — with expansion that would be `O(n³)`.
>
> **And there is an `O(n)` algorithm, Manacher's.** I know what it does — it reuses mirrored results inside a
> known palindrome — and I would not write it from memory unless you want it.
>
> **One question before I code: substring or subsequence?** They are different problems with different
> answers."

### The follow-ups

**"Why can't you fill the table in the normal order?"**

> "Because of which cell the recurrence reads, and this is the first time in dynamic programming that the
> natural loop order is wrong.
>
> **`dp[i][j] = s[i] == s[j] and dp[i+1][j-1]`.** That dependency is at a **larger** `i` and a **smaller** `j`
> — one row down, one column left.
>
> **In a left-to-right, top-to-bottom fill, I reach `dp[0][4]` in the very first row, and `dp[1][3]` is in the
> second row and has not been computed.** So I read the initialised `False`, which means 'not yet', and treat
> it as 'not a palindrome'.
>
> **Concretely, on `"aabaa"`: `dp[0][4]` is the whole string, which is a palindrome, and the natural order
> reports `False`.** No exception, no warning — the answer is just too small, and only for palindromes longer
> than three, which is exactly the case a short test would not cover.
>
> **The fix is to fill by increasing substring length.** All substrings of length 1, then length 2, then 3.
> **When I compute a substring of length `L`, everything of length `L-2` is finished** — which is precisely
> what `dp[i+1][j-1]` is, since it is two characters shorter.
>
> **There is a second fill order that also works: iterate `i` from `n-1` down to 0, and `j` from `i` upwards.**
> Then row `i+1` is always complete when I need it. **It is shorter to write and the reason is less obvious**,
> so I would use the length version in an interview and mention the other.
>
> **The general lesson is worth naming**, because it recurs in every interval DP — matrix chain
> multiplication, burst balloons, optimal binary search trees. **The fill order must follow the dependency
> direction, and when the state is a range, that means shortest ranges first.**"

**"Can you do it in `O(1)` space?"**

> "Yes, and that solution is also simpler than the table — which is why I would offer it first if I had not
> already.
>
> **Every palindrome has a centre. Stand there and walk outwards while the characters match.** When they stop
> matching, or I run off either end, I have the longest palindrome centred at that point. Do that for every
> centre and keep the best.
>
> **Two kinds of centre, and this is the part that catches people.** `"aba"` is centred on the `b` — a
> character. `"abba"` is centred between the two `b`s — a gap, on nothing at all.
>
> **So the loop does two expansions per index: one starting at `(i, i)` for odd lengths, one at `(i, i+1)` for
> even.** That is `2n - 1` centres — `n` characters and `n-1` gaps.
>
> **Missing the even case is the classic bug**, and it is invisible on any test whose answer happens to be
> odd-length. On `"abba"` the odd-only version returns a single character.
>
> **The other fiddly bit is the off-by-one when the expansion stops.** The while loop always overshoots by one
> on each side before the condition fails, so the answer is `left + 1` to `right`, not `left` to `right`. **And
> in Python a negative `left` does not raise — it silently slices from the end of the string**, so the bug
> gives a wrong answer rather than an error.
>
> **Cost: same `O(n²)` worst case** — `2n-1` centres, each expanding up to `n/2` — **and `O(1)` space, four
> integers.**
>
> **Worth adding: the worst case needs adversarial input.** On a string of a thousand identical characters
> every expansion runs the full width. **On ordinary text expansions stop after one or two steps**, so it is
> close to linear in practice, and `n = 100,000` finishes in well under a second.
>
> **And counting palindromic substrings is the same code with one extra line** — `count += 1` inside the while
> loop, because every successful step outwards is one more distinct palindromic substring."

**"How is this different from the longest palindromic subsequence?"**

> "Different problem, different algorithm, different answer — and the words are close enough that I would
> confirm which one is being asked before writing anything.
>
> **A substring is contiguous. A subsequence may skip characters.**
>
> **On `"bbbab"`: the longest palindromic substring is `"bbb"`, length three.** The longest palindromic
> **subsequence** is `"bbbb"`, length four — take the three `b`s at the start and the one at the end, skipping
> the `a`. **Both are correct answers to different questions.**
>
> **The algorithms have nothing in common.** For the substring I expand around centres, because a substring
> has a physical middle and grows outwards from it. **A subsequence has no contiguous centre**, so there is
> nothing to expand from and that approach simply does not apply.
>
> **The subsequence version is `LCS(s, reversed(s))`.** That reduction is worth being able to justify: a
> palindrome reads the same forwards and backwards, so **a subsequence that appears in both `s` and its
> reverse is exactly a palindromic subsequence.** Run the standard longest-common-subsequence table and the
> answer falls out.
>
> **Cost: `O(n²)` time and `O(n²)` space, or `O(n)` space with two rows** — but then no reconstruction.
>
> **There is also a direct interval DP for it** — `dp[i][j]` is the longest palindromic subsequence within
> `s[i..j]`, with `dp[i][j] = dp[i+1][j-1] + 2` when the ends match and `max(dp[i+1][j], dp[i][j-1])`
> otherwise. **Same fill-by-length requirement as today's table**, and it is the version I would write if I
> also needed the subsequence itself.
>
> **The tell in the problem statement is the word 'substring' or 'contiguous'.** If it is absent and the
> examples skip characters, it is the subsequence version."

### The model answer

*"Given a string, find the longest palindromic substring. Then tell me how you would handle a ten-megabyte
input."*

> "Let me confirm one thing first, because it changes the answer: **substring, so contiguous — not a
> subsequence.** `"bbbab"` gives `"bbb"`, not four.
>
> **I would write expand-around-centre, and I want to say why rather than just writing it.**
>
> **The textbook answer is an interval DP** where `dp[i][j]` says whether `s[i..j]` is a palindrome, with the
> rule that the two ends match and the inside is already a palindrome. **It has to be filled by increasing
> substring length**, because the recurrence reads a cell below and to the left, and the natural loop order
> reads it before it exists — silently, producing answers that are too small.
>
> **That is `O(n²)` time and `O(n²)` space. Expansion is `O(n²)` time and `O(1)` space, and it is shorter.**
> So the table costs a million booleans at `n = 1,000` and buys nothing.
>
> **The algorithm: every palindrome has a centre, so stand at each centre and walk outwards while the ends
> match.** Two expansions per index — one on the character for odd lengths, one on the gap for even —
> **`2n - 1` centres, and missing the even ones is the classic bug that reports `"abba"` as a single letter.**
>
> **Now the ten megabytes, which is the real question.**
>
> **Ten million characters. The worst case for expansion is `O(n²)` — that is `10^14` steps, which is not
> happening.** So the first thing I would establish is **what the data actually looks like**, because the
> worst case needs adversarial input.
>
> **On ordinary text, expansions terminate after one or two steps almost everywhere**, so the real cost is
> close to `O(n)` and ten megabytes finishes in a few seconds. **On a file of ten million identical
> characters, it does not finish at all.** Those are wildly different situations and the constraint alone does
> not tell me which I have.
>
> **If the input can be adversarial, the answer is Manacher's algorithm**, which is genuinely `O(n)`. **The
> idea is that as you scan left to right you track the rightmost palindrome found so far, and for a position
> inside it you can reuse the result from the mirrored position instead of expanding from scratch** — so total
> work is linear. **I would look it up rather than write it from memory**, and I would say that plainly rather
> than produce a half-remembered version, because it is exactly the kind of code that is subtly wrong.
>
> **Two engineering points that matter more than the algorithm at this size.**
>
> **Memory.** Ten megabytes of text is fine; **the DP table for it would be `10^14` cells, so the table
> approach is not merely slower, it is impossible** — which settles the choice before any timing argument.
>
> **And streaming.** If the input arrives as a stream rather than a string, **none of these work as written**,
> because both need random access backwards. A palindrome can span any distance, so **there is no bounded
> window that guarantees correctness** — I would have to buffer, and I would want to know the maximum plausible
> palindrome length to size that buffer, or accept that I only find palindromes shorter than it.
>
> **And I would ask what the answer is for.** If it is for finding repeated structure in DNA, the biologists
> want *all* long palindromes above a threshold, not the single longest — **which is a different output and
> changes the loop, though not the approach.** If it is a puzzle, the longest is what is wanted. **That
> question costs ten seconds and can change the whole shape of the work.**"

---

## 9. Recall card

**`dp[i][j]` is true when `s[i] == s[j]` AND `dp[i+1][j-1]`** — the ends match and the inside is already a
palindrome. **The dependency is below-and-left, so the natural fill order reads cells that do not exist yet**
and silently misses every palindrome longer than 3. **Fill by increasing substring length** (or with `i`
decreasing). Handle length 2 separately, or guard with `j - i < 2`.

**Expand around centre is the answer to write:** same `O(n²)` time, **`O(1)` space, fewer lines.** The DP costs
`n²` memory and buys nothing — a million booleans against four integers at `n = 1,000`.

**There are `2n - 1` centres, not `n`** — `n` characters (odd palindromes) and `n - 1` gaps (even). **Checking
only characters reports `"abba"` as one letter, with no error.** The expansion overshoots by one, so return
`left + 1, right` — and a negative index slices from the end rather than raising.

**Counting is the same loop with `count += 1` inside the while** — each successful step outwards is one more
distinct palindromic substring.

**The table earns its place only for palindrome partitioning**, which needs constant-time "is `s[i..j]` a
palindrome?" `O(n²)` times — `O(n³)` with expansion.

**Substring ≠ subsequence:** `"bbbab"` gives 3 as a substring and 4 as a subsequence (`"bbbb"`), and the
subsequence version is **`LCS(s, reversed(s))`** — expansion does not apply, because a subsequence has no
contiguous centre. **Manacher's is `O(n)`** (reuse mirrored results inside the rightmost known palindrome) —
name it, don't write it; on real text expansion is already near-linear.
