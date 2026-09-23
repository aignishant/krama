---
day: 79
track: dsa
title: "Traversal, insertion, and deletion"
phase: "Linked lists"
status: written
---

# Day 079 · DSA — Traversal, insertion, and deletion

**After today you can:** You can insert and delete at any position without losing the rest of the list.

**The interviewer asks it as:** *Delete the node at position k. What if it is the head?*

---

## 1. What this is, and why they ask it

Yesterday you met the node and the chain. Today you learn the three operations that everything else
in this phase is made of: **walk to a position**, **insert there**, and **delete there**.

There is one idea underneath all three, and it is worth stating before anything else: **to change the
list at position `k`, you must be standing at position `k − 1`.** You cannot remove a node while
holding it, because the node before it is still pointing at it and you cannot reach backwards. So
every operation is really "walk to the node before, then do one or two assignments".

They ask it because the code is six lines and the boundaries are where people fall over. Position
zero is different, because there is no node before the head. Position `size` is different, because
there is nothing after it. An empty list is different again. A candidate who writes the loop
confidently and then cannot say what happens when `k` is 0 has shown the interviewer exactly what
they wanted to see. It is also the setup for tomorrow: every one of those special cases disappears
with the dummy-head trick on [day 080](../day-080-dummy-head/README.md), and that trick only lands
if you have felt the pain first.

---

## 2. The story

The shunting yard at the goods station is behind the water tank, and Ganesh has worked it for
nineteen years.

His job on a Tuesday morning is to take the train that came in overnight and change it. Two wagons
out, one new one in, and the rest goes on at eleven. The wagons are joined by couplings — a heavy
hook and a screw at each joint — and one man with a bar can do a coupling in about two minutes.

What Ganesh does, and what the new boys do not do, is that he never walks to the wagon he wants. He
walks to the **joint before it**.

If the third wagon has to come out, he does not go and stand at the third wagon. He counts couplings
from the engine end — one, two — and stops at the joint between the second and the third. That is the
joint he has to open. Then he goes one further along, opens the joint between the third and the
fourth, and then he has a loose wagon that can be pulled aside. Then he brings the second and the
fourth together and makes one new joint. Three pieces of work, and all of them happen at the joints,
never at the wagon.

Putting one in is the same in reverse. Open one joint, and make two.

He is very particular about the counting, because he has seen what happens when somebody is off by
one. Twenty years ago a boy opened the joint on the wrong side and they took out the wrong wagon, and
nobody noticed until Belgaum.

The one job that is genuinely different is the first wagon. There is no joint before it — there is
the engine. Taking the first wagon out is not a shunting job at all, it is a job for the driver, and
it is done differently, by different people, with the engine moving. Ganesh will tell you this
without being asked, because every new boy tries to do it his own way once.

And there is a small thing he does at the end that the new boys skip. He walks the whole train to the
back and checks the last wagon, because the yard's board has to say how many wagons and which one is
last, and if that board is wrong at eleven o'clock the whole thing goes to the wrong platform.

---

## 3. The idea in plain English

Ganesh's rule is the rule. **You work at the joint before the wagon**, which in code is: to change
the list at position `k`, hold the node at position `k − 1`.

### Walking to a position

```python
    node = head
    for _ in range(k):          # take exactly k steps
        node = node.next
```

After `k` steps you are standing on the node at index `k`. Ganesh counting couplings from the engine
end. There is no shortcut — this is O(k), and it is the price of the structure from
[day 078](../day-078-nodes-and-links/README.md).

Take `k − 1` steps instead and you are standing on the node *before* the one you want, which is where
the work happens.

### Insertion at position k

You want the new node to end up at index `k`, so the node currently at `k − 1` must point at it, and
it must point at whatever used to be at `k`.

```python
    previous = walk_to(head, k - 1)
    previous.next = Node(value, previous.next)      # build, then relink
```

One line of work, once you are standing in the right place. Notice the order inside it: the new node
is fully built — already pointing at `previous.next` — *before* `previous.next` is reassigned. Written
as two statements the wrong way round, you lose the rest of the list.

### Deletion at position k

Open two joints and make one.

```python
    previous = walk_to(head, k - 1)
    previous.next = previous.next.next              # close the gap
```

