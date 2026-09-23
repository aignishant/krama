---
day: 64
track: dsa
title: "Grouping: the key-design skill"
phase: "Hashing: maps and sets"
status: written
---

# Day 064 · DSA — Grouping: the key-design skill

**After today you can:** You can invent the right dictionary key for a grouping problem, which is the whole trick.

**The interviewer asks it as:** *Group these strings into anagram groups. What is your key?*

---

## 1. What this is, and why they ask it

**Grouping** is putting every item into a pile, where the pile is chosen by something you compute
from the item. In code it is a dictionary whose values are lists: `key -> [items with that key]`. The
mechanics take four lines and you will have them in ten minutes.

The mechanics are not the lesson. **The lesson is choosing the key**, and that is a genuine skill
with a genuine failure mode in both directions. A key that captures too little merges things that do
not belong together. A key that captures too much splits things that do. The right key is the answer
to one question — *what exactly makes two of these items belong in the same pile?* — computed and
nothing more.

They ask it because the key is where the thinking is, and it is impossible to fake. Group Anagrams
is the standard vehicle, and it is asked at almost every product company, but the same question comes
disguised a dozen other ways: group shifted strings, group by diagonal in a matrix, validate a
Sudoku, find duplicate files by content, bucket events by hour. In every one of them the code is the
same four lines and the interview is entirely in the one line that computes the key. An interviewer
watching you will say almost nothing until you write that line, and then ask "why that key?".

---

## 2. The story

The wedding at the hall in Basavanagudi finished at about four, and by half past four the problem
everyone had been quietly not thinking about was sitting in the middle of the floor.

Six households had lent their vessels. Six hundred-odd of them — steel plates, tumblers, the big
serving dishes, four enormous pots. All used, all washed, and all stacked in one heap by two tired
boys who had no instructions.

Lakshmi, whose sister's daughter had just been married, sat down on a chair in front of the heap with
two nieces and said they were not leaving until it was done.

The first niece started by size. Small tumblers here, medium plates there, the big things at the
end. Twenty minutes in, Lakshmi stopped her. Every one of the six houses owns small tumblers. Sorting
by size had made four beautiful piles, and not one of them belonged to anybody.

The second niece tried by how worn they looked, which was worse.

What actually works is a thing everybody in that room already knew and nobody had said out loud.
Every household scratches a mark on the underside of its vessels, because this happens four or five
times a year. A letter, or two, or a little symbol. You turn the vessel over and it tells you whose
it is.

So that is what they did. Pick one up, turn it over, read the mark, put it on that mark's pile. If
the mark was one they had not seen yet, they started a new pile for it and carried on. No thinking
after the first minute — just turn, read, drop.

Six hundred vessels, three of them, a little over an hour.

The one real problem came near the end. Two of the six households both use a single letter S —
Srinivas and Shankar, who live on the same road and had never noticed. There was one pile of about
ninety vessels belonging to two houses, and no way to split it by looking. The two families had to
sit together and go through it by memory, item by item, which took another forty minutes and involved
some disagreement about a rice dish.

Lakshmi's line about it afterwards was that the mark has to be enough to tell you apart from
everybody else, and no more than that. Srinivas has since started scratching SRN.

---

## 3. The idea in plain English

The heap is your input. Each pile is a **group**. The mark scratched underneath is the **key**, and
the act of turning the vessel over to read it is **computing the key from the item**.

Three things from that afternoon, and they are the three things this lesson is about.

**One: the piles are a dictionary of lists.** Key to a list of everything with that key. New key means
a new empty pile, exactly like Shobha's new dish on the whiteboard in
[day 063](../day-063-counting-with-dicts/README.md).

**Two: sorting by size was not a bad *method*, it was a bad *key*.** The loop was fine. The piles
were tidy. The key answered the wrong question. This is the failure that actually happens in
interviews — the code is correct and the answer is wrong.

**Three: a key must capture exactly what makes two items the same, and nothing else.** The single
letter S captured too little, so two households merged. If they had scratched the date of purchase as
well, the key would have captured too much, and one household's vessels would have split into nine
piles.

