---
day: 56
track: dsa
title: "Counting sort, radix sort, and bucket sort"
phase: "Sorting"
status: written
---

# Day 056 · DSA — Counting sort, radix sort, and bucket sort

**After today you can:** You can sort in O(n) when the values are bounded, and say exactly when that is allowed.

**The interviewer asks it as:** *Sort a million integers in the range 0 to 100. Can you beat n log n?*

---

## 1. What this is, and why they ask it

Every sort so far has worked by comparing two values and asking which is bigger. Today's three do
not. Counting sort counts how many of each value there are and then writes them out in order. Radix
sort does that one digit at a time. Bucket sort drops values into ranges and sorts each range. None
of them ever compares two elements of the input with each other, and that is why they can run in
`O(n)` — because the `n log n` limit applies only to sorts that compare.

They ask it because it is the clearest test of whether you look at the *data* before choosing an
algorithm. "Sort a million integers between 0 and 100" is a question with a trap in it: the trap is
answering `O(n log n)`, which is correct and slower than necessary. The information you were handed —
the range is a hundred — is the whole question. It also gets asked as the follow-up to almost any
sorting question ("could you do better if the values were bounded?"), and radix sort in particular is
the reason [day 057](../day-057-stability-and-pythons-sort/README.md)'s stability matters: radix
sort is *built* out of stability, and without it the whole thing silently produces garbage.

---

## 2. The story

Rafiq works the night shift at a courier depot on the edge of Nagpur, and between about nine at night
and four in the morning roughly four thousand parcels have to end up sorted by the six-digit code
written on each label, so the vans can be loaded route by route at first light.

He never holds up two parcels and compares them. Not once, all night. When his nephew came to help
and started doing that — picking up two, deciding which came first, putting one down — Rafiq stopped
him after ten minutes and showed him the rack.

The rack has ten open pigeonholes along a wall, numbered zero to nine, and it is the whole method.

He takes a parcel, looks at the **last** digit of the code, and pushes it into the hole with that
number. One look. He does not think about the other five digits and he does not think about the
parcel he handled before. Four thousand parcels, four thousand looks, and by about ten o'clock the
whole night's load is sitting in ten piles.

Then he empties the rack. Hole zero first, then hole one, then two, all the way to nine, stacking
them onto a trolley in that order — and this is the part that matters — keeping each hole's parcels
in exactly the order they went in. Nothing gets turned over, nothing gets shuffled.

Then he runs the whole trolley past the rack again, this time looking at the **second-to-last** digit.
Then the third. Six passes in all, one per digit, and at the end of the sixth pass the trolley comes
off in perfect code order, and he still has not compared one parcel to another.

The night it went wrong was in February, when a new boy emptied one of the holes by tipping the whole
pile upside down onto the trolley. The result was not obviously wrong. It looked sorted. It was
sorted by the last two digits and scrambled underneath, and three vans went out with the wrong bundles
and Rafiq had to explain to the supervisor at six in the morning why something that looked completely
fine was completely wrong.

Now he tells everyone the same thing on their first night. It does not matter how you put them in.
What matters is that when you take them out, they come out in the order they went in. That one rule
is the only reason the six passes add up to anything.

---

## 3. The idea in plain English

Rafiq's rack is counting sort. Six passes over the rack, one digit at a time, is radix sort. And the
new boy tipping the pile upside down is what happens when your sort is not **stable**.

### First, the fact that makes today possible

Every sort you have written so far decides everything by asking "is `a` bigger than `b`?" There is a
known limit on how fast that can possibly be: **no sort that works purely by comparing pairs of
elements can be faster than `O(n log n)`.** That is not a limitation of merge sort or quicksort in
particular; it is a limit on the whole approach.

Today's sorts escape it by not comparing. They use the value itself as a position. If you know a
value is 47, you do not need to ask anything about it — you already know where it goes. That extra
information has to come from somewhere, and it comes from a restriction: **you must know the range of
the values in advance, and it must be small.**

### Counting sort

Suppose you have a million exam marks, each between 0 and 100.

**Step one: count.** Make a list of 101 counters, all zero. Walk the input once, and for each mark
add one to the counter with that number. One pass, one addition each.

```
 input  [ 3, 1, 4, 1, 5, 1, 4 ]        values are 0..5

 counts  index   0   1   2   3   4   5
                +---+---+---+---+---+---+
                | 0 | 3 | 0 | 1 | 2 | 1 |
                +---+---+---+---+---+---+
                      ^           ^
                 three 1s      two 4s
```

**Step two: write them out.** Walk the counters from 0 upwards and write each value out as many
times as its count says.

```
 output  [ 1, 1, 1, 3, 4, 4, 5 ]
```

Done. No comparisons anywhere. The cost is one pass over `n` values plus one pass over `k` counters,
which is **`O(n + k)`** where `k` is the size of the range.

That simple version works when the thing you are sorting *is* the number. Usually it is not — you are
sorting records by a key, and you need the whole record to move with it. Then you need one more step.

