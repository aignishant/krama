---
day: 20
track: dsa
title: "Building strings without the quadratic trap"
phase: "Strings"
status: written
---

# Day 020 · DSA — Building strings without the quadratic trap

**After today you can:** You build strings with a list and join, and can show the cost difference with numbers.

**The interviewer asks it as:** *Build a string of n characters efficiently.*

---

## 1. What this is, and why they ask it

Yesterday established the problem: strings are immutable, so growing one a piece at a time copies
everything each turn, and building `n` characters costs `1 + 2 + ... + n` — quadratic. Today is the
fix, and the fix is one sentence:

> **Accumulate the pieces in something cheap to extend. Produce the string exactly once, at the end.**

In Python that is a list and `"".join(parts)`. In Java it is `StringBuilder`. In Go it is
`strings.Builder`. In C# it is `StringBuilder` again. Four languages, one idea, because all four
have immutable strings and all four hit the same wall.

Interviewers care about this beyond the trivia because **almost every string problem builds a
result**. Compress a string, encode a run, format a report, reverse the words, produce the output of
a state machine. If you reach for `+=` in a loop the correctness is fine and the complexity is
wrong, and complexity is what the question was about. The tell they are listening for is whether you
say "I'll collect into a list and join" *before* writing the loop, rather than being told afterwards.

There is also a second, subtler question hiding in this topic, and it is worth having ready: **what
if the problem hands you a list of characters instead of a string?** Then you can mutate, and the
right answer is often the write pointer from
[day 015](../day-015-the-write-pointer/README.md), not `join` at all.

---

## 2. The story

Hema lives on the second floor of a house in a lane in Coimbatore, and there is a vegetable shop
right at the end of that lane. Four minutes there, four minutes back, up two flights of stairs.

For years she went whenever something ran out. Somebody would say there were no onions and she would
put on her slippers and go. Half an hour later somebody else would say there was no coriander, and
she would go again. On a bad evening she did that walk four or five times, and each walk took the
same eight minutes whether she was carrying one bunch of coriander or a full bag. The bag was never
the problem. **The walk was the problem, and the walk cost the same either way.**

Her daughter changed it, in the way that daughters do, by refusing to argue and simply doing
something different. She made a note in her phone, and every time anyone in that house said the
words "we've run out of", she typed it in. It takes two seconds. Nobody has to stop what they are
doing, nobody has to remember it later, and the note just sits there getting longer.

Then on Saturday morning Hema takes the phone and goes once. She reads the whole list at the shop,
the man puts everything into her big cloth bag, and she comes back up the stairs. One walk.

She uses the big bag now, not the small one, and that is deliberate too. The big bag is more than
she needs most weeks. But going back down for a second bag would cost her the whole walk again, so
she takes the bigger one and does not think about it. The extra room costs nothing; a second trip
costs eight minutes.

The thing that surprised her was that it also made the shopping better. When she went five times she
bought whatever she had gone for and forgot two other things every time. Now she reads out a list
that somebody wrote down at the exact moment they noticed, so nothing gets missed, and she is home
by nine.

---

## 3. The idea in plain English

The note on the phone is the list. The walk to the shop is the allocate-and-copy. Adding to the note
is nearly free; the walk is not, and it costs about the same whatever you carry. So you add freely,
and you walk once.

### The rule, and the three things it applies to

**Never build a string incrementally. Collect, then join.**

```python
parts = []                 # cheap to extend
for word in words:
    parts.append(word)     # O(1) amortised — day 011
return "".join(parts)      # one allocation, each character copied once
```

`"".join(parts)` does two passes over the list: one to add up the total length, one to copy each
piece into a string allocated at exactly that size. Every character is copied exactly once. That is
`O(n)` where `n` is the length of the output.

Read the call carefully, because it reads backwards the first time. **`join` is a method on the
separator**, not on the list. `"".join(parts)` glues with nothing between; `", ".join(parts)` puts a
comma and a space between each pair, and — importantly — not after the last one. Every trailing-comma
bug you have ever seen is somebody not using `join`.

### The big bag: why appending is cheap

Hema takes a bag bigger than she needs. A Python list does the same thing. When it fills up it does
not grow by one — it allocates a noticeably larger block and copies everything across, then has room
to spare for many more appends.

That is why `append` is **`O(1)` amortised**: most appends are free, an occasional one is expensive,
and spread across all of them the average is constant. You met this on
[day 011](../day-011-insert-and-delete/README.md). It is the exact reason a list is the right
accumulator and a string is not: **a list can be given room to grow, and an immutable string cannot.**

