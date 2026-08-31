---
day: 86
track: dsa
title: "Linked lists revision and mock round"
phase: "Linked lists"
status: written
---

# Day 086 · DSA — Linked lists revision and mock round

**After today you can:** You can solve two unseen pointer-surgery problems cold.

**The interviewer asks it as:** *Two problems, no hints, talk as you go.*

---

## 1. What this is, and why they ask it

Eight days ago a node was two fields. Since then you have inserted and deleted at any position, deleted
the head special case with a dummy node, reversed a list three ways, found the middle and the Nth from
the end in one pass, detected a cycle and proved where it starts, merged and sorted, and added a
second pointer to get O(1) removal.

Today is none of those. Today is **recognition**: looking at an unfamiliar linked-list problem and
knowing, within thirty seconds, which two or three of those techniques it is made of.

That is the actual skill, because linked-list problems are almost never one technique. "Reorder the
list" is the runner plus a reversal plus a merge. "Copy a list with random pointers" is a hash map or
an interleaving trick. "Is it a palindrome" is the runner plus a reversal plus a comparison, and then
a reversal back. A candidate who has memorised eight solutions freezes on the ninth. A candidate with
six trigger questions does not.

They run this round because the phase's techniques are small and combinable, which makes it very easy
to set a problem nobody has seen. The defence is not more problems. It is being able to say *what this
is made of* before writing anything.

---

## 2. The story

Ismail's cycle shop is the one under the peepal tree, and it is about the width of two cupboards.

People bring him bicycles in every state. He does not, as far as anyone has ever seen, take a bicycle
apart to find out what is wrong with it. He asks two questions and then he knows.

The first question is: does it happen when you pedal, or all the time? The second is: does it get worse
when you turn, or on a straight road?

That is it. Between those two answers he has, he says, about seven problems, and he has been fixing
those same seven for thirty-one years. Chain. Bearings. Brake rubbing. Wheel out of true. Bent
mudguard catching. Tyre. Something loose. He does not have a list written down anywhere; he just knows
that a noise when you pedal and not when you coast is one small family of things, and a noise that gets
worse on a turn is a completely different family, and once you know which family, the actual repair is
the easy part.

The boy who works with him now, Sameer, is quick and careful and much better with the newer bikes with
gears. And for the first six months he took things apart. A man would bring in a bicycle making a
noise and Sameer would have the chain off and the wheel out inside four minutes, and then he would sit
there in front of a bicycle in pieces, still not knowing what was wrong, and Ismail would come over,
lift the front end, spin the wheel, listen, and say bearings.

What Ismail told him, eventually, was not about bicycles. He said: you are very good at the repairs.
You are doing them in the wrong order. Find out which of the seven it is first, and then you will only
ever do one repair. If you start repairing before you know, you will do three.

Sameer says the change took about a month and that he now diagnoses more than he repairs, and that
customers think he has got faster at fixing bicycles, which is not what happened at all.

---

## 3. The idea in plain English

Ismail's two questions are the point. **Diagnose first, then repair** — and for linked lists there are
six questions, and every problem in this phase is one or two of them.

### The six trigger questions

Run these on any linked-list problem, in under thirty seconds.

**1. Can the operation change which node is first?**
→ **Dummy head** ([day 080](../day-080-dummy-head/README.md)). Remove-by-value, remove-Nth-from-end,
merge, partition, reverse-a-sublist. Write `dummy = Node(0, head)` and `return dummy.next` together,
before the loop.

**2. Do I need a position I cannot count to — the middle, or `n` from the end — in one pass?**
→ **The runner** ([day 082](../day-082-runner-technique/README.md)). Different *speeds* for the
middle; a fixed *gap* for a distance from the end.

**3. Might this list not end?**
→ **Floyd's** ([day 083](../day-083-cycle-detection/README.md)). Two runners; if the fast one catches
the slow one from behind, there is a cycle; then head-plus-meeting-point at equal speed finds the
entrance.

