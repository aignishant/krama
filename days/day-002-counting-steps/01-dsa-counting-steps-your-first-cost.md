---
day: 2
track: dsa
title: "Counting steps: your first cost model"
phase: "Foundations: how code costs"
status: written
---

# Day 002 · DSA — Counting steps: your first cost model

**After today you can:** You can count how many times a loop body runs, for any input size, without running the code.

**The interviewer asks it as:** *How many times does the inner loop execute if the array has n elements?*

---

## 1. What this is, and why they ask it

Yesterday you learnt to find the line that runs the most times. Today you learn to say
**exactly how many times it runs**, as a number you can work out before the code has ever
been executed.

The tool is small. You look at a loop's header, work out how many times its body runs, and
multiply when loops sit inside one another. Everything you will ever be asked about cost
is built out of that one move.

Interviewers ask for the count because it is the honest version of the complexity question.
Anybody can say "n squared" after hearing it enough times. Very few people can say "the
inner loop runs n minus i times, and adding that up over every i gives n times n minus one,
over two". The second answer proves you worked it out. The first proves you have seen the
answer somewhere. This distinction is the difference between a pass and a strong hire in
the first fifteen minutes of a phone screen.

---

## 2. The story

Arun works for a catering company, and today's job is a wedding at a hall on the main road.
He arrives two hours early. The hall is empty apart from the tables.

His boss says, "lay the tables", and drives off. That is the whole instruction.

Arun counts before he carries anything, because he learnt that the hard way. Twelve long
tables. Eight chairs at each table. Twelve eights are ninety-six, so he needs ninety-six
plates, ninety-six glasses and ninety-six spoons.

He goes to the van and counts what is in it. Ninety plates.

This is the moment the whole evening turns on. It is a quarter past four, the supplier is
twenty minutes away, and he knows he is six plates short *before* he has carried a single
one inside. He rings and asks for a dozen more, and they arrive while he is still on the
fourth table. Nobody ever finds out.

The version of Arun who does not count is the one who finds out at the twelfth table, at
half past five, with guests already at the door.

Then he nearly makes the other mistake. He starts loading the trolley with water jugs, one
for each place, so ninety-six jugs. He stops with the fourth one in his hand. The jugs do
not go in front of each chair. One jug sits in the middle of each table, and so does one
basket of bread. That is twelve jugs and twelve baskets, not ninety-six. Same hall, same
tables, a completely different number — and the only thing that decides it is whether the
thing belongs to a chair or to a table.

He lays the whole hall in fifty minutes.

On the drive back, his boss asks about a booking next Saturday: twenty-four tables, same
size. Arun does not need to see the place. Twenty-four eights are a hundred and ninety-two
plates, twenty-four jugs, twenty-four baskets. He answers in the van, before anybody has
gone anywhere.

---

## 3. The idea in plain English

Arun did three things today, and all three of them are on the exam.

He worked out the number **before** doing the work. He noticed that two jobs in the same
hall had two different counts. And he answered for a hall he had never seen, because he had
a rule rather than a memory.

Let us take those apart.

### One loop

A **loop body** is the indented block underneath the loop header — the part that runs again
and again. One run of the body is called one **iteration**. Counting steps means counting
iterations.

```python
for chair in range(8):
    put_plate(chair)
```

`range(8)` produces the numbers 0, 1, 2, 3, 4, 5, 6, 7. That is eight numbers, so the body
runs **8** times. Not 7, and not 9. `range(8)` starts at 0 and stops *before* 8.

Now replace the 8 with a name. If there are `n` chairs, `for chair in range(n)` runs the
body **n** times. That is the whole rule for a single loop: read the header, and count how
many values it produces.

### Two loops, one inside the other

```python
for table in range(12):
    put_jug(table)
    for chair in range(8):
        put_plate(table, chair)
```

Two lines, two different counts, and this is the part Arun almost got wrong.

`put_jug` is inside the outer loop only. It runs once per table, so **12** times.

`put_plate` is inside both loops. The outer loop runs 12 times, and for each one of those
the inner loop runs its own 8 times. So `put_plate` runs 12 × 8 = **96** times.

**The rule: loops inside loops multiply. Loops beside each other add.** Everything else
today is that sentence, applied carefully.

Notice that it is 12 × 8 and not 12 × 12. The two loops count different things — tables and
chairs — so give them different names. If there are `n` tables and `m` chairs at each, the
inner body runs `n × m` times. It is only `n × n` when both loops walk the same list, which
is the case that happens to come up most often in interviews.

### When the inner loop depends on the outer one

This is the shape you met yesterday, and the one that gets asked about most.

