---
day: 116
track: dsa
title: "Top K problems"
phase: "Heaps and priority queues"
status: written
---

# Day 116 · DSA — Top K problems

**After today you can:** You can choose between a heap, a sort and quickselect and defend the choice with n and k.

**The interviewer asks it as:** *Find the k largest elements. Which approach, and why?*

---

## 1. What this is, and why they ask it

"Top k" is a family: the k largest values, the k most frequent words, the k closest points, the k-th
largest element. They all reduce to the same question — **you need a few extremes out of many items, and
you do not need the rest in any order.**

Three sentences. There are exactly **three** approaches — sort everything, keep a heap of size `k`, or
partition with **quickselect** — and each one wins in a different region of `n` and `k`, so the answer is
never a single technique. The heap version has one counter-intuitive detail that is the whole problem:
**to find the k *largest*, you keep a MIN-heap**, because the thing you constantly need is the *worst* of
your current best, so you can throw it away. And the choice is also constrained by the *shape* of the
input: if the data arrives as a stream and does not fit in memory, sorting and quickselect are both
unavailable and the heap is the only option.

They ask *"which approach, and why?"* because the question is explicitly about the trade-off, not about
the code. A candidate who writes a heap solution and stops has answered half; a candidate who says *"at
k = 10 out of a million, a heap does about three million comparisons against twenty million for a sort —
but at k = 500,000 the sort wins on constants"* has answered it.

---

## 2. The story

The mango crates came off the lorry at four in the morning and by six Chellappa had to have twenty picked
out for the hotel order.

There were about a thousand mangoes in the load, and the hotel wanted the twenty best — big, unmarked, and
at exactly the right ripeness. The rest went to the market at whatever they fetched.

His nephew, in his first week, tried to be systematic about it and started arranging the entire load in
order of quality along the ground. He had about two hundred laid out by half past four and was already in
trouble, because every new mango meant walking along the line to find where it belonged.

Chellappa did it differently and finished in about forty minutes.

He kept a shallow basket at his feet with twenty mangoes in it. That was it. He picked up each mango from
the crate, looked at it for perhaps a second, and did one of two things.

If it was worse than the worst one in his basket, he threw it in the market pile without another thought.
That was most of them — maybe nine hundred out of a thousand.

If it was better, he took the worst one out of the basket, threw *that* in the market pile, and put the new
one in.

The thing his nephew could not work out was how he knew, instantly, which one in the basket was the worst.
He was not searching through twenty mangoes each time.

Chellappa showed him. He kept the basket tilted, and the worst one always sat at the low corner. When he
put a new one in, he gave the basket a small shake and the poor one worked its way down to the corner
again. It took a moment. He never had to look at the other nineteen.

The nephew said: but at the end you still do not know which of the twenty is the best.

Chellappa said the hotel had not asked which was best. They had asked for twenty good ones. Knowing the
order inside the basket would have cost him the whole morning and nobody had asked for it.

Then he said the thing that stuck. He said if they had wanted five hundred out of the thousand, he would
not have done it this way at all — he would have gone through and split the load roughly into good and bad
and taken the good half, because at that point carrying half the crate around in a basket is madness.

---

## 3. The idea in plain English

Chellappa's basket is a size-k heap, the tilt is the heap property, and his last remark is the reason
there are three approaches rather than one.

- The basket of twenty is a **fixed-size heap of size k**.
- "The worst one sits at the low corner" is why it must be a **min-heap** when you want the largest.
- Throwing away anything worse than the worst is the **`O(1)` rejection** that makes it fast.
- The nephew laying out the whole load is **sorting everything** — correct, and far more work than asked
  for.
- "If they wanted five hundred, I would split the load instead" is **quickselect**.

### The counter-intuitive part

> **To find the k LARGEST, keep a MIN-heap of size k.**

**Say it out loud, because it feels backwards.** The reasoning: your basket holds the best `k` so far. The
only question you ever ask is *"is this new item better than the worst thing I am keeping?"* — so the item
you need instant access to is the **minimum** of your basket. A min-heap puts exactly that at the root.

```python
    heap = values[:k]
    heapq.heapify(heap)                     # O(k)
    for v in values[k:]:
        if v > heap[0]:                     # better than my worst? O(1) check
            heapq.heapreplace(heap, v)      # ONE sift-down
    return heap                             # the k largest, in no order
```

**The mirror rule**: to find the k **smallest**, keep a **max-heap** of size k — in Python, a min-heap of
negated values.

**And the `heap[0]` comparison is where the speed comes from.** Most items fail it and are rejected in one
comparison with no heap operation at all — Chellappa's nine hundred mangoes.

### The three approaches

