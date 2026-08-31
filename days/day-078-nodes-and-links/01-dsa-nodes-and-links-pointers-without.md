---
day: 78
track: dsa
title: "Nodes and links: pointers without pointers"
phase: "Linked lists"
status: written
---

# Day 078 · DSA — Nodes and links: pointers without pointers

**After today you can:** You can draw a linked list in memory and say why it is not an array.

**The interviewer asks it as:** *What is a linked list, and when is it better than an array?*

---

## 1. What this is, and why they ask it

A **linked list** is a chain of small objects. Each object — a **node** — holds one value and a
reference to the next node. You keep hold of the first node, called the **head**, and everything else
is reached by following the chain.

That is the entire structure, and everything about it follows from one difference with an array: an
array's elements sit **next to each other in memory** and are found by arithmetic, while a linked
list's nodes sit **wherever they happen to be** and are found by following references. So an array
can jump straight to element 500 and a linked list cannot. And a linked list can insert in the middle
without moving anything, while an array must shift everything after the gap.

They ask it because "when would you use a linked list instead of an array?" is a question with a
genuinely honest answer that most candidates get wrong in both directions. Some say "linked lists are
faster for insertion" without the qualifier that makes it true. Some say "never use them" without
noticing that the LRU cache they just built on [day 076](../day-076-lru-cache/README.md) needs one.
It is also the foundation for the next eight days, and for trees and graphs after that — a tree is a
node with two links instead of one, and nothing else changes.

---

## 2. The story

There are forty flats in Prakash's building and the association has a way of passing on news that
was set up long before he moved in.

It used to be that the secretary called everybody. Forty calls, on a Sunday, about the water tanker
being late or the lift being serviced on Tuesday. He was seventy-one and it took him most of a
morning, and by the end of it he had usually forgotten two flats and rung one twice.

So they changed it. Now every flat has exactly one number saved for this — the next flat along. 101
has 102's number. 102 has 103's. 103 has 201's, because that is how the building runs. And the last
flat, 404, has nobody, which is how you know the message has finished going round.

The secretary makes one call. Then he goes back to his tea.

Prakash likes it and he has also noticed the two things about it that everyone in the building has
noticed.

The first is that you cannot skip. When the plumber told him he would be at flat 302 in ten minutes
and Prakash wanted to warn them, he could not — he does not have 302's number. Nobody in the building
has anybody's number except the one they were given. To get a message to 302 you start at 101 and you
go through everybody in between, or you walk up.

The second is what happened when the Menons moved into 204, which had been empty for two years. It
took about a minute. 203 saved the Menons' number instead of 205's, and the Menons saved 205's, and
that was it. Nobody else in the building changed anything or even knew. When old Mr Iyer in 302
passed away and the flat was locked up, it was the same in reverse: 301 saved 303's number and the
chain closed over the gap, and again nobody else was affected.

The one thing that goes wrong, and it goes wrong about twice a year, is when somebody does not
answer. Then the message stops there. Everybody after them hears nothing, and they do not know they
have heard nothing, and the first anyone finds out is when half the building turns up on the wrong
day.

---

## 3. The idea in plain English

Each flat is a **node**. The number saved in each flat's phone is the **link** to the next node. The
secretary's own number for 101 is the **head**. And 404 having nobody is how the chain ends.

### A node, in code

```python
class Node:
    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value       # the flat's news
        self.next = next         # the one number they have saved
```

Two fields. That is the whole data structure. A list of three values is three of these objects, each
holding the next:

```python
third = Node(3)
second = Node(2, third)
first = Node(1, second)
head = first
```

`head` is not a special object. It is just a name for the first node, and losing that name loses the
whole list, because nothing else points at it.

### "Pointers without pointers"

In C you would write `struct Node *next` and think about memory addresses. Python has no pointers and
you never need to think about addresses — but the mechanism is the same one, and it is worth being
precise about it because interviewers probe here.

**In Python, a variable does not hold an object. It holds a reference to one.** When you write
`second = Node(2, third)`, the name `second` refers to a node object living somewhere on the heap,
and `first.next` refers to *the same object*. Two names, one object. That is why:

```python
first.next.value = 99
print(second.value)          # 99 — same object, seen through a different name
```

