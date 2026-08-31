---
day: 118
track: dsa
title: "Two heaps: the running median"
phase: "Heaps and priority queues"
status: written
---

# Day 118 · DSA — Two heaps: the running median

**After today you can:** You can keep a stream balanced across two heaps and read the median in O(1).

**The interviewer asks it as:** *Find the median of a stream of numbers.*

---

## 1. What this is, and why they ask it

Numbers arrive one at a time and after each one you must be able to say the **median** — the middle value
if the numbers were sorted.

Three sentences. Sorting after every arrival is `O(n log n)` per query and hopeless; the trick is to keep
the numbers **already split into a lower half and an upper half**, so the median is at the boundary and
costs nothing to read. Each half is a heap, and they face each other: a **max-heap** holding the lower
half so its largest is at the top, and a **min-heap** holding the upper half so its smallest is at the top
— **the two elements at the boundary are exactly the ones you need.** And the only real work is keeping
the two halves the same size, which is two lines and is where every bug in this problem lives.

They ask it because it is the clearest example of a technique that is otherwise hard to motivate:
**maintain an invariant incrementally rather than recomputing an answer.** It is also the shape of a small
family — the sliding-window median, scheduling problems, "IPO"-style greedy selection — where two heaps
facing each other answer a question neither could answer alone.

---

## 2. The story

Mrs Kurian took the fourth standard for PT and every year in November there was a photograph, and every
year she needed the children in two lines of equal length, shorter children in one and taller in the
other.

The complication was that they never all arrived at once. They came out of the classroom in ones and twos
over about ten minutes, and the boy at the front of each line kept changing.

The way she had done it in her first year was to line everybody up in full height order and then cut the
line in half. That worked and it meant re-sorting forty children every time one more came out of the door.

By her third year she did something else.

She kept **two lines from the start**. Left line for the shorter half, right line for the taller half. And
she kept each line arranged so that the child nearest her was the extreme one — in the left line, the
**tallest** of the short children stood at the front; in the right line, the **shortest** of the tall
children stood at the front.

So the two children standing in front of her, one from each line, were always the two in the middle of the
whole class.

When a new child came out, she did two things and never more.

She looked at the child against the front of the left line. Shorter or equal — join the left line. Taller —
join the right line. Either way the child worked their way to the correct position within their own line,
which took a few steps, not forty.

Then she counted. If one line was now two longer than the other, she took the front child of the longer
line and moved them to the front of the shorter one. One child, every time, never two.

Her student teacher that year asked what happened if a child joined the left line but was actually taller
than half the right line.

Mrs Kurian said it could not happen, because she had checked against the front of the left line first —
and the front of the left line is the tallest short child. Anybody shorter than him belongs on the left.
The check is against the boundary, not against the whole line.

And she said the counting was the part people got wrong. If you do not move a child across, the lines drift
apart, and after twenty children one line has fifteen and the other has five, and the two children in front
of you are not the middle of anything.

---

## 3. The idea in plain English

Mrs Kurian's two lines are two heaps facing each other, and both of her rules — check against the
boundary, then rebalance by one — are the algorithm.

- The left line is a **max-heap** of the lower half: its **largest** is at the top.
- The right line is a **min-heap** of the upper half: its **smallest** is at the top.
- The two children in front of her are the two middle values, so the **median is at the boundary**.
- "Check against the front of the left line" is the routing rule.
- "Move one child across" is the **rebalance**, and it is exactly one move.

### The two invariants

Everything follows from these, and stating them is most of the answer.

```
 1. ORDER    every value in the low heap  ≤  every value in the high heap
 2. BALANCE  the two sizes differ by at most 1
```

**Given both, the median is free:**

```
 odd total   -> the larger heap's top
 even total  -> the average of the two tops
```

**`O(1)`.** No sorting, no scanning — the answer is sitting at the boundary because the invariants put it
there.

### The insert, in three steps

```python
    heapq.heappush(low, -value)                         # 1. always push here
    heapq.heappush(high, -heapq.heappop(low))           # 2. move the top across
    if len(high) > len(low):                            # 3. rebalance if needed
        heapq.heappush(low, -heapq.heappop(high))
```

**Three lines, and they are worth reading carefully because they look strange.**

**Step 1 — push into `low` unconditionally.** Not "compare and choose". Pushing to `low` regardless is
correct because step 2 fixes it.

**Step 2 — move `low`'s top to `high`.** This is what guarantees invariant 1. Whatever the new value was,
after this move the largest thing in `low` is genuinely ≤ the smallest thing in `high`, because the largest
candidate was just handed over.

**Step 3 — restore the balance.** After steps 1 and 2, `low` has lost one and `high` has gained one, so
`high` may now be one too big. One move back fixes it.