**4. Am I turning the arrows around?**
→ **The three-pointer reverse** ([day 081](../day-081-reversing-a-list/README.md)). *Save, turn,
previous up, current up.* Return `previous`.

**5. Am I combining two ordered things, or imposing order?**
→ **Merge**, and merge sort ([day 084](../day-084-merging-and-sorting-lists/README.md)). Builder
dummy, `<=` for stability, attach the remainder in one assignment.

**6. Do I already hold the node I must remove?**
→ **Doubly linked** ([day 085](../day-085-doubly-and-circular/README.md)). Two assignments, O(1). If
I have to *search* for the node first, the search is O(n) and the second pointer buys nothing.

### The five sentences that carry the phase

1. **"To change the list at position k, I must be standing at k−1."** You cannot reach backwards, so
   every insertion and deletion is really "walk to the node before".
2. **"Save the next node before you overwrite the pointer."** The defining mistake of the phase:
   overwrite `current.next` first and the rest of the list is gone, with no error.
3. **"Return `dummy.next`, never `head`."** And its cousin: a bare function that changes the first node
   must *return* the new head, because rebinding a parameter changes nothing for the caller.
4. **"Insertion is O(1) *given the node*."** Given a position, both a list and an array are O(n) — one
   pays for the walk, the other for the shift.
5. **"Advance only when you keep."** After unlinking, `previous.next` is a node you have not inspected.

### The one-page comparison

| Technique | Cost | Space | Use it when |
|---|---|---|---|
| Traverse with `previous` | O(n) | O(1) | Delete or insert by position or value |
| Dummy head | — | O(1) | The first node can change, or you are building a list |
| Reverse (iterative) | O(n) | O(1) | Turning arrows; also the O(1)-space half of palindrome |
| Reverse (recursive) | O(n) | **O(n) stack** | Never in Python past ~1000 nodes |
| Runner, different speeds | O(n) | O(1) | The middle, in one pass |
| Runner, fixed gap | O(n) | O(1) | The Nth from the end, in one pass |
| Floyd's | O(n) | O(1) | Cycle detection, and the entrance |
| Merge two sorted | O(n+m) | O(1) | Combining; also the inner loop of a sort |
| Merge sort | O(n log n) | O(log n) | Sorting a list; O(1) if bottom-up |
| Doubly linked | O(1) removal | +8 B/node | You already hold the node (LRU) |
| Hash map of nodes | O(n) | **O(n)** | The honest baseline for cycles and for copying |

### What the round is actually scoring

Four things, in this order of weight:

1. **Did you say what the problem is made of, before coding?** "This is the runner to find the middle,
   then a reverse of the second half, then an interleave." That sentence is the answer.
2. **Did you draw the pointers before assigning them?** Every bug in this phase is an assignment made
   before its picture existed.
3. **Did you handle the empty list, one node, and two nodes?** All three, out loud, before you claim to
   be finished.
4. **Did you leave the caller's data as you found it**, or say that you did not? A function asked to
   *inspect* a list must not return it reversed.

---

## 4. The picture

The whole phase, grouped by the question that triggers it.

```
 "can the first node change?"                     -> DUMMY HEAD
   +-- remove all nodes equal to v                   guard form: Node(0, head)
   +-- remove the nth from the end                   builder form: Node(0) + tail
   +-- merge two sorted lists
   +-- partition around a value
   +-- reverse a sublist

 "a position I cannot count to, in one pass?"     -> RUNNER
   +-- the middle                                    different SPEEDS (1 and 2)
   |     +-- first middle  -> splitting for a sort
   |     +-- second middle -> "return the middle"
   +-- the nth from the end                          fixed GAP

 "might it not end?"                              -> FLOYD'S
   +-- has a cycle                                   meet => cycle
   +-- where does the cycle start                    head + meeting, equal speed
   +-- find the duplicate number                     read the array as i -> nums[i]

 "turning the arrows around?"                     -> THREE-POINTER REVERSE
   +-- reverse the whole list                        save, turn, previous up, current up
   +-- reverse positions m..n                        capture the future tail FIRST
   +-- reverse in groups of k                        COUNT before reversing

 "combining, or imposing order?"                  -> MERGE
   +-- merge two sorted                              attach the remainder in ONE line
   +-- sort a list                                   split (first middle + CUT), sort, merge
   +-- merge k sorted                                pairwise rounds, or a heap

 "do I already hold the node?"                    -> DOUBLY LINKED
   +-- LRU cache                                     map answers WHERE, list answers CHEAPLY
   +-- browser history, playlists                    circular: no first, no last, no None
```

