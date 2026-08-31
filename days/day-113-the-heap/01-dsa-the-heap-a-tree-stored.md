---
day: 113
track: dsa
title: "The heap: a tree stored in an array"
phase: "Heaps and priority queues"
status: written
---

# Day 113 · DSA — The heap: a tree stored in an array

**After today you can:** You can compute parent and child indices and explain the heap property.

**The interviewer asks it as:** *What is a heap? Where is the parent of index i?*

---

## 1. What this is, and why they ask it

A **heap** is a binary tree with one rule about values — **every parent is smaller than both its
children** (for a min-heap) — and one rule about shape: **every level is full except the last, which
fills left to right**.

Three sentences. That value rule is much weaker than the [BST rule](../day-106-bst-property/README.md)
and it is deliberately so: a heap does not know which of two siblings is smaller, so it cannot search —
but it can tell you **the single smallest item instantly**, which is all some problems ever need. The
shape rule is what earns its keep: a tree with no gaps can live in a **plain array with no pointers at
all**, where a node at index `i` has its children at `2i + 1` and `2i + 2`. And those two facts together
give you a structure that costs a fifteenth of the memory of a pointer tree and answers "what is next?"
in constant time.

They ask *"where is the parent of index i?"* because it is a five-second question that reveals whether
you understand why a heap is an array. And they ask *"what is a heap?"* because most candidates answer
with the value rule and forget the shape rule — and the shape rule is the entire reason the structure
exists.

---

## 2. The story

The clinic at the bus stand had one doctor, thirty-two plastic chairs bolted into four rows, and a
compounder called Muniyandi who decided the order.

The chairs were numbered, one to thirty-two, painted on the backs. Everybody knew that chair one was seen
next.

What Muniyandi did not do — and this is what the young doctor could not get used to in her first month —
was put everybody in order of how ill they were.

She asked him once who was third-worst in the room, and he said he had no idea, and she thought he was
being difficult.

He explained it that evening. He said: I only ever need one person. When the door opens I need to know
who goes in, and that is chair one. Nobody has ever asked me for third-worst. If I tried to keep all
thirty-two in exact order, every time somebody new walked in I would be shuffling half the room, and
people would be moving chairs all afternoon for a question nobody asks.

What he did keep was a much smaller rule, and he was strict about it: **each chair had two chairs it was
responsible for, and the person in a chair was never worse than either of those two.**

Chair one was responsible for two and three. Chair two for four and five. Chair three for six and seven.
Always the same two, worked out from the number, so nobody had to remember anything.

When somebody new arrived he put them in the highest empty chair — the rows filled left to right, no gaps
— and then walked them up. If they were worse than the person in the chair above, the two swapped, and he
checked again. Usually one or two swaps. Never more than five, because there were only five rows' worth
of steps from the bottom to the top.

And when the door opened, chair one went in, the person from the last occupied chair moved to chair one,
and then walked back down the same way — swapping with the worse of their two responsibilities until they
were in a chair where both of their two were less ill than them.

The young doctor's actual objection came later, and it was a fair one. She said: a man with chest pain is
in chair two, and a man with a headache is in chair three, and there is somebody in chair six who is worse
than the headache. Your rule does not notice.

Muniyandi said it does not, and it does not have to. Chair six is below chair three, and chair three is
below chair one, and all I have ever promised is that **chair one is the worst person in the room**. I
have not promised anything about how two and three compare, and I never will, because keeping that
promise costs more than it is worth.

---

## 3. The idea in plain English

Muniyandi has built a min-heap, and both of his rules — the weak ordering and the no-gaps filling — are
the two halves of the definition.

- "Never worse than the two you are responsible for" is the **heap property**.
- "No idea who is third-worst" is the crucial weakness, and it is deliberate.
- "Fill the highest empty chair, left to right" is the **complete tree** shape.
- "Worked out from the number" is the **array indexing**, which is what the shape rule buys.
- Walking a new arrival up is **sift-up**; walking the replacement down is **sift-down** —
  [tomorrow](../day-114-heapify/README.md).

### The two rules, and why both are needed

**The heap property.** In a **min-heap**, every node is less than or equal to both of its children. In a
**max-heap**, greater than or equal.

```
        1
      /   \
     3     2          every parent <= both children
    / \   / \
   7   4 5   6

 NOTE: 3 and 2 are NOT in order. Neither are 7 and 4 against 5.
 The heap says NOTHING about siblings, or about any two nodes
 not on the same root-to-leaf path.
```

