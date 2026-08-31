---
day: 66
track: dsa
title: "When a hash map is the wrong answer"
phase: "Hashing: maps and sets"
status: written
---

# Day 066 · DSA — When a hash map is the wrong answer

**After today you can:** You can name the three cases where sorting or an array beats a dictionary.

**The interviewer asks it as:** *You used a hash map. Could you do it in O(1) space instead?*

---

## 1. What this is, and why they ask it

For six days the answer to everything has been "put it in a dictionary". Today is the correction.
There are three situations where a hash map is the wrong tool, and they are specific enough to
memorise: **when the interviewer takes your extra space away**, **when the keys are small dense
integers**, and **when you need the data in order**. In all three, something simpler and faster
exists, and reaching for the dictionary out of habit is a visible reflex rather than a decision.

They ask it in a very particular way. You give the O(n) hash-map answer, they nod, and then they say
*now do it in O(1) space*, or *now give me the k-th smallest*, or *what if the values are all between
1 and n*. That is not a trick. It is the second half of the question, and it was always coming. An
interviewer wants to see that you know what the map was buying you — it was buying time with memory —
and that you can name what you would trade instead.

The deeper point, and the one worth carrying out of this phase, is that **a hash map throws away
structure**. If the input is sorted, the map does not care. If the keys are the numbers 1 to n, the
map hashes them anyway. Every one of today's three cases is a situation where the input had structure
and the dictionary ignored it.

---

## 2. The story

The wedding at the hall in Jayanagar had about four hundred people coming, and because it was August
half of them would arrive with something — an umbrella, a bag, a stack of boxes somebody had been
asked to carry.

Ramesh's nephew Kiran, who is twenty-three and quite pleased with himself, arrived on the Friday
evening with a plan. He would sit at a table by the door with his phone. Every person who handed
something over, he would type in their name and where he had put their things. Then when they came
back he would look up the name.

Ramesh listened to the whole thing and then pointed at the wall behind the table.

The wall has a hundred and twenty wooden pigeonholes in it, six rows of twenty, and each one has a
number painted on it in white. In a drawer under the table there is a book of small numbered brass
tokens, two of each number.

So the actual system is: a woman hands over her umbrella, Kiran puts it in the first empty hole,
which is 47, and hands her token 47. She comes back and gives him the token, and he goes to hole 47.
He does not need her name. He does not need to look anything up. He does not need to remember
anything at all, and neither does she.

It took Kiran most of Friday evening to stop being annoyed about this.

Two more things happened over the weekend, and they are the reason Ramesh tells the story.

On the Sunday there was a much smaller function in the same hall — fourteen people, a naming
ceremony. Kiran arrived and started setting up the tokens. Ramesh told him not to bother. There were
fourteen bags on one table. If somebody wants theirs, you look at the table. Setting up a system to
avoid looking at fourteen bags is more work than looking at fourteen bags.

And on the Saturday night, at about half past eleven, the caterer needed to shut the hall and asked
which things were still uncollected. Because the holes are in a row and numbered in order, Ramesh
walked along the wall from 1 and had the answer in a minute. Kiran's phone would have held four
hundred names in the order people arrived, and answering that would have meant reading all four
hundred.

---

## 3. The idea in plain English

Kiran's phone is a **hash map**: a general system that can look up anything by any key, at the price
of storing the keys and computing where they go. It works for every situation, which is exactly why
it is the default.

The wall of numbered holes is **direct addressing**: because the keys are the numbers 1 to 120, you
do not need to hash anything. The key *is* the position. No hashing, no storing keys, no collisions,
and about a quarter of the memory.

The fourteen bags are **n is too small for a data structure**. Setting one up costs more than the
scan it saves.

And the walk along the wall is **order**. A hash map has none, so any question that mentions
smallest, largest, next, previous, k-th or between cannot be answered by one.

### Case 1 — the interviewer takes your space away

The map bought time with memory. When memory is taken away, you have two standard replacements.

**Sort, then walk.** Sorting brings equal elements next to each other and puts everything in order, so
duplicates, ranges and neighbours all become one pass. Cost: O(n log n) time instead of O(n), O(1)
extra space if you may modify the input.

**Two pointers on the sorted input.** Once the data is sorted, the opposite-ends walk from
[day 028](../day-028-opposite-ends/README.md) answers pair-sum questions with no map at all. Two Sum
on a *sorted* array is O(n) time and O(1) space, and needs no dictionary.