Six questions. **Every problem in eight days is one or two of them**, and that compression is what you
are trying to walk into the room with.

And the three error messages, which between them account for most of your debugging:

```
 AttributeError: 'NoneType' object has no attribute 'next'
   -> a `.next.next` where only one node was guaranteed. Guard, or use a sentinel.

 RecursionError: maximum recursion depth exceeded
   -> recursive reverse past ~1000 nodes, OR a split that does not shrink
      (second middle, or a missing cut)

 (no error at all — the program hangs, or memory fills)
   -> a cycle you built by accident, or `while node is not None` on a circular list
```

The third is the dangerous one, because there is nothing to read.

---

## 5. The code, built step by step

Two problems, worked the way you would work them in the room: the diagnosis out loud, then the code.

### Problem one: *"Reorder the list `L0 → L1 → … → Ln` into `L0 → Ln → L1 → Ln−1 → …`, in place."*

**Diagnose first, out loud.**

"Let me say what this is made of before I write anything. I need the second half in reverse order,
interleaved with the first half. So: find the middle — that is the runner. Reverse the second half —
that is the three-pointer loop. Then weave the two together, one node from each. Three techniques I
already have, and no new idea."

"One thing to settle: which middle. `[1,2,3,4]` should become `[1,4,2,3]`, so the first half is `[1,2]`
and the second is `[3,4]` — the **first** middle, and I cut there so the halves are genuinely
separate."

**Then the code, in fragments.**

```python
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                          # the cut, in the same breath
```

```python
    previous = None
    while second is not None:
        second.next, previous, second = previous, second, second.next
    second = previous                         # the reversed second half
```

The tuple assignment is the four lines compressed; if it makes you nervous under pressure, write them
out. Say which you are doing and why.

```python
    first = head
    while second is not None:
        first_next, second_next = first.next, second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next
```

**Say the loop's invariant while writing it:** the second half is the same length or one shorter, so
looping while `second` is not `None` terminates correctly and the last node ends up pointing at
`None` on its own.

**Then the edge cases, out loud.** "Empty and single-node lists return unchanged, so I guard at the
top. `[1,2]` becomes `[1,2]`, which is correct. `[1,2,3]` becomes `[1,3,2]`."

**Then the complexity.** "Three passes, each O(n), so O(n) time and O(1) space — nothing is allocated,
only relinked."

### Problem two: *"Each node has `next` and an extra `random` pointer to any node or `None`. Make a deep copy."*

**Diagnose first.**

"The difficulty is that `random` can point *forward* to a node I have not created yet. So I cannot
build the copy in one pass unless I have a way to map an original node to its copy."

"The obvious solution is a hash map from original node to copy: one pass to create all the copies, a
second to wire up both pointers. O(n) time, O(n) space. I would say that first because it is clean and
correct."

"There is an O(1)-space trick, and it is worth knowing: interleave each copy directly after its
original, so `A → A' → B → B' → …`. Then the copy of any node is simply `node.next`, which is the map,
stored in the list itself. Three passes: interleave, set the random pointers, then unweave."

**The map version.**

