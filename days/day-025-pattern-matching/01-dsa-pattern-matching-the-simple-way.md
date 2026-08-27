---
day: 25
track: dsa
title: "Pattern matching, the simple way"
phase: "Strings"
status: written
---

# Day 025 · DSA — Pattern matching, the simple way

**After today you can:** You can write naive substring search and state its cost honestly.

**The interviewer asks it as:** *Implement strStr: find the first occurrence of a needle in a haystack.*

---

## 1. What this is, and why they ask it

Given a long string — the **haystack** — and a short one — the **needle** — find the position where the
needle first appears, or report that it does not. `strStr("sadbutsad", "sad")` is `0`.
`strStr("leetcode", "leeto")` is `-1`.

The straightforward answer is: try every starting position, and at each one compare the needle
against the haystack character by character until it either runs out or fails. Two loops, about ten
lines, and it is called **naive** or **brute-force** substring search.

The interesting part is the cost, and it is genuinely subtle. The worst case is `O(n × m)` — you can
build an input where nearly every starting position matches almost the whole needle before failing.
The *typical* case on real text is close to `O(n)`, because ordinary English mismatches on the first
or second character almost every time. Both statements are true, and being able to say both, with the
input that produces each, is exactly what the question is testing. §6 has the measurements: 43
comparisons on English text, 10,901 on an adversarial one of the same size.

Interviewers ask it because it is a five-minute problem with a real conversation attached. Anyone can
write the loops. The follow-up — *"can you do better than O(n·m)?"* — separates candidates who know
that KMP, Rabin-Karp and Boyer-Moore exist, and what each buys, from those who do not. You are not
expected to implement KMP under time pressure. You are expected to name it and say what it does.

---

## 2. The story

The curtains in Ayesha's front room have been up since before her daughter was born, and last month
the one on the left tore right down the seam where the sun has been hitting it for years. The rest of
the cloth is fine. She wants one more panel of the same print, and the shop she bought it from has
closed.

So she cuts a piece about the size of her hand from the torn end and takes it to the big cloth
market, and this is where it becomes a proper job of work.

The shop she ends up in has rolls standing on end all along one wall, and the man unrolls one across
the counter — twenty feet of printed cotton, small cream flowers on a dark ground, close enough that
she cannot tell from across the room.

The way he checks is the only way there is. He lays her piece down at the very start of the roll,
lines up the top corner, and looks along it. Flower matches flower. Second one matches. Third one is
slightly the wrong shape, and that is that — no match here.

He does not throw the whole roll out. He slides her piece along by one repeat and starts again from
the top corner of her piece. First flower, second flower, third, fourth, and then the little gap
between the rows is wrong. Slide along again, start from the top of her piece again.

The frustrating rolls are the ones that are nearly right. There is one with a print so close to hers
that he gets seven or eight flowers in every time before something is off, and checking that roll
takes him ten minutes on its own. The obviously wrong ones take two seconds each, because the very
first flower is a different colour and he is done.

On the fourth roll it goes all the way. Every flower, every gap, right to the end of her little
piece, and he says that is it and cuts her three metres.

She asks how he knew where to start each time. He says you always start at the top of the piece
again. You cannot carry over what matched before, because you have moved.

---

## 3. The idea in plain English

The roll of cloth is the haystack. Ayesha's hand-sized piece is the needle. The shopkeeper sliding
along one repeat at a time and starting from the top of her piece each time is the naive algorithm,
exactly.

### The algorithm

```python
for start in range(n - m + 1):        # every position the needle could begin at
    k = 0
    while k < m and haystack[start + k] == needle[k]:
        k += 1
    if k == m:                        # the inner loop ran out of needle: full match
        return start
return -1
```

Two loops. The outer one picks a starting position. The inner one compares the needle against the
haystack from that position, stopping at the first mismatch or at the end of the needle. If it
stopped because it reached the end of the needle — `k == m` — every character matched, so this is the
answer.