```python
for i in range(n):
    for j in range(i + 1, n):
        compare(i, j)
```

Now the inner loop is a different length every time round. When `i` is 0, `j` runs from 1
to n − 1, which is n − 1 iterations. When `i` is 1, it is n − 2. By the time `i` is n − 1,
it is 0.

So the total is not one multiplication. It is a sum:

```
(n − 1) + (n − 2) + ... + 2 + 1 + 0
```

Add it up for n = 8, where the sum is 7 + 6 + 5 + 4 + 3 + 2 + 1. Pair the ends: 7 + 1 is 8,
6 + 2 is 8, 5 + 3 is 8. That is three pairs of 8, which is 24, and the 4 in the middle is
left over. 24 + 4 = **28**.

The general version of that pairing is `n × (n − 1) / 2`. Check it: 8 × 7 / 2 = 28. It
matches. You will meet this number so often that it is worth recognising on sight — 10, 45,
190, 499,500 are the values at n = 5, 10, 20 and 1,000.

### The loop that halves

```python
size = n
while size > 0:
    size = size // 2
```

`//` is integer division: it divides and throws away the remainder. Start at 1,000 and the
sizes go 1,000, 500, 250, 125, 62, 31, 15, 7, 3, 1, and then 0 stops it. That is **10**
runs of the body, for an input of a thousand.

Ten, for a thousand. That is not a straight line and it is not a grid. Halving repeatedly
is the cheapest useful shape there is, and the number of halvings needed to get from `n`
down to 1 is called **log₂ n** — "log base two of n". You do not need the maths. You need
the picture: every step throws away half of what is left, so a thousand becomes ten steps
and a million becomes twenty.

### When the count depends on the input, not just its size

```python
for x in items:
    if x == target:
        return True
```

If `target` is the first item, the body runs once. If it is the last item, or missing, the
body runs n times. Same code, same n, two very different counts.

When that happens, you quote both. The **best case** is 1, the **worst case** is n. In
interviews the worst case is the default — when somebody says "the cost of this", they mean
the worst case unless they say otherwise.

---

## 4. The picture

The hall, with the two counts on it:

```
              chair0 chair1 chair2 chair3 chair4 chair5 chair6 chair7
            +------+------+------+------+------+------+------+------+
 table 0    |  P   |  P   |  P   |  P   |  P   |  P   |  P   |  P   |   + 1 jug
            +------+------+------+------+------+------+------+------+
 table 1    |  P   |  P   |  P   |  P   |  P   |  P   |  P   |  P   |   + 1 jug
            +------+------+------+------+------+------+------+------+
   ...                            ...                                    ...
            +------+------+------+------+------+------+------+------+
 table 11   |  P   |  P   |  P   |  P   |  P   |  P   |  P   |  P   |   + 1 jug
            +------+------+------+------+------+------+------+------+

            P = one plate. 12 rows x 8 columns = 96 plates.
                                                12 jugs, one per row.
```

**What to notice:** the plates fill the grid and the jugs fill the left-hand margin. A line
inside both loops touches every cell. A line inside the outer loop only touches every row.
That is the entire difference between 96 and 12.

Here is the same thing as code, with the counts written beside each line:

```
                                           times this line runs
                                           (12 tables, 8 chairs)
for table in range(12):                  |  12
    put_jug(table)                       |  12      belongs to the table
    for chair in range(8):               |  12 restarts, 8 each
        put_plate(table, chair)          |  96      belongs to the chair
    wipe_table(table)                    |  12      back out to the table level
```

**What to notice:** `wipe_table` is indented once, the same as `put_jug`, so it is back at
the table level and runs 12 times. Indentation is not decoration in Python. It is the thing
that decides the count.

And the uneven shape, where the inner loop shrinks as `i` grows:

```
 i=0   |XXXXXXX|          7 iterations
 i=1   |XXXXXX|           6
 i=2   |XXXXX|            5
 i=3   |XXXX|             4
 i=4   |XXX|              3
 i=5   |XX|               2
 i=6   |X|                1
 i=7   ||                 0
                        ----
                          28  =  8 x 7 / 2
```

**What to notice:** it is a staircase, not a rectangle. A staircase holds about half of the
rectangle it sits inside — 28 against 64 — which is where the "/ 2" comes from.

---

## 5. The code, built step by step

The way to be certain about a count is to make the program count itself. Add a `steps`
variable, tick it once inside the body, and return it. Do that for every shape until the
shapes are familiar.

Start with the single loop.

```python
def single(n: int) -> int:
    steps = 0
    for _i in range(n):
        steps += 1
    return steps
```

