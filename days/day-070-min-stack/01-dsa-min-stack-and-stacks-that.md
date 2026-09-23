---
day: 70
track: dsa
title: "Min stack, and stacks that carry extra state"
phase: "Stacks and queues"
status: written
---

# Day 070 · DSA — Min stack, and stacks that carry extra state

**After today you can:** You can get the minimum of a stack in O(1) and explain the two standard tricks.

**The interviewer asks it as:** *Design a stack that returns its minimum in constant time.*

---

## 1. What this is, and why they ask it

Build a stack with the usual `push`, `pop` and `top`, plus a fourth operation `get_min` that returns
the smallest element currently in it — and all four must be O(1). The obvious implementation of
`get_min` scans the stack, which is O(n). The question is how to remove that scan.

The answer is one idea, and it is worth more than the problem: **a stack can carry extra state
computed at push time, because the LIFO discipline means popping automatically restores whatever was
true before.** You do not have to recompute the minimum on a pop; the answer that was correct before
that element arrived is sitting one level down, exactly where you left it. Nothing else in the phase
has this property — you could not do it with a queue, or an array you delete from the middle of.

They ask it because it is a design question disguised as a data-structure question, it has two
genuinely different standard answers, and it has a duplicate-handling bug that catches most people
the first time. It is also one of the few problems where an interviewer can reasonably ask "now do it
in O(1) extra space" and there is a real, clever answer — which they will not expect you to derive,
but will be pleased if you know exists.

---

## 2. The story

Nirmala's hardware shop in Hubli has a storeroom with one narrow wall where the boxes go, stacked,
because there is no room to put them side by side.

The boxes are all different weights. Hinges are heavy, switches are light, and a box of PVC fittings
weighs almost nothing. The rule is simply that the last one in is the first one out, because there is
nowhere else for it to go.

The thing she needs to know several times a day is which is the lightest box in the pile. There is a
boy with a cycle who does the local deliveries, and he can carry one box if it is light enough.

For a long time this meant a stool and going through the pile, which on a bad day is fourteen boxes.

Her nephew fixed it with a piece of chalk, and it took him about two minutes to explain.

When a box goes on the pile, before she lets go of it, she writes one number on its side. Not its own
weight — she writes **the weight of the lightest box in the pile now that this one is on it**. So if
the lightest so far was four kilos and the new box is seven, she writes four. If the new box is two,
she writes two.

Now, whenever she wants the answer, she reads the chalk mark on the top box. That is it. One glance,
whatever the pile is.

And the part that makes it work is what happens when a box comes off. She works nothing out. The box
underneath already has the right number chalked on it, because that number was written when the pile
was exactly what it is about to become again. The answer for the smaller pile was recorded when the
pile *was* that size, and it has sat there ever since.

There was one problem in the first week, because he had been slightly too clever. He had told her to
only chalk a box when it was lighter than the current lightest. Which is fine until two boxes weigh
the same. Two boxes of three kilos went on, only the first got a mark, and when the second came off
she was reading a mark that no longer applied to anything.

Now she chalks every single box, and the pile is never wrong.

---

## 3. The idea in plain English

The chalk mark is **extra state carried per element**, and the whole trick is *when* it is computed:
**at push time, never at pop time.**

Read the property that makes it work, because it is the sentence to say in an interview:

> **The minimum of a stack depends only on what is in it. A stack only ever changes at the top. So
> the minimum that was correct before you pushed is exactly the minimum that becomes correct again
> when you pop — and it is already recorded one level down.**

That is why `pop` does no work. It is not that you recompute the minimum quickly; it is that you
never recompute it at all.

### Approach one — store pairs

Each entry on the stack is not a value but a pair: the value, and the minimum of everything from the
bottom up to and including it.

```python
self._stack: list[tuple[int, int]] = []

def push(self, value: int) -> None:
    current_min = value if not self._stack else min(value, self._stack[-1][1])
    self._stack.append((value, current_min))

def get_min(self) -> int:
    return self._stack[-1][1]
```

Four lines. `get_min` reads the top and is obviously O(1). `pop` is `self._stack.pop()` unchanged,
because the pair below already carries the right answer.

This is Nirmala's chalk mark, exactly. It is the version to write first: it is the shortest, it is
the hardest to get wrong, and its correctness argument is one sentence.

