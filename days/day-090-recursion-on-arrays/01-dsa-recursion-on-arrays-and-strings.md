---
day: 90
track: dsa
title: "Recursion on arrays and strings"
phase: "Recursion and backtracking"
status: written
---

# Day 090 · DSA — Recursion on arrays and strings

**After today you can:** You can convert any simple loop into recursion, and back again.

**The interviewer asks it as:** *Reverse a string recursively. Now do it without extra space.*

---

## 1. What this is, and why they ask it

Arrays and strings are where recursion is most often *asked for* and least often *needed*. A loop over
a list is clearer, faster, and does not die at a thousand elements. So this day is not about
convincing you to write recursion here — it is about being able to, correctly, when someone asks.

Two techniques do almost all of the work.

**Pass an index, never a slice.** `f(items[1:])` copies the list on every call, which turns an O(n)
algorithm into O(n²) in time and allocation, silently. `f(items, start + 1)` does not. This is the
single most common performance bug in recursive array code and it never raises an error — the function
is correct and mysteriously slow.

**Two indices, moving toward each other.** Palindromes, reversing in place, comparing from both ends —
all of them are `low` and `high` walking inward, and the base case is `low >= high`. That is the
recursive form of the two-pointer technique from
[day 028](../day-028-opposite-ends/README.md), and it is what "without extra space" means when an
interviewer says it.

They ask it because "write this recursively" is a five-minute filter, because the slicing trap catches
most people, and because the honest answer to "which would you ship?" — the loop — is a small test of
judgement that some candidates fail by over-committing to the clever version.

---

## 2. The story

Nagaraj has run the stationery shop by the bus stand for twenty-six years, and once a month he reads
his order out to the supplier over the phone.

It is a long list. Three hundred and forty lines on a good month, and it lives in a spreadsheet on his
phone that his daughter set up in 2019.

His nephew Manju sat with him last year to help and did it in a way that Nagaraj still talks about.

Every time the call dropped — and it drops, that corner has always been bad — Manju would go back to
the top of the list and start reading down again to find his place. Every single time. He said he did
not want to lose track. Six drops in one call, and each time he read from the first line again, out
loud, to find where they had stopped. Twenty minutes to read a list that takes six.

Nagaraj does not do that. He puts his thumb on the screen where he has got to and leaves it there. The
call drops, he says the last item again to be safe, and carries on from under his thumb. It costs him
nothing. The list has not moved; only his place in it has.

He said the same thing to Manju about four times before it stuck. You are not making a new list every
time. You are just remembering where you are.

There is a second thing they do together at the end of the year, when the stock has to be checked
against the shelves. Two of them, one list. Nagaraj starts at the top and works down; Manju starts at
the bottom and works up. They call out to each other as they go, and when they meet in the middle,
somewhere around line one hundred and seventy, the job is done and neither of them has walked the shop
twice.

Manju is quite proud of that one and points out that it takes half the time. Nagaraj says it takes the
same time, there are just two of you.

---

## 3. The idea in plain English

Nagaraj's thumb is the **index**. Manju re-reading from the top is **slicing**. And the two of them
meeting in the middle is the **two-index** recursion.

### Rule one: pass an index, never a slice

```python
def total(numbers: list[int]) -> int:
    if not numbers:
        return 0
    return numbers[0] + total(numbers[1:])       # SLICE: copies the whole list
```

Correct, and quietly quadratic. There are `n` calls, and each one builds a new list of nearly `n`
elements, so the total work is `n + (n−1) + … + 1 ≈ n²/2` element copies. Summing a thousand numbers
does half a million copies and allocates a thousand lists.

```python
def total(numbers: list[int], start: int = 0) -> int:
    if start == len(numbers):
        return 0
    return numbers[start] + total(numbers, start + 1)   # INDEX: nothing is copied
```

`n` calls, constant work each. **O(n) time, no allocation at all.**

