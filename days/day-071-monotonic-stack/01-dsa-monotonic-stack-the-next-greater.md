---
day: 71
track: dsa
title: "Monotonic stack: the next greater element"
phase: "Stacks and queues"
status: written
---

# Day 071 · DSA — Monotonic stack: the next greater element

**After today you can:** You can solve the whole next-greater and next-smaller family in O(n).

**The interviewer asks it as:** *For every element, find the next greater element to its right.*

---

## 1. What this is, and why they ask it

A **monotonic stack** is a stack whose contents are always in order — either increasing or decreasing
from bottom to top. You keep it that way by popping anything that would break the order before you
push. That one discipline solves a whole family of questions in a single pass: for every element,
find the next greater element to its right, or the next smaller, or the previous greater, or the
previous smaller.

The idea that makes it work is worth having in one sentence: **the moment you pop something, you have
found its answer.** You are not scanning for answers; the answers fall out as a side effect of
keeping the stack ordered. And the elements sitting in the stack are exactly the ones whose answer is
still unknown.

They ask it because the brute force is obvious and quadratic, the linear solution is eight lines, and
the eight lines contain a `while` loop inside a `for` loop that is *not* quadratic — so you have to
be able to defend the complexity. That defence is the real question. It is also the gateway to a set
of problems that look nothing alike on the surface — daily temperatures, stock spans, trapping rain
water, largest rectangle in a histogram — and are all this one pattern.

---

## 2. The story

Chickpet is decorated for the festival every year, and the man who does the street of cloth shops is
called Nagesh.

The decoration is strings of small lights, and the rule was fixed forty years ago: from the top of
each shop's board, a string runs forward along the street to the top of the **first board taller than
it**. Shorter boards ahead do not count, or the string sags into the road.

The boards are all different heights — a small painted plank, or a great tin hoarding two storeys up.

Nagesh does it in one walk down the street, and he has done it this way for so long he does not think
about it.

He starts at the first shop, ties one end of a string to its board, and carries the loose end with
him. At the second shop, if that board is taller, he ties the end off there — that string is
finished. Then he ties a fresh string to the second shop's board and carries that end on.

Usually the next board is not taller. So he ties a new string to that shop as well, and now he walks
with two loose ends in his hand. Then three. On a stretch of small shops he can be carrying six or
seven ends bunched in his fist.

And then he reaches something big — the hoarding outside the sari shop, the tallest thing on the
street — and in twenty seconds he ties off every end he is holding, because that board is taller than
all of them. His hand is empty. He ties one new string there and walks on with one end.

The thing his nephew noticed is that the ends in his hand are always in a particular order without
him arranging them. The oldest one, at the bottom of the bunch, is from the tallest board, and each
one above it is from a shorter board than the one below. It cannot be otherwise — if a new board
were taller than one he is holding, he would have tied that one off instead of adding to the bunch.

At the end of the street he still holds four or five ends, from the boards that never found anything
taller ahead. Those get tied to the pole at the corner, which is what it is for.

---

## 3. The idea in plain English

The bunch of loose ends in Nagesh's hand is a **monotonic stack**. Each end is a shop whose answer —
"which is the next taller board?" — is **not yet known**. Tying an end off is finding that shop's
answer. And the ends left at the end of the street are the elements with no answer.

Three properties, and all three are things to say out loud.

**One: the stack holds exactly the unanswered elements.** Not a scratch space, not a buffer. Every
element in the stack is one whose next-greater is still unknown.

**Two: the stack is automatically ordered.** Nobody sorts it. It is decreasing from bottom to top
because anything that would break the order gets tied off — popped — before the new one is added.
That is what "monotonic" means, and it is a consequence of the algorithm rather than a rule you
enforce separately.

**Three: one arrival can answer many.** The big hoarding tied off seven strings at once. This is why
the inner loop is not a problem: those seven had each been pushed once, and now they are popped once.

### The eight lines

```python
def next_greater(numbers: list[int]) -> list[int]:
    answer = [-1] * len(numbers)          # -1 means "nothing taller ahead"
    stack: list[int] = []                 # indices of unanswered elements

    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            answer[stack.pop()] = value   # this element's answer is `value`
        stack.append(index)

    return answer
```

