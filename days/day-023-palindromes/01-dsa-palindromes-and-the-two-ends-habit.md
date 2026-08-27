---
day: 23
track: dsa
title: "Palindromes and the two-ends habit"
phase: "Strings"
status: written
---

# Day 023 · DSA — Palindromes and the two-ends habit

**After today you can:** You can check a palindrome with two pointers and handle the messy input rules.

**The interviewer asks it as:** *Is this string a palindrome, ignoring punctuation and case?*

---

## 1. What this is, and why they ask it

A **palindrome** is a sequence that reads the same forwards and backwards. `madam`. `racecar`.
`12321`.

Checking one introduces a habit you will use for the next fifty days: **put one index at each end and
walk them towards each other, comparing as you go.** Two indices, `O(n)` time, `O(1)` extra space, and
the loop stops when they meet. That is the two-pointer pattern, arriving four days before
[day 027](../day-027-two-pointers-idea/README.md) makes it official, and palindromes are the gentlest
possible introduction to it.

The reason interviewers keep asking it is not the algorithm — everyone gets the algorithm. It is the
**input rules**. The real question is almost always *"ignoring punctuation, spaces and case"*, and
that turns a five-line problem into a test of whether you handle messy input carefully: which
characters count, what happens when both ends land on characters that do not count, and what an empty
string returns. Candidates who reach straight for `s == s[::-1]` get a correct answer and miss the
point of the exercise, which is `O(1)` space.

It is LeetCode 125, 680 and 5, and it is one of the most common opening questions at every level.

---

## 2. The story

The level crossing near Nithya's school shuts for about twelve minutes at a time, and on a bad
evening her father catches it twice. They sit in the car with the engine off and the window down, and
they have a game they have played since she was seven.

They look at the number plate of whichever car is in front, and they see whether the numbers read the
same both ways.

The plate says TN 09 BX 4554. Her father does not read the whole thing out and then reverse it in his
head; he tried that once and gave up. What they do instead is that she takes the left end and he
takes the right end, and they work towards each other.

She starts at the far left. T. That is a letter, so it does not count — the game is only about the
numbers — and she moves along. N, also a letter, move along. Then a zero, and she stops there. He
starts at the far right. Four. That counts, and he stops there. Zero against four, no match, and the
game is over in about three seconds.

The next car is TN 37 AC 8228. She skips the letters and lands on the three; wait, no — she reads it
again properly. The numbers, in order, are 3, 7, 8, 2, 2, 8. She is on the 3 and he is on the last 8.
Three against eight. No.

Then a scooter goes past with 2002 on it and they both say it at the same time.

Two things about how they do it. Neither of them ever has to hold the whole plate in their head —
she only ever remembers where she is, and he only remembers where he is. And they stop the moment
their hands would cross. On 2002 she checks the first 2 against the last 2, then the 0 against the 0,
and at that point she has reached where he is, and there is nothing in the middle left to check. On a
plate with five numbers the middle one has nobody to be compared with, and they skip it, because a
thing is always the same as itself.

The gates go up. He starts the car.

---

## 3. The idea in plain English

Nithya at the left and her father at the right are **two indices**, usually called `left` and
`right`. Everything today is those two, and the rules for moving them.

### The core loop

```python
left, right = 0, len(s) - 1
while left < right:
    if s[left] != s[right]:
        return False
    left += 1
    right -= 1
return True
```

Start at the two ends. Compare. If they differ, it is not a palindrome and you are finished. If they
match, step both inwards. If you get all the way to the middle without a mismatch, it is a
palindrome.

**`while left < right`, not `<=`.** When `left == right` the two indices are on the same character,
and comparing a character with itself is always true — that is the middle number on a five-digit
plate, with nobody to be compared with. Using `<=` is not wrong, merely one wasted comparison, but
saying *why* `<` is enough shows you have thought about the odd-length case.

Notice what is **not** here: any copy of the string. `left` and `right` are two integers. That is the
`O(1)` space, and it is the entire reason this version is better than reversing.

### The reversing version, and when it is fine

```python
def is_palindrome(s: str) -> bool:
    return s == s[::-1]
```

One line, correct, and — from [day 019](../day-019-what-a-string-is/README.md) — `s[::-1]` builds a
whole new string, so it costs `O(n)` extra space. Write it, say that, and then offer the two-pointer
version. In real code with short strings the one-liner is what you would ship; in an interview asking
for `O(1)` space it is the thing being ruled out.

