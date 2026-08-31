---
day: 73
track: dsa
title: "Queues: first in, first out"
phase: "Stacks and queues"
status: written
---

# Day 073 · DSA — Queues: first in, first out

**After today you can:** You can implement a queue with O(1) enqueue and dequeue and say why a list is wrong.

**The interviewer asks it as:** *Implement a queue. Why not just use a list and pop(0)?*

---

## 1. What this is, and why they ask it

A **queue** is a collection where things come out in the order they went in. You add at one end and
remove from the other. First in, first out — **FIFO** — which is the exact opposite of the stack from
[day 068](../day-068-stacks/README.md), where the last thing in comes out first.

There are only four operations and none of them searches: **enqueue** (add at the back), **dequeue**
(remove from the front), **peek** (look at the front without removing), and **is empty**. All four
must be O(1). If any of them is O(n), you have not built a queue, you have built a list with
inconvenient method names.

They ask it because the obvious Python implementation is wrong in a way that is invisible in testing
and catastrophic in production. `queue = []`, `queue.append(x)` to add, `queue.pop(0)` to remove — it
looks right, it passes every small test, and it is O(n) per removal, which makes any loop over it
O(n²). At a hundred thousand elements that is ten seconds instead of three milliseconds, measured
below. The follow-up — "why not a list?" — is the actual question, and it is asked because the answer
requires you to know what an array is in memory, which is [day 009](../day-009-what-an-array-is/README.md).
Queues also underpin breadth-first search, level-order tree traversal, and every rate limiter and job
runner you will ever design, so this is a foundation day, not a trivia day.

---

## 2. The story

The sub-registrar's office opens at ten and Ramesh gets there at twenty past nine, which he has
learned is the only way.

For years it worked one way. You joined the line at the door and you stood in it. The line ran along
the wall, out past the notice board, and on a Monday it went down the steps and into the car park.
When the clerk finished with somebody, that person walked away, and then every single person in the
line took one step forward. Sixty people, one step each, for one person served. Then it happened
again. And again.

Ramesh hated it, and not because of the walking. It was that the line stopped being a line. Somebody
would step out to take a call and someone behind would close the gap. Two brothers would arrive and
one would join at the back and the other would drift up to the front to "just ask something". By
eleven o'clock nobody could say who was ahead of whom, and there were arguments almost every day.

Then last April they put in the machine by the door and the screen above the counter.

Now Ramesh walks in, presses the button, and the machine gives him a small printed number — 47 on the
day he tells this story. He sits down on the bench. The screen says 31. When the clerk finishes, the
screen changes to 32, and one person stands up and walks to the counter. Nobody else moves at all.
Sixty people sit still while the number goes up by one.

The machine keeps handing out numbers going up — 48, 49, 50 — and the screen keeps calling numbers
going up — 32, 33, 34. Two numbers, one at each end, and they never touch each other. The gap between
them is how many people are waiting.

What Ramesh noticed, sitting there with 47 in his hand, is that the amount of work per person served
has changed completely. Before, serving one person cost sixty people one step each. Now it costs one
number changing on a screen. And nobody argues any more, because the number in your hand says exactly
when you arrived and there is nothing to argue about.

---

## 3. The idea in plain English

The old line and the new machine are the same queue. First in, first out, both times. What changed is
the **cost of serving one person**, and that is the whole lesson.

### The four operations

- **enqueue(x)** — a new person takes a number. Add at the back.
- **dequeue()** — the screen calls the next number. Remove from the front and return it.
- **peek()** — who is next, without calling them.
- **is_empty()** — has everyone been served?

All four are O(1) in a correct implementation. "O(1)" means the work does not depend on how many
people are waiting: sixty or six thousand, the screen still changes one number.

### Why `list.pop(0)` is the old line

A Python list is a block of slots laid out one after another in memory, exactly as in
[day 009](../day-009-what-an-array-is/README.md). The list knows where its first slot is. `pop(0)`
removes the first element — and then every remaining element has to move one slot to the left, so
that the first element is at slot 0 again. Sixty people, one step each.

