---
day: 85
track: dsa
title: "Doubly and circular linked lists"
phase: "Linked lists"
status: written
---

# Day 085 · DSA — Doubly and circular linked lists

**After today you can:** You can splice a node out in O(1) and say what the extra pointer costs.

**The interviewer asks it as:** *Why does an LRU cache use a doubly linked list?*

---

## 1. What this is, and why they ask it

A **doubly linked list** gives every node a second reference: `prev`, pointing back at the node before
it. That one extra field changes exactly one thing, and it is the thing that matters: **given a node,
you can remove it in O(1)**, because you can reach both of its neighbours and join them to each other.

In a singly linked list you cannot. From [day 079](../day-079-list-traversal/README.md), removing a
node requires the node *before* it, and finding that means walking from the head — O(n). The extra
pointer buys you the predecessor for free.

A **circular** list is a different, independent change: the last node points at the first instead of
at `None`. There is no end, so "keep going round" is the natural traversal, and there is no first or
last node to be a special case. The two ideas combine — a circular doubly linked list with one
sentinel is the cleanest list structure there is, and it is what Python's `collections.deque` and the
Linux kernel's `list_head` both are.

They ask it because you built an LRU cache on [day 076](../day-076-lru-cache/README.md) and used one
without being able to justify it in one sentence yet. The interviewer wants that sentence, plus an
honest account of what the second pointer costs — eight bytes a node, twice the pointer updates, and
twice as many chances to leave the list inconsistent.

---

## 2. The story

The courtyard game starts at about half past six, once it is cool enough, and it needs at least ten
children to be worth playing.

They stand in a ring holding hands and one of them, usually Divya because she is loudest, walks round
the outside counting. Every seventh child is out. The child who is out lets go, steps back, and sits
on the low wall to watch, and the two children either side of the gap take each other's hands. The ring
closes up. Divya carries on counting from wherever she had got to.

That last part is what makes the game work. Nobody stops. Nobody goes back to the beginning. There is
no beginning to go back to — it is a ring, so wherever Divya is standing is as good as anywhere else,
and the counting simply continues.

It takes about four seconds for the gap to close and it does not matter at all whether there are
nineteen children left or four.

Last year the younger ones tried to play it in a straight line instead, because there were only six of
them and a ring of six looked silly.

It went badly in a way that took them a while to understand. When a child in the middle was out and
stepped away, the child behind had nobody in front of her — she could not simply take the next hand,
because she did not know whose it was. She was holding the shoulder of somebody who had gone. The only
way to sort it out was to go to the front of the line and count along until they reached the gap, and
by then the counting had been lost and three of them were arguing about whose turn it was.

Divya watched this for one evening and told them to stand in a ring like everybody else.

Her small brother asked her afterwards why the line was harder, since it was the same children.

She said: in the ring you are holding two hands. You know who is on both sides of you, so when you go,
the two of them just take each other. In the line each of you was only holding the one in front. Nobody
knew who was behind them.

---

## 3. The idea in plain English

The children joining hands are the two pointer updates. The ring having no front is the circular
list. And the fact that the game never restarts is why round-robin problems want one.

### The node, with one more field

```python
class Node:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: int) -> None:
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None
```

One extra reference, eight more bytes. Everything below follows from it.

### Removal in O(1), which is the whole point

```python
    node.prev.next = node.next
    node.next.prev = node.prev
```

Two assignments. The child stepping back, and the two either side taking hands. **No walk, no length
check, no dependence on where the node is** — the same two lines whether the list holds three nodes or
three million.

Compare with the singly linked version, which needs the predecessor and therefore a walk:

```
 singly linked, given the node:   O(n)  — walk from the head to find `previous`
 doubly linked, given the node:   O(1)  — two assignments
```

**That is the LRU cache's entire reason.** The hash map hands you the node for a key in O(1); if
removing it were O(capacity) you would have gained nothing. The map answers *where*, the doubly linked
list answers *cheaply*, and neither works without the other.

### Insertion, and the order of the four assignments