**Mark inside the input itself.** This is the sharp one. If the values are integers in a known range —
usually 1 to n — the array can be its own hash table. You record "I have seen the value 3" by making
the element at index 2 negative. No extra memory, because you are storing the information in the sign
bit of data you already have.

```python
for number in numbers:
    index = abs(number) - 1
    if numbers[index] > 0:
        numbers[index] = -numbers[index]     # mark "value index+1 was seen"
```

`abs` is there because the element may already have been flipped by an earlier step. This is O(n)
time and O(1) extra space, and it destroys the input, which is a question you must ask before doing
it.

### Case 2 — the keys are small dense integers

If the keys are the twenty-six lowercase letters, or the ASCII range, or the numbers 0 to 100, a
plain list indexed directly beats a dictionary on every axis.

```python
counts = [0] * 26
counts[ord(character) - ord("a")] += 1
```

No hashing, no collisions, no key storage, and the memory is contiguous so the processor's cache
works properly. This is the same idea as counting sort from
[day 056](../day-056-non-comparison-sorts/README.md).

The condition is **dense**. Twenty-six keys in a range of twenty-six is dense. Three keys in the
range 0 to a billion is not — that list would be four gigabytes of zeroes, and the dictionary is
obviously right.

### Case 3 — you need order

A hash map answers exactly one question: *is this key present, and what is its value?* Every other
question needs a different structure.

| The question | Hash map | What to use |
|---|---|---|
| Is key 57 present? | O(1) | hash map |
| What is the smallest key? | O(n) — read everything | heap, or sorted array |
| What is the k-th smallest? | O(n log n) — sort it first | heap, quickselect |
| Which keys are between 10 and 20? | O(n) | sorted array + binary search |
| What is the next key after 57? | O(n) | sorted array, or a balanced tree |
| Give me everything in order | O(n log n) | sorted array, balanced tree |

The row that matters most in interviews is the range query. "Which events happened between these two
times" against a dictionary is a full scan. Against a sorted array it is two binary searches from
[day 044](../day-044-first-and-last-occurrence/README.md) and a slice.

Python has no built-in balanced tree. The honest answers are `bisect` on a sorted list, `heapq` for
smallest-or-largest, or the third-party `sortedcontainers.SortedList`. Say which you would reach for
and why — "there is no `TreeMap` in the standard library" is a correct and useful sentence.

### The three smaller reasons

Not headline cases, but each is a real answer to a real follow-up.

**Memory.** Measured, on a million integers:

```
 list   7 MB          dict   40 MB
 set   32 MB
```

A set is roughly four times a list and a dict is nearly six, because both store hashes, keep the
table about two-thirds empty by design, and hold pointers rather than values.

**Tiny n.** At eight elements, scanning a list is only about twice as slow as a set lookup in Python,
and in a compiled language the list often wins outright because it is one cache line and the hash is
a computation. Below roughly eight to sixteen elements, building a set costs more than it saves.

**Untrusted keys.** O(1) is the average, not the worst. A hash map fed adversarial keys degrades to
O(n) per operation — the attack from [day 061](../day-061-collisions/README.md). In a latency-critical
path where the worst case is what you are promising, a sorted structure with a guaranteed O(log n)
can be the right choice even though it is slower on average.

---

## 4. The picture

The same information, three ways, on the values `[3, 1, 3, 4]` where every value is between 1 and 4.

```
 (a) a hash map          keys stored, hashed, ~40 bytes per entry
       { 3: 2, 1: 1, 4: 1 }

 (b) direct addressing   the key IS the position. No keys stored.
       value:   1   2   3   4
              +---+---+---+---+
       count  | 1 | 0 | 2 | 1 |
              +---+---+---+---+
       index    0   1   2   3        <- index = value - 1

 (c) marking in place    no extra memory at all
       before:  [  3 ,  1 ,  3 ,  4 ]
                   |
       see 3 -> flip index 2:
                [  3 ,  1 , -3 ,  4 ]
       see 1 -> flip index 0:
                [ -3 ,  1 , -3 ,  4 ]
       see 3 -> index 2 already negative, leave it
       see 4 -> flip index 3:
                [ -3 ,  1 , -3 , -4 ]
                        ^
                index 1 is still positive  ->  the value 2 never appeared
```

What to notice in (c): the array is now carrying two pieces of information at once. The **magnitude**
is still the original value, and the **sign** is the "have I seen index+1" flag. That is why every
read has to be `abs(numbers[i])` — you are reading through a mark that you put there.

