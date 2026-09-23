---
day: 1
track: dsa
title: "How your code actually runs, and where the time goes"
phase: "Foundations: how code costs"
status: written
---

# Day 001 · DSA — How your code actually runs, and where the time goes

**After today you can:** You can read a function and point at the one line that does most of the work.

**The interviewer asks it as:** *Walk me through this function line by line. Which line runs the most times?*

---

## 1. What this is, and why they ask it

Your program is a list of small instructions. The computer performs them one at a time,
in order, very fast. The time your program takes is simply **how many instructions it
performs**, multiplied by how long each one takes.

You control only the first of those two numbers. That is the whole subject.

Interviewers open with this because it is the cheapest way to find out whether you can
read code or only write it. Someone who can look at eight lines and say, "this line runs
about twenty-five million times, and that is the problem", has a skill that survives every
language and every job. Someone who says, "it looks fine, let me run it", does not. Almost
every interview at Amazon, Google, Microsoft, Flipkart or Zomato contains this question in
some form, usually disguised as, "so what is the bottleneck here?"

---

## 2. The story

Anil gets home on Sunday and tips the laundry basket out on his bed. It is a week's
washing for the four people in the flat, and most of it is socks. He counts the heap
roughly. About sixty socks.

There are two jobs to do, and he does them in order.

The first job is turning them the right way out. Almost every sock comes out of the
machine inside out. So he picks one up, pulls it through, and drops it on the left side of
the bed. Then the next one. Sixty socks, sixty pulls. He puts a song on, and the job takes
four minutes.

The second job is finding the pairs, and this is the one that ruins his evening.

He picks up a plain black sock. Is its partner in the heap? He cannot tell by looking at
the heap, so he starts holding the black sock against the others, one at a time. Grey, no.
Black but shorter, no. Blue, no. Twenty socks later, he finds the match. He drops the pair
on the right side of the bed and picks up the next single sock.

An hour later he is barely halfway, and he stops to work out why. For each sock he has to
try it against the rest of the heap, and the heap is fifty-odd socks deep. He has sixty
socks to place. Sixty socks, each held up against roughly sixty others, is about three
thousand hold-ups. Even after he stops re-checking the pairs he has already matched, it is
close to two thousand. Each hold-up takes him a second. Two thousand seconds is more than
half an hour of nothing but lifting socks towards the light.

His flatmate suggests turning the big light on, so that telling grey from black is
quicker. Anil tries it, and it helps a little. But even if every hold-up became twice as
fast, half an hour would only become fifteen minutes, and he would still be sitting on
that bed at ten o'clock.

Nothing is wrong with his hands, and nothing is wrong with the light. The two jobs felt
the same — pick up a sock, look at it — and they are not the same at all. One of them is
sixty looks. The other is two thousand.

---

## 3. The idea in plain English

Anil's two jobs are the two shapes of almost every piece of code you will ever write.

Let us line the story up against the code, one piece at a time.

A **program** is a sequence of **statements**. A statement is a line of code that tells
the computer to do one small thing. Turning a sock the right way out is a statement.
Holding one sock against another is a statement.

**Running** a statement means the computer actually performs it. This is the number that
matters, and it is not the same as the number of lines you typed. Anil had one instruction
in his head — "hold this sock against that sock" — and he performed it two thousand times.

A **loop** is a statement that says, "do the following again and again". Anil working
through the heap, sock after sock, is a loop. In Python it looks like this:

```python
for sock in heap:
    turn_right_way_out(sock)
```

`heap` is a **list**: a row of values kept in order, like the socks piled on the bed. The
loop takes each value in turn and gives it the name `sock`. If there are 60 socks,
`turn_right_way_out` runs 60 times. That is the first job.

A **nested loop** is a loop inside another loop. This is the second job, and it is where
the trouble lives:

```python
for sock_a in heap:
    for sock_b in heap:
        is_pair(sock_a, sock_b)
```

Read that slowly, because it is the most important thing on this page. The outer loop runs
60 times. **For each one of those 60 runs**, the inner loop runs its own 60 times. So
`is_pair` runs 60 × 60 = 3,600 times. You wrote three lines. The computer performed three
thousand six hundred comparisons.

