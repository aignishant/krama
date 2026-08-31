---
day: 76
track: dsa
title: "LRU cache: the structure interviewers love"
phase: "Stacks and queues"
status: written
---

# Day 076 · DSA — LRU cache: the structure interviewers love

**After today you can:** You can build an LRU cache with O(1) get and put and explain both data structures.

**The interviewer asks it as:** *Design an LRU cache with O(1) get and put.*

---

## 1. What this is, and why they ask it

An **LRU cache** is a fixed-size store of key–value pairs. When it is full and something new arrives,
it throws out the **least recently used** entry — the one nobody has touched for the longest. LRU is
the three-letter name for that eviction rule.

Both operations must be O(1). `get(key)` returns the value and marks that key as just used.
`put(key, value)` stores it, marks it as just used, and evicts the oldest if the store is now over
capacity.

They ask it because it cannot be solved with one data structure, and the whole interview is watching
you discover that. A hash map gives you O(1) lookup and no notion of order. A list gives you order
and O(n) removal. The answer is **both at once**: a hash map from key to node, and a doubly linked
list holding the nodes in recency order. It is asked constantly — it is LeetCode 146, it appears in
Amazon, Google, Microsoft, Uber and Atlassian loops, and it is the most common "design a data
structure" question there is. It also stops being a puzzle the moment you have to build a real cache,
because this is what Redis, your CPU and your operating system all do.

---

## 2. The story

Sudha's kitchen has one shelf that is actually within reach, and it holds twelve jars.

It is above the stove and about as wide as her arms. Everything else — the rest of the spices, the
things bought in bulk, the box of dried things she uses twice a year — lives in the loft over the
door, and getting up there means the stool, and the stool means moving the water drum.

So the twelve jars on the shelf are the twelve she is actually cooking with, and she has a way of
keeping it that way that she has never once thought about as a system.

When she takes a jar down and uses it, she does not put it back where it was. She puts it back at the
left end, next to the stove, where her hand goes first. Everything else shifts along a little to make
room. So the left end of the shelf is always whatever she used last, and the right end is whatever
she has not touched in the longest time.

That right end is where the decision gets made. When something new arrives — the packet of star anise
her sister brought from Kerala — the shelf is already full, so something has to go up to the loft.
She does not think about which. She takes whatever is sitting at the far right, because by definition
that is the one she has gone longest without needing. It goes up, star anise comes down to the left
end, and the shelf is twelve again.

Two small things make this fast, and she would not be able to name either of them.

The first is that she never searches the shelf. She knows where the turmeric is the way she knows
where the light switch is — she reaches, and it is there. If she had to read every label from the
left each time, the whole arrangement would be pointless, because finding would cost more than the
walking she saved.

The second is what happens when she pulls a jar out of the middle. The jars stand shoulder to
shoulder, so lifting one out leaves a gap, and she closes it in the same movement — one hand nudges
the jar on the left, the other the jar on the right, and they meet. She does not touch the other nine.
Whether the shelf holds twelve jars or forty, closing the gap is the same two nudges.

Her daughter reorganised it once, alphabetically, and it lasted four days.

---

## 3. The idea in plain English

The shelf is a **doubly linked list**. Knowing where the turmeric is without looking is a **hash
map**. And the reason the whole thing is O(1) is Sudha's two nudges.

### Why one structure is not enough

**A hash map alone.** A dictionary gives you `get` and `put` in O(1), which sounds like the whole
problem solved — until you have to evict. Which key is the least recently used? A dictionary has no
answer. You would have to store a timestamp with each value and scan every entry to find the smallest
one, which is O(n) per eviction.

**A list alone.** Keep entries in a list, most recent at the front. Now eviction is trivial — remove
the last one. But `get(key)` has to scan the list to find the key, which is O(n), and moving an entry
from the middle to the front means shifting everything after it, which is another O(n), for exactly
the reason `list.pop(0)` was slow on [day 073](../day-073-queues/README.md).

