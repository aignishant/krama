---
day: 6
track: dsa
title: "Python for DSA II: strings, dictionaries, and sets"
phase: "Foundations: how code costs"
status: written
---

# Day 006 · DSA — Python for DSA II: strings, dictionaries, and sets

**After today you can:** You reach for a dict or a set by reflex when a problem asks whether you have seen something before.

**The interviewer asks it as:** *How would you check for duplicates in O(n)?*

---

## 1. What this is, and why they ask it

A **dictionary** stores values under keys and finds one in a single step, no matter how many
it holds. A **set** stores values and answers "is this in here?" in a single step, no matter
how many it holds. A **string** in Python is a sequence of characters that **cannot be
changed** once made.

Those three facts convert a large family of `O(n²)` solutions into `O(n)` solutions, and
they are the reason the interview answer to "how would you check for duplicates" is one
sentence long.

Interviewers ask because the reflex is what they are testing. The question is never really
"can you detect duplicates". It is "when a problem says *have I seen this before*, does a
hash-based structure come to mind immediately, or do you write two nested loops first and
get rescued?". That reflex is worth more than any single technique in this course, because
it applies to perhaps a third of all interview problems.

---

## 2. The story

Suresh minds the shoe counter outside a temple in Nashik. On an ordinary Tuesday there are
sixty or seventy pairs. On a Saturday, and on festival days, there are six hundred.

For the first two years he did it the obvious way. Shoes went into a heap behind the
counter, roughly in the order they came in, and when someone came back he went and looked
for them. On a Tuesday that was fine — thirty seconds, and half the time he remembered the
sandals anyway. On a Saturday it was miserable. Six hundred pairs, everyone finishing at
about the same time, and a queue of people watching him crouch in a heap of footwear. The
worst was a Saturday in the monsoon when a man waited nineteen minutes and missed a bus.

Before the next festival he did something about it. He and his brother built a wall of
wooden racks along the back, seven hundred of them, each one just big enough for a pair.
Then he painted a number on every rack, one to seven hundred, and got a box of small metal
tokens made with the same numbers.

Now the whole thing changed. You hand him your shoes, he puts them in rack 412, and he gives
you token 412. When you come back you show him the token, he reads four-one-two, and he
walks straight to it. He does not look at rack 411 on the way and he does not start at the
beginning. **It takes him the same fifteen seconds whether there are twenty pairs in the wall
or six hundred**, and that is the part he still finds slightly remarkable.

There is a second thing he did not plan for and now uses every day. If a man arrives claiming
token 412 and rack 412 is empty, Suresh knows instantly that those shoes have already gone.
He does not have to search anything to know that something is not there.

The tokens themselves are simple and stubborn. They are stamped metal. When one bent last
year and the 6 looked like an 8, he did not try to fix it. He threw it away and had a new one
made.

The one bad afternoon since then was the Saturday the count went past seven hundred. There
was no rack 701, and there was no room to slip one in — the numbers are painted on the wall
in order. So he shut the counter for twenty minutes, and he and his brother put up a second
wall of racks, renumbered everything to fifteen hundred, and moved every single pair across
to its new rack. It was a bad twenty minutes. It has not happened since.

---

## 3. The idea in plain English

Suresh's wall is a **hash table**, and a hash table is what Python's dictionaries and sets
are built out of.

### The token is the key, and the rack number is worked out from it

The trick that makes the wall fast is that the token **tells you where to go**. There is no
searching, because the number *is* the location.

A Python dictionary does the same thing with a calculation. It takes your key — a string, a
number, a tuple — and runs it through a function that turns it into a number. That function
is a **hash function**, and the number it produces decides which slot to look in. Give it
the same key again and it produces the same number again, so it lands on the same slot.

So `phone_book["Anjali"]` is not a search. It is: compute the hash of `"Anjali"`, go to that
slot, read what is there. One step. `O(1)`.
[Day 060](../day-060-hash-tables/README.md) builds one from scratch; today you only need to
know that it works and what it costs.

### The empty rack: sets and membership

Suresh's second discovery is the whole of set membership. To know that something is **not**
there, he does not have to look anywhere except the one place it would be.

