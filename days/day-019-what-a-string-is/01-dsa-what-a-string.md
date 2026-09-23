---
day: 19
track: dsa
title: "What a string is, and why it is immutable"
phase: "Strings"
status: written
---

# Day 019 · DSA — What a string is, and why it is immutable

**After today you can:** You can explain why building a string with += inside a loop is a trap in Python.

**The interviewer asks it as:** *Why is string concatenation in a loop slow?*

---

## 1. What this is, and why they ask it

A **string** is a sequence of characters, laid out in order, addressed by position — very nearly the
array you met on [day 009](../day-009-what-an-array-is/README.md). The one difference is the whole
of today: in Python a string is **immutable**. Once it exists, not a single character in it can ever
be changed. Every operation that looks like changing a string in fact builds a brand new one.

That single fact has a consequence that catches almost everybody. Adding one character to a string
of length `n` costs `n` steps, because the whole thing has to be copied into the new one. Do that
inside a loop and you pay `1 + 2 + 3 + ... + n` steps to build a string of length `n`, which is
`O(n²)` — quadratic. The obvious code is the slow code.

Interviewers ask this for two reasons. It is a fast, reliable filter: a candidate who says "strings
are immutable, so `+=` in a loop is quadratic, use a list and `join`" has clearly worked with the
language, and one who says "I think it's a bit slower" has not. And it recurs constantly in real
problems — every question that builds an answer character by character has this trap in it, which is
why [day 020](../day-020-building-strings/README.md) is entirely about the fix.

---

## 2. The story

Vimala and her husband moved into the flat in Whitefield in March, and the one thing missing was a
nameplate on the door. There is a small shop near the bus stop with an old man who does engraving —
brass plates, plastic ones, a machine on the counter that makes a high whining noise and throws up
a fine gold dust.

She went on a Tuesday and gave him her husband's name. Four inches by ten, brass. He said Thursday,
and it was ready on Thursday, and it looked good.

Then her mother-in-law, who lives with them, said quite reasonably that her name should be on it
too. So Vimala went back on the Saturday with the plate.

The old man turned it over in his hands and shook his head. He could not add to it. The letters are
cut into the metal, and once they are cut they are where they are — he cannot move them up an inch
to make room, and squeezing a second name into the space below would look wrong because the spacing
is worked out for the whole plate at once. What he does instead is take a fresh plate, and cut both
names onto it. The first name gets cut all over again, from the beginning.

Fine, she said. Two hundred rupees, Tuesday.

Three weeks later her son's name had to go on. Third plate. All three names cut from scratch, the
first name now being cut for the third time and the second for the second time.

She was standing in the shop when it occurred to her, and she laughed about it later. If she had
simply asked everyone in the house at the start and gone once with all three names, it would have
been one plate and one job. Instead the old man had cut the same name three times, made three
plates, and charged her three times, and she had spent three Saturdays on the bus.

The old man, who has been doing this for forty years, said what he always says to people who come
back a second time. Decide the whole thing first. Then come.

---

## 3. The idea in plain English

The brass plate is a string. The letters are cut in and cannot be moved. To "change" it you make a
new one, and making a new one means cutting **every** letter again, not just the new ones.

### What a string actually is

A string is a sequence of characters in order, and you address them by position exactly as you do
an array — first position is 0.

```python
s = "hello"
s[0]      # 'h'
s[-1]     # 'o'    negative counts from the end
len(s)    # 5
s[1:4]    # 'ell'  from 1 up to but not including 4
```

`s[1:4]` is a **slice** — a new string made of part of the old one. Note *new*: slicing does not
give you a view into the original, it gives you a fresh copy of that section. That matters for cost,
and §6 counts it.

### Immutable, and what it forbids

**Immutable** means the value cannot be changed after it is created. Not "should not" — cannot. The
language refuses:

```python
s = "hello"
s[0] = "H"
```

```
TypeError: 'str' object does not support item assignment
```

A list allows exactly this and a string does not, and that is the only real difference between the
two for our purposes. A list is a shelf you can rearrange; a string is a cut plate.

So what does this do?

```python
s = "hello"
s = s + " world"
```

It does **not** modify the string `"hello"`. It builds a completely new string, `"hello world"`, by
copying all five characters of the old one and then the six new ones, and then points the name `s`
at the new string. The old `"hello"` is untouched and, if nothing else refers to it, thrown away.

You can watch that happen:

```python
a = "hello"
b = a
a = a + " world"
print(a, b)        # hello world hello
```

`b` still says `hello`. If strings were mutable, `b` would have changed too — which is exactly the
kind of surprise immutability exists to prevent.

### Why the language does it this way

Three reasons, and the first is the one to say in an interview.

**Strings can be dictionary keys and set members.** A dictionary works by computing a number from
the key — its hash — and using that to decide where to store it. If a key could change after it was
filed, it would be filed in the wrong place and could never be found again. Immutable things can be
hashed safely; mutable things cannot, which is why `{"a": 1}` works and `{[1,2]: 3}` raises
`TypeError: unhashable type: 'list'`. Dictionaries are days
[006](../day-006-python-strings-dicts-sets/README.md) and
[060](../day-060-hash-tables/README.md), and they lean on this completely.

**Sharing is free and safe.** Because nothing can modify a string, two variables can point at the
same one with no risk. Python takes advantage: identical short literals in your source often become
one object.

```python
x = "hello"
y = "hello"
x is y        # True — the same object
```

**It removes a whole class of bug.** You can pass a string to a function knowing it cannot come back
altered.

### The cost, which is the actual question

Here is the trap, and it is Vimala's three Saturdays:

```python
s = ""
for word in words:
    s = s + word       # a whole new string every time
```

Each turn copies everything built so far. Building a result of length `n` one character at a time
copies 1, then 2, then 3, and so on:

```
1 + 2 + 3 + ... + n  =  n(n + 1) / 2
```

For `n = 100,000` that is about **five billion character copies** to produce a string of a hundred
thousand characters. The work is quadratic in the size of the answer.

### The fix, which is the old man's advice

Decide the whole thing first, then make it once. Collect the pieces in a list — which *is* mutable
and *does* append cheaply — and join them at the end:

```python
parts = []
for word in words:
    parts.append(word)     # O(1) amortised, from day 011
result = "".join(parts)    # one pass, one allocation
```

`"".join(parts)` walks the list once to add up the total length, allocates a string of exactly that
size, and copies each piece into it once. Every character is copied exactly one time. That is
`O(n)`, and §6 shows the measured difference: 36 times faster at a hundred and sixty thousand
characters, and the gap widens with size.

The string before the `.join` is the **separator** — `"".join` glues with nothing between,
`", ".join` puts a comma and a space between each pair. It is a method on the separator, not on the
list, which reads oddly the first time and is worth saying out loud once.

### An honest note about `+=`

You may benchmark this and find that `s += "x"` in a loop looks linear rather than quadratic. It
sometimes is, because CPython has a special case: when the string being extended has no other
references, it can occasionally resize it where it stands instead of copying.

Do not rely on this. It disappears the moment anything else refers to the string, it disappears if
you build the other way round — `s = "x" + s` — and it does not exist in other Python
implementations. The measurement in §6 uses the prepend form for exactly this reason, and shows the
textbook quadratic. **The right answer in an interview is that string building is quadratic and you
use `join`;** mentioning the special case afterwards, as a caveat, reads as depth rather than
pedantry.

---

## 4. The picture

A string is an array of characters with fixed positions:

```
  position   0    1    2    3    4
           +----+----+----+----+----+
   "hello" | h  | e  | l  | l  | o  |
           +----+----+----+----+----+
             ^                   ^
           s[0]                s[4], also s[-1]

           s[1:4]  =  "ell"     (1, 2, 3 — the 4 is not included)
```

**What to notice:** it is exactly the day-009 array picture. Reading `s[3]` is `O(1)` — one jump.
The only thing missing is the ability to write into a box.

Now the cost of building one character at a time. Each row is one turn of the loop, and each `#` is
one character copied:

```
  turn 1   result "a"       copied: #                    1
  turn 2   result "ab"      copied: ##                   2
  turn 3   result "abc"     copied: ###                  3
  turn 4   result "abcd"    copied: ####                 4
  turn 5   result "abcde"   copied: #####                5
                                              ---------------
                            total copies for n = 5:      15

           for n characters:  1 + 2 + ... + n  =  n(n+1)/2  ->  O(n²)
```

Against the `join` version:

```
  build the list      a  b  c  d  e         n cheap appends
  add up the lengths                        one pass
  allocate once       [_____________]       exactly n characters
  copy each piece     a  b  c  d  e         each character copied ONCE
                                              ---------------
                            total copies for n = 5:       5   ->  O(n)
```