**Both.** The hash map answers "where is it?" in O(1). The list answers "which is oldest?" in O(1).
Neither can do the other's job, and neither can be dropped. Saying that sentence out loud early is
how you show the interviewer you have understood the problem rather than remembered the answer.

### Why the list must be doubly linked

Sudha's two nudges. To remove a jar from the middle of the row, you need to join its left neighbour
to its right neighbour. That means **from the jar itself you must be able to reach both neighbours**.

A **singly linked list** — where each node knows only the *next* one — cannot do that. Given a node,
you cannot find the one before it without walking from the start, which is O(n). A **doubly linked
list** gives each node a `prev` and a `next`, so unlinking is:

```python
    node.prev.next = node.next
    node.next.prev = node.prev
```

Two assignments. Constant time, whatever the size of the list. That is the second reason the pattern
works, and it is the answer to the follow-up "why not a singly linked list?"

You will meet linked lists properly from [day 078](../day-078-nodes-and-links/README.md) onwards.
Everything you need today is in those two lines.

### The two ends

Pick an orientation and stick to it, because mixing them up mid-solution is how this problem gets
lost:

```
 head  <->  most recently used  ...  least recently used  <->  tail
```

- `get(key)` — find the node through the map, **move it to the head**, return its value.
- `put(key, value)` — if the key exists, update the value and move it to the head. Otherwise create a
  node, add it at the head, put it in the map, and **if the size now exceeds capacity, remove the
  node before the tail** and delete its key from the map.

### The sentinel nodes that remove every special case

The awkward part of linked-list code is the ends: inserting into an empty list, removing the only
node, removing the first node. Each is a separate `if`, and each is a chance to get it wrong.

The fix is two permanent nodes that hold no data: a `head` and a `tail` that always exist. Real nodes
live strictly between them.

```
   head <-> A <-> B <-> C <-> tail
   (fake)   most            least   (fake)
```

Now the list is never empty from the code's point of view, `node.prev` is never `None`, and insert
and remove are the same three lines every time. These are **sentinel nodes**, the same idea as the
sentinel bar on [day 072](../day-072-largest-rectangle/README.md), and the dummy head you will use
for the whole of the linked-list phase from [day 080](../day-080-dummy-head/README.md).

Write the sentinels first. It turns a fiddly problem into a mechanical one.

### The one line people forget

**`get` is a write.** Reading an entry changes the cache, because it moves that entry to the front.
A `get` that does not move the node is a cache that evicts things you have been using constantly, and
it passes every test that only checks returned values. Say it out loud while you write it.

### What you would actually use

Python's `OrderedDict` is a dictionary with exactly this structure inside it, and it exposes the move:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self._store: OrderedDict[int, int] = OrderedDict()
        self._capacity = capacity

    def get(self, key: int) -> int:
        if key not in self._store:
            return -1
        self._store.move_to_end(key)              # mark as most recent
        return self._store[key]

    def put(self, key: int, value: int) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self._capacity:
            self._store.popitem(last=False)       # drop the least recent
