---
day: 83
track: dsa
title: "Cycle detection, and why Floyd's algorithm works"
phase: "Linked lists"
status: written
---

# Day 083 · DSA — Cycle detection, and why Floyd's algorithm works

**After today you can:** You can detect a cycle, find where it starts, and explain the two-pointer proof simply.

**The interviewer asks it as:** *Detect a cycle in a linked list. Now find the node where it begins.*

---

## 1. What this is, and why they ask it

A linked list has a **cycle** if some node's `next` points back at a node you have already visited.
Then the list has no end: walking it never reaches `None`, and any loop written the ordinary way runs
for ever.

**Floyd's cycle detection** — the tortoise and the hare — finds out in O(n) time and O(1) space. Send
one pointer forward one step at a time and another two steps at a time. If the list ends, the fast one
falls off. If it loops, the fast one comes round and catches the slow one from behind, and **that
meeting is the proof.**

Then comes the part that makes this a real interview question rather than a trick: *find the node
where the cycle begins.* The answer is three lines and looks like magic — put one pointer back at the
head, move both one step at a time, and they meet exactly at the entrance. You will be asked why it
works, and "I memorised it" is a visible answer. The arithmetic is four lines and worth having.

They ask it because the hash-set solution is obvious and the O(1)-space solution is not, because the
proof separates people who understand from people who recall, and because the same algorithm answers
questions that are not about linked lists at all — *find the duplicate number in an array*
(LeetCode 287) is this algorithm in disguise.

---

## 2. The story

The park behind the water tank has one path in and one loop, and Ravi has walked it most mornings for
eleven years.

From the gate a straight path runs past the swings to a junction by the big tree — three hundred
metres, give or take. At the junction the loop begins, and the loop is about eight hundred metres and
comes back to that same tree. So "doing the track" means walking out along the path and then round,
and round, and round.

Manju joined him about two years ago, and Manju does not walk. He jogs, at roughly twice Ravi's pace,
which they established once by counting steps and arguing.

They set off together from the gate and they do not stay together. Manju pulls away, disappears round
the loop, and then — this is the part Ravi still finds slightly annoying — comes up behind him. Not
towards him. **Behind him.** Somewhere on the far side of the loop, most mornings near the broken
bench, Manju taps his shoulder on the way past.

Ravi's daughter pointed out what that actually means, one Sunday when she came along.

If the path had no loop — if it just ended at a wall — Manju would reach the wall and that would be
that. He would be standing there waiting. He could never come up behind Ravi, because there is no
behind. The only way a faster person catches a slower one **from behind** is if the route comes back
on itself.

So the tap on the shoulder is not a coincidence of pace. It is a fact about the shape of the park.

The second thing they worked out took them three attempts and they still cannot explain why it works,
though Ravi's daughter did the numbers on the back of her hand and said it was obvious.

They wanted to know exactly where the loop begins — which tree, precisely, because there are two big
trees near each other and they had been arguing about it for a year.

What she told them to do was this. Manju stays exactly where he tapped Ravi's shoulder. Ravi walks
back to the gate. Then both of them set off at the **same** speed — Manju continuing round the loop,
Ravi coming in along the path from the gate.

They meet at the junction. Every time. The correct tree, settled.

---

## 3. The idea in plain English

The park is the shape every list with a cycle has: **a straight bit, then a loop.** People draw it as
the Greek letter rho, ρ — a tail and a circle.

### Phase one: is there a loop at all?

```python
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True             # the tap on the shoulder
    return False                    # fast fell off the end: no loop
```

The same two runners as [day 082](../day-082-runner-technique/README.md), asking a different question.
There are exactly two possible outcomes:

- **`fast` reaches `None`.** The route ends. No cycle. This is the wall.
- **`fast` catches `slow`.** They are on the same node. There is a cycle — and there must be, because a
  faster runner can only come up *behind* a slower one on a route that returns to itself.

**Compare with `is`, not `==`.** You are asking whether they are on the same *node*, not whether two
nodes hold the same value. `==` on two different nodes with equal values would report a cycle that
does not exist.

### Why they must meet, rather than skip past each other

The one gap in the obvious argument: could the fast runner jump *over* the slow one and keep missing?

