---
day: 115
track: dsa
title: "Python's heapq, and the min-heap-only problem"
phase: "Heaps and priority queues"
status: written
---

# Day 115 · DSA — Python's heapq, and the min-heap-only problem

**After today you can:** You can simulate a max-heap and store tuples with tie-breakers safely.

**The interviewer asks it as:** *Python only has a min-heap. How do you get the maximum?*

---

## 1. What this is, and why they ask it

`heapq` is Python's heap, and it has three properties that shape every solution you will write with it:
it is **min-only**, it operates on a **plain list** rather than an object, and it compares items with
`<`.

Three sentences. Getting a max-heap means **inverting the ordering**, and the standard trick — negate the
values — works for numbers and fails for everything else, so you need the second technique too. Storing
anything richer than a number means pushing **tuples**, and the moment two tuples have equal first
elements, Python compares the *second* element — which is why a tie-breaker is not optional but a
correctness requirement. And because a heap cannot find or update an element, changing a priority means
**lazy deletion**: push a new entry and skip the stale one when it surfaces.

They ask *"Python only has a min-heap, how do you get the maximum?"* because it takes five seconds to
answer and the follow-up separates people: *"and what if the items are objects rather than numbers?"* The
negation trick is common knowledge; knowing that it does not generalise, and knowing what to do instead,
is not.

---

## 2. The story

The token machine at the sub-registrar's office was installed in 2011 and it did exactly one thing: it
called the **lowest** number that had not yet been served.

For ordinary work that was correct and nobody thought about it. You took a token, and when your number
came up you went in.

The problem arrived when the department decided that senior citizens and people with a disability should
be seen ahead of everybody else. The machine had no setting for it. The man who had installed it had left
the company, and the department that would have to approve a replacement met twice a year.

The clerk, Anjaneyulu, worked out the fix in about a day and a half, and it was not clever, it was
sideways.

The machine called the lowest number. So he issued priority tokens with **low** numbers and ordinary
tokens with **high** ones. Priority tokens started at one; ordinary tokens started at ten thousand.
Nothing about the machine changed. It went on calling the lowest number available, and because of how the
numbers were handed out, that was always the person who ought to go first.

He said afterwards that he had spent a morning trying to make the machine call the highest number, and
about ten minutes on realising that he did not have to.

Two things went wrong with it, and both took him longer to work out than the original idea.

The first was that within the priority group he wanted the person who had arrived first to go first. So he
started printing two things on the token — the priority band, and a running count of how many tokens had
been issued that morning. The machine compared the band first, and when two bands were equal it compared
the count, and the count was never equal to anything.

The second happened on a Thursday when he had briefly tried printing the person's **name** as the second
thing instead of a count. Two people in the priority band, and the machine had to decide between them, and
it compared the names — which worked, in a sense, until a man whose name was written in Telugu and a woman
whose name was written in English came at the same time, and the machine stopped and would not continue
until somebody cleared it.

He went back to the count. He said the second thing on the token has one job, which is to never be equal
and always be comparable, and a name is neither.

---

## 3. The idea in plain English

Anjaneyulu has solved both of the practical problems with `heapq`, and his diagnosis of the second one is
exactly right.

- The machine calling the lowest number is `heapq` being **min-only**.
- Issuing priority tokens with low numbers is **inverting the ordering** rather than changing the
  machine.
- The running count is a **tie-breaker**, and it exists so that the comparison never reaches the payload.
- The names jamming the machine is `TypeError: '<' not supported between instances of ...`.

### The API, in full

```python
    import heapq

    heapq.heapify(lst)              # O(n), in place — NOT n pushes
    heapq.heappush(h, item)         # O(log n)
    heapq.heappop(h)                # O(log n), returns the smallest
    h[0]                            # peek, O(1) — there is no heappeek
    heapq.heappushpop(h, item)      # push then pop, ONE pass
    heapq.heapreplace(h, item)      # pop then push, ONE sift-down
    heapq.nsmallest(k, iterable)    # O(n log k)
    heapq.nlargest(k, iterable)     # O(n log k)
    heapq.merge(*iterables)         # a lazy merge of sorted inputs
```

**There is no heap object.** The list *is* the heap, which means:

```python
    h.append(5)                     # BREAKS the invariant, silently
    h.sort()                        # technically still a valid heap, by luck
    h[3] = 0                        # BREAKS it, silently
    len(h)                          # fine — a heap is a list
    for x in h: ...                 # fine, and NOT in sorted order
```

**Nothing raises.** The list stays a list and the heap property is quietly gone, so subsequent pops return
the wrong element. **Never touch the list except through `heapq` functions.**

### Making a max-heap: negate the values

```python
    for v in values:
        heapq.heappush(h, -v)
    largest = -heapq.heappop(h)
```

**Negate on the way in, negate on the way out.** The min of the negatives is the max of the originals.

**Three caveats worth stating:**