Same rule for strings, and it bites harder there because strings are immutable, so `text[1:]` copies
every time and so does every `+`.

> **The recursion should look at a *view* of the data, never at a *copy* of it.** An index is a view.

### Rule two: two indices, moving inward

For anything symmetric — palindromes, reversing, comparing ends — one index is not enough.

```python
def is_palindrome(text: str, low: int = 0, high: int | None = None) -> bool:
    if high is None:
        high = len(text) - 1
    if low >= high:                      # met, or crossed: nothing left to compare
        return True
    if text[low] != text[high]:
        return False
    return is_palindrome(text, low + 1, high - 1)
```

The base case is `low >= high`, and it must be `>=` rather than `==`: on an even-length string the two
indices **cross without ever being equal**. `"abba"` goes `(0,3)` then `(1,2)` then `(2,1)` — never
equal. That single character is the most common bug in this shape.

**The measure** — from [day 089](../day-089-recursion-that-terminates/README.md) — is `high - low`,
which drops by two each call and is bounded below. Naming it takes five seconds and it is what makes
the base case obviously right.

### Rule three: an accumulator, when the loop had one

A loop with a running total converts to a recursion with an extra parameter:

```python
    running = 0                          # loop:  running = 0; for x: running += x
    for value in numbers:
        running += value
```

```python
def total_acc(numbers, start=0, running=0):     # recursion: running is a parameter
    if start == len(numbers):
        return running
    return total_acc(numbers, start + 1, running + numbers[start])
```

**Whatever the loop carried between iterations becomes a parameter.** That is the whole conversion
recipe, and it works in both directions: to turn a recursion into a loop, look at what is being
combined on the way back up and make it a running variable.

This version is also **tail-recursive** — nothing happens after the call returns — which a language
with tail-call elimination would turn into a loop for free. Python does not, deliberately, as on
[day 088](../day-088-the-call-stack/README.md), so it dies at the same depth. Know the term; write the
loop.

### The private-helper pattern

Public functions should not have `start` and `high` in their signature — callers should not be able to
pass a wrong one, and the defaults are noise.

```python
def is_palindrome(text: str) -> bool:
    def check(low: int, high: int) -> bool:
        if low >= high:
            return True
        return text[low] == text[high] and check(low + 1, high - 1)
    return check(0, len(text) - 1)
```

The inner function closes over `text`, so it is not passed on every call, and the outer signature is
clean. **This is how recursion on arrays is written in real code**, and it is worth doing in an
interview because it shows you are thinking about the caller.

### Rule four: divide and conquer, when the answer combines

The two shapes so far shrink the problem by one. The other shape splits it in half:

```python
def maximum(numbers: list[int], low: int, high: int) -> int:
    if low == high:
        return numbers[low]              # one element
    middle = (low + high) // 2
    return max(maximum(numbers, low, middle),
               maximum(numbers, middle + 1, high))
```

The measure is `high - low`, which halves. There are still `n` leaves and `2n − 1` calls in total, so
it is O(n) — **the same as the loop, with more calls and log-depth stack.** For `max` that is a strictly
worse way to get the same answer, and it is worth saying so.

Divide and conquer earns its keep when **combining two halves is cheaper than redoing the work**: merge
sort ([day 084](../day-084-merging-and-sorting-lists/README.md)), quickselect, maximum subarray. It is
not a general speed-up.

### Strings: the extra trap

Strings are immutable, so every `+` builds a new string:

```python
def reverse(text: str) -> str:
    if len(text) <= 1:
        return text
    return reverse(text[1:]) + text[0]   # a slice AND a concatenation, per call
```

`n` calls, each building a string of length up to `n`: **O(n²)**, twice over. At 10,000 characters that
is a hundred million character copies to do something `text[::-1]` does instantly.

The fix is to collect into a list and join once, or to work on a `list(text)` in place with two indices.
This is the same lesson as building strings on
[day 020](../day-020-building-strings/README.md), and recursion makes it easier to commit by accident
because the concatenation is hidden in a return statement.