### Approach two — a second stack

Keep the values in one stack and the running minimums in another.

```python
self._values: list[int] = []
self._mins: list[int] = []

def push(self, value: int) -> None:
    self._values.append(value)
    self._mins.append(value if not self._mins else min(value, self._mins[-1]))
```

Same information, laid out differently. `pop` pops both; `get_min` reads `self._mins[-1]`.

The reason this version exists is that it invites an optimisation, and the optimisation is where the
bug lives.

### The optimisation, and the bug

If the new value is not smaller than the current minimum, why record anything? Only push onto the min
stack when the value is a new minimum:

```python
    if not self._mins or value < self._mins[-1]:     # BUG
        self._mins.append(value)
```

and on pop, only pop the min stack if the value leaving is the current minimum:

```python
    value = self._values.pop()
    if value == self._mins[-1]:
        self._mins.pop()
```

This saves memory when the values are mostly increasing. And it is wrong, for exactly Nirmala's
reason.

```
 push 3    values [3]      mins [3]
 push 3    values [3,3]    mins [3]      <- second 3 not recorded (3 < 3 is False)
 pop       values [3]      mins [ ]      <- 3 == 3, so the min stack is emptied
 get_min   -> IndexError, or a wrong answer
```

There is still a 3 in the stack and no record of it. The fix is one character:

```python
    if not self._mins or value <= self._mins[-1]:    # <= not <
```

With `<=`, every duplicate minimum gets its own entry, so every pop that removes a minimum removes
exactly one record. **This is the trap of the problem**, and volunteering it before the interviewer
constructs `[3, 3]` is one of the best things you can do in this question.

### Which one to write

Write the pairs version. Then say the second-stack version exists, and that its optimised form has
the duplicate bug and needs `<=`. That sequence — simplest first, then the variant, then the trap —
is a better answer than writing the clever one and getting it right.

### The O(1) extra space version, which you should know about and not write

There is a way to keep only a single `min` variable and no per-element state. Instead of storing the
value, store an encoded number when a new minimum arrives:

```python
def push(self, value: int) -> None:
    if not self._stack:
        self._stack.append(value)
        self._min = value
    elif value >= self._min:
        self._stack.append(value)
    else:
        self._stack.append(2 * value - self._min)    # encoded, and < value
        self._min = value
```

On pop, if the stored number is less than `self._min`, it is an encoded marker, and the previous
minimum is recovered as `2 * self._min - stored`.

It works. It is also arithmetic that can overflow in a fixed-width language, it makes `top()` need
its own special case, and it takes five minutes to explain. **Mention it, do not write it**, unless
the interviewer explicitly asks for O(1) extra space — and then say the overflow caveat as you go.

### The general idea, which is the transferable part

The min stack is one instance of a family:

| You want | What each element carries |
|---|---|
| minimum in O(1) | the min from the bottom to here |
| maximum in O(1) | the max from the bottom to here |
| running sum | the sum from the bottom to here |
| average | sum and count |
| "the largest so far in this bracket" | whatever the aggregate is |

The condition is the one that makes it work: **the aggregate must be computable from the new element
and the previous aggregate alone.** Minimum, maximum, sum, count and product all satisfy that.
Median does not — you cannot get the median of a set from the new element and the old median — and
that is why "design a stack with O(1) median" is a genuinely harder problem needing two heaps.

Saying *why* it works, and naming the one that does not, is the difference between having memorised
this problem and understanding it.

---

## 4. The picture

The pairs version, filling and emptying. Each cell shows `value | min-up-to-here`.

```
 push 5      push 3      push 7      push 3      pop         pop
                                     +-------+
                         +-------+   | 3 | 3 |   +-------+
             +-------+   | 7 | 3 |   | 7 | 3 |   | 7 | 3 |   +-------+
 +-------+   | 3 | 3 |   | 3 | 3 |   | 3 | 3 |   | 3 | 3 |   | 3 | 3 |
 | 5 | 5 |   | 5 | 5 |   | 5 | 5 |   | 5 | 5 |   | 5 | 5 |   | 5 | 5 |
 +-------+   +-------+   +-------+   +-------+   +-------+   +-------+
 min = 5     min = 3     min = 3     min = 3     min = 3     min = 3
```