The removed node still points forward, but nothing points at it, so Python collects it. One
assignment.

### The three boundaries, and what makes each one different

**`k == 0` — the head.** There is no node at `k − 1`. This is Ganesh's first wagon: not a harder
version of the same job, a *different* job, done by whoever holds the reference to the head.

```python
    if k == 0:
        return head.next             # a NEW head, which the caller must accept
```

And that "which the caller must accept" is the second half of the trap. In Python, rebinding a
parameter does not change the caller's variable, so any operation that can change the first node must
**return the new head**.

**`k == size` — appending.** Legal for insertion, illegal for deletion. Inserting at `size` means
walking to the last node and attaching. It is the one insertion position that needs no gap-closing.

**`k > size` — out of range.** Must raise, and must raise *before* you dereference `None`. The naive
loop hits `None.next` and gives you the phase's favourite error.

### Size and tail: the board at the end of the yard

Ganesh walking to the back to check the last wagon is bookkeeping that a bare chain of nodes cannot
do for itself. Two things are worth storing in a wrapper class:

- **`size`** — otherwise `len()` is O(n) every time. Maintained on every insert and delete.
- **`tail`** — a reference to the last node, which makes `append` **O(1)** instead of O(n).

Both are pure profit and both are a maintenance burden: **every operation must update them**, and the
subtle one is that deleting the last node leaves `tail` pointing at a node no longer in the list.
That is the bug in this lesson that produces no error at all — the list looks fine until the next
`append` attaches to a node nobody can reach.

Note what a `tail` reference does *not* buy you: deleting the last node is still O(n) in a singly
linked list, because you need the node *before* the tail and you cannot walk backwards. That is
exactly the argument for a doubly linked list, on
[day 085](../day-085-doubly-and-circular/README.md).

### The pattern that covers deletion by value

Deleting "the first node whose value is 7" is the same idea. You walk with `previous` and look at
`previous.next`, not at `previous`:

```python
    while previous.next is not None:
        if previous.next.value == target:
            previous.next = previous.next.next
            return
        previous = previous.next
```

**Look one ahead, act on the joint.** Every delete-by-condition problem in this phase is this loop,
plus a special case for the head that tomorrow's trick removes.

---

## 4. The picture

Deleting index 2 from a five-element list. Positions above, values below.

```
 index      0        1        2        3        4
          +---+    +---+    +---+    +---+    +---+
 head --> | 7 |--> | 3 |--> | 9 |--> | 4 |--> | 8 |--> None
          +---+    +---+    +---+    +---+    +---+
                     ^        ^
                 previous   target
              (walk k-1 = 1 step)

   previous.next = previous.next.next

 index      0        1                 2        3
          +---+    +---+             +---+    +---+
 head --> | 7 |--> | 3 |-----------> | 4 |--> | 8 |--> None
          +---+    +---+             +---+    +---+
                            +---+
                            | 9 |--> (still points at 4, but nothing points at it)
                            +---+
```

What to notice: the walk is `k − 1 = 1` step, not `k`. Standing on the node you want to delete is
useless, because the node before it is still pointing at you.

Now the head case, which is a different shape entirely:

```
 delete index 0

          +---+    +---+    +---+
 head --> | 7 |--> | 3 |--> | 9 |--> ...
          +---+    +---+    +---+
            ^
        nothing points at this from inside the list —
        the only reference is the caller's variable

   head = head.next        <- this is not a link change, it is a VARIABLE change
                              and the caller must be given the new value

          +---+    +---+
 head --> | 3 |--> | 9 |--> ...
          +---+    +---+
```

And insertion, where the order of the two assignments is the whole thing:

```
 insert 5 at index 2

 before:   [3]---->[9]
           prev

 RIGHT:  new = Node(5, prev.next)   ->  [5]---->[9]     (new node built, 9 still reachable)
         prev.next = new            ->  [3]---->[5]---->[9]

 WRONG:  prev.next = new            ->  [3]---->[5]     (9 is now unreachable)
         new.next = prev.next       ->  [5]---->[5]     (points at itself: infinite list)
```

---

## 5. The code, built step by step

### Step 1 — the walk, with the bounds check inside it