### And the honest part

For a flat array or string, **the loop is better** — clearer, O(1) space, and it does not die at a
thousand elements. Recursion here is a *demonstration*, and if an interviewer asks for it, give it and
then say what you would ship.

Recursion earns its place when the structure is recursive — trees, nested lists, directories — or when
the problem splits and recombines. Those are the next ten days.

---

## 4. The picture

Slicing against indexing, drawn as what exists in memory.

```
 SLICING — a new list per call

   call 1:  [4, 7, 2, 9, 1]         the original
   call 2:     [7, 2, 9, 1]         a NEW list, 4 elements copied
   call 3:        [2, 9, 1]         a NEW list, 3 copied
   call 4:           [9, 1]         2 copied
   call 5:              [1]         1 copied
   ------------------------------------------------
   total copied: 4+3+2+1 = 10       -> n^2/2 for n elements
   lists allocated: 4

 INDEXING — one list, a moving marker

   [4, 7, 2, 9, 1]
    ^start=0
       ^start=1
          ^start=2
             ^start=3
                ^start=4
   ------------------------------------------------
   total copied: 0
   lists allocated: 0
```

Nagaraj's thumb against Manju reading from the top.

The two-index shape, and why the base case is `>=`:

```
 "abcba"  (odd length)                "abba"  (even length)

  a b c b a                            a b b a
  ^       ^     low=0 high=4           ^     ^     low=0 high=3
    ^   ^       low=1 high=3             ^ ^       low=1 high=2
      ^         low=2 high=2               X       low=2 high=1
      low == high -> stop                  low > high -> stop

 ODD lengths stop with low == high.
 EVEN lengths never have low == high; they CROSS.
 So the base case is `low >= high`, and `==` alone loops for ever on even input.
```

And the two shapes of array recursion:

```
 SHRINK BY ONE                        SPLIT IN HALF

   f(0, n)                              f(0, n)
     |                                  /      \
   f(1, n)                        f(0, n/2)   f(n/2, n)
     |                             /    \       /    \
   f(2, n)                       ...    ...   ...    ...
     |
   ...                            depth log n, 2n-1 calls
   depth n, n calls               O(n) work, O(log n) stack

   dies at ~1000                  fine at a million
```

**The second shape is safe at any size and the first is not**, which is why merge sort recurses happily
on a million elements and `total` does not.

---

## 5. The code, built step by step

### Step 1 — write the loop first, then convert

```python
    running = 0
    for value in numbers:
        running += value
    return running
```

Look at it and name three things: **what changes between iterations** (the position), **what is carried
across** (the running total), and **when it stops** (the end of the list). Those become the index, the
accumulator, and the base case.

### Step 2 — the signature, with a private helper

```python
def total(numbers: list[int]) -> int:
    def go(start: int) -> int:
        ...
    return go(0)
```

The public function takes what a caller would sensibly pass. The helper takes the bookkeeping. `numbers`
is closed over rather than passed, so it is not on the stack `n` times.

### Step 3 — the base case as the measure hitting its floor

```python
        if start == len(numbers):        # measure: len(numbers) - start, floor 0
            return 0
```

Written as the measure reaching zero, exactly as on
[day 089](../day-089-recursion-that-terminates/README.md).

### Step 4 — the recursive call, with the index moving

```python
        return numbers[start] + go(start + 1)
```

Point at `start + 1`. That is the measure decreasing, and it is where the bug lives when there is one.

### Step 5 — the two-index version, with the `>=`

```python
    def check(low: int, high: int) -> bool:
        if low >= high:                  # >= not ==, or even lengths never stop
            return True
        return text[low] == text[high] and check(low + 1, high - 1)
```

Say "greater than or equal, because even lengths cross rather than meet" as you type the `>=`. It is
one character and it is the whole bug.