**This is much weaker than a BST**, and the weakness is the point. A BST maintains a total order and pays
`O(log n)` on every insertion to do it. A heap maintains only *"the minimum is at the top"* and pays
`O(log n)` too — but for a far cheaper promise, which is why the constants are small and the memory is
tiny.

```
 heap:  the minimum is at the root.        Finding 5 costs O(n).
 BST:   every value has a known place.     Finding 5 costs O(height).
```

**Say that comparison out loud.** *"A heap is not a sorted structure — it is a structure that knows its
minimum."*

**The shape property.** A heap is a **complete** binary tree: every level is completely full except
possibly the last, and the last fills from the left with no gaps.

**That rule has nothing to do with values and everything to do with storage.**

### The array, which is the actual idea

Because there are no gaps, you can number the nodes level by level, left to right, and store them in a
plain array. Then the tree structure is **arithmetic**:

```
 for a node at index i (0-based):

     left child   =  2i + 1
     right child  =  2i + 2
     parent       =  (i - 1) // 2
```

```
 array:  [ 1, 3, 2, 7, 4, 5, 6 ]
 index:    0  1  2  3  4  5  6

           0:1
          /   \
       1:3     2:2
       /  \    /  \
    3:7  4:4 5:5  6:6

 children of index 1  ->  3 and 4   ✓
 parent of index 5    ->  (5-1)//2 = 2  ✓
```

**No pointers. No node objects. No allocation.** Muniyandi's numbered chairs — the relationships are
computed from the number, so nobody has to remember them.

And this is **only possible because the tree is complete.** A tree with gaps would need a slot for every
possible position, which is `2^(h+1) − 1`:

```
 complete tree, 1,000 nodes     ->  ~1,024 array slots     99% used
 degenerate tree, 40 nodes      ->  ~10^12 slots           impossible
```

**That is why "complete" is half the definition and not a detail.**

### The 1-based variant, and why you might see it

Some texts index from 1, which makes the arithmetic prettier:

```
 0-based:  left = 2i+1,  right = 2i+2,  parent = (i-1)//2
 1-based:  left = 2i,    right = 2i+1,  parent = i//2
```

**Python's `heapq` is 0-based.** Know both, use the 0-based one, and say which you are using — mixing them
silently corrupts the structure.

### What a heap is for

```
 peek the minimum       O(1)        it is index 0
 insert                 O(log n)    place at the end, sift UP
 extract the minimum    O(log n)    swap in the last, sift DOWN
 build from n items     O(n)        not O(n log n) — day 114
 find an arbitrary item O(n)        THE weakness
 delete an arbitrary    O(n)        because you must find it first
```

**`O(1)` peek is the reason the structure exists.** Everything that repeatedly asks *"what is the next
most urgent thing?"* wants a heap:

- **task schedulers and event loops** — the next event by time
- **Dijkstra's algorithm and A\*** — the nearest unvisited node
- **top-k problems** — [day 116](../day-116-top-k/README.md)
- **merging k sorted lists** — [day 117](../day-117-merge-k-sorted/README.md)
- **the running median** — [day 118](../day-118-two-heaps/README.md), with two heaps
- **heapsort** — build a heap, extract everything

### What a heap is not for

**Searching.** There is no ordering between siblings, so an arbitrary value could be anywhere. `O(n)`,
and it is the answer that catches people out.

**Sorted iteration.** A heap's array is *not* sorted, and printing it is not printing sorted order. You
must extract `n` times, at `O(log n)` each — which is `O(n log n)` and is exactly heapsort.

**The k-th smallest, for arbitrary k.** `O(k log n)` by extracting k times, which is fine for small `k`
and terrible for `k = n/2`.

**Say the weakness unprompted.** *"A heap gives me the minimum in constant time and nothing else in less
than linear time."*

### Heap against the alternatives

```
                     peek min   insert     extract min   search    sorted order
 sorted array        O(1)       O(n)       O(1)          O(log n)  free
 unsorted array      O(n)       O(1)       O(n)          O(n)      O(n log n)
 balanced BST        O(log n)   O(log n)   O(log n)      O(log n)  free
 HEAP                O(1)       O(log n)   O(log n)      O(n)      O(n log n)
```

**The heap wins nothing outright and loses nothing badly**, and that is the point: it is the cheapest
structure that does insert-and-extract-minimum well, and its constants and memory are far better than a
BST's because there are no pointers and no allocation.

