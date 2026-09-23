---
day: 58
track: dsa
title: "Custom comparators and sorting by keys"
phase: "Sorting"
status: written
---

# Day 058 · DSA — Custom comparators and sorting by keys

**After today you can:** You can sort by two fields in opposite directions without writing a comparator class.

**The interviewer asks it as:** *Sort by score descending, then by name ascending.*

---

## 1. What this is, and why they ask it

Almost every real sorting task is "sort by *this*", not "sort these numbers". Python separates the
two completely: `sorted()` knows how to put things in order, and you tell it what to look at with
`key=`. A **key function** is called once for each element and returns the thing to order by — a
number, a string, or a tuple of both. That one argument answers ninety-nine sorting requirements out
of a hundred, and the remaining one has a different tool, `functools.cmp_to_key`.

They ask it because it is the sorting question that comes up in actual work, and because the
two-fields-in-opposite-directions version separates people quickly. "Score descending, name
ascending" cannot be done with `reverse=True`, because `reverse` applies to the whole thing. It has
one clean answer with a tuple key, one clean answer with two passes, and about four wrong answers
that look right. It also connects everything from the last two days:
[day 051](../day-051-why-sorting-matters/README.md) said `key` is called once per element,
[day 057](../day-057-stability-and-pythons-sort/README.md) said stability is what makes the two-pass
version work, and today is where those two facts get used.

---

## 2. The story

Sunil has photographed weddings around Mysore for nineteen years, and the part of the day he actually
has to think about is the big group photograph, because forty-odd people have to end up standing
somewhere and every single one of them has an opinion about where.

He does not decide the order. He has never decided the order. The family decides, and he arranges.

The first thing he asks, before anybody comes out, is what the rule is. That morning the bride's
mother said the obvious one — taller people behind, shorter people in front, so everybody's face
shows. That one is easy, because he can look at somebody and know the answer without asking.

Then, while forty-six people were standing about in the sun, she changed it. The groom's side on the
left as you look at the photograph, her side on the right. And within each side, older people in
front and younger behind.

Sunil did not learn a new way of arranging people. He has one way of arranging people and it has not
changed in nineteen years. What changed is what he had to know about each person, and now it was two
things instead of one — which side, and roughly how old.

So he walked down the group once, asked every person those two questions, once each, and remembered
the answers. Then he arranged.

That "once each" is something he learned the hard way. In his first years he used to work by holding
two people side by side and asking them both, then holding one of them against the next and asking
both again, and with forty-six people he was asking the same aunt her age five or six times and she
was getting shorter with him every time. Asking everybody once at the start and then arranging is
faster and nobody gets annoyed.

There was one thing that morning he could not do by asking each person separately. Two of the older
men were both uncles, and the mother wanted the more senior of the two on the left, and neither of
them could tell him a number — seniority in that family came out of who married whose sister, and the
only sensible statement anybody could make was about the two of them together, not about either one
on his own. So for those two, and only those two, he went and asked an elder: of these two, which one
goes on the left? One question, about a pair.

Everything else that morning was a question he could ask one person at a time.

---

## 3. The idea in plain English

Sunil's one way of arranging people is `sorted()`. The rule he is given is the **key function**.
Asking each person once is why `key=` is called once per element. And the two uncles are the one case
that needs a **comparator** — a rule about a pair, not a fact about an item.

### The key function

`sorted()` and `list.sort()` take a `key` argument. It is a function called once on each element,
and the results are what get compared:

```python
words = ["banana", "fig", "cherry", "kiwi"]
sorted(words, key=len)                 # ['fig', 'kiwi', 'banana', 'cherry']
```

`len` is called on each word once, giving `6, 3, 6, 4`, and the words are ordered by those numbers.
The words themselves are never compared with each other.

That last sentence is the whole idea. **You are not changing how sorting works; you are changing what
it looks at.**

```python
people.sort(key=lambda p: p.age)                  # by one field
files.sort(key=lambda f: f.name.lower())          # case-insensitive
records.sort(key=lambda r: r["created_at"])       # by a dictionary entry
```

### Two fields at once: the tuple key

A tuple compares element by element. It looks at the first item; if those are equal, it looks at the
second; and so on. That is exactly what "sort by department, then by name" means:

```python
people.sort(key=lambda p: (p.department, p.name))
```