```
 1. SORT EVERYTHING          sorted(data)[-k:]
    O(n log n) time, O(n) space (or O(1) if in place)
    -> simplest; excellent constants; returns them in order for free

 2. HEAP OF SIZE k           the basket
    O(n log k) time, O(k) space
    -> the only option for a STREAM or data too big for memory
    -> wins when k is small relative to n

 3. QUICKSELECT              partition, recurse one side only
    O(n) AVERAGE, O(n^2) worst case, O(1) extra space
    -> fastest when all the data is in memory and you can reorder it
    -> gives you the k-th element and an UNORDERED set of the top k
```

**Say all three and then choose.** That is the question.

### Which one wins, and where

```
 k = 1                    max(data) — O(n), no structure at all
 k very small (< n/100)   heap: O(n log k) with a cheap rejection test
 k moderate               quickselect if in memory: O(n) average
 k close to n             SORT — O(n log n) with far better constants
 streaming / unbounded n  HEAP — the only one that works
 need them in order       sort, or heap then sort the k results
 many queries on the same data   sort ONCE, then every query is O(k)
```

**The crossover between heap and sort is around `k ≈ n/10`**, and the exact point depends on constants
rather than asymptotics — which is worth saying, because it explains why the theoretically better
`O(n log k)` loses to `O(n log n)` in practice at large k.

### Quickselect

The same partition step as [quicksort](../day-054-quicksort/README.md), but **you only recurse into one
side.**

```python
    def select(lo, hi, k_index):
        p = partition(lo, hi)               # everything left of p is smaller
        if p == k_index:
            return data[p]
        if p < k_index:
            return select(p + 1, hi, k_index)   # ONE side only
        return select(lo, p - 1, k_index)
```

**Why it is `O(n)` on average**: the first partition costs `n`, the next costs `n/2`, then `n/4`, and
`n + n/2 + n/4 + … = 2n`. **The geometric series is the whole argument**, and it is the same shape as the
[heapify](../day-114-heapify/README.md) sum.

**Why it is `O(n²)` in the worst case**: if every pivot is the smallest or largest element, each partition
removes one item. **Sorted input with a first-element pivot does exactly that**, and it is not a rare
input.

**The fixes, in order of practicality:**

```
 random pivot          O(n) expected; adversary-proof in practice; ONE line
 median of three       cheap, helps on partly-sorted data, still O(n^2) adversarially
 median of medians     O(n) GUARANTEED worst case, and constants so bad it is
                         slower in practice — know the name, do not write it
 introselect           quickselect that switches to median-of-medians after
                         too many bad partitions — what real libraries do
```

**Always randomise the pivot**, and say why: sorted input is the common case, not an adversarial one.

**And the side effect people forget**: quickselect **reorders the input array**. If the caller needs the
original order, you must copy first, which costs the `O(1)` space advantage.

### The variants, and what changes

**k most frequent** — count first, then top-k on the counts.

```python
    counts = Counter(words)                 # O(n)
    return heapq.nlargest(k, counts, key=counts.get)    # O(m log k), m distinct
```

**Note the two different sizes.** The heap is over the number of **distinct** items, not the number of
items — which matters enormously when a million words have only five thousand distinct values.

**And bucket sort beats everything here when the counts are bounded**: a frequency can be at most `n`, so
you can bucket by count and read down from the top for `O(n)` overall with no heap at all. **That is the
answer to "can you do better than `O(n log k)`?" for this specific problem.**

**k closest points** — the same shape with a computed key.

```python
    heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)
```

**Do not take the square root.** It is a monotonic function, so it does not change the ordering, and it
costs a transcendental operation per point. Saying that is a cheap, real optimisation.

**k-th largest specifically** — quickselect is the natural fit, because you want one element rather than a
set, and quickselect gives it directly.

**Top k in a stream** — the heap, and only the heap. You cannot sort what you cannot hold.

### The output-order question, which is worth asking

```
 sort:          returns them in order
 size-k heap:   returns them UNORDERED — the heap array is not sorted
 quickselect:   returns them UNORDERED
```

**If the answer must be sorted, add `O(k log k)`** to sort the `k` results — which is negligible when `k`
is small and is exactly the cost that makes sorting competitive when `k` is large.

**Ask whether the order matters.** It is a real requirement and it changes the comparison.

---

## 4. The picture

The basket, which is the algorithm.

```
 1,000 mangoes, basket of 20

 for each mango:
     ┌─────────────────────────────────┐
     │ is it better than the WORST     │
     │ one in the basket?              │   ← ONE comparison, O(1)
     └───────┬─────────────────┬───────┘
             │ no (~900)       │ yes (~100)
             ▼                 ▼
      market pile        swap out the worst,
      (rejected in       shake the basket
       one comparison)   (heapreplace, O(log k))

 THE BASKET IS A MIN-HEAP:
   you want the k LARGEST, so the thing you constantly need is
   the SMALLEST of what you are keeping — a min-heap puts it at heap[0].

 at the end: the basket holds the top 20, IN NO ORDER.
 The hotel did not ask for an order.
```