**This "push, shift, rebalance" form is worth memorising as a unit** — it avoids all the branching of the
version that compares first, and there is no case analysis to get wrong.

**The alternative version** compares first:

```python
    if not low or value <= -low[0]:
        heapq.heappush(low, -value)
    else:
        heapq.heappush(high, value)
    # then rebalance whichever side is too big
```

Both are correct. **The first is shorter and has no branches; the second is easier to explain.** Say which
one you are writing and why.

### The max-heap, which Python does not have

From [day 115](../day-115-heapq/README.md): `heapq` is min-only, so the lower half is stored **negated**.

```python
    heapq.heappush(low, -value)             # store the negation
    -low[0]                                 # read back with another negation
```

**Every value that goes into `low` is negated, and every value that comes out is negated again.** Getting
one of the two negations wrong is the single most common bug here, and it produces a plausible-looking
median that is quietly wrong.

**Say the convention out loud as you write it**: *"`low` holds negated values, so `-low[0]` is the largest
number in the lower half."*

### Reading the median

```python
    if len(low) > len(high):
        return -low[0]                      # odd count: the extra one is in low
    return (-low[0] + high[0]) / 2          # even count: average the two tops
```

**Two conventions exist for where the extra element goes when the count is odd** — `low` or `high` — and
either is fine as long as the median function agrees with the rebalance rule. **Pick one and be
consistent**; mixing them gives an answer that is right for even counts and wrong for odd ones.

### Why not the obvious alternatives

```
 sort after every insert          O(n log n) per query    ->  O(n^2 log n) overall
 keep a sorted list, insert with
   bisect                         O(log n) to FIND, O(n) to SHIFT
                                  -> O(n) per insert
 a balanced BST with subtree
   sizes                          O(log n) insert AND O(log n) k-th
                                  -> more general, much more code
 TWO HEAPS                        O(log n) insert, O(1) median
```

**The sorted-list version is the one worth discussing**, because it is what people reach for and it is
`O(n)` per insert: `bisect` finds the position in `O(log n)` and then `list.insert` shifts everything after
it.

```
 n = 100,000 insertions
   sorted list:  ~2,500,000,000 element moves
   two heaps:    ~1,700,000 comparisons
```

**And the BST answer is worth naming**: an order-statistic tree gives you the k-th element for any `k`, not
just the middle. **Two heaps are better when you only ever want the median**, because they are twenty lines
rather than two hundred.

### The variants

**Sliding-window median** — LeetCode 480. The same two heaps, plus **removal**, which a heap cannot do.
The standard answer is **lazy deletion** from [day 115](../day-115-heapq/README.md): keep a dictionary of
values scheduled for removal, and discard them when they surface at a top.

**The catch is the size accounting.** Lazily deleted elements are still physically in the heaps, so you
must track the **logical** sizes separately from `len(heap)` — and that is where the bugs are.

**Any percentile, not just the median.** Change the balance rule: to track the 90th percentile, keep the
heaps at a 9:1 ratio instead of 1:1. **Same structure, one different comparison.**

**"IPO" / maximise capital** — LeetCode 502. A min-heap of projects by cost and a max-heap of affordable
projects by profit: move everything affordable from the first to the second, then take the best. **Two
heaps facing each other again, with a different question.**

**Meeting rooms II, task scheduling** — a heap of end times against a stream of start times, which is the
same "one heap holds candidates, another holds committed" shape.

**The unifying idea worth stating**: *two heaps facing each other let you maintain a **boundary** in a
changing set — and the boundary is the answer.*

---

## 4. The picture

The two lines, which is the data structure.

```
              Mrs Kurian
                  │
      LEFT LINE   │   RIGHT LINE
   (shorter half) │  (taller half)
                  │
   ... 118 120 [124]  [126] 129 133 ...
                  ▲    ▲
        TALLEST short  SHORTEST tall
        = max-heap top = min-heap top

 THE TWO CHILDREN IN FRONT OF HER ARE THE TWO MIDDLE VALUES.

 odd total   -> the front of whichever line is longer
 even total  -> the average of the two fronts

 O(1). The invariants put the answer at the boundary.
```

The two heaps, drawn as heaps:

```
 LOW  — a MAX-heap (stored negated in Python)     HIGH — a MIN-heap

           124                                            126
          /   \                                          /   \
        120    118                                    129     133
        / \                                           /
      115  119                                      141

 top = 124  (the LARGEST of the lower half)      top = 126 (the SMALLEST
                                                        of the upper half)

 INVARIANT 1:  everything in LOW  ≤  everything in HIGH
 INVARIANT 2:  |len(LOW) − len(HIGH)| ≤ 1

 median (7 values, odd)  ->  124, the top of the larger heap
 median (8 values, even) ->  (124 + 126) / 2
```