Read the `while` line as Nagesh: *while I am holding an end from a board shorter than this one, tie
it off.* Then push the current index, because this element's own answer is not yet known.

**Store indices, not values.** You need the index to write into `answer`, and if the question asks
"how many days until" rather than "what is", you need `index - stack.pop()`. Storing values throws
that away, and it is the first thing to change when the follow-up arrives.

### The four variants, and the one rule that generates them

The whole family is two knobs: which direction you walk, and which way the comparison points.

| You want | Walk | Pop while the top is |
|---|---|---|
| **next greater** to the right | left → right | **smaller** than current |
| **next smaller** to the right | left → right | **greater** than current |
| **previous greater** to the left | right → left | **smaller** than current |
| **previous smaller** to the left | right → left | **greater** than current |

The rule to memorise, because it generates all four:

> **Direction of the walk is opposite to the direction you are looking. Pop while the top is on the
> wrong side of the comparison you want.**

If you want the next greater *to the right*, you walk left to right, and each element's answer is
found by something that arrives later. So you walk forwards and look backwards into the stack.

The stack's order follows automatically: for "next greater", the stack ends up **decreasing** from
bottom to top. For "next smaller", **increasing**. You do not have to remember that — it falls out —
but stating it is a good check that your comparison is the right way round.

### Strict or not: the `<` versus `<=` question

`numbers[stack[-1]] < value` pops on strictly smaller, so equal elements stay in the stack, and an
element's answer must be *strictly* greater.

Change it to `<=` and equal elements pop each other, so an element's answer is the next
greater-*or-equal*. On `[2, 2, 3]`:

```
 with <   : answer for index 0 is 3   (skips the equal 2)
 with <=  : answer for index 0 is 2   (the equal one counts)
```

**Ask which the problem wants.** "Next greater" almost always means strictly greater, but "next day
at least as warm" does not, and getting it wrong is a one-character bug that passes half the tests.

### The leftovers

Whatever is still in the stack when the loop ends has no answer. Initialising `answer` to `-1` (or
`0` for "how many days") handles that with no extra code — Nagesh's pole at the corner.

If you prefer, push a sentinel of infinity at the end to force everything out, which is the trick
that makes [day 072](../day-072-largest-rectangle/README.md)'s histogram problem cleaner.

### Circular arrays

"Next greater element in a circular array" — after the last element you wrap round to the first. The
trick is to walk `2n` steps and use `index % n`:

```python
for step in range(2 * len(numbers)):
    index = step % len(numbers)
    while stack and numbers[stack[-1]] < numbers[index]:
        answer[stack.pop()] = numbers[index]
    if step < len(numbers):          # only push on the FIRST pass
        stack.append(index)
```

The `if step < len(numbers)` is the part people miss. On the second pass you only answer; you do not
add new unanswered elements, or they would never be resolved.

### The family this unlocks

- **Daily Temperatures** — next warmer day, answering with the *distance* rather than the value.
- **Stock Span** — previous greater, walking the other way.
- **Largest Rectangle in a Histogram** — for each bar, the previous smaller and the next smaller.
  That is [day 072](../day-072-largest-rectangle/README.md).
- **Trapping Rain Water** — the same stack, accumulating as it pops.
- **Remove K Digits / smallest subsequence** — a monotonic stack maintaining the smallest sequence.

Recognising the family is what the pattern is for. "For each element, the nearest element on one side
satisfying a comparison" is the trigger sentence.

---

## 4. The picture

`[2, 1, 2, 4, 3]`, finding the next greater to the right. The stack holds **indices**; the heights
underneath are the values there.

```
 i=0  v=2   stack empty            push 0        stack: [0]        (2)
 i=1  v=1   top is 2, not < 1      push 1        stack: [0,1]      (2,1)
 i=2  v=2   top is 1 < 2  -> pop 1, answer[1]=2
            top is 2, not < 2      push 2        stack: [0,2]      (2,2)
 i=3  v=4   top is 2 < 4  -> pop 2, answer[2]=4
            top is 2 < 4  -> pop 0, answer[0]=4
            stack empty            push 3        stack: [3]        (4)
 i=4  v=3   top is 4, not < 3      push 4        stack: [3,4]      (4,3)

 leftovers: indices 3 and 4 keep -1
 answer = [4, 2, 4, -1, -1]
```

