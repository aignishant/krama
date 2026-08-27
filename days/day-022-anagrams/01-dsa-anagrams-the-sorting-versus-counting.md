---
day: 22
track: dsa
title: "Anagrams: the sorting versus counting choice"
phase: "Strings"
status: written
---

# Day 022 · DSA — Anagrams: the sorting versus counting choice

**After today you can:** You can give two solutions with different complexities and say which one you would ship.

**The interviewer asks it as:** *Are these two strings anagrams? Now group a list of words into anagram groups.*

---

## 1. What this is, and why they ask it

Two strings are **anagrams** if one is a rearrangement of the other — same letters, same number of
each, different order. `listen` and `silent`. `eat` and `tea`.

The question has exactly one idea in it, and it is a big one: **find a form of the string that is
identical for all its anagrams, and different for everything else.** That is called a **canonical
form**, and once you have one, "are these anagrams?" becomes "are their canonical forms equal?", and
"group these words" becomes "put them in a dictionary keyed by canonical form". There are two natural
canonical forms — the letters in sorted order, and the count of each letter — and choosing between
them is the whole exercise.

Interviewers like this because it has **two correct answers with different complexities**, which is
rare and useful. Sorting is one line and `O(k log k)` per word; counting is five lines and `O(k)`.
Producing both, unprompted, and then saying which you would actually ship and why, is a complete
demonstration of the thing they are trying to measure. Producing only the one-liner is fine and
unremarkable. Producing only the counting version and never mentioning that `sorted(a) == sorted(b)`
exists looks like you have memorised a solution.

It is LeetCode 242 and 49, it appears in phone screens everywhere, and the canonical-form idea itself
comes back on [day 064](../day-064-grouping/README.md) as a design skill in its own right.

---

## 2. The story

Murugan drives a school van in Coimbatore, the small yellow one, and he has eight children on the
afternoon round. He picks them up from the gate at half past three and drops the last one at Ganapathy
by about a quarter past four.

Getting them into the van is not the problem. The problem is knowing that the eight who got in are the
eight who are meant to be in it, because at half past three there are two hundred children coming out
of one gate and four vans parked in a line, and children are not careful.

They never sit in the same places. Whoever gets there first takes the back seat, the two brothers
fight about the window, and one girl always sits behind him because she says the back makes her
sick. So he cannot check by looking at the seats. The arrangement is different every single day and
it does not mean anything.

The first thing he does takes two seconds. He counts heads. If there are seven, something is wrong,
and if there are nine, something is very wrong, and either way he does not need to know anything else
yet — he gets out and goes and looks. Most days it is eight and he carries on.

Then he does the actual check, and he has two ways of doing it depending on his mood.

Some days he makes them sit in the order he always uses — the two brothers at the front, then the
girl from Race Course, and so on down the van, the same order every day — and then one look tells
him. Everyone in their proper place, nobody extra, nobody missing.

Most days he does not bother with that, because getting eight children to move is harder than it
sounds. Instead he reads out the names from the list on his phone and each one shouts. Eight names,
eight shouts, and if he gets to the end and a name has not been answered, or somebody shouts twice,
he knows.

Both ways work. The first takes longer because he has to rearrange everybody. The second is quicker
but he has to have the list. And on the day a boy from another van climbed in by mistake, the head
count had already told Murugan something was wrong before he started either of them.

---

## 3. The idea in plain English

Murugan's two methods are the two solutions. Making everyone sit in the fixed order is **sorting**.
Reading the names off the list is **counting**. And counting heads first is the length check, which
you should always do.

### What the question is really asking

Two strings are anagrams when they contain the same characters with the same multiplicities, ignoring
order. So you need a way of describing a string that **throws the order away and keeps nothing
else**. Any two anagrams must produce the same description, and any two non-anagrams must produce
different ones.

That description is the **canonical form**, and there are two obvious choices.

### Canonical form one: sort the letters