What to notice: `get_min` always reads the second number in the top cell, and `pop` never computes
anything. The two pops at the end restore `min = 3` for free, because the cell underneath was
written when the pile was that shape.

Now the two-stack version with the buggy `<`, on the input that kills it:

```
                push 3        push 3        pop           get_min
 values         [ 3 ]         [ 3, 3 ]      [ 3 ]         [ 3 ]
 mins           [ 3 ]         [ 3 ]         [ ]           [ ]
                              ^^^^^^        ^^^^          ^^^^^
                        3 < 3 is False,   3 == 3, so    a 3 is still
                        so nothing        the record    in the stack
                        recorded          is removed    with no record
```

And with `<=`:

```
                push 3        push 3        pop           get_min
 values         [ 3 ]         [ 3, 3 ]      [ 3 ]         [ 3 ]
 mins           [ 3 ]         [ 3, 3 ]      [ 3 ]         -> 3   correct
```

One character. Two entries instead of one. That is the whole fix.

---

## 5. The code, built step by step

### Step 1 — the naive version, so the problem is visible

```python
class SlowMinStack:
    def __init__(self) -> None:
        self._stack: list[int] = []

    def push(self, value: int) -> None:
        self._stack.append(value)

    def get_min(self) -> int:
        return min(self._stack)       # O(n) — this is the thing to remove
```

Write this and say the complexity out loud: "push and pop are O(1), `get_min` is O(n) because it
reads everything. The question is how to make that constant."

### Step 2 — the observation

Say it before you write the fix, because the code is obvious once the sentence is said.

"The minimum only changes at the top. When I push, the new minimum is the smaller of the new value
and the old minimum — one comparison. When I pop, the minimum goes back to whatever it was before
that push. So if I record the answer at push time, popping restores it for free."

### Step 3 — the pairs version

```python
    def push(self, value: int) -> None:
        current_min = value if not self._stack else min(value, self._stack[-1][1])
        self._stack.append((value, current_min))
```

The `if not self._stack` handles the first push, where there is no previous minimum to compare
against. `self._stack[-1][1]` is the min recorded on the current top.

```python
    def get_min(self) -> int:
        return self._stack[-1][1]
```

One indexing operation. No loop, no comparison, no state to maintain.

### Step 4 — the guards

Every method that touches the top must handle the empty case, and the message should mention a stack:

```python
    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()[0]      # [0] — return the value, not the pair
```

The `[0]` matters. `self._stack.pop()` gives back the tuple, and returning the tuple to a caller who
pushed an integer is a bug that type checking would catch and a quick interview would not.

### The complete solution

```python
class MinStack:
    """A stack whose minimum is available in O(1).

    Each entry carries the minimum of everything from the bottom up to and
    including itself, computed at push time. Because a stack only changes at
    the top, popping restores the previous minimum with no work at all.

    All four operations are O(1). Space is O(n) — two integers per element.
    """

    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []      # (value, min so far)

    def push(self, value: int) -> None:
        current_min = value if not self._stack else min(value, self._stack[-1][1])
        self._stack.append((value, current_min))

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()[0]                  # the value, not the pair

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top of empty stack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        if not self._stack:
            raise IndexError("min of empty stack")
        return self._stack[-1][1]

    def __len__(self) -> int:
        return len(self._stack)


class TwoStackMinStack:
    """The other standard answer: values in one stack, minimums in another.

    The `<=` is load-bearing. With `<`, two equal minimums share one record,
    and popping one of them removes the record for both.
    """

    def __init__(self) -> None:
        self._values: list[int] = []
        self._mins: list[int] = []

    def push(self, value: int) -> None:
        self._values.append(value)
        if not self._mins or value <= self._mins[-1]:      # <= NOT <
            self._mins.append(value)

    def pop(self) -> int:
        if not self._values:
            raise IndexError("pop from empty stack")
        value = self._values.pop()
        if self._mins and value == self._mins[-1]:
            self._mins.pop()
        return value

    def top(self) -> int:
        return self._values[-1]

    def get_min(self) -> int:
        if not self._mins:
            raise IndexError("min of empty stack")
        return self._mins[-1]


class MaxStack:
    """Same idea, one comparison flipped — the transferable part."""

    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, value: int) -> None:
        current_max = value if not self._stack else max(value, self._stack[-1][1])
        self._stack.append((value, current_max))

    def pop(self) -> int:
        return self._stack.pop()[0]

    def get_max(self) -> int:
        return self._stack[-1][1]


class SumStack:
    """The aggregate does not have to be an extreme. Sum works because the new
    sum is computable from the new value and the previous sum alone."""

    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, value: int) -> None:
        previous = 0 if not self._stack else self._stack[-1][1]
        self._stack.append((value, previous + value))

    def pop(self) -> int:
        return self._stack.pop()[0]

    def total(self) -> int:
        return 0 if not self._stack else self._stack[-1][1]


if __name__ == "__main__":
    stack = MinStack()
    for value in (5, 3, 7, 3):
        stack.push(value)
    print(stack.get_min(), stack.top())        # 3 3
    print(stack.pop(), stack.get_min())        # 3 3
    print(stack.pop(), stack.get_min())        # 7 3
    print(stack.pop(), stack.get_min())        # 3 5

    # The duplicate case, on the version that has the trap.
    two = TwoStackMinStack()
    two.push(3); two.push(3)
    print(two.pop(), two.get_min())            # 3 3   — correct because of <=

    max_stack = MaxStack()
    for value in (2, 9, 4):
        max_stack.push(value)
    print(max_stack.get_max())                 # 9

    sums = SumStack()
    for value in (5, 3, 7):
        sums.push(value)
    print(sums.total())                        # 15
    sums.pop()
    print(sums.total())                        # 8
```