`_i` with an underscore is Python's way of saying "I must name this, but I never use it".
`steps += 1` is short for `steps = steps + 1`. Call `single(8)` and you get 8. The count is
`n`.

Now a loop that skips.

```python
def every_second(n: int) -> int:
    steps = 0
    for _i in range(0, n, 2):
        steps += 1
    return steps
```

`range(0, n, 2)` means "start at 0, stop before n, and go up in twos". For n = 8 it gives
0, 2, 4, 6, so the body runs 4 times. The count is `n / 2`, rounded up.

Now two loops side by side, which people mistake for a nested loop surprisingly often.

```python
def one_after_another(n: int) -> int:
    steps = 0
    for _i in range(n):
        steps += 1
    for _j in range(n):
        steps += 1
    return steps
```

The second loop starts only after the first has finished. Nothing multiplies. The count is
`n + n = 2n`. For n = 8 that is 16, not 64.

Now the rectangle.

```python
def nested_full(n: int) -> int:
    steps = 0
    for _i in range(n):
        for _j in range(n):
            steps += 1
    return steps
```

The inner loop is a fresh `range(n)` every time, so it does not care what `i` is. The count
is `n × n`. For n = 8 that is 64.

Now the staircase.

```python
def nested_triangle(n: int) -> int:
    steps = 0
    for i in range(n):
        for _j in range(i + 1, n):
            steps += 1
    return steps
```

The inner header mentions `i`, which is the signal that the count is a sum rather than a
product. The count is `n × (n − 1) / 2`. For n = 8 that is 28.

And the halving loop.

```python
def halving(n: int) -> int:
    steps = 0
    size = n
    while size > 0:
        steps += 1
        size = size // 2
    return steps
```

A `while` loop runs its body for as long as the condition is true. Because `size` is cut in
half each time, it reaches 0 quickly. The count is about `log₂ n + 1`.

Here is the complete program. It runs every shape at four sizes and prints a table, so that
you can compare your predictions against the truth in one go.

```python
"""Day 2 — count first, then check. Every shape you will meet this week."""


def single(n: int) -> int:
    """for i in range(n)"""
    steps = 0
    for _i in range(n):
        steps += 1
    return steps


def every_second(n: int) -> int:
    """for i in range(0, n, 2)"""
    steps = 0
    for _i in range(0, n, 2):
        steps += 1
    return steps


def one_after_another(n: int) -> int:
    """two separate loops, not nested"""
    steps = 0
    for _i in range(n):
        steps += 1
    for _j in range(n):
        steps += 1
    return steps


def nested_full(n: int) -> int:
    """inner loop starts at 0 every time"""
    steps = 0
    for _i in range(n):
        for _j in range(n):
            steps += 1
    return steps


def nested_triangle(n: int) -> int:
    """inner loop starts at i + 1"""
    steps = 0
    for i in range(n):
        for _j in range(i + 1, n):
            steps += 1
    return steps


def halving(n: int) -> int:
    """cut it in half until nothing is left"""
    steps = 0
    size = n
    while size > 0:
        steps += 1
        size = size // 2
    return steps


SHAPES = [
    ("single", single, "n"),
    ("every second", every_second, "n / 2, rounded up"),
    ("one after another", one_after_another, "2n"),
    ("nested full", nested_full, "n x n"),
    ("nested triangle", nested_triangle, "n x (n - 1) / 2"),
    ("halving", halving, "about log2(n) + 1"),
]

if __name__ == "__main__":
    sizes = (8, 16, 64, 1000)
    print(f"{'shape':<20}{'formula':<22}" + "".join(f"{'n=' + str(s):>12}" for s in sizes))
    print("-" * (42 + 12 * len(sizes)))
    for name, fn, formula in SHAPES:
        counts = "".join(f"{fn(s):>12,}" for s in sizes)
        print(f"{name:<20}{formula:<22}{counts}")
```

This is exactly what it printed:

```
shape               formula                        n=8        n=16        n=64      n=1000
------------------------------------------------------------------------------------------
single              n                                8          16          64       1,000
every second        n / 2, rounded up                4           8          32         500
one after another   2n                              16          32         128       2,000
nested full         n x n                           64         256       4,096   1,000,000
nested triangle     n x (n - 1) / 2                 28         120       2,016     499,500
halving             about log2(n) + 1                4           5           7          10
```

Read the last column downwards, because that column is the entire course in miniature. At
one thousand items the shapes cost 1,000, then 500, then 2,000, then one million, then half
a million, then **ten**. The gap between the top rows and the middle rows is a thousandfold.
The gap between the middle rows and the last row is another hundred-thousandfold.