```python
    def insert_after(node: Node, fresh: Node) -> None:
        fresh.prev = node
        fresh.next = node.next
        node.next.prev = fresh          # fix the neighbour BEFORE overwriting node.next
        node.next = fresh
```

Four assignments, and the order is not free. Set `node.next = fresh` first and you have lost your
reference to the old successor, so line three has nothing to fix. **Point the new node at both
neighbours first, then rewire the neighbours** — the same rule as the singly linked insertion on
[day 078](../day-078-nodes-and-links/README.md), now with twice as many links to get wrong.

The reliable habit: write the two assignments *into* the new node, then the two assignments *out of*
the neighbours.

### Sentinels, which stop being optional

With one direction, a missing `prev` was not a problem. With two, every operation touches both
neighbours, so an operation at either end has a `None` where a node should be — and you get the
phase's favourite error:

```
AttributeError: 'NoneType' object has no attribute 'prev'
```

The fix is the sentinel from [day 080](../day-080-dummy-head/README.md), used at **both** ends:

```
   head <-> A <-> B <-> C <-> tail
  (fake)                      (fake)
```

Now every real node has a real `prev` and a real `next`, `_unlink` and `_push_front` have no branches,
and inserting into an empty list is the same code as inserting into a full one. On
[day 076](../day-076-lru-cache/README.md) this was presented as a convenience. In a doubly linked list
it is closer to a requirement — the number of `None` checks it removes roughly doubles.

### Circular lists: no end, and no first

Make the last node point at the first and the first point back at the last, and the structure has no
boundary at all. Two consequences.

**Traversal must stop by counting or by comparison, never by `None`.**

```python
    node = start
    while True:
        visit(node)
        node = node.next
        if node is start:               # the only way to know you have been round
            break
```

`while node is not None` never terminates on a circular list. Every loop needs either a "have I come
back to where I started" test or a known count, and forgetting that is the standard way to hang a
program with no error message.

**There is no head to be special.** Round-robin scheduling, a music playlist on repeat, the players in
a card game, the turn order in a board game — all of them are "the next one, for ever", and a circular
list expresses that without a wrap-around branch.

The classic problem is the **Josephus problem**: `n` people in a ring, every `k`-th is removed until
one remains. It is the counting-out game, and with a circular doubly linked list it is a direct
simulation — walk `k − 1`, unlink in O(1), continue from where you are, no restart. That "continue
from where you are" is the property an array simulation has to fake with modular arithmetic.

### The combination, which is what real code uses

A **circular doubly linked list with one sentinel** is the standard industrial structure:

```
        +-----------------------------------+
        |                                   |
        v                                   |
   [sentinel] <-> [A] <-> [B] <-> [C] <-----+
```

The sentinel is both the head and the tail. `sentinel.next` is the first real node, `sentinel.prev`
is the last, an empty list is `sentinel.next is sentinel`, and **there is not a single `None` in the
structure**. Every insertion and removal is the same four or two assignments with no branches at all.

This is what the Linux kernel's `list_head` is, what Python's `collections.deque` is internally (a
circular doubly linked list of fixed-size blocks), and what a well-written LRU cache uses.

### What the second pointer costs, honestly

```
 memory:      +8 bytes per node (about +17% on a 48-byte node)
 writes:      2 per removal instead of 1; 4 per insertion instead of 2
 bugs:        every operation must maintain BOTH directions, and a list that is
              correct forwards and broken backwards looks completely fine until
              something walks the other way
```

That last one is the real cost. A singly linked list is either right or obviously wrong. A doubly
linked list can be **half right**, and the symptom appears far from the cause. Write an invariant
check — walk forward collecting nodes, walk backward collecting nodes, assert the reverse of one
equals the other — and run it after every operation in tests.

### When you do *not* want one

- **You only ever walk forwards.** Then `prev` is 17% more memory and twice the writes for nothing.
- **You only ever insert and remove at the front.** A singly linked list is a perfect stack.
- **Memory is tight and n is large.** Ten million nodes is 80 MB of `prev` pointers alone.