And the ordering point, drawn:

```
 hash map, iterated:     3, 1, 4       <- no order you can rely on
 sorted array:           1, 3, 3, 4    <- "smallest" is [0]
                                          "between 2 and 4" is two binary searches
```

The map is not badly ordered. It is *unordered* — there is no order to be wrong about, which is why
every ordering question has to go somewhere else.

---

## 5. The code, built step by step

The flagship problem for this whole lesson is **First Missing Positive** — LeetCode 41. Given an
unsorted array, find the smallest positive integer that is not in it. `[3, 4, -1, 1]` gives `2`. The
required complexity is **O(n) time and O(1) extra space**, which is precisely the sentence "you may
not use a hash map".

### Step 1 — the answer that is not allowed

```python
def first_missing_positive_with_set(numbers: list[int]) -> int:
    present = set(numbers)
    candidate = 1
    while candidate in present:
        candidate += 1
    return candidate
```

Write this first anyway, and say so: "this is O(n) time and O(n) space, and it is the answer if space
is free. You have asked for O(1) space, so the set has to go." Showing the easy answer and then
removing it is a better interview than jumping to the clever one.

### Step 2 — notice the bound nobody gave you

Here is the observation the whole problem turns on, and it is worth saying slowly.

With `n` numbers, the answer must be between `1` and `n + 1`.

Why: if the array contained all of `1, 2, ..., n`, the answer would be `n + 1`. If it did not contain
all of them, the answer is one of them, so it is at most `n`. **Nothing outside `1..n+1` can be the
answer, so nothing outside that range matters.** Negative numbers, zero, and anything above `n` can
be ignored entirely.

That single fact converts an unbounded problem into a bounded one, which is what makes direct
addressing possible.

### Step 3 — clean the array so the marking is safe

The marking trick uses the sign bit, so a value that is already negative or zero would confuse it.
Replace anything useless with a value that is out of range but positive:

```python
n = len(numbers)
for i in range(n):
    if numbers[i] <= 0 or numbers[i] > n:
        numbers[i] = n + 1          # a harmless placeholder, definitely out of range
```

After this pass every element is between 1 and n + 1, and every element is positive. The array is
now safe to write signs into.

### Step 4 — mark what is present

```python
for i in range(n):
    value = abs(numbers[i])
    if value <= n:
        numbers[value - 1] = -abs(numbers[value - 1])
```

Read it carefully, because both `abs` calls are load-bearing. The first reads the original value
through any mark already placed on this slot. The second makes the target negative *without*
flipping an already-negative slot back to positive — `-abs(x)` is idempotent, while `-x` is not. That
is the bug people write, and it fails on any input with a repeated value.

### Step 5 — read the answer off

```python
for i in range(n):
    if numbers[i] > 0:
        return i + 1           # slot i was never marked, so i+1 never appeared
return n + 1                   # everything 1..n was present
```

The first positive slot is the first missing positive. If there is none, the array held all of
`1..n`, so the answer is `n + 1`.

### The complete solution

```python
def first_missing_positive(numbers: list[int]) -> int:
    """The smallest positive integer absent from `numbers`.

    O(n) time, O(1) extra space. Uses the array itself as the table: slot i
    records whether the value i + 1 was seen, in its sign bit.

    NOTE: this modifies the input. Ask before doing that.
    """
    n = len(numbers)

    # 1. The answer is in 1..n+1, so anything outside that range is irrelevant.
    #    Replace it with a positive placeholder so the sign trick is safe.
    for i in range(n):
        if numbers[i] <= 0 or numbers[i] > n:
            numbers[i] = n + 1

    # 2. For each value v in 1..n, mark slot v-1 negative.
    #    -abs(...) so a repeated value does not flip a slot back to positive.
    for i in range(n):
        value = abs(numbers[i])
        if value <= n:
            numbers[value - 1] = -abs(numbers[value - 1])

    # 3. The first slot still positive is the first value never seen.
    for i in range(n):
        if numbers[i] > 0:
            return i + 1
    return n + 1


def two_sum_sorted(numbers: list[int], target: int) -> tuple[int, int] | None:
    """Two Sum on SORTED input: O(n) time, O(1) space, no hash map needed."""
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return left, right
        if total < target:
            left += 1               # need a bigger sum
        else:
            right -= 1              # need a smaller sum
    return None


def has_duplicate_sorted(numbers: list[int]) -> bool:
    """O(n log n) time, O(1) extra space — the answer when the set is taken away."""
    numbers.sort()                          # in place
    return any(numbers[i] == numbers[i - 1] for i in range(1, len(numbers)))


def count_letters(word: str) -> list[int]:
    """Direct addressing: the key IS the index. No hashing, no key storage."""
    counts = [0] * 26
    for character in word:
        counts[ord(character) - ord("a")] += 1
    return counts


def values_between(sorted_values: list[int], low: int, high: int) -> list[int]:
    """A range query — the thing a hash map cannot do. Two binary searches."""
    import bisect
    start = bisect.bisect_left(sorted_values, low)
    end = bisect.bisect_right(sorted_values, high)
    return sorted_values[start:end]


if __name__ == "__main__":
    print(first_missing_positive([1, 2, 0]))          # 3
    print(first_missing_positive([3, 4, -1, 1]))      # 2
    print(first_missing_positive([7, 8, 9, 11, 12]))  # 1
    print(first_missing_positive([1, 1]))             # 2  <- the -abs case
    print(first_missing_positive([]))                 # 1
    print(two_sum_sorted([2, 7, 11, 15], 9))          # (0, 1)
    print(count_letters("banana")[:5])                # [3, 1, 0, 0, 0]
    print(values_between([1, 3, 5, 7, 9, 11], 4, 9))  # [5, 7, 9]
```