**Step two and a half: turn counts into positions.** Replace each counter with the running total of
itself and everything before it. Each counter then says *how many values are less than or equal to
this one* — which is one past the last position where that value belongs.

```
 counts    [ 0, 3, 0, 1, 2, 1 ]
 running   [ 0, 3, 3, 4, 6, 7 ]      <- how many values are <= this one
                ^           ^
     three values <= 1      six values <= 4, so the 4s END at 6
     so the 1s fill 0,1,2      i.e. they sit at positions 4 and 5
```

**Step three: place each element, walking the input backwards.** For each element, decrement its
counter first, then write the element at that position.

Both directions matter and they must agree. Each value's block is filled from its **right-hand end**,
and the input is read from its **right-hand end**, so the last equal element in the input lands in
the last of its slots and the original relative order survives. Reverse either direction and the sort
is still correct on bare numbers but silently stops being stable — which is the new boy tipping the
pile upside down, and it destroys radix sort three passes later.

### Radix sort

Counting sort is `O(n + k)`, so it is only good when `k` is small. Sorting a million values in the
range 0 to 4,000,000,000 would need four billion counters, which is not possible.

Radix sort fixes that. Instead of sorting by the whole value at once, sort by **one digit at a time**,
starting from the least significant, using a stable sort for each pass. Ten counters per pass instead
of four billion.

```
 input        329   457   657   839   436   720   355

 pass 1, by the LAST digit:
              720   355   436   457   657   329   839
                ^     ^     ^     ^     ^     ^     ^
                0     5     6     7     7     9     9      <- in digit order

 pass 2, by the MIDDLE digit:
              720   329   436   839   355   457   657

 pass 3, by the FIRST digit:
              329   355   436   457   657   720   839      <- sorted
```

Look at pass 2 carefully. `457` and `657` both have a middle digit of 5, and `457` stayed in front of
`657` because pass 1 had already put it there. **That is stability doing the actual work.** If pass 2
had reordered them, pass 1's result would have been thrown away, and after three passes the list
would be sorted by the first digit only and scrambled underneath — exactly Rafiq's February.

The cost is `d` passes of `O(n + b)` each, where `d` is the number of digits and `b` is the base
(usually 10, or 256 if you work a byte at a time). That is **`O(d × (n + b))`**, and since `d` and `b`
are constants for a fixed integer width, it is `O(n)`.

### Bucket sort

The third one, and the one with the most conditions attached. Split the value range into `n` equal
buckets, drop each value into the bucket its value falls in, sort each bucket with anything you like
(insertion sort, because buckets are tiny), then read the buckets out in order.

```
 values in [0, 1):   0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21

 bucket 0 [0.0-0.1) :
 bucket 1 [0.1-0.2) : 0.17
 bucket 2 [0.2-0.3) : 0.26, 0.21
 bucket 3 [0.3-0.4) : 0.39
   ...
 bucket 7 [0.7-0.8) : 0.78, 0.72
 bucket 9 [0.9-1.0) : 0.94

 sort each small bucket, then read left to right
```

This is `O(n)` **only if the values are spread out evenly.** If they are not — if every value falls
into one bucket — you have done `O(n)` work to hand one bucket of `n` elements to insertion sort, and
the whole thing is `O(n²)`. Bucket sort is the one whose complexity depends on the shape of your data
rather than just its range, and that condition must be said out loud whenever you propose it.

### When you are allowed to use each

| | Use it when | Cost | Space |
|---|---|---|---|
| **Counting sort** | Integer keys in a small known range (marks, ages, days, statuses) | `O(n + k)` | `O(n + k)` |
| **Radix sort** | Fixed-width integers or equal-length strings | `O(d(n + b))` | `O(n + b)` |
| **Bucket sort** | Values known to be uniformly spread over a range | `O(n)` average, `O(n²)` worst | `O(n)` |

The one sentence to have ready: **"These are not general-purpose sorts. They buy `O(n)` by requiring
something about the keys, and if you cannot state that requirement, you cannot use them."**

---

## 4. The picture

Counting sort, all three steps, on marks out of 5:

```
 STEP 1 — count             input: [ 3, 1, 4, 1, 5, 1, 4 ]

   value    0   1   2   3   4   5
          +---+---+---+---+---+---+
   count  | 0 | 3 | 0 | 1 | 2 | 1 |        one pass over n, one addition each
          +---+---+---+---+---+---+

 STEP 2 — running totals: how many values are <= v?

          +---+---+---+---+---+---+
   count  | 0 | 3 | 0 | 1 | 2 | 1 |
          +---+---+---+---+---+---+
   <= v   | 0 | 3 | 3 | 4 | 6 | 7 |        count[v] += count[v-1], left to right
          +---+---+---+---+---+---+
                ^           ^
      three values <= 1     six values <= 4
      so the 1s occupy      so the 4s END at position 6,
      positions 0,1,2       i.e. they sit at 4 and 5

 STEP 3 — place, walking the INPUT BACKWARDS, decrementing before writing

   read 4 (last)  -> count[4] 6 -> 5 -> output[5] = 4
   read 1         -> count[1] 3 -> 2 -> output[2] = 1
   read 5         -> count[5] 7 -> 6 -> output[6] = 5
   read 1         -> count[1] 2 -> 1 -> output[1] = 1
   read 4         -> count[4] 5 -> 4 -> output[4] = 4
   read 1         -> count[1] 1 -> 0 -> output[0] = 1
   read 3 (first) -> count[3] 4 -> 3 -> output[3] = 3

   output  index   0   1   2   3   4   5   6
                 +---+---+---+---+---+---+---+
                 | 1 | 1 | 1 | 3 | 4 | 4 | 5 |
                 +---+---+---+---+---+---+---+
```

**What to notice:** the two 4s and the direction of travel. Each value's block is filled from its
**right-hand end**, and the input is read from its **right-hand end** — so the 4 that came last in
the input lands at position 5, and the 4 that came earlier lands at position 4. The original order
survives. Reverse either one of those two directions and the sort is still correct on bare numbers
but no longer stable, which is the bug in §7 and the one that silently destroys radix sort.

Radix sort, and where stability does the work:

```
 pass 2, sorting by the middle digit

   coming in (already sorted by the last digit):
        720   355   436   457   657   329   839
                          ^^^   ^^^
                     both have middle digit 5

   going out:
        720   329   436   839   355   457   657
                                      ^^^   ^^^
                     457 STILL comes before 657

   why: pass 1 put 457 before 657, and a stable sort does not disturb
        elements whose keys are equal. Pass 2 only reorders by the middle
        digit; anything it does not distinguish keeps pass 1's order.

   with an UNSTABLE sort in pass 2, 657 might come out before 457,
   and pass 1's work is destroyed. No error. Just a wrong answer.
```

**What to notice:** radix sort has no correctness of its own. It is entirely borrowed from the
stability of the sort used in each pass. That is the single most important sentence about it.

The three sorts against the comparison sorts, drawn on the same axis:

```
  n = 1,000,000 values

  values are 0..100          counting sort   n + k = 1,000,100 ops       BEST
                             quicksort       n log n = 20,000,000        20x more

  values are 0..4,000,000,000
                             counting sort   4 BILLION counters  -> MemoryError
                             radix sort      10 passes x (n + 10) = 10,000,100
                             quicksort       20,000,000                  2x more

  values are arbitrary floats, no known range
                             counting sort   impossible
                             radix sort      possible but fiddly
                             quicksort       20,000,000                  THE ANSWER

  values are objects with a custom comparison
                             counting/radix  impossible -- there is no "digit"
                             quicksort       20,000,000                  THE ANSWER
```

**What to notice:** two of the four rows say "the answer is the comparison sort". The skill being
tested is not knowing counting sort; it is knowing which row you are in.

---

## 5. The code, built step by step

### Counting sort, the simple version

When you are sorting bare numbers and nothing rides along with them:

```python
def counting_sort_simple(nums: list[int], max_value: int) -> list[int]:
    """Values must be 0..max_value. O(n + k). Not usable for records with keys."""
    counts = [0] * (max_value + 1)
    for x in nums:
        counts[x] += 1                       # one look per element, no comparisons
    out: list[int] = []
    for value, count in enumerate(counts):
        out.extend([value] * count)          # write each value out `count` times
    return out
```

Four lines of real work. `counts[x] += 1` is the whole idea: the value *is* the position. Note there
is no comparison anywhere in this function — not one `<` or `>`.

### Counting sort, the stable version

The simple version cannot carry a record along with its key, and it cannot be used inside radix sort.
The real version places elements rather than regenerating them:

```python
def counting_sort(nums: list[int], max_value: int) -> list[int]:
    """Stable. O(n + k) time, O(n + k) space."""
    counts = [0] * (max_value + 1)
    for x in nums:
        counts[x] += 1
    for v in range(1, max_value + 1):
        counts[v] += counts[v - 1]           # counts[v] is now: how many are <= v
    out = [0] * len(nums)
    for x in reversed(nums):                 # BACKWARDS -- this is what keeps it stable
        counts[x] -= 1
        out[counts[x]] = x
    return out
```

Three things to say about this while writing it.

`counts[v] += counts[v - 1]` turns the counts into a **running total**, so `counts[v]` now means "how
many elements are less than or equal to `v`" — which is one past the last position where a `v`
belongs.

`for x in reversed(nums)` is the stability step. Because `counts[x]` holds the position just past the
end of `x`'s block, decrementing first and then writing fills the block from the right. Reading the
input from the right at the same time means the last equal element lands in the last slot, so
original order is preserved. **Change `reversed(nums)` to `nums` and every group of equal elements
comes out reversed** — no error, no crash.

### Handling negative numbers and a shifted range

Counting sort assumes values start at 0. Real data rarely does:

```python
def counting_sort_range(nums: list[int]) -> list[int]:
    """Works for any integer range, including negatives. O(n + k), k = max - min + 1."""
    if not nums:
        return []
    low, high = min(nums), max(nums)
    counts = [0] * (high - low + 1)
    for x in nums:
        counts[x - low] += 1                 # shift so the smallest value maps to 0
    out: list[int] = []
    for offset, count in enumerate(counts):
        out.extend([offset + low] * count)   # shift back on the way out
    return out
```

The `- low` and `+ low` pair is the whole fix. Notice that `k` is now `max − min + 1`, so a list
containing `0` and `1_000_000_000` needs a billion counters even if it only has two elements. That is
the failure in §7.

### Radix sort

```python
def counting_sort_by_digit(nums: list[int], exponent: int) -> list[int]:
    """One stable pass, sorting by the digit at 10**exponent."""
    counts = [0] * 10
    for x in nums:
        counts[(x // exponent) % 10] += 1
    for d in range(1, 10):
        counts[d] += counts[d - 1]
    out = [0] * len(nums)
    for x in reversed(nums):                 # stable, and radix depends on it
        digit = (x // exponent) % 10
        counts[digit] -= 1
        out[counts[digit]] = x
    return out
```

`(x // exponent) % 10` extracts one digit: divide away the digits to the right, then take the
remainder to drop the digits to the left. For `x = 457` and `exponent = 10`, that is
`457 // 10 = 45`, then `45 % 10 = 5`. The middle digit.

```python
def radix_sort(nums: list[int]) -> list[int]:
    """O(d x (n + 10)) for d-digit non-negative integers. Stable."""
    if not nums:
        return []
    if min(nums) < 0:
        raise ValueError("radix_sort here handles non-negative integers only")
    out = list(nums)
    exponent = 1
    largest = max(out)
    while largest // exponent > 0:           # one pass per digit of the largest value
        out = counting_sort_by_digit(out, exponent)
        exponent *= 10
    return out
```

The loop condition is how you get the number of passes without computing it: keep going while there
are still digits left in the largest value. For a maximum of 4,000, that is four passes.

### Bucket sort

```python
def bucket_sort(values: list[float], bucket_count: int | None = None) -> list[float]:
    """O(n) when the values are uniformly spread. O(n^2) when they are not."""
    if not values:
        return []
    n = bucket_count or len(values)
    low, high = min(values), max(values)
    if high == low:
        return list(values)
    buckets: list[list[float]] = [[] for _ in range(n)]
    for v in values:
        index = int((v - low) / (high - low) * (n - 1))    # which bucket does v fall in
        buckets[index].append(v)
    out: list[float] = []
    for bucket in buckets:
        bucket.sort()                        # tiny, so any sort will do
        out.extend(bucket)
    return out
```

`(n - 1)` rather than `n` in the index calculation, so the maximum value maps to the last bucket
rather than one past the end. That single `- 1` is the difference between working and an
`IndexError`.

### The complete file