```python
    def _node_at(self, index: int) -> Node:
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for length {self._size}")
        node = self._head
        for _ in range(index):
            node = node.next
        return node
```

The check comes **first**, before any dereference. Doing it inside one helper means every public
method gets it for free and none of them can forget.

### Step 2 — insertion, with the three cases named

```python
    def insert_at(self, index: int, value: int) -> None:
        if index < 0 or index > self._size:            # note: > not >=, size is legal
            raise IndexError(f"cannot insert at {index} in a list of length {self._size}")
        if index == 0:
            self._head = Node(value, self._head)       # the head case
            if self._size == 0:
                self._tail = self._head                # first ever node is also the tail
```

`index > self._size` rather than `>=`, because inserting *at* `size` is appending and is legal. That
one character is the most common off-by-one in this problem.

```python
        else:
            previous = self._node_at(index - 1)        # stand at the joint before
            previous.next = Node(value, previous.next)
            if previous is self._tail:
                self._tail = previous.next             # appended: tail moved
        self._size += 1
```

Three lines of work and two lines of bookkeeping. The `if previous is self._tail` is what keeps the
tail honest, and forgetting it produces a list that is correct until the next `append`.

### Step 3 — deletion, and the head case

```python
    def delete_at(self, index: int) -> int:
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for length {self._size}")
        if index == 0:
            removed = self._head
            self._head = removed.next                  # a NEW head
            if self._size == 1:
                self._tail = None                      # the list is now empty
```

The `size == 1` branch is the one that bites. Deleting the only node must clear the tail as well, or
the list reports itself empty while `tail` still refers to the departed node.

```python
        else:
            previous = self._node_at(index - 1)
            removed = previous.next
            previous.next = removed.next
            if removed is self._tail:
                self._tail = previous                  # deleted the last: tail moves back
        removed.next = None                            # do not leave a stale link
        self._size -= 1
        return removed.value
```

`removed.next = None` is not required for correctness, but it stops a caller who kept a reference to
the removed node from walking back into a list it is no longer part of. That is a real source of
confusing bugs.

### Step 4 — append in O(1), which is the whole reason for the tail

```python
    def append(self, value: int) -> None:
        node = Node(value)
        if self._tail is None:
            self._head = self._tail = node             # empty list
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1
```

Without the tail reference this would walk the whole list every time, making `n` appends O(n²). With
it, each append is two assignments. Say the O(n²) out loud — building a list by repeatedly appending
without a tail is a classic accidental quadratic.

### Step 5 — delete by value, the look-one-ahead loop

```python
    def remove_value(self, value: int) -> bool:
        if self._head is None:
            return False
        if self._head.value == value:
            self.delete_at(0)                          # reuse, do not duplicate
            return True

        previous = self._head
        while previous.next is not None:
            if previous.next.value == value:
                ...
```

Calling `delete_at(0)` rather than re-writing the head logic is worth doing and worth saying: the head
case is fiddly enough that it should exist in exactly one place.

### The complete solution

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