The `[1, 1]` case is the one to run. With `-x` instead of `-abs(x)` in step 2, the second `1` flips
slot 0 back to positive and the function returns `1` instead of `2`.

---

## 6. What it costs

### The three passes, counted

Each of the three loops runs exactly `n` times and does constant work inside.

```
 pass 1 (clean):   n iterations x 1 comparison, 1 possible write
 pass 2 (mark):    n iterations x 1 abs, 1 comparison, 1 write
 pass 3 (read):    n iterations x 1 comparison
 -----------------------------------------------------------
 total:            3n  ->  O(n)
```

Space is **O(1) extra**. The only variables are `n`, `i` and `value`. The array is reused, not
copied, which is the entire point.

Compare with the set version: same O(n) time, but O(n) space and — at a million elements — 32 MB of
extra memory that the marking version does not need.

### Direct addressing versus a dictionary, counted

Counting the letters of a 100,000-character string:

```
 list of 26:   100,000 x (1 subtraction + 1 indexed write)   ~ 2 operations each
 dictionary:   100,000 x (1 hash + 1 modulo + 1 probe + 1 write) ~ 5 operations each
```

Roughly two and a half times the work, plus the dictionary stores 26 keys and their hashes while the
list stores nothing but the counts. In practice the list version is about twice as fast, and the gap
widens on long inputs because 26 integers fit in a couple of cache lines and a dictionary does not.

### Memory, measured

On a million small integers:

```
 list   7 MB
 set   32 MB      about 4.5x
 dict  40 MB      about 5.7x
```

Those numbers are the container only; they are the right ones to quote because they are what the
extra structure costs you over the data you already had.

### Small n, measured

A million membership tests:

```
 n = 100:   set 0.018 s    list 0.265 s     set wins by ~15x
 n = 8:     set 0.019 s    list 0.034 s     set wins by ~1.8x
```

At n = 8 the gap has nearly closed, and that is before counting the cost of *building* the set. If
you build a set to do one lookup over eight items, you have lost. The rule of thumb: **below about
eight to sixteen elements, scan.**

### Sorting versus hashing

```
 hash map:   O(n) time,        O(n) extra space
 sort:       O(n log n) time,  O(1) extra space (in place), input destroyed
```

At n = 1,000,000: the map is 1,000,000 operations and 32 MB; the sort is about 20,000,000 comparisons
and no extra memory. **You are trading a factor of twenty in time for all of the memory**, and which
side of that trade you want depends entirely on the constraint you were given. Say it as a trade, not
as a ranking.

---

## 7. The traps

### Trap 1 — `-x` instead of `-abs(x)`

```python
numbers[value - 1] = -numbers[value - 1]      # WRONG
```

Looks right, is right on inputs with no duplicates, and fails on `[1, 1]`. The first `1` makes slot 0
negative; the second `1` negates it again and makes it positive; the final pass sees a positive slot
0 and answers `1` when the answer is `2`.

```
 input [1, 1]
   correct: 2
   with -x: 1
```

An input of two elements. It will not be caught by eyeballing the code, and it is the single most
common way this problem is failed.

### Trap 2 — forgetting the cleaning pass