The recognition rule: **use a doubly linked list when something else hands you a node and you must
remove it in O(1).** That is the LRU cache, a scheduler removing a task it holds a handle to, and an
editor's undo list. If you are always searching for the node first, the search is O(n) anyway and the
second pointer buys nothing.

---

## 4. The picture

Removal, drawn at the pointer level — this is the diagram to reproduce in an interview.

```
 before:
        +-----+       +-----+       +-----+
   ...  |  P  | <---> |  N  | <---> |  Q  |  ...
        +-----+       +-----+       +-----+
                    the node to remove

   node.prev.next = node.next      ->   P.next = Q
   node.next.prev = node.prev      ->   Q.prev = P

 after:
        +-----+                     +-----+
   ...  |  P  | <-----------------> |  Q  |  ...
        +-----+                     +-----+

        +-----+
        |  N  |   still points at P and Q, but nothing points at it
        +-----+

 Two assignments. No loop. No length. Divya's two children taking hands.
```

Insertion, with the ordering that matters:

```
 insert F between P and Q

 RIGHT:   1. F.prev = P          (F now knows both neighbours)
          2. F.next = Q
          3. P.next.prev = F     ->  Q.prev = F
          4. P.next = F

 WRONG:   1. P.next = F          (Q is now unreachable from P)
          2. F.next = P.next     ->  F.next = F   — points at itself
          3. ...                     the rest of the list is gone

 Rule: write INTO the new node first, then rewire the neighbours.
```

The circular list with one sentinel, which is the shape to remember:

```
              +-------------------------------------------+
              |                                           |
              v                                           |
        [sentinel] <-> [A] <-> [B] <-> [C] <--------------+

   sentinel.next  ->  the first real node
   sentinel.prev  ->  the last real node
   empty list     ->  sentinel.next is sentinel
   no None anywhere, so no branch anywhere
```

And the traversal difference, because it is where circular lists bite:

```
 linear:     while node is not None:        ... terminates at the end
 circular:   while node is not None:        ... NEVER terminates

 circular, correct:
             start = node
             while True:
                 visit(node)
                 node = node.next
                 if node is start: break
```

---

## 5. The code, built step by step

### Step 1 — the two sentinels

```python
        self._head = Node()                 # fake
        self._tail = Node()                 # fake
        self._head.next = self._tail
        self._tail.prev = self._head
```

Four lines that delete every `None` check in the class. Write them before anything else, exactly as on
[day 076](../day-076-lru-cache/README.md).

### Step 2 — unlink, in two assignments

```python
    def _unlink(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None        # do not leave a dead node pointing in
```

The third line is optional for correctness and worth writing: a removed node that still points into
the list lets a caller who kept a reference walk back into a structure it is no longer part of, which
is a genuinely confusing bug.

### Step 3 — insert, into the new node first

```python
    def _insert_between(self, fresh: Node, left: Node, right: Node) -> None:
        fresh.prev, fresh.next = left, right      # into the new node
        left.next = fresh                         # then the neighbours
        right.prev = fresh
```

Taking `left` and `right` as parameters rather than computing them inside removes the ordering trap
entirely: both neighbours are captured before anything is overwritten. Every public insertion —
front, back, before, after — becomes a one-line call to this.

### Step 4 — the invariant check, which you should actually write

```python
    def _check(self) -> None:
        forwards, node = [], self._head.next
        while node is not self._tail:
            forwards.append(node.value)
            node = node.next
        backwards, node = [], self._tail.prev
        while node is not self._head:
            backwards.append(node.value)
            node = node.prev
        assert forwards == backwards[::-1], f"{forwards} vs {backwards[::-1]}"
        assert len(forwards) == self._size
```

**Walk both ways and compare.** This is the check that catches a list which is correct forwards and
broken backwards — the failure mode a singly linked list cannot have and this one can. Three lines of
assertion, and running it after every operation in a random test finds every pointer bug in minutes.

### Step 5 — the circular traversal

```python
    node = start
    while True:
        yield node
        node = node.next
        if node is start:
            break
```

Never `while node is not None`. On a circular list there is no `None` and that loop hangs with no
error at all.

### The complete solution

