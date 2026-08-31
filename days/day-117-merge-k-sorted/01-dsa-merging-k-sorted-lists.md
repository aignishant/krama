---
day: 117
track: dsa
title: "Merging K sorted lists"
phase: "Heaps and priority queues"
status: written
---

# Day 117 · DSA — Merging K sorted lists

**After today you can:** You can merge k lists in O(n log k) and explain why the heap holds only k items.

**The interviewer asks it as:** *Merge k sorted lists efficiently.*

---

## 1. What this is, and why they ask it

You have `k` lists, each already sorted, holding `n` items between them. Produce one sorted list.

Three sentences. The whole problem reduces to a single repeated question — **which of the `k` current
front items is smallest?** — and that is precisely what a heap answers in `O(log k)`. The detail that
carries the complexity, and the one the interviewer is checking, is that **the heap holds only `k` items,
never `n`**: one candidate per list, replaced as each is consumed. And there is a second `O(n log k)`
solution — merging the lists pairwise in a tournament — which is worth knowing because it uses no heap at
all and beats the heap when comparisons are expensive.

They ask it because it is where the heap stops being a data structure and becomes a technique. It is also
the shape of **external sorting** — how you sort a file larger than memory — so it is one of the few
interview problems whose answer is literally how real systems work.

---

## 2. The story

The sorting office at the district headquarters took the bundles off the night bus at about half past
four, and Basheer had been the man who combined them since 1988.

Six bundles arrived, one from each of the six taluk offices. Each bundle was already in order by pincode —
the taluk clerks did that overnight — and Basheer's job was to turn the six into one sequence for the
delivery vans.

The new man who came in 2004 did it by putting all six bundles on the table together, going through the
entire pile, finding the lowest pincode, taking it, and starting again. It worked. It took him until nine
o'clock.

Basheer's method took about seventy minutes, and it looked lazy.

He did not look at the bundles at all. He looked at **six letters** — the top one of each bundle — and
nothing else. Six letters, laid out in front of him in a small arc.

He picked the lowest of those six, put it in the outgoing tray, and then **pulled the next letter off
whichever bundle he had just taken from** and put it in the gap.

Six letters in front of him, always. Never seven, never five. Whatever was on the table was one candidate
from each bundle, and the answer was always among them, because everything behind a letter in its own
bundle had a higher pincode than it.

The new man watched for a while and asked how Basheer knew he was not missing something further down one
of the bundles.

Basheer said: the bundles are already in order. If the top letter of the Erode bundle is 638001, then
nothing else in that bundle is lower. So the lowest letter in the whole load has to be the lowest of the
six on the table. There is nowhere else it could be hiding.

And he made one more point, which was the reason he could do it at four in the morning without thinking.
He said he never had to compare six letters properly either. He kept them arranged so that the lowest was
always at his left hand. When he took it and slid a new one in, he only had to nudge the new one along
until it sat in the right place — usually one or two positions — and the lowest was at his left hand
again.

He said the whole job was six letters and a small nudge, repeated four thousand times.

---

## 3. The idea in plain English

Basheer's six letters are a heap of size `k`, and his argument about the Erode bundle is the proof that
the method is correct.

- The six bundles are the `k` sorted lists.
- The six letters on the table are the **heap**: one candidate per list.
- "Nothing else in that bundle is lower" is the **invariant** that makes it correct.
- "Pull the next one off the bundle I just took from" is what keeps the heap at exactly `k`.
- "Nudge it into place" is `heappush` — `O(log k)`, not a scan of six.

### The invariant, which is the whole correctness argument

> **At every moment, the smallest remaining item across all lists is one of the `k` current front items.**

**Why**: each list is sorted, so within a list nothing behind the front is smaller than the front. The
overall smallest must therefore be at the front of *some* list — and the heap holds all `k` fronts.

**That is the entire proof**, and being able to give it in one sentence is what separates a memorised
solution from an understood one.

### The algorithm

```python
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)                     # O(k)

    out = []
    while heap:
        value, list_index, item_index = heapq.heappop(heap)      # O(log k)
        out.append(value)
        nxt = item_index + 1
        if nxt < len(lists[list_index]):
            heapq.heappush(heap, (lists[list_index][nxt], list_index, nxt))
    return out
```

**Three things to point at while writing it.**

**The heap holds `k` items, never `n`.** One per list. Every pop is immediately followed by at most one
push from the same list, so the size never grows. That is why the complexity is `O(n log k)` and not
`O(n log n)` — and it is the thing the question is testing.

**The tuple carries where it came from.** You pop a value and must know which list to advance, so the
entry is `(value, list_index, item_index)` rather than just the value.

