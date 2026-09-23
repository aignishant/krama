---
day: 26
track: dsa
title: "Strings revision and mock round"
phase: "Strings"
status: written
---

# Day 026 · DSA — Strings revision and mock round

**After today you can:** You can solve two unseen string problems under time pressure.

**The interviewer asks it as:** *Two string problems, no hints, talk as you go.*

---

## 1. What this is, and why they ask it

Days 19 to 25 built the string toolkit: what a string is and why it is immutable, building one without
the quadratic trap, frequency maps, anagrams and canonical forms, palindromes and the two-ends habit,
substrings versus subsequences, and naive pattern matching. Today is the second mock round, and it is
about a different skill from [day 018](../day-018-arrays-revision/README.md).

Day 18 was about **process**: the six beats, narrating, testing with your own edge cases. That still
applies and you should still do it. Today adds the thing that actually decides string questions:
**recognition**. String problems are almost never new. They are one of about six patterns wearing
different words, and the whole game is deciding which one in the first ninety seconds. Get that right
and the code is fifteen lines you already know. Get it wrong and you spend twenty minutes writing
something correct that answers a different question.

There are six patterns, and §3 lists them with their tells. Every string problem in the last seven
days, and most of the ones you will be asked, is one of them.

---

## 2. The story

The workshop where Ramesh mends two-wheelers is under a tin roof at the end of a lane, and on a
Monday there will be nine or ten machines waiting by eight in the morning.

What he has learnt in nineteen years is not really about engines. It is that people cannot tell him
what is wrong, and they are not supposed to be able to, and it does not matter.

A man came in on Thursday and said the scooter was making a noise. Ramesh asked when, and the man
said when he goes over the humps near the school. On Friday a woman said hers felt loose at the
front. Last month a boy said his handlebar shook when he braked hard on the main road. Three
completely different sentences, three people who have never met, and the same worn part underneath
all three.

He does not have a list he goes through. What he has is that after nineteen years there are perhaps
six things that actually go wrong on a scooter of that age, and every complaint he has ever heard is
one of the six in different words. So he listens for about twenty seconds — not to the words, to what
is behind them — and by the time the man has finished talking Ramesh has usually decided, and the
rest is checking whether he is right.

His nephew has been with him for two years now and is good with a spanner. He is faster than Ramesh
at the actual work. But when a customer describes something he has not heard described in that way
before, he stands there, and then he starts taking things off the machine to find out. Sometimes that
works and it takes him an hour and a half.

Ramesh keeps telling him the same thing. It is not a new problem. You have fixed this exact thing
eleven times. What you have not heard before is the sentence.

---

## 3. The idea in plain English

Ramesh's six faults are today's six patterns. The customer's sentence changes every time; what is
underneath does not.

### The six string patterns, with their tells

| # | Pattern | The tell in the problem statement | Cost | Day |
|---|---|---|---|---|
| 1 | **Count and compare** | "how many times", "most common", "appears once", "duplicate" | `O(n)` | [021](../day-021-frequency-maps/README.md) |
| 2 | **Canonical form as a key** | "are these the same apart from order", "group these" | `O(n·k)` | [022](../day-022-anagrams/README.md) |
| 3 | **Two ends inwards** | "palindrome", "reverse", "from both sides" | `O(n)`, `O(1)` | [023](../day-023-palindromes/README.md) |
| 4 | **Sliding window** | "substring", "contiguous", "longest ... without", "at most k" | `O(n)` | [032](../day-032-variable-window/README.md) |
| 5 | **Build with a list and join** | the answer is a string you construct in a loop | `O(n)` | [020](../day-020-building-strings/README.md) |
| 6 | **Two indices, one per string** | comparing two strings position by position; "is A a subsequence of B" | `O(n + m)` | [024](../day-024-substrings-vs-subsequences/README.md) |

That is the whole list. Print it into your head, because **the first ninety seconds of every string
question is deciding which row you are in.**

### The three questions that pick the row

Ask these, in this order, and the pattern usually falls out:

1. **What shape is the answer?** A number → count or window. A boolean → compare or two ends. A string
   → build with a list. A list of groups → canonical form as a key.
2. **Contiguous or not?** From [day 024](../day-024-substrings-vs-subsequences/README.md): contiguous
   means a window; gaps allowed means two indices or a table.
3. **One string or two?** One → window or two ends. Two → one index per string, or a canonical form for
   each.

### The five facts that must be automatic

These come up in almost every string question and you should never have to think about them:

- **Strings are immutable.** `s[0] = "x"` is a `TypeError`. Building with `+=` in a loop is `O(n²)`;
  collect into a list and `"".join`.
- **`len` is `O(1)`; slicing is `O(k)` and copies.** So slicing inside a loop turns linear into
  quadratic, silently.
- **`sorted(s)` returns a list, not a string.** You need `"".join(sorted(s))` for a dictionary key,
  because a list is not hashable.
- **Every string method returns a new string.** `s.replace(...)` on its own does nothing.
- **`ord(ch) - ord("a")` is `O(1)` space and silently wrong** on anything but lowercase a–z, because
  negative indices do not raise.

### The four contract questions for any string problem

Forty seconds, and they catch most of the traps in the last seven days:

1. **Which characters count?** Letters only, alphanumeric, everything? (`isalnum` versus `isalpha` —
   `"0P"` from [day 023](../day-023-palindromes/README.md).)
2. **Does case matter?**
3. **What is the alphabet?** Lowercase English lets you use 26 slots; Unicode does not.
4. **What do I return for the empty string?** Almost always a defined value, almost never an error.

### The two beats that matter most today

Day 18's six beats still hold — clarify, example, brute force, optimise, code, test. Two of them carry
extra weight for string problems:

**Beat 3, the brute force, is where you say the pattern out loud.** Not *"I'd check every
substring"*, but *"this is asking for a contiguous run, so it's a sliding window, and the brute force
would be to check every substring at O(n²)"*. Naming the family is the thing being scored.

**Beat 6, testing, has a fixed list for strings.** Empty string. One character. All the same character.
Everything different. And, for anything with rules, one input that is only punctuation. Those five find
almost every string bug you can write.

---

## 4. The picture

The decision, as a shape you can run in ninety seconds:

```
   read the problem
          |
          v
   what shape is the answer?
          |
   +------+---------+------------------+------------------+
   |                |                  |                  |
 a number         a boolean          a string        a list of groups
   |                |                  |                  |
   v                v                  v                  v
 contiguous?     one string        build it with      canonical form
   |               or two?         a list + join       as a dict key
   |                 |                                (day 022)
 +-+--+          +---+----+
 |    |          |        |
yes   no        one      two
 |    |          |        |
 v    v          v        v
window  count   two ends  two indices
(day 032)(021)  (day 023) (day 024)
```

**What to notice:** four questions, six leaves, and every string problem from the last seven days
lands on one of them. This is the picture to be able to redraw from memory.

The five test inputs, as a checklist you run every time:

```
   +---------------------+---------------------------+
   | ""                  | the empty case            |
   | "a"                 | one character             |
   | "aaaa"              | all the same              |
   | "abcd"              | all different             |
   | ".,! "              | nothing that counts       |
   +---------------------+---------------------------+
              ^
       these five find almost every string bug
```

**What to notice:** none of them is the example the interviewer gave you. That example is guaranteed
to pass. Testing it proves nothing, and testing these proves quite a lot.

---

## 5. The code, built step by step

Two problems, worked as transcripts. Read them for the order things are said, not for the solutions.

### Problem one — Isomorphic Strings

> *"Two strings are isomorphic if you can replace the characters of the first to get the second, with
> each character mapping to exactly one other character and no two characters mapping to the same one.
> `egg` and `add` are isomorphic. `foo` and `bar` are not."*

**Beat 1, clarify.** *"So it's a one-to-one mapping in both directions? That is, can two different
characters of `s` both map to the same character of `t`?"* No — that is the whole trap. *"And are the
strings guaranteed the same length?"*