### The messy input rules, which are the actual question

The real problem says *"consider only alphanumeric characters and ignore case"*. Two rules, and each
needs handling.

**Which characters count.** `ch.isalnum()` is `True` for letters and digits and `False` for spaces,
commas, colons and everything else. That is Nithya skipping the letters on the plate — except in the
real problem letters *do* count and punctuation does not.

**Case.** `A` and `a` must match, so compare `s[left].lower()` against `s[right].lower()`.

There are two ways to apply them.

**Clean first, then check.** Simple and readable:

```python
cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
return cleaned == cleaned[::-1]
```

Two lines, obviously correct, and `O(n)` extra space for the cleaned copy.

**Skip as you go.** No copy at all, so `O(1)` space — and this is the version the question is asking
for:

```python
while left < right:
    while left < right and not s[left].isalnum():
        left += 1
    while left < right and not s[right].isalnum():
        right -= 1
    if s[left].lower() != s[right].lower():
        return False
    left += 1
    right -= 1
```

**The two inner loops are the whole difficulty**, and there are two things to get right about them.

They must be `while`, not `if`. A string can have several unwanted characters in a row —
`"a,,,  ;a"` — and one `if` skips only the first.

They must **also** test `left < right`. Without it, a string of nothing but punctuation runs `left`
straight past `right` and off the end of the string. That inner guard is the difference between
correct code and an `IndexError`, and §7 shows it.

### Why the pointers can never cross wrongly

At the point of comparison, one of two things is true: either `left < right` and both are on
characters that count, or `left == right`, in which case the loops stopped there and the comparison is
a character against itself, which passes harmlessly before the outer condition ends the loop. Either
way you never read outside the string. Being able to say that sentence is what separates code you
trust from code you hope about.

### The two shapes of palindrome, which matter later

```
   odd length, centre is one character        even length, centre is a gap
   r a c e c a r                              a b b a
         ^                                       ^
      one middle                              between two

   7 characters, 3 comparisons                4 characters, 2 comparisons
```

For the simple check this only decides whether the last comparison happens. For *finding* palindromes
— §5's longest-substring problem — it matters a great deal, because every centre has to be tried both
ways, and forgetting the even case is the standard bug.

---

## 4. The picture

`"racecar"`, with the two indices walking inwards:

```
  index   0    1    2    3    4    5    6
        +----+----+----+----+----+----+----+
        | r  | a  | c  | e  | c  | a  | r  |
        +----+----+----+----+----+----+----+
          ^                             ^
        left                          right      r == r, step both

               ^                   ^
             left                right          a == a, step both

                    ^         ^
                  left      right               c == c, step both

                         ^
                      left,right                left == right: STOP
                                                nothing left to compare
```

**What to notice:** three comparisons for seven characters, not seven. Each step settles two positions
at once, which is why the loop runs `n/2` times.

Now `"A man, a plan, a canal: Panama"`, where the skipping happens:

```
  A   m a n ,   a   p l a n ,   a   c a n a l :   P a n a m a
  ^                                                          ^
 left                                                      right     A vs a -> match

      ^                                                 ^
    left                                              right          m vs m -> match

        ^ skip the comma and space                ^ skip the colon and space
        |                                         |
        +-- inner while advances left             +-- inner while retreats right
```

**What to notice:** the outer loop compares; the two inner loops do nothing but move past characters
that do not count. Keeping those three loops separate in your head is the trick to writing this
correctly under pressure.

The two centre shapes, for finding palindromes rather than checking one:

```
   expand from a single character        expand from between two
        b a b a d                             c b b d
          ^                                     ^ ^
        i, i                                  i, i+1
      "aba" grows outward                   "bb" grows outward

   every position gives TWO centres to try, so 2n - 1 centres in total
```

**What to notice:** `2n - 1` centres, not `n`. A string of length 5 has 5 single-character centres and
4 gaps between characters. Missing the gaps means never finding an even-length palindrome, and
`"cbbd"` is the four-character input that exposes it.

---

## 5. The code, built step by step

### The simplest correct thing

```python
def is_palindrome_slice(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```

Filter, lower-case, join — the pattern from [day 020](../day-020-building-strings/README.md) — then
compare against the reverse. Write this first in an interview. It is correct, it takes fifteen
seconds, and it gives you something to improve.

