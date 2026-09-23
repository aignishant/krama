---
day: 37
track: dsa
title: "Prefix sums: answering range queries instantly"
phase: "Prefix sums"
status: written
---

# Day 037 · DSA — Prefix sums: answering range queries instantly

**After today you can:** You can precompute once and then answer any range-sum question in O(1).

**The interviewer asks it as:** *Answer many range-sum queries on a fixed array.*

---

## 1. What this is, and why they ask it

A **prefix sum** is a running total: for each position, the sum of everything up to it. Build that
once, in one pass, and the sum of *any* stretch of the array becomes a single subtraction — the
total up to the stretch's end, minus the total up to just before its start. One `O(n)` preparation
buys unlimited `O(1)` answers.

This opens a new phase because it is a new *kind* of idea. The window days made one pass clever;
prefix sums **precompute** — spend memory and preparation time now so that questions cost nothing
later. That trade is everywhere in computing, and interviewers use this family to see whether you
recognise it: the tell is *many queries against data that does not change*. Range Sum Query —
LeetCode 303 — is the direct form, easy to code and easy to get subtly wrong at index zero. And
tomorrow this same running total plus [day 021](../day-021-frequency-maps/README.md)'s map solves
the subarray-sum problems that yesterday's windows could not touch — the negatives case has been
waiting since [day 032](../day-032-variable-window/README.md).

---

## 2. The story

Ramu drives a delivery van for a wholesale cloth merchant, the same route every day: the godown,
then eleven shops strung along the highway, ending at the big showroom in the next town.

The owner is a man for questions. How far is it from the third shop to the seventh? From the godown
to the fifth? If we drop the ninth shop and go straight from the eighth to the tenth, what does that
save? He asks because diesel is money and the van is old.

For the first month, Ramu answered the slow way. He knew every leg of the route — godown to first
shop four kilometres, first to second seven, second to third three — so for each question he would
add the legs up in his head, one by one, from the start of the stretch to the end. Third shop to
seventh meant adding four legs. The owner never asked just one question, either. He asked six or
seven in a row, and Ramu stood there adding.

Then Ramu noticed the van had been keeping a better answer all along. The meter behind the steering
wheel only ever counts up, and one morning, on a whim, he noted the reading into his phone at every
stop. Leaving the godown: 40,180. First shop: 40,184. Second: 40,191. Third: 40,194. All the way to
the showroom.

Now every question is one subtraction. Third shop to seventh? Reading at the seventh minus reading
at the third. Done before the owner finishes the sentence. It does not matter whether the stretch
covers two stops or all eleven — one subtraction, always the same speed.

The detail he learnt to be careful about: the godown reading, the 40,180 from **before the first
shop**. The first time he forgot to note it, every question that started from the beginning of the
route — godown to anywhere — had no answer, because there was nothing to subtract. The list in his
phone starts with the reading at the start of the day, before anything has been driven at all.

---

## 3. The idea in plain English

Ramu's legs between shops are the array. His noted meter readings are the **prefix sums** — and his
godown reading, taken before anything was driven, is the extra zero at the front that today's code
lives or dies by.

### From legs to readings

Take a seven-element array of leg lengths:

```python
nums = [4, 7, 3, 6, 2, 5, 1]
```

The prefix sums are the meter readings — what the counter shows *after* each leg, starting from the
reading before any leg at all:

```python
prefix = [0, 4, 11, 14, 20, 22, 27, 28]
```

`prefix[i]` is the sum of the **first `i` elements** — `prefix[3]` is `4 + 7 + 3 = 14`, the reading
after three legs. The array has 7 elements; `prefix` has 8, because the reading before the first
leg — the plain 0 — is a real entry. That extra entry is called a **sentinel**: a value placed at
the boundary so that the boundary needs no special treatment.

### The subtraction

The sum of any stretch is reading-at-the-end minus reading-before-the-start:

```
sum of nums[i..j]  =  prefix[j + 1] - prefix[i]
```