A **set** is a dictionary that keeps only the keys. `x in some_set` computes the hash of `x`,
goes to that slot, and reports whether anything is there. `O(1)` on average, whether the set
holds ten items or ten million.

Compare that with a list. `x in some_list` walks from the beginning until it finds `x` or
runs out — `O(n)`. **The two are spelled identically.** That single collision of syntax is
responsible for more accidental quadratics in Python than anything else.

### That is the whole duplicates answer

```python
def has_duplicate(items: list[int]) -> bool:
    seen = set()
    for x in items:
        if x in seen:
            return True
        seen.add(x)
    return False
```

One pass, and each step is `O(1)`. `O(n)` time, `O(n)` space. That is the answer the
interviewer is waiting for, and it fits on five lines.

### The bad Saturday: what "average" is hiding

When the count passed seven hundred, everything had to move. Python does the same. A dict or
set keeps more slots than entries, and when it gets about two-thirds full it allocates a
bigger table and **re-inserts every key** into the new one. That is a **rehash**, and it is
`O(n)` for that one insertion.

Averaged over many insertions it disappears, exactly like `list.append` on
[day 005](../day-005-python-lists-and-tuples/README.md). So the honest statement is:
**dict and set operations are `O(1)` average, amortised.**

There is also a worst case. If every key landed in the same slot, lookups would degrade to
`O(n)`. In practice Python's hashing makes this vanishingly unlikely for ordinary data, and
strings are additionally randomised per run to stop anyone doing it deliberately. Say
"`O(1)` average, `O(n)` worst case" in an interview and you have said the correct thing.

### What can be a key, and what cannot

Only things that cannot change can be keys, because a key whose value changed would hash to a
different slot and become unfindable.

**Allowed:** numbers, strings, tuples of allowed things, `frozenset`.
**Not allowed:** lists, dictionaries, sets.

So grid coordinates go in as `seen.add((row, col))` — a tuple — and never as a list.

### Strings are stamped, not written

Suresh threw the bent token away rather than fixing it. Python strings work the same way:
they are **immutable**. Every operation that looks like it changes a string actually builds a
new one.

```python
s = "hello"
s[0] = "H"
```

```
Traceback (most recent call last):
  File "d6.py", line 2, in <module>
    s[0] = "H"
    ~^^^
TypeError: 'str' object does not support item assignment
```

The consequence that costs people interviews:

```python
out = ""
for ch in text:
    out += ch          # builds a whole new string, every time
```

Each `+=` copies everything built so far into a new string. The costs are 1, 2, 3, ... up to
n — the staircase, `O(n²)`. The fix is to collect the pieces in a list and join once at the
end:

```python
pieces = []
for ch in text:
    pieces.append(ch)   # O(1)
out = "".join(pieces)   # one pass, O(n)
```

**`"".join(list_of_strings)` is the correct way to build a string in Python.** Learn it as a
reflex, the way you learnt `deque` yesterday.

### The two dictionary helpers you will use constantly

```python
from collections import Counter, defaultdict
```

`Counter(items)` counts everything in one line and is a dict underneath:

```python
Counter("mississippi")   # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
```

`defaultdict(list)` gives a fresh empty list for any key you touch, so grouping needs no
"is this key here yet?" check:

```python
groups = defaultdict(list)
for word in words:
    groups[sorted_key(word)].append(word)
```

Both come back properly on [day 063](../day-063-counting-with-dicts/README.md) and
[day 064](../day-064-grouping/README.md).

---

## 4. The picture

The wall of racks, which is a hash table:

```
   key "Anjali"  --> hash function --> 8,391,204,553  --> % 8 slots --> slot 1
   key "Suresh"  --> hash function --> 2,110,884,921  --> % 8 slots --> slot 5

   slot     0        1        2        3        4        5        6        7
         +--------+--------+--------+--------+--------+--------+--------+--------+
         |        | Anjali |        |        |        | Suresh |        |        |
         |        | 98765..|        |        |        | 91234..|        |        |
         +--------+--------+--------+--------+--------+--------+--------+--------+

   lookup "Anjali": hash it, go to slot 1, read. ONE step, whatever the table holds.
   lookup "Farid" : hash it, go to slot 3, find nothing -> not present. ONE step.
```