Its cost: `O(n)` time and `O(n)` extra space, because `cleaned` and `cleaned[::-1]` are two new
strings.

### The two-pointer skeleton

```python
left, right = 0, len(s) - 1
while left < right:
    if s[left] != s[right]:
        return False
    left += 1
    right -= 1
return True
```

Correct when every character counts. `left < right` because the middle character of an odd-length
string needs no comparison.

### Adding the skip loops

```python
while left < right and not s[left].isalnum():
    left += 1
while left < right and not s[right].isalnum():
    right -= 1
```

These go **inside** the outer loop, before the comparison. `while` and not `if`, because runs of
punctuation exist. And `left < right` inside each condition, because a string with no alphanumeric
characters at all would otherwise walk off the end.

### The comparison, case-folded

```python
if s[left].lower() != s[right].lower():
    return False
```

`.lower()` on a single character is cheap. Some solutions upper-case instead; either is fine as long
as you do the same to both sides.

### Putting it together

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

Eleven lines, `O(n)` time, `O(1)` extra space, and it handles `""`, `" "`, `".,"` and `"0P"`
correctly. Test all four.

That last one is worth pausing on. `"0P"` is **not** a palindrome — `0` and `P` are both alphanumeric
and they differ. A solution that uses `isalpha()` instead of `isalnum()` skips the `0` and wrongly
returns `True`. It is the standard trap input for this problem.

### Allowing one deletion

LeetCode 680: *"can it become a palindrome by deleting at most one character?"* Walk inwards as
usual, and at the first mismatch there are exactly two possibilities — delete the left character, or
delete the right one:

```python
def valid_palindrome(s: str) -> bool:
    def is_pal(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True
```

**Why only two possibilities?** Because everything outside `left` and `right` has already matched
pairwise, so the deletion has to happen at one of those two positions — deleting anywhere else leaves
the mismatch untouched. That argument is the whole answer, and it is what turns an apparently
exponential problem into two linear checks.

The cost stays `O(n)`: the main loop is at most `n/2` steps, and the branch happens **at most once**,
after which each helper call is another `n/2` at worst.

### Finding the longest palindromic substring

LeetCode 5. The idea: every palindrome has a centre, so try every centre and grow outwards while the
characters match.

```python
def expand(s: str, left: int, right: int) -> tuple[int, int]:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1          # step back to the last matching pair
```

The `left + 1, right - 1` at the end is the off-by-one people get wrong. The loop exits **after**
stepping one too far — either off the end of the string or onto a mismatch — so the answer is one
step back on each side.

```python
for i in range(len(s)):
    a, b = expand(s, i, i)          # odd-length centre
    ...
    a, b = expand(s, i, i + 1)      # even-length centre
```

Both centres for every position, which is the `2n - 1` from §4.

### The complete solutions

```python
def is_palindrome_slice(s: str) -> bool:
    """LeetCode 125, the readable version. O(n) time, O(n) space."""
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def is_palindrome(s: str) -> bool:
    """LeetCode 125 in O(1) space. Two indices walking inwards, skipping what does not count."""
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():    # while, not if
            left += 1
        while left < right and not s[right].isalnum():   # and guard left < right
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def valid_palindrome(s: str) -> bool:
    """LeetCode 680. Palindrome after deleting at most one character."""
    def is_pal(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # everything outside left/right already matched, so the deletion
            # must be at one of these two positions
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True


def longest_palindrome(s: str) -> str:
    """LeetCode 5. Expand around every centre. O(n^2) time, O(1) space."""
    if not s:
        return ""

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1       # the loop overshot by one on each side

    start, end = 0, 0
    for i in range(len(s)):
        a, b = expand(i, i)              # odd-length palindrome centred on i
        if b - a > end - start:
            start, end = a, b
        a, b = expand(i, i + 1)          # even-length palindrome centred between i and i+1
        if b - a > end - start:
            start, end = a, b
    return s[start:end + 1]


if __name__ == "__main__":
    cases = ["A man, a plan, a canal: Panama", "race a car", "", " ", ".,", "0P",
             "aba", "abba", "ab", "a"]
    print([is_palindrome_slice(c) for c in cases])
    # [True, False, True, True, True, False, True, True, False, True]
    print([is_palindrome(c) for c in cases])
    # identical

    print([valid_palindrome(x) for x in ("aba", "abca", "abc", "", "a", "deeee")])
    # [True, True, False, True, True, True]

    print([longest_palindrome(x) for x in ("babad", "cbbd", "a", "", "ac", "forgeeksskeegfor")])
    # ['bab', 'bb', 'a', '', 'a', 'geeksskeeg']
```