### Step 6 — in-place reversal, which is what "no extra space" means

```python
    def swap(low: int, high: int) -> None:
        if low >= high:
            return
        chars[low], chars[high] = chars[high], chars[low]
        swap(low + 1, high - 1)
```

O(1) extra space beyond the stack, which is the honest caveat: **recursion is never truly O(1) space**,
because the frames are space. If the interviewer means strictly constant, the answer is the loop.

### The complete solution

```python
def total(numbers: list[int]) -> int:
    """Sum by INDEX, not by slice.

    The slicing version copies the list on every call: n calls x O(n) copy each
    = O(n^2) time and allocation, silently. This one allocates nothing.

    O(n) time, O(n) stack. The loop is better; this is the demonstration.
    """
    def go(start: int) -> int:
        if start == len(numbers):         # measure: len(numbers) - start
            return 0
        return numbers[start] + go(start + 1)
    return go(0)


def total_slicing(numbers: list[int]) -> int:
    """The version to write once, measure, and never write again. O(n^2)."""
    if not numbers:
        return 0
    return numbers[0] + total_slicing(numbers[1:])


def total_accumulator(numbers: list[int]) -> int:
    """Whatever the loop carried between iterations becomes a parameter.

    Also tail-recursive — nothing happens after the call — which a language
    with tail-call elimination would turn into a loop. Python does not, so
    this dies at the same depth as any other recursion.
    """
    def go(start: int, running: int) -> int:
        if start == len(numbers):
            return running
        return go(start + 1, running + numbers[start])
    return go(0, 0)


def is_palindrome(text: str) -> bool:
    """Two indices moving inward. O(n) time, O(n) stack, no copying.

    The base case is low >= high, NOT ==: on an even length the indices cross
    without ever being equal, so `==` alone never terminates.
    """
    def check(low: int, high: int) -> bool:
        if low >= high:
            return True
        return text[low] == text[high] and check(low + 1, high - 1)
    return check(0, len(text) - 1)


def reverse_in_place(chars: list[str]) -> list[str]:
    """LeetCode 344: reverse a character list in place, recursively.

    O(1) extra space apart from the stack — and that caveat matters: recursion
    is never truly constant space, because the frames ARE space.
    """
    def swap(low: int, high: int) -> None:
        if low >= high:
            return
        chars[low], chars[high] = chars[high], chars[low]
        swap(low + 1, high - 1)
    swap(0, len(chars) - 1)
    return chars


def reverse_string_slow(text: str) -> str:
    """The trap, twice over: a slice AND a concatenation on every call.
    n calls each building a string of up to n characters -> O(n^2)."""
    if len(text) <= 1:
        return text
    return reverse_string_slow(text[1:]) + text[0]


def reverse_string_fast(text: str) -> str:
    """Collect into a list, join once. O(n) total character copying."""
    parts: list[str] = []

    def go(index: int) -> None:
        if index < 0:
            return
        parts.append(text[index])
        go(index - 1)

    go(len(text) - 1)
    return "".join(parts)


def maximum(numbers: list[int]) -> int:
    """Divide and conquer. The measure (high - low) HALVES, so the stack depth
    is log n and this survives a million elements where shrink-by-one does not.

    But it is 2n-1 calls to do what one loop does in n steps: for `max`,
    divide and conquer is a demonstration, not an improvement. It earns its
    keep only when combining halves is cheaper than redoing the work.
    """
    if not numbers:
        raise ValueError("maximum() of an empty sequence")

    def go(low: int, high: int) -> int:
        if low == high:
            return numbers[low]
        middle = (low + high) // 2
        return max(go(low, middle), go(middle + 1, high))

    return go(0, len(numbers) - 1)


def binary_search(numbers: list[int], target: int) -> int:
    """Recursion where the depth is log n, so the stack cost is irrelevant:
    about 20 frames at a million elements."""
    def go(low: int, high: int) -> int:
        if low > high:
            return -1
        middle = (low + high) // 2
        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            return go(middle + 1, high)
        return go(low, middle - 1)
    return go(0, len(numbers) - 1)


def remove_character(text: str, unwanted: str) -> str:
    """Build with a list and one join, never with `+` inside the recursion."""
    kept: list[str] = []

    def go(index: int) -> None:
        if index == len(text):
            return
        if text[index] != unwanted:
            kept.append(text[index])
        go(index + 1)

    go(0)
    return "".join(kept)


def flatten(items: list) -> list:
    """The case where recursion is genuinely the right tool: the STRUCTURE is
    recursive, so there is no index that expresses the problem."""
    out: list = []

    def go(node) -> None:
        for item in node:
            if isinstance(item, list):
                go(item)                 # depth = nesting depth, not length
            else:
                out.append(item)

    go(items)
    return out


if __name__ == "__main__":
    import time

    print(total([4, 7, 2]), total([]), total_accumulator([4, 7, 2]))    # 13 0 13
    print(is_palindrome("malayalam"), is_palindrome("abba"),
          is_palindrome("abc"), is_palindrome(""), is_palindrome("a"))
    # True True False True True

    print("".join(reverse_in_place(list("recursion"))))                 # noisrucer
    print(reverse_string_fast("recursion"))                             # noisrucer
    print(maximum([3, 9, 2, 9, 1]), binary_search([1, 3, 5, 7, 9], 7))  # 9 3
    print(remove_character("mississippi", "s"))                         # miiippi
    print(flatten([1, [2, [3, [4, 5]], 6], 7]))                         # [1,2,3,4,5,6,7]

    # the slicing trap, measured
    sample = list(range(900))
    start = time.perf_counter()
    total_slicing(sample)
    slicing = time.perf_counter() - start
    start = time.perf_counter()
    total(sample)
    indexing = time.perf_counter() - start
    print(f"slicing {slicing:.5f}s  indexing {indexing:.5f}s  ratio {slicing / indexing:.1f}x")

    # and the shape that survives a big input, against the one that does not
    big = list(range(100_000))
    print(maximum(big))                                                 # 99999
    try:
        total(big)
    except RecursionError as error:
        print(f"RecursionError: {error}")
    print(sum(big))                                                     # 4999950000
```