The three approaches, side by side:

```
 SORT EVERYTHING            HEAP OF SIZE k              QUICKSELECT
 ─────────────────          ──────────────────          ─────────────────────

 [ ][ ][ ][ ][ ][ ]         basket ┌────┐               [   ?   |p|   ?   ]
        ↓ sort              stream │k=3 │                       ↓ partition
 [ ][ ][ ][ ][ ][ ]  →→→→→→→→→→→→→ └────┘               [ < p  |p|  > p  ]
        take the last k                                          ↓
                                                        RECURSE ONE SIDE ONLY
 O(n log n), O(n)          O(n log k), O(k)             O(n) avg, O(1) space
 in order, free            NOT in order                 NOT in order
 works on any input        THE ONLY streaming option    reorders the input
```

Where each one wins:

```
 n = 1,000,000

 k          sort              size-k heap        quickselect
 --------   ---------------   ---------------    ---------------
 1          20,000,000 cmp    n/a — use max()    n/a — use max()
 10         20,000,000        ~3,300,000  ← ✓    ~2,000,000  ← ✓
 1,000      20,000,000        ~10,000,000        ~2,000,000  ← ✓
 100,000    20,000,000  ← ✓   ~17,000,000        ~2,000,000  ← ✓
 500,000    20,000,000  ← ✓   ~19,000,000        ~2,000,000  ← ✓
                              (worse constants)  (but reorders, and O(n^2) worst)

 the crossover between HEAP and SORT is around k ≈ n/10,
 and it is decided by CONSTANTS, not by the asymptotics.
```

Why quickselect is `O(n)`:

```
 partition the whole array          n comparisons
 recurse into ONE half             n/2
                                   n/4
                                   n/8
                                   ...
                                   ────
                                    2n        ->  O(n)

 compare with QUICKSORT, which recurses into BOTH halves:
                                   n
                                   n/2 + n/2  = n
                                   n/4 × 4    = n
                                   ...  log n levels  ->  O(n log n)

 ONE side instead of two turns log n levels of full work into
 a geometric series that sums to 2.
```

The worst case, and why it is not exotic:

```
 sorted input [1,2,3,...,n], pivot = first element

 partition -> pivot is the smallest, so ONE element is removed
   n + (n-1) + (n-2) + ... = n^2/2   ->  O(n^2)

 THE FIX: choose the pivot at RANDOM. One line.
   -> O(n) EXPECTED, and an adversary cannot construct the bad case

 median-of-medians gives O(n) GUARANTEED and is slower in practice —
 know the name, do not write it.
```

---

## 5. The code, built step by step

### Step 1 — ask the three questions that decide the approach

"How big is `k` relative to `n`? Does the data fit in memory, or is it a stream? And do you need the
results in order?" **Those three answers choose the algorithm**, and asking them is the answer to the
question.

### Step 2 — say the counter-intuitive rule as you write it

```python
    heap = values[:k]
    heapq.heapify(heap)
```

**"For the k largest I keep a min-heap, because the thing I constantly need is the worst of what I am
keeping, so I can throw it away."** That sentence is what the problem is testing.

### Step 3 — the `O(1)` rejection, which is where the speed is

```python
        if v > heap[0]:
```

"Most items fail this in one comparison and never touch the heap. On random data only about `k log(n/k)`
items ever get inserted, which is why the practical cost is far below the `O(n log k)` bound."

### Step 4 — `heapreplace`, not pop-then-push

```python
            heapq.heapreplace(heap, v)
```

"One sift-down instead of a sift-down and a sift-up. In a hot loop over a million items that is a real
constant-factor win."

### Step 5 — offer quickselect with its caveats

"If everything is in memory and I am allowed to reorder it, quickselect is `O(n)` average — better than
both. Two caveats: it is `O(n²)` if I pick pivots badly, so I randomise; and it **mutates the input**, so
if the caller needs the original order I have to copy first."

### The complete solution