So `node.next` is exactly a pointer: something that lets you get to another object without containing
it. What Python removes is address arithmetic and manual freeing, not the idea.

### The difference that decides everything

An array — a Python `list` — is a **contiguous block of slots**. From
[day 009](../day-009-what-an-array-is/README.md): the list knows the address of slot 0, and element
`i` is at `start + i × slot_size`. One multiplication and one addition, whatever `i` is. That is why
`numbers[500_000]` is as fast as `numbers[0]`.

A linked list has no such arithmetic available, because the nodes are **not next to each other**. Node
5 could be a megabyte away from node 4. The only way to reach the 500,000th node is to start at the
head and follow `next` 500,000 times.

```
 array:        one multiply and one add          -> O(1) access
 linked list:  follow k references                -> O(k) access
```

Everything else in this phase is a consequence of that one sentence.

### What you get in exchange

**Insertion and deletion in the middle are O(1) — *if you already have the node.*** That qualifier is
the entire honest answer and most people leave it out.

To delete a node from an array you must shift every element after it left by one, which is O(n). To
delete a node from a linked list you set one reference:

```python
    previous.next = node_to_remove.next        # the chain closes over the gap
```

One assignment. 203 saving 205's number. Nothing else in the building changes, and it costs the same
whether the building has forty flats or forty thousand.

**But** if all you have is a *position* — "delete the 500th element" — you must walk to it first, and
that walk is O(n). So the honest complexity is:

```
 delete, given the node:        O(1)
 delete, given the position:    O(n) to find + O(1) to unlink  =  O(n)
 delete from an array, given the position:  O(1) to find + O(n) to shift = O(n)
```

**Both are O(n) when you are given a position.** The linked list wins only when the node is already in
your hand — which is exactly the LRU cache, where a hash map hands you the node.

### The other two differences, which are real

**No reallocation.** A Python list that grows past its capacity allocates a bigger block and copies
everything across. A linked list never copies anything; it just makes one more small object. That
matters when elements are huge or when a copy pause is unacceptable.

**Worse memory and worse speed per element.** Measured, at a million elements:

```
 python list:  8 bytes per element (a pointer in the block)
 Node object:  48 bytes with __slots__, 336 bytes without
```

Six times the memory with `__slots__`, forty times without. And walking the chain was **2.0× slower**
than walking the list, because each step is an attribute lookup on an object that may be anywhere in
memory, rather than the next slot in a block the processor has already fetched.

That second effect is **cache locality**, and it is the reason experienced engineers reach for arrays
by default. When the processor fetches memory it fetches a whole 64-byte line, so reading an array
brings the next several elements along for free. Reading a linked list brings a node and whatever
happens to be beside it, which is usually nothing useful.

### So when is a linked list actually right?

Four honest cases, and you should be able to give them without hedging:

1. **You already hold the node and must splice it out in O(1).** The LRU cache. This is the big one.
2. **You are always inserting or removing at the front.** Measured: 100,000 front insertions took
   **1.443 s** with `list.insert(0, x)` and **0.0246 s** building a chain — about **59×**. Though in
   Python you would reach for a `deque`, which is a linked list of blocks and gets both.
3. **Copying is unacceptable.** Real-time systems where a reallocation pause matters, or elements too
   large to copy.
4. **The structure is the point.** A tree is a node with two links. A graph adjacency list is a list
   of chains. Everything after this phase is built out of nodes.

And the honest fifth case: **because the interviewer said so.** Half the problems in the next eight
days exist to test pointer manipulation, not to be good engineering.

### The failure mode

Mr Iyer not answering the phone is a **broken link**. In Python, a `next` that is `None` when you
expected a node gives you:

```
AttributeError: 'NoneType' object has no attribute 'next'
```

That single error will account for most of your debugging for the next eight days, and the two
defences are: check `while node is not None`, and use a **dummy head** so the first node is never a
special case. That is [day 080](../day-080-dummy-head/README.md), and it is the most useful trick in
the phase.

---

## 4. The picture

An array and a linked list holding the same four values.