```
 1,000,000 integers
   pointer-based BST     ~120 MB
   heap in a Python list   ~8 MB      15x smaller
   heap in a C array        4 MB
```

**That memory difference is a real reason to choose it**, and it is worth quoting.

### `heapq`, and its one surprise

```python
    import heapq
    h = []
    heapq.heappush(h, 5)
    heapq.heappush(h, 1)
    heapq.heappop(h)            # 1
    h[0]                        # peek, O(1)
    heapq.heapify(lst)          # O(n), in place
```

**Python's `heapq` is a MIN-heap only.** There is no `max=True`. For a max-heap you push negated values —
[day 115](../day-115-heapq/README.md) — and that is the single most common practical gotcha.

Also: **`heapq` operates on a plain list.** There is no heap object; the list *is* the heap, and if you
mutate it directly you break the invariant with no error.

---

## 4. The picture

The tree and its array, side by side. **This is the diagram to be able to draw.**

```
            0:1                        index:  0  1  2  3  4  5  6
           /    \                      array: [1, 3, 2, 7, 4, 5, 6]
        1:3      2:2
       /   \    /   \                  left(i)   = 2i + 1
    3:7   4:4 5:5   6:6                right(i)  = 2i + 2
                                       parent(i) = (i-1) // 2

 check:  children of 1  ->  3, 4   ->  values 7 and 4.  3 <= both ✓
         parent of 5    ->  (5-1)//2 = 2  ->  value 2.  2 <= 5 ✓

 THE SAME THING, TWICE. The tree is a drawing; the array is the data.
```

Why "complete" is what makes the array possible:

```
 COMPLETE — every level full except the last, which fills LEFT to right

        o                index 0
      /   \
     o     o             1, 2
    / \   /
   o   o o               3, 4, 5      ← no gaps, so no wasted slots
                         array: 6 entries for 6 nodes

 NOT COMPLETE

        o                index 0
      /   \
     o     o             1, 2
    /       \
   o         o           3, ... 6     ← indices 4 and 5 are EMPTY
                         array: 7 slots for 5 nodes, and it gets
                                exponentially worse with depth

 a degenerate tree of 40 nodes would need ~10^12 slots.
 That is why the shape rule is half the definition.
```

The heap property is weak, and that is deliberate:

```
        1
      /   \
     3     2       is 3 < 2?  The heap does not care and does not know.
    / \   / \      is 7 < 5?  Same.
   7   4 5   6

 GUARANTEED:      every node <= its own descendants
 NOT GUARANTEED:  anything between two nodes on different branches

 CONSEQUENCE: the minimum is at index 0, instantly.
              finding the value 5 means scanning: O(n).
              a BST would find it in O(height) — but a BST pays for
              a total order it does not need here.
```

Muniyandi's clinic, as the same picture:

```
 chairs  1   2   3   4   5   6   7      (his numbering is 1-based)
        [A] [B] [C] [D] [E] [F] [G]

 chair 1's responsibilities:  2, 3      = 2i, 2i+1
 chair 3's responsibilities:  6, 7
 chair 6's boss:              3         = i // 2

 he promises:  A is worse than B and C
               B is worse than D and E
 he promises NOTHING about B against C.

 "Nobody has ever asked me for third-worst."
```

Insert and extract, at a glance (the mechanics are tomorrow):

```
 INSERT 0                             EXTRACT MIN

 put it in the next free slot         take index 0 (the answer)
 then walk it UP while it is          move the LAST element to index 0
 smaller than its parent              then walk it DOWN, swapping with
                                      the SMALLER child
        1                                    1  ← returned
      /   \                                /   \
     3     2                              3     2
    / \   / \                            / \   /
   7   4 5   6                          7   4 5   [6 moves to the top]
  /
 0  ← new                              at most `height` swaps either way
                                       = O(log n)
 0 < 7, swap. 0 < 3, swap. 0 < 1, swap.
 at most `height` swaps = O(log n)
```

---

## 5. The code, built step by step

### Step 1 — say both halves of the definition

"A heap has two rules. The **value** rule: every parent is less than or equal to both children — which is
much weaker than a BST, because siblings are unordered. And the **shape** rule: it is a complete tree,
every level full except the last which fills left to right. The shape rule is the one people forget, and
it is the reason the whole thing works."

### Step 2 — derive the index arithmetic rather than reciting it