**What to notice:** finding something and finding nothing cost exactly the same. That is what
makes `x in some_set` fast, and it is the opposite of a list, where "not present" is the
worst case.

Now the same lookup in a list, so the difference is visible:

```
   list:  ["Deepa", "Farid", "Suresh", "Kavita", "Anjali", "Ravi", "Meena"]
             |        |        |         |         |
             1        2        3         4         5   <- comparisons to find "Anjali"

   "not present" is worse: all 7 comparisons, every time.
```

**What to notice:** the list has to walk. The number of steps depends on where the item is —
or on how long the list is, if the item is not there at all.

And the string-building trap, drawn out:

```
   out += ch, five times, building "abcde"

   step 1:  ""     + "a"  -> new string "a"          copied 1 character
   step 2:  "a"    + "b"  -> new string "ab"         copied 2
   step 3:  "ab"   + "c"  -> new string "abc"        copied 3
   step 4:  "abc"  + "d"  -> new string "abcd"       copied 4
   step 5:  "abcd" + "e"  -> new string "abcde"      copied 5
                                                     ----
                                             total:   15  = 5 x 6 / 2

   "".join(["a","b","c","d","e"])  ->  measures the total, allocates once, copies 5.
```

**What to notice:** the discarded strings. Four complete strings were built and thrown away
to produce one. `join` builds exactly one.

---

## 5. The code, built step by step

Build the three ways of detecting duplicates, then measure them, because the gap is the
lesson.

Start with the version everyone writes first.

```python
def has_duplicate_nested(items: list[int]) -> bool:
    """Compare every pair. O(n^2)."""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False
```

Correct, and it is Meena's copying check from [day 003](../day-003-big-o-in-plain-english/README.md).
`n × (n − 1) / 2` comparisons in the worst case.

Now the version that *looks* better and is not.

```python
def has_duplicate_list(items: list[int]) -> bool:
    """One loop — and still O(n^2), because `in` on a list is a loop."""
    seen = []
    for x in items:
        if x in seen:
            return True
        seen.append(x)
    return False
```

This is the trap. There is one visible loop, so it reads as linear. `x in seen` walks the
whole of `seen`, which grows, so it is quadratic. This is exactly trap one from day 003, and
it is worth writing out again because people keep writing it.

Now the correct version.

```python
def has_duplicate_set(items: list[int]) -> bool:
    """O(n): each membership test and each add is O(1) on average."""
    seen = set()
    for x in items:
        if x in seen:
            return True
        seen.add(x)
    return False
```

One character of difference from the previous one — `set()` instead of `[]` — and a
completely different shape.

And the one-line version, worth knowing and worth understanding.

```python
def has_duplicate_short(items: list[int]) -> bool:
    return len(set(items)) < len(items)
```

`set(items)` drops duplicates, so a shorter set means there were some. It is `O(n)` and it is
clean. The one thing it gives up: it always builds the whole set, where the loop version can
return `True` the moment it finds a repeat. For an input whose first two elements match, the
loop is two steps and this is n steps. Both are `O(n)`; only one of them stops early.

Now the string half.

```python
def build_by_concat(n: int) -> str:
    """O(n^2): every += copies the whole string built so far."""
    out = ""
    for i in range(n):
        out += "x"
    return out


def build_by_join(n: int) -> str:
    """O(n): collect the pieces, allocate once."""
    pieces = []
    for i in range(n):
        pieces.append("x")
    return "".join(pieces)
```

Here is the complete program.