```python
sorted("listen")     # ['e', 'i', 'l', 'n', 's', 't']
sorted("silent")     # ['e', 'i', 'l', 'n', 's', 't']
```

`sorted` on a string returns a **list of characters**, not a string — surprising the first time, and
it does not matter for comparison because two equal lists compare equal. If you need a string, as
you will for a dictionary key, use `"".join(sorted(s))`.

Sorting puts the letters into one fixed order regardless of how they started, so any two anagrams
land on the same result. That is Murugan making everyone sit in the same seats.

```python
def is_anagram(a: str, b: str) -> bool:
    return sorted(a) == sorted(b)
```

One line, correct, and worth writing first.

### Canonical form two: count the letters

```python
Counter("listen")    # {'l':1,'i':1,'s':1,'e':1,'n':1,'t':1}
Counter("silent")    # {'s':1,'i':1,'l':1,'e':1,'n':1,'t':1}
```

Two `Counter`s compare equal when they hold the same keys with the same values, and dictionaries do
not care about insertion order for equality. So:

```python
def is_anagram(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)
```

That is Murugan reading out the names. The frequency map from
[day 021](../day-021-frequency-maps/README.md), used as an identity rather than as a count.

### The length check, which is free

`if len(a) != len(b): return False` costs nothing — `len` is `O(1)` on both a string and a list from
[day 019](../day-019-what-a-string-is/README.md) — and it exits immediately on a whole class of
inputs. It is Murugan counting heads.

Strictly, the sorting version does not need it and the counting version does not either, since
different lengths produce different counts. Write it anyway and say why: **it is the cheapest possible
rejection and it makes the intent obvious.** Interviewers notice.

### Grouping: the same idea, one level up

*"Group these words into anagram groups"* — LeetCode 49 — is the canonical form used as a
**dictionary key**:

```python
groups = defaultdict(list)
for word in words:
    groups[canonical(word)].append(word)
return list(groups.values())
```

That is the entire algorithm. All the thinking is in `canonical`. With sorting:

```python
groups["".join(sorted(word))].append(word)
```

`"".join(sorted(word))` rather than `sorted(word)`, because a **dictionary key must be hashable** and
a list is not — from [day 019](../day-019-what-a-string-is/README.md), only immutable things can be
keys. §7 shows the exact error.

With counting, the same constraint applies, so the count has to become a tuple:

```python
key = [0] * 26
for ch in word:
    key[ord(ch) - ord("a")] += 1
groups[tuple(key)].append(word)          # tuple, because a list cannot be a key
```

A 26-element tuple of counts, identical for all anagrams of a word and different for everything else.

### Which to ship

Sorting is `O(k log k)` per word; counting is `O(k)`. So counting wins asymptotically, and that is the
answer to *"can you do better?"*.

But be honest about the size of the win. Measured in Python on 2,000 words:

```
word length   sorting    counting
     10       0.0028 s   0.0027 s
    100       0.0155 s   0.0162 s
  1,000       0.1834 s   0.1172 s
  5,000       0.9841 s   0.7152 s
```

At realistic word lengths they are the same, and counting only pulls ahead around a thousand
characters — because `sorted` runs as compiled C while the counting loop runs as Python bytecode, and
that constant factor swamps a `log k` of about 5. **For ordinary words I would ship the sorted
version, because it is one line and obviously correct. For long strings, or if the interviewer asks
for better than `O(k log k)`, I would switch to counting.** That sentence is the answer to the
question.

---

## 4. The picture

The two canonical forms:

```
   SORTING                                  COUNTING
   -------                                  --------
   "eat"  -> a e t                          "eat"  -> a:1 e:1 t:1
   "tea"  -> a e t   same                   "tea"  -> a:1 e:1 t:1   same
   "ate"  -> a e t                          "ate"  -> a:1 e:1 t:1
   "tan"  -> a n t   different              "tan"  -> a:1 n:1 t:1   different

   cost per word: O(k log k)                cost per word: O(k)
   key type: a string                       key type: a tuple of 26 counts
```

