---
day: 3
track: dsa
title: "Big-O in plain English"
phase: "Foundations: how code costs"
status: written
---

# Day 003 · DSA — Big-O in plain English

**After today you can:** You can say O(n), O(n log n) or O(n^2) about your own code and defend the answer.

**The interviewer asks it as:** *What is the time complexity of your solution?*

---

## 1. What this is, and why they ask it

**Big-O** is a way of describing how the cost of your code grows when the input gets
bigger. It throws away every detail that does not change as the input grows — the exact
number of steps, how fast your laptop is, whether one line takes two nanoseconds or
twenty — and keeps only the **shape** of the growth.

Yesterday you counted steps exactly: `n × (n − 1) / 2`, or 499,500 at n = 1,000. Today you
take that exact count and reduce it to one short phrase, **O(n²)**, which is the phrase the
interviewer is waiting to hear.

This is the single most-asked question in a coding interview. It comes after every solution
you write, in almost every round, at almost every company. "What's the time complexity?" is
the standard closing move, and it is usually followed by "can you do better?", which really
means "you have just told me O(n²) and I want O(n log n)". Getting the notation wrong makes
a correct solution look like a lucky one. Getting it right, with the counting behind it,
makes a merely good solution look deliberate.

---

## 2. The story

Meena teaches maths to Class 9 at a school in Pune. There are forty students in her
section, and on Friday afternoon she takes in their test sheets.

Marking them is a job she knows exactly. Each sheet takes her about four minutes. Forty
sheets at four minutes each is a hundred and sixty minutes — under three hours, spread
across the weekend. She has been doing this since 2009 and the sum has never once surprised
her.

On Monday the head of department stops her outside the staff room with a different job. Two
of the sheets have the same wrong working in question six, word for word. He wants the
whole set checked for copying.

Meena says yes, and then, walking down the corridor, works out what she has just agreed to.
Checking for copying is not one look at each sheet. It is holding one sheet against
another. The first one has to go against every other one, which is thirty-nine comparisons.
The second goes against the ones she has not already done, which is thirty-eight. And so
on, all the way down. She adds it up before she reaches the stairs: seven hundred and
eighty pairs. At even one minute a pair, that is thirteen hours.

The first job grew with the size of the pile. The second job grew with the pile multiplied
by itself, and that turns out to be a completely different animal.

Farid, who teaches the other section, offers to take half. Farid is genuinely quicker than
her — about thirty seconds a pair, half her time. Meena is grateful, and also clear-eyed
about it. Half of thirteen hours is six and a half hours. Being twice as fast did not change
the job. It only moved it.

Then she remembers that the school is opening a second section in June. Eighty students
instead of forty. She does that sum standing on the stairs. The marking goes from three
hours to six, which doubles, and that feels fair. The copying check goes from seven hundred
and eighty pairs to three thousand one hundred and sixty. Twice the students, four times
the work.

She turns round and goes back to ask the head for a different way of finding copies.

---

## 3. The idea in plain English

Meena worked out three things on those stairs, and all three of them are what Big-O is.

She saw that **two jobs on the same pile can grow at different speeds**. She saw that
**being twice as fast did not help**, because the shape stayed the same. And she saw that
**doubling the input did not double the second job** — it quadrupled it.

Big-O is the notation for exactly those three observations. Let us build it.

### It starts with the exact count

You already know how to get the exact count. From [day 002](../day-002-counting-steps/README.md):

| Code shape | Exact count at size `n` |
|---|---|
| One loop | `n` |
| Two loops, one after the other | `2n` |
| Nested loops, inner from 0 | `n × n` |
| Nested loops, inner from `i + 1` | `n × (n − 1) / 2` |
| Halving each pass | about `log₂ n` |

Big-O does not replace this. It is a summary of it. You must still be able to produce the
exact count, because that is what you say when the interviewer asks "why?".

### Then you throw two things away