That is O(n) per removal. Empty a queue of `n` elements and you have done `n + (n−1) + (n−2) + … + 1`
moves, which is `n²/2`. The measurement in §6 is 10.2 seconds for a hundred thousand elements against
0.0034 seconds for the right structure.

`append` and `pop()` at the *end* are fine, which is why the stack works with a plain list. **The end
is the cheap end.** The front is the expensive one, and a queue lives at the front.

### The first fix: stop shuffling, keep a head marker

Do not remove the element. Leave it where it is and remember where the front now starts.

```python
    front = 0
    def dequeue():
        value = items[front]
        front += 1              # move the marker, not the data
        return value
```

That is the screen. Dequeue is now O(1). But there is a new problem: the slots before `front` are
dead and never reused, so the list grows for ever. A queue that handles a million jobs holds a
million dead slots. That is a memory leak with extra steps.

### The second fix: let the numbers wrap around

Fix the number of slots at, say, 8, and let both markers wrap around to 0 when they run off the end.
That is a **circular buffer**, also called a **ring buffer**: a fixed block of slots where position
`7 + 1` is position `0`.

```python
    self.tail = (self.tail + 1) % self.capacity
```

The `% capacity` is the wrap. Now nothing is ever shuffled and nothing is ever leaked, because slots
are reused as they are freed. This is how real fixed-size queues are built — network card buffers,
audio buffers, log ring buffers — and it is the implementation an interviewer means when they say
"implement a queue with an array".

**The one hard part** is telling *full* from *empty*. When `head == tail`, is the buffer empty or
completely full? Both look identical. Two standard answers: keep a separate `size` counter, or leave
one slot permanently unused so `head == tail` can only mean empty. Keep the counter — it is one
integer and it makes `is_empty`, `is_full` and `__len__` trivial.

### The third fix, and the one you actually use

`collections.deque` — a **double-ended queue**, pronounced "deck". It supports `append`, `appendleft`,
`pop` and `popleft`, all O(1). You have already met it in passing on
[day 031](../day-031-fixed-window/README.md).

```python
from collections import deque

queue = deque()
queue.append("a")        # enqueue at the back
queue.append("b")
first = queue.popleft()  # dequeue from the front -> "a"
```

Internally it is a doubly linked list of fixed-size blocks, so growing at either end never moves
existing elements. That is why both ends are cheap. **In an interview: build the array version to
show you understand it, then say "in real code I would use `collections.deque`."**

One structure you should be able to reject by name: `queue.Queue`. It exists for passing work between
threads and takes a lock on every operation, which makes it about **48 times slower** than a `deque`
in a single-threaded program, measured below. Correct answer, wrong question.

### Where queues turn up

- **Breadth-first search** on a graph or a grid, and **level-order traversal** of a tree. Both are
  "visit everything one distance away, then everything two away", and that is a queue. This is why
  today matters far beyond today.
- **Job runners and message brokers.** RabbitMQ and SQS are queues with durability bolted on.
- **Rate limiters and buffers** — a fixed-size ring that drops the oldest when full.
- **Sliding-window maximum**, tomorrow, which needs both ends and therefore a deque.

---

## 4. The picture

The two markers, and the gap between them. Slots along the top, values underneath.

```
 capacity 8, after enqueuing A B C D E and dequeuing A B

 slot     0     1     2     3     4     5     6     7
        +-----+-----+-----+-----+-----+-----+-----+-----+
 value  |  .  |  .  |  C  |  D  |  E  |  .  |  .  |  .  |
        +-----+-----+-----+-----+-----+-----+-----+-----+
                       ^                 ^
                     head              tail
                  (next out)        (next slot in)

 size = 3        the gap between the markers is who is waiting
```

What to notice: `head` moved right without anything else moving. Slots 0 and 1 hold rubbish and
nobody cares. That is the screen going from 31 to 33 while sixty people sit still.

Now enqueue F, G, H and watch `tail` fall off the end and come back:

```
 after F, G at slots 5, 6, then H wraps to slot 7 then 0

 slot     0     1     2     3     4     5     6     7
        +-----+-----+-----+-----+-----+-----+-----+-----+
 value  |  I  |  .  |  C  |  D  |  E  |  F  |  G  |  H  |
        +-----+-----+-----+-----+-----+-----+-----+-----+
           ^           ^
         tail        head

 size = 7        tail is now to the LEFT of head, and that is fine
```

What to notice: `tail < head` now, and the queue is still perfectly ordered — C, D, E, F, G, H, I.
The order is defined by walking forward from `head` with wraparound, not by slot number. This is the
picture people fail to draw, and then they write `while head < tail` and it breaks.

And the state that needs the size counter:

```
 head == tail == 2   with size 0  ->  EMPTY
 head == tail == 2   with size 8  ->  FULL

 identical markers, opposite meanings. Hence the counter.
```

---

## 5. The code, built step by step

### Step 1 — the version to write down and then reject

```python
class SlowQueue:
    def __init__(self) -> None:
        self._items: list[int] = []

    def enqueue(self, value: int) -> None:
        self._items.append(value)        # O(1), fine

    def dequeue(self) -> int:
        return self._items.pop(0)        # O(n) — every element shifts left
```

Say out loud what is wrong before the interviewer says it: "`pop(0)` moves every remaining element
one slot left, so it is O(n), and draining the queue is O(n²)."

### Step 2 — the head marker

```python
    def dequeue(self) -> int:
        value = self._items[self._head]
        self._items[self._head] = None   # release the reference
        self._head += 1
        return value
```

Dequeue is O(1) now. Setting the slot to `None` matters in Python: without it the list keeps a
reference to the object and the garbage collector cannot free it, so a queue of large objects holds
all of them alive for ever.

The remaining problem is that `self._items` never shrinks. A fix is to rebuild the list when the dead
prefix gets big:

```python
        if self._head > 64 and self._head * 2 > len(self._items):
            self._items = self._items[self._head:]     # amortised compaction
            self._head = 0
```

Copying is O(n), but it only happens when at least half the list is dead, so the cost spreads out to
O(1) per operation on average. That is **amortised**, the same argument as list growth from
[day 005](../day-005-python-lists-and-tuples/README.md). It works, and it is more code than the ring
buffer for the same result.

### Step 3 — the ring buffer, which is what they mean

```python
class RingQueue:
    def __init__(self, capacity: int) -> None:
        self._items: list[object | None] = [None] * capacity
        self._capacity = capacity
        self._head = 0          # index of the front element
        self._tail = 0          # index of the next free slot
        self._size = 0          # how many are in it — full/empty needs this
```

Four fields. The `_size` counter is not optional bookkeeping; it is what separates full from empty
when the two markers coincide.

```python
    def enqueue(self, value: object) -> None:
        if self._size == self._capacity:
            raise OverflowError("queue is full")
        self._items[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity      # wrap
        self._size += 1
```

Three lines: write, advance with wrap, count. The `% self._capacity` is the only clever thing in the
class, and it is the thing to say out loud: "position capacity − 1 plus one is position zero".

```python
    def dequeue(self) -> object:
        if self._size == 0:
            raise IndexError("dequeue from an empty queue")
        value = self._items[self._head]
        self._items[self._head] = None                      # release the reference
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value
```

The mirror image. Read, clear, advance with wrap, count down.

### Step 4 — growing when it fills

A fixed capacity is sometimes exactly what you want — a buffer that drops the oldest when full. If
you want it unbounded, double the capacity and **unroll the ring** while copying:

```python
    def _grow(self) -> None:
        bigger: list[object | None] = [None] * (self._capacity * 2)
        for i in range(self._size):
            bigger[i] = self._items[(self._head + i) % self._capacity]
        self._items, self._capacity = bigger, self._capacity * 2
        self._head, self._tail = 0, self._size
```

The loop walks forward from `head` with wraparound, which is the only correct way to read a ring in
order. Copying straight from slot 0 would give you the wrong order whenever `tail < head` — the
picture in §4 shows exactly that case.

### The complete solution