What to notice at `i=3`: **one element answered two**. That is the hoarding tying off the bunch, and
it is the reason a `while` inside a `for` is still linear — those two pops correspond to two pushes
that already happened.

And the stack drawn as a bunch, so the ordering is visible:

```
        top ->  +-----+                 the values in the stack are
                |  1  |  index 1        always DECREASING from the
                +-----+                 bottom up, for next-greater.
                |  2  |  index 0
     bottom ->  +-----+                 Nothing sorted it. Anything that
                                        would have broken the order was
                                        popped before it could go on.
```

If your stack ever has a smaller value below a bigger one while solving next-greater, your comparison
is backwards.

---

## 5. The code, built step by step

### Step 1 — the brute force, said and not written

"For each element, walk right until I find something bigger." That is `n(n-1)/2` comparisons in the
worst case, which at n = 100,000 is five billion. Say the number and move on.

### Step 2 — the observation

Say this before writing anything, because it is the answer:

"When I am at element `i` and it is bigger than something I passed earlier, that earlier element's
answer is `i`. So I do not need to search forward from each element — I need to remember which
earlier elements are still waiting, and resolve them when something bigger arrives."

### Step 3 — the loop

```python
    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            answer[stack.pop()] = value
        stack.append(index)
```

Three lines, and the `while` before the `append` is the whole ordering discipline. Resolve everything
this element can resolve, *then* add yourself as unresolved.

Note `while stack and ...` — the same guard as every stack problem. Without it, the first element
raises `IndexError` when the stack is empty.

### Step 4 — the distance variant

Daily Temperatures asks *how many days until it is warmer*, not *what is the next warmer
temperature*. Only one line changes, and this is why you store indices:

```python
        while stack and temperatures[stack[-1]] < temperature:
            previous = stack.pop()
            answer[previous] = index - previous      # a distance, not a value
```

If you had stored values, this variant would be impossible without a second structure. **Always store
indices** and derive the value with `numbers[index]` when you need it.

### The complete solution

```python
def next_greater(numbers: list[int]) -> list[int]:
    """For each element, the next strictly greater element to its right,
    or -1 if there is none.

    The stack holds INDICES of elements whose answer is not yet known, and is
    kept decreasing by value from bottom to top. Each index is pushed once and
    popped at most once, so this is O(n) despite the inner while loop.
    """
    answer = [-1] * len(numbers)
    stack: list[int] = []                # indices, values decreasing bottom->top

    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            answer[stack.pop()] = value  # `value` is this element's next greater
        stack.append(index)              # its own answer is not known yet

    return answer                        # leftovers keep -1


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """How many days until a strictly warmer day. 0 if there is none.

    Identical to next_greater, except the answer is a DISTANCE — which is why
    the stack must hold indices rather than values.
    """
    answer = [0] * len(temperatures)
    stack: list[int] = []

    for index, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            previous = stack.pop()
            answer[previous] = index - previous
        stack.append(index)

    return answer


def next_smaller(numbers: list[int]) -> list[int]:
    """The next strictly smaller element to the right. One comparison flipped;
    the stack is now INCREASING from bottom to top."""
    answer = [-1] * len(numbers)
    stack: list[int] = []

    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] > value:
            answer[stack.pop()] = value
        stack.append(index)

    return answer


def previous_greater(numbers: list[int]) -> list[int]:
    """The previous strictly greater element to the LEFT. Same comparison as
    next_greater; the walk is reversed."""
    answer = [-1] * len(numbers)
    stack: list[int] = []

    for index in range(len(numbers) - 1, -1, -1):
        while stack and numbers[stack[-1]] < numbers[index]:
            answer[stack.pop()] = numbers[index]
        stack.append(index)

    return answer


def next_greater_circular(numbers: list[int]) -> list[int]:
    """Circular: after the last element, wrap round to the first.

    Walk 2n steps with index = step % n, but only PUSH on the first pass —
    otherwise the second pass adds elements that can never be resolved.
    """
    n = len(numbers)
    answer = [-1] * n
    stack: list[int] = []

    for step in range(2 * n):
        index = step % n
        while stack and numbers[stack[-1]] < numbers[index]:
            answer[stack.pop()] = numbers[index]
        if step < n:
            stack.append(index)

    return answer


def next_greater_or_equal(numbers: list[int]) -> list[int]:
    """The <= variant: an equal element counts as an answer.
    On [2, 2, 3] this gives 2 for index 0, where the strict version gives 3."""
    answer = [-1] * len(numbers)
    stack: list[int] = []

    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] <= value:      # <= not <
            answer[stack.pop()] = value
        stack.append(index)

    return answer


if __name__ == "__main__":
    print(next_greater([2, 1, 2, 4, 3]))          # [4, 2, 4, -1, -1]
    print(next_greater([5, 4, 3, 2, 1]))          # [-1, -1, -1, -1, -1]
    print(next_greater([1, 2, 3, 4, 5]))          # [2, 3, 4, 5, -1]
    print(next_greater([]))                       # []
    print(next_greater([7]))                      # [-1]
    print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    # [1, 1, 4, 2, 1, 1, 0, 0]
    print(next_smaller([4, 2, 5, 1]))             # [2, 1, 1, -1]
    print(previous_greater([2, 1, 2, 4, 3]))      # [-1, 2, -1, -1, 4]
    print(next_greater_circular([1, 2, 1]))       # [2, -1, 2]
    print(next_greater([2, 2, 3]))                # [3, 3, -1]
    print(next_greater_or_equal([2, 2, 3]))       # [2, 3, -1]
```