```

Twelve lines, all O(1). Since Python 3.7 a plain `dict` also keeps insertion order, so a `dict` plus
`del` and re-insert works too. And `functools.lru_cache` is this, applied to function results.

**Build the linked list version in the interview, then say this exists.** The interviewer is testing
whether you know what is inside `OrderedDict`, not whether you can import it.

---

## 4. The picture

Capacity 3. `put(A,1)`, `put(B,2)`, `put(C,3)`, then `get(A)`, then `put(D,4)`.

```
 after put A, B, C          the map points into the list, so no searching

   map:  A -> [A]   B -> [B]   C -> [C]

   head <-> C <-> B <-> A <-> tail
   (fake)  MRU              LRU  (fake)


 get(A)  ->  find A through the map in O(1), unlink it, put it at the head

   unlink A:      B.next = tail ;  tail.prev = B        (Sudha's two nudges)
   insert at head: head <-> A <-> C ...

   head <-> A <-> C <-> B <-> tail
           MRU              LRU
   returns 1


 put(D,4)  ->  size would be 4 > 3, so evict the node before tail, which is B

   remove B from the list AND from the map        <- both, always
   insert D at the head

   map:  A -> [A]   C -> [C]   D -> [D]           B is gone from both

   head <-> D <-> A <-> C <-> tail
           MRU              LRU
```

What to notice: **`get(A)` changed the list.** After it, B is the least recently used rather than A,
which is why `put(D,4)` evicts B. If `get` had not moved A, the cache would have thrown away the
entry you had just asked for.

And the removal itself, drawn at the pointer level, because this is the part that gets written wrong:

```
 before:      ... <-> P <-> N <-> Q <-> ...
                          (the node to remove)

   P.next = N.next   ->   P.next = Q
   N.next.prev = N.prev   ->   Q.prev = P

 after:       ... <-> P <-> Q <-> ...

 N still points at P and Q, and nobody points at N. It is gone.
 Two assignments, no loop, no dependence on the list's length.
```

---

## 5. The code, built step by step

### Step 1 — the node

```python
class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None
```

The node stores the **key** as well as the value, and that is not redundant. When you evict the node
before the tail, you must also delete it from the map — and to do that you need its key. Leave the
key out and eviction becomes impossible without a scan. This is the single most common design slip in
this problem.

`__slots__` is a small optimisation: it stops each node carrying a dictionary of attributes, cutting
memory per node from about 200 bytes to about 90. Mention it, do not dwell on it.

### Step 2 — the sentinels

```python
        self._head = Node()          # fake, always the front
        self._tail = Node()          # fake, always the back
        self._head.next = self._tail
        self._tail.prev = self._head
```

Four lines that delete every edge case. The list is now never empty, `node.prev` is never `None` for
a real node, and the first insertion is the same code as the hundredth.

### Step 3 — unlink, in two assignments

```python
    def _unlink(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
```

Sudha's two nudges. No loop, no length check, no `if`. This works for any real node because the
sentinels guarantee both neighbours exist.

### Step 4 — insert at the head

```python
    def _push_front(self, node: Node) -> None:
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node        # the old first node points back at us
        self._head.next = node
```

Four assignments, and the **order matters**. Set the new node's two pointers first, then fix the
neighbours. Doing `self._head.next = node` too early loses your only reference to the old first node.

### Step 5 — get, which is also a write

```python
    def get(self, key: int) -> int:
        node = self._map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)             # a read makes it the most recent
        return node.value
```

Three lines of work and the middle two are the ones people forget.

### Step 6 — put, with the two cases kept apart

```python
    def put(self, key: int, value: int) -> None:
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value         # update in place
            self._unlink(existing)
            self._push_front(existing)
            return
```

Handle "the key is already here" first and return. Trying to merge the two cases into one branch is
where the bug lives — an existing key must not be inserted twice, and it must not count against the
capacity.

```python
        node = Node(key, value)
        self._map[key] = node
        self._push_front(node)

        if len(self._map) > self._capacity:
            oldest = self._tail.prev       # the node just before the fake tail
            self._unlink(oldest)
            del self._map[oldest.key]      # BOTH structures, always
```

`del self._map[oldest.key]` is the line that needs the key stored on the node. Removing from the list
but not the map leaves a dangling entry: a later `get` finds a node that is no longer in the list,
moves it to the front, and now the list and the map disagree for ever.

### The complete solution

```python
class Node:
    """One entry, doubly linked. It stores the KEY as well as the value,
    because eviction needs the key to delete the map entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    """Fixed-capacity cache that evicts the least recently used entry.

    Two structures, and neither can do the other's job:
      map  : key -> node, so lookup is O(1) with no searching
      list : doubly linked, most recent at the head, so eviction is O(1)

    Sentinel head and tail nodes hold no data and always exist, which removes
    every empty-list and first-node special case.

    IMPORTANT: get() is a write. Reading an entry moves it to the head.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity cannot be negative")
        self._capacity = capacity
        self._map: dict[int, Node] = {}
        self._head = Node()                    # fake front sentinel
        self._tail = Node()                    # fake back sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key: int) -> int:
        node = self._map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)                 # a read is a use
        return node.value

    def put(self, key: int, value: int) -> None:
        if self._capacity == 0:
            return                             # a cache that stores nothing

        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._unlink(existing)
            self._push_front(existing)
            return

        node = Node(key, value)
        self._map[key] = node
        self._push_front(node)

        if len(self._map) > self._capacity:
            oldest = self._tail.prev           # just before the fake tail
            self._unlink(oldest)
            del self._map[oldest.key]          # remove from BOTH structures

    def _unlink(self, node: Node) -> None:
        """Join the two neighbours to each other. Two assignments, O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: Node) -> None:
        """Put the node immediately after the head sentinel. Order matters."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def keys_most_recent_first(self) -> list[int]:
        """For testing and for drawing the list on a whiteboard."""
        keys, node = [], self._head.next
        while node is not self._tail:
            keys.append(node.key)
            node = node.next
        return keys