```python
from collections import deque


class RingQueue:
    """A FIFO queue on a fixed block of slots, with both markers wrapping around.

    All four operations are O(1). Nothing is ever shifted; only the two markers
    move. `_size` is what distinguishes full from empty when they coincide.
    """

    def __init__(self, capacity: int = 8) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._items: list[object | None] = [None] * capacity
        self._capacity = capacity
        self._head = 0          # slot of the front element
        self._tail = 0          # next free slot
        self._size = 0

    def enqueue(self, value: object) -> None:
        if self._size == self._capacity:
            self._grow()
        self._items[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> object:
        if self._size == 0:
            raise IndexError("dequeue from an empty queue")
        value = self._items[self._head]
        self._items[self._head] = None          # do not hold the object alive
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self) -> object:
        if self._size == 0:
            raise IndexError("peek at an empty queue")
        return self._items[self._head]

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def _grow(self) -> None:
        """Double the slots, unrolling the ring so the order survives."""
        bigger: list[object | None] = [None] * (self._capacity * 2)
        for i in range(self._size):
            bigger[i] = self._items[(self._head + i) % self._capacity]
        self._items = bigger
        self._capacity *= 2
        self._head = 0
        self._tail = self._size

    def __repr__(self) -> str:
        order = [self._items[(self._head + i) % self._capacity] for i in range(self._size)]
        return f"RingQueue({order})"


class DequeQueue:
    """The version you would actually write. collections.deque is a doubly
    linked list of blocks, so both ends are O(1) and nothing is ever shifted."""

    def __init__(self) -> None:
        self._items: deque[object] = deque()

    def enqueue(self, value: object) -> None:
        self._items.append(value)

    def dequeue(self) -> object:
        if not self._items:
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def peek(self) -> object:
        if not self._items:
            raise IndexError("peek at an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


def level_order(root: "Node | None") -> list[list[int]]:
    """Why queues matter: visit a tree one level at a time.

    The queue holds the nodes at the current distance from the root. Taking
    them all out and pushing their children gives the next distance.
    """
    if root is None:
        return []
    levels: list[list[int]] = []
    frontier: deque = deque([root])
    while frontier:
        this_level = []
        for _ in range(len(frontier)):          # exactly the current level
            item = frontier.popleft()
            this_level.append(item.value)
            if item.left:
                frontier.append(item.left)
            if item.right:
                frontier.append(item.right)
        levels.append(this_level)
    return levels


if __name__ == "__main__":
    q = RingQueue(capacity=4)
    for value in "ABCDE":                        # 5 into a capacity of 4: it grows
        q.enqueue(value)
    print(q)                                     # RingQueue(['A', 'B', 'C', 'D', 'E'])
    print(q.dequeue(), q.dequeue())              # A B
    q.enqueue("F")
    print(q, len(q), q.peek())                   # RingQueue(['C','D','E','F']) 4 C

    small = RingQueue(capacity=3)
    small.enqueue(1); small.enqueue(2); small.enqueue(3)
    print(small.dequeue(), small.dequeue())      # 1 2
    small.enqueue(4); small.enqueue(5)           # tail wraps past the end
    print(small)                                 # RingQueue([3, 4, 5])

    empty = RingQueue()
    print(empty.is_empty())                      # True
    try:
        empty.dequeue()
    except IndexError as error:
        print(f"IndexError: {error}")            # IndexError: dequeue from an empty queue
```

Write `RingQueue` when asked to implement a queue. Then say the last sentence: "in production I would
use `collections.deque`, because it does this and handles growth for me."

---

## 6. What it costs

### The four operations

```
 enqueue   O(1)   write one slot, advance one marker
 dequeue   O(1)   read one slot, advance one marker
 peek      O(1)   one index
 is_empty  O(1)   one comparison
```

Nothing loops. Nothing searches. The `_grow` call is O(n), but it doubles the capacity, so `n`
enqueues cause at most `1 + 2 + 4 + … + n ≈ 2n` slot copies in total — **amortised O(1)** per
enqueue, exactly the argument for list growth.

Space is O(capacity), which is between `n` and `2n` slots for `n` elements — the price of doubling.