```python
class Node:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


class DoublyLinkedList:
    """A doubly linked list with sentinels at both ends.

    The one thing the extra pointer buys: given a node, remove it in O(1),
    because both neighbours are reachable from it. That is why an LRU cache
    uses one — the hash map answers WHERE, the list answers CHEAPLY.

    Two sentinels mean there is no None anywhere among the real nodes, so
    every operation is the same handful of assignments with no branches.
    """

    def __init__(self, values: list[int] | None = None) -> None:
        self._head = Node()                     # fake front
        self._tail = Node()                     # fake back
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in values or []:
            self.push_back(value)

    # ---- the two primitives -------------------------------------------

    def _insert_between(self, fresh: Node, left: Node, right: Node) -> Node:
        """Both neighbours are parameters, so nothing can be overwritten early."""
        fresh.prev, fresh.next = left, right
        left.next = fresh
        right.prev = fresh
        self._size += 1
        return fresh

    def _unlink(self, node: Node) -> int:
        """The whole reason for the second pointer. Two assignments, O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None            # no dangling links out of a dead node
        self._size -= 1
        return node.value

    # ---- the public operations ----------------------------------------

    def push_front(self, value: int) -> Node:
        return self._insert_between(Node(value), self._head, self._head.next)

    def push_back(self, value: int) -> Node:
        return self._insert_between(Node(value), self._tail.prev, self._tail)

    def insert_after(self, node: Node, value: int) -> Node:
        return self._insert_between(Node(value), node, node.next)

    def insert_before(self, node: Node, value: int) -> Node:
        return self._insert_between(Node(value), node.prev, node)

    def remove(self, node: Node) -> int:
        """O(1) — this is the operation a singly linked list cannot do."""
        return self._unlink(node)

    def pop_front(self) -> int:
        if not self._size:
            raise IndexError("pop from an empty list")
        return self._unlink(self._head.next)

    def pop_back(self) -> int:
        if not self._size:
            raise IndexError("pop from an empty list")
        return self._unlink(self._tail.prev)     # O(1), unlike a singly linked list

    def move_to_front(self, node: Node) -> None:
        """Unlink and re-insert. The LRU cache's `get`, in two calls."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node
        self._head.next = node

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def reversed_values(self) -> list[int]:
        """Proof that the backward links are maintained — walk the other way."""
        out, node = [], self._tail.prev
        while node is not self._head:
            out.append(node.value)
            node = node.prev
        return out

    def __repr__(self) -> str:
        return f"DoublyLinkedList({list(self)})"

    def _check(self) -> None:
        """Walk both ways and compare. Catches a list that is correct forwards
        and broken backwards — the failure a singly linked list cannot have."""
        forwards = list(self)
        backwards = self.reversed_values()
        assert forwards == backwards[::-1], f"{forwards} vs {list(reversed(backwards))}"
        assert len(forwards) == self._size, f"size {self._size}, chain {len(forwards)}"


class CircularList:
    """A circular doubly linked list with ONE sentinel, which is both head and
    tail. There is no None anywhere, so there are no branches anywhere.

    This is what the Linux kernel's list_head is, and what collections.deque
    is internally (over blocks rather than single elements).
    """

    def __init__(self, values: list[int] | None = None) -> None:
        self._sentinel = Node()
        self._sentinel.next = self._sentinel.prev = self._sentinel      # points at itself
        self._size = 0
        for value in values or []:
            self.push_back(value)

    def push_back(self, value: int) -> Node:
        fresh = Node(value)
        last = self._sentinel.prev
        fresh.prev, fresh.next = last, self._sentinel
        last.next = fresh
        self._sentinel.prev = fresh
        self._size += 1
        return fresh

    def remove(self, node: Node) -> int:
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node.value

    def is_empty(self) -> bool:
        return self._sentinel.next is self._sentinel     # the emptiness test

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        node = self._sentinel.next
        while node is not self._sentinel:
            yield node.value
            node = node.next

    def walk_from(self, start: Node, steps: int) -> Node:
        """Move `steps` forward, skipping the sentinel so it is invisible."""
        node = start
        for _ in range(steps):
            node = node.next
            if node is self._sentinel:
                node = node.next
        return node


def josephus(n: int, k: int) -> int:
    """n people in a ring, every k-th is eliminated. Return the survivor (1-based).

    A direct simulation: the ring closes in O(1) after each removal and the
    counting continues from where it stopped — no restart, no wrap-around
    arithmetic. Divya's game.

    O(n*k) time, O(n) space.
    """
    if n < 1 or k < 1:
        raise ValueError("n and k must be at least 1")

    ring = CircularList(list(range(1, n + 1)))
    current = ring._sentinel.next
    while len(ring) > 1:
        current = ring.walk_from(current, k - 1)     # step to the k-th
        following = current.next
        if following is ring._sentinel:
            following = following.next
        ring.remove(current)
        current = following                          # continue from where we are
    return next(iter(ring))


if __name__ == "__main__":
    lst = DoublyLinkedList([1, 2, 3, 4])
    print(lst, lst.reversed_values())            # [1,2,3,4]  [4,3,2,1]
    lst._check()

    node = lst.push_back(5)
    lst.push_front(0)
    print(lst, len(lst))                         # [0,1,2,3,4,5] 6
    lst._check()

    print(lst.remove(node))                      # 5   — O(1), given the node
    print(lst.pop_front(), lst.pop_back())       # 0 4
    print(lst)                                   # [1, 2, 3]
    lst._check()

    middle = lst._head.next.next                 # the node holding 2
    lst.move_to_front(middle)
    print(lst, lst.reversed_values())            # [2,1,3]  [3,1,2]
    lst._check()

    empty = DoublyLinkedList()
    print(len(empty), list(empty))               # 0 []
    try:
        empty.pop_front()
    except IndexError as error:
        print(f"IndexError: {error}")            # pop from an empty list

    ring = CircularList([1, 2, 3])
    print(list(ring), len(ring), ring.is_empty())    # [1,2,3] 3 False

    print(josephus(7, 3))                        # 4
    print(josephus(5, 2))                        # 3
    print(josephus(1, 5))                        # 1
    print(josephus(10, 1))                       # 10

    # the invariant check earns itself on random sequences
    import random
    for _ in range(2000):
        test = DoublyLinkedList()
        handles: list[Node] = []
        for _ in range(30):
            action = random.random()
            if action < 0.4:
                handles.append(test.push_back(random.randint(0, 99)))
            elif action < 0.7:
                handles.append(test.push_front(random.randint(0, 99)))
            elif handles:
                victim = handles.pop(random.randrange(len(handles)))
                test.remove(victim)
            test._check()
    print("forwards and backwards agreed on 2000 random sequences")
```