```python
import heapq
import random
from collections import Counter


# ---------------------------------------------------------------------------
# 1. The size-k heap — the basket
# ---------------------------------------------------------------------------

def k_largest_heap(values: list[int], k: int) -> list[int]:
    """The k largest, via a MIN-heap of size k.

    THE COUNTER-INTUITIVE PART: for the k LARGEST you keep a MIN-heap,
    because the thing you constantly need is the WORST of what you are
    currently keeping — so you can throw it out. A min-heap puts exactly
    that at heap[0].

    The `v > heap[0]` test is where the speed lives: most items fail it in
    ONE comparison and never touch the heap at all.

    O(n log k) time, O(k) space. Returns them UNORDERED.
    THE ONLY option for a stream or for data larger than memory.
    """
    if k <= 0:
        return []
    if k >= len(values):
        return list(values)

    heap = values[:k]
    heapq.heapify(heap)                     # O(k)
    for v in values[k:]:
        if v > heap[0]:                     # O(1) rejection — most fail here
            heapq.heapreplace(heap, v)      # ONE sift-down, not pop+push
    return heap                             # unordered


def k_smallest_heap(values: list[int], k: int) -> list[int]:
    """The mirror: for the k SMALLEST, a MAX-heap of size k.
    In Python that is a min-heap of negated values."""
    if k <= 0:
        return []
    heap = [-v for v in values[:k]]
    heapq.heapify(heap)
    for v in values[k:]:
        if -v > heap[0]:                    # v < the largest we are keeping
            heapq.heapreplace(heap, -v)
    return [-v for v in heap]


# ---------------------------------------------------------------------------
# 2. Sorting — simplest, and the right answer more often than people think
# ---------------------------------------------------------------------------

def k_largest_sort(values: list[int], k: int) -> list[int]:
    """O(n log n), excellent constants, and they come back IN ORDER.

    Beats the heap once k is a large fraction of n, and beats everything if
    you will run many queries against the same data — sort once, then each
    query is O(k).
    """
    return sorted(values, reverse=True)[:k]


# ---------------------------------------------------------------------------
# 3. Quickselect — O(n) average, when the data is in memory
# ---------------------------------------------------------------------------

def quickselect(values: list[int], k: int) -> int:
    """The k-th LARGEST element (1-indexed), in O(n) average time.

    Quicksort's partition, but recursing into ONE side only:
      n + n/2 + n/4 + ... = 2n   ->  O(n)

    O(n^2) worst case if the pivots are always extreme — and SORTED INPUT
    with a fixed pivot does exactly that, which is not a rare input. So the
    pivot is RANDOM: one line, and it makes the bad case unconstructible.

    NOTE: this MUTATES `values`. Copy first if the caller needs the original
    order — which costs the O(1)-space advantage.
    """
    if not 1 <= k <= len(values):
        raise ValueError("k out of range")

    target = len(values) - k                # the k-th largest is at this index
    lo, hi = 0, len(values) - 1

    while lo < hi:
        p = _partition(values, lo, hi)
        if p == target:
            return values[p]
        if p < target:
            lo = p + 1                      # ONE side
        else:
            hi = p - 1
    return values[lo]


def _partition(values: list[int], lo: int, hi: int) -> int:
    """Lomuto partition with a RANDOM pivot."""
    pivot_index = random.randint(lo, hi)    # THE line that avoids O(n^2)
    values[pivot_index], values[hi] = values[hi], values[pivot_index]
    pivot = values[hi]

    boundary = lo
    for i in range(lo, hi):
        if values[i] < pivot:
            values[boundary], values[i] = values[i], values[boundary]
            boundary += 1
    values[boundary], values[hi] = values[hi], values[boundary]
    return boundary


def k_largest_quickselect(values: list[int], k: int) -> list[int]:
    """The SET of the k largest, unordered, in O(n) average.
    Partition until the boundary is exactly at n-k, then take the tail."""
    if k <= 0:
        return []
    if k >= len(values):
        return list(values)
    data = list(values)                     # copy: quickselect mutates
    quickselect(data, k)
    return data[len(data) - k:]


# ---------------------------------------------------------------------------
# 4. The variants
# ---------------------------------------------------------------------------

def top_k_frequent(items: list[str], k: int) -> list[str]:
    """LeetCode 347. Count first, then top-k over the DISTINCT items.

    Note the two different sizes: the heap is over m distinct items, not n
    total. A million words with 5,000 distinct values makes the heap step
    almost free.

    O(n) to count + O(m log k) for the heap.
    """
    counts = Counter(items)
    return heapq.nlargest(k, counts, key=counts.get)


def top_k_frequent_buckets(items: list[str], k: int) -> list[str]:
    """The O(n) answer for this SPECIFIC problem: a frequency can be at most
    n, so bucket by count and read down from the top. No heap at all.

    This is the answer to "can you do better than O(n log k)?" here — and it
    only works because the KEY IS BOUNDED, which is the general lesson.
    """
    counts = Counter(items)
    buckets: list[list[str]] = [[] for _ in range(len(items) + 1)]
    for item, count in counts.items():
        buckets[count].append(item)

    out: list[str] = []
    for count in range(len(buckets) - 1, 0, -1):
        for item in buckets[count]:
            out.append(item)
            if len(out) == k:
                return out
    return out


def k_closest_points(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    """LeetCode 973. The same shape with a computed key.

    DO NOT take the square root: it is monotonic, so it does not change the
    ordering, and it costs a transcendental operation per point.
    """
    return heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)


class KthLargestStream:
    """LeetCode 703. A stream — the ONLY case where the heap is forced.

    You cannot sort what you cannot hold, and quickselect needs random
    access to the whole array.
    """

    def __init__(self, k: int, initial: list[int]) -> None:
        self.k = k
        self.heap = list(initial)
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)        # keep only the k largest

    def add(self, value: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, value)
        elif value > self.heap[0]:
            heapq.heapreplace(self.heap, value)
        return self.heap[0]                 # the k-th largest, O(1)


def k_largest_across_sorted_lists(lists: list[list[int]], k: int) -> list[int]:
    """When the inputs are already sorted, neither a full sort nor
    quickselect is needed — merge lazily and take k. Day 117."""
    return list(heapq.merge(*lists, reverse=True))[:k]


# ---------------------------------------------------------------------------
# 5. Measuring the choice
# ---------------------------------------------------------------------------

def compare_approaches(n: int, k: int) -> None:
    """Run this rather than trusting the table."""
    import time
    data = [random.randint(0, 10 ** 9) for _ in range(n)]

    t = time.perf_counter(); a = k_largest_sort(data, k)
    sort_time = time.perf_counter() - t

    t = time.perf_counter(); b = k_largest_heap(data, k)
    heap_time = time.perf_counter() - t

    t = time.perf_counter(); c = k_largest_quickselect(data, k)
    qs_time = time.perf_counter() - t

    assert sorted(a) == sorted(b) == sorted(c)
    print(f"n={n:>9} k={k:>7}   sort {sort_time:.4f}s   "
          f"heap {heap_time:.4f}s   quickselect {qs_time:.4f}s")


if __name__ == "__main__":
    random.seed(0)
    values = [5, 1, 9, 3, 7, 2, 8, 6, 4]

    print(sorted(k_largest_heap(values, 3), reverse=True))          # [9, 8, 7]
    print(sorted(k_smallest_heap(values, 3)))                       # [1, 2, 3]
    print(k_largest_sort(values, 3))                                # [9, 8, 7]
    print(quickselect(values[:], 3))                                # 7
    print(sorted(k_largest_quickselect(values, 3), reverse=True))   # [9, 8, 7]

    # the heap result is NOT sorted — the hotel did not ask for an order
    print(k_largest_heap(values, 4))                                # e.g. [6, 7, 9, 8]

    # variants
    words = "the quick brown fox the lazy dog the fox".split()
    print(top_k_frequent(words, 2))                                 # ['the', 'fox']
    print(top_k_frequent_buckets(words, 2))                         # ['the', 'fox']
    print(k_closest_points([(1, 3), (-2, 2), (5, 8), (0, 1)], 2))   # [(0,1), (-2,2)]

    stream = KthLargestStream(3, [4, 5, 8, 2])
    print([stream.add(v) for v in (3, 5, 10, 9, 4)])                # [4, 5, 5, 8, 8]

    # edge cases
    print(k_largest_heap([], 3), k_largest_heap([1, 2], 5))         # [] [1, 2]
    print(k_largest_heap([1, 1, 1], 2))                             # [1, 1]

    # WHERE EACH ONE WINS — run it, do not trust the table
    compare_approaches(1_000_000, 10)
    compare_approaches(1_000_000, 100_000)
    compare_approaches(1_000_000, 500_000)
```