### The four lines

```python
from collections import defaultdict

groups: dict[str, list[str]] = defaultdict(list)
for word in words:
    groups[key_of(word)].append(word)
```

`defaultdict(list)` is a dictionary that creates an empty list the first time you touch a key, so
there is no "does this pile exist yet" branch. That is the new-pile moment, handled.

Written without the import, in case an interviewer asks:

```python
groups: dict[str, list[str]] = {}
for word in words:
    groups.setdefault(key_of(word), []).append(word)
```

`setdefault(k, [])` means: give me the list at `k`, putting an empty list there first if there is
none. It works, and it has a small cost worth knowing about — the `[]` is constructed on *every*
call, even when the key already exists, and then thrown away. For a million items that is a million
wasted list allocations. Use `defaultdict` when you have the import.

### Now: what goes in `key_of`?

This is the whole subject. Here is the recipe, and it is one sentence.

> **Write down, in words, what makes two items belong in the same pile. Then compute exactly that.**

Say the sentence before you write the line. If you cannot say the sentence, you are not ready to
write the line.

### Worked keys

**Anagrams.** Two words belong together when they use the same letters the same number of times.
Order does not matter. So the key must throw away order and keep counts.

```python
def key_of(word: str) -> str:
    return "".join(sorted(word))      # "eat" -> "aet", "tea" -> "aet"
```

Sorting the letters destroys exactly the thing that should not matter — the order — and keeps exactly
the thing that should — which letters, how many. That sentence is the answer to "why that key?".

There is a second key for the same question:

```python
def key_of(word: str) -> tuple[int, ...]:
    counts = [0] * 26
    for character in word:
        counts[ord(character) - ord("a")] += 1
    return tuple(counts)              # "eat" -> (1,0,0,0,1,...,1,...)
```

A tuple of 26 counts. Same grouping, different cost, and it must be a `tuple` and not a `list`
because dictionary keys must be hashable. Which one to use is a real trade and §6 has the numbers.

**Shifted strings.** `"abc"`, `"bcd"` and `"xyz"` are all the same shape — each letter one further on
than the last. Two words belong together when the *gaps between consecutive letters* match. So the
key is the gaps, not the letters.

```python
def shift_key(word: str) -> tuple[int, ...]:
    return tuple((ord(b) - ord(a)) % 26 for a, b in zip(word, word[1:]))
```

The `% 26` is the part people miss: `"az"` has a gap of 25 and `"za"` has a gap of -25, which is 1
after wrapping — and `"za"` really is a shift of `"ab"`.

**Cells of a Sudoku box.** Two cells are in the same three-by-three box when their row divided by
three and column divided by three match.

```python
box_key = (row // 3, column // 3)
```

**Diagonals of a matrix.** Every cell on the same top-left-to-bottom-right diagonal has the same
`row - column`. Every anti-diagonal has the same `row + column` — which you met in
[day 016](../day-016-2d-arrays/README.md).

```python
diagonal_key = row - column
anti_key = row + column
```

**Files with identical contents.** Two files belong together when their bytes match. Comparing every
pair is O(n²) reads. The key is a digest of the contents.

```python
key = hashlib.sha256(data).hexdigest()
```

### The two failure modes, named

| Failure | What it looks like | Vessels |
|---|---|---|
| **Key too coarse** — captures too little | Groups merge that should be separate | Both households marked S |
| **Key too fine** — captures too much | One real group splits into many | Marking the purchase date too |

The test for coarse: *can I construct two items with the same key that should not be together?* The
test for fine: *can I construct two items that should be together and have different keys?* Run both
tests out loud on your key before you write the loop. It takes fifteen seconds and it is the entire
question.

### The key must be hashable

Same rule as [day 062](../day-062-sets/README.md). A `list` cannot be a key:

```python
>>> groups = defaultdict(list)
>>> groups[["a"]].append(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

So the count key is a `tuple(counts)`, never `counts`. For a group where order genuinely does not
matter, `frozenset` is the hashable set.

---

## 4. The picture

Grouping six words by the sorted-letters key. Left is the input, middle is the computed key, right is
the pile it lands on.

```
  word      key = sorted letters        piles as they fill
 ------    ---------------------       ---------------------------------
 "eat"     -> "aet"                    aet: [eat]
 "tea"     -> "aet"                    aet: [eat, tea]
 "tan"     -> "ant"                    aet: [eat, tea]   ant: [tan]
 "ate"     -> "aet"                    aet: [eat, tea, ate]   ant: [tan]
 "nat"     -> "ant"                    aet: [...]  ant: [tan, nat]
 "bat"     -> "abt"                    aet: [...]  ant: [...]  abt: [bat]
```

What to notice: the key column is the only place any thinking happens. Once a word has a key, the
rest is `groups[key].append(word)` and cannot go wrong.

Now the two failure modes drawn on the same six words. First, a key that is too coarse — group by
word length:

```
 key = len(word)
   3: [eat, tea, tan, ate, nat, bat]     <- one pile, everything in it
```

Every word has length three, so the key tells you nothing. Two things that should be apart are
together. Second, a key that is too fine — group by the word itself:

```
 key = word
   eat: [eat]   tea: [tea]   tan: [tan]   ate: [ate]   nat: [nat]   bat: [bat]
```

Six piles of one. Two things that should be together are apart. **The right key sits between these
two, and finding where is the problem.**

And the box key on a nine-by-nine grid, so you can see why integer division works:

```
 column ->  0  1  2 | 3  4  5 | 6  7  8
 row 0     (0,0)... | (0,1)...| (0,2)...
 row 1     (0,0)    | (0,1)   | (0,2)
 row 2     (0,0)    | (0,1)   | (0,2)
 ---------+---------+---------+---------
 row 3     (1,0)    | (1,1)   | (1,2)
 row 4     (1,0)    | (1,1)   | (1,2)
 row 5     (1,0)    | (1,1)   | (1,2)
 ---------+---------+---------+---------
 row 6     (2,0)    | (2,1)   | (2,2)
 row 7     (2,0)    | (2,1)   | (2,2)
 row 8     (2,0)    | (2,1)   | (2,2)
```

Rows 0, 1 and 2 all give `row // 3 == 0`. That is the whole trick, and it is worth drawing once
because the same `// k` key groups anything into fixed-size blocks — timestamps into hours, ids into
shards, scores into bands.

---

## 5. The code, built step by step

### Step 1 — the grouping loop, with the key left blank

```python
from collections import defaultdict

def group_by(items: list[str], key_of) -> list[list[str]]:
    groups: dict[object, list[str]] = defaultdict(list)
    for item in items:
        groups[key_of(item)].append(item)
    return list(groups.values())
```

Write this first, every time. It is the same four lines for every grouping problem there is, and
separating it from the key makes the interview conversation land on the right place.

### Step 2 — the anagram key, by sorting

```python
def anagram_key(word: str) -> str:
    return "".join(sorted(word))
```

`sorted("eat")` gives `['a', 'e', 't']` and `"".join` turns it back into `"aet"`. Say what it is
doing as you write it: *sorting destroys the order, which is the thing that must not matter, and
keeps the multiset of letters, which is the thing that must.*

### Step 3 — the anagram key, by counting

```python
def anagram_key_counts(word: str) -> tuple[int, ...]:
    counts = [0] * 26
    for character in word:
        counts[ord(character) - ord("a")] += 1
    return tuple(counts)
```

`ord("a")` is 97, so `ord("c") - ord("a")` is 2, which is the slot for `c`. This avoids the sort, so
it is O(k) per word rather than O(k log k) — and it hard-codes the assumption that the input is
twenty-six lowercase English letters. **Say that assumption out loud.** If the interviewer says
"Unicode", this key is dead and the sorted key survives.