Sum of `nums[2..4]` — the stretch `3, 6, 2` — is `prefix[5] - prefix[2] = 22 - 11 = 11`. The `+ 1`
is not decoration: `prefix[j + 1]` is the reading *after* element `j`, and `prefix[i]` is the
reading *before* element `i`, so the difference is exactly the elements from `i` to `j`, both ends
included. Say the formula as a sentence — *after the end, minus before the start* — and the
off-by-ones lose their grip.

And the sentinel earns its place at `i = 0`: sum of `nums[0..3]` is `prefix[4] - prefix[0] =
20 - 0`. Without the leading zero there is no "before the start" reading for stretches that begin
at the beginning — Ramu's forgotten godown reading — and §7 shows the two distinct ways that bug
bites.

### Why this is a new kind of tool

Every day since 27 has answered one question in one pass. Today's shape is different:

```
prepare once:  O(n)      — build the readings
answer often:  O(1) each — one subtraction per question
```

The trade is worth it exactly when the data holds still and the questions keep coming — **many
queries, fixed array** is the tell in the problem statement. One query only? The plain loop is
already optimal; building the prefix first is ceremony. Data that changes between queries? Every
change invalidates readings to its right, and rebuilding is `O(n)` per change — the honest
limitation, and the interviewer's favourite follow-up.

### The running-total form

Half the problems in this family never store the prefix array at all — they carry the running total
in one variable, updating it as they walk, and consult it on the spot. *Find the Pivot Index* —
LeetCode 724 — asks for the position where the sum on the left equals the sum on the right. With
`total` known, the right side is always `total - left_sum - nums[i]`, so one walk with one running
number settles it. Same idea, `O(1)` extra space — the stored array is for when *later* questions
need *arbitrary* stretches; the running variable is for when the walk itself is the only customer.

---

## 4. The picture

The array and its readings, boundaries marked:

```
 index          0     1     2     3     4     5     6
              +-----+-----+-----+-----+-----+-----+-----+
 nums         |  4  |  7  |  3  |  6  |  2  |  5  |  1  |
              +-----+-----+-----+-----+-----+-----+-----+

 prefix    0     4    11    14    20    22    27    28
           ^                                         ^
        before                                    after
        everything                                everything

 prefix has one entry per BOUNDARY, not per element: 8 entries for 7 elements.
```

**What to notice:** the readings live on the boundaries between elements — that is why there is one
more reading than there are elements, and why the leading 0 is not padding but the first boundary.

The subtraction, drawn:

```
 sum of nums[2..4]  =  prefix[5] - prefix[2]  =  22 - 11  =  11

              +-----+-----+-----+-----+-----+-----+-----+
 nums         |  4  |  7  |  3  |  6  |  2  |  5  |  1  |
              +-----+-----+-----+-----+-----+-----+-----+
                          |<--- wanted --->|
           0     4    11    14    20    22    27    28
                       ^                 ^
                  prefix[2]         prefix[5]
                  before start      after end

 everything up to the end of the stretch,
 minus everything before it began — the wanted part is what remains.
```

**What to notice:** both readings already existed. No element of the stretch was visited to answer
the question — that is where the `O(1)` comes from.

---

## 5. The code, built step by step

### Building the readings

```python
prefix = [0] * (len(nums) + 1)
for i, x in enumerate(nums):
    prefix[i + 1] = prefix[i] + x
```

One pass. Each reading is the previous reading plus the leg just driven — `prefix[i + 1] =
prefix[i] + nums[i]` — and the sentinel 0 is written before the loop by the initialisation itself.

The standard library builds it too, and in an interview you would say so:

```python
from itertools import accumulate

prefix = list(accumulate(nums, initial=0))
```

`accumulate` yields running totals; `initial=0` supplies the sentinel. Write the loop today so the
`+ 1` lives in your hands once; use `accumulate` from tomorrow.

### Answering a query

```python
def range_sum(i: int, j: int) -> int:
    return prefix[j + 1] - prefix[i]     # after the end, minus before the start
```

That is the entire query path. No loop anywhere near it.

### Range Sum Query as the interview asks it

LeetCode 303 wraps this in a class — build once in the constructor, subtract in the method:

```python
class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.prefix = list(accumulate(nums, initial=0))

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

The class shape *is* the lesson: the expensive work happens once, where it can be amortised; the
method the caller hammers is a subtraction.

### The pivot index, with a running total

```python
total = sum(nums)
left_sum = 0
for i, x in enumerate(nums):
    if left_sum == total - left_sum - x:
        return i
    left_sum += x