The insert, step by step:

```
 inserting 122 into  LOW={115,118,119,120,124}  HIGH={126,129,133}

 STEP 1  push into LOW unconditionally
         LOW = {115,118,119,120,122,124}   top = 124
         HIGH = {126,129,133}
         -> sizes 6 and 3. Unbalanced, and that is fine for now.

 STEP 2  move LOW's top to HIGH
         LOW = {115,118,119,120,122}       top = 122
         HIGH = {124,126,129,133}          top = 124
         -> INVARIANT 1 is now guaranteed: the largest candidate was
            handed over, so max(LOW) ≤ min(HIGH)

 STEP 3  rebalance if HIGH is bigger
         sizes 5 and 4  ->  no move needed

 median -> LOW is larger, so -low[0] = 122

 WHY PUSH TO LOW BLINDLY? Because step 2 repairs it. There is no case
 analysis and no branch to get wrong.
```

Why the rebalance is not optional:

```
 WITHOUT step 3, inserting an increasing sequence:

 after 1:  LOW={1}          HIGH={}
 after 2:  LOW={1}          HIGH={2}
 after 3:  LOW={1}          HIGH={2,3}
 after 4:  LOW={1}          HIGH={2,3,4}
 after 5:  LOW={1}          HIGH={2,3,4,5}
                  ▲               ▲
           the "median" reads as 1 or (1+2)/2 — and the real median is 3

 the boundary has DRIFTED away from the middle.
 Mrs Kurian: "after twenty children one line has fifteen and the other five,
 and the two children in front of you are not the middle of anything."
```

The negation, which is where the bugs are:

```
 Python has no max-heap, so LOW stores NEGATED values.

 push:  heappush(low, -value)          store the negation
 peek:  -low[0]                        negate again to read it
 move:  heappush(high, -heappop(low))  ONE negation, because it is
                                        leaving the negated heap

 TWO negations on the way in and out; ONE when moving across.
 Get any of them wrong and you get a plausible number that is WRONG.
```

The family, all the same shape:

```
 RUNNING MEDIAN       LOW: max-heap of the small half
                      HIGH: min-heap of the large half
                      -> the boundary IS the answer

 SLIDING WINDOW       the same, plus LAZY DELETION for elements leaving
   MEDIAN             the window — and LOGICAL sizes tracked separately
                      from len(heap)

 ANY PERCENTILE       the same, with the balance ratio changed
                      (9:1 instead of 1:1 for the 90th)

 IPO / MAX CAPITAL    LOW: min-heap of projects by COST
                      HIGH: max-heap of affordable projects by PROFIT
                      -> move everything affordable across, then take the best

 THE UNIFYING IDEA: two heaps facing each other maintain a BOUNDARY in a
 changing set, and the boundary is what you were asked for.
```

---

## 5. The code, built step by step

### Step 1 — state both invariants before writing anything

"I keep the numbers split into a lower half and an upper half. Two invariants: everything in the low half
is at most everything in the high half, and their sizes differ by at most one. Given those, the median is
at the boundary and costs nothing to read."

### Step 2 — say which heap is which, and why

"The **low** half is a **max**-heap, so its largest — the biggest of the small numbers — is at the top. The
**high** half is a **min**-heap, so its smallest is at the top. Those two are exactly the middle values."

### Step 3 — the negation convention, said out loud

```python
    heapq.heappush(low, -value)
```

"Python's `heapq` is min-only, so the low heap stores negated values. `-low[0]` is the largest number in
the lower half. Two negations in and out; that is where the bugs are."

### Step 4 — push, shift, rebalance — as one unit

```python
        heapq.heappush(low, -value)
        heapq.heappush(high, -heapq.heappop(low))
        if len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
```

"Push into low unconditionally, move low's top across — which is what guarantees the ordering — then move
one back if high has become too big. Three lines, no branches, no case analysis."

### Step 5 — the median, matching the convention

```python
        if len(low) > len(high):
            return float(-low[0])
        return (-low[0] + high[0]) / 2
```

"The rebalance rule lets `low` be one larger, so on an odd count the extra element is in `low` and that is
the median. The median function has to agree with the rebalance rule — if they disagree you get the right
answer for even counts and the wrong one for odd."

### The complete solution