---

## 6. What it costs

### The operations, against a singly linked list

```
                                   singly        doubly
 remove, GIVEN the node            O(n)          O(1)     <- the whole point
 remove at the front               O(1)          O(1)
 remove at the back                O(n)          O(1)     <- with a tail reference
 insert before a given node        O(n)          O(1)
 insert after a given node         O(1)          O(1)
 walk forwards                     O(n)          O(n)
 walk backwards                    impossible    O(n)
```

Three rows changed from O(n) to O(1), and every one of them is "you already have the node". That is
the pattern: **the second pointer converts *having* a node into *being able to act* on it.**

### The price

```
 memory per node:
   singly, __slots__:   48 B   (value, next)
   doubly, __slots__:   56 B   (value, prev, next)
   -> +8 B, about +17%

 at 10,000,000 nodes:  +80 MB of prev pointers alone

 writes:
   removal:    1 assignment  ->  2
   insertion:  2 assignments ->  4
```

Seventeen percent more memory and twice the pointer writes. Neither is a reason to avoid it when you
need O(1) removal, and both are reasons not to use one when you do not.

### The cost that is not in the table

**A doubly linked list can be half correct.** Forward links right, backward links wrong. Iterating
forwards gives the right answer, `len` gives the right answer, every test passes — and then something
walks backwards, or removes a node, and the structure falls apart far from where the bug was
introduced.