```python
"""Three sorts that never compare two elements, and the conditions they demand."""


def counting_sort(nums: list[int], max_value: int) -> list[int]:
    """Stable counting sort for values 0..max_value. O(n + k) time and space.

    Use when: integer keys, small known range (marks 0-100, ages, weekdays, statuses).
    Do NOT use when: the range is large, the keys are not integers, or the range
    is unknown -- k is the range, not the count, and it decides everything.
    """
    if not nums:
        return []
    counts = [0] * (max_value + 1)
    for x in nums:
        counts[x] += 1
    for v in range(1, max_value + 1):
        counts[v] += counts[v - 1]           # running total: how many are <= v
    out = [0] * len(nums)
    for x in reversed(nums):                 # backwards keeps it STABLE
        counts[x] -= 1
        out[counts[x]] = x
    return out


def counting_sort_pairs(
    records: list[tuple[int, str]], max_key: int
) -> list[tuple[int, str]]:
    """The version that matters: sort records by an integer key, stably."""
    counts = [0] * (max_key + 1)
    for key, _ in records:
        counts[key] += 1
    for v in range(1, max_key + 1):
        counts[v] += counts[v - 1]
    out: list[tuple[int, str]] = [(0, "")] * len(records)
    for key, payload in reversed(records):
        counts[key] -= 1
        out[counts[key]] = (key, payload)
    return out


def counting_sort_range(nums: list[int]) -> list[int]:
    """Any integer range, negatives included. k = max - min + 1."""
    if not nums:
        return []
    low, high = min(nums), max(nums)
    counts = [0] * (high - low + 1)
    for x in nums:
        counts[x - low] += 1
    out: list[int] = []
    for offset, count in enumerate(counts):
        out.extend([offset + low] * count)
    return out


def counting_sort_by_digit(nums: list[int], exponent: int) -> list[int]:
    counts = [0] * 10
    for x in nums:
        counts[(x // exponent) % 10] += 1
    for d in range(1, 10):
        counts[d] += counts[d - 1]
    out = [0] * len(nums)
    for x in reversed(nums):
        digit = (x // exponent) % 10
        counts[digit] -= 1
        out[counts[digit]] = x
    return out


def radix_sort(nums: list[int]) -> list[int]:
    """Least-significant-digit radix sort. O(d x (n + 10)). Non-negative only.

    Correct ONLY because each pass is stable: a later pass never disturbs the
    relative order established by an earlier one.
    """
    if not nums:
        return []
    if min(nums) < 0:
        raise ValueError("radix_sort handles non-negative integers only")
    out = list(nums)
    exponent = 1
    largest = max(out)
    while largest // exponent > 0:
        out = counting_sort_by_digit(out, exponent)
        exponent *= 10
    return out


def bucket_sort(values: list[float], bucket_count: int | None = None) -> list[float]:
    """O(n) when values are uniformly distributed; O(n^2) when they cluster."""
    if not values:
        return []
    n = bucket_count or len(values)
    low, high = min(values), max(values)
    if high == low:
        return list(values)
    buckets: list[list[float]] = [[] for _ in range(n)]
    for v in values:
        buckets[int((v - low) / (high - low) * (n - 1))].append(v)
    out: list[float] = []
    for bucket in buckets:
        bucket.sort()
        out.extend(bucket)
    return out


def sort_by_age(people: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """The realistic use: ages are 0..120, so counting sort is O(n)."""
    counts = [0] * 121
    for _, age in people:
        counts[age] += 1
    for a in range(1, 121):
        counts[a] += counts[a - 1]
    out: list[tuple[str, int]] = [("", 0)] * len(people)
    for name, age in reversed(people):
        counts[age] -= 1
        out[counts[age]] = (name, age)
    return out


if __name__ == "__main__":
    print(counting_sort([3, 1, 4, 1, 5, 1, 4], 5))       # [1, 1, 1, 3, 4, 4, 5]
    print(counting_sort([], 5))                          # []
    print(counting_sort_range([-3, 7, -1, 0, 7]))        # [-3, -1, 0, 7, 7]

    print(radix_sort([329, 457, 657, 839, 436, 720, 355]))
    # [329, 355, 436, 457, 657, 720, 839]
    print(radix_sort([0, 0, 10, 1]))                     # [0, 0, 1, 10]

    print(bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21]))
    # [0.17, 0.21, 0.26, 0.39, 0.72, 0.78, 0.94]

    # stability, demonstrated -- the reason radix sort works at all
    records = [(2, "first"), (1, "x"), (2, "second"), (1, "y")]
    print(counting_sort_pairs(records, 2))
    # [(1, 'x'), (1, 'y'), (2, 'first'), (2, 'second')]
    #  'x' before 'y' and 'first' before 'second', exactly as in the input

    print(sort_by_age([("Asha", 34), ("Bala", 12), ("Chitra", 34), ("Devi", 7)]))
    # [('Devi', 7), ('Bala', 12), ('Asha', 34), ('Chitra', 34)]

    # the arithmetic that justifies it
    import random
    marks = [random.randint(0, 100) for _ in range(1_000_000)]
    #  counting sort : 1,000,000 + 101      = ~1,000,101 operations
    #  sorted()      : 1,000,000 x 20       = ~20,000,000 comparisons
    print(counting_sort(marks, 100)[:5], counting_sort(marks, 100)[-5:])
```

---

## 6. What it costs

### Counting sort, counted

```
 pass 1: count            n additions
 pass 2: running totals   k additions
 pass 3: place            n writes

 total = 2n + k  ->  O(n + k)
```

`k` is the **size of the range**, not the number of elements. That distinction is the whole subject:

```
 n = 1,000,000 marks in 0..100
     counting sort : 2 x 1,000,000 + 101   = 2,000,101 operations
     sorted()      : 1,000,000 x 20        = 20,000,000 comparisons
                                             -> 10x fewer operations

 n = 1,000 values in 0..1,000,000,000
     counting sort : 2 x 1,000 + 1,000,000,000  = a billion operations
                     and a list of a billion integers = ~8 GB
     sorted()      : 1,000 x 10 = 10,000
                                             -> counting sort is 100,000x WORSE
```

The rule that follows: **counting sort wins when `k` is comparable with `n` or smaller.** If `k` is
much larger than `n`, it is a catastrophe, and the failure mode is running out of memory rather than
being slow.

### Radix sort, counted

```
 d passes, each one a counting sort over base b:
    each pass = 2n + b
    total     = d x (2n + b)

 sorting 1,000,000 values up to 999,999 (d = 6 digits, b = 10):
    6 x (2,000,000 + 10) = 12,000,060 operations
    sorted()             = 20,000,000 comparisons
                          -> ~1.7x fewer, and each is cheaper (no comparisons)

 with base 256 (one byte at a time), a 32-bit integer is d = 4:
    4 x (2,000,000 + 256) = 8,001,024
                          -> 2.5x fewer than sorted()
```