**Throw away constant multipliers.** `2n` becomes `O(n)`. `n × (n − 1) / 2`, which is
really `n²/2 − n/2`, becomes `O(n²)`. Farid being twice as fast is a constant multiplier of
one half, and it did not rescue Meena's weekend.

**Throw away everything except the fastest-growing term.** If a function costs
`n² + 500n + 10,000`, that is `O(n²)`. The `500n` and the `10,000` look enormous at first —
at n = 10 they are 5,000 and 10,000 against a mere 100. But at n = 100,000 the `n²` term is
ten billion, and the other two together come to barely fifty million, which is half of one
percent of the total. The biggest term wins, and it wins by more and more as `n` grows.

That is the whole mechanical rule: **drop the constants, keep the biggest term.**

### What is actually left

What is left is the **shape** — the answer to "if I double the input, what happens to the
time?".

| Big-O | Name | Double the input and the time... | Example |
|---|---|---|---|
| `O(1)` | constant | does not change | reading `items[5]` |
| `O(log n)` | logarithmic | goes up by one step | halving until you reach 1 |
| `O(n)` | linear | doubles | one loop over the list |
| `O(n log n)` | linearithmic | slightly more than doubles | sorting |
| `O(n²)` | quadratic | goes up **four** times | every pair, like Meena's check |
| `O(2ⁿ)` | exponential | **squares** — it is over | every subset of a set |

Read the third column downwards. That column is the answer to almost every "and if the
input were bigger?" question you will ever be asked.

### Saying it out loud

`O(n)` is spoken "oh of n", or "order n", or just "linear". `O(n²)` is "oh of n squared", or
"quadratic". `O(n log n)` is "n log n" — nobody says "n logarithm n". `O(1)` is "constant
time", and it does not mean fast. It means **the cost does not depend on the input size**.
Reaching for one item in a list of ten million is `O(1)`, and so is a fixed calculation that
takes a whole millisecond.

### The word "worst"

`O(n)` on its own means the **worst case**, unless somebody says otherwise. If you search a
list of n items for a value, the best case is one step and the worst case is n steps, and
the complexity you quote is `O(n)`.

You will meet two more words later, and they are worth naming now so that they are not a
surprise. **Average case** is the cost over typical inputs. **Amortised** cost is the average
per operation over a long run of them, which is what makes Python's `list.append` cheap on
[day 005](../day-005-python-lists-and-tuples/README.md). For today, worst case is the
default, and it is the right default.

---

## 4. The picture

Here is what the shapes actually do, at four input sizes.

```
                     n = 10      n = 100        n = 1,000       n = 1,000,000
 O(1)                   1            1                  1                   1
 O(log n)               3            7                 10                  20
 O(n)                  10          100              1,000           1,000,000
 O(n log n)            33          664              9,966          19,931,569
 O(n^2)               100       10,000          1,000,000   1,000,000,000,000
 O(2^n)             1,024   1.3 x 10^30            forever             forever
```

**What to notice:** at n = 10 every row is small, and the differences look academic — 1
against 100 is nothing you would ever feel. At n = 1,000,000, `O(log n)` is twenty steps and
`O(n²)` is a trillion. **The shapes only separate when the input is large, which is exactly
where interview questions live.**

Now the same thing as curves, so the growth is visible rather than tabulated:

```
  steps
    ^
    |                                          .   O(n^2)
    |                                        .
    |                                      .
    |                                    .
    |                                  .           ______ O(n log n)
    |                                .      ______/
    |                             .  ______/
    |                         .   __/                   ______ O(n)
    |                    .   _/    _____________________/
    |               .    __/______/
    |          .    __/_/                    ___________________ O(log n)
    |     .   _/___/______________________--/
    |__.__/__/____-------------------------------------------- O(1)
    +--------------------------------------------------------> n
```

**What to notice:** `O(n²)` starts *below* `O(n log n)` for tiny inputs and then leaves it
far behind. Big-O is a statement about the right-hand side of this chart, not the left. That
is precisely why constants get dropped — a constant shifts a curve up or down a little, and
it never changes which curve ends up on top.