A singly linked list has no such state: it is right, or it is visibly broken. That is the real cost of
the second pointer, and the mitigation is the `_check` above — walk both ways, compare, assert. Say
this in an interview; it is the kind of thing that comes from having debugged one.

### The LRU cache, priced

From [day 076](../day-076-lru-cache/README.md), with capacity `c`:

```
 with a doubly linked list:  get = map lookup + 2 writes + 4 writes  -> O(1)
 with a singly linked list:  get = map lookup + O(c) walk to find prev
   c = 100,000:  ~100,000 steps per get instead of about 6 writes
```

**Roughly ten thousand times more work per read**, and it would make the cache slower than the
database it was put in front of. That is the one-sentence answer to "why doubly linked".

### Circular lists

```
 memory:       identical to a linear doubly linked list
 traversal:    O(n) per lap, and there is no natural stopping point
 Josephus:     O(n*k) by direct simulation, O(n) space
               (the closed-form recurrence is O(n) time and O(1) space, and is
                a different solution rather than a better implementation)
```

The circular structure buys **no asymptotic improvement anywhere**. What it buys is the absence of
special cases: no first, no last, no wrap-around branch, no `None`.

---

## 7. The traps

### Trap 1 — updating only one direction

```python
    node.prev.next = node.next          # forgot: node.next.prev = node.prev
```

The list is now correct forwards and broken backwards. Iteration works. `len` works. Printing works.
And then a later `pop_back` or a backward walk finds a `prev` pointing at a node that was removed, and
the removed node comes back from the dead. **No error, and the symptom is nowhere near the cause.**

This is the defining bug of doubly linked lists and it is why `_check` exists.

### Trap 2 — insertion in the wrong order

```python
    left.next = fresh                   # WRONG FIRST
    fresh.next = left.next              # this is now `fresh` — points at itself
```

A node pointing at itself, and the rest of the list unreachable. The next traversal either hangs or
returns one element. **Write into the new node first, then rewire the neighbours** — or take both
neighbours as parameters, which makes it impossible.

### Trap 3 — `None` at the ends, without sentinels

```python
    node.prev.next = node.next          # node.prev is None for the first node
```

```
AttributeError: 'NoneType' object has no attribute 'next'
```

With two directions there are twice as many ends and twice as many branches to forget. Two sentinels
remove all of them, and in a doubly linked list that is closer to a requirement than a convenience.

### Trap 4 — `while node is not None` on a circular list

```python
    while node is not None:             # there is no None. This never ends.
        visit(node)
        node = node.next
```

No exception, no output, no end — the program simply stops responding, and if `visit` appends to a
list, it eventually dies of memory exhaustion instead. Circular traversal must compare against the
starting node or count.

### Trap 5 — the sentinel appearing in the output

```python
    for value in ring:                  # yields the sentinel's value too
```

The sentinel is not data. Every traversal must skip it, and every `walk_from` must step over it, or
your Josephus simulation eliminates a child who does not exist. Wrapping the traversal in `__iter__`
once — so no caller ever walks manually — is the fix.

### Trap 6 — forgetting that `remove` needs the node, not the value

```python
    lst.remove(5)                       # 5 is a value, not a node
```

The O(1) guarantee is *given the node*. If the caller has a value, finding the node is an O(n) search
and the whole advantage is gone. This is why the LRU cache keeps a map from key to node, and why the
API here takes a `Node` — making the caller hold handles is a deliberate design decision, not an
oversight.

### Trap 7 — a removed node still pointing into the list

```python
    node.prev.next = node.next
    node.next.prev = node.prev
                                        # node.prev and node.next still set
```

A caller who kept a reference can now walk from a removed node back into the live list, and in an LRU
cache a stale node can be moved to the front, silently resurrecting an evicted entry. One line —
`node.prev = node.next = None` — closes it.

### Trap 8 — using one when you only ever walk forwards

Seventeen percent more memory, twice the writes, and a whole class of half-correct states, in exchange
for nothing. If you never remove a node you already hold, and never walk backwards, a singly linked
list is strictly better. Say the recognition rule rather than reaching for the fancier structure.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Why does an LRU cache use a doubly linked list?"* — a one-sentence answer with
  a number attached.
