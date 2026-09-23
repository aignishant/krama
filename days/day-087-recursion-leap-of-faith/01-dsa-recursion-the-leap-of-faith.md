---
day: 87
track: dsa
title: "Recursion: the leap of faith"
phase: "Recursion and backtracking"
status: written
---

# Day 087 · DSA — Recursion: the leap of faith

**After today you can:** You can write a recursive function by trusting it on the smaller input.

**The interviewer asks it as:** *Solve this recursively. What is the base case?*

---

## 1. What this is, and why they ask it

A **recursive** function is one that calls itself. It solves a big problem by asking a smaller version
of itself for an answer and then doing one small piece of work with what comes back.

The mechanics are two lines. There is a **base case** — an input so small you can answer it without
asking anybody — and a **recursive case**, which asks the same function about something smaller and
combines the answer.

The difficulty is not the mechanics. It is that most people try to *trace* the recursion in their head:
this call makes that call, which makes that one, and by the fourth level they are lost. That is the
wrong way to think about it, and it is why recursion feels hard.

The right way is the **leap of faith**: assume the recursive call already works, on the smaller input,
and write the one line that uses its answer. You do not check. You do not trace. You trust it, exactly
the way you trust a library function you did not write.

They ask it because everything from here to the end of the course is recursive — backtracking, trees,
graphs, divide and conquer, dynamic programming — and because "what is the base case?" is a question
you will be asked in every one of those rounds. Getting comfortable with the leap of faith this week is
what makes the next sixty days possible.

---

## 2. The story

The ration shop opens at nine and by ten past eight the line already goes round the corner and along
the side of the school wall, and from where Murali is standing he cannot see the shop at all.

He wants to know how many people are ahead of him, because if it is more than about forty he will come
back after lunch.

He cannot count them. The line bends twice, there are people sitting on the step who may or may not be
in it, and walking to the front to count and coming back would lose him his place.

So he taps the shoulder of the woman in front of him and asks how many people are ahead of *her*.

She does not know either. She is in exactly the same position — she cannot see the front, and the line
bends. So she taps the man in front of her and asks him the same question.

He asks the person in front of him. And so on, all the way up the line and round the corner, one
shoulder at a time.

At the very front, right at the shutter, is an old man who has been there since half past seven. When
he is asked how many people are ahead of him, he does not have to ask anybody. He can see the shutter.
He says: none.

Then it comes back. The person behind him hears "none" and says "one" to the person behind her. She
hears nothing else and needs nothing else — she does not know or care how the number was arrived at.
She adds herself and passes it back. One becomes two, two becomes three, and about ninety seconds
later the woman in front of Murali turns round and says thirty-seven.

Murali adds one for her and knows he is thirty-eighth. He stays.

What he did not do, and this is the whole thing, is check her answer. He did not walk up the line to
verify that there really were thirty-seven people. He asked one person one question and trusted what
came back, and every single person in that line did exactly the same, and the answer was right.

---

## 3. The idea in plain English

Murali's question is the recursive call. The old man at the shutter is the base case. And nobody
checking anybody else's answer is the leap of faith.

### The three questions

Every recursive function you will ever write comes from answering these three, **in this order**:

**1. What is the smallest input I can answer without asking anybody?**
That is the base case. The old man who can see the shutter. If you cannot name it, you cannot write
the function.

**2. What is a smaller version of the same problem?**
Not a different problem — the *same* problem, on less. "How many are ahead of the person in front of
me" is the same question, one person shorter.

**3. Given the answer to that smaller problem, what one thing do I do to get mine?**
Add one. That is all Murali's neighbour did.

```python
def count_ahead(person):
    if person.is_at_the_front():        # 1. the base case
        return 0
    return 1 + count_ahead(person.in_front)   # 2. smaller, and 3. one small step
```

Three lines, and they are the three questions in order.

### The leap of faith

Here is the habit that makes recursion easy, and it is genuinely a habit rather than an insight.

**When you write the recursive call, assume it already works.** Do not trace it. Do not wonder what
happens three levels down. Treat `count_ahead(person.in_front)` as if it were a finished library
function written by somebody competent, which returns the correct answer for a shorter line.

Then your only job is the one line that uses it.

People fail at recursion because they try to hold the whole tree of calls in their head. Nobody can do
that past three levels, and you do not need to: **if the base case is right, and each call is on a
strictly smaller input, and your one line is right, then the whole thing is right.** Those three
conditions are all you have to check.