```

`left_sum` is the reading just before `i`; the right side is everything minus the left minus the
element itself. Check *before* adding — the element at `i` belongs to neither side. Note the edge
this order gets right for free: on `[2, 1, -1]` the answer is index 0, whose left side is the empty
sum 0.

### The complete solutions

```python
from itertools import accumulate


def build_prefix(nums: list[int]) -> list[int]:
    """Readings at every boundary: prefix[i] = sum of the first i elements."""
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return prefix


class NumArray:
    """LeetCode 303. Build once, subtract forever."""

    def __init__(self, nums: list[int]) -> None:
        self.prefix = list(accumulate(nums, initial=0))

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


def pivot_index(nums: list[int]) -> int:
    """LeetCode 724. The running-total form: no stored array needed."""
    total = sum(nums)
    left_sum = 0
    for i, x in enumerate(nums):
        if left_sum == total - left_sum - x:
            return i
        left_sum += x
    return -1


if __name__ == "__main__":
    nums = [4, 7, 3, 6, 2, 5, 1]
    prefix = build_prefix(nums)
    print(prefix)                        # [0, 4, 11, 14, 20, 22, 27, 28]
    print(prefix[5] - prefix[2], sum(nums[2:5]))    # 11 11
    print(prefix[4] - prefix[0], sum(nums[0:4]))    # 20 20  <- the sentinel at work

    arr = NumArray([-2, 0, 3, -5, 2, -1])
    print(arr.sumRange(0, 2), arr.sumRange(2, 5), arr.sumRange(0, 5))   # 1 -1 -3

    print(pivot_index([1, 7, 3, 6, 5, 6]))   # 3
    print(pivot_index([2, 1, -1]))           # 0  <- empty left side counts
    print(pivot_index([1, 2, 3]))            # -1
```

Note the `NumArray` test: negatives everywhere, and nothing anywhere in today's code cares. The
subtraction never needed the values to be positive — which is exactly what
[day 032](../day-032-variable-window/README.md)'s windows could not say, and why tomorrow exists.

---

## 6. What it costs

### Build, then query

```
build:  one pass over n elements, one addition each          -> O(n) time
store:  n + 1 readings                                       -> O(n) extra space
query:  two lookups and one subtraction, regardless of span  -> O(1) each
```

### The comparison that sells it

`q` queries on an array of length `n`, summing each stretch by loop against subtracting readings:

```
n = 100,000 and q = 100,000, stretches averaging n/2 long:

loop per query : 100,000 × 50,000  = 5,000,000,000 additions
prefix         : 100,000 build  +  100,000 × 1  ≈  200,000 operations

25,000 times less work — bought with one array of 100,001 numbers.
```

Say the trade explicitly: **O(n) memory purchased a 25,000× speedup.** Interviewers want the cost
named on both sides, not just the win.

### When the trade goes wrong

One query only: the loop costs `n` and the prefix costs `n` to build *plus* the query — no win,
just ceremony. Updates between queries: one changed element invalidates every reading to its right,
so each update costs `O(n)` rebuild; at that point the honest answers are "rebuild if updates are
rare" or "a Fenwick or segment tree if they are not" — name them, both `O(log n)` per operation,
and say they are beyond today's scope. Recognising *when the tool loses* is worth as much as the
tool.

### The number to have ready

> Build once in O(n), answer each range in O(1) — for a hundred thousand queries on a hundred
> thousand elements that is two hundred thousand operations against five billion. Cost: one extra
> array, and the array must hold still — an update invalidates everything to its right.

---

## 7. The traps

### The near-miss: skipping the sentinel

Build the readings without the leading zero and use the tempting formula `prefix[j] - prefix[i - 1]`:

```python
prefix = list(accumulate(nums))          # length n — no leading zero
def range_sum(i, j):
    return prefix[j] - prefix[i - 1]