### The four ways to build, and when each is right

| Way | Use it when | Cost |
|---|---|---|
| `"a" + b + "c"` | a **fixed, small** number of pieces | `O(total)` — fine |
| `f"{name}: {count}"` | formatting a handful of values | `O(total)` — the readable default |
| `"".join(parts)` | a **loop** builds the pieces | `O(n)` — the answer to today's question |
| `io.StringIO()` | the output is huge, or genuinely streamed | `O(n)`, and constant memory if you write it out as you go |

Notice what is *not* wrong: `"Hello, " + name + "!"` is perfectly good code. Concatenation is only a
problem when the number of concatenations grows with the input. Three pieces is three pieces.

### The comprehension form, which is what you actually write

Once the pattern is in your hands, the intermediate list usually disappears into the call:

```python
return " ".join(word.upper() for word in words)
```

That is a **generator expression** — it produces each item as `join` asks for it. Note that `join`
has to know the total length before allocating, so it materialises the generator internally anyway;
you are not saving memory, you are saving a line. Both are `O(n)` and either is fine in an
interview. Say `"".join(...)` and you have answered the question.

### `io.StringIO`, for when the output is enormous

```python
import io

buffer = io.StringIO()
for row in rows:
    buffer.write(row)
    buffer.write("\n")
result = buffer.getvalue()
```

`StringIO` is a growable in-memory text buffer — the closest thing Python has to Java's
`StringBuilder`. It is about as fast as list-and-join and it earns its place in one specific case:
when you are producing something too large to want in memory at all, you can swap `io.StringIO()`
for an actual open file and the loop does not change. That is worth one sentence in an interview and
no more.

### When the input is a list of characters, do not join at all

Some problems hand you `list[str]` rather than `str`, and that is a deliberate signal: **you are
allowed to mutate, so mutate.** LeetCode 443, *String Compression*, is the canonical one — it wants
`["a","a","b"]` turned into `["a","2","b"]` **in place**, returning the new length.

That is not a `join` problem. That is the write pointer from
[day 015](../day-015-the-write-pointer/README.md): a `read` index walking the input, a `write` index
saying where the next kept character goes, and `write <= read` throughout so overwriting is always
safe. `O(1)` extra space, where `join` would be `O(n)`.

**Reading the signature is part of solving the problem.** `s: str` means build and return.
`chars: list[str]` means mutate and return a count.

---

## 4. The picture

The two shapes, side by side. Each `#` is one character copied.

```
  GROWING A STRING                     COLLECT, THEN JOIN
  ---------------                      ------------------
  turn 1  "a"        #                 append 'a'      (no copy)
  turn 2  "ab"       ##                append 'b'      (no copy)
  turn 3  "abc"      ###               append 'c'      (no copy)
  turn 4  "abcd"     ####              append 'd'      (no copy)
  turn 5  "abcde"    #####             append 'e'      (no copy)
                     -----             join:  #####     one pass
        total 15 copies for n=5              total 5 copies for n=5

        n(n+1)/2  ->  O(n²)                  n  ->  O(n)
```

**What to notice:** the left column is a triangle and the right is a single row. The triangle is the
whole cost, and it is entirely made of re-copying characters that were already in the right order.

Inside `join`, in two passes:

```
   parts:   [ "the" ][ " " ][ "sky" ][ " " ][ "is" ]
                3   +   1  +   3    +   1  +   2     = 10      pass 1: measure

   allocate exactly 10 characters:
            +---+---+---+---+---+---+---+---+---+---+
            |   |   |   |   |   |   |   |   |   |   |
            +---+---+---+---+---+---+---+---+---+---+

            t   h   e       s   k   y       i   s              pass 2: copy once each
            +---+---+---+---+---+---+---+---+---+---+
            | t | h | e |   | s | k | y |   | i | s |
            +---+---+---+---+---+---+---+---+---+---+
```

**What to notice:** the allocation happens once and it is exactly the right size. No character is
ever moved twice, and there is no over-allocation to waste.

