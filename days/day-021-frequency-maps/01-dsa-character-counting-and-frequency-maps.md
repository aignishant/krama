---
day: 21
track: dsa
title: "Character counting and frequency maps"
phase: "Strings"
status: written
---

# Day 021 · DSA — Character counting and frequency maps

**After today you can:** You reach for a counter dictionary the moment a problem says how many times.

**The interviewer asks it as:** *Find the first non-repeating character in a string.*

---

## 1. What this is, and why they ask it

A **frequency map** is a dictionary from each distinct thing to how many times it appeared. Walk the
input once, adding one to the right entry each time, and afterwards you can answer *how many of
each?* instantly instead of re-scanning.

That is the whole idea, and it is worth an entire day because of how often it is the answer. Any
question containing the words **how many times**, **most common**, **appears once**, **duplicate**,
**can we make X from Y**, or **do these contain the same letters** is a frequency-map question, and
recognising that in five seconds is a large fraction of what interviewers are measuring.

The specific question today — the first non-repeating character — is asked constantly, at Amazon and
Microsoft especially, because it has a small trap in it. The obvious answer is to check each
character against the rest of the string, which is `O(n²)`. The good answer is two passes with a
counter, which is `O(n)`. And the interesting part is *why two passes are unavoidable*: you cannot
know a character is unique until you have seen the entire string, because the second copy might be
the very last character. Candidates who try to force it into one pass are answering a question that
has no answer, and saying that clearly earns more than the code does.

This also opens the door to the whole hashing phase from
[day 060](../day-060-hash-tables/README.md), and it is the tool behind anagrams
tomorrow and sliding windows on [day 033](../day-033-window-with-a-map/README.md).

---

## 2. The story

Bhaskar has been a conductor on the 27C for nine years. It runs from the depot to the market and
back, twelve times a day, and on a weekday he will take money from something like four hundred
people.

The thing that makes his job possible is the tray. It is a shallow metal box with a lid, divided
into six compartments, and each compartment holds one kind of coin — ones in the first, twos in the
second, fives, tens, and two bigger sections at the back for the notes. When somebody hands him a
five-rupee coin it goes into the fives, straight away, without him thinking about it. He does that
four hundred times a day and he does not look while he does it.

The first year, before he had the tray, he used the cloth pouch everyone starts with, and everything
went into the pouch together. At the end of the shift he would sit on the step of the bus at half
past nine at night and tip the whole thing out and sort it, and it took him twenty minutes and he
got it wrong about once a week. Now the sorting has already happened, all day, one coin at a time,
and at the end he only has to count what is already in each compartment. Four minutes.

The clerk at the depot asked him something odd last month. She was doing some kind of study and she
wanted to know which kinds of coin he had received exactly one of, all day.

Bhaskar's answer is the interesting part. He said he could tell her — but not until the day was
over. At two in the afternoon he might have exactly one twenty-rupee note in the tray, and it would
be perfectly true at that moment that he had received only one. But somebody could hand him a second
one at eight in the evening, and then the answer changes. There is no point in the day when he can
look into the tray and say *this one is the only one I will get*, because the day is not finished
with him yet.

So he does what she asked at the end of the shift, when everything has been through his hands, and
then it takes him about thirty seconds.

---

## 3. The idea in plain English

Bhaskar's tray is a frequency map. Each compartment is a key, the number of coins in it is the
value, and dropping a coin in is the one line of code you write in the loop.

### Building one

The idea is the same three ways; only the syntax differs.

**With a plain dictionary and `get`:**

```python
counts = {}
for ch in s:
    counts[ch] = counts.get(ch, 0) + 1
```

`counts.get(ch, 0)` returns the current count, or `0` if this character has never been seen. That
default is the whole trick — without it, the first time you touch a new key you get a `KeyError`, and
§7 shows it.

**With `defaultdict`:**

```python
from collections import defaultdict

counts = defaultdict(int)
for ch in s:
    counts[ch] += 1
```

`defaultdict(int)` creates a missing key with the value `int()`, which is `0`, the moment you touch
it. Cleaner to read, and you met it on [day 016](../day-016-2d-arrays/README.md).

**With `Counter`, which is what you would actually write:**

```python
from collections import Counter

counts = Counter(s)          # one line, does the whole loop
```

`Counter` is a dictionary subclass built for exactly this. It counts any iterable in one call, and
it never raises for a missing key — `counts["z"]` on a string with no `z` returns `0`, not an error.