### Worked, four times, so the shape becomes familiar

**Sum a list.**

- Smallest input I can answer directly: the empty list. Sum is 0.
- Smaller version: the list without its first element.
- One small step: add the first element.

```python
def total(numbers: list[int]) -> int:
    if not numbers:
        return 0
    return numbers[0] + total(numbers[1:])
```

**Reverse a string.**

- Base case: a string of length 0 or 1 is its own reverse.
- Smaller: everything after the first character.
- One step: put the first character on the *end*.

```python
def reverse(text: str) -> str:
    if len(text) <= 1:
        return text
    return reverse(text[1:]) + text[0]
```

**Count the nodes in a linked list**, which ties this to the last eight days:

```python
def length(node) -> int:
    if node is None:                 # the base case is the end of the list
        return 0
    return 1 + length(node.next)     # exactly Murali's question
```

**Raise a number to a power.**

- Base case: anything to the power 0 is 1.
- Smaller: one less in the exponent.
- One step: multiply by the base.

```python
def power(base: int, exponent: int) -> int:
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)
```

Four functions, one shape. **Base case, smaller call, one small step.** If you can see that shape, you
can write the function without understanding what happens in the middle — and you are not supposed to
understand what happens in the middle.

### The two ways the base case goes wrong

**Missing.** The function never stops:

```
RecursionError: maximum recursion depth exceeded
```

**Unreachable**, which is worse because it looks correct. `total(numbers[2:])` skips a step, so an
odd-length list steps over the empty case and goes negative into an infinite loop of empty slices —
or, more commonly, `power(base, exponent - 2)` never lands on exactly 0 for an odd exponent.

**Every recursive call must make the input strictly smaller, and it must be able to reach the base
case.** Say both halves out loud when you write it. This is [day 089](../day-089-recursion-that-terminates/README.md)'s
whole subject.

### Recursion is not free

Every call in progress occupies a **stack frame** — a small block of memory holding its arguments and
where to return to. From [day 068](../day-068-stacks/README.md), that is a real stack, and Python's
limit is about a thousand frames:

```
RecursionError: maximum recursion depth exceeded
```

So `total` on a list of ten thousand numbers **crashes**, while the loop version does not. That is not
an edge case; ten thousand is a small list.

**Recursion costs O(depth) space, always.** A loop costs O(1). When the depth is `log n` — binary
search, merge sort — that is twenty frames at a million elements and nobody cares. When the depth is
`n`, it is a real limit.

### The one where recursion is a trap

```python
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Beautiful, correct, and **exponential**. Each call makes two more, so the number of calls roughly
doubles with every increase in `n`. `fib(40)` makes about 331 million calls and takes about thirteen seconds.
`fib(50)` would take about half an hour.

The reason is that the same subproblems are computed again and again — `fib(35)` is recomputed
millions of times. Two fixes, and both are worth knowing today:

```python
from functools import cache

@cache                                  # remember answers; now each n is computed once
def fib(n: int) -> int:
    return n if n <= 1 else fib(n - 1) + fib(n - 2)
```

One decorator turns 331 million calls into 41. That is **memoisation**, and it is the entire
foundation of dynamic programming later in the course.

Or write the loop, which is O(n) time and O(1) space and needs no stack at all.

**Fibonacci is the standard example of recursion and it is a bad one**, because it teaches the shape
while hiding the cost. Notice the difference: in `total` and `length`, each call makes **one** further
call — so the work is linear. In `fib`, each call makes **two** — so the work explodes. Counting the
calls per level is how you tell them apart, and it is [day 088](../day-088-the-call-stack/README.md)'s
material.

### Recursion and iteration are interchangeable

Anything recursive can be written with an explicit stack, and anything with a stack can be written
recursively — because the call stack *is* a stack. From day 068: a recursion that would blow the
thousand-frame limit becomes a loop with a list, limited only by memory.

So when do you choose recursion? **When the problem is defined recursively.** A tree is a node with
subtrees. A directory contains directories. Merge sort sorts two halves. Writing those iteratively
means managing a stack by hand, and the code is longer and worse. Writing `total` recursively, on the
other hand, is showing off — the loop is clearer and does not crash.

---

## 4. The picture

`total([4, 7, 2])`, drawn as the two journeys — down the line asking, and back up answering.

```
 GOING DOWN (each call asks a smaller question)

   total([4, 7, 2])
     |  4 + ?
     v
   total([7, 2])
     |  7 + ?
     v
   total([2])
     |  2 + ?
     v
   total([])          <- the base case. The old man at the shutter.
        returns 0

 COMING BACK UP (each call does its one small step)

   total([])   -> 0
   total([2])  -> 2 + 0  = 2
   total([7,2])-> 7 + 2  = 9
   total([4,7,2]) -> 4 + 9 = 13

 Nobody on the way down knew the answer.
 Nobody on the way up checked anybody else's.