### Step 4 — put them together

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())
```

Five lines, and the fourth is the only one that required thought.

### Step 5 — the general helper, and three more keys

The value of separating the key out is that the same helper solves five problems.

```python
def group_shifted(words: list[str]) -> list[list[str]]:
    def key(word: str) -> tuple[int, ...]:
        return tuple((ord(b) - ord(a)) % 26 for a, b in zip(word, word[1:]))
    return group_by(words, key)
```

Note what happens to a one-character word: `zip("a", "")` is empty, so the key is `()`, and all
single characters land in one group. That is correct — every single letter is a shift of every other
— and it is the edge case an interviewer will ask about.

### The complete solution

```python
from collections import defaultdict
from typing import Callable, Hashable, TypeVar

T = TypeVar("T")


def group_by(items: list[T], key_of: Callable[[T], Hashable]) -> list[list[T]]:
    """Split items into groups by a computed key. The four lines every
    grouping problem shares — all the thinking is in `key_of`."""
    groups: dict[Hashable, list[T]] = defaultdict(list)
    for item in items:
        groups[key_of(item)].append(item)
    return list(groups.values())


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Words using the same letters the same number of times, grouped.

    The key throws away order (which must not matter) and keeps the letter
    multiset (which must). O(n * k log k) for n words of length k.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


def group_anagrams_counting(words: list[str]) -> list[list[str]]:
    """Same grouping in O(n * k), assuming lowercase a-z only."""
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in words:
        counts = [0] * 26
        for character in word:
            counts[ord(character) - ord("a")] += 1
        groups[tuple(counts)].append(word)
    return list(groups.values())


def group_shifted_strings(words: list[str]) -> list[list[str]]:
    """"abc", "bcd" and "xyz" are one group: the gaps between letters match.
    The % 26 handles wrap-around, so "za" groups with "ab"."""
    def key(word: str) -> tuple[int, ...]:
        return tuple((ord(b) - ord(a)) % 26 for a, b in zip(word, word[1:]))
    return group_by(words, key)


def diagonal_groups(matrix: list[list[int]]) -> dict[int, list[int]]:
    """Every cell on one top-left-to-bottom-right diagonal shares row - column."""
    groups: dict[int, list[int]] = defaultdict(list)
    for row, values in enumerate(matrix):
        for column, value in enumerate(values):
            groups[row - column].append(value)
    return dict(groups)