**Beat 2, example.** *"`egg` → `add`: `e` goes to `a`, `g` goes to `d`, and the second `g` also goes to
`d`, which is consistent. `foo` → `bar`: `o` would have to go to both `a` and `r`, so no."*

Then produce the input that shows you understood the follow-up question you asked:

*"And `badc` → `baba` is the interesting one. Every character of the first maps consistently — `b`→`b`,
`a`→`a`, `d`→`b`, `c`→`a`. But `b` and `d` both map to `b`, so it fails the one-to-one requirement in
the other direction."*

**Producing that example unprompted is the whole question.** It is the difference between a solution
with one dictionary and a correct one.

**Beat 3, brute force.** *"There isn't much of one here. The naive thing is to build the mapping and
check consistency, which is already linear."*

**Beat 4, name the pattern.** *"Shape of the answer is a boolean, and I'm comparing two strings position
by position — so it's the two-indices family, walking both together. I'll need two dictionaries, one
for each direction."*

**Beat 5, code.**

```python
if len(s) != len(t):
    return False
forward, backward = {}, {}
```

*"Length check first, free. Two maps because the relationship has to hold both ways."*

```python
for a, b in zip(s, t):
    if a in forward and forward[a] != b:
        return False
    if b in backward and backward[b] != a:
        return False
    forward[a] = b
    backward[b] = a
return True
```

*"`zip` walks both strings together, which is cleaner than indexing. For each pair: if I have seen this
character of `s` before and it mapped somewhere else, fail. If this character of `t` has already been
claimed by a different character, fail. Otherwise record both directions."*

**Beat 6, test.** `("egg","add")` True. `("foo","bar")` False. `("paper","title")` True.
`("badc","baba")` False — the one that needs the second map. `("","")` True. `("ab","aa")` False.

### Problem two — String Compression

> *"Compress a string by replacing runs with the character and the count: `aabcccccaaa` becomes
> `a2b1c5a3`. If the compressed version is not shorter, return the original."*

**Beat 1, clarify.** *"Runs of one become `a1`, or just `a`? And if the result is the same length as
the original, do I return the original or the compressed one?"* Say `a1`, and return the original on a
tie.

**Beat 2, example.** *"`aabcccccaaa` → `a2b1c5a3`, which is 8 against 11, so return the compressed one.
`abcdef` → `a1b1c1d1e1f1`, which is 12 against 6, so return the original."*

**Beat 3 and 4, name the pattern.** *"The answer is a string I build in a loop, so this is the
build-with-a-list-and-join family. And it's a grouping loop over consecutive characters, which means
there's a last group that ends by running out rather than by changing — I'll need to handle that."*

**Naming the flush before writing it** is exactly what
[day 020](../day-020-building-strings/README.md) drilled, and interviewers watch for it.

**Beat 5, code.** Using the two-index form, which avoids the flush entirely:

```python
parts: list[str] = []
i = 0
while i < len(s):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
```

*"`i` marks the start of a run and `j` walks to the end of it. When the inner loop stops, the run is
`s[i:j]` and its length is `j - i`."*

```python
    parts.append(s[i])
    parts.append(str(j - i))
    i = j
```

*"Emit the character and the count, then jump `i` to the start of the next run."*

**This shape has no last-group problem**, because the run is consumed and emitted inside one turn of
the outer loop rather than being detected by a change. Say that out loud — it is a real reason to
prefer this form.

```python
out = "".join(parts)
return out if len(out) < len(s) else s
```

*"Join once, and honour the contract about not being shorter."*

**Beat 6, test.** `"aabcccccaaa"` → `"a2b1c5a3"`. `"abcdef"` → `"abcdef"`. `"aabb"` → `"aabb"` (the
compressed form is the same length, so the original wins). `""` → `""`. `"a"` → `"a"`.

### The complete solutions