```python
    mapping = {None: None}
    node = head
    while node is not None:
        mapping[node] = Node(node.value)      # create every copy first
        node = node.next

    node = head
    while node is not None:
        mapping[node].next = mapping[node.next]
        mapping[node].random = mapping[node.random]
        node = node.next
    return mapping[head]
```

`mapping[None] = None` at the start removes every "is this pointer null" branch from the second loop —
the same trick as a sentinel, applied to a dictionary.

**The interleaving version**, which is the one that gets remembered:

```python
    node = head                               # pass 1: A -> A' -> B -> B'
    while node is not None:
        copy = Node(node.value)
        copy.next, node.next = node.next, copy
        node = copy.next
```

```python
    node = head                               # pass 2: the random pointers
    while node is not None:
        if node.random is not None:
            node.next.random = node.random.next    # the copy of X is X.next
        node = node.next.next
```

`node.random.next` **is** the copy of `node.random`. That single expression is the whole trick, and it
is worth pointing at rather than letting the interviewer decode it.

```python
    node, copy_head = head, head.next         # pass 3: unweave, restoring the original
    while node is not None:
        copy = node.next
        node.next = copy.next
        copy.next = copy.next.next if copy.next else None
        node = node.next
    return copy_head
```

**Restoring the original list is mandatory**, not optional tidiness. The caller handed you a list to
copy, not to mangle, and a version that leaves it interleaved passes every test that only checks the
copy.

### The reference implementations, for revision

```python
class Node:
    __slots__ = ("value", "next", "random")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next
        self.random: "Node | None" = None


def from_values(values: list[int]) -> Node | None:
    head: Node | None = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def to_values(head: Node | None) -> list[int]:
    out, node = [], head
    while node is not None:
        out.append(node.value)
        node = node.next
    return out


def reverse(head: Node | None) -> Node | None:
    """Save, turn, previous up, current up. Return `previous`."""
    previous, current = None, head
    while current is not None:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    return previous


def first_middle(head: Node) -> Node:
    """The FIRST middle, which is what splitting needs so both halves shrink."""
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    return slow


def reorder(head: Node | None) -> Node | None:
    """L0 -> Ln -> L1 -> Ln-1 -> ...  in place.

    Three techniques: the runner finds the middle, the three-pointer loop
    reverses the second half, and an interleave weaves them together.
    O(n) time, O(1) space — nothing is allocated, only relinked.
    """
    if head is None or head.next is None:
        return head

    middle = first_middle(head)
    second = reverse(middle.next)
    middle.next = None                        # the cut

    first = head
    while second is not None:
        first_next, second_next = first.next, second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next
    return head


def copy_with_random_map(head: Node | None) -> Node | None:
    """Deep copy with an extra `random` pointer. O(n) time, O(n) space.

    The honest baseline: a map from original node to copy, so a forward
    `random` pointer can be resolved in the second pass.
    mapping[None] = None removes every null check from that pass.
    """
    mapping: dict[Node | None, Node | None] = {None: None}
    node = head
    while node is not None:
        mapping[node] = Node(node.value)
        node = node.next

    node = head
    while node is not None:
        mapping[node].next = mapping[node.next]
        mapping[node].random = mapping[node.random]
        node = node.next
    return mapping[head]


def copy_with_random_interleaved(head: Node | None) -> Node | None:
    """The same thing in O(1) extra space, by storing the map IN the list.

    Interleave each copy after its original, so the copy of X is X.next.
    Then the random pointers are node.next.random = node.random.next.
    Three passes, and the third RESTORES the caller's list — mandatory.
    """
    if head is None:
        return None

    node = head                                # 1. A -> A' -> B -> B'
    while node is not None:
        copy = Node(node.value)
        copy.next = node.next
        node.next = copy
        node = copy.next

    node = head                                # 2. the copy of X is X.next
    while node is not None:
        if node.random is not None:
            node.next.random = node.random.next
        node = node.next.next

    node = head                                # 3. unweave, restoring the original
    copy_head = head.next
    while node is not None:
        copy = node.next
        node.next = copy.next
        copy.next = copy.next.next if copy.next is not None else None
        node = node.next
    return copy_head


def has_cycle(head: Node | None) -> bool:
    """Two runners. Advance first, compare by IDENTITY."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def merge_two(a: Node | None, b: Node | None) -> Node | None:
    """Builder dummy, `<=` for stability, remainder in one assignment."""
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def remove_nth_from_end(head: Node | None, n: int) -> Node | None:
    """Fixed gap, both pointers starting at the dummy so `slow` lands on the
    PREDECESSOR and removing the head needs no special case."""
    dummy = Node(0, head)
    fast = slow = dummy
    for _ in range(n):
        if fast.next is None:
            raise ValueError(f"list has fewer than {n} nodes")
        fast = fast.next
    while fast.next is not None:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next


if __name__ == "__main__":
    print(to_values(reorder(from_values([1, 2, 3, 4, 5]))))   # [1, 5, 2, 4, 3]
    print(to_values(reorder(from_values([1, 2, 3, 4]))))      # [1, 4, 2, 3]
    print(to_values(reorder(from_values([1, 2]))))            # [1, 2]
    print(to_values(reorder(from_values([1]))))               # [1]
    print(to_values(reorder(None)))                           # []

    # a list with random pointers: 1 -> 2 -> 3, randoms 1->3, 2->1, 3->None
    a, b, c = Node(1), Node(2), Node(3)
    a.next, b.next = b, c
    a.random, b.random, c.random = c, a, None

    for copier in (copy_with_random_map, copy_with_random_interleaved):
        copy = copier(a)
        print(to_values(copy),
              copy.random.value, copy.next.random.value, copy.next.next.random)
        assert copy is not a and copy.random is not c        # a real deep copy
        assert to_values(a) == [1, 2, 3] and a.random is c   # original UNCHANGED
    print("both copies are deep, and the original survived")

    print(to_values(merge_two(from_values([1, 3]), from_values([2, 4]))))   # [1,2,3,4]
    print(to_values(remove_nth_from_end(from_values([1, 2, 3, 4, 5]), 2)))  # [1,2,3,5]
    print(has_cycle(from_values([1, 2, 3])))                  # False
```