if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(group_anagrams(words))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(group_anagrams_counting(words))
    print(group_shifted_strings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]))
    # [['abc', 'bcd', 'xyz'], ['acef'], ['az', 'ba'], ['a', 'z']]
    print(diagonal_groups([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # {0: [1, 5, 9], -1: [2, 6], -2: [3], 1: [4, 8], 2: [7]}
    print(group_anagrams([]))          # []
    print(group_anagrams([""]))        # [['']]
```

The last two lines are the edge cases. An empty input gives an empty list of groups; a list
containing the empty string gives one group containing it, because `"".join(sorted(""))` is `""`,
which is a perfectly good key.

---

## 6. What it costs

Let `n` be the number of words and `k` the length of the longest word.

### The sorted key

The loop runs `n` times. Each iteration sorts a word of length `k`, which is `O(k log k)`, then joins
it, `O(k)`, then does one dictionary insert, `O(k)` because hashing a string of length `k` reads all
`k` characters.

```
 n iterations x ( k log k  +  k  +  k )  =  O(n k log k)
```

With `n = 10,000` words of length `k = 10`: `10,000 × 10 × log2(10)` ≈ `10,000 × 10 × 3.3` =
**330,000 comparison steps**.

### The counting key

The loop runs `n` times. Each iteration walks the word once, `O(k)`, builds a 26-tuple, `O(26)`, and
hashes it, `O(26)`.

```
 n iterations x ( k  +  26  +  26 )  =  O(n(k + 26))  =  O(nk) for k around 26
```

With the same numbers: `10,000 × (10 + 52)` = **620,000 steps**.

Notice the counting key is *worse* here, and this is the honest part most write-ups skip. The 26-slot
array is a fixed cost paid on every word, so for short words it loses. Work out where it wins:

```
 sorted key beats counting when   k log k  <  k + 52
 k = 10:   33  <  62    sorted wins
 k = 100:  664 <  152   counting wins
```

So the crossover is around `k ≈ 25`. **For interview-sized words, the sorted key is both simpler and
faster, and you should say so** rather than reciting that counting is O(k) and therefore better.
Counting wins for long strings, and it is the only option if the interviewer says the words can be a
megabyte each.

### Space

Both are `O(nk)` total — every input word is stored once inside some group, and the keys add at most
another `O(nk)`. There is no version of this problem with less than `O(nk)` space, because the output
itself is that big. Say that: *the output is the same size as the input, so the space is not
optional.*

### What the wrong key costs

If your key is too fine and produces `n` groups of one, you have done `O(n k log k)` work to produce
the input back again. If it is too coarse and produces one group of `n`, you have done the same work
to produce a copy of the input in a list. Both run fast and both are wrong, which is why the
complexity is never where this problem is failed.

### Compare with the brute force

The obvious approach is: for every pair of words, check whether they are anagrams. That is
`n(n-1)/2` pairs, each costing `O(k log k)`:

```
 n = 10,000:  10,000 x 9,999 / 2 = 49,995,000 pairs x 33 = 1.6 x 10^9 steps
```

Against 330,000. **A factor of about five thousand**, and the reason is exactly the reason from
[day 062](../day-062-sets/README.md): computing a key turns "compare with everything" into "look it
up once".

---

## 7. The traps

### Trap 1 — an unhashable key

```python
>>> groups = defaultdict(list)
>>> groups[["a", "b"]].append(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

The counting key is the place this bites: `return counts` where `counts` is a list raises, and
`return tuple(counts)` works. It is one word of difference and it is the commonest runtime error in
this problem.

### Trap 2 — `itertools.groupby` does not group

This one is genuinely nasty because it looks like the tool for the job, has the right name, and
produces plausible wrong output.

```python
>>> from itertools import groupby
>>> words = ["eat", "tea", "tan", "ate", "nat", "bat"]
>>> key = lambda w: "".join(sorted(w))
>>> [(k, list(v)) for k, v in groupby(words, key=key)]
[('aet', ['eat', 'tea']), ('ant', ['tan']), ('aet', ['ate']), ('ant', ['nat']), ('abt', ['bat'])]
```

Five groups instead of three, and `aet` appears twice. `groupby` only collects **runs of adjacent
items** with the same key. It does not gather items from across the sequence.

The fix is to sort first — but sort **by the key**, not by the item:

```python
>>> [(k, list(v)) for k, v in groupby(sorted(words), key=key)]
[('aet', ['ate']), ('abt', ['bat']), ('aet', ['eat']), ('ant', ['nat', 'tan']), ('aet', ['tea'])]

>>> [(k, list(v)) for k, v in groupby(sorted(words, key=key), key=key)]
[('abt', ['bat']), ('aet', ['eat', 'tea', 'ate']), ('ant', ['tan', 'nat'])]
```

Look at the middle one. `sorted(words)` sorts alphabetically, which is not the same order as the key,
so `groupby` still splits `aet` three ways. Only `sorted(words, key=key)` works. And even then you
have paid `O(n log n)` for a job the dictionary does in `O(n)`.

**In an interview, use a `defaultdict`.** Mention `groupby` only to say why you are not using it.

### Trap 3 — the key that is too coarse

Grouping anagrams by `sorted(word)` is right. Grouping them by `len(word)` and `set(word)` looks
close and is wrong:

```python
key = (len(word), frozenset(word))
```

`"aab"` and `"abb"` both give `(3, frozenset({'a','b'}))` and they are not anagrams. `frozenset`
throws away *how many* of each letter, which is exactly the thing the question is about. The test to
run: *can I construct two items with the same key that should not be together?* Here, in five
seconds, yes.

### Trap 4 — the key that is too fine

For "group words that are one edit apart" it is tempting to key on the word with each position
blanked. That is fine. For "group anagrams", keying on `tuple(sorted(word)) + (len(word),)` adds a
component that is already implied by the rest — harmless here, but the same instinct applied to
"group customers by city" produces a key of `(city, pincode, area)` and splits one city into forty
piles. **Every component you add to a key can only split groups further, never merge them.** Add none
you cannot justify.

### Trap 5 — reading from a `defaultdict` creates the pile

```python
>>> groups = defaultdict(list)
>>> groups["never seen"]
[]
>>> len(groups)
1
>>> dict(groups)
{'never seen': []}
```

If you check `if groups[k]:` instead of `if k in groups:`, you have just added an empty group, and
`list(groups.values())` now returns an empty list among your real answers. This is the same trap as
[day 063](../day-063-counting-with-dicts/README.md)'s `defaultdict(int)`, and here it shows up as an
extra `[]` in the output, which LeetCode will reject and you will stare at.

### Trap 6 — `setdefault` builds a list every single time

```python
groups.setdefault(key, []).append(word)
```

Correct, and the `[]` is constructed on every iteration even when the key already exists, then
discarded. At `n = 1,000,000` that is a million pointless allocations — roughly twice as slow as
`defaultdict` in practice. Fine for an interview; worth knowing why the other one exists.

### Trap 7 — mutating something you used as a key

If your key is a tuple built from an object's fields and you then change those fields, the group is
unaffected — the key was copied at insertion. But if you keep a `list` of items in the group and
mutate an item, the grouping is now a lie: the item sits in a pile it no longer belongs to, silently.
Same rule as [day 060](../day-060-hash-tables/README.md): **group on fields that do not change.**

---

## 8. In the interview

### How it gets asked

- *"Given an array of strings, group the anagrams together. You may return the answer in any
  order."* The standard one, LeetCode 49.
- *"Group all strings that are shifts of one another."* Same shape, harder key, and the wrap-around
  is the point.
- *"Determine if a 9×9 Sudoku board is valid."* Nobody calls it grouping, and it is three grouping
  problems at once — rows, columns and boxes — with a set per group.
- The vague one: *"I have two million files. Find the duplicates."* No mention of keys or maps. The
  whole answer is "hash the contents and group by the digest", and the follow-up is about hash
  collisions and why you would compare bytes on a match anyway.
- And the direct probe, which will come whatever the question was: *"why that key?"*

### What to say out loud, in the first ninety seconds

1. **Say the belonging rule in plain words, before any code.** "Two words are in the same group when
   they use the same letters the same number of times. Order does not matter."
2. **Turn that sentence into a key, and say why it is exactly right.** "So my key must destroy order
   and preserve counts. Sorting the letters does exactly those two things — `eat` and `tea` both
   become `aet`."
3. **Run the two tests out loud.** "Can two words that are not anagrams share this key? No, because
   the sorted letters determine the multiset. Can two anagrams get different keys? No, because
   sorting is deterministic." Fifteen seconds, and it is the strongest part of the answer.
4. **Then say the loop is trivial.** "The rest is a `defaultdict(list)` and one append per word."
5. **State the cost with both letters named.** "n words of length k, so O(n·k log k) time and O(n·k)
   space, and the space is not optional because the output is that size."

### The follow-ups

**"Can you avoid the sort?"**
"Yes — key on a tuple of 26 letter counts instead, which is O(k) per word rather than O(k log k). But
I would check the input first. The 26-count key pays a fixed 52-step cost per word, so for words of
about ten characters the sorted key is actually faster; counting wins from roughly k = 25 upwards.
And the count key assumes lowercase a to z, so it dies on Unicode while the sorted key does not."

**"What if the strings are Unicode?"**
"The fixed 26-slot array is gone. I would either keep the sorted key, which needs no assumption at
all, or use a `Counter` and key on `frozenset(counter.items())` — hashable, and it works for any
alphabet. I would mention that sorting arbitrary Unicode has its own normalisation questions, so I
would ask whether é and e-plus-accent should be equal."

**"How would you find duplicate files in a directory of two million?"**
"Group by a key, same shape. Cheapest first: group by file size, because two files of different sizes
cannot be identical, and that discards almost everything for nothing. Within each size group, hash
the contents — SHA-256 — and group by the digest. Then, for anything that collides, compare the bytes
directly, because a digest match is overwhelmingly likely but not a proof. That is three keys of
increasing cost, applied in increasing order."

**"Why not `itertools.groupby`?"**
"Because it only groups adjacent items. It would give me `aet` three separate times on the standard
example unless I sort by the key first, and sorting costs O(n log n) for something the dictionary
does in O(n). It is the right tool when the data is already ordered by the key — reading a sorted log
file, for instance."

**"Your key is a list. Will that work?"**
This one is a test, not a question. "No — dictionary keys must be hashable and a list is not. I would
return `tuple(counts)`."

### A model answer

Asked: *group these strings into anagram groups. What is your key?*

> "Let me state the rule for belonging first, because everything follows from it. Two words go in the
> same group when they contain the same letters with the same multiplicities. The order of the
> letters is exactly the thing that must not matter.
>
> So I want a key that destroys order and preserves counts. Sorting the letters of the word does
> precisely those two things: `eat` and `tea` and `ate` all become `aet`.
>
> Let me check it both ways. Could two words share that key without being anagrams? No — if the
> sorted letters are identical then the letter multisets are identical, which is the definition.
> Could two anagrams get different keys? No — sorting is deterministic, so the same multiset always
> sorts the same way. The key is exactly as coarse as it should be and no coarser.
>
> The rest is four lines: a `defaultdict(list)`, and for each word append it to the pile for its key,
> then return the values.
>
> For cost, let n be the number of words and k the longest word length. Each word costs k log k to
> sort plus k to hash, so it is O(n·k log k) time. Space is O(n·k) and that is not avoidable, because
> the output holds every input word.
>
> If you want to remove the sort I can key on a tuple of twenty-six letter counts instead, which is
> O(k) per word. I would only do that for long words though — the fixed cost of the 26-slot array
> means the sorted key is faster up to about k = 25, and the count key hard-codes lowercase English,
> so it breaks on Unicode.
>
> Edge cases: an empty list returns an empty list; the empty string is its own valid key, so a list
> containing `""` gives one group. And I would use a `defaultdict` rather than `itertools.groupby`,
> because `groupby` only collects adjacent runs and would split each anagram group several times
> unless I sorted by the key first."

---

## 9. Recall card

- **Grouping is four lines; the key is the whole problem.**
  `groups = defaultdict(list)` then `groups[key_of(item)].append(item)`. Without the import,
  `groups.setdefault(k, []).append(x)` — correct, but it allocates a throwaway `[]` on every call.
- **The recipe: say in words what makes two items belong together, then compute exactly that — no
  more, no less.** Then run both tests out loud: *same key but shouldn't be together?* (too coarse) ·
  *should be together but different keys?* (too fine).
- **The keys worth memorising:** anagrams → `"".join(sorted(word))` (destroys order, keeps counts) ·
  shifted strings → `tuple((ord(b)-ord(a)) % 26 ...)` · Sudoku box → `(r // 3, c // 3)` · diagonals →
  `r - c`, anti-diagonals → `r + c` · duplicate files → size first, then SHA-256, then compare bytes.
- **The count key is not automatically better.** `k log k` vs `k + 52` crosses over at about
  **k = 25**, so for interview-length words the sorted key wins — and it survives Unicode, which the
  26-slot array does not. Cost: **O(n·k log k)** time, **O(n·k)** space, and the space is not optional
  because the output is that big. Brute force is 5,000× worse at n = 10,000.
- **Three things that bite:** the key must be hashable (`tuple(counts)`, never `counts`) ·
  `itertools.groupby` only groups **adjacent** runs, so it splits `aet` three ways unless you
  `sorted(words, key=key)` first · reading a missing key from a `defaultdict(list)` **inserts an
  empty list** and it turns up in your output.