Run the last two lines together. The same input gives different answers, and knowing which one the
problem wants is a question, not a guess.

---

## 6. What it costs

### Time — and this is the whole interview

The code has a `while` inside a `for`, which looks quadratic and is not. Count it the right way.

The `for` loop runs `n` times, so there are exactly `n` pushes — one per element, and no element is
ever pushed twice.

The `while` loop only ever pops. **An element can be popped at most once, because once it is off the
stack it never goes back on.** So across the entire execution, the total number of pops is at most
`n`, however unevenly they are spread.

```
 pushes across the whole run:  exactly n
 pops   across the whole run:  at most  n
 -----------------------------------------
 total stack operations:       <= 2n     ->  O(n)
```

Say it exactly like this: **the inner loop is bounded in total, not per iteration.** One iteration
can do `n` pops — the sari shop hoarding — and that is fine, because those `n` pops used up all the
pops the rest of the run was going to do.

This is the same argument as the `while` loop in longest-consecutive from
[day 062](../day-062-sets/README.md), and it will keep being the argument for the rest of the stack
phase.

### Against the brute force

```
 brute force:  n(n-1)/2 comparisons
 monotonic:    <= 2n stack operations

 n = 100,000:  4,999,950,000  vs  200,000
 ratio:        about 25,000x
```

At n = 100,000 the brute force is roughly five billion operations — tens of seconds — and the
monotonic stack is two hundred thousand, which is a few milliseconds.

### Space

```
 answer array:  O(n)   — required, it is the output
 stack:         O(n)   worst case
```

The stack holds every element at once when nothing ever gets popped, which is a strictly decreasing
input like `[5, 4, 3, 2, 1]`. Best case is O(1): on `[1, 2, 3, 4, 5]` every element pops the previous
one immediately, so the stack never holds more than one.

Say both, and name the inputs. It takes five seconds and it is the difference between having thought
about it and having recited it.

### The circular version

`2n` steps, still at most `n` pushes and `n` pops, so still **O(n)** with a constant of two. Worth
stating, because "you loop twice, so it is O(n²)" is a thing interviewers say to see whether you will
agree with them.

---

## 7. The traps

### Trap 1 — storing values instead of indices

```python
    stack.append(value)                 # instead of index
```

Works for "what is the next greater". Fails completely for "how many days until", because you cannot
compute a distance without knowing where the element was. It also fails for the histogram problems,
where the width is the whole point. **Always store indices.** The only cost is writing
`numbers[stack[-1]]` instead of `stack[-1]`.

### Trap 2 — the missing emptiness guard

```python
        while numbers[stack[-1]] < value:      # no `stack and`
```

```
IndexError: list index out of range
```

Fires on the very first element, since the stack starts empty. Same guard as every stack problem in
this phase, and it must be the first half of the `and`.

### Trap 3 — pushing before popping