```
 comparing (Sales, Bina) with (Sales, Ravi):
   "Sales" == "Sales"   -> keep going
   "Bina"  <  "Ravi"    -> Bina first

 comparing (HR, Zafar) with (Sales, Anil):
   "HR" < "Sales"       -> decided. Zafar first. Never looks at the names.
```

Tuples of any length work, and you can mix types as long as each *position* is consistent — position
one always a string, position two always a number.

### Opposite directions, which is the actual question

`reverse=True` reverses the whole ordering, so it cannot give you one field ascending and another
descending. There are three correct answers and you should know which to use when.

**One: negate the numeric field inside the tuple key.** The cleanest, when the descending field is a
number.

```python
students.sort(key=lambda s: (-s.score, s.name))     # score DESC, then name ASC
```

`-s.score` reverses that field and nothing else. This is the answer to the interview question as
usually asked, because scores are numbers.

**Two: two passes, relying on stability.** Needed when the descending field is a **string**, because
you cannot negate a string.

```python
people.sort(key=lambda p: p.name)                        # least significant first
people.sort(key=lambda p: p.department, reverse=True)    # most significant second
```

Sort by the *least* significant key first. The final pass reorders only by department; everyone
inside a department compares equal, and Python's sort is stable, so the name order set up by the
first pass survives ([day 057](../day-057-stability-and-pythons-sort/README.md)).

**Three: a reversing wrapper for a non-numeric field.** Occasionally useful, and worth knowing
exists:

```python
class Descending:
    def __init__(self, value): self.value = value
    def __lt__(self, other): return other.value < self.value      # flipped
    def __eq__(self, other): return self.value == other.value

people.sort(key=lambda p: (Descending(p.department), p.name))
```

More machinery than most situations deserve, but it does let one string field go backwards inside a
tuple key.

### When the rule is about a pair: `cmp_to_key`

Sometimes there is no per-item answer, only a rule about two items together — Sunil's two uncles.
The classic example is arranging numbers to form the largest possible number:

```
 [3, 30, 34, 5, 9]   ->   "9534330"
```

Ask yourself what the key of `3` would be. There is no answer, because whether `3` should come before
`30` depends on `30`. But the *pairwise* rule is simple: `a` comes before `b` if `a + b` (as strings)
is bigger than `b + a`. `"330" > "303"`, so `3` goes first.

For that, wrap a comparison function:

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1                # a comes first
        if a + b < b + a:
            return 1                 # b comes first
        return 0                     # equal
    strings = sorted(map(str, nums), key=cmp_to_key(compare))
    return "0" if strings[0] == "0" else "".join(strings)
```

The comparison function returns a **negative number if the first argument comes first**, positive if
the second does, and zero if they tie. That convention is inherited from C and it trips people up:
negative means "already in the right order".

`cmp_to_key` is genuinely slower — the comparison runs `O(n log n)` times rather than the key running
`n` times — so use it only when there is no key. That is the rule: **if you can describe the order by
a fact about one item, use `key`. If you can only describe it by comparing two, use `cmp_to_key`.**

### Sorting your own objects

Three options, and the choice is worth having an opinion about:

```python
# 1. key= at the call site -- the default choice
sorted(people, key=lambda p: p.age)

# 2. @dataclass(order=True) -- ordering by every field, in declaration order
@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int

# 3. __lt__ -- one natural order, defined once on the class
class Money:
    def __lt__(self, other: "Money") -> bool:
        return self.paise < other.paise
```

**Prefer `key=`** unless the type has exactly one obvious ordering that everybody would agree on.
`Version` and `Money` do. `Person` does not — sorting by age, by name and by joining date are all
equally reasonable, so putting one of them on the class is an arbitrary decision imposed on every
caller.

If you use `@dataclass(order=True)` and one field should not participate, exclude it:

```python
@dataclass(order=True)
class Task:
    priority: int
    description: str = field(compare=False)     # not part of the ordering
```

### `operator.itemgetter` and `attrgetter`

Faster than a lambda, because they run in C rather than in Python:

```python
from operator import itemgetter, attrgetter