from collections import OrderedDict


class LRUCacheOrderedDict:
    """What you would write in production. OrderedDict is exactly a dict plus
    a doubly linked list, and move_to_end / popitem(last=False) are the moves."""

    def __init__(self, capacity: int) -> None:
        self._store: OrderedDict[int, int] = OrderedDict()
        self._capacity = capacity

    def get(self, key: int) -> int:
        if key not in self._store:
            return -1
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key: int, value: int) -> None:
        if self._capacity == 0:
            return
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self._capacity:
            self._store.popitem(last=False)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))                    # 1
    cache.put(3, 3)                        # evicts key 2 (least recently used)
    print(cache.get(2))                    # -1
    cache.put(4, 4)                        # evicts key 1
    print(cache.get(1))                    # -1
    print(cache.get(3), cache.get(4))      # 3 4

    order = LRUCache(3)
    for key in (1, 2, 3):
        order.put(key, key * 10)
    print(order.keys_most_recent_first())  # [3, 2, 1]
    order.get(1)
    print(order.keys_most_recent_first())  # [1, 3, 2]   <- get moved it
    order.put(4, 40)
    print(order.keys_most_recent_first())  # [4, 1, 3]   <- 2 was evicted

    print(LRUCache(0).get(1))              # -1, and put() does nothing

    # both implementations must agree on any sequence of operations
    import random
    for _ in range(2000):
        capacity = random.randint(1, 5)
        mine, reference = LRUCache(capacity), LRUCacheOrderedDict(capacity)
        for _ in range(40):
            key = random.randint(1, 8)
            if random.random() < 0.5:
                assert mine.get(key) == reference.get(key)
            else:
                value = random.randint(0, 99)
                mine.put(key, value)
                reference.put(key, value)
    print("linked-list and OrderedDict versions agreed on 2000 random sequences")
```

The random cross-check is the test that catches the two silent bugs: `get` not moving the node, and
eviction removing from only one structure. Both produce correct answers for a while and wrong ones
later, so a fixed script of eight calls will not find them.

---

## 6. What it costs

### Time

```
 get(key)
   dict lookup            O(1)
   unlink                 O(1)   two assignments
   push to front          O(1)   four assignments
   ------------------------------
   total                  O(1)

 put(key, value)
   dict lookup            O(1)
   create / update node   O(1)
   push to front          O(1)
   evict if over capacity O(1)   the node before the tail, then one dict delete
   ------------------------------
   total                  O(1)