```

What to notice: **the work happens on the way back up.** Going down, every call is suspended in the
middle of an addition, waiting. That waiting is what a stack frame is, and it is why depth costs
memory.

The shape of the three questions, as a template:

```
 def solve(problem):
     if <smallest case>:              # 1. What can I answer without asking?
         return <the direct answer>
     smaller = solve(<problem, but smaller>)     # 2. Ask, and TRUST the answer
     return <one small step involving `smaller`> # 3. My one piece of work
```

And the difference between linear and exponential recursion, which is the thing to be able to see:

```
 ONE call per level -> linear                TWO calls per level -> exponential

   total([4,7,2])                              fib(5)
        |                                     /      \
   total([7,2])                          fib(4)      fib(3)
        |                                /     \     /     \
   total([2])                        fib(3) fib(2) fib(2) fib(1)
        |                            /   \    ...    ...
   total([])                     fib(2) fib(1)

   3 calls for 3 elements                    15 calls for n = 5
   n calls for n elements                    ~2^n calls
                                             fib(40) ≈ 331,000,000 calls
```

Count the branches per call. **One branch is a line; two branches is a tree**, and a tree of depth `n`
has about 2ⁿ nodes.

---

## 5. The code, built step by step

### Step 1 — answer the three questions out loud, before typing

For "sum a list":

> "The smallest input I can answer without asking anybody is the empty list, and the answer is zero.
> A smaller version of the same problem is the list without its first element. And given the sum of
> that, my one step is to add the first element."

Three sentences, and the function is now written. Say them in the interview — it is the same move as
"say what the stack holds" in the last phase.

### Step 2 — write the base case first

```python
    if not numbers:
        return 0
```

**Always first, always at the top.** A function whose base case is buried below the recursive call has
already made the call before checking, which is an immediate `RecursionError`.

### Step 3 — write the recursive call, and do not think about it

```python
    return numbers[0] + total(numbers[1:])
```

`total(numbers[1:])` is *correct*. It returns the sum of the rest. You are not going to check that,
and looking inside it is the thing that makes recursion feel hard.

### Step 4 — check the three conditions, not the trace

1. Does the base case return the right answer? `total([])` is 0. Yes.
2. Is every recursive call on a **strictly smaller** input? `numbers[1:]` is one shorter. Yes.
3. Is the combining step right? Sum of the whole is the first plus the sum of the rest. Yes.

**Those three checks replace tracing.** If all three hold, the function is correct, and you never had
to imagine four levels of calls.

### Step 5 — the cost, from the recurrence

`total` makes one call per element, so `n` calls, each doing constant work — O(n) time. But
`numbers[1:]` **copies the list**, which is O(n) itself, so this particular version is secretly O(n²)
in time and O(n²) in total allocation.

The fix is to pass an index instead of slicing:

```python
def total(numbers: list[int], start: int = 0) -> int:
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start + 1)
```

**Slicing in a recursive call is the quiet performance bug of this phase**, and it is worth catching
now, because it will reappear in every string and array recursion for the next ten days.

### The complete solution

```python
from functools import cache


def total(numbers: list[int], start: int = 0) -> int:
    """Sum a list recursively.

    1. base case      : nothing left, the sum is 0
    2. smaller problem: the list from `start + 1` onwards
    3. one small step : add numbers[start]

    An INDEX, not a slice: `numbers[1:]` copies the list on every call, which
    turns an O(n) algorithm into O(n^2) time and allocation.

    O(n) time, O(n) stack — so it dies past ~1000 elements in Python. The loop
    version is strictly better; this exists to show the shape.
    """
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start + 1)


def reverse_string(text: str) -> str:
    """A string of 0 or 1 characters is its own reverse; otherwise put the
    first character behind the reverse of the rest.

    O(n) calls, but each `+` builds a new string, so O(n^2) total work — the
    same slicing trap in a different costume.
    """
    if len(text) <= 1:
        return text
    return reverse_string(text[1:]) + text[0]