```
 ARRAY — one block, elements adjacent, found by arithmetic

  address  1000  1008  1016  1024
          +-----+-----+-----+-----+
  value   |  7  |  3  |  9  |  4  |
          +-----+-----+-----+-----+
  index      0     1     2     3

  numbers[2]  ->  1000 + 2*8 = 1016  ->  one multiply, one add, O(1)


 LINKED LIST — separate objects, scattered, found by following

  head
   |
   v
  +------+------+     +------+------+     +------+------+     +------+------+
  |  7   |  ----+---->|  3   |  ----+---->|  9   |  ----+---->|  4   | None |
  +------+------+     +------+------+     +------+------+     +------+------+
  @ 4200              @ 9016              @ 4408              @ 7712

  the third node  ->  head.next.next     ->  follow 2 links, O(k)
  the addresses are in no order at all, and that is the whole point
```

What to notice: the array's addresses go up by 8 every time and the linked list's addresses are
random. That randomness is what buys the cheap insertion and what costs the fast access.

Now the insertion, which is the operation the structure exists for:

```
 insert 5 between 3 and 9

 before:   ... [3| ]---->[9| ]---->[4|None]

 step 1: new node points at 9      [5| ]---->[9| ]
 step 2: 3 points at the new node  [3| ]---->[5| ]

 after:    ... [3| ]---->[5| ]---->[9| ]---->[4|None]

 Two assignments. Node 9 and node 4 were not touched, moved, or copied.
 ORDER MATTERS: do step 1 first. If you set 3.next = 5 first, you have
 lost your only reference to 9 and the rest of the list is gone.
```

And the deletion:

```
 delete 9, given the node BEFORE it

 before:   [3| ]---->[9| ]---->[4|None]
              previous  node

   previous.next = node.next

 after:    [3| ]------------->[4|None]

 One assignment. Node 9 still points at 4, but nothing points at 9,
 so Python collects it. 203 saving 205's number.
```

---

## 5. The code, built step by step

### Step 1 — the node

```python
class Node:
    """One link in the chain. A value and a reference to the next node."""

    __slots__ = ("value", "next")          # 48 bytes instead of 336

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next
```

`__slots__` stops each node from carrying its own attribute dictionary. Mention it once and move on;
in an interview the plain version is fine.

### Step 2 — building a list, and the loop that appears in every problem

```python
def from_values(values: list[int]) -> Node | None:
    head: Node | None = None
    for value in reversed(values):         # build backwards
        head = Node(value, head)           # each new node points at the old head
    return head
```

Building **backwards** is the trick, and it is worth understanding rather than memorising: pushing at
the front is the only O(1) insertion when you hold nothing but the head. Reverse the input, push each
value at the front, and the list comes out in the original order.

### Step 3 — the traversal loop

```python
    node = head
    while node is not None:
        ...                                # do something with node.value
        node = node.next                   # step forward
```

**This loop is the phase.** It will appear in every problem for the next eight days. Two things about
it: the condition is `is not None`, not `while node`, because a node holding the value `0` is
perfectly real and `while node` happens to work only because `Node` has no `__bool__` — do not rely
on that. And the last line must be inside the loop, or it never ends.

### Step 4 — length and access by position

```python
def length(head: Node | None) -> int:
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count
```

O(n), and there is no way to make it O(1) without storing a count separately. An array knows its
length; a chain does not. That is worth saying out loud when the interviewer asks for the `k`th
element.

```python
def value_at(head: Node | None, index: int) -> int:
    node = head
    for _ in range(index):                 # walk `index` links
        if node is None:
            raise IndexError("index out of range")
        node = node.next
    if node is None:
        raise IndexError("index out of range")
    return node.value
```

O(index). Compare with `numbers[index]` on a list, which is one multiply and one add. This function is
the reason you do not use a linked list when you need random access.

### Step 5 — insertion after a node you hold

```python
def insert_after(node: Node, value: int) -> Node:
    node.next = Node(value, node.next)     # build first, then relink
    return node.next
```

One line, and it is correct because `Node(value, node.next)` is fully constructed *before*
`node.next` is reassigned. Written as two statements in the wrong order, it loses the tail.

### Step 6 — deletion, and the two ways it is asked

```python
def delete_after(node: Node) -> None:
    if node.next is not None:
        node.next = node.next.next         # close the gap
```

Given the node *before* the target: one assignment, O(1).

Given only the target and no head — a genuine interview question, LeetCode 237 — you cannot reach the
node before it. The trick is to **become the next node**:

```python
def delete_this_node(node: Node) -> None:
    """Delete a node when you are given only that node (never the tail)."""
    node.value = node.next.value           # copy the successor's value into me
    node.next = node.next.next             # then unlink the successor
```

You have not deleted the node you were given; you have deleted the one after it, having first stolen
its value. The effect is identical from the outside. It fails on the last node, and saying so
unprompted is the point of the question.

### The complete solution

```python
class Node:
    """One link in a singly linked list: a value and a reference to the next."""

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


def from_values(values: list[int]) -> Node | None:
    """Build a list from a Python list. Build BACKWARDS: pushing at the front
    is the only O(1) insertion available when you hold only the head."""
    head: Node | None = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def to_values(head: Node | None) -> list[int]:
    """The traversal loop, which is every problem in this phase."""
    values: list[int] = []
    node = head
    while node is not None:
        values.append(node.value)
        node = node.next
    return values


def length(head: Node | None) -> int:
    """O(n). A chain does not know its own length; an array does."""
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count


def value_at(head: Node | None, index: int) -> int:
    """O(index), against O(1) for an array. This is the cost of the structure."""
    if index < 0:
        raise IndexError("index must be non-negative")
    node = head
    for _ in range(index):
        if node is None:
            raise IndexError("index out of range")
        node = node.next
    if node is None:
        raise IndexError("index out of range")
    return node.value


def find(head: Node | None, value: int) -> Node | None:
    """Return the first node with this value, or None. O(n) — no shortcut."""
    node = head
    while node is not None:
        if node.value == value:
            return node
        node = node.next
    return None


def push_front(head: Node | None, value: int) -> Node:
    """O(1), and the reason linked lists are good at stacks.
    Returns the NEW head — the caller must reassign."""
    return Node(value, head)


def insert_after(node: Node, value: int) -> Node:
    """O(1) given the node. Construct first, THEN relink, or the tail is lost."""
    node.next = Node(value, node.next)
    return node.next


def delete_after(node: Node) -> int | None:
    """Remove the node following `node`. O(1). Returns the removed value."""
    target = node.next
    if target is None:
        return None
    node.next = target.next               # close the gap over the target
    target.next = None                    # not required, but keeps stale links out
    return target.value


def delete_value(head: Node | None, value: int) -> Node | None:
    """Remove the FIRST node with this value. Returns the (possibly new) head.

    Note the special case for the head — this is exactly the ugliness that the
    dummy-head trick on day 080 removes.
    """
    if head is None:
        return None
    if head.value == value:               # the special case
        return head.next

    node = head
    while node.next is not None:
        if node.next.value == value:
            node.next = node.next.next
            return head
        node = node.next
    return head


def delete_this_node(node: Node) -> None:
    """LeetCode 237: delete a node given ONLY that node, never the tail.

    You cannot reach the node before it, so instead you steal the successor's
    value and unlink the successor. Indistinguishable from outside, and
    impossible for the last node — say that before being asked.
    """
    if node.next is None:
        raise ValueError("cannot delete the last node without its predecessor")
    node.value = node.next.value
    node.next = node.next.next


if __name__ == "__main__":
    head = from_values([7, 3, 9, 4])
    print(to_values(head))                      # [7, 3, 9, 4]
    print(length(head), value_at(head, 2))      # 4 9

    node = find(head, 3)
    insert_after(node, 5)
    print(to_values(head))                      # [7, 3, 5, 9, 4]

    delete_after(node)
    print(to_values(head))                      # [7, 3, 9, 4]

    head = push_front(head, 1)
    print(to_values(head))                      # [1, 7, 3, 9, 4]

    head = delete_value(head, 1)                # the head case
    print(to_values(head))                      # [7, 3, 9, 4]
    head = delete_value(head, 9)                # the middle case
    print(to_values(head))                      # [7, 3, 4]
    head = delete_value(head, 99)               # not present
    print(to_values(head))                      # [7, 3, 4]

    print(to_values(from_values([])))           # []
    print(length(None))                         # 0

    victim = find(head, 3)
    delete_this_node(victim)                    # steals 4's value
    print(to_values(head))                      # [7, 4]

    try:
        value_at(head, 9)
    except IndexError as error:
        print(f"IndexError: {error}")           # IndexError: index out of range
```

