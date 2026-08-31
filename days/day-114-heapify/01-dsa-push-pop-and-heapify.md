---
day: 114
track: dsa
title: "Push, pop, and heapify"
phase: "Heaps and priority queues"
status: written
---

# Day 114 · DSA — Push, pop, and heapify

**After today you can:** You can sift up and sift down by hand, and know why build-heap is O(n).

**The interviewer asks it as:** *Insert into the heap. Now remove the minimum.*

---

## 1. What this is, and why they ask it

[Yesterday](../day-113-the-heap/README.md) was the structure. Today is the two operations that maintain
it — **sift up** and **sift down** — and the one surprising fact that comes out of them.

Three sentences. Both operations are the same shape: a value is in the wrong place, and it **swaps its way
along one root-to-leaf path** until the heap property holds again, which is at most `log n` swaps. Insert
puts the new value at the end and sifts it **up**; extract moves the last value to the root and sifts it
**down** — and the choice of *which* element to move is not arbitrary, it is the only choice that keeps
the tree complete. And then the surprise: **building a heap from `n` items costs `O(n)`, not
`O(n log n)`**, which looks wrong and is the single most-asked follow-up in this topic.

They ask you to insert and extract by hand because it takes ninety seconds and shows whether you can hold
an invariant while mutating a structure. They ask *"why is heapify `O(n)`?"* because the intuitive answer
is `O(n log n)` and the real answer requires you to notice that **most nodes are near the bottom and have
almost nowhere to sink.**

---

## 2. The story

The annual day photograph was the same argument every year and Mrs Fernandes had been running it since
1997.

Two hundred and forty children, six rows, shortest at the front. Getting them into height order took
between forty minutes and — one memorable year — the whole morning.

The way it had always been done was one child at a time. A child walks up, and you find where they belong,
and everybody after that point shuffles along one place. Two hundred and forty times. The last child in
the queue might displace a hundred and eighty people to slot into the middle.

In 2003 a new PT master took it over and did it in about eleven minutes, and the way he did it looked
wrong to everybody watching.

He did not start at the front. He put all two hundred and forty children into the six rows in whatever
order they happened to be standing — no sorting at all — and then he started at the **back**.

He walked along the back row and did nothing at all, because there was nobody behind them to compare
against. He said that was half the school dealt with in one pass of looking.

Then the second row from the back. For each child there, he compared them with the two children standing
directly behind them, and if one of those two was shorter, they swapped. One swap, maybe two, and then he
moved on. Nobody in that row could travel more than one row backwards, because there was only one row
behind them.

Then the third row from the back, where a child could sink at most two rows. Then the fourth, at most
three.

By the time he reached the front row — where a child could in principle travel all the way to the back —
there were only four children in it.

Mrs Fernandes said afterwards that the thing she had not seen was where the work actually was. She had
always assumed that if the worst case is walking a child from the front to the back, and there are two
hundred and forty children, it must be two hundred and forty times six.

The PT master said no. Half of them are in the back row and move nowhere. A quarter are one row in and
move at most one. An eighth move at most two. The children who *could* travel a long way are the few at
the front, and there are almost none of them.

He said: the long journeys are rare and the short journeys are common, and if you add it up properly it
comes to roughly one move per child.

---

## 3. The idea in plain English

The PT master has just performed a `heapify`, bottom-up, and his final paragraph is the proof that it is
`O(n)`.

- Inserting one child at a time and shuffling is **`n` pushes**, at `O(log n)` each.
- Starting at the back and working forwards is **bottom-up heapify**.
- "Half of them are in the back row and move nowhere" is the reason it is `O(n)` and not `O(n log n)`.
- Comparing with the two children directly behind is **sift-down**.

### Sift up: used by insert

A value is too small for its position. Compare it with its parent; if it is smaller, swap; repeat.

```python
    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self.data[i] >= self.data[parent]:
                break                       # the property holds — STOP
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent
```

**It walks one path towards the root**, so at most `height` swaps: `O(log n)`.

**Insert appends first, and that is not a detail.** Putting the new value at the end of the array is the
only place that keeps the tree **complete** — any other position leaves a gap and destroys the array
layout. The value is then almost certainly in the wrong place, and sifting up fixes it.

### Sift down: used by extract

A value is too large for its position. Compare it with **both** children; if either is smaller, swap with
**the smaller of the two**; repeat.

```python
    def _sift_down(self, i: int) -> None:
        n = len(self.data)
        while True:
            smallest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == i:
                return
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest
```

**Swap with the smaller child, not just any smaller child.** If you swap with the larger one, the new
parent is bigger than its other child and the property is still broken — silently. That is trap 2.

### Extract: why the *last* element moves to the root