**What to notice:** both columns collapse the three arrangements of `eat` onto one thing, and keep
`tan` apart. That is all a canonical form has to do. Anything with those two properties would work —
these two are simply the cheapest to compute.

Grouping, as one pass into a dictionary:

```
   word     canonical key      the dictionary after this word
   ----     -------------      ------------------------------
   eat      "aet"              { "aet": ["eat"] }
   tea      "aet"              { "aet": ["eat","tea"] }
   tan      "ant"              { "aet": ["eat","tea"], "ant": ["tan"] }
   ate      "aet"              { "aet": ["eat","tea","ate"], "ant": ["tan"] }
   nat      "ant"              { "aet": [...], "ant": ["tan","nat"] }
   bat      "abt"              { "aet": [...], "ant": [...], "abt": ["bat"] }

   answer = list of the values = [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

**What to notice:** one pass, and each word is looked at exactly once. There is no comparing of words
against each other at all — which is what makes it `O(n·k)` instead of the `O(n²·k)` you would get by
testing every pair.

The count key, laid out:

```
   "tan"      t a n
              | | |
   index:     0    1    2  ...  13   ...  19  ...  25
            +---+---+---+     +---+     +---+    +---+
            | 1 | 0 | 0 |     | 1 |     | 1 |    | 0 |
            +---+---+---+     +---+     +---+    +---+
              a   b   c         n         t        z

   key = (1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0)
```

**What to notice:** the key is a fixed 26 numbers whatever the word, so building it is `O(k)` to fill
and `O(26)` to hash — constant. Twenty-five of the twenty-six entries here are noise, which is the
price of the fixed shape.

---

## 5. The code, built step by step

### The one-liner, and why to write it first

```python
def is_anagram_sorting(a: str, b: str) -> bool:
    return sorted(a) == sorted(b)