```
 level 0:  index 0                  1 node
 level 1:  indices 1, 2             2 nodes
 level 2:  indices 3, 4, 5, 6       4 nodes
```

"Numbering level by level, left to right, node `i`'s children land at `2i + 1` and `2i + 2`, and the
parent is `(i − 1) // 2`. It works only because there are no gaps — that is what 'complete' buys."

### Step 3 — the peek, which is the whole value proposition

```python
    def peek(self):
        return self.data[0]                 # O(1)
```

**One line, constant time.** Say why it matters: everything that repeatedly asks "what is next?" wants
this and nothing else.

### Step 4 — insert: place at the end, walk up

```python
        self.data.append(value)
        i = len(self.data) - 1
        while i > 0 and self.data[i] < self.data[(i - 1) // 2]:
            parent = (i - 1) // 2
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent
```

**Appending keeps the tree complete automatically**, which is why the shape rule survives every operation
for free.

### Step 5 — say the weakness before being asked

"Finding an arbitrary value is `O(n)`, because siblings are unordered so it could be anywhere. A heap
knows its minimum and nothing else."

### The complete solution

```python
import heapq


class MinHeap:
    """A binary min-heap in a plain list. No nodes, no pointers, no allocation.

    TWO RULES:
      VALUE  every parent <= both children.  Siblings are UNORDERED.
      SHAPE  a COMPLETE tree — every level full except the last, which fills
             left to right. This is what allows array storage.

    INDEX ARITHMETIC (0-based; Python's heapq is 0-based too):
      left(i)   = 2i + 1
      right(i)  = 2i + 2
      parent(i) = (i - 1) // 2
    """

    def __init__(self, items: list[int] | None = None) -> None:
        self.data: list[int] = list(items or [])
        if self.data:
            self._heapify()

    # -- the arithmetic, named so the code reads as the tree ---------------

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    # -- the operations ----------------------------------------------------

    def peek(self) -> int:
        """THE reason the structure exists: O(1)."""
        if not self.data:
            raise IndexError("peek from an empty heap")
        return self.data[0]

    def push(self, value: int) -> None:
        """Append (which keeps the tree complete for free), then sift UP.
        At most `height` swaps, so O(log n)."""
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def pop(self) -> int:
        """Take index 0, move the LAST element there, then sift DOWN.

        Moving the last element is what preserves completeness — removing
        from the middle would leave a gap and break the array layout.
        """
        if not self.data:
            raise IndexError("pop from an empty heap")
        smallest = self.data[0]
        last = self.data.pop()
        if self.data:                       # not the element we just removed
            self.data[0] = last
            self._sift_down(0)
        return smallest

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = self._parent(i)
            if self.data[i] >= self.data[parent]:
                break                       # the property holds; stop
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent

    def _sift_down(self, i: int) -> None:
        n = len(self.data)
        while True:
            smallest = i
            left, right = self._left(i), self._right(i)
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right            # swap with the SMALLER child
            if smallest == i:
                return
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest

    def _heapify(self) -> None:
        """Build in O(n), not O(n log n). Day 114 explains why.
        Start at the last PARENT — everything after it is a leaf."""
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __len__(self) -> int:
        return len(self.data)

    def is_valid(self) -> bool:
        """Check the property directly: every parent <= both children."""
        return all(
            self.data[self._parent(i)] <= self.data[i]
            for i in range(1, len(self.data))
        )

    def find(self, value: int) -> int:
        """THE WEAKNESS: O(n). Siblings are unordered, so the value could be
        anywhere. This is what a heap cannot do, and it is why a heap is not
        a substitute for a BST."""
        for i, v in enumerate(self.data):
            if v == value:
                return i
        return -1


def index_arithmetic_demo(n: int) -> None:
    """Print the tree relationships for a heap of n items, to make the
    arithmetic concrete."""
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        parent = (i - 1) // 2 if i > 0 else None
        print(f"index {i}: parent {parent}, children "
              f"{left if left < n else '-'}, {right if right < n else '-'}")


def is_heap(data: list[int]) -> bool:
    """Is this array a valid min-heap? Checks the VALUE rule; the shape rule
    is automatic for any array, which is the point."""
    return all(data[(i - 1) // 2] <= data[i] for i in range(1, len(data)))


def heapsort(items: list[int]) -> list[int]:
    """Build a heap, then extract everything. O(n log n), and it shows that
    a heap's array is NOT sorted — you have to extract to get order."""
    h = MinHeap(items)
    return [h.pop() for _ in range(len(h))]


def kth_smallest(items: list[int], k: int) -> int:
    """O(n + k log n): build in O(n), then k extractions.
    Good for small k; for k = n/2 a sort is better."""
    h = MinHeap(items)
    for _ in range(k - 1):
        h.pop()
    return h.pop()


class Task:
    """Heaps hold anything ORDERABLE, not just numbers. A tuple is the usual
    trick: (priority, tie_breaker, payload) — see day 115 for why the
    tie-breaker matters."""

    def __init__(self, priority: int, name: str) -> None:
        self.priority = priority
        self.name = name

    def __lt__(self, other: "Task") -> bool:
        return self.priority < other.priority

    def __repr__(self) -> str:
        return f"Task({self.priority}, {self.name!r})"


if __name__ == "__main__":
    h = MinHeap()
    for v in (5, 3, 8, 1, 9, 2, 7):
        h.push(v)

    print(h.data)                           # [1, 3, 2, 5, 9, 8, 7]
    print(h.peek(), len(h))                 # 1 7
    print(h.is_valid())                     # True

    # THE ARRAY IS NOT SORTED — that is the point
    print(h.data == sorted(h.data))         # False
    print(heapsort([5, 3, 8, 1, 9, 2, 7]))  # [1, 2, 3, 5, 7, 8, 9]

    index_arithmetic_demo(7)
    # index 0: parent None, children 1, 2
    # index 1: parent 0, children 3, 4
    # index 3: parent 1, children -, -

    # extraction gives sorted order, one at a time
    print([h.pop() for _ in range(3)])      # [1, 2, 3]
    print(h.is_valid())                     # True

    # building is O(n), not O(n log n)
    big = MinHeap(list(range(1000, 0, -1)))
    print(big.peek(), big.is_valid())       # 1 True

    # THE WEAKNESS
    print(big.find(500) != -1)              # True, in O(n)

    # heapq: the same thing, in C, and MIN-ONLY
    lst = [5, 3, 8, 1]
    heapq.heapify(lst)                      # O(n), in place
    heapq.heappush(lst, 0)
    print(lst[0], heapq.heappop(lst))       # 0 0
    print(heapq.nsmallest(3, [5, 1, 8, 3, 9]))          # [1, 3, 5]

    # a max-heap by negating — day 115
    maxh: list[int] = []
    for v in (5, 3, 8, 1):
        heapq.heappush(maxh, -v)
    print(-maxh[0])                         # 8

    # heaps hold anything orderable
    tasks: list[Task] = []
    for t in (Task(3, "email"), Task(1, "page"), Task(2, "log")):
        heapq.heappush(tasks, t)
    print(heapq.heappop(tasks))             # Task(1, 'page')

    # memory: a heap is an array, not a pointer structure
    import sys
    arr = list(range(100_000))
    print(f"{sys.getsizeof(arr) / 1024:.0f} KB for 100,000 ints in a list")
```