And here is Meena's pile, drawn as the pairs she has to check when there are six sheets:

```
          sheet: 0    1    2    3    4    5
                 |    |    |    |    |    |
        0 -------+----X----X----X----X----X     5 comparisons
        1 ------------+----X----X----X----X     4
        2 -----------------+----X----X----X     3
        3 ----------------------+----X----X     2
        4 ---------------------------+----X     1
        5 --------------------------------+     0
                                              ----
                                                15  = 6 x 5 / 2
```

**What to notice:** the X marks form a triangle, which is half of the six-by-six square. Half
is a constant factor, so the triangle and the square are both `O(n²)`. The picture is
different. The shape is the same.

---

## 5. The code, built step by step

The way to make Big-O stop being notation is to measure it. Write each shape, count its
steps, then **double the input and look at the ratio**. The ratio is the shape.

Start with constant time.

```python
def constant(items: list[int]) -> int:
    """Look at one item. The list could hold a billion; this does not care."""
    if not items:
        return 0
    return items[0]
```

There is no loop. The body does the same work for a list of 10 and a list of 10 million.
That is `O(1)`. Note that `items[0]` really is one step —
[day 009](../day-009-what-an-array-is/README.md) explains why reaching into the middle of a
list is not a search.

Now linear time.

```python
def linear(items: list[int]) -> int:
    total = 0
    for x in items:
        total += x
    return total
```

The body runs once per item, so the count is exactly `n`. That is `O(n)`. Double the list
and the work doubles.

Now the case people get wrong.

```python
def also_linear(items: list[int]) -> int:
    total = 0
    for x in items:
        total += x
    for x in items:
        total += x
    return total
```

Two loops, one after the other, so the count is `2n`. The constant 2 is dropped, and this is
still `O(n)`. **Two loops side by side do not make a quadratic.** Only nesting does.

Now quadratic time.

```python
def quadratic(items: list[int]) -> int:
    pairs = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                pairs += 1
    return pairs
```

This is Meena's copying check. The exact count is `n × (n − 1) / 2`. Drop the `/ 2` and the
`− 1`, and it is `O(n²)`.

Now logarithmic time.

```python
def logarithmic(n: int) -> int:
    steps = 0
    while n > 1:
        n = n // 2
        steps += 1
    return steps
```

Each pass throws away half of what is left, so the count is about `log₂ n`. That is
`O(log n)`. Notice that nobody writes the base. Changing the base only multiplies by a
constant, and constants are dropped, so `log₂ n` and `log₁₀ n` are both just `O(log n)`.

And the one that ends careers.

```python
def exponential(n: int) -> int:
    """Every way of choosing yes-or-no, n times over."""
    if n == 0:
        return 1
    return exponential(n - 1) + exponential(n - 1)
```

Each call makes two more calls, one level down. That is 2 calls, then 4, then 8. The count
is `2ⁿ`. At n = 40 that is a trillion calls, and the function will not finish today.

Here is the complete program. It runs each shape at four sizes and — this is the part that
matters — prints the **ratio** between one size and the next.

```python
"""Day 3 — measure the shape by doubling the input and reading the ratio."""


def constant(n: int) -> int:
    """O(1): one step, whatever n is."""
    return 1


def logarithmic(n: int) -> int:
    """O(log n): halve until nothing is left."""
    steps = 0
    size = n
    while size > 1:
        size //= 2
        steps += 1
    return steps


def linear(n: int) -> int:
    """O(n): one pass."""
    steps = 0
    for _i in range(n):
        steps += 1
    return steps


def linearithmic(n: int) -> int:
    """O(n log n): one full pass for each halving level."""
    steps = 0
    size = n
    while size > 1:
        for _i in range(n):     # one full pass...
            steps += 1
        size //= 2              # ...once per level
    return steps


def quadratic(n: int) -> int:
    """O(n^2): every pair."""
    steps = 0
    for i in range(n):
        for _j in range(i + 1, n):
            steps += 1
    return steps


SHAPES = [
    ("O(1)", constant),
    ("O(log n)", logarithmic),
    ("O(n)", linear),
    ("O(n log n)", linearithmic),
    ("O(n^2)", quadratic),
]

if __name__ == "__main__":
    sizes = (250, 500, 1000, 2000)
    header = "".join(f"{'n=' + str(s):>14}" for s in sizes)
    print(f"{'shape':<14}{header}{'  ratio when n doubles'}")
    print("-" * (14 + 14 * len(sizes) + 24))
    for name, fn in SHAPES:
        counts = [fn(s) for s in sizes]
        cells = "".join(f"{c:>14,}" for c in counts)
        ratios = [counts[i + 1] / counts[i] for i in range(len(counts) - 1)]
        average = sum(ratios) / len(ratios)
        print(f"{name:<14}{cells}{average:>18.2f} x")
```