### The two details that are easy to get wrong

**`range(n - m + 1)`, not `range(n)`.** A needle of length `m` cannot start later than position
`n - m`, because there would not be enough haystack left. `range` excludes its upper bound, so the
`+ 1` is what lets the last valid position be tried. On `haystack = "hello"` (5) and `needle = "lo"`
(2), the valid starts are 0, 1, 2, 3 — that is `range(5 - 2 + 1) = range(4)`. Off by one here and you
either miss a match at the end or read off the string.

**`k` resets to 0 at every start.** That is the shopkeeper's own answer: *you always start at the top
of the piece again.* Whatever matched at the previous starting position tells you nothing about this
one, because the alignment moved. That resetting is precisely the wasted work KMP removes.

### The empty-needle convention

`strStr(anything, "")` returns **0**, by convention — an empty needle is found immediately, at the
start. It matches `"abc".find("")`, which is `0`, and it also falls out of the code for free: with
`m = 0` the inner loop runs zero times, `k == m` is `0 == 0`, and it returns the first `start`.
Ask about it anyway; some versions of the problem want `-1`.

### The cost, honestly

**Worst case.** The outer loop runs about `n` times, and the inner loop can run up to `m` times each,
so `O(n × m)`. To make that actually happen you need a needle that almost matches everywhere:

```
haystack = "aaaaaaaaaa...aaab"      (1,000 a's then a b)
needle   = "aaaaaaaaaab"            (10 a's then a b)
```

At every starting position the inner loop matches all ten `a`s and then fails on the `b`. §6 measures
it: **10,901 comparisons** for a haystack of 1,001 characters.

**Typical case.** On ordinary text, the inner loop almost always fails on the very first character,
because most letters are not the one you are looking for. Measured on English prose, finding an
eight-character needle took **43 comparisons** — barely more than the 35 positions it had to walk
past. In practice the naive algorithm behaves like `O(n)` on natural language.

**Both are true.** The honest sentence is: *"It is `O(n·m)` in the worst case and close to `O(n)` on
real text, and the worst case needs a highly repetitive haystack and needle to trigger."*

### What Python actually does

```python
haystack.find(needle)     # position, or -1
haystack.index(needle)    # position, or raises ValueError
needle in haystack        # True or False
```

All three use the same underlying search, which is a hybrid of Boyer-Moore and Horspool with a
worst-case fallback — far faster than the naive loop and written in C. §6 measures it at about
**23,000 times faster** on the adversarial input. In real code, use `find`. In an interview, write the
loop and then say `find` exists.

### The better algorithms, by name

You will be asked *"can you do better?"*. Have one sentence each ready. Do **not** attempt to
implement KMP from memory unless you have practised it.

| Algorithm | Idea | Time |
|---|---|---|
| **KMP** (Knuth-Morris-Pratt) | Precompute, for each prefix of the needle, the longest prefix that is also a suffix. On a mismatch, jump the needle forward by that much instead of restarting — so the haystack index never moves backwards. | `O(n + m)` |
| **Rabin-Karp** | Compare a rolling hash of each window instead of the characters, and only compare characters when the hashes agree. | `O(n + m)` average, `O(n·m)` worst |
| **Boyer-Moore** | Compare from the **right** end of the needle, and on a mismatch skip ahead by however far that character is from the needle's end. Often skips most of the haystack. | `O(n/m)` best, sublinear in practice |

**KMP is the expected answer**, because it is the one with a guaranteed linear bound. The sentence to
say: *"KMP precomputes a table of how far the needle can safely jump on a mismatch, so the haystack
index never goes backwards — that makes it `O(n + m)`."* Rabin-Karp is the right answer when you want
to search for **many** needles at once, because one pass of hashing serves them all.

---

## 4. The picture

Searching for `"sad"` in `"sadbutsad"`:

```
  start = 0
    s a d b u t s a d
    | | |
    s a d                -> all three match, k reaches 3 == m, return 0
```

Now `"issip"` in `"mississippi"`, where the sliding is visible:

```
  start = 0     m i s s i s s i p p i
                x                        'm' vs 'i' -> fail after 1 comparison
                i

  start = 1     m i s s i s s i p p i
                  | | x                  'i','s' match, 's' vs 's'... 's' vs 'i' fails at k=2
                  i s s i p

  start = 4     m i s s i s s i p p i
                        | | | | |        all five match -> return 4
                        i s s i p
```

**What to notice:** at `start = 1` the comparison got two characters in before failing, and every one
of those comparisons is thrown away — the next attempt begins again at `k = 0`. That discarded work is
what KMP recovers.

The worst case, drawn:

```
  haystack:  a a a a a a a a a a a a ... a a a b
  needle:    a a a a a a a a a a b

  start = 0   a a a a a a a a a a b        10 matches, then 'a' vs 'b' fails   -> 11 comparisons
  start = 1     a a a a a a a a a a b      10 matches, then fails              -> 11 comparisons
  start = 2       a a a a a a a a a a b    10 matches, then fails              -> 11 comparisons
              ...
              ~n starting positions, ~m comparisons each  ->  n x m
```

**What to notice:** the needle nearly matches everywhere and only fails at the last character. That is
the shopkeeper's roll of nearly-identical cloth, and it is the only shape of input that makes the
naive algorithm slow.

---

## 5. The code, built step by step

### The bound on the outer loop

```python
n, m = len(haystack), len(needle)
for start in range(n - m + 1):
    ...
```

Work it out on a small case rather than remembering it: haystack length 5, needle length 2, so the
needle can start at 0, 1, 2 or 3 — four positions, which is `5 - 2 + 1`.

If `m > n` then `n - m + 1` is zero or negative, `range` produces nothing, and the function correctly
falls through to `return -1`. No special case needed, which is worth noticing out loud.

### The inner comparison

```python
k = 0
while k < m and haystack[start + k] == needle[k]:
    k += 1
```

Walk forward while the characters agree. **`k < m` comes first**, and it must, because Python's `and`
short-circuits — without that ordering, `needle[k]` would read off the end of the needle the moment
everything matched.

After this loop there are exactly two possibilities: `k == m`, meaning the needle ran out and every
character matched, or `k < m`, meaning a character differed.

### The test

```python
if k == m:
    return start
```

**`k == m`, not `k == m - 1`.** The loop increments `k` after each successful comparison, so a full
match leaves `k` one past the last character. This is the same off-by-one as the `range` bound, in a
different costume.

### The guard, and the whole thing

```python
def str_str(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    for start in range(n - m + 1):
        k = 0
        while k < m and haystack[start + k] == needle[k]:
            k += 1
        if k == m:
            return start
    return -1
```

The explicit empty guard is not strictly needed — the loop handles it — but it states the contract
plainly, and stating the contract is worth more than saving a line.

### Counting the comparisons, to make the cost real

```python
def count_comparisons(haystack: str, needle: str) -> tuple[int, int]:
    """Returns (position, number of character comparisons made)."""
    comparisons = 0
    n, m = len(haystack), len(needle)
    for start in range(n - m + 1):
        k = 0
        while k < m and haystack[start + k] == needle[k]:
            k += 1
            comparisons += 1
        if k < m:
            comparisons += 1          # the one that failed
        if k == m:
            return start, comparisons
    return -1, comparisons
```

Run this on two inputs of similar size and the difference between the worst case and the typical case
stops being an abstraction. §6 has the numbers.

### The complete solutions