```

Nothing loops. Nothing searches. Nothing depends on the capacity. Count the assignments out loud —
about six for a `get` and about ten for a `put` — because "O(1)" is more convincing when you can say
what the constant is made of.

Both are **worst case** O(1), not amortised, apart from the dictionary itself. Dictionary lookup is
O(1) average and O(n) in a pathological collision case, which is
[day 061](../day-061-collisions/README.md)'s material and worth one sentence if the interviewer is
being thorough.

### Against the alternatives

Capacity `c`, and `n` operations:

```
 dict + timestamp, scan to evict:   O(1) get, O(c) evict
 list, most recent at the front:    O(c) get (search), O(c) move
 dict + doubly linked list:         O(1) get, O(1) put

 c = 10,000 and 1,000,000 operations:
   scan-to-evict:  up to 10^10 comparisons
   this:           about 10^7 pointer writes
```

Three orders of magnitude, and the gap grows with the capacity — which matters because real caches
are large. A Redis instance holding ten million keys cannot afford anything that scans.

### Space

```
 per entry:
   Node with __slots__      about  90 B   (key, value, prev, next)
   Node without __slots__   about 200 B   (plus an instance dictionary)
   dict entry               about 100 B   (key, hash, pointer, and slack)
   ------------------------------------
   total with __slots__     about 190 B per entry
```

For a cache of 100,000 entries:

```
 100,000 × 190 B  ≈  19 MB   of overhead, before the values themselves
```

Say that number if asked about memory. It is why real caches with millions of entries are written in
C and store values as bytes — and why `functools.lru_cache` on a hot function with a large `maxsize`
can be a surprising amount of memory.

Space is **O(capacity)**, not O(n). The whole point of a cache is that it is bounded.

### The hit-rate arithmetic, which is the systems half of the question

A cache is only worth having if it hits. With a 100 µs database read and a 1 µs cache read:

```
 hit rate 90%:  0.90 × 1 µs + 0.10 × 100 µs = 10.9 µs average
 hit rate 50%:  0.50 × 1 µs + 0.50 × 100 µs = 50.5 µs average
 no cache:                                   100.0 µs
```

Ninety percent hits gives a **9× speed-up**; fifty percent gives 2×. Doubling the capacity usually
moves the hit rate by a few points, which is why capacity planning is measurement rather than
guesswork. If the interviewer turns the question from "implement it" to "would you use it", this is
the arithmetic they want.

---

## 7. The traps

### Trap 1 — `get` that does not move the node

```python
    def get(self, key: int) -> int:
        node = self._map.get(key)
        return node.value if node else -1        # no reordering
```

Every returned value is correct. Every eviction is wrong. The cache now evicts by *insertion* order
rather than *use* order, so the entry you read a thousand times gets thrown out while an entry
inserted once and never touched survives. On the standard LeetCode sequence it fails at the fourth
call; in production it shows up as a mysteriously poor hit rate.

**A read is a use.** Say it while you type it.

### Trap 2 — evicting from the list but not the map

```python
            oldest = self._tail.prev
            self._unlink(oldest)                 # forgot: del self._map[oldest.key]
```

The map keeps growing for ever, so the cache is no longer bounded — that alone is a memory leak. And
it is worse than a leak: a later `get` on the evicted key finds the node, pushes it back into the
list, and returns a value for an entry that was supposed to be gone. The two structures now disagree,
and every subsequent eviction is wrong.

**Every change touches both structures.** Make that a rule and check each method against it.

### Trap 3 — no key on the node

```python
class Node:
    __slots__ = ("value", "prev", "next")        # no key
```

Now `del self._map[oldest.key]` cannot be written. The usual patch is to scan the map for the value,
which is O(capacity) and makes the whole solution pointless. Store the key in the node. It costs eight
bytes and it is what makes eviction O(1).

### Trap 4 — treating an existing key as a new insert

```python
    def put(self, key: int, value: int) -> None:
        node = Node(key, value)
        self._map[key] = node                    # overwrites the map entry
        self._push_front(node)                   # old node is still in the list
        if len(self._map) > self._capacity:
            ...