```python
        stack.append(index)
        while stack and numbers[stack[-1]] < value:     # WRONG ORDER
            answer[stack.pop()] = value
```

Now the element compares against itself. `numbers[index] < numbers[index]` is false, so it happens to
survive — but on the `<=` variant it pops itself and writes its own answer as its own value.
**Resolve first, then push.**

### Trap 4 — `<` when the problem wanted `<=`

```
 next_greater([2, 2, 3])          -> [3, 3, -1]
 next_greater_or_equal([2, 2, 3]) -> [2, 3, -1]
```

Both are correct programs. Only one answers the question you were asked. Read the problem statement
for the word "strictly", and if it is not there, ask.

### Trap 5 — the wrong comparison for the wrong variant

For **next smaller**, the comparison flips to `>` and the stack becomes increasing. People flip the
direction of the walk instead, which gives *previous* greater, and the answers look plausible on
symmetric inputs. The check: run it on `[4, 2, 5, 1]` and read the answer for index 0. Next smaller
gives 2; previous greater gives -1.

### Trap 6 — pushing on both passes of the circular version

```python
    for step in range(2 * n):
        index = step % n
        ...
        stack.append(index)          # WRONG — pushes again on the second pass
```

The second pass adds elements that nothing after them can resolve, so they sit in the stack forever
and some answers get overwritten with values from the wrong lap. Guard with `if step < n`.

### Trap 7 — forgetting the leftovers

If you build the answer by appending as you pop, the elements never popped are simply missing from
your output, and the list is shorter than the input. Pre-fill the answer array with the default and
write into it by index. Never append.

### Trap 8 — believing the interviewer when they call it quadratic

They will say "there is a loop inside a loop, so that is O(n²)". The answer is the counting argument,
stated confidently: n pushes total, at most n pops total, so at most 2n operations. Do not soften it.

---

## 8. In the interview

### How it gets asked

- The base case: *"For every element in this array, find the next greater element to its right.
  Return -1 if there is none."* LeetCode 496 and 503.
- The distance version, which is the most commonly asked: *"Given daily temperatures, return how many
  days you would have to wait for a warmer day."* LeetCode 739.
- Disguised: *"For each day, how many consecutive days before it had a price less than or equal to
  today's?"* — the Stock Span problem, which is previous-greater.
- The escalation: *"largest rectangle in a histogram"*, or *"trapping rain water"* — the same stack
  with more bookkeeping.

### What to say out loud, in the first ninety seconds

1. **State the brute force with a number and reject it.** "For each element, walk right until
   something is bigger. That is n squared over two — five billion at a hundred thousand elements."
2. **Say the observation, not the algorithm.** "When I am standing on an element that is bigger than
   things I passed, I have just found *their* answer. So instead of searching forward from each
   element, I remember which earlier elements are still waiting and resolve them when something
   bigger turns up."
3. **Say what is in the stack.** "The stack holds the indices of elements whose answer is still
   unknown, and it stays decreasing by value — not because I sort it, but because anything that would
   break the order gets popped first."
4. **Say indices, and why.** "I store indices, not values, because the follow-up is usually a
   distance."
5. **Pre-empt the complexity challenge.** "There is a `while` inside the `for` and it is still O(n):
   n pushes total, and each element is popped at most once, so at most 2n operations overall."

### The follow-ups

**"That is a loop inside a loop. Is it not O(n²)?"**
"No. Count the operations rather than the nesting. Every element is pushed exactly once, by the outer
loop. Every element is popped at most once, because once it leaves the stack it never returns. So the
total work across the whole run is at most 2n stack operations, however unevenly they are
distributed. One iteration might pop n elements, and that is fine — it has consumed all the pops the
rest of the run was going to do."

**"Now do it circularly."**
"Walk 2n steps with `index = step % n`, and only push during the first pass. If I push on the second
pass I add elements that nothing after them can resolve. Still O(n), with a constant factor of two."

**"What if I want the next smaller instead?"**
"Flip the comparison from `<` to `>`, and the stack becomes increasing rather than decreasing.
Nothing else changes. There are four variants from two knobs — which direction I walk, and which way
the comparison points — and they generate next greater, next smaller, previous greater and previous
smaller."