```python
import time


def str_str(haystack: str, needle: str) -> int:
    """LeetCode 28. First index of needle in haystack, or -1.

    Naive: try every start, compare forward from k = 0 each time.
    O(n*m) worst case, close to O(n) on ordinary text.
    """
    if not needle:
        return 0                                  # convention: empty needle is found at 0
    n, m = len(haystack), len(needle)
    for start in range(n - m + 1):                # last valid start is n - m
        k = 0
        while k < m and haystack[start + k] == needle[k]:   # k < m FIRST: short-circuits
            k += 1
        if k == m:                                # ran out of needle, so all matched
            return start
    return -1


def count_comparisons(haystack: str, needle: str) -> tuple[int, int]:
    """Same search, but reports how many character comparisons it took."""
    comparisons = 0
    n, m = len(haystack), len(needle)
    for start in range(n - m + 1):
        k = 0
        while k < m and haystack[start + k] == needle[k]:
            k += 1
            comparisons += 1
        if k < m:
            comparisons += 1
        if k == m:
            return start, comparisons
    return -1, comparisons


def find_all(haystack: str, needle: str) -> list[int]:
    """Every occurrence, including overlapping ones. 'aaa' in 'aaaa' -> [0, 1]."""
    if not needle:
        return []
    out: list[int] = []
    n, m = len(haystack), len(needle)
    for start in range(n - m + 1):
        if haystack[start:start + m] == needle:   # slice-compare: clear, and O(m)
            out.append(start)
    return out


if __name__ == "__main__":
    tests = [("sadbutsad", "sad"), ("leetcode", "leeto"), ("hello", "ll"),
             ("", ""), ("", "a"), ("a", ""), ("aaaaa", "bba"), ("mississippi", "issip")]
    print([str_str(h, n) for h, n in tests])
    # [0, -1, 2, 0, -1, 0, -1, 4]
    print([h.find(n) for h, n in tests])
    # identical — the naive version agrees with the library on all of them

    print(count_comparisons("a" * 1000 + "b", "a" * 10 + "b"))
    # (990, 10901)   <- the adversarial case: ~n*m
    print(count_comparisons("the quick brown fox jumps over the lazy dog" * 10, "lazy dog"))
    # (35, 43)       <- ordinary English: barely more than n

    print(find_all("aaaa", "aa"))            # [0, 1, 2]  overlapping

    haystack = "a" * 200_000 + "b"
    needle = "a" * 1_000 + "b"
    start = time.perf_counter()
    str_str(haystack, needle)
    naive = time.perf_counter() - start
    start = time.perf_counter()
    haystack.find(needle)
    builtin = time.perf_counter() - start
    print(f"naive {naive:.4f}s   builtin {builtin:.6f}s   ratio {naive / builtin:.0f}x")
    # naive 13.9039s   builtin 0.000594s   ratio 23403x
```

---

## 6. What it costs

### Counted from the loops

The outer loop runs `n - m + 1` times, which is about `n` when the needle is short. For each of those,
the inner loop runs at most `m` times. So the body executes at most `(n - m + 1) × m` times, and each
execution is one character comparison — constant work.

**O(n × m) time.** Space is `k`, `start`, `n` and `m`: four integers, so **O(1) extra space**.

### The worst case, measured

```
haystack = 1,000 'a's followed by 'b'   (length 1,001)
needle   = 10 'a's followed by 'b'      (length 11)

comparisons made: 10,901
n x m            = 1,001 x 11 = 11,011
```

10,901 against a theoretical ceiling of 11,011 — so this input drives the algorithm to about 99% of
its worst case. Every start matches ten characters and fails on the eleventh.

### The typical case, measured

```
haystack = 430 characters of ordinary English
needle   = "lazy dog"  (8 characters)
found at position 35

comparisons made: 43
```

Forty-three comparisons to walk past 35 positions. The inner loop essentially never ran more than
once, because in English the chance that a random position starts with `l` is small, and if it does
not, the attempt costs one comparison. **On natural language the naive algorithm is effectively
linear**, and that is why it survives in real code far more often than its worst case suggests.

### Against the library