Run the `[3, 3]` case on both implementations. On the pairs version it cannot go wrong, which is a
real reason to prefer it.

---

## 6. What it costs

### Time

```
 push     1 comparison + 1 append        O(1)
 pop      1 pop                          O(1)
 top      1 index                        O(1)
 get_min  1 index                        O(1)
```

Say what changed and why: `get_min` went from O(n) to O(1) because the work moved to `push`, where it
is one comparison instead of a scan. **You did not make anything faster; you moved the cost to a
place where it is constant.** That sentence is worth saying.

### Space

**Pairs version:** two integers per element, so `2n` — O(n), and precisely twice the naive stack.

**Two-stack version, unoptimised:** also `2n`, identical.

**Two-stack version with the `<=` optimisation:**

```
 values increasing  [1,2,3,...,n]     mins holds 1 entry     total ~n
 values decreasing  [n,...,3,2,1]     mins holds n entries   total 2n
 all equal          [3,3,3,...,3]     mins holds n entries   total 2n
```

Best case n, worst case 2n. So the optimisation saves up to half the extra memory on friendly inputs
and nothing on hostile ones. **On a decreasing sequence it saves nothing at all**, which is worth
knowing before you claim it as an improvement.

**The encoded version:** one integer per element plus one variable — O(n) total, O(1) *extra*. That
is the only version that is genuinely O(1) extra space, and it pays for it in overflow risk and
readability.

### Compared with recomputing

At n = 10,000 with 10,000 `get_min` calls:

```
 naive:   10,000 calls x 10,000 elements = 100,000,000 comparisons
 O(1):    10,000 calls x 1               =      10,000 reads
```

**Ten thousand times less work**, for the cost of one extra integer per element.

### The condition for the whole technique

An aggregate can be carried this way when it is computable from `(new element, previous aggregate)`
in O(1).

```
 min, max, sum, count, product     yes — one operation each
 median                            NO  — needs the whole multiset
 k-th smallest                     NO
 mode (most frequent)              NO  — needs all counts
```

Median needs two heaps and O(log n) per operation. Naming that as the boundary is what shows you
understand the technique rather than the problem.

---

## 7. The traps

### Trap 1 — `<` instead of `<=` in the optimised two-stack version

The one this problem is famous for.

```python
    if not self._mins or value < self._mins[-1]:     # BUG
```

Input: `push(3)`, `push(3)`, `pop()`, `get_min()`.

```
IndexError: list index out of range
```

or, in a version with more elements underneath, a silently wrong minimum. The fix is `<=`, and the
matching `pop` must use `==` so it removes exactly one record.

### Trap 2 — returning the pair instead of the value

```python
    def pop(self) -> int:
        return self._stack.pop()          # returns (7, 3), not 7
```