```python
import heapq
from collections import defaultdict


class MedianFinder:
    """LeetCode 295. The running median in O(log n) insert, O(1) query.

    TWO INVARIANTS, and everything follows from them:
      1. ORDER    every value in `low` <= every value in `high`
      2. BALANCE  |len(low) - len(high)| <= 1, with `low` allowed to be
                  the larger one

    `low`  is a MAX-heap of the smaller half  (negated, since heapq is min-only)
    `high` is a MIN-heap of the larger half

    So the two heap tops are the two middle values, and the median is free.
    """

    def __init__(self) -> None:
        self.low: list[int] = []            # max-heap, values stored NEGATED
        self.high: list[int] = []           # min-heap, values stored as-is

    def add(self, value: int) -> None:
        """PUSH, SHIFT, REBALANCE — three lines, no branches.

        Pushing into `low` unconditionally is safe because the shift repairs
        it: whatever the new value was, moving low's top to high guarantees
        max(low) <= min(high), because the largest candidate was just handed
        over.
        """
        heapq.heappush(self.low, -value)                        # 1. push
        heapq.heappush(self.high, -heapq.heappop(self.low))     # 2. shift
        if len(self.high) > len(self.low):                      # 3. rebalance
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        """O(1). The invariants have already put the answer at the boundary.

        This MUST agree with the rebalance rule about which heap holds the
        extra element on an odd count — here, `low`.
        """
        if not self.low:
            raise ValueError("no values yet")
        if len(self.low) > len(self.high):
            return float(-self.low[0])                  # odd: the extra is in low
        return (-self.low[0] + self.high[0]) / 2        # even: average the tops

    def __len__(self) -> int:
        return len(self.low) + len(self.high)

    def check_invariants(self) -> bool:
        """Assert both invariants directly — run this in tests, because every
        bug in this problem breaks one of them silently."""
        if abs(len(self.low) - len(self.high)) > 1:
            return False
        if self.low and self.high and -self.low[0] > self.high[0]:
            return False
        return True


class MedianFinderBranching:
    """The same thing, written with an explicit comparison instead of the
    shift. Correct, easier to explain, more branches to get wrong.

    Say which version you are writing and why."""

    def __init__(self) -> None:
        self.low: list[int] = []
        self.high: list[int] = []

    def add(self, value: int) -> None:
        if not self.low or value <= -self.low[0]:
            heapq.heappush(self.low, -value)
        else:
            heapq.heappush(self.high, value)

        # rebalance: low may be at most one larger
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        elif len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


class PercentileTracker:
    """The generalisation: change the BALANCE RATIO and you track any
    percentile, not just the median.

    p = 0.5 -> the median (1:1).  p = 0.9 -> the 90th percentile (9:1).
    Same structure, one different comparison.
    """

    def __init__(self, p: float = 0.5) -> None:
        self.p = p
        self.low: list[int] = []            # max-heap, negated
        self.high: list[int] = []           # min-heap

    def add(self, value: int) -> None:
        heapq.heappush(self.low, -value)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # low should hold about p of the total
        total = len(self.low) + len(self.high)
        want_low = max(1, round(self.p * total))
        while len(self.low) < want_low:
            heapq.heappush(self.low, -heapq.heappop(self.high))
        while len(self.low) > want_low:
            heapq.heappush(self.high, -heapq.heappop(self.low))

    def value(self) -> float:
        return float(-self.low[0])


class SlidingWindowMedian:
    """LeetCode 480. Two heaps plus LAZY DELETION, because a heap cannot
    remove an arbitrary element.

    THE HARD PART is the size accounting: lazily removed elements are still
    physically in the heaps, so the LOGICAL sizes must be tracked separately
    from len(heap). Every bug in this problem is there.
    """

    def __init__(self) -> None:
        self.low: list[int] = []            # max-heap, negated
        self.high: list[int] = []           # min-heap
        self.pending: dict[int, int] = defaultdict(int)     # value -> count to drop
        self.low_size = 0                   # LOGICAL sizes
        self.high_size = 0

    def _prune(self, heap: list[int], is_low: bool) -> None:
        """Discard scheduled-for-removal values sitting at the top."""
        while heap:
            value = -heap[0] if is_low else heap[0]
            if self.pending[value] > 0:
                self.pending[value] -= 1
                heapq.heappop(heap)
            else:
                break

    def _rebalance(self) -> None:
        if self.low_size > self.high_size + 1:
            self._prune(self.low, True)
            heapq.heappush(self.high, -heapq.heappop(self.low))
            self.low_size -= 1
            self.high_size += 1
        elif self.low_size < self.high_size:
            self._prune(self.high, False)
            heapq.heappush(self.low, -heapq.heappop(self.high))
            self.high_size -= 1
            self.low_size += 1
        self._prune(self.low, True)
        self._prune(self.high, False)

    def add(self, value: int) -> None:
        if not self.low or value <= -self.low[0]:
            heapq.heappush(self.low, -value)
            self.low_size += 1
        else:
            heapq.heappush(self.high, value)
            self.high_size += 1
        self._rebalance()

    def remove(self, value: int) -> None:
        self.pending[value] += 1            # LAZY: mark, do not search
        if self.low and value <= -self.low[0]:
            self.low_size -= 1
            if value == -self.low[0]:
                self._prune(self.low, True)
        else:
            self.high_size -= 1
            if self.high and value == self.high[0]:
                self._prune(self.high, False)
        self._rebalance()

    def median(self) -> float:
        if self.low_size > self.high_size:
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


def median_sliding_window(nums: list[int], k: int) -> list[float]:
    """The window walked across the array."""
    window = SlidingWindowMedian()
    out: list[float] = []
    for i, value in enumerate(nums):
        window.add(value)
        if i >= k:
            window.remove(nums[i - k])
        if i >= k - 1:
            out.append(window.median())
    return out


def find_maximized_capital(k: int, capital: int,
                           profits: list[int], costs: list[int]) -> int:
    """LeetCode 502 — two heaps facing each other with a DIFFERENT question.

    LOW:  a min-heap of projects by COST      (what might become affordable)
    HIGH: a max-heap of affordable projects by PROFIT   (what to do next)

    Each round: move everything now affordable from LOW to HIGH, then take
    HIGH's best. Same structure, different boundary.
    """
    by_cost = list(zip(costs, profits))
    heapq.heapify(by_cost)                  # min-heap on cost
    affordable: list[int] = []              # max-heap on profit (negated)

    for _ in range(k):
        while by_cost and by_cost[0][0] <= capital:
            cost, profit = heapq.heappop(by_cost)
            heapq.heappush(affordable, -profit)
        if not affordable:
            break
        capital += -heapq.heappop(affordable)
    return capital


class MedianBySortedList:
    """The alternative people reach for. O(log n) to FIND the position and
    O(n) to SHIFT — so O(n) per insert.

    n = 100,000 insertions: ~2.5 billion element moves against ~1.7 million
    heap comparisons.
    """

    def __init__(self) -> None:
        self.data: list[int] = []

    def add(self, value: int) -> None:
        import bisect
        bisect.insort(self.data, value)     # O(log n) find, O(n) shift

    def median(self) -> float:
        n = len(self.data)
        if n % 2:
            return float(self.data[n // 2])
        return (self.data[n // 2 - 1] + self.data[n // 2]) / 2


if __name__ == "__main__":
    mf = MedianFinder()
    for v in (5, 15, 1, 3):
        mf.add(v)
        print(f"add {v:>3} -> median {mf.median():>6.1f}  "
              f"low={sorted(-x for x in mf.low)} high={sorted(mf.high)}  "
              f"ok={mf.check_invariants()}")
    # add   5 -> median    5.0
    # add  15 -> median   10.0
    # add   1 -> median    5.0
    # add   3 -> median    4.0

    # both versions agree
    a, b = MedianFinder(), MedianFinderBranching()
    import random
    random.seed(0)
    for _ in range(1000):
        v = random.randint(-1000, 1000)
        a.add(v); b.add(v)
        assert abs(a.median() - b.median()) < 1e-9
    print("both versions agree over 1,000 insertions")

    # and against the honest reference
    ref = MedianBySortedList()
    c = MedianFinder()
    for _ in range(1000):
        v = random.randint(-1000, 1000)
        ref.add(v); c.add(v)
        assert abs(ref.median() - c.median()) < 1e-9
    print("matches a sorted-list reference over 1,000 insertions")

    # WHY THE REBALANCE MATTERS — an increasing sequence is the worst case
    drift = MedianFinder()
    for v in range(1, 8):
        drift.add(v)
    print(drift.median(), drift.check_invariants())     # 4.0 True

    # the variants
    print(median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
    # [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]

    p90 = PercentileTracker(0.9)
    for v in range(1, 101):
        p90.add(v)
    print(p90.value())                      # ~90

    print(find_maximized_capital(2, 0, [1, 2, 3], [0, 1, 1]))       # 4

    # edge cases
    single = MedianFinder(); single.add(7)
    print(single.median())                  # 7.0
    two = MedianFinder(); two.add(1); two.add(2)
    print(two.median())                     # 1.5
    dup = MedianFinder()
    for v in (5, 5, 5, 5):
        dup.add(v)
    print(dup.median())                     # 5.0
```