No, and the reason is simple. Once both are inside the loop, look at the distance from `fast` to
`slow` going forwards round the loop. Each step, `slow` advances one and `fast` advances two, so that
gap **shrinks by exactly one every step.** A gap that decreases by exactly one can never jump from 1
to −1; it must pass through 0. So they land on the same node.

That is the whole argument and it fits in two sentences. It is also why the speed ratio must be 2 and
1 rather than, say, 3 and 1 — with a gap shrinking by two each step, they could indeed skip past each
other on a cycle of odd length.

### Phase two: where does the loop begin?

```python
    finder = head
    while finder is not slow:
        finder = finder.next
        slow = slow.next
    return finder                   # the junction
```

Manju standing still while Ravi walks back to the gate, then both moving at the same pace. Three
lines, and the interviewer will ask why.

### The proof, in four lines of arithmetic

Name three distances, in nodes:

```
 a = from the head to the start of the cycle      (the path from the gate)
 b = from the start of the cycle to the meeting   (round to the broken bench)
 c = the length of the cycle                      (once round)
```

When they meet:

```
 slow has walked   a + b
 fast has walked   a + b + kc          — the same place, having gone k full laps more
 fast walked twice as far:
   2(a + b) = a + b + kc
        a + b = kc
            a = kc - b
```

Read that last line as an instruction. **From the meeting point, walking `a` more steps takes you `b +
a = kc` steps into the cycle — a whole number of laps — which lands you exactly back at the start of
the cycle.** And walking `a` steps from the head also lands you at the start of the cycle, by
definition of `a`.

So two pointers, one at the head and one at the meeting point, both moving one step at a time, arrive
at the cycle's start at the same moment. That is the whole proof, and you can say it in thirty
seconds.

The common case `k = 1` makes it concrete: `a = c − b`. The distance from the head to the junction
equals the distance from the meeting point round to the junction. Ravi's three hundred metres of path
equals the remaining stretch of loop from the broken bench back to the tree.

### The length of the cycle, if asked

Stay at the meeting point and walk until you come back to it, counting:

```python
    length, node = 1, meeting.next
    while node is not meeting:
        node = node.next
        length += 1
```

O(c), no extra space.

### The obvious solution, named and rejected

```python
    seen = set()
    node = head
    while node is not None:
        if node in seen:            # by IDENTITY — nodes are unhashable by value here
            return node
        seen.add(node)
        node = node.next
```

Correct, O(n) time, **O(n) space**, and it gives you the cycle's start for free with no proof
required. Say it first, then say why you are not writing it: at a million nodes that is a set holding
a million references — roughly 32 MB — to answer a question that needs two variables.

It is not a bad answer. It is the answer you give if you cannot recall Floyd's, and it is far better
than nothing. Volunteer it as the baseline, and then improve it.

### Where this shows up when it is not a linked list

**Find the Duplicate Number** (LeetCode 287): an array of `n + 1` integers, each between 1 and `n`,
with exactly one value repeated. Treat the array as a function — from index `i`, go to index
`nums[i]`. Because values are in `1..n`, following that never leaves the array, so the walk must
eventually repeat: it is a rho shape. The duplicate value is the entrance to the cycle, and Floyd's
finds it in O(1) space without modifying the array. That reframing is a genuinely hard leap and it is
worth knowing it exists.

**Happy Number** (LeetCode 202) is the same idea over "replace the number with the sum of the squares
of its digits".

---

## 4. The picture

The rho shape, with the three distances marked.

```
   head
    |
    v
   [1] -> [2] -> [3] -> [4] -> [5]
    |<--- a = 3 --->|      |     |
                    ^      v     |
                   [6] <- [7] <--+          (drawn flat; 4->5->7->6->4 is the loop)
                    |
              cycle start

   a = nodes from the head to the cycle start
   b = nodes from the cycle start to where they meet
   c = the number of nodes in the cycle
```

Now the walk itself, on a list of six nodes where the cycle starts at node 3 and has length 4:

```
 nodes:  1 -> 2 -> 3 -> 4 -> 5 -> 6 -+
                   ^                 |
                   +-----------------+

 step  slow   fast
 ----  ----   ----
  0      1      1
  1      2      3
  2      3      5
  3      4      3        fast has lapped
  4      5      5        MEET at node 5

 a = 2 (nodes 1, 2 before the cycle)
 b = 2 (from node 3 to node 5)
 c = 4 (nodes 3, 4, 5, 6)
 check: a + b = 4 = kc with k = 1.  Correct.

 phase two:
   finder = head = 1,  slow stays at 5
   step 1: finder = 2, slow = 6
   step 2: finder = 3, slow = 3      MEET at node 3 = the cycle start
```

What to notice: they meet at node 5, which is **not** the cycle start, and phase two walks exactly
`a = 2` more steps to reach it. The meeting point is almost never the entrance, and any solution that
returns it is wrong on most inputs.

And the reason a faster runner cannot jump over a slower one:

```
 distance from fast to slow, going forwards round the loop:

   step 0:  gap = 3
   step 1:  gap = 2        slow +1, fast +2  ->  gap shrinks by exactly 1
   step 2:  gap = 1
   step 3:  gap = 0        they are on the same node

 a gap that decreases by exactly one cannot skip 0.
```

---

## 5. The code, built step by step

### Step 1 — detection, and the comparison that matters

```python
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

Advance **first**, then compare. Comparing before advancing would report a cycle immediately, since
both start on the head. And `is`, not `==`: you are asking about node identity.

### Step 2 — the loop condition, which is the same two guards as yesterday

`fast is not None` covers an even-length tail where `fast` lands exactly on `None`; `fast.next is not
None` covers an odd one where `fast.next.next` would raise. The null check must come first because
`and` short-circuits.

### Step 3 — phase two, returned from phase one

```python
    finder = head
    while finder is not slow:
        finder = finder.next
        slow = slow.next
    return finder