sorted(rows, key=itemgetter(2))                    # by position 2
sorted(rows, key=itemgetter("score", "name"))      # a tuple key on a dict
sorted(people, key=attrgetter("department", "name"))
```

Roughly two times faster than the equivalent lambda on a large list. Worth using and worth being able
to name.

### The one fact that decides most arguments

**`key` is called exactly once per element — `n` times, not `n log n`.** So an expensive key function
is fine, and a lambda that does a database lookup is a disaster for a different reason. This also
means the key must be *deterministic*: a key function that returns a different answer on two calls
gives an undefined ordering.

---

## 4. The picture

How a tuple key decides, step by step:

```
 sorting by (department, name)

   element                key produced           comparison
   ------------------     -------------------    -----------------------------
   Person("Ravi","Sales") ("Sales", "Ravi")  \
   Person("Anil","HR")    ("HR", "Anil")      |  key() called ONCE per element
   Person("Bina","Sales") ("Sales", "Bina")   |  n calls, not n log n
   Person("Chandra","HR") ("HR", "Chandra")  /

   then the TUPLES are compared, position by position:

     ("HR","Anil")  vs  ("HR","Chandra")
       "HR" == "HR"          -> tie, look at position 2
       "Anil" < "Chandra"    -> Anil first

     ("HR","Anil")  vs  ("Sales","Bina")
       "HR" < "Sales"        -> DECIDED. Position 2 is never looked at.

   result: HR/Anil, HR/Chandra, Sales/Bina, Sales/Ravi
```

**What to notice:** the second element of the tuple is only ever consulted when the first is a tie.
That is why a tuple key means "then by", and why the order of the tuple's elements is the order of
the sorting rules.

The three ways to get opposite directions:

```
 want: score DESCENDING, then name ASCENDING

  data   ("Asha", 90)  ("Bala", 85)  ("Chitra", 90)  ("Devi", 85)


 (1) NEGATE the number inside the tuple key            <- use this when you can
     key = lambda s: (-s.score, s.name)
       Asha   -> (-90, "Asha")
       Chitra -> (-90, "Chitra")
       Bala   -> (-85, "Bala")
     result: Asha(90), Chitra(90), Bala(85), Devi(85)


 (2) TWO PASSES, least significant key first           <- use when the field is a string
     sort(key=name)                 -> Asha, Bala, Chitra, Devi
     sort(key=score, reverse=True)  -> Asha, Chitra, Bala, Devi
                                       ^^^^^^^^^^^^  stability preserved the name order


 (3) reverse=True ALONE                                <- WRONG. Reverses everything.
     sort(key=lambda s: (s.score, s.name), reverse=True)
     result: Chitra(90), Asha(90), Devi(85), Bala(85)
             ^^^^^^^^^^^^^^^^^^^  names now DESCENDING too
```

**What to notice:** option 3 is the trap, and it produces a plausible answer. The scores are
descending, which is what you asked for; the names are also descending, which you did not.

Key against comparator:

```
  key=            asks a question about ONE element
                  "what is this person's age?"
                  called n times
                  n = 1,000,000  ->  1,000,000 calls

  cmp_to_key()    asks a question about TWO elements
                  "of these two, which goes first?"
                  called once per comparison
                  n = 1,000,000  ->  ~20,000,000 calls,
                                     each with Python-level function overhead

  -> roughly 20x more work, and each call is slower.
     Use it ONLY when no per-element key exists.
```

**What to notice:** the choice is not stylistic. If a key exists, `cmp_to_key` costs you a factor of
twenty for nothing.

---

## 5. The code, built step by step

### The simplest key

```python
words = ["banana", "fig", "cherry", "kiwi"]
print(sorted(words, key=len))            # ['fig', 'kiwi', 'banana', 'cherry']
print(sorted(words, key=str.lower))      # case-insensitive
```

`key=len` passes the function itself, not a call to it. `key=len(words)` is a common beginner error
and raises immediately.

### The interview question, three ways

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Student:
    name: str
    score: int
```

```python
def by_score_desc_then_name(students: list[Student]) -> list[Student]:
    """Score descending, name ascending. The tuple key with a negated number."""
    return sorted(students, key=lambda s: (-s.score, s.name))
```

One line, one pass, and it is the answer to give first.

```python
def by_score_desc_then_name_two_pass(students: list[Student]) -> list[Student]:
    """The same result, using stability. Needed when the DESC field is a string."""
    out = sorted(students, key=lambda s: s.name)              # least significant
    return sorted(out, key=lambda s: s.score, reverse=True)   # most significant
```

Both give the same answer here. The second generalises to fields you cannot negate.

### The version people write that is wrong