**"What does 'next greater' mean if there are duplicates?"**
"That is a question I would ask you. With a strict `<` in the pop condition, an equal element does
not count and `[2, 2, 3]` gives 3 for the first element. With `<=`, it does count and gives 2. Both
are one-character changes and only one matches the specification."

**"Where else does this pattern show up?"**
"Anywhere the question is 'for each element, the nearest element on one side satisfying a
comparison'. Daily temperatures is the distance version. Stock span is previous-greater. Largest
rectangle in a histogram needs the previous smaller and the next smaller for each bar, which is two
runs of this. Trapping rain water is the same stack accumulating water as it pops."

### A model answer

Asked: *for every element, find the next greater element to its right.*

> "The brute force is: for each element, walk right until I find something bigger. Worst case that is
> n squared over two — about five billion comparisons at a hundred thousand elements — so I want a
> single pass.
>
> Here is the observation that gives me one. When I am standing on an element and it is bigger than
> some elements I have already passed, I have just found *their* answers. So I should stop thinking
> of it as 'search forward from each element' and start thinking of it as 'remember which earlier
> elements are still waiting, and settle them when something big enough arrives'.
>
> That collection of waiting elements is a stack, and I store indices rather than values in it —
> because the standard follow-up is 'how many days until', and a distance needs the position.
>
> The loop is three lines. For each element: while the stack is not empty and the value at the top is
> less than the current value, pop it and record that its answer is the current value. Then push the
> current index, because its own answer is not known yet. Resolve first, then push — the other order
> makes an element compare against itself.
>
> The stack ends up decreasing from bottom to top, and I did not sort it. It has to be decreasing,
> because anything that would break the order is exactly the thing the `while` pops before pushing.
> That is what makes it a monotonic stack.
>
> Whatever is still in the stack at the end has no greater element to its right, so I pre-fill the
> answer array with -1 and only ever write into it by index — never append, or the unanswered
> elements just go missing.
>
> On complexity, since the shape looks quadratic: it is O(n). Every element is pushed exactly once by
> the outer loop, and popped at most once, because once it is off the stack it never goes back on. So
> the total number of stack operations across the whole run is at most 2n. One single iteration might
> pop a hundred thousand elements, and that is fine, because it has used up all the pops the rest of
> the run was going to do. The inner loop is bounded in total, not per iteration.
>
> Space is O(n) for the answer, which is the output, plus O(n) for the stack in the worst case — a
> strictly decreasing input, where nothing is ever popped. On a strictly increasing input the stack
> never holds more than one element.
>
> One thing I would check before writing: does 'greater' mean strictly greater? With duplicates,
> `[2, 2, 3]` gives 3 for the first element under a strict comparison and 2 under a non-strict one,
> and it is one character of difference."

---

## 9. Recall card

- **The stack holds exactly the elements whose answer is not yet known, and it stays ordered by
  itself** — anything that would break the order is popped before the new element goes on. **The
  moment you pop something, you have found its answer.**
- **Eight lines: `while stack and numbers[stack[-1]] < value: answer[stack.pop()] = value`, then
  `stack.append(index)`.** Resolve first, then push. **Store indices, never values** — the usual
  follow-up wants a *distance* (`index - stack.pop()`), and values cannot give you one.
- **Four variants from two knobs:** direction of the walk × direction of the comparison → next
  greater · next smaller · previous greater · previous smaller. Next-greater leaves the stack
  **decreasing** bottom-to-top; next-smaller **increasing**. And ask about duplicates: `<` gives
  strictly greater, `<=` gives greater-or-equal — on `[2, 2, 3]` that is 3 versus 2.
- **The complexity defence is the interview.** n pushes total, **each element popped at most once**,
  so ≤ 2n operations — **the inner loop is bounded in total, not per iteration.** One iteration
  popping n elements has consumed all the pops the rest of the run was going to do. 5 × 10⁹ vs 2 ×
  10⁵ at n = 100,000, about **25,000×**.
- **Space O(n) worst case** (a strictly decreasing input, nothing ever pops), **O(1) best case** (a
  strictly increasing one). **Pre-fill the answer array and write by index — never append**, or the
  leftovers vanish. Circular: walk `2n` with `step % n` and **push only on the first pass**. The
  family: daily temperatures · stock span · largest rectangle · trapping rain water.