### The measurement that answers "why not a list?"

Draining a queue of 100,000 integers, on this machine:

```
 list, dequeue with pop(0)      10.203 s
 collections.deque, popleft      0.0034 s
 ------------------------------------------
 ratio                          about 3,000x
```

And the shape, which matters more than the ratio:

```
 n = 100,000  ->  10.20 s
 n = 200,000  ->  39.74 s        3.9x the time for 2x the input
```

**Doubling the input roughly quadrupled the time.** That is the signature of O(n²) and it is the
number to quote. It also means the problem gets worse the more successful your system is, which is
the worst possible failure shape.

Count it out: `pop(0)` shifts every remaining element left by one slot, so it is O(n). Doing that `n`
times is `n + (n−1) + … + 1 = n(n+1)/2`. At n = 100,000 that is five billion slot moves.

### And the structure that is correct but wrong here

```
 collections.deque, 100,000 in and out    0.0034 s
 queue.Queue,       100,000 in and out    0.1650 s
 ------------------------------------------------
 ratio                                    about 48x
```

`queue.Queue` acquires and releases a lock on every `put` and `get`, because it is built for handing
work between threads. In a single-threaded algorithm you are paying for synchronisation you do not
need. Know it exists, name it as the right tool for producer–consumer threads, and do not use it in a
coding round.

---

## 7. The traps

### Trap 1 — `pop(0)`, the whole reason this day exists

```python
    def dequeue(self):
        return self._items.pop(0)
```

No error. No warning. Correct output on every test you write by hand. Ten seconds instead of three
milliseconds at a hundred thousand elements, and quadratic growth after that. This is the single most
common performance bug in beginner Python, and `list.insert(0, x)` is its twin at the other end.

If you remember one thing from today: **the front of a Python list is the expensive end.**

### Trap 2 — full and empty look identical

```python
    def is_empty(self) -> bool:
        return self._head == self._tail          # WRONG without a size counter
```

Fill a capacity-4 ring with four elements. `tail` wraps around to equal `head`, and this reports the
full queue as empty. Then `dequeue` returns `None` or raises, depending on how you wrote it, and the
bug only appears when the buffer happens to fill exactly.

Two fixes. Keep `_size` — one integer, and `is_empty`, `is_full` and `len` all become trivial. Or
deliberately waste one slot so the buffer is "full" at `capacity − 1`, making `head == tail` mean
empty and only empty. The counter is clearer; say both, and say which you chose.

### Trap 3 — reading the ring in slot order

```python
    def __repr__(self):
        return f"RingQueue({[x for x in self._items if x is not None]})"
```

This looks reasonable and is wrong twice. It reports the wrong order the moment `tail < head` — the
second picture in §4 would print `I, C, D, E, F, G, H` instead of `C, D, E, F, G, H, I`. And it
silently drops any legitimate `None` you stored. Always walk `(head + i) % capacity` for `i` in
`range(size)`.

### Trap 4 — forgetting to clear the dequeued slot

```python
        value = self._items[self._head]
        self._head = (self._head + 1) % self._capacity      # slot still points at value
```

The queue works. The memory does not get freed, because the list still holds a reference to the
object. In a long-running job runner that has handled a million 2 KB messages, that is two gigabytes
of garbage that cannot be collected. One line fixes it: `self._items[self._head] = None`.

### Trap 5 — dequeuing from an empty queue

```python
        return self._items[self._head]           # no size check
```

On an empty `deque`-backed queue:

```
IndexError: pop from an empty deque
```

On a list-backed one:

```
IndexError: list index out of range
```

Both are unhelpful to a caller. Raise your own with a message that says what happened —
`IndexError("dequeue from an empty queue")` — and, more importantly, check for emptiness in the
*caller's* loop condition: `while frontier:` is how every BFS is written.

### Trap 6 — `while head < tail`

```python
        while self._head < self._tail:           # WRONG on a wrapped ring
```

Perfectly correct until `tail` wraps around, at which point `tail < head` and the loop does nothing.
The queue silently reports itself as empty while holding seven elements. Loop on `_size`, never on
the relationship between the markers.