---

## 6. What it costs

### The operations, side by side with an array

```
                              linked list        Python list (array)
 access by index              O(n)  walk         O(1)  one multiply, one add
 search for a value           O(n)               O(n)
 insert at the front          O(1)               O(n)  shift everything
 insert at the back           O(n) without a
                              tail reference;
                              O(1) with one      O(1) amortised
 insert given the node        O(1)               n/a
 insert at a known position   O(n) walk + O(1)   O(1) find + O(n) shift  = both O(n)
 delete given the node        O(1)  one write    n/a
 delete at a known position   O(n)               O(n)
 length                       O(n) unless stored O(1)
 memory per element           48 B (__slots__)   8 B
```

The two rows that decide real arguments are `insert at the front` and `insert given the node`.
Everything else is a draw or a loss.

### The measurements

All on a million elements unless stated, on this machine.

```
 walking the whole structure and summing:
   python list      0.0621 s
   linked list      0.1232 s        2.0x slower
```

Two times, not a hundred, and it is worth being accurate about that. The slowdown is one attribute
lookup per step plus poor cache behaviour, not an asymptotic difference — both are O(n).

```
 100,000 insertions at the FRONT:
   list.insert(0, x)   1.443 s
   push_front on nodes 0.0246 s     about 59x faster
```

That is the linked list's real win, and it is the same measurement as `pop(0)` from
[day 073](../day-073-queues/README.md) seen from the other end. In Python you would use a `deque`,
which is a linked list of blocks and gets the O(1) front for free.

```
 memory per element:
   python list slot      8 B  (a pointer; the int objects are shared or separate)
   Node with __slots__  48 B
   Node without         336 B
```

Six times with `__slots__`, forty times without. At ten million elements that is 80 MB against
480 MB — and against 3.4 GB if you forget `__slots__`, which is the difference between fitting in
memory and not.

### Space

```
 the list itself:  O(n) nodes
 traversal:        O(1) — one variable, and this matters
```

Every algorithm in this phase should use O(1) extra space. If your solution converts the list to a
Python list, works on that, and rebuilds — which is legal and sometimes the right answer — say that
you are trading O(n) space for simplicity, because the interviewer is watching for it.

---

## 7. The traps

### Trap 1 — losing the head

```python
    while head is not None:
        print(head.value)
        head = head.next            # the parameter now points at None
```

The loop works, prints correctly, and the caller's list is unaffected because Python passes the
reference by value — but *inside* your function you no longer have the head, so anything after the
loop that needs it is broken. **Always walk with a separate variable**: `node = head`, then move
`node`.

### Trap 2 — relinking in the wrong order

```python
    node.next = new_node                # WRONG ORDER
    new_node.next = node.next           # now points at ITSELF
```

`node.next` has already been changed, so `new_node.next` is set to `new_node`. You have built a cycle
of one node, and the next traversal hangs for ever with no error at all. **Point the new node at the
rest of the list first, then attach it.**

### Trap 3 — `AttributeError` on `None`

```python
    while node.next.value != target:      # two dots, two chances to be None
        node = node.next
```

```
AttributeError: 'NoneType' object has no attribute 'value'
```

The single most common error in this phase. Every `.next.next` is a promise that two more nodes
exist. Guard it: `while node.next is not None and node.next.value != target`.

### Trap 4 — the head as a special case

```python
def delete_value(head, value):
    node = head
    while node.next is not None:
        if node.next.value == value:
            node.next = node.next.next
            return head
        node = node.next
    return head                            # never checks the head itself
```

Deleting the first element silently does nothing. Every problem in this phase has this bug available,
which is exactly why [day 080](../day-080-dummy-head/README.md) exists — a dummy node before the head
makes the first element ordinary.

### Trap 5 — `while node:` instead of `while node is not None:`

These happen to be equivalent for a plain `Node` class, and stop being equivalent the moment somebody
adds `__len__` or `__bool__` to it — at which point a node holding an empty value is treated as the
end of the list. Write `is not None`. It also reads as what you mean.

### Trap 6 — forgetting that the caller's head does not update

```python
    push_front(head, 5)                   # return value discarded
    print(to_values(head))                # the 5 is not there
```