**Which to use in an interview?** Write `Counter`, and be able to write the manual loop if asked.
Interviewers occasionally say *"without using Counter"* precisely to see whether you know what it is
doing.

### The other representation: a fixed-size array

When the alphabet is small and known — the 26 lowercase English letters — you can use a list of 26
integers instead of a dictionary, mapping each character to a position with `ord`.

```python
counts = [0] * 26
for ch in s:
    counts[ord(ch) - ord("a")] += 1
```

`ord(ch)` gives the character's numeric code — `ord("a")` is 97, `ord("b")` is 98. Subtracting
`ord("a")` turns `"a"` into 0, `"b"` into 1, and so on up to `"z"` as 25.

This is faster than a dictionary by a constant factor and uses fixed memory, and interviewers like
it because it shows you noticed the constraint. It is also **fragile**: it silently breaks on capital
letters, spaces, digits and anything non-English, and §7 shows exactly how silently. Use it only when
the problem promises lowercase English letters, and say so out loud when you do.

### Why the answer needs two passes

Here is Bhaskar at two in the afternoon, and it is the heart of today's question.

To find the first character that appears exactly once, you must:

1. **Pass one:** count every character. Now `counts` is complete.
2. **Pass two:** walk the string again from the start, and return the position of the first character
   whose count is 1.

You cannot merge these. Halfway through the string, a character you have seen once may be about to
appear again — you have no way to know until you reach the end. **Uniqueness is a property of the
whole string, so it cannot be decided from a prefix.** That is Bhaskar's twenty-rupee note.

Pass two must go in **string order**, not dictionary order, because the question asks for the
*first*. (Python dictionaries do happen to preserve insertion order, so iterating `counts` would in
fact give the same answer here — but relying on that is fragile reasoning, and walking the string is
clearer about what you mean.)

### Recognising the pattern

The tell-tale phrases, and what each one becomes:

| The problem says | You build | Then |
|---|---|---|
| "appears exactly once" | a count of every character | scan in order for a count of 1 |
| "most common" / "top k" | a count | `most_common(k)` |
| "can you build A from B" | a count of B | check every count in A is available |
| "same characters" | counts of both | compare the two dictionaries |
| "how many distinct" | a **set**, not a count | `len(set(s))` |
| "at most k distinct in a window" | a count, updated as the window moves | [day 033](../day-033-window-with-a-map/README.md) |

Note the fifth row. When you only care *whether* something appeared and not how often, a set is the
right structure and is cheaper. Reaching for a counter when a set will do is a small but real signal.

---

## 4. The picture

Building the map for `"loveleetcode"`, one character at a time:

```
   character:  l  o  v  e  l  e  e  t  c  o  d  e
               |  |  |  |  |  |  |  |  |  |  |  |
   after each step, the map holds:

   l -> {l:1}
   o -> {l:1, o:1}
   v -> {l:1, o:1, v:1}
   e -> {l:1, o:1, v:1, e:1}
   l -> {l:2, o:1, v:1, e:1}          <- l is no longer unique
   e -> {l:2, o:1, v:1, e:2}
   e -> {l:2, o:1, v:1, e:3}
   t -> {l:2, o:1, v:1, e:3, t:1}
   c -> {l:2, o:1, v:1, e:3, t:1, c:1}
   o -> {l:2, o:2, v:1, e:3, t:1, c:1} <- o is no longer unique
   d -> {l:2, o:2, v:1, e:3, t:1, c:1, d:1}
   e -> {l:2, o:2, v:1, e:4, t:1, c:1, d:1}
```

**What to notice:** `o` was unique for eight steps and then stopped being unique at step ten. Any
decision made before the end would have been wrong. That is why there are two passes.

Now pass two, walking the original string with the finished map:

```
   position:   0    1    2    3    4    5    6    7    8    9   10   11
   character:  l    o    v    e    l    e    e    t    c    o    d    e
   count:      2    2    1    4    2    4    4    1    1    2    1    4
               |    |    ^
               |    |    +--- first count of 1  ->  answer is position 2
               |    +-------- 2, keep going
               +------------- 2, keep going
```

**What to notice:** the answer is 2, not 7 — `t` also has a count of 1, but `v` comes first. Walking
in string order is what makes "first" mean the right thing.

The other representation, for lowercase-only input:

```
   index    0    1    2  ...   4  ...  11  ...  14  ...  19  ...  25
          +----+----+----+   +----+   +----+   +----+   +----+  +----+
   value  |  0 |  0 |  1 |   |  4 |   |  2 |   |  2 |   |  1 |  |  0 |
          +----+----+----+   +----+   +----+   +----+   +----+  +----+
            a    b    c        e       l        o        t        z

   position = ord(ch) - ord('a')
```

**What to notice:** there is one box for every possible letter, including the ones that never
appeared. That is the trade — fixed, predictable memory, and it only works when the alphabet is
fixed and known.

---

## 5. The code, built step by step

### The count, three ways

```python
counts = {}
for ch in s:
    counts[ch] = counts.get(ch, 0) + 1
```

The version to write if asked not to use the library. `get` with a default is the load-bearing part.

```python
from collections import defaultdict
counts = defaultdict(int)
for ch in s:
    counts[ch] += 1
```

Cleaner. One caution: a `defaultdict` **creates** the key when you read a missing one, so
`if counts[x] == 0` quietly inserts `x`. Use `x in counts` to test membership.

```python
from collections import Counter
counts = Counter(s)
```

What you write in practice. It works on any iterable — a string, a list, a generator.

### The second pass

```python
for i, ch in enumerate(s):
    if counts[ch] == 1:
        return i
return -1
```

`enumerate(s)` yields `(position, character)` pairs, which is exactly what "return the index" needs.
The `return -1` at the end is the contract for "there is no such character" — ask which sentinel the
interviewer wants; some versions of the problem want the character itself, or `None`.

### The two together

```python
def first_uniq_char(s: str) -> int:
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
```

Four lines, `O(n)`, and it is the complete answer to LeetCode 387.

### `Counter`'s useful extras

```python
c = Counter("hello world")
c.most_common(3)      # [('l', 3), ('o', 2), ('h', 1)]
c["z"]                # 0  — never a KeyError
Counter("aabbc") - Counter("abc")     # Counter({'a': 1, 'b': 1})
Counter("aab") == Counter("aba")      # True
```

`most_common(k)` returns the `k` highest counts, already sorted. Subtraction keeps only positive
counts, which makes "can I build A out of B?" a one-liner — that is LeetCode 383 below. And equality
compares the whole mapping, which is the entire anagram check on
[day 022](../day-022-anagrams/README.md).

### The fixed-array version, written safely

```python
def first_uniq_char_array(s: str) -> int:
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord("a")] += 1     # lowercase a-z ONLY
    for i, ch in enumerate(s):
        if counts[ord(ch) - ord("a")] == 1:
            return i
    return -1
```

Faster by a constant factor, `O(1)` space by any sensible reading, and correct **only** if the input
really is lowercase English. Say that constraint out loud before you use it.

### The complete solutions

```python
from collections import Counter, defaultdict


def count_chars_manual(s: str) -> dict[str, int]:
    """The version to write when asked not to use Counter."""
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1   # get with a default, never counts[ch]
    return counts


def count_chars_defaultdict(s: str) -> dict[str, int]:
    """Same thing. defaultdict(int) supplies 0 for a missing key."""
    counts: defaultdict[str, int] = defaultdict(int)
    for ch in s:
        counts[ch] += 1
    return dict(counts)


def first_uniq_char(s: str) -> int:
    """LeetCode 387. Index of the first character appearing exactly once, else -1.

    Two passes: you cannot know a character is unique until the string has ended.
    """
    counts = Counter(s)
    for i, ch in enumerate(s):               # string order, because "first" means first
        if counts[ch] == 1:
            return i
    return -1


def first_uniq_char_array(s: str) -> int:
    """The same, using 26 slots instead of a dictionary. Lowercase a-z only."""
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord("a")] += 1
    for i, ch in enumerate(s):
        if counts[ord(ch) - ord("a")] == 1:
            return i
    return -1


def can_construct(note: str, magazine: str) -> bool:
    """LeetCode 383. Can `note` be built from the letters of `magazine`?"""
    return not (Counter(note) - Counter(magazine))   # empty means nothing was missing


def most_common_char(s: str) -> str | None:
    """The most frequent character. Ties broken by first appearance, as Counter does."""
    if not s:
        return None
    return Counter(s).most_common(1)[0][0]


def count_distinct(s: str) -> int:
    """When you only care WHETHER, not HOW MANY — a set is cheaper than a counter."""
    return len(set(s))


if __name__ == "__main__":
    print(count_chars_manual("hello"))          # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

    print(first_uniq_char("leetcode"))          # 0
    print(first_uniq_char("loveleetcode"))      # 2
    print(first_uniq_char("aabb"))              # -1
    print(first_uniq_char(""))                  # -1
    print(first_uniq_char("z"))                 # 0

    print(first_uniq_char_array("loveleetcode"))  # 2

    print(can_construct("aa", "aab"))           # True
    print(can_construct("aa", "ab"))            # False

    print(most_common_char("hello world"))      # l
    print(count_distinct("hello"))              # 4
```