**What to notice:** the triangle in the first picture is the whole problem. Every character in the
early part of the string gets copied again on every subsequent turn — the first character is copied
`n` times. The second picture has no triangle; it is a rectangle one row deep.

---

## 5. The code, built step by step

### Reading a string

```python
s = "interview"
print(s[0], s[-1], len(s))       # i w 9
print(s[0:4], s[:4], s[5:])      # inte inte view
print(s[::-1])                   # weivretni  — the whole string, backwards
```

`s[::-1]` is a slice with a step of `-1`. It is the idiomatic Python way to reverse a string and it
is worth knowing cold, because reversing shows up in palindromes on
[day 023](../day-023-palindromes/README.md). It builds a new string, so it costs `O(n)` time and
`O(n)` space — say that, rather than pretending it is free.

### What you cannot do

```python
s = "hello"
s[0] = "H"          # TypeError
s.append("!")       # AttributeError — that is a list method
```

To get a modified string you build a new one:

```python
s = "H" + s[1:]     # 'Hello'
```

### The methods that come up constantly

Every one of these **returns a new string** and leaves the original alone. This is the second most
common string bug in interviews.

```python
"  padded  ".strip()          # 'padded'      — whitespace off both ends
"a,b,,c".split(",")           # ['a', 'b', '', 'c']  — note the empty piece
"-".join(["a", "b", "c"])     # 'a-b-c'
"Hello".lower()               # 'hello'
"hello world".replace("world", "there")   # 'hello there'
"hello".startswith("he")      # True
"hello".find("z")             # -1     — not found
"hello".index("z")            # raises ValueError
```

`find` returns `-1` when it fails and `index` raises. Pick deliberately: `find` when absence is
normal, `index` when absence is a bug you want to hear about.

### Building a string, the wrong way and the right way

The wrong way, written out so you recognise it:

```python
def shout(words: list[str]) -> str:
    result = ""
    for word in words:
        result = result + word.upper() + " "    # a new string every turn
    return result.strip()
```

The right way:

```python
def shout(words: list[str]) -> str:
    parts = []
    for word in words:
        parts.append(word.upper())              # cheap append
    return " ".join(parts)                      # one allocation, one copy each
```

Notice a second benefit: the separator is handled by `join`, so there is no trailing space to strip
off. The fix made the code shorter as well as faster, which is usually a sign it is the right fix.

The same thing as a comprehension, which is what you would actually write:

```python
return " ".join(word.upper() for word in words)
```

### When you are genuinely mutating, use a list

If you need to change characters at positions — a cipher, a swap, an in-place-looking transform —
convert to a list, work on it, and join back:

```python
chars = list("hello")     # ['h', 'e', 'l', 'l', 'o']
chars[0] = "H"
result = "".join(chars)   # 'Hello'
```

`list(s)` is `O(n)`, the changes are `O(1)` each, and the `join` is `O(n)`. Total `O(n)`, against
`O(n²)` if you rebuilt the string on every change. **This is the standard answer to "modify a string
in place" in Python, and it is worth saying that Python cannot literally do it** — there is no such
thing as an in-place string edit — so you convert, edit, and convert back.

### The complete, runnable comparison

```python
import time


def build_by_concatenation(n: int) -> float:
    """Quadratic. Each turn copies everything built so far."""
    s = ""
    start = time.perf_counter()
    for _ in range(n):
        s = "x" + s          # prepend: cannot be optimised away
    return time.perf_counter() - start


def build_by_join(n: int) -> float:
    """Linear. Cheap appends, then one allocation and one copy per character."""
    parts: list[str] = []
    start = time.perf_counter()
    for _ in range(n):
        parts.append("x")
    _ = "".join(parts)
    return time.perf_counter() - start


def to_title_case(sentence: str) -> str:
    """A small real use: capitalise each word. Builds once, not per word."""
    return " ".join(word[0].upper() + word[1:] for word in sentence.split() if word)


def reverse_words(sentence: str) -> str:
    """'the sky is blue' -> 'blue is sky the'. LeetCode 151, the easy version."""
    return " ".join(reversed(sentence.split()))


def swap_case_manually(s: str) -> str:
    """Character-by-character work: build a list, join once."""
    out: list[str] = []
    for ch in s:
        out.append(ch.lower() if ch.isupper() else ch.upper())
    return "".join(out)


if __name__ == "__main__":
    for n in (20_000, 40_000, 80_000, 160_000):
        concat = build_by_concatenation(n)
        joined = build_by_join(n)
        print(f"n={n:>7}   concat {concat:.4f}s   join {joined:.4f}s   "
              f"ratio {concat / joined:.0f}x")

    print(to_title_case("the sky is blue"))       # The Sky Is Blue
    print(reverse_words("the sky is blue"))       # blue is sky the
    print(swap_case_manually("Hello World"))      # hELLO wORLD
```