class LinkedList:
    """A singly linked list with O(1) length and O(1) append.

    The rule underneath every operation: to change the list at position k, you
    must be standing at position k-1, because you cannot reach backwards.

    Two pieces of bookkeeping, and both must be updated by EVERY mutation:
      _size — otherwise len() is O(n)
      _tail — otherwise append() is O(n) and building a list is O(n^2)

    The bug with no error message: deleting the last node without moving _tail
    back leaves it pointing at a node that is no longer in the list.
    """

    def __init__(self, values: list[int] | None = None) -> None:
        self._head: Node | None = None
        self._tail: Node | None = None
        self._size = 0
        for value in values or []:
            self.append(value)

    # ---- reading -------------------------------------------------------

    def __len__(self) -> int:
        return self._size                              # O(1), because we store it

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def to_list(self) -> list[int]:
        return list(self)

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"

    def value_at(self, index: int) -> int:
        return self._node_at(index).value

    def index_of(self, value: int) -> int:
        for position, item in enumerate(self):
            if item == value:
                return position
        return -1

    # ---- writing -------------------------------------------------------

    def append(self, value: int) -> None:
        """O(1), thanks to the tail reference."""
        node = Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value: int) -> None:
        """O(1) always — the one thing a linked list is unambiguously good at."""
        self._head = Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def insert_at(self, index: int, value: int) -> None:
        """O(index). Inserting AT size is legal and means append."""
        if index < 0 or index > self._size:            # > not >=
            raise IndexError(f"cannot insert at {index} in a list of length {self._size}")
        if index == 0:
            self.prepend(value)
            return
        if index == self._size:
            self.append(value)
            return
        previous = self._node_at(index - 1)            # stand at the joint before
        previous.next = Node(value, previous.next)     # build, THEN relink
        self._size += 1

    def delete_at(self, index: int) -> int:
        """O(index). Returns the removed value."""
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for length {self._size}")

        if index == 0:
            removed = self._head
            self._head = removed.next
            if removed is self._tail:                  # the list had exactly one node
                self._tail = None
        else:
            previous = self._node_at(index - 1)
            removed = previous.next
            previous.next = removed.next
            if removed is self._tail:                  # deleted the last node
                self._tail = previous

        removed.next = None                            # no stale link out of a dead node
        self._size -= 1
        return removed.value

    def remove_value(self, value: int) -> bool:
        """Remove the first node with this value. Look ONE AHEAD and act on the joint."""
        if self._head is None:
            return False
        if self._head.value == value:
            self.delete_at(0)                          # one home for the head case
            return True

        previous = self._head
        while previous.next is not None:
            if previous.next.value == value:
                if previous.next is self._tail:
                    self._tail = previous
                previous.next = previous.next.next
                self._size -= 1
                return True
            previous = previous.next
        return False

    # ---- internals -----------------------------------------------------

    def _node_at(self, index: int) -> Node:
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for length {self._size}")
        node = self._head
        for _ in range(index):
            node = node.next
        return node

    def _check(self) -> None:
        """Assert the invariants. Run this in tests; it catches the stale tail."""
        count, node, last = 0, self._head, None
        while node is not None:
            count, last, node = count + 1, node, node.next
        assert count == self._size, f"size says {self._size}, chain has {count}"
        assert last is self._tail, "tail does not point at the last node"
        assert self._tail is None or self._tail.next is None, "tail is not the end"


if __name__ == "__main__":
    lst = LinkedList([7, 3, 9, 4, 8])
    print(lst)                                # LinkedList([7, 3, 9, 4, 8])
    print(len(lst), lst.value_at(2))          # 5 9

    print(lst.delete_at(2), lst)              # 9 LinkedList([7, 3, 4, 8])
    print(lst.delete_at(0), lst)              # 7 LinkedList([3, 4, 8])
    print(lst.delete_at(2), lst)              # 8 LinkedList([3, 4])
    lst._check()                              # the tail moved back correctly

    lst.insert_at(0, 1)
    lst.insert_at(3, 99)                      # index == size, so this appends
    lst.insert_at(2, 50)
    print(lst, len(lst))                      # LinkedList([1, 3, 50, 4, 99]) 5
    lst._check()

    lst.append(6)
    print(lst, lst.index_of(99))              # LinkedList([1, 3, 50, 4, 99, 6]) 4

    print(lst.remove_value(50), lst)          # True LinkedList([1, 3, 4, 99, 6])
    print(lst.remove_value(404), lst)         # False LinkedList([1, 3, 4, 99, 6])

    single = LinkedList([42])
    print(single.delete_at(0), single, len(single))    # 42 LinkedList([]) 0
    single._check()
    single.append(1)                          # would break if the tail were stale
    print(single)                             # LinkedList([1])

    empty = LinkedList()
    try:
        empty.delete_at(0)
    except IndexError as error:
        print(f"IndexError: {error}")         # index 0 out of range for length 0
    try:
        empty.insert_at(1, 5)
    except IndexError as error:
        print(f"IndexError: {error}")         # cannot insert at 1 in a list of length 0
```

`_check` is worth writing in an interview if there is a minute spare. It catches the stale tail, the
wrong size and a broken chain in three assertions, and running it after every operation in a test loop
finds bugs that eyeballing never will.

---

## 6. What it costs

### The operations

```
 walk to index k                    O(k)
 value_at(k)                        O(k)
 prepend                            O(1)
 append (with a tail reference)     O(1)
 append (without one)               O(n)
 insert_at(k)                       O(k)
 delete_at(k)                       O(k)
 delete_at(0)                       O(1)
 delete the LAST node               O(n)  even with a tail reference
 remove_value                       O(n)
 len                                O(1)  because we store it