```python
"""Day 6 — dictionaries, sets, and why string += is a quadratic."""

import time
from collections import Counter, defaultdict


def time_it(label: str, fn) -> float:
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    print(f"  {label:<36}{elapsed:>10.4f} s")
    return elapsed


# ---- duplicates ----------------------------------------------------------

def has_duplicate_nested(items: list[int]) -> bool:
    """O(n^2) time, O(1) space. Every pair."""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicate_list(items: list[int]) -> bool:
    """O(n^2) time. Looks linear; `in` on a list is not O(1)."""
    seen: list[int] = []
    for x in items:
        if x in seen:
            return True
        seen.append(x)
    return False


def has_duplicate_set(items: list[int]) -> bool:
    """O(n) time, O(n) space. The answer."""
    seen: set[int] = set()
    for x in items:
        if x in seen:
            return True
        seen.add(x)
    return False


def has_duplicate_short(items: list[int]) -> bool:
    """O(n) time, O(n) space. No early exit."""
    return len(set(items)) < len(items)


# ---- building strings ----------------------------------------------------

def build_by_concat(n: int) -> str:
    """Looks O(n^2) -- but CPython special-cases it. See the note under the output."""
    out = ""
    for _i in range(n):
        out += "x"
    return out


def build_by_concat_shared(n: int) -> str:
    """The honest O(n^2): a second name holds the string, so the special case cannot apply."""
    out = ""
    history = []
    for _i in range(n):
        history.append(out)        # `out` now has more than one reference...
        out = out + "x"            # ...so this must allocate and copy, every time
    return out


def build_by_join(n: int) -> str:
    """O(n): one allocation at the end."""
    pieces = []
    for _i in range(n):
        pieces.append("x")
    return "".join(pieces)


# ---- the two dict helpers ------------------------------------------------

def first_non_repeating(text: str) -> str | None:
    """The classic two-pass Counter problem."""
    counts = Counter(text)                  # O(n)
    for ch in text:                         # O(n)
        if counts[ch] == 1:
            return ch
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """defaultdict removes the 'is this key here yet?' check."""
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))         # O(k log k) for a word of length k
        groups[key].append(word)
    return list(groups.values())


if __name__ == "__main__":
    N = 20_000
    distinct = list(range(N))               # worst case: no duplicates at all

    print(f"checking {N:,} distinct values for duplicates")
    a = time_it("nested loops         O(n^2)", lambda: has_duplicate_nested(distinct))
    b = time_it("`in` on a list       O(n^2)", lambda: has_duplicate_list(distinct))
    c = time_it("`in` on a set        O(n)", lambda: has_duplicate_set(distinct))
    d = time_it("len(set(items))      O(n)", lambda: has_duplicate_short(distinct))
    print(f"  the set version is {a / c:,.0f}x faster than nested loops")
    print(f"  and {b / c:,.0f}x faster than the list version it resembles\n")

    M = 40_000
    print(f"building a string of {M:,} characters")
    e = time_it("out += ch      (special-cased)", lambda: build_by_concat(M))
    g = time_it("out = out + ch (shared)  O(n^2)", lambda: build_by_concat_shared(M))
    f = time_it('"".join(pieces)          O(n)', lambda: build_by_join(M))
    print(f"  the special-cased version is {e / f:,.1f}x the cost of join")
    print(f"  the honest quadratic is      {g / f:,.0f}x the cost of join")
    print()

    print("the two helpers")
    print(f"  first non-repeating in 'swiss'        : {first_non_repeating('swiss')}")
    print(f"  first non-repeating in 'aabb'         : {first_non_repeating('aabb')}")
    print(f"  Counter('mississippi')                : {dict(Counter('mississippi'))}")
    print(f"  grouped anagrams                      : "
          f"{group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])}")
```

This is exactly what it printed:

```
checking 20,000 distinct values for duplicates
  nested loops         O(n^2)            22.1194 s
  `in` on a list       O(n^2)             3.2798 s
  `in` on a set        O(n)               0.0035 s
  len(set(items))      O(n)               0.0017 s
  the set version is 6,348x faster than nested loops
  and 941x faster than the list version it resembles

building a string of 40,000 characters
  out += ch      (special-cased)          0.0115 s
  out = out + ch (shared)  O(n^2)         1.3205 s
  "".join(pieces)          O(n)           0.0050 s
  the special-cased version is 2.3x the cost of join
  the honest quadratic is      262x the cost of join

the two helpers
  first non-repeating in 'swiss'        : w
  first non-repeating in 'aabb'         : None
  Counter('mississippi')                : {'m': 1, 'i': 4, 's': 4, 'p': 2}
  grouped anagrams                      : [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

**Look at rows two and three.** They differ by one word — `[]` against `set()` — and by a
factor of nearly a thousand. Nothing about the code's appearance tells you which is which. You
have to know.

**Now look at the three string rows, because they contain an honest surprise.** The plain
`out += ch` version is only about twice the cost of `join`, not hundreds of times. That is not
because the language semantics changed — it is because **CPython has a special case**: when the
string being appended to has exactly one reference, the interpreter resizes it in place instead
of building a new one. The middle row defeats that by keeping a second reference, and there the
true quadratic appears at over two hundred times the cost of `join`.

Take the right lesson from this. The optimisation is real and it is also fragile: it disappears
the moment the string is stored anywhere else, passed to a function that keeps it, built up
inside a class attribute, or run on a different Python implementation. `"".join(pieces)` is
`O(n)` by construction and needs no luck, which is why it remains the correct habit.

---

## 6. What it costs

The table to know cold.

| Operation | Cost | Note |
|---|---|---|
| `d[key]`, `d[key] = v`, `key in d` | `O(1)` average | `O(n)` worst case, essentially never |
| `d.get(key, default)` | `O(1)` average | no exception on a missing key |
| `del d[key]`, `d.pop(key)` | `O(1)` average | |
| `len(d)` | `O(1)` | stored |
| `for k in d` | `O(n)` | insertion order, guaranteed since Python 3.7 |
| `x in some_set`, `s.add(x)`, `s.remove(x)` | `O(1)` average | |
| `set(items)` | `O(n)` | |
| `a & b`, `a \| b`, `a - b` | `O(min(len a, len b))` for `&`; `O(len a + len b)` for the rest | |
| `x in some_list` | **`O(n)`** | the trap |
| `s[i]` on a string | `O(1)` | |
| `s1 + s2` | `O(len s1 + len s2)` | builds a new string |
| `"".join(parts)` | `O(total length)` | one allocation |
| `s.split()`, `s.replace()`, `s.lower()` | `O(n)` | each returns a new string |
| `sub in s` (substring) | `O(n × m)` worst case | not a hash lookup |
| `sorted(s)` | `O(n log n)` | returns a list of characters |

**Why `O(1)` is honest here.** The hash of a key does not depend on how many keys exist, and
going to a slot is arithmetic. So the work is: hash the key, compute a slot, look. Three
fixed steps. The size of the table changes nothing about them.

**The memory price, with the arithmetic.** A set keeps its table under two-thirds full, so
storing n items needs about 1.5n slots at 8 bytes each, plus the objects themselves:

```
1,000,000 integers in a set:
  table slots : 1,500,000 x 8 bytes  =  12 MB
  int objects : 1,000,000 x 28 bytes =  28 MB
                                       ------
                                         40 MB

the same integers in a list:
  references  : 1,000,000 x 8 bytes  =   8 MB
  int objects : 1,000,000 x 28 bytes =  28 MB
                                       ------
                                         36 MB
```

So a set costs roughly 10–30% more memory than a list of the same values. **That is the whole
price of turning `O(n)` lookups into `O(1)` lookups**, and it is almost always worth paying.
Naming that trade out loud — "O(n) time and O(n) space, and I'm spending the space
deliberately" — is what the interviewer wants to hear.

**The string concatenation arithmetic.** Building a string of length n one character at a
time, without the in-place special case, copies:

```
1 + 2 + 3 + ... + n = n(n+1)/2 characters

at n = 40,000  ->  800,000,000 character copies
```

Eight hundred million copies to build a forty-thousand-character string. `join` copies exactly
40,000. That is the 262× measured on the shared-reference row. The special-cased row avoids
almost all of it — when it can.

**Where the trade stops being worth it.** If `n` is 20, a nested loop is 190 comparisons and
a set costs an allocation and 20 hashes. The set is not faster there, and it is not slower
enough to matter either. Use the set anyway, because it is clearer and because the constraint
will change.

---

## 7. The traps

### Trap one: the missing key

You count things, and reach for the dictionary directly:

```python
counts = {}
for ch in "hello":
    counts[ch] += 1