This is exactly what it printed:

```
shape                  n=250         n=500        n=1000        n=2000  ratio when n doubles
----------------------------------------------------------------------------------------------
O(1)                       1             1             1             1              1.00 x
O(log n)                   7             8             9            10              1.13 x
O(n)                     250           500         1,000         2,000              2.00 x
O(n log n)             1,750         4,000         9,000        20,000              2.25 x
O(n^2)                31,125       124,750       499,500     1,999,000              4.00 x
```

**The last column is the whole lesson.** You do not need to recognise the code. Double the
input, look at what happens to the work, and the shape names itself:

- stays the same → `O(1)`
- goes up by a small fixed amount → `O(log n)`
- doubles → `O(n)`
- a bit more than doubles → `O(n log n)`
- quadruples → `O(n²)`
- squares → `O(2ⁿ)`

That is a test you can run on your own code in ten seconds, and it is how you check an
answer you are not sure about.

---

## 6. What it costs

Big-O is itself a cost statement, so this section does the arithmetic that turns the
notation into a decision.

**The rule of thumb that decides interview answers.** A modern machine does very roughly
**10⁸ simple operations per second** in Python — a hundred million. That single number,
combined with the constraint printed at the bottom of the problem, tells you what you are
allowed to write.

| Constraint on n | Steps you can afford | Shapes that fit |
|---|---|---|
| n ≤ 10 | anything | even `O(n!)` |
| n ≤ 25 | ~3 × 10⁷ | `O(2ⁿ)` |
| n ≤ 5,000 | 2.5 × 10⁷ | `O(n²)` |
| n ≤ 10⁵ | 1.7 × 10⁶ for `n log n` | `O(n log n)`, `O(n)` |
| n ≤ 10⁶ | 10⁶ | `O(n)`, `O(log n)` |
| n ≤ 10⁹ | you cannot even read the input | `O(log n)`, `O(1)` |

Work through the row that matters most. The constraint says `n ≤ 100,000`, which is by far
the most common one on LeetCode. An `O(n²)` solution does:

```
100,000 x 100,000 = 10,000,000,000 operations
10,000,000,000 / 100,000,000 per second = 100 seconds
```

The time limit is usually one or two seconds. So `O(n²)` fails by a factor of about fifty,
and it fails *no matter how clean the code is*. Now the same input with `O(n log n)`:

```
log2(100,000) is about 17
100,000 x 17 = 1,700,000 operations
1,700,000 / 100,000,000 = 0.017 seconds
```

Seventeen milliseconds against a hundred seconds. **The constraint told you which shape to
write before you had even read the problem statement properly.** That is a habit worth
building now, and [day 004](../day-004-the-growth-curves/README.md) drills it.

**Constants are dropped, and constants are still real.** `O(n)` with a heavy body can be
slower than `O(n log n)` with a light one, at the input sizes you actually have. Big-O does
not lie about this; it simply is not answering that question. It answers "what happens as n
grows", and it stops being the right tool when n is small and fixed. An interviewer who
says "in practice the constant matters here" is not correcting you. They are agreeing with
you and adding to it.