Skip step 3 and the marking loop reads a negative number, takes `abs`, and marks a slot that has
nothing to do with anything. On `[-1, 4, 2, 1]` you get an answer that happens to be right sometimes
and wrong other times, which is worse than always wrong.

Also: without the cleaning pass, an index can go out of range.

```python
>>> numbers = [1, 2, 3]
>>> numbers[abs(-7) - 1] = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list assignment index out of range
```

### Trap 3 — destroying the input without asking

The marking solution overwrites the array. So does the sorting solution. If the caller needed that
array afterwards, you have introduced a bug that no test of your function will catch, because it is
in the caller.

**Ask, every time: "may I modify the input?"** It takes three seconds and it is one of the highest
signal-to-effort questions in the whole interview. If the answer is no, the O(1) space solution does
not exist and you say so.

### Trap 4 — direct addressing on a sparse range

```python
counts = [0] * (max(numbers) + 1)
```

Fine for `[3, 1, 4]`. On `[1, 2, 1000000000]` that allocates a list of a billion entries — about
8 GB — to store three counts.

```
MemoryError
```

The condition for direct addressing is **dense**, not just "integer". Say the condition out loud when
you propose it: "the values are between 1 and n, so I can index by them."

### Trap 5 — asking a hash map an ordering question

```python
smallest = min(counts)              # O(n) — reads everything
first_key = list(d)[0]              # insertion order, not sorted order
```

`min` on a dictionary is a full scan every time you call it. If you need the smallest repeatedly, you
wanted a heap. And `list(d)[0]` gives the first-inserted key, which people mistake for the smallest
key because it often is, on small examples.

### Trap 6 — using a hash map on already-sorted input

If the input is sorted and you build a set from it, you have paid O(n) time and O(n) space to throw
away the very property that would have made the problem easy. Two Sum on a sorted array with a hash
map is O(n) space; with two pointers it is O(1). The interviewer said "sorted" for a reason, and the
word is doing work.

### Trap 7 — quoting O(1) for a worst case

A hash map's O(1) is an average. In a system that must promise a latency bound — an order matching
engine, an ad auction with a 20 ms budget — the O(n) worst case matters, and a structure with a
guaranteed O(log n) can be the correct choice despite being slower on average. Knowing when average
is the wrong statistic is a senior signal.

---

## 8. In the interview

### How it gets asked

- The follow-up, and this is the main one: *"That works. Now do it in O(1) space."* You will hear
  this after almost every hash-map answer you give. It is not a rejection; it is the next question.
- The hint disguised as a constraint: *"All the numbers are between 1 and n."* That sentence exists
  to tell you to index instead of hash.
- The ordering pivot: *"Now give me the k-th smallest"* or *"now give me everything between 10 and
  20"* — the map is finished and something else has to start.
- The direct one: *"When would you not use a hash map?"* Asked at senior level, and the three cases
  are the answer.

### What to say out loud, in the first ninety seconds

1. **Say what the map was buying.** "The dictionary bought me time with memory — O(n) time for O(n)
   space. If you take the space away, I have to buy the time back some other way."
2. **Name the three replacements before choosing one.** "There are three things I can do: sort and
   walk, which is O(n log n) time and O(1) space; two pointers if it is sorted or I sort it; or, if
   the values are in a bounded range, use the array itself as the table."
3. **Ask the question that decides it.** "May I modify the input?" Everything O(1)-space in this
   lesson destroys the array. If the answer is no, say the O(1) solution does not exist and offer the
   O(n log n) copy-and-sort.
4. **Find and state the bound.** For First Missing Positive: "with n numbers, the answer has to be
   between 1 and n + 1, so anything outside that range cannot matter." That sentence is the whole
   problem and you should say it before writing anything.
5. **Then write it, and name the `-abs` line as you write it.** "This has to be `-abs`, not `-`, or a
   repeated value flips the mark back."

### The follow-ups

**"Why is the answer bounded by n + 1?"**
"Because there are only n numbers. If they were exactly 1 through n, the smallest missing positive is
n + 1. If they were not, then one of 1 through n is missing, so the answer is at most n. Either way
nothing outside 1 to n + 1 can be the answer, which is what lets me index into an array of length n."

**"Your solution destroys the input. Is that acceptable?"**
"That is why I asked. If it is not, I can copy the array first, which costs O(n) space and puts me
back where I started, or I can sort a copy for O(n log n) time and O(n) space. There is no O(1) space
solution that preserves the input, because O(1) space means the only place to write anything is the
input."