```python
        smallest = self.data[0]             # the answer
        last = self.data.pop()              # remove from the END
        if self.data:
            self.data[0] = last             # move it to the root
            self._sift_down(0)
        return smallest
```

**You cannot just delete index 0** — that leaves a hole at the root and the array layout has no way to
represent a hole. And you cannot promote the smaller child, because that leaves a hole one level down and
you have the same problem recursively.

**The last element is the only one whose removal keeps the tree complete.** So you move it to the root —
where it is almost certainly far too big — and let it sink. Everything else is a consequence of the
completeness rule.

### Heapify: the `O(n)` surprise

Given an unordered array, make it a heap. **Two ways, and they are not the same cost.**

```
 TOP-DOWN:     push each of the n items       n × O(log n)  =  O(n log n)
 BOTTOM-UP:    sift down from the last parent backwards to the root  =  O(n)
```

```python
    for i in range(len(data) // 2 - 1, -1, -1):
        sift_down(i)
```

Three things to say about that line:

**Start at the last parent, not the last element.** Everything from index `n//2` onwards is a **leaf**, and
a leaf is trivially a valid heap of one node. **That is already half the array skipped**, and it is the
first half of the argument.

**Go backwards.** Sifting down a node requires both its subtrees to already be heaps, and processing in
decreasing index order guarantees that.

**And why it is `O(n)`:**

```
 nodes at depth d          ≈ n / 2^(d+1)
 work per node at depth d  ≤ (height − d) swaps

 total  =  Σ  (n / 2^(d+1)) × (h − d)
        =  n × Σ (h − d) / 2^(d+1)
        ≈  n × Σ k/2^k          (which converges to 2)
        =  O(n)
```

**The intuition is the PT master's, and it is what to say out loud:** *"Half the nodes are leaves and do
zero work. A quarter can sink at most one level. An eighth at most two. The nodes that could travel far
are rare, and the ones that are common travel almost nowhere — and the sum converges to about two swaps
per node."*

**Notice the asymmetry**, because it is a good follow-up: doing the same thing with sift-**up** from the
top is genuinely `O(n log n)`, because then the *many* nodes at the bottom are the ones that could travel
far. **The direction matters, and it matters because of where the nodes are.**

### Heapsort, which falls out for free

Build a max-heap in `O(n)`, then repeatedly swap the root with the last element and shrink the heap by
one:

```python
    build_max_heap(a)
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]         # the largest goes to its final place
        sift_down(a, 0, end)                # restore the heap over a[0:end]
```

```
 O(n log n) time, O(1) extra space, in place
```

**It is the only common sort that is `O(n log n)` in the worst case *and* uses constant extra space.**
Merge sort needs `O(n)` extra; quicksort is `O(n²)` in the worst case. Heapsort is neither — and it is
still not what anyone uses, because its cache behaviour is poor: sift-down jumps to `2i+1`, then `4i+3`,
scattering across memory, where quicksort scans linearly.

**That trade — better worst case, worse constants — is worth stating**, because it explains why a
theoretically superior algorithm loses in practice.

### Push-then-pop, and the two shortcuts

Two `heapq` functions exist because the naive pairs waste a pass:

```
 heappushpop(h, x)    push then pop        — if x <= h[0], return x immediately
 heapreplace(h, x)    pop then push        — one sift-down instead of two passes
```

**`heapreplace` is the one that matters for [top-k](../day-116-top-k/README.md)**: keeping a heap of size
`k` means "if this beats the smallest, replace it", which is exactly one operation rather than a pop
followed by a push.

### Increase-key and decrease-key

If a value already in the heap changes:

```
 the value DECREASED  ->  sift UP    (it may now be too small for its position)
 the value INCREASED  ->  sift DOWN
```