---

## 6. What it costs

### The operations

```
 add       O(log n)   at most three heap operations, each O(log n)
 median    O(1)       both answers are at the tops
 space     O(n)       every value is stored once, in one heap or the other
```

**The `O(1)` median is the point.** Everything else about the design exists to make that line free.

### Against the alternatives

```
 approach                    insert        median      space
 -------------------------   -----------   ---------   -----
 sort on every query         O(1)          O(n log n)  O(n)
 sorted list (bisect.insort) O(n)          O(1)        O(n)
 order-statistic BST         O(log n)      O(log n)    O(n)
 TWO HEAPS                   O(log n)      O(1)        O(n)
```

```
 n = 100,000 insertions

 sorted list   O(n) per insert  ->  ~2,500,000,000 element moves
 two heaps     O(log n)         ->  ~1,700,000 comparisons
                                    ~1,500x fewer operations
```

**The sorted-list version is the honest competitor** and it is `O(n)` per insert because `list.insert`
shifts. It is genuinely faster for small `n`, because the shift is a memory move in C while a heap
operation is interpreted Python — **the crossover is around a few thousand elements**, which is worth
knowing rather than claiming the heap always wins.

**And the order-statistic BST is the more general answer**: it gives the k-th element for any `k`, not just
the middle, at the cost of `O(log n)` for the query instead of `O(1)` and roughly ten times the code.