---

## 6. What it costs

### The three approaches

```
 approach        time                 space      in order?   streaming?
 -------------   ------------------   --------   ---------   ----------
 sort            O(n log n)           O(n)       YES         no
 size-k heap     O(n log k)           O(k)       no          YES
 quickselect     O(n) average         O(1)       no          no
                 O(n^2) worst                                (and it MUTATES)
```

### Comparison counts at n = 1,000,000

```
 k          sort          heap            quickselect
 --------   -----------   -------------   -----------
 10         20,000,000    ~3,300,000      ~2,000,000
 1,000      20,000,000    ~10,000,000     ~2,000,000
 100,000    20,000,000    ~17,000,000     ~2,000,000
 500,000    20,000,000    ~19,000,000     ~2,000,000
```

**Asymptotically quickselect always wins. In practice it often does not**, because `sorted()` in CPython
is a highly tuned C implementation and quickselect written in Python is interpreted. **That is worth
saying**: the constants dominate at these sizes, which is why the measured comparison in the code matters
more than the table.

### The rejection rate, which is the heap's real advantage

```
 the number of items that ever ENTER a size-k heap, on random data:
   expected insertions ≈ k · ln(n/k)

 n = 1,000,000, k = 10   ->  ~115 insertions out of 1,000,000 items
                             999,885 rejected in ONE comparison each
```