```
haystack = 200,000 'a's + 'b'
needle   = 1,000 'a's + 'b'

naive loop : 13.9039 s
str.find   :  0.000594 s
ratio      : about 23,000x
```

Two things are happening. The library uses a better algorithm — a Boyer-Moore-Horspool hybrid that
skips ahead rather than sliding by one — and it runs as compiled C rather than interpreted Python.
Neither alone explains 23,000×; together they do.

**Say this in an interview**: *"In production I would call `find`, which is a smarter algorithm in C.
I am writing the loop because you asked me to implement it."*

### The better algorithms

| | Time | Extra space | When it wins |
|---|---|---|---|
| Naive | `O(n·m)` worst, ~`O(n)` typical | `O(1)` | short needles, ordinary text |
| KMP | `O(n + m)` guaranteed | `O(m)` for the table | repetitive input, worst-case guarantees |
| Rabin-Karp | `O(n + m)` average | `O(1)` | searching many needles at once |
| Boyer-Moore | sublinear in practice, `O(n/m)` best | `O(alphabet)` | long needles, large alphabets |

For `n = 200,000` and `m = 1,000`: naive is up to 200 million comparisons, KMP is at most 201,000.
That is the thousand-fold difference the table is describing, and it is the number to quote.

---

## 7. The traps

### The near-miss: the outer loop bound

```python
for start in range(n):                  # should be n - m + 1
    k = 0
    while k < m and haystack[start + k] == needle[k]:
        k += 1
    if k == m:
        return start
```

```python
print(str_str("hello", "lo"))
```

This one happens to work, because the inner loop's `k < m` test stops it before it reads too far —
`haystack[start + k]` with `start = 4` and `k = 0` is `'o'`, which mismatches `'l'`, so nothing runs
off the end. But it does `m` extra useless iterations of the outer loop, and if you write the inner
comparison as a slice instead — `haystack[start:start+m] == needle` — the slice silently comes back
short and can never match, so a needle at the very end is missed. **Compute `n - m + 1` and mean it.**

### The near-miss: not resetting `k`

```python
k = 0
for start in range(n - m + 1):          # k declared outside the loop
    while k < m and haystack[start + k] == needle[k]:
        k += 1
    if k == m:
        return start
```

After the first failed attempt, `k` keeps whatever value it reached, so the next attempt starts
comparing from the middle of the needle against the wrong part of the haystack. It produces confident
wrong answers. This is the shopkeeper's rule violated: **you always start at the top of the piece
again.**

### The real error: comparing before checking the bound

```python
while haystack[start + k] == needle[k] and k < m:      # order swapped
    k += 1
```

```
Traceback (most recent call last):
  ...
    while haystack[start + k] == needle[k] and k < m:
                                ~~~~~~^^^
IndexError: string index out of range
```

The moment every character matches, `k` reaches `m` and `needle[k]` reads off the end. Python's `and`
evaluates left to right and stops as soon as the answer is known, so **`k < m` must come first**. This
ordering is not stylistic; it is the guard.

### The contract corner: the empty needle

```python
str_str("abc", "")     # 0, by convention
"abc".find("")         # 0
```

Every string contains the empty string at position 0. It falls out of the loop naturally, so the
explicit guard is documentation rather than logic — but **ask**, because some problem statements
specify `-1` and you would be marked wrong for the convention.

### The near-miss: `find` versus `index`

```python
"abc".find("z")      # -1
"abc".index("z")     # ValueError: substring not found
```

`find` reports failure with a sentinel; `index` raises. Choose deliberately — `find` when absence is
normal, `index` when absence is a bug you want to hear about. Writing `if s.index(x):` is a bug twice
over: it raises when absent, and it is falsy when the answer is 0.

### The trap in the follow-up: attempting KMP from memory

The failure-function construction in KMP is short and extremely easy to get subtly wrong, and a
half-correct KMP is worse than a correct naive solution plus an accurate description. **The right move
is: write the naive version, state both costs, name KMP with one sentence about what it does, and
offer to work through the table if they want to spend the time on it.** That reads as judgement.
Fumbling a half-remembered table for ten minutes does not.