Both are `O(log n)` **once you know where the element is** — and finding it is `O(n)`, which is
[yesterday's](../day-113-the-heap/README.md) weakness. Hence the **indexed heap**: a hash map from value
to index, updated on every swap.

**Python has neither.** The idiomatic workaround is **lazy deletion**: push a new entry and mark the old
one stale, skipping stale entries as they surface. It is [day 115](../day-115-heapq/README.md), and it is
what a Dijkstra implementation in Python actually does.

---

## 4. The picture

Sift up and sift down, side by side. **Both walk one path; they differ in which way and how many
comparisons per step.**

```
 SIFT UP (insert 0)                    SIFT DOWN (after moving 6 to the root)

        1                                     6
      /   \                                 /   \
     3     2                               3     2
    / \   / \                             / \   /
   7   4 5   6                           7   4 5
  /
 0  ← appended at the end

 compare with the PARENT only           compare with BOTH children,
 (one comparison per level)             swap with the SMALLER
                                        (two comparisons per level)

 0 < 7  swap                            6 vs (3, 2) -> 2 is smaller, swap
 0 < 3  swap                            6 vs (5)    -> 5 is smaller, swap
 0 < 1  swap                            done
 at the root: stop

 at most `height` swaps either way = O(log n)
```

Why the **last** element moves to the root:

```
 EXTRACT from                 WRONG: delete index 0 and promote a child

        1                              _              ← a HOLE at the root
      /   \                          /   \
     3     2                        3     2           the array has no way to
    / \   /                        / \   /             represent a hole, and
   7   4 5                        7   4 5              promoting 2 leaves a hole
                                                       where 2 was — recursively

 RIGHT: take 1 (the answer), move the LAST element (5) to the root,
        and let it sink.

        5            ->        2
      /   \                  /   \
     3     2                3     5
    / \                    / \
   7   4                  7   4

 the LAST element is the ONLY one whose removal keeps the tree COMPLETE.
```

**The `O(n)` heapify argument, drawn.** This is the diagram to reproduce.

```
 a heap of 15 nodes, height 3

 depth 0:  ● ────────────────────  1 node,  can sink 3 levels   =  3 work
 depth 1:  ● ●  ──────────────────  2 nodes, can sink 2 levels   =  4
 depth 2:  ● ● ● ●  ───────────────  4 nodes, can sink 1 level    =  4
 depth 3:  ● ● ● ● ● ● ● ●  ───────  8 nodes, can sink 0 levels   =  0
                                                                 ----
                                                       total  =  11 swaps
                                                       for 15 nodes  ≈ 0.7 each

 HALF the nodes are LEAVES and do ZERO work.
 A quarter can move at most one level.
 The nodes that could travel far are the RARE ones at the top.

 Σ (n / 2^(d+1)) × (h − d)  ≈  n × Σ k/2^k  =  2n   ->  O(n)
```

The asymmetry, which is the good follow-up:

```
 BOTTOM-UP with sift-DOWN            TOP-DOWN with sift-UP (n pushes)

 the MANY nodes (leaves) move        the MANY nodes (leaves) are inserted LAST
 almost NOWHERE                      and can travel the FULL height

 depth 3: 8 nodes × 0 = 0            the 8 leaves × up to 3 levels = 24
 depth 0: 1 node × 3  = 3            the root × 0 = 0
 -> O(n)                             -> O(n log n)

 SAME structure, SAME final heap, DIFFERENT cost.
 The direction matters because of WHERE THE NODES ARE.
```

Heapsort, in place:

```
 [ heap region ][ sorted region ]

 build a MAX-heap over the whole array          O(n)
 repeat:
   swap a[0] with a[end]      ← the largest goes to its final place
   end -= 1                   ← the sorted region grows from the right
   sift_down(a, 0, end)       ← restore the heap over the shrinking region

 [9 5 8 1 3 2]  ->  [8 5 2 1 3 | 9]  ->  [5 3 2 1 | 8 9]  ->  ...
                                    ▲
                              sorted, and never touched again

 O(n log n) worst case, O(1) extra space, in place.
```

---

## 5. The code, built step by step

### Step 1 — say what both operations have in common

"Both restore the invariant by moving one value along **one root-to-leaf path**, swapping as it goes.
Neither touches anything off that path, which is why both are `O(log n)` and not `O(n)`."

### Step 2 — sift up, and where the loop stops

```python
        while i > 0 and data[i] < data[(i - 1) // 2]:
```

"Stop at the root, or as soon as the parent is no larger. The early stop matters: on a typical insertion
the new value only rises one or two levels, so `O(log n)` is the bound and the average is close to
constant."

### Step 3 — sift down, and the smaller child

```python
            if right < n and data[right] < data[smallest]:
                smallest = right
```

**"Swap with the smaller of the two children."** Say it as you write it. Swapping with the larger one
leaves the new parent greater than its other child — the property is still violated, and nothing raises.

### Step 4 — extract, and why the last element

"I take index 0 as the answer, move the **last** element to the root, and sift it down. It has to be the
last one, because that is the only removal that keeps the tree complete — anything else leaves a hole the
array cannot represent."

### Step 5 — heapify from the last parent, backwards

```python
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)
```

"Start at `n//2 − 1`, the last node that has a child — everything after it is a leaf and is already a
valid heap. Go backwards, because sifting down a node needs its subtrees to be heaps already."

### Step 6 — say why it is `O(n)` before being asked

"Half the nodes are leaves and do no work at all. A quarter can sink at most one level, an eighth at most
two. The nodes that could travel the full height are the handful near the root. Summed properly it comes
to about two swaps per node, so `O(n)`."

### The complete solution

```python
import heapq


# ---------------------------------------------------------------------------
# The two primitives. Everything else is built from these.
# ---------------------------------------------------------------------------

def sift_up(data: list[int], i: int) -> None:
    """Move data[i] UP while it is smaller than its parent.

    Walks ONE path towards the root: at most `height` swaps, O(log n).
    Only ONE comparison per level, because a node has only one parent.
    """
    while i > 0:
        parent = (i - 1) // 2
        if data[i] >= data[parent]:
            break                           # the property holds — stop early
        data[i], data[parent] = data[parent], data[i]
        i = parent


def sift_down(data: list[int], i: int, end: int | None = None) -> None:
    """Move data[i] DOWN while it is larger than a child.

    TWO comparisons per level, and it MUST swap with the SMALLER child —
    swapping with the larger one leaves the new parent bigger than its other
    child, and the property is still broken with no error.

    `end` bounds the heap region, which is what heapsort needs.
    """
    n = len(data) if end is None else end
    while True:
        smallest = i
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and data[left] < data[smallest]:
            smallest = left
        if right < n and data[right] < data[smallest]:
            smallest = right                # the SMALLER of the two
        if smallest == i:
            return
        data[i], data[smallest] = data[smallest], data[i]
        i = smallest


# ---------------------------------------------------------------------------
# The operations
# ---------------------------------------------------------------------------

def push(data: list[int], value: int) -> None:
    """APPEND, then sift up.

    Appending is not a stylistic choice: the end of the array is the ONLY
    position that keeps the tree COMPLETE.
    """
    data.append(value)
    sift_up(data, len(data) - 1)


def pop_min(data: list[int]) -> int:
    """Take index 0, move the LAST element to the root, sift down.

    It has to be the last element: that is the only removal that keeps the
    tree complete. Deleting index 0 would leave a hole the array cannot
    represent, and promoting a child moves the hole down recursively.
    """
    if not data:
        raise IndexError("pop from an empty heap")
    smallest = data[0]
    last = data.pop()
    if data:                                # not the element we just removed
        data[0] = last
        sift_down(data, 0)
    return smallest


def heapify(data: list[int]) -> None:
    """Build a heap IN PLACE, in O(n) — not O(n log n).

    Start at the LAST PARENT (n//2 - 1): everything after it is a leaf, and
    a leaf is already a valid heap of one node. That is HALF the array
    skipped before any work happens.

    Go BACKWARDS: sifting down a node requires both its subtrees to be heaps
    already, which decreasing index order guarantees.

    WHY O(n): nodes at depth d number about n/2^(d+1) and can sink at most
    (h - d) levels. Summing gives n × Σ k/2^k, and that series converges to
    2 — so about 2 swaps per node.

    Half the nodes are leaves and do ZERO work. The nodes that could travel
    far are the rare ones at the top.
    """
    for i in range(len(data) // 2 - 1, -1, -1):
        sift_down(data, i)


def heapify_by_pushing(items: list[int]) -> list[int]:
    """The O(n log n) way, for contrast. Same result, more work — because
    now the MANY nodes (the leaves) are the ones inserted last, and they can
    travel the full height."""
    out: list[int] = []
    for v in items:
        push(out, v)
    return out


# ---------------------------------------------------------------------------
# Heapsort
# ---------------------------------------------------------------------------

def _sift_down_max(data: list[int], i: int, end: int) -> None:
    while True:
        largest = i
        left, right = 2 * i + 1, 2 * i + 2
        if left < end and data[left] > data[largest]:
            largest = left
        if right < end and data[right] > data[largest]:
            largest = right
        if largest == i:
            return
        data[i], data[largest] = data[largest], data[i]
        i = largest


def heapsort(data: list[int]) -> list[int]:
    """In place, O(n log n) WORST CASE, O(1) extra space.

    The only common sort with both of those properties: merge sort needs
    O(n) extra, quicksort is O(n^2) in the worst case.

    And still not what anyone uses, because sift_down jumps to 2i+1 then
    4i+3 — scattering across memory — where quicksort scans linearly and
    wins on cache behaviour.
    """
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):     # build a MAX-heap, O(n)
        _sift_down_max(data, i, n)
    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]     # largest to its final place
        _sift_down_max(data, 0, end)                # restore over the prefix
    return data


# ---------------------------------------------------------------------------
# The shortcuts, and why they exist
# ---------------------------------------------------------------------------

def push_pop(data: list[int], value: int) -> int:
    """Push then pop, in ONE pass. If the new value is already the smallest,
    it never enters the heap at all."""
    if data and data[0] < value:
        value, data[0] = data[0], value
        sift_down(data, 0)
    return value


def replace(data: list[int], value: int) -> int:
    """Pop then push, in ONE sift-down instead of two passes.
    THE operation for a fixed-size top-k heap."""
    smallest = data[0]
    data[0] = value
    sift_down(data, 0)
    return smallest


def update_at(data: list[int], i: int, value: int) -> None:
    """Change a value already in the heap.

    DECREASED -> sift up.  INCREASED -> sift down.
    Both O(log n) — ONCE YOU KNOW THE INDEX. Finding it is O(n), which is
    why an indexed heap (a value -> index map, maintained on every swap)
    exists, and why Python uses lazy deletion instead.
    """
    old = data[i]
    data[i] = value
    if value < old:
        sift_up(data, i)
    else:
        sift_down(data, i)


def is_heap(data: list[int]) -> bool:
    return all(data[(i - 1) // 2] <= data[i] for i in range(1, len(data)))


def count_swaps_heapify(data: list[int]) -> int:
    """Instrumented heapify, so the O(n) claim is measured rather than
    asserted."""
    swaps = 0

    def sd(i: int) -> None:
        nonlocal swaps
        n = len(data)
        while True:
            smallest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and data[left] < data[smallest]:
                smallest = left
            if right < n and data[right] < data[smallest]:
                smallest = right
            if smallest == i:
                return
            data[i], data[smallest] = data[smallest], data[i]
            swaps += 1
            i = smallest

    for i in range(len(data) // 2 - 1, -1, -1):
        sd(i)
    return swaps


def count_swaps_pushing(items: list[int]) -> int:
    out: list[int] = []
    swaps = 0
    for v in items:
        out.append(v)
        i = len(out) - 1
        while i > 0:
            parent = (i - 1) // 2
            if out[i] >= out[parent]:
                break
            out[i], out[parent] = out[parent], out[i]
            swaps += 1
            i = parent
    return swaps


if __name__ == "__main__":
    h: list[int] = []
    for v in (5, 3, 8, 1, 9, 2, 7):
        push(h, v)
    print(h, is_heap(h))                    # [1, 3, 2, 5, 9, 8, 7] True

    print(pop_min(h), h, is_heap(h))        # 1 [2, 3, 7, 5, 9, 8] True

    # heapify in place
    a = [9, 4, 7, 1, 8, 2, 6, 3, 5]
    heapify(a)
    print(a, is_heap(a))                    # a valid heap, min at index 0

    # THE O(n) CLAIM, MEASURED
    import random
    random.seed(1)
    for n in (1_000, 10_000, 100_000):
        items = [random.randint(0, 10**6) for _ in range(n)]
        bottom_up = count_swaps_heapify(items[:])
        top_down = count_swaps_pushing(items[:])
        print(f"n={n:>7}  bottom-up {bottom_up:>8} ({bottom_up/n:.2f}/node)"
              f"   top-down {top_down:>8} ({top_down/n:.2f}/node)")
    # bottom-up stays near ~1 swap per node; top-down grows with log n

    # heapsort
    print(heapsort([9, 4, 7, 1, 8, 2, 6, 3, 5]))    # [1..9]
    print(heapsort([]), heapsort([1]))               # [] [1]

    # the shortcuts
    k = [3, 5, 8]
    heapify(k)
    print(push_pop(k[:], 1))                # 1 — never enters the heap
    print(replace(k[:], 10), k)             # 3 (the old min) returned

    # update
    u = [1, 3, 2, 7, 4, 5, 6]
    update_at(u, 6, 0)                      # decrease 6 -> 0
    print(u, is_heap(u))                    # 0 has risen to the root

    # heapq does all of this in C
    lst = [9, 4, 7, 1, 8]
    heapq.heapify(lst)                      # O(n)
    print(heapq.heappushpop(lst, 0))        # 0
    print(heapq.heapreplace(lst, 100))      # 1
    print(lst[0])                           # 4
```

---

## 6. What it costs

### The operations

```
 sift up            O(log n)   one comparison per level
 sift down          O(log n)   TWO comparisons per level
 push               O(log n)   append + sift up
 pop                O(log n)   swap in the last + sift down
 heapify (bottom-up) O(n)      the surprise
 heapify (n pushes)  O(n log n)
 heapsort            O(n log n) worst case, O(1) extra space
 update a known index O(log n)
 find an element      O(n)
```

**Sift down does twice the comparisons of sift up per level**, which is why `heapreplace` (one sift down)
is preferred over pop-then-push (a sift down plus a sift up).

### The `O(n)` argument, in numbers

```
 a heap of n = 15, height 3

 depth   nodes   max sinks   work
 -----   -----   ---------   ----
   0       1         3         3
   1       2         2         4
   2       4         1         4
   3       8         0         0
                              ---
                               11 swaps for 15 nodes  ≈ 0.73 per node
```

```
 n            bottom-up swaps      top-down swaps      ratio
 ----------   -----------------    ----------------    -----
 1,000        ~900                 ~2,000              2.2x
 10,000       ~9,000               ~26,000             2.9x
 100,000      ~90,000              ~330,000            3.7x

 bottom-up stays at ~0.9 swaps per node as n grows.
 top-down grows like log n per node.
```

**The instrumented version is in the code above — run it rather than trusting the table.**

### The series, for the follow-up

```
 total work  =  Σ_{d=0}^{h}  (n / 2^(d+1)) × (h − d)

 substitute k = h − d:

             =  n × Σ_{k=0}^{h}  k / 2^(h−k+1)
             ≈  n × Σ_{k≥0}  k / 2^k
             =  n × 2
             =  O(n)
```

**`Σ k/2^k = 2` is the fact worth remembering.** It is why the answer is about two swaps per node, and it
is the whole content of the proof.

### Heapsort against the alternatives

```
                 worst case    average      extra space   stable   in practice
 quicksort       O(n^2)        O(n log n)   O(log n)      no       fastest
 merge sort      O(n log n)    O(n log n)   O(n)          yes      predictable
 HEAPSORT        O(n log n)    O(n log n)   O(1)          no       ~2-3x slower
                                                                    than quicksort
```

**Heapsort is the only one with both a guaranteed `O(n log n)` and `O(1)` extra space**, and it still
loses in practice by a factor of two or three because of cache behaviour: sift-down jumps to `2i+1` then
`4i+3` then `8i+7`, striding further each level, while quicksort scans contiguously.

**That comparison is the answer to "why does nobody use heapsort?"** — and it is a good example of an
algorithm that is theoretically superior and practically worse.

### Where the work actually is

```
 building a heap of 1,000,000 items
   bottom-up heapify      ~1,000,000 swaps      O(n)
   n pushes               ~4,000,000 swaps      O(n log n)

 then extracting all of them
   1,000,000 pops × ~20 levels  =  ~20,000,000 swaps
```

**Extraction dominates by a factor of twenty.** So if you only need the smallest few, `heapify` plus a few
pops is enormously cheaper than sorting — and that is exactly the
[top-k](../day-116-top-k/README.md) argument.

---

## 7. The traps

### Trap 1 — starting heapify at the wrong index

```python
    for i in range(len(data) - 1, -1, -1):      # from the LAST element
```

Correct, and it does needless work: every index from `n//2` onwards is a leaf and `sift_down` returns
immediately. Not a bug, but **half the calls are wasted**, and starting at `n//2 − 1` is the version that
shows you know why.

```python
    for i in range(len(data) // 2):             # FORWARDS — actually WRONG
```

Going forwards breaks the precondition: sifting down a node requires its subtrees to already be heaps.
**The result is not a heap, and `is_heap` returns False with no error raised.**

### Trap 2 — sifting down against the wrong child

```python
        if data[left] < data[i]:
            swap with left                  # even when right is smaller
```

The new parent is now greater than its right child. **The property is violated and nothing raises** — pops
return values in the wrong order, quietly.

**Compare with both, swap with the smaller.**

### Trap 3 — the bounds check inside sift down

```python
        if data[left] < data[smallest]:     # missing `left < n`
```

```
 IndexError: list index out of range
```

Every access to `2i+1` and `2i+2` needs a bounds check, because most nodes are leaves and have neither.

### Trap 4 — popping without preserving completeness

```python
        return data.pop(0)                  # removes the root by shifting
```

Two problems. `list.pop(0)` is `O(n)` because everything shifts. And shifting the array is **not** the
same as removing the root from the tree — the resulting array is not a valid heap, and every relationship
is off by one position.

### Trap 5 — the single-element pop

```python
        smallest = data[0]
        last = data.pop()
        data[0] = last                      # IndexError when the heap had one element
```

After popping the only element the list is empty, so assigning to index 0 raises. The check
`if data:` after the pop is not optional.

### Trap 6 — building by pushing when you have all the items

```python
    for v in items:
        heapq.heappush(h, v)                # O(n log n)
```

Correct, and four times slower than `heapq.heapify(items)` at a million items. **If you have all the items
in advance, heapify.** This is the most common practical inefficiency in this topic.

### Trap 7 — assuming sift up and sift down are interchangeable

They are not. **Insert must sift up** (the new value is at a leaf and may be too small) and **extract must
sift down** (the moved value is at the root and may be too large). Using the wrong one leaves the heap
broken in a way that only shows up several operations later.

### Trap 8 — mutating a value in place and expecting the heap to notice

```python
    h[3] = 0                                # the invariant is now broken
```

Nothing re-establishes the property. You must call `sift_up` or `sift_down` on that index — and since you
usually do not know the index, this is why **indexed heaps** or **lazy deletion** exist.

---

## 8. In the interview

### How it gets asked

- The mechanical one: *"Insert into the heap. Now remove the minimum."* — often on a whiteboard, by hand.
- The follow-up that decides it: *"Why is building a heap `O(n)` and not `O(n log n)`?"*
- The design probe: *"Why does the last element move to the root?"*
- The sorting one: *"Implement heapsort. Why does nobody use it?"*
- The mutation one: *"How would you change the priority of something already in the heap?"*

### What to say out loud, in the first ninety seconds

1. **Say what both operations share.** "Both move one value along a single root-to-leaf path, swapping as
   they go. Nothing off that path is touched, which is why both are `O(log n)`."
2. **Insert: append, then sift up — and say why append.** "The new value goes at the end, because that is
   the only position that keeps the tree complete. Then it rises while it is smaller than its parent."
3. **Extract: last to the root, then sift down — and say why the last.** "I take index 0 as the answer,
   then move the **last** element to the root. It has to be the last one: any other removal leaves a hole
   the array cannot represent."
4. **Say the smaller-child rule explicitly.** "Sifting down compares with both children and swaps with the
   **smaller** — swapping with the larger leaves the property broken, silently."
5. **Volunteer the `O(n)` fact.** "And building a heap from an array is `O(n)`, not `O(n log n)`, which
   surprises people."
6. **Have the argument ready.** "Half the nodes are leaves and do no work. A quarter can sink one level, an
   eighth two. The nodes that could travel far are the rare ones near the root — the sum converges to about
   two swaps per node."

### The follow-ups

**"Why is heapify `O(n)`?"**
"Because the work is concentrated where the nodes are not. Bottom-up heapify sifts each node **down**, and
a node at depth `d` can sink at most `height − d` levels — so the nodes that could travel far are the ones
near the root, and there are almost none of them. Meanwhile half of all nodes are **leaves**, which do zero
work; a quarter are one level up and can sink at most one; an eighth at most two. Summing gives
`n × Σ k/2^k`, and that series converges to 2 — about two swaps per node, so `O(n)`. The other half of the
answer is the asymmetry: doing it **top-down** with sift-**up**, which is what `n` pushes does, is genuinely
`O(n log n)`, because then the many nodes at the bottom are exactly the ones that can travel the full
height. Same structure, same final heap, different cost — and the difference is entirely about where the
nodes are relative to how far they can move."

**"Why does the last element move to the root?"**
"Because it is the only removal that keeps the tree **complete**, and completeness is what makes the array
representation work. If I simply deleted index 0 I would have a hole at the root, and an array has no way
to represent a hole. If I promoted the smaller child instead, I would move the hole one level down and have
exactly the same problem recursively, and the tree would no longer be complete because the gap would be in
the middle rather than at the end. Taking the last element is the one removal that shortens the array by
one without disturbing any other position. It then sits at the root where it is almost certainly far too
big, so it sinks — at most `height` swaps."

**"Implement heapsort. Why does nobody use it?"**
"Build a max-heap over the whole array in `O(n)`, then repeatedly swap the root with the last element of
the heap region and shrink that region by one, sifting the new root down. The array fills from the right
with the sorted values, in place. `O(n log n)` in the **worst case** and `O(1)` extra space — and it is the
only common sort with both of those properties, since merge sort needs `O(n)` extra and quicksort degrades
to `O(n²)`. Nobody uses it because of **cache behaviour**: sift-down jumps from `i` to `2i+1` to `4i+3`,
striding further at every level and touching memory all over the array, while quicksort scans contiguous
ranges and the prefetcher keeps up. In practice heapsort is two to three times slower than a good
quicksort, which makes it a nice example of an algorithm that is theoretically superior and practically
worse. Where it does get used is as the **fallback** in introsort — quicksort switches to heapsort when the
recursion gets too deep, which caps the worst case without paying heapsort's constants in the normal
case."

**"How would you change the priority of an element already in the heap?"**
"Two parts, and the second is the problem. If the value **decreased**, sift it **up**; if it **increased**,
sift it **down**. Both are `O(log n)` — **once you know the index**. Finding the index is `O(n)`, because a
heap cannot search. So a real implementation that needs decrease-key, like Dijkstra's algorithm, uses an
**indexed heap**: the heap plus a hash map from element to its current index, with the map updated on every
swap. That makes decrease-key `O(log n)` at the cost of maintaining the map. Python has no such thing, so
the idiomatic answer here is **lazy deletion**: push a new entry with the new priority, leave the old one in
place, and skip stale entries as they surface — which costs extra memory and a check on every pop, and is
what a Python Dijkstra actually does."

**"You have a million items. How do you build the heap?"**
"`heapify`, not a million pushes. Heapify is `O(n)` — about a million swaps — and pushing one at a time is
`O(n log n)`, about four million, so roughly four times the work for exactly the same result. It is the
most common practical inefficiency in this topic, and the fix is one line. Worth adding: if I then extract
everything, the extraction dominates completely — a million pops at about twenty levels each is twenty
million swaps, twenty times the build. Which is why, if I only need the smallest few, heapify plus a handful
of pops is dramatically cheaper than sorting, and that is exactly the top-k argument."

**"Walk me through inserting 0 into this heap, by hand."**
"I append it at the end of the array, which keeps the tree complete. Then it is at the deepest level and
almost certainly too small for its position, so it rises: compare with its parent at `(i−1)//2`; if it is
smaller, swap and repeat. On this heap: 0 against 7, swap; 0 against 3, swap; 0 against 1, swap; now it is
at the root and the loop ends. Three swaps, and the heap is valid again — I can check it by confirming
every node is at most its two children. The bound is the height, so `log n`, but in practice most insertions
rise only a level or two, because a random new value is usually not near the minimum."

### A model answer

Asked: *insert into the heap, then remove the minimum — and why is heapify `O(n)`?*

> "Both operations do the same thing structurally: a value ends up in the wrong place, and it **swaps its
> way along one root-to-leaf path** until the property holds. Nothing off that path is touched, so both are
> `O(log n)`.
>
> **Insert** appends the value at the **end** of the array and sifts it **up**. Appending is not a
> convenience — the end is the only position that keeps the tree **complete**, and completeness is what lets
> the whole thing live in an array. Then the new value compares with its parent at `(i−1)//2`, swaps if it
> is smaller, and repeats until it is not, or until it reaches the root. One comparison per level, because a
> node has only one parent.
>
> **Extract** takes index 0 as the answer, then moves the **last** element to the root and sifts it
> **down**. It must be the last element: deleting index 0 leaves a hole at the root that an array cannot
> represent, and promoting a child just moves the hole one level down, recursively. Sifting down compares
> with **both** children and swaps with the **smaller** one — that detail matters, because swapping with
> the larger child leaves the new parent greater than its other child and the property is still broken with
> nothing raised.
>
> Now the `O(n)` question, because it does look wrong. Building a heap bottom-up means sifting each node
> **down**, starting from the last node that has a child — index `n//2 − 1` — and working backwards.
> Backwards because sifting a node down requires its subtrees to already be heaps.
>
> The reason it is linear is **where the nodes are relative to how far they can move**. A node at depth `d`
> can sink at most `height − d` levels. Half of all nodes are **leaves** and sink zero. A quarter are one
> level up and sink at most one. An eighth at most two. The nodes that could travel the full height are the
> handful near the root. So the total is a sum of `(n / 2^(d+1)) × (h − d)`, which reduces to `n × Σ k/2^k`,
> and that series converges to **2** — about two swaps per node.
>
> The clinching part is the asymmetry: doing the same job **top-down**, by pushing `n` items and sifting
> **up**, really is `O(n log n)`. In that direction, the many nodes at the bottom are exactly the ones that
> can travel the full height. Same values, same final heap, different cost — measured at a million items it
> is about a million swaps against four million.
>
> Which has a practical consequence worth stating: if you have all the items in advance, call `heapify`
> rather than pushing them one at a time. And if you then need only the smallest few, heapify plus a few
> pops is far cheaper than sorting — a million pops would be twenty million swaps, twenty times the cost of
> building it."

---

## 9. Recall card

- **Both operations move ONE value along ONE root-to-leaf path — `O(log n)`.** Sift **up** compares with
  the single parent (one comparison per level); sift **down** compares with both children and must swap
  with **the smaller** — swapping with the larger leaves the property broken, silently.
- **Insert APPENDS then sifts up; extract moves the LAST element to the root then sifts down.** Both are
  forced by completeness: the end is the only position you can add to or remove from without leaving a hole
  the array cannot represent.
- **Heapify is `O(n)`, not `O(n log n)`.** Start at the **last parent** (`n//2 − 1`) and go **backwards**
  (a node's subtrees must already be heaps). **Half the nodes are leaves and do zero work**; a quarter sink
  ≤ 1; the far travellers are the rare ones at the top. `Σ (n/2^(d+1))(h−d) = n·Σ k/2^k = 2n`.
- **The asymmetry is the clincher: top-down with sift-UP (n pushes) really is `O(n log n)`**, because then
  the many bottom nodes can travel the full height. Measured at n = 1,000,000: **~1M swaps against ~4M.**
  **If you have all the items, `heapify` — never `n` pushes.**
- **Heapsort is `O(n log n)` worst case with `O(1)` extra space — the only common sort with both — and
  still 2–3× slower than quicksort** because sift-down strides `2i+1`, `4i+3`, `8i+7` and destroys cache
  locality. **Changing a priority is `O(log n)` only once you know the index** (decrease → sift up,
  increase → sift down); finding it is `O(n)`, hence **indexed heaps** or **lazy deletion**.