Measured on Python 3.12:

```
n=  20000   concat 0.0054s   join 0.0011s   ratio    5x
n=  40000   concat 0.0208s   join 0.0022s   ratio    9x
n=  80000   concat 0.0790s   join 0.0043s   ratio   18x
n= 160000   concat 0.3062s   join 0.0086s   ratio   36x
```

Look at the concat column doubling: 0.0054, 0.0208, 0.0790, 0.3062. Each time `n` doubles, the time
goes up roughly **four** times. That is the signature of `O(n²)` and it is worth recognising on
sight. The join column doubles when `n` doubles, which is `O(n)`.

---

## 6. What it costs

### Reading and slicing

- `s[i]` — one jump to a known position. **O(1)**.
- `len(s)` — Python stores the length. **O(1)**.
- `s[a:b]` — allocates and copies `b - a` characters. **O(k)** time and **O(k)** space where `k` is
  the slice length. `s[::-1]` is therefore `O(n)` in both.
- `s1 == s2` — compares character by character, stopping at the first difference. **O(n)** worst
  case, and worst case is when the strings are equal, which is the common case in a dictionary
  lookup.
- `"abc" in s` — the naive scan is **O(n × m)** for a haystack of `n` and needle of `m`. Python's
  actual implementation is cleverer, and [day 025](../day-025-pattern-matching/README.md) covers
  what interviewers expect you to say here.

### Building, counted properly

**Concatenation in a loop.** On turn `k`, the result has `k` characters, and building the next one
copies all `k` plus the new piece. Adding those up over `n` turns:

```
1 + 2 + 3 + ... + n  =  n(n + 1) / 2  ≈  n² / 2
```

At `n = 100,000`: `100,000 × 100,001 / 2` ≈ **5 billion** character copies. **O(n²) time.**

**List and join.** `n` appends, each `O(1)` amortised — from
[day 011](../day-011-insert-and-delete/README.md), the list occasionally grows and copies, but
spread over all the appends it averages to constant. Then `join` does one pass to total the
lengths and one pass to copy, so `2n` steps. Total `n + 2n = 3n`: **O(n) time**, and `O(n)` extra
space for the list of pieces.

**The ratio.** `n²/2` against `3n` is `n/6`. At `n = 100,000` that predicts about 16,000 times
fewer operations. The measured ratio is smaller — 36× at `n = 160,000` — because a character copy
inside CPython's optimised memory move is very much cheaper than a Python-level loop turn. The
*shape* of the growth is what matters and it matches: four times the time for twice the input.

### The number to have ready

> Building a 100,000-character string with `+=` is about 5 billion character copies. With a list and
> `join` it is about 300,000 operations. That is the difference between a visible pause and no pause
> at all, and it comes entirely from strings being immutable.

### Space

Every operation that "changes" a string allocates a new one. A chain of five transformations on a
one-megabyte string — strip, lower, replace, split, join — creates several megabyte-sized
intermediates. Usually irrelevant; occasionally the reason a process runs out of memory on a large
file. If it matters, the answer is to work line by line rather than loading the whole thing.

---

## 7. The traps

### The real error: trying to assign into a string

```python
s = "hello"
s[0] = "H"
```

```
TypeError: 'str' object does not support item assignment
```

The message is precise, and recognising it instantly saves you thirty seconds in an interview. The
fix is either `s = "H" + s[1:]`, or convert to a list if you are making several changes.

### The real error: reaching for a list method

```python
s = "hello"
s.append("!")
```

```
AttributeError: 'str' object has no attribute 'append'
```

There is no `append`, no `insert`, no `remove`, no `sort` on a string, because all four would
modify it. `sorted(s)` exists and returns a **list** of characters, which surprises people:
`sorted("cab")` is `['a', 'b', 'c']`, not `"abc"`. You need `"".join(sorted(s))` — and that idiom is
the whole of the anagram question on [day 022](../day-022-anagrams/README.md).