---

## 6. What it costs

### `is_palindrome`, the two-pointer version

**Time.** Each turn of the outer loop moves `left` forward at least one and `right` back at least
one. The inner skip loops also only ever move them in those directions. So across the whole run,
`left` moves at most `n` positions in total and `right` moves at most `n`, and they stop when they
meet — **every character is looked at at most once by each index**. That is **O(n) time**, not
`O(n²)`, even though there are loops inside a loop.

That last sentence is worth practising, because nested `while` loops make people say `O(n²)`
reflexively. The right argument is not "there are two loops" but "count how far the indices travel in
total".

**Space.** Two integers. **O(1) extra space** — and this is the whole reason the two-pointer version
exists.

### `is_palindrome_slice`

**Time.** One pass to filter and lower-case, one to join, one to reverse, one to compare: `4n` steps,
so **O(n)** — the same class.

**Space.** `cleaned` is up to `n` characters, and `cleaned[::-1]` is another `n`. **O(n) extra
space**, which at a hundred megabytes of input is two hundred megabytes of copies for a question that
needs two integers.

### `valid_palindrome`

The main loop is at most `n/2` turns. The branch fires **at most once**, and each helper call is at
most another `n/2` turns. Worst case `n/2 + n/2 + n/2`, so **O(n) time** and **O(1) space**.

Compare with the naive answer — try deleting each of the `n` characters and check each result, which
is `n` deletions × `O(n)` check = **O(n²)**, plus `O(n)` space per deleted copy. The insight that only
two positions can possibly matter is what removes a whole factor of `n`.

### `longest_palindrome`

`2n - 1` centres. Each `expand` runs until it fails, which is at most `n/2` steps. So
`(2n - 1) × n/2`, which is about `n²`: **O(n²) time**, **O(1) space**.

At `n = 1,000` that is around a million operations — instant. At `n = 100,000` it is ten billion,
which is not. If an interviewer pushes past `O(n²)` there is Manacher's algorithm at `O(n)`; it is
genuinely tricky and almost never expected. **The right move is to name it, say it is `O(n)`, and say
you would look it up rather than derive it under time pressure.** That is a better answer than a
half-remembered attempt.

### The number to have ready

> Two pointers: `O(n)` time and `O(1)` space, and the nested skip loops do not make it quadratic
> because each index only ever travels forward. Reversing is the same `O(n)` time but `O(n)` space.
> Longest-palindromic-substring by expanding around `2n - 1` centres is `O(n²)`.

---

## 7. The traps

### The real error: forgetting `left < right` in the skip loops

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while not s[left].isalnum():        # no left < right guard
            left += 1
        while not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome(".,"))
```

```
Traceback (most recent call last):
  File "t.py", line 12, in <module>
    print(is_palindrome(".,"))
          ~~~~~~~~~~~~~^^^^^^
  File "t.py", line 5, in is_palindrome
    while not s[left].isalnum():
              ~^^^^^^
IndexError: string index out of range
```

`".,"` has no alphanumeric characters, so the first inner loop walks `left` past `right`, past the
end of the string, and off into nothing. **Every skip loop needs the bound test in its own
condition.** Test with `".,"`, `" "` and `"!!!"` — those three inputs find this bug and almost
nothing else does.

### The near-miss: `isalpha` instead of `isalnum`

```python
cleaned = "".join(ch.lower() for ch in s if ch.isalpha())
print(cleaned == cleaned[::-1])     # on "0P"
```

```
True
```

Wrong. `"0P"` is not a palindrome — the digit and the letter are both alphanumeric and they differ.
`isalpha()` drops the `0`, leaving `"p"`, which reads the same both ways. This is the standard trap
input on LeetCode 125 and it exists precisely to catch this. Read the problem statement: it says
**alphanumeric**.

### The near-miss: `if` instead of `while` when skipping

```python
if not s[left].isalnum():
    left += 1