- The comparison: *"What does the extra pointer cost you?"*
- The implementation: *"Implement a doubly linked list with insert, delete and reverse traversal."*
- The circular version: *"n people stand in a circle and every k-th is eliminated. Who survives?"* —
  the Josephus problem.
- The real-world probe: *"Where have you seen one of these?"* — `collections.deque`, the Linux kernel,
  a browser's history, a music playlist.

### What to say out loud, in the first ninety seconds

1. **Name the one thing it buys.** "The second pointer buys exactly one operation: given a node, remove
   it in O(1), because I can reach both neighbours and join them to each other."
2. **Say what it replaces.** "In a singly linked list I would need the node before it, which means
   walking from the head — O(n)."
3. **Give the LRU sentence with the number.** "That is why the LRU cache uses one. The map gives me the
   node in O(1); with a singly linked list, removing it would be O(capacity), so at a hundred thousand
   entries a read would be a hundred thousand steps instead of about six writes."
4. **Say the sentinels are not optional here.** "I use fake head and tail nodes, because with two
   directions there are twice as many ends and twice as many `None` checks to forget."
5. **State the cost honestly.** "Eight bytes a node, about seventeen percent, and twice the pointer
   writes. And the real cost is that the list can be half correct — right forwards and broken
   backwards — which a singly linked list cannot be. I would write an invariant check that walks both
   ways and compares."

### The follow-ups

**"Why does an LRU cache need a doubly linked list?"**
"Because the hash map hands me the node directly, and unlinking it must be O(1) or the map's O(1)
lookup is wasted. Unlinking needs both neighbours joined to each other, and reaching the predecessor
from a node is exactly what the `prev` pointer gives me. With a singly linked list I would have to walk
from the head to find the predecessor — O(capacity) — so at a hundred thousand entries every read
becomes a hundred-thousand-step walk. The map answers *where*; the doubly linked list answers
*cheaply*."

**"What does the extra pointer cost?"**
"Eight bytes per node, which is about seventeen percent on a small node, and eighty megabytes at ten
million nodes. Twice the pointer writes: two per removal instead of one, four per insertion instead of
two. And the cost that does not show up in a table — the list can be correct in one direction and
broken in the other, so it passes every forward test and falls apart later, somewhere else. A singly
linked list cannot be half right. That is why I would write a check that walks both ways and asserts
the reverse of one equals the other, and run it after every operation in tests."

**"What is a circular list good for?"**
"Anything that is 'the next one, for ever' with no natural end — round-robin scheduling, a playlist on
repeat, turn order in a game, a ring buffer. The structural benefit is the absence of special cases:
no first node, no last node, no wrap-around branch, and with a single sentinel there is no `None`
anywhere, so insertion and removal have no branches at all. That is exactly what the Linux kernel's
`list_head` is. The trap is that `while node is not None` never terminates, so every traversal has to
compare against the starting node or count."

**"n people in a circle, every k-th eliminated. Who survives?"**
"Direct simulation with a circular list: walk `k−1`, unlink in O(1), and continue from where I am — no
restart and no modular arithmetic, because the ring closes itself. That is O(n·k) time and O(n) space.
There is also a closed-form recurrence — the survivor for `n` people is `(survivor(n−1) + k) mod n`,
with one person surviving trivially — which is O(n) time and O(1) space, and I would mention it as the
better answer if `k` is large. The list version is the one that shows you understand the structure;
the recurrence is the one that is fast."

**"Where would you not use one?"**
"When I only ever walk forwards and never remove a node I already hold. Then `prev` is pure cost —
more memory, more writes, and a class of bugs I did not have. The recognition rule I use is: a doubly
linked list is for when something *else* hands me the node and I must act on it in constant time. If I
have to search for the node first, the search is O(n) anyway and the second pointer buys nothing."

**"Have you used one without knowing?"**
"`collections.deque` is a circular doubly linked list of fixed-size blocks — that is how it gets O(1)
at both ends without shifting. `OrderedDict` is a dict plus a doubly linked list, which is why
`move_to_end` is O(1) and why it *is* an LRU cache. The Linux kernel's `list_head` is a circular
doubly linked list with a sentinel, embedded in the structs themselves. And a browser's back and
forward history is the obvious user-facing one."