The base is a tunable trade: a bigger base means fewer passes but more counters. Base 256 for 32-bit
integers is the usual compromise — four passes, 256 counters.

```
 base 10  : d = 10 passes for a 32-bit integer, 10 counters
 base 256 : d = 4  passes,                      256 counters
 base 65536: d = 2 passes,                      65,536 counters
```

### Bucket sort, and the condition

```
 n values, n buckets, uniformly distributed:
   distribute : n
   each bucket holds ~1 element, sorting it is ~1
   collect    : n
   total = O(n)

 n values, all landing in one bucket:
   distribute : n
   one bucket of n elements, insertion-sorted: n(n-1)/2
   total = O(n^2)

 n = 10,000 uniformly spread : ~20,000 operations
 n = 10,000 all in one bucket: ~50,000,000 operations   -> 2,500x worse
```

That is why "uniformly distributed" is not a footnote. Say it every time you propose bucket sort.

### Space

```
 counting sort : O(n + k)   -- the output list plus the counters
 radix sort    : O(n + b)   -- one output list, b counters, reused each pass
 bucket sort   : O(n)       -- the buckets hold every element once

 every one of them is O(n) or worse. NONE of these sorts in place.
```

That is the trade in one line: **these sorts buy time with memory and with a restriction on the
keys.** Quicksort's `O(1)` space is exactly what you give up.

### The real-world caveat

Python's `sorted()` is written in C. Your counting sort is written in Python. At `n = 1,000,000`
values in `0..100`:

```
 sorted(nums)              ~0.15 s   (C, 20,000,000 comparisons)
 counting_sort in Python   ~0.35 s   ( Python, 2,000,101 operations)
```

Ten times fewer operations, and still slower, because a Python bytecode operation costs roughly fifty
times a C one. **Say this out loud in an interview.** The asymptotic answer is counting sort; the
practical answer in Python is `sorted()` unless `n` is very large or you are using NumPy. Knowing
both, and knowing which question you are being asked, is the complete answer.

---

## 7. The traps

### The real error: the range decides the memory

```python
nums = [1, 5, 2_000_000_000]
print(counting_sort(nums, max(nums)))
```

```
Traceback (most recent call last):
  File "day56.py", line 2, in <module>
    print(counting_sort(nums, max(nums)))
          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "day56.py", line 9, in counting_sort
    counts = [0] * (max_value + 1)
             ~~~~~~^~~~~~~~~~~~~~~
MemoryError
```

Three elements, and it ran out of memory. `k` is the *range*, not the count — a list of two billion
counters is about sixteen gigabytes. **Always ask for the range before proposing counting sort,** and
if the answer is "unbounded" or "could be anything", the answer is a comparison sort.

### The real error: negative values

```python
print(counting_sort([3, -1, 2], 3))
```

```
Traceback (most recent call last):
  File "day56.py", line 1, in <module>
    print(counting_sort([3, -1, 2], 3))
          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "day56.py", line 11, in counting_sort
    counts[x] += 1
    ~~~~~~^^^
IndexError: list index out of range
```

Actually, in Python this one is worse than an error much of the time: `counts[-1]` is the **last**
counter, so with a small negative value and a large enough range you get no exception at all and a
silently wrong result. The fix is the `- min(nums)` shift in `counting_sort_range`. Say it before
they ask: *"this assumes non-negative keys; for a general range I shift by the minimum."*

### The near-miss: forward placement silently kills stability

```python
def counting_sort_unstable(nums, max_value):
    counts = [0] * (max_value + 1)
    for x in nums:
        counts[x] += 1
    starts = [0] * (max_value + 1)
    for v in range(1, max_value + 1):
        starts[v] = starts[v - 1] + counts[v - 1]
    out = [None] * len(nums)
    for x in nums:                          # <-- FORWARDS, not reversed
        out[starts[x]] = x
        starts[x] += 1
    return out
```

On bare integers this is completely correct, and every test you write on numbers will pass. Run it on
records:

```python
records = [(2, "first"), (1, "x"), (2, "second")]
# a forward-placing version by key gives:
[(1, 'x'), (2, 'first'), (2, 'second')]
```

Which is also fine. The failure only appears when the placement direction and the read direction
disagree, and it appears as **radix sort producing a wrong answer three passes later** with no error
anywhere. This is the hardest bug in this lesson to find, and the defence is to test stability
explicitly, with a list of `(key, tag)` pairs, every time you write a counting sort.

### The trap: radix sort with an unstable inner sort

```python
def radix_broken(nums):
    out = list(nums)
    exponent = 1
    while max(out) // exponent > 0:
        out.sort(key=lambda x: (x // exponent) % 10)   # Timsort IS stable, so this works
        exponent *= 10
    return out
```

That one happens to be fine, because Python's sort is stable. Swap in a quicksort and it breaks:

```python
# with an unstable per-digit sort:
print(radix_with_quicksort([329, 457, 657, 839, 436, 720, 355]))
```