---

## 6. What it costs

### Slicing against indexing

```
 slicing:   n calls, each copying up to n elements
            total element copies = n + (n-1) + ... + 1 = n(n+1)/2
            allocations: n lists
            -> O(n^2) time AND O(n^2) total allocation

 indexing:  n calls, constant work each
            allocations: 0
            -> O(n) time, O(n) stack only
```

```
 n = 900:  slicing copies ~405,000 elements to add up 900 numbers
```

Measured at n = 900 — about the largest that fits under the recursion limit — the slicing version took
**0.0037 s against 0.00013 s, roughly 29× slower**, and the gap widens with `n` because it is a
different complexity class rather than a constant factor.

### Strings are worse

```
 reverse_string_slow("..."), n characters:
   n calls
   each builds a new string of up to n characters
   -> O(n^2) character copies, AND O(n) intermediate strings

 n = 10,000:  ~50,000,000 character copies
              text[::-1] does it in one pass
```

Two O(n²) sources in one function — the slice and the concatenation — which is why string recursion
written naively is so much slower than array recursion written naively.

### The two shapes of stack cost

```
 shrink by one:   depth n       -> dies at ~1000 in Python
 split in half:   depth log n   -> 17 frames at 100,000; 20 at 1,000,000
```

```
 maximum([...100,000 items...])   works: depth 17
 total([...100,000 items...])     RecursionError
```

**Same input, same language, opposite outcomes**, and the only difference is how the measure shrinks.
That is the practical reason merge sort recurses comfortably on a million elements and a
sum-by-index does not.