---

## 8. In the interview

### How it gets asked

- *"Implement strStr / indexOf."* — LeetCode 28. Ten minutes, and the follow-up is the real question.
- *"What's the time complexity?"* — where the good answer has two parts and an example input for each.
- *"Can you do better than O(n·m)?"* — name KMP, say what it does, say why it is linear.
- *"Find all occurrences, including overlapping ones."* — the small variant that catches people who
  jump `start` by `m` instead of by 1.
- *"How would you search for a thousand different needles in the same text?"* — where Rabin-Karp or
  Aho-Corasick is the right name to produce.

### What to say out loud, in the first ninety seconds

1. **Ask the contract questions.** *"What should I return for an empty needle — 0 or -1? And do you
   want the first occurrence or all of them?"*
2. **Describe the approach before writing it.** *"Try every starting position where the needle could
   fit, and at each one compare forward until a mismatch or until the needle runs out."*
3. **Say the bound out loud as you write it.** *"The last position the needle can start at is n minus
   m, so the loop is `range(n - m + 1)`."*
4. **Flag the short-circuit.** *"The bound test goes first in the while condition, or the moment
   everything matches I read past the end of the needle."*
5. **Give both costs, with the input for each.** *"O(n·m) worst case — you need something like a
   thousand a's with a needle of ten a's and a b, where every position matches almost the whole needle
   before failing. On ordinary text it's close to O(n), because most positions fail on the first
   character."*
6. **Say what the library does.** *"In production I'd call `find`, which uses a Boyer-Moore variant in
   C."*
7. **Offer the improvement before being asked.** *"If you want a guaranteed linear bound, that's KMP."*

### The follow-ups

**"What's the actual worst case, and can you construct it?"**
`O(n·m)`, and yes. I need the needle to almost match at every position and fail only at the end — so a
haystack of a thousand `a`s followed by a `b`, and a needle of ten `a`s followed by a `b`. At every one
of the roughly thousand starting positions, the inner loop matches ten characters and then fails on
the eleventh, so it does about `n × m` comparisons. I measured that exact case: 10,901 comparisons
against a theoretical maximum of 11,011, so it drives the algorithm to about 99% of its worst case.
The reason this rarely bites in practice is that natural language has almost no repetition of that
kind — on English prose the same code took 43 comparisons to find an eight-character needle 35
characters in, because the inner loop almost always fails on the very first character. So the honest
answer is that it is `O(n·m)` in theory and behaves linearly on text, and the inputs that break it are
DNA, binary data, and anything an adversary chose.

**"Can you do better?"**
KMP gives a guaranteed `O(n + m)`. The idea is that when the naive algorithm fails partway through the
needle, it throws away everything it just learned and restarts at the top of the needle one position
along. But it *does* know something: it knows exactly which characters of the needle it just matched.
KMP precomputes, for every prefix of the needle, the length of the longest proper prefix that is also
a suffix of it — and on a mismatch it slides the needle forward by that amount instead of by one, so
the haystack index never moves backwards. That is what makes it linear. Building the table is `O(m)`
and it uses `O(m)` extra space. I would not try to write it from memory unless you want to spend the
time, because the table construction is easy to get subtly wrong; I would rather give you a correct
naive solution and an accurate description of KMP.

**"Find all occurrences, including overlapping ones."**
Almost the same loop, with two changes. Instead of returning at the first match, append the position
and carry on. And critically, advance `start` by **one**, not by `m` — because `"aa"` occurs in
`"aaaa"` at positions 0, 1 and 2, and jumping by the needle length would find only 0 and 2. If
overlapping matches are explicitly not wanted, jumping by `m` is the correct behaviour, so this is a
contract question rather than a bug. Worth asking, because the phrase "all occurrences" is genuinely
ambiguous and the two answers differ.