And the list growing underneath, which is why the appends were free (Hema's big bag):

```
  capacity   4      [a][b][c][d]                 4 appends, no copying
  full ->    8      [a][b][c][d][ ][ ][ ][ ]     one copy of 4 items, then 4 free appends
  full ->   16      [a]...                        one copy of 8 items, then 8 free appends

  n appends cost about 2n operations in total  ->  O(1) each, amortised
```

**What to notice:** the copies happen at 4, 8, 16, 32 — and each copy is followed by twice as many
free appends. That is why the average stays constant no matter how long the list gets.

---

## 5. The code, built step by step

### The pattern, in three lines

```python
parts: list[str] = []
for piece in source:
    parts.append(piece)
return "".join(parts)
```

Learn it as one unit. Whenever a loop produces output, this is the shape.

### Joining things that are not strings

```python
counts = [3, 1, 4]
",".join(counts)
```

```
TypeError: sequence item 0: expected str instance, int found
```

`join` will not convert for you. Two fixes, both idiomatic:

```python
",".join(str(c) for c in counts)     # a generator expression
",".join(map(str, counts))           # map — slightly faster, equally clear
```

The same strictness bites in plain concatenation:

```python
"count: " + 5
```

```
TypeError: can only concatenate str (not "int") to str
```

which is why f-strings exist: `f"count: {5}"` converts for you.

### Worked example one: run-length encoding

*"Turn `aaabbc` into `a3b2c1`."* A loop that produces output — so, the pattern.

Start with the accumulator and the running count.

```python
if not s:
    return ""
parts: list[str] = []
count = 1
```

The empty guard first, because the loop below reads `s[-1]` and would raise on `""`.

```python
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        count += 1
    else:
        parts.append(s[i - 1])
        parts.append(str(count))
        count = 1
```

*Walk from position 1. If this character matches the one before it, the run continues. Otherwise the
run has ended, so emit the character and its count and start a new run.*

Now the part everybody forgets:

```python
parts.append(s[-1])
parts.append(str(count))
return "".join(parts)
```

**The last run is never emitted inside the loop**, because the loop only emits when it sees a
*change*, and the final run ends by running out of string rather than by changing. Emitting after
the loop is not a special case bolted on — it is the natural consequence, and saying that out loud
is much better than saying "oh, and I forgot the end".

### Worked example two: the same problem, in place

LeetCode 443 hands you `chars: list[str]` and wants the answer written back into it.

```python
write = 0
read = 0
n = len(chars)
```

Two indices, exactly as on [day 015](../day-015-the-write-pointer/README.md).

```python
while read < n:
    ch = chars[read]
    count = 0
    while read < n and chars[read] == ch:
        read += 1
        count += 1
```

*The inner loop consumes one whole run and counts it, leaving `read` at the first character of the
next run.* This is why the outer loop is a `while` and not a `for`: `read` advances by a whole run,
not by one.

```python
    chars[write] = ch
    write += 1
    if count > 1:
        for digit in str(count):
            chars[write] = digit
            write += 1
```

*Write the character, then its count — but only if the count is more than 1, because the problem
says a run of one is written as just the character.* And a count of 12 becomes two cells, `'1'` and
`'2'`, which is why it loops over the digits of `str(count)`.

**Is the write safe?** Yes, and this is the sentence to say: a run of length `k` occupies at least
`k` cells in the input and produces at most `1 + len(str(k))` cells of output, which for every `k ≥ 1`
is never more than `k`. So `write` can never overtake `read`.

### Worked example three: formatting a report

```python
def report(rows: list[tuple[str, int]]) -> str:
    lines = [f"{name:<12} {count:>5}" for name, count in rows]
    lines.append("-" * 18)
    lines.append(f"{'TOTAL':<12} {sum(c for _, c in rows):>5}")
    return "\n".join(lines)
```

`f"{name:<12}"` pads to width 12, left aligned; `{count:>5}` pads to 5, right aligned. Building the
lines in a list and joining with `"\n"` is the same pattern, and it means the last line has no
trailing newline unless you want one.

### The complete solutions

```python
import io
import time


def run_length_encode(s: str) -> str:
    """'aaabbc' -> 'a3b2c1'. Builds once."""
    if not s:
        return ""
    parts: list[str] = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(s[i - 1])
            parts.append(str(count))
            count = 1
    parts.append(s[-1])          # the final run always ends outside the loop
    parts.append(str(count))
    return "".join(parts)


def compress(chars: list[str]) -> int:
    """LeetCode 443. In place. Returns the new length; chars[:length] is the answer.

    Runs of 1 are written as just the character. write never overtakes read.
    """
    write = 0
    read = 0
    n = len(chars)
    while read < n:
        ch = chars[read]
        count = 0
        while read < n and chars[read] == ch:   # consume one whole run
            read += 1
            count += 1
        chars[write] = ch
        write += 1
        if count > 1:
            for digit in str(count):            # 12 becomes '1' then '2'
                chars[write] = digit
                write += 1
    return write


def to_csv_line(values: list[object]) -> str:
    """Join anything, converting as you go. Note map(str, ...)."""
    return ",".join(map(str, values))


def build_with_stringio(rows: list[str]) -> str:
    """The StringBuilder equivalent. Swap StringIO for a file and nothing else changes."""
    buffer = io.StringIO()
    for row in rows:
        buffer.write(row)
        buffer.write("\n")
    return buffer.getvalue()


def compare(n: int) -> None:
    """The measurement to have in your head."""
    start = time.perf_counter()
    s = ""
    for _ in range(n):
        s = "x" + s                      # prepend: the honest quadratic
    grow = time.perf_counter() - start

    start = time.perf_counter()
    parts: list[str] = []
    for _ in range(n):
        parts.append("x")
    _ = "".join(parts)
    join = time.perf_counter() - start

    start = time.perf_counter()
    buffer = io.StringIO()
    for _ in range(n):
        buffer.write("x")
    _ = buffer.getvalue()
    sio = time.perf_counter() - start

    print(f"n={n}: grow {grow:.4f}s   list+join {join:.4f}s   StringIO {sio:.4f}s   "
          f"({grow / join:.0f}x)")


if __name__ == "__main__":
    print(run_length_encode("aaabbc"))       # a3b2c1
    print(run_length_encode("abc"))          # a1b1c1
    print(run_length_encode("a"))            # a1
    print(repr(run_length_encode("")))       # ''

    c = list("aabbccc")
    k = compress(c)
    print(k, "".join(c[:k]))                 # 6 a2b2c3

    c = list("abbbbbbbbbbbb")                # 12 b's
    k = compress(c)
    print(k, "".join(c[:k]))                 # 4 ab12

    c = list("a")
    k = compress(c)
    print(k, "".join(c[:k]))                 # 1 a

    print(to_csv_line(["Hema", 3, 37.5]))    # Hema,3,37.5
    compare(200_000)
```

Measured on Python 3.12:

```
n=200000: grow 0.9202s   list+join 0.0087s   StringIO 0.0090s   (106x)
```

---

## 6. What it costs

### The list-and-join version

**The appends.** `n` calls to `append`, each `O(1)` amortised. Totalling the occasional growth
copies — 4, then 8, then 16, and so on — the copying done across all `n` appends adds up to less
than `2n`, so the whole loop is about `3n` operations. **O(n).**

**The join.** One pass over the pieces to total the lengths, one allocation, one pass copying. Each
character is copied exactly once. **O(n)** time.

**Total: O(n) time**, `O(n)` space for the list of pieces plus `O(n)` for the result. Note honestly
that you are holding roughly two copies of the output at the moment `join` runs — that is the price,
and it is the reason `StringIO` writing straight to a file wins when the output is genuinely huge.

### Against growing a string

From yesterday: `1 + 2 + ... + n = n(n+1)/2`, so **O(n²)**.

The measured comparison at `n = 200,000`:

```
grow one at a time : 0.9202 s
list + join        : 0.0087 s      106 times faster
StringIO           : 0.0090 s      about the same as join
```

And the predicted operation counts:

```
grow : 200,000 × 200,001 / 2  ≈ 20,000,000,000 character copies
join : about 600,000 operations
```

Twenty billion against six hundred thousand. The measured ratio is only 106× rather than 33,000×
because a bulk memory copy inside CPython is enormously cheaper per character than a Python-level
loop turn — but the *shape* is what you are being asked about, and the shape is unambiguous.

### `compress`, the in-place version

The outer `while` and the inner `while` between them advance `read` exactly `n` times in total —
each character is consumed by exactly one run — so it is `n` turns of constant work: **O(n) time**.

Space: `write`, `read`, `count`, `ch`, and the digits of one count. **O(1) extra space**, which is
the entire reason the problem hands you a list rather than a string.

### The number to have ready

> Building a 200,000-character string one piece at a time is about 20 billion character copies and
> takes roughly a second. With a list and `join` it is about 600,000 operations and takes 9
> milliseconds — a hundred times faster, and the gap widens as the input grows.

---

## 7. The traps

### The near-miss: the loop that hides inside another loop

```python
def flatten(rows):
    out = ""
    for row in rows:
        for cell in row:
            out += str(cell) + ","      # quadratic, and hard to see
        out += "\n"
    return out
```

The `+=` is buried two levels down, and the quadratic cost is in the total output length, not the
number of rows. On a 1,000 × 100 grid the output is around 300,000 characters and this does tens of
billions of copies. The fix is the same as ever, and it is also clearer:

```python
def flatten(rows):
    return "\n".join(",".join(map(str, row)) for row in rows) + "\n"
```

**When you see `+=` on a string inside any loop, that is the bug**, however deeply it is nested.

### The real error: joining non-strings

```python
counts = [3, 1, 4]
print(",".join(counts))
```

```
TypeError: sequence item 0: expected str instance, int found
```

The message even tells you which item. Fix with `map(str, counts)` or a generator expression. And
the sibling error:

```python
print("count: " + 5)
```

```
TypeError: can only concatenate str (not "int") to str
```

Both are Python refusing to guess. Use an f-string when you want conversion.

### The near-miss: forgetting the final run

```python
def run_length_encode(s):
    parts = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(s[i - 1])
            parts.append(str(count))
            count = 1
    return "".join(parts)          # the last run never got emitted

print(run_length_encode("aaabbc"))
```

```
a3b2
```

The `c1` is missing. The loop emits a run only when it *sees a change*, and the last run ends by
reaching the end of the string, which is not a change. **Any "group consecutive things" loop has this
shape and this bug**, and it will recur when you group anything — so learn the reflex: after the
loop, flush what is still in hand.

### The near-miss: `join` on a string instead of a list

```python
print("-".join("abc"))
```

```
a-b-c
```

No error, and probably not what you meant. A string *is* a sequence of characters, so `join` happily
iterates it one character at a time. If you meant to join a single string to something, you did not
want `join` at all. This silently produces plausible nonsense, which is the worst kind of bug.

### The near-miss: building the separator by hand

```python
out = ""
for word in words:
    out += word + ", "
return out[:-2]          # chop off the trailing ", "
```

Quadratic, and the `[:-2]` is a bug waiting for the empty list — `"".join([])[: -2]` is fine but
`""[:-2]` on the hand-rolled version returns `""` only by luck, and with a one-character separator
the slice would be wrong. `", ".join(words)` handles the separator, the last element and the empty
list correctly, all three, and is faster. There is no situation in which the manual version is
better.

### The trap: reaching for `join` when the problem wanted mutation

If the signature says `chars: list[str]` and asks you to return a length, building a new string and
joining is the wrong answer even though it produces the right characters — it uses `O(n)` extra space
where the question is specifically testing whether you can do it in `O(1)`. **Read the signature. It
is telling you which technique is being examined.**

---

## 8. In the interview

### How it gets asked

- *"Build a string of n characters efficiently."* — the direct version, usually as a follow-up to
  "why is concatenation slow".
- *"Compress the string: aabbccc becomes a2b2c3."* — LeetCode 443, and note whether the signature
  hands you a string or a list.
- *"Reverse the words in this sentence."* — LeetCode 151, where the whole answer is `split` and
  `join`.
- *"Given a large log file, produce a summary line per user."* — the practical version, where the
  right answer includes streaming rather than holding it all.

### What to say out loud, in the first ninety seconds

1. **Announce the pattern before the loop.** *"Since strings are immutable, I'll collect the pieces
   in a list and join once at the end — that keeps it O(n) instead of O(n²)."* Saying it first is
   the whole difference.
2. **Check the signature out loud.** *"The input is a list of characters rather than a string, which
   means I'm allowed to mutate it — so this is a write-pointer problem in O(1) space, not a join
   problem."*
3. **Name what the loop emits and when.** *"I'll walk the string tracking the current run, and emit a
   character-and-count each time the run ends."*
4. **Flag the final flush before you write it.** *"The last run ends by reaching the end of the
   string rather than by changing, so it never gets emitted inside the loop — I'll emit it after."*
   Interviewers watch specifically for this.
5. **Give the cost with the counting.** *"One pass over n characters, each turn constant work, so
   O(n) time. O(n) space for the pieces — or O(1) extra if I'm mutating in place."*
6. **Mention the language-independence.** *"Same idea as StringBuilder in Java or strings.Builder in
   Go — accumulate in something mutable, materialise once."*

### The follow-ups

**"What if the output doesn't fit in memory?"**
Then do not build it in memory at all. The list-and-join approach holds the pieces *and* the result
simultaneously, which is roughly two copies at the moment `join` runs. Instead I would stream: open
the destination and write each piece as it is produced, so memory stays constant regardless of output
size. In Python that is the same loop with `file.write(piece)` in place of `parts.append(piece)` —
`io.StringIO` and a real file expose the same interface, which is exactly why the swap is free. If
the consumer is another part of the program rather than a file, I would make the function a generator
that yields pieces, letting the caller decide whether to join them or stream them onward.

**"Is `+=` really always quadratic?"**
Not always in CPython, and it is worth being precise. There is an optimisation that can extend a
string in place when nothing else refers to it, so a benchmark of exactly `s += "x"` may look linear.
It vanishes the moment another name refers to the string, or if you build the other way round with
`s = "x" + s`, or on a different Python implementation. So the behaviour you get depends on a
refcount you are not tracking, which is not something to design around. The rule stands: accumulate
in a list and join. I would mention the optimisation as a caveat, never as a justification.

**"How does this work in Java?"**
The same, with a different name. Java strings are immutable too, and `+` in a loop compiles to
repeated allocation, so Java gives you `StringBuilder` — a mutable character buffer with an
`append` method and a `toString` at the end. It is exactly Python's list-and-join with the two steps
fused into one object. `StringBuffer` is the older, synchronised version and you would use
`StringBuilder` unless you genuinely need thread safety. Go has `strings.Builder`, C# has
`StringBuilder`, and every one of them exists for the reason we just discussed.

**"In `compress`, how do you know the write index never overtakes the read index?"**
Because compression never makes a run longer. A run of `k` identical characters occupies `k` cells in
the input and produces `1 + len(str(k))` cells of output — one for the character, plus the digits of
the count, and nothing at all for the count when `k` is 1. For `k = 1` that is 1 cell out of 1 in.
For `k = 2` it is 2 out of 2. For `k = 9` it is 2 out of 9. For `k = 10` it is 3 out of 10. It is
never more, so after processing each run `write` is at most where `read` is. The worst case is a
string with no repeats at all, where output length equals input length and the two indices stay
exactly level — which is precisely the `write <= read` guarantee from the write-pointer pattern.

### A model answer

> "Strings are immutable, so if I build the answer with `+=` inside the loop, each turn copies
> everything produced so far and the whole thing costs 1 + 2 + ... + n, which is quadratic in the
> output length. So I'll collect the pieces in a list and call `join` once at the end. Appending to a
> list is O(1) amortised, and `join` makes one pass to total the lengths, allocates exactly that much,
> and copies each character once — so the whole thing is O(n).
>
> For run-length encoding specifically: I walk the string from position 1, comparing each character
> with the one before it. If they match, the run is still going and I increment a counter. If they
> differ, the run has ended, so I append the character and its count to the parts list and reset the
> counter to 1.
>
> ```python
> def run_length_encode(s: str) -> str:
>     if not s:
>         return ""
>     parts: list[str] = []
>     count = 1
>     for i in range(1, len(s)):
>         if s[i] == s[i - 1]:
>             count += 1
>         else:
>             parts.append(s[i - 1])
>             parts.append(str(count))
>             count = 1
>     parts.append(s[-1])
>     parts.append(str(count))
>     return "".join(parts)
> ```
>
> The two lines after the loop are the part worth calling out. The loop only emits when it sees a
> change, and the final run doesn't end with a change — it ends by running out of string. So the last
> group is still in hand when the loop finishes and has to be flushed. Every 'group consecutive
> items' loop has that shape, and forgetting the flush is the standard bug: on `aaabbc` you'd get
> `a3b2` and silently lose the `c1`.
>
> The empty-string guard at the top is needed because I read `s[-1]` afterwards.
>
> That's O(n) time and O(n) space for the pieces.
>
> If instead you hand me the input as a list of characters and ask me to return a length — which is
> how LeetCode 443 phrases it — then I'd solve it differently, because that signature is telling me I
> may mutate. I'd use a read index and a write index over the same list: the read index consumes a
> whole run at a time, and the write index emits the character and, if the count is above one, its
> digits. That's O(1) extra space. It's safe because compressing never lengthens a run — a run of k
> characters produces at most k cells of output — so the write index can never overtake the read
> index."

---

## 9. Recall card

- **Accumulate in a list, `"".join(parts)` once.** `O(n)` instead of `O(n²)`. Say it before the loop.
- **`join` is a method on the separator** and handles the last element for you — never build
  separators by hand.
- **`join` will not convert types:** `",".join(map(str, values))`.
- **After any grouping loop, flush the last group** — it ends by running out, not by changing.
- **`chars: list[str]` in the signature means mutate**, so use the write pointer and `O(1)` space,
  not `join`.