### Recursion against the loop, honestly

```
                       loop            recursion (index)
 time                  O(n)            O(n)
 space                 O(1)            O(n) stack
 max input             unbounded       ~1000
 speed                 baseline        ~1.5-2x slower (call overhead)
 clarity on a flat
   array               better          worse
```

**There is no column where recursion wins on a flat array.** That is the honest summary, and saying it
is a better answer than defending the recursive version.

### Where recursion does win

```
 nested structure (flatten):  depth = NESTING depth, not length
   a list of 1,000,000 items nested 3 deep:  3 frames
   the iterative version needs an explicit stack and is longer

 divide and conquer (merge sort, quickselect):
   depth log n, and combining halves is cheaper than redoing the work
```

The rule: **recursion is for recursive structure and for divide-and-conquer, not for iteration.**

---

## 7. The traps

### Trap 1 — slicing in the recursive call

```python
    return numbers[0] + total(numbers[1:])
```

No error, correct answer, O(n²). It is the single most common recursion bug on arrays and it is
invisible until the input grows. **Pass an index.** Same for `text[1:]`, which is worse because strings
copy on every operation.

### Trap 2 — `==` instead of `>=` in the two-index base case

```python
        if low == high:
            return True
```

Works on odd lengths, recurses for ever on even ones, because `low` and `high` **cross without meeting**:
`"abba"` goes `(0,3) → (1,2) → (2,1)` and never equal.

```
RecursionError: maximum recursion depth exceeded
```

on exactly half of all inputs. This is condition two from
[day 089](../day-089-recursion-that-terminates/README.md) — the measure decreases and steps over the
bound.

### Trap 3 — building a string with `+` inside the recursion

```python
    return reverse(text[1:]) + text[0]
```

Two quadratic behaviours at once. Collect into a list and `"".join` at the end, or work on a
`list(text)` in place.

### Trap 4 — a mutable default as the accumulator

```python
def collect(text, index=0, out=[]):     # created ONCE at definition time
```

The second top-level call sees the first call's results. Use `None` and create it inside, or close over
a local list in a private helper — which is the pattern that avoids the problem by construction.

### Trap 5 — a public signature full of bookkeeping

```python
def is_palindrome(text: str, low: int = 0, high: int = -1) -> bool:
```

A caller can pass a wrong `low`, the default for `high` has to be a sentinel because it depends on
`text`, and the signature lies about what the function is for. **Use a private helper**, and the outer
function takes one argument.

### Trap 6 — divide and conquer where a loop would do

```python
    return max(go(low, middle), go(middle + 1, high))
```

`2n − 1` calls to find a maximum that a loop finds in `n` steps with no stack. It is not wrong, and it
is not an improvement. Divide and conquer pays only when **combining the halves is cheaper than
redoing the work** — merging two sorted halves, or discarding one half entirely.

### Trap 7 — mutating the caller's data without saying so

```python
def reverse_in_place(chars: list[str]) -> list[str]:
    ...                                  # returns the SAME list, reversed
```

The caller's list is now reversed. That is exactly what "in place" means and it is correct here — but a
function that *inspects* and mutates is a real bug, and it is the same rule as the palindrome check
that leaves a linked list half-reversed on
[day 082](../day-082-runner-technique/README.md). Say which you are doing.

### Trap 8 — claiming O(1) space for a recursive in-place algorithm

```python
    swap(low + 1, high - 1)              # O(n) stack frames
```

The array is untouched and the stack is not. **Recursion is never truly O(1) space.** If the requirement
is strictly constant, the answer is a loop, and saying that is better than being corrected.

---

## 8. In the interview

### How it gets asked

- The base: *"Reverse a string recursively."* Then: *"Now without extra space."* — which means two
  indices on a character list, and the honest note about the stack.
- The classic: *"Check if a string is a palindrome, recursively."*
- The conversion: *"Here is a loop. Write it recursively."* Or the reverse, which is what production
  work actually needs.