---

## 6. What it costs

### The operations

```
 peek the minimum        O(1)          index 0
 push                    O(log n)      append, then at most `height` swaps up
 pop the minimum         O(log n)      swap in the last, then at most `height` down
 build from n items      O(n)          NOT O(n log n) — day 114
 heapsort                O(n log n)    n extractions
 find an arbitrary value O(n)          THE weakness
 delete an arbitrary     O(n)          find is the expensive part
 merge two heaps         O(n)          rebuild; a binary heap cannot merge cheaply
```

**Height is `⌊log₂ n⌋` and it is guaranteed**, not merely expected — because the tree is complete by
construction. **That is a real advantage over a BST**, which needs balancing machinery to promise the same
thing.

```
 n = 1,000          height 9
 n = 1,000,000      height 19
 n = 1,000,000,000  height 29
```

### Memory, which is the underrated advantage

```
 1,000,000 integers

 pointer-based BST (Python)   ~120 bytes/node  ->  ~120 MB
 heap in a Python list        ~8 bytes/slot + int objects  ->  ~8 MB of list,
                                                                ~28 MB with the ints
 heap in a C/NumPy array      4 bytes/int      ->  4 MB
```

**Fifteen to thirty times smaller than a pointer tree**, because there are no node objects, no pointers,
and no allocation per element. And the array is **contiguous**, so it is far friendlier to the CPU cache:
a sift-down walks `2i+1`, `4i+3`, and so on, which spreads out — but the top levels of the heap stay
resident in cache and those are where most comparisons happen.