### The constant factor

```
 each add: 1 push + 1 pop + 1 push  (+1 pop +1 push if rebalancing)
        =  3 to 5 heap operations, each O(log n)
```

**The push-shift-rebalance form always does at least three operations**, where the branching version often
does one. On random data the branching version is measurably faster; the shift version is shorter and has
no case analysis. **Say which trade you are making.**

### The sliding window

```
 window size k, array length n

 add + remove per step   O(log k)
 total                   O(n log k)
 space                   O(k) live values, plus lazily deleted ones
```

**The lazy deletion cost is the subtlety**: removed elements stay in the heaps until they reach a top, so
the heaps can grow to `O(n)` in the worst case even though only `k` values are logically present.

**The mitigation** is that a removed element is pruned as soon as it surfaces, so in practice the heaps
stay near `O(k)` — but the worst case is real and worth stating.

### Where the median problem gets harder

```
 running median, insert only        two heaps.  O(log n) / O(1).
 sliding window median              two heaps + lazy deletion.  O(log k).
 median with arbitrary deletion     two heaps + lazy deletion + an index
                                    -> or just use an order-statistic tree
 any percentile                     change the balance ratio
 approximate percentiles at scale   t-digest or HdrHistogram, O(1) space
```

**That last row is the production answer** and worth naming: for monitoring — p50, p95, p99 over millions
of events — nobody keeps every value. **t-digest** and **HdrHistogram** give accurate percentiles in
bounded memory, which is what your metrics system is actually doing.

---

## 7. The traps

### Trap 1 — forgetting the rebalance

```python
        heapq.heappush(self.low, -value)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # missing step 3
```

On an increasing sequence, everything drifts into `high` and the "median" reads from a `low` that holds one
element.

```
 add 1..7 without rebalancing  ->  median reads as 1.0
 correct answer                ->  4.0
```

**No error, and the answer is plausible.** Mrs Kurian's fifteen-and-five.

### Trap 2 — a negation missing

```python
        return float(self.low[0])           # forgot to negate
```

`low` stores negated values, so this returns the negative of the median. **Two negations on the way in and
out, and one when moving across** — and the version that moves a value between heaps needs exactly one.

```python
        heapq.heappush(self.high, -heapq.heappop(self.low))      # correct
        heapq.heappush(self.high, heapq.heappop(self.low))       # WRONG: no negation
```

### Trap 3 — the median function disagreeing with the rebalance rule

```python
    # rebalance lets LOW be the larger one
    if len(self.high) > len(self.low): ...

    # but the median reads from HIGH on an odd count
    if len(self.high) > len(self.low):
        return float(self.high[0])
```

**Right for even counts, wrong for odd.** The two rules must agree about which heap holds the extra
element. Pick one convention and write both lines from it.

### Trap 4 — comparing against the wrong boundary

```python
        if value <= self.high[0]:           # comparing against HIGH's top
            heapq.heappush(self.low, -value)
```

In the branching version you must compare against **`low`'s top** — the largest of the small values.
Comparing against `high`'s top puts values in the wrong heap and breaks invariant 1.

**Mrs Kurian: "the check is against the boundary, not against the whole line" — and specifically against
the near end of the left line.**

### Trap 5 — an empty heap on the first insert

```python
        if value <= -self.low[0]:           # IndexError when low is empty
```

```
 IndexError: list index out of range
```

The branching version needs `if not self.low or ...`. **The push-shift-rebalance version has no such
problem**, which is one more argument for it.

### Trap 6 — integer division for the even case

```python
        return (-self.low[0] + self.high[0]) // 2       # floor division
```

The median of 1 and 2 is 1.5, not 1. **`/`, not `//`** — and returning `float` even for the odd case keeps
the type consistent.

### Trap 7 — the sliding window's size accounting

```python
        if self.low_size > self.high_size + 1:          # LOGICAL sizes
        if len(self.low) > len(self.high) + 1:          # PHYSICAL sizes — WRONG
```

Lazily deleted elements are still physically present, so `len(heap)` is not the logical size. **Every bug
in the sliding-window version is this**, and it produces a median that is correct most of the time.