The line sitting deepest inside the loops — `is_pair(sock_a, sock_b)` — is what this
course calls the **hot line**. It is the line that runs the most times, so it is the line
that decides how long the whole program takes. When an interviewer asks where the time
goes, they are asking you to find the hot line.

Now the part with the big light, which is the part people underestimate.

Making each individual step faster is called a **constant-factor** improvement: a faster
machine, a faster language, a cleverer comparison. It divides your total by two, or by
ten, and then it has finished helping you. Doing fewer steps changes the shape of the
growth itself. Anil going from 2,000 hold-ups down to 60 looks is not "twice as good". It
is more than thirty times as good, and it gets better still as the pile of laundry grows.

Here is the sentence to keep. Double the socks, and the first job takes twice as long.
Double the socks, and the second job takes **four** times as long, because there is a
"sixty" on both sides of the multiplication and both of them doubled.

One honest complication, before we look at code. It is not quite true that every line
costs the same. Some lines hide a whole loop inside them. `x in my_list` looks like one
statement, and is really the computer walking the list from the start, looking for `x`. We
come back to this in §7, because it is the trap that catches almost everybody.

And if you are wondering what Anil should have done: sort the socks into colour piles
first, then match inside each small pile. That instinct is correct, it is the whole idea
behind [day 062](../day-062-sets/README.md), and you are not expected to write it yet.

---

## 4. The picture

Here is the second job written as code, with what actually happens beside each line. The
heap has been shrunk to five socks, so that you can count every step yourself.

```
                                              times this line runs
                                              (with 5 items)
def has_duplicate(items):                     |  1
    for i in range(len(items)):               |  5      outer loop
        for j in range(i + 1, len(items)):    |  5      restarts once per outer run
            if items[i] == items[j]:          | 10      <-- the hot line
                return True                   |  0 or 1
    return False                              |  1
```

**What to notice:** the `if` line is indented twice. Every extra level of indentation
inside a loop multiplies how often that line runs. Finding the hot line is usually just a
matter of finding the deepest indentation inside the loops.

And here is *why* the count is 10 and not 25. The inner loop starts at `i + 1`, so each
sock is only ever compared with the socks after it:

```
        j=0   j=1   j=2   j=3   j=4
      +-----+-----+-----+-----+-----+
 i=0  |  -  |  X  |  X  |  X  |  X  |     4 comparisons
      +-----+-----+-----+-----+-----+
 i=1  |  -  |  -  |  X  |  X  |  X  |     3
      +-----+-----+-----+-----+-----+
 i=2  |  -  |  -  |  -  |  X  |  X  |     2
      +-----+-----+-----+-----+-----+
 i=3  |  -  |  -  |  -  |  -  |  X  |     1
      +-----+-----+-----+-----+-----+
 i=4  |  -  |  -  |  -  |  -  |  -  |     0
      +-----+-----+-----+-----+-----+
                                        ----
                                          10 comparisons
```

**What to notice:** only the upper half of the grid is filled in. Skipping the lower half
halves the work, which is a real saving — and it is still nowhere near as important as the
fact that the shape is a *grid* at all. Double the number of socks, and the triangle does
not get twice as big. It gets roughly four times as big.

---

## 5. The code, built step by step

We are going to build a small program that **counts its own work**, so that you can stop
guessing and see the numbers.

Start with the first job: one loop, one pass through the heap.

```python
def sum_all(items: list[int]) -> int:
    total = 0
    for x in items:
        total = total + x
    return total
```

The line `total = total + x` sits inside one loop, so it runs once per item. Five items,
five runs. Five thousand items, five thousand runs. The relationship is a straight line:
double the items, and you double the work.

Now the second job: the nested loop.

```python
def has_duplicate(items: list[int]) -> bool:
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False
```

`range(len(items))` gives the positions 0, 1, 2, and so on, up to one less than the
length. `items[i]` means "the value at position `i`". The inner loop starts at `i + 1`, so
you never compare a sock with itself and never repeat a pair. This is the upper triangle
from the diagram above.