---

## 6. What it costs

### `first_uniq_char`

**Pass one.** `Counter(s)` visits each of the `n` characters once. Each visit is one dictionary
lookup and one increment, both `O(1)` on average — that is the promise of a hash table, and
[day 060](../day-060-hash-tables/README.md) explains why. So pass one is `n` turns
of constant work.

**Pass two.** At most `n` characters, one dictionary lookup each. Another `n` turns of constant work.

**Total: `2n` turns, so O(n) time.** Two passes over the data is still linear — a common
misunderstanding is that two passes means `O(n²)`, and being clear that it does not is worth a mark.

**Space.** The dictionary holds one entry per **distinct** character. Call that `k`:

- For arbitrary text, `k ≤ n`, so **O(k)**, and `O(n)` in the worst case where every character
  differs.
- For lowercase English, `k ≤ 26` no matter how long the string is. That is a constant, so it is
  **O(1) space** — and saying "O(1) because the alphabet is bounded at 26" is exactly the sentence
  interviewers want here.
- For full Unicode, `k` can be over a million in principle, though never more than `n` in practice.

### Against the naive version

```python
for i, ch in enumerate(s):
    if s.count(ch) == 1:      # scans the whole string, every time
        return i
```

`s.count(ch)` is `O(n)`, done up to `n` times: **O(n²)**. At `n = 100,000` that is 10 billion
character comparisons against 200,000 for the counter version — fifty thousand times more work.
It is also two lines shorter, which is why it gets written.

### Dictionary against array of 26

Both are `O(n)` time. The array wins on the constant factor: an integer subtraction and a direct
index, against hashing the character and probing a table. In CPython the gap is usually somewhere
around two to three times. It also uses a fixed 26 slots regardless of input.

The dictionary wins on generality — it handles any character with no changes, and it stores only
what actually appeared. **Say both, then pick the dictionary unless the problem states the alphabet.**

### The number to have ready

> Counting is one pass, `O(n)`. Finding the first unique character is two passes, still `O(n)`. The
> naive "count each character against the whole string" version is `O(n²)` — 10 billion operations at
> a hundred thousand characters, against 200,000.

---

## 7. The traps

### The real error: touching a key that is not there

```python
counts = {}
for ch in "hello":
    counts[ch] += 1
```

```
Traceback (most recent call last):
  File "t.py", line 3, in <module>
    counts[ch] += 1
    ~~~~~~^^^^
KeyError: 'h'
```

`counts[ch] += 1` reads before it writes, and on the first `h` there is nothing to read. Three fixes,
all fine: `counts.get(ch, 0) + 1`, a `defaultdict(int)`, or a `Counter`.

### The near-miss that never raises: `ord` with the wrong alphabet

```python
def counts26(s):
    arr = [0] * 26
    for ch in s:
        arr[ord(ch) - ord("a")] += 1
    return arr

print(counts26("Hello"))
```

Predict the output. You may expect an `IndexError`. Here is what actually happens:

```
[0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

**No error.** `ord("H")` is 72 and `ord("a")` is 97, so `72 - 97` is `-25` — and a negative index is
perfectly legal in Python, counting back from the end. Position `-25` of a 26-element list is
position 1, so the capital `H` was silently counted as a `b`. Look at the output: index 1 has a
count of 1 and index 7, which is where `h` belongs, has 0.

This is the negative-index trap from [day 016](../day-016-2d-arrays/README.md) in a new costume, and
it is worse here because the answer looks completely plausible. **Whenever you use `ord(ch) -
ord("a")`, state the assumption out loud and, in real code, normalise first with `s.lower()` or guard
with `if ch.isalpha()`.**

### The near-miss: trying to do it in one pass

```python
def first_uniq_char(s):
    seen = set()
    for i, ch in enumerate(s):
        if ch not in seen:
            seen.add(ch)
            return i          # wrong: this is just the first character
    return -1