---

## 6. What it costs

### The whole phase, priced

```
 traverse / search              O(n) time,  O(1) space
 insert or delete at position k O(k) time,  O(1) space
 insert or delete GIVEN a node  O(1) singly (after), O(1) doubly (either side)
 reverse, iterative             O(n) time,  O(1) space
 reverse, recursive             O(n) time,  O(n) STACK
 middle / nth from end          O(n) time,  O(1) space, ONE pass
 cycle detection                O(n) time,  O(1) space
 cycle start                    <= a + c then exactly a, so O(n), O(1)
 merge two sorted               O(n+m) time, O(1) space
 merge sort                     O(n log n) time, O(log n) stack (O(1) bottom-up)
 merge k sorted                 O(n log k) time
 doubly linked removal          O(1) time,  +8 B per node
```

**Every single one is O(1) space except the recursive reversal and the merge sort's stack.** That is
the shape of the phase: linked-list algorithms move pointers, they do not allocate. If your solution
allocates, say what you traded.

### The measurements to quote

```
 1. traversal, 1,000,000 elements
      python list  0.0621 s  |  linked list  0.1232 s      2.0x  (cache locality)
 2. 100,000 insertions at the FRONT
      list.insert(0,x)  1.443 s  |  node push_front  0.0246 s   ~59x
 3. memory per element
      list slot 8 B  |  Node with __slots__ 48 B  |  without __slots__ 336 B
 4. LRU cache read at capacity 100,000
      doubly linked ~6 pointer writes  |  singly linked ~100,000 steps   ~10^4 x
```

One real measurement beats three complexity classes. Number 2 is the linked list's only unambiguous
win; number 1 is the honest cost.