- **It only works for numbers.** Strings, tuples of strings and objects cannot be negated.
- **`-x` for floats is fine**, including `-0.0`, but be careful with `float('nan')`, which compares false
  with everything and will corrupt the heap silently.
- **The integer edge case:** in a fixed-width language, negating the most negative integer overflows.
  Python's integers are arbitrary precision so this does not bite here — **but say it if the interview is
  in C++ or Java**, where `-INT_MIN` is undefined behaviour.

### Making a max-heap: invert the comparison

For anything that is not a number, wrap it in a class whose `__lt__` is reversed:

```python
    from dataclasses import dataclass, field

    @dataclass(order=True)
    class MaxItem:
        key: int
        payload: object = field(compare=False)

        def __lt__(self, other):
            return self.key > other.key         # INVERTED
```

**This is the general answer**, and it is what to give when they ask *"and if the items are objects?"* It
also works for a compound ordering — largest by score, then earliest by time — where negation cannot
express the mixture.

**A third option worth knowing**: `heapq` has private `_heapify_max`, `_heappop_max` and `_siftup_max`
functions. **Do not use them** — they are undocumented, incomplete (there is no `_heappush_max`), and they
change between versions. Naming them and rejecting them is a better answer than using them.

### Tuples: the standard way to carry a payload

```python
    heapq.heappush(h, (priority, tie_breaker, payload))
```

**Tuples compare element by element**, so this orders by `priority` first and then by `tie_breaker`.

**And that is exactly the danger.** If two priorities are equal, Python moves on to the next element — and
if that is your payload, it must be comparable.

```python
    heapq.heappush(h, (1, {"name": "a"}))
    heapq.heappush(h, (1, {"name": "b"}))
```

```
 TypeError: '<' not supported between instances of 'dict' and 'dict'
```

**The tie-breaker is not for tidiness. It is what stops the comparison ever reaching the payload.**
Anjaneyulu's count.

The standard tie-breaker is a monotonically increasing counter:

```python
    counter = itertools.count()
    heapq.heappush(h, (priority, next(counter), payload))
```

**Two properties, and it needs both**: it is **always comparable** (integers), and it is **never equal**
(strictly increasing). A timestamp fails the second on a fast machine; a name fails the first when the
types differ.

**It also gives you FIFO within a priority for free**, which is usually what you want and is worth
mentioning.

### Changing a priority: lazy deletion