### A model answer

Asked: *why does an LRU cache use a doubly linked list?*

> "Because of exactly one operation, and it is the one the cache does on every single read.
>
> An LRU cache needs two things at once: find the entry for a key in constant time, and know which
> entry has been untouched the longest. The hash map does the first. A list in recency order does the
> second. And the moment a key is read, that entry has to move to the front — which means unlinking it
> from wherever it currently is.
>
> Unlinking a node means joining its predecessor to its successor. Two assignments, if I can reach
> both. In a singly linked list I cannot reach the predecessor from the node — I would have to walk
> from the head until I found the node whose `next` is my node, and that is O(capacity). So the map's
> constant-time lookup would be immediately thrown away by a linear walk. At a hundred thousand
> entries, every read would be about a hundred thousand steps instead of half a dozen pointer writes —
> roughly ten thousand times more work, which would make the cache slower than the thing it was put in
> front of.
>
> The `prev` pointer is what makes it two assignments. The general statement is: **the second pointer
> converts *having* a node into *being able to act* on it in constant time.** That is also why the map
> maps to nodes rather than to values, and why the node stores its own key — when I evict the node
> before the tail, I need its key to delete the map entry.
>
> I would use sentinels at both ends — fake head and tail nodes that always exist. In a singly linked
> list that is a convenience; here it is close to a requirement, because with two directions there are
> twice as many ends and every operation touches both neighbours, so without them half the code is
> `None` checks.
>
> The cost, honestly: eight bytes a node, about seventeen percent, and twice the pointer writes — two
> per removal, four per insertion. And the cost people do not mention: a doubly linked list can be
> *half* correct. If I update the forward links and forget the backward ones, iteration works, `len`
> works, every test passes, and then a later removal walks backwards into a node that was deleted. A
> singly linked list cannot be in that state. So I would write an invariant check that walks forwards
> and backwards and asserts they are reverses of each other, and run it after every operation in a
> randomised test — that catches every pointer bug in this structure in about a minute.
>
> One more thing worth saying: I would not reach for a doubly linked list by default. The rule is that
> it is for when something else hands me the node. If I have to search for the node first, the search
> is O(n) anyway and `prev` has bought me nothing but memory and bugs."

---

## 9. Recall card

- **The second pointer buys exactly one thing: given a node, remove it in O(1)** —
  `node.prev.next = node.next; node.next.prev = node.prev`. Two assignments, no walk, no length. In a
  singly linked list the same operation is **O(n)**, because reaching the predecessor means walking
  from the head. *The second pointer converts having a node into being able to act on it.*
- **That is the LRU cache's whole reason, with a number:** the map hands you the node in O(1), so
  unlinking must be O(1) too — at capacity 100,000 a singly linked list would make every **read** a
  100,000-step walk instead of ~6 pointer writes.
- **Write into the new node first, then rewire the neighbours** — or take both neighbours as
  parameters, which makes the ordering bug impossible. **Use sentinels at BOTH ends**; with two
  directions there are twice as many `None` checks to forget, so they stop being a convenience.
- **The cost that is not memory: a doubly linked list can be HALF correct** — right forwards, broken
  backwards — and it passes every forward test before failing somewhere else entirely. A singly linked
  list cannot be in that state. **Write `_check`: walk both ways, assert one is the reverse of the
  other.** Price: **+8 B per node (~17%)**, 2 writes per removal instead of 1, 4 per insertion instead
  of 2.
- **Circular = the last node points at the first: no head, no tail, no wrap-around branch, and with
  one sentinel no `None` anywhere.** `while node is not None` **never terminates** — compare against
  the starting node or count. Good for round-robin, playlists, turn order, ring buffers, and
  **Josephus** (simulate in O(n·k), or use `survivor(n) = (survivor(n−1) + k) mod n` in O(n) time and
  O(1) space). Real ones: `collections.deque`, `OrderedDict`, the Linux kernel's `list_head`.