**The list index doubles as the tie-breaker.** Two equal values would make Python compare the next tuple
element, and the list index is always distinct — so the payload is never compared. That is
[day 115's](../day-115-heapq/README.md) rule, satisfied for free here.

### Why `O(n log k)` and not `O(n log n)`

```
 n items are popped, once each          n pops
 each pop costs                         O(log k)   — the heap holds k, not n
 ------------------------------------------------
 total                                  O(n log k)
```

**The difference is real and worth quantifying**:

```
 n = 1,000,000 items, k = 100 lists

 O(n log n)  ->  1,000,000 × 20  =  20,000,000 comparisons
 O(n log k)  ->  1,000,000 × 7   =   7,000,000
                                     -> ~3x fewer
 O(n·k)      ->  1,000,000 × 100 = 100,000,000    ← the naive scan
```

**And the space difference is the bigger one:** `O(k)` instead of `O(n)`, which is what makes the
technique work on data that does not fit in memory.

### The naive approaches, and why they lose

**Scan all `k` fronts each time.** The new man's method, sort of.

```
 O(n · k) time, O(k) space
```

Correct, and it re-compares the same `k − 1` items on every step. At `k = 100` it is fourteen times slower
than the heap. **The heap's only job is to avoid re-finding the minimum you already knew.**

**Concatenate everything and sort.**

```
 O(n log n) time, O(n) space
```

Correct, simple, and it **throws away the fact that the inputs are sorted** — which is the only
interesting property of the problem. It is also `O(n)` space, so it cannot stream.

**Merge them one at a time, sequentially.**

```
 merge list 1 with list 2, then with list 3, then with list 4 ...
 -> the accumulating result is re-walked every time
 -> 2n + 3n + ... = O(n·k)
```

**This is the trap** — it looks like a divide-and-conquer solution and it is not. The accumulated list
gets longer each time, so early elements are copied `k` times.

### The other `O(n log k)`: pairwise tournament merging

**Merge them in pairs, then merge the results in pairs, and so on** — a knockout tournament.

```
 round 1:  k lists  ->  k/2 lists     each element touched once:  n
 round 2:  k/2      ->  k/4                                        n
 ...
 log k rounds, n work per round  ->  O(n log k)
```

**The same complexity as the heap, with no heap.** Its advantages:

- **No priority queue at all** — just the two-list merge you already know.
- **Better cache behaviour**, because each merge is two linear scans.
- **Trivially parallel**: the merges in a round are independent.

Its disadvantages:

- **`O(n)` space** for the intermediate results (unless the lists are linked lists, where merging is in
  place — which is why LeetCode 23 uses linked lists).
- **Not streaming**: it needs all the data up front.

**Say both.** *"Two solutions at `O(n log k)`: a heap of the `k` fronts, or a pairwise tournament. The heap
is `O(k)` space and streams; the tournament has better constants and parallelises."*

### External sorting: the reason this matters

**How do you sort a hundred gigabytes with eight gigabytes of memory?**

```
 1. read a chunk that fits in memory, sort it, write it to disk    (a "run")
 2. repeat until the input is consumed        ->  ~13 sorted runs
 3. MERGE the runs with a k-way merge         ->  exactly today's problem
```

**Step 3 is this algorithm**, and the `O(k)` memory is what makes it possible: you hold one block from
each run, not the whole file. **That is why merge is the sorting algorithm of the disk world** and
quicksort is the one of memory — quicksort needs random access, and merging is sequential in every
direction.

**It is also how a database merges sorted index scans**, and how log-structured storage engines compact
their SSTables. Naming one of those is a strong finish.

### Variants, which are the same shape

**Merge k sorted linked lists** — LeetCode 23. The heap holds nodes; the tuple is
`(node.val, index, node)`; and you advance with `node.next`. **The tournament version merges in place with
no extra space**, which is why the linked-list framing exists.

**Smallest range covering elements from all k lists** — LeetCode 632. Keep the same heap of `k` fronts, and
also track the **maximum** of the current fronts. The range is `[heap_min, current_max]`, and you advance
the minimum each time. **Same heap, one extra variable.**

**Kth smallest in a sorted matrix** — LeetCode 378. Each row is a sorted list, so it is a k-way merge where
you stop after `k` pops: `O(k log rows)`.

**Merging sorted streams** — `heapq.merge(*iterables)` does exactly this and is **lazy**, so it works on
inputs larger than memory.

**Ugly numbers, super ugly numbers** — the same heap-of-frontiers idea where the "lists" are generated
lazily rather than given.

---

## 4. The picture

The six letters, which is the algorithm.

```
 six bundles, each already sorted by pincode

  Erode      Salem      Namakkal   Karur      Tiruppur   Dharmapuri
  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
  │638001│   │636001│   │637001│   │639001│   │641601│   │636701│  ← ON THE TABLE
  ├──────┤   ├──────┤   ├──────┤   ├──────┤   ├──────┤   ├──────┤
  │638002│   │636003│   │637002│   │639002│   │641602│   │636702│
  │638011│   │636004│   │637003│   │639003│   │641604│   │636703│
  │  ...  │   │ ...  │   │ ...  │   │ ...  │   │ ...  │   │ ...  │
  └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   └──────┘

 THE INVARIANT: each bundle is sorted, so nothing behind a top letter is
 smaller than it. Therefore the smallest letter in the WHOLE load must be
 one of the six on the table. There is nowhere else it can hide.

 take 636001 (Salem)  ->  pull the NEXT Salem letter, 636003, into the gap
 -> six letters on the table again. Never seven, never five.
```

Why the heap is `k` and not `n`:

```
 pop one item                          heap: k -> k-1
 push the next from the SAME list      heap: k-1 -> k

 -> the size is invariant at k (falling only when a list is exhausted)
 -> n pops × O(log k) each  =  O(n log k)
 -> and O(k) SPACE, which is what lets this work on data larger than memory
```

The four approaches, compared:

```
 SCAN ALL k FRONTS EACH TIME          CONCATENATE AND SORT
 for each of n outputs:               [all n items] -> sort
   scan k fronts    -> O(n·k)
                                      O(n log n), O(n) space
 re-compares the same k-1 items       THROWS AWAY the sortedness,
 every single step                    which is the only interesting
                                      property of the input


 SEQUENTIAL PAIRWISE  ← THE TRAP      HEAP OF k FRONTS  ← the answer
 merge(1,2) -> merge(·,3) -> ...      ┌───┐
 the accumulator is re-walked          │ k │  one candidate per list
 each time: 2n + 3n + ... = O(n·k)     └───┘
 LOOKS like divide and conquer;        O(n log k) time, O(k) space
 it is not.                            STREAMS


 TOURNAMENT PAIRWISE  ← also O(n log k)
 round 1: k -> k/2   (n work)
 round 2: k/2 -> k/4 (n work)
 ... log k rounds
 O(n log k), O(n) space, NO HEAP, better cache, parallelises
```

The costs, at scale:

```
 n = 1,000,000 items, k = 100 lists

 approach                comparisons        space
 ---------------------   ----------------   ------
 scan k fronts           100,000,000        O(k)
 concatenate + sort       20,000,000        O(n)
 sequential pairwise     ~50,000,000        O(n)
 HEAP of k fronts          7,000,000        O(k)    ← time AND space
 tournament pairwise       7,000,000        O(n)
```

External sorting, which is why this technique exists:

```
 100 GB file, 8 GB of memory

 PASS 1 — create sorted runs
   read 8 GB, sort in memory, write to disk       ┐
   repeat                                         ├─ ~13 sorted runs on disk
                                                  ┘

 PASS 2 — k-way merge  ← TODAY'S ALGORITHM
   hold ONE BLOCK from each of the 13 runs in memory
   ┌────┬────┬────┬ ... ┬────┐
   │run1│run2│run3│     │r13 │   ← the heap of k fronts
   └────┴────┴────┴ ... ┴────┘
   pop the smallest, write it out, refill from that run

 O(k) memory is the WHOLE POINT: you never hold the file, only k blocks.
 -> this is why MERGE is the sorting algorithm of disks and QUICKSORT is
    the one of memory.
```

---

## 5. The code, built step by step

### Step 1 — state the invariant before writing anything

"Each list is sorted, so nothing behind a list's front element is smaller than that front. Therefore the
overall smallest must be one of the `k` fronts — there is nowhere else it can be. So I keep exactly those
`k` candidates in a heap."

**That sentence is the correctness proof and it takes ten seconds.**

### Step 2 — say the size, because it is the point

"The heap holds `k` items, not `n`. Every pop is followed by at most one push from the same list, so the
size never grows. That is what makes it `O(n log k)` rather than `O(n log n)`, and `O(k)` space rather
than `O(n)`."

### Step 3 — the tuple, with all three fields

```python
    (value, list_index, item_index)
```

"I need to know which list a popped value came from, so I can advance that list. And the list index is
always distinct, so it doubles as a tie-breaker — two equal values never cause Python to compare the
payload."

### Step 4 — heapify the initial fronts, do not push them

```python
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)                     # O(k), not O(k log k)
```

**And skip the empty lists**, or the first pop crashes on an index that does not exist.

### Step 5 — offer the second `O(n log k)` solution

"There is another solution at the same complexity with no heap at all: merge the lists in pairs, then merge
those results in pairs — a tournament, `log k` rounds of `n` work each. It has better cache behaviour and
parallelises, and it needs `O(n)` space unless the lists are linked, which is why the classic version of
this problem uses linked lists."

### The complete solution

```python
import heapq
from typing import Iterable, Iterator


# ---------------------------------------------------------------------------
# 1. The heap solution — O(n log k) time, O(k) space, and it STREAMS
# ---------------------------------------------------------------------------

def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    """LeetCode 23, array form.

    THE INVARIANT: each list is sorted, so nothing behind a list's front is
    smaller than that front. Therefore the overall smallest is one of the k
    fronts — there is nowhere else it can hide. That is the whole proof.

    THE HEAP HOLDS k ITEMS, NEVER n: every pop is followed by at most one
    push from the SAME list, so the size is invariant. That is why this is
    O(n log k) and O(k) space rather than O(n log n) and O(n).

    The tuple is (value, list_index, item_index):
      - list_index says which list to advance after a pop
      - and it is always DISTINCT, so it doubles as the tie-breaker and the
        payload is never compared (day 115's rule, satisfied for free)
    """
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)                     # O(k), not k pushes

    out: list[int] = []
    while heap:
        value, li, ii = heapq.heappop(heap)         # O(log k)
        out.append(value)
        nxt = ii + 1
        if nxt < len(lists[li]):
            heapq.heappush(heap, (lists[li][nxt], li, nxt))
    return out


def merge_k_sorted_lazy(lists: list[list[int]]) -> Iterator[int]:
    """The same, as a generator — so the caller can stop early and the
    output never has to fit in memory. This is what makes it usable for
    external sorting."""
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    while heap:
        value, li, ii = heapq.heappop(heap)
        yield value
        nxt = ii + 1
        if nxt < len(lists[li]):
            heapq.heappush(heap, (lists[li][nxt], li, nxt))


# ---------------------------------------------------------------------------
# 2. Linked lists — the classic framing, because merging is IN PLACE
# ---------------------------------------------------------------------------

class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt


def merge_k_linked_heap(heads: list["ListNode | None"]) -> "ListNode | None":
    """The heap version for linked lists. The tuple carries the NODE, and the
    index is the tie-breaker because ListNode has no __lt__."""
    heap: list[tuple[int, int, ListNode]] = [
        (node.val, i, node) for i, node in enumerate(heads) if node
    ]
    heapq.heapify(heap)

    dummy = ListNode()
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    tail.next = None
    return dummy.next


def merge_two(a: "ListNode | None", b: "ListNode | None") -> "ListNode | None":
    """The two-list merge — the primitive the tournament is built from.
    IN PLACE for linked lists: no new nodes, only pointer changes."""
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k_linked_tournament(heads: list["ListNode | None"]) -> "ListNode | None":
    """THE OTHER O(n log k) SOLUTION — no heap at all.

    Merge in pairs, then merge those results in pairs: log k rounds, each
    doing O(n) work.

    Advantages over the heap: better cache behaviour (two linear scans per
    merge), trivially parallel (the merges in a round are independent), and
    for LINKED lists it is O(1) extra space because merging is in place.

    Disadvantage: it needs all the data up front — it cannot stream.
    """
    if not heads:
        return None
    lists = [h for h in heads if h]
    if not lists:
        return None

    while len(lists) > 1:
        merged: list[ListNode] = []
        for i in range(0, len(lists) - 1, 2):
            merged.append(merge_two(lists[i], lists[i + 1]))    # type: ignore[arg-type]
        if len(lists) % 2:
            merged.append(lists[-1])
        lists = merged                      # k -> k/2, one round done
    return lists[0]


# ---------------------------------------------------------------------------
# 3. The approaches that lose, written out so the difference is concrete
# ---------------------------------------------------------------------------

def merge_by_scanning(lists: list[list[int]]) -> list[int]:
    """O(n·k): re-find the minimum from scratch every time.

    Correct, and it re-compares the same k-1 items on every single step.
    The heap's ONLY job is to avoid re-finding a minimum it already knew.
    """
    positions = [0] * len(lists)
    out: list[int] = []
    total = sum(len(lst) for lst in lists)

    for _ in range(total):
        best_value = None
        best_list = -1
        for i, lst in enumerate(lists):
            if positions[i] < len(lst):
                if best_value is None or lst[positions[i]] < best_value:
                    best_value = lst[positions[i]]
                    best_list = i
        out.append(best_value)               # type: ignore[arg-type]
        positions[best_list] += 1
    return out


def merge_by_concatenating(lists: list[list[int]]) -> list[int]:
    """O(n log n), O(n) space. Correct, simple, and it THROWS AWAY the
    sortedness — which is the only interesting property of the input.
    Also cannot stream."""
    return sorted(v for lst in lists for v in lst)


def merge_sequentially(lists: list[list[int]]) -> list[int]:
    """THE TRAP: it looks like divide and conquer and it is not.

    The accumulator grows every round, so the early elements are walked
    k times: 2n + 3n + ... = O(n·k).
    """
    result: list[int] = []
    for lst in lists:
        merged: list[int] = []
        i = j = 0
        while i < len(result) and j < len(lst):
            if result[i] <= lst[j]:
                merged.append(result[i]); i += 1
            else:
                merged.append(lst[j]); j += 1
        merged.extend(result[i:]); merged.extend(lst[j:])
        result = merged                     # ← re-walked next round
    return result


# ---------------------------------------------------------------------------
# 4. The variants — the same heap, a small change
# ---------------------------------------------------------------------------

def smallest_range(lists: list[list[int]]) -> tuple[int, int]:
    """LeetCode 632: the smallest range containing at least one element from
    each list.

    THE SAME heap of k fronts, plus ONE extra variable: the maximum of the
    current fronts. The range is [heap_min, current_max], and advancing the
    minimum is the only move that can shrink it.
    """
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    current_max = max(lst[0] for lst in lists)

    best = (heap[0][0], current_max)
    while True:
        value, li, ii = heapq.heappop(heap)
        if current_max - value < best[1] - best[0]:
            best = (value, current_max)
        if ii + 1 == len(lists[li]):
            return best                     # one list exhausted: no more ranges
        nxt = lists[li][ii + 1]
        current_max = max(current_max, nxt)
        heapq.heappush(heap, (nxt, li, ii + 1))


def kth_smallest_in_matrix(matrix: list[list[int]], k: int) -> int:
    """LeetCode 378: each row is a sorted list, so this is a k-way merge
    that STOPS after k pops. O(k log rows) rather than O(n log n)."""
    rows = len(matrix)
    heap = [(matrix[r][0], r, 0) for r in range(min(rows, k))]
    heapq.heapify(heap)
    value = 0
    for _ in range(k):
        value, r, c = heapq.heappop(heap)
        if c + 1 < len(matrix[r]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return value


def external_merge_sort(chunks: list[Iterable[int]]) -> Iterator[int]:
    """The reason this technique matters: `heapq.merge` is a lazy k-way
    merge, so it works on runs far larger than memory.

    100 GB with 8 GB of RAM:
      pass 1 — sort chunks that fit, write ~13 runs to disk
      pass 2 — merge the runs, holding ONE BLOCK from each  ← this line
    """
    return heapq.merge(*chunks)


# ---------------------------------------------------------------------------
# 5. Measuring the difference
# ---------------------------------------------------------------------------

def compare(n: int, k: int) -> None:
    """Run this rather than trusting the table."""
    import random
    import time

    per = n // k
    lists = [sorted(random.randint(0, 10 ** 9) for _ in range(per))
             for _ in range(k)]

    for name, fn in (("heap        ", merge_k_sorted),
                     ("concat+sort ", merge_by_concatenating),
                     ("sequential  ", merge_sequentially),
                     ("scan k      ", merge_by_scanning)):
        t = time.perf_counter()
        fn(lists)
        print(f"  {name} {time.perf_counter() - t:.4f}s")


def to_linked(values: list[int]) -> "ListNode | None":
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def from_linked(node: "ListNode | None") -> list[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]

    print(merge_k_sorted(lists))                    # [1, 1, 2, 3, 4, 4, 5, 6]
    print(list(merge_k_sorted_lazy(lists)))         # the same, lazily
    print(merge_by_scanning(lists) == merge_k_sorted(lists))         # True
    print(merge_by_concatenating(lists) == merge_k_sorted(lists))    # True
    print(merge_sequentially(lists) == merge_k_sorted(lists))        # True

    # linked lists — both solutions
    heads = [to_linked(l) for l in lists]
    print(from_linked(merge_k_linked_heap(heads)))  # [1, 1, 2, 3, 4, 4, 5, 6]
    heads = [to_linked(l) for l in lists]
    print(from_linked(merge_k_linked_tournament(heads)))             # same

    # edge cases
    print(merge_k_sorted([]))                       # []
    print(merge_k_sorted([[], [], []]))             # []
    print(merge_k_sorted([[], [1, 2], []]))         # [1, 2]   ← empty lists skipped
    print(merge_k_sorted([[5]]))                    # [5]

    # equal values across lists — the tie-breaker earns its keep
    print(merge_k_sorted([[1, 1], [1, 1], [1]]))    # [1, 1, 1, 1, 1]

    # the variants
    print(smallest_range([[4, 10, 15, 24, 26],
                          [0, 9, 12, 20],
                          [5, 18, 22, 30]]))        # (20, 24)
    print(kth_smallest_in_matrix([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))  # 13

    # heapq.merge is lazy and does this for you
    print(list(heapq.merge([1, 4, 7], [2, 5, 8], [3, 6, 9])))        # [1..9]

    # WHERE THE DIFFERENCE SHOWS — run it
    print("n=100,000 k=100")
    compare(100_000, 100)
```

---

## 6. What it costs

### The four approaches

```
 approach             time          space   streams?   uses sortedness?
 ------------------   -----------   -----   --------   ----------------
 scan k fronts        O(n·k)        O(k)    yes        yes
 concatenate + sort   O(n log n)    O(n)    no         NO
 sequential pairwise  O(n·k)        O(n)    no         yes
 HEAP of k fronts     O(n log k)    O(k)    YES        yes
 tournament pairwise  O(n log k)    O(n)*   no         yes

 * O(1) for linked lists, where merging is in place
```

### At scale

```
 n = 1,000,000 items, k = 100 lists

 scan k fronts        100,000,000 comparisons
 concatenate + sort    20,000,000
 sequential pairwise  ~50,000,000
 heap                   7,000,000        ← 14x better than scanning
 tournament             7,000,000
```

```
 k = 2      log k = 1     the heap gains nothing; just merge them
 k = 10     log k = 3.3   ~3x better than a full sort
 k = 100    log k = 6.6   ~3x better than a full sort, 14x better than scanning
 k = 10,000 log k = 13.3  approaching log n; the advantage narrows
```

**When `k` approaches `n` — many tiny lists — `log k` approaches `log n` and the heap's advantage
disappears.** At that point concatenate and sort, because its constants are far better.

### Space, which is the more important difference

```
 n = 100,000,000 items (does not fit in memory), k = 50 runs

 concatenate + sort   O(n)   -> IMPOSSIBLE
 tournament           O(n)   -> IMPOSSIBLE (for arrays)
 heap of k fronts     O(k)   -> 50 entries. Trivial.
```

**That is the whole reason external sorting works**, and it is why "merge" is the disk-world sorting
algorithm.

### The heap versus the tournament, honestly

```
 same complexity: O(n log k)

 HEAP                              TOURNAMENT
 log k comparisons per element     log k comparisons per element
 random access into the heap       two LINEAR scans per merge
 -> poor cache locality            -> excellent cache locality
 O(k) space                        O(n) space (O(1) for linked lists)
 STREAMS                           needs everything up front
 sequential                        the merges in a round are INDEPENDENT
                                   -> trivially parallel
```

**Measured, the tournament is often 1.5–2× faster on arrays in memory**, and the heap is the only one that
works when the data does not fit. **Neither dominates**, which is why both are worth naming.

### Where the constants live

```
 each heap pop:      ~log k comparisons, plus tuple allocation in Python
 each tournament
   merge step:       1 comparison, and sequential memory access
```

**In Python the tuple allocation per push is a real cost** — a heap of a million pushes allocates a million
three-tuples at about 72 bytes each. `heapq.merge` avoids some of this internally, which is one reason to
prefer it over a hand-rolled loop.

---

## 7. The traps

### Trap 1 — a heap of everything instead of a heap of `k`

```python
    heap = [v for lst in lists for v in lst]        # ALL n items
    heapq.heapify(heap)
```

Correct output, and it is `O(n)` space and `O(n log n)` time — which is just "concatenate and sort" with
extra steps. **The whole point is that the heap holds one candidate per list.**

**And on a stream it is not merely slower, it is impossible.**

### Trap 2 — not skipping empty lists

```python
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
```

```
 IndexError: list index out of range
```

An empty input list has no `lst[0]`. **The `if lst` guard is not defensive coding — it is required**, and
`[[], [1, 2], []]` is the first test case anyone runs.

### Trap 3 — no tie-breaker with an unorderable payload

```python
    heapq.heappush(heap, (node.val, node))          # two nodes with val 5
```

```
 TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
```

[Day 115's](../day-115-heapq/README.md) trap, and it appears in exactly this problem because equal values
across lists are common. **The list index is the natural tie-breaker and it is always distinct**, so
`(value, index, node)` fixes it for free.

### Trap 4 — sequential merging, believing it is divide and conquer

```python
    for lst in lists:
        result = merge_two(result, lst)
```

`O(n·k)`, because the accumulator is re-walked every round: `2n + 3n + 4n + …`. **The tournament pairs them
up so that each round touches every element exactly once** — that one structural difference is `O(n·k)`
against `O(n log k)`.

### Trap 5 — advancing the wrong list

```python
        value, li, ii = heapq.heappop(heap)
        heapq.heappush(heap, (lists[0][ii + 1], 0, ii + 1))     # always list 0
```

You must advance the list the popped value came from, which is why the tuple carries `list_index`. **This
produces plausible-looking but wrong output**, not a crash.

### Trap 6 — pushing before checking the bound

```python
        heapq.heappush(heap, (lists[li][ii + 1], li, ii + 1))   # no bound check
```

```
 IndexError: list index out of range
```

when a list is exhausted. **The heap shrinks as lists run out** — that is normal and expected, and the
`if nxt < len(...)` guard is what allows it.

### Trap 7 — `heapify` versus `k` pushes

```python
    for i, lst in enumerate(lists):
        heapq.heappush(heap, (lst[0], i, 0))        # O(k log k)
```

Correct, and `heapify` is `O(k)`. Negligible when `k` is small, and it is the same
[day 114](../day-114-heapify/README.md) point, so it is worth getting right by habit.

### Trap 8 — building the output list when the caller wants a stream

```python
    return out                              # O(n) memory for the result
```

If the point is that the data does not fit in memory, **returning a list defeats it**. Yield instead —
which is what `heapq.merge` does, and it is the difference between a technique that works on a hundred
gigabytes and one that does not.

---

## 8. In the interview

### How it gets asked

- The classic: *"Merge k sorted linked lists."* LeetCode 23.
- The complexity probe: *"Why `O(n log k)` and not `O(n log n)`?"*
- The alternative probe: *"Can you do it without a heap?"*
- The applied one: *"How would you sort a file larger than memory?"*
- The variant: *"Find the smallest range covering at least one element from each list."* LeetCode 632.

### What to say out loud, in the first ninety seconds

1. **State the invariant, which is the proof.** "Each list is sorted, so nothing behind a list's front is
   smaller than that front. So the overall smallest must be one of the `k` fronts — there is nowhere else
   it can be."
2. **Say what the heap holds, because that is the answer.** "So I keep exactly those `k` candidates in a
   heap: one per list. Pop the smallest, output it, and push the next item from **that** list."
3. **Give the complexity with the reason attached.** "`n` pops at `O(log k)` each, because the heap holds
   `k` and not `n` — so `O(n log k)` time and, more importantly, `O(k)` **space**."
4. **Say what the tuple carries and why.** "The entry is `(value, list index, position)`. I need the list
   index to know which list to advance — and it is always distinct, so it also serves as the tie-breaker
   and the payload is never compared."
5. **Offer the second solution.** "There is another `O(n log k)` with no heap: merge in pairs, then merge
   those in pairs — `log k` rounds of `n` work. Better cache behaviour and it parallelises; it needs
   `O(n)` space unless the lists are linked."
6. **Name the real use.** "This is exactly the merge phase of an external sort, which is how you sort a
   file larger than memory — and the `O(k)` space is the whole reason it works."

### The follow-ups

**"Why `O(n log k)` and not `O(n log n)`?"**
"Because of what the heap contains. It holds **one candidate per list** — `k` items — not all `n`. Every
pop is followed by at most one push, and that push comes from the same list the popped item came from, so
the size is invariant at `k` and only falls as lists are exhausted. So the cost is `n` pops at `O(log k)`
each. Concretely, at a million items across a hundred lists that is about seven million comparisons
against twenty million for a full sort — three times fewer. But the difference I care about more is
**space**: `O(k)` instead of `O(n)`. With a hundred million items across fifty runs, the heap holds fifty
entries, which is what makes the technique work on data that does not fit in memory at all."

**"Can you do it without a heap?"**
"Yes, and at the same complexity. **Merge the lists in pairs**, then merge those results in pairs, and so
on — a knockout tournament. There are `log k` rounds, and each round touches every element exactly once,
so it is `O(n)` per round and `O(n log k)` overall. It has real advantages: no priority queue at all, just
the two-list merge; **much better cache behaviour**, because each merge is two linear scans rather than
random access into a heap; and the merges within a round are independent, so it **parallelises trivially**.
Measured on arrays in memory it is often one and a half to two times faster than the heap. Its
disadvantage is space: `O(n)` for the intermediate results — though for **linked lists** merging is in
place, so it is `O(1)`, which is exactly why the classic version of this problem uses linked lists. And it
cannot stream, which is where the heap wins outright."

**"What is the trap here?"**
"Merging them **sequentially** — merge list one with list two, then that result with list three, and so
on. It looks like the same idea and it is `O(n·k)`, because the accumulated result is re-walked on every
round: `2n + 3n + 4n + …`. The elements of the first list get copied `k` times. The tournament version
pairs them up so that each round touches every element exactly once, and that single structural difference
is `O(n·k)` against `O(n log k)`. The other trap is putting **all** `n` items in the heap, which produces
the right answer and is just 'concatenate and sort' with extra steps — and on a stream it is not slower,
it is impossible."

**"How would you sort a file larger than memory?"**
"An external merge sort, and its second phase is exactly this problem. **Pass one**: read as much as fits
in memory, sort it, write it out as a sorted run, and repeat — a hundred gigabytes with eight gigabytes of
memory gives about thirteen runs. **Pass two**: do a k-way merge of those thirteen runs, holding one
**block** from each in memory rather than the whole run. That is the heap of `k` fronts, and the `O(k)`
memory is the entire reason it is possible. It also explains a broader fact: merge is the sorting algorithm
of the disk world and quicksort is the one of memory, because quicksort needs random access while merging
is sequential in every direction — which is exactly what disks and network streams are good at. The same
machinery is what a database uses to merge sorted index scans, and what log-structured storage engines use
to compact SSTables."

**"Now find the smallest range covering an element from each list."**
"The same heap, with one extra variable. I keep the `k` fronts in a min-heap as before, and I also track
the **maximum** of the current fronts. At any moment the range `[heap minimum, current maximum]` covers at
least one element from every list, because the heap holds exactly one per list. To shrink it I must raise
the minimum — nothing else can help — so I pop the smallest, record the range if it is the best so far,
and push the next item from that list, updating the maximum. I stop as soon as one list is exhausted,
because from then on no range can cover all `k`. It is `O(n log k)` and the insight is that the heap is
already doing the work; I just needed to notice what else its contents tell me."

**"What are the edge cases?"**
"Four, and they all appear in the tests. **An empty input list** among the others — `lst[0]` raises, so the
initial heap build must skip empties; `[[], [1,2], []]` is the first case anyone runs. **All lists empty**,
which should return empty rather than crash. **Equal values across lists**, which is common and is exactly
where a missing tie-breaker raises `TypeError` — the list index solves it for free because it is always
distinct. And **a list running out mid-merge**, which is normal: the heap simply shrinks, and the
`if next_index < len(list)` guard is what allows that rather than an `IndexError`. I would also check `k =
1` and a single-element list, because both exercise the loop boundaries."

### A model answer

Asked: *merge k sorted lists efficiently.*

> "Let me start with why this can be done better than sorting everything, because that argument is the
> solution.
>
> Each list is already **sorted**. So within any list, nothing behind the front element is smaller than
> that front element. Which means the smallest item in the entire collection has to be at the **front of
> some list** — there is nowhere else it could be hiding. So at any moment I only ever need to consider
> `k` candidates: one per list.
>
> That is exactly what a heap is for. I put the `k` front elements in a min-heap, pop the smallest, write
> it to the output, and then push the **next** element from the list I just took from. The heap goes from
> `k` to `k−1` and back to `k`, so its size never grows.
>
> **That invariant is the whole complexity result**: the heap holds `k` items, not `n`. There are `n` pops
> and each costs `O(log k)`, so it is `O(n log k)` time — about seven million comparisons for a million
> items across a hundred lists, against twenty million for a full sort. And it is `O(k)` **space**, which
> matters more, because it means the technique works when the data does not fit in memory.
>
> One implementation detail: the heap entry is `(value, list index, position)` rather than just the value.
> I need the list index to know which list to advance after a pop — and because it is always distinct, it
> also acts as the tie-breaker, so when two lists have equal values Python never tries to compare whatever
> comes after. That matters here because equal values across lists are common, and without it you get a
> `TypeError` on nodes or objects.
>
> I would also mention the second `O(n log k)` solution, because it is genuinely different: **merge the
> lists in pairs, then merge those results in pairs** — a tournament, `log k` rounds each doing `O(n)`
> work. It uses no heap at all, has much better cache behaviour because every merge is two linear scans,
> and the merges within a round are independent so it parallelises. Its cost is `O(n)` space for the
> intermediates — unless the lists are **linked lists**, where merging is in place and it is `O(1)`, which
> is exactly why the classic version of this problem is posed with linked lists.
>
> The trap I would avoid explicitly is merging them **sequentially** — first with second, then that with
> third — because the accumulator is re-walked every round and it degenerates to `O(n·k)`. Pairing them up
> is what makes each round touch every element once.
>
> And the reason this is worth knowing beyond the interview: it is the merge phase of an **external
> sort**. To sort a hundred gigabytes with eight gigabytes of memory, you write sorted runs and then do a
> k-way merge holding one block from each — the `O(k)` memory is the entire point."

---

## 9. Recall card

- **The invariant IS the proof: each list is sorted, so nothing behind a list's front is smaller than that
  front — therefore the overall smallest is one of the `k` fronts, and there is nowhere else it can be.**
  Keep exactly those `k` candidates in a heap.
- **The heap holds `k`, never `n`** — every pop is followed by at most one push **from the same list**, so
  the size is invariant. That gives **`O(n log k)` time** (7M comparisons against 20M for a sort at n = 1M,
  k = 100) and — the part that matters more — **`O(k)` space**, which is what lets it work on data larger
  than memory.
- **The entry is `(value, list_index, position)`.** The index says which list to advance, and because it is
  always **distinct** it doubles as the **tie-breaker** — equal values across lists are common, and without
  it you get `TypeError` on unorderable payloads.
- **There is a second `O(n log k)` with no heap: a pairwise TOURNAMENT** — `log k` rounds, `O(n)` each.
  Better cache locality, trivially parallel, `O(n)` space (**`O(1)` for linked lists, which is why the
  classic problem uses them**), but it cannot stream. **The trap is SEQUENTIAL pairwise merging**, which
  re-walks the accumulator and is `O(n·k)`.
- **This is the merge phase of an EXTERNAL SORT**: sort runs that fit in memory, then k-way merge holding
  one block per run. It is why **merge is the disk world's sorting algorithm and quicksort is memory's**.
  Edge cases that bite: **skip empty lists** when building the heap (`IndexError` otherwise), bound-check
  before pushing, and expect the heap to **shrink** as lists are exhausted.