```

Two of those need saying out loud.

**`append` without a tail is O(n), so building a list of `n` elements by appending is O(n²).** At
n = 100,000 that is five billion steps. With a tail it is 100,000 assignments. This is the single most
common accidental quadratic in linked-list code.

**Deleting the last node is O(n) even with a tail reference**, because you need the node *before* the
tail and a singly linked list cannot walk backwards. Say this when the tail comes up — it is the
cleanest possible motivation for the doubly linked list.

### Against a Python list

```
                              LinkedList         Python list
 insert at 0                  O(1)               O(n)   shift everything
 delete at 0                  O(1)               O(n)   shift everything
 insert at the end            O(1) with a tail   O(1) amortised
 delete at the end            O(n)               O(1)
 insert at the middle         O(k) walk          O(n) shift
 access index k               O(k)               O(1)
```

The honest summary: **the linked list wins at the front and loses everywhere else.** Even in the
middle, where the folklore says linked lists win, both are linear — one pays for the walk, the other
for the shift — and the array's shift is a fast contiguous memory move while the walk is a chain of
scattered dereferences.

### The measurement

Building a 100,000-element list, from [day 078](../day-078-nodes-and-links/README.md)'s numbers:

```
 100,000 × list.insert(0, x)     1.443 s
 100,000 × prepend on nodes      0.0246 s        about 59x
```

And the quadratic append, if you forget the tail:

```
 n appends without a tail:  1 + 2 + ... + n = n(n+1)/2 steps
 n = 100,000:               about 5 x 10^9 steps  — tens of seconds
 n appends with a tail:     100,000 × 2 assignments
```

### Space

```
 the list:      O(n) nodes, 48 bytes each with __slots__
 bookkeeping:   O(1) — one size integer and one tail reference
 every operation: O(1) extra — one `previous` variable
```

Every algorithm in this phase should be O(1) extra space. If yours copies to a Python list first, say
so and say what you traded.

---

## 7. The traps

### Trap 1 — walking `k` steps instead of `k − 1`

```python
    previous = self._node_at(index)          # should be index - 1
    previous.next = previous.next.next
```

Deletes the wrong node — the one *after* the target — and does it silently. `delete_at(2)` on
`[7, 3, 9, 4, 8]` removes 4 instead of 9. Ganesh's boy opening the joint on the wrong side.

The fix is to say the rule out loud before writing the line: **stand at `k − 1`, act on `k`.**

### Trap 2 — the head, unhandled

```python
    previous = self._node_at(index - 1)      # index 0 -> _node_at(-1)
```

```
IndexError: index -1 out of range for length 5
```

if you guarded, and this if you did not:

```python
    node = self._head
    for _ in range(-1):                      # loop body never runs
        node = node.next
    node.next = node.next.next               # deletes index 1, not index 0
```

Silently wrong, which is worse. **Position zero is a different operation**, not a harder version of
the same one.

### Trap 3 — not returning the new head

```python
def delete_first(head):
    head = head.next                         # rebinds the local name only
    return None
```

```python
    delete_first(head)
    print(to_values(head))                   # unchanged, no error
```

Python passes the reference by value, so rebinding a parameter changes nothing for the caller. **Any
function that can change which node is first must return the new head**, and the caller must assign
it. Inside a class this disappears, because `self._head` is shared state — which is one good reason to
wrap the chain in a class.

### Trap 4 — the stale tail

```python
        previous.next = removed.next
        self._size -= 1                      # forgot: if removed is self._tail
```

No error. The list is correct, `len` is correct, iteration is correct. And then:

```python
    lst.append(6)                            # attaches to the REMOVED node
    print(lst.to_list())                     # the 6 is nowhere to be seen
```

The append succeeds and the value vanishes. This is the hardest bug in the lesson to find by reading,
and it is why `_check` exists.

The same trap in its other form: deleting the only node must set `_tail = None`, or an empty list
holds a reference to a departed node and the next `append` attaches to nothing reachable.

### Trap 5 — `>` versus `>=` on the insert bound

```python
    if index < 0 or index >= self._size:     # WRONG for insertion
        raise IndexError(...)