```python
def by_score_desc_then_name_broken(students):
    return sorted(students, key=lambda s: (s.score, s.name), reverse=True)
```

```python
data = [Student("Asha", 90), Student("Bala", 85),
        Student("Chitra", 90), Student("Devi", 85)]
print([s.name for s in by_score_desc_then_name_broken(data)])
```

```
['Chitra', 'Asha', 'Devi', 'Bala']
```

The scores are descending, which looks correct. The names inside each score are descending too —
Chitra before Asha — because `reverse=True` reverses the entire comparison, including the tie-break.
Nothing raises. This is the single commonest wrong answer to this question.

### Descending on a string field

```python
def by_department_desc_then_name(people: list[Student]) -> list[Student]:
    """Department descending, name ascending. Two passes -- you cannot negate a string."""
    out = sorted(people, key=lambda p: p.name)                       # least significant, ASC
    return sorted(out, key=lambda p: p.department, reverse=True)     # most significant, DESC
```

And the attempt that does not work, so you recognise the error:

```python
sorted(people, key=lambda p: (-p.department, p.name))
```

```
Traceback (most recent call last):
  File "day58.py", line 1, in <module>
    sorted(people, key=lambda p: (-p.department, p.name))
                                  ^^^^^^^^^^^^^
TypeError: bad operand type for unary -: 'str'
```

### Sorting by a lookup table

When the order is *given* to you rather than computed — a custom alphabet, a priority list, a status
ordering:

```python
STATUS_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def by_status(tickets: list[dict]) -> list[dict]:
    """Order given as data. Unknown statuses sort last, deterministically."""
    return sorted(tickets, key=lambda t: (STATUS_ORDER.get(t["status"], 99), t["id"]))
```

Two things worth pointing at. `.get(..., 99)` means an unrecognised status does not raise — it sorts
to the end, which is almost always what you want, and the alternative (`KeyError` in production on
one unexpected row) is worse. And the `t["id"]` tie-break makes the output **deterministic**, which
matters more than people expect: without it, two runs on the same data can produce different orders
if the input order differs, and that shows up as a flaky test.

### The comparator case

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    """LeetCode 179. There is no per-element key: order depends on the PAIR."""
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1                       # negative: a comes first
        if a + b < b + a:
            return 1
        return 0

    strings = sorted((str(n) for n in nums), key=cmp_to_key(compare))
    joined = "".join(strings)
    return "0" if joined[0] == "0" else joined      # [0, 0] must give "0", not "00"
```

Say the convention out loud when you write it: **negative means the first argument comes first.** It
is the opposite of what most people guess, because it comes from C's "return `a - b`".

### The complete file

```python
"""Custom orderings: key functions, tuple keys, opposite directions, and comparators."""

from dataclasses import dataclass, field
from functools import cmp_to_key
from operator import attrgetter, itemgetter


@dataclass(frozen=True)
class Student:
    name: str
    score: int
    department: str = "General"


def by_score_desc_then_name(students: list[Student]) -> list[Student]:
    """The standard answer. Negating reverses ONE field inside a tuple key."""
    return sorted(students, key=lambda s: (-s.score, s.name))


def by_score_desc_then_name_two_pass(students: list[Student]) -> list[Student]:
    """The same, via stability. Generalises to fields that cannot be negated."""
    out = sorted(students, key=lambda s: s.name)
    return sorted(out, key=lambda s: s.score, reverse=True)


def by_department_desc_then_name(students: list[Student]) -> list[Student]:
    """A DESCENDING STRING field: two passes are the only clean way."""
    out = sorted(students, key=lambda s: s.name)
    return sorted(out, key=lambda s: s.department, reverse=True)


class Descending:
    """Wrap a value to reverse just that field inside a tuple key."""

    __slots__ = ("value",)

    def __init__(self, value) -> None:
        self.value = value

    def __lt__(self, other: "Descending") -> bool:
        return other.value < self.value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Descending) and self.value == other.value


def by_department_desc_then_name_wrapped(students: list[Student]) -> list[Student]:
    """One pass, with a reversing wrapper. More machinery; occasionally worth it."""
    return sorted(students, key=lambda s: (Descending(s.department), s.name))


STATUS_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def by_status(tickets: list[dict]) -> list[dict]:
    """Order given as DATA. Unknown values sort last; the id makes it deterministic."""
    return sorted(tickets, key=lambda t: (STATUS_ORDER.get(t["status"], 99), t["id"]))