```

Every attempt to answer this in one pass has the same flaw. At position `i` you simply do not know
whether the character repeats later. There is no clever bookkeeping that fixes it, because the
information does not exist yet. **The right response in an interview is to say so** — *"this needs two
passes, because uniqueness is a property of the whole string"* — rather than to search for a
one-pass version that cannot exist.

(The related problem that *does* work in one pass is *"return the first character that has not
repeated so far, after each new character"* — a stream question, which needs a queue as well as a
counter. If an interviewer pushes towards one pass, this is probably the question they are steering
towards.)

### The real error: changing a dictionary while looping over it

```python
d = {"a": 1, "b": 2, "c": 3}
for k in d:
    if d[k] == 2:
        del d[k]
```

```
RuntimeError: dictionary changed size during iteration
```

Same family as deleting from a list while iterating on
[day 015](../day-015-the-write-pointer/README.md), and here Python catches it rather than silently
skipping. Loop over a copy — `for k in list(d)` — or build a new dictionary with a comprehension.

### The near-miss: `defaultdict` inserting on read

```python
from collections import defaultdict
counts = defaultdict(int)
counts["a"] += 1
if counts["z"] == 0:      # this INSERTS 'z' with value 0
    pass
print(dict(counts))       # {'a': 1, 'z': 0}
```

Reading a missing key from a `defaultdict` creates it. Usually harmless, occasionally not — a later
`len(counts)` or a loop over the keys now sees a character that never appeared. Use `"z" in counts`
to test membership, or use `Counter`, which returns 0 for a missing key **without** inserting it.

### The near-miss: counting when you meant to check membership

```python
counts = Counter(s)
if counts[ch] > 0: ...      # you only wanted to know IF
```

If the question is "does this appear at all", a set is the right structure: `set(s)` builds faster,
uses less memory, and says what you mean. Using a counter for a membership test works and reads as
though you had not decided what you needed.

---

## 8. In the interview

### How it gets asked

- *"Find the first non-repeating character in a string."* — LeetCode 387, the direct version. Ask
  whether they want the index or the character.
- *"What's the most frequent character / word?"* — `most_common`, plus a conversation about ties.
- *"Can you build this string from the letters in that one?"* — LeetCode 383, the counter-subtraction
  question.
- *"Find the first non-repeating character in a stream."* — the harder relative, needing a counter
  **and** a queue. If they say "stream", that is the signal.

### What to say out loud, in the first ninety seconds

1. **Pin the contract.** *"Should I return the index or the character? What do I return if every
   character repeats — minus one, or None? And can I assume lowercase English letters, or arbitrary
   Unicode?"* That third question decides dictionary versus array of 26.
2. **Name the brute force and its cost.** *"The obvious version checks each character against the
   whole string, which is O(n²)."*
3. **State the structure.** *"I'll build a frequency map in one pass — character to count — then walk
   the string again and return the first character whose count is one."*
4. **Say why two passes, before being asked.** *"It has to be two passes. A character that has
   appeared once so far might appear again at the very last position, so uniqueness can't be decided
   from a prefix."* This is the sentence the question exists to elicit.
5. **Say why pass two walks the string.** *"The second pass goes over the string, not the dictionary,
   because the question asks for the first one in the original order."*
6. **Give the cost precisely.** *"Two passes, so O(n) time — two passes is still linear. Space is one
   entry per distinct character; if the alphabet is the 26 lowercase letters that's bounded, so
   O(1)."*
7. **Offer the alternative representation.** *"If it's guaranteed lowercase I'd use a 26-element
   array instead of a dictionary — same complexity, a smaller constant."*

### The follow-ups

**"Can you do it in one pass?"**
Not for this problem, and I think the honest answer is more useful than an attempt. At any position
in the string, a character I have seen exactly once might still appear again later — the second copy
could be the final character — so uniqueness genuinely is not decidable from a prefix, and no
bookkeeping fixes that because the information does not exist yet. What I *can* do is one pass to
build the counts and one pass over the counts rather than the string, but that is still two passes
and it loses the ordering unless I rely on dictionaries preserving insertion order, which I would
rather not lean on. If the question is instead about a **stream** — report the first non-repeating
character seen *so far*, after each new character — that does work incrementally, and I would keep a
counter plus a queue of candidates, popping from the front of the queue whenever its count rises
above one.

**"What if the string is huge and can't fit in memory?"**
The counter still works, because it is bounded by the number of *distinct* characters rather than the
length — for text that is at most a few thousand entries however many gigabytes the file is. So pass
one streams the file and builds the counts in constant memory. The problem is pass two, which needs
the original order again; I would either re-read the file, which is fine because a sequential read is
cheap, or record the first position of each character during pass one and then take the minimum
position among characters with count 1, which turns pass two into a scan of the small dictionary
rather than of the data. The second option is one pass over the data, which matters when the data is
on a network or a tape rather than a disk.

**"Now find the first non-repeating character in a stream."**
Counter plus a queue. Maintain the frequency map as before, and a queue holding candidates in arrival
order. For each new character: increment its count, and push it onto the queue. Then, before
answering, pop from the front of the queue while the front character's count is above one — those can
never be the answer again. Whatever is at the front is the current answer, or the stream has no
unique character if the queue is empty. Each character is pushed once and popped at most once, so it
is `O(1)` amortised per character and `O(k)` space for the alphabet. That is the genuine one-pass
version, and it works only because the *question* changed to allow an answer that evolves.

**"How would you handle Unicode, or count words instead of characters?"**
Nothing changes structurally — a dictionary keyed by whatever the unit is. The array-of-26 trick
disappears, which is the practical difference: `ord(ch) - ord('a')` is meaningless outside a known
alphabet and, as I showed, fails silently rather than loudly because negative indices are legal. For
Unicode I would also normalise first, because the same visible character can have more than one
encoding — `é` as one code point or as `e` plus a combining accent — and those would count as
different keys. For words, I would split and count the words, and decide explicitly whether case and
punctuation matter, because "The" and "the" being one word or two is a product decision, not a
technical one.

### A model answer

> "First, two clarifications: do you want the index or the character itself, and what should I return
> if there isn't one — minus one, or None? And can I assume the string is lowercase English letters,
> or should I handle arbitrary Unicode?
>
> ...Index, minus one, arbitrary characters. Good, I'll use a dictionary rather than a fixed array.
>
> The brute force is to take each character and count its occurrences in the whole string, returning
> the first with a count of one. That's correct and O(n²), since counting is a full scan done up to n
> times.
>
> Instead I'll count once. One pass over the string building a map from character to how many times
> it appeared. Then a second pass over the string, in order, returning the index of the first
> character whose count is one.
>
> ```python
> def first_uniq_char(s: str) -> int:
>     counts = Counter(s)
>     for i, ch in enumerate(s):
>         if counts[ch] == 1:
>             return i
>     return -1
> ```
>
> Two things worth calling out. First, this genuinely has to be two passes. A character that has
> appeared once so far might appear again at the very last position, so I can't decide uniqueness
> from a prefix — the information doesn't exist until the string ends. I mention that because the
> instinct is to look for a one-pass version, and there isn't one for this phrasing.
>
> Second, the second pass walks the *string*, not the dictionary, because the question asks for the
> first in the original order. Python dictionaries do preserve insertion order so iterating the map
> would happen to give the same answer, but I'd rather the code say what I mean than rely on that.
>
> Cost: two passes over n characters with O(1) dictionary operations, so O(n) time — and two passes
> is still linear, not quadratic. Space is one entry per distinct character. For arbitrary input
> that's O(k) where k is the alphabet size, bounded by n; if you'd told me it was lowercase English,
> k is at most 26 and it's O(1), and I'd have used a 26-element array indexed by `ord(ch) - ord('a')`
> for a smaller constant factor.
>
> On `loveleetcode` the counts are l:2, o:2, v:1, e:4, t:1, c:1, d:1, and walking the string gives
> position 2 for the `v` — not position 7 for the `t`, even though both are unique, because `v` comes
> first.
>
> Edge cases: empty string returns minus one because the second loop never runs; a single character
> returns 0; and a string where everything repeats falls through to minus one."

---

## 9. Recall card

- **"How many times", "most common", "appears once", "duplicate" → build a frequency map.**
- **`Counter(s)`** in practice; `counts.get(ch, 0) + 1` or `defaultdict(int)` when asked to do it by
  hand. Plain `counts[ch] += 1` is a `KeyError`.
- **First-unique needs two passes.** Uniqueness is a property of the whole string. Two passes is
  still `O(n)`.
- **Pass two walks the string, not the map**, because "first" means first in the input.
- **`ord(ch) - ord("a")` is `O(1)` space and silently wrong on anything but lowercase a–z** — negative
  indices do not raise.