def power(base: int, exponent: int) -> int:
    """base ** exponent, for exponent >= 0. O(exponent) calls."""
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)


def fast_power(base: int, exponent: int) -> int:
    """The same thing in O(log exponent) calls, by halving instead of decrementing.

    x^n = (x^(n/2))^2 for even n, and x * x^(n-1) for odd n. The recursive call
    is made ONCE and stored — calling it twice would make this exponential
    again, and that is a real mistake people make here.
    """
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)          # once, not twice
    return half * half if exponent % 2 == 0 else base * half * half


def count_nodes(node) -> int:
    """The linked list from the last phase, counted recursively.
    The base case is the end of the list — Murali's old man at the shutter."""
    if node is None:
        return 0
    return 1 + count_nodes(node.next)


def is_palindrome(text: str) -> bool:
    """Two characters at a time from the outside in.

    base case      : 0 or 1 characters left is a palindrome
    smaller problem: the string without its two ends
    one small step : the two ends must match
    """
    if len(text) <= 1:
        return True
    if text[0] != text[-1]:
        return False
    return is_palindrome(text[1:-1])


def fib_slow(n: int) -> int:
    """The classic example, and a BAD one. TWO recursive calls per level means
    about 2^n calls: fib(40) is roughly 331 million and takes about thirteen seconds."""
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)


@cache
def fib_fast(n: int) -> int:
    """The same function with one decorator. Each n is now computed once, so
    fib(40) is 41 calls instead of 331 million. This is memoisation, and it is
    the foundation of dynamic programming later in the course."""
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)


def fib_loop(n: int) -> int:
    """O(n) time, O(1) space, no stack at all. What you would actually ship."""
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def binary_search(numbers: list[int], target: int, low: int = 0, high: int | None = None) -> int:
    """Recursion where the DEPTH is log n, so the stack cost is irrelevant:
    about 20 frames at a million elements."""
    if high is None:
        high = len(numbers) - 1
    if low > high:
        return -1                                   # base case: nothing left
    middle = (low + high) // 2
    if numbers[middle] == target:
        return middle
    if numbers[middle] < target:
        return binary_search(numbers, target, middle + 1, high)
    return binary_search(numbers, target, low, middle - 1)


if __name__ == "__main__":
    import sys
    import time

    print(total([4, 7, 2]), total([]), total([5]))          # 13 0 5
    print(reverse_string("recursion"), reverse_string(""))  # noisrucer ''
    print(power(2, 10), power(7, 0))                        # 1024 1
    print(fast_power(2, 10), fast_power(3, 13))             # 1024 1594323
    print(is_palindrome("malayalam"), is_palindrome("recursion"))   # True False
    print(binary_search([1, 3, 5, 7, 9, 11], 9))            # 4
    print(binary_search([1, 3, 5, 7, 9, 11], 4))            # -1

    start = time.perf_counter()
    print(fib_slow(30), f"{time.perf_counter() - start:.3f}s")      # 832040
    start = time.perf_counter()
    print(fib_fast(30), f"{time.perf_counter() - start:.6f}s")      # 832040, ~0.000s
    print(fib_loop(30), fib_fast(90))                               # 832040 2880067194370816120

    print(sys.getrecursionlimit())                          # 1000
    try:
        total(list(range(5000)))
    except RecursionError as error:
        print(f"RecursionError: {error}")

    # the same input, iteratively, with no limit at all
    print(sum(range(5000)))                                 # 12497500
```

---

## 6. What it costs

### Time, read off the recurrence

**One recursive call per level** means the number of calls is the depth:

```
 total(n):    T(n) = T(n-1) + O(1)   ->  n calls        ->  O(n)
 power(n):    T(n) = T(n-1) + O(1)   ->  n calls        ->  O(n)
 fast_power:  T(n) = T(n/2) + O(1)   ->  log2(n) calls  ->  O(log n)
 binary_search: same shape           ->  O(log n)
```

**Two recursive calls per level** means the number of calls doubles each level:

```
 fib(n):      T(n) = T(n-1) + T(n-2) + O(1)  ->  about 2^n calls  ->  O(2^n)
```

```
 fib(30):        about 2.7 million calls     ~0.10 s   (measured)
 fib(40):        about 331 million calls     ~13 s     (123x the calls)
 fib(50):        about 4 x 10^10 calls       ~30 minutes
 fib(40), memoised:  41 calls                ~0.00002 s