def largest_number(nums: list[int]) -> str:
    """LeetCode 179. The one case where no per-element key exists.

    Negative return = the FIRST argument comes first. Inherited from C's a - b.
    """
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    joined = "".join(sorted((str(n) for n in nums), key=cmp_to_key(compare)))
    return "0" if joined[0] == "0" else joined


def sort_by_custom_alphabet(words: list[str], alphabet: str) -> list[str]:
    """Order the letters by a given alphabet -- an alien dictionary ordering."""
    rank = {letter: i for i, letter in enumerate(alphabet)}
    return sorted(words, key=lambda w: [rank[c] for c in w])


@dataclass(order=True, frozen=True)
class Version:
    """A type with ONE obvious ordering -- so put it on the class."""
    major: int
    minor: int
    patch: int


@dataclass(order=True)
class Task:
    """Order by priority only; the description takes no part."""
    priority: int
    description: str = field(compare=False)


if __name__ == "__main__":
    data = [
        Student("Asha", 90, "Sales"),
        Student("Bala", 85, "HR"),
        Student("Chitra", 90, "HR"),
        Student("Devi", 85, "Sales"),
    ]

    print([s.name for s in by_score_desc_then_name(data)])
    # ['Asha', 'Chitra', 'Bala', 'Devi']
    assert by_score_desc_then_name(data) == by_score_desc_then_name_two_pass(data)

    # the common WRONG answer
    print([s.name for s in sorted(data, key=lambda s: (s.score, s.name), reverse=True)])
    # ['Chitra', 'Asha', 'Devi', 'Bala']   <- names reversed too

    print([(s.department, s.name) for s in by_department_desc_then_name(data)])
    # [('Sales', 'Asha'), ('Sales', 'Devi'), ('HR', 'Bala'), ('HR', 'Chitra')]
    assert by_department_desc_then_name(data) == by_department_desc_then_name_wrapped(data)

    print(largest_number([3, 30, 34, 5, 9]))       # 9534330
    print(largest_number([10, 2]))                 # 210
    print(largest_number([0, 0]))                  # 0   -- not "00"

    print(sort_by_custom_alphabet(["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"))
    # ['world', 'word', 'row']   -- 'world' first: at position 3, 'l' (rank 3) beats 'd' (rank 4)

    print(sorted([Version(1, 2, 3), Version(1, 10, 0), Version(1, 2, 10)]))
    # [Version(1,2,3), Version(1,2,10), Version(1,10,0)]

    tickets = [
        {"id": 3, "status": "low"},
        {"id": 1, "status": "critical"},
        {"id": 2, "status": "unknown"},
        {"id": 4, "status": "critical"},
    ]
    print([t["id"] for t in by_status(tickets)])   # [1, 4, 3, 2]

    # itemgetter / attrgetter -- the same thing, ~2x faster because it is C
    rows = [("b", 2), ("a", 2), ("c", 1)]
    print(sorted(rows, key=itemgetter(1, 0)))      # [('c', 1), ('a', 2), ('b', 2)]
    print([s.name for s in sorted(data, key=attrgetter("department", "name"))])
    # ['Bala', 'Chitra', 'Asha', 'Devi']

    # key is called exactly n times
    calls = 0
    def counted(s: Student) -> int:
        global calls
        calls += 1
        return s.score
    sorted(data * 250, key=counted)
    print(calls)                                   # 1000  -- n, not n log n
```

---

## 6. What it costs

### `key` is called `n` times, not `n log n`

```
 n = 1,000,000 elements

 key=            1,000,000 calls
 cmp_to_key()    ~20,000,000 calls (one per comparison, n log n of them)

 -> 20x more calls, AND each cmp_to_key call goes through a wrapper object,
    so the real difference is closer to 30-50x on the clock.
```

That is the whole argument for preferring `key`. A key function that costs a millisecond is
`1,000` seconds at a million elements — bad, but predictable; the same work in a comparator is twenty
thousand seconds.

### The cost of the key function itself

```
 sorting 1,000,000 records

 key=attrgetter("score")     ~0.9 s   (C-level attribute access)
 key=lambda s: s.score       ~1.6 s   (a Python call per element)
 key=lambda s: (-s.score, s.name)
                             ~2.1 s   (a tuple allocation per element)
 key=cmp_to_key(compare)     ~28 s    (a wrapper object per element,
                                       plus a Python call per comparison)
```

`itemgetter`/`attrgetter` are roughly twice as fast as the equivalent lambda, for free.

### Two passes against one tuple key

```
 n = 1,000,000, sorting by two fields

 one tuple key : 1 sort  x n log n comparisons on TUPLES  (~1.5x a scalar comparison)
                 1,000,000 tuple allocations
                 ~2.1 s

 two passes    : 2 sorts x n log n comparisons on SCALARS
                 no tuple allocation
                 the SECOND sort is on nearly-sorted data, so Timsort is fast
                 ~2.4 s
```

They are close. Choose on clarity, not on speed: **one tuple key when you control both fields in one
place, two passes when a field must go descending and cannot be negated.**

### Memory

```
 sorted(data, key=f)   :  O(n) for the output list
                        + O(n) for the computed keys (Python builds them all first)

 So a tuple key on a million records allocates a million tuples, held
 simultaneously. At ~72 bytes for a 2-tuple, that is ~72 MB of keys
 on top of the data.
```

Worth knowing before you use an elaborate key on a very large list. If memory matters, sort by a
single scalar in two passes rather than building a million tuples.

### Determinism

```
 sorting 10,000 tickets by status only, where 4,000 are "high":

   the relative order of those 4,000 comes from the INPUT order.
   Two runs over the same data from a database with no ORDER BY
   can give two different outputs.

   adding a tie-break on a unique id: one extra tuple element,
   ~0.1 s at a million rows, and the output is reproducible.
```

The rule: **if the output is shown to a person or compared in a test, always end the key with
something unique.** This is a small habit that prevents a whole class of flaky test.

---

## 7. The traps

### The near-miss: `reverse=True` with a tuple key

```python
sorted(students, key=lambda s: (s.score, s.name), reverse=True)
```

```
['Chitra', 'Asha', 'Devi', 'Bala']
```

Scores descending — correct. Names descending inside each score — not what was asked. `reverse`
applies to the whole comparison, including the tie-break, and there is no way to make it apply to one
element of a tuple. This is the commonest wrong answer to today's interview question, and it produces
a plausible-looking output.

### The real error: negating a string

```python
sorted(people, key=lambda p: (-p.name, p.age))
```

```
Traceback (most recent call last):
  File "day58.py", line 1, in <module>
    sorted(people, key=lambda p: (-p.name, p.age))
                                  ^^^^^^^
TypeError: bad operand type for unary -: 'str'
```

At least this one fails loudly. The fix is two passes, or the `Descending` wrapper.

### The real error: calling the key function instead of passing it

```python
sorted(words, key=len(words))
```

```
Traceback (most recent call last):
  File "day58.py", line 1, in <module>
    sorted(words, key=len(words))
    ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'int' object is not callable
```

`key` takes a *function*, not a value. `key=len`, not `key=len(x)`.

### The real error: sorting objects with no ordering

```python
@dataclass(frozen=True)
class Student:
    name: str
    score: int

sorted([Student("Asha", 90), Student("Bala", 85)])
```

```
Traceback (most recent call last):
  File "day58.py", line 6, in <module>
    sorted([Student("Asha", 90), Student("Bala", 85)])
    ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'Student' and 'Student'
```

`@dataclass` gives `__eq__`, not `__lt__`. Either pass `key=`, or declare `order=True` — and prefer
`key=`, because most types do not have one obvious order that every caller would agree with.

### The trap: a key that raises on some rows

```python
sorted(tickets, key=lambda t: STATUS_ORDER[t["status"]])
```

```
Traceback (most recent call last):
  File "day58.py", line 1, in <module>
    sorted(tickets, key=lambda t: STATUS_ORDER[t["status"]])
                                  ~~~~~~~~~~~~^^^^^^^^^^^^^
KeyError: 'unknown'
```

One unexpected value from the database and the whole page fails to render. Use
`.get(status, <a sensible default>)` and decide deliberately whether unknown values sort first or
last.

### The trap: an inconsistent comparator

```python
def compare_broken(a, b):
    return 1 if a > b else -1       # never returns 0
```

Python will not raise. It will produce an ordering that is not what you meant, and in some inputs an
order that is not even self-consistent — `a` before `b`, `b` before `c`, `c` before `a`. A comparator
must be **total and consistent**: it must return 0 for genuinely equal items, and if it says `a`
before `b` it must never also say `b` before `a`. Getting that wrong is undefined behaviour with no
error message.

### The trap: a non-deterministic or side-effecting key

```python
sorted(users, key=lambda u: fetch_score_from_api(u.id))     # 1,000,000 HTTP calls
sorted(items, key=lambda i: random.random())                # undefined ordering
```

The first is correct and catastrophically slow — `n` network calls, and `key` being called only `n`
times is no comfort at a million rows. Fetch the scores once into a dict, then sort by the dict. The
second produces an ordering Python makes no promises about, because the comparison is not
self-consistent; to shuffle a list, use `random.shuffle`.

### The trap: `sort()` returns `None`

Still the commonest Python sorting bug, and it survives into this lesson:

```python
top = students.sort(key=lambda s: -s.score)[:3]
```

```
TypeError: 'NoneType' object is not subscriptable
```

`sorted()` when you want a value; `.sort()` when you want the side effect.

---

## 8. In the interview

### How it gets asked

- *"Sort by score descending, then by name ascending."* — the direct form. The tuple key with a
  negated number is the answer; the `reverse=True` version is the trap.
- *"Now sort by department descending, then name ascending."* — the follow-up that breaks the
  negation trick, because departments are strings.
- *"Sort these employee objects."* — expects `key=`, and a good answer says why not `__lt__`.
- *"Arrange these numbers to form the largest possible number."* — LeetCode 179, and the point is
  recognising that no per-element key exists.
- *"How many times is your key function called?"* — `n`, and the follow-up is why that matters.
- *"Sort these words by a custom alphabet."* — a lookup table as the key.

### What to say out loud, in the first ninety seconds

1. **Separate the two things.** *"Sorting doesn't change; what it looks at does. `key=` is a function
   called once per element that returns the thing to order by."*
2. **Give the tuple-key answer and read it aloud as a sentence.** *"`key=lambda s: (-s.score,
   s.name)` — negative score first, so higher scores come first; name second, so it only decides
   ties."*
3. **Say why not `reverse=True`.** *"`reverse` applies to the whole comparison, so it would reverse
   the name tie-break too. That gives a plausible wrong answer with no error."*
4. **Volunteer the string case before being asked.** *"If the descending field were a string I
   couldn't negate it — `-p.name` raises a `TypeError`. Then I'd do two passes, least significant key
   first, and rely on Python's sort being stable."*
5. **Mention the call count.** *"`key` is called n times, not n log n, so an expensive key is
   affordable. A comparator with `cmp_to_key` is called once per comparison, so about twenty times
   more at a million elements — I'd only use it when no per-element key exists."*

### The follow-ups

**"Why not just `reverse=True`?"**
Because `reverse` reverses the entire comparison, not one field of it. If I write
`key=lambda s: (s.score, s.name), reverse=True`, the scores do come out descending, which is what
makes it dangerous — it looks right. But the tie-break reverses too, so within a score the names come
out descending as well, and the output is plausible and wrong with no error anywhere. There is no
argument that applies `reverse` to only part of a tuple key. So for a numeric field I negate it
inside the key — `(-s.score, s.name)` — which reverses exactly that one field. For a field I cannot
negate, such as a string, I use two passes and rely on stability: sort by the least significant key
first, then by the most significant with `reverse=True`, and because Python's sort is stable the
second pass leaves elements with equal keys exactly as the first pass arranged them. There is a third
option I would mention if the field is a string and I want one pass: a small wrapper class with
`__lt__` flipped, used inside the tuple key. It works, and it is more machinery than most cases
deserve.

**"How many times is your key function called, and why does it matter?"**
Exactly `n` times — once per element, before any comparison happens. Python computes all the keys
first, then sorts the elements by those keys. That is why `key=` replaced the old comparison-function
style: a comparison function is called once per comparison, which is on the order of `n log n`, so at
a million elements that is about twenty million calls against one million. In practice the gap is
bigger than twenty times, because `cmp_to_key` also wraps every element in a small object whose
`__lt__` calls back into Python. It has three practical consequences. An expensive key is affordable —
if computing the key costs a millisecond, I pay for it a million times rather than twenty million.
The key must be deterministic, because it is computed once and reused; a key based on `random` or on
the current time gives an ordering Python makes no promises about. And it costs memory: all `n` keys
exist simultaneously, so a tuple key on a million records allocates a million tuples, about seventy
megabytes on top of the data. If that mattered I would sort by a single scalar in two passes rather
than building the tuples.

**"When would you need a comparator instead of a key?"**
When the ordering cannot be expressed as a fact about a single element — when it only makes sense as
a statement about a pair. The example I would give is arranging numbers to form the largest possible
number: given 3, 30, 34, 5 and 9 the answer is "9534330". Ask what the key of `3` would be and there
is no answer, because whether `3` should come before `30` depends entirely on `30` — but the pairwise
rule is simple, `a` before `b` if the string `a + b` is greater than `b + a`, since "330" beats
"303". For that I use `functools.cmp_to_key`, and the convention to remember is that a **negative**
return means the first argument comes first, which is the opposite of what most people guess because
it comes from C's `a - b`. Two cautions. It is the slow path, so I would only reach for it when no
key exists, and the comparator must be consistent — it must return zero for genuinely equal items and
must never say both that `a` comes before `b` and that `b` comes before `a`, or the result is an
undefined ordering with no error message. Other genuine cases are ordering by a graph relationship
rather than a value, and version strings where the rule is a segment-by-segment comparison — although
for versions I would usually build a tuple key instead and keep the fast path.

### A model answer

> "Sorting itself doesn't change; what changes is what it looks at. In Python that's the `key`
> argument — a function called once per element that returns the value to order by.
>
> ```python
> sorted(students, key=lambda s: (-s.score, s.name))
> ```
>
> Read as a sentence: the negated score comes first, so higher scores sort earlier; the name is
> second, so it only decides ties. A tuple compares position by position and stops as soon as one
> position differs, which is exactly what 'then by' means.
>
> The thing I'd point at is why I negated rather than using `reverse=True`. `reverse` applies to the
> whole comparison, so `key=(s.score, s.name), reverse=True` gives descending scores — which looks
> right — but also descending names inside each score, which isn't what was asked, and nothing raises.
> It's the commonest wrong answer to this question.
>
> If the descending field were a string I couldn't negate it — `-p.name` raises a `TypeError`. Then
> I'd do it in two passes: sort by the ascending field first, then by the descending field with
> `reverse=True`. That's correct only because Python's sort is stable — the second pass sees everyone
> with the same department as equal and leaves them in the order the first pass produced. Note the
> passes go least-significant-key first, which is backwards from how you say it aloud.
>
> One detail worth stating: `key` is called exactly n times, not n log n, because Python computes all
> the keys first and then sorts. So an expensive key is affordable, the key must be deterministic, and
> all n keys are held in memory at once. The alternative, `functools.cmp_to_key`, is called once per
> comparison — about twenty times more at a million elements — so I'd only use it when no per-element
> key exists at all. The case where that's genuinely true is something like arranging numbers to form
> the largest number, where whether 3 comes before 30 depends on 30.
>
> Last thing: I'd end the key with something unique — an id — if the output is shown to a person or
> compared in a test, so two runs on the same data always give the same order."

---

## 9. Recall card

- **`key=` is a function called once per element that returns what to order by.** Sorting does not
  change; what it *looks at* does. `key=len`, `key=attrgetter("dept", "name")` (~2× faster than a
  lambda — it is C), `key=lambda t: STATUS_ORDER.get(t["status"], 99)` for an order given as data.
- **Two fields: a tuple key.** It compares position by position and stops at the first difference, so
  the tuple's order *is* the order of the rules. Opposite directions: **negate the number** —
  `(-s.score, s.name)`. Never `reverse=True` on a tuple key: it reverses the tie-break too and gives
  a **plausible wrong answer with no error**.
- **A descending *string* field needs two passes**, because `-p.name` raises
  `TypeError: bad operand type for unary -: 'str'`. Sort by the **least significant key first**, then
  the most significant with `reverse=True` — correct only because Python's sort is stable.
- **`key` runs n times; a comparator runs ~n log n times.** At n = 10⁶ that is 1M calls against ~20M,
  and on the clock 30-50× because of the wrapper. Use `functools.cmp_to_key` **only when no
  per-element key exists** — the test case is LeetCode 179, where `a` before `b` iff `a+b > b+a`, and
  **negative means the first argument comes first**.
- **Prefer `key=` to `__lt__`** unless the type has one order everybody would agree on (`Version`,
  `Money`). And always end the key with something **unique** if a person or a test will see the
  output, or two runs on the same data can differ.