Now check two of them by hand against the formulas. Nested triangle at n = 64 should be
64 × 63 / 2 = 2,016, and the program says 2,016. Halving at n = 1,000 should be about
log₂ 1,000, which is just under 10, plus one, and the program says 10. The formulas are not
decoration. They predict the measurement exactly.

---

## 6. What it costs

Here is every shape from §5, with the arithmetic written out at n = 1,000 so that the
numbers are real rather than symbolic.

| Shape | Count | At n = 1,000 |
|---|---|---:|
| One loop | `n` | 1,000 |
| Every second item | `n / 2` | 500 |
| Two loops, one after the other | `n + n = 2n` | 2,000 |
| Nested, inner from 0 | `n × n` | 1,000,000 |
| Nested, inner from `i + 1` | `n × (n − 1) / 2` | 499,500 |
| Halving | `log₂ n + 1` | 10 |

**The two nested rows are the ones to look at.** The staircase does half the work of the
rectangle — 499,500 against 1,000,000 — and yet, if you double n to 2,000, both of them go
up by four times: 4,000,000 and 1,999,000. Halving the work once is a constant-factor win.
It does not change what happens when the input grows. That difference is the whole point of
[day 003](../day-003-big-o-in-plain-english/README.md).

**How to count a loop's header, exactly.** `range(a, b)` produces `b − a` values, provided
`b` is bigger than `a`, and none at all otherwise. So `range(0, n)` gives n, `range(1, n)`
gives n − 1, and `range(i + 1, n)` gives `n − i − 1`. Nearly every off-by-one in your first
month comes from not doing this subtraction deliberately.

**Space.** Every function in §5 keeps one integer called `steps`, plus a loop variable or
two. That does not change when n changes. Ten items or ten million, the extra memory is the
same handful of values. Compare it with a function that builds a list of every pair: at
n = 1,000 that is 499,500 stored pairs, and now the memory grows as fast as the work does.
We measure that properly on [day 007](../day-007-space-complexity/README.md).

**What this buys you.** Once the count is a formula in `n`, you can answer questions about
inputs you have never seen — which is exactly what Arun did in the van. An interviewer who
asks "and if the array had a million elements?" is asking you to substitute a number into a
formula, not to run anything.

---

## 7. The traps

### Trap one: the near-miss that counts each item with itself

Here is a function that counts how many pairs a list has. It looks right, it runs without
complaint, and it returns the wrong number.

```python
def count_pairs(items: list[int]) -> int:
    pairs = 0
    for i in range(len(items)):
        for j in range(i, len(items)):     # should be i + 1
            pairs += 1
    return pairs
```

The inner loop starts at `i` instead of `i + 1`. So when `i` is 0, `j` is also 0 on the
first turn, and the code counts item 0 paired with item 0. An item paired with itself is
not a pair.

Run it on a four-item list and count what it should be by hand: item 0 with 1, 2 and 3;
item 1 with 2 and 3; item 2 with 3. That is 3 + 2 + 1 = 6 pairs.

```
near-miss : 10
correct   : 6
n(n-1)/2  : 6
```

Ten, not six. It over-counts by exactly four, which is exactly n — one bogus self-pair for
every item. Nothing crashes, no error is printed, and the function will pass any test you
wrote by eye on a two-element list, because there the answer 3 still looks plausible.

**How to catch it every time:** before you trust a nested loop, run it on a list of four
items and check the count against `n × (n − 1) / 2` = 6. Four is small enough to count in
your head and big enough to expose the error. Two is not.

### Trap two: dividing when you meant to halve

You want a loop that runs half as many times, so you write the obvious thing:

```python
n = 10
steps = 0
for i in range(n / 2):
    steps += 1
print(steps)
```

It does not run at all:

```
Traceback (most recent call last):
  File "d2.py", line 3, in <module>
    for i in range(n / 2):
             ^^^^^^^^^^^^
TypeError: 'float' object cannot be interpreted as an integer
```

Read the message literally, because it is telling you exactly what went wrong. In Python,
`/` always produces a **float** — a number with a decimal point. `10 / 2` is not `5`, it is
`5.0`. And `range` refuses floats, because there is no sensible answer to "count up to
five and a half".

The fix is `//`, which divides and throws away the remainder, giving a plain whole number:

```python
for i in range(n // 2):     # 10 // 2 is 5, not 5.0
```

The `^^^^^^^^^^^^` marks under the traceback point at `range(n / 2)`, the exact part of the
line Python objected to. This is the same error you will hit on
[day 042](../day-042-binary-search-idea/README.md) when you compute the middle of a range,
so it is worth fixing the habit now: **use `//` whenever the result is going to be used as
a position or a count.**

---

## 8. In the interview

### How it gets asked