```

```
Traceback (most recent call last):
  File "d6.py", line 3, in <module>
    counts[ch] += 1
    ~~~~~~^^^^
KeyError: 'h'
```

Read it exactly. `counts[ch] += 1` means `counts[ch] = counts[ch] + 1`, and the right-hand
side runs first. On the very first character there is no entry to add one to, so the lookup
fails. `KeyError` names the key it could not find, which is `'h'`.

Three correct fixes, in increasing order of how much a reviewer will like them:

```python
counts[ch] = counts.get(ch, 0) + 1          # get with a default
```

```python
from collections import defaultdict
counts = defaultdict(int)                    # missing keys start at 0
counts[ch] += 1
```

```python
from collections import Counter
counts = Counter("hello")                    # the whole loop, in one call
```

Note the subtlety in the middle one: `defaultdict` **creates** the entry when you touch it.
So `if counts[x] == 0` on a `defaultdict(int)` silently adds `x` to the dictionary, which can
turn a read into a write and make a later `len(counts)` wrong. Use `x in counts` to check
without creating.

### Trap two: the key that cannot be a key

Grid problems make everyone meet this one.

```python
seen = set()
seen.add([2, 3])
```

```
Traceback (most recent call last):
  File "d6.py", line 2, in <module>
    seen.add([2, 3])
    ~~~~~~~~^^^^^^^^
TypeError: unhashable type: 'list'
```

**Unhashable** means "this cannot be run through the hash function". Lists can be changed, and
a key that changed would hash to a different slot and become invisible — the entry would
still be in the table and no lookup would ever find it again. Python refuses at the door
rather than allowing that.

The fix is a tuple, which cannot change:

```python
seen.add((2, 3))          # round brackets. This works.
```

And the same rule with the same error appears for dictionary keys:
`d[[1, 2]] = "x"` raises the identical `TypeError`. If you need a set as a key, use
`frozenset`.

**How to catch both every time:** when a value is going into a set or being used as a key,
ask "could this object be modified?". If yes, convert it — `tuple(...)` for a list,
`frozenset(...)` for a set, and `"".join(sorted(word))` for the canonical form of a word.

### The near-miss worth knowing

This one produces no error and the wrong answer:

```python
def is_anagram(a: str, b: str) -> bool:
    return set(a) == set(b)
```

`set("aab") == set("abb")` is `True`, because both sets are `{'a', 'b'}`. A set forgets how
many times something appeared. The correct version keeps the counts:

```python
def is_anagram(a: str, b: str) -> bool:
    return Counter(a) == Counter(b)