```python
def is_isomorphic(s: str, t: str) -> bool:
    """LeetCode 205. One-to-one mapping in BOTH directions — 'badc'/'baba' proves it."""
    if len(s) != len(t):
        return False
    forward: dict[str, str] = {}
    backward: dict[str, str] = {}
    for a, b in zip(s, t):
        if a in forward and forward[a] != b:
            return False
        if b in backward and backward[b] != a:      # without this, badc/baba passes
            return False
        forward[a] = b
        backward[b] = a
    return True


def compress(s: str) -> str:
    """'aabcccccaaa' -> 'a2b1c5a3'. Returns the original if compressing does not shorten it.

    Two indices: i starts a run, j walks to its end. No last-group flush needed.
    """
    parts: list[str] = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        parts.append(s[i])
        parts.append(str(j - i))
        i = j
    out = "".join(parts)
    return out if len(out) < len(s) else s


if __name__ == "__main__":
    print([is_isomorphic(a, b) for a, b in
           (("egg", "add"), ("foo", "bar"), ("paper", "title"),
            ("badc", "baba"), ("", ""), ("ab", "aa"))])
    # [True, False, True, False, True, False]

    print([compress(x) for x in ("aabcccccaaa", "abcdef", "aabb", "", "a")])
    # ['a2b1c5a3', 'abcdef', 'aabb', '', 'a']
```

---

## 6. What it costs

### `is_isomorphic`

`zip(s, t)` produces `n` pairs, where `n` is the common length. Each turn does at most two dictionary
lookups and two assignments, all `O(1)` on average. So **O(n) time**.

Space: two dictionaries, each holding at most one entry per distinct character. For lowercase English
that is at most 26 each, so **O(1) space** for a bounded alphabet, `O(k)` in general.

Count the comparisons rather than naming a class: `n` turns × 4 dictionary operations = `4n`
operations, which is linear.

### `compress`

The outer `while` and the inner `while` between them advance through the string exactly once — every
character is consumed by exactly one run, and `i` jumps straight to `j`. So **O(n) time**, despite the
nested loop. That is the same argument as
[day 023](../day-023-palindromes/README.md): count how far the indices travel in total, not how many
loops there are.

Space: `parts` holds at most `2n` pieces in the worst case (every character distinct, so a character
and a `"1"` each), and the joined result is at most `2n` characters. **O(n) space.**

The in-place version from [day 020](../day-020-building-strings/README.md), which mutates a
`list[str]` and returns a length, is **O(1) extra space** — and it only works because the problem hands
you a list rather than a string.

### The pattern costs, as a table to have memorised

| Pattern | Time | Space |
|---|---|---|
| count and compare | `O(n)` | `O(k)`, `O(1)` for a bounded alphabet |
| canonical form: sorting | `O(n · k log k)` | `O(n · k)` |
| canonical form: counting | `O(n · k)` | `O(n · k)` |
| two ends inwards | `O(n)` | `O(1)` |
| sliding window | `O(n)` | `O(k)` |
| build with list + join | `O(n)` | `O(n)` |
| build with `+=` in a loop | **`O(n²)`** | `O(n)` |
| naive pattern matching | `O(n · m)` worst, ~`O(n)` typical | `O(1)` |
| longest common subsequence | `O(m · n)` | `O(m · n)`, `O(n)` rolled |

**The only `O(n²)` in that table that you can accidentally write is the `+=` one**, and it is the one
that most often goes unnoticed, because the code is correct.

### The numbers to have ready

> Building a 100,000-character string with `+=` is about 5 billion character copies; with a list and
> `join` it is about 300,000 operations. A string of length `n` has `n(n+1)/2` substrings and `2ⁿ`
> subsequences — 210 against a million at `n = 20`. Naive substring search took 43 comparisons on
> English text and 10,901 on an adversarial input of the same size.

---

## 7. The traps

### The near-miss: one map instead of two

```python
def is_isomorphic(s, t):
    mapping = {}
    for a, b in zip(s, t):
        if a in mapping and mapping[a] != b:
            return False
        mapping[a] = b
    return True

print(is_isomorphic("badc", "baba"))
```

```
True
```