**Space has a Big-O too, and it is a separate answer.** `quadratic` above keeps one integer
no matter how long the list is, so its extra space is `O(1)` even though its time is
`O(n²)`. Never let one number stand in for both.
[Day 007](../day-007-space-complexity/README.md) does space properly.

---

## 7. The traps

### Trap one: the loop that hides another loop

Here is a function that removes duplicates. It has one loop. Almost everyone calls it
`O(n)`.

```python
def dedupe(items: list[int]) -> list[int]:
    seen = []
    out = []
    for x in items:
        if x not in seen:      # <- this line is a loop
            seen.append(x)
            out.append(x)
    return out
```

`x not in seen` is not one step. For a **list**, Python has to walk `seen` from the start
until it finds `x` or runs out. That costs as much as `seen` is long — and `seen` grows as
the outer loop goes on.

So the outer loop runs n times, and the hidden inner walk costs 0, then 1, then 2, and on up.
That is the staircase from day 002 again: `n × (n − 1) / 2`, which is `O(n²)`.

Measure it and the deception is obvious:

```
n = 20,000 all distinct
  dedupe with a list : 3.58 s
  dedupe with a set  : 0.0056 s
  ratio              : 636 x
```

The fix is one word:

```python
def dedupe(items: list[int]) -> list[int]:
    seen = set()               # a set, not a list
    out = []
    for x in items:
        if x not in seen:      # O(1) for a set
            seen.add(x)
            out.append(x)
    return out
```

`x in some_set` is `O(1)`. `x in some_list` is `O(n)`. They are spelled identically, they
read identically out loud, and one of them is six hundred times slower here — and the gap
widens with `n`, because one is linear and one is quadratic.
[Day 006](../day-006-python-strings-dicts-sets/README.md) is entirely about this.

**How to catch it every time:** when you state a complexity, put a finger on every line
inside the loop and ask "is this really one step?". `in`, `.index()`, `.count()`, `min()`,
`max()`, `sum()`, `sorted()`, slicing and string concatenation are all loops wearing a short
name.

### Trap two: what a quadratic submission actually looks like

Nothing crashes. There is no error message telling you that you chose the wrong shape. This
is what LeetCode returns instead:

```
Time Limit Exceeded

Last executed input:
  nums = [7,4,9,2,8,1,...]  (100000 elements)
```

And this is what it looks like when you run it yourself and give up waiting:

```
^CTraceback (most recent call last):
  File "slow.py", line 12, in <module>
    print(count_pairs(list(range(200000))))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "slow.py", line 6, in count_pairs
    for j in range(i + 1, len(items)):
KeyboardInterrupt
```

Read that traceback carefully, because it is a useful thing rather than a failure. The `^C`
is you pressing Ctrl+C. Python then shows the exact line it was standing on when you
interrupted it, and that line is the inner loop header. **The interpreter has just pointed
at your quadratic.** When something is taking too long and you do not know why, interrupt it
and read where it stops. That is the cheapest profiler there is.

**The habit that prevents both traps:** before you submit, read the constraint, multiply it
out, and compare against 10⁸. If the answer is bigger, you already know the verdict, and you
have not spent a submission finding out.

---

## 8. In the interview

### How it gets asked

- *"What's the time complexity of your solution?"* — after every single solution, in every
  round. This is not optional and it is not conversational.
- *"And the space complexity?"* — always the second half. Answer both without being asked
  twice.
- *"Can you do better?"* — means "your answer was O(n²) and there is an O(n log n) or an
  O(n)". It is a hint, not a criticism.
- *"What if n were a million?"* — asking you to substitute into your own formula and reach a
  conclusion out loud.

### What to say out loud, in the first ninety seconds

Do not open with the letter O. Open with the count, and let the notation be the summary.

1. **Name the loops.** *"There's an outer loop over the array and an inner loop from i plus
   one."*
2. **Give the exact count.** *"So the body runs n minus one times, then n minus two, and so
   on — that's n times n minus one, over two."*