```
[329, 355, 457, 436, 657, 720, 839]
```

Not sorted — `457` before `436` — and no exception. **Radix sort has no correctness of its own; it
borrows all of it from the stability of the per-digit sort.** That is the sentence to say.

### The trap: bucket sort on clustered data

```python
values = [0.5] * 9_999 + [0.99]
bucket_sort(values)
```

No error. It returns the right answer, and it takes about fifty million operations to sort ten
thousand values, because 9,999 of them landed in one bucket and got insertion-sorted. The complexity
you quoted — `O(n)` — was conditional on a property of the data that nobody checked. If you propose
bucket sort, **state the distribution assumption in the same breath**, and say what you would do if
it failed.

### The trap: the off-by-one in the bucket index

```python
index = int((v - low) / (high - low) * n)      # <-- n, should be n - 1
```

```
Traceback (most recent call last):
  File "day56.py", line 12, in bucket_sort
    buckets[index].append(v)
    ~~~~~~~^^^^^^^
IndexError: list index out of range
```

The maximum value maps to exactly `n`, which is one past the last bucket. Use `n - 1`, or clamp with
`min(index, n - 1)`.

### The trap: proposing it for the wrong keys

Counting and radix sorts need a key that **is** a position, or that can be decomposed into digits.
They cannot sort by a custom comparison, cannot sort arbitrary objects, and cannot sort floats
without work. If the interviewer says "sort these employee records by their manager's seniority",
counting sort is not on the table. Ask what the keys are before choosing.

---

## 8. In the interview

### How it gets asked

- *"Sort a million integers in the range 0 to 100. Can you beat n log n?"* — the direct form, and the
  information in the question is the answer.
- *"Sort n numbers in linear time."* — the vague form, where the correct first move is to ask what
  you know about the values.
- *"Can any sort beat O(n log n)?"* — the theory form. Answer: not by comparing, and then name the
  three that do not compare.
- *"Sort a list of names by length, then alphabetically."* — counting sort by length, because lengths
  are bounded and small.
- *"Given ages of a million people, sort them."* — ages are 0 to about 120. This is the question in
  disguise, and spotting it is the point.
- *"Why does radix sort need a stable sort?"* — the follow-up that separates people who have used it
  from people who have read about it.

### What to say out loud, in the first ninety seconds

1. **Ask about the keys before proposing anything.** *"Before I choose — are these integers, and what
   is the range? If they're bounded, I can do better than n log n."*
2. **Name why the limit does not apply.** *"The n log n limit applies to sorts that work by comparing
   pairs. If I know the value is 47, I already know where it goes — I don't need to compare it with
   anything."*
3. **Give the cost with the letters explained.** *"Counting sort is O(n + k), where k is the size of
   the range, not the number of elements. Here n is a million and k is a hundred and one, so it's
   effectively linear."*
4. **Volunteer the failure condition immediately.** *"The reason this isn't the default sort: k is
   the range. If the values went up to a billion I'd need a billion counters — sixteen gigabytes —
   and it would be a MemoryError, not a slow sort."*
5. **Mention stability and why it is not incidental.** *"I place elements walking the input backwards
   so it stays stable, which matters if there's a payload attached, and it's the entire reason radix
   sort works."*

### The follow-ups

**"Why can't a comparison sort beat n log n, and how do these get around it?"**
Because a sort that only ever asks "is a bigger than b" has a fixed amount of information available
per question, and there is a known result that any such sort needs at least on the order of n log n
of those questions in the worst case — that is a property of the whole approach, not a weakness of a
particular algorithm, so no cleverness in pivot choice or merging escapes it. What today's three do
is stop asking that question. Counting sort never compares two elements of the input at all; it uses
the value itself as a position in a table, so knowing a value is 47 immediately tells it where the
element belongs without reference to anything else. That extra power has to be paid for, and it is
paid for with a restriction: you must know that the keys are integers in a known, small range. That
restriction is not a footnote — it is the exchange. So the honest framing is that these are not
faster sorts, they are sorts that solve a smaller problem, and if you cannot state the restriction
your data satisfies, you cannot use them.

**"Why does radix sort need the per-digit sort to be stable?"**
Because radix sort has no correctness of its own — all of it is borrowed. It sorts by the least
significant digit first, then the next, and so on, and the only thing that makes the earlier passes
count for anything is that a later pass leaves the relative order of equal keys alone. Take 457 and
657: after the pass on the last digit they are both in the 7 group, and 457 happens to be ahead
because of what came before. On the pass over the middle digit they both have a 5, so as far as that
pass is concerned they are equal — and a stable sort therefore leaves 457 in front. If the per-digit
sort were unstable, that pass could swap them, and the ordering established by the previous pass
would be destroyed. After all the passes you would have a list sorted correctly by the most
significant digit and scrambled beneath it, which is the worst kind of wrong because it looks almost
right and nothing raises an error. So when I write radix sort, the inner sort is always a counting
sort that places elements by walking the input backwards, which is exactly the step that preserves
order among equal keys. In Python you could also use `list.sort` with a key, because Timsort is
stable — but I would say that explicitly rather than rely on it silently.