```

Now `insert_at(size, value)` — appending — raises. Inserting *at* `size` is legal; deleting at `size`
is not. One character, two different bounds, and the reason is that insertion has `size + 1` valid
positions and deletion has `size`.

### Trap 6 — `previous.next.next` with no guard

```python
    while previous.next.value != target:     # two dereferences, one check
```

```
AttributeError: 'NoneType' object has no attribute 'value'
```

Fires as soon as the target is absent. The loop condition must be `while previous.next is not None and
previous.next.value != target`, and the `is not None` must come first because `and` short-circuits.

### Trap 7 — forgetting to update `_size`

Silent, and it corrupts everything downstream: `_node_at` uses `_size` for its bounds check, so a
size that is one too large lets a walk run off the end into `None`, and a size one too small makes
the last element unreachable. **Every mutation updates size**, and the assertion in `_check` catches
it in one line.

### Trap 8 — building a list with `append` and no tail

```python
    for value in range(100_000):
        lst.append(value)                    # each append walks the whole list
```

No error, correct output, and about five billion steps. The tail reference turns O(n²) into O(n) and
costs one attribute.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Delete the node at position k."* Then, immediately: *"What if k is 0?"* — the
  follow-up is the question.
- The class version: *"Design a linked list with get, addAtHead, addAtTail, addAtIndex and
  deleteAtIndex."* LeetCode 707, and it is entirely a boundary-conditions exercise.
- The by-value version: *"Remove all elements equal to `val`."* LeetCode 203, which is the strongest
  possible motivation for tomorrow's dummy head.
- The trap version: *"What is the complexity of appending n elements?"* — they want to hear "O(n) with
  a tail reference, O(n²) without".

### What to say out loud, in the first ninety seconds

1. **State the rule that generates all three operations.** "To change the list at position k I have to
   be standing at k−1, because I cannot reach backwards from a node to the one before it."
2. **Name the boundaries before writing.** "So there are three cases: k equals zero, where there is no
   previous node and the head itself changes; k in the middle, which is the general case; and k out of
   range, which must raise before I dereference anything."
3. **Say the order-of-assignment rule for insertion.** "I build the new node pointing at the rest of
   the list first, then attach it. The other order loses the tail."
4. **Say what you will store, and why.** "I would keep a size and a tail reference. Size makes `len`
   O(1), and the tail makes `append` O(1) — without it, building a list of n elements by appending is
   O(n²)."
5. **Name the maintenance cost yourself.** "The price is that every mutation has to maintain both, and
   the bug that has no error message is deleting the last node without moving the tail back."

### The follow-ups

**"What if k is 0?"**
"Then there is no node at k−1 to work from, so it is a different operation rather than a harder one:
the head reference itself changes. In a class, `self._head = self._head.next` and I also have to
clear the tail if that was the only node. In a bare function, the important part is that I must
*return* the new head, because rebinding the parameter does not change the caller's variable — that
is a bug that produces no error at all. Tomorrow's dummy-head trick removes the case entirely."

**"What is the complexity of appending n elements?"**
"O(n) if I keep a tail reference, because each append is two assignments. O(n²) without one, because
each append walks the whole list — that is n(n+1)/2 steps, about five billion at a hundred thousand
elements. It is the classic accidental quadratic in this structure."

**"You have a tail reference. Can you delete the last node in O(1)?"**
"No, and that is the cleanest argument for a doubly linked list. To unlink the last node I need the
node *before* it so I can set its `next` to `None`, and a singly linked list cannot walk backwards, so
I have to traverse from the head. A tail reference makes append O(1) and does nothing for
delete-last."

**"How do you know your list is not corrupt?"**
"I would write a small invariant check: walk the chain counting nodes, assert the count equals the
stored size, assert the last node reached is the tail, and assert the tail's `next` is `None`. Three
assertions, and they catch the stale tail, the wrong size and a broken chain. In a test I would run
it after every operation on a random sequence."

**"Delete every node with a given value."**
"The same look-one-ahead loop: I hold `previous` and test `previous.next.value`, so that when it
matches I can unlink it. Two subtleties. After a deletion I must *not* advance `previous`, or two
equal values in a row leave one behind. And the head needs its own loop first, because several leading
nodes may all match. Both of those disappear with a dummy node before the head, which is what I would
actually write."

**"Why wrap the nodes in a class at all?"**
"Three reasons. It gives `size` and `tail` a home, so `len` and `append` are O(1). It puts the head
case in exactly one place instead of in every function. And it removes the return-the-new-head
problem, because `self._head` is shared state rather than a parameter that gets rebound."

### A model answer

Asked: *delete the node at position k. What if it is the head?*

> "The rule that generates this whole family: to change the list at position k, I have to be standing
> at position k−1. A node cannot reach the node before it, so I cannot unlink a node I am holding —
> I have to be holding its predecessor.
>
> So the general case is: walk k−1 steps from the head, then `previous.next = previous.next.next`.
> That is one assignment. The walk is O(k) and the unlink is O(1), so the operation is O(k) overall.
> The removed node still points forward, but nothing points at it, so it is collected.
>
> Now, k equals zero. There is no node at position minus one, so this is not a harder version of the
> same operation — it is a different operation. What changes is the head reference itself, not a link
> inside the list. In a class that is `self._head = self._head.next`, and I also have to clear the
> tail if that was the only node, or I am left with a reference to a node that is no longer in the
> list.
>
> If it is a bare function rather than a class, there is a second half to that answer and it is the
> part people miss: Python passes the reference by value, so rebinding the `head` parameter inside the
> function does not change the caller's variable. The function has to *return* the new head and the
> caller has to assign it. That bug produces no error — the list just still has its first element.
>
> The other boundaries: k greater than or equal to the size must raise, and it must raise *before* I
> dereference anything, or I get `AttributeError: 'NoneType' object has no attribute 'next'` instead
> of a useful message. And note that insertion and deletion have different bounds — inserting *at*
> size is legal and means append, so insertion allows size + 1 positions and deletion allows size.
>
> If I am writing this as a class rather than a one-off function, I would store two extra things. A
> size, so `len` is O(1) rather than a walk. And a tail reference, so `append` is O(1) — without one,
> building a list of n elements by appending is O(n²), about five billion steps at a hundred thousand
> elements. The cost is that every mutation has to maintain both, and the nastiest bug in this class
> is deleting the last node and forgetting to move the tail back: the list looks completely correct
> until the next append attaches to a node nobody can reach, and the value silently vanishes. So I
> would write a three-line invariant check — count the chain, compare to size, confirm the tail is the
> last node — and run it after every operation in tests.
>
> One thing a tail reference does *not* buy me: deleting the last node is still O(n), because I need
> the node before the tail and I cannot walk backwards. That is the argument for a doubly linked
> list."

---

## 9. Recall card

- **One rule generates all three operations: to change the list at position `k`, stand at `k − 1`.**
  You cannot reach backwards, so you can never unlink a node you are holding. Deletion is
  `previous.next = previous.next.next`; insertion is `previous.next = Node(value, previous.next)` —
  **build first, then relink**, or the node points at itself and the rest of the list is gone.
- **`k == 0` is a different operation, not a harder one** — the head *reference* changes, not a link.
  In a bare function you must **return the new head**, because rebinding a parameter changes nothing
  for the caller and raises no error. Tomorrow's **dummy head** deletes this case entirely.
- **Insertion and deletion have different bounds.** Inserting *at* `size` is legal (it appends), so
  insertion has `size + 1` valid positions and deletion has `size`: `index > size` versus
  `index >= size`. Check bounds **before** any dereference.
- **Store `size` and `tail`, and maintain them in every mutation.** `size` makes `len` O(1); `tail`
  makes `append` O(1) — **without it, n appends is O(n²)**, about 5 × 10⁹ steps at n = 100,000. The
  bug with **no error message** is deleting the last node without moving the tail back: the next
  `append` attaches to an unreachable node and the value vanishes. A three-assertion `_check` catches
  it.
- **A tail reference does not make delete-last O(1)** — you need the node *before* the tail and a
  singly linked list cannot walk backwards. That is the argument for the **doubly linked list**. And
  the honest summary against a Python list: **the linked list wins at the front and loses everywhere
  else** (100,000 front inserts: **1.443 s vs 0.0246 s**, ~59×).