3. **Then reduce it.** *"Dropping the constant and the lower term, that's O(n squared)."*
4. **Check every line inside the loop.** *"Everything in the body is O(1) — comparisons and
   an integer add, no slicing, no `in` on a list."* This sentence is the one that shows you
   are not reciting.
5. **Give the space separately.** *"Space is O(1) extra. I only keep a counter. The input
   itself is O(n), but I'm not counting that as extra."*
6. **Put a number on it.** *"With n up to a hundred thousand, that's ten to the ten
   operations, which won't pass. So I'd want to get this to O(n) with a hash set."*

Step 6 is what separates a candidate who knows the notation from one who uses it. You have
just answered the interviewer's next question before they asked it.

### The follow-ups

**"Why do you drop the constant?"**
Because it does not change what happens when the input grows. `n²/2` and `n²` both go up
four times when you double `n`. A constant shifts the curve; it does not bend it. It is also
why a colleague working twice as fast does not rescue a quadratic job — halving thirteen
hours still leaves six and a half. Constants matter in production, where you tune them, and
they do not matter for the question Big-O is answering.

**"Two loops, one after the other — is that O(n²)?"**
No. Sequential loops add, so it is `n + n = 2n`, which is `O(n)`. Only nesting multiplies.
You could put ten loops one after another and it would still be linear.

**"Is O(1) always faster than O(n)?"**
No, and this is worth answering precisely. `O(1)` means the cost does not depend on `n`, not
that the cost is small. A constant-time operation that takes a millisecond is slower than a
linear pass over five items. Big-O tells you how something scales, and for small fixed
inputs it can be the wrong question entirely.

**"You said the average case is O(n). What's the worst case?"**
Whenever the two differ, give both, and say which one you are quoting. Quicksort is
`O(n log n)` on average and `O(n²)` in the worst case. Hash lookups are `O(1)` on average
and `O(n)` if every key collides. Interviewers ask this to find out whether you know that
both numbers exist.

### A model answer

The interviewer has just watched the candidate write a nested loop that looks for a pair of
numbers summing to a target, and asks for the complexity.

> "The outer loop runs n times. For each of those, the inner loop runs from i plus one to n,
> so it's n minus one iterations on the first pass, n minus two on the second, down to zero
> on the last. Adding those up gives n times n minus one, over two.
>
> Dropping the one-half and the minus one, that's O(n squared) time. I want to check the
> body too — inside I've got an array index and an integer comparison, both O(1), so there's
> nothing hidden in there.
>
> Space is O(1) extra. I'm not allocating anything that grows with n. The input array is
> O(n), but that's given to me rather than something I create.
>
> Now, the constraint says n can be a hundred thousand. n squared is ten to the tenth, which
> is about a hundred seconds in Python against a one-second limit, so this will time out. I
> can get it to O(n) with a hash set — one pass, and for each element I check whether target
> minus that element is already in the set. Lookups are O(1) on average, so that's O(n) time
> and O(n) extra space.
>
> That trade is worth naming: I'm spending O(n) memory to remove a factor of n from the
> time. If memory were the constraint instead, and the array were sorted, I'd use two
> pointers from both ends and get O(n) time with O(1) space."

The last paragraph is what gets remembered. The candidate did not just improve the answer.
They named the resource they spent to do it, and gave the condition under which they would
choose differently.

---

## 9. Recall card

1. Big-O is the **shape of the growth**. Get the exact count first, then **drop the
   constants and keep the biggest term**. `n²/2 − n/2` is `O(n²)`.
2. The test that never fails: **double the input**. Same → `O(1)`. Plus one step →
   `O(log n)`. Doubles → `O(n)`. Quadruples → `O(n²)`.
3. **Nested loops multiply, sequential loops add.** Two loops in a row is `O(n)`, not
   `O(n²)`.
4. **Check every line inside the loop.** `x in a_list`, `.index()`, slicing and `sorted()`
   are loops in disguise. `x in a_set` is not.
5. Roughly **10⁸ operations per second**. So n ≤ 10⁵ rules out `O(n²)`, and the constraint
   printed in the problem tells you the shape before you start writing.