**So the practical cost is `n` cheap comparisons plus about a hundred heap operations** — far below the
`O(n log k)` bound, which assumes every item is inserted. **That is why the heap is so much better than
its bound suggests on random data**, and it is a genuinely good thing to know.

**And the worst case**: ascending input, where every item beats the current worst.

```
 sorted ascending, n = 1,000,000, k = 10:  1,000,000 insertions
 -> the full O(n log k), and no rejections at all
```

### Space, which often decides it

```
 n = 1,000,000,000 items (does not fit in memory)

 sort           impossible without external sort
 quickselect    impossible — needs random access to everything
 size-k heap    O(k) = a few hundred bytes.  THE ONLY OPTION.
```

**That is the case where the choice is not a trade-off at all.**

### The frequency variant

```
 n = 1,000,000 words, m = 5,000 distinct

 counting              O(n)          = 1,000,000
 heap over DISTINCT    O(m log k)    = 5,000 × log(10) ≈ 17,000
 -> the heap step is 0.2% of the work; the COUNT dominates

 bucket sort           O(n)          — no heap at all, and it is exact
```

**Noticing that `m` and `n` are different is worth stating**, and the bucket-sort answer for bounded keys
is the strongest finish available on that problem.

### Quickselect's recursion

```
 expected depth      O(log n)
 worst-case depth    O(n)  ->  RecursionError if written recursively

 -> write it ITERATIVELY, as the code above does, with a while loop
    adjusting lo and hi. One less thing to worry about.
```

---

## 7. The traps

### Trap 1 — using a max-heap for the k largest

```python
    heap = [-v for v in values]             # a max-heap of EVERYTHING
    heapq.heapify(heap)
    return [-heapq.heappop(heap) for _ in range(k)]
```

Correct, and it is `O(n + k log n)` with **`O(n)` space** — it holds the entire input. The whole point of
the size-k heap is that it holds `k` items, and to do that it must be a **min**-heap so the worst is at the
root.

**On a stream this version is not merely slower, it is impossible.**

### Trap 2 — pop-then-push instead of `heapreplace`

```python
            heapq.heappop(heap)
            heapq.heappush(heap, v)
```

Two passes over the heap instead of one sift-down. Correct, and a measurable constant-factor loss in a
loop over a million items.

### Trap 3 — forgetting that the results are unordered

```python
    return k_largest_heap(values, 3)        # e.g. [6, 7, 9, 8]
```

The heap's array is not sorted, and neither is quickselect's tail. **If the answer must be in order, add
`O(k log k)`** — and say so, because a test comparing against a sorted expectation will fail.

### Trap 4 — a fixed pivot in quickselect

```python
    pivot = values[hi]                      # always the last element
```

On sorted or reverse-sorted input, every partition removes one element: `O(n²)`. **Sorted input is the
common case, not adversarial.** One line — `random.randint(lo, hi)` — fixes it.

### Trap 5 — forgetting that quickselect mutates

```python
    kth = quickselect(user_data, 5)         # user_data is now reordered
```

The caller's array is scrambled. If the original order matters, copy first — which costs the `O(1)` space
advantage that made quickselect attractive.

### Trap 6 — `k > len(values)` and other boundaries

```python
    heap = values[:k]                       # fine
    for v in values[k:]:                    # empty, fine
    return heap                             # returns everything — correct
```

Handled by luck here, but `quickselect` with `k > n` must raise, and `k <= 0` must return empty.
**Check the boundaries explicitly**; every one of these problems has a `k = 0`, `k = n` and empty-input
test case.

### Trap 7 — the square root in k-closest-points

```python
    key=lambda p: math.sqrt(p[0]**2 + p[1]**2)
```

Correct, and it computes a square root a million times for no reason: the ordering is identical without
it because `sqrt` is monotonic on non-negative values. **A free optimisation, and interviewers notice.**

### Trap 8 — heap size over the wrong `n` in the frequency problem

```python
    heapq.nlargest(k, items)                # over ALL items, not the counts
```

You want the top `k` **distinct** items by frequency, so the heap is over the `m` distinct keys. Running
it over all `n` items is both wrong and much slower.

---

## 8. In the interview

### How it gets asked

- The open one: *"Find the k largest elements. Which approach, and why?"*
- The specific: *"Find the k-th largest element."* LeetCode 215.
- The variant: *"Top k frequent elements."* LeetCode 347 — and then *"can you do better than `O(n log k)`?"*
- The constraint: *"The data is a stream and does not fit in memory."*
- The efficiency probe: *"Can you do it in `O(n)`?"*