### The near-miss: expecting a method to modify in place

```python
s = "hello world"
s.replace("world", "there")
print(s)
```

```
hello world
```

Nothing changed, and there is no error to tell you. `replace` returned a new string and you threw it
away. Every string method behaves like this — `strip`, `lower`, `upper`, `replace`, `title` — and the
fix is always `s = s.replace(...)`.

This is the single most common string bug for people coming from languages where such methods
mutate, and because it fails silently it can survive a long time in real code.

### The near-miss: `is` instead of `==`

```python
a = "hello"
b = "hello"
print(a is b)                       # True

c = "hello"
d = "".join(["hel", "lo"])
print(c == d)                       # True
print(c is d)                       # False
```

`==` compares the characters. `is` asks whether they are the same object. Identical literals written
in your source often end up as one shared object, so `is` appears to work — right up until one of
the strings is built at run time, at which point it silently returns `False`. **Never compare strings
with `is`.** Use `==`, always.

### The trap: benchmarking `+=` and concluding it is fine

```python
s = ""
for _ in range(100_000):
    s += "x"        # may look linear
```

CPython can sometimes extend such a string in place when nothing else refers to it, which makes a
naive benchmark of exactly this form look fast. Change it to `s = "x" + s`, or keep a second
reference to `s`, or run it under a different Python implementation, and the quadratic behaviour is
right there. Relying on an optimisation that vanishes when you touch the code is not a plan.

### The near-miss: `split()` versus `split(" ")`

```python
"a  b".split()        # ['a', 'b']        — splits on runs of whitespace
"a  b".split(" ")     # ['a', '', 'b']    — splits on each single space
```

With no argument, `split` treats any run of whitespace as one separator and ignores leading and
trailing whitespace. With an explicit separator it does not. Nearly every word-counting bug in
interviews is this one line, so use bare `split()` unless you specifically want the empty pieces.

---

## 8. In the interview

### How it gets asked

- *"Why is string concatenation in a loop slow?"* — the direct version. They want "immutable",
  "quadratic", and "use join", in that order.
- *"Are strings mutable in Python? What about in Java, or C?"* — the comparison version. Python and
  Java: immutable. C: a mutable array of bytes. Java has `StringBuilder` for exactly the same reason
  Python has `join`.
- *"Reverse this string / check if it's a palindrome."* — where the immutability decides your
  approach without being mentioned.
- *"Why can a string be a dictionary key but a list can't?"* — the deeper version, and the one that
  shows whether you know *why* immutability exists rather than just that it does.

### What to say out loud, in the first ninety seconds

1. **Lead with the property, not the symptom.** *"Because strings are immutable in Python. You can
   never modify one, so anything that looks like modifying builds a whole new string."*
2. **Turn that into the cost, with the counting.** *"So `s = s + x` copies every character of `s`
   into a new string. Inside a loop, turn one copies one character, turn two copies two, and so on,
   so building a result of length n costs 1 + 2 + ... + n, which is about n²/2. Quadratic in the
   size of the output."*
3. **Give a number.** *"For a hundred thousand characters that is around five billion character
   copies."*
4. **Name the fix and why it is linear.** *"Collect the pieces in a list — appends are O(1)
   amortised — and call `join` once at the end. `join` totals the lengths, allocates exactly once,
   and copies each character exactly once. O(n)."*
5. **Add the general rule.** *"And if I need to change characters at positions, I convert to a list,
   mutate, and join back — that is O(n) overall instead of O(n²)."*
6. **Say why the language does it.** *"The reason strings are immutable is mostly hashing: a
   dictionary decides where to file a key from its contents, so a key that could change afterwards
   could never be found again. It also makes sharing safe."*

### The follow-ups

**"Why does it matter for dictionaries?"**
A dictionary stores a key by computing a number from its contents and using that number to choose a
slot. If the contents could change afterwards, the key would still be sitting in the slot chosen from
its old contents, and every future lookup — which computes the number from the *new* contents — would
look in a different slot and find nothing. So the key would effectively vanish from the dictionary
while still being in it. Python prevents that by requiring keys to be hashable, and only immutable
things are hashable. That is exactly why `{"a": 1}` works and a list key raises `TypeError:
unhashable type: 'list'`, and why tuples can be keys but lists cannot.