### Trap 7 — using `queue.Queue` in a coding round

It is not incorrect, so nothing breaks. It is 48 times slower and it signals that you reached for the
first thing whose name matched. If threads come up, name it then — that is when it is the right
answer.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Implement a queue. What is the complexity of each operation?"* Usually
  followed immediately by *"why not just use a list and `pop(0)`?"*
- The constrained version: *"Implement a queue using a fixed-size array."* LeetCode 622, Design
  Circular Queue. This is the ring buffer, and the full-versus-empty question is the point of it.
- The applied version: *"Print a binary tree level by level."* LeetCode 102. The queue is the whole
  answer and they want to see you reach for it without prompting.
- The structural version, which is tomorrow and the day after: *"Implement a queue using only
  stacks"*, and *"find the maximum of every window of size k"*.

### What to say out loud, in the first ninety seconds

1. **Define it by the restriction.** "A queue is FIFO — I add at the back and remove from the front,
   and I never touch the middle. That restriction is why all four operations can be O(1)."
2. **Name the four operations and their costs immediately.** "Enqueue, dequeue, peek, is-empty, all
   O(1). If any of them is O(n) I have not built a queue."
3. **Kill the list version before they ask.** "The tempting implementation is a list with `append`
   and `pop(0)`, and it is wrong: `pop(0)` shifts every remaining element one slot left, so it is
   O(n), and draining the queue is O(n²). I measured it once — a hundred thousand elements took ten
   seconds against three milliseconds."
4. **Then give the fix, in order of sophistication.** "The first fix is to keep a head marker and
   never shift, which leaks the dead prefix. The proper fix is a ring buffer: fixed slots, both
   markers wrap with modulo, nothing ever moves."
5. **Flag the hard part yourself.** "The one subtlety is that `head == tail` means both empty and
   full, so I keep a size counter."
6. **Close with the real-world line.** "In production I would use `collections.deque`, which is a
   linked list of blocks so both ends are O(1). Not `queue.Queue` — that locks on every operation for
   thread safety I do not need here."

### The follow-ups

**"Why is `pop(0)` O(n)? Explain it in terms of memory."**
"A Python list is a contiguous block of slots, and the list object stores a pointer to the start plus
the length. Element `i` is found by adding `i` to the start address, and that arithmetic only works
if element 0 really is at the start. So removing the first element means moving all `n − 1` remaining
elements one slot left to restore that. Removing from the *end* moves nothing, which is why the same
list is a perfectly good stack."

**"How do you tell full from empty in a ring buffer?"**
"You cannot from the markers alone — both states have `head == tail`. Two standard answers. Keep an
explicit size counter, which is one integer and makes empty, full and length all trivial. Or waste
one slot so the buffer is considered full at `capacity − 1`, which makes `head == tail` mean empty
and only empty; that is what you do when memory for the counter genuinely matters, in an embedded
context. I would use the counter."

**"What happens when it fills up?"**
"That is a product decision, not a code decision, and I would ask. Three sensible behaviours: grow —
double the slots and unroll the ring while copying, which keeps enqueue amortised O(1). Reject — raise
or return false, which is what a bounded work queue should do so that back-pressure reaches the
producer. Or drop the oldest — overwrite at `head` and advance both markers, which is what a metrics
buffer or an audio buffer wants, because stale data is worthless."

**"Give me a real use for a queue."**
"Breadth-first search, and everything shaped like it. Level-order traversal of a tree is the same
code. The property I am relying on is that FIFO order visits everything at distance one before
anything at distance two, which is what makes BFS find shortest paths in an unweighted graph.
Outside algorithms: job runners, rate limiters, and the buffer on a network card, which is a ring
buffer exactly like this one."

**"Can you make it thread-safe?"**
"Wrap enqueue and dequeue in a lock, which is exactly what `queue.Queue` does — and that is why it is
about fifty times slower than a `deque` in a single thread. `deque`'s `append` and `popleft` happen to
be atomic in CPython because of the global interpreter lock, so a single-producer, single-consumer
`deque` is safe without a lock, but I would not rely on that in code that other people maintain."