**"How would you search for a thousand needles in the same text?"**
Not by running this a thousand times, which is `O(1000 · n · m)`. Two answers depending on the shape.
Rabin-Karp handles it well: it hashes the current window of the haystack and compares against a set
containing the hashes of all the needles, so one pass serves every needle, provided they are all the
same length. For needles of different lengths, the right answer is Aho-Corasick, which builds a single
automaton from all the patterns — essentially a trie with failure links, which is the KMP idea
generalised to many patterns — and then makes one pass over the haystack finding every occurrence of
every needle simultaneously, in `O(n + total pattern length + matches)`. That is what tools like `grep
-f` and intrusion-detection systems actually use. Tries arrive on
[day 120](../day-120-the-trie/README.md), and Aho-Corasick is the natural sequel.

### A model answer

> "Two questions first: what should I return for an empty needle, 0 or -1? And do you want just the
> first occurrence?
>
> ...0, and just the first. Good.
>
> The straightforward approach is to try every position in the haystack where the needle could
> possibly start, and at each of those compare the needle forward, character by character, until
> either something differs or the needle runs out. If it runs out, everything matched, so that
> position is the answer.
>
> ```python
> def str_str(haystack: str, needle: str) -> int:
>     if not needle:
>         return 0
>     n, m = len(haystack), len(needle)
>     for start in range(n - m + 1):
>         k = 0
>         while k < m and haystack[start + k] == needle[k]:
>             k += 1
>         if k == m:
>             return start
>     return -1
> ```
>
> Three details worth calling out. The outer loop goes to `n - m + 1`, because the last position the
> needle can start at is `n - m` — on a five-character haystack with a two-character needle the valid
> starts are 0 through 3. The `k < m` test has to come first in the while condition, because Python's
> `and` short-circuits and without that ordering the moment everything matches I'd read past the end
> of the needle. And `k` resets to zero at every start: whatever matched at the last position tells me
> nothing here, because the alignment moved.
>
> On cost: it's `O(n·m)` in the worst case and `O(1)` space. To actually hit the worst case you need a
> highly repetitive input — a thousand `a`s with a needle of ten `a`s and a `b` — where every position
> matches almost the whole needle and fails on the last character. I measured that: about 10,900
> comparisons for a thousand-character haystack. But on ordinary text it behaves linearly, because
> almost every position fails on the very first character — the same code found an eight-character
> phrase in 430 characters of English in 43 comparisons.
>
> In production I'd just call `find`, which uses a Boyer-Moore variant written in C — on that
> adversarial input it was about 23,000 times faster than my loop.
>
> And if you want a guaranteed linear bound, that's KMP. The insight is that when the naive version
> fails partway through the needle it discards everything it learned, but it does know which
> characters it just matched — so KMP precomputes, for each prefix of the needle, the longest proper
> prefix that is also a suffix, and slides the needle forward by that much on a mismatch rather than
> by one. The haystack index then never moves backwards, which gives `O(n + m)` with `O(m)` extra
> space for the table. I'd rather describe it than write it from memory — the table construction is
> famously easy to get subtly wrong — but I'm happy to work through it if you'd like."

---

## 9. Recall card

- **Naive search: try every start, compare forward, reset to the top of the needle each time.**
- **`range(n - m + 1)`** — the last valid start is `n - m`. And `k < m` goes **first** in the while
  condition.
- **`O(n·m)` worst case, `O(1)` space** — but close to `O(n)` on real text, because most positions fail
  on the first character.
- **The worst case needs repetition:** `"aaaa...b"` with needle `"aaab"`. Measured: 10,901 comparisons
  for `n = 1,001`.
- **Better: KMP `O(n + m)`** (never move the haystack index back), **Rabin-Karp** (rolling hash, many
  needles), **Boyer-Moore** (skip from the right). Name them; do not improvise them.