### Trap 8 — assuming the heaps are sorted

```python
        print(self.low)                     # NOT the sorted lower half
```

A heap's array is not sorted — [day 113](../day-113-the-heap/README.md). Only the **tops** are meaningful,
which is exactly what the design relies on and exactly what makes it cheap.

---

## 8. In the interview

### How it gets asked

- The classic: *"Design a data structure that supports adding numbers and finding the median."* LeetCode
  295.
- The follow-up they always ask: *"What if all the numbers are in the range 0 to 100?"*
- The harder one: *"Now do it over a sliding window."* LeetCode 480.
- The generalisation: *"What if I wanted the 90th percentile instead?"*
- The comparison: *"Why not just keep a sorted list?"*

### What to say out loud, in the first ninety seconds

1. **State the shape before the structure.** "I keep the numbers split into a lower half and an upper half,
   so the median is at the boundary between them and costs nothing to read."
2. **Say which heap is which, and why.** "The lower half is a **max**-heap, so its largest is on top; the
   upper half is a **min**-heap, so its smallest is on top. Those two are the middle values."
3. **Give both invariants.** "Two invariants: everything in low is at most everything in high, and the
   sizes differ by at most one. Given those, the median is `O(1)`."
4. **Describe the insert as one unit.** "Push into low, move low's top to high — which is what guarantees
   the ordering — then move one back if high is now bigger. Three lines, no branches."
5. **Flag the negation.** "Python's `heapq` is min-only, so the low heap stores negated values — two
   negations in and out, and that is where the bugs are."
6. **Give both complexities.** "`O(log n)` to add, `O(1)` to read the median, `O(n)` space."

### The follow-ups

**"Why not just keep a sorted list?"**
"It is a fair alternative and it is `O(n)` per insert, which is the thing to say. `bisect` finds the
position in `O(log n)`, but `list.insert` then has to **shift** every element after it, so at a hundred
thousand insertions that is around two and a half billion element moves against about one and a half
million heap comparisons for the two-heap version. I would add one honest caveat: for small `n` the sorted
list is actually **faster**, because the shift is a `memmove` in C while a heap operation is interpreted
Python — the crossover is somewhere in the low thousands. So 'use two heaps' is the right answer at scale
and not automatically the right answer at every size. The other alternative worth naming is an
**order-statistic tree** — a balanced BST with subtree sizes — which gives the k-th element for **any** k
in `O(log n)`, not just the middle. Two heaps are better when the median is all you ever need, because
they are twenty lines rather than two hundred."

**"What if all the numbers are between 0 and 100?"**
"Then I would not use heaps at all — I would keep a **count array** of 101 buckets. Adding is `O(1)`: just
increment. Finding the median is a scan across at most 101 buckets accumulating counts until I pass half
the total, so it is `O(1)` in terms of `n` — the bucket count is a constant. That is better than
`O(log n)` insert and it is exact, not approximate. The general lesson is the same one as counting sort and
as the top-k bucket trick: **when the key space is small and bounded, bucketing beats every
comparison-based structure**. If the range were bounded but large — say a million — I would use a
**Fenwick tree** over the value range, which gives `O(log range)` insert and `O(log range)` for the k-th
element, and is what you actually want for a large bounded domain."

**"Now do it over a sliding window."**
"Same two heaps, plus the problem that a heap cannot remove an arbitrary element. So: **lazy deletion**.
When a value leaves the window I record it in a dictionary of pending removals rather than searching for
it, and I discard it when it surfaces at a heap top. The part that is genuinely fiddly, and where all the
bugs are, is that lazily deleted elements are **still physically in the heaps** — so I have to track the
**logical** sizes separately from `len(heap)`, and the rebalance must use the logical sizes. If you use
`len(heap)` there, you get a median that is correct most of the time and wrong occasionally, which is the
worst kind of bug. The complexity is `O(n log k)` overall, and the heaps stay near `O(k)` in practice
because removed elements get pruned as soon as they reach a top — though the worst case is `O(n)`."

**"What if I wanted the 90th percentile?"**
"Change the balance ratio and nothing else. The median keeps the heaps at one-to-one; for the 90th
percentile I keep them at nine-to-one, so that ninety percent of the values are in the low heap and the
answer is the top of the low heap. Same two heaps, same push-shift structure, one different comparison in
the rebalance. Worth adding what happens at real scale, though: for monitoring — p50, p95, p99 over
millions of events a minute — nobody stores every value, because that is `O(n)` memory forever. The
production answer is an approximate structure like **t-digest** or **HdrHistogram**, which give accurate
percentiles in bounded memory and are what your metrics system is doing under the hood. Two heaps are the
exact answer for a stream you can afford to keep."