Wrong. Every character of `s` maps consistently, but `b` and `d` both map to `b`, so the mapping is
not one-to-one. **A single dictionary only checks that the mapping is a function; it does not check
that it is injective.** The second dictionary is what enforces the other direction, and `"badc"` /
`"baba"` is the input that finds it. This one passes `"egg"`/`"add"`, `"foo"`/`"bar"` and
`"paper"`/`"title"` — every example the problem gives you.

### The real error: mutating a string

```python
s = "hello"
s[0] = "H"
```

```
TypeError: 'str' object does not support item assignment
```

Seven days on and it is still the most common string error there is. `list(s)`, mutate, `"".join`.

### The near-miss: the accidental quadratic

```python
def compress(s):
    out = ""
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += s[i] + str(j - i)        # here
        i = j
    return out
```

Correct output, wrong complexity. The algorithm is `O(n)` and the string building makes it `O(n²)`.
There is no error and no wrong answer — it simply gets slow, and only on inputs bigger than the ones
you tested. Whenever you see `+=` on a string inside any loop, that is the bug.

### The near-miss: slicing inside a loop

```python
for i in range(len(s)):
    if s[i:] .startswith(needle):    # s[i:] copies the rest of the string, every turn
        return i
```

`s[i:]` is `O(n - i)`, so the loop is `O(n²)` even though it looks linear. Use `s.startswith(needle,
i)`, which takes a start position and copies nothing, or compare with indices. **Slicing is the
silent quadratic of string code**, and it is much harder to spot than `+=`.

### The near-miss: testing only the given example

The example in the problem statement is guaranteed to pass, because you built the solution around it.
It is the least informative test you have. Run the five from §4 instead: `""`, `"a"`, `"aaaa"`,
`"abcd"`, and one input containing nothing that counts.

### The process trap: pattern-matching too fast

Recognition is today's skill and it has a failure mode. A problem that *sounds* like a window and is
actually a subsequence question costs you the whole round. **Recognition tells you which family to
consider; the contract questions confirm it.** Say the family out loud and then verify it against the
statement — *"this says contiguous, so a window is right"* — rather than jumping straight into the
code you remember.

---

## 8. In the interview

### How it gets asked

- *"We'll do two problems. Talk me through your thinking."* — the standard opening.
- *"Here's a string problem"* — where the first ninety seconds of pattern recognition decide the next
  thirty minutes.
- *"Can you do it in O(1) space?"* — the follow-up that means "stop building a copy", and usually
  points at two pointers or a write pointer.
- *"How would you test this?"* — a gift, if you have the five inputs ready.

### What to say out loud, in the first ninety seconds

The same script for every string problem:

1. **Restate it in your own words.** If your restatement is wrong you find out now.
2. **Ask the four contract questions.** Which characters count, does case matter, what alphabet, what
   about the empty string.
3. **Name the family, explicitly.** *"The answer is a boolean and I'm comparing two strings position by
   position, so this is the two-indices family."* This is the sentence today exists to install.
4. **Confirm it against the statement.** *"It says contiguous, so a window rather than a subsequence
   table."*
5. **Give the brute force with its cost**, then the better approach with its cost, then pause for
   agreement.
6. **Name the trap you are about to avoid**, before you write it — the second map, the flush, the
   `join` instead of `+=`.
7. **Test with your five**, not with their example.

### The follow-ups

**"How did you know which technique to use?"**
A genuine question, and worth answering properly rather than saying "experience". I ask three things.
What shape is the answer — a number points at counting or a window, a boolean at comparison, a string
at building with a list, a list of groups at a canonical form used as a key. Is it contiguous — that
word decides between a sliding window and a table, and if it is not in the statement I ask. And is it
one string or two — one suggests a window or two ends, two suggests one index per string. Those three
questions land on one of about six patterns, and every string problem I have seen is one of them
wearing different words.