```

Note there is no `while True` and no length check — the arithmetic guarantees they meet, and they meet
within `a` steps. If your phase two has a safety counter in it, you do not believe your own proof.

### Step 4 — restructuring so both phases live in one function

```python
def find_cycle_start(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break                       # meeting point found; slow is standing on it
    else:
        return None                     # the loop ended normally: no cycle
```

The `while ... else` runs the `else` only when the loop finished **without** `break`, which is exactly
"no cycle". It is a real Python feature, it is the right tool here, and using it deliberately with a
one-line explanation reads well. If it makes you uncomfortable, a boolean flag is fine.

### The complete solution

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


def build_with_cycle(values: list[int], cycle_at: int | None = None) -> Node | None:
    """Build a list, optionally joining the tail back to index `cycle_at`."""
    if not values:
        return None
    nodes = [Node(value) for value in values]
    for first, second in zip(nodes, nodes[1:]):
        first.next = second
    if cycle_at is not None:
        nodes[-1].next = nodes[cycle_at]
    return nodes[0]


def has_cycle(head: Node | None) -> bool:
    """Floyd's tortoise and hare. O(n) time, O(1) space.

    A faster runner can only catch a slower one FROM BEHIND on a route that
    returns to itself. Once both are inside the loop, the forward gap between
    them shrinks by exactly one each step, so it cannot skip past zero.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next          # advance first...
        if slow is fast:               # ...then compare, by IDENTITY
            return True
    return False


def find_cycle_start(head: Node | None) -> Node | None:
    """The node where the cycle begins, or None.

    Why phase two works, in four lines:
        a = head to cycle start, b = cycle start to meeting, c = cycle length
        slow walked a + b ; fast walked 2(a + b) = a + b + kc
        so a + b = kc, therefore a = kc - b
        => from the meeting point, a more steps lands exactly on the start
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break
    else:
        return None                    # fell off the end: no cycle

    finder = head
    while finder is not slow:          # guaranteed to meet within `a` steps
        finder = finder.next
        slow = slow.next
    return finder


def cycle_length(head: Node | None) -> int:
    """The number of nodes in the cycle, or 0 if there is none."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            length, node = 1, slow.next
            while node is not slow:
                node = node.next
                length += 1
            return length
    return 0


def has_cycle_with_a_set(head: Node | None) -> Node | None:
    """The obvious solution: O(n) time, O(n) SPACE. Name it, then improve on it.

    At a million nodes this set holds a million references — about 32 MB — to
    answer a question that needs two variables.
    """
    seen: set[int] = set()
    node = head
    while node is not None:
        if id(node) in seen:
            return node
        seen.add(id(node))
        node = node.next
    return None


def find_duplicate(numbers: list[int]) -> int:
    """LeetCode 287, which is this algorithm in disguise.

    n + 1 values, each in 1..n, exactly one repeated. Read the array as a
    function: from index i, go to index numbers[i]. Values stay in range, so
    the walk can never leave the array and must eventually repeat — a rho
    shape. The repeated VALUE is the entrance to the cycle.

    O(n) time, O(1) space, and the input is never modified.
    """
    slow = fast = numbers[0]
    while True:
        slow = numbers[slow]
        fast = numbers[numbers[fast]]
        if slow == fast:
            break

    finder = numbers[0]
    while finder != slow:
        finder = numbers[finder]
        slow = numbers[slow]
    return finder


if __name__ == "__main__":
    straight = build_with_cycle([1, 2, 3, 4, 5])
    looped = build_with_cycle([1, 2, 3, 4, 5, 6], cycle_at=2)   # cycle starts at node 3

    print(has_cycle(straight), has_cycle(looped))          # False True
    print(has_cycle(None), has_cycle(build_with_cycle([1])))  # False False

    print(find_cycle_start(straight))                      # None
    print(find_cycle_start(looped))                        # Node(3)
    print(cycle_length(looped), cycle_length(straight))    # 4 0

    self_loop = build_with_cycle([1], cycle_at=0)          # a node pointing at itself
    print(has_cycle(self_loop), find_cycle_start(self_loop), cycle_length(self_loop))
    # True Node(1) 1

    whole_loop = build_with_cycle([1, 2, 3], cycle_at=0)   # the entire list is the cycle
    print(find_cycle_start(whole_loop), cycle_length(whole_loop))    # Node(1) 3

    print(has_cycle_with_a_set(looped))                    # Node(3)  — same answer, O(n) space

    print(find_duplicate([1, 3, 4, 2, 2]))                 # 2
    print(find_duplicate([3, 1, 3, 4, 2]))                 # 3
    print(find_duplicate([2, 2, 2, 2, 2]))                 # 2

    # the two implementations must agree, on every shape
    import random
    for _ in range(2000):
        size = random.randint(1, 12)
        values = list(range(size))
        at = random.choice([None] + list(range(size)))
        head = build_with_cycle(values, at)
        expected = None if at is None else head
        for _ in range(at or 0):
            expected = expected.next
        assert find_cycle_start(head) is expected
        assert has_cycle_with_a_set(head) is expected
    print("Floyd's and the set version agreed on 2000 random shapes")
```

The three edge cases in the middle are the ones interviewers reach for: a single node pointing at
itself, and a list where the entire thing is the cycle so `a = 0` and phase two must return the head
immediately without moving.

---

## 6. What it costs

### Time

**Phase one.** Before either pointer enters the cycle, `slow` walks `a` steps. Once both are in the
cycle, the gap between them shrinks by one per step, and the gap is at most `c`, so they meet within
`c` more steps. So phase one is at most `a + c` iterations of `slow`, and `a + c ≤ n`.

```
 phase one:  <= a + c steps   ->  O(n)
 phase two:  exactly a steps  ->  O(n)
 total:      O(n)
```

Say it as "at most `a + c`, which is at most `n`" rather than waving at O(n). The bound on phase one
being `c` and not something worse is the part that needs the shrinking-gap argument.

### Space

```
 slow, fast, finder:  three references  ->  O(1)
```

That is the entire point of the algorithm, and it is what you are being asked for. Against the set
version:

```
 n = 1,000,000
   set of node references:  ~32 MB
   Floyd's:                 three variables
```

### Against the alternatives

```
 hash set of nodes      O(n) time,  O(n) space,  start is free, no proof needed
 Floyd's                O(n) time,  O(1) space,  start needs 3 more lines and a proof
 mark visited nodes     O(n) time,  O(1) space,  but MUTATES the input — usually forbidden
```

The third one is worth naming and rejecting: adding a `visited` flag to each node, or reversing links
as you go, works and destroys the caller's data. If the interviewer says "you may modify the list", it
becomes a legitimate answer.

### The duplicate-number version

```
 array of n+1 values in 1..n
 sorting:                    O(n log n) time, and it mutates the array
 a set of seen values:       O(n) time, O(n) space
 marking with negatives:     O(n) time, O(1) space, but mutates
 Floyd's on index -> value:  O(n) time, O(1) space, no mutation
```

Only the last one satisfies all three constraints the problem states, which is why the problem is
stated with all three.

---

## 7. The traps

### Trap 1 — comparing values instead of identity

```python
        if slow == fast:                     # WRONG for arbitrary node objects
```

`==` on two different `Node` objects falls back to identity in Python *unless* someone has defined
`__eq__` — and the moment somebody does, on values, this reports a cycle whenever two nodes hold the
same number. **Write `is`.** It is also clearer about what you mean.

### Trap 2 — comparing before advancing

```python
    while fast is not None and fast.next is not None:
        if slow is fast:                     # both start on the head
            return True
        slow, fast = slow.next, fast.next.next
```

Returns `True` for every non-empty list, immediately. Advance first, then compare.

### Trap 3 — returning the meeting point as the cycle start

```python
        if slow is fast:
            return slow                      # this is NOT the entrance
```

On the six-node example the meeting is at node 5 and the entrance is node 3. It happens to be right
only when `a = 0`, meaning the whole list is one cycle — which is exactly the test case people use, so
this bug survives casual testing.

### Trap 4 — the loop condition in the wrong order

```python
    while fast.next is not None and fast is not None:
```

```
AttributeError: 'NoneType' object has no attribute 'next'
```

on any list without a cycle whose length is even. `and` short-circuits left to right, so the null
check must be first. Same trap as [day 082](../day-082-runner-technique/README.md), and it will keep
being the same trap.

### Trap 5 — a safety counter in phase two

```python
    steps = 0
    while finder is not slow and steps < 1_000_000:      # do not do this
```

The arithmetic guarantees they meet within `a` steps. Adding a guard says you do not trust the proof,
and if phase one was correct the guard can never fire. If you *want* a guard, put an `assert` on the
result instead — that documents the invariant rather than hiding a bug.

### Trap 6 — assuming the fast pointer cannot jump over the slow one

The most common gap in an otherwise good explanation. It cannot, and the reason is that the forward
gap shrinks by **exactly one** each step, so it must pass through zero. Note this is specific to the
2:1 ratio: at 3:1 the gap shrinks by two and could indeed step from 1 to −1 on an odd-length cycle.
Being able to say that is a genuine sign of understanding.

### Trap 7 — modifying the list to detect the cycle

Marking nodes as visited, or reversing links as you walk, both work and both destroy the caller's
data. If the list is shared, or the caller uses it afterwards, this is a serious bug and it is
invisible in a test that only checks the boolean. Ask before mutating.

### Trap 8 — the two degenerate shapes

A single node pointing at itself: `a = 0`, `b = 0`, `c = 1`, and phase two must return the head without
moving. A list where the entire thing is the cycle: `a = 0` again. Both are the cases where "return
the meeting point" accidentally works, so run them last to catch that bug rather than first.

---

## 8. In the interview

### How it gets asked

- The base: *"Does this linked list have a cycle?"* LeetCode 141. Usually five minutes.
- The real question: *"Now return the node where the cycle begins."* LeetCode 142 — and then *"why does
  that work?"*
- The constraint version: *"Can you do it without extra space?"* — which is the hint that the set
  solution is not what they want.
- The disguised version, which is genuinely hard: *"Given an array of n+1 integers each between 1 and
  n, find the duplicate, without modifying the array and in O(1) space."* LeetCode 287.
- The proof probe: *"Why must they meet? Could the fast one jump over the slow one?"*

### What to say out loud, in the first ninety seconds

1. **Give the O(n)-space answer first, as the baseline.** "The obvious solution is a set of visited
   nodes — O(n) time and O(n) space, and it gives me the entrance for free. Let me improve the space."
2. **State the shape.** "A list with a cycle is a tail followed by a loop — a rho shape. So either a
   walk falls off the end, or it goes round for ever."
3. **State the detection rule and *why*, not just the mechanics.** "Two pointers, one at single speed
   and one at double. If the list ends, the fast one falls off. If it loops, the fast one comes up
   *behind* the slow one — and a faster runner can only catch a slower one from behind on a route that
   returns to itself."
4. **Pre-empt the skipping objection.** "They cannot pass each other: once both are in the loop, the
   forward gap shrinks by exactly one per step, so it has to hit zero."
5. **Then the entrance, with the arithmetic offered.** "For the start of the cycle, put one pointer
   back at the head and move both at single speed — they meet at the entrance. I can show you why in
   about four lines if you want."
6. **State the costs.** "O(n) time, O(1) space, and I do not modify the list."

### The follow-ups

**"Why does phase two work?"**
"Call `a` the distance from the head to the cycle start, `b` the distance from the cycle start to the
meeting point, and `c` the cycle length. When they meet, slow has walked `a + b` and fast has walked
twice that, and fast is in the same place having gone some whole number of extra laps — so
`2(a + b) = a + b + kc`, which gives `a + b = kc`, so `a = kc − b`. That last line says: from the
meeting point, walking `a` more steps takes me `a + b = kc` steps into the cycle, a whole number of
laps, which is exactly the cycle start. And walking `a` steps from the head is the cycle start by
definition. So both pointers arrive there together. In the common case where `k` is one it reads even
more simply: the distance from the head to the entrance equals the distance from the meeting point
round to the entrance."

**"Could the fast pointer skip over the slow one?"**
"No. Once both are inside the loop, look at the gap from fast to slow measured forwards round the
loop. Each step slow gains one and fast gains two, so that gap decreases by exactly one. A quantity
that decreases by exactly one cannot go from 1 to −1 without being 0, so they land on the same node.
That argument depends on the 2:1 ratio — at 3:1 the gap would shrink by two and could step over zero
on an odd-length cycle."

**"Why not just use a hash set?"**
"You can, and I would say so first — O(n) time, O(n) space, and it hands you the entrance with no
proof required. I would not ship it if space matters: at a million nodes the set holds a million
references, about thirty-two megabytes, to answer something two variables can answer. And it is
usually exactly the improvement the question is asking for."

**"What is the time complexity, precisely?"**
"Phase one is at most `a + c` steps of the slow pointer: `a` to enter the cycle, then at most `c` more
because the gap shrinks by one each step and starts below `c`. Phase two is exactly `a`. So at most
`2a + c`, which is at most `2n` — linear, and I would rather give the bound that way than just say
O(n), because the `c` bound is the part that needs the shrinking-gap argument."

**"Find the duplicate number in an array of n+1 values from 1 to n, without modifying it, in O(1)
space."**
"That is this algorithm wearing a costume. Read the array as a function: from index `i`, go to index
`nums[i]`. Every value is between 1 and n, so the walk can never leave the array, and since it is
infinite and the space is finite it must eventually repeat — a rho shape. Two values map to the same
index precisely at the duplicate, so the duplicate is the *entrance* to the cycle, and Floyd's finds
entrances. Start both at index 0, run the tortoise and hare on the mapping, then run phase two. O(n)
time, O(1) space, and the array is untouched — which is why the problem states all three
constraints."

**"Can you find the cycle's length too?"**
"Yes, and it is nearly free once you have the meeting point: stay there and walk forward counting
until you return to it. That is O(c) and no extra space. If you want the length before the entrance,
that also gives an alternative phase two — advance one pointer `c` steps ahead of the other and then
move both together, which lands them at the entrance for the same reason."

### A model answer

Asked: *detect a cycle in a linked list, then find the node where it begins.*

> "Let me give you the obvious answer first so we agree on the baseline. Walk the list, keep a set of
> nodes you have seen, and the first node you meet twice is the entrance. That is O(n) time, O(n)
> space, and it needs no cleverness. If space is not a constraint, I would ship it.
>
> To do it in constant space: a list with a cycle has a definite shape — a straight tail, then a loop —
> so a walk either falls off the end or goes round for ever. I send two pointers, one moving one step
> at a time and one moving two.
>
> If the list ends, the fast pointer reaches `None` and there is no cycle. If it loops, the fast
> pointer comes up *behind* the slow one — and that is the whole insight. A faster runner can only
> catch a slower one from behind on a route that returns to itself. On a route that ends, the fast one
> arrives and waits; there is no behind.
>
> The objection to pre-empt is whether the fast one could jump over the slow one. It cannot. Once both
> are inside the loop, the forward gap from fast to slow shrinks by exactly one every step — slow gains
> one, fast gains two — and a quantity that decreases by exactly one has to pass through zero. That
> depends on the two-to-one ratio, incidentally: at three to one the gap shrinks by two and could step
> over zero on an odd-length cycle.
>
> Two details in the code. I compare with `is`, not `==`, because the question is whether they are on
> the same node, not whether two nodes hold the same value. And I advance both before comparing —
> comparing first would report a cycle immediately, since they start together.
>
> Now the entrance, which is the actual question. Leave the slow pointer at the meeting point, put a
> new pointer at the head, and move both one step at a time. They meet exactly at the cycle start.
>
> Here is why, and it is four lines. Call `a` the distance from the head to the cycle start, `b` the
> distance from the start round to the meeting point, and `c` the cycle length. Slow has walked
> `a + b`. Fast has walked twice that, and ended up in the same place, so it did some whole number of
> extra laps: `2(a + b) = a + b + kc`. Therefore `a + b = kc`, therefore `a = kc − b`. Read the last one
> as an instruction: from the meeting point, `a` more steps takes me `a + b` steps into the cycle,
> which is `kc`, a whole number of laps, landing exactly on the entrance. And `a` steps from the head
> is the entrance by definition. So they arrive together.
>
> With `k = 1` it is easier to picture: the distance from the head to the entrance equals the distance
> from the meeting point round to the entrance.
>
> Complexity: phase one is at most `a + c` steps, because the gap shrinks by one and starts below the
> cycle length; phase two is exactly `a`. So at most about `2n` — linear time, three variables of
> space, and I never modify the list, which matters because marking nodes as visited would also work
> and would destroy the caller's data.
>
> Two cases I would run before saying I am done: a single node pointing at itself, and a list where
> the whole thing is one cycle. In both, `a` is zero and phase two must return the head without moving
> — and those are the two cases where the wrong answer, returning the meeting point, happens to look
> correct."

---

## 9. Recall card

- **A list with a cycle is a tail plus a loop — a rho shape.** Two runners, **one step and two steps**.
  Fast falls off the end → no cycle. Fast catches slow **from behind** → cycle, because *a faster
  runner can only catch a slower one from behind on a route that returns to itself.* Compare with
  **`is`, not `==`**, and **advance before comparing**.
- **They cannot skip past each other: inside the loop the forward gap shrinks by exactly one per
  step**, so it must hit zero. That argument needs the **2:1 ratio** — at 3:1 the gap falls by two and
  could step over zero on an odd cycle.
- **Phase two, and the proof is four lines.** `a` = head → start, `b` = start → meeting, `c` = cycle
  length. slow walked `a + b`; fast walked `2(a+b) = a+b+kc`; so **`a + b = kc`**, so **`a = kc − b`**.
  Hence from the meeting point, `a` more steps = a whole number of laps = the entrance. Put one
  pointer back at the **head**, move both at **single speed**, they meet at the start. **No safety
  counter** — the arithmetic guarantees it.
- **The meeting point is NOT the entrance** (it only looks right when `a = 0`, which is exactly the
  test case people try). Run the two degenerate shapes last: **one node pointing at itself**, and **a
  list that is entirely one cycle**.
- **Costs: phase one ≤ `a + c`, phase two exactly `a`, so ≤ 2n — O(n) time, O(1) space, no mutation.**
  Name the **hash-set** baseline first (O(n) space, ~32 MB at a million nodes, entrance for free) and
  then improve it; reject **marking nodes** because it destroys the caller's data. The disguise to
  recognise: **Find the Duplicate Number** — read the array as `i → nums[i]`, the walk can never leave
  the array, and the **duplicate is the entrance**.