A heap cannot find an element, so it cannot update one —
[day 113's](../day-113-the-heap/README.md) weakness. Python offers nothing for this, and the idiomatic
answer is:

```python
    heapq.heappush(h, (new_priority, next(counter), item))    # push the new one
    dead.add(old_entry_id)                                    # mark the old one

    while h:
        priority, seq, item = heapq.heappop(h)
        if seq in dead:
            continue                                          # skip the stale entry
        return item
```

**Push the new entry, leave the old one, and skip it when it surfaces.**

```
 cost:  the heap grows with stale entries — up to O(total pushes) rather than O(live items)
 benefit: no index map to maintain, and no code at all in the hot path
```

**This is what a Python implementation of Dijkstra's algorithm actually does**, and saying so — rather
than describing an indexed heap you would not write — is the practical answer.

### `nlargest` and `nsmallest`

```python
    heapq.nlargest(3, data)                     # O(n log k)
    heapq.nlargest(3, data, key=lambda x: x.score)
```

**They keep a heap of size `k`**, so the memory is `O(k)` rather than `O(n)` and there is no sorting of
the whole input. And the `key` argument means **no tuples and no tie-breaker needed** — the comparison
never touches your objects.

But know where they stop being the right tool:

```
 k = 1              use max() / min() — O(n), no heap at all
 k small (< n/10)   nlargest / nsmallest — O(n log k)
 k close to n       sorted() — O(n log n) and much better constants
```

**CPython's implementation actually does this switching internally for the degenerate cases**, which is a
nice detail to know but not to rely on.

### `merge`

```python
    heapq.merge(list_a, list_b, list_c)         # a lazy iterator
    heapq.merge(*lists, key=..., reverse=...)
```

**It is lazy**, so it merges streams larger than memory — which is exactly the external-sort use case, and
it is [day 117](../day-117-merge-k-sorted/README.md) done for you.

### The comparison rules, in one place

```
 heapq compares with <  only. It never uses ==, >, or __gt__.
 -> you only need __lt__ to make a class heap-compatible
 -> @dataclass(order=True) generates it
 -> functools.total_ordering also works and is more than needed

 tuples compare LEFT TO RIGHT, moving on only when elements are EQUAL
 -> so the payload is compared ONLY when everything before it ties
 -> which is why the tie-breaker must never be equal
```

---

## 4. The picture

The min-only problem, and the two ways round it.

```
 THE PROBLEM                          heapq always gives you the SMALLEST

   values:  3  9  1  7
   heap:    [1, 7, 3, 9]
   pop  ->  1        ...but you wanted 9


 FIX 1 — NEGATE (numbers only)        FIX 2 — INVERT __lt__ (anything)

   push -3, -9, -1, -7                  class MaxItem:
   heap: [-9, -7, -3, -1]                   def __lt__(self, other):
   pop -> -9                                    return self.key > other.key
   negate again -> 9  ✓
                                        heap holds MaxItem objects
   ✓ trivial for ints and floats        ✓ works for ANY type
   ✗ strings, tuples, objects           ✓ works for COMPOUND orderings
                                          (largest score, then earliest time)
```

Anjaneyulu's token machine, as the same picture:

```
 the machine calls the LOWEST number. It cannot be changed.

 priority tokens:   1, 2, 3, ...          ← issued LOW
 ordinary tokens:   10001, 10002, ...     ← issued HIGH

 the machine's behaviour is unchanged.
 The ORDERING was changed, not the machine.
```

The tie-breaker, and what it prevents:

```
 tuples compare LEFT TO RIGHT and stop at the first difference

 (1, 5, obj_a)  vs  (1, 9, obj_b)
  ▲  ▲                ▲  ▲
  │  └── 5 < 9 -> DECIDED here. obj_a and obj_b are never touched.
  └── equal, so move on


 WITHOUT a tie-breaker:

 (1, obj_a)  vs  (1, obj_b)
  ▲  ▲             ▲
  │  └───────────── Python compares obj_a < obj_b
  └── equal, so move on
                            TypeError: '<' not supported between
                            instances of 'dict' and 'dict'

 THE TIE-BREAKER'S ONLY JOB:
   1. always comparable   (an int — a NAME fails this across scripts)
   2. never equal          (a strictly increasing counter — a TIMESTAMP
                            fails this on a fast machine)
```

Lazy deletion, which is how a priority changes:

```
 the heap                       the "dead" set

 (5, 12, taskA)   ← stale       {12}
 (3, 47, taskA)   ← current
 (8, 13, taskB)

 pop -> (3, 47, taskA)   seq 47 not dead   -> USE IT
 pop -> (5, 12, taskA)   seq 12 IS dead    -> SKIP, pop again
 pop -> (8, 13, taskB)   fine

 cost:    the heap holds every version ever pushed, not just the live ones
 benefit: no index map, no bookkeeping on every swap
 -> and this is exactly what a Python Dijkstra does
```

The `heapq` decision table:

```
 what you want                       what to use
 ---------------------------------   -----------------------------------------
 the single largest                  max(data)            — O(n), no heap
 the k largest, k small              heapq.nlargest(k, data)   — O(n log k)
 the k largest, k close to n         sorted(data)[-k:]    — better constants
 a running "next smallest"           heappush / heappop
 a running "next largest"            negate, or invert __lt__
 keep only the best k so far         a size-k heap + heapreplace
 merge sorted streams                heapq.merge()        — LAZY
 change a priority                   lazy deletion (push new, skip stale)
 build from a list you already have  heapq.heapify()      — O(n), NOT n pushes
```

---

## 5. The code, built step by step

### Step 1 — answer the min-only question two ways

"For numbers, negate on the way in and on the way out — the minimum of the negatives is the maximum of the
originals. For anything else, wrap the item in a class with an inverted `__lt__`, because you cannot
negate a string or an object."

**Give both. The second is what the follow-up is for.**

### Step 2 — push tuples, and say why the middle element exists

```python
    heapq.heappush(h, (priority, next(counter), payload))
```

"Tuples compare left to right, so if two priorities tie, Python compares the next element. If that is my
payload, it has to be orderable — and a dictionary is not, so it raises. The counter guarantees the
comparison never gets that far, and it gives me FIFO within a priority for free."

### Step 3 — `heapify`, never `n` pushes

```python
    heapq.heapify(items)                    # O(n)
```

"If I already have all the items, heapify is `O(n)` and pushing them one at a time is `O(n log n)` — about
four times the work at a million items, for the same result."

### Step 4 — `heapreplace` for a fixed-size heap

```python
        if value > h[0]:
            heapq.heapreplace(h, value)
```

"For 'keep the best k', I compare against the smallest first and only then replace — one sift-down instead
of a pop followed by a push."

### Step 5 — say what you must never do to the list

"There is no heap object in Python; the list *is* the heap. Appending to it, sorting it, or assigning to
an element breaks the invariant silently — no exception, just wrong results from later pops."

### The complete solution

```python
import heapq
import itertools
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. The min-only problem: two answers
# ---------------------------------------------------------------------------

def k_largest_by_negation(values: list[int], k: int) -> list[int]:
    """FIX 1: negate in, negate out. The min of the negatives is the max.

    Works for ints and floats. Does NOT work for strings, tuples of
    strings, or objects — which is why fix 2 exists.

    In C++/Java, note that -INT_MIN overflows. Python's ints are arbitrary
    precision, so it does not bite here, but say it if the language differs.
    """
    heap = [-v for v in values]
    heapq.heapify(heap)                     # O(n)
    return [-heapq.heappop(heap) for _ in range(k)]


@dataclass(order=True)
class MaxItem:
    """FIX 2: invert the comparison. Works for ANY type, and for compound
    orderings that negation cannot express.

    heapq only ever uses `<`, so __lt__ is the only method that must exist.
    `compare=False` keeps the payload out of the comparison entirely — which
    is the tie-breaker problem solved at the type level.
    """

    key: int
    payload: object = field(compare=False, default=None)

    def __lt__(self, other: "MaxItem") -> bool:
        return self.key > other.key         # INVERTED: bigger keys sort first


def k_largest_by_inversion(items: list[tuple[int, object]], k: int) -> list[object]:
    heap = [MaxItem(key, payload) for key, payload in items]
    heapq.heapify(heap)
    return [heapq.heappop(heap).payload for _ in range(k)]


# ---------------------------------------------------------------------------
# 2. Tuples and the tie-breaker
# ---------------------------------------------------------------------------

class PriorityQueue:
    """A priority queue that will not raise on a tie.

    THE TIE-BREAKER has exactly two requirements and needs BOTH:
      1. always comparable  — an int. A NAME fails this across scripts.
      2. never equal        — strictly increasing. A TIMESTAMP fails this
                              on a fast machine.

    Tuples compare left to right, so with a unique counter in position 2 the
    payload in position 3 is NEVER compared — which is the point.

    Bonus: the counter gives FIFO within a priority for free.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, object]] = []
        self._counter = itertools.count()

    def push(self, priority: int, item: object) -> None:
        heapq.heappush(self._heap, (priority, next(self._counter), item))

    def pop(self) -> object:
        return heapq.heappop(self._heap)[2]

    def peek(self) -> object:
        return self._heap[0][2]             # O(1)

    def __len__(self) -> int:
        return len(self._heap)


def demonstrate_tie_breaker_bug() -> None:
    """Run this. It raises, and the error is worth seeing once."""
    h: list[tuple[int, dict]] = []
    heapq.heappush(h, (1, {"name": "a"}))
    try:
        heapq.heappush(h, (1, {"name": "b"}))
    except TypeError as exc:
        print(f"TypeError: {exc}")
        # '<' not supported between instances of 'dict' and 'dict'


# ---------------------------------------------------------------------------
# 3. Changing a priority: lazy deletion
# ---------------------------------------------------------------------------

class UpdatablePriorityQueue:
    """A heap cannot find or update an element, so: push the new version,
    mark the old one dead, and skip it when it surfaces.

    This is what a Python implementation of Dijkstra ACTUALLY does — an
    indexed heap (a value -> index map maintained on every swap) is the
    textbook answer and nobody writes it in Python.

    Cost: the heap grows with every version ever pushed, not just the live
    entries. For Dijkstra that is O(E) rather than O(V), which is fine.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, object]] = []
        self._counter = itertools.count()
        self._entry: dict[object, int] = {}      # item -> its live sequence number

    def push(self, priority: int, item: object) -> None:
        seq = next(self._counter)
        self._entry[item] = seq                  # any earlier seq is now stale
        heapq.heappush(self._heap, (priority, seq, item))

    def pop(self) -> tuple[int, object] | None:
        while self._heap:
            priority, seq, item = heapq.heappop(self._heap)
            if self._entry.get(item) == seq:     # is this the live version?
                del self._entry[item]
                return priority, item
            # otherwise it is stale — skip it
        return None

    def __len__(self) -> int:
        return len(self._entry)                  # LIVE entries, not heap size


def dijkstra(graph: dict[str, list[tuple[str, int]]], source: str) -> dict[str, int]:
    """The canonical use of lazy deletion, written out.

    No decrease-key: push a better distance whenever we find one, and skip
    an entry whose distance is worse than the one already settled.
    """
    distance = {source: 0}
    heap = [(0, source)]
    settled: set[str] = set()

    while heap:
        d, node = heapq.heappop(heap)
        if node in settled:
            continue                        # a stale entry — skip it
        settled.add(node)
        for neighbour, weight in graph.get(node, []):
            nd = d + weight
            if nd < distance.get(neighbour, float("inf")):
                distance[neighbour] = nd
                heapq.heappush(heap, (nd, neighbour))    # push, do not update
    return distance


# ---------------------------------------------------------------------------
# 4. Fixed-size heaps, and the shortcuts
# ---------------------------------------------------------------------------

def k_largest_fixed_heap(values: list[int], k: int) -> list[int]:
    """Keep a MIN-heap of size k. The smallest of the k largest is at the
    root, so a new value only matters if it beats it.

    O(n log k) time, O(k) space — better than sorting when k << n.
    heapreplace is ONE sift-down; heappop followed by heappush is two passes.
    """
    heap = values[:k]
    heapq.heapify(heap)
    for v in values[k:]:
        if v > heap[0]:
            heapq.heapreplace(heap, v)      # NOT heappop + heappush
    return sorted(heap, reverse=True)


def top_k_by_key(items: list[dict], k: int, key: str) -> list[dict]:
    """nlargest with a `key` avoids tuples and tie-breakers entirely —
    the comparison never touches your objects."""
    return heapq.nlargest(k, items, key=lambda d: d[key])


def running_median_hint() -> None:
    """Two heaps facing each other: a MAX-heap of the lower half (negated)
    and a MIN-heap of the upper half. Day 118."""


# ---------------------------------------------------------------------------
# 5. The traps, written out so you can run them
# ---------------------------------------------------------------------------

def demonstrate_list_mutation() -> None:
    """There is no heap object. Touching the list breaks it silently."""
    h = [1, 3, 2, 7, 4]
    heapq.heapify(h)
    print("valid:", all(h[(i - 1) // 2] <= h[i] for i in range(1, len(h))))
    h.append(0)                             # NOT heappush
    print("after append, valid:", all(h[(i - 1) // 2] <= h[i]
                                      for i in range(1, len(h))))
    print("pop returns:", heapq.heappop(h), "— not 0, which was the smallest")


def demonstrate_build_cost() -> None:
    """heapify is O(n); n pushes is O(n log n). Same result."""
    import time
    data = list(range(200_000, 0, -1))

    t = time.perf_counter()
    a = data[:]
    heapq.heapify(a)
    fast = time.perf_counter() - t

    t = time.perf_counter()
    b: list[int] = []
    for v in data:
        heapq.heappush(b, v)
    slow = time.perf_counter() - t

    print(f"heapify {fast:.4f}s vs {len(data)} pushes {slow:.4f}s "
          f"({slow / fast:.1f}x)")


if __name__ == "__main__":
    values = [5, 1, 9, 3, 7, 2, 8]

    print(k_largest_by_negation(values, 3))             # [9, 8, 7]
    print(k_largest_by_inversion(
        [(5, "e"), (1, "a"), (9, "i"), (3, "c")], 2))   # ['i', 'e']
    print(k_largest_fixed_heap(values, 3))              # [9, 8, 7]

    # the tie-breaker
    demonstrate_tie_breaker_bug()
    # TypeError: '<' not supported between instances of 'dict' and 'dict'

    pq = PriorityQueue()
    pq.push(2, {"task": "email"})
    pq.push(1, {"task": "page"})
    pq.push(1, {"task": "alert"})           # SAME priority — no raise
    print(pq.pop(), pq.pop(), pq.pop())
    # {'task': 'page'} {'task': 'alert'} {'task': 'email'}   FIFO within priority

    # lazy deletion
    upq = UpdatablePriorityQueue()
    upq.push(5, "taskA")
    upq.push(8, "taskB")
    upq.push(3, "taskA")                    # taskA's priority IMPROVED
    print(upq.pop(), upq.pop(), upq.pop())
    # (3, 'taskA') (8, 'taskB') None        the stale (5, 'taskA') was skipped

    graph = {
        "a": [("b", 1), ("c", 4)],
        "b": [("c", 2), ("d", 5)],
        "c": [("d", 1)],
        "d": [],
    }
    print(dijkstra(graph, "a"))             # {'a': 0, 'b': 1, 'c': 3, 'd': 4}

    # nlargest with a key — no tuples, no tie-breaker
    people = [{"n": "a", "age": 30}, {"n": "b", "age": 25}, {"n": "c", "age": 40}]
    print(top_k_by_key(people, 2, "age"))   # the two oldest

    # merge is LAZY
    merged = heapq.merge([1, 4, 7], [2, 5, 8], [3, 6, 9])
    print(list(merged))                     # [1..9]

    # the traps
    demonstrate_list_mutation()
    demonstrate_build_cost()

    # peek is O(1) and there is no heappeek
    h = [5, 1, 9]
    heapq.heapify(h)
    print(h[0])                             # 1
```

---

## 6. What it costs

### The `heapq` functions

```
 heapify        O(n)
 heappush       O(log n)
 heappop        O(log n)
 h[0]           O(1)
 heappushpop    O(log n)      one pass, not two
 heapreplace    O(log n)      one sift-down
 nsmallest(k)   O(n log k)
 nlargest(k)    O(n log k)
 merge          O(n log k) total, LAZY — O(k) memory
```

**`heapify` against `n` pushes** is the one that matters in practice:

```
 200,000 items, worst-case input (reverse sorted)
   heapify:     ~0.01 s
   n pushes:    ~0.05 s        roughly 4-5x
```

**The measurement is in the code above.** Same result, four times the work, one line to fix.

### `heapreplace` against pop-then-push

```
 heappop + heappush   two operations: a sift-down and a sift-up
 heapreplace          ONE sift-down

 in a top-k loop over 1,000,000 items with k = 100:
   the comparison `if v > h[0]` rejects ~99.99% before touching the heap
   the survivors cost one sift-down each instead of two passes
```

**In a hot loop that is a real constant-factor win**, and it is why the fixed-size-heap idiom is written
that way.

### Top-k, three ways

```
 n = 1,000,000

 k = 10
   sorted(data)[-10:]        O(n log n)   ~20,000,000 comparisons
   heapq.nlargest(10, data)  O(n log k)   ~3,300,000  ← 6x fewer
   size-k heap + replace     O(n log k)   ~3,300,000, and O(k) memory

 k = 500,000
   sorted(data)[-k:]         O(n log n)   ~20,000,000, excellent constants
   heapq.nlargest(k, data)   O(n log k)   ~19,000,000, worse constants
   -> SORT WINS. nlargest is not always the answer.
```

**The crossover is around `k ≈ n/10`**, and knowing that there *is* a crossover is the point.

```
 k = 1  ->  max(data), O(n), no heap at all.
```

### Lazy deletion's memory cost

```
 Dijkstra on a graph with V = 100,000 and E = 500,000

 indexed heap:      the heap holds at most V = 100,000 entries
 lazy deletion:     the heap holds up to E = 500,000 entries
                    -> 5x the memory, and ~5x the pops (most skipped)
```

**Still `O(E log V)` overall**, which is the same asymptotic bound, and the constant is worth paying to
avoid maintaining an index map on every swap.

### Tuple overhead

```
 a heap of 1,000,000 plain ints        ~8 MB list + the int objects
 a heap of 1,000,000 3-tuples          ~8 MB list + ~72 bytes per tuple
                                        ≈ 80 MB
```

**Ten times the memory for the tuple wrapper.** For a large heap, `nlargest` with a `key` — which keeps
only `k` items — or a class with `__slots__` is worth considering.

### Comparison count

```
 heapq uses ONLY `<`.
 -> a class needs only __lt__
 -> @dataclass(order=True) generates all six, which is more than needed
 -> functools.total_ordering also works and is heavier
```

**Each sift-down does two comparisons per level**, so a pop from a million-element heap is about forty
comparisons. If `__lt__` is expensive — a database lookup, a string collation — that is where the time
goes, not in the heap machinery.

---

## 7. The traps

### Trap 1 — expecting a max-heap parameter

```python
    heapq.heappush(h, x, reverse=True)
```

```
 TypeError: heappush() takes 2 positional arguments but 3 were given
```

**There is no such option.** Negate, or invert `__lt__`.

### Trap 2 — the missing tie-breaker

```python
    heapq.heappush(h, (1, {"a": 1}))
    heapq.heappush(h, (1, {"b": 2}))
```

```
 TypeError: '<' not supported between instances of 'dict' and 'dict'
```

**It only fails when priorities tie**, which means it passes in testing and raises in production on the
first collision. Always include a counter.

### Trap 3 — a tie-breaker that can repeat

```python
    heapq.heappush(h, (priority, time.time(), payload))
```

`time.time()` has limited resolution, so two pushes in the same microsecond produce equal timestamps and
Python falls through to the payload. **Use `itertools.count()`** — strictly increasing, always
comparable, and it gives FIFO ordering for free.

### Trap 4 — touching the list directly

```python
    h.append(0)
    heapq.heappop(h)                        # does NOT return 0
```

The list *is* the heap and appending does not sift. **The invariant is broken silently**, and later pops
return wrong values. Same for `h[i] = x` and for sorting the list yourself.

### Trap 5 — building by pushing

```python
    for v in items:
        heapq.heappush(h, v)                # O(n log n)
```

Four to five times slower than `heapq.heapify(items)` for the same result. **If you have the items, use
`heapify`.**

### Trap 6 — negating something that cannot be negated

```python
    heapq.heappush(h, -"banana")
```

```
 TypeError: bad operand type for unary -: 'str'
```

And worse, the *silent* version: negating only the first element of a tuple gives an ordering that is
inverted on the first field and normal on the rest, which is very rarely what anyone wants.

### Trap 7 — `nlargest` when `k` is close to `n`

```python
    heapq.nlargest(500_000, million_items)
```

Correct and slower than `sorted()`. `O(n log k)` with `k ≈ n` is `O(n log n)` with worse constants and
more memory. **The crossover is around `k ≈ n/10`.**

### Trap 8 — mutating an item that is inside the heap

```python
    task.priority = 1                       # the heap does not notice
```

The heap ordered the item when it was pushed and has no way to observe a change. **Push a new entry and
skip the stale one** — lazy deletion.

### Trap 9 — `nan` in a heap of floats

```python
    heapq.heappush(h, float("nan"))
```

`nan < x` and `x < nan` are both `False`, so the sift comparisons behave arbitrarily and the heap property
is quietly meaningless. **No exception.** Filter `nan` out before it goes in.

---

## 8. In the interview

### How it gets asked

- The opener: *"Python only has a min-heap. How do you get the maximum?"*
- The follow-up that decides it: *"And if the items are objects rather than numbers?"*
- The tuple probe: *"You are pushing tuples — what happens when two priorities are equal?"*
- The practical one: *"How do you change the priority of something already in the queue?"*
- The efficiency one: *"You have all million items already. How do you build the heap?"*

### What to say out loud, in the first ninety seconds

1. **Give the quick answer and immediately its limit.** "Negate on the way in and on the way out — the
   minimum of the negatives is the maximum. That works for numbers and only for numbers."
2. **Give the general answer.** "For anything else, wrap the item in a class with an inverted `__lt__`.
   `heapq` only ever uses `<`, so that is the only method it needs — and it also handles compound orderings
   that negation cannot express."
3. **Reject the private functions by name.** "There are undocumented `_heapify_max` and `_heappop_max`
   functions. I would not use them — there is no `_heappush_max`, and they change between versions."
4. **Bring up the tie-breaker before being asked.** "If I am pushing tuples, I always include a counter as
   the second element. Tuples compare left to right, so if two priorities tie, Python compares whatever
   comes next — and if that is a dict or a custom object, it raises."
5. **Say the tie-breaker's two requirements.** "It has to be always comparable and never equal. A timestamp
   fails the second on a fast machine; a name fails the first. `itertools.count()` does both, and gives
   FIFO within a priority for free."
6. **Say what you must not do to the list.** "And there is no heap object — the list *is* the heap.
   Appending to it or assigning to an element breaks the invariant with no exception."

### The follow-ups

**"And if the items are objects rather than numbers?"**
"Then negation is not available, and this is where most people stop. The general answer is to **invert the
comparison** rather than the values: wrap the item in a small class whose `__lt__` returns `self.key >
other.key`. `heapq` only ever uses `<` — it never calls `>`, `==` or `__gt__` — so `__lt__` is the only
method that must exist, and a `@dataclass(order=True)` with `compare=False` on the payload generates it
and keeps the payload out of comparisons entirely. That approach has two advantages over negation beyond
just working: it handles **compound orderings** — largest score first, then earliest timestamp — which
negation cannot express, and it solves the tie-breaker problem at the type level, because the payload is
never compared at all."

**"What happens when two priorities are equal?"**
"Python moves on to the next tuple element, and that is the bug. If my tuple is `(priority, payload)` and
two priorities tie, it compares the payloads — and a dict or a custom object without `__lt__` raises
`TypeError: '<' not supported between instances of 'dict' and 'dict'`. The nasty part is that it **only
fails on a collision**, so it passes every test with distinct priorities and raises in production the first
time two things are equally urgent. So I always push `(priority, counter, payload)` with a counter from
`itertools.count()`. The tie-breaker has exactly two requirements and needs both: **always comparable** —
an integer, where a name fails across scripts — and **never equal** — strictly increasing, where a
timestamp fails on a fast machine. And it gives FIFO ordering within a priority for free, which is usually
what you actually want."

**"How do you change the priority of something already in the queue?"**
"A heap cannot find an element, so it cannot update one — searching is `O(n)`. The textbook answer is an
**indexed heap**: the heap plus a hash map from item to its current index, maintained on every swap, which
makes decrease-key `O(log n)`. Nobody writes that in Python. The idiomatic answer is **lazy deletion**:
push a new entry with the new priority, leave the old one in place, and skip it when it surfaces — I keep
a dict from item to its live sequence number and discard any popped entry whose sequence does not match.
The cost is that the heap holds every version ever pushed rather than just the live ones — for Dijkstra
that is `O(E)` entries instead of `O(V)` — but it stays `O(E log V)` overall and it keeps the hot path
free of bookkeeping. That is exactly what a Python implementation of Dijkstra does, and it is why you see
`if node in settled: continue` at the top of the loop."

**"You already have a million items. How do you build the heap?"**
"`heapq.heapify(items)`, in place, which is `O(n)`. Pushing them one at a time is `O(n log n)` — measured,
about four to five times slower for exactly the same result — and it is the most common avoidable
inefficiency in this topic. The reason heapify is linear is that it sifts **down** from the last parent
backwards: half the nodes are leaves and do no work at all, a quarter can sink at most one level, and the
nodes that could travel far are the rare ones near the root. Pushing sifts **up**, so the many nodes at the
bottom are exactly the ones that can travel the full height, and that really is `O(n log n)`."

**"When would you not use a heap for top-k?"**
"Two cases. When **k is 1**, `max()` is `O(n)` with no structure at all. And when **k is close to n**,
sorting wins: `nlargest` is `O(n log k)`, which at `k ≈ n` is `O(n log n)` with worse constants and more
memory than a straight `sorted()`. The crossover is roughly `k = n/10` — at a million items and k = 10 the
heap does about three million comparisons against twenty million for a sort, a six-fold win; at k =
500,000 the sort wins. So the answer is 'a heap when k is small relative to n', and knowing that there is a
crossover at all is more useful than the exact figure. I would also mention `nlargest` with a `key=`
argument, because it avoids tuples and tie-breakers entirely — the comparison never touches your objects."

**"What can silently break a `heapq` heap?"**
"Four things, and none of them raises. **Touching the list directly** — `append`, an index assignment,
sorting it yourself — because there is no heap object and the list is the heap, so nothing re-establishes
the invariant. **Mutating an item that is already inside**, because the heap ordered it at push time and
cannot observe a change. **A missing tie-breaker**, which does raise but only on a collision, so it is
silent until it is not. And **`float('nan')`**, which compares `False` against everything in both
directions, so the sift comparisons behave arbitrarily and the heap property becomes meaningless with no
error at all. My habit is to assert the invariant in tests — one line,
`all(h[(i-1)//2] <= h[i] for i in range(1, len(h)))` — because every one of these is otherwise invisible."

### A model answer

Asked: *Python only has a min-heap. How do you get the maximum?*

> "Two ways, and I would give both, because the first one is the common answer and it does not generalise.
>
> **For numbers: negate.** Push `-v` and pop `-x`. The minimum of the negated values is the maximum of the
> originals, and nothing about the heap changes — I have inverted the *ordering*, not the structure. Two
> lines, and it is what I would write for a list of integers. One caveat worth stating if the language were
> C++ or Java: negating the most negative integer overflows. Python's integers are arbitrary precision, so
> it does not bite here.
>
> **For anything else: invert the comparison.** You cannot negate a string or an object, so instead I wrap
> the item in a small class whose `__lt__` returns `self.key > other.key`. `heapq` only ever uses `<` — it
> never calls `>` or `==` — so `__lt__` is the only method that has to exist. That version is strictly more
> general: it works for any type, and it handles **compound orderings** like 'highest score, then earliest
> arrival' that negation simply cannot express.
>
> There are undocumented `_heapify_max` and `_heappop_max` functions in the module. I would name them and
> not use them — there is no `_heappush_max`, so the set is incomplete, and they are private and change
> between versions.
>
> While I am here, the two things that actually bite people when using `heapq` for real work.
>
> **Tuples and the tie-breaker.** To carry a payload you push `(priority, payload)` — and tuples compare
> left to right, so when two priorities are equal Python compares the *payloads*. If those are dicts or
> custom objects, that raises `TypeError: '<' not supported`. And it only happens **on a collision**, so it
> passes every test with distinct priorities and fails in production the first time two things are equally
> urgent. So I always push `(priority, counter, payload)` with `itertools.count()`. The tie-breaker needs
> two properties and both matter: **always comparable** — an integer, where a name fails across scripts —
> and **never equal** — strictly increasing, where a timestamp fails on a fast machine. It also gives FIFO
> within a priority for free.
>
> **And changing a priority.** A heap cannot find an element, so there is no update. The textbook answer is
> an indexed heap with a value-to-index map maintained on every swap; the Python answer is **lazy
> deletion** — push the new version, leave the old one, and skip it when it surfaces by checking a live
> sequence number. That is what a Python Dijkstra actually does, and it costs memory proportional to the
> number of pushes rather than the number of live items.
>
> Last thing: there is no heap object. The list *is* the heap, so `append`, an index assignment or sorting
> it yourself breaks the invariant with no exception at all."

---

## 9. Recall card

- **`heapq` is MIN-ONLY. Two fixes: NEGATE (numbers only — `push(-v)`, `pop` and negate back) or INVERT
  `__lt__`** (any type, and the only way to express compound orderings). `heapq` uses **only `<`**, so
  `__lt__` is the only method a class needs. The private `_heapify_max` family is incomplete — name it and
  reject it.
- **Always push `(priority, counter, payload)`.** Tuples compare **left to right**, so equal priorities
  make Python compare the **payload** → `TypeError: '<' not supported between instances of 'dict' and
  'dict'` — **and only on a collision**, so it passes tests and fails in production. The tie-breaker needs
  **both**: always comparable (an int — a *name* fails) and never equal (`itertools.count()` — a
  *timestamp* fails). Bonus: FIFO within a priority.
- **A heap cannot find or update — so changing a priority is LAZY DELETION**: push the new version, leave
  the old, skip it when it surfaces via a live sequence number. Costs `O(pushes)` entries instead of
  `O(live)` — and it is exactly what a Python Dijkstra does.
- **There is no heap object — the list IS the heap.** `append`, `h[i] = x`, or sorting it yourself breaks
  the invariant **with no exception**; so does mutating an item already inside; so does `float('nan')`,
  which compares `False` both ways. Assert `all(h[(i-1)//2] <= h[i] ...)` in tests.
- **`heapify` is `O(n)`; `n` pushes is `O(n log n)` — measured ~4–5× slower for the same result.** Use
  **`heapreplace`** (one sift-down) rather than pop-then-push in a fixed-size top-k loop. And know where
  heaps stop winning: **k = 1 → `max()`; k ≲ n/10 → `nlargest` (`O(n log k)`); k near n → `sorted()`**.
  `nlargest(..., key=)` avoids tuples and tie-breakers entirely, and `heapq.merge` is **lazy**.