print(range_sum(2, 5), sum(nums[2:6]))
print(range_sum(0, 3), sum(nums[0:4]))
```

```
19 19
-22 9
```

Interior stretches come out right, which is what makes this version survive a casual test. Any
stretch starting at 0 reaches for `prefix[-1]` — the **last** reading, by Python's negative
indexing — and returns garbage with no error. Third appearance of this exact trap, after
[day 021](../day-021-frequency-maps/README.md) and [day 035](../day-035-choosing-the-pattern/README.md):
an index that can reach −1 is a bug that does not crash. The sentinel exists precisely so `i = 0`
subtracts a real, honest 0.

### The real error: the sentinel forgotten the other way

Keep the zero-less array but use today's formula:

```python
prefix = list(accumulate(nums))          # length 8, no leading zero
print(prefix[7 + 1] - prefix[2])         # sum of nums[2..7]
```

```
Traceback (most recent call last):
  File "day37.py", line 4, in <module>
    print(prefix[7 + 1] - prefix[2])         # sum of nums[2..7]
          ~~~~~~^^^^^^^
IndexError: list index out of range
```

The formula assumes `n + 1` readings; the array has `n`. Same root cause as the silent version —
**the sentinel and the formula are a set**. Adopt them together: `initial=0`, size `n + 1`, and
`prefix[j + 1] - prefix[i]`, always, and neither failure can exist.

### The near-miss: answering queries after the array changed

```python
arr = NumArray([4, 7, 3, 6])
nums_changes_somewhere_else()            # element 1 becomes 9
print(arr.sumRange(0, 2))                # still answers 14 — built from the old values
```

No error, ever — the readings are a snapshot, and they go stale the moment the array moves.
LeetCode splits this into two problems deliberately: 303 is immutable, and 307 — *Range Sum Query,
Mutable* — exists because the answer changes completely. If the interviewer says "now support
updates", the correct first sentence is that the prefix array's deal is off, not a patch to it.

### The contract corner: which ends are included

"Sum from i to j" — inclusive of both? Half-open? The formula differs by one at each end, and both
conventions are common. Ask, then anchor yourself with the sentence: *after the end, minus before
the start*. For inclusive `[i, j]` that is `prefix[j + 1] - prefix[i]`; for half-open `[i, j)` it
is `prefix[j] - prefix[i]`. One clarifying question, ten seconds, and the whole class of off-by-one
bugs never happens.

### The near-miss: overflow, elsewhere

In Python the running total grows without limit — `int` is arbitrary precision, from
[day 005](../day-005-python-lists-and-tuples/README.md). In Java or C++ the prefix of a large array of large
values overflows a 32-bit `int` silently. Worth one sentence in an interview if the interviewer's
language is not Python: "I'd hold the prefix in a 64-bit type." It signals you know where the trap
is even when your language hides it.

---

## 8. In the interview

### How it gets asked

- *"Given an array, answer q queries: the sum from index i to j."* — the direct form, LeetCode 303.
- *"Design a class that returns range sums efficiently."* — the same thing wearing design clothes;
  the constructor/method split is the answer.
- *"Find the index where the left sum equals the right sum."* — LeetCode 724, the running-total
  form.
- And as a **component**: "as a first step I'll build a prefix array" inside harder problems —
  tomorrow's subarray-sum family, [day 039](../day-039-difference-arrays/README.md)'s updates,
  [day 040](../day-040-2d-prefix-sums/README.md)'s matrices. From today, prefix sums are vocabulary.

### What to say out loud, in the first ninety seconds

1. **Spot the tell and say it.** *"Many queries, and the array doesn't change — that's a
   precompute-once shape. I'll trade O(n) memory for O(1) per query."*
2. **Name the object.** *"I'll build a prefix array: prefix[i] is the sum of the first i elements —
   n + 1 entries, with a 0 sentinel at the front so queries touching index 0 need no special
   case."*
3. **Give the formula as a sentence.** *"A range sum is: after the end minus before the start —
   prefix[j + 1] minus prefix[i], both ends inclusive."*
4. **Confirm the contract.** *"Are both ends inclusive? And can queries repeat / can the array
   change between them?"*
5. **State the costs, both sides.** *"O(n) build and O(n) extra space, then O(1) per query — for a
   hundred thousand queries that's two hundred thousand operations against five billion by
   looping."*

### The follow-ups

**"What if the array can be updated between queries?"**
Then the prefix array's contract is broken — changing one element invalidates every reading to its
right, so keeping it current costs O(n) per update, and I would say so before proposing anything.
The decision is a ratio: with very rare updates and floods of queries, rebuild on update and keep
O(1) reads. With mixed traffic, the standard tools are a Fenwick tree or a segment tree — both keep
running totals in a tree shape so that update and query are each O(log n). I would name them,
say the trade — O(1) queries with unpayable updates, against O(log n) for both — and ask which the
problem wants before coding either, since they are a step up in implementation weight and this
course meets trees properly later.

**"Why the extra zero at the front? Can't you handle i = 0 with an if?"**
You can — `return prefix[j] if i == 0 else prefix[j] - prefix[i - 1]` — and it is strictly worse in
three small ways. It doubles the surface for off-by-one mistakes, because now two formulas must
each be right instead of one. It hides the meaning: with the sentinel, prefix has one entry per
*boundary*, and a range sum is always after-the-end minus before-the-start, one rule with no
exceptions. And the failure mode of getting it wrong is vicious: without the guard, `prefix[i - 1]`
at `i = 0` is `prefix[-1]` — Python reads the *last* element, silently — so the bug ships instead of
crashing. A sentinel that removes a special case is nearly always worth one extra slot; this is the
cleanest example of that principle I know, and it is why I write `initial=0` reflexively.

**"The queries arrive faster than you can precompute — say, the first query comes immediately."**
Build lazily or build anyway — and mostly build anyway, because the numbers say so: the build is
one pass, and at a hundred thousand elements it is a fraction of a millisecond, cheaper than a
single looped query over a long stretch. If the input is truly enormous and the first response
matters, I can answer the first query with a direct loop while building, or build incrementally —
extend the readings only as far as the furthest index any query has touched, since a query needs
only prefix values up to j + 1. That keeps worst-case work the same and front-loads nothing. The
deeper point I would make: this is an amortisation question — the build cost divided by the query
count is the real per-query price, and it falls toward zero as queries arrive.

### A model answer

> "Many range-sum queries on an array that doesn't change — so I'll precompute. One O(n) pass
> builds a prefix array where prefix[i] is the sum of the first i elements; it has n + 1 entries
> because I include a 0 at the front, the sum of nothing, so that ranges starting at index 0 fall
> out of the same formula as everything else.
>
> Then any query is one subtraction: the sum from i to j inclusive is prefix[j + 1] minus
> prefix[i] — everything up to and including the end, minus everything before the start.
>
> ```python
> class NumArray:
>     def __init__(self, nums):
>         self.prefix = list(accumulate(nums, initial=0))
>     def sumRange(self, left, right):
>         return self.prefix[right + 1] - self.prefix[left]
> ```
>
> Costs on both sides of the trade: O(n) once to build, O(n) extra space held for the object's
> lifetime, and O(1) per query after that. For a hundred thousand queries on a hundred thousand
> elements that's about two hundred thousand operations, against five billion if each query
> loops.
>
> Two things I'd flag. Negative values are completely fine — the subtraction never cared about
> sign, which matters because sliding windows can't say that. And the deal requires the array to
> hold still: one update invalidates every reading to its right. If updates arrive, I'd say the
> options out loud — rebuild if they're rare, or a Fenwick or segment tree for O(log n) both ways —
> rather than quietly patching a structure whose contract has changed."

---

## 9. Recall card

- **prefix[i] = sum of the first i elements** — n + 1 entries, one per *boundary*, sentinel 0 in
  front. `accumulate(nums, initial=0)`.
- **Range sum = after the end minus before the start:** `prefix[j + 1] - prefix[i]` for inclusive
  `[i, j]`. Say the sentence, not the indices.
- **The trade: O(n) build and space buys O(1) per query** — worth it when queries are many and the
  array holds still; one update invalidates everything to its right.
- **Without the sentinel:** ranges from 0 read `prefix[-1]` — the last element, silently. The
  sentinel and the formula are a set; adopt both or neither.
- **Negatives are fine here** — which windows could not say. Tomorrow: prefix + hash map counts
  subarrays summing to k, negatives included.