### What to say out loud, in the first ninety seconds

1. **Ask the three questions that decide it.** "How big is `k` relative to `n`? Does everything fit in
   memory, or is it a stream? And do you need the results in order?"
2. **Name all three approaches before choosing.** "Sort everything — `O(n log n)`, simplest, and they come
   back ordered. A heap of size `k` — `O(n log k)`, `O(k)` space, and the only option for a stream.
   Quickselect — `O(n)` average, but it mutates the input."
3. **Give the counter-intuitive rule explicitly.** "For the k **largest** I keep a **min**-heap of size k,
   because the thing I constantly need is the **worst** of what I am keeping, so I can throw it away —
   and a min-heap puts exactly that at the root."
4. **Point at where the speed is.** "The comparison against `heap[0]` rejects most items in one comparison
   without touching the heap. On random data only about `k log(n/k)` items ever get inserted — for a
   million items and k = 10, about a hundred insertions out of a million."
5. **Give a concrete comparison.** "At n a million and k ten, the heap does roughly three million
   comparisons against twenty million for a sort. At k = 500,000, the sort wins on constants."
6. **Say the space consequence.** "And if the data does not fit in memory, it is not a trade-off — sorting
   and quickselect are both unavailable and the heap is the only option."

### The follow-ups

**"Why a min-heap for the largest? That feels backwards."**
"It does, and the reason it is right is that the heap is not holding the answer to the question you are
asking — it is holding the **candidates**, and the only question you ever ask of it is *'is this new item
better than the worst thing I am currently keeping?'* So the element I need instant access to is the
**minimum** of my current best `k`, and a min-heap puts exactly that at index zero. When a new item beats
it, I evict the minimum and insert the new one. At the end, the heap contains the `k` largest — unordered,
because nobody asked for an order. The mirror rule is the same logic: for the k **smallest**, keep a
**max**-heap, which in Python means negating."

**"Can you do it in `O(n)`?"**
"Yes, with **quickselect**, if the data is in memory and I am allowed to reorder it. It is quicksort's
partition step, but I only recurse into the side containing the k-th position — so the cost is
`n + n/2 + n/4 + …`, a geometric series summing to `2n`. Two caveats I would state rather than let you
find. It is `O(n²)` in the worst case, when every pivot is extreme — and **sorted input with a fixed pivot
does exactly that**, which is a common input, not an adversarial one, so the pivot must be **random**.
And it **mutates the array**, so if the caller needs the original order I have to copy first, which costs
the `O(1)`-space advantage. If I needed a guaranteed `O(n)` I would name **median-of-medians**, and then
say that its constants are bad enough that it is slower in practice — which is why real libraries use
**introselect**: quickselect that falls back to it after too many bad partitions."

**"Top k frequent — can you do better than `O(n log k)`?"**
"Yes, for this specific problem, because the key is **bounded**. A frequency can be at most `n`, so
instead of a heap I can bucket by count: an array of `n + 1` lists, put each distinct item in the bucket
for its count, then read down from the highest bucket until I have `k`. That is `O(n)` overall with no
heap at all, and it is exact rather than approximate. The general lesson is the one worth stating:
**when the sort key is bounded and small, bucketing beats comparison-based approaches**, which is the same
reason counting sort exists. I would also point out something about the heap version that people miss —
the heap is over the number of **distinct** items, not the total. A million words with five thousand
distinct values makes the heap step about 0.2% of the work; the counting dominates."

**"The data is a stream and does not fit in memory."**
"Then it stops being a trade-off. Sorting needs to hold everything, and quickselect needs random access to
the whole array, so **both are unavailable** — the size-`k` heap is the only option. I keep `k` items and
`O(1)` state, process each element once, and the answer is available at any moment. That is also why the
'k-th largest in a stream' problem exists as a separate question: it is the one shape where the choice is
forced. If `k` itself were too large to hold, I would be into approximate territory — count-min sketch for
frequencies, or reservoir sampling — and I would say so rather than pretend the exact answer is
available."

**"Which would you actually write?"**
"For an interview, the **size-k heap**, and I would say why: it is six lines, it handles the streaming case
for free, its space is `O(k)` rather than `O(n)`, and its practical cost is far below its bound because
most items are rejected in one comparison. For production with everything in memory and `k` a large
fraction of `n`, I would just **sort** — `O(n log n)` with excellent library constants beats a hand-written
`O(n log k)` in Python, and it returns the results ordered. And if I were running many top-k queries
against the same unchanging data, I would sort **once** and then every query is `O(k)`. Quickselect I would
offer as the `O(n)` answer and mention that in practice, in Python, `sorted()` in C often beats it — the
asymptotics say one thing and the constants say another, and it is worth measuring rather than assuming."