- The performance probe: *"Your version is slower than the loop even though both are O(n). Why?"*
- The judgement probe: *"Which would you actually ship?"*

### What to say out loud, in the first ninety seconds

1. **Name the shape.** "This shrinks by one from the front, so one index." Or: "this is symmetric, so
   two indices moving inward."
2. **Say the index rule before writing it.** "I will pass an index rather than a slice — slicing copies
   the list on every call and turns this into O(n²) time and allocation."
3. **Name the measure and the base case together.** "The measure is `len(text) - start`, and the base
   case fires when it reaches zero." Or, for two indices: "the measure is `high - low`, dropping by
   two, and the base case is `low >= high` — greater-or-equal, because even lengths cross rather than
   meet."
4. **Use a private helper.** "The public function takes just the string; the recursion is an inner
   function so the bookkeeping is not in the signature."
5. **State both costs.** "O(n) time and O(n) stack — which means it dies at about a thousand characters
   in Python."
6. **Then give the judgement.** "For a flat string I would ship the loop. Recursion here is a
   demonstration; it earns its place on recursive structures and divide-and-conquer."

### The follow-ups

**"Your recursive version is slower than the loop even though both are O(n). Why?"**
"Two reasons, and one of them is usually a bug. There is genuine per-call overhead — building a frame,
binding arguments, returning — which is a constant factor of about one and a half to two in Python. But
if the gap is much bigger than that, it is slicing: `f(items[1:])` copies the list on every call, so n
calls each copying up to n elements is O(n²) in time *and* in allocation. Passing an index fixes it and
allocates nothing. In strings it is worse, because a slice copies and every `+` builds a new string, so
a naive recursive reverse is quadratic twice over."

**"Reverse a string without extra space."**
"Strings are immutable in Python, so strictly I need a character list — `list(text)` — and then two
indices moving inward, swapping and recursing on `low + 1, high - 1`. The array is O(1) extra space.
But I would add the honest caveat: **recursion is never truly constant space**, because the frames are
space, so this is O(n) stack. If you mean strictly constant, the answer is the loop with the same two
indices, and I would write that."

**"Why is the base case `low >= high` and not `low == high`?"**
"Because on an even-length input the indices cross without ever being equal. `\"abba\"` goes zero and
three, then one and two, then two and one — never equal, so `==` alone recurses for ever and you get a
`RecursionError` on exactly half of all inputs. It is the classic 'measure decreases and steps over
the bound' failure: `high - low` drops by two, so it can jump from one to minus one without passing
through zero."

**"Convert this loop to recursion."**
"Three things become three things. What changes between iterations becomes the index parameter. What is
carried across iterations — the running total, the best-so-far, the accumulated list — becomes an
accumulator parameter. And the loop's stopping condition becomes the base case. Going the other way is
the same recipe backwards: look at what is being combined on the way back up and make it a running
variable. And if the recursive version happens to be tail-recursive, that conversion is completely
mechanical — though it is worth noting Python will not do it for you."

**"When would you actually use recursion on an array?"**
"Rarely, and I would say so. For a flat array the loop wins on every axis: same time, O(1) space
instead of O(n), no thousand-element limit, and clearer. Recursion earns its place in two cases. When
the *structure* is recursive — a nested list, a directory tree, a JSON document — because then the
depth is the nesting depth rather than the length, and the iterative version means managing a stack by
hand. And divide and conquer, where combining two halves is cheaper than redoing the work: merge sort,
quickselect, binary search. Splitting an array in half just to find a maximum is 2n−1 calls to do what
a loop does in n steps."

**"Does the stack depth depend on which shape you chose?"**
"Entirely, and it is the difference between working and crashing. Shrink-by-one gives depth n, so it
dies at about a thousand. Split-in-half gives depth log n — seventeen frames at a hundred thousand
elements, twenty at a million. Same language, same input, opposite outcomes. That is why merge sort
recurses happily on a million elements and a sum-by-index does not, and it comes straight out of how
the measure shrinks."