So far you have been told the counts. Now measure them. Add a counter that ticks once
every time the hot line runs.

```python
def count_comparisons(items: list[int]) -> int:
    comparisons = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            comparisons += 1
            _ = items[i] == items[j]
    return comparisons
```

That is the whole trick, and it is worth doing yourself at least once. You are no longer
reasoning about the code. You are watching it report on itself.

Here is the complete program. It runs both shapes at four different sizes and prints what
it finds. Copy it, run it, and read the two count columns before you read the paragraph
underneath.

```python
"""Day 1 — where the time goes. Run this and read the count columns."""

import time


def sum_all(items: list[int]) -> int:
    """One loop: touches every item once."""
    total = 0
    for x in items:
        total = total + x
    return total


def count_single(items: list[int]) -> int:
    """How many times does the hot line of sum_all run?"""
    steps = 0
    for _x in items:
        steps += 1
    return steps


def count_nested(items: list[int]) -> int:
    """How many times does the hot line of has_duplicate run?"""
    steps = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            steps += 1
            _ = items[i] == items[j]
    return steps


def timed(fn, items: list[int]) -> tuple[int, float]:
    """Run fn(items). Return what it returned, and how long it took in milliseconds."""
    start = time.perf_counter()
    result = fn(items)
    return result, (time.perf_counter() - start) * 1000


if __name__ == "__main__":
    print(f"{'items':>7} {'one loop':>12} {'ms':>8} {'nested loop':>14} {'ms':>10}")
    for n in (10, 100, 1000, 5000):
        data = list(range(n))
        single, t_single = timed(count_single, data)
        nested, t_nested = timed(count_nested, data)
        print(f"{n:>7} {single:>12,} {t_single:>8.2f} {nested:>14,} {t_nested:>10.2f}")

    print("\nsum of 1..100 =", sum_all(list(range(1, 101))))
```

This is exactly what it printed on the machine this lesson was written on:

```
  items     one loop       ms    nested loop         ms
     10           10     0.00             45       0.01
    100          100     0.01          4,950       0.63
   1000        1,000     0.06        499,500      93.84
   5000        5,000     2.88     12,497,500    1785.13

sum of 1..100 = 5050
```

Look at the two count columns, not at the milliseconds. Going from 1,000 items to 5,000
items is five times as many. The one-loop count went from 1,000 to 5,000, which is exactly
five times. The nested count went from 499,500 to 12,497,500, which is **twenty-five**
times.

Five times the input. Twenty-five times the work. That is the grid from the diagram,
showing up in real numbers.

Now run the program a second time. Your millisecond columns will not match the ones above,
and they will not even match each other. On a second run on this same machine, with
nothing changed, the last nested figure came out at **3063.92 ms** instead of 1785.13 ms.
That is almost double, for no reason you can see or control. The **count** columns were
identical to the digit, as they will be on every machine, in every language, every time.

That is the first real lesson of this course. Seconds are a fact about one run, on one
machine, on one afternoon. Counts are a fact about the code. Only one of those two things
is worth writing down, and it is the one nobody thinks to measure.

---

## 6. What it costs

Count it out from the code in front of you, rather than trusting anybody, including this
document.

**The one-loop shape.** `for x in items:` runs the body once per item. Nothing is nested
inside it. With 5,000 items the hot line runs 5,000 times. Now give it a name: if there
are `n` items, the hot line runs `n` times. That is a straight line. Double the input, and
you double the work.

**The nested shape.** The outer loop runs `n` times. For each of those runs, the inner
loop runs somewhere between `n - 1` and 0 times, which averages out at about `n / 2`. So
the hot line runs roughly `n × n / 2` times. Check that against the measurement: at
n = 5,000 it predicts 5,000 × 5,000 / 2 = 12,500,000, and the program actually reported
12,497,500. That is close enough to trust the reasoning.

The exact count is `n × (n − 1) / 2`, which is simply the upper triangle of the grid.