### Space, side by side

```
 in-place pointer surgery       O(1)   — the default, and what interviews want
 hash map of nodes              O(n)   — the baseline for cycles and for deep copy
 copy values into a list        O(n)   — legitimate, but say what you traded
 recursion                      O(n)   — and RecursionError past ~1000 in Python
```

### The complexity claims that get probed

- *"Insertion in a linked list is O(1)."* → **only given the node.** Given a position, both structures
  are O(n).
- *"Your sort is O(n log n)."* → every level does `n` work, and there are `log₂ n` levels, about 20 at
  a million nodes.
- *"Floyd's is O(n)."* → at most `a + c` for phase one and exactly `a` for phase two, so at most `2n`.
- *"One pass is faster than two."* → **same asymptotics and about the same pointer moves**; what it
  buys is one traversal instead of two, which matters when each node is a fresh cache miss.

---

## 7. The traps

The complete list for the phase. Each one has cost somebody an interview.

### Overwriting a pointer before saving what it pointed at

The defining mistake. `current.next = previous` before `next_node = current.next`, and the rest of the
list is unreachable. `[1,2,3]` reverses to `[1]`, with no error.

### Returning `head` instead of `previous` or `dummy.next`

After a reversal, `head` is the last node. After a removal, `head` may be a deleted node. Both return
a wrong answer silently.

### Rebinding a parameter and expecting the caller to see it

```python
    push_front(head, 5)          # return value discarded — nothing happens
```

Python passes the reference by value. Any function that can change the first node must **return the
new head**, and the caller must assign it.

### `.next.next` with only one node guaranteed

```
AttributeError: 'NoneType' object has no attribute 'next'
```

Every double dereference is a promise that two nodes exist. Guard it, and put the null check first
because `and` short-circuits.

### The head as a special case, handled with an `if` instead of a dummy

On `[7,7,7,1]` the head is a *run*, so an `if` is not enough — and then everything-deleted is a second
branch. A dummy takes the count to zero.

### Advancing after a deletion

`[1,7,7,2]` becomes `[1,7,2]`. After unlinking, `previous.next` is a node you have not inspected.
**Advance only in the `else`.**

### The wrong middle when splitting

The second middle leaves `[1,2]` as `[1,2]` and `[]`, so a merge sort never terminates. **Splitting
needs the first middle.**

### Forgetting the cut

`slow.next = None`. Without it both halves are the whole list. Same `RecursionError`, different cause.

### The off-by-one in the runner's expiry or gap

`window[0] <= index - k`, derived not memorised. And the opening walk must check for a short list, or
it dereferences `None`.

### Returning the meeting point as the cycle's start

It is only right when `a = 0` — a list that is entirely one cycle, which is exactly the case people
test with.

### Comparing nodes with `==` instead of `is`

Fine until someone defines `__eq__` on the value, at which point two distinct nodes holding equal
values report a cycle that does not exist.

### `while node is not None` on a circular list

There is no `None`. The program hangs with no error.

### Updating only one direction in a doubly linked list

Correct forwards, broken backwards. Every forward test passes and it falls apart later, elsewhere.
Write the both-ways `_check`.

### Not terminating a list built from existing nodes

`more.next = None` in partition, `tail.next = None` after a heap merge. Without it you build a cycle
and printing never returns.

### The heap in "merge k lists" with no tie-breaker

```
TypeError: '<' not supported between instances of 'Node' and 'Node'
```

Fires the moment two heads are equal. Add an index to the tuple.

### Mutating the caller's list in a read-only operation

The palindrome check that leaves the second half reversed; the deep copy that leaves the list
interleaved. Both return the right answer and hand back damaged data.

### Recursion in Python

```
RecursionError: maximum recursion depth exceeded
```

at about a thousand nodes. Not an edge case — an ordinary input. And raising the limit turns a clean
exception into a segmentation fault.

---