**"What are the boundary cases?"**
"Four, and each problem in the family has all of them. **k = 0** — return empty rather than raising.
**k ≥ n** — return everything, and note that the heap version handles it naturally while quickselect must
check. **An empty input.** And **duplicates** — 'the three largest' of `[5, 5, 5]` is `[5, 5, 5]`, not one
element, which matters because a solution built on a set would get it wrong. I would also ask whether the
result needs to be **in order**, because the heap and quickselect both return it unordered, and adding
`O(k log k)` to sort the answer is the difference between passing and failing a test that compares against
a sorted expectation."

### A model answer

Asked: *find the k largest elements — which approach, and why?*

> "Three questions first, because they decide the answer: **how big is `k` relative to `n`**, **does
> everything fit in memory or is this a stream**, and **do the results need to be in order?**
>
> There are three approaches and each wins somewhere.
>
> **Sort everything** and take the last `k`. `O(n log n)`, the simplest possible code, excellent library
> constants, and the results come back ordered for free.
>
> **A heap of size `k`.** `O(n log k)` time and — the important part — **`O(k)` space**. This is the one I
> would write by default, and it has a detail that sounds backwards: **for the k largest, you keep a
> MIN-heap.** The heap holds my current best `k`, and the only question I ever ask is 'is this new item
> better than the *worst* one I am keeping?' — so the element I need instantly is the minimum of my
> candidates, and a min-heap puts that at index zero. If the new item beats it, I evict and insert;
> otherwise I discard it after one comparison.
>
> That rejection is where the real speed is. On random data only about `k · ln(n/k)` items ever enter the
> heap — for a million items with `k` of ten, that is roughly a **hundred** insertions out of a million,
> and the other 999,900 cost a single comparison each. So the practical cost is far below the `O(n log k)`
> bound, which assumes every item is inserted.
>
> **Quickselect** is the third. Quicksort's partition, recursing into only the side that contains the k-th
> position, so the cost is `n + n/2 + n/4 + …`, which sums to `2n` — `O(n)` average. Two caveats I would
> raise myself: it is `O(n²)` when pivots are extreme, and **sorted input with a fixed pivot does exactly
> that**, so the pivot must be random; and it **reorders the caller's array**, so preserving the original
> costs a copy and with it the `O(1)`-space advantage.
>
> Choosing between them: at a million items and `k` of ten, the heap is about three million comparisons
> against twenty million for a sort — a clear win. At `k` of five hundred thousand, the sort wins on
> constants, and the crossover is around `k ≈ n/10`. Quickselect is asymptotically best and in Python is
> often beaten by `sorted()` in C, so I would measure rather than assume.
>
> And there is one case where it is not a trade-off at all: if the data is a **stream** or larger than
> memory, sorting and quickselect are both impossible, and the size-`k` heap is the only option.
>
> One thing I would confirm before writing: the heap and quickselect both return the results **unordered**.
> If you need them sorted, that is an extra `O(k log k)`."

---

## 9. Recall card

- **Three approaches, and the answer is which one and why: sort (`O(n log n)`, ordered, simplest) · a
  size-k heap (`O(n log k)`, **`O(k)` space**, the ONLY streaming option) · quickselect (`O(n)` average,
  `O(1)` space, but it **mutates** the input).** Ask: **how big is k relative to n · in memory or a stream
  · do you need them in order?**
- **For the k LARGEST, keep a MIN-heap of size k** — the heap holds candidates, and the only question you
  ask is *"better than the worst I am keeping?"*, so you need the **minimum** at the root. Mirror rule: k
  smallest → a max-heap. Use **`heapreplace`**, not pop-then-push.
- **The `v > heap[0]` test is where the speed is.** On random data only ~**`k·ln(n/k)`** items ever enter
  the heap — **~100 insertions out of 1,000,000** at k = 10 — so the practical cost is far below the bound.
  Worst case is **ascending input**, where every item is inserted.
- **Quickselect is `O(n)` because it recurses into ONE side: `n + n/2 + n/4 + … = 2n`.** It is `O(n²)` when
  pivots are extreme, and **sorted input with a fixed pivot does exactly that — so randomise the pivot,
  always.** Name **median-of-medians** (guaranteed `O(n)`, bad constants) and **introselect** (what real
  libraries do).
- **Crossover is around `k ≈ n/10`, decided by constants.** `k = 1` → `max()`. **Both the heap and
  quickselect return results UNORDERED** — add `O(k log k)` if order matters. For **top-k frequent**, the
  heap is over the **distinct** items, and **bucket sort by count is `O(n)`** because the key is bounded —
  that is the "can you do better?" answer.