**"How does Java handle this?"**
Identically in the important respects. Java strings are immutable for the same reasons, and `+` in a
loop has the same quadratic problem — which is why Java ships `StringBuilder`, a mutable buffer you
append to and convert to a string once at the end. It is the same idea as Python's list-and-join:
accumulate in something cheap to extend, materialise the immutable result once. In C a string is just
an array of bytes and *is* mutable, which is faster and is also why C has a long history of buffer
overflow bugs. That trade — safety and hashability against in-place speed — is the actual answer to
the question.

**"So how do you modify a string in Python?"**
You do not, strictly. You build a new one. For a single change, slicing and concatenating is fine:
`s = s[:i] + new_char + s[i+1:]`, which is `O(n)`. For many changes, do it once: `chars = list(s)`,
mutate positions freely at `O(1)` each, then `"".join(chars)`. That is `O(n)` overall rather than
`O(n)` per edit. The list-then-join pattern is the standard answer to any interview question phrased
as "modify the string in place", and it is worth saying explicitly that Python has no true in-place
string edit so this is the honest equivalent.

**"What's the cost of slicing?"**
`O(k)` time and `O(k)` space for a slice of length `k`, because it allocates and copies — it is not a
view into the original. That is worth watching in loops: a function that takes `s[1:]` and recurses
looks elegant and is secretly `O(n²)`, because each level copies the rest of the string. The fix is
to pass the original string plus an index instead of a slice. Some languages do give you cheap
views — Go's slices, Rust's `&str` — and Python's `memoryview` does it for bytes, but plain string
slicing copies.

### A model answer

> "It's slow because Python strings are immutable. You can't change a string once it exists, so
> `s = s + x` doesn't extend `s` — it allocates a brand new string, copies every character of the old
> one into it, then copies `x` on the end, and points the name at the new object.
>
> Inside a loop that compounds. On the first turn you copy one character, on the second you copy two,
> on the third three, and so on. Building a result of length n costs 1 + 2 + ... + n character
> copies, which is n(n+1)/2 — so it's O(n²) in the length of the output, even though the output only
> has n characters in it. For a hundred thousand characters that's about five billion copies to
> produce a hundred thousand characters.
>
> The fix is to accumulate in something mutable and materialise once. Append the pieces to a list —
> that's O(1) amortised per append — and then call `"".join(parts)` at the end. `join` walks the list
> once to add up the total length, allocates a string of exactly that size, and copies each piece in
> once. Every character is copied exactly one time, so it's O(n).
>
> ```python
> parts = []
> for word in words:
>     parts.append(word)
> result = "".join(parts)
> ```
>
> I measured it: building 160,000 characters by concatenation took 0.31 seconds, and the list-and-
> join version took 0.0086 — about 36 times faster. And the shape is the giveaway: as I doubled n,
> the concatenation time went up four times each doubling, which is the signature of quadratic
> growth, while the join time just doubled.
>
> The same idea covers modifying characters. There's no in-place string edit in Python, so if I need
> to change several positions I do `chars = list(s)`, mutate freely, and `"".join(chars)` at the end.
> That's O(n) overall instead of O(n) per edit.
>
> One honest caveat: if you benchmark exactly `s += 'x'` in CPython you may see linear behaviour,
> because there's a special case that can extend the buffer in place when nothing else references
> the string. It disappears the moment you keep a second reference, or build the string the other way
> round, or use a different implementation — so it's not something to design around. The rule stands:
> accumulate in a list, join once.
>
> And the reason for the immutability in the first place is mostly hashing. A dictionary picks a slot
> for a key based on its contents. If the contents could change afterwards, the key would be sitting
> in the wrong slot and could never be found again. So Python requires keys to be hashable, and only
> immutable objects are — which is why strings and tuples work as keys and lists don't."

---

## 9. Recall card

- **A string is an immutable array of characters.** `s[i]` is `O(1)`; `s[i] = c` is a `TypeError`.
- **Every "change" builds a new string.** `+=` in a loop is `1 + 2 + ... + n` copies — **O(n²)**.
- **Build with a list and `"".join(parts)`** — `O(n)`. To edit characters: `list(s)`, mutate,
  `"".join`.
- **Every string method returns a new string.** `s.replace(...)` alone does nothing; you need
  `s = s.replace(...)`.
- **Immutable so it can be hashed** — that is why a string can be a dictionary key and a list cannot.
  Compare with `==`, never `is`.