**"Do it in O(1) space."**
For string problems that almost always means one of two things. Either stop building a copy — replace
`cleaned = "".join(...)` and a reverse with two indices walking inwards, which is the palindrome
answer. Or, if I have been handed a `list[str]` rather than a `str`, use a write pointer and mutate in
place, returning a length. The signature tells me which: `s: str` means build and return, `chars:
list[str]` means mutate and count. The one thing I cannot do is mutate a Python string, because it is
immutable — so if the input is a string and you want constant space, the answer has to be an algorithm
that never materialises anything, not a clever way to edit it.

**"Your solution passes all the examples. Convince me it's correct."**
I would not argue from the examples, because I built it around them. I would state the property the
code maintains and then attack it. For isomorphic strings, the property is that after processing `k`
pairs, `forward` and `backward` describe a bijection consistent with the first `k` characters — and
the two checks before the assignments are exactly what preserve that. Then I would deliberately look
for the input that breaks a *nearly* correct version, which here is `badc`/`baba`: it passes every
example in the problem statement and fails on one dictionary. Being able to produce the input that
breaks the plausible-but-wrong solution is a much stronger correctness argument than any number of
passing tests.

**"What would you test?"**
Five inputs, and none of them is the example you gave me. The empty string, because it is the one that
raises. A single character, because it exercises the loop-runs-once path. All-the-same, because it
maximises runs and windows. All-different, because it minimises them. And one input containing nothing
that counts — pure punctuation — because that is what walks an index off the end in any solution with
skip loops. For a problem with two strings I would add unequal lengths, and one where the answer is at
the very last position, since off-by-one errors in the loop bound hide there.

### A model answer

Written out for problem one.

> "Let me restate it: I need to decide whether there is a one-to-one character mapping that turns `s`
> into `t`. Two questions — is it one-to-one in both directions, meaning two different characters of
> `s` cannot both map to the same character of `t`? And are the strings the same length?
>
> ...Both ways, and lengths may differ. Good, that second point matters and I'll guard for it.
>
> On `egg` and `add`: `e` maps to `a`, `g` maps to `d`, and the second `g` maps to `d` again, which is
> consistent. On `foo` and `bar`, `o` would have to map to both `a` and `r`, so no.
>
> The interesting case is `badc` and `baba`. Every character of the first maps consistently — `b`→`b`,
> `a`→`a`, `d`→`b`, `c`→`a` — but `b` and `d` both end up at `b`, so it fails in the other direction.
> I mention it because a solution with one dictionary passes all three of the standard examples and
> fails on that one.
>
> Pattern-wise: the answer is a boolean and I am walking two strings position by position, so this is
> the two-indices family, and because the relationship has to hold both ways I need two maps.
>
> ```python
> def is_isomorphic(s: str, t: str) -> bool:
>     if len(s) != len(t):
>         return False
>     forward, backward = {}, {}
>     for a, b in zip(s, t):
>         if a in forward and forward[a] != b:
>             return False
>         if b in backward and backward[b] != a:
>             return False
>         forward[a] = b
>         backward[b] = a
>     return True
> ```
>
> `zip` walks both together, which reads better than indexing and stops at the shorter one — though the
> length check already ruled that out. For each pair: if I have seen this character of `s` mapping
> somewhere else, fail; if this character of `t` has already been claimed by a different source, fail;
> otherwise record both directions.
>
> That is O(n) time — n pairs, four constant-time dictionary operations each — and O(k) space where k
> is the alphabet size, so O(1) for lowercase English.
>
> For tests: the three examples, then `badc`/`baba` for the injectivity check, then the empty string,
> a single character, and unequal lengths."

---

## 9. Recall card

- **Six patterns:** count · canonical key · two ends · sliding window · list-and-join · two indices.
  Decide which in the first ninety seconds.
- **Three questions that pick it:** what shape is the answer, is it contiguous, one string or two?
- **Four contract questions:** which characters count, does case matter, what alphabet, what about
  empty?
- **Five test inputs, never the given example:** `""`, `"a"`, `"aaaa"`, `"abcd"`, and one with nothing
  that counts.
- **The two silent quadratics:** `+=` on a string in a loop, and slicing inside a loop. Both are
  correct and both are slow.