## 8. In the interview

### How it gets asked

- The plain mock: *"Two problems, forty-five minutes, talk as you go."*
- The composite, which is the standard hard linked-list question: *"Reorder the list"*, *"is it a
  palindrome, in O(1) space"*, *"copy a list with random pointers"*, *"reverse in groups of k"*.
- The design question wearing a list costume: *"design an LRU cache"*, *"design browser history"*.
- The reasoning probe: *"why a linked list rather than an array?"* — and the answer must contain the
  words "given the node".
- The trap: *"just use `sorted()`"* — say what you traded.

### The script, minute by minute, for a 45-minute round

**Minutes 0–3 — restate and clarify.** Say the problem back. Ask the three things that always matter
here: can the list be empty; can the first node change; and may I modify the input list. That third
question is specific to this phase and asking it is a strong signal.

**Minutes 3–6 — diagnose out loud.** Ismail's two questions. "This is the runner to find the middle,
then a reversal, then an interleave." Name the pieces before writing any of them. If you cannot name
them, say what the baseline O(n)-space solution is and improve from there.

**Minutes 6–10 — draw the pointers.** Two or three boxes and arrows, and what each arrow should point
at afterwards. Every bug in this phase is an assignment made before its picture existed.

**Minutes 10–25 — code, narrating.** Write the dummy and its `return dummy.next` together. Say "save
first" as you write the save. Say "advance only when I keep" as you write the `else`.

**Minutes 25–30 — trace the degenerate case out loud.** Empty, one node, two nodes. Finding your own
off-by-one reads far better than having it pointed out.

**Minutes 30–35 — complexity, with the counting**, and say the space explicitly, including whether you
mutated the input.

**Minutes 35–45 — the second problem**, faster, because the diagnosis is now warm.

### The follow-ups

**"Why a linked list rather than an array?"**
"Only for O(1) insertion and deletion **given the node** — and that qualifier is the whole answer. If I
have a position rather than a node, both are O(n): the array pays for the shift and the list pays for
the walk. The genuine wins are when something else hands me the node, like a hash map in an LRU cache;
when I only ever work at the front, where a hundred thousand front insertions were 1.4 seconds against
0.02; and when the structure itself is the point, since a tree is a node with two links. Otherwise an
array wins on memory — 8 bytes a slot against 48 — and on traversal, about twice as fast, because of
cache locality."

**"Can you do it in O(1) space?"**
"Usually yes, and that is what these problems are for. The pattern is: replace a hash map of nodes with
information stored *in* the list. Cycle detection replaces a set of visited nodes with two runners.
Copying a list with random pointers replaces the map with interleaving each copy after its original,
so the copy of X is X.next. Reversal is already O(1) if it is iterative. The one place I cannot is a
recursive solution, which is O(n) stack by definition."

**"May I modify the input?"**
"That is the question I would ask *you*, and it changes the answer. If yes, the palindrome check can
reverse the second half in place and be O(1) space. If no, I would either copy the values into an
array — O(n) space, and I would say so — or reverse and then reverse back, restoring the list before
returning. Silently handing back a mangled list is the bug in this phase that no test catches."

**"Is that not quadratic?"**
"No, and let me count rather than assert. In a merge sort, every level does `n` work and there are
`log₂ n` levels. In Floyd's, phase one is at most `a + c` and phase two is exactly `a`, so at most
`2n`. In a merge, every node is attached exactly once. The one place it *is* quadratic is appending to
a list with no tail reference — `n` appends is `n(n+1)/2` steps, about five billion at a hundred
thousand — which is the classic accidental quadratic here."

**"What is the most common bug in your code?"**
A good answer to have ready: "Assignment order. Overwriting `current.next` before saving what it
pointed at, or attaching a new node to a neighbour before the new node knows both its neighbours. Both
lose part of the list and neither raises. So I write the save first, and I draw the two boxes before I
type the assignments."

### A model answer