```

Correct for every input including empty strings, handles any characters including Unicode, and needs
no explanation. Write it, say `O(k log k)`, and then offer the better one. Starting from the simple
correct thing and improving it is exactly the shape an interviewer wants.

### The counting version

```python
def is_anagram_counting(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)
```

Two `Counter`s are equal when every key has the same value in both. The length guard is the free
early exit.

### The counting version without the library

Asked to do it without `Counter`, this is the one to write — and it is better than it looks, because
it does a single combined pass rather than two:

```python
def is_anagram_manual(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    counts = [0] * 26
    for ch in a:
        counts[ord(ch) - ord("a")] += 1      # lowercase a-z only
    for ch in b:
        counts[ord(ch) - ord("a")] -= 1
        if counts[ord(ch) - ord("a")] < 0:   # b has a letter a did not
            return False
    return True
```

Two things worth saying out loud while you write it.

**The second loop subtracts rather than building a second count.** If the two strings are anagrams,
every entry returns to zero.

**The early exit inside the second loop is what removes the final check.** The moment any count goes
negative, `b` contains a character more often than `a` does, so they cannot be anagrams. And because
the lengths are equal, if no count ever goes negative then none can be left positive either — so
there is no need to scan the array at the end. That last sentence is a genuinely good thing to say
in an interview.

### Grouping, with sorted keys

```python
def group_anagrams_sorting(words: list[str]) -> list[list[str]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())
```

Four lines. `"".join(sorted(word))` because a list cannot be a dictionary key.

### Grouping, with count keys

```python
def group_anagrams_counting(words: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in words:
        key = [0] * 26
        for ch in word:
            key[ord(ch) - ord("a")] += 1
        groups[tuple(key)].append(word)      # tuple: hashable, list is not
    return list(groups.values())
```

The only differences are how the key is built and that it must be frozen into a tuple.

### The complete solutions

```python
from collections import Counter, defaultdict


def is_anagram_sorting(a: str, b: str) -> bool:
    """LeetCode 242, the one-liner. O(k log k). Works on any characters."""
    return sorted(a) == sorted(b)


def is_anagram_counting(a: str, b: str) -> bool:
    """The same, in O(k). The length check is a free early exit."""
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)


def is_anagram_manual(a: str, b: str) -> bool:
    """Without the library. Lowercase a-z only. One count, incremented then decremented."""
    if len(a) != len(b):
        return False
    counts = [0] * 26
    for ch in a:
        counts[ord(ch) - ord("a")] += 1
    for ch in b:
        index = ord(ch) - ord("a")
        counts[index] -= 1
        if counts[index] < 0:                # b has more of this letter than a does
            return False
    return True                              # equal lengths + nothing negative => anagram


def group_anagrams_sorting(words: list[str]) -> list[list[str]]:
    """LeetCode 49. Key = the letters in sorted order. O(n * k log k)."""
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


def group_anagrams_counting(words: list[str]) -> list[list[str]]:
    """The same in O(n * k). Key = a 26-tuple of letter counts."""
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in words:
        key = [0] * 26
        for ch in word:
            key[ord(ch) - ord("a")] += 1
        groups[tuple(key)].append(word)
    return list(groups.values())


if __name__ == "__main__":
    for f in (is_anagram_sorting, is_anagram_counting, is_anagram_manual):
        print(f.__name__,
              f("anagram", "nagaram"),   # True
              f("rat", "car"),           # False
              f("a", "ab"),              # False
              f("", ""),                 # True
              f("aacc", "ccac"))         # False  — same letters, different counts

    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(group_anagrams_sorting(words))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(group_anagrams_counting(words))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(group_anagrams_sorting([]))    # []
    print(group_anagrams_sorting([""]))  # [['']]
```

Note the test `f("aacc", "ccac")`. Both have four characters from `{a, c}`, and they are **not**
anagrams — `aacc` has two of each, `ccac` has one `a` and three `c`. Any solution that checks only
*which* letters appear, using a set, gets this wrong. It is the input to reach for when you want to
break somebody's set-based answer, including your own.

---

## 6. What it costs

Let `k` be the length of a word and `n` the number of words.

### `is_anagram`

**Sorting.** `sorted` on `k` characters is `O(k log k)`, done twice, then a comparison of two lists of
length `k` which is `O(k)`. Total **O(k log k)** time. Space is two lists of `k` characters, so
**O(k)**.

**Counting.** One pass over each string, `k` steps each, with constant-time dictionary operations —
`2k` steps. Then comparing two dictionaries of at most 26 entries. Total **O(k)** time. Space is one
entry per distinct character, at most 26 for lowercase English, so **O(1)**.

So counting is asymptotically better in both time and space, and that is the answer when asked "can
you do better?".

### Grouping

Each word is processed once and appended once, so:

- **Sorting:** `n` words × `O(k log k)` each = **O(n · k log k)**.
- **Counting:** `n` words × `O(k)` each = **O(n · k)**.

Space for both is `O(n · k)` — every word is stored once in the output, plus the keys.

Notice what is **not** here: no comparison between words. The naive approach of testing every pair
would be `O(n² · k)`; at `n = 10,000` that is 100 million pair tests against 10,000 key computations.
**The dictionary turns a pairwise problem into a single pass, and that is the real lesson of the
grouping question.**

### The honest measurement

2,000 randomly generated lowercase words, grouped:

```
word length   sorting     counting    ratio
     10       0.0028 s    0.0027 s     1.0x
    100       0.0155 s    0.0162 s     0.96x  (sorting slightly faster)
  1,000       0.1834 s    0.1172 s     1.6x
  5,000       0.9841 s    0.7152 s     1.4x
```

At `k = 10` and `k = 100` there is nothing between them, and at `k = 100` sorting is marginally
ahead. The reason is that `log₂(100)` is about 7, so sorting does roughly seven times the *asymptotic*
work — but `sorted` is compiled C and the counting loop is interpreted Python, and that constant
factor is worth more than the 7×. Only when `k` reaches a thousand does the asymptotic difference
start to show.

**The honest conclusion:** counting is the better answer to give, sorting is usually the better code
to ship for word-sized strings, and being able to say both — with the reason — is worth more than
either.

### The number to have ready

> Sorting is `O(k log k)` per word, counting is `O(k)`. Grouping `n` words is `O(n·k log k)` or
> `O(n·k)` — and either way it beats the `O(n²·k)` of comparing every pair, which at ten thousand
> words is a hundred million comparisons against ten thousand key computations.

---

## 7. The traps

### The real error: a list as a dictionary key

```python
groups = {}
groups[sorted("eat")] = ["eat"]
```

```
TypeError: unhashable type: 'list'
```

A dictionary key must be **hashable**, and only immutable things are — the reason from
[day 019](../day-019-what-a-string-is/README.md): a key that could change after being filed could
never be found again. So `sorted(word)`, which is a list, has to become `"".join(sorted(word))` or
`tuple(sorted(word))`. Same for the count key: `tuple(key)`, not `key`.

This is the single most common error in the grouping problem and the message names the cause exactly.

### The near-miss: using a set instead of a count

```python
def is_anagram(a, b):
    return set(a) == set(b)      # wrong
```

```python
is_anagram("aacc", "ccac")       # True  — should be False
is_anagram("aab", "abb")         # True  — should be False
```

A set records **which** characters appeared and throws away **how many**. Anagram is about
multiplicities, so a set is the wrong structure — exactly the distinction drawn on
[day 021](../day-021-frequency-maps/README.md). It passes on `listen`/`silent` and on most casual
test data, which is why it survives long enough to reach a grader.

### The near-miss: the missing length check in the manual version

```python
def is_anagram(a, b):
    counts = [0] * 26            # no length check
    for ch in a:
        counts[ord(ch) - ord("a")] += 1
    for ch in b:
        counts[ord(ch) - ord("a")] -= 1
        if counts[ord(ch) - ord("a")] < 0:
            return False
    return True

print(is_anagram("aab", "ab"))
```

```
True
```

Wrong. `"aab"` and `"ab"` are not anagrams, but nothing ever goes negative — the leftover `a` sits
in the array as a positive 1 and is never examined. **The early-exit logic is only valid because the
lengths are equal**, and removing the length check silently removes that guarantee. If you want to
drop the length check you must scan the array for a non-zero entry at the end, which costs another 26
steps. The length check is cheaper and clearer.

### The silent bug: `ord` on anything but lowercase

```python
counts[ord(ch) - ord("a")] += 1
print(is_anagram_manual("Listen", "Silent"))
```

`ord("L") - ord("a")` is `-21`, a perfectly legal negative index, so the capital letters are counted
into the wrong slots with no error at all — the trap from
[day 021](../day-021-frequency-maps/README.md). It happens to return `True` here, for the wrong
reason. Normalise first with `.lower()`, and say the assumption out loud before you rely on it.

### The contract question: what counts as an anagram?

Three things the interviewer may or may not want, and you should ask rather than guess:

- **Case.** Is `Listen` an anagram of `Silent`? Usually yes, so `.lower()` both.
- **Spaces and punctuation.** Is `"conversation"` an anagram of `"voices rant on"`? The classic
  phrase-anagram version strips non-letters first.
- **Unicode.** `é` can be one code point or `e` plus a combining accent, and those compare unequal.
  If the input may be Unicode, normalise with `unicodedata.normalize("NFC", s)` first.

Asking one of these takes five seconds and shows you read the problem rather than pattern-matched it.

### The near-miss: comparing `sorted` results of different types

```python
sorted("abc") == "abc"           # False
```

`sorted` returns a **list**, so `['a','b','c'] == "abc"` is `False`. Harmless when you compare two
`sorted` calls with each other, and a real bug the moment you compare one against a string. If you
want a string, `"".join(sorted(s))`.

---

## 8. In the interview

### How it gets asked

- *"Are these two strings anagrams?"* — LeetCode 242, the warm-up. Then, almost always, *"can you do
  it faster than sorting?"*
- *"Group these words into anagram groups."* — LeetCode 49, and the real question. It is about using a
  canonical form as a dictionary key.
- *"Find all anagrams of p inside s."* — LeetCode 438, which is this plus a sliding window from
  [day 033](../day-033-window-with-a-map/README.md).
- *"Given a list of words, find any two that are anagrams of each other."* — the version that tempts
  people into a nested loop. The dictionary makes it one pass.

### What to say out loud, in the first ninety seconds

1. **Ask the contract questions.** *"Does case matter? Should I ignore spaces and punctuation? Can I
   assume lowercase English letters, or arbitrary Unicode?"* The last one decides whether the
   26-element array is available.
2. **Name the idea before either solution.** *"The core idea is a canonical form — some
   representation that's identical for all anagrams and different for anything else. Then the whole
   problem is comparing, or grouping by, that form."*
3. **Give the simple one first.** *"The simplest canonical form is the letters in sorted order.
   `sorted(a) == sorted(b)`, one line, O(k log k)."*
4. **Then improve it, unprompted.** *"But I can do better. Counting the letters is also a canonical
   form, and counting is O(k) instead of O(k log k). Two counts, compare them — or one count,
   incremented for the first string and decremented for the second."*
5. **Mention the free check.** *"And the length check first, which costs nothing and rejects a whole
   class of inputs immediately."*
6. **For grouping, say the key insight explicitly.** *"For grouping, the canonical form becomes a
   dictionary key. One pass, each word appended to its group. That turns what looks like a pairwise
   comparison problem — O(n²·k) — into a single pass."*
7. **Say which you would ship, and why.** *"I'd write the sorted version for word-length strings
   because it's one obviously-correct line, and switch to counting for long strings or if you want
   better than O(k log k)."*

### The follow-ups

**"Can you do better than sorting?"**
Yes — count instead. Sorting is `O(k log k)` because it establishes a total order on the characters,
which is strictly more information than I need; I only need how many of each. Counting is one pass,
`O(k)`, and for a fixed alphabet the space is constant. The neat version uses a single array: add one
for each character of the first string, subtract one for each character of the second, and return
false the moment any entry goes negative. That early exit is only correct because I checked the
lengths are equal first — with equal lengths, if nothing ever goes negative then nothing can be left
positive either, so I do not need a final scan. Without the length check, `"aab"` and `"ab"` would
wrongly come back as anagrams.

**"How would you group a million words?"**
The same one pass, and the constant factors start to matter. I would use the 26-tuple count key rather
than the sorted string, since it is `O(k)` per word and the tuple hashes in constant time. Memory is
the real question: a million words at 20 characters is roughly 20 MB of text, plus a key per word and
the group lists — comfortably a single machine, so I would not distribute it. If it genuinely did not
fit, this parallelises perfectly: the canonical key is a pure function of the word, so I can shard by
`hash(key) % N`, have each machine group its own shard, and concatenate the results with no merging
at all, since every anagram of a word produces the same key and therefore lands on the same machine.
That is a map-reduce with a trivial reduce.

**"What if the strings are Unicode, or contain spaces and capitals?"**
The sorted version keeps working unchanged, which is a real argument in its favour. The 26-element
array does not, and worse, it fails silently rather than raising, because `ord(ch) - ord('a')` for a
capital letter is a negative number and negative indices are legal in Python — so a capital `L` gets
counted into slot 5 with no error at all. For Unicode I would use a `Counter`, which handles any
character, and normalise first with `unicodedata.normalize`, because the same visible character can
have more than one encoding and those would count as different keys. For phrase anagrams I would
lower-case and filter to letters before doing anything else, and I would ask which of those the
problem wants rather than assuming.

**"Now find all the anagrams of `p` inside `s`."**
That is the sliding window version. I keep a count of `p`, and a count of the current window of `s`
which has the same length as `p`. If the two counts match, the window's start index is an answer. Then
I slide: increment the character entering on the right, decrement the one leaving on the left, and
compare again. Recomputing the whole window count each time would be `O(n·k)`; updating two entries
per step makes it `O(n)`, with `O(1)` space for a fixed alphabet. The detail worth mentioning is that
comparing two 26-entry counts on every step is technically constant but not free, so a common
refinement tracks a single "number of letters currently matching" counter and updates it as the two
edges move — which makes the per-step work genuinely `O(1)`.

### A model answer

> "First, a couple of contract questions. Does case matter — is `Listen` an anagram of `Silent`?
> Should I ignore spaces and punctuation? And can I assume lowercase English letters, or could this
> be arbitrary Unicode?
>
> ...Lowercase English, case-sensitive. Good.
>
> The idea underneath this problem is a canonical form: some representation of a string that is
> identical for every anagram of it and different for anything else. Once I have one, 'are these
> anagrams' is just comparing two canonical forms, and 'group these words' is putting them in a
> dictionary keyed by that form.
>
> The simplest canonical form is the letters in sorted order, so `sorted(a) == sorted(b)`. That is one
> line, correct for any input including Unicode, and it is `O(k log k)`.
>
> I can do better, because sorting produces a total ordering and I only need multiplicities. Counting
> the letters is also a canonical form and it is `O(k)`:
>
> ```python
> def is_anagram(a: str, b: str) -> bool:
>     if len(a) != len(b):
>         return False
>     counts = [0] * 26
>     for ch in a:
>         counts[ord(ch) - ord("a")] += 1
>     for ch in b:
>         index = ord(ch) - ord("a")
>         counts[index] -= 1
>         if counts[index] < 0:
>             return False
>     return True
> ```
>
> The length check first is free and rejects a whole class of inputs. The second loop subtracts rather
> than building a second count, and bails the moment an entry goes negative, which means `b` has a
> letter more often than `a` does. And I want to point out that the early exit is only valid *because*
> the lengths are equal — with equal lengths, if nothing goes negative then nothing can be left
> positive either, so there is no final scan. Drop the length check and `aab` versus `ab` wrongly
> returns true.
>
> For grouping, the same canonical form becomes a dictionary key:
>
> ```python
> groups = defaultdict(list)
> for word in words:
>     groups["".join(sorted(word))].append(word)
> return list(groups.values())
> ```
>
> The important thing there is that there is no comparison between words at all. The obvious approach
> would test every pair, which is `O(n²·k)` — a hundred million comparisons at ten thousand words —
> and keying a dictionary makes it a single pass. I have to join the sorted characters into a string
> because a list is not hashable and cannot be a key; with the counting version the key would be a
> 26-element tuple for the same reason.
>
> On which to ship: I actually measured this, and for word-length strings the sorted version is no
> slower, because `sorted` is compiled C while the counting loop is interpreted. The asymptotic win
> only shows up somewhere around a thousand characters. So I would write the sorted one-liner by
> default, and switch to counting for long strings or if you specifically want better than
> `O(k log k)`."

---

## 9. Recall card

- **Anagram = same multiset of characters.** Find a **canonical form**: sorted letters, or letter
  counts.
- **`sorted(a) == sorted(b)`** is `O(k log k)`; **counting** is `O(k)`. Give both, then say which you
  would ship.
- **Length check first** — free, and it is what makes the single-array subtract-and-bail version
  correct.
- **Grouping = canonical form as a dictionary key**, one pass. Keys must be hashable:
  `"".join(sorted(w))` or `tuple(counts)`.
- **A set is the wrong structure** — it loses multiplicities, so `aacc` and `ccac` compare equal.