**The thing to remember about the nested shape.** Because there is an `n` on both sides of
the multiplication, doubling `n` multiplies the work by four, not by two. From the numbers
above: 10,000 items would be about 50,000,000 comparisons, and 20,000 items about
200,000,000. Two hundred million really is four times fifty million.

**Space.** Neither function stores anything that grows with the input. `sum_all` keeps one
running `total`. `has_duplicate` keeps two positions, `i` and `j`. Whether you hand it ten
items or ten million, the extra memory is the same three or four values. This is the
cheapest kind of function to run, and we treat it properly on
[day 007](../day-007-space-complexity/README.md).

**And the big light.** The nested run at n = 5,000 took 1,785 ms. Buy a machine twice as
fast and it takes about 890 ms, which is a real improvement — once. Now let the input grow
to 10,000, and even on the fast machine you are back to roughly 3,600 ms. The faster
machine bought you exactly one doubling. Changing the shape buys you all of them.

Tomorrow, on [day 002](../day-002-counting-steps/README.md), you count these steps exactly
instead of roughly. On [day 003](../day-003-big-o-in-plain-english/README.md) you get the
shorthand that lets you say all of this in three characters.

---

## 7. The traps

### Trap one: the loop that is hiding

This is the near-miss, and it catches almost everyone. Look at this function and count the
loops.

```python
def looks_like_one_loop(items: list[int]) -> bool:
    seen = []
    for x in items:
        if x in seen:          # one line... or is it?
            return True
        seen.append(x)
    return False
```

There is one `for` on the page, so this must be the one-loop shape. It is not.

`x in seen` is not a single step. To decide whether `x` is in `seen`, the computer walks
`seen` from the beginning, comparing as it goes, until it either finds `x` or runs out of
list. That is a loop. Python has simply written it for you and hidden it behind two
characters.

So the real shape is an outer loop over `items`, and inside it a hidden loop over `seen`,
which gets longer on every pass. That is the nested shape wearing a disguise.

Here is the same function, measured, on the input that exposes it — a list with no
duplicates at all, so `x in seen` never finds a match and always scans the whole thing:

```
n=1000           8.12 ms
n=5000         240.40 ms
n=10000        921.72 ms
n=20000       4279.55 ms
```

Going from 10,000 to 20,000 is one doubling of the input. Going from 921 ms to 4,279 ms is
four and a half times the work. Four, not two. It is the grid again.

**The rule to carry forward:** a line is only one step if you can describe what it does
without using the word "every". "Check every item in `seen`" contains a loop. So does
`sorted()`, so does `max()`, so does `sum()`, so does `"".join()`, and so does copying a
list with `[:]`. When you are counting work in an interview, read every line and ask:
*does this single line touch every item?*

### Trap two: the off-by-one that ends the interview

Now the mistake people make while writing the nested loop under pressure. The inner loop
must start at `i + 1`, so that each pair is checked once. Here is what happens when the
`+ 1` gets attached to the wrong thing:

```python
def has_duplicate(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j + 1]:     # should be items[j]
                return True
    return False

print(has_duplicate([4, 9, 2, 9, 7]))
```

It looks right. `j` starts one ahead of `i`, and the `+ 1` reads as though it belongs
there. It even runs correctly for the first several comparisons. Then `j` reaches the last
position, `j + 1` points one past the end of the list, and this happens:

```
Traceback (most recent call last):
  File "d1a.py", line 8, in <module>
    print(has_duplicate([4, 9, 2, 9, 7]))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d1a.py", line 4, in has_duplicate
    if items[i] == items[j + 1]:     # should be items[j]
                   ~~~~~^^^^^^^
IndexError: list index out of range
```

`IndexError: list index out of range` is Python telling you that you asked for a position
the list does not have. A list of five values has positions 0, 1, 2, 3 and 4. There is no
position 5. The `~~~~~^^^^^^^` marks under the code point at exactly which part of the line
went wrong, which is genuinely useful and which most people never notice.

The fix is to decide the offset once, in the loop header, and never adjust it again inside
the body. `range(i + 1, len(items))` already guarantees that `j` is ahead of `i`. Adding
another `+ 1` inside does the same job twice.