The caller pushed integers and gets tuples back. `top()` has the same trap. Both need the `[0]`.

### Trap 3 — recomputing the minimum on pop

```python
    def pop(self) -> int:
        value = self._stack.pop()
        self._min = min(self._stack) if self._stack else None    # O(n)
        return value
```

This is correct and it is O(n) on every pop, which is exactly what you were asked to avoid. It is a
natural thing to write if you have not said the observation out loud first, which is why saying it
first matters.

### Trap 4 — one `self._min` variable and nothing else

```python
    def push(self, value):
        self._min = min(self._min, value)      # correct
    def pop(self):
        ...                                    # and now what?
```

Push is easy; pop is impossible. There is no way to recover the previous minimum from a single
variable, because the information was overwritten. This is the honest reason the problem needs
per-element state, and the encoded version is precisely a trick for smuggling that state into the
values themselves.

### Trap 5 — the empty stack

```python
>>> MinStack().get_min()
IndexError: list index out of range
```

Every one of the four operations needs an empty guard. Interviewers ask "what does `get_min` return
on an empty stack?" and the right answer is a question back: "should it raise, or return `None`? I
would raise, because there is no sensible minimum of nothing, and returning `None` makes every caller
handle it."

### Trap 6 — assuming the optimisation always saves memory

"I only push when it is a new minimum, so it uses less space" — true on `[1,2,3,...]` and false on
`[n,...,2,1]`, where every element is a new minimum and the min stack is exactly as long as the
values. Quote the worst case, not the best.

### Trap 7 — overflow in the encoded version

`2 * value - self._min` can exceed the range of a fixed-width integer when the values are near the
limits. Python integers are arbitrary precision so it is safe there, but in Java or C++ it needs
`long` and a caveat. If you mention the trick, mention this in the same breath.

---

## 8. In the interview

### How it gets asked

- *"Design a stack that supports push, pop, top and retrieving the minimum element, all in constant
  time."* LeetCode 155, almost word for word.
- The immediate variant: *"now the maximum"* — one comparison flipped, and they are checking whether
  you understood or memorised.
- The space pivot: *"can you do it with O(1) extra space?"* — the encoded trick.
- The boundary probe: *"what about the median in O(1)?"* — the answer is no, and why.
- The harder relative, asked at senior level: *Max Frequency Stack* (LeetCode 895), which is the same
  "carry extra state" idea with a map of stacks.

### What to say out loud, in the first ninety seconds

1. **State the naive version and its cost.** "Push and pop are already O(1). `get_min` scanning the
   stack is O(n), so that is the thing to remove."
2. **Say the observation before the code.** "A stack only changes at the top, and the minimum depends
   only on what is in it. So the minimum before a push is exactly the minimum after the matching pop
   — I can record it on the way in and never recompute it."
3. **Write the pairs version.** Four lines, and say "each entry carries the minimum from the bottom
   up to itself."
4. **Give the second approach and its trap, unprompted.** "The other standard answer is two stacks.
   There is an optimisation where you only push a new minimum, and it has a duplicates bug — with
   `<` instead of `<=`, two equal minimums share one record and popping one removes both. I would use
   `<=`."
5. **State the cost.** "All four operations O(1). Space is 2n, which is twice the plain stack. If you
   want O(1) extra space there is an encoding trick — I can describe it, and I would flag that it can
   overflow in a fixed-width language."

### The follow-ups

**"Why does pop not need to recompute the minimum?"**
"Because the answer was already computed when the pile was that shape. The entry underneath the one I
am removing carries the minimum of everything from the bottom up to itself, and once the top is gone,
that is exactly the whole stack. The LIFO discipline is what guarantees it — I only ever remove the
most recent thing, so I only ever return to a state I have already been in and recorded."

**"Can you do it in O(1) extra space?"**
"Yes, with an encoding. When a new minimum arrives I push `2 * value - min` instead of the value,
which is provably smaller than the new minimum, and I update `min`. On pop, anything smaller than the
current minimum is a marker, and the previous minimum is `2 * min - stored`. It works and I would
raise two concerns: it can overflow in Java or C++ so it needs a wider type, and `top()` now needs a
special case. Unless space is genuinely the constraint, I would take the extra n integers."