### Why `find` is `O(n)`

```
 the value 5 could be at ANY index below the first index whose value exceeds 5
 -> in the worst case, everywhere
 -> n/2 of the nodes are leaves, and any of them could hold it
```

**No pruning is possible**, because siblings are unordered. This is the single sentence that explains why
a heap does not replace a BST.

### Against the alternatives, with numbers

```
 task: insert 1,000,000 items, then extract the smallest 1,000

 sorted array (kept sorted)  1,000,000 insertions × up to 1,000,000 shifts  — no
 sort once, then read        O(n log n) = ~20,000,000 comparisons
 balanced BST                1,000,000 × 20 = 20,000,000, plus 120 MB
 HEAP                        build O(n) = 1,000,000
                             + 1,000 pops × 20 = 20,000
                             ≈ 1,020,000 operations, and 8 MB
```

**Twenty times fewer operations and fifteen times less memory** for this shape of problem, which is
exactly the top-k shape of [day 116](../day-116-top-k/README.md).

### Where the array layout breaks down

```
 array slots needed = 2^(height + 1) - 1

 COMPLETE tree, n = 1,000        1,024 slots       99% used
 COMPLETE tree, n = 1,000,000    ~1,048,576        99.9% used
 degenerate tree, n = 40         ~1.1 × 10^12      impossible
```

**The completeness rule is not a stylistic preference** — it is the precondition for the whole
representation.

---

## 7. The traps

### Trap 1 — saying only the value rule

*"A heap is a tree where every parent is smaller than its children."* Incomplete, and it misses the half
that matters. **Without the shape rule there is no array, and without the array a heap is just a worse
BST.**

### Trap 2 — thinking a heap is sorted

```python
    h = MinHeap([5, 3, 8, 1])
    print(h.data)                           # [1, 3, 8, 5] — NOT sorted
```

The array is a heap, not a sorted list. **Printing it is not printing sorted order**, and iterating it
gives you the elements in no useful sequence. Sorted order costs `n` extractions, which is `O(n log n)`.

### Trap 3 — expecting to find things

```python
    5 in h.data                             # O(n)
```

A heap cannot search. If a problem needs both "give me the minimum" and "find and update an arbitrary
element", you need a heap **plus a hash map from value to index**, and every swap must update the map.
**That is the indexed-heap structure Dijkstra's algorithm uses**, and it is worth naming.

### Trap 4 — the off-by-one in the index arithmetic

```python
    parent = i // 2                         # WRONG for 0-based indexing
```

`i // 2` is the 1-based formula. For 0-based it is `(i - 1) // 2`. Mixing the conventions produces a
structure that looks like a heap and is not, with no error.

```
 0-based:  left = 2i+1, right = 2i+2, parent = (i-1)//2
 1-based:  left = 2i,   right = 2i+1, parent = i//2
```

### Trap 5 — removing the wrong element on pop

```python
        self.data[0] = self.data[-1]
        self.data.pop()                     # order matters
```

You must move the **last** element to the root and shorten the array — never remove from the middle, which
would leave a gap and destroy the completeness the array layout depends on.

And the subtle case: **when there is exactly one element**, popping the last and then assigning it to
index 0 would resurrect it. The version in the code checks `if self.data:` after the pop.

### Trap 6 — sifting down against the wrong child

```python
        if self.data[left] < self.data[i]:
            swap with left                  # WRONG when right is smaller
```

You must swap with the **smaller** of the two children. Swapping with the left one when the right is
smaller leaves the new parent greater than its right child — the property is violated and nothing raises.

### Trap 7 — mutating the list behind `heapq`'s back

```python
    lst[3] = 0                              # the invariant is now broken
    heapq.heappop(lst)                      # returns the wrong element
```

**There is no heap object in Python** — the list *is* the heap. Changing an element's value, sorting it,
appending with `.append()` instead of `heappush`, all silently break it. If you must change a priority,
push a new entry and mark the old one dead — [day 115](../day-115-heapq/README.md).

### Trap 8 — expecting a max-heap from `heapq`

```python
    heapq.heappush(h, x, reverse=True)      # TypeError — no such thing
```