**"Why push into the low heap unconditionally?"**
"Because the next line repairs it, and that removes all the case analysis. If I push into `low` and then
immediately move `low`'s top into `high`, then whatever the new value was, the largest candidate for the
lower half has just been handed over — so `max(low) <= min(high)` is guaranteed afterwards. Then I only
have to fix the sizes. The alternative is to compare the new value against `low`'s top and choose a heap,
which is also correct and is easier to explain, but it has two branches plus an empty-heap check on the
very first insert, and each of those is a chance to be wrong. I would write the three-line version and
mention that the branching one exists — and note that the branching one is measurably faster on random
data, because it usually does one heap operation rather than three."

**"How would you test it?"**
"Against an honest reference. I keep a sorted list alongside, insert into both, and assert the medians
agree after every single insertion over a few thousand random values — that catches the negation errors
and the odd/even convention mismatch immediately, which are otherwise plausible-looking wrong numbers. And
separately I assert the **invariants** directly after each add: the sizes differ by at most one, and
`max(low) <= min(high)`. Those two assertions catch every structural bug in this problem, and each of them
is one line. The specific cases I would include are a strictly increasing sequence — which is what a
missing rebalance breaks — a single element, exactly two elements, and all-duplicates."

### A model answer

Asked: *find the median of a stream of numbers.*

> "The naive approach is to sort after every insertion, which is `O(n log n)` per query. The idea that fixes
> it is to **keep the numbers already split** into a lower half and an upper half, so the median sits at
> the boundary between them and reading it costs nothing.
>
> Concretely: two heaps facing each other. The lower half is a **max-heap**, so the **largest** of the small
> numbers is at its top. The upper half is a **min-heap**, so the **smallest** of the large numbers is at
> its top. Those two values are exactly the two middle elements of the whole stream.
>
> Two invariants make it work. **Order**: everything in the low heap is at most everything in the high heap.
> **Balance**: their sizes differ by at most one. Given both, the median is `O(1)` — on an odd count it is
> the top of the larger heap, and on an even count it is the average of the two tops.
>
> The insert is three lines and I would write them as one unit. **Push** the new value into the low heap
> unconditionally. **Shift** the low heap's top across into the high heap — that is the line that guarantees
> the ordering invariant, because whatever the new value was, the largest candidate for the lower half has
> just been handed over. Then **rebalance**: if the high heap is now larger, move one back. No branches and
> no case analysis.
>
> One Python detail worth saying aloud: `heapq` is min-only, so the low heap stores **negated** values —
> two negations on the way in and out, and exactly one when moving a value across. That is where the bugs
> in this problem live, along with the median function disagreeing with the rebalance rule about which heap
> holds the extra element on an odd count.
>
> `O(log n)` to add, `O(1)` to read, `O(n)` space.
>
> Compared with the alternative people reach for — a sorted list with `bisect` — that is `O(n)` per insert,
> because insertion has to shift everything after it: about two and a half billion element moves at a
> hundred thousand insertions, against roughly a million and a half heap comparisons.
>
> And if you told me the values were bounded — say zero to a hundred — I would throw all of this away and
> keep a **count array**, which is `O(1)` to insert and a constant scan to find the median. Same lesson as
> counting sort: when the key space is small and bounded, bucketing beats every comparison-based
> structure."

---

## 9. Recall card

- **Keep the numbers already SPLIT so the median sits at the boundary.** `low` is a **max-heap** of the
  smaller half (its **largest** on top), `high` is a **min-heap** of the larger half (its **smallest** on
  top) — those two are the middle values. **`O(log n)` add, `O(1)` median.**
- **Two invariants, and everything follows: ORDER (`max(low) ≤ min(high)`) and BALANCE (sizes differ by
  ≤ 1).** Assert both in tests — every bug here breaks one of them **silently**.
- **PUSH, SHIFT, REBALANCE, as one unit:** push into `low` unconditionally · move `low`'s top into `high`
  (this is what guarantees the ordering) · move one back if `high` is bigger. **No branches, no case
  analysis.** The branching version is also correct, faster on random data, and has an empty-heap trap on
  the first insert.
- **Python has no max-heap, so `low` stores NEGATED values — two negations in and out, one when moving
  across.** And **the median function must agree with the rebalance rule** about which heap holds the extra
  element, or you are right on even counts and wrong on odd. Use `/`, not `//`.
- **Forgetting the rebalance is the classic bug**: an increasing sequence drifts everything into one heap
  and the median reads plausibly and wrongly. Variants: **sliding window** = the same + **lazy deletion**,
  where you must track **logical** sizes separately from `len(heap)`; **any percentile** = change the
  balance ratio; **bounded values** → a **count array**, `O(1)`; **at scale** → **t-digest / HdrHistogram**,
  which is what your metrics system really does.