- *"How many times does the inner loop execute if the array has n elements?"* — the direct
  version, usually about code they have just shown you.
- *"How many iterations does this do in total?"* — the same question, asking for the sum
  rather than the inner count.
- *"If I change the inner loop to start at i instead of i plus one, what changes?"* — the
  version that checks whether you actually counted or recognised a pattern.

### What to say out loud, in the first ninety seconds

Do not answer with a complexity. Answer with a count, and let the complexity follow.

1. **Read the inner loop's header out loud.** *"The inner loop is range i plus one to n."*
   Saying it aloud stops you from assuming it is `range(n)`, which is the mistake.
2. **Say whether the inner count depends on the outer variable.** *"It mentions i, so the
   length changes on every pass."* If it does not mention `i`, you are multiplying and you
   are done in one sentence.
3. **Write the count for one specific i.** *"When i is 0 it runs n minus one times, and
   when i is n minus one it runs zero times."*
4. **Add them up.** *"So the total is n minus one, plus n minus two, all the way down to
   one, which is n times n minus one over two."*
5. **Sanity-check with a small number.** *"For n equals four that's six, and I can count
   six pairs by hand, so the formula is right."* This step takes five seconds and it is the
   one that makes an interviewer relax.
6. **Only then name the shape.** *"So it's quadratic — n squared over two, with the two
   being a constant factor."*

### The follow-ups

**"Why is it n times n minus one, over two, and not n squared?"**
Because the inner loop shrinks. It runs n − 1 times, then n − 2, and so on down to 0, so
you are adding a staircase rather than filling a rectangle. Pair the first term with the
last, the second with the second-last, and every pair sums to n, which gives you n over two
pairs — hence n times n minus one, over two. It is exactly half the rectangle, so the
constant is 2, and the growth is the same either way.

**"What if the two loops are one after the other instead of nested?"**
Then you add rather than multiply: n + n = 2n. That is a completely different cost. Ten
sequential loops over the same list is 10n, which is still a straight line, while two
nested loops is n squared. Nesting is what costs you, not the number of loops on the page.

**"How do you know the halving loop is log n?"**
Count the halvings. From 1,000 you get 500, 250, 125, 62, 31, 15, 7, 3, 1 — ten steps to
reach the bottom. Doubling the input to 2,000 adds exactly one step, not a thousand. Any
time the input is cut by a constant fraction each pass, the count is the number of times
you can do that before you run out, and that is what log₂ n means.

### A model answer

The interviewer puts up the nested loop with `range(i + 1, n)` and asks how many times the
comparison runs.

> "Let me count the inner loop first. The header is `range(i + 1, n)`, so its length depends
> on `i` — it isn't a fixed `n` each time. `range(a, b)` produces `b − a` values, so for a
> given `i` the inner loop runs `n − i − 1` times.
>
> When `i` is 0 that's n − 1 iterations. When `i` is 1 it's n − 2. And when `i` gets to
> n − 1 it's zero, so the last outer pass does nothing at all.
>
> The total is the sum of all of those: n − 1, plus n − 2, down to 1 and 0. That's the
> standard staircase sum, and it collapses to n times n minus one, over two.
>
> Let me check it on a small case. For n equals 4, the formula gives 4 times 3 over 2, which
> is 6 — and by hand that's item 0 against 1, 2 and 3, then 1 against 2 and 3, then 2
> against 3. Three plus two plus one is six. It matches.
>
> So the comparison runs about n squared over two times. For n of a thousand, that's around
> half a million — 499,500 exactly. The one-half is a constant factor, so as a shape it's
> quadratic: if you double n, the work goes up roughly four times.
>
> And if you'd started the inner loop at `i` instead of `i + 1`, you'd add one more
> iteration per outer pass, so it becomes n times n plus one, over two. That's n extra
> comparisons of each item with itself, which for a pairs problem would also be a
> correctness bug, not just a cost one."

That last paragraph is the one that gets remembered. The candidate answered a question they
were not asked, in one sentence, and it showed they had understood the loop rather than
recalled a formula.

---

## 9. Recall card

1. Read the header, count the values. `range(a, b)` produces **b − a** iterations.
2. **Nested loops multiply. Loops side by side add.** A line inside both loops runs `n × m`
   times; a line inside the outer one only runs `n` times.
3. If the inner header mentions `i`, the answer is a **sum**, not a product, and it
   collapses to `n × (n − 1) / 2`.
4. Halving each pass means about **log₂ n** steps. A thousand is ten, a million is twenty.
5. When the count depends on the values and not just on `n`, quote **best case and worst
   case**. The worst case is what "the cost" means unless somebody says otherwise.