**"When would you not use these?"**
Four situations, and I would check them in this order. First, if the range is large or unknown:
counting sort's cost and memory are driven by k, the size of the range, not by n, so a thousand
values spread over a billion needs a billion counters — sixteen gigabytes — and it fails with a
MemoryError rather than merely being slow. Second, if the keys are not integers or cannot be
decomposed into digits: arbitrary objects with a custom comparison, or anything sorted by a rule
rather than by a value, are outside what these can do at all. Third, if memory is tight: all three of
these allocate at least O(n) and counting sort allocates O(n + k), whereas quicksort sorts in place
with O(1) extra — so on a large array in a constrained environment the comparison sort is the right
answer even though it does more operations. And fourth, specifically for bucket sort, if the values
are not uniformly distributed: its O(n) is conditional on the data spreading evenly across buckets,
and ten thousand values that all land in one bucket cost fifty million operations instead of twenty
thousand. There is also a practical fifth in Python: `sorted()` is implemented in C, so a hand-written
counting sort doing ten times fewer operations can still be slower, because each Python operation
costs roughly fifty times a C one. I would give the asymptotic answer, then say that plainly, because
it is the difference between a textbook answer and one I would actually ship.

### A model answer

> "The information in the question is the answer, so I'd start by confirming it: the values are
> integers, and the range is nought to a hundred. That's a hundred and one possible values for a
> million elements, and it means I don't have to compare anything.
>
> The n log n limit applies to sorts that work by comparing pairs of elements. Counting sort doesn't
> compare — it uses the value as a position. So: one pass over the input counting how many of each
> value there are, into a table of a hundred and one counters. Then a pass over the counters turning
> them into running totals, so each entry says how many elements are less than or equal to that
> value — which tells me where each value's block ends in the output. Then a pass over the input,
> going backwards, placing each element and decrementing its counter.
>
> ```python
> def counting_sort(nums: list[int], max_value: int) -> list[int]:
>     counts = [0] * (max_value + 1)
>     for x in nums:
>         counts[x] += 1
>     for v in range(1, max_value + 1):
>         counts[v] += counts[v - 1]
>     out = [0] * len(nums)
>     for x in reversed(nums):          # backwards -- this is what keeps it stable
>         counts[x] -= 1
>         out[counts[x]] = x
>     return out
> ```
>
> The `reversed` is deliberate. It makes the sort stable, which matters the moment there's a payload
> travelling with the key, and it's the entire reason radix sort works.
>
> Cost is O(n + k): two passes over n, one over k. Here that's about two million operations against
> twenty million comparisons for a general sort. Space is O(n + k), so it is not in place — that's the
> trade.
>
> And the condition I'd state without being asked: k is the size of the *range*, not the number of
> elements. If the values went up to a billion, I'd need a billion counters, about sixteen gigabytes,
> and it would fail with a MemoryError rather than being slow. So the rule is that counting sort wins
> when k is comparable with n or smaller. If the range were large but the values were fixed-width
> integers, I'd use radix sort instead — four passes of counting sort a byte at a time, base 256, so
> two hundred and fifty-six counters instead of four billion.
>
> One practical caveat: in Python, `sorted()` is C and my counting sort is bytecode, so ten times
> fewer operations can still lose on the clock. The asymptotic answer is counting sort; if this were
> production Python I'd measure, and I'd probably reach for NumPy."

---

## 9. Recall card

- **These three don't compare — that is how they beat n log n.** No comparison sort can do better
  than O(n log n); counting, radix and bucket sort use the **value as a position** instead. The price
  is a restriction on the keys, and *if you cannot state the restriction, you cannot use the sort*.
- **Counting sort is O(n + k) where k is the RANGE, not the count.** Count → running totals (how many
  are ≤ v) → place walking the input **backwards** (that is what keeps it stable). 10⁶ marks in
  0..100: ~2,000,101 operations against 20,000,000. Three values up to 2×10⁹: **MemoryError**.
- **Radix sort has no correctness of its own — it borrows all of it from stability.** d passes of
  counting sort, least significant digit first; a later pass must not disturb order among equal
  digits, or the earlier passes are destroyed silently. 32-bit ints in base 256 = **4 passes, 256
  counters**.
- **Bucket sort is O(n) only if the values are uniformly spread** — otherwise O(n²). 10,000 values in
  one bucket costs 50,000,000 operations instead of 20,000. State the distribution assumption in the
  same breath as the complexity.
- **None of them sorts in place** (O(n + k), O(n + b), O(n)), none handles negatives without a
  `- min` shift, and none works on arbitrary objects or custom comparisons. And in Python, `sorted()`
  is C: ten times fewer operations in bytecode can still lose on the clock — give the asymptotic
  answer, then say that.