---

## 8. In the interview

### How it gets asked

- *"Walk me through what this function does."* — the warm-up. They are watching whether
  you read the code or skim it.
- *"Which line runs the most times?"* — the direct version.
- *"Where's the bottleneck?"* or *"Why is this slow?"* — the same question wearing a
  work-experience costume. It usually arrives after you have written a working solution
  and they want to know whether you can see its cost.

### What to say out loud, in the first ninety seconds

Do not start guessing at a fix. Do this instead, in this order.

1. **Say what the function returns.** One sentence. *"This returns True if any value
   appears twice."* If you cannot say this, you have not read it yet.
2. **Find the loops, and say how deep they nest.** *"There's an outer loop over the list,
   and an inner loop over the rest of the list, so two levels."*
3. **Name the hot line.** Point at it. *"The comparison on line four is the deepest thing
   inside both loops, so it's the line that runs most."*
4. **Count it, roughly, out loud.** *"The outer loop runs n times, the inner one averages
   about n over two, so the comparison happens around n squared over two times."*
5. **Put a real number on it.** *"For a list of ten thousand, that's about fifty million
   comparisons."* This is the step that separates candidates. Everybody else stops at
   step 4.
6. **Then, and only then, offer a direction.** *"If we're allowed extra memory, there's a
   way to do this in one pass. Do you want me to go there?"*

### The follow-ups

**"Would a faster machine fix it?"**
No, and here is the arithmetic. A machine twice as fast halves the time once. But the work
grows four times every time the input doubles, so a single doubling of the data cancels
the new machine out completely. Faster hardware buys you a constant factor. The shape of
the growth is the thing you have to change.

**"Is `x in my_list` a single step?"**
No. It walks the list from the start until it finds `x` or reaches the end, so on a list of
length n it costs up to n steps. A single `for` loop with `x in seen` inside it is a
two-level shape, not a one-level shape. The same is true of `sorted`, `max`, `sum`, `join`,
and slicing a list.

**"How would you check your count instead of guessing?"**
Put a counter on the hot line, and print it for a few input sizes. If the input grows five
times and the counter grows twenty-five times, it is the nested shape. It takes two
minutes, and it turns an argument into a measurement.

### A model answer

The interviewer shows you `has_duplicate` and says, *"talk me through this"*. Here is what
a strong candidate actually says, more or less word for word:

> "So this returns True if the list has any value appearing more than once, and False
> otherwise.
>
> There are two loops. The outer one walks position `i` through the whole list. The inner
> one walks `j` from `i + 1` to the end, so it only ever looks at the items after `i`,
> which means each pair gets compared once instead of twice. That's the small optimisation
> in the loop header.
>
> The comparison inside both loops is the hot line. The outer loop runs n times, and the
> inner one averages about n over two, so that comparison happens roughly n squared over
> two times. Concretely, for ten thousand items that's about fifty million comparisons,
> which in Python is going to be seconds, not milliseconds.
>
> The thing I'd flag is that it's the shape, not the constant. If I double the list to
> twenty thousand, the work goes up four times, not two. So tuning the comparison, or
> running it on a faster box, doesn't really help. I'd want to change the approach if this
> is on a hot path.
>
> Space is fine, though. It only holds two positions, so it doesn't grow with the input at
> all. Do you want me to look at trading some memory for speed here?"

Notice what that answer does. It reads the code, finds the hot line, counts it, puts a real
number on it, separates the constant from the shape, mentions memory, and hands control
back. That is the whole performance, and it takes about forty seconds.

---

## 9. Recall card

1. Time is **how many instructions run**, not how many lines you wrote.
2. The **hot line** is the deepest line inside the most loops. Find it first, always.
3. One loop over n items means the hot line runs **n** times. Double the input, double the
   work.
4. Two nested loops over n items means roughly **n × n** times. Double the input, and you
   get **four times** the work.
5. A line that touches every item is a hidden loop: `x in list`, `sorted`, `max`, `sum`,
   `join`, `list[:]`.