```

One skip per turn. On `"a,,,  ,a"` the left index steps past one comma, then compares a comma against
an `a`, and returns `False` for a string that is a palindrome under the rules. Runs of unwanted
characters are normal in real text, so this fails on almost any realistic sentence.

### The near-miss: expanding without stepping back

```python
def expand(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left, right               # forgot the +1 / -1
```

The loop exits **after** the step that failed, so `left` and `right` are each one position too far
out. The returned substring is two characters too long and includes the mismatching pair — or
`s[left:right+1]` raises, or silently produces nonsense from a negative index. Return
`left + 1, right - 1`.

### The near-miss: only trying odd centres

```python
for i in range(len(s)):
    a, b = expand(i, i)          # and nothing else
```

Every palindrome found will have odd length. On `"cbbd"` the answer is `"bb"` and this returns `"c"`.
`"abba"`, `"cbbd"` and `"aa"` are the inputs that expose it — all of them even-length, all of them
easy to leave out of your own test list because the first example you were given was `"babad"`.

### The near-miss: greedily choosing which character to delete

```python
if s[left] != s[right]:
    if s[left + 1] == s[right]:
        left += 1                # assume deleting the left one is right
    else:
        right -= 1
    ...
```

This decides on one character of look-ahead and can be wrong. On `"eeccccbebaeeabebccceees"` a greedy
choice at the first mismatch commits to a branch that fails later while the other branch would have
succeeded. **You must actually try both**, which is what `is_pal(left+1, right) or is_pal(left,
right-1)` does — and because the branch fires at most once, trying both is still `O(n)`.

---

## 8. In the interview

### How it gets asked

- *"Is this string a palindrome, ignoring punctuation and case?"* — LeetCode 125. The last five words
  are the question.
- *"Do it without using extra space."* — the follow-up that rules out `s[::-1]` and asks for two
  pointers.
- *"Can it be a palindrome if you delete at most one character?"* — LeetCode 680, and the interesting
  one, because the two-branch insight is a real idea.
- *"Find the longest palindromic substring."* — LeetCode 5, expanding around centres.
- *"Is this number a palindrome, without converting it to a string?"* — the arithmetic variant, using
  `% 10` and `// 10`.

### What to say out loud, in the first ninety seconds

1. **Pin the rules.** *"Which characters count — letters and digits only, or everything? Is it
   case-insensitive? And what should an empty string return?"* All three change the code, and the
   empty case is usually `True`.
2. **Give the simple version and its cost.** *"The simplest correct answer is to strip out the
   non-alphanumeric characters, lower-case them, and compare against the reverse. O(n) time, but O(n)
   space because reversing builds a new string."*
3. **Offer the better one, unprompted.** *"I can do it in O(1) space with two indices walking inwards
   from each end."*
4. **Describe the three loops before writing them.** *"The outer loop compares and steps both inwards.
   Inside it, two small loops move each index past characters that don't count."*
5. **Name the two details that break it.** *"Those inner loops have to be `while`, not `if`, because
   punctuation comes in runs. And each one has to test `left < right` in its own condition, or a
   string of pure punctuation walks straight off the end."*
6. **Say why `<` and not `<=`.** *"The outer loop stops when they meet, because on an odd-length
   string the middle character has nothing to be compared with."*
7. **Give the cost with the argument.** *"O(n) time — the nested loops don't make it quadratic,
   because each index only ever moves in one direction, so between them they travel at most n
   positions. O(1) space, just two integers."*
8. **Name your test cases.** *"I'd test the empty string, a single space, a string of only
   punctuation, and `0P` — that last one catches using isalpha instead of isalnum."*

### The follow-ups

**"Can you do it without extra space?"**
That is the two-pointer version, and it is the reason the pattern is worth learning. One index at each
end, walking inwards, comparing as they go, with small inner loops skipping characters that do not
count. Two integers of state regardless of input size. The reversing version is the same `O(n)` time
but allocates two full copies of the string, which for a very large input is the difference between
constant memory and doubling your footprint. The one thing to be careful about is that the inner skip
loops must repeat their own bound check, because a string containing no alphanumeric characters at all
would otherwise run an index off the end — `".,"` is the input that proves it.

**"Now allow one deletion."**
Walk inwards as before. At the first mismatch, the character causing it must be either the one on the
left or the one on the right — everything outside those two positions has already matched pairwise, so
deleting anywhere else leaves the mismatch exactly where it was. So I check whether the remainder is a
palindrome with the left character skipped, or with the right one skipped, and return true if either
holds. That branch fires at most once, so the whole thing is still `O(n)` time and `O(1)` space. The
version to avoid is deciding greedily which one to delete based on one character of look-ahead — that
is wrong on inputs where the losing branch survives longer than the winning one, and you have to
actually try both.

**"Find the longest palindromic substring."**
Every palindrome has a centre, so I try every centre and expand outwards while the characters match,
keeping the longest. The detail that matters is that there are `2n - 1` centres, not `n`: each
character is a centre for odd-length palindromes, and each gap between two characters is a centre for
even-length ones. Missing the even centres means never finding `"bb"` in `"cbbd"`. That gives `O(n²)`
time and `O(1)` space, which is what is normally expected. Dynamic programming gives the same `O(n²)`
time but `O(n²)` space, so it is strictly worse here. There is an `O(n)` algorithm — Manacher's — and
I would name it and say I would look it up rather than reconstruct it under time pressure, because
getting it subtly wrong is worse than not offering it.

**"Is this integer a palindrome, without converting it to a string?"**
Negative numbers are never palindromes, because of the minus sign, and any number ending in zero is
not unless it is zero itself. Otherwise I reverse half the number arithmetically: repeatedly take the
last digit with `% 10`, build it onto a reversed value with `reversed = reversed * 10 + digit`, and
drop it from the original with `// 10`, stopping when the original is no longer greater than the
reversed half. For an odd number of digits the middle digit ends up alone in the reversed half, so I
compare `original == reversed` or `original == reversed // 10`. Reversing only half avoids overflow in
languages with fixed-width integers, which is the actual reason the problem is posed that way — Python
has arbitrary precision so it would not matter here, and saying that shows you know why the constraint
exists.

### A model answer

> "First, the rules, because they are most of this problem. Which characters count — is it letters and
> digits only, and does case matter? And what should the empty string return?
>
> ...Alphanumeric only, case-insensitive, empty is true. Good.
>
> The simplest correct answer is to filter out everything non-alphanumeric, lower-case it, and compare
> the result against its reverse. That is two lines and O(n) time — but O(n) extra space, because
> reversing a string in Python builds a whole new one.
>
> I can do it in constant space with two indices. One starts at the left end, one at the right, and
> they walk towards each other comparing as they go.
>
> ```python
> def is_palindrome(s: str) -> bool:
>     left, right = 0, len(s) - 1
>     while left < right:
>         while left < right and not s[left].isalnum():
>             left += 1
>         while left < right and not s[right].isalnum():
>             right -= 1
>         if s[left].lower() != s[right].lower():
>             return False
>         left += 1
>         right -= 1
>     return True
> ```
>
> Three things I want to call out.
>
> The inner loops have to be `while` and not `if`, because unwanted characters come in runs — in
> `'a,,, ,a'` a single `if` only skips one comma and then compares a comma against a letter.
>
> Each inner loop repeats the `left < right` test in its own condition. Without that, a string like
> `'.,'` with no alphanumeric characters at all runs the left index straight past the right one and
> off the end of the string, and you get an IndexError. That is the one input that finds this bug.
>
> And the outer loop is `left < right`, not `<=`, because on an odd-length string the middle character
> has nothing to compare against — comparing it with itself is always true.
>
> On cost: O(n) time. It is worth being explicit that the nested loops don't make it quadratic — each
> index only ever moves in one direction, so between them they travel at most n positions in total.
> And O(1) extra space, which is the whole point of doing it this way.
>
> For tests I'd use the empty string, a single space, a string of pure punctuation, and `'0P'`. That
> last one is the interesting one: it is not a palindrome, and a solution using `isalpha` instead of
> `isalnum` drops the zero and wrongly says it is."

---

## 9. Recall card

- **Two indices from the ends, walking inwards.** `while left < right` — the middle character needs no
  comparison.
- **`O(n)` time, `O(1)` space.** The nested skip loops stay linear because each index only ever moves
  one way.
- **Skip loops must be `while`, not `if`, and must repeat `left < right`** — or `".,"` runs off the
  end.
- **`isalnum`, not `isalpha`.** `"0P"` is the input that catches it.
- **Finding palindromes: `2n - 1` centres**, odd and even. Expanding overshoots, so return
  `left + 1, right - 1`.