```

The old node is still linked into the list and nothing points to it from the map. The list now has
more nodes than the map has keys, the size check is wrong, and eviction eventually unlinks the
orphan and tries `del self._map[key]` for a key whose map entry now belongs to the *new* node —
deleting a live entry.

```
KeyError: 3
```

is the friendly version of this bug. The silent version is worse. Handle "already present" as its own
branch with an early `return`.

### Trap 5 — using a singly linked list

Each node knows only `next`. Unlinking a node now requires the node *before* it, and finding that
means walking from the head — O(capacity). The whole solution degrades to O(n) per operation and the
interviewer will ask why.

If you are forced to use a singly linked list, the trick is to store `key -> previous node` in the
map instead, which works and is horrible. Say the doubly linked list and move on.

### Trap 6 — no sentinels, and the null checks that follow

Without a fake head and tail, `_unlink` needs `if node.prev is None` and `if node.next is None`,
`_push_front` needs a separate empty-list branch, and eviction needs a "was that the only node?"
check. Six extra branches, each one a chance to write:

```
AttributeError: 'NoneType' object has no attribute 'next'
```

It is the single most common runtime error in hand-written linked-list code. Two fake nodes remove
all of it.

### Trap 7 — capacity zero or one

`capacity = 0` should accept nothing. Without a guard, `put` inserts the node, finds `1 > 0`, and
immediately evicts... the node it just inserted, which happens to work, but only by accident and only
if `_tail.prev` is that node. Guard it explicitly.

`capacity = 1` is the case that catches ordering bugs: `put(1,1); put(2,2); get(1)` must return -1.
Run it.

### Trap 8 — assuming thread safety

Two threads calling `get` at the same time can interleave the pointer updates and corrupt the list —
one node pointing into a region no longer linked, or a cycle. Nothing raises; the cache just starts
returning wrong values or hangs in `keys_most_recent_first`. Real caches take a lock, or shard the
cache into 16 independent caches keyed by `hash(key) % 16` so that most operations do not contend.
Say this if asked "is this thread-safe?" — the answer is no, and the two fixes are worth naming.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Design an LRU cache with O(1) get and put."* LeetCode 146. Almost always
  stated with the O(1) requirement, which is the hint that one structure is not enough.
- The follow-up that is really a second question: *"Now make it LFU — least *frequently* used."*
  LeetCode 460, and it needs a third structure.
- The systems version: *"Your service reads the same user record thousands of times a second. What do
  you do?"* — the answer is this, plus a TTL, plus a hit-rate number.
- The concurrency version: *"Two threads use this cache at once. What breaks?"*

### What to say out loud, in the first ninety seconds

1. **State the requirement that forces the design.** "Both operations have to be O(1), including
   eviction. That immediately rules out any single structure, so let me say why."
2. **Reject each single structure, with its cost.** "A hash map gives me O(1) lookup but has no order,
   so finding the least recently used means scanning — O(capacity). A list gives me order but finding
   a key is a scan and moving an entry to the front shifts everything."
3. **Name the combination.** "So I use both: a hash map from key to *node*, and a doubly linked list
   holding the nodes in recency order, most recent at the head."
4. **Say why doubly.** "Doubly linked, because removing a node from the middle in O(1) means joining
   its two neighbours, and for that I need to reach both from the node itself. A singly linked list
   would need a walk to find the predecessor."
5. **Say the thing people forget, before writing it.** "`get` is a write — reading an entry moves it
   to the head. Otherwise I am evicting by insertion order, not by use."
6. **Mention sentinels as a decision.** "I will use fake head and tail nodes that always exist, which
   removes every empty-list and first-node special case."
7. **Say the eviction detail.** "The node stores its own key, because when I evict the node before
   the tail I have to delete it from the map too, and I need the key for that."

Then write it. With that said first, the code is fifteen minutes of typing and the interviewer
already knows you understand it.

### The follow-ups

**"Why does the node need to store the key?"**
"Because eviction starts from the list, not from the map. I find the node before the tail sentinel,
unlink it, and then I have to remove its entry from the map — and the only thing I have at that
moment is the node. Without the key on it, I would have to scan the map for a matching node, which
is O(capacity) and destroys the whole design."

**"Why not a singly linked list?"**
"Removing a node in O(1) needs to join the node before it to the node after it. With only `next`
pointers, finding the node *before* a given node means walking from the head, which is O(capacity).
There is a workaround — map each key to its *predecessor* — but it is fiddly and buys nothing. The
extra pointer is eight bytes per entry and it makes the operation two assignments."

**"Is `get` really a mutation?"**
"Yes, and it is the line most people leave out. If `get` does not move the entry to the head, the
cache evicts in insertion order rather than use order, so the hot entry you read a thousand times
gets thrown away while a cold one survives. Every returned value is still correct, which is why it
passes naive tests — the damage only shows up in the eviction sequence and, in production, as a bad
hit rate."

**"Make it LFU instead."**
"Least frequently used needs a third structure, because now I have to find the smallest *count*
in O(1). The standard answer is a map from key to node, a map from frequency to a doubly linked list
of the nodes with that frequency, and a running `min_frequency` integer. On access, the node moves
from list `f` to list `f+1`; if list `f` becomes empty and `f` was the minimum, the minimum increases
by exactly one — that is what keeps it O(1). Eviction takes the tail of the `min_frequency` list.
The honest caveat is that plain LFU never forgets: an entry that was hot yesterday holds a huge count
and refuses to leave, so real implementations use a decay or a window."

**"Is this thread-safe?"**
"No. Two threads can interleave the pointer updates and leave the list with a node linked from one
side only, or a cycle — and nothing raises, it just returns wrong values or hangs. The simple fix is
one lock around both operations, which serialises everything and becomes the bottleneck. The usual
production fix is sharding: sixteen independent caches keyed by `hash(key) % 16`, each with its own
lock, so contention drops by roughly the number of shards. Java's `ConcurrentHashMap` and Caffeine do
essentially that."

**"What would you use in production?"**
"`OrderedDict` in Python, which *is* a dict plus a doubly linked list — `move_to_end` and
`popitem(last=False)` are exactly these two operations — or `functools.lru_cache` for memoising a
function. For a shared cache across processes, Redis with `maxmemory-policy allkeys-lru`, which
approximates LRU by sampling a handful of keys rather than maintaining an exact order, because at ten
million keys the exact bookkeeping costs more than the accuracy is worth. Naming that approximation
is worth doing — it shows the difference between the interview answer and the production one."

**"How do you know the capacity is right?"**
"Measure the hit rate. With a 100 microsecond database read and a 1 microsecond cache read, ninety
percent hits gives about 11 microseconds average — a ninefold improvement — while fifty percent gives
about 50 microseconds, which is only twofold. So I would instrument hits and misses, plot hit rate
against capacity, and stop where the curve flattens. Doubling memory for two points of hit rate is
usually a bad trade."

### A model answer

Asked: *design an LRU cache with O(1) get and put.*

> "The requirement that decides the design is that eviction also has to be O(1). That rules out any
> single data structure, so let me say why before I choose.
>
> A hash map gives me O(1) lookup, but a dictionary has no notion of order, so 'which entry has been
> untouched longest' means storing a timestamp with each value and scanning every entry — O(capacity)
> per eviction. A list in recency order gives me eviction for free, take the last one, but finding a
> key means scanning, and moving an entry from the middle to the front means shifting everything
> after it.
>
> So I use both, and the trick is that the map points *into* the list. A dictionary from key to node,
> and a doubly linked list of those nodes with the most recently used at the head and the least
> recently used at the tail. The map answers 'where is it' in constant time; the list answers 'which
> is oldest' in constant time; neither can do the other's job.
>
> Doubly linked specifically, because removing a node from the middle in constant time means joining
> its left neighbour to its right neighbour, and to do that I have to reach both from the node itself.
> With only forward pointers I would have to walk from the head to find the predecessor, which is
> linear.
>
> Two decisions I would make before writing a line. First, sentinel nodes: a fake head and a fake tail
> that always exist and hold no data, with the real nodes strictly between them. That removes every
> empty-list and first-node special case, and those special cases are where linked-list code goes
> wrong — you end up with `AttributeError: 'NoneType' object has no attribute 'next'`. Second, the
> node stores its own key as well as its value. That looks redundant until eviction: I find the node
> before the tail, unlink it, and then I have to delete it from the map, and the key is the only way
> to do that.
>
> Now the operations. `get` looks the key up in the map, and — this is the line people leave out —
> **moves the node to the head**, because a read is a use. If I skip that, every value I return is
> still correct but the cache evicts by insertion order instead of use order, so the entry I read a
> thousand times gets thrown out while a cold one survives. It passes a naive test and produces a
> terrible hit rate in production.
>
> `put` has two cases and I keep them apart. If the key already exists, update the value, move it to
> the head, and return — it must not be inserted twice and it must not count against the capacity. If
> it does not exist, create the node, add it to the map, push it to the head, and then, if the size
> now exceeds capacity, take the node just before the tail sentinel, unlink it, and delete its key
> from the map. Both structures, every time — removing from one and not the other is the bug that
> makes the map grow without bound and lets a later `get` resurrect an evicted entry.
>
> Everything is O(1) worst case: about six pointer writes for a get and ten for a put, no loops, and
> nothing that depends on capacity. Space is O(capacity), which is the point of a cache — roughly 190
> bytes of overhead per entry in Python with `__slots__`, so a hundred thousand entries is about
> nineteen megabytes before the values themselves.
>
> Two things I would say at the end. In production I would use `OrderedDict`, which is exactly this
> structure with `move_to_end` and `popitem(last=False)`, or Redis with an LRU eviction policy — and
> Redis actually *approximates* LRU by sampling a few keys, because at ten million keys exact
> bookkeeping costs more than the accuracy is worth. And this implementation is not thread-safe: two
> threads interleaving the pointer updates can leave the list corrupt with no exception raised. The
> fix is a lock, and the fix for the lock being a bottleneck is sharding into sixteen independent
> caches by key hash."

---

## 9. Recall card

- **One structure cannot do it, and saying why is the first ninety seconds.** A hash map has **no
  order** (finding the LRU is an O(capacity) scan); a list has **no lookup** (finding a key is a
  scan, moving it shifts everything). So: **map from key → node**, plus a **doubly linked list** of
  nodes, **most recent at the head**.
- **Doubly linked, because unlinking is two assignments** — `node.prev.next = node.next` and
  `node.next.prev = node.prev` — and that needs both neighbours reachable *from the node*. A singly
  linked list must walk to find the predecessor: O(capacity).
- **Two things everyone forgets. `get` is a write** — it moves the node to the head, or you evict by
  insertion order and the hot entry gets thrown away while returning correct values. **The node stores
  its own key**, because eviction starts from the list and must then `del map[node.key]` — **every
  change touches both structures.**
- **Write the sentinels first.** A fake head and fake tail that always exist delete every empty-list
  and first-node branch, and with them `AttributeError: 'NoneType' object has no attribute 'next'`.
  Keep `put`'s two cases apart with an early `return` on the existing key. Test `capacity = 1` and
  `capacity = 0`.
- **All O(1) worst case, ~6 writes per get and ~10 per put; space O(capacity)** — about **190 B per
  entry** in Python, so 100,000 entries ≈ **19 MB** of overhead. In production: **`OrderedDict`**
  (`move_to_end`, `popitem(last=False)`), `functools.lru_cache`, or Redis `allkeys-lru`, which
  **approximates** LRU by sampling. **Not thread-safe** — one lock, or shard by `hash(key) % 16`.
  LFU needs a **third** structure plus a `min_frequency` counter.