```

**Set when you care whether it appeared. Counter when you care how often.** That distinction
is worth a full second of thought each time, and it is the subject of
[day 022](../day-022-anagrams/README.md).

---

## 8. In the interview

### How it gets asked

- *"How would you check for duplicates in O(n)?"* — the direct version, often as a warm-up.
- *"Can you do that lookup faster?"* — said while you are writing `x in some_list`. It is a
  rescue. Take it.
- *"What's the time complexity of a dictionary lookup, and when is it not that?"* — the
  version that checks whether you know `O(1)` is an average.
- *"You're using a list as a dictionary key — what happens?"* — a precision check.

### What to say out loud, in the first ninety seconds

1. **Name the structure immediately.** *"I'd use a set. The question is whether I've seen
   something before, and that's exactly what a set answers in O(1)."*
2. **Describe the pass.** *"One pass over the array. For each element, check whether it's in
   the set — if it is, return True; otherwise add it and carry on."*
3. **Give both costs.** *"O(n) time, O(n) extra space."*
4. **Say why it is O(1), briefly.** *"Set membership hashes the value to a slot and looks
   there, so it doesn't depend on how many items the set holds."*
5. **Give the honest caveat.** *"That's O(1) on average. Worst case, if everything collided,
   it degrades to O(n), but Python randomises string hashing so that isn't reachable in
   practice."*
6. **Name the trade and the alternative.** *"If O(n) extra space weren't acceptable, I'd sort
   first and check adjacent pairs — O(n log n) time, O(1) extra space if the sort is in
   place."*

Step 6 is what turns a five-line answer into a design answer.

### The follow-ups

**"Why is a set lookup O(1) but a list lookup O(n)?"**
Because a set computes where the value would be, and a list has to go and look. The set runs
the value through a hash function, which produces a number, which picks a slot. Three fixed
steps, independent of size. A list has no such shortcut: elements are in insertion order, not
in an order derived from their values, so the only way to know whether something is present
is to compare against each one. That is also why finding out that something is *absent* is
the worst case for a list and costs the same as anything else for a set.

**"When is a dictionary not O(1)?"**
Two cases. When many keys hash to the same slot, lookups walk a chain and degrade toward
`O(n)` — that is the theoretical worst case, and it is why hash-flooding was once a real
denial-of-service technique against web frameworks. Python defends against it by randomising
string hashes for each run. The second case is insertion: when the table gets about
two-thirds full it allocates a bigger one and rehashes every key, which is `O(n)` for that
one insertion. Amortised over many, it is still constant.

**"Can you use a list as a dictionary key?"**
No — `TypeError: unhashable type: 'list'`. Keys have to be immutable, because the hash decides
the slot, and if the object changed after insertion its hash would change and the entry would
be permanently unreachable. Tuples work, `frozenset` works, strings and numbers work. In grid
problems I use `(row, col)` tuples for exactly this reason.

**"Do dictionaries keep insertion order?"**
Yes, and it is guaranteed by the language specification, not just an implementation detail —
it became an accident of the implementation in 3.6 and a promise in 3.7. Sets do **not** keep
order, and their iteration order can differ between runs. So if the order of your output
matters, do not iterate a set and hope.

### A model answer

> "For duplicates in O(n), I'd use a set.
>
> I walk the array once. For each element I ask whether it's already in the set. If it is,
> I've found a duplicate and I return immediately. If it isn't, I add it and move on. If I
> get to the end without a hit, there are no duplicates.
>
> That's O(n) time, because each element costs one membership test and at most one insertion,
> and both of those are O(1) on average. It's O(n) extra space in the worst case, when
> everything is distinct and the set ends up as large as the input.
>
> The reason set membership is constant is that it isn't a search. The value goes through a
> hash function, which gives a number, which picks a slot, and it looks in that one slot. It
> doesn't matter whether the set holds ten items or ten million. That's the difference from
> `x in some_list`, which is spelled identically and is O(n), because a list has to compare
> against each element in turn.
>
> I'd add the caveat that O(1) is the average. If every key collided it would degrade to
> O(n), and insertions occasionally trigger a rehash of the whole table. Neither matters in
> practice for ordinary data, but I'd want to say it rather than claim a guarantee I don't
> have.
>
> There's also a one-liner — `len(set(items)) < len(items)` — which is the same complexity and
> reads better, but it always builds the whole set, so it loses the early exit. If the first
> two elements match, the loop version does two steps and this does n.
>
> And if extra space were the constraint rather than time, I'd sort the array and check
> adjacent pairs instead: O(n log n) time, O(1) extra space with an in-place sort. That's the
> trade — I'm spending O(n) memory to buy back a factor of log n, or a factor of n against
> the nested-loop version."

That answer gives the code, both complexities, the mechanism, the honest caveat, and two
alternatives with the conditions that would make each one right.

---

## 9. Recall card

1. **"Have I seen this before?" means a set.** `x in some_set` is `O(1)`; `x in some_list` is
   `O(n)`. They are spelled the same. This is the reflex the whole day exists to build.
2. **Dict and set are `O(1)` average, `O(n)` worst case**, and insertion is amortised because
   the table occasionally rehashes.
3. **Keys must be immutable.** Tuples yes, lists no — `TypeError: unhashable type: 'list'`.
   Grid coordinates go in as `(row, col)`.
4. **Strings are immutable, so building one with `+=` in a loop is `O(n²)`** — CPython
   sometimes rescues it with an in-place resize, and that rescue vanishes the moment a second
   reference exists. Collect pieces in a list and `"".join(pieces)` once.
5. **`Counter` when you care how many, `set` when you care whether.** `set("aab") ==
   set("abb")` is `True`, and that is a bug waiting to happen.