Python passes a reference *by value*, so rebinding `head` inside a function does not change the
caller's variable. Any operation that can change which node is first must **return the new head**,
and the caller must write `head = push_front(head, 5)`. This is the second-most-common bug in the
phase and it produces no error at all.

### Trap 7 — building a cycle by accident

```python
    last.next = head                      # now it never ends
```

```
KeyboardInterrupt
```

is what you get, eventually, from `to_values` on a cyclic list — or a `MemoryError` when the output
list eats your RAM. There is no exception for "this list has a cycle"; detecting it is
[day 083](../day-083-cycle-detection/README.md).

### Trap 8 — assuming a linked list is faster because it is "O(1) insertion"

The claim is true only when you already hold the node. If you have a position, you must walk to it,
and that walk is O(n) — the same as the array's shift, but with worse constants and worse cache
behaviour. Say the qualifier every time: **O(1) insertion *given the node*.**

---

## 8. In the interview

### How it gets asked

- The direct version, usually as a warm-up before a harder problem: *"What is a linked list, and when
  would you use one instead of an array?"*
- The implementation version: *"Implement a singly linked list with insert, delete and search."*
- The trick version: *"Delete a node from a linked list when you are given only that node."*
  LeetCode 237. It is a test of whether you will say "that is impossible for the tail".
- The memory version: *"Why is iterating a linked list slower than iterating an array, if both are
  O(n)?"* — they want cache locality.

### What to say out loud, in the first ninety seconds

1. **Define it by the one difference.** "An array's elements are contiguous in memory, so element `i`
   is found by arithmetic. A linked list's nodes are scattered and each holds a reference to the
   next, so the only way to reach the `k`th is to follow `k` links."
2. **Give both consequences immediately.** "So access by index is O(n) instead of O(1), and in
   exchange, inserting or deleting does not move anything."
3. **Say the qualifier that makes the trade honest.** "Insertion is O(1) *given the node*. If I am
   given a position, I have to walk there first, so both structures are O(n) — the array pays for the
   shift and the list pays for the walk."
4. **Name the real use.** "Where it genuinely wins is when something else already hands me the node —
   the LRU cache, where a hash map maps a key straight to its node, so unlinking is two assignments."
5. **Concede the costs.** "And the costs are real: about six times the memory per element in Python
   with `__slots__`, and about twice the traversal time, because each step is a reference to
   somewhere else in memory rather than the next slot in a block the processor already has."

### The follow-ups

**"If both traversals are O(n), why is the linked list slower?"**
"Cache locality. When the processor reads memory it fetches a whole cache line, typically 64 bytes,
so reading an array element brings the next several along for free — the loop mostly runs out of
cache. A linked list's nodes are wherever the allocator put them, so each step is likely to be a
fresh fetch, and the prefetcher cannot predict where you are going next because the address is inside
the data. I measured about twice the time on a million elements. Same complexity, different constant,
and the constant is what you feel."

**"When would you actually use one?"**
"Four cases. When something else hands me the node and I must splice it out in O(1) — that is the LRU
cache and it is the main one. When I only ever add and remove at the front, where 100,000 front
insertions were 1.4 seconds with `list.insert(0, x)` and 0.02 seconds with nodes. When a
reallocation copy is unacceptable, in real-time code or with very large elements. And when the
structure itself is the point — a tree is a node with two links, so everything after this phase is
built out of these. In day-to-day Python I would use a `list`, or a `deque` if I need both ends,
because a deque is a linked list of blocks and gets both properties."

**"Delete a node given only that node."**
"I cannot reach the node before it, so I cannot unlink it directly. Instead I copy the next node's
value into this node and unlink the next node — from outside, the effect is identical. It fails on
the tail, because there is no successor to steal from, and I would state that as a precondition
rather than let you find it. It also breaks any reference someone else is holding to the successor
node, which is worth mentioning if the nodes are shared."

**"How would you make length O(1)?"**
"Store it. Wrap the head in a small list class that keeps a `size` field and updates it on every
insertion and deletion. That is what real implementations do. The cost is that every mutation now has
to go through the class — a bare node graph cannot maintain it — and that is exactly the trade a
`LinkedList` class exists to make."