Asked: *reorder the list so it goes first, last, second, second-last, and so on — in place.*

> "Before writing anything, let me say what this is made of, because it is three things I already have
> rather than one new idea.
>
> I need the second half of the list, reversed, interleaved with the first half. So: find the middle
> with two runners, one moving one step and one moving two. Reverse the second half with the
> three-pointer loop. Then weave them together, one node from each. Nothing gets allocated — it is all
> relinking — so this should be O(n) time and O(1) space.
>
> One decision to settle first: which middle. On `[1,2,3,4]` the answer is `[1,4,2,3]`, so the halves
> are `[1,2]` and `[3,4]` — that is the **first** middle, the one where the loop condition looks two
> nodes ahead. And I cut immediately: set the first half's last node's `next` to `None`, in the same
> breath as finding it, or the two halves are still one list and the interleave will loop.
>
> The reversal is the standard four lines: save the next node, turn this arrow round, move `previous`
> up, move `current` up. Save first, always — the moment I overwrite `current.next` I have lost my only
> reference to the rest, and that failure produces no error, just a shorter list.
>
> The interleave is four assignments per step. I hold `first_next` and `second_next` before touching
> anything, because both are about to be overwritten. Then first points at second, second points at
> `first_next`, and both cursors advance. The second half is the same length or one shorter, so looping
> while `second` is not `None` terminates correctly, and the final node ends up pointing at `None`
> without a special case.
>
> Edge cases before I say I am done: empty and one node return unchanged, which I guard at the top.
> `[1,2]` should come out as `[1,2]`, and it does. `[1,2,3]` becomes `[1,3,2]`.
>
> Complexity: three passes over the list, each O(n), so O(n) time. O(1) space — three or four
> references, and nothing allocated.
>
> One thing I would confirm with you: this modifies the caller's list in place, which is what 'in
> place' asks for. If it had been a read-only question I would either work on a copy or restore the
> list before returning, because handing back a rearranged list that the caller did not expect is the
> kind of bug that passes every test."

---

## 9. Recall card

- **Six trigger questions cover eight days.** *Can the first node change?* → **dummy head**. *A position
  I cannot count to, in one pass?* → **runner** (speeds for the middle, a gap for the end). *Might it
  not end?* → **Floyd's**. *Turning the arrows?* → **three-pointer reverse**. *Combining or ordering?*
  → **merge**. *Do I already hold the node?* → **doubly linked**. Diagnose first, then repair.
- **The five sentences.** *Stand at k−1.* · ***Save the next node before you overwrite the pointer.*** ·
  *Return `dummy.next`, never `head` — and a bare function must return the new head.* · *Insertion is
  O(1) **given the node**.* · *Advance only when you keep.*
- **Composites are the real questions, and they are two or three techniques each.** Reorder = runner +
  reverse + interleave. Palindrome in O(1) = runner + reverse + compare + **reverse back**. Copy with
  random pointers = a node map, or **interleave so the copy of X is `X.next`** and then unweave to
  **restore the caller's list**. Sort = split (first middle + **cut**) + merge.
- **Almost everything here is O(1) space — if yours allocates, say what you traded.** The exceptions
  are the recursive reverse (**O(n) stack, `RecursionError` at ~1000**) and merge sort's O(log n).
  The measurements: traversal **2× slower** than a list, **~59×** faster at front insertion, **48 B vs
  8 B** per element, and the LRU read **~10⁴×** worse with a singly linked list.
- **The traps that end rounds:** overwriting before saving · `return head` · discarding the returned
  head · `.next.next` unguarded · the head as an `if` instead of a dummy · advancing after a deletion ·
  the **second** middle when splitting · the missing **cut** · returning the meeting point as the cycle
  start · `==` instead of `is` · `while node is not None` on a circular list · one direction updated ·
  an unterminated built list · a heap with no tie-breaker · and **mutating the caller's list in a
  read-only operation**.