**"When would you use a plain array instead of a dictionary?"**
"When the keys are small dense integers. Twenty-six letters, ASCII, values bounded by n. The array
does not hash, does not store keys, does not collide, and it is contiguous so the cache works. The
condition is density — three keys in a range of a billion is eight gigabytes of zeroes and obviously
wrong."

**"What can a hash map not do at all?"**
"Anything about order. Smallest, largest, k-th, next, previous, or a range. All of those are O(n)
scans against a map. Sorted array plus binary search for range queries, a heap for repeated
smallest-or-largest, and a balanced tree if I need both ordering and fast insertion — which Python
does not have in the standard library, so I would use `bisect` on a sorted list, or
`sortedcontainers.SortedList`."

**"Is a hash map always O(1)?"**
"On average, with a good hash and a load factor kept low. The worst case is O(n) per operation, when
everything collides. That is rare accidentally and achievable deliberately — the hash-flooding
attacks. So in a latency-critical path where I am promising a bound rather than an average, a
structure with a guaranteed O(log n) can be the better choice even though it is slower most of the
time."

### A model answer

Asked: *find the first missing positive integer, in O(n) time and O(1) space.*

> "Let me give the easy answer first so we agree on the problem. Put everything in a set, then count
> up from 1 until I find a number that is not there. That is O(n) time and O(n) space. You have asked
> for O(1) space, so the set has to go, and the question becomes where I am allowed to store the
> information instead. The only place left is the input array.
>
> The observation that makes that possible is a bound nobody gave me. There are n numbers, so if the
> array happened to contain exactly 1 through n, the answer would be n + 1. If it did not, then one
> of 1 through n is missing, so the answer is at most n. Either way the answer lies between 1 and
> n + 1, which means anything negative, zero, or larger than n is irrelevant and I can ignore it.
>
> That turns it into direct addressing: slot i can record whether the value i + 1 is present, and I
> can record that in the sign bit, because after cleaning, every value is positive.
>
> So it is three passes. First, replace anything outside 1 to n with n + 1, a harmless positive
> placeholder, so the sign trick is safe. Second, for each value v, make slot v − 1 negative. Third,
> walk the array and return the index of the first positive slot, plus one — or n + 1 if there is no
> positive slot.
>
> One line needs care: the marking has to be `numbers[v-1] = -abs(numbers[v-1])`, not
> `-numbers[v-1]`. With a repeated value, plain negation flips the slot back to positive and the
> answer is wrong. On the input `[1, 1]` the correct answer is 2 and the buggy version returns 1.
>
> Cost: three passes of n, so O(n) time, and the only extra variables are two integers, so O(1)
> space.
>
> Before I write it I should ask — may I modify the input? Everything I have described destroys it.
> If the caller needs it afterwards then O(1) space is impossible, because the input is the only
> memory I have, and I would offer sorting a copy instead: O(n log n) time and O(n) space."

---

## 9. Recall card

- **A hash map buys time with memory and throws away structure.** Three cases where it is the wrong
  tool: **space is taken away** · **keys are small dense integers** · **you need order**.
- **No extra space → three moves.** Sort and walk (O(n log n) time, O(1) space) · two pointers on
  sorted input (Two Sum sorted is O(n)/O(1), no map) · **mark in the input itself** when values are
  bounded by n. Always ask first: ***may I modify the input?*** — every O(1)-space answer destroys
  it.
- **First Missing Positive is the flagship.** The answer is bounded by **n + 1** (n numbers: either
  they are exactly 1..n, or one of 1..n is missing). Three passes: clean out-of-range to `n+1` ·
  mark slot `v-1` with **`-abs(...)`, never `-x`** (on `[1, 1]` plain negation returns 1 instead of
  2) · return the first positive index + 1.
- **Direct addressing needs *dense* keys, not just integer ones.** `[0]*26` for letters is right;
  `[0]*(max+1)` on `[1, 2, 10**9]` is 8 GB and a `MemoryError`. Memory per million ints: **list 7 MB
  · set 32 MB · dict 40 MB**. And below ~8-16 elements, just scan — at n = 8 a set wins by only 1.8×
  before you count building it.
- **A map answers one question: is this key present?** Smallest, k-th, next, previous and range are
  all O(n) scans against it — use `bisect` on a sorted list, `heapq`, or `SortedList` (Python has no
  `TreeMap`). And its O(1) is an *average*: where you must promise a bound, a guaranteed O(log n) can
  beat a faster average.