```

**Count the recursive calls in the body.** One is a line, two is a tree, and the difference between
them is the difference between a tenth of a second and half an hour.

### Space, which is always the depth

```
 every call in progress = one stack frame
 stack frame in CPython ≈ 100-500 bytes depending on locals

 total(n):        depth n        -> O(n) space, crashes past ~1000
 fast_power(n):   depth log n    -> O(log n), about 20 frames at a million
 binary_search:   depth log n    -> irrelevant
 fib(n):          depth n        -> O(n), even though it makes 2^n calls
```

That last line is worth pausing on: **`fib` makes 2ⁿ calls but only ever has `n` of them on the stack
at once**, because it finishes the left branch before starting the right. Time and space complexity
are answering different questions, and this is the cleanest example of the difference.

### The recursion limit is a real limit

```
 sys.getrecursionlimit()  ->  1000
```

```
RecursionError: maximum recursion depth exceeded
```

on a list of five thousand. Not an exotic input — a small list. And `sys.setrecursionlimit(100000)` is
**not** a fix: it moves the failure from a clean Python exception to a segmentation fault when the C
stack runs out, which crashes the whole process with no traceback.

**The rule: recursion whose depth is `log n` is free. Recursion whose depth is `n` is a bug waiting for
a big input**, unless you know `n` is small.

### The slicing trap

```python
    return numbers[0] + total(numbers[1:])
```

```
 calls:        n
 work per call: O(n) to build the slice
 -------------------------------------
 total:        O(n^2) time AND O(n^2) allocation
```

At n = 1000 that is half a million element copies to add up a thousand numbers. Pass an index. The
same trap in strings — `text[1:]` — makes `reverse_string` quadratic, and it is the reason real string
recursions carry two indices.

### Against iteration

```
                     recursive        iterative
 sum a list          O(n) time        O(n) time
                     O(n) space       O(1) space
                     dies at ~1000    no limit

 fibonacci           O(2^n) naive     O(n) time, O(1) space
                     O(n) memoised

 binary search       O(log n) both, and the space difference is 20 frames
```

**Iteration wins whenever the depth is proportional to the input**, and it does not matter when the
depth is logarithmic. Recursion wins when the *problem* is recursive — trees, directories, divide and
conquer — where the iterative version means managing a stack by hand.

---

## 7. The traps

### Trap 1 — no base case

```python
def total(numbers):
    return numbers[0] + total(numbers[1:])      # nothing stops it
```

```
RecursionError: maximum recursion depth exceeded
```

The most common recursion bug, and the friendliest, because Python tells you exactly what happened.
**Write the base case first, at the top, before the recursive call.**

### Trap 2 — an unreachable base case

```python
def power(base, exponent):
    if exponent == 0:
        return 1
    return base * power(base, exponent - 2)     # steps over 0 on odd exponents
```

`power(2, 5)` goes 5, 3, 1, −1, −3, … and never equals 0. Same error, much harder to see, because the
base case is *there* — it just cannot be reached from every input.

**Say both halves out loud: the base case exists, and every input can reach it.** Guarding with
`if exponent <= 0` instead of `== 0` is a defensive fix that hides the real bug; fixing the step is the
right one.

### Trap 3 — forgetting to return the recursive call

```python
def total(numbers, start=0):
    if start == len(numbers):
        return 0
    numbers[start] + total(numbers, start + 1)  # computed, then thrown away