**"Singly or doubly linked?"**
"Doubly if I need to remove a node in O(1) when I only have that node, because unlinking needs both
neighbours. That is why the LRU cache is doubly linked. The cost is one extra reference per node —
eight more bytes — and twice as many pointer updates to get wrong, which is a real source of bugs.
Singly linked when I only ever walk forwards."

### A model answer

Asked: *what is a linked list, and when is it better than an array?*

> "A linked list is a chain of small objects. Each node holds a value and a reference to the next
> node, and you keep the first one, the head. Following `next` repeatedly is the only way to get
> anywhere.
>
> The whole structure comes out of one difference from an array. An array is a contiguous block, so
> the runtime knows where slot zero is and finds element `i` with one multiplication and one addition
> — constant time, whatever `i` is. A linked list's nodes are wherever the allocator happened to put
> them; node five might be a megabyte from node four. There is no arithmetic that gets you to the
> five-hundredth node, so you follow five hundred references.
>
> So access is O(n) instead of O(1). What I get in exchange is that inserting and deleting move
> nothing. Deleting from the middle of an array shifts every following element left; deleting from a
> linked list is one assignment — the previous node points at the next one, and the chain closes over
> the gap. That is the same whether the list has forty elements or forty thousand.
>
> But I want to state the qualifier, because it is where people overclaim. That insertion is O(1)
> *given the node*. If I am given a position — 'delete the five-hundredth element' — I have to walk
> there first, which is O(n), and then both structures are O(n): the array pays for the shift and the
> list pays for the walk. So 'linked lists are faster for insertion' is only true when something else
> already put the node in my hand.
>
> Which is exactly the LRU cache. A hash map maps the key straight to the node, so unlinking it is
> two assignments and never a search. That is the case where I would genuinely reach for one. The
> others are: when I only ever work at the front — I measured 100,000 front insertions at 1.4 seconds
> with `list.insert(0, x)` and 0.02 seconds building a chain, about sixty times — when a reallocation
> copy is unacceptable, and when the structure is the point, because a tree is just a node with two
> links.
>
> The costs are real and I would say them without being asked. Memory: a Python list slot is eight
> bytes; a node with `__slots__` is forty-eight, and without `__slots__` it is over three hundred. So
> six times the memory at best. Speed: I measured walking a million nodes at about twice the time of
> walking a million list elements. Same complexity, worse constant, and the reason is cache locality —
> the processor fetches a whole cache line at a time, so an array brings the next few elements along
> for free, while each node is a fresh trip to memory that the prefetcher cannot anticipate.
>
> So in ordinary Python I use a `list`, or a `deque` when I need both ends cheaply — a deque is
> internally a linked list of blocks, which is how it gets O(1) at both ends without the per-element
> overhead. I write an explicit linked list when I need O(1) splicing of a node I already hold, or
> when the interviewer has asked me to."

---

## 9. Recall card

- **A node is a value plus a reference to the next node; the head is just a name for the first one,
  and losing it loses the list.** In Python a variable holds a **reference**, not an object — so
  `node.next` is exactly a pointer, minus the address arithmetic.
- **One difference explains everything: an array is contiguous and finds element `i` by arithmetic;
  a linked list is scattered and must follow `k` links.** So access is **O(n) vs O(1)** — and in
  exchange, insertion and deletion **move nothing**.
- **Say the qualifier or the claim is wrong: insertion and deletion are O(1) *given the node*.** Given
  only a **position**, both structures are O(n) — the array pays for the shift, the list pays for the
  walk. The genuine win is when a **hash map hands you the node** (the LRU cache).
- **The measurements, at 1,000,000 elements:** traversal **0.062 s list vs 0.123 s linked — 2.0×**
  (cache locality, not complexity) · **100,000 front insertions: 1.443 s vs 0.0246 s — ~59×** ·
  memory **8 B per list slot vs 48 B per node with `__slots__` (336 B without)** — **6× at best**.
- **The three bugs that will cost you the next eight days.** Relink in the **wrong order** and a node
  points at itself — build the new node first, then attach. **`AttributeError: 'NoneType' object has
  no attribute 'next'`** — every `.next.next` promises two nodes exist. And **rebinding `head` inside
  a function does not change the caller's variable** — return the new head, always. The head as a
  special case is what **[day 080](../day-080-dummy-head/README.md)** deletes.