`heapq` is min-only. Negate the values, or wrap them in a class with an inverted `__lt__`. This is the
most common practical gotcha in Python and it is [tomorrow's neighbour](../day-115-heapq/README.md).

---

## 8. In the interview

### How it gets asked

- The definition: *"What is a heap?"*
- The five-second one: *"Where is the parent of index i?"*
- The comparison: *"How is it different from a BST?"* / *"Why not use a sorted array?"*
- The weakness: *"How would you find an arbitrary element?"*
- The application: *"Which problems does this actually solve?"*

### What to say out loud, in the first ninety seconds

1. **Give both rules, and flag which one people forget.** "Two rules. Values: every parent is less than or
   equal to both children — much weaker than a BST, because siblings are unordered. And shape: it is a
   **complete** tree, every level full except the last, filling left to right. The shape rule is the one
   people leave out, and it is the reason the structure exists."
2. **Say what the shape buys.** "Because there are no gaps, it lives in a plain array — node `i`'s children
   are at `2i + 1` and `2i + 2`, and the parent is `(i − 1) // 2`. No pointers, no node objects, no
   allocation."
3. **Give the value proposition in one line.** "`O(1)` to see the minimum, `O(log n)` to insert or remove
   it. That is all it promises, and it is exactly what anything asking 'what is next?' needs."
4. **State the weakness before being asked.** "It cannot search: an arbitrary value could be anywhere,
   because siblings are unordered, so finding one is `O(n)`. A heap knows its minimum and nothing else."
5. **Compare with a BST honestly.** "A BST maintains a total order and can find anything in `O(height)`. A
   heap maintains a much weaker promise for the same `O(log n)` cost — which buys far smaller constants and
   about fifteen times less memory, because it is an array."
6. **Name the height guarantee.** "And the height is `log n` **guaranteed**, not expected, because
   completeness is maintained by construction — no rotations, no balancing machinery."

### The follow-ups

**"Where is the parent of index i?"**
"`(i − 1) // 2`, zero-based — and the children are at `2i + 1` and `2i + 2`. I would say which convention I
am using, because the one-based version is `i // 2`, `2i` and `2i + 1`, and mixing them produces something
that looks like a heap and is not, with no error. The reason the arithmetic works at all is the shape
rule: the tree is **complete**, so numbering it level by level, left to right, leaves no gaps, and the
positions are computable rather than stored. If the tree could have gaps you would need a slot for every
possible position — `2^(h+1) − 1` — and a forty-node chain would need about a trillion slots."

**"How is it different from a BST?"**
"The promise is much weaker, deliberately. A BST orders **every** pair of values, so it can find anything
in `O(height)`. A heap only guarantees that each node is smaller than its own descendants — it says
nothing about siblings, or about any two nodes on different branches. So it gives you the minimum in
constant time and cannot find anything else in less than linear time. The trade is worth it when you only
ever need the extreme: you get the same `O(log n)` insertion for a cheaper promise, which means much
smaller constants, a **guaranteed** `log n` height with no balancing machinery, and about fifteen times
less memory because it is an array with no pointers or node objects. A million integers is roughly 8 MB as
a heap against 120 MB as a pointer tree."

**"How would you find an arbitrary element?"**
"Linear scan, `O(n)`, and there is no way around it inside the heap itself — no pruning is possible,
because siblings are unordered, so the value could be under either child of every node. If a problem needs
both 'give me the minimum' and 'find and update this specific element', which Dijkstra's algorithm does,
the standard answer is an **indexed heap**: the heap plus a hash map from element to its current index, and
every swap updates the map. That gets find and decrease-key down to `O(log n)`, at the cost of maintaining
the map on every operation. In Python the usual shortcut is lazier — push a new entry with the new
priority and skip stale entries when you pop them."

**"Why not use a sorted array?"**
"A sorted array beats a heap on everything except the operation that matters here. Peeking the minimum is
`O(1)` in both. Searching is `O(log n)` in the array and `O(n)` in the heap. Sorted iteration is free in
the array. But **insertion** is `O(n)` in a sorted array because everything after the insertion point
shifts — a million-element array means up to a million moves per insert. The heap is `O(log n)`. So: if
the data is built once and only read, use a sorted array; if items arrive and leave continuously and you
only ever need the extreme, use a heap. Concretely, for 'insert a million items and take the smallest
thousand', a heap is about a million operations and a sorted array is a million insertions each shifting
up to a million elements."

**"What is it actually used for?"**
"Anything that repeatedly asks 'what is the next most urgent thing?'. **Task schedulers and event loops** —
the next event by timestamp. **Dijkstra and A\*** — the nearest unvisited node, which is the classic. **Top
k** — keep a heap of size k and you get the k largest in `O(n log k)` instead of sorting everything.
**Merging k sorted lists** — a heap of the k current heads. **The running median** — two heaps facing each
other. And **heapsort**, which is build-then-extract-everything and is the one algorithm that sorts in
`O(n log n)` with `O(1)` extra space. The unifying property is that all of them need only the extreme
element and never need to search."

**"Can you merge two heaps?"**
"Not cheaply with a binary heap — the honest answer is that you concatenate the arrays and rebuild, which
is `O(n + m)`. Merging is the operation binary heaps are bad at, and it is why other heap variants exist:
a **binomial heap** merges in `O(log n)`, and a **Fibonacci heap** merges in `O(1)` amortised and also
does decrease-key in `O(1)`, which is what makes Dijkstra's theoretical bound better. In practice nobody
uses Fibonacci heaps because the constants are terrible — but naming them shows you know that the binary
heap is a point on a curve rather than the only option."

### A model answer

Asked: *what is a heap, and where is the parent of index i?*

> "A heap has **two** rules, and the second one is the one people leave out.
>
> The **value** rule: every parent is less than or equal to both of its children, for a min-heap. That is a
> much weaker promise than a binary search tree makes — it says nothing at all about how two siblings
> compare, or about any two nodes on different branches. All it guarantees is that **the minimum is at the
> root**.
>
> The **shape** rule: it is a **complete** binary tree. Every level is completely full except possibly the
> last, and the last fills from the left with no gaps.
>
> That second rule is why the structure exists. Because there are no gaps, you can number the nodes level
> by level, left to right, and store them in a **plain array** — the tree structure becomes arithmetic
> rather than pointers. Node `i`'s children are at `2i + 1` and `2i + 2`, and **the parent of `i` is
> `(i − 1) // 2`**, zero-based. I would say the convention, because one-based indexing gives the prettier
> `2i`, `2i + 1` and `i // 2`, and mixing them silently corrupts the structure.
>
> The payoff is that there are no node objects, no pointers and no allocation per element: a million
> integers is about eight megabytes as a heap against a hundred and twenty as a pointer tree. And the
> height is `log n` **guaranteed** rather than expected, because completeness is preserved by construction
> — you append at the end and sift up, or move the last element to the root and sift down, and both keep
> the shape automatically. No rotations, no balancing machinery.
>
> What it promises is narrow and worth being explicit about: **`O(1)` to see the minimum, `O(log n)` to
> insert or extract it, and `O(n)` for absolutely everything else.** Finding an arbitrary value is a linear
> scan, because siblings are unordered so no pruning is possible. A heap is not a sorted structure — its
> array is not in order, and getting sorted order costs `n` extractions.
>
> Which makes it exactly the right tool for anything that repeatedly asks 'what is the next most urgent
> thing?' — schedulers, Dijkstra, top-k, merging sorted streams, a running median — and the wrong tool for
> anything that needs to look things up."

---

## 9. Recall card

- **TWO rules, and the second is the one people forget. VALUE: every parent ≤ both children — much weaker
  than a BST, because siblings are UNORDERED. SHAPE: a COMPLETE tree, every level full except the last,
  filling left to right.** The shape rule is why the structure exists.
- **Completeness means no gaps, so the tree lives in a plain ARRAY: `left = 2i + 1`, `right = 2i + 2`,
  `parent = (i − 1) // 2`** (0-based; the 1-based forms are `2i`, `2i+1`, `i // 2` — **never mix them**).
  No pointers, no node objects, and the height is **`log n` guaranteed**, not expected.
- **The promise is narrow: `O(1)` peek, `O(log n)` push and pop, `O(n)` build — and `O(n)` for everything
  else.** Finding an arbitrary value is a **linear scan**, because no pruning is possible when siblings are
  unordered. **A heap knows its minimum and nothing else**, and its array is **not sorted**.
- **Memory is the underrated win: 1,000,000 integers ≈ 8 MB as a heap against ~120 MB as a pointer tree.**
  For "insert a million, take the smallest thousand", a heap is ~1 million operations against 20 million
  for a sort.
- **Use it whenever the question is "what is next?"** — schedulers, **Dijkstra**, top-k, merging k sorted
  lists, running median, heapsort. **Do not use it to search.** If you need find-and-update too, that is an
  **indexed heap** (heap plus a value→index map). And **Python's `heapq` is min-only, operates on a plain
  list, and breaks silently if you mutate that list directly.**