### A model answer

Asked: *implement a queue, and tell me why you would not just use a list with `pop(0)`.*

> "A queue is first in, first out: I add at the back, remove from the front, and never touch the
> middle. The restriction is the point — because I only ever work at the two ends, every operation
> can be constant time. Enqueue, dequeue, peek and is-empty, all O(1). If any of those turns out to
> be O(n), I have not built a queue.
>
> Now, why not a list with `append` and `pop(0)`. A Python list is a contiguous block of slots, and
> the list holds the address of the start. Element `i` lives at start plus `i`, which only works if
> element 0 is genuinely at the start. So `pop(0)` has to move every remaining element one slot left
> to restore that, which is O(n). Draining a queue of n elements that way is n plus n−1 plus n−2 and
> so on, which is about n²/2 — five billion slot moves at a hundred thousand elements. I have
> measured it: a hundred thousand took about ten seconds, and two hundred thousand took forty. Double
> the input, quadruple the time. That is the signature of quadratic behaviour, and it is exactly the
> failure that only shows up once the system is busy.
>
> Appending at the end is fine, though, which is why the same list makes a perfectly good stack. The
> front is the expensive end; the back is not.
>
> The first fix is to stop shifting: leave the element where it is and keep a head marker that moves
> forward. Dequeue is O(1) now, but the slots before the marker are dead and the list grows for ever,
> so it leaks.
>
> The proper fix is a ring buffer. A fixed block of slots, a head marker for the front and a tail
> marker for the next free slot, and both wrap around with modulo capacity, so slot capacity−1 is
> followed by slot 0. Nothing is ever moved. Enqueue writes at the tail and advances it; dequeue reads
> at the head, clears that slot so the object can be collected, and advances the head.
>
> The subtlety worth flagging before you ask about it: when `head == tail`, the buffer is either
> completely empty or completely full and the markers cannot tell you which. I keep an explicit size
> counter, which makes empty, full and length all one comparison. The alternative is to waste one slot
> so full means `capacity − 1`, and I would only do that if the counter's memory genuinely mattered.
>
> If it needs to be unbounded, I grow by doubling — and when I copy, I have to walk forward from head
> with wraparound rather than copying slot by slot, or the order is wrong whenever tail is behind
> head. Doubling makes enqueue amortised O(1), the same argument as list growth.
>
> In production I would not write any of this. I would use `collections.deque`, which is a doubly
> linked list of fixed-size blocks, so growing at either end never moves anything and both ends are
> O(1). What I would not use is `queue.Queue` — it takes a lock on every operation for thread safety,
> and in a single-threaded program that costs about fifty times the runtime for nothing."

---

## 9. Recall card

- **A queue is FIFO: add at the back, remove from the front, never touch the middle** — and that
  restriction is *why* enqueue, dequeue, peek and is-empty are all **O(1)**. It is the mirror of the
  stack. Every **BFS** and every **level-order traversal** is a queue.
- **`list.pop(0)` is O(n) because a list is a contiguous block and element 0 must stay at the start**,
  so everything shifts left. Draining is **O(n²)**: measured **10.2 s vs 0.0034 s** at n = 100,000
  (~3,000×), and **n → 2n gave 3.9× the time**, which is the quadratic signature. The **back** of a
  list is the cheap end — same list, perfectly good stack.
- **The ring buffer is the answer they want:** fixed slots, `head` for the front, `tail` for the next
  free slot, both advanced with `(marker + 1) % capacity`. Nothing ever moves. **Clear the dequeued
  slot to `None`** or the objects are never collected.
- **`head == tail` means empty *and* full — keep a `_size` counter** (or waste one slot). Never loop
  on `head < tail`; it breaks the moment tail wraps. Read the ring in order with
  `(head + i) % capacity`, never by slot number. Growing = double and **unroll while copying**,
  amortised O(1).
- **In production: `collections.deque`** — a linked list of blocks, both ends O(1). **Not
  `queue.Queue`**, which locks on every operation and measured **48× slower** single-threaded; name it
  only when the question is producer–consumer threads.