### A model answer

Asked: *reverse a string recursively, then do it without extra space.*

> "Two things to decide before writing: the shape of the recursion, and how I pass the data.
>
> On the shape: reversing is symmetric, so this is the two-index form — one index at each end, moving
> inward, swapping as they go. The measure is `high - low`, it drops by two on every call, and the base
> case is when they meet or cross.
>
> On passing the data: an index, not a slice. This matters more than it looks. The obvious recursive
> reverse is `reverse(text[1:]) + text[0]`, and that is quadratic twice over — the slice copies the
> string on every call, and every `+` builds a new string. At ten thousand characters that is about
> fifty million character copies to do something the slice notation does in one pass. Passing indices
> copies nothing.
>
> The base case is `low >= high`, greater *or equal*, and that one character is where this goes wrong.
> On an even-length string the two indices cross without ever being equal — `\"abba\"` is zero-and-three,
> then one-and-two, then two-and-one — so `==` alone never terminates, and you get a `RecursionError`
> on exactly half of all inputs.
>
> Now, 'without extra space'. Python strings are immutable, so I cannot swap characters in a string; I
> need a character list. Then the swap is a tuple assignment and the recursion carries the two indices,
> and the array itself uses no extra space.
>
> But I want to be honest about the caveat, because it is the thing an interviewer is often checking:
> **recursion is never truly O(1) space.** The frames are space. This is O(n) stack, and in Python it
> dies at about a thousand characters. If 'without extra space' means strictly constant, the answer is
> a loop with the same two indices, and I would write that one.
>
> I would also structure it with a private helper: the public function takes just the string, and the
> inner function carries `low` and `high`. That keeps the bookkeeping out of the signature so a caller
> cannot pass a wrong index, and the inner function closes over the data rather than passing it on
> every call.
>
> And the judgement, since it usually comes next: for a flat string I would ship the loop. Same
> complexity, constant space, no depth limit, clearer. Recursion earns its place when the structure is
> recursive — a nested list where the depth is the nesting rather than the length — or in divide and
> conquer, where combining two halves is genuinely cheaper than redoing the work."

---

## 9. Recall card

- **Pass an INDEX, never a slice.** `f(items[1:])` copies on every call — n calls × O(n) copy =
  **O(n²) time *and* allocation**, silently, with no error. `f(items, start + 1)` allocates nothing.
  In strings it is worse: the slice copies **and** every `+` builds a new string, so a naive recursive
  reverse is quadratic twice over (~5 × 10⁷ character copies at n = 10,000).
- **Symmetric problems use TWO indices moving inward, and the base case is `low >= high`.** Not `==`:
  on even lengths they **cross without meeting** — `"abba"` goes (0,3) → (1,2) → (2,1) — so `==` alone
  recurses for ever on half of all inputs. The measure is `high − low`, dropping by two.
- **Converting a loop is a three-part recipe:** what *changes* between iterations → the index · what is
  *carried across* → an accumulator parameter · the *stopping condition* → the base case. Put the
  bookkeeping in a **private helper** so the public signature takes only what a caller would pass.
- **The shape decides whether it survives.** Shrink-by-one → depth **n**, dies at ~1000. Split-in-half →
  depth **log n**, 17 frames at 100,000. *Same input, opposite outcomes.* And divide-and-conquer on a
  flat array is **2n − 1 calls to do what a loop does in n** — it only pays when combining halves is
  cheaper than redoing the work.
- **On a flat array the loop wins on every axis** — same time, **O(1) space vs O(n) stack**, no depth
  limit, clearer — and **recursion is never truly O(1) space** even when the array is untouched.
  Recursion earns its place on **recursive structure** (nesting depth, not length) and on
  **divide-and-conquer**. Say which you would ship.