**"Now do maximum instead."**
"One comparison flipped — `max` instead of `min` at push time. Nothing else changes, which is the
sign that the technique is about carrying an aggregate, not about minimums."

**"What about the median in O(1)?"**
"No, and the reason is the interesting part. This technique works only when the aggregate is
computable from the new element and the previous aggregate alone. Min, max, sum, count and product
all are. Median is not — the median of a set cannot be derived from the old median plus one new
value. That needs two heaps, a max-heap of the lower half and a min-heap of the upper half, giving
O(log n) per operation rather than O(1)."

**"Does the two-stack optimisation actually save memory?"**
"Sometimes. On an increasing sequence the min stack holds one entry, so it is about n total. On a
decreasing sequence every element is a new minimum, so it holds n entries and saves nothing — same
2n as the pairs version. Best case n, worst case 2n. I would not claim it as an improvement without
saying which input I am assuming."

### A model answer

Asked: *design a stack that returns its minimum in constant time.*

> "Push, pop and top are already constant on a normal stack. The one that is not is the minimum —
> scanning is O(n) — so that is the operation to fix.
>
> The observation that makes it work is about the shape of a stack rather than about minimums. A
> stack only ever changes at the top, and the minimum depends only on what is currently in it. So the
> minimum that was correct just before I pushed something is exactly the minimum that becomes correct
> again the moment I pop it. That means I do not have to recompute anything on the way out — I only
> have to record the answer on the way in.
>
> So each entry on my stack is a pair: the value, and the minimum of everything from the bottom up to
> and including that value. On push I compare the new value with the minimum recorded on the current
> top, which is one comparison. On pop I just pop the pair, and the pair underneath already carries
> the right answer. `get_min` reads the second half of the top entry.
>
> All four operations are O(1). Space is two integers per element, so 2n — twice a plain stack. I
> have not made anything faster; I have moved the work from `get_min`, where it was a scan, to
> `push`, where it is one comparison.
>
> There is a second standard answer worth mentioning: keep the values in one stack and the minimums
> in a parallel stack. Same information. The reason people prefer it is an optimisation — only push
> onto the min stack when the value is a new minimum — and that optimisation has the bug this
> question is really about. If the condition is strictly less-than, then pushing 3 and then 3 records
> only one minimum, and popping one of them deletes the record while a 3 is still in the stack. The
> fix is less-than-or-equal, so every duplicate gets its own record. I would also note that the
> optimisation saves nothing on a decreasing sequence, where every element is a new minimum.
>
> If you want O(1) extra space there is an encoding trick — push `2*value - min` when a new minimum
> arrives, and recover the previous minimum arithmetically on pop. It works; I would flag that it can
> overflow in a fixed-width language and that `top()` needs a special case.
>
> And the general form is worth stating: this works for any aggregate computable from the new element
> and the previous aggregate in constant time. Min, max, sum, count, product — all fine. Median is
> not, because you cannot derive a median from the old median and one new value, and that is why the
> median version needs two heaps and O(log n)."

---

## 9. Recall card

- **The observation, not the code, is the answer:** a stack only changes at the top, so **the minimum
  before a push is exactly the minimum after the matching pop** — record it on the way in and never
  recompute it. `pop` does no work at all.
- **Write the pairs version:** each entry is `(value, min from the bottom to here)`; push does one
  comparison against `stack[-1][1]`; `get_min` is one index. Four operations, all **O(1)**; space
  **2n**. Remember the `[0]` in `pop` and `top`, or you hand the caller a tuple.
- **The two-stack variant's optimisation has the famous bug: `<` must be `<=`.** `push(3), push(3),
  pop(), get_min()` loses the record while a 3 is still in the stack. And the optimisation saves
  **nothing** on a decreasing sequence — best case n, worst case 2n.
- **O(1) extra space exists: push `2*value - min` on a new minimum, recover with `2*min - stored`.**
  Mention it, do not write it — it **overflows** in fixed-width languages and forces a special case in
  `top()`.
- **The transferable rule: you can carry any aggregate computable from `(new element, previous
  aggregate)` in O(1)** — min, max, sum, count, product. **Median cannot** (needs two heaps, O(log
  n)), and naming that boundary is what shows understanding rather than memorisation. At n = 10,000
  with 10,000 queries this is 10⁸ comparisons versus 10⁴ reads.