```

Returns `None` for any non-empty list, and then:

```
TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
```

one level up. **Every path through a recursive function must return something.** Reading the function
and checking that each branch has a `return` takes five seconds.

### Trap 4 — two recursive calls where one would do

```python
def fast_power(base, exponent):
    if exponent == 0:
        return 1
    if exponent % 2 == 0:
        return fast_power(base, exponent // 2) * fast_power(base, exponent // 2)
```

Correct, and **exponential** — it recomputes the same value twice at every level, which turns
O(log n) into O(n). Call it once, store it in a variable, use it twice. This is the same mistake as
naive Fibonacci and it is easy to make while writing a function specifically designed to be fast.

### Trap 5 — slicing in the recursive call

```python
    return numbers[0] + total(numbers[1:])
```

O(n²) time and allocation, silently. Pass an index or two indices. This is the quiet one — the function
is correct and just mysteriously slow on larger inputs.

### Trap 6 — a mutable default argument

```python
def collect(node, found=[]):                    # created ONCE, at definition time
    ...
```

The list is created once when the function is defined, not per call, so the second call to `collect`
sees everything the first one found. Use `None` and create it inside:

```python
def collect(node, found=None):
    if found is None:
        found = []
```

This bites hardest in recursion because helper functions with accumulators are so common here.

### Trap 7 — sharing mutable state across branches

```python
def subsets(items, index=0, current=[]):
    ...
    current.append(items[index])
    subsets(items, index + 1, current)          # the SAME list, mutated
    current.pop()                               # so it must be undone
```

Passing a mutable accumulator down is a real and standard technique — it is what backtracking is — but
every branch must leave it exactly as it found it. The missing `pop` is the defining bug of
[day 094](../day-094-backtracking/README.md), and it is worth knowing today that it is coming.

### Trap 8 — raising the recursion limit

```python
    sys.setrecursionlimit(1_000_000)            # do not
```

Python's limit exists to convert a C-stack overflow into a catchable exception. Raising it past what
the C stack can hold turns a clean `RecursionError` into a segmentation fault that kills the process
with no traceback. If the depth is genuinely large, convert to iteration with an explicit stack.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Solve this recursively."* Then, immediately: *"What is the base case?"*
- The conversion: *"Here is a loop. Write it recursively."* Or the reverse, which is more common in
  production work.
- The classic trap: *"Write Fibonacci recursively."* Followed by *"what is its complexity?"* and *"can
  you do better?"*
- The cost question: *"What does recursion cost that a loop does not?"* — they want stack depth.
- The design question: *"When would you choose recursion over a loop?"*

### What to say out loud, in the first ninety seconds

1. **Answer the three questions, aloud, before writing.** "The smallest input I can answer directly is
   X, and the answer is Y. A smaller version of the same problem is Z. And given that answer, my one
   step is W."
2. **Name the leap of faith explicitly.** "I am going to assume the recursive call works on the smaller
   input, and only write the line that uses it."
3. **Write the base case first**, at the top.
4. **Say the two termination conditions.** "The base case is reachable because every call reduces the
   input by exactly one, so it lands on zero."
5. **Give both complexities, and separate them.** "One recursive call per level and `n` levels, so O(n)
   time. And O(n) *stack* space, which matters — this dies at about a thousand elements in Python."
6. **Offer the iterative version if the depth is linear.** "For a list, I would actually write the loop
   — the recursion is O(n) stack for no benefit. I would use recursion where the problem is genuinely
   recursive, like a tree."

### The follow-ups

**"What is the base case?"**
"The smallest input I can answer without making another call. For summing a list it is the empty list,
which sums to zero. Two things have to be true about it: it must return the right answer, and every
input must be able to *reach* it. The second half is the one people miss — a function that steps by two
towards a base case of exactly zero never terminates on odd inputs, and the base case looks perfectly
correct while it happens."

**"What does recursion cost that a loop does not?"**
"Stack space, proportional to the depth. Every call in progress holds a frame with its arguments and
its return address, and they all coexist until the deepest one returns. In Python the limit is about a
thousand frames, so a recursion whose depth is the size of the input dies on a five-thousand-element
list — that is not an exotic input. When the depth is logarithmic, like binary search or merge sort,
it is about twenty frames at a million elements and nobody cares. So the rule I use: log-depth
recursion is free, linear-depth recursion is a bug waiting for a big input."

**"Write Fibonacci recursively. What is its complexity?"**
"It is three lines and it is exponential, and the reason is worth stating precisely: the body makes
**two** recursive calls, so the number of calls roughly doubles per level — about 2ⁿ. `fib(40)` is
around 331 million calls, about thirteen seconds. Compare with summing a list, where the body makes **one**
call and the work is linear. Counting the recursive calls in the body is how you tell those apart.
The fix is memoisation — one `@cache` decorator turns 331 million calls into 41, because each `n` is
computed once — and that is the foundation of dynamic programming. Or write the loop, which is O(n)
time and O(1) space."

**"When would you choose recursion over iteration?"**
"When the problem is defined recursively and the depth is bounded. A tree is a node with subtrees, a
directory contains directories, merge sort sorts two halves — writing those iteratively means managing
a stack by hand, and the code is longer and easier to get wrong. For a flat list I would write the
loop: the recursive version is O(n) stack for no gain and it crashes on real inputs. And anything
recursive *can* be converted, because the call stack is a stack — that is the escape hatch when the
depth is too large."

**"Your recursive version is slower than the loop even though both are O(n). Why?"**
"Two reasons, and one of them is usually a bug. Every call has overhead — building a frame, binding
arguments, returning — which is a real constant factor in Python. But the bug is usually slicing: if
the recursive call is `f(items[1:])`, each call copies the list, so an O(n) algorithm is secretly
O(n²) in both time and allocation. Passing an index instead of slicing fixes it, and the same trap
appears in every string recursion."

**"How would you make this work on a million elements?"**
"Convert it to a loop with an explicit stack, because the call stack is a stack — that transformation
always exists. I would not raise the recursion limit: Python's limit is there to turn a C-stack
overflow into a catchable exception, and raising it past what the C stack can hold gives a
segmentation fault instead, which kills the process with no traceback."

### A model answer

Asked: *sum the numbers in a list, recursively. What is the base case?*

> "Let me answer three questions before writing anything, because they are the function.
>
> First: what is the smallest input I can answer without asking anybody? The empty list. Its sum is
> zero. That is the base case.
>
> Second: what is a smaller version of the *same* problem? The list without its first element. Not a
> different question — the same question, one element shorter.
>
> Third: given the sum of that smaller list, what one thing do I do? Add the first element.
>
> So: if the list is empty, return zero; otherwise return the first element plus the sum of the rest.
> Three lines.
>
> The habit that makes this easy is the leap of faith. When I write the recursive call, I assume it
> already works — that it correctly returns the sum of the shorter list — and I only write the line
> that uses the answer. I do not trace it. Trying to hold four levels of calls in your head is what
> makes recursion feel hard, and it is unnecessary: if the base case is right, and every call is on a
> strictly smaller input, and my one combining step is right, then the whole function is right. Three
> checks instead of a trace.
>
> On the base case specifically, since you asked: two things have to be true, and people usually only
> say the first. It has to return the correct answer, and every input has to be able to *reach* it. If
> I stepped by two instead of one, an odd-length list would step straight over the empty case and
> recurse for ever — and the base case would still look perfectly correct while it happened.
>
> One implementation detail I would flag. I would pass an index rather than slicing, because
> `numbers[1:]` copies the list on every call, which turns this into O(n²) time and allocation. It is
> a quiet bug — the function is correct, just mysteriously slow on bigger inputs — and the same trap
> appears in every string recursion.
>
> Complexity: one recursive call per element, so n calls of constant work, O(n) time. And O(n) *stack*
> space, which is the part that matters. Python's recursion limit is about a thousand frames, so this
> raises `RecursionError` on a five-thousand-element list, which is not a large list.
>
> So honestly, for a flat list I would write the loop. The recursion is O(n) stack for no benefit. I
> would reach for recursion when the problem is genuinely recursive — a tree, a directory, merge sort
> — where the depth is logarithmic or the iterative version means managing a stack by hand."

---

## 9. Recall card

- **Three questions, in order, and they *are* the function.** *What is the smallest input I can answer
  without asking anybody?* (the base case) · *What is a smaller version of the **same** problem?* ·
  *Given that answer, what one small step gives me mine?* Write the base case **first, at the top**.
- **The leap of faith: assume the recursive call already works, and write only the line that uses it.**
  Do not trace it — nobody can hold four levels in their head. **Three checks replace tracing:** the
  base case returns the right answer · every call is on a **strictly smaller** input · the combining
  step is right.
- **A base case can be present and unreachable, which is the harder bug.** Stepping by two towards
  `== 0` never terminates on odd inputs. Say both halves: *it exists, and every input can reach it.*
- **Count the recursive calls in the body: one is a line, two is a tree.** `total` makes one → O(n).
  `fib` makes two → **~2ⁿ**: `fib(40)` is ~**331 million calls, ~13 s**, and `@cache` turns it
  into **41 calls** — that is memoisation, and it is the foundation of DP.
- **Recursion always costs O(depth) stack, and Python's limit is ~1000 frames** — so a linear-depth
  recursion dies on a **5,000-element list**, and `sys.setrecursionlimit` converts a clean
  `RecursionError` into a **segfault**. *Log-depth recursion is free; linear-depth is a bug waiting for
  a big input.* And **never slice in the recursive call** — `f(items[1:])` copies every time and makes
  an O(n) algorithm **O(n²)**; pass an index.
